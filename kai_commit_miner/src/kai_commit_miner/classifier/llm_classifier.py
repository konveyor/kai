"""Orchestrate LLM calls for hint generation and rule candidate discovery.

Strategy:
- Group attributed fixes by violation key
- Within each group, cluster by similarity (same file pattern, same message)
- Generate one hint per cluster (covers similar incidents)
- Generate one rollup hint per violation type (covers the overall pattern)
- Track accumulated hints so the LLM can skip/refine across commit pairs
"""

import json
import sys
from collections import defaultdict

import yaml
from langchain_core.language_models.chat_models import BaseChatModel

from kai_commit_miner.attribution.models import AttributedFix, UnattributedChange
from kai_commit_miner.classifier.models import (
    ClassificationResult,
    HintCandidate,
    MigrationRelevance,
    RuleCandidate,
)
from kai_commit_miner.classifier.prompts import (
    build_hint_prompt,
    build_rule_discovery_prompt,
)
from kai_mcp_solution_server.db.python_objects import ViolationID


class LLMClassifier:
    """Classifies attributed fixes into hints and discovers new rule candidates.

    Maintains state across commit pairs to avoid regenerating identical hints.
    """

    def __init__(
        self,
        model: BaseChatModel,
        migration_description: str,
        known_rulesets: list[str],
    ) -> None:
        self.model = model
        self.migration_description = migration_description
        self.known_rulesets = known_rulesets
        self._accumulated_hints: dict[ViolationID, str] = {}
        self._known_violation_names: set[str] = set()
        # LLM call tracking
        self.llm_calls: int = 0
        self.input_tokens: int = 0
        self.output_tokens: int = 0

    def _track_usage(self, response: object) -> None:
        """Extract token usage from LLM response metadata if available."""
        usage = getattr(response, "usage_metadata", None)
        if usage and isinstance(usage, dict):
            self.input_tokens += usage.get("input_tokens", 0)
            self.output_tokens += usage.get("output_tokens", 0)
        elif hasattr(response, "response_metadata"):
            meta = response.response_metadata  # type: ignore[union-attr]
            if isinstance(meta, dict) and "usage" in meta:
                u = meta["usage"]
                self.input_tokens += u.get("input_tokens", u.get("prompt_tokens", 0))
                self.output_tokens += u.get(
                    "output_tokens", u.get("completion_tokens", 0)
                )

    async def classify_commit_pair(
        self,
        attributed_fixes: list[AttributedFix],
        unattributed_changes: list[UnattributedChange],
        commit_before: str,
        commit_after: str,
    ) -> ClassificationResult:
        hints: list[HintCandidate] = []
        rule_candidates: list[RuleCandidate] = []

        # Group fixes by violation key
        fixes_by_violation: dict[ViolationID, list[AttributedFix]] = defaultdict(list)
        for fix in attributed_fixes:
            fixes_by_violation[fix.violation_key].append(fix)
            self._known_violation_names.add(fix.violation_key.violation_name)

        # Process each violation type
        for viol_key, fixes in fixes_by_violation.items():
            # Skip LLM call entirely if we already have a hint and ALL fixes
            # in this commit are indirect (no new code patterns to learn from)
            existing = self._accumulated_hints.get(viol_key)
            has_direct_fixes = any(not f.indirect for f in fixes)

            if existing and not has_direct_fixes:
                print(
                    f"    {viol_key.violation_name}: skipped locally "
                    f"({len(fixes)} indirect, hint exists)",
                    file=sys.stderr,
                )
                hints.append(
                    HintCandidate(
                        violation_key=viol_key,
                        hint_text=existing,
                        incident_count=len(fixes),
                        sample_fixes=fixes[:3],
                        skipped=True,
                        skipped_reason="All fixes indirect, hint already exists",
                    )
                )
                continue

            violation_desc = ""
            for f in fixes:
                if f.incident.violation_description:
                    violation_desc = f.incident.violation_description
                    break

            # Cluster by incident message to identify distinct sub-patterns
            clusters = _cluster_fixes(fixes)

            if len(clusters) == 1:
                hint = await self._generate_hint(
                    viol_key,
                    violation_desc,
                    fixes,
                    commit_before,
                    commit_after,
                )
                if hint:
                    hints.append(hint)
            else:
                print(
                    f"    {viol_key.violation_name}: {len(clusters)} distinct patterns "
                    f"across {len(fixes)} incidents",
                    file=sys.stderr,
                )
                for cluster_key, cluster_fixes in clusters.items():
                    # Also skip clusters where all fixes are indirect
                    if existing and not any(not f.indirect for f in cluster_fixes):
                        print(
                            f"    {viol_key.violation_name} [{cluster_key[:60]}]: "
                            f"skipped locally (indirect)",
                            file=sys.stderr,
                        )
                        continue
                    hint = await self._generate_hint(
                        viol_key,
                        violation_desc,
                        cluster_fixes,
                        commit_before,
                        commit_after,
                        cluster_label=cluster_key,
                    )
                    if hint:
                        hints.append(hint)

        # Discover new rule candidates
        if unattributed_changes:
            candidates = await self._discover_rules(
                unattributed_changes,
                commit_before,
                commit_after,
            )
            rule_candidates.extend(candidates)

        return ClassificationResult(
            commit_before=commit_before,
            commit_after=commit_after,
            hints=hints,
            rule_candidates=rule_candidates,
        )

    async def _generate_hint(
        self,
        viol_key: ViolationID,
        violation_desc: str,
        fixes: list[AttributedFix],
        commit_before: str,
        commit_after: str,
        cluster_label: str | None = None,
    ) -> HintCandidate | None:
        """Generate a hint for a group of fixes. Returns None on failure."""
        existing = self._accumulated_hints.get(viol_key)

        prompt = build_hint_prompt(
            migration_description=self.migration_description,
            violation_key=viol_key,
            violation_description=violation_desc,
            attributed_fixes=fixes,
            commit_before=commit_before,
            commit_after=commit_after,
            existing_hint=existing,
        )

        try:
            self.llm_calls += 1
            response = await self.model.ainvoke(prompt)
            self._track_usage(response)
            hint_text = str(response.content).strip()

            # Check if LLM decided to skip
            if hint_text.startswith("SKIP:"):
                reason = hint_text[5:].strip()
                label = f" [{cluster_label}]" if cluster_label else ""
                print(
                    f"    {viol_key.violation_name}{label}: skipped ({reason})",
                    file=sys.stderr,
                )
                return HintCandidate(
                    violation_key=viol_key,
                    hint_text=existing or "",
                    incident_count=len(fixes),
                    sample_fixes=fixes[:3],
                    skipped=True,
                    skipped_reason=reason,
                )

            # Store as the latest hint for this violation type
            self._accumulated_hints[viol_key] = hint_text

            return HintCandidate(
                violation_key=viol_key,
                hint_text=hint_text,
                incident_count=len(fixes),
                sample_fixes=fixes[:3],
            )

        except Exception as e:
            print(
                f"Warning: hint generation failed for {viol_key}: {e}",
                file=sys.stderr,
            )
            return None

    async def _discover_rules(
        self,
        unattributed_changes: list[UnattributedChange],
        commit_before: str,
        commit_after: str,
    ) -> list[RuleCandidate]:
        prompt = build_rule_discovery_prompt(
            migration_description=self.migration_description,
            known_rulesets=self.known_rulesets,
            known_violation_names=sorted(self._known_violation_names),
            unattributed_changes=unattributed_changes,
            commit_before=commit_before,
            commit_after=commit_after,
        )

        try:
            self.llm_calls += 1
            response = await self.model.ainvoke(prompt)
            self._track_usage(response)
            return _parse_rule_candidates(str(response.content), commit_after)
        except Exception as e:
            print(f"Warning: rule discovery failed: {e}", file=sys.stderr)
            return []


def _cluster_fixes(fixes: list[AttributedFix]) -> dict[str, list[AttributedFix]]:
    """Cluster fixes by incident message to identify distinct sub-patterns.

    Returns a dict of cluster_key -> fixes. If all messages are the same
    (or very similar), returns a single cluster.
    """
    clusters: dict[str, list[AttributedFix]] = defaultdict(list)
    for fix in fixes:
        # Use the first ~60 chars of the message as the cluster key
        # This groups "Replace javax.ejb.Stateless" with "Replace javax.ejb.Stateless"
        # but separates it from "Replace javax.persistence.Entity"
        key = fix.incident.message[:60].strip()
        clusters[key].append(fix)

    # If we ended up with too many tiny clusters, collapse them
    # (e.g., 50 unique messages with 1 incident each isn't useful)
    if len(clusters) > 10 and all(len(v) <= 2 for v in clusters.values()):
        return {"all": fixes}

    return dict(clusters)


def _parse_rule_candidates(content: str, source_commit: str) -> list[RuleCandidate]:
    """Parse LLM response (YAML analyzer-lsp rules) into RuleCandidate objects."""
    cleaned = content.strip()

    # Extract from code blocks
    if "```yaml" in cleaned:
        start = cleaned.index("```yaml") + 7
        end = cleaned.index("```", start)
        cleaned = cleaned[start:end].strip()
    elif "```" in cleaned:
        start = cleaned.index("```") + 3
        end = cleaned.index("```", start)
        cleaned = cleaned[start:end].strip()

    # Try YAML first (the new format), fall back to JSON (the old format)
    data = None
    try:
        data = yaml.safe_load(cleaned)
    except Exception:
        pass

    if data is None:
        try:
            data = json.loads(cleaned)
        except Exception:
            return []

    if not isinstance(data, list):
        return []

    candidates: list[RuleCandidate] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        # Extract the 'when' condition as YAML string for storage
        when_condition = item.get("when", {})
        when_yaml = (
            yaml.dump(when_condition, default_flow_style=False).strip()
            if when_condition
            else ""
        )

        # Extract links
        links = []
        for link in item.get("links", []):
            if isinstance(link, dict):
                links.append(
                    {"url": link.get("url", ""), "title": link.get("title", "")}
                )

        candidate = RuleCandidate(
            ruleID=item.get("ruleID", ""),
            description=item.get("description", ""),
            category=item.get("category", "potential"),
            effort=int(item.get("effort", 1)),
            message=item.get("message", ""),
            labels=item.get("labels", []),
            when_yaml=when_yaml,
            links=links,
            migration_relevance=_parse_relevance(
                item.get("migration_relevance", "medium")
            ),
            relevance_reasoning=str(item.get("relevance_reasoning", "")),
            source_file=item.get("source_file", ""),
            source_commit=source_commit,
        )
        _validate_rule(candidate)
        candidates.append(candidate)
    return candidates


def _relevance_from_float(v: float) -> MigrationRelevance:
    if v >= 0.8:
        return MigrationRelevance.HIGH
    elif v >= 0.5:
        return MigrationRelevance.MEDIUM
    elif v >= 0.2:
        return MigrationRelevance.LOW
    return MigrationRelevance.VERY_LOW


def _parse_relevance(value: object) -> MigrationRelevance:
    """Parse a relevance value from LLM output, handling strings, floats, etc."""
    if isinstance(value, str):
        v = value.strip().lower().replace(" ", "_")
        try:
            return MigrationRelevance(v)
        except ValueError:
            pass
        try:
            return _relevance_from_float(float(v))
        except ValueError:
            pass
    elif isinstance(value, (int, float)):
        return _relevance_from_float(float(value))
    return MigrationRelevance.MEDIUM


def _validate_rule(candidate: RuleCandidate) -> None:
    """Check structural quality of a generated rule and populate validation_notes."""
    notes: list[str] = []

    if not candidate.ruleID:
        notes.append("missing ruleID")
    if not candidate.when_yaml or candidate.when_yaml in ("{}", "null", "''"):
        notes.append("missing when condition")
    else:
        has_specific_condition = any(
            kw in candidate.when_yaml
            for kw in [
                "java.referenced",
                "java.dependency",
                "builtin.filecontent",
                "builtin.xml",
                "builtin.file",
                "builtin.json",
            ]
        )
        if not has_specific_condition:
            notes.append("when condition may not be a valid analyzer-lsp provider")
    if not candidate.message:
        notes.append("missing message")
    if not candidate.labels:
        notes.append("missing labels")

    candidate.validation_notes = notes

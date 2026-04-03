"""Top-level orchestrator for the commit mining pipeline.

Simple model: diff two refs, attribute resolved violations, classify once per
violation type. No commit-by-commit walking.
"""

import asyncio
import sys
from dataclasses import dataclass, field
from typing import Union

from langchain.chat_models import init_chat_model
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.chat_models import BaseChatModel

from kai_commit_miner.analyzer.base import AnalyzerBackend
from kai_commit_miner.analyzer.cache import AnalysisCache
from kai_commit_miner.analyzer.kantra import KantraBackend
from kai_commit_miner.analyzer.precomputed import PrecomputedBackend
from kai_commit_miner.attribution.fix_attributor import attribute_fixes
from kai_commit_miner.attribution.models import AttributedFix, UnattributedChange
from kai_commit_miner.classifier.llm_classifier import LLMClassifier
from kai_commit_miner.client.solution_server import DryRunClient, SolutionServerClient
from kai_commit_miner.config import AnalyzerBackendType, MinerSettings
from kai_commit_miner.diff.report_differ import diff_reports
from kai_commit_miner.git.diff_parser import FileDiff, parse_unified_diff
from kai_commit_miner.git.repo import GitRepo
from kai_commit_miner.migration_inferrer import (
    MigrationInfo,
    get_available_labels,
    infer_migration,
)
from kai_mcp_solution_server.analyzer_types import AnalysisReport


def _normalize_uri(uri: str, worktree_path: str) -> str:
    """Normalize a kantra incident URI to a repo-relative path."""
    from urllib.parse import urlparse

    from kai_mcp_solution_server.analyzer_types import remove_known_prefixes

    if uri.startswith("file://"):
        uri = urlparse(uri).path

    if worktree_path and uri.startswith(worktree_path):
        uri = uri[len(worktree_path) :]
        if uri.startswith("/"):
            uri = uri[1:]
        return uri

    return remove_known_prefixes(uri)


def _normalize_report_uris(report: AnalysisReport, worktree_path: str) -> None:
    """Normalize all incident URIs in an analysis report in-place."""
    for ruleset in report.root:
        if not ruleset.violations:
            continue
        for violation in ruleset.violations.values():
            if not violation.incidents:
                continue
            for incident in violation.incidents:
                incident.uri = _normalize_uri(incident.uri, worktree_path)


def _add_rename_summary(
    unattributed: list[UnattributedChange],
    renames: list["FileDiff"],
) -> None:
    """Summarize bulk renames as a synthetic unattributed change.

    Instead of sending 2500 individual rename entries to the LLM,
    group by common prefix change and add one summary entry per pattern.
    """
    from collections import Counter

    from kai_commit_miner.git.diff_parser import DiffHunk

    patterns: Counter[tuple[str, str]] = Counter()
    for fd in renames:
        old_parts = fd.old_path.split("/")
        new_parts = fd.new_path.split("/")
        # Find the first diverging directory
        common_len = 0
        for o, n in zip(old_parts, new_parts):
            if o == n:
                common_len += 1
            else:
                old_prefix = "/".join(old_parts[: common_len + 1])
                new_prefix = "/".join(new_parts[: common_len + 1])
                patterns[(old_prefix, new_prefix)] += 1
                break

    for (old_prefix, new_prefix), count in patterns.most_common():
        summary = (
            f"# {count} files renamed: {old_prefix}/ -> {new_prefix}/\n"
            f"# This is a directory structure migration pattern.\n"
            f"# Example: {renames[0].old_path} -> {renames[0].new_path}"
        )
        unattributed.append(
            UnattributedChange(
                file_path=f"{old_prefix}/ (rename pattern)",
                hunks=[
                    DiffHunk(
                        old_start=0,
                        old_count=0,
                        new_start=0,
                        new_count=0,
                        content=summary,
                    )
                ],
            )
        )


@dataclass
class MiningReport:
    """Summary of a mining run."""

    violations_resolved: int = 0
    hints_generated: int = 0
    rule_candidates_found: int = 0
    errors: list[str] = field(default_factory=list)


class MiningPipeline:
    """Orchestrates the commit mining workflow.

    Takes two git refs (before/after migration), diffs the analysis reports
    and code, then generates hints and rules -- one LLM call per violation type.
    """

    def __init__(self, settings: MinerSettings) -> None:
        self.settings = settings
        self.repo = GitRepo(settings.repo_path)
        self.analyzer = self._create_analyzer()
        self.cache = AnalysisCache(settings.cache_dir)
        self._config_hash = AnalysisCache.compute_config_hash(
            settings.analyzer_config_path
        )

    def _create_analyzer(self) -> AnalyzerBackend | None:
        if self.settings.analyzer_backend == AnalyzerBackendType.NONE:
            return None
        elif self.settings.analyzer_backend == AnalyzerBackendType.KANTRA:
            return KantraBackend()
        elif self.settings.analyzer_backend == AnalyzerBackendType.PRECOMPUTED:
            return PrecomputedBackend()
        else:
            raise ValueError(
                f"Unknown analyzer backend: {self.settings.analyzer_backend}"
            )

    def _create_model(self) -> BaseChatModel:
        if self.settings.llm_params is None:
            raise ValueError("LLM parameters must be provided")
        if self.settings.llm_params.get("model") == "fake":
            params = self.settings.llm_params.copy()
            params.pop("model", None)
            if "responses" not in params:
                params["responses"] = ["[]"]
            return FakeListChatModel(**params)
        return init_chat_model(**self.settings.llm_params)

    async def _analyze_commit(self, commit_hash: str) -> AnalysisReport:
        """Analyze a single commit, using cache if available."""
        assert self.analyzer is not None

        cached = self.cache.get(commit_hash, self._config_hash)
        if cached is not None:
            print(f"  Cache hit for {commit_hash[:8]}", file=sys.stderr)
            return cached

        print(f"  Analyzing {commit_hash[:8]}...", file=sys.stderr)
        worktree = await asyncio.to_thread(self.repo.create_worktree, commit_hash)
        try:
            analysis = await self.analyzer.analyze(worktree, self.settings, commit_hash)
            _normalize_report_uris(analysis, str(worktree))
            self.cache.put(commit_hash, self._config_hash, analysis)
            return analysis
        finally:
            await asyncio.to_thread(self.repo.remove_worktree, worktree)

    async def run(self) -> MiningReport:
        """Execute the mining pipeline.

        1. Resolve the two refs (start_commit, end_commit)
        2. Infer migration from manifest diffs
        3. Optionally run analysis on both refs, diff reports
        4. Get the full git diff
        5. Attribute resolved violations to diff hunks
        6. One LLM call per violation type (preferring larger diffs)
        7. One LLM call for unattributed changes (rule discovery)
        """
        report = MiningReport()

        start_ref = self.settings.start_commit
        end_ref = self.settings.end_commit
        if not start_ref or not end_ref:
            raise ValueError("Both --start-commit and --end-commit are required")

        # Resolve short refs to full hashes
        start_hash = self.repo._run("rev-parse", start_ref).strip()
        end_hash = self.repo._run("rev-parse", end_ref).strip()
        print(f"Mining: {start_hash[:8]} -> {end_hash[:8]}", file=sys.stderr)

        model = self._create_model()

        # Step 1: Infer migration
        migration_info: MigrationInfo
        if self.settings.migration_description:
            migration_info = MigrationInfo(
                description=self.settings.migration_description
            )
        else:
            print("Inferring migration...", file=sys.stderr)
            available_targets: list[str] | None = None
            available_sources: list[str] | None = None
            if self.analyzer is not None:
                try:
                    available_targets, available_sources = get_available_labels(
                        self.settings.kantra_binary
                    )
                except Exception:
                    pass

            migration_info = await infer_migration(
                self.repo,
                start_hash,
                end_hash,
                model,
                available_targets=available_targets,
                available_sources=available_sources,
            )
            print(f"  {migration_info.description[:200]}", file=sys.stderr)
            if migration_info.label_selector:
                print(f"  Labels: {migration_info.label_selector}", file=sys.stderr)
                if not self.settings.analyzer_label_selector:
                    self.settings.analyzer_label_selector = (
                        migration_info.label_selector
                    )

        migration_desc = migration_info.description

        # Step 2: Analysis (if enabled)
        known_rulesets: list[str] = []
        resolved_violations = []

        if self.analyzer is not None:
            print("Analyzing before and after states...", file=sys.stderr)
            try:
                report_before = await self._analyze_commit(start_hash)
                report_after = await self._analyze_commit(end_hash)
                report_diff = diff_reports(
                    report_before, report_after, start_hash, end_hash
                )
                resolved_violations = report_diff.resolved
                known_rulesets = [rs.name or "" for rs in report_before.root if rs.name]
                print(
                    f"  {len(resolved_violations)} violations resolved", file=sys.stderr
                )
            except Exception as e:
                msg = f"Analysis failed: {e}"
                print(f"  ERROR: {msg}", file=sys.stderr)
                report.errors.append(msg)
                if self.settings.analyzer_backend != AnalyzerBackendType.NONE:
                    print(
                        "  Use --analyzer-backend none to skip analysis.",
                        file=sys.stderr,
                    )
                    return report
        else:
            print("Analysis: skipped (no backend)", file=sys.stderr)

        report.violations_resolved = len(resolved_violations)

        # Step 3: Get the full git diff
        print("Getting diff...", file=sys.stderr)
        git_diff_text = await asyncio.to_thread(
            self.repo.get_diff, start_hash, end_hash
        )
        file_diffs = parse_unified_diff(git_diff_text)
        print(f"  {len(file_diffs)} files changed", file=sys.stderr)

        # Step 4: Attribute violations to diff hunks
        if resolved_violations:
            attributed, unattributed = attribute_fixes(
                resolved_violations,
                file_diffs,
                self.repo,
                start_hash,
                end_hash,
            )
            direct = sum(1 for f in attributed if not f.indirect)
            print(
                f"  {direct} direct attributions, "
                f"{len(attributed) - direct} indirect, "
                f"{len(unattributed)} unattributed file changes",
                file=sys.stderr,
            )
        else:
            # No analysis -- everything is unattributed
            attributed = []
            unattributed = [
                UnattributedChange(file_path=fd.new_path, hunks=fd.hunks)
                for fd in file_diffs
                if fd.hunks
            ]
            # Summarize rename patterns as synthetic unattributed changes
            renames = [fd for fd in file_diffs if fd.is_renamed and not fd.hunks]
            if renames:
                _add_rename_summary(unattributed, renames)
            print(
                f"  {len(unattributed)} file changes (all unattributed)",
                file=sys.stderr,
            )

        # Step 5: Classify with LLM
        print("Classifying with LLM...", file=sys.stderr)
        classifier = LLMClassifier(
            model=model,
            migration_description=migration_desc,
            known_rulesets=known_rulesets,
            max_prompt_tokens=self.settings.max_prompt_tokens,
        )

        classification = await classifier.classify_commit_pair(
            attributed,
            unattributed,
            start_hash,
            end_hash,
        )

        report.hints_generated = len(classification.hints)
        report.rule_candidates_found = len(classification.rule_candidates)

        # Print LLM usage
        cost = (classifier.input_tokens * 3 + classifier.output_tokens * 15) / 1_000_000
        token_info = ""
        if classifier.input_tokens > 0:
            token_info = (
                f"{classifier.input_tokens:,} in / {classifier.output_tokens:,} out, "
            )
        print(
            f"  {classifier.llm_calls} LLM calls, {token_info}${cost:.2f}",
            file=sys.stderr,
        )

        # Step 6: Save results
        client: Union[SolutionServerClient, DryRunClient]
        collection_id: int | None = None

        if self.settings.dry_run:
            client = DryRunClient(self.settings.dry_run_output_dir)
            client.set_metadata("migration_description", migration_desc)
            client.set_metadata("inferred", self.settings.migration_description is None)
            client.set_metadata("source_labels", migration_info.source_labels)
            client.set_metadata("target_labels", migration_info.target_labels)
            client.set_metadata("label_selector", migration_info.label_selector)
            client.set_metadata("start_commit", start_hash)
            client.set_metadata("end_commit", end_hash)
            client.set_metadata("violations_resolved", len(resolved_violations))
            client.set_metadata("files_changed", len(file_diffs))
        else:
            client = SolutionServerClient(
                self.settings.solution_server_url,
                self.settings.solution_server_client_id,
            )
            try:
                collection_id = await client.create_collection(
                    name=f"miner-{self.settings.repo_path.name}-{self._config_hash[:8]}",
                    description=migration_desc,
                    source_repo=str(self.settings.repo_path),
                    migration_type=migration_desc,
                )
            except Exception as e:
                print(f"Warning: failed to create collection: {e}", file=sys.stderr)

        await client.push_classification(classification, collection_id=collection_id)
        await client.close()

        return report

"""Infer migration description and analysis label selectors from manifest diffs."""

import asyncio
import json
import sys
from dataclasses import dataclass, field

from langchain_core.language_models.chat_models import BaseChatModel

from kai_commit_miner.git.repo import GitRepo

MANIFEST_PATTERNS = [
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "package.json",
    "go.mod",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "Gemfile",
]


@dataclass
class MigrationInfo:
    """Result of migration inference."""

    description: str
    source_labels: list[str] = field(default_factory=list)
    target_labels: list[str] = field(default_factory=list)
    label_selector: str = ""


async def infer_migration(
    repo: GitRepo,
    first_commit: str,
    last_commit: str,
    model: BaseChatModel,
    base_branch: str = "main",
    available_targets: list[str] | None = None,
    available_sources: list[str] | None = None,
) -> MigrationInfo:
    """Infer migration description and kantra label selectors from manifest diffs."""
    merge_base = await asyncio.to_thread(
        _find_merge_base, repo, first_commit, base_branch
    )

    diff_from = merge_base or first_commit
    manifest_diff = await asyncio.to_thread(
        _get_manifest_diff, repo, diff_from, last_commit
    )

    if not manifest_diff:
        manifest_diff = await asyncio.to_thread(
            _get_diff_summary, repo, diff_from, last_commit
        )

    # Build the prompt -- ask for both description and label matching
    targets_section = ""
    sources_section = ""
    if available_targets:
        targets_section = (
            "\n## Available analysis targets\n"
            "Pick ALL that apply from this list:\n"
            f"{', '.join(available_targets)}\n"
        )
    if available_sources:
        sources_section = (
            "\n## Available analysis sources\n"
            "Pick ALL that apply from this list:\n"
            f"{', '.join(available_sources)}\n"
        )

    prompt = (
        "You are analyzing a code repository's commit history to understand what "
        "migration is being performed.\n\n"
        "Below are the changes to dependency/build manifest files between the "
        "pre-migration state and the latest migration commit.\n\n"
        f"## Manifest changes\n```diff\n{manifest_diff}\n```\n"
        f"{targets_section}{sources_section}\n"
        "Respond with ONLY a JSON object (no markdown, no explanation):\n"
        "```\n"
        "{\n"
        '  "description": "One paragraph describing the migration (source framework/version -> target framework/version, key changes)",\n'
        '  "sources": ["source-label-1", "source-label-2"],\n'
        '  "targets": ["target-label-1", "target-label-2"]\n'
        "}\n"
        "```\n"
        "For sources/targets, pick from the available lists above.\n"
        "- Targets matter most -- err on the side of being TOO BROAD. Include the "
        "general target AND specific versions (e.g., both 'quarkus' AND 'quarkus3', "
        "both 'eap8' AND 'eap', both 'jakarta-ee' AND 'jakarta-ee9').\n"
        "- Also include related targets that share relevant rules (e.g., for a quarkus "
        "migration, also include 'jakarta-ee', 'cloud-readiness', 'eap8').\n"
        "- For sources, be specific to what the code is migrating FROM.\n"
        "- If no lists are provided, leave sources/targets as empty arrays.\n"
    )

    response = await model.ainvoke(prompt)
    return _parse_migration_response(str(response.content))


def _parse_migration_response(content: str) -> MigrationInfo:
    """Parse the LLM response into a MigrationInfo."""
    cleaned = content.strip()
    # Strip markdown code fences if present
    if "```" in cleaned:
        start = cleaned.index("```")
        # Skip the language tag line
        start = cleaned.index("\n", start) + 1
        end = cleaned.index("```", start)
        cleaned = cleaned[start:end].strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to treating the whole response as the description
        return MigrationInfo(description=content.strip())

    sources = data.get("sources", [])
    targets = data.get("targets", [])

    # Build the label selector for kantra
    parts = []
    for t in targets:
        parts.append(f"konveyor.io/target={t}")
    selector = " || ".join(parts) if parts else ""

    return MigrationInfo(
        description=data.get("description", content.strip()),
        source_labels=sources,
        target_labels=targets,
        label_selector=selector,
    )


def get_available_labels(kantra_binary: str) -> tuple[list[str], list[str]]:
    """Get available source and target labels from kantra."""
    import subprocess

    targets: list[str] = []
    sources: list[str] = []

    try:
        result = subprocess.run(
            [kantra_binary, "analyze", "--list-targets", "--run-local=false"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line and not line.startswith(("time=", "available", "found")):
                targets.append(line)
    except Exception as e:
        print(f"Warning: could not list kantra targets: {e}", file=sys.stderr)

    try:
        result = subprocess.run(
            [kantra_binary, "analyze", "--list-sources", "--run-local=false"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line and not line.startswith(("time=", "available", "found")):
                sources.append(line)
    except Exception as e:
        print(f"Warning: could not list kantra sources: {e}", file=sys.stderr)

    return targets, sources


def _find_merge_base(repo: GitRepo, commit: str, base_branch: str) -> str | None:
    for branch in [base_branch, f"origin/{base_branch}"]:
        result = repo.merge_base(commit, branch)
        if result:
            return result
    return None


def _get_manifest_diff(repo: GitRepo, first_commit: str, last_commit: str) -> str:
    paths = []
    for pattern in MANIFEST_PATTERNS:
        paths.extend([f"**/{pattern}", pattern])
    try:
        return repo.diff_files(first_commit, last_commit, *paths)
    except Exception:
        return ""


def _get_diff_summary(repo: GitRepo, first_commit: str, last_commit: str) -> str:
    try:
        return repo.diff_stat(first_commit, last_commit)
    except Exception:
        return ""

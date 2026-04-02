"""Match resolved incidents to git diff hunks, capturing both direct fixes and context."""

from kai_commit_miner.attribution.models import AttributedFix, UnattributedChange
from kai_commit_miner.diff.models import IncidentDelta
from kai_commit_miner.git.diff_parser import DiffHunk, FileDiff
from kai_commit_miner.git.repo import GitRepo
from kai_mcp_solution_server.analyzer_types import remove_known_prefixes

_LINE_TOLERANCE = 5
_SNIPPET_CONTEXT = 10


def _hunk_overlaps_line(
    hunk: DiffHunk, line: int, tolerance: int = _LINE_TOLERANCE
) -> bool:
    hunk_start = hunk.old_start - tolerance
    hunk_end = hunk.old_start + hunk.old_count + tolerance
    return hunk_start <= line <= hunk_end


def _extract_snippet(content: str, line: int, context: int = _SNIPPET_CONTEXT) -> str:
    lines = content.split("\n")
    start = max(0, line - context)
    end = min(len(lines), line + context + 1)
    return "\n".join(lines[start:end])


def attribute_fixes(
    resolved_incidents: list[IncidentDelta],
    file_diffs: list[FileDiff],
    repo: GitRepo,
    commit_before: str,
    commit_after: str,
) -> tuple[list[AttributedFix], list[UnattributedChange]]:
    """Match resolved incidents to diff hunks, capturing context.

    For each resolved incident:
    - relevant_hunks: hunks that directly overlap the incident line
    - context_hunks: other hunks in the same file (knock-on changes like
      import additions, config changes, etc. that accompany the fix)

    Returns:
        - attributed_fixes: resolved incidents with their fix + context
        - unattributed_changes: hunks in files that have NO resolved incidents at all
    """
    # Index file diffs by normalized path
    diff_by_path: dict[str, FileDiff] = {}
    for fd in file_diffs:
        diff_by_path[remove_known_prefixes(fd.old_path)] = fd
        diff_by_path[remove_known_prefixes(fd.new_path)] = fd

    # Cache file contents to avoid repeated git show calls
    file_cache: dict[tuple[str, str], str] = {}

    def _get_file(commit: str, path: str) -> str:
        key = (commit, path)
        if key not in file_cache:
            try:
                file_cache[key] = repo.get_file_at_commit(commit, path)
            except Exception:
                file_cache[key] = ""
        return file_cache[key]

    # Track which files have at least one resolved incident
    files_with_incidents: set[str] = set()

    attributed: list[AttributedFix] = []

    for delta in resolved_incidents:
        if delta.incident_before is None:
            continue

        incident = delta.incident_before
        norm_path = remove_known_prefixes(incident.uri)
        file_diff = diff_by_path.get(norm_path)
        files_with_incidents.add(norm_path)

        before_content = _get_file(commit_before, norm_path)
        after_content = _get_file(commit_after, norm_path)

        if file_diff is None:
            attributed.append(
                AttributedFix(
                    incident=incident,
                    violation_key=delta.violation_key,
                    file_path=norm_path,
                    relevant_hunks=[],
                    context_hunks=[],
                    before_content=before_content,
                    after_content=after_content,
                    before_snippet=_extract_snippet(
                        before_content, incident.line_number
                    ),
                    indirect=True,
                )
            )
            continue

        # Split hunks into directly relevant vs context
        relevant: list[DiffHunk] = []
        context: list[DiffHunk] = []
        for hunk in file_diff.hunks:
            if _hunk_overlaps_line(hunk, incident.line_number):
                relevant.append(hunk)
            else:
                context.append(hunk)

        attributed.append(
            AttributedFix(
                incident=incident,
                violation_key=delta.violation_key,
                file_path=norm_path,
                relevant_hunks=relevant,
                context_hunks=context,
                before_content=before_content,
                after_content=after_content,
                before_snippet=_extract_snippet(before_content, incident.line_number),
                after_snippet=_extract_snippet(after_content, incident.line_number),
                indirect=len(relevant) == 0,
            )
        )

    # Unattributed = changes in files that have NO resolved incidents at all.
    # Changes in files WITH incidents are captured as context_hunks above.
    unattributed: list[UnattributedChange] = []
    for fd in file_diffs:
        norm = remove_known_prefixes(fd.new_path)
        if norm in files_with_incidents:
            continue
        unattributed.append(
            UnattributedChange(
                file_path=norm,
                hunks=fd.hunks,
            )
        )

    return attributed, unattributed

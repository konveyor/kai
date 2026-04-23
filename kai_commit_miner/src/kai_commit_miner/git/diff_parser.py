"""Parse unified diffs into structured data."""

import re
from dataclasses import dataclass, field


@dataclass
class DiffHunk:
    """A single hunk from a unified diff."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    content: str
    added_lines: list[int] = field(default_factory=list)
    removed_lines: list[int] = field(default_factory=list)


@dataclass
class FileDiff:
    """Diff information for a single file."""

    old_path: str
    new_path: str
    hunks: list[DiffHunk] = field(default_factory=list)
    is_new_file: bool = False
    is_deleted_file: bool = False
    is_renamed: bool = False


_DIFF_HEADER = re.compile(r"^diff --git a/(.*) b/(.*)$")
_HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def parse_unified_diff(diff_text: str) -> list[FileDiff]:
    """Parse a unified diff string into structured FileDiff objects."""
    files: list[FileDiff] = []
    current_file: FileDiff | None = None
    current_hunk: DiffHunk | None = None
    hunk_lines: list[str] = []

    def _finish_hunk() -> None:
        nonlocal current_hunk, hunk_lines
        if current_hunk is not None:
            current_hunk.content = "\n".join(hunk_lines)
            hunk_lines = []
            current_hunk = None

    for line in diff_text.split("\n"):
        header_match = _DIFF_HEADER.match(line)
        if header_match:
            _finish_hunk()
            current_file = FileDiff(
                old_path=header_match.group(1),
                new_path=header_match.group(2),
            )
            files.append(current_file)
            continue

        if current_file is None:
            continue

        if line.startswith("new file"):
            current_file.is_new_file = True
            continue
        if line.startswith("deleted file"):
            current_file.is_deleted_file = True
            continue
        if line.startswith("rename from") or line.startswith("rename to"):
            current_file.is_renamed = True
            continue

        hunk_match = _HUNK_HEADER.match(line)
        if hunk_match:
            _finish_hunk()
            current_hunk = DiffHunk(
                old_start=int(hunk_match.group(1)),
                old_count=int(hunk_match.group(2) or "1"),
                new_start=int(hunk_match.group(3)),
                new_count=int(hunk_match.group(4) or "1"),
                content="",
            )
            current_file.hunks.append(current_hunk)
            hunk_lines = [line]
            continue

        if current_hunk is not None:
            hunk_lines.append(line)
            if line.startswith("+") and not line.startswith("+++"):
                current_hunk.added_lines.append(
                    current_hunk.new_start + len(current_hunk.added_lines)
                )
            elif line.startswith("-") and not line.startswith("---"):
                current_hunk.removed_lines.append(
                    current_hunk.old_start + len(current_hunk.removed_lines)
                )

    _finish_hunk()
    return files

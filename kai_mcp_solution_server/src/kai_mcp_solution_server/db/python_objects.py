from difflib import unified_diff
from enum import StrEnum

from pydantic import BaseModel


class SolutionFile(BaseModel):
    uri: str
    content: str


def get_diff(before: list[SolutionFile], after: list[SolutionFile]) -> str:
    # use difflib to create a multiline diff

    # if the file names are the same, we assume they are the same file
    # if the file names are different, we create a similarity matrix. If two files have a similarity of 0.8 or more, we assume they are the same file
    # Any files not matched afterwards are considered new/deleted files

    # (before_uri, after_uri) -> (before_file, after_file)
    diff_dict: dict[tuple[str, str], tuple[SolutionFile, SolutionFile]] = {}

    before_files = {f.uri: f for f in before}
    after_files = {f.uri: f for f in after}

    matched_files = set(before_files.keys()) & set(after_files.keys())
    unmatched_before_files = set(before_files.keys()) - set(after_files.keys())
    unmatched_after_files = set(after_files.keys()) - set(before_files.keys())

    for uri in matched_files:
        before_file = before_files[uri]
        after_file = after_files[uri]
        diff_dict[(before_file.uri, after_file.uri)] = (before_file, after_file)

    # TODO: Implement similarity score
    for uri in unmatched_before_files:
        before_file = before_files[uri]
        diff_dict[(before_file.uri, "")] = (
            before_file,
            SolutionFile(uri="", content=""),
        )

    for uri in unmatched_after_files:
        after_file = after_files[uri]
        diff_dict[("", after_file.uri)] = (
            SolutionFile(uri="", content=""),
            after_file,
        )

    diffs = []
    for (before_uri, after_uri), (before_file, after_file) in diff_dict.items():
        if before_file.content == after_file.content:
            continue

        diff = unified_diff(
            before_file.content.splitlines(keepends=True),
            after_file.content.splitlines(keepends=True),
            fromfile=before_uri,
            tofile=after_uri,
        )

        diffs.append("".join(diff))

    return "\n".join(diffs) if diffs else ""


class SolutionChangeSet(BaseModel):
    before: list[SolutionFile]
    after: list[SolutionFile]


class SolutionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MODIFIED = "modified"
    PENDING = "pending"
    UNKNOWN = "unknown"


class ViolationID(BaseModel):
    ruleset_name: str
    violation_name: str


class Solution(BaseModel):
    # TODO: Turn this into a more general "Trajectory" thing?
    change_set: SolutionChangeSet

    reasoning: str | None = None

    solution_status: SolutionStatus

    hint_id: int | None = None

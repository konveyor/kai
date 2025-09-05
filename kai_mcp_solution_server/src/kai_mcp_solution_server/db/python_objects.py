from difflib import SequenceMatcher, unified_diff
from enum import StrEnum

from pydantic import BaseModel


class SolutionFile(BaseModel):
    uri: str
    content: str


def associate_files(
    before: list[SolutionFile], after: list[SolutionFile]
) -> dict[tuple[str, str], tuple[SolutionFile, SolutionFile]]:
    # Create a mapping of (before_uri, after_uri) -> (before_file, after_file)
    diff_dict: dict[tuple[str, str], tuple[SolutionFile, SolutionFile]] = {}

    before_files = {f.uri: f for f in before}
    after_files = {f.uri: f for f in after}

    matched_uris = set(before_files.keys()) & set(after_files.keys())

    for uri in matched_uris:
        before_file = before_files[uri]
        after_file = after_files[uri]
        diff_dict[(before_file.uri, after_file.uri)] = (before_file, after_file)

    unmatched_before_uris = set(before_files.keys()) - set(after_files.keys())
    unmatched_after_uris = set(after_files.keys()) - set(before_files.keys())
    similarity_matrix: dict[tuple[str, str], float] = {}

    for before_uri in unmatched_before_uris:
        for after_uri in unmatched_after_uris:
            similarity_matrix[(before_uri, after_uri)] = SequenceMatcher(
                None,
                before_files[before_uri].content.splitlines(),
                after_files[after_uri].content.splitlines(),
            ).quick_ratio()

    # TODO: This is O(n^3) in the worst case, which is not ideal.
    while len(unmatched_after_uris) != 0 and len(unmatched_before_uris) != 0:
        best_match = ("", "")
        best_similarity = 0.0

        for before_uri in unmatched_before_uris:
            for after_uri in unmatched_after_uris:
                similarity = similarity_matrix[(before_uri, after_uri)]
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = (before_uri, after_uri)

        if best_similarity < 0.8:
            break

        diff_dict[(best_match[0], best_match[1])] = (
            before_files[best_match[0]],
            after_files[best_match[1]],
        )

        unmatched_before_uris.remove(best_match[0])
        unmatched_after_uris.remove(best_match[1])

    # Add unmatched before files as deleted
    for before_uri in unmatched_before_uris:
        before_file = before_files[before_uri]
        diff_dict[(before_file.uri, "")] = (
            before_file,
            SolutionFile(uri="", content=""),
        )

    # Add unmatched after files as new
    for after_uri in unmatched_after_uris:
        after_file = after_files[after_uri]
        diff_dict[("", after_file.uri)] = (SolutionFile(uri="", content=""), after_file)

    return diff_dict


def get_diff(before: list[SolutionFile], after: list[SolutionFile]) -> str:
    diff_dict = associate_files(before, after)

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

    def __hash__(self) -> int:
        return hash((self.ruleset_name, self.violation_name))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ViolationID):
            raise NotImplementedError(f"Cannot compare ViolationID with {type(other)}")
        return (
            self.ruleset_name == other.ruleset_name
            and self.violation_name == other.violation_name
        )


class Solution(BaseModel):
    # TODO: Turn this into a more general "Trajectory" thing?
    change_set: SolutionChangeSet

    reasoning: str | None = None

    solution_status: SolutionStatus

    hint_id: int | None = None

import difflib
from dataclasses import dataclass
from typing import Sequence

from kai_mcp_solution_server.dao import SolutionFile


@dataclass
class UnifiedDiffParams:
    a: Sequence[str]
    b: Sequence[str]
    fromfile: str
    tofile: str


def create_diff(
    before: list[SolutionFile] | None = None,
    after: list[SolutionFile] | None = None,
    similarity_threshold: float = 0.9,
) -> str:
    """
    Create the diff using the SolutionFile objects.
    """

    if before is None:
        before = []
    if after is None:
        after = []

    before_dict: dict[str, Sequence[str]] = {
        file.uri: file.content.splitlines(keepends=True) for file in before
    }
    after_dict: dict[str, Sequence[str]] = {
        file.uri: file.content.splitlines(keepends=True) for file in after
    }

    if len(before_dict) != len(before):
        raise ValueError("Before list contains duplicate URIs.")
    if len(after_dict) != len(after):
        raise ValueError("After list contains duplicate URIs.")

    params: list[UnifiedDiffParams] = []

    same_uris = set(before_dict.keys()).intersection(after_dict.keys())
    for uri in same_uris:
        params.append(
            UnifiedDiffParams(
                a=before_dict.pop(uri),
                b=after_dict.pop(uri),
                fromfile=uri,
                tofile=uri,
            )
        )

    for before_uri, before_content in before_dict.items():
        best_ratio = 0.0
        best_after_uri = None
        best_after_content = None

        for after_uri, after_content in after_dict.items():
            ratio = difflib.SequenceMatcher(None, before_content, after_content).ratio()
            if ratio > best_ratio:
                best_ratio, best_after_uri, best_after_content = (
                    ratio,
                    after_uri,
                    after_content,
                )

        if (
            best_after_uri is not None
            and best_after_content is not None
            and best_ratio >= similarity_threshold
        ):
            params.append(
                UnifiedDiffParams(
                    a=before_content,
                    b=best_after_content,
                    fromfile=before_uri,
                    tofile=best_after_uri,
                )
            )
            del after_dict[best_after_uri]
        else:
            params.append(
                UnifiedDiffParams(
                    a=before_content,
                    b=[],
                    fromfile=before_uri,
                    tofile="",
                )
            )

    for after_uri, after_content in after_dict.items():
        params.append(
            UnifiedDiffParams(
                a=[],
                b=after_content,
                fromfile="",
                tofile=after_uri,
            )
        )

    diffs: list[str] = []
    for param in params:
        diff = difflib.unified_diff(
            param.a,
            param.b,
            fromfile=param.fromfile,
            tofile=param.tofile,
            lineterm="",
        )
        diffs.append("\n".join(diff))

    return "\n".join(diffs) if diffs else "No differences found."

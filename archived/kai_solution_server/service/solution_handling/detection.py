import json
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, cast
from urllib.parse import unquote, urlparse

import tree_sitter as ts
import tree_sitter_java
from git import Repo
from sequoia_diff import loaders
from sequoia_diff.matching import generate_mappings
from sequoia_diff.models import Node

from kai.analyzer_types import remove_known_prefixes
from kai.kai_config import SolutionDetectorKind
from kai_solution_server.service.incident_store.sql_types import SQLIncident


@dataclass
class SolutionDetectorContext:
    old_incidents: list[SQLIncident]
    new_incidents: list[SQLIncident]
    repo: Repo
    app_path: str
    old_commit: str
    new_commit: str


@dataclass
class SolutionDetectorResult:
    new: list[SQLIncident]
    unsolved: list[SQLIncident]
    solved: list[SQLIncident]


# Produce new, unsolved, and solved incidents. Statefully modify the unsolved
# incidents
#
# NOTE: Due to the way that SQLAlchemy works, the return value of unsolved
# incidents MUST be references to incidents in old_incidents, not new_incidents
# or any incidents created in the function. That way, we can call
# session.commit().
SolutionDetectionAlgorithm = Callable[[SolutionDetectorContext], SolutionDetectorResult]


def naive_hash(x: SQLIncident) -> int:
    """
    Returns a hash of the incident that is used for naive equality checking.
    """
    return hash(
        (
            x.violation_name,
            x.ruleset_name,
            x.application_name,
            x.incident_uri,
            x.incident_line,
            json.dumps(x.incident_variables, sort_keys=True),
        )
    )


def solution_detection_naive(ctx: SolutionDetectorContext) -> SolutionDetectorResult:
    """
    The naive solution detection algorithm is the simplest one. It just checks
    if a new incident is exactly the same as an old incident. If it is, then the
    incident is *unsolved*. Otherwise, it's new. Any old incidents that are not
    matched are considered solved.
    """

    result = SolutionDetectorResult([], [], [])

    updating_set: dict[int, SQLIncident] = {naive_hash(x): x for x in ctx.old_incidents}

    for incident in ctx.new_incidents:
        incident_hash = naive_hash(incident)

        if incident_hash in updating_set:
            result.unsolved.append(updating_set.pop(incident_hash))
        else:
            result.new.append(incident)

    result.solved = list(updating_set.values())

    return result


def line_match_hash(x: SQLIncident) -> int:
    """
    Returns a hash of the incident that is used for line matching.
    """
    return hash(
        (
            x.violation_name,
            x.ruleset_name,
            x.application_name,
            x.incident_uri,
            json.dumps(x.incident_variables, sort_keys=True),
        )
    )


def node_with_tightest_bounds(node: Node, start_byte: int, end_byte: int) -> Node:
    """
    Find the node with the tightest bounds that still contains the given byte
    range.
    """

    best = node
    while True:
        best.orig_node = cast(ts.Node, best.orig_node)
        another_iteration = False

        for child in best.children:
            ts_node = cast(ts.Node, child.orig_node)

            if (
                ts_node.start_byte > start_byte
                or ts_node.end_byte < end_byte
                or ts_node.start_byte < best.orig_node.start_byte
                or ts_node.end_byte > best.orig_node.end_byte
            ):
                continue
            best = child
            another_iteration = True

        if not another_iteration:
            break

    return best


def solution_detection_line_match(
    ctx: SolutionDetectorContext,
) -> SolutionDetectorResult:
    """
    The line match algorithm is trying to find incidents that still exist after
    a change by making the assumption that if the code exists in the changed
    file somewhere, then the incident is not solved. Note that this should be
    irrelevant of line number.

    1.  Filter out the exact matches.
    2.  Get a mapping between the two ASTs. (A each item in a mapping is a node
        in the source tree and the corresponding node in the destination tree.
        The algorithm for that is in the sequoia-diff library).
    3.  Get the smallest node that still contains the line under question.
    4.  Check if the mapping contains the node. If it does, the incident is
        unsolved. If not, it's solved
    """
    # TODO: Support multiple languages
    ts_language = ts.Language(tree_sitter_java.language())
    parser = ts.Parser(ts_language)

    result = SolutionDetectorResult([], [], [])
    # new_incidents = ctx.new_incidents.copy()
    new_incidents = [x for x in ctx.new_incidents]

    # Map the old incidents to their hashes for quick equality lookup.

    naive_old_incidents: dict[int, SQLIncident] = {
        naive_hash(x): x for x in ctx.old_incidents
    }

    # Filter the exact matches

    i = 0
    while i < len(new_incidents):
        incident = new_incidents[i]
        incident_hash = naive_hash(incident)

        if incident_hash in naive_old_incidents:
            result.unsolved.append(naive_old_incidents.pop(incident_hash))
            new_incidents.pop(i)
        else:
            i += 1

    # result.unsolved now contains all exact matches and naive_old_incidents
    # contains all non-exact matches.

    # Filter incidents whose line numbers match and whose line contents may have
    # just been moved.

    # NOTE: We use a multi-map here because there may be more than one match. We
    # may also need to switch the naive matching to use a multi-map in the
    # future.

    line_match_old_incidents: dict[int, set[SQLIncident]] = defaultdict(set)
    for x in naive_old_incidents.values():
        line_match_old_incidents[line_match_hash(x)].add(x)

    # Check each remaining incident in new_incidents

    for incident in new_incidents:
        incident_line_match_hash = line_match_hash(incident)

        # Check if the incident is in the remaining old incidents. If not, then
        # it's a new incident.

        if incident_line_match_hash not in line_match_old_incidents:
            result.new.append(incident)
            continue
        if len(line_match_old_incidents[incident_line_match_hash]) == 0:
            result.new.append(incident)
            del line_match_old_incidents[incident_line_match_hash]
            continue

        # Construct the trees for the old and new files

        # NOTE: Both file paths should be the same, but just in case we might
        # want to use the old file path.

        file_path = os.path.join(
            cast(str, ctx.repo.working_tree_dir),
            ctx.app_path,
            remove_known_prefixes(unquote(urlparse(incident.incident_uri).path)),
        )

        # TODO: See if we should cache these files/trees for performance

        old_file: str = ctx.repo.git.show(f"{ctx.old_commit}:{file_path}")
        new_file: str = ctx.repo.git.show(f"{ctx.new_commit}:{file_path}")

        old_tree = parser.parse(bytes(old_file, "utf-8"))
        new_tree = parser.parse(bytes(new_file, "utf-8"))

        old_node = loaders.from_tree_sitter_tree(old_tree, "java")
        new_node = loaders.from_tree_sitter_tree(new_tree, "java")

        # Get the byte offsets for the incident line

        old_line_start_byte = 0
        old_line_end_byte = 0
        for _ in range(incident.incident_line + 1):
            old_line_start_byte = old_file.find("\n", old_line_start_byte) + 1
            old_line_end_byte = old_file.find("\n", old_line_start_byte)

        # Get the node with the tightest bounds

        best = node_with_tightest_bounds(
            old_node, old_line_start_byte, old_line_end_byte
        )

        # Get the mappings from old_tree to new_tree

        mappings = generate_mappings(old_node, new_node)

        if best not in mappings.src_to_dst:
            result.new.append(incident)
            continue

        # NOTE: Right now we're just assuming that if the mapping algorithm
        # successfully finds a mapping, then the incident is unsolved. This is a
        # very naive approach and should be improved in the future. Some static
        # analysis may be required.

        old_incident = line_match_old_incidents[incident_line_match_hash].pop()
        old_incident.incident_line = incident.incident_line
        result.unsolved.append(old_incident)

    # These are the incidents that weren't matched to any incident in
    # new_incidents, meaning they were solved.

    for incident_set in line_match_old_incidents.values():
        if len(incident_set) > 0:
            result.solved.extend(incident_set)

    return result


def solution_detection_factory(
    kind: SolutionDetectorKind,
) -> SolutionDetectionAlgorithm:
    match kind:
        case SolutionDetectorKind.NAIVE:
            return solution_detection_naive
        case SolutionDetectorKind.LINE_MATCH:
            return solution_detection_line_match
        case _:
            raise ValueError(f"Unknown solution detection kind: {kind}")

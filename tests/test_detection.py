import os
import unittest
from unittest.mock import MagicMock, create_autospec

import tree_sitter as ts
import yaml
from sequoia_diff.models import Node

from kai.constants import PATH_TEST_DATA
from kai.service.incident_store.sql_types import SQLIncident
from kai.service.solution_handling.detection import (
    SolutionDetectorContext,
    node_with_tightest_bounds,
    solution_detection_line_match,
    solution_detection_naive,
)


class TestDetection(unittest.TestCase):
    def test_naive_simple(self):
        db_incidents = [
            # solved incidents
            SQLIncident(
                incident_id=0,
                violation_name="test_violation",
                ruleset_name="test_ruleset",
                application_name="test_application",
                incident_uri="test_uri",
                incident_message="test_message",
                incident_snip="test_snip",
                incident_line=0,
                incident_variables={},
                solution_id=None,
            ),
            # unsolved incidents
            SQLIncident(
                incident_id=1,
                violation_name="test_violation",
                ruleset_name="test_ruleset",
                application_name="test_application",
                incident_uri="test_uri",
                incident_message="test_message",
                incident_snip="test_snip",
                incident_line=1,
                incident_variables={},
                solution_id=None,
            ),
        ]

        report_incidents = [
            # unsolved incidents
            SQLIncident(
                incident_id=2,
                violation_name="test_violation",
                ruleset_name="test_ruleset",
                application_name="test_application",
                incident_uri="test_uri",
                incident_message="test_message",
                incident_snip="test_snip",
                incident_line=1,
                incident_variables={},
                solution_id=None,
            ),
            # new incidents
            SQLIncident(
                incident_id=3,
                violation_name="test_violation",
                ruleset_name="test_ruleset",
                application_name="test_application",
                incident_uri="test_uri",
                incident_message="test_message",
                incident_snip="test_snip",
                incident_line=2,
                incident_variables={},
                solution_id=None,
            ),
        ]

        result = solution_detection_naive(
            SolutionDetectorContext(db_incidents, report_incidents, MagicMock(), "", "")
        )

        self.assertTrue(len(result.new) == 1)
        self.assertTrue(len(result.unsolved) == 1)
        self.assertTrue(len(result.solved) == 1)

        self.assertTrue(db_incidents[0] == result.solved[0])
        self.assertTrue(db_incidents[1] == result.unsolved[0])
        self.assertTrue(report_incidents[0] != result.unsolved[0])
        self.assertTrue(report_incidents[1] == result.new[0])

    def test_line_match_simple(self):
        def local_read(*args) -> str:
            sections = args[0].split(":")
            stuff = sections[0]
            file_path = sections[1]
            dirname = os.path.dirname(os.path.realpath(file_path))
            basename = os.path.basename(file_path)

            file_name = os.path.join(dirname, f"{stuff}_{basename}")

            with open(file_name, "r") as file:
                return file.read()

        def local_yaml(file_path: str) -> dict | list:
            with open(
                os.path.join(
                    PATH_TEST_DATA,
                    "test_detection",
                    "test_line_match_simple",
                    file_path,
                ),
                "r",
            ) as file:
                return yaml.safe_load(file)

        mock_repo = MagicMock()
        mock_repo.git.show.side_effect = local_read
        mock_repo.working_tree_dir = os.path.join(
            PATH_TEST_DATA, "test_detection", "test_line_match_simple"
        )

        old_commit = "old"
        new_commit = "new"

        # No incidents, no changes

        result = solution_detection_line_match(
            SolutionDetectorContext([], [], mock_repo, old_commit, new_commit)
        )

        self.assertEqual(result.new, [], "Failed no incidents no changes")
        self.assertEqual(result.unsolved, [], "Failed no incidents no changes")
        self.assertEqual(result.solved, [], "Failed no incidents no changes")

        # Exact matches of incidents

        old_incidents = [SQLIncident(**x) for x in local_yaml("exact_matches.yaml")]
        new_incidents = [SQLIncident(**x) for x in local_yaml("exact_matches.yaml")]

        result = solution_detection_line_match(
            SolutionDetectorContext(
                old_incidents, new_incidents, mock_repo, old_commit, new_commit
            )
        )

        self.assertEqual(result.new, [], "Failed exact matches")
        self.assertEqual(result.unsolved, old_incidents, "Failed exact matches")
        self.assertEqual(result.solved, [], "Failed exact matches")

        # Exact matches of incidents, with some new incidents

        old_incidents = [
            SQLIncident(**x) for x in local_yaml("old_added_incidents.yaml")
        ]
        new_incidents = [
            SQLIncident(**x) for x in local_yaml("new_added_incidents.yaml")
        ]

        result = solution_detection_line_match(
            SolutionDetectorContext(
                old_incidents, new_incidents, mock_repo, old_commit, new_commit
            )
        )

        self.assertEqual(result.new, [new_incidents[1]], "Failed added incidents")
        self.assertEqual(result.unsolved, [old_incidents[0]], "Failed added incidents")
        self.assertEqual(result.solved, [], "Failed added incidents")

        # Adding whitespace

        old_incidents = [
            SQLIncident(**x) for x in local_yaml("old_added_whitespace.yaml")
        ]
        new_incidents = [
            SQLIncident(**x) for x in local_yaml("new_added_whitespace.yaml")
        ]

        result = solution_detection_line_match(
            SolutionDetectorContext(
                old_incidents, new_incidents, mock_repo, old_commit, new_commit
            )
        )

        self.assertEqual(result.new, [], "Failed added whitespace")
        self.assertEqual(result.unsolved, old_incidents, "Failed added whitespace")
        self.assertEqual(result.solved, [], "Failed added whitespace")


class TestNodeWithTightestBounds(unittest.TestCase):
    def setUp(self):
        # Mocking ts.Node
        self.mock_ts_node = create_autospec(ts.Node)

    def create_node(self, start_byte, end_byte, children=None) -> Node:
        orig_node = self.mock_ts_node()
        orig_node.start_byte = start_byte
        orig_node.end_byte = end_byte
        node = Node(
            type="mock_type", label="mock_label", orig_node=orig_node, children=children
        )
        return node

    def test_single_node_within_bounds(self):
        node = self.create_node(10, 20)
        result = node_with_tightest_bounds(node, 12, 18)
        self.assertEqual(result, node)

    def test_child_node_within_bounds(self):
        parent_node = self.create_node(10, 30)
        child_node = self.create_node(15, 25)
        parent_node.children_append(child_node)

        result = node_with_tightest_bounds(parent_node, 16, 24)
        self.assertEqual(result, child_node)

    def test_no_child_node_within_bounds(self):
        parent_node = self.create_node(5, 35)
        child_node = self.create_node(10, 30)
        parent_node.children_append(child_node)

        result = node_with_tightest_bounds(parent_node, 16, 24)
        self.assertEqual(result, child_node)

    def test_multiple_children_one_within_bounds(self):
        parent_node = self.create_node(10, 50)
        child_node1 = self.create_node(15, 35)
        child_node2 = self.create_node(20, 30)
        parent_node.children_append(child_node1)
        parent_node.children_append(child_node2)

        result = node_with_tightest_bounds(parent_node, 21, 29)
        self.assertEqual(result, child_node2)

    def test_multiple_nested_children(self):
        parent_node = self.create_node(10, 60)
        child_node1 = self.create_node(15, 55)
        child_node2 = self.create_node(20, 50)
        child_node3 = self.create_node(25, 45)
        child_node4 = self.create_node(30, 40)

        parent_node.children_append(child_node1)
        child_node1.children_append(child_node2)
        child_node2.children_append(child_node3)
        child_node3.children_append(child_node4)

        result = node_with_tightest_bounds(parent_node, 31, 39)
        self.assertEqual(result, child_node4)

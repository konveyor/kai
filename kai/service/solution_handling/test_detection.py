import unittest

from kai.service.incident_store.sql_types import SQLIncident
from kai.service.solution_handling.detection import (
    SolutionDetectorContext,
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
            SolutionDetectorContext(db_incidents, report_incidents, None, None, None)
        )

        self.assertTrue(len(result.new) == 1)
        self.assertTrue(len(result.unsolved) == 1)
        self.assertTrue(len(result.solved) == 1)

        self.assertTrue(db_incidents[0] == result.solved[0])
        self.assertTrue(db_incidents[1] == result.unsolved[0])
        self.assertTrue(report_incidents[0] != result.unsolved[0])
        self.assertTrue(report_incidents[1] == result.new[0])


def test_line_match():
    pass

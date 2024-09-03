import unittest
from unittest.mock import MagicMock, patch

from git import Repo

from kai.server.service.incident_store.sql_types import SQLIncident
from kai.server.service.llm_interfacing.model_provider import ModelProvider
from kai.server.service.solution_handling.production import (
    SolutionProducerLLMLazy,
    SolutionProducerTextOnly,
)
from kai.server.service.solution_handling.solution_types import Solution


def create_test_incident(**kwargs):
    return SQLIncident(
        incident_id=0,
        violation_name="test_violation",
        ruleset_name="test_ruleset",
        application_name="test_application",
        incident_uri="file:///test/file.py",
        incident_message="test_message",
        incident_snip="test_snip",
        incident_line=1,
        incident_variables={},
        solution_id=None,
        **kwargs,
    )


class TestSolutionProducerTextOnly(unittest.TestCase):
    def test_produce_one(self):
        # Arrange
        repo = MagicMock(spec=Repo)
        repo.git.show.side_effect = ["original code", "updated code"]
        repo.git.diff.return_value = "diff"

        incident = create_test_incident()

        solution_producer = SolutionProducerTextOnly()

        old_commit = "deadbeef"
        new_commit = "cafefeed"

        # Act
        solution = solution_producer.produce_one(incident, repo, old_commit, new_commit)

        # Assert
        self.assertEqual(solution.uri, incident.incident_uri)
        self.assertEqual(solution.file_diff, "diff")
        self.assertEqual(solution.original_code, "original code")
        self.assertEqual(solution.updated_code, "updated code")

    def test_post_process_one(self):
        # Arrange
        incident = create_test_incident()
        solution = Solution(
            uri=incident.incident_uri,
            file_diff="diff",
            original_code="original code",
            updated_code="updated code",
        )

        solution_producer = SolutionProducerTextOnly()

        # Act
        processed_solution = solution_producer.post_process_one(incident, solution)

        # Assert
        self.assertEqual(processed_solution, solution)


class TestSolutionProducerLLMLazy(unittest.TestCase):
    def test_produce_one(self):
        # Arrange
        repo = MagicMock(spec=Repo)
        repo.git.show.side_effect = ["original code", "updated code"]
        repo.git.diff.return_value = "diff"

        incident = create_test_incident()

        model_provider = MagicMock(spec=ModelProvider)
        solution_producer = SolutionProducerLLMLazy(model_provider)

        old_commit = "deadbeef"
        new_commit = "cafefeed"

        # Act
        solution = solution_producer.produce_one(incident, repo, old_commit, new_commit)

        # Assert
        self.assertEqual(solution.llm_summary_generated, False)

    @patch("kai.server.service.solution_handling.production.jinja2.Environment")
    def test_post_process_one(self, mock_jinja_env):
        # Arrange
        incident = create_test_incident()
        solution = Solution(
            uri=incident.incident_uri,
            file_diff="diff",
            original_code="original code",
            updated_code="updated code",
        )

        mock_template = mock_jinja_env.return_value.get_template.return_value
        mock_template.render.return_value = "rendered template"

        model_provider = MagicMock()
        model_provider.llm.invoke.return_value.content = "LLM summary"
        solution_producer = SolutionProducerLLMLazy(model_provider=model_provider)

        # Act
        processed_solution = solution_producer.post_process_one(incident, solution)

        # Assert
        self.assertEqual(processed_solution.llm_summary, "LLM summary")
        model_provider.llm.invoke.assert_called_with("rendered template")
        self.assertTrue(processed_solution.llm_summary_generated)

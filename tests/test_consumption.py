import unittest
from unittest.mock import MagicMock, patch

import jinja2

from kai.server.service.solution_handling.consumption import (
    solution_consumer_before_and_after,
    solution_consumer_diff_only,
    solution_consumer_factory,
    solution_consumer_llm_summary,
)
from kai.server.service.solution_handling.solution_types import Solution


class TestSolutionConsumers(unittest.TestCase):

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_diff_only(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        solution.file_diff = "some_diff"
        result = solution_consumer_diff_only(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "mocked render result")

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_before_and_after(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        solution.original_code = "original code"
        solution.updated_code = "updated code"
        result = solution_consumer_before_and_after(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "mocked render result")

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_llm_summary(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        solution.llm_summary = "summary"
        result = solution_consumer_llm_summary(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "mocked render result")

    def test_solution_consumer_factory_single_kind(self):
        consumer = solution_consumer_factory("diff_only")
        self.assertEqual(consumer, solution_consumer_diff_only)

        consumer = solution_consumer_factory("before_and_after")
        self.assertEqual(consumer, solution_consumer_before_and_after)

        consumer = solution_consumer_factory("llm_summary")
        self.assertEqual(consumer, solution_consumer_llm_summary)

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_factory_multiple_kinds(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        solution.file_diff = "some_diff"
        solution.llm_summary = "summary"
        consumer = solution_consumer_factory(["diff_only", "llm_summary"])
        result = consumer(solution)

        self.assertEqual(result, "mocked render result\nmocked render result")

    def test_solution_consumer_factory_invalid_kind(self):
        with self.assertRaises(ValueError) as context:
            solution_consumer_factory("invalid_kind")
        self.assertTrue("Unknown solution consumer kind" in str(context.exception))

    def test_solution_consumer_diff_only_empty_solution(self):
        empty_solution = MagicMock(spec=Solution)
        empty_solution.file_diff = ""
        result = solution_consumer_diff_only(empty_solution)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_solution_consumer_before_and_after_large_solution(self):
        large_solution = MagicMock(spec=Solution)
        large_solution.original_code = "x" * 10000
        large_solution.updated_code = "y" * 10000
        result = solution_consumer_before_and_after(large_solution)
        self.assertIn("x" * 10000, result)
        self.assertIn("y" * 10000, result)

    @patch(
        "jinja2.Environment.get_template",
        side_effect=jinja2.TemplateNotFound("template"),
    )
    def test_solution_consumer_template_not_found(self, mock_get_template):
        with self.assertRaises(jinja2.TemplateNotFound):
            solution_consumer_diff_only(MagicMock(spec=Solution))

    def test_solution_consumer_factory_mixed_kinds(self):
        kinds = ["diff_only", "invalid_kind"]

        solution_mock = MagicMock(spec=Solution)
        solution_mock.file_diff = "some_diff"

        with self.assertRaises(ValueError):
            solution_consumer_factory(kinds)(solution_mock)

    @patch("jinja2.Environment.get_template")
    def test_solution_consumer_resource_cleanup(self, mock_get_template):
        mock_template = MagicMock()
        mock_get_template.return_value = mock_template
        solution_consumer_diff_only(MagicMock(spec=Solution))
        mock_template.render.assert_called_once()

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_renders_empty_string(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = ""
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        result = solution_consumer_diff_only(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "")

    @patch("kai.server.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_partial_success(self, mock_create_jinja_env):
        mock_template_diff = MagicMock()
        mock_template_diff.render.return_value = "diff render result"

        mock_template_llm = MagicMock()
        mock_template_llm.render.side_effect = Exception("Rendering failed")

        mock_env = MagicMock()
        mock_env.get_template.side_effect = [mock_template_diff, mock_template_llm]
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        solution.file_diff = "some_diff"
        solution.llm_summary = "summary"

        consumer = solution_consumer_factory(["diff_only", "llm_summary"])

        with self.assertRaises(Exception) as context:
            consumer(solution)
        self.assertTrue("Rendering failed" in str(context.exception))

        mock_template_diff.render.assert_called_once_with(solution=solution)
        mock_template_llm.render.assert_called_once_with(solution=solution)


if __name__ == "__main__":
    unittest.main()

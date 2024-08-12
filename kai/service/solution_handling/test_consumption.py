import unittest
from unittest.mock import MagicMock, patch

from kai.service.solution_handling.consumption import (
    solution_consumer_before_and_after,
    solution_consumer_diff_only,
    solution_consumer_factory,
    solution_consumer_llm_summary,
)
from kai.service.solution_handling.solution_types import Solution


class TestSolutionConsumers(unittest.TestCase):

    @patch("kai.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_diff_only(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        result = solution_consumer_diff_only(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "mocked render result")

    @patch("kai.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_before_and_after(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        result = solution_consumer_before_and_after(solution)

        mock_template.render.assert_called_once_with(solution=solution)
        self.assertEqual(result, "mocked render result")

    @patch("kai.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_llm_summary(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
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

    @patch("kai.service.solution_handling.consumption.__create_jinja_env")
    def test_solution_consumer_factory_multiple_kinds(self, mock_create_jinja_env):
        mock_template = MagicMock()
        mock_template.render.return_value = "mocked render result"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_create_jinja_env.return_value = mock_env

        solution = MagicMock(spec=Solution)
        consumer = solution_consumer_factory(["diff_only", "llm_summary"])
        result = consumer(solution)

        self.assertEqual(result, "mocked render result\nmocked render result")

    def test_solution_consumer_factory_invalid_kind(self):
        with self.assertRaises(ValueError) as context:
            solution_consumer_factory("invalid_kind")
        self.assertTrue("Unknown solution consumer kind" in str(context.exception))


if __name__ == "__main__":
    unittest.main()

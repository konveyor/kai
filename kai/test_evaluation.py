import os
import unittest
from unittest.mock import MagicMock, patch

from kai.evaluation import (
    BenchmarkExample,
    evaluate,
    judge_result,
    levenshtein_distance,
    load_benchmark_examples,
    load_single_benchmark_example,
)
from kai.models.kai_config import KaiConfig, KaiConfigModels
from kai.models.report import Report
from kai.models.report_types import ExtendedIncident
from kai.service.incident_store.incident_store import Application


class TestEvaluation(unittest.TestCase):

    @patch("os.path.isdir", return_value=True)
    @patch("os.listdir")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="data")
    @patch("yaml.safe_load")
    @patch("kai.models.report.Report.load_report_from_file")
    @patch(
        "kai.evaluation.ExtendedIncident.model_validate",
        wraps=ExtendedIncident.model_construct,
    )
    @unittest.skip(
        reason="(pgaikwad): skipping this until we fully integrate the Kai Client"
    )
    def test_load_single_benchmark_example(
        self,
        mock_model_validate,
        mock_load_report,
        mock_yaml_load,
        mock_open,
        mock_listdir,
        mock_isdir,
    ):
        mock_isdir.return_value = True
        mock_listdir.return_value = [
            "original.java",
            "expected.java",
            "incidents.yaml",
            "report.yaml",
            "application.yaml",
        ]
        mock_yaml_load.return_value = {
            "application_name": "application_name",
            "repo_uri_origin": "https://www.example.com/",
            "repo_uri_local": "file:///path/to/repo",
            "current_branch": "main",
            "current_commit": "deadbeef",
            "generated_at": "2024-01-01T00:00:00Z",
        }
        mock_load_report.return_value = MagicMock(spec=Report)

        example = load_single_benchmark_example("/path/to/example")

        self.assertEqual(example.name, "example")
        self.assertEqual(example.original_file, "data")
        self.assertEqual(example.expected_file, "data")
        self.assertIsInstance(example.report, Report)
        self.assertIsInstance(example.application, Application)
        self.assertIsInstance(example.incidents, list)

    @patch("os.listdir", return_value=["example1", "example2"])
    @patch("kai.evaluation.load_single_benchmark_example")
    @unittest.skip(
        reason="(pgaikwad): skipping this until we fully integrate the Kai Client"
    )
    def test_load_benchmark_examples(
        self, mock_load_single_benchmark_example, mock_listdir
    ):
        mock_load_single_benchmark_example.side_effect = lambda x: BenchmarkExample(
            name=os.path.basename(x),
            original_file="original",
            expected_file="expected",
            incidents=[],
            report=MagicMock(spec=Report),
            application=MagicMock(spec=Application),
        )

        examples = load_benchmark_examples("/path/to/examples")

        self.assertIn("example1", examples)
        self.assertIn("example2", examples)
        self.assertEqual(examples["example1"].name, "example1")
        self.assertEqual(examples["example2"].name, "example2")

    @patch("kai.evaluation.ModelProvider")
    @patch("kai.evaluation.IncidentStore")
    @patch("kai.evaluation.get_prompt", return_value="prompt")
    @patch("kai.evaluation.guess_language", return_value="python")
    @patch(
        "kai.evaluation.parse_file_solution_content",
        return_value=MagicMock(updated_file="updated_file"),
    )
    @patch("kai.evaluation.judge_result", return_value=0.9)
    @unittest.skip(
        reason="(pgaikwad): skipping this until we fully integrate the Kai Client"
    )
    def test_evaluate(
        self,
        mock_model_provider,
        mock_incident_store,
        mock_get_prompt,
        mock_guess_language,
        mock_parse_file_solution_content,
        mock_judge_result,
    ):
        config = MagicMock(spec=KaiConfig)
        config.models = KaiConfigModels(
            provider="FakeListChatModel",
            args={},
        )
        configs = {"config_path": config}

        example = BenchmarkExample(
            name="example",
            original_file="original",
            expected_file="expected",
            incidents=[MagicMock()],
            report=MagicMock(),
            application=MagicMock(),
        )
        examples = {"example_path": example}

        results = evaluate(configs, examples)

        self.assertIn(("example_path", "config_path"), results)
        self.assertEqual(results[("example_path", "config_path")].similarity, 0.9)
        self.assertEqual(results[("example_path", "config_path")].prompt, "prompt")
        self.assertTrue(
            isinstance(results[("example_path", "config_path")].llm_result, str)
        )

    def test_levenshtein_distance(self):
        dist = levenshtein_distance("kitten", "sitting")
        self.assertEqual(dist, 3)

    def test_judge_result(self):
        dist = judge_result("kitten", "sitting")
        self.assertEqual(dist, 3)


if __name__ == "__main__":
    unittest.main()

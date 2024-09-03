import unittest
from unittest.mock import MagicMock, patch

from jinja2 import TemplateNotFound

from kai.models.report_types import ExtendedIncident, Incident
from kai.service.kai_application.util import (
    BatchMode,
    batch_incidents,
    get_prompt,
    playback_if_demo_mode,
)


class TestGetPrompt(unittest.TestCase):

    @patch("kai.service.kai_application.util.Environment.get_template")
    def test_get_prompt_with_valid_template(self, mock_get_template):
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered template"
        mock_get_template.return_value = mock_template

        result = get_prompt(template_name="test_template", pb_vars={"key": "value"})

        mock_get_template.assert_called_once_with("test_template.jinja")
        self.assertEqual(result, "rendered template")

    @patch(
        "kai.service.kai_application.util.Environment.get_template",
        side_effect=TemplateNotFound("test_template.jinja"),
    )
    @patch("kai.service.kai_application.util.KAI_LOG.warning")
    def test_get_prompt_fallback(self, mock_warning, mock_get_template):
        mock_fallback_template = MagicMock()
        mock_fallback_template.render.return_value = "fallback template"
        mock_env = MagicMock()
        mock_env.get_template.side_effect = [
            TemplateNotFound("test_template.jinja"),
            mock_fallback_template,
        ]

        with patch(
            "kai.service.kai_application.util.Environment", return_value=mock_env
        ):
            result = get_prompt(
                template_name="test_template", pb_vars={"key": "value"}, fallback=True
            )

            self.assertEqual(mock_warning.call_count, 0)
            self.assertEqual(result, "fallback template")

    def test_get_prompt_without_fallback(self):
        with self.assertRaises(TemplateNotFound):
            get_prompt(
                template_name="nonexistent_template",
                pb_vars={"key": "value"},
                fallback=False,
            )


class TestPlaybackIfDemoMode(unittest.TestCase):

    @patch("kai.service.kai_application.util.vcr.VCR.use_cassette")
    @patch("kai.service.kai_application.util.KAI_LOG.debug")
    def test_playback_if_demo_mode(self, mock_debug, mock_use_cassette):
        mock_use_cassette.return_value.__enter__.return_value = None

        with playback_if_demo_mode(
            demo_mode=True, model_id="model1", application_name="app1", filename="file1"
        ) as cassette:
            self.assertIsNone(cassette)

        mock_debug.assert_called_once()
        mock_use_cassette.assert_called_once_with("file1.yaml")

    @patch("kai.service.kai_application.util.vcr.VCR.use_cassette")
    def test_playback_if_not_demo_mode(self, mock_use_cassette):
        mock_use_cassette.return_value.__enter__.return_value = None

        with playback_if_demo_mode(
            demo_mode=False,
            model_id="model2",
            application_name="app2",
            filename="file2",
        ) as cassette:
            self.assertIsNone(cassette)

        mock_use_cassette.assert_called_once_with("file2.yaml")


class TestBatchIncidents(unittest.TestCase):

    def setUp(self):
        self.incident_dict = Incident(
            uri="uri",
            message="message",
        ).model_dump()

        self.incidents = [
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset1",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset1",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset1",
                violation_name="violation2"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset1",
                violation_name="violation2"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset1",
                violation_name="violation2"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
            ExtendedIncident(
                **self.incident_dict,
                ruleset_name="ruleset2",
                violation_name="violation1"
            ),
        ]

    def test_batch_incidents_none(self):
        result = batch_incidents(self.incidents, BatchMode.NONE)
        self.assertEqual(len(result), len(self.incidents))

    def test_batch_incidents_single_group(self):
        result = batch_incidents(self.incidents, BatchMode.SINGLE_GROUP)
        self.assertEqual(len(result), 1)

    def test_batch_incidents_ruleset(self):
        result = batch_incidents(self.incidents, BatchMode.RULESET)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0][1]), 5)
        self.assertEqual(len(result[1][1]), 6)

    def test_batch_incidents_violation(self):
        result = batch_incidents(self.incidents, BatchMode.VIOLATION)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0][1]), 2)
        self.assertEqual(len(result[1][1]), 3)
        self.assertEqual(len(result[2][1]), 6)


if __name__ == "__main__":
    unittest.main()

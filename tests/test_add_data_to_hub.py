import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

import yaml

from samples.add_data_to_hub import (
    add_analysis_report,
    add_applications,
    get_application_id,
    reformat_analysis_report,
)


class TestAddDataToHub(unittest.TestCase):

    @unittest.skip("TODO: Figure out best way to mock gitpython's Repos")
    @patch("samples.add_data_to_hub.requests.post")
    @patch("samples.add_data_to_hub.requests.get")
    def test_add_applications(self, mock_get, mock_post):
        mock_sample_apps = {"app1": "path/to/app1", "app2": "path/to/app2"}
        mock_repos = {
            "app1": ("https://repo.url/app1.git", "main", None),
            "app2": ("https://repo.url/app2.git", "main", None),
        }

        with patch(
            "samples.add_data_to_hub.config.sample_apps", mock_sample_apps
        ), patch("samples.add_data_to_hub.config.repos", mock_repos), patch(
            "samples.add_data_to_hub.add_analysis_report"
        ), patch(
            "os.path.exists", return_value=True
        ):

            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = {"id": 123}

            add_applications("http://mock_hub_url", False)
            self.assertEqual(mock_post.call_count, 2)
            self.assertEqual(mock_get.call_count, 0)

            mock_post.return_value.status_code = 409
            mock_post.return_value.json.return_value = {}

            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = [{"name": "app1", "id": 123}]
            add_applications("http://mock_hub_url", False)
            self.assertEqual(mock_post.call_count, 4)
            self.assertEqual(mock_get.call_count, 2)

    @patch("samples.add_data_to_hub.requests.get")
    def test_get_application_id(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"name": "app1", "id": 123}]

        app_id = get_application_id("http://mock_hub_url", "app1", False)
        self.assertEqual(app_id, 123)

    @patch("samples.add_data_to_hub.requests.post")
    def test_add_analysis_report(self, mock_post):
        mock_analysis_report = [
            {
                "name": "ruleset1",
                "violations": {
                    "rule1": {
                        "description": "violation description",
                        "category": "mandatory",
                        "effort": 1,
                        "incidents": [
                            {
                                "uri": "file1.java",
                                "lineNumber": 10,
                                "message": "violation message",
                                "codeSnip": "code snippet",
                                "variables": {"var1": "value1"},
                            }
                        ],
                    }
                },
            }
        ]

        mock_tempfile = MagicMock()
        mock_tempfile.name = "tempfile.yaml"

        with patch(
            "builtins.open", mock_open(read_data=yaml.dump(mock_analysis_report))
        ), patch("tempfile.NamedTemporaryFile", MagicMock(return_value=mock_tempfile)):

            add_analysis_report(
                "http://mock_hub_url", 1, 1, "path/to/analysis.yaml", False, False
            )

            self.assertEqual(mock_post.call_count, 1)

    def test_reformat_analysis_report(self):
        mock_analysis_report = [
            {
                "name": "ruleset1",
                "violations": {
                    "rule1": {
                        "description": "violation description",
                        "category": "mandatory",
                        "effort": 1,
                        "incidents": [
                            {
                                "uri": "file1.java",
                                "lineNumber": 10,
                                "message": "violation message",
                                "codeSnip": "code snippet",
                                "variables": {"var1": "value1"},
                            }
                        ],
                    }
                },
            }
        ]

        expected_result = {
            "commit": "deadbeef",
            "issues": [
                {
                    "id": 0,
                    "analysis": 1,
                    "ruleset": "ruleset1",
                    "rule": "rule1",
                    "name": "rule1",
                    "description": "violation description",
                    "category": "mandatory",
                    "effort": 1,
                    "incidents": [
                        {
                            "id": 0,
                            "issue": 0,
                            "file": "file1.java",
                            "uri": "file1.java",
                            "line": 10,
                            "message": "violation message",
                            "codeSnip": "code snippet",
                            "facts": {"var1": "value1"},
                            "createUser": None,
                            "updateUser": None,
                            "createTime": None,
                        }
                    ],
                    "links": [],
                    "labels": [],
                    "createUser": None,
                    "updateUser": None,
                    "createTime": None,
                }
            ],
            "dependencies": [],
        }

        result = reformat_analysis_report(mock_analysis_report, 0, 1, "deadbeef")

        # print result and expected_result to json file
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        with open("expected_result.json", "w") as f:
            json.dump(expected_result, f, indent=4)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

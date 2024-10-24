import json
import os
import re
import unittest
from typing import Any, Callable, Coroutine
from unittest.mock import Mock, patch

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application
from sqlalchemy import select
from sqlalchemy.orm import Session

from kai.constants import PATH_TEST_DATA
from kai.kai_config import (
    KaiConfig,
    KaiConfigIncidentStore,
    KaiConfigIncidentStoreSQLiteArgs,
    KaiConfigModels,
    SolutionDetectorKind,
    SolutionProducerKind,
)
from kai_solution_server.hub_importer import poll_api
from kai_solution_server.main import app as kai_app
from kai_solution_server.service.incident_store.incident_store import IncidentStore
from kai_solution_server.service.incident_store.sql_types import (
    SQLAcceptedSolution,
    SQLApplication,
    SQLIncident,
    SQLUnmodifiedReport,
)


class HubImporterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.incident_store = IncidentStore.incident_store_from_config(
            KaiConfig(
                models=KaiConfigModels(
                    provider="FakeListChatModel",
                    args={
                        "sleep": None,
                        "responses": [
                            "These are the steps:\n1. Frobinate the widget\n2. Profit\n",
                        ],
                    },
                ),
                incident_store=KaiConfigIncidentStore(
                    args=KaiConfigIncidentStoreSQLiteArgs(
                        provider="sqlite",
                        connection_string="sqlite:///:memory:",
                    ),
                    solution_producers=SolutionProducerKind.LLM_LAZY,
                    solution_detectors=SolutionDetectorKind.NAIVE,
                ),
            )
        )
        self.call_count = 0

        def mock_hub_api_get(url: str, *args, **kwargs):
            def response(res_gen: Callable = lambda: []) -> Mock:
                mock = Mock()
                mock.raise_for_status = Mock()
                mock.json = Mock(return_value=res_gen())
                return mock

            def load_json_file(path: str) -> dict[str, Any]:
                data = {}
                with open(
                    os.path.join(PATH_TEST_DATA, "test_hub_importer", path), "r"
                ) as f:
                    data = json.load(f)
                return data

            def grab_issues(analysis: dict[str, Any]) -> list[dict[str, Any]]:
                issues = []
                for idx, issue in enumerate(analysis.get("issues", [])):
                    issue["id"] = analysis.get("id") * 100 + idx
                    issue["analysis"] = analysis.get("id")
                    for idx, incident in enumerate(issue.get("incidents", [])):
                        incident["id"] = issue["id"] * 100 + idx
                    issues.append(issue)
                return issues

            match url:
                case _ if re.match(r".*analyses(\?filter=.*)?$", url):
                    if self.call_count > 2:
                        return response()
                    res = [
                        response(),
                        response(
                            lambda: [
                                load_json_file(
                                    os.path.join("ticket-monster", "unsolved.json")
                                )
                            ]
                        ),
                        response(
                            lambda: [
                                load_json_file(
                                    os.path.join("ticket-monster", "solved.json")
                                )
                            ]
                        ),
                    ][self.call_count]
                    self.call_count += 1
                    return res
                case _ if (m := re.match(r".*applications/(\d+)", url)):
                    app_id = m.group(1)
                    match app_id:
                        case "98":
                            return response(
                                lambda: load_json_file(
                                    os.path.join("ticket-monster", "app.json")
                                )
                            )
                        case _:
                            return response(lambda: {})
                case _ if (m := re.match(r".*analyses/(\d+)/issues.*", url)):
                    if int(kwargs.get("params", {}).get("offset", "0")) > 0:
                        return response()
                    analysis_id = m.group(1)
                    match analysis_id:
                        case "9801":
                            return response(
                                lambda: grab_issues(
                                    load_json_file(
                                        os.path.join("ticket-monster", "unsolved.json")
                                    )
                                )
                            )
                        case "9802":
                            return response(
                                lambda: grab_issues(
                                    load_json_file(
                                        os.path.join("ticket-monster", "solved.json")
                                    )
                                )
                            )
                        case _:
                            return response()
                case _:
                    return response(lambda: {})

        with patch("requests.get") as mock_get:
            mock_get.side_effect = mock_hub_api_get
            poll_api(
                "localhost:8080",
                incident_store=self.incident_store,
                interval=0,
                poll_condition=lambda: self.call_count < 3,
                post_process_limit=-1,
            )

    def test_hub_importer(self):
        with Session(self.incident_store.engine) as session:
            incidents = session.scalars(select(SQLIncident)).all()
            applications = session.scalars(select(SQLApplication)).all()
            reports = session.scalars(select(SQLUnmodifiedReport)).all()
            accepted_solutions = session.scalars(select(SQLAcceptedSolution)).all()

            self.assertEqual(len(incidents), 218)
            self.assertEqual(len(applications), 1)
            self.assertEqual(len(reports), 2)
            self.assertEqual(len(accepted_solutions), 82)

            for accepted_solution in accepted_solutions:
                self.assertTrue(accepted_solution.solution.llm_summary_generated)


class SolvedIncidentsServerTest(HubImporterTest, AioHTTPTestCase):
    @patch(
        "kai_solution_server.service.incident_store.incident_store.IncidentStore.incident_store_from_config"
    )
    @patch("kai_solution_server.main.get_config")
    @patch("kai.logging.logging.init_logging")
    async def get_application(
        self, mock_incident_store, mock_get_config, mock_init_logging
    ) -> Coroutine[Any, Any, Application]:
        mock_incident_store.return_value = Mock()
        mock_get_config.return_value = Mock()
        return kai_app()

    def setUp(self) -> None:
        super().setUp()

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.app["kai_incident_store"] = self.incident_store

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self.app.shutdown()

    async def test_get_solutions(self) -> None:
        response = await self.client.post(
            "/get_solutions",
            json={
                "ruleset_name": "eap8/eap7",
                "violation_name": "hibernate-00005",
                "incident_variables": {"kind": "Field"},
            },
        )
        content = await response.json()
        status_code = response.status
        self.assertEqual(status_code, 200)
        self.assertEqual(len(json.loads(content)["solutions"]), 43)

    @unittest.skip(reason="ran in parent fixture")
    def test_hub_importer(self):
        return super().test_hub_importer()

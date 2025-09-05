import asyncio
import datetime
import json
import os
import unittest
from uuid import uuid4

from mcp import ClientSession
from mcp.types import CallToolResult

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db.python_objects import ViolationID
from kai_mcp_solution_server.server import GetBestHintResult, SuccessRateMetric
from tests.mcp_client import MCPClientArgs
from tests.mcp_loader_script import create_client

# TODO: The tracebacks from these tests contain horrible impossibly-to-parse output.


class TestMultipleIntegration(unittest.IsolatedAsyncioTestCase):
    current_dir: str
    test_data_dir: str
    mcp_args: MCPClientArgs

    async def asyncSetUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = os.path.join(
            self.current_dir, "data/test_multiple_integration"
        )

        timestamp = datetime.datetime.now().isoformat()
        self.db_path = os.path.join(self.current_dir, f"test_{timestamp}.db")
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        os.environ["KAI_DB_DSN"] = f"sqlite+aiosqlite:///{self.db_path}"
        os.environ["KAI_DROP_ALL"] = "True"

        self.mcp_args = MCPClientArgs(
            transport="stdio",
            server_path=os.path.join(
                self.current_dir, "../src/kai_mcp_solution_server/"
            ),
        )

    async def asyncTearDown(self) -> None:
        pass

    async def test_tool_metadata(self) -> None:
        """
        Test that the MCP client tools have been unchanged and match what is expected.
        """
        async with create_client(self.mcp_args) as session:
            await session.initialize()

            tools_response = (await session.list_tools()).model_dump()
            self.assertFalse(
                tools_response.get("isError"),
                f"Error in tool response: {tools_response}",
            )

            tool_names = {tool["name"] for tool in tools_response["tools"]}
            expected_tool_names = {
                "create_incident",
                "create_multiple_incidents",
                "create_solution",
                "delete_solution",
                "get_best_hint",
                "get_success_rate",
                "accept_file",
                "reject_file",
            }
            self.assertSetEqual(
                tool_names,
                expected_tool_names,
                "Tool names do not match expected values",
            )

            tool_schemas = {
                tool["name"]: tool["inputSchema"] for tool in tools_response["tools"]
            }
            expected_tool_schemas = json.loads(
                open(self.test_data_dir + "/expected_tool_schemas.json").read()
            )
            self.assertDictEqual(
                tool_schemas,
                expected_tool_schemas,
                "Tool schemas do not match expected values",
            )

            failure = (await session.call_tool("failure_tool", {"a": "v"})).model_dump()
            self.assertTrue(
                failure.get("isError"), "Expected failure from failure_tool"
            )

    async def call_tool(
        self, session: ClientSession, tool_name: str, args: dict
    ) -> CallToolResult:
        """
        Helper method to call a tool and assert the response is not an error.
        """
        response = await session.call_tool(tool_name, args)
        self.assertFalse(
            response.isError,
            f"Tool {tool_name} failed with error: {response.model_dump()}",
        )
        return response

    async def test_solution_server_1(self) -> None:
        llm_params = {
            "model": "fake",
            "responses": [
                f"{uuid4()} You should add a smiley face to the file.",
            ],
        }
        os.environ["KAI_LLM_PARAMS"] = json.dumps(llm_params)

        async with create_client(self.mcp_args) as session:
            await session.initialize()

            RULESET_NAME_A = f"ruleset-{uuid4()}"
            VIOLATION_NAME_A = f"violation-{uuid4()}"
            CLIENT_ID_A = str(uuid4())

            print()
            print("--- Accept file as is ---")

            create_incident = await self.call_tool(
                session,
                "create_incident",
                {
                    "client_id": CLIENT_ID_A,
                    "extended_incident": ExtendedIncident(
                        uri="file://src/file_to_smile.txt",
                        message="this file needs to have a smiley face",
                        ruleset_name=RULESET_NAME_A,
                        violation_name=VIOLATION_NAME_A,
                    ).model_dump(),
                },
            )
            incident_id = int(create_incident.model_dump()["content"][0]["text"])
            print(f"Created incident with ID: {incident_id}")

            create_solution = await self.call_tool(
                session,
                "create_solution",
                {
                    "client_id": CLIENT_ID_A,
                    "incident_ids": [incident_id],
                    "before": [
                        {
                            "uri": "file://src/file_to_smile.txt",
                            "content": "I am very frowny :(",
                        }
                    ],
                    "after": [
                        {
                            "uri": "file://src/file_to_smile.txt",
                            "content": "I am very smiley :)",
                        }
                    ],
                    "reasoning": None,
                    "used_hint_ids": None,
                },
            )
            solution_id = int(create_solution.model_dump()["content"][0]["text"])
            print(f"Created solution with ID: {solution_id}")

            get_success_rate = await self.call_tool(
                session,
                "get_success_rate",
                {
                    "violation_ids": [
                        {
                            "ruleset_name": RULESET_NAME_A,
                            "violation_name": VIOLATION_NAME_A,
                        }
                    ]
                },
            )
            metric = SuccessRateMetric(**json.loads(get_success_rate.content[0].text))
            print(f"Success rate of {RULESET_NAME_A}/{VIOLATION_NAME_A}: {metric}")
            self.assertEqual(
                metric,
                SuccessRateMetric(
                    violation_id=ViolationID(
                        ruleset_name=RULESET_NAME_A,
                        violation_name=VIOLATION_NAME_A,
                    ),
                    counted_solutions=1,
                    pending_solutions=1,
                    pending_incidents=[incident_id],
                ),
            )

            await self.call_tool(
                session,
                "accept_file",
                {
                    "client_id": CLIENT_ID_A,
                    "solution_file": {
                        "uri": "file://src/file_to_smile.txt",
                        "content": "I am very smiley :)",
                    },
                },
            )

            get_success_rate = await self.call_tool(
                session,
                "get_success_rate",
                {
                    "violation_ids": [
                        {
                            "ruleset_name": RULESET_NAME_A,
                            "violation_name": VIOLATION_NAME_A,
                        }
                    ]
                },
            )
            metric = SuccessRateMetric(**json.loads(get_success_rate.content[0].text))
            print(
                f"Success rate of {RULESET_NAME_A}/{VIOLATION_NAME_A} after accepting file: {metric}"
            )
            self.assertEqual(
                metric,
                SuccessRateMetric(
                    violation_id=ViolationID(
                        ruleset_name=RULESET_NAME_A,
                        violation_name=VIOLATION_NAME_A,
                    ),
                    counted_solutions=1,
                    accepted_solutions=1,
                    accepted_incidents=[incident_id],
                ),
            )

            get_best_hint = await self.call_tool(
                session,
                "get_best_hint",
                {
                    "ruleset_name": RULESET_NAME_A,
                    "violation_name": VIOLATION_NAME_A,
                },
            )
            best_hint = GetBestHintResult(**json.loads(get_best_hint.content[0].text))
            print(f"Best hint for {RULESET_NAME_A}/{VIOLATION_NAME_A}: {best_hint}")
            self.assertEqual(best_hint.hint, llm_params["responses"][0])

            print()
            print("--- Modify file ---")

            RULESET_NAME_B = f"ruleset-{uuid4()}"
            VIOLATION_NAME_B = f"violation-{uuid4()}"
            CLIENT_ID_B = str(uuid4())

            create_incident = await self.call_tool(
                session,
                "create_incident",
                {
                    "client_id": CLIENT_ID_B,
                    "extended_incident": ExtendedIncident(
                        uri="file://src/file_to_smile.txt",
                        message="this file needs to have a smiley face",
                        ruleset_name=RULESET_NAME_B,
                        violation_name=VIOLATION_NAME_B,
                    ).model_dump(),
                },
            )
            incident_id = int(create_incident.model_dump()["content"][0]["text"])
            print(f"Created incident with ID: {incident_id}")

            create_solution = await self.call_tool(
                session,
                "create_solution",
                {
                    "client_id": CLIENT_ID_B,
                    "incident_ids": [incident_id],
                    "before": [
                        {
                            "uri": "file://src/file_to_smile.txt",
                            "content": "I am very frowny :(",
                        }
                    ],
                    "after": [
                        {
                            "uri": "file://src/file_to_smile.txt",
                            "content": "I am still very frowny :(",
                        }
                    ],
                    "reasoning": None,
                    "used_hint_ids": None,
                },
            )
            solution_id = int(create_solution.model_dump()["content"][0]["text"])
            print(f"Created solution with ID: {solution_id}")

            get_success_rate = await self.call_tool(
                session,
                "get_success_rate",
                {
                    "violation_ids": [
                        {
                            "ruleset_name": RULESET_NAME_B,
                            "violation_name": VIOLATION_NAME_B,
                        }
                    ]
                },
            )
            metric = SuccessRateMetric(**json.loads(get_success_rate.content[0].text))
            print(f"Success rate of {RULESET_NAME_A}/{VIOLATION_NAME_A}: {metric}")
            self.assertEqual(
                metric,
                SuccessRateMetric(
                    violation_id=ViolationID(
                        ruleset_name=RULESET_NAME_B,
                        violation_name=VIOLATION_NAME_B,
                    ),
                    counted_solutions=1,
                    pending_solutions=1,
                    pending_incidents=[incident_id],
                ),
            )

            await self.call_tool(
                session,
                "accept_file",
                {
                    "client_id": CLIENT_ID_B,
                    "solution_file": {
                        "uri": "file://src/file_to_smile.txt",
                        "content": "I am very smiley :)",
                    },
                },
            )

            get_success_rate = await self.call_tool(
                session,
                "get_success_rate",
                {
                    "violation_ids": [
                        {
                            "ruleset_name": RULESET_NAME_B,
                            "violation_name": VIOLATION_NAME_B,
                        }
                    ]
                },
            )
            metric = SuccessRateMetric(**json.loads(get_success_rate.content[0].text))
            print(
                f"Success rate of {RULESET_NAME_A}/{VIOLATION_NAME_A} after accepting file: {metric}"
            )
            self.assertEqual(
                metric,
                SuccessRateMetric(
                    violation_id=ViolationID(
                        ruleset_name=RULESET_NAME_B,
                        violation_name=VIOLATION_NAME_B,
                    ),
                    counted_solutions=1,
                    modified_solutions=1,
                    modified_incidents=[incident_id],
                ),
            )

            await asyncio.sleep(0.5)
            get_best_hint = await self.call_tool(
                session,
                "get_best_hint",
                {
                    "ruleset_name": RULESET_NAME_B,
                    "violation_name": VIOLATION_NAME_B,
                },
            )
            best_hint = GetBestHintResult(**json.loads(get_best_hint.content[0].text))
            print(f"Best hint for {RULESET_NAME_A}/{VIOLATION_NAME_A}: {best_hint}")
            self.assertEqual(best_hint.hint, llm_params["responses"][0])

import asyncio
import concurrent
import concurrent.futures
import datetime
import json
import os
import subprocess
import threading
import unittest
from uuid import uuid4

from fastmcp import Client
from mcp import ClientSession
from mcp.types import CallToolResult

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.server import GetBestHintResult, SuccessRateMetric
from tests.mcp_client import MCPClientArgs
from tests.mcp_loader_script import create_client
from tests.ssl_utils import apply_ssl_bypass

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
                    counted_solutions=1,
                    pending_solutions=1,
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
                    counted_solutions=1,
                    accepted_solutions=1,
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
                    counted_solutions=1,
                    pending_solutions=1,
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
                    counted_solutions=1,
                    modified_solutions=1,
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

    @unittest.skip("Skipping test_solution_server_2 for now")
    async def test_solution_server_2(self) -> None:
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
            print("--- Testing modify ---")

            create_incident_a = await self.call_tool(
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
            INCIDENT_ID_A = int(create_incident_a.model_dump()["content"][0]["text"])

            create_solution_for_incident_a = await self.call_tool(
                session,
                "create_solution",
                {
                    "client_id": CLIENT_ID_A,
                    "incident_ids": [INCIDENT_ID_A],
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
            SOLUTION_FOR_INCIDENT_A_ID = int(
                create_solution_for_incident_a.model_dump()["content"][0]["text"]
            )

    async def test_multiple_users(self) -> None:
        multiple_user_mcp_args = MCPClientArgs(
            transport="http",
            host="localhost",
            port=8087,
            insecure=True,
            server_path=self.mcp_args.server_path,
        )

        os.environ["KAI_LLM_PARAMS"] = json.dumps(
            {
                "model": "fake",
                "responses": [
                    f"You should add a smiley face to the file.",
                ],
            }
        )

        def stream_output(process: subprocess.Popen) -> None:
            try:
                assert process.stdout is not None
                for line in iter(process.stdout.readline, b""):
                    print(f"[Server] {line.decode().rstrip()}")
            except Exception as e:
                print(f"Error while streaming output: {e}")
            finally:
                process.stdout.close()

        def poll_process(process: subprocess.Popen) -> None:
            # Check if the process has exited early
            if process.poll() is not None:
                output = process.stdout.read() if process.stdout else b""
                raise RuntimeError(
                    f"HTTP server process exited prematurely. Output: {output.decode(errors='replace')}"
                )

        def run_async_in_thread(fn, *args, **kwargs):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(fn(*args, **kwargs))
                return result
            finally:
                loop.close()

        async def client_task(client_id: str) -> None:
            print(f"[Client {client_id}] starting")
            ssl_patch = apply_ssl_bypass()

            client = Client(
                transport="http://localhost:8087",
            )

            async with client:
                await client.session.initialize()
                print(f"[Client {client_id}] initialized")

                await client.session.list_tools()
                print(f"[Client {client_id}] listed tools")

            print(f"[Client {client_id}] finished")

        try:
            self.http_server_process = subprocess.Popen(
                [
                    "python",
                    "-m",
                    "kai_mcp_solution_server",
                    "--transport",
                    "streamable-http",
                    "--port",
                    "8087",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            stream_thread = threading.Thread(
                target=stream_output, args=(self.http_server_process,)
            )
            stream_thread.daemon = True
            stream_thread.start()

            await asyncio.sleep(1)  # give the server a second to start

            NUM_TASKS = 1
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Submit each task to the thread pool and store the Future objects.
                # The executor will call run_async_in_thread for each task ID.
                futures = {
                    executor.submit(run_async_in_thread, client_task, i): i
                    for i in range(1, NUM_TASKS + 1)
                }

                # Use as_completed() to process results as they become available.
                # This is non-blocking to the main thread while tasks are running.
                for future in concurrent.futures.as_completed(futures):
                    task_id = futures[future]
                    try:
                        result = future.result()
                        print(
                            f"[Main] received result for Task {task_id}: {result}",
                            flush=True,
                        )
                    except Exception as exc:
                        print(f"[Main] Task {task_id} generated an exception: {exc}")

            await asyncio.sleep(10)  # wait a moment for all output to be printed

        finally:
            self.http_server_process.terminate()
            self.http_server_process.wait()
            print("Server process terminated.")
            stream_thread.join()

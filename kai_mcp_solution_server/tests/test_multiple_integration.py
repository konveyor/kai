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
        # Note: We don't set KAI_DROP_ALL anymore - tables are created automatically

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
            int(create_solution_for_incident_a.model_dump()["content"][0]["text"])

    async def test_multiple_users(self) -> None:
        """
        Test multiple concurrent users accessing the MCP server.

        This test can be used for stress testing by setting NUM_CONCURRENT_CLIENTS
        environment variable to a high value (e.g., 100, 200).

        Two modes of operation:
        1. Self-contained mode (default): Starts its own server with SQLite
           NUM_CONCURRENT_CLIENTS=100 pytest tests/test_multiple_integration.py::TestMultipleIntegration::test_multiple_users

        2. External server mode: Connect to already-running server
           MCP_SERVER_URL="http://localhost:8000" NUM_CONCURRENT_CLIENTS=100 pytest tests/test_multiple_integration.py::TestMultipleIntegration::test_multiple_users
        """
        # Check if we should use an external server
        external_server_url = os.environ.get("MCP_SERVER_URL")

        if external_server_url:
            # External server mode - parse URL to get host and port
            from urllib.parse import urlparse

            parsed = urlparse(external_server_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 8000
            print(f"Using external MCP server at {host}:{port}")

            multiple_user_mcp_args = MCPClientArgs(
                transport="http",
                host=host,
                port=port,
                insecure=True,
                server_path=None,  # Not needed for external server
            )
            # Don't set KAI_LLM_PARAMS for external server - it should already be configured
            start_own_server = False
        else:
            # Self-contained mode - will start own server on port 8087
            print("Starting self-contained MCP server on port 8087")
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
                        "You should add a smiley face to the file.",
                    ],
                }
            )
            start_own_server = True

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
            apply_ssl_bypass()

            client = Client(
                transport=f"http://{multiple_user_mcp_args.host}:{multiple_user_mcp_args.port}",
            )

            try:
                async with client:
                    await client.session.initialize()
                    print(f"[Client {client_id}] initialized")

                    # List tools
                    tools = await client.session.list_tools()
                    print(f"[Client {client_id}] listed {len(tools.tools)} tools")

                    # Exercise the API with actual operations
                    client_uuid = str(uuid4())

                    # Create an incident
                    incident_result = await client.session.call_tool(
                        "create_incident",
                        {
                            "client_id": f"stress-test-{client_uuid}",
                            "extended_incident": {
                                "uri": f"file://test/file_{client_id}.java",
                                "message": f"Test issue for client {client_id}",
                                "ruleset_name": f"test-ruleset-{client_id % 10}",  # Share some rulesets
                                "violation_name": f"test-violation-{client_id % 5}",  # Share some violations
                                "violation_category": "potential",
                                "code_snip": "// test code",
                                "line_number": 42,
                                "variables": {},
                            },
                        },
                    )
                    incident_id = int(incident_result.content[0].text)
                    print(f"[Client {client_id}] created incident {incident_id}")
                    assert incident_id > 0, f"Invalid incident ID: {incident_id}"

                    # Create a solution
                    solution_result = await client.session.call_tool(
                        "create_solution",
                        {
                            "client_id": f"stress-test-{client_uuid}",
                            "incident_ids": [incident_id],
                            "before": [
                                {
                                    "uri": f"file://test/file_{client_id}.java",
                                    "content": "// original code",
                                }
                            ],
                            "after": [
                                {
                                    "uri": f"file://test/file_{client_id}.java",
                                    "content": "// fixed code",
                                }
                            ],
                            "reasoning": f"Fix applied by client {client_id}",
                            "used_hint_ids": None,
                        },
                    )
                    solution_id = int(solution_result.content[0].text)
                    print(f"[Client {client_id}] created solution {solution_id}")
                    assert solution_id > 0, f"Invalid solution ID: {solution_id}"

                    # Get success rate (before accepting)
                    success_rate_result = await client.session.call_tool(
                        "get_success_rate",
                        {
                            "violation_ids": [
                                {
                                    "ruleset_name": f"test-ruleset-{client_id % 10}",
                                    "violation_name": f"test-violation-{client_id % 5}",
                                }
                            ]
                        },
                    )
                    # Parse and verify success rate
                    success_rate_text = success_rate_result.content[0].text
                    import json

                    success_rate = json.loads(success_rate_text)
                    print(f"[Client {client_id}] got success rate: {success_rate}")

                    # Handle both single object and array response
                    if isinstance(success_rate, list):
                        # If it's a list, check the first element
                        assert len(success_rate) > 0, "Success rate list is empty"
                        rate = success_rate[0]
                    else:
                        rate = success_rate

                    # Store initial counts to compare deltas later
                    initial_counted = rate["counted_solutions"]
                    initial_accepted = rate["accepted_solutions"]
                    initial_pending = rate["pending_solutions"]

                    # In a shared database, we should see at least our solution
                    assert (
                        rate["counted_solutions"] >= 1
                    ), f"Expected at least 1 counted solution, got {rate['counted_solutions']}"
                    assert (
                        rate["pending_solutions"] >= 1
                    ), f"Expected at least 1 pending solution, got {rate['pending_solutions']}"

                    # Accept the file
                    await client.session.call_tool(
                        "accept_file",
                        {
                            "client_id": f"stress-test-{client_uuid}",
                            "solution_file": {
                                "uri": f"file://test/file_{client_id}.java",
                                "content": "// fixed code",
                            },
                        },
                    )
                    print(f"[Client {client_id}] accepted file")

                    # Wait a bit for the acceptance to be processed
                    await asyncio.sleep(0.5)

                    # Get success rate again (after accepting)
                    success_rate_result2 = await client.session.call_tool(
                        "get_success_rate",
                        {
                            "violation_ids": [
                                {
                                    "ruleset_name": f"test-ruleset-{client_id % 10}",
                                    "violation_name": f"test-violation-{client_id % 5}",
                                }
                            ]
                        },
                    )
                    success_rate_text2 = success_rate_result2.content[0].text
                    success_rate2 = json.loads(success_rate_text2)
                    print(
                        f"[Client {client_id}] got success rate after accept: {success_rate2}"
                    )

                    # Handle both single object and array response
                    if isinstance(success_rate2, list):
                        # If it's a list, check the first element
                        assert len(success_rate2) > 0, "Success rate list is empty"
                        rate2 = success_rate2[0]
                    else:
                        rate2 = success_rate2

                    # Check deltas after accepting the solution
                    # With multiple clients working on same violations, we need to be flexible
                    delta_accepted = rate2["accepted_solutions"] - initial_accepted
                    delta_pending = rate2["pending_solutions"] - initial_pending

                    # Since multiple clients may be working on the same violation types,
                    # we need to allow for some variance in the counts
                    assert (
                        delta_accepted >= 1
                    ), f"Expected accepted to increase by at least 1, but delta was {delta_accepted} (from {initial_accepted} to {rate2['accepted_solutions']})"
                    assert (
                        delta_pending <= 0
                    ), f"Expected pending to stay same or decrease, but delta was {delta_pending} (from {initial_pending} to {rate2['pending_solutions']})"

                    # The sum of accepted + pending changes should be close to 0
                    # (one solution moved from pending to accepted)
                    total_delta = delta_accepted + delta_pending
                    assert (
                        -2 <= total_delta <= 2
                    ), f"Expected net change close to 0, but was {total_delta} (accepted: +{delta_accepted}, pending: {delta_pending})"

                    # Total counted should remain the same (or increase if others added solutions)
                    assert (
                        rate2["counted_solutions"] >= initial_counted
                    ), f"Counted solutions should not decrease (was {initial_counted}, now {rate2['counted_solutions']})"

                    print(
                        f"[Client {client_id}] ✓ All operations completed successfully"
                    )
            except Exception as e:
                print(f"[Client {client_id}] ERROR: {e}")
                raise  # Re-raise to fail the test

        stream_thread = None
        try:
            if start_own_server:
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
            else:
                # External server should already be running
                self.http_server_process = None

            # Allow configuring number of concurrent clients via environment variable
            NUM_TASKS = int(os.environ.get("NUM_CONCURRENT_CLIENTS", "30"))
            print(f"Testing with {NUM_TASKS} concurrent clients")

            errors = []  # Track any errors that occur
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=NUM_TASKS
            ) as executor:
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
                        error_msg = f"Task {task_id} failed: {exc}"
                        print(f"[Main] {error_msg}")
                        errors.append(error_msg)

            await asyncio.sleep(10)  # wait a moment for all output to be printed

            # Fail the test if any errors occurred
            if errors:
                self.fail(f"\n{len(errors)} clients failed:\n" + "\n".join(errors))

            print(
                f"\n✓ All {NUM_TASKS} clients completed successfully with correct results!"
            )

            # Wait a bit for async hint generation to complete
            print("\nWaiting for hint generation to complete...")
            await asyncio.sleep(5)

            # Verify hints were generated by checking a few violations
            print("Verifying hints were generated...")
            async with create_client(multiple_user_mcp_args) as hint_session:
                await hint_session.initialize()

                # Check hints for a few different violation combinations
                violations_to_check = [
                    ("test-ruleset-0", "test-violation-0"),
                    ("test-ruleset-1", "test-violation-1"),
                    ("test-ruleset-2", "test-violation-2"),
                ]

                hints_found = 0
                for ruleset, violation in violations_to_check:
                    try:
                        hint_result = await hint_session.call_tool(
                            "get_best_hint",
                            {
                                "ruleset_name": ruleset,
                                "violation_name": violation,
                            },
                        )
                        if hint_result and not hint_result.isError:
                            hints_found += 1
                            print(f"  ✓ Found hint for {ruleset}/{violation}")
                        else:
                            print(f"  ✗ No hint for {ruleset}/{violation}")
                    except Exception as e:
                        print(f"  ✗ Error checking hint for {ruleset}/{violation}: {e}")

                if hints_found == 0:
                    self.fail(
                        "No hints were generated! Hint generation may not be working correctly."
                    )
                else:
                    print(
                        f"\n✓ Found {hints_found}/{len(violations_to_check)} hints generated"
                    )

        finally:
            if self.http_server_process:
                self.http_server_process.terminate()
                self.http_server_process.wait()
                print("Server process terminated.")
                if stream_thread:
                    stream_thread.join()

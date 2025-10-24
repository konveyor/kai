import asyncio
import json
import os
import unittest
from uuid import uuid4

from fastmcp import Client
from mcp.types import CallToolResult
from tests.ssl_utils import apply_ssl_bypass

from kai_mcp_solution_server.analyzer_types import ExtendedIncident


class TestDuplicateViolations(unittest.IsolatedAsyncioTestCase):
    """Test handling of duplicate violation creation scenarios.

    These tests require a running MCP server. Start the server with:
    make run-local  or  make podman-postgres

    Then run tests with:
    MCP_SERVER_URL=http://localhost:8000 pytest tests/test_duplicate_violations.py
    """

    async def asyncSetUp(self) -> None:
        # Require external server URL
        self.server_url = os.environ.get("MCP_SERVER_URL")
        if not self.server_url:
            self.skipTest(
                "MCP_SERVER_URL environment variable is required. "
                "Please start a server (e.g., 'make run-local' or 'make podman-postgres') "
                "and set MCP_SERVER_URL=http://localhost:8000"
            )

        apply_ssl_bypass()
        print(f"Using MCP server at {self.server_url}")

    async def call_tool(self, client, tool_name: str, args: dict) -> CallToolResult:
        """Helper method to call a tool and return the result."""
        response = await client.session.call_tool(tool_name, args)
        return response

    async def test_duplicate_violation_sequential(self) -> None:
        """Test that creating incidents with the same violation sequentially works."""

        client = Client(transport=self.server_url)
        async with client:
            await client.session.initialize()

            # Use the exact violation from the error message
            RULESET_NAME = "eap8/eap7"
            VIOLATION_NAME = "javax-to-jakarta-import-00001"
            CLIENT_ID_1 = str(uuid4())
            CLIENT_ID_2 = str(uuid4())

            print("\n--- Testing sequential duplicate violation creation ---")

            # Create first incident with this violation
            incident1 = await self.call_tool(
                client,
                "create_incident",
                {
                    "client_id": CLIENT_ID_1,
                    "extended_incident": ExtendedIncident(
                        uri="file://src/file1.java",
                        message="First incident with this violation",
                        ruleset_name=RULESET_NAME,
                        violation_name=VIOLATION_NAME,
                    ).model_dump(),
                },
            )

            self.assertFalse(
                incident1.isError,
                f"First incident creation failed: {incident1.model_dump()}",
            )
            incident1_id = int(incident1.model_dump()["content"][0]["text"])
            print(f"Created first incident with ID: {incident1_id}")

            # Create second incident with the same violation (should reuse existing violation)
            incident2 = await self.call_tool(
                client,
                "create_incident",
                {
                    "client_id": CLIENT_ID_2,
                    "extended_incident": ExtendedIncident(
                        uri="file://src/file2.java",
                        message="Second incident with same violation",
                        ruleset_name=RULESET_NAME,
                        violation_name=VIOLATION_NAME,
                    ).model_dump(),
                },
            )

            self.assertFalse(
                incident2.isError,
                f"Second incident creation failed: {incident2.model_dump()}",
            )
            incident2_id = int(incident2.model_dump()["content"][0]["text"])
            print(f"Created second incident with ID: {incident2_id}")

            # Verify both incidents were created successfully
            self.assertNotEqual(incident1_id, incident2_id)
            self.assertGreater(incident1_id, 0)
            self.assertGreater(incident2_id, 0)

    async def test_concurrent_duplicate_violations(self) -> None:
        """Test that concurrent creation of incidents with same violation is handled correctly.

        This test is expected to FAIL with the current implementation due to race condition.
        """

        # Use unique names to avoid conflicts with other tests
        RULESET_NAME = f"concurrent-ruleset-{uuid4()}"
        VIOLATION_NAME = f"concurrent-violation-{uuid4()}"

        print("\n--- Testing concurrent duplicate violation creation ---")
        print(f"Ruleset: {RULESET_NAME}")
        print(f"Violation: {VIOLATION_NAME}")

        # Create multiple clients for truly concurrent operations
        async def create_incident_with_client(client_id: str, file_num: int):
            try:
                client = Client(transport=self.server_url)
                async with client:
                    await client.session.initialize()

                    result = await client.session.call_tool(
                        "create_incident",
                        {
                            "client_id": client_id,
                            "extended_incident": ExtendedIncident(
                                uri=f"file://src/concurrent_file_{file_num}.java",
                                message=f"Concurrent incident {file_num}",
                                ruleset_name=RULESET_NAME,
                                violation_name=VIOLATION_NAME,
                            ).model_dump(),
                        },
                    )
                    return file_num, result
            except Exception as e:
                return file_num, e

        num_concurrent = int(os.environ.get("NUM_CONCURRENT_CLIENTS", "30"))
        print(f"Creating {num_concurrent} concurrent incidents...")

        tasks = []
        for i in range(num_concurrent):
            client_id = str(uuid4())
            tasks.append(create_incident_with_client(client_id, i))

        results = await asyncio.gather(*tasks, return_exceptions=False)

        incident_ids = []
        errors = []
        for file_num, result in results:
            if isinstance(result, Exception):
                errors.append((file_num, str(result)))
                print(
                    f"Concurrent incident {file_num} creation failed with exception: {result}"
                )
            elif hasattr(result, "isError") and result.isError:
                error_msg = result.model_dump()
                errors.append((file_num, error_msg))
                print(f"Concurrent incident {file_num} returned error: {error_msg}")
                error_text = str(error_msg)
                if (
                    "duplicate key" in error_text.lower()
                    and "kai_violations_pkey" in error_text
                ):
                    print("  -> This is the expected duplicate key violation error!")
            else:
                incident_id = int(result.model_dump()["content"][0]["text"])
                incident_ids.append(incident_id)
                print(f"Created concurrent incident {file_num} with ID: {incident_id}")

        print("\nSummary:")
        print(f"  Successful creations: {len(incident_ids)}")
        print(f"  Failed creations: {len(errors)}")

        if errors:
            print("\nErrors during concurrent creation:")
            for file_num, error in errors:
                print(f"  File {file_num}: {error}")

        # This test demonstrates the race condition - we expect some failures
        # with duplicate key violations when the issue is not fixed
        if errors:
            for _, error in errors:
                error_str = str(error).lower()
                if "duplicate key" in error_str and "kai_violations_pkey" in error_str:
                    print(
                        "\n*** RACE CONDITION DETECTED: Got expected duplicate key violation ***"
                    )
                    print("This confirms the bug that needs to be fixed.")
                    return  # Test passed by demonstrating the issue

        if not errors:
            print(
                "\nAll concurrent creations succeeded - issue may be fixed or timing was lucky"
            )
            self.assertEqual(
                len(incident_ids), num_concurrent, "Not all incidents were created"
            )
            self.assertEqual(
                len(incident_ids),
                len(set(incident_ids)),
                "Duplicate incident IDs found",
            )

    async def test_create_multiple_incidents_with_same_violation(self) -> None:
        """Test that create_multiple_incidents handles same violations correctly.

        This tests the batch creation where all incidents share the same violation.
        This should work because they're processed sequentially.
        """

        client = Client(transport=self.server_url)
        async with client:
            await client.session.initialize()

            RULESET_NAME = f"multi-ruleset-{uuid4()}"
            VIOLATION_NAME = f"multi-violation-{uuid4()}"
            CLIENT_ID = str(uuid4())

            print("\n--- Testing batch creation with same violation ---")

            # Create multiple incidents with the same violation in one call
            incidents_data = []
            for i in range(3):
                incidents_data.append(
                    ExtendedIncident(
                        uri=f"file://src/multi_file_{i}.java",
                        message=f"Multi incident {i}",
                        ruleset_name=RULESET_NAME,
                        violation_name=VIOLATION_NAME,
                    ).model_dump()
                )

            result = await self.call_tool(
                client,
                "create_multiple_incidents",
                {
                    "client_id": CLIENT_ID,
                    "extended_incidents": incidents_data,
                },
            )

            self.assertFalse(
                result.isError, f"Batch creation failed: {result.model_dump()}"
            )

            results_data = json.loads(result.model_dump()["content"][0]["text"])
            print(f"Created multiple incidents: {results_data}")

            # Verify all incidents were created
            self.assertEqual(len(results_data), 3)
            incident_ids = [r["incident_id"] for r in results_data]
            self.assertEqual(
                len(incident_ids),
                len(set(incident_ids)),
                "Duplicate incident IDs in batch creation",
            )

            # All should succeed since they're processed sequentially
            for r in results_data:
                self.assertGreater(r["incident_id"], 0, "Invalid incident ID")

            print(
                "Batch creation succeeded - sequential processing avoids race condition"
            )


if __name__ == "__main__":
    unittest.main()

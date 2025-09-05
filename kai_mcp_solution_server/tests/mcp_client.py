#!/usr/bin/env python3
"""
MCP Solution Server Test Client

This script tests the functionality of the MCP Solution Server by establishing
a proper Model Context Protocol connection and testing the available tools and resources.
"""

import argparse
import asyncio
import logging
import os
import sys
import uuid
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from pydantic import BaseModel

try:
    from ssl_utils import apply_ssl_bypass
except ImportError:
    from .ssl_utils import apply_ssl_bypass

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db.python_objects import SolutionFile, ViolationID
from kai_mcp_solution_server.server import SuccessRateMetric

# Configure logger
logger = logging.getLogger("kai-mcp-client")

# Configure console handler with a specific format
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Default level is INFO, verbose will set to DEBUG
logger.setLevel(logging.INFO)


async def _run_create_incident(client: Client, client_id: str) -> int:
    print("\n--- Testing create_incident ---")

    request = {
        "client_id": client_id,
        "extended_incident": ExtendedIncident(
            uri="file://ExampleService.java",
            message="Example incident for testing",
            line_number=1,
            variables={},
            ruleset_name="test-ruleset",
            violation_name="test-violation",
        ).model_dump(),
    }

    logger.debug(f"Preparing create_incident request: {request}")

    try:
        result = await client.call_tool("create_incident", request)

        # fastmcp returns list of TextContent objects
        incident_id = int(result[0].text) if result else None

        if incident_id is None:
            raise ValueError("Incident ID is None, check server response")

        print(f"o Incident created with ID: {incident_id}")

        return incident_id
    except Exception as e:
        logger.error("Error creating incident: %s", str(e), exc_info=True)
        print(f"x Error creating incident: {e}")
        raise e


async def _run_create_solution(
    client: Client, client_id: str, incident_ids: list[int]
) -> int:
    """Test the create_solution tool by creating a new solution."""
    print("\n--- Testing create_solution ---")

    before_code = """
// Original Java EE code
@Stateless
public class ExampleService {
    @PersistenceContext
    private EntityManager em;

    public List<Entity> findAll() {
        return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
    }
}
"""

    after_code = """
// Migrated Quarkus code
@ApplicationScoped
public class ExampleService {
    @Inject
    EntityManager em;

    public List<Entity> findAll() {
        return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
    }
}
"""

    diff = """
-// Original Java EE code
-@Stateless
+// Migrated Quarkus code
+@ApplicationScoped
 public class ExampleService {
-    @PersistenceContext
+    @Inject
     private EntityManager em;

     public List<Entity> findAll() {
         return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
     }
 }
"""
    logger.debug("Before code prepared (length: %d)", len(before_code))
    logger.debug("After code prepared (length: %d)", len(after_code))
    logger.debug("Diff prepared (length: %d)", len(diff))

    request = {
        "client_id": client_id,
        "incident_ids": incident_ids,
        "before": [
            SolutionFile(
                uri="file://ExampleService.java",
                content=before_code,
            ).model_dump()
        ],
        "after": [
            SolutionFile(
                uri="file://ExampleService.java",
                content=after_code,
            ).model_dump(),
        ],
    }

    try:
        logger.debug("Calling create_solution tool")
        result = await client.call_tool("create_solution", request)

        # fastmcp returns list of TextContent objects
        solution_id = int(result[0].text) if result else None

        if solution_id is None:
            raise ValueError("Solution ID is None, check server response")

        print(f"o Solution created with ID: {solution_id}")
        return solution_id
    except Exception as e:
        logger.error("Error creating solution: %s", str(e), exc_info=True)
        print(f"x Error creating solution: {e}")
        raise e


async def _run_accept_file(
    client: Client, client_id: str, solution_file: SolutionFile
) -> None:
    print("\n--- Testing accept_file ---")

    request = {
        "client_id": client_id,
        "solution_file": solution_file.model_dump(),
    }

    try:
        logger.debug("Calling accept_file tool with request: %s", request)
        result = await client.call_tool("accept_file", request)
        print("o accept_file tool call completed")
        logger.debug("accept_file tool call completed, result: %s", result)

    except Exception as e:
        logger.error("Error accepting file: %s", str(e), exc_info=True)
        print(f"x Error accepting file: {e}")
        raise e


async def _run_get_best_hint(client: Client) -> str | None:
    print("\n--- Testing get_best_hint ---")

    request = {
        "ruleset_name": "test-ruleset",
        "violation_name": "test-violation",
    }

    try:
        logger.debug("Preparing get_best_hint request: %s", request)
        result = await client.call_tool("get_best_hint", request)

        print("get_best_hint tool call completed, result: %s", result)

        # if not result:
        #     raise ValueError("! No related solutions found")

        return result

    except Exception as e:
        logger.error("Error finding related solutions: %s", str(e), exc_info=True)
        print(f"x Error finding related solutions: {e}")
        raise e


async def _run_get_success_rate(
    client: Client,
) -> list[SuccessRateMetric] | None:
    print("\n--- Testing get_success_rate ---")

    request = {
        "violation_ids": [
            ViolationID(
                violation_name="test-violation",
                ruleset_name="test-ruleset",
            ).model_dump(),
        ]
    }

    try:
        logger.debug("Preparing get_success_rate request: %s", request)
        result = await client.call_tool("get_success_rate", request)

        print("get_success_rate resource call completed, result: %s", result)

        if not result:
            print("! No success rate data found")
            return None

        # Convert to list of SuccessRateMetric objects
        return result
        # success_rates = [SuccessRateMetric(**item) for item in result]
        # print(f"o Success rates retrieved: {len(success_rates)} metrics")
        # return success_rates

    except Exception as e:
        logger.error("Error retrieving success rate: %s", str(e), exc_info=True)
        print(f"x Error retrieving success rate: {e}")
        raise e


class MCPClientArgs(BaseModel):
    host: str = "localhost"
    port: int = 8000
    transport: str = "stdio"  # Use stdio transport to test without network
    server_path: Path | None = None  # Optional for external server mode
    mount_path: str = "/"
    full_output: bool = False
    verbose: bool = False
    insecure: bool = False
    bearer_token: str | None = None


async def run_tests(args: MCPClientArgs) -> bool:
    """Run all the tests with the appropriate transport.
    Returns True if all tests completed successfully, False otherwise.
    """
    print("MCP Solution Server Test Client")
    print("==============================")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Transport: {args.transport}")

    if args.insecure and args.transport == "http":
        print("SSL verification: Disabled (insecure mode)")

    logger.debug("Starting test run with arguments: %s", vars(args))

    ssl_patch = None

    try:
        # Build client kwargs based on transport type
        if args.transport == "http":
            # Setup HTTP transport
            transport = ""
            if not args.host.startswith("http"):
                transport = "http://"
            host = args.host
            if host.endswith(args.mount_path):
                host = host[: -len(args.mount_path)]
            server_url = f"{transport}{host}:{args.port}{args.mount_path}"
            print(f"Connecting to server at {server_url}...")
            logger.debug("Initializing fastmcp Client with URL: %s", server_url)

            if args.insecure:
                logger.debug(
                    "Applying SSL monkey patch to bypass certificate verification"
                )
                ssl_patch = apply_ssl_bypass()
                print("⚠️ Warning: SSL certificate verification is disabled")

            # Setup client kwargs with transport and optional auth
            client_kwargs = {"transport": server_url}

            if args.bearer_token:
                client_kwargs["auth"] = args.bearer_token
                logger.debug("Added bearer token authentication")
                print("🔐 Bearer token authentication enabled")

        else:  # stdio transport
            print(f"Using server path: {args.server_path}")
            logger.debug(
                f"Initializing STDIO transport with server path: {args.server_path}"
            )

            # For stdio, use PythonStdioTransport with explicit environment variables
            server_path = Path(args.server_path)
            if (server_path / "__main__.py").exists():
                script_path = str(server_path / "__main__.py")
                working_dir = str(server_path.parent)
            else:
                # Fallback for when server_path is the project root
                script_path = str(
                    server_path / "src" / "kai_mcp_solution_server" / "__main__.py"
                )
                working_dir = str(server_path)

            # Create transport with explicit environment variables
            transport = PythonStdioTransport(
                script_path=script_path,
                args=["--transport", "stdio"],
                env=dict(os.environ),  # Explicitly pass all environment variables
                cwd=working_dir,
            )

            client_kwargs = {"transport": transport}

        logger.debug(f"Client kwargs: {client_kwargs}")

        try:
            # Create fastmcp client with the appropriate kwargs
            client = Client(**client_kwargs)

            async def run_with_timeout():
                async with client:
                    logger.debug(
                        f"FastMCP {args.transport.upper()} client connection established"
                    )
                    await run_test_suite(client, args)
                logger.debug(
                    f"Test suite completed successfully with {args.transport.upper()} transport"
                )
                return True

            # Run with timeout to prevent hanging indefinitely
            try:
                await asyncio.wait_for(run_with_timeout(), timeout=15.0)
                return True
            except asyncio.TimeoutError:
                logger.error(
                    f"{args.transport.upper()} transport timed out after 15 seconds"
                )
                print(
                    f"x {args.transport.upper()} transport timed out after 15 seconds"
                )
                return False

        except Exception as e:
            logger.error(
                f"{args.transport.upper()} transport error: %s", str(e), exc_info=True
            )
            print(f"x Error with {args.transport.upper()} transport: {e}")

            if args.transport == "http":
                print(
                    f"! Make sure the server is running at {client_kwargs['transport']}"
                )
                if "ssl" in str(e).lower() or "certificate" in str(e).lower():
                    print(
                        "! SSL certificate verification error. Try --insecure flag for testing"
                    )
                print("! Try using the STDIO transport instead with --transport stdio")
            else:
                print(f"! Make sure the server script exists: {args.server_path}")

            return False

        finally:
            # Clean up SSL patches if they were applied
            if ssl_patch is not None:
                ssl_patch.restore_ssl_settings()

    except Exception as e:
        logger.error("Unexpected error: %s", str(e), exc_info=True)
        print(f"x Unexpected error: {e}")
        return False


async def run_test_suite(client: Client, args) -> None:
    """Run the full test suite against an initialized MCP client."""
    try:
        await client.ping()
        print("Connected to MCP server successfully!")
        logger.debug("FastMCP client connection established")
    except RuntimeError:
        print("Connection to MCP server was not established")
        logger.debug("Connection to MCP server was not established")
        raise

    # generate a uuid
    client_id = uuid.uuid4().hex
    print(f"Using client ID: {client_id}")

    # Run tests
    incident_id = await _run_create_incident(client, client_id)
    logger.debug(f"create_incident test completed with incident_id: {incident_id}")
    await asyncio.sleep(0.1)

    solution_id = await _run_create_solution(client, client_id, [incident_id])
    logger.debug(f"create_solution test completed with solution_id: {solution_id}")
    await asyncio.sleep(0.1)

    await _run_accept_file(
        client,
        client_id,
        SolutionFile(
            uri="file://ExampleService.java",
            content="// Example content for testing",
        ),
    )
    logger.debug("accept_file test completed")
    await asyncio.sleep(0.1)

    best_hint = await _run_get_best_hint(client)
    logger.debug(
        f"get_best_hint test completed with result: {best_hint}"
    )  # (len: {len(best_hint) if best_hint else 0})")
    await asyncio.sleep(0.1)

    success_rates = await _run_get_success_rate(client)
    logger.debug(
        f"success_rate test completed with result: {success_rates}"
    )  # (len: {len(success_rates) if success_rates else 0})")
    await asyncio.sleep(0.1)

    print("\no All tests completed successfully!")
    logger.debug("All test functions completed successfully")


def main() -> None:
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Test client for MCP Solution Server")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Hostname of the MCP server (for http transport)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port of the MCP server (for http transport)",
    )
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["http", "stdio"],
        help="Transport protocol (http or stdio)",
    )
    parser.add_argument(
        "--mount-path",
        type=str,
        default="/",
        help="Path the MCP server is mounted behind (ie, /hub/services/kai) (for http transport)",
    )
    # Calculate default server path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_server_path = os.path.dirname(
        script_dir
    )  # Parent directory of the tests dir

    parser.add_argument(
        "--server-path",
        default=default_server_path,
        help="Path to the MCP server script (for stdio transport)",
    )
    parser.add_argument(
        "--task-key", default="test-migration", help="Task key to use for tests"
    )
    parser.add_argument(
        "--full-output", action="store_true", help="Show full output for resources"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed debug information"
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Allow insecure connections (skip SSL verification for http transport)",
    )
    parser.add_argument(
        "--bearer-token",
        type=str,
        help="Bearer token for authentication (for http transport)",
    )

    args = parser.parse_args()

    # Set log level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    success = asyncio.run(run_tests(args))
    sys.exit(0 if success else 1)


# A pytest-compatible test function that actually runs the tests
def test_mcp_solution_client() -> None:
    """Test function that will be run by pytest.

    This runs the same tests as when using the script directly, but with a non-async
    entry point that pytest can call.

    This test actually starts an MCP server using stdio transport and runs the
    full test suite against it.
    """

    # Create args for stdio transport
    args = MCPClientArgs(
        host="localhost",
        port=8000,
        transport="stdio",
        server_path=Path(os.path.abspath(__file__)).parent,
        mount_path="/",
        full_output=False,
        verbose=False,
        insecure=False,
        bearer_token=None,
    )

    print(f"Using server script path: {args.server_path}")
    print(f"Current working directory: {os.getcwd()}")

    # Run the tests using the same function as the CLI with a timeout
    # This will start up the stdio server and run the full test suite
    try:
        # Set a reasonable timeout to prevent hanging in CI/CD
        success = asyncio.run(asyncio.wait_for(run_tests(args), timeout=30.0))
    except asyncio.TimeoutError:
        print("x Test timed out after 30 seconds")
        success = False

    # Assert that the tests succeeded
    assert (
        success
    ), "MCP solution client tests failed"  # nosec B101 - This is a test script


if __name__ == "__main__":
    main()

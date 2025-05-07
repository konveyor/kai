#!/usr/bin/env python3
"""
MCP Solution Server Test Client

This script tests the functionality of the MCP Solution Server by establishing
a proper Model Context Protocol connection and testing the available tools and resources.
"""

import argparse
import asyncio
import json
import logging
import os
import ssl
import sys
import warnings

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

# Store the original SSL context creator to patch it properly
original_create_default_context = ssl.create_default_context

# Import httpx for direct inspection
try:
    import httpx
except ImportError:
    httpx = None

# Configure logger
logger = logging.getLogger("kai-mcp-client")

# Configure console handler with a specific format
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Default level is INFO, verbose will set to DEBUG
logger.setLevel(logging.INFO)


def format_code_block(code: str, language: str = "java") -> str:
    """Format a code block with syntax highlighting."""
    if not code:
        return "No code provided"
    return f"```{language}\n{code}\n```"


def format_diff_block(diff: str) -> str:
    """Format a diff block with syntax highlighting."""
    if not diff:
        return "No diff provided"
    return f"```diff\n{diff}\n```"


async def _run_store_solution(session: ClientSession) -> int:
    """Test the store_solution tool by creating a new solution."""
    print("\n--- Testing store_solution ---")

    task = {
        "key": "test-migration",
        "description": "Test migration task",
        "source_framework": "java-ee",
        "target_framework": "quarkus",
        "language": "java",
    }
    logger.debug("Preparing task data: %s", task)

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
    logger.debug("Before code prepared (length: %d)", len(before_code))

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
    logger.debug("After code prepared (length: %d)", len(after_code))

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
    logger.debug("Diff prepared (length: %d)", len(diff))
    status = "accepted"

    try:
        logger.debug("Calling store_solution tool with status: %s", status)
        result = await session.call_tool(
            "store_solution",
            arguments={
                "task": task,
                "before_code": before_code,
                "after_code": after_code,
                "diff": diff,
                "status": status,
            },
        )
        logger.debug("store_solution tool call completed, processing result")

        # Extract the solution ID from the result
        solution_id = None
        if hasattr(result, "content"):
            logger.debug(
                "Result has content attribute with %d items", len(result.content)
            )
            for content_item in result.content:
                if hasattr(content_item, "text"):
                    try:
                        solution_id = int(content_item.text)
                        logger.debug("Found solution_id: %s", solution_id)
                        break
                    except (ValueError, TypeError):
                        logger.debug(
                            "Failed to parse content item as integer: %s",
                            content_item.text,
                        )
                        pass
                else:
                    logger.debug("Content item has no text attribute: %s", content_item)

        print(f"✅ Solution created with ID: {solution_id}")
        return solution_id or -1
    except Exception as e:
        logger.error("Error creating solution: %s", str(e), exc_info=True)
        print(f"❌ Error creating solution: {e}")
        return -1


async def _run_find_related_solutions(session: ClientSession, task_key: str) -> None:
    """Test the find_related_solutions tool by searching for existing solutions."""
    print("\n--- Testing find_related_solutions ---")

    try:
        logger.debug(
            "Calling find_related_solutions tool with task_key: %s, limit: 5", task_key
        )
        result = await session.call_tool(
            "find_related_solutions", arguments={"task_key": task_key, "limit": 5}
        )
        logger.debug("find_related_solutions tool call completed, processing result")

        # Extract the solutions from the result
        solutions = []
        if hasattr(result, "content"):
            logger.debug(
                "Result has content attribute with %d items", len(result.content)
            )
            for content_item in result.content:
                if hasattr(content_item, "text"):
                    try:
                        # Parse each item as an individual JSON object
                        logger.debug(
                            "Parsing JSON from content item: %s",
                            (
                                content_item.text[:100] + "..."
                                if len(content_item.text) > 100
                                else content_item.text
                            ),
                        )
                        solution_data = json.loads(content_item.text)
                        solutions.append(solution_data)
                        logger.debug(
                            "Successfully parsed JSON solution: %s",
                            solution_data.get("id", "No ID"),
                        )
                    except (json.JSONDecodeError, TypeError) as json_err:
                        logger.error("Failed to parse JSON: %s", str(json_err))
                        print(f"Failed to parse JSON from: {content_item.text}")
                        pass
                else:
                    logger.debug("Content item has no text attribute: %s", content_item)

        if solutions:
            logger.debug("Found %d solutions", len(solutions))
            print(f"✅ Found {len(solutions)} related solutions:")
            for i, solution in enumerate(solutions):
                logger.debug("Processing solution %d: %s", i, solution.get("id"))
                print(f"  - ID: {solution.get('id')}")
                print(f"    Status: {solution.get('status')}")
                print(f"    Task Key: {solution.get('task_key')}")

                # Add snippet of before/after code if available
                before_code = solution.get("before_code", "")
                after_code = solution.get("after_code", "")

                if before_code:
                    logger.debug(
                        "Solution has before_code (length: %d)", len(before_code)
                    )
                    print(
                        f"    Before: {before_code[:30]}..."
                        if len(before_code) > 30
                        else f"    Before: {before_code}"
                    )
                if after_code:
                    logger.debug(
                        "Solution has after_code (length: %d)", len(after_code)
                    )
                    print(
                        f"    After: {after_code[:30]}..."
                        if len(after_code) > 30
                        else f"    After: {after_code}"
                    )

                print()
        else:
            logger.debug("No solutions found for task_key: %s", task_key)
            print("ℹ️ No related solutions found")

    except Exception as e:
        logger.error("Error finding related solutions: %s", str(e), exc_info=True)
        print(f"❌ Error finding related solutions: {e}")


async def _run_success_rate(session: ClientSession, task_key: str) -> None:
    """Test the success_rate resource by getting the success rate for a task key."""
    print("\n--- Testing success_rate resource ---")

    try:
        resource_uri = f"kai://success_rate/{task_key}"
        logger.debug("Reading resource: %s", resource_uri)
        result = await session.read_resource(resource_uri)
        logger.debug("Resource read completed, processing result")

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            logger.debug(
                "Result has contents attribute with %d items", len(result.contents)
            )
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    logger.debug("Found content text: %s", content)
                    break
                else:
                    logger.debug("Content item has no text attribute: %s", content_item)

        if content:
            logger.debug("Successfully retrieved success rate information")
            print(f"✅ {content}")
        else:
            logger.debug(
                "No success rate information available for task_key: %s", task_key
            )
            print("ℹ️ No success rate information available")
    except Exception as e:
        logger.error("Error fetching success rate: %s", str(e), exc_info=True)
        print(f"❌ Error fetching success rate: {e}")


async def _run_solutions(session: ClientSession, task_key: str) -> None:
    """Test the solutions resource by getting all solutions for a task key."""
    print("\n--- Testing solutions resource ---")

    try:
        resource_uri = f"kai://solutions/{task_key}"
        logger.debug("Reading resource: %s", resource_uri)
        result = await session.read_resource(resource_uri)
        logger.debug("Resource read completed, processing result")

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            logger.debug(
                "Result has contents attribute with %d items", len(result.contents)
            )
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    logger.debug("Found content text (length: %d)", len(content))
                    break
                else:
                    logger.debug("Content item has no text attribute: %s", content_item)

        if content:
            logger.debug("Successfully retrieved solutions history")
            print("✅ Solutions history retrieved successfully")
            # Display a summary
            if "No solutions found" in content:
                logger.debug("No solutions found message in content")
                print("ℹ️ " + content)
            else:
                solution_count = content.count("Solution ID:")
                logger.debug(
                    "Found %d solutions for task '%s'", solution_count, task_key
                )
                print(f"ℹ️ Found {solution_count} solutions for task '{task_key}'")

                # Print the first solution details only to avoid overwhelming output
                if solution_count > 0:
                    first_solution = content.split("---")[0].strip()
                    logger.debug(
                        "First solution: %s",
                        (
                            first_solution[:100] + "..."
                            if len(first_solution) > 100
                            else first_solution
                        ),
                    )
                    print("\nFirst solution:")
                    print(first_solution)

                    if solution_count > 1:
                        logger.debug("There are %d more solutions", solution_count - 1)
                        print(f"\n... and {solution_count-1} more solutions")
        else:
            logger.debug("No solutions history available for task_key: %s", task_key)
            print("ℹ️ No solutions history available")
    except Exception as e:
        logger.error("Error fetching solutions: %s", str(e), exc_info=True)
        print(f"❌ Error fetching solutions: {e}")


async def _run_example_solution(session: ClientSession, task_key: str) -> None:
    """Test the example_solution resource by getting the best solution example."""
    print("\n--- Testing example_solution resource ---")

    try:
        resource_uri = f"kai://example_solution/{task_key}"
        logger.debug("Reading resource: %s", resource_uri)
        result = await session.read_resource(resource_uri)
        logger.debug("Resource read completed, processing result")

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            logger.debug(
                "Result has contents attribute with %d items", len(result.contents)
            )
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    logger.debug("Found content text (length: %d)", len(content))
                    break
                else:
                    logger.debug("Content item has no text attribute: %s", content_item)

        if content:
            logger.debug("Successfully retrieved example solution content")
            if "No accepted solutions found" in content:
                logger.debug("No accepted solutions found message in content")
                print(f"ℹ️ {content}")
            else:
                logger.debug("Example solution retrieved successfully")
                print("✅ Example solution retrieved successfully:")
                header = content.split("\n\n")[0]
                logger.debug("Solution header: %s", header)
                print(header)  # Show just the header

                # Preview the solution with limited output
                if "Before Code:" in content:
                    before_index = content.find("Before Code:") + len("Before Code:")
                    before_end = content.find("```\n\n", before_index)
                    if before_end > before_index:
                        code_preview = content[before_index : before_index + 60].strip()
                        if len(code_preview) > 50:
                            code_preview = code_preview[:50] + "..."
                        logger.debug("Before code preview: %s", code_preview)
                        print(f"Before code preview: {code_preview}")

                if "After Code:" in content:
                    after_index = content.find("After Code:") + len("After Code:")
                    after_end = content.find("```\n\n", after_index)
                    if after_end > after_index:
                        code_preview = content[after_index : after_index + 60].strip()
                        if len(code_preview) > 50:
                            code_preview = code_preview[:50] + "..."
                        logger.debug("After code preview: %s", code_preview)
                        print(f"After code preview: {code_preview}")

                print("\nUse --full-output to see complete solutions")
        else:
            logger.debug("No example solution available for task_key: %s", task_key)
            print("ℹ️ No example solution available")
    except Exception as e:
        logger.error("Error fetching example solution: %s", str(e), exc_info=True)
        print(f"❌ Error fetching example solution: {e}")


async def run_tests(args) -> bool:
    """Run all the tests with the appropriate transport.
    Returns True if all tests completed successfully, False otherwise.
    """
    print("MCP Solution Server Test Client")
    print("==============================")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Transport: {args.transport}")
    print(f"Task key: {args.task_key}")
    if args.insecure and args.transport == "http":
        print("SSL verification: Disabled (insecure mode)")

    logger.debug("Starting test run with arguments: %s", vars(args))

    try:
        if args.transport == "http":
            # Setup HTTP transport using SSE
            transport = ""
            if not args.host.startswith("http"):
                transport = "http://"
            server_url = f"{transport}{args.host}:{args.port}/sse"
            print(f"Connecting to server at {server_url}...")
            logger.debug("Initializing HTTP/SSE transport with URL: %s", server_url)

            try:
                # Configure SSL verification if insecure flag is set
                if args.insecure:
                    logger.debug(
                        "Disabling SSL certificate verification by patching SSL module"
                    )
                    # Disable SSL verification warnings
                    warnings.filterwarnings(
                        "ignore", message="Unverified HTTPS request"
                    )
                    warnings.filterwarnings("ignore", category=Warning)

                    # Patch SSL module's default context creator to disable verification
                    def unverified_context(*args, **kwargs):
                        context = original_create_default_context(*args, **kwargs)
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        return context

                    # Apply the patch
                    ssl.create_default_context = unverified_context
                    logger.debug("Successfully patched ssl.create_default_context")

                    # For httpx - try to patch its SSL defaults too if available
                    if httpx:
                        try:
                            # Try to patch httpx client classes
                            old_client_init = httpx.Client.__init__

                            def patched_client_init(self, *args, **kwargs):
                                kwargs["verify"] = False
                                old_client_init(self, *args, **kwargs)

                            httpx.Client.__init__ = patched_client_init

                            # Same for AsyncClient
                            old_async_client_init = httpx.AsyncClient.__init__

                            def patched_async_client_init(self, *args, **kwargs):
                                kwargs["verify"] = False
                                old_async_client_init(self, *args, **kwargs)

                            httpx.AsyncClient.__init__ = patched_async_client_init
                            logger.debug("Patched httpx Client classes")

                        except Exception as patch_err:
                            logger.warning("Failed to patch httpx: %s", patch_err)

                    # Also set environment variables as backup
                    os.environ["SSL_CERT_VERIFY"] = "false"
                    os.environ["HTTPX_SSL_VERIFY"] = "false"
                    os.environ["HTTPX_NO_VERIFY"] = "true"
                    os.environ["PYTHONHTTPSVERIFY"] = "0"

                    print("⚠️ Warning: SSL certificate verification is disabled")

                try:
                    async with sse_client(server_url) as (read, write):
                        logger.debug("SSE client connection established")
                        async with ClientSession(read, write) as session:
                            logger.debug("MCP ClientSession initialized")
                            await run_test_suite(session, args)
                    logger.debug(
                        "Test suite completed successfully with HTTP transport"
                    )
                    return True
                finally:
                    # Clean up patches and environment variables if insecure mode was used
                    if args.insecure:
                        # Restore original SSL context creator
                        ssl.create_default_context = original_create_default_context
                        logger.debug("Restored original ssl.create_default_context")

                        # Restore httpx patches if applied
                        if httpx:
                            try:
                                if "old_client_init" in locals() and hasattr(
                                    httpx, "Client"
                                ):
                                    httpx.Client.__init__ = old_client_init
                                    logger.debug(
                                        "Restored original httpx.Client.__init__"
                                    )

                                if "old_async_client_init" in locals() and hasattr(
                                    httpx, "AsyncClient"
                                ):
                                    httpx.AsyncClient.__init__ = old_async_client_init
                                    logger.debug(
                                        "Restored original httpx.AsyncClient.__init__"
                                    )
                            except Exception as restore_err:
                                logger.warning(
                                    "Failed to restore httpx patches: %s", restore_err
                                )

                        # Clean up environment variables
                        ssl_env_vars = [
                            "SSL_CERT_VERIFY",
                            "HTTPX_SSL_VERIFY",
                            "HTTPX_NO_VERIFY",
                            "PYTHONHTTPSVERIFY",
                        ]

                        for env_var in ssl_env_vars:
                            if env_var in os.environ:
                                del os.environ[env_var]

                        logger.debug("Cleaned up all SSL verification settings")
            except Exception as e:
                logger.error("HTTP transport error: %s", str(e), exc_info=True)
                print(f"❌ Error with HTTP transport: {e}")
                print(f"ℹ️ Make sure the server is running at {server_url}")

                # Add specific advice for SSL certificate errors
                if (
                    isinstance(e, ssl.SSLError)
                    or "ssl" in str(e).lower()
                    or "certificate" in str(e).lower()
                ):
                    print("ℹ️ SSL certificate verification error. Try these options:")
                    print(
                        "   1. Use the --insecure flag to bypass SSL verification (not recommended for production)"
                    )
                    print("   2. Use a valid SSL certificate on the server")
                    print("   3. Add the server's certificate to your trusted CA store")

                print("ℹ️ Try using the STDIO transport instead with --transport stdio")
                return False

        else:  # stdio transport
            # Use the server path from args (which already has the correct default)
            server_path = args.server_path
            print(f"Using server path: {server_path}")
            logger.debug(
                "Initializing STDIO transport with server path: %s", server_path
            )

            # Setup STDIO transport
            server_params = StdioServerParameters(
                command="python",
                args=["-m", "main", "--transport", "stdio"],
                cwd=server_path,
            )
            logger.debug("STDIO server parameters: %s", server_params)

            try:
                # Create a timeout to prevent hanging in case of issues
                async def run_with_timeout():
                    async with stdio_client(server_params) as (read, write):
                        logger.debug("STDIO client connection established")
                        async with ClientSession(read, write) as session:
                            logger.debug("MCP ClientSession initialized")
                            await run_test_suite(session, args)
                    logger.debug(
                        "Test suite completed successfully with STDIO transport"
                    )
                    return True

                # Run with timeout to prevent hanging indefinitely
                try:
                    await asyncio.wait_for(run_with_timeout(), timeout=15.0)
                    return True
                except asyncio.TimeoutError:
                    logger.error("STDIO transport timed out after 15 seconds")
                    print("❌ STDIO transport timed out after 15 seconds")
                    return False
            except Exception as e:
                logger.error("STDIO transport error: %s", str(e), exc_info=True)
                print(f"❌ Error with STDIO transport: {e}")
                print(f"ℹ️ Make sure the main.py exists in {server_path}")
                return False

    except Exception as e:
        logger.error("Unexpected error: %s", str(e), exc_info=True)
        print(f"❌ Unexpected error: {e}")
        return False


async def run_test_suite(session: ClientSession, args) -> None:
    """Run the full test suite against an initialized MCP session."""
    # Initialize the connection
    print("Initializing MCP connection...")
    logger.debug("Calling session.initialize()")
    await session.initialize()
    print("Connected to MCP server successfully!")
    logger.debug("MCP connection initialized successfully")

    # Run tests
    logger.debug("Starting store_solution test")
    solution_id = await _run_store_solution(session)
    logger.debug("store_solution test completed with solution_id: %s", solution_id)

    # Wait a bit for data to be persisted
    print("Waiting for database operations to complete...")
    logger.debug("Waiting for database operations to complete...")
    await asyncio.sleep(1)

    logger.debug(
        "Starting find_related_solutions test with task_key: %s", args.task_key
    )
    await _run_find_related_solutions(session, args.task_key)

    logger.debug("Starting success_rate test with task_key: %s", args.task_key)
    await _run_success_rate(session, args.task_key)

    logger.debug("Starting solutions test with task_key: %s", args.task_key)
    await _run_solutions(session, args.task_key)

    logger.debug("Starting example_solution test with task_key: %s", args.task_key)
    await _run_example_solution(session, args.task_key)

    print("\n✅ All tests completed successfully!")
    logger.debug("All test functions completed successfully")


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Test client for MCP Solution Server")
    parser.add_argument(
        "--host", default="localhost", help="Hostname of the MCP server"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port of the MCP server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["http", "stdio"],
        help="Transport protocol (http or stdio)",
    )
    # Calculate default server path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_server_path = os.path.dirname(
        script_dir
    )  # Parent directory of the tests dir

    parser.add_argument(
        "--server-path",
        default=default_server_path,
        help="Path to the MCP server directory (for stdio transport)",
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
        help="Allow insecure connections (skip SSL verification)",
    )

    args = parser.parse_args()

    # Set log level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    success = asyncio.run(run_tests(args))
    sys.exit(0 if success else 1)


# A pytest-compatible test function that actually runs the tests
def test_mcp_solution_client():
    """Test function that will be run by pytest.

    This runs the same tests as when using the script directly, but with a non-async
    entry point that pytest can call.

    This test actually starts an MCP server using stdio transport and runs the
    full test suite against it.
    """

    # Create args for stdio transport
    class Args:
        host = "localhost"
        port = 8000
        transport = "stdio"  # Use stdio transport to test without network

        # Calculate correct server path regardless of where the test is run from
        # This handles both pytest . from kai_mcp_solution_server dir
        # and ./run_tests.sh from project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.dirname(script_dir)

        # If running from project root via run_tests.sh, the relative path
        # will be different, so check if we need to adjust
        if not os.path.exists(os.path.join(server_path, "main.py")):
            # Try looking for the correct directory
            possible_server_path = os.path.join(os.getcwd(), "kai_mcp_solution_server")
            if os.path.exists(os.path.join(possible_server_path, "main.py")):
                server_path = possible_server_path
                print(f"Adjusted server path to: {server_path}")
            else:
                print(
                    f"WARNING: Could not find main.py in {server_path} or {possible_server_path}"
                )

        task_key = "test-migration"
        full_output = False
        verbose = False  # Only enable verbose logging when debugging problems
        insecure = False

    print(f"Using server path: {Args.server_path}")
    print(f"Current working directory: {os.getcwd()}")

    # Run the tests using the same function as the CLI with a timeout
    # This will start up the stdio server and run the full test suite
    try:
        # Set a reasonable timeout to prevent hanging in CI/CD
        success = asyncio.run(asyncio.wait_for(run_tests(Args()), timeout=30.0))
    except asyncio.TimeoutError:
        print("❌ Test timed out after 30 seconds")
        success = False

    # Assert that the tests succeeded
    assert success, "MCP solution client tests failed"


if __name__ == "__main__":
    main()

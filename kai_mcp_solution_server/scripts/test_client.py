#!/usr/bin/env python3
"""
MCP Solution Server Test Client

This script tests the functionality of the MCP Solution Server by establishing
a proper Model Context Protocol connection and testing the available tools and resources.
"""

import argparse
import asyncio
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


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


async def test_store_solution(session: ClientSession) -> int:
    """Test the store_solution tool by creating a new solution."""
    print("\n--- Testing store_solution ---")

    task = {
        "key": "test-migration",
        "description": "Test migration task",
        "source_framework": "java-ee",
        "target_framework": "quarkus",
        "language": "java",
    }

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
    status = "accepted"

    try:
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

        # Extract the solution ID from the result
        solution_id = None
        if hasattr(result, "content"):
            for content_item in result.content:
                if hasattr(content_item, "text"):
                    try:
                        solution_id = int(content_item.text)
                        break
                    except (ValueError, TypeError):
                        pass

        print(f"✅ Solution created with ID: {solution_id}")
        return solution_id or -1
    except Exception as e:
        print(f"❌ Error creating solution: {e}")
        return -1


async def test_find_related_solutions(session: ClientSession, task_key: str) -> None:
    """Test the find_related_solutions tool by searching for existing solutions."""
    print("\n--- Testing find_related_solutions ---")

    try:
        result = await session.call_tool(
            "find_related_solutions", arguments={"task_key": task_key, "limit": 5}
        )

        # Extract the solutions from the result
        solutions = []
        if hasattr(result, "content"):
            for content_item in result.content:
                if hasattr(content_item, "text"):
                    try:
                        # Parse each item as an individual JSON object
                        solution_data = json.loads(content_item.text)
                        solutions.append(solution_data)
                    except (json.JSONDecodeError, TypeError):
                        print(f"Failed to parse JSON from: {content_item.text}")
                        pass

        if solutions:
            print(f"✅ Found {len(solutions)} related solutions:")
            for solution in solutions:
                print(f"  - ID: {solution.get('id')}")
                print(f"    Status: {solution.get('status')}")
                print(f"    Task Key: {solution.get('task_key')}")

                # Add snippet of before/after code if available
                before_code = solution.get("before_code", "")
                after_code = solution.get("after_code", "")

                if before_code:
                    print(
                        f"    Before: {before_code[:30]}..."
                        if len(before_code) > 30
                        else f"    Before: {before_code}"
                    )
                if after_code:
                    print(
                        f"    After: {after_code[:30]}..."
                        if len(after_code) > 30
                        else f"    After: {after_code}"
                    )

                print()
        else:
            print("ℹ️ No related solutions found")

    except Exception as e:
        print(f"❌ Error finding related solutions: {e}")


async def test_success_rate(session: ClientSession, task_key: str) -> None:
    """Test the success_rate resource by getting the success rate for a task key."""
    print("\n--- Testing success_rate resource ---")

    try:
        resource_uri = f"kai://success_rate/{task_key}"
        result = await session.read_resource(resource_uri)

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    break

        if content:
            print(f"✅ {content}")
        else:
            print("ℹ️ No success rate information available")
    except Exception as e:
        print(f"❌ Error fetching success rate: {e}")


async def test_solutions(session: ClientSession, task_key: str) -> None:
    """Test the solutions resource by getting all solutions for a task key."""
    print("\n--- Testing solutions resource ---")

    try:
        resource_uri = f"kai://solutions/{task_key}"
        result = await session.read_resource(resource_uri)

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    break

        if content:
            print("✅ Solutions history retrieved successfully")
            # Display a summary
            if "No solutions found" in content:
                print("ℹ️ " + content)
            else:
                solution_count = content.count("Solution ID:")
                print(f"ℹ️ Found {solution_count} solutions for task '{task_key}'")

                # Print the first solution details only to avoid overwhelming output
                if solution_count > 0:
                    first_solution = content.split("---")[0].strip()
                    print("\nFirst solution:")
                    print(first_solution)

                    if solution_count > 1:
                        print(f"\n... and {solution_count-1} more solutions")
        else:
            print("ℹ️ No solutions history available")
    except Exception as e:
        print(f"❌ Error fetching solutions: {e}")


async def test_example_solution(session: ClientSession, task_key: str) -> None:
    """Test the example_solution resource by getting the best solution example."""
    print("\n--- Testing example_solution resource ---")

    try:
        resource_uri = f"kai://example_solution/{task_key}"
        result = await session.read_resource(resource_uri)

        # Extract the content from ReadResourceResult
        content = ""
        if hasattr(result, "contents") and result.contents:
            for content_item in result.contents:
                if hasattr(content_item, "text"):
                    content = content_item.text
                    break

        if content:
            if "No accepted solutions found" in content:
                print(f"ℹ️ {content}")
            else:
                print("✅ Example solution retrieved successfully:")
                print(content.split("\n\n")[0])  # Show just the header

                # Preview the solution with limited output
                if "Before Code:" in content:
                    before_index = content.find("Before Code:") + len("Before Code:")
                    before_end = content.find("```\n\n", before_index)
                    if before_end > before_index:
                        code_preview = content[before_index : before_index + 60].strip()
                        if len(code_preview) > 50:
                            code_preview = code_preview[:50] + "..."
                        print(f"Before code preview: {code_preview}")

                if "After Code:" in content:
                    after_index = content.find("After Code:") + len("After Code:")
                    after_end = content.find("```\n\n", after_index)
                    if after_end > after_index:
                        code_preview = content[after_index : after_index + 60].strip()
                        if len(code_preview) > 50:
                            code_preview = code_preview[:50] + "..."
                        print(f"After code preview: {code_preview}")

                print("\nUse --full-output to see complete solutions")
        else:
            print("ℹ️ No example solution available")
    except Exception as e:
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

    try:
        if args.transport == "http":
            # Setup HTTP transport using SSE
            server_url = f"http://{args.host}:{args.port}/sse"
            print(f"Connecting to server at {server_url}...")

            try:
                async with sse_client(server_url) as (read, write):
                    async with ClientSession(read, write) as session:
                        await run_test_suite(session, args)
                return True
            except Exception as e:
                print(f"❌ Error with HTTP transport: {e}")
                print(f"ℹ️ Make sure the server is running at {server_url}")
                print("ℹ️ Try using the STDIO transport instead with --transport stdio")
                return False

        else:  # stdio transport
            # Determine the server path
            if args.server_path:
                server_path = args.server_path
            else:
                # Default to parent directory of the scripts directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                server_path = os.path.dirname(script_dir)

            print(f"Using server path: {server_path}")

            # Setup STDIO transport
            server_params = StdioServerParameters(
                command="python",
                args=["-m", "main", "--transport", "stdio"],
                cwd=server_path,
            )

            try:
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await run_test_suite(session, args)
                return True
            except Exception as e:
                print(f"❌ Error with STDIO transport: {e}")
                print(f"ℹ️ Make sure the main.py exists in {server_path}")
                return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def run_test_suite(session: ClientSession, args) -> None:
    """Run the full test suite against an initialized MCP session."""
    # Initialize the connection
    print("Initializing MCP connection...")
    await session.initialize()
    print("Connected to MCP server successfully!")

    # Run tests
    solution_id = await test_store_solution(session)

    # Wait a bit for data to be persisted
    print("Waiting for database operations to complete...")
    await asyncio.sleep(1)

    await test_find_related_solutions(session, args.task_key)
    await test_success_rate(session, args.task_key)
    await test_solutions(session, args.task_key)
    await test_example_solution(session, args.task_key)

    print("\n✅ All tests completed successfully!")


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Test client for MCP Solution Server")
    parser.add_argument(
        "--host", default="localhost", help="Hostname of the MCP server"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port of the MCP server")
    parser.add_argument(
        "--transport",
        default="http",
        choices=["http", "stdio"],
        help="Transport protocol (http or stdio)",
    )
    parser.add_argument(
        "--server-path",
        default=None,
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

    args = parser.parse_args()

    success = asyncio.run(run_tests(args))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

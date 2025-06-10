#!/usr/bin/env python3
"""
Integration tests for KAI MCP solution server.

This test module verifies that the MCP solution server can be started,
imported, and communicates correctly via the Model Context Protocol.
"""

import asyncio
import os
import subprocess  # nosec B404 - Subprocess is necessary for integration testing
import sys
import tempfile
import time
import unittest
from pathlib import Path

import mcp_client

from kai_mcp_solution_server.server import SolutionServerSettings


class TestMCPIntegration(unittest.TestCase):
    """Test integration with the MCP solution server."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        os.environ["KAI_DB_DSN"] = (
            f"sqlite+aiosqlite:///{self.temp_path}/kai_mcp_solution_server.db"
        )
        os.environ["KAI_LLM_PARAMS"] = '{"model": "fake"}'

        self.tests_path = Path(__file__).parent
        self.client_path = self.tests_path / "mcp_client.py"
        self.server_path = (
            self.tests_path.parent / "src/kai_mcp_solution_server/__main__.py"
        )

        # Log details for debugging
        print("=== Test Setup ===")
        print(f"Temporary directory: {self.temp_dir.name}")
        print(f"Tests directory: {self.tests_path}")
        print(f"Client path: {self.client_path}")
        print(f"Server path: {self.server_path}")
        print(f"Environment:")
        print(f"  KAI_DB_DSN: {os.environ['KAI_DB_DSN']}")
        print(f"  KAI_LLM_PARAMS: {os.environ['KAI_LLM_PARAMS']}")

    def tearDown(self):
        """Clean up after tests."""
        try:
            self.temp_dir.cleanup()
        except (OSError, PermissionError) as e:
            print(f"Warning: Failed to clean up after tests: {e}")

    def test_server_start(self):
        """
        Test that the MCP solution server can be started with the help command.
        """

        # Start the server process
        print(f"Starting server: {self.server_path}")

        # Run the server with --help to verify it works
        # Use explicit path to Python executable and validate path existence for security
        python_executable = sys.executable
        if not os.path.isfile(python_executable):
            self.fail(f"Invalid Python executable path: {python_executable}")

        if not os.path.isfile(self.server_path):
            self.fail(f"Invalid main script path: {self.server_path}")

        # Use secure paths and arguments
        # Paths are validated above to prevent security issues
        result = (
            subprocess.run(  # nosec B603 - We've validated the command arguments above
                [python_executable, self.server_path, "--help"],
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PYTHONUNBUFFERED": "1",
                },
            )
        )

        # Print output for debugging
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)

        # Check that the server help command succeeded
        self.assertEqual(
            result.returncode,
            0,
            f"Server failed with code {result.returncode}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}",
        )

        # Verify help output contains expected information
        self.assertIn("usage:", result.stdout, "Help message not found")
        self.assertIn("transport", result.stdout, "Transport argument not found")

        print("Server start test passed successfully!")

    @unittest.skip(reason="TODO: Determine if this test is still needed")
    def test_direct_import(self):
        """
        Test that we can directly import the solution server modules.
        """

        # This test ensures that the modules can be imported directly
        # which tests that the package structure is correct

        # Make sure the server directory is in the path

        try:
            # Add the server directory to the path if needed
            if self.server_dir not in sys.path:
                sys.path.insert(0, self.server_dir)
                print(f"Added server directory to sys.path: {self.server_dir}")

            # Try importing the main module
            import importlib

            # Debug imports with more detailed error handling
            try:
                main_module = importlib.import_module("main")
                print("Successfully imported main module")
            except ImportError as e:
                print(f"Failed to import main module: {e}")
                raise

            # Import the DAO module with detailed error handling
            try:
                dao_module = importlib.import_module("kai_solutions_dao")
                print("Successfully imported kai_solutions_dao module")
            except ImportError as e:
                print(f"Failed to import kai_solutions_dao module: {e}")
                raise

            # Check if MCP module can be imported
            try:
                # Check for the required MCP modules using importlib.util
                import importlib.util

                # Verify MCP is installed
                spec = importlib.util.find_spec("mcp")
                self.assertIsNotNone(spec, "MCP package is not installed")

                # Verify the required fastmcp module
                fastmcp_spec = importlib.util.find_spec("mcp.server.fastmcp")
                self.assertIsNotNone(
                    fastmcp_spec, "mcp.server.fastmcp module not found"
                )

                print("Successfully found MCP modules")
            except ImportError as e:
                print(f"Failed to check MCP modules: {e}")
                raise

            # Verify basic functionality
            self.assertTrue(
                hasattr(main_module, "mcp"), "MCP server not found in main module"
            )
            self.assertTrue(
                hasattr(dao_module, "KaiSolutionsDAO"), "DAO class not found"
            )

            # Create a test solution in a clean DB
            dao = dao_module.KaiSolutionsDAO()

            # Create a test solution
            task = {
                "key": "test-direct-import",
                "description": "Test direct import",
            }

            solution_id = dao.create_solution(
                task=task,
                before_code="// Before",
                after_code="// After",
                diff="// Diff",
                status="accepted",
            )

            # Verify solution was created
            self.assertIsNotNone(solution_id, "Failed to create solution")
            self.assertGreater(solution_id, 0, "Invalid solution ID")

            print(f"Created test solution with ID: {solution_id}")

        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")

    def test_mcp_client_endpoints(self):
        """
        Test the server endpoints using the mcp_client's
        test_mcp_solution_client function.
        """
        # Run the existing test function from mcp_client by running its body directly
        # This will test all the endpoints using the client's built-in test functionality

        # Create args for stdio transport - copied from test_mcp_solution_client

        # Run the tests using the same function as the CLI with a timeout
        # This will start up the stdio server and run the full test suite
        try:
            # Set a reasonable timeout to prevent hanging in CI/CD
            success = asyncio.run(
                asyncio.wait_for(
                    mcp_client.run_tests(
                        mcp_client.MCPClientArgs(
                            server_path=self.server_path,
                        )
                    ),
                    timeout=30.0,
                )
            )

            # Verify the test succeeded
            self.assertTrue(success, "MCP client tests should succeed")
        except asyncio.TimeoutError:
            self.fail("MCP client tests timed out after 30 seconds")
        except Exception as e:
            self.fail(f"MCP client tests failed with error: {e}")

        print("MCP client endpoints test completed successfully!")


if __name__ == "__main__":
    unittest.main()

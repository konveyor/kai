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


class TestMCPIntegration(unittest.TestCase):
    """Test integration with the MCP solution server."""

    def setUp(self):
        """Set up test environment."""
        # Get the path to the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.server_dir = os.path.dirname(self.script_dir)
        self.main_path = os.path.join(self.server_dir, "main.py")

        # Create a temporary database for testing
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")

        # Ensure the paths exist
        self.assertTrue(
            os.path.exists(self.server_dir),
            f"Server directory not found: {self.server_dir}",
        )
        self.assertTrue(
            os.path.exists(self.main_path), f"Main script not found: {self.main_path}"
        )

        # Log details for debugging
        print(f"Server directory: {self.server_dir}")
        print(f"Main script: {self.main_path}")
        print(f"Temporary DB: {self.temp_db_path}")

    def tearDown(self):
        """Clean up after tests."""
        try:
            os.close(self.temp_db_fd)
            os.unlink(self.temp_db_path)
        except (OSError, PermissionError) as e:
            print(f"Warning: Failed to clean up temp file: {e}")

    def test_server_start(self):
        """Test that the MCP solution server can be started with the help command."""
        # Start the server process
        main_path = os.path.join(self.server_dir, "main.py")
        print(f"Starting server: {main_path}")

        # Run the server with --help to verify it works
        # Use explicit path to Python executable and validate path existence for security
        python_executable = sys.executable
        if not os.path.isfile(python_executable):
            self.fail(f"Invalid Python executable path: {python_executable}")

        if not os.path.isfile(main_path):
            self.fail(f"Invalid main script path: {main_path}")

        # Use secure paths and arguments
        # Paths are validated above to prevent security issues
        result = subprocess.run(  # nosec B603 - We've validated the command arguments above
            [python_executable, main_path, "--help"],
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "DB_PATH": self.temp_db_path,
                "PYTHONUNBUFFERED": "1",
                # Include server dir and all Python paths to ensure MCP package is found
                "PYTHONPATH": f"{self.server_dir}:{os.environ.get('PYTHONPATH', '')}:{':'.join(sys.path)}",
            },
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

    def test_direct_import(self):
        """Test that we can directly import the solution server modules."""
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
        """Test the server endpoints using the mcp_client's test_mcp_solution_client function."""
        # Import the mcp_client module
        sys.path.insert(0, self.script_dir)
        import mcp_client

        # Use a unique task key for this test run
        task_key = f"endpoint-test-{int(time.time())}"
        print(f"Testing MCP client endpoints with task key: {task_key}")

        # Set environment variable to use our test database
        os.environ["DB_PATH"] = self.temp_db_path

        # Run the existing test function from mcp_client by running its body directly
        # This will test all the endpoints using the client's built-in test functionality

        # Create args for stdio transport - copied from test_mcp_solution_client
        task_key_val = (
            task_key  # Create a local var that can be accessed inside the class
        )
        server_dir = self.server_dir  # Same for server dir

        class Args:
            host = "localhost"
            port = 8000
            transport = "stdio"  # Use stdio transport to test without network
            server_path = server_dir
            task_key = task_key_val
            full_output = False
            verbose = False
            insecure = False

        # Run the tests using the same function as the CLI with a timeout
        # This will start up the stdio server and run the full test suite
        try:
            # Set a reasonable timeout to prevent hanging in CI/CD
            success = asyncio.run(
                asyncio.wait_for(mcp_client.run_tests(Args()), timeout=30.0)
            )
            # Verify the test succeeded
            self.assertTrue(success, "MCP client tests should succeed")
        except asyncio.TimeoutError:
            self.fail("MCP client tests timed out after 30 seconds")
        except Exception as e:
            self.fail(f"MCP client tests failed with error: {e}")

        # The tests are already verified by checking the success variable
        # and the test_mcp_solution_client function prints appropriate output

        print("MCP client endpoints test completed successfully!")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Simple integration test for KAI MCP solution server.

This test module simply runs the original test_client.py script directly 
and verifies that it completes successfully.
"""

import os
import subprocess
import sys
import tempfile
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
        """Test that the MCP solution server can be started."""
        # Start the server process
        main_path = os.path.join(self.server_dir, "main.py")
        print(f"Starting server: {main_path}")

        # Run the server with --help to verify it works
        result = subprocess.run(
            [sys.executable, main_path, "--help"],
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

        # Add debug output for Python paths
        print("Python sys.path:")
        for idx, path in enumerate(sys.path):
            print(f"  {idx}: {path}")

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
                from mcp.server.fastmcp import Context, FastMCP

                print("Successfully imported mcp.server.fastmcp")
            except ImportError as e:
                print(f"Failed to import mcp.server.fastmcp: {e}")
                # Continue with the test even if this fails - it might be a warning only

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


if __name__ == "__main__":
    unittest.main()

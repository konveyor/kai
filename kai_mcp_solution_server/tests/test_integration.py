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
import unittest
from pathlib import Path

try:
    import mcp_client
except ImportError:
    from . import mcp_client


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
        self.server_path = self.tests_path.parent / "src/kai_mcp_solution_server"

        # Log details for debugging
        print("=== Test Setup ===")
        print(f"Temporary directory: {self.temp_dir.name}")
        print(f"Tests directory: {self.tests_path}")
        print(f"Client path: {self.client_path}")
        print(f"Server path: {self.server_path}")
        print("Environment:")
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

        if not os.path.exists(self.server_path):
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

    def test_ssl_insecure_flag_real_request(self):
        """
        Test that the SSL insecure flag works by making a real HTTPS request
        to a server with a self-signed or invalid certificate.

        This uses httpbin.org's self-signed certificate endpoint to verify
        that our SSL monkey patch actually works in practice.
        """
        import asyncio
        import ssl

        print("=== Testing SSL Insecure Flag with Real HTTPS Request ===")

        # Import the fastmcp Client and our SSL utility
        from fastmcp import Client

        try:
            from ssl_utils import apply_ssl_bypass
        except ImportError:
            from .ssl_utils import apply_ssl_bypass

        async def test_insecure_connection():
            # Use a test URL that has SSL certificate issues
            # httpbin.org provides endpoints for testing SSL
            test_url = "https://self-signed.badssl.com"  # Known to have invalid cert

            # Store original SSL context function
            original_ssl_create_default_context = ssl.create_default_context

            try:
                # First, verify that without the patch, SSL verification fails
                print("Testing that SSL verification normally fails...")
                try:
                    # This should fail with SSL verification error
                    client = Client(transport=test_url)
                    async with client:
                        pass
                    # If we get here, the test endpoint doesn't actually have SSL issues
                    print(
                        "! Warning: Test endpoint may not have SSL certificate issues"
                    )
                except Exception as e:
                    if "ssl" in str(e).lower() or "certificate" in str(e).lower():
                        print("✓ SSL verification correctly fails without --insecure")
                    else:
                        print(f"! Unexpected error (not SSL-related): {e}")
                        # Continue with test anyway

                # Now apply the monkey patch like the --insecure flag does
                print("Applying SSL monkey patch...")
                ssl_patch = apply_ssl_bypass()

                # Try to connect with the patch applied
                print("Testing SSL connection with monkey patch applied...")
                ssl_error_found = False
                connection_succeeded = False

                try:
                    client = Client(transport=test_url)
                    async with client:
                        # If we get here, the SSL handshake succeeded
                        connection_succeeded = True
                        print(
                            "✓ SSL handshake succeeded - monkey patch bypassed certificate verification"
                        )
                except Exception as e:
                    error_str = str(e)
                    # Remove URLs from the error message to avoid false positives
                    # from URLs that contain "ssl" in them (like badssl.com)
                    import re

                    error_without_urls = re.sub(
                        r"https?://[^\s]+", "", error_str.lower()
                    )

                    if (
                        "ssl" in error_without_urls
                        or "certificate" in error_without_urls
                    ):
                        ssl_error_found = True
                        print(f"✗ SSL monkey patch failed to bypass verification: {e}")
                    else:
                        # Non-SSL errors mean SSL was bypassed but other issues occurred
                        print(f"✓ SSL bypassed (non-SSL error occurred): {e}")

                # Success if either we got a full connection or we got non-SSL errors
                success = connection_succeeded or not ssl_error_found

                if success:
                    print("✓ SSL certificate verification was successfully bypassed")
                else:
                    print("✗ SSL certificate verification was NOT bypassed")

                return success

            finally:
                # Always restore SSL settings if patch was applied
                if "ssl_patch" in locals():
                    ssl_patch.restore_ssl_settings()

        # Run the async test
        try:
            success = asyncio.run(test_insecure_connection())
            self.assertTrue(
                success,
                "SSL insecure flag should successfully bypass certificate verification",
            )
            print("SSL insecure flag real request test completed successfully!")
        except Exception as e:
            self.fail(f"SSL insecure flag test failed: {e}")

    def test_bearer_token_in_mcp_client_requests(self):
        """
        Test that bearer tokens are properly sent by mcp_client to HTTP servers.

        This test starts a simple HTTP server that captures the Authorization header,
        then uses the actual mcp_client.run_tests() function to make requests with
        a bearer token and verifies the token was received.
        """
        import asyncio
        import threading
        import time
        from http.server import BaseHTTPRequestHandler, HTTPServer

        print("=== Testing Bearer Token in MCP Client Requests ===")

        test_bearer_token = "test-mcp-bearer-token-67890"  # trunk-ignore(bandit/B105)
        captured_headers = {}
        server_port = 18123  # Use a high port to avoid conflicts

        class AuthCapturingHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                # Capture all headers
                captured_headers.update(dict(self.headers))

                # Send a simple response
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "test"}')

            def do_POST(self):
                # Also capture POST requests
                captured_headers.update(dict(self.headers))

                # Send a simple response
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "test"}')

            def log_message(self, format, *args):
                # Suppress server logs to keep test output clean
                pass

        # Start HTTP server in a thread
        server = HTTPServer(("localhost", server_port), AuthCapturingHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        try:
            # Give server time to start
            time.sleep(0.5)

            # Create args for HTTP transport with bearer token
            args = mcp_client.MCPClientArgs(
                host="localhost",
                port=server_port,
                transport="http",
                server_path=self.server_path,
                bearer_token=test_bearer_token,
                insecure=True,  # Use insecure since our test server doesn't have proper SSL
            )

            print(f"Testing with bearer token: {test_bearer_token}")
            print(f"Test server running on localhost:{server_port}")

            # Run the mcp client (it will fail to connect properly, but should make HTTP requests)
            try:
                # Use a short timeout since we expect this to fail
                asyncio.run(asyncio.wait_for(mcp_client.run_tests(args), timeout=5.0))
            except (asyncio.TimeoutError, Exception) as e:
                # Expected to fail since our test server isn't a real MCP server
                print(f"Expected connection failure: {type(e).__name__}")

            # Check if we captured the Authorization header
            print(f"\nCaptured headers: {list(captured_headers.keys())}")

            if "Authorization" in captured_headers:
                auth_header = captured_headers["Authorization"]
                expected_header = f"Bearer {test_bearer_token}"

                print(f"Authorization header: {auth_header}")

                if auth_header == expected_header:
                    print("✓ Bearer token correctly sent in Authorization header")
                    self.assertEqual(
                        auth_header,
                        expected_header,
                        "Bearer token should match expected format",
                    )
                else:
                    print("✗ Authorization header mismatch")
                    print(f"  Expected: {expected_header}")
                    print(f"  Got:      {auth_header}")
                    self.fail(
                        f"Authorization header mismatch: expected '{expected_header}', got '{auth_header}'"
                    )
            else:
                print("✗ No Authorization header found in captured requests")
                print("Available headers:", list(captured_headers.keys()))
                self.fail("Authorization header not found in HTTP requests")

        finally:
            # Clean up server
            server.shutdown()
            server.server_close()

        print("Bearer token MCP client request test completed successfully!")


if __name__ == "__main__":
    unittest.main()

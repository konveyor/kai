#!/usr/bin/env python3
"""
Regression test for https://github.com/konveyor/kai/issues/934.

When the deployed image floated up to a fastmcp major version whose MCP SDK
enables DNS-rebinding protection by default, the streamable-http server started
returning HTTP 421 "Misdirected Request" for every request whose Host header did
not match the bind host (e.g. requests arriving through an nginx ingress with the
external IP as the Host). This broke all editor-extensions @requires-minikube CI.

This test starts the streamable-http transport and sends an ``initialize`` request
with a deliberately mismatched Host/Origin header (mirroring the ingress case in
issue #934). It must NOT come back as 421. The repo's other HTTP tests always
connect with a matching ``localhost`` Host header, so they never exercised this
path.
"""

import os
import socket
import subprocess  # nosec B404 - needed to launch the server like production does
import sys
import tempfile
import time
import unittest
from pathlib import Path

import httpx


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestHostHeaderValidation(unittest.TestCase):
    """The server must not reject proxied requests with a mismatched Host header."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.port = _free_port()

        self.server_path = Path(__file__).parent.parent / "src/kai_mcp_solution_server"

        self.env = {
            **os.environ,
            "KAI_DB_DSN": f"sqlite+aiosqlite:///{self.temp_path}/kai_solution_server.db",
            "KAI_LLM_PARAMS": '{"model": "fake"}',
            "PYTHONUNBUFFERED": "1",
        }

        python_executable = sys.executable
        self.assertTrue(
            os.path.isfile(python_executable),
            f"Invalid Python executable path: {python_executable}",
        )
        self.assertTrue(
            os.path.exists(self.server_path),
            f"Invalid server script path: {self.server_path}",
        )

        # Launch the streamable-http transport exactly as the container does.
        self.proc = subprocess.Popen(  # nosec B603 - args validated above
            [
                python_executable,
                str(self.server_path),
                "--transport",
                "streamable-http",
                "--host",
                "127.0.0.1",
                "--port",
                str(self.port),
                "--mount-path",
                "/",
            ],
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def tearDown(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        try:
            self.temp_dir.cleanup()
        except (OSError, PermissionError) as e:
            print(f"Warning: Failed to clean up after tests: {e}")

    def _wait_until_ready(self, url: str, timeout: float = 30.0) -> None:
        """Poll the endpoint until the server accepts connections (or dies)."""
        body = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 0,
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "readiness-probe", "version": "0.0.0"},
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Host": f"127.0.0.1:{self.port}",
        }
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                out = self.proc.stdout.read() if self.proc.stdout else ""
                self.fail(f"Server exited early (code {self.proc.returncode}):\n{out}")
            try:
                httpx.post(url, json=body, headers=headers, timeout=2.0)
                return
            except httpx.HTTPError:
                time.sleep(0.5)
        self.fail(f"Server did not become ready within {timeout}s")

    def test_mismatched_host_header_is_not_421(self):
        """A request with an ingress-style external Host must not return 421."""
        url = f"http://127.0.0.1:{self.port}/"
        self._wait_until_ready(url)

        body = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1,
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "ingress-test", "version": "0.0.0"},
            },
        }
        # Host/Origin the server never bound to — this is what nginx forwards in
        # the issue #934 repro (the minikube external IP).
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Host": "192.168.49.2",
            "Origin": "https://192.168.49.2",
        }

        response = httpx.post(url, json=body, headers=headers, timeout=10.0)

        self.assertNotEqual(
            response.status_code,
            421,
            "Server returned 421 Misdirected Request for a proxied Host header — "
            "DNS-rebinding protection has regressed (see issue #934). "
            f"Body: {response.text[:500]}",
        )
        # Sanity: the request should actually be handled (initialize succeeds).
        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 for initialize, got {response.status_code}: "
            f"{response.text[:500]}",
        )


if __name__ == "__main__":
    unittest.main()

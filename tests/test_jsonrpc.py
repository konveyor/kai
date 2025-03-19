import asyncio
import subprocess  # trunk-ignore(bandit/B404)
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Literal, cast
from unittest import IsolatedAsyncioTestCase

from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcResponse
from kai.jsonrpc.streams import LspStyleStream
from kai.logging.logging import get_logger


class TestJsonRpc(IsolatedAsyncioTestCase):
    async def test_jsonrpc(self) -> None:
        self.maxDiff = None

        loop = asyncio.get_running_loop()

        print("Starting server")

        # trunk-ignore(bandit/B607)
        # trunk-ignore(bandit/B603)
        server = subprocess.Popen(
            [
                "python",
                Path(f"{__file__}/../test_data/test_jsonrpc/server.py").resolve(),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        print(f"Server started ({server.pid})")

        print("Starting client")
        app = JsonRpcApplication()

        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        @app.add_notify(method="task_notification")
        async def task_notification(
            app: JsonRpcApplication,
            server: JsonRpcServer,
            id: None,
            params: dict[str, Any],
        ) -> None:
            params["method"] = "task_notification"
            await q.put(params)

        @app.add_notify(method="ping")
        async def ping(
            app: JsonRpcApplication,
            server: JsonRpcServer,
            id: None,
            params: dict[str, Any],
        ) -> None:
            params["method"] = "ping"
            await q.put(params)

        rpc = JsonRpcServer(
            json_rpc_stream=LspStyleStream(
                cast(BufferedReader, server.stdout),
                cast(BufferedWriter, server.stdin),
            ),
            app=app,
            request_timeout=4 * 60,
            log=get_logger("kai.analyzer-rpc-client"),
        )

        _ = loop.create_task(rpc.start())
        print("Client started")

        async def send_then_queue(method: str, params: dict[str, Any]) -> None:
            print("send_then_queue")
            result = await rpc.send_request(method, params)
            print(f"  result: {result}")

            if result is None:
                d = {}
            else:
                d = result.model_dump()

            # d["method"] = method

            await q.put(d)

        async def wait_then_spam(duration: float) -> None:
            await asyncio.sleep(duration)
            for i in range(10):
                params = {"value": f"spam {i}"}
                await rpc.send_notification("ping", params)

        loop.create_task(
            send_then_queue(
                method="task",
                params={"duration": 5.0},
            )
        )

        loop.create_task(wait_then_spam(1.5))

        expected: list[dict[str, Any]] = [
            {"method": "task_notification", "id": 0, "value": "start"},
            {"method": "ping", "pong": True, "value": "spam 0"},
            {"method": "ping", "pong": True, "value": "spam 1"},
            {"method": "ping", "pong": True, "value": "spam 2"},
            {"method": "ping", "pong": True, "value": "spam 3"},
            {"method": "ping", "pong": True, "value": "spam 4"},
            {"method": "ping", "pong": True, "value": "spam 5"},
            {"method": "ping", "pong": True, "value": "spam 6"},
            {"method": "ping", "pong": True, "value": "spam 7"},
            {"method": "ping", "pong": True, "value": "spam 8"},
            {"method": "ping", "pong": True, "value": "spam 9"},
            {"method": "task_notification", "id": 0, "value": "end"},
            JsonRpcResponse(
                jsonrpc="2.0",
                result=None,
                error=JsonRpcError(code=-32603, message="No response sent", data=None),
                id=0,
            ).model_dump(),
        ]
        result: list[dict[str, Any]] = []

        try:
            while len(result) != len(expected):
                result.append(await asyncio.wait_for(q.get(), timeout=12.5))
        except TimeoutError:
            print(f"result: {result}")
            print(f"expected: {expected}")
            raise

        self.assertEqual(result, expected)

        server.kill()
        await rpc.stop()

    async def test_cancel(self) -> None:
        self.maxDiff = None

        loop = asyncio.get_running_loop()

        print("Starting server")

        # trunk-ignore(bandit/B607)
        # trunk-ignore(bandit/B603)
        server = subprocess.Popen(
            [
                "python",
                Path(f"{__file__}/../test_data/test_jsonrpc/server.py").resolve(),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        print(f"Server started ({server.pid})")

        print("Starting client")
        app = JsonRpcApplication()

        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        @app.add_notify(method="task_notification")
        async def task_notification(
            app: JsonRpcApplication,
            server: JsonRpcServer,
            id: None,
            params: dict[str, Any],
        ) -> None:
            params["client_method"] = "task_notification"
            await q.put(params)

        rpc = JsonRpcServer(
            json_rpc_stream=LspStyleStream(
                cast(BufferedReader, server.stdout),
                cast(BufferedWriter, server.stdin),
            ),
            app=app,
            request_timeout=4 * 60,
            log=get_logger("kai.analyzer-rpc-client"),
        )

        _ = loop.create_task(rpc.start())
        print("Client started")

        async def wait_send_queue(
            kind: Literal["notify", "request"],
            method: str,
            params: dict[str, Any],
            wait: float = 0.0,
        ) -> None:
            print("send_then_queue")

            await asyncio.sleep(wait)

            if kind == "notify":
                await rpc.send_notification(method, params)
                return

            result = await rpc.send_request(method, params)
            print(f"  result: {result}")

            await q.put({} if result is None else result.model_dump())

        loop.create_task(
            wait_send_queue(
                kind="notify",
                method="long_task.cancel",
                params={},
                wait=0.0,
            )
        )

        loop.create_task(
            wait_send_queue(kind="request", method="long_task", params={}, wait=0.5)
        )

        loop.create_task(
            wait_send_queue(kind="request", method="long_task", params={}, wait=0.75)
        )

        loop.create_task(
            wait_send_queue(
                kind="notify",
                method="long_task.cancel",
                params={},
                wait=3,
            )
        )

        loop.create_task(
            wait_send_queue(
                kind="notify",
                method="long_task.cancel",
                params={},
                wait=4,
            )
        )

        expected: list[dict[str, Any]] = [
            {
                "server_method": "long_task.cancel",
                "long_task_exists": False,
                "client_method": "task_notification",
            },
            {"id": 0, "value": 0, "client_method": "task_notification"},
            {
                "jsonrpc": "2.0",
                "result": None,
                "error": {
                    "code": -32603,
                    "message": "Function long_task already running",
                    "data": None,
                },
                "id": 1,
            },
            {"id": 0, "value": 1, "client_method": "task_notification"},
            {"id": 0, "value": 2, "client_method": "task_notification"},
            {
                "server_method": "long_task.cancel",
                "long_task_exists": True,
                "client_method": "task_notification",
            },
            {
                "server_method": "long_task.cancel",
                "long_task_exists": False,
                "client_method": "task_notification",
            },
        ]
        result: list[dict[str, Any]] = []

        try:
            while len(result) != len(expected):
                result.append(await asyncio.wait_for(q.get(), timeout=12.5))
        except TimeoutError:
            print(f"result: {result}")
            print(f"expected: {expected}")
            raise

        self.assertEqual(result, expected)

        server.kill()
        await rpc.stop()


if __name__ == "__main__":
    # import sys
    # sys.argv.append("-v")
    from unittest import main

    main()

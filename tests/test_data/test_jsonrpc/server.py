import asyncio
import sys
from contextlib import ExitStack
from io import BufferedReader, BufferedWriter
from typing import Any, Optional, cast

from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcId
from kai.jsonrpc.streams import LspStyleStream
from kai.logging import logging


class TestApplication(JsonRpcApplication):
    def __init__(self) -> None:
        super().__init__()

        self.long_task: Optional[asyncio.Task[None]] = None


app = TestApplication()


@app.add_request(method="task")
async def task(
    app: TestApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    await server.send_notification("task_notification", {"id": id, "value": "start"})
    await asyncio.sleep(params["duration"])
    await server.send_notification("task_notification", {"id": id, "value": "end"})
    # await server.send_response(
    #     id=id,
    #     result={"are you kidding me": "no"},
    # )


@app.add_notify(method="ping")
async def ping(
    app: TestApplication,
    server: JsonRpcServer,
    id: None,
    params: dict[str, Any],
) -> None:
    params["pong"] = True
    await server.send_notification("ping", params)


@app.add_notify(method="long_task.cancel")
async def long_task_cancel(
    app: TestApplication, server: JsonRpcServer, id: None, params: dict[str, Any]
) -> None:
    await server.send_notification(
        "task_notification",
        {
            "server_method": "long_task.cancel",
            "long_task_exists": app.long_task is not None,
        },
    )
    if app.long_task is not None:
        app.long_task.cancel()
        app.long_task = None


@app.add_request(method="long_task", sync="error")
async def long_task(
    app: TestApplication, server: JsonRpcServer, id: JsonRpcId, params: dict[str, Any]
) -> None:
    with ExitStack() as defer:
        app.long_task = asyncio.current_task()
        defer.callback(lambda: setattr(app, "long_task", None))

        i = 0
        while True:
            await server.send_notification("task_notification", {"id": id, "value": i})
            i += 1
            await asyncio.sleep(1)


def main() -> None:
    server = JsonRpcServer(
        json_rpc_stream=LspStyleStream(
            cast(BufferedReader, sys.stdin.buffer),
            cast(BufferedWriter, sys.stdout.buffer),
        ),
        app=app,
        log=logging.get_logger("kai-rpc-logger"),
    )

    asyncio.run(server.start(), debug=True)


if __name__ == "__main__":
    main()

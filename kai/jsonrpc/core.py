import asyncio
import time
from typing import Any, Callable, Literal, Optional, overload

from pydantic import BaseModel

from kai.jsonrpc.callbacks import JsonRpcCallback, JsonRpcCoroutine
from kai.jsonrpc.models import (
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcId,
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcResult,
)
from kai.jsonrpc.streams import JsonRpcStream
from kai.logging.logging import TRACE, KaiLogger, get_logger

log = get_logger("jsonrpc")


class JsonRpcApplication:
    """
    Taking a page out of the ASGI standards, JsonRpcApplication is a collection
    of JsonRpcCallbacks that can be used to handle incoming requests and
    notifications.

    Exceptions raised within a call back are handled in JsonRpcCallback.

    NOTE(JonahSussman): We should investigate potentially moving the handling
    here to make it more clear.
    """

    def __init__(
        self,
        request_callbacks: Optional[dict[str, JsonRpcCoroutine]] = None,
        notify_callbacks: Optional[dict[str, JsonRpcCoroutine]] = None,
    ):
        if request_callbacks is None:
            request_callbacks = {}
        if notify_callbacks is None:
            notify_callbacks = {}

        self.request_callbacks = request_callbacks
        self.notify_callbacks = notify_callbacks

    async def handle_request(
        self, request: JsonRpcRequest, server: "JsonRpcServer"
    ) -> None:
        log.log(TRACE, "Handling request: %s", request)

        if request.id is not None:
            log.log(TRACE, "Request is a request")

            if request.method not in self.request_callbacks:
                await server.send_response(
                    id=request.id,
                    error=JsonRpcError(
                        code=JsonRpcErrorCode.MethodNotFound,
                        message=f"Method not found: {request.method}",
                    ),
                )
                return

            log.log(TRACE, "Calling method: %s", request.method)

            await self.request_callbacks[request.method](
                request=request, server=server, app=self
            )

        else:
            log.log(TRACE, "Request is a notification")

            if request.method not in self.notify_callbacks:
                log.error(f"Notify method not found: {request.method}")
                log.error(f"Notify methods: {self.notify_callbacks.keys()}")
                return

            log.log(TRACE, "Calling method: %s", request.method)

            await self.notify_callbacks[request.method](
                request=request, server=server, app=self
            )

    @overload
    def add(
        self,
        func: JsonRpcCoroutine,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add(
        self,
        func: None = ...,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> Callable[[JsonRpcCoroutine], JsonRpcCallback]: ...

    def add(
        self,
        func: JsonRpcCoroutine | None = None,
        *,
        kind: Literal["request", "notify"] = "request",
        method: str | None = None,
        sync: Literal[None, "error", "wait"] = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCoroutine], JsonRpcCallback]:
        if method is None:
            raise ValueError("Method name must be provided")

        def decorator(
            func: JsonRpcCoroutine,
        ) -> JsonRpcCallback:
            callback = JsonRpcCallback(
                func=func,
                kind=kind,
                method=method,
                sync=sync,
            )

            if kind == "request":
                self.request_callbacks[method] = callback
            else:
                self.notify_callbacks[method] = callback

            log.error(f"Added {kind} callback: {method}")

            return callback

        if func:
            return decorator(func)
        else:
            return decorator

    @overload
    def add_notify(
        self,
        func: JsonRpcCoroutine,
        *,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_notify(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> Callable[[JsonRpcCoroutine], JsonRpcCallback]: ...

    def add_notify(
        self,
        func: JsonRpcCoroutine | None = None,
        *,
        method: str | None = None,
        sync: Literal[None, "error", "wait"] = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCoroutine], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="notify",
            method=method,
            sync=sync,
        )

    @overload
    def add_request(
        self,
        func: JsonRpcCoroutine,
        *,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_request(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        sync: Literal[None, "error", "wait"] = ...,
    ) -> Callable[[JsonRpcCoroutine], JsonRpcCallback]: ...

    def add_request(
        self,
        func: JsonRpcCoroutine | None = None,
        *,
        method: str | None = None,
        sync: Literal[None, "error", "wait"] = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCoroutine], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="request",
            method=method,
            sync=sync,
        )

    def generate_docs(self) -> str:
        raise NotImplementedError()


class JsonRpcServer:
    """
    Taking a page from Python's ASGI standards, JsonRpcServer serves a
    JsonRpcApplication. It is a thread that listens for incoming requests and
    notifications on a JsonRpcStream, and handle_requests responses over the
    same stream.

    We separate the two classes to allow one to define routes in different
    files.

    Despite being called "server", you can also use this as a client.
    """

    def __init__(
        self,
        json_rpc_stream: JsonRpcStream,
        app: JsonRpcApplication | None = None,
        request_timeout: float | None = 60.0,
        log: KaiLogger | None = None,
    ) -> None:
        if app is None:
            app = JsonRpcApplication()

        self.jsonrpc_stream: JsonRpcStream = json_rpc_stream

        self.app = app

        self.event_dict: dict[JsonRpcId, asyncio.Event] = {}
        self.response_dict: dict[JsonRpcId, JsonRpcResponse] = {}
        self.next_id = 0
        self.request_timeout = request_timeout
        self.outstanding_requests: dict[JsonRpcId, tuple[JsonRpcRequest, asyncio.Task]] = {}  # type: ignore[type-arg]

        self.shutdown_flag = False
        self.log = get_logger("jsonrpc-server")
        if log is not None:
            self.log = log

    async def stop(self) -> None:
        self.log.info("JsonRpcServer stopping")

        self.shutdown_flag = True

        await self.jsonrpc_stream.close()

    async def start(self) -> None:
        loop = asyncio.get_running_loop()

        self.log.debug("JsonRpcServer started")

        while not self.shutdown_flag:
            self.log.debug("Waiting for message")

            msg = await self.jsonrpc_stream.recv()
            if msg is None:
                self.log.info("Server quit")
                break

            self.log.log(TRACE, f"Received {type(msg)}: {msg}")

            if isinstance(msg, JsonRpcError):
                self.log.error(f"Error during recv: {msg}")

            elif isinstance(msg, JsonRpcRequest):
                task = loop.create_task(
                    self.app.handle_request(msg, self),
                    name=f"{msg.method} {msg.id or -1} {time.time():.2f}",
                )

                if msg.id is not None:
                    self.outstanding_requests[msg.id] = (msg, task)

            elif isinstance(msg, JsonRpcResponse):
                if msg.id is not None:
                    self.response_dict[msg.id] = msg
                    event = self.event_dict[msg.id]
                    event.set()

            else:
                self.log.error(f"Unknown message type: {type(msg)}")

        for request_id in self.outstanding_requests:
            _, task = self.outstanding_requests[request_id]
            task.cancel()
            await self.send_response(
                id=request_id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message="Server shutting down",
                ),
            )

        self.log.debug("No longer waiting for messages, closing stream")
        await self.jsonrpc_stream.close()

        self.log.info("JsonRpcServer stopped")

    async def send_request(
        self, method: str, params: BaseModel | dict[str, Any] | list[Any] | None
    ) -> JsonRpcResponse | JsonRpcError | None:
        if isinstance(params, BaseModel):
            params = params.model_dump()

        self.log.log(TRACE, "Sending request: %s", method)
        current_id = self.next_id
        self.next_id += 1

        event = asyncio.Event()
        self.event_dict[current_id] = event

        await self.jsonrpc_stream.send(
            JsonRpcRequest(method=method, params=params, id=current_id)
        )

        if self.shutdown_flag:
            return None

        try:
            await asyncio.wait_for(event.wait(), timeout=self.request_timeout)
        except asyncio.TimeoutError:
            return JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message="Timeout waiting for response",
            )

        self.event_dict.pop(current_id)

        return self.response_dict.pop(current_id)

    async def send_notification(
        self,
        method: str,
        params: dict[str, Any] | None,
    ) -> None:
        if isinstance(params, BaseModel):
            params = params.model_dump()

        await self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))

    async def send_response(
        self,
        *,
        result: Optional[JsonRpcResult] = None,
        error: Optional[JsonRpcError] = None,
        id: JsonRpcId = None,
    ) -> None:
        response = JsonRpcResponse(result=result, error=error, id=id)

        if response.id is not None:
            if response.id not in self.outstanding_requests:
                self.log.error(
                    f"Request ID {response.id} not found in outstanding requests\nTried sending: {response}"
                )
                return
            del self.outstanding_requests[response.id]

        await self.jsonrpc_stream.send(response)

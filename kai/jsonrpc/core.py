import threading
from typing import Any, Callable, Literal, Optional, overload

from pydantic import BaseModel

from kai.jsonrpc.callbacks import JsonRpcCallable, JsonRpcCallback
from kai.jsonrpc.models import (
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcId,
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcResult,
)
from kai.jsonrpc.streams import JsonRpcStream
from kai.logging.logging import TRACE, get_logger

log = get_logger("jsonrpc")


class JsonRpcApplication:
    """
    Taking a page out of the ASGI standards, JsonRpcApplication is a collection
    of JsonRpcCallbacks that can be used to handle incoming requests and
    notifications.
    """

    def __init__(
        self,
        request_callbacks: Optional[dict[str, JsonRpcCallback]] = None,
        notify_callbacks: Optional[dict[str, JsonRpcCallback]] = None,
    ):
        if request_callbacks is None:
            request_callbacks = {}
        if notify_callbacks is None:
            notify_callbacks = {}

        self.request_callbacks = request_callbacks
        self.notify_callbacks = notify_callbacks

    def handle_request(self, request: JsonRpcRequest, server: "JsonRpcServer") -> None:
        log.log(TRACE, "Handling request: %s", request)

        if request.id is not None:
            log.log(TRACE, "Request is a request")

            if request.method not in self.request_callbacks:
                server.send_response(
                    error=JsonRpcError(
                        code=JsonRpcErrorCode.MethodNotFound,
                        message=f"Method not found: {request.method}",
                    ),
                    id=request.id,
                )
                return

            log.log(TRACE, "Calling method: %s", request.method)

            self.request_callbacks[request.method](
                request=request, server=server, app=self
            )

        else:
            log.log(TRACE, "Request is a notification")

            if request.method not in self.notify_callbacks:
                log.error(f"Notify method not found: {request.method}")
                log.error(f"Notify methods: {self.notify_callbacks.keys()}")
                return

            log.log(TRACE, "Calling method: %s", request.method)

            self.notify_callbacks[request.method](
                request=request, server=server, app=self
            )

    @overload
    def add(
        self,
        func: JsonRpcCallable,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add(
        self,
        func: None = ...,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
    ) -> Callable[[JsonRpcCallable], JsonRpcCallback]: ...

    def add(
        self,
        func: JsonRpcCallable | None = None,
        *,
        kind: Literal["request", "notify"] = "request",
        method: str | None = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCallable], JsonRpcCallback]:
        if method is None:
            raise ValueError("Method name must be provided")

        if kind == "request":
            callbacks = self.request_callbacks
        else:
            callbacks = self.notify_callbacks

        def decorator(
            func: JsonRpcCallable,
        ) -> JsonRpcCallback:
            callback = JsonRpcCallback(
                func=func,
                kind=kind,
                method=method,
            )
            callbacks[method] = callback

            return callback

        if func:
            return decorator(func)
        else:
            return decorator

    @overload
    def add_notify(
        self,
        func: JsonRpcCallable,
        *,
        method: str | None = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_notify(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
    ) -> Callable[[JsonRpcCallable], JsonRpcCallback]: ...

    def add_notify(
        self,
        func: JsonRpcCallable | None = None,
        *,
        method: str | None = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="notify",
            method=method,
        )

    @overload
    def add_request(
        self,
        func: JsonRpcCallable,
        *,
        method: str | None = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_request(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
    ) -> Callable[[JsonRpcCallable], JsonRpcCallback]: ...

    def add_request(
        self,
        func: JsonRpcCallable | None = None,
        *,
        method: str | None = None,
    ) -> JsonRpcCallback | Callable[[JsonRpcCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="request",
            method=method,
        )

    def generate_docs(self) -> str:
        raise NotImplementedError()


class JsonRpcServer(threading.Thread):
    """
    Taking a page from Python's ASGI standards, JsonRpcServer serves a
    JsonRpcApplication. It is a thread that listens for incoming requests and
    notifications on a JsonRpcStream, and sends responses over the same stream.

    We separate the two classes to allow one to define routes in different
    files.

    Despite being called "server", you can also use this as a client.
    """

    def __init__(
        self,
        json_rpc_stream: JsonRpcStream,
        app: JsonRpcApplication | None = None,
        request_timeout: float | None = 60.0,
    ):
        if app is None:
            app = JsonRpcApplication()

        threading.Thread.__init__(self)

        self.jsonrpc_stream = json_rpc_stream
        self.app = app

        self.event_dict: dict[JsonRpcId, threading.Condition] = {}
        self.response_dict: dict[JsonRpcId, JsonRpcResponse] = {}
        self.next_id = 0
        self.request_timeout = request_timeout
        self.outstanding_requests: set[JsonRpcId] = set()

        self.shutdown_flag = False

    def stop(self) -> None:
        self.shutdown_flag = True

    def run(self) -> None:
        log.debug("Server thread started")

        while not self.shutdown_flag:
            log.debug("Waiting for message")
            msg = self.jsonrpc_stream.recv()
            if msg is None:
                log.info("Server quit")
                break

            elif isinstance(msg, JsonRpcError):
                self.jsonrpc_stream.send(JsonRpcResponse(error=msg))
                continue

            elif isinstance(msg, JsonRpcRequest):
                log.log(TRACE, "Received request: %s", msg)
                if msg.id is not None:
                    self.outstanding_requests.add(msg.id)

                self.app.handle_request(msg, self)

                if msg.id is not None and msg.id in self.outstanding_requests:
                    self.send_response(
                        id=msg.id,
                        error=JsonRpcError(
                            code=JsonRpcErrorCode.InternalError,
                            message="No response sent",
                        ),
                    )

            elif isinstance(msg, JsonRpcResponse):
                self.response_dict[msg.id] = msg
                cond = self.event_dict[msg.id]
                cond.acquire()
                cond.notify()
                cond.release()

            else:
                log.error(f"Unknown message type: {type(msg)}")

        self.jsonrpc_stream.close()

    def send_request(
        self, method: str, params: BaseModel | dict[str, Any] | list[Any] | None
    ) -> JsonRpcResponse | JsonRpcError | None:
        if isinstance(params, BaseModel):
            params = params.model_dump()

        log.log(TRACE, "Sending request: %s", method)
        current_id = self.next_id
        self.next_id += 1
        cond = threading.Condition()
        self.event_dict[current_id] = cond

        cond.acquire()
        self.jsonrpc_stream.send(
            JsonRpcRequest(method=method, params=params, id=current_id)
        )

        if self.shutdown_flag:
            cond.release()
            return None

        if not cond.wait(self.request_timeout):
            cond.release()
            return JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message="Timeout waiting for response",
            )
        cond.release()

        self.event_dict.pop(current_id)
        return self.response_dict.pop(current_id)

    def send_notification(
        self,
        method: str,
        params: dict[str, Any] | None,
    ) -> None:
        if isinstance(params, BaseModel):
            params = params.model_dump()

        self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))

    def send_response(
        self,
        *,
        response: Optional[JsonRpcResponse] = None,
        result: Optional[JsonRpcResult] = None,
        error: Optional[JsonRpcError] = None,
        id: JsonRpcId = None,
    ) -> None:
        if response is None:
            response = JsonRpcResponse(result=result, error=error, id=id)

        if response.id is not None:
            if response.id not in self.outstanding_requests:
                log.error(
                    f"Request ID {response.id} not found in outstanding requests\nTried sending: {response}"
                )
                return
            self.outstanding_requests.remove(response.id)

        self.jsonrpc_stream.send(response)

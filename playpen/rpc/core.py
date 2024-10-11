import threading
from typing import Any, Callable, Literal, Optional, overload

from playpen.rpc.callbacks import (
    JsonRpcCallback,
    JsonRpcNotifyCallable,
    JsonRpcRequestCallable,
)
from playpen.rpc.models import (
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcId,
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcResult,
)
from playpen.rpc.streams import JsonRpcStream
from playpen.rpc.util import TRACE, get_logger

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

    def handle_request(
        self, msg: JsonRpcRequest, server: "JsonRpcServer"
    ) -> tuple[JsonRpcResult | None, JsonRpcError | None] | None:
        log.log(TRACE, "Handling request: %s", msg)

        if msg.id is not None:
            log.log(TRACE, "Request is a bona fide request")
            # bona fide request
            if msg.method not in self.request_callbacks:
                return None, JsonRpcError(
                    code=JsonRpcErrorCode.MethodNotFound,
                    message=f"Method not found: {msg.method}",
                )

            log.log(TRACE, "Calling method: %s", msg.method)

            result = self.request_callbacks[msg.method](
                params=msg.params, server=server, app=self
            )

            err = JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message="Method did not return a tuple[JsonRpcResult | None, JsonRpcError | None]",
            )

            if not isinstance(result, tuple) or len(result) != 2:
                return None, err
            # NOTE: If we ever narrow down JsonRpcResult from Any, we should
            # re-enable this check.
            if not isinstance(result[0], (type(None), JsonRpcResult)):
                return None, err
            if not isinstance(result[1], (type(None), JsonRpcError)):
                return None, err

            return result

        else:
            log.log(TRACE, "Request is a notification")

            # notification
            if msg.method not in self.notify_callbacks:
                log.error(f"Notify method not found: {msg.method}")
                return None

            log.log(TRACE, "Calling method: %s", msg.method)

            result = self.notify_callbacks[msg.method](
                params=msg.params, server=server, app=self
            )

            if result is not None:
                return None, JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message="Notification did not return None",
                )

            return None

    @overload
    def add(
        self,
        func: JsonRpcRequestCallable,
        *,
        kind: Literal["request"] = "request",
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add(
        self,
        func: JsonRpcNotifyCallable,
        *,
        kind: Literal["notify"] = "notify",
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add(
        self,
        func: None = ...,
        *,
        kind: Literal["request"] = "request",
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcRequestCallable], JsonRpcCallback]: ...

    @overload
    def add(
        self,
        func: None = ...,
        *,
        kind: Literal["notify"] = "notify",
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcNotifyCallable], JsonRpcCallback]: ...

    def add(
        self,
        func: JsonRpcRequestCallable | JsonRpcNotifyCallable | None = None,
        *,
        kind: Literal["request", "notify"] = "request",
        method: str | None = None,
        params_model: type[JsonRpcResult] | None = None,
        include_server: bool = False,
        include_app: bool = True,
    ) -> (
        JsonRpcCallback
        | Callable[[JsonRpcRequestCallable], JsonRpcCallback]
        | Callable[[JsonRpcNotifyCallable], JsonRpcCallback]
    ):
        if method is None:
            raise ValueError("Method name must be provided")

        if kind == "request":
            callbacks = self.request_callbacks
        else:
            callbacks = self.notify_callbacks

        def decorator(
            func: JsonRpcRequestCallable | JsonRpcNotifyCallable,
        ) -> JsonRpcCallback:
            callback = JsonRpcCallback(
                func=func,
                include_server=include_server,
                include_app=include_app,
                kind=kind,
                method=method,
                params_model=params_model,
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
        func: JsonRpcNotifyCallable,
        *,
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_notify(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcNotifyCallable], JsonRpcCallback]: ...

    def add_notify(
        self,
        func: JsonRpcNotifyCallable | None = None,
        *,
        method: str | None = None,
        params_model: type[JsonRpcResult] | None = None,
        include_server: bool = False,
        include_app: bool = True,
    ) -> JsonRpcCallback | Callable[[JsonRpcNotifyCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="notify",
            method=method,
            params_model=params_model,
            include_server=include_server,
            include_app=include_app,
        )

    @overload
    def add_request(
        self,
        func: JsonRpcRequestCallable,
        *,
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_request(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        params_model: type[JsonRpcResult] | None = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcRequestCallable], JsonRpcCallback]: ...

    def add_request(
        self,
        func: JsonRpcRequestCallable | None = None,
        *,
        method: str | None = None,
        params_model: type[JsonRpcResult] | None = None,
        include_server: bool = False,
        include_app: bool = True,
    ) -> JsonRpcCallback | Callable[[JsonRpcRequestCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="request",
            method=method,
            params_model=params_model,
            include_server=include_server,
            include_app=include_app,
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

        self.shutdown_flag = False

    def stop(self) -> None:
        self.shutdown_flag = True

    def run(self) -> None:
        log.debug("Server thread started")

        while not self.shutdown_flag:
            msg = self.jsonrpc_stream.recv()
            if msg is None:
                log.info("Server quit")
                break

            elif isinstance(msg, JsonRpcError):
                self.jsonrpc_stream.send(JsonRpcResponse(error=msg))
                continue

            elif isinstance(msg, JsonRpcRequest):
                log.log(TRACE, "Received request: %s", msg)
                if (tmp := self.app.handle_request(msg, self)) is not None:
                    result, error = tmp
                    sending_response = JsonRpcResponse(
                        result=result, error=error, id=msg.id
                    )
                    log.log(TRACE, "Sending response: %s", sending_response)
                    self.jsonrpc_stream.send(sending_response)
                    continue

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
        self, method: str, params: dict[str, Any]
    ) -> JsonRpcResponse | JsonRpcError | None:
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

    def send_notification(self, method: str, params: dict[str, Any]) -> None:
        self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))

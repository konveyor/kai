import functools
import json
import logging
import threading
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import IO, Any, Callable, Literal, Optional

from pydantic import BaseModel, ConfigDict, validate_call

log = logging.getLogger(__name__)


class JsonRpcErrorCode(IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerErrorStart = -32099
    ServerErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001


JsonRpcId = Optional[str | int]

JsonRpcResult = Any


class JsonRpcError(BaseModel):
    code: JsonRpcErrorCode | int
    message: str
    data: Optional[Any] = None


class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[JsonRpcResult] = None
    error: Optional[JsonRpcError] = None
    id: JsonRpcId = None


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[dict] = None
    id: JsonRpcId = None


class JsonRpcStream(ABC):
    def __init__(
        self,
        recv_file: IO[bytes],
        send_file: IO[bytes],
        json_dumps_kwargs: Optional[dict] = None,
        json_loads_kwargs: Optional[dict] = None,
    ):
        if json_dumps_kwargs is None:
            json_dumps_kwargs = {}
        if json_loads_kwargs is None:
            json_loads_kwargs = {}

        self.recv_file = recv_file
        self.recv_lock = threading.Lock()

        self.send_file = send_file
        self.send_lock = threading.Lock()

        self.json_dumps_kwargs = json_dumps_kwargs
        self.json_loads_kwargs = json_loads_kwargs

    def close(self):
        self.recv_file.close()
        self.send_file.close()

    @abstractmethod
    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None: ...

    @abstractmethod
    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None: ...


class LspStyleStream(JsonRpcStream):
    JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
    LEN_HEADER = "Content-Length: "
    TYPE_HEADER = "Content-Type: "

    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        json_str = msg.model_dump_json()
        json_req = f"Content-Length: {len(json_str)}\r\n\r\n{json_str}"

        with self.send_lock:
            self.send_file.write(json_req.encode())
            self.send_file.flush()

    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        with self.recv_lock:
            content_length = -1

            while True:
                if self.recv_file.closed:
                    return None

                line_bytes = self.recv_file.readline()
                if not line_bytes:
                    return None

                line = line_bytes.decode("utf-8")
                if not line.endswith("\r\n"):
                    return JsonRpcError(
                        code=JsonRpcErrorCode.ParseError,
                        message="Bad header: missing newline",
                    )

                line = line[:-2]

                if line == "":
                    break
                elif line.startswith(self.LEN_HEADER):
                    line = line[len(self.LEN_HEADER) :]
                    if not line.isdigit():
                        return JsonRpcError(
                            code=JsonRpcErrorCode.ParseError,
                            message="Bad header: size is not int",
                        )
                    content_length = int(line)
                elif line.startswith(self.TYPE_HEADER):
                    pass
                else:
                    return JsonRpcError(
                        code=JsonRpcErrorCode.ParseError,
                        message=f"Bad header: unknown header {line}",
                    )

            if content_length < 0:
                return JsonRpcError(
                    code=JsonRpcErrorCode.ParseError,
                    message="Bad header: missing Content-Length",
                )

            try:
                msg_str = self.recv_file.read(content_length).decode("utf-8")
                msg_dict = json.loads(msg_str, **self.json_loads_kwargs)
            except Exception as e:
                return JsonRpcError(
                    code=JsonRpcErrorCode.ParseError,
                    message=f"Invalid JSON: {e}",
                )

            try:
                if "method" in msg_dict:
                    return JsonRpcRequest.model_validate(msg_dict)
                else:
                    return JsonRpcResponse.model_validate(msg_dict)
            except Exception as e:
                return JsonRpcError(
                    code=JsonRpcErrorCode.ParseError,
                    message=f"Could not validate JSON: {e}",
                )


JsonRpcMethodCallable = Callable[..., tuple[JsonRpcResult | None, JsonRpcError | None]]
JsonRpcNotifyCallable = Callable[..., None]


class JsonRpcCallback:
    def __init__(
        self,
        func: JsonRpcMethodCallable | JsonRpcNotifyCallable,
        extract_params: bool,
        include_server: bool,
        include_app: bool,
    ):
        self.func = func
        self.extract_params = extract_params
        self.include_server = include_server
        self.include_app = include_app

        @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
        @functools.wraps(self.func)
        def validate_func_args(*args, **kwargs):
            return args, kwargs

        self.validate_func_args = validate_func_args

    def __call__(
        self,
        params: dict | None,
        server: Optional["JsonRpcServer"],
        app: Optional["JsonRpcApplication"],
    ) -> tuple[JsonRpcResult | None, JsonRpcError | None] | None:
        if params is None:
            params = {}

        kwargs = params if self.extract_params else {"params": params}

        if self.include_server:
            kwargs["server"] = server
        if self.include_app:
            kwargs["app"] = app

        try:
            self.validate_func_args(**kwargs)
            return self.func(**kwargs)
        except Exception as e:
            return None, JsonRpcError(
                code=JsonRpcErrorCode.InvalidParams,
                message=f"Invalid parameters: {e}",
            )


class JsonRpcApplication:
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
        if msg.id is not None:
            # bona fide request
            if msg.method not in self.request_callbacks:
                return None, JsonRpcError(
                    code=JsonRpcErrorCode.MethodNotFound,
                    message=f"Method not found: {msg.method}",
                )

            return self.request_callbacks[msg.method](
                params=msg.params, server=server, app=self
            )
        else:
            # notification
            if msg.method not in self.notify_callbacks:
                log.error(f"Notify method not found: {msg.method}")
                return None

            self.notify_callbacks[msg.method](
                params=msg.params, server=server, app=self
            )
            return None

    def add(
        self,
        func: JsonRpcMethodCallable | JsonRpcNotifyCallable | None = None,
        *,
        kind: Literal["request", "notify"] = "request",
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_self: bool = True,
    ):
        if method is None:
            raise ValueError("Method name must be provided")

        if kind == "request":
            callbacks = self.request_callbacks
        else:
            callbacks = self.notify_callbacks

        def decorator(func: JsonRpcMethodCallable | JsonRpcNotifyCallable):
            callback = JsonRpcCallback(
                func, extract_params, include_server, include_self
            )
            callbacks[method] = callback

            return callback

        if func:
            return decorator(func)
        else:
            return decorator

    def add_notify(
        self,
        func: JsonRpcNotifyCallable | None = None,
        *,
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_self: bool = True,
    ):
        return self.add(
            func=func,
            kind="notify",
            method=method,
            extract_params=extract_params,
            include_server=include_server,
            include_self=include_self,
        )

    def add_request(
        self,
        func: JsonRpcMethodCallable | None = None,
        *,
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_self: bool = True,
    ):
        return self.add(
            func=func,
            kind="request",
            method=method,
            extract_params=extract_params,
            include_server=include_server,
            include_self=include_self,
        )

    def generate_docs(self):
        raise NotImplementedError()


class JsonRpcServer(threading.Thread):
    def __init__(
        self,
        json_rpc_stream: JsonRpcStream,
        app: JsonRpcApplication | None = None,
        request_timeout: float = 60.0,
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

    def run(self):
        while not self.shutdown_flag:
            msg = self.jsonrpc_stream.recv()
            if msg is None:
                log.info("Server quit")
                break

            elif isinstance(msg, JsonRpcError):
                self.jsonrpc_stream.send(JsonRpcResponse(error=msg))
                continue

            elif isinstance(msg, JsonRpcRequest):
                if (tmp := self.app.handle_request(msg, self)) is not None:
                    result, error = tmp
                    self.jsonrpc_stream.send(
                        JsonRpcResponse(result=result, error=error, id=msg.id)
                    )
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

    def send_request(self, method: str, **params):
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

    def send_notification(self, method: str, **params):
        self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))


class JsonRpcLoggingHandler(logging.Handler):
    def __init__(self, server: JsonRpcServer, method: str = "logMessage"):
        logging.Handler.__init__(self)
        self.server = server
        self.method = method

    def emit(self, record: logging.LogRecord):
        try:
            self.server.send_notification(
                self.method,
                level=record.levelname,
                message=record.getMessage(),
            )
        except Exception:
            self.server.send_notification(
                self.method,
                level="ERROR",
                message="Failed to log message",
            )
            self.handleError(record)

import functools
import json
import logging
import sys
import threading
from abc import ABC, abstractmethod
from enum import IntEnum
from io import BufferedReader, BufferedWriter
from typing import Any, Callable, Literal, Optional, overload

from pydantic import BaseModel, ConfigDict, validate_call

TRACE = logging.DEBUG - 5
DEFAULT_FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_logger(
    name: str,
    stderr_level: int | str = "TRACE",
    formatter: logging.Formatter = DEFAULT_FORMATTER,
) -> logging.Logger:
    logging.addLevelName(logging.DEBUG - 5, "TRACE")

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(TRACE)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(stderr_level)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    return logger


def log_record_to_dict(record: logging.LogRecord) -> dict[str, Any]:
    return {
        "name": record.name,
        "levelno": record.levelno,
        "levelname": record.levelname,
        "pathname": record.pathname,
        "filename": record.filename,
        "module": record.module,
        "lineno": record.lineno,
        "funcName": record.funcName,
        "created": record.created,
        "asctime": record.asctime,
        "msecs": record.msecs,
        "relativeCreated": record.relativeCreated,
        "thread": record.thread,
        "threadName": record.threadName,
        "process": record.process,
        "msg": record.msg,
        "args": record.args,
        "message": record.getMessage(),
    }


log = get_logger("jsonrpc")


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
    """
    And abstract base class for a JSON-RPC stream. This class is used to
    communicate with the JSON-RPC server and client.
    """

    def __init__(
        self,
        recv_file: BufferedReader,
        send_file: BufferedWriter,
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

    def close(self) -> None:
        self.recv_file.close()
        self.send_file.close()

    @abstractmethod
    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None: ...

    @abstractmethod
    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None: ...


class LspStyleStream(JsonRpcStream):
    """
    Standard LSP-style stream for JSON-RPC communication. This uses HTTP-style
    headers for content length and content type.
    """

    JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
    LEN_HEADER = "Content-Length: "
    TYPE_HEADER = "Content-Type: "

    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        json_str = msg.model_dump_json()
        json_req = f"Content-Length: {len(json_str)}\r\n\r\n{json_str}"

        # Prevent infinite recursion
        if isinstance(msg, JsonRpcRequest) and msg.method != "logMessage":
            log.log(TRACE, "Sending request: %s", json_req)

        with self.send_lock:
            self.send_file.write(json_req.encode())
            self.send_file.flush()

    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        log.debug("Waiting for message")

        with self.recv_lock:
            log.log(TRACE, "Reading headers")
            content_length = -1

            while True:
                if self.recv_file.closed:
                    return None

                log.log(TRACE, "Reading header line")
                line_bytes = self.recv_file.readline()

                log.log(TRACE, "Read header line: %s", line_bytes)
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

            log.log(TRACE, "Got message with content length: %s", content_length)

            try:
                msg_str = self.recv_file.read(content_length).decode("utf-8")
                msg_dict = json.loads(msg_str, **self.json_loads_kwargs)
            except Exception as e:
                return JsonRpcError(
                    code=JsonRpcErrorCode.ParseError,
                    message=f"Invalid JSON: {e}",
                )

            log.log(TRACE, "Got message: %s", msg_dict)

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


class BareJsonStream(JsonRpcStream):
    def __init__(
        self,
        recv_file: BufferedReader,
        send_file: BufferedWriter,
        json_dumps_kwargs: dict | None = None,
        json_loads_kwargs: dict | None = None,
    ):
        super().__init__(recv_file, send_file, json_dumps_kwargs, json_loads_kwargs)

        self.buffer: str = ""
        self.decoder = json.JSONDecoder()
        self.chunk_size = 512

    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        json_req = msg.model_dump_json()

        # Prevent infinite recursion
        if not isinstance(msg, JsonRpcRequest) or msg.method != "logMessage":
            log.log(TRACE, "send: %s", json_req)
        else:
            log_msg = msg.model_copy()
            if log_msg.params is None:
                log_msg.params = {}
            if "message" in log_msg.params:
                log_msg.params["message"] = "<omitted>"
            log.log(TRACE, f"send: {log_msg.model_dump_json()}")

        with self.send_lock:
            self.send_file.write(json_req.encode())
            self.send_file.flush()

    def get_from_buffer(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        try:
            msg, idx = self.decoder.raw_decode(self.buffer)
            self.buffer = self.buffer[idx:]

            log.log(TRACE, "recv msg: %s", msg)
            log.log(TRACE, "recv buffer: %s", self.buffer)

            if "method" in msg:
                return JsonRpcRequest.model_validate(msg)
            else:
                return JsonRpcResponse.model_validate(msg)
        except json.JSONDecodeError:
            return None
        except Exception as e:
            return JsonRpcError(
                code=JsonRpcErrorCode.ParseError,
                message=f"Invalid JSON: {e}",
            )

    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        with self.recv_lock:
            result = self.get_from_buffer()
            if result is not None:
                return result

            while chunk := self.recv_file.read1(self.chunk_size):
                self.buffer += chunk.decode("utf-8")
                log.log(TRACE, "recv buffer: %s", self.buffer)

                result = self.get_from_buffer()
                if result is not None:
                    return result

        return None


JsonRpcRequestResult = tuple[JsonRpcResult | None, JsonRpcError | None]

JsonRpcRequestCallable = Callable[..., JsonRpcRequestResult]
JsonRpcNotifyCallable = Callable[..., None]


class JsonRpcCallback:
    """
    A JsonRpcCallback is a wrapper around a JsonRpcMethodCallable or
    JsonRpcNotifyCallable. It validates the parameters and calls the function.

    We use this class to allow for more flexibility in the parameters that can
    be passed to the function.
    """

    def __init__(
        self,
        func: JsonRpcRequestCallable | JsonRpcNotifyCallable,
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
        def validate_func_args(
            *args: Any, **kwargs: Any
        ) -> tuple[tuple[Any, ...], dict[str, Any]]:
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
            # if not isinstance(result[0], (type(None), JsonRpcResult)):
            #     return None, err
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
        func: JsonRpcRequestCallable | JsonRpcNotifyCallable,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add(
        self,
        func: None = ...,
        *,
        kind: Literal["request", "notify"] = ...,
        method: str | None = ...,
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[
        [JsonRpcRequestCallable | JsonRpcNotifyCallable], JsonRpcCallback
    ]: ...

    def add(
        self,
        func: JsonRpcRequestCallable | JsonRpcNotifyCallable | None = None,
        *,
        kind: Literal["request", "notify"] = "request",
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_app: bool = True,
    ) -> (
        JsonRpcCallback
        | Callable[[JsonRpcRequestCallable | JsonRpcNotifyCallable], JsonRpcCallback]
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
                func, extract_params, include_server, include_app
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
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_notify(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcNotifyCallable], JsonRpcCallback]: ...

    def add_notify(
        self,
        func: JsonRpcNotifyCallable | None = None,
        *,
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_app: bool = True,
    ) -> JsonRpcCallback | Callable[[JsonRpcNotifyCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="notify",
            method=method,
            extract_params=extract_params,
            include_server=include_server,
            include_app=include_app,
        )

    @overload
    def add_request(
        self,
        func: JsonRpcRequestCallable,
        *,
        method: str | None = ...,
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> JsonRpcCallback: ...

    @overload
    def add_request(
        self,
        func: None = ...,
        *,
        method: str | None = ...,
        extract_params: bool = ...,
        include_server: bool = ...,
        include_app: bool = ...,
    ) -> Callable[[JsonRpcRequestCallable], JsonRpcCallback]: ...

    def add_request(
        self,
        func: JsonRpcRequestCallable | None = None,
        *,
        method: str | None = None,
        extract_params: bool = True,
        include_server: bool = False,
        include_app: bool = True,
    ) -> JsonRpcCallback | Callable[[JsonRpcRequestCallable], JsonRpcCallback]:
        return self.add(
            func=func,
            kind="request",
            method=method,
            extract_params=extract_params,
            include_server=include_server,
            include_app=include_app,
        )

    def generate_docs(self) -> None:
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
                    log.log(TRACE, "Sending response: %s", tmp)
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

    def send_request(
        self, method: str, **params: Any
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

    def send_notification(self, method: str, **params: Any) -> None:
        self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))


class JsonRpcLoggingHandler(logging.Handler):
    def __init__(self, server: JsonRpcServer, method: str = "logMessage"):
        logging.Handler.__init__(self)
        self.server = server
        self.method = method

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.server.send_notification(
                self.method,
                name=record.name,
                levelno=record.levelno,
                levelname=record.levelname,
                pathname=record.pathname,
                filename=record.filename,
                module=record.module,
                lineno=record.lineno,
                funcName=record.funcName,
                created=record.created,
                asctime=record.asctime,
                msecs=record.msecs,
                relativeCreated=record.relativeCreated,
                thread=record.thread,
                threadName=record.threadName,
                process=record.process,
                message=record.getMessage(),
            )
        except Exception:
            print("Failed to log message", file=sys.stderr)
            # self.server.send_notification(
            #     self.method,
            #     level="ERROR",
            #     message="Failed to log message",
            # )
            self.handleError(record)

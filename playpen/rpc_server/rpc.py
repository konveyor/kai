import functools
import json
import logging
import threading
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any, BinaryIO, Callable, Optional

from pydantic import BaseModel, validate_call

log = logging.getLogger(__name__)


class JsonRpcErrorCode(IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    serverErrorStart = -32099
    serverErrorEnd = -32000
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
        recv_file: BinaryIO,
        send_file: BinaryIO,
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
                line = self.recv_file.readline()
                if not line:
                    return None

                line = line.decode("utf-8")
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


JsonRpcMethodCallback = Callable[..., tuple[JsonRpcResult | None, JsonRpcError | None]]
JsonRpcNotifyCallback = Callable[..., None]


# NOTE: Maybe we should have a separation between server and application a la
# asgi? The server would be responsible for handling the stream and the
# application would be responsible for handling the methods and notifications.
class JsonRpcServer(threading.Thread):
    def __init__(
        self,
        json_rpc_stream: JsonRpcStream,
        method_callbacks: Optional[dict[str, JsonRpcMethodCallback]] = None,
        notify_callbacks: Optional[dict[str, JsonRpcNotifyCallback]] = None,
        timeout: float = 60.0,
    ):
        if method_callbacks is None:
            method_callbacks = {}
        if notify_callbacks is None:
            notify_callbacks = {}

        threading.Thread.__init__(self)

        self.jsonrpc_stream = json_rpc_stream
        self.method_callbacks = method_callbacks
        self.notify_callbacks = notify_callbacks

        self.event_dict: dict[JsonRpcId, threading.Condition] = {}
        self.response_dict: dict[JsonRpcId, JsonRpcResponse] = {}
        self.next_id = 0
        self.timeout = timeout
        self.shutdown_flag = False

    def add_method(
        self,
        func: JsonRpcMethodCallback | None = None,
        /,
        *,
        method: str | None = None,
        model: type[BaseModel] | None = None,
    ):
        return self.__add_callback(
            func=func,
            method=method,
            model=model,
            callbacks=self.method_callbacks,
        )

    def add_notify(
        self,
        func: JsonRpcNotifyCallback | None = None,
        /,
        *,
        method: str | None = None,
        model: type[BaseModel] | None = None,
    ):
        return self.__add_callback(
            func=func,
            method=method,
            model=model,
            callbacks=self.notify_callbacks,
        )

    def __add_callback(
        self,
        /,
        func: JsonRpcNotifyCallback | None = None,
        *,
        method: str | None = None,
        model: type[BaseModel] | None = None,
        callbacks: dict[str, JsonRpcMethodCallback | JsonRpcNotifyCallback],
    ):
        if method is None:
            raise ValueError("Method name must be provided")

        def decorator(func: JsonRpcMethodCallback):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    if model is None:

                        @validate_call
                        @functools.wraps(func)
                        def validate_func_args(*args, **kwargs):
                            return args, kwargs

                        validate_func_args(*args, **kwargs)
                    else:
                        model.model_validate(*args, **kwargs)

                except Exception as e:
                    return None, JsonRpcError(
                        code=JsonRpcErrorCode.InvalidParams,
                        message=f"Invalid parameters: {e}",
                    )

                return func(*args, **kwargs)

            callbacks[method] = wrapper

            return wrapper

        if func:
            return decorator(func)
        else:
            return decorator

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
                if msg.id is not None:
                    # bona fide request
                    if msg.method not in self.method_callbacks:
                        error = JsonRpcError(
                            code=JsonRpcErrorCode.MethodNotFound,
                            message=f"Method not found: {msg.method}",
                        )
                        self.jsonrpc_stream.send(
                            JsonRpcResponse(error=error, id=msg.id)
                        )
                        continue

                    params = msg.params or {}
                    result, error = self.method_callbacks[msg.method](**params)
                    self.jsonrpc_stream.send(
                        JsonRpcResponse(result=result, error=error, id=msg.id)
                    )
                else:
                    if msg.method not in self.notify_callbacks:
                        log.error(f"Notify method not found: {msg.method}")
                        continue

                    params = msg.params or {}
                    self.notify_callbacks[msg.method](**params)

            elif isinstance(msg, JsonRpcResponse):
                self.response_dict[msg.id] = msg
                cond = self.event_dict[msg.id]
                cond.acquire()
                cond.notify()
                cond.release()

            else:
                log.error(f"Unknown message type: {type(msg)}")

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

        if not cond.wait(self.timeout):
            cond.release()
            return JsonRpcError(
                code=JsonRpcErrorCode.InternalError,
                message="Timeout waiting for response",
            )
        cond.release()

        self.event_dict.pop(current_id)
        response = self.response_dict.pop(current_id)
        if response.error:
            return response.error
        return response.result

    def send_notification(self, method: str, **params):
        self.jsonrpc_stream.send(JsonRpcRequest(method=method, params=params))

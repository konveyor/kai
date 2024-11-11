import json
import threading
from abc import ABC, abstractmethod
from concurrent import futures
from concurrent.futures import CancelledError
from io import BufferedReader, BufferedWriter
from typing import Any, Optional

from pydantic import BaseModel

from kai.jsonrpc.models import (
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcRequest,
    JsonRpcResponse,
)
from kai.logging.logging import TRACE, KaiLogger, get_logger

log = get_logger("jsonrpc")


class JsonRpcStream(ABC):
    """
    And abstract base class for a JSON-RPC stream. This class is used to
    communicate with the JSON-RPC server and client.
    """

    def __init__(
        self,
        recv_file: BufferedReader,
        send_file: BufferedWriter,
        json_dumps_kwargs: Optional[dict[Any, Any]] = None,
        json_loads_kwargs: Optional[dict[Any, Any]] = None,
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

    def close(self) -> None:  # trunk-ignore(ruff/B027)
        pass
        # The only thing that this has is the pipes for std in and std out
        # but the recv() methods have blocking I/O on readline
        # because of this we can not close the PIPEs because the read lock
        # stays open forever, and we have a deadlock.
        # We may be able in the future to rewrite readline with a non blocking i/o
        # by keeping a pointer to the last read index, seeking past that index to see if
        # more data is in the pipe and when it is, to seek til we get the new line
        # then read that many bytes.
        # For now, the thread approach works, because we terminate the server command
        # which will close the streams, sending a EOF, and that stops readline.

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
        json_dumps_kwargs: dict[Any, Any] | None = None,
        json_loads_kwargs: dict[Any, Any] | None = None,
        log: KaiLogger | None = None,
    ):
        super().__init__(recv_file, send_file, json_dumps_kwargs, json_loads_kwargs)

        self.buffer: str = ""
        self.decoder = json.JSONDecoder()
        self.chunk_size = 512
        self.log = get_logger("jsonrpc")
        if log is not None:
            self.log = log

    def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        json_req = f"{msg.model_dump_json()}\n"

        # Prevent infinite recursion
        if not isinstance(msg, JsonRpcRequest) or msg.method != "logMessage":
            self.log.log(TRACE, "send: %s", json_req)
        else:
            log_msg = msg.model_copy()
            if log_msg.params is None:
                log_msg.params = {}
            elif isinstance(log_msg.params, dict):
                if "message" in log_msg.params:
                    log_msg.params["message"] = "<omitted>"
            elif isinstance(log_msg.params, BaseModel):
                if hasattr(log_msg.params, "message"):
                    log_msg.params.message = "<omitted>"

            self.log.log(TRACE, f"send: {log_msg.model_dump_json()}")

        with self.send_lock:
            self.send_file.write(json_req.encode())
            self.send_file.flush()

    def readline(self) -> bytes | None:
        try:
            return self.recv_file.readline()
        except CancelledError:
            self.log.info("cancelling readline")
            raise

    def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        with self.recv_lock:
            if self.recv_file.closed:
                return None

            with futures.ThreadPoolExecutor(1, "readline") as executor:
                self.readline_task = executor.submit(self.readline)

                try:
                    result = self.readline_task.result()
                    # EOF
                    if not result:
                        return None

                    msg, idx = self.decoder.raw_decode(result.decode("utf-8"))
                    self.log.log(TRACE, "recv msg: %s", msg)
                    if "method" in msg:
                        return JsonRpcRequest.model_validate(msg)
                    else:
                        return JsonRpcResponse.model_validate(msg)
                except json.JSONDecodeError as e:
                    return JsonRpcError(
                        code=JsonRpcErrorCode.ParseError,
                        message=f"Invalid JSON: {e}",
                    )
                except Exception as e:
                    return JsonRpcError(
                        code=JsonRpcErrorCode.ParseError,
                        message=f"Unknown parsing error: {e}",
                    )
                except CancelledError:
                    return None

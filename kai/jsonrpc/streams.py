import asyncio
import json
import logging
from abc import ABC, abstractmethod
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
from kai.logging.logging import TRACE, get_logger

log = get_logger("jsonrpc")


class JsonRpcStream(ABC):
    """
    And abstract base class for a JSON-RPC stream. This class is used to
    communicate with the JSON-RPC server and client.
    """

    recv_file: BufferedReader
    send_file: BufferedWriter

    recv_lock: asyncio.Lock
    send_lock: asyncio.Lock

    json_dumps_kwargs: dict[Any, Any]
    json_loads_kwargs: dict[Any, Any]

    _writer: asyncio.StreamWriter | None
    _reader: asyncio.StreamReader | None

    loop: asyncio.AbstractEventLoop

    def __init__(
        self,
        recv_file: BufferedReader,
        send_file: BufferedWriter,
        json_dumps_kwargs: Optional[dict[Any, Any]] = None,
        json_loads_kwargs: Optional[dict[Any, Any]] = None,
        *,
        log: logging.Logger | None = None,
    ) -> None:
        if json_dumps_kwargs is None:
            json_dumps_kwargs = {}
        if json_loads_kwargs is None:
            json_loads_kwargs = {}

        self.recv_file = recv_file
        self.recv_lock = asyncio.Lock()  # NOTE(JonahSussman): Might not need?

        self.send_file = send_file
        self.send_lock = asyncio.Lock()  # NOTE(JonahSussman): Might not need?

        self.json_dumps_kwargs = json_dumps_kwargs
        self.json_loads_kwargs = json_loads_kwargs

        self._reader = None
        self._writer = None

        self.log = log or get_logger("jsonrpc")

    async def close(self) -> None:
        if self._reader is not None and not self._reader.at_eof():
            self._reader.feed_eof()

        if self._writer is not None and not self._writer.is_closing():
            self._writer.close()

    async def get_reader(self) -> asyncio.StreamReader:
        loop = asyncio.get_running_loop()

        if self._reader is not None:
            return self._reader

        reader = asyncio.StreamReader(loop=loop)
        read_transport, read_protocol = await loop.connect_read_pipe(
            lambda: asyncio.StreamReaderProtocol(reader, loop=loop), self.recv_file
        )

        self._reader = reader
        return self._reader

    async def get_writer(self) -> asyncio.StreamWriter:
        loop = asyncio.get_running_loop()

        if self._writer is not None:
            return self._writer

        write_transport, write_protocol = await loop.connect_write_pipe(
            lambda: asyncio.streams.FlowControlMixin(loop=loop), self.send_file
        )
        writer = asyncio.StreamWriter(write_transport, write_protocol, None, loop)

        self._writer = writer
        return self._writer

    @abstractmethod
    async def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None: ...

    @abstractmethod
    async def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None: ...


def dump_json_no_infinite_recursion(msg: JsonRpcRequest | JsonRpcResponse) -> str:
    if not isinstance(msg, JsonRpcRequest) or msg.method != "logMessage":
        # exclude_none = True because `None` serializes as `null`, which is not
        # the same thing as `undefined` in JS
        return msg.model_dump_json(exclude_none=True)
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

        return log_msg.model_dump_json(exclude_none=True)


class LspStyleStream(JsonRpcStream):
    """
    Standard LSP-style stream for JSON-RPC communication. This uses HTTP-style
    headers for content length and content type.
    """

    JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
    LEN_HEADER = "Content-Length: "
    TYPE_HEADER = "Content-Type: "

    async def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        writer = await self.get_writer()

        json_str = msg.model_dump_json(exclude_none=True)
        json_req = f"Content-Length: {len(json_str.encode('utf-8'))}\r\n\r\n{json_str}"

        if not writer.is_closing():
            log.log(TRACE, "Sending request: %s", dump_json_no_infinite_recursion(msg))

            writer.write(json_req.encode("utf-8"))
            await writer.drain()
        else:
            log.error("Writer is closed or closing, cannot send message")

    async def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        reader = await self.get_reader()

        log.debug("Waiting for message")

        content_length = -1

        while True:
            if reader.at_eof():
                return None

            log.log(TRACE, "Reading header line")
            line_bytes = await reader.readline()

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
            msg_str = (await reader.read(content_length)).decode("utf-8")
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
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.buffer: str = ""
        self.decoder = json.JSONDecoder()
        self.chunk_size = 512

    async def send(self, msg: JsonRpcRequest | JsonRpcResponse) -> None:
        writer = await self.get_writer()

        json_req = f"{msg.model_dump_json(exclude_none=True)}\n"

        if not writer.is_closing():
            log.log(TRACE, "Sending request: %s", dump_json_no_infinite_recursion(msg))

            writer.write(json_req.encode("utf-8"))
            # TODO(JonahSussman): Do we need this? If you drain a closed stream,
            # you get an exception.
            # await writer.drain()
        else:
            log.error("Writer is closed or closing, cannot send message")

    async def unlimited_readline(self, reader: asyncio.StreamReader) -> bytes:
        result = b""

        while True:
            try:
                result += await reader.readuntil(b"\n")
                break

            # except asyncio.IncompleteReadError as e:
            #     result += e.partial
            #     return result

            except asyncio.LimitOverrunError as e:
                chunk = await reader.readexactly(e.consumed)
                result += chunk

        return result

    async def recv(self) -> JsonRpcError | JsonRpcRequest | JsonRpcResponse | None:
        reader = await self.get_reader()

        if reader.at_eof():
            return None

        try:
            result = await self.unlimited_readline(reader)
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

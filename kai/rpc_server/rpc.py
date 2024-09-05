"""
Port of the `pylspclient` rpc library with bugfixes and improvements.
"""

import json
import logging
import logging.handlers
import threading
from enum import IntEnum
from typing import IO, Any, Callable, Optional

from pydantic import BaseModel

logger = logging.getLogger("kai_rpc")
logger.setLevel(logging.NOTSET)


JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
LEN_HEADER = b"Content-Length: "
TYPE_HEADER = b"Content-Type: "


class ErrorCodes(IntEnum):
    # Defined by JSON RPC
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    serverErrorStart = -32099
    serverErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

    # Defined by the protocol.
    RequestCancelled = -32800
    ContentModified = -32801


class ResponseError(Exception):
    def __init__(self, code: ErrorCodes, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        if data:
            self.data = data


class MyEncoder(json.JSONEncoder):
    """
    Encodes an object in JSON
    """

    def default(self, o):  # pylint: disable=E0202
        return o.__dict__


class RpcMessageError(BaseModel):
    code: ErrorCodes
    message: str
    data: Optional[Any] = None


class RpcMessage(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[Any] = None
    result: Optional[Any] = None
    error: Optional[RpcMessageError] = None


class RpcEndpoint:
    """
    Thread safe JSON RPC endpoint implementation. Responsible to receive and
    send JSON RPC messages, as described in the protocol. More information can
    be found: https://www.jsonrpc.org/
    """

    def __init__(self, io_send: IO[bytes], io_recv: IO[bytes]):
        self.io_send = io_send
        self.io_recv = io_recv
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    @staticmethod
    def __add_header(json_string):
        """
        Adds a header for the given json string

        :param str json_string: The string
        :return: the string with the header
        """
        return JSON_RPC_REQ_FORMAT.format(
            json_string_len=len(json_string), json_string=json_string
        )

    def send_request(self, message):
        """
        Sends the given message.

        :param dict message: The message to send.
        """
        json_string = json.dumps(message, cls=MyEncoder)
        jsonrpc_req = self.__add_header(json_string).encode("utf-8")

        logger.debug(f"Sending data over {self.io_send} {jsonrpc_req}")

        with self.write_lock:
            logger.debug(f"writing {repr(jsonrpc_req)}")

            self.io_send.write(jsonrpc_req)
            self.io_send.flush()

    def recv_response(self):
        """
        Receives a message.

        :return: a message
        """
        with self.read_lock:
            message_size = None
            while True:
                # read header
                line: bytes = self.io_recv.readline()

                logger.debug(f"Received data over {self.io_recv} {repr(line)}")

                if not line:
                    return None  # server quit

                if not line.endswith(b"\r\n"):
                    raise ResponseError(
                        ErrorCodes.ParseError,
                        f"Bad header: missing newline. Received: {line}",
                    )
                # remove the "\r\n"
                line = line[:-2]
                if line == b"":
                    # done with the headers
                    break
                elif line.startswith(LEN_HEADER):
                    line = line[len(LEN_HEADER) :]
                    if not line.isdigit():
                        raise ResponseError(
                            ErrorCodes.ParseError, "Bad header: size is not int"
                        )
                    message_size = int(line)
                elif line.startswith(TYPE_HEADER):
                    # nothing to do with type for now.
                    pass
                else:
                    raise ResponseError(
                        ErrorCodes.ParseError, f"Bad header: unknown header {line}"
                    )
            if not message_size:
                raise ResponseError(ErrorCodes.ParseError, "Bad header: missing size")

            logger.debug(f"Message size: {message_size}")

            # jsonrpc_res = self.io_recv.read(message_size).decode("utf-8")
            jsonrpc_res = self.io_recv.read(message_size)

            logger.debug(f"Received data over {self.io_recv} {jsonrpc_res}")

            try:
                return RpcMessage.model_validate_json(jsonrpc_res)
            except Exception as e:
                raise ResponseError(
                    ErrorCodes.InvalidRequest, "Bad response: could not validate."
                ) from e


class RpcServer(threading.Thread):
    def __init__(
        self,
        json_rpc_endpoint: RpcEndpoint,
        method_callbacks: Optional[dict[str, Callable]] = None,
        notify_callbacks: Optional[dict[str, Callable]] = None,
        timeout=2,
    ):
        if method_callbacks is None:
            method_callbacks = dict[str, Callable]({})
        if notify_callbacks is None:
            notify_callbacks = dict[str, Callable]({})

        threading.Thread.__init__(self)

        self.json_rpc_endpoint = json_rpc_endpoint
        self.notify_callbacks = notify_callbacks
        self.method_callbacks = method_callbacks
        self.event_dict: dict[int, threading.Condition] = {}
        self.response_dict: dict[
            int, tuple[Optional[Any], Optional[RpcMessageError]]
        ] = {}
        self.next_id = 0
        self._timeout = timeout
        self.shutdown_flag = False

    def handle_result(
        self, rpc_id: int, result: Optional[Any], error: Optional[RpcMessageError]
    ):
        self.response_dict[rpc_id] = (result, error)
        cond = self.event_dict[rpc_id]
        cond.acquire()
        cond.notify()
        cond.release()

    def stop(self):
        self.shutdown_flag = True

    def run(self):
        while not self.shutdown_flag:
            # try:
            msg = self.json_rpc_endpoint.recv_response()
            if msg is None:
                logger.info("server quit")
                break

            if msg.method is not None:
                if msg.id is not None:
                    # a call for method
                    if msg.method not in self.method_callbacks:
                        raise ResponseError(
                            ErrorCodes.MethodNotFound,
                            f"Method not found: {msg.method}",
                        )
                    self.send_response(
                        msg.id, self.method_callbacks[msg.method](msg.params), None
                    )
                else:
                    # a call for notify
                    if msg.method not in self.notify_callbacks:
                        # Have nothing to do with this.
                        logger.error(f"Notify method not found: {msg.method}.")
                    else:
                        self.notify_callbacks[msg.method](msg.params)
            else:
                self.handle_result(msg.id, msg.result, msg.error)

        # FIXME: msg.id is None when we reach here
        # except ResponseError as e:
        #     self.send_response(msg.id, None, e)

    def send_response(self, id, result, error):
        message_dict = {}
        message_dict["jsonrpc"] = "2.0"
        message_dict["id"] = id
        if result:
            message_dict["result"] = result
        if error:
            message_dict["error"] = error
        self.json_rpc_endpoint.send_request(message_dict)

    def send_message(self, method_name, params, id=None):
        message_dict = {}
        message_dict["jsonrpc"] = "2.0"
        if id is not None:
            message_dict["id"] = id
        message_dict["method"] = method_name
        message_dict["params"] = params
        self.json_rpc_endpoint.send_request(message_dict)

    def call_method(self, method_name, **kwargs):
        current_id = self.next_id
        self.next_id += 1
        cond = threading.Condition()
        self.event_dict[current_id] = cond

        cond.acquire()
        self.send_message(method_name, kwargs, current_id)
        if self.shutdown_flag:
            cond.release()
            return None

        if not cond.wait(timeout=self._timeout):
            raise TimeoutError()
        cond.release()

        self.event_dict.pop(current_id)
        result, error = self.response_dict.pop(current_id)
        if error is not None:
            raise ResponseError(error.code, error.message, error.data)
        return result

    def send_notification(self, method_name, **kwargs):
        self.send_message(method_name, kwargs)

import abc
import json
import logging
import threading

# Based on: github.com/python-lsp/python-lsp-jsonrpc

log = logging.getLogger(__name__)


class JsonRpcStreamReader(abc.ABC):
    @abc.abstractmethod
    def __init__(self, rfile) -> None: ...

    @abc.abstractmethod
    def close(self) -> None: ...

    @abc.abstractmethod
    def listen(self, message_consumer) -> None: ...


class LSPStyleStreamReader(JsonRpcStreamReader):
    def __init__(self, rfile):
        self._rfile = rfile

    def close(self):
        self._rfile.close()

    def listen(self, message_consumer):
        """Blocking call to listen for messages on the rfile.

        Args:
            message_consumer (fn): function that is passed each message as it is read off the socket.
        """
        while not self._rfile.closed:
            try:
                request_str = self._read_message()
            except ValueError:
                if self._rfile.closed:
                    return
                log.exception("Failed to read from rfile")

            if request_str is None:
                break

            try:
                message_consumer(json.loads(request_str.decode("utf-8")))
            except ValueError:
                log.exception("Failed to parse JSON message %s", request_str)
                continue

    def _read_message(self):
        """Reads the contents of a message.

        Returns:
            body of message if parsable else None
        """
        line = self._rfile.readline()

        if not line:
            return None

        content_length = self._content_length(line)

        # Blindly consume all header lines
        while line and line.strip():
            line = self._rfile.readline()

        if not line:
            return None

        # Grab the body
        return self._rfile.read(content_length)

    @staticmethod
    def _content_length(line):
        """Extract the content length from an input line."""
        if line.startswith(b"Content-Length: "):
            _, value = line.split(b"Content-Length: ")
            value = value.strip()
            try:
                return int(value)
            except ValueError as e:
                raise ValueError(f"Invalid Content-Length header: {value}") from e

        return None


class JsonRpcStreamWriter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, wfile, **json_dumps_args): ...

    @abc.abstractmethod
    def close(self) -> None: ...

    @abc.abstractmethod
    def write(self, message) -> None: ...


class LSPStyleStreamWriter:
    def __init__(self, wfile, **json_dumps_args):
        self._wfile = wfile
        self._wfile_lock = threading.Lock()
        self._json_dumps_args = json_dumps_args

    def close(self):
        with self._wfile_lock:
            self._wfile.close()

    def write(self, message):
        with self._wfile_lock:
            if self._wfile.closed:
                return
            try:
                body = json.dumps(message, **self._json_dumps_args)

                # Ensure we get the byte length, not the character length
                content_length = (
                    len(body) if isinstance(body, bytes) else len(body.encode("utf-8"))
                )

                response = (
                    f"Content-Length: {content_length}\r\n"
                    f"Content-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n"
                    f"{body}"
                )

                self._wfile.write(response.encode("utf-8"))
                self._wfile.flush()
            except Exception:  # pylint: disable=broad-except
                log.exception("Failed to write message to output file %s", message)

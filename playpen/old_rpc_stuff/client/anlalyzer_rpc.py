import json
import logging

from pylspclient.json_rpc_endpoint import JsonRpcEndpoint, MyEncoder
from pylspclient.lsp_client import LspEndpoint as RpcServer
from pylspclient.lsp_errors import ErrorCodes, ResponseError

log = logging.getLogger("analyzer-rpc")


class AnalyzerRpcServer(RpcServer):

    def run(self):
        while not self.shutdown_flag:
            try:
                jsonrpc_message = self.json_rpc_endpoint.recv_response()
                if jsonrpc_message is None:
                    log.debug("server quit")
                    break
                method = jsonrpc_message.get("method")
                result = jsonrpc_message.get("result")
                error = jsonrpc_message.get("error")
                rpc_id = jsonrpc_message.get("id")
                params = jsonrpc_message.get("params")

                # Because this is only a client, we will never not have a result. If we don't have a result, we are
                if not result:
                    continue

                if method:
                    if rpc_id is not None:
                        if method not in self.method_callbacks:
                            raise ResponseError(
                                ErrorCodes.MethodNotFound,
                                "Method not found: {method}".format(method=method),
                            )
                        result = self.method_callbacks[method](**params["kwargs"])
                        self.send_response(rpc_id, result, None)
                    else:
                        if method not in self.notify_callbacks:
                            log.debug(
                                "Notify method not found: {method}.".format(
                                    method=method
                                )
                            )
                        else:
                            self.notify_callbacks[method](params)
                else:
                    self.handle_result(rpc_id, result, error)
            except ResponseError as e:
                self.send_response(rpc_id, None, e)
            except Exception as e:
                self.send_response(
                    rpc_id, None, ResponseError(ErrorCodes.InternalError, str(e))
                )

    def send_message(self, method_name, params, id=None):
        message_dict = {}
        message_dict["jsonrpc"] = "2.0"
        if id is not None:
            message_dict["id"] = id
        message_dict["Method"] = method_name
        if "kwargs" in params:
            message_dict["params"] = [params["kwargs"]]
        self.json_rpc_endpoint.send_request(message_dict)


class AnlayzerRPCEndpoint(JsonRpcEndpoint):
    def send_request(self, message):
        json_string = json.dumps(message, cls=MyEncoder)
        log.debug(f"sending data over stdin {repr(json_string)}")
        with self.write_lock:
            self.stdin.buffer.write(json_string.encode())
            self.stdin.flush()

    def recv_response(self):
        with self.read_lock:
            jsonrpc_res = self.stdout.buffer.readline().decode("utf-8")
            if jsonrpc_res:
                log.debug(f"read data from stdout {repr(jsonrpc_res)}")
                try:
                    return json.loads(jsonrpc_res)
                except Exception as e:
                    print(f"unable to load read data to json: {jsonrpc_res} -- {e}")
            return json.loads("{}")

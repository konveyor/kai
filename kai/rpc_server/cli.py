import json
import os
import subprocess  # trunk-ignore(bandit/B404)
import sys
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Literal, cast

import yaml
from pydantic import BaseModel, Field, FilePath
from pydantic_settings import BaseSettings, CliApp, CliSubCommand

from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer
from kai.jsonrpc.models import JsonRpcError, JsonRpcRequest
from kai.jsonrpc.streams import BareJsonStream


class RpcConfig(BaseModel):
    process: str
    request_timeout: float | None = 240


class RunFile(BaseSettings):
    rpc_config: RpcConfig | FilePath

    input: FilePath = Field(
        ..., description="Sequence of requests to make from a YAML or JSON file."
    )
    output: Path | None = Field(
        None, description="Output file to write the results to."
    )
    output_format: Literal["yaml", "json"] = Field(
        "yaml", description="Output format that the results should be written in."
    )

    def cli_cmd(self) -> None:
        if isinstance(self.rpc_config, Path):
            with open(self.rpc_config, "r") as f:
                self.rpc_config = RpcConfig.model_validate(yaml.safe_load(f.read()))

        input_data_raw = yaml.safe_load(open(self.input, "r"))
        if not isinstance(input_data_raw, list):
            raise Exception(
                "Input file must be a list of dicts with keys 'method' and 'params'"
            )

        input_data: list[JsonRpcRequest] = []
        for request in input_data_raw:
            input_data.append(JsonRpcRequest.model_validate(request))

        output: list[dict[str, Any] | None] = []

        # trunk-ignore-begin(bandit/B603)
        rpc_subprocess = subprocess.Popen(
            self.rpc_config.process.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            env=os.environ,
        )
        # trunk-ignore-end(bandit/B603)

        app = JsonRpcApplication()

        @app.add_notify(method="*")
        def recv_notify(
            app: JsonRpcApplication,
            server: JsonRpcServer,
            id: Any,
            params: dict[str, Any],
        ) -> None:
            output.append(params)

        rpc_server = JsonRpcServer(
            json_rpc_stream=BareJsonStream(
                cast(BufferedReader, rpc_subprocess.stdout),
                cast(BufferedWriter, rpc_subprocess.stdin),
            ),
            app=app,
            request_timeout=self.rpc_config.request_timeout,
        )

        rpc_server.start()

        try:
            for request in input_data:
                response = rpc_server.send_request(
                    method=request.method, params=request.params
                )

                if isinstance(response, JsonRpcError):
                    raise Exception(
                        f"Failed to get response for {request['method']} - {response.code} {response.message}"
                    )
                elif response is None:
                    output.append(response)
                else:
                    output.append(response.model_dump())

            if self.output is not None:
                with open(self.output, "w") as f:
                    if self.output_format == "json":
                        f.write(json.dumps(output))
                    else:
                        f.write(yaml.dump(output))

        finally:
            rpc_subprocess.terminate()
            rpc_subprocess.wait()
            rpc_server.stop()


class KaiCli(BaseSettings):
    run_file: CliSubCommand[RunFile] = Field(
        ..., description="Run a sequence of JSON-RPC requests from a file."
    )

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)


if __name__ == "__main__":
    _cmd = CliApp.run(KaiCli, sys.argv[1:])

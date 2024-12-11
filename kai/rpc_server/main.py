# Need to initialize this before we start getting the tracer in the other files on import
import argparse
import logging as core_logging
import multiprocessing
import os
import sys
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import cast

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.threading import ThreadingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import kai.logging.logging as logging
from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.streams import LspStyleStream
from kai.rpc_server.server import KaiLogConfig, app

DEFAULT_FORMATTER = core_logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

TRACING_ENABLED = "ENABLE_TRACING"

resource = Resource(attributes={SERVICE_NAME: "kai-rpc"})
tracer_provider = TracerProvider(resource=resource)
tracer = trace.get_tracer(__name__)

ThreadingInstrumentor().instrument()


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.description = "Kai RPC Server"
    parser.add_argument(
        "--log-level",
        help="The initial log level for the server",
        default="INFO",
        type=str,
    )
    parser.add_argument(
        "--stderr-log-level",
        help="The initial stderr log level for the server",
        default="TRACE",
        type=str,
    )
    parser.add_argument(
        "--file-log-level",
        help="The initial file log level for the server",
        default="DEBUG",
        type=str,
    )
    parser.add_argument(
        "--log-dir-path",
        help="The directory path for log files",
        default=Path("./logs"),
        type=Path,
    )
    parser.add_argument(
        "--log-file-name",
        help="The name of the log file",
        default="kai-rpc-server.log",
        type=str,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    log_config = KaiLogConfig(
        log_level=_args.log_level,
        stderr_log_level=_args.stderr_log_level,
        file_log_level=_args.file_log_level,
        log_dir_path=_args.log_dir_path,
        log_file_name=_args.log_file_name,
    )
    logging.init_logging_from_log_config(log_config)

    log = logging.get_logger("kai-rpc-logger")
    log.info(f"using log config: {log_config}")

    if TRACING_ENABLED in os.environ:
        tracer_provider.add_span_processor(
            span_processor=BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(tracer_provider=tracer_provider)

    # mypy incorrectly type checks sys.stdin.buffer and sys.stdout.buffer as
    # simply IO[bytes], rather than as BufferedReader and BufferedWriter for
    # some reason, at least on my machine.
    rpc_server = JsonRpcServer(
        json_rpc_stream=LspStyleStream(
            cast(BufferedReader, sys.stdin.buffer),
            cast(BufferedWriter, sys.stdout.buffer),
        ),
        app=app,
        log=log,
    )

    with tracer.start_as_current_span("main_server"):
        rpc_server.start()
        log.info("Started kai RPC Server")
        rpc_server.join()


if __name__ == "__main__":
    # We need this to have PyInstaller work properly
    multiprocessing.freeze_support()

    main()

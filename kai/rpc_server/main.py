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
from kai.jsonrpc.streams import BareJsonStream
from kai.kai_config import KaiConfig
from kai.rpc_server.server import app

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
        "-c",
        "--config",
        help="This is the configuration file for the kai rpc server.",
        type=Path,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    _args = parser.parse_args()

    if _args.config:
        config = KaiConfig.model_validate_filepath(_args.config)
        logging.init_logging_from_config(config)

    log = logging.get_logger("kai-rpc-logger")
    log.info(f"using config: {config}")

    if TRACING_ENABLED in os.environ:
        tracer_provider.add_span_processor(
            span_processor=BatchSpanProcessor(OTLPSpanExporter())
        )
        trace.set_tracer_provider(tracer_provider=tracer_provider)

    # mypy incorrectly type checks sys.stdin.buffer and sys.stdout.buffer as
    # simply IO[bytes], rather than as BufferedReader and BufferedWriter for
    # some reason, at least on my machine.
    rpc_server = JsonRpcServer(
        json_rpc_stream=BareJsonStream(
            cast(BufferedReader, sys.stdin.buffer),
            cast(BufferedWriter, sys.stdout.buffer),
            log=log,
        ),
        app=app,
        log=log,
    )

    with tracer.start_as_current_span("main_server"):
        rpc_server.start()
        log.info("Started kai RPC Server")
        rpc_server.join()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

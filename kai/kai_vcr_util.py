import logging
import os
from contextlib import contextmanager
from typing import Generator

import vcr  # type: ignore

from kai.constants import PATH_DATA

KAI_LOG = logging.getLogger("vcr")


@contextmanager
def playback_if_demo_mode(
    demo_mode: bool, model_id: str, application_name: str, agent: str, filename: str
) -> Generator[None, None, None]:
    """
    A context manager to conditionally use a VCR cassette when demo mode is
    enabled.
    """

    record_mode = "once" if demo_mode else "all"

    my_vcr = vcr.VCR(
        cassette_library_dir=os.path.join(
            PATH_DATA, "vcr", application_name, agent, model_id
        ),
        record_mode=record_mode,
        match_on=[
            "uri",
            "method",
            "scheme",
            "host",
            "port",
            "path",
            "query",
            "headers",
        ],
        record_on_exception=False,
        filter_headers=[
            "authorization",
            "cookie",
            "content-length",
            "x-stainless-lang",
            "x-stainless-async",
            "x-stainless-runtime",
            "x-stainless-arch",
            "x-stainless-os",
            "x-stainless-package-version",
            "x-stainless-runtime-version",
            "user-agent",
        ],
    )
    KAI_LOG.debug(
        f"record_mode='{record_mode}' - Using cassette {application_name}/{agent}/{model_id}/{filename}.yaml",
    )

    # Workaround to actually blow away the cassettes instead of appending
    if my_vcr.record_mode == "all":
        my_vcr.persister.load_cassette = lambda cassette_path, serializer: ([], [])

    with my_vcr.use_cassette(f"{filename}.yaml"):
        yield

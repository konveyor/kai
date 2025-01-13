import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import vcr  # type: ignore

# vcr has no type hints :(
from git import Optional
from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    Template,
    TemplateNotFound,
)

from kai.constants import PATH_DATA, PATH_TEMPLATES

KAI_LOG = logging.getLogger(__name__)


def get_prompt(
    template_name: str,
    pb_vars: dict[Any, Any],
    path_templates: Path = PATH_TEMPLATES,
    jinja_kwargs: Optional[dict[Any, Any]] = None,
    fallback: bool = True,
    add_ext_if_not_present: bool = True,
) -> str:
    """
    Generate a prompt using Jinja templates based on the provided model
    provider, variable dictionary, and optional path templates and Jinja
    arguments. `fallback` is a boolean that determines whether to fall back to
    main.jinja or error out.
    """

    if add_ext_if_not_present and not template_name.endswith(".jinja"):
        template_name = f"{template_name}.jinja"

    if jinja_kwargs is None:
        jinja_kwargs = {}

    jinja_kwargs = {
        "loader": FileSystemLoader(path_templates),
        "undefined": StrictUndefined,
        "trim_blocks": True,
        "lstrip_blocks": True,
        "autoescape": True,
        **jinja_kwargs,
    }

    jinja_env = Environment(**jinja_kwargs)  # trunk-ignore(bandit/B701)

    template: Template

    try:
        try:
            template = jinja_env.get_template(template_name)
        except TemplateNotFound:
            # Template might be a full path, create new Jinja environment
            template_dir = os.path.abspath(os.path.join(template_name, ".."))
            template_filename = os.path.basename(template_name)

            template_kwargs = {
                **jinja_kwargs,
                "loader": FileSystemLoader(template_dir),
            }

            # NOTE: Have to use ignore-begin and ignore-end because `trunk` will
            # push the comments to the next line, which will break the ignore

            # trunk-ignore-begin(bandit/B701)
            template_jinja_env = Environment(**template_kwargs)
            # trunk-ignore-end(bandit/B701)

            template = template_jinja_env.get_template(template_filename)
    except TemplateNotFound as e:
        if not fallback:
            raise e

        KAI_LOG.debug(f"Template '{e.name}' not found. Falling back to main.jinja")
        template = jinja_env.get_template("main.jinja")

    KAI_LOG.debug(f"Template {template.filename} loaded")

    return template.render(pb_vars)


@contextmanager
def playback_if_demo_mode(
    demo_mode: bool, model_id: str, application_name: str, filename: str
) -> Generator[None, None, None]:
    """
    A context manager to conditionally use a VCR cassette when demo mode is
    enabled.
    """

    record_mode = "once" if demo_mode else "all"

    my_vcr = vcr.VCR(
        cassette_library_dir=os.path.join(
            PATH_DATA, f"vcr/{application_name}/{model_id}/"
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
        f"record_mode='{record_mode}' - Using cassette {application_name}/{model_id}/{filename}.yaml",
    )

    # Workaround to actually blow away the cassettes instead of appending
    if my_vcr.record_mode == "all":
        my_vcr.persister.load_cassette = lambda cassette_path, serializer: ([], [])

    with my_vcr.use_cassette(f"{filename}.yaml"):
        yield

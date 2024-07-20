import itertools
import os
from contextlib import contextmanager
from enum import StrEnum
from typing import Callable

import vcr
from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    Template,
    TemplateNotFound,
)

from kai.constants import PATH_DATA, PATH_TEMPLATES
from kai.kai_logging import KAI_LOG
from kai.models.report_types import ExtendedIncident


def get_prompt(
    template_name: str,
    pb_vars: dict,
    path_templates: str = PATH_TEMPLATES,
    jinja_kwargs: dict = None,
    fallback: bool = True,
    add_ext_if_not_present: bool = True,
):
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

        KAI_LOG.warning(f"Template '{e.name}' not found. Falling back to main.jinja")
        template = jinja_env.get_template("main.jinja")

    KAI_LOG.debug(f"Template {template.filename} loaded")

    return template.render(pb_vars)


@contextmanager
def playback_if_demo_mode(
    demo_mode: bool, model_id: str, application_name: str, filename: str
):
    """
    A context manager to conditionally use a VCR cassette when demo mode is
    enabled.
    """

    record_mode = ("once" if demo_mode else "all",)

    my_vcr = vcr.VCR(
        cassette_library_dir=f"{os.path.join(PATH_DATA, 'vcr/{application_name}/{model_id}/')}",
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
        filter_headers=["authorization", "cookie", "content-length"],
    )
    KAI_LOG.debug(
        f"record_mode='{record_mode}' - Using cassette {application_name}/{model_id}/{filename}.yaml",
    )

    # Workaround to actually blow away the cassettes instead of appending
    if my_vcr.record_mode == "all":
        my_vcr.persister.load_cassette = lambda cassette_path, serializer: ([], [])

    with my_vcr.use_cassette(f"{filename}.yaml"):
        yield


class BatchMode(StrEnum):
    # Every incident is passed individually one after the other
    NONE = "none"
    # One llm call where we pass all incidents
    SINGLE_GROUP = "single_group"
    # Group by ruleset, then call LLM per ruleset group
    RULESET = "ruleset"
    # Group by violation, then call LLM per violation group
    VIOLATION = "violation"


def batch_incidents(incidents: list[ExtendedIncident], batch_mode: BatchMode):
    """
    Batch mode represents different strategies for how we group the incidents in
    each call to the LLM, updating the code from the previous call/input.
    Returns a list of tuples, where each tuple contains a dictionary of what is
    common to every element in the list.
    """
    key_fn: Callable[[ExtendedIncident], tuple]
    res_fn: Callable[[tuple], dict]

    # trunk-ignore-begin(ruff/E731)

    match batch_mode:
        case BatchMode.NONE:
            key_fn = lambda x: (id(x),)
            res_fn = lambda k: {}
        case BatchMode.SINGLE_GROUP:
            key_fn = lambda x: (0,)
            res_fn = lambda k: {}
        case BatchMode.RULESET:
            key_fn = lambda x: (x.ruleset_name,)
            res_fn = lambda k: {"ruleset_name": k[0]}
        case BatchMode.VIOLATION:
            key_fn = lambda x: (x.ruleset_name, x.violation_name)
            res_fn = lambda k: {"ruleset_name": k[0], "violation_name": k[1]}

    # trunk-ignore-end(ruff/E731)

    incidents.sort(key=key_fn)
    batched_groupby = itertools.groupby(incidents, key_fn)

    return [(res_fn(key), list(grp)) for key, grp in batched_groupby]

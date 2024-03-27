#!/usr/bin/python3

# FIXME: This code should live in 'kai-service' but I couldn't get it to import
# the required `kai` modules. Someone smarter than me may be able to fix this.
# For now, I just copied this code wholesale. - jsussman

"""This module is intended to facilitate using Konveyor with LLMs."""

import argparse
import itertools
import json
import os
import pprint
import time
import tomllib
import warnings
from collections import defaultdict
from os import listdir
from os.path import isfile, join

import aiohttp
import jsonschema
import yaml
from aiohttp import web
from aiohttp.web_request import Request
from incident_store_advanced import Application, EmbeddingNone, PSQLIncidentStore
from kai_logging import KAI_LOG
from model_provider import IBMGraniteModel, IBMOpenSourceModel, OpenAIModel
from prompt_builder import CONFIG_IBM_GRANITE_MF, build_prompt
from report import Report

from kai.capture import Capture
from kai.pydantic_models import parse_file_solution_content

LLM_RETRIES = 5
LLM_RETRY_DELAY = 10

# TODO: Make openapi spec for everything

# TODO: Repo lives both on client and on server. Determine either A) Best way to
# rectify differences or B) Only have the code on one and pass stuff between
# each other
# - can be solved by getting last common commits and then applying a git diff in
#   the same manner as `git stash apply`


routes = web.RouteTableDef()

JSONSCHEMA_DIR = os.path.join(
    os.path.dirname(__file__),
    "data/jsonschema/",
)


def load_config():
    """Load the configuration from a yaml conf file."""
    config_prefix = "/usr/local/etc"
    if os.environ.get("KAI_CONFIG_PREFIX"):
        config_prefix = os.environ.get("KAI_CONFIG_PREFIX")

    config_dir = "kai.conf.d"
    model_dir = os.path.join(config_prefix, config_dir)
    files = [f for f in listdir(model_dir) if isfile(join(model_dir, f))]
    model_templates = {}
    for f in files:
        filename, file_extension = os.path.splitext(f)
        with open(join(model_dir, f), encoding="utf-8") as reader:
            try:
                model = reader.read()
                model_templates[filename] = model
            except yaml.YAMLError as exc:
                print(exc)
                return None
    return {"model_templates": model_templates}


def load_templates():
    """Get model templates from the loaded configuration."""
    return load_config()["model_templates"]


def load_template(model_name):
    """Loads the requested template."""
    model_templates = load_templates()
    if model_name in model_templates:
        return model_templates[model_name]

    warnings.warn(
        "Warning: Model not found, using first available model.",
        stacklevel=5,
    )
    return list(model_templates.items())[0][1]


@routes.post("/generate_prompt")
async def generate_prompt(request):
    """Generates a prompt based on input using the specified template."""
    try:
        data = await request.json()

        language = data.get("language", "")
        issue_description = data.get("issue_description", "")
        example_original_code = data.get("example_original_code", "")
        example_solved_code = data.get("example_solved_code", "")
        current_original_code = data.get("current_original_code", "")
        model_template = data.get("model_template", "")

        if model_template == "":
            warnings.warn(
                "Model template not specified. For best results specify a model template.",
                stacklevel=5,
            )

        response = load_template(model_template).format(
            language=language,
            issue_description=issue_description,
            example_original_code=example_original_code,
            example_solved_code=example_solved_code,
            current_original_code=current_original_code,
            model_template=model_template,
        )

        warnings.resetwarnings()
        return web.json_response({"generated_prompt": response})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


@routes.route("*", "/proxy")
async def proxy_handler(request):
    """Proxies a streaming request to an LLM."""
    upstream_url = request.query.get("upstream_url")

    if not upstream_url:
        return web.Response(
            status=400, text="Missing 'upstream_url' parameter in the request"
        )

    headers = {}
    if request.headers.get("Authorization"):
        headers.update({"Authorization": request.headers.get("Authorization")})
    if request.headers.get("Content-Type"):
        headers.update({"Content-Type": request.headers.get("Content-Type")})
    method = request.method
    data = await request.read()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method, upstream_url, headers=headers, data=data
            ) as upstream_response:
                if "chunked" in upstream_response.headers.get("Transfer-Encoding", ""):
                    response = web.StreamResponse()
                    await response.prepare(request)

                    async for data in upstream_response.content.iter_any():
                        await response.write(data)

                    await response.write_eof()
                    return response

                return web.Response(
                    status=upstream_response.status,
                    text=await upstream_response.text(),
                    headers=upstream_response.headers,
                )
        except aiohttp.ClientError as e:
            return web.Response(
                status=500, text=f"Error connecting to upstream service: {str(e)}"
            )


async def run_analysis_report():
    pass


@routes.post("/dummy_json_request")
async def post_dummy_json_request(request: Request):
    KAI_LOG.debug(f"post_dummy_json_request recv'd: {request}")

    request_json: dict = await request.json()

    return web.json_response({"feeling": "OK!", "recv": request_json})


@routes.post("/load_analysis_report")
async def post_load_analysis_report(request: Request):
    schema: dict = json.loads(
        open(os.path.join(JSONSCHEMA_DIR, "post_load_analysis_report.json")).read()
    )
    request_json: dict = await request.json()

    try:
        jsonschema.validate(instance=request_json, schema=schema)
    except jsonschema.ValidationError as err:
        raise web.HTTPUnprocessableEntity(text=f"{err}") from err

    request_json["application"].setdefault("application_id")

    application = Application(**request_json["application"])
    path_to_report: str = request_json["path_to_report"]
    report = Report(path_to_report)

    count = request.app["incident_store"].insert_and_update_from_report(
        application, report
    )

    return web.json_response(
        {
            "number_new_incidents": count[0],
            "number_unsolved_incidents": count[1],
            "number_solved_incidents": count[2],
        }
    )


@routes.post("/change_model")
async def post_change_model(request: Request):
    pass


def get_incident_solution(request_app, request_json: dict, stream: bool = False):
    start = time.time()
    capture = Capture()
    capture.request = request_json
    capture.model_id = request_app["model_provider"].get_current_model_id()

    application_name: str = request_json["application_name"]
    application_name = application_name  # NOTE: To please trunk error, remove me
    ruleset_name: str = request_json["ruleset_name"]
    violation_name: str = request_json["violation_name"]
    # FIXME: See my comment here
    # https://github.com/konveyor-ecosystem/kai/issues/87#issuecomment-2015574994
    incident_snip: str = request_json.get("incident_snip", "")
    incident_vars: dict = request_json["incident_variables"]
    file_name: str = request_json["file_name"]
    file_contents: str = request_json["file_contents"]
    line_number: int = request_json["line_number"]
    analysis_message: str = request_json.get("analysis_message", "")

    KAI_LOG.info(
        f"START - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{capture.model_id}'"
    )

    # Gather context
    # First, let's see if there's an "exact" match

    solved_incident, match_type = request_app[
        "incident_store"
    ].get_fuzzy_similar_incident(
        violation_name, ruleset_name, incident_snip, incident_vars
    )
    capture.solved_incident = solved_incident

    if not isinstance(solved_incident, dict):
        raise Exception("solved_example not a dict")

    pb_vars = {
        "src_file_name": file_name,
        "src_file_contents": file_contents,
        "analysis_line_number": str(line_number),
        "analysis_message": analysis_message,
    }

    KAI_LOG.debug(solved_incident)

    if bool(solved_incident) and match_type == "exact":
        solved_example = request_app["incident_store"].select_accepted_solution(
            solved_incident["solution_id"]
        )
        pb_vars["solved_example_diff"] = solved_example["solution_small_diff"]
        pb_vars["solved_example_file_name"] = solved_incident["incident_uri"]

    prompt = build_prompt(
        request_app["model_provider"].get_prompt_builder_config(), pb_vars
    )
    capture.prompt = prompt

    if stream:
        capture.llm_result = (
            "TODO consider if we need to implement for streaming responses"
        )
        capture.commit()
        end = time.time()
        KAI_LOG.info(
            f"END - completed in '{end-start}s: - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{capture.model_id}'"
        )
        return request_app["model_provider"].stream(prompt)
    else:
        llm_result = request_app["model_provider"].invoke(prompt)
        capture.llm_result = request_app["model_provider"].invoke(prompt)
        capture.commit()
        end = time.time()
        KAI_LOG.info(
            f"END - completed in '{end-start}s: - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{capture.model_id}'"
        )
        return llm_result


# TODO: Figure out why we have to put this validator wrapping the routes
# decorator
def validator(schema_file):
    def decorator(fn):
        async def inner(request: Request, *args, **kwargs):
            request_json = await request.json()

            schema: dict = json.loads(
                open(os.path.join(JSONSCHEMA_DIR, schema_file)).read()
            )

            try:
                jsonschema.validate(instance=request_json, schema=schema)
            except jsonschema.ValidationError as err:
                KAI_LOG.error(f"{err}")
                raise web.HTTPUnprocessableEntity(text=f"{err}") from err

            return fn(request, *args, **kwargs)

        return inner

    return decorator


@validator("post_get_incident_solution.json")
@routes.post("/get_incident_solution")
async def post_get_incident_solution(request: Request):
    """
    Will need to cache the incident result so that the user, when it accepts
    or rejects it knows what the heck the user is referencing

    Stateful, stores it

    params (json):
    - application_name (str)
    - ruleset_name (str)
    - violation_name (str)
    - incident_snip (str optional)
    - incident_variables (object)
    - file_name (str)
    - file_contents (str)
    - line_number: 0-indexed (let's keep it consistent)
    - analysis_message (str)

    return (json):
    - llm_output:
    """

    KAI_LOG.debug(f"post_get_incident_solution recv'd: {request}")

    llm_output = get_incident_solution(request.app, await request.json(), False).content

    return web.json_response(
        {
            "llm_output": llm_output,
        }
    )


@validator("post_get_incident_solution.json")
@routes.get("/ws/get_incident_solution")
async def ws_get_incident_solution(request: Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    msg = await ws.receive()

    if msg.type == web.WSMsgType.TEXT:
        try:
            json_request = json.loads(msg.data)

            for chunk in get_incident_solution(request.app, json_request, True):
                await ws.send_str(
                    json.dumps(
                        {
                            "content": chunk.content,
                        }
                    )
                )

        except json.JSONDecodeError:
            await ws.send_str(json.dumps({"error": "Received non-json data"}))

    elif msg.type == web.WSMsgType.ERROR:
        await ws.send_str(
            json.dumps({"error": f"Websocket closed with exception {ws.exception()}"})
        )
    else:
        await ws.send_str(json.dumps({"error": "Unsupported message type"}))

    await ws.close()

    return ws


@validator("get_incident_solutions_for_file.json")
@routes.post("/get_incident_solutions_for_file")
async def get_incident_solutions_for_file(request: Request):
    """
    - file_name (str)
    - file_contents (str)
    - application_name (str)
    - outside_grouping (str optional, one of 'sequential', 'none', 'violation', 'violation_and_variables')
    - inside_grouping (str optional, one of 'none', 'line_number')
    - incidents (list)
        - ruleset_name (str)
        - violation_name (str)
        - incident_snip (str optional)
        - incident_variables (object)
        - line_number: 0-indexed (let's keep it consistent)
        - analysis_message (str)
    """
    start = time.time()
    KAI_LOG.debug(f"get_incident_solutions_for_file recv'd: {request}")

    request_json = await request.json()

    KAI_LOG.info(
        f"START - App: '{request_json['application_name']}', File: '{request_json['file_name']}' with {len(request_json['incidents'])} incidents'"
    )

    outside_grouping = request_json.get("outside_grouping", "sequential")
    inside_grouping = request_json.get("inside_grouping", "sequential")

    # NOTE: Looks worse than it is, `trunk check` mangled the heck out of this
    # section. It doesn't like lambdas for some reason :(

    if outside_grouping == "none":  # own group

        def outside_key_fn(x):
            return (id(x),)

        def outside_res_fn(k, g):
            return {}, list(g)

    elif outside_grouping == "single_group":  # single group

        def outside_key_fn(x):
            return (0,)

        def outside_res_fn(k, g):
            return {}, list(g)

    elif outside_grouping == "ruleset":

        def outside_key_fn(x):
            return (x.get("ruleset_name"),)

        def outside_res_fn(k, g):
            return {"ruleset_name": k[0]}, list(g)

    elif outside_grouping == "violation":  # violations group

        def outside_key_fn(x):
            return x.get("ruleset_name"), x.get("violation_name")

        def outside_res_fn(k, g):
            return {"ruleset_name": k[0], "violation_name": k[1]}, list(g)

    else:
        raise Exception(f"Invalid outside_grouping: {outside_grouping}")

    if inside_grouping == "none":

        def inside_key_fn(x):
            return 0

        def inside_res_fn(k, g):
            return {}, list(g)

    # FIXME: 'incident_variables' is unhashable.
    elif inside_grouping == "violation":

        def inside_key_fn(x):
            return x.get("ruleset_name"), x.get("violation_name")

        def inside_res_fn(key, group):
            aggregated = defaultdict(set)
            for item in group:
                for k, v in item.items():
                    if k not in key:
                        aggregated[k].add(v)
            return ({"ruleset_name": k[0], "violation_name": k[1]}, dict(aggregated))

    else:
        raise Exception(f"Invalid inside_grouping: {inside_grouping}")

    updated_file = request_json["file_contents"]
    total_reasoning = []
    used_prompts = []

    request_json["incidents"].sort(key=outside_key_fn)
    outside_grouped = itertools.groupby(request_json["incidents"], outside_key_fn)
    for outside_key, outside_group in outside_grouped:
        _, outside_incidents = outside_res_fn(outside_key, outside_group)

        outside_incidents.sort(key=inside_key_fn)
        inside_grouped = itertools.groupby(outside_incidents, inside_key_fn)
        for inside_key, inside_group in inside_grouped:
            _, inside_incidents = inside_res_fn(inside_key, inside_group)
            for i, incident in enumerate(inside_incidents):
                incident["issue_number"] = i + 1
                incident["src_file_language"] = "java"
                incident["analysis_line_number"] = incident["line_number"]

            prompt = build_prompt(
                CONFIG_IBM_GRANITE_MF,
                {
                    "src_file_name": request_json["file_name"],
                    "src_file_language": "java",
                    "src_file_contents": updated_file,
                    "incidents": inside_incidents,
                },
            )

            #         KAI_LOG.info(
            #             f"Processing incident {count}/{len(request_json['incidents'])} for {incident['file_name']}"
            #         )

            llm_result = request.app["model_provider"].invoke(prompt)
            content = parse_file_solution_content(llm_result.content)

            total_reasoning.append(content.reasoning)
            updated_file = content.updated_file
            used_prompts.append(prompt)

            KAI_LOG.info(prompt)

    end = time.time()
    KAI_LOG.info(
        f"END - completed in '{end-start}s:  - App: '{request_json['application_name']}', File: '{request_json['file_name']}' with {len(request_json['incidents'])} incidents'"
    )

    return web.json_response(
        {
            "updated_file": updated_file,
            "total_reasoning": total_reasoning,
            "used_prompts": used_prompts,
        }
    )


def app(loglevel):
    webapp = web.Application()
    base_path = os.path.dirname(__file__)
    KAI_LOG.setLevel(loglevel.upper())
    print(
        f"Logging for KAI has been initialized and the level set to {loglevel.upper()}"
    )

    with open(os.path.join(base_path, "config.toml"), "rb") as f:
        config = tomllib.load(f)
        KAI_LOG.info(f"Config loaded: {pprint.pformat(config)}")

    schema: dict = json.loads(
        open(os.path.join(JSONSCHEMA_DIR, "server_config.json")).read()
    )
    # TODO: Make this error look nicer
    jsonschema.validate(instance=config, schema=schema)

    webapp["incident_store"] = PSQLIncidentStore(
        config=config["postgresql"],
        # emb_provider=EmbeddingInstructor(model="hkunlp/instructor-base"),
        emb_provider=EmbeddingNone(),
        drop_tables=False,
    )

    if config["models"]["provider"].lower() == "IBMGranite".lower():
        webapp["model_provider"] = IBMGraniteModel(**config["models"]["args"])
    elif config["models"]["provider"].lower() == "IBMOpenSource".lower():
        webapp["model_provider"] = IBMOpenSourceModel(**config["models"]["args"])
    elif config["models"]["provider"].lower() == "OpenAI".lower():
        webapp["model_provider"] = OpenAIModel(**config["models"]["args"])
    else:
        raise Exception(f"Unrecognized model '{config['models']['provider']}'")

    KAI_LOG.info(f"Selected model {config['models']['provider']}")
    webapp.add_routes(routes)

    return webapp


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-log",
        "--loglevel",
        default=os.environ.get("KAI_LOG_LEVEL", "info"),
        choices=["debug", "info", "warning", "error", "critical"],
        help="""Provide logging level.
Options:
- debug: Detailed information, typically of interest only when diagnosing problems.
- info: Confirmation that things are working as expected.
- warning: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
- error: Due to a more serious problem, the software has not been able to perform some function.
- critical: A serious error, indicating that the program itself may be unable to continue running.
Example: --loglevel debug (default: warning)""",
    )

    args, _ = arg_parser.parse_known_args()
    web.run_app(app(args.loglevel))


if __name__ == "__main__":
    main()

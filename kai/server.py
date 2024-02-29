#!/usr/bin/python3

# FIXME: This code should live in 'kai-service' but I couldn't get it to import
# the required `kai` modules. Someone smarter than me may be able to fix this.
# For now, I just copied this code wholesale. - jsussman

# TODO: Evaluate the viability of making this a django app - jsussman

"""This module is intended to facilitate using Konveyor with LLMs."""

import datetime
import json
import os
import warnings
from os import listdir
from os.path import isfile, join
import asyncio

import aiohttp
from aiohttp import web
from aiohttp.web import Response
from aiohttp.web_request import Request
import yaml
import jsonschema

from report import Report
from incident_store_advanced import PSQLIncidentStore, EmbeddingNone, Application
from prompt_builder import PromptBuilder

# TODO: Make openapi spec for everything

# TODO: Repo lives both on client and on server. Determine either A) Best way to
# rectify differences or B) Only have the code on one and pass stuff between
# each other
# - can be solved by getting last common commits and then applying a git diff in
#   the same manner as `git stash apply`

# TODO: Parameter validation


routes = web.RouteTableDef()

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


@routes.post('/dummy_json_request')
async def post_dummy_json_request(request: Request):
    print(f"post_dummy_json_request recv'd: {request}")

    request_json: dict = await request.json()

    return web.json_response({'feeling': 'OK!'})


@routes.post('/load_analysis_report')
async def post_load_analysis_report(request: Request):
    schema: dict = json.loads(open("data/jsonschema/post_load_analysis_report.json").read())
    request_json: dict = await request.json()

    try:
        jsonschema.validate(instance=request_json, schema=schema)
    except jsonschema.ValidationError as err:
        raise web.HTTPUnprocessableEntity(text=f"{err}")

    request_json['application'].setdefault('application_id')

    application = Application(**request_json["application"])
    path_to_report: str = request_json["path_to_report"]
    report = Report(path_to_report)

    count = incident_store.insert_and_update_from_report(application, report)

    return web.json_response({
        'number_new_incidents':      count[0],
        'number_unsolved_incidents': count[1],
        'number_solved_incidents':   count[2],
    })


# FIXME: Dangerous! Remove before deploying!
@routes.post('/drop_tables')
async def post_drop_tables(request: Request):
    conn = incident_store.conn
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS applications CASCADE;")
        cur.execute("DROP TABLE IF EXISTS rulesets CASCADE;")
        cur.execute("DROP TABLE IF EXISTS violations CASCADE;")
        cur.execute("DROP TABLE IF EXISTS accepted_solutions CASCADE;")
        cur.execute("DROP TABLE IF EXISTS incidents CASCADE;")
        cur.execute("DROP TABLE IF EXISTS potential_solutions CASCADE;")

    return web.Response(text="Ok")


@routes.post('/get_incident_solution')
async def post_get_incident_solution(request: Request):
    # TODO: Make a streaming version

    """
    Will need to cache the incident result so that the user, when it accepts
    or rejects it knows what the heck the user is referencing

    Stateful, stores it

    params (json):
    - application_name
    - ruleset_name
    - violation_name
    - file_contents
    - line_number: 0-indexed (let's keep it consistent)

    return (json):
    - previously solved incident (if exists)
    - context from the llm (high-level, "This is how I'd solve it")
    - some diff of the code to apply
    - id of the associated solved incident
    """

    solved_example = try_and_get_the_fricken_solved_example_maybe()
    prompt = generate_prompt()
    llm_result = proxy_handler(prompt)  # Maybe?

    diff = get_diff_from_llm_result()
    cache_result_id = cache_the_solution_somehow()

    return json.dumps(
        {
            "diff": diff,
            "id": cache_result_id,
        }
    )





def accept_or_reject_solution(params):
    """
    User says which solution and whether to reject or accept it

    params (json):
    - id: the id of the incident to accept or reject
    - accept: bool to say yes or no

    return (json):
    - success: duh
    """

    id = params["id"]
    accept = params["accept"]

    if accept:
        solution = get_solution_from_id(id)
        put_solution_in_indicent_store(solution)

    return json.dump({"success": True})


app = web.Application()
app.add_routes(routes)

incident_store: PSQLIncidentStore
prompt_builder: PromptBuilder

if __name__ == "__main__":
    incident_store = PSQLIncidentStore(
        config_filepath="../kai/database.ini",
        config_section="postgresql",
        emb_provider=EmbeddingNone(),
        drop_tables=True,
    )

    old_cmt_commit = 'c0267672ffab448735100996f5ad8ed814c38847'
    old_cmt_time   = 1708003534
    old_cmt_report_path ='/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/samples/analysis_reports/cmt/initial/output.yaml'
    old_cmt_report      = Report(old_cmt_report_path)
    new_cmt_commit = '25f00d88f8bceefb223390dcdd656bd5af45146e'
    new_cmt_time   = 1708003640
    new_cmt_report_path = '/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/samples/analysis_reports/cmt/solved/output.yaml'
    new_cmt_report      = Report(new_cmt_report_path)
    cmt_uri_origin = 'https://github.com/konveyor-ecosystem/cmt.git'
    cmt_uri_local  = 'file:///home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/samples/sample_repos/cmt'

    old_cmt_application = Application(None, 'cmt', cmt_uri_origin, cmt_uri_local, 'main',    old_cmt_commit, datetime.datetime.fromtimestamp(old_cmt_time))
    new_cmt_application = Application(None, 'cmt', cmt_uri_origin, cmt_uri_local, 'quarkus', new_cmt_commit, datetime.datetime.fromtimestamp(new_cmt_time))

    incident_store.insert_and_update_from_report(old_cmt_application, old_cmt_report)
    # input("> ")
    incident_store.insert_and_update_from_report(new_cmt_application, new_cmt_report)

    web.run_app(app)


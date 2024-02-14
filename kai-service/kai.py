#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import json
import os
import warnings
from os import listdir
from os.path import isfile, join

import aiohttp
import yaml
from aiohttp import web

# TODO: Make openapi spec for everything

# TODO: Repo lives both on client and on server. Determine either A) Best way to
# rectify differences or B) Only have the code on one and pass stuff between
# each other

# TODO: Parameter validation


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


async def send_analysis_report():
    pass


def prepopulate_incident_store():
    """For demo, populate store with already solved examples"""
    pass


def user_gives_which_repo_and_branch(params):
    """
    params (json):
    - repo: The repo to look at
    - program: 'git' | 'svn' | etc... (let's only support git for now)
    - branch: Duh
    """

    # TODO: Clone the repo locally on the server

    pass


def user_gives_service_which_incident_to_solve(params):
    # TODO: Make a streaming version

    """
    Will need to cache the incident result so that the user, when it accepts
    or rejects it knows what the heck the user is referencing

    Stateful, stores it

    params (json):
    - some identifier of the incident that we are looking at

    return (json):
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
app.router.add_post("/generate_prompt", generate_prompt)
app.router.add_route("*", "/proxy", proxy_handler)

if __name__ == "__main__":
    # TODO: Remove after demo
    prepopulate_incident_store()

    web.run_app(app)

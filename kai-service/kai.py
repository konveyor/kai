#!/usr/bin/python3

"""This module is intended to facilitate using Konveyor with LLMs."""

import os
import warnings
import aiohttp
import yaml

from aiohttp import web

def load_config():
    """Load the configuration from a yaml conf file."""
    config = "/usr/local/etc/kai.conf"
    if os.environ.get('KAI_CONFIG'):
        config = os.environ.get('KAI_CONFIG')

    with open(config, "r", encoding="utf-8") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None

def load_templates():
    """Get model templates from the loaded configuration."""
    return load_config()['model_templates']

def load_template(model_name):
    """Loads the requested template."""
    model_templates = load_templates()
    if model_name in model_templates:
        return model_templates[model_name]

    warnings.warn("Warning: Model not found, using default (first) model from kai.conf")
    return list(model_templates.items())[0][1]

async def generate_prompt(request):
    """Generates a prompt based on input using the specified template."""
    try:
        data = await request.json()

        language = data.get('language', '')
        issue_description = data.get('issue_description', '')
        example_original_code = data.get('example_original_code', '')
        example_solved_code = data.get('example_solved_code', '')
        current_original_code = data.get('current_original_code', '')
        model_template = data.get('model_template', '')

        if model_template == '':
            warnings.warn("Model template not specified. For best results specify a model template.")

        response = load_template(model_template).format(language=language,
                                                        issue_description=issue_description,
                                                        example_original_code=example_original_code,
                                                        example_solved_code=example_solved_code,
                                                        current_original_code=current_original_code,
                                                        model_template=model_template)

        warnings.resetwarnings()
        return web.json_response({'generated_prompt': response})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=400)

async def proxy_handler(request):
    """Proxies a streaming request to an LLM."""
    upstream_url = request.query.get('upstream_url')

    if not upstream_url:
        return web.Response(status=400, text="Missing 'upstream_url' parameter in the request")

    headers = {}
    if request.headers.get('Authorization'):
        headers.update({ 'Authorization': request.headers.get('Authorization') })
    if request.headers.get('Content-Type'):
        headers.update({ 'Content-Type': request.headers.get('Content-Type') })
    method = request.method
    data = await request.read()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(method, upstream_url, headers=headers, data=data) as upstream_response:
                if 'chunked' in upstream_response.headers.get('Transfer-Encoding', ''):
                    response = web.StreamResponse()
                    await response.prepare(request)

                    async for data in upstream_response.content.iter_any():
                        await response.write(data)

                    await response.write_eof()
                    return response

                return web.Response(
                    status=upstream_response.status,
                    text=await upstream_response.text(),
                    headers=upstream_response.headers
                )
        except aiohttp.ClientError as e:
            return web.Response(status=500, text=f"Error connecting to upstream service: {str(e)}")

app = web.Application()
app.router.add_post('/generate_prompt', generate_prompt)
app.router.add_route('*', '/proxy', proxy_handler)

if __name__ == '__main__':
    web.run_app(app)

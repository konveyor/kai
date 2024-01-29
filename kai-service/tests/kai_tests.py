""" Test for kai.py."""
import os
import pytest

from aiohttp import web

import kai

os.environ['KAI_CONFIG'] = "tests/kai_tests.conf"

@pytest.fixture
def cli(event_loop, aiohttp_client):
    """Start server to listen for test connections."""
    app = web.Application()
    app.router.add_post('/generate_prompt', kai.generate_prompt)
    app.router.add_route('*', '/proxy', kai.proxy_handler)
    return event_loop.run_until_complete(aiohttp_client(app))

@pytest.mark.asyncio
async def test_set_value(cli):
    """Test a template renders properly."""
    resp = await cli.post('/generate_prompt', headers={"Content-Type": "application/json"},
                                              data=b"""{"issue_description": "description",
                                                      "language": "go",
                                                      "example_original_code": "my original code",
                                                      "example_solved_code": "my solved example",
                                                      "current_original_code": "my current issue code",
                                                      "model_template": "gpt"}""")

    print(await resp.read())
    print(os.environ.get('KAI_CONFIG'))
    assert resp.status == 200
    assert await resp.text() == '{"generated_prompt": "My Prompt description go my original code my solved example my current issue code"}'

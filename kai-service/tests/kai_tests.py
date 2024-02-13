""" Test for kai.py."""

import os

import pytest
from aiohttp import web

import kai

os.environ["KAI_CONFIG_PREFIX"] = "tests"


@pytest.fixture
def cli(event_loop, aiohttp_client):
    """Start server to listen for test connections."""
    app = web.Application()
    app.router.add_post("/generate_prompt", kai.generate_prompt)
    app.router.add_route("*", "/proxy", kai.proxy_handler)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio
async def test_set_value(cli):
    """Test a template renders properly."""
    resp = await cli.post(
        "/generate_prompt",
        headers={"Content-Type": "application/json"},
        data=b"""{"issue_description": "description",
                                                      "language": "go",
                                                      "example_original_code": "my original code",
                                                      "example_solved_code": "my solved example",
                                                      "current_original_code": "my current issue code",
                                                      "model_template": "gpt"}""",
    )

    assert resp.status == 200
    assert (
        await resp.text()
        == '{"generated_prompt": "My Prompt description go my original code my solved example my current issue code"}'
    )


@pytest.mark.asyncio
async def test_set_value2(cli):
    """Test a second template renders properly."""
    resp = await cli.post(
        "/generate_prompt",
        headers={"Content-Type": "application/json"},
        data=b"""{"issue_description": "description",
                                                      "language": "go",
                                                      "example_original_code": "my original code",
                                                      "example_solved_code": "my solved example",
                                                      "current_original_code": "my current issue code",
                                                      "model_template": "alpaca"}""",
    )

    assert resp.status == 200
    assert (
        await resp.text()
        == '{"generated_prompt": "My Alpaca Prompt description go my original code my solved example my current issue code"}'
    )


def test_model_len():
    """Test how many models are loaded"""
    t = kai.load_templates()
    assert len(t) == 2
    assert "gpt" in t
    assert "alpaca" in t

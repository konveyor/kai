"""Governed prompt templates for the solution server (ISO 42001 A.5.2).

Prompts live as individual Jinja2 assets under ``templates/`` and are rendered
through :func:`render_prompt`. They are versioned and validated independently of
the application code; see ``manifest.yaml`` and ``PROMPT_GOVERNANCE.md``.
"""

from __future__ import annotations

from functools import lru_cache

from jinja2 import Environment, PackageLoader, StrictUndefined, Template

# One id per governed prompt -> its template filename.
_TEMPLATES: dict[str, str] = {
    "generate_hint_v3": "generate_hint_v3.md.jinja",
}

# autoescape is intentionally off: these are plain-text LLM prompts, not HTML, so
# HTML-escaping would corrupt code snippets in the rendered prompt (B701 N/A).
# keep_trailing_newline preserves the template's final newline verbatim;
# StrictUndefined makes a missing context variable fail loudly.
_env = Environment(  # nosec B701
    loader=PackageLoader("kai_mcp_solution_server", "prompts/templates"),
    autoescape=False,
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


@lru_cache(maxsize=None)
def _template(filename: str) -> Template:
    return _env.get_template(filename)


def render_prompt(prompt_id: str, /, **context: object) -> str:
    """Render a governed prompt template to its final string."""
    try:
        filename = _TEMPLATES[prompt_id]
    except KeyError:
        raise KeyError(f"Unknown prompt id: {prompt_id!r}") from None
    return _template(filename).render(**context)

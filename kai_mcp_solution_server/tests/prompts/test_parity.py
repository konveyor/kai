"""Byte-exact parity: the Jinja template must reproduce the original prompt
string exactly, across the full incident/ast-diff matrix."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from kai_mcp_solution_server.prompts import render_prompt

from .oracle import oracle_generate_hint_v3


def _incident(
    uri: str = "file:///src/Foo.java",
    message: str = "javax.* must become jakarta.*",
    code_snip: str = "import javax.persistence.Entity;",
    line_number: int = 12,
    variables: object = None,
    ruleset_name: str = "javax-to-jakarta",
    violation_name: str = "javax-import",
) -> SimpleNamespace:
    if variables is None:
        variables = {"kind": "import"}
    return SimpleNamespace(
        uri=uri,
        message=message,
        code_snip=code_snip,
        line_number=line_number,
        variables=variables,
        violation=SimpleNamespace(
            ruleset_name=ruleset_name, violation_name=violation_name
        ),
    )


_AST_DIFF = (
    "class Foo {\n-  @javax.persistence.Entity\n+  @jakarta.persistence.Entity\n}"
)

_CASES = {
    "0 incidents, empty ast": ([], ""),
    "1 incident, empty ast": ([_incident()], ""),
    "1 incident, populated ast": ([_incident()], _AST_DIFF),
    "N incidents, populated ast": (
        [
            _incident(),
            _incident(
                uri="file:///src/Bar.java",
                message="multi\nline\nmessage",
                code_snip="line1\nline2",
                line_number=99,
                variables={"a": 1, "b": ["x", "y"]},
                violation_name="ejb-usage",
            ),
            _incident(message="special <>&\"' chars", variables=None),
        ],
        _AST_DIFF,
    ),
}


@pytest.mark.parametrize("name", list(_CASES))
def test_v3_renders_byte_identical_to_oracle(name: str) -> None:
    incidents, ast_diff_str = _CASES[name]
    rendered = render_prompt(
        "generate_hint_v3", incidents=incidents, ast_diff_str=ast_diff_str
    )
    assert rendered == oracle_generate_hint_v3(incidents, ast_diff_str)


def test_unknown_prompt_id_raises() -> None:
    with pytest.raises(KeyError):
        render_prompt("does-not-exist")

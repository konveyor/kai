"""Deterministic (mock-model) semantic regression.

Renders the hint prompt against a baseline of migration scenarios and asserts the
scaffolding a model needs to produce a usable hint survives any wording change:
the output-format contract, every incident's identifying fields, and the AST diff.
No live model is involved.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from kai_mcp_solution_server.prompts import render_prompt

_OUTPUT_CONTRACT = [
    "IMPORTANT: Follow this EXACT output format:",
    "SUMMARY:",
    "HINT:",
    "Incidents:",
    "AST Diff:",
]


def _incident(uri: str, message: str, violation_name: str) -> SimpleNamespace:
    return SimpleNamespace(
        uri=uri,
        message=message,
        code_snip="import javax.persistence.Entity;",
        line_number=1,
        variables={"kind": "import"},
        violation=SimpleNamespace(
            ruleset_name="javax-to-jakarta", violation_name=violation_name
        ),
    )


_BASELINE = {
    "javaee->quarkus": (
        [
            _incident(
                "file:///Foo.java",
                "Replace javax.persistence with jakarta.persistence",
                "javax-import",
            )
        ],
        "class Foo {\n-  @javax.persistence.Entity\n+  @jakarta.persistence.Entity\n}",
    ),
    "multi-incident": (
        [
            _incident("file:///A.java", "Remove EJB usage", "ejb-usage"),
            _incident("file:///B.java", "Migrate persistence.xml", "persistence-xml"),
        ],
        "class A {}\n\nclass B {}",
    ),
}


@pytest.mark.parametrize("name", list(_BASELINE))
def test_v3_preserves_migration_scaffolding(name: str) -> None:
    incidents, ast_diff_str = _BASELINE[name]
    rendered = render_prompt(
        "generate_hint_v3", incidents=incidents, ast_diff_str=ast_diff_str
    )

    for anchor in _OUTPUT_CONTRACT:
        assert anchor in rendered, f"missing output-contract anchor: {anchor!r}"
    for incident in incidents:
        assert incident.uri in rendered
        assert incident.message in rendered
        assert incident.code_snip in rendered
        assert str(incident.line_number) in rendered
        assert str(incident.variables) in rendered
        assert incident.violation.violation_name in rendered
    assert ast_diff_str in rendered

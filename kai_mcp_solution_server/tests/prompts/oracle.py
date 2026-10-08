"""Parity oracle — the byte-exact baseline for the prompt-template migration.

This is a VERBATIM copy of the ``generate_hint_v3`` prompt-building logic as it
existed inline in ``server.py`` immediately before extraction. The parity suite
asserts that ``render_prompt("generate_hint_v3", ...)`` reproduces this string
byte-for-byte. Do not "clean up" anything here — quirks (the ``-   `` triple
space before the violation name, the trailing blank line) are intentional and
are exactly what the template must reproduce.
"""

from __future__ import annotations

from typing import Any


def oracle_generate_hint_v3(incidents: list[Any], ast_diff_str: str) -> str:
    prompt = (
        "The following incidents had this accepted solution. "
        "Use the AST diffs below as a guiding pattern for migration.\n\n"
        "Generate a hint for the user so that they can migrate the code.\n\n"
        "IMPORTANT: Follow this EXACT output format:\n"
        "---\n"
        "SUMMARY:\n"
        "[concise summary of necessary changes]\n\n"
        "HINT:\n"
        "[numbered steps with generic, reusable code examples]\n"
        "---\n\n"
        "Guidelines for high-quality response:\n"
        "1. Keep SUMMARY concise and focused\n"
        "2. Use numbered steps (1, 2, 3) in HINT section\n"
        "3. Provide generic before/after code examples that can be reused and mark them as examples (e.g. 'Example 1: Before: ... After: ...')\n"
        "4. Write in direct, actionable tone\n"
        "Incidents:\n"
    )

    for i, incident in enumerate(incidents):
        prompt += (
            f"Incident {i + 1}:\n"
            f"  URI: {incident.uri}\n"
            f"  Message: {incident.message}\n"
            f"  Code Snippet: {incident.code_snip}\n"
            f"  Line Number: {incident.line_number}\n"
            f"  Variables: {incident.variables}\n"
            f"  Violation: {incident.violation.ruleset_name} - "
            f"  {incident.violation.violation_name}\n\n"
        )

    prompt += f"AST Diff:\n{ast_diff_str}\n\n"
    return prompt

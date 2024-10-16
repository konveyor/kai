from __future__ import annotations

import os
from enum import StrEnum
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import AliasChoices, BaseModel, Field, RootModel

"""
Report types ripped straight from analyzer-lsp.
"""


class Category(StrEnum):
    POTENTIAL = "potential"
    OPTIONAL = "optional"
    MANDATORY = "mandatory"


class Incident(BaseModel):
    """
    An Incident is a specific instance of a rule being violated.
    """

    # NOTE: `str` is the best equivalent of Go's `json.RawMessage`
    uri: str

    # Explanation of the incident
    message: str = Field(
        ..., validation_alias=AliasChoices("message", "analysis_message")
    )

    # NOTE: Why camelCase for these ones? :weary: - JonahSussman
    code_snip: str = Field(
        "",
        validation_alias=AliasChoices("code_snip", "codeSnip", "incident_snip"),
        serialization_alias="codeSnip",
    )

    # 0-indexed line number
    line_number: int = Field(
        -1,
        validation_alias=AliasChoices("line_number", "lineNumber"),
        serialization_alias="lineNumber",
    )

    variables: dict[str, Any] = Field(
        {}, validation_alias=AliasChoices("variables", "incident_variables")
    )


class ExtendedIncident(Incident):
    """
    An Incident with extra metadata.
    """

    ruleset_name: str
    ruleset_description: Optional[str] = None

    violation_name: str
    violation_description: Optional[str] = None
    violation_category: Category = Category.POTENTIAL
    violation_labels: list[str] = []


class Link(BaseModel):
    """
    Link defines an external hyperlink.
    """

    url: str

    # Title optional description
    title: str = ""


class Violation(BaseModel):
    """
    A Violation is a specific rule being broken, i.e. a rule being "violated".
    It may have many different incidents throughout the codebase.
    """

    # Description text description about the violation
    description: str = ""

    # Category category of the violation
    category: Category = Category.POTENTIAL

    # Labels list of labels for the violation
    labels: list[str] = []

    # Incidents list of instances of violation found
    incidents: list[Incident] = []

    # ExternalLinks hyperlinks to external sources of docs, fixes, etc.
    links: list[Link] = []

    # Extras reserved for additional data
    # NOTE: `str` is the best equivalent of Go's `json.RawMessage`
    extras: Optional[str] = None

    # Effort defines expected story points for this incident
    effort: Optional[int] = None


class RuleSet(BaseModel):
    """
    A RuleSet is a collection of rules that are evaluated together. It different
    data on its rules: which rules were unmatched, which rules where skipped,
    and which rules generated errors or violations.
    """

    # Name is a name for the ruleset.
    name: Optional[str] = None

    # Description text description for the ruleset.
    description: str = ""

    # Tags list of generated tags from the rules in this ruleset.
    tags: Optional[list[str]] = None

    # Violations is a map containing violations generated for the matched rules
    # in this ruleset. Keys are rule IDs, values are their respective generated
    # violations.
    violations: dict[str, Violation] = {}

    # Errors is a map containing errors generated during evaluation of rules in
    # this ruleset. Keys are rule IDs, values are their respective generated
    # errors.
    errors: Optional[dict[str, str]] = None

    # Unmatched is a list of rule IDs of the rules that weren't matched.
    unmatched: Optional[list[str]] = None

    # Skipped is a list of rule IDs that were skipped
    skipped: Optional[list[str]] = None


class AnalysisReport(RootModel[list[RuleSet]]):
    """
    An analysis report is simply a list of rule sets.
    """

    root: list[RuleSet] = Field(..., title="AnalysisReport")


def generate_json_schema():
    main_model_schema = AnalysisReport.model_json_schema()

    file_name = Path(os.path.dirname(__file__)) / "report_types.yaml"

    # delete report_types.yaml if it exists
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "w") as f:
        f.write(yaml.dump(main_model_schema))


if __name__ == "__main__":
    generate_json_schema()

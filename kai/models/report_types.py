from __future__ import annotations

import os
from enum import StrEnum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import AliasChoices, BaseModel, Field, RootModel


class Category(StrEnum):
    potential = "potential"
    optional = "optional"
    mandatory = "mandatory"


class Incident(BaseModel):
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

    variables: Dict[str, Any] = Field(
        {}, validation_alias=AliasChoices("variables", "incident_variables")
    )


class ExtendedIncident(Incident):
    """
    A "flattened" incident, containing its ruleset and violation names.
    """

    ruleset_name: str
    ruleset_description: Optional[str] = None
    violation_name: str
    violation_description: Optional[str] = None


# Link defines an external hyperlink
class Link(BaseModel):
    url: str

    # Title optional description
    title: str = ""


class Violation(BaseModel):
    # Description text description about the violation
    description: str = ""

    # Category category of the violation
    category: Category = "potential"

    # Labels list of labels for the violation
    labels: List[str] = []

    # Incidents list of instances of violation found
    incidents: List[Incident] = []

    # ExternalLinks hyperlinks to external sources of docs, fixes, etc.
    links: List[Link] = []

    # Extras reserved for additional data
    # NOTE: `str` is the best equivalent of Go's `json.RawMessage`
    extras: Optional[str] = None

    # Effort defines expected story points for this incident
    effort: Optional[int] = None


class RuleSet(BaseModel):
    # Name is a name for the ruleset.
    name: Optional[str] = None

    # Description text description for the ruleset.
    description: str = ""

    # Tags list of generated tags from the rules in this ruleset.
    tags: Optional[List[str]] = None

    # Violations is a map containing violations generated for the matched rules
    # in this ruleset. Keys are rule IDs, values are their respective generated
    # violations.
    violations: Dict[str, Violation] = {}

    # Errors is a map containing errors generated during evaluation of rules in
    # this ruleset. Keys are rule IDs, values are their respective generated
    # errors.
    errors: Optional[Dict[str, str]] = None

    # Unmatched is a list of rule IDs of the rules that weren't matched.
    unmatched: Optional[List[str]] = None

    # Skipped is a list of rule IDs that were skipped
    skipped: Optional[List[str]] = None


class AnalysisReport(RootModel[List[RuleSet]]):
    root: List[RuleSet] = Field(..., title="AnalysisReport")


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

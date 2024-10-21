from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
from collections.abc import KeysView
from enum import StrEnum
from io import StringIO, TextIOWrapper
from pathlib import Path
from typing import Any, Iterator, Optional
from urllib.parse import urlparse

import yaml
from pydantic import AliasChoices, BaseModel, Field, RootModel
from kai.logging.kai_logging import get_logger

KAI_LOG = get_logger(__name__)


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


def generate_json_schema() -> None:
    main_model_schema = AnalysisReport.model_json_schema()

    file_name = Path(os.path.dirname(__file__)) / "report_types.yaml"

    # delete report_types.yaml if it exists
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "w") as f:
        f.write(yaml.dump(main_model_schema))


class Report:
    def __init__(
        self, report_data: dict[str, Any] | list[dict[str, Any]], report_id: str
    ) -> None:
        self.workaround_counter_for_missing_ruleset_name = 0
        self.report_id = report_id
        self.rulesets: dict[str, RuleSet] = {}

        if isinstance(report_data, dict):
            self.add_ruleset(report_data)
        else:
            for ruleset in report_data:
                self.add_ruleset(ruleset)

    def __str__(self) -> str:
        return str(self.rulesets)

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, key: str) -> RuleSet:
        return self.rulesets[key]

    def keys(self) -> KeysView[str]:
        return self.rulesets.keys()

    def __iter__(self) -> Iterator[str]:
        return iter(self.rulesets)

    def __len__(self) -> int:
        return len(self.rulesets)

    @classmethod
    def load_report_from_object(
        cls, report_data: dict[str, Any] | list[dict[str, Any]], report_id: str
    ) -> "Report":
        return cls(report_data=report_data, report_id=report_id)

    @classmethod
    def load_report_from_file(cls, file_name: str | pathlib.Path) -> "Report":
        with open(file_name, "r") as f:
            report: dict[str, Any] = yaml.safe_load(f)
        report_data = report

        # report_id is the hash of the json.dumps of the report_data
        return cls(
            report_data,
            hashlib.sha256(
                json.dumps(report_data, sort_keys=True).encode()
            ).hexdigest(),
        )

    def add_ruleset(self, ruleset_dict: dict[str, Any]) -> None:
        if "name" not in ruleset_dict:
            ruleset_dict["name"] = (
                f"Unnamed ruleset {self.workaround_counter_for_missing_ruleset_name}"
            )
            self.workaround_counter_for_missing_ruleset_name += 1

        ruleset = RuleSet.model_validate(ruleset_dict)
        if ruleset.name:
            self.rulesets[ruleset.name] = ruleset

    def get_impacted_files(self) -> dict[pathlib.Path, list[ExtendedIncident]]:
        impacted_files: dict[pathlib.Path, list[ExtendedIncident]] = {}

        for ruleset_name, ruleset in self.rulesets.items():
            for violation_name, violation in ruleset.violations.items():
                for incident in violation.incidents:
                    if self.should_we_skip_incident(incident):
                        continue

                    file_path = remove_known_prefixes(urlparse(incident.uri).path)
                    if file_path.startswith("root/.m2/"):
                        ## Workaround for bug found in Kantra 0.5.0
                        ## See:  https://github.com/konveyor/kantra/issues/321
                        ## Extra files are being reported in the analysis
                        ## from the dependencies.
                        ## We will skip these files for now.
                        continue

                    current_entry = ExtendedIncident.model_validate(
                        {
                            "uri": incident.uri,
                            "message": incident.message,
                            "codeSnip": incident.code_snip,
                            "lineNumber": incident.line_number,
                            "variables": incident.variables,
                            "ruleset_name": ruleset_name,
                            "violation_name": violation_name,
                            "ruleset_description": ruleset.description,
                            "violation_description": violation.description,
                        }
                    )

                    file_path_as_path = Path(file_path)
                    if impacted_files.get(file_path_as_path) is None:
                        impacted_files[file_path_as_path] = []

                    impacted_files[file_path_as_path].append(current_entry)

        return impacted_files

    def write_markdown(self, output_dir: str) -> None:
        # We will create a single directory per source app where each ruleset
        # with data is in its own file
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as error:
            KAI_LOG.error(f"Error creating directory {output_dir}: {error}")
            raise error

        # Iterate through each Ruleset that has data. Write a separate file per
        # ruleset
        for ruleset_name, ruleset in self.rulesets.items():
            ruleset_name_display = ruleset_name.replace("/", "_")

            with open(f"{output_dir}/{ruleset_name_display}.md", "w") as f:
                # We want to start each run with a clean file
                f.truncate(0)
                buffer = StringIO()
                self._write_markdown_snippet(ruleset_name, ruleset, buffer)
                buffer.seek(0)
                shutil.copyfileobj(buffer, f)
                KAI_LOG.info(
                    f"Writing {ruleset_name} to {output_dir}/{ruleset_name_display}.md"
                )
                buffer.close()

    # TODO: Migrate to a jinja template
    def _write_markdown_snippet(
        self, ruleset_name: str, ruleset: RuleSet, f: TextIOWrapper
    ) -> None:
        f.write(f"# {ruleset_name}\n")
        f.write("## Description\n")
        f.write(f"{ruleset.description}\n")
        f.write(
            "* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated\n"
        )
        f.write("## Violations\n")
        f.write(f"Number of Violations: {len(ruleset.violations)}\n")

        for count, (key, items) in enumerate(ruleset.violations.items()):
            f.write(f"### #{count} - {key}\n")
            # Break out below for violation. Then we can weave in an example
            # perhaps?
            #
            # Or should there be a Markdown class that is responsible for
            # blending:
            #   - Report
            #   - Per Violation create a prompt/run/example

            f.write(f"* Category: {items.category}\n")
            if items.effort is not None:
                f.write(f"* Effort: {items.effort}\n")
            f.write(f"* Description: {items.description}\n")
            if items.labels:
                f.write(f"* Labels: {', '.join(items.labels)}\n")
            if items.links:
                f.write("* Links\n")
                for link in items.links:
                    f.write(f"  * {link.title}: {link.url}\n")
            if items.incidents:
                f.write("* Incidents\n")
                for incident in items.incidents:
                    # Possible keys of 'uri', 'message', 'codeSnip'
                    if incident.uri:
                        f.write(f"  * {incident.uri}\n")
                    if incident.line_number:
                        f.write(f"      * Line Number: {incident.line_number}\n")
                    if incident.message and incident.message.strip() != "":
                        f.write(f"      * Message: '{incident.message.strip()}'\n")
                    if incident.code_snip:
                        f.write("      * Code Snippet:\n")
                        f.write("```java\n")
                        f.write(f"{incident.code_snip}\n")
                        f.write("```\n")

    def get_violation_snippet(self, ruleset_name: str, violation_name: str) -> None:
        ruleset = self.rulesets[ruleset_name]
        # violation = ruleset.violations[violation_name]

        buffer = StringIO()
        buffer.write(f"# {ruleset_name}\n")
        buffer.write("## Description\n")
        buffer.write(f"{ruleset.description}\n")
        buffer.write("* Source of rules:")

    def should_we_skip_incident(self, incident: Incident) -> bool:
        """
        Filter out known issues
        """

        file_path = remove_known_prefixes(urlparse(incident.uri).path)

        if file_path.startswith("target/"):
            # Skip any incident that begins with 'target/'
            # Related to: https://github.com/konveyor/analyzer-lsp/issues/358
            return True

        if file_path.endswith(".svg"):
            # See https://github.com/konveyor/rulesets/issues/41
            return True

        return False


# These prefixes are sometimes in front of the paths, strip them.
# Also strip leading slashes since os.path.join can't join two absolute paths

KNOWN_PREFIXES = (
    "/opt/input/source/",
    # trunk-ignore(bandit/B108)
    "/tmp/source-code/",
    "/addon/source/",
    "/",
)


# These are known unique variables that can be included by incidents
# They would prevent matches that we actually want, so we filter them
# before adding to the database or searching
FILTERED_INCIDENT_VARS = [
    "file",  # Java, URI of the offending file
    "package",  # Java, shows the package
    "name",  # Java, shows the name of the method that caused the incident
]


def remove_known_prefixes(path: str) -> str:
    for prefix in KNOWN_PREFIXES:
        if path.startswith(prefix):
            return path.removeprefix(prefix)
    return path


def filter_incident_vars(incident_vars: dict[str, Any]) -> dict[str, Any]:
    for v in FILTERED_INCIDENT_VARS:
        incident_vars.pop(v, None)
    return incident_vars


if __name__ == "__main__":
    generate_json_schema()

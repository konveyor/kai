import hashlib
import json
import logging
import os
import pathlib
import shutil
from io import StringIO, TextIOWrapper
from urllib.parse import urlparse

import yaml

from kai.models.report_types import ExtendedIncident, Incident, RuleSet
from kai.models.util import remove_known_prefixes

KAI_LOG = logging.getLogger(__name__)


class Report:
    def __init__(self, report_data: dict | list[dict], report_id: str):
        self.workaround_counter_for_missing_ruleset_name = 0
        self.report_id = report_id
        self.rulesets: dict[str, RuleSet] = {}

        if isinstance(report_data, dict):
            self.add_ruleset(report_data)
        else:
            for ruleset in report_data:
                self.add_ruleset(ruleset)

    def __str__(self):
        return str(self.rulesets)

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.rulesets[key]

    def keys(self):
        return self.rulesets.keys()

    def __iter__(self):
        return iter(self.rulesets)

    def __len__(self):
        return len(self.rulesets)

    @classmethod
    def load_report_from_object(cls, report_data: dict | list[dict], report_id: str):
        return cls(report_data=report_data, report_id=report_id)

    @classmethod
    def load_report_from_file(cls, file_name: str | pathlib.Path):
        with open(file_name, "r") as f:
            report: dict = yaml.safe_load(f)
        report_data = report

        # report_id is the hash of the json.dumps of the report_data
        return cls(
            report_data,
            hashlib.sha256(
                json.dumps(report_data, sort_keys=True).encode()
            ).hexdigest(),
        )

    def add_ruleset(self, ruleset_dict: dict):
        ruleset = RuleSet.model_validate(ruleset_dict)

        if ruleset.name is None:
            ruleset.name = (
                f"Unnamed ruleset {self.workaround_counter_for_missing_ruleset_name}"
            )
            self.workaround_counter_for_missing_ruleset_name += 1

        self.rulesets[ruleset.name] = ruleset

    def get_impacted_files(self) -> dict[pathlib.Path, list[ExtendedIncident]]:
        impacted_files: dict[pathlib.Path, list[ExtendedIncident]] = {}

        for ruleset_name, ruleset in self.rulesets.items():
            for violation_name, violation in ruleset.violations.items():
                for incident in violation.incidents:
                    if self.should_we_skip_incident(incident):
                        continue

                    file_path = pathlib.Path(
                        remove_known_prefixes(urlparse(incident.uri).path)
                    )
                    if str(file_path).startswith("root/.m2/"):
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

                    if impacted_files.get(file_path) is None:
                        impacted_files[file_path] = []

                    impacted_files[file_path].append(current_entry)

        return impacted_files

    def write_markdown(self, output_dir: str):
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
    ):
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

    def get_violation_snippet(self, ruleset_name: str, violation_name: str):
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

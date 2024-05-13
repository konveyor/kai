__all__ = ["Report"]

import os
import shutil
from io import StringIO

import yaml

from kai.kai_logging import KAI_LOG


class Report:
    report = {}

    def __init__(self, report_data: dict):
        self.workaround_counter_for_missing_ruleset_name = 0
        self.report = self._reformat_report(report_data)

    def __str__(self):
        return str(self.report)

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.report[key]

    def keys(self):
        return self.report.keys()

    def __iter__(self):
        return iter(self.report)

    def __len__(self):
        return len(self.report)

    @classmethod
    def load_report_from_object(cls, report_data: dict):
        """
        Class method to create a Report instance directly from a Python dictionary object.
        """
        return cls(report_data=report_data)

    @classmethod
    def load_report_from_file(cls, file_name: str):
        KAI_LOG.info(f"Reading report from {file_name}")
        with open(file_name, "r") as f:
            report: dict = yaml.safe_load(f)
        report_data = report
        return cls(report_data)

    @staticmethod
    def get_cleaned_file_path(uri: str):
        file_path = uri.replace("file:///tmp/source-code/", "")
        return file_path

    def get_impacted_files(self):
        """
        Return a dictionary of impacted files:
            key = file path
            value = list of violations
        """
        impacted_files = dict()
        # key = file_path
        # value = list of violations
        for ruleset_name in self.report.keys():
            ruleset = self.report[ruleset_name]
            # We iterate over each ruleset
            for violation_name in ruleset["violations"].keys():
                violation = ruleset["violations"][violation_name]
                # We look at each violation
                for incid in violation["incidents"]:
                    if "uri" in incid:
                        if not self.should_we_skip_incident(incid):
                            file_path = Report.get_cleaned_file_path(incid["uri"])
                            current_entry = {
                                "ruleset_name": ruleset_name,
                                "violation_name": violation_name,
                                "ruleset_description": ruleset.get("description", ""),
                                "violation_description": violation.get(
                                    "description", ""
                                ),
                                "message": incid.get("message", ""),
                                "codeSnip": incid.get("codeSnip", ""),
                                "lineNumber": incid.get("lineNumber", ""),
                                "variables": incid.get("variables", {}),
                            }
                            if impacted_files.get(file_path) is None:
                                impacted_files[file_path] = []
                            impacted_files[file_path].append(current_entry)
        return impacted_files

    def _reformat_report(self, report: dict):
        new_report = {}
        # Reformat from a List to a Dict where the key is the name
        if isinstance(report, list):
            for item in report:
                if "violations" in item.keys():
                    # Only add entries that have Violations
                    ruleset_name = self._get_ruleset_name(item)
                    new_report[ruleset_name] = item
                # We dropped all rulesests with empty violations
        else:
            new_report = report
        return new_report

    def _get_ruleset_name(self, item):
        # The 'name' of a ruleset is not guaranteed from what I'm seeing in our
        # rulesets.  We need a way to distinguish rulesets if no name is present
        # hence this workaround.
        # See https://github.com/konveyor/rulesets/issues/36 for what motivated
        # this workaround
        name = ""
        if "name" not in item.keys():
            self.workaround_counter_for_missing_ruleset_name += 1
            name = f"mising_ruleset_name_{self.workaround_counter_for_missing_ruleset_name}"
        else:
            name = item["name"]
        return name

    def write_markdown(self, output_dir):
        # We will create a single directory per source app
        # Where each ruleset with data is in its own file
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as error:
            KAI_LOG.error(f"Error creating directory {output_dir}: {error}")
            raise error
        # Iterate through each Ruleset that has data
        # Write a separate file per ruleset
        for ruleset_name in self.report.keys():
            ruleset = self.report[ruleset_name]
            ruleset = ruleset  # FIXME: To stop trunk error
            ruleset_name_display = ruleset_name.replace("/", "_")
            with open(f"{output_dir}/{ruleset_name_display}.md", "w") as f:
                # We want to start each run with a clean file
                f.truncate(0)
                buffer = StringIO()
                self._get_markdown_snippet(ruleset_name, buffer)
                buffer.seek(0)
                shutil.copyfileobj(buffer, f)
                KAI_LOG.info(
                    f"Writing {ruleset_name} to {output_dir}/{ruleset_name_display}.md"
                )
                buffer.close()

    def _get_markdown_snippet(self, ruleset_name, f):
        ruleset = self.report[ruleset_name]
        f.write(f"# {ruleset_name}\n")
        f.write("## Description\n")
        f.write(f"{ruleset.get('description', '')}\n")
        f.write(
            "* Source of rules: https://github.com/konveyor/rulesets/tree/main/default/generated\n"
        )
        f.write("## Violations\n")
        f.write(f"Number of Violations: {len(ruleset['violations'])}\n")
        # counter = 0
        for count, key in enumerate(ruleset["violations"]):
            items = ruleset["violations"][key]
            f.write(f"### #{count} - {key}\n")
            # Break out below for violation
            # Then we can weave in an example perhaps?
            # Or should there be a Markdown class that is responsible for blending
            # . - Report
            # . - Per Violation create a prompt/run/example

            f.write(f"* Category: {items['category']}\n")
            if "effort" in items:
                f.write(f"* Effort: {items['effort']}\n")
            f.write(f"* Description: {items['description']}\n")
            if "labels" in items:
                f.write(f"* Labels: {', '.join(items['labels'])}\n")
            if "links" in items:
                f.write("* Links\n")
                for l in items["links"]:
                    f.write(f"  * {l['title']}: {l['url']}\n")
            if "incidents" in items:
                f.write("* Incidents\n")
                for incid in items["incidents"]:
                    # Possible keys of 'uri', 'message', 'codeSnip'
                    if "uri" in incid:
                        f.write(f"  * {incid['uri']}\n")
                    if "lineNumber" in incid:
                        f.write(f"      * Line Number: {incid['lineNumber']}\n")
                    if "message" in incid and incid["message"].strip() != "":
                        f.write(f"      * Message: '{incid['message'].strip()}'\n")
                    if "codeSnip" in incid:
                        f.write("      * Code Snippet:\n")
                        f.write("```java\n")
                        f.write(f"{incid['codeSnip']}\n")
                        f.write("```\n")

    def get_violation_snippet(self, ruleset_name, violation_name):
        ruleset = self.report[ruleset_name]
        violation = ruleset["violations"][violation_name]
        violation = violation  # FIXME: to please trunk error
        buffer = StringIO()
        buffer.write(f"# {ruleset_name}\n")
        buffer.write("## Description\n")
        buffer.write(f"{ruleset['description']}\n")
        buffer.write("* Source of rules:")

    def should_we_skip_incident(self, incid):
        # Filter out known issues
        file_path = Report.get_cleaned_file_path(incid["uri"])
        if file_path.startswith("target/"):
            # Skip any incident that begins with 'target/'
            # Related to: https://github.com/konveyor/analyzer-lsp/issues/358
            return True
        if file_path.endswith(".svg"):
            # See https://github.com/konveyor/rulesets/issues/41
            return True

#!/usr/bin/env python

import json
import pprint
import sys
from dataclasses import dataclass

import requests

# Ensure that we have 'kai' in our import path
sys.path.append("../../kai")
from kai import Report

SERVER_URL = "http://0.0.0.0:8080"
APP_NAME = "coolstore"
SAMPLE_APP_DIR = "./coolstore"

# TODOs
# 1) Add ConfigFile to tweak the server URL an rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in
# 3) Allow multiple violations to be fixed per request
# 4) Save the updated file to disk


@dataclass
class KaiRequestParams:
    application_name: str
    file_name: str
    file_contents: str
    violation_name: str
    ruleset_name: str
    analysis_message: str
    line_number: int | None = None
    incident_variables: dict | None = None
    incident_snip: str | None = None

    @staticmethod
    def from_incident(
        app_name, file_path, file_contents, incident
    ) -> "KaiRequestParams":
        return KaiRequestParams(
            app_name,
            file_path,
            file_contents,
            incident["violation_name"],
            incident["ruleset_name"],
            incident["message"],
            incident["lineNumber"],  # this may be empty in the report
            incident["variables"],
            "",  # We don't plan to use 'incident_snip'
        )

    def to_json(self):
        return json.dumps(self.__dict__)


def collect_parameters(file_path, violations) -> KaiRequestParams:
    print(f"Collecting parameters for {file_path}")
    with open(f"{SAMPLE_APP_DIR}/{file_path}", "r") as f:
        file_contents = f.read()

    print(f"File contents: {file_contents}")
    # TODO: Update for batching all incidents in a single request to backend
    # Limit to only 1 violation to begin with
    violation = violations[0]

    params = KaiRequestParams.from_incident(
        APP_NAME, file_path, file_contents, violation
    )
    return params


def generate_fix(params: KaiRequestParams):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    response = requests.post(
        f"{SERVER_URL}/get_incident_solution",
        data=params.to_json(),
        headers=headers,
        timeout=600,
    )
    return response


def parse_response(response):
    return ""


def run_demo(report):
    impacted_files = report.get_impacted_files()
    for file_path, violations in impacted_files.items():
        # Gather the info we need to send to the REST API
        params = collect_parameters(file_path, violations)
        print("Sending request data:")
        pprint.pprint(params.to_json())
        ####
        ## Call Kai
        #####
        response = generate_fix(params)
        print(f"\nResponse StatusCode: {response.status_code}\n")
        print("Response:")
        pprint.pprint(response.json())
        # Parse the Output
        # updated_file_contents = parse_response(response)
        # Write it to Disk
        return


if __name__ == "__main__":
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report(coolstore_analysis_dir)
    run_demo(r)

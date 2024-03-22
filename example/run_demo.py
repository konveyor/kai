#!/usr/bin/env python

import json
import sys
from dataclasses import asdict, dataclass

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
# 3) Save the updated file to disk


@dataclass
class KaiIncident:
    violation_name: str
    ruleset_name: str
    analysis_message: str
    line_number: int | None = None
    incident_variables: dict | None = None
    incident_snip: str | None = None

    @staticmethod
    def from_incident(incident) -> "KaiIncident":
        return KaiIncident(
            incident["violation_name"],
            incident["ruleset_name"],
            incident["message"],
            incident["lineNumber"],  # this may be empty in the report
            incident["variables"],
            "",  # We don't plan to use 'incident_snip'
        )


@dataclass
class KaiRequestParams:
    application_name: str
    file_name: str
    file_contents: str
    incidents: list[KaiIncident]

    @staticmethod
    def from_incidents(
        app_name, file_path, file_contents, incidents
    ) -> "KaiRequestParams":
        kai_incidents = []
        for incident in incidents:
            kai_incidents.append(KaiIncident.from_incident(incident))
        return KaiRequestParams(app_name, file_path, file_contents, kai_incidents)

    def to_json(self):
        return json.dumps(asdict(self))


def collect_parameters(file_path, violations) -> KaiRequestParams:
    with open(f"{SAMPLE_APP_DIR}/{file_path}", "r") as f:
        file_contents = f.read()

    params = KaiRequestParams.from_incidents(
        APP_NAME, file_path, file_contents, violations
    )
    return params


def generate_fix(params: KaiRequestParams):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    response = requests.post(
        # f"{SERVER_URL}/get_incident_solution",
        f"{SERVER_URL}/get_incident_solutions_for_file",
        data=params.to_json(),
        headers=headers,
        timeout=600,
    )
    return response


def parse_response(response):
    return ""


def run_demo(report):
    impacted_files = report.get_impacted_files()
    num_impacted_files = len(impacted_files)
    # Quick loop to find the total number of violations
    total_violations = 0
    for _, violations in impacted_files.items():
        total_violations += len(violations)
    print(f"{num_impacted_files} files with a total of {total_violations} violations.")

    count = 1
    for file_path, violations in impacted_files.items():
        print(
            f"File #{count} of {num_impacted_files} - Processing {file_path} which has {len(violations)} violations"
        )
        # Gather the info we need to send to the REST API
        params = collect_parameters(file_path, violations)
        ####
        ## Call Kai
        #####
        response = generate_fix(params)
        print(f"\nResponse StatusCode: {response.status_code} for {file_path}\n")
        # Parse the Output
        # updated_file_contents = parse_response(response)
        # Write it to Disk
        count += 1


if __name__ == "__main__":
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report(coolstore_analysis_dir)
    run_demo(r)

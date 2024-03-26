#!/usr/bin/env python

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass

import requests

# Ensure that we have 'kai' in our import path
sys.path.append("../../kai")
from kai import Report
from kai.kai_logging import KAI_LOG

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


def _generate_fix(params: KaiRequestParams):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    ## We will timeout in 10 minutes if we do not receive a reply
    response = requests.post(
        # f"{SERVER_URL}/get_incident_solution",
        f"{SERVER_URL}/get_incident_solutions_for_file",
        data=params.to_json(),
        headers=headers,
        timeout=2400,
    )
    return response


def generate_fix(params: KaiRequestParams):
    retries_left = 6
    for i in range(retries_left):
        try:
            response = _generate_fix(params)
            if response.status_code == 200:
                return response
            else:
                print(f"Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Received exception: {e}")
            # This is what a timeout exception will look like:
            # requests.exceptions.ReadTimeout: HTTPConnectionPool(host='0.0.0.0', port=8080): Read timed out. (read timeout=600)
        print(
            f"Failed to get a '200' response from the server.  Retrying {retries_left-i} more times"
        )
    sys.exit(f"Failed to get a '200' response from the server.  Parameters = {params}")


def parse_response(response):
    return response.json()
    ## TODO:  Below is rough guess at error handling, need to confirm
    # if "error" in response_json:
    #    print(f"Error: {response_json['error']}")
    #    return ""
    # TODO: When we are batching incidents we get back a parse result so we dont need below
    # return pydantic_models.parse_file_solution_content(response_json["updated_file"])


def write_to_disk(file_path, updated_file_contents):
    # We expect that we are overwriting the file, so all directories should exist
    intended_file_path = f"{SAMPLE_APP_DIR}/{file_path}"
    if not os.path.exists(intended_file_path):
        print(
            f"**WARNING* File {intended_file_path} does not exist.  Proceeding, but suspect this is a new file or there is a problem with the filepath"
        )

    print(f"Writing to {intended_file_path}")
    # print(f"{updated_file_contents['updated_file']}")
    # print(f"Reasoning: {updated_file_contents['total_reasoning']}")
    with open(intended_file_path, "w") as f:
        f.write(updated_file_contents["updated_file"])


def process_file(file_path, violations, num_impacted_files, count):
    print(
        f"File #{count} of {num_impacted_files} - Processing {file_path} which has {len(violations)} violations"
    )

    if not file_path.endswith(".java"):
        print(f"Skipping {file_path} as it is not a Java file")
        return

    params = collect_parameters(file_path, violations)
    response = generate_fix(params)
    print(f"\nResponse StatusCode: {response.status_code} for {file_path}\n")
    updated_file_contents = parse_response(response)
    write_to_disk(file_path, updated_file_contents)


def run_demo(report):
    impacted_files = report.get_impacted_files()
    num_impacted_files = len(impacted_files)

    total_violations = sum(len(violations) for violations in impacted_files.values())
    print(f"{num_impacted_files} files with a total of {total_violations} violations.")

    with ThreadPoolExecutor() as executor:
        futures = []
        for count, (file_path, violations) in enumerate(impacted_files.items(), 1):
            future = executor.submit(
                process_file, file_path, violations, num_impacted_files, count
            )
            futures.append(future)

        for future in futures:
            future.result()


if __name__ == "__main__":
    KAI_LOG.setLevel("info".upper())
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report(coolstore_analysis_dir)
    run_demo(r)

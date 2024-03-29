#!/usr/bin/env python

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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
# 1) Add ConfigFile to tweak the server URL and rulesets/violations
# 2) Limit to specific rulesets/violations we are interested in


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
    include_llm_results: bool = True

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
    response = requests.post(
        ###
        # If we are sending only one incident, we can use this endpoint
        # f"{SERVER_URL}/get_incident_solution",
        ###
        f"{SERVER_URL}/get_incident_solutions_for_file",
        data=params.to_json(),
        headers=headers,
        timeout=3600,
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
                KAI_LOG.info(
                    f"[{params.file_name}] Received status code {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            KAI_LOG.error(f"[{params.file_name}] Received exception: {e}")
            # This is what a timeout exception will look like:
            # requests.exceptions.ReadTimeout: HTTPConnectionPool(host='0.0.0.0', port=8080): Read timed out. (read timeout=600)
        KAI_LOG.error(
            f"[{params.file_name}] Failed to get a '200' response from the server.  Retrying {retries_left-i} more times"
        )
    sys.exit(
        f"[{params.file_name}] Failed to get a '200' response from the server.  Parameters = {params}"
    )


def parse_response(response):
    try:
        return response.json()
    except Exception as e:
        KAI_LOG.error(f"Failed to parse response with error: {e}")
        KAI_LOG.error(f"Response: {response}")
        sys.exit(1)
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
        KAI_LOG.warning(
            f"**WARNING* File {intended_file_path} does not exist.  Proceeding, but suspect this is a new file or there is a problem with the filepath"
        )

    KAI_LOG.info(f"Writing updated source code to {intended_file_path}")
    try:
        with open(intended_file_path, "w") as f:
            f.write(updated_file_contents["updated_file"])
    except Exception as e:
        KAI_LOG.error(
            f"Failed to write updated_file @ {intended_file_path} with error: {e}"
        )
        KAI_LOG.error(f"Contents: {updated_file_contents}")
        sys.exit(1)

    reasoning_path = f"{intended_file_path}.reasoning"
    KAI_LOG.info(f"Writing reasoning to {reasoning_path}")
    try:
        with open(reasoning_path, "w") as f:
            json.dump(updated_file_contents["total_reasoning"], f)
    except Exception as e:
        KAI_LOG.error(f"Failed to write reasoning @ {reasoning_path} with error: {e}")
        KAI_LOG.error(f"Contents: {updated_file_contents}")
        sys.exit(1)

    prompts_path = f"{intended_file_path}.prompts"
    KAI_LOG.info(f"Writing prompts to {prompts_path}")
    try:
        with open(prompts_path, "w") as f:
            f.write("\n---\n".join(updated_file_contents["used_prompts"]))
    except Exception as e:
        KAI_LOG.error(f"Failed to write prompts @ {prompts_path} with error: {e}")
        KAI_LOG.error(f"Contents: {updated_file_contents}")
        sys.exit(1)

    if updated_file_contents.get("llm_results"):
        llm_result_path = f"{intended_file_path}.llm_result"
        KAI_LOG.info(f"Writing llm_result to {llm_result_path}")
        try:
            model_id = updated_file_contents.get("model_id", "unknown")
            with open(llm_result_path, "w") as f:
                f.write(f"Model ID: {model_id}\n")
                f.write("\n---\n".join(updated_file_contents["llm_results"]))
        except Exception as e:
            KAI_LOG.error(
                f"Failed to write llm_result @ {llm_result_path} with error: {e}"
            )
            KAI_LOG.error(f"Contents: {updated_file_contents}")
            sys.exit(1)


def process_file(file_path, violations, num_impacted_files, count):
    start = time.time()
    KAI_LOG.info(
        f"File #{count} of {num_impacted_files} - Processing {file_path} which has {len(violations)} violations"
    )

    params = collect_parameters(file_path, violations)
    response = generate_fix(params)
    KAI_LOG.info(f"Response StatusCode: {response.status_code} for {file_path}\n")
    updated_file_contents = parse_response(response)
    write_to_disk(file_path, updated_file_contents)
    end = time.time()
    return f"{end-start}s to process {file_path} with {len(violations)} violations"


def run_demo(report):
    impacted_files = report.get_impacted_files()
    num_impacted_files = len(impacted_files)
    remaining_files = num_impacted_files
    total_violations = sum(len(violations) for violations in impacted_files.values())
    print(f"{num_impacted_files} files with a total of {total_violations} violations.")

    max_workers = os.environ.get("KAI_MAX_WORKERS", 8)
    KAI_LOG.info(f"Running in parallel with {max_workers} workers")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for count, (file_path, violations) in enumerate(impacted_files.items(), 1):
            future = executor.submit(
                process_file, file_path, violations, num_impacted_files, count
            )
            futures.append(future)

        for future in as_completed(futures):
            try:
                result = future.result()
                KAI_LOG.info(f"Result:  {result}")
            except Exception as exc:
                KAI_LOG.error(f"Generated an exception: {exc}")
            remaining_files -= 1
            KAI_LOG.info(
                f"{remaining_files} files remaining from total of {num_impacted_files}"
            )


if __name__ == "__main__":
    KAI_LOG.setLevel("info".upper())
    start = time.time()
    coolstore_analysis_dir = "./analysis/coolstore/output.yaml"
    r = Report(coolstore_analysis_dir)
    run_demo(r)
    end = time.time()
    KAI_LOG.info(f"Total time to process '{coolstore_analysis_dir}' was {end-start}s")

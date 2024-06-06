#!/usr/bin/env python

import argparse
import os
import pprint

# trunk-ignore(bandit/B404)
import subprocess
import tempfile
import time
from typing import Any, Dict, Iterator, List, Optional, Tuple

import dateutil.parser
import requests
import urllib3
from pydantic import BaseModel, Field

from kai.kai_logging import KAI_LOG
from kai.models.kai_config import KaiConfig
from kai.report import Report
from kai.service.incident_store import Application, IncidentStore


# BaseModel that also acts as a dict
class KaiBaseModel(BaseModel):
    def __contains__(self, item):
        return hasattr(self, item)

    def __getitem__(self, key):
        if not hasattr(self, key):
            raise KeyError(f"Key '{key}' not found")
        return getattr(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        setattr(self, key, value)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default


class Incident(KaiBaseModel):
    id: int
    createUser: Optional[str] = None
    updateUser: Optional[str] = None
    createTime: Optional[str] = None
    issue: int
    file: str
    uri: str = Field(..., alias="file")
    lineNumber: int = Field(..., alias="line")
    message: str
    codeSnip: str
    variables: Dict[str, Any] = Field(..., alias="facts")


class Link(KaiBaseModel):
    url: str
    title: str


class Issue(KaiBaseModel):
    id: int
    createUser: Optional[str] = None
    updateUser: Optional[str] = None
    createTime: Optional[str] = None
    analysis: int
    ruleset: str
    rule: str
    name: str
    description: str
    category: str
    effort: int
    incidents: List[Incident]
    links: Optional[List[Link]] = []
    labels: List[str]


class HubApplication(KaiBaseModel):
    id: int
    createUser: Optional[str] = None
    updateUser: Optional[str] = None
    createTime: Optional[str] = None


class Analysis(KaiBaseModel):
    id: int
    createUser: Optional[str] = None
    updateUser: Optional[str] = None
    createTime: Optional[str] = None
    application: HubApplication
    effort: int
    archived: Optional[bool] = False
    commit: Optional[str] = None


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("konveyor_url", help="The base URL for konveyor hub")
    arg_parser.add_argument(
        "-log",
        "--loglevel",
        default=os.environ.get("KAI_LOG_LEVEL", "info"),
        choices=["debug", "info", "warning", "error", "critical"],
        help="""Provide logging level.
Options:
- debug: Detailed information, typically of interest only when diagnosing problems.
- info: Confirmation that things are working as expected.
- warning: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
- error: Due to a more serious problem, the software has not been able to perform some function.
- critical: A serious error, indicating that the program itself may be unable to continue running.
Example: --loglevel debug (default: warning)""",
    )

    arg_parser.add_argument(
        "--config_filepath",
        type=str,
        default="kai/config.toml",
        help="Path to the config file.",
    )

    arg_parser.add_argument(
        "-i",
        "--interval",
        default=60,
        help="Interval to poll the konveyor API for changes",
    )

    arg_parser.add_argument(
        "-k",
        "--skip-verify",
        default=False,
        action="store_true",
        help="Skip verifying SSL certs when making requests",
    )

    arg_parser.add_argument(
        "-t",
        "--timeout",
        default=60,
        help="Set the request timeout for Konveyor API requests",
    )

    args, _ = arg_parser.parse_known_args()
    KAI_LOG.setLevel(args.loglevel.upper())

    config: KaiConfig
    if os.path.exists(args.config_filepath):
        config = KaiConfig.model_validate_filepath(args.config_filepath)
    else:
        raise ValueError(
            f"A valid config file is required, {args.config_filepath} does not exist"
        )
    config.log_level = args.loglevel
    KAI_LOG.info(f"Config loaded: {pprint.pformat(config)}")

    incident_store = IncidentStore.from_config(config.incident_store)

    if args.skip_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    poll_api(
        args.konveyor_url,
        incident_store,
        interval=args.interval,
        timeout=args.timeout,
        verify=not args.skip_verify,
    )


def paginate_api(url: str, timeout: int = 60, verify: bool = True) -> Iterator:
    previous_offset = None
    current_offset = 0
    while previous_offset != current_offset:
        previous_offset = current_offset
        request_params = {"offset": f"{current_offset}"}
        for item in get_data_from_api(
            url, params=request_params, timeout=timeout, verify=verify
        ):
            current_offset += 1
            yield item


def poll_api(
    konveyor_url: str,
    incident_store: IncidentStore,
    interval: int = 60,
    timeout: int = 60,
    verify: bool = True,
    initial_last_analysis: int = 0,
):
    last_analysis = initial_last_analysis

    while True:
        new_last_analysis = import_from_api(
            incident_store, konveyor_url, last_analysis, timeout, verify
        )
        if new_last_analysis == last_analysis:
            print(f"No new analyses. Sleeping for {interval} seconds.")
            time.sleep(interval)
        else:
            print(f"New analyses found. Updating last_analysis to {new_last_analysis}.")
            last_analysis = new_last_analysis


def import_from_api(
    incident_store: IncidentStore,
    konveyor_url: str,
    last_analysis: int = 0,
    timeout: int = 60,
    verify: bool = True,
) -> int:
    analyses_url = f"{konveyor_url}/hub/analyses"
    request_params = {"filter": f"id>{last_analysis}"}
    analyses = get_data_from_api(
        analyses_url, params=request_params, timeout=timeout, verify=verify
    )

    validated_analyses = [Analysis(**item) for item in analyses]

    # TODO(fabianvf) add mechanism to skip import if a report has already been imported
    with tempfile.TemporaryDirectory() as tmpdir:
        reports = process_analyses(
            validated_analyses, konveyor_url, tmpdir, timeout, verify
        )

        for app, report in reports:
            clone_repo_at_commit(
                app.repo_uri_origin,
                app.current_branch,
                app.current_commit,
                app.repo_uri_local,
            )
            incident_store.load_report(app, report)
    if validated_analyses:
        return validated_analyses[0].id

    return last_analysis


def get_data_from_api(url: str, params=None, timeout: int = 60, verify: bool = True):
    if not params:
        params = {}
    KAI_LOG.debug(f"Making request to {url} with {params=}")
    response = requests.get(url, params=params, timeout=timeout, verify=verify)
    response.raise_for_status()
    return response.json()


def process_analyses(
    analyses: List[Analysis],
    base_url: str,
    application_dir: str,
    request_timeout: int = 60,
    request_verify: bool = True,
) -> List[Tuple[Application, Report]]:

    reports: List[Tuple[Application, Report]] = []
    for analysis in analyses:
        KAI_LOG.info(
            f"Processing analysis {analysis.id} for application {analysis.application.id}"
        )
        application = parse_application_data(
            get_data_from_api(
                f"{base_url}/hub/applications/{analysis.application.id}",
                timeout=request_timeout,
                verify=request_verify,
            ),
            application_dir,
        )
        application.current_commit = analysis.commit
        report_data = {}
        issues_url = f"{base_url}/hub/analyses/{analysis.id}/issues"
        for raw_issue in paginate_api(
            issues_url, timeout=request_timeout, verify=request_verify
        ):
            issue = Issue(**raw_issue)
            KAI_LOG.info(
                f"Processing issue {issue.id} with effort {issue.effort} on ruleset {issue.ruleset} (commit: {analysis.commit})"
            )
            key = issue.ruleset
            if key not in report_data:
                report_data[key] = {"description": issue.description, "violations": {}}
            for incident in issue.incidents:
                incident.file = incident.file.removeprefix(
                    f"/addon/source/{application.application_name}/"
                )
                incident.uri = incident.uri.removeprefix(
                    f"/addon/source/{application.application_name}/"
                )
                KAI_LOG.debug(f"{incident.variables=}")
            report_data[key]["violations"][issue.rule] = {
                "category": issue.category,
                "description": issue.description,
                "effort": issue.effort,
                "incidents": issue.incidents,
            }
        if report_data:
            reports.append((application, Report.load_report_from_object(report_data)))
    return reports


def clone_repo_at_commit(repo_url, branch, commit, destination_folder):
    try:
        # trunk-ignore(bandit/B603,bandit/B607)
        subprocess.run(
            ["git", "clone", "-b", branch, repo_url, destination_folder], check=True
        )
    except subprocess.CalledProcessError as e:
        KAI_LOG.error(f"An error occurred: {e}")

    try:
        # trunk-ignore(bandit/B603,bandit/B607)
        subprocess.run(["git", "checkout", commit], cwd=destination_folder, check=True)
        KAI_LOG.info(f"Repository cloned at commit {commit} into {destination_folder}")
    except subprocess.CalledProcessError as e:
        KAI_LOG.error(f"An error occurred: {e}")


def parse_application_data(api_response, application_dir):
    application_name = api_response.get("name", "")
    repo_uri_origin = (
        api_response["repository"]["url"]
        if "repository" in api_response and "url" in api_response["repository"]
        else ""
    )
    current_branch = (
        api_response["repository"]["branch"]
        if "repository" in api_response and "branch" in api_response["repository"]
        else ""
    )

    current_commit = api_response["repository"].get("commit", "")
    generated_at = dateutil.parser.parse(
        api_response.get("createTime", "1970-01-01T00:00:00Z")
    )

    application = Application(
        application_name=application_name,
        repo_uri_origin=repo_uri_origin,
        repo_uri_local=os.path.join(application_dir, application_name),
        current_branch=current_branch,
        current_commit=current_commit,
        generated_at=generated_at,
    )

    return application


if __name__ == "__main__":
    main()

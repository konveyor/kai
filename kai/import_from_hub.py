#!/usr/bin/env python

import argparse
import os
import pprint
import subprocess
from typing import Any, Dict, List, Optional, Tuple

import dateutil.parser
import requests
import urllib3
from pydantic import BaseModel, Field, HttpUrl

from kai.constants import PATH_KAI
from kai.kai_logging import KAI_LOG
from kai.models.kai_config import KaiConfig
from kai.report import Report
from kai.service.incident_store import Application, IncidentStore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    url: HttpUrl
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


def get_data_from_api(url: str, request_timeout: int, request_verify: bool):
    response = requests.get(url, verify=False, timeout=60)
    response.raise_for_status()
    return response.json()


def process_analyses(
    base_url: str, request_timeout: int, request_verify: bool
) -> List[Tuple[Application, Report]]:
    analyses_url = f"{base_url}/hub/analyses"
    analyses = get_data_from_api(analyses_url, request_timeout, request_verify)

    reports: List[Tuple[Application, Report]] = []
    validated_analyses = [Analysis(**item) for item in analyses]
    for analysis in validated_analyses:
        KAI_LOG.info(
            f"Processing analysis {analysis.id} for application {analysis.application.id}"
        )
        application = parse_application_data(
            get_data_from_api(
                f"{base_url}/hub/applications/{analysis.application.id}",
                request_timeout,
                request_verify,
            )
        )
        application.current_commit = analysis.commit
        report_data = {}
        app_id = analysis.application.id
        issues_url = f"{base_url}/hub/analyses/{analysis.id}/issues"
        issues = [
            Issue(**item)
            for item in get_data_from_api(issues_url, request_timeout, request_verify)
        ]
        for issue in issues:
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


def parse_application_data(api_response):
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
        # I think we'll need to set this in config? And clone the applications there manually
        repo_uri_local=f"/tmp/{application_name}",
        current_branch=current_branch,
        current_commit=current_commit,
        generated_at=generated_at,
    )

    return application


def clone_repo_at_commit(repo_url, branch, commit, destination_folder):
    try:
        subprocess.run(
            ["git", "clone", "-b", branch, repo_url, destination_folder], check=True
        )
    except subprocess.CalledProcessError as e:
        KAI_LOG.error(f"An error occurred: {e}")

    try:
        subprocess.run(["git", "checkout", commit], cwd=destination_folder, check=True)
        KAI_LOG.info(f"Repository cloned at commit {commit} into {destination_folder}")
    except subprocess.CalledProcessError as e:
        KAI_LOG.error(f"An error occurred: {e}")


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

    # TODO(fabianvf) implement this
    arg_parser.add_argument(
        "-p",
        "--poll",
        default=False,
        action="store_true",
        help="Poll the konveyor API for changes",
    )

    arg_parser.add_argument(
        "-k",
        "--verify",
        default=True,
        action="store_true",
        help="Verify SSL certs when making requests",
    )

    arg_parser.add_argument(
        "-t",
        "--timeout",
        default=60,
        help="Set the request timeout for Konveyor API requests",
    )

    arg_parser.add_argument(
        "-d",
        "--drop-tables",
        default=False,
        action="store_true",
        help="Drop the incident store tables before loading reports",
    )

    args, _ = arg_parser.parse_known_args()
    KAI_LOG.setLevel(args.loglevel.upper())
    base_path = os.path.dirname(__file__)

    config: KaiConfig
    if os.path.exists(os.path.join(PATH_KAI, "config.toml")):
        config = KaiConfig.model_validate_filepath(
            os.path.join(PATH_KAI, "config.toml")
        )
    config.log_level = args.loglevel
    KAI_LOG.info(f"Config loaded: {pprint.pformat(config)}")

    incident_store = IncidentStore.from_config(config.incident_store)

    # TODO(fabianvf): This seems too easy and destructive
    if args.drop_tables:
        incident_store.delete_store()

    reports = process_analyses(args.konveyor_url, args.timeout, args.verify)
    for app, report in reports:
        clone_repo_at_commit(
            app.repo_uri_origin,
            app.current_branch,
            app.current_commit,
            app.repo_uri_local,
        )
        incident_store.load_report(app, report)


if __name__ == "__main__":
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with __import__("ipdb").launch_ipdb_on_exception():
        main()

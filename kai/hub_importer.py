#!/usr/bin/env python

import argparse
import logging
import os
import pprint
import tempfile
import time
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

import dateutil.parser
import requests
import urllib3
from git import GitCommandError, Repo
from pydantic import BaseModel, Field

from kai.models.kai_config import KaiConfig
from kai.models.report import Report
from kai.service.incident_store import Application, IncidentStore

KAI_LOG = logging.getLogger(__name__)


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


class Identity(KaiBaseModel):
    id: int
    kind: Optional[str] = None
    name: str
    user: Optional[str] = None
    password: Optional[str] = None
    key: Optional[str] = None


class HubApplication(KaiBaseModel):
    id: int
    createUser: Optional[str] = None
    updateUser: Optional[str] = None
    createTime: Optional[str] = None
    identities: List[Identity] = None


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
    arg_parser.add_argument("konveyor_hub_url", help="The URL for Konveyor Hub")
    arg_parser.add_argument(
        "-log",
        "--loglevel",
        default=os.environ.get("KAI__LOG_LEVEL", "info"),
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
        default=None,
        help="Path to the config file.",
    )

    arg_parser.add_argument(
        "-i",
        "--interval",
        default=60,
        help="Interval to poll the konveyor API for changes",
        type=int,
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
        type=int,
    )

    arg_parser.add_argument(
        "--log_file",
        help="Set the request timeout for Konveyor API requests",
        type=str,
    )

    args, _ = arg_parser.parse_known_args()
    KAI_LOG.setLevel(args.loglevel.upper())
    if args.log_file:
        KAI_LOG.addHandler(logging.FileHandler(args.log_file))
    else:
        KAI_LOG.addHandler(logging.StreamHandler())

    config: KaiConfig
    if os.path.exists(args.config_filepath):
        config = KaiConfig.model_validate_filepath(args.config_filepath)
    else:
        config = KaiConfig()

    config.log_level = args.loglevel
    KAI_LOG.info(f"Config loaded: {pprint.pformat(config)}")

    incident_store = IncidentStore.incident_store_from_config(config)

    if args.skip_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    poll_api(
        args.konveyor_hub_url,
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
    konveyor_hub_url: str,
    incident_store: IncidentStore,
    interval: int = 60,
    timeout: int = 60,
    verify: bool = True,
    initial_last_analysis: int = 0,
    post_process_limit: int = 5,
    poll_condition: Callable = lambda: True,
):
    last_analysis = initial_last_analysis

    while poll_condition():
        new_last_analysis = import_from_api(
            incident_store, konveyor_hub_url, last_analysis, timeout, verify
        )

        if new_last_analysis == last_analysis:
            KAI_LOG.info("No new analyses.")
        else:
            KAI_LOG.info(
                f"New analyses found. Updating last_analysis to {new_last_analysis}."
            )
            last_analysis = new_last_analysis

        post_proc_start = time.time()
        # generate solutions for some incidents
        KAI_LOG.info("Running post_process to generate solutions")
        incident_store.post_process(limit=post_process_limit)
        post_proc_duration = int(time.time() - post_proc_start)
        if new_last_analysis == last_analysis and post_proc_duration < interval:
            KAI_LOG.info(f"Sleeping for {interval-post_proc_duration} seconds.")
            time.sleep(interval - post_proc_duration)


def import_from_api(
    incident_store: IncidentStore,
    konveyor_hub_url: str,
    last_analysis: int = 0,
    timeout: int = 60,
    verify: bool = True,
) -> int:
    analyses_url = f"{konveyor_hub_url}/analyses"
    request_params = {"filter": f"id>{last_analysis}"}
    analyses = get_data_from_api(
        analyses_url, params=request_params, timeout=timeout, verify=verify
    )

    validated_analyses = [Analysis(**item) for item in analyses]

    # TODO(fabianvf) add mechanism to skip import if a report has already been imported
    with tempfile.TemporaryDirectory() as tmpdir:
        reports = process_analyses(
            validated_analyses, konveyor_hub_url, tmpdir, timeout, verify
        )

        for app, creds, report in reports:
            clone_repo_at_commit(
                app.repo_uri_origin,
                app.current_branch,
                app.current_commit,
                app.repo_uri_local,
                identity=creds,
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
    konveyor_hub_url: str,
    application_dir: str,
    request_timeout: int = 60,
    request_verify: bool = True,
) -> List[Tuple[Application, Optional[Identity], Report]]:

    reports: List[Tuple[Application, Optional[Identity], Report]] = []
    for analysis in analyses:
        KAI_LOG.info(
            f"Processing analysis {analysis.id} for application {analysis.application.id}"
        )
        resp = get_data_from_api(
            f"{konveyor_hub_url}/applications/{analysis.application.id}",
            timeout=request_timeout,
            verify=request_verify,
        )
        # This contains credential information if we need it
        hub_application = HubApplication(**resp)
        credentials = None
        if hub_application.identities:
            for identity in hub_application.identities:
                creds = Identity(
                    **get_data_from_api(
                        f"{konveyor_hub_url}/identities/{identity.id}",
                        timeout=request_timeout,
                        verify=request_verify,
                    )
                )
                # Default to the first identity that provides a key
                # TODO(fabianvf) what does it mean if there are multiple identities
                if not credentials:
                    credentials = creds
                elif not credentials.key and creds.key:
                    credentials = creds
        application = parse_application_data(
            resp,
            application_dir,
        )
        application.current_commit = analysis.commit
        report_data = {}
        issues_url = f"{konveyor_hub_url}/analyses/{analysis.id}/issues"
        for raw_issue in paginate_api(
            issues_url, timeout=request_timeout, verify=request_verify
        ):
            issue = Issue(**raw_issue)
            KAI_LOG.info(
                f"Processing issue {issue.id} with effort {issue.effort} on ruleset {issue.ruleset} (commit: {analysis.commit})"
            )
            key = issue.ruleset
            if key not in report_data:
                report_data[key] = {
                    "name": key,
                    "description": issue.description,
                    "violations": {},
                }
            for incident in issue.incidents:
                for prefix in [
                    "/addon/source/",
                    "/shared/source/",
                ]:
                    incident.file = incident.file.replace(prefix, "", -1)
                    incident.uri = incident.uri.replace(prefix, "", -1)

                def remove_base_dir(x):
                    return x.split("/", 1)[1] if len(x.split("/", 1)) > 1 else x

                incident.file = remove_base_dir(incident.file)
                incident.uri = remove_base_dir(incident.uri)
                KAI_LOG.debug(f"{incident.variables=}")
            report_data[key]["violations"][issue.rule] = {
                "category": issue.category,
                "description": issue.description,
                "effort": issue.effort,
                "incidents": [i.model_dump() for i in issue.incidents],
            }
        if report_data:
            reports.append(
                (
                    application,
                    credentials,
                    Report.load_report_from_object(
                        [rs for rs in report_data.values()], str(analysis.id)
                    ),
                )
            )
    return reports


def clone_repo_at_commit(repo_url, branch, commit, destination_folder, identity=None):
    if identity:
        user = identity.get("user")
        password = identity.get("password")
        key = identity.get("key")

        if user and password:
            KAI_LOG.debug(f"Using password authentication for {repo_url}")
            repo_url = repo_url.replace("https://", f"https://{user}:{password}@")
        elif key:
            KAI_LOG.debug(f"Using key-based authentication for {repo_url}")
            ssh_command = f"ssh -i {key}"
            os.environ["GIT_SSH_COMMAND"] = ssh_command
    try:
        # Clone the repository and checkout the specified branch
        repo = Repo.clone_from(repo_url, destination_folder, branch=branch)
        KAI_LOG.info(f"Repository cloned to {destination_folder}")
    except GitCommandError as e:
        KAI_LOG.error(f"An error occurred while cloning the repo: {e}")
        return

    try:
        # Checkout the specified commit
        repo.git.checkout(commit)
        KAI_LOG.info(f"Checked out commit {commit} in {destination_folder}")
    except GitCommandError as e:
        KAI_LOG.error(f"An error occurred while checking out the commit: {e}")


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
        path=api_response.get("repository", {}).get("path", ""),
    )

    return application


if __name__ == "__main__":
    main()

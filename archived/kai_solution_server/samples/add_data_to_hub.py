#!/usr/bin/env python

import argparse
import os
import tempfile
from typing import Any

import requests
import urllib3
import yaml
from git import Repo

from kai_solution_server.hub_importer import Incident, Issue

# Little hack so we can import from test directory
try:
    import config
except ImportError:
    from . import config


def main():
    parser = argparse.ArgumentParser(description="Add sample data to the hub")
    parser.add_argument("hub_url", type=str, help="The URL of the Konveyor hub")

    parser.add_argument(
        "-k", "--skip-verify", action="store_true", help="Allow insecure requests"
    )

    args = parser.parse_args()

    if args.skip_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    add_applications(args.hub_url, args.skip_verify)


def add_applications(hub_url, skip_verify):
    analysis_id = 1
    for app_name, _ in config.sample_apps.items():
        repo_info = config.repos.get(app_name)
        repo_path = config.sample_apps.get(app_name)
        if repo_info:
            url, initial_branch, solved_branch = repo_info
            payload = {
                "name": app_name,
                "description": f"{app_name} application.",
                "repository": {
                    "kind": "git",
                    "url": url,
                    "branch": solved_branch,
                },
            }

            headers = {
                "Content-Type": "application/x-yaml",
                "Accept": "application/json",
            }

            try:
                response = requests.post(
                    f"{hub_url}/applications",
                    headers=headers,
                    data=yaml.dump(payload),
                    verify=not skip_verify,
                    timeout=60,
                )

                if response.status_code == 201:
                    print(f"Successfully added {app_name}")
                    app_id = response.json()["id"]
                elif (
                    response.status_code == 409
                ):  # Conflict, application already exists
                    print(
                        f"{app_name} already exists. Retrieving existing application ID."
                    )
                    app_id = get_application_id(hub_url, app_name, skip_verify)
                    if not app_id:
                        print(
                            f"Failed to retrieve application ID for {app_name}. Skipping analysis report upload."
                        )
                        continue
                else:
                    print(
                        f"Failed to add {app_name}: {response.status_code} - {response.text}"
                    )
                    continue

                script_dir = os.path.dirname(os.path.realpath(__file__))
                app_repo = Repo(os.path.join(script_dir, repo_path))

                analyses = [
                    (
                        os.path.join(
                            script_dir,
                            f"analysis_reports/{app_name}/initial/output.yaml",
                        ),
                        str(app_repo.branches[initial_branch].checkout().commit),
                    ),
                    (
                        os.path.join(
                            script_dir,
                            f"analysis_reports/{app_name}/solved/output.yaml",
                        ),
                        str(app_repo.branches[solved_branch].checkout().commit),
                    ),
                ]

                for analysis_path, commit in analyses:
                    try:
                        if os.path.exists(analysis_path):
                            add_analysis_report(
                                hub_url,
                                app_id,
                                analysis_id,
                                analysis_path,
                                commit,
                                skip_verify,
                            )
                            analysis_id += 1
                        else:
                            print(f"Analysis report file missing for {app_name}")
                    except Exception as e:
                        print(
                            f"Failed to upload analysis report {analysis_path} for {app_name}: {e}"
                        )
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {app_name}: {e}")


def get_application_id(hub_url, app_name, skip_verify):
    response = requests.get(
        f"{hub_url}/applications", verify=not skip_verify, timeout=60
    )
    if response.status_code == 200:
        applications = response.json()
        for app in applications:
            if app["name"] == app_name:
                return app["id"]
    return None


def add_analysis_report(
    hub_url, app_id, analysis_id, analysis_path, commit, skip_verify
):
    with open(analysis_path, "r") as f:
        analysis_report = yaml.safe_load(f)

    reformatted_report = reformat_analysis_report(
        analysis_report, app_id, analysis_id, commit
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False
    ) as temp_analysis_file, tempfile.NamedTemporaryFile(
        mode="w", delete=False
    ) as temp_issues_file, tempfile.NamedTemporaryFile(
        mode="w", delete=False
    ) as temp_dependencies_file:

        yaml.safe_dump_all([reformatted_report], temp_analysis_file)
        temp_analysis_path = temp_analysis_file.name

        issues = reformatted_report.get("issues", [])
        yaml.safe_dump_all(issues, temp_issues_file)
        temp_issues_path = temp_issues_file.name

        # TODO(fabianvf) handle the dependencies file
        dependencies = reformatted_report.get("dependencies", [])
        yaml.safe_dump_all(dependencies, temp_dependencies_file)
        temp_dependencies_path = temp_dependencies_file.name

    try:
        mime = "application/x-yaml"
        files = {
            "file": ("reformatted_analysis.yaml", open(temp_analysis_path, "rb"), mime),
            "issues": ("reformatted_issues.yaml", open(temp_issues_path, "rb"), mime),
            "dependencies": (
                "reformatted_dependencies.yaml",
                open(temp_dependencies_path, "rb"),
                mime,
            ),
        }

        response = requests.post(
            f"{hub_url}/applications/{app_id}/analyses",
            headers={"Accept": mime},
            files=files,
            verify=not skip_verify,
            timeout=120,
        )

        if response.status_code == 201:
            print(f"Successfully added analysis report for application ID {app_id}")
        else:
            print(
                f"Failed to add analysis report for application ID {app_id}: {response.status_code} - {response.text}"
            )
    finally:
        for f in files.values():
            f[1].close()
        # # Clean up the temporary files
        # os.remove(temp_analysis_path)
        # os.remove(temp_issues_path)
        # os.remove(temp_dependencies_path)


def reformat_analysis_report(
    report: list[dict[str, Any]], app_id: int, analysis_id: int, commit: str
) -> dict[str, Any]:
    issues = []

    for ruleset in report:
        for issue_id, (violation_id, violation) in enumerate(
            ruleset.get("violations", {}).items()
        ):
            incidents = [
                Incident(
                    id=incident_id,
                    issue=issue_id,
                    file=incident["uri"],
                    line=incident.get("lineNumber", 0),
                    message=incident["message"],
                    codeSnip=incident.get("codeSnip", ""),
                    facts=incident.get("variables", {}),
                )
                for incident_id, incident in enumerate(violation.get("incidents", []))
            ]

            # TODO(fabianvf)
            # keep getting 409 - error: 'UNIQUE constraint failed: Issue.RuleSet, Issue.Rule, Issue.AnalysisID'
            # Is it something I'm doing wrong here? Issues seem to import correctly despite the error
            issue = Issue(
                id=issue_id,
                analysis=analysis_id,
                ruleset=ruleset["name"],
                rule=violation_id,
                name=violation_id,
                description=violation["description"],
                category=violation["category"],
                effort=violation.get("effort", 0),
                incidents=incidents,
                links=violation.get("links", []),
                labels=violation.get("labels", []),
            )
            issues.append(issue.model_dump(by_alias=True))

    return {"commit": commit, "issues": issues, "dependencies": []}


if __name__ == "__main__":
    main()

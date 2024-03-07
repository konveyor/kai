__all__ = ["Application", "IncidentStore"]

import copy
import os
import pprint
from dataclasses import dataclass
from typing import Optional

import yaml

from kai.report import Report
from kai.scm import GitDiff

# TODO: Add types to this entire file - jsussman

# TODO: Make this more like the real n -> n+1 problem


@dataclass
class Application:
    name: str
    report: dict
    repo: Optional[str] = None
    initial_branch: Optional[str] = None  # shouldn't it be current branch?
    solved_branch: Optional[str] = None
    timestamp: Optional[int] = None


class IncidentStore:
    def __init__(self, report_path: str, output_dir: str):
        # applications, keyed on App Name
        self.applications: dict[str, Application] = {}
        # cached_violations is defined in comments in self._update_cached_violations
        self.cached_violations = {}
        self.solved_violations = {}
        self.missing_violations = {}
        self.output_dir = output_dir
        self.analysis_dir = report_path
        self.pp = pprint.PrettyPrinter(indent=2)

    def add_app_to_incident_store(self, app_name: str, path_to_report: str):
        r = Report(path_to_report).get_report()
        app_variables = self.get_app_variables(app_name)
        if app_variables is None:
            raise Exception(f"Unable to get app_variables for app_name '{app_name}'.")

        a = Application(
            app_name,
            r,
            app_variables.get("repo", None),
            app_variables.get("initial_branch", None),
            app_variables.get("solved_branch", None),
            app_variables.get("timestamp", None),
        )
        self.applications[app_name] = a
        self._update_cached_violations(a)

    def get_app_from_incident_store(self, app_name: str):
        return self.applications[app_name]

    def get_app_names_from_incident_store(self):
        return self.applications.keys()

    # TODO: query hub api for the application
    def get_app_from_konveyor_hub(self, app_name: str):
        return None  # For now, return None always - jsussman

    # get the app variables from the app.yaml
    def get_app_variables(self, app_name: str):
        # Path to the analysis_reports directory
        analysis_reports_dir = "samples/analysis_reports"

        # Check if the specified app folder exists
        app_folder = os.path.join(analysis_reports_dir, app_name)
        if not os.path.exists(app_folder):
            print(
                f"Error: {app_name} does not exist in the analysis_reports directory."
            )
            return None

        # Path to the app.yaml file
        app_yaml_path = os.path.join(app_folder, "app.yaml")

        # Check if app.yaml exists for the specified app
        if not os.path.exists(app_yaml_path):
            print(f"Error: app.yaml does not exist for {app_name}.")
            return None

        # Load contents of app.yaml
        with open(app_yaml_path, "r") as app_yaml_file:
            app_data: dict = yaml.safe_load(app_yaml_file)

        return app_data

    # determine if new application analysis report is available
    def is_new_analysis_report_available(self, application):
        # query hub api for the application
        # if the timestamp is newer than the current timestamp
        # return true
        # else return false
        app1 = self.get_app_from_konveyor_hub(application.name)
        if app1 is not None:
            if app1.timestamp > application.timestamp:
                return True
        return False

    def _update_cached_violations(self, a):
        """
        Update the cached_violations with the new application
        The desired structure
         cached_violations: {
           ruleset_name: {
               violation_name: {
                   app_name: {
                       file_path: [ {
                            variables: {}
                            line_number: int
                            message: str
                        } ]
                    }
               }
           }
         }

        """
        ### Add our Application's Name to the cached_violations
        # self.pp.pprint(a.report)
        # load self.cached_violations if it is not loaded
        if self.cached_violations is None:
            self.cached_violations = self.get_cached_violations(
                "cached_violations.yaml"
            )
        print(f"Updating cached_violations with '{a.name}'")
        for ruleset in a.report.keys():
            if ruleset not in self.cached_violations:
                self.cached_violations[ruleset] = {}
            for violation_name in a.report[ruleset]["violations"].keys():
                if violation_name not in self.cached_violations[ruleset]:
                    self.cached_violations[ruleset][violation_name] = {}
                # Assume there can be multiple incidents of the same violation in same file
                ## Example of the YAML report data for an incident
                ##  incidents:
                ##  - uri: file:///tmp/source-code/src/main/webapp/WEB-INF/web.xml
                ##    message: "\n Session replication ensures that client sessions are not disrupted by node failure.
                ##             Each node in the cluster shares information about ongoing sessions and can take over sessions
                ##             if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.\n\n
                ##             Recommendations\n\n * Review the session replication usage and ensure that it is configured properly.\n *
                ##             Disable HTTP session clustering and accept its implications.\n * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.\n\n
                ##             A remote data grid has the following benefits:\n\n * The application is more scaleable and elastic.\n * The application can survive EAP node failures
                ##             because a JVM failure does not cause session data loss.\n * Session data can be shared by multiple applications.\n "
                ##    variables:
                ##      data: distributable
                ##      innerText: ""
                ##      matchingXML: ""
                ##
                incidents = a.report[ruleset]["violations"][violation_name].get(
                    "incidents", None
                )
                if incidents is None:
                    # self.pp.pprint(a.report[ruleset]["violations"])
                    print(
                        f"Found no incidents for '{a.name}' with {ruleset} and {violation_name}"
                    )
                    continue
                for incident in incidents:
                    if a.name not in self.cached_violations[ruleset][violation_name]:
                        self.cached_violations[ruleset][violation_name][a.name] = {}
                    uri = incident.get("uri", None)
                    if uri is None:
                        # self.pp.pprint(incident)
                        print(
                            f"'{a.name}' with {ruleset} and {violation_name}, incident has no 'uri'"
                        )
                        continue
                    file_path = Report.get_cleaned_file_path(uri)
                    if (
                        file_path
                        not in self.cached_violations[ruleset][violation_name][a.name]
                    ):
                        self.cached_violations[ruleset][violation_name][a.name][
                            file_path
                        ] = []
                    # Remember for future matches we need to take into account the variables
                    entry = {
                        "variables": copy.deepcopy(incident.get("variables", {})),
                        "line_number": incident.get("lineNumber", None),
                        "message": incident.get("message", None),
                    }
                    self.cached_violations[ruleset][violation_name][a.name][
                        file_path
                    ].append(entry)

    def find_common_violations(self, ruleset_name, violation_name):
        """
        Find the common violation across all applications
        Returns:
            None        - if no common violation
            {}          - if a common violation is found
        """

        # if the cached_violations is not loaded, load it
        if not self.cached_violations:
            self.cached_violations = self.get_cached_violations(
                "cached_violations.yaml"
            )
        # check the loaded cached_violations and see if its empty
        if self.cached_violations is None:
            return None

        common_entries = []

        # iterate through the cached_violations and find the common entries
        for ruleset, violations in self.cached_violations.items():
            if ruleset == ruleset_name:
                for violation, apps in violations.items():
                    if violation == violation_name:
                        for app, file_paths in apps.items():
                            common_entries.append([ruleset, violation, app, file_paths])

                        break
                break
        return common_entries

    def cleanup(self):
        """
        Cleanup the incident store
        """
        output_directory = self.output_dir
        # delete cached_violations.yaml if it exists
        if os.path.exists(f"{output_directory}/cached_violations.yaml"):
            os.remove(f"{output_directory}/cached_violations.yaml")
        # delete solved_incidents.yaml if it exists
        if os.path.exists(f"{output_directory}/solved_incidents.yaml"):
            os.remove(f"{output_directory}/solved_incidents.yaml")
        # delete missing_incidents.yaml if it exists
        if os.path.exists(f"{output_directory}/missing_incidents.yaml"):
            os.remove(f"{output_directory}/missing_incidents.yaml")
        # clear cached_violations if it is not None
        if self.cached_violations is not None:
            self.cached_violations = {}

    def load_incident_store(self):
        # check if the folder exists
        folder_path = self.analysis_dir
        if not os.path.exists(folder_path):
            print(f"Error: {folder_path} does not exist.")
            return None
        # check if the folder is empty
        if not os.listdir(folder_path):
            print(f"Error: {folder_path} is empty.")
            return None
        apps = os.listdir(folder_path)
        print(f"Loading incident store with applications: {apps}\n")
        if len(apps) != 0:
            # cleanup incident store
            self.cleanup()

        for app in apps:
            # if app is a directory then check if there is a folder called initial
            app_path = os.path.join(folder_path, app)
            if os.path.isdir(app_path):
                initial_folder = os.path.join(app_path, "initial")
                if not os.path.exists(initial_folder):
                    print(f"Error: {initial_folder} does not exist.")
                    return None
                # check if the folder is empty
                if not os.listdir(initial_folder):
                    print(f"Error: No analysis report found in {initial_folder}.")
                    return None
                print(f"Loading application {app}\n")
                _ = self.load_app_cached_violation(app, "initial")
                print(f"Loaded application {app}\n")

        for app in apps:
            solved_folder = os.path.join(folder_path, app, "solved")
            if os.path.exists(solved_folder) and os.listdir(solved_folder):
                print("finding missing incidents")
                self.update_incident_store(app)

        self.write_cached_violations(self.cached_violations, "cached_violations.yaml")
        # write missing incidents to the a new file
        self.write_cached_violations(self.missing_violations, "missing_incidents.yaml")
        self.write_cached_violations(self.solved_violations, "solved_incidents.yaml")

    def load_app_cached_violation(self, app: str, folder):
        """
        Load the incident store with the given applications
        """

        print(f"Loading application {app}\n")
        output_yaml = self.fetch_output_yaml(app, folder)
        if output_yaml is None:
            print(f"Error: output.yaml does not exist for {app}.")
            return None
        self.add_app_to_incident_store(app, output_yaml)
        # self.write_cached_violations(self.cached_violations, "cached_violations.yaml")
        return self.cached_violations

    def fetch_output_yaml(self, app_name: str, folder: str = "solved") -> str:
        """
        Fetch the output and app yaml for the given application
        """
        # Path to the analysis_reports directory
        analysis_reports_dir = self.analysis_dir

        # Check if the specified app folder exists
        app_folder = os.path.join(analysis_reports_dir, app_name)
        if not os.path.exists(app_folder):
            print(
                f"Error: {app_name} does not exist in the analysis_reports directory."
            )
            return None

        # Path to the output.yaml file
        output_yaml_path = os.path.join(app_folder, folder, "output.yaml")

        # Check if output.yaml exists for the specified app
        if not os.path.exists(output_yaml_path):
            print(f"Error: output.yaml does not exist for {app_name}.")
            return None

        return output_yaml_path

    def write_cached_violations(self, cached_violations, file_name):
        """
        Write the cached_violations to a file for later use
        """
        output_directory = self.output_dir
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(dir_path)
        os.path.join(parent_dir, output_directory)
        os.makedirs(
            output_directory, exist_ok=True
        )  # Create the directory if it doesn't exist
        output_file_path = os.path.join(output_directory, file_name)

        mode = "w" if not os.path.exists(output_file_path) else "a"
        with open(output_file_path, mode) as f:
            yaml.dump(cached_violations, f)

        if mode == "w":
            print(f"Written cached_violations to {output_file_path}\n")
        else:
            print(f"Appended cached_violations to {output_file_path}\n")

    # determine if new application analysis report is available
    def is_new_analysis_report_available(self, application):
        # Todo: query hub api for the application
        # if the timestamp is newer than the current timestamp
        # return true
        # else return false
        # app1 = IncidentStore.get_app_from_konveyor_hub(application.name)
        # if app1 is not None:
        # if app1.timestamp > application.timestamp:
        # return app1.timestamp
        # return None

        # fetch app.yaml from the analysis_reports directory
        app_variables = self.get_app_variables(application.name)
        if app_variables is not None:
            if app_variables["timestamp"] > application.timestamp:
                return app_variables["timestamp"]
        return None

    # update the timestamp in app.yaml if new analysis report is available
    # It is a WORKAROUND until we retrieve data from the hub api
    def update_timestamp(application):
        # query hub api for the application
        # if the timestamp is newer than the current timestamp
        # update the timestamp in app.yaml
        # return true
        # else return false
        if IncidentStore.is_new_analysis_report_available(application) is not None:
            # update the timestamp in app.yaml
            # Path to the analysis_reports directory
            analysis_reports_dir = "samples/analysis_reports"

            # Check if the specified app folder exists
            app_folder = os.path.join(analysis_reports_dir, application.name)
            if not os.path.exists(app_folder):
                print(
                    f"Error: {application.name} does not exist in the analysis_reports directory."
                )
                return False

            # Load contents of app.yaml
            app_yaml_path = os.path.join(app_folder, "app.yaml")
            if not os.path.exists(app_yaml_path):
                print(f"Error: app.yaml does not exist for {application.name}.")
                return False
            # open the file in write mode and update the timestamp field
            with open(app_yaml_path, "r") as app_yaml_file:
                app_yaml_data = yaml.safe_load(app_yaml_file)

            # Update the timestamp in the app.yaml data
            app_yaml_data["timestamp"] = application.timestamp

            # Write the updated contents back to app.yaml
            with open(app_yaml_path, "w") as app_yaml_file:
                yaml.dump(app_yaml_data, app_yaml_file)

            # Return true
            return True
        return False

    def get_cached_violations(self, filename):
        """
        Load the cached_violations from a file
        """

        output_directory = self.output_dir
        output_file_path = os.path.join(output_directory, filename)
        print(f"Loading incident store from file: {filename}\n")
        # check if the file is present
        if not os.path.exists(output_file_path):
            print(f"Error: {output_file_path} does not exist.")
            return None

        # check if the contents of the file is not empty
        if os.stat(output_file_path).st_size == 0:
            print(f"Error: {output_file_path} is empty.")
            return None

        # load the contents of the file
        with open(output_file_path, "r") as f:
            self.cached_violations = yaml.safe_load(f)

        print(f"Loaded incident store from file: {output_file_path}\n")

        return self.cached_violations

    def create_temp_cached_violations(self, app_name, report):
        """
        Create a temporary cached_violations for the given application

        """
        temp_cached_violations = {}
        for ruleset in report.keys():
            if ruleset not in temp_cached_violations:
                temp_cached_violations[ruleset] = {}
            for violation_name in report[ruleset]["violations"].keys():
                if violation_name not in temp_cached_violations[ruleset]:
                    temp_cached_violations[ruleset][violation_name] = {}
                    # Assume there can be multiple incidents of the same violation in same file

                    incidents = report[ruleset]["violations"][violation_name].get(
                        "incidents", None
                    )
                if incidents is None:

                    print(
                        f"Found no incidents for '{app_name}' with {ruleset} and {violation_name}"
                    )
                    continue
                for incident in incidents:
                    if app_name not in temp_cached_violations[ruleset][violation_name]:
                        temp_cached_violations[ruleset][violation_name][app_name] = {}
                    uri = incident.get("uri", None)
                    if uri is None:

                        print(
                            f"'{app_name}' with {ruleset} and {violation_name}, incident has no 'uri'"
                        )
                        continue
                    file_path = Report.get_cleaned_file_path(uri)
                    if (
                        file_path
                        not in temp_cached_violations[ruleset][violation_name][app_name]
                    ):
                        temp_cached_violations[ruleset][violation_name][app_name][
                            file_path
                        ] = []
                    # Remember for future matches we need to take into account the variables
                    entry = {
                        "variables": copy.deepcopy(incident.get("variables", {})),
                        "line_number": incident.get("lineNumber", None),
                        "message": incident.get("message", None),
                    }
                    temp_cached_violations[ruleset][violation_name][app_name][
                        file_path
                    ].append(entry)
        return temp_cached_violations

    def update_incident_store(self, app_name):
        """
        Update the incident store with the given application
        Find missing and solved incidents
        Add new incidents to the cached_violations
        """

        cached_violations = self.cached_violations

        print(f"Updating incident store with application {app_name}\n")
        output_yaml = self.fetch_output_yaml(app_name)
        if output_yaml is None:
            print(f"Error: output.yaml does not exist for {app_name}.")
            return None
        temp_report = Report(output_yaml).get_report()
        report = self.create_temp_cached_violations(app_name, temp_report)
        self.missing_violations = self.get_missing_incidents(app_name, report)

        self.solved_violations = self.find_solved_issues(app_name)

        for ruleset in report.keys():
            if ruleset not in cached_violations:
                cached_violations[ruleset] = {}

            for violation_name in report[ruleset].keys():
                if violation_name not in cached_violations[ruleset]:
                    cached_violations[ruleset][violation_name] = {}

                for app in report[ruleset][violation_name].keys():
                    if app not in cached_violations[ruleset][violation_name]:
                        cached_violations[ruleset][violation_name][app] = {}

                    for file_path in report[ruleset][violation_name][app].keys():
                        if (
                            file_path
                            not in cached_violations[ruleset][violation_name][app]
                        ):
                            cached_violations[ruleset][violation_name][app][
                                file_path
                            ] = []

                        existing_incidents = cached_violations[ruleset][violation_name][
                            app
                        ][file_path]

                        for incident in report[ruleset][violation_name][app][file_path]:
                            # Check if the incident is a duplicate
                            is_duplicate = False
                            for existing_incident in existing_incidents:
                                if (
                                    existing_incident["variables"]
                                    == incident["variables"]
                                    and existing_incident["line_number"]
                                    == incident["line_number"]
                                ):
                                    is_duplicate = True
                                    # print(f"skip duplicate incident: {existing_incident}\n")
                                    break

                            if not is_duplicate:
                                self.cached_violations[ruleset][violation_name][app][
                                    file_path
                                ].append(incident)

        return self.cached_violations

    # find the missing incidents from self.cached_violations
    def get_missing_incidents(self, app_name, new_report):
        """
        Compare the new report with the cached_violations to find the missing incidents from cached_violations
        """

        # get commit_id from app.yaml
        app_variables = self.get_app_variables(app_name)

        for ruleset in self.cached_violations.keys():
            for violation in self.cached_violations[ruleset].keys():
                for app in self.cached_violations[ruleset][violation].keys():
                    if app == app_name:
                        for file_path in self.cached_violations[ruleset][violation][
                            app
                        ].keys():
                            if new_report is not None:
                                new_incidents = (
                                    new_report.get(ruleset, {})
                                    .get(violation, {})
                                    .get(app_name, {})
                                    .get(file_path, [])
                                )
                            else:
                                new_incidents = []
                            for incident in self.cached_violations[ruleset][violation][
                                app
                            ][file_path]:
                                if incident not in new_incidents:
                                    if ruleset not in self.missing_violations:
                                        self.missing_violations[ruleset] = {}
                                    if (
                                        violation
                                        not in self.missing_violations[ruleset]
                                    ):
                                        self.missing_violations[ruleset][violation] = {}
                                    if (
                                        app
                                        not in self.missing_violations[ruleset][
                                            violation
                                        ]
                                    ):
                                        self.missing_violations[ruleset][violation][
                                            app
                                        ] = {}
                                    if (
                                        file_path
                                        not in self.missing_violations[ruleset][
                                            violation
                                        ][app]
                                    ):
                                        self.missing_violations[ruleset][violation][
                                            app
                                        ][file_path] = []
                                    self.missing_violations[ruleset][violation][app][
                                        file_path
                                    ].append(
                                        {
                                            "variables": incident["variables"],
                                            "line_number": incident["line_number"],
                                            "message": incident["message"],
                                            "repo": app_variables["repo"],
                                            "initial_branch": app_variables[
                                                "initial_branch"
                                            ],
                                            "solved_branch": app_variables[
                                                "solved_branch"
                                            ],
                                        }
                                    )

        return self.missing_violations

    def find_solved_issues(self, app_name):
        """
        Find solved issues from the missing incidents
        """

        # for every missing incident, find the solved issue
        for ruleset in self.missing_violations.keys():
            for violation in self.missing_violations[ruleset].keys():
                for app in self.missing_violations[ruleset][violation].keys():
                    if app == app_name:
                        for file_path in self.missing_violations[ruleset][violation][
                            app
                        ].keys():
                            for incident in self.missing_violations[ruleset][violation][
                                app
                            ][file_path]:
                                # find the solved issue
                                scm = GitDiff(IncidentStore.get_repo_path(app))

                                diff_exists = scm.diff_exists_for_file(
                                    scm.get_commit_from_branch(
                                        incident["initial_branch"]
                                    ),
                                    scm.get_commit_from_branch(
                                        incident["solved_branch"]
                                    ),
                                    file_path,
                                )
                                if diff_exists:
                                    if ruleset not in self.solved_violations:
                                        self.solved_violations[ruleset] = {}
                                    if violation not in self.solved_violations[ruleset]:
                                        self.solved_violations[ruleset][violation] = {}
                                    if (
                                        app
                                        not in self.solved_violations[ruleset][
                                            violation
                                        ]
                                    ):
                                        self.solved_violations[ruleset][violation][
                                            app
                                        ] = {}
                                    if (
                                        file_path
                                        not in self.solved_violations[ruleset][
                                            violation
                                        ][app]
                                    ):
                                        self.solved_violations[ruleset][violation][app][
                                            file_path
                                        ] = []
                                    self.solved_violations[ruleset][violation][app][
                                        file_path
                                    ].append(incident)
        return self.solved_violations

    def get_repo_path(app_name):
        """
        Get the repo path
        """

        # TODO:  This mapping data should be moved out of the code, consider moving to a config file
        mapping = {
            "eap-coolstore-monolith": "samples/sample_repos/eap-coolstore-monolith",
            "ticket-monster": "samples/sample_repos/ticket-monster",
            "kitchensink": "samples/sample_repos/kitchensink",
            "helloworld-mdb": "samples/sample_repos/helloworld-mdb",
            "bmt": "samples/sample_repos/bmt",
            "cmt": "samples/sample_repos/cmt",
            "ejb-remote": "samples/sample_repos/ejb-remote",
            "ejb-security": "samples/sample_repos/ejb-security",
            "tasks-qute": "samples/sample_repos/tasks-qute",
            "greeter": "samples/sample_repos/greeter",
        }

        basedir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(basedir)
        path = mapping.get(app_name, None)
        return os.path.join(parent_dir, path)

    def find_if_solved_issues_exist(self):
        """
        Find if solved issues exist
        """
        output_directory = self.output_dir
        # check if file solved_incidents.yaml exists
        if not os.path.exists(f"{output_directory}/solved_incidents.yaml"):
            return False
        if os.stat(f"{output_directory}/solved_incidents.yaml").st_size == 0:
            return False
        return True

    def get_solved_issue(self, ruleset, violation):
        """
        For the given ruleset and violation, return the solved issue(s) if it exists
        """
        patches = []

        # Check if solved issues exist
        if not self.find_if_solved_issues_exist():
            return None

        # Load the solved issues
        solved_issues = self.get_cached_violations("solved_incidents.yaml")

        # Iterate over the solved issues to find the match
        if ruleset in solved_issues and violation in solved_issues[ruleset]:
            for app, app_data in solved_issues[ruleset][violation].items():
                print(f"Found solved issues for {ruleset} - {violation} for app {app}")

                for file_path, incidents in app_data.items():
                    for incident in incidents:
                        scm = GitDiff(IncidentStore.get_repo_path(app))
                        patches.append(
                            scm.get_patch_for_file(
                                scm.get_commit_from_branch(incident["initial_branch"]),
                                scm.get_commit_from_branch(incident["solved_branch"]),
                                file_path,
                            )
                        )

                        # If a match is found, break out of the loop
                        break
                    else:
                        continue
        return patches

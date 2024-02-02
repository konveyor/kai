__all__ = ["Application", "IncidentStore"]

import copy
import os
import pprint

import yaml

from kai.git import GitHelper
from kai.report import Report


class Application:
    def __init__(
        self,
        name,
        report,
        repo=None,
        initial_branch=None,
        solved_branch=None,
        commitId=None,
        timestamp=None,
    ):
        self.name = name
        self.report = report
        self.repo = repo
        self.initial_branch = initial_branch
        self.solved_branch = solved_branch
        self.commitId = commitId
        self.timestamp = timestamp


class IncidentStore:
    def __init__(self):
        # applications, keyed on App Name
        self.applications = {}
        # cached_violations is defined in comments in self._update_cached_violations
        self.cached_violations = {}
        self.pp = pprint.PrettyPrinter(indent=2)

    def add_app_to_incident_store(self, app_name, yaml):
        r = Report(yaml).get_report()
        app_variables = IncidentStore.get_app_variables(app_name)
        a = Application(
            app_name,
            r,
            app_variables.get("repo", None),
            app_variables.get("initial_branch", None),
            app_variables.get("solved_branch", None),
            app_variables.get("commitId", None),
            app_variables.get("timestamp", None),
        )
        self.applications[app_name] = a
        self._update_cached_violations(a)

    def get_app_from_incident_store(self, app_name):
        return self.applications[app_name]

    def get_app_names_from_incident_store(self):
        return self.applications.keys()

    # todo query hub api for the application
    def get_app_from_konveyor_hub(self, name):
        # query hub api for the application
        # return the application
        if self.applications[name] is None:
            return None
        else:
            app = self.applications[name]
            # todo: query hub api for the application
            # populate the application with the hub api data
            return app

    # get the app variables from the app.yaml
    def get_app_variables(app_name):
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
            app_data = yaml.safe_load(app_yaml_file)

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
                            commitId: str
                        } ]
                    }
               }
           }
         }

        """
        ### Add our Application's Name to the cached_violations
        # self.pp.pprint(a.report)

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
                        "commitId": a.commitId,
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
        if self.cached_violations is None:
            self.get_cached_violations()
        # check the loaded cached_violations and see if its empty
        if self.cached_violations is None:
            return None
        ruleset = self.cached_violations.get(ruleset_name, None)
        if ruleset is None:
            print(f"Unable to find cached_violations for ruleset: '{ruleset_name}'")
            return None
        entry = ruleset.get(violation_name, None)
        if entry is None:
            print(
                f"Unable to find a match of ruleset: '{ruleset_name}' and violation_name: '{violation_name}'"
            )
            return None
        # print(f"Found a match of ruleset: '{ruleset_name}' and violation_name: '{violation_name}': entry is '{entry}'")
        # print(f"DeepCopy = {copy.deepcopy(entry)}")
        # Make   a deepcopy of entries
        return copy.deepcopy(entry)

    def load_app_cached_violation(self, apps):
        """
        Load the incident store with the given applications
        """

        print(f"Loading incident store with {len(apps)} applications\n")
        for app in apps:
            print(f"Loading application {app}\n")
            output_yaml = self.fetch_output_yaml(app)
            if output_yaml is None:
                print(f"Error: output.yaml does not exist for {app}.")
                return None
            self.add_app_to_incident_store(app, output_yaml)
        print(f"Loaded incident store with {len(apps)} applications\n")
        return self.cached_violations

    def fetch_output_yaml(self, app_name):
        """
        Fetch the output and app yaml for the given application
        """
        # Path to the analysis_reports directory
        analysis_reports_dir = "samples/analysis_reports"

        # Check if the specified app folder exists
        app_folder = os.path.join(analysis_reports_dir, app_name)
        if not os.path.exists(app_folder):
            print(
                f"Error: {app_name} does not exist in the analysis_reports directory."
            )
            return None

        # Path to the output.yaml file
        output_yaml_path = os.path.join(app_folder, "output.yaml")

        # Check if output.yaml exists for the specified app
        if not os.path.exists(output_yaml_path):
            print(f"Error: output.yaml does not exist for {app_name}.")
            return None

        return output_yaml_path

    def write_cached_violations(self, cached_violations, file_name):
        """
        Write the cached_violations to a file for later use
        """

        output_directory = "samples/generated_output/incident_store"
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
    def is_new_analysis_report_available(application):
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
        app_variables = IncidentStore.get_app_variables(application.name)
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

    def get_cached_violations(self):
        """
        Load the cached_violations from a file
        """

        output_directory = "samples/generated_output/incident_store"
        output_file_path = os.path.join(output_directory, "cached_violations.yaml")

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

    def create_temp_cached_violations(app_name, report):
        """
        Create a temporary cached_violations for the given application

        """
        app_variables = IncidentStore.get_app_variables(app_name)
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
                    # self.pp.pprint(a.report[ruleset]["violations"])
                    print(
                        f"Found no incidents for '{app_name}' with {ruleset} and {violation_name}"
                    )
                    continue
                for incident in incidents:
                    if app_name not in temp_cached_violations[ruleset][violation_name]:
                        temp_cached_violations[ruleset][violation_name][app_name] = {}
                    uri = incident.get("uri", None)
                    if uri is None:
                        # self.pp.pprint(incident)
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
                        "commitId": app_variables["commitId"],
                    }
                    temp_cached_violations[ruleset][violation_name][app_name][
                        file_path
                    ].append(entry)

    def update_incident_store(self, app_name):
        """
        Update the incident store with the given application
        """

        cached_violations = self.get_cached_violations()

        print(f"Updating incident store with application {app_name}\n")
        output_yaml = self.fetch_output_yaml(app_name)
        if output_yaml is None:
            print(f"Error: output.yaml does not exist for {app_name}.")
            return None
        temp_report = Report(output_yaml).get_report()
        report = IncidentStore.create_temp_cached_violations(app_name, temp_report)
        missing_incidents = self.get_missing_incidents(app_name, report)

        # write missing incidents to the a new file
        self.write_cached_violations(missing_incidents, "missing_incidents.yaml")
        solved_issues = self.find_solved_issues(missing_incidents)
        self.write_cached_violations(solved_issues, "solved_incidents.yaml")

        for ruleset in report.keys():
            if ruleset not in cached_violations:
                cached_violations[ruleset] = {}
            for violation_name in report[ruleset]["violations"].keys():
                if violation_name not in cached_violations[ruleset]:
                    cached_violations[ruleset][violation_name] = {}
                for app in cached_violations[ruleset][violation_name].keys():
                    if app == app_name:
                        for file_path in cached_violations[ruleset][violation_name][
                            app
                        ].keys():
                            if (
                                file_path
                                not in cached_violations[ruleset][violation_name][app]
                            ):
                                cached_violations[ruleset][violation_name][app][
                                    file_path
                                ] = []
                            existing_incidents = cached_violations[ruleset][
                                violation_name
                            ][app][file_path]
                            incidents = report[ruleset][violation_name].keys()
                            for incident in incidents:
                                # only match if variables and line number are same as the cached incident, if so skip

                                for existing_incident in existing_incidents:
                                    if (
                                        existing_incident["variables"]
                                        == incident["variables"]
                                        and existing_incident["line_number"]
                                        == incident["line_number"]
                                    ):
                                        continue
                                    else:
                                        cached_violations[ruleset][violation_name][app][
                                            file_path
                                        ].append(incident)

        self.write_cached_violations(cached_violations, "cached_violations.yaml")
        print(f"Updated incident store with new issues for application {app_name}\n")

    # find the missing incidents from self.cached_violations
    def get_missing_incidents(self, app_name, new_report):
        """
        Compare the new report with the cached_violations to find the missing incidents from cached_violations
        """

        # get commit_id from app.yaml
        app_variables = IncidentStore.get_app_variables(app_name)
        commit_id = app_variables["commitId"]

        # find the missing incidents
        missing_incidents = {}
        for ruleset in self.cached_violations.keys():
            for violation in self.cached_violations[ruleset].keys():
                for app in self.cached_violations[ruleset][violation].keys():
                    if app == app_name:
                        for file_path in self.cached_violations[ruleset][violation][
                            app
                        ].keys():
                            new_incidents = (
                                new_report.get(ruleset, {})
                                .get(violation, {})
                                .get(app_name)
                                .get(file_path, [])
                            )
                            for incident in self.cached_violations[ruleset][violation][
                                app
                            ][file_path]:
                                if incident not in new_incidents:
                                    if ruleset not in missing_incidents:
                                        missing_incidents[ruleset] = {}
                                    if violation not in missing_incidents[ruleset]:
                                        missing_incidents[ruleset][violation] = {}
                                    if app not in missing_incidents[ruleset][violation]:
                                        missing_incidents[ruleset][violation][app] = {}
                                    if (
                                        file_path
                                        not in missing_incidents[ruleset][violation][
                                            app
                                        ]
                                    ):
                                        missing_incidents[ruleset][violation][app][
                                            file_path
                                        ] = []
                                    missing_incidents[ruleset][violation][app][
                                        file_path
                                    ].append(
                                        {
                                            "variables": incident["variables"],
                                            "line_number": incident["line_number"],
                                            "message": incident["message"],
                                            "commitId": app.get("commitId", None),
                                            "new_commitId": commit_id,
                                            "repo": app_variables["repo"],
                                            "initial_branch": app_variables[
                                                "initial_branch"
                                            ],
                                            "solved_branch": app_variables[
                                                "solved_branch"
                                            ],
                                        }
                                    )

        return missing_incidents

    def find_solved_issues(self, missing_incidents):
        """
        Find solved issues from the missing incidents
        """
        solved_issues = {}

        # for every missing incident, find the solved issue
        for ruleset in missing_incidents.keys():
            for violation in missing_incidents[ruleset].keys():
                for app in missing_incidents[ruleset][violation].keys():
                    repo_path = IncidentStore.get_repo_path(app)
                    for file_path in missing_incidents[ruleset][violation][app].keys():
                        for incident in missing_incidents[ruleset][violation][app][
                            file_path
                        ]:
                            # find the solved issue
                            git_helper = GitHelper(
                                incident["repo"],
                                repo_path,
                                incident["initial_branch"],
                                incident["solved_branch"],
                                incident["commitId"],
                                incident["new_commitId"],
                            )
                            diff_exists = git_helper.get_diff_for_file(file_path)
                            if diff_exists:
                                if ruleset not in solved_issues:
                                    solved_issues[ruleset] = {}
                                if violation not in solved_issues[ruleset]:
                                    solved_issues[ruleset][violation] = {}
                                if app not in solved_issues[ruleset][violation]:
                                    solved_issues[ruleset][violation][app] = {}
                                if (
                                    file_path
                                    not in solved_issues[ruleset][violation][app]
                                ):
                                    solved_issues[ruleset][violation][app][
                                        file_path
                                    ] = []
                                solved_issues[ruleset][violation][app][
                                    file_path
                                ].append(incident)
        self.write_cached_violations(solved_issues, "solved_incidents.yaml")
        return solved_issues

    def get_repo_path(app_name):
        """
        Get the repo path
        """
        repo_dir = "sample_repo/{app_name}"
        if not os.path.exists(repo_dir):
            return None
        return repo_dir

    def find_if_solved_issues_exist(solved_issues):
        """
        Find if solved issues exist
        """

        if solved_issues:
            return True
        return False

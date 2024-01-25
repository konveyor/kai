__all__ = ['ApplicationHub', 'Application']

import copy
import os
import shutil
import yaml 
import pprint

from io import StringIO
from kai.report import Report
from kai.scm import GitDiff

class Application:
    def __init__(self, name, report, repo, 
                initial_branch, solved_branch):
        self.name = name
        self.report = report
        self.repo = repo
        self.initial_branch = initial_branch
        self.solved_branch = solved_branch
        
class ApplicationHub:
    def __init__(self):
        # applications, keyed on App Name        
        self.applications = {}
        # cached_violations is defined in comments in self._update_cached_violations
        self.cached_violations = {}
        self.pp = pprint.PrettyPrinter(indent=2)
    
    def add_application(self, name, yaml, repo, 
                        initial_branch="main", 
                        solved_branch=None):
        """
        Add an analysis to consider
        """
        # Verify repo, initial_branch, and solved_branch if valid
        gd = GitDiff(repo)
        #print(f"Checking {repo} has branches:  {gd.get_branches()}  ")
        try:
            #print(f"Checking {initial_branch} in {repo}")
            gd.get_commit_from_branch(initial_branch)
        except:
            raise FileNotFoundError(f"Branch {initial_branch} not found in {repo}") 
        
        if solved_branch:
            try:
                #print(f"Checking {initial_branch} in {repo}")
                gd.get_commit_from_branch(solved_branch)
            except:
                raise FileNotFoundError(f"Branch {initial_branch} not found in {repo}")

        report = Report(yaml).get_report()
        a = Application(name, report, repo, initial_branch, solved_branch)
        self.applications[name] = a
        self._update_cached_violations(a)
    
    def get_application(self, name):
        return self.applications[name]
    
    def get_application_names(self):
        return self.applications.keys()
    
    def find_common_violation(self, ruleset_name, violation_name):
        """     
        Find the common violation across all applications
        Returns:
            None        - if no common violation
            {}          - if a common violation is found
        """
        if self.cached_violations is None:
            return None
        ruleset = self.cached_violations.get(ruleset_name, None)
        if ruleset is None:
            print(f"Unable to find cached_violations for ruleset: '{ruleset_name}'")
            return None
        entry = self.cached_violations[ruleset_name].get(violation_name, None) 
        if entry is None:
            print(f"Unable to find a match of ruleset: '{ruleset_name}' and violation_name: '{violation_name}'") 
            return None
        #print(f"Found a match of ruleset: '{ruleset_name}' and violation_name: '{violation_name}': entry is '{entry}'") 
        #print(f"DeepCopy = {copy.deepcopy(entry)}")
        # Make   a deepcopy of entries
        return copy.deepcopy(entry)     


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
                        } ]
                    }
               }
           }
         }

        """
        ### Add our Application's Name to the cached_violations
        #self.pp.pprint(a.report)

        for ruleset in a.report.keys():
            if ruleset not in self.cached_violations:
                self.cached_violations[ruleset] = {}
            for violation_name in a.report[ruleset]['violations'].keys():
                if violation_name not in self.cached_violations[ruleset]:
                    self.cached_violations[ruleset][violation_name] = {}
                # Assume there can be multiple incidents of the same violation in same file
                ## Example of the YAML report data for an incident
                ##  incidents:
                ##  - uri: file:///tmp/source-code/src/main/webapp/WEB-INF/web.xml
                ##    message: "\n Session replication ensures that client sessions are not disrupted by node failure. Each node in the cluster shares information about ongoing sessions and can take over sessions if another node disappears. In a cloud environment, however, data in the memory of a running container can be wiped out by a restart.\n\n Recommendations\n\n * Review the session replication usage and ensure that it is configured properly.\n * Disable HTTP session clustering and accept its implications.\n * Re-architect the application so that sessions are stored in a cache backing service or a remote data grid.\n\n A remote data grid has the following benefits:\n\n * The application is more scaleable and elastic.\n * The application can survive EAP node failures because a JVM failure does not cause session data loss.\n * Session data can be shared by multiple applications.\n "
                ##    variables:
                ##      data: distributable
                ##      innerText: ""
                ##      matchingXML: ""
                ##
                incidents = a.report[ruleset]['violations'][violation_name].get('incidents', None)
                if incidents is None:
                    self.pp.pprint(a.report[ruleset]['violations'])
                    print(f"Found no incidents for '{a.name}' with {ruleset} and {violation_name}")
                    continue
                for incident in incidents:
                    if a.name not in self.cached_violations[ruleset][violation_name]:
                        self.cached_violations[ruleset][violation_name][a.name] = {}
                    uri = incident.get('uri', None)
                    if uri is None:
                        self.pp.pprint(incident)
                        print(f"'{a.name}' with {ruleset} and {violation_name}, incident has no 'uri'")
                        continue 
                    file_path = Report.get_cleaned_file_path(uri)
                    if file_path not in self.cached_violations[ruleset][violation_name][a.name]:
                        self.cached_violations[ruleset][violation_name][a.name][file_path] = []
                    # Remember for future matches we need to take into account the variables
                    entry = {
                        'variables': copy.deepcopy(incident.get('variables', {})),
                        'line_number': incident.get('lineNumber', None),
                        'message': incident.get('message', None)
                    }
                    self.cached_violations[ruleset][violation_name][a.name][file_path].append(entry)    
                    

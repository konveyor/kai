__all__ = ["LLMResult"]

import logging
import os

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from .report import Report
from .scm import GitDiff


class LLMResult:
    """The intent of this class is to help us form several Prompt examples using a single application
    which we have already migrated.  We are using this single application and picking a few
    violations our analyzer finds and then will construct a few prompt examples to assess the
    quality of response from a LLM

    We are assuming for the sample application that it is:
    - In a single git repo
    - It has 2 branches
        - One of which is the original state (Java EE) and
        - the other is the solved state (Quarkus)

    We will begin with the 'JavaEE' branch and if we find a violation that has
    2 or more incidents we will generate a patch for the first incident and use the
    2nd incident as the 'solved' example.  This is done to simulate what we can
    accomplish in Konveyor when we have access to the entire application portfolio
    whereby we will have a larger number of solved incidents we can find from other
    applications which have been migrated.
    """

    def __init__(self, source_dir, initial_branch, solved_branch):
        """We expect to have 1 directory that represents the example application and 2 branches

        - source_dir:       path to git repo for example
        - initial_branch    branch name for initial state of example
        - solved_branch     branch name for solved state of example
        """
        self.example_source_dir = source_dir
        self.example_initial_branch = initial_branch
        self.example_solved_branch = solved_branch
        self.path_to_report = None
        self.report = None

    def parse_report(self, path_to_report):
        self.report = Report(path_to_report).get_report()

    def get_prompt_template(self):
        rel_dir = os.path.dirname(__file__)
        template_file = os.path.join(rel_dir, "data/templates/template_02.txt")
        print(f"Loading template from {template_file}")
        with open(template_file, "r") as f:
            template = f.read()
        return PromptTemplate.from_template(template)

    def _extract_diff(self, text: str):
        try:
            _, after = text.split("```diff")
            return after.split("```")[0]
        except Exception as e:
            print(f"Error: {e}")
            return "Error: Unable to extract diff"

    def create_prompt(self, description, incidents, template):
        # To form a prompt we need:
        template = self.get_prompt_template()
        print(f"{len(incidents)} incidents:  {description}\n")

    def _update_uri(self, uri):
        logging.debug(f"Updating uri {uri}")
        f = uri.replace("file:///tmp/source-code/", "")
        logging.debug(f"Updated uri {f}")
        # Skip any incident that begins with 'target/'
        # Related to: https://github.com/konveyor/analyzer-lsp/issues/358
        return f if not f.startswith("target/") else None

    def _ensure_output_dir_exists(self, output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as error:
            print(f"Error creating directory {output_dir}: {error}")
            raise error

    def _write_output(self, filename, content):
        with open(filename, "w") as f:
            # We want to start each run with a clean file
            f.truncate(0)
            f.write(content)

    def process(
        self,
        path_to_output,
        model_name="",
        limit_to_rulesets=None,
        limit_to_violations=None,
    ):
        if self.report is None:
            raise Exception("No report to process.  Please parse a report first")

        # We want to be able to pass in either '[]' or 'None' to signify we want to run all
        if limit_to_rulesets == []:
            limit_to_rulesets = None
        if limit_to_violations == []:
            limit_to_violations = None

        # Create result directory
        self._ensure_output_dir_exists(path_to_output)
        gd = GitDiff(self.example_source_dir)

        for ruleset_name in self.report.keys():
            if limit_to_rulesets is not None and ruleset_name not in limit_to_rulesets:
                print(f"Skipping {ruleset_name} as it is not in {limit_to_rulesets}")
                continue
            ruleset = self.report[ruleset_name]
            ruleset_name_display = ruleset_name.replace("/", "_")
            print(f"Processing {ruleset_name} {ruleset_name_display}")
            for count, key in enumerate(ruleset["violations"]):
                if limit_to_violations is not None and key not in limit_to_violations:
                    print(f"Skipping {key} as it is not in {limit_to_violations}")
                    continue

                ###############################################################
                # For each violation, we will form only 1 prompt
                # If we have 2 incidents, we will use second as a 'solved' example, looking at the
                # other repo which has the solved code present
                # Otherwise we will just send the prompt with the first incident
                #
                # Note this only a POC so we are intentionally ignoring other incidents that
                # would need to be solved.
                ###############################################################
                items = ruleset["violations"][key]

                if len(items["incidents"]) == 0:
                    # No incidents so skip this iteration
                    continue

                description = items["description"]
                # TODO
                # Don't use the codeSnip from the report, get the code from Git and use the linenumber
                # We want to avoide the line number printed on each line of code snip, worried it will impact
                # the diff we get back from LLM
                # current_issue_original_code =  items['incidents'][0].get('codeSnip', None)
                lineNumber = items["incidents"][0].get("lineNumber", None)
                current_issue_filename = self._update_uri(items["incidents"][0]["uri"])
                if current_issue_filename is None:
                    continue
                current_issue_message = items["incidents"][0].get("message", None)
                print(
                    f"Fetching original code for {current_issue_filename} in branch {self.example_initial_branch}"
                )
                current_issue_original_code = gd.get_file_contents(
                    current_issue_filename, self.example_initial_branch
                )

                solved_example_filename = ""
                solved_example_diff = ""
                if len(items["incidents"]) > 1:
                    ###
                    # NOTE:  We are skipping the lineNumber at present, we aren't actually
                    # using it to adjust what what we pass into the prompt.
                    # We are experimenting with the diff for right now
                    ###
                    example_lineNumber = items["incidents"][1].get("lineNumber", None)
                    solved_example_filename = self._update_uri(
                        items["incidents"][1]["uri"]
                    )
                    if solved_example_filename is None:
                        continue
                    try:
                        commit_initial = gd.get_commit_from_branch(
                            self.example_initial_branch
                        )
                        commit_solved = gd.get_commit_from_branch(
                            self.example_solved_branch
                        )
                        solved_example_diff = gd.get_patch_for_file(
                            commit_initial.hexsha,
                            commit_solved.hexsha,
                            solved_example_filename,
                        )
                        # example_original_code = GitDiff(self.path_original_source).get_file_contents(example_original_filename)
                    except Exception as e:
                        print(f"Unable to find a solved_example_diff.  Error: {e}")
                        solved_example_diff = ""
                print(f"Processing {ruleset_name} {key} {count}")
                prompt = self.get_prompt_template()
                template_args = {
                    "description": description,
                    "current_issue_filename": current_issue_filename,
                    "current_issue_message": current_issue_message,
                    "current_issue_original_code": current_issue_original_code,
                    "solved_example_filename": solved_example_filename,
                    "solved_example_diff": solved_example_diff,
                }
                formatted_prompt = prompt.format(**template_args)
                # self._write_output(f"./results/{ruleset_name_display}_{key}_{count}_template.txt", formatted_prompt)

                llm = ChatOpenAI(temperature=0.1, model_name=model_name)
                chain = LLMChain(llm=llm, prompt=prompt)
                result = chain.run(template_args)
                result_diff = self._extract_diff(result)

                # Create result directory
                self._ensure_output_dir_exists(os.path.join(path_to_output, model_name))
                f_name = os.path.join(
                    path_to_output,
                    model_name,
                    f"{ruleset_name_display}_{key}_{count}_full_run.md",
                )
                with open(f_name, "w") as f:
                    f.truncate(0)
                    f.write(f"## Prompt:\n")
                    f.write(f"{formatted_prompt}\n")
                    f.write(f"\n\n## Result:\n")
                    f.write(f"{result}\n\n")

                d_name = f_name = os.path.join(
                    path_to_output,
                    model_name,
                    f"{ruleset_name_display}_{key}_{count}.diff",
                )
                with open(d_name, "w") as f:
                    f.truncate(0)
                    f.write(result_diff)

        print(f"Process complete")

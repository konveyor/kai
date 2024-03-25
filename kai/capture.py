import json
import os
import pprint
from collections import defaultdict
from dataclasses import dataclass, field

# TODO: There are various scenarios where we will overwrite prior information
# - <JWM Notes> We do not distinguish between differences in Line Numbers, an issue with same appname, filename, ruleset, violation but different line number will overwrite prior
#   I am not addressing now as I think we ultimately want to group all violations of same type together and we dont want to attemt to fix separate line numbers in independent calls


# TODO: Capture at get_solutions_for_file level as well.
#   We are only capturing at the lower level of get_incident_solution
@dataclass
class Capture:
    """Gathers information from the server for a request, prompt, and LLM Response
    This is intended to help with:
     - capturing data to evaluate different LLM responses
     - debug specific requests/responses
    """

    request: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    solved_incident: defaultdict[dict] = field(
        default_factory=lambda: defaultdict(dict)
    )
    prompt: str = ""
    llm_result: str = ""
    model_id: str = "unknown"
    logs_dir: str = ""

    def __init__(self):
        super()
        self.logs_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../logs"
        )

    def commit(self):
        """
        Saves the captured information to disk
        Organized by:
        {model}/{application_name}/{src_file_name}/
            request.md
            prompt.md
            solved_examples.md
            llm_result.md
        """
        """Saves the capture to disk"""
        application_name = self.request["application_name"]
        src_file_name = self.request["file_name"]
        ruleset_name = self.request["ruleset_name"]
        violation_name = self.request["violation_name"]

        # We want to group the output by the source file name, but flatten the dir structure
        src_file_name = src_file_name.replace("/", "_")

        out_dir = os.path.join(
            self.logs_dir,
            f"{self.model_id}/{application_name}/{src_file_name}/{ruleset_name}/{violation_name}",
        )
        os.makedirs(out_dir, exist_ok=True)

        with open(os.path.join(out_dir, src_file_name), "w") as f:
            f.write(self.request["file_contents"])
        with open(os.path.join(out_dir, "request.json"), "w") as f:
            json.dump(self.request, f, indent=2)
        with open(os.path.join(out_dir, "solved_incident.json"), "w") as f:
            json.dump(self.solved_incident, f, indent=2)
        with open(os.path.join(out_dir, "prompt"), "w") as f:
            pprint.pprint(self.prompt, f, indent=2)
        with open(os.path.join(out_dir, "llm_result"), "w") as f:
            f.write(self.llm_result.pretty_repr())

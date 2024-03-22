import json
import os
import pprint
from collections import defaultdict
from dataclasses import dataclass, field


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
        # We want to group the output by the source file name, but flatten the dir structure
        src_file_name = src_file_name.replace("/", "_")

        out_dir = os.path.join(
            self.logs_dir, f"{self.model_id}/{application_name}/{src_file_name}"
        )
        os.makedirs(out_dir, exist_ok=True)

        with open(os.path.join(out_dir, "request.json"), "w") as f:
            json.dump(self.request, f, indent=2)
        with open(os.path.join(out_dir, "solved_incident.json"), "w") as f:
            json.dump(self.solved_incident, f, indent=2)
        with open(os.path.join(out_dir, "prompt"), "w") as f:
            pprint.pprint(self.prompt, f, indent=2)
        with open(os.path.join(out_dir, "llm_result"), "w") as f:
            f.write(self.llm_result.pretty_repr())

        print(f"Saved capture to {out_dir}")

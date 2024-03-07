import os
import string
from dataclasses import dataclass
from enum import Enum
from os import path

# TODO: Unify the model selection criteria across PromptBuilder, IncidentStore
# embeddings and the actual llm call itself


"""
TODO Right now, `PromptBuilder` is very basic. I want to extend this. Here's my
thoughts with some unsolved problems.

General idea is that we want maximum configurability so that when we switch out
models, we can use the most optimal prompt. I'm envisioning we have multiple
different "sections" in different text files that we can use to build the
prompt.

Each type of model could have 3 different types of variables (e.g.
`{variable_whatever}` in a prompt_section.txt): 

- required: These are the variables that must be present in order for the prompt
  to be built
- optional: These variables will add/modify the sections used, but may not be
  necessary
- override: If certain variables are set, then use one section. Otherwise use
  another prompt. (Think DAG) A variable can override multiple other variables.

This whole variable-section DAG could be unique for each model type. Only major
issue is how to define custom PromptBuilders without them getting too unwieldy.

There's also the issue of "variants". A prompt might need tweaking to get a good
result, so we should also support variants somehow.

A section has variables. A section is "valid" if all the variables for it are
set.

dfs order determines priority

topological sort to get the "seen" thing

TODO: Ugliness could be solved by getting rid of the "optional" stuff. Instead,
a section, when it overrides another section, can not only replace it, but also
add to it. For example, if A overrides C and B overrides C, currently we only
take A as it comes first. There's another path where A and B are put in C's
place. Then we can have a "dummy" root and an elegant graph of just sections. 

A few problems I see with with this:

- How do we do mandatory sections? 
- What if we have initial order [A, B, C] and D overrides A and C? We can't just
  replace A and C with D...

- jsussman
"""


class PromptBuilderVariables(Enum):
    ANALYSIS_MESSAGE = "analysis_message"


# TODO: Variants
class Section:
    """
    Simple data class containing the template and the variables for a section
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.template = open(file_path).read()

        itr = string.Formatter().parse(self.template)
        self.vars = [v[1] for v in itr if v[1] is not None]

    def __hash__(self):
        return hash((self.file_path, self.template))

    def is_valid(self, vars_dict: dict[str, str]):
        for v in self.vars:
            if v not in vars_dict:
                return False

        return True

    def format(self, vars_dict: dict[str, str]):
        return self.template.format(**vars_dict)


# TODO: How to do optional sections that don't have variables?
@dataclass
class SectionGraph:
    """
    Using Section as a "value" node, contains the adjacency list as well as
    whether this section is optional or not
    """

    root: Section
    optional: bool
    adj: dict[Section, list[Section]]

    def topological(self) -> list[Section]:
        visited = set()
        result = []

        def dfs(node: Section):
            if node in visited:
                return
            visited.add(node)
            for child in self.adj.get(node, []):
                dfs(child)
            result.append(node)

        dfs(self.root)

        result.reverse()
        return result

    # NOTE: Maybe have an option for bfs instead? Where would we put the option
    # for that?
    def get_valid_section(self, vars_dict: dict[str, str]) -> Section | None:
        visited = set()

        def dfs(node: Section):
            if node in visited:
                return
            visited.add(node)
            for child in self.adj.get(node, []):
                x = dfs(child)
                if x is not None:
                    return x

            return node if node.is_valid(vars_dict) else None

        return dfs(self.root)


# NOTE: Class may be unnecessary
class Config:
    def __init__(self, sections: list[SectionGraph]):
        self.sections = sections


T_DIR = path.join(path.dirname(__file__), "data/templates")
S_PREAMBLE = Section(path.join(T_DIR, "preamble.txt"))
S_SOLVED_EXAMPLE_DIFF = Section(path.join(T_DIR, "solved_example_diff.txt"))
S_SOLVED_EXAMPLE_FILE = Section(path.join(T_DIR, "solved_example_file.txt"))
S_SOLVED_EXAMPLE_NONE = Section(path.join(T_DIR, "solved_example_none.txt"))
S_INPUT_FILE = Section(path.join(T_DIR, "input_file.txt"))
S_OUTPUT_INSTRUCTIONS = Section(path.join(T_DIR, "output_instructions.txt"))


# NOTE: May need to do something like foo: AtLeastOneOf([bar, baz]) or something
CONFIG_IBM = Config(
    [
        SectionGraph(S_PREAMBLE, False, {}),
        SectionGraph(
            S_SOLVED_EXAMPLE_NONE,
            False,
            {
                S_SOLVED_EXAMPLE_NONE: [S_SOLVED_EXAMPLE_DIFF, S_SOLVED_EXAMPLE_FILE],
            },
        ),
        SectionGraph(S_INPUT_FILE, False, {}),
        SectionGraph(S_OUTPUT_INSTRUCTIONS, False, {}),
    ]
)


# CONFIG_OPENAI = Config ...


# TODO: Make custom configs easier to define
class PromptBuilder:
    def __init__(self, config: Config, vars: dict[str, str] = {}):
        self.config = config
        self.vars = vars

        self.root_required_vars = set()

        for g in self.config.sections:
            if g.optional:
                continue
            self.root_required_vars.update(g.root.vars)

    def build_prompt(self):
        """
        Returns either the built prompt or the list of missing vars in order to
        build it. Note that a prompt may not need these vars. Rather, these are the
        vars that would guarantee that the prompt be built. In other words, some
        other combination of vars may work too (see SectionGraph) but these ones are
        sufficient.
        """
        result = ""
        missing_vars = set()

        for section_graph in self.config.sections:
            section = section_graph.get_valid_section(self.vars)
            if section is None:
                missing_vars.update(section_graph.root.vars)
                # raise Exception(f"Must set at least variables {section_graph.root.vars}.")
            elif not missing_vars:
                result += section.format(self.vars)

        return result if not missing_vars else list(missing_vars - self.vars.keys())


if __name__ == "__main__":
    pb = PromptBuilder(CONFIG_IBM)

    print(pb.build_prompt())
    input()

    pb.vars = {
        "src_file_name": "/var/src_file_name.java",
        "src_file_contents": "import nothing;",
        "analysis_line_number": 10,
        "analysis_message": "ya done goofed!",
    }

    print(pb.build_prompt())
    input()

    pb.vars = {
        "src_file_name": "/var/src_file_name.java",
        "solved_example_diff": "Here's a diff for ya!",
        "solved_example_file_name": "the/solved/example.java",
        "src_file_contents": "import nothing;",
        "analysis_line_number": 10,
        "analysis_message": "ya done goofed!",
    }

    print(pb.build_prompt())
    input()

    pb.vars = {
        "src_file_name": "/var/src_file_name.java",
        "solved_example_before": "File before!",
        "solved_example_after": "File after!",
        "solved_example_file_name": "the/solved/example.java",
        "src_file_contents": "import nothing;",
        "analysis_line_number": 10,
        "analysis_message": "ya done goofed!",
    }

    print(pb.build_prompt())

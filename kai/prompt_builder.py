import os
import string
from dataclasses import dataclass, field
from enum import Enum
from os import path

import yaml

# TODO: Unify the model selection criteria across PromptBuilder, IncidentStore
# embeddings and the actual llm call itself


"""
TODO Honestly, upon further evaluation this is bad and I feel bad about making
it :( - jsussman

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


class PBError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


@dataclass
class Symbol:
    value: str

    def __hash__(self):
        return hash(self.value)


@dataclass
class Env:
    inner: dict = field(default_factory=dict)
    outer: "Env" = None

    def find(self, x: str):
        if x in self.inner:
            return self.inner

        if self.outer is not None:
            return self.outer.find(x)

        return None


def pb_concat(args: list, pb_env: Env, pb_vars: dict) -> str:
    result = ""

    for arg in args:
        arg = pb_eval(arg, pb_env, pb_vars)
        if not isinstance(arg, str):
            raise PBError(f"Can only concat strings. Got {type(arg)}.")
        result += arg

    return result


def pb_format(args: list, pb_env: Env, pb_vars: dict) -> str | None:
    print(f"pb_format: {args=}")
    if len(args) > 2:
        raise PBError(f"Max 2 arguments.")
    if len(args) == 0:
        return ""

    section = pb_eval(args[0], pb_env, pb_vars)
    if not isinstance(section, Section):
        raise PBError("Not a section!")

    if len(args) == 1:
        return section.format_with_raise(pb_vars)

    pb_vars = pb_vars[pb_eval(args[1], pb_env, pb_vars)]
    if isinstance(pb_vars, dict):
        return section.format_with_raise(pb_vars)
    if not isinstance(pb_vars, list):
        raise PBError("Uh-oh, not a list!")

    result = ""
    for vars in pb_vars:
        s = section.format_with_raise(vars)
        # if s is None:
        #     return None
        result += s

    return result


def pb_one_of(args: list, pb_env: Env, pb_vars: dict) -> str:
    for arg in args:
        try:
            arg = pb_eval(arg, pb_env, pb_vars)
            if not (isinstance(arg, str) or arg is None):
                raise PBError(f"Can only one_of strings or None. Got {type(arg)}.")
            if arg is not None:
                return arg
        except Exception:
            continue

    raise PBError(f"one_of: All of the arguments were invalid.")


def pb_eval(x, pb_env: Env, pb_vars: dict):
    print(f"pb_eval: {x}")
    if isinstance(x, Symbol) or (isinstance(x, str) and len(x) > 0 and x[0] == "$"):
        f = pb_env.find(x)
        if f is not None:
            return f[x]
        else:
            return None

    if not isinstance(x, dict):
        return x

    if len(list(x.keys())) != 1:
        raise PBError("Only one action at a time!")

    fn_name = list(x.keys())[0]
    if not isinstance(fn_name, str):
        raise PBError("Action key must be string!")

    fn_args = x[fn_name]
    if not isinstance(fn_args, list):
        fn_args = [fn_args]

    if fn_name == "quote" or fn_name == "q":
        return fn_args[0]

    func = pb_eval(Symbol(fn_name), pb_env, pb_vars)
    return func(fn_args, pb_env, pb_vars)


def standard_env():
    return Env(
        inner={
            Symbol("concat"): pb_concat,
            Symbol("format"): pb_format,
            Symbol("one_of"): pb_one_of,
        }
    )


global_env = standard_env()


# TODO: Variants
class Section:
    """
    Simple data class containing the template and the variables for a section
    """

    # TODO: Fix this
    @staticmethod
    def from_dict(x: dict):
        return Section(
            uuid=x.get("uuid", None),
            file_path=x.get("file_path", None),
            template=x.get("template", None),
            default_vars=x.get("default_vars", None),
            build_steps=x.get("build_steps", None),
        )

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "file_path": self.file_path,
            "template": self.template,
            "default_vars": self.default_vars,
            "build_steps": self.build_steps,
        }

    def __init__(
        self,
        *,
        uuid: str = None,
        file_path: str = None,
        template: str = None,
        default_vars: dict[str, str] = None,
        build_steps: list = None,
    ):
        print(type(template))
        print(template)

        if uuid is None:
            raise Exception("uuid can't be none")
        self.uuid = uuid

        if file_path is not None and template is not None:
            raise Exception("Can't provide both file_path and template")
        elif file_path is not None:
            self.file_path = file_path
            self.template = open(file_path).read()
        elif template is not None:
            self.file_path = "/dev/null"
            self.template = template
        else:
            self.file_path = "/dev/null"
            self.template = ""

        if build_steps is None:
            build_steps = []

        self.build_steps = build_steps

        itr = string.Formatter().parse(self.template)
        self.vars = [v[1] for v in itr if v[1] is not None]
        self.default_vars = {} if default_vars is None else default_vars

    def __hash__(self):
        return hash((self.file_path, self.template))

    def is_valid(self, vars_dict: dict[str, str]):
        vars_dict = self.default_vars | vars_dict

        for v in self.vars:
            if v not in vars_dict:
                return False

        return True

    def format(self, vars_dict: dict[str, str]):
        vars_dict = self.default_vars | vars_dict

        return self.template.format(**vars_dict)

    def format_with_raise(self, vars_dict: dict[str, str]):
        if self.is_valid(vars_dict):
            return self.format(vars_dict)

        raise PBError(
            f"Missing variables: {set(self.vars).difference(set(vars_dict))} for section '{self.uuid}'"
        )


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

# # NOTE: May need to do something like foo: AtLeastOneOf([bar, baz]) or something
# CONFIG_IBM_GRANITE = Config(
#     [
#         SectionGraph(S_PREAMBLE, False, {}),
#         SectionGraph(
#             S_SOLVED_EXAMPLE_NONE,
#             False,
#             {
#                 S_SOLVED_EXAMPLE_NONE: [S_SOLVED_EXAMPLE_DIFF, S_SOLVED_EXAMPLE_FILE],
#             },
#         ),
#         SectionGraph(S_INPUT_FILE, False, {}),
#         SectionGraph(S_OUTPUT_INSTRUCTIONS, False, {}),
#     ]
# )


# CONFIG_IBM_LLAMA = Config(
#     [
#         SectionGraph(S_LLAMA_BEGIN, False, {}),
#         SectionGraph(S_PREAMBLE, False, {}),
#         SectionGraph(
#             S_SOLVED_EXAMPLE_NONE,
#             False,
#             {
#                 S_SOLVED_EXAMPLE_NONE: [S_SOLVED_EXAMPLE_DIFF, S_SOLVED_EXAMPLE_FILE],
#             },
#         ),
#         SectionGraph(S_INPUT_FILE, False, {}),
#         SectionGraph(S_OUTPUT_INSTRUCTIONS, False, {}),
#         SectionGraph(S_LLAMA_END, False, {}),
#     ]
# )


# TODO: Make custom configs easier to define
class PromptBuilder:
    def __init__(self, config: Config, vars: dict[str, str] = None):
        self.config = config
        self.vars = vars if vars is not None else {}

        self.root_required_vars = set()

        for g in self.config.sections:
            if g.optional:
                continue
            self.root_required_vars.update(g.root.vars)

    def build_prompt(self):
        """
        Returns either the built prompt or the list of missing vars in order to
        build it. Note that a prompt may not need these vars. Rather, these are
        the vars that would guarantee that the prompt be built. In other words,
        some other combination of vars may work too (see SectionGraph) but these
        ones are sufficient.
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


# def build_prompt_incident_solver(
#     *,
#     model: str = "granite",
#     grouping: GroupingStrategy = GroupingStrategy.GROUP_NONE,
#     src_file_name: str = None,
#     src_file_language: str = None,
#     src_file_contents: str = None,
#     incidents: list[dict] = None,
# ):
#     """
#     TODO: Make pydantic models so it's cleaner

#     Assuming an incident is a dict with the following
#     - ruleset_name (str)
#     - violation_name (str)
#     - incident_snip (str optional)
#     - incident_variables (object)
#     - line_number: 0-indexed (let's keep it consistent)
#     - analysis_message (str)
#     - solved_example (str)
#     """

#     if src_file_name is None:
#         raise ValueError("Must provide a source file name to prompt builder")

#     if src_file_language is None:
#         _, ext = os.path.splitext(src_file_name)
#         src_file_language = ext[1:] if len(ext) > 0 else ""

#     if src_file_contents is None:
#         raise ValueError("Must provide source file contents to prompt builder")

#     if incidents is None:
#         incidents = []

#     preamble = """# Java EE to Quarkus Migration

# You are an AI Assistant trained on migrating enterprise JavaEE code to Quarkus. I will give you an example of a JavaEE file and you will give me the Quarkus equivalent.

# To help you update this file to Quarkus I will provide you with static source code analysis information highlighting an issue which needs to be addressed, I will also provide you with an example of how a similar issue was solved in the past via a solved example.  You can refer to the solved example for a pattern of how to update the input Java EE file to Quarkus.

# Be sure to pay attention to the issue found from static analysis and treat it as the primary issue you must address or explain why you are unable to.

# Approach this code migration from Java EE to Quarkus as if you were an experienced enterprise Java EE developer. Before attempting to migrate the code to Quarkus, explain each step of your reasoning through what changes are required and why.

# Pay attention to changes you make and impacts to external dependencies in the pom.xml as well as changes to imports we need to consider.

# As you make changes that impact the pom.xml or imports, be sure you explain what needs to be updated.

# After you have shared your step by step thinking, provide a full output of the updated file.

# """

#     input_information = """# Input Information

# """

#     input_file = """## Input File

# File name: "{src_file_name}"
# Source file contents:
# ```{src_file_language}
# {src_file_contents}'
# ```

# """.format(
#         src_file_name=src_file_name,
#         src_file_language=src_file_language,
#         src_file_contents=src_file_contents,
#     )

#     issues = "## Issues \n\n"

#     if grouping == GroupingStrategy.GROUP_NONE:
#         for i in range(len(incidents)):
#             issues += """### Issue {i}
# Issue to fix: "{analysis_message}"
# Line number: {analysis_line_number}
# """.format(
#                 i=i,
#                 analysis_message=incidents[i]["analysis_message"],
#                 analysis_line_number=incidents[i]["analysis_line_number"],
#             )

#             if "solved_example" in incidents[i]:
#                 issues += """Solved example:
# ```diff
# {solved_example_diff}
# ```
# """.format(
#                     solved_example_diff=incidents[i]["solved_example_diff"]
#                 )
#             issues += "\n"
#     # elif grouping == GroupingStrategy.GROUP_ON_VIOLATION:
#     #     raise Exception()
#     else:
#         raise ValueError(f"Invalid grouping strategy {grouping}")

#     # res = {i: [j[0] for j in j] for i, j in itertools.groupby(sorted(test_dict.items(), key = lambda x : x[1]), lambda x : x[1])}

#     # for i, j in itertools.groupby(sorted(test_dict.items(), key = lambda x : x[1]), lambda x : x[1]):

#     output_instructions = """# Output instructions

# Structure your output in the following Markdown format:

# ## Reasoning

# Write the step by step reasoning in this markdown section. If you are unsure of a step or reasoning, clearly state you are unsure and why.

# ## Updated File

# ```{src_file_language}
# // Write the updated file for Quarkus in this section
# ```

# """.format(
#         src_file_language=src_file_language
#     )

#     return preamble + input_information + input_file + issues + output_instructions


if __name__ == "__main__":
    """
    # pb = PromptBuilder(CONFIG_IBM_GRANITE)

    # print(pb.build_prompt())
    # input()

    # pb.vars = {
    #     "src_file_name": "/var/src_file_name.java",
    #     "src_file_contents": "import nothing;",
    #     "analysis_line_number": 10,
    #     "analysis_message": "ya done goofed!",
    # }

    # print(pb.build_prompt())
    # input()

    # pb.vars = {
    #     "src_file_name": "/var/src_file_name.java",
    #     "solved_example_diff": "Here's a diff for ya!",
    #     "solved_example_file_name": "the/solved/example.java",
    #     "src_file_contents": "import nothing;",
    #     "analysis_line_number": 10,
    #     "analysis_message": "ya done goofed!",
    # }

    # print(pb.build_prompt())
    # input()

    # pb.vars = {
    #     "src_file_name": "/var/src_file_name.java",
    #     "solved_example_before": "File before!",
    #     "solved_example_after": "File after!",
    #     "solved_example_file_name": "the/solved/example.java",
    #     "src_file_contents": "import nothing;",
    #     "analysis_line_number": 10,
    #     "analysis_message": "ya done goofed!",
    # }

    # print(pb.build_prompt())

    """

    # Example usage
    yaml_str = """
uuid: $ibm_config
file_path: null
default_vars: null
build_steps:
    - one_of:
        - format: $test_0
        - format: $test_1
    - format: [ $test_0, test_0 ]
    # - format: [ "123" ]
    # - one_of:
    #     - format: [ xyz, asdfgh ]
    #     - format: [ abc, qwerty ]
    #     - format: [ ]
---
uuid: $test_0
template: "{replace_me}"
---
uuid: $test_1
template: "Hello!"
"""

    documents = yaml.safe_load_all(yaml_str)

    for doc in documents:
        s = Section.from_dict(doc)
        if global_env.find(s.uuid) is not None:
            print("already exists")
        else:
            global_env.inner[s.uuid] = s

    s = global_env.find("$ibm_config")["$ibm_config"]
    print(yaml.dump(s.to_dict()))
    print(
        pb_concat(
            s.build_steps,
            global_env,
            {
                "test_0": [
                    {"replace_me": "first"},
                    {"replace_me": "second"},
                    {"replace_me": "third"},
                ]
            },
        )
    )

    exit()

    x = build_prompt_incident_solver(
        src_file_name="/var/whatever.java",
        src_file_contents="""import whatever;
        
class Java {

}
""",
        incidents=[
            {
                "analysis_line_number": 10,
                "analysis_message": "ya done goofed!",
            },
            {
                "analysis_line_number": 10,
                "analysis_message": "ya done goofed!",
            },
        ],
    )

    print(x, end="")

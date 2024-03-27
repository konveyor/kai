import os
import string
from dataclasses import dataclass, field
from os import path

import yaml

T_DIR = path.join(path.dirname(__file__), "data/templates")


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
        if uuid is None:
            raise Exception("uuid can't be none")
        self.uuid = uuid

        if file_path is not None and template is not None:
            raise Exception("Can't provide both file_path and template")
        elif file_path is not None:
            self.file_path = path.join(T_DIR, file_path)
            self.template = open(self.file_path).read()
        elif template is not None:
            self.file_path = "/dev/null"
            self.template = template
        else:
            self.file_path = "/dev/null"
            self.template = ""

        if build_steps is None:
            build_steps = [{"format": self.uuid}]

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
    # print(f"pb_format: {args=}")
    if len(args) > 2:
        raise PBError("Max 2 arguments.")
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
        result += s

    return result


def pb_build(args: list, pb_env: Env, pb_vars: dict):
    # print(f"pb_format: {args=}")
    if len(args) > 2:
        raise PBError("Max 2 arguments.")
    if len(args) == 0:
        return ""

    section = pb_eval(args[0], pb_env, pb_vars)
    if not isinstance(section, Section):
        raise PBError("Not a section!")

    if len(args) == 1:
        for s in section.build_steps:
            result = pb_eval(s, pb_env, pb_vars)
        return result

    pb_vars = pb_vars[pb_eval(args[1], pb_env, pb_vars)]
    if isinstance(pb_vars, dict):
        for s in section.build_steps:
            r = pb_eval(s, pb_env, pb_vars)
        return r
    if not isinstance(pb_vars, list):
        raise PBError("Uh-oh, not a list!")

    result = ""
    for vars in pb_vars:
        for s in section.build_steps:
            r = pb_eval(s, pb_env, vars)
        result += r

    return result


def pb_one_of(args: list, pb_env: Env, pb_vars: dict) -> str:
    errors = []
    for arg in args:
        try:
            arg = pb_eval(arg, pb_env, pb_vars)
            if not (isinstance(arg, str) or arg is None):
                raise PBError(f"Can only one_of strings or None. Got {type(arg)}.")
            if arg is not None:
                return arg
        except Exception as e:
            errors.append(e)

    msg = "one_of: All of the arguments were invalid. Got the following errors:\n"
    for e in errors:
        msg += f"- {str(e)}\n"

    raise PBError(msg)


def pb_eval(x, pb_env: Env, pb_vars: dict):
    # print(f"pb_eval: {x}")
    if isinstance(x, Symbol) or (isinstance(x, str) and len(x) > 0 and x[0] == "$"):
        f = pb_env.find(x)
        if f is not None:
            return f[x]

        raise PBError(f"pb_eval: Couldn't find symbol {x}.")

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
    env = Env(
        inner={
            Symbol("concat"): pb_concat,
            Symbol("format"): pb_format,
            Symbol("build"): pb_build,
            Symbol("one_of"): pb_one_of,
        }
    )

    for dirpath, _dirnames, filenames in os.walk(T_DIR):
        for filename in filenames:
            if filename.endswith(".yaml"):
                file_path = os.path.join(dirpath, filename)
                x = open(file_path).read()

                documents = yaml.safe_load_all(x)

                for doc in documents:
                    section = Section.from_dict(doc)
                    if env.find(section.uuid) is not None:
                        raise Exception(f"{section.uuid} already exists!")
                    else:
                        env.inner[section.uuid] = section

    return env


global_env = standard_env()


CONFIG_IBM_GRANITE_MF = "$mf_ibm_model"
CONFIG_IBM_GRANITE = "$ibm_granite_model"
CONFIG_IBM_LLAMA = "$ibm_llama_model"


def build_prompt(section_name: str, pb_vars: dict):
    section = global_env.find(section_name)[section_name]
    if not isinstance(section, Section):
        raise PBError(f"Not a section. Got type: {type(section)}")

    for step in section.build_steps:
        result = pb_eval(step, global_env, pb_vars)

    if not isinstance(result, str):
        raise PBError(f"Prompt building did not return str. Got type: {type(result)}")
    return result


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

    # FIXME: Make pb_vars an environment, not a dict (cascading stuff)

    build_prompt(
        CONFIG_IBM_GRANITE_MF,
        {
            "src_file_name": "/var/src_file_name.java",
            "src_file_language": "java",
            "src_file_contents": "import nothing;",
            "solved_example_file_name": "the/solved/example.java",
            "incidents": [
                {
                    "issue_number": 1,
                    "analysis_line_number": 10,
                    "analysis_message": "ya done goofed!",
                    "solved_example_before": "File before!",
                    "solved_example_after": "File after!",
                    "src_file_language": "java",
                }
            ],
        },
    )

    print(
        build_prompt(
            CONFIG_IBM_LLAMA,
            {
                "analysis_message": "test message",
                "src_file_name": "/var/src_file_name.java",
                "src_file_language": "java",
                "src_file_contents": "import nothing;",
                "analysis_line_number": 10,
            },
        )
    )

    exit()

#     x = build_prompt(
#         src_file_name="/var/whatever.java",
#         src_file_contents="""import whatever;

# class Java {

# }
# """,
#         incidents=[
#             {
#                 "analysis_line_number": 10,
#                 "analysis_message": "ya done goofed!",
#             },
#             {
#                 "analysis_line_number": 10,
#                 "analysis_message": "ya done goofed!",
#             },
#         ],
#     )

#     print(x, end="")

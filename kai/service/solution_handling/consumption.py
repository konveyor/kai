import os
from functools import singledispatch
from typing import Callable

import jinja2

from kai.constants import PATH_TEMPLATES
from kai.models.kai_config import SolutionConsumerKind
from kai.service.solution_handling.types import Solution

# TODO: Potentially add fallback functionality. For example, before_and_after
# might be too large, so we should fall back to diff_only.

# TODO: This might be a lot of boilerplate for just calling `render`

SolutionConsumerAlgorithm = Callable[[Solution], str]


def __create_jinja_env() -> jinja2.Environment:
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(PATH_TEMPLATES, "solution_handling")
        ),
        undefined=jinja2.StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )


def solution_consumer_diff_only(solution: Solution) -> str:
    return (
        __create_jinja_env().get_template("diff_only.jinja2").render(solution=solution)
    )


def solution_consumer_before_and_after(solution: Solution) -> str:
    return (
        __create_jinja_env()
        .get_template("before_and_after.jinja2")
        .render(solution=solution)
    )


def solution_consumer_llm_summary(solution: Solution) -> str:
    return (
        __create_jinja_env()
        .get_template("llm_summary.jinja2")
        .render(solution=solution)
    )


@singledispatch
def solution_consumer_factory(kind) -> SolutionConsumerAlgorithm:
    raise ValueError(f"Unknown solution consumer kind: {kind}")


@solution_consumer_factory.register
def _(kind: SolutionConsumerKind) -> SolutionConsumerAlgorithm:
    match kind:
        case "diff_only":
            return solution_consumer_diff_only
        case "before_and_after":
            return solution_consumer_before_and_after
        case "llm_summary":
            return solution_consumer_llm_summary
        case _:
            raise ValueError(f"Unknown solution consumer kind: {kind}")


@solution_consumer_factory.register
def _(kinds: list[SolutionConsumerKind]) -> SolutionConsumerAlgorithm:
    algorithms = [solution_consumer_factory(kind) for kind in kinds]
    return lambda solution: "\n".join(algo(solution) for algo in algorithms)

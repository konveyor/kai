# TODO: Come up with some sort of "solution generator strategy" so we
# don't blow up our llm API usage. Lazy, immediate, other etc...

import enum
from typing import Callable, Optional

from kai.service.incident_store.incident_store import Solution, SQLIncident


class SolutionProductionKind(enum.Enum):
    DIFF = "diff"
    LLM_EAGER = "llm_eager"
    LLM_LAZY = "llm_lazy"


SolutionProductionAlgorithm = Callable[
    [list[SQLIncident], list[Optional[Solution]]], list[Solution]
]


def solution_production_diff(
    incidents: list[SQLIncident], solutions: list[Optional[Solution]]
) -> list[Solution]:
    pass


# TODO: Figure out how to best pass the model_provider


def solution_production_llm_eager(
    incidents: list[SQLIncident], solutions: list[Optional[Solution]]
) -> list[Solution]:
    pass


def solution_production_llm_lazy(
    incidents: list[SQLIncident], solutions: list[Optional[Solution]]
) -> list[Solution]:
    pass

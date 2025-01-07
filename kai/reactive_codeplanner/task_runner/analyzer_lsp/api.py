import itertools
from dataclasses import dataclass
from typing import Any
from functools import cached_property

from kai.analyzer_types import Incident, RuleSet, Violation
from kai.logging.logging import get_logger
from kai.reactive_codeplanner.task_manager.api import Task, ValidationError

logger = get_logger(__name__)


@dataclass(eq=False, kw_only=True)
class AnalyzerRuleViolation(ValidationError):
    incident: Incident

    # NOTE(JonahSussman): Violation contains a list of Incidents, and RuleSet
    # contains a list of Violations. We have another class, ExtendedIncident,
    # that is a flattened version of this, but it might not contain everything
    # we want yet. Maybe there's a better way to create ExtendedIncident. I
    # don't think these fields are used anywhere regardless.
    violation: Violation
    ruleset: RuleSet
    # TODO Highest priority?
    priority: int = 2

    def __str__(self) -> str:
        if self.parent:
            shadowed_priority = self.oldest_ancestor().priority
        else:
            shadowed_priority = self.__class__.priority

        return f"{self.__class__.__name__}<loc={self.file}:{self.line}:{self.column}, violation.id={self.violation.id}>(priority={self.priority}({shadowed_priority}), depth={self.depth}, retries={self.retry_count})"

    @cached_property
    def sources(self) -> list[str]:
        labels = set(
            itertools.chain(*[v.labels for v in self.ruleset.violations.values()])
        )
        source_key = "konveyor.io/source="
        return [
            label.replace(source_key, "") for label in labels if source_key in label
        ]

    @cached_property
    def targets(self) -> list[str]:
        labels = set(
            itertools.chain(*[v.labels for v in self.ruleset.violations.values()])
        )
        target_key = "konveyor.io/target="
        return [
            label.replace(target_key, "") for label in labels if target_key in label
        ]

    __repr__ = __str__

    def fuzzy_equals(self, error2: Task, offset: int = 1) -> bool:
        if not isinstance(error2, AnalyzerRuleViolation):
            return False

        if (
            self.ruleset.name == error2.ruleset.name
            and self.violation.id == error2.violation.id
            and self.incident.message == error2.incident.message
            and self.file == error2.file
        ):
            logger.debug("found match line numbers may be off %s -- %s", self, error2)
            return True

        return False

    def sort_key(self) -> tuple[Any, ...]:
        base_key = super().sort_key()
        ruleset_name = self.ruleset.name if self.ruleset and self.ruleset.name else ""
        viol_id = self.violation.id if self.violation else 0
        inc_msg = (
            self.incident.message if self.incident and self.incident.message else ""
        )
        return base_key + (ruleset_name, viol_id, inc_msg)


class AnalyzerDependencyRuleViolation(AnalyzerRuleViolation):
    """The same as a AnalyzerRuleValidation but higher priority and used by the dependency task_runner"""

    priority: int = 1

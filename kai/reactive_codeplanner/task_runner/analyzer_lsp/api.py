from dataclasses import dataclass

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

        return f"{self.__class__.__name__}<loc={self.file}:{self.line}:{self.column}, message={self.violation.description}>(priority={self.priority}({shadowed_priority}), depth={self.depth}, retries={self.retry_count})"

    __repr__ = __str__

    def fuzzy_equals(self, error2: Task, offset: int = 1) -> bool:
        if not isinstance(error2, AnalyzerRuleViolation):
            return False

        if (
            self.ruleset.name == error2.ruleset.name
            and self.incident.message == error2.incident.message
            and self.file == error2.file
            and self.incident.variables == error2.incident.variables
        ):
            logger.info("should match on line numbers %s -- %s", self.line, error2.line)
            return True

        return False


class AnalyzerDependencyRuleViolation(AnalyzerRuleViolation):
    """The same as a AnalyzerRuleValidation but higher priority and used by the dependency task_runner"""

    priority: int = 1

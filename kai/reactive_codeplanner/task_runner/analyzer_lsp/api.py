from dataclasses import dataclass
from functools import cached_property
from typing import Any

from kai.analyzer_types import Incident, RuleSet, Violation
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.task_manager.api import Task, ValidationError

logger = get_logger(__name__)


@dataclass(eq=False, kw_only=True)
class AnalyzerRuleViolation(ValidationError):
    incidents: list[Incident]

    # NOTE(JonahSussman): Violation contains a list of Incidents, and RuleSet
    # contains a list of Violations. We have another class, ExtendedIncident,
    # that is a flattened version of this, but it might not contain everything
    # we want yet. Maybe there's a better way to create ExtendedIncident. I
    # don't think these fields are used anywhere regardless.
    violation: Violation
    ruleset: RuleSet
    # TODO Highest priority?
    priority: int = 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if not (
            self.ruleset.name == other.ruleset.name
            and self.violation.id == other.violation.id
            and self.file == other.file
            and self.incident_message == other.incident_message
        ):
            logger.log(
                TRACE,
                "ruleset_name: %s, violation_id: %s, file: %s, for self did not match ruleset_name: %s, violation_id: %s, file: %s",
                self.ruleset.name,
                self.violation.id,
                self.file,
                other.ruleset.name,
                other.violation.id,
                other.file,
            )
            return False

        return True

    def __hash__(self) -> int:
        return hash(
            (
                self.ruleset.name,
                self.violation.id,
                self.file,
                tuple(self.incident_message),
            )
        )

    def __str__(self) -> str:
        if self.parent:
            shadowed_priority = self.oldest_ancestor().priority
        else:
            shadowed_priority = self.__class__.priority

        return f"{self.__class__.__name__}<loc={self.file}:{self.line}:{self.column}, violation.id={self.violation.id}>(priority={self.priority}({shadowed_priority}), depth={self.depth}, retries={self.retry_count})"

    @cached_property
    def sources(self) -> list[str]:
        source_key = "konveyor.io/source="
        source = [
            label.replace(source_key, "")
            for label in self.violation.labels
            if source_key in label
        ]
        source.sort()
        return source

    @cached_property
    def targets(self) -> list[str]:
        target_key = "konveyor.io/target="
        target = [
            label.replace(target_key, "")
            for label in self.violation.labels
            if target_key in label
        ]
        target.sort()
        return target

    def background(self) -> str:
        if self.parent is not None:
            return self.oldest_ancestor().background()
        if self.children:
            message = f"""You attempted to solve the following issues in the source code you are migrating:
Issues: {"\n".join(self.incident_message)}"""

            if self.result and self.result.summary:
                message += f"\n\nHere is the reasoning you provided for your initial solution:\n\n{self.result.summary}"
            message += "\n\nHowever your solution caused additional problems elsewhere in the repository."
            return message

        return ""

    @cached_property
    def incident_message(self) -> list[str]:
        incident_msg_list = [i.message for i in self.incidents]
        incident_msg_list.sort()
        return incident_msg_list

    __repr__ = __str__

    def fuzzy_equals(self, error2: Task, offset: int = 1) -> bool:
        if not isinstance(error2, AnalyzerRuleViolation):
            logger.log(
                TRACE,
                "error2 %s is not of correct type for %s",
                type(error2),
                type(self),
            )
            return False

        if not (
            self.ruleset.name == error2.ruleset.name
            and self.violation.id == error2.violation.id
            and self.file == error2.file
        ):
            logger.log(
                TRACE,
                "ruleset_name: %s, violation_id: %s, file: %s, for self did not match ruleset_name: %s, violation_id: %s, file: %s",
                self.ruleset.name,
                self.violation.id,
                self.file,
                error2.ruleset.name,
                error2.violation.id,
                error2.file,
            )
            return False

        if len(self.incidents) == len(error2.incidents):
            if self.incidents == error2.incidents:
                logger.log(
                    TRACE, "incidents match for self: %s, error2: %s", self, error2
                )
                return True

        """When there are different numbers, we have three cases to consider
            1. error2 has more incidents, and maybe the change didn't fix things and
            introduced more issues. In this case, we want to retry the task, with the added
            incidents.
            2. error2 has less issues, but one thing was not fixed, I think today, we want to 
            remove the incidents that have been fixed.
            3. They don't have any matching incidents, and in this case, I think we want to consider
              the resulting ask a child.
            
            The update described here, has to happen in an other function that will pop this task and create a new one
            in the task manager because incident message's are used to calculate the hash and equality.
        """
        still_found_incidents: list[Incident] = []
        to_remove_incidents: list[Incident] = []
        for i in self.incidents:
            if i.message in error2.incident_message:
                still_found_incidents.append(i)
            else:
                to_remove_incidents.append(i)

        # Here we handle the third case, where they are new issues.
        if len(still_found_incidents) == 0:
            logger.log(TRACE, "no incidents from original found")
            return False

        # here we handle the first case, we will update self to add the context of new issues
        if (
            len(still_found_incidents) == len(self.incidents)
            and len(to_remove_incidents) == 0
        ):
            logger.log(
                TRACE,
                "found all old incidents and some new ones, making task retry, with all the new incidents",
            )
            logger.log(
                TRACE,
                "incident messages for self: %s --- incident messages for fuzzy equals: %s",
                self.incident_message,
                error2.incident_message,
            )
            return True

        # here we handle the second case
        if len(to_remove_incidents) != 0 and len(still_found_incidents) > 0:
            logger.log(
                TRACE,
                "removed incidents that were not found, retry with remaining incidents",
            )
            return True

        return False

    def sort_key(self) -> tuple[Any, ...]:
        base_key = super().sort_key()
        ruleset_name = self.ruleset.name if self.ruleset and self.ruleset.name else ""
        viol_id = self.violation.id if self.violation else 0
        inc_msg = self.incident_message
        return base_key + (ruleset_name, viol_id, inc_msg)


class AnalyzerDependencyRuleViolation(AnalyzerRuleViolation):
    """The same as a AnalyzerRuleValidation but higher priority and used by the dependency task_runner"""

    priority: int = 1

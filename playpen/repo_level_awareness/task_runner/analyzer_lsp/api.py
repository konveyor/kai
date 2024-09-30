from dataclasses import dataclass

from kai.models.report_types import Incident, RuleSet, Violation
from playpen.repo_level_awareness.api import ValidationError


@dataclass
class AnalyzerRuleViolation(ValidationError):
    incident: Incident
    violation: Violation
    ruleset: RuleSet

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type
from kai.models.report_types import AnalysisReport, Incident, RuleSet, Violation
from playpen.repo_level_awareness.api import ValidationError, ValidationResult, ValidationStep

@dataclass
class AnalyzerRuleViolation(ValidationError):
    incident: Incident
    violation: Violation
    ruleset: RuleSet  



from enum import StrEnum

from pydantic import BaseModel

from kai_commit_miner.attribution.models import AttributedFix
from kai_mcp_solution_server.db.python_objects import ViolationID


class MigrationRelevance(StrEnum):
    HIGH = "high"  # Clearly on the migration path
    MEDIUM = "medium"  # Probably migration-related, needs human review
    LOW = "low"  # Probably unrelated
    VERY_LOW = "very_low"  # Almost certainly unrelated, shouldn't be a rule


class HintCandidate(BaseModel):
    """A hint for an existing rule, generated from resolved violations.

    One hint per violation type per commit pair (not per incident).
    """

    violation_key: ViolationID
    hint_text: str
    sample_fixes: list[AttributedFix] = []
    incident_count: int = 0
    skipped: bool = False
    skipped_reason: str = ""


class RuleCandidate(BaseModel):
    """A candidate for a new analyzer-lsp rule, discovered from unattributed changes.

    Fields match the analyzer-lsp rule YAML format so they can be written
    directly to a ruleset file for review.
    """

    # analyzer-lsp rule fields
    ruleID: str = ""
    description: str = ""
    category: str = "potential"  # mandatory, optional, potential
    effort: int = 1
    message: str = ""
    labels: list[str] = []
    when_yaml: str = ""  # YAML string for the 'when' condition
    links: list[dict[str, str]] = []

    # Mining metadata (not part of the rule)
    migration_relevance: MigrationRelevance = MigrationRelevance.MEDIUM
    relevance_reasoning: str = ""  # LLM's explanation of why it scored this way
    source_file: str = ""
    source_commit: str = ""
    validation_notes: list[str] = []  # Structural issues with the rule


class ClassificationResult(BaseModel):
    """Result of LLM classification for a single commit pair."""

    commit_before: str
    commit_after: str
    hints: list[HintCandidate]
    rule_candidates: list[RuleCandidate]

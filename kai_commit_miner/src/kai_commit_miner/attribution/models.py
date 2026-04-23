from pydantic import BaseModel, Field

from kai_commit_miner.git.diff_parser import DiffHunk
from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.db.python_objects import ViolationID


class AttributedFix(BaseModel):
    """A resolved incident matched to the code change that fixed it."""

    model_config = {"arbitrary_types_allowed": True}

    incident: ExtendedIncident
    violation_key: ViolationID
    file_path: str
    relevant_hunks: list[DiffHunk]
    context_hunks: list[DiffHunk] = (
        []
    )  # Other hunks in the same file (knock-on changes)
    before_content: str
    after_content: str
    before_snippet: str = ""
    after_snippet: str = ""
    indirect: bool = False  # True if no direct hunk overlap found


class UnattributedChange(BaseModel):
    """A code change that doesn't correspond to any known resolved violation."""

    model_config = {"arbitrary_types_allowed": True}

    file_path: str
    hunks: list[DiffHunk]

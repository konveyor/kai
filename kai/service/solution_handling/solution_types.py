import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Solution(BaseModel):
    uri: str  # NOTE: This kinda doesn't make sense if we start to have multiple incidents associated with one solution
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    file_diff: str
    repo_diff: Optional[str] = None

    original_code: str
    updated_code: str

    # If None, then llm summary should not be generated.
    llm_summary_generated: Optional[bool] = None
    llm_summary: Optional[str] = None

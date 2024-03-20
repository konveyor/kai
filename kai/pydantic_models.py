import re

from pydantic import BaseModel


class FileSolutionContent(BaseModel):
    reasoning: str
    updated_file: str


# TODO: Sometimes this will fail. Why?
def parse_file_solution_content(content: str) -> FileSolutionContent:
    reasoning_pattern = r"## Reasoning\s+(.+?)(?=##|$)"
    updated_file_pattern = r"```java\s+(.+?)```"

    reasoning_match = re.search(reasoning_pattern, content, re.DOTALL)
    updated_file_match = re.search(updated_file_pattern, content, re.DOTALL)

    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    updated_file = updated_file_match.group(1).strip() if updated_file_match else ""

    return FileSolutionContent(reasoning=reasoning, updated_file=updated_file)

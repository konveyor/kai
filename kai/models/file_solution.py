import re
from typing import Any

from pydantic import BaseModel
from pygments import lexers
from pygments.util import ClassNotFound

import kai.logging.logging as logging

KAI_LOG = logging.get_logger(__name__)


class FileSolutionContent(BaseModel):
    reasoning: str
    updated_file: str
    additional_info: str


def guess_language(code: str, filename: str = None) -> str:
    try:
        if filename:
            lexer = lexers.guess_lexer_for_filename(filename, code)
            KAI_LOG.debug(f"{filename} classified as {lexer.aliases[0]}")
        else:
            lexer = lexers.guess_lexer(code)
            KAI_LOG.debug(f"Code content classified as {lexer.aliases[0]}\n{code}")
        return lexer.aliases[0]
    except ClassNotFound:
        KAI_LOG.debug(
            f"Code content for filename {filename} could not be classified\n{code}"
        )
        return "unknown"


def separate_sections(document: str) -> dict[str, Any]:
    section_titles = ["## Reasoning", "## Updated File", "## Additional Information"]
    # Find the start index of each section by looking for the section titles, filter out not found (-1) indices
    indices = {
        title: document.find(title)
        for title in section_titles
        if document.find(title) != -1
    }

    sorted_indices = dict(sorted(indices.items(), key=lambda item: item[1]))
    sorted_indices["end"] = len(document)
    titles_sorted = list(sorted_indices.keys()) + ["end"]

    # Extract the sections based on the indices found
    sections = {}
    for i, title in enumerate(
        titles_sorted[:-1]
    ):  # Skip the last item ('end') for iteration
        start_index = sorted_indices[title] + len(title)
        end_title = titles_sorted[i + 1]
        end_index = sorted_indices[end_title]
        sections[title] = document[start_index:end_index].strip()

    return sections


def parse_file_solution_content(language: str, content: str) -> FileSolutionContent:
    code_block_pattern = r"```(?:\w+)?\s+(.+?)```"

    sections = separate_sections(content)
    reasoning = sections.get("## Reasoning", "")
    updated_file_content = sections.get("## Updated File", "")
    additional_info = sections.get("## Additional Information", "")

    code_block_matches = re.findall(code_block_pattern, updated_file_content, re.DOTALL)

    matching_blocks = []
    for block in code_block_matches:
        guessed_language = guess_language(block)
        if language == guessed_language:
            matching_blocks.append(block)

    if matching_blocks:
        # If multiple matches default to first
        updated_file = matching_blocks[0].strip()
        if len(matching_blocks) > 1:
            KAI_LOG.debug(
                f"Multiple matching codeblocks found, defaulting to first {matching_blocks}"
            )
        else:
            KAI_LOG.debug(f"Found single matching codeblock \n{updated_file}")
    elif code_block_matches:
        # fallback to first discovered codeblock
        updated_file = code_block_matches[0]
        if len(code_block_matches) > 1:
            KAI_LOG.debug(
                f"Multiple codeblocks found, defaulting to first {code_block_matches}"
            )
        else:
            KAI_LOG.debug(f"Found single codeblock \n{updated_file}")
    else:
        updated_file = ""
        KAI_LOG.warn("No codeblocks detected in LLM response")
        KAI_LOG.debug(content)

    return FileSolutionContent(
        reasoning=reasoning, updated_file=updated_file, additional_info=additional_info
    )

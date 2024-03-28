import re

from pydantic import BaseModel
from pygments import lexers
from pygments.util import ClassNotFound

from kai.kai_logging import KAI_LOG


class FileSolutionContent(BaseModel):
    reasoning: str
    updated_file: str


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


def parse_file_solution_content(language: str, content: str) -> FileSolutionContent:
    reasoning_pattern = r"## Reasoning\s+(.+?)(?=##|$)"
    code_block_pattern = r"```(?:\w+)?\s+(.+?)```"

    reasoning_match = re.search(reasoning_pattern, content, re.DOTALL)
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    code_block_matches = re.findall(code_block_pattern, content, re.DOTALL)

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

    return FileSolutionContent(reasoning=reasoning, updated_file=updated_file)

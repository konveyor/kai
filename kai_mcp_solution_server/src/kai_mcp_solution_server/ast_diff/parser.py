from enum import StrEnum

import tree_sitter as ts
import tree_sitter_java as ts_java

from kai_mcp_solution_server.ast_diff.base import DiffableDict, DiffableSummary
from kai_mcp_solution_server.ast_diff.java import _extract_java_info


class Language(StrEnum):
    JAVA = "java"
    # TODO (pgaikwad): add a parser for xml
    XML = "xml"


def extract_ast_info(content: str, language: Language) -> DiffableSummary:
    """
    Returns a Diffable containing information about given AST node (usually root node of
    a file)
    """
    match language:
        case Language.JAVA:
            return _extract_java_info(
                ts.Parser(ts.Language(ts_java.language())).parse(
                    content.encode("utf-8")
                )
            )
    return DiffableDict()

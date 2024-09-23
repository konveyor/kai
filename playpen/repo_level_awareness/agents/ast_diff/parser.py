from enum import Enum

import tree_sitter as ts

from .base import DiffableDict, DiffableSummary
from .java import _extract_java_info


class Language(Enum):
    Java = "java"


def extract_ast_info(root: ts.Node, language: Language) -> DiffableSummary:
    """Returns a Diffable containing information about given AST node (usually root node of a file)"""
    match language:
        case Language.Java:
            return _extract_java_info(root)
    return DiffableDict()

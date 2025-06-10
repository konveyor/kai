import difflib

from kai_mcp_solution_server.dao import SolutionFile


def create_diff(before: list[SolutionFile], after: list[SolutionFile]) -> str:
    """
    Create the diff using the SolutionFile objects.
    """

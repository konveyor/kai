import argparse
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import List, Optional

from kai_solutions_dao import KaiSolutionsDAO, SolutionStatus, conn_pool
from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[KaiSolutionsDAO]:
    """
    This function is called once at server startup and once at shutdown.
    We create a DAO instance that will be available to tools.
    """
    conn_pool.initialize()

    dao = KaiSolutionsDAO.get_instance()

    try:
        yield dao
    finally:
        conn_pool.close()


mcp = FastMCP("KaiSolutionServer", lifespan=lifespan)


def get_dao(ctx: Optional[Context] = None) -> KaiSolutionsDAO:
    """
    Retrieve or create a KaiSolutionsDAO.
    If context is provided, gets DAO from lifespan context.
    Otherwise, creates a new DAO using the connection pool.
    """
    if ctx is not None and hasattr(ctx.request_context, "lifespan_context"):
        return ctx.request_context.lifespan_context
    else:
        return KaiSolutionsDAO.get_instance()


@mcp.tool()
def store_solution(
    ctx: Context,
    task: dict,
    before_code: str = "",
    after_code: str = "",
    # TODO THis should probably just be computed?
    diff: str = "",
    status: str = "unknown",
) -> int:
    """
    Insert a new Kai solution.

    Args:
        task: The task/issue JSON object
        before_code: Original code before the fix
        after_code: Modified code after the fix
        diff: Code diff between before and after
        status: Solution status (accepted/rejected/modified/unknown)

    Returns:
        The ID of the newly created solution
    """
    dao = get_dao(ctx)
    solution_id = dao.create_solution(
        task=task,
        before_code=before_code,
        after_code=after_code,
        diff=diff,
        status=status,
    )
    return solution_id


@mcp.tool()
def find_related_solutions(
    ctx: Context, task_key: Optional[str] = None, limit: int = 5
) -> List[dict]:
    """
    Find solutions related to specific criteria.

    Args:
        task_key: Optional specific task key to match
        limit: Maximum number of results to return

    Returns:
        List of matching solutions
    """
    dao = get_dao(ctx)
    solutions = dao.find_related_solutions(task_key=task_key, limit=limit)

    return [
        {
            "id": s.id,
            "task": s.task,
            "task_key": s.task_key,
            "before_code": s.before_code,
            "after_code": s.after_code,
            "diff": s.diff,
            "status": s.status.value,
        }
        for s in solutions
    ]


@mcp.resource("kai://success_rate/{task_key}")
def get_success_rate(task_key: str) -> str:
    """
    Resource to compute success rate (fraction of solutions with status=ACCEPTED).

    Args:
        task_key: The task key to get success rate for

    Returns:
        Success rate as a formatted string percentage
    """
    dao = KaiSolutionsDAO.get_instance()
    success_rate = dao.get_success_rate(task_key)
    return f"Success rate for task '{task_key}': {success_rate:.2%}"


@mcp.resource("kai://solutions/{task_key}")
def get_solution_history(task_key: str) -> str:
    """
    Resource to fetch the history of solutions for a given task_key.

    Args:
        task_key: The task key to get solutions for

    Returns:
        Formatted string with solution history
    """
    dao = KaiSolutionsDAO.get_instance()
    solutions = dao.get_solution_history(task_key)

    if not solutions:
        return f"No solutions found for task '{task_key}'"

    result = f"Found {len(solutions)} solutions for task '{task_key}':\n\n"

    for s in solutions:
        result += f"Solution ID: {s.id}\n"
        result += f"Status: {s.status.value}\n"
        if s.before_code:
            result += "Before Code:\n```\n" + s.before_code + "\n```\n"
        if s.after_code:
            result += "After Code:\n```\n" + s.after_code + "\n```\n"
        if s.diff:
            result += "Diff:\n```\n" + s.diff + "\n```\n"
        result += "\n---\n\n"

    return result


@mcp.resource("kai://example_solution/{task_key}")
def get_best_solution_example(task_key: str) -> str:
    """
    Resource to get the best (accepted) solution example for a task.

    Args:
        task_key: The task key to get an example solution for

    Returns:
        Formatted string with the best solution example
    """
    dao = KaiSolutionsDAO.get_instance()
    solutions = dao.get_solution_history(task_key)

    accepted_solutions = [s for s in solutions if s.status == SolutionStatus.ACCEPTED]

    if not accepted_solutions:
        return f"No accepted solutions found for task '{task_key}'"

    solution = accepted_solutions[-1]

    result = f"Best solution example for task '{task_key}':\n\n"
    result += f"Solution ID: {solution.id}\n"

    if solution.before_code:
        result += "Before Code:\n```\n" + solution.before_code + "\n```\n\n"

    if solution.after_code:
        result += "After Code:\n```\n" + solution.after_code + "\n```\n\n"

    if solution.diff:
        result += "Changes:\n```diff\n" + solution.diff + "\n```\n"

    return result


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Solution Server for KAI")
    parser.add_argument(
        "--transport",
        default="sse",
        choices=["sse", "stdio"],
        help="Transport protocol (sse or stdio)",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host to bind to (for sse transport)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (for sse transport)"
    )
    parser.add_argument("--db-path", help="Path to SQLite database file")
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level",
    )

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    # TODO: Can probably just defer to the envvars with some same defaults
    if args.db_path:
        os.environ["DB_PATH"] = args.db_path

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print(f"Starting MCP Solution Server with {args.transport} transport")

    # Set environment variables for host and port that might be used internally
    # TODO: Can probably just defer to the envvars with some same defaults
    if args.transport == "sse":
        print(f"Listening on {args.host}:{args.port}")
        os.environ["MCP_HOST"] = args.host
        os.environ["MCP_PORT"] = str(args.port)

    # Run the server with the specified transport
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()

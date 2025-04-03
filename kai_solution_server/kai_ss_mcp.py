import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

# Import the DAO and data structures
from kai_solutions_dao import KaiSolution, KaiSolutionsDAO, SolutionStatus
from mcp.server.fastmcp import Context, FastMCP

#
# 1) Create an MCP server
#


#
# 2) Lifespan that provides a DB connection
#
@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[sqlite3.Connection]:
    """
    This function is called once at server startup and once at shutdown.
    We create (and store) our SQLite connection, which the DAO will use.
    """
    conn = sqlite3.connect("kai_solutions.db")
    try:
        yield conn
    finally:
        conn.close()


mcp = FastMCP("KaiSolutionServer", lifespan=lifespan)


#
# 3) Helper to get a DAO instance from the lifespan context
#
def get_dao(ctx: Context) -> KaiSolutionsDAO:
    """
    Retrieve or create a KaiSolutionsDAO. The DB connection
    is found via ctx.request_context.lifespan_context.
    """
    db_conn = ctx.request_context.lifespan_context
    return KaiSolutionsDAO(db_conn)


#
# 4) Tools (writes/updates)
#


@mcp.tool()
def store_solution(
    ctx: Context,
    task: dict,
    before_code: str = "",
    after_code: str = "",
    diff: str = "",
    status: str = "unknown",
) -> int:
    """
    Insert a new Kai solution. We call our DAO for actual DB operations.
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
def update_solution_status(ctx: Context, solution_id: int, status: str) -> bool:
    """
    Change the status of a solution. We call our DAO for the update.
    """
    dao = get_dao(ctx)
    return dao.update_solution_status(solution_id, status)


#
# 5) Resources (reads)
#


@mcp.resource("kai://success_rate/{task_key}")
def get_success_rate(task_key: str) -> float:
    """
    Resource to compute success rate (fraction of solutions with status=ACCEPTED).
    """
    ctx = Context.current()
    dao = get_dao(ctx)
    return dao.get_success_rate(task_key)


@mcp.resource("kai://solution_history/{task_key}")
def get_solution_history(task_key: str) -> list[dict[str, Any]]:
    """
    Resource to fetch the history of solutions for a given task_key.
    """
    ctx = Context.current()
    dao = get_dao(ctx)
    solutions = dao.get_solution_history(task_key)
    # Convert KaiSolution objects to dict
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


#
# 6) Entry point if running directly
#
if __name__ == "__main__":
    mcp.run()

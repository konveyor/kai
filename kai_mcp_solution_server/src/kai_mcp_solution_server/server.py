import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from fastmcp import Context, FastMCP

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.constants import log
from kai_mcp_solution_server.db.python_objects import SolutionFile, ViolationID
from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.service import (
    CreateIncidentResult,
    GetBestHintResult,
    SuccessRateMetric,
    accept_file,
    create_incident,
    create_solution,
    delete_solution,
    get_best_hint,
    get_success_rate,
    reject_file,
)
from kai_mcp_solution_server.settings import SolutionServerSettings


def _get_kai_ctx(ctx: Context) -> KaiSolutionServerContext:
    """Extract KaiSolutionServerContext from an MCP Context."""
    if ctx.request_context is None:
        raise RuntimeError("No request context available")
    return cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)


@asynccontextmanager
async def kai_solution_server_lifespan(
    server: FastMCP[KaiSolutionServerContext],
) -> AsyncIterator[KaiSolutionServerContext]:
    log("kai_solution_server_lifespan")
    try:
        settings = SolutionServerSettings()
        log(f"Settings: {settings.model_dump_json(indent=2)}")

        log("creating context")
        ctx = KaiSolutionServerContext(settings)
        await ctx.create()
        log("yielding context")

        yield ctx
    except Exception:
        log(f"Error in lifespan: {traceback.format_exc()}")
        raise


mcp: FastMCP[KaiSolutionServerContext] = FastMCP(
    "KaiSolutionServer", lifespan=kai_solution_server_lifespan
)


@mcp.tool(name="create_incident")
async def tool_create_incident(
    ctx: Context,
    client_id: str,
    extended_incident: ExtendedIncident,
) -> int:
    """
    Create an incident in the database.
    This function will create a new incident in the database, associating it with
    the provided client ID and the extended incident data. If the violation
    associated with the incident does not exist in the database, it will be created
    as well.
    """
    kai_ctx = _get_kai_ctx(ctx)
    return await create_incident(
        kai_ctx,
        client_id,
        extended_incident,
    )


@mcp.tool(name="create_multiple_incidents")
async def tool_create_multiple_incidents(
    ctx: Context,
    client_id: str,
    extended_incidents: list[ExtendedIncident],
) -> list[CreateIncidentResult]:
    """
    Create multiple incidents in the database.
    This function will create multiple new incidents in the database, associating
    them with the provided client ID and the list of extended incident data.
    If any of the violations associated with the incidents do not exist in the
    database, they will be created as well.
    """
    kai_ctx = _get_kai_ctx(ctx)
    results: list[CreateIncidentResult] = []
    for extended_incident in extended_incidents:
        incident_id = await create_incident(kai_ctx, client_id, extended_incident)
        results.append(CreateIncidentResult(incident_id=incident_id, solution_id=0))

    return results


@mcp.tool(name="create_solution")
async def tool_create_solution(
    ctx: Context,
    client_id: str,
    incident_ids: list[int],
    before: list[SolutionFile],
    after: list[SolutionFile],
    reasoning: str | None = None,
    used_hint_ids: list[int] | None = None,
) -> int:
    """
    Create a solution in the database.
    This function will create a new solution in the database, associating it with
    the provided client ID, incident IDs, change set, reasoning, and used hint IDs.
    If the incident IDs do not exist in the database, a ValueError will be raised.
    If the used hint IDs do not exist in the database, a ValueError will be raised
    """
    kai_ctx = _get_kai_ctx(ctx)
    return await create_solution(
        kai_ctx,
        client_id,
        incident_ids,
        before,
        after,
        reasoning,
        used_hint_ids,
    )


@mcp.tool(name="delete_solution")
async def tool_delete_solution(
    ctx: Context,
    client_id: str,
    solution_id: int,
) -> bool:
    """
    Delete the solution with the given ID from the database.
    """
    kai_ctx = _get_kai_ctx(ctx)
    return await delete_solution(
        kai_ctx,
        client_id,
        solution_id,
    )


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.


@mcp.tool(name="get_best_hint")
async def tool_get_best_hint(
    ctx: Context,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
    """
    Get the best hint for a given ruleset and violation name.
    This function retrieves the most recent hint for the specified ruleset and
    violation name from the database. If no hint is found, it returns None.
    If a hint is found, it returns a GetBestHintResult object containing the hint text
    and the hint ID. The hint is considered the best if it has at least one solution
    with the status "accepted".
    """
    kai_ctx = _get_kai_ctx(ctx)
    return await get_best_hint(
        kai_ctx,
        ruleset_name,
        violation_name,
    )


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.
@mcp.tool(name="get_success_rate")
async def tool_get_success_rate(
    ctx: Context,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
    """
    Get the success rate for a list of violations.

    This function retrieves the success rate for the given list of violations from the
    database. The success rate is calculated as the number of accepted solutions divided
    by the total number of solutions for each violation. If no violations are provided,
    an empty list is returned. If any of the violations do not exist in the database,
    they are ignored.
    """
    kai_ctx = _get_kai_ctx(ctx)
    return await get_success_rate(
        kai_ctx,
        violation_ids,
    )


@mcp.tool(name="accept_file")
async def tool_accept_file(
    ctx: Context,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    kai_ctx = _get_kai_ctx(ctx)
    return await accept_file(
        kai_ctx,
        client_id,
        solution_file,
    )


@mcp.tool(name="reject_file")
async def tool_reject_file(
    ctx: Context,
    client_id: str,
    file_uri: str,
) -> None:
    kai_ctx = _get_kai_ctx(ctx)
    return await reject_file(
        kai_ctx,
        client_id,
        file_uri,
    )

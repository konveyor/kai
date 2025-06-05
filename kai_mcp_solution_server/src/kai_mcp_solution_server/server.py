import asyncio
import os
import sys
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastmcp import Context, FastMCP
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.constants import log
from kai_mcp_solution_server.dao import (
    DBHint,
    DBIncident,
    DBSolution,
    DBViolation,
    Solution,
    SolutionChangeSet,
    SolutionStatus,
    ViolationID,
    get_async_engine,
)


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    pg_dsn: str = (
        "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
    )

    llm_params: dict[str, Any] = {
        "model": "gpt-4o-mini",
        "model_provider": "openai",
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
    }

    drop_all: bool = False


class KaiSolutionServerContext:
    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings

    async def create(self) -> None:
        self.engine = await get_async_engine(
            self.settings.pg_dsn, self.settings.drop_all
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        self.model = init_chat_model(**self.settings.llm_params)


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
    except Exception as e:

        log(f"Error in lifespan: {traceback.format_exc()}")
        raise e
    finally:
        pass


mcp: FastMCP[KaiSolutionServerContext] = FastMCP(
    "KaiSolutionServer", lifespan=kai_solution_server_lifespan, dependencies=[]
)


class CreateProposedSolutionResult(BaseModel):
    incident_id: int
    solution_id: int


@mcp.tool()
async def create_incident(
    ctx: Context,
    client_id: str,
    extended_incident: ExtendedIncident,
    # proposed_solution: Solution,
) -> int:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)

    async with kai_ctx.session_maker.begin() as session:
        violation_stmt = select(DBViolation).where(
            DBViolation.ruleset_name == extended_incident.ruleset_name,
            DBViolation.violation_name == extended_incident.violation_name,
        )

        violation = (await session.execute(violation_stmt)).scalar_one_or_none()
        if violation is None:
            log(
                f"Violation {extended_incident.ruleset_name} - {extended_incident.violation_name} not found in the database.",
            )

            violation = DBViolation(
                ruleset_name=extended_incident.ruleset_name,
                ruleset_description=extended_incident.ruleset_description,
                violation_name=extended_incident.violation_name,
                violation_category=extended_incident.violation_category,
                incidents=set(),
                hints=set(),
            )
            session.add(violation)

        incident = DBIncident(
            client_id=client_id,
            uri=extended_incident.uri,
            message=extended_incident.message,
            code_snip=extended_incident.code_snip,
            line_number=extended_incident.line_number,
            variables=extended_incident.variables,
            violation=violation,
            solution=None,
        )
        session.add(incident)

        await session.commit()

    return incident.id


@mcp.tool()
async def create_solution(
    ctx: Context,
    client_id: str,
    incident_ids: list[int],
    change_set: SolutionChangeSet,
    reasoning: str | None = None,
    used_hint_id: int | None = None,
) -> int:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)

    if len(incident_ids) == 0:
        raise ValueError("At least one incident ID must be provided.")

    async with kai_ctx.session_maker.begin() as session:
        incident_ids_cond = [
            and_(DBIncident.id == incident_id, DBIncident.client_id == client_id)
            for incident_id in incident_ids
        ]
        incidents_stmt = select(DBIncident).where(or_(*incident_ids_cond))
        incidents = (await session.execute(incidents_stmt)).scalars().all()

        hint_stmt = select(DBHint).where(DBHint.id == used_hint_id)
        hint = (await session.execute(hint_stmt)).scalar_one_or_none()
        if used_hint_id is not None and hint is None:
            raise ValueError(f"Hint with ID {used_hint_id} not found in the database.")

        solution = DBSolution(
            client_id=client_id,
            change_set=change_set,
            reasoning=reasoning,
            solution_status=SolutionStatus.PENDING,
            incidents=set(incidents),
            hint=hint,
        )

        session.add(solution)
        await session.commit()

    return solution.id


@mcp.tool()
async def update_solution_status(
    ctx: Context,
    client_id: str,
    solution_status: SolutionStatus = SolutionStatus.ACCEPTED,
) -> None:
    """
    Update the status of the solution with the given ID in the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()

        for solution in solutions:
            solution.solution_status = solution_status

        await session.commit()

    if solution_status == SolutionStatus.ACCEPTED:
        asyncio.create_task(generate_hint(kai_ctx, client_id))


async def generate_hint(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    return
    """
    async with kai_ctx.session_maker.begin() as session:
        incident_stmt = select(DBIncident).where(DBIncident.id == incident_id)
        incident = (await session.execute(incident_stmt)).scalar_one_or_none()
        if incident is None:
            raise ValueError(
                f"Incident with ID {incident_id} not found in the database."
            )

        should_generate_hint = not any(
            solution.solution_status == SolutionStatus.ACCEPTED
            for solution in incident.solutions
        )

        if not should_generate_hint:
            log(
                f"No new hint generated for incident {incident_id} as there are accepted solutions."
            )
            return

        log(f"Generating hint for incident {incident_id}...")
        prompt = (
            f"Generate a hint for the following incident:\n"
            f"URI: {incident.uri}\n"
            f"Message: {incident.message}\n"
            f"Code Snippet: {incident.code_snip}\n"
            f"Line Number: {incident.line_number}\n"
            f"Variables: {incident.variables}\n"
            f"Violation: {incident.violation.ruleset_name} - {incident.violation.violation_name}\n"
        )
        response = await cast(BaseChatModel, kai_ctx.model).ainvoke(prompt)

        log(f"Generated hint: {response}")

        hint = DBHint(
            text=str(response.content),
            incident=incident,
            violation=incident.violation,
        )
        session.add(hint)
        await session.commit()
    """


@mcp.tool()
async def delete_solution(
    ctx: Context,
    client_id: str,
    solution_id: int,
) -> bool:
    """
    Delete the solution with the given ID from the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBSolution, solution_id)
        if sln is None:
            return False
        await session.delete(sln)
        await session.commit()
    return True


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.
@mcp.tool()
async def get_best_hint(
    ctx: Context,
    incident_id: int,
) -> str | None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        incident_stmt = select(DBIncident).where(DBIncident.id == incident_id)
        incident = (await session.execute(incident_stmt)).scalar_one_or_none()
        if incident is None:
            raise ValueError(
                f"Incident with ID {incident_id} not found in the database."
            )

        hints = list(incident.hints)
        if len(hints) == 0:
            return None

        # try to get a hint that is associated with an accepted solution
        # if no solutions are accepted, return a random hint
        accepted_hints = [
            h
            for h in hints
            if any(
                s.solution_status == SolutionStatus.ACCEPTED for s in incident.solutions
            )
        ]

        if len(accepted_hints) > 0:
            return accepted_hints[0].text

        # if no accepted hints, return the most recently created hint
        hints.sort(key=lambda h: h.created_at, reverse=True)
        return hints[0].text


class SuccessRateMetric(BaseModel):
    counted_solutions: int
    accepted_solutions: int


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.
@mcp.tool()
async def get_success_rate(
    ctx: Context,
    violation_ids: list[ViolationID],
    all_attempts: bool = False,
) -> list[SuccessRateMetric] | None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    result: list[SuccessRateMetric] = []

    if len(violation_ids) == 0:
        return result

    async with kai_ctx.session_maker.begin() as session:
        violation_ids_stmt = [
            and_(
                DBViolation.ruleset_name == ruleset_name,
                DBViolation.violation_name == violation_name,
            )
            for ruleset_name, violation_name in violation_ids
        ]
        violations_stmt = select(DBViolation).where(or_(*violation_ids_stmt))
        violations = (await session.execute(violations_stmt)).scalars().all()

        for violation in violations:
            metric = SuccessRateMetric(
                counted_solutions=0,
                accepted_solutions=0,
            )

            for incident in violation.incidents:
                if all_attempts:
                    metric.counted_solutions += len(incident.solutions)
                    metric.accepted_solutions += sum(
                        solution.solution_status == SolutionStatus.ACCEPTED
                        for solution in incident.solutions
                    )
                else:
                    metric.counted_solutions += 1
                    metric.accepted_solutions += int(
                        any(
                            solution.solution_status == SolutionStatus.ACCEPTED
                            for solution in incident.solutions
                        )
                    )

            result.append(metric)

    return result

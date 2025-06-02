import asyncio
import difflib
import os
import sys
import traceback
from asyncio import sleep
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastmcp import Context, FastMCP
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel, BaseMessage
from mcp import ServerSession
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Text
from sqlalchemy import cast as sacast
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from kai_mcp_solution_server.analyzer_types import Category, ExtendedIncident
from kai_mcp_solution_server.dao import (
    DBHint,
    DBIncident,
    DBSolution,
    DBViolation,
    Solution,
    SolutionStatus,
    get_async_engine,
)

# print_err = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)
log_file = open("stderr.log", "a")
log_file.close()


def log(*args, **kwargs) -> None:
    print(*args, file=log_file if not log_file.closed else sys.stderr, **kwargs)


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    pg_dsn: str = cast(
        str, "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
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
async def create_solution(
    ctx: Context,  # type: ignore[type-arg]
    extended_incident: ExtendedIncident,
    proposed_solution: Solution,
) -> CreateProposedSolutionResult:
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

        incident_stmt = select(DBIncident).where(
            DBIncident.id == extended_incident.incident_id
        )

        incident = (await session.execute(incident_stmt)).scalar_one_or_none()
        if incident is None:
            log(f"Incident {extended_incident.incident_id} not found in the database.")

            incident = DBIncident(
                id=extended_incident.incident_id,
                uri=extended_incident.uri,
                message=extended_incident.message,
                code_snip=extended_incident.code_snip,
                line_number=extended_incident.line_number,
                variables=extended_incident.variables,
                violation=violation,
                solutions=set(),
                hints=set(),
            )
            session.add(incident)

        hint_smt = select(DBHint).where(DBHint.id == proposed_solution.hint_id)
        hint = (await session.execute(hint_smt)).scalar_one_or_none()
        if hint is None and proposed_solution.hint_id is not None:
            raise ValueError(
                f"Hint {proposed_solution.hint_id} not found in the database."
            )
        elif hint is not None:
            if hint not in incident.hints:
                raise ValueError(
                    f"Hint {proposed_solution.hint_id} is not associated with the incident {extended_incident.incident_id}."
                )
            if hint not in violation.hints:
                raise ValueError(
                    f"Hint {proposed_solution.hint_id} is not associated with the violation {extended_incident.ruleset_name} - {extended_incident.violation_name}."
                )

        solution = DBSolution(
            before_uri=proposed_solution.before_uri,
            before_content=proposed_solution.before_content,
            after_uri=proposed_solution.after_uri,
            after_content=proposed_solution.after_content,
            solution_status=proposed_solution.solution_status,
            incident=incident,
            hint=hint,
        )

        session.add(solution)
        await session.commit()

    asyncio.create_task(generate_hint(kai_ctx, incident.id))

    return CreateProposedSolutionResult(
        incident_id=incident.id,
        solution_id=solution.id,
    )


async def generate_hint(
    kai_ctx: KaiSolutionServerContext,
    incident_id: int,
) -> None:
    async with kai_ctx.session_maker.begin() as session:
        session = cast(AsyncSession, session)  # TODO: fix type hinting

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
        response = cast(
            BaseMessage, await cast(BaseChatModel, kai_ctx.model).ainvoke(prompt)
        )

        log(f"Generated hint: {response}")

        hint = DBHint(
            text=str(response.content),
            incident=incident,
            violation=incident.violation,
        )
        session.add(hint)
        await session.commit()


@mcp.tool()
async def update_solution_status(
    ctx: Context,  # type: ignore[type-arg]
    solution_id: int,
    solution_status: SolutionStatus = SolutionStatus.ACCEPTED,
) -> DBSolution:
    """
    Update the status of the solution with the given ID in the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBSolution, solution_id)
        if sln is None:
            raise ValueError(f"Solution with ID {solution_id} not found.")

        sln.solution_status = solution_status
        await session.commit()
        return sln


@mcp.tool()
async def delete_solution(
    ctx: Context,  # type: ignore[type-arg]
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


@mcp.tool()
async def get_best_hint(
    ctx: Context,  # type: ignore[type-arg]
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


@mcp.tool()
async def get_success_rate(
    ctx: Context,  # type: ignore[type-arg]
    extended_incident: ExtendedIncident,
) -> float:
    """
    Get the success rate of the given incident in the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        solutions_result = await session.execute(select(DBSolution))
        solutions = list(solutions_result)

        log(f"Solutions: {solutions}")

        if not solutions:
            return -1.0

        accepted_count = sum(
            1 for solution in solutions if solution[0].status == SolutionStatus.ACCEPTED
        )
        proportion = accepted_count / len(solutions)
        return proportion

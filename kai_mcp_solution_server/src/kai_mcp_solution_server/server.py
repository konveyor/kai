import asyncio
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from fastmcp import Context, FastMCP
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from langchain_core.language_models.fake_chat_models import FakeChatModel
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
    SolutionChangeSet,
    SolutionStatus,
    ViolationID,
    get_async_engine,
)


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    # "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
    # "sqlite+aiosqlite:////home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/kai_mcp_solution_server/kai_mcp_solution_server.db"
    db_dsn: str

    llm_params: dict[str, Any] | None

    drop_all: bool = False


class KaiSolutionServerContext:
    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings

    async def create(self) -> None:
        self.engine = await get_async_engine(
            self.settings.db_dsn, self.settings.drop_all
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        self.model: BaseChatModel

        if self.settings.llm_params is None:
            raise ValueError("LLM parameters must be provided in the settings.")
        elif self.settings.llm_params.get("model") == "fake":
            self.model = FakeChatModel()
        else:
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


class CreateIncidentResult(BaseModel):
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


# TODO: Support multiple hint ids
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
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            DBSolution.solution_status == SolutionStatus.ACCEPTED,
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            log(
                f"No accepted solutions found for client {client_id}. No hint generated."
            )
            return

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Generate a hint for the user so that they can perform the same solution:\n"
            )

            for i, incident in enumerate(solution.incidents):
                prompt += (
                    f"Incident {i + 1}:\n"
                    f"  URI: {incident.uri}\n"
                    f"  Message: {incident.message}\n"
                    f"  Code Snippet: {incident.code_snip}\n"
                    f"  Line Number: {incident.line_number}\n"
                    f"  Variables: {incident.variables}\n"
                    f"  Violation: {incident.violation.ruleset_name} - "
                    f"  {incident.violation.violation_name}\n\n"
                )

            prompt += "Solution:\n" f"{solution.change_set.diff}\n\n"

            log(f"Generating hint for client {client_id} with prompt:\n{prompt}")

            response = await cast(BaseChatModel, kai_ctx.model).ainvoke(prompt)

            log(f"Generated hint: {response.content}")

            hint = DBHint(
                text=str(response.content),
                violations=set(
                    incident.violation
                    for incident in solution.incidents
                    if incident.violation is not None
                ),
                solutions=set([solution]),
            )
            session.add(hint)

            await session.flush()

        await session.commit()

    return


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


class GetBestHintResult(BaseModel):
    hint: str
    hint_id: int


@mcp.tool()
async def get_best_hint(
    ctx: Context,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)

    async with kai_ctx.session_maker.begin() as session:
        violation_name_stmt = select(DBViolation).where(
            DBViolation.ruleset_name == ruleset_name,
            DBViolation.violation_name == violation_name,
        )
        violation = (await session.execute(violation_name_stmt)).scalar_one_or_none()
        if violation is None:
            log(
                f"Violation {ruleset_name} - {violation_name} not found in the database.",
            )
            return None

        for hint in sorted(violation.hints, key=lambda h: h.created_at, reverse=True):
            if any(
                s.solution_status == SolutionStatus.ACCEPTED for s in hint.solutions
            ):
                return GetBestHintResult(
                    hint=hint.text,
                    hint_id=hint.id,
                )

    return None


class SuccessRateMetric(BaseModel):
    counted_solutions: int
    accepted_solutions: int


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.
@mcp.tool()
async def get_success_rate(
    ctx: Context,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    result: list[SuccessRateMetric] = []

    if len(violation_ids) == 0:
        return result

    async with kai_ctx.session_maker.begin() as session:
        violations_where = or_(  # type: ignore[arg-type]
            and_(
                DBViolation.ruleset_name == violation_id.ruleset_name,
                DBViolation.violation_name == violation_id.violation_name,
            )
            for violation_id in violation_ids
        )
        # Hack using text() to avoid strange tuple error with SQLAlchemy
        violations_stmt = select(DBViolation).where(violations_where)
        # violations_values = {}
        # for i, violation_id in enumerate(violation_ids, 1):
        #     violations_values[f"ruleset_name_{i}"] = violation_id.ruleset_name
        #     violations_values[f"violation_name_{i}"] = violation_id.violation_name

        # print(f"Violations values: {violations_values}", file=sys.stderr)

        # violations_stmt = violations_stmt.bindparams(**violations_values)

        # print(f"SQL Statement: {str(violations_stmt)}", file=sys.stderr)
        # return None

        violations = (await session.execute(violations_stmt)).scalars().all()
        # violations = cast(Sequence[DBViolation], violations)

        for violation in violations:
            metric = SuccessRateMetric(
                counted_solutions=0,
                accepted_solutions=0,
            )

            for incident in violation.incidents:
                if incident.solution is None:
                    continue

                metric.counted_solutions += 1
                metric.accepted_solutions += int(
                    incident.solution is not None
                    and incident.solution.solution_status == SolutionStatus.ACCEPTED
                )

            result.append(metric)

    return result

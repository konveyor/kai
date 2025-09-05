import asyncio
import json
import os
import sys
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Any, cast

from fastmcp import Context, FastMCP
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models.fake import FakeListChatModel
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict
from sqlalchemy import URL, and_, make_url, or_, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.ast_diff.parser import Language, extract_ast_info
from kai_mcp_solution_server.constants import log
from kai_mcp_solution_server.db.dao import (
    DBFile,
    DBHint,
    DBIncident,
    DBSolution,
    DBViolation,
    get_async_engine,
)
from kai_mcp_solution_server.db.python_objects import (
    SolutionFile,
    SolutionStatus,
    ViolationID,
    associate_files,
    get_diff,
)


class SolutionServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kai_")

    db_dsn: Annotated[URL, NoDecode]
    """
    Example DSNs:
    - PostgreSQL: `postgresql+asyncpg://username:password@host:port/database`
    - SQLite: `sqlite+aiosqlite:///path/to/database.db`
    """

    llm_params: dict[str, Any] | None

    drop_all: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_db_dsn(cls, data: Any) -> Any:
        """
        Environment variables added:
        - `KAI_DB_DRIVERNAME`
        - `KAI_DB_USERNAME`
        - `KAI_DB_PASSWORD`
        - `KAI_DB_HOST`
        - `KAI_DB_PORT`
        - `KAI_DB_DATABASE`

        1. Any parameters supplied via Python's `SolutionServerSettings`
           constructor takes highest precedence, then any configuration supplied
           via `KAI_DB_DSN`.
        2. Try to parse `KAI_DB_DSN` as a json object, containing `drivername`,
           `username`, etc... If that fails, parse it as a connection string.
        3. If the `KAI_DB_DSN` environment variable or the `db_dsn` field is not
           supplied, try to get all information from the new variables
        """

        if isinstance(data, dict):
            kwargs: dict[str, Any]

            if "db_dsn" not in data:
                kwargs = {}

            elif isinstance(data["db_dsn"], URL):
                kwargs = data["db_dsn"]._asdict()

            elif isinstance(data["db_dsn"], dict):
                kwargs = data["db_dsn"]

            elif isinstance(data["db_dsn"], str):
                try:
                    kwargs = json.loads(data["db_dsn"])
                except json.JSONDecodeError:
                    kwargs = make_url(data["db_dsn"])._asdict()

            else:
                raise ValueError(
                    f"Invalid type for db_dsn: {type(data['db_dsn'])}. Expected missing, str, dict, or URL."
                )

            for key in [
                "drivername",
                "username",
                "password",
                "host",
                "port",
                "database",
            ]:
                if kwargs.get(key) is None:
                    kwargs[key] = os.getenv(f"KAI_DB_{key.upper()}", None)

            data["db_dsn"] = URL.create(**kwargs)

        return data


class KaiSolutionServerContext:
    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings
        self.lock = asyncio.Lock()

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
            llm_params = self.settings.llm_params.copy()
            llm_params.pop("model", None)
            if "responses" not in llm_params:
                llm_params["responses"] = [
                    "fake response",
                ]
            self.model = FakeListChatModel(**llm_params)
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


async def create_incident(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    extended_incident: ExtendedIncident,
) -> int:
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
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
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
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    results: list[CreateIncidentResult] = []

    async with kai_ctx.lock:
        for extended_incident in extended_incidents:
            incident_id = await create_incident(kai_ctx, client_id, extended_incident)
            results.append(CreateIncidentResult(incident_id=incident_id, solution_id=0))

    return results


async def create_solution(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    incident_ids: list[int],
    before: list[SolutionFile],
    after: list[SolutionFile],
    reasoning: str | None = None,
    used_hint_ids: list[int] | None = None,
) -> int:
    if len(incident_ids) == 0:
        raise ValueError("At least one incident ID must be provided.")

    if used_hint_ids is None:
        used_hint_ids = []

    async with kai_ctx.session_maker.begin() as session:
        incident_ids_cond = [
            and_(DBIncident.id == incident_id, DBIncident.client_id == client_id)
            for incident_id in incident_ids
        ]
        incidents_stmt = select(DBIncident).where(or_(*incident_ids_cond))
        incidents = (await session.execute(incidents_stmt)).scalars().all()

        hint_stmt = select(DBHint).where(DBHint.id.in_(used_hint_ids))
        hints = (await session.execute(hint_stmt)).scalars().all()

        if missing_ids := set(used_hint_ids) - {hint.id for hint in hints}:
            raise ValueError(
                f"Some hint IDs {missing_ids} do not exist in the database."
            )

        # Try to match the before files. If you can't, create them.
        # Create the after files. Associate them with the before files.
        # Create the solution.

        db_before_files: set[DBFile] = set()
        for file in before:
            stmt = (
                select(DBFile)
                .where(
                    DBFile.client_id == client_id,
                    DBFile.uri == file.uri,
                )
                .order_by(DBFile.created_at.desc())
            )
            prev_before = (await session.execute(stmt)).scalars().first()

            if prev_before is None or prev_before.content != file.content:
                next_before = DBFile(
                    client_id=client_id,
                    uri=file.uri,
                    content=file.content,
                    status=SolutionStatus.PENDING,
                    solution_before=set(),
                    solution_after=set(),
                )
                session.add(next_before)
                db_before_files.add(next_before)
            else:
                db_before_files.add(prev_before)

        db_after_files: set[DBFile] = set()
        for file in after:
            # FIXME: Something is fishy here...
            next_after = DBFile(
                client_id=client_id,
                uri=file.uri,
                content=file.content,
                status=SolutionStatus.PENDING,
                solution_before=set(),
                solution_after=set(),
            )

            stmt = (
                select(DBFile)
                .where(
                    DBFile.client_id == client_id,
                    DBFile.uri == file.uri,
                )
                .order_by(DBFile.created_at.desc())
            )

            db_after_files.add(next_after)
            session.add(next_after)

        solution = DBSolution(
            client_id=client_id,
            before=db_before_files,
            after=db_after_files,
            reasoning=reasoning,
            solution_status=SolutionStatus.UNKNOWN,
            incidents=set(incidents),
            hints=set(hints),
        )

        session.add(solution)
        await session.commit()

    return solution.id


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
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await create_solution(
            kai_ctx,
            client_id,
            incident_ids,
            before,
            after,
            reasoning,
            used_hint_ids,
        )


async def generate_hint_v1(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            log(
                f"No accepted or modified solutions found for client {client_id}. No hint generated."
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

            diff = get_diff(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            prompt += "Solution:\n" f"{diff}\n\n"

            log(f"Generating hint for client {client_id} with prompt:\n{prompt}")

            response = await kai_ctx.model.ainvoke(prompt)

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


async def generate_hint_v2(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    # print(f"Generating hint for client {client_id}", file=sys.stderr)
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            print(
                f"No accepted solutions found for client {client_id}. No hint generated.",
                file=sys.stderr,
            )
            return

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Generate a hint for the user so that they can create the same solution:\n"
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

            diff = associate_files(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            ast_diffs: list[dict[str, Any]] = []
            for (_before_uri, _after_uri), (before_file, after_file) in diff.items():
                if before_file.content == after_file.content:
                    continue

                ast_diffs.append(
                    extract_ast_info(before_file.content, language=Language.JAVA).diff(
                        extract_ast_info(after_file.content, language=Language.JAVA)
                    )
                )

            ast_diff_str = "\n\n".join(str(a) for a in ast_diffs if a is not None)
            prompt += f"AST Diff:\n{ast_diff_str}\n\n"

            # print(f"Generating hint for client {client_id} with prompt:\n{prompt}", file=sys.stderr)

            response = await kai_ctx.model.ainvoke(prompt)

            # print(f"Generated hint: {response.content}", file=sys.stderr)

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


async def generate_hint_v3(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    """
    Generate hints for accepted solutions using improved prompt format with better structure.
    """
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(
            DBSolution.client_id == client_id,
            or_(
                DBSolution.solution_status == SolutionStatus.ACCEPTED,
                DBSolution.solution_status == SolutionStatus.MODIFIED,
            ),
        )
        solutions = (await session.execute(solutions_stmt)).scalars().all()
        if len(solutions) == 0:
            print(
                f"No accepted or modified solutions found for client {client_id}. No hint generated.",
                file=sys.stderr,
            )
            return

        for solution in solutions:
            prompt = (
                "The following incidents had this accepted solution. "
                "Use the AST diffs below as a guiding pattern for migration.\n\n"
                "Generate a hint for the user so that they can migrate the code.\n\n"
                "IMPORTANT: Follow this EXACT output format:\n"
                "---\n"
                "SUMMARY:\n"
                "[concise summary of necessary changes]\n\n"
                "HINT:\n"
                "[numbered steps with generic, reusable code examples]\n"
                "---\n\n"
                "Guidelines for high-quality response:\n"
                "1. Keep SUMMARY concise and focused\n"
                "2. Use numbered steps (1, 2, 3) in HINT section\n"
                "3. Provide generic before/after code examples that can be reused and mark them as examples (e.g. 'Example 1: Before: ... After: ...')\n"
                "4. Write in direct, actionable tone\n"
                "Incidents:\n"
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

            diff = associate_files(
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.before],
                [SolutionFile(uri=f.uri, content=f.content) for f in solution.after],
            )

            ast_diffs: list[dict[str, Any]] = []
            for (_before_uri, _after_uri), (before_file, after_file) in diff.items():
                if before_file.content == after_file.content:
                    continue

                ast_diffs.append(
                    extract_ast_info(before_file.content, language=Language.JAVA).diff(
                        extract_ast_info(after_file.content, language=Language.JAVA)
                    )
                )

            ast_diff_str = "\n\n".join(str(a) for a in ast_diffs if a is not None)
            prompt += f"AST Diff:\n{ast_diff_str}\n\n"

            response = await kai_ctx.model.ainvoke(prompt)

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


async def delete_solution(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_id: int,
) -> bool:
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBSolution, solution_id)
        if sln is None:
            return False
        await session.delete(sln)
        await session.commit()
    return True


@mcp.tool(name="delete_solution")
async def tool_delete_solution(
    ctx: Context,
    client_id: str,
    solution_id: int,
) -> bool:
    """
    Delete the solution with the given ID from the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await delete_solution(
            kai_ctx,
            client_id,
            solution_id,
        )


# TODO: Make this a resource instead of a tool. Need to figure out how to handle
# lists in a resource.


class GetBestHintResult(BaseModel):
    hint: str
    hint_id: int


async def get_best_hint(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
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
                s.solution_status == SolutionStatus.ACCEPTED
                or s.solution_status == SolutionStatus.MODIFIED
                for s in hint.solutions
            ):
                return GetBestHintResult(
                    hint=hint.text or "",
                    hint_id=hint.id,
                )

    return None


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
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await get_best_hint(
            kai_ctx,
            ruleset_name,
            violation_name,
        )


class SuccessRateMetric(BaseModel):
    violation_id: ViolationID

    counted_solutions: int = 0

    accepted_solutions: int = 0
    accepted_incidents: list[int] = Field(default_factory=list)

    rejected_solutions: int = 0
    rejected_incidents: list[int] = Field(default_factory=list)

    modified_solutions: int = 0
    modified_incidents: list[int] = Field(default_factory=list)

    pending_solutions: int = 0
    pending_incidents: list[int] = Field(default_factory=list)

    unknown_solutions: int = 0
    unknown_incidents: list[int] = Field(default_factory=list)


async def get_success_rate(
    kai_ctx: KaiSolutionServerContext,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
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

        violations_stmt = select(DBViolation).where(violations_where)
        violations = (await session.execute(violations_stmt)).scalars().all()

        for violation in violations:
            metric = SuccessRateMetric(
                violation_id=ViolationID(
                    ruleset_name=violation.ruleset_name,
                    violation_name=violation.violation_name,
                ),
            )

            for incident in violation.incidents:
                if incident.solution is None:
                    continue

                # FIXME: This should be automatic, but its not
                incident.solution.update_solution_status()

                # TODO: Make this cleaner
                metric.counted_solutions += 1

                if incident.solution.solution_status == SolutionStatus.ACCEPTED:
                    metric.accepted_solutions += 1
                    metric.accepted_incidents.append(incident.id)

                elif incident.solution.solution_status == SolutionStatus.REJECTED:
                    metric.rejected_solutions += 1
                    metric.rejected_incidents.append(incident.id)

                elif incident.solution.solution_status == SolutionStatus.MODIFIED:
                    metric.modified_solutions += 1
                    metric.modified_incidents.append(incident.id)

                elif incident.solution.solution_status == SolutionStatus.PENDING:
                    metric.pending_solutions += 1
                    metric.pending_incidents.append(incident.id)

                elif incident.solution.solution_status == SolutionStatus.UNKNOWN:
                    metric.unknown_solutions += 1
                    metric.unknown_incidents.append(incident.id)

            result.append(metric)

    return result


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
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await get_success_rate(
            kai_ctx,
            violation_ids,
        )


async def accept_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(DBSolution.client_id == client_id)
        solutions = (await session.execute(solutions_stmt)).scalars().all()

        # Files to add or remove from the solution
        files_to_update: set[tuple[DBSolution, DBFile]] = set()

        for solution in solutions:
            for file in solution.after:
                if file.uri != solution_file.uri:
                    continue

                if file.content == solution_file.content:
                    file.status = SolutionStatus.ACCEPTED
                    continue

                files_to_update.add((solution, file))

        if len(files_to_update) != 0:
            log(
                f"Updating {len(files_to_update)} files for client {client_id} with URI {solution_file.uri}",
            )
            new_file = DBFile(
                client_id=client_id,
                uri=solution_file.uri,
                content=solution_file.content,
                status=SolutionStatus.MODIFIED,
                solution_before=set(),
                solution_after=set(),
            )
            session.add(new_file)
            for solution, old_file in files_to_update:
                # Remove the old file from the solution
                solution.after.remove(old_file)
                solution.after.add(new_file)

                session.add(new_file)
                session.add(solution)

        await session.flush()

        all_solutions_accepted_or_modified = True
        for solution in solutions:
            # FIXME: There is some extreme weirdness going on here. The data in the
            # database does not update when the object updates, so we have to invalidate
            # it and refresh it. Also, sometimes the solution status is not updated
            # automatically?
            session.expire(solution)
            await session.refresh(solution)
            solution.update_solution_status()
            session.add(solution)
            await session.flush()

            print(
                f"Solution {solution.id} status: {solution.solution_status}",
                file=sys.stderr,
            )

            if not (
                solution.solution_status == SolutionStatus.ACCEPTED
                or solution.solution_status == SolutionStatus.MODIFIED
            ):
                all_solutions_accepted_or_modified = False
                break

        await session.commit()

    if all_solutions_accepted_or_modified:
        asyncio.create_task(generate_hint_v3(kai_ctx, client_id))  # type: ignore[unused-awaitable, unused-ignore]


@mcp.tool(name="accept_file")
async def tool_accept_file(
    ctx: Context,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await accept_file(
            kai_ctx,
            client_id,
            solution_file,
        )


async def reject_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    file_uri: str,
) -> None:
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(DBSolution.client_id == client_id)
        solutions = (await session.execute(solutions_stmt)).scalars().all()

        for solution in solutions:
            for file in solution.after:
                if file.uri != file_uri:
                    continue

                file.status = SolutionStatus.REJECTED

        await session.commit()


@mcp.tool(name="reject_file")
async def tool_reject_file(
    ctx: Context,
    client_id: str,
    file_uri: str,
) -> None:
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.lock:
        return await reject_file(
            kai_ctx,
            client_id,
            file_uri,
        )

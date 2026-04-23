import asyncio
import sys
from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import IntegrityError

from kai_mcp_solution_server.analyzer_types import ExtendedIncident
from kai_mcp_solution_server.ast_diff.parser import Language, extract_ast_info
from kai_mcp_solution_server.constants import log
from kai_mcp_solution_server.db.dao import (
    DBCollection,
    DBFile,
    DBHint,
    DBIncident,
    DBSolution,
    DBViolation,
)
from kai_mcp_solution_server.db.python_objects import (
    SolutionFile,
    SolutionStatus,
    ViolationID,
    associate_files,
    get_diff,
)
from kai_mcp_solution_server.resources import KaiSolutionServerContext, with_db_recovery


class CreateIncidentResult(BaseModel):
    incident_id: int
    solution_id: int


class GetBestHintResult(BaseModel):
    hint: str
    hint_id: int


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


@with_db_recovery
async def create_incident(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    extended_incident: ExtendedIncident,
) -> int:
    # Retry with exponential backoff if we hit a duplicate violation race condition
    max_attempts = 3
    base_delay = 0.05  # 50ms base delay

    assert kai_ctx.session_maker is not None
    for attempt in range(max_attempts):
        try:
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
                await session.flush()

                return incident.id

        except IntegrityError as e:
            error_msg = str(e)
            if "kai_violations_pkey" in error_msg and attempt < max_attempts - 1:
                # Exponential backoff: 50ms, 100ms, 200ms
                delay = base_delay * (2**attempt)
                log(
                    f"Duplicate violation creation detected for {extended_incident.ruleset_name} - "
                    f"{extended_incident.violation_name}, retrying in {delay:.0f}ms (attempt {attempt + 1}/{max_attempts})..."
                )
                await asyncio.sleep(delay)
                continue
            else:
                raise

    raise RuntimeError("Failed to create incident after retries")


@with_db_recovery
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

    assert kai_ctx.session_maker is not None
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
            next_after = DBFile(
                client_id=client_id,
                uri=file.uri,
                content=file.content,
                status=SolutionStatus.PENDING,
                solution_before=set(),
                solution_after=set(),
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

    return solution.id


@with_db_recovery
async def generate_hint_v1(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    assert kai_ctx.session_maker is not None
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

            prompt += f"Solution:\n{diff}\n\n"

            log(f"Generating hint for client {client_id} with prompt:\n{prompt}")

            if kai_ctx.model is None:
                raise RuntimeError("Model not initialized")
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


@with_db_recovery
async def generate_hint_v2(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    # print(f"Generating hint for client {client_id}", file=sys.stderr)

    assert kai_ctx.session_maker is not None
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

            if kai_ctx.model is None:
                raise RuntimeError("Model not initialized")
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


@with_db_recovery
async def generate_hint_v3(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
) -> None:
    """
    Generate hints for accepted solutions using improved prompt format with better structure.
    """

    assert kai_ctx.session_maker is not None
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

            if kai_ctx.model is None:
                raise RuntimeError("Model not initialized")
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


@with_db_recovery
async def delete_solution(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_id: int,
) -> bool:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBSolution, solution_id)
        if sln is None:
            return False
        await session.delete(sln)
    return True


@with_db_recovery
async def get_best_hint(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str,
    violation_name: str,
) -> GetBestHintResult | None:
    assert kai_ctx.session_maker is not None
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


@with_db_recovery
async def get_success_rate(
    kai_ctx: KaiSolutionServerContext,
    violation_ids: list[ViolationID],
) -> list[SuccessRateMetric] | None:
    result: list[SuccessRateMetric] = []

    if len(violation_ids) == 0:
        return result

    assert kai_ctx.session_maker is not None
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


@with_db_recovery
async def accept_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    solution_file: SolutionFile,
) -> None:
    assert kai_ctx.session_maker is not None
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

    if all_solutions_accepted_or_modified:
        asyncio.create_task(generate_hint_v3(kai_ctx, client_id))  # type: ignore[unused-awaitable, unused-ignore]


@with_db_recovery
async def reject_file(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    file_uri: str,
) -> None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        solutions_stmt = select(DBSolution).where(DBSolution.client_id == client_id)
        solutions = (await session.execute(solutions_stmt)).scalars().all()

        for solution in solutions:
            for file in solution.after:
                if file.uri != file_uri:
                    continue

                file.status = SolutionStatus.REJECTED


# --- Query functions for REST API ---


@with_db_recovery
async def list_violations(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = 0,
    limit: int = 50,
) -> tuple[list[DBViolation], int]:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        stmt = select(DBViolation)
        count_stmt = select(func.count()).select_from(DBViolation)

        if ruleset_name is not None:
            stmt = stmt.where(DBViolation.ruleset_name == ruleset_name)
            count_stmt = count_stmt.where(DBViolation.ruleset_name == ruleset_name)
        if violation_name is not None:
            stmt = stmt.where(DBViolation.violation_name == violation_name)
            count_stmt = count_stmt.where(DBViolation.violation_name == violation_name)

        total = (await session.execute(count_stmt)).scalar() or 0
        violations = (
            (await session.execute(stmt.offset(offset).limit(limit))).scalars().all()
        )
        return list(violations), total


@with_db_recovery
async def get_violation(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str,
    violation_name: str,
) -> DBViolation | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        stmt = select(DBViolation).where(
            DBViolation.ruleset_name == ruleset_name,
            DBViolation.violation_name == violation_name,
        )
        return (await session.execute(stmt)).scalar_one_or_none()


@with_db_recovery
async def list_incidents(
    kai_ctx: KaiSolutionServerContext,
    client_id: str | None = None,
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = 0,
    limit: int = 50,
) -> tuple[list[DBIncident], int]:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        stmt = select(DBIncident)
        count_stmt = select(func.count()).select_from(DBIncident)

        if client_id is not None:
            stmt = stmt.where(DBIncident.client_id == client_id)
            count_stmt = count_stmt.where(DBIncident.client_id == client_id)
        if ruleset_name is not None:
            stmt = stmt.where(DBIncident.ruleset_name == ruleset_name)
            count_stmt = count_stmt.where(DBIncident.ruleset_name == ruleset_name)
        if violation_name is not None:
            stmt = stmt.where(DBIncident.violation_name == violation_name)
            count_stmt = count_stmt.where(DBIncident.violation_name == violation_name)

        total = (await session.execute(count_stmt)).scalar() or 0
        incidents = (
            (await session.execute(stmt.offset(offset).limit(limit))).scalars().all()
        )
        return list(incidents), total


@with_db_recovery
async def get_incident(
    kai_ctx: KaiSolutionServerContext,
    incident_id: int,
) -> DBIncident | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        return await session.get(DBIncident, incident_id)


@with_db_recovery
async def list_solutions(
    kai_ctx: KaiSolutionServerContext,
    client_id: str | None = None,
    status: SolutionStatus | None = None,
    offset: int = 0,
    limit: int = 50,
) -> tuple[list[DBSolution], int]:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        stmt = select(DBSolution)
        count_stmt = select(func.count()).select_from(DBSolution)

        if client_id is not None:
            stmt = stmt.where(DBSolution.client_id == client_id)
            count_stmt = count_stmt.where(DBSolution.client_id == client_id)
        if status is not None:
            stmt = stmt.where(DBSolution.solution_status == status)
            count_stmt = count_stmt.where(DBSolution.solution_status == status)

        total = (await session.execute(count_stmt)).scalar() or 0
        solutions = (
            (
                await session.execute(
                    stmt.order_by(DBSolution.created_at.desc())
                    .offset(offset)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )
        return list(solutions), total


@with_db_recovery
async def get_solution(
    kai_ctx: KaiSolutionServerContext,
    solution_id: int,
) -> DBSolution | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        return await session.get(DBSolution, solution_id)


@with_db_recovery
async def list_hints(
    kai_ctx: KaiSolutionServerContext,
    ruleset_name: str | None = None,
    violation_name: str | None = None,
    offset: int = 0,
    limit: int = 50,
) -> tuple[list[DBHint], int]:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        stmt = select(DBHint)
        count_stmt = select(func.count()).select_from(DBHint)

        if ruleset_name is not None and violation_name is not None:
            stmt = stmt.join(DBHint.violations).where(
                DBViolation.ruleset_name == ruleset_name,
                DBViolation.violation_name == violation_name,
            )
            count_stmt = count_stmt.join(DBHint.violations).where(
                DBViolation.ruleset_name == ruleset_name,
                DBViolation.violation_name == violation_name,
            )

        total = (await session.execute(count_stmt)).scalar() or 0
        hints = (
            (
                await session.execute(
                    stmt.order_by(DBHint.created_at.desc()).offset(offset).limit(limit)
                )
            )
            .scalars()
            .all()
        )
        return list(hints), total


@with_db_recovery
async def get_hint(
    kai_ctx: KaiSolutionServerContext,
    hint_id: int,
) -> DBHint | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        return await session.get(DBHint, hint_id)


# --- Collection operations ---


@with_db_recovery
async def create_collection(
    kai_ctx: KaiSolutionServerContext,
    name: str,
    description: str | None = None,
    source_repo: str | None = None,
    migration_type: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> int:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        collection = DBCollection(
            name=name,
            description=description,
            source_repo=source_repo,
            migration_type=migration_type,
            metadata_=metadata or {},
        )
        session.add(collection)
        await session.flush()
        return collection.id


@with_db_recovery
async def list_collections(
    kai_ctx: KaiSolutionServerContext,
    offset: int = 0,
    limit: int = 50,
) -> tuple[list[DBCollection], int]:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        count_stmt = select(func.count()).select_from(DBCollection)
        total = (await session.execute(count_stmt)).scalar() or 0
        stmt = (
            select(DBCollection)
            .order_by(DBCollection.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        collections = (await session.execute(stmt)).scalars().all()
        return list(collections), total


@with_db_recovery
async def get_collection(
    kai_ctx: KaiSolutionServerContext,
    collection_id: int,
) -> DBCollection | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        return await session.get(DBCollection, collection_id)


@with_db_recovery
async def update_collection(
    kai_ctx: KaiSolutionServerContext,
    collection_id: int,
    description: str | None = None,
    source_repo: str | None = None,
    migration_type: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> DBCollection | None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        collection = await session.get(DBCollection, collection_id)
        if collection is None:
            return None
        if description is not None:
            collection.description = description
        if source_repo is not None:
            collection.source_repo = source_repo
        if migration_type is not None:
            collection.migration_type = migration_type
        if metadata is not None:
            collection.metadata_ = metadata
        return collection


@with_db_recovery
async def delete_collection(
    kai_ctx: KaiSolutionServerContext,
    collection_id: int,
) -> bool:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        collection = await session.get(DBCollection, collection_id)
        if collection is None:
            return False
        await session.delete(collection)
    return True


@with_db_recovery
async def add_to_collection(
    kai_ctx: KaiSolutionServerContext,
    collection_id: int,
    solution_ids: list[int] | None = None,
    incident_ids: list[int] | None = None,
) -> None:
    assert kai_ctx.session_maker is not None
    async with kai_ctx.session_maker.begin() as session:
        collection = await session.get(DBCollection, collection_id)
        if collection is None:
            raise ValueError(f"Collection {collection_id} not found")

        if solution_ids:
            sol_stmt = select(DBSolution).where(DBSolution.id.in_(solution_ids))
            solutions = (await session.execute(sol_stmt)).scalars().all()
            collection.solutions.update(solutions)

        if incident_ids:
            inc_stmt = select(DBIncident).where(DBIncident.id.in_(incident_ids))
            incidents = (await session.execute(inc_stmt)).scalars().all()
            collection.incidents.update(incidents)


# --- Bulk operations ---


@with_db_recovery
async def ingest_commit(
    kai_ctx: KaiSolutionServerContext,
    client_id: str,
    incidents: list[ExtendedIncident],
    before_files: list[SolutionFile],
    after_files: list[SolutionFile],
    reasoning: str | None = None,
    collection_id: int | None = None,
) -> tuple[list[int], int, int | None]:
    """Atomically ingest a commit's incidents + solution + optionally add to collection.

    Returns (incident_ids, solution_id, collection_id).
    """
    # Create all incidents first
    incident_ids: list[int] = []
    for ei in incidents:
        iid = await create_incident(kai_ctx, client_id, ei)
        incident_ids.append(iid)

    # Create the solution linking them
    solution_id = await create_solution(
        kai_ctx,
        client_id,
        incident_ids,
        before_files,
        after_files,
        reasoning=reasoning,
    )

    # Add to collection if specified
    if collection_id is not None:
        await add_to_collection(
            kai_ctx,
            collection_id,
            solution_ids=[solution_id],
            incident_ids=incident_ids,
        )

    return incident_ids, solution_id, collection_id

import asyncio
import difflib
import os
import sys
from asyncio import sleep
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

from analyzer_types import Category, ExtendedIncident
from dao import DBKaiSolution, SolutionStatus, get_async_engine
from fastmcp import Context, FastMCP
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy import Text
from sqlalchemy import cast as sacast
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class SolutionServerSettings(BaseSettings):
    pg_dsn: str = cast(
        str, "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres"
    )
    # llm_params: dict[str, Any] = {
    #     "model": "gpt-4o-mini",
    #     "model_provider": "openai",
    #     "openai_api_key": os.getenv("OPENAI_API_KEY"),
    # }


class KaiSolutionServerContext:
    def __init__(self, settings: SolutionServerSettings) -> None:
        self.settings = settings

    async def create(self) -> None:
        self.engine = await get_async_engine(self.settings.pg_dsn)
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


@asynccontextmanager
async def kai_solution_server_lifespan(
    server: FastMCP,
) -> AsyncIterator[KaiSolutionServerContext]:
    print("kai_solution_server_lifespan", file=sys.stderr)
    try:
        print("getting settings", file=sys.stderr)
        settings = SolutionServerSettings()
        print("creating context", file=sys.stderr)
        ctx = KaiSolutionServerContext(settings)
        await ctx.create()
        print("yielding context", file=sys.stderr)
        yield ctx
    except Exception as e:
        print(f"Error in lifespan: {e}", file=sys.stderr)
        raise e
    finally:
        pass


mcp: FastMCP = FastMCP(
    "KaiSolutionServer", lifespan=kai_solution_server_lifespan, dependencies=[]
)


@mcp.tool()
async def request_llm(
    ctx: Context, text: str
) -> dict:  # TODO: Use a more specific type
    prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral. Just output a single word - 'positive', 'negative', or 'neutral'. Text to analyze: {text}"

    response = await ctx.sample(prompt)

    sentiment = response.text.strip().lower()

    if "positive" in sentiment:
        sentiment = "positive"
    elif "negative" in sentiment:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"text": text, "sentiment": sentiment}


@mcp.tool()
async def create_solution(
    ctx: Context,
    before_filename: str = "before.txt",
    before_text: str = "before text",
    after_filename: str = "after.txt",
    after_text: str = "after text",
    extended_incident: ExtendedIncident = ExtendedIncident(
        ruleset_name="example_ruleset",
        violation_name="example_violation",
        uri="example_uri",
        message="example_message",
    ),
    status: SolutionStatus = SolutionStatus.UNKNOWN,
    hint: str | None = None,
) -> int:
    """
    Add the given data to the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        # Assuming you have a function to add data to the database
        # add_data_to_db(session, data)
        sln = DBKaiSolution(
            before_filename=before_filename,
            before_text=before_text,
            after_filename=after_filename,
            after_text=after_text,
            extended_incident=extended_incident.model_dump(),
            status=status,
            hint=hint,
        )
        session.add(sln)
        await session.commit()

    async def add_hint():
        print("Getting sample...", file=sys.stderr)

        diff = "".join(
            difflib.context_diff(
                before_text.splitlines(keepends=True),
                after_text.splitlines(keepends=True),
                fromfile=before_filename,
                tofile=after_filename,
            )
        )

        hint = await ctx.sample(
            "The following incident was solved by the following diff. "
            "Describe the changes required in a step-by-step manner so similar situations "
            f"can be solved in the future:\n\nIncident\n{extended_incident.model_dump_json()}\n\n"
            f"diff\n```\n{diff}\n```\n\n"
        )

        async with kai_ctx.session_maker.begin() as session:
            print("Adding hint to the database...", file=sys.stderr)
            sln.hint = hint.text.strip()
            print("session.add(sln)", file=sys.stderr)
            session.add(sln)
            print("await session.commit()", file=sys.stderr)
            await session.commit()
        print("Hint added to the database.", file=sys.stderr)

    asyncio.create_task(add_hint())

    return sln.id


@mcp.tool()
async def delete_solution(
    ctx: Context,
    solution_id: int,
) -> bool:
    """
    Delete the solution with the given ID from the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBKaiSolution, solution_id)
        if sln is None:
            return False
        await session.delete(sln)
        await session.commit()
    return True


@mcp.tool()
async def update_solution_status(
    ctx: Context,
    solution_id: int,
    status: str = "accepted",
) -> bool:
    """
    Update the status of the solution with the given ID in the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        sln = await session.get(DBKaiSolution, solution_id)
        if sln is None:
            return False
        sln.status = status
        await session.commit()
    return True


@mcp.tool()
async def get_success_rate(
    ctx: Context,
    extended_incident: ExtendedIncident,
) -> float:
    """
    Get the success rate of the given incident in the database.
    """
    kai_ctx = cast(KaiSolutionServerContext, ctx.request_context.lifespan_context)
    async with kai_ctx.session_maker.begin() as session:
        solutions_result = await session.execute(select(DBKaiSolution))
        solutions = list(solutions_result)

        print(f"Solutions: {solutions}", file=sys.stderr)

        if not solutions:
            return -1.0

        accepted_count = sum(
            1 for solution in solutions if solution[0].status == SolutionStatus.ACCEPTED
        )
        proportion = accepted_count / len(solutions)
        return proportion


if __name__ == "__main__":
    mcp.run()

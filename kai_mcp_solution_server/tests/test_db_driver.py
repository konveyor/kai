from kai_mcp_solution_server.resources import KaiSolutionServerContext
from kai_mcp_solution_server.settings import SolutionServerSettings


async def main() -> None:
    settings = SolutionServerSettings()
    ctx = KaiSolutionServerContext(settings)
    await ctx.create()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

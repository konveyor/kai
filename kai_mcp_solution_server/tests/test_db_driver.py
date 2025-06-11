from kai_mcp_solution_server.server import (
    KaiSolutionServerContext,
    SolutionServerSettings,
)


async def main() -> None:
    settings = SolutionServerSettings()
    ctx = KaiSolutionServerContext(settings)
    await ctx.create()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

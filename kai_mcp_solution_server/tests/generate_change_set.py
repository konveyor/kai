import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Coroutine, TypeVar

from kai_mcp_solution_server.dao import SolutionChangeSet, SolutionFile
from kai_mcp_solution_server.server import (
    KaiSolutionServerContext,
    SolutionServerSettings,
)

T = TypeVar("T")


# https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues
def run_coroutine_sync(coroutine: Coroutine[Any, Any, T], timeout: float = 30) -> T:
    def run_in_new_loop():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coroutine)
        finally:
            new_loop.close()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)

    if threading.current_thread() is threading.main_thread():
        if not loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            with ThreadPoolExecutor() as pool:
                future = pool.submit(run_in_new_loop)
                return future.result(timeout=timeout)
    else:
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()


async def main() -> None:
    s = SolutionChangeSet(
        diff="diff --git a/file.txt b/file.txt\nindex 83db48f..f735c8d 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-Hello World\n+Hello Universe\n",
        before=[
            SolutionFile(
                uri="file://file.txt",
                content="Hello World",
            )
        ],
        after=[
            SolutionFile(
                uri="file://file.txt",
                content="Hello Universe",
            )
        ],
    )

    print(s.model_dump_json(indent=2))

    settings = SolutionServerSettings()
    ctx = KaiSolutionServerContext(settings)
    await ctx.create()

    print(settings.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())

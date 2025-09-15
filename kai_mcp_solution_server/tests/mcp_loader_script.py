import asyncio
import json
import os
import ssl
import sys
import traceback
from asyncio.log import logger
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, AsyncIterator

import yaml
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console

from .ssl_utils import apply_ssl_bypass

# Import httpx for direct inspection
try:
    import httpx
except ImportError:
    httpx = None  # type:ignore[assignment]


console = Console(file=sys.stderr)
logger.setLevel("DEBUG")  # Set logger to debug level for detailed output


class MCPClientArgs(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    host: str | None = None
    port: int | None = None
    transport: str | None = None
    server_path: str | None = None
    mount_path: str | None = None
    full_output: bool = False
    verbose: bool = False
    insecure: bool = False


@asynccontextmanager
async def create_http_client(args: MCPClientArgs) -> AsyncIterator[ClientSession]:
    if args.host is None:
        raise ValueError("Host must be specified for HTTP transport")

    # Setup HTTP transport using streamable-http
    transport = ""
    if not args.host.startswith("http"):
        transport = "http://"
    server_url = f"{transport}{args.host}:{args.port}{args.mount_path}"
    print(f"Connecting to server at {server_url}...")
    logger.debug(f"Initializing streamable-http transport with URL: {server_url}")

    try:
        async with AsyncExitStack() as stack:
            if args.insecure:
                stack.enter_context(apply_ssl_bypass())

            read, write, get_session_id = await stack.enter_async_context(
                streamablehttp_client(server_url)
            )
            logger.debug("Streamable HTTP client connection established")
            # Note: get_session_id is for session management, not passed to ClientSession
            session = await stack.enter_async_context(ClientSession(read, write))
            logger.debug("MCP ClientSession initialized")

            yield session

    except Exception as e:
        logger.error("HTTP transport error: %s", str(e), exc_info=True)
        print(f"x Error with HTTP transport: {traceback.format_exc()}")

        # Add specific advice for SSL certificate errors
        if (
            isinstance(e, ssl.SSLError)
            or "ssl" in str(e).lower()
            or "certificate" in str(e).lower()
        ):
            print("! SSL certificate verification error. Try these options:")
            print(
                "   1. Use the --insecure flag to bypass SSL verification (not recommended for production)"
            )
            print("   2. Use a valid SSL certificate on the server")
            print("   3. Add the server's certificate to your trusted CA store")

        print(f"! Make sure the server is running at {server_url}")
        raise  # Re-raise the exception so the test fails properly


@asynccontextmanager
async def create_stdio_client(args: MCPClientArgs) -> AsyncIterator[ClientSession]:
    print(f"Using server path: {args.server_path}")
    logger.debug(f"Initializing STDIO transport with server path: {args.server_path}")

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "kai_mcp_solution_server", "--transport", "stdio"],
        cwd=str(args.server_path),
        env=os.environ.copy(),
    )
    logger.debug("STDIO server parameters: %s", server_params)

    try:
        async with AsyncExitStack() as stack:
            read, write = await stack.enter_async_context(stdio_client(server_params))
            logger.debug("STDIO client connection established")

            session = await stack.enter_async_context(ClientSession(read, write))
            logger.debug("MCP ClientSession initialized")

            yield session

    except Exception as e:
        logger.error("STDIO transport error: %s", str(e), exc_info=True)
        print(f"x Error with STDIO transport: {e}")
        print(f"! Make sure the server script exists: {args.server_path}")

        raise Exception("Error encountered during MCP STDIO session") from e


@asynccontextmanager
async def create_client(args: MCPClientArgs) -> AsyncIterator[ClientSession]:
    if args.insecure and args.transport == "http":
        print("SSL verification: Disabled (insecure mode)")

    if args.transport == "http":
        async with create_http_client(args) as session:
            yield session

    elif args.transport == "stdio":
        async with create_stdio_client(args) as session:
            yield session

    else:
        raise ValueError(
            f"Unsupported transport type: {args.transport}. Use 'http' or 'stdio'."
        )


async def interact_with_server(session: ClientSession) -> None:
    await session.initialize()
    console.print("MCP Client initialized successfully")

    tools = await session.list_tools()
    print_result = [
        {
            "name": tool.name,
            # "inputSchema": tool.inputSchema if tool.inputSchema else "No schema defined",
        }
        for tool in tools.tools
    ]
    console.print("Available tools:")
    console.print(yaml.dump(print_result))

    console.print("Enter actions as:")
    console.print("  - `<name> <args as JSON>`")
    console.print("  - `<name> <filepath to JSON file>`")
    console.print("  - <filepath to JSON file> (sequential tool call)")
    console.print("Type 'exit' to quit")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == "exit":
                break

            parts = user_input.split(maxsplit=1)
            if len(parts) > 2 or len(parts) < 1:
                console.print("Invalid input format.")
                continue

            name = parts[0]
            try:
                with open(name, "r") as f:
                    # If the first part is a file path, read the content
                    content = f.read()
                    sequence: list[dict[str, Any]] = json.loads(content)

                for item in sequence:
                    args_str = str(item["args"])
                    if len(args_str) > 100:
                        args_str = args_str[:100] + "..."
                    console.log("Calling tool:")
                    console.log(f"  name: {item['name']}")
                    console.log(f"  args: {args_str}")
                    result = await session.call_tool(item["name"], item["args"])
                    console.log(f"Result: {result.model_dump()}")
                    input("Press Enter to continue to the next tool call...")

            except FileNotFoundError:
                try:
                    # if that fails, try to parse 2nd arg as a JSON object
                    arguments = json.loads(parts[1].strip())
                except json.JSONDecodeError:
                    try:
                        # if that fails, treat it as a file path
                        file_path = parts[1].strip()
                        with open(file_path, "r") as f:
                            arguments = json.load(f)
                    except Exception as e:
                        console.print(f"Error reading arguments: {e}")
                        continue

                result = await session.call_tool(name, arguments)
                console.print(result.model_dump())

        except Exception as e:
            logger.error("Error during tool call: %s", str(e), exc_info=True)


async def main() -> None:
    args = MCPClientArgs()

    try:
        async with create_client(args) as session:
            await interact_with_server(session)

    except Exception as e:
        logger.error("Error in main client loop: %s", str(e), exc_info=True)
        print(f"x Error: {e}")
        print("! Make sure the server is running and accessible")


if __name__ == "__main__":
    asyncio.run(main())

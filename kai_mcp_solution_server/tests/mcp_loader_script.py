import asyncio
import json
import os
import ssl
import warnings
from asyncio.log import logger
from contextlib import AsyncExitStack, asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Iterator

from httpx import AsyncClient, Client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console

# Import httpx for direct inspection
try:
    import httpx
except ImportError:
    httpx = None  # type:ignore[assignment]


console = Console()
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


@contextmanager
def disable_ssl_certificate_verification() -> Iterator[None]:
    original_ssl_create_default_context = ssl.create_default_context

    logger.debug("Disabling SSL certificate verification by patching SSL module")
    # Disable SSL verification warnings
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    warnings.filterwarnings("ignore", category=Warning)

    # Patch SSL module's default context creator to disable verification
    def unverified_context(*args: Any, **kwargs: Any) -> ssl.SSLContext:
        context = original_ssl_create_default_context(*args, **kwargs)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    # Apply the patch
    ssl.create_default_context = unverified_context
    logger.debug("Successfully patched ssl.create_default_context")

    # For httpx - try to patch its SSL defaults too if available
    if httpx:
        try:
            # Try to patch httpx client classes
            old_client_init = httpx.Client.__init__

            def patched_client_init(self: Client, *args: Any, **kwargs: Any) -> None:
                kwargs["verify"] = False
                old_client_init(self, *args, **kwargs)

            httpx.Client.__init__ = patched_client_init  # type:ignore[method-assign]

            # Same for AsyncClient
            old_async_client_init = httpx.AsyncClient.__init__

            def patched_async_client_init(
                self: AsyncClient, *args: Any, **kwargs: Any
            ) -> None:
                kwargs["verify"] = False
                old_async_client_init(self, *args, **kwargs)

            httpx.AsyncClient.__init__ = (
                patched_async_client_init
            )  # type:ignore[method-assign]
            logger.debug("Patched httpx Client classes")

        except Exception as patch_err:
            logger.warning("Failed to patch httpx: %s", patch_err)

    # Also set environment variables as backup
    os.environ["SSL_CERT_VERIFY"] = "false"
    os.environ["HTTPX_SSL_VERIFY"] = "false"
    os.environ["HTTPX_NO_VERIFY"] = "true"
    os.environ["PYTHONHTTPSVERIFY"] = "0"

    print("⚠️ Warning: SSL certificate verification is disabled")

    yield

    # Restore original SSL context creator
    ssl.create_default_context = original_ssl_create_default_context
    logger.debug("Restored original ssl.create_default_context")

    # Restore httpx patches if applied
    if httpx:
        try:
            if "old_client_init" in locals() and hasattr(httpx, "Client"):
                httpx.Client.__init__ = old_client_init  # type:ignore[method-assign]
                logger.debug("Restored original httpx.Client.__init__")

            if "old_async_client_init" in locals() and hasattr(httpx, "AsyncClient"):
                httpx.AsyncClient.__init__ = (
                    old_async_client_init
                )  # type:ignore[method-assign]
                logger.debug("Restored original httpx.AsyncClient.__init__")
        except Exception as restore_err:
            logger.warning("Failed to restore httpx patches: %s", restore_err)

    # Clean up environment variables
    ssl_env_vars = [
        "SSL_CERT_VERIFY",
        "HTTPX_SSL_VERIFY",
        "HTTPX_NO_VERIFY",
        "PYTHONHTTPSVERIFY",
    ]

    for env_var in ssl_env_vars:
        if env_var in os.environ:
            del os.environ[env_var]

    logger.debug("Cleaned up all SSL verification settings")


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
                stack.enter_context(disable_ssl_certificate_verification())

            read, write, get_session_id = await stack.enter_async_context(
                streamablehttp_client(server_url, insecure=args.insecure)
            )
            logger.debug("Streamable HTTP client connection established")
            session = await stack.enter_async_context(
                ClientSession(read, write, get_session_id)
            )
            logger.debug("MCP ClientSession initialized")

            yield session

    except Exception as e:
        logger.error("HTTP transport error: %s", str(e), exc_info=True)
        print(f"x Error with HTTP transport: {e}")
        print(f"! Make sure the server is running at {server_url}")

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

        print("! Try using the STDIO transport instead with --transport stdio")


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

    console.print("Enter actions as <name> <args as JSON or file path>")
    console.print("Type 'exit' to quit")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == "exit":
                break

            parts = user_input.split(maxsplit=1)
            if len(parts) != 2:
                console.print("Invalid input format. Use '<name> <args>'")
                continue

            name = parts[0]
            try:
                # try to parse as a JSON object
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

import argparse
from typing import Any

from kai_mcp_solution_server.server import mcp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the KAI MCP Solution Server",
    )
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to run the server on (default: nothing)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to run the server on (default: nothing)",
    )

    parser.add_argument(
        "--mount-path",
        type=str,
        default="/sse",
        help="Path the MCP server is mounted behind (ie, /hub/services/kai)",
    )

    args = parser.parse_args()

    kwargs: dict[str, Any] = {"transport": args.transport}
    if args.transport != "stdio":
        kwargs["port"] = args.port
        kwargs["host"] = args.host
        kwargs["path"] = args.mount_path

    mcp.run(**kwargs)

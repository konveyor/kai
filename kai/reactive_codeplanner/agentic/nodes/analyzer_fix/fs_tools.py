import os
from functools import partial
from pathlib import Path
from typing import Annotated, Optional

from langchain_core.tools import BaseTool, Tool, tool

from kai.logging.logging import get_logger

logger = get_logger(__name__)


def list_files(base_dir: Path) -> BaseTool:
    def _list_files(
        base_dir: Path,
        extensions: Annotated[
            Optional[list[str]], "Optional list of file extensions to filter by"
        ],
    ) -> str:
        filtered_files: list[str] = []
        for root, _, files in os.walk(base_dir):
            for file in files:
                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    filtered_files.append(os.path.join(root, file))
        return "\n".join(filtered_files)

    return Tool.from_function(
        name="list_files",
        func=partial(_list_files, base_dir),
        description="Lists files, optionally filters by file extensions",
    )


@tool
def read_file(
    path: Annotated[Path, "Full path to the file to read"],
) -> str:
    """Reads a file at given path"""
    try:
        return path.read_text()
    except Exception as e:
        logger.error("Failed to read file %s - %s", path, e)
        return "Could not read file..."


@tool
def write_to_file(
    path: Annotated[Path, "Full path to the file to write"],
    content: Annotated[str, "Content to write"],
) -> str:
    """Writes content to file at given path. Creates a new file if one doesn't exist."""
    try:
        if not path.exists():
            path.touch()
        path.write_text(content)
        return "Successfully wrote to file"
    except Exception as e:
        logger.error("Failed to write to file %s", f"{path} - {e}")
        return "Failed to write to file"

import os
import unittest
from pathlib import Path

from langchain_core.tools import render_text_description

from kai.reactive_codeplanner.agentic.nodes.analyzer_fix.fs_tools import (
    list_files,
    read_file,
    write_to_file,
)


class TestFsTools(unittest.TestCase):
    def setUp(self):
        self.project_base_path = Path(
            ".", "tests", "test_data", "test_analysis_agent"
        ).absolute()
        return super().setUp()

    def tearDown(self):
        os.remove(self.temp_file_one)
        return super().tearDown()

    def test_fs_tools(self):
        self.assertEqual(
            render_text_description([write_to_file]),
            "write_to_file(path: Annotated[pathlib.Path, 'Full path to the file to write'], content: Annotated[str, 'Content to write']) -> str - Writes content to file at given path. Creates a new file if one doesn't exist.",
        )
        self.temp_file_one = self.project_base_path / "temp.properties"
        result = write_to_file.invoke(
            {"path": str(self.temp_file_one), "content": "test"}
        )
        self.assertEqual(result, "Successfully wrote to file")
        result = read_file.invoke({"path": str(self.temp_file_one)})
        self.assertEqual(result, "test")

        list_files_tool = list_files(self.project_base_path)
        self.assertEqual(
            render_text_description([list_files_tool]),
            "list_files(extensions: Annotated[Optional[list[str]], 'Optional list of file extensions to filter by']) -> str - Lists files, optionally filters by file extensions",
        )
        result = list_files_tool.invoke({"extensions": [".java"]})
        self.assertEqual(result, str(self.project_base_path / "test.java"))
        result = list_files_tool.invoke({"extensions": [".xml"]})
        self.assertEqual(result, str(self.project_base_path / "pom.xml"))

        self.assertEqual(
            render_text_description([read_file]),
            "read_file(path: Annotated[pathlib.Path, 'Full path to the file to read']) -> str - Reads a file at given path",
        )
        result = read_file.invoke({"path": str(self.project_base_path / "pom.xml")})
        self.assertEqual(result, "<xml>\n</xml>")

import shutil
import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from kai.analyzer_types import Category, Incident, RuleSet, Violation
from kai.cache import BadCacheError, JSONCacheWithTrace, TaskBasedPathResolver
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import AnalyzerRuleViolation
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    DependencyResolutionError,
    PackageDoesNotExistError,
)


class TestCache(unittest.TestCase):
    def setUp(self) -> None:
        self.cache_dir = tempfile.mkdtemp()
        self.trace_dir = tempfile.mkdtemp()

        self.t1 = AnalyzerRuleViolation(
            file="test/src/main/java/io/konveyor/main.java",
            depth=0,
            line=10,
            column=2,
            ruleset=RuleSet(description="test", name="test-rs"),
            violation=Violation(
                category=Category.MANDATORY,
                description="test",
                id="rule-id-000",
                incidents=[],
            ),
            message="Fix this",
            incident=Incident(
                message="test",
                uri="file://test/src/main/java/io/konveyor/main.java",
                code_snip="test",
                line_number=10,
            ),
        )
        self.t2 = PackageDoesNotExistError(
            file="file://test/pom.xml",
            line=10,
            column=2,
            message="package not found",
            parent=self.t1,
        )
        self.t3 = DependencyResolutionError(
            file="file://test/pom.xml",
            line=10,
            column=2,
            message="package not found",
            parent=self.t2,
        )

        self.t1_cache_expected_path = Path(
            "AnalyzerRuleViolation",
            "konveyor_main_java",
            "line_10",
            "0_analyzerfix.json",
        )
        self.t2_cache_expected_path = Path(
            "AnalyzerRuleViolation",
            "konveyor_main_java",
            "line_10",
            "PackageDoesNotExistError",
            "test_pom_xml",
            "line_10",
            "0_analyzerfix.json",
        )
        self.t3_cache_expected_path = Path(
            "AnalyzerRuleViolation",
            "konveyor_main_java",
            "line_10",
            "PackageDoesNotExistError",
            "test_pom_xml",
            "line_10",
            "DependencyResolutionError",
            "test_pom_xml",
            "line_10",
            "0_analyzerfix.json",
        )

        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(self.cache_dir)
        shutil.rmtree(self.trace_dir)
        return super().tearDown()

    def test_task_based_path_resolver(self) -> None:
        # level 1 dir
        path_resolver = TaskBasedPathResolver(
            task=self.t1, request_type="analyzerfix"
        )  # cspell: disable-line
        t1_cache_path = path_resolver.cache_path()
        self.assertEqual(t1_cache_path, self.t1_cache_expected_path)

        # nested level 2 dir
        path_resolver = TaskBasedPathResolver(task=self.t2, request_type="analyzerfix")
        t2_cache_path = path_resolver.cache_path()
        self.assertEqual(t2_cache_path, self.t2_cache_expected_path)
        self.assertEqual(
            t2_cache_path,
            t1_cache_path.parent
            / Path(
                "PackageDoesNotExistError",
                "test_pom_xml",
                "line_10",
                "0_analyzerfix.json",
            ),
        )

        # deeply nested level 3 dir
        path_resolver = TaskBasedPathResolver(task=self.t3, request_type="analyzerfix")
        t3_cache_path = path_resolver.cache_path()
        self.assertEqual(t3_cache_path, self.t3_cache_expected_path)
        self.assertEqual(
            t3_cache_path,
            t2_cache_path.parent
            / Path(
                "DependencyResolutionError",
                "test_pom_xml",
                "line_10",
                "0_analyzerfix.json",
            ),
        )

    def test_json_cache(self) -> None:
        cache = JSONCacheWithTrace(
            cache_dir=Path(self.cache_dir),
            model_id="dummy",
            trace_dir=Path(self.trace_dir),
            fail_on_cache_mismatch=True,
            enable_trace=True,
        )

        # test a simple put
        path_resolver = TaskBasedPathResolver(task=self.t1, request_type="analyzerfix")
        cache_path = path_resolver.cache_path()
        cache.put(
            input="test",
            output=AIMessage(content="hello from ai"),
            path=cache_path,
        )
        expected_cache_file = (
            Path(self.cache_dir) / "dummy" / self.t1_cache_expected_path
        )
        self.assertTrue(expected_cache_file.exists())

        # test a get
        cache_entry = cache.get(input="test", path=cache_path)
        self.assertIsNotNone(cache_entry)
        self.assertIsInstance(cache_entry, AIMessage)
        if cache_entry is not None:
            self.assertEqual(cache_entry.content, "hello from ai")
        # consistency test
        cache_entry = cache.get(input="test", path=cache_path)
        self.assertIsNotNone(cache_entry)
        self.assertIsInstance(cache_entry, AIMessage)
        if cache_entry is not None:
            self.assertEqual(cache_entry.content, "hello from ai")

        # test an exception is raised when input mismatch for the same resolver
        with self.assertRaises(BadCacheError):
            cache.get(input="test_bad_input", path=cache_path)

        # test that a trace file is generated
        path_resolver = TaskBasedPathResolver(task=self.t1, request_type="analyzerfix")
        cache_path = path_resolver.cache_path()
        cache.put(
            path=cache_path,
            input=[HumanMessage(content="human"), AIMessage(content="ai")],
            output=AIMessage("response"),
        )
        expected_trace_dir = (
            Path(self.trace_dir) / "dummy" / self.t1_cache_expected_path.with_suffix("")
        )
        self.assertTrue((expected_trace_dir / "input").exists())
        self.assertTrue((expected_trace_dir / "output").exists())

        cache_path = path_resolver.cache_path()
        # another request on the same cache path
        cache.put(
            input="test",
            output=AIMessage(content="another hello from ai"),
            path=cache_path,
        )
        cache_entry = cache.get(input="test", path=cache_path)
        self.assertIsNotNone(cache_entry)
        self.assertIsInstance(cache_entry, AIMessage)
        if cache_entry is not None:
            self.assertEqual(cache_entry.content, "another hello from ai")

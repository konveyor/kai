"""Tests for LLM classifier with FakeListChatModel."""

import json
import unittest

from langchain_community.chat_models.fake import FakeListChatModel

from kai_commit_miner.attribution.models import AttributedFix, UnattributedChange
from kai_commit_miner.classifier.llm_classifier import (
    LLMClassifier,
    _parse_rule_candidates,
)
from kai_commit_miner.git.diff_parser import DiffHunk
from kai_mcp_solution_server.analyzer_types import Category, ExtendedIncident
from kai_mcp_solution_server.db.python_objects import ViolationID


def _make_fix(
    file_path: str = "src/Foo.java",
    line_number: int = 3,
) -> AttributedFix:
    return AttributedFix(
        incident=ExtendedIncident(
            uri=f"file:///{file_path}",
            message="javax import needs migration",
            code_snip="import javax.ejb.Stateless;",
            line_number=line_number,
            variables={},
            ruleset_name="quarkus/springboot",
            ruleset_description="Quarkus migration",
            violation_name="javax-to-jakarta",
            violation_description="Replace javax with jakarta",
            violation_category=Category.MANDATORY,
            violation_labels=[],
        ),
        violation_key=ViolationID(
            ruleset_name="quarkus/springboot",
            violation_name="javax-to-jakarta",
        ),
        file_path=file_path,
        relevant_hunks=[
            DiffHunk(
                old_start=1,
                old_count=5,
                new_start=1,
                new_count=5,
                content="-import javax.ejb.Stateless;\n+import jakarta.ejb.Stateless;",
            )
        ],
        before_content="import javax.ejb.Stateless;\n@Stateless\nclass Foo {}",
        after_content="import jakarta.ejb.Stateless;\n@Stateless\nclass Foo {}",
        before_snippet="import javax.ejb.Stateless;",
        after_snippet="import jakarta.ejb.Stateless;",
    )


def _make_unattributed() -> UnattributedChange:
    return UnattributedChange(
        file_path="pom.xml",
        hunks=[
            DiffHunk(
                old_start=10,
                old_count=3,
                new_start=10,
                new_count=3,
                content="-<version>2.0</version>\n+<version>3.0</version>",
            )
        ],
    )


class TestLLMClassifier(unittest.IsolatedAsyncioTestCase):
    async def test_classify_generates_hints(self) -> None:
        model = FakeListChatModel(
            responses=[
                "SUMMARY:\nReplace javax imports with jakarta.\n\nHINT:\n1. Change import javax.ejb to jakarta.ejb",
            ]
        )
        classifier = LLMClassifier(
            model=model,
            migration_description="Java EE to Quarkus",
            known_rulesets=["quarkus/springboot"],
        )

        result = await classifier.classify_commit_pair(
            attributed_fixes=[_make_fix()],
            unattributed_changes=[],
            commit_before="aaa",
            commit_after="bbb",
        )

        assert len(result.hints) == 1
        assert "jakarta" in result.hints[0].hint_text
        assert result.hints[0].violation_key.violation_name == "javax-to-jakarta"

    async def test_classify_discovers_rule_candidates(self) -> None:
        rule_yaml = """```yaml
- ruleID: mined-javaee-web-api-dependency
  description: Detects Java EE Web API dependency that needs removal
  category: mandatory
  effort: 1
  when:
    java.dependency:
      name: javax:javaee-web-api
  message: |
    Remove javaee-web-api dependency and replace with individual framework extensions
  labels:
    - konveyor.io/source=java-ee
    - konveyor.io/target=quarkus3
```"""
        model = FakeListChatModel(responses=[rule_yaml])
        classifier = LLMClassifier(
            model=model,
            migration_description="Java EE to Quarkus",
            known_rulesets=["quarkus/springboot"],
        )

        result = await classifier.classify_commit_pair(
            attributed_fixes=[],
            unattributed_changes=[_make_unattributed()],
            commit_before="aaa",
            commit_after="bbb",
        )

        assert len(result.rule_candidates) == 1
        assert result.rule_candidates[0].ruleID == "mined-javaee-web-api-dependency"
        assert result.rule_candidates[0].category == "mandatory"
        assert "java.dependency" in result.rule_candidates[0].when_yaml
        assert "javax" in result.rule_candidates[0].when_yaml

    async def test_classify_both_hints_and_rules(self) -> None:
        model = FakeListChatModel(
            responses=[
                "SUMMARY:\nMigrate javax to jakarta\n\nHINT:\n1. Update imports",
                "[]",  # no rule candidates
            ]
        )
        classifier = LLMClassifier(
            model=model,
            migration_description="Java EE to Quarkus",
            known_rulesets=["quarkus/springboot"],
        )

        result = await classifier.classify_commit_pair(
            attributed_fixes=[_make_fix()],
            unattributed_changes=[_make_unattributed()],
            commit_before="aaa",
            commit_after="bbb",
        )

        assert len(result.hints) == 1
        assert len(result.rule_candidates) == 0


class TestParseRuleCandidates:
    def test_parse_yaml_rule(self) -> None:
        content = """```yaml
- ruleID: mined-test-001
  description: Test rule
  category: mandatory
  effort: 3
  when:
    java.referenced:
      pattern: com.example.OldClass
      location: IMPORT
  message: |
    Replace OldClass with NewClass
  labels:
    - konveyor.io/source=javaee
    - konveyor.io/target=quarkus
```"""
        candidates = _parse_rule_candidates(content, "abc123")
        assert len(candidates) == 1
        assert candidates[0].ruleID == "mined-test-001"
        assert candidates[0].category == "mandatory"
        assert candidates[0].effort == 3
        assert "java.referenced" in candidates[0].when_yaml
        assert candidates[0].source_commit == "abc123"

    def test_parse_empty_array(self) -> None:
        candidates = _parse_rule_candidates("[]", "abc")
        assert len(candidates) == 0

    def test_parse_invalid_content(self) -> None:
        candidates = _parse_rule_candidates("not yaml at all {{{", "abc")
        assert len(candidates) == 0

    def test_parse_non_array(self) -> None:
        candidates = _parse_rule_candidates("ruleID: single-rule", "abc")
        assert len(candidates) == 0

    def test_parse_json_fallback(self) -> None:
        content = '[{"ruleID": "legacy", "description": "old format"}]'
        candidates = _parse_rule_candidates(content, "abc")
        assert len(candidates) == 1
        assert candidates[0].ruleID == "legacy"

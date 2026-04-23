"""Tests for analysis report diffing."""

from kai_commit_miner.diff.models import IncidentDeltaStatus
from kai_commit_miner.diff.report_differ import diff_reports
from kai_mcp_solution_server.analyzer_types import (
    AnalysisReport,
    Category,
    Incident,
    RuleSet,
    Violation,
)


def _make_report(*rulesets: RuleSet) -> AnalysisReport:
    return AnalysisReport(list(rulesets))


def _make_ruleset(name: str, violations: dict[str, Violation] | None = None) -> RuleSet:
    return RuleSet(name=name, description=f"{name} desc", violations=violations)


def _make_violation(
    description: str = "test violation",
    category: Category = Category.MANDATORY,
    incidents: list[Incident] | None = None,
) -> Violation:
    return Violation(
        description=description,
        category=category,
        incidents=incidents,
    )


def _make_incident(
    uri: str = "file:///src/Foo.java",
    message: str = "javax import",
    line_number: int = 3,
) -> Incident:
    return Incident(
        uri=uri,
        message=message,
        code_snip="import javax.ejb.Stateless;",
        line_number=line_number,
        variables={},
    )


def test_no_changes() -> None:
    incident = _make_incident()
    report = _make_report(
        _make_ruleset(
            "rs1",
            {"v1": _make_violation(incidents=[incident])},
        )
    )

    result = diff_reports(report, report, "aaa", "bbb")
    assert len(result.resolved) == 0
    assert len(result.new) == 0
    assert len(result.unchanged) == 1
    assert result.unchanged[0].status == IncidentDeltaStatus.UNCHANGED


def test_resolved_incident() -> None:
    incident = _make_incident()
    before = _make_report(
        _make_ruleset("rs1", {"v1": _make_violation(incidents=[incident])})
    )
    after = _make_report(_make_ruleset("rs1", {"v1": _make_violation(incidents=[])}))

    result = diff_reports(before, after, "aaa", "bbb")
    assert len(result.resolved) == 1
    assert result.resolved[0].status == IncidentDeltaStatus.RESOLVED
    assert result.resolved[0].incident_before is not None
    assert result.resolved[0].incident_before.uri == "file:///src/Foo.java"


def test_new_incident() -> None:
    incident = _make_incident()
    before = _make_report(_make_ruleset("rs1", {"v1": _make_violation(incidents=[])}))
    after = _make_report(
        _make_ruleset("rs1", {"v1": _make_violation(incidents=[incident])})
    )

    result = diff_reports(before, after, "aaa", "bbb")
    assert len(result.new) == 1
    assert result.new[0].status == IncidentDeltaStatus.NEW


def test_moved_incident() -> None:
    before = _make_report(
        _make_ruleset(
            "rs1",
            {"v1": _make_violation(incidents=[_make_incident(line_number=10)])},
        )
    )
    after = _make_report(
        _make_ruleset(
            "rs1",
            {"v1": _make_violation(incidents=[_make_incident(line_number=15)])},
        )
    )

    result = diff_reports(before, after, "aaa", "bbb")
    assert len(result.moved) == 1
    assert result.moved[0].status == IncidentDeltaStatus.MOVED


def test_mixed_changes() -> None:
    before = _make_report(
        _make_ruleset(
            "rs1",
            {
                "v1": _make_violation(
                    incidents=[
                        _make_incident(uri="file:///a.java", line_number=1),
                        _make_incident(uri="file:///b.java", line_number=5),
                    ]
                ),
            },
        )
    )
    after = _make_report(
        _make_ruleset(
            "rs1",
            {
                "v1": _make_violation(
                    incidents=[
                        _make_incident(uri="file:///a.java", line_number=1),
                        # b.java resolved, c.java is new
                        _make_incident(uri="file:///c.java", line_number=10),
                    ]
                ),
            },
        )
    )

    result = diff_reports(before, after, "aaa", "bbb")
    assert len(result.unchanged) == 1
    assert len(result.resolved) == 1
    assert len(result.new) == 1
    assert result.resolved[0].incident_before is not None
    assert result.resolved[0].incident_before.uri == "file:///b.java"
    assert result.new[0].incident_after is not None
    assert result.new[0].incident_after.uri == "file:///c.java"


def test_entire_violation_resolved() -> None:
    before = _make_report(
        _make_ruleset(
            "rs1",
            {
                "v1": _make_violation(incidents=[_make_incident()]),
                "v2": _make_violation(incidents=[_make_incident(uri="file:///x.java")]),
            },
        )
    )
    after = _make_report(
        _make_ruleset(
            "rs1",
            {
                "v1": _make_violation(incidents=[_make_incident()]),
                # v2 gone entirely
            },
        )
    )

    result = diff_reports(before, after, "aaa", "bbb")
    assert len(result.unchanged) == 1
    assert len(result.resolved) == 1
    assert result.resolved[0].violation_key.violation_name == "v2"


def test_empty_reports() -> None:
    empty = _make_report()
    result = diff_reports(empty, empty, "aaa", "bbb")
    assert len(result.resolved) == 0
    assert len(result.new) == 0
    assert len(result.unchanged) == 0
    assert len(result.moved) == 0

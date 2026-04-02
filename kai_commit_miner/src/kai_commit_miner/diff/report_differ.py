"""Diff two AnalysisReports to find resolved, new, unchanged, and moved incidents."""

from kai_commit_miner.diff.models import IncidentDelta, IncidentDeltaStatus, ReportDiff
from kai_mcp_solution_server.analyzer_types import (
    AnalysisReport,
    ExtendedIncident,
    remove_known_prefixes,
)
from kai_mcp_solution_server.db.python_objects import ViolationID

# Line number tolerance for "moved" detection
_LINE_TOLERANCE = 10


def _flatten_report(
    report: AnalysisReport,
) -> dict[ViolationID, list[ExtendedIncident]]:
    """Flatten an AnalysisReport into a dict keyed by ViolationID."""
    result: dict[ViolationID, list[ExtendedIncident]] = {}
    for ruleset in report.root:
        if ruleset.violations is None:
            continue
        for viol_name, violation in ruleset.violations.items():
            key = ViolationID(
                ruleset_name=ruleset.name or "",
                violation_name=viol_name,
            )
            if key not in result:
                result[key] = []
            if violation.incidents is None:
                continue
            for incident in violation.incidents:
                result[key].append(
                    ExtendedIncident(
                        uri=incident.uri,
                        message=incident.message,
                        code_snip=incident.code_snip,
                        line_number=incident.line_number,
                        variables=incident.variables,
                        ruleset_name=ruleset.name or "",
                        ruleset_description=ruleset.description or "",
                        violation_name=viol_name,
                        violation_description=violation.description or "",
                        violation_category=violation.category,
                        violation_labels=violation.labels or [],
                    )
                )
    return result


def _match_incident(
    incident: ExtendedIncident,
    candidates: list[ExtendedIncident],
    strict: bool = True,
) -> ExtendedIncident | None:
    """Find a matching incident in candidates."""
    norm_uri = remove_known_prefixes(incident.uri)
    for candidate in candidates:
        if remove_known_prefixes(candidate.uri) != norm_uri:
            continue
        if candidate.message != incident.message:
            continue
        if strict and candidate.line_number != incident.line_number:
            continue
        if (
            not strict
            and abs(candidate.line_number - incident.line_number) > _LINE_TOLERANCE
        ):
            continue
        return candidate
    return None


def diff_reports(
    report_before: AnalysisReport,
    report_after: AnalysisReport,
    commit_before: str,
    commit_after: str,
) -> ReportDiff:
    """Compare two analysis reports and categorize incident changes."""
    before_map = _flatten_report(report_before)
    after_map = _flatten_report(report_after)

    resolved: list[IncidentDelta] = []
    new: list[IncidentDelta] = []
    unchanged: list[IncidentDelta] = []
    moved: list[IncidentDelta] = []

    matched_after: set[int] = set()

    all_keys = set(before_map.keys()) | set(after_map.keys())

    for key in all_keys:
        before_incidents = before_map.get(key, [])
        after_incidents = after_map.get(key, [])

        for before_inc in before_incidents:
            exact = _match_incident(before_inc, after_incidents, strict=True)
            if exact is not None:
                matched_after.add(id(exact))
                unchanged.append(
                    IncidentDelta(
                        violation_key=key,
                        incident_before=before_inc,
                        incident_after=exact,
                        status=IncidentDeltaStatus.UNCHANGED,
                    )
                )
                continue

            fuzzy = _match_incident(before_inc, after_incidents, strict=False)
            if fuzzy is not None and id(fuzzy) not in matched_after:
                matched_after.add(id(fuzzy))
                moved.append(
                    IncidentDelta(
                        violation_key=key,
                        incident_before=before_inc,
                        incident_after=fuzzy,
                        status=IncidentDeltaStatus.MOVED,
                    )
                )
                continue

            resolved.append(
                IncidentDelta(
                    violation_key=key,
                    incident_before=before_inc,
                    status=IncidentDeltaStatus.RESOLVED,
                )
            )

        for after_inc in after_incidents:
            if id(after_inc) not in matched_after:
                new.append(
                    IncidentDelta(
                        violation_key=key,
                        incident_after=after_inc,
                        status=IncidentDeltaStatus.NEW,
                    )
                )

    return ReportDiff(
        commit_before=commit_before,
        commit_after=commit_after,
        resolved=resolved,
        new=new,
        unchanged=unchanged,
        moved=moved,
    )

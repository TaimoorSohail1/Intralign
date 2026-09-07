from dataclasses import replace

from oslo_api.analysis.models import Assessment, Issue

ISSUE_SEVERITIES = frozenset({"Warning", "Moderate", "Critical"})
_SEVERITY_ALIASES = {
    "warning": "Warning",
    "low": "Warning",
    "moderate": "Moderate",
    "high": "Critical",
    "critical": "Critical",
}


def canonicalize_assessment(assessment: Assessment) -> Assessment:
    """Return an assessment that satisfies the persisted issue contract."""

    return replace(
        assessment,
        issues=tuple(_canonicalize_issue(issue) for issue in assessment.issues),
    )


def _canonicalize_issue(issue: Issue) -> Issue:
    severity = _SEVERITY_ALIASES.get(issue.severity.casefold())
    if severity is None:
        raise ValueError("ISSUE_SEVERITY_CONTRACT_FAILED")
    return issue if issue.severity == severity else replace(issue, severity=severity)

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import oslo_api.analysis.service as analysis_service
from oslo_api.analysis.history import (
    _history_grounding,
    _snapshot_provenance,
    build_resolution_identity_audits,
)
from oslo_api.analysis.service import DatabaseSliceTwoApplication


def _serialized_issue(index: int, *, resolved: bool = False) -> dict:
    return {
        "id": f"ISS-{index:03d}",
        "artifact_type": "requirements",
        "dimension": "Grounding",
        "severity": "Moderate",
        "title": f"Issue {index}",
        "why": "The current read needs verified evidence.",
        "recommendation": "Verify the evidence.",
        "evidence_refs": [f"document:test:page:1:fragment:{index}"],
        "status": "resolved" if resolved else "open",
        "load_bearing": True,
        "primary_act": "verify",
        "basis": "documented" if resolved else None,
    }


def test_snapshot_provenance_rejects_a_stale_cached_grounding_denominator() -> None:
    """B3: History must not prefer 4/88 when the retained read says 4/48."""
    snapshot = {
        "artifacts": [],
        "assessment": {
            "issues": [
                _serialized_issue(index, resolved=index < 4) for index in range(48)
            ]
        },
        "provenance": {
            "schema_version": 1,
            "grounding": {
                "grounded": 4,
                "addressed": 0,
                "routed": 0,
                "inferred": 84,
                "total": 88,
                "basis": 4 / 88,
                "band": "Fragile",
            },
        },
    }

    grounding = _snapshot_provenance(snapshot)["grounding"]

    assert grounding["grounded"] == 4
    assert grounding["total"] == 48


def test_current_history_grounding_uses_the_current_overview_projection() -> None:
    """B3: the current History read must display the same judgment as Overview."""
    retained_snapshot = {
        "artifacts": [],
        "assessment": {
            "issues": [
                _serialized_issue(index, resolved=index < 4) for index in range(88)
            ]
        },
        "provenance": {
            "schema_version": 1,
            "grounding": {
                "grounded": 4,
                "addressed": 0,
                "routed": 0,
                "inferred": 84,
                "total": 88,
                "basis": 4 / 88,
                "band": "Fragile",
            },
        },
    }
    current_overview_grounding = {
        "grounded": 4,
        "addressed": 0,
        "routed": 0,
        "inferred": 44,
        "total": 48,
        "basis": 4 / 48,
        "band": "Fragile",
    }

    grounding = _history_grounding(
        retained_snapshot,
        current=True,
        current_grounding=current_overview_grounding,
    )

    assert grounding["grounded"] == 4
    assert grounding["total"] == 48


def test_historical_grounding_keeps_the_projection_retained_for_that_run() -> None:
    historical_snapshot = {
        "artifacts": [],
        "assessment": {
            "issues": [_serialized_issue(index) for index in range(88)]
        },
        "provenance": {
            "schema_version": 1,
            "grounding": {
                "grounded": 4,
                "addressed": 0,
                "routed": 0,
                "inferred": 84,
                "total": 88,
                "basis": 4 / 88,
                "band": "Fragile",
            },
        },
    }

    grounding = _history_grounding(
        historical_snapshot,
        current=False,
        current_grounding={"grounded": 4, "total": 48},
    )

    assert grounding["grounded"] == 4
    assert grounding["total"] == 88


def test_history_service_passes_the_current_overview_grounding_to_history(
    monkeypatch,
) -> None:
    application = object.__new__(DatabaseSliceTwoApplication)
    workspace_id = uuid4()
    project_id = uuid4()
    user_id = uuid4()
    snapshot = SimpleNamespace(
        artifacts=(),
        assessment=SimpleNamespace(issues=()),
    )
    application._engine = object()
    application._store = SimpleNamespace(current_snapshot=lambda _project_id: snapshot)
    application._workspace_for_project = lambda _user_id, _project_id: workspace_id
    application.list_issue_actions = lambda **_kwargs: [{"issue_id": "ISS-001"}]
    expected_grounding = {"grounded": 4, "total": 48}
    captured: dict = {}

    monkeypatch.setattr(
        analysis_service,
        "build_project_provenance",
        lambda **_kwargs: {"grounding": expected_grounding},
    )
    monkeypatch.setattr(
        analysis_service,
        "with_integrity",
        lambda assessment, _artifacts, **_kwargs: assessment,
    )

    def recording_history(_engine, **kwargs):
        captured.update(kwargs)
        return {"trend": []}

    monkeypatch.setattr(analysis_service, "list_project_history", recording_history)

    result = application.list_history(
        actor_user_id=user_id,
        project_id=project_id,
        category="all",
        cursor=None,
        limit=25,
    )

    assert result == {"trend": []}
    assert captured["current_grounding"] == expected_grounding
    assert captured["workspace_id"] == workspace_id
    assert captured["project_id"] == project_id


def test_history_service_uses_the_same_issue_projection_as_overview(monkeypatch) -> None:
    """IC-WB-EVAL/B3: checkpoint issues must not inflate History's current total."""
    application = object.__new__(DatabaseSliceTwoApplication)
    workspace_id = uuid4()
    project_id = uuid4()
    user_id = uuid4()
    raw_issues = tuple(SimpleNamespace(id=f"ISS-{index:03d}") for index in range(88))
    overview_issues = raw_issues[:48]
    snapshot = SimpleNamespace(
        artifacts=(),
        assessment=SimpleNamespace(issues=raw_issues),
    )
    application._engine = object()
    application._store = SimpleNamespace(current_snapshot=lambda _project_id: snapshot)
    application._workspace_for_project = lambda _user_id, _project_id: workspace_id
    application.list_issue_actions = lambda **_kwargs: []
    captured: dict = {}

    monkeypatch.setattr(
        analysis_service,
        "with_integrity",
        lambda assessment, _artifacts, **_kwargs: SimpleNamespace(
            issues=overview_issues
        ),
        raising=False,
    )

    def recording_provenance(**kwargs):
        captured["issues"] = kwargs["issues"]
        return {"grounding": {"grounded": 4, "total": len(kwargs["issues"])}}

    monkeypatch.setattr(
        analysis_service,
        "build_project_provenance",
        recording_provenance,
    )
    monkeypatch.setattr(
        analysis_service,
        "list_project_history",
        lambda _engine, **kwargs: {"current_grounding": kwargs["current_grounding"]},
    )

    result = application.list_history(
        actor_user_id=user_id,
        project_id=project_id,
        category="all",
        cursor=None,
        limit=25,
    )

    assert captured["issues"] == overview_issues
    assert result["current_grounding"] == {"grounded": 4, "total": 48}


def test_resolution_identity_audit_accepts_only_recorded_lifecycle_departures() -> None:
    """B2: addressed, routed and resolved transitions explain departures from open."""
    occurred_at = datetime(2026, 9, 11, 1, 14, 50, tzinfo=UTC)
    run_id = "6db4691d-01d0-4fcf-9deb-ce6fc0e21149"
    events = [
        {
            "id": 10,
            "run_id": run_id,
            "event_type": "grounding_act.confirm",
            "issue_id": "ISS-CONFIRMED",
            "payload": {},
            # #335 allowed the durable act event to be appended just after the
            # inline run completed. Same-run identity still proves the transition.
            "occurred_at": occurred_at + timedelta(seconds=1),
        },
        {
            "id": 11,
            "run_id": "earlier-run",
            "event_type": "grounding_act.route",
            "issue_id": "ISS-ROUTED",
            "payload": {},
            "occurred_at": occurred_at - timedelta(minutes=5),
        },
        {
            "id": 12,
            "run_id": run_id,
            "event_type": "issues.reconciled",
            "issue_id": None,
            "payload": {"resolved": ["ISS-CONFIRMED", "ISS-ROUTED"]},
            "detail": "2 opened and 2 resolved in this read.",
            "occurred_at": occurred_at,
        },
    ]

    audits = build_resolution_identity_audits(events)

    assert audits == [
        {
            "run_id": run_id,
            "reported_resolved_count": 2,
            "resolved_issue_ids": ["ISS-CONFIRMED", "ISS-ROUTED"],
            "identity_count_matches": True,
            "recorded_transitions": [
            {
                "issue_id": "ISS-CONFIRMED",
                "state": "addressed",
                    "event_type": "grounding_act.confirm",
                    "run_id": run_id,
                    "occurred_at": (occurred_at + timedelta(seconds=1)).isoformat(),
                },
                {
                    "issue_id": "ISS-ROUTED",
                    "state": "routed",
                    "event_type": "grounding_act.route",
                    "run_id": "earlier-run",
                    "occurred_at": (occurred_at - timedelta(minutes=5)).isoformat(),
                },
            ],
            "missing_transition_issue_ids": [],
            "verdict": "pass",
        }
    ]


def test_resolution_identity_audit_fails_a_silent_disappearance() -> None:
    """B2 negative proof: an aggregate count cannot hide an unrecorded departure."""
    occurred_at = datetime(2026, 9, 11, 1, 14, 50, tzinfo=UTC)
    events = [
        {
            "id": 20,
            "run_id": "target-run",
            "event_type": "issues.reconciled",
            "issue_id": None,
            "payload": {"resolved": ["ISS-WITH-TRANSITION", "ISS-VANISHED"]},
            "detail": "7 opened and 2 resolved in this read.",
            "occurred_at": occurred_at,
        },
        {
            "id": 19,
            "run_id": "earlier-run",
            "event_type": "issue.resolution_apply",
            "issue_id": "ISS-WITH-TRANSITION",
            "payload": {},
            "occurred_at": occurred_at - timedelta(minutes=1),
        },
    ]

    audit = build_resolution_identity_audits(events)[0]

    assert audit["verdict"] == "fail"
    assert audit["identity_count_matches"] is True
    assert audit["missing_transition_issue_ids"] == ["ISS-VANISHED"]


def test_resolution_identity_audit_does_not_treat_withdraw_as_a_terminal_state() -> None:
    occurred_at = datetime(2026, 9, 11, 1, 14, 50, tzinfo=UTC)
    events = [
        {
            "id": 30,
            "run_id": "earlier-run",
            "event_type": "grounding_act.confirm",
            "issue_id": "ISS-WITHDRAWN",
            "payload": {},
            "occurred_at": occurred_at - timedelta(minutes=2),
        },
        {
            "id": 31,
            "run_id": "earlier-run",
            "event_type": "grounding_act.withdraw",
            "issue_id": "ISS-WITHDRAWN",
            "payload": {},
            "occurred_at": occurred_at - timedelta(minutes=1),
        },
        {
            "id": 32,
            "run_id": "target-run",
            "event_type": "issues.reconciled",
            "issue_id": None,
            "payload": {"resolved": ["ISS-WITHDRAWN"]},
            "detail": "0 opened and 1 resolved in this read.",
            "occurred_at": occurred_at,
        },
    ]

    audit = build_resolution_identity_audits(events)[0]

    assert audit["verdict"] == "fail"
    assert audit["missing_transition_issue_ids"] == ["ISS-WITHDRAWN"]


def test_resolution_identity_audit_fails_when_count_and_identities_disagree() -> None:
    occurred_at = datetime(2026, 9, 11, 1, 14, 50, tzinfo=UTC)
    audit = build_resolution_identity_audits(
        [
            {
                "id": 40,
                "run_id": "target-run",
                "event_type": "issues.reconciled",
                "issue_id": None,
                "payload": {"resolved": ["ISS-ONLY-IDENTITY"]},
                "detail": "7 opened and 11 resolved in this read.",
                "occurred_at": occurred_at,
            }
        ]
    )[0]

    assert audit["reported_resolved_count"] == 11
    assert audit["resolved_issue_ids"] == ["ISS-ONLY-IDENTITY"]
    assert audit["identity_count_matches"] is False
    assert audit["verdict"] == "fail"

from datetime import UTC, datetime, timedelta

from oslo_api.analysis.history import (
    _snapshot_provenance,
    build_resolution_identity_audits,
)


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

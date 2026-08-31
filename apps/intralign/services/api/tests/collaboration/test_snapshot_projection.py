from oslo_api.collaboration.service import (
    _freeze_public_snapshot,
    _with_current_full_plan_artifacts,
)


def test_public_snapshot_replaces_a_stale_intake_preamble_with_current_title() -> None:
    frozen = _freeze_public_snapshot(
        {
            "project_title": "Atlas B2B Commerce Launch",
            "summary": (
                "DevNorth 2026 is a one-day developer conference. "
                "At the expanded stage, OSLO mapped the supplied evidence into 7 plan "
                "artifacts; 13 open findings identify the main uncertainty."
            ),
            "assessment": {
                "issues": [
                    {"id": "grounded", "status": "resolved"},
                    {"id": "open-1", "status": "open"},
                    {"id": "open-2", "status": "awaiting_evidence"},
                ]
            },
        }
    )

    assert frozen["summary"].startswith("Atlas B2B Commerce Launch.")
    assert "DevNorth" not in frozen["summary"]
    assert "2 open findings" in frozen["summary"]


def test_public_snapshot_does_not_mutate_the_retained_analysis() -> None:
    original = {
        "project_title": "Atlas",
        "summary": "At the expanded stage, 1 open finding remains.",
        "assessment": {"issues": [{"id": "one", "status": "resolved"}]},
    }

    frozen = _freeze_public_snapshot(original)

    assert frozen["summary"] == "Atlas. At the expanded stage, 0 open findings remains."
    assert original["summary"] == "At the expanded stage, 1 open finding remains."


def test_full_plan_projection_uses_current_artifact_drafts_without_mutating_snapshot() -> None:
    original = {
        "artifacts": [
            {
                "artifact_type": "work_breakdown",
                "title": "Retained plan",
                "content": {"sections": []},
            }
        ]
    }
    projected = _with_current_full_plan_artifacts(
        original,
        [
            {
                "artifact_type": "work_breakdown",
                "title": "Current plan",
                "summary": "Latest authored plan",
                "reliability": "grounded",
                "basis": "Confirmed by the user",
                "evidence_refs": ["document:plan:page:1"],
                "content_json": {"sections": [{"rows": [["1.0", "Launch"]]}]},
                "draft_content": {"sections": [{"rows": [["1.0", "Launch now"]]}]},
                "draft_provenance": "confirmed_by_user",
                "assumptions_json": [],
                "conflicts_json": [],
            }
        ],
    )

    assert projected["artifacts"][0]["title"] == "Current plan"
    assert projected["artifacts"][0]["content"]["sections"][0]["rows"] == [
        ["1.0", "Launch now"]
    ]
    assert original["artifacts"][0]["title"] == "Retained plan"
    assert original["artifacts"][0]["content"] == {"sections": []}

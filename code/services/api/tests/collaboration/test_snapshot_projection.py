from oslo_api.collaboration.service import _freeze_public_snapshot


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

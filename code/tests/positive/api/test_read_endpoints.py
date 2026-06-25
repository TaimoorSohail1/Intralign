"""Disclose read-surface endpoints (DTM-0018) — GET list/detail per resource.

Each GET returns the Data Model v1.2 DTO with the epistemic label intact. These
are the positive proofs the frontend can fetch the governed objects over REST.
"""

from __future__ import annotations

from tests.positive.api.conftest import AUTH, PROJECT


def test_list_projects(client) -> None:
    resp = client.get("/v1/projects", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["project_id"] == PROJECT
    assert body[0]["lifecycle_state"] == "oriented"


def test_get_project(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["workspace_id"] == "ws-1"


def test_list_analysis_runs(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/analysis-runs", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()[0]["run_type"] == "fast_analysis_pass"


def test_get_analysis_run(client) -> None:
    resp = client.get("/v1/analysis-runs/run-1", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["run_status"] == "completed"


def test_list_findings_carry_labels(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/findings", headers=AUTH)
    assert resp.status_code == 200
    finding = resp.json()[0]
    assert finding["finding_id"] == "f-1"
    assert finding["finding_type"] == "conflict"
    # The epistemic label travels with the object (decision #5).
    assert finding["label"]["epistemic_label"] == "derived"
    assert finding["label"]["confidence_band"] == "medium"
    assert finding["label"]["conflict_state"] == "contested"


def test_get_finding_detail(client) -> None:
    resp = client.get("/v1/findings/f-1", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["finding_id"] == "f-1"


def test_list_recommendations(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/recommendations", headers=AUTH)
    assert resp.status_code == 200
    rec = resp.json()[0]
    assert rec["recommendation_id"] == "r-1"
    assert rec["finding_id"] == "f-1"
    assert rec["recommendation_type"] == "improvement"
    assert rec["status"] == "generated"
    assert rec["label"]["epistemic_label"] == "derived"


def test_list_recommendations_for_finding_rp_c1(client) -> None:
    """RP-C1: recommendations are listed in a Finding context."""
    resp = client.get(
        "/v1/findings/f-1/recommendations", params={"project_id": PROJECT}, headers=AUTH
    )
    assert resp.status_code == 200
    assert all(r["finding_id"] == "f-1" for r in resp.json())


def test_get_recommendation_detail(client) -> None:
    resp = client.get("/v1/recommendations/r-1", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["recommendation_id"] == "r-1"


def test_get_confidence(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/confidence", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["confidence_band"] == "medium"
    assert body["label"]["epistemic_label"] == "derived"


def test_get_caf(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/caf", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["feasibility"]["band"] == "high"


def test_list_acceptances_attested_user(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/acceptance", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()[0]["epistemic_label"] == "attested-user"


def test_list_plan_facts_attested_user(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/plan-facts", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()[0]["epistemic_label"] == "attested-user"


def test_list_acceptance_impact_derived(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/acceptance-impact", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()[0]
    assert body["band_changed"] is True
    assert body["label"]["epistemic_label"] == "derived"


def test_list_notifications(client) -> None:
    resp = client.get("/v1/notifications", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()[0]["state"] == "created"


def test_notifications_filter_by_state(client) -> None:
    resp = client.get("/v1/notifications", params={"state": "dismissed"}, headers=AUTH)
    assert resp.status_code == 200
    assert resp.json() == []

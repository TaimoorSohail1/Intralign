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


def test_list_issues_carry_labels_and_lineage(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/issues", headers=AUTH)
    assert resp.status_code == 200
    issue = resp.json()[0]
    assert issue["issue_id"] == "i-1"
    assert issue["finding_id"] == "f-1"  # source-Finding lineage
    assert issue["finding_type"] == "conflict"
    assert issue["severity"] == "critical"
    assert issue["label"]["epistemic_label"] == "derived"
    assert issue["label"]["conflict_state"] == "contested"
    # No internal cognition field leaks onto the Issue DTO.
    assert "mode" not in issue
    assert "confidence_stage" not in issue
    assert "understanding_state" not in issue


def test_list_issues_filter_by_finding(client) -> None:
    resp = client.get(
        f"/v1/projects/{PROJECT}/issues", params={"finding_id": "f-1"}, headers=AUTH
    )
    assert resp.status_code == 200
    assert all(i["finding_id"] == "f-1" for i in resp.json())
    resp_none = client.get(
        f"/v1/projects/{PROJECT}/issues", params={"finding_id": "nope"}, headers=AUTH
    )
    assert resp_none.json() == []


def test_get_issue_detail(client) -> None:
    resp = client.get("/v1/issues/i-1", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["issue_id"] == "i-1"


def test_get_issue_detail_missing_is_404(client) -> None:
    resp = client.get("/v1/issues/does-not-exist", headers=AUTH)
    assert resp.status_code == 404


def test_overview_counts_and_aggregates_labelled(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/overview", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    counts = {c["kind"]: c["count"] for c in body["counts"]}
    assert counts == {"finding": 1, "issue": 1, "recommendation": 1}
    assert {c["label"] for c in body["counts"]} == {"findings", "issues", "recommendations"}
    # The aggregates carry their Derived band (presentation, not a health number).
    assert body["outcome_confidence"]["confidence_band"] == "medium"
    assert body["outcome_confidence"]["label"]["epistemic_label"] == "derived"
    assert body["caf"]["feasibility"]["band"] == "high"
    # NOT a project-health metric — no health/score field on the payload.
    assert "health" not in body
    assert "score" not in body
    assert "readiness" not in body
    assert "probability" not in body


def test_history_feed_append_order_derived_labelled(client) -> None:
    resp = client.get(f"/v1/projects/{PROJECT}/history", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    # Append order: oldest emitted first.
    assert [e["chr_id"] for e in body] == ["chr-1", "chr-2"]
    # Each entry is the OSLO-self-attested Derived trail receipt.
    assert all(e["epistemic_label"] == "attested-oslo" for e in body)
    # The supersession link is the drift backbone.
    assert body[1]["supersedes_chr_id"] == "chr-1"
    # No internal CHR field leaks onto the trail entry.
    assert "output_payload" not in body[0]
    assert "model_or_rule_version" not in body[0]


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

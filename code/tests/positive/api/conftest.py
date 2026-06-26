"""Shared API test harness (DTM-0018) — a TestClient with the read seam faked.

The Disclose read surface is exercised end-to-end over HTTP via FastAPI's
TestClient, with:
- ``current_principal`` overridden to a fixed in-workspace Principal (auth/scoping
  is the dependency the routers consume; the JWT seam itself is deployment-wired).
- ``get_projection_reader`` overridden with an in-memory SELECT-only fake (no
  Supabase). The fake mirrors the real ``ProjectionReader`` read surface and has
  NO write method (read-mostly by construction).
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_history_reader,
    get_projection_reader,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
WORKSPACE = "ws-1"


class FakeReader:
    """In-memory SELECT-only read seam (mirrors ProjectionReader; no writes)."""

    def __init__(self) -> None:
        self.projections: dict[str, list[dict[str, Any]]] = {}
        self.acceptances: list[dict[str, Any]] = []
        self.plan_facts: list[dict[str, Any]] = []
        self.projects: list[dict[str, Any]] = []
        self.analysis_runs: list[dict[str, Any]] = []
        self.notifications: list[dict[str, Any]] = []

    def list_projection(self, project_id: str, output_kind: str) -> list[dict[str, Any]]:
        return [
            r for r in self.projections.get(output_kind, [])
            if str(r.get("project_id")) == project_id
        ]

    def get_projection(self, output_kind: str, projection_id: str) -> dict[str, Any] | None:
        for r in self.projections.get(output_kind, []):
            if str(r.get("projection_id")) == projection_id:
                return r
        return None

    def list_acceptances(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.acceptances if str(r.get("project_id")) == project_id]

    def list_plan_facts(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.plan_facts if str(r.get("project_id")) == project_id]

    def list_projects(self, workspace_id: str) -> list[dict[str, Any]]:
        return [r for r in self.projects if str(r.get("workspace_id")) == workspace_id]

    def get_project(self, project_id: str) -> dict[str, Any] | None:
        for r in self.projects:
            if str(r.get("project_id")) == project_id:
                return r
        return None

    def list_analysis_runs(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.analysis_runs if str(r.get("project_id")) == project_id]

    def get_analysis_run(self, analysis_run_id: str) -> dict[str, Any] | None:
        for r in self.analysis_runs:
            if str(r.get("analysis_run_id")) == analysis_run_id:
                return r
        return None

    def list_notifications(self, workspace_id: str) -> list[dict[str, Any]]:
        return [r for r in self.notifications if str(r.get("workspace_id")) == workspace_id]


class FakeHistoryReader:
    """In-memory SELECT-only Cognition-History trail reader (no append/mutate).

    Returns the CHR rows for a project in APPEND ORDER (oldest emitted first), the
    way the real ``SupabaseHistoryReader`` orders by ``emitted_at`` ascending.
    """

    def __init__(self) -> None:
        self.history: list[dict[str, Any]] = []

    def list_history(self, project_id: str) -> list[dict[str, Any]]:
        rows = [r for r in self.history if str(r.get("project_id")) == project_id]
        return sorted(rows, key=lambda r: r.get("emitted_at") or "")


def _projection_row(output_kind: str, payload: dict, project_id: str = PROJECT, **env) -> dict:
    return {
        "projection_id": env.get("projection_id", f"{output_kind}-proj-1"),
        "project_id": project_id,
        "output_kind": output_kind,
        "current_payload": payload,
        "current_chr_ref": "chr-1",
        "epistemic_label": "derived",
        "confidence_value": env.get("confidence_value", 60.0),
        "confidence_band": env.get("confidence_band", "medium"),
        "conflict_state": env.get("conflict_state", "none"),
        "recomputed_at": "2026-06-25T00:00:00Z",
    }


@pytest.fixture
def reader() -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE, "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    })
    r.analysis_runs.append({
        "analysis_run_id": "run-1", "project_id": PROJECT,
        "run_type": "fast_analysis_pass", "run_status": "completed",
        "started_at": "2026-06-25T00:00:00Z",
    })
    r.projections.setdefault("finding", []).append(_projection_row(
        "finding", {"finding_id": "f-1", "finding_type": "conflict", "summary": "x",
                    "evidence_anchors": ["a-0"], "status": "detected"},
        conflict_state="contested", projection_id="f-1"))
    r.projections.setdefault("issue", []).append(_projection_row(
        "issue", {"issue_id": "i-1", "finding_id": "f-1", "finding_type": "conflict",
                  "severity": "critical", "summary": "x", "evidence_anchors": ["a-0"],
                  "status": "detected",
                  # internal-only payload fields that must NOT leak onto the DTO:
                  "mode": "fast", "confidence_stage": "orientation",
                  "understanding_state": "initial", "epistemic_state": "derived"},
        conflict_state="contested", projection_id="i-1"))
    r.projections.setdefault("recommendation", []).append(_projection_row(
        "recommendation", {"recommendation_id": "r-1", "anchor": "f-1",
                           "recommendation_type": "candidate_improvement",
                           "summary": "Clarify scope.", "state": "generated"},
        projection_id="r-1"))
    r.projections.setdefault("outcome_confidence", []).append(_projection_row(
        "outcome_confidence", {"index": 62.0, "band": "medium",
                               "reliability_qualifier": "moderate", "basis": ["clarity"]}))
    r.projections.setdefault("caf", []).append(_projection_row(
        "caf", {"dimensions": {
            "clarity": {"index": 70.0, "band": "medium", "reliability": "moderate"},
            "alignment": {"index": 55.0, "band": "medium", "reliability": "low"},
            "feasibility": {"index": 80.0, "band": "high", "reliability": "high"}}}))
    r.projections.setdefault("acceptance_impact", []).append(_projection_row(
        "acceptance_impact", {"uar_ref": "uar-1", "pinned_chr": "c-a", "latest_chr": "c-b",
                              "delta": -12.0, "band_changed": True}))
    r.acceptances.append({
        "uar_id": "uar-1", "project_id": PROJECT, "user_id": "u-1", "action": "accept",
        "target_kind": "recommendation", "version_pin": "chr-1",
        "epistemic_state": "attested-user", "created_at": "2026-06-25T00:00:00Z"})
    r.plan_facts.append({
        "assertion_id": "pf-1", "project_id": PROJECT, "proposition": "Scope excludes X.",
        "content_type": "fact", "attesting_source": "u-1", "epistemic_state": "attested-user",
        "provenance_ref": {"version_pin": "chr-1", "user_id": "u-1"},
        "created_at": "2026-06-25T00:00:00Z"})
    r.notifications.append({
        "notification_id": "n-1", "workspace_id": WORKSPACE, "project_id": PROJECT,
        "source_object_type": "finding", "source_object_id": "f-1",
        "event_type": "created", "state": "created"})
    return r


@pytest.fixture
def history_reader() -> FakeHistoryReader:
    r = FakeHistoryReader()
    # Two CHRs in append order; the second supersedes the first (drift backbone).
    r.history.append({
        "chr_id": "chr-1", "project_id": PROJECT, "output_kind": "outcome_confidence",
        "recompute_trigger": "promotion", "supersedes_chr_id": None,
        "emitted_at": "2026-06-25T00:00:00Z", "epistemic_state": "attested-oslo",
        # internal-only CHR fields that must NOT leak onto the trail DTO:
        "output_payload": {"index": 60.0}, "model_or_rule_version": {"model": "x"},
    })
    r.history.append({
        "chr_id": "chr-2", "project_id": PROJECT, "output_kind": "outcome_confidence",
        "recompute_trigger": "knowledge-change", "supersedes_chr_id": "chr-1",
        "emitted_at": "2026-06-25T01:00:00Z", "epistemic_state": "attested-oslo",
        "output_payload": {"index": 55.0}, "model_or_rule_version": {"model": "x"},
    })
    return r


@pytest.fixture
def principal() -> Principal:
    return Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")


@pytest.fixture
def client(
    reader: FakeReader, history_reader: FakeHistoryReader, principal: Principal
) -> TestClient:
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_history_reader] = lambda: history_reader
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Header presence is irrelevant once current_principal is overridden, but the
# real routers require it — keep an auth header for realism.
AUTH = {"Authorization": "Bearer test-token"}

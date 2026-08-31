"""DEV-ONLY local server for manual UI checks — NOT prod, NOT committed canon.

Boots the real FastAPI app but overrides the two seams that aren't wired locally,
using the code's OWN supported pattern (deps.py: "overridable via
app.dependency_overrides — the house pattern"):

- ``current_principal`` -> a fixed in-workspace dev Principal (the Supabase-Auth
  JWT seam only wires at deployment).
- ``get_projection_reader`` -> an in-memory SELECT-only reader seeded with a demo
  dataset (no Supabase / Neo4j / Redis needed; no projection-write wave exists yet).

This invents NO production behaviour and writes nothing — it just lets the
read-only Disclose surfaces render real DTOs for a manual walkthrough.

Run:  cd apps/intralign && .venv/bin/python scripts/dev_server.py    # serves :8000
"""

from __future__ import annotations

from typing import Any

import uvicorn

from backend.api.app import app
from backend.api.deps import Principal, current_principal, get_projection_reader

WORKSPACE = "ws-dev"
P1 = "11111111-1111-1111-1111-111111111111"
P2 = "22222222-2222-2222-2222-222222222222"


def _proj(output_kind: str, payload: dict, project_id: str, pid: str, **env) -> dict:
    return {
        "projection_id": pid,
        "project_id": project_id,
        "output_kind": output_kind,
        "current_payload": payload,
        "current_chr_ref": env.get("chr", "chr-1"),
        "epistemic_label": "derived",
        "confidence_value": env.get("confidence_value", 60.0),
        "confidence_band": env.get("confidence_band", "medium"),
        "conflict_state": env.get("conflict_state", "none"),
        "recomputed_at": "2026-06-26T00:00:00Z",
    }


class SeededReader:
    """In-memory SELECT-only reader (mirrors ProjectionReader; no writes)."""

    def __init__(self) -> None:
        self.projections: dict[str, list[dict[str, Any]]] = {}
        self.acceptances: list[dict[str, Any]] = []
        self.plan_facts: list[dict[str, Any]] = []
        self.projects: list[dict[str, Any]] = []
        self.analysis_runs: list[dict[str, Any]] = []
        self.notifications: list[dict[str, Any]] = []
        self._seed()

    # --- ProjectionReader surface -------------------------------------------
    def list_projection(self, project_id: str, output_kind: str) -> list[dict[str, Any]]:
        return [r for r in self.projections.get(output_kind, []) if str(r["project_id"]) == project_id]

    def get_projection(self, output_kind: str, projection_id: str) -> dict[str, Any] | None:
        return next((r for r in self.projections.get(output_kind, []) if str(r["projection_id"]) == projection_id), None)

    def list_acceptances(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.acceptances if str(r["project_id"]) == project_id]

    def list_plan_facts(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.plan_facts if str(r["project_id"]) == project_id]

    def list_projects(self, workspace_id: str) -> list[dict[str, Any]]:
        return [r for r in self.projects if str(r["workspace_id"]) == workspace_id]

    def get_project(self, project_id: str) -> dict[str, Any] | None:
        return next((r for r in self.projects if str(r["project_id"]) == project_id), None)

    def list_analysis_runs(self, project_id: str) -> list[dict[str, Any]]:
        return [r for r in self.analysis_runs if str(r["project_id"]) == project_id]

    def get_analysis_run(self, analysis_run_id: str) -> dict[str, Any] | None:
        return next((r for r in self.analysis_runs if str(r["analysis_run_id"]) == analysis_run_id), None)

    def list_notifications(self, workspace_id: str) -> list[dict[str, Any]]:
        return [r for r in self.notifications if str(r["workspace_id"]) == workspace_id]

    # --- demo dataset --------------------------------------------------------
    def _seed(self) -> None:
        self.projects += [
            {"project_id": P1, "workspace_id": WORKSPACE, "title": "Atlas Migration",
             "lifecycle_state": "oriented", "current_confidence_state_id": "oc-1",
             "created_at": "2026-06-20T00:00:00Z"},
            {"project_id": P2, "workspace_id": WORKSPACE, "title": "Payments Revamp",
             "lifecycle_state": "created", "current_confidence_state_id": None,
             "created_at": "2026-06-24T00:00:00Z"},
        ]
        self.analysis_runs += [
            {"analysis_run_id": "run-1", "project_id": P1, "run_type": "fast_analysis_pass",
             "run_status": "superseded", "previous_run_id": None, "started_at": "2026-06-20T09:00:00Z"},
            {"analysis_run_id": "run-2", "project_id": P1, "run_type": "deep_analysis_pass",
             "run_status": "completed", "previous_run_id": "run-1", "started_at": "2026-06-25T09:00:00Z"},
        ]
        findings = [
            ("f-1", "conflict", "Scope and schedule disagree on the Q3 cutover date.",
             ["intent#3", "schedule#7"], "critical", "low", "contested"),
            ("f-2", "gap", "No acceptance criteria defined for the data-migration step.",
             ["scope#2"], "moderate", "medium", "none"),
            ("f-3", "risk", "Single-owner dependency on the legacy ETL is a delivery risk.",
             ["resources#1"], "warning", "high", "none"),
        ]
        for fid, ftype, summary, anchors, sev, band, conflict in findings:
            self.projections.setdefault("finding", []).append(_proj(
                "finding",
                {"finding_id": fid, "finding_type": ftype, "summary": summary,
                 "evidence_anchors": anchors, "evidence_links": anchors,
                 "severity": sev, "status": "detected",
                 "affected_caf_dimensions": ["clarity"] if ftype == "gap" else ["alignment"]},
                P1, fid, confidence_band=band, conflict_state=conflict, chr="run-2"))
        self.projections.setdefault("recommendation", []).extend([
            _proj("recommendation",
                  {"recommendation_id": "r-1", "anchor": "f-1", "finding_id": "f-1",
                   "recommendation_type": "candidate_improvement", "state": "generated",
                   "summary": "Reconcile the cutover date with stakeholders before locking scope."},
                  P1, "r-1", chr="run-2"),
            _proj("recommendation",
                  {"recommendation_id": "r-2", "anchor": "f-1", "finding_id": "f-1",
                   "recommendation_type": "suggested_action", "state": "generated",
                   "summary": "Hold the cutover date and rebaseline the schedule instead."},
                  P1, "r-2", chr="run-2"),
            _proj("recommendation",
                  {"recommendation_id": "r-3", "anchor": "f-2", "finding_id": "f-2",
                   "recommendation_type": "validation", "state": "generated",
                   "summary": "Confirm migration acceptance criteria with the data owner."},
                  P1, "r-3", chr="run-2"),
        ])
        self.projections.setdefault("outcome_confidence", []).append(_proj(
            "outcome_confidence",
            {"index": 58.0, "band": "medium", "reliability_qualifier": "moderate",
             "basis": ["clarity", "alignment"]}, P1, "oc-1",
            confidence_value=58.0, confidence_band="medium", chr="run-2"))
        self.projections.setdefault("caf", []).append(_proj(
            "caf",
            {"dimensions": {
                "clarity": {"index": 72.0, "band": "medium", "reliability": "moderate"},
                "alignment": {"index": 44.0, "band": "low", "reliability": "low"},
                "feasibility": {"index": 81.0, "band": "high", "reliability": "high"}}},
            P1, "caf-1", confidence_band="medium", chr="run-2"))
        self.projections.setdefault("acceptance_impact", []).append(_proj(
            "acceptance_impact",
            {"uar_ref": "uar-1", "pinned_chr": "run-1", "latest_chr": "run-2",
             "delta": -14.0, "band_changed": True,
             "summary": "A decision you confirmed is affected by the latest analysis."},
            P1, "ai-1", confidence_value=44.0, confidence_band="low", chr="run-2"))
        self.acceptances.append({
            "uar_id": "uar-1", "project_id": P1, "user_id": "u-dev", "action": "accept",
            "target_kind": "recommendation", "target_id": "r-1", "version_pin": "run-1",
            "epistemic_state": "attested-user", "created_at": "2026-06-22T00:00:00Z"})
        self.plan_facts.append({
            "assertion_id": "pf-1", "project_id": P1,
            "proposition": "The Q3 cutover date is fixed and will not move.",
            "content_type": "fact", "attesting_source": "u-dev", "epistemic_state": "attested-user",
            "provenance_ref": {"version_pin": "run-1", "user_id": "u-dev"},
            "created_at": "2026-06-22T00:00:00Z"})
        self.notifications += [
            {"notification_id": "n-1", "workspace_id": WORKSPACE, "project_id": P1,
             "source_object_type": "acceptance_impact", "source_object_id": "ai-1",
             "event_type": "acceptance_impact", "state": "created"},
            {"notification_id": "n-2", "workspace_id": WORKSPACE, "project_id": P1,
             "source_object_type": "finding", "source_object_id": "f-1",
             "event_type": "created", "state": "created"},
        ]


app.dependency_overrides[current_principal] = lambda: Principal(
    user_id="u-dev", workspace_id=WORKSPACE, role="owner")
app.dependency_overrides[get_projection_reader] = lambda: SeededReader()


if __name__ == "__main__":
    print("DEV server (seeded, no backing services) on http://localhost:8000")
    print(f"  demo projects: {P1} (Atlas Migration), {P2} (Payments Revamp)")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

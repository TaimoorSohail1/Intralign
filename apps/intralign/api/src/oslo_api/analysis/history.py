import base64
import json
import re
from collections import OrderedDict
from collections.abc import Iterable, Mapping
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from sqlalchemy import Connection, Engine, text

from oslo_api.analysis.provenance import build_serialized_project_provenance

HistoryCategory = Literal[
    "analysis",
    "issues",
    "versions",
    "decisions",
    "collaboration",
]


def _snapshot_provenance(snapshot: dict) -> dict:
    rebuilt = build_serialized_project_provenance(snapshot)
    stored = snapshot.get("provenance")
    if isinstance(stored, dict) and isinstance(stored.get("grounding"), dict):
        stored_total = stored["grounding"].get("total")
        rebuilt_total = rebuilt["grounding"].get("total")
        if stored_total == rebuilt_total:
            return stored
    # Provenance is derived cognition, not canonical state. A retained payload
    # can carry a projection written before its issue set was reconciled. When
    # that cache disagrees with the retained assessment, rebuild it from the
    # assessment so History and Overview describe one Grounding population.
    return rebuilt


_TRANSITION_STATE_BY_EVENT = {
    "clarification.answered": "addressed",
    "review.responded": "addressed",
    "issue.resolution_selected": "addressed",
    "grounding_act.confirm": "addressed",
    "grounding_act.confirmed": "addressed",
    "grounding_act.answer": "addressed",
    "grounding_act.answered": "addressed",
    "grounding_act.fix": "addressed",
    "grounding_act.fix_applied": "addressed",
    "grounding_act.flag": "needs_fix",
    "grounding_act.flagged": "needs_fix",
    "grounding_act.ground": "addressed",
    "grounding_act.grounded": "addressed",
    "grounding_act.route": "routed",
    "grounding_act.routed": "routed",
    "grounding_act.withdraw": "open",
    "grounding_act.withdrawn": "open",
}
_RECORDED_DEPARTURE_STATES = {"addressed", "routed", "resolved"}


def _event_time(value: object) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value or "")


def _transition_state(event_type: str) -> str | None:
    if event_type.startswith("issue.resolution_"):
        return "addressed"
    return _TRANSITION_STATE_BY_EVENT.get(event_type)


def build_resolution_identity_audits(
    events: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Prove aggregate resolved counts against stable keys and legal transitions.

    IC-WB-INFER and the ratified B2 wording permit an issue to leave the open
    set only through ``addressed``, ``routed`` or ``resolved``. The aggregate
    History count is not evidence unless every identity has such a transition.
    """

    rows = [dict(event) for event in events]
    transitions = [
        {
            **event,
            "state": _transition_state(str(event.get("event_type") or "")),
        }
        for event in rows
        if event.get("issue_id")
        and _transition_state(str(event.get("event_type") or "")) is not None
    ]
    audits: list[dict[str, Any]] = []
    for reconciliation in rows:
        if reconciliation.get("event_type") != "issues.reconciled":
            continue
        detail = str(reconciliation.get("detail") or "")
        payload = reconciliation.get("payload")
        payload = payload if isinstance(payload, dict) else {}
        raw_resolved = payload.get("resolved")
        declared_match = re.search(r"\b(\d+) resolved\b", detail)
        reported_count = (
            int(declared_match.group(1))
            if declared_match
            else len(raw_resolved)
            if isinstance(raw_resolved, list)
            else 0
        )
        if reported_count == 0:
            continue

        run_id = str(reconciliation.get("run_id") or "")
        if not isinstance(raw_resolved, list):
            audits.append(
                {
                    "run_id": run_id,
                    "reported_resolved_count": reported_count,
                    "resolved_issue_ids": [],
                    "identity_count_matches": False,
                    "recorded_transitions": [],
                    "missing_transition_issue_ids": [],
                    "verdict": "unverifiable",
                }
            )
            continue

        resolved_ids = list(dict.fromkeys(str(issue_id) for issue_id in raw_resolved))
        identity_count_matches = len(resolved_ids) == reported_count
        recorded: list[dict[str, Any]] = []
        missing: list[str] = []
        reconciliation_time = _event_time(reconciliation.get("occurred_at"))
        for issue_id in resolved_ids:
            candidates = [
                transition
                for transition in transitions
                if str(transition.get("issue_id")) == issue_id
                and (
                    str(transition.get("run_id") or "") == run_id
                    or _event_time(transition.get("occurred_at")) <= reconciliation_time
                )
            ]
            if not candidates:
                missing.append(issue_id)
                continue
            latest = max(
                candidates,
                key=lambda event: (
                    _event_time(event.get("occurred_at")),
                    int(event.get("id") or 0),
                ),
            )
            state = str(latest["state"])
            if state not in _RECORDED_DEPARTURE_STATES:
                missing.append(issue_id)
                continue
            recorded.append(
                {
                    "issue_id": issue_id,
                    "state": state,
                    "event_type": str(latest.get("event_type") or ""),
                    "run_id": str(latest.get("run_id") or ""),
                    "occurred_at": _event_time(latest.get("occurred_at")),
                }
            )
        audits.append(
            {
                "run_id": run_id,
                "reported_resolved_count": reported_count,
                "resolved_issue_ids": resolved_ids,
                "identity_count_matches": identity_count_matches,
                "recorded_transitions": recorded,
                "missing_transition_issue_ids": missing,
                "verdict": "fail" if missing or not identity_count_matches else "pass",
            }
        )
    return audits


def append_history_event(
    connection: Connection,
    *,
    workspace_id: UUID,
    project_id: UUID,
    analysis_run_id: UUID,
    actor_type: Literal["user", "oslo", "system"],
    category: HistoryCategory,
    event_type: str,
    summary: str,
    idempotency_key: str,
    actor_id: UUID | None = None,
    detail: str | None = None,
    artifact_type: str | None = None,
    artifact_version: int | None = None,
    issue_id: str | None = None,
    payload: dict | None = None,
) -> None:
    """Append one safe, idempotent product-history event."""

    connection.execute(
        text(
            """
            insert into public.project_history_events (
              workspace_id, project_id, analysis_run_id, actor_id, actor_type,
              category, event_type, summary, detail, artifact_type,
              artifact_version, issue_stable_key, payload, idempotency_key
            ) values (
              :workspace_id, :project_id, :analysis_run_id, :actor_id, :actor_type,
              cast(:category as public.project_history_category),
              :event_type, :summary, :detail,
              cast(:artifact_type as public.plan_artifact_type),
              :artifact_version, :issue_id, cast(:payload as jsonb), :idempotency_key
            )
            on conflict (workspace_id, idempotency_key) do nothing
            """
        ),
        {
            "workspace_id": workspace_id,
            "project_id": project_id,
            "analysis_run_id": analysis_run_id,
            "actor_id": actor_id,
            "actor_type": actor_type,
            "category": category,
            "event_type": event_type,
            "summary": summary[:300],
            "detail": detail[:2000] if detail else None,
            "artifact_type": artifact_type,
            "artifact_version": artifact_version,
            "issue_id": issue_id,
            "payload": json.dumps(payload or {}),
            "idempotency_key": idempotency_key,
        },
    )


def _encode_cursor(occurred_at: datetime, event_id: int) -> str:
    raw = f"{occurred_at.isoformat()}|{event_id}".encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _decode_cursor(cursor: str | None) -> tuple[datetime, int] | None:
    if not cursor:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        raw = base64.urlsafe_b64decode(padded.encode()).decode()
        timestamp, event_id = raw.rsplit("|", 1)
        return datetime.fromisoformat(timestamp), int(event_id)
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError("INVALID_HISTORY_CURSOR") from error


def _change_labels(
    snapshot: dict,
    previous: dict | None,
) -> list[dict[str, str]]:
    if previous is None:
        count = len(snapshot.get("assessment", {}).get("issues", []))
        return [{"label": f"{count} issues opened", "tone": "neutral"}]
    current_assessment = snapshot.get("assessment", {})
    previous_assessment = previous.get("assessment", {})
    labels: list[dict[str, str]] = []
    for key, name in (
        ("clarity", "Clarity"),
        ("alignment", "Alignment"),
        ("feasibility", "Feasibility"),
    ):
        before = previous_assessment.get(key)
        after = current_assessment.get(key)
        if before and after and before != after:
            labels.append(
                {
                    "label": f"{name} {before} → {after}",
                    "tone": "positive"
                    if current_assessment.get("confidence_index", 0)
                    >= previous_assessment.get("confidence_index", 0)
                    else "warning",
                }
            )
    previous_issues = {
        item.get("id")
        for item in previous_assessment.get("issues", [])
        if item.get("status") != "resolved"
    }
    current_issues = {
        item.get("id")
        for item in current_assessment.get("issues", [])
        if item.get("status") != "resolved"
    }
    opened = len(current_issues - previous_issues)
    resolved = len(previous_issues - current_issues)
    if opened:
        labels.append({"label": f"{opened} opened", "tone": "warning"})
    if resolved:
        labels.append({"label": f"{resolved} resolved", "tone": "positive"})
    return labels or [{"label": "Read strengthened", "tone": "neutral"}]


def list_project_history(
    engine: Engine,
    *,
    workspace_id: UUID,
    project_id: UUID,
    category: str,
    cursor: str | None,
    limit: int,
) -> dict:
    decoded = _decode_cursor(cursor)
    cursor_time, cursor_id = decoded or (None, None)
    category_clause = "" if category == "all" else "and history.category = :category"
    cursor_clause = (
        ""
        if cursor_time is None
        else """
          and (history.occurred_at, history.id) < (:cursor_time, :cursor_id)
        """
    )
    params = {
        "workspace_id": workspace_id,
        "project_id": project_id,
        "category": category,
        "cursor_time": cursor_time,
        "cursor_id": cursor_id,
        "limit": limit + 1,
    }
    with engine.connect() as connection:
        rows = (
            connection.execute(
                text(
                    f"""
                    select history.id, history.analysis_run_id, history.category,
                           history.event_type, history.summary, history.detail,
                           history.actor_type, history.artifact_type,
                           history.artifact_version, history.issue_stable_key,
                           history.occurred_at, run.kind, run.status,
                           snapshot.snapshot_json,
                           project.current_analysis_run_id
                    from public.project_history_events history
                    join public.analysis_runs run on run.id = history.analysis_run_id
                    join public.projects project on project.id = history.project_id
                    left join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = history.analysis_run_id
                    where history.workspace_id = :workspace_id
                      and history.project_id = :project_id
                      {category_clause}
                      {cursor_clause}
                    order by history.occurred_at desc, history.id desc
                    limit :limit
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        snapshots = (
            connection.execute(
                text(
                    """
                    select snapshot.analysis_run_id, snapshot.snapshot_json,
                           snapshot.published_at, run.kind, run.status,
                           project.current_analysis_run_id
                    from public.assessment_snapshots snapshot
                    join public.analysis_runs run on run.id = snapshot.analysis_run_id
                    join public.projects project on project.id = snapshot.project_id
                    where snapshot.workspace_id = :workspace_id
                      and snapshot.project_id = :project_id
                    order by snapshot.published_at
                    """
                ),
                {"workspace_id": workspace_id, "project_id": project_id},
            )
            .mappings()
            .all()
        )
        identity_rows = (
            connection.execute(
                text(
                    """
                    select history.id, history.analysis_run_id as run_id,
                           history.event_type,
                           history.issue_stable_key as issue_id,
                           history.payload, history.detail, history.occurred_at
                    from public.project_history_events history
                    where history.workspace_id = :workspace_id
                      and history.project_id = :project_id
                      and (
                        history.event_type = 'issues.reconciled'
                        or history.issue_stable_key is not null
                      )
                    order by history.occurred_at, history.id
                    """
                ),
                {"workspace_id": workspace_id, "project_id": project_id},
            )
            .mappings()
            .all()
        )
    has_more = len(rows) > limit
    page_rows = rows[:limit]
    previous_by_run: dict[UUID, dict | None] = {}
    previous: dict | None = None
    for snapshot_row in snapshots:
        previous_by_run[snapshot_row["analysis_run_id"]] = previous
        previous = dict(snapshot_row["snapshot_json"])

    grouped: OrderedDict[UUID, dict] = OrderedDict()
    for row in page_rows:
        run_id = row["analysis_run_id"]
        snapshot = (
            dict(row["snapshot_json"]) if row["snapshot_json"] is not None else None
        )
        assessment = snapshot.get("assessment", {}) if snapshot else {}
        provenance = _snapshot_provenance(snapshot) if snapshot else {}
        grounding = provenance.get("grounding") or {}
        group = grouped.setdefault(
            run_id,
            {
                "run_id": str(run_id),
                "kind": str(row["kind"]),
                "status": str(row["status"]),
                "current": run_id == row["current_analysis_run_id"],
                "occurred_at": row["occurred_at"].isoformat(),
                "confidence_band": assessment.get("confidence_band"),
                "grounded_load_bearing": int(grounding.get("grounded", 0)),
                "total_load_bearing": int(grounding.get("total", 0)),
                "confidence_direction": assessment.get("confidence_direction"),
                "understanding_stage": assessment.get("understanding_stage"),
                "changes": (
                    _change_labels(snapshot, previous_by_run.get(run_id))
                    if snapshot
                    else [{"label": "Run did not publish", "tone": "warning"}]
                ),
                "events": [],
            },
        )
        group["events"].append(
            {
                "id": row["id"],
                "category": str(row["category"]),
                "event_type": row["event_type"],
                "summary": row["summary"],
                "detail": row["detail"],
                "actor_type": row["actor_type"],
                "artifact_type": (
                    str(row["artifact_type"]) if row["artifact_type"] else None
                ),
                "artifact_version": row["artifact_version"],
                "issue_id": row["issue_stable_key"],
                "occurred_at": row["occurred_at"].isoformat(),
            }
        )

    if not page_rows and cursor is None:
        synthetic_event_id = -1
        for row in reversed(snapshots):
            run_id = row["analysis_run_id"]
            snapshot = dict(row["snapshot_json"])
            assessment = snapshot.get("assessment", {})
            issues = [
                issue
                for issue in assessment.get("issues", [])
                if issue.get("status") != "resolved"
            ]
            artifacts = snapshot.get("artifacts", [])
            run_label = "Initial" if str(row["kind"]) == "initial" else "Extended"
            published_at = row["published_at"].isoformat()
            fallback_events = [
                {
                    "id": synthetic_event_id,
                    "category": "analysis",
                    "event_type": f"analysis.{str(row['kind'])}_completed",
                    "summary": f"{run_label} Analysis complete",
                    "detail": "The retained evidence-qualified read is available.",
                    "actor_type": "oslo",
                    "artifact_type": None,
                    "artifact_version": None,
                    "issue_id": None,
                    "occurred_at": published_at,
                },
                {
                    "id": synthetic_event_id - 1,
                    "category": "issues",
                    "event_type": "issues.reconciled",
                    "summary": f"{len(issues)} issues detected",
                    "detail": (
                        f"{len(issues)} open issues are retained in this project read."
                    ),
                    "actor_type": "system",
                    "artifact_type": None,
                    "artifact_version": None,
                    "issue_id": None,
                    "occurred_at": published_at,
                },
                {
                    "id": synthetic_event_id - 2,
                    "category": "versions",
                    "event_type": "artifacts.versions_retained",
                    "summary": (
                        f"{len(artifacts)} plan-artifact versions retained"
                    ),
                    "detail": " · ".join(
                        str(artifact.get("title") or artifact.get("artifact_type", ""))
                        for artifact in artifacts
                    ),
                    "actor_type": "system",
                    "artifact_type": None,
                    "artifact_version": None,
                    "issue_id": None,
                    "occurred_at": published_at,
                },
            ]
            synthetic_event_id -= 3
            visible_events = (
                fallback_events
                if category == "all"
                else [
                    event
                    for event in fallback_events
                    if event["category"] == category
                ]
            )
            if not visible_events:
                continue
            grouped[run_id] = {
                "run_id": str(run_id),
                "kind": str(row["kind"]),
                "status": str(row["status"]),
                "current": run_id == row["current_analysis_run_id"],
                "occurred_at": published_at,
                "confidence_band": assessment.get("confidence_band"),
                "grounded_load_bearing": int(
                    (_snapshot_provenance(snapshot).get("grounding") or {}).get(
                        "grounded", 0
                    )
                ),
                "total_load_bearing": int(
                    (_snapshot_provenance(snapshot).get("grounding") or {}).get(
                        "total", 0
                    )
                ),
                "confidence_direction": assessment.get("confidence_direction"),
                "understanding_stage": assessment.get("understanding_stage"),
                "changes": _change_labels(
                    snapshot,
                    previous_by_run.get(run_id),
                ),
                "events": visible_events,
            }

    trend: list[dict] = []
    previous = None
    for row in snapshots:
        snapshot = dict(row["snapshot_json"])
        assessment = snapshot.get("assessment", {})
        changes = _change_labels(snapshot, previous)
        provenance = _snapshot_provenance(snapshot)
        grounding = provenance.get("grounding") or {}
        grounded_load_bearing = int(grounding.get("grounded", 0))
        total_load_bearing = int(grounding.get("total", 0))
        trend.append(
            {
                "run_id": str(row["analysis_run_id"]),
                "confidence_band": assessment.get("confidence_band", "Low"),
                "grounded_load_bearing": grounded_load_bearing,
                "total_load_bearing": total_load_bearing,
                "direction": assessment.get("confidence_direction", "unchanged"),
                "cause": changes[0]["label"],
                "occurred_at": row["published_at"].isoformat(),
                "current": row["analysis_run_id"] == row["current_analysis_run_id"],
            }
        )
        previous = snapshot

    next_cursor = None
    if has_more and page_rows:
        last = page_rows[-1]
        next_cursor = _encode_cursor(last["occurred_at"], last["id"])
    return {
        "project_id": str(project_id),
        "groups": list(grouped.values()),
        "trend": trend,
        "resolution_identity_audits": build_resolution_identity_audits(identity_rows),
        "next_cursor": next_cursor,
    }

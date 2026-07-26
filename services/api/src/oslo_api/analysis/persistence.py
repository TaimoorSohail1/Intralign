import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from hashlib import sha256
from time import monotonic, sleep
from urllib.parse import quote
from uuid import UUID, uuid4

from sqlalchemy import Connection, Engine, text

from oslo_api.analysis.history import append_history_event
from oslo_api.analysis.models import (
    AnalysisEvent,
    AnalysisPhase,
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    Artifact,
    ArtifactType,
    Assessment,
    AssessmentSnapshot,
    EvidenceCitation,
    EvidenceFragment,
    Issue,
    Perception,
    ReliabilityBasis,
    RunKind,
)


def evidence_reference(
    *,
    document_id: UUID,
    ordinal: int,
    locator: dict[str, object],
) -> str:
    """Create a stable evidence URI without losing source-format location."""

    prefix = f"document:{document_id}"
    kind = locator.get("kind")
    if kind == "docx_section":
        location = f"section:{quote(str(locator.get('section', 'Document')), safe='')}"
    elif kind == "pptx_slide":
        location = f"slide:{locator.get('slide', 1)}"
    elif kind == "xlsx_range":
        sheet = quote(str(locator.get("sheet", "Sheet")), safe="")
        cell_range = quote(str(locator.get("cell_range", "A1")), safe="")
        location = f"sheet:{sheet}:range:{cell_range}"
    else:
        location = f"page:{locator.get('page', 1)}"
    return f"{prefix}:{location}:fragment:{ordinal}"


def evidence_location(locator: dict[str, object]) -> str:
    kind = locator.get("kind")
    if kind == "docx_section":
        return f"Section: {locator.get('section', 'Document')}"
    if kind == "pptx_slide":
        return f"Slide {locator.get('slide', 1)}"
    if kind == "xlsx_range":
        return (
            f"Sheet: {locator.get('sheet', 'Sheet')} · "
            f"{locator.get('cell_range', 'A1')}"
        )
    return f"Page {locator.get('page', 1)}"


def _json_default(value):
    if isinstance(value, (UUID, datetime)):
        return str(value)
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def _state_json(state: dict[str, object]) -> dict[str, object]:
    def encode(value):
        if is_dataclass(value):
            return asdict(value)
        if hasattr(value, "value"):
            return value.value
        if isinstance(value, (UUID, datetime)):
            return str(value)
        raise TypeError(f"Unsupported checkpoint value: {type(value)!r}")

    return json.loads(json.dumps(state, default=encode, sort_keys=True))


def _restore_state(payload: dict[str, object]) -> dict[str, object]:
    restored: dict[str, object] = {}
    harness_calls = payload.get("harness_calls")
    if isinstance(harness_calls, dict):
        restored["harness_calls"] = harness_calls
    perception_data = payload.get("perception")
    if isinstance(perception_data, dict):
        restored["perception"] = Perception(
            facts=tuple(perception_data.get("facts", [])),
            claims=tuple(perception_data.get("claims", [])),
            gaps=tuple(perception_data.get("gaps", [])),
            evidence_refs=tuple(perception_data.get("evidence_refs", [])),
            evidence=tuple(
                EvidenceFragment(
                    reference=item["reference"],
                    content=item["content"],
                    source_name=item.get("source_name"),
                    location=item.get("location"),
                )
                for item in perception_data.get("evidence", [])
            ),
        )
    artifact_data = payload.get("artifacts")
    if isinstance(artifact_data, list):
        restored["artifacts"] = tuple(_artifact_from_dict(item) for item in artifact_data)
    assessment_data = payload.get("assessment")
    if isinstance(assessment_data, dict):
        restored["assessment"] = _assessment_from_dict(assessment_data)
    return restored


def _artifact_from_dict(data: dict) -> Artifact:
    return Artifact(
        artifact_type=ArtifactType(data["artifact_type"]),
        title=data["title"],
        summary=data["summary"],
        reliability=data["reliability"],
        evidence_refs=tuple(data["evidence_refs"]),
        basis=data.get("basis", "derived"),
    )


def _issue_from_dict(data: dict) -> Issue:
    return Issue(
        id=data["id"],
        artifact_type=ArtifactType(data["artifact_type"]),
        dimension=data["dimension"],
        severity=data["severity"],
        title=data["title"],
        why=data["why"],
        recommendation=data["recommendation"],
        evidence_refs=tuple(data["evidence_refs"]),
        clarification=data.get("clarification"),
        status=data.get("status", "open"),
    )


def _assessment_from_dict(data: dict) -> Assessment:
    basis = data.get("reliability_basis", {})
    return Assessment(
        confidence_index=data["confidence_index"],
        confidence_band=data["confidence_band"],
        reliability=data["reliability"],
        clarity=data["clarity"],
        alignment=data["alignment"],
        feasibility=data["feasibility"],
        issues=tuple(_issue_from_dict(issue) for issue in data["issues"]),
        understanding_stage=data.get("understanding_stage", "orientation"),
        reliability_basis=ReliabilityBasis(
            coverage=basis.get("coverage", "Low"),
            evidence=basis.get("evidence", "Low"),
            assessability=basis.get("assessability", "Low"),
        ),
        confidence_direction=data.get("confidence_direction", "unchanged"),
        limiting_dimension=data.get("limiting_dimension", "feasibility"),
        false_confidence=data.get("false_confidence", False),
        confidence_explanation=data.get("confidence_explanation", ""),
        resolved_issue_count=data.get("resolved_issue_count", 0),
        confirmed_dependency_count=data.get("confirmed_dependency_count", 0),
    )


def _snapshot_dict(snapshot: AssessmentSnapshot) -> dict:
    return json.loads(json.dumps(asdict(snapshot), default=_json_default))


def _snapshot_from_dict(data: dict) -> AssessmentSnapshot:
    return AssessmentSnapshot(
        id=UUID(data["id"]),
        analysis_run_id=UUID(data["analysis_run_id"]),
        workspace_id=UUID(data["workspace_id"]),
        project_id=UUID(data["project_id"]),
        state=data["state"],
        summary=data["summary"],
        artifacts=tuple(_artifact_from_dict(item) for item in data["artifacts"]),
        assessment=_assessment_from_dict(data["assessment"]),
        published_at=datetime.fromisoformat(data["published_at"]),
        evidence_citations=tuple(
            EvidenceCitation(
                reference=item["reference"],
                source_name=item["source_name"],
                location=item["location"],
                excerpt=item["excerpt"],
            )
            for item in data.get("evidence_citations", [])
        ),
    )


class DatabaseAnalysisStore:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def create_run(self, request: AnalysisRunRequest) -> AnalysisRun:
        run_id = uuid4()
        key = request.idempotency_key or str(run_id)
        with self._engine.begin() as connection:
            inserted = connection.execute(
                text(
                    """
                    insert into public.analysis_runs (
                      id, workspace_id, project_id, requested_by, kind, status,
                      description, source_names, source_document_ids,
                      idempotency_key, parent_run_id
                    ) values (
                      :id, :workspace_id, :project_id, :requested_by, :kind, 'queued',
                      :description, cast(:source_names as jsonb),
                      cast(:source_document_ids as jsonb), :key, :parent_run_id
                    )
                    on conflict (workspace_id, idempotency_key) do nothing
                    returning id
                    """
                ),
                {
                    "id": run_id,
                    "workspace_id": request.workspace_id,
                    "project_id": request.project_id,
                    "requested_by": request.requested_by,
                    "kind": request.kind.value,
                    "description": request.description,
                    "source_names": json.dumps(request.source_names),
                    "source_document_ids": json.dumps(
                        [str(document_id) for document_id in request.source_document_ids]
                    ),
                    "key": key,
                    "parent_run_id": request.parent_run_id,
                },
            ).scalar_one_or_none()
            actual_id = (
                inserted
                or connection.execute(
                    text(
                        """
                    select id from public.analysis_runs
                    where workspace_id = :workspace_id and idempotency_key = :key
                    """
                    ),
                    {"workspace_id": request.workspace_id, "key": key},
                ).scalar_one()
            )
            if inserted:
                self._append_event(
                    connection,
                    actual_id,
                    "analysis.queued",
                    AnalysisRunStatus.QUEUED,
                )
        run = self.get_run(actual_id)
        if run is None:
            raise RuntimeError("ANALYSIS_RUN_CREATE_FAILED")
        return run

    def get_run(self, run_id: UUID) -> AnalysisRun | None:
        with self._engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        select id, workspace_id, project_id, requested_by, kind, status,
                               description, source_names, source_document_ids,
                               idempotency_key, parent_run_id,
                               current_phase, error_code, created_at, updated_at
                        from public.analysis_runs where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                return None
            completed = connection.execute(
                text(
                    """
                    select phase from public.analysis_run_events
                    where analysis_run_id = :run_id
                      and event_type = 'analysis.phase_completed'
                    order by sequence_no
                    """
                ),
                {"run_id": run_id},
            ).scalars()
            checkpoint = (
                connection.execute(
                    text(
                        """
                        select state_json from public.analysis_checkpoints
                        where analysis_run_id = :run_id
                        order by created_at desc limit 1
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
            snapshot_row = (
                connection.execute(
                    text(
                        """
                        select snapshot_json from public.assessment_snapshots
                        where analysis_run_id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one_or_none()
            )
        request = AnalysisRunRequest(
            workspace_id=row["workspace_id"],
            project_id=row["project_id"],
            requested_by=row["requested_by"],
            kind=RunKind(row["kind"]),
            description=row["description"],
            source_names=tuple(row["source_names"]),
            source_document_ids=tuple(
                UUID(document_id) for document_id in row["source_document_ids"]
            ),
            idempotency_key=row["idempotency_key"],
            parent_run_id=row["parent_run_id"],
        )
        return AnalysisRun(
            id=row["id"],
            request=request,
            status=AnalysisRunStatus(row["status"]),
            current_phase=AnalysisPhase(row["current_phase"]) if row["current_phase"] else None,
            completed_phases=[AnalysisPhase(phase) for phase in completed if phase],
            checkpoint_state=_restore_state(checkpoint["state_json"]) if checkpoint else {},
            error_code=row["error_code"],
            snapshot=_snapshot_from_dict(snapshot_row["snapshot_json"]) if snapshot_row else None,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def latest_run_for_project(
        self,
        project_id: UUID,
        kind: RunKind,
    ) -> AnalysisRun | None:
        with self._engine.connect() as connection:
            run_id = connection.execute(
                text(
                    """
                    select id
                    from public.analysis_runs
                    where project_id = :project_id and kind = :kind
                    order by created_at desc, id desc
                    limit 1
                    """
                ),
                {"project_id": project_id, "kind": kind.value},
            ).scalar_one_or_none()
        return self.get_run(run_id) if run_id else None

    def evidence_for(self, request: AnalysisRunRequest) -> tuple[EvidenceFragment, ...]:
        if not request.source_document_ids:
            return ()
        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select fragment.source_document_id, fragment.ordinal,
                               fragment.content, fragment.locator,
                               document.file_name
                        from public.source_fragments fragment
                        join public.source_documents document
                          on document.id = fragment.source_document_id
                         and document.workspace_id = fragment.workspace_id
                        where fragment.workspace_id = :workspace_id
                          and fragment.project_id = :project_id
                          and fragment.source_document_id = any(:document_ids)
                        order by fragment.source_document_id, fragment.ordinal
                        """
                    ),
                    {
                        "workspace_id": request.workspace_id,
                        "project_id": request.project_id,
                        "document_ids": list(request.source_document_ids),
                    },
                )
                .mappings()
                .all()
            )
        return tuple(
            EvidenceFragment(
                reference=evidence_reference(
                    document_id=row["source_document_id"],
                    ordinal=row["ordinal"],
                    locator=row["locator"],
                ),
                content=row["content"],
                source_name=row["file_name"],
                location=evidence_location(row["locator"]),
            )
            for row in rows
        )

    def start_run(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'running', started_at = coalesce(started_at, now()),
                        error_code = null, updated_at = now()
                    where id = :run_id and status <> 'completed'
                    """
                ),
                {"run_id": run_id},
            )
            self._append_event(
                connection,
                run_id,
                "analysis.started",
                AnalysisRunStatus.RUNNING,
            )

    def start_phase(self, run_id: UUID, phase: AnalysisPhase) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set current_phase = :phase, updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id, "phase": phase.value},
            )
            attempt = connection.execute(
                text(
                    """
                    select coalesce(max(attempt_no), 0) + 1
                    from public.analysis_node_attempts
                    where analysis_run_id = :run_id and phase = :phase
                    """
                ),
                {"run_id": run_id, "phase": phase.value},
            ).scalar_one()
            workspace_id = self._workspace_id(connection, run_id)
            connection.execute(
                text(
                    """
                    insert into public.analysis_node_attempts (
                      workspace_id, analysis_run_id, phase, attempt_no, status
                    ) values (:workspace_id, :run_id, :phase, :attempt, 'running')
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "run_id": run_id,
                    "phase": phase.value,
                    "attempt": attempt,
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.phase_started",
                self._run_status(connection, run_id),
                phase,
            )

    def complete_phase(
        self,
        run_id: UUID,
        phase: AnalysisPhase,
        checkpoint_state: dict[str, object] | None = None,
    ) -> None:
        state = _state_json(checkpoint_state or {})
        state_text = json.dumps(state, sort_keys=True, separators=(",", ":"))
        harness_calls = state.get("harness_calls", {})
        call_metadata = harness_calls.get(phase.value) if isinstance(harness_calls, dict) else None
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.analysis_node_attempts
                    set status = 'completed', completed_at = now(),
                        provider = :provider,
                        model_id = :model_id,
                        prompt_version = :prompt_version,
                        provider_response_id = :provider_response_id,
                        input_tokens = :input_tokens,
                        output_tokens = :output_tokens,
                        duration_ms = :duration_ms,
                        execution_mode = :execution_mode,
                        fallback_reason = :fallback_reason
                    where id = (
                      select id from public.analysis_node_attempts
                      where analysis_run_id = :run_id and phase = :phase
                      order by attempt_no desc limit 1
                    )
                    """
                ),
                {
                    "run_id": run_id,
                    "phase": phase.value,
                    "provider": (
                        call_metadata.get("provider") if isinstance(call_metadata, dict) else None
                    ),
                    "model_id": (
                        call_metadata.get("model") if isinstance(call_metadata, dict) else None
                    ),
                    "prompt_version": (
                        call_metadata.get("prompt_version")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "provider_response_id": (
                        call_metadata.get("response_id")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "input_tokens": (
                        call_metadata.get("input_tokens")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "output_tokens": (
                        call_metadata.get("output_tokens")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "duration_ms": (
                        call_metadata.get("duration_ms")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                    "execution_mode": (
                        call_metadata.get("mode") if isinstance(call_metadata, dict) else None
                    ),
                    "fallback_reason": (
                        call_metadata.get("fallback_reason")
                        if isinstance(call_metadata, dict)
                        else None
                    ),
                },
            )
            if isinstance(call_metadata, dict):
                connection.execute(
                    text(
                        """
                        update public.analysis_runs
                        set prompt_versions = prompt_versions ||
                              jsonb_build_object(
                                cast(:phase as text),
                                cast(:prompt_version as text)
                              ),
                            model_versions = model_versions ||
                              jsonb_build_object(
                                cast(:phase as text),
                                cast(:model_id as text)
                              ),
                            updated_at = now()
                        where id = :run_id
                        """
                    ),
                    {
                        "run_id": run_id,
                        "phase": phase.value,
                        "prompt_version": call_metadata.get("prompt_version"),
                        "model_id": call_metadata.get("model"),
                    },
                )
            workspace_id = self._workspace_id(connection, run_id)
            completed = connection.execute(
                text(
                    """
                    select coalesce(jsonb_agg(phase order by sequence_no), '[]'::jsonb)
                    from public.analysis_run_events
                    where analysis_run_id = :run_id
                      and event_type = 'analysis.phase_completed'
                    """
                ),
                {"run_id": run_id},
            ).scalar_one()
            completed = list(completed) + [phase.value]
            connection.execute(
                text(
                    """
                    insert into public.analysis_checkpoints (
                      workspace_id, analysis_run_id, checkpoint_key, completed_phases,
                      state_json, state_hash, graph_version
                    ) values (
                      :workspace_id, :run_id, :key, cast(:completed as jsonb),
                      cast(:state as jsonb), :state_hash, 'slice2-graph-v1'
                    )
                    on conflict (analysis_run_id, checkpoint_key) do update set
                      completed_phases = excluded.completed_phases,
                      state_json = excluded.state_json,
                      state_hash = excluded.state_hash,
                      created_at = now()
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "run_id": run_id,
                    "key": phase.value,
                    "completed": json.dumps(completed),
                    "state": state_text,
                    "state_hash": sha256(state_text.encode()).hexdigest(),
                },
            )
            self._append_event(
                connection,
                run_id,
                "analysis.phase_completed",
                self._run_status(connection, run_id),
                phase,
            )

    def publish(self, run_id: UUID, snapshot: AssessmentSnapshot) -> None:
        payload = _snapshot_dict(snapshot)
        with self._engine.begin() as connection:
            run_row = (
                connection.execute(
                    text(
                        """
                        select kind
                        from public.analysis_runs
                        where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one()
            )
            previous_issue_keys = set(
                connection.execute(
                    text(
                        """
                        select stable_key
                        from public.issues
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and current_status <> 'resolved'
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                    },
                ).scalars()
            )
            connection.execute(
                text(
                    """
                    insert into public.assessment_snapshots (
                      id, workspace_id, project_id, analysis_run_id,
                      snapshot_state, snapshot_json, published_at
                    ) values (
                      :id, :workspace_id, :project_id, :run_id,
                      :state, cast(:snapshot as jsonb), :published_at
                    )
                    on conflict (analysis_run_id) do nothing
                    """
                ),
                {
                    "id": snapshot.id,
                    "workspace_id": snapshot.workspace_id,
                    "project_id": snapshot.project_id,
                    "run_id": run_id,
                    "state": snapshot.state,
                    "snapshot": json.dumps(payload),
                    "published_at": snapshot.published_at,
                },
            )
            for artifact in snapshot.artifacts:
                connection.execute(
                    text(
                        """
                        insert into public.artifact_versions (
                          workspace_id, project_id, analysis_run_id, artifact_type,
                          title, summary, reliability, basis, evidence_refs
                        ) values (
                          :workspace_id, :project_id, :run_id, :artifact_type,
                          :title, :summary, :reliability, :basis, cast(:evidence_refs as jsonb)
                        )
                        on conflict (analysis_run_id, artifact_type) do nothing
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "run_id": run_id,
                        "artifact_type": artifact.artifact_type.value,
                        "title": artifact.title,
                        "summary": artifact.summary,
                        "reliability": artifact.reliability,
                        "basis": artifact.basis,
                        "evidence_refs": json.dumps(artifact.evidence_refs),
                    },
                )
            # A completed snapshot is the authoritative issue read for the project.
            # Resolve rows that disappeared from the new read before upserting the
            # issues that are still present (which restores their exact status).
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = 'resolved', updated_at = now()
                    where project_id = :project_id
                      and current_status <> 'resolved'
                    """
                ),
                {"project_id": snapshot.project_id},
            )
            for issue in snapshot.assessment.issues:
                issue_id = connection.execute(
                    text(
                        """
                        insert into public.issues (
                          workspace_id, project_id, stable_key, current_status
                        ) values (
                          :workspace_id, :project_id, :stable_key, :status
                        )
                        on conflict (project_id, stable_key) do update set
                          current_status = excluded.current_status,
                          updated_at = now()
                        returning id
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "stable_key": issue.id,
                        "status": issue.status,
                    },
                ).scalar_one()
                connection.execute(
                    text(
                        """
                        insert into public.issue_observations (
                          workspace_id, project_id, issue_id, analysis_run_id,
                          artifact_type, dimension, severity, status,
                          observation_json
                        ) values (
                          :workspace_id, :project_id, :issue_id, :run_id,
                          :artifact_type, :dimension, :severity, :status,
                          cast(:observation as jsonb)
                        )
                        on conflict (analysis_run_id, issue_id) do nothing
                        """
                    ),
                    {
                        "workspace_id": snapshot.workspace_id,
                        "project_id": snapshot.project_id,
                        "issue_id": issue_id,
                        "run_id": run_id,
                        "artifact_type": issue.artifact_type.value,
                        "dimension": issue.dimension,
                        "severity": issue.severity,
                        "status": issue.status,
                        "observation": json.dumps(
                            {
                                "stable_key": issue.id,
                                "title": issue.title,
                                "why": issue.why,
                                "recommendation": issue.recommendation,
                                "clarification": issue.clarification,
                                "evidence_refs": issue.evidence_refs,
                            }
                        ),
                    },
                )
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'completed', completed_at = now(), updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id},
            )
            connection.execute(
                text(
                    """
                    update public.projects
                    set current_analysis_run_id = :run_id, status = 'active', updated_at = now()
                    where id = :project_id
                    """
                ),
                {"run_id": run_id, "project_id": snapshot.project_id},
            )
            self._append_event(
                connection,
                run_id,
                "assessment.published",
                AnalysisRunStatus.COMPLETED,
                payload={"snapshot_id": str(snapshot.id), "state": snapshot.state},
            )
            run_kind = str(run_row["kind"])
            current_issue_keys = {
                issue.id
                for issue in snapshot.assessment.issues
                if issue.status != "resolved"
            }
            opened = sorted(current_issue_keys - previous_issue_keys)
            resolved = sorted(previous_issue_keys - current_issue_keys)
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="oslo",
                category="analysis",
                event_type=f"analysis.{run_kind}_completed",
                summary=(
                    "Initial Analysis complete"
                    if run_kind == "initial"
                    else "Extended Analysis complete"
                ),
                detail=(
                    "The first evidence-qualified read is available."
                    if run_kind == "initial"
                    else "The deeper evidence read is now the current trusted view."
                ),
                idempotency_key=f"history:analysis-completed:{run_id}",
                payload={
                    "snapshot_id": str(snapshot.id),
                    "confidence_index": snapshot.assessment.confidence_index,
                    "confidence_band": snapshot.assessment.confidence_band,
                    "clarity": snapshot.assessment.clarity,
                    "alignment": snapshot.assessment.alignment,
                    "feasibility": snapshot.assessment.feasibility,
                },
            )
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="system",
                category="issues",
                event_type="issues.reconciled",
                summary=f"{len(current_issue_keys)} issues detected",
                detail=(
                    f"{len(opened)} opened and {len(resolved)} resolved in this read."
                ),
                idempotency_key=f"history:issues-reconciled:{run_id}",
                payload={"opened": opened, "resolved": resolved},
            )
            append_history_event(
                connection,
                workspace_id=snapshot.workspace_id,
                project_id=snapshot.project_id,
                analysis_run_id=run_id,
                actor_type="system",
                category="versions",
                event_type="artifacts.versions_retained",
                summary=f"{len(snapshot.artifacts)} plan-artifact versions retained",
                detail="A read-only version of every plan artifact was retained.",
                idempotency_key=f"history:artifact-versions:{run_id}",
                payload={
                    "artifact_types": [
                        artifact.artifact_type.value for artifact in snapshot.artifacts
                    ]
                },
            )

    def complete_run(self, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            already_completed = connection.execute(
                text(
                    """
                    select exists(
                      select 1 from public.analysis_run_events
                      where analysis_run_id = :run_id
                        and event_type = 'analysis.completed'
                    )
                    """
                ),
                {"run_id": run_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'completed', completed_at = coalesce(completed_at, now()),
                        updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id},
            )
            if not already_completed:
                self._append_event(
                    connection,
                    run_id,
                    "analysis.completed",
                    AnalysisRunStatus.COMPLETED,
                )

    def fail(
        self,
        run_id: UUID,
        *,
        error_code: str,
        phase: AnalysisPhase,
        retryable: bool = True,
    ) -> None:
        safe_code = error_code[:120]
        with self._engine.begin() as connection:
            run_context = (
                connection.execute(
                    text(
                        """
                        select workspace_id, project_id
                        from public.analysis_runs
                        where id = :run_id
                        """
                    ),
                    {"run_id": run_id},
                )
                .mappings()
                .one()
            )
            connection.execute(
                text(
                    """
                    update public.analysis_runs
                    set status = 'failed', error_code = :error_code,
                        current_phase = :phase, completed_at = now(), updated_at = now()
                    where id = :run_id
                    """
                ),
                {"run_id": run_id, "error_code": safe_code, "phase": phase.value},
            )
            connection.execute(
                text(
                    """
                    update public.analysis_node_attempts
                    set status = 'failed', safe_error_code = :error_code, completed_at = now()
                    where id = (
                      select id from public.analysis_node_attempts
                      where analysis_run_id = :run_id and phase = :phase
                      order by attempt_no desc limit 1
                    )
                    """
                ),
                {"run_id": run_id, "phase": phase.value, "error_code": safe_code},
            )
            self._append_event(
                connection,
                run_id,
                "analysis.failed",
                AnalysisRunStatus.FAILED,
                phase,
                {"code": safe_code, "retryable": retryable},
            )
            append_history_event(
                connection,
                workspace_id=run_context["workspace_id"],
                project_id=run_context["project_id"],
                analysis_run_id=run_id,
                actor_type="system",
                category="analysis",
                event_type="analysis.failed",
                summary="Analysis did not complete",
                detail="The last-good project read remains current and can be retried.",
                idempotency_key=f"history:analysis-failed:{run_id}",
                payload={
                    "phase": phase.value,
                    "error_code": safe_code,
                    "retryable": retryable,
                },
            )

    def current_snapshot(self, project_id: UUID) -> AssessmentSnapshot | None:
        with self._engine.connect() as connection:
            payload = connection.execute(
                text(
                    """
                    select snapshot.snapshot_json
                    from public.projects project
                    join public.assessment_snapshots snapshot
                      on snapshot.analysis_run_id = project.current_analysis_run_id
                    where project.id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).scalar_one_or_none()
        return _snapshot_from_dict(payload) if payload else None

    def snapshot_for_run(self, run_id: UUID) -> AssessmentSnapshot | None:
        with self._engine.connect() as connection:
            payload = connection.execute(
                text(
                    """
                    select snapshot_json
                    from public.assessment_snapshots
                    where analysis_run_id = :run_id
                    """
                ),
                {"run_id": run_id},
            ).scalar_one_or_none()
        return _snapshot_from_dict(payload) if payload else None

    def events_after(self, run_id: UUID, sequence: int) -> tuple[AnalysisEvent, ...]:
        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select analysis_run_id, sequence_no, event_type, status,
                               phase, payload, occurred_at
                        from public.analysis_run_events
                        where analysis_run_id = :run_id and sequence_no > :sequence
                        order by sequence_no
                        """
                    ),
                    {"run_id": run_id, "sequence": sequence},
                )
                .mappings()
                .all()
            )
        return tuple(
            AnalysisEvent(
                run_id=row["analysis_run_id"],
                sequence=row["sequence_no"],
                event_type=row["event_type"],
                status=row["status"],
                phase=AnalysisPhase(row["phase"]) if row["phase"] else None,
                occurred_at=row["occurred_at"],
                error_code=row["payload"].get("code"),
                retryable=row["payload"].get("retryable"),
            )
            for row in rows
        )

    def wait_for_events(
        self,
        run_id: UUID,
        sequence: int,
        timeout: float,
    ) -> tuple[AnalysisEvent, ...]:
        deadline = monotonic() + timeout
        while monotonic() < deadline:
            events = self.events_after(run_id, sequence)
            if events:
                return events
            sleep(0.2)
        return ()

    @staticmethod
    def _workspace_id(connection: Connection, run_id: UUID) -> UUID:
        return connection.execute(
            text("select workspace_id from public.analysis_runs where id = :run_id"),
            {"run_id": run_id},
        ).scalar_one()

    @staticmethod
    def _run_status(connection: Connection, run_id: UUID) -> AnalysisRunStatus:
        status = connection.execute(
            text("select status from public.analysis_runs where id = :run_id"),
            {"run_id": run_id},
        ).scalar_one()
        return AnalysisRunStatus(status)

    def _append_event(
        self,
        connection: Connection,
        run_id: UUID,
        event_type: str,
        status: AnalysisRunStatus,
        phase: AnalysisPhase | None = None,
        payload: dict | None = None,
    ) -> None:
        run = (
            connection.execute(
                text(
                    """
                    select workspace_id, project_id from public.analysis_runs
                    where id = :run_id for update
                    """
                ),
                {"run_id": run_id},
            )
            .mappings()
            .one()
        )
        sequence = connection.execute(
            text(
                """
                select coalesce(max(sequence_no), 0) + 1
                from public.analysis_run_events where analysis_run_id = :run_id
                """
            ),
            {"run_id": run_id},
        ).scalar_one()
        event_payload = payload or {}
        connection.execute(
            text(
                """
                insert into public.analysis_run_events (
                  workspace_id, project_id, analysis_run_id, sequence_no,
                  event_type, phase, status, payload
                ) values (
                  :workspace_id, :project_id, :run_id, :sequence,
                  :event_type, :phase, :status, cast(:payload as jsonb)
                )
                """
            ),
            {
                "workspace_id": run["workspace_id"],
                "project_id": run["project_id"],
                "run_id": run_id,
                "sequence": sequence,
                "event_type": event_type,
                "phase": phase.value if phase else None,
                "status": status.value,
                "payload": json.dumps(event_payload),
            },
        )
        connection.execute(
            text(
                """
                insert into public.outbox_events (
                  workspace_id, aggregate_type, aggregate_id, event_type, payload
                ) values (
                  :workspace_id, 'analysis_run', :run_id, :event_type,
                  cast(:payload as jsonb)
                )
                """
            ),
            {
                "workspace_id": run["workspace_id"],
                "run_id": run_id,
                "event_type": event_type,
                "payload": json.dumps({"sequence": sequence, **event_payload}),
            },
        )

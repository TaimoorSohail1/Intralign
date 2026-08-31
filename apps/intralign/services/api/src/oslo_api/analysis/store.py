from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime
from threading import Condition, RLock
from typing import Protocol
from uuid import UUID

from oslo_api.analysis.models import (
    AnalysisEvent,
    AnalysisPhase,
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    Artifact,
    ArtifactType,
    AssessmentSnapshot,
    EvidenceFragment,
    HarnessCallMetadata,
    RunKind,
)


class AnalysisStore(Protocol):
    def create_run(self, request: AnalysisRunRequest) -> AnalysisRun: ...

    def get_run(self, run_id: UUID) -> AnalysisRun | None: ...

    def merge_queued_run(
        self,
        run_id: UUID,
        *,
        evidence: tuple[EvidenceFragment, ...],
        event_ids: tuple[UUID, ...],
    ) -> AnalysisRun: ...

    def withdraw_queued_event(
        self,
        run_id: UUID,
        *,
        event_id: UUID,
        evidence_references: tuple[str, ...],
    ) -> AnalysisRun: ...

    def latest_run_for_project(
        self,
        project_id: UUID,
        kind: RunKind,
    ) -> AnalysisRun | None: ...

    def start_run(self, run_id: UUID) -> None: ...

    def queue_run(self, run_id: UUID) -> None: ...

    def queue_auto_retry(self, run_id: UUID) -> AnalysisRun: ...

    def start_phase(self, run_id: UUID, phase: AnalysisPhase) -> None: ...

    def complete_phase(
        self,
        run_id: UUID,
        phase: AnalysisPhase,
        checkpoint_state: dict[str, object] | None = None,
    ) -> None: ...

    def publish(self, run_id: UUID, snapshot: AssessmentSnapshot) -> None: ...

    def complete_run(self, run_id: UUID) -> None: ...

    def fail(
        self,
        run_id: UUID,
        *,
        error_code: str,
        phase: AnalysisPhase,
        retryable: bool = True,
    ) -> None: ...

    def current_snapshot(self, project_id: UUID) -> AssessmentSnapshot | None: ...

    def events_after(self, run_id: UUID, sequence: int) -> tuple[AnalysisEvent, ...]: ...

    def evidence_for(self, request: AnalysisRunRequest) -> tuple[EvidenceFragment, ...]: ...

    def completed_artifacts(self, run_id: UUID) -> dict[ArtifactType, Artifact]: ...

    def start_artifact_job(self, run_id: UUID, artifact_type: ArtifactType) -> None: ...

    def complete_artifact_job(
        self,
        run_id: UUID,
        artifact: Artifact,
        metadata: HarnessCallMetadata | None = None,
    ) -> None: ...

    def fail_artifact_job(
        self,
        run_id: UUID,
        artifact_type: ArtifactType,
        *,
        error_code: str,
        retryable: bool,
    ) -> None: ...


class InMemoryAnalysisStore:
    def __init__(self) -> None:
        self._runs: dict[UUID, AnalysisRun] = {}
        self._events: dict[UUID, list[AnalysisEvent]] = {}
        self._current_snapshots: dict[UUID, AssessmentSnapshot] = {}
        self._idempotency: dict[tuple[UUID, str], UUID] = {}
        self._artifact_jobs: dict[UUID, dict[ArtifactType, Artifact]] = {}
        self._lock = RLock()
        self._condition = Condition(self._lock)

    def create_run(self, request: AnalysisRunRequest) -> AnalysisRun:
        with self._condition:
            if request.idempotency_key:
                existing_id = self._idempotency.get((request.workspace_id, request.idempotency_key))
                if existing_id:
                    return deepcopy(self._runs[existing_id])
            run = AnalysisRun.queued(request)
            self._runs[run.id] = run
            self._events[run.id] = []
            self._artifact_jobs[run.id] = {}
            if request.idempotency_key:
                self._idempotency[(request.workspace_id, request.idempotency_key)] = run.id
            self._append_event(run, "analysis.queued", AnalysisRunStatus.QUEUED.value)
            return deepcopy(run)

    def get_run(self, run_id: UUID) -> AnalysisRun | None:
        with self._lock:
            run = self._runs.get(run_id)
            return deepcopy(run) if run else None

    def merge_queued_run(
        self,
        run_id: UUID,
        *,
        evidence: tuple[EvidenceFragment, ...],
        event_ids: tuple[UUID, ...],
    ) -> AnalysisRun:
        with self._condition:
            run = self._runs[run_id]
            if run.status is not AnalysisRunStatus.QUEUED:
                raise ValueError("Only a queued analysis run can accept another change")
            run.request = replace(
                run.request,
                user_evidence=run.request.user_evidence + evidence,
                consolidated_event_ids=tuple(
                    dict.fromkeys((*run.request.consolidated_event_ids, *event_ids))
                ),
            )
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.batch_extended", run.status.value)
            return deepcopy(run)

    def withdraw_queued_event(
        self,
        run_id: UUID,
        *,
        event_id: UUID,
        evidence_references: tuple[str, ...],
    ) -> AnalysisRun:
        with self._condition:
            run = self._runs[run_id]
            if run.status is not AnalysisRunStatus.QUEUED:
                raise ValueError("Only a queued analysis run can withdraw a pending change")
            references = set(evidence_references)
            run.request = replace(
                run.request,
                user_evidence=tuple(
                    item for item in run.request.user_evidence if item.reference not in references
                ),
                consolidated_event_ids=tuple(
                    item for item in run.request.consolidated_event_ids if item != event_id
                ),
            )
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.pending_change_withdrawn", run.status.value)
            return deepcopy(run)

    def latest_run_for_project(
        self,
        project_id: UUID,
        kind: RunKind,
    ) -> AnalysisRun | None:
        with self._lock:
            matches = [
                run
                for run in self._runs.values()
                if run.request.project_id == project_id and run.request.kind is kind
            ]
            if not matches:
                return None
            return deepcopy(max(matches, key=lambda run: (run.created_at, str(run.id))))

    def start_run(self, run_id: UUID) -> None:
        with self._condition:
            run = self._runs[run_id]
            run.status = AnalysisRunStatus.RUNNING
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.started", run.status.value)

    def queue_run(self, run_id: UUID) -> None:
        with self._condition:
            run = self._runs[run_id]
            if run.status is AnalysisRunStatus.COMPLETED:
                return
            run.status = AnalysisRunStatus.QUEUED
            run.error_code = None
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.retry_queued", run.status.value)

    def queue_auto_retry(self, run_id: UUID) -> AnalysisRun:
        with self._condition:
            run = self._runs[run_id]
            if run.status is not AnalysisRunStatus.FAILED:
                raise ValueError("Only a failed analysis run can be automatically retried")
            if run.request.auto_retry_count >= 1:
                raise ValueError("The transient automatic retry has already been used")
            run.request = replace(run.request, auto_retry_count=1)
            run.status = AnalysisRunStatus.QUEUED
            run.error_code = None
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.auto_retry_queued", run.status.value)
            return deepcopy(run)

    def start_phase(self, run_id: UUID, phase: AnalysisPhase) -> None:
        with self._condition:
            run = self._runs[run_id]
            run.current_phase = phase
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.phase_started", run.status.value, phase)

    def complete_phase(
        self,
        run_id: UUID,
        phase: AnalysisPhase,
        checkpoint_state: dict[str, object] | None = None,
    ) -> None:
        with self._condition:
            run = self._runs[run_id]
            if phase not in run.completed_phases:
                run.completed_phases.append(phase)
            if checkpoint_state is not None:
                run.checkpoint_state = deepcopy(checkpoint_state)
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.phase_completed", run.status.value, phase)

    def publish(self, run_id: UUID, snapshot: AssessmentSnapshot) -> None:
        with self._condition:
            run = self._runs[run_id]
            run.status = AnalysisRunStatus.COMPLETED
            run.snapshot = snapshot
            run.updated_at = datetime.now(UTC)
            self._current_snapshots[snapshot.project_id] = snapshot
            self._append_event(run, "assessment.published", run.status.value)

    def complete_run(self, run_id: UUID) -> None:
        with self._condition:
            run = self._runs[run_id]
            run.status = AnalysisRunStatus.COMPLETED
            run.updated_at = datetime.now(UTC)
            self._append_event(run, "analysis.completed", run.status.value)

    def fail(
        self,
        run_id: UUID,
        *,
        error_code: str,
        phase: AnalysisPhase,
        retryable: bool = True,
    ) -> None:
        with self._condition:
            run = self._runs[run_id]
            run.status = AnalysisRunStatus.FAILED
            run.error_code = error_code
            run.current_phase = phase
            run.updated_at = datetime.now(UTC)
            self._append_event(
                run,
                "analysis.failed",
                run.status.value,
                phase,
                error_code=error_code,
                retryable=retryable,
            )

    def current_snapshot(self, project_id: UUID) -> AssessmentSnapshot | None:
        with self._lock:
            return deepcopy(self._current_snapshots.get(project_id))

    def evidence_for(self, request: AnalysisRunRequest) -> tuple[EvidenceFragment, ...]:
        return ()

    def completed_artifacts(self, run_id: UUID) -> dict[ArtifactType, Artifact]:
        with self._lock:
            return deepcopy(self._artifact_jobs.get(run_id, {}))

    def start_artifact_job(self, run_id: UUID, artifact_type: ArtifactType) -> None:
        with self._condition:
            run = self._runs[run_id]
            self._append_event(
                run,
                "analysis.artifact_started",
                run.status.value,
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                artifact_type=artifact_type,
            )

    def complete_artifact_job(
        self,
        run_id: UUID,
        artifact: Artifact,
        metadata: HarnessCallMetadata | None = None,
    ) -> None:
        del metadata
        with self._condition:
            run = self._runs[run_id]
            self._artifact_jobs.setdefault(run_id, {})[artifact.artifact_type] = deepcopy(artifact)
            self._append_event(
                run,
                "analysis.artifact_completed",
                run.status.value,
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                artifact_type=artifact.artifact_type,
            )

    def fail_artifact_job(
        self,
        run_id: UUID,
        artifact_type: ArtifactType,
        *,
        error_code: str,
        retryable: bool,
    ) -> None:
        with self._condition:
            run = self._runs[run_id]
            self._append_event(
                run,
                "analysis.artifact_failed",
                run.status.value,
                AnalysisPhase.CONSTRUCT_ARTIFACTS,
                artifact_type=artifact_type,
                error_code=error_code,
                retryable=retryable,
            )

    def events_after(self, run_id: UUID, sequence: int) -> tuple[AnalysisEvent, ...]:
        with self._lock:
            return tuple(
                deepcopy(event)
                for event in self._events.get(run_id, ())
                if event.sequence > sequence
            )

    def wait_for_events(
        self,
        run_id: UUID,
        sequence: int,
        timeout: float,
    ) -> tuple[AnalysisEvent, ...]:
        with self._condition:
            events = self.events_after(run_id, sequence)
            if events:
                return events
            self._condition.wait(timeout)
            return self.events_after(run_id, sequence)

    def _append_event(
        self,
        run: AnalysisRun,
        event_type: str,
        status: str,
        phase: AnalysisPhase | None = None,
        *,
        error_code: str | None = None,
        retryable: bool | None = None,
        artifact_type: ArtifactType | None = None,
    ) -> None:
        event = AnalysisEvent(
            run_id=run.id,
            sequence=len(self._events[run.id]) + 1,
            event_type=event_type,
            status=status,
            phase=phase,
            error_code=error_code,
            retryable=retryable,
            artifact_type=artifact_type,
        )
        self._events[run.id].append(event)
        self._condition.notify_all()

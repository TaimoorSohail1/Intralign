from dataclasses import asdict
from datetime import UTC, datetime
from time import sleep
from typing import TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from oslo_api.analysis.harness import AgentHarness, AgentHarnessError
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisRunResult,
    AnalysisRunStatus,
    AssessmentSnapshot,
    HarnessInvocation,
    RunKind,
)
from oslo_api.analysis.store import AnalysisStore


class _GraphState(TypedDict):
    run_id: object


class AnalysisWorkflow:
    def __init__(
        self,
        *,
        store: AnalysisStore,
        harness: AgentHarness,
        phase_delay_seconds: float = 0,
    ) -> None:
        self._store = store
        self._harness = harness
        self._phase_delay_seconds = phase_delay_seconds
        builder = StateGraph(_GraphState)
        phases = tuple(AnalysisPhase)
        for phase in phases:
            builder.add_node(
                phase.value,
                lambda graph_state, selected=phase: self._graph_node(graph_state, selected),
            )
        builder.add_edge(START, phases[0].value)
        for current, following in zip(phases, phases[1:], strict=False):
            builder.add_edge(current.value, following.value)
        builder.add_edge(phases[-1].value, END)
        self._graph = builder.compile()

    def run(self, request: AnalysisRunRequest) -> AnalysisRunResult:
        run = self._store.create_run(request)
        if run.status is AnalysisRunStatus.COMPLETED:
            return AnalysisRunResult(run.id, run.status, run.snapshot)
        return self._execute(run.id)

    def resume(self, run_id) -> AnalysisRunResult:
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        if run.status is AnalysisRunStatus.COMPLETED:
            return AnalysisRunResult(run.id, run.status, run.snapshot)
        return self._execute(run.id)

    def _execute(self, run_id) -> AnalysisRunResult:
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        self._store.start_run(run.id)
        try:
            self._graph.invoke({"run_id": run.id})
            latest = self._store.get_run(run.id)
            return AnalysisRunResult(
                run.id,
                AnalysisRunStatus.COMPLETED,
                latest.snapshot if latest else None,
            )
        except Exception as error:
            current = self._store.get_run(run.id)
            phase = (
                current.current_phase
                if current and current.current_phase
                else AnalysisPhase.SUBMIT_INTAKE
            )
            error_code, retryable = self._safe_failure(error)
            self._store.fail(
                run.id,
                error_code=error_code,
                phase=phase,
                retryable=retryable,
            )
            return AnalysisRunResult(
                run.id,
                AnalysisRunStatus.FAILED,
                None,
                error_code,
            )

    def _graph_node(self, graph_state: _GraphState, phase: AnalysisPhase) -> _GraphState:
        run_id = graph_state["run_id"]
        run = self._store.get_run(run_id)
        if run is None:
            raise KeyError(f"Unknown analysis run: {run_id}")
        if phase in set(run.completed_phases):
            return graph_state
        request = run.request
        state = dict(run.checkpoint_state)

        if phase in {
            AnalysisPhase.SUBMIT_INTAKE,
            AnalysisPhase.VALIDATE_SCOPE,
            AnalysisPhase.INGEST_PARSE,
            AnalysisPhase.RETRIEVE_EVIDENCE,
            AnalysisPhase.CHECKPOINT,
            AnalysisPhase.PROJECT_BROWSER,
            AnalysisPhase.EXTENDED_TRANSITION,
        }:
            self._phase(run.id, request, phase, state)
        elif phase is AnalysisPhase.PERCEIVE:
            self._start(run.id, request, phase)
            invocation = self._harness_invocation(run.id, phase, state)
            state["perception"] = self._harness.perceive(
                description=request.description,
                source_names=request.source_names,
                evidence=self._store.evidence_for(request),
                kind=request.kind,
                invocation=invocation,
            )
            self._record_harness_call(state, invocation)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.CONSTRUCT_ARTIFACTS:
            self._start(run.id, request, phase)
            invocation = self._harness_invocation(run.id, phase, state)
            state["artifacts"] = self._harness.construct(
                perception=state["perception"],
                kind=request.kind,
                invocation=invocation,
            )
            self._record_harness_call(state, invocation)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.EVALUATE_ADVISE:
            self._start(run.id, request, phase)
            invocation = self._harness_invocation(run.id, phase, state)
            state["assessment"] = self._harness.evaluate(
                artifacts=state["artifacts"],
                perception=state["perception"],
                kind=request.kind,
                invocation=invocation,
            )
            self._record_harness_call(state, invocation)
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.VALIDATE_RESULT:
            self._start(run.id, request, phase)
            artifacts = state["artifacts"]
            if tuple(artifact.artifact_type for artifact in artifacts) != ARTIFACT_TYPES:
                raise ValueError("SEVEN_ARTIFACT_CONTRACT_FAILED")
            if not all(artifact.evidence_refs for artifact in artifacts):
                raise ValueError("EVIDENCE_CONTRACT_FAILED")
            self._store.complete_phase(run.id, phase, state)
        elif phase is AnalysisPhase.PUBLISH:
            self._start(run.id, request, phase)
            snapshot = AssessmentSnapshot(
                id=uuid4(),
                analysis_run_id=run.id,
                workspace_id=request.workspace_id,
                project_id=request.project_id,
                state="current" if request.kind is RunKind.EXTENDED else "provisional",
                summary=self._summary(request.description),
                artifacts=state["artifacts"],
                assessment=state["assessment"],
                published_at=datetime.now(UTC),
            )
            self._store.publish(run.id, snapshot)
            self._store.complete_phase(run.id, phase, state)
        if phase is AnalysisPhase.EXTENDED_TRANSITION:
            self._store.complete_run(run.id)
        return graph_state

    def _phase(
        self,
        run_id,
        request: AnalysisRunRequest,
        phase: AnalysisPhase,
        state: dict[str, object],
    ) -> None:
        self._start(run_id, request, phase)
        self._store.complete_phase(run_id, phase, state)

    def _start(self, run_id, request: AnalysisRunRequest, phase: AnalysisPhase) -> None:
        self._store.start_phase(run_id, phase)
        if request.fail_at is phase:
            raise RuntimeError(f"{phase.value.upper()}_FAILED")
        if self._phase_delay_seconds > 0:
            sleep(self._phase_delay_seconds)

    @staticmethod
    def _harness_invocation(
        run_id,
        phase: AnalysisPhase,
        state: dict[str, object],
    ) -> HarnessInvocation:
        calls = state.get("harness_calls", {})
        fallback_active = isinstance(calls, dict) and any(
            isinstance(record, dict) and record.get("mode") == "fallback"
            for record in calls.values()
        )
        return HarnessInvocation(
            run_id=run_id,
            phase=phase,
            fallback_active=fallback_active,
        )

    @staticmethod
    def _record_harness_call(
        state: dict[str, object],
        invocation: HarnessInvocation,
    ) -> None:
        if invocation.metadata is None:
            return
        calls = state.setdefault("harness_calls", {})
        if isinstance(calls, dict):
            calls[invocation.phase.value] = asdict(invocation.metadata)

    @staticmethod
    def _summary(description: str) -> str:
        normalized = " ".join(description.split())
        return normalized[:320] if normalized else "Project information supplied through documents."

    @staticmethod
    def _safe_failure(error: Exception) -> tuple[str, bool]:
        if isinstance(error, AgentHarnessError):
            return error.code, error.retryable
        message = str(error)
        if message and len(message) <= 120 and all(
            character.isupper() or character.isdigit() or character == "_"
            for character in message
        ):
            return message, True
        return "ANALYSIS_FAILED", True

from uuid import UUID

from oslo_api.analysis import (
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisRunStatus,
    AnalysisWorkflow,
    DeterministicAgentHarness,
    FallbackAgentHarness,
    InMemoryAnalysisStore,
    RunKind,
)
from oslo_api.analysis.harness import AgentHarnessError

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")


class FailConstructOnceHarness(DeterministicAgentHarness):
    def __init__(self) -> None:
        self.perceive_calls = 0
        self.construct_calls = 0
        self.evaluate_calls = 0

    def perceive(self, **kwargs):
        self.perceive_calls += 1
        return super().perceive(**kwargs)

    def construct(self, **kwargs):
        self.construct_calls += 1
        if self.construct_calls == 1:
            raise RuntimeError("MODEL_GATEWAY_INTERRUPTED")
        return super().construct(**kwargs)

    def evaluate(self, **kwargs):
        self.evaluate_calls += 1
        return super().evaluate(**kwargs)


class UnavailableOpenAIHarness(DeterministicAgentHarness):
    def perceive(self, **kwargs):
        raise AgentHarnessError("OPENAI_UNAVAILABLE", retryable=True)


class AuthenticationRejectedHarness(DeterministicAgentHarness):
    def perceive(self, **kwargs):
        raise AgentHarnessError("OPENAI_AUTHENTICATION", retryable=False)


def test_initial_analysis_publishes_exactly_seven_traceable_artifacts() -> None:
    store = InMemoryAnalysisStore()
    workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())

    result = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description=(
                "DevNorth 2026 is a one-day developer conference for 450 attendees. "
                "Sponsors fund it. The venue, Wi-Fi capacity and speaker backups are unknown."
            ),
            source_names=(),
        )
    )

    assert result.status is AnalysisRunStatus.COMPLETED
    assert result.snapshot is not None
    assert result.snapshot.state == "provisional"
    assert [artifact.artifact_type.value for artifact in result.snapshot.artifacts] == [
        "intent",
        "context",
        "scope",
        "requirements",
        "work_breakdown",
        "schedule",
        "resources",
    ]
    assert all(artifact.evidence_refs for artifact in result.snapshot.artifacts)
    assert store.current_snapshot(PROJECT_ID) == result.snapshot


def test_governed_node_failures_preserve_the_last_good_snapshot() -> None:
    store = InMemoryAnalysisStore()
    workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
    baseline = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="A supported baseline project.",
            source_names=(),
        )
    )
    assert baseline.snapshot is not None

    for phase in (
        AnalysisPhase.PERCEIVE,
        AnalysisPhase.CONSTRUCT_ARTIFACTS,
        AnalysisPhase.EVALUATE_ADVISE,
    ):
        failed = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=PROJECT_ID,
                requested_by=USER_ID,
                kind=RunKind.EXTENDED,
                description="A deeper analysis that fails safely.",
                source_names=(),
                fail_at=phase,
            )
        )

        assert failed.status is AnalysisRunStatus.FAILED
        assert failed.error_code == f"{phase.value.upper()}_FAILED"
        assert store.current_snapshot(PROJECT_ID) == baseline.snapshot
        assert store.events_after(failed.run_id, 0)[-1].event_type == "analysis.failed"


def test_failed_run_resumes_from_the_last_completed_checkpoint() -> None:
    store = InMemoryAnalysisStore()
    harness = FailConstructOnceHarness()
    workflow = AnalysisWorkflow(store=store, harness=harness)

    failed = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="A project whose model connection is interrupted once.",
            source_names=(),
        )
    )
    assert failed.status is AnalysisRunStatus.FAILED

    resumed = workflow.resume(failed.run_id)

    assert resumed.status is AnalysisRunStatus.COMPLETED
    assert resumed.snapshot is not None
    assert harness.perceive_calls == 1
    assert harness.construct_calls == 2
    assert harness.evaluate_calls == 1
    assert store.current_snapshot(PROJECT_ID) == resumed.snapshot


def test_initial_openai_failure_uses_one_consistent_deterministic_fallback() -> None:
    store = InMemoryAnalysisStore()
    workflow = AnalysisWorkflow(
        store=store,
        harness=FallbackAgentHarness(
            primary=UnavailableOpenAIHarness(),
            fallback=DeterministicAgentHarness(),
        ),
    )

    result = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="A launch plan with a defined goal and incomplete dependencies.",
            source_names=(),
        )
    )

    assert result.status is AnalysisRunStatus.COMPLETED
    assert result.snapshot is not None
    assert all(artifact.basis == "fallback" for artifact in result.snapshot.artifacts)
    run = store.get_run(result.run_id)
    assert run is not None
    harness_calls = run.checkpoint_state["harness_calls"]
    assert harness_calls["perceive"]["fallback_reason"] == "OPENAI_UNAVAILABLE"
    assert harness_calls["construct_artifacts"]["mode"] == "fallback"
    assert harness_calls["evaluate_advise"]["mode"] == "fallback"


def test_permanent_openai_failure_is_safe_and_not_retryable() -> None:
    store = InMemoryAnalysisStore()
    workflow = AnalysisWorkflow(store=store, harness=AuthenticationRejectedHarness())

    result = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="A project that cannot reach the configured model.",
            source_names=(),
        )
    )

    assert result.status is AnalysisRunStatus.FAILED
    assert result.error_code == "OPENAI_AUTHENTICATION"
    failed_event = store.events_after(result.run_id, 0)[-1]
    assert failed_event.error_code == "OPENAI_AUTHENTICATION"
    assert failed_event.retryable is False


def test_extended_openai_failure_preserves_last_good_without_fallback() -> None:
    store = InMemoryAnalysisStore()
    baseline = AnalysisWorkflow(
        store=store,
        harness=DeterministicAgentHarness(),
    ).run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="A valid provisional baseline.",
            source_names=(),
        )
    )
    assert baseline.snapshot is not None
    workflow = AnalysisWorkflow(
        store=store,
        harness=FallbackAgentHarness(
            primary=UnavailableOpenAIHarness(),
            fallback=DeterministicAgentHarness(),
        ),
    )

    extended = workflow.run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.EXTENDED,
            description="A deeper read whose provider is unavailable.",
            source_names=(),
            parent_run_id=baseline.run_id,
        )
    )

    assert extended.status is AnalysisRunStatus.FAILED
    assert extended.error_code == "OPENAI_UNAVAILABLE"
    assert store.current_snapshot(PROJECT_ID) == baseline.snapshot
    assert store.events_after(extended.run_id, 0)[-1].retryable is True

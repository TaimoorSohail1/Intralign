from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine, text

from oslo_api.analysis import (
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisRunStatus,
    AnalysisWorkflow,
    DeterministicAgentHarness,
    RunKind,
)
from oslo_api.analysis.persistence import DatabaseAnalysisStore
from oslo_api.settings import Settings

SETTINGS = Settings()  # type: ignore[call-arg]
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")


class FailingEvaluateHarness(DeterministicAgentHarness):
    def evaluate(self, **_kwargs):
        raise RuntimeError("EVALUATE_ADVISE_FAILED")


class FailingStageHarness(DeterministicAgentHarness):
    def __init__(self, phase: AnalysisPhase) -> None:
        self.phase = phase

    def perceive(self, **kwargs):
        if self.phase is AnalysisPhase.PERCEIVE:
            raise RuntimeError("PERCEIVE_FAILED")
        return super().perceive(**kwargs)

    def construct(self, **kwargs):
        if self.phase is AnalysisPhase.CONSTRUCT_ARTIFACTS:
            raise RuntimeError("CONSTRUCT_ARTIFACTS_FAILED")
        return super().construct(**kwargs)

    def evaluate(self, **kwargs):
        if self.phase is AnalysisPhase.EVALUATE_ADVISE:
            raise RuntimeError("EVALUATE_ADVISE_FAILED")
        return super().evaluate(**kwargs)


def test_postgres_analysis_is_checkpointed_and_published_atomically() -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Slice 2 integration', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
        initial = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A conference plan with unknown Wi-Fi capacity.",
                source_names=("brief.md",),
                idempotency_key=f"integration:{project_id}",
            )
        )

        assert initial.status is AnalysisRunStatus.COMPLETED
        assert initial.snapshot is not None
        with engine.connect() as connection:
            current_run_id = connection.execute(
                text("select current_analysis_run_id from public.projects where id = :id"),
                {"id": project_id},
            ).scalar_one()
            artifact_count = connection.execute(
                text(
                    "select count(*) from public.artifact_versions "
                    "where analysis_run_id = :run_id"
                ),
                {"run_id": initial.run_id},
            ).scalar_one()
            construct_checkpoint = connection.execute(
                text(
                    """
                    select count(*) from public.analysis_checkpoints
                    where analysis_run_id = :run_id
                      and checkpoint_key = 'construct_artifacts'
                    """
                ),
                {"run_id": initial.run_id},
            ).scalar_one()
            perceive_attempt = connection.execute(
                text(
                    """
                    select provider, model_id, prompt_version, execution_mode
                    from public.analysis_node_attempts
                    where analysis_run_id = :run_id and phase = 'perceive'
                    order by attempt_no desc limit 1
                    """
                ),
                {"run_id": initial.run_id},
            ).mappings().one()

        assert current_run_id == initial.run_id
        assert artifact_count == 7
        assert construct_checkpoint == 1
        assert perceive_attempt["provider"] == "deterministic"
        assert perceive_attempt["model_id"] == "oslo-deterministic-v1"
        assert perceive_attempt["prompt_version"] == "oslo-deterministic-v1"
        assert perceive_attempt["execution_mode"] == "primary"

        failed_extended = AnalysisWorkflow(
            store=store,
            harness=FailingEvaluateHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.EXTENDED,
                description="A deeper run that is interrupted.",
                source_names=("brief.md",),
                idempotency_key=f"integration-extended:{project_id}",
                parent_run_id=initial.run_id,
            )
        )

        assert failed_extended.status is AnalysisRunStatus.FAILED
        with engine.connect() as connection:
            unchanged_pointer = connection.execute(
                text("select current_analysis_run_id from public.projects where id = :id"),
                {"id": project_id},
            ).scalar_one()
        assert unchanged_pointer == initial.run_id
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


@pytest.mark.parametrize(
    "failed_phase",
    [
        AnalysisPhase.PERCEIVE,
        AnalysisPhase.CONSTRUCT_ARTIFACTS,
        AnalysisPhase.EVALUATE_ADVISE,
    ],
)
def test_postgres_refresh_retry_resumes_each_governed_llm_stage(
    failed_phase: AnalysisPhase,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Slice 2 restart integration', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=FailingStageHarness(failed_phase))
        failed = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A durable analysis run used to exercise refresh and retry.",
                source_names=("brief.md",),
                idempotency_key=f"integration-restart:{failed_phase}:{project_id}",
            )
        )
        assert failed.status is AnalysisRunStatus.FAILED
        assert store.current_snapshot(project_id) is None

        refreshed_store = DatabaseAnalysisStore(create_engine(SETTINGS.database_url))
        refreshed = refreshed_store.get_run(failed.run_id)
        assert refreshed is not None
        assert refreshed.status is AnalysisRunStatus.FAILED
        completed_before_retry = set(refreshed.completed_phases)

        resumed = AnalysisWorkflow(
            store=refreshed_store,
            harness=DeterministicAgentHarness(),
        ).resume(failed.run_id)
        assert resumed.status is AnalysisRunStatus.COMPLETED
        assert resumed.snapshot is not None
        assert len(resumed.snapshot.artifacts) == 7
        assert completed_before_retry.issubset(
            set(refreshed_store.get_run(failed.run_id).completed_phases)
        )
        assert refreshed_store.current_snapshot(project_id) == resumed.snapshot
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )

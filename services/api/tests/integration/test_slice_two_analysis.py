from dataclasses import replace
from datetime import UTC, datetime, timedelta
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
from oslo_api.analysis.document_store import DatabaseDocumentStore
from oslo_api.analysis.history import list_project_history
from oslo_api.analysis.object_storage import LocalObjectStorage
from oslo_api.analysis.persistence import DatabaseAnalysisStore
from oslo_api.analysis.service import DatabaseSliceTwoApplication
from oslo_api.collaboration.service import DatabaseCollaborationService
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


class TitledHarness(DeterministicAgentHarness):
    def construct(self, **kwargs):
        return tuple(
            replace(artifact, project_title="Northstar CRM Modernization")
            for artifact in super().construct(**kwargs)
        )


class NoopExecutor:
    def submit(self, *_args, **_kwargs):
        return None


class RecordingReportMailer:
    def __init__(self) -> None:
        self.messages: list[dict] = []

    def send_report(self, **payload) -> None:
        self.messages.append(payload)


def test_artifact_noop_is_inert_and_material_edit_uses_structured_evidence(
    tmp_path,
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
                values (:id, :workspace_id, 'Artifact no-op integration', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
        baseline = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A governed delivery plan.",
                source_names=("brief.md",),
                idempotency_key=f"artifact-noop-baseline:{project_id}",
            )
        )
        assert baseline.snapshot is not None
        application = DatabaseSliceTwoApplication(
            engine=engine,
            store=store,
            workflow=workflow,
            executor=NoopExecutor(),  # type: ignore[arg-type]
            document_store=DatabaseDocumentStore(
                engine=engine,
                object_store=LocalObjectStorage(tmp_path),
            ),
            extended_delay_seconds=0,
        )
        current = application.get_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="intent",
        )

        unchanged, noop_run = application.update_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="intent",
            content=current["content"],
            expected_version=current["version"],
            key=f"artifact-noop:{project_id}",
        )

        assert noop_run is None
        assert unchanged["version"] == current["version"]
        material_content = {
            "sections": [
                {
                    **current["content"]["sections"][0],
                    "body": "The user confirmed the governed delivery outcome.",
                }
            ]
        }
        edited, edit_run = application.update_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="intent",
            content=material_content,
            expected_version=current["version"],
            key=f"artifact-material:{project_id}",
        )

        assert edit_run is not None
        assert edited["version"] == current["version"] + 1
        assert edited["provenance"] == "mixed"
        assert "USER_ARTIFACT_EDIT" not in edit_run.request.description
        assert len(edit_run.request.user_evidence) == 1
        assert edit_run.request.user_evidence[0].reference.startswith(
            "user:artifact:intent:version:"
        )
        completed_edit = workflow.resume(edit_run.id)
        assert completed_edit.status is AnalysisRunStatus.COMPLETED
        after_reanalysis = application.get_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="intent",
        )
        assert after_reanalysis["version"] == edited["version"]

        repeated, repeated_run = application.update_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="intent",
            content=material_content,
            expected_version=edited["version"],
            key=f"artifact-repeat:{project_id}",
        )
        assert repeated_run is None
        assert repeated["version"] == edited["version"]

        with engine.connect() as connection:
            run_count = connection.execute(
                text(
                    "select count(*) from public.analysis_runs where project_id = :project_id"
                ),
                {"project_id": project_id},
            ).scalar_one()
            draft_version_count = connection.execute(
                text(
                    """
                    select count(*) from public.artifact_draft_versions
                    where project_id = :project_id and artifact_type = 'intent'
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
            unchanged_schedule_revisions = list(
                connection.execute(
                    text(
                        """
                        select revision
                        from public.artifact_versions
                        where project_id = :project_id
                          and artifact_type = 'schedule'
                        order by created_at
                        """
                    ),
                    {"project_id": project_id},
                ).scalars()
            )
        assert run_count == 2
        assert draft_version_count == 1
        assert unchanged_schedule_revisions == [1, 1]
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_report_draft_and_immediate_delivery_are_durable() -> None:
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
                values (:id, :workspace_id, 'Durable report integration', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        result = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A governed project readout.",
                source_names=("brief.md",),
                idempotency_key=f"report-baseline:{project_id}",
            )
        )
        assert result.snapshot is not None
        content = {
            "sections": [
                {
                    "id": f"section-{index}",
                    "title": f"Section {index}",
                    "body": [f"Exact retained paragraph {index}"],
                }
                for index in range(7)
            ]
        }
        mailer = RecordingReportMailer()
        service = DatabaseCollaborationService(
            engine,
            "http://localhost:3000",
            mailer,
        )

        service.save_report(
            actor_user_id=owner_id,
            project_id=project_id,
            snapshot_id=result.snapshot.id,
            content=content,
        )
        delivery = service.deliver_report(
            actor_user_id=owner_id,
            project_id=project_id,
            snapshot_id=result.snapshot.id,
            recipient_email="sponsor@example.com",
            recipient_label="Sponsor",
            subject="Durable project readout",
            content=content,
            scheduled_for=datetime.now(UTC) - timedelta(seconds=1),
        )
        reloaded = service.report_state(
            actor_user_id=owner_id,
            project_id=project_id,
        )

        assert reloaded["content"] == content
        assert delivery["status"] == "sent"
        assert len(mailer.messages) == 1
        assert mailer.messages[0]["sections"] == content["sections"]
        with engine.connect() as connection:
            stored_status = connection.execute(
                text(
                    """
                    select status from public.project_report_deliveries
                    where id = cast(:delivery_id as uuid)
                    """
                ),
                {"delivery_id": delivery["id"]},
            ).scalar_one()
            report_events = set(
                connection.execute(
                    text(
                        """
                        select event_type
                        from public.project_history_events
                        where project_id = :project_id
                          and event_type like 'report.%'
                        """
                    ),
                    {"project_id": project_id},
                ).scalars()
            )
        assert stored_status == "sent"
        assert report_events == {"report.delivery_requested", "report.sent"}
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


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
                consumes_analysis_allowance=True,
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
            history_events = connection.execute(
                text(
                    """
                    select category, event_type, summary
                    from public.project_history_events
                    where analysis_run_id = :run_id
                    order by id
                    """
                ),
                {"run_id": initial.run_id},
            ).mappings().all()
            analysis_usage = connection.execute(
                text(
                    """
                    select usage_kind
                    from public.workspace_analysis_usage
                    where analysis_run_id = :run_id
                    """
                ),
                {"run_id": initial.run_id},
            ).scalar_one()

        assert current_run_id == initial.run_id
        assert artifact_count == 7
        assert construct_checkpoint == 1
        assert perceive_attempt["provider"] == "deterministic"
        assert perceive_attempt["model_id"] == "oslo-deterministic-v1"
        assert perceive_attempt["prompt_version"] == "oslo-deterministic-v1"
        assert perceive_attempt["execution_mode"] == "primary"
        assert analysis_usage == "user_requested_analysis"
        assert [event["event_type"] for event in history_events] == [
            "analysis.initial_completed",
            "issues.reconciled",
            "artifacts.versions_retained",
        ]
        assert history_events[0]["category"] == "analysis"
        assert history_events[0]["summary"] == "Initial Analysis complete"

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
            failed_history = connection.execute(
                text(
                    """
                    select event_type, detail
                    from public.project_history_events
                    where analysis_run_id = :run_id
                    """
                ),
                {"run_id": failed_extended.run_id},
            ).mappings().one()
        assert unchanged_pointer == initial.run_id
        assert failed_history["event_type"] == "analysis.failed"
        assert "last-good project read remains current" in failed_history["detail"]
        history = list_project_history(
            engine,
            workspace_id=WORKSPACE_ID,
            project_id=project_id,
            category="all",
            cursor=None,
            limit=40,
        )
        assert [group["status"] for group in history["groups"]] == [
            "failed",
            "completed",
        ]
        assert len(history["trend"]) == 1
        assert history["trend"][0]["current"] is True
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_new_snapshot_does_not_resolve_issue_rows_without_resolution_evidence() -> None:
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
                values (:id, :workspace_id, 'Slice 3 issue lifecycle', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
        connection.execute(
            text(
                """
                insert into public.issues (
                  workspace_id, project_id, stable_key, current_status
                ) values (
                  :workspace_id, :project_id, 'ISS-STALE', 'open'
                )
                """
            ),
            {"workspace_id": WORKSPACE_ID, "project_id": project_id},
        )
    try:
        result = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A governed delivery plan with a confirmed owner and fallback.",
                source_names=("brief.md",),
                idempotency_key=f"integration-issue-lifecycle:{project_id}",
            )
        )

        assert result.status is AnalysisRunStatus.COMPLETED
        with engine.connect() as connection:
            stale_status = connection.execute(
                text(
                    """
                    select current_status from public.issues
                    where project_id = :project_id and stable_key = 'ISS-STALE'
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
        assert stale_status == "open"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_history_falls_back_to_retained_snapshots_when_legacy_events_are_absent() -> None:
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
                values (:id, :workspace_id, 'Slice 7 retained history', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        result = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A retained plan read with a documented owner and schedule.",
                source_names=("brief.md",),
                idempotency_key=f"integration-history-fallback:{project_id}",
            )
        )
        assert result.status is AnalysisRunStatus.COMPLETED

        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    delete from public.project_history_events
                    where project_id = :project_id
                    """
                ),
                {"project_id": project_id},
            )

        history = list_project_history(
            engine,
            workspace_id=WORKSPACE_ID,
            project_id=project_id,
            category="all",
            cursor=None,
            limit=40,
        )

        assert len(history["trend"]) == 1
        assert len(history["groups"]) == 1
        assert history["groups"][0]["run_id"] == str(result.run_id)
        assert history["groups"][0]["current"] is True
        assert history["groups"][0]["events"][0]["summary"] == (
            "Initial Analysis complete"
        )
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_analysis_promotes_a_supported_title_and_increments_artifact_revisions() -> None:
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
                values (:id, :workspace_id, 'Untitled project', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=TitledHarness())
        source_names = tuple(f"project-{index}.pdf" for index in range(1, 11))
        initial = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="Northstar CRM Modernization project.",
                source_names=source_names,
                idempotency_key=f"title-initial:{project_id}",
            )
        )
        extended = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.EXTENDED,
                description="Northstar CRM Modernization project.",
                source_names=source_names,
                parent_run_id=initial.run_id,
                idempotency_key=f"title-extended:{project_id}",
            )
        )

        assert initial.status is AnalysisRunStatus.COMPLETED
        assert extended.status is AnalysisRunStatus.COMPLETED
        assert extended.snapshot is not None
        assert extended.snapshot.project_title == "Northstar CRM Modernization"
        assert extended.snapshot.source_document_count == 10
        with engine.connect() as connection:
            project_name = connection.execute(
                text("select name from public.projects where id = :id"),
                {"id": project_id},
            ).scalar_one()
            revisions = list(
                connection.execute(
                    text(
                        """
                        select revision
                        from public.artifact_versions
                        where project_id = :project_id
                          and artifact_type = 'schedule'
                        order by revision
                        """
                    ),
                    {"project_id": project_id},
                ).scalars()
            )
        assert project_name == "Northstar CRM Modernization"
        assert revisions == [1, 2]
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

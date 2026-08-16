from collections.abc import Iterator
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import httpx
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy import event as sqlalchemy_event

from oslo_api.analysis import (
    AnalysisPassKind,
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
from oslo_api.analysis.persistence import DatabaseAnalysisStore, _primary_outcome_title
from oslo_api.analysis.service import DatabaseSliceTwoApplication
from oslo_api.application import DatabaseSliceOneApplication
from oslo_api.collaboration.service import CollaborationError, DatabaseCollaborationService
from oslo_api.identity import SupabaseIdentityProvider
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

    def construct_artifact(self, **kwargs):
        if self.phase is AnalysisPhase.CONSTRUCT_ARTIFACTS:
            raise RuntimeError("CONSTRUCT_ARTIFACTS_FAILED")
        return super().construct_artifact(**kwargs)

    def evaluate(self, **kwargs):
        if self.phase is AnalysisPhase.EVALUATE_ADVISE:
            raise RuntimeError("EVALUATE_ADVISE_FAILED")
        return super().evaluate(**kwargs)


class TitledHarness(DeterministicAgentHarness):
    def construct_artifact(self, **kwargs):
        return replace(
            super().construct_artifact(**kwargs),
            project_title="Northstar CRM Modernization",
        )


class NoopExecutor:
    def submit(self, *_args, **_kwargs):
        return None


class RecordingReportMailer:
    def __init__(self) -> None:
        self.messages: list[dict] = []

    def send_report(self, **payload) -> None:
        self.messages.append(payload)


class RecordingAsanaGateway:
    destination_gid = "asana-project-integration"

    def __init__(self) -> None:
        self.items: list[dict] = []

    def create_task(self, item: dict) -> dict[str, str]:
        self.items.append(item)
        index = len(self.items)
        return {
            "gid": f"asana-task-{index}",
            "permalink_url": f"https://app.asana.com/0/1/{index}",
        }


class FailingReviewMailer:
    def __init__(self) -> None:
        self.attempts = 0

    def send_report(self, **_payload) -> None:
        self.attempts += 1
        raise RuntimeError("REVIEW_EMAIL_PROVIDER_UNAVAILABLE")


@pytest.fixture(scope="module")
def workspace_owner_id() -> Iterator[UUID]:
    """Provide a real workspace Owner without conflating it with the platform Admin."""
    engine = create_engine(SETTINGS.database_url)
    with httpx.Client(timeout=20) as client:
        identity = SupabaseIdentityProvider(
            client=client,
            supabase_url=SETTINGS.supabase_url,
            api_key=SETTINGS.supabase_secret_key,
        )
        # Every pytest process owns its identity. The full API suite and the
        # focused R2 guardrail suite may run at the same time in CI; sharing a
        # fixed user lets one suite remove the other's workspace membership
        # during teardown and turns valid behavior into permission failures.
        email = f"slice-two-integration-owner-{uuid4().hex}@oslo.local"
        owner = identity.create_user(
            email=email,
            password="SliceTwoIntegrationOwner123!",
            display_name="Slice Two Integration Owner",
        )
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    insert into public.profiles (id, display_name)
                    values (:id, 'Slice Two Integration Owner')
                    on conflict (id) do update set display_name = excluded.display_name
                    """
                ),
                {"id": owner.id},
            )
            connection.execute(
                text(
                    """
                    insert into public.memberships (workspace_id, user_id, role)
                    values (:workspace_id, :user_id, 'owner')
                    on conflict (workspace_id, user_id) do update set role = 'owner'
                    """
                ),
                {"workspace_id": WORKSPACE_ID, "user_id": owner.id},
            )
        try:
            yield owner.id
        finally:
            with engine.begin() as connection:
                connection.execute(
                    text("delete from public.memberships where user_id = :user_id"),
                    {"user_id": owner.id},
                )
            identity.delete_user(owner.id)


def test_confirming_the_primary_outcome_updates_the_first_class_outcome_record(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            text(
                "insert into public.projects (id, workspace_id, name, status, created_by) "
                "values (:id, :workspace_id, 'Outcome declaration', 'draft', :owner_id)"
            ),
            {
                "id": project_id,
                "workspace_id": WORKSPACE_ID,
                "owner_id": workspace_owner_id,
            },
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
        baseline = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=workspace_owner_id,
                kind=RunKind.INITIAL,
                description="A governed plan whose outcome the owner will confirm.",
                source_names=("brief.md",),
                idempotency_key=f"outcome-declaration-baseline:{project_id}",
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

        application.act_on_outcome(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            action="confirm",
            outcome="Reduce failed customer handoffs",
            key=f"confirm-primary-outcome:{project_id}",
        )

        with engine.connect() as connection:
            stored = connection.execute(
                text(
                    "select title, provenance from public.project_outcomes "
                    "where project_id = :project_id and is_primary"
                ),
                {"project_id": project_id},
            ).mappings().one()
        assert dict(stored) == {
            "title": "Reduce failed customer handoffs",
            "provenance": "declared",
        }
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )
        engine.dispose()


def test_clarification_is_durable_and_addressed_before_reanalysis_completes(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Clarification lifecycle', 'draft', :owner_id)
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
                description="A migration plan with unresolved delivery ownership.",
                source_names=("brief.md",),
                idempotency_key=f"clarification-baseline:{project_id}",
            )
        )
        assert baseline.snapshot is not None
        inferred_outcome = _primary_outcome_title(baseline.snapshot.artifacts)
        with engine.connect() as connection:
            stored_outcome = connection.execute(
                text(
                    "select title, status, is_primary, provenance "
                    "from public.project_outcomes where project_id = :project_id"
                ),
                {"project_id": project_id},
            ).mappings().one()
        assert dict(stored_outcome) == {
            "title": inferred_outcome,
            "status": "active",
            "is_primary": True,
            "provenance": "inferred",
        }
        issue = next(
            item
            for item in baseline.snapshot.assessment.issues
            if item.clarification is not None
        )
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

        run = application.answer_issue(
            actor_user_id=owner_id,
            project_id=project_id,
            issue_id=issue.id,
            answer="Priya owns migration and the legacy import is the fallback.",
            key=f"clarification-answer:{project_id}",
        )
        updates = application.list_issue_actions(
            actor_user_id=owner_id,
            project_id=project_id,
        )

        assert run.status is AnalysisRunStatus.QUEUED
        assert updates[0]["issue_id"] == issue.id
        assert updates[0]["action"] == "clarification"
        assert updates[0]["status"] == "addressed"
        with engine.connect() as connection:
            stored = connection.execute(
                text(
                    """
                    select answer.analysis_run_id, issue.current_status
                    from public.issue_answers answer
                    join public.issues issue
                      on issue.workspace_id = answer.workspace_id
                     and issue.project_id = answer.project_id
                     and issue.stable_key = answer.issue_stable_key
                    where answer.project_id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).mappings().one()
        assert stored["analysis_run_id"] == run.id
        assert stored["current_status"] == "addressed"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_rejecting_a_proposal_records_history_against_the_source_read(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Proposal decision history', 'draft', :owner_id)
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
                description="A delivery plan with unresolved ownership and checkpoints.",
                source_names=("brief.md",),
                idempotency_key=f"proposal-baseline:{project_id}",
            )
        )
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
        proposal = application.list_issue_proposals(
            actor_user_id=owner_id,
            project_id=project_id,
        )[0]

        decision = application.decide_issue_proposal(
            actor_user_id=owner_id,
            project_id=project_id,
            proposal_id=UUID(proposal["id"]),
            accepted=False,
            surface="folded_read",
            key=f"proposal-reject:{project_id}",
        )

        assert decision["analysis_run"] is None
        assert decision["proposal"]["rejected"] is True
        with engine.connect() as connection:
            history_run_id = connection.execute(
                text(
                    """
                    select analysis_run_id
                    from public.project_history_events
                    where project_id = :project_id
                      and event_type = 'proposal.rejected'
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
        assert history_run_id == baseline.run_id
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_accepting_a_build_proposal_creates_a_withdrawable_lifecycle_act(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Withdraw accepted proposal', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
        workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.INITIAL,
                description="A delivery plan with unresolved ownership and checkpoints.",
                source_names=("brief.md",),
                idempotency_key=f"proposal-withdraw-baseline:{project_id}",
            )
        )
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
        proposal = next(
            candidate
            for candidate in application.list_issue_proposals(
                actor_user_id=owner_id,
                project_id=project_id,
            )
            if candidate["kind"] == "build"
        )

        accepted = application.decide_issue_proposal(
            actor_user_id=owner_id,
            project_id=project_id,
            proposal_id=UUID(proposal["id"]),
            accepted=True,
            surface="folded_read",
            key=f"proposal-accept:{project_id}",
        )
        withdrawn = application.act_on_issue_lifecycle(
            actor_user_id=owner_id,
            project_id=project_id,
            issue_id=proposal["issue_id"],
            act="withdraw",
            basis=None,
            evidence_ref=None,
            resolution=None,
            reviewer=None,
            key=f"proposal-withdraw:{project_id}",
        )

        assert accepted["analysis_run"] is not None
        assert withdrawn["status"] == "open"
        assert withdrawn["attestation"]["supersedes"] is not None
        with engine.connect() as connection:
            acts = connection.execute(
                text(
                    """
                    select act
                    from public.issue_attestations
                    where project_id = :project_id
                      and issue_stable_key = :issue_id
                    order by created_at
                    """
                ),
                {"project_id": project_id, "issue_id": proposal["issue_id"]},
            ).scalars().all()
        assert [str(act) for act in acts] == ["fix", "withdraw"]
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_artifact_noop_is_inert_and_material_edit_uses_structured_evidence(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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
                    "provenance": "confirmed_by_user",
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
        assert (
            after_reanalysis["content"]["sections"][0]["provenance"]
            == "confirmed_by_user"
        )

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


def test_report_draft_and_immediate_delivery_are_durable(workspace_owner_id: UUID) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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
        with engine.connect() as connection:
            read_before_report = connection.execute(
                text(
                    "select current_analysis_run_id from public.projects "
                    "where id = :project_id"
                ),
                {"project_id": project_id},
            ).scalar_one()
            analysis_count_before_report = connection.execute(
                text(
                    "select count(*) from public.analysis_runs "
                    "where project_id = :project_id"
                ),
                {"project_id": project_id},
            ).scalar_one()

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
        with engine.connect() as connection:
            read_after_report = connection.execute(
                text(
                    "select current_analysis_run_id from public.projects "
                    "where id = :project_id"
                ),
                {"project_id": project_id},
            ).scalar_one()
            analysis_count_after_report = connection.execute(
                text(
                    "select count(*) from public.analysis_runs "
                    "where project_id = :project_id"
                ),
                {"project_id": project_id},
            ).scalar_one()

        assert read_after_report == read_before_report == result.run_id
        assert analysis_count_after_report == analysis_count_before_report == 1

        newer = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.EXTENDED,
                description="A governed project readout with newer evidence.",
                source_names=("brief.md",),
                parent_run_id=result.run_id,
                idempotency_key=f"report-newer-analysis:{project_id}",
            )
        )
        assert newer.snapshot is not None
        with pytest.raises(CollaborationError) as stale_error:
            service.deliver_report(
                actor_user_id=owner_id,
                project_id=project_id,
                snapshot_id=result.snapshot.id,
                recipient_email="sponsor@example.com",
                recipient_label="Sponsor",
                subject="Durable project readout",
                content=content,
                scheduled_for=datetime.now(UTC) - timedelta(seconds=1),
            )
        with pytest.raises(CollaborationError) as confirmed_stale_error:
            service.deliver_report(
                actor_user_id=owner_id,
                project_id=project_id,
                snapshot_id=result.snapshot.id,
                recipient_email="sponsor@example.com",
                recipient_label="Sponsor",
                subject="Durable project readout",
                content=content,
                scheduled_for=datetime.now(UTC) - timedelta(seconds=1),
                confirm_previous_analysis=True,
            )

        assert reloaded["content"] == content
        assert delivery["status"] == "sent"
        assert stale_error.value.code == "REPORT_PREVIOUS_ANALYSIS_BLOCKED"
        assert confirmed_stale_error.value.code == "REPORT_PREVIOUS_ANALYSIS_BLOCKED"
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


def test_asana_handoff_is_idempotent_and_exports_only_executable_fields(
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        original_subscription = connection.execute(
            text(
                """
                select plan_code, status from public.workspace_subscriptions
                where workspace_id = :workspace_id
                """
            ),
            {"workspace_id": WORKSPACE_ID},
        ).mappings().one()
        connection.execute(
            text(
                """
                update public.workspace_subscriptions
                set plan_code = 'basic', status = 'active'
                where workspace_id = :workspace_id
                """
            ),
            {"workspace_id": WORKSPACE_ID},
        )
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Asana handoff integration', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": workspace_owner_id},
        )
    try:
        result = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=workspace_owner_id,
                kind=RunKind.INITIAL,
                description="A launch plan with work, owners, dates and retained source evidence.",
                source_names=("delivery-plan.md",),
                idempotency_key=f"asana-baseline:{project_id}",
            )
        )
        assert result.snapshot is not None
        gateway = RecordingAsanaGateway()
        service = DatabaseCollaborationService(
            engine,
            "http://localhost:3000",
            asana_gateway=gateway,
        )

        preview = service.asana_handoff_state(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
        )
        first = service.import_asana_handoff(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
        )
        second = service.import_asana_handoff(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
        )

        assert preview["configured"] is True
        assert preview["entitled"] is True
        assert first["state"] == "completed"
        assert second["state"] == "completed"
        assert len(gateway.items) == first["total_count"]
        assert all("assessment" not in item and "summary" not in item for item in gateway.items)
        with engine.connect() as connection:
            item_count = connection.execute(
                text(
                    """
                    select count(*) from public.project_asana_handoff_items item
                    join public.project_asana_handoffs handoff on handoff.id = item.handoff_id
                    where handoff.project_id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
        assert item_count == first["total_count"]
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )
            connection.execute(
                text(
                    """
                    update public.workspace_subscriptions
                    set plan_code = :plan_code, status = :status
                    where workspace_id = :workspace_id
                    """
                ),
                {
                    "plan_code": original_subscription["plan_code"],
                    "status": original_subscription["status"],
                    "workspace_id": WORKSPACE_ID,
                },
            )


def test_scoped_reviewer_confirmation_is_private_attributed_and_queued(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Scoped reviewer round-trip', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": workspace_owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(store=store, harness=DeterministicAgentHarness())
        baseline = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=workspace_owner_id,
                kind=RunKind.INITIAL,
                description="A launch plan with an unconfirmed accountable owner.",
                source_names=("launch-brief.md",),
                idempotency_key=f"review-baseline:{project_id}",
            )
        )
        assert baseline.snapshot is not None
        issue = baseline.snapshot.assessment.issues[0]
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.assessment_snapshots
                    set snapshot_json = jsonb_set(
                      snapshot_json,
                      '{project_title}',
                      to_jsonb(cast('Evidence-backed launch plan' as text))
                    )
                    where id = :snapshot_id
                    """
                ),
                {"snapshot_id": baseline.snapshot.id},
            )
        review_mailer = FailingReviewMailer()
        collaboration = DatabaseCollaborationService(
            engine,
            "http://localhost:3000",
            review_mailer=review_mailer,
        )
        created_comment = collaboration.add_comment(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=issue.id,
            body="This discussion must stay attributed and must not change grounding.",
            mentions=[],
        )
        assert created_comment["author_name"] == "Slice Two Integration Owner"
        shared = collaboration.create_snapshot_link(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            recipient_name="Executive sponsor",
            recipient_email="sponsor@example.com",
        )
        share_token = shared["url"].rsplit("/", 1)[-1]
        frozen_snapshot = collaboration.resolve_snapshot(share_token)
        assert frozen_snapshot["recipient_name"] == "Executive sponsor"
        assert frozen_snapshot["project_name"] == "Evidence-backed launch plan"
        assert frozen_snapshot["snapshot_json"]["summary"].startswith(
            "Evidence-backed launch plan."
        )
        assert "At the orientation stage" in frozen_snapshot["snapshot_json"]["summary"]
        assert "90 days" in frozen_snapshot["view_audit_disclosure"]
        stale_grant = collaboration.create_review_grant(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=issue.id,
            reviewer_name="First reviewer",
            reviewer_email="first@example.com",
            question="Who is accountable for the launch decision?",
            source_ref="launch-brief.md#ownership",
            source_excerpt="The launch owner has not yet been named.",
        )
        stale_token = stale_grant["url"].rsplit("/", 1)[-1]
        grant = collaboration.create_review_grant(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=issue.id,
            reviewer_name="Amina Khan",
            reviewer_email="amina@example.com",
            question="Who is accountable for the launch decision?",
            source_ref="launch-brief.md#ownership",
            source_excerpt="The launch owner has not yet been named.",
        )
        token = grant["url"].rsplit("/", 1)[-1]
        assert stale_grant["delivery_state"] == "failed"
        assert stale_grant["delivery_attempts"] == 3
        assert grant["delivery_state"] == "failed"
        assert grant["delivery_attempts"] == 3
        assert review_mailer.attempts == 6

        manual_delivery = collaboration.mark_review_delivered(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            grant_id=UUID(grant["id"]),
        )
        assert manual_delivery["delivery_state"] == "awaiting"

        with pytest.raises(CollaborationError) as stale_error:
            collaboration.resolve_review(stale_token)
        assert stale_error.value.code == "REVIEW_UNAVAILABLE"

        scoped = collaboration.resolve_review(token)
        assert set(scoped) == {
            "id",
            "reviewer_name",
            "project_name",
            "expires_at",
            "question",
            "source",
            "response_kind",
        }
        assert scoped["source"] == {
            "reference": "launch-brief.md#ownership",
            "excerpt": "The launch owner has not yet been named.",
        }
        assert scoped["project_name"] == "Evidence-backed launch plan"
        with pytest.raises(CollaborationError) as scope_error:
            collaboration.resolve_snapshot(token)
        assert scope_error.value.code == "TOKEN_SCOPE_FORBIDDEN"
        assert scope_error.value.status_code == 403

        response = collaboration.respond_to_review(
            token=token,
            kind="approve",
            body="I am accountable for the launch decision.",
        )
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
            reanalysis_debounce_seconds=0,
        )
        queued = application.apply_reviewer_attestation(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=issue.id,
            reviewer_name=response["reviewer_name"],
            response_kind=response["response_kind"],
            body=response["body"],
            key=f"review:{response['id']}",
        )
        collaboration.link_review_run(response_id=UUID(response["id"]), run_id=queued.id)

        with engine.connect() as connection:
            stored = connection.execute(
                text(
                    """
                    select r.basis, r.evidence_ref, r.attributed_to,
                           r.analysis_run_id, i.current_status
                    from public.project_review_responses r
                    join public.issues i
                      on i.project_id = r.project_id
                     and i.stable_key = r.issue_stable_key
                    where r.id = :response_id
                    """
                ),
                {"response_id": UUID(response["id"])},
            ).mappings().one()
            events = set(
                connection.execute(
                    text(
                        """
                        select event_type from public.outbox_events
                        where aggregate_id = :response_id
                        """
                    ),
                    {"response_id": UUID(response["id"])},
                ).scalars()
            )
            stale_state = connection.execute(
                text(
                    """
                    select delivery_state::text, revoked_at, withdrawn_at, token_version
                    from public.project_review_grants
                    where reviewer_name = 'First reviewer' and project_id = :project_id
                    """
                ),
                {"project_id": project_id},
            ).mappings().one()
            review_history = connection.execute(
                text(
                    """
                    select summary, detail
                    from public.project_history_events
                    where project_id = :project_id
                      and event_type = 'collaboration.reviewer_approve'
                    order by id desc
                    limit 1
                    """
                ),
                {"project_id": project_id},
            ).mappings().one()
        assert stored["basis"] == "answered"
        assert stored["evidence_ref"] == "launch-brief.md#ownership"
        assert stored["attributed_to"]["display_name"] == "Amina Khan"
        assert stored["analysis_run_id"] == queued.id
        assert stored["current_status"] == "addressed"
        assert events == {
            "review.responded",
            "notify.routed_response",
            "invite.drafted",
        }
        assert stale_state["delivery_state"] == "withdrawn"
        assert stale_state["revoked_at"] is not None
        assert stale_state["withdrawn_at"] is not None
        assert stale_state["token_version"] == 1
        assert review_history["summary"] == "Reviewer confirmed"
        assert review_history["detail"] == (
            "Amina Khan submitted a confirmation response."
        )
        workspace = DatabaseSliceOneApplication(
            engine=engine,
            mailer=object(),  # type: ignore[arg-type]
            web_url="http://127.0.0.1:3002",
        ).get_workspace_summary(
            actor_user_id=workspace_owner_id,
            workspace_id=WORKSPACE_ID,
        )
        review_notification = next(
            item
            for item in workspace.notifications
            if item.key == f"review:{response['id']}"
        )
        assert review_notification.title == "Amina Khan confirmed the requested evidence"
        collaboration_state = collaboration.state(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
        )
        share_state = next(
            item
            for item in collaboration_state["share_links"]
            if item["id"] == shared["id"]
        )
        assert share_state["recipient_name"] == "Executive sponsor"
        assert share_state["first_viewed_at"] is not None
        assert share_state["last_viewed_at"] is not None
        with engine.connect() as connection:
            before_projection_reads = {
                "attestations": connection.execute(
                    text("select count(*) from public.issue_attestations where project_id = :id"),
                    {"id": project_id},
                ).scalar_one(),
                "history": connection.execute(
                    text(
                        "select count(*) from public.project_history_events "
                        "where project_id = :id"
                    ),
                    {"id": project_id},
                ).scalar_one(),
            }
        projection_writes: list[str] = []

        def reject_projection_write(
            _connection,
            _cursor,
            statement,
            _parameters,
            _context,
            _executemany,
        ) -> None:
            normalized = statement.lstrip().lower()
            if not normalized.startswith(("select", "with")):
                projection_writes.append(statement)
                raise AssertionError("Collaboration projections attempted a write")

        sqlalchemy_event.listen(engine, "before_cursor_execute", reject_projection_write)
        try:
            roll_up = collaboration.roll_up(
                actor_user_id=workspace_owner_id,
                project_id=project_id,
            )
            grounding_map = collaboration.grounding_map(
                actor_user_id=workspace_owner_id,
                project_id=project_id,
            )
        finally:
            sqlalchemy_event.remove(engine, "before_cursor_execute", reject_projection_write)
        assert projection_writes == []
        assert roll_up["integrity"]["limiting_pillar"]
        assert any(item["issue_id"] == issue.id for item in roll_up["decision_queue"])
        node = next(item for item in grounding_map["nodes"] if item["issue_id"] == issue.id)
        assert node["state"] == "addressed"
        assert node["href"].endswith(f"/issues?issue={issue.id}")
        with engine.connect() as connection:
            after_projection_reads = {
                "attestations": connection.execute(
                    text("select count(*) from public.issue_attestations where project_id = :id"),
                    {"id": project_id},
                ).scalar_one(),
                "history": connection.execute(
                    text(
                        "select count(*) from public.project_history_events "
                        "where project_id = :id"
                    ),
                    {"id": project_id},
                ).scalar_one(),
            }
        assert after_projection_reads == before_projection_reads

        # Land two distinct reviewer responses in sequence. Accepted reviewer
        # evidence is cumulative: the second Deep Pass must not reopen the issue
        # grounded by the first response.
        application._execute(queued.id)
        first_landed = store.current_snapshot(project_id)
        assert first_landed is not None
        second_issue = next(
            candidate
            for candidate in first_landed.assessment.issues
            if candidate.id != issue.id
        )
        second_grant = collaboration.create_review_grant(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=second_issue.id,
            reviewer_name="Omar Saleem",
            reviewer_email=None,
            question="What evidence confirms this issue is addressed?",
            source_ref="launch-brief.md#delivery",
            source_excerpt="The delivery dependency still needs an accountable response.",
        )
        second_response = collaboration.respond_to_review(
            token=second_grant["url"].rsplit("/", 1)[-1],
            kind="approve",
            body="I confirm the dependency owner and the recorded fallback.",
        )
        second_run = application.apply_reviewer_attestation(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            issue_id=second_issue.id,
            reviewer_name=second_response["reviewer_name"],
            response_kind=second_response["response_kind"],
            body=second_response["body"],
            key=f"review:{second_response['id']}",
        )
        collaboration.link_review_run(
            response_id=UUID(second_response["id"]),
            run_id=second_run.id,
        )
        application._execute(second_run.id)

        with engine.connect() as connection:
            cumulative_statuses = dict(
                connection.execute(
                    text(
                        """
                        select stable_key, current_status::text
                        from public.issues
                        where project_id = :project_id
                          and stable_key in (:first_issue, :second_issue)
                        """
                    ),
                    {
                        "project_id": project_id,
                        "first_issue": issue.id,
                        "second_issue": second_issue.id,
                    },
                ).all()
            )
            current_history_detail = connection.execute(
                text(
                    """
                    select detail
                    from public.project_history_events
                    where project_id = :project_id
                      and analysis_run_id = :run_id
                      and event_type = 'issues.reconciled'
                    """
                ),
                {"project_id": project_id, "run_id": second_run.id},
            ).scalar_one()
        assert cumulative_statuses == {
            issue.id: "resolved",
            second_issue.id: "resolved",
        }
        assert "1 resolved" in current_history_detail

        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.assessment_snapshots
                    set snapshot_json = jsonb_set(
                      snapshot_json,
                      '{summary}',
                      to_jsonb(cast('The read contains 99 open findings.' as text))
                    )
                    where project_id = :project_id
                      and published_at = (
                        select max(published_at)
                        from public.assessment_snapshots
                        where project_id = :project_id
                      )
                    """
                ),
                {"project_id": project_id},
            )
        post_review_share = collaboration.create_snapshot_link(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            recipient_name="Post-review sponsor",
            recipient_email=None,
        )
        shared_after_reviews = collaboration.resolve_snapshot(
            post_review_share["url"].rsplit("/", 1)[-1]
        )
        shared_statuses = {
            item["id"]: item.get("status")
            for item in shared_after_reviews["snapshot_json"]["assessment"]["issues"]
        }
        assert "99 open findings" not in shared_after_reviews["snapshot_json"]["summary"]
        assert shared_statuses[issue.id] == "resolved"
        assert shared_statuses[second_issue.id] == "resolved"

        collaboration.revoke_share_link(
            actor_user_id=workspace_owner_id,
            project_id=project_id,
            link_id=UUID(shared["id"]),
        )
        with pytest.raises(CollaborationError) as revoked_share_error:
            collaboration.resolve_snapshot(share_token)
        assert revoked_share_error.value.code == "LINK_UNAVAILABLE"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )
        engine.dispose()


def test_postgres_analysis_is_checkpointed_and_published_atomically(
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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


def test_work_breakdown_tasks_project_into_schedule_and_resources(
    tmp_path,
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Shared task projection', 'draft', :owner_id)
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
                idempotency_key=f"shared-task-baseline:{project_id}",
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
        work_breakdown = application.get_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="work_breakdown",
        )
        task_id = "work-breakdown-section-1-row-2"
        content = {
            "sections": [
                {
                    "id": "work-breakdown-section-1",
                    "heading": "Commerce launch",
                    "body": "",
                    "bullets": [],
                    "columns": ["WBS", "Item"],
                    "rows": [
                        ["1.0", "Release readiness"],
                        ["1.1", "Validate production support handoff"],
                    ],
                    "row_ids": ["work-breakdown-section-1-row-1", task_id],
                    "row_evidence_refs": [[], []],
                    "row_states": ["confirmed", "confirmed"],
                    "row_provenance": ["confirmed_by_user", "confirmed_by_user"],
                    "provenance": "confirmed_by_user",
                    "evidence_refs": [],
                }
            ]
        }
        edited, run = application.update_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="work_breakdown",
            content=content,
            expected_version=work_breakdown["version"],
            key=f"shared-task-add:{project_id}",
        )
        assert run is not None

        for artifact_type in ("schedule", "resources"):
            projected = application.get_artifact(
                actor_user_id=owner_id,
                project_id=project_id,
                artifact_type=artifact_type,
            )
            rows = [
                (row_id, row)
                for section in projected["content"]["sections"]
                for row_id, row in zip(section.get("row_ids", []), section["rows"], strict=True)
            ]
            matching = [row for row_id, row in rows if row_id == task_id]
            assert len(matching) == 1
            assert "Validate production support handoff" in matching[0]

        content["sections"][0]["rows"] = content["sections"][0]["rows"][:1]
        content["sections"][0]["row_ids"] = content["sections"][0]["row_ids"][:1]
        content["sections"][0]["row_evidence_refs"] = [[]]
        content["sections"][0]["row_states"] = ["confirmed"]
        content["sections"][0]["row_provenance"] = ["confirmed_by_user"]
        application.update_artifact(
            actor_user_id=owner_id,
            project_id=project_id,
            artifact_type="work_breakdown",
            content=content,
            expected_version=edited["version"],
            key=f"shared-task-remove:{project_id}",
        )
        for artifact_type in ("schedule", "resources"):
            projected = application.get_artifact(
                actor_user_id=owner_id,
                project_id=project_id,
                artifact_type=artifact_type,
            )
            assert all(
                task_id not in section.get("row_ids", [])
                for section in projected["content"]["sections"]
            )
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_new_snapshot_does_not_resolve_issue_rows_without_resolution_evidence(
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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
            reconciled_summary = connection.execute(
                text(
                    """
                    select summary from public.project_history_events
                    where project_id = :project_id
                      and analysis_run_id = :run_id
                      and event_type = 'issues.reconciled'
                    """
                ),
                {"project_id": project_id, "run_id": result.run_id},
            ).scalar_one()
        assert stale_status == "open"
        current_snapshot = DatabaseAnalysisStore(engine).current_snapshot(project_id)
        assert current_snapshot is not None
        current_open_count = sum(
            issue.status != "resolved"
            for issue in current_snapshot.assessment.issues
        )
        assert reconciled_summary == f"{current_open_count} issues detected"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_new_snapshot_preserves_lifecycle_state_for_a_repeated_issue(
    workspace_owner_id: UUID,
) -> None:
    """Publishing a read must not briefly replace a durable owner decision."""
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Repeated issue lifecycle', 'draft', :owner_id)
                """
            ),
            {"id": project_id, "workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    try:
        store = DatabaseAnalysisStore(engine)
        workflow = AnalysisWorkflow(
            store=store,
            harness=DeterministicAgentHarness(),
        )
        request = AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=project_id,
            requested_by=owner_id,
            kind=RunKind.INITIAL,
            description="A delivery plan with an unresolved owner and fallback.",
            source_names=("brief.md",),
            idempotency_key=f"integration-repeated-lifecycle:first:{project_id}",
        )
        first = workflow.run(request)
        assert first.status is AnalysisRunStatus.COMPLETED
        first_snapshot = store.current_snapshot(project_id)
        assert first_snapshot is not None
        issue_id = first_snapshot.assessment.issues[0].id

        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = 'resolved', updated_at = now()
                    where project_id = :project_id and stable_key = :issue_id
                    """
                ),
                {"project_id": project_id, "issue_id": issue_id},
            )

        second = workflow.run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=owner_id,
                kind=RunKind.EXTENDED,
                description=request.description,
                source_names=request.source_names,
                idempotency_key=f"integration-repeated-lifecycle:second:{project_id}",
                parent_run_id=first.run_id,
            )
        )
        assert second.status is AnalysisRunStatus.COMPLETED
        second_snapshot = store.current_snapshot(project_id)
        assert second_snapshot is not None
        assert any(issue.id == issue_id for issue in second_snapshot.assessment.issues)

        with engine.connect() as connection:
            current_status = connection.execute(
                text(
                    """
                    select current_status from public.issues
                    where project_id = :project_id and stable_key = :issue_id
                    """
                ),
                {"project_id": project_id, "issue_id": issue_id},
            ).scalar_one()
        assert current_status == "resolved"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_workspace_summary_projects_current_issue_statuses(
    workspace_owner_id: UUID,
) -> None:
    """PF workspace awareness must agree with the current Issue projection."""
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values (:id, :workspace_id, 'Workspace issue projection', 'draft', :owner_id)
                """
            ),
            {
                "id": project_id,
                "workspace_id": WORKSPACE_ID,
                "owner_id": workspace_owner_id,
            },
        )
    try:
        result = AnalysisWorkflow(
            store=DatabaseAnalysisStore(engine),
            harness=DeterministicAgentHarness(),
        ).run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=workspace_owner_id,
                kind=RunKind.INITIAL,
                description="A delivery plan with a confirmed owner and fallback.",
                source_names=("brief.md",),
                idempotency_key=f"integration-workspace-projection:{project_id}",
            )
        )
        assert result.status is AnalysisRunStatus.COMPLETED

        snapshot = DatabaseAnalysisStore(engine).current_snapshot(project_id)
        assert snapshot is not None
        issue_id = snapshot.assessment.issues[0].id
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = 'resolved', updated_at = now()
                    where project_id = :project_id and stable_key = :issue_id
                    """
                ),
                {"project_id": project_id, "issue_id": issue_id},
            )

        workspace = DatabaseSliceOneApplication(
            engine=engine,
            mailer=object(),  # type: ignore[arg-type]
            web_url="http://127.0.0.1:3002",
        ).get_workspace_summary(
            actor_user_id=workspace_owner_id,
            workspace_id=WORKSPACE_ID,
        )
        project = next(item for item in workspace.projects if item.id == project_id)
        assert project.open_issues == len(snapshot.assessment.issues) - 1
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.projects where id = :id"),
                {"id": project_id},
            )


def test_history_falls_back_to_retained_snapshots_when_legacy_events_are_absent(
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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


def test_analysis_promotes_a_supported_title_and_increments_artifact_revisions(
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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
                pass_kind=AnalysisPassKind.DEEP,
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
    workspace_owner_id: UUID,
) -> None:
    engine = create_engine(SETTINGS.database_url)
    project_id = uuid4()
    owner_id = workspace_owner_id
    with engine.begin() as connection:
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

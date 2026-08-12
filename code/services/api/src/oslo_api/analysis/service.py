import json
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from time import sleep
from typing import Protocol
from uuid import UUID, uuid4

from sqlalchemy import Engine, create_engine, text

from oslo_api.analysis import (
    AnalysisEvent,
    AnalysisPassKind,
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    AnalysisWorkflow,
    AssessmentSnapshot,
    DeterministicAgentHarness,
    ReanalysisTrigger,
    RunKind,
)
from oslo_api.analysis.artifact_edits import (
    artifact_content_hash,
    build_user_edit_evidence,
)
from oslo_api.analysis.document_store import DatabaseDocumentStore
from oslo_api.analysis.harness import AgentHarness
from oslo_api.analysis.history import append_history_event, list_project_history
from oslo_api.analysis.job_queue import DatabaseAnalysisJobQueue
from oslo_api.analysis.models import EvidenceFragment
from oslo_api.analysis.object_storage import LocalObjectStorage, SupabaseObjectStorage
from oslo_api.analysis.openai_harness import OpenAIAgentHarness
from oslo_api.analysis.persistence import DatabaseAnalysisStore
from oslo_api.analysis.user_evidence import (
    build_clarification_evidence,
    build_reviewer_evidence,
)
from oslo_api.settings import Settings
from oslo_api.slice_two import (
    SliceTwoArtifactConflict,
    SliceTwoIssueNotAnswerable,
    SliceTwoNotFound,
    SliceTwoPermissionDenied,
)
from oslo_api.tiering.repository import get_workspace_plan


class AnalysisDispatcher(Protocol):
    def submit(self, function: Callable[[UUID], object], run_id: UUID) -> object: ...


class DatabaseSliceTwoApplication:
    def __init__(
        self,
        *,
        engine: Engine,
        store: DatabaseAnalysisStore,
        workflow: AnalysisWorkflow,
        executor: AnalysisDispatcher,
        document_store: DatabaseDocumentStore,
        extended_delay_seconds: float = 0.5,
        reanalysis_debounce_seconds: float = 1.5,
        read_moved_immediate_threshold_seconds: float = 5,
        read_moved_linger_seconds: float = 16,
        first_run_unlock_threshold: int = 2,
    ) -> None:
        self._engine = engine
        self._store = store
        self._workflow = workflow
        self._executor = executor
        self._document_store = document_store
        self._extended_delay_seconds = extended_delay_seconds
        self._reanalysis_debounce_seconds = reanalysis_debounce_seconds
        self._read_moved_immediate_threshold_seconds = read_moved_immediate_threshold_seconds
        self._read_moved_linger_seconds = read_moved_linger_seconds
        self._first_run_unlock_threshold = first_run_unlock_threshold

    def upload_document(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        file_name: str,
        content_type: str | None,
        content: bytes,
    ):
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        with self._engine.connect() as connection:
            policy = get_workspace_plan(connection, workspace_id)
        return self._document_store.ingest(
            workspace_id=workspace_id,
            project_id=project_id,
            submitted_by=actor_user_id,
            file_name=file_name,
            declared_content_type=content_type,
            content=content,
            document_limit=policy.document_limit,
            word_limit=policy.word_limit,
        )

    def start_analysis(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        description: str,
        source_names: tuple[str, ...],
        source_document_ids: tuple[UUID, ...],
        kind: RunKind,
        key: str,
    ) -> AnalysisRun:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        self._validate_documents(
            workspace_id=workspace_id,
            project_id=project_id,
            document_ids=source_document_ids,
        )
        request = AnalysisRunRequest(
            workspace_id=workspace_id,
            project_id=project_id,
            requested_by=actor_user_id,
            kind=kind,
            description=description,
            source_names=source_names,
            source_document_ids=source_document_ids,
            idempotency_key=key,
            consumes_analysis_allowance=True,
        )
        run = self._store.create_run(request)
        if run.status is AnalysisRunStatus.QUEUED:
            self._executor.submit(self._execute, run.id)
        return run

    def refresh_analysis(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        key: str,
    ) -> AnalysisRun:
        self._workspace_for_project(actor_user_id, project_id)
        previous = self._store.latest_run_for_project(project_id, RunKind.INITIAL)
        if previous is None:
            raise SliceTwoNotFound
        if previous.status in {AnalysisRunStatus.QUEUED, AnalysisRunStatus.RUNNING}:
            return previous
        return self.start_analysis(
            actor_user_id=actor_user_id,
            project_id=project_id,
            description=previous.request.description,
            source_names=previous.request.source_names,
            source_document_ids=previous.request.source_document_ids,
            kind=RunKind.INITIAL,
            key=key,
        )

    def get_run(self, *, actor_user_id: UUID, run_id: UUID) -> AnalysisRun:
        run = self._store.get_run(run_id)
        if run is None:
            raise SliceTwoNotFound
        self._workspace_for_project(actor_user_id, run.request.project_id)
        return run

    def events_after(
        self,
        *,
        actor_user_id: UUID,
        run_id: UUID,
        sequence: int,
    ) -> tuple[AnalysisEvent, ...]:
        self.get_run(actor_user_id=actor_user_id, run_id=run_id)
        return self._store.events_after(run_id, sequence)

    def wait_for_events(
        self,
        *,
        actor_user_id: UUID,
        run_id: UUID,
        sequence: int,
        timeout: float,
    ) -> tuple[AnalysisEvent, ...]:
        self.get_run(actor_user_id=actor_user_id, run_id=run_id)
        return self._store.wait_for_events(run_id, sequence, timeout)

    def current_overview(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> AssessmentSnapshot:
        self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        return snapshot

    def latest_extended_run(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> AnalysisRun | None:
        self._workspace_for_project(actor_user_id, project_id)
        return self._store.latest_run_for_project(project_id, RunKind.EXTENDED)

    def list_history(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        category: str,
        cursor: str | None,
        limit: int,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        return list_project_history(
            self._engine,
            workspace_id=workspace_id,
            project_id=project_id,
            category=category,
            cursor=cursor,
            limit=limit,
        )

    def history_snapshot(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        run_id: UUID,
    ) -> AssessmentSnapshot:
        self._workspace_for_project(actor_user_id, project_id)
        run = self._store.get_run(run_id)
        if run is None or run.request.project_id != project_id:
            raise SliceTwoNotFound
        snapshot = self._store.snapshot_for_run(run_id)
        if snapshot is None:
            raise SliceTwoNotFound
        return snapshot

    def retry(self, *, actor_user_id: UUID, run_id: UUID) -> AnalysisRun:
        run = self.get_run(actor_user_id=actor_user_id, run_id=run_id)
        if run.status is not AnalysisRunStatus.FAILED:
            return run
        with self._engine.begin() as connection:
            append_history_event(
                connection,
                workspace_id=run.request.workspace_id,
                project_id=run.request.project_id,
                analysis_run_id=run.id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type="analysis.retry_requested",
                summary="Analysis retry requested",
                detail="The same governed run resumed from durable state.",
                idempotency_key=f"history:analysis-retry:{run.id}",
            )
        self._store.queue_run(run.id)
        self._executor.submit(self._execute, run.id)
        return self._store.get_run(run.id) or run

    def answer_issue(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        answer: str,
        key: str,
    ) -> AnalysisRun:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        issue = next(
            (candidate for candidate in snapshot.assessment.issues if candidate.id == issue_id),
            None,
        )
        if issue is None:
            raise SliceTwoNotFound
        if issue.clarification is None or issue.status == "resolved":
            raise SliceTwoIssueNotAnswerable

        with self._engine.begin() as connection:
            answer_row = (
                connection.execute(
                    text(
                        """
                    insert into public.issue_answers (
                      workspace_id, project_id, issue_stable_key, answered_by,
                      answer, idempotency_key
                    ) values (
                      :workspace_id, :project_id, :issue_id, :answered_by,
                      :answer, :idempotency_key
                    )
                    on conflict (workspace_id, idempotency_key) do update set
                      answer = public.issue_answers.answer
                    returning analysis_run_id, answer
                    """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                        "answered_by": actor_user_id,
                        "answer": answer,
                        "idempotency_key": key,
                    },
                )
                .mappings()
                .one()
            )
        if answer_row["analysis_run_id"] is not None:
            existing = self._store.get_run(answer_row["analysis_run_id"])
            if existing is not None:
                return existing

        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound
        stored_answer = str(answer_row["answer"])
        clarification_evidence = build_clarification_evidence(
            issue_id=issue.id,
            issue_title=issue.title,
            question=issue.clarification or "Clarification requested",
            answer=stored_answer,
            answer_key=key,
        )
        run = self._batched_reanalysis_run(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            project_id=project_id,
            parent_run=parent_run,
            evidence=(clarification_evidence,),
            event_key=f"clarification:{key}",
            change_kind="confirm",
            scope=issue.artifact_type.value,
            consumes_analysis_allowance=True,
        )
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.issue_answers
                    set analysis_run_id = :run_id
                    where workspace_id = :workspace_id
                      and idempotency_key = :idempotency_key
                    """
                ),
                {
                    "run_id": run.id,
                    "workspace_id": workspace_id,
                    "idempotency_key": key,
                },
            )
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = 'addressed', updated_at = now()
                    where workspace_id = :workspace_id
                      and project_id = :project_id
                      and stable_key = :issue_id
                      and current_status <> 'resolved'
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                },
            )
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=run.id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type="clarification.answered",
                summary="Clarification answered",
                detail=f"Answered the clarification for “{issue.title}”.",
                issue_id=issue_id,
                idempotency_key=f"history:clarification:{key}",
            )
        return run

    def apply_reviewer_attestation(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str | None,
        reviewer_name: str,
        response_kind: str,
        body: str,
        key: str,
    ) -> AnalysisRun:
        """Re-run from reviewer evidence without mutating the issue lifecycle.

        Reviewer approval is evidence, not a user decision. The governed analysis
        may change the read, but the reviewer response never marks an issue
        addressed or resolved.
        """

        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound
        issue_title = "Project review"
        issue_scope = "project"
        if issue_id:
            issue = next(
                (candidate for candidate in snapshot.assessment.issues if candidate.id == issue_id),
                None,
            )
            if issue is None:
                raise SliceTwoNotFound
            issue_title = issue.title
            issue_scope = issue.artifact_type.value
        reviewer_evidence = build_reviewer_evidence(
            response_key=key,
            reviewer_name=reviewer_name,
            issue_id=issue_id,
            issue_title=issue_title,
            response_kind=response_kind,
            body=body,
        )
        run = self._batched_reanalysis_run(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            project_id=project_id,
            parent_run=parent_run,
            evidence=(reviewer_evidence,),
            event_key=f"review:{key}",
            change_kind="route",
            scope=issue_scope,
            consumes_analysis_allowance=False,
        )
        with self._engine.begin() as connection:
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=run.id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type="review.responded",
                summary=f"Reviewer {response_kind.replace('_', ' ')}",
                detail=f"{reviewer_name} responded to “{issue_title}”.",
                issue_id=issue_id,
                idempotency_key=f"history:review:{key}",
            )
        return run

    def act_on_issue(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        action: str,
        resolution: str,
        key: str,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        issue = next(
            (candidate for candidate in snapshot.assessment.issues if candidate.id == issue_id),
            None,
        )
        if issue is None:
            raise SliceTwoNotFound
        if issue.status == "resolved":
            raise SliceTwoIssueNotAnswerable

        with self._engine.begin() as connection:
            existing = (
                connection.execute(
                    text(
                        """
                        select issue_stable_key, action_type, resolution_text,
                               artifact_type, artifact_version, analysis_run_id
                        from public.issue_actions
                        where workspace_id = :workspace_id
                          and idempotency_key = :idempotency_key
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "idempotency_key": key,
                    },
                )
                .mappings()
                .one_or_none()
            )
        if existing is not None:
            run = (
                self._store.get_run(existing["analysis_run_id"])
                if existing["analysis_run_id"] is not None
                else None
            )
            return {
                "issue_id": str(existing["issue_stable_key"]),
                "action": str(existing["action_type"]),
                "selected_resolution": str(existing["resolution_text"]),
                "artifact_type": (
                    str(existing["artifact_type"])
                    if existing["artifact_type"] is not None
                    else None
                ),
                "artifact_version": existing["artifact_version"],
                "analysis_run": run,
                "status": "addressed",
            }

        if action == "select":
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        insert into public.issue_actions (
                          workspace_id, project_id, issue_stable_key, acted_by,
                          action_type, resolution_text, artifact_type,
                          idempotency_key
                        ) values (
                          :workspace_id, :project_id, :issue_id, :acted_by,
                          :action_type, :resolution_text,
                          cast(:artifact_type as public.plan_artifact_type),
                          :idempotency_key
                        )
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                        "acted_by": actor_user_id,
                        "action_type": action,
                        "resolution_text": resolution,
                        "artifact_type": issue.artifact_type.value,
                        "idempotency_key": key,
                    },
                )
                connection.execute(
                    text(
                        """
                        update public.issues
                        set current_status = 'addressed', updated_at = now()
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and stable_key = :issue_id
                          and current_status <> 'resolved'
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                    },
                )
                append_history_event(
                    connection,
                    workspace_id=workspace_id,
                    project_id=project_id,
                    analysis_run_id=snapshot.analysis_run_id,
                    actor_id=actor_user_id,
                    actor_type="user",
                    category="decisions",
                    event_type="issue.resolution_selected",
                    summary="Resolution selected",
                    detail=f"Selected a proposed response for “{issue.title}”.",
                    issue_id=issue_id,
                    artifact_type=issue.artifact_type.value,
                    idempotency_key=f"history:issue-action:{key}",
                )
            return {
                "issue_id": issue_id,
                "action": action,
                "selected_resolution": resolution,
                "artifact_type": issue.artifact_type.value,
                "artifact_version": None,
                "analysis_run": None,
                "status": "addressed",
            }

        artifact = self.get_artifact(
            actor_user_id=actor_user_id,
            project_id=project_id,
            artifact_type=issue.artifact_type.value,
        )
        content = dict(artifact["content"])
        sections = list(content.get("sections", []))
        sections.append(
            {
                "heading": "Confirmed resolution",
                "body": resolution,
                "bullets": [],
                "columns": [],
                "rows": [],
            }
        )
        content["sections"] = sections
        resolution_evidence = build_clarification_evidence(
            issue_id=issue.id,
            issue_title=issue.title,
            question=(issue.clarification or "What governed change addresses this issue?"),
            answer=resolution,
            answer_key=key,
        )
        updated_artifact, run = self.update_artifact(
            actor_user_id=actor_user_id,
            project_id=project_id,
            artifact_type=issue.artifact_type.value,
            content=content,
            expected_version=int(artifact["version"]),
            key=f"issue-action:{key}",
            issue_evidence=resolution_evidence,
        )
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    insert into public.issue_actions (
                      workspace_id, project_id, issue_stable_key, acted_by,
                      action_type, resolution_text, artifact_type,
                      artifact_version, analysis_run_id, idempotency_key
                    ) values (
                      :workspace_id, :project_id, :issue_id, :acted_by,
                      :action_type, :resolution_text,
                      cast(:artifact_type as public.plan_artifact_type),
                      :artifact_version, :analysis_run_id, :idempotency_key
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                    "acted_by": actor_user_id,
                    "action_type": action,
                    "resolution_text": resolution,
                    "artifact_type": issue.artifact_type.value,
                    "artifact_version": updated_artifact["version"],
                    "analysis_run_id": run.id,
                    "idempotency_key": key,
                },
            )
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = 'addressed', updated_at = now()
                    where workspace_id = :workspace_id
                      and project_id = :project_id
                      and stable_key = :issue_id
                      and current_status <> 'resolved'
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                },
            )
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=run.id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type=f"issue.resolution_{action}",
                summary="Resolution applied",
                detail=f"Applied a governed change for “{issue.title}”.",
                issue_id=issue_id,
                artifact_type=issue.artifact_type.value,
                artifact_version=updated_artifact["version"],
                idempotency_key=f"history:issue-action:{key}",
            )
        return {
            "issue_id": issue_id,
            "action": action,
            "selected_resolution": resolution,
            "artifact_type": issue.artifact_type.value,
            "artifact_version": updated_artifact["version"],
            "analysis_run": run,
            "status": "addressed",
        }

    def list_issue_actions(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> list[dict]:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        with self._engine.begin() as connection:
            lifecycle_by_issue = {
                str(row["stable_key"]): str(row["current_status"])
                for row in connection.execute(
                    text(
                        """
                        select stable_key, current_status
                        from public.issues
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                    },
                ).mappings()
            }
            actions = (
                connection.execute(
                    text(
                        """
                        select distinct on (issue_stable_key)
                               issue_stable_key, action_type, resolution_text,
                               artifact_type, artifact_version, analysis_run_id,
                               created_at
                        from public.issue_actions
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                        order by issue_stable_key, created_at desc
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                    },
                )
                .mappings()
                .all()
            )
            answers = (
                connection.execute(
                    text(
                        """
                        select distinct on (issue_stable_key)
                               issue_stable_key, answer, analysis_run_id, created_at
                        from public.issue_answers
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                        order by issue_stable_key, created_at desc
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                    },
                )
                .mappings()
                .all()
            )
        updates = [
            {
                "issue_id": str(action["issue_stable_key"]),
                "action": str(action["action_type"]),
                "status": lifecycle_by_issue.get(str(action["issue_stable_key"]), "open"),
                "selected_resolution": str(action["resolution_text"]),
                "artifact_type": (
                    str(action["artifact_type"]) if action["artifact_type"] is not None else None
                ),
                "artifact_version": action["artifact_version"],
                "analysis_run": (
                    self._store.get_run(action["analysis_run_id"])
                    if action["analysis_run_id"] is not None
                    else None
                ),
                "created_at": action["created_at"],
            }
            for action in actions
        ]
        updates.extend(
            {
                "issue_id": str(answer["issue_stable_key"]),
                "action": "clarification",
                "status": lifecycle_by_issue.get(str(answer["issue_stable_key"]), "open"),
                "selected_resolution": None,
                "artifact_type": None,
                "artifact_version": None,
                "analysis_run": (
                    self._store.get_run(answer["analysis_run_id"])
                    if answer["analysis_run_id"] is not None
                    else None
                ),
                "created_at": answer["created_at"],
            }
            for answer in answers
        )
        latest_by_issue: dict[str, dict] = {}
        for update in sorted(updates, key=lambda item: item["created_at"], reverse=True):
            latest_by_issue.setdefault(update["issue_id"], update)
        return list(latest_by_issue.values())

    def get_artifact(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        artifact_type: str,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        artifact = next(
            (
                candidate
                for candidate in snapshot.artifacts
                if candidate.artifact_type.value == artifact_type
            ),
            None,
        )
        if artifact is None:
            raise SliceTwoNotFound
        with self._engine.begin() as connection:
            draft = (
                connection.execute(
                    text(
                        """
                        select content_json, version, provenance, updated_at
                        from public.artifact_drafts
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and artifact_type = cast(:artifact_type as public.plan_artifact_type)
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "artifact_type": artifact_type,
                    },
                )
                .mappings()
                .one_or_none()
            )
            analysis_revision = connection.execute(
                text(
                    """
                    select revision
                    from public.artifact_versions
                    where analysis_run_id = :run_id
                      and artifact_type = cast(
                        :artifact_type as public.plan_artifact_type
                      )
                    """
                ),
                {
                    "run_id": snapshot.analysis_run_id,
                    "artifact_type": artifact_type,
                },
            ).scalar_one_or_none()
        content = (
            dict(draft["content_json"]) if draft is not None else self._artifact_content(artifact)
        )
        open_issues = [
            issue
            for issue in snapshot.assessment.issues
            if issue.artifact_type.value == artifact_type and issue.status != "resolved"
        ]
        return {
            "artifact_type": artifact_type,
            "title": artifact.title,
            "content": content,
            "version": (
                int(draft["version"]) if draft is not None else int(analysis_revision or 1)
            ),
            "provenance": (str(draft["provenance"]) if draft is not None else "from_oslo"),
            "reliability": artifact.reliability,
            "basis": artifact.basis,
            "evidence_refs": list(artifact.evidence_refs),
            "assumptions": [
                {
                    "id": assumption.id,
                    "statement": assumption.statement,
                    "state": assumption.state,
                    "load_bearing": assumption.load_bearing,
                    "evidence_refs": list(assumption.evidence_refs),
                }
                for assumption in artifact.assumptions
            ],
            "conflicts": [
                {
                    "id": conflict.id,
                    "field": conflict.field,
                    "values": list(conflict.values),
                    "evidence_refs": list(conflict.evidence_refs),
                }
                for conflict in artifact.conflicts
            ],
            "evidence_citations": list(snapshot.evidence_citations),
            "issues": open_issues,
            "updated_at": (draft["updated_at"] if draft is not None else snapshot.published_at),
        }

    def update_artifact(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        artifact_type: str,
        content: dict,
        expected_version: int,
        key: str,
        issue_evidence: EvidenceFragment | None = None,
    ) -> tuple[dict, AnalysisRun | None]:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        artifact = next(
            (
                candidate
                for candidate in snapshot.artifacts
                if candidate.artifact_type.value == artifact_type
            ),
            None,
        )
        if artifact is None:
            raise SliceTwoNotFound
        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound
        with self._engine.begin() as connection:
            existing = (
                connection.execute(
                    text(
                        """
                        select id, version, content_json
                        from public.artifact_drafts
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and artifact_type = cast(:artifact_type as public.plan_artifact_type)
                        for update
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "artifact_type": artifact_type,
                    },
                )
                .mappings()
                .one_or_none()
            )
            current_version = (
                int(existing["version"])
                if existing is not None
                else int(
                    connection.execute(
                        text(
                            """
                            select revision
                            from public.artifact_versions
                            where analysis_run_id = :run_id
                              and artifact_type = cast(
                                :artifact_type as public.plan_artifact_type
                              )
                            """
                        ),
                        {
                            "run_id": snapshot.analysis_run_id,
                            "artifact_type": artifact_type,
                        },
                    ).scalar_one_or_none()
                    or 1
                )
            )
            if current_version != expected_version:
                raise SliceTwoArtifactConflict
            current_content = (
                dict(existing["content_json"])
                if existing is not None
                else self._artifact_content(artifact)
            )
            if artifact_content_hash(current_content) == artifact_content_hash(content):
                return (
                    self.get_artifact(
                        actor_user_id=actor_user_id,
                        project_id=project_id,
                        artifact_type=artifact_type,
                    ),
                    None,
                )
            next_version = current_version + 1
            if existing is None:
                draft = (
                    connection.execute(
                        text(
                            """
                            insert into public.artifact_drafts (
                              workspace_id, project_id, artifact_type, source_snapshot_id,
                              content_json, version, provenance, updated_by
                            ) values (
                              :workspace_id, :project_id,
                              cast(:artifact_type as public.plan_artifact_type),
                              :snapshot_id, cast(:content as jsonb), :version,
                              'mixed', :updated_by
                            )
                            returning id
                            """
                        ),
                        {
                            "workspace_id": workspace_id,
                            "project_id": project_id,
                            "artifact_type": artifact_type,
                            "snapshot_id": snapshot.id,
                            "content": json.dumps(content),
                            "version": next_version,
                            "updated_by": actor_user_id,
                        },
                    )
                    .mappings()
                    .one()
                )
                draft_id = draft["id"]
            else:
                draft_id = existing["id"]
                connection.execute(
                    text(
                        """
                        update public.artifact_drafts
                        set source_snapshot_id = :snapshot_id,
                            content_json = cast(:content as jsonb),
                            version = :version,
                            provenance = 'mixed',
                            updated_by = :updated_by,
                            updated_at = now()
                        where id = :draft_id
                        """
                    ),
                    {
                        "snapshot_id": snapshot.id,
                        "content": json.dumps(content),
                        "version": next_version,
                        "updated_by": actor_user_id,
                        "draft_id": draft_id,
                    },
                )
            connection.execute(
                text(
                    """
                    insert into public.artifact_draft_versions (
                      workspace_id, project_id, artifact_type, artifact_draft_id,
                      version, content_json, provenance, changed_by
                    ) values (
                      :workspace_id, :project_id,
                      cast(:artifact_type as public.plan_artifact_type), :draft_id,
                      :version, cast(:content as jsonb), 'mixed', :changed_by
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "artifact_type": artifact_type,
                    "draft_id": draft_id,
                    "version": next_version,
                    "content": json.dumps(content),
                    "changed_by": actor_user_id,
                },
            )

        edit_evidence = build_user_edit_evidence(
            artifact_type=artifact_type,
            version=next_version,
            content=content,
        )
        user_evidence = (edit_evidence,)
        if issue_evidence is not None:
            user_evidence += (issue_evidence,)
        run = self._batched_reanalysis_run(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            project_id=project_id,
            parent_run=parent_run,
            evidence=user_evidence,
            event_key=f"artifact-edit:{key}",
            change_kind="edit",
            scope=artifact_type,
            consumes_analysis_allowance=False,
        )
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.artifact_draft_versions
                    set analysis_run_id = :run_id
                    where artifact_draft_id = :draft_id and version = :version
                    """
                ),
                {"run_id": run.id, "draft_id": draft_id, "version": next_version},
            )
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=run.id,
                actor_id=actor_user_id,
                actor_type="user",
                category="versions",
                event_type="artifact.version_created",
                summary=f"{artifact.title} updated",
                detail=f"Version {next_version} was retained and queued for re-analysis.",
                artifact_type=artifact_type,
                artifact_version=next_version,
                idempotency_key=f"history:artifact-edit:{key}",
            )
        return (
            self.get_artifact(
                actor_user_id=actor_user_id,
                project_id=project_id,
                artifact_type=artifact_type,
            ),
            run,
        )

    @staticmethod
    def _artifact_content(artifact) -> dict:
        if not artifact.sections:
            return DatabaseSliceTwoApplication._default_artifact_content(
                artifact.artifact_type.value,
                artifact.summary,
            )
        return {
            "sections": [
                {
                    "heading": section.heading,
                    "body": section.body,
                    "bullets": list(section.bullets),
                    "columns": list(section.columns),
                    "rows": [list(row) for row in section.rows],
                    "provenance": "from_oslo",
                    "evidence_refs": list(section.evidence_refs),
                    "row_evidence_refs": [
                        list(references) for references in section.row_evidence_refs
                    ],
                    "row_states": list(section.row_states),
                    "row_provenance": ["from_oslo" for _ in section.rows],
                }
                for section in artifact.sections
            ]
        }

    @staticmethod
    def _default_artifact_content(artifact_type: str, summary: str) -> dict:
        if artifact_type == "intent":
            return {
                "sections": [
                    {"heading": "", "body": summary, "bullets": [], "columns": [], "rows": []},
                    {
                        "heading": "What success looks like",
                        "body": "",
                        "bullets": [summary],
                        "columns": [],
                        "rows": [],
                    },
                ]
            }
        if artifact_type == "context":
            return {
                "sections": [
                    {"heading": "", "body": summary, "bullets": [], "columns": [], "rows": []},
                    {
                        "heading": "Stakeholders",
                        "body": "",
                        "bullets": [],
                        "columns": ["Group", "Interest", "Status"],
                        "rows": [],
                    },
                ]
            }
        if artifact_type == "scope":
            return {
                "sections": [
                    {
                        "heading": "In scope",
                        "body": summary,
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    },
                    {
                        "heading": "Out of scope",
                        "body": (
                            "Exclusions were not retained in this legacy summary. "
                            "Re-analyze the project to rebuild structured scope evidence."
                        ),
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    },
                ]
            }
        if artifact_type == "requirements":
            return {
                "sections": [
                    {
                        "heading": "Success metrics",
                        "body": summary,
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    },
                    {
                        "heading": "Acceptance",
                        "body": "",
                        "bullets": [summary],
                        "columns": [],
                        "rows": [],
                    },
                ]
            }
        table_contract = {
            "work_breakdown": ("Workstreams", ["Workstream", "Key deliverable", "Owner"]),
            "schedule": ("Milestones", ["Milestone", "Date", "Status"]),
            "resources": ("Vendors & dependencies", ["Resource", "Role", "Status"]),
        }
        heading, columns = table_contract[artifact_type]
        return {
            "sections": [
                {
                    "heading": heading,
                    "body": summary,
                    "bullets": [],
                    "columns": list(columns),
                    "rows": [],
                }
            ]
        }

    def mark_orientation_seen(self, *, actor_user_id: UUID, workspace_id: UUID) -> None:
        with self._engine.begin() as connection:
            updated = connection.execute(
                text(
                    """
                    update public.memberships
                    set orientation_seen_at = coalesce(orientation_seen_at, now())
                    where workspace_id = :workspace_id and user_id = :user_id
                    """
                ),
                {"workspace_id": workspace_id, "user_id": actor_user_id},
            )
            if updated.rowcount != 1:
                raise SliceTwoPermissionDenied

    def has_seen_orientation(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> bool:
        with self._engine.connect() as connection:
            seen_at = connection.execute(
                text(
                    """
                    select membership.orientation_seen_at
                    from public.projects project
                    join public.memberships membership
                      on membership.workspace_id = project.workspace_id
                    where project.id = :project_id
                      and membership.user_id = :user_id
                    """
                ),
                {"project_id": project_id, "user_id": actor_user_id},
            ).scalar_one_or_none()
        return seen_at is not None

    def runtime_state(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    insert into public.project_read_freshness (
                      workspace_id, project_id, based_on_run_id
                    )
                    select workspace_id, id, current_analysis_run_id
                    from public.projects where id = :project_id
                    on conflict (project_id) do nothing
                    """
                ),
                {"project_id": project_id},
            )
            connection.execute(
                text(
                    """
                    insert into public.project_first_run_states (
                      workspace_id, project_id, user_id, unlock_threshold
                    ) values (
                      :workspace_id, :project_id, :user_id, :unlock_threshold
                    )
                    on conflict (project_id, user_id) do nothing
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "user_id": actor_user_id,
                    "unlock_threshold": self._first_run_unlock_threshold,
                },
            )
            freshness = (
                connection.execute(
                    text(
                        """
                        select state, pending_count, based_on_run_id, active_run_id,
                               last_act_at, last_landed_at
                        from public.project_read_freshness
                        where project_id = :project_id
                        """
                    ),
                    {"project_id": project_id},
                )
                .mappings()
                .one()
            )
            latest_pending_event_id = connection.execute(
                text(
                    """
                    select id from public.reanalysis_change_events
                    where project_id = :project_id and actor_user_id = :user_id
                      and state = 'pending'
                    order by created_at desc
                    limit 1
                    """
                ),
                {"project_id": project_id, "user_id": actor_user_id},
            ).scalar_one_or_none()
            first_run = (
                connection.execute(
                    text(
                        """
                        select first_run, onboarded, grounding_act_count,
                               ever_unlocked, unlock_threshold
                        from public.project_first_run_states
                        where project_id = :project_id and user_id = :user_id
                        """
                    ),
                    {"project_id": project_id, "user_id": actor_user_id},
                )
                .mappings()
                .one()
            )
            notifications = (
                connection.execute(
                    text(
                        """
                        select id, analysis_run_id, pillar_deltas, settled_causes,
                               previous_band, current_band, delivery_kind,
                               seen_at, expires_at, created_at
                        from public.read_moved_notifications
                        where project_id = :project_id and user_id = :user_id
                          and (expires_at is null or expires_at > now())
                        order by created_at desc
                        limit 5
                        """
                    ),
                    {"project_id": project_id, "user_id": actor_user_id},
                )
                .mappings()
                .all()
            )
        freeze_on = (
            bool(first_run["first_run"])
            and int(first_run["grounding_act_count"]) < int(first_run["unlock_threshold"])
            and not bool(first_run["ever_unlocked"])
        )
        return {
            "freshness": {
                **dict(freshness),
                "latest_pending_event_id": latest_pending_event_id,
            },
            "first_run": {**dict(first_run), "freeze_on": freeze_on},
            "notifications": [dict(notification) for notification in notifications],
        }

    def withdraw_pending_act(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        event_id: UUID,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        with self._engine.begin() as connection:
            event = (
                connection.execute(
                    text(
                        """
                        select id, state, analysis_run_id, evidence_json,
                               grounding_counted_at
                        from public.reanalysis_change_events
                        where id = :event_id and project_id = :project_id
                          and actor_user_id = :user_id
                        for update
                        """
                    ),
                    {
                        "event_id": event_id,
                        "project_id": project_id,
                        "user_id": actor_user_id,
                    },
                )
                .mappings()
                .one_or_none()
            )
            if event is None:
                raise SliceTwoNotFound
            if event["state"] != "pending":
                raise ValueError("ACT_NOT_PENDING")
            if event["analysis_run_id"] is not None:
                run = self._store.get_run(event["analysis_run_id"])
                if run is None or run.status is not AnalysisRunStatus.QUEUED:
                    raise ValueError("ACT_REANALYSIS_STARTED")
                evidence = event["evidence_json"] or {}
                self._store.withdraw_queued_event(
                    run.id,
                    event_id=event_id,
                    evidence_references=tuple(evidence.get("references", [])),
                )
            connection.execute(
                text(
                    """
                    update public.reanalysis_change_events
                    set state = 'withdrawn', withdrawn_at = now()
                    where id = :event_id and state = 'pending'
                    """
                ),
                {"event_id": event_id},
            )
            if event["grounding_counted_at"] is not None:
                connection.execute(
                    text(
                        """
                        update public.project_first_run_states
                        set grounding_act_count = greatest(grounding_act_count - 1, 0),
                            updated_at = now()
                        where project_id = :project_id and user_id = :user_id
                        """
                    ),
                    {"project_id": project_id, "user_id": actor_user_id},
                )
            pending_count = connection.execute(
                text(
                    """
                    select count(*) from public.reanalysis_change_events
                    where project_id = :project_id and state = 'pending'
                    """
                ),
                {"project_id": project_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.project_read_freshness
                    set state = cast(:state as public.read_freshness_state),
                        pending_count = :pending_count, updated_at = now()
                    where project_id = :project_id
                    """
                ),
                {
                    "state": "stale" if pending_count else "fresh",
                    "pending_count": pending_count,
                    "project_id": project_id,
                },
            )
            first_run = (
                connection.execute(
                    text(
                        """
                        select grounding_act_count, ever_unlocked, unlock_threshold
                        from public.project_first_run_states
                        where project_id = :project_id and user_id = :user_id
                        """
                    ),
                    {"project_id": project_id, "user_id": actor_user_id},
                )
                .mappings()
                .one_or_none()
            )
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=snapshot.analysis_run_id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type="analysis.pending_change_withdrawn",
                summary="Pending change withdrawn before reanalysis",
                idempotency_key=f"history:withdraw:{event_id}",
                payload={"event_id": str(event_id)},
            )
        grounding_count = int(first_run["grounding_act_count"]) if first_run else 0
        ever_unlocked = bool(first_run["ever_unlocked"]) if first_run else False
        unlock_threshold = (
            int(first_run["unlock_threshold"]) if first_run else self._first_run_unlock_threshold
        )
        return {
            "event_id": event_id,
            "state": "withdrawn",
            "pending_count": int(pending_count),
            "grounding_act_count": grounding_count,
            "ever_unlocked": ever_unlocked,
            "freeze_on": grounding_count < unlock_threshold and not ever_unlocked,
        }

    def run_reanalysis_now(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        deep: bool,
        key: str,
    ) -> AnalysisRun:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound
        event_id, existing_run_id = self._enqueue_change(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            project_id=project_id,
            event_key=f"explicit:{key}",
            change_kind="explicit",
            scope="all" if deep else "pending",
            evidence={},
            requires_deep_pass=deep,
        )
        if existing_run_id is not None:
            existing = self._store.get_run(existing_run_id)
            if existing is not None:
                return existing
        run = self._store.create_run(
            AnalysisRunRequest(
                workspace_id=workspace_id,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=parent_run.request.description,
                source_names=parent_run.request.source_names,
                source_document_ids=parent_run.request.source_document_ids,
                user_evidence=parent_run.request.user_evidence,
                idempotency_key=f"explicit-reanalysis:{key}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=False,
                pass_kind=(AnalysisPassKind.DEEP if deep else AnalysisPassKind.FAST),
                reanalysis_trigger=ReanalysisTrigger.EXPLICIT,
                consolidated_event_ids=(event_id,),
            )
        )
        self._attach_change_to_run(event_id, run.id)
        if run.status is AnalysisRunStatus.QUEUED:
            self._executor.submit(self._execute, run.id)
        return run

    def act_on_outcome(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        action: str,
        outcome: str | None,
        key: str,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        snapshot = self._store.current_snapshot(project_id)
        if snapshot is None:
            raise SliceTwoNotFound
        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound
        intent = next(
            (
                artifact
                for artifact in snapshot.artifacts
                if artifact.artifact_type.value == "intent"
            ),
            None,
        )
        if intent is None:
            raise SliceTwoNotFound
        current_outcome = (outcome or intent.summary).strip()
        if not current_outcome:
            raise ValueError("OUTCOME_REQUIRED")

        if action == "defer":
            with self._engine.begin() as connection:
                append_history_event(
                    connection,
                    workspace_id=workspace_id,
                    project_id=project_id,
                    analysis_run_id=snapshot.analysis_run_id,
                    actor_id=actor_user_id,
                    actor_type="user",
                    category="decisions",
                    event_type="outcome.confirmation_deferred",
                    summary="Outcome confirmation deferred",
                    detail="The primary outcome remains OSLO's inference.",
                    artifact_type="intent",
                    idempotency_key=f"history:outcome:{key}",
                )
            return {"action": action, "outcome": current_outcome, "analysis_run": None}

        if action == "refine":
            artifact = self.get_artifact(
                actor_user_id=actor_user_id,
                project_id=project_id,
                artifact_type="intent",
            )
            content = dict(artifact["content"])
            sections = [dict(section) for section in content.get("sections", [])]
            if sections:
                sections[0]["body"] = current_outcome
            else:
                sections = [
                    {
                        "heading": "Primary outcome",
                        "body": current_outcome,
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    }
                ]
            content["sections"] = sections
            _, run = self.update_artifact(
                actor_user_id=actor_user_id,
                project_id=project_id,
                artifact_type="intent",
                content=content,
                expected_version=int(artifact["version"]),
                key=f"outcome-refine:{key}",
            )
            if run is None:
                raise RuntimeError("OUTCOME_REFINEMENT_REANALYSIS_MISSING")
            if run.request.consolidated_event_ids:
                self._record_grounding_act(
                    event_id=run.request.consolidated_event_ids[-1],
                    workspace_id=workspace_id,
                    project_id=project_id,
                    actor_user_id=actor_user_id,
                )
        elif action == "confirm":
            evidence = EvidenceFragment(
                reference=f"user:outcome:{key}",
                content=f"The user confirmed the primary outcome: {current_outcome}",
                source_name="Outcome confirmation",
                location="First analysis",
            )
            run = self._batched_reanalysis_run(
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                project_id=project_id,
                parent_run=parent_run,
                evidence=(evidence,),
                event_key=f"outcome-confirm:{key}",
                change_kind="confirm",
                scope="intent",
                consumes_analysis_allowance=False,
            )
        else:
            raise ValueError("OUTCOME_ACTION_INVALID")

        return {"action": action, "outcome": current_outcome, "analysis_run": run}

    def _batched_reanalysis_run(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        project_id: UUID,
        parent_run: AnalysisRun,
        evidence: tuple[EvidenceFragment, ...],
        event_key: str,
        change_kind: str,
        scope: str,
        consumes_analysis_allowance: bool,
        requires_deep_pass: bool = False,
    ) -> AnalysisRun:
        event_id, existing_run_id = self._enqueue_change(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            project_id=project_id,
            event_key=event_key,
            change_kind=change_kind,
            scope=scope,
            evidence={"references": [item.reference for item in evidence]},
            requires_deep_pass=requires_deep_pass,
        )
        if change_kind in {"confirm", "flag", "route"}:
            self._record_grounding_act(
                event_id=event_id,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
            )
        if existing_run_id is not None:
            existing = self._store.get_run(existing_run_id)
            if existing is not None:
                return existing

        active = self._store.latest_run_for_project(project_id, RunKind.EXTENDED)
        if (
            active is not None
            and active.status is AnalysisRunStatus.QUEUED
            and active.request.reanalysis_trigger is ReanalysisTrigger.BATCH
        ):
            merged = self._store.merge_queued_run(
                active.id,
                evidence=evidence,
                event_ids=(event_id,),
            )
            self._attach_change_to_run(event_id, merged.id)
            return merged

        run = self._store.create_run(
            AnalysisRunRequest(
                workspace_id=workspace_id,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=parent_run.request.description,
                source_names=parent_run.request.source_names,
                source_document_ids=parent_run.request.source_document_ids,
                user_evidence=parent_run.request.user_evidence + evidence,
                idempotency_key=f"reanalysis-batch:{event_id}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=consumes_analysis_allowance,
                pass_kind=(AnalysisPassKind.DEEP if requires_deep_pass else AnalysisPassKind.FAST),
                reanalysis_trigger=ReanalysisTrigger.BATCH,
                consolidated_event_ids=(event_id,),
            )
        )
        self._attach_change_to_run(event_id, run.id)
        if run.status is AnalysisRunStatus.QUEUED:
            self._submit_batched(run.id)
        return run

    def _enqueue_change(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        project_id: UUID,
        event_key: str,
        change_kind: str,
        scope: str,
        evidence: dict,
        requires_deep_pass: bool,
    ) -> tuple[UUID, UUID | None]:
        with self._engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        insert into public.reanalysis_change_events (
                          workspace_id, project_id, actor_user_id, event_key,
                          change_kind, scope, evidence_json, requires_deep_pass
                        ) values (
                          :workspace_id, :project_id, :actor_user_id, :event_key,
                          :change_kind, :scope, cast(:evidence as jsonb),
                          :requires_deep_pass
                        )
                        on conflict (workspace_id, event_key) do update set
                          event_key = excluded.event_key
                        returning id, analysis_run_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "actor_user_id": actor_user_id,
                        "event_key": event_key,
                        "change_kind": change_kind,
                        "scope": scope,
                        "evidence": json.dumps(evidence),
                        "requires_deep_pass": requires_deep_pass,
                    },
                )
                .mappings()
                .one()
            )
            connection.execute(
                text(
                    """
                    insert into public.project_read_freshness (
                      workspace_id, project_id, state, pending_count, last_act_at
                    ) values (
                      :workspace_id, :project_id, 'stale', 1, now()
                    )
                    on conflict (project_id) do update set
                      state = 'stale',
                      pending_count = (
                        select count(*) from public.reanalysis_change_events
                        where project_id = :project_id and state = 'pending'
                      ),
                      last_act_at = now(), updated_at = now()
                    """
                ),
                {"workspace_id": workspace_id, "project_id": project_id},
            )
        return row["id"], row["analysis_run_id"]

    def _attach_change_to_run(self, event_id: UUID, run_id: UUID) -> None:
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.reanalysis_change_events
                    set analysis_run_id = :run_id
                    where id = :event_id and state = 'pending'
                    """
                ),
                {"event_id": event_id, "run_id": run_id},
            )

    def _submit_batched(self, run_id: UUID) -> None:
        submit_after = getattr(self._executor, "submit_after", None)
        if callable(submit_after):
            submit_after(run_id, delay_seconds=self._reanalysis_debounce_seconds)
            return
        self._executor.submit(self._execute_after_debounce, run_id)

    def _execute_after_debounce(self, run_id: UUID) -> None:
        sleep(self._reanalysis_debounce_seconds)
        self._execute(run_id)

    def _mark_reanalysis_running(self, run: AnalysisRun) -> None:
        if run.request.kind is not RunKind.EXTENDED:
            return
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.project_read_freshness
                    set state = 'reanalyzing', active_run_id = :run_id,
                        updated_at = now()
                    where project_id = :project_id
                    """
                ),
                {"project_id": run.request.project_id, "run_id": run.id},
            )

    def _mark_reanalysis_landed(self, run: AnalysisRun) -> None:
        if run.request.kind is not RunKind.EXTENDED:
            return
        with self._engine.begin() as connection:
            if run.request.consolidated_event_ids:
                connection.execute(
                    text(
                        """
                        update public.reanalysis_change_events
                        set state = 'consumed', consumed_at = now()
                        where id = any(:event_ids) and state = 'pending'
                        """
                    ),
                    {"event_ids": list(run.request.consolidated_event_ids)},
                )
            pending_count = connection.execute(
                text(
                    """
                    select count(*) from public.reanalysis_change_events
                    where project_id = :project_id and state = 'pending'
                    """
                ),
                {"project_id": run.request.project_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.project_read_freshness
                    set state = cast(:state as public.read_freshness_state),
                        pending_count = :pending_count,
                        based_on_run_id = :run_id, active_run_id = null,
                        last_landed_at = now(), updated_at = now()
                    where project_id = :project_id
                    """
                ),
                {
                    "state": "stale" if pending_count else "fresh",
                    "pending_count": pending_count,
                    "run_id": run.id,
                    "project_id": run.request.project_id,
                },
            )
            if run.request.reanalysis_trigger is ReanalysisTrigger.DEEP_SUPERSEDE:
                append_history_event(
                    connection,
                    workspace_id=run.request.workspace_id,
                    project_id=run.request.project_id,
                    analysis_run_id=run.id,
                    actor_type="oslo",
                    category="analysis",
                    event_type="reanalysis.superseded",
                    summary="Deep analysis superseded the provisional read",
                    idempotency_key=f"history:deep-supersede:{run.id}",
                    payload={"parent_run_id": str(run.request.parent_run_id)},
                )
        self._create_read_moved_notification(run)

    def _withdrawn_batch_is_empty(self, run: AnalysisRun) -> bool:
        if (
            run.request.kind is not RunKind.EXTENDED
            or run.request.reanalysis_trigger is not ReanalysisTrigger.BATCH
            or not run.request.consolidated_event_ids
        ):
            return False
        with self._engine.connect() as connection:
            active_count = connection.execute(
                text(
                    """
                    select count(*) from public.reanalysis_change_events
                    where id = any(:event_ids) and state = 'pending'
                    """
                ),
                {"event_ids": list(run.request.consolidated_event_ids)},
            ).scalar_one()
        return int(active_count) == 0

    def _complete_withdrawn_batch_noop(self, run: AnalysisRun) -> None:
        self._store.complete_run(run.id)
        with self._engine.begin() as connection:
            pending_count = connection.execute(
                text(
                    """
                    select count(*) from public.reanalysis_change_events
                    where project_id = :project_id and state = 'pending'
                    """
                ),
                {"project_id": run.request.project_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    update public.project_read_freshness
                    set state = cast(:state as public.read_freshness_state),
                        pending_count = :pending_count, active_run_id = null,
                        updated_at = now()
                    where project_id = :project_id
                    """
                ),
                {
                    "state": "stale" if pending_count else "fresh",
                    "pending_count": pending_count,
                    "project_id": run.request.project_id,
                },
            )

    def _mark_reanalysis_failed(self, run: AnalysisRun) -> None:
        if run.request.kind is not RunKind.EXTENDED:
            return
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.project_read_freshness
                    set state = 'stale', active_run_id = null, updated_at = now()
                    where project_id = :project_id
                    """
                ),
                {"project_id": run.request.project_id},
            )

    def _create_read_moved_notification(self, run: AnalysisRun) -> None:
        if run.snapshot is None or run.request.parent_run_id is None:
            return
        parent = self._store.get_run(run.request.parent_run_id)
        if parent is None or parent.snapshot is None:
            return
        previous = parent.snapshot.assessment.integrity
        current = run.snapshot.assessment.integrity
        if previous is None or current is None:
            return
        previous_pillars = {pillar.key: pillar.band for pillar in previous.decomposition}
        pillar_deltas = [
            {"pillar": pillar.key, "from": previous_pillars.get(pillar.key), "to": pillar.band}
            for pillar in current.decomposition
            if previous_pillars.get(pillar.key) != pillar.band
        ]
        settled = [
            issue.title
            for issue in run.snapshot.assessment.issues
            if issue.status == "resolved"
            and not any(
                parent_issue.id == issue.id and parent_issue.status == "resolved"
                for parent_issue in parent.snapshot.assessment.issues
            )
        ]
        if not pillar_deltas and previous.level == current.level and not settled:
            return
        now = datetime.now(UTC)
        with self._engine.begin() as connection:
            runtime = (
                connection.execute(
                    text(
                        """
                        select last_act_at from public.project_read_freshness
                        where project_id = :project_id
                        """
                    ),
                    {"project_id": run.request.project_id},
                )
                .mappings()
                .one_or_none()
            )
            last_act_at = runtime["last_act_at"] if runtime else None
            immediate = bool(
                last_act_at
                and (now - last_act_at).total_seconds()
                <= self._read_moved_immediate_threshold_seconds
            )
            delivery = "transient" if immediate else "durable"
            connection.execute(
                text(
                    """
                    insert into public.read_moved_notifications (
                      workspace_id, project_id, user_id, analysis_run_id,
                      pillar_deltas, settled_causes, previous_band, current_band,
                      delivery_kind, expires_at
                    ) values (
                      :workspace_id, :project_id, :user_id, :run_id,
                      cast(:pillar_deltas as jsonb), cast(:settled as jsonb),
                      :previous_band, :current_band, :delivery,
                      :expires_at
                    )
                    """
                ),
                {
                    "workspace_id": run.request.workspace_id,
                    "project_id": run.request.project_id,
                    "user_id": run.request.requested_by,
                    "run_id": run.id,
                    "pillar_deltas": json.dumps(pillar_deltas),
                    "settled": json.dumps(settled),
                    "previous_band": previous.level,
                    "current_band": current.level,
                    "delivery": delivery,
                    "expires_at": (
                        now + timedelta(seconds=self._read_moved_linger_seconds)
                        if delivery == "transient"
                        else None
                    ),
                },
            )

    def _record_grounding_act(
        self,
        *,
        event_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
        actor_user_id: UUID,
    ) -> None:
        activation_event_id = uuid4()
        with self._engine.begin() as connection:
            claimed = connection.execute(
                text(
                    """
                    update public.reanalysis_change_events
                    set grounding_counted_at = now()
                    where id = :event_id and grounding_counted_at is null
                    """
                ),
                {"event_id": event_id},
            )
            if claimed.rowcount != 1:
                return
            state = (
                connection.execute(
                    text(
                        """
                        insert into public.project_first_run_states (
                          workspace_id, project_id, user_id, grounding_act_count,
                          ever_unlocked, unlock_threshold
                        ) values (
                          :workspace_id, :project_id, :user_id, 1,
                          :unlock_threshold <= 1, :unlock_threshold
                        )
                        on conflict (project_id, user_id) do update set
                          grounding_act_count =
                            public.project_first_run_states.grounding_act_count + 1,
                          ever_unlocked =
                            public.project_first_run_states.ever_unlocked
                            or public.project_first_run_states.grounding_act_count + 1
                               >= public.project_first_run_states.unlock_threshold,
                          updated_at = now()
                        returning grounding_act_count, ever_unlocked,
                                  activation_event_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "user_id": actor_user_id,
                        "unlock_threshold": self._first_run_unlock_threshold,
                    },
                )
                .mappings()
                .one()
            )
            if state["ever_unlocked"] and state["activation_event_id"] is None:
                claimed = connection.execute(
                    text(
                        """
                        update public.project_first_run_states
                        set activation_event_id = :event_id, updated_at = now()
                        where project_id = :project_id and user_id = :user_id
                          and activation_event_id is null
                        """
                    ),
                    {
                        "event_id": activation_event_id,
                        "project_id": project_id,
                        "user_id": actor_user_id,
                    },
                )
                if claimed.rowcount == 1:
                    connection.execute(
                        text(
                            """
                            insert into public.outbox_events (
                              id, workspace_id, aggregate_type, aggregate_id,
                              event_type, payload
                            ) values (
                              :event_id, :workspace_id, 'project', :project_id,
                              'activation.unlocked',
                              jsonb_build_object('user_id', cast(:user_id as text))
                            )
                            """
                        ),
                        {
                            "event_id": activation_event_id,
                            "workspace_id": workspace_id,
                            "project_id": project_id,
                            "user_id": actor_user_id,
                        },
                    )

    def _execute(self, run_id: UUID) -> None:
        before = self._store.get_run(run_id)
        if before is not None:
            if self._withdrawn_batch_is_empty(before):
                self._complete_withdrawn_batch_noop(before)
                return
            self._mark_reanalysis_running(before)
        result = self._workflow.resume(run_id)
        run = self._store.get_run(run_id)
        if run is not None and result.status is AnalysisRunStatus.COMPLETED:
            self._mark_reanalysis_landed(run)
        elif run is not None and result.status is AnalysisRunStatus.FAILED:
            if run.request.auto_retry_count == 0 and result.error_code in {
                "OPENAI_OUTPUT_LIMIT",
                "OPENAI_RATE_LIMIT",
                "OPENAI_SCHEMA_INVALID",
                "OPENAI_TIMEOUT",
                "OPENAI_UNAVAILABLE",
            }:
                self._store.queue_auto_retry(run.id)
                submit_after = getattr(self._executor, "submit_after", None)
                if callable(submit_after):
                    submit_after(run.id, delay_seconds=1)
                else:
                    self._executor.submit(self._execute, run.id)
                return
            self._mark_reanalysis_failed(run)
        if (
            result.status is AnalysisRunStatus.COMPLETED
            and run is not None
            and run.request.kind is RunKind.INITIAL
            and run.request.provisional
        ):
            sleep(self._extended_delay_seconds)
            extended = self._store.create_run(
                AnalysisRunRequest(
                    workspace_id=run.request.workspace_id,
                    project_id=run.request.project_id,
                    requested_by=run.request.requested_by,
                    kind=RunKind.EXTENDED,
                    description=run.request.description,
                    source_names=run.request.source_names,
                    source_document_ids=run.request.source_document_ids,
                    idempotency_key=f"extended:{run.id}",
                    parent_run_id=run.id,
                    consumes_analysis_allowance=False,
                    pass_kind=AnalysisPassKind.DEEP,
                    reanalysis_trigger=ReanalysisTrigger.DEEP_SUPERSEDE,
                )
            )
            if extended.status is AnalysisRunStatus.QUEUED:
                self._executor.submit(self._execute, extended.id)

    def execute_queued_run(self, run_id: UUID) -> AnalysisRun:
        self._execute(run_id)
        run = self._store.get_run(run_id)
        if run is None:
            raise SliceTwoNotFound
        return run

    def _workspace_for_project(self, actor_user_id: UUID, project_id: UUID) -> UUID:
        with self._engine.connect() as connection:
            workspace_id = connection.execute(
                text(
                    """
                    select project.workspace_id
                    from public.projects project
                    join public.memberships membership
                      on membership.workspace_id = project.workspace_id
                    where project.id = :project_id and membership.user_id = :user_id
                    """
                ),
                {"project_id": project_id, "user_id": actor_user_id},
            ).scalar_one_or_none()
        if workspace_id is None:
            raise SliceTwoPermissionDenied
        return workspace_id

    def _validate_documents(
        self,
        *,
        workspace_id: UUID,
        project_id: UUID,
        document_ids: tuple[UUID, ...],
    ) -> None:
        if not document_ids:
            return
        with self._engine.connect() as connection:
            count = connection.execute(
                text(
                    """
                    select count(*) from public.source_documents
                    where workspace_id = :workspace_id
                      and project_id = :project_id
                      and status = 'parsed'
                      and id = any(:document_ids)
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "document_ids": list(document_ids),
                },
            ).scalar_one()
        if count != len(set(document_ids)):
            raise SliceTwoPermissionDenied


def build_slice_two_application() -> DatabaseSliceTwoApplication:
    settings = Settings()  # type: ignore[call-arg]
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    store = DatabaseAnalysisStore(engine)
    object_store = (
        SupabaseObjectStorage(
            base_url=settings.supabase_url,
            secret_key=settings.supabase_secret_key,
            bucket=settings.object_storage_bucket,
        )
        if settings.object_storage_backend == "supabase"
        else LocalObjectStorage(settings.object_storage_path)
    )
    document_store = DatabaseDocumentStore(engine=engine, object_store=object_store)
    harness = build_agent_harness(settings)
    workflow = AnalysisWorkflow(
        store=store,
        harness=harness,
        phase_delay_seconds=settings.analysis_phase_delay_ms / 1000,
        artifact_workers_per_run=min(4, settings.analysis_artifact_worker_threads),
        artifact_worker_limit=settings.analysis_artifact_worker_threads,
    )
    executor = (
        DatabaseAnalysisJobQueue(engine)
        if settings.analysis_execution_mode == "durable"
        else ThreadPoolExecutor(
            max_workers=settings.analysis_worker_threads,
            thread_name_prefix="oslo-analysis",
        )
    )
    return DatabaseSliceTwoApplication(
        engine=engine,
        store=store,
        workflow=workflow,
        executor=executor,
        document_store=document_store,
        extended_delay_seconds=settings.extended_analysis_delay_ms / 1000,
        reanalysis_debounce_seconds=settings.reanalysis_debounce_ms / 1000,
        read_moved_immediate_threshold_seconds=(settings.read_moved_immediate_threshold_ms / 1000),
        read_moved_linger_seconds=settings.read_moved_linger_ms / 1000,
        first_run_unlock_threshold=settings.first_run_unlock_threshold,
    )


def build_agent_harness(settings: Settings) -> AgentHarness:
    if settings.analysis_harness == "deterministic":
        return DeterministicAgentHarness()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY_REQUIRED_FOR_OPENAI_HARNESS")
    legacy_model = settings.openai_model
    return OpenAIAgentHarness(
        api_key=settings.openai_api_key,
        fast_model=legacy_model or settings.openai_fast_model,
        extended_model=legacy_model or settings.openai_extended_model,
        fallback_model=settings.openai_fallback_model,
        timeout_seconds=settings.openai_timeout_seconds,
        max_retries=settings.openai_max_retries,
    )

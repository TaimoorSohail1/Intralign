import json
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Protocol
from uuid import UUID

from sqlalchemy import Engine, create_engine, text

from oslo_api.analysis import (
    AnalysisEvent,
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    AnalysisWorkflow,
    AssessmentSnapshot,
    DeterministicAgentHarness,
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
    SliceTwoAnalysisInProgress,
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
    ) -> None:
        self._engine = engine
        self._store = store
        self._workflow = workflow
        self._executor = executor
        self._document_store = document_store
        self._extended_delay_seconds = extended_delay_seconds

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
        run = self._store.create_run(
            AnalysisRunRequest(
                workspace_id=workspace_id,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=parent_run.request.description,
                source_names=parent_run.request.source_names,
                source_document_ids=parent_run.request.source_document_ids,
                user_evidence=parent_run.request.user_evidence + (clarification_evidence,),
                idempotency_key=f"clarification:{key}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=True,
            )
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
        if run.status is AnalysisRunStatus.QUEUED:
            self._executor.submit(self._execute, run.id)
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
        if issue_id:
            issue = next(
                (
                    candidate
                    for candidate in snapshot.assessment.issues
                    if candidate.id == issue_id
                ),
                None,
            )
            if issue is None:
                raise SliceTwoNotFound
            issue_title = issue.title
        reviewer_evidence = build_reviewer_evidence(
            response_key=key,
            reviewer_name=reviewer_name,
            issue_id=issue_id,
            issue_title=issue_title,
            response_kind=response_kind,
            body=body,
        )
        run = self._store.create_run(
            AnalysisRunRequest(
                workspace_id=workspace_id,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=parent_run.request.description,
                source_names=parent_run.request.source_names,
                source_document_ids=parent_run.request.source_document_ids,
                user_evidence=parent_run.request.user_evidence + (reviewer_evidence,),
                idempotency_key=f"review:{key}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=False,
            )
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
        if run.status is AnalysisRunStatus.QUEUED:
            self._executor.submit(self._execute, run.id)
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
            question=(
                issue.clarification
                or "What governed change addresses this issue?"
            ),
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
                "status": lifecycle_by_issue.get(
                    str(action["issue_stable_key"]), "open"
                ),
                "selected_resolution": str(action["resolution_text"]),
                "artifact_type": (
                    str(action["artifact_type"])
                    if action["artifact_type"] is not None
                    else None
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
                "status": lifecycle_by_issue.get(
                    str(answer["issue_stable_key"]), "open"
                ),
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
            dict(draft["content_json"])
            if draft is not None
            else self._artifact_content(artifact)
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
                int(draft["version"])
                if draft is not None
                else int(analysis_revision or 1)
            ),
            "provenance": (
                str(draft["provenance"]) if draft is not None else "from_oslo"
            ),
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
            "updated_at": (
                draft["updated_at"] if draft is not None else snapshot.published_at
            ),
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
        active_extended = self._store.latest_run_for_project(
            project_id,
            RunKind.EXTENDED,
        )
        if (
            active_extended is not None
            and active_extended.id != parent_run.id
            and active_extended.status
            in {AnalysisRunStatus.QUEUED, AnalysisRunStatus.RUNNING}
        ):
            raise SliceTwoAnalysisInProgress

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
        user_evidence = parent_run.request.user_evidence + (edit_evidence,)
        if issue_evidence is not None:
            user_evidence += (issue_evidence,)
        run = self._store.create_run(
            AnalysisRunRequest(
                workspace_id=workspace_id,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=parent_run.request.description,
                source_names=parent_run.request.source_names,
                source_document_ids=parent_run.request.source_document_ids,
                user_evidence=user_evidence,
                idempotency_key=f"artifact-edit:{key}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=False,
            )
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
        if run.status is AnalysisRunStatus.QUEUED:
            self._executor.submit(self._execute, run.id)
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

    def _execute(self, run_id: UUID) -> None:
        result = self._workflow.resume(run_id)
        run = self._store.get_run(run_id)
        if (
            result.status is AnalysisRunStatus.COMPLETED
            and run is not None
            and run.request.kind is RunKind.INITIAL
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

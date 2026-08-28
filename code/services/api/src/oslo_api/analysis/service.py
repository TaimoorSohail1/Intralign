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
    project_work_breakdown_tasks,
)
from oslo_api.analysis.document_store import DatabaseDocumentStore
from oslo_api.analysis.harness import AgentHarness
from oslo_api.analysis.history import append_history_event, list_project_history
from oslo_api.analysis.job_queue import DatabaseAnalysisJobQueue
from oslo_api.analysis.models import EvidenceFragment, normalize_evidence_state
from oslo_api.analysis.object_storage import LocalObjectStorage, SupabaseObjectStorage
from oslo_api.analysis.openai_harness import OpenAIAgentHarness
from oslo_api.analysis.persistence import DatabaseAnalysisStore
from oslo_api.analysis.user_evidence import (
    build_clarification_evidence,
    build_reviewer_evidence,
)
from oslo_api.project_access import find_project_access
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
        provisional: bool = False,
    ) -> AnalysisRun:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        parent_run = None
        if kind is RunKind.EXTENDED:
            snapshot = self._store.current_snapshot(project_id)
            if snapshot is None:
                raise SliceTwoNotFound
            parent_run = self._store.get_run(snapshot.analysis_run_id)
            if parent_run is None:
                raise SliceTwoNotFound

            prior = parent_run.request
            documents = list(zip(prior.source_document_ids, prior.source_names, strict=False))
            known_document_ids = {document_id for document_id, _name in documents}
            documents.extend(
                (document_id, source_name)
                for document_id, source_name in zip(
                    source_document_ids,
                    source_names,
                    strict=False,
                )
                if document_id not in known_document_ids
            )
            source_document_ids = tuple(document_id for document_id, _name in documents)
            source_names = tuple(source_name for _document_id, source_name in documents)
            descriptions = [
                value
                for value in (prior.description.strip(), description.strip())
                if value
            ]
            description = "\n\n".join(dict.fromkeys(descriptions))

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
            user_evidence=parent_run.request.user_evidence if parent_run else (),
            idempotency_key=key,
            parent_run_id=parent_run.id if parent_run else None,
            consumes_analysis_allowance=True,
            provisional=provisional and kind is RunKind.INITIAL,
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
        pending_event_ids, pending_evidence = self._recoverable_pending_changes(
            run.request.project_id
        )
        existing_event_ids = set(run.request.consolidated_event_ids)
        additional_event_ids = tuple(
            event_id for event_id in pending_event_ids if event_id not in existing_event_ids
        )
        existing_references = {item.reference for item in run.request.user_evidence}
        additional_evidence = tuple(
            item for item in pending_evidence if item.reference not in existing_references
        )
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
        if additional_event_ids or additional_evidence:
            self._store.merge_queued_run(
                run.id,
                evidence=additional_evidence,
                event_ids=additional_event_ids,
            )
        self._attach_changes_to_run(pending_event_ids, run.id)
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
            connection.execute(
                text(
                    """
                    insert into public.issue_attestations (
                      workspace_id, project_id, issue_stable_key, act,
                      actor_user_id, attributed_to, basis, evidence_ref,
                      analysis_run_id, idempotency_key
                    )
                    select :workspace_id, :project_id, :issue_id, 'answer',
                           :actor_user_id,
                           jsonb_build_object(
                             'id', cast(profile.id as text),
                             'display_name', profile.display_name,
                             'role', membership.role
                           ),
                           'answered', :evidence_ref, :analysis_run_id,
                           :idempotency_key
                    from public.profiles profile
                    cross join lateral (
                      select membership.role::text as role
                      from public.memberships membership
                      where membership.user_id = profile.id
                        and membership.workspace_id = :workspace_id
                      union all
                      select membership.role::text as role
                      from public.project_memberships membership
                      where membership.user_id = profile.id
                        and membership.project_id = :project_id
                      limit 1
                    ) membership
                    where profile.id = :actor_user_id
                    on conflict (workspace_id, idempotency_key) do nothing
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                    "actor_user_id": actor_user_id,
                    "evidence_ref": clarification_evidence.reference,
                    "analysis_run_id": run.id,
                    "idempotency_key": f"clarification:{key}",
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
        """Promote reviewer evidence through the same reanalysis-only lifecycle."""

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
            if issue_id is not None:
                reviewer_act = "flag" if response_kind == "reject" else "answer"
                connection.execute(
                    text(
                        """
                        insert into public.issue_attestations (
                          workspace_id, project_id, issue_stable_key, act,
                          actor_user_id, attributed_to, basis, evidence_ref,
                          analysis_run_id, idempotency_key
                        ) values (
                          :workspace_id, :project_id, :issue_id,
                          cast(:act as public.issue_attestation_act), :actor_user_id,
                          cast(:attributed_to as jsonb), 'answered', :evidence_ref,
                          :analysis_run_id, :idempotency_key
                        )
                        on conflict (workspace_id, idempotency_key) do nothing
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                        "act": reviewer_act,
                        "actor_user_id": actor_user_id,
                        "attributed_to": json.dumps(
                            {
                                "id": f"reviewer:{key}",
                                "display_name": reviewer_name,
                                "role": "reviewer",
                            }
                        ),
                        "evidence_ref": reviewer_evidence.reference,
                        "analysis_run_id": run.id,
                        "idempotency_key": f"review-attestation:{key}",
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

    def act_on_issue_lifecycle(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        act: str,
        basis: str | None,
        evidence_ref: str | None,
        resolution: str | None,
        reviewer: dict | None,
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
        parent_run = self._store.get_run(snapshot.analysis_run_id)
        if parent_run is None:
            raise SliceTwoNotFound

        with self._engine.begin() as connection:
            existing = (
                connection.execute(
                    text(
                        """
                        select attestation.id, attestation.act, attestation.basis,
                               attestation.evidence_ref, attestation.attributed_to,
                               attestation.supersedes, attestation.analysis_run_id,
                               issue.current_status
                        from public.issue_attestations attestation
                        join public.issues issue
                          on issue.workspace_id = attestation.workspace_id
                         and issue.project_id = attestation.project_id
                         and issue.stable_key = attestation.issue_stable_key
                        where attestation.workspace_id = :workspace_id
                          and attestation.idempotency_key = :idempotency_key
                        """
                    ),
                    {"workspace_id": workspace_id, "idempotency_key": key},
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
                    "issue_id": issue_id,
                    "act": str(existing["act"]),
                    "status": str(existing["current_status"]),
                    "attestation": {
                        "id": str(existing["id"]),
                        "act": str(existing["act"]),
                        "basis": str(existing["basis"]) if existing["basis"] else None,
                        "evidence_ref": existing["evidence_ref"],
                        "attributed_to": dict(existing["attributed_to"]),
                        "supersedes": (
                            str(existing["supersedes"])
                            if existing["supersedes"] is not None
                            else None
                        ),
                    },
                    "analysis_run": run,
                }
            issue_row = (
                connection.execute(
                    text(
                        """
                        select current_status
                        from public.issues
                        where workspace_id = :workspace_id
                          and project_id = :project_id
                          and stable_key = :issue_id
                        for update
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                    },
                )
                .mappings()
                .one_or_none()
            )
            actor_row = (
                connection.execute(
                    text(
                        """
                        select profile.display_name, membership.role
                        from public.profiles profile
                        cross join lateral (
                          select owner.role::text as role
                          from public.memberships owner
                          where owner.user_id = profile.id
                            and owner.workspace_id = :workspace_id
                          union all
                          select delegate.role::text as role
                          from public.project_memberships delegate
                          where delegate.user_id = profile.id
                            and delegate.project_id = :project_id
                          limit 1
                        ) membership
                        where profile.id = :actor_user_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "actor_user_id": actor_user_id,
                    },
                )
                .mappings()
                .one()
            )
            latest_attestation_id = connection.execute(
                text(
                    """
                    select id from public.issue_attestations
                    where workspace_id = :workspace_id
                      and project_id = :project_id
                      and issue_stable_key = :issue_id
                    order by created_at desc
                    limit 1
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                },
            ).scalar_one_or_none()
        if issue_row is None:
            raise SliceTwoNotFound

        current_status = str(issue_row["current_status"])
        allowed_acts = {"confirm", "flag", "fix", "ground", "route", "withdraw"}
        if act not in allowed_acts:
            raise ValueError("ISSUE_LIFECYCLE_ACT_INVALID")
        if act in {"confirm", "ground"} and basis is None:
            raise ValueError("ISSUE_ACT_REQUIRES_BASIS")
        if act == "ground" and current_status != "needs_grounding":
            raise ValueError("GROUND_REQUIRES_MITIGATED_ISSUE")
        if act == "fix" and current_status not in {"open", "needs_fix"}:
            raise ValueError("FIX_REQUIRES_OPEN_OR_NEEDS_FIX_ISSUE")
        if act == "fix" and not (resolution or "").strip():
            raise ValueError("FIX_REQUIRES_PLAN_CHANGE")
        if act == "route" and (current_status != "open" or reviewer is None):
            raise ValueError("ROUTE_REQUIRES_OPEN_ISSUE_AND_REVIEWER")
        if act == "withdraw" and (current_status == "open" or latest_attestation_id is None):
            raise ValueError("ISSUE_HAS_NO_LIVE_ACT_TO_WITHDRAW")
        if current_status == "resolved" and act != "withdraw":
            raise ValueError("RESOLVED_ISSUE_IS_NOT_ACTIONABLE")

        attributed_to = {
            "id": str(actor_user_id),
            "display_name": str(actor_row["display_name"]),
            "role": str(actor_row["role"]),
        }
        run: AnalysisRun | None = None
        plan_change_ref: str | None = None
        routed_to: dict | None = None
        supersedes: UUID | None = None

        if act == "route":
            routed_to = reviewer
            live_status = "routed"
            route_event_id, _ = self._enqueue_change(
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                project_id=project_id,
                event_key=f"issue-route:{key}",
                change_kind="route",
                scope=issue.artifact_type.value,
                evidence={},
                requires_deep_pass=False,
            )
            self._record_grounding_act(
                event_id=route_event_id,
                workspace_id=workspace_id,
                project_id=project_id,
                actor_user_id=actor_user_id,
            )
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        update public.reanalysis_change_events
                        set state = 'consumed', consumed_at = now()
                        where id = :event_id and state = 'pending'
                        """
                    ),
                    {"event_id": route_event_id},
                )
                connection.execute(
                    text(
                        """
                        update public.project_read_freshness
                        set state = case when pending_count > 1
                              then 'stale'::public.read_freshness_state
                              else 'fresh'::public.read_freshness_state end,
                            pending_count = greatest(pending_count - 1, 0),
                            updated_at = now()
                        where project_id = :project_id
                        """
                    ),
                    {"project_id": project_id},
                )
        elif act == "fix":
            applied = self.act_on_issue(
                actor_user_id=actor_user_id,
                project_id=project_id,
                issue_id=issue_id,
                action="apply",
                resolution=(resolution or "").strip(),
                key=f"lifecycle-fix:{key}",
            )
            run = applied["analysis_run"]
            plan_change_ref = (
                f"artifact:{applied['artifact_type']}:v{applied['artifact_version']}"
            )
            live_status = "addressed"
        else:
            if act == "withdraw":
                supersedes = latest_attestation_id
            reference = evidence_ref or f"user:issue-act:{act}:{key}"
            evidence = EvidenceFragment(
                reference=reference,
                content=(
                    (resolution or "").strip()
                    or f"The user recorded a governed {act} act for {issue.title}."
                ),
                source_name="Issue attestation",
                location=issue.title,
            )
            run = self._batched_reanalysis_run(
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                project_id=project_id,
                parent_run=parent_run,
                evidence=(evidence,),
                event_key=f"issue-{act}:{key}",
                change_kind={
                    "confirm": "confirm",
                    "flag": "flag",
                    "ground": "ground",
                    "withdraw": "withdraw",
                }[act],
                scope=issue.artifact_type.value,
                consumes_analysis_allowance=False,
            )
            live_status = "open" if act == "withdraw" else "addressed"

        with self._engine.begin() as connection:
            attestation = (
                connection.execute(
                    text(
                        """
                        insert into public.issue_attestations (
                          workspace_id, project_id, issue_stable_key, act,
                          actor_user_id, attributed_to, basis, evidence_ref,
                          plan_change_ref, routed_to, supersedes, analysis_run_id,
                          idempotency_key
                        ) values (
                          :workspace_id, :project_id, :issue_id,
                          cast(:act as public.issue_attestation_act), :actor_user_id,
                          cast(:attributed_to as jsonb),
                          cast(:basis as public.issue_attestation_basis),
                          :evidence_ref, :plan_change_ref, cast(:routed_to as jsonb),
                          :supersedes, :analysis_run_id, :idempotency_key
                        )
                        returning id, act, basis, evidence_ref, attributed_to, supersedes
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "issue_id": issue_id,
                        "act": act,
                        "actor_user_id": actor_user_id,
                        "attributed_to": json.dumps(attributed_to),
                        "basis": basis,
                        "evidence_ref": evidence_ref,
                        "plan_change_ref": plan_change_ref,
                        "routed_to": json.dumps(routed_to) if routed_to else None,
                        "supersedes": supersedes,
                        "analysis_run_id": run.id if run is not None else None,
                        "idempotency_key": key,
                    },
                )
                .mappings()
                .one()
            )
            connection.execute(
                text(
                    """
                    update public.issues
                    set current_status = :status, updated_at = now()
                    where workspace_id = :workspace_id
                      and project_id = :project_id
                      and stable_key = :issue_id
                    """
                ),
                {
                    "status": live_status,
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "issue_id": issue_id,
                },
            )
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=run.id if run is not None else snapshot.analysis_run_id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type=f"grounding_act.{act}",
                summary=f"Issue {act} recorded",
                detail=f"{issue.title} now reads {live_status.replace('_', ' ')}.",
                issue_id=issue_id,
                artifact_type=issue.artifact_type.value,
                idempotency_key=f"history:issue-lifecycle:{key}",
                payload={"basis": basis, "evidence_ref": evidence_ref},
            )

        first_run = self.runtime_state(
            actor_user_id=actor_user_id,
            project_id=project_id,
        )["first_run"]
        return {
            "issue_id": issue_id,
            "act": act,
            "status": live_status,
            "attestation": {
                "id": str(attestation["id"]),
                "act": str(attestation["act"]),
                "basis": str(attestation["basis"]) if attestation["basis"] else None,
                "evidence_ref": attestation["evidence_ref"],
                "attributed_to": dict(attestation["attributed_to"]),
                "supersedes": (
                    str(attestation["supersedes"])
                    if attestation["supersedes"] is not None
                    else None
                ),
            },
            "analysis_run": run,
            "first_run": first_run,
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
            attestations = (
                connection.execute(
                    text(
                        """
                        select distinct on (issue_stable_key)
                               issue_stable_key, act, basis, evidence_ref,
                               attributed_to, routed_to, plan_change_ref,
                               analysis_run_id, created_at
                        from public.issue_attestations
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
        clarification_issue_keys = {
            str(answer["issue_stable_key"]) for answer in answers
        }
        updates.extend(
            {
                "issue_id": str(attestation["issue_stable_key"]),
                "action": (
                    "clarification"
                    if str(attestation["act"]) == "answer"
                    and str(attestation["issue_stable_key"])
                    in clarification_issue_keys
                    else str(attestation["act"])
                ),
                "status": lifecycle_by_issue.get(
                    str(attestation["issue_stable_key"]), "open"
                ),
                "selected_resolution": attestation["plan_change_ref"],
                "artifact_type": None,
                "artifact_version": None,
                "analysis_run": (
                    self._store.get_run(attestation["analysis_run_id"])
                    if attestation["analysis_run_id"] is not None
                    else None
                ),
                "basis": (
                    str(attestation["basis"])
                    if attestation["basis"] is not None
                    else None
                ),
                "evidence_ref": attestation["evidence_ref"],
                "attested_by": dict(attestation["attributed_to"]),
                "routed_to": (
                    dict(attestation["routed_to"])
                    if attestation["routed_to"] is not None
                    else None
                ),
                "created_at": attestation["created_at"],
            }
            for attestation in attestations
        )
        latest_by_issue: dict[str, dict] = {}
        for update in sorted(updates, key=lambda item: item["created_at"], reverse=True):
            latest_by_issue.setdefault(update["issue_id"], update)
        return list(latest_by_issue.values())

    def list_issue_proposals(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> list[dict]:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        with self._engine.begin() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select proposal.id, proposal.issue_stable_key,
                               proposal.kind, proposal.resolver_key,
                               proposal.title, proposal.rationale,
                               proposal.artifact_type, proposal.load_bearing,
                               decision.accepted, decision.surface
                        from public.issue_proposals proposal
                        left join lateral (
                          select candidate.accepted, candidate.surface
                          from public.issue_proposal_decisions candidate
                          where candidate.proposal_id = proposal.id
                          order by candidate.created_at desc
                          limit 1
                        ) decision on true
                        where proposal.workspace_id = :workspace_id
                          and proposal.project_id = :project_id
                        order by proposal.created_at, proposal.id
                        """
                    ),
                    {"workspace_id": workspace_id, "project_id": project_id},
                )
                .mappings()
                .all()
            )
        return [
            {
                "id": str(row["id"]),
                "issue_id": str(row["issue_stable_key"]),
                "kind": str(row["kind"]),
                "resolver_key": str(row["resolver_key"]),
                "title": str(row["title"]),
                "rationale": str(row["rationale"]),
                "artifact_type": (
                    str(row["artifact_type"])
                    if row["artifact_type"] is not None
                    else None
                ),
                "load_bearing": bool(row["load_bearing"]),
                "accepted": row["accepted"] is True,
                "rejected": row["accepted"] is False,
                "surface": str(row["surface"]) if row["surface"] else None,
            }
            for row in rows
        ]

    def decide_issue_proposal(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        proposal_id: UUID,
        accepted: bool,
        surface: str,
        key: str,
    ) -> dict:
        workspace_id = self._workspace_for_project(actor_user_id, project_id)
        allowed_surfaces = {"issue_card", "artifact", "folded_read"}
        if surface not in allowed_surfaces:
            raise ValueError("PROPOSAL_SURFACE_INVALID")
        with self._engine.begin() as connection:
            existing = (
                connection.execute(
                    text(
                        """
                        select decision.analysis_run_id, proposal.issue_stable_key
                        from public.issue_proposal_decisions decision
                        join public.issue_proposals proposal
                          on proposal.id = decision.proposal_id
                        where decision.workspace_id = :workspace_id
                          and decision.idempotency_key = :idempotency_key
                        """
                    ),
                    {"workspace_id": workspace_id, "idempotency_key": key},
                )
                .mappings()
                .one_or_none()
            )
            proposal = (
                connection.execute(
                    text(
                        """
                        select proposal.id, proposal.issue_stable_key,
                               proposal.kind, proposal.title, proposal.artifact_type,
                               coalesce(
                                 proposal.created_by_run_id,
                                 project.current_analysis_run_id
                               ) as source_analysis_run_id,
                               issue.current_status,
                               latest.accepted as latest_accepted
                        from public.issue_proposals proposal
                        join public.projects project
                          on project.workspace_id = proposal.workspace_id
                         and project.id = proposal.project_id
                        join public.issues issue
                          on issue.workspace_id = proposal.workspace_id
                         and issue.project_id = proposal.project_id
                         and issue.stable_key = proposal.issue_stable_key
                        left join lateral (
                          select decision.accepted
                          from public.issue_proposal_decisions decision
                          where decision.proposal_id = proposal.id
                          order by decision.created_at desc
                          limit 1
                        ) latest on true
                        where proposal.workspace_id = :workspace_id
                          and proposal.project_id = :project_id
                          and proposal.id = :proposal_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "proposal_id": proposal_id,
                    },
                )
                .mappings()
                .one_or_none()
            )
        if proposal is None:
            raise SliceTwoNotFound
        if existing is not None:
            run = (
                self._store.get_run(existing["analysis_run_id"])
                if existing["analysis_run_id"] is not None
                else None
            )
            current = next(
                proposal_item
                for proposal_item in self.list_issue_proposals(
                    actor_user_id=actor_user_id,
                    project_id=project_id,
                )
                if proposal_item["id"] == str(proposal_id)
            )
            return {"proposal": current, "analysis_run": run}
        if proposal["latest_accepted"] is not None:
            raise ValueError("PROPOSAL_ALREADY_DECIDED")
        if proposal["current_status"] == "resolved":
            raise ValueError("FINDING_ALREADY_RESOLVED")

        run: AnalysisRun | None = None
        if accepted and str(proposal["kind"]) == "build":
            applied = self.act_on_issue_lifecycle(
                actor_user_id=actor_user_id,
                project_id=project_id,
                issue_id=str(proposal["issue_stable_key"]),
                act="fix",
                basis=None,
                evidence_ref=None,
                resolution=str(proposal["title"]),
                reviewer=None,
                key=f"proposal-build:{key}",
            )
            run = applied["analysis_run"]

        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    insert into public.issue_proposal_decisions (
                      workspace_id, project_id, proposal_id, accepted,
                      actor_user_id, surface, analysis_run_id, idempotency_key
                    ) values (
                      :workspace_id, :project_id, :proposal_id, :accepted,
                      :actor_user_id,
                      cast(:surface as public.issue_proposal_surface),
                      :analysis_run_id, :idempotency_key
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "proposal_id": proposal_id,
                    "accepted": accepted,
                    "actor_user_id": actor_user_id,
                    "surface": surface,
                    "analysis_run_id": run.id if run is not None else None,
                    "idempotency_key": key,
                },
            )
            history_run_id = (
                run.id if run is not None else proposal["source_analysis_run_id"]
            )
            if history_run_id is None:
                raise RuntimeError("PROPOSAL_HISTORY_REQUIRES_ANALYSIS_RUN")
            append_history_event(
                connection,
                workspace_id=workspace_id,
                project_id=project_id,
                analysis_run_id=history_run_id,
                actor_id=actor_user_id,
                actor_type="user",
                category="decisions",
                event_type=("proposal.accepted" if accepted else "proposal.rejected"),
                summary=("Proposal accepted" if accepted else "Proposal rejected"),
                detail=str(proposal["title"]),
                issue_id=str(proposal["issue_stable_key"]),
                artifact_type=(
                    str(proposal["artifact_type"])
                    if proposal["artifact_type"] is not None
                    else None
                ),
                idempotency_key=f"history:proposal:{key}",
                payload={"proposal_id": str(proposal_id), "surface": surface},
            )
        current = next(
            proposal_item
            for proposal_item in self.list_issue_proposals(
                actor_user_id=actor_user_id,
                project_id=project_id,
            )
            if proposal_item["id"] == str(proposal_id)
        )
        return {"proposal": current, "analysis_run": run}

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
            work_breakdown_draft = None
            if artifact_type in {"schedule", "resources"}:
                work_breakdown_draft = (
                    connection.execute(
                        text(
                            """
                            select content_json
                            from public.artifact_drafts
                            where workspace_id = :workspace_id
                              and project_id = :project_id
                              and artifact_type = 'work_breakdown'
                            """
                        ),
                        {"workspace_id": workspace_id, "project_id": project_id},
                    )
                    .mappings()
                    .one_or_none()
                )
        content = (
            dict(draft["content_json"]) if draft is not None else self._artifact_content(artifact)
        )
        if artifact_type in {"schedule", "resources"}:
            work_breakdown = next(
                (
                    candidate
                    for candidate in snapshot.artifacts
                    if candidate.artifact_type.value == "work_breakdown"
                ),
                None,
            )
            work_breakdown_content = (
                dict(work_breakdown_draft["content_json"])
                if work_breakdown_draft is not None
                else (
                    self._artifact_content(work_breakdown)
                    if work_breakdown is not None
                    else {"sections": []}
                )
            )
            content = project_work_breakdown_tasks(
                artifact_type=artifact_type,
                content=content,
                work_breakdown_content=work_breakdown_content,
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
                    "row_states": [
                        normalize_evidence_state(state) for state in section.row_states
                    ],
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
            if updated.rowcount == 0:
                updated = connection.execute(
                    text(
                        """
                        update public.project_memberships
                        set orientation_seen_at = coalesce(orientation_seen_at, now())
                        where workspace_id = :workspace_id and user_id = :user_id
                        """
                    ),
                    {"workspace_id": workspace_id, "user_id": actor_user_id},
                )
            if updated.rowcount < 1:
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
                    from public.memberships membership
                    join public.projects project
                      on project.workspace_id = membership.workspace_id
                    where project.id = :project_id
                      and membership.user_id = :user_id
                    union all
                    select membership.orientation_seen_at
                    from public.project_memberships membership
                    where membership.project_id = :project_id
                      and membership.user_id = :user_id
                    limit 1
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
        pending_event_ids, pending_evidence = self._recoverable_pending_changes(project_id)
        merged_evidence = self._merge_evidence(
            parent_run.request.user_evidence,
            pending_evidence,
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
                user_evidence=merged_evidence,
                idempotency_key=f"explicit-reanalysis:{key}",
                parent_run_id=parent_run.id,
                consumes_analysis_allowance=False,
                pass_kind=(AnalysisPassKind.DEEP if deep else AnalysisPassKind.FAST),
                reanalysis_trigger=ReanalysisTrigger.EXPLICIT,
                consolidated_event_ids=pending_event_ids or (event_id,),
            )
        )
        self._attach_changes_to_run(pending_event_ids or (event_id,), run.id)
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

        self._declare_primary_outcome(
            workspace_id=workspace_id,
            project_id=project_id,
            actor_user_id=actor_user_id,
            title=current_outcome,
        )
        return {"action": action, "outcome": current_outcome, "analysis_run": run}

    def _declare_primary_outcome(
        self,
        *,
        workspace_id: UUID,
        project_id: UUID,
        actor_user_id: UUID,
        title: str,
    ) -> None:
        with self._engine.begin() as connection:
            updated = connection.execute(
                text(
                    "update public.project_outcomes "
                    "set title = :title, provenance = 'declared', updated_at = now() "
                    "where project_id = :project_id and is_primary"
                ),
                {"project_id": project_id, "title": title},
            )
            if updated.rowcount == 0:
                connection.execute(
                    text(
                        "insert into public.project_outcomes "
                        "(workspace_id, project_id, title, is_primary, provenance, created_by) "
                        "values (:workspace_id, :project_id, :title, true, 'declared', "
                        ":created_by)"
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "title": title,
                        "created_by": actor_user_id,
                    },
                )

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
        self._attach_changes_to_run((event_id,), run_id)

    def _attach_changes_to_run(self, event_ids: tuple[UUID, ...], run_id: UUID) -> None:
        if not event_ids:
            return
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    """
                    update public.reanalysis_change_events
                    set analysis_run_id = :run_id
                    where id = any(:event_ids) and state = 'pending'
                    """
                ),
                {"event_ids": list(event_ids), "run_id": run_id},
            )

    def _recoverable_pending_changes(
        self,
        project_id: UUID,
    ) -> tuple[tuple[UUID, ...], tuple[EvidenceFragment, ...]]:
        """Return pending changes that are not owned by an active analysis run.

        A failed run keeps its change events pending so the last-good read remains
        visible. An explicit rerun or retry must adopt those events; otherwise the
        successful replacement read lands while the workspace remains permanently
        stale and reviewer evidence can be omitted from the resumed request.
        """

        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    text(
                        """
                        select event.id, event.analysis_run_id
                        from public.reanalysis_change_events event
                        left join public.analysis_runs run
                          on run.id = event.analysis_run_id
                        where event.project_id = :project_id
                          and event.state = 'pending'
                          and (
                            event.analysis_run_id is null
                            or run.status = 'failed'
                          )
                        order by event.created_at, event.id
                        """
                    ),
                    {"project_id": project_id},
                )
                .mappings()
                .all()
            )
        event_ids = tuple(row["id"] for row in rows)
        evidence: list[EvidenceFragment] = []
        seen_references: set[str] = set()
        for failed_run_id in dict.fromkeys(
            row["analysis_run_id"] for row in rows if row["analysis_run_id"] is not None
        ):
            failed_run = self._store.get_run(failed_run_id)
            if failed_run is None:
                continue
            for item in failed_run.request.user_evidence:
                if item.reference in seen_references:
                    continue
                seen_references.add(item.reference)
                evidence.append(item)
        return event_ids, tuple(evidence)

    @staticmethod
    def _merge_evidence(
        current: tuple[EvidenceFragment, ...],
        recovered: tuple[EvidenceFragment, ...],
    ) -> tuple[EvidenceFragment, ...]:
        merged = list(current)
        seen_references = {item.reference for item in current}
        for item in recovered:
            if item.reference in seen_references:
                continue
            seen_references.add(item.reference)
            merged.append(item)
        return tuple(merged)

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
            connection.execute(
                text(
                    """
                    with landed as (
                      select distinct on (issue_stable_key)
                             issue_stable_key, act
                      from public.issue_attestations
                      where project_id = :project_id
                      order by issue_stable_key, created_at desc
                    )
                    update public.issues issue
                    set current_status = case landed.act
                          when 'flag' then 'needs_fix'
                          when 'fix' then 'needs_grounding'
                          when 'withdraw' then 'open'
                          else 'resolved'
                        end,
                        updated_at = now()
                    from landed
                    where issue.project_id = :project_id
                      and issue.stable_key = landed.issue_stable_key
                    """
                ),
                {"project_id": run.request.project_id},
            )
            connection.execute(
                text(
                    """
                    with landed_actions as (
                      select distinct issue_stable_key
                      from public.issue_actions
                      where project_id = :project_id
                        and analysis_run_id = :run_id
                        and action_type in ('apply', 'custom')
                    )
                    update public.issues issue
                    set current_status = 'needs_grounding', updated_at = now()
                    from landed_actions
                    where issue.project_id = :project_id
                      and issue.stable_key = landed_actions.issue_stable_key
                      and issue.current_status = 'addressed'
                    """
                ),
                {"project_id": run.request.project_id, "run_id": run.id},
            )
            connection.execute(
                text(
                    """
                    with run_findings as (
                      select distinct proposal.issue_stable_key
                      from public.issue_proposals proposal
                      join public.issue_proposal_decisions decision
                        on decision.proposal_id = proposal.id
                      where decision.analysis_run_id = :run_id
                        and decision.accepted
                        and proposal.kind = 'build'
                    ), completed as (
                      select finding.issue_stable_key
                      from run_findings finding
                      where not exists (
                        select 1
                        from public.issue_proposals required
                        where required.project_id = :project_id
                          and required.issue_stable_key = finding.issue_stable_key
                          and required.kind = 'build'
                          and not exists (
                            select 1
                            from public.issue_proposal_decisions latest
                            where latest.proposal_id = required.id
                              and latest.accepted
                              and not exists (
                                select 1
                                from public.issue_proposal_decisions newer
                                where newer.proposal_id = required.id
                                  and newer.created_at > latest.created_at
                              )
                          )
                      )
                    )
                    update public.issues issue
                    set current_status = 'resolved', updated_at = now()
                    from completed
                    where issue.project_id = :project_id
                      and issue.stable_key = completed.issue_stable_key
                    """
                ),
                {"run_id": run.id, "project_id": run.request.project_id},
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
            access = find_project_access(
                connection,
                actor_user_id=actor_user_id,
                project_id=project_id,
            )
        if access is None or not access.can_edit:
            raise SliceTwoPermissionDenied
        return access.workspace_id

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

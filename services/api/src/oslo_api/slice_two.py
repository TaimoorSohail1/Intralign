from typing import Protocol
from uuid import UUID

from oslo_api.analysis import (
    AnalysisEvent,
    AnalysisRun,
    AssessmentSnapshot,
    RunKind,
)


class SliceTwoPermissionDenied(Exception):
    """Raised when a user cannot access a Slice 2 project or run."""


class SliceTwoNotFound(Exception):
    """Raised when a Slice 2 resource does not exist."""


class SliceTwoIssueNotAnswerable(Exception):
    """Raised when an issue has no active clarification request."""


class SliceTwoArtifactConflict(Exception):
    """Raised when an artifact edit was based on a stale version."""


class SliceTwoAnalysisInProgress(Exception):
    """Raised when a second material edit would overlap an active re-analysis."""


class SliceTwoApplication(Protocol):
    def upload_document(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        file_name: str,
        content_type: str | None,
        content: bytes,
    ): ...

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
    ) -> AnalysisRun: ...

    def get_run(self, *, actor_user_id: UUID, run_id: UUID) -> AnalysisRun: ...

    def events_after(
        self,
        *,
        actor_user_id: UUID,
        run_id: UUID,
        sequence: int,
    ) -> tuple[AnalysisEvent, ...]: ...

    def wait_for_events(
        self,
        *,
        actor_user_id: UUID,
        run_id: UUID,
        sequence: int,
        timeout: float,
    ) -> tuple[AnalysisEvent, ...]: ...

    def current_overview(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> AssessmentSnapshot: ...

    def latest_extended_run(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> AnalysisRun | None: ...

    def list_history(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        category: str,
        cursor: str | None,
        limit: int,
    ) -> dict: ...

    def history_snapshot(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        run_id: UUID,
    ) -> AssessmentSnapshot: ...

    def has_seen_orientation(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> bool: ...

    def retry(self, *, actor_user_id: UUID, run_id: UUID) -> AnalysisRun: ...

    def answer_issue(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        answer: str,
        key: str,
    ) -> AnalysisRun: ...

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
    ) -> AnalysisRun: ...

    def act_on_issue(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        issue_id: str,
        action: str,
        resolution: str,
        key: str,
    ) -> dict: ...

    def list_issue_actions(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
    ) -> list[dict]: ...

    def get_artifact(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        artifact_type: str,
    ) -> dict: ...

    def update_artifact(
        self,
        *,
        actor_user_id: UUID,
        project_id: UUID,
        artifact_type: str,
        content: dict,
        expected_version: int,
        key: str,
    ) -> tuple[dict, AnalysisRun | None]: ...

    def mark_orientation_seen(self, *, actor_user_id: UUID, workspace_id: UUID) -> None: ...

from unittest.mock import Mock
from uuid import uuid4

from oslo_api.analysis.models import (
    AnalysisRun,
    AnalysisRunRequest,
    AnalysisRunStatus,
    ReanalysisTrigger,
    RunKind,
)
from oslo_api.analysis.service import DatabaseSliceTwoApplication


def test_unchanged_refresh_is_recorded_as_explicit_reanalysis() -> None:
    actor_user_id = uuid4()
    workspace_id = uuid4()
    project_id = uuid4()
    previous = AnalysisRun(
        id=uuid4(),
        request=AnalysisRunRequest(
            workspace_id=workspace_id,
            project_id=project_id,
            requested_by=actor_user_id,
            kind=RunKind.INITIAL,
            description="Unedited plan",
            source_names=("plan.pdf",),
            source_document_ids=(uuid4(),),
        ),
        status=AnalysisRunStatus.COMPLETED,
    )
    expected = AnalysisRun.queued(previous.request)
    application = object.__new__(DatabaseSliceTwoApplication)
    application._workspace_for_project = Mock(return_value=workspace_id)
    application._store = Mock()
    application._store.latest_run_for_project.return_value = previous
    application.start_analysis = Mock(return_value=expected)

    actual = application.refresh_analysis(
        actor_user_id=actor_user_id,
        project_id=project_id,
        key="refresh-key",
    )

    assert actual is expected
    application.start_analysis.assert_called_once_with(
        actor_user_id=actor_user_id,
        project_id=project_id,
        description="Unedited plan",
        source_names=("plan.pdf",),
        source_document_ids=previous.request.source_document_ids,
        kind=RunKind.INITIAL,
        key="refresh-key",
        reanalysis_trigger=ReanalysisTrigger.EXPLICIT,
    )

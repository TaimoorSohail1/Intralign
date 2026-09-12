from contextlib import nullcontext
from datetime import UTC, datetime
from uuid import uuid4

from oslo_api.analysis.models import ArtifactType, Assessment, AssessmentSnapshot, Issue
from oslo_api.analysis.persistence import _snapshot_dict
from oslo_api.collaboration.service import DatabaseCollaborationService


def _issue(index: int, *, retired_derived: bool = False) -> Issue:
    issue_id = f"ISS-CP-{index:03d}" if retired_derived else f"ISS-{index:03d}"
    return Issue(
        id=issue_id,
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Grounding",
        severity="Moderate",
        title=f"Issue {index}",
        why="The current read needs evidence.",
        recommendation="Verify the evidence.",
        evidence_refs=(),
        status="open",
        load_bearing=True,
    )


def _snapshot(project_id) -> dict:
    issues = tuple(_issue(index) for index in range(48)) + tuple(
        _issue(index, retired_derived=True) for index in range(50)
    )
    snapshot = AssessmentSnapshot(
        id=uuid4(),
        analysis_run_id=uuid4(),
        workspace_id=uuid4(),
        project_id=project_id,
        state="final",
        summary="Current read.",
        artifacts=(),
        assessment=Assessment(
            confidence_index=50,
            confidence_band="Moderate",
            reliability="Moderate",
            clarity="Moderate",
            alignment="Moderate",
            feasibility="Moderate",
            issues=issues,
        ),
        published_at=datetime.now(UTC),
    )
    return _snapshot_dict(snapshot)


class _Result:
    def __init__(self, *, scalar=None, rows=()):
        self._scalar = scalar
        self._rows = rows

    def scalar_one_or_none(self):
        return self._scalar

    def mappings(self):
        return self._rows


class _Connection:
    def __init__(self, project_id):
        self._project_id = project_id

    def execute(self, statement, _parameters):
        query = str(statement)
        if "public.assessment_snapshots" in query:
            return _Result(scalar=_snapshot(self._project_id))
        return _Result(rows=())


class _Engine:
    def __init__(self, project_id):
        self._project_id = project_id

    def connect(self):
        return nullcontext(_Connection(self._project_id))


def test_grounding_map_uses_the_same_canonical_issue_projection_as_overview() -> None:
    """B3: retired derived issues must not inflate the Grounding Map denominator."""
    service = object.__new__(DatabaseCollaborationService)
    workspace_id = uuid4()
    project_id = uuid4()
    service._engine = _Engine(project_id)
    service._project_access = lambda _actor_user_id, _project_id: (workspace_id, "owner")

    result = service.grounding_map(actor_user_id=uuid4(), project_id=project_id)

    assert sum(result["counts"].values()) == 48
    assert len(result["nodes"]) == 48

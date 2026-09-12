from contextlib import nullcontext
from uuid import uuid4

from oslo_api.collaboration.service import DatabaseCollaborationService


def _issue(index: int) -> dict:
    return {
        "id": f"ISS-{index:03d}",
        "title": f"Issue {index}",
        "status": "open",
        "load_bearing": True,
    }


class _Result:
    def __init__(self, *, scalar=None, rows=()):
        self._scalar = scalar
        self._rows = rows

    def scalar_one_or_none(self):
        return self._scalar

    def mappings(self):
        return self._rows


class _Connection:
    def execute(self, statement, _parameters):
        query = str(statement)
        if "public.assessment_snapshots" in query:
            issue_count = 48 if "current_analysis_run_id" in query else 98
            return _Result(
                scalar={"assessment": {"issues": [_issue(i) for i in range(issue_count)]}}
            )
        return _Result(rows=())


class _Engine:
    def connect(self):
        return nullcontext(_Connection())


def test_grounding_map_uses_the_project_current_read_not_the_latest_published_snapshot() -> None:
    """B3: Grounding Map must use the same current read as Overview and History."""
    service = object.__new__(DatabaseCollaborationService)
    service._engine = _Engine()
    workspace_id = uuid4()
    project_id = uuid4()
    service._project_access = lambda _actor_user_id, _project_id: (workspace_id, "owner")

    result = service.grounding_map(actor_user_id=uuid4(), project_id=project_id)

    assert sum(result["counts"].values()) == 48
    assert len(result["nodes"]) == 48

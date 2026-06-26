"""DTM-0031 positive suite — platform repos read+write project / analysis_run / notification.

Proves the platform persistence the DTM-0018 read seam expects: each repo
CREATEs, READs, and (mutable lifecycle/status/state) UPDATEs a row, scoped to a
workspace/project, in the EXACT column shape ``SupabaseProjectionReader`` SELECTs
and the ``shared.entities`` DTOs (Data Model v1.2) bind.

A pure in-memory fake Supabase client stands in for the live stack (the house
style — see ``tests/positive/disclose`` / ``tests/positive/render``): the repos
are exercised through the same PostgREST-shaped chain
(``table().insert/update/select().eq().order().limit().execute()``) they use in
production, so the column wiring is asserted without a live Supabase.
"""

from __future__ import annotations

import uuid

from backend.platform import (
    SupabaseAnalysisRunRepository,
    SupabaseNotificationRepository,
    SupabaseProjectRepository,
)
from backend.services.render.read_seam import SupabaseProjectionReader
from shared.entities import (
    AnalysisRun,
    Notification,
    Project,
)

from tests.support.fake_supabase import FakeSupabaseClient

WS_A = str(uuid.uuid4())
WS_B = str(uuid.uuid4())
PROJECT = str(uuid.uuid4())


# --- project: create -> get -> update lifecycle -------------------------------

def test_project_create_get_and_lifecycle_update() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseProjectRepository(client)

    created = repo.create({
        "project_id": PROJECT,
        "workspace_id": WS_A,
        "created_by_user_id": str(uuid.uuid4()),
        "title": "Mars rover plan",
        "description": "Q3 planning",
        "lifecycle_state": "created",
    })
    assert created["project_id"] == PROJECT
    assert created["lifecycle_state"] == "created"

    got = repo.get(PROJECT)
    assert got is not None
    assert got["workspace_id"] == WS_A

    # Mutable lifecycle transition (platform tables are NOT append-only).
    updated = repo.update_lifecycle(PROJECT, "orienting")
    assert updated["lifecycle_state"] == "orienting"
    assert repo.get(PROJECT)["lifecycle_state"] == "orienting"


def test_project_row_satisfies_project_dto() -> None:
    """The stored row carries every Data Model v1.2 §7 Project field (DTO binds)."""
    client = FakeSupabaseClient()
    repo = SupabaseProjectRepository(client)
    repo.create({
        "project_id": PROJECT,
        "workspace_id": WS_A,
        "lifecycle_state": "created",
        "title": "x",
    })
    row = repo.get(PROJECT)
    dto = Project(**row)
    assert dto.project_id == PROJECT
    assert dto.lifecycle_state.value == "created"


# --- analysis_run: insert -> get -> status transition -------------------------

def test_analysis_run_insert_get_and_status_transition() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseAnalysisRunRepository(client)
    run_id = str(uuid.uuid4())

    created = repo.create({
        "analysis_run_id": run_id,
        "project_id": PROJECT,
        "run_type": "fast_analysis_pass",
        "run_status": "queued",
    })
    assert created["run_status"] == "queued"

    repo.update_status(run_id, "running")
    repo.update_status(run_id, "completed", completed_at="2026-06-26T01:00:00Z")
    got = repo.get(run_id)
    assert got["run_status"] == "completed"
    assert got["completed_at"] == "2026-06-26T01:00:00Z"

    dto = AnalysisRun(**got)
    assert dto.run_type.value == "fast_analysis_pass"
    assert dto.run_status.value == "completed"


def test_analysis_runs_for_project_scoped() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseAnalysisRunRepository(client)
    other_project = str(uuid.uuid4())
    repo.create({"analysis_run_id": str(uuid.uuid4()), "project_id": PROJECT,
                 "run_type": "fast_analysis_pass", "run_status": "queued"})
    repo.create({"analysis_run_id": str(uuid.uuid4()), "project_id": other_project,
                 "run_type": "deep_analysis_pass", "run_status": "queued"})
    runs = repo.list_for_project(PROJECT)
    assert len(runs) == 1
    assert runs[0]["project_id"] == PROJECT


# --- notification: insert -> get -> view -> dismiss ---------------------------

def test_notification_insert_view_and_dismiss() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseNotificationRepository(client)
    notif_id = str(uuid.uuid4())

    created = repo.create({
        "notification_id": notif_id,
        "workspace_id": WS_A,
        "project_id": PROJECT,
        "source_object_type": "finding",
        "source_object_id": str(uuid.uuid4()),
        "event_type": "finding_acknowledged",
        "state": "created",
    })
    assert created["state"] == "created"

    viewed = repo.mark_viewed(notif_id, viewed_at="2026-06-26T02:00:00Z")
    assert viewed["state"] == "viewed"
    assert viewed["viewed_at"] == "2026-06-26T02:00:00Z"

    dismissed = repo.mark_dismissed(notif_id, dismissed_at="2026-06-26T03:00:00Z")
    assert dismissed["state"] == "dismissed"
    assert dismissed["dismissed_at"] == "2026-06-26T03:00:00Z"

    dto = Notification(**repo.get(notif_id))
    assert dto.state.value == "dismissed"
    assert dto.source_object_type.value == "finding"


def test_notifications_for_workspace_scoped() -> None:
    client = FakeSupabaseClient()
    repo = SupabaseNotificationRepository(client)
    repo.create({"notification_id": str(uuid.uuid4()), "workspace_id": WS_A,
                 "source_object_type": "finding", "source_object_id": "s-1",
                 "event_type": "e", "state": "created"})
    repo.create({"notification_id": str(uuid.uuid4()), "workspace_id": WS_B,
                 "source_object_type": "finding", "source_object_id": "s-2",
                 "event_type": "e", "state": "created"})
    rows = repo.list_for_workspace(WS_A)
    assert len(rows) == 1
    assert rows[0]["workspace_id"] == WS_A


# --- read-seam reads the SAME rows the repos write (end-to-end) ---------------

def test_read_seam_lists_repo_written_rows() -> None:
    """Rows written through the platform repos are visible through the DTM-0018
    read seam (same fake client), in the DTO shape — the seam now hits real tables."""
    client = FakeSupabaseClient()
    proj = SupabaseProjectRepository(client)
    runs = SupabaseAnalysisRunRepository(client)
    notifs = SupabaseNotificationRepository(client)
    reader = SupabaseProjectionReader(client)

    proj.create({"project_id": PROJECT, "workspace_id": WS_A,
                 "lifecycle_state": "created", "title": "t"})
    run_id = str(uuid.uuid4())
    runs.create({"analysis_run_id": run_id, "project_id": PROJECT,
                 "run_type": "fast_analysis_pass", "run_status": "queued",
                 "started_at": "2026-06-26T00:00:00Z"})
    notif_id = str(uuid.uuid4())
    notifs.create({"notification_id": notif_id, "workspace_id": WS_A,
                   "project_id": PROJECT, "source_object_type": "analysis_run",
                   "source_object_id": run_id, "event_type": "deep_analysis_completed",
                   "state": "created"})

    listed = reader.list_projects(WS_A)
    assert [Project(**r).project_id for r in listed] == [PROJECT]
    assert reader.get_project(PROJECT)["workspace_id"] == WS_A

    seam_runs = reader.list_analysis_runs(PROJECT)
    assert [AnalysisRun(**r).analysis_run_id for r in seam_runs] == [run_id]
    assert reader.get_analysis_run(run_id)["run_status"] == "queued"

    seam_notifs = reader.list_notifications(WS_A)
    assert [Notification(**r).notification_id for r in seam_notifs] == [notif_id]


def test_read_seam_workspace_scoping_for_projects() -> None:
    client = FakeSupabaseClient()
    proj = SupabaseProjectRepository(client)
    reader = SupabaseProjectionReader(client)
    proj.create({"project_id": str(uuid.uuid4()), "workspace_id": WS_A,
                 "lifecycle_state": "created"})
    proj.create({"project_id": str(uuid.uuid4()), "workspace_id": WS_B,
                 "lifecycle_state": "created"})
    assert len(reader.list_projects(WS_A)) == 1
    assert len(reader.list_projects(WS_B)) == 1

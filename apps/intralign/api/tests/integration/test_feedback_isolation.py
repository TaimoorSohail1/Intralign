from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

from oslo_api.feedback import (
    FeedbackCategory,
    FeedbackContext,
    FeedbackImpact,
    FeedbackService,
    SqlFeedbackRepository,
)
from oslo_api.settings import Settings

DATABASE_URL = Settings().database_url  # type: ignore[call-arg]


def test_feedback_role_can_file_a_ticket_but_cannot_write_canonical_history() -> None:
    engine = create_engine(DATABASE_URL)
    repository = SqlFeedbackRepository(engine)
    session_id = f"guard-{uuid4().hex}"
    workspace_id = uuid4()
    actor_user_id = uuid4()
    service = FeedbackService(
        repository=repository,
        clock=lambda: datetime(2026, 8, 16, 10, 30, tzinfo=UTC),
    )

    ticket = service.file_ticket(
        actor_user_id=actor_user_id,
        workspace_id=workspace_id,
        session_id=session_id,
        category=FeedbackCategory.DEFECT,
        body="The report used GBP 1,845,000 twice.",
        expected="Show the figure once.",
        impact=FeedbackImpact.SLOWING,
        context=FeedbackContext(
            where="Reports",
            view="reports",
            role="owner",
            grounded_x=4,
            total_y=13,
            first_run_flag=False,
            ts="2026-08-16T10:29:00Z",
        ),
    )

    assert repository.list_for_session(
        actor_user_id=actor_user_id,
        workspace_id=workspace_id,
        session_id=session_id,
    ) == [ticket]

    with engine.connect() as connection:
        transaction = connection.begin()
        connection.execute(text("set local role feedback_service"))
        with pytest.raises(ProgrammingError) as denied:
            connection.execute(
                text("delete from public.project_history_events where false"),
            )
        transaction.rollback()

    assert getattr(denied.value.orig, "sqlstate", None) == "42501"

    with engine.begin() as connection:
        connection.execute(
            text("delete from feedback_svc.events where ticket_id = :ticket_id"),
            {"ticket_id": ticket.ticket_id},
        )
        connection.execute(
            text("delete from feedback_svc.tickets where id = :id"),
            {"id": ticket.id},
        )
    engine.dispose()

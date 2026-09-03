from datetime import UTC, datetime
from uuid import UUID

from oslo_api.feedback import (
    FeedbackCategory,
    FeedbackContext,
    FeedbackImpact,
    FeedbackService,
)

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
TICKET_ID = UUID("018f9f7e-8de2-7000-8000-000000000012")


class RecordingFeedbackRepository:
    def __init__(self) -> None:
        self.tickets = []
        self.events = []

    def reserve_ticket_id(self, category) -> str:
        return {
            FeedbackCategory.DEFECT: "DEF-0001",
            FeedbackCategory.ENHANCEMENT: "ENH-0001",
            FeedbackCategory.OTHER: "NOTE-0001",
        }[category]

    def file(self, *, ticket, event) -> None:
        self.tickets.append(ticket)
        self.events.append(event)

    def list_for_session(self, **_kwargs):
        return list(self.tickets)


def test_feedback_is_sanitized_and_emits_no_free_text_or_history_payload() -> None:
    repository = RecordingFeedbackRepository()
    service = FeedbackService(
        repository=repository,
        clock=lambda: datetime(2026, 8, 16, 9, 30, tzinfo=UTC),
        new_id=lambda: TICKET_ID,
    )

    ticket = service.file_ticket(
        actor_user_id=USER_ID,
        workspace_id=WORKSPACE_ID,
        session_id="browser-session-001",
        category=FeedbackCategory.DEFECT,
        body="The GBP 1,845,000 forecast appears twice for owner@example.com.",
        expected="Show one approved forecast of GBP 1,800,000.",
        impact=FeedbackImpact.BLOCKING,
        context=FeedbackContext(
            where="Reports",
            view="reports",
            role="owner",
            grounded_x=4,
            total_y=13,
            first_run_flag=False,
            ts="2026-08-16T09:29:00Z",
        ),
    )

    assert ticket.ticket_id == "DEF-0001"
    assert ticket.status == "Filed"
    assert "1,845,000" not in ticket.body
    assert "owner@example.com" not in ticket.body
    assert "1,800,000" not in (ticket.expected or "")
    assert "[redacted]" in ticket.body
    assert repository.events == [
        {
            "event_name": "feedback_filed",
            "ticket_id": "DEF-0001",
            "category": "defect",
            "session_id": "browser-session-001",
            "occurred_at": "2026-08-16T09:30:00+00:00",
        }
    ]
    assert "body" not in repository.events[0]
    assert "expected" not in repository.events[0]


def test_feedback_context_is_metadata_only() -> None:
    context = FeedbackContext(
        where="Grounding map",
        view="grounding",
        role="owner",
        grounded_x=4,
        total_y=13,
        first_run_flag=False,
        ts="2026-08-16T09:29:00Z",
    )

    assert set(context.as_dict()) == {
        "where",
        "view",
        "role",
        "grounded_x",
        "total_y",
        "first_run_flag",
        "ts",
    }
    assert "project_id" not in context.as_dict()
    assert "plan" not in context.as_dict()


def test_enhancement_drops_defect_only_fields() -> None:
    repository = RecordingFeedbackRepository()
    service = FeedbackService(repository=repository, new_id=lambda: TICKET_ID)

    ticket = service.file_ticket(
        actor_user_id=USER_ID,
        workspace_id=WORKSPACE_ID,
        session_id="browser-session-001",
        category=FeedbackCategory.ENHANCEMENT,
        body="Let me save report audience defaults.",
        expected="This field is not part of an enhancement ticket.",
        impact=FeedbackImpact.SLOWING,
        context=FeedbackContext(
            where="Reports",
            view="reports",
            role="owner",
            grounded_x=4,
            total_y=13,
            first_run_flag=False,
            ts="2026-08-16T09:29:00Z",
        ),
    )

    assert ticket.expected is None
    assert ticket.impact is None

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID, uuid4

from sqlalchemy import Engine, text


class FeedbackCategory(StrEnum):
    DEFECT = "defect"
    ENHANCEMENT = "enhancement"
    OTHER = "other"


class FeedbackImpact(StrEnum):
    BLOCKING = "blocking"
    SLOWING = "slowing"
    MINOR = "minor"


@dataclass(frozen=True, slots=True)
class FeedbackContext:
    where: str
    view: str
    role: str
    grounded_x: int
    total_y: int
    first_run_flag: bool
    ts: str

    def as_dict(self) -> dict[str, object]:
        return {
            "where": self.where,
            "view": self.view,
            "role": self.role,
            "grounded_x": self.grounded_x,
            "total_y": self.total_y,
            "first_run_flag": self.first_run_flag,
            "ts": self.ts,
        }


@dataclass(frozen=True, slots=True)
class FeedbackTicket:
    id: UUID
    ticket_id: str
    actor_user_id: UUID
    workspace_id: UUID
    session_id: str
    category: FeedbackCategory
    title: str
    body: str
    expected: str | None
    impact: FeedbackImpact | None
    context: FeedbackContext
    status: str
    created_at: datetime


class FeedbackRepository(Protocol):
    def reserve_ticket_id(self, category: FeedbackCategory) -> str: ...

    def file(self, *, ticket: FeedbackTicket, event: dict[str, str]) -> None: ...

    def list_for_session(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
    ) -> list[FeedbackTicket]: ...


class FeedbackApplication(Protocol):
    def file_ticket(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
        category: FeedbackCategory,
        body: str,
        expected: str | None,
        impact: FeedbackImpact | None,
        context: FeedbackContext,
    ) -> FeedbackTicket: ...

    def list_session_tickets(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
    ) -> list[FeedbackTicket]: ...


_CURRENCY_AMOUNT = re.compile(
    r"(?i)(?:\b(?:GBP|USD|EUR|CAD|AUD)\s*|[\u0024\u00a3\u20ac]\s*)"
    r"\d[\d,]*(?:\.\d+)?\b"
)
_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_UUID = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_feedback_text(value: str, *, limit: int = 4000) -> str:
    """Apply the Slice 8 egress scan before anything reaches the queue."""

    sanitized = _CONTROL.sub("", value).strip()
    sanitized = _CURRENCY_AMOUNT.sub("[redacted]", sanitized)
    sanitized = _EMAIL.sub("[redacted]", sanitized)
    sanitized = _UUID.sub("[redacted]", sanitized)
    return sanitized[:limit]


class FeedbackService:
    def __init__(
        self,
        *,
        repository: FeedbackRepository,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        new_id: Callable[[], UUID] = uuid4,
    ) -> None:
        self._repository = repository
        self._clock = clock
        self._new_id = new_id

    def file_ticket(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
        category: FeedbackCategory,
        body: str,
        expected: str | None,
        impact: FeedbackImpact | None,
        context: FeedbackContext,
    ) -> FeedbackTicket:
        created_at = self._clock()
        sanitized_body = sanitize_feedback_text(body)
        sanitized_expected = (
            sanitize_feedback_text(expected)
            if category is FeedbackCategory.DEFECT and expected and expected.strip()
            else None
        )
        compact_title = " ".join(sanitized_body.split())[:80]
        ticket = FeedbackTicket(
            id=self._new_id(),
            ticket_id=self._repository.reserve_ticket_id(category),
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            session_id=session_id,
            category=category,
            title=compact_title,
            body=sanitized_body,
            expected=sanitized_expected,
            impact=impact if category is FeedbackCategory.DEFECT else None,
            context=context,
            status="Filed",
            created_at=created_at,
        )
        event = {
            "event_name": "feedback_filed",
            "ticket_id": ticket.ticket_id,
            "category": category.value,
            "session_id": session_id,
            "occurred_at": created_at.isoformat(),
        }
        self._repository.file(ticket=ticket, event=event)
        return ticket

    def list_session_tickets(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
    ) -> list[FeedbackTicket]:
        return self._repository.list_for_session(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            session_id=session_id,
        )


class SqlFeedbackRepository:
    """Runs every queue query under the database-isolated feedback role."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    @staticmethod
    def _assume_isolated_role(connection) -> None:
        connection.execute(text("set local role feedback_service"))

    def reserve_ticket_id(self, category: FeedbackCategory) -> str:
        sequence = {
            FeedbackCategory.DEFECT: "feedback_svc.defect_ticket_seq",
            FeedbackCategory.ENHANCEMENT: "feedback_svc.enhancement_ticket_seq",
            FeedbackCategory.OTHER: "feedback_svc.note_ticket_seq",
        }[category]
        prefix = {
            FeedbackCategory.DEFECT: "DEF",
            FeedbackCategory.ENHANCEMENT: "ENH",
            FeedbackCategory.OTHER: "NOTE",
        }[category]
        with self._engine.begin() as connection:
            self._assume_isolated_role(connection)
            number = connection.execute(text(f"select nextval('{sequence}')")).scalar_one()
        return f"{prefix}-{number:04d}"

    def file(self, *, ticket: FeedbackTicket, event: dict[str, str]) -> None:
        with self._engine.begin() as connection:
            self._assume_isolated_role(connection)
            connection.execute(
                text(
                    """
                    insert into feedback_svc.tickets (
                      id, ticket_id, actor_user_id, workspace_id, session_id,
                      category, title, body, expected, impact, repro_context,
                      status, created_at
                    ) values (
                      :id, :ticket_id, :actor_user_id, :workspace_id, :session_id,
                      :category, :title, :body, :expected, :impact,
                      cast(:repro_context as jsonb), :status, :created_at
                    )
                    """
                ),
                {
                    "id": ticket.id,
                    "ticket_id": ticket.ticket_id,
                    "actor_user_id": ticket.actor_user_id,
                    "workspace_id": ticket.workspace_id,
                    "session_id": ticket.session_id,
                    "category": ticket.category.value,
                    "title": ticket.title,
                    "body": ticket.body,
                    "expected": ticket.expected,
                    "impact": ticket.impact.value if ticket.impact else None,
                    "repro_context": json.dumps(ticket.context.as_dict()),
                    "status": ticket.status,
                    "created_at": ticket.created_at,
                },
            )
            connection.execute(
                text(
                    """
                    insert into feedback_svc.events (
                      id, workspace_id, actor_user_id, session_id,
                      event_name, ticket_id, payload, occurred_at
                    ) values (
                      :id, :workspace_id, :actor_user_id, :session_id,
                      :event_name, :ticket_id, cast(:payload as jsonb), :occurred_at
                    )
                    """
                ),
                {
                    "id": uuid4(),
                    "workspace_id": ticket.workspace_id,
                    "actor_user_id": ticket.actor_user_id,
                    "session_id": ticket.session_id,
                    "event_name": event["event_name"],
                    "ticket_id": ticket.ticket_id,
                    "payload": json.dumps(
                        {"category": event["category"], "ticket_id": event["ticket_id"]}
                    ),
                    "occurred_at": ticket.created_at,
                },
            )

    def list_for_session(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        session_id: str,
    ) -> list[FeedbackTicket]:
        with self._engine.begin() as connection:
            self._assume_isolated_role(connection)
            rows = (
                connection.execute(
                    text(
                        """
                        select id, ticket_id, actor_user_id, workspace_id, session_id,
                               category, title, body, expected, impact, repro_context,
                               status, created_at
                        from feedback_svc.tickets
                        where actor_user_id = :actor_user_id
                          and workspace_id = :workspace_id
                          and session_id = :session_id
                        order by created_at desc, ticket_id desc
                        """
                    ),
                    {
                        "actor_user_id": actor_user_id,
                        "workspace_id": workspace_id,
                        "session_id": session_id,
                    },
                )
                .mappings()
                .all()
            )
        return [
            FeedbackTicket(
                id=row["id"],
                ticket_id=row["ticket_id"],
                actor_user_id=row["actor_user_id"],
                workspace_id=row["workspace_id"],
                session_id=row["session_id"],
                category=FeedbackCategory(row["category"]),
                title=row["title"],
                body=row["body"],
                expected=row["expected"],
                impact=FeedbackImpact(row["impact"]) if row["impact"] else None,
                context=FeedbackContext(**row["repro_context"]),
                status=row["status"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

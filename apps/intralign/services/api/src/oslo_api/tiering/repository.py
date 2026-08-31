import json
from datetime import date
from uuid import UUID

from sqlalchemy import Connection, text

from oslo_api.tiering.policy import PlanCode, PlanPolicy, get_plan_policy


def get_workspace_plan(connection: Connection, workspace_id: UUID) -> PlanPolicy:
    plan_code = connection.execute(
        text(
            """
            select plan_code
            from public.workspace_subscriptions
            where workspace_id = :workspace_id
              and (
                status = 'active'
                or (status = 'past_due' and grace_ends_at > now())
              )
            """
        ),
        {"workspace_id": workspace_id},
    ).scalar_one_or_none()
    return get_plan_policy(plan_code or PlanCode.FREE)


def count_monthly_analysis_usage(
    connection: Connection,
    *,
    workspace_id: UUID,
    period_start: date | None = None,
) -> int:
    return int(
        connection.execute(
            text(
                """
                select count(*)
                from public.workspace_analysis_usage
                where workspace_id = :workspace_id
                  and period_start = coalesce(
                    :period_start,
                    date_trunc('month', now())::date
                  )
                """
            ),
            {"workspace_id": workspace_id, "period_start": period_start},
        ).scalar_one()
    )


def record_limit_event(
    connection: Connection,
    *,
    workspace_id: UUID,
    actor_user_id: UUID | None,
    project_id: UUID | None,
    limit_kind: str,
    outcome: str,
    details: dict[str, object],
    idempotency_key: str,
) -> None:
    connection.execute(
        text(
            """
            insert into public.workspace_limit_events (
              workspace_id, actor_user_id, project_id, limit_kind,
              outcome, details, idempotency_key
            ) values (
              :workspace_id, :actor_user_id, :project_id, :limit_kind,
              :outcome, cast(:details as jsonb), :idempotency_key
            )
            on conflict (workspace_id, idempotency_key) do nothing
            """
        ),
        {
            "workspace_id": workspace_id,
            "actor_user_id": actor_user_id,
            "project_id": project_id,
            "limit_kind": limit_kind,
            "outcome": outcome,
            "details": json.dumps(details),
            "idempotency_key": idempotency_key,
        },
    )

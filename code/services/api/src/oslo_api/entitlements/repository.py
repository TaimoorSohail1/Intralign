import json
from uuid import UUID, uuid4

from sqlalchemy import Engine, text
from sqlalchemy.engine import Connection, RowMapping

from oslo_api.entitlements.service import (
    BillingCustomerMissing,
    BillingPermissionDenied,
    OutcomeCapacityReached,
    OutcomeNotFound,
    OutcomePermissionDenied,
    UnknownCheckoutSession,
    UnknownSubscription,
)
from oslo_api.slice_four import (
    BillingInterval,
    EntitlementView,
    IntentChoice,
    OutcomeProvenance,
    OutcomeStatus,
    ProjectOutcome,
    SubscriptionState,
    VerifiedCheckoutCompletion,
    VerifiedSubscriptionState,
    WallKey,
)
from oslo_api.tiering.policy import get_plan_policy
from oslo_api.tiering.repository import record_limit_event


class SqlEntitlementRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def require_owner(self, *, workspace_id: UUID, actor_user_id: UUID) -> None:
        with self._engine.connect() as connection:
            is_owner = connection.execute(
                text(
                    "select exists (select 1 from public.memberships "
                    "where workspace_id = :workspace_id and user_id = :actor_user_id "
                    "and role = 'owner')"
                ),
                {"workspace_id": workspace_id, "actor_user_id": actor_user_id},
            ).scalar_one()
        if not is_owner:
            raise BillingPermissionDenied

    def get_entitlement(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> EntitlementView:
        with self._engine.connect() as connection:
            role = connection.execute(
                text(
                    "select role from public.memberships "
                    "where workspace_id = :workspace_id and user_id = :actor_user_id"
                ),
                {"workspace_id": workspace_id, "actor_user_id": actor_user_id},
            ).scalar_one_or_none()
            if role is None:
                raise OutcomePermissionDenied
            subscription = connection.execute(
                text(
                    "select plan_code, status, cancel_at_period_end, current_period_end, "
                    "grace_ends_at from public.workspace_subscriptions "
                    "where workspace_id = :workspace_id"
                ),
                {"workspace_id": workspace_id},
            ).mappings().one_or_none()
            policy = self._workspace_policy(connection, workspace_id)
        return EntitlementView(
            workspace_id=workspace_id,
            tier=policy.code.value,
            enforcement_mode="enforce",
            max_active_outcomes=policy.active_outcome_limit,
            max_active_plans=policy.active_project_limit,
            intake_word_envelope=policy.word_limit,
            never_metered_exemptions=policy.never_metered_exemptions,
            subscription_status=(subscription["status"] if subscription else "active"),
            cancel_at_period_end=(
                bool(subscription["cancel_at_period_end"]) if subscription else False
            ),
            current_period_end=(subscription["current_period_end"] if subscription else None),
            grace_ends_at=(subscription["grace_ends_at"] if subscription else None),
            can_manage_billing=role == "owner",
        )

    def customer_id_for_owner(
        self, *, workspace_id: UUID, actor_user_id: UUID
    ) -> str:
        self.require_owner(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
        )
        with self._engine.connect() as connection:
            customer_id = connection.execute(
                text(
                    "select provider_customer_id from public.workspace_subscriptions "
                    "where workspace_id = :workspace_id"
                ),
                {"workspace_id": workspace_id},
            ).scalar_one_or_none()
        if not customer_id:
            raise BillingCustomerMissing
        return str(customer_id)

    @staticmethod
    def _require_member(
        connection: Connection, *, workspace_id: UUID, actor_user_id: UUID
    ) -> None:
        is_member = connection.execute(
            text(
                "select exists (select 1 from public.memberships "
                "where workspace_id = :workspace_id and user_id = :actor_user_id)"
            ),
            {"workspace_id": workspace_id, "actor_user_id": actor_user_id},
        ).scalar_one()
        if not is_member:
            raise OutcomePermissionDenied

    @staticmethod
    def _outcome_from_row(row: RowMapping) -> ProjectOutcome:
        return ProjectOutcome(
            id=row["id"],
            workspace_id=row["workspace_id"],
            project_id=row["project_id"],
            title=row["title"],
            status=OutcomeStatus(row["status"]),
            is_primary=row["is_primary"],
            provenance=OutcomeProvenance(row["provenance"]),
            created_at=row["created_at"],
            archived_at=row["archived_at"],
        )

    @staticmethod
    def _lock_workspace(connection: Connection, workspace_id: UUID) -> None:
        connection.execute(
            text("select pg_advisory_xact_lock(hashtextextended(:key, 0))"),
            {"key": str(workspace_id)},
        )

    @staticmethod
    def _workspace_policy(connection: Connection, workspace_id: UUID):
        plan_code = connection.execute(
            text(
                "select plan_code from public.workspace_subscriptions "
                "where workspace_id = :workspace_id and ("
                "status = 'active' or (status = 'past_due' and grace_ends_at > now()))"
            ),
            {"workspace_id": workspace_id},
        ).scalar_one_or_none()
        return get_plan_policy(plan_code or "free")

    def create_outcome(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
        title: str,
        provenance: OutcomeProvenance,
    ) -> ProjectOutcome:
        blocked_limit: int | None = None
        row: RowMapping | None = None
        with self._engine.begin() as connection:
            self._require_member(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
            )
            project_exists = connection.execute(
                text(
                    "select exists (select 1 from public.projects "
                    "where id = :project_id and workspace_id = :workspace_id)"
                ),
                {"project_id": project_id, "workspace_id": workspace_id},
            ).scalar_one()
            if not project_exists:
                raise OutcomeNotFound
            self._lock_workspace(connection, workspace_id)
            policy = self._workspace_policy(connection, workspace_id)
            active_count = connection.execute(
                text(
                    "select count(*) from public.project_outcomes outcome "
                    "join public.projects project on project.id = outcome.project_id "
                    "where outcome.workspace_id = :workspace_id "
                    "and outcome.status = 'active' and project.archived_at is null"
                ),
                {"workspace_id": workspace_id},
            ).scalar_one()
            if (
                policy.active_outcome_limit is not None
                and active_count >= policy.active_outcome_limit
            ):
                blocked_limit = policy.active_outcome_limit
                record_limit_event(
                    connection,
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=project_id,
                    limit_kind="active_outcomes",
                    outcome="blocked",
                    details={
                        "active_count": int(active_count),
                        "limit": blocked_limit,
                        "wall_key": WallKey.MULTI_OUTCOME.value,
                    },
                    idempotency_key=f"outcome-capacity:{uuid4()}",
                )
            else:
                is_primary = not connection.execute(
                    text(
                        "select exists (select 1 from public.project_outcomes "
                        "where project_id = :project_id)"
                    ),
                    {"project_id": project_id},
                ).scalar_one()
                row = connection.execute(
                    text(
                        "insert into public.project_outcomes "
                        "(workspace_id, project_id, title, is_primary, provenance, "
                        " created_by) values "
                        "(:workspace_id, :project_id, :title, :is_primary, "
                        " :provenance, :actor_user_id) "
                        "returning id, workspace_id, project_id, title, status, "
                        "is_primary, provenance, created_at, archived_at"
                    ),
                    {
                        "workspace_id": workspace_id,
                        "project_id": project_id,
                        "title": title,
                        "is_primary": is_primary,
                        "provenance": provenance.value,
                        "actor_user_id": actor_user_id,
                    },
                ).mappings().one()
        if blocked_limit is not None:
            raise OutcomeCapacityReached(active_outcome_limit=blocked_limit)
        if row is None:
            raise RuntimeError("OUTCOME_CREATE_DID_NOT_RETURN_A_ROW")
        return self._outcome_from_row(row)

    def list_outcomes(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
    ) -> list[ProjectOutcome]:
        with self._engine.connect() as connection:
            self._require_member(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
            )
            rows = connection.execute(
                text(
                    "select id, workspace_id, project_id, title, status, is_primary, "
                    "provenance, created_at, archived_at from public.project_outcomes "
                    "where workspace_id = :workspace_id and project_id = :project_id "
                    "order by created_at, id"
                ),
                {"workspace_id": workspace_id, "project_id": project_id},
            ).mappings().all()
        return [self._outcome_from_row(row) for row in rows]

    def archive_outcome(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        outcome_id: UUID,
    ) -> ProjectOutcome:
        with self._engine.begin() as connection:
            self._require_member(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
            )
            row = connection.execute(
                text(
                    "update public.project_outcomes set status = 'archived', "
                    "archived_at = coalesce(archived_at, now()), updated_at = now() "
                    "where id = :outcome_id and workspace_id = :workspace_id "
                    "returning id, workspace_id, project_id, title, status, is_primary, "
                    "provenance, created_at, archived_at"
                ),
                {"outcome_id": outcome_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
            if row is None:
                raise OutcomeNotFound
        return self._outcome_from_row(row)

    def reactivate_outcome(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        outcome_id: UUID,
    ) -> ProjectOutcome:
        blocked_limit: int | None = None
        row: RowMapping | None = None
        with self._engine.begin() as connection:
            self._require_member(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
            )
            self._lock_workspace(connection, workspace_id)
            current = connection.execute(
                text(
                    "select id, workspace_id, project_id, title, status, is_primary, "
                    "provenance, created_at, archived_at from public.project_outcomes "
                    "where id = :outcome_id and workspace_id = :workspace_id for update"
                ),
                {"outcome_id": outcome_id, "workspace_id": workspace_id},
            ).mappings().one_or_none()
            if current is None:
                raise OutcomeNotFound
            if current["status"] == "active":
                return self._outcome_from_row(current)
            policy = self._workspace_policy(connection, workspace_id)
            active_count = connection.execute(
                text(
                    "select count(*) from public.project_outcomes outcome "
                    "join public.projects project on project.id = outcome.project_id "
                    "where outcome.workspace_id = :workspace_id "
                    "and outcome.status = 'active' and project.archived_at is null"
                ),
                {"workspace_id": workspace_id},
            ).scalar_one()
            if (
                policy.active_outcome_limit is not None
                and active_count >= policy.active_outcome_limit
            ):
                blocked_limit = policy.active_outcome_limit
                record_limit_event(
                    connection,
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=current["project_id"],
                    limit_kind="active_outcomes",
                    outcome="blocked",
                    details={
                        "active_count": int(active_count),
                        "limit": blocked_limit,
                        "wall_key": WallKey.MULTI_OUTCOME.value,
                        "reactivation": True,
                    },
                    idempotency_key=f"outcome-reactivation-capacity:{uuid4()}",
                )
            else:
                row = connection.execute(
                    text(
                        "update public.project_outcomes set status = 'active', "
                        "archived_at = null, updated_at = now() "
                        "where id = :outcome_id returning id, workspace_id, project_id, "
                        "title, status, is_primary, provenance, created_at, archived_at"
                    ),
                    {"outcome_id": outcome_id},
                ).mappings().one()
        if blocked_limit is not None:
            raise OutcomeCapacityReached(active_outcome_limit=blocked_limit)
        if row is None:
            raise RuntimeError("OUTCOME_REACTIVATION_DID_NOT_RETURN_A_ROW")
        return self._outcome_from_row(row)

    def record_intent(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        wall_key: WallKey,
        chosen_path: IntentChoice,
        full_option_set: tuple[str, ...],
        context: dict[str, object],
    ) -> None:
        with self._engine.begin() as connection:
            self._require_member(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
            )
            connection.execute(
                text(
                    "insert into public.intent_signals "
                    "(workspace_id, actor_user_id, wall_key, chosen_path, "
                    " full_option_set, context) values "
                    "(:workspace_id, :actor_user_id, :wall_key, :chosen_path, "
                    " cast(:full_option_set as jsonb), cast(:context as jsonb))"
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "wall_key": wall_key.value,
                    "chosen_path": chosen_path.value,
                    "full_option_set": json.dumps(list(full_option_set)),
                    "context": json.dumps(context),
                },
            )

    def record_checkout_started(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        checkout_session_id: str,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> None:
        basic = get_plan_policy("basic")
        price_usd = (
            basic.price_usd_monthly
            if interval is BillingInterval.MONTHLY
            else basic.price_usd_annual
        )
        with self._engine.begin() as connection:
            connection.execute(
                text(
                    "insert into public.billing_checkout_sessions "
                    "(id, workspace_id, actor_user_id, billing_interval, price_usd, wall_key) "
                    "values (:id, :workspace_id, :actor_user_id, :interval, :price_usd, "
                    ":wall_key)"
                ),
                {
                    "id": checkout_session_id,
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "interval": interval.value,
                    "price_usd": price_usd,
                    "wall_key": wall_key.value,
                },
            )
            connection.execute(
                text(
                    "insert into public.intent_signals "
                    "(workspace_id, actor_user_id, wall_key, chosen_path, "
                    " full_option_set, context) "
                    "values (:workspace_id, :actor_user_id, :wall_key, 'keep_both', "
                    " cast(:full_option_set as jsonb), cast(:context as jsonb))"
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "wall_key": wall_key.value,
                    "full_option_set": json.dumps(
                        ["archive_to_switch", "upgrade_basic", "not_now"]
                    ),
                    "context": json.dumps({"checkout_session_id": checkout_session_id}),
                },
            )

    def commit_checkout_and_grant_basic(
        self, *, completion: VerifiedCheckoutCompletion
    ) -> None:
        with self._engine.begin() as connection:
            new_event = connection.execute(
                text(
                    "insert into public.billing_webhook_events (event_id, event_type) "
                    "values (:event_id, 'checkout.session.completed') "
                    "on conflict (event_id) do nothing returning event_id"
                ),
                {"event_id": completion.event_id},
            ).scalar_one_or_none()
            if new_event is None:
                return

            checkout = connection.execute(
                text(
                    "select workspace_id, actor_user_id, billing_interval, price_usd, "
                    "wall_key, status "
                    "from public.billing_checkout_sessions "
                    "where id = :checkout_session_id for update"
                ),
                {"checkout_session_id": completion.checkout_session_id},
            ).mappings().one_or_none()
            if checkout is None or checkout["workspace_id"] != completion.workspace_id:
                raise UnknownCheckoutSession
            if checkout["status"] == "committed":
                return

            connection.execute(
                text(
                    "update public.billing_checkout_sessions "
                    "set status = 'committed', committed_at = now() "
                    "where id = :checkout_session_id"
                ),
                {"checkout_session_id": completion.checkout_session_id},
            )
            connection.execute(
                text(
                    "insert into public.commitment_logs "
                    "(workspace_id, checkout_session_id, provider_event_id, plan_code, "
                    " billing_interval, price_usd) "
                    "values (:workspace_id, :checkout_session_id, :event_id, 'basic', "
                    " :billing_interval, :price_usd)"
                ),
                {
                    "workspace_id": completion.workspace_id,
                    "checkout_session_id": completion.checkout_session_id,
                    "event_id": completion.event_id,
                    "billing_interval": checkout["billing_interval"],
                    "price_usd": checkout["price_usd"],
                },
            )
            connection.execute(
                text(
                    "insert into public.workspace_subscriptions "
                    "(workspace_id, plan_code, status, changed_by, provider_customer_id, "
                    " provider_subscription_id, started_at, updated_at) "
                    "values (:workspace_id, 'basic', 'active', :actor_user_id, "
                    " :customer_id, :subscription_id, now(), now()) "
                    "on conflict (workspace_id) do update set "
                    "plan_code = 'basic', status = 'active', "
                    "changed_by = excluded.changed_by, "
                    "provider_customer_id = excluded.provider_customer_id, "
                    "provider_subscription_id = excluded.provider_subscription_id, "
                    "cancel_at_period_end = false, grace_ends_at = null, updated_at = now()"
                ),
                {
                    "workspace_id": completion.workspace_id,
                    "actor_user_id": checkout["actor_user_id"],
                    "customer_id": completion.customer_id,
                    "subscription_id": completion.subscription_id,
                },
            )
            connection.execute(
                text(
                    "insert into public.intent_signals "
                    "(workspace_id, actor_user_id, wall_key, chosen_path, "
                    " full_option_set, context) "
                    "values (:workspace_id, :actor_user_id, :wall_key, 'committed', "
                    " cast(:full_option_set as jsonb), cast(:context as jsonb))"
                ),
                {
                    "workspace_id": completion.workspace_id,
                    "actor_user_id": checkout["actor_user_id"],
                    "wall_key": checkout["wall_key"],
                    "full_option_set": json.dumps(
                        ["archive_to_switch", "upgrade_basic", "not_now"]
                    ),
                    "context": json.dumps(
                        {"checkout_session_id": completion.checkout_session_id}
                    ),
                },
            )

    def apply_subscription_state(self, *, change: VerifiedSubscriptionState) -> None:
        with self._engine.begin() as connection:
            new_event = connection.execute(
                text(
                    "insert into public.billing_webhook_events (event_id, event_type) "
                    "values (:event_id, 'customer.subscription.state') "
                    "on conflict (event_id) do nothing returning event_id"
                ),
                {"event_id": change.event_id},
            ).scalar_one_or_none()
            if new_event is None:
                return
            if change.state is SubscriptionState.CANCELLED:
                updated = connection.execute(
                    text(
                        "update public.workspace_subscriptions set plan_code = 'free', "
                        "status = 'cancelled', cancel_at_period_end = false, "
                        "current_period_end = :current_period_end, grace_ends_at = null, "
                        "updated_at = now() "
                        "where provider_subscription_id = :subscription_id"
                    ),
                    {
                        "subscription_id": change.subscription_id,
                        "current_period_end": change.current_period_end,
                    },
                )
                if updated.rowcount == 0:
                    raise UnknownSubscription
                return
            status_value = (
                "active"
                if change.state is SubscriptionState.ACTIVE
                else "past_due"
            )
            updated = connection.execute(
                text(
                    "update public.workspace_subscriptions set plan_code = 'basic', "
                    "status = :status, cancel_at_period_end = :cancel_at_period_end, "
                    "current_period_end = :current_period_end, "
                    "grace_ends_at = :grace_ends_at, updated_at = now() "
                    "where provider_subscription_id = :subscription_id"
                ),
                {
                    "subscription_id": change.subscription_id,
                    "status": status_value,
                    "cancel_at_period_end": change.cancel_at_period_end,
                    "current_period_end": change.current_period_end,
                    "grace_ends_at": (
                        change.current_period_end
                        if change.state is SubscriptionState.PAST_DUE
                        else None
                    ),
                },
            )
            if updated.rowcount == 0:
                raise UnknownSubscription

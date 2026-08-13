from datetime import UTC, datetime
from uuid import UUID

import httpx
import pytest
from sqlalchemy import create_engine, text

from oslo_api.application import ActiveProjectLimitReached, DatabaseSliceOneApplication
from oslo_api.email import SmtpInvitationMailer
from oslo_api.entitlements.repository import SqlEntitlementRepository
from oslo_api.entitlements.service import OutcomeCapacityReached, UnknownSubscription
from oslo_api.identity import SupabaseIdentityProvider
from oslo_api.settings import Settings
from oslo_api.slice_four import (
    BillingInterval,
    IntentChoice,
    OutcomeProvenance,
    OutcomeStatus,
    SubscriptionState,
    VerifiedCheckoutCompletion,
    VerifiedSubscriptionState,
    WallKey,
)
from oslo_api.tiering.repository import get_workspace_plan

SETTINGS = Settings()  # type: ignore[call-arg]
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000098")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000097")


@pytest.fixture
def entitlement_repository():
    engine = create_engine(SETTINGS.database_url)
    with engine.begin() as connection:
        connection.execute(
            text(
                "delete from public.billing_webhook_events "
                "where event_id in ('evt_slice_four', 'evt_lifecycle_checkout', "
                "'evt_lifecycle_past_due', 'evt_lifecycle_cancelled', "
                "'evt_unknown_subscription')"
            )
        )
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text(
                "insert into public.workspaces (id, name, created_by) "
                "values (:workspace_id, 'Slice Four Integration', :owner_id) "
                "on conflict (id) do update set created_by = excluded.created_by"
            ),
            {"workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
        connection.execute(
            text(
                "insert into public.projects (id, workspace_id, name, status, created_by) "
                "values (:project_id, :workspace_id, 'Slice Four Plan', 'active', :owner_id)"
            ),
            {
                "project_id": PROJECT_ID,
                "workspace_id": WORKSPACE_ID,
                "owner_id": owner_id,
            },
        )
        connection.execute(
            text("delete from public.memberships where workspace_id = :workspace_id"),
            {"workspace_id": WORKSPACE_ID},
        )
        connection.execute(
            text(
                "insert into public.memberships (workspace_id, user_id, role) "
                "values (:workspace_id, :owner_id, 'owner')"
            ),
            {"workspace_id": WORKSPACE_ID, "owner_id": owner_id},
        )
    yield SqlEntitlementRepository(engine), owner_id, engine
    with engine.begin() as connection:
        connection.execute(
            text("delete from public.workspaces where id = :workspace_id"),
            {"workspace_id": WORKSPACE_ID},
        )
        connection.execute(
            text(
                "delete from public.billing_webhook_events "
                "where event_id in ('evt_slice_four', 'evt_lifecycle_checkout', "
                "'evt_lifecycle_past_due', 'evt_lifecycle_cancelled', "
                "'evt_unknown_subscription')"
            )
        )
    engine.dispose()


def test_verified_checkout_grant_is_transactional_and_idempotent(
    entitlement_repository,
) -> None:
    repository, owner_id, engine = entitlement_repository
    repository.require_owner(workspace_id=WORKSPACE_ID, actor_user_id=owner_id)
    repository.record_checkout_started(
        workspace_id=WORKSPACE_ID,
        actor_user_id=owner_id,
        checkout_session_id="cs_test_slice_four",
        interval=BillingInterval.MONTHLY,
        wall_key=WallKey.MULTI_PLAN,
    )

    completion = VerifiedCheckoutCompletion(
        event_id="evt_slice_four",
        checkout_session_id="cs_test_slice_four",
        workspace_id=WORKSPACE_ID,
        customer_id="cus_slice_four",
        subscription_id="sub_slice_four",
    )
    repository.commit_checkout_and_grant_basic(completion=completion)
    repository.commit_checkout_and_grant_basic(completion=completion)

    with engine.connect() as connection:
        subscription = connection.execute(
            text(
                "select plan_code, status, provider_customer_id, "
                "provider_subscription_id from public.workspace_subscriptions "
                "where workspace_id = :workspace_id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).mappings().one()
        commitment_count = connection.execute(
            text(
                "select count(*) from public.commitment_logs "
                "where workspace_id = :workspace_id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
        checkout_intents = connection.execute(
            text(
                "select chosen_path from public.intent_signals "
                "where workspace_id = :workspace_id order by occurred_at, id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalars().all()

    assert dict(subscription) == {
        "plan_code": "basic",
        "status": "active",
        "provider_customer_id": "cus_slice_four",
        "provider_subscription_id": "sub_slice_four",
    }
    assert commitment_count == 1
    assert checkout_intents == ["keep_both", "committed"]


def test_out_of_order_subscription_event_rolls_back_so_stripe_can_retry(
    entitlement_repository,
) -> None:
    repository, _owner_id, engine = entitlement_repository

    with pytest.raises(UnknownSubscription):
        repository.apply_subscription_state(
            change=VerifiedSubscriptionState(
                event_id="evt_unknown_subscription",
                subscription_id="sub_not_yet_committed",
                state=SubscriptionState.ACTIVE,
                cancel_at_period_end=False,
                current_period_end=None,
            )
        )

    with engine.connect() as connection:
        stored_event = connection.execute(
            text(
                "select count(*) from public.billing_webhook_events "
                "where event_id = 'evt_unknown_subscription'"
            )
        ).scalar_one()
    assert stored_event == 0


def test_second_plan_gate_hit_is_durable(entitlement_repository) -> None:
    _repository, owner_id, engine = entitlement_repository
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=SupabaseIdentityProvider(
            client=httpx.Client(timeout=10),
            supabase_url=SETTINGS.supabase_url,
            api_key=SETTINGS.supabase_secret_key,
        ),
        mailer=SmtpInvitationMailer(
            host=SETTINGS.smtp_host,
            port=SETTINGS.smtp_port,
            sender=SETTINGS.email_sender,
        ),
        web_url=SETTINGS.web_url,
    )

    with pytest.raises(ActiveProjectLimitReached):
        application.start_first_project(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
        )

    with engine.connect() as connection:
        gate_hit = connection.execute(
            text(
                "select details from public.workspace_limit_events "
                "where workspace_id = :workspace_id and limit_kind = 'active_projects' "
                "and outcome = 'blocked' order by created_at desc limit 1"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
    assert gate_hit["wall_key"] == "multiPlan"


def test_free_outcome_archive_is_reversible_and_reactivation_respects_the_slot(
    entitlement_repository,
) -> None:
    repository, owner_id, engine = entitlement_repository
    first = repository.create_outcome(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        project_id=PROJECT_ID,
        title="Improve successful delivery",
        provenance=OutcomeProvenance.DECLARED,
    )

    with pytest.raises(OutcomeCapacityReached):
        repository.create_outcome(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            title="Reduce avoidable rework",
            provenance=OutcomeProvenance.DECLARED,
        )
    with engine.connect() as connection:
        blocked_gate_count = connection.execute(
            text(
                "select count(*) from public.workspace_limit_events "
                "where workspace_id = :workspace_id "
                "and limit_kind = 'active_outcomes' and outcome = 'blocked'"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
    assert blocked_gate_count == 1

    archived = repository.archive_outcome(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        outcome_id=first.id,
    )
    second = repository.create_outcome(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        project_id=PROJECT_ID,
        title="Reduce avoidable rework",
        provenance=OutcomeProvenance.DECLARED,
    )

    assert archived.status is OutcomeStatus.ARCHIVED
    assert [outcome.status for outcome in repository.list_outcomes(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        project_id=PROJECT_ID,
    )] == [OutcomeStatus.ARCHIVED, OutcomeStatus.ACTIVE]
    with pytest.raises(OutcomeCapacityReached):
        repository.reactivate_outcome(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            outcome_id=first.id,
        )

    repository.archive_outcome(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        outcome_id=second.id,
    )
    restored = repository.reactivate_outcome(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        outcome_id=first.id,
    )

    assert restored.status is OutcomeStatus.ACTIVE
    assert restored.title == "Improve successful delivery"
    with engine.connect() as connection:
        blocked_gate_count = connection.execute(
            text(
                "select count(*) from public.workspace_limit_events "
                "where workspace_id = :workspace_id "
                "and limit_kind = 'active_outcomes' and outcome = 'blocked'"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
    assert blocked_gate_count == 2


def test_every_intent_branch_is_durable(entitlement_repository) -> None:
    repository, owner_id, engine = entitlement_repository

    for chosen_path in IntentChoice:
        repository.record_intent(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            wall_key=WallKey.MULTI_OUTCOME,
            chosen_path=chosen_path,
            full_option_set=("archive_to_switch", "upgrade_basic", "not_now"),
            context={"surface": "outcome_gate"},
        )

    with engine.connect() as connection:
        choices = connection.execute(
            text(
                "select chosen_path from public.intent_signals "
                "where workspace_id = :workspace_id order by occurred_at, id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalars().all()

    assert choices == [choice.value for choice in IntentChoice]


def test_payment_grace_and_cancellation_preserve_existing_outcomes(
    entitlement_repository,
) -> None:
    repository, owner_id, engine = entitlement_repository
    repository.record_checkout_started(
        workspace_id=WORKSPACE_ID,
        actor_user_id=owner_id,
        checkout_session_id="cs_test_lifecycle",
        interval=BillingInterval.MONTHLY,
        wall_key=WallKey.MULTI_OUTCOME,
    )
    repository.commit_checkout_and_grant_basic(
        completion=VerifiedCheckoutCompletion(
            event_id="evt_lifecycle_checkout",
            checkout_session_id="cs_test_lifecycle",
            workspace_id=WORKSPACE_ID,
            customer_id="cus_lifecycle",
            subscription_id="sub_lifecycle",
        )
    )
    for title in ("First outcome", "Second outcome"):
        repository.create_outcome(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            title=title,
            provenance=OutcomeProvenance.DECLARED,
        )

    paid_through = datetime(2026, 8, 20, tzinfo=UTC)
    repository.apply_subscription_state(
        change=VerifiedSubscriptionState(
            event_id="evt_lifecycle_past_due",
            subscription_id="sub_lifecycle",
            state=SubscriptionState.PAST_DUE,
            cancel_at_period_end=False,
            current_period_end=paid_through,
        )
    )
    with engine.connect() as connection:
        assert get_workspace_plan(connection, WORKSPACE_ID).code.value == "basic"
    repository.apply_subscription_state(
        change=VerifiedSubscriptionState(
            event_id="evt_lifecycle_cancelled",
            subscription_id="sub_lifecycle",
            state=SubscriptionState.CANCELLED,
            cancel_at_period_end=False,
            current_period_end=paid_through,
        )
    )

    with pytest.raises(OutcomeCapacityReached):
        repository.create_outcome(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            title="Third outcome",
            provenance=OutcomeProvenance.DECLARED,
        )
    with engine.connect() as connection:
        entitlement = connection.execute(
            text(
                "select plan_code, status, grace_ends_at from public.workspace_subscriptions "
                "where workspace_id = :workspace_id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).mappings().one()
        outcomes = connection.execute(
            text(
                "select count(*) from public.project_outcomes "
                "where workspace_id = :workspace_id"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()

    assert dict(entitlement) == {
        "plan_code": "free",
        "status": "cancelled",
        "grace_ends_at": None,
    }
    assert outcomes == 2

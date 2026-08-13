import httpx
from sqlalchemy import create_engine

from oslo_api.application import DatabaseSliceOneApplication
from oslo_api.email import PostmarkInvitationMailer, SmtpInvitationMailer
from oslo_api.entitlements.repository import SqlEntitlementRepository
from oslo_api.entitlements.service import EntitlementService
from oslo_api.entitlements.stripe_gateway import StripeBillingGateway
from oslo_api.identity import SupabaseIdentityProvider
from oslo_api.settings import Settings


def build_slice_one_application() -> DatabaseSliceOneApplication:
    settings = Settings()  # type: ignore[call-arg]
    if settings.postmark_server_token:
        mailer = PostmarkInvitationMailer(
            server_token=settings.postmark_server_token.get_secret_value(),
            sender=settings.email_from,
            sender_name=settings.from_name,
        )
    else:
        mailer = SmtpInvitationMailer(
            host=settings.smtp_host,
            port=settings.smtp_port,
            sender=settings.email_sender,
        )
    return DatabaseSliceOneApplication(
        engine=create_engine(settings.database_url, pool_pre_ping=True),
        identity=SupabaseIdentityProvider(
            client=httpx.Client(timeout=10),
            supabase_url=settings.supabase_url,
            api_key=settings.supabase_secret_key,
        ),
        mailer=mailer,
        web_url=settings.web_url,
    )


def build_slice_four_application() -> EntitlementService:
    settings = Settings()  # type: ignore[call-arg]
    billing_configured = all(
        (
            settings.stripe_secret_key,
            settings.stripe_webhook_secret,
            settings.stripe_basic_monthly_price_id,
            settings.stripe_basic_annual_price_id,
        )
    )
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    web_url = settings.web_url.rstrip("/")
    return EntitlementService(
        repository=SqlEntitlementRepository(engine),
        billing_gateway=(
            StripeBillingGateway(
                secret_key=settings.stripe_secret_key.get_secret_value(),
                webhook_secret=settings.stripe_webhook_secret.get_secret_value(),
                monthly_price_id=settings.stripe_basic_monthly_price_id,
                annual_price_id=settings.stripe_basic_annual_price_id,
                success_url=(
                    f"{web_url}/settings?checkout=success"
                    "&session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=f"{web_url}/settings?checkout=cancelled",
            )
            if billing_configured
            and settings.stripe_secret_key is not None
            and settings.stripe_webhook_secret is not None
            and settings.stripe_basic_monthly_price_id is not None
            and settings.stripe_basic_annual_price_id is not None
            else None
        ),
    )

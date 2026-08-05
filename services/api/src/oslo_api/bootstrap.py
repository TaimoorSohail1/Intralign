import httpx
from sqlalchemy import create_engine

from oslo_api.application import DatabaseSliceOneApplication
from oslo_api.email import PostmarkInvitationMailer, SmtpInvitationMailer
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

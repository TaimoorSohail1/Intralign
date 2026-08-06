import json
from datetime import UTC, datetime

import httpx

from oslo_api.email import PostmarkInvitationMailer, PostmarkReportMailer


def recording_client(requests: list[httpx.Request]) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"ErrorCode": 0, "Message": "OK", "MessageID": "message-1"},
        )

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_postmark_invitation_uses_transactional_api_and_branded_sender() -> None:
    requests: list[httpx.Request] = []
    mailer = PostmarkInvitationMailer(
        server_token="server-token",
        sender="sender@example.com",
        sender_name="Oslo",
        client_factory=lambda: recording_client(requests),
    )

    mailer.send_invitation(
        email="new.member@example.com",
        workspace_name="OSLO Product Grill",
        role="Collaborator",
        activation_url="https://app.example.com/activate?token=secret",
        expires_at=datetime(2026, 8, 6, 9, 0, tzinfo=UTC),
    )

    request = requests[0]
    payload = json.loads(request.content)
    assert request.url == "https://api.postmarkapp.com/email"
    assert request.headers["X-Postmark-Server-Token"] == "server-token"
    assert payload["From"] == "Oslo <sender@example.com>"
    assert payload["To"] == "new.member@example.com"
    assert payload["Subject"] == "You're invited to OSLO Product Grill"
    assert "You've been invited" in payload["TextBody"]
    assert payload["MessageStream"] == "outbound"
    assert "Activate my account" in payload["HtmlBody"]
    assert "https://app.example.com/activate?token=secret" in payload["TextBody"]


def test_postmark_report_sends_the_saved_readout() -> None:
    requests: list[httpx.Request] = []
    mailer = PostmarkReportMailer(
        server_token="server-token",
        sender="sender@example.com",
        sender_name="Oslo",
        client_factory=lambda: recording_client(requests),
    )

    mailer.send_report(
        email="sponsor@example.com",
        subject="Project readout",
        project_name="Project North",
        recipient_label="Sponsor",
        sections=[{"title": "Summary", "body": ["The current read."]}],
    )

    payload = json.loads(requests[0].content)
    assert payload["Subject"] == "Project readout"
    assert payload["To"] == "sponsor@example.com"
    assert "Project North" in payload["HtmlBody"]
    assert "The current read." in payload["TextBody"]

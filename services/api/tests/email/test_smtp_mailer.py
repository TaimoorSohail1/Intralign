from datetime import UTC, datetime

from oslo_api.email import SmtpInvitationMailer


class RecordingSmtp:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.messages = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def send_message(self, message) -> None:
        self.messages.append(message)


def test_invitation_email_contains_workspace_expiry_and_activation_link() -> None:
    smtp_connections = []

    def smtp_factory(host: str, port: int) -> RecordingSmtp:
        connection = RecordingSmtp(host, port)
        smtp_connections.append(connection)
        return connection

    mailer = SmtpInvitationMailer(
        host="mail.local",
        port=2525,
        sender="OSLO <no-reply@oslo.local>",
        smtp_factory=smtp_factory,
    )

    mailer.send_invitation(
        email="new.member@example.com",
        workspace_name="OSLO Product Grill",
        role="Collaborator",
        activation_url="http://localhost:3000/activate?token=secret",
        expires_at=datetime(2026, 7, 27, 9, 0, tzinfo=UTC),
    )

    connection = smtp_connections[0]
    message = connection.messages[0]
    body = message.get_body(preferencelist=("plain",)).get_content()
    assert (connection.host, connection.port) == ("mail.local", 2525)
    assert message["To"] == "new.member@example.com"
    assert message["Subject"] == "You’re invited to OSLO Product Grill"
    assert "http://localhost:3000/activate?token=secret" in body
    assert "27 July 2026" in body
    assert "Collaborator" in body


def test_invitation_email_has_branded_responsive_html_and_fallback_link() -> None:
    smtp_connections = []

    def smtp_factory(host: str, port: int) -> RecordingSmtp:
        connection = RecordingSmtp(host, port)
        smtp_connections.append(connection)
        return connection

    mailer = SmtpInvitationMailer(
        host="mail.local",
        port=2525,
        sender="OSLO <no-reply@oslo.local>",
        smtp_factory=smtp_factory,
    )
    activation_url = "http://localhost:3000/activate?token=secret&source=email"

    mailer.send_invitation(
        email="new.member@example.com",
        workspace_name="OSLO Product Grill",
        role="Collaborator",
        activation_url=activation_url,
        expires_at=datetime(2026, 7, 27, 9, 0, tzinfo=UTC),
    )

    message = smtp_connections[0].messages[0]
    html = message.get_body(preferencelist=("html",)).get_content()
    assert '<meta name="viewport" content="width=device-width, initial-scale=1.0">' in html
    assert 'role="presentation"' in html
    assert "OSLO" in html
    assert "Activate my account" in html
    assert "This secure invitation expires on 27 July 2026" in html
    assert "Collaborator" in html
    assert activation_url.replace("&", "&amp;") in html
    assert "If the button doesn&rsquo;t work" in html

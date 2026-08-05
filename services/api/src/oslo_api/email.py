# ruff: noqa: E501

import smtplib
from collections.abc import Callable
from datetime import datetime
from email.message import EmailMessage
from html import escape
from typing import Any

import httpx

POSTMARK_EMAIL_URL = "https://api.postmarkapp.com/email"


def _sender_address(sender: str, sender_name: str) -> str:
    return f"{sender_name} <{sender}>" if sender_name.strip() else sender


def _postmark_send(
    *,
    server_token: str,
    sender: str,
    sender_name: str,
    recipient: str,
    subject: str,
    text_body: str,
    html_body: str,
    client_factory: Callable[[], httpx.Client],
) -> None:
    with client_factory() as client:
        response = client.post(
            POSTMARK_EMAIL_URL,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Postmark-Server-Token": server_token,
            },
            json={
                "From": _sender_address(sender, sender_name),
                "To": recipient,
                "Subject": subject,
                "TextBody": text_body,
                "HtmlBody": html_body,
                "MessageStream": "outbound",
            },
        )
        response.raise_for_status()
        result = response.json()
        if result.get("ErrorCode") != 0:
            raise RuntimeError(f"Postmark rejected the email: {result.get('Message', 'unknown error')}")


def _invitation_html(*, workspace_name: str, role: str, activation_url: str, expiry: str) -> str:
    safe_workspace_name = escape(workspace_name)
    safe_role = escape(role)
    safe_activation_url = escape(activation_url)
    safe_expiry = escape(expiry)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <title>You&rsquo;re invited to {safe_workspace_name}</title>
  <style>
    @media only screen and (max-width: 620px) {{
      .email-shell {{ width: 100% !important; }}
      .email-card {{ padding: 32px 24px !important; }}
      .email-title {{ font-size: 30px !important; line-height: 36px !important; }}
      .email-button {{ display: block !important; text-align: center !important; }}
    }}
  </style>
</head>
<body style="margin:0; padding:0; background-color:#0f1113; color:#f7f7f3; font-family:Arial, Helvetica, sans-serif;">
  <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:transparent;">
    Your secure invitation to join {safe_workspace_name} is ready.
  </div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; background-color:#0f1113;">
    <tr>
      <td align="center" style="padding:40px 16px;">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" class="email-shell" style="width:600px; max-width:600px;">
          <tr>
            <td style="padding:0 0 20px 4px;">
              <span style="font-size:19px; font-weight:800; letter-spacing:3px; color:#ffffff;">OSLO</span>
              <span style="font-size:11px; font-weight:700; letter-spacing:1.5px; color:#e98a45; padding-left:10px;">PRODUCT GRILL</span>
            </td>
          </tr>
          <tr>
            <td class="email-card" style="padding:48px; background-color:#191d21; border:1px solid #353b42; border-radius:16px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <td>
                    <div style="font-size:12px; line-height:18px; font-weight:800; letter-spacing:1.5px; color:#e98a45; text-transform:uppercase;">Workspace invitation</div>
                    <h1 class="email-title" style="margin:14px 0 18px; font-size:38px; line-height:44px; letter-spacing:-1px; color:#ffffff;">You&rsquo;re invited.</h1>
                    <p style="margin:0; font-size:17px; line-height:28px; color:#c9ced6;">You&rsquo;ve been invited to join <strong style="color:#ffffff;">{safe_workspace_name}</strong> as <strong style="color:#ffffff;">{safe_role}</strong>. Activate your account to enter the workspace and start working with your team.</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:32px 0 30px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                      <tr>
                        <td bgcolor="#e98a45" style="border-radius:8px;">
                          <a href="{safe_activation_url}" class="email-button" style="display:inline-block; padding:15px 24px; border:1px solid #e98a45; border-radius:8px; background-color:#e98a45; color:#111315; font-size:16px; line-height:20px; font-weight:800; text-decoration:none;">Activate my account&nbsp;&rarr;</a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td style="padding:18px 20px; background-color:#22272d; border:1px solid #353b42; border-radius:10px;">
                    <p style="margin:0; font-size:14px; line-height:22px; color:#d7dbe0;"><strong style="color:#ffffff;">Time-sensitive link</strong><br>This secure invitation expires on {safe_expiry}.</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding-top:28px;">
                    <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#9299a3;">If the button doesn&rsquo;t work, copy and paste this link into your browser:</p>
                    <p style="margin:0; font-size:12px; line-height:18px; word-break:break-all;"><a href="{safe_activation_url}" style="color:#e98a45; text-decoration:underline;">{safe_activation_url}</a></p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:22px 12px 0; text-align:center;">
              <p style="margin:0 0 6px; font-size:12px; line-height:18px; color:#7f8791;">If you weren&rsquo;t expecting this invitation, you can safely ignore this email.</p>
              <p style="margin:0; font-size:12px; line-height:18px; color:#626a74;">OSLO Product Grill &middot; Evidence-led product decisions</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


class SmtpInvitationMailer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        sender: str,
        smtp_factory: Callable[[str, int], Any] = smtplib.SMTP,
    ) -> None:
        self._host = host
        self._port = port
        self._sender = sender
        self._smtp_factory = smtp_factory

    def send_invitation(
        self,
        *,
        email: str,
        workspace_name: str,
        role: str,
        activation_url: str,
        expires_at: datetime,
    ) -> None:
        expiry = expires_at.strftime("%d %B %Y")
        message = EmailMessage()
        message["From"] = self._sender
        message["To"] = email
        message["Subject"] = f"You’re invited to {workspace_name}"
        message.set_content(
            f"""You’ve been invited to join {workspace_name} as {role} in OSLO Product Grill.

Activate your account:
{activation_url}

This invitation expires on {expiry}.
"""
        )
        message.add_alternative(
            _invitation_html(
                workspace_name=workspace_name,
                role=role,
                activation_url=activation_url,
                expiry=expiry,
            ),
            subtype="html",
        )
        with self._smtp_factory(self._host, self._port) as smtp:
            smtp.send_message(message)


class SmtpReportMailer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        sender: str,
        smtp_factory: Callable[[str, int], Any] = smtplib.SMTP,
    ) -> None:
        self._host = host
        self._port = port
        self._sender = sender
        self._smtp_factory = smtp_factory

    def send_report(
        self,
        *,
        email: str,
        subject: str,
        project_name: str,
        recipient_label: str,
        sections: list[dict],
    ) -> None:
        message = EmailMessage()
        message["From"] = self._sender
        message["To"] = email
        message["Subject"] = subject
        plain_lines = [project_name, f"Prepared for {recipient_label}", ""]
        html_sections: list[str] = []
        for section in sections:
            title = str(section.get("title") or "Section")
            paragraphs = [
                str(item).strip()
                for item in section.get("body", [])
                if str(item).strip()
            ]
            plain_lines.extend([title, *paragraphs, ""])
            html_sections.append(
                f"<h2>{escape(title)}</h2>"
                + "".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
            )
        message.set_content("\n".join(plain_lines))
        message.add_alternative(
            (
                '<!doctype html><html lang="en"><body style="font-family:Arial,sans-serif;'
                'max-width:720px;margin:auto;color:#17191c">'
                f"<h1>{escape(project_name)}</h1>"
                f"<p>Prepared for {escape(recipient_label)}</p>"
                + "".join(html_sections)
                + "<hr><p>Sent from Intralign.</p></body></html>"
            ),
            subtype="html",
        )
        with self._smtp_factory(self._host, self._port) as smtp:
            smtp.send_message(message)


class PostmarkInvitationMailer:
    def __init__(
        self,
        *,
        server_token: str,
        sender: str,
        sender_name: str,
        client_factory: Callable[[], httpx.Client] = lambda: httpx.Client(timeout=15),
    ) -> None:
        self._server_token = server_token
        self._sender = sender
        self._sender_name = sender_name
        self._client_factory = client_factory

    def send_invitation(
        self,
        *,
        email: str,
        workspace_name: str,
        role: str,
        activation_url: str,
        expires_at: datetime,
    ) -> None:
        expiry = expires_at.strftime("%d %B %Y")
        text_body = f"""Youâ€™ve been invited to join {workspace_name} as {role} in OSLO Product Grill.

Activate your account:
{activation_url}

This invitation expires on {expiry}.
"""
        _postmark_send(
            server_token=self._server_token,
            sender=self._sender,
            sender_name=self._sender_name,
            recipient=email,
            subject=f"Youâ€™re invited to {workspace_name}",
            text_body=text_body,
            html_body=_invitation_html(
                workspace_name=workspace_name,
                role=role,
                activation_url=activation_url,
                expiry=expiry,
            ),
            client_factory=self._client_factory,
        )


class PostmarkReportMailer:
    def __init__(
        self,
        *,
        server_token: str,
        sender: str,
        sender_name: str,
        client_factory: Callable[[], httpx.Client] = lambda: httpx.Client(timeout=15),
    ) -> None:
        self._server_token = server_token
        self._sender = sender
        self._sender_name = sender_name
        self._client_factory = client_factory

    def send_report(
        self,
        *,
        email: str,
        subject: str,
        project_name: str,
        recipient_label: str,
        sections: list[dict],
    ) -> None:
        plain_lines = [project_name, f"Prepared for {recipient_label}", ""]
        html_sections: list[str] = []
        for section in sections:
            title = str(section.get("title") or "Section")
            paragraphs = [
                str(item).strip()
                for item in section.get("body", [])
                if str(item).strip()
            ]
            plain_lines.extend([title, *paragraphs, ""])
            html_sections.append(
                f"<h2>{escape(title)}</h2>"
                + "".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
            )
        html_body = (
            '<!doctype html><html lang="en"><body style="font-family:Arial,sans-serif;'
            'max-width:720px;margin:auto;color:#17191c">'
            f"<h1>{escape(project_name)}</h1>"
            f"<p>Prepared for {escape(recipient_label)}</p>"
            + "".join(html_sections)
            + "<hr><p>Sent from Intralign.</p></body></html>"
        )
        _postmark_send(
            server_token=self._server_token,
            sender=self._sender,
            sender_name=self._sender_name,
            recipient=email,
            subject=subject,
            text_body="\n".join(plain_lines),
            html_body=html_body,
            client_factory=self._client_factory,
        )

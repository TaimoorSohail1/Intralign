"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button, Dialog, TextAreaField } from "@/components/design-system";

export function InviteMemberForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [activationUrl, setActivationUrl] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [sending, setSending] = useState(false);
  const [copied, setCopied] = useState(false);

  async function sendInvitation(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const invitedEmail = email.trim().toLowerCase();
    if (!invitedEmail) return;
    setSending(true);
    setError("");
    setNotice("");
    setActivationUrl("");
    setCopied(false);
    try {
      const response = await fetch("/api/workspace/invitations", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ action: "invite", email: invitedEmail }),
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(payload?.message ?? "The invitation could not be sent.");
      setNotice(
        payload?.delivery_status === "unavailable"
          ? "Invitation created, but email delivery is unavailable. Copy the link to share it manually."
          : `Invitation sent to ${invitedEmail}.`,
      );
      setActivationUrl(typeof payload?.activation_url === "string" ? payload.activation_url : "");
      setEmail("");
      // Refresh the server-rendered invitation list while retaining this
      // client component's one-time link state for the dialog.
      router.refresh();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "The invitation could not be sent.");
    } finally {
      setSending(false);
    }
  }

  async function copyInvitationUrl() {
    try {
      await navigator.clipboard.writeText(activationUrl);
      setCopied(true);
      setNotice("Invitation link copied to the clipboard.");
    } catch {
      setError("The invitation link could not be copied. Use the invitation email instead.");
    }
  }

  return (
    <>
      {notice ? <p className="success-notice" role="status">{notice}</p> : null}
      {error ? <p className="form-error" role="alert">{error}</p> : null}
      <form className="invite-form" onSubmit={sendInvitation}>
        <div className="field"><label htmlFor="invite-email">Email address</label><input id="invite-email" name="email" onChange={(event) => setEmail(event.target.value)} required type="email" value={email} /></div>
        <Button disabled={sending} type="submit">{sending ? "Sending…" : "Send invitation →"}</Button>
      </form>
      <Dialog
        actions={(
          <>
            <Button onClick={() => void copyInvitationUrl()} type="button">{copied ? "Copied" : "Copy link"}</Button>
            <Button onClick={() => setActivationUrl("")} type="button" variant="ghost">Done</Button>
          </>
        )}
        description="Recommended only if the invitation email has not arrived. This secure link is shown once."
        onClose={() => setActivationUrl("")}
        open={Boolean(activationUrl)}
        title="Invitation link"
      >
        <TextAreaField
          id="invitation-link"
          label="Secure link"
          readOnly
          rows={2}
          spellCheck={false}
          value={activationUrl}
        />
      </Dialog>
    </>
  );
}

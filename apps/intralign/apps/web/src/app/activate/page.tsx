import Link from "next/link";

import { ActivationForm } from "@/components/auth/activation-form";
import { EntryShell } from "@/components/layout/entry-shell";
import { resolveInvitation } from "@/lib/server/oslo-api";

import { activateAccount } from "./actions";

interface ActivatePageProps {
  searchParams: Promise<{ token?: string }>;
}

export default async function ActivatePage({ searchParams }: ActivatePageProps) {
  const { token } = await searchParams;
  if (!token) {
    return (
      <EntryShell><section className="activation-card error-card"><h1>Invitation link required</h1><p>Open the unique link from your OSLO invitation email.</p></section></EntryShell>
    );
  }
  const invitation = await resolveInvitation(token).catch(() => null);
  if (!invitation) {
    return (
      <EntryShell><section className="activation-card error-card"><p className="eyebrow">Invitation unavailable</p><h1>This link can’t be used</h1><p>It may have expired, been revoked, or already been accepted. Ask your workspace Owner for a new invitation.</p></section></EntryShell>
    );
  }
  return (
    <EntryShell>
      {invitation.account_exists ? (
        <section className="activation-card">
          <p className="eyebrow">Existing OSLO account</p>
          <h1>Sign in to accept your invitation</h1>
          <p className="activation-subtitle">{invitation.email} already has an account. Sign in with that email to join {invitation.workspace_name}.</p>
          <Link className="button button-primary button-full" href={`/login?invite=${encodeURIComponent(token)}`}>Sign in &amp; continue <span aria-hidden="true">→</span></Link>
        </section>
      ) : (
        <ActivationForm action={activateAccount} email={invitation.email} token={token} workspaceName={invitation.workspace_name} />
      )}
    </EntryShell>
  );
}

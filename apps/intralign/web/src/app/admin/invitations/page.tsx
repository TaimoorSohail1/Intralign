import { redirect } from "next/navigation";

import { BrandLockup } from "@/components/brand/brand-lockup";
import { Button } from "@/components/design-system";
import { listInvitations, OsloApiError, type InvitationSummary } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";
import { logout } from "@/app/logout-action";

import { resendMemberInvitation, revokeMemberInvitation } from "./actions";
import { InviteMemberForm } from "./invite-member-form";

interface InvitationsPageProps {
  searchParams: Promise<{
    sent?: string;
    updated?: string;
    error?: string;
  }>;
}

export default async function InvitationsPage({ searchParams }: InvitationsPageProps) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  if (!session.workspaceId) redirect("/login");
  if (session.accountRole !== "admin") redirect("/workspace");
  const { sent, updated, error: requestError } = await searchParams;
  let invitations: InvitationSummary[] = [];
  let invitationServiceError = "";
  try {
    invitations = await listInvitations({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    });
  } catch (error) {
    if (error instanceof OsloApiError && error.status === 403) {
      redirect("/settings?access=owner-required");
    }
    invitationServiceError = "Invitations are temporarily unavailable. Check the local backend configuration and try again.";
  }
  return (
    <main className="admin-shell">
      <header className="admin-header"><BrandLockup /><div><span className="role-badge">Admin</span><span>{session.displayName}</span><form action={logout}><Button variant="ghost" type="submit">Log out</Button></form></div></header>
      <section className="admin-content">
        <p className="eyebrow">Workspace access</p><h1>Invitations</h1>
        <p className="admin-copy">Invite trusted teammates into OSLO. Every link is unique and expires after 14 days.</p>
        {sent ? <p className="success-notice">Invitation sent to {sent}. It is pending acceptance by the recipient.</p> : null}
        {updated ? <p className="success-notice">Invitation {updated}.</p> : null}
        {requestError ? <p className="form-error" id="invite-error" role="alert">{requestError}</p> : null}
        {invitationServiceError ? <p className="form-error" role="alert">{invitationServiceError}</p> : null}
        <InviteMemberForm />
        <section className="invitation-table">
          <h2>Workspace invitations</h2>
          {invitations.length === 0 ? <p className="table-empty">No invitations yet.</p> : invitations.map((invitation) => (
            <article className="invitation-row" key={invitation.id}>
              <div><strong>{invitation.email}</strong><span>Owner invitation · expires {new Date(invitation.expires_at).toLocaleDateString("en-GB")}</span></div>
              <span className={`status-badge status-${invitation.status}`}>
                {invitation.status === "pending" ? "sent · pending acceptance" : invitation.status}
              </span>
              {invitation.status === "pending" ? <div className="row-actions">
                <form action={resendMemberInvitation}><input name="invitation_id" type="hidden" value={invitation.id} /><Button variant="ghost" type="submit">Resend</Button></form>
                <form action={revokeMemberInvitation}><input name="invitation_id" type="hidden" value={invitation.id} /><Button variant="danger" type="submit">Revoke</Button></form>
              </div> : null}
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}

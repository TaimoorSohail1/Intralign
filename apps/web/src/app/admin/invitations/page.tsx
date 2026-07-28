import { redirect } from "next/navigation";

import { BrandLockup } from "@/components/brand/brand-lockup";
import { listInvitations, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";
import { logout } from "@/app/logout-action";

import { inviteMember, resendMemberInvitation, revokeMemberInvitation } from "./actions";

interface InvitationsPageProps {
  searchParams: Promise<{
    sent?: string;
    updated?: string;
    error?: string;
    email?: string;
  }>;
}

export default async function InvitationsPage({ searchParams }: InvitationsPageProps) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  if (!session.workspaceId) redirect("/login");
  const { sent, updated, error, email } = await searchParams;
  let invitations;
  try {
    invitations = await listInvitations({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    });
  } catch (error) {
    if (error instanceof OsloApiError && error.status === 403) {
      redirect("/settings?access=owner-required");
    }
    throw error;
  }
  return (
    <main className="admin-shell">
      <header className="admin-header"><BrandLockup /><div><span className="role-badge">Owner</span><span>{session.displayName}</span><form action={logout}><button className="button button-ghost" type="submit">Log out</button></form></div></header>
      <section className="admin-content">
        <p className="eyebrow">Workspace access</p><h1>Invitations</h1>
        <p className="admin-copy">Invite trusted teammates into the OSLO Alpha. Every link is unique and expires after seven days.</p>
        {sent ? <p className="success-notice">Invitation sent to {sent}. Open Mailpit locally to view it.</p> : null}
        {updated ? <p className="success-notice">Invitation {updated}.</p> : null}
        {error ? <p className="form-error" id="invite-error" role="alert">{error}</p> : null}
        <form action={inviteMember} className="invite-form">
          <div className="field"><label htmlFor="invite-email">Email address</label><input aria-describedby={error ? "invite-error" : undefined} defaultValue={email} id="invite-email" name="email" required type="email" /></div>
          <div className="field"><label htmlFor="invite-role">Role</label><select defaultValue="collaborator" id="invite-role" name="role"><option value="owner">Owner</option><option value="collaborator">Collaborator</option><option value="viewer">Viewer</option></select></div>
          <button className="button button-primary" type="submit">Send invitation →</button>
        </form>
        <section className="invitation-table">
          <h2>Workspace invitations</h2>
          {invitations.length === 0 ? <p className="table-empty">No invitations yet.</p> : invitations.map((invitation) => (
            <article className="invitation-row" key={invitation.id}>
              <div><strong>{invitation.email}</strong><span>{invitation.role} · expires {new Date(invitation.expires_at).toLocaleDateString("en-GB")}</span></div>
              <span className={`status-badge status-${invitation.status}`}>{invitation.status}</span>
              {invitation.status === "pending" ? <div className="row-actions">
                <form action={resendMemberInvitation}><input name="invitation_id" type="hidden" value={invitation.id} /><button className="button button-ghost" type="submit">Resend</button></form>
                <form action={revokeMemberInvitation}><input name="invitation_id" type="hidden" value={invitation.id} /><button className="button button-ghost danger-button" type="submit">Revoke</button></form>
              </div> : null}
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}

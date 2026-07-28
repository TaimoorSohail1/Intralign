import { EntryShell } from "@/components/layout/entry-shell";
import { resolveInvitation } from "@/lib/server/oslo-api";

import { signIn } from "./actions";

interface LoginPageProps {
  searchParams: Promise<{ invite?: string }>;
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const { invite } = await searchParams;
  const invitation = invite ? await resolveInvitation(invite).catch(() => null) : null;
  const showDevelopmentCredentials =
    process.env.NODE_ENV === "development" &&
    process.env.OSLO_SHOW_DEV_CREDENTIALS === "true" &&
    !invitation;
  const localAdminEmail = showDevelopmentCredentials
    ? "admin@oslo.local"
    : undefined;
  const localAdminPassword = showDevelopmentCredentials
    ? "OsloLocalAdmin123!"
    : undefined;
  return (
    <EntryShell>
      <form action={signIn} className="activation-card">
        <p className="eyebrow">Invite-only Alpha</p>
        <h1>Sign in to OSLO</h1>
        <p className="activation-subtitle">{invitation ? `Sign in to join ${invitation.workspace_name}.` : "Use the email and password connected to your invited account."}</p>
        {invite ? <input name="invitation_token" type="hidden" value={invite} /> : null}
        <div className="field"><label htmlFor="email">Email</label><input autoComplete="email" defaultValue={invitation?.email ?? localAdminEmail} id="email" name="email" readOnly={Boolean(invitation)} required type="email" /></div>
        <div className="field"><label htmlFor="password">Password</label><input autoComplete="current-password" defaultValue={localAdminPassword} id="password" name="password" required type="password" /></div>
        <label className="stay-signed-in"><input defaultChecked name="stay_signed_in" type="checkbox" value="true" /><span>Stay signed in on this device</span></label>
        <button className="button button-primary button-full" type="submit">Sign in <span aria-hidden="true">→</span></button>
      </form>
    </EntryShell>
  );
}

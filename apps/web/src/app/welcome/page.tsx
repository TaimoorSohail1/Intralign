import { redirect } from "next/navigation";

import { EntryShell } from "@/components/layout/entry-shell";
import { readSession } from "@/lib/server/session";

import { startFirstProject } from "./actions";

export default async function WelcomePage() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  return (
    <EntryShell>
      <section className="welcome-card">
        <div className="welcome-check" aria-hidden="true">✓</div>
        <h1>Welcome to OSLO, {session.displayName ?? "there"}.</h1>
        <p>Your Alpha account is active. Bring in a plan and OSLO will give you the strategic read your task tracker can’t. You stay in control at every step.</p>
        <form action={startFirstProject}><button className="button button-primary" type="submit">Start your first project <span aria-hidden="true">→</span></button></form>
      </section>
    </EntryShell>
  );
}

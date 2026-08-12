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
        <h1>Welcome to Intralign, {session.displayName ?? "there"}.</h1>
        <p>
          Your Alpha account is active. Intralign runs on <strong>OSLO</strong> — Outcome-driven
          Strategic Lifecycle Orchestration — the AI that drives your outcome across the whole
          lifecycle, planning included. Bring in a plan and OSLO shows you what stands between it
          and that outcome — the read your task tracker, schedule, or spreadsheet can’t give you.
          You stay in control at every step.
        </p>
        <form action={startFirstProject}>
          <button className="button button-primary" type="submit">
            Start your first outcome <span aria-hidden="true">→</span>
          </button>
        </form>
      </section>
    </EntryShell>
  );
}

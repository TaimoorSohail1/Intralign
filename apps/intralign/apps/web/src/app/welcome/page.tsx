import { redirect } from "next/navigation";

import { EntryShell } from "@/components/layout/entry-shell";
import { readSession } from "@/lib/server/session";

import { startFirstProject } from "./actions";
import { WelcomeSubmitButton } from "./welcome-submit";

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
          <WelcomeSubmitButton />
        </form>
      </section>
    </EntryShell>
  );
}

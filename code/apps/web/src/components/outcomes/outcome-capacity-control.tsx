"use client";

import { Archive, ArrowCounterClockwise, Plus, Target, X } from "@phosphor-icons/react";
import { FormEvent, useState } from "react";

import type { ProjectOutcomeSummary } from "@/lib/server/oslo-api";

const gateOptions = ["archive_to_switch", "upgrade_basic", "not_now"];

export function OutcomeCapacityControl({
  projectId,
  onOutcomesChange,
}: {
  projectId: string;
  onOutcomesChange?: (outcomes: ProjectOutcomeSummary[]) => void;
}) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [pendingId, setPendingId] = useState<string | null>(null);
  const [outcomes, setOutcomes] = useState<ProjectOutcomeSummary[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [gate, setGate] = useState(false);

  const openDialog = async () => {
    setOpen(true);
    setLoading(true);
    setError(null);
    const response = await fetch(`/api/projects/${projectId}/outcomes`, {
      cache: "no-store",
    });
    const payload = await response.json().catch(() => null);
    if (response.ok && Array.isArray(payload)) {
      setOutcomes(payload);
      onOutcomesChange?.(payload);
    } else {
      setError(payload?.message ?? "Outcomes could not be loaded.");
    }
    setLoading(false);
  };

  const addOutcome = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!title.trim() || pendingId) return;
    setPendingId("new");
    setError(null);
    const response = await fetch(`/api/projects/${projectId}/outcomes`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ title: title.trim() }),
    });
    const payload = await response.json().catch(() => null);
    if (response.ok) {
      setOutcomes((current) => {
        const next = [...current, payload as ProjectOutcomeSummary];
        onOutcomesChange?.(next);
        return next;
      });
      setTitle("");
    } else if (response.status === 422) {
      setGate(true);
      setError(null);
    } else {
      setError(payload?.message ?? "The Outcome could not be added.");
    }
    setPendingId(null);
  };

  const changeStatus = async (outcome: ProjectOutcomeSummary) => {
    const action = outcome.status === "active" ? "archive" : "reactivate";
    setPendingId(outcome.id);
    setError(null);
    if (action === "archive" && gate) {
      await fetch("/api/workspace/intent-signals", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          wall_key: "multiOutcome",
          chosen_path: "free_path",
          full_option_set: gateOptions,
          context: { project_id: projectId, outcome_id: outcome.id },
        }),
      }).catch(() => null);
    }
    const response = await fetch(`/api/outcomes/${outcome.id}/${action}`, {
      method: "POST",
    });
    const payload = await response.json().catch(() => null);
    if (response.ok) {
      setOutcomes((current) => {
        const next = current.map((item) =>
          item.id === outcome.id ? payload as ProjectOutcomeSummary : item,
        );
        onOutcomesChange?.(next);
        return next;
      });
      setGate(false);
    } else {
      if (response.status === 422) setGate(true);
      setError(payload?.message ?? "The Outcome could not be updated.");
    }
    setPendingId(null);
  };

  const startCheckout = async () => {
    setPendingId("checkout");
    const response = await fetch("/api/workspace/billing/checkout", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ interval: "monthly", wall_key: "multiOutcome" }),
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      setError(payload?.message ?? "Secure checkout could not be started.");
      setPendingId(null);
      return;
    }
    try {
      const destination = new URL(payload.url);
      if (destination.protocol !== "https:" || destination.hostname !== "checkout.stripe.com") {
        throw new Error("INVALID_CHECKOUT_URL");
      }
      window.location.assign(destination.toString());
    } catch {
      setError("Secure checkout returned an invalid destination.");
      setPendingId(null);
    }
  };

  const declineGate = async () => {
    setGate(false);
    await fetch("/api/workspace/intent-signals", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        wall_key: "multiOutcome",
        chosen_path: "declined",
        full_option_set: gateOptions,
        context: { project_id: projectId },
      }),
    }).catch(() => null);
  };

  const chooseArchivePath = async () => {
    setGate(false);
    await fetch("/api/workspace/intent-signals", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        wall_key: "multiOutcome",
        chosen_path: "free_path",
        full_option_set: gateOptions,
        context: { project_id: projectId },
      }),
    }).catch(() => null);
  };

  return (
    <>
      <button aria-label="Manage Outcomes" className="outcome-manage-trigger" onClick={() => void openDialog()} type="button">
        <Target aria-hidden="true" size={15} weight="bold" />
        <span role="tooltip">Manage Outcomes</span>
      </button>
      {open ? (
        <div className="outcome-dialog-backdrop">
          <section aria-labelledby="outcome-dialog-title" aria-modal="true" className="outcome-dialog" role="dialog">
            <header>
              <div><h2 id="outcome-dialog-title">Outcomes</h2><p>Archive is reversible. The record always stays viewable.</p></div>
              <button aria-label="Close Outcomes" onClick={() => setOpen(false)} type="button"><X size={18} /></button>
            </header>
            {loading ? <p role="status">Loading Outcomes…</p> : null}
            {!loading ? (
              <div className="outcome-list">
                {outcomes.map((outcome) => (
                  <article key={outcome.id}>
                    <div>
                      <strong>{outcome.title}</strong>
                      <span>{outcome.status === "archived" ? "Archived · record remains viewable" : outcome.provenance === "declared" ? "Active · declared" : "Active · OSLO inference"}</span>
                    </div>
                    <button
                      aria-label={`${outcome.status === "active" ? "Archive" : "Reactivate"} ${outcome.title}`}
                      disabled={pendingId === outcome.id}
                      onClick={() => void changeStatus(outcome)}
                      type="button"
                    >
                      {outcome.status === "active" ? <Archive size={15} /> : <ArrowCounterClockwise size={15} />}
                      {outcome.status === "active" ? "Archive" : "Reactivate"}
                    </button>
                  </article>
                ))}
              </div>
            ) : null}
            <form onSubmit={addOutcome}>
              <label htmlFor="new-outcome">New Outcome</label>
              <div><input id="new-outcome" maxLength={240} onChange={(event) => setTitle(event.target.value)} value={title} /><button disabled={!title.trim() || pendingId !== null} type="submit"><Plus size={14} /> Add Outcome</button></div>
            </form>
            {gate ? (
              <aside className="outcome-capacity-gate">
                <strong>Optimize all your outcomes</strong>
                <span>Basic · $29/month</span>
                <p>Keep both through secure checkout, or archive an active Outcome to stay on Free.</p>
                <div>
                  <button disabled={pendingId !== null} onClick={() => void startCheckout()} type="button">Keep both with Basic</button>
                  <button onClick={() => void chooseArchivePath()} type="button">Archive an Outcome instead</button>
                  <button onClick={() => void declineGate()} type="button">Not now</button>
                </div>
              </aside>
            ) : null}
            {error ? <p className="form-error" role="alert">{error}</p> : null}
          </section>
        </div>
      ) : null}
    </>
  );
}

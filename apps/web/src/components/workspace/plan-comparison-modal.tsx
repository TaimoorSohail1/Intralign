"use client";

import { Check, X } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

const plans = {
  free: {
    label: "Free",
    price: "$0",
    tagline: "The whole read, on one plan.",
    features: [
      "Your plan, in",
      "Initial analysis and orientation (never queued)",
      "Overview, confidence and reliability",
      "Attention map",
      "Issues, recommendations and the clarification loop",
      "OSLO chat — uncapped",
      "Every recommendation, in full · editing by hand is free",
      "Share for review — the answer lands as evidence",
      "Review requests — unlimited",
      "Comments and sharing",
      "A shareable readout — PDF",
      "Documents — unlimited · History — full, forever",
      "Link revocation and purpose-scoped expiry",
      "1 active project",
      "Reads ~20 documents / ~50k words",
      "Analyses a month — generous",
      "‘Update now’ — free · slow auto-refresh",
      "3 owner seats (including you)",
      "2 invites / month",
      "Export — PDF",
    ],
  },
  basic: {
    label: "Basic",
    price: "$12",
    tagline: "More plans, bigger plans, less to redo.",
    features: [
      "Everything in Free",
      "3 active projects",
      "Reads ~40 documents / ~100k words — twice the Free envelope",
      "Connected sources — Jira · Confluence",
      "The readout, kept — your wording, week to week",
      "Extra readout sections · branding · scheduling",
      "Export / sync → your execution tool",
      "OSLO applies fixes freely · ‘Apply all’",
      "Continuous auto-refresh",
      "Analyses a month — a larger budget",
      "Documents · History · chat · review requests — identical to Free",
      "10 owner seats",
      "Overage — against a spend cap you set",
      "Export — PDF · Copy summary · Export link",
    ],
  },
} as const;

const futurePlans = [
  {
    label: "Pro",
    price: "~$39 / month",
    tagline: "OSLO starts following the work.",
    features: [
      "Execution and programme support — continuous monitoring",
      "Programme-level view across your plans",
      "10 active projects · reads ~80 documents / ~200k words",
      "Documents · History · Chat · review requests — as Free",
    ],
  },
  {
    label: "Team",
    price: "~$99–149 / seat / month",
    tagline: "Collaboration becomes the product.",
    features: [
      "Shared plans, shared issues, shared decisions",
      "Governance — policies, roles, review workflow",
      "Reads ~150 documents / ~400k words · a per-seat budget",
      "Review requests remain free",
    ],
  },
  {
    label: "Enterprise",
    price: "custom / contract",
    tagline: "Portfolio and organisational governance.",
    features: [
      "Portfolio — many programmes, one read",
      "Organisational governance — policy, audit, capacity",
      "The record, evidence loop and safety defaults — as Free",
    ],
  },
] as const;

export function PlanComparisonModal({
  open,
  workspace,
  onClose,
  onWorkspaceChange,
}: {
  open: boolean;
  workspace: WorkspaceSummary;
  onClose: () => void;
  onWorkspaceChange: (workspace: WorkspaceSummary) => void;
}) {
  const [pending, setPending] = useState<WorkspaceSummary["plan"] | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [onClose, open]);

  if (!open) return null;

  const selectPlan = async (plan: WorkspaceSummary["plan"]) => {
    if (plan === workspace.plan || pending) return;
    setPending(plan);
    setMessage(null);
    const response = await fetch("/api/workspace/plan", {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ plan }),
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      setMessage(payload?.message ?? "The plan could not be updated.");
      setPending(null);
      return;
    }
    onWorkspaceChange(payload as WorkspaceSummary);
    setMessage(
      plan === "basic"
        ? "Basic is now active in this preview. No card was charged."
        : "Free is now active. Everything you already understood is retained.",
    );
    setPending(null);
  };

  return (
    <div className="plan-modal-backdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <section aria-labelledby="plan-modal-title" aria-modal="true" className="plan-modal" role="dialog">
        <header>
          <div>
            <h2 id="plan-modal-title">Your plan</h2>
            <span>What each plan includes.</span>
          </div>
          <button aria-label="Close plans" onClick={onClose} type="button"><X size={19} /></button>
        </header>

        <div className="plan-modal-body">
          <div className="plan-equality-note">
            <strong>Every plan gets the same read.</strong>
            <span>Plans differ on capacity, scope and collaboration.</span>
          </div>

          <div className="plan-card-grid">
            {(Object.entries(plans) as Array<[WorkspaceSummary["plan"], typeof plans.free | typeof plans.basic]>).map(([code, plan]) => {
              const current = workspace.plan === code;
              return (
                <article className={`plan-card ${current ? "is-current" : ""}`} key={code}>
                  <div className="plan-card-heading">
                    <h3>{plan.label}</h3>
                    {current ? <span>Your plan</span> : null}
                  </div>
                  <p className="plan-price"><strong>{plan.price}</strong>{code === "basic" ? <span> / month</span> : null}</p>
                  <p className="plan-tagline">{plan.tagline}</p>
                  <ul>{plan.features.map((feature, index) => <li className={index < (code === "free" ? 14 : 1) ? "is-core" : ""} key={feature}>{index < (code === "free" ? 14 : 1) ? <Check size={13} weight="bold" /> : <span>·</span>}<span>{feature}</span></li>)}</ul>
                  <button
                    className={current ? "plan-current-button" : "plan-select-button"}
                    disabled={current || pending !== null || !workspace.can_manage_plan}
                    onClick={() => void selectPlan(code)}
                    type="button"
                  >
                    {current ? `You’re on ${plan.label}` : pending === code ? "Updating…" : code === "basic" ? "Upgrade to Basic — $12/mo." : "Move back to Free"}
                  </button>
                  {code === "basic" && !current ? <small>Preview billing only — no card, no charge.</small> : null}
                </article>
              );
            })}
          </div>

          <p className="plan-future-label">Where this goes next</p>
          <p className="plan-future-note">Not available in this release.</p>
          <div className="plan-future-grid">
            {futurePlans.map((plan) => <article className={`plan-future-card is-${plan.label.toLowerCase()}`} key={plan.label}><h3>{plan.label}<span>Forward</span></h3><strong>{plan.price}</strong><p>{plan.tagline}</p><ul>{plan.features.map((feature) => <li key={feature}>· <span>{feature}</span></li>)}</ul><small>Not in this release</small></article>)}
          </div>

          <div className="plan-never-limited">
            <strong>Never limited, on any plan.</strong>
            <span>the read · the record · evidence · safety</span>
            <p>The quality of the read · Documents and History · OSLO chat · Asking anyone for their read · Link revocation and expiry · Every recommendation · Editing by hand</p>
            <b>Move back to Free and you keep everything you understood.</b>
          </div>

          {!workspace.can_manage_plan ? <p className="plan-modal-status" role="status">Only the workspace owner can change this plan.</p> : null}
          {message ? <p className="plan-modal-status" role="status">{message}</p> : null}
        </div>
        <footer><span><strong>Plan changes are preview-only</strong> — no card, no charge.</span><button onClick={onClose} type="button">Done</button></footer>
      </section>
    </div>
  );
}

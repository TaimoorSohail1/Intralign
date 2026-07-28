"use client";

import { Check, Sparkle, X } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

const plans = {
  free: {
    label: "Free",
    price: "$0",
    tagline: "The complete OSLO read for one active project.",
    features: [
      "The same governed OSLO judgment",
      "1 active project",
      "Up to 20 documents and 50,000 words",
      "3 collaborator seats",
      "Full artifacts, issues, history, and review",
    ],
  },
  basic: {
    label: "Basic",
    price: "$12",
    tagline: "More room for active work, evidence, and your team.",
    features: [
      "Everything in Free",
      "3 active projects",
      "Up to 40 documents and 100,000 words",
      "10 collaborator seats",
      "The same prompts, model, safety, and scoring",
    ],
  },
} as const;

type PlanDefinition = {
  label: string;
  price: string;
  tagline: string;
  features: readonly string[];
};

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
        ? "Basic is now active in this local preview. No card was charged."
        : "Free is now active. Your existing project data remains retained.",
    );
    setPending(null);
  };

  return (
    <div className="plan-modal-backdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <section
        aria-labelledby="plan-modal-title"
        aria-modal="true"
        className="plan-modal"
        role="dialog"
      >
        <header>
          <span className="plan-modal-mark"><Sparkle size={19} weight="fill" /></span>
          <div>
            <p>Workspace plan</p>
            <h2 id="plan-modal-title">Your plan</h2>
            <span>Capacity changes. The quality of OSLO&apos;s judgment does not.</span>
          </div>
          <button aria-label="Close plans" onClick={onClose} type="button"><X size={19} /></button>
        </header>

        <div className="plan-equality-note">
          <strong>Every plan gets the same read.</strong>
          <span>Plans differ only in capacity, scope, and collaboration—not model quality.</span>
        </div>

        <div className="plan-card-grid">
          {(Object.entries(plans) as Array<[WorkspaceSummary["plan"], PlanDefinition]>).map(
            ([code, plan]) => {
              const current = workspace.plan === code;
              return (
                <article className={`plan-card ${current ? "is-current" : ""}`} key={code}>
                  <div className="plan-card-heading">
                    <div>
                      <h3>{plan.label}</h3>
                      {current ? <span>Your plan</span> : null}
                    </div>
                    <p><strong>{plan.price}</strong>{code === "basic" ? <span>/ month</span> : null}</p>
                  </div>
                  <p>{plan.tagline}</p>
                  <ul>
                    {plan.features.map((feature) => (
                      <li key={feature}><Check size={15} weight="bold" />{feature}</li>
                    ))}
                  </ul>
                  <button
                    className={current ? "plan-current-button" : "plan-select-button"}
                    disabled={current || pending !== null || !workspace.can_manage_plan}
                    onClick={() => selectPlan(code)}
                    type="button"
                  >
                    {current
                      ? "Current plan"
                      : pending === code
                        ? "Updating…"
                        : code === "basic"
                          ? "Simulate upgrade"
                          : "Switch to Free"}
                  </button>
                </article>
              );
            },
          )}
        </div>

        {!workspace.can_manage_plan ? (
          <p className="plan-modal-status" role="status">Only the workspace owner can change this plan.</p>
        ) : null}
        {message ? <p className="plan-modal-status" role="status">{message}</p> : null}
        <footer>
          <span><strong>Preview only:</strong> no payment method, invoice, or charge is created.</span>
          <button onClick={onClose} type="button">Done</button>
        </footer>
      </section>
    </div>
  );
}

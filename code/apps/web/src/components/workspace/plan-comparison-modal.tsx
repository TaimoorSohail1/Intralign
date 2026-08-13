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
      "1 active project",
      "1 active outcome",
      "Up to ~50k extracted words",
      "The complete OSLO read and record",
      "Reviewers, Viewers and manual file export",
    ],
  },
  basic: {
    label: "Basic",
    price: "$29",
    tagline: "More plans and outcomes, with the same governed judgment.",
    features: [
      "Everything in Free",
      "3 active projects",
      "Multiple active outcomes",
      "Up to ~100k extracted words",
      "Flat workspace price — never per seat",
    ],
  },
} as const;

export function PlanComparisonModal({
  open,
  workspace,
  onClose,
  onCheckoutRedirect = (url) => window.location.assign(url),
  wallKey = "multiPlan",
}: {
  open: boolean;
  workspace: WorkspaceSummary;
  onClose: () => void;
  onWorkspaceChange?: (workspace: WorkspaceSummary) => void;
  onCheckoutRedirect?: (url: string) => void;
  wallKey?: "multiOutcome" | "multiPlan" | "envelope";
}) {
  const [pending, setPending] = useState<"checkout" | "portal" | null>(null);
  const [interval, setInterval] = useState<"monthly" | "annual">("monthly");
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

  const redirectToStripe = (url: unknown, expectedHost: string) => {
    if (typeof url !== "string") throw new Error("CHECKOUT_URL_MISSING");
    const parsed = new URL(url);
    if (parsed.protocol !== "https:" || parsed.hostname !== expectedHost) {
      throw new Error("CHECKOUT_URL_INVALID");
    }
    onCheckoutRedirect(url);
  };

  const startCheckout = async () => {
    if (workspace.plan === "basic" || pending) return;
    setPending("checkout");
    setMessage(null);
    const response = await fetch("/api/workspace/billing/checkout", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ interval, wall_key: wallKey }),
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      setMessage(payload?.message ?? "Secure checkout could not be started.");
      setPending(null);
      return;
    }
    try {
      redirectToStripe(payload?.url, "checkout.stripe.com");
    } catch {
      setMessage("Secure checkout returned an invalid destination.");
      setPending(null);
    }
  };

  const openBillingPortal = async () => {
    if (workspace.plan !== "basic" || pending) return;
    setPending("portal");
    setMessage(null);
    const response = await fetch("/api/workspace/billing/portal", { method: "POST" });
    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      setMessage(payload?.message ?? "Billing could not be opened.");
      setPending(null);
      return;
    }
    try {
      redirectToStripe(payload?.url, "billing.stripe.com");
    } catch {
      setMessage("Billing returned an invalid destination.");
      setPending(null);
    }
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
            <span>Plans differ only on capacity. Judgment quality never changes.</span>
          </div>

          {workspace.plan === "free" ? (
            <div aria-label="Billing interval" className="plan-billing-toggle" role="group">
              <button
                aria-pressed={interval === "monthly"}
                onClick={() => setInterval("monthly")}
                type="button"
              >
                $29 / month
              </button>
              <button
                aria-pressed={interval === "annual"}
                onClick={() => setInterval("annual")}
                type="button"
              >
                $290 / year
              </button>
            </div>
          ) : null}

          <div className="plan-card-grid">
            {(Object.entries(plans) as Array<[WorkspaceSummary["plan"], typeof plans.free | typeof plans.basic]>).map(([code, plan]) => {
              const current = workspace.plan === code;
              return (
                <article className={`plan-card ${current ? "is-current" : ""}`} key={code}>
                  <div className="plan-card-heading">
                    <h3>{plan.label}</h3>
                    {current ? <span>Your plan</span> : null}
                  </div>
                  <p className="plan-price">
                    <strong>{code === "basic" && interval === "annual" ? "$290" : plan.price}</strong>
                    {code === "basic" ? <span>{interval === "annual" ? " / year" : " / month"}</span> : null}
                  </p>
                  <p className="plan-tagline">{plan.tagline}</p>
                  <ul>{plan.features.map((feature) => <li className="is-core" key={feature}><Check size={13} weight="bold" /><span>{feature}</span></li>)}</ul>
                  <button
                    className={current ? "plan-current-button" : "plan-select-button"}
                    disabled={(current && code === "free") || pending !== null || !workspace.can_manage_plan}
                    onClick={() => void (code === "basic" && !current ? startCheckout() : openBillingPortal())}
                    type="button"
                  >
                    {current && code === "free"
                      ? "You’re on Free"
                      : pending !== null
                        ? "Opening secure billing…"
                        : code === "basic" && !current
                          ? interval === "annual"
                            ? "Upgrade to Basic — $290/year"
                            : "Upgrade to Basic — $29/mo"
                          : "Manage billing"}
                  </button>
                  {code === "basic" && !current ? <small>Secure hosted checkout. Basic activates only after payment is verified.</small> : null}
                </article>
              );
            })}
          </div>

          <div className="plan-never-limited">
            <strong>Never limited, on any plan.</strong>
            <span>the read · the record · reviewers · Viewers · judgment quality</span>
            <p>Manual file export, History, evidence, recommendations and the complete governed read remain available on Free.</p>
            <b>Cancellation preserves every record. Existing over-limit work is never deleted.</b>
          </div>

          {!workspace.can_manage_plan ? <p className="plan-modal-status" role="status">Only the workspace owner can change this plan.</p> : null}
          {message ? <p className="plan-modal-status" role="status">{message}</p> : null}
        </div>
        <footer><span><strong>Billing is handled by Stripe</strong> — entitlement changes only after a verified payment event.</span><button onClick={onClose} type="button">Done</button></footer>
      </section>
    </div>
  );
}

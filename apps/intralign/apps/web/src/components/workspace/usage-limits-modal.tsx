"use client";

import { X } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

type UsageRow = {
  label: string;
  badge: string;
  detail: string;
  value: string;
  progress?: number;
  action?: string;
};

export function UsageLimitsModal({
  onClose,
  onUpdate,
  open,
  workspace,
}: {
  onClose: () => void;
  onUpdate: () => Promise<void>;
  open: boolean;
  workspace: WorkspaceSummary;
}) {
  const [updating, setUpdating] = useState(false);
  const [updateError, setUpdateError] = useState("");
  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [onClose, open]);

  if (!open) return null;

  const updateNow = async () => {
    setUpdating(true);
    setUpdateError("");
    try {
      await onUpdate();
    } catch (error) {
      setUpdateError(error instanceof Error ? error.message : "Analysis could not refresh");
      setUpdating(false);
    }
  };

  const activeProjects = workspace.projects.filter((project) => !project.archived).length;
  const activeProjectLimit = workspace.active_project_limit ?? (workspace.plan === "free" ? 1 : 3);
  const members = workspace.member_count ?? 1;
  const rows: UsageRow[] = [
    {
      label: "Monthly analyses",
      badge: workspace.monthly_analysis_limit === null ? "Not yet set" : "Included",
      detail: "Resets 1 September. Only an analysis run counts. Nothing is enforced.",
      value: `${workspace.monthly_analyses_used} used`,
    },
    {
      label: "Refresh — ‘Update now’ is free",
      badge: "",
      detail: "OSLO refreshes slowly. An update is one analysis.",
      value: "",
      action: "Update now",
    },
    {
      label: "Fixes OSLO applied today",
      badge: "No limit",
      detail: "Editing by hand is free.",
      value: "0 applied · no limit",
    },
    {
      label: "Questions asked today",
      badge: "Never capped",
      detail: "Does not count against your analyses.",
      value: "0 · uncapped",
    },
    {
      label: "Analyses run today",
      badge: "A count, not a cap",
      detail: "A count, not a limit.",
      value: `${Math.min(workspace.monthly_analyses_used, 1)} · today`,
    },
    {
      label: "Analyses from evidence today",
      badge: "Never metered",
      detail: "OSLO re-reads when someone answers you.",
      value: "0 · uncapped",
    },
    {
      label: "Active projects",
      badge: "Included",
      detail: "Archiving is reversible.",
      value: `${activeProjects} of ${activeProjectLimit}`,
      progress: Math.min(activeProjects / activeProjectLimit, 1),
    },
    {
      label: "Workspace members",
      badge: "Never capacity-gated",
      detail: "People, reviewers and Viewers are not a plan limit.",
      value: `${members}`,
    },
    {
      label: "Documents · History",
      badge: "Never metered",
      detail: "History never expires.",
      value: "∞",
    },
  ];

  return (
    <div
      className="usage-modal-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <section aria-labelledby="usage-modal-title" aria-modal="true" className="usage-modal" role="dialog">
        <header>
          <div>
            <h2 id="usage-modal-title">Usage &amp; limits</h2>
            <p>What you are using, what your plan includes, and — plainly — what has not been decided yet.</p>
          </div>
          <button aria-label="Close usage and limits" onClick={onClose} type="button">
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        <div className="usage-modal-body">
          <p className="usage-modal-label">What you are using, on {workspace.plan_label}</p>
          <div className="usage-limit-list">
            {rows.map((row) => (
              <article key={row.label}>
                <div>
                  <strong>{row.label}</strong>
                  {row.badge ? <span>{row.badge}</span> : null}
                  <small>{row.detail}</small>
                  {row.progress !== undefined ? (
                    <i aria-hidden="true"><b style={{ width: `${row.progress * 100}%` }} /></i>
                  ) : null}
                </div>
                {row.action ? (
                  <button disabled={updating} onClick={updateNow} type="button">
                    {updating ? "Updating…" : row.action}
                  </button>
                ) : <em>{row.value}</em>}
              </article>
            ))}
          </div>
          {updateError ? <p className="form-error" role="alert">{updateError}</p> : null}
          <p className="usage-modal-label">Never limited, on any plan</p>
          <p className="usage-never-limited">The record · History · reviewers · Viewers · manual file export · judgment quality.</p>
        </div>
      </section>
    </div>
  );
}

"use client";

import { useState, useSyncExternalStore } from "react";

import { BrandLockup } from "@/components/brand/brand-lockup";
import { startProjectAnalysis } from "@/lib/client/start-project-analysis";

interface IntakeExperienceProps {
  displayName: string;
  projectId?: string;
  logoutAction?: () => Promise<void>;
}

const templates = [
  ["Event", "Plan an event: define the outcome, audience, scope, schedule, resources and success measures."],
  ["Marketing Campaign", "Plan a marketing campaign: define the audience, message, channels, budget, schedule and success measures."],
  ["Product / Software Launch", "Plan a product or software launch: define users, scope, requirements, release plan, resources and adoption measures."],
  ["Strategic Initiative", "Plan a strategic initiative: define the intended outcome, scope, dependencies, milestones, resources and measures."],
  ["Generic Project Plan", "Describe the project outcome, context, scope, requirements, work, schedule, resources and measures."],
] as const;

const phases = [
  "Reading your plan",
  "Constructing plan artifacts",
  "Checking clarity, alignment and feasibility",
  "Preparing your Overview",
];

const supportedExtensions = new Set([
  ".pdf",
  ".docx",
  ".pptx",
  ".xlsx",
  ".csv",
  ".txt",
  ".md",
]);
const maxFiles = 10;
const maxFileBytes = 10 * 1024 * 1024;
const maxTotalBytes = 50 * 1024 * 1024;

async function noOpLogout() {}

const subscribeToHydration = () => () => {};

function AccountMenu({ displayName, logoutAction }: { displayName: string; logoutAction: () => Promise<void> }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="account-menu">
      <button
        aria-expanded={open}
        className="button button-ghost"
        onClick={() => setOpen((current) => !current)}
        type="button"
      >
        Account menu
      </button>
      {open ? (
        <div className="account-menu-panel">
          <strong>{displayName}</strong>
          <form action={logoutAction}>
            <button className="account-menu-logout" type="submit">Log out</button>
          </form>
        </div>
      ) : null}
    </div>
  );
}

export function IntakeExperience({
  displayName,
  projectId,
  logoutAction = noOpLogout,
}: IntakeExperienceProps) {
  const hydrated = useSyncExternalStore(subscribeToHydration, () => true, () => false);
  const [description, setDescription] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [view, setView] = useState<"intake" | "analyzing" | "overview">("intake");
  const [phase, setPhase] = useState(0);
  const [orientationOpen, setOrientationOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const canStart = description.trim().length > 0 || files.length > 0;

  const selectFiles = (selected: File[]) => {
    const errors: string[] = [];
    const supported = selected.filter((file) => {
      const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
      if (!supportedExtensions.has(extension)) {
        errors.push(`${file.name} is not a supported document.`);
        return false;
      }
      if (file.size === 0) {
        errors.push(`${file.name} is empty.`);
        return false;
      }
      if (file.size > maxFileBytes) {
        errors.push(`${file.name} is larger than the 10 MB limit.`);
        return false;
      }
      return true;
    });
    const limited = supported.slice(0, maxFiles);
    if (supported.length > maxFiles) {
      errors.push(`Choose no more than ${maxFiles} documents.`);
    }
    let totalBytes = 0;
    const withinTotalLimit = limited.filter((file) => {
      if (totalBytes + file.size > maxTotalBytes) {
        errors.push(`${file.name} exceeds the 50 MB combined limit.`);
        return false;
      }
      totalBytes += file.size;
      return true;
    });
    setFiles(withinTotalLimit);
    setError(errors.join(" "));
  };

  const startAnalysis = async () => {
    if (!canStart || view !== "intake") return;
    if (projectId) {
      setSubmitting(true);
      setError("");
      try {
        const result = await startProjectAnalysis({
          projectId,
          description,
          files,
        });
        window.location.assign(`/projects/${projectId}/analysis/${result.run_id}`);
        return;
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : "Analysis could not start");
        setSubmitting(false);
        return;
      }
    }
    setView("analyzing");
    const phaseDuration = ["127.0.0.1", "localhost"].includes(window.location.hostname) ? 250 : 7_500;
    phases.slice(1).forEach((_, index) => {
      window.setTimeout(() => setPhase(index + 1), phaseDuration * (index + 1));
    });
    window.setTimeout(() => {
      setView("overview");
      setOrientationOpen(localStorage.getItem("oslo_orientation_seen") !== "true");
    }, phaseDuration * phases.length);
  };

  const dismissOrientation = () => {
    localStorage.setItem("oslo_orientation_seen", "true");
    setOrientationOpen(false);
  };

  if (view === "analyzing") {
    return (
      <main className="entry-shell analysis-shell">
        <BrandLockup />
        <div className="analysis-status" role="status" aria-live="polite">
          <span className="analysis-spinner" aria-hidden="true" />
          <p className="eyebrow">Analyzing…</p>
          <h1>{phases[phase]}</h1>
          <p>Initial Analysis runs first · timing varies with evidence volume</p>
        </div>
        <footer className="entry-footer">ⓘ OSLO advises; you decide — you stay in control at every step.</footer>
      </main>
    );
  }

  if (view === "overview") {
    return (
      <main className="overview-shell">
        <header className="overview-header">
          <BrandLockup />
          <div className="overview-actions">
            <button className="button button-ghost" onClick={() => setOrientationOpen(true)} type="button">
              How OSLO works (replay)
            </button>
            <AccountMenu displayName={displayName} logoutAction={logoutAction} />
          </div>
        </header>
        <section className="overview-content">
          <p className="eyebrow">Project understanding</p>
          <h1>Overview</h1>
          <p>Your Initial Analysis is complete. This provisional read will be deepened automatically.</p>
          <div className="overview-sections">
            <section><h2>Confidence</h2><p>Understanding is forming · qualified by moderate reliability.</p></section>
            <section><h2>Start here</h2><p>Review the highest-impact clarification first.</p></section>
            <section><h2>Progress</h2><p>Initial Analysis complete · Extended Analysis queued.</p></section>
            <section><h2>More</h2><p>Plan artifacts (7) · Attention Map · Analysis history.</p></section>
          </div>
        </section>
        {orientationOpen ? (
          <section aria-label="How OSLO works" aria-modal="true" className="orientation-dialog" role="dialog">
            <p className="eyebrow">A quick orientation</p>
            <h2>How OSLO works</h2>
            <p>Understanding · OSLO → Judgement · you → Decision · you → Oversight · you</p>
            <button className="button button-primary" onClick={dismissOrientation} type="button">Get started</button>
          </section>
        ) : null}
        <footer className="entry-footer">ⓘ OSLO advises; you decide — you stay in control at every step.</footer>
      </main>
    );
  }

  return (
    <main className="entry-shell intake-shell">
      <BrandLockup />
      <h1 className="intake-title">See your plan like a strategic leader.</h1>
      <p className="intake-subtitle">
        Drop in a plan, brief, or notes. OSLO shows how clear, aligned, and feasible it is — and
        where the issues are.
      </p>
      <section className="composer">
        <textarea
          aria-label="Describe your project"
          disabled={!hydrated}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="e.g. We’re running DevNorth 2026, a one-day developer conference…"
          value={description}
        />
        {files.length > 0 ? (
          <ul className="file-list">
            {files.map((file, index) => (
              <li key={`${file.name}-${file.size}`}>
                <span>{file.name}</span>
                <button
                  aria-label={`Remove ${file.name}`}
                  onClick={() =>
                    setFiles((current) =>
                      current.filter((_, fileIndex) => fileIndex !== index),
                    )
                  }
                  type="button"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : null}
        <div className="composer-row">
          <label aria-disabled={!hydrated} className="button button-ghost" htmlFor="intake-files">⊕ Attach documents</label>
          <input
            accept=".pdf,.docx,.pptx,.xlsx,.csv,.txt,.md"
            aria-label="Attach documents"
            className="sr-only"
            disabled={!hydrated}
            id="intake-files"
            multiple
            onChange={(event) => selectFiles(Array.from(event.target.files ?? []))}
            type="file"
          />
          {!canStart ? <span className="composer-hint">Add a description, a document, or a template to start</span> : null}
          <button className="button button-primary" disabled={!canStart || !hydrated || submitting} onClick={startAnalysis} type="button">
            {submitting ? "Starting analysis…" : "See where I stand →"}
          </button>
        </div>
        {error ? <p className="intake-error" role="alert">{error}</p> : null}
      </section>
      <div className="template-list">
        <span>or start from a template:</span>
        {templates.map(([name, seed]) => (
          <button className="template-pill" disabled={!hydrated} key={name} onClick={() => setDescription(seed)} type="button">
            {name}
          </button>
        ))}
      </div>
      <button
        className="sample-link"
        disabled={!hydrated}
        onClick={() => setDescription("DevNorth 2026 is a one-day developer conference for approximately 450 attendees on 18 September. Confirm the venue, programme, Wi-Fi capacity, sponsors, budget, schedule and delivery owners.")}
        type="button"
      >
        See it on a sample project →
      </button>
      <footer className="entry-footer">ⓘ OSLO advises; you decide — you stay in control at every step.</footer>
    </main>
  );
}

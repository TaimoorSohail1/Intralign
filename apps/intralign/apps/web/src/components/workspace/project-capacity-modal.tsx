"use client";

import { Archive, ArrowRight, LockSimple, X } from "@phosphor-icons/react";
import { useEffect, useRef } from "react";

export function ProjectCapacityModal({
  busy,
  currentProjectName,
  onArchive,
  onClose,
  onComparePlans,
  open,
  planLabel,
}: {
  busy: boolean;
  currentProjectName: string;
  onArchive: () => void;
  onClose: () => void;
  onComparePlans: () => void;
  open: boolean;
  planLabel: string;
}) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeRef.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [onClose, open]);

  if (!open) return null;

  return (
    <div className="project-capacity-backdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <section aria-labelledby="project-capacity-title" aria-modal="true" className="project-capacity-modal" role="dialog">
        <header>
          <span className="project-capacity-title">
            <LockSimple aria-hidden="true" size={15} weight="fill" />
            <strong id="project-capacity-title">Run more than one plan</strong>
          </span>
          <span className="project-capacity-price">Basic · <b>$29/mo</b><small>or $290/yr · 2 months free</small></span>
          <button aria-label="Close capacity choice" onClick={onClose} ref={closeRef} type="button"><X size={17} /></button>
        </header>
        <p>
          Working several plans in your workspace at the same time is a <strong>Basic</strong> capability.
        </p>
        <p className="project-capacity-assurance">
          This gates <strong>capacity</strong>, never the <strong>quality</strong> of your read — the accuracy bar and your record stay the same on every plan.
        </p>
        <div className="project-capacity-choices">
          <button aria-label="Upgrade your plan" className="is-primary" onClick={onComparePlans} type="button">
            <span><strong>Unlock Basic — compare plans</strong></span>
            <ArrowRight aria-hidden="true" size={15} />
          </button>
          <button aria-label={`Archive ${currentProjectName} to free the slot`} className="is-link" disabled={busy} onClick={onArchive} type="button">
            <Archive aria-hidden="true" size={17} />
            <span><strong>Archive {currentProjectName} to switch (free)</strong></span>
          </button>
        </div>
        <footer>
          <button onClick={onClose} type="button">Not now</button>
          <p>You’re on the {planLabel} plan. Archiving is non-destructive: History, issues and the latest assessment remain restorable.</p>
        </footer>
      </section>
    </div>
  );
}

"use client";

import { Archive, ArrowRight, Diamond, X } from "@phosphor-icons/react";
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
          <span>{planLabel} plan · active-project capacity</span>
          <button aria-label="Close capacity choice" onClick={onClose} ref={closeRef} type="button"><X size={17} /></button>
        </header>
        <h2 id="project-capacity-title">Start another project</h2>
        <p>
          You’re on the {planLabel} plan. To start another project, compare plans or archive {currentProjectName} first. Nothing here changes your plan without your decision.
        </p>
        <div className="project-capacity-choices">
          <button onClick={onComparePlans} type="button">
            <Diamond aria-hidden="true" size={17} weight="fill" />
            <span><strong>Upgrade your plan</strong><small>See plans and what additional active-project capacity includes.</small></span>
            <ArrowRight aria-hidden="true" size={15} />
          </button>
          <button disabled={busy} onClick={onArchive} type="button">
            <Archive aria-hidden="true" size={17} />
            <span><strong>Archive {currentProjectName} to free the slot</strong><small>Non-destructive — History, issues and the latest assessment are retained and restorable.</small></span>
            <ArrowRight aria-hidden="true" size={15} />
          </button>
        </div>
        <footer><button onClick={onClose} type="button">Not now</button></footer>
      </section>
    </div>
  );
}

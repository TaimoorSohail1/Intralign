"use client";

import { useEffect, useRef, useState } from "react";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

type AnalysisCapacity = Pick<
  WorkspaceSummary,
  "monthly_analysis_limit" | "monthly_analyses_used" | "monthly_analysis_resets_at"
>;

const resetDateFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  timeZone: "UTC",
  year: "numeric",
});

function formatResetDate(value: string | null) {
  if (!value) return null;
  const parsed = new Date(`${value}T00:00:00Z`);
  return Number.isNaN(parsed.getTime()) ? null : resetDateFormatter.format(parsed);
}

export function ReadRefreshControl({
  capacity,
  projectId,
}: {
  capacity?: AnalysisCapacity;
  projectId: string;
}) {
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);
  const [capacityFailed, setCapacityFailed] = useState(false);
  const [remoteCapacity, setRemoteCapacity] = useState<AnalysisCapacity | null>(null);
  const requestInFlight = useRef(false);
  const activeCapacity = capacity ?? remoteCapacity;
  const limit = activeCapacity?.monthly_analysis_limit ?? null;
  const remaining = limit === null
    ? null
    : Math.max(limit - (activeCapacity?.monthly_analyses_used ?? 0), 0);
  const exhausted = activeCapacity !== null && activeCapacity !== undefined && remaining === 0;
  const explanationId = `read-refresh-capacity-${projectId}`;
  const resetDate = formatResetDate(activeCapacity?.monthly_analysis_resets_at ?? null);
  const unavailable = !activeCapacity || exhausted || busy;

  useEffect(() => {
    if (capacity) return;
    let cancelled = false;
    void (async () => {
      try {
        const response = await fetch("/api/workspace", { cache: "no-store" });
        const payload = await response.json().catch(() => null);
        if (
          !response.ok
          || !payload
          || !(payload.monthly_analysis_limit === null
            || typeof payload.monthly_analysis_limit === "number")
          || typeof payload.monthly_analyses_used !== "number"
          || !(payload.monthly_analysis_resets_at === null
            || typeof payload.monthly_analysis_resets_at === "string")
        ) {
          throw new Error("Capacity unavailable");
        }
        if (!cancelled) setRemoteCapacity(payload as AnalysisCapacity);
      } catch {
        if (!cancelled) setCapacityFailed(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [capacity]);

  const updateNow = async () => {
    if (unavailable || requestInFlight.current) return;
    requestInFlight.current = true;
    setBusy(true);
    setFailed(false);
    try {
      const response = await fetch(`/api/projects/${projectId}/analysis-runs/refresh`, {
        method: "POST",
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok || !payload?.run_id) throw new Error("Analysis could not refresh");
      window.location.assign(`/projects/${projectId}/analysis/${payload.run_id}`);
    } catch {
      requestInFlight.current = false;
      setBusy(false);
      setFailed(true);
    }
  };

  return (
    <section
      aria-busy={!activeCapacity && !capacityFailed}
      aria-label="Refresh the current read"
      className="read-refresh-control"
    >
      <span>
        <strong>Refresh the current read</strong>
        <small id={explanationId}>
          {!activeCapacity ? (
            capacityFailed
              ? "Capacity details are unavailable. Your current read remains available."
              : "Loading analysis capacity…"
          ) : exhausted ? (
            <>
              0 analyses remaining this month. Your current read remains available.
              {resetDate ? ` Resets ${resetDate}.` : null}
            </>
          ) : limit === null ? (
            "Runs a new Deep Pass · counts as 1 analysis · no monthly cap."
          ) : (
            `Runs a new Deep Pass · uses 1 of ${remaining} analyses remaining this month.`
          )}
        </small>
      </span>
      <button
        aria-describedby={explanationId}
        aria-disabled={unavailable}
        onClick={() => void updateNow()}
        type="button"
      >
        {busy ? "Starting…" : failed ? "Try again" : "Update now"}
      </button>
      {failed ? (
        <p className="read-refresh-error" role="alert">
          Analysis could not refresh. Your project data is unchanged; try again.
        </p>
      ) : null}
    </section>
  );
}

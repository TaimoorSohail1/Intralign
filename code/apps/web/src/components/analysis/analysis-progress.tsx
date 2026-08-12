"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { analysisFailureCopy } from "@/lib/analysis-errors";

const workflow = [
  ["submit_intake", "Reading your inputs…", "Securing the submitted project request…"],
  ["validate_scope", "Reading your inputs…", "Checking the project boundary…"],
  ["ingest_parse", "Drafting your plan documents…", "Intent · Scope · Requirements · Constraints · Work breakdown · Schedule · Resourcing"],
  ["perceive", "Drafting your plan documents…", "Extracting facts, claims and gaps from your evidence"],
  ["retrieve_evidence", "Mapping what your outcome rests on…", "Connecting the parts of your plan to the result"],
  ["construct_artifacts", "Drafting your plan documents…", "Intent · Scope · Requirements · Constraints · Work breakdown · Schedule · Resourcing"],
  ["checkpoint", "Mapping what your outcome rests on…", "Saving a safe, restartable checkpoint"],
  ["evaluate_advise", "Checking what is clear, aligned and feasible…", "Testing Viability · Grounding · Adaptability"],
  ["validate_result", "Ordering your issues…", "Putting the biggest threat to your outcome first"],
  ["publish", "Your read is ready.", "Preparing your first outcome decision"],
] as const;

type OutcomeDecision = {
  projectTitle: string;
  outcome: string;
};

export function AnalysisProgress({
  mode = "guided",
  projectId,
  runId,
}: {
  mode?: "guided" | "watch";
  projectId: string;
  runId: string;
}) {
  const router = useRouter();
  const arcRef = useRef<HTMLIFrameElement>(null);
  const decisionOutcomeRef = useRef<string | null>(null);
  const submittingDecisionRef = useRef(false);
  const [phase, setPhase] = useState<string>("submit_intake");
  const [completed, setCompleted] = useState<string[]>([]);
  const [completedArtifacts, setCompletedArtifacts] = useState<string[]>([]);
  const [failed, setFailed] = useState<string | null>(null);
  const [syncVersion, setSyncVersion] = useState(0);
  const [decision, setDecision] = useState<OutcomeDecision | null>(null);
  const [arcReady, setArcReady] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const failureCopy = failed ? analysisFailureCopy(failed) : null;
  const activeIndex = Math.max(0, workflow.findIndex(([id]) => id === phase));

  const loadDecision = useCallback(async () => {
    const response = await fetch(`/api/projects/${projectId}/overview`, { cache: "no-store" });
    if (!response.ok) {
      setFailed("ANALYSIS_RESULT_UNAVAILABLE");
      return;
    }
    const overview = await response.json();
    const intent = overview.artifacts?.find((artifact: { artifact_type?: string }) => artifact.artifact_type === "intent");
    const outcome = intent?.summary || overview.summary || overview.project_title || "Your project outcome";
    decisionOutcomeRef.current = outcome;
    setDecision({ projectTitle: overview.project_title || "Your project", outcome });
  }, [projectId]);

  useEffect(() => {
    const started = Date.now();
    const timer = window.setInterval(() => setElapsed(Date.now() - started), 1000);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    let closed = false;
    const sync = async () => {
      const response = await fetch(`/api/analysis-runs/${runId}`, { cache: "no-store" });
      if (!response.ok || closed) return;
      const run = await response.json();
      setPhase(run.phase ?? "submit_intake");
      setCompleted(run.completed_phases ?? []);
      if (run.status === "completed") await loadDecision();
      if (run.status === "failed") setFailed(run.error_code ?? "Analysis paused unexpectedly");
    };
    void sync();
    const stream = new EventSource(`/api/analysis-runs/${runId}/events`);
    const onProgress = (event: MessageEvent) => {
      const payload = JSON.parse(event.data);
      if (payload.phase) setPhase(payload.phase);
      if (event.type === "analysis.phase_completed" && payload.phase) {
        setCompleted((current) => [...new Set([...current, payload.phase])]);
      }
    };
    const onArtifactCompleted = (event: MessageEvent) => {
      const payload = JSON.parse(event.data);
      if (!payload.artifact_type) return;
      setCompletedArtifacts((current) => [...new Set([...current, payload.artifact_type])]);
    };
    const onCompleted = () => {
      stream.close();
      void loadDecision();
    };
    stream.addEventListener("analysis.phase_started", onProgress);
    stream.addEventListener("analysis.phase_completed", onProgress);
    stream.addEventListener("analysis.artifact_completed", onArtifactCompleted);
    stream.addEventListener("assessment.published", onCompleted);
    stream.addEventListener("analysis.completed", onCompleted);
    stream.addEventListener("analysis.failed", (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFailed(payload.error?.code ?? "Analysis paused unexpectedly");
      stream.close();
    });
    return () => {
      closed = true;
      stream.close();
    };
  }, [loadDecision, projectId, runId, syncVersion]);

  const stage = useMemo(() => Math.max(1, Math.min(8, Math.ceil(((activeIndex + 1) / workflow.length) * 8))), [activeIndex]);

  const arcEvents = useMemo(() => {
    const events: string[] = [];
    if (activeIndex >= 2) events.push("plan-structure");
    if (activeIndex >= 3) events.push("inference");
    if (activeIndex >= 7) events.push("pillars");
    if (decision) events.push("outcome");
    return events;
  }, [activeIndex, decision]);

  const syncArc = useCallback(() => {
    const target = arcRef.current?.contentWindow;
    if (!target) return;
    target.postMessage(
      {
        oarc: "sync",
        projectTitle: decision?.projectTitle,
        outcome: decision?.outcome,
        events: arcEvents,
        progress: decision ? 100 : ((activeIndex + 1) / workflow.length) * 100,
        complete: Boolean(decision),
        elapsed,
      },
      window.location.origin,
    );
  }, [activeIndex, arcEvents, decision, elapsed]);

  useEffect(() => {
    if (arcReady) syncArc();
  }, [arcReady, syncArc]);

  const retry = async () => {
    setFailed(null);
    const response = await fetch(`/api/analysis-runs/${runId}/retry`, { method: "POST" });
    if (!response.ok) {
      setFailed("ANALYSIS_RETRY_FAILED");
      return;
    }
    setSyncVersion((current) => current + 1);
  };

  const actOnOutcome = useCallback(async (action: "confirm" | "refine" | "defer", refinedOutcome?: string) => {
    const outcome = action === "refine" ? refinedOutcome?.trim() : decisionOutcomeRef.current;
    if (!outcome || submittingDecisionRef.current) return;
    submittingDecisionRef.current = true;
    const response = await fetch(`/api/projects/${projectId}/outcome-actions`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ action, outcome, idempotencyKey: crypto.randomUUID() }),
    });
    if (!response.ok) {
      submittingDecisionRef.current = false;
      arcRef.current?.contentWindow?.postMessage(
        { oarc: "decision-result", ok: false },
        window.location.origin,
      );
      return;
    }
    arcRef.current?.contentWindow?.postMessage(
      { oarc: "decision-result", ok: true },
      window.location.origin,
    );
    if (mode === "guided") {
      await fetch("/api/orientation", { method: "POST" }).catch(() => null);
    }
    window.setTimeout(() => router.replace(`/projects/${projectId}/overview`), 850);
  }, [mode, projectId, router]);

  useEffect(() => {
    if (mode !== "watch" || !decision) return;
    const handoff = window.setTimeout(() => void actOnOutcome("confirm"), 100);
    return () => window.clearTimeout(handoff);
  }, [actOnOutcome, decision, mode]);

  useEffect(() => {
    const onArcMessage = (event: MessageEvent) => {
      if (event.origin !== window.location.origin || event.source !== arcRef.current?.contentWindow) return;
      const payload = event.data as { oarc?: string; action?: string; text?: string | null } | null;
      if (!payload) return;
      if (payload.oarc === "ready") {
        setArcReady(true);
        return;
      }
      if (payload.oarc !== "handoff" && payload.oarc !== "decision") return;
      if (payload.action !== "confirm" && payload.action !== "refine" && payload.action !== "defer") return;
      void actOnOutcome(payload.action, payload.text ?? undefined);
    };
    window.addEventListener("message", onArcMessage);
    return () => window.removeEventListener("message", onArcMessage);
  }, [actOnOutcome]);

  return (
    <main aria-busy={!decision && !failed} className="r2-analysis-page">
      <iframe
        className="r2-analysis-prototype-frame"
        data-oarc-complete={decision ? "true" : "false"}
        data-oarc-elapsed={String(elapsed)}
        data-oarc-events={arcEvents.join(",")}
        data-oarc-outcome={decision?.outcome ?? ""}
        data-oarc-progress={String(decision ? 100 : ((activeIndex + 1) / workflow.length) * 100)}
        data-oarc-project-title={decision?.projectTitle ?? ""}
        onLoad={() => {
          setArcReady(true);
          window.setTimeout(syncArc, 0);
        }}
        ref={arcRef}
        src={`/r2/onboarding-arc.html?embed=1&live=1&mode=${mode}`}
        title="OSLO analysis and outcome confirmation"
      />

      {failed ? (
        <section className="r2-analysis-failure-shell" aria-live="assertive">
          <div className="r2-analysis-failure" role="alert">
            <p className="analysis-pill">Read paused</p>
            <h1>{failureCopy?.title ?? "The read paused"}</h1>
            <p>{failureCopy?.detail ?? "Your last good read is still available."}</p>
            <p>No incomplete result was published.</p>
            <button className="button button-primary" onClick={retry} type="button">Retry analysis</button>
          </div>
        </section>
      ) : null}
      <p className="sr-only" role="status">
        {decision
          ? "Analysis complete. Confirm, refine, or defer the inferred outcome."
          : `${workflow[activeIndex]?.[1] ?? "Preparing your read…"} Stage ${stage} of 8. ${Math.max(completedArtifacts.length, completed.length)} analysis steps complete.`}
      </p>
    </main>
  );
}

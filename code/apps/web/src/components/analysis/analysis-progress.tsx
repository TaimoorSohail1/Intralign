"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { analysisFailureCopy } from "@/lib/analysis-errors";
import { intralignLogo } from "@/components/overview/project-overview";

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

const graphNodes = [
  [0, 0, 13, "outcome"], [-105, -70, 8, "plan"], [8, -92, 8, "plan"], [114, -62, 8, "plan"],
  [-175, -132, 5, "work"], [-116, -150, 5, "work"], [-47, -162, 5, "work"], [62, -162, 5, "work"],
  [137, -143, 5, "work"], [205, -118, 5, "work"], [-245, -191, 3, "leaf"], [-196, -220, 3, "leaf"],
  [-136, -228, 3, "leaf"], [-78, -235, 3, "leaf"], [-16, -225, 3, "leaf"], [45, -232, 3, "leaf"],
  [102, -222, 3, "leaf"], [168, -210, 3, "leaf"], [235, -181, 3, "leaf"], [-263, -93, 3, "leaf"],
  [-210, -55, 3, "leaf"], [-145, -31, 3, "leaf"], [173, -47, 3, "leaf"], [226, -72, 3, "leaf"],
] as const;

const graphEdges = [
  [0, 1], [0, 2], [0, 3], [1, 4], [1, 5], [1, 6], [2, 6], [2, 7], [2, 8], [3, 8], [3, 9],
  [4, 10], [4, 11], [5, 12], [5, 13], [6, 14], [7, 15], [7, 16], [8, 17], [9, 18], [1, 19],
  [1, 20], [1, 21], [3, 22], [3, 23],
] as const;

type OutcomeDecision = {
  projectTitle: string;
  outcome: string;
};

function PlanGraph({ activeIndex }: { activeIndex: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const context = canvas.getContext("2d");
    if (!context) return;
    let frame = 0;
    let animationFrame = 0;

    const render = () => {
      const scale = window.devicePixelRatio || 1;
      const bounds = canvas.getBoundingClientRect();
      if (canvas.width !== bounds.width * scale || canvas.height !== bounds.height * scale) {
        canvas.width = bounds.width * scale;
        canvas.height = bounds.height * scale;
      }
      context.setTransform(scale, 0, 0, scale, 0, 0);
      context.clearRect(0, 0, bounds.width, bounds.height);
      const centerX = bounds.width / 2;
      const centerY = Math.max(270, bounds.height * 0.43);
      const reveal = activeIndex < 3 ? 1 : activeIndex < 5 ? 8 : activeIndex < 8 ? 18 : graphNodes.length;
      const grounded = activeIndex >= 7;

      graphEdges.forEach(([from, to], edgeIndex) => {
        if (from >= reveal || to >= reveal) return;
        const a = graphNodes[from];
        const b = graphNodes[to];
        const pulse = 0.15 + 0.08 * Math.sin(frame / 42 + edgeIndex);
        context.beginPath();
        context.moveTo(centerX + a[0], centerY + a[1]);
        context.lineTo(centerX + b[0], centerY + b[1]);
        context.strokeStyle = grounded && edgeIndex % 3 !== 1
          ? `rgba(226, 168, 67, ${0.48 + pulse})`
          : `rgba(126, 157, 204, ${0.18 + pulse})`;
        context.lineWidth = grounded && edgeIndex % 3 !== 1 ? 1.5 : 1;
        context.stroke();
      });

      graphNodes.slice(0, reveal).forEach(([x, y, radius, kind], nodeIndex) => {
        const cx = centerX + x;
        const cy = centerY + y;
        const glow = context.createRadialGradient(cx, cy, 0, cx, cy, radius * 4);
        const color = kind === "outcome" ? "80, 194, 159" : grounded && nodeIndex % 3 === 1 ? "226, 168, 67" : "126, 157, 204";
        glow.addColorStop(0, `rgba(${color}, .34)`);
        glow.addColorStop(1, `rgba(${color}, 0)`);
        context.fillStyle = glow;
        context.beginPath();
        context.arc(cx, cy, radius * 4, 0, Math.PI * 2);
        context.fill();
        context.fillStyle = `rgb(${color})`;
        context.beginPath();
        context.arc(cx, cy, radius, 0, Math.PI * 2);
        context.fill();
      });

      frame += 1;
      animationFrame = window.requestAnimationFrame(render);
    };
    render();
    return () => window.cancelAnimationFrame(animationFrame);
  }, [activeIndex]);

  return <canvas aria-hidden="true" className="r2-analysis-graph" ref={canvasRef} />;
}

export function AnalysisProgress({ projectId, runId }: { projectId: string; runId: string }) {
  const router = useRouter();
  const [phase, setPhase] = useState<string>("submit_intake");
  const [completed, setCompleted] = useState<string[]>([]);
  const [completedArtifacts, setCompletedArtifacts] = useState<string[]>([]);
  const [failed, setFailed] = useState<string | null>(null);
  const [syncVersion, setSyncVersion] = useState(0);
  const [decision, setDecision] = useState<OutcomeDecision | null>(null);
  const [refining, setRefining] = useState(false);
  const [refinedOutcome, setRefinedOutcome] = useState("");
  const [submittingDecision, setSubmittingDecision] = useState(false);
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
    setDecision({ projectTitle: overview.project_title || "Your project", outcome });
    setRefinedOutcome(outcome);
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

  const retry = async () => {
    setFailed(null);
    const response = await fetch(`/api/analysis-runs/${runId}/retry`, { method: "POST" });
    if (!response.ok) {
      setFailed("ANALYSIS_RETRY_FAILED");
      return;
    }
    setSyncVersion((current) => current + 1);
  };

  const actOnOutcome = async (action: "confirm" | "refine" | "defer") => {
    const outcome = action === "refine" ? refinedOutcome.trim() : decision?.outcome;
    if (!outcome || submittingDecision) return;
    setSubmittingDecision(true);
    const response = await fetch(`/api/projects/${projectId}/outcome-actions`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ action, outcome, idempotencyKey: crypto.randomUUID() }),
    });
    if (!response.ok) {
      setFailed("OUTCOME_ACTION_FAILED");
      setSubmittingDecision(false);
      return;
    }
    router.replace(`/projects/${projectId}/overview`);
  };

  return (
    <main className="r2-analysis-page">
      <header className="r2-analysis-masthead">
        <div className="r2-analysis-brand">
          <Image alt="Intralign" height={26} priority src={intralignLogo} unoptimized width={143} />
          <span>Outcome Orchestration</span>
        </div>
        <div className="r2-analysis-status">
          <span>{decision ? "Analysis complete" : "Initial analysis"}</span>
          <i style={{ width: `${decision ? 100 : ((activeIndex + 1) / workflow.length) * 100}%` }} />
        </div>
      </header>

      {!failed && activeIndex >= 3 ? <PlanGraph activeIndex={decision ? workflow.length : activeIndex} /> : null}

      <section className={`r2-analysis-stage${decision ? " is-decision" : ""}`} aria-live="polite">
        {failed ? (
          <div className="r2-analysis-failure" role="alert">
            <p className="analysis-pill">Read paused</p>
            <h1>{failureCopy?.title ?? "The read paused"}</h1>
            <p>{failureCopy?.detail ?? "Your last good read is still available."}</p>
            <p>No incomplete result was published.</p>
            <button className="button button-primary" onClick={retry} type="button">Retry analysis</button>
          </div>
        ) : decision ? (
          <div className="r2-outcome-card">
            <p>Confirm your outcome</p>
            {refining ? (
              <>
                <h1>Put the outcome in your own words.</h1>
                <textarea aria-label="Refine your outcome" onChange={(event) => setRefinedOutcome(event.target.value)} value={refinedOutcome} />
                <div className="r2-outcome-actions">
                  <button className="button button-primary" disabled={!refinedOutcome.trim() || submittingDecision} onClick={() => void actOnOutcome("refine")} type="button">Save — this is my outcome<span>In your own words</span></button>
                  <button className="button" onClick={() => setRefining(false)} type="button">Back</button>
                </div>
              </>
            ) : (
              <>
                <h1>“{decision.outcome}”</h1>
                <p className="r2-outcome-help">Either way, <strong>you own it</strong> — OSLO advises, you decide. Until you confirm, it stays OSLO’s inference.</p>
                <div className="r2-outcome-actions">
                  <button className="button button-primary" disabled={submittingDecision} onClick={() => void actOnOutcome("confirm")} type="button">✓ Yes — this is my outcome<span>Lock it in and steer by it</span></button>
                  <button className="button" disabled={submittingDecision} onClick={() => setRefining(true)} type="button">Close — I’ll refine it<span>Reword it right here</span></button>
                </div>
                <button className="r2-outcome-defer" disabled={submittingDecision} onClick={() => void actOnOutcome("defer")} type="button">Not sure yet — keep it as OSLO’s inference →</button>
              </>
            )}
          </div>
        ) : (
          <>
            {activeIndex < 3 ? <div className="r2-analysis-orb" aria-hidden="true"><i /></div> : null}
            <p className="analysis-pill"><i aria-hidden="true" /> Analyzing…</p>
            <h1>{workflow[activeIndex]?.[1] ?? "Preparing your read…"}</h1>
            <p className="r2-analysis-description">{workflow[activeIndex]?.[2]}</p>
            <p className="r2-analysis-stage-count">Stage {stage} of 8</p>
            <div className="r2-analysis-trace" aria-label="Completed analysis steps">
              <p>read inputs <span>· ok</span></p>
              {activeIndex >= 3 ? <p>drafted plan <span>· {completedArtifacts.length || Math.max(1, completed.length)} ready</span></p> : null}
              {activeIndex >= 5 ? <p>mapped the outcome <span>· ok</span></p> : null}
            </div>
            {elapsed >= 45_000 ? <p className="r2-analysis-wait">Still working — your current read remains safe.</p> : null}
            {elapsed >= 60_000 ? <p className="r2-analysis-provisional">This pass is taking longer than expected. OSLO will preserve the last good read and continue safely.</p> : null}
          </>
        )}
      </section>
      <p className="sr-only">OSLO is analyzing the submitted project evidence. Progress updates appear here without requiring a page reload.</p>
    </main>
  );
}

"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { analysisFailureCopy } from "@/lib/analysis-errors";

const workflow = [
  ["submit_intake", "Building your understanding…", "Securing your project request…"],
  ["validate_scope", "Building your understanding…", "Checking the project boundary…"],
  ["ingest_parse", "Reading your evidence…", "Turning documents into stable evidence fragments…"],
  ["perceive", "Reading your evidence…", "Extracting facts, claims and gaps…"],
  ["retrieve_evidence", "Grounding the project read…", "Linking every conclusion to supporting evidence…"],
  ["construct_artifacts", "Constructing your seven plan artifacts…", "Organising the plan into a complete project model…"],
  ["checkpoint", "Constructing your seven plan artifacts…", "Saving a safe, restartable checkpoint…"],
  ["evaluate_advise", "Evaluating the plan…", "Assessing clarity, alignment and feasibility…"],
  ["validate_result", "Preparing your Overview…", "Validating the evidence and scoring contract…"],
  ["publish", "Preparing your Overview…", "Publishing your provisional first read…"],
] as const;

const visibleStages = [
  "Read inputs",
  "Grounded evidence",
  "Constructed plan artifacts",
  "Evaluated the plan",
] as const;

const artifactLabels: Record<string, string> = {
  intent: "Intent",
  context: "Context",
  scope: "Scope",
  requirements: "Requirements",
  work_breakdown: "Work breakdown",
  schedule: "Schedule",
  resources: "Resources",
};

export function AnalysisProgress({
  projectId,
  runId,
}: {
  projectId: string;
  runId: string;
}) {
  const router = useRouter();
  const [phase, setPhase] = useState<string>("submit_intake");
  const [completed, setCompleted] = useState<string[]>([]);
  const [completedArtifacts, setCompletedArtifacts] = useState<string[]>([]);
  const [activeArtifacts, setActiveArtifacts] = useState<string[]>([]);
  const [failed, setFailed] = useState<string | null>(null);
  const failureCopy = failed ? analysisFailureCopy(failed) : null;
  const activeIndex = Math.max(0, workflow.findIndex(([id]) => id === phase));

  useEffect(() => {
    let closed = false;
    const sync = async () => {
      const response = await fetch(`/api/analysis-runs/${runId}`, { cache: "no-store" });
      if (!response.ok || closed) return;
      const run = await response.json();
      setPhase(run.phase ?? "submit_intake");
      setCompleted(run.completed_phases ?? []);
      if (run.status === "completed") router.replace(`/projects/${projectId}/overview`);
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
    const onArtifactStarted = (event: MessageEvent) => {
      const payload = JSON.parse(event.data);
      if (!payload.artifact_type) return;
      setActiveArtifacts((current) => [
        ...new Set([...current, payload.artifact_type]),
      ]);
    };
    const onArtifactCompleted = (event: MessageEvent) => {
      const payload = JSON.parse(event.data);
      if (!payload.artifact_type) return;
      setActiveArtifacts((current) =>
        current.filter((item) => item !== payload.artifact_type),
      );
      setCompletedArtifacts((current) => [
        ...new Set([...current, payload.artifact_type]),
      ]);
    };
    stream.addEventListener("analysis.phase_started", onProgress);
    stream.addEventListener("analysis.phase_completed", onProgress);
    stream.addEventListener("analysis.artifact_started", onArtifactStarted);
    stream.addEventListener("analysis.artifact_completed", onArtifactCompleted);
    stream.addEventListener("analysis.artifact_failed", (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      if (!payload.artifact_type) return;
      setActiveArtifacts((current) =>
        current.filter((item) => item !== payload.artifact_type),
      );
    });
    stream.addEventListener("assessment.published", () => {
      router.replace(`/projects/${projectId}/overview`);
    });
    stream.addEventListener("analysis.completed", () => {
      router.replace(`/projects/${projectId}/overview`);
    });
    stream.addEventListener("analysis.failed", (event) => {
      const payload = JSON.parse((event as MessageEvent).data);
      setFailed(payload.error?.code ?? "Analysis paused unexpectedly");
      stream.close();
    });
    return () => {
      closed = true;
      stream.close();
    };
  }, [projectId, router, runId]);

  const visibleStage = useMemo(() => {
    if (activeIndex <= 2) return 0;
    if (activeIndex <= 4) return 1;
    if (activeIndex <= 6) return 2;
    return 3;
  }, [activeIndex]);

  const completedTrace = visibleStages.slice(
    0,
    Math.max(visibleStage, Math.min(4, Math.floor(completed.length / 2))),
  );

  const retry = async () => {
    setFailed(null);
    await fetch(`/api/analysis-runs/${runId}/retry`, { method: "POST" });
    window.location.reload();
  };

  return (
    <main className="analysis-page">
      <section className="analysis-panel" aria-live="polite">
        <div className="analysis-scanner" aria-hidden="true"><i /></div>
        {failed ? (
          <>
            <p className="analysis-pill">Analysis failed</p>
            <h1>{failureCopy?.title}</h1>
            <p className="analysis-lede">{failureCopy?.detail}</p>
            <div className="failure-card" role="alert">
              <strong>{failureCopy?.title}</strong>
              <span>No incomplete result was published.</span>
            </div>
            <button className="button button-primary" onClick={retry} type="button">
              Retry analysis
            </button>
          </>
        ) : (
          <>
            <p className="analysis-pill"><i aria-hidden="true" /> Analyzing…</p>
            <h1>{workflow[activeIndex]?.[1] ?? "Preparing your Overview…"}</h1>
            <p className="analysis-lede">
              {workflow[activeIndex]?.[2] ?? "OSLO is preparing an evidence-qualified first read…"}
            </p>
            <div className="analysis-dots" aria-label={`Analysis stage ${visibleStage + 1} of 4`}>
              {visibleStages.map((stage, index) => (
                <i
                  aria-hidden="true"
                  className={index <= visibleStage ? "is-active" : ""}
                  key={stage}
                />
              ))}
            </div>
            <div className="analysis-trace" aria-label="Completed analysis steps">
              {completedTrace.length ? (
                completedTrace.map((stage) => (
                  <p key={stage}>
                    {stage.toLowerCase()} <span>· ok</span>
                  </p>
                ))
              ) : (
                <p>starting analysis <span>· ok</span></p>
              )}
            </div>
            {phase === "construct_artifacts" ? (
              <div className="analysis-trace" aria-label="Artifact construction progress">
                <p>
                  {completedArtifacts.length} of 7 artifacts safely saved
                  <span> · resumable</span>
                </p>
                {activeArtifacts.map((artifactType) => (
                  <p key={artifactType}>
                    {artifactLabels[artifactType] ?? artifactType}
                    <span> · building</span>
                  </p>
                ))}
              </div>
            ) : null}
            <p className="analysis-timing">
              Initial Analysis runs first · timing varies with evidence volume
            </p>
          </>
        )}
      </section>
      <footer className="entry-footer">
        ⓘ OSLO advises; you decide — you stay in control at every step.
      </footer>
    </main>
  );
}

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

const returningStages = [
  {
    title: "Reading your inputs…",
    description: "Opening your brief and any attachments…",
    trace: "read inputs",
    result: "ok",
  },
  {
    title: "Drafting your plan documents…",
    description: "Building the working documents that make up your plan…",
    trace: "drafted plan",
    result: "documents",
  },
  {
    title: "Separating evidence from inference…",
    description: "Marking what you stated as your evidence…",
    trace: "separated evidence from inference",
    result: "tagged",
  },
  {
    title: "Mapping what your outcome rests on…",
    description: "Linking program, venue, sponsors and logistics to your outcome…",
    trace: "mapped what your outcome rests on",
    result: "linked",
  },
  {
    title: "Noting your open questions…",
    description: "Collecting the open questions in your brief…",
    trace: "noted your open questions",
    result: "flagged",
  },
  {
    title: "Assessing your plan…",
    description: "Checking clarity, alignment and feasibility…",
    trace: "assessed Clarity · Alignment · Feasibility",
    result: "",
  },
  {
    title: "Pulling your read together…",
    description: "Bringing it into one clear read of where you stand…",
    trace: "pulled your read together",
    result: "first read",
  },
  {
    title: "Your strategic read is ready.",
    description: "Preparing your initial read…",
    trace: "surfaced issues + clarifications",
    result: "initial read complete",
  },
] as const;

const returningStageByPhase: Record<string, number> = {
  submit_intake: 1,
  validate_scope: 1,
  ingest_parse: 2,
  perceive: 3,
  retrieve_evidence: 4,
  construct_artifacts: 4,
  checkpoint: 5,
  evaluate_advise: 6,
  validate_result: 7,
  publish: 8,
};

const returningStageDurations = [2_000, 4_800, 2_100, 2_100, 2_100, 2_100, 2_100, 1_200] as const;

function buildRingSegments(count: number) {
  const center = 84;
  const radius = 79;
  const gap = count > 10 ? 6 : 9;
  const segment = 360 / count;
  return Array.from({ length: count }, (_, index) => {
    const start = ((index * segment) - 90 + gap / 2) * Math.PI / 180;
    const end = (((index + 1) * segment) - 90 - gap / 2) * Math.PI / 180;
    const x0 = center + radius * Math.cos(start);
    const y0 = center + radius * Math.sin(start);
    const x1 = center + radius * Math.cos(end);
    const y1 = center + radius * Math.sin(end);
    const largeArc = segment - gap > 180 ? 1 : 0;
    return `M${x0.toFixed(1)} ${y0.toFixed(1)} A${radius} ${radius} 0 ${largeArc} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}`;
  });
}

const ringSegments = buildRingSegments(returningStages.length);

function ReturningAnalysisLoader({
  artifactCount,
  stage,
}: {
  artifactCount: number;
  stage: number;
}) {
  const active = returningStages[stage - 1];
  return (
    <section className="r2-returning-loader" aria-label="Analysis progress">
      <div className="r2-returning-scanner" aria-hidden="true">
        <svg className="r2-returning-ring" viewBox="0 0 168 168">
          {ringSegments.map((path, index) => (
            <path
              className={
                stage === returningStages.length || index < stage - 1
                  ? "is-complete"
                  : index === stage - 1
                    ? "is-active"
                    : ""
              }
              d={path}
              key={path}
            />
          ))}
        </svg>
        <span className="r2-returning-core" />
      </div>
      <p className="r2-returning-pill"><span />Analyzing…</p>
      <h1>{active.title}</h1>
      <p className="r2-returning-description">{active.description}</p>
      <p className="r2-returning-stage">Stage {stage} of 8</p>
      <ol className="r2-returning-trace">
        {returningStages.slice(0, stage).map((item, index) => {
          const result = index === 1
            ? `${artifactCount || 7} documents`
            : item.result;
          return (
            <li key={item.trace}>
              <span>{item.trace}</span>
              {result ? <><i>·</i><strong className="is-complete-status">{result}</strong></> : null}
            </li>
          );
        })}
      </ol>
      <p className="r2-returning-expectation">Preliminary Outcome Analysis · up to about a minute</p>
    </section>
  );
}

type OutcomeDecision = {
  projectTitle: string;
  outcome: string;
};

type OutcomeOverview = {
  project_title?: string | null;
  summary?: string | null;
  artifacts?: Array<{ artifact_type?: string; summary?: string | null }>;
};

type IntentArtifact = {
  content?: {
    sections?: Array<{
      heading?: string | null;
      body?: string | null;
      bullets?: string[];
    }>;
  };
};

const extractionSummary = /\b(?:extracted|derived|assembled) from\b|^initial (?:structured|evidence-qualified) intent\b/i;

function firstSentence(value: string) {
  const normalized = value.replace(/\s+/g, " ").trim();
  const sentence = normalized.match(/^.+?[.!?](?:\s|$)/)?.[0]?.trim();
  return sentence && sentence.length >= 20 ? sentence : normalized;
}

export function selectOutcomeCandidate(
  overview: OutcomeOverview,
  intentArtifact?: IntentArtifact | null,
) {
  const sections = intentArtifact?.content?.sections ?? [];
  const preferredSections = [
    ...sections.filter((section) =>
      /outcome|executive summary|intent|objective/i.test(section.heading ?? ""),
    ),
    ...sections.filter((section) =>
      !/outcome|executive summary|intent|objective/i.test(section.heading ?? ""),
    ),
  ];
  const sourceCandidate = preferredSections
    .flatMap((section) => [section.body ?? "", ...(section.bullets ?? [])])
    .map((candidate) => candidate.replace(/\s+/g, " ").trim())
    .find((candidate) => candidate.length >= 20 && !extractionSummary.test(candidate));
  if (sourceCandidate) return firstSentence(sourceCandidate);

  const intentSummary = overview.artifacts?.find(
    (artifact) => artifact.artifact_type === "intent",
  )?.summary?.trim();
  if (intentSummary && !extractionSummary.test(intentSummary)) return intentSummary;
  if (overview.summary?.trim() && !extractionSummary.test(overview.summary)) {
    return overview.summary.trim();
  }
  if (overview.project_title?.trim()) {
    return `Deliver ${overview.project_title.trim()} according to the submitted plan.`;
  }
  return "Deliver the outcome described in the submitted project information.";
}

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
  const [visibleWatchStage, setVisibleWatchStage] = useState(1);
  const failureCopy = failed ? analysisFailureCopy(failed) : null;
  const activeIndex = Math.max(0, workflow.findIndex(([id]) => id === phase));

  const loadDecision = useCallback(async () => {
    const [overviewResponse, intentResponse] = await Promise.all([
      fetch(`/api/projects/${projectId}/overview`, { cache: "no-store" }),
      fetch(`/api/projects/${projectId}/artifacts/intent`, { cache: "no-store" }),
    ]);
    if (!overviewResponse.ok) {
      setFailed("ANALYSIS_RESULT_UNAVAILABLE");
      return;
    }
    const overview = await overviewResponse.json() as OutcomeOverview;
    const publishedArtifacts = [
      ...new Set(
        (overview.artifacts ?? [])
          .map((artifact) => artifact.artifact_type?.trim())
          .filter((artifactType): artifactType is string => Boolean(artifactType)),
      ),
    ];
    if (publishedArtifacts.length > 0) {
      setCompletedArtifacts(publishedArtifacts);
    }
    const intentArtifact = intentResponse.ok
      ? await intentResponse.json() as IntentArtifact
      : null;
    const outcome = selectOutcomeCandidate(overview, intentArtifact);
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

  // Completed runs can end on a post-publication phase (for example
  // `extended_transition`) that is intentionally outside the visible loader
  // vocabulary. Once the result is available, always finish the eight-stage
  // cadence instead of falling back to Stage 1.
  const actualWatchStage = decision ? returningStages.length : returningStageByPhase[phase] ?? 1;

  useEffect(() => {
    if (mode !== "watch" || visibleWatchStage >= actualWatchStage) return;
    const timer = window.setTimeout(
      () => setVisibleWatchStage((current) => Math.min(current + 1, actualWatchStage)),
      returningStageDurations[visibleWatchStage - 1],
    );
    return () => window.clearTimeout(timer);
  }, [actualWatchStage, mode, visibleWatchStage]);

  const stage = mode === "watch"
    ? visibleWatchStage
    : Math.max(1, Math.min(8, Math.ceil(((activeIndex + 1) / workflow.length) * 8)));

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
    if (mode === "watch") setVisibleWatchStage(1);
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
    if (mode !== "watch" || !decision || stage < returningStages.length) return;
    const handoff = window.setTimeout(
      () => router.replace(`/projects/${projectId}/overview`),
      returningStageDurations[returningStageDurations.length - 1],
    );
    return () => window.clearTimeout(handoff);
  }, [decision, mode, projectId, router, stage]);

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
    <main aria-busy={!failed && (!decision || (mode === "watch" && stage < returningStages.length))} className="r2-analysis-page">
      {mode === "guided" ? (
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
          src="/r2/onboarding-arc.html?embed=1&live=1&mode=guided"
          title="OSLO analysis and outcome confirmation"
        />
      ) : (
        <ReturningAnalysisLoader artifactCount={completedArtifacts.length} stage={stage} />
      )}

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
        {decision && (mode !== "watch" || stage === returningStages.length)
          ? "Analysis complete. Confirm, refine, or defer the inferred outcome."
          : `${mode === "watch" ? returningStages[stage - 1].title : workflow[activeIndex]?.[1] ?? "Preparing your read…"} Stage ${stage} of 8. ${Math.max(completedArtifacts.length, completed.length)} analysis steps complete.`}
      </p>
    </main>
  );
}

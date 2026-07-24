"use client";

import {
  ArrowRight,
  CaretDown,
  CaretRight,
  ChatTeardropDots,
  Info,
  PaperPlaneTilt,
  Sparkle,
  X,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import type { FormEvent } from "react";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

const dimensions = ["clarity", "alignment", "feasibility"] as const;
const artifactOrder = [
  "intent",
  "context",
  "scope",
  "requirements",
  "work_breakdown",
  "schedule",
  "resources",
] as const;
const initialAdvisorQuestions = [
  "What should I address first?",
  "Why is Feasibility Low?",
  "Explain the top issue",
  "What do you need me to confirm?",
];
const severityRank: Record<string, number> = {
  Critical: 3,
  Moderate: 2,
  Warning: 1,
};
const dimensionStrength: Record<string, number> = {
  High: 76,
  Moderate: 55,
  Low: 38,
  "Very Low": 28,
};

type Issue = OverviewSnapshot["assessment"]["issues"][number];
type ProjectView = "overview" | "attention";

interface ChatMessage {
  id: number;
  role: "user" | "advisor";
  text: string;
}

function issueSort(left: Issue, right: Issue) {
  return (severityRank[right.severity] ?? 0) - (severityRank[left.severity] ?? 0);
}

function artifactLabel(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function ProjectOverview({
  initial,
  displayName,
  logoutAction,
  initialView = "overview",
}: {
  initial: OverviewSnapshot;
  displayName: string;
  logoutAction: () => Promise<void>;
  initialView?: ProjectView;
}) {
  const router = useRouter();
  const [snapshot, setSnapshot] = useState(initial);
  const [orientation, setOrientation] = useState(false);
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(null);
  const [advisorOpen, setAdvisorOpen] = useState(true);
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [attentionMode, setAttentionMode] = useState<"heatmap" | "dimensions">("heatmap");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [advisorQuestions, setAdvisorQuestions] = useState(initialAdvisorQuestions);
  const [question, setQuestion] = useState("");
  const [advisorPending, setAdvisorPending] = useState(false);
  const [advisorError, setAdvisorError] = useState<string | null>(null);
  const [newProjectPending, setNewProjectPending] = useState(false);
  const [newProjectError, setNewProjectError] = useState<string | null>(null);
  const [extendedRetrying, setExtendedRetrying] = useState(false);
  const [extendedRetryError, setExtendedRetryError] = useState<string | null>(null);
  const [clarificationAnswer, setClarificationAnswer] = useState("");
  const [clarificationPending, setClarificationPending] = useState(false);
  const [clarificationError, setClarificationError] = useState<string | null>(null);
  const [analysisUpdateRunId, setAnalysisUpdateRunId] = useState<string | null>(null);
  const advisorInFlight = useRef(false);
  const projectInFlight = useRef(false);
  const advisorStateBeforeIssue = useRef(true);
  const issueTrigger = useRef<HTMLElement | null>(null);
  const messageId = useRef(0);

  const isProvisional = snapshot.state === "provisional";
  const extendedRun = snapshot.extended_analysis;
  const extendedFailed =
    isProvisional && extendedRun?.status === "failed" && !extendedRetrying;
  const openIssues = useMemo(
    () =>
      snapshot.assessment.issues
        .filter((issue) => issue.status !== "resolved")
        .sort(issueSort),
    [snapshot.assessment.issues],
  );
  const clarificationIssue = openIssues.find((issue) => Boolean(issue.clarification));
  const criticalCount = openIssues.filter((issue) => issue.severity === "Critical").length;
  const clarificationCount = openIssues.filter((issue) => Boolean(issue.clarification)).length;
  const limitingDimension = useMemo(
    () =>
      dimensions.reduce((weakest, dimension) =>
        (dimensionStrength[snapshot.assessment[dimension]] ?? 0) <
        (dimensionStrength[snapshot.assessment[weakest]] ?? 0)
          ? dimension
          : weakest,
      ),
    [snapshot.assessment],
  );

  useEffect(() => {
    const orientationTimer = window.setTimeout(
      () => setOrientation(localStorage.getItem("oslo_orientation_seen") !== "true"),
      0,
    );
    if (!isProvisional || extendedFailed) {
      return () => window.clearTimeout(orientationTimer);
    }
    const timer = window.setInterval(async () => {
      try {
        const response = await fetch(`/api/projects/${snapshot.project_id}/overview`, {
          cache: "no-store",
        });
        if (!response.ok) return;
        const next: OverviewSnapshot = await response.json();
        setSnapshot(next);
        setExtendedRetrying(false);
        if (next.state === "current" || next.extended_analysis?.status === "failed") {
          window.clearInterval(timer);
        }
      } catch {
        // Keep the last published Overview through transient polling failures.
      }
    }, 2500);
    return () => {
      window.clearTimeout(orientationTimer);
      window.clearInterval(timer);
    };
  }, [extendedFailed, isProvisional, snapshot.project_id]);

  useEffect(() => {
    if (!analysisUpdateRunId) return;
    const timer = window.setInterval(async () => {
      try {
        const runResponse = await fetch(`/api/analysis-runs/${analysisUpdateRunId}`, {
          cache: "no-store",
        });
        if (!runResponse.ok) return;
        const run = await runResponse.json();
        if (run.status === "completed") {
          const overviewResponse = await fetch(
            `/api/projects/${snapshot.project_id}/overview`,
            { cache: "no-store" },
          );
          if (overviewResponse.ok) setSnapshot(await overviewResponse.json());
          setAnalysisUpdateRunId(null);
          setClarificationAnswer("");
        }
        if (run.status === "failed") {
          setAnalysisUpdateRunId(null);
          setClarificationError(
            "Your answer is saved, but the update paused safely. The current read is unchanged.",
          );
        }
      } catch {
        // Durable state will be recovered by the next poll or page refresh.
      }
    }, 2500);
    return () => window.clearInterval(timer);
  }, [analysisUpdateRunId, snapshot.project_id]);

  useEffect(() => {
    if (!selectedIssue) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSelectedIssue(null);
        setAdvisorOpen(advisorStateBeforeIssue.current);
        window.setTimeout(() => issueTrigger.current?.focus(), 0);
      }
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  });

  const dismissOrientation = async () => {
    localStorage.setItem("oslo_orientation_seen", "true");
    setOrientation(false);
    await fetch("/api/orientation", { method: "POST" });
  };

  const openIssue = (issue: Issue, trigger?: HTMLElement | null) => {
    advisorStateBeforeIssue.current = advisorOpen;
    issueTrigger.current = trigger ?? (document.activeElement as HTMLElement | null);
    setAdvisorOpen(false);
    setSelectedIssue(issue);
    setClarificationAnswer("");
    setClarificationError(null);
  };

  const closeIssue = () => {
    setSelectedIssue(null);
    setAdvisorOpen(advisorStateBeforeIssue.current);
    window.setTimeout(() => issueTrigger.current?.focus(), 0);
  };

  const askQuestion = async (value: string) => {
    const normalized = value.trim();
    if (!normalized || advisorInFlight.current) return;
    advisorInFlight.current = true;
    setAdvisorPending(true);
    setAdvisorError(null);
    setQuestion("");
    setMessages((current) => [
      ...current,
      { id: ++messageId.current, role: "user", text: normalized },
    ]);
    try {
      const response = await fetch(`/api/projects/${snapshot.project_id}/advisor`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question: normalized }),
      });
      if (!response.ok) throw new Error("advisor unavailable");
      const reply = await response.json();
      setMessages((current) => [
        ...current,
        { id: ++messageId.current, role: "advisor", text: reply.answer },
      ]);
      setAdvisorQuestions(reply.follow_up_questions ?? []);
    } catch {
      setAdvisorError("OSLO could not answer right now. Your project data is unchanged.");
    } finally {
      advisorInFlight.current = false;
      setAdvisorPending(false);
    }
  };

  const submitQuestion = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    void askQuestion(question);
  };

  const createNewProject = async () => {
    if (projectInFlight.current) return;
    projectInFlight.current = true;
    setNewProjectPending(true);
    setNewProjectError(null);
    try {
      const response = await fetch("/api/projects/new", { method: "POST" });
      if (!response.ok) throw new Error("project creation failed");
      const project = await response.json();
      router.push(`/intake?project=${project.id}`);
    } catch {
      projectInFlight.current = false;
      setNewProjectPending(false);
      setNewProjectError("A new project could not be created. Please try again.");
    }
  };

  const retryExtendedAnalysis = async () => {
    if (!extendedRun || extendedRetrying) return;
    setExtendedRetryError(null);
    setExtendedRetrying(true);
    try {
      const response = await fetch(`/api/analysis-runs/${extendedRun.run_id}/retry`, {
        method: "POST",
      });
      if (!response.ok) throw new Error("retry failed");
    } catch {
      setExtendedRetrying(false);
      setExtendedRetryError("Extended Analysis could not be restarted. Please try again.");
    }
  };

  const submitClarification = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedIssue || !clarificationAnswer.trim() || clarificationPending) return;
    setClarificationPending(true);
    setClarificationError(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/issues/${encodeURIComponent(selectedIssue.id)}/answers`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            answer: clarificationAnswer.trim(),
            idempotencyKey: crypto.randomUUID(),
          }),
        },
      );
      if (!response.ok) throw new Error("answer was not accepted");
      const result = await response.json();
      setAnalysisUpdateRunId(result.run_id);
    } catch {
      setClarificationError("Your answer could not be saved. Please try again.");
    } finally {
      setClarificationPending(false);
    }
  };

  const extendedFailureMessage =
    extendedRun?.error_code === "EVIDENCE_REFERENCE_CONTRACT_FAILED"
      ? "An evidence reference did not match the source document."
      : "The deeper read stopped before it could safely publish.";

  const panelVisible = advisorOpen || Boolean(selectedIssue);

  return (
    <main className={`project-shell ${selectedIssue ? "has-issue" : ""}`}>
      <header className="project-header">
        <Link className="project-logo" href={`/projects/${snapshot.project_id}/overview`}>
          <span aria-hidden="true">O</span>
          OSLO
        </Link>
        <nav aria-label="Project">
          <Link
            className={initialView === "overview" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/overview`}
          >
            Overview
          </Link>
          <Link
            className={initialView === "attention" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/attention`}
          >
            Attention
            {openIssues.length ? <span className="nav-count">{openIssues.length}</span> : null}
          </Link>
          <Link href={`/projects/${snapshot.project_id}/overview#project-summary`}>Project</Link>
        </nav>
        <div className="project-actions">
          {!panelVisible ? (
            <button
              className="advisor-reopen"
              onClick={() => setAdvisorOpen(true)}
              type="button"
            >
              <ChatTeardropDots aria-hidden="true" size={15} />
              OSLO
            </button>
          ) : null}
          <button
            aria-label="New project"
            className="new-project-button"
            disabled={newProjectPending}
            onClick={createNewProject}
            type="button"
          >
            {newProjectPending ? "Creating…" : "+ New project"}
          </button>
          <details className="project-account">
            <summary>{displayName.slice(0, 1).toUpperCase()}</summary>
            <div>
              <strong>{displayName}</strong>
              <button
                onClick={(event) => {
                  event.currentTarget.closest("details")?.removeAttribute("open");
                  setOrientation(true);
                }}
                type="button"
              >
                How OSLO works
              </button>
              <form action={logoutAction}>
                <button type="submit">Log out</button>
              </form>
            </div>
          </details>
          {newProjectError ? (
            <span className="project-action-error" role="alert">
              {newProjectError}
            </span>
          ) : null}
        </div>
      </header>

      <div className={`project-grid ${panelVisible ? "" : "is-panel-closed"}`}>
        <section className="project-main">
          {initialView === "overview" ? (
            <>
              <section className="confidence-read">
                <div className="confidence-topline">
                  <p className="eyebrow">Confidence</p>
                  <span className={`snapshot-badge ${isProvisional ? "" : "is-current"}`}>
                    {snapshot.state.replace("_", "-")}
                  </span>
                </div>
                <div className="confidence-summary">
                  <div className="confidence-number">
                    <strong>{snapshot.assessment.confidence_index}</strong>
                    <span>/100</span>
                    <button
                      onClick={() => {
                        setAdvisorOpen(true);
                        void askQuestion("Explain the confidence score");
                      }}
                      type="button"
                    >
                      <Sparkle aria-hidden="true" size={12} weight="fill" />
                      Ask OSLO why
                    </button>
                  </div>
                  <div className="confidence-copy">
                    <h1>Understanding is forming</h1>
                    <p>
                      {snapshot.assessment.confidence_band} · qualified by{" "}
                      <strong>{snapshot.assessment.reliability.toLowerCase()} reliability</strong>
                    </p>
                    {!isProvisional ? (
                      <span className="confidence-change">Current evidence-qualified read</span>
                    ) : null}
                  </div>
                </div>
                <div className="confidence-divider" />
                <p className="dimension-help">
                  What&apos;s driving it — hover or focus a dimension for detail
                </p>
                <div className="dimension-bars">
                  {dimensions.map((name) => {
                    const value = snapshot.assessment[name];
                    const limiting = name === limitingDimension;
                    return (
                      <div className={limiting ? "is-limiting" : ""} key={name}>
                        <span>{artifactLabel(name)}</span>
                        <div
                          aria-label={`${artifactLabel(name)}: ${value}`}
                          aria-valuemax={100}
                          aria-valuemin={0}
                          aria-valuenow={dimensionStrength[value] ?? 50}
                          className="dimension-track"
                          role="progressbar"
                          tabIndex={0}
                        >
                          <i style={{ width: `${dimensionStrength[value] ?? 50}%` }} />
                        </div>
                        <strong>{value}</strong>
                      </div>
                    );
                  })}
                </div>
                <div className="confidence-footer">
                  <span>
                    <strong>{openIssues.length}</strong> issues open · <strong>0</strong> resolved
                  </span>
                  <div>
                    <button type="button">
                      Why <CaretDown aria-hidden="true" size={11} />
                    </button>
                    <Link
                      aria-label="Timeline"
                      href={`/projects/${snapshot.project_id}/attention`}
                    >
                      Timeline <ArrowRight aria-hidden="true" size={12} />
                    </Link>
                  </div>
                </div>
              </section>

              <section className="start-here">
                <div className="overview-label">
                  <p>Start here</p>
                  <Info aria-hidden="true" size={14} />
                </div>
                <div className="issue-list">
                  {openIssues.slice(0, 4).map((issue, index) => (
                    <button
                      className={`issue-row issue-row-${issue.severity.toLowerCase()}`}
                      key={issue.id}
                      onClick={(event) => openIssue(issue, event.currentTarget)}
                      type="button"
                    >
                      <span className={`severity severity-${issue.severity.toLowerCase()}`}>
                        {issue.severity}
                      </span>
                      <strong>{issue.title}</strong>
                      {index === 0 ? (
                        <span className="issue-review">
                          Review <ArrowRight aria-hidden="true" size={12} />
                        </span>
                      ) : (
                        <span className="issue-location">
                          in {artifactLabel(issue.artifact_type)}
                          <CaretRight aria-hidden="true" size={12} />
                        </span>
                      )}
                    </button>
                  ))}
                </div>
                <Link
                  className="attention-map-link"
                  href={`/projects/${snapshot.project_id}/attention`}
                >
                  See all {openIssues.length} open issues in the Attention map
                  <ArrowRight aria-hidden="true" size={12} />
                </Link>
                {clarificationIssue ? (
                  <div className="clarification-pointer">
                    <Info aria-hidden="true" size={14} />
                    <span>
                      OSLO has <strong>{clarificationCount} things to confirm</strong> — open the
                      tied issue to answer.
                    </span>
                    <button
                      onClick={(event) =>
                        openIssue(clarificationIssue, event.currentTarget)
                      }
                      type="button"
                    >
                      Answer the first
                      <ArrowRight aria-hidden="true" size={12} />
                    </button>
                  </div>
                ) : null}
              </section>

              <section className="progress-read">
                <div className="overview-label">
                  <p>Progress</p>
                  <Info aria-hidden="true" size={14} />
                </div>
                <div className="progress-layout">
                  <div className="progress-numbers">
                    <div>
                      <strong>0</strong>
                      <span>issues resolved · {openIssues.length} open</span>
                    </div>
                    <div>
                      <strong className="critical-number">{criticalCount}</strong>
                      <span>critical issues open</span>
                    </div>
                  </div>
                  <div className="progress-bars">
                    <div>
                      <span>Dependencies confirmed</span>
                      <strong>0 / {clarificationCount}</strong>
                      <i><b style={{ width: "0%" }} /></i>
                    </div>
                    <div>
                      <span>Plan artifacts read</span>
                      <strong>{snapshot.artifacts.length} / 7</strong>
                      <i>
                        <b
                          style={{
                            width: `${Math.min(100, (snapshot.artifacts.length / 7) * 100)}%`,
                          }}
                        />
                      </i>
                    </div>
                  </div>
                </div>
              </section>

              <section className="project-summary" id="project-summary">
                <div className="summary-caption">
                  <strong>More</strong>
                  <span>optional — the read above is the summary</span>
                </div>
                <button
                  aria-label="Project summary"
                  aria-expanded={summaryOpen}
                  onClick={() => setSummaryOpen((current) => !current)}
                  type="button"
                >
                  <strong>Project summary</strong>
                  <span>{snapshot.summary}</span>
                  <CaretDown
                    aria-hidden="true"
                    className={summaryOpen ? "is-open" : ""}
                    size={13}
                  />
                </button>
                {summaryOpen ? <p>{snapshot.summary}</p> : null}
              </section>
            </>
          ) : (
            <AttentionView
              mode={attentionMode}
              onModeChange={setAttentionMode}
              onOpenIssue={openIssue}
              issues={openIssues}
            />
          )}
        </section>

        {selectedIssue ? (
          <IssuePanel
            analysisRunning={Boolean(analysisUpdateRunId)}
            answer={clarificationAnswer}
            error={clarificationError}
            issue={selectedIssue}
            onAnswerChange={setClarificationAnswer}
            onAsk={() => {
              closeIssue();
              setAdvisorOpen(true);
              void askQuestion(`Explain this issue: ${selectedIssue.title}`);
            }}
            onClose={closeIssue}
            onSubmit={submitClarification}
            pending={clarificationPending}
          />
        ) : advisorOpen ? (
          <AdvisorPanel
            advisorError={advisorError}
            advisorPending={advisorPending}
            advisorQuestions={advisorQuestions}
            extendedFailed={extendedFailed}
            extendedFailureMessage={extendedFailureMessage}
            extendedRetryError={extendedRetryError}
            extendedRetrying={extendedRetrying}
            isProvisional={isProvisional}
            messages={messages}
            onAsk={askQuestion}
            onClose={() => setAdvisorOpen(false)}
            onQuestionChange={setQuestion}
            onRetry={retryExtendedAnalysis}
            onSubmit={submitQuestion}
            question={question}
          />
        ) : null}
      </div>

      {!panelVisible ? (
        <button className="advisor-floating" onClick={() => setAdvisorOpen(true)} type="button">
          <Sparkle aria-hidden="true" size={14} weight="fill" />
          Ask OSLO
        </button>
      ) : null}

      <footer className="project-advisory">
        <Info aria-hidden="true" size={12} />
        OSLO advises; you decide — you stay in control at every step.
      </footer>

      {orientation ? (
        <section
          aria-label="How OSLO works"
          aria-modal="true"
          className="orientation-overlay"
          role="dialog"
        >
          <div className="orientation-pro">
            <h2>You bring the strategy. OSLO brings the understanding.</h2>
            <p>
              This is how you work as an AI-first PM — you stay in control at every step,
              with OSLO&apos;s understanding beside you.
            </p>
            <div className="orientation-cards">
              <article>
                <strong>Understanding</strong>
                <small>OSLO</small>
                <p>OSLO reads your plan and shows how sound it is — where it&apos;s clear, where it&apos;s weak, and what could derail the outcome.</p>
              </article>
              <article>
                <strong>Judgement</strong>
                <small>You</small>
                <p>You weigh what matters. OSLO surfaces the issues and options; the call is always yours.</p>
              </article>
              <article>
                <strong>Decision</strong>
                <small>You</small>
                <p>You commit the path. OSLO records it — it never decides for you.</p>
              </article>
              <article>
                <strong>Oversight</strong>
                <small>You</small>
                <p>As reality shifts, OSLO re-reads and updates the picture, so you can adjust and stay on course.</p>
              </article>
            </div>
            <div className="orientation-footer">
              <p>OSLO advises. You lead. That&apos;s how an AI-first PM steers to the outcome — augmented, not automated.</p>
              <button className="button button-primary" onClick={dismissOrientation} type="button">
                Get started
                <ArrowRight aria-hidden="true" size={14} />
              </button>
            </div>
          </div>
        </section>
      ) : null}
    </main>
  );
}

function AttentionView({
  issues,
  mode,
  onModeChange,
  onOpenIssue,
}: {
  issues: Issue[];
  mode: "heatmap" | "dimensions";
  onModeChange: (mode: "heatmap" | "dimensions") => void;
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
}) {
  return (
    <section className="attention-view">
      <div className="attention-heading">
        <div>
          <h1>Attention map</h1>
          <span>Where the plan needs work</span>
          <p>
            Brighter = more attention. Click a cell to investigate.
            <Info aria-hidden="true" size={13} />
          </p>
        </div>
        <div className="attention-toggle" role="group" aria-label="Attention view">
          <button
            aria-pressed={mode === "heatmap"}
            onClick={() => onModeChange("heatmap")}
            type="button"
          >
            Heatmap
          </button>
          <button
            aria-pressed={mode === "dimensions"}
            onClick={() => onModeChange("dimensions")}
            type="button"
          >
            Dimensions
          </button>
        </div>
      </div>

      {mode === "heatmap" ? (
        <div className="attention-matrix" role="grid" aria-label="Project attention map">
          <div className="matrix-corner">
            <span>Dimension →</span>
            <span>Section ↓</span>
          </div>
          {dimensions.map((dimension) => (
            <strong className="matrix-column" key={dimension}>
              {artifactLabel(dimension)}
            </strong>
          ))}
          {artifactOrder.map((artifact, rowIndex) => (
            <MatrixRow
              artifact={artifact}
              issues={issues}
              key={artifact}
              onOpenIssue={onOpenIssue}
              rowIndex={rowIndex}
            />
          ))}
          <div className="attention-legend">
            <span>Calm</span>
            <i className="legend-calm" />
            <i className="legend-warning" />
            <i className="legend-moderate" />
            <i className="legend-critical" />
            <span>Needs attention</span>
          </div>
          <p className="matrix-note">
            Rows = plan artifacts · columns = Clarity · Alignment · Feasibility.
          </p>
        </div>
      ) : (
        <div className="dimension-view">
          {dimensions.map((dimension) => {
            const dimensionIssues = issues.filter(
              (issue) => issue.dimension.toLowerCase() === dimension,
            );
            return (
              <section key={dimension}>
                <h2>{artifactLabel(dimension)}</h2>
                <span>{dimensionIssues.length} open</span>
                {dimensionIssues.length ? (
                  dimensionIssues.map((issue) => (
                    <button
                      key={issue.id}
                      onClick={(event) => onOpenIssue(issue, event.currentTarget)}
                      type="button"
                    >
                      <span className={`severity severity-${issue.severity.toLowerCase()}`}>
                        {issue.severity}
                      </span>
                      <strong>{issue.title}</strong>
                      <CaretRight aria-hidden="true" size={13} />
                    </button>
                  ))
                ) : (
                  <p>No current issues in this dimension.</p>
                )}
              </section>
            );
          })}
        </div>
      )}
    </section>
  );
}

function MatrixRow({
  artifact,
  issues,
  onOpenIssue,
  rowIndex,
}: {
  artifact: string;
  issues: Issue[];
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  rowIndex: number;
}) {
  const groupBreak = rowIndex === 0 ? "Understanding" : rowIndex === 4 ? "Execution" : null;
  return (
    <>
      {groupBreak ? <strong className="matrix-group">{groupBreak}</strong> : null}
      <span className="matrix-row-label">{artifactLabel(artifact)}</span>
      {dimensions.map((dimension) => {
        const cellIssues = issues
          .filter(
            (issue) =>
              issue.artifact_type === artifact &&
              issue.dimension.toLowerCase() === dimension,
          )
          .sort(issueSort);
        const highest = cellIssues[0]?.severity.toLowerCase() ?? "calm";
        return (
          <button
            aria-label={`${artifactLabel(artifact)} ${artifactLabel(dimension)}: ${
              cellIssues.length
            } issue${cellIssues.length === 1 ? "" : "s"}`}
            className={`attention-cell attention-cell-${highest}`}
            disabled={!cellIssues.length}
            key={dimension}
            onClick={(event) => onOpenIssue(cellIssues[0], event.currentTarget)}
            role="gridcell"
            type="button"
          >
            {cellIssues.length ? (
              <>
                <strong>{cellIssues.length}</strong>
                <span>{highest}</span>
              </>
            ) : (
              <span>·</span>
            )}
          </button>
        );
      })}
    </>
  );
}

function IssuePanel({
  analysisRunning,
  answer,
  error,
  issue,
  onAnswerChange,
  onAsk,
  onClose,
  onSubmit,
  pending,
}: {
  analysisRunning: boolean;
  answer: string;
  error: string | null;
  issue: Issue;
  onAnswerChange: (value: string) => void;
  onAsk: () => void;
  onClose: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  pending: boolean;
}) {
  return (
    <aside aria-label="Issue details" className="project-sidepanel issue-panel">
      <div className="issue-panel-heading">
        <div>
          <span className={`severity severity-${issue.severity.toLowerCase()}`}>
            {issue.severity}
          </span>
          <h2>{issue.title}</h2>
        </div>
        <button aria-label="Close issue" onClick={onClose} type="button">
          <X aria-hidden="true" size={20} />
        </button>
      </div>
      <p className="issue-meta">
        Dimension · {issue.dimension} &nbsp; Section · {artifactLabel(issue.artifact_type)}
        &nbsp; Type · Finding
      </p>
      <div className="issue-lifecycle" aria-label={`Issue status ${issue.status}`}>
        {["open", "addressed", "resolved"].map((status) => (
          <span className={status === issue.status ? "is-current" : ""} key={status}>
            {artifactLabel(status)}
          </span>
        ))}
      </div>
      <button className="ask-oslo-issue" onClick={onAsk} type="button">
        <Sparkle aria-hidden="true" size={12} weight="fill" />
        Ask OSLO about this issue
      </button>
      <section>
        <h3>Why this matters</h3>
        <p>{issue.why}</p>
      </section>
      <section>
        <h3>Evidence</h3>
        <div className="evidence-list">
          {issue.evidence_refs.map((reference) => (
            <div key={reference}>
              <small>{artifactLabel(issue.artifact_type)} · source</small>
              <p>{reference}</p>
            </div>
          ))}
        </div>
      </section>
      {issue.clarification ? (
        <form className="clarification-form" onSubmit={onSubmit}>
          <h3>Clarification request</h3>
          <strong>{issue.clarification}</strong>
          <textarea
            aria-label="Clarification answer"
            disabled={pending || analysisRunning}
            maxLength={5_000}
            onChange={(event) => onAnswerChange(event.target.value)}
            placeholder="Type your answer — OSLO will update your project info and re-run analysis…"
            value={answer}
          />
          <div>
            <p>OSLO asks; you answer; you decide. Answering re-runs analysis.</p>
            <button
              disabled={!answer.trim() || pending || analysisRunning}
              type="submit"
            >
              {analysisRunning ? "Re-analyzing…" : pending ? "Saving…" : "Submit & re-analyze"}
            </button>
          </div>
          {error ? <p className="clarification-error" role="alert">{error}</p> : null}
        </form>
      ) : null}
      <section>
        <h3>Suggested fixes</h3>
        <div className="suggested-fixes">
          <span><ArrowRight aria-hidden="true" size={12} />{issue.recommendation}</span>
          <span><ArrowRight aria-hidden="true" size={12} />Confirm an accountable owner and fallback.</span>
        </div>
      </section>
    </aside>
  );
}

function AdvisorPanel({
  advisorError,
  advisorPending,
  advisorQuestions,
  extendedFailed,
  extendedFailureMessage,
  extendedRetryError,
  extendedRetrying,
  isProvisional,
  messages,
  onAsk,
  onClose,
  onQuestionChange,
  onRetry,
  onSubmit,
  question,
}: {
  advisorError: string | null;
  advisorPending: boolean;
  advisorQuestions: string[];
  extendedFailed: boolean;
  extendedFailureMessage: string;
  extendedRetryError: string | null;
  extendedRetrying: boolean;
  isProvisional: boolean;
  messages: ChatMessage[];
  onAsk: (question: string) => Promise<void>;
  onClose: () => void;
  onQuestionChange: (question: string) => void;
  onRetry: () => Promise<void>;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  question: string;
}) {
  return (
    <aside aria-label="OSLO project advisor" className="project-sidepanel oslo-chat">
      <div className="chat-heading">
        <span aria-hidden="true">O</span>
        <div><strong>OSLO</strong><small>Project advisor</small></div>
        <button aria-label="Hide the OSLO panel" onClick={onClose} type="button">
          <CaretRight aria-hidden="true" size={16} />
        </button>
      </div>
      <div aria-live="polite" className="chat-content">
        <p className="chat-note">
          I&apos;ve completed the {isProvisional ? "initial" : "extended"} read. Start with
          the top issue, or ask about any part of the plan.
        </p>
        <div className="chat-completion-note">
          <strong>
            {extendedFailed
              ? "Extended Analysis paused safely"
              : extendedRetrying
                ? "Extended Analysis is retrying"
                : isProvisional
                  ? "Initial Analysis complete"
                  : "Extended Analysis complete"}
          </strong>
          <p>
            {extendedFailed
              ? extendedFailureMessage
              : isProvisional
                ? "Your provisional read is ready while the deeper evidence pass continues."
                : "The current read supersedes the provisional orientation."}
          </p>
          {extendedFailed ? (
            <button onClick={() => void onRetry()} type="button">Retry Extended Analysis</button>
          ) : null}
          {extendedRetryError ? <p className="chat-error" role="alert">{extendedRetryError}</p> : null}
        </div>
        <div className="chat-messages">
          {messages.map((message) => (
            <p className={`chat-message chat-message-${message.role}`} key={message.id}>
              {message.text}
            </p>
          ))}
          {advisorPending ? <p className="chat-thinking">OSLO is reviewing this project…</p> : null}
          {advisorError ? <p className="chat-error" role="alert">{advisorError}</p> : null}
        </div>
      </div>
      <div className="chat-bottom">
        <div className="chat-prompts">
          {advisorQuestions.map((prompt) => (
            <button
              disabled={advisorPending}
              key={prompt}
              onClick={() => void onAsk(prompt)}
              type="button"
            >
              {prompt}
            </button>
          ))}
        </div>
        <form className="chat-composer" onSubmit={onSubmit}>
          <input
            aria-label="Ask OSLO"
            disabled={advisorPending}
            maxLength={1000}
            onChange={(event) => onQuestionChange(event.target.value)}
            placeholder="Ask OSLO about the read, an issue, or what to do next…"
            value={question}
          />
          <button
            aria-label="Send"
            disabled={advisorPending || !question.trim()}
            type="submit"
          >
            <PaperPlaneTilt aria-hidden="true" size={15} weight="fill" />
          </button>
        </form>
        <p className="chat-advisory">OSLO advises; you decide.</p>
      </div>
    </aside>
  );
}

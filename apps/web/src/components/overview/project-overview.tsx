"use client";

import {
  ArrowRight,
  CaretDown,
  CaretRight,
  ChatTeardropDots,
  ClockCounterClockwise,
  FileText,
  FolderOpen,
  House,
  Info,
  ListBullets,
  MapTrifold,
  MagnifyingGlass,
  PaperPlaneTilt,
  Sparkle,
  X,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import type { FormEvent } from "react";

import type { OverviewSnapshot, ProjectHistory } from "@/lib/server/oslo-api";
import { ArtifactWorkspace } from "@/components/artifacts/artifact-workspace";
import { HistoryWorkspace } from "@/components/history/history-workspace";

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
const orientationSteps = [
  {
    title: "Your confidence read",
    body: "See how mature OSLO's understanding is, what limits it, and how reliable the supporting evidence is.",
  },
  {
    title: "What needs attention",
    body: "Start with the highest-impact open findings. OSLO explains the issue; you decide what to do.",
  },
  {
    title: "The Attention map",
    body: "Move from the summary into the seven plan artifacts across Clarity, Alignment, and Feasibility.",
  },
  {
    title: "Progress and evidence",
    body: "Track resolved findings, confirmed dependencies, and how much of the plan has been evidence-qualified.",
  },
  {
    title: "Your OSLO advisor",
    body: "Ask grounded questions about this project. The advisor reads the published snapshot and never changes it.",
  },
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
const dimensionDescriptions = {
  clarity: "How complete, explicit, and unambiguous the plan evidence is.",
  alignment: "Whether the objectives, scope, dependencies, and decisions agree.",
  feasibility: "Whether the schedule, resources, and dependencies support delivery.",
} as const;

type Issue = OverviewSnapshot["assessment"]["issues"][number];
type ArtifactView = (typeof artifactOrder)[number];
type ProjectView = "overview" | "attention" | "issues" | "history" | ArtifactView;

function isArtifactView(value: ProjectView): value is ArtifactView {
  return artifactOrder.includes(value as ArtifactView);
}

interface ChatMessage {
  id: number;
  role: "user" | "advisor";
  text: string;
}

interface AttentionScope {
  artifact?: string;
  dimension?: string;
}

function issueSort(left: Issue, right: Issue) {
  return (severityRank[right.severity] ?? 0) - (severityRank[left.severity] ?? 0);
}

function artifactLabel(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function issueResolutionMap(issues: Issue[]) {
  return Object.fromEntries(
    issues
      .filter((issue) => Boolean(issue.selected_resolution))
      .map((issue) => [issue.id, issue.selected_resolution as string]),
  );
}

export function ProjectOverview({
  initial,
  displayName,
  logoutAction,
  initialView = "overview",
  initialHistory,
}: {
  initial: OverviewSnapshot;
  displayName: string;
  logoutAction: () => Promise<void>;
  initialView?: ProjectView;
  initialHistory?: ProjectHistory;
}) {
  const router = useRouter();
  const [snapshot, setSnapshot] = useState(initial);
  const [orientation, setOrientation] = useState(false);
  const [tourStep, setTourStep] = useState<number | null>(null);
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(null);
  const [advisorOpen, setAdvisorOpen] = useState(true);
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [confidenceDetailsOpen, setConfidenceDetailsOpen] = useState(false);
  const [confidenceBreakdownOpen, setConfidenceBreakdownOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [attentionScope, setAttentionScope] = useState<AttentionScope | null>(null);
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
  const [issueActionPending, setIssueActionPending] = useState(false);
  const [issueActionError, setIssueActionError] = useState<string | null>(null);
  const [selectedResolutions, setSelectedResolutions] = useState<Record<string, string>>(
    () => issueResolutionMap(initial.assessment.issues),
  );
  const [analysisUpdateRunId, setAnalysisUpdateRunId] = useState<string | null>(() => {
    const activeExtended = initial.extended_analysis;
    return initial.state === "current" &&
      (activeExtended?.status === "queued" || activeExtended?.status === "running")
      ? activeExtended.run_id
      : null;
  });
  const advisorInFlight = useRef(false);
  const projectInFlight = useRef(false);
  const advisorStateBeforeIssue = useRef(true);
  const issueTrigger = useRef<HTMLElement | null>(null);
  const messageId = useRef(0);
  const clarificationIdempotency = useRef<{
    signature: string;
    key: string;
  } | null>(null);
  const issueActionIdempotency = useRef<{
    signature: string;
    key: string;
  } | null>(null);

  const isProvisional = snapshot.state === "provisional";
  const extendedRun = snapshot.extended_analysis;
  const extendedFailed =
    extendedRun?.status === "failed" && !extendedRetrying;
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
  const totalConfirmationCount =
    clarificationCount + snapshot.assessment.confirmed_dependency_count;
  const limitingDimension = snapshot.assessment.limiting_dimension;
  const overviewScrollKey = `oslo:overview-scroll:${snapshot.project_id}`;

  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const compact = window.matchMedia("(max-width: 980px)");
    const keepMainConsoleAvailable = (event: MediaQueryListEvent | MediaQueryList) => {
      if (event.matches) setAdvisorOpen(false);
    };
    keepMainConsoleAvailable(compact);
    compact.addEventListener("change", keepMainConsoleAvailable);
    return () => compact.removeEventListener("change", keepMainConsoleAvailable);
  }, []);

  useEffect(() => {
    const orientationTimer = window.setTimeout(
      () => setOrientation(!snapshot.orientation_seen),
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
        setSelectedResolutions(issueResolutionMap(next.assessment.issues));
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
  }, [
    extendedFailed,
    isProvisional,
    snapshot.orientation_seen,
    snapshot.project_id,
  ]);

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
          if (overviewResponse.ok) {
            const next: OverviewSnapshot = await overviewResponse.json();
            setSnapshot(next);
            setSelectedResolutions(issueResolutionMap(next.assessment.issues));
            setSelectedIssue((current) => {
              if (!current) return current;
              return (
                next.assessment.issues.find((issue) => issue.id === current.id) ??
                current
              );
            });
          }
          setExtendedRetrying(false);
          setAnalysisUpdateRunId(null);
          setClarificationAnswer("");
          clarificationIdempotency.current = null;
        }
        if (run.status === "failed") {
          const overviewResponse = await fetch(
            `/api/projects/${snapshot.project_id}/overview`,
            { cache: "no-store" },
          );
          if (overviewResponse.ok) {
            const next: OverviewSnapshot = await overviewResponse.json();
            setSnapshot(next);
            setSelectedResolutions(issueResolutionMap(next.assessment.issues));
          }
          setExtendedRetrying(false);
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
    const handleProjectShortcut = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setConfidenceBreakdownOpen(false);
        setSearchOpen(true);
      }
      if (event.key === "Escape") {
        setSearchOpen(false);
        setConfidenceBreakdownOpen(false);
      }
    };
    window.addEventListener("keydown", handleProjectShortcut);
    return () => window.removeEventListener("keydown", handleProjectShortcut);
  }, []);

  useEffect(() => {
    if (!selectedIssue && !attentionScope) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        if (selectedIssue && attentionScope) {
          setSelectedIssue(null);
        } else {
          setSelectedIssue(null);
          setAttentionScope(null);
          setAdvisorOpen(advisorStateBeforeIssue.current);
          window.setTimeout(() => issueTrigger.current?.focus(), 0);
        }
        return;
      }
      if (event.key === "Tab") {
        const panel = document.querySelector<HTMLElement>(
          '[role="dialog"][aria-label="Issue details"], [role="dialog"][aria-label="Scoped attention findings"]',
        );
        const focusable = panel?.querySelectorAll<HTMLElement>(
          'button:not([disabled]), textarea:not([disabled]), input:not([disabled]), a[href]',
        );
        if (!focusable?.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [attentionScope, selectedIssue]);

  useEffect(() => {
    if (initialView !== "overview") return;
    const savedPosition = window.sessionStorage.getItem(overviewScrollKey);
    if (!savedPosition) return;
    const top = Number(savedPosition);
    if (!Number.isFinite(top)) return;
    const restorePosition = () => {
      window.scrollTo({ behavior: "auto", top });
    };
    const restore = window.requestAnimationFrame(restorePosition);
    const layoutRetry = window.setTimeout(restorePosition, 100);
    const hydrationRetry = window.setTimeout(() => {
      restorePosition();
      window.sessionStorage.removeItem(overviewScrollKey);
    }, 300);
    return () => {
      window.cancelAnimationFrame(restore);
      window.clearTimeout(layoutRetry);
      window.clearTimeout(hydrationRetry);
    };
  }, [initialView, overviewScrollKey]);

  const dismissOrientation = async () => {
    localStorage.setItem("oslo_orientation_seen", "true");
    setSnapshot((current) => ({ ...current, orientation_seen: true }));
    setOrientation(false);
    setTourStep(null);
    await fetch("/api/orientation", { method: "POST" }).catch(() => undefined);
  };

  const openIssue = (issue: Issue, trigger?: HTMLElement | null) => {
    if (!attentionScope) {
      advisorStateBeforeIssue.current = advisorOpen;
    }
    issueTrigger.current = trigger ?? (document.activeElement as HTMLElement | null);
    setAdvisorOpen(false);
    setSelectedIssue(issue);
    setClarificationAnswer("");
    setClarificationError(null);
  };

  const closeIssue = () => {
    setSelectedIssue(null);
    if (!attentionScope) {
      setAdvisorOpen(advisorStateBeforeIssue.current);
      window.setTimeout(() => issueTrigger.current?.focus(), 0);
    }
  };

  const openAttentionScope = (
    scope: AttentionScope,
    trigger?: HTMLElement | null,
  ) => {
    advisorStateBeforeIssue.current = advisorOpen;
    issueTrigger.current = trigger ?? (document.activeElement as HTMLElement | null);
    setSelectedIssue(null);
    setAdvisorOpen(false);
    setAttentionScope(scope);
  };

  const closeAttentionScope = () => {
    setSelectedIssue(null);
    setAttentionScope(null);
    setAdvisorOpen(advisorStateBeforeIssue.current);
    window.setTimeout(() => issueTrigger.current?.focus(), 0);
  };

  const rememberOverviewPosition = () => {
    if (initialView !== "overview") return;
    window.sessionStorage.setItem(overviewScrollKey, String(window.scrollY));
  };

  const askQuestion = async (value: string, historyRunId?: string) => {
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
        body: JSON.stringify({ question: normalized, historyRunId }),
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
      setAnalysisUpdateRunId(extendedRun.run_id);
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
    const normalizedAnswer = clarificationAnswer.trim();
    const signature = `${selectedIssue.id}:${normalizedAnswer}`;
    if (clarificationIdempotency.current?.signature !== signature) {
      clarificationIdempotency.current = {
        signature,
        key: crypto.randomUUID(),
      };
    }
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/issues/${encodeURIComponent(selectedIssue.id)}/answers`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            answer: normalizedAnswer,
            idempotencyKey: clarificationIdempotency.current.key,
          }),
        },
      );
      if (!response.ok) throw new Error("answer was not accepted");
      const result = await response.json();
      setSelectedIssue((current) =>
        current ? { ...current, status: "addressed" } : current,
      );
      setAnalysisUpdateRunId(result.run_id);
    } catch {
      setClarificationError("Your answer could not be saved. Please try again.");
    } finally {
      setClarificationPending(false);
    }
  };

  const actOnIssue = async (
    action: "select" | "apply" | "custom",
    resolution: string,
  ) => {
    if (!selectedIssue || !resolution.trim() || issueActionPending) return;
    const normalizedResolution = resolution.trim();
    const signature = `${selectedIssue.id}:${action}:${normalizedResolution}`;
    if (issueActionIdempotency.current?.signature !== signature) {
      issueActionIdempotency.current = {
        signature,
        key: crypto.randomUUID(),
      };
    }
    setIssueActionPending(true);
    setIssueActionError(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/issues/${encodeURIComponent(selectedIssue.id)}/actions`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            action,
            resolution: normalizedResolution,
            idempotencyKey: issueActionIdempotency.current.key,
          }),
        },
      );
      if (!response.ok) throw new Error("issue action was not accepted");
      const result = await response.json();
      setSelectedResolutions((current) => ({
        ...current,
        [selectedIssue.id]: result.selected_resolution,
      }));
      setSelectedIssue((current) =>
        current ? { ...current, status: "addressed" } : current,
      );
      setSnapshot((current) => ({
        ...current,
        assessment: {
          ...current.assessment,
          issues: current.assessment.issues.map((issue) =>
            issue.id === selectedIssue.id
              ? {
                  ...issue,
                  status: "addressed",
                  selected_resolution: result.selected_resolution,
                }
              : issue,
          ),
        },
      }));
      if (result.analysis_run?.run_id) {
        setAnalysisUpdateRunId(result.analysis_run.run_id);
      }
    } catch {
      setIssueActionError("The resolution could not be saved. Please try again.");
    } finally {
      setIssueActionPending(false);
    }
  };

  const extendedFailureMessage =
    extendedRun?.error_code === "EVIDENCE_REFERENCE_CONTRACT_FAILED"
      ? "An evidence reference did not match the source document."
      : "The deeper read stopped before it could safely publish.";

  const panelVisible = advisorOpen || Boolean(selectedIssue) || Boolean(attentionScope);

  return (
    <main
      className={`project-shell ${
        selectedIssue || attentionScope ? "has-issue" : ""
      }`}
    >
      <header className="project-header">
        <Link className="project-toolbar-brand" href={`/projects/${snapshot.project_id}/overview`}>
          <span aria-hidden="true">I</span>
          <strong>Intralign</strong>
        </Link>
        <div className="project-context">
          <strong>Project understanding</strong>
          <span aria-hidden="true">›</span>
          <em>{initialView === "attention" ? "Attention map" : artifactLabel(initialView)}</em>
        </div>
        <button
          aria-label={`Confidence ${snapshot.assessment.confidence_index}, ${snapshot.assessment.confidence_band}, ${snapshot.assessment.reliability} reliability`}
          aria-expanded={confidenceBreakdownOpen}
          className="project-header-confidence"
          onClick={() => {
            setSearchOpen(false);
            setConfidenceBreakdownOpen((current) => !current);
          }}
          type="button"
        >
          <span>Confidence</span>
          <strong>{snapshot.assessment.confidence_index}</strong>
          <span>{snapshot.assessment.confidence_band}</span>
          <small>{snapshot.assessment.reliability} reliability</small>
        </button>
        <div className="project-actions">
          <button
            aria-label="Search project"
            className="project-search-button"
            onClick={() => {
              setConfidenceBreakdownOpen(false);
              setSearchOpen(true);
            }}
            type="button"
          >
            <MagnifyingGlass aria-hidden="true" size={16} />
          </button>
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
                  setTourStep(null);
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

      {confidenceBreakdownOpen ? (
        <ConfidenceBreakdown
          assessment={snapshot.assessment}
          onClose={() => setConfidenceBreakdownOpen(false)}
        />
      ) : null}

      <aside className="workspace-sidebar">
        <p className="workspace-label">Project</p>
        <nav aria-label="Workspace">
          <Link
            className={initialView === "overview" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/overview`}
          >
            <House aria-hidden="true" size={17} />
            Overview
          </Link>
          <Link
            aria-label={`Issues ${openIssues.length}`}
            className={initialView === "issues" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/issues`}
          >
            <ListBullets aria-hidden="true" size={17} />
            Issues
            <span className="nav-count">{openIssues.length}</span>
          </Link>
          <Link
            className={initialView === "history" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/history`}
          >
            <ClockCounterClockwise aria-hidden="true" size={17} />
            History
          </Link>
          <Link
            className={initialView === "attention" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/attention`}
            onClick={rememberOverviewPosition}
          >
            <MapTrifold aria-hidden="true" size={17} />
            Attention map
            {openIssues.length ? <span className="nav-count">{openIssues.length}</span> : null}
          </Link>
        </nav>
        <p className="workspace-label workspace-artifact-label">Plan artifacts</p>
        <div className="workspace-artifact-group">
          <span>Understanding</span>
          {artifactOrder.slice(0, 4).map((artifactType) => {
            const count = openIssues.filter(
              (issue) => issue.artifact_type === artifactType,
            ).length;
            return (
              <Link
                className={initialView === artifactType ? "is-current" : ""}
                href={`/projects/${snapshot.project_id}/artifacts/${artifactType}`}
                key={artifactType}
              >
                <FileText aria-hidden="true" size={15} />
                {artifactLabel(artifactType)}
                {count ? <span className="nav-count">{count}</span> : null}
              </Link>
            );
          })}
          <span>Execution</span>
          {artifactOrder.slice(4).map((artifactType) => {
            const count = openIssues.filter(
              (issue) => issue.artifact_type === artifactType,
            ).length;
            return (
              <Link
                className={initialView === artifactType ? "is-current" : ""}
                href={`/projects/${snapshot.project_id}/artifacts/${artifactType}`}
                key={artifactType}
              >
                <FileText aria-hidden="true" size={15} />
                {artifactLabel(artifactType)}
                {count ? <span className="nav-count">{count}</span> : null}
              </Link>
            );
          })}
        </div>
        <div className="workspace-future" aria-label="Planned capabilities">
          <p>Coming in later slices</p>
          <span><FolderOpen aria-hidden="true" size={15} /> Reports</span>
          <span>Share &amp; export</span>
        </div>
        <div className="workspace-sidebar-footer">
          <button
            onClick={() => {
              setTourStep(null);
              setOrientation(true);
            }}
            type="button"
          >
            <Sparkle aria-hidden="true" size={15} />
            Take a quick tour
          </button>
          <span>OSLO advises; you decide.</span>
        </div>
      </aside>

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
                    <div className="confidence-stage">
                      <span>Stage</span>
                      {(["orientation", "expanded", "validated"] as const).map(
                        (stage, index) => (
                          <Fragment key={stage}>
                            <strong
                              className={
                                snapshot.assessment.understanding_stage === stage
                                  ? "is-active"
                                  : ""
                              }
                            >
                              {artifactLabel(stage)}
                            </strong>
                            {index < 2 ? <i>›</i> : null}
                          </Fragment>
                        ),
                      )}
                    </div>
                    <h1>Understanding is forming</h1>
                    <p>
                      {snapshot.assessment.confidence_band} · qualified by{" "}
                      <strong>{snapshot.assessment.reliability.toLowerCase()} reliability</strong>
                    </p>
                    <div className="confidence-statusline">
                      <span>{artifactLabel(snapshot.assessment.confidence_direction)}</span>
                      {!isProvisional ? <span>Current evidence-qualified read</span> : null}
                    </div>
                  </div>
                </div>
                {snapshot.assessment.false_confidence ? (
                  <div className="false-confidence-warning" role="alert">
                    <Info aria-hidden="true" size={15} />
                    The score is high, but the supporting evidence is not yet reliable enough
                    for a confident commitment.
                  </div>
                ) : null}
                <div className="confidence-divider" />
                <div className="dimension-help">
                  <p>What&apos;s driving it — hover or focus a dimension for detail</p>
                  <button
                    aria-expanded={confidenceDetailsOpen}
                    aria-label="How confidence is calculated"
                    onClick={() => setConfidenceDetailsOpen((current) => !current)}
                    type="button"
                  >
                    <Info aria-hidden="true" size={13} />
                    How calculated
                  </button>
                </div>
                {confidenceDetailsOpen ? (
                  <section className="confidence-method" aria-label="Confidence calculation">
                    <p>{snapshot.assessment.confidence_explanation}</p>
                    <dl>
                      <div>
                        <dt>Coverage</dt>
                        <dd>{snapshot.assessment.reliability_basis.coverage}</dd>
                      </div>
                      <div>
                        <dt>Evidence</dt>
                        <dd>{snapshot.assessment.reliability_basis.evidence}</dd>
                      </div>
                      <div>
                        <dt>Assessability</dt>
                        <dd>{snapshot.assessment.reliability_basis.assessability}</dd>
                      </div>
                    </dl>
                  </section>
                ) : null}
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
                          <span className="dimension-tooltip" role="tooltip">
                            <strong>{artifactLabel(name)} · {value}</strong>
                            {dimensionDescriptions[name]}
                          </span>
                        </div>
                        <strong>{value}</strong>
                      </div>
                    );
                  })}
                </div>
                <div className="confidence-footer">
                  <span>
                    <strong>{openIssues.length}</strong> issues open ·{" "}
                    <strong>{snapshot.assessment.resolved_issue_count}</strong> resolved
                  </span>
                  <div>
                    <button
                      aria-expanded={confidenceDetailsOpen}
                      aria-label="Why this confidence read"
                      onClick={() => setConfidenceDetailsOpen((current) => !current)}
                      type="button"
                    >
                      Why <CaretDown aria-hidden="true" size={11} />
                    </button>
                    <Link
                      aria-label="Timeline"
                      href={`/projects/${snapshot.project_id}/attention`}
                      onClick={rememberOverviewPosition}
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
                  onClick={rememberOverviewPosition}
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
                      <strong>{snapshot.assessment.resolved_issue_count}</strong>
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
                      <strong>
                        {snapshot.assessment.confirmed_dependency_count} / {totalConfirmationCount}
                      </strong>
                      <i>
                        <b
                          style={{
                            width: totalConfirmationCount
                              ? `${Math.min(
                                  100,
                                  (snapshot.assessment.confirmed_dependency_count /
                                    totalConfirmationCount) *
                                    100,
                                )}%`
                              : "100%",
                          }}
                        />
                      </i>
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
          ) : initialView === "attention" ? (
            <AttentionView
              onAskOslo={(scope) => {
                const focus = [scope.artifact, scope.dimension]
                  .filter((value): value is string => Boolean(value))
                  .map(artifactLabel)
                  .join(" × ");
                setAttentionScope(null);
                setAdvisorOpen(true);
                void askQuestion(
                  focus
                    ? `Explain why ${focus} needs attention in the current published read.`
                    : "Explain the Attention map and what I should address first.",
                );
              }}
              onOpenIssue={openIssue}
              onOpenScope={openAttentionScope}
              issues={openIssues}
            />
          ) : isArtifactView(initialView) ? (
            <ArtifactWorkspace
              analysisRunning={Boolean(analysisUpdateRunId)}
              artifactType={initialView}
              onAnalysisStarted={setAnalysisUpdateRunId}
              onAskOslo={(prompt) => {
                setAdvisorOpen(true);
                void askQuestion(prompt);
              }}
              onOpenIssue={openIssue}
              projectId={snapshot.project_id}
            />
          ) : initialView === "issues" ? (
            <IssuesWorkspace
              issues={snapshot.assessment.issues}
              onOpenIssue={openIssue}
            />
          ) : initialView === "history" && initialHistory ? (
            <HistoryWorkspace
              history={initialHistory}
              onAskOslo={(runId, prompt) => {
                setAdvisorOpen(true);
                void askQuestion(prompt, runId);
              }}
              projectId={snapshot.project_id}
            />
          ) : (
            <DeferredWorkspace />
          )}
        </section>

        {selectedIssue ? (
          <IssuePanel
            analysisRunning={Boolean(analysisUpdateRunId)}
            answer={clarificationAnswer}
            error={clarificationError ?? issueActionError}
            issue={selectedIssue}
            onAnswerChange={setClarificationAnswer}
            onAsk={() => {
              closeIssue();
              setAdvisorOpen(true);
              void askQuestion(`Explain this issue: ${selectedIssue.title}`);
            }}
            onClose={closeIssue}
            onIssueAction={actOnIssue}
            onSubmit={submitClarification}
            pending={clarificationPending || issueActionPending}
            selectedResolution={selectedResolutions[selectedIssue.id] ?? null}
          />
        ) : attentionScope ? (
          <AttentionScopePanel
            issues={openIssues}
            onAsk={() => {
              const focus = [attentionScope.artifact, attentionScope.dimension]
                .filter((value): value is string => Boolean(value))
                .map(artifactLabel)
                .join(" × ");
              setAttentionScope(null);
              setAdvisorOpen(true);
              void askQuestion(
                `Explain the ${focus} findings and what I should address first.`,
              );
            }}
            onClearArtifact={() => {
              if (!attentionScope.dimension) {
                closeAttentionScope();
                return;
              }
              setAttentionScope({ dimension: attentionScope.dimension });
            }}
            onClearDimension={() => {
              if (!attentionScope.artifact) {
                closeAttentionScope();
                return;
              }
              setAttentionScope({ artifact: attentionScope.artifact });
            }}
            onClose={closeAttentionScope}
            onOpenIssue={openIssue}
            scope={attentionScope}
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
          {tourStep === null ? (
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
                <button
                  className="button button-primary"
                  onClick={() => setTourStep(0)}
                  type="button"
                >
                  Get started
                  <ArrowRight aria-hidden="true" size={14} />
                </button>
              </div>
            </div>
          ) : (
            <div className="tour-card">
              <div className="tour-progress">
                <span>{tourStep + 1} of {orientationSteps.length}</span>
                <div>
                  {orientationSteps.map((step, index) => (
                    <i className={index <= tourStep ? "is-active" : ""} key={step.title} />
                  ))}
                </div>
              </div>
              <Sparkle aria-hidden="true" size={24} weight="fill" />
              <h2>{orientationSteps[tourStep].title}</h2>
              <p>{orientationSteps[tourStep].body}</p>
              <div className="tour-actions">
                <button onClick={() => void dismissOrientation()} type="button">Skip tour</button>
                <button
                  className="button button-primary"
                  onClick={() => {
                    if (tourStep === orientationSteps.length - 1) {
                      void dismissOrientation();
                    } else {
                      setTourStep((current) => (current ?? 0) + 1);
                    }
                  }}
                  type="button"
                >
                  {tourStep === orientationSteps.length - 1 ? "Finish tour" : "Next"}
                  <ArrowRight aria-hidden="true" size={14} />
                </button>
              </div>
            </div>
          )}
        </section>
      ) : null}

      {searchOpen ? (
        <SearchPalette
          issues={openIssues}
          onClose={() => {
            setSearchOpen(false);
            setSearchQuery("");
          }}
          onOpenIssue={(issue) => {
            setSearchOpen(false);
            setSearchQuery("");
            openIssue(issue);
          }}
          projectId={snapshot.project_id}
          query={searchQuery}
          setQuery={setSearchQuery}
        />
      ) : null}
    </main>
  );
}

function ConfidenceBreakdown({
  assessment,
  onClose,
}: {
  assessment: OverviewSnapshot["assessment"];
  onClose: () => void;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    closeButton.current?.focus();
  }, []);

  return (
    <section
      aria-label="Confidence breakdown"
      className="confidence-breakdown"
      role="dialog"
    >
      <div className="confidence-breakdown-heading">
        <div>
          <span>Confidence</span>
          <strong>{assessment.confidence_index}</strong>
          <em>{assessment.confidence_band}</em>
        </div>
        <button aria-label="Close confidence breakdown" onClick={onClose} ref={closeButton} type="button">
          <X aria-hidden="true" size={16} />
        </button>
      </div>
      <p>
        Understanding maturity — not project health, readiness, or probability.
        Qualified by <strong>{assessment.reliability.toLowerCase()} reliability</strong>.
      </p>
      <dl className="confidence-breakdown-dimensions">
        {dimensions.map((name) => (
          <div key={name}>
            <dt>{artifactLabel(name)}</dt>
            <dd>
              <i><b style={{ width: `${dimensionStrength[assessment[name]] ?? 50}%` }} /></i>
              <strong>{assessment[name]}</strong>
            </dd>
          </div>
        ))}
      </dl>
      <h3>Reliability basis</h3>
      <dl className="confidence-breakdown-reliability">
        {(["coverage", "evidence", "assessability"] as const).map((name) => (
          <div key={name}>
            <dt>{artifactLabel(name)}</dt>
            <dd>{assessment.reliability_basis[name]}</dd>
          </div>
        ))}
      </dl>
      <small>{assessment.confidence_explanation}</small>
    </section>
  );
}

function SearchPalette({
  issues,
  onClose,
  onOpenIssue,
  projectId,
  query,
  setQuery,
}: {
  issues: Issue[];
  onClose: () => void;
  onOpenIssue: (issue: Issue) => void;
  projectId: string;
  query: string;
  setQuery: (value: string) => void;
}) {
  const router = useRouter();
  const input = useRef<HTMLInputElement>(null);
  const normalizedQuery = query.trim().toLowerCase();
  const routes: ReadonlyArray<readonly [string, string, string]> = [
    ["Overview", "overview", "Project workspace"],
    ["Issues", "issues", "Project workspace"],
    ["History", "history", "Project workspace"],
    ["Attention map", "attention", "Project workspace"],
    ...artifactOrder.map(
      (artifactType) =>
        [
          artifactLabel(artifactType),
          `artifacts/${artifactType}`,
          "Plan artifact",
        ] as const,
    ),
  ];
  const filteredRoutes = routes.filter(([label]) =>
    label.toLowerCase().includes(normalizedQuery),
  );
  const filteredIssues = issues.filter((issue) =>
    `${issue.title} ${issue.dimension} ${issue.artifact_type}`
      .toLowerCase()
      .includes(normalizedQuery),
  );

  useEffect(() => {
    input.current?.focus();
  }, []);

  return (
    <section
      aria-label="Search or jump to"
      aria-modal="true"
      className="project-search-overlay"
      onMouseDown={(event) => {
        if (event.currentTarget === event.target) onClose();
      }}
      role="dialog"
    >
      <div className="project-search-palette">
        <label>
          <MagnifyingGlass aria-hidden="true" size={16} />
          <input
            aria-label="Search project"
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search or jump to…"
            ref={input}
            value={query}
          />
          <kbd>Esc</kbd>
        </label>
        <div className="project-search-results" role="listbox">
          {filteredRoutes.length ? <p>Go to</p> : null}
          {filteredRoutes.map(([label, route, category]) => (
            <button
              aria-label={label}
              aria-selected="false"
              key={route}
              onClick={() => {
                onClose();
                router.push(`/projects/${projectId}/${route}`);
              }}
              role="option"
              type="button"
            >
              <span>{label}</span>
              <small>{category}</small>
            </button>
          ))}
          {filteredIssues.length ? <p>Open an issue</p> : null}
          {filteredIssues.map((issue) => (
            <button
              aria-label={issue.title}
              aria-selected="false"
              key={issue.id}
              onClick={() => onOpenIssue(issue)}
              role="option"
              type="button"
            >
              <span>{issue.title}</span>
              <small>{issue.severity} · {artifactLabel(issue.artifact_type)}</small>
            </button>
          ))}
          {!filteredRoutes.length && !filteredIssues.length ? (
            <p className="project-search-empty">No matching project content.</p>
          ) : null}
        </div>
      </div>
    </section>
  );
}

function DeferredWorkspace() {
  return (
    <section className="deferred-workspace">
      <span className="eyebrow">Project workspace</span>
      <h1>History</h1>
      <p>
        The current and last-good reads are already preserved safely. The full decision
        history arrives in Slice 7.
      </p>
      <Link href="./overview">
        Return to Overview
        <ArrowRight aria-hidden="true" size={13} />
      </Link>
      <div className="deferred-preview" aria-hidden="true">
        <i />
        <i />
        <i />
      </div>
    </section>
  );
}

type IssueGroupMode = "dimension" | "severity" | "artifact";

function IssuesWorkspace({
  issues,
  onOpenIssue,
}: {
  issues: Issue[];
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
}) {
  const [groupMode, setGroupMode] = useState<IssueGroupMode>("dimension");
  const [artifactFilter, setArtifactFilter] = useState<string | null>(null);
  const [dimensionFilter, setDimensionFilter] = useState<string | null>(null);
  const [severityFilter, setSeverityFilter] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("active");

  const filteredIssues = useMemo(
    () =>
      issues
        .filter((issue) => {
          if (artifactFilter && issue.artifact_type !== artifactFilter) return false;
          if (
            dimensionFilter &&
            issue.dimension.toLowerCase() !== dimensionFilter.toLowerCase()
          ) {
            return false;
          }
          if (severityFilter && issue.severity !== severityFilter) return false;
          if (statusFilter === "active") return issue.status !== "resolved";
          if (statusFilter !== "all" && issue.status !== statusFilter) return false;
          return true;
        })
        .sort(issueSort),
    [artifactFilter, dimensionFilter, issues, severityFilter, statusFilter],
  );

  const groups = useMemo(() => {
    const grouped = new Map<string, Issue[]>();
    for (const issue of filteredIssues) {
      const key =
        groupMode === "artifact"
          ? artifactLabel(issue.artifact_type)
          : groupMode === "severity"
            ? issue.severity
            : issue.dimension;
      grouped.set(key, [...(grouped.get(key) ?? []), issue]);
    }
    const order =
      groupMode === "dimension"
        ? ["Feasibility", "Clarity", "Alignment"]
        : groupMode === "severity"
          ? ["Critical", "Moderate", "Warning"]
          : artifactOrder.map(artifactLabel);
    return [...grouped.entries()].sort(
      ([left], [right]) => order.indexOf(left) - order.indexOf(right),
    );
  }, [filteredIssues, groupMode]);

  const activeCount = issues.filter((issue) => issue.status !== "resolved").length;
  const hiddenCount = Math.max(0, issues.length - filteredIssues.length);
  const hasExplicitFilters = Boolean(
    artifactFilter ||
      dimensionFilter ||
      severityFilter ||
      statusFilter !== "active",
  );

  function clearFilters() {
    setArtifactFilter(null);
    setDimensionFilter(null);
    setSeverityFilter(null);
    setStatusFilter("active");
  }

  return (
    <section className="issues-workspace">
      <header className="issues-heading">
        <div>
          <h1>Issues</h1>
          <p>What needs your attention</p>
        </div>
        <strong>
          {activeCount} active {activeCount === 1 ? "finding" : "findings"}
        </strong>
      </header>

      <div aria-label="Issue grouping" className="issue-group-tabs">
        {(["dimension", "severity", "artifact"] as const).map((mode) => (
          <button
            aria-pressed={groupMode === mode}
            key={mode}
            onClick={() => setGroupMode(mode)}
            type="button"
          >
            By {mode}
          </button>
        ))}
      </div>

      <section aria-label="Issue filters" className="issue-filter-panel">
        <IssueFilterRow
          active={artifactFilter}
          label="Artifact"
          onChange={setArtifactFilter}
          options={artifactOrder
            .map((artifact) => ({
              label: artifactLabel(artifact),
              value: artifact,
              count: issues.filter((issue) => issue.artifact_type === artifact).length,
            }))
            .filter((option) => option.count)}
        />
        <IssueFilterRow
          active={dimensionFilter}
          label="Dimension"
          onChange={setDimensionFilter}
          options={dimensions.map((dimension) => ({
            label: artifactLabel(dimension),
            value: dimension,
            count: issues.filter(
              (issue) => issue.dimension.toLowerCase() === dimension,
            ).length,
          }))}
        />
        <IssueFilterRow
          active={severityFilter}
          label="Severity"
          onChange={setSeverityFilter}
          options={["Critical", "Moderate", "Warning"].map((severity) => ({
            label: severity,
            value: severity,
            count: issues.filter((issue) => issue.severity === severity).length,
          }))}
        />
        <div className="issue-filter-row">
          <span>Status</span>
          {[
            ["Active", "active"],
            ["Open", "open"],
            ["Addressed", "addressed"],
            ["Resolved", "resolved"],
            ["All", "all"],
          ].map(([label, value]) => (
            <button
              aria-pressed={statusFilter === value}
              key={value}
              onClick={() => setStatusFilter(value)}
              type="button"
            >
              {label}
            </button>
          ))}
        </div>
      </section>

      {hiddenCount ? (
        <div className="issue-filter-summary" role="status">
          <span>
            {hiddenCount} {hiddenCount === 1 ? "finding" : "findings"} hidden by the
            current filters.
          </span>
          <button onClick={clearFilters} type="button">Clear filters</button>
        </div>
      ) : null}

      {groups.length ? (
        <div className="issue-groups">
          {groups.map(([group, groupIssues]) => (
            <section className="issue-group" key={group}>
              <h2>{group} · {groupIssues.length}</h2>
              <div>
                {groupIssues.map((issue) => (
                  <button
                    aria-label={`${issue.title}, ${issue.severity}, ${artifactLabel(issue.artifact_type)}, ${issue.dimension}, ${artifactLabel(issue.status)}`}
                    className={`issue-workspace-card issue-card-${issue.severity.toLowerCase()}`}
                    key={issue.id}
                    onClick={(event) => onOpenIssue(issue, event.currentTarget)}
                    type="button"
                  >
                    <i aria-hidden="true" />
                    <span>
                      <strong>{issue.title}</strong>
                      <small>
                        <b className={`severity severity-${issue.severity.toLowerCase()}`}>
                          {issue.severity}
                        </b>
                        {artifactLabel(issue.artifact_type)} · {issue.dimension}
                        <em>{artifactLabel(issue.status)}</em>
                        {issue.clarification ? <mark>Clarification</mark> : null}
                      </small>
                    </span>
                    <CaretRight aria-hidden="true" size={15} />
                  </button>
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <div className="issues-empty" role="status">
          <Sparkle aria-hidden="true" size={22} weight="fill" />
          <h2>
            {issues.length && hasExplicitFilters
              ? "No issues match this lens."
              : "Nothing needs your attention right now."}
          </h2>
          <p>
            {issues.length && hasExplicitFilters
              ? "Try another filter or return to all active findings."
              : "All seven plan artifacts are clear in the current read."}
          </p>
          {hasExplicitFilters ? (
            <button onClick={clearFilters} type="button">Clear filters</button>
          ) : null}
        </div>
      )}
    </section>
  );
}

function IssueFilterRow({
  active,
  label,
  onChange,
  options,
}: {
  active: string | null;
  label: string;
  onChange: (value: string | null) => void;
  options: Array<{ label: string; value: string; count: number }>;
}) {
  return (
    <div className="issue-filter-row">
      <span>{label}</span>
      <button
        aria-pressed={!active}
        onClick={() => onChange(null)}
        type="button"
      >
        All
      </button>
      {options.map((option) => (
        <button
          aria-label={`${option.label} ${option.count}`}
          aria-pressed={active === option.value}
          key={option.value}
          onClick={() => onChange(active === option.value ? null : option.value)}
          type="button"
        >
          {option.label} <small>{option.count}</small>
        </button>
      ))}
    </div>
  );
}

function AttentionView({
  issues,
  onAskOslo,
  onOpenIssue,
  onOpenScope,
}: {
  issues: Issue[];
  onAskOslo: (scope: AttentionScope) => void;
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  onOpenScope: (scope: AttentionScope, trigger?: HTMLElement | null) => void;
}) {
  return (
    <section className="attention-view">
      <div className="attention-heading">
        <div>
          <div className="attention-title">
            <h1>Attention map</h1>
            <span>Where the plan needs work</span>
          </div>
          <p>
            Brighter = more attention — not a health score. Click a cell to
            investigate.
          </p>
        </div>
        <button className="attention-ask" onClick={() => onAskOslo({})} type="button">
          <Sparkle aria-hidden="true" size={12} weight="fill" />
          Ask OSLO about this map
        </button>
      </div>

      {issues.length ? (
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
              onAskOslo={onAskOslo}
              onOpenIssue={onOpenIssue}
              onOpenScope={onOpenScope}
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
        <div className="attention-all-clear" role="status">
          <span>
            <Sparkle aria-hidden="true" size={20} weight="fill" />
          </span>
          <div>
            <h2>Nothing needs your attention right now.</h2>
            <p>All seven plan artifacts are clear in the current read.</p>
          </div>
        </div>
      )}
    </section>
  );
}

function MatrixRow({
  artifact,
  issues,
  onAskOslo,
  onOpenIssue,
  onOpenScope,
  rowIndex,
}: {
  artifact: string;
  issues: Issue[];
  onAskOslo: (scope: AttentionScope) => void;
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  onOpenScope: (scope: AttentionScope, trigger?: HTMLElement | null) => void;
  rowIndex: number;
}) {
  const groupBreak = rowIndex === 0 ? "Understanding" : rowIndex === 4 ? "Execution" : null;

  return (
    <>
      {groupBreak ? <strong className="matrix-group">{groupBreak}</strong> : null}
      <button
        aria-label={`Open ${artifactLabel(artifact)} findings`}
        className="matrix-row-label matrix-row-button"
        onClick={(event) => onOpenScope({ artifact }, event.currentTarget)}
        type="button"
      >
        {artifactLabel(artifact)}
        <CaretRight aria-hidden="true" size={12} />
      </button>
      {dimensions.map((dimension) => {
        const cellIssues = issues
          .filter(
            (issue) =>
              issue.artifact_type === artifact &&
              issue.dimension.toLowerCase() === dimension,
          )
          .sort(issueSort);
        const highest = cellIssues[0]?.severity.toLowerCase() ?? "calm";
        const label = `${artifactLabel(artifact)} ${artifactLabel(dimension)}: ${
          cellIssues.length
        } issue${cellIssues.length === 1 ? "" : "s"}${
          cellIssues.length ? `, ${artifactLabel(highest)}` : ""
        }`;

        const openCell = (target: HTMLElement) => {
          if (cellIssues.length === 1) {
            onOpenIssue(cellIssues[0], target);
          } else {
            onOpenScope({ artifact, dimension }, target);
          }
        };

        return cellIssues.length ? (
          <div
            aria-label={label}
            className={`attention-cell attention-cell-${highest}`}
            key={dimension}
            onClick={(event) => openCell(event.currentTarget)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                openCell(event.currentTarget);
              }
            }}
            role="gridcell"
            tabIndex={0}
          >
            <button
              aria-label={`Ask OSLO about ${artifactLabel(artifact)} ${artifactLabel(
                dimension,
              )}`}
              className="attention-cell-ask"
              onClick={(event) => {
                event.stopPropagation();
                onAskOslo({ artifact, dimension });
              }}
              type="button"
            >
              <Sparkle aria-hidden="true" size={10} weight="fill" />
            </button>
            <strong>{cellIssues.length}</strong>
            <span>{highest}</span>
            {cellIssues.length > 1 ? <small>Multiple</small> : null}
          </div>
        ) : (
          <div
            aria-label={label}
            className="attention-cell attention-cell-calm"
            key={dimension}
            role="gridcell"
          >
            <span>·</span>
          </div>
        );
      })}
    </>
  );
}

function AttentionScopePanel({
  issues,
  onAsk,
  onClearArtifact,
  onClearDimension,
  onClose,
  onOpenIssue,
  scope,
}: {
  issues: Issue[];
  onAsk: () => void;
  onClearArtifact: () => void;
  onClearDimension: () => void;
  onClose: () => void;
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  scope: AttentionScope;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);
  const scopedIssues = issues.filter(
    (issue) =>
      (!scope.artifact || issue.artifact_type === scope.artifact) &&
      (!scope.dimension || issue.dimension.toLowerCase() === scope.dimension),
  );

  useEffect(() => {
    closeButton.current?.focus();
  }, []);

  return (
    <aside
      aria-label="Scoped attention findings"
      aria-modal="true"
      className="project-sidepanel attention-scope-panel"
      role="dialog"
    >
      <div className="attention-scope-heading">
        <div>
          <span>Attention focus</span>
          <h2>{scopedIssues.length} findings in this view</h2>
          <p>Current published read · open and addressed</p>
        </div>
        <button
          aria-label="Close scoped findings"
          onClick={onClose}
          ref={closeButton}
          type="button"
        >
          <X aria-hidden="true" size={19} />
        </button>
      </div>
      <div className="attention-scope-chips" aria-label="Active filters">
        {scope.artifact ? (
          <button
            aria-label={`Clear ${artifactLabel(scope.artifact)} filter`}
            onClick={onClearArtifact}
            type="button"
          >
            {artifactLabel(scope.artifact)}
            <X aria-hidden="true" size={11} />
          </button>
        ) : null}
        {scope.dimension ? (
          <button
            aria-label={`Clear ${artifactLabel(scope.dimension)} filter`}
            onClick={onClearDimension}
            type="button"
          >
            {artifactLabel(scope.dimension)}
            <X aria-hidden="true" size={11} />
          </button>
        ) : null}
      </div>
      <button className="ask-oslo-issue" onClick={onAsk} type="button">
        <Sparkle aria-hidden="true" size={12} weight="fill" />
        Ask OSLO about this focus
      </button>
      <div className="attention-scope-list">
        {scopedIssues.map((issue) => (
          <button
            aria-label={`Open ${issue.title}`}
            key={issue.id}
            onClick={(event) => onOpenIssue(issue, event.currentTarget)}
            type="button"
          >
            <span className={`severity severity-${issue.severity.toLowerCase()}`}>
              {issue.severity}
            </span>
            <strong>{issue.title}</strong>
            <small>
              {artifactLabel(issue.artifact_type)} · {issue.dimension} ·{" "}
              {artifactLabel(issue.status)}
            </small>
            <CaretRight aria-hidden="true" size={14} />
          </button>
        ))}
      </div>
      <p className="attention-scope-note">
        A finding can appear in more than one focused view when the same evidence affects
        multiple dimensions. The underlying issue remains one governed record.
      </p>
    </aside>
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
  onIssueAction,
  onSubmit,
  pending,
  selectedResolution,
}: {
  analysisRunning: boolean;
  answer: string;
  error: string | null;
  issue: Issue;
  onAnswerChange: (value: string) => void;
  onAsk: () => void;
  onClose: () => void;
  onIssueAction: (
    action: "select" | "apply" | "custom",
    resolution: string,
  ) => Promise<void>;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  pending: boolean;
  selectedResolution: string | null;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);
  const [evidenceOpen, setEvidenceOpen] = useState(false);
  const [customResolution, setCustomResolution] = useState("");
  const evidence = issue.evidence ?? [];
  const effectiveStatus = analysisRunning ? "addressed" : issue.status;

  useEffect(() => {
    closeButton.current?.focus();
  }, []);

  return (
    <aside
      aria-describedby={analysisRunning ? "issue-addressed-status" : undefined}
      aria-label="Issue details"
      aria-modal="true"
      className="project-sidepanel issue-panel"
      role="dialog"
    >
      <div className="issue-panel-heading">
        <div>
          <span className={`severity severity-${issue.severity.toLowerCase()}`}>
            {issue.severity}
          </span>
          <h2>{issue.title}</h2>
        </div>
        <button
          aria-label="Close issue"
          onClick={onClose}
          ref={closeButton}
          type="button"
        >
          <X aria-hidden="true" size={20} />
        </button>
      </div>
      <p className="issue-meta">
        Dimension · {issue.dimension} &nbsp; Section · {artifactLabel(issue.artifact_type)}
        &nbsp; Type · Finding
      </p>
      <div className="issue-lifecycle" aria-label={`Issue status ${effectiveStatus}`}>
        {["open", "addressed", "resolved"].map((status) => (
          <span className={status === effectiveStatus ? "is-current" : ""} key={status}>
            {artifactLabel(status)}
          </span>
        ))}
      </div>
      {analysisRunning ? (
        <p className="sr-only" id="issue-addressed-status" aria-live="polite">
          Your answer is saved. This issue is addressed while OSLO re-analyzes it.
        </p>
      ) : null}
      <button className="ask-oslo-issue" onClick={onAsk} type="button">
        <Sparkle aria-hidden="true" size={12} weight="fill" />
        Ask OSLO about this issue
      </button>
      <section>
        <h3>Why this matters</h3>
        <p>{issue.why}</p>
      </section>
      <section className="issue-evidence">
        <button
          aria-controls="issue-evidence-content"
          aria-expanded={evidenceOpen}
          aria-label={`Evidence · ${evidence.length} ${
            evidence.length === 1 ? "source" : "sources"
          }, traceable to inputs`}
          className="issue-evidence-disclosure"
          onClick={() => setEvidenceOpen((current) => !current)}
          type="button"
        >
          <span>Evidence</span>
          <small>
            {evidence.length} {evidence.length === 1 ? "source" : "sources"}, traceable to inputs
          </small>
          <CaretDown aria-hidden="true" size={14} />
        </button>
        {evidenceOpen ? (
          <div className="evidence-list" id="issue-evidence-content">
            {evidence.map((citation) => (
              <div key={`${citation.source_name}:${citation.location}:${citation.excerpt}`}>
                <small>
                  <strong>{citation.source_name}</strong>
                  <span>{citation.location}</span>
                </small>
                <p>{citation.excerpt}</p>
              </div>
            ))}
            {!evidence.length ? (
              <p className="evidence-unavailable">
                Readable evidence details are not available for this earlier snapshot.
              </p>
            ) : null}
          </div>
        ) : null}
      </section>
      <section>
        <h3>What this weakens</h3>
        <p>
          This finding lowers the {issue.dimension.toLowerCase()} read for{" "}
          {artifactLabel(issue.artifact_type)} until the plan contains verified evidence.
        </p>
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
      <section className="issue-recommendation">
        <h3>OSLO recommended</h3>
        <strong>{issue.recommendation}</strong>
        <p>
          Applying this fix creates a new user-confirmed artifact version and re-runs the
          governed analysis. OSLO never marks the issue resolved without that new read.
        </p>
        <div className="issue-action-row">
          <button
            disabled={pending || analysisRunning}
            onClick={() => void onIssueAction("apply", issue.recommendation)}
            type="button"
          >
            Apply this fix
          </button>
          <button onClick={onAsk} type="button">Discuss</button>
        </div>
      </section>
      <section>
        <h3>Possible resolution paths</h3>
        <div className="resolution-path">
          <span><ArrowRight aria-hidden="true" size={12} />{issue.recommendation}</span>
          <button
            disabled={pending || analysisRunning}
            onClick={() => void onIssueAction("select", issue.recommendation)}
            type="button"
          >
            Select this path
          </button>
        </div>
        <div className="resolution-path">
          <span>
            <ArrowRight aria-hidden="true" size={12} />
            Confirm an accountable owner, decision date, and fallback.
          </span>
          <button onClick={onAsk} type="button">Discuss</button>
        </div>
      </section>
      {selectedResolution ? (
        <section className="confirmed-resolution" aria-live="polite">
          <h3>Confirmed by you</h3>
          <p>{selectedResolution}</p>
        </section>
      ) : null}
      <section className="custom-resolution">
        <h3>Write my own fix in {artifactLabel(issue.artifact_type)}</h3>
        <textarea
          aria-label="Custom resolution"
          disabled={pending || analysisRunning}
          maxLength={5_000}
          onChange={(event) => setCustomResolution(event.target.value)}
          placeholder="Describe the confirmed change to add to this artifact."
          value={customResolution}
        />
        <button
          disabled={!customResolution.trim() || pending || analysisRunning}
          onClick={() => void onIssueAction("custom", customResolution)}
          type="button"
        >
          Apply custom fix
        </button>
      </section>
      <p className="issue-history-pointer">
        Status changes are recorded in project history. Full history arrives in Slice 7.
      </p>
      {error ? <p className="clarification-error" role="alert">{error}</p> : null}
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

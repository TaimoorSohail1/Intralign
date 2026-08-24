"use client";

import {
  ArrowRight,
  CaretDown,
  CaretRight,
  ChatTeardropDots,
  ClockCounterClockwise,
  Diamond,
  FileText,
  Gear,
  House,
  Info,
  ListBullets,
  MapTrifold,
  MagnifyingGlass,
  Question,
  SignOut,
  Sparkle,
  X,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import type { FormEvent } from "react";

import type { OverviewSnapshot, ProjectHistory } from "@/lib/server/oslo-api";
import { ArtifactWorkspace } from "@/components/artifacts/artifact-workspace";
import { HistoryWorkspace } from "@/components/history/history-workspace";
import { InferenceMap } from "@/components/inference/inference-map";
import { ReportWorkspace } from "@/components/reports/report-workspace";
import { ProjectWorkspaceControls } from "@/components/workspace/project-workspace-controls";
import { analysisFailureCopy } from "@/lib/analysis-errors";
import {
  defaultIssueFilters,
  issueFiltersToSearchParams,
  type IssueFilters,
} from "@/lib/issue-filters";
import { buildProjectProvenance } from "@/lib/project-provenance";

const dimensions = ["clarity", "alignment", "feasibility"] as const;
const confidenceBands = ["Very Low", "Low", "Moderate", "High", "Very High"] as const;
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
  "What should I do next?",
  "Why is Feasibility where it is?",
  "Explain the top issue",
  "What changed in the last run?",
  "What does my plan include?",
];
const orientationSteps = [
  {
    title: "Your strategic read",
    body: "Outcome Confidence is how mature OSLO’s understanding of your plan is. It sits on a five-step scale, always qualified by how well grounded the read is.",
  },
  {
    title: "Your read, always visible",
    body: "Outcome Confidence and how well grounded it is stay in the top bar. Click it for the Clarity · Alignment · Feasibility breakdown and the reliability basis.",
  },
  {
    title: "Where to start",
    body: "The most consequential open issue, most severe first — OSLO suggests where to begin. Advisory; the call stays yours.",
  },
  {
    title: "The Attention map",
    body: "Switch to the Attention map to see where the plan needs attention — documents × Clarity/Alignment/Feasibility. Brighter means more attention, not a health score.",
  },
  {
    title: "Edit a document",
    body: "Open any of the seven documents and type. Your edits become confirmed evidence; saved changes reanalyse automatically and keep every view up to date.",
  },
  {
    title: "Ask OSLO anything",
    body: "A persistent advisor — ask about the read, an issue, or what to do next. It reads and explains; nothing changes your plan without you.",
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
type ProjectView =
  | "overview"
  | "attention"
  | "inference"
  | "issues"
  | "history"
  | "reports"
  | ArtifactView;

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
  initialIssueFilters = defaultIssueFilters,
}: {
  initial: OverviewSnapshot;
  displayName: string;
  logoutAction: () => Promise<void>;
  initialView?: ProjectView;
  initialHistory?: ProjectHistory;
  initialIssueFilters?: IssueFilters;
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
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [advisorQuestions, setAdvisorQuestions] = useState(initialAdvisorQuestions);
  const [question, setQuestion] = useState("");
  const [advisorPending, setAdvisorPending] = useState(false);
  const [advisorError, setAdvisorError] = useState<string | null>(null);
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
  const [projectHistory, setProjectHistory] = useState(initialHistory);
  const [analysisUpdateRunId, setAnalysisUpdateRunId] = useState<string | null>(() => {
    const activeExtended = initial.extended_analysis;
    return activeExtended?.status === "queued" || activeExtended?.status === "running"
      ? activeExtended.run_id
      : null;
  });
  const advisorInFlight = useRef(false);
  const advisorStateBeforeIssue = useRef(true);
  const issueTrigger = useRef<HTMLElement | null>(null);
  const mainScrollRegion = useRef<HTMLElement | null>(null);
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
  const limitingDimension = snapshot.assessment.limiting_dimension;
  const provenance = useMemo(() => buildProjectProvenance(snapshot), [snapshot]);
  const confidenceBandIndex = Math.max(
    0,
    confidenceBands.indexOf(
      snapshot.assessment.confidence_band as (typeof confidenceBands)[number],
    ),
  );
  const groundingQualifier =
    provenance.totalClaims === 0
      ? "forming"
      : provenance.groundedClaims / provenance.totalClaims >= 0.75
        ? "well grounded"
        : provenance.groundedClaims / provenance.totalClaims >= 0.5
          ? "largely grounded"
          : provenance.groundedClaims / provenance.totalClaims >= 0.25
            ? "partly grounded"
            : "thinly grounded";
  const hasFirstValue = snapshot.artifacts.length > 0;
  const overviewScrollKey = `oslo:overview-scroll:${snapshot.project_id}`;

  useEffect(() => {
    if (!initialHistory) return;
    let cancelled = false;
    void fetch(`/api/projects/${snapshot.project_id}/history?category=all`, {
      cache: "no-store",
    })
      .then(async (response) => {
        if (!response.ok) return null;
        return response.json() as Promise<ProjectHistory>;
      })
      .then((nextHistory) => {
        if (!cancelled && nextHistory) setProjectHistory(nextHistory);
      })
      .catch(() => {
        // Keep the last history page when refresh fails. All other views still use
        // the last atomically published Overview snapshot.
      });
    return () => {
      cancelled = true;
    };
  }, [initialHistory, snapshot.analysis_run_id, snapshot.project_id]);

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
            `${analysisFailureCopy(run.error_code).title}. Your answer is saved and the current read is unchanged.`,
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
    if (!selectedIssue) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSelectedIssue(null);
        setAdvisorOpen(advisorStateBeforeIssue.current);
        window.setTimeout(() => issueTrigger.current?.focus(), 0);
        return;
      }
      if (event.key === "Tab") {
        const panel = document.querySelector<HTMLElement>(
          '[role="dialog"][aria-label="Issue details"]',
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
  }, [selectedIssue]);

  useEffect(() => {
    if (initialView !== "overview") return;
    const savedPosition = window.sessionStorage.getItem(overviewScrollKey);
    if (!savedPosition) return;
    const top = Number(savedPosition);
    if (!Number.isFinite(top)) return;
    const restorePosition = () => {
      mainScrollRegion.current?.scrollTo({ behavior: "auto", top });
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
  const updateIssueLifecycle = (
    issueId: string,
    status: Issue["status"],
    selectedResolution?: string,
  ) => {
    const update = (issue: Issue) =>
      issue.id === issueId
        ? {
            ...issue,
            status,
            ...(selectedResolution === undefined
              ? {}
              : { selected_resolution: selectedResolution }),
          }
        : issue;
    setSnapshot((current) => ({
      ...current,
      assessment: {
        ...current.assessment,
        issues: current.assessment.issues.map(update),
      },
    }));
    setSelectedIssue((current) => (current ? update(current) : current));
  };

  const openAttentionScope = (scope: AttentionScope) => {
    const filters: IssueFilters = {
      ...defaultIssueFilters,
      artifact: (scope.artifact as IssueFilters["artifact"]) ?? null,
      dimension: (scope.dimension as IssueFilters["dimension"]) ?? null,
    };
    const query = issueFiltersToSearchParams(filters).toString();
    router.push(
      `/projects/${snapshot.project_id}/issues${query ? `?${query}` : ""}`,
    );
  };

  const rememberOverviewPosition = () => {
    if (initialView !== "overview") return;
    window.sessionStorage.setItem(
      overviewScrollKey,
      String(mainScrollRegion.current?.scrollTop ?? 0),
    );
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
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.message || "Your answer could not be saved.");
      }
      updateIssueLifecycle(selectedIssue.id, "addressed");
      setAnalysisUpdateRunId(result.run_id);
    } catch (error) {
      setClarificationError(
        error instanceof Error
          ? error.message
          : "Your answer could not be saved. Please try again.",
      );
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
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.message || "The resolution could not be saved.");
      }
      setSelectedResolutions((current) => ({
        ...current,
        [selectedIssue.id]: result.selected_resolution,
      }));
      updateIssueLifecycle(
        selectedIssue.id,
        "addressed",
        result.selected_resolution,
      );
      if (result.analysis_run?.run_id) {
        setAnalysisUpdateRunId(result.analysis_run.run_id);
      }
    } catch (error) {
      setIssueActionError(
        error instanceof Error
          ? error.message
          : "The resolution could not be saved. Please try again.",
      );
    } finally {
      setIssueActionPending(false);
    }
  };

  const extendedFailure = analysisFailureCopy(extendedRun?.error_code);

  const panelVisible = advisorOpen || Boolean(selectedIssue);
  const activeTourStep = tourStep ?? 0;

  return (
    <main
      className={`project-shell ${selectedIssue ? "has-issue" : ""} ${
        orientation ? "is-touring" : ""
      }`}
    >
      <header className="project-header">
        <Link className="project-toolbar-brand" href="/workspace">
          <span aria-hidden="true">I</span>
          <strong>Intralign</strong>
        </Link>
        <ProjectWorkspaceControls
          planPortalId="project-sidebar-plan"
          projectId={snapshot.project_id}
        />
        <div className="project-context">
          <strong>Project understanding</strong>
          <span aria-hidden="true">›</span>
          <em>
            {initialView === "attention"
              ? "Attention map"
              : initialView === "inference"
                ? "Inference map"
              : initialView === "reports"
                ? "Reports"
                : artifactLabel(initialView)}
          </em>
        </div>
        <button
          aria-label={`Outcome Confidence ${snapshot.assessment.confidence_band}, ${groundingQualifier}`}
          aria-expanded={confidenceBreakdownOpen}
          className={`project-header-confidence ${
            orientation && activeTourStep === 1 ? "is-tour-target" : ""
          }`}
          onClick={() => {
            setSearchOpen(false);
            setConfidenceBreakdownOpen((current) => !current);
          }}
          type="button"
        >
          <span className="project-header-confidence-dot" />
          <span>Outcome Confidence</span>
          <strong>{snapshot.assessment.confidence_band}</strong>
          <small>{groundingQualifier}</small>
        </button>
        <div className="project-actions">
          <button
            aria-label="Search project"
            className="project-search-button"
            onClick={() => {
              setConfidenceBreakdownOpen(false);
              setSearchOpen(true);
            }}
            title="Search project"
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
        </div>
      </header>

      {confidenceBreakdownOpen ? (
        <ConfidenceBreakdown
          assessment={snapshot.assessment}
          groundingQualifier={groundingQualifier}
          onClose={() => setConfidenceBreakdownOpen(false)}
        />
      ) : null}

      <aside
        aria-label="Project navigation"
        className="workspace-sidebar"
        tabIndex={0}
      >
        <p className="workspace-label">Project</p>
        <nav aria-label="Workspace">
          <Link
            aria-current={initialView === "overview" ? "page" : undefined}
            className={initialView === "overview" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/overview`}
          >
            <House aria-hidden="true" size={17} />
            Overview
          </Link>
          <Link
            aria-current={initialView === "issues" ? "page" : undefined}
            aria-label={`Issues ${openIssues.length}`}
            className={initialView === "issues" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/issues`}
          >
            <ListBullets aria-hidden="true" size={17} />
            Issues
            <span className="nav-count">{openIssues.length}</span>
          </Link>
          <Link
            aria-current={initialView === "history" ? "page" : undefined}
            className={initialView === "history" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/history`}
          >
            <ClockCounterClockwise aria-hidden="true" size={17} />
            History
          </Link>
          <Link
            aria-current={initialView === "attention" ? "page" : undefined}
            className={`${initialView === "attention" ? "is-current" : ""} ${
              orientation && activeTourStep === 3 ? "is-tour-target" : ""
            }`}
            href={`/projects/${snapshot.project_id}/attention`}
            onClick={rememberOverviewPosition}
          >
            <MapTrifold aria-hidden="true" size={17} />
            Attention map
            {openIssues.length ? <span className="nav-count">{openIssues.length}</span> : null}
          </Link>
          <Link
            aria-current={initialView === "inference" ? "page" : undefined}
            className={initialView === "inference" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/inference`}
          >
            <Diamond aria-hidden="true" size={17} />
            Inference map
          </Link>
          <Link
            aria-current={initialView === "reports" ? "page" : undefined}
            className={initialView === "reports" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/reports`}
          >
            <FileText aria-hidden="true" size={17} />
            Reports
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
                className={`${initialView === artifactType ? "is-current" : ""} ${
                  orientation && activeTourStep === 4 && artifactType === "resources"
                    ? "is-tour-target"
                    : ""
                }`}
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
        <div className="workspace-sidebar-footer">
          <button
            onClick={() => {
              setTourStep(0);
              setOrientation(true);
            }}
            type="button"
          >
            <Sparkle aria-hidden="true" size={15} />
            Take a quick tour
          </button>
          <div
            className="project-sidebar-plan-slot"
            id="project-sidebar-plan"
          />
          <details className="project-account project-sidebar-account">
            <summary
              aria-label={`Open account menu for ${displayName}`}
              role="button"
              title="Account and settings"
            >
              <span aria-hidden="true">{displayName.slice(0, 1).toUpperCase()}</span>
              <span className="project-account-summary-copy">
                <strong>{displayName}</strong>
                <small>Your account &amp; settings</small>
              </span>
            </summary>
            <div className="project-account-menu">
              <header>
                <span aria-hidden="true">{displayName.slice(0, 1).toUpperCase()}</span>
                <div>
                  <strong>{displayName}</strong>
                  <small>Account &amp; workspace</small>
                </div>
              </header>
              <button
                onClick={(event) => {
                  event.currentTarget.closest("details")?.removeAttribute("open");
                  setTourStep(0);
                  setOrientation(true);
                }}
                type="button"
              >
                <Question aria-hidden="true" size={16} />
                How OSLO works
              </button>
              <Link href="/settings">
                <Gear aria-hidden="true" size={16} />
                Settings
              </Link>
              <form action={logoutAction}>
                <button type="submit">
                  <SignOut aria-hidden="true" size={16} />
                  Log out
                </button>
              </form>
            </div>
          </details>
          <span>OSLO advises; you decide.</span>
        </div>
      </aside>

      <div className={`project-grid ${panelVisible ? "" : "is-panel-closed"}`}>
        <section
          aria-label="Project content"
          className="project-main"
          ref={mainScrollRegion}
          tabIndex={0}
        >
          {initialView === "overview" ? (
            <div className={`overview-stack ${hasFirstValue ? "has-first-value" : ""}`}>
              <section className="confidence-read">
                <div className="confidence-topline">
                  <p className="eyebrow">Outcome confidence</p>
                  <span className={`snapshot-badge ${isProvisional ? "" : "is-current"}`}>
                    {snapshot.state.replace("_", "-")}
                  </span>
                </div>
                <div
                  aria-label={`Outcome Confidence ${snapshot.assessment.confidence_band}, ${groundingQualifier}`}
                  className="confidence-ramp"
                  role="img"
                >
                  {confidenceBands.map((band, index) => (
                    <span
                      className={index === confidenceBandIndex ? "is-current" : ""}
                      key={band}
                    >
                      <i />
                      <small>{band}</small>
                    </span>
                  ))}
                </div>
                <div className="confidence-prototype-hero">
                  <div>
                    <strong>{snapshot.assessment.confidence_band}</strong>
                    <p>
                      on the read is <b>{groundingQualifier}</b>
                    </p>
                  </div>
                  <div className="confidence-limiter">
                    <p>
                      <strong>{artifactLabel(limitingDimension)}</strong> — the lowest.
                      Confirm it to lift the read.
                    </p>
                    <button
                      onClick={() => {
                        setAdvisorOpen(true);
                        void askQuestion("Explain the current Outcome Confidence");
                      }}
                      type="button"
                    >
                      <Sparkle aria-hidden="true" size={12} weight="fill" />
                      Ask OSLO why
                    </button>
                  </div>
                </div>
                {snapshot.assessment.false_confidence ? (
                  <div className="false-confidence-warning" role="alert">
                    <Info aria-hidden="true" size={15} />
                    This read sits high on thin evidence. Confirm the supporting
                    assumptions before relying on it.
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
                    const valueIndex = Math.max(
                      0,
                      confidenceBands.indexOf(
                        value as (typeof confidenceBands)[number],
                      ),
                    );
                    return (
                      <div className={limiting ? "is-limiting" : ""} key={name}>
                        <span>{artifactLabel(name)}</span>
                        <div
                          aria-label={`${artifactLabel(name)}: ${value}`}
                          className="dimension-ramp"
                          role="img"
                          tabIndex={0}
                        >
                          {confidenceBands.map((band, index) => (
                            <i
                              className={index <= valueIndex ? "is-filled" : ""}
                              key={band}
                            />
                          ))}
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
                  <span>{artifactLabel(snapshot.assessment.confidence_direction)}</span>
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
                      href={`/projects/${snapshot.project_id}/history`}
                      onClick={rememberOverviewPosition}
                    >
                      Timeline <ArrowRight aria-hidden="true" size={12} />
                    </Link>
                    <Link href={`/projects/${snapshot.project_id}/attention`}>
                      Attention map <ArrowRight aria-hidden="true" size={12} />
                    </Link>
                  </div>
                </div>
              </section>

              <section className={`start-here ${
                orientation && activeTourStep === 2 ? "is-tour-target" : ""
              }`}>
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
                  <Info
                    aria-label="Progress in grounding the current read, not project completion."
                    size={14}
                  />
                </div>
                <div className="progress-foundation">
                  <div className="progress-foundation-hero">
                    <p>
                      <strong>{provenance.groundedClaims}</strong>
                      <span>of {provenance.totalClaims}</span>
                    </p>
                    <div>
                      <b>grounded in your evidence</b>
                      <span>the rest of your read is OSLO&apos;s inference</span>
                    </div>
                  </div>
                  <div
                    aria-label={`${provenance.groundedClaims} grounded and ${provenance.inferredClaims} inferred claims`}
                    className="progress-foundation-bar"
                    role="img"
                  >
                    {provenance.groundedClaims ? (
                      <span
                        className="is-grounded"
                        style={{ flex: provenance.groundedClaims }}
                      >
                        <strong>{provenance.groundedClaims}</strong>
                        Confirmed by evidence
                      </span>
                    ) : null}
                    {provenance.inferredClaims ? (
                      <span
                        className="is-inferred"
                        style={{ flex: provenance.inferredClaims }}
                      >
                        <strong>{provenance.inferredClaims}</strong>
                        From OSLO
                      </span>
                    ) : null}
                  </div>
                  <div className="progress-foundation-legend">
                    <span><i className="is-grounded" /> Grounded — your evidence</span>
                    <span><i className="is-inferred" /> Inferred — OSLO&apos;s read</span>
                  </div>
                  {provenance.loadBearingInferences ? (
                    <p className="progress-load-bearing">
                      Your read leans on{" "}
                      <strong>{provenance.loadBearingInferences}</strong>{" "}
                      load-bearing inference
                      {provenance.loadBearingInferences === 1 ? "" : "s"}{" "}
                      <Link href={`/projects/${snapshot.project_id}/inference`}>
                        See them <ArrowRight aria-hidden="true" size={11} />
                      </Link>
                    </p>
                  ) : null}
                  <div className="progress-work">
                    <section>
                      <p>Open</p>
                      <div>
                        <article>
                          <strong>{openIssues.length}</strong>
                          <span>Issues</span>
                        </article>
                        <article className="is-critical">
                          <strong>{criticalCount}</strong>
                          <span>Critical</span>
                        </article>
                        <article>
                          <strong>{clarificationCount}</strong>
                          <span>Open questions</span>
                        </article>
                      </div>
                    </section>
                    <section>
                      <p>Closed</p>
                      <div>
                        <article>
                          <strong>{snapshot.assessment.resolved_issue_count}</strong>
                          <span>Issues resolved</span>
                        </article>
                        <article>
                          <strong>{snapshot.assessment.confirmed_dependency_count}</strong>
                          <span>Questions answered</span>
                        </article>
                      </div>
                    </section>
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
            </div>
          ) : initialView === "attention" ? (
            <AttentionView
              onAskOslo={(scope) => {
                const focus = [scope.artifact, scope.dimension]
                  .filter((value): value is string => Boolean(value))
                  .map(artifactLabel)
                  .join(" × ");
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
          ) : initialView === "inference" ? (
            <InferenceMap onOpenIssue={openIssue} snapshot={snapshot} />
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
              initialFilters={initialIssueFilters}
              issues={snapshot.assessment.issues}
              onOpenIssue={openIssue}
              projectId={snapshot.project_id}
            />
          ) : initialView === "history" && initialHistory ? (
            <HistoryWorkspace
              analysisRunId={snapshot.analysis_run_id}
              history={projectHistory ?? initialHistory}
              onAskOslo={(runId, prompt) => {
                setAdvisorOpen(true);
                void askQuestion(prompt, runId);
              }}
              projectId={snapshot.project_id}
            />
          ) : initialView === "reports" ? (
            <ReportWorkspace history={projectHistory} snapshot={snapshot} />
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
            projectId={snapshot.project_id}
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
        ) : advisorOpen ? (
          <div className={orientation && activeTourStep === 5 ? "advisor-tour-target" : ""}>
            <AdvisorPanel
            advisorError={advisorError}
            advisorPending={advisorPending}
            advisorQuestions={advisorQuestions}
            extendedFailed={extendedFailed}
            extendedFailure={extendedFailure}
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
          </div>
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
          data-step={activeTourStep + 1}
          role="dialog"
        >
          <div className="tour-card">
            <span className="tour-step-label">Step {activeTourStep + 1} of {orientationSteps.length}</span>
            <h2>{orientationSteps[activeTourStep].title}</h2>
            <p>{orientationSteps[activeTourStep].body}</p>
            <div className="tour-actions">
              <button onClick={() => void dismissOrientation()} type="button">Skip</button>
              <span aria-hidden="true" />
              {activeTourStep > 0 ? (
                <button onClick={() => setTourStep(activeTourStep - 1)} type="button">Back</button>
              ) : null}
              <button
                className="button button-primary"
                onClick={() => {
                  if (activeTourStep === orientationSteps.length - 1) {
                    void dismissOrientation();
                  } else {
                    setTourStep(activeTourStep + 1);
                  }
                }}
                type="button"
              >
                {activeTourStep === orientationSteps.length - 1 ? "Done" : "Next"}
              </button>
            </div>
          </div>
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
  groundingQualifier,
  onClose,
}: {
  assessment: OverviewSnapshot["assessment"];
  groundingQualifier: string;
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
          <span>Outcome Confidence</span>
          <strong>{assessment.confidence_band}</strong>
          <em>{groundingQualifier}</em>
        </div>
        <button aria-label="Close confidence breakdown" onClick={onClose} ref={closeButton} type="button">
          <X aria-hidden="true" size={16} />
        </button>
      </div>
      <p>
        Understanding maturity — not project health, readiness, or probability.
        The grounding qualifier shows how much of the read rests directly on evidence.
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
  initialFilters,
  issues,
  onOpenIssue,
  projectId,
}: {
  initialFilters: IssueFilters;
  issues: Issue[];
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  projectId: string;
}) {
  const router = useRouter();
  const [groupMode, setGroupMode] = useState<IssueGroupMode>("dimension");
  const [filters, setFiltersState] = useState<IssueFilters>(initialFilters);
  const {
    artifact: artifactFilter,
    dimension: dimensionFilter,
    severity: severityFilter,
    status: statusFilter,
  } = filters;

  function setFilters(next: IssueFilters) {
    setFiltersState(next);
    const query = issueFiltersToSearchParams(next).toString();
    router.replace(
      `/projects/${projectId}/issues${query ? `?${query}` : ""}`,
      { scroll: false },
    );
  }

  const statusScopedIssues = useMemo(
    () =>
      issues.filter((issue) => {
        if (statusFilter === "active") return issue.status !== "resolved";
        if (statusFilter === "all") return true;
        return issue.status === statusFilter;
      }),
    [issues, statusFilter],
  );

  const filteredIssues = useMemo(
    () =>
      statusScopedIssues
        .filter((issue) => {
          if (artifactFilter && issue.artifact_type !== artifactFilter) return false;
          if (
            dimensionFilter &&
            issue.dimension.toLowerCase() !== dimensionFilter.toLowerCase()
          ) {
            return false;
          }
          if (severityFilter && issue.severity !== severityFilter) return false;
          return true;
        })
        .sort(issueSort),
    [artifactFilter, dimensionFilter, severityFilter, statusScopedIssues],
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
  const hiddenCount = Math.max(0, statusScopedIssues.length - filteredIssues.length);
  const hasExplicitFilters = Boolean(
    artifactFilter ||
      dimensionFilter ||
      severityFilter ||
      statusFilter !== "active",
  );

  function clearFilters() {
    setFilters(defaultIssueFilters);
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
          onChange={(artifact) =>
            setFilters({
              ...filters,
              artifact: artifact as IssueFilters["artifact"],
            })
          }
          options={artifactOrder
            .map((artifact) => ({
              label: artifactLabel(artifact),
              value: artifact,
              count: statusScopedIssues.filter(
                (issue) => issue.artifact_type === artifact,
              ).length,
            }))
            .filter((option) => option.count)}
        />
        <IssueFilterRow
          active={dimensionFilter}
          label="Dimension"
          onChange={(dimension) =>
            setFilters({
              ...filters,
              dimension: dimension as IssueFilters["dimension"],
            })
          }
          options={dimensions.map((dimension) => ({
            label: artifactLabel(dimension),
            value: dimension,
            count: statusScopedIssues.filter(
              (issue) => issue.dimension.toLowerCase() === dimension,
            ).length,
          }))}
        />
        <IssueFilterRow
          active={severityFilter}
          label="Severity"
          onChange={(severity) =>
            setFilters({
              ...filters,
              severity: severity as IssueFilters["severity"],
            })
          }
          options={["Critical", "Moderate", "Warning"].map((severity) => ({
            label: severity,
            value: severity,
            count: statusScopedIssues.filter(
              (issue) => issue.severity === severity,
            ).length,
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
              onClick={() =>
                setFilters({
                  ...filters,
                  status: value as IssueFilters["status"],
                })
              }
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

function IssuePanel({
  analysisRunning,
  answer,
  error,
  issue,
  projectId,
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
  projectId: string;
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
  const [comments, setComments] = useState<Array<{
    id: string;
    body: string;
    author_name: string;
    created_at: string;
  }>>([]);
  const [commentBody, setCommentBody] = useState("");
  const [commentPending, setCommentPending] = useState(false);
  const [collaborationError, setCollaborationError] = useState("");
  const [reviewerName, setReviewerName] = useState("");
  const [reviewerEmail, setReviewerEmail] = useState("");
  const [reviewPending, setReviewPending] = useState(false);
  const [reviewLink, setReviewLink] = useState("");
  const [reviewCopied, setReviewCopied] = useState(false);
  const evidence = issue.evidence ?? [];
  const effectiveStatus = issue.status;

  useEffect(() => {
    closeButton.current?.focus();
  }, []);

  useEffect(() => {
    let active = true;
    fetch(`/api/projects/${projectId}/collaboration`, { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) throw new Error("Collaboration details are unavailable.");
        return response.json();
      })
      .then((state: { comments?: Array<{
        id: string;
        issue_id: string;
        body: string;
        author_name: string;
        created_at: string;
      }> }) => {
        if (active) {
          setComments((state.comments ?? []).filter((comment) => comment.issue_id === issue.id));
        }
      })
      .catch(() => {
        if (active) setCollaborationError("Comments could not be loaded.");
      });
    return () => {
      active = false;
    };
  }, [issue.id, projectId]);

  const submitComment = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!commentBody.trim()) return;
    setCommentPending(true);
    setCollaborationError("");
    try {
      const mentions = Array.from(
        new Set(Array.from(commentBody.matchAll(/@([\w.-]+)/g), (match) => match[1])),
      );
      const response = await fetch(`/api/projects/${projectId}/collaboration`, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ issueId: issue.id, body: commentBody.trim(), mentions }),
      });
      const created = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(created.message ?? "Comment could not be added.");
      setComments((current) => [...current, created]);
      setCommentBody("");
    } catch (caught) {
      setCollaborationError(
        caught instanceof Error ? caught.message : "Comment could not be added.",
      );
    } finally {
      setCommentPending(false);
    }
  };

  const createReview = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!reviewerName.trim()) return;
    setReviewPending(true);
    setCollaborationError("");
    setReviewLink("");
    try {
      const response = await fetch(`/api/projects/${projectId}/collaboration`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          action: "review",
          issueId: issue.id,
          reviewerName: reviewerName.trim(),
          reviewerEmail: reviewerEmail.trim() || null,
        }),
      });
      const created = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(created.message ?? "Review link could not be created.");
      setReviewLink(created.url);
      setReviewerName("");
      setReviewerEmail("");
    } catch (caught) {
      setCollaborationError(
        caught instanceof Error ? caught.message : "Review link could not be created.",
      );
    } finally {
      setReviewPending(false);
    }
  };

  return (
    <aside
      aria-describedby={analysisRunning ? "issue-analysis-pending-status" : undefined}
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
        <p
          className="issue-analysis-status"
          id="issue-analysis-pending-status"
          aria-live="polite"
        >
          <strong>Saved · Analysis pending</strong>
          <span>
            The issue stays {artifactLabel(issue.status)} until the completed analysis
            confirms its new status.
          </span>
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
      <section className="issue-collaboration">
        <div className="issue-collaboration-heading">
          <div>
            <h3>Discussion</h3>
            <p>Append-only project comments. Mention teammates with @name.</p>
          </div>
          <span>{comments.length}</span>
        </div>
        <div className="issue-comment-thread">
          {comments.map((comment) => (
            <article key={comment.id}>
              <header>
                <strong>{comment.author_name}</strong>
                <time dateTime={comment.created_at}>
                  {new Date(comment.created_at).toLocaleString()}
                </time>
              </header>
              <p>{comment.body}</p>
            </article>
          ))}
          {!comments.length ? <p className="issue-comment-empty">No comments yet.</p> : null}
        </div>
        <form className="issue-comment-form" onSubmit={submitComment}>
          <textarea
            aria-label="Add a comment"
            disabled={commentPending}
            maxLength={5_000}
            onChange={(event) => setCommentBody(event.target.value)}
            placeholder="Add a comment or mention @teammate…"
            value={commentBody}
          />
          <button disabled={commentPending || !commentBody.trim()} type="submit">
            {commentPending ? "Adding…" : "Add comment"}
          </button>
        </form>
      </section>
      <section className="issue-review-share">
        <div className="issue-review-share-heading">
          <span className="issue-review-share-icon">
            <Sparkle aria-hidden="true" size={15} weight="fill" />
          </span>
          <div>
            <h3>Share for review</h3>
            <p>Invite a reviewer without using a workspace seat or invitation.</p>
          </div>
        </div>
        <form className="issue-review-share-form" onSubmit={createReview}>
          <div className="issue-review-fields">
            <label>
              Reviewer name
              <input
                disabled={reviewPending}
                onChange={(event) => setReviewerName(event.target.value)}
                placeholder="e.g. Alex Morgan"
                required
                value={reviewerName}
              />
            </label>
            <label>
              <span>
                Email <em>Optional</em>
              </span>
              <input
                disabled={reviewPending}
                onChange={(event) => setReviewerEmail(event.target.value)}
                placeholder="alex@example.com"
                type="email"
                value={reviewerEmail}
              />
            </label>
          </div>
          <button disabled={reviewPending || !reviewerName.trim()} type="submit">
            <Sparkle aria-hidden="true" size={13} weight="fill" />
            {reviewPending ? "Creating…" : "Create secure review link"}
          </button>
        </form>
        {reviewLink ? (
          <div className="issue-review-link" role="status">
            <code>{reviewLink}</code>
            <button
              onClick={() => {
                void navigator.clipboard.writeText(reviewLink);
                setReviewCopied(true);
              }}
              type="button"
            >
              {reviewCopied ? "Copied" : "Copy link"}
            </button>
          </div>
        ) : null}
        {collaborationError ? (
          <p className="clarification-error" role="alert">{collaborationError}</p>
        ) : null}
      </section>
      <p className="issue-history-pointer">
        Status changes and reviewer attestations are retained in project history.
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
  extendedFailure,
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
  extendedFailure: ReturnType<typeof analysisFailureCopy>;
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
      <div
        aria-label="OSLO conversation"
        aria-live="polite"
        className="chat-content"
        role="region"
        tabIndex={0}
      >
        <p className="chat-note">
          I&apos;ve completed the {isProvisional ? "initial" : "extended"} read. Start with
          the top issue, or ask about any part of the plan.
        </p>
        <div className="chat-completion-note">
          <strong>
            {extendedFailed
              ? extendedFailure.title
              : extendedRetrying
                ? "Extended Analysis is retrying"
                : isProvisional
                  ? "Initial Analysis complete"
                  : "Extended Analysis complete"}
          </strong>
          <p>
            {extendedFailed
              ? `${extendedFailure.detail} The last successful read is unchanged.`
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
          <textarea
            aria-label="Ask OSLO"
            disabled={advisorPending}
            maxLength={1000}
            onChange={(event) => onQuestionChange(event.target.value)}
            placeholder="Ask OSLO about the read, an issue, or what to do next…  (@ to pin a context)"
            rows={3}
            value={question}
          />
          <div className="chat-composer-footer">
            <span>↳ advisory <Info aria-hidden="true" size={12} /></span>
            <button disabled={advisorPending || !question.trim()} type="submit">Send</button>
          </div>
        </form>
      </div>
    </aside>
  );
}

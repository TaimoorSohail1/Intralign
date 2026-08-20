"use client";

import {
  ArrowRight,
  ArrowSquareOut,
  ArrowsSplit,
  CaretDown,
  CaretRight,
  CaretUp,
  CheckCircle,
  ClockCounterClockwise,
  Diamond,
  FileText,
  Gear,
  House,
  Info,
  ListBullets,
  LockSimple,
  MapTrifold,
  MagnifyingGlass,
  PencilSimple,
  SignOut,
  Sparkle,
  Target,
  X,
} from "@phosphor-icons/react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Fragment,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import type { FormEvent, RefObject, SetStateAction } from "react";

import type {
  CollaborationRollUpProjection,
  GroundingMapProjection,
  IssueBasis,
  IssueLifecycleAct,
  IssueProposalSummary,
  OverviewSnapshot,
  ProjectHistory,
  ProjectOutcomeSummary,
} from "@/lib/server/oslo-api";
import { ArtifactWorkspace } from "@/components/artifacts/artifact-workspace";
import { FullPlanWorkspace } from "@/components/execution/full-plan-workspace";
import {
  CollaborationGroundingMap,
  CollaborationRollUp,
} from "@/components/collaboration/collaboration-projections";
import { HistoryWorkspace } from "@/components/history/history-workspace";
import { InferenceMap } from "@/components/inference/inference-map";
import { YourOutcomeDashboard } from "@/components/outcomes/your-outcome-dashboard";
import type { YourOutcomeProjection } from "@/components/outcomes/your-outcome-projection";
import { ReportWorkspace } from "@/components/reports/report-workspace";
import { ProjectWorkspaceControls } from "@/components/workspace/project-workspace-controls";
import {
  WorkspaceSettingsDialog,
  type SettingsSectionId,
} from "@/components/workspace/workspace-settings";
import { analysisFailureCopy } from "@/lib/analysis-errors";
import {
  defaultIssueFilters,
  issueFiltersToSearchParams,
  type IssueFilters,
} from "@/lib/issue-filters";
import { buildProjectProvenance } from "@/lib/project-provenance";
import { currentReadSummary } from "@/lib/current-read-summary";

const dimensions = ["clarity", "alignment", "feasibility"] as const;
const integrityBands = ["Fragile", "Weak", "Developing", "Solid", "Sound"] as const;
const intralignLogo = "/intralign-logo.webp";
export { intralignLogo };

const artifactOrder = [
  "intent",
  "scope",
  "requirements",
  "constraints",
  "work_breakdown",
  "schedule",
  "resources",
] as const;
const r2UnderstandingOrder = ["intent", "scope", "requirements", "constraints"] as const;
const initialAdvisorQuestions = [
  "What should I do next?",
  "Why is Feasibility where it is?",
  "Explain the top issue",
  "What changed in the last run?",
  "What does my plan include?",
];
const orientationSteps = [
  {
    title: "Outcome Integrity",
    body: "Your read at a glance — the weakest of three pillars gates it. A maturity read of how sound the plan is, never a health score or a forecast.",
  },
  {
    title: "Your outcome",
    body: "What you’re steering toward. Open it any time for the full definition, its provenance, and any other outcomes.",
  },
  {
    title: "The read",
    body: "Your plan’s weaknesses, most-exposed first — one layer across all three pillars. Open any issue to settle it right in the read.",
  },
  {
    title: "Your plan & work",
    body: "Your understanding artifacts and the execution plan live here — the documents OSLO reads and you author.",
  },
  {
    title: "OSLO — advisory",
    body: "OSLO’s reasoning and chat. It advises and acts only on your say-so; every action is recorded as yours.",
  },
];
const feedbackKinds = [
  { id: "broken", title: "Something’s broken", detail: "a defect — it didn’t work as expected" },
  { id: "missing", title: "Something’s missing", detail: "an enhancement — it could be better" },
  { id: "other", title: "Something else", detail: "a question, a reaction, anything" },
] as const;
const feedbackImpacts = ["Blocking me", "Slowing me down", "Minor"] as const;
type FeedbackKind = (typeof feedbackKinds)[number]["id"];
type FeedbackTicketSummary = {
  ticket_id: string;
  title: string;
  status: string;
  created_at: string;
};
const feedbackSessionStorageKey = "oslo_feedback_session_id";

function currentFeedbackSessionId() {
  const existing = window.sessionStorage.getItem(feedbackSessionStorageKey);
  if (existing) return existing;
  const created =
    globalThis.crypto?.randomUUID?.() ??
    `feedback-${Date.now()}-${Math.random().toString(36).slice(2)}`;
  window.sessionStorage.setItem(feedbackSessionStorageKey, created);
  return created;
}
const severityRank: Record<string, number> = {
  Critical: 3,
  Moderate: 2,
  Warning: 1,
};
type Issue = OverviewSnapshot["assessment"]["issues"][number];
type ArtifactView = (typeof artifactOrder)[number];
type ProjectView =
  | "overview"
  | "outcome"
  | "inference"
  | "rollup"
  | "grounding"
  | "issues"
  | "history"
  | "reports"
  | "full_plan"
  | ArtifactView;

function isArtifactView(value: ProjectView): value is ArtifactView {
  return artifactOrder.includes(value as ArtifactView);
}

function isR2ReadView(value: ProjectView) {
  return !isArtifactView(value);
}

interface ChatMessage {
  id: number;
  role: "user" | "advisor";
  text: string;
}

function issueSort(left: Issue, right: Issue) {
  if (left.exposure_rank !== right.exposure_rank) {
    return (right.exposure_rank ?? 0) - (left.exposure_rank ?? 0);
  }
  return (severityRank[right.severity] ?? 0) - (severityRank[left.severity] ?? 0);
}

function issuePillar(issue: Issue) {
  if (issue.pillar) return issue.pillar;
  if (issue.id.startsWith("ISS-FC-")) return "Grounding";
  if (issue.id.startsWith("ISS-CP-")) return "Adaptability";
  return "Viability";
}

type IssueActionFeedback = {
  title: string;
  detail: string;
  target: string;
};

function integrityReadLabel(
  integrity: OverviewSnapshot["assessment"]["integrity"],
) {
  return integrity.complete === false ? "Under review" : integrity.level;
}

function artifactLabel(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function persistedArtifactType(value: string) {
  return value === "constraints" ? "context" : value;
}

function artifactSidebarStatus({
  artifactType,
  issues,
  proposals,
  snapshot,
}: {
  artifactType: string;
  issues: Issue[];
  proposals: IssueProposalSummary[];
  snapshot: OverviewSnapshot;
}) {
  const persistedType = persistedArtifactType(artifactType);
  const artifact = snapshot.artifacts.find(
    (candidate) => candidate.artifact_type === persistedType,
  );
  const inferred = artifact?.content?.sections.reduce((total, section) => {
    const sectionClaims =
      section.provenance === "from_oslo" && !section.rows.some((row) => row.some((cell) => cell.trim()))
        ? Number(Boolean(section.body.trim())) + section.bullets.filter(Boolean).length
        : 0;
    const rowClaims = section.rows.reduce(
      (count, _row, index) =>
        count +
        Number(
          section.row_states?.[index] === "inferred" ||
            (section.row_states?.[index] !== "confirmed" &&
              section.row_provenance?.[index] === "from_oslo"),
        ),
      0,
    );
    return total + sectionClaims + rowClaims;
  }, 0);
  return {
    inferred: inferred ?? issues.filter((issue) => issue.artifact_type === persistedType).length,
    issues: issues.filter((issue) => issue.artifact_type === persistedType).length,
    proposals: proposals.filter((proposal) => proposal.artifact_type === persistedType).length,
  };
}

function ArtifactSidebarIndicators({
  execution,
  status,
}: {
  execution?: boolean;
  status: ReturnType<typeof artifactSidebarStatus>;
}) {
  const openCount = execution ? status.issues : status.inferred;
  return (
    <span
      aria-hidden="true"
      className="r2-artifact-indicators"
      title={`${status.proposals} proposals, ${openCount} open`}
    >
      {status.proposals ? <span className="is-proposal">◆{status.proposals}</span> : null}
      {openCount ? <span className="is-open">{openCount}</span> : <span className="is-clear" />}
    </span>
  );
}

function issueResolutionMap(issues: Issue[]) {
  return Object.fromEntries(
    issues
      .filter((issue) => Boolean(issue.selected_resolution))
      .map((issue) => [issue.id, issue.selected_resolution as string]),
  );
}

function useProjectAdvisorState(projectId: string, initialOpen: boolean) {
  const storageKey = `oslo:advisor-open:${projectId}`;
  const readOpen = useCallback(() => {
    const stored = window.sessionStorage.getItem(storageKey);
    return stored === null ? initialOpen : stored !== "false";
  }, [initialOpen, storageKey]);
  const subscribe = useCallback(
    (onStoreChange: () => void) => {
      const handleAdvisorState = (event: Event) => {
        if (event instanceof CustomEvent && event.detail === storageKey) onStoreChange();
      };
      const handleStorage = (event: StorageEvent) => {
        if (event.key === storageKey) onStoreChange();
      };
      window.addEventListener("oslo:advisor-state", handleAdvisorState);
      window.addEventListener("storage", handleStorage);
      return () => {
        window.removeEventListener("oslo:advisor-state", handleAdvisorState);
        window.removeEventListener("storage", handleStorage);
      };
    },
    [storageKey],
  );
  const open = useSyncExternalStore(subscribe, readOpen, () => initialOpen);

  const setOpen = useCallback(
    (value: SetStateAction<boolean>) => {
      const nextOpen = typeof value === "function" ? value(readOpen()) : value;
      window.sessionStorage.setItem(storageKey, String(nextOpen));
      window.dispatchEvent(new CustomEvent("oslo:advisor-state", { detail: storageKey }));
    },
    [readOpen, storageKey],
  );

  return [open, setOpen] as const;
}

export function ProjectOverview({
  initial,
  displayName,
  logoutAction,
  initialView = "overview",
  initialHistory,
  initialIssueFilters = defaultIssueFilters,
  initialProposals = [],
  initialOutcome = null,
  initialOutcomeDashboard,
  initialRollUp,
  initialGroundingMap,
  initialIssueId,
  compactIssuesLanding = false,
  initialArtifactFocus,
  returnToOutcome = false,
}: {
  initial: OverviewSnapshot;
  displayName: string;
  logoutAction: () => Promise<void>;
  initialView?: ProjectView;
  initialHistory?: ProjectHistory;
  initialIssueFilters?: IssueFilters;
  initialProposals?: IssueProposalSummary[];
  initialOutcome?: ProjectOutcomeSummary | null;
  initialOutcomeDashboard?: YourOutcomeProjection;
  initialRollUp?: CollaborationRollUpProjection;
  initialGroundingMap?: GroundingMapProjection;
  initialIssueId?: string;
  compactIssuesLanding?: boolean;
  initialArtifactFocus?: "primary-outcome" | "held-outcomes" | "new-outcome";
  returnToOutcome?: boolean;
}) {
  const router = useRouter();
  const replaceRoute = router.replace;
  const [snapshot, setSnapshot] = useState(initial);
  const [activeOutcome] = useState(initialOutcome);
  const [orientation, setOrientation] = useState(false);
  const [tourStep, setTourStep] = useState<number | null>(null);
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(
    initial.assessment.issues.find((issue) => issue.id === initialIssueId) ?? null,
  );
  const [advisorOpen, setAdvisorOpen] = useProjectAdvisorState(
    initial.project_id,
    !initial.first_run?.freeze_on,
  );
  const [advisorWide, setAdvisorWide] = useState(false);
  const [workspaceNoticeOpen, setWorkspaceNoticeOpen] = useState(
    !initial.first_run?.freeze_on,
  );
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [confidenceBreakdownOpen, setConfidenceBreakdownOpen] = useState(false);
  const [r2IntegrityExpanded, setR2IntegrityExpanded] = useState(
    initialView === "overview" && !compactIssuesLanding && !initial.first_run?.freeze_on,
  );
  const [r2IntegrityDetailOpen, setR2IntegrityDetailOpen] = useState(false);
  const r2Shell = useRef<HTMLElement>(null);
  const r2IntegrityHeader = useRef<HTMLElement>(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settingsSection, setSettingsSection] = useState<SettingsSectionId>("profile");
  const [feedbackKind, setFeedbackKind] = useState<FeedbackKind>("broken");
  const [feedbackText, setFeedbackText] = useState("");
  const [feedbackExpected, setFeedbackExpected] = useState("");
  const [feedbackImpact, setFeedbackImpact] = useState<(typeof feedbackImpacts)[number]>("Blocking me");
  const [feedbackTicket, setFeedbackTicket] = useState<FeedbackTicketSummary | null>(null);
  const [feedbackTickets, setFeedbackTickets] = useState<FeedbackTicketSummary[]>([]);
  const [feedbackPending, setFeedbackPending] = useState(false);
  const [feedbackError, setFeedbackError] = useState<string | null>(null);
  const [feedbackListPending, setFeedbackListPending] = useState(false);
  const [feedbackListError, setFeedbackListError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [advisorQuestions, setAdvisorQuestions] = useState(initialAdvisorQuestions);
  const [question, setQuestion] = useState("");
  const [advisorPending, setAdvisorPending] = useState(false);
  const [advisorError, setAdvisorError] = useState<string | null>(null);
  const [extendedRetrying, setExtendedRetrying] = useState(false);
  const [extendedRetryError, setExtendedRetryError] = useState<string | null>(null);
  const [reanalysisPending, setReanalysisPending] = useState(false);
  const [reanalysisFeedback, setReanalysisFeedback] = useState<string | null>(null);
  const [clarificationAnswer, setClarificationAnswer] = useState("");
  const [clarificationPending, setClarificationPending] = useState(false);
  const [clarificationError, setClarificationError] = useState<string | null>(null);
  const [issueActionPending, setIssueActionPending] = useState(false);
  const [issueActionError, setIssueActionError] = useState<string | null>(null);
  const [issueActionFeedback, setIssueActionFeedback] = useState<IssueActionFeedback | null>(null);
  const [showFirstRunRecorded, setShowFirstRunRecorded] = useState(false);
  const [proposals, setProposals] = useState(initialProposals);
  const [proposalActionPending, setProposalActionPending] = useState<string | null>(null);
  const [proposalOpen, setProposalOpen] = useState(true);
  const [awaitingOpen, setAwaitingOpen] = useState(true);
  const [actedOpen, setActedOpen] = useState(true);
  const [resolvedOpen, setResolvedOpen] = useState(true);
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
  const advisorStateBeforeIssue = useRef(!initial.first_run?.freeze_on);
  const firstRunIssueOpened = useRef(false);
  const previousFirstRunFreeze = useRef(Boolean(initial.first_run?.freeze_on));
  const issueTrigger = useRef<HTMLElement | null>(null);
  const integrityTrigger = useRef<HTMLButtonElement | null>(null);
  const accountTrigger = useRef<HTMLElement | null>(null);
  const accountMenu = useRef<HTMLDetailsElement | null>(null);
  const feedbackDialog = useRef<HTMLElement | null>(null);
  const tourLaunchRequested = useRef(false);
  const tourOutcomeTarget = useRef<HTMLButtonElement | null>(null);
  const tourReadTarget = useRef<HTMLButtonElement | null>(null);
  const tourPlanTarget = useRef<HTMLDivElement | null>(null);
  const tourAdvisorTarget = useRef<HTMLFormElement | null>(null);
  const tourCard = useRef<HTMLDivElement | null>(null);
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
  const visibleSummary = useMemo(
    () => currentReadSummary(snapshot.summary, openIssues.length, snapshot.project_title),
    [openIssues.length, snapshot.project_title, snapshot.summary],
  );
  const artifactAdvisorIssues = isArtifactView(initialView)
    ? openIssues.filter(
        (issue) => issue.artifact_type === persistedArtifactType(initialView),
      )
    : openIssues;
  const rankedIssues = useMemo(
    () => openIssues.filter((issue) => issue.status === "open"),
    [openIssues],
  );
  const awaitingEvidenceIssues = useMemo(
    () => openIssues.filter((issue) => issue.status === "routed"),
    [openIssues],
  );
  const actedIssues = useMemo(
    () => openIssues.filter((issue) =>
      ["addressed", "needs_fix", "needs_grounding"].includes(issue.status),
    ),
    [openIssues],
  );
  const firstRunTargetIssue =
    rankedIssues[0] ??
    actedIssues.find((issue) => issue.status === "needs_grounding") ??
    actedIssues.find((issue) => issue.primary_act === "verify") ??
    actedIssues[0] ??
    null;
  const resolvedIssues = useMemo(
    () => snapshot.assessment.issues.filter((issue) => issue.status === "resolved"),
    [snapshot.assessment.issues],
  );
  const compactFilterActive = compactIssuesLanding && Boolean(
    initialIssueFilters.artifact ||
      initialIssueFilters.dimension ||
      initialIssueFilters.severity ||
      initialIssueFilters.status !== "active",
  );
  const compactScopedIssues = useMemo(() => {
    if (!compactFilterActive) return snapshot.assessment.issues;
    return snapshot.assessment.issues.filter((issue) => {
      if (
        initialIssueFilters.artifact &&
        issue.artifact_type !== initialIssueFilters.artifact
      ) return false;
      if (
        initialIssueFilters.dimension &&
        issue.dimension.toLowerCase() !== initialIssueFilters.dimension
      ) return false;
      if (
        initialIssueFilters.severity &&
        issue.severity !== initialIssueFilters.severity
      ) return false;
      if (initialIssueFilters.status === "active") return issue.status !== "resolved";
      if (initialIssueFilters.status === "all") return true;
      return issue.status === initialIssueFilters.status;
    });
  }, [
    compactFilterActive,
    initialIssueFilters.artifact,
    initialIssueFilters.dimension,
    initialIssueFilters.severity,
    initialIssueFilters.status,
    snapshot.assessment.issues,
  ]);
  const compactScopedIssueIds = useMemo(
    () => new Set(compactScopedIssues.map((issue) => issue.id)),
    [compactScopedIssues],
  );
  const displayRankedIssues = compactFilterActive
    ? rankedIssues.filter((issue) => compactScopedIssueIds.has(issue.id))
    : rankedIssues;
  const displayAwaitingEvidenceIssues = compactFilterActive
    ? awaitingEvidenceIssues.filter((issue) => compactScopedIssueIds.has(issue.id))
    : awaitingEvidenceIssues;
  const displayActedIssues = compactFilterActive
    ? actedIssues.filter((issue) => compactScopedIssueIds.has(issue.id))
    : actedIssues;
  const displayResolvedIssues = compactFilterActive
    ? resolvedIssues.filter((issue) => compactScopedIssueIds.has(issue.id))
    : resolvedIssues;
  const settledIssueCount = Math.max(
    snapshot.assessment.resolved_issue_count,
    resolvedIssues.length,
  );
  const activeIssueIds = useMemo(
    () => new Set(openIssues.map((issue) => issue.id)),
    [openIssues],
  );
  const undecidedProposals = useMemo(
    () => proposals.filter(
      (proposal) =>
        !proposal.accepted &&
        !proposal.rejected &&
        activeIssueIds.has(proposal.issue_id),
    ),
    [activeIssueIds, proposals],
  );
  const displayUndecidedProposals = compactFilterActive
    ? undecidedProposals.filter((proposal) => compactScopedIssueIds.has(proposal.issue_id))
    : undecidedProposals;
  const clarificationIssue = rankedIssues.find((issue) => Boolean(issue.clarification));
  const criticalCount = openIssues.filter((issue) => issue.severity === "Critical").length;
  const clarificationCount = openIssues.filter((issue) => Boolean(issue.clarification)).length;
  const provenance = useMemo(() => buildProjectProvenance(snapshot), [snapshot]);
  const integrity = snapshot.assessment.integrity;
  const groundingPillar = integrity.decomposition.find((pillar) => pillar.key === "Grounding");
  const integrityBandIndex = Math.max(0, integrityBands.indexOf(integrity.level));
  const hasFirstValue = snapshot.artifacts.length > 0;
  const outcomeArtifact = snapshot.artifacts.find(
    (artifact) => artifact.artifact_type === "intent",
  );
  const outcomeDefinition = outcomeArtifact?.summary ?? null;
  const projectTitle = snapshot.project_title?.trim() || "Project";
  const overviewScrollKey = `oslo:overview-scroll:${snapshot.project_id}`;
  const workspaceNoticeKey = `oslo:workspace-open:${snapshot.project_id}`;

  useEffect(() => {
    const firstRun = snapshot.first_run;
    if (!firstRun?.freeze_on) {
      firstRunIssueOpened.current = false;
      return;
    }
    if (initialView === "overview") {
      advisorStateBeforeIssue.current = false;
      setAdvisorOpen(false);
    }
    if (
      initialView !== "overview" ||
      firstRun.grounding_act_count < 1 ||
      firstRunIssueOpened.current ||
      !firstRunTargetIssue
    ) {
      return;
    }
    firstRunIssueOpened.current = true;
    issueTrigger.current = null;
    setSelectedIssue(firstRunTargetIssue);
  }, [firstRunTargetIssue, initialView, setAdvisorOpen, snapshot.first_run]);

  useEffect(() => {
    const freezeOn = Boolean(snapshot.first_run?.freeze_on);
    if (previousFirstRunFreeze.current && !freezeOn) {
      setWorkspaceNoticeOpen(true);
    }
    previousFirstRunFreeze.current = freezeOn;
  }, [snapshot.first_run?.freeze_on]);

  useEffect(() => {
    const url = new URL(window.location.href);
    if (!url.searchParams.has("settings")) return;
    url.searchParams.delete("settings");
    window.history.replaceState(window.history.state, "", `${url.pathname}${url.search}${url.hash}`);
    const timer = window.setTimeout(() => {
      setOrientation(false);
      setSettingsOpen(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    const url = new URL(window.location.href);
    const tourRequested =
      url.searchParams.has("tour") ||
      window.sessionStorage.getItem("oslo_pending_tour") === "1";
    if (!tourRequested || initialView !== "overview") return;
    tourLaunchRequested.current = true;
    window.sessionStorage.removeItem("oslo_pending_tour");
    url.searchParams.delete("tour");
    window.history.replaceState(window.history.state, "", `${url.pathname}${url.search}${url.hash}`);
    const timer = window.setTimeout(() => {
      setSelectedIssue(null);
      setAdvisorOpen(true);
      setR2IntegrityExpanded(true);
      setWorkspaceNoticeOpen(true);
      setTourStep(0);
      setOrientation(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, [initialView, setAdvisorOpen]);

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
    const compact = window.matchMedia(
      initialView === "overview" ? "(max-width: 900px)" : "(max-width: 980px)",
    );
    const keepMainConsoleAvailable = (event: MediaQueryListEvent | MediaQueryList) => {
      if (event.matches) setAdvisorOpen(false);
    };
    keepMainConsoleAvailable(compact);
    compact.addEventListener("change", keepMainConsoleAvailable);
    return () => compact.removeEventListener("change", keepMainConsoleAvailable);
  }, [initialView, setAdvisorOpen]);

  useLayoutEffect(() => {
    const shell = r2Shell.current;
    if (!shell) return;
    if (!r2IntegrityExpanded || isArtifactView(initialView)) {
      shell.style.setProperty("--r2-integrity-height", "124px");
      return;
    }

    const header = r2IntegrityHeader.current;
    if (!header) return;
    const syncHeight = () => {
      const nextHeight = Math.max(124, Math.ceil(header.getBoundingClientRect().height));
      shell.style.setProperty("--r2-integrity-height", `${nextHeight}px`);
    };

    syncHeight();
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(syncHeight);
    observer.observe(header);
    return () => observer.disconnect();
  }, [initialView, r2IntegrityDetailOpen, r2IntegrityExpanded, snapshot.analysis_run_id]);

  useEffect(() => {
    const orientationTimer = window.setTimeout(() => {
      if (tourLaunchRequested.current) return;
      if (!snapshot.orientation_seen && initialView !== "overview") {
        replaceRoute(`/projects/${snapshot.project_id}/overview?tour=1`);
        return;
      }
      setOrientation(!snapshot.orientation_seen);
    }, 0);
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
    initialView,
    isProvisional,
    replaceRoute,
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
          setIssueActionFeedback(null);
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
    if (!issueActionFeedback) return;
    const revealFeedback = () => {
      const region = mainScrollRegion.current;
      if (!region) return;
      if (typeof region.scrollTo === "function") {
        region.scrollTo({ behavior: "auto", top: 0 });
        return;
      }
      region.scrollTop = 0;
    };
    revealFeedback();
    const frame = window.requestAnimationFrame(revealFeedback);
    const timer = window.setTimeout(() => setIssueActionFeedback(null), 2600);
    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(timer);
    };
  }, [issueActionFeedback]);

  useEffect(() => {
    let cancelled = false;
    const updateRecordedVisibility = (visible: boolean) => {
      void Promise.resolve().then(() => {
        if (!cancelled) setShowFirstRunRecorded(visible);
      });
    };
    if (!snapshot.first_run?.freeze_on || snapshot.first_run.grounding_act_count < 1) {
      updateRecordedVisibility(false);
      return () => {
        cancelled = true;
      };
    }
    const storageKey = `r2-first-run-recorded:${snapshot.project_id}`;
    const storedValue = window.sessionStorage.getItem(storageKey);
    if (storedValue === "done") {
      updateRecordedVisibility(false);
      return () => {
        cancelled = true;
      };
    }
    const now = Date.now();
    const storedDeadline = Number(storedValue);
    if (storedValue && Number.isFinite(storedDeadline) && storedDeadline <= now) {
      window.sessionStorage.setItem(storageKey, "done");
      updateRecordedVisibility(false);
      return () => {
        cancelled = true;
      };
    }
    const deadline = Number.isFinite(storedDeadline) && storedDeadline > now
      ? storedDeadline
      : now + 2200;
    window.sessionStorage.setItem(storageKey, String(deadline));
    updateRecordedVisibility(true);
    const timer = window.setTimeout(() => {
      window.sessionStorage.setItem(storageKey, "done");
      setShowFirstRunRecorded(false);
    }, Math.max(0, deadline - now));
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [snapshot.first_run?.freeze_on, snapshot.first_run?.grounding_act_count, snapshot.project_id]);

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
        const returnFocus = issueTrigger.current;
        const returnIssueId = selectedIssue.id;
        setSelectedIssue(null);
        setAdvisorOpen(advisorStateBeforeIssue.current);
        window.setTimeout(() => {
          const queueButton = document.querySelector<HTMLElement>(
            `[data-issue-id="${CSS.escape(returnIssueId)}"]`,
          );
          const nextQueueButton = document.querySelector<HTMLElement>(
            '[aria-label="Exposure-ranked issue queue"] [data-issue-id]',
          );
          (queueButton ?? (returnFocus?.isConnected ? returnFocus : null) ?? nextQueueButton)?.focus();
        }, 0);
        return;
      }
      if (event.key === "Tab" && initialView !== "overview") {
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
  }, [initialView, selectedIssue, setAdvisorOpen]);

  useEffect(() => {
    if (!selectedIssue) return;
    const revealIssue = window.requestAnimationFrame(() => {
      const panel = document.getElementById(`issue-detail-${selectedIssue.id}`);
      if (typeof panel?.scrollIntoView === "function") {
        panel.scrollIntoView({ behavior: "auto", block: "start" });
      }
      panel?.focus({ preventScroll: true });
    });
    return () => window.cancelAnimationFrame(revealIssue);
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

  useEffect(() => {
    if (window.localStorage.getItem(workspaceNoticeKey) !== "dismissed") return;
    const restore = window.setTimeout(() => setWorkspaceNoticeOpen(false), 0);
    return () => window.clearTimeout(restore);
  }, [workspaceNoticeKey]);

  useEffect(() => {
    const closeAccountMenu = (event: MouseEvent) => {
      if (!accountMenu.current?.open || accountMenu.current.contains(event.target as Node)) return;
      accountMenu.current.removeAttribute("open");
    };
    const closeAccountMenuOnEscape = (event: KeyboardEvent) => {
      if (event.key !== "Escape" || !accountMenu.current?.open) return;
      accountMenu.current.removeAttribute("open");
      accountTrigger.current?.focus();
    };
    document.addEventListener("mousedown", closeAccountMenu);
    document.addEventListener("keydown", closeAccountMenuOnEscape);
    return () => {
      document.removeEventListener("mousedown", closeAccountMenu);
      document.removeEventListener("keydown", closeAccountMenuOnEscape);
    };
  }, []);

  useEffect(() => {
    if (!feedbackOpen) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const focusFrame = window.requestAnimationFrame(() => feedbackDialog.current?.focus());
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setFeedbackOpen(false);
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      window.cancelAnimationFrame(focusFrame);
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [feedbackOpen]);

  useEffect(() => {
    if (!orientation) return;
    const step = tourStep ?? 0;
    const target = [
      integrityTrigger.current,
      tourOutcomeTarget.current,
      tourReadTarget.current,
      tourPlanTarget.current,
      tourAdvisorTarget.current,
    ][step];
    const card = tourCard.current;
    if (!target || !card) return;

    target.scrollIntoView?.({
      behavior: "auto",
      block: step < 2 ? "nearest" : "center",
      inline: "nearest",
    });

    let secondFrame = 0;
    const placeCard = () => {
      const targetRect = target.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();
      const margin = 12;
      const gap = 14;
      let left = targetRect.left;
      let top = targetRect.bottom + gap;

      if (step === 2 || step === 3) {
        const targetEdge = step === 3
          ? target.closest(".workspace-sidebar")?.getBoundingClientRect().right ?? targetRect.right
          : targetRect.right;
        left = targetEdge + gap;
        top = targetRect.top;
        if (left + cardRect.width > window.innerWidth - margin) {
          left = targetRect.left - cardRect.width - gap;
        }
      } else if (step === 4) {
        left = targetRect.left;
        top = targetRect.top - cardRect.height - gap;
      }

      left = Math.max(margin, Math.min(left, window.innerWidth - cardRect.width - margin));
      top = Math.max(margin, Math.min(top, window.innerHeight - cardRect.height - margin));
      card.style.left = `${Math.round(left)}px`;
      card.style.top = `${Math.round(top)}px`;
      card.style.right = "auto";
      card.style.bottom = "auto";
      card.style.transform = "none";
    };

    const firstFrame = window.requestAnimationFrame(() => {
      secondFrame = window.requestAnimationFrame(placeCard);
    });
    window.addEventListener("resize", placeCard);
    window.addEventListener("scroll", placeCard, true);
    return () => {
      window.cancelAnimationFrame(firstFrame);
      window.cancelAnimationFrame(secondFrame);
      window.removeEventListener("resize", placeCard);
      window.removeEventListener("scroll", placeCard, true);
    };
  }, [orientation, tourStep]);

  const dismissOrientation = async () => {
    localStorage.setItem("oslo_orientation_seen", "true");
    setSnapshot((current) => ({ ...current, orientation_seen: true }));
    setOrientation(false);
    setTourStep(null);
    await fetch("/api/orientation", { method: "POST" }).catch(() => undefined);
    router.refresh();
  };

  const openIssue = (issue: Issue, trigger?: HTMLElement | null) => {
    advisorStateBeforeIssue.current = advisorOpen;
    issueTrigger.current = trigger ?? (document.activeElement as HTMLElement | null);
    setSelectedIssue(issue);
    setClarificationAnswer("");
    setClarificationError(null);
  };

  const closeIssue = () => {
    const returnFocus = issueTrigger.current;
    const returnIssueId = selectedIssue?.id;
    setSelectedIssue(null);
    setAdvisorOpen(advisorStateBeforeIssue.current);
    window.setTimeout(() => {
      const queueButton = returnIssueId
        ? document.querySelector<HTMLElement>(`[data-issue-id="${CSS.escape(returnIssueId)}"]`)
        : null;
      const nextQueueButton = document.querySelector<HTMLElement>(
        '[aria-label="Exposure-ranked issue queue"] [data-issue-id]',
      );
      (queueButton ?? (returnFocus?.isConnected ? returnFocus : null) ?? nextQueueButton)?.focus();
    }, 0);
  };

  const closeIssueAfterGovernedAction = (issueId: string) => {
    if (selectedIssue?.id !== issueId) return;
    setSelectedIssue(null);
    setClarificationAnswer("");
    setClarificationError(null);
    setAdvisorOpen(advisorStateBeforeIssue.current);
  };
  const closeIntegrityBreakdown = () => {
    setConfidenceBreakdownOpen(false);
    integrityTrigger.current?.focus();
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

  const dismissWorkspaceNotice = () => {
    window.localStorage.setItem(workspaceNoticeKey, "dismissed");
    setWorkspaceNoticeOpen(false);
  };

  const showQueuedReadChange = (run: {
    run_id?: string | null;
    consolidated_event_ids?: string[] | null;
  }) => {
    const eventIds = run.consolidated_event_ids ?? [];
    setSnapshot((current) => ({
      ...current,
      freshness: {
        state: "stale",
        pending_count: Math.max(
          current.freshness?.pending_count ?? 0,
          eventIds.length || 1,
        ),
        based_on_run_id:
          current.freshness?.based_on_run_id ?? current.analysis_run_id,
        active_run_id: run.run_id ?? current.freshness?.active_run_id ?? null,
        last_act_at: new Date().toISOString(),
        last_landed_at: current.freshness?.last_landed_at ?? null,
        latest_pending_event_id:
          eventIds.at(-1) ?? current.freshness?.latest_pending_event_id ?? null,
      },
    }));
  };

  const showIssueActionRecorded = (
    issue: Issue,
    target: string,
    detail = "Your decision was recorded. OSLO will re-read to reflect it.",
  ) => {
    setIssueActionFeedback({ title: issue.title, detail, target });
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
      showIssueActionRecorded(
        selectedIssue,
        "Re-analyzing your answer",
        "Your answer is now evidence in your words. OSLO will re-read all three pillars to reflect it.",
      );
      showQueuedReadChange(result);
      setAnalysisUpdateRunId(result.run_id);
      closeIssueAfterGovernedAction(selectedIssue.id);
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
    const actedIssue = selectedIssue;
    const normalizedResolution = resolution.trim();
    const signature = `${actedIssue.id}:${action}:${normalizedResolution}`;
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
        `/api/projects/${snapshot.project_id}/issues/${encodeURIComponent(actedIssue.id)}/actions`,
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
        [actedIssue.id]: result.selected_resolution,
      }));
      updateIssueLifecycle(
        actedIssue.id,
        "addressed",
        result.selected_resolution,
      );
      showIssueActionRecorded(
        actedIssue,
        action === "apply" || action === "custom"
          ? "Settling to needs grounding"
          : "Settling to resolved",
        action === "apply" || action === "custom"
          ? "OSLO drafted the fix into your plan. OSLO will re-read to reflect it."
          : "Your decision is on the record. OSLO will re-read to reflect it.",
      );
      if (result.analysis_run?.run_id) {
        showQueuedReadChange(result.analysis_run);
        setAnalysisUpdateRunId(result.analysis_run.run_id);
      }
      closeIssueAfterGovernedAction(actedIssue.id);
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

  const runReanalysisNow = async () => {
    if (reanalysisPending) return;
    setReanalysisPending(true);
    setReanalysisFeedback(null);
    try {
      const response = await fetch(`/api/projects/${snapshot.project_id}/reanalysis`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ pass_kind: "fast" }),
      });
      if (!response.ok) throw new Error("Reanalysis could not be queued.");
      const run = await response.json();
      if (run.run_id) setAnalysisUpdateRunId(run.run_id);
      setSnapshot((current) => ({
        ...current,
        freshness: current.freshness
          ? { ...current.freshness, state: "reanalyzing", active_run_id: run.run_id ?? null }
          : current.freshness,
      }));
      setReanalysisFeedback("Reanalysis queued");
    } catch (error) {
      setReanalysisFeedback(
        error instanceof Error ? error.message : "Reanalysis could not be queued.",
      );
    } finally {
      setReanalysisPending(false);
    }
  };

  const actOnIssueLifecycle = async (
    issue: Issue,
    act: IssueLifecycleAct,
    options: {
      basis?: IssueBasis | null;
      evidenceRef?: string | null;
      resolution?: string | null;
      reviewer?: { id: string; display_name: string; role: string } | null;
    } = {},
  ) => {
    if (issueActionPending) return;
    setIssueActionPending(true);
    setIssueActionError(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/issues/${encodeURIComponent(issue.id)}/acts`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            act,
            basis: options.basis ?? null,
            evidenceRef: options.evidenceRef ?? null,
            resolution: options.resolution ?? null,
            reviewer: options.reviewer ?? null,
            idempotencyKey: crypto.randomUUID(),
          }),
        },
      );
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.message || "The issue act could not be saved.");
      }
      updateIssueLifecycle(
        issue.id,
        result.status,
        act === "fix" ? options.resolution ?? undefined : undefined,
      );
      showIssueActionRecorded(
        issue,
        act === "route"
          ? "Awaiting evidence"
          : act === "fix"
            ? "Settling to needs grounding"
            : act === "withdraw"
              ? "Returning to open"
              : act === "flag"
                ? "Settling to needs fix"
                : "Settling to resolved",
        act === "route"
          ? "The evidence request is recorded and attributed. The read will move only when evidence arrives."
          : act === "fix"
            ? "OSLO drafted the fix into your plan. OSLO will re-read to reflect it."
            : "Your governed action was recorded. OSLO will re-read all three pillars to reflect it.",
      );
      if (result.first_run) {
        setSnapshot((current) => ({ ...current, first_run: result.first_run }));
      }
      if (result.analysis_run?.run_id) {
        showQueuedReadChange(result.analysis_run);
        setAnalysisUpdateRunId(result.analysis_run.run_id);
      }
      if (act !== "route") {
        closeIssueAfterGovernedAction(issue.id);
      }
    } catch (error) {
      setIssueActionError(
        error instanceof Error
          ? error.message
          : "The issue act could not be saved. Please try again.",
      );
    } finally {
      setIssueActionPending(false);
    }
  };

  const decideProposal = async (
    proposal: IssueProposalSummary,
    accepted: boolean,
    surface: "issue_card" | "artifact" | "folded_read",
  ) => {
    if (proposalActionPending) return;
    setProposalActionPending(proposal.id);
    setIssueActionError(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/proposals/${proposal.id}/decisions`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            accepted,
            surface,
            idempotencyKey: crypto.randomUUID(),
          }),
        },
      );
      const result = await response.json().catch(() => ({}));
      if (!response.ok || !result.proposal) {
        throw new Error(result.message || "The proposal decision could not be saved.");
      }
      setProposals((current) =>
        current.map((item) => item.id === proposal.id ? result.proposal : item),
      );
      if (accepted) {
        const issue = snapshot.assessment.issues.find(
          (candidate) => candidate.id === proposal.issue_id,
        );
        if (issue) {
          showIssueActionRecorded(
            issue,
            "Settling to needs grounding",
            "The accepted proposal was drafted into your plan. OSLO will re-read to reflect it.",
          );
        }
      }
      if (result.analysis_run?.run_id) {
        showQueuedReadChange(result.analysis_run);
        setAnalysisUpdateRunId(result.analysis_run.run_id);
      }
    } catch (error) {
      setIssueActionError(
        error instanceof Error
          ? error.message
          : "The proposal decision could not be saved. Please try again.",
      );
    } finally {
      setProposalActionPending(null);
    }
  };

  const undoLatestPendingAct = async () => {
    const eventId = snapshot.freshness?.latest_pending_event_id;
    if (!eventId || reanalysisPending) return;
    setReanalysisPending(true);
    setReanalysisFeedback(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/acts/${eventId}`,
        { method: "DELETE" },
      );
      if (!response.ok) throw new Error("The change can no longer be undone.");
      const result = await response.json();
      setSnapshot((current) => ({
        ...current,
        freshness: current.freshness
          ? {
              ...current.freshness,
              state: result.pending_count > 0 ? "stale" : "fresh",
              pending_count: result.pending_count,
              latest_pending_event_id: null,
            }
          : current.freshness,
        first_run: current.first_run
          ? {
              ...current.first_run,
              grounding_act_count: result.grounding_act_count,
              ever_unlocked: result.ever_unlocked,
              freeze_on: result.freeze_on,
            }
          : current.first_run,
      }));
      setAnalysisUpdateRunId(null);
      setReanalysisFeedback("Pending change undone");
    } catch (error) {
      setReanalysisFeedback(
        error instanceof Error ? error.message : "The change could not be undone.",
      );
    } finally {
      setReanalysisPending(false);
    }
  };

  const issueSidepanelVisible = Boolean(selectedIssue && initialView !== "overview");
  const advisorVisible = advisorOpen && !issueSidepanelVisible;
  const panelVisible = advisorVisible || issueSidepanelVisible;
  const activeTourStep = tourStep ?? 0;
  const beginTour = (replay = false) => {
    if (replay) localStorage.removeItem("oslo_orientation_seen");
    accountMenu.current?.removeAttribute("open");
    if (initialView !== "overview") {
      tourLaunchRequested.current = true;
      window.sessionStorage.setItem("oslo_pending_tour", "1");
      router.push(`/projects/${snapshot.project_id}/overview?tour=1`);
      return;
    }
    setSelectedIssue(null);
    setAdvisorOpen(true);
    setR2IntegrityExpanded(true);
    setWorkspaceNoticeOpen(true);
    mainScrollRegion.current?.scrollTo?.({ top: 0, behavior: "auto" });
    setTourStep(0);
    setOrientation(true);
  };
  const openFeedback = () => {
    setFeedbackKind("broken");
    setFeedbackText("");
    setFeedbackExpected("");
    setFeedbackImpact("Blocking me");
    setFeedbackTicket(null);
    setFeedbackError(null);
    setFeedbackOpen(true);
    const sessionId = currentFeedbackSessionId();
    setFeedbackListPending(true);
    setFeedbackListError(null);
    void fetch(`/api/feedback/tickets?session_id=${encodeURIComponent(sessionId)}`)
      .then(async (response) => {
        if (!response.ok) throw new Error("Filed feedback could not be loaded.");
        return response.json() as Promise<FeedbackTicketSummary[]>;
      })
      .then(setFeedbackTickets)
      .catch(() => setFeedbackListError("Filed feedback could not be loaded."))
      .finally(() => setFeedbackListPending(false));
  };
  const submitFeedback = async () => {
    if (!feedbackText.trim() || feedbackPending) return;
    setFeedbackPending(true);
    setFeedbackError(null);
    const total = snapshot.assessment.issues.length;
    const grounded = snapshot.assessment.issues.filter(
      (issue) => issue.status === "resolved",
    ).length;
    const category =
      feedbackKind === "broken"
        ? "defect"
        : feedbackKind === "missing"
          ? "enhancement"
          : "other";
    const impact =
      feedbackImpact === "Blocking me"
        ? "blocking"
        : feedbackImpact === "Slowing me down"
          ? "slowing"
          : "minor";
    try {
      const response = await fetch("/api/feedback/tickets", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          session_id: currentFeedbackSessionId(),
          category,
          body: feedbackText.trim(),
          expected: category === "defect" ? feedbackExpected.trim() || null : null,
          impact: category === "defect" ? impact : null,
          context: {
            where: initialView === "overview" ? "Issues" : artifactLabel(initialView),
            view: initialView,
            role: "workspace-user",
            grounded_x: grounded,
            total_y: total,
            first_run_flag: Boolean(snapshot.first_run?.freeze_on),
            ts: new Date().toISOString(),
          },
        }),
      });
      const payload = (await response.json().catch(() => null)) as
        | (FeedbackTicketSummary & { message?: string })
        | null;
      if (!response.ok || !payload?.ticket_id) {
        throw new Error(
          payload?.message ??
            "Feedback could not be filed. Your text is still here; try again.",
        );
      }
      setFeedbackTicket(payload);
      setFeedbackTickets((current) => [
        payload,
        ...current.filter((item) => item.ticket_id !== payload.ticket_id),
      ]);
    } catch (error) {
      setFeedbackError(
        error instanceof Error
          ? error.message
          : "Feedback could not be filed. Your text is still here; try again.",
      );
    } finally {
      setFeedbackPending(false);
    }
  };
  const issuePanel = selectedIssue ? (
    <IssuePanel
      analysisRunning={Boolean(analysisUpdateRunId)}
      answer={clarificationAnswer}
      error={clarificationError ?? issueActionError}
      firstRunFocus={initialView === "overview" && Boolean(snapshot.first_run?.freeze_on)}
      inline={initialView === "overview"}
      issue={selectedIssue}
      key={selectedIssue.id}
      projectId={snapshot.project_id}
      onAnswerChange={setClarificationAnswer}
      onAsk={() => {
        closeIssue();
        setAdvisorOpen(true);
        void askQuestion(`Explain this issue: ${selectedIssue.title}`);
      }}
      onClose={closeIssue}
      onIssueAction={actOnIssue}
      onLifecycleAct={(act, options) => actOnIssueLifecycle(selectedIssue, act, options)}
      onProposalDecision={(proposal, accepted) =>
        decideProposal(proposal, accepted, "issue_card")
      }
      onSubmit={submitClarification}
      pending={clarificationPending || issueActionPending}
      proposalPending={proposalActionPending}
      proposals={undecidedProposals.filter(
        (proposal) => proposal.issue_id === selectedIssue.id,
      )}
      selectedResolution={selectedResolutions[selectedIssue.id] ?? null}
    />
  ) : null;

  const integritySummary = (
    <section
      aria-label="Outcome Integrity summary"
      className="confidence-read integrity-read"
      id="r2-integrity-summary"
      key={snapshot.analysis_run_id}
      ref={r2IntegrityHeader}
    >
      <div className="r2-integrity-copy">
        <div className="confidence-topline">
          <p className="eyebrow">Outcome integrity</p>
          <span className={`snapshot-badge ${isProvisional ? "" : "is-current"}`}>
            {snapshot.state.replace("_", "-")}
          </span>
        </div>
        <div className="confidence-prototype-hero">
          <strong>{integrityReadLabel(integrity)}</strong>
          <div className="r2-integrity-limit-row">
            <p>
              limited by <b>{integrity.limiting_pillar}</b> — a composite is only as sound
              as its weakest pillar
            </p>
            <button
              aria-controls="r2-integrity-summary"
              aria-expanded={r2IntegrityExpanded}
              aria-label="Collapse Outcome Integrity"
              className="r2-integrity-toggle"
              onClick={() => {
                setR2IntegrityDetailOpen(false);
                setR2IntegrityExpanded(false);
              }}
              type="button"
            >
              Collapse <CaretUp aria-hidden="true" size={11} />
            </button>
          </div>
          <p className="r2-grounding-read">
            {groundingPillar?.band === "Sound"
              ? "load-bearing details rest on your evidence, not OSLO’s inferences"
              : "load-bearing details still rest on OSLO’s inferences, not your evidence"}
          </p>
        </div>
        {snapshot.assessment.false_confidence ? (
          <div className="false-confidence-warning" role="alert">
            <Info aria-hidden="true" size={15} />
            This read sits high on thin evidence. Confirm the supporting assumptions before
            relying on it.
          </div>
        ) : null}
        <div className="r2-maturity-row">
          <span>Fragile</span>
          <div
            aria-label={`Outcome Integrity ${integrityReadLabel(integrity)}, limited by ${integrity.limiting_pillar}`}
            className="confidence-ramp"
            role="img"
          >
            {integrityBands.map((band, index) => (
              <span className={index === integrityBandIndex ? "is-current" : ""} key={band}>
                <i />
                <small>{band}</small>
              </span>
            ))}
          </div>
          <span>Sound</span>
          <small><b>as of this analysis</b> · live tracking begins at execution</small>
        </div>
        <details
          className="confidence-method"
          onToggle={(event) => setR2IntegrityDetailOpen(event.currentTarget.open)}
        >
          <summary>Why a maturity read, not a probability?</summary>
          <div className="r2-maturity-explanation">
            <p>{snapshot.assessment.confidence_explanation}</p>
          </div>
        </details>
      </div>
      <div className="integrity-pillars">
        {integrity.decomposition.map((pillar) => (
          <button
            aria-label={`${pillar.key} ${pillar.band}`}
            className={pillar.key === integrity.limiting_pillar ? "is-limiting" : ""}
            key={pillar.key}
            onClick={(event) => {
              const issue = openIssues.find(
                (candidate) => issuePillar(candidate) === pillar.key,
              );
              if (issue) {
                openIssue(issue, event.currentTarget);
                return;
              }
              router.push(
                `/projects/${snapshot.project_id}/issues?pillar=${pillar.key.toLowerCase()}`,
              );
            }}
            type="button"
          >
            <span>
              <strong>
                {pillar.key}
                {pillar.key === integrity.limiting_pillar ? <em>Floor</em> : null}
              </strong>
              <b>{pillar.band}</b>
            </span>
            <i aria-hidden="true"><b style={{ width: `${pillar.basis * 100}%` }} /></i>
            <small>{pillar.why[0]}</small>
            <CaretRight aria-hidden="true" size={13} />
          </button>
        ))}
      </div>
    </section>
  );

  return (
    <main
      className={`project-shell ${isR2ReadView(initialView) ? "is-r2-slice-one" : ""} ${
        isArtifactView(initialView) ? "is-r2-artifact-workspace" : ""
      } ${initialView === "reports" || initialView === "full_plan" ? "is-r2-reports" : ""} ${
        initialView === "full_plan" ? "is-r2-full-plan" : ""
      } ${
        initialView === "outcome" ? "is-r2-outcome" : ""
      } ${
        r2IntegrityExpanded ? "r2-integrity-expanded" : ""
      } ${
        r2IntegrityDetailOpen ? "r2-integrity-detail-open" : ""
      } ${
        isR2ReadView(initialView) && initialView !== "overview"
          ? "r2-integrity-without-outcome-anchor"
          : ""
      } ${initialView === "overview" && snapshot.first_run?.freeze_on ? "is-first-run-frozen" : ""
      } ${selectedIssue ? "has-issue" : ""} ${
        orientation ? "is-touring" : ""
      }`}
      ref={r2Shell}
    >
      {initialView === "reports" || initialView === "full_plan" ? (
        <div aria-label="Reports product context" className="r2-reports-banner" role="note">
          <strong>OSLO · AI-first R2</strong>
          <div>
            <b>Official</b>
            <span>
              One walkable shell: the read is home · artifacts + execution plan in the center ·
              reasoning + chat on the right · Issues / History / Reports / Map as doors.
            </span>
          </div>
        </div>
      ) : null}
      <header className="project-header">
        <Link className="project-toolbar-brand" href="/workspace">
          <Image
            alt="Intralign"
            height={20}
            priority
            src={intralignLogo}
            unoptimized
            width={112}
          />
        </Link>
        <ProjectWorkspaceControls
          onOpenPlanSettings={() => {
            setSettingsSection("plan");
            setSettingsOpen(true);
          }}
          planPortalId="project-sidebar-plan"
          projectId={snapshot.project_id}
          projectName={projectTitle}
        />
        <div className={`project-context ${initialView === "overview" ? "is-overview" : ""}`}>
          {initialView === "overview" || isArtifactView(initialView) ? null : (
            <strong>{initialView === "outcome" ? "The read" : projectTitle}</strong>
          )}
          <span aria-hidden="true">›</span>
          <em>
            {initialView === "overview"
              ? "Issues"
              : initialView === "inference"
                ? "Inference map"
                : initialView === "grounding"
                  ? "Grounding map"
                  : initialView === "reports"
                    ? "Reports"
                    : initialView === "full_plan"
                      ? "Full plan · export"
                    : initialView === "outcome"
                      ? "Your Outcome"
                      : artifactLabel(initialView)}
          </em>
        </div>
        <button
          aria-label={`Outcome Integrity ${integrityReadLabel(integrity)}, limited by ${integrity.limiting_pillar}`}
          aria-expanded={confidenceBreakdownOpen}
          className={`project-header-confidence ${
            orientation && activeTourStep === 0 ? "is-tour-target" : ""
          }`}
          ref={integrityTrigger}
          onClick={() => {
            setSearchOpen(false);
            setConfidenceBreakdownOpen((current) => !current);
          }}
          type="button"
        >
          <span className="project-header-confidence-dot" />
          <span>Outcome Integrity</span>
          <strong>{integrityReadLabel(integrity)}</strong>
          <span aria-hidden="true" className="project-header-pillar-shape">
            {integrity.decomposition.map((pillar) => (
              <span
                className={`${pillar.key === integrity.limiting_pillar ? "is-limiting" : ""} is-${pillar.key.toLowerCase()}`}
                key={pillar.key}
              >
                {pillar.key} {pillar.band}
                <i><b style={{ width: `${pillar.basis * 100}%` }} /></i>
              </span>
            ))}
          </span>
          <small>as of this analysis</small>
        </button>
        <div className="project-actions">
          {(isR2ReadView(initialView) && !r2IntegrityExpanded) ||
          isArtifactView(initialView) ? (
            <button
              aria-controls="r2-integrity-summary"
              aria-expanded={r2IntegrityExpanded}
              aria-label={`${r2IntegrityExpanded ? "Collapse" : "Expand"} Outcome Integrity`}
              className="r2-integrity-toggle is-compact"
              onClick={() => setR2IntegrityExpanded((current) => !current)}
              type="button"
            >
              <CaretDown aria-hidden="true" size={13} />
            </button>
          ) : null}
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
        </div>
      </header>

      {(initialView === "overview" || (isArtifactView(initialView) && r2IntegrityExpanded)) &&
      (activeOutcome?.title ?? outcomeDefinition) ? (
        <div className="r2-outcome-capacity-row">
          <button
            aria-label={`Outcome: ${activeOutcome?.title ?? outcomeDefinition}`}
            className={`r2-outcome-anchor ${orientation && activeTourStep === 1 ? "is-tour-target" : ""}`}
            onClick={() => router.push(`/projects/${snapshot.project_id}/outcome`)}
            ref={tourOutcomeTarget}
            type="button"
          >
            <span aria-hidden="true">◎</span>
            <small>Outcome</small>
            <strong>{activeOutcome?.title ?? outcomeDefinition}</strong>
            <em>{activeOutcome?.provenance === "declared" ? "✓ yours" : "OSLO inference"}</em>
            <CaretRight aria-hidden="true" size={13} />
          </button>
        </div>
      ) : null}

      {isArtifactView(initialView) && r2IntegrityExpanded ? (
        <section
          aria-label="Outcome Integrity summary"
          className="r2-artifact-integrity"
          id="r2-integrity-summary"
        >
          <div className="r2-artifact-integrity-copy">
            <span>Outcome integrity</span>
            <strong>{integrityReadLabel(integrity)}</strong>
            <p>
              limited by <b>{integrity.limiting_pillar}</b> — a composite is only as sound
              as its weakest pillar
            </p>
            <small>
              {groundingPillar?.band === "Sound"
                ? "Load-bearing details rest on your evidence, not OSLO’s inferences."
                : "Load-bearing details still rest on OSLO’s inferences, not your evidence."}
            </small>
            <button
              aria-label="Collapse Outcome Integrity"
              onClick={() => setR2IntegrityExpanded(false)}
              type="button"
            >
              Collapse <CaretUp aria-hidden="true" size={11} />
            </button>
          </div>
          <div className="integrity-pillars">
            {integrity.decomposition.map((pillar) => (
              <button
                aria-label={`${pillar.key} ${pillar.band}`}
                className={pillar.key === integrity.limiting_pillar ? "is-limiting" : ""}
                key={pillar.key}
                onClick={(event) => {
                  const issue = openIssues.find(
                    (candidate) => issuePillar(candidate) === pillar.key,
                  );
                  if (issue) {
                    openIssue(issue, event.currentTarget);
                    return;
                  }
                  router.push(
                    `/projects/${snapshot.project_id}/issues?pillar=${pillar.key.toLowerCase()}`,
                  );
                }}
                type="button"
              >
                <span>
                  <strong>
                    {pillar.key}
                    {pillar.key === integrity.limiting_pillar ? <em>Floor</em> : null}
                  </strong>
                  <b>{pillar.band}</b>
                </span>
                <i aria-hidden="true"><b style={{ width: `${pillar.basis * 100}%` }} /></i>
                <small>{pillar.why[0]}</small>
                <CaretRight aria-hidden="true" size={13} />
              </button>
            ))}
          </div>
        </section>
      ) : null}

      {isR2ReadView(initialView) && initialView !== "overview" && r2IntegrityExpanded
        ? integritySummary
        : null}

      {confidenceBreakdownOpen ? (
        <IntegrityBreakdown
          assessment={snapshot.assessment}
          onClose={closeIntegrityBreakdown}
        />
      ) : null}

      <aside
        aria-label="Project navigation"
        className="workspace-sidebar"
        tabIndex={0}
      >
        <div className="workspace-sidebar-content">
        <p className="workspace-label">
          {isR2ReadView(initialView) || isArtifactView(initialView) ? "Views" : "Project"}
        </p>
        <nav aria-label="Workspace">
          {isR2ReadView(initialView) || isArtifactView(initialView) ? (
            <>
              <Link aria-current={initialView === "overview" || initialView === "issues" ? "page" : undefined} aria-label={`Issues ${openIssues.length}`} className={initialView === "overview" || initialView === "issues" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/issues`}>
                <ListBullets aria-hidden="true" size={17} />
                Issues
                <span className="nav-count">{openIssues.length}</span>
              </Link>
              <Link aria-current={initialView === "outcome" ? "page" : undefined} className={initialView === "outcome" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/outcome`}>
                <Diamond aria-hidden="true" size={17} />
                Your Outcome
              </Link>
              <Link aria-current={initialView === "grounding" ? "page" : undefined} className={initialView === "grounding" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/grounding`} onClick={rememberOverviewPosition}>
                <MapTrifold aria-hidden="true" size={17} />
                Grounding map
              </Link>
              <Link aria-current={initialView === "reports" ? "page" : undefined} className={initialView === "reports" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/reports`}>
                <FileText aria-hidden="true" size={17} />
                Reports
              </Link>
              <Link aria-current={initialView === "history" ? "page" : undefined} className={initialView === "history" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/history`}>
                <ClockCounterClockwise aria-hidden="true" size={17} />
                History
              </Link>
            </>
          ) : (
            <>
              <Link className="" href={`/projects/${snapshot.project_id}/overview`}>
                <House aria-hidden="true" size={17} /> Overview
              </Link>
              <Link aria-current={initialView === "issues" ? "page" : undefined} aria-label={`Issues ${openIssues.length}`} className={initialView === "issues" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/issues`}>
                <ListBullets aria-hidden="true" size={17} /> Issues <span className="nav-count">{openIssues.length}</span>
              </Link>
              <Link aria-current={initialView === "history" ? "page" : undefined} className={initialView === "history" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/history`}>
                <ClockCounterClockwise aria-hidden="true" size={17} /> History
              </Link>
              <Link aria-current={initialView === "inference" ? "page" : undefined} className={initialView === "inference" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/inference`}>
                <Diamond aria-hidden="true" size={17} /> Inference map
              </Link>
              <Link aria-current={initialView === "reports" ? "page" : undefined} className={initialView === "reports" ? "is-current" : ""} href={`/projects/${snapshot.project_id}/reports`}>
                <FileText aria-hidden="true" size={17} /> Reports
              </Link>
            </>
          )}
        </nav>
        <p className="workspace-label workspace-artifact-label">
          Documents
        </p>
        <div
          className={`workspace-artifact-group ${orientation && activeTourStep === 3 ? "is-tour-target" : ""}`}
          ref={tourPlanTarget}
        >
          <span>Understanding</span>
          {r2UnderstandingOrder.map((artifactType) => {
            const status = artifactSidebarStatus({
              artifactType,
              issues: openIssues,
              proposals: undecidedProposals,
              snapshot,
            });
            return (
              <Link
                className={initialView === artifactType ? "is-current" : ""}
                href={`/projects/${snapshot.project_id}/artifacts/${artifactType}`}
                key={artifactType}
              >
                <FileText aria-hidden="true" size={15} />
                {artifactLabel(artifactType)}
                <ArtifactSidebarIndicators status={status} />
              </Link>
            );
          })}
          <span>Execution</span>
          {artifactOrder.slice(4).map((artifactType) => {
            const status = artifactSidebarStatus({
              artifactType,
              issues: openIssues,
              proposals: undecidedProposals,
              snapshot,
            });
            return (
              <Link
                className={initialView === artifactType ? "is-current" : ""}
                href={`/projects/${snapshot.project_id}/artifacts/${artifactType}`}
                key={artifactType}
              >
                <FileText aria-hidden="true" size={15} />
                {initialView === "overview" && artifactType === "work_breakdown"
                  ? "Work breakdown"
                  : artifactLabel(artifactType)}
                <ArtifactSidebarIndicators execution status={status} />
              </Link>
            );
          })}
          <Link
            aria-current={initialView === "full_plan" ? "page" : undefined}
            className={initialView === "full_plan" ? "is-current" : ""}
            href={`/projects/${snapshot.project_id}/full-plan`}
          >
            <ArrowSquareOut aria-hidden="true" size={15} />
            Full plan · export
          </Link>
        </div>
        </div>
        <div className="workspace-sidebar-footer">
          <button
            onClick={() => beginTour()}
            type="button"
          >
            <Sparkle aria-hidden="true" size={15} />
            Take a quick tour
          </button>
          <button
            onClick={openFeedback}
            title="Report a defect, an idea, or anything else — straight to the team"
            type="button"
          >
            <PencilSimple aria-hidden="true" size={15} />
            Feedback
          </button>
          <div
            className="project-sidebar-plan-slot"
            id="project-sidebar-plan"
          />
          <details className="project-account project-sidebar-account" ref={accountMenu}>
            <summary
              aria-label={`Open account menu for ${displayName}`}
              ref={accountTrigger}
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
              <button
                onClick={() => {
                  accountMenu.current?.removeAttribute("open");
                  setSettingsSection("profile");
                  setSettingsOpen(true);
                }}
                type="button"
              >
                <Gear aria-hidden="true" size={16} />
                Settings
              </button>
              <button
                onClick={() => beginTour()}
                type="button"
              >
                <Target aria-hidden="true" size={16} />
                Take a quick tour
              </button>
              <button
                onClick={() => beginTour(true)}
                type="button"
              >
                <ClockCounterClockwise aria-hidden="true" size={16} />
                Replay walkthrough
              </button>
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

      <div className={`project-grid ${panelVisible ? "" : "is-panel-closed"} ${advisorWide ? "is-advisor-wide" : ""}`}>
        <section
          aria-label="Project content"
          className={`project-main ${snapshot.first_run?.freeze_on ? "is-first-run-frozen" : ""}`}
          ref={mainScrollRegion}
          tabIndex={0}
        >
          {issueActionFeedback ? (
            <section
              aria-label="Issue action recorded"
              className="r2-action-feedback r2-overview-notice"
              role="status"
            >
              <CheckCircle aria-hidden="true" size={32} weight="duotone" />
              <div>
                <small>Recorded</small>
                <strong>{issueActionFeedback.title}</strong>
                <p>{issueActionFeedback.detail}</p>
              </div>
              <span>{issueActionFeedback.target}</span>
            </section>
          ) : null}
          {initialView === "overview" ? (
            <>
              {!snapshot.first_run?.freeze_on &&
              !issueActionFeedback &&
              snapshot.freshness &&
              snapshot.freshness.state !== "fresh" ? (
                <section
                  aria-label="Read freshness"
                  className={`r2-read-freshness r2-overview-notice is-${snapshot.freshness?.state}`}
                >
                  <div>
                    <strong>
                      {snapshot.freshness?.state === "reanalyzing"
                        ? "Reanalyzing your latest changes…"
                        : "Your read is safely out of date."}
                    </strong>
                    <p>
                      The last completed read stays visible while OSLO consolidates{" "}
                      {snapshot.freshness?.pending_count || "your"} latest change
                      {snapshot.freshness?.pending_count === 1 ? "" : "s"}.
                    </p>
                  </div>
                  {snapshot.freshness?.state === "stale" ? (
                    <span className="r2-read-freshness-actions">
                      {snapshot.freshness.latest_pending_event_id ? (
                        <button
                          className="button"
                          disabled={reanalysisPending}
                          onClick={() => void undoLatestPendingAct()}
                          type="button"
                        >
                          Undo last change
                        </button>
                      ) : null}
                      <button
                        className="button"
                        disabled={reanalysisPending}
                        onClick={() => void runReanalysisNow()}
                        type="button"
                      >
                        {reanalysisPending ? "Queuing…" : "Reanalyze now"}
                      </button>
                    </span>
                  ) : (
                    <span className="r2-read-freshness-pulse" aria-hidden="true" />
                  )}
                </section>
              ) : null}
              {reanalysisFeedback ? (
                <p className="r2-reanalysis-feedback" role="status">{reanalysisFeedback}</p>
              ) : null}
              {snapshot.read_moved_notifications?.[0] && !snapshot.first_run?.freeze_on ? (
                <section className="r2-read-moved r2-overview-notice" role="status">
                  <Sparkle aria-hidden="true" size={16} weight="fill" />
                  <div>
                    <strong>
                      {snapshot.read_moved_notifications[0].previous_band ===
                      snapshot.read_moved_notifications[0].current_band
                        ? "Your read was updated."
                        : "Your read moved."}
                    </strong>
                    <p>
                      {snapshot.read_moved_notifications[0].previous_band ===
                      snapshot.read_moved_notifications[0].current_band
                        ? `Outcome Integrity remains ${snapshot.read_moved_notifications[0].current_band || integrity.level}`
                        : `${snapshot.read_moved_notifications[0].previous_band || "The previous read"} → ${snapshot.read_moved_notifications[0].current_band || integrity.level}`}
                      {snapshot.read_moved_notifications[0].settled_causes[0]
                        ? ` because ${snapshot.read_moved_notifications[0].settled_causes[0]}`
                        : " after your latest grounded change"}.
                    </p>
                  </div>
                </section>
              ) : null}
              {snapshot.first_run?.freeze_on ? (
                snapshot.first_run.grounding_act_count > 0 ? (
                  <div className="r2-first-run-focus-copy">
                    {showFirstRunRecorded ? (
                      <section className="r2-first-run-recorded r2-overview-notice" role="status">
                        <CheckCircle aria-hidden="true" size={34} weight="duotone" />
                        <div>
                          <small>Recorded</small>
                          <strong>You confirmed your outcome</strong>
                          <p>The read now rests on your goal, not OSLO&apos;s guess. OSLO will re-read to reflect it.</p>
                        </div>
                      </section>
                    ) : null}
                    <section className="r2-first-run-guide is-one-call" aria-label="First run guidance">
                      <LockSimple aria-hidden="true" size={16} weight="duotone" />
                      <div>
                        <strong>One call down - you confirmed your outcome.</strong>
                        <p>One more confirm opens your full workspace. OSLO waits a click away.</p>
                      </div>
                    </section>
                    <button
                      aria-label={`Start here: settle ${firstRunTargetIssue?.title ?? "the top issue"}`}
                      className="r2-first-run-start"
                      disabled={!firstRunTargetIssue}
                      onClick={(event) => {
                        const issue = firstRunTargetIssue;
                        if (!issue) return;
                        issueTrigger.current = event.currentTarget;
                        advisorStateBeforeIssue.current = false;
                        setAdvisorOpen(false);
                        setSelectedIssue(issue);
                        setClarificationAnswer("");
                        setClarificationError(null);
                        window.requestAnimationFrame(() => {
                          const panel = document.getElementById(`issue-detail-${issue.id}`);
                          if (typeof panel?.scrollIntoView === "function") {
                            panel.scrollIntoView({ behavior: "auto", block: "start" });
                          }
                          panel?.focus({ preventScroll: true });
                        });
                      }}
                      type="button"
                    >
                      <span>Start here</span>
                      <strong>Settle &quot;{firstRunTargetIssue?.title ?? "the top issue"}&quot;</strong>
                      <small>the most load-bearing detail OSLO still had to guess</small>
                      <CaretRight aria-hidden="true" size={14} />
                    </button>
                  </div>
                ) : (
                  <section className="r2-first-run-guide" aria-label="First run guidance">
                    <span>{snapshot.first_run.grounding_act_count} of {snapshot.first_run.unlock_threshold}</span>
                    <div>
                      <strong>Ground two decisions to open the full workspace.</strong>
                      <p>Your plan remains available. Start with the top issue; every confirmed, flagged, or routed decision counts.</p>
                    </div>
                  </section>
                )
              ) : null}
              <div className={`overview-stack ${hasFirstValue ? "has-first-value" : ""}`}>
              {r2IntegrityExpanded ? integritySummary : null}

              <section className="start-here">
                {workspaceNoticeOpen ? (
                  <div
                    className="r2-workspace-open-slot"
                    data-state="open"
                  >
                    <section
                      aria-label="Workspace open"
                      className="r2-workspace-open r2-overview-notice"
                    >
                    <span aria-hidden="true">✦</span>
                    <div>
                      <strong>Your workspace is open.</strong>
                      <p>Your plan documents are on the left and OSLO&apos;s reasoning is on the right — every pillar and open issue travels with them.</p>
                      <div><small>New to OSLO?</small><button onClick={() => beginTour()} type="button">Take a 30-second tour →</button><button onClick={dismissWorkspaceNotice} type="button">No thanks</button></div>
                    </div>
                      <button aria-label="Dismiss workspace open message" onClick={dismissWorkspaceNotice} type="button">×</button>
                    </section>
                  </div>
                ) : null}
                <div className="overview-label r2-worklist-label">
                  <p>Your work — most important first</p>
                  <span>Do them top to bottom; the order re-ranks itself as you go.</span>
                </div>
                <div
                  aria-label="Exposure-ranked issue queue"
                  className="issue-list"
                  role="region"
                >
                  {displayRankedIssues.map((issue, index) => {
                    const isSelected = selectedIssue?.id === issue.id;
                    return (
                      <Fragment key={issue.id}>
                        {isSelected ? issuePanel : (
                          <button
                            aria-controls={`issue-detail-${issue.id}`}
                            aria-expanded={false}
                            className={`issue-row issue-row-${issue.severity.toLowerCase()} ${
                              orientation && activeTourStep === 2 && index === 0
                                ? "is-tour-target"
                                : ""
                            }`}
                            data-issue-id={issue.id}
                            onClick={(event) => openIssue(issue, event.currentTarget)}
                            ref={index === 0 ? tourReadTarget : undefined}
                            type="button"
                          >
                            <span className="r2-issue-rank">{index + 1}</span>
                            <span className="r2-issue-copy">
                              {index === 0 ? <b>◆ Do this next</b> : null}
                              <strong>{issue.title}</strong>
                              <small><em>Holds up</em> {issue.why}</small>
                            </span>
                            <span className={`r2-pillar r2-pillar-${issuePillar(issue).toLowerCase()}`}>
                              {issuePillar(issue)}
                            </span>
                            <span className={`severity severity-${issue.severity.toLowerCase()}`}>
                              {issue.severity}
                            </span>
                            <CaretRight aria-hidden="true" className="r2-issue-caret" size={13} />
                          </button>
                        )}
                      </Fragment>
                    );
                  })}
                  {selectedIssue && !displayRankedIssues.some((issue) => issue.id === selectedIssue.id)
                    ? issuePanel
                    : null}
                </div>
                {!displayRankedIssues.length ? (
                  <section className="r2-cleared-start" aria-label="Start here" role="status">
                    <strong>{compactFilterActive ? "No issues match this lens." : "✦ Start here"}</strong>
                    <span>
                      {compactFilterActive
                        ? "Clear the current filters to return to the full issue queue."
                        : displayActedIssues.length
                        ? "Finish the acted-on items below; they are not closed until reanalysis verifies them."
                        : displayAwaitingEvidenceIssues.length
                          ? "Review the evidence requests below while OSLO keeps their answers attributed."
                          : displayUndecidedProposals.length
                            ? "Decide the itemized OSLO proposals below; each one stays optional until you accept it."
                            : "Your exposure-ranked worklist is clear. Review the settled items below or continue with your plan."}
                    </span>
                  </section>
                ) : null}
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
                <IssueProposalGroup
                  onDecision={(proposal, accepted) =>
                    decideProposal(proposal, accepted, "folded_read")
                  }
                  onToggle={() => setProposalOpen((current) => !current)}
                  open={proposalOpen}
                  pendingId={proposalActionPending}
                  proposals={displayUndecidedProposals}
                  surface="folded_read"
                />
                <IssueLifecycleTray
                  issues={displayAwaitingEvidenceIssues}
                  kind="awaiting"
                  label="Awaiting evidence"
                  onAct={actOnIssueLifecycle}
                  onToggle={() => setAwaitingOpen((current) => !current)}
                  onView={openIssue}
                  open={awaitingOpen}
                />
                <IssueLifecycleTray
                  issues={displayActedIssues}
                  kind="acted"
                  label="Acted on, not yet closed"
                  onAct={actOnIssueLifecycle}
                  onToggle={() => setActedOpen((current) => !current)}
                  onView={openIssue}
                  open={actedOpen}
                />
                <IssueLifecycleTray
                  countLabel={`${displayResolvedIssues.length} of ${compactFilterActive ? compactScopedIssues.length : snapshot.assessment.issues.length} settled`}
                  issues={displayResolvedIssues}
                  kind="resolved"
                  label="Resolved"
                  onAct={actOnIssueLifecycle}
                  onToggle={() => setResolvedOpen((current) => !current)}
                  onView={openIssue}
                  open={resolvedOpen}
                />
                {issueActionError && !selectedIssue ? (
                  <p className="r2-lifecycle-error" role="alert">{issueActionError}</p>
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
                          <strong>{settledIssueCount}</strong>
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
                  <span>{visibleSummary}</span>
                  <CaretDown
                    aria-hidden="true"
                    className={summaryOpen ? "is-open" : ""}
                    size={13}
                  />
                </button>
                {summaryOpen ? <p>{visibleSummary}</p> : null}
              </section>
              </div>
              {initialView !== "overview" ? issuePanel : null}
            </>
          ) : initialView === "outcome" && initialOutcomeDashboard ? (
            <YourOutcomeDashboard
              data={initialOutcomeDashboard}
              onDismissWorkspaceNotice={dismissWorkspaceNotice}
              onTakeTour={() => {
                beginTour();
              }}
              workspaceNoticeOpen={workspaceNoticeOpen}
            />
          ) : initialView === "rollup" && initialRollUp ? (
            <CollaborationRollUp data={initialRollUp} />
          ) : initialView === "grounding" && initialGroundingMap ? (
            <CollaborationGroundingMap data={initialGroundingMap} />
          ) : initialView === "inference" ? (
            <InferenceMap onOpenIssue={openIssue} snapshot={snapshot} />
          ) : isArtifactView(initialView) ? (
            <>
              {workspaceNoticeOpen ? (
                <section aria-label="Workspace open" className="r2-artifact-workspace-open">
                  <Sparkle aria-hidden="true" size={20} weight="fill" />
                  <div>
                    <strong>Your workspace is open.</strong>
                    <p>
                      Your two calls unlocked the full read. <b>Now live:</b> your plan
                      documents on the left and <b>OSLO&apos;s reasoning</b> on the right —
                      every pillar and open issue with them.
                    </p>
                    <div>
                      <small>New to OSLO?</small>
                      <button
                        onClick={() => beginTour()}
                        type="button"
                      >
                        Take a 30-second tour →
                      </button>
                      <button onClick={dismissWorkspaceNotice} type="button">
                        No thanks
                      </button>
                    </div>
                  </div>
                  <button
                    aria-label="Dismiss workspace open message"
                    onClick={dismissWorkspaceNotice}
                    type="button"
                  >
                    <X aria-hidden="true" size={14} />
                  </button>
                </section>
              ) : null}
              <ArtifactWorkspace
              analysisRunning={Boolean(analysisUpdateRunId)}
              artifactType={initialView}
              initialFocus={initialView === "intent" ? initialArtifactFocus : undefined}
              onAnalysisStarted={setAnalysisUpdateRunId}
              onAskOslo={(prompt) => {
                setAdvisorOpen(true);
                void askQuestion(prompt);
              }}
              onOpenIssue={openIssue}
              onProposalDecision={(proposal, accepted) =>
                decideProposal(proposal, accepted, "artifact")
              }
              proposalError={issueActionError}
              proposalPending={proposalActionPending}
              proposals={undecidedProposals.filter(
                (proposal) =>
                  proposal.artifact_type === persistedArtifactType(initialView),
              )}
              projectId={snapshot.project_id}
              returnToOutcome={initialView === "intent" && returnToOutcome}
              />
            </>
          ) : initialView === "issues" ? (
            <IssuesWorkspace
              initialFilters={initialIssueFilters}
              issues={snapshot.assessment.issues}
              limitingPillar={snapshot.assessment.integrity.limiting_pillar}
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
          ) : initialView === "full_plan" ? (
            <FullPlanWorkspace proposals={undecidedProposals} snapshot={snapshot} />
          ) : (
            <DeferredWorkspace />
          )}
        </section>

        {issueSidepanelVisible ? issuePanel : advisorVisible ? (
          <div
            className="project-sidepanel-slot"
          >
            <AdvisorPanel
            advisorError={advisorError}
            advisorPending={advisorPending}
            advisorQuestions={isArtifactView(initialView)
              ? [
                  "What’s OSLO’s read here?",
                  `Show me the ${artifactAdvisorIssues.length} open ${artifactAdvisorIssues.length === 1 ? "question" : "questions"}`,
                  "What should I do here?",
                ]
              : advisorQuestions}
            contextLabel={isArtifactView(initialView) ? artifactLabel(initialView) : null}
            extendedFailed={extendedFailed}
            extendedFailure={extendedFailure}
            extendedRetryError={extendedRetryError}
            extendedRetrying={extendedRetrying}
            integrity={integrity}
            isProvisional={isProvisional}
            messages={messages}
            onAsk={askQuestion}
            onClose={() => setAdvisorOpen(false)}
            onQuestionChange={setQuestion}
            onRetry={retryExtendedAnalysis}
            onSubmit={submitQuestion}
            onWideChange={setAdvisorWide}
            openIssueCount={openIssues.length}
            question={question}
            resolvedIssueCount={settledIssueCount}
            r2Mode
            topIssue={artifactAdvisorIssues[0] ?? openIssues[0] ?? null}
            tourTarget={orientation && activeTourStep === 4 ? tourAdvisorTarget : undefined}
            wide={advisorWide}
            />
          </div>
        ) : null}
      </div>

      {!advisorVisible ? (
        <button
          aria-label="Ask OSLO"
          className="advisor-floating"
          onClick={() => {
            if (issueSidepanelVisible) setSelectedIssue(null);
            setAdvisorOpen(true);
          }}
          type="button"
        >
          <Sparkle aria-hidden="true" size={14} weight="fill" />
          <span>Ask OSLO</span>
        </button>
      ) : null}

      <footer className="project-advisory">
        <Info aria-hidden="true" size={12} />
        OSLO advises; you decide — you stay in control at every step.
      </footer>

      <WorkspaceSettingsDialog
        displayName={displayName}
        initialSection={settingsSection}
        onClose={() => {
          setSettingsOpen(false);
          window.requestAnimationFrame(() => accountTrigger.current?.focus());
        }}
        open={settingsOpen}
      />

      {orientation ? (
        <>
          <div
            aria-hidden="true"
            className="orientation-overlay"
            data-step={activeTourStep + 1}
          />
          <section
            aria-label="How OSLO works"
            aria-modal="true"
            className="tour-card orientation-tour-card"
            ref={tourCard}
            role="dialog"
          >
            <span className="tour-step-label">Step {activeTourStep + 1} of {orientationSteps.length}</span>
            <h2>{orientationSteps[activeTourStep].title}</h2>
            <p>{orientationSteps[activeTourStep].body}</p>
            <div className="tour-actions">
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
                {activeTourStep === orientationSteps.length - 1 ? (
                  <>Done <CheckCircle aria-hidden="true" size={14} weight="fill" /></>
                ) : (
                  <>Next <ArrowRight aria-hidden="true" size={14} /></>
                )}
              </button>
              <button className="tour-skip" onClick={() => void dismissOrientation()} type="button">Skip tour</button>
            </div>
          </section>
        </>
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

      {feedbackOpen ? (
        <div
          className="workspace-modal-backdrop r2-feedback-backdrop"
          onMouseDown={(event) => {
            if (event.currentTarget === event.target) setFeedbackOpen(false);
          }}
          role="presentation"
        >
          <section
            aria-label="Feedback"
            aria-modal="true"
            className="r2-feedback-dialog"
            ref={feedbackDialog}
            role="dialog"
            tabIndex={-1}
          >
            <header>
              <h2>Feedback</h2>
              <p>tell us what’s broken or missing — it goes straight to the team</p>
              <button aria-label="Close feedback" onClick={() => setFeedbackOpen(false)} type="button">
                <X aria-hidden="true" size={18} />
              </button>
            </header>
            {feedbackTicket ? (
              <div className="r2-feedback-success" role="status">
                <CheckCircle aria-hidden="true" size={28} weight="fill" />
                <strong>Filed — your feedback is with the team.</strong>
                <span className="r2-feedback-ticket-id">{feedbackTicket.ticket_id}</span>
                <p>Your read, band, and project content were not changed.</p>
                <div>
                  <button
                    className="button"
                    onClick={() => {
                      setFeedbackTicket(null);
                      setFeedbackText("");
                      setFeedbackExpected("");
                    }}
                    type="button"
                  >
                    Add another
                  </button>
                  <button className="button" onClick={() => setFeedbackOpen(false)} type="button">Close</button>
                </div>
                <FeedbackSessionList tickets={feedbackTickets} />
              </div>
            ) : (
              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  void submitFeedback();
                }}
              >
                <p>Tell us what’s <strong>broken or missing</strong> — it’s filed as a ticket straight to the team. It never changes your read, your band, or your issues.</p>
                <div className="r2-feedback-title">
                  <PencilSimple aria-hidden="true" size={16} weight="fill" />
                  <div><strong>Report feedback</strong><small>A defect, an idea, or anything else on your mind — filed as a ticket to the team.</small></div>
                </div>
                <div aria-label="Feedback type" className="r2-feedback-kinds" role="group">
                  {feedbackKinds.map((kind) => (
                    <button
                      aria-pressed={feedbackKind === kind.id}
                      className={feedbackKind === kind.id ? "is-selected" : ""}
                      key={kind.id}
                      onClick={() => {
                        setFeedbackKind(kind.id);
                        if (kind.id !== "broken") setFeedbackExpected("");
                      }}
                      type="button"
                    >
                      <strong>{kind.title}</strong>
                      <small>{kind.detail}</small>
                    </button>
                  ))}
                </div>
                <label className="sr-only" htmlFor="r2-feedback-text">What happened?</label>
                <textarea
                  id="r2-feedback-text"
                  onChange={(event) => setFeedbackText(event.target.value)}
                  placeholder="What happened? (the step you took, and what went wrong)"
                  required
                  value={feedbackText}
                />
                {feedbackKind === "broken" ? (
                  <>
                    <label className="sr-only" htmlFor="r2-feedback-expected">What did you expect?</label>
                    <textarea
                      id="r2-feedback-expected"
                      onChange={(event) => setFeedbackExpected(event.target.value)}
                      placeholder="What did you expect to happen instead? (optional)"
                      value={feedbackExpected}
                    />
                    <fieldset className="r2-feedback-impact">
                      <legend>How much is it getting in your way?</legend>
                      <div>
                        {feedbackImpacts.map((impact) => (
                          <button
                            aria-pressed={feedbackImpact === impact}
                            className={feedbackImpact === impact ? "is-selected" : ""}
                            key={impact}
                            onClick={() => setFeedbackImpact(impact)}
                            type="button"
                          >
                            {impact}
                          </button>
                        ))}
                      </div>
                    </fieldset>
                  </>
                ) : null}
                <div className="r2-feedback-context">
                  <strong>↳ Auto-attached to the ticket, so we can reproduce it:</strong>
                  <span>{initialView === "overview" ? "Issues" : artifactLabel(initialView)} · workspace user · {snapshot.assessment.issues.filter((issue) => issue.status === "resolved").length}/{snapshot.assessment.issues.length} grounded</span>
                  <small>nothing from your plan’s content leaves — just this location + state.</small>
                </div>
                {feedbackError ? <p className="r2-feedback-error" role="alert">{feedbackError}</p> : null}
                <button className="button button-primary" disabled={feedbackPending} type="submit">
                  {feedbackPending
                    ? "Filing feedback…"
                    : feedbackError
                      ? "Try again"
                      : `${feedbackKind === "broken" ? "File defect" : feedbackKind === "missing" ? "Request enhancement" : "Send feedback"} →`}
                </button>
                {feedbackListPending ? <p className="r2-feedback-list-state" role="status">Loading filed feedback…</p> : null}
                {feedbackListError ? (
                  <p className="r2-feedback-list-state" role="alert">
                    {feedbackListError} Close and reopen Feedback to retry.
                  </p>
                ) : null}
                <FeedbackSessionList tickets={feedbackTickets} />
              </form>
            )}
            <small>Feedback is for us — it never moves your read or your band.</small>
          </section>
        </div>
      ) : null}
    </main>
  );
}

function FeedbackSessionList({ tickets }: { tickets: FeedbackTicketSummary[] }) {
  if (!tickets.length) return null;
  return (
    <section aria-label="Filed this session" className="r2-feedback-filed">
      <h3>Filed this session</h3>
      <ul>
        {tickets.map((ticket) => (
          <li key={ticket.ticket_id}>
            <strong>{ticket.ticket_id}</strong>
            <span>{ticket.title}</span>
            <small>{ticket.status}</small>
          </li>
        ))}
      </ul>
    </section>
  );
}

function IntegrityBreakdown({
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
      aria-label="Integrity breakdown"
      className="confidence-breakdown"
      onKeyDown={(event) => {
        if (event.key === "Escape") onClose();
      }}
      role="dialog"
    >
      <div className="confidence-breakdown-heading">
        <div>
          <span>Outcome Integrity</span>
          <strong>{integrityReadLabel(assessment.integrity)}</strong>
          <em>limited by {assessment.integrity.limiting_pillar}</em>
        </div>
        <button aria-label="Close integrity breakdown" onClick={onClose} ref={closeButton} type="button">
          <X aria-hidden="true" size={16} />
        </button>
      </div>
      <p>
        Moment-in-time maturity — not project health, readiness, or probability.
        Live tracking begins at execution.
      </p>
      <dl className="confidence-breakdown-dimensions">
        {assessment.integrity.decomposition.map((pillar) => (
          <div key={pillar.key}>
            <dt>{pillar.key}</dt>
            <dd>
              <i><b style={{ width: `${pillar.basis * 100}%` }} /></i>
              <strong>{pillar.band}</strong>
            </dd>
            <small>{pillar.why.join(" ")}</small>
          </div>
        ))}
      </dl>
      <small>The lowest pillar sets the overall integrity level.</small>
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

type IssueGroupMode = "exposure" | "dimension" | "severity" | "artifact";

function IssuesWorkspace({
  initialFilters,
  issues,
  limitingPillar,
  onOpenIssue,
  projectId,
}: {
  initialFilters: IssueFilters;
  issues: Issue[];
  limitingPillar: string;
  onOpenIssue: (issue: Issue, trigger?: HTMLElement | null) => void;
  projectId: string;
}) {
  const router = useRouter();
  const [groupMode, setGroupMode] = useState<IssueGroupMode>("exposure");
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
    if (groupMode === "exposure") return [];
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

  const activeIssues = useMemo(
    () => issues.filter((issue) => issue.status !== "resolved").sort(issueSort),
    [issues],
  );
  const resolvedIssues = useMemo(
    () => issues.filter((issue) => issue.status === "resolved").sort(issueSort),
    [issues],
  );
  const activeCount = activeIssues.length;
  const pillarCounts = useMemo(
    () =>
      activeIssues.reduce<Record<string, number>>(
        (counts, issue) => ({
          ...counts,
          [issuePillar(issue)]: (counts[issuePillar(issue)] ?? 0) + 1,
        }),
        { Viability: 0, Grounding: 0, Adaptability: 0 },
      ),
    [activeIssues],
  );
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

  const renderIssueCard = (issue: Issue, settled = false) => (
    <button
      aria-label={`${issue.title}, ${issue.severity}, ${artifactLabel(issue.artifact_type)}, ${issue.dimension}, ${artifactLabel(issue.status)}. Open issue`}
      className={`issue-layer-card issue-workspace-card issue-card-${issue.severity.toLowerCase()} ${
        issuePillar(issue) === limitingPillar ? "is-gating" : ""
      } ${settled ? "is-settled" : ""}`}
      key={issue.id}
      onClick={(event) => onOpenIssue(issue, event.currentTarget)}
      type="button"
    >
      <span className="issue-layer-tags">
        <b className={`issue-layer-pillar pillar-${issuePillar(issue).toLowerCase()}`}>
          {issuePillar(issue)}
          {issuePillar(issue) === limitingPillar ? " · gating" : ""}
        </b>
        <em>{issue.clarification ? "Clarification" : "Finding"}</em>
        {!settled ? (
          <i aria-label={`Exposure rank ${issue.exposure_rank ?? 0}`}>
            {Array.from({ length: 4 }, (_, index) => (
              <span
                className={
                  index < Math.min(4, Math.max(1, issue.exposure_rank ?? 1))
                    ? "is-on"
                    : ""
                }
                key={index}
              />
            ))}
          </i>
        ) : null}
      </span>
      <span className="issue-layer-title">
        <b className={`severity severity-${issue.severity.toLowerCase()}`}>
          {settled ? "✓" : issue.severity}
        </b>
        <strong>{issue.title}</strong>
      </span>
      <span className="issue-layer-detail">{issue.why}</span>
      <span className="issue-layer-footer">
        <small>{artifactLabel(issue.artifact_type)} · {artifactLabel(issue.dimension)}</small>
        <b>{settled ? "Resolved" : "Open issue →"}</b>
      </span>
    </button>
  );

  return (
    <section className="issues-workspace">
      <header className="issues-heading">
        <div>
          <h1>Issues</h1>
          <p>where the plan is weak — all open issues</p>
        </div>
        <strong>{activeCount} open</strong>
        <span className="sr-only">
          {activeCount} active {activeCount === 1 ? "finding" : "findings"}
        </span>
      </header>

      <section className="issue-layer-intro" aria-labelledby="issue-layer-title">
        <h2 id="issue-layer-title">The issue layer</h2>
        <p>
          Every weakness across all three pillars — <b>one layer, exposure-ranked</b>.
          Resolving an issue strengthens its pillar; the read is only as sound as its
          weakest one, so <b>{limitingPillar}</b> gates it.
        </p>
        <div aria-label="Issue layer dimensions" className="issue-layer-dimensions">
          {["Viability", "Grounding", "Adaptability"].map((pillar) => (
            <span className={pillar === limitingPillar ? "is-gating" : ""} key={pillar}>
              {`${pillar} ${pillarCounts[pillar] ?? 0}${
                pillar === limitingPillar ? " · gating" : ""
              }`}
            </span>
          ))}
        </div>
      </section>

      <details className="issue-refine" open={hasExplicitFilters || undefined}>
        <summary>Refine issue view</summary>
        <div aria-label="Issue grouping" className="issue-group-tabs">
          {(["exposure", "dimension", "severity", "artifact"] as const).map((mode) => (
            <button
              aria-pressed={groupMode === mode}
              key={mode}
              onClick={() => setGroupMode(mode)}
              type="button"
            >
              {mode === "exposure" ? "Exposure ranked" : `By ${mode}`}
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
      </details>

      {hiddenCount ? (
        <div className="issue-filter-summary" role="status">
          <span>
            {hiddenCount} {hiddenCount === 1 ? "finding" : "findings"} hidden by the
            current filters.
          </span>
          <button onClick={clearFilters} type="button">Clear filters</button>
        </div>
      ) : null}

      {filteredIssues.length ? (
        <div className="issue-groups">
          {groupMode === "exposure"
            ? filteredIssues.map((issue) => renderIssueCard(issue))
            : groups.map(([group, groupIssues]) => (
                <section className="issue-group" key={group}>
                  <h2>{group} · {groupIssues.length}</h2>
                  <div>{groupIssues.map((issue) => renderIssueCard(issue))}</div>
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

      {statusFilter === "active" &&
      !artifactFilter &&
      !dimensionFilter &&
      !severityFilter &&
      resolvedIssues.length ? (
        <section className="issue-settled-layer">
          <h2>Resolved · {resolvedIssues.length}</h2>
          <div>{resolvedIssues.map((issue) => renderIssueCard(issue, true))}</div>
        </section>
      ) : null}

      <p className="issues-workspace-footnote">
        Select an issue to open the governed detail, review its evidence, and choose an
        available action. Viewing or filtering never changes the read.
      </p>
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

type IssueLifecycleActOptions = {
  basis?: IssueBasis | null;
  evidenceRef?: string | null;
  resolution?: string | null;
  reviewer?: { id: string; display_name: string; role: string } | null;
};

function IssueProposalGroup({
  onDecision,
  onToggle,
  open,
  pendingId,
  proposals,
  surface,
}: {
  onDecision: (proposal: IssueProposalSummary, accepted: boolean) => void;
  onToggle: () => void;
  open: boolean;
  pendingId: string | null;
  proposals: IssueProposalSummary[];
  surface: "issue_card" | "folded_read";
}) {
  if (!proposals.length) return null;
  return (
    <section
      aria-label="OSLO proposes"
      className={`r2-proposal-group ${surface === "issue_card" ? "is-issue-card" : ""}`}
      role="region"
    >
      <button
        aria-expanded={open}
        className="r2-proposal-heading"
        onClick={onToggle}
        type="button"
      >
        <span><CaretDown aria-hidden="true" size={12} /> <i aria-hidden="true">◆</i> OSLO proposes</span>
        <strong>{proposals.length} optional addition{proposals.length === 1 ? "" : "s"}</strong>
      </button>
      <div
        aria-hidden={!open}
        className={`r2-proposal-body ${open ? "" : "is-collapsed"}`}
        inert={!open}
      >
          <p>
            Beyond what your plan rests on — <strong>accept or reject each, here.</strong>{" "}
            Optional: these round out your plan; they don&apos;t move your integrity band,
            and nothing enters until you decide.
          </p>
          {proposals.map((proposal) => (
            <article className="r2-proposal-row" key={proposal.id}>
              <span aria-hidden="true">◆</span>
              <div>
                <strong>{proposal.title}</strong>
                <small><b>Why:</b> {proposal.rationale} · in {artifactLabel(proposal.artifact_type ?? "plan")}</small>
              </div>
              <div>
                <button
                  aria-label={`Accept ${proposal.title}`}
                  disabled={pendingId === proposal.id}
                  onClick={() => onDecision(proposal, true)}
                  type="button"
                >
                  {pendingId === proposal.id ? "Saving…" : "Accept"}
                </button>
                <button
                  aria-label={`Reject ${proposal.title}`}
                  disabled={pendingId === proposal.id}
                  onClick={() => onDecision(proposal, false)}
                  type="button"
                >
                  Reject
                </button>
              </div>
            </article>
          ))}
      </div>
    </section>
  );
}

function issueAttestationVerb(issue: Issue): string {
  if (issue.status === "needs_fix") return "Flagged by";
  if (issue.status === "needs_grounding") return "Answered by";
  return "Confirmed by";
}

function IssueLifecycleTray({
  countLabel,
  issues,
  kind,
  label,
  onAct,
  onToggle,
  onView,
  open,
}: {
  countLabel?: string;
  issues: Issue[];
  kind: "awaiting" | "acted" | "resolved";
  label: string;
  onAct: (issue: Issue, act: IssueLifecycleAct, options?: IssueLifecycleActOptions) => void;
  onToggle: () => void;
  onView: (issue: Issue, trigger?: HTMLElement | null) => void;
  open: boolean;
}) {
  if (!issues.length && kind !== "resolved") return null;
  const statusCount = kind === "acted"
    ? `${issues.filter((issue) => issue.status === "needs_fix").length} to fix · ${
      issues.filter((issue) => issue.status === "needs_grounding").length
    } to ground`
    : `${issues.length}`;
  return (
    <section aria-label={label} className={`r2-lifecycle-tray is-${kind}`} role="region">
      <button
        aria-expanded={open}
        className="r2-tray-heading"
        onClick={onToggle}
        type="button"
      >
        <span><CaretDown aria-hidden="true" size={12} /> {kind === "resolved" ? "✓" : "◇"} {label}</span>
        <strong>{countLabel ?? statusCount}</strong>
      </button>
      <div
        aria-hidden={!open}
        className={`r2-tray-body ${open ? "" : "is-collapsed"}`}
        inert={!open}
      >
          {issues.map((issue) => (
            <article className="r2-tray-row" key={issue.id}>
              <span aria-hidden="true">{kind === "resolved" ? "✓" : "○"}</span>
              <div>
                <strong>{issue.title}</strong>
                {issue.attested_by ? (
                  <small>{artifactLabel(issue.basis ?? "documented")} · {issueAttestationVerb(issue)} {issue.attested_by.display_name}</small>
                ) : null}
              </div>
              <span className={`r2-pillar r2-pillar-${issuePillar(issue).toLowerCase()}`}>
                {issuePillar(issue)}
              </span>
              <div className="r2-tray-actions">
                {issue.status === "needs_fix" ? (
                  <button
                    onClick={() => onAct(issue, "fix", { resolution: issue.recommendation })}
                    type="button"
                  >Fix it in your plan</button>
                ) : null}
                {issue.status === "needs_grounding" ? (
                  <button
                    onClick={() => onAct(issue, "ground", {
                      basis: "verified-directly",
                      evidenceRef: issue.evidence_refs.at(0) ?? `user:direct-confirm:${issue.id}`,
                    })}
                    type="button"
                  >Ground it on evidence</button>
                ) : null}
                {issue.status === "addressed" ? <span>Waiting for reanalysis</span> : null}
                <button
                  aria-label={`View ${issue.title}`}
                  onClick={(event) => onView(issue, event.currentTarget)}
                  type="button"
                >View →</button>
                <button onClick={() => onAct(issue, "withdraw")} type="button">Withdraw</button>
              </div>
            </article>
          ))}
      </div>
    </section>
  );
}

function IssuePanel({
  analysisRunning,
  answer,
  error,
  firstRunFocus,
  inline,
  issue,
  projectId,
  onAnswerChange,
  onAsk,
  onClose,
  onIssueAction,
  onLifecycleAct,
  onProposalDecision,
  onSubmit,
  pending,
  proposalPending,
  proposals,
  selectedResolution,
}: {
  analysisRunning: boolean;
  answer: string;
  error: string | null;
  firstRunFocus: boolean;
  inline: boolean;
  issue: Issue;
  projectId: string;
  onAnswerChange: (value: string) => void;
  onAsk: () => void;
  onClose: () => void;
  onIssueAction: (
    action: "select" | "apply" | "custom",
    resolution: string,
  ) => Promise<void>;
  onLifecycleAct: (
    act: IssueLifecycleAct,
    options?: IssueLifecycleActOptions,
  ) => Promise<void>;
  onProposalDecision: (proposal: IssueProposalSummary, accepted: boolean) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  pending: boolean;
  proposalPending: string | null;
  proposals: IssueProposalSummary[];
  selectedResolution: string | null;
}) {
  const closeButton = useRef<HTMLButtonElement>(null);
  const panel = useRef<HTMLElement>(null);
  const reviewComposer = useRef<HTMLElement>(null);
  const [clarificationOpen, setClarificationOpen] = useState(false);
  const [evidenceOpen, setEvidenceOpen] = useState(false);
  const [whyMattersOpen, setWhyMattersOpen] = useState(false);
  const [proposalsOpen, setProposalsOpen] = useState(true);
  const [otherWaysOpen, setOtherWaysOpen] = useState(false);
  const [routingOpen, setRoutingOpen] = useState(false);
  const [discussionVisible, setDiscussionVisible] = useState(false);
  const [customResolution, setCustomResolution] = useState("");
  const [customResolutionOpen, setCustomResolutionOpen] = useState(false);
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
  const [reviewGrantId, setReviewGrantId] = useState("");
  const [reviewDeliveryState, setReviewDeliveryState] = useState("");
  const [reviewCopied, setReviewCopied] = useState(false);
  const [externalComposerOpen, setExternalComposerOpen] = useState(false);
  const evidence = issue.evidence ?? [];
  const scopedSource = evidence.at(0);
  const scopedQuestion = issue.clarification?.trim() || issue.title;
  const scopedSourceRef = issue.evidence_refs.at(0)
    ?? (scopedSource ? `${scopedSource.source_name} · ${scopedSource.location}` : "");
  const scopedSourceExcerpt = scopedSource?.excerpt?.trim() ?? "";
  const externalReviewReady = Boolean(scopedQuestion && scopedSourceRef && scopedSourceExcerpt);
  const effectiveStatus = issue.status;
  const routeIssue = async (reviewer: { id: string; display_name: string; role: string }) => {
    if (reviewer.role === "external") {
      setRoutingOpen(false);
      setExternalComposerOpen(true);
      setCollaborationError(
        externalReviewReady
          ? "Add the external reviewer below. The preview shows their exact scope."
          : "This issue has no cited source excerpt, so it cannot be sent externally yet.",
      );
      requestAnimationFrame(() => reviewComposer.current?.scrollIntoView?.({ block: "nearest" }));
      return;
    }
    setReviewPending(true);
    setCollaborationError("");
    try {
      await onLifecycleAct("route", { reviewer });
      setRoutingOpen(false);
    } catch (caught) {
      setCollaborationError(
        caught instanceof Error ? caught.message : "Review route could not be created.",
      );
    } finally {
      setReviewPending(false);
    }
  };

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
      setDiscussionVisible(true);
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
    if (!externalReviewReady) {
      setCollaborationError(
        "This issue needs a cited source excerpt before it can be sent externally.",
      );
      return;
    }
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
          question: scopedQuestion,
          sourceRef: scopedSourceRef,
          sourceExcerpt: scopedSourceExcerpt,
        }),
      });
      const created = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(created.message ?? "Review link could not be created.");
      setReviewLink(created.url);
      setReviewGrantId(created.id);
      setReviewDeliveryState(created.delivery_state ?? "draft");
      if (created.delivery_state === "awaiting") {
        await onLifecycleAct("route", {
          reviewer: {
            id: created.id,
            display_name: reviewerName.trim(),
            role: "external",
          },
        });
      }
    } catch (caught) {
      setCollaborationError(
        caught instanceof Error ? caught.message : "Review link could not be created.",
      );
    } finally {
      setReviewPending(false);
    }
  };

  const copyReviewLink = async () => {
    if (!reviewLink || !reviewGrantId) return;
    setReviewPending(true);
    setCollaborationError("");
    try {
      await navigator.clipboard.writeText(reviewLink);
      if (reviewDeliveryState !== "awaiting") {
        const response = await fetch(`/api/projects/${projectId}/collaboration`, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            action: "review_delivered",
            grantId: reviewGrantId,
          }),
        });
        const delivered = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(delivered.message ?? "The review handoff could not be confirmed.");
        }
        await onLifecycleAct("route", {
          reviewer: {
            id: reviewGrantId,
            display_name: reviewerName.trim() || "External evidence holder",
            role: "external",
          },
        });
        setReviewDeliveryState(delivered.delivery_state ?? "awaiting");
      }
      setReviewCopied(true);
    } catch (caught) {
      setCollaborationError(
        caught instanceof Error ? caught.message : "The secure review link could not be copied.",
      );
    } finally {
      setReviewPending(false);
    }
  };

  const primaryAct = issue.primary_act || (inline ? "verify" : "build");
  const otherActs = issue.also_offered ?? [];
  const foregroundFirstRunVerification = firstRunFocus && otherActs.includes("verify");
  const presentedPrimaryAct = foregroundFirstRunVerification ? "verify" : primaryAct;
  const unassessed = issue.unassessed || issue.classification_state === "escalated";

  return (
    <aside
      aria-describedby={analysisRunning ? "issue-analysis-pending-status" : undefined}
      aria-label="Issue details"
      aria-modal={inline ? undefined : true}
      className={`project-sidepanel issue-panel ${inline ? "is-inline" : ""} severity-${issue.severity.toLowerCase()}`}
      id={`issue-detail-${issue.id}`}
      ref={panel}
      role={inline ? "region" : "dialog"}
      tabIndex={-1}
    >
      <div className="issue-panel-heading">
        <div>
          {inline ? (
            <span className={`r2-pillar r2-pillar-${issuePillar(issue).toLowerCase()}`}>
              {issuePillar(issue)}
            </span>
          ) : null}
          <span className={`severity severity-${issue.severity.toLowerCase()}`}>
            {issue.severity}
          </span>
          <h2>{issue.title}</h2>
        </div>
        {!inline ? (
          <button
            aria-label="Close issue"
            onClick={onClose}
            ref={closeButton}
            type="button"
          >
            <X aria-hidden="true" size={20} />
          </button>
        ) : null}
      </div>
      {inline ? (
        <div className="issue-inline-summary">
          <p>{issue.why}</p>
          <dl>
            <div><dt>Affects</dt><dd><span>{artifactLabel(issue.artifact_type)}</span><span>{artifactLabel(issue.dimension)}</span></dd></div>
            <div><dt>Holds up</dt><dd>{issue.why}</dd></div>
          </dl>
        </div>
      ) : null}
      <p className="issue-meta">
        Dimension · {issue.dimension} &nbsp; Section · {artifactLabel(issue.artifact_type)}
        &nbsp; Type · Finding
      </p>
      {issue.sensitivity_trace ? (
        <details className="issue-sensitivity-trace">
          <summary>Why this is load-bearing</summary>
          <dl>
            <div><dt>Counterfactual span</dt><dd>{issue.sensitivity_trace.span.toFixed(2)}</dd></div>
            <div><dt>Path leverage</dt><dd>{issue.sensitivity_trace.leverage.toFixed(2)}</dd></div>
            <div><dt>Uncertainty factor</dt><dd>{issue.sensitivity_trace.uncertainty_factor.toFixed(2)}</dd></div>
            <div><dt>Runway factor</dt><dd>{issue.sensitivity_trace.runway_factor.toFixed(2)}</dd></div>
            <div><dt>Outcome paths</dt><dd>{issue.sensitivity_trace.paths.length}</dd></div>
          </dl>
          <p>
            This trace compares favorable and adverse plan states. It explains ranking;
            it does not manufacture evidence or change Grounding.
          </p>
        </details>
      ) : null}
      <div className="issue-lifecycle" aria-label={`Issue status ${effectiveStatus}`}>
        {["open", "addressed", "routed", "needs_fix", "needs_grounding", "resolved"].map((status) => (
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
      {inline ? (
        <div className="issue-inline-guide">
          <strong>First time here · what {issuePillar(issue)} means</strong>
          <p>
            This is one of the load-bearing issues holding back the current read. Review
            what OSLO is basing it on, then decide the next move from your evidence.
          </p>
        </div>
      ) : null}
      {inline ? (
        <div className="issue-inline-footer">
          <button className="ask-oslo-issue" onClick={onAsk} type="button">
            <Sparkle aria-hidden="true" size={12} weight="fill" />
            Ask OSLO about this issue
          </button>
          <button
            className="issue-inline-discuss"
            onClick={() => setDiscussionVisible(true)}
            type="button"
          >
            <PencilSimple aria-hidden="true" size={12} />
            Discuss / @mention
          </button>
          <button
            aria-label="Close issue"
            className="issue-inline-close"
            onClick={onClose}
            ref={closeButton}
            type="button"
          >
            <CaretUp aria-hidden="true" size={11} />
            Close
          </button>
        </div>
      ) : (
        <button className="ask-oslo-issue" onClick={onAsk} type="button">
          <Sparkle aria-hidden="true" size={12} weight="fill" />
          Ask OSLO about this issue
        </button>
      )}

      <section className="issue-evidence issue-detail-disclosure">
        <button
          aria-controls="issue-evidence-content"
          aria-expanded={evidenceOpen}
          aria-label={`Evidence · ${evidence.length} ${
            evidence.length === 1 ? "source" : "sources"
          }, traceable to inputs`}
          className="issue-evidence-disclosure issue-detail-disclosure-trigger"
          onClick={() => setEvidenceOpen((current) => !current)}
          type="button"
        >
          <span aria-hidden="true" className="issue-detail-disclosure-icon">
            <FileText size={17} />
          </span>
          <span className="issue-detail-disclosure-copy">
            <strong>Evidence</strong>
            <small>What OSLO is basing this on.</small>
          </span>
          <CaretRight aria-hidden="true" size={13} />
        </button>
        {evidenceOpen ? (
          <div className="evidence-list issue-detail-disclosure-content" id="issue-evidence-content">
            <small className="issue-evidence-count">
              {evidence.length} {evidence.length === 1 ? "source" : "sources"}, traceable to inputs
            </small>
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
      <section className="issue-why-matters issue-detail-disclosure">
        <button
          aria-controls="issue-why-matters-content"
          aria-expanded={whyMattersOpen}
          aria-label="Why it matters"
          className="issue-detail-disclosure-trigger"
          onClick={() => setWhyMattersOpen((current) => !current)}
          type="button"
        >
          <span aria-hidden="true" className="issue-detail-disclosure-icon">
            <Target size={17} />
          </span>
          <span className="issue-detail-disclosure-copy">
            <strong>Why it matters</strong>
            <small>The impact to your goal and your plan if this isn’t addressed.</small>
          </span>
          <CaretRight aria-hidden="true" size={13} />
        </button>
        {whyMattersOpen ? (
          <div className="issue-detail-disclosure-content" id="issue-why-matters-content">
            <p>{issue.why}</p>
            <h3>What this weakens</h3>
            <p>
              This finding lowers the {issue.dimension.toLowerCase()} read for{" "}
              {artifactLabel(issue.artifact_type)} until the plan contains verified evidence.
            </p>
          </div>
        ) : null}
      </section>
      {issue.clarification && clarificationOpen ? (
        <form className="clarification-form" onSubmit={onSubmit}>
          <h3><span className="sr-only">Clarification request. </span>◆ Answer OSLO&apos;s question</h3>
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
            <p>
              Your answer updates the read and grounds this detail — recorded as your
              evidence, in your words.
            </p>
            <button
              disabled={!answer.trim() || pending || analysisRunning}
              type="submit"
            >
              {analysisRunning ? "Re-analyzing…" : pending ? "Saving…" : "Submit answer →"}
            </button>
          </div>
          <button
            className="clarification-cancel"
            onClick={() => setClarificationOpen(false)}
            type="button"
          >
            Cancel
          </button>
          {error ? <p className="clarification-error" role="alert">{error}</p> : null}
        </form>
      ) : null}
      <section className="issue-recommendation">
        <h3>{unassessed ? "Known unknown" : "OSLO recommended"}</h3>
        <strong>{issue.recommendation}</strong>
        <p>
          {unassessed
            ? "This region is incomplete, not weak. Clarify it so OSLO can assess it without inventing a score."
            : presentedPrimaryAct === "verify"
              ? "Verify or refute it with evidence. Only verification can move Grounding."
              : presentedPrimaryAct === "build"
                ? "Build the missing plan structure and re-run the governed analysis. Building never manufactures grounding."
                : "Record the tradeoff you are accepting. A decision adds clarity; it does not manufacture certainty."}
        </p>
        {unassessed ? (
          <div className="issue-action-row">
            <button onClick={onAsk} type="button">Help me clarify this</button>
          </div>
        ) : presentedPrimaryAct === "verify" ? (
          <div className="issue-action-row is-lifecycle">
            <button
              aria-label="Confirm — it holds"
              disabled={pending || analysisRunning}
              onClick={() => void onLifecycleAct("confirm", {
                basis: "verified-directly",
                evidenceRef: issue.evidence_refs.at(0) ?? `user:direct-confirm:${issue.id}`,
              })}
              type="button"
            >
              ✓ Confirm — it holds
            </button>
            <button
              disabled={pending || analysisRunning}
              onClick={() => void onLifecycleAct("flag", {
                basis: "verified-directly",
                evidenceRef: issue.evidence_refs.at(0) ?? `user:direct-flag:${issue.id}`,
              })}
              type="button"
            >
              It doesn&apos;t hold →
            </button>
            <button onClick={() => setRoutingOpen(true)} type="button">→ Ask for evidence →</button>
          </div>
        ) : presentedPrimaryAct === "build" ? (
          <div className="issue-action-row is-build">
            <button
              disabled={pending || analysisRunning}
              onClick={() => void onIssueAction("apply", issue.recommendation)}
              type="button"
            >
              Apply this fix →
            </button>
            <button onClick={() => setOtherWaysOpen((current) => !current)} type="button">
              Other options ({Math.max(2, otherActs.length)})
            </button>
            <button onClick={() => setCustomResolutionOpen(true)} type="button">
              Write my own →
            </button>
          </div>
        ) : (
          <div className="issue-action-row is-decision">
            <button
              disabled={pending || analysisRunning}
              onClick={() => void onIssueAction("select", issue.recommendation)}
              type="button"
            >
              Draw the line →
            </button>
            <button
              disabled={pending || analysisRunning}
              onClick={() => void onIssueAction(
                "select",
                `Accepted on the record: ${issue.recommendation}`,
              )}
              type="button"
            >
              Accept on the record →
            </button>
          </div>
        )}
        {!unassessed && otherActs.includes("verify") && presentedPrimaryAct !== "verify" ? (
          <button
            className="issue-clarification-disclosure"
            onClick={() => setRoutingOpen(true)}
            type="button"
          >
            Verify with evidence
          </button>
        ) : null}
        {issue.clarification ? (
          <button
            aria-expanded={clarificationOpen}
            aria-label="Let OSLO ask you a question"
            className="issue-clarification-disclosure"
            onClick={() => setClarificationOpen((current) => !current)}
            type="button"
          >
            Let OSLO ask you a question →
          </button>
        ) : null}
      </section>
      {routingOpen ? (
        <section className="issue-route-panel" aria-label="Ask for evidence">
          <h3>⇢ Ask for evidence — who can ground it?</h3>
          <p>
            <strong>Asking for evidence</strong> routes the question; their answer grounds
            the read, attributed to them. It stays OSLO&apos;s inference — not grounded —
            until they answer.
          </p>
          <button
            disabled={pending || analysisRunning || reviewPending}
            onClick={() => void routeIssue({
              id: "project-collaborator",
              display_name: "Project collaborator",
              role: "collaborator",
            })}
            type="button"
          >
            <span><b>Project collaborator</b> · collaborator <small>Sees your full read · co-grounds with you</small></span>
            <strong>Ask →</strong>
          </button>
          <button
            disabled={pending || analysisRunning || reviewPending}
            onClick={() => void routeIssue({
              id: "external-evidence-holder",
              display_name: "External evidence holder",
              role: "external",
            })}
            type="button"
          >
            <span><b>External evidence holder</b> · scoped <small>Gets only this question + its source · answers once</small></span>
            <strong>Ask →</strong>
          </button>
          <h3>Or just discuss it</h3>
          <p>
            A <strong>comment</strong> is discussion only. It never grounds the read or
            resolves the issue; the item stays open.
          </p>
          <button
            onClick={() => {
              setDiscussionVisible(true);
              setRoutingOpen(false);
            }}
            type="button"
          >
            <span><b>Comment / @mention</b> <small>Start a discussion — doesn&apos;t move the read</small></span>
            <strong>Comment →</strong>
          </button>
          <button className="issue-route-cancel" onClick={() => setRoutingOpen(false)} type="button">Cancel</button>
        </section>
      ) : null}
      <IssueProposalGroup
        onDecision={onProposalDecision}
        onToggle={() => setProposalsOpen((current) => !current)}
        open={proposalsOpen}
        pendingId={proposalPending}
        proposals={proposals}
        surface="issue_card"
      />
      <section className="issue-resolution-paths issue-detail-disclosure">
        {primaryAct !== "build" ? (
          <button
            aria-expanded={otherWaysOpen}
            aria-label="Other ways to handle this"
            className="issue-other-ways-disclosure issue-detail-disclosure-trigger"
            onClick={() => setOtherWaysOpen((current) => !current)}
            type="button"
          >
            <span aria-hidden="true" className="issue-detail-disclosure-icon">
              <ArrowsSplit size={17} />
            </span>
            <span className="issue-detail-disclosure-copy">
              <strong>Other ways to handle this</strong>
              <small>Alternative approaches and tradeoffs.</small>
            </span>
            <CaretRight aria-hidden="true" size={13} />
          </button>
        ) : null}
        {otherWaysOpen ? (
          <div className="issue-other-ways-content issue-detail-disclosure-content">
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
          </div>
        ) : null}
      </section>
      {selectedResolution ? (
        <section className="confirmed-resolution" aria-live="polite">
          <h3>Confirmed by you</h3>
          <p>{selectedResolution}</p>
        </section>
      ) : null}
      {customResolutionOpen ? (
        <section className="custom-resolution">
          <h3>Write my own fix in {artifactLabel(issue.artifact_type)}</h3>
          <textarea
            aria-label="Custom resolution"
            autoFocus
            disabled={pending || analysisRunning}
            maxLength={5_000}
            onChange={(event) => setCustomResolution(event.target.value)}
            placeholder="Describe the confirmed change to add to this artifact."
            value={customResolution}
          />
          <div>
            <button
              disabled={!customResolution.trim() || pending || analysisRunning}
              onClick={() => void onIssueAction("custom", customResolution)}
              type="button"
            >
              Apply custom fix →
            </button>
            <button onClick={() => setCustomResolutionOpen(false)} type="button">Cancel</button>
          </div>
        </section>
      ) : null}
      <section className={`issue-collaboration ${discussionVisible ? "is-visible" : ""}`}>
        <div className="issue-collaboration-heading">
          <div>
            <h3>Discussion · on {issue.title}</h3>
            <p>Anchored here · append-only</p>
          </div>
          <span>{comments.length}</span>
        </div>
        <div className="issue-comment-thread">
          {comments.map((comment) => (
            <article key={comment.id}>
              <span aria-hidden="true" className="issue-comment-avatar">
                {(comment.author_name || "You").slice(0, 1).toUpperCase()}
              </span>
              <header>
                <strong>{comment.author_name || "You"}</strong>
                <time dateTime={comment.created_at}>
                  {new Date(comment.created_at).toLocaleString()}
                </time>
              </header>
              <p>{comment.body}</p>
            </article>
          ))}
          {!comments.length ? <p className="issue-comment-empty">Start the discussion here.</p> : null}
        </div>
        <form className="issue-comment-form" onSubmit={submitComment}>
          <textarea
            aria-label="Add a comment"
            disabled={commentPending}
            maxLength={5_000}
            onChange={(event) => setCommentBody(event.target.value)}
            placeholder="Reply… @mention a teammate"
            value={commentBody}
          />
          <div className="issue-mention-shortcuts" aria-label="Mention shortcuts">
            <button onClick={() => setCommentBody((value) => `${value}@Priya `)} type="button">@Priya</button>
            <button onClick={() => setCommentBody((value) => `${value}@Dana `)} type="button">@Dana</button>
            <button onClick={() => setCommentBody((value) => `${value}@team `)} type="button">@team</button>
          </div>
          <p><strong>Comments never change the read</strong> — only grounding does.</p>
          <button disabled={commentPending || !commentBody.trim()} type="submit">
            {commentPending ? "Adding…" : "Comment"}
          </button>
        </form>
        {discussionVisible ? (
          <button className="issue-discussion-close" onClick={() => setDiscussionVisible(false)} type="button">
            Close discussion
          </button>
        ) : null}
      </section>
      {!inline || externalComposerOpen ? (
        <section
          className={`issue-review-share ${externalComposerOpen ? "is-routing" : ""}`}
          ref={reviewComposer}
        >
        <div className="issue-review-share-heading">
          <span className="issue-review-share-icon">
            <Sparkle aria-hidden="true" size={15} weight="fill" />
          </span>
          <div>
            <h3>Share for review</h3>
            <p>Invite a reviewer without using a workspace seat or invitation.</p>
          </div>
        </div>
        <div className="issue-review-scope-preview" aria-label="External reviewer scope preview">
          <span>They will see only</span>
          <strong>{scopedQuestion}</strong>
          {externalReviewReady ? (
            <>
              <p>{scopedSourceExcerpt}</p>
              <small>{scopedSourceRef}</small>
            </>
          ) : (
            <p>This issue does not yet contain a cited source excerpt.</p>
          )}
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
          <button
            disabled={reviewPending || !reviewerName.trim() || !externalReviewReady}
            type="submit"
          >
            <Sparkle aria-hidden="true" size={13} weight="fill" />
            {reviewPending ? "Creating…" : "Create secure review link"}
          </button>
        </form>
        {reviewLink ? (
          <div className="issue-review-link" role="status">
            <strong>
              {reviewDeliveryState === "awaiting"
                ? "Awaiting response"
                : reviewDeliveryState === "failed"
                  ? "Email delivery failed — copy the secure link"
                  : "Draft — copy the link to hand it off"}
            </strong>
            <code>{reviewLink}</code>
            <button
              disabled={reviewPending}
              onClick={() => void copyReviewLink()}
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
      ) : null}
      <p className={`issue-history-pointer ${inline ? "is-inline" : ""}`}>
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
  contextLabel,
  extendedFailed,
  extendedFailure,
  extendedRetryError,
  extendedRetrying,
  integrity,
  isProvisional,
  messages,
  onAsk,
  onClose,
  onQuestionChange,
  onRetry,
  onSubmit,
  onWideChange,
  openIssueCount,
  question,
  resolvedIssueCount,
  r2Mode,
  topIssue,
  tourTarget,
  wide,
}: {
  advisorError: string | null;
  advisorPending: boolean;
  advisorQuestions: string[];
  contextLabel: string | null;
  extendedFailed: boolean;
  extendedFailure: ReturnType<typeof analysisFailureCopy>;
  extendedRetryError: string | null;
  extendedRetrying: boolean;
  integrity: OverviewSnapshot["assessment"]["integrity"];
  isProvisional: boolean;
  messages: ChatMessage[];
  onAsk: (question: string) => Promise<void>;
  onClose: () => void;
  onQuestionChange: (question: string) => void;
  onRetry: () => Promise<void>;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onWideChange: (wide: boolean) => void;
  openIssueCount: number;
  question: string;
  resolvedIssueCount: number;
  r2Mode: boolean;
  topIssue: Issue | null;
  tourTarget?: RefObject<HTMLFormElement | null>;
  wide: boolean;
}) {
  return (
    <aside aria-label="OSLO project advisor" className={`project-sidepanel oslo-chat ${wide ? "is-wide" : ""}`}>
      <div className="chat-heading">
        <span aria-hidden="true">O</span>
        <div><strong>OSLO</strong><small>thinking with you — advisory, acts only when you say so</small></div>
        {r2Mode ? <em className="r2-advisor-governed">Governed</em> : null}
        {r2Mode ? (
          <button
            aria-label={wide ? "Narrow OSLO panel" : "Widen OSLO panel"}
            className="r2-advisor-width"
            onClick={() => onWideChange(!wide)}
            type="button"
          >
            ↔ {wide ? "Narrow" : "Wider"}
          </button>
        ) : null}
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
        {r2Mode ? <p className="r2-advisor-session">
          On {contextLabel ? <strong>{contextLabel}</strong> : "your read"} · <b>{resolvedIssueCount} of {resolvedIssueCount + openIssueCount}</b> settled
          {topIssue ? <> · next biggest exposure: <strong>{topIssue.title}</strong></> : null}
          <span> · toward your outcome →</span>
        </p> : null}
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
        {r2Mode ? <><section className="r2-advisor-reasoning">
          <p>Reasoning</p>
          <strong>Outcome Integrity is gated by {integrity.limiting_pillar}.</strong>
          <span>{integrity.decomposition.find((pillar) => pillar.key === integrity.limiting_pillar)?.why[0]}</span>
        </section>
        <section className="r2-advisor-basis">
          <p>Reliability basis</p>
          <span><b>{resolvedIssueCount}</b> load-bearing details grounded · <b>{openIssueCount}</b> still OSLO&apos;s inference. The read is only as strong as what it rests on.</span>
        </section>
        {topIssue ? (
          <section className="r2-advisor-next">
            <p>◆ Your next move</p>
            <strong>{topIssue.recommendation}</strong>
            <button onClick={() => void onAsk(`Explain the top issue: ${topIssue.title}`)} type="button">
              What settles it?
            </button>
          </section>
        ) : null}</> : null}
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
        <form
          className={tourTarget ? "chat-composer is-tour-target" : "chat-composer"}
          onSubmit={onSubmit}
          ref={tourTarget}
        >
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

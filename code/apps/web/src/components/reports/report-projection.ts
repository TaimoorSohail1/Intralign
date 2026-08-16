import type { OverviewSnapshot, ProjectHistory } from "@/lib/server/oslo-api";
import { currentReadSummary } from "@/lib/current-read-summary";

export { currentReadSummary } from "@/lib/current-read-summary";

export type ReportEvidenceState = "confirmed" | "inferred" | "conflicting";

export type ReportEvidenceItem = {
  id: string;
  artifactType: string;
  text: string;
  issueId: string | null;
  issueTitle: string | null;
  loadBearing: boolean;
  state: ReportEvidenceState;
};

export type ReportDecision = {
  id: string;
  title: string;
  detail: string | null;
  actor: string;
  occurredAt: string;
  issueId: string | null;
};

export type ProjectReportProjection = {
  projectId: string;
  projectTitle: string;
  analysisRunId: string;
  analysisAt: string;
  readSignature: string;
  summary: string;
  integrity: OverviewSnapshot["assessment"]["integrity"];
  openIssues: OverviewSnapshot["assessment"]["issues"];
  resolvedIssues: OverviewSnapshot["assessment"]["issues"];
  criticalGrounding: { grounded: number; total: number };
  evidenceRegister: { grounded: number; inferred: number; total: number };
  evidenceItems: ReportEvidenceItem[];
  decisions: ReportDecision[];
  nextMove: OverviewSnapshot["assessment"]["issues"][number] | null;
};

const severityOrder: Record<string, number> = {
  critical: 0,
  moderate: 1,
  warning: 2,
};

function issueOrder(
  left: OverviewSnapshot["assessment"]["issues"][number],
  right: OverviewSnapshot["assessment"]["issues"][number],
) {
  const leftRank = left.exposure_rank ?? Number.MAX_SAFE_INTEGER;
  const rightRank = right.exposure_rank ?? Number.MAX_SAFE_INTEGER;
  if (leftRank !== rightRank) return leftRank - rightRank;
  return (
    (severityOrder[left.severity.toLowerCase()] ?? 9) -
      (severityOrder[right.severity.toLowerCase()] ?? 9)
  );
}

function fallbackEvidenceItems(snapshot: OverviewSnapshot): ReportEvidenceItem[] {
  return snapshot.artifacts.flatMap((artifact) =>
    (artifact.assumptions ?? []).map((assumption) => ({
      id: assumption.id,
      artifactType: artifact.artifact_type,
      text: assumption.statement,
      issueId: null,
      issueTitle: null,
      loadBearing: assumption.load_bearing,
      state: assumption.state,
    })),
  );
}

function evidenceItems(snapshot: OverviewSnapshot): ReportEvidenceItem[] {
  if (!snapshot.provenance?.assumptions.length) return fallbackEvidenceItems(snapshot);
  return snapshot.provenance.assumptions.map((assumption) => ({
    id: assumption.id,
    artifactType: assumption.artifact_type,
    text: assumption.text,
    issueId: assumption.issue_id,
    issueTitle: assumption.issue_title,
    loadBearing: assumption.load_bearing,
    state: assumption.state,
  }));
}

function historyDecisions(history: ProjectHistory | undefined): ReportDecision[] {
  if (!history) return [];
  const seen = new Set<string>();
  const decisions: ReportDecision[] = [];
  for (const group of history.groups) {
    for (const event of group.events) {
      if (event.category !== "decisions") continue;
      const key = `${event.event_type}:${event.issue_id ?? "none"}:${event.summary}`;
      if (seen.has(key)) continue;
      seen.add(key);
      decisions.push({
        id: String(event.id),
        title: event.summary,
        detail: event.detail,
        actor: event.actor_type === "user" ? "You" : event.actor_type === "oslo" ? "OSLO" : "System",
        occurredAt: event.occurred_at,
        issueId: event.issue_id,
      });
    }
  }
  return decisions.sort((left, right) => right.occurredAt.localeCompare(left.occurredAt));
}

function resolvedIssueDecisions(
  snapshot: OverviewSnapshot,
  existing: ReportDecision[],
): ReportDecision[] {
  const coveredIssues = new Set(existing.map((decision) => decision.issueId).filter(Boolean));
  const additions = snapshot.assessment.issues
    .filter((issue) => issue.status === "resolved" && !coveredIssues.has(issue.id))
    .map((issue) => ({
      id: `issue:${issue.id}`,
      title: issue.selected_resolution || `Resolved ${issue.title}`,
      detail: issue.why,
      actor: issue.attested_by?.display_name || "You",
      occurredAt: snapshot.published_at,
      issueId: issue.id,
    }));
  return [...existing, ...additions];
}

export function projectReportProjection(
  snapshot: OverviewSnapshot,
  history?: ProjectHistory,
): ProjectReportProjection {
  const projectedEvidence = evidenceItems(snapshot);
  const loadBearing = projectedEvidence.filter((item) => item.loadBearing);
  const openIssues = snapshot.assessment.issues
    .filter((issue) => issue.status !== "resolved")
    .slice()
    .sort(issueOrder);
  const resolvedIssues = snapshot.assessment.issues.filter(
    (issue) => issue.status === "resolved",
  );
  const decisions = resolvedIssueDecisions(snapshot, historyDecisions(history));

  return {
    projectId: snapshot.project_id,
    projectTitle: snapshot.project_title || "Project understanding",
    analysisRunId: snapshot.analysis_run_id,
    analysisAt: snapshot.published_at,
    readSignature: `${snapshot.analysis_run_id}:${snapshot.snapshot_id}`,
    summary: currentReadSummary(
      snapshot.summary,
      openIssues.length,
      snapshot.project_title,
    ),
    integrity: snapshot.assessment.integrity,
    openIssues,
    resolvedIssues,
    criticalGrounding: {
      grounded: loadBearing.filter((item) => item.state === "confirmed").length,
      total: loadBearing.length,
    },
    evidenceRegister: {
      grounded: projectedEvidence.filter((item) => item.state === "confirmed").length,
      inferred: projectedEvidence.filter((item) => item.state !== "confirmed").length,
      total: projectedEvidence.length,
    },
    evidenceItems: projectedEvidence,
    decisions,
    nextMove: openIssues[0] ?? null,
  };
}

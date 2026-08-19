"use client";

import {
  ArrowCounterClockwise,
  ArrowRight,
  Buildings,
  CaretDown,
  CaretLeft,
  CaretRight,
  CaretUp,
  Check,
  CurrencyDollar,
  DotsSixVertical,
  Gear,
  Handshake,
  MagnifyingGlass,
  Minus,
  Plus,
  Sparkle,
  Target,
  Users,
} from "@phosphor-icons/react";
import Link from "next/link";
import {
  type FormEvent,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import type {
  ArtifactSection,
  ArtifactWorkspaceSummary,
  IssueProposalSummary,
  OverviewSnapshot,
} from "@/lib/server/oslo-api";

import { R2ArtifactContent, R2Narrative } from "./r2-artifact-content";

const artifactOrder = [
  "intent",
  "scope",
  "requirements",
  "constraints",
  "work_breakdown",
  "schedule",
  "resources",
] as const;

const understandingArtifacts = new Set([
  "intent",
  "scope",
  "requirements",
  "constraints",
]);

type Issue = OverviewSnapshot["assessment"]["issues"][number];
type ClaimProvenance = NonNullable<ArtifactSection["provenance"]>;
let editorIdSequence = 0;

function label(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function cloneContent(content: ArtifactWorkspaceSummary["content"]) {
  return structuredClone(content);
}

function nextEditorId(prefix: string) {
  editorIdSequence += 1;
  return `${prefix}-${editorIdSequence}`;
}

function isLegacyWorkBreakdownAuditText(value: string) {
  return /^(?:schedule|resources|intent|scope|requirements|constraints|work breakdown) artifact changes confirmed by the user:|^(?:section|issue|question|answer):/i.test(
    value.trim().replace(/^[-•]\s*/, ""),
  );
}

function sentenceCase(value: string) {
  const normalized = value.trim().replace(/[.;]+$/, "");
  return normalized ? normalized[0].toUpperCase() + normalized.slice(1) : normalized;
}

function legacyWorkBreakdownTree(value: string) {
  const normalized = value.trim().replace(/^[-•]\s*/, "").replace(/[.;]+$/, "");
  const separator = normalized.indexOf(":");
  if (separator < 1) return null;
  const packageName = normalized.slice(0, separator).trim();
  const detail = normalized.slice(separator + 1).trim();
  const fragments = detail
    .split(/\s*,\s*|\s+and\s+/i)
    .map((fragment) => fragment.trim())
    .filter(Boolean);
  if (fragments.length < 2) return null;

  const first = fragments[0].match(/^([a-z]+)\s+(.+)$/i);
  if (!first) return null;
  const verb = first[1].toLowerCase();
  const tasks = [first[2], ...fragments.slice(1)].map((fragment) =>
    sentenceCase(`${verb} ${fragment.replace(new RegExp(`^${verb}\\s+`, "i"), "")}`),
  );
  const deliverable = sentenceCase(
    packageName.replace(
      /^(?:plan|deliver|run|build|create|implement)\s+(?:an?\s+|the\s+)?/i,
      "",
    ),
  );
  if (!deliverable || !tasks.length) return null;
  return { deliverable, packageName: sentenceCase(packageName), tasks };
}

function normalizeLegacyWorkBreakdown(
  content: ArtifactWorkspaceSummary["content"],
) {
  if (content.sections.some((section) => section.rows.length)) return content;

  const sections = content.sections.flatMap((section, sectionIndex) => {
    const isLegacyFallback =
      /^(?:work breakdown|workstreams)$/i.test(section.heading.trim()) &&
      /evidence-qualified work breakdown/i.test(section.body);
    if (!isLegacyFallback) return [section];

    const trees = section.bullets
      .filter((bullet) => !isLegacyWorkBreakdownAuditText(bullet))
      .map(legacyWorkBreakdownTree)
      .filter((tree): tree is NonNullable<typeof tree> => tree !== null);
    if (!trees.length) return [section];

    return trees.map((tree, treeIndex) => {
      const rows = [
        ["1.0", tree.packageName],
        ...tree.tasks.map((task, taskIndex) => [`1.${taskIndex + 1}`, task]),
      ];
      return {
        ...section,
        id: section.id ?? `legacy-wbs-${sectionIndex + 1}-${treeIndex + 1}`,
        heading: tree.deliverable,
        body: "",
        bullets: [],
        columns: ["WBS", "Item"],
        rows,
        row_evidence_refs: rows.map(() => [...(section.evidence_refs ?? [])]),
        row_states: rows.map(() => "confirmed" as const),
        row_provenance: rows.map(() => "confirmed_by_user" as const),
        provenance: "confirmed_by_user" as const,
      };
    });
  });
  return { ...content, sections };
}

function ensureEditorIds(
  content: ArtifactWorkspaceSummary["content"],
  artifactType: string,
) {
  const normalized = cloneContent(
    artifactType === "work_breakdown"
      ? normalizeLegacyWorkBreakdown(content)
      : content,
  );
  normalized.sections = normalized.sections.map((section, sectionIndex) => {
    const sectionId =
      section.id ?? nextEditorId(`${artifactType}-section-${sectionIndex + 1}`);
    return {
      ...section,
      id: sectionId,
      row_ids: section.rows.map(
        (_, rowIndex) =>
          section.row_ids?.[rowIndex] ??
          nextEditorId(`${sectionId}-row-${rowIndex + 1}`),
      ),
    };
  });
  return normalized;
}

function sameContent(
  left: ArtifactWorkspaceSummary["content"],
  right: ArtifactWorkspaceSummary["content"],
) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function hasEmptySection(content: ArtifactWorkspaceSummary["content"]) {
  return content.sections.some(
    (section) =>
      !section.body.trim() &&
      !section.bullets.some((item) => item.trim()) &&
      !section.rows.some((row) => row.some((cell) => cell.trim())),
  );
}

function claimProvenanceLabel(
  provenance: ClaimProvenance | undefined,
  artifactProvenance: ArtifactWorkspaceSummary["provenance"],
) {
  if (provenance === "confirmed_by_user") return "Confirmed by you";
  if (provenance === "from_oslo" || artifactProvenance === "from_oslo") {
    return "From OSLO";
  }
  return "Contains your edits";
}

function evidenceStateLabel(state: NonNullable<ArtifactSection["row_states"]>[number]) {
  if (state === "confirmed") return "Grounded in project evidence";
  if (state === "inferred") return "Inferred by OSLO";
  if (state === "conflicting") return "Conflicting project evidence";
  return "Evidence origin unknown";
}

function rowProvenanceValues(
  section: ArtifactSection,
  artifactProvenance: ArtifactWorkspaceSummary["provenance"],
) {
  const legacyFallback: ClaimProvenance =
    artifactProvenance === "from_oslo" ? "from_oslo" : "confirmed_by_user";
  return section.rows.map(
    (_, index) => section.row_provenance?.[index] ?? legacyFallback,
  );
}

function artifactCategory(artifactType: string) {
  return understandingArtifacts.has(artifactType) ? "Understanding" : "Execution";
}

function artifactRead(
  artifact: ArtifactWorkspaceSummary,
  executionView: "outline" | "backlog",
) {
  if (artifact.artifact_type === "work_breakdown") {
    if (executionView === "backlog") {
      return "Your plan as a backlog — epics and stories. The same tasks, agile-framed.";
    }
    return "Decomposes the outcome into deliverables, work packages, and tasks — add, rename, confirm, or remove tasks here.";
  }
  const openIssues = artifact.issues.filter((issue) => issue.status !== "resolved");
  if (openIssues.length) {
    return `${openIssues.length} open ${openIssues.length === 1 ? "question remains" : "questions remain"} in this ${artifact.title.toLowerCase()} read.`;
  }
  return `${artifact.title} is clear in the current read.`;
}

function executionIntro(
  artifactType: string,
  executionView: "outline" | "backlog",
) {
  if (artifactType === "work_breakdown") {
    if (executionView === "backlog") {
      return "Your plan as a backlog — epics from deliverables, stories from work packages. Same tasks, agile-framed; schedule stories on Schedule.";
    }
    return "Deliverable → work package → task. Click any name to rename; add or remove at every level; confirm OSLO's inferences.";
  }
  if (artifactType === "schedule") {
    return "Set the dates the plan actually contains. Missing dates stay visibly unscheduled.";
  }
  return "People and non-human dependencies stay linked to the plan evidence that defines them.";
}

function checkpointStatement(proposal: IssueProposalSummary | undefined) {
  if (!proposal) return null;
  const proposedRead = proposal.title.replace(/^Add checkpoint:\s*read\s*/i, "").trim();
  if (!proposedRead || proposedRead === proposal.title.trim()) return null;
  return `Outcome checkpoint — read ${proposedRead}`;
}

function resourceValues(content: ArtifactWorkspaceSummary["content"]) {
  return content.sections.flatMap((section) => [
    section.heading,
    section.body,
    ...section.bullets,
    ...section.rows.flat(),
  ]).filter(Boolean);
}

function conciseResourceEvidence(value: string, maximum = 136) {
  const normalized = value.replace(/\s+/g, " ").trim();
  if (normalized.length <= maximum) return normalized;
  return `${normalized.slice(0, maximum - 1).trimEnd()}\u2026`;
}

function resourceSummaryDetail(
  content: ArtifactWorkspaceSummary["content"],
  key: string,
  hint: string,
) {
  if (key === "people") {
    const peopleSection = content.sections.find(
      (section) =>
        /resource plan|people|team|staff/i.test(section.heading) &&
        section.rows.length > 0,
    );
    if (peopleSection) {
      const count = peopleSection.rows.length;
      return `${count} resource ${count === 1 ? "entry" : "entries"} in ${peopleSection.heading}`;
    }
  }

  if (key === "vendors") {
    const vendorRows = content.sections
      .filter((section) =>
        /resource plan|vendor|supplier|partner|contractor/i.test(section.heading),
      )
      .flatMap((section) =>
        section.rows.filter((row) =>
          /vendor|supplier|partner|contractor/i.test(row.slice(0, 2).join(" ")),
        ),
      );
    if (vendorRows.length) {
      const labels = vendorRows
        .map((row) => [row[1], row[0]].filter(Boolean).join(" \u00b7 "))
        .slice(0, 2);
      return conciseResourceEvidence(labels.join("; "));
    }
  }

  const matcher = new RegExp(hint, "i");
  const rowEvidence = content.sections
    .flatMap((section) => section.rows.flat())
    .find((value) => matcher.test(value));
  if (rowEvidence) return conciseResourceEvidence(rowEvidence);

  const detail = resourceValues(content).find((value) => matcher.test(value));
  return detail ? conciseResourceEvidence(detail) : undefined;
}

function ResourceSummaryCards({
  content,
}: {
  content: ArtifactWorkspaceSummary["content"];
}) {
  const definitions = [
    { key: "people", label: "People", hint: "owner|people|team|staff" },
    { key: "budget", label: "Budget", hint: "budget|cost|fund|revenue" },
    { key: "facility", label: "Facility", hint: "venue|facility|room|site" },
    { key: "vendors", label: "Vendors", hint: "vendor|supplier|catering" },
    { key: "equipment", label: "Equipment", hint: "equipment|wi-fi|wifi|av|hardware" },
  ];
  return (
    <div aria-label="Resource summary" className="resource-summary-cards">
      {definitions.map((definition) => {
        const detail = resourceSummaryDetail(
          content,
          definition.key,
          definition.hint,
        );
        const Icon = definition.key === "people"
          ? Users
          : definition.key === "budget"
            ? CurrencyDollar
            : definition.key === "facility"
              ? Buildings
              : definition.key === "vendors"
                ? Handshake
                : Gear;
        return (
          <article key={definition.key}>
            <Icon aria-hidden="true" size={18} />
            <div>
              <strong>{definition.label}</strong>
              <small>{detail ?? "No explicit evidence in this artifact"}</small>
            </div>
            <span>{detail ? "linked" : "open"}</span>
          </article>
        );
      })}
    </div>
  );
}

function parsedDates(values: string[]) {
  return values
    .map((value) => Date.parse(value))
    .filter((value) => Number.isFinite(value));
}

function scheduleBarStyle(section: ArtifactSection, row: string[]) {
  const domain = parsedDates(section.rows.flat());
  const dates = parsedDates(row);
  if (!domain.length || !dates.length) return null;
  const minimum = Math.min(...domain);
  const maximum = Math.max(...domain);
  const span = Math.max(maximum - minimum, 24 * 60 * 60 * 1000);
  const start = Math.min(...dates);
  const end = Math.max(...dates);
  const left = ((start - minimum) / span) * 72;
  const width = Math.max(12, ((Math.max(end - start, span * 0.12)) / span) * 72);
  return {
    left: `${Math.min(76, left)}%`,
    width: `${Math.min(88 - left, width)}%`,
  };
}

function workBreakdownDepth(row: string[]) {
  const code = row.find((cell) => /^\d+(?:\.\d+)+$/.test(cell.trim()));
  if (!code) return 0;
  const parts = code.split(".");
  if (parts.length >= 3) return 2;
  return parts.at(-1) === "0" ? 0 : 1;
}

function StableEditableText({
  as,
  className,
  onValueChange,
  title,
  value,
}: {
  as: "li" | "p" | "td";
  className?: string;
  onValueChange: (value: string) => void;
  title?: string;
  value: string;
}) {
  const elementRef = useRef<HTMLElement | null>(null);

  useLayoutEffect(() => {
    const element = elementRef.current;
    if (
      element &&
      document.activeElement !== element &&
      element.textContent !== value
    ) {
      element.textContent = value;
    }
  }, [value]);

  const handleInput = (event: FormEvent<HTMLElement>) => {
    onValueChange(event.currentTarget.textContent ?? "");
  };
  const setElementRef = (element: HTMLElement | null) => {
    elementRef.current = element;
  };
  const sharedProps = {
    className,
    contentEditable: true,
    onInput: handleInput,
    suppressContentEditableWarning: true,
    title,
  };

  if (as === "p") {
    return <p {...sharedProps} ref={setElementRef} />;
  }
  if (as === "li") {
    return <li {...sharedProps} ref={setElementRef} />;
  }
  return <td {...sharedProps} ref={setElementRef} />;
}

export function ArtifactWorkspace({
  artifactType,
  projectId,
  onAnalysisStarted,
  onAskOslo,
  onOpenIssue,
  onProposalDecision,
  proposalError,
  proposalPending,
  proposals = [],
  analysisRunning,
  initialFocus,
  returnToOutcome = false,
}: {
  artifactType: string;
  projectId: string;
  onAnalysisStarted: (runId: string) => void;
  onAskOslo: (question: string) => void;
  onOpenIssue: (issue: Issue, target: HTMLElement) => void;
  onProposalDecision?: (proposal: IssueProposalSummary, accepted: boolean) => void;
  proposalError?: string | null;
  proposalPending?: string | null;
  proposals?: IssueProposalSummary[];
  analysisRunning: boolean;
  initialFocus?: "primary-outcome" | "held-outcomes" | "new-outcome";
  returnToOutcome?: boolean;
}) {
  const [artifact, setArtifact] = useState<ArtifactWorkspaceSummary | null>(null);
  const [content, setContent] = useState<ArtifactWorkspaceSummary["content"] | null>(null);
  const [status, setStatus] = useState<
    "loading" | "saved" | "editing" | "saving" | "stale" | "reanalyzing" | "error"
  >("loading");
  const [error, setError] = useState<string | null>(null);
  const [loadRevision, setLoadRevision] = useState(0);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [issueIndex, setIssueIndex] = useState(0);
  const [viewMode, setViewMode] = useState<"statements" | "narrative">("statements");
  const [executionView, setExecutionView] = useState<"outline" | "backlog">("outline");
  const [historyDepth, setHistoryDepth] = useState(0);
  const [futureDepth, setFutureDepth] = useState(0);
  const historyRef = useRef<ArtifactWorkspaceSummary["content"][]>([]);
  const futureRef = useRef<ArtifactWorkspaceSummary["content"][]>([]);
  const reanalysisStartedRef = useRef(false);
  const outcomeFocusAppliedRef = useRef(false);
  const newOutcomeSeededRef = useRef(false);

  useEffect(() => {
    let cancelled = false;
    void fetch(`/api/projects/${projectId}/artifacts/${artifactType}`, {
      cache: "no-store",
    })
      .then(async (response) => {
        if (!response.ok) throw new Error("Artifact could not be loaded");
        return response.json() as Promise<ArtifactWorkspaceSummary>;
      })
      .then((loaded) => {
        if (cancelled) return;
        const normalizedContent = ensureEditorIds(loaded.content, artifactType);
        setArtifact({ ...loaded, content: normalizedContent });
        const nextContent = cloneContent(normalizedContent);
        if (
          artifactType === "intent" &&
          initialFocus === "new-outcome" &&
          !newOutcomeSeededRef.current
        ) {
          newOutcomeSeededRef.current = true;
          let outcomes = nextContent.sections.find((section) => /^outcomes?$/i.test(section.heading.trim()));
          if (!outcomes) {
            outcomes = {
              id: nextEditorId("intent-outcomes"),
              heading: "Outcomes",
              body: "",
              bullets: [],
              columns: [],
              rows: [],
              provenance: "confirmed_by_user",
            };
            nextContent.sections.push(outcomes);
          }
          outcomes.bullets.push("New outcome");
          outcomes.provenance = "confirmed_by_user";
          historyRef.current = [cloneContent(normalizedContent)];
          setHistoryDepth(1);
          setStatus("editing");
        } else {
          historyRef.current = [];
          setHistoryDepth(0);
          setStatus("saved");
        }
        setContent(nextContent);
        futureRef.current = [];
        setFutureDepth(0);
        setIssueIndex(0);
      })
      .catch((loadError) => {
        if (cancelled) return;
        setError(loadError instanceof Error ? loadError.message : "Artifact could not be loaded");
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [artifactType, initialFocus, loadRevision, projectId]);

  useEffect(() => {
    if (analysisRunning) {
      reanalysisStartedRef.current = true;
      return;
    }
    if (!reanalysisStartedRef.current) return;
    reanalysisStartedRef.current = false;
    void fetch(`/api/projects/${projectId}/artifacts/${artifactType}`, {
      cache: "no-store",
    })
      .then(async (response) => {
        if (!response.ok) throw new Error("Artifact refresh failed");
        return response.json() as Promise<ArtifactWorkspaceSummary>;
      })
      .then((loaded) => {
        const normalizedContent = ensureEditorIds(loaded.content, artifactType);
        setArtifact({ ...loaded, content: normalizedContent });
        setContent(cloneContent(normalizedContent));
        setStatus("saved");
      })
      .catch(() => setStatus("saved"));
  }, [analysisRunning, artifactType, projectId]);

  const issues = artifact?.issues.filter((issue) => issue.status !== "resolved") ?? [];
  const currentIndex = artifactOrder.indexOf(artifactType as (typeof artifactOrder)[number]);
  const previous = currentIndex > 0 ? artifactOrder[currentIndex - 1] : null;
  const next =
    currentIndex >= 0 && currentIndex < artifactOrder.length - 1
      ? artifactOrder[currentIndex + 1]
      : null;
  const displayStatus = analysisRunning ? "reanalyzing" : status;
  const isUnderstanding = understandingArtifacts.has(artifactType);
  const proposedCheckpoint = artifactType === "schedule"
    ? proposals.find((proposal) => /^Add checkpoint:\s*read\s+/i.test(proposal.title))
    : undefined;
  const proposedCheckpointStatement = checkpointStatement(proposedCheckpoint);
  const hasConfirmedScheduleCheckpoint = artifactType === "schedule" && Boolean(
    content?.sections.some((section) => section.rows.some(
      (row) => /^Outcome checkpoint\s*[—-]\s*read\s+/i.test(row[0] ?? ""),
    )),
  );

  const matches = useMemo(() => {
    if (!content || !searchQuery.trim()) return 0;
    const needle = searchQuery.trim().toLowerCase();
    return JSON.stringify(content).toLowerCase().split(needle).length - 1;
  }, [content, searchQuery]);

  function stageContent(nextContent: ArtifactWorkspaceSummary["content"]) {
    if (!artifact) return;
    setError(null);
    if (sameContent(nextContent, artifact.content)) {
      setStatus("saved");
      return;
    }
    setStatus("editing");
  }

  async function applyChanges() {
    if (!artifact || !content) return;
    if (sameContent(content, artifact.content)) {
      setStatus("saved");
      return;
    }
    if (hasEmptySection(content)) {
      setError("Complete or remove empty sections before saving changes");
      setStatus("editing");
      return;
    }

    setStatus("saving");
    setError(null);
    try {
      const response = await fetch(
        `/api/projects/${projectId}/artifacts/${artifactType}`,
        {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            content,
            expectedVersion: artifact.version,
            idempotencyKey: `artifact-${artifactType}-${crypto.randomUUID()}`,
          }),
        },
      );
      const payload = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(payload?.message ?? "Artifact save failed");
      }
      const saved = payload as ArtifactWorkspaceSummary;
      const normalizedContent = ensureEditorIds(saved.content, artifactType);
      setArtifact({ ...saved, content: normalizedContent });
      setContent(cloneContent(normalizedContent));
      historyRef.current = [];
      futureRef.current = [];
      setHistoryDepth(0);
      setFutureDepth(0);
      if (saved.analysis_run?.run_id) {
        setStatus("stale");
        onAnalysisStarted(saved.analysis_run.run_id);
      } else {
        setStatus("saved");
      }
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Artifact save failed");
      setStatus("error");
    }
  }

  function updateContent(mutator: (draft: ArtifactWorkspaceSummary["content"]) => void) {
    if (!content) return;
    historyRef.current.push(cloneContent(content));
    futureRef.current = [];
    setHistoryDepth(historyRef.current.length);
    setFutureDepth(0);
    const nextContent = cloneContent(content);
    mutator(nextContent);
    setContent(nextContent);
    stageContent(nextContent);
  }

  function cancelChanges() {
    if (!artifact) return;
    setContent(cloneContent(artifact.content));
    historyRef.current = [];
    futureRef.current = [];
    setHistoryDepth(0);
    setFutureDepth(0);
    setError(null);
    setStatus("saved");
  }

  useEffect(() => {
    if (
      artifactType !== "intent" ||
      !initialFocus ||
      outcomeFocusAppliedRef.current ||
      (status !== "saved" && status !== "editing") ||
      !content
    ) return;
    outcomeFocusAppliedRef.current = true;

    window.requestAnimationFrame(() => {
      const group = document.querySelector<HTMLElement>(
        '.r2-artifact-group[data-group-key="outcomes"]',
      );
      group?.scrollIntoView({ block: "center", behavior: "smooth" });
      if (initialFocus === "new-outcome") {
        const editor = group?.querySelector<HTMLElement>(
          ".r2-statement-row:last-of-type [contenteditable]",
        );
        editor?.focus();
        if (editor) document.getSelection()?.selectAllChildren(editor);
      }
    });
  }, [artifactType, content, initialFocus, status]);

  function undo() {
    if (!content) return;
    const previousContent = historyRef.current.pop();
    if (!previousContent) return;
    futureRef.current.push(cloneContent(content));
    setHistoryDepth(historyRef.current.length);
    setFutureDepth(futureRef.current.length);
    setContent(previousContent);
    stageContent(previousContent);
  }

  function redo() {
    if (!content) return;
    const nextContent = futureRef.current.pop();
    if (!nextContent) return;
    historyRef.current.push(cloneContent(content));
    setHistoryDepth(historyRef.current.length);
    setFutureDepth(futureRef.current.length);
    setContent(nextContent);
    stageContent(nextContent);
  }

  if (status === "error" && (!artifact || !content)) {
    return (
      <section className="artifact-workspace artifact-loading is-error" role="alert">
        <p>{error ?? `${label(artifactType)} could not be loaded.`}</p>
        <button
          className="button"
          onClick={() => {
            setError(null);
            setStatus("loading");
            setLoadRevision((current) => current + 1);
          }}
          type="button"
        >
          Try again
        </button>
      </section>
    );
  }

  if (status === "loading" || !artifact || !content) {
    return (
      <section className="artifact-workspace artifact-loading" aria-busy="true">
        <span />
        <p>Loading {label(artifactType)}…</p>
      </section>
    );
  }

  const activeIssue = issues[issueIndex] ?? null;
  const issueSectionIndex = activeIssue
    ? Math.max(
        0,
        content.sections.findIndex((section) => {
          const sectionEvidence = new Set([
            ...(section.evidence_refs ?? []),
            ...(section.row_evidence_refs ?? []).flat(),
          ]);
          return activeIssue.evidence_refs.some((reference) =>
            sectionEvidence.has(reference),
          );
        }),
      )
    : -1;

  return (
    <section className="artifact-workspace">
      {returnToOutcome ? (
        <aside aria-label="Your Outcome handoff" className="outcome-intent-handoff">
          <div>
            <Target aria-hidden="true" size={15} weight="fill" />
            <span>
              <strong>{initialFocus === "new-outcome" ? "Declare an outcome" : initialFocus === "held-outcomes" ? "Review outcomes OSLO detected" : "Manage your primary outcome"}</strong>
              <small>Intent is the editable source. Your Outcome remains a read-only view.</small>
            </span>
          </div>
          <Link href={`/projects/${projectId}/outcome`}>Back to Your Outcome →</Link>
        </aside>
      ) : null}
      <header className="artifact-editor-header">
        <div className="artifact-title-row">
          <span className="artifact-category-chip">{artifactCategory(artifactType)}</span>
          <h1>{artifact.title}</h1>
          <span className={`artifact-read-state ${issues.length ? "is-weak" : "is-clear"}`}>
            {issues.length ? "weak" : "clear"}
          </span>
          {isUnderstanding ? (
            <div aria-label="Artifact view" className="artifact-view-toggle" role="group">
              <button
                aria-pressed={viewMode === "statements"}
                onClick={() => setViewMode("statements")}
                type="button"
              >
                Statements
              </button>
              <button
                aria-pressed={viewMode === "narrative"}
                onClick={() => setViewMode("narrative")}
                type="button"
              >
                Narrative
              </button>
            </div>
          ) : artifactType === "work_breakdown" ? (
            <div aria-label="Work breakdown framing" className="artifact-view-toggle" role="group">
              <button
                aria-pressed={executionView === "outline"}
                onClick={() => setExecutionView("outline")}
                type="button"
              >
                Outline · WBS
              </button>
              <button
                aria-pressed={executionView === "backlog"}
                onClick={() => setExecutionView("backlog")}
                type="button"
              >
                Backlog · agile
              </button>
            </div>
          ) : null}
        </div>
        <p className="artifact-oslo-read">
          <strong>OSLO&apos;s read:</strong> {artifactRead(artifact, executionView)}
        </p>
        <div className="artifact-content-heading">
          <strong>Contents · you author, OSLO reads</strong>
          <span>
            <i className="is-yours" /> yours
            <i className="is-inferred" /> OSLO-inferred
          </span>
        </div>
        <div className="artifact-editor-toolbar">
          <div className="artifact-pager">
            {previous ? (
              <Link
                aria-label={`Open ${label(previous)}`}
                href={`/projects/${projectId}/artifacts/${previous}`}
              >
                <CaretLeft size={14} />
              </Link>
            ) : (
              <button aria-label="No previous artifact" disabled type="button">
                <CaretLeft size={14} />
              </button>
            )}
            {next ? (
              <Link
                aria-label={`Open ${label(next)}`}
                href={`/projects/${projectId}/artifacts/${next}`}
              >
                <CaretRight size={14} />
              </Link>
            ) : (
              <button aria-label="No next artifact" disabled type="button">
                <CaretRight size={14} />
              </button>
            )}
          </div>
          <span>v{artifact.version}</span>
          {issues.length ? (
            <div className="weakness-stepper">
              <span>Jump to weakness</span>
              <button
                aria-label="Previous issue"
                onClick={() => {
                  setIssueIndex((current) => (current - 1 + issues.length) % issues.length);
                  document
                    .querySelector(".artifact-inline-issue")
                    ?.scrollIntoView({ block: "center", behavior: "smooth" });
                }}
                type="button"
              >
                <CaretUp size={12} />
              </button>
              <strong>
                {issueIndex + 1} of {issues.length}
              </strong>
              <button
                aria-label="Next issue"
                onClick={() => {
                  setIssueIndex((current) => (current + 1) % issues.length);
                  document
                    .querySelector(".artifact-inline-issue")
                    ?.scrollIntoView({ block: "center", behavior: "smooth" });
                }}
                type="button"
              >
                <CaretDown size={12} />
              </button>
            </div>
          ) : (
            <span className="artifact-clear">
              <Check size={13} /> No issues in view
            </span>
          )}
          <div className="artifact-tools">
            <button aria-label="Undo" disabled={!historyDepth} onClick={undo} type="button">
              <ArrowCounterClockwise size={14} />
            </button>
            <button aria-label="Redo" disabled={!futureDepth} onClick={redo} type="button">
              <ArrowCounterClockwise mirrored size={14} />
            </button>
            <button
              aria-label="Add section"
              onClick={() =>
                updateContent((draft) =>
                  draft.sections.push({
                    id: nextEditorId(`${artifactType}-section`),
                    heading: "New section",
                    body: "",
                    bullets: [],
                    columns: [],
                    rows: [],
                    row_ids: [],
                    provenance: "confirmed_by_user",
                  }),
                )
              }
              type="button"
            >
              <Plus size={14} />
            </button>
            <button
              aria-expanded={searchOpen}
              aria-label="Find in artifact"
              onClick={() => setSearchOpen((current) => !current)}
              type="button"
            >
              <MagnifyingGlass size={14} />
            </button>
            <button
              aria-label="Ask OSLO about this artifact"
              onClick={() => onAskOslo(`Explain the current ${artifact.title} artifact.`)}
              type="button"
            >
              <Sparkle size={14} />
            </button>
          </div>
          <span className={`artifact-save-state is-${displayStatus}`}>
            {displayStatus === "editing"
              ? "Changes not applied"
              : displayStatus === "saving"
                ? "Saving…"
                : displayStatus === "stale"
                  ? "Saved · analysis stale"
                  : displayStatus === "reanalyzing"
                    ? "Reanalyzing…"
                : displayStatus === "error"
                  ? "Save failed"
                  : "Up to date"}
          </span>
          {displayStatus === "editing" || displayStatus === "error" ? (
            <div className="artifact-change-actions">
              <button
                className="artifact-cancel-button"
                onClick={cancelChanges}
                type="button"
              >
                Cancel changes
              </button>
              <button
                className="artifact-apply-button"
                disabled={hasEmptySection(content)}
                onClick={() => void applyChanges()}
                type="button"
              >
                Save changes
              </button>
            </div>
          ) : null}
        </div>
        {displayStatus === "editing" ||
        displayStatus === "saving" ||
        displayStatus === "stale" ? (
          <p className={`artifact-state-hint is-${displayStatus}`}>
            {displayStatus === "editing"
              ? "Changes stay local until you save them. Undoing back to the current version starts no analysis."
              : displayStatus === "saving"
                ? "Saving one governed artifact revision and preparing one re-analysis."
                : "Your change is saved as project evidence. The current read remains available while OSLO re-analyzes it."}
          </p>
        ) : null}
        {searchOpen ? (
          <label className="artifact-find">
            <MagnifyingGlass size={14} />
            <input
              autoFocus
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder="Find in this artifact…"
              value={searchQuery}
            />
            <span>{searchQuery ? `${matches} found` : ""}</span>
          </label>
        ) : null}
        {error ? (
          <button
            className="artifact-save-error"
            onClick={() => void applyChanges()}
            type="button"
          >
            {error}. Retry save
          </button>
        ) : null}
      </header>

      {!isUnderstanding ? (
        <p className="artifact-execution-intro">
          {executionIntro(artifactType, executionView)}
        </p>
      ) : null}
      {artifactType === "resources" ? (
        <ResourceSummaryCards content={content} />
      ) : null}

      {isUnderstanding && viewMode === "narrative" ? (
        <R2Narrative
          artifactProvenance={artifact.provenance}
          artifactType={artifactType}
          content={content}
        />
      ) : (
        <div
          className={`artifact-editor-body r2-artifact-editor-body is-${artifactType} is-${executionView} ${
            artifact.provenance !== "from_oslo" ? "is-confirmed" : ""
          }`}
        >
          <R2ArtifactContent
            activeIssue={activeIssue}
            artifactProvenance={artifact.provenance}
            artifactType={artifactType}
            content={content}
            executionView={executionView}
            issueSectionIndex={issueSectionIndex}
            onChangeContent={updateContent}
            onOpenIssue={onOpenIssue}
          />
        </div>
      )}
      {!isUnderstanding && artifactType !== "resources" && (
        artifactType !== "schedule" ||
        (proposedCheckpointStatement && !hasConfirmedScheduleCheckpoint)
      ) ? (
        <div className="artifact-execution-actions">
          <button
            onClick={() =>
              updateContent((draft) => {
                if (artifactType === "work_breakdown") {
                  const id = nextEditorId("work-breakdown-section");
                  draft.sections.push({
                    id,
                    heading: "New deliverable",
                    body: "",
                    bullets: [],
                    columns: ["WBS", "Item"],
                    rows: [["1.0", "New work package"]],
                    row_ids: [nextEditorId(`${id}-row`)],
                    row_evidence_refs: [[]],
                    row_states: ["confirmed"],
                    row_provenance: ["confirmed_by_user"],
                    provenance: "confirmed_by_user",
                  });
                  return;
                }
                const section = draft.sections[0];
                if (!section) return;
                const existingRowProvenance = rowProvenanceValues(
                  section,
                  artifact.provenance,
                );
                const row = section.columns.map(() => "");
                row[0] = artifactType === "schedule"
                  ? proposedCheckpointStatement ?? ""
                  : artifactType === "resources"
                    ? "New teammate"
                    : "New deliverable";
                if (artifactType === "resources" && row.length > 2) row[2] = "Unassigned";
                const placeholderIndex = artifactType === "schedule"
                  ? section.rows.findIndex(
                      (candidate) => candidate[0]?.trim() === "New outcome checkpoint",
                    )
                  : -1;
                if (placeholderIndex >= 0) {
                  section.rows[placeholderIndex] = row;
                  const rowProvenance = [...existingRowProvenance];
                  rowProvenance[placeholderIndex] = "confirmed_by_user";
                  section.row_provenance = rowProvenance;
                  section.row_states = section.rows.map((_, index) =>
                    index === placeholderIndex
                      ? "confirmed"
                      : section.row_states?.[index] ?? "unknown",
                  );
                  section.provenance = "confirmed_by_user";
                  return;
                }
                section.rows.push(row);
                section.row_ids = [
                  ...(section.row_ids ?? []),
                  nextEditorId(`${section.id ?? artifactType}-row`),
                ];
                section.row_evidence_refs = [...(section.row_evidence_refs ?? []), []];
                section.row_states = [...(section.row_states ?? []), "confirmed"];
                section.row_provenance = [
                  ...existingRowProvenance,
                  "confirmed_by_user",
                ];
                section.provenance = "confirmed_by_user";
              })
            }
            type="button"
          >
            <Plus size={13} />
            {artifactType === "schedule"
              ? "Add outcome checkpoint"
              : artifactType === "resources"
                ? "Add teammate"
                : "Add deliverable"}
          </button>
        </div>
      ) : null}
      {proposals.length && onProposalDecision ? (
        <section aria-label="OSLO proposes in this artifact" className="artifact-proposals">
          <header>
            <span aria-hidden="true">◆</span>
            <div>
              <strong>OSLO proposes — nothing enters your plan until you accept</strong>
              <small>{proposals.length} item{proposals.length === 1 ? "" : "s"} for this document · you decide</small>
            </div>
          </header>
          {proposalError ? <p role="alert">{proposalError}</p> : null}
          {proposals.map((proposal) => (
            <article key={proposal.id}>
              <span aria-hidden="true">◆</span>
              <div>
                <strong>{proposal.title}</strong>
                <small><b>Why:</b> {proposal.rationale}</small>
              </div>
              <div>
                <button
                  aria-label={`Add ${proposal.title} to plan in ${label(artifactType)}`}
                  disabled={proposalPending === proposal.id}
                  onClick={() => onProposalDecision(proposal, true)}
                  type="button"
                >{proposalPending === proposal.id ? "Saving…" : "Add to plan"}</button>
                <button
                  aria-label={`Dismiss ${proposal.title} in ${label(artifactType)}`}
                  disabled={proposalPending === proposal.id}
                  onClick={() => onProposalDecision(proposal, false)}
                  type="button"
                >Dismiss</button>
              </div>
            </article>
          ))}
        </section>
      ) : null}
      <nav aria-label="Artifact sequence" className="artifact-sequence-nav">
        {previous ? (
          <Link href={`/projects/${projectId}/artifacts/${previous}`}>
            <CaretLeft size={14} /> {label(previous)}
          </Link>
        ) : <span />}
        {next ? (
          <Link href={`/projects/${projectId}/artifacts/${next}`}>
            {label(next)} <CaretRight size={14} />
          </Link>
        ) : <span />}
      </nav>
    </section>
  );
}

export function ArtifactSectionEditor({
  activeIssue,
  artifactProvenance,
  artifactType,
  onChange,
  onOpenIssue,
  section,
}: {
  activeIssue: Issue | null;
  artifactProvenance: ArtifactWorkspaceSummary["provenance"];
  artifactType: string;
  onChange: (section: ArtifactSection) => void;
  onOpenIssue: (issue: Issue, target: HTMLElement) => void;
  section: ArtifactSection;
}) {
  const issueHere = activeIssue?.artifact_type === artifactType ? activeIssue : null;
  const hasStructuredUnderstandingRows =
    understandingArtifacts.has(artifactType) && section.rows.length > 0;

  return (
    <section className="artifact-section">
      <button
        aria-label="Reorder block"
        className="artifact-block-grip"
        title="Reorder block"
        type="button"
      >
        <DotsSixVertical size={14} />
      </button>
      <span
        aria-label={`Provenance: ${claimProvenanceLabel(
          section.provenance,
          artifactProvenance,
        )}`}
        className="artifact-block-provenance"
      >
        {claimProvenanceLabel(section.provenance, artifactProvenance)}
      </span>
      {section.heading ? <h2>{section.heading}</h2> : null}
      {!hasStructuredUnderstandingRows &&
      (section.body || (!section.bullets.length && !section.rows.length)) ? (
        <StableEditableText
          as="p"
          className={
            issueHere
              ? `artifact-copy has-${issueHere.severity.toLowerCase()}-issue`
              : "artifact-copy"
          }
          onValueChange={(value) =>
            onChange({
              ...section,
              body: value,
              provenance: "confirmed_by_user",
            })
          }
          value={section.body}
        />
      ) : null}
      {!hasStructuredUnderstandingRows && section.bullets.length ? (
        <ul className="artifact-bullets">
          {section.bullets.map((bullet, bulletIndex) => (
            <StableEditableText
              as="li"
              key={`${section.id ?? artifactType}-bullet-${bulletIndex}`}
              onValueChange={(value) => {
                const bullets = [...section.bullets];
                bullets[bulletIndex] = value;
                onChange({
                  ...section,
                  bullets,
                  provenance: "confirmed_by_user",
                });
              }}
              value={bullet}
            />
          ))}
        </ul>
      ) : null}
      {section.columns.length ? (
        <div className="artifact-table-wrap">
          <table>
            <thead>
              <tr>
                <th className="artifact-row-gutter">
                  <button
                    aria-label="Insert a row at the top of this table"
                    onClick={() =>
                      onChange({
                        ...section,
                        rows: [section.columns.map(() => ""), ...section.rows],
                        row_ids: [
                          nextEditorId(`${section.id ?? artifactType}-row`),
                          ...(section.row_ids ?? []),
                        ],
                        provenance: "confirmed_by_user",
                        row_evidence_refs: [[], ...(section.row_evidence_refs ?? [])],
                        row_states: ["confirmed", ...(section.row_states ?? [])],
                        row_provenance: [
                          "confirmed_by_user",
                          ...rowProvenanceValues(section, artifactProvenance),
                        ],
                      })
                    }
                    title="Insert row at top"
                    type="button"
                  >
                    <Plus size={11} />
                  </button>
                </th>
                {section.columns.map((column, columnIndex) => (
                  <th key={`${column}-${columnIndex}`}>
                    <span>{column}</span>
                    <span className="artifact-column-controls">
                      <button
                        aria-label={`Add a column after ${column}`}
                        onClick={() => {
                          const columns = [...section.columns];
                          columns.splice(columnIndex + 1, 0, "New column");
                          const rows = section.rows.map((row) => {
                            const nextRow = [...row];
                            nextRow.splice(columnIndex + 1, 0, "");
                            return nextRow;
                          });
                          onChange({
                            ...section,
                            columns,
                            rows,
                            provenance: "confirmed_by_user",
                            row_provenance: rows.map(() => "confirmed_by_user"),
                          });
                        }}
                        type="button"
                      >
                        <Plus size={10} />
                      </button>
                      <button
                        aria-label={`Delete ${column} column`}
                        disabled={section.columns.length === 1}
                        onClick={() => {
                          const columns = section.columns.filter(
                            (_, index) => index !== columnIndex,
                          );
                          const rows = section.rows.map((row) =>
                            row.filter((_, index) => index !== columnIndex),
                          );
                          onChange({
                            ...section,
                            columns,
                            rows,
                            provenance: "confirmed_by_user",
                            row_provenance: rows.map(() => "confirmed_by_user"),
                          });
                        }}
                        type="button"
                      >
                        <Minus size={10} />
                      </button>
                    </span>
                  </th>
                ))}
                {artifactType === "schedule" ? (
                  <th className="artifact-timeline-heading">Timeline</th>
                ) : null}
              </tr>
            </thead>
            <tbody>
              {section.rows.map((row, rowIndex) => (
                <tr
                  className={
                    artifactType === "work_breakdown"
                      ? `is-wbs-depth-${workBreakdownDepth(row)}`
                      : undefined
                  }
                  key={
                    section.row_ids?.[rowIndex] ??
                    `${section.id ?? artifactType}-row-${rowIndex}`
                  }
                >
                  <td className="artifact-row-gutter">
                    <span
                      aria-label={`${evidenceStateLabel(
                        section.row_states?.[rowIndex] ?? "unknown",
                      )}; ${
                        section.row_evidence_refs?.[rowIndex]?.length ?? 0
                      } evidence reference(s)`}
                      className={`artifact-row-provenance is-${
                        section.row_states?.[rowIndex] ?? "unknown"
                      }`}
                      title={`${evidenceStateLabel(
                        section.row_states?.[rowIndex] ?? "unknown",
                      )} · ${
                        section.row_evidence_refs?.[rowIndex]?.length ?? 0
                      } evidence reference(s)`}
                    />
                    <span
                      aria-label={`Provenance: ${claimProvenanceLabel(
                        section.row_provenance?.[rowIndex],
                        artifactProvenance,
                      )}`}
                      className="artifact-row-origin"
                    >
                      {claimProvenanceLabel(
                        section.row_provenance?.[rowIndex],
                        artifactProvenance,
                      )}
                    </span>
                    <button
                      aria-label="Reorder row — use Up and Down arrow keys to move"
                      className="artifact-row-grip"
                      onKeyDown={(event) => {
                        if (event.key !== "ArrowUp" && event.key !== "ArrowDown") return;
                        event.preventDefault();
                        const targetIndex =
                          event.key === "ArrowUp" ? rowIndex - 1 : rowIndex + 1;
                        if (targetIndex < 0 || targetIndex >= section.rows.length) return;
                        const rows = section.rows.map((item) => [...item]);
                        const [movedRow] = rows.splice(rowIndex, 1);
                        rows.splice(targetIndex, 0, movedRow);
                        const rowEvidence = [...(section.row_evidence_refs ?? [])];
                        const [movedEvidence] = rowEvidence.splice(rowIndex, 1);
                        rowEvidence.splice(targetIndex, 0, movedEvidence ?? []);
                        const rowStates = [...(section.row_states ?? [])];
                        const [movedState] = rowStates.splice(rowIndex, 1);
                        rowStates.splice(targetIndex, 0, movedState ?? "unknown");
                        const rowProvenance = rowProvenanceValues(
                          section,
                          artifactProvenance,
                        );
                        const rowIds = [...(section.row_ids ?? [])];
                        const [movedRowId] = rowIds.splice(rowIndex, 1);
                        rowIds.splice(
                          targetIndex,
                          0,
                          movedRowId ??
                            nextEditorId(`${section.id ?? artifactType}-row`),
                        );
                        const [movedProvenance] = rowProvenance.splice(rowIndex, 1);
                        rowProvenance.splice(
                          targetIndex,
                          0,
                          movedProvenance ?? "from_oslo",
                        );
                        rowProvenance[targetIndex] = "confirmed_by_user";
                        onChange({
                          ...section,
                          rows,
                          provenance: "confirmed_by_user",
                          row_evidence_refs: rowEvidence,
                          row_states: rowStates,
                          row_provenance: rowProvenance,
                          row_ids: rowIds,
                        });
                      }}
                      title="Use Up and Down arrow keys to reorder"
                      type="button"
                    >
                      <DotsSixVertical size={12} />
                    </button>
                    <button
                      aria-label="Insert a row after this row"
                      onClick={() => {
                        const rows = section.rows.map((item) => [...item]);
                        rows.splice(rowIndex + 1, 0, section.columns.map(() => ""));
                        const rowEvidence = [...(section.row_evidence_refs ?? [])];
                        rowEvidence.splice(rowIndex + 1, 0, []);
                        const rowStates = [...(section.row_states ?? [])];
                        rowStates.splice(rowIndex + 1, 0, "confirmed");
                        const rowProvenance = rowProvenanceValues(
                          section,
                          artifactProvenance,
                        );
                        rowProvenance.splice(rowIndex + 1, 0, "confirmed_by_user");
                        const rowIds = [...(section.row_ids ?? [])];
                        rowIds.splice(
                          rowIndex + 1,
                          0,
                          nextEditorId(`${section.id ?? artifactType}-row`),
                        );
                        onChange({
                          ...section,
                          rows,
                          provenance: "confirmed_by_user",
                          row_evidence_refs: rowEvidence,
                          row_states: rowStates,
                          row_provenance: rowProvenance,
                          row_ids: rowIds,
                        });
                      }}
                      type="button"
                    >
                      <Plus size={10} />
                    </button>
                    <button
                      aria-label="Delete this row"
                      onClick={() =>
                        onChange({
                          ...section,
                          rows: section.rows.filter((_, index) => index !== rowIndex),
                          provenance: "confirmed_by_user",
                          row_evidence_refs: (section.row_evidence_refs ?? []).filter(
                            (_, index) => index !== rowIndex,
                          ),
                          row_states: (section.row_states ?? []).filter(
                            (_, index) => index !== rowIndex,
                          ),
                          row_provenance: rowProvenanceValues(
                            section,
                            artifactProvenance,
                          ).filter(
                            (_, index) => index !== rowIndex,
                          ),
                          row_ids: (section.row_ids ?? []).filter(
                            (_, index) => index !== rowIndex,
                          ),
                        })
                      }
                      type="button"
                    >
                      <Minus size={10} />
                    </button>
                  </td>
                  {row.map((cell, cellIndex) => (
                    <StableEditableText
                      as="td"
                      className={
                        issueHere && rowIndex === 0 && cellIndex === row.length - 1
                          ? `has-${issueHere.severity.toLowerCase()}-issue`
                          : undefined
                      }
                      key={`${rowIndex}-${cellIndex}`}
                      onValueChange={(value) => {
                        const rows = section.rows.map((item) => [...item]);
                        rows[rowIndex][cellIndex] = value;
                        const rowProvenance = rowProvenanceValues(
                          section,
                          artifactProvenance,
                        );
                        rowProvenance[rowIndex] = "confirmed_by_user";
                        onChange({
                          ...section,
                          rows,
                          row_provenance: rowProvenance,
                        });
                      }}
                      title={
                        issueHere && rowIndex === 0 && cellIndex === row.length - 1
                          ? `${issueHere.title}: ${issueHere.why}`
                          : undefined
                      }
                      value={cell}
                    />
                  ))}
                  {artifactType === "schedule" ? (
                    <td className="artifact-schedule-bar">
                      {scheduleBarStyle(section, row) ? (
                        <span style={scheduleBarStyle(section, row) ?? undefined} />
                      ) : (
                        <button
                          onClick={(event) => {
                            const dateColumn = Math.max(
                              0,
                              section.columns.findIndex((column) => /date|start/i.test(column)),
                            );
                            const cells = event.currentTarget
                              .closest("tr")
                              ?.querySelectorAll<HTMLElement>("td[contenteditable='true']");
                            cells?.[dateColumn]?.focus();
                          }}
                          type="button"
                        >
                          Set date →
                        </button>
                      )}
                    </td>
                  ) : null}
                </tr>
              ))}
            </tbody>
          </table>
          <button
            className="artifact-add-row"
            onClick={() =>
              onChange({
                ...section,
                rows: [...section.rows, section.columns.map(() => "")],
                provenance: "confirmed_by_user",
                row_evidence_refs: [...(section.row_evidence_refs ?? []), []],
                row_states: [...(section.row_states ?? []), "confirmed"],
                row_provenance: [
                  ...rowProvenanceValues(section, artifactProvenance),
                  "confirmed_by_user",
                ],
                row_ids: [
                  ...(section.row_ids ?? []),
                  nextEditorId(`${section.id ?? artifactType}-row`),
                ],
              })
            }
            type="button"
          >
            <Plus size={13} /> Add row
          </button>
        </div>
      ) : null}
      {issueHere ? (
        <button
          className={`artifact-inline-issue severity-${issueHere.severity.toLowerCase()}`}
          onClick={(event) => onOpenIssue(issueHere, event.currentTarget)}
          type="button"
        >
          <span>{issueHere.severity}</span>
          <strong>{issueHere.title}</strong>
          <small>{issueHere.why}</small>
          <ArrowRight size={13} />
        </button>
      ) : null}
    </section>
  );
}

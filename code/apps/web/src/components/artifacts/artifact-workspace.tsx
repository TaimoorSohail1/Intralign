"use client";

import {
  ArrowCounterClockwise,
  ArrowRight,
  CaretDown,
  CaretLeft,
  CaretRight,
  CaretUp,
  Check,
  DotsSixVertical,
  MagnifyingGlass,
  Minus,
  Plus,
  Sparkle,
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

const artifactOrder = [
  "intent",
  "context",
  "scope",
  "requirements",
  "work_breakdown",
  "schedule",
  "resources",
] as const;

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

function ensureEditorIds(
  content: ArtifactWorkspaceSummary["content"],
  artifactType: string,
) {
  const normalized = cloneContent(content);
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

function provenanceLabel(provenance: ArtifactWorkspaceSummary["provenance"]) {
  if (provenance === "confirmed_by_user") return "Confirmed by you";
  if (provenance === "mixed") return "Contains your edits";
  return "From OSLO";
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
  proposalPending,
  proposals = [],
  analysisRunning,
}: {
  artifactType: string;
  projectId: string;
  onAnalysisStarted: (runId: string) => void;
  onAskOslo: (question: string) => void;
  onOpenIssue: (issue: Issue, target: HTMLElement) => void;
  onProposalDecision?: (proposal: IssueProposalSummary, accepted: boolean) => void;
  proposalPending?: string | null;
  proposals?: IssueProposalSummary[];
  analysisRunning: boolean;
}) {
  const [artifact, setArtifact] = useState<ArtifactWorkspaceSummary | null>(null);
  const [content, setContent] = useState<ArtifactWorkspaceSummary["content"] | null>(null);
  const [status, setStatus] = useState<
    "loading" | "saved" | "editing" | "saving" | "stale" | "reanalyzing" | "error"
  >("loading");
  const [error, setError] = useState<string | null>(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [issueIndex, setIssueIndex] = useState(0);
  const [historyDepth, setHistoryDepth] = useState(0);
  const [futureDepth, setFutureDepth] = useState(0);
  const historyRef = useRef<ArtifactWorkspaceSummary["content"][]>([]);
  const futureRef = useRef<ArtifactWorkspaceSummary["content"][]>([]);
  const reanalysisStartedRef = useRef(false);

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
        setContent(cloneContent(normalizedContent));
        historyRef.current = [];
        futureRef.current = [];
        setHistoryDepth(0);
        setFutureDepth(0);
        setIssueIndex(0);
        setStatus("saved");
      })
      .catch((loadError) => {
        if (cancelled) return;
        setError(loadError instanceof Error ? loadError.message : "Artifact could not be loaded");
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [artifactType, projectId]);

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
      setError("Complete or remove empty sections before applying changes");
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
      <header className="artifact-editor-header">
        <div className="artifact-title-row">
          <h1>{artifact.title}</h1>
          <span className="editable-chip">Editable</span>
          <span className="artifact-provenance">
            {provenanceLabel(
              sameContent(content, artifact.content) ? artifact.provenance : "mixed",
            )}
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
            <button
              className="artifact-apply-button"
              disabled={hasEmptySection(content)}
              onClick={() => void applyChanges()}
              type="button"
            >
              Apply changes
            </button>
          ) : null}
        </div>
        {displayStatus === "editing" ||
        displayStatus === "saving" ||
        displayStatus === "stale" ? (
          <p className={`artifact-state-hint is-${displayStatus}`}>
            {displayStatus === "editing"
              ? "Changes stay local until you apply them. Undoing back to the current version starts no analysis."
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

      <div
        className={`artifact-editor-body ${
          artifact.provenance !== "from_oslo" ? "is-confirmed" : ""
        }`}
      >
        {content.sections.map((section, sectionIndex) => (
          <ArtifactSectionEditor
            activeIssue={sectionIndex === issueSectionIndex ? activeIssue : null}
            artifactProvenance={artifact.provenance}
            artifactType={artifactType}
            key={section.id ?? `${artifactType}-${sectionIndex}`}
            onChange={(nextSection) =>
              updateContent((draft) => {
                draft.sections[sectionIndex] = nextSection;
              })
            }
            onOpenIssue={onOpenIssue}
            section={section}
          />
        ))}
      </div>
      {proposals.length && onProposalDecision ? (
        <section aria-label="OSLO proposes in this artifact" className="artifact-proposals">
          <header>
            <span aria-hidden="true">◆</span>
            <div>
              <strong>OSLO proposes</strong>
              <small>{proposals.length} item{proposals.length === 1 ? "" : "s"} for this document · you decide</small>
            </div>
          </header>
          {proposals.map((proposal) => (
            <article key={proposal.id}>
              <span aria-hidden="true">◆</span>
              <div>
                <strong>{proposal.title}</strong>
                <small><b>Why:</b> {proposal.rationale}</small>
              </div>
              <div>
                <button
                  aria-label={`Accept ${proposal.title} in ${label(artifactType)}`}
                  disabled={proposalPending === proposal.id}
                  onClick={() => onProposalDecision(proposal, true)}
                  type="button"
                >{proposalPending === proposal.id ? "Saving…" : "Accept"}</button>
                <button
                  aria-label={`Reject ${proposal.title} in ${label(artifactType)}`}
                  disabled={proposalPending === proposal.id}
                  onClick={() => onProposalDecision(proposal, false)}
                  type="button"
                >Reject</button>
              </div>
            </article>
          ))}
        </section>
      ) : null}
    </section>
  );
}

function ArtifactSectionEditor({
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
      {section.body || (!section.bullets.length && !section.rows.length) ? (
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
      {section.bullets.length ? (
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
              </tr>
            </thead>
            <tbody>
              {section.rows.map((row, rowIndex) => (
                <tr
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

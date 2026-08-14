"use client";

import {
  Check,
  PencilSimple,
  Plus,
  Trash,
  Warning,
  X,
} from "@phosphor-icons/react";
import {
  type FormEvent,
  type KeyboardEvent,
  useLayoutEffect,
  useMemo,
  useRef,
} from "react";

import type {
  ArtifactSection,
  ArtifactWorkspaceSummary,
} from "@/lib/server/oslo-api";

type ArtifactContent = ArtifactWorkspaceSummary["content"];
type ArtifactProvenance = ArtifactWorkspaceSummary["provenance"];
type Issue = ArtifactWorkspaceSummary["issues"][number];

type EntrySource =
  | { kind: "body" }
  | { kind: "bullet"; bulletIndex: number }
  | { kind: "row"; rowIndex: number; cellIndex: number };

interface R2Entry {
  id: string;
  sectionIndex: number;
  sectionHeading: string;
  source: EntrySource;
  text: string;
  meta: string[];
  inferred: boolean;
  confirmed: boolean;
}

interface R2ArtifactContentProps {
  activeIssue: Issue | null;
  artifactProvenance: ArtifactProvenance;
  artifactType: string;
  content: ArtifactContent;
  executionView: "outline" | "backlog";
  issueSectionIndex: number;
  onChangeContent: (mutator: (draft: ArtifactContent) => void) => void;
  onOpenIssue: (issue: Issue, target: HTMLElement) => void;
}

const intentGroups = [
  { key: "purpose", label: "Purpose", hint: "the why" },
  { key: "outcomes", label: "Outcomes", hint: "the end-states you’re steering toward" },
  { key: "goals", label: "Goals", hint: "the aims that ladder up" },
  { key: "success", label: "Success criteria", hint: "the measurable targets" },
  { key: "kpis", label: "KPIs & metrics", hint: "how each target is tracked" },
] as const;

const scopeGroups = [
  { key: "in", label: "✓ In scope", hint: "what the work covers" },
  { key: "out", label: "× Out of scope", hint: "deliberately excluded" },
  { key: "edge", label: "Edge — undecided", hint: "not yet drawn either way" },
] as const;

function isIdentifier(value: string) {
  return /^(?:[A-Z]{1,5}-?\d+|\d+(?:\.\d+){1,4})$/i.test(value.trim());
}

function bestTextCell(section: ArtifactSection, row: string[]) {
  const preferred = section.columns.findIndex((column) =>
    /statement|description|requirement|constraint|deliverable|task|milestone|resource|name|title|outcome|goal/i.test(
      column,
    ),
  );
  if (preferred >= 0 && row[preferred]?.trim()) return preferred;

  const candidates = row
    .map((value, index) => ({ value: value.trim(), index }))
    .filter(({ value }) => value && !isIdentifier(value) && !/^\d{4}-\d{2}-\d{2}$/.test(value));
  if (!candidates.length) return Math.max(0, row.findIndex(Boolean));
  return candidates.sort((left, right) => right.value.length - left.value.length)[0].index;
}

function entryState(
  section: ArtifactSection,
  source: EntrySource,
  artifactProvenance: ArtifactProvenance,
) {
  if (source.kind === "row") {
    const state = section.row_states?.[source.rowIndex];
    const provenance = section.row_provenance?.[source.rowIndex];
    return {
      inferred:
        state === "inferred" ||
        (state !== "confirmed" && provenance === "from_oslo"),
      confirmed: state === "confirmed" || provenance === "confirmed_by_user",
    };
  }
  const confirmed =
    section.provenance === "confirmed_by_user" ||
    artifactProvenance === "confirmed_by_user" ||
    Boolean(section.evidence_refs?.length);
  return {
    inferred:
      !confirmed &&
      (section.provenance === "from_oslo" || artifactProvenance === "from_oslo"),
    confirmed,
  };
}

function entriesForSection(
  section: ArtifactSection,
  sectionIndex: number,
  artifactProvenance: ArtifactProvenance,
) {
  const entries: R2Entry[] = [];
  const hasStructuredRows = section.rows.some((row) =>
    row.some((cell) => cell.trim()),
  );
  if (!hasStructuredRows && section.body.trim()) {
    const source: EntrySource = { kind: "body" };
    entries.push({
      id: `${section.id ?? sectionIndex}-body`,
      sectionIndex,
      sectionHeading: section.heading,
      source,
      text: section.body.trim(),
      meta: [],
      ...entryState(section, source, artifactProvenance),
    });
  }
  if (!hasStructuredRows) section.bullets.forEach((bullet, bulletIndex) => {
    if (!bullet.trim()) return;
    const source: EntrySource = { kind: "bullet", bulletIndex };
    entries.push({
      id: `${section.id ?? sectionIndex}-bullet-${bulletIndex}`,
      sectionIndex,
      sectionHeading: section.heading,
      source,
      text: bullet.trim(),
      meta: [],
      ...entryState(section, source, artifactProvenance),
    });
  });
  section.rows.forEach((row, rowIndex) => {
    const cellIndex = bestTextCell(section, row);
    const text = row[cellIndex]?.trim();
    if (!text) return;
    const source: EntrySource = { kind: "row", rowIndex, cellIndex };
    entries.push({
      id: section.row_ids?.[rowIndex] ?? `${section.id ?? sectionIndex}-row-${rowIndex}`,
      sectionIndex,
      sectionHeading: section.heading,
      source,
      text,
      meta: row.filter((cell, index) => index !== cellIndex && cell.trim()),
      ...entryState(section, source, artifactProvenance),
    });
  });
  return deduplicateEntries(entries);
}

function allEntries(content: ArtifactContent, artifactProvenance: ArtifactProvenance) {
  return deduplicateEntries(
    content.sections.flatMap((section, sectionIndex) =>
      entriesForSection(section, sectionIndex, artifactProvenance),
    ),
  );
}

function normalizedEntryKey(value: string) {
  return value
    .normalize("NFKC")
    .toLocaleLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .trim();
}

function deduplicateEntries(entries: R2Entry[]) {
  const unique = new Map<string, R2Entry>();
  for (const entry of entries) {
    const key = normalizedEntryKey(entry.text);
    if (!key) continue;
    const retained = unique.get(key);
    if (!retained || (retained.inferred && !entry.inferred)) {
      unique.set(key, entry);
    }
  }
  return [...unique.values()];
}

function removeParallelRowState(section: ArtifactSection, rowIndex: number) {
  section.rows.splice(rowIndex, 1);
  section.row_ids?.splice(rowIndex, 1);
  section.row_evidence_refs?.splice(rowIndex, 1);
  section.row_states?.splice(rowIndex, 1);
  section.row_provenance?.splice(rowIndex, 1);
}

function mutateEntry(
  draft: ArtifactContent,
  entry: R2Entry,
  mutation: "confirm" | "delete" | "update",
  value = "",
) {
  const section = draft.sections[entry.sectionIndex];
  if (!section) return;
  if (mutation === "delete") {
    if (entry.source.kind === "body") section.body = "";
    if (entry.source.kind === "bullet") section.bullets.splice(entry.source.bulletIndex, 1);
    if (entry.source.kind === "row") removeParallelRowState(section, entry.source.rowIndex);
    if (!section.body.trim() && !section.bullets.length && !section.rows.length) {
      draft.sections.splice(entry.sectionIndex, 1);
    }
    return;
  }

  section.provenance = "confirmed_by_user";
  if (entry.source.kind === "body" && mutation === "update") section.body = value;
  if (entry.source.kind === "bullet" && mutation === "update") {
    section.bullets[entry.source.bulletIndex] = value;
  }
  if (entry.source.kind === "row") {
    if (mutation === "update") {
      section.rows[entry.source.rowIndex][entry.source.cellIndex] = value;
    }
    const rowStates = [...(section.row_states ?? section.rows.map(() => "unknown" as const))];
    const rowProvenance = [
      ...(section.row_provenance ?? section.rows.map(() => "from_oslo" as const)),
    ];
    rowStates[entry.source.rowIndex] = "confirmed";
    rowProvenance[entry.source.rowIndex] = "confirmed_by_user";
    section.row_states = rowStates;
    section.row_provenance = rowProvenance;
  }
}

function addEntryToGroup(
  draft: ArtifactContent,
  heading: string,
  sectionMatcher: RegExp,
) {
  let section = draft.sections.find((candidate) => sectionMatcher.test(candidate.heading));
  if (!section) {
    section = {
      id: `section-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      heading,
      body: "",
      bullets: [],
      columns: [],
      rows: [],
      row_ids: [],
      provenance: "confirmed_by_user",
    };
    draft.sections.push(section);
  }
  section.bullets.push("New statement");
  section.provenance = "confirmed_by_user";
}

function groupIntent(section: ArtifactSection, index: number) {
  const source = `${section.heading} ${section.body}`.toLowerCase();
  if (/kpi|metric|tracked|measure/.test(source)) return "kpis";
  if (/success|criterion|criteria|target|acceptance/.test(source)) return "success";
  if (/goal|aim|objective/.test(source)) return "goals";
  if (/outcome|end.state|result|business case|benefit|value|impact/.test(source)) return "outcomes";
  if (/purpose|intent|why|summary/.test(source)) return "purpose";
  return intentGroups[Math.min(index, intentGroups.length - 1)].key;
}

function groupScope(section: ArtifactSection, index: number, entry?: R2Entry) {
  const source = `${section.heading} ${entry?.text ?? section.body} ${entry?.meta.join(" ") ?? ""}`.toLowerCase();
  if (/out of scope|outside|exclud|exclusion|not included|rejected/.test(source)) return "out";
  if (/edge|undecided|open|boundary|tbd|deferred/.test(source)) return "edge";
  if (/in scope|included|approved|baseline|covers|scope/.test(source)) return "in";
  return scopeGroups[Math.min(index, scopeGroups.length - 1)].key;
}

function EditableStatement({
  entry,
  issue,
  onConfirm,
  onDelete,
  onOpenIssue,
  onUpdate,
  task = false,
}: {
  entry: R2Entry;
  issue?: Issue | null;
  onConfirm: () => void;
  onDelete: () => void;
  onOpenIssue?: (issue: Issue, target: HTMLElement) => void;
  onUpdate: (value: string) => void;
  task?: boolean;
}) {
  const valueRef = useRef<HTMLSpanElement | null>(null);
  useLayoutEffect(() => {
    if (valueRef.current && document.activeElement !== valueRef.current) {
      valueRef.current.textContent = entry.text;
    }
  }, [entry.text]);

  const handleInput = (event: FormEvent<HTMLSpanElement>) => {
    onUpdate(event.currentTarget.textContent ?? "");
  };
  const handleKeyDown = (event: KeyboardEvent<HTMLSpanElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      event.currentTarget.blur();
    }
  };

  return (
    <div
      className={`r2-statement-row ${entry.inferred ? "is-inferred" : "is-yours"}`}
      data-entry-id={entry.id}
    >
      <i aria-label={entry.inferred ? "OSLO inferred" : "Yours"} />
      <div>
        <span
          contentEditable
          onInput={handleInput}
          onKeyDown={handleKeyDown}
          ref={valueRef}
          suppressContentEditableWarning
        />
        {!task && entry.meta.length ? <small>{entry.meta.join(" · ")}</small> : null}
      </div>
      {issue ? (
        <button
          className="r2-row-warning"
          onClick={(event) => onOpenIssue?.(issue, event.currentTarget)}
          type="button"
        >
          <Warning size={12} /> {issue.title}
        </button>
      ) : null}
      <div className="r2-row-actions">
        {entry.inferred ? (
          <button
            aria-label={`Confirm ${entry.text}`}
            onClick={onConfirm}
            title="Confirm"
            type="button"
          >
            <Check size={13} />
          </button>
        ) : null}
        {!task ? (
          <button
            aria-label={`Edit ${entry.text}`}
            onClick={() => {
              valueRef.current?.focus();
              document.getSelection()?.selectAllChildren(valueRef.current as Node);
            }}
            title="Edit"
            type="button"
          >
            <PencilSimple size={13} />
          </button>
        ) : null}
        <button
          aria-label={`Delete ${entry.text}`}
          onClick={onDelete}
          title="Delete"
          type="button"
        >
          {task ? <X size={13} /> : <Trash size={13} />}
        </button>
      </div>
    </div>
  );
}

function EntryList({
  entries,
  issue,
  issueEntryId,
  onChangeContent,
  onOpenIssue,
}: {
  entries: R2Entry[];
  issue: Issue | null;
  issueEntryId?: string;
  onChangeContent: R2ArtifactContentProps["onChangeContent"];
  onOpenIssue: R2ArtifactContentProps["onOpenIssue"];
}) {
  return entries.map((entry) => (
    <EditableStatement
      entry={entry}
      issue={entry.id === issueEntryId ? issue : null}
      key={entry.id}
      onConfirm={() => onChangeContent((draft) => mutateEntry(draft, entry, "confirm"))}
      onDelete={() => onChangeContent((draft) => mutateEntry(draft, entry, "delete"))}
      onOpenIssue={onOpenIssue}
      onUpdate={(value) =>
        onChangeContent((draft) => mutateEntry(draft, entry, "update", value))
      }
    />
  ));
}

function GroupedUnderstanding({
  artifactType,
  ...props
}: R2ArtifactContentProps) {
  const isIntent = artifactType === "intent";
  const groups = isIntent ? intentGroups : scopeGroups;
  const grouped = new Map<string, R2Entry[]>();
  const issueSection = props.content.sections[props.issueSectionIndex];
  const issueEntryId = issueSection
    ? entriesForSection(issueSection, props.issueSectionIndex, props.artifactProvenance)[0]?.id
    : undefined;
  props.content.sections.forEach((section, sectionIndex) => {
    const entries = entriesForSection(
      section,
      sectionIndex,
      props.artifactProvenance,
    );
    for (const entry of entries) {
      const key = isIntent
        ? groupIntent(section, sectionIndex)
        : groupScope(section, sectionIndex, entry);
      grouped.set(key, [...(grouped.get(key) ?? []), entry]);
    }
  });

  return (
    <div className={`r2-understanding-groups is-${artifactType}`}>
      {groups.map((group) => {
        const entries = deduplicateEntries(grouped.get(group.key) ?? []);
        const matcher = isIntent
          ? new RegExp(group.key === "success" ? "success|criterion|target|acceptance" : group.key, "i")
          : new RegExp(
              group.key === "in"
                ? "in scope|included|covers|scope"
                : group.key === "out"
                  ? "out of scope|exclude|not included"
                  : "edge|undecided|open|boundary|tbd",
              "i",
            );
        return (
          <section className="r2-artifact-group" key={group.key}>
            <header>
              <strong>{group.label}</strong>
              <span>{entries.length}</span>
              <small>{group.hint}</small>
            </header>
            <EntryList
              entries={entries}
              issue={props.activeIssue}
              issueEntryId={issueEntryId}
              onChangeContent={props.onChangeContent}
              onOpenIssue={props.onOpenIssue}
            />
            <button
              className="r2-add-inline"
              onClick={() =>
                props.onChangeContent((draft) => addEntryToGroup(draft, group.label.replace(/^[✓×]\s*/, ""), matcher))
              }
              type="button"
            >
              <Plus size={12} /> add {group.label.replace(/^[✓×]\s*/, "").toLowerCase()}
            </button>
          </section>
        );
      })}
    </div>
  );
}

function FlatUnderstanding(props: R2ArtifactContentProps) {
  const entries = allEntries(props.content, props.artifactProvenance);
  const issueEntryId = entries.find(
    (entry) => entry.sectionIndex === props.issueSectionIndex,
  )?.id;
  return (
    <div className={`r2-flat-statements is-${props.artifactType}`}>
      <EntryList
        entries={entries}
        issue={props.activeIssue}
        issueEntryId={issueEntryId}
        onChangeContent={props.onChangeContent}
        onOpenIssue={props.onOpenIssue}
      />
      <button
        className="r2-add-inline"
        onClick={() =>
          props.onChangeContent((draft) =>
            addEntryToGroup(
              draft,
              props.artifactType === "requirements" ? "Requirements" : "Constraints",
              props.artifactType === "requirements" ? /requirement|acceptance|success/i : /constraint|limit/i,
            ),
          )
        }
        type="button"
      >
        <Plus size={12} /> Add {props.artifactType === "requirements" ? "requirement" : "constraint"}
      </button>
    </div>
  );
}

function wbsCode(entry: R2Entry) {
  return entry.meta.find((value) => /^\d+(?:\.\d+)+$/.test(value.trim()))?.trim() ?? "";
}

function isPackageCode(code: string) {
  return /^\d+\.0$/.test(code);
}

function removeWbsPackage(
  draft: ArtifactContent,
  sectionIndex: number,
  packageEntry: R2Entry,
) {
  if (packageEntry.source.kind !== "row") return;
  const section = draft.sections[sectionIndex];
  if (!section) return;
  const start = packageEntry.source.rowIndex;
  let finish = start + 1;
  while (finish < section.rows.length) {
    const candidateCode = section.rows[finish].find((cell) => /^\d+(?:\.\d+)+$/.test(cell.trim())) ?? "";
    if (isPackageCode(candidateCode)) break;
    finish += 1;
  }
  for (let index = finish - 1; index >= start; index -= 1) {
    removeParallelRowState(section, index);
  }
}

function nextPackageCode(section: ArtifactSection) {
  const values = section.rows
    .flatMap((row) => row.filter((cell) => isPackageCode(cell.trim())))
    .map((code) => Number.parseInt(code, 10))
    .filter(Number.isFinite);
  return `${(values.length ? Math.max(...values) : 0) + 1}.0`;
}

function addWbsRow(
  section: ArtifactSection,
  item: string,
  code: string,
) {
  if (!section.columns.length) section.columns = ["WBS", "Item"];
  const codeIndex = Math.max(0, section.columns.findIndex((column) => /wbs|id|code/i.test(column)));
  let itemIndex = section.columns.findIndex((column) => /item|task|package|name|title/i.test(column));
  if (itemIndex < 0) {
    section.columns.push("Item");
    section.rows.forEach((row) => row.push(""));
    itemIndex = section.columns.length - 1;
  }
  const row = section.columns.map(() => "");
  row[codeIndex] = code;
  row[itemIndex] = item;
  section.rows.push(row);
  section.row_ids = [...(section.row_ids ?? []), `row-${Date.now()}-${section.rows.length}`];
  section.row_states = [...(section.row_states ?? []), "confirmed"];
  section.row_provenance = [...(section.row_provenance ?? []), "confirmed_by_user"];
  section.row_evidence_refs = [...(section.row_evidence_refs ?? []), []];
  section.provenance = "confirmed_by_user";
}

function nextTaskCode(section: ArtifactSection, packageEntry: R2Entry) {
  const packageCode = wbsCode(packageEntry);
  const prefix = packageCode.split(".")[0] || "1";
  const siblings = section.rows
    .flatMap((row) => row.filter((cell) => new RegExp(`^${prefix}\\.(?!0$)\\d+(?:\\.\\d+)*$`).test(cell.trim())))
    .map((code) => Number.parseInt(code.split(".")[1], 10))
    .filter(Number.isFinite);
  return `${prefix}.${(siblings.length ? Math.max(...siblings) : 0) + 1}`;
}

function WbsBranch({
  entry,
  label,
  onConfirm,
  onDelete,
  onUpdate,
}: {
  entry: R2Entry;
  label: "Package" | "Story";
  onConfirm: () => void;
  onDelete: () => void;
  onUpdate: (value: string) => void;
}) {
  const valueRef = useRef<HTMLSpanElement | null>(null);
  useLayoutEffect(() => {
    if (valueRef.current && document.activeElement !== valueRef.current) {
      valueRef.current.textContent = entry.text;
    }
  }, [entry.text]);
  return (
    <div className={`r2-wbs-package ${entry.inferred ? "is-inferred" : "is-yours"}`}>
      <i />
      <span
        contentEditable
        onInput={(event) => onUpdate(event.currentTarget.textContent ?? "")}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            event.currentTarget.blur();
          }
        }}
        ref={valueRef}
        suppressContentEditableWarning
      />
      <em>{label}</em>
      <div className="r2-wbs-branch-actions">
        {entry.inferred ? (
          <button onClick={onConfirm} type="button"><Check size={13} /> Confirm</button>
        ) : null}
        <button aria-label={`Delete ${entry.text}`} onClick={onDelete} type="button"><X size={13} /></button>
      </div>
    </div>
  );
}

function WorkBreakdown(props: R2ArtifactContentProps) {
  return (
    <div className={`r2-wbs is-${props.executionView}`}>
      {props.content.sections.map((section, sectionIndex) => {
        const rowEntries = entriesForSection(
          { ...section, body: "", bullets: [] },
          sectionIndex,
          props.artifactProvenance,
        );
        const packages: Array<{ entry: R2Entry; tasks: R2Entry[] }> = [];
        rowEntries.forEach((entry) => {
          if (isPackageCode(wbsCode(entry)) || !packages.length) {
            packages.push({ entry, tasks: [] });
          } else {
            packages.at(-1)?.tasks.push(entry);
          }
        });
        return (
          <section className="r2-wbs-deliverable" key={section.id ?? sectionIndex}>
            {section.heading ? (
              <header>
                <i />
                <strong
                  contentEditable
                  onInput={(event) =>
                    props.onChangeContent((draft) => {
                      const target = draft.sections[sectionIndex];
                      if (target) target.heading = event.currentTarget.textContent ?? "";
                    })
                  }
                  suppressContentEditableWarning
                >{section.heading}</strong>
                <span>{props.executionView === "backlog" ? "Epic" : "Deliverable"}</span>
                <button
                  aria-label={`Delete ${section.heading}`}
                  onClick={() => props.onChangeContent((draft) => draft.sections.splice(sectionIndex, 1))}
                  type="button"
                ><X size={13} /></button>
              </header>
            ) : null}
            {packages.map((workPackage) => (
              <div className="r2-wbs-package-group" key={workPackage.entry.id}>
                <WbsBranch
                  entry={workPackage.entry}
                  label={props.executionView === "backlog" ? "Story" : "Package"}
                  onConfirm={() => props.onChangeContent((draft) => mutateEntry(draft, workPackage.entry, "confirm"))}
                  onDelete={() => props.onChangeContent((draft) => removeWbsPackage(draft, sectionIndex, workPackage.entry))}
                  onUpdate={(value) => props.onChangeContent((draft) => mutateEntry(draft, workPackage.entry, "update", value))}
                />
                {workPackage.tasks.map((entry) => (
                  <div className="r2-wbs-node is-depth-2" key={entry.id}>
                  <EditableStatement
                    entry={entry}
                    issue={entry.sectionIndex === props.issueSectionIndex ? props.activeIssue : null}
                    onConfirm={() => props.onChangeContent((draft) => mutateEntry(draft, entry, "confirm"))}
                    onDelete={() => props.onChangeContent((draft) => mutateEntry(draft, entry, "delete"))}
                    onOpenIssue={props.onOpenIssue}
                    onUpdate={(value) => props.onChangeContent((draft) => mutateEntry(draft, entry, "update", value))}
                    task
                  />
                  </div>
                ))}
                <button
                  aria-label={`Add task to ${workPackage.entry.text}`}
                  className="r2-add-inline"
                  onClick={() =>
                    props.onChangeContent((draft) => {
                      const target = draft.sections[sectionIndex];
                      if (target) addWbsRow(target, "New task", nextTaskCode(target, workPackage.entry));
                    })
                  }
                  type="button"
                >
                  <Plus size={12} /> Add task
                </button>
              </div>
            ))}
            <button
              className="r2-add-inline is-secondary"
              onClick={() =>
                props.onChangeContent((draft) => {
                  const target = draft.sections[sectionIndex];
                  if (!target) return;
                  addWbsRow(target, "New work package", nextPackageCode(target));
                })
              }
              type="button"
            >
              <Plus size={12} /> Add work package
            </button>
          </section>
        );
      })}
      <p className="r2-wbs-note">
        {props.executionView === "backlog"
          ? "Same work items as the outline — only the framing changes."
          : "Edits write the one task model — confirming an inference or accepting a proposal makes it yours, and Schedule, Resources, and the Full plan · export update too."}
      </p>
    </div>
  );
}

function dateCell(section: ArtifactSection, pattern: RegExp) {
  return section.columns.findIndex((column) => pattern.test(column));
}

function valueAt(row: string[], index: number) {
  return index >= 0 ? row[index] ?? "" : "";
}

function ensureColumn(section: ArtifactSection, label: string) {
  let index = section.columns.findIndex((column) => column.toLowerCase() === label.toLowerCase());
  if (index >= 0) return index;
  section.columns.push(label);
  section.rows.forEach((row) => row.push(""));
  index = section.columns.length - 1;
  return index;
}

function materializeEntryRow(
  section: ArtifactSection,
  entry: R2Entry,
  values: Record<string, string>,
) {
  const itemIndex = ensureColumn(section, "Item");
  const row = section.columns.map(() => "");
  row[itemIndex] = entry.text;
  Object.entries(values).forEach(([column, value]) => {
    row[ensureColumn(section, column)] = value;
  });
  if (entry.source.kind === "body") section.body = "";
  if (entry.source.kind === "bullet") {
    section.bullets.splice(entry.source.bulletIndex, 1);
  }
  section.rows.push(row);
  section.row_ids = [...(section.row_ids ?? []), `row-${Date.now()}`];
  section.row_states = [...(section.row_states ?? []), "confirmed"];
  section.row_provenance = [
    ...(section.row_provenance ?? []),
    "confirmed_by_user",
  ];
  section.provenance = "confirmed_by_user";
}

function Schedule(props: R2ArtifactContentProps) {
  const rows = props.content.sections.flatMap((section, sectionIndex) => {
    const tableRows = section.rows.map((row, rowIndex) => ({
        entry: null,
        row,
        rowIndex,
        section,
        sectionIndex,
      }));
    if (tableRows.length) return tableRows;
    const statementRows = entriesForSection(
      section,
      sectionIndex,
      props.artifactProvenance,
    ).filter((entry) => entry.source.kind !== "row").map(
      (entry, rowIndex) => ({
        entry,
        row: [entry.text],
        rowIndex,
        section,
        sectionIndex,
      }),
    );
    return [...tableRows, ...statementRows];
  });
  const parsed = rows.flatMap(({ row }) => row.map((cell) => Date.parse(cell)).filter(Number.isFinite));
  const minDate = parsed.length ? Math.min(...parsed) : null;
  const maxDate = parsed.length ? Math.max(...parsed) : null;

  return (
    <div className="r2-schedule">
      <div className="r2-schedule-axis" aria-hidden="true">
        <span />
        {Array.from({ length: 7 }, (_, index) => <i key={index} />)}
      </div>
      {rows.map(({ entry, section, sectionIndex, row, rowIndex }) => {
        const nameIndex = bestTextCell(section, row);
        const ownerIndex = dateCell(section, /\b(?:owner|assignee|lead)\b/i);
        const startIndex = dateCell(section, /\b(?:start|begin)\b/i);
        const endIndex = dateCell(section, /\b(?:end|finish|due)\b/i);
        const genericDateIndex = dateCell(section, /^date$|milestone date/i);
        const start = valueAt(row, startIndex >= 0 ? startIndex : genericDateIndex);
        const end = valueAt(row, endIndex);
        const dates = [start, end].map(Date.parse).filter(Number.isFinite);
        let left = 0;
        let width = 0;
        if (minDate !== null && maxDate !== null && dates.length) {
          const domain = Math.max(maxDate - minDate, 86400000);
          left = ((Math.min(...dates) - minDate) / domain) * 84;
          width = Math.max(12, ((Math.max(...dates) - Math.min(...dates)) / domain) * 84);
        }
        const rowState = section.row_states?.[rowIndex];
        const inferred = rowState === "inferred" ||
          (rowState !== "confirmed" && section.row_provenance?.[rowIndex] === "from_oslo");
        const rowContext = row.filter(
          (cell, index) =>
            index !== nameIndex &&
            index !== ownerIndex &&
            index !== startIndex &&
            index !== endIndex &&
            index !== genericDateIndex &&
            cell.trim(),
        );
        return (
          <div className={`r2-schedule-row ${inferred ? "is-inferred" : "is-yours"}`} key={entry?.id ?? section.row_ids?.[rowIndex] ?? `${sectionIndex}-${rowIndex}`}>
            <div className="r2-schedule-name">
              <i />
              <strong title={row[nameIndex] || "Untitled task"}>{row[nameIndex] || "Untitled task"}</strong>
              <small>{valueAt(row, ownerIndex) || rowContext.join(" · ") || "unowned"}</small>
            </div>
            <div className="r2-schedule-dates">
              <input
                aria-label={`Start date for ${row[nameIndex] || "task"}`}
                onChange={(event) => props.onChangeContent((draft) => {
                  const target = draft.sections[sectionIndex];
                  if (entry) {
                    materializeEntryRow(target, entry, { Start: event.target.value });
                    return;
                  }
                  const columnIndex = startIndex >= 0 ? startIndex : genericDateIndex >= 0 ? genericDateIndex : ensureColumn(target, "Start");
                  target.rows[rowIndex][columnIndex] = event.target.value;
                  target.provenance = "confirmed_by_user";
                })}
                placeholder="mm/dd/yyyy"
                value={start}
              />
              <span>→</span>
              <input
                aria-label={`End date for ${row[nameIndex] || "task"}`}
                onChange={(event) => props.onChangeContent((draft) => {
                  const target = draft.sections[sectionIndex];
                  if (entry) {
                    materializeEntryRow(target, entry, { End: event.target.value });
                    return;
                  }
                  const columnIndex = endIndex >= 0 ? endIndex : ensureColumn(target, "End");
                  target.rows[rowIndex][columnIndex] = event.target.value;
                  target.provenance = "confirmed_by_user";
                })}
                placeholder="mm/dd/yyyy"
                value={end}
              />
            </div>
            <div className="r2-schedule-track">
              {dates.length ? <span style={{ left: `${Math.min(82, left)}%`, width: `${Math.min(92 - left, width)}%` }} /> : <button type="button"><Warning size={11} /> set dates →</button>}
            </div>
          </div>
        );
      })}
      {props.activeIssue ? (
        <button
          className="r2-schedule-issue"
          onClick={(event) => props.onOpenIssue(props.activeIssue as Issue, event.currentTarget)}
          type="button"
        >
          <Warning size={13} />
          <span>
            <strong>{props.activeIssue.title}</strong>
            <small>{props.activeIssue.why}</small>
          </span>
        </button>
      ) : null}
    </div>
  );
}

function Resources(props: R2ArtifactContentProps) {
  const rows = props.content.sections.flatMap((section, sectionIndex) => {
    const tableRows = section.rows.map((row, rowIndex) => ({
        entry: null,
        row,
        rowIndex,
        section,
        sectionIndex,
      }));
    const statementRows = entriesForSection(
      section,
      sectionIndex,
      props.artifactProvenance,
    ).filter((entry) => entry.source.kind !== "row").map(
      (entry, rowIndex) => ({
        entry,
        row: [entry.text],
        rowIndex,
        section,
        sectionIndex,
      }),
    );
    return [...tableRows, ...statementRows];
  });
  const assignmentRows = rows.filter(
    ({ section }) => dateCell(section, /\b(?:owner|assignee|lead)\b/i) >= 0,
  );
  const evidenceSections = props.content.sections
    .map((section, sectionIndex) => ({
      entries: entriesForSection(section, sectionIndex, props.artifactProvenance),
      section,
      sectionIndex,
    }))
    .filter(
      ({ section }) => dateCell(section, /\b(?:owner|assignee|lead)\b/i) < 0,
    );
  const owners = Array.from(new Set(assignmentRows.flatMap(({ section, row }) => {
    const ownerIndex = dateCell(section, /\b(?:owner|assignee|lead)\b/i);
    return ownerIndex >= 0 && row[ownerIndex]?.trim() ? [row[ownerIndex].trim()] : [];
  })));
  return (
    <div className="r2-resource-assignments">
      <header>
        <p>People — assign an owner to each task. Unowned work is where execution drift starts.</p>
        <button
          onClick={() => props.onChangeContent((draft) => {
            let target = draft.sections.find((section) =>
              /task owners|people assignments/i.test(section.heading),
            );
            if (!target) {
              target = {
                heading: "Task owners",
                body: "",
                bullets: [],
                columns: ["Resource", "Owner"],
                rows: [],
                provenance: "confirmed_by_user",
              };
              draft.sections.push(target);
            }
            const ownerIndex = ensureColumn(target, "Owner");
            let resourceIndex = target.columns.findIndex((column) =>
              /resource|task|name|title/i.test(column),
            );
            if (resourceIndex < 0) resourceIndex = 0;
            const row = target.columns.map(() => "");
            row[resourceIndex] = "New teammate";
            row[ownerIndex] = "";
            target.rows.push(row);
            target.row_ids = [...(target.row_ids ?? []), `row-${Date.now()}`];
            target.row_states = [...(target.row_states ?? []), "confirmed"];
            target.row_provenance = [...(target.row_provenance ?? []), "confirmed_by_user"];
            target.provenance = "confirmed_by_user";
          })}
          type="button"
        ><Plus size={12} /> Add teammate</button>
      </header>
      {assignmentRows.length ? assignmentRows.map(({ entry, section, sectionIndex, row, rowIndex }) => {
        const nameIndex = bestTextCell(section, row);
        const ownerIndex = dateCell(section, /\b(?:owner|assignee|lead)\b/i);
        const owner = valueAt(row, ownerIndex);
        const rowState = section.row_states?.[rowIndex];
        const inferred = rowState === "inferred" ||
          (rowState !== "confirmed" && section.row_provenance?.[rowIndex] === "from_oslo");
        return (
          <div className={`r2-resource-row ${!owner ? "is-unassigned" : ""}`} key={entry?.id ?? section.row_ids?.[rowIndex] ?? `${sectionIndex}-${rowIndex}`}>
            <div>
              <strong title={row[nameIndex] || "Untitled task"}>{row[nameIndex] || "Untitled task"}</strong>
              <small>{section.heading}{row.filter((cell, index) => index !== nameIndex && index !== ownerIndex && cell.trim()).length ? ` · ${row.filter((cell, index) => index !== nameIndex && index !== ownerIndex && cell.trim()).join(" · ")}` : ""}</small>
            </div>
            <select
              aria-label={`Owner for ${row[nameIndex] || "task"}`}
              onChange={(event) => props.onChangeContent((draft) => {
                const target = draft.sections[sectionIndex];
                if (entry) {
                  materializeEntryRow(target, entry, { Owner: event.target.value });
                  return;
                }
                const columnIndex = ownerIndex >= 0 ? ownerIndex : ensureColumn(target, "Owner");
                target.rows[rowIndex][columnIndex] = event.target.value;
                target.row_states = [...(target.row_states ?? target.rows.map(() => "unknown" as const))];
                target.row_provenance = [...(target.row_provenance ?? target.rows.map(() => "from_oslo" as const))];
                target.row_states[rowIndex] = "confirmed";
                target.row_provenance[rowIndex] = "confirmed_by_user";
                target.provenance = "confirmed_by_user";
              })}
              value={owner}
            >
              <option value="">{ownerIndex >= 0 ? "— unassigned —" : "— assign owner —"}</option>
              {!owners.includes("You") ? <option value="You">You</option> : null}
              {owners.map((candidate) => <option key={candidate} value={candidate}>{candidate}</option>)}
            </select>
            <span className={inferred ? "is-inferred" : "is-yours"}>{inferred ? "OSLO inferred" : "yours"}</span>
          </div>
        );
      }) : <p className="r2-resource-empty">No task owner assignments are recorded yet.</p>}
      {evidenceSections.length ? (
        <div aria-label="Resource evidence" className="r2-resource-evidence">
          {evidenceSections.map(({ entries, section, sectionIndex }) => (
            <section key={section.id ?? `${section.heading}-${sectionIndex}`}>
              <h2>{section.heading || "Resource evidence"}</h2>
              <EntryList
                entries={entries}
                issue={sectionIndex === props.issueSectionIndex ? props.activeIssue : null}
                issueEntryId={entries[0]?.id}
                onChangeContent={props.onChangeContent}
                onOpenIssue={props.onOpenIssue}
              />
            </section>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export function R2ArtifactContent(props: R2ArtifactContentProps) {
  if (props.artifactType === "intent" || props.artifactType === "scope") {
    return <GroupedUnderstanding {...props} />;
  }
  if (props.artifactType === "requirements" || props.artifactType === "constraints") {
    return <FlatUnderstanding {...props} />;
  }
  if (props.artifactType === "work_breakdown") return <WorkBreakdown {...props} />;
  if (props.artifactType === "schedule") return <Schedule {...props} />;
  return <Resources {...props} />;
}

export function R2Narrative({
  artifactProvenance,
  artifactType,
  content,
}: Pick<R2ArtifactContentProps, "artifactProvenance" | "artifactType" | "content">) {
  const entries = useMemo(
    () => allEntries(content, artifactProvenance),
    [artifactProvenance, content],
  );
  const yours = entries.filter((entry) => !entry.inferred);
  const inferred = entries.filter((entry) => entry.inferred);
  const lead = artifactType === "intent"
    ? "Here is what this plan is setting out to achieve, in plain language."
    : artifactType === "scope"
      ? "Here are the boundaries this plan currently sets."
      : artifactType === "requirements"
        ? "Here is what must be true for this plan to hold."
        : "Here are the hard limits the plan must work within.";
  return (
    <article
      className="artifact-narrative r2-artifact-narrative"
      aria-label={`${artifactType.slice(0, 1).toUpperCase()}${artifactType.slice(1).replaceAll("_", " ")} narrative`}
    >
      <div className="artifact-narrative-provenance">
        <span>your evidence</span>
        <span>OSLO&apos;s inference — holds until you confirm</span>
      </div>
      <p>{lead}</p>
      {yours.length ? <p>{yours.map((entry) => entry.text).join(" ")}</p> : null}
      {inferred.length ? (
        <p className="is-inferred">
          OSLO also reads {inferred.map((entry) => entry.text).join(" ")}
          <strong> Nothing enters your plan until you accept it in the Statements view.</strong>
        </p>
      ) : null}
      <footer>
        A plain-language reading of your statements — provenance and all. Switch to Statements to edit; this view rewrites itself.
      </footer>
    </article>
  );
}

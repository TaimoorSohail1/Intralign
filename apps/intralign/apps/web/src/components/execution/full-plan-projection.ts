import type {
  ArtifactSection,
  ArtifactWorkspaceSummary,
  IssueProposalSummary,
  OverviewSnapshot,
} from "@/lib/server/oslo-api";

export type FullPlanRowState = "yours" | "inferred" | "proposed";

export type FullPlanRow = {
  id: string;
  task: string;
  workPackage: string;
  deliverable: string;
  owner: string | null;
  start: string | null;
  due: string | null;
  schedule: string | null;
  state: FullPlanRowState;
  provenance: string[];
  note: string;
};

export type FullPlanProjection = {
  rows: FullPlanRow[];
  confirmedCount: number;
  inferredCount: number;
  proposedCount: number;
  missingWorkBreakdown: boolean;
};

type Artifact = OverviewSnapshot["artifacts"][number];

type IndexedRow = {
  id: string;
  section: ArtifactSection;
  sectionHeading: string;
  rowIndex: number;
  values: string[];
  fields: Record<string, string>;
  evidenceRefs: string[];
  state: NonNullable<ArtifactSection["row_states"]>[number] | null;
  provenance: NonNullable<ArtifactSection["row_provenance"]>[number] | null;
};

function normalized(value: string) {
  return value.trim().toLocaleLowerCase();
}

function firstField(fields: Record<string, string>, ...names: string[]) {
  for (const name of names) {
    const value = fields[normalized(name)]?.trim();
    if (value) return value;
  }
  return null;
}

function indexedRows(artifact: Artifact | undefined): IndexedRow[] {
  if (!artifact) return [];
  return (artifact.content?.sections ?? []).flatMap((section, sectionIndex) =>
    (section.rows ?? []).map((row, rowIndex) => {
      const values = row.map((value) => String(value ?? "").trim());
      const fields = Object.fromEntries(
        values.map((value, columnIndex) => [
          normalized(section.columns?.[columnIndex] || `field ${columnIndex + 1}`),
          value,
        ]),
      );
      return {
        id: section.row_ids?.[rowIndex] || `${artifact.artifact_type}-${sectionIndex + 1}-${rowIndex + 1}`,
        section,
        sectionHeading: section.heading,
        rowIndex,
        values,
        fields,
        evidenceRefs: section.row_evidence_refs?.[rowIndex] ?? artifact.evidence_refs ?? [],
        state: section.row_states?.[rowIndex] ?? null,
        provenance: section.row_provenance?.[rowIndex] ?? null,
      };
    }),
  );
}

function taskName(row: IndexedRow) {
  return (
    firstField(row.fields, "item", "task", "name", "key deliverable", "deliverable") ??
    row.values.find((value, index) => normalized(row.section.columns?.[index] ?? "") !== "wbs" && value) ??
    ""
  );
}

function wbsCode(row: IndexedRow) {
  return firstField(row.fields, "wbs", "code") ?? "";
}

function isGovernedTask(row: IndexedRow, rows: IndexedRow[]) {
  const name = taskName(row);
  if (!name) return false;
  const code = wbsCode(row);
  if (!code) return true;
  const segments = code.split(".");
  if (segments.at(-1) === "0") {
    return !rows.some((candidate) => {
      const candidateCode = wbsCode(candidate);
      return candidateCode !== code && candidateCode.split(".")[0] === segments[0];
    });
  }
  return !rows.some((candidate) => {
    const candidateCode = wbsCode(candidate);
    return candidateCode !== code && candidateCode.startsWith(`${code}.`);
  });
}

function hierarchyFor(row: IndexedRow, rows: IndexedRow[]) {
  const code = wbsCode(row);
  const explicitDeliverable = firstField(row.fields, "deliverable");
  const explicitPackage = firstField(row.fields, "work package", "package", "workstream");
  if (!code) {
    return {
      deliverable: explicitDeliverable ?? row.sectionHeading ?? "Plan",
      workPackage: explicitPackage ?? row.sectionHeading ?? "Plan",
    };
  }

  if (code.endsWith(".0")) {
    return {
      deliverable: explicitDeliverable ?? row.sectionHeading ?? "Plan",
      workPackage: explicitPackage ?? taskName(row),
    };
  }

  const segments = code.split(".");
  const deliverableCode = `${segments[0]}.0`;
  const packageCode = segments.length > 1 ? segments.slice(0, 2).join(".") : code;
  const deliverable = rows.find((candidate) => wbsCode(candidate) === deliverableCode);
  const workPackage = rows.find((candidate) => wbsCode(candidate) === packageCode);
  return {
    deliverable: explicitDeliverable ?? (deliverable ? taskName(deliverable) : row.sectionHeading || "Plan"),
    workPackage: explicitPackage ?? (workPackage ? taskName(workPackage) : row.sectionHeading || "Plan"),
  };
}

function indexFacetRows(rows: IndexedRow[]) {
  const byId = new Map(rows.map((row) => [row.id, row]));
  const byName = new Map(
    rows
      .map((row) => [normalized(taskName(row)), row] as const)
      .filter(([name]) => Boolean(name)),
  );
  return { byId, byName };
}

function matchingFacet(
  row: IndexedRow,
  index: ReturnType<typeof indexFacetRows>,
) {
  return index.byId.get(row.id) ?? index.byName.get(normalized(taskName(row))) ?? null;
}

function unique(values: Array<string | null | undefined>) {
  return Array.from(new Set(values.filter((value): value is string => Boolean(value?.trim()))));
}

function scheduleLabel(start: string | null, due: string | null) {
  if (start && due && start !== due) return `${start} – ${due}`;
  return start ?? due;
}

export function withCurrentFullPlanArtifacts(
  snapshot: OverviewSnapshot,
  workspaces: ArtifactWorkspaceSummary[],
): OverviewSnapshot {
  const current = new Map(workspaces.map((artifact) => [artifact.artifact_type, artifact]));
  const projected = snapshot.artifacts.map((artifact) => {
    const workspace = current.get(artifact.artifact_type);
    if (!workspace) return artifact;
    current.delete(artifact.artifact_type);
    return {
      ...artifact,
      title: workspace.title,
      reliability: workspace.reliability,
      basis: workspace.basis,
      evidence_refs: workspace.evidence_refs,
      content: workspace.content,
      assumptions: workspace.assumptions,
      conflicts: workspace.conflicts,
    };
  });
  for (const workspace of current.values()) {
    projected.push({
      artifact_type: workspace.artifact_type,
      title: workspace.title,
      summary: workspace.basis,
      reliability: workspace.reliability,
      basis: workspace.basis,
      evidence_refs: workspace.evidence_refs,
      content: workspace.content,
      assumptions: workspace.assumptions,
      conflicts: workspace.conflicts,
    });
  }
  return { ...snapshot, artifacts: projected };
}

export function buildFullPlanProjection(
  snapshot: OverviewSnapshot,
  proposals: IssueProposalSummary[] = [],
): FullPlanProjection {
  const workBreakdown = snapshot.artifacts.find(
    (artifact) => artifact.artifact_type === "work_breakdown",
  );
  const workRows = indexedRows(workBreakdown);
  const scheduleRows = indexFacetRows(
    indexedRows(snapshot.artifacts.find((artifact) => artifact.artifact_type === "schedule")),
  );
  const resourceRows = indexFacetRows(
    indexedRows(snapshot.artifacts.find((artifact) => artifact.artifact_type === "resources")),
  );

  const governedRows: FullPlanRow[] = workRows
    .filter((row) => isGovernedTask(row, workRows))
    .map((row) => {
      const schedule = matchingFacet(row, scheduleRows);
      const resource = matchingFacet(row, resourceRows);
      const start = schedule
        ? firstField(schedule.fields, "start", "start date", "starts")
        : null;
      const due = schedule
        ? firstField(schedule.fields, "due", "due date", "end", "end date", "date")
        : null;
      const owner =
        (resource
          ? firstField(resource.fields, "owner", "responsible", "accountable", "lead")
          : null) ??
        (schedule
          ? firstField(schedule.fields, "owner", "responsible", "accountable", "lead")
          : null);
      const hierarchy = hierarchyFor(row, workRows);
      return {
        id: row.id,
        task: taskName(row),
        workPackage: hierarchy.workPackage,
        deliverable: hierarchy.deliverable,
        owner,
        start,
        due,
        schedule: scheduleLabel(start, due),
        state: row.provenance === "confirmed_by_user" ? "yours" : "inferred",
        provenance: unique([
          ...row.evidenceRefs,
          ...(schedule?.evidenceRefs ?? []),
          ...(resource?.evidenceRefs ?? []),
        ]),
        note: firstField(row.fields, "note", "notes", "description", "detail") ?? "",
      } satisfies FullPlanRow;
    });

  const proposedRows: FullPlanRow[] = proposals
    .filter(
      (proposal) =>
        proposal.artifact_type === "work_breakdown" &&
        !proposal.accepted &&
        !proposal.rejected,
    )
    .map((proposal) => ({
      id: proposal.id,
      task: proposal.title,
      workPackage: "OSLO proposes",
      deliverable: "Optional addition",
      owner: null,
      start: null,
      due: null,
      schedule: null,
      state: "proposed",
      provenance: [],
      note: proposal.rationale,
    }));

  const rows = [...governedRows, ...proposedRows];
  return {
    rows,
    confirmedCount: rows.filter((row) => row.state === "yours").length,
    inferredCount: rows.filter((row) => row.state === "inferred").length,
    proposedCount: rows.filter((row) => row.state === "proposed").length,
    missingWorkBreakdown: !workBreakdown,
  };
}

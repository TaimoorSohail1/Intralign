import type { OverviewSnapshot } from "@/lib/server/oslo-api";

export type PlanExportPayload = {
  content: string;
  extension: "csv" | "xls" | "txt";
  mime: "text/csv" | "application/vnd.ms-excel" | "text/plain";
};

type ExportRecord = {
  artifact: string;
  section: string;
  fields: Record<string, string>;
  provenance: string;
};

function protectSpreadsheetCell(value: string) {
  return /^[\t\r ]*[=+\-@]/.test(value) ? `'${value}` : value;
}

function csvCell(value: string) {
  const safe = protectSpreadsheetCell(value);
  return /[",\r\n]/.test(safe) ? `"${safe.replaceAll('"', '""')}"` : safe;
}

function htmlCell(value: string) {
  return protectSpreadsheetCell(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function exportRecords(snapshot: OverviewSnapshot): ExportRecord[] {
  return snapshot.artifacts.flatMap((artifact) => {
    const sections = artifact.content?.sections ?? [];
    if (!sections.length) {
      return [{
        artifact: artifact.title,
        section: artifact.artifact_type,
        fields: { Item: artifact.summary },
        provenance: artifact.evidence_refs.join(" | "),
      }];
    }
    return sections.flatMap((section) => {
      const rows = section.rows ?? [];
      if (rows.length) {
        return rows.map((row, index) => ({
          artifact: artifact.title,
          section: section.heading,
          fields: Object.fromEntries(
            row.map((value, columnIndex) => [
              section.columns?.[columnIndex] || `Field ${columnIndex + 1}`,
              value,
            ]),
          ),
          provenance: (section.row_evidence_refs?.[index] ?? artifact.evidence_refs).join(" | "),
        }));
      }
      const items = section.bullets?.length
        ? section.bullets
        : section.body
          ? [section.body]
          : [];
      return items.map((item, index) => ({
        artifact: artifact.title,
        section: section.heading,
        fields: { Item: item },
        provenance: (section.row_evidence_refs?.[index] ?? artifact.evidence_refs).join(" | "),
      }));
    });
  });
}

export function buildPlanExport(snapshot: OverviewSnapshot): {
  csv: PlanExportPayload;
  excel: PlanExportPayload;
  text: PlanExportPayload;
} {
  const records = exportRecords(snapshot);
  const fieldNames = Array.from(new Set(records.flatMap((record) => Object.keys(record.fields))));
  const headers = ["Artifact", "Section", ...fieldNames, "Provenance"];
  const rows = records.map((record) => [
    record.artifact,
    record.section,
    ...fieldNames.map((field) => record.fields[field] ?? ""),
    record.provenance,
  ]);
  const title = snapshot.project_title || "Project";

  const csv = [
    ["Project", title],
    ["Analysis completed", snapshot.published_at],
    ["Analysis run", snapshot.analysis_run_id],
    [],
    headers,
    ...rows,
  ].map((row) => row.map(csvCell).join(",")).join("\r\n");

  const excelRows = [headers, ...rows]
    .map((row, index) => `<tr>${row.map((value) => `<${index ? "td" : "th"}>${htmlCell(value)}</${index ? "td" : "th"}>`).join("")}</tr>`)
    .join("");
  const excel = `<!doctype html><html><head><meta charset="utf-8"></head><body>` +
    `<h1>${htmlCell(title)}</h1><p>Analysis completed: ${htmlCell(snapshot.published_at)}</p>` +
    `<table>${excelRows}</table></body></html>`;

  const text = [
    title,
    `Analysis completed: ${snapshot.published_at}`,
    `Analysis run: ${snapshot.analysis_run_id}`,
    "",
    ...records.flatMap((record) => [
      `${record.artifact} — ${record.section}`,
      ...Object.entries(record.fields).map(([name, value]) => `${name}: ${value}`),
      `Provenance: ${record.provenance || "Not recorded"}`,
      "",
    ]),
    "OSLO advisory disclaimer: this is a maturity read of the retained plan, not a forecast or probability of success.",
  ].join("\r\n");

  return {
    csv: { content: csv, extension: "csv", mime: "text/csv" },
    excel: { content: excel, extension: "xls", mime: "application/vnd.ms-excel" },
    text: { content: text, extension: "txt", mime: "text/plain" },
  };
}

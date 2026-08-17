import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import type { FullPlanProjection } from "./full-plan-projection";

export type FullPlanExportPayload = {
  content: string;
  extension: "csv" | "xls" | "txt";
  mime: "text/csv" | "application/vnd.ms-excel" | "text/plain";
};

const exportHeaders = [
  "Deliverable",
  "Workstream",
  "Task",
  "Owner",
  "Start",
  "Due",
  "Provenance",
  "Note",
] as const;

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

function slug(value: string) {
  return value
    .toLocaleLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || "project";
}

function taskRows(projection: FullPlanProjection) {
  return projection.rows.map((row) => [
    row.deliverable,
    row.workPackage,
    row.task,
    row.owner ?? "",
    row.start ?? "",
    row.due ?? "",
    row.provenance.join(" | "),
    row.note,
  ]);
}

function warningLine(projection: FullPlanProjection) {
  const governed = projection.rows.filter((row) => row.state !== "proposed");
  const unowned = governed.filter((row) => !row.owner).length;
  const unscheduled = governed.filter((row) => !row.schedule).length;
  if (!unowned && !unscheduled) return "Warning: none.";
  const ownerLabel = `${unowned} task${unowned === 1 ? " is" : "s are"} unowned`;
  const scheduleLabel = `${unscheduled} task${unscheduled === 1 ? " is" : "s are"} unscheduled`;
  return `Warning: ${ownerLabel}; ${scheduleLabel}.`;
}

export function buildFullPlanExport(
  snapshot: OverviewSnapshot,
  projection: FullPlanProjection,
): {
  baseName: string;
  csv: FullPlanExportPayload;
  excel: FullPlanExportPayload;
  text: FullPlanExportPayload;
} {
  const title = snapshot.project_title?.trim() || "Project";
  const baseName = `${slug(title)}-full-plan`;
  const rows = taskRows(projection);
  const warning = warningLine(projection);

  const csv = [
    ["Project", title],
    ["Analysis completed", snapshot.published_at],
    ["Analysis run", snapshot.analysis_run_id],
    ["Warning", warning.replace(/^Warning:\s*/, "")],
    [],
    [...exportHeaders],
    ...rows,
  ]
    .map((row) => row.map(csvCell).join(","))
    .join("\r\n");

  const excelRows = [[...exportHeaders], ...rows]
    .map((row, rowIndex) => {
      const tag = rowIndex ? "td" : "th";
      return `<tr>${row.map((value) => `<${tag}>${htmlCell(value)}</${tag}>`).join("")}</tr>`;
    })
    .join("");
  const excel = [
    "<!doctype html><html><head><meta charset=\"utf-8\"></head><body>",
    `<h1>${htmlCell(title)} — Full plan</h1>`,
    `<p>Analysis completed: ${htmlCell(snapshot.published_at)}</p>`,
    `<p>${htmlCell(warning)}</p>`,
    `<table>${excelRows}</table>`,
    "</body></html>",
  ].join("");

  const text = [
    `${title} — Full plan`,
    `Analysis completed: ${snapshot.published_at}`,
    `Analysis run: ${snapshot.analysis_run_id}`,
    warning,
    "",
    ...projection.rows.flatMap((row, index) => [
      `${index + 1}. ${row.task}`,
      `Deliverable: ${row.deliverable}`,
      `Workstream: ${row.workPackage}`,
      `Owner: ${row.owner ?? "Unowned"}`,
      `Schedule: ${row.schedule ?? "Unscheduled"}`,
      `State: ${row.state}`,
      `Provenance: ${row.provenance.join(" | ") || "Not recorded"}`,
      `Note: ${row.note || "—"}`,
      "",
    ]),
    "OSLO advisory disclaimer: this is a maturity read of the retained plan, not a forecast or probability of success.",
  ].join("\r\n");

  return {
    baseName,
    csv: { content: csv, extension: "csv", mime: "text/csv" },
    excel: { content: excel, extension: "xls", mime: "application/vnd.ms-excel" },
    text: { content: text, extension: "txt", mime: "text/plain" },
  };
}

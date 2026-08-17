"use client";

import { DownloadSimple, FileText, X } from "@phosphor-icons/react";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";

import type {
  AsanaHandoffState,
  IssueProposalSummary,
  OverviewSnapshot,
} from "@/lib/server/oslo-api";

import { buildFullPlanExport } from "./full-plan-export-content";
import { buildFullPlanProjection } from "./full-plan-projection";

type ExportFormat = "excel" | "csv" | "text" | "pdf";

function downloadBlob(content: BlobPart, mime: string, fileName: string) {
  const blob = content instanceof Blob ? content : new Blob([content], { type: mime });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = fileName;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(href);
}

function formatLabel(format: ExportFormat) {
  if (format === "excel") return "Excel";
  if (format === "text") return "Text";
  return format.toUpperCase();
}

export function FullPlanWorkspace({
  snapshot,
  proposals,
}: {
  snapshot: OverviewSnapshot;
  proposals: IssueProposalSummary[];
}) {
  const projection = useMemo(
    () => buildFullPlanProjection(snapshot, proposals),
    [proposals, snapshot],
  );
  const exports = useMemo(
    () => buildFullPlanExport(snapshot, projection),
    [projection, snapshot],
  );
  const dialogRef = useRef<HTMLDivElement>(null);
  const [exportOpen, setExportOpen] = useState(false);
  const [exportFormat, setExportFormat] = useState<ExportFormat>("pdf");
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [pending, setPending] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [exportError, setExportError] = useState<string | null>(null);
  const [asanaState, setAsanaState] = useState<AsanaHandoffState | null>(null);

  const governedRows = projection.rows.filter((row) => row.state !== "proposed");
  const unownedCount = governedRows.filter((row) => !row.owner).length;
  const unscheduledCount = governedRows.filter((row) => !row.schedule).length;

  useEffect(() => {
    if (!exportOpen) return;
    dialogRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setExportOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    void fetch(`/api/projects/${snapshot.project_id}/report/asana`)
      .then((response) => response.ok ? response.json() : null)
      .then((result) => {
        if (result) setAsanaState(result as AsanaHandoffState);
      })
      .catch(() => undefined);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [exportOpen, snapshot.project_id]);

  const recordExport = (format: ExportFormat) =>
    fetch(`/api/projects/${snapshot.project_id}/report/exports`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ format, surface: "full_plan" }),
    }).catch(() => null);

  const runExport = async () => {
    setPending(true);
    setExportError(null);
    setNotice(null);
    try {
      if (exportFormat === "pdf") {
        const response = await fetch(
          `/api/projects/${snapshot.project_id}/full-plan/export`,
        );
        if (!response.ok) {
          const result = await response.json().catch(() => ({}));
          throw new Error(result.message || "The PDF could not be exported.");
        }
        const blob = await response.blob();
        downloadBlob(blob, "application/pdf", `${exports.baseName}.pdf`);
      } else {
        const payload = exports[exportFormat];
        downloadBlob(
          payload.content,
          `${payload.mime};charset=utf-8`,
          `${exports.baseName}.${payload.extension}`,
        );
      }
      if (exportFormat !== "pdf") void recordExport(exportFormat);
      setNotice(`${formatLabel(exportFormat)} export downloaded.`);
      setExportOpen(false);
    } catch (error) {
      setExportError(
        error instanceof Error ? error.message : "The export failed safely. Try again.",
      );
    } finally {
      setPending(false);
    }
  };

  const importToAsana = async () => {
    if (!asanaState?.entitled) {
      setNotice("Asana hand-off requires Basic. Manual exports remain free.");
      setExportOpen(false);
      return;
    }
    if (!asanaState.configured) {
      setNotice("Connect an Asana project in workspace settings before importing.");
      setExportOpen(false);
      return;
    }
    setPending(true);
    setExportError(null);
    try {
      const response = await fetch(`/api/projects/${snapshot.project_id}/report/asana`, {
        method: "POST",
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.message || "Asana import failed safely.");
      setNotice(`${result.completed_count} executable plan items imported to Asana.`);
      setExportOpen(false);
    } catch (error) {
      setExportError(error instanceof Error ? error.message : "Asana import failed safely.");
    } finally {
      setPending(false);
    }
  };

  return (
    <section className="full-plan-workspace" aria-labelledby="full-plan-heading">
      <header className="full-plan-heading">
        <span>Execution</span>
        <h1 id="full-plan-heading">Full plan · export</h1>
      </header>

      <p className="full-plan-read">
        <strong>OSLO’s read:</strong> The whole sequenced plan — task, owner, dates,
        provenance. Read-only: this is what leaves as the export.
      </p>

      {snapshot.freshness?.state === "stale" || snapshot.freshness?.state === "reanalyzing" ? (
        <aside className="full-plan-freshness" role="status">
          Showing the last completed plan while OSLO consolidates the latest changes.
        </aside>
      ) : null}

      {projection.rows.length ? (
        <div className="full-plan-table-wrap">
          <table aria-label="Full execution plan" className="full-plan-table">
            <thead>
              <tr>
                <th scope="col">Task</th>
                <th scope="col">Work package</th>
                <th scope="col">Deliverable</th>
                <th scope="col">Owner</th>
                <th scope="col">Schedule</th>
                <th scope="col">State</th>
              </tr>
            </thead>
            <tbody>
              {projection.rows.map((row) => (
                <tr className={`is-${row.state}`} key={row.id}>
                  <th scope="row">{row.task}</th>
                  <td>{row.workPackage}</td>
                  <td>{row.deliverable}</td>
                  <td className={!row.owner ? "is-missing" : undefined}>
                    {row.owner ?? "— unowned"}
                  </td>
                  <td className={!row.schedule ? "is-missing" : undefined}>
                    {row.schedule ?? "unscheduled"}
                  </td>
                  <td><span className="full-plan-state">{row.state}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="full-plan-empty">
          <FileText aria-hidden="true" size={24} />
          <h2>No execution tasks yet</h2>
          <p>Build the governed hierarchy first; this export never invents work.</p>
          <Link href={`/projects/${snapshot.project_id}/artifacts/work_breakdown`}>
            Open Work Breakdown
          </Link>
        </div>
      )}

      <footer className="full-plan-export-bar">
        <button
          className="button is-primary"
          disabled={!governedRows.length}
          onClick={() => setExportOpen(true)}
          type="button"
        >
          <DownloadSimple aria-hidden="true" size={15} /> Export plan
        </button>
        <span>This combined view is what a PM tool consumes.</span>
        {unownedCount || unscheduledCount ? (
          <small>
            {unownedCount} unowned · {unscheduledCount} unscheduled — exported with warnings
          </small>
        ) : null}
      </footer>

      {notice ? <p className="full-plan-notice" role="status">{notice}</p> : null}

      {exportOpen ? createPortal(
        <div className="report-modal-backdrop" onMouseDown={() => setExportOpen(false)}>
          <div
            aria-label="Export your plan"
            aria-modal="true"
            className="report-export-panel full-plan-export-panel"
            onMouseDown={(event) => event.stopPropagation()}
            ref={dialogRef}
            role="dialog"
            tabIndex={-1}
          >
            <header>
              <div>
                <span className="report-popover-label">Export your plan</span>
                <p>
                  <strong>{snapshot.project_title || "Project"}</strong> · {governedRows.length}{" "}
                  {governedRows.length === 1 ? "task" : "tasks"} · {snapshot.assessment.integrity.level}
                </p>
              </div>
              <div className="report-export-header-actions">
                <button
                  aria-expanded={detailsOpen}
                  onClick={() => setDetailsOpen((current) => !current)}
                  type="button"
                >
                  Details
                </button>
                <button aria-label="Close export" onClick={() => setExportOpen(false)} type="button">
                  <X aria-hidden="true" size={15} />
                </button>
              </div>
            </header>
            {detailsOpen ? (
              <aside className="report-export-details" role="note">
                <span>Read-only projection of the retained execution plan</span>
                <strong>
                  {projection.confirmedCount} yours · {projection.inferredCount} inferred · {projection.proposedCount} proposed
                </strong>
                <p>{unownedCount} unowned · {unscheduledCount} unscheduled. Hidden reasoning is excluded.</p>
              </aside>
            ) : null}
            <span className="report-popover-label">Choose a format</span>
            <div aria-label="Export format" className="report-export-formats" role="group">
              {(["excel", "csv", "text", "pdf"] as const).map((format) => (
                <button
                  aria-pressed={exportFormat === format}
                  key={format}
                  onClick={() => setExportFormat(format)}
                  type="button"
                >
                  {format === "pdf" ? "PDF package" : formatLabel(format)}
                </button>
              ))}
            </div>
            <p>A dated snapshot with provenance, visible warnings, and the advisory disclaimer.</p>
            {exportError ? <p className="full-plan-export-error" role="alert">{exportError}</p> : null}
            <div className="report-export-actions">
              <button className="is-primary" disabled={pending} onClick={() => void runExport()} type="button">
                <DownloadSimple aria-hidden="true" size={14} />
                {pending ? "Exporting…" : exportError ? "Retry export" : exportFormat === "pdf" ? "Export as PDF" : `Download ${formatLabel(exportFormat)}`}
              </button>
              <button onClick={() => setExportOpen(false)} type="button">Cancel</button>
            </div>
            <div className="report-asana-gate">
              <div>
                <strong>Or let OSLO import it into Asana for you</strong>
                <span>One-way · executable plan fields only</span>
              </div>
              <button disabled={pending} onClick={() => void importToAsana()} type="button">
                {!asanaState?.entitled
                  ? "Upgrade to Basic →"
                  : !asanaState.configured
                    ? "Connect Asana →"
                    : `Import ${asanaState.preview.length} tasks →`}
              </button>
            </div>
            <footer>
              Carries OSLO’s advisory disclaimer — a read of the plan’s maturity, not a forecast.
            </footer>
          </div>
        </div>,
        document.body,
      ) : null}
    </section>
  );
}

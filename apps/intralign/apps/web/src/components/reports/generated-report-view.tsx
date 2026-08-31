"use client";

import { DownloadSimple } from "@phosphor-icons/react";
import { useState } from "react";

import type { ProjectReportProjection } from "./report-projection";

export type GeneratedReportViewName =
  | "outcome-readiness"
  | "assumptions-evidence"
  | "decision-record";

const analysisDateFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "2-digit",
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});

function ReportHeader({
  reportName,
  projection,
}: {
  reportName: string;
  projection: ProjectReportProjection;
}) {
  return (
    <header className="generated-report-header">
      <div>
        <h2 className="generated-report-eyebrow">{reportName} · read-only snapshot</h2>
        <h1>{projection.projectTitle}</h1>
        <p>
          Plan as of {analysisDateFormatter.format(new Date(projection.analysisAt))} · current analysis
        </p>
      </div>
    </header>
  );
}

function GeneratedDisclaimer({ onExport }: { onExport: () => void }) {
  return (
    <footer className="generated-report-disclaimer">
      <p>
        A generated snapshot of the read — it runs no new analysis and is read-only. The read firms as you confirm more. The Executive Briefing tab is the one you edit and send.
      </p>
      <div>
        <button onClick={onExport} type="button">
          <DownloadSimple size={14} /> Export this report
        </button>
        <strong>A dated snapshot with the advisory disclaimer.</strong>
      </div>
    </footer>
  );
}

function OutcomeReadiness({
  onExport,
  projection,
}: {
  onExport: () => void;
  projection: ProjectReportProjection;
}) {
  return (
    <>
      <p className="report-view-context">Where the plan stands — a read-only snapshot of the read.</p>
      <article className="generated-report">
        <ReportHeader projection={projection} reportName="Outcome Readiness" />
        <section className="generated-report-lead">
          <div>
            <span>Outcome integrity — how mature OSLO’s read of the plan is</span>
            <strong>{projection.integrity.level}</strong>
            <p>Limited by {projection.integrity.limiting_pillar}.</p>
          </div>
          <p>{projection.summary}</p>
        </section>
        <section aria-label="Integrity pillars" className="generated-report-pillars">
          {projection.integrity.decomposition.map((pillar) => (
            <article key={pillar.key}>
              <span>{pillar.key}</span>
              <strong>{pillar.band}</strong>
              <small>{pillar.basis} grounded</small>
            </article>
          ))}
        </section>
        <section className="generated-report-block">
          <div className="generated-report-block-heading">
            <div>
              <span>Critical grounding</span>
              <h2>
                {projection.criticalGrounding.grounded} of {projection.criticalGrounding.total}{" "}
                critical details grounded
              </h2>
            </div>
            <strong>
              {projection.criticalGrounding.total
                ? Math.round(
                    (projection.criticalGrounding.grounded /
                      projection.criticalGrounding.total) *
                      100,
                  )
                : 100}
              %
            </strong>
          </div>
          <div
            aria-label={`${projection.criticalGrounding.grounded} of ${projection.criticalGrounding.total} critical details grounded`}
            aria-valuemax={Math.max(1, projection.criticalGrounding.total)}
            aria-valuemin={0}
            aria-valuenow={projection.criticalGrounding.grounded}
            className="generated-report-progress"
            role="progressbar"
          >
            <span
              style={{
                width: `${
                  projection.criticalGrounding.total
                    ? (projection.criticalGrounding.grounded /
                        projection.criticalGrounding.total) *
                      100
                    : 100
                }%`,
              }}
            />
          </div>
        </section>
        <section className="generated-report-block">
          <span>Next move</span>
          <h2>{projection.nextMove?.title || "No open action is currently required"}</h2>
          <p>{projection.nextMove?.recommendation || "Keep monitoring the retained plan."}</p>
        </section>
        {projection.openIssues.length ? (
          <section className="generated-report-list" aria-labelledby="readiness-open-issues">
            <div className="generated-report-block-heading">
              <h2 id="readiness-open-issues">Open issues</h2>
              <strong>{projection.openIssues.length}</strong>
            </div>
            {projection.openIssues.map((issue) => (
              <article key={issue.id}>
                <div>
                  <span>{issue.dimension} · {issue.severity}</span>
                  <h3>{issue.title}</h3>
                  <p>{issue.why}</p>
                </div>
                <span>{issue.status}</span>
              </article>
            ))}
          </section>
        ) : null}
        <GeneratedDisclaimer onExport={onExport} />
      </article>
    </>
  );
}

function DepthControl({
  depth,
  setDepth,
}: {
  depth: "summary" | "full";
  setDepth: (depth: "summary" | "full") => void;
}) {
  return (
    <div aria-label="Report depth" className="generated-report-depth" role="group">
      <span>Depth</span>
      <button aria-pressed={depth === "summary"} onClick={() => setDepth("summary")} type="button">
        Summary
      </button>
      <button aria-pressed={depth === "full"} onClick={() => setDepth("full")} type="button">
        Full
      </button>
      <small>{depth === "summary" ? "The decision-useful shortlist" : "The complete retained register"}</small>
    </div>
  );
}

function AssumptionsEvidence({
  onExport,
  projection,
}: {
  onExport: () => void;
  projection: ProjectReportProjection;
}) {
  const [depth, setDepth] = useState<"summary" | "full">("summary");
  const visible = depth === "summary" ? projection.evidenceItems.slice(0, 5) : projection.evidenceItems;
  return (
    <>
      <p className="report-view-context">What the plan rests on — grounded vs OSLO’s inference.</p>
      <DepthControl depth={depth} setDepth={setDepth} />
      <article className="generated-report">
        <ReportHeader projection={projection} reportName="Assumptions & Evidence" />
        <p className="generated-report-intro">
          <strong>{projection.criticalGrounding.grounded}</strong> of {projection.criticalGrounding.total}{" "}
          load-bearing details rest on your evidence; {Math.max(
            0,
            projection.criticalGrounding.total - projection.criticalGrounding.grounded,
          )} remain ungrounded.
        </p>
        <section aria-label="Evidence register" className="generated-report-list is-compact">
          <span className="generated-report-list-label">
            {projection.evidenceRegister.inferred
              ? "Still resting on OSLO’s inference — most load-bearing first"
              : "Grounded on source evidence — most load-bearing first"}
          </span>
          {visible.map((item) => (
            <article key={item.id}>
              <div>
                <span>{item.artifactType} · {item.loadBearing ? "Load-bearing" : "Supporting"}</span>
                <h3>{item.text}</h3>
                {item.issueTitle ? <p>Issue: {item.issueTitle}</p> : null}
              </div>
              <span className={`generated-report-state is-${item.state}`}>{item.state}</span>
            </article>
          ))}
          {!visible.length ? <p>No assumptions are recorded in this analysis.</p> : null}
          {depth === "summary" && projection.evidenceItems.length > visible.length ? (
            <button onClick={() => setDepth("full")} type="button">
              + {projection.evidenceItems.length - visible.length} more in Full
            </button>
          ) : null}
        </section>
        <GeneratedDisclaimer onExport={onExport} />
      </article>
    </>
  );
}

function DecisionRecord({
  onExport,
  projection,
}: {
  onExport: () => void;
  projection: ProjectReportProjection;
}) {
  const [depth, setDepth] = useState<"summary" | "full">("summary");
  const visible = depth === "summary" ? projection.decisions.slice(0, 5) : projection.decisions;
  return (
    <>
      <p className="report-view-context">The calls you’ve made — and what each affirmed.</p>
      {projection.decisions.length > 5 ? <DepthControl depth={depth} setDepth={setDepth} /> : null}
      <article className="generated-report">
        <ReportHeader projection={projection} reportName="Decision Record" />
        <p className="generated-report-intro">
          <strong>{projection.decisions.length}</strong>{" "}
          {projection.decisions.length === 1 ? "decision" : "decisions"} on the record — your judgement, attributed to you.
        </p>
        <section className="generated-report-list" aria-labelledby="confirmed-decisions">
          <div className="generated-report-block-heading">
            <h2 id="confirmed-decisions">Confirmed decisions</h2>
            <strong>{projection.decisions.length}</strong>
          </div>
          {visible.map((decision) => (
            <article key={decision.id}>
              <div>
                <span>{decision.actor} · {analysisDateFormatter.format(new Date(decision.occurredAt))}</span>
                <h3>{decision.title}</h3>
                {decision.detail ? <p>{decision.detail}</p> : null}
              </div>
              <span>confirmed</span>
            </article>
          ))}
          {!visible.length ? <p>No confirmed decisions are recorded in this analysis.</p> : null}
        </section>
        <section className="generated-report-list" aria-labelledby="open-decisions">
          <div className="generated-report-block-heading">
            <h2 id="open-decisions">Open decisions</h2>
            <strong>{projection.openIssues.length}</strong>
          </div>
          {projection.openIssues.map((issue) => (
            <article key={issue.id}>
              <div>
                <span>{issue.dimension} · {issue.severity}</span>
                <h3>{issue.clarification || issue.title}</h3>
                <p>{issue.recommendation}</p>
              </div>
              <span>open</span>
            </article>
          ))}
        </section>
        <GeneratedDisclaimer onExport={onExport} />
      </article>
    </>
  );
}

export function GeneratedReportView({
  projection,
  view,
  onExport,
}: {
  projection: ProjectReportProjection;
  view: GeneratedReportViewName;
  onExport: () => void;
}) {
  if (view === "outcome-readiness") {
    return <OutcomeReadiness onExport={onExport} projection={projection} />;
  }
  if (view === "assumptions-evidence") {
    return <AssumptionsEvidence onExport={onExport} projection={projection} />;
  }
  return <DecisionRecord onExport={onExport} projection={projection} />;
}

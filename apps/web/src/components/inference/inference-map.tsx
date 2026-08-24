"use client";

import {
  ArrowRight,
  Diamond,
  Info,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useMemo } from "react";

import {
  buildProjectProvenance,
  type InferenceAssumption,
} from "@/lib/project-provenance";
import type { OverviewSnapshot } from "@/lib/server/oslo-api";

type Issue = OverviewSnapshot["assessment"]["issues"][number];

function label(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function ageLabel(createdAt: string) {
  const ageMs = Math.max(0, Date.now() - new Date(createdAt).getTime());
  const minutes = Math.floor(ageMs / 60_000);
  if (minutes < 2) return "moments";
  if (minutes < 60) return `${minutes} minutes`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"}`;
  const days = Math.floor(hours / 24);
  return `${days} day${days === 1 ? "" : "s"}`;
}

function visualClaimMarkers(grounded: number, inferred: number) {
  const total = grounded + inferred;
  if (total <= 40) return { grounded, inferred };
  const groundedMarkers = Math.max(
    grounded > 0 ? 1 : 0,
    Math.min(
      grounded > 0 && inferred > 0 ? 39 : 40,
      Math.round((grounded / total) * 40),
    ),
  );
  return { grounded: groundedMarkers, inferred: 40 - groundedMarkers };
}

function AssumptionRow({
  assumption,
  issue,
  onOpenIssue,
}: {
  assumption: InferenceAssumption;
  issue: Issue | undefined;
  onOpenIssue?: (issue: Issue, trigger?: HTMLElement | null) => void;
}) {
  return (
    <article className={assumption.loadBearing ? "is-load-bearing" : ""}>
      <span aria-hidden="true" className="inference-row-marker" />
      <div>
        <strong>{assumption.text}</strong>
        <p>
          Unvalidated for {ageLabel(assumption.createdAt)}
          {issue ? (
            <>
              {" "}· 1 issue depends on it —{" "}
              <button
                onClick={(event) => onOpenIssue?.(issue, event.currentTarget)}
                type="button"
              >
                {issue.title} <ArrowRight aria-hidden="true" size={11} />
              </button>
            </>
          ) : (
            " · nothing depends on it"
          )}
        </p>
      </div>
      <span>{label(assumption.artifactType)}</span>
    </article>
  );
}

export function InferenceMap({
  snapshot,
  onOpenIssue,
}: {
  snapshot: OverviewSnapshot;
  onOpenIssue?: (issue: Issue, trigger?: HTMLElement | null) => void;
}) {
  const provenance = useMemo(() => buildProjectProvenance(snapshot), [snapshot]);
  const flagged = provenance.artifacts.find((artifact) => artifact.verifyFirst);

  return (
    <section className="inference-view">
      <header className="inference-heading">
        <div>
          <h1>Inference map</h1>
          <span>Where OSLO inferred</span>
        </div>
        <p>Your evidence is solid ground. Everything else, OSLO worked out.</p>
      </header>

      {flagged ? (
        <div className="inference-flag" role="status">
          <Info aria-hidden="true" size={16} />
          <p>
            <strong>{label(flagged.artifactType)}</strong> reads strong — but{" "}
            {flagged.inferred} of {flagged.total} items read as inference. Worth
            verifying first.{" "}
            <Link
              href={`/projects/${snapshot.project_id}/artifacts/${flagged.artifactType}`}
            >
              Open {label(flagged.artifactType)} <ArrowRight aria-hidden="true" size={11} />
            </Link>
          </p>
        </div>
      ) : null}

      <section className="inference-card inference-documents">
        <header>
          <div>
            <h2>By artifact</h2>
            <span>One mark per structured claim OSLO extracted</span>
          </div>
          <Info
            aria-label="Solid marks are grounded in project evidence. Outlined marks are inferred by OSLO."
            size={14}
          />
        </header>
        <div className="inference-document-rows">
          {provenance.artifacts
            .filter((artifact) => artifact.total > 0)
            .map((artifact) => {
              const markers = visualClaimMarkers(
                artifact.grounded,
                artifact.inferred,
              );
              return (
                <Link
                className={artifact.verifyFirst ? "is-verify-first" : ""}
                href={`/projects/${snapshot.project_id}/artifacts/${artifact.artifactType}`}
                key={artifact.artifactType}
              >
                <span>{label(artifact.artifactType)}</span>
                <span
                  aria-label={`${artifact.grounded} grounded and ${artifact.inferred} inferred`}
                  className="inference-pips"
                  role="img"
                >
                  {Array.from({ length: markers.grounded }, (_, index) => (
                    <i className="is-grounded" key={`grounded-${index}`} />
                  ))}
                  {Array.from({ length: markers.inferred }, (_, index) => (
                    <i className="is-inferred" key={`inferred-${index}`} />
                  ))}
                </span>
                <span>
                  <strong>{artifact.grounded}</strong> grounded ·{" "}
                  <strong>{artifact.inferred}</strong> inferred
                </span>
                </Link>
              );
            })}
        </div>
        <footer>
          <span><i className="is-grounded" /> Confirmed by evidence</span>
          <span><i className="is-inferred" /> From OSLO</span>
        </footer>
      </section>

      <section className="inference-card inference-assumptions">
        <header>
          <div>
            <h2>Assumptions</h2>
            <span>The ones your read rests on come first</span>
          </div>
          <Info
            aria-label="Load-bearing assumptions are marked at the left edge."
            size={14}
          />
        </header>
        <div>
          {provenance.assumptions.length ? (
            provenance.assumptions.map((assumption) => (
              <AssumptionRow
                assumption={assumption}
                issue={snapshot.assessment.issues.find(
                  (candidate) => candidate.id === assumption.issueId,
                )}
                key={`${assumption.artifactType}:${assumption.id}:${assumption.text}`}
                onOpenIssue={onOpenIssue}
              />
            ))
          ) : (
            <p className="inference-empty">OSLO has not had to assume anything here.</p>
          )}
        </div>
      </section>

      <section className="inference-card inference-structure">
        <header>
          <h2>Structure</h2>
        </header>
        <div>
          <article>
            <strong>{provenance.structure.unconfirmedDependencies}</strong>
            <span>Unconfirmed dependencies</span>
          </article>
          <article>
            <strong>{provenance.structure.unownedParties}</strong>
            <span>Unowned parties</span>
          </article>
          <article>
            <strong>{provenance.structure.untraceableNumbers}</strong>
            <span>Untraceable numbers</span>
          </article>
        </div>
      </section>

      <section className="inference-card inference-week">
        <header>
          <h2>This week</h2>
        </header>
        <div>
          <article>
            <strong>{provenance.thisWeek.userGrounded}</strong>
            <span>you grounded</span>
          </article>
          <article>
            <strong>{provenance.thisWeek.osloInferred}</strong>
            <span>OSLO inferred</span>
          </article>
        </div>
      </section>

      {!provenance.totalClaims ? (
        <div className="inference-empty-state">
          <Diamond aria-hidden="true" size={24} />
          <h2>No extracted claims yet</h2>
          <p>The map will appear after a project analysis publishes.</p>
        </div>
      ) : null}
    </section>
  );
}

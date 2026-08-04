import { osloApiUrl } from "@/lib/server/oslo-api";
import { openSharedIssues, type SharedIssue } from "@/lib/shared-snapshot";

type SharePayload = {
  project_name: string;
  snapshot_state: string;
  published_at: string;
  expires_at: string;
  snapshot_json: {
    summary?: string;
    artifacts?: Array<{ artifact_type: string; title: string; summary: string; reliability: string }>;
    assessment?: {
      confidence_band?: string;
      clarity?: string;
      alignment?: string;
      feasibility?: string;
      issues?: SharedIssue[];
    };
  };
};

export default async function SharedSnapshotPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  const response = await fetch(`${osloApiUrl}/v1/public/share/${encodeURIComponent(token)}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    return (
      <main className="public-collaboration-shell">
        <section className="public-link-error">
          <span>OSLO</span>
          <h1>This snapshot link is unavailable</h1>
          <p>It may have expired or been revoked by the project team.</p>
        </section>
      </main>
    );
  }
  const shared = await response.json() as SharePayload;
  const assessment = shared.snapshot_json.assessment;
  return (
    <main className="public-collaboration-shell">
      <header className="public-collaboration-brand">
        <span>I</span>
        <div><strong>Intralign</strong><small>Read-only project snapshot</small></div>
      </header>
      <section className="public-snapshot">
        <header>
          <div>
            <p className="public-eyebrow">Retained OSLO snapshot</p>
            <h1>{shared.project_name}</h1>
            <p>{shared.snapshot_json.summary}</p>
          </div>
          <span className="public-readonly-badge">Read only · {shared.snapshot_state}</span>
        </header>
        <div className="public-confidence-card">
          <strong>{assessment?.confidence_band ?? "Current read"}</strong>
          <span><b>Outcome confidence</b><small>Evidence-qualified read, not a project score</small></span>
          <dl>
            <div><dt>Clarity</dt><dd>{assessment?.clarity ?? "—"}</dd></div>
            <div><dt>Alignment</dt><dd>{assessment?.alignment ?? "—"}</dd></div>
            <div><dt>Feasibility</dt><dd>{assessment?.feasibility ?? "—"}</dd></div>
          </dl>
        </div>
        <div className="public-snapshot-grid">
          {(shared.snapshot_json.artifacts ?? []).map((artifact) => (
            <article key={artifact.artifact_type}>
              <small>{artifact.reliability} reliability</small>
              <h2>{artifact.title}</h2>
              <p>{artifact.summary}</p>
            </article>
          ))}
        </div>
        <section className="public-snapshot-issues">
          <h2>Open attention items</h2>
          {openSharedIssues(assessment?.issues).map((issue) => (
            <article key={issue.id}>
              <span>{issue.severity}</span>
              <div><strong>{issue.title}</strong><small>{issue.dimension}</small></div>
            </article>
          ))}
        </section>
        <footer>
          <p>Published {new Date(shared.published_at).toLocaleString()}</p>
          <p>Expires {new Date(shared.expires_at).toLocaleDateString()}</p>
          <strong>OSLO advises; you decide.</strong>
        </footer>
      </section>
    </main>
  );
}

import { osloApiUrl } from "@/lib/server/oslo-api";
import { openSharedIssues, type SharedIssue } from "@/lib/shared-snapshot";

type SharePayload = {
  project_name: string;
  recipient_name?: string | null;
  snapshot_state: string;
  published_at: string;
  expires_at: string;
  view_audit_disclosure: string;
  snapshot_json: {
    summary?: string;
    artifacts?: Array<{ artifact_type: string; title: string; summary: string; reliability: string }>;
    assessment?: {
      integrity?: {
        level?: string;
        decomposition?: Array<{ key: string; band: string }>;
      };
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
            {shared.recipient_name ? <small>Shared with {shared.recipient_name}</small> : null}
          </div>
          <span className="public-readonly-badge">Read only · {shared.snapshot_state}</span>
        </header>
        <div className="public-confidence-card">
          <strong>{assessment?.integrity?.level ?? "Current read"}</strong>
          <span><b>Outcome integrity</b><small>Evidence-qualified read, not a project score</small></span>
          <dl>
            {(assessment?.integrity?.decomposition ?? []).map((pillar) => (
              <div key={pillar.key}><dt>{pillar.key}</dt><dd>{pillar.band}</dd></div>
            ))}
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
          <p>{shared.view_audit_disclosure}</p>
          <strong>OSLO advises; you decide.</strong>
        </footer>
      </section>
    </main>
  );
}

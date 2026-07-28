import { ReviewerResponseForm } from "@/components/collaboration/reviewer-response-form";
import { osloApiUrl } from "@/lib/server/oslo-api";

type ReviewPayload = {
  reviewer_name: string;
  project_name: string;
  issue_id?: string | null;
  expires_at: string;
  response_kind?: string | null;
  snapshot_json: {
    summary?: string;
    assessment?: {
      confidence_index?: number;
      confidence_band?: string;
      issues?: Array<{
        id: string;
        title: string;
        severity: string;
        why: string;
        recommendation: string;
      }>;
    };
  };
};

const reviewDateFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "2-digit",
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});

export default async function ReviewPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  const response = await fetch(`${osloApiUrl}/v1/public/review/${encodeURIComponent(token)}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    return (
      <main className="public-collaboration-shell">
        <section className="public-link-error">
          <span>OSLO</span>
          <h1>This review link is unavailable</h1>
          <p>It may have expired, been revoked, been completed, or the linked issue was resolved.</p>
        </section>
      </main>
    );
  }

  const review = await response.json() as ReviewPayload;
  const issues = review.snapshot_json.assessment?.issues ?? [];
  const issue = issues.find((candidate) => candidate.id === review.issue_id) ?? issues[0];

  return (
    <main className="public-collaboration-shell">
      <header className="public-collaboration-brand">
        <span>I</span>
        <div><strong>Intralign</strong><small>Governed OSLO review</small></div>
      </header>
      <div className="public-review-layout">
        <section className="public-review-context">
          <p className="public-eyebrow">External project review</p>
          <h1>{review.project_name}</h1>
          <p>
            {review.reviewer_name}, you have been invited to provide one traceable response
            without joining the workspace.
          </p>
          <div
            aria-label={`Outcome confidence ${
              review.snapshot_json.assessment?.confidence_index ?? "not available"
            } out of 100`}
            className="public-confidence-card"
          >
            <span className="public-confidence-score">
              <strong>{review.snapshot_json.assessment?.confidence_index ?? "—"}</strong>
              <small>/100</small>
            </span>
            <span>
              <small>Outcome confidence</small>
              <b>{review.snapshot_json.assessment?.confidence_band ?? "Current read"}</b>
              <small>Retained snapshot at the time this review was requested</small>
            </span>
          </div>
          {issue ? (
            <article className="public-review-issue">
              <header><span>{issue.severity}</span><small>Issue selected for review</small></header>
              <h2>{issue.title}</h2>
              <h3>Why this matters</h3>
              <p>{issue.why}</p>
              <h3>OSLO recommended</h3>
              <p>{issue.recommendation}</p>
            </article>
          ) : (
            <article className="public-review-issue">
              <h2>Review the retained project read</h2>
              <p>{review.snapshot_json.summary}</p>
            </article>
          )}
          <small className="public-expiry">
            Secure link expires {reviewDateFormatter.format(new Date(review.expires_at))}.
          </small>
        </section>
        <aside className="public-review-response">
          <p className="public-eyebrow">Your attestation</p>
          <h2>Respond to this project read</h2>
          {review.response_kind ? (
            <div className="review-response-success">
              <p>This link has already received a response.</p>
            </div>
          ) : <ReviewerResponseForm token={token} />}
        </aside>
      </div>
    </main>
  );
}

import { ReviewerResponseForm } from "@/components/collaboration/reviewer-response-form";
import { osloApiUrl } from "@/lib/server/oslo-api";

type ReviewPayload = {
  id: string;
  reviewer_name: string;
  project_name: string;
  expires_at: string;
  question: string;
  source: {
    reference: string;
    excerpt: string;
  };
  response_kind?: string | null;
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
          <article className="public-review-issue">
            <header><span>Scoped</span><small>One question · one cited source</small></header>
            <h2>{review.question}</h2>
            <h3>Cited source</h3>
            <p>{review.source.excerpt}</p>
            <small>{review.source.reference}</small>
          </article>
          <p className="public-review-scope-note">
            This link cannot open the project, its artifacts, other issues, members, or history.
          </p>
          <small className="public-expiry">
            Secure link expires {reviewDateFormatter.format(new Date(review.expires_at))}.
          </small>
        </section>
        <aside className="public-review-response">
          <p className="public-eyebrow">Your attestation</p>
          <h2>Respond to this question</h2>
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

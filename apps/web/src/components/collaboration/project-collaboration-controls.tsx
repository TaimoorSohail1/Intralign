"use client";

import {
  ArrowSquareOut,
  Check,
  Copy,
  DownloadSimple,
  FilePdf,
  LinkSimple,
  ShareNetwork,
  ShieldCheck,
  UserPlus,
  UsersThree,
  X,
} from "@phosphor-icons/react";
import { useCallback, useMemo, useState, type ReactNode } from "react";

type CollaborationMode = "share" | "export" | null;
type WorkspaceRole = "collaborator" | "viewer";

interface Participant {
  id: string;
  display_name: string;
  email?: string | null;
  role: "owner" | WorkspaceRole;
}

interface Invitation {
  id: string;
  email: string;
  role: WorkspaceRole;
  status: string;
  expires_at: string;
}

interface ShareLink {
  id: string;
  url?: string;
  expires_at: string;
  revoked_at?: string | null;
}

interface ReviewGrant {
  id: string;
  reviewer_name: string;
  reviewer_email?: string | null;
  url?: string;
  expires_at: string;
  revoked_at?: string | null;
  responded_at?: string | null;
  response_id?: string | null;
  response_kind?: string | null;
  response_body?: string | null;
  analysis_run_id?: string | null;
}

interface CollaborationState {
  actor_role: "owner" | WorkspaceRole;
  plan: {
    name: string;
    collaborator_seats: number;
    collaborator_seats_used: number;
    monthly_invites: number;
    monthly_invites_used?: number;
    viewers_unlimited: boolean;
    reviewers_unmetered: boolean;
  };
  participants: Participant[];
  invitations?: Invitation[];
  share_links?: ShareLink[];
  reviews?: ReviewGrant[];
}

interface CreatedAccess {
  kind: "snapshot" | "review";
  url: string;
  expires_at: string;
}

function readableDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date);
}

function initials(name: string) {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}

export function ProjectCollaborationControls({ projectId }: { projectId: string }) {
  const [mode, setMode] = useState<CollaborationMode>(null);
  const [state, setState] = useState<CollaborationState | null>(null);
  const [loading, setLoading] = useState(false);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState<WorkspaceRole>("collaborator");
  const [reviewerName, setReviewerName] = useState("");
  const [reviewerEmail, setReviewerEmail] = useState("");
  const [created, setCreated] = useState<CreatedAccess | null>(null);
  const [copied, setCopied] = useState(false);

  const loadCollaboration = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`/api/projects/${projectId}/collaboration`, {
        cache: "no-store",
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.message ?? "Collaboration could not be loaded.");
      }
      setState(payload as CollaborationState);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Collaboration could not be loaded.");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  function resetTransientState() {
    setCreated(null);
    setCopied(false);
    setError("");
    setSuccess("");
  }

  function openShare() {
    resetTransientState();
    setState(null);
    setMode("share");
    void loadCollaboration();
  }

  function openExport() {
    resetTransientState();
    setMode("export");
  }

  function closeModal() {
    setMode(null);
    resetTransientState();
  }

  const pendingInvitations = useMemo(
    () => (state?.invitations ?? []).filter((item) => item.status === "pending"),
    [state],
  );
  const activeShares = useMemo(
    () => (state?.share_links ?? []).filter((item) => !item.revoked_at),
    [state],
  );
  const activeReviews = useMemo(
    () => (state?.reviews ?? []).filter((item) => !item.revoked_at && !item.responded_at),
    [state],
  );
  const reviewerResponses = useMemo(
    () => (state?.reviews ?? []).filter((item) => item.responded_at && item.response_id),
    [state],
  );

  async function runAction(body: Record<string, unknown>) {
    setError("");
    setSuccess("");
    const response = await fetch(`/api/projects/${projectId}/collaboration`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = response.status === 204 ? null : await response.json().catch(() => ({}));
    if (!response.ok) {
      setError(payload?.message ?? "The collaboration action could not be completed.");
      return undefined;
    }
    return payload;
  }

  async function createSnapshot() {
    setBusy("snapshot");
    const payload = await runAction({
      action: "share",
      reviewerName: "",
      reviewerEmail: null,
    });
    if (payload?.url) {
      setCreated({ kind: "snapshot", url: payload.url, expires_at: payload.expires_at });
      setSuccess("A read-only snapshot is ready to share.");
      await loadCollaboration();
    }
    setBusy("");
  }

  async function createReview() {
    if (!reviewerName.trim()) {
      setError("Add the reviewer’s name first.");
      return;
    }
    setBusy("review");
    const payload = await runAction({
      action: "review",
      reviewerName: reviewerName.trim(),
      reviewerEmail: reviewerEmail.trim() || null,
    });
    if (payload?.url) {
      setCreated({ kind: "review", url: payload.url, expires_at: payload.expires_at });
      setSuccess("The external review link is ready.");
      setReviewerName("");
      setReviewerEmail("");
      await loadCollaboration();
    }
    setBusy("");
  }

  async function promoteReviewEvidence(review: ReviewGrant) {
    if (!review.response_id || review.analysis_run_id) return;
    setBusy(`response-${review.response_id}`);
    const payload = await runAction({
      action: "use_review_evidence",
      responseId: review.response_id,
    });
    if (payload?.analysis_run_id) {
      setSuccess("Reviewer evidence queued for analysis.");
      await loadCollaboration();
    }
    setBusy("");
  }

  async function sendInvite() {
    if (!inviteEmail.trim()) {
      setError("Add a valid email address first.");
      return;
    }
    setBusy("invite");
    const payload = await runAction({
      action: "invite",
      email: inviteEmail.trim(),
      role: inviteRole,
    });
    if (payload) {
      setSuccess(`Invitation sent to ${inviteEmail.trim()}.`);
      setInviteEmail("");
      await loadCollaboration();
    }
    setBusy("");
  }

  async function revoke(body: Record<string, unknown>, key: string, message: string) {
    setBusy(key);
    const result = await runAction(body);
    if (result !== undefined) {
      setSuccess(message);
      await loadCollaboration();
    }
    setBusy("");
  }

  async function copyCreated() {
    if (!created) return;
    await navigator.clipboard.writeText(created.url);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div
      aria-label="Project sharing and export"
      className="project-collaboration-actions"
      role="group"
    >
      <button
        aria-label="Share"
        className="topbar-action"
        type="button"
        onClick={openShare}
      >
        <ShareNetwork size={16} weight="bold" aria-hidden="true" />
        <span>Share</span>
      </button>
      <button
        aria-label="Export"
        className="topbar-action"
        type="button"
        onClick={openExport}
      >
        <DownloadSimple size={16} weight="bold" aria-hidden="true" />
        <span>Export</span>
      </button>

      {mode ? (
        <div className="collaboration-modal-backdrop" role="presentation">
          <section
            aria-label={mode === "share" ? "Share project" : "Export project"}
            aria-modal="true"
            className="collaboration-modal"
            role="dialog"
          >
            <button
              aria-label="Close"
              className="collaboration-modal-dismiss"
              type="button"
              onClick={closeModal}
            >
              <X size={18} aria-hidden="true" />
            </button>
            <header className="collaboration-modal-header">
              <div>
                <span className="eyebrow">
                  {mode === "share" ? "PROJECT ACCESS" : "READ-ONLY EXPORT"}
                </span>
                <h2>{mode === "share" ? "Share this project" : "Project snapshot · PDF"}</h2>
                <p>
                  {mode === "share"
                    ? "Invite workspace members, create a governed review, or share a read-only snapshot."
                    : "Download the current evidence-qualified read. Exporting never runs analysis."}
                </p>
              </div>
            </header>

            {mode === "export" ? (
              <div className="collaboration-export">
                <div className="collaboration-export-icon" aria-hidden="true">
                  <FilePdf size={30} weight="duotone" />
                </div>
                <div>
                  <h3>Current project read</h3>
                  <p>
                    Includes the seven artifacts, confidence read, findings, evidence references,
                    currency marker, and OSLO advisory disclaimer.
                  </p>
                </div>
                <a
                  className="collaboration-primary-button"
                  href={`/api/projects/${projectId}/export`}
                >
                  <DownloadSimple size={16} weight="bold" aria-hidden="true" />
                  Download PDF
                </a>
              </div>
            ) : null}

            {mode === "share" ? (
              <div className="collaboration-share-body">
                {loading ? (
                  <div className="collaboration-loading" role="status">
                    Loading governed project access…
                  </div>
                ) : null}
                {error ? (
                  <div className="collaboration-error" role="alert">
                    <span>{error}</span>
                    {!state ? (
                      <button type="button" onClick={() => void loadCollaboration()}>
                        Retry
                      </button>
                    ) : null}
                  </div>
                ) : null}
                {success ? (
                  <p className="collaboration-success" role="status">
                    <Check size={15} weight="bold" aria-hidden="true" />
                    {success}
                  </p>
                ) : null}

                {state ? (
                  <>
                    <Heading
                      icon={<UsersThree size={18} weight="duotone" />}
                      title="People with workspace access"
                      detail={`${state.plan.collaborator_seats_used}/${state.plan.collaborator_seats} seats`}
                    />
                    <div className="collaboration-participants">
                      {state.participants.map((participant) => (
                        <div className="collaboration-participant" key={participant.id}>
                          <span className="collaboration-avatar">
                            {initials(participant.display_name) || "OS"}
                          </span>
                          <span>
                            <strong>{participant.display_name}</strong>
                            <small>{participant.email ?? participant.role}</small>
                          </span>
                          <span className="collaboration-role">{participant.role}</span>
                        </div>
                      ))}
                    </div>

                    {state.actor_role === "owner" ? (
                      <div className="collaboration-invite-card">
                        <Heading
                          icon={<UserPlus size={18} weight="duotone" />}
                          title="Invite to workspace"
                          detail={`${state.plan.monthly_invites_used ?? 0}/${state.plan.monthly_invites} this month`}
                        />
                        <div className="collaboration-invite-fields">
                          <label>
                            Email address
                            <input
                              type="email"
                              value={inviteEmail}
                              placeholder="teammate@company.com"
                              onChange={(event) => setInviteEmail(event.target.value)}
                            />
                          </label>
                          <label>
                            Role
                            <select
                              value={inviteRole}
                              onChange={(event) =>
                                setInviteRole(event.target.value as WorkspaceRole)
                              }
                            >
                              <option value="collaborator">Collaborator</option>
                              <option value="viewer">Viewer</option>
                            </select>
                          </label>
                          <button
                            className="collaboration-secondary-button"
                            type="button"
                            disabled={busy === "invite"}
                            onClick={() => void sendInvite()}
                          >
                            <UserPlus size={16} weight="bold" aria-hidden="true" />
                            {busy === "invite" ? "Sending…" : "Send invitation"}
                          </button>
                        </div>
                        <p className="collaboration-fine-print">
                          Viewers are unlimited. Collaborators use a plan seat. Invitations expire
                          after 14 days.
                        </p>
                      </div>
                    ) : null}

                    <div className="collaboration-share-grid">
                      <article className="collaboration-share-card">
                        <span className="collaboration-card-icon" aria-hidden="true">
                          <LinkSimple size={21} weight="duotone" />
                        </span>
                        <div>
                          <h3>Read-only snapshot</h3>
                          <p>
                            Share the current result without granting workspace access. The link
                            expires after 30 days and never starts analysis.
                          </p>
                        </div>
                        <button
                          className="collaboration-primary-button"
                          type="button"
                          disabled={busy === "snapshot"}
                          onClick={() => void createSnapshot()}
                        >
                          <LinkSimple size={16} weight="bold" aria-hidden="true" />
                          {busy === "snapshot" ? "Creating…" : "Create snapshot link"}
                        </button>
                      </article>

                      <article className="collaboration-share-card collaboration-review-card">
                        <span className="collaboration-card-icon" aria-hidden="true">
                          <ShieldCheck size={21} weight="duotone" />
                        </span>
                        <div>
                          <h3>External review</h3>
                          <p>
                            Ask a named reviewer to comment, approve, reject, or suggest an
                            alternative. Reviewers do not use a workspace seat.
                          </p>
                        </div>
                        <label>
                          Reviewer name
                          <input
                            value={reviewerName}
                            placeholder="Amina Khan"
                            onChange={(event) => setReviewerName(event.target.value)}
                          />
                        </label>
                        <label>
                          Reviewer email <small>optional</small>
                          <input
                            type="email"
                            value={reviewerEmail}
                            placeholder="amina@company.com"
                            onChange={(event) => setReviewerEmail(event.target.value)}
                          />
                        </label>
                        <button
                          className="collaboration-secondary-button"
                          type="button"
                          disabled={busy === "review"}
                          onClick={() => void createReview()}
                        >
                          <ShieldCheck size={16} weight="bold" aria-hidden="true" />
                          {busy === "review" ? "Creating…" : "Create review link"}
                        </button>
                      </article>
                    </div>

                    {created ? (
                      <div className="collaboration-created-link" role="status">
                        <div>
                          <strong>
                            {created.kind === "review"
                              ? "External review link"
                              : "Read-only snapshot link"}
                          </strong>
                          <span>Expires {readableDate(created.expires_at)}</span>
                        </div>
                        <code>{created.url}</code>
                        <div className="collaboration-created-actions">
                          <button type="button" onClick={() => void copyCreated()}>
                            {copied ? (
                              <Check size={15} weight="bold" aria-hidden="true" />
                            ) : (
                              <Copy size={15} weight="bold" aria-hidden="true" />
                            )}
                            {copied ? "Copied" : "Copy link"}
                          </button>
                          <a href={created.url} target="_blank" rel="noreferrer">
                            <ArrowSquareOut size={15} weight="bold" aria-hidden="true" />
                            Open
                          </a>
                        </div>
                      </div>
                    ) : null}

                    {pendingInvitations.length || activeShares.length || activeReviews.length ? (
                      <section className="collaboration-access-records">
                        <Heading
                          icon={<ShieldCheck size={18} weight="duotone" />}
                          title="Active access"
                          detail={`${pendingInvitations.length + activeShares.length + activeReviews.length} records`}
                        />
                        <div className="collaboration-record-list">
                          {pendingInvitations.map((invitation) => (
                            <AccessRecord
                              key={invitation.id}
                              title={invitation.email}
                              detail={`${invitation.role} invitation · expires ${readableDate(
                                invitation.expires_at,
                              )}`}
                              actionLabel={
                                busy === `invitation-${invitation.id}` ? "Revoking…" : "Revoke"
                              }
                              onAction={() =>
                                void revoke(
                                  { action: "revoke_invitation", invitationId: invitation.id },
                                  `invitation-${invitation.id}`,
                                  "The invitation was revoked.",
                                )
                              }
                            />
                          ))}
                          {activeShares.map((share) => (
                            <AccessRecord
                              key={share.id}
                              title="Read-only snapshot"
                              detail={`Expires ${readableDate(share.expires_at)}`}
                              actionLabel={busy === `share-${share.id}` ? "Revoking…" : "Revoke"}
                              onAction={() =>
                                void revoke(
                                  { action: "revoke_share", linkId: share.id },
                                  `share-${share.id}`,
                                  "The snapshot link was revoked.",
                                )
                              }
                            />
                          ))}
                          {activeReviews.map((review) => (
                            <AccessRecord
                              key={review.id}
                              title={review.reviewer_name}
                              detail={`External review · expires ${readableDate(
                                review.expires_at,
                              )}`}
                              actionLabel={busy === `review-${review.id}` ? "Revoking…" : "Revoke"}
                              onAction={() =>
                                void revoke(
                                  { action: "revoke_review", grantId: review.id },
                                  `review-${review.id}`,
                                  "The external review was revoked.",
                                )
                              }
                            />
                          ))}
                        </div>
                      </section>
                    ) : null}
                    {reviewerResponses.length ? (
                      <section className="collaboration-access-records">
                        <Heading
                          icon={<Check size={18} weight="duotone" />}
                          title="Reviewer responses"
                          detail={`${reviewerResponses.length} received`}
                        />
                        <div className="collaboration-record-list">
                          {reviewerResponses.map((review) => (
                            <AccessRecord
                              key={review.response_id}
                              title={`${review.reviewer_name} · ${(
                                review.response_kind ?? "comment"
                              ).replaceAll("_", " ")}`}
                              detail={review.response_body ?? "Reviewer response received."}
                              actionLabel={
                                review.analysis_run_id
                                  ? "Evidence added"
                                  : busy === `response-${review.response_id}`
                                    ? "Queuing…"
                                    : "Use as project evidence"
                              }
                              onAction={
                                review.analysis_run_id
                                  ? undefined
                                  : () => void promoteReviewEvidence(review)
                              }
                            />
                          ))}
                        </div>
                      </section>
                    ) : null}
                  </>
                ) : null}
              </div>
            ) : null}
          </section>
        </div>
      ) : null}
    </div>
  );
}

function Heading({
  icon,
  title,
  detail,
}: {
  icon: ReactNode;
  title: string;
  detail: string;
}) {
  return (
    <div className="collaboration-section-heading">
      <span aria-hidden="true">{icon}</span>
      <div>
        <h3>{title}</h3>
        <small>{detail}</small>
      </div>
    </div>
  );
}

function AccessRecord({
  title,
  detail,
  actionLabel,
  onAction,
}: {
  title: string;
  detail: string;
  actionLabel: string;
  onAction?: () => void;
}) {
  return (
    <div className="collaboration-access-record">
      <span>
        <strong>{title}</strong>
        <small>{detail}</small>
      </span>
      <button type="button" disabled={!onAction} onClick={onAction}>
        {actionLabel}
      </button>
    </div>
  );
}

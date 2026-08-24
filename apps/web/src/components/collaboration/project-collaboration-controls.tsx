"use client";

import {
  ArrowSquareOut,
  Check,
  Copy,
  DownloadSimple,
  FilePdf,
  LinkSimple,
  ShieldCheck,
  UserPlus,
  X,
} from "@phosphor-icons/react";
import { useCallback, useMemo, useState, type ReactNode } from "react";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

type CollaborationMode = "share" | "export" | null;
type ExportAudience = "sponsor" | "programme" | "operations" | "executive";

interface Participant {
  id: string;
  display_name: string;
  email?: string | null;
  role: "owner";
}

interface Invitation {
  id: string;
  email: string;
  role: "owner";
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
  actor_role: "owner";
  plan: {
    name: string;
    collaborator_seats: number;
    collaborator_seats_used: number;
    monthly_invites: number;
    monthly_invites_used?: number;
    viewers_unlimited: boolean;
    reviewers_unmetered: boolean;
    export_formats?: string[];
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

const audienceLabels: Record<ExportAudience, string> = {
  sponsor: "Sponsor",
  programme: "Programme lead",
  operations: "Operations",
  executive: "Executive / board",
};

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

function humanize(value?: string | null) {
  if (!value) return "Unknown";
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function issueDimensionSummary(snapshot: OverviewSnapshot | null) {
  const dimensions = Array.from(
    new Set(snapshot?.assessment?.issues?.map((issue) => humanize(issue.dimension)) ?? []),
  );
  return dimensions.length ? dimensions.join(" · ") : "Clarity · Alignment · Feasibility";
}

function readoutSections(snapshot: OverviewSnapshot | null, audience: ExportAudience) {
  const issues = snapshot?.assessment?.issues ?? [];
  const openIssues = issues.filter((issue) => issue.status !== "resolved");
  const limiting = humanize(snapshot?.assessment?.limiting_dimension);
  const top = openIssues[0];
  const questions = openIssues
    .filter((issue) => issue.clarification)
    .slice(0, 3)
    .map((issue) => issue.clarification as string);
  const confirmations = openIssues.slice(0, 5).map((issue) => issue.recommendation);
  const ask: Record<ExportAudience, string> = {
    sponsor: "Confirm the key decisions, ownership, and evidence needed to release the plan.",
    programme: "Assign owners and close the cross-workstream dependencies that limit the current read.",
    operations: "Confirm the operational capacity, controls, and delivery assumptions that remain open.",
    executive: "Confirm the decisions, funding, and risk appetite needed for the plan to move forward.",
  };

  return [
    {
      number: "§1",
      title: "The read",
      body:
        snapshot?.summary
        ?? "OSLO is packaging the latest published understanding of this project.",
    },
    {
      number: "§2",
      title: "What’s limiting it",
      body: `${limiting} is the limiting dimension (${openIssues.length} open issue${openIssues.length === 1 ? "" : "s"}).${top ? ` The sharpest issue is ${top.title}.` : ""}`,
    },
    {
      number: "§3",
      title: "What we don’t know yet",
      items: questions.length ? questions : ["No open clarification questions are recorded in the current read."],
    },
    {
      number: "§4",
      title: `What I need from ${audienceLabels[audience]}`,
      body: ask[audience],
      addressed: true,
    },
    {
      number: "§5",
      title: "What I’d need to be sure",
      items: confirmations.length
        ? confirmations
        : ["No further confirmation is requested in the current published read."],
    },
  ];
}

export function ProjectCollaborationControls({
  projectId,
  projectName = "this project",
}: {
  projectId: string;
  projectName?: string;
}) {
  const [mode, setMode] = useState<CollaborationMode>(null);
  const [state, setState] = useState<CollaborationState | null>(null);
  const [overview, setOverview] = useState<OverviewSnapshot | null>(null);
  const [loading, setLoading] = useState(false);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [reviewerName, setReviewerName] = useState("");
  const [reviewerEmail, setReviewerEmail] = useState("");
  const [created, setCreated] = useState<CreatedAccess | null>(null);
  const [copied, setCopied] = useState(false);
  const [audience, setAudience] = useState<ExportAudience>("sponsor");

  const loadCollaboration = useCallback(async () => {
    const response = await fetch(`/api/projects/${projectId}/collaboration`, {
      cache: "no-store",
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.message ?? "Collaboration could not be loaded.");
    setState(payload as CollaborationState);
    return payload as CollaborationState;
  }, [projectId]);

  const loadModalData = useCallback(async (includeOverview: boolean) => {
    setLoading(true);
    setError("");
    try {
      const tasks: Array<Promise<unknown>> = [loadCollaboration()];
      if (includeOverview) {
        tasks.push(
          fetch(`/api/projects/${projectId}/overview`, { cache: "no-store" })
            .then(async (response) => {
              const payload = await response.json().catch(() => ({}));
              if (!response.ok) throw new Error(payload.message ?? "The current read could not be loaded.");
              setOverview(payload as OverviewSnapshot);
            }),
        );
      }
      await Promise.all(tasks);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "The current project state could not be loaded.");
    } finally {
      setLoading(false);
    }
  }, [loadCollaboration, projectId]);

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
    void loadModalData(false);
  }

  function openExport() {
    resetTransientState();
    setState(null);
    setOverview(null);
    setAudience("sponsor");
    setMode("export");
    void loadModalData(true);
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
    const payload = await runAction({ action: "share", reviewerName: "", reviewerEmail: null });
    if (payload?.url) {
      setCreated({ kind: "snapshot", url: payload.url, expires_at: payload.expires_at });
      setSuccess("A view-only snapshot is ready to share.");
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
    const payload = await runAction({ action: "use_review_evidence", responseId: review.response_id });
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
    const payload = await runAction({ action: "invite", email: inviteEmail.trim() });
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

  async function copySummary() {
    const text = readoutSections(overview, audience)
      .map((section) => `${section.number} ${section.title}\n${section.body ?? section.items?.join("\n")}`)
      .join("\n\n");
    await navigator.clipboard.writeText(text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  const inviteLimit = state?.plan.monthly_invites ?? 0;
  const inviteUsed = state?.plan.monthly_invites_used ?? 0;
  const inviteRemaining = Math.max(inviteLimit - inviteUsed, 0);
  const isBasic = state?.plan.name.toLowerCase() === "basic";
  const sections = readoutSections(overview, audience);

  return (
    <div aria-label="Project sharing and export" className="project-collaboration-actions" role="group">
      <button aria-label="Share" className="topbar-action" type="button" onClick={openShare}>
        <UserPlus size={16} weight="bold" aria-hidden="true" />
        <span>Share</span>
      </button>
      <button aria-label="Export" className="topbar-action" type="button" onClick={openExport}>
        <DownloadSimple size={16} weight="bold" aria-hidden="true" />
        <span>Export</span>
      </button>

      {mode ? (
        <div className="collaboration-modal-backdrop" role="presentation" onMouseDown={(event) => {
          if (event.target === event.currentTarget) closeModal();
        }}>
          <section
            aria-labelledby="collaboration-modal-title"
            aria-modal="true"
            className={`collaboration-modal is-${mode}`}
            role="dialog"
          >
            <header className="collaboration-modal-header">
              <div>
                <h2 id="collaboration-modal-title">
                  {mode === "share" ? `Share ${projectName}` : "Export a snapshot"}
                </h2>
                <p>
                  {mode === "share"
                    ? "Invite people, or hand out a view-only snapshot of where understanding stands."
                    : "Where understanding stands, as it stands now."}
                </p>
              </div>
              <button aria-label="Close" className="collaboration-modal-dismiss" type="button" onClick={closeModal}>
                <X size={18} aria-hidden="true" />
              </button>
            </header>

            <div className="collaboration-modal-body">
              {loading ? <div className="collaboration-loading" role="status">Loading the current project state…</div> : null}
              {error ? (
                <div className="collaboration-error" role="alert">
                  <span>{error}</span>
                  {!state ? <button type="button" onClick={() => void loadModalData(mode === "export")}>Retry</button> : null}
                </div>
              ) : null}
              {success ? <p className="collaboration-success" role="status"><Check size={15} weight="bold" />{success}</p> : null}

              {mode === "export" && !loading ? (
                <ExportComposer
                  audience={audience}
                  copied={copied}
                  isBasic={isBasic}
                  overview={overview}
                  projectId={projectId}
                  sections={sections}
                  setAudience={setAudience}
                  onCopySummary={() => void copySummary()}
                />
              ) : null}

              {mode === "share" && state ? (
                <div className="prototype-share-body">
                  <div className="collaboration-limit-box is-phase">
                    <span>Phase limit — invites (supply)</span>
                    <p><strong>{inviteRemaining} of {inviteLimit} left</strong> this month on {state.plan.name}. Resets monthly and does not accumulate.</p>
                  </div>
                  <div className="collaboration-limit-box is-tier">
                    <span>Tier limit — workspace owner seats</span>
                    <p><strong>{state.plan.collaborator_seats} owner seats</strong> on {state.plan.name}, including you. {state.plan.collaborator_seats_used} of {state.plan.collaborator_seats} filled.</p>
                  </div>
                  <div className="collaboration-review-free">
                    <strong>Asking for a read is free — no invite, no seat.</strong>
                    <span>Review requests</span>
                  </div>

                  {state.actor_role === "owner" ? (
                    <section className="prototype-share-section">
                      <p className="collaboration-label">Invite by email</p>
                      <div className="prototype-invite-row">
                        <label>
                          <span className="sr-only">Email address</span>
                          <input aria-label="Email address" type="email" value={inviteEmail} placeholder="name@company.com" onChange={(event) => setInviteEmail(event.target.value)} />
                        </label>
                        <button className="collaboration-primary-button" disabled={busy === "invite"} type="button" onClick={() => void sendInvite()}>{busy === "invite" ? "Sending…" : "Invite"}</button>
                      </div>
                      <p className="collaboration-fine-print">The invitation is sent by email and expires after 14 days.</p>
                    </section>
                  ) : null}

                  <section className="prototype-share-section">
                    <p className="collaboration-label">Workspace role</p>
                    <div className="prototype-role-table">
                      <RoleRow label="Owner" seat detail="Every workspace member can change the plan, share it, and export it." />
                    </div>
                  </section>

                  <section className="prototype-share-section">
                    <p className="collaboration-label">People on this project</p>
                    <div className="prototype-people-list">
                      {state.participants.map((participant) => (
                        <div className="prototype-person" key={participant.id}>
                          <span className="collaboration-avatar">{initials(participant.display_name) || "OS"}</span>
                          <span><strong>{participant.display_name}</strong><small>{participant.email ?? participant.role}</small></span>
                          <span className="seat-badge">seat</span>
                          <span className="collaboration-role">Owner</span>
                        </div>
                      ))}
                    </div>
                  </section>

                  <section className="prototype-share-section">
                    <p className="collaboration-label">Share link — a view-only snapshot of this project</p>
                    <div className="prototype-share-link-card">
                      {activeShares.length ? (
                        <>
                          <p><strong>{activeShares.length} active snapshot link{activeShares.length === 1 ? "" : "s"}.</strong> It stays frozen at the analysis used when it was created.</p>
                          {activeShares.map((share) => (
                            <AccessRecord
                              key={share.id}
                              title={`Snapshot · expires ${readableDate(share.expires_at)}`}
                              detail="View-only and revocable"
                              actionLabel={busy === `share-${share.id}` ? "Revoking…" : "Revoke"}
                              onAction={() => void revoke({ action: "revoke_share", linkId: share.id }, `share-${share.id}`, "The snapshot link was revoked.")}
                            />
                          ))}
                        </>
                      ) : (
                        <><p>No link yet. A snapshot link is view-only.</p><button className="collaboration-primary-button" type="button" disabled={busy === "snapshot"} onClick={() => void createSnapshot()}>{busy === "snapshot" ? "Creating…" : "Create a view-only link"}</button></>
                      )}
                    </div>
                    <p className="collaboration-fine-print">A share link shows OSLO’s read as it stood when the link was made. If the project moves on, recipients are told they are viewing a previous analysis.</p>
                    <div className="collaboration-rule-box"><strong>A share link is not an export link.</strong> Share links give revocable, view-only access. Export creates a frozen copy of one snapshot.</div>
                  </section>

                  <section className="prototype-share-section prototype-review-request">
                    <Heading icon={<ShieldCheck size={18} weight="duotone" />} title="External review request" detail="Free — no workspace seat" />
                    <div className="prototype-review-fields">
                      <label>Reviewer name<input value={reviewerName} placeholder="Amina Khan" onChange={(event) => setReviewerName(event.target.value)} /></label>
                      <label>Reviewer email <small>optional</small><input type="email" value={reviewerEmail} placeholder="amina@company.com" onChange={(event) => setReviewerEmail(event.target.value)} /></label>
                      <button className="collaboration-secondary-button" disabled={busy === "review"} type="button" onClick={() => void createReview()}>{busy === "review" ? "Creating…" : "Create review link"}</button>
                    </div>
                  </section>

                  {created ? (
                    <div className="collaboration-created-link" role="status">
                      <div><strong>{created.kind === "review" ? "External review link" : "View-only snapshot link"}</strong><span>Expires {readableDate(created.expires_at)}</span></div>
                      <code>{created.url}</code>
                      <div className="collaboration-created-actions">
                        <button type="button" onClick={() => void copyCreated()}>{copied ? <Check size={15} weight="bold" /> : <Copy size={15} weight="bold" />}{copied ? "Copied" : "Copy link"}</button>
                        <a href={created.url} target="_blank" rel="noreferrer"><ArrowSquareOut size={15} weight="bold" />Open</a>
                      </div>
                    </div>
                  ) : null}

                  {pendingInvitations.length || activeReviews.length ? (
                    <section className="prototype-share-section collaboration-access-records">
                      <p className="collaboration-label">Active access</p>
                      {pendingInvitations.map((invitation) => <AccessRecord key={invitation.id} title={invitation.email} detail={`Pending owner invite · expires ${readableDate(invitation.expires_at)}`} actionLabel={busy === `invite-${invitation.id}` ? "Revoking…" : "Revoke"} onAction={() => void revoke({ action: "revoke_invitation", invitationId: invitation.id }, `invite-${invitation.id}`, "The invitation was revoked.")} />)}
                      {activeReviews.map((review) => <AccessRecord key={review.id} title={review.reviewer_name} detail={`External review · expires ${readableDate(review.expires_at)}`} actionLabel={busy === `review-${review.id}` ? "Revoking…" : "Revoke"} onAction={() => void revoke({ action: "revoke_review", grantId: review.id }, `review-${review.id}`, "The external review was revoked.")} />)}
                    </section>
                  ) : null}

                  {reviewerResponses.length ? (
                    <section className="prototype-share-section collaboration-access-records">
                      <p className="collaboration-label">Reviewer responses</p>
                      {reviewerResponses.map((review) => <AccessRecord key={review.response_id} title={`${review.reviewer_name} · ${humanize(review.response_kind)}`} detail={review.response_body ?? "Reviewer response received."} actionLabel={review.analysis_run_id ? "Evidence added" : busy === `response-${review.response_id}` ? "Queuing…" : "Use as project evidence"} onAction={review.analysis_run_id ? undefined : () => void promoteReviewEvidence(review)} />)}
                    </section>
                  ) : null}
                </div>
              ) : null}
            </div>

            <footer className="collaboration-modal-footer">
              <span>{mode === "share" ? "Sharing changes no assessment. Only an analysis update does." : "Export runs no analysis."}</span>
              <button type="button" onClick={closeModal}>{mode === "share" ? "Done" : "Cancel"}</button>
            </footer>
          </section>
        </div>
      ) : null}
    </div>
  );
}

function ExportComposer({
  audience,
  copied,
  isBasic,
  overview,
  projectId,
  sections,
  setAudience,
  onCopySummary,
}: {
  audience: ExportAudience;
  copied: boolean;
  isBasic: boolean;
  overview: OverviewSnapshot | null;
  projectId: string;
  sections: ReturnType<typeof readoutSections>;
  setAudience: (audience: ExportAudience) => void;
  onCopySummary: () => void;
}) {
  const openIssues = overview?.assessment?.issues?.filter((issue) => issue.status !== "resolved").length ?? 0;
  return (
    <div className="prototype-export-body">
      <p className="collaboration-label">What you’re exporting</p>
      <div className="prototype-export-current">
        <strong>Outcome Confidence {humanize(overview?.assessment?.confidence_band)}</strong> · {humanize(overview?.assessment?.reliability).toLowerCase()} reliability<br />
        <strong>{overview?.extended_analysis ? "Extended analysis run" : "Current analysis run"}</strong> · {overview?.state ?? "current"} · Current<br />
        {openIssues} open issue{openIssues === 1 ? "" : "s"} · {issueDimensionSummary(overview)}
      </div>
      <div className="prototype-export-disclaimer">This reflects OSLO’s <strong>understanding maturity</strong> — how clear, aligned and feasible the plan reads, and how reliable that read is. It is <strong>not</strong> a measure of project health, readiness, or probability of success.</div>

      <p className="collaboration-label">Strategic readout — the five-section read</p>
      <div className="prototype-export-draftbar">Assembled from what OSLO already understands — one honest read, many asks. Generating a snapshot runs no analysis.</div>
      <div className="prototype-export-binding"><Check size={16} weight="bold" /> <span>The read (§1–§3 and §5) is <strong>identical for every audience</strong>. Only <strong>§4 — what I need from you</strong> changes for the recipient.</span></div>
      <div className="prototype-audience-picker"><span>Address the ask to</span>{(Object.keys(audienceLabels) as ExportAudience[]).map((key) => <button className={audience === key ? "is-selected" : ""} key={key} type="button" onClick={() => setAudience(key)}>{audienceLabels[key]}</button>)}</div>
      <div className="prototype-readout-document">
        {sections.map((section) => <section className={section.addressed ? "is-addressed" : ""} key={section.number}><h3><span>{section.number}</span>{section.title}</h3>{section.body ? <p>{section.body}</p> : null}{section.items ? <ul>{section.items.map((item) => <li key={item}>{item}</li>)}</ul> : null}{section.addressed ? <small>Addressed to the recipient — the read above stays unchanged.</small> : null}</section>)}
      </div>
      <div className="prototype-export-options"><span>Optional sections <i>Basic</i></span>{["Alignment", "Unvalidated assumptions", "How understanding matured", "Document detail"].map((label) => <label key={label}><input type="checkbox" disabled={!isBasic} />{label}</label>)}</div>
      <p className="collaboration-fine-print"><strong>Free</strong> exports the five-section snapshot as a PDF. <strong>Basic</strong> adds optional sections, branding, and scheduling. The read itself is never gated.</p>
      <p className="collaboration-label">Format</p>
      <div className="prototype-export-formats">
        <a href={`/api/projects/${projectId}/export`}><FilePdf size={19} /><span><strong>PDF</strong><small>A written snapshot you can send on.</small></span></a>
        <button type="button" disabled={!isBasic} onClick={onCopySummary}><Copy size={19} /><span><strong>{copied ? "Copied" : "Copy summary"}</strong><small>The read as text, on your clipboard.</small></span>{!isBasic ? <i>Basic</i> : null}</button>
        <button type="button" disabled><LinkSimple size={19} /><span><strong>Export link</strong><small>A hosted frozen copy of this snapshot.</small></span><i>{isBasic ? "Coming soon" : "Basic"}</i></button>
      </div>
      {!isBasic ? <div className="collaboration-tier-note"><strong>Tier limit — export formats</strong> Free exports as PDF. Copy summary and export links come with Basic.</div> : null}
    </div>
  );
}

function RoleRow({ label, detail, seat = false }: { label: string; detail: string; seat?: boolean }) {
  return <div><strong>{label}</strong><span className={seat ? "seat-badge" : "seat-badge no-seat"}>{seat ? "takes a seat" : "no seat"}</span><p>{detail}</p></div>;
}

function Heading({ icon, title, detail }: { icon: ReactNode; title: string; detail: string }) {
  return <div className="collaboration-section-heading"><span aria-hidden="true">{icon}</span><div><h3>{title}</h3><small>{detail}</small></div></div>;
}

function AccessRecord({ title, detail, actionLabel, onAction }: { title: string; detail: string; actionLabel: string; onAction?: () => void }) {
  return <div className="collaboration-access-record"><span><strong>{title}</strong><small>{detail}</small></span><button type="button" disabled={!onAction} onClick={onAction}>{actionLabel}</button></div>;
}

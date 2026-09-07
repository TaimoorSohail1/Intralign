"use client";

import {
  ArrowRight,
  Check,
  Diamond,
  Sparkle,
  Target,
  X,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useState } from "react";

import type { YourOutcomeProjection } from "./your-outcome-projection";

const stateLabels = {
  inferred: "Needs evidence",
  routed: "Awaiting evidence",
  addressed: "Analysis pending",
  grounded: "Grounded",
} as const;

type OutcomeIssue = YourOutcomeProjection["needs_you"][number];

function issueSeverity(issue: OutcomeIssue) {
  return issue.severity ?? stateLabels[issue.state];
}

function issueSeverityClass(issue: OutcomeIssue) {
  return (issue.severity ?? issue.state).toLowerCase().replaceAll(" ", "-");
}

function OutcomeIssueRow({ issue }: { issue: OutcomeIssue }) {
  return (
    <Link
      className={`your-outcome-issue-row severity-${issueSeverityClass(issue)}`}
      href={issue.href}
    >
      <span>{issueSeverity(issue)}</span>
      <strong>{issue.title}</strong>
      <small>{issue.detail}</small>
      <em>Decide in the read →</em>
    </Link>
  );
}

export function YourOutcomeDashboard({
  data,
  onDismissWorkspaceNotice,
  onTakeTour,
  workspaceNoticeOpen = false,
}: {
  data: YourOutcomeProjection;
  onDismissWorkspaceNotice?: () => void;
  onTakeTour?: () => void;
  workspaceNoticeOpen?: boolean;
}) {
  const [needsExpanded, setNeedsExpanded] = useState(false);
  const criticalIssues = data.needs_you.filter(
    (issue) => issue.severity?.toLowerCase() === "critical",
  );
  const leadIssues = criticalIssues.length ? criticalIssues : data.needs_you.slice(0, 2);
  const leadIssueIds = new Set(leadIssues.map((issue) => issue.issue_id));
  const lowerStakeIssues = data.needs_you.filter((issue) => !leadIssueIds.has(issue.issue_id));
  const primary = data.primary_outcome;
  const intentHref = `/projects/${data.project_id}/artifacts/intent`;

  return (
    <div className="your-outcome-dashboard">
      {workspaceNoticeOpen ? (
        <section aria-label="Workspace open" className="r2-workspace-open">
          <span aria-hidden="true"><Sparkle size={20} weight="fill" /></span>
          <div>
            <strong>Your workspace is open.</strong>
            <p>
              Your guided review is complete. <b>Now in focus:</b> your plan documents on the
              left and <b>OSLO&apos;s reasoning</b> on the right — every pillar and open issue with them.
            </p>
            <div>
              <small>New to OSLO?</small>
              <button onClick={onTakeTour} type="button">Take a 30-second tour →</button>
              <button onClick={onDismissWorkspaceNotice} type="button">No thanks</button>
            </div>
          </div>
          <button
            aria-label="Dismiss workspace open message"
            onClick={onDismissWorkspaceNotice}
            type="button"
          >
            <X aria-hidden="true" size={14} />
          </button>
        </section>
      ) : null}

      <header className="your-outcome-heading">
        <h1>Your Outcome</h1>
        <p>at a glance — where it stands, and what needs you</p>
      </header>

      <section aria-label="Current outcome" className="your-outcome-card">
        {primary ? (
          <>
            <div className="your-outcome-card-main">
              <span aria-hidden="true" className="your-outcome-icon"><Target size={15} weight="fill" /></span>
              <div>
                <small>Your Outcome · {data.project_title}</small>
                <p>
                  <b>Primary</b>
                  <strong>{primary.title}</strong>
                  <em>{primary.provenance === "declared" ? <><Check size={10} /> yours</> : "OSLO inference"}</em>
                </p>
              </div>
              <Link href={`${intentHref}?focus=primary-outcome&return=outcome`}>Manage in Intent</Link>
            </div>

            {data.visible_secondary_outcomes.length ? (
              <div className="your-outcome-secondary-list">
                {data.visible_secondary_outcomes.map((outcome) => (
                  <span key={outcome.id}><Diamond size={10} /> {outcome.title}</span>
                ))}
              </div>
            ) : null}

            {data.held_outcome_count ? (
              <div className="your-outcome-held">
                <span aria-hidden="true">◐</span>
                <p>
                  <strong>
                    OSLO also read {data.held_outcome_count} more outcome{data.held_outcome_count === 1 ? "" : "s"} in your brief while analyzing it — held until you&apos;re settled in.
                  </strong>{" "}
                  Nothing&apos;s lost; OSLO will offer {data.held_outcome_count === 1 ? "it" : "them"} to review once you&apos;re grounded a few things.
                </p>
                <Link href={`${intentHref}?review=held-outcomes&return=outcome`}>
                  Review {data.held_outcome_count === 1 ? "it" : "them"} now →
                </Link>
              </div>
            ) : null}

            <p className="your-outcome-definition">
              The definition of success this read is measured against — a target, not a forecast.
              Its goals, success criteria and KPIs live in Intent ({data.intent_counts.goals} goals · {data.intent_counts.success_criteria} success criteria · {data.intent_counts.kpis} KPIs).
            </p>
          </>
        ) : (
          <div className="your-outcome-empty">
            <Target aria-hidden="true" size={22} />
            <div>
              <strong>No outcome is defined yet.</strong>
              <p>Define the outcome OSLO should measure the plan against in Intent.</p>
            </div>
            <Link href={`${intentHref}?focus=primary-outcome&return=outcome`}>Define in Intent →</Link>
          </div>
        )}
      </section>

      <div className="your-outcome-declare">
        <Link href={`${intentHref}?new=outcome&return=outcome`}>
          + Declare an outcome <span>Free</span>
        </Link>
      </div>

      {data.unseen_changes.length ? (
        <section aria-label="Since you last looked" className="your-outcome-changes">
          <header><span>↪ Since you last looked</span><Link aria-label="Full history" href={`/projects/${data.project_id}/history?focus=since-last-looked`}>Full history →</Link></header>
          <div>
            {data.trend !== "unchanged" ? <span className="is-trend">↑ integrity {data.trend}</span> : null}
            {data.unseen_changes.slice(0, 3).map((change) => (
              <Link href={change.href} key={change.id}><Check size={11} /> {change.summary}</Link>
            ))}
          </div>
        </section>
      ) : null}

      <section aria-label="Outcome Integrity" className="your-outcome-integrity">
        <div className="your-outcome-integrity-summary">
          <small>Outcome Integrity</small>
          <strong>{data.integrity.level}</strong>
          <span>{data.trend === "unchanged" ? "No movement this session" : `↑ ${data.trend} this session`}</span>
          <em>maturity, not a forecast</em>
        </div>
        <div className="your-outcome-pillars">
          {data.integrity.decomposition.map((pillar) => (
            <Link
              className={pillar.key === data.integrity.limiting_pillar ? "is-limiting" : ""}
              href={`/projects/${data.project_id}/issues?pillar=${pillar.key.toLowerCase()}`}
              key={pillar.key}
            >
              <small>{pillar.key}</small>
              <strong>{pillar.band}</strong>
              {pillar.key === data.integrity.limiting_pillar ? <span>Gating →</span> : null}
            </Link>
          ))}
          <div className="your-outcome-grounding-progress">
            <span aria-label={`${data.grounding.grounded} of ${data.grounding.total} load-bearing details grounded`} role="img">
              <i style={{ width: `${data.grounding.total ? (data.grounding.grounded / data.grounding.total) * 100 : 0}%` }} />
            </span>
            <b>{data.grounding.grounded} of {data.grounding.total} details grounded</b>
            <small>{data.integrity.limiting_pillar} gates it — lift it and the whole read moves</small>
          </div>
        </div>
      </section>

      <section aria-label="Needs you" className="your-outcome-needs">
        <header><h2>Needs you <span>{data.needs_you.length}</span></h2><p>— decisions to make</p></header>
        {leadIssues.length ? (
          <div className="your-outcome-issue-list">
            {leadIssues.map((issue) => <OutcomeIssueRow issue={issue} key={issue.issue_id} />)}
          </div>
        ) : (
          <p className="your-outcome-settled"><Check size={14} /> No open decision currently needs you.</p>
        )}
        {lowerStakeIssues.length ? (
          <div className="your-outcome-lower-stakes">
            <div hidden={!needsExpanded} id="your-outcome-lower-stake-calls">
              {lowerStakeIssues.map((issue) => (
                <OutcomeIssueRow issue={issue} key={issue.issue_id} />
              ))}
            </div>
            <button
              aria-controls="your-outcome-lower-stake-calls"
              aria-expanded={needsExpanded}
              aria-label={needsExpanded ? "Show fewer" : `Show ${lowerStakeIssues.length} more, lower stakes — these can wait`}
              onClick={() => setNeedsExpanded((open) => !open)}
              type="button"
            >
              {needsExpanded ? "▾ Show fewer" : `▸ ${lowerStakeIssues.length} more, lower stakes — these can wait`}
            </button>
          </div>
        ) : null}
      </section>

      <section aria-label="In motion" className="your-outcome-motion">
        <header><h2>In motion <Check size={13} /></h2><p>— delegated, grounding with your team</p></header>
        {data.in_motion.length ? (
          <div className="your-outcome-motion-list">
            {data.in_motion.map((item) => {
              const answered = item.state === "answered";
              const firstName = item.reviewer_name.split(" ")[0] || item.reviewer_name;
              return (
                <Link href={item.href} key={`${item.issue_id}-${item.reviewer_name}`}>
                  <span className={answered ? "is-done" : "is-pending"}>
                    {answered ? <Check aria-hidden="true" size={12} /> : <ArrowRight aria-hidden="true" size={12} />}
                  </span>
                  <strong>
                    {item.issue_title} — {answered ? "grounded by" : "asked"} <b>{item.reviewer_name}</b>
                  </strong>
                  <small>{answered ? "grounded · attributed" : `awaiting ${firstName}`}</small>
                </Link>
              );
            })}
          </div>
        ) : (
          <p>Nothing delegated yet — every grounded detail rests on your own evidence. Route a detail to whoever holds it and it appears here.</p>
        )}
      </section>

      <p className="your-outcome-readonly">
        Your at-a-glance view — read-only. Every row opens into the read, where the call is made and recorded; this view never acts on its own.
      </p>
    </div>
  );
}

"use client";

import {
  ArrowRight,
  CaretDown,
  CaretRight,
  ClockCounterClockwise,
  FileText,
  Info,
  Sparkle,
  UsersThree,
  X,
} from "@phosphor-icons/react";
import { useEffect, useMemo, useRef, useState } from "react";

import type {
  HistoryCategory,
  HistoryEvent,
  HistoryGroup,
  OverviewSnapshot,
  ProjectHistory,
} from "@/lib/server/oslo-api";

type HistoryFilter = "all" | HistoryCategory;

const filters: Array<{ label: string; value: HistoryFilter }> = [
  { label: "All", value: "all" },
  { label: "Analysis", value: "analysis" },
  { label: "Issues", value: "issues" },
  { label: "Versions", value: "versions" },
  { label: "Your decisions", value: "decisions" },
  { label: "Collaboration & invites", value: "collaboration" },
];

function runTitle(group: HistoryGroup) {
  if (group.status === "failed") {
    return `${group.kind === "initial" ? "Initial" : "Extended"} Analysis stopped`;
  }
  return `${group.kind === "initial" ? "Initial" : "Extended"} Analysis complete`;
}

function relativeDate(value: string) {
  const date = new Date(value);
  const now = new Date();
  if (date.toDateString() === now.toDateString()) return "Today";
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: date.getFullYear() === now.getFullYear() ? undefined : "numeric",
  }).format(date);
}

function eventIcon(event: HistoryEvent) {
  if (event.category === "versions") return <FileText aria-hidden="true" size={15} />;
  if (event.category === "decisions") return <Sparkle aria-hidden="true" size={15} />;
  if (event.category === "collaboration") {
    return <UsersThree aria-hidden="true" size={15} />;
  }
  return <ClockCounterClockwise aria-hidden="true" size={15} />;
}

export function HistoryWorkspace({
  history,
  onAskOslo,
  projectId,
}: {
  history: ProjectHistory;
  onAskOslo: (runId: string, prompt: string) => void;
  projectId: string;
}) {
  const [filter, setFilter] = useState<HistoryFilter>("all");
  const [groups, setGroups] = useState(history.groups);
  const [nextCursor, setNextCursor] = useState(history.next_cursor);
  const [expandedRuns, setExpandedRuns] = useState<Set<string>>(
    () =>
      new Set(
        history.groups
          .filter((group) => group.current)
          .map((group) => group.run_id),
      ),
  );
  const [snapshot, setSnapshot] = useState<OverviewSnapshot | null>(null);
  const [snapshotPending, setSnapshotPending] = useState(false);
  const [snapshotError, setSnapshotError] = useState<string | null>(null);
  const [loadPending, setLoadPending] = useState(false);

  const visibleGroups = useMemo(
    () =>
      groups
        .map((group) => ({
          ...group,
          events:
            filter === "all"
              ? group.events
              : group.events.filter((event) => event.category === filter),
        }))
        .filter((group) => filter === "all" || group.events.length > 0),
    [filter, groups],
  );

  const openSnapshot = async (runId: string) => {
    setSnapshotPending(true);
    setSnapshotError(null);
    try {
      const response = await fetch(
        `/api/projects/${projectId}/history/runs/${runId}`,
      );
      if (!response.ok) throw new Error("snapshot unavailable");
      setSnapshot((await response.json()) as OverviewSnapshot);
    } catch {
      setSnapshotError("This retained snapshot could not be opened.");
    } finally {
      setSnapshotPending(false);
    }
  };

  const loadMore = async () => {
    if (!nextCursor || loadPending) return;
    setLoadPending(true);
    try {
      const query = new URLSearchParams({
        category: "all",
        cursor: nextCursor,
      });
      const response = await fetch(`/api/projects/${projectId}/history?${query}`);
      if (!response.ok) throw new Error("history unavailable");
      const page = (await response.json()) as ProjectHistory;
      setGroups((current) => [...current, ...page.groups]);
      setNextCursor(page.next_cursor);
    } finally {
      setLoadPending(false);
    }
  };

  const toggleRun = (runId: string) => {
    setExpandedRuns((current) => {
      const next = new Set(current);
      if (next.has(runId)) next.delete(runId);
      else next.add(runId);
      return next;
    });
  };

  return (
    <section className="history-workspace">
      <header className="history-heading">
        <div>
          <h1>History &amp; timeline</h1>
          <p>
            append-only · prior states retained
            <Info aria-label="History is read-only" size={14} />
          </p>
        </div>
        {groups[0] ? (
          <button
            className="history-ask"
            onClick={() =>
              onAskOslo(
                groups[0].run_id,
                `Explain the ${runTitle(groups[0])} historical read and what changed.`,
              )
            }
            type="button"
          >
            <Sparkle aria-hidden="true" size={13} weight="fill" />
            Ask OSLO
          </button>
        ) : null}
      </header>

      <HistoryTrend history={history} />

      <div aria-label="History filters" className="history-filters" role="group">
        <span>Show</span>
        {filters.map((item) => (
          <button
            aria-pressed={filter === item.value}
            className={filter === item.value ? "is-active" : ""}
            key={item.value}
            onClick={() => setFilter(item.value)}
            type="button"
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className="history-collaboration-note">
        <UsersThree aria-hidden="true" size={17} />
        <p>
          <strong>Collaboration is retained here.</strong>
          Comments, review invitations, shared snapshots, exports, and reviewer
          decisions appear in this read-only timeline.
        </p>
      </div>

      <div className="history-runs">
        {visibleGroups.map((group) => {
          const expanded = expandedRuns.has(group.run_id);
          return (
            <article className="history-run" key={group.run_id}>
              <header>
                <button
                  aria-expanded={expanded}
                  aria-label={`${expanded ? "Collapse" : "Expand"} ${runTitle(group)}`}
                  className="history-run-toggle"
                  onClick={() => toggleRun(group.run_id)}
                  type="button"
                >
                  {expanded ? (
                    <CaretDown aria-hidden="true" size={13} />
                  ) : (
                    <CaretRight aria-hidden="true" size={13} />
                  )}
                  <span className={`history-run-icon history-run-${group.status}`}>
                    <ClockCounterClockwise aria-hidden="true" size={15} />
                  </span>
                  <span>
                    <strong>{runTitle(group)}</strong>
                    <small>
                      Analysis run · {relativeDate(group.occurred_at)}
                      {group.confidence_band ? ` · ${group.confidence_band} confidence` : ""}
                    </small>
                  </span>
                </button>
                <div className="history-run-actions">
                  <button
                    aria-label={`Ask OSLO about ${runTitle(group)}`}
                    onClick={() =>
                      onAskOslo(
                        group.run_id,
                        `Explain the ${runTitle(group)} historical read and what changed.`,
                      )
                    }
                    type="button"
                  >
                    <Sparkle aria-hidden="true" size={12} weight="fill" />
                    Ask OSLO
                  </button>
                  <span className={group.current ? "is-current" : ""}>
                    {group.current ? "Current" : "History"}
                  </span>
                </div>
              </header>

              {expanded ? (
                <div className="history-run-body">
                  <div className="history-changes">
                    <span>What changed</span>
                    {group.changes.map((change) => (
                      <em className={`tone-${change.tone}`} key={change.label}>
                        {change.label}
                      </em>
                    ))}
                  </div>
                  <div className="history-events">
                    {group.events.map((event) => (
                      <div className="history-event" key={event.id}>
                        <span>{eventIcon(event)}</span>
                        <div>
                          <strong>{event.summary}</strong>
                          {event.detail ? <p>{event.detail}</p> : null}
                          <small>{event.actor_type === "user" ? "Your decision" : "OSLO record"}</small>
                        </div>
                        {event.category === "versions" ? (
                          <button
                            aria-label={`View snapshot for ${runTitle(group)}`}
                            disabled={snapshotPending}
                            onClick={() => void openSnapshot(group.run_id)}
                            type="button"
                          >
                            View snapshot <ArrowRight aria-hidden="true" size={11} />
                          </button>
                        ) : null}
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}
            </article>
          );
        })}
        {!visibleGroups.length ? (
          <div className="history-empty">
            <ClockCounterClockwise aria-hidden="true" size={22} />
            <strong>No history in this view</strong>
            <p>Choose another filter to see retained project events.</p>
          </div>
        ) : null}
      </div>

      {nextCursor ? (
        <button
          className="history-load"
          disabled={loadPending}
          onClick={() => void loadMore()}
          type="button"
        >
          {loadPending ? "Loading…" : "Load earlier history"}
        </button>
      ) : null}

      {snapshotError ? <p className="history-error" role="alert">{snapshotError}</p> : null}
      <p className="history-readonly">
        <Info aria-hidden="true" size={14} />
        Read-only · viewing history changes nothing
      </p>

      {snapshot ? (
        <HistoricalSnapshot
          onClose={() => setSnapshot(null)}
          snapshot={snapshot}
        />
      ) : null}
    </section>
  );
}

function HistoryTrend({ history }: { history: ProjectHistory }) {
  const points = history.trend;
  if (!points.length) return null;
  return (
    <section className="history-trend" aria-label="Understanding over runs">
      <div>
        <strong>Understanding over runs</strong>
        <span>rises or falls with the read</span>
      </div>
      <div className="history-trend-line" aria-hidden="true">
        {points.map((point, index) => (
          <i
            className={point.current ? "is-current" : ""}
            key={point.run_id}
            style={{
              left: `${points.length === 1 ? 50 : (index / (points.length - 1)) * 100}%`,
              bottom: `${Math.max(8, Math.min(82, point.confidence_index))}%`,
            }}
          />
        ))}
      </div>
      <div className="history-trend-labels">
        {points.map((point, index) => (
          <div key={point.run_id}>
            <span>{index === 0 ? "Initial" : index === points.length - 1 ? "Current" : `Run ${index + 1}`}</span>
            <strong>{point.confidence_band}</strong>
            <small>{point.cause}</small>
          </div>
        ))}
      </div>
    </section>
  );
}

function HistoricalSnapshot({
  onClose,
  snapshot,
}: {
  onClose: () => void;
  snapshot: OverviewSnapshot;
}) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const previouslyFocused = document.activeElement as HTMLElement | null;
    closeButtonRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      previouslyFocused?.focus();
    };
  }, [onClose]);

  return (
    <div
      className="history-modal-backdrop"
      onMouseDown={(event) => {
        if (event.currentTarget === event.target) onClose();
      }}
    >
      <section
        aria-label="Historical snapshot"
        aria-modal="true"
        className="history-snapshot"
        role="dialog"
      >
        <header>
          <div>
            <span>Read-only retained state</span>
            <h2>Historical snapshot</h2>
            <p>{new Date(snapshot.published_at).toLocaleString()}</p>
          </div>
          <button
            aria-label="Close historical snapshot"
            autoFocus
            onClick={onClose}
            ref={closeButtonRef}
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        <div className="history-snapshot-score">
          <strong>{snapshot.assessment.confidence_index}</strong>
          <span>/100 · {snapshot.assessment.confidence_band} confidence</span>
        </div>
        <p className="history-snapshot-summary">{snapshot.summary}</p>
        <div className="history-snapshot-artifacts">
          {snapshot.artifacts.map((artifact) => (
            <article key={artifact.artifact_type}>
              <span>{artifact.title}</span>
              <p>{artifact.summary}</p>
              <small>{artifact.reliability} reliability</small>
            </article>
          ))}
        </div>
        <footer>
          This snapshot is evidence of a prior read. It cannot be edited or restored.
        </footer>
      </section>
    </div>
  );
}

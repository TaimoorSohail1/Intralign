"use client";

import {
  ArrowRight,
  ClockCounterClockwise,
  FileText,
  Info,
  Sparkle,
  UsersThree,
  X,
} from "@phosphor-icons/react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import type {
  HistoryEvent,
  HistoryGroup,
  OverviewSnapshot,
  ProjectHistory,
} from "@/lib/server/oslo-api";

type HistoryFilter = "all" | "analysis" | "decisions" | "issues";

const filters: Array<{ label: string; value: HistoryFilter }> = [
  { label: "All", value: "all" },
  { label: "Analysis", value: "analysis" },
  { label: "Your decisions", value: "decisions" },
  { label: "Issues", value: "issues" },
];

function displayCategory(event: HistoryEvent): Exclude<HistoryFilter, "all"> {
  if (event.category === "issues") return "issues";
  if (event.category === "decisions" || event.category === "collaboration") {
    return "decisions";
  }
  return "analysis";
}

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
  analysisRunId,
  history,
  projectId,
}: {
  analysisRunId?: string;
  history: ProjectHistory;
  onAskOslo?: (runId: string, prompt: string) => void;
  projectId: string;
}) {
  const [filter, setFilter] = useState<HistoryFilter>("all");
  const [groups, setGroups] = useState(history.groups);
  const [trend, setTrend] = useState(history.trend);
  const [nextCursor, setNextCursor] = useState(history.next_cursor);
  const [snapshot, setSnapshot] = useState<OverviewSnapshot | null>(null);
  const [snapshotPending, setSnapshotPending] = useState(false);
  const [snapshotError, setSnapshotError] = useState<string | null>(null);
  const [loadPending, setLoadPending] = useState(false);
  const closeSnapshot = useCallback(() => setSnapshot(null), []);

  useEffect(() => {
    let active = true;

    const refreshHistory = async () => {
      try {
        const response = await fetch(
          `/api/projects/${projectId}/history?category=all`,
          { cache: "no-store" },
        );
        if (!response.ok) return;
        const latest = (await response.json()) as ProjectHistory;
        if (!active || !Array.isArray(latest.groups)) return;
        setGroups(latest.groups);
        setTrend(Array.isArray(latest.trend) ? latest.trend : []);
        setNextCursor(latest.next_cursor);
      } catch {
        // The server-rendered history remains the safe last-good view.
      }
    };

    void refreshHistory();
    return () => {
      active = false;
    };
  }, [analysisRunId, projectId]);

  const visibleEvents = useMemo(() => {
    const entries = groups.flatMap((group) => {
      const title = runTitle(group);
      const hasRunEvent = group.events.some((event) => event.summary === title);
      const runEvent: HistoryEvent = {
        id: 0,
        category: "analysis",
        event_type: `analysis.${group.kind}_${group.status}`,
        summary: title,
        detail:
          group.status === "completed"
            ? group.current
              ? "The current read supersedes the prior state."
              : "A prior read was retained without replacing the current one."
            : "The last-good read remains current and can be retried.",
        actor_type: "oslo",
        artifact_type: null,
        artifact_version: null,
        issue_id: null,
        occurred_at: group.occurred_at,
      };
      return (hasRunEvent ? group.events : [runEvent, ...group.events]).map((event) => ({
        event,
        runId: group.run_id,
      }));
    });
    return filter === "all"
      ? entries
      : entries.filter(({ event }) => displayCategory(event) === filter);
  }, [filter, groups]);

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

  return (
    <section className="history-workspace">
      <header className="history-heading">
        <div>
          <h1>History</h1>
          <p>append-only — how the read moved</p>
        </div>
      </header>

      <HistoryTrend points={trend} />

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
      <div className="history-runs">
        {visibleEvents.map(({ event, runId }, index) => {
          const category = displayCategory(event);
          return (
            <article className="history-card" key={`${runId}-${event.id}-${index}`}>
              <header>
                <span className={`history-category is-${category}`}>
                  {category === "decisions"
                    ? "Your decisions"
                    : category === "analysis"
                      ? "Analysis"
                      : "Issues"}
                </span>
                <time dateTime={event.occurred_at}>{relativeDate(event.occurred_at)}</time>
              </header>
              <div>
                <span className="history-card-icon">{eventIcon(event)}</span>
                <div>
                  <strong>{event.summary}</strong>
                  {event.detail ? <p>{event.detail}</p> : null}
                </div>
                {event.category === "versions" ? (
                  <button
                    aria-label={`View snapshot for ${event.summary}`}
                    disabled={snapshotPending}
                    onClick={() => void openSnapshot(runId)}
                    type="button"
                  >
                    View snapshot <ArrowRight aria-hidden="true" size={11} />
                  </button>
                ) : null}
              </div>
            </article>
          );
        })}
        {!visibleEvents.length ? (
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
          onClose={closeSnapshot}
          snapshot={snapshot}
        />
      ) : null}
    </section>
  );
}

function HistoryTrend({ points }: { points: ProjectHistory["trend"] }) {
  if (!points.length) {
    return (
      <section className="history-trend" aria-label="Your read over this session">
        <div className="history-session-heading">
          <strong>Your read over this session</strong>
        </div>
        <div className="history-session-legend">
          <span>Grounded <b>0 of 0 load-bearing</b></span>
          <strong>— steady this session</strong>
        </div>
      </section>
    );
  }
  const first = points[0];
  const current = points.find((point) => point.current) ?? points.at(-1) ?? first;
  const percentage = (grounded: number, total: number) => total > 0 ? (grounded / total) * 100 : 0;
  const sessionScale = Math.max(
    1,
    ...points.map((point) =>
      Math.max(point.grounded_load_bearing, point.total_load_bearing),
    ),
  );
  const start = Math.max(3, Math.min(97, percentage(first.grounded_load_bearing, sessionScale)));
  const now = Math.max(3, Math.min(97, percentage(current.grounded_load_bearing, sessionScale)));
  const groundedDelta = current.grounded_load_bearing - first.grounded_load_bearing;
  const direction = groundedDelta > 0
    ? "rising"
    : groundedDelta < 0
      ? "eased"
      : "steady this session";
  return (
    <section className="history-trend" aria-label="Your read over this session">
      <div className="history-session-heading">
        <strong>Your read over this session</strong>
        <span>it rises or falls only when something real is confirmed — never on a guess</span>
      </div>
      <div className="history-session-track" aria-hidden="true">
        <span>Start</span>
        <div>
          <i style={{ left: `${start}%` }} />
          <i className="is-current" style={{ left: `${now}%` }} />
        </div>
        <span>Now</span>
      </div>
      <div className="history-session-legend">
        <span>Grounded <b>{current.grounded_load_bearing} of {current.total_load_bearing} load-bearing</b></span>
        <strong className={direction === "rising" ? "is-rising" : ""}>
          {direction === "rising" ? "▲" : direction === "eased" ? "▼" : "—"} {direction}
        </strong>
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
  const publishedAt = snapshot.published_at
    ? new Date(snapshot.published_at)
    : null;
  const publishedLabel =
    publishedAt && !Number.isNaN(publishedAt.getTime())
      ? publishedAt.toLocaleString()
      : "Publication time unavailable";

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
            <p>{publishedLabel}</p>
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
          <strong>{snapshot.assessment.integrity.level}</strong>
          <span>Outcome Integrity · retained read</span>
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

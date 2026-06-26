/**
 * DTM-0026 — Notification / Awareness (IC-WE-DISCLOSE E1).
 *
 * A Companion-Surface-class lightweight awareness layer/inbox
 * (NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1 §D). It PRESENTS awareness
 * and ROUTES to source context; it computes nothing, generates nothing, governs
 * nothing, and changes no assessment. It surfaces:
 *
 *   - **New emissions / activity** as `Notification`s (the DTM-0018
 *     `useListNotifications…` read) — finding/recommendation/analysis-run/comment/
 *     shared-artifact pointers that route to their source context.
 *   - **Acceptance-Impact** alerts (the DTM-0018 `useListAcceptanceImpact…` read,
 *     project-scoped) — "a decision you confirmed is affected": a **Derived** drift
 *     (≥10pts or a band change vs the version-pinned acceptance, CONTEXT.md). Each
 *     carries its `DerivedEnvelope` → `EpistemicLabel` (banded, conflict-aware),
 *     never shown settled and NEVER auto-resolved.
 *
 * ── THE CRITICAL BOUNDARY (the spine of this slice) ──────────────────────────────
 * Read/unread/dismiss is **platform state (Category E), NON-canonical** (spec §J;
 * CONTEXT.md). Marking a notification read or dismissing it:
 *   - writes NO canonical, changes NO assessment, promotes nothing;
 *   - does NOT resolve the underlying drift / Acceptance-Impact;
 *   - does NOT mutate the underlying governed `Notification` object.
 *
 * THE DISMISS-STATE FINDING (binding to this slice — see the worker report): the
 * DTM-0018 REST surface exposes only a notifications READ
 * (`GET /v1/notifications`). There is **no platform read/dismiss WRITE endpoint**
 * in the generated client (no PATCH/POST mutation for notification state). Per the
 * task contract we therefore model read/dismiss as **LOCAL platform state**
 * (component state) — a presentation convenience — and we do NOT invent a
 * canonical write. The governed object is never mutated; the local state is layered
 * over it for display only.
 *
 * Read-only over governed objects: no generate / score / accept / resolve /
 * approve / govern / recompute / reanalyze control anywhere (decision #3 — Disclose
 * presents, never generates; only reanalysis changes an assessment, and reanalysis
 * is not a Disclose affordance).
 */
import { useMemo, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import CircularProgress from "@mui/material/CircularProgress";
import { Link } from "@tanstack/react-router";

import { useListNotificationsV1NotificationsGet } from "../../api/generated/notifications/notifications";
import { useListAcceptanceImpactV1ProjectsProjectIdAcceptanceImpactGet } from "../../api/generated/acceptance/acceptance";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import { epistemicTones } from "../../theme/tokens";
import type {
  Notification,
  NotificationSourceType,
  AcceptanceImpactAssessment,
} from "../../api/generated/oSLORelease1API.schemas";

export interface NotificationsProps {
  /**
   * Optional project scope for the Acceptance-Impact read (project-scoped). The
   * notifications feed itself is workspace-level. When absent, only the
   * notifications feed is shown (the impact read is skipped).
   */
  projectId?: string;
}

/** A user-facing label for the activity kind (a descriptive pointer, never a status). */
const SOURCE_TYPE_LABEL: Record<NotificationSourceType, string> = {
  finding: "Finding",
  recommendation: "Recommendation",
  analysis_run: "Analysis",
  comment: "Comment",
  shared_artifact: "Shared artifact",
};

/** True for a plain array of objects (defensive against partial responses). */
function asArray<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as T[]) : [];
}

/** A notification is "unread" unless its platform state is viewed/dismissed. */
function isUnread(n: Notification): boolean {
  return n.state !== "viewed" && n.state !== "dismissed";
}

/**
 * Route an awareness item to its SOURCE CONTEXT (spec §I), preserving context and
 * obeying surface rules. A finding/comment pointer opens the source Finding's
 * panel; analysis/shared-artifact pointers route to the project workspace/overview.
 * It never routes to a place that would change an assessment.
 */
function NotificationSourceLink({
  notification,
  projectId,
}: {
  notification: Notification;
  projectId?: string;
}) {
  const pid = notification.project_id ?? projectId;
  if (!pid) {
    // No project context to route into — present honestly, route nowhere fabricated.
    return null;
  }
  switch (notification.source_object_type) {
    case "finding":
    case "comment":
      return (
        <Link
          to="/projects/$projectId/findings/$findingId"
          params={{ projectId: pid, findingId: notification.source_object_id }}
          style={{ textDecoration: "none" }}
          data-testid="open-source"
        >
          <Button variant="text" component="span" size="small">
            Open source
          </Button>
        </Link>
      );
    case "analysis_run":
      return (
        <Link
          to="/projects/$projectId/orientation"
          params={{ projectId: pid }}
          style={{ textDecoration: "none" }}
          data-testid="open-source"
        >
          <Button variant="text" component="span" size="small">
            Open project overview
          </Button>
        </Link>
      );
    case "recommendation":
    case "shared_artifact":
    default:
      return (
        <Link
          to="/projects/$projectId"
          params={{ projectId: pid }}
          style={{ textDecoration: "none" }}
          data-testid="open-source"
        >
          <Button variant="text" component="span" size="small">
            Open project
          </Button>
        </Link>
      );
  }
}

/**
 * One notification row. `read` and the dismiss/mark-read affordances are LOCAL
 * platform state — they change nothing about the governed `notification` object
 * (which is rendered read-only). The handlers update only the parent's local map.
 */
function NotificationItem({
  notification,
  read,
  projectId,
  onMarkRead,
  onDismiss,
}: {
  notification: Notification;
  read: boolean;
  projectId?: string;
  onMarkRead: (id: string) => void;
  onDismiss: (id: string) => void;
}) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2, display: "flex", alignItems: "flex-start", gap: 1.5 }}
      data-testid="notification-item"
      data-notification-id={notification.notification_id}
      data-read={read ? "true" : "false"}
    >
      {/* Unread cue — a "look here" convenience, NOT a status/obligation. */}
      <Box
        aria-hidden
        data-testid={read ? undefined : "unread-cue"}
        sx={{
          mt: 0.75,
          width: 8,
          height: 8,
          borderRadius: "50%",
          flexShrink: 0,
          backgroundColor: read ? "transparent" : epistemicTones.bandMedium,
          border: read ? `1px solid ${epistemicTones.derived}` : "none",
        }}
      />
      <Box sx={{ flexGrow: 1, minWidth: 0 }}>
        <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 0.5 }}>
          <Chip
            size="small"
            variant="outlined"
            label={SOURCE_TYPE_LABEL[notification.source_object_type] ?? notification.source_object_type}
            data-testid="notification-kind"
          />
          {notification.created_at ? (
            <Typography variant="caption" color="text.secondary">
              {notification.created_at}
            </Typography>
          ) : null}
        </Box>
        <Typography variant="body2" sx={{ mb: 1 }}>
          New activity on {SOURCE_TYPE_LABEL[notification.source_object_type] ?? "an object"}{" "}
          ({notification.source_object_id}).
        </Typography>
        <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
          <NotificationSourceLink notification={notification} projectId={projectId} />
          {/* Platform affordances — local presentation state only, non-canonical. */}
          {!read ? (
            <Button
              variant="text"
              size="small"
              color="inherit"
              data-testid="mark-read"
              onClick={() => onMarkRead(notification.notification_id)}
            >
              Mark read
            </Button>
          ) : null}
          <IconButton
            size="small"
            aria-label="Dismiss this notification"
            data-testid="dismiss-notification"
            onClick={() => onDismiss(notification.notification_id)}
          >
            <Box component="span" aria-hidden sx={{ fontSize: 16, lineHeight: 1 }}>
              ✕
            </Box>
          </IconButton>
        </Box>
      </Box>
    </Paper>
  );
}

/**
 * One Acceptance-Impact alert — "a decision you confirmed is affected". A Derived
 * drift, surfaced via `EpistemicLabel` (banded, conflict-aware), with a link to
 * the affected accepted item's context. Never settled, NEVER auto-resolved, no
 * accept/resolve affordance.
 */
function AcceptanceImpactAlert({
  impact,
  projectId,
}: {
  impact: AcceptanceImpactAssessment;
  projectId?: string;
}) {
  const pid = impact.project_id ?? projectId;
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2, borderColor: epistemicTones.bandLow }}
      data-testid="acceptance-impact-alert"
      data-uar-ref={impact.uar_ref}
    >
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 1 }}>
        <Chip
          size="small"
          variant="outlined"
          label="Acceptance impact"
          data-testid="impact-kind"
          sx={{ color: epistemicTones.bandLow, borderColor: epistemicTones.bandLow, fontWeight: 600 }}
        />
        {/* Derived label — banded, conflict-aware; never settled. */}
        <EpistemicLabel epistemic={fromDerivedEnvelope(impact.label)} />
      </Box>
      <Typography variant="body1" sx={{ mb: 0.5, fontWeight: 600 }}>
        A decision you confirmed is affected.
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
        OSLO&apos;s understanding behind something you accepted has drifted
        {impact.band_changed
          ? ` (its confidence band changed from ${impact.pinned_band} to ${impact.latest_band})`
          : ` by ${Math.abs(impact.delta)} points`}
        . This is shown for your awareness — OSLO presents it; only reanalysis changes
        the assessment.
      </Typography>
      {pid ? (
        <Link
          to="/projects/$projectId"
          params={{ projectId: pid }}
          style={{ textDecoration: "none" }}
          data-testid="open-affected-item"
        >
          <Button variant="text" component="span" size="small">
            Review the affected understanding
          </Button>
        </Link>
      ) : null}
    </Paper>
  );
}

export function Notifications({ projectId }: NotificationsProps) {
  const notificationsQ = useListNotificationsV1NotificationsGet(
    projectId ? { project_id: projectId } : undefined,
  );
  const impactQ = useListAcceptanceImpactV1ProjectsProjectIdAcceptanceImpactGet(
    projectId ?? "",
    { query: { enabled: Boolean(projectId) } },
  );

  const notifications = asArray<Notification>(notificationsQ.data?.data);
  const impacts = projectId
    ? asArray<AcceptanceImpactAssessment>(impactQ.data?.data)
    : [];

  // ── LOCAL platform state (non-canonical): which notifications the user has
  //    locally read / dismissed. Layered over the governed feed for display only;
  //    it mutates NO governed object and writes NO canonical (no write endpoint
  //    exists — see the module docstring + the worker report).
  const [locallyRead, setLocallyRead] = useState<Record<string, true>>({});
  const [locallyDismissed, setLocallyDismissed] = useState<Record<string, true>>({});

  const visible = useMemo(
    () => notifications.filter((n) => !locallyDismissed[n.notification_id]),
    [notifications, locallyDismissed],
  );

  const markRead = (id: string) => setLocallyRead((m) => ({ ...m, [id]: true }));
  const dismiss = (id: string) => setLocallyDismissed((m) => ({ ...m, [id]: true }));

  const loading = notificationsQ.isLoading || (Boolean(projectId) && impactQ.isLoading);
  const isEmpty = !loading && visible.length === 0 && impacts.length === 0;

  return (
    <Box data-testid="notifications" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Awareness
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        What changed and where to return. Marking an item read or dismissing it is a
        personal convenience — it changes nothing about your project&apos;s understanding
        and resolves nothing. Only reanalysis changes an assessment.
      </Typography>

      {loading ? (
        <Box
          data-testid="notifications-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading awareness…
          </Typography>
        </Box>
      ) : isEmpty ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="notifications-empty" variant="body2" color="text.secondary">
            You&apos;re all caught up — nothing new to look at. (This reflects current
            activity; it is not an incomplete or pending result.)
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={3}>
          {impacts.length > 0 ? (
            <Box>
              <Typography variant="subtitle2" sx={{ mb: 1 }} data-testid="impact-section-title">
                Decisions you confirmed that are affected
              </Typography>
              <Stack spacing={2}>
                {impacts.map((impact) => (
                  <AcceptanceImpactAlert
                    key={impact.uar_ref}
                    impact={impact}
                    projectId={projectId}
                  />
                ))}
              </Stack>
            </Box>
          ) : null}

          {visible.length > 0 ? (
            <Box>
              <Typography variant="subtitle2" sx={{ mb: 1 }} data-testid="activity-section-title">
                Recent activity
              </Typography>
              <Stack spacing={2}>
                {visible.map((n) => (
                  <NotificationItem
                    key={n.notification_id}
                    notification={n}
                    read={Boolean(locallyRead[n.notification_id]) || !isUnread(n)}
                    projectId={projectId}
                    onMarkRead={markRead}
                    onDismiss={dismiss}
                  />
                ))}
              </Stack>
            </Box>
          ) : null}
        </Stack>
      )}
    </Box>
  );
}

export default Notifications;

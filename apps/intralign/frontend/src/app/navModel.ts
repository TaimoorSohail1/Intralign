/**
 * navModel — the Release 1 navigation model (DTM-0042).
 *
 * Reconciles the flat DTM-0019 nav with the project-SCOPED surface routing the
 * Wave E slices landed. Grounded in RELEASE_1_UI_SPECIFICATION_V1 §2 (Information
 * Architecture) + UI_SCREEN_INVENTORY.
 *
 * The §2 rail lists Projects · Findings · Recommendations · Reports · Shared
 * Artifacts · Notifications (+ Settings in the user menu), and states that
 * Findings/Recommendations/Reports "resolve within the active project". Wave E
 * landed those as project-scoped surfaces (`/projects/$projectId/…`), so the
 * single flat rail is split into two groups (the spec is silent on the exact
 * split — flagged; the global + project-context model below is the reconciliation):
 *
 *   - GLOBAL_NAV — always visible (Projects/Dashboard, Notifications, Settings).
 *   - PROJECT_NAV — visible only when a project is active (the route is under
 *     `/projects/$projectId`); each link targets the ACTIVE project.
 *
 * Epistemic / IA invariants encoded here:
 *   - RP-C1: there is NO standalone "Recommendations" nav entry. The Recommendation
 *     Panel is reached only from a Finding (the route nests under a Finding), so it
 *     never appears in this model.
 *   - Category-E (commodity) screens with no R1 surface — Reports, Shared Artifacts —
 *     are NOT in the R1 nav (honest: the spec's §3 lists them, but no surface is
 *     built; rather than a silent "Surface pending" dead-end they are omitted).
 *   - Settings is a global entry but is a DEFERRED stub (no settings UI invented).
 */

/** A nav entry whose `to` is an absolute, already-resolved route. */
export interface NavEntry {
  to: string;
  label: string;
  /** True when the link only resolves on exact match (the Dashboard `/`). */
  exact?: boolean;
  /** Marks an entry that has no R1 surface — rendered disabled, never a dead-end. */
  deferred?: boolean;
}

/**
 * Global nav — always rendered (UI spec §2: Projects, Notifications; Settings from
 * the user menu, surfaced here as a top-level global entry for R1).
 */
export const GLOBAL_NAV: ReadonlyArray<NavEntry> = [
  { to: "/", label: "Projects", exact: true },
  { to: "/notifications", label: "Notifications" },
  // Settings has no built surface in R1 (Category-E commodity) — kept as a global
  // entry but flagged deferred so it never dead-ends at a silent "Surface pending".
  { to: "/settings", label: "Settings", deferred: true },
];

/**
 * Project-context sub-paths (relative to `/projects/$projectId`). These resolve to
 * the BUILT Wave E surfaces; `buildProjectNav` resolves them against the active
 * project id. Order follows the §2 hierarchy (Workspace → Orientation → Findings →
 * secondary project-context surfaces).
 */
const PROJECT_NAV_TEMPLATE: ReadonlyArray<{ sub: string; label: string }> = [
  { sub: "", label: "Workspace" }, // MRI umbrella — `/projects/$pid/`
  { sub: "/orientation", label: "Overview" }, // Project Overview
  { sub: "/findings", label: "Findings" }, // Issue Cards
  { sub: "/history", label: "History" }, // Timeline
  { sub: "/export", label: "Export" }, // Export / Share-out
  { sub: "/companion", label: "Companion" }, // Understanding Companion
  { sub: "/chat", label: "Chat" }, // OSLO Chat
];

/**
 * The active project's id, derived from the current route. `null` when no project is
 * active (e.g. the Dashboard) — callers HIDE the project group rather than route a
 * project-scoped link with no id.
 */
export function activeProjectIdFromPath(pathname: string): string | null {
  // `/projects/<id>` or `/projects/<id>/...` — but NOT `/projects/new`.
  const m = pathname.match(/^\/projects\/([^/]+)(?:\/|$)/);
  if (!m) return null;
  const id = decodeURIComponent(m[1]);
  if (id === "new") return null;
  return id;
}

/** Resolve the project-context nav against the active project id. */
export function buildProjectNav(projectId: string): NavEntry[] {
  return PROJECT_NAV_TEMPLATE.map(({ sub, label }) => ({
    to: `/projects/${projectId}${sub}`,
    label,
    exact: sub === "", // the Workspace root must match exactly (else every child highlights it)
  }));
}

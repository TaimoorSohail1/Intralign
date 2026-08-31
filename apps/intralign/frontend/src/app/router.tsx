/**
 * TanStack Router tree (code-based) for the OSLO app shell.
 *
 * Routes are the Release 1 screens from UI_SCREEN_INVENTORY.md, scoped per the IA
 * in RELEASE_1_UI_SPECIFICATION_V1 §2. Every element is a PLACEHOLDER (DTM-0019
 * ships the shell only); the real surfaces mount here in DTM-0020+.
 *
 * RP-C1 is encoded structurally: the Recommendation Panel route lives ONLY under a
 * Finding (`/projects/$projectId/findings/$findingId/recommendations`), never as a
 * standalone top-level route — so "Recommendation-Panel-only-in-Finding-context" is
 * enforced by the route tree itself, not duplicated as a cognition rule.
 */
import {
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
} from "@tanstack/react-router";
import { AppShell } from "./AppShell";
import { PlaceholderSurface } from "./PlaceholderSurface";
import { MRIRoute } from "../surfaces/MRI/MRIRoute";
import { FindingPanelRoute } from "../surfaces/Panels/FindingPanel/FindingPanelRoute";
import { RecommendationPanelRoute } from "../surfaces/Panels/RecommendationPanel/RecommendationPanelRoute";
import { IssueCardsRoute } from "../surfaces/IssueCards/IssueCardsRoute";
import { DashboardRoute } from "../surfaces/Overview/DashboardRoute";
import { ProjectOverviewRoute } from "../surfaces/Overview/ProjectOverviewRoute";
import { CompanionRoute } from "../surfaces/Companion/CompanionRoute";
import { NotificationsRoute } from "../surfaces/Notifications/NotificationsRoute";
import { TimelineRoute } from "../surfaces/Timeline/TimelineRoute";
import { ExportRoute } from "../surfaces/Export/ExportRoute";
import { ChatRoute } from "../surfaces/Chat/ChatRoute";
import { ArtifactEditorRoute } from "../surfaces/AssistedEditing/ArtifactEditorRoute";

const rootRoute = createRootRoute({
  component: AppShell,
});

// ── Top-level screens ──────────────────────────────────────────────────────────
// DTM-0024 — the Dashboard / Project List mounts at the top-level `/` route,
// replacing the DTM-0019 placeholder. It lists the caller's workspace projects,
// each with its current Outcome Confidence (Derived, banded) and a workspace link.
// Read-only — no edit/score/accept/generate control (decision #3, Disclose presents,
// never generates); the project understanding stays the center of gravity, never a
// "project health"/score indicator.
const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: DashboardRoute,
});

const projectsCreateRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/projects/new",
  component: () => (
    <PlaceholderSurface
      title="Create a project"
      purpose="Create a project; add first intent/evidence; trigger Fast Analysis."
    />
  ),
});

// Project workspace + its sub-surfaces (a layout route with a nested outlet).
const projectRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/projects/$projectId",
  component: () => <Outlet />,
});

// DTM-0020 — the MRI umbrella surface mounts at the Project Workspace route,
// replacing the DTM-0019 placeholder. It is the project's understanding view
// (Findings/CAF/Confidence + the four DL-047 sub-components), read-only.
const projectWorkspaceRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/",
  component: MRIRoute,
});

// DTM-0024 — the Project Overview mounts at the Orientation route, replacing the
// DTM-0019 placeholder. UI_SCREEN_INVENTORY maps the 60-Second Orientation to the
// project-level understanding summary (confidence, CAF, counts) — exactly the
// Project Overview. The Workspace root (`/`) is the MRI umbrella (DTM-0020), so the
// Overview mounts here. Read-only — aggregate Outcome Confidence + CAF via
// EpistemicLabel (Derived, banded), counts of governed objects; never project health.
const orientationRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/orientation",
  component: ProjectOverviewRoute,
});

// DTM-0025 — the Understanding Companion mounts at the project Companion route,
// replacing the DTM-0019 placeholder. It is the contextual understanding surface
// (Outcome Confidence · CAF · Top Findings · Top Recommendations · stale-analysis
// state · Ask OSLO), read-only. Option B (preserves RP-C1): a Top Recommendation's
// affordance routes to the recommendation's ASSOCIATED FINDING (the Finding Panel),
// NEVER directly to a standalone Recommendation Panel.
const companionRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/companion",
  component: CompanionRoute,
});

// DTM-0027 — the History / Timeline surface mounts at the project History route,
// replacing the DTM-0019 placeholder (none existed under the project; this is the
// one route add). It is a SECONDARY project-context surface (Companion-Surface-class,
// HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1 §D) — never a primary top-level
// destination — that reconstructs the append-only TRAIL: the CHR history (the
// analysis runs that appended Cognition History Records, each Derived/never settled)
// + the UARs + the plan facts the user attested (user-attested, "You confirmed …",
// NOT world-truth). Read-only — no edit/accept/generate/restore/rollback control
// (decision #3, Disclose presents, never generates; spec §J append-only, no
// deletion/mutation affordances). Superseded entries STAY visible (additive).
const historyRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/history",
  component: TimelineRoute,
});

// DTM-0028 — the Export / Share-out surface mounts at the project Export route
// (`/projects/$projectId/export`; the one route add — no project-level export route
// existed). It is a lightweight Companion-Surface-class ACTION (Export & Share-Out
// spec §D) — a secondary project-context surface, never a primary top-level
// destination and never a reporting workspace. It PACKAGES the existing governed
// outputs (confidence/CAF/findings/recommendations/UARs/plan facts) into an
// exportable artifact (browser Blob/anchor download + an in-app preview) that honors
// the epistemic labels (Derived/Attested + band, plan-fact attribution) and preserves
// provenance (the CHR version/source travels into the package) — and introduces NO new
// claim (every line traces to a governed source field; decision #3, Disclose presents,
// never generates). Read-only — no generate/score/accept/edit/govern/reanalyze control.
const exportRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/export",
  component: ExportRoute,
});

// DTM-0029 — OSLO Chat mounts at the project Chat route, replacing the DTM-0025
// placeholder. It is a Disclose-class conversation surface that CONSUMES cognition
// (Explain/Clarify) and may TRIGGER it (Improve → Advise + Deep Pass) — but writes NO
// canonical, mutates NO artifact, changes NO assessment (Critical, decision #10). It
// inherits context when launched from an issue/recommendation/artifact/finding via the
// search params (`context_kind`/`context_id`/`context_label`) — read-only, used only to
// present and route relevantly. CHAT-COMMAND ENDPOINT (ANTI_ASSUMPTION, flagged): the
// DTM-0018 client is GET-only, with no chat send/trigger endpoint — a send appends an
// ephemeral, non-canonical pending exchange; "Improve" would route to the existing
// Advise/Deep-Pass trigger when exposed. Nothing canonical is recorded.
const projectChatRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/chat",
  validateSearch: (
    search: Record<string, unknown>,
  ): { context_kind?: string; context_id?: string; context_label?: string } => ({
    context_kind:
      typeof search.context_kind === "string" ? search.context_kind : undefined,
    context_id:
      typeof search.context_id === "string" ? search.context_id : undefined,
    context_label:
      typeof search.context_label === "string" ? search.context_label : undefined,
  }),
  component: ChatRoute,
});

const analysisRunRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/analysis-runs/$runId",
  component: () => (
    <PlaceholderSurface
      title="Analysis Progress"
      purpose="Async status while a fast/deep run executes."
    />
  ),
});

// DTM-0023 — Issue Cards mount at the project findings route, replacing the
// DTM-0019 placeholder. There is no dedicated "Issues" screen in the inventory;
// issues (prioritized findings — Finding + assigned severity) are presented in
// the project's findings context. The cards present severity + Derived confidence
// and link each card back to its source Finding (the Finding Panel route).
// Read-only — no triage/act control (decision #3, Disclose presents, never
// generates; the inventory's "act" verbs are out of scope for the read surface).
const projectFindingsRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/findings",
  component: IssueCardsRoute,
});

// Finding detail (the Finding Panel context). RP-C1: recommendations nest here.
const findingRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/findings/$findingId",
  component: () => <Outlet />,
});

// DTM-0021 — the Finding Panel mounts at the Finding-detail route, replacing the
// DTM-0019 placeholder. It presents one finding + its Attested evidence lineage +
// Derived confidence, and the RP-C1 affordance into the nested recommendations
// route. Read-only.
const findingDetailRoute = createRoute({
  getParentRoute: () => findingRoute,
  path: "/",
  component: FindingPanelRoute,
});

// DTM-0022 — the Recommendation Panel mounts at the nested recommendations route,
// replacing the DTM-0019 placeholder. RP-C1: it renders ONLY within a Finding
// context (this route lives only under a Finding). It presents the finding's
// Recommendations as OSLO Recommended + Resolution Paths (presentation grouping,
// no object) with the accept/reject/defer affordance that HANDS OFF to the Wave U
// capture (the project Recommendation Workspace below) — Disclose never accepts.
const findingRecommendationsRoute = createRoute({
  getParentRoute: () => findingRoute,
  path: "/recommendations",
  component: RecommendationPanelRoute,
});

// DTM-0042 — the standalone project Recommendation Workspace and Report Viewer
// placeholder routes were REMOVED here. Reasons:
//   - Recommendation Workspace: RP-C1 keeps the Recommendation Panel reachable only
//     from a Finding (`/findings/$findingId/recommendations`); a standalone project
//     recommendations route is not a Wave E surface and had no inbound nav/affordance.
//   - Report Viewer: Reports are a Category-E commodity screen with no R1 surface; a
//     placeholder route is a silent dead-end. Omitted (honest) rather than shipped.

// DTM-0029 — the Artifact Editor mounts the Assisted-Editing / Persistent-Intelligence
// panel (AW-04/05), replacing the DTM-0019 placeholder. The panel is ALWAYS-VISIBLE,
// READ-ONLY presentation of the governed intelligence (Outcome Confidence + CAF +
// Understanding-State via EpistemicLabel) and ROUTES assists to Chat (B1) / Suggested
// Fix (B3) — performing none. It needs the project context: the editor reads it from the
// `project_id` search param (the launching surface carries it); an optional `finding_id`
// scopes the B3 Suggested-Fix assist via its Finding (RP-C1). Absent project context ⇒
// the panel is held until it is provided (no fabricated project).
const artifactRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/artifacts/$artifactId",
  validateSearch: (
    search: Record<string, unknown>,
  ): { project_id?: string; finding_id?: string; limited?: boolean } => ({
    project_id: typeof search.project_id === "string" ? search.project_id : undefined,
    finding_id: typeof search.finding_id === "string" ? search.finding_id : undefined,
    // The DL-048 scope/budget-limit signal is NOT yet exposed over REST (flagged
    // dependency). This param is the presentation seam: when the limit signal arrives,
    // the honest-limit disclosure renders on this same (partial-orientation) surface.
    limited: search.limited === true || search.limited === "true",
  }),
  component: ArtifactEditorRoute,
});

// DTM-0042 — the leftover top-level cross-project placeholder routes
// (`/findings`, `/recommendations`, `/reports`, `/shared`, `/shared/$shareId`) were
// REMOVED. The DTM-0019 nav linked the rail to these top-level routes, but the real
// Wave E surfaces are project-SCOPED (`/projects/$projectId/findings`, the MRI at
// `/projects/$projectId/`, …). The nav (see AppShell + navModel) now routes Findings
// et al. into the ACTIVE project, so these flat routes were dead-ending at a
// "Surface pending" placeholder for surfaces that already exist. Reports/Shared are
// Category-E commodity screens with no R1 surface — omitted (honest), not stubbed.
// RP-C1 is preserved: there is no standalone Recommendations route at all (the
// Recommendation Panel lives only under a Finding).

// DTM-0026 — the Notification / Awareness surface mounts at the top-level
// `/notifications` route, replacing the DTM-0019 placeholder. It presents new
// emissions (the workspace-level notifications read) + Acceptance-Impact alerts
// ("a decision you confirmed is affected" — a Derived drift, project-scoped via
// the optional `project_id` search param) as awareness, and routes each to its
// source context. Read-only over governed objects; read/unread/dismiss is platform
// state (Category E) — NON-canonical (decision #9): it writes no canonical, changes
// no assessment, and resolves no drift.
const notificationsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/notifications",
  validateSearch: (search: Record<string, unknown>): { project_id?: string } => ({
    project_id:
      typeof search.project_id === "string" ? search.project_id : undefined,
  }),
  component: NotificationsRoute,
});

const settingsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/settings",
  component: () => (
    <PlaceholderSurface title="User Settings" purpose="Profile and workspace basics." />
  ),
});

const routeTree = rootRoute.addChildren([
  dashboardRoute,
  projectsCreateRoute,
  projectRoute.addChildren([
    projectWorkspaceRoute,
    orientationRoute,
    companionRoute,
    historyRoute,
    exportRoute,
    projectChatRoute,
    analysisRunRoute,
    projectFindingsRoute,
    findingRoute.addChildren([findingDetailRoute, findingRecommendationsRoute]),
  ]),
  artifactRoute,
  notificationsRoute,
  settingsRoute,
]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

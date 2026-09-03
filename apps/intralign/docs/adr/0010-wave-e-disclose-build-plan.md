# Wave E (Disclose) is REST-exposure-first, then the UI surfaces; Disclose presents, never generates

Phase VI / Wave E contracts `IC/QA/OBS-WE-DISCLOSE` — the user-facing presentation layer and the
**Release 1 feature-complete gate**. Disclose is a **consumer** (presents, never generates);
**Render** is its non-cognitive service. Every surface labels uncertainty (**Attested/Derived +
confidence band + conflict**), shows **current + history**, and **changes no assessment**. This
ADR records how it lands in `code/`; the Wave E contract + the ratified UX specs + DL-043/047/048/055
are the governing source (if a plan and a spec differ, the **spec wins**).

## The load-bearing finding (why this isn't "just a UI build")

The frontend is a correct but **bare scaffold** (React 18 · Vite · MUI · Emotion · TanStack
Query + Router · Orval · Axios — no components/routes/theme). Critically, **the backend REST
surface the UI consumes does not exist yet**: `backend/api/v1/` wires only `GET /health`; every
domain router (projects, artifacts, findings, recommendations, issues, confidence/CAF, history,
acceptance, notifications, export) is a *commented catalog* — none built. The Orval client only
generates `/health`. So Phase VI delivers **two layers**:
1. **REST exposure (backend `api/v1/` + `services/render`)** — present the governed objects the
   Waves A–U cognition already produces, as **Data Model v1.2 DTOs** (`shared/entities.py`), over
   the ratified REST `/v1` surface (ADR-0003). The `render` service maps internal cognition
   (Finding/Issue/Confidence/CHR/UAR/PlanFact) → external DTOs; the API is **read-mostly** (it
   presents; writes are the existing capture/acceptance seams). This is what Disclose presents
   *through*.
2. **UI surfaces (`frontend/src/surfaces/`)** — the screens, consuming the generated client.

## Build plan (slices; one fresh worker each, reviewed before the next)

- **DTM-0018 — REST exposure + render DTOs:** wire the `api/v1` routers + `services/render`
  mappers for the governed objects the surfaces need; OpenAPI regenerates the Orval client; the
  drift gate stays green. *(Enabling layer — no new cognition; read-mostly.)*
- **DTM-0019 — App shell + design system:** TanStack Router tree + MUI `ThemeProvider`/`CssBaseline`
  with the **Intralign palette** (charcoal `#111315`, warm-white `#F5F4F0`, orange `#D97A3A`,
  CHG-068), WCAG 2.1 AA, evergreen browsers; the reusable **epistemic-safety label** component
  (Attested/Derived + band + conflict) used by every surface.
- **DTM-0020…002N — one surface per slice:** MRI (umbrella + MRI-04…07 Heatmap/CAF-Triangle/
  Understanding-Timeline/Dependencies) · Finding Panel · Recommendation Panel (**RP-C1**) · Issue
  Cards · Project Overview · Understanding Companion (route via Finding — Option B) ·
  Notification/Awareness · History/Timeline · Export/Share-out · OSLO Chat (DL-047, Disclose-class)
  + Assisted Editing (AW-04/05) + honest-limit disclosure (DL-048 UP-4).

## Status

accepted — locked from docs (Phase VI plan + Wave E contract E0–E3 + DL-047/048 additions + the
ratified UX specs + the frontend scaffold), 2026-06-25. **Coding gated on the Wave E owner
authorization (DL-044) + readiness gate; Wave E is the Release 1 feature-complete gate, so its
exit is the final pre-production owner sign-off.**

## Considered Options

- **UI-only (assume the API exists)** — rejected: the domain REST endpoints are not built; the UI
  would have nothing to consume. REST exposure is a real prerequisite, surfaced here.
- **One mega-slice** — rejected: ~10 surfaces + the API + the shell is unreviewable as one diff.
- **REST-exposure-first → shell → per-surface slices (chosen)** — each surface is independently
  verifiable against its UX spec + the QA negatives; matches the Wave A–U discipline.

## Consequences

- **Disclose presents, never generates** — no surface (and no router) computes, scores,
  recommends, promotes Derived→Attested, **accepts** (the Recommendation Panel renders the
  accept/reject/defer *affordance* → routes to the existing **Wave U** capture; Disclose itself
  never accepts), or changes an assessment. Negative-proven (the QA negatives are the heart of
  Wave E): Derived-as-settled, confidence overstated (band-edge guard), **RP-C1** violation,
  Resolution-Path-as-object, acceptance-by-Disclose, notification-state-as-canonical, unsourced
  export, **Chat writing canonical / mutating an artifact / changing assessment outside recompute**
  (Critical).
- **Epistemic-safety labeling everywhere** — one shared component renders Attested/Derived + the
  confidence band (0–49/50–74/75–100, ±3 conservative edge guard) + conflict; plan facts show as
  **user-attested** (distinct from evidence- and OSLO-attested); confidence is **trust in
  understanding, never project health**. Current foreground **and** history/timeline both present;
  drift surfaced at ≥10 pts / band change.
- **Stack frozen** — reuse the scaffold (no new framework). **E2E = Playwright** (the plan's
  Playwright/Cypress → Playwright); component tests = Vitest; the Orval **OpenAPI drift gate**
  (tsc) stays in CI; gate-6 keeps `npm audit`.
- **Visual system — locked vs designer-pending (ANTI_ASSUMPTION):** the **Intralign palette**,
  **WCAG 2.1 AA**, and **evergreen browsers** are owner-ratified → build to them. Type scale/fonts,
  logo/favicon, component redlines, and final microcopy are **designer-pending (OPEN_TBD E4)** →
  use a sensible MUI default type scale + placeholder copy from the UX specs; **do not invent**
  final brand details (leave a clean theme seam for the designer).
- **Observability** — OBS-WE events (`Disclosure Rendered`, `Notification Raised`,
  `Acceptance-Impact surfaced`, `Export produced`; platform read/dismiss is non-canonical);
  "what-was-shown" is reconstructable from the governed source + the CHR version it presented.
- Detailed slice scope/tests live in `code/docs/deep-tasks/wavee-disclose-deep-task/` (authored at
  build time).

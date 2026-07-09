# R1 UX Build — Developer Handoff Index

> **Single entry point** for building the Release-1 experience exactly as designed and correctly wired to the backend. Read this first, then work top-down. Date: 2026-07-02 (updated 2026-07-03).

> **Before you build — read `20_handoff/R1_BUILD_SEQUENCE_AND_GATES.md`.** It defines the build **order** and the gates that enforce it. Two hard prerequisites and one guardrail apply to everything below:
>
> 1. **BLOCKER — the R1 app is not on `main` yet.** The Disclose application lives on `feat/phase6-wavee-disclose`; `main` holds only a skeleton (`code/frontend/src/` is just `main.tsx`, `api/v1/routers/` just `__init__.py`). **Integrate it first** (Issue #113) — do **not** start wiring the UI until it lands. Only the specs, prototype, and baselines referenced here are on `main`.
> 2. **The prototype + all 9 visual baselines were updated (PR #116).** Pull latest `main` and build to the **current** `product-design/oslo_r1_experience_mockup_v3.html` — not any earlier read.
> 3. **GUARDRAIL — RB-035 (PR #117) is UNRATIFIED; do not build it.** It proposes dropping the `acknowledged` finding state and single-action resolution. Build the **ratified** `FINDING_SYSTEM_SPECIFICATION_V1 §C` (`detected → acknowledged → addressed → closed`, multi-step resolution) until the owner ratifies the DL.

## The build contract (read first)
1. **The prototype is the spec.** `product-design/oslo_r1_experience_mockup_v3.html` is the **reference of record** — build the UX to match it exactly (layout, states, interactions, copy). The experience specs describe intent; where a detail is only visible in the prototype, the prototype wins.
2. **Two gates make "exact" verifiable, not trusted** (`30_engineering/visual_regression/`):
   - **Visual** — screenshot diff of each built surface vs the committed baselines (≤ 2%).
   - **Behavioral** — the per-surface checks in `ACCEPTANCE_CRITERIA.md`, each traced to a decision.
   A surface ships only when **both** pass. Wire the sample CI (`visual_regression/ci/visual-regression.sample.yml`) into the app repo.
3. **Wire to real data from day one.** Every dynamic element maps to a real state field / event / endpoint — see the integration map (below). Don't build a shell.
4. **Governance invariants are non-negotiable** — advisory-only (DL-043/047); only reanalysis changes assessment; Confidence never bare and never health/probability; neutral (non-health-color) confidence ramp.

## What to read, in order

**A. The design (what to build)**
- Prototype (reference of record): `product-design/oslo_r1_experience_mockup_v3.html` (+ `OSLO_R1_UX_PROTOTYPE_NOTES_AND_GAP_AUDIT.md`).
- Experience specs: `10_product/experience/` — especially `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` (§P/§Q), `FINDING_PRESENTATION_SPECIFICATION_V1` (§O), `FINDING_PANEL_SPECIFICATION_V1`, `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1` (§U), `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1` (§U), `MRI_EXPERIENCE_SPECIFICATION_V1` (§R), `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1` (Q3), `UI_SCREEN_INVENTORY` (12 primary screens; Recommendation Workspace retired).
- Screen list: `10_product/experience/UI_SCREEN_INVENTORY.md`.

**B. Why it's this way (the ratified decisions — this session)**
- `00_owner/decisions/records/DL-085` Confidence presentation (number-focal, cause-bound, work-ledger, no-gamification).
- `DL-086` Confidence calibration (5-band map · v0 defaults · ±7 tolerance).
- `DL-087` Strategic-chain positioning + plain-language labels (glossary Disambiguation Register).
- `DL-088` UX-surface reconciliation (Overview hierarchy, Findings/History center panes, shell declutter; ⌘K → R2).
- `DL-089` Clarification contract (object-free; in-panel + chat).

**C. How it binds to the backend (what to wire)**
- **UI↔backend map:** `20_handoff/traceability/R1_UI_BACKEND_INTEGRATION_MAP.md` — each surface → state field / read / write / event, plus open gaps (G3–G8).
- **Interfaces:** `20_handoff/interfaces/RELEASE_1_STATE_MODEL_SPECIFICATION_V1`, `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1` (incl. §14a clarification), `RELEASE_1_API_CONTRACT_SPECIFICATION_V1` + `API_CONTRACT_ENDPOINT_CATALOG`.
- **Contracts:** `20_handoff/contracts/` (WAVE packages).
- **Coverage:** `20_handoff/traceability/RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` — every capability → contract → test → observability event (incl. `CLR-01`).

**D. Confidence (the signature surface)**
- Formula: `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (v0, ratified for R1 by DL-086).
- Bands (ratified): Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100; ±7/same-band tolerance. Sub-±7 jitter must not render as change.

**E. Build rules + starter kit**
- `30_engineering/delivery/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` → `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`.
- App-repo build rules: `30_engineering/delivery/starter_kit/CLAUDE.md` (+ `AGENTS.md`).
- **Anti-Assumption:** `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md` — never infer a spec gap; escalate it.
- **Owner-TBD values:** `00_owner/OPEN_TBD_REGISTER.md` — scaffold the metric, don't invent the value (A2 latency, E3 tiers still open).

## Known open items (do not assume — build to contract, escalate gaps)
- Integration-map **G3–G8** (history feed read; ledger-derived metrics; confidence-change cause linkage in `confidence_recalculated`; numeric trend series in `confidence?history`; auto-reanalysis debounce; recommendation `deferred` surface).
- `OPEN_TBD` **A2** (latency p50/p95) and **E3** (paid-tier limits).
- Command palette (⌘K) is **R2**, not R1.

## R1 completion dependencies — what blocks R1 vs what doesn't
**No *TBD* in this list blocks starting R1** — but the app-integration prerequisite in the banner at the top **does** (Issue #113; integrate the app before wiring the UI). Categorized so no TBD is mistaken for a blocker:

- **Ratified for R1 — build to these now:** confidence formula v0 + **5-band** + **±7** (DL-086); Fast-Pass **Free envelope** ~20 artifacts / ~50k words / 1 active (A1); the **`<60s` Time-to-First-MRI ceiling** (ratified, Master Spec §20/M1); browsers **evergreen** (E1); **WCAG 2.1 AA** (E2); Intralign **palette** core (E4).
- **Not R1 — do not wait on these:** paid-tier values Pro/Team/Enterprise (**E3 → R2**; tiers are Calibration config rows, not code); latency **p50/p95 distribution targets** (A2 — only the *targets* are open; the `<60s` ceiling is ratified; refine from telemetry); **command palette ⌘K** (R2); designer assets — type scale / logo / microcopy (E4 → designer; token contract holds).
- **Resolve *during* build (feature-completeness, not pre-start blockers):**
  - **G5** — `confidence_recalculated` payload carries the driving finding/CAF ref (backs the cause-bound Confidence banner, DL-085).
  - **G6** — `GET /projects/{pid}/confidence?history=true` returns the numeric value per run (backs the trend chart, DL-085).
  - **G3** — history-surface read (existing per-object reads likely suffice; confirm).
  - **G4 / G7 / G8** — soft: derive-or-drop the two derived ledger counts; auto-reanalysis debounce tuning; optional recommendation-`deferred` affordance.

**Rule:** treat any open TBD as *"build to the ratified default / scaffold the metric, refine from telemetry"* — never as a blocker, and never guess an owner value (escalate per the Anti-Assumption Build Protocol).

## Definition of done (per surface)
Visual baseline match (≤2%) **and** all `ACCEPTANCE_CRITERIA.md` checks pass **and** every dynamic element bound per the integration map **and** governance invariants hold. Any capability missing from the traceability matrix is a coverage defect to **escalate**, not fill by assumption.

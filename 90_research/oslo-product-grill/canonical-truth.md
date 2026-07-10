# Canonical Truth — OSLO R1

Derived from the R1 product artifacts (see `source-summary.md`). Structure is canon-traceable; sample text/numbers in the prototype are illustrative demo data, not ratified values.

**Baseline: `oslo_r1_experience_mockup_v4.html`.** v4 folds in these ratified additions (all Locked from docs):
- **DL-095** — user-facing label is **"Issues"** ("Finding" = internal object); toggle "By dimension / By severity".
- **DL-094** — issue lifecycle **Open → Addressed → Resolved** (Acknowledge removed); single-action "Apply this fix".
- **DL-096** — Overview redesign: confidence-led focal score, CAF maturity bars, quiet trend, "Why" disclosure; ring/green box/pills removed.
- **DL-086 / DL-098** — shared **5-band scale** (Very Low·Low·Moderate·High·Very High) for Confidence + CAF.

## Locked From Docs

- **Decision:** OSLO is advisory-only — OSLO advises; the user decides and acts. Never "OSLO plans/decides/runs it for you."
  - Source: Onboarding Positioning §Guardrails (DL-043/DL-047); Workflow diagram; UX Notes §2
  - Confidence: High · Applies to: all surfaces, AI behavior, copy · Impact: global
  - Source classification: Product evidence

- **Decision:** Confidence = understanding maturity (0–100 + band), never health/success/readiness/probability/risk; never traffic-light colored.
  - Source: Confidence Doctrine; Visual spec §1.2; UX Notes §4c, §2; Workflow diagram
  - Confidence: High · Applies to: Overview, pill, CAF, exports · Impact: doctrine-level
  - Source classification: Product evidence

- **Decision:** Color semantics — red/amber/green (severity ramp) is used ONLY for finding severity (critical/moderate/warning). Confidence and CAF stay on a neutral maturity ramp.
  - Source: UX Notes §4c; Visual spec §1.2 · Confidence: High · Applies to: all color · Impact: doctrine-level
  - Source classification: Product + Design evidence

- **Decision:** Seven planning artifacts — Intent · Context · Scope · Requirements (understanding core) + WBS · Schedule · Resources (classical-PM execution).
  - Source: DL-077; UX Notes §2 · Confidence: High · Applies to: artifact model, editor, explorer · Impact: data model
  - Source classification: Product evidence

- **Decision:** Flow — Intake → Fast Pass <60s → 60-second orientation lands on MRI → Deep Pass auto-runs (non-blocking) and supersedes.
  - Source: DL-046; Workflow diagram; UX Notes §2 · Confidence: High · Applies to: onboarding, analysis · Impact: core flow
  - Source classification: Product evidence

- **Decision:** Reanalysis is event-driven only (no manual "Reanalyze" button). Editing an artifact or updating a finding auto-reanalyzes. Only reanalysis changes the assessment; last-good is preserved on failure.
  - Source: UX Notes §6.3, §6.4; Orientation State Model · Confidence: High · Applies to: editor, findings, analysis state · Impact: core behavior
  - Source classification: Product evidence

- **Decision:** MRI is Heatmap-primary (artifacts × CAF); CAF field secondary. Attention is the plain user-facing surface.
  - Source: MRI Experience/Model; UX Notes §2, §6.8 · Confidence: High · Applies to: Overview/MRI · Impact: primary screen
  - Source classification: Product evidence

- **Decision:** Findings are never resolved by hand. Finding Panel is contextual (Header→Why→Evidence→CAF impact→Recommendations→History→Reanalysis). Lifecycle: detected→acknowledged→addressed→closed.
  - Source: Finding Panel spec (Option A, ratified); Finding System §C; UX Notes §2, §6 · Confidence: High · Impact: findings surface
  - Source classification: Product evidence

- **Decision:** Panel Model (Decision 001, 2026-05-31, Option A) — Recommendations exist ONLY inside the Finding context; no standalone Recommendation Workspace / orphan roll-up. Selecting a Resolution Path = Selected Path (Attested).
  - Source: Finding & Recommendation Surface Reconciliation Decision 001; RECOMMENDATION_PANEL_SPEC RP-12; UX Notes §6.3 · Confidence: High · Impact: findings/recs
  - Source classification: Product evidence

- **Decision:** Reliability qualifier with three components — Coverage · Evidence availability · Assessability (High/Moderate/Low), independent of CAF. False-confidence flag when high band sits on low reliability.
  - Source: Reliability Model V1; Confidence Model CONF-06; UX Notes §6, Tier 1 · Confidence: High · Impact: Overview
  - Source classification: Product evidence

- **Decision:** Epistemic notation — text is Derived (OSLO) by default; edit/confirm makes it Attested (you) = a plan fact. Plain labels: "From OSLO" / "Confirmed by you."
  - Source: DL-043; PlanFact; UX Notes §2, §6.8 · Confidence: High · Impact: editor, data model
  - Source classification: Product evidence

- **Decision:** Plain-language display map (internal canonical terms unchanged): Artifacts→"Plan artifacts", WBS→"Work breakdown", CAF→"Clarity·Alignment·Feasibility", Derived→"From OSLO", Attested→"Confirmed by you", Fast/Deep Pass→"Initial/Extended Analysis", Provisional→"Still updating".
  - Source: UX Notes §6.8 (owner 2026-06-30/07-01) · Confidence: High · Impact: all copy
  - Source classification: Product evidence

- **Decision:** Global shell = three nested contexts (Workspace › Project › Object, NAV-6). Left rail = Project/Object; top-left = Workspace Home + project switcher; top-center = Project views (Overview·MRI·Artifact primary; Collaboration·History secondary); top-right = Settings/Account.
  - Source: GLOBAL_NAVIGATION spec NAV-6/C3; UX Notes §4b · Confidence: High · Impact: app shell
  - Source classification: Product evidence

- **Decision:** Intake accepts **PDF, DOCX, TXT, MD, PPTX, XLSX, CSV + paste** (D033; ~10 MB/file, ~10 files illustrative). Ingestion = text extraction + synthesis into the 7 plan artifacts + **structured-table extraction** for spreadsheets/CSV/doc tables; **no OCR in R1** (D034, owner-TBD later).
  - Source: owner 2026-07-09 · Confidence: High · Applies to: intake, analysis · Impact: user-visible capability

- **Decision:** Release phasing — R1 is the **Alpha** release; **Alpha & Beta are invite-only (users authenticated from activation, never anonymous). Anonymous product access begins at GA.** Anonymous first-run, save-to-keep gate, and claim-through are GA-phase.
  - Source: owner direction 2026-07-09 (clarifying DL-073/DL-080 phasing) · Confidence: High · Applies to: onboarding, tiering · Impact: scope/phasing
  - Source classification: Product evidence (owner)

- **Decision:** Free-tier is visibility-first — honest at-cap upgrade-or-archive modal (non-destructive archive frees slot), persistent quiet "Free · Upgrade" chip, save-to-keep after orientation, anonymous first-run = Fast-Pass-only. Billing/enforcement deferred; all tier numbers illustrative.
  - Source: DL-048, DL-080; UX Notes §6.6 · Confidence: High · Impact: tier/onboarding
  - Source classification: Product evidence

- **Decision:** Two-theme model (VISUAL_DESIGN §1) — one semantic token set; dark default (`:root`), light overrides same names. Neutral maturity ramp per theme. Accessibility WCAG 2.1 AA target (focus rings, keyboard nav, reduced-motion, no-animation-during-analysis).
  - Source: Visual Design spec §1/§3; UX Notes §6.2, Tier 4 · Confidence: High · Impact: theme (Phase 2)
  - Source classification: Design evidence

## Needs Client Decision

- **Decision:** Onboarding hero headline (A "See your plan like a strategic leader" / B / C) and wordmark descriptor.
  - Why docs insufficient: Positioning draft explicitly leaves this as an owner choice.
  - Recommended answer: Headline A + descriptor "Strategic project leadership."

- **Decision:** Confidence movement magnitude on apply-fix (the 58→66 demo).
  - Why insufficient: numeric NFR is owner-TBD (OPEN_TBD A1); prototype shows direction only.
  - Recommended answer: Direction-only in prototype (▲/▼ with cause); no fabricated number.

- **Decision:** Does the R1 prototype scope include multi-project Dashboard, Notifications, Settings, Collaboration/Sharing, Export as full surfaces, or Alpha-scope stubs?
  - Why insufficient: specs exist but prototype notes mark several as Alpha-scope/larger.
  - Recommended answer: Include them as fat slices (they are already built in v2); mark CRR out of scope.

## Conflicts

- **Conflict:** MRI nested inside Overview vs NAV-C3 "MRI as co-primary."
  - Sources: prototype (nested) vs GLOBAL_NAVIGATION NAV-C3 (owner-directed co-primary).
  - Recommended resolution: Owner to confirm; default = keep Attention/MRI reachable as co-primary top-center view (see `contradictions.md`).

- **Conflict:** UI_SCREEN_INVENTORY / RELEASE_1_UI_SPEC still list "Recommendation Workspace" vs ratified Panel Model (Decision 001).
  - Sources: stale UI inventory vs Decision 001.
  - Recommended resolution: Normalize inventory to Panel Model (owner doc task, not a prototype change).

## Ignored Engineering Noise

- **Source:** Governance V2 proposals, decision-log entry drafts (DL-058/060), CODEOWNERS, dev-readiness monitors/feed, ratification packets, reconciliation changesets.
  - Ignored content: risk-tiered routing, PR dispositions, CI doc-integrity gates, repo zone governance, build sequencing.
  - Reason: release/execution/governance mechanics — not user-visible product behavior.
  - Product implication: none directly; tier rules and calibration remain owner-TBD (do not lock as product values).

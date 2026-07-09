# Issues + Overview — Vertical-Slice Build Brief (engineering hand-off)

**Type:** Engineering hand-off brief (non-canonical). AI-authored analysis; engineering authors the realization and proposes; owner ratifies (ratify ≠ author). Traces every task to ratified canon.
**Date:** 2026-07-09
**For:** the R1 Issues/Overview vertical slices.
**Reference of record (UX):** `product-design/oslo_r1_experience_mockup_v4.html`.

---

## 1. What's ratified (build to these — no assumptions needed)

| Decision | What it fixes | Key points |
|---|---|---|
| **DL-094** | Issue lifecycle | User states: **Open → Addressed → Resolved** (+ Reopened). `Acknowledged` **removed**. *Addressed* = user acted; *Resolved* = **only reanalysis** confirms. Single-action **"Apply this fix"** where OSLO can draft. `validated`/`recommended` are **derived attributes, not status**. |
| **DL-095** | User-facing label | Users see **"Issues"** everywhere; **Finding** stays the internal first-class object. One **1:1 Issue-per-Finding** projection (already in `evaluate/engine.py`: `form_issue(f) for f in findings`). "Weakness"/overlay language → "Issues". |
| **DL-096** | Overview surface | Confidence-led redesign: focal score, three CAF **maturity bars** with band words + hover, quiet change-delta trend, **Why** disclosure; ring / green "your change" box / Current-From OSLO pills **removed**. Aligned **Start here / Progress / More** (one grammar; amber = action/attention, green = good state, neutral maturity ramp). |
| **DL-098** (supersedes DL-097) | CAF dimension bands | Dimensions use the **DL-086 5-band scheme** — **Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100** — the same unit as Confidence. **No separate thresholds** (DL-086 owns the edges + ±3 guard). |
| **DL-086** | CAF/Confidence scoring | Per-dimension 0–100 (baseline − impact), power-mean aggregate (`p=−0.5`, `ε=5`), reliability qualifier (non-arithmetic), 5-band. Confidence is **maturity, not probability/health**. Determinism **±7 / same-band**. |

**No open owner-decision items block these slices.** The one former open item (CAF band thresholds) is closed by DL-098 → DL-086.

## 2. Slices (vertical: DB → backend → UI, each demoable + testable)

**Slice A — Issues (terminology + lifecycle).**
- Relabel user-facing surfaces Findings/weakness → **Issues** (route through the 1:1 Issue projection; do **not** rename the Finding object). Finding Panel → Issue detail.
- Lifecycle: collapse backend `finding_commands` `:acknowledge` + `:address` into a single `:address` (`detected → addressed`); keep `:reopen`; resolution stays reanalysis-driven. Update `Finding.status` enum; migrate persisted `acknowledged`/`validated`/`recommended` → `open` (lossless w.r.t. user action). `validated`/`recommended` become derived attributes (run-lineage / finding↔recommendation coupling), not status.
- Single-action "Apply this fix" where a `SuggestedFix` draft exists; "Write my own fix" fallback.

**Slice B — Overview surface.**
- Confidence panel per v4: focal score + band (5-band, DL-086); reliability one-liner; three CAF **bars** with the 5-band word per dimension + hover detail; amber flag on the lowest; quiet change-delta trend; **Why** disclosure (auto-open once after a *material user-initiated* change, then collapse/sunset — not on every Deep Pass recompute).
- Surface per-dimension CAF **0–100 score + band** (CAF-01 supplies the score; DL-086 bands it).
- Aligned Start here / Progress / More (eyebrow + descriptor, dot-label chips, neutral tracks, amber = action, green = good state).
- Staleness: show a "previous analysis — reanalyzing" marker **only when not current** (no persistent Current pill).

## 3. Build order + guardrails

- **Backend/contracts first** against ratified canon (lifecycle enum, Issue projection, CAF score→band per DL-086), **UI last against v4** — so the UI isn't built twice.
- Every UI surface must pass the **visual-regression harness** (`30_engineering/visual_regression/`, baselines from v4) + `ACCEPTANCE_CRITERIA.md`; behavioral invariants via `behavioral.mjs` (Confidence never bare, reliability in the explainer, quick-tour steps resolve).
- Governance: **engineering proposes realization, owner ratifies**; changes land on branch → PR → green gate → owner merge; never push to main.
- Contracts/traceability: bind each surface element to the State/Event/API model via `20_handoff/traceability/R1_UI_BACKEND_INTEGRATION_MAP.md`.

## 4. Spec references

- UX: `product-design/oslo_r1_experience_mockup_v4.html`; `10_product/experience/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md`; `FINDING_PRESENTATION_SPECIFICATION_V1.md`.
- Lifecycle/label: DL-094, DL-095 (records); `FINDING_SYSTEM_SPECIFICATION_V1 §C` + `Finding.status` enum.
- Scoring/bands: `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (DL-086); DL-098 record.
- Verification: `30_engineering/visual_regression/` (harness + acceptance criteria).

## 5. Anti-assumption note

All numeric CAF/Confidence values (impact table, `p`, `ε`, band edges, determinism tolerance) are **DL-086 R1-provisional — refine from telemetry**, structure fixed. Do not re-pick them. If a spec gap appears, **escalate — do not infer** (`00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md`).

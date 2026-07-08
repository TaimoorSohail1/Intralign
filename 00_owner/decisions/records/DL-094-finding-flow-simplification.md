# DL-094 — Finding flow simplification: no-Acknowledge lifecycle + single-action resolution (RB-035)

- **Date:** 2026-07-08 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner-directed R1 UX refinement (PR #116; reconfirmed 2026-07-07). Proposal: `00_owner/decisions/PROPOSAL_FINDING_FLOW_SIMPLIFICATION_DRAFT.md` (RB-035; Framework 001A Review complete). Exploration: `90_research/design_artifacts/oslo_r1_proposed_findings_lifecycle.html`. Grounded in `FINDING_SYSTEM_SPECIFICATION_V1 §C`, `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001` (only reanalysis changes the assessment), State Model §10 / Data Model finding-status enum.
- **Layer:** `10_product/domain` (finding lifecycle + enum) with `10_product/experience` (Finding/Issue panel + presentation) realization. No doctrine or constitution change.

## Decision (ratifiable text — D1, D2, D3; **owner adopted all three, 2026-07-07**)

**D1 — Collapse the lifecycle: drop `acknowledged`.**
New lifecycle: **`detected/open → addressed → closed`**; `closed → reopened`; `{detected, addressed} → superseded`. The `acknowledged` state (a user "accepting a finding as real") records sentiment with **no effect on the assessment**, contrary to the canonical rule that **only reanalysis changes the assessment** — it is epistemically inert. Removing it preserves every invariant: closure still passes through `addressed` (detected→closed remains invalid); **closure is still only by reanalysis** — a user marking *addressed* never closes; findings stay descriptive and append-only.

**D2 — Single-action resolution (where OSLO can draft).**
Collapse "choose approach → apply to plan" into one confirm — **"Apply this fix"** — that applies OSLO's drafted change and triggers reanalysis. The click is the user's confirmation of the plan change; **reanalysis, not the click, closes** the finding. Applies where OSLO carries a draftable fix; a **"Write my own fix"** path is always available (two-step remains where OSLO cannot draft).

## Conditions

- **Preserve the addressed → closed boundary.** *Addressed* = the user acted; *Closed/Resolved* = reanalysis confirmed. The user's action never directly closes an item — only evidence/reanalysis does. This is the load-bearing epistemic invariant and is **not** collapsed.
- **Enum reconciliation is a required realization step (C2).** The finding-status enum is `detected/validated/recommended/addressed/resolved/reopened`; removing `acknowledged` requires amending the State Model + Data Model enum, not just `§C`. Persisted `acknowledged` findings map losslessly to `open`.
- **D3 — Retire `validated` and `recommended` from the status lifecycle (owner ruling, 2026-07-07).** These were never mutually-exclusive lifecycle phases: a finding stays *validated* after it is addressed, and keeps its recommendation after it is resolved — they coexist with the action status rather than replacing it, which is the root of the State-Model↔enum conflict. They are therefore modeled as **derived attributes, not status**:
  - **`validated`** → a derived confirmation property read from **analysis-run lineage** (`first_seen_run_id` / the confirming run); if surfaced to users at all, it rides the existing **Initial/Extended Analysis + confidence-stage** presentation, never the issue's action-status.
  - **`recommended`** → the existing **finding↔recommendation coupling** ("does this issue have a recommended fix?") — a relationship/join, not a state (modeling it as status invites drift when a recommendation is withdrawn).
  - Resulting user-facing status is exactly **`open → addressed → resolved`** (+ reopened, + superseded). Persisted `validated`/`recommended` migrate to `open` (lossless w.r.t. user action), as with `acknowledged`. This is a fuller enum cleanup than D1 alone and resolves the debt the State Model Spec already flagged.
- Coupling check: `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1 §3` keys on `closed`/`superseded`, not `acknowledged` — confirm unaffected. Acceptance subsystem (Wave U) is decoupled from finding.status — confirmed in the RB-035 Review.

## Realization (landed with the decision)

Amend `FINDING_SYSTEM_SPECIFICATION_V1 §C` (state table + transitions); amend the State Model §10 / Data Model finding-status enum (note persistence migration); update `FINDING_PANEL_SPECIFICATION_V1` / `FINDING_PRESENTATION_SPECIFICATION_V1` (no Acknowledge; single-action Apply); collapse the backend `finding_commands` `:acknowledge` + `:address` into a single `:address` transition (detected→addressed), keep `:reopen`. Realization timing per owner (RB-035 recommends Release 2; the R1 vertical-slice plan may pull it forward — owner's call).

## Supersedes / Amends

Amends `FINDING_SYSTEM_SPECIFICATION_V1 §C`, the State/Data Model finding-status enum, and the Finding panel/presentation specs. Reconciles the pre-existing State-Model↔Data-Model enum divergence already flagged in the State Model Spec. No doctrine or constitution superseded; epistemic invariants (addressed-before-closed; reanalysis-only closure; append-only) preserved.

## Pairing

Recommend ratifying and realizing **with RB-036** (Findings→Issues user-facing label) — both touch the Issue surface; the user-facing lifecycle shown on an "Issue" is exactly this lifecycle.

## Provenance

Owner-directed exploration (PR #116), reconfirmed in the 2026-07-07 working session. AI surveyed canon, confirmed the change strengthens (does not weaken) the epistemic model, produced the Framework 001A Review (in the RB-035 proposal), and drafted this record — surfacing the `validated`/`recommended` reconciliation, which the **owner ruled on 2026-07-07 (D3 — retire from the status lifecycle).** **AI drafted and recommended; the owner ratifies.** Number assigned at landing (DL-065); effect on canon at owner merge.

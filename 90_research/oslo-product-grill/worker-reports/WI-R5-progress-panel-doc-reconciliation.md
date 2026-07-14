# WI-R5 — Slice-10 doc reconciliation to the DL-111 foundation bar — WORKER REPORT

**Status:** ✅ COMPLETE · **Date:** 2026-07-14 · **Slice:** 10 (Overview / Progress panel) · **Decision:** DL-111

## Task
Reconcile the slice-10 product docs from the OLD Progress **class-ledger** ("From OSLO N · Confirmed by you M" sentence row + "load-bearing / your read rests on" row) to the ratified **foundation-bar** design (DL-111), surgically — Progress/Overview descriptions only.

## Reconciled (6 docs)
- **frontend-ui.md** — the panel's authoritative layout: DL-109 §1 ledger ASCII → foundation-bar schematic (hero grounded-facts, proportional Confirmed-by-you + From-OSLO segments, hatched provisional tail, legend); D194 "panel as it renders" ASCII + markup → the `.pgx` foundation bar; tokens → cool-blue accent on attested (echoes the Confidence ramp), red scoped to Critical, orange on links only; guard note (structure guards D194a/d retired, single-source D194b/c survive).
- **user-experience.md** — D194a/c/d + D196 quotes and the canonical "Progress panel" section rebuilt to the foundation bar; incommensurable-populations argument preserved (solid bar = comparison, provisional tail = subset).
- **success-criteria.md** — C-DL109-1, C-D183-4, C-D186-1, C-D194-1/2/4/5/9, C-D196-3, C-D197-1/4 updated to assert foundation-bar behavior (hero = attested+derived computed; segments = real counts; red only on Critical; neutral deltas; single-source labels).
- **e2e-test-scenarios.md** — T-DL109-1/2/3 rewritten to the bar (hero + segments; tail "inferences your read leans on"; grounding-moves-counts relabeled).
- **edge-cases.md** — D194 section header note + E-D194-1/6, E-D196-8 current-state fixes (historical defect log otherwise preserved as evolution history).
- **open-items.md** — O-D186-2, O-D194-1, O-D197-1 annotated with DL-111 outcomes (owner escalations not unilaterally closed).

## Unchanged (3 docs — no Progress-panel layout content)
product-detail.md · product-data.md · workflow.md (their grounded/inference matches are the Readout, the data model, and the Inference-map computation — untouched).

## Scope confirmation
NOT modified: the **Inference Map** (countable pips / "N grounded · M inferred" intact), the **Outcome Confidence maturity ramp**, Reports, Tiering, Plans, Chat, Memo, budget/limits. Exact copy taken verbatim from the live prototype.

## Verification
Prototype source of truth: `slice10 prototype.html` (foundation bar; **135/135 self-check, 0 pageerrors**, dark+light; ratified DL-111). Reconciled docs committed to device (md5-verified) and their sizes grew only marginally (surgical): frontend-ui 168,854→172,805 · user-experience 103,807→105,166 · success-criteria 122,192→123,438 · e2e 49,618→49,958 · edge-cases 229,389→230,359 · open-items 137,645→138,773.

## Re-signoff
Awaiting owner re-signoff of the **Slice-10 Overview/Progress** portion (WI-R5).

---

## ADDENDUM — 2026-07-14 — P1 ERRATUM (owner defect report)

Owner caught three semantic defects in the ratified bar; the prototype and the six docs were corrected (Decision 251):
1. **Hero = grounded/attested only** (was attested+derived; 12 of 29 were evidence_id-null). 2. **Two provenance states** — "Derived — supported" deleted; "From OSLO" is the inferred (hatched) state. 3. **Load-bearing is a superset line**, not a `+`-joined bar tail (inferred claims ⊂ inferred items of every type).
New **population guards**: `_assertPgxTwoProvenanceStates` added; `_assertPgxBarIsComputedFromRealCounts` now requires hero == grounded (RED on a+d); `_assertPgxBarStructure` forbids load-bearing inside the bar / any `+`. Prototype **R6: 136/136, 0 pageerrors**, both themes. Docs re-reconciled (same 6 files, 0 residual uncorrected language). Canon erratum to DL-111 drafted (`DL-PENDING-progress-panel-erratum-BODY.md`), awaiting owner land.

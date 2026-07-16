# DL-114 — A finding/statement impacts a set of CAF dimensions — data-model conformance + by-dimension inference

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — A finding/statement impacts a SET of CAF dimensions (data-model conformance to CAF_ASSESSMENT_MODEL_V1)

**Class:** A (data-model + surfacing conformance) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-14 · Grill record: **Enhancement #2, Phase 1**. Review basis: `caf-dimension-reconciliation-review.md`.

## Problem
`CAF_ASSESSMENT_MODEL_V1` §3 (Founder Position #2) states the three dimensions are **independent assessment targets** and **a single finding may impact one or more dimensions simultaneously**; §8.3 / §9 state a finding's affected dimensions are established by **Impact Assessment**, **not** predetermined by finding type. The implementation stored a **single scalar dimension** per Issue and per ContextItem — so a finding could touch only one dimension and occupied exactly one Attention-Map cell. That is a narrowing of ratified canon (Review findings F2, F3).

## Decision (recommended — owner ratifies)
A finding/ContextItem's CAF dimension attribute becomes a **set** of one or more of {Clarity, Alignment, Feasibility}, established by Impact Assessment. Concretely:
- **Data model:** the scalar `dim` is superseded by a dimension **set** (`dims`). A single-dimension finding is the degenerate case (a set of one). Access is single-sourced through **`_dimsOf(x)`** (returns the set; falls back to the scalar for back-compat).
- **Attention Map:** the grid is unchanged (7 artifacts × 3 dimensions = 21 cells), but **issue→cell is many-to-many** — a multi-dimension finding lights **each** of its `{artifact × dimension}` cells. `openFindingsFor(artifact, dimension)` selects by `_dimsOf(issue).includes(dimension)`.
- **Derived reads:** the limiting dimension, the CAF bands, load-bearing, and per-dimension statement tallies count a finding/item toward **each** of its dimensions. All remain computed from state; CAF still renders as **bands, not percentages** (D176b); severity color stays on cells only.
- **Display:** the Issue Panel header and lists show all impacted dimensions ("Feasibility · Alignment"); the "By dimension" grouping lists a multi-dimension finding under **each** of its dimensions.
- **Demo (illustrative):** **ISS-07** ("Sponsor funding closes after the costs are committed", critical) now impacts **Feasibility + Alignment** — a sequencing conflict incoherent in time (Alignment) that threatens achievability (Feasibility) — appearing in Schedule × Feasibility **and** Schedule × Alignment. Supporting item CI-64 likewise.

## Scope boundary (explicitly NOT in this decision)
- **Widening Alignment's content criteria** to the full canonical "coherence between project elements and intended outcomes" (Review F1) — **Phase 2**.
- The **dimensional Inference Map** (grounded-vs-inferred by dimension) — **Phase 3**.
- The **7-vs-9 Confidence-driver inconsistency** in canon (Review F5) — a separate owner-escalated canon-hygiene item; not resolved here.

## Conformance basis
`CAF_ASSESSMENT_MODEL_V1` §3 (independent dimensions; a finding may impact one or more), §8.3 (finding type does not predetermine dimension), §9 (Impact Assessment determines affected dimensions). **No canonical definition is changed** — this brings the implementation into conformance with already-ratified canon.

## Guard (executable — boot `window._S10`)
`_assertFindingCanImpactMultipleDimensions` (aggregate key `findingImpactsManyDims`): proves `_dimsOf` returns arrays, ≥1 live finding is multi-dimension, that finding resolves to >1 Attention cell, and the single-dimension floor still holds (exactly one cell). Live self-check: **140/140, 0 pageerrors**, both themes.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). The data-model shape (`dim` → `dims`) and the Attention-Map cardinality are product-authored spec touches (Data Model, MRI/Attention spec) proposed for owner ratification. Slices 4 & 10 reopened; re-signoff required. AI recommends; only the owner ratifies.

## Provenance
Owner thread 2026-07-14 (progress-panel grounding → CAF criteria → "be really clear on the criteria"); authoritative canon read from the newly-connected `~/GitHub/oslo-knowledge-base` (`10_product/domain/CAF_ASSESSMENT_MODEL_V1.md`). Review drafted (`caf-dimension-reconciliation-review.md`); owner directed "proceed with recommendation" → Phase 1 built and verified. AI implemented; owner ratifies.

### Sources
- [CAF_ASSESSMENT_MODEL_V1.md](computer:///Users/macuser/GitHub/oslo-knowledge-base/10_product/domain/CAF_ASSESSMENT_MODEL_V1.md) — §3, §8.3, §9.

---

## ADDENDUM — Phase 3: the Inference Map cuts by dimension (2026-07-15)

Enabled by this decision (a finding/statement bears on a SET of dimensions), the existing **Inference Map** — which surfaced grounded-vs-inferred **by artifact** (DL-109; "where is OSLO guessing?") — gains a **by-dimension** cut: grounded-vs-inferred across **Clarity · Alignment · Feasibility**, counting each statement toward every dimension in `_dimsOf(it)`. Neutral treatment (guessing is not a failure state — `_assertInferenceMapIsNeutral` holds), within the **AE-06** boundary (reads existing ContextItem state; no accumulated "debt" aggregate, no new object).

Conforms to CAF_ASSESSMENT_MODEL_V1 **§6** (*inference is a characteristic of understanding, not a dimension*) — the map reports the inference **characteristic** cut across the three assessment targets, not a new dimension. It makes explicit what an aggregate grounding count hid — e.g. **Feasibility 0 of 10 grounded** (rests entirely on OSLO's inference) — the exact concern that opened this reconciliation.

Realized by `_ciDimInferenceStats()` / `_infDimHTML()` / container `#inf-dim`, guarded by `_assertInferenceMapCutsByDimension` (`window._S10` = **142/142**, 0 pageerrors). Owner ratifies with the rest of this note.

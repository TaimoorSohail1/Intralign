# Phase IV — Wave C: Advisory (Advise)

**Sequence:** After Phase III. · **Status:** Not started · **Owner gate:** required before Phase V.
**Contracts:** `IC/QA/OBS-WC-ADVISE` (`03_architecture/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`, Wave C section).

## Goal
Generate **advice** — Recommendations and Clarification Requests anchored to Findings/Issues — as governable candidate *responses*. Advise proposes; it never accepts, governs, or executes. This is the layer that turns understanding into "here's what you might do."

## Scope
- **`IC-WC-ADVISE`** — Recommendation (+ Suggested-Action / Candidate-Improvement types) and Clarification Request; each anchored to a Finding/Issue. **Resolution Paths are a presentation-only substructure of a Recommendation — no standalone Resolution-Path object.**

## Depends on
Phase III (Findings/Issues to anchor to) and Phase II (recompute appends CHRs for advisory emissions too).

## Expected outcomes (definition of done)
- ✅ Recommendations are generated **only in the context of a Finding** (Recommendation-only-in-Finding-context invariant), each traceable to its anchor.
- ✅ Clarification Requests generate where understanding is insufficient.
- ✅ Resolution Paths appear as a **substructure** of a Recommendation, **not** as a separate object (negative test rejects a standalone Resolution-Path object).
- ✅ Advise **never** accepts, governs, executes, or self-authorizes (negative tests reject each).
- ✅ Recommendations are **Derived** and recomputable; a recompute appends a new CHR; recommendations never exact-replay (semantic equivalence is the bar).

## Invariants enforced
Only **Advise** generates candidate responses (Authority generates nothing); Recommendation only in Finding context; Resolution-Paths presentation-only; Advise never accepts/governs/executes; cognition Derived + recomputable.

## Testing focus
Governance-adjacent negatives are central here: prove Advise cannot accept/govern/execute and cannot emit a standalone Resolution-Path object. Semantic-equivalence replay for recommendation text.

## Exit gate (owner-approved before Phase V)
OSLO advises with Finding-anchored, governable candidate recommendations and clarifications; the "advise proposes, never disposes" boundary is proven by passing negative tests.

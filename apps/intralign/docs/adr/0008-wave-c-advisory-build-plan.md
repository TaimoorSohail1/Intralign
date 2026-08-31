# Wave C (Advise) is two slices behind the existing chain seam; Advise generates, the user disposes

Phase IV / Wave C contracts `IC/QA/OBS-WC-ADVISE`: Advise is the single producer of
**Recommendation** (Suggested-Action / Candidate-Improvement types) and **Clarification
Request**, each anchored to a Finding/Issue, all **Derived** — "advise proposes, never
disposes." Per the Phase IV plan's DL-047 additions, Wave C also generates **Suggested Fixes
(REC-04)** and **Validation Recommendations (REC-05)**. This ADR records how that lands in
`code/`; the contracts + DL-043/047/055 are the governing source.

Like Wave B, the change is **injection behind the frozen chain seam** — the `deep_pass` graph
already has a `stage_advise` node and `CHAIN_STAGE_ORDER` already ends in `advise`; Wave C
replaces `wave_c_placeholder_advise` via `register_stage("advise", …)` and extends the
`orchestration/wave_b.py` composition pattern (a `wave_c.py` that composes infer→evaluate→
advise, or extends the Wave B chain). No graph-topology change. CHR-append follows the
DTM-0013 model contract exactly (construct `CognitionHistoryRecord`, never a dict).

**Two slices** (one fresh worker each, reviewed before the next):
- **DTM-0014 — Recommendation + Clarification (core IC-WC-ADVISE):** the Recommendation Engine
  (Finding/Issue-anchored, multiple alternatives = multiple Recommendations) + Clarification
  Engine; `Recommendation`/`ClarificationRequest` types; `EVENT_NAMES_WC_ADVISE`; the advise
  stage; the governance-adjacent negatives (no accept/govern/execute/self-accept; no standalone
  Resolution-Path object; Recommendation-only-in-Finding-context).
- **DTM-0015 — Suggested Fix (REC-04) + Validation Recommendation (REC-05):** Advise generates
  the `SuggestedFix` candidate (anchored to a Finding, Derived, CHR-appended) and the Validation
  Recommendation type. **The Critical negative is the headline: OSLO never autonomously writes a
  fix** — application is a user-initiated artifact edit that triggers recompute (the apply
  surface + daily-cap MON are commodity / Wave I, not built here).

## Status

accepted — locked from docs (Phase IV plan + WAVE_C contract + DL-047/055), 2026-06-18.
**Coding gated on the Wave B owner exit-gate + per-wave authorization (DL-044) + readiness gate.**

## Considered Options

- **One slice (all four output types together)** — rejected: bundles the Critical autonomous-write
  negative (SuggestedFix) with the core Recommendation engine; a larger, harder-to-review diff.
- **Defer SuggestedFix/Validation entirely to Wave I** — rejected: the Phase IV plan lists REC-04/
  REC-05 as Wave C DL-047 additions (Advise *generates* them); only their *application* is Wave I.
- **Two slices, generation in Wave C (chosen)** — clean contract→slice traceability; isolates the
  autonomous-write negative; matches the Wave B discipline.

## Consequences

- **No new migration:** CHR `output_kind` already includes `recommendation` + `clarification`
  (the 14-value Literal/CHECK); `SuggestedFix`/`Validation` ride the `recommendation` kind or a
  payload discriminator — a *new* output_kind would be a STOP/owner-approval (don't add one
  silently).
- **Recommendation state is the user's, not Advise's:** per DL-055, Advise emits a Recommendation
  in the `Generated` state only; `Accept/Defer/Reject/Apply` are user actions recorded by **Wave U**
  (not Wave C); "Modify" → supersession (recompute); "Discuss"/"Share For Review" are collaboration
  affordances, not states. Wave C must not implement acceptance.
- **Advise uses the LLM** (recommendations are AI-text → semantic determinism), so `RoutingStage`
  gains an `"advise"` stage and `TierRouting` an `advise` ref (internal Gemma primary, DL-069);
  recorded-fixture CI (ADR-0004) is unchanged — recommendations replay *semantically*, never exact.
- **Resolution Paths stay presentation-only** — multiple Recommendations rendered as paths; a
  standalone Resolution-Path object is a rejected negative (Major).
- **Reversible:** the advise stage is injected; reverting to the placeholder is a registry change.
- Detailed slice scope/tests live in `code/docs/deep-tasks/wavec-advisory-deep-task/` (authored at
  build time).

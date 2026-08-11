# Canon — the "why" behind every locked decision

The slices tell you *what* to build; the canon tells you *why it must be that way*. Before overriding any locked decision in a slice, trace it here — most "surely it should just…" instincts are the exact wrong-default a ratified decision exists to prevent.

## `decisions/` — the ratified decision log

The `DL-*` (decision-log) and `DR-*` (decision-ratification) documents. These are canonical and load-bearing; a slice's "Source" column points into them.

| Doc | What it ratifies |
|---|---|
| `DL-172_FREEMIUM_VALUE_MOMENTS_OUTCOME_UNIT.md` | Outcome as the metered unit; freemium value moments (renumbered DL-198 in later refs) |
| `DL-184_R2_GRAPH_SCHEMA_RATIFICATION.md` | The R2 product data-concept schema |
| `DL-193_PRIORITY_REANCHOR_outcome-integrity.md` | Outcome integrity = CAF × Grounding × Adaptability; exposure priority |
| `DL-194_OUTCOME_INTEGRITY_INDICATOR_roadmap.md` | The composite indicator; State 1 (moment-in-time) as committed R2 scope |
| `DL-195_STEERABILITY_checkpoint-assessment.md` | Adaptability pillar; weakest-gates + foundation-first tie-break; 5-step Fragile→Sound bands |
| `DL-196_INTEGRITY_VIA_ISSUE_LAYER.md` | The single exposure-gated issue layer all three pillars resolve through |
| `DL-197_FALSE_CONFIDENCE_ISSUE_TYPE.md` | The Grounding false-confidence issue type (`ISS-FC-<art>`), one-door resolution |
| `DL-200-205_R2_RESOLVE_FIRST_DECISIONS.md` | DL-200–205 + the DR-1…7 resolve-first rulings (incl. DR-6 activation=2nd act) |
| `DR-7_PRICING_RATIFICATION.md` | Basic $29/mo flat; Pro $79 provisional |
| `R2_DL_READJUDICATION_WORKSHEET.md` | The ratified re-adjudication of DL-164…197 — the master verdict sheet |

## `audits/` — the analyses that produced the slices

The working audits and build plans. Not canonical rulings, but the reasoning that the slices distill. Read these when a slice's "R1 reuse vs net-new" or a landmine (DL-L*) needs its full context.

- `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md` — the §4 gap register (R2-*) + §3 landmines (DL-L1…L9) + §8 slice seeds the slices are built from. **The keystone audit.**
- `OSLO_BACKEND_CAPABILITIES.md` — the capability list (#1…#18) the slices cite.
- `OSLO_EXPORT_OBJECTIVE_AUDIT_2026-08-05.md` — the export-flow audit behind Slice 7.
- `R2_FREEMIUM_COMPLETION_CHECKLIST.md` — the freemium gap checklist behind Slice 4.
- `R2_RESOLVE_FIRST_DECISION_BRIEF.md` — the resolve-first decision brief (enforcement = enforce, DR-3/DL-202).
- `R2_STATE1_BUILD_PLAN.md` — the State-1 Phase-A engine build plan (behind Slice 1 + the prototype corrections).

## `product/` — R2 product references

Cross-cutting product docs the slices assume.

- `OSLO_R2_DELTA_SLICE_MAP_2026-08-06.md` — the approved nine-slice map.
- `OSLO_R2_INGESTION_LATENCY_AND_LIMIT_ENFORCEMENT_INSTRUCTIONS_2026-08-05.md` — the Fast/Deep two-pass + L1a output contract + content-metered ingest (behind Slice 3 + Slice 4).
- `OSLO_R2_OPEN_QUESTIONS_RATIFIED_2026-08-06.md` — the nine settled open questions.
- `OSLO_R2_PROTOTYPE_TECHDEBT_DISPOSITIONS_2026-08-06.md` — the tech-debt dispositions (what was fixed in the prototype vs deferred to Phase A).
- `OSLO_R2_BUILD_READINESS_2026-08-06.md` — the build-readiness assessment.

## Tracing a decision

Each slice doc's §1 "Locked decisions" table has a **Source** column (e.g. `DL-195 §6`, `DR-7`, `audit R2-I2`). To check why a rule is what it is: open the cited doc in `decisions/` or `audits/`, find the section. If you believe a locked decision is wrong, that is an owner escalation — not a build-time override — because later slices and the acceptance suite are built on it.

# Architecture V1 Refactor — Change Impact Matrix

**Document:** ARCHITECTURE_V1_REFACTOR_IMPACT_MATRIX.md
**Type:** Per-file change impact matrix (companion to `ARCHITECTURE_V1_REFACTOR_REPORT.md`)
**Date:** 2026-05-31

> Per-file record of governance references found, changes required, changes applied, and future-architecture references preserved. **Reclassification only — no deletion, no model rewrite, no new doctrine.**

---

## Active Architecture V1 — Understanding Domain (8 models)

| File | Governance references found | Changes required | Changes applied | Future-architecture refs preserved |
|---|---|---|---|---|
| CAF_ASSESSMENT_MODEL_V1.md | None (finding types ≠ governance) | None | None | n/a — active V1 |
| CAF_SCORING_MODEL_V1.md | Incidental "CAF Review Requests" (Master Spec feature) | None | None | n/a — active V1 |
| RELIABILITY_MODEL_V1.md | None | None | None | n/a — active V1 |
| CONFIDENCE_MODEL_V1.md | None | None | None | n/a — active V1 |
| MRI_MODEL_V1.md | None | None | None | n/a — active V1 |
| OVERLAY_MODEL_V1.md | None | None | None | n/a — active V1 |
| FINDING_MODEL_V1.md | Incidental "Finding review requests" (future-evolution list) | None | None | Its own future-evolution list preserved |
| RECOMMENDATION_MODEL_V1.md | None | None | None | n/a — active V1 |

---

## Active Architecture V1 — Supporting Service

| File | Governance references found | Changes required | Changes applied | Future-architecture refs preserved |
|---|---|---|---|---|
| NOTIFICATION_MODEL_V1.md | Trigger list names governance objects (Review Request, Disposition, Governance outcomes, Accepted Understanding) — conceptual | None to the model (active-object triggers operative; governance-object triggers dormant) | None (no model change); classification recorded in index + report | Governance triggers preserved in the model's conceptual list for future activation |

---

## Future Architecture — Governance Domain (5 models)

| File | Governance references found | Changes required | Changes applied | Future-architecture refs preserved |
|---|---|---|---|---|
| RESOLUTION_CANDIDATE_MODEL_V1.md | Self-describes as a governance object (whole document) | Reclassify as Future Architecture without rewriting | **Additive banner** after header → "Future Architecture; not active V1; content unchanged" | **All** content preserved verbatim |
| REVIEW_REQUEST_MODEL_V1.md | Self (governance object) | Reclassify only | **Additive banner** | All preserved |
| DISPOSITION_MODEL_V1.md | Self (governance object) | Reclassify only | **Additive banner** | All preserved |
| GOVERNANCE_MODEL_V1.md | Self (governance object) | Reclassify only | **Additive banner** | All preserved |
| ACCEPTED_UNDERSTANDING_MODEL_V1.md | Self (governance output object) | Reclassify only | **Additive banner** | All preserved |

---

## Lineage / Audit / Terminology / Index

| File | Governance references found | Changes required | Changes applied | Future-architecture refs preserved |
|---|---|---|---|---|
| MODEL_LINEAGE_INDEX_V1.md | Presented Governance Domain as active, fully-specified; "two specified domains"; "final output Accepted Understanding"; "no future models remain" | Refactor to Active V1 / Future split; ensure no section implies governance is active V1; reframe Knowledge Layer as non-gated | **Header classification line; §2 Active/Future split block; §5 matrix classification note; §7 reframed to Future Architecture (chain + Human-Evaluation note kept verbatim); §8 governance relabeled Future Architecture + Knowledge-Layer reframed; §9 governance principles marked Future; §10 reframed; Validation reclassified** | Governance lineage chain, governance principles, and all governance model entries preserved (reclassified, not removed) |
| MODEL_COVERAGE_AUDIT_V1.md | Treated Governance Domain as a completed active domain; "the destination of the entire chain — Accepted Understanding" | Reframe maturity/completeness: V1 complete without governance; governance = future; Notification active | **Top reclassification note; §6 Domain Completeness reframed; §9 maturity reframed** | **All findings preserved**; governance described as completed-and-preserved Future Architecture |
| TERMINOLOGY_RECONCILIATION_AUDIT_V1.md | "Accepted/Acceptance," "Governed vs Accepted Understanding," governance "Outcome" collisions | Mark governance terminology Future Scope, off V1 critical path | **Framing note added** | **All findings preserved unchanged** |
| TERMINOLOGY_RECONCILIATION_DECISION_001.md | Three governance decision areas | Mark Future Scope, non-blocking for V1 | **Framing note added** | **Package preserved in full** |
| FOUNDER_TERMINOLOGY_DECISION_WORKBOOK_001.md | Three governance decision areas + blank response template | Mark Future Scope, non-blocking for V1 | **Framing note added** | **Workbook + blank template preserved** |
| OSLO_ARCHITECTURE_V1_SIMPLIFICATION_PLAN.md | Classifies governance as Future Scope already | None (already consistent) | None | Already classified as Future Scope |

---

## Release 1 Product Documents (out of scope — feature, not governance model lineage)

| File | Governance references found | Changes required | Changes applied | Future-architecture refs preserved |
|---|---|---|---|---|
| OSLO_RELEASE_1_MASTER_SPEC.md | "CAF Review Requests" (collaboration **feature**); "governance" generic | None — not the governance model lineage | None | n/a (feature is active V1) |
| OSLO_CAPABILITY_MATRIX_V2.md | "CAF Review Requests" capability | None | None | n/a |
| OSLO_LINEAR_INITIATIVES_V2.md | "CAF Review Requests" initiative | None | None | n/a |
| OSLO_RELEASE_1_DEPENDENCY_GRAPH.md | Feature references | None | None | n/a |
| OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md | Feature references | None | None | n/a |
| OSLO_RELEASE_1_SCOPE_OPTIMIZATION_REVIEW.md | Feature references | None | None | n/a |

---

## Totals

| Metric | Count |
|---|---|
| Files reviewed | 25 (+ 2 new deliverables) |
| Files changed | 10 |
| Governance models reclassified (banner only) | 5 |
| Governance models deleted / deprecated / invalidated / rewritten | 0 |
| Index refactored | 1 |
| Audits/terminology reframed (findings preserved) | 4 |
| Release 1 feature docs changed | 0 (correctly excluded) |
| New doctrine / new models / new workflows introduced | 0 |

*All future-architecture (governance) content is preserved and re-activatable. See `ARCHITECTURE_V1_REFACTOR_REPORT.md` and `ARCHITECTURE_V1_FINAL_CONSISTENCY_AUDIT.md`.*

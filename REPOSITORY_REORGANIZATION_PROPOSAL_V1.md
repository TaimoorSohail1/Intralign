# Repository Reorganization Proposal v1

**Document Type:** Repository Restructure Proposal (plan only — nothing moved) · **Status:** **Proposed · Pending Owner Approval** · **Date:** 2026-06-04
**Scope:** sub-folder the two flat hotspots — `03_architecture/` (44 root files) and `02_product/specs/` (134 files) — for retrieval/management. **Top-level structure is unchanged** (the `01–05` domain split is constitutional per DL-037 and stays). Companion to `REPOSITORY_ARCHITECTURE.md`.

> **Mode:** review gate. This proposes the target layout, the move rules, the reference-update plan, and the judgment calls — **no files are moved**. On approval, execution is a **single dedicated commit** (pure moves + reference fixes, no content change). Per `CLAUDE.md`, owner approves; recorded like DL-037 (tracked, references updated).

---

## 0. Why this is low-risk (the key finding)

A repo-wide scan shows **only 18 full *path-style* references** (`02_product/specs/…md` or `03_architecture/…md`) that would break on a move. The other **~1,442 document references are bare filenames** (`` `FOO_V1.md` ``) — these **do not encode a directory**, so they **survive sub-foldering untouched.** The reference-update burden is therefore **~18 edits**, not 1,400. This is what makes the reorg cheap and safe to do now, before engineering depends on paths.

**Bounded blast radius:** only the two flat hotspots move. **Untouched:** `01_governance/` (doctrine/constitution/decisions — stable, heavily cited), `04_research/`, `05_execution/`, `raw/`, `subsystems/`, and all root files.

---

## 1. Target layout — `03_architecture/` (44 → 6 sub-folders + existing)

Files are assigned by deterministic name rules (so the mapping is reproducible). Counts approximate.

| New folder | Membership rule | Representative members |
|---|---|---|
| `specifications/` | core canonical architecture specs | `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1`, `…RATIFICATION_PACKAGE_V1`, `OSLO_ADVISORY_COGNITION_ARCHITECTURE_SPECIFICATION_V1`, `AI_FIRST_PRODUCT_DELIVERY_ARCHITECTURE_V1` |
| `runtime_models/` | object/behavior/ownership/data models | `RELEASE_1_RUNTIME_OBJECT_MODEL_V1`, `…BEHAVIOR_MODEL_V1`, `…RUNTIME_OWNERSHIP_UPDATE_…`, `…RUNTIME_LAYER_OWNERSHIP_…`, `RELEASE_1_LOGICAL_DATA_MODEL_V1` |
| `contracts/` | contract specs + Wave packages + their conformance reviews | `WAVE_A_…001/001_CONFORMANCE_REVIEW/002/00R`, `WAVE_B_…`, `WAVE_C_AND_U_…`, `WAVE_E_…`, `IMPLEMENTATION_/QA_/RUNTIME_OBSERVABILITY_CONTRACT_SPECIFICATION_V1`, `CONTRACT_GENERATION_FRAMEWORK_V1`, `RELEASE_1_IMPLEMENTATION_CONTRACT_TEMPLATE_V1`, `RELEASE_1_CONTRACT_INVENTORY_V1`, `RELEASE_1_CONTRACT_GENERATION_PLAN_V1` |
| `decisions/` | architecture decisions/analyses (ratified via DL log) | `ACTIVE_ARCHITECTURE_RECONCILIATION_DECISION/RECOMMENDATION_001`, `…INTERPRETATION_ACCEPTANCE_ANALYSIS_001`, `CANONICALIZATION_CONTROL_CHALLENGE_REVIEW_001`, `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`, `DERIVED_COGNITION_LIFECYCLE_DECISION_001`, `USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001`, `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001` |
| `reviews/` | architecture/governance reviews + audits | `AI_FIRST_AUTONOMOUS_DEVELOPMENT_READINESS_AUDIT_V1`, `RELEASE_1_CAPABILITY_COVERAGE_REVIEW_V1`, `GOV_ARCH_001_…REVIEW`, `OSLO_ADVISORY_COGNITION_REVIEW_001`/`…RATIFICATION_REVIEW_002`, `OSLO_ARCHITECTURE_VALIDATION_REVIEW_003`, `OSLO_COGNITIVE_ENGINE_…REVIEW_001`, `…VS_LAYER_…REVIEW_001`, `OSLO_RUNTIME_RECOMMENDATION_OWNERSHIP_REVIEW_001` |
| `environment/` | runtime environment + calibration | `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1`, `RUNTIME_ENVIRONMENT_PROFILE_DL043_RECONCILIATION_001`, `RELEASE_1_CALIBRATION_DEFAULTS_V1` |
| *(keep)* `components/`, `governance_layer/`, `judgement_layer/`, `runtime_architecture/` | existing legacy-layer engineering (re-homed per DL-043) | unchanged; optionally grouped under `legacy_layer_engineering/` |
| *(keep at root)* `README.md` | the directory index | updated to point at the new sub-folders |

## 2. Target layout — `02_product/specs/` (134 → 7 sub-folders)

| New folder | Membership rule | Approx. count |
|---|---|---|
| `ux/` | `*_EXPERIENCE_SPECIFICATION`, `*_PANEL_/_WORKSPACE_SPECIFICATION`, `MRI_*`, `NOTIFICATION_/HISTORY_/EXPORT_/HELP_/INVITE_*`, navigation/dashboard/overview, artifact/onboarding/account/collaboration/chat/companion/journey, `RELEASE_1_UI_SPECIFICATION`, `UI_SCREEN_INVENTORY`, `*_PRESENTATION_SPECIFICATION` | ~40 |
| `models/` | `*_MODEL_V*`, `CAF_*`, `CONFIDENCE_*`, `RELIABILITY_*`, `FINDING_MODEL/SYSTEM`, `RECOMMENDATION_MODEL/SYSTEM`, `OVERLAY/ORIENTATION/DISPOSITION/GOVERNANCE/RESOLUTION/REVIEW_REQUEST/CLARIFICATION/ACCEPTED_UNDERSTANDING`, `PLANNING_INTELLIGENCE`, `OUTCOME_CONFIDENCE_*` stack, `MODEL_LINEAGE_INDEX`, `MODEL_COVERAGE_AUDIT` | ~35 |
| `decisions/` | `*_DECISION_*`, `*_RECONCILIATION_DECISION`, `*_RATIFICATION_DECISION`, `TERMINOLOGY_RECONCILIATION_DECISION`, `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION`, `*_DECISION_WORKBOOK` | ~15 |
| `audits_reviews/` | `*_AUDIT*`, `*_REVIEW*`, `*_ASSESSMENT`, `ARCHITECTURE_V1_*`, `DEEP_ANALYSIS_PASS_*`, `*_SCOPE_GAP_ANALYSIS`, `TERMINOLOGY_RECONCILIATION_AUDIT` | ~18 |
| `data_api_nfr/` | `RELEASE_1_DATA_MODEL_*`, `DATA_MODEL_RECONCILIATION_*`, `*_API_CONTRACT*`, `RELEASE_1_EVENT_/STATE_MODEL`, `RELEASE_1_PERFORMANCE_AND_NFR`, `RELEASE_1_NFR_ACCEPTANCE_MATRIX`, `RELEASE_1_ANALYSIS_ENGINE` | ~14 |
| `testing_fixtures/` | `*_FIXTURE_LIBRARY*`, `*_SUBSYSTEM_TEST_SPECIFICATION`, `RELEASE_1_TESTING_STRATEGY`, `*_CONFIDENCE_SUBSYSTEM_TEST`, `DETERMINISM_CALIBRATION_NOTE` | ~10 |
| `planning/` | `OSLO_RELEASE_1_CANONICAL_SCOPE/MASTER_SPEC/IMPLEMENTATION_PLAN/DEPENDENCY_GRAPH/SCOPE_OPTIMIZATION`, `OSLO_CAPABILITY_MATRIX_V2`, `OSLO_LINEAR_INITIATIVES_V2`, `RELEASE_1_SPECIFICATION_BACKLOG/ROADMAP`, `RELEASE_1_UX_*` (execution/backlog/handoff/plan set), `DEVELOPER_ONBOARDING_PATH`, `DOCUMENT_CONSOLIDATION_PLAN`, `RELEASE_1_DOCUMENTATION_SIMPLIFICATION_REPORT` | ~20 |
| *(keep at root)* `CURRENT_TRUTH.md` | the "read me first" entry point — stays visible at `specs/` root, with a one-line pointer into the new folders | 1 |

## 3. Judgment Calls (please confirm — small list)

1. **Conformance reviews** (`WAVE_A_…001_CONFORMANCE_REVIEW`): proposed in `contracts/` (locality with the package) rather than `reviews/`. *Confirm.*
2. **Architecture `decisions/` location:** keep them in `03_architecture/decisions/` (substantive specs) while the **DL-NNN ledger stays in `01_governance/decisions/`** — they're complementary, not duplicate. *Confirm (recommended).*
3. **Legacy-layer dirs:** keep the four as-is, or nest them under `03_architecture/legacy_layer_engineering/` for clarity. *Pick one (nesting recommended; they're secondary per DL-043).*
4. **`02_product/specs/` `decisions/` vs governance:** product-level decisions stay local in `specs/decisions/`; only canonical DL entries live in `01_governance`. *Confirm.*
5. **`CURRENT_TRUTH.md`** stays at `specs/` root (not moved into `planning/`) so it remains the obvious entry point. *Confirm.*

## 4. Reference-Update Plan (execution step — not now)

- **Path-style references (~18):** the only ones that break. Execution greps `(02_product/specs|03_architecture)/…\.md`, rewrites each to its new sub-path. A precise old→new manifest is generated at execution time.
- **Bare-filename references (~1,442):** **no change needed** — they don't encode directories and resolve by name.
- **Per-directory `README` indexes:** add/refresh a short index in each new sub-folder and at `02_product/specs/` and `03_architecture/` roots (retrieval aid; zero breakage).
- **`REPOSITORY_ARCHITECTURE.md`:** update the "Where Do I Put Things?" table to include the new sub-folders.

## 5. Execution Plan (on approval)

1. Generate the **exhaustive per-file manifest** (every old→new path) from the §1–§2 rules + §3 confirmations.
2. `git mv` each file (preserves history) into its sub-folder — **moves only, no content edits**.
3. Rewrite the **~18 path-style references**; add the README indexes; update `REPOSITORY_ARCHITECTURE.md`.
4. Commit as **one dedicated commit** (`repo: reorganize 02_product/specs and 03_architecture into sub-folders`) — isolated, reviewable, revertible.
5. Record a **changelog entry** (tracked structural change, à la DL-037); no DL ratification needed unless you want one (structure is governance-controlled but content-neutral).
6. **Then** write the Engineering Handoff Package against the clean tree.

## 6. Risks & Mitigations
- **Broken links:** mitigated — only ~18 path refs; all rewritten in the same commit; `git mv` preserves history.
- **Reviewer noise:** mitigated — isolated moves-only commit; diff is renames + 18 ref edits, easy to verify.
- **Drift back to flat:** mitigated — the new convention is documented in `REPOSITORY_ARCHITECTURE.md` + per-dir READMEs so future files land correctly.
- **Timing:** execute **before** engineering clones/builds (cheap window); after that, structural change becomes a heavyweight tracked event.

> ### Proposed Owner Approval
> Approve the target sub-foldering of `03_architecture/` (specifications/runtime_models/contracts/decisions/reviews/environment) and `02_product/specs/` (ux/models/decisions/audits_reviews/data_api_nfr/testing_fixtures/planning), top level unchanged; confirm the five §3 judgment calls; authorize execution as a single moves-only commit with the ~18 path references rewritten and README indexes added, recorded in the changelog. Then proceed to the Engineering Handoff Package against the reorganized tree.

---

*This proposal plans a low-risk sub-foldering of the two flat hotspots — 03_architecture (44 root files into specifications/runtime_models/contracts/decisions/reviews/environment, legacy-layer dirs retained) and 02_product/specs (134 files into ux/models/decisions/audits_reviews/data_api_nfr/testing_fixtures/planning, with CURRENT_TRUTH kept as the root entry point) — leaving the constitutional 01–05 top-level domain split and all of 01_governance/04_research/05_execution untouched. A repo scan establishes the change is cheap: only ~18 full-path references would break (all rewritten at execution), while ~1,442 bare-filename references survive sub-foldering unchanged. It specifies deterministic membership rules, five judgment calls for owner confirmation (conformance-review placement, architecture-decisions-vs-DL-ledger separation, legacy-dir nesting, product-decisions locality, CURRENT_TRUTH placement), a reference-update plan, and an execution plan as a single moves-only git-mv commit with README indexes and a changelog entry recorded like DL-037, sequenced before the Engineering Handoff Package so the handoff map is drawn on the final tree. Nothing is moved by this document; it is routed to the owner for approval.*

**Repository Reorganization Proposal v1 — plan only. Pending Owner Approval.**

# Repository Restructure — Current → Target Migration Map (DRAFT)

**Status:** **DRAFT · plan only — nothing moved** · **Date:** 2026-06-08 · companion to `PROPOSAL_PRODUCT_ENGINEERING_OWNERSHIP_MODEL_DRAFT.md`.
Target zones: `00_owner / 10_product / 20_handoff / 30_engineering / 90_research`. ⚠ = genuine judgment call (owner to confirm). **SPLIT** = folder contains both product and engineering content and must be divided, not moved intact.

## Top-level mapping

| Current | → Target zone | Notes |
|---|---|---|
| `01_governance/doctrine/` | `00_owner/doctrine/` | Amendment 2 — owner canon |
| `01_governance/constitution/` | `00_owner/constitution/` | owner canon |
| `01_governance/frameworks/` | `00_owner/frameworks/` | governance procedure |
| `01_governance/decisions/` | `00_owner/decisions/` | ratified decisions + dispositions |
| `01_governance/canonical_definitions/` | `00_owner/canonical_definitions/` | ⚠ glossary authority — owner-governed |
| `01_governance/ontology/` | `00_owner/ontology/` | ⚠ owner-governed vocabulary |
| `01_governance/manifest/` | `00_owner/manifest/` | charter |
| `01_governance/changelog/` | `00_owner/changelog/` | ledger |
| `01_governance/audits/` | `00_owner/audits/` | ⚠ or a governance/quality area |
| `01_governance/backlog/` | `00_owner/backlog/` | ⚠ revision backlog (owner-directed) vs product backlog (→10) — keep governance backlog here |
| `01_governance/protocols/` | `00_owner/` | Anti-Assumption etc. (governance) |
| `01_governance/{QA,Observability,Deployment}_GOVERNANCE_*`, `AUTONOMOUS_IMPLEMENTATION_CONTROL_*`, `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_*` (+ AI-First delivery rules) | **`00_owner/build_governance/`** | **Owner-ratified build policy** (Amendment 5 / owner-constraint clause). Binds engineering; engineering may *propose* edits, owner *ratifies*. Preserves the owner's right to prescribe *how* OSLO is built. |
| `02_product/{plg,tiering,collaboration,user_experience,workflows}/` | `10_product/strategy/` (+ experience) | product |
| `02_product/specs/planning/` | `10_product/scope/` + `/strategy/` | vision/positioning→strategy; master spec/capability matrix/backlog→scope |
| `02_product/specs/ux/` | `10_product/experience/` | journeys, surface behavior |
| `02_product/specs/models/` | `10_product/domain/` | ⚠ CAF/Confidence *meaning* = product; any realization detail → 30 |
| `02_product/specs/data_api_nfr/` | **SPLIT** | NFR targets→`10_product/acceptance`; API/event-state→`20_handoff/interfaces`; data schema→`30_engineering/data` |
| `02_product/specs/telemetry/` | **SPLIT** | analytics/economics *intent*→`10_product`; observability *realization*→`30_engineering`; event contract→`20_handoff` |
| `02_product/specs/testing_fixtures/` | `30_engineering/qa/` | test strategy/fixtures |
| `02_product/specs/audits_reviews/` | `00_owner/audits/` | ⚠ product audits |
| `02_product/specs/decisions/` | `00_owner/decisions/` | consolidate decisions in owner zone |
| `02_product/specs/FAST_DEEP_WORKFLOW_PACK/` | `30_engineering/analysis_engine/` | fast/deep stage I/O, rule-vs-LLM |
| `02_product/specs/CURRENT_TRUTH.md` | `90_research/` or `00_owner` | ⚠ confirm role (pointer/secondary) |
| `03_architecture/specifications/` | `30_engineering/architecture/` | cognitive-responsibility arch |
| `03_architecture/runtime_models/` | **SPLIT** | object/behavior→`30_engineering/architecture`; logical+physical data→`30_engineering/data` |
| `03_architecture/contracts/` | `20_handoff/contracts/` | the seam |
| `03_architecture/environment/` | `30_engineering/environment/` | runtime profile, calibration, stack |
| `03_architecture/engineering/` | `30_engineering/delivery/` (+ code starter kit) | starter kit, coding constraints |
| `03_architecture/decisions/` | `00_owner/decisions/` | architecture decisions (ratified via DL) |
| `03_architecture/reviews/` | `30_engineering/` reviews | ⚠ eng review trail (or 00 if decision-grade) |
| `03_architecture/RELEASE_1_ENGINEERING_{HANDOFF,ONBOARDING}_*` | `30_engineering/delivery/` | onboarding/handoff |
| `05_execution/implementation/` + `implementation_tracking/` | `30_engineering/delivery/` | phase plans, sequencing, tracking |
| `04_research/`, `raw/` | `90_research/` | non-canonical |
| `subsystems/` | `00_owner/` (or its own) | ⚠ declares doctrinal scope → owner-governed |

## Root files

| Current | → | Notes |
|---|---|---|
| `RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` | `20_handoff/traceability/` | capability→contract→test→event = the seam |
| `OPEN_TBD_REGISTER.md`, `OWNER_DECISION_QUEUE.md` | `00_owner/` | owner decision surfaces |
| `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` | `00_owner/` | governs how eng builds (owner canon) |
| `CANONICAL_GLOSSARY.md` | `00_owner/` | ⚠ drift-control vocabulary (product references it) |
| `README.md`, `START_HERE.md`, `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md` | **ROOT (keep)** | navigation/orientation — not a zone; **update contents** to the new map |
| `CLAUDE.md`, `AGENTS.md` | **ROOT (keep)** | agent rules (span all zones); add boundary-principle insert |
| `tools/`, `.github/` | **ROOT (keep)** | cross-zone infra; update CI path allowlists |
| `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` | retire → `90_research/` or delete | superseded by zone model |

## Reference-update plan (low-cost, per v1 scan)

- **~18 path-style references** (`02_product/specs/…md`, `03_architecture/…md`) break on move → fix each.
- **~1,442 bare-filename references** survive untouched (no directory encoded).
- **Must hand-update:** `START_HERE.md`, `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md`, `CLAUDE.md`/`AGENTS.md`, the Phase-1 kickoff packet, and `tools/doc_integrity_check.py` (path allowlists/excludes, `raw/`→`90_research/raw/`).
- **Execution = one atomic commit:** pure moves + the ~18 path fixes + the meta-file updates + CI config. **No content changes** in the same commit. **Gate the merge on a green doc-integrity run** (0 errors).

## Open judgment calls for owner (the ⚠ rows)
1. **Glossary / ontology / canonical_definitions** — `00_owner` (governance vocabulary) vs `10_product` (domain meaning). Recommendation: `00_owner`, product references it.
2. **Build-governance specs** (QA/Obs/Deploy governance, control system, coding constraints, AI-First delivery rules) — **RESOLVED → `00_owner/build_governance/` as owner-ratified policy** (owner-constraint clause). Engineering may propose edits; the owner ratifies. This preserves the owner's standing right to prescribe *how* OSLO is built.
3. **Architecture reviews / audits** — `30_engineering` (eng trail) vs `00_owner` (decision-grade). Recommendation: decision-grade → `00_owner/decisions`; working reviews → `30_engineering`.
4. **`subsystems/`** — confirm it's owner-governed scope declarations.

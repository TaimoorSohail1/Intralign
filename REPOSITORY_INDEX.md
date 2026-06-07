# Repository Index — Concept → Canonical File

**Purpose:** the fast "where is X?" map for a new Claude Code instance, engineer, PM, or architect. For every major OSLO concept, this points to the **canonical** source (and notes when something is deferred or NOT DISCOVERABLE). Created per **KIA-6** (`01_governance/audits/OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001.md`).

> **Authority order (when sources disagree):** Doctrine > Constitution > Implementation; the **append-only ledger** (`01_governance/decisions/decision_log.md` DL-029–DL-049 + `changelog/changelog.md` CHG-001–069) is current and wins over any summary. Two canonical-definitions surfaces exist — where they conflict, **Doctrine prevails (DL-036)**.

## Orientation & rules (read first)
| Concept | Canonical file |
|---|---|
| Where to start (build path) | `START_HERE.md` → `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` |
| Never infer a gap — escalate | `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` |
| One name per concept + banned synonyms | `CANONICAL_GLOSSARY.md` |
| Capability → contract → test → event | `RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` |
| Owner-decision values (do not assume) | `OPEN_TBD_REGISTER.md` |
| Repository organization + precedence | `REPOSITORY_ARCHITECTURE.md` |
| AI-contributor rules / authority constraint | `CLAUDE.md` (+ `AGENTS.md` twin) |

## Cognitive architecture (the spine)
| Concept | Canonical file |
|---|---|
| Cognitive spine (Perceive→Retain→Infer→Evaluate→Advise→Disclose) | `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`; glossary |
| Act/Adapt · Render · Authority (inactive R1) | same + `CANONICAL_GLOSSARY.md` |
| Epistemic invariants (Attested/Derived, append-only, recompute-appends) | DL-043 (`decision_log.md`); `START_HERE.md` §1 |
| Runtime Object / Behavior Models | `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…_BEHAVIOR_MODEL_V1.md` |
| `Principal` identity (reviewer→user) | Object Model DL-049 Additions; DL-049 |
| ~~Layer model (Judgement/Governance/Communication)~~ | **DEPRECATED** — `03_architecture/legacy_layer_engineering/` (do not build from) |

## Canon / doctrine concepts
| Concept | Canonical file |
|---|---|
| Foundational thesis (what OSLO is) | `01_governance/doctrine/` (DL-001) |
| Outcome Orchestration | `01_governance/canonical_definitions/canonical_definitions.md`; `ontology/ontology_registry.md` |
| **Outcome Management** | ❌ undefined → **resolution proposed** `01_governance/decisions/PROPOSAL_OUTCOME_MANAGEMENT_RESOLUTION_DL050_DISPOSITION.md` (KIA-4; recommend retire/map) |
| Planning Intelligence | `02_product/specs/planning/OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` |
| Execution Intelligence | Future/R2 — `01_governance/backlog/RELEASE_2_BACKLOG_CANDIDATES.md` |
| CAF (Clarity/Alignment/Feasibility) | `02_product/specs/models/` + `constitution/`; Evaluate |
| Outcome Confidence · Reliability · False-Confidence | `02_product/specs/models/OUTCOME_CONFIDENCE_*`; DL-047 (false-confidence); Evaluate |
| Confidence ≠ probability/health | `CANONICAL_GLOSSARY.md`; Seam Audit 001 S6; Visual Spec §1.2 |
| **Product Vision / positioning / Intralign mission** | ⚠ **DRAFT skeleton** `02_product/specs/planning/OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md` (KIA-2 — `[OWNER TO COMPLETE]` strategy fields) |

## Product
| Concept | Canonical file |
|---|---|
| Capability matrix (R1 scope) | `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` |
| Canonical R1 scope | `02_product/specs/planning/OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` |
| Freemium / tier behavior + upgrade prompts (UP-1…8) | `02_product/tiering/12_freemium_tier_behavior_logic.md` |
| 5-tier taxonomy (Free·Basic·Pro·Team·Enterprise) | `CANONICAL_GLOSSARY.md`; Calibration §4c |
| Limit-reached interaction (Seam Audit) | freemium spec + `02_product/specs/audits_reviews/RELEASE_1_CROSS_LAYER_SEAM_AUDIT_001.md` |
| UX surfaces (MRI, Panels, Chat, Onboarding, Dashboard, Nav) | `02_product/specs/ux/` |
| Visual design / brand tokens | `02_product/specs/ux/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` |
| Virality / k-factor | `02_product/specs/planning/RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md`; Calibration §4f |

## Engineering / architecture / data
| Concept | Canonical file |
|---|---|
| Wave contracts (IC/QA/OBS build spec) | `03_architecture/contracts/WAVE_*` + `RELEASE_1_CONTRACT_INVENTORY_V1.md` |
| API contract | `02_product/specs/data_api_nfr/RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` |
| Event model (system/cognitive) | `02_product/specs/data_api_nfr/RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` |
| Logical data model (**current = V1.2**) | `02_product/specs/data_api_nfr/RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (V1/V1.1 superseded) |
| Calibration defaults (numeric config) | `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` |
| Cost governance / unit economics | DL-048; Calibration §4c; NFR §12 |
| Starter kit (app-repo seed) | `03_architecture/engineering/starter_kit/` |
| Implementation phases I–VI | `05_execution/implementation/Phase_*/IMPLEMENTATION_PLAN.md` |

## Telemetry / trust / testing / governance
| Concept | Canonical file |
|---|---|
| Telemetry + AI economics platform | `02_product/specs/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1.md` |
| Trust Index / cost-to-value ratios | same |
| Cognitive Observability Governance (two-axis replay) | `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` |
| Trust & Confidence models + fixtures | `02_product/specs/models/`; `02_product/specs/testing_fixtures/RELEASE_1_CONFIDENCE_*` |
| Testing strategy / fixtures / subsystem tests | `02_product/specs/testing_fixtures/` |
| QA + Deployment governance (gates, release criteria) | `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `…/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md` |
| Governance lifecycle / frameworks | `01_governance/frameworks/framework_001.md` · `…_001A.md` |
| Decisions / changelog (the ledger) | `01_governance/decisions/decision_log.md` · `01_governance/changelog/changelog.md` |
| Backlogs (revision + R2 candidates) | `01_governance/backlog/revision_backlog.md` · `…/RELEASE_2_BACKLOG_CANDIDATES.md` |
| Audits | `01_governance/audits/`; `02_product/specs/audits_reviews/`; `03_architecture/reviews/` |

---
*Non-canonical orientation aid (KIA-6). The linked files are authoritative; where this index and a source differ, the source wins. NOT-DISCOVERABLE items are open backlog (KIA-2, KIA-4).*

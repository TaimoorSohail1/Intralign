# Repository Index — Concept → Canonical File

> **Organized by ownership zone (DL-051).** This repository is filed by *ownership*, not topic:
> `00_owner/` (doctrine, constitution, frameworks, decisions, canonical definitions, glossary/ontology,
> build-governance — owner-only) · `10_product/` (product-authoritative) · `20_handoff/` (co-governed
> seam: contracts, traceability, interfaces) · `30_engineering/` (engineering-authoritative) ·
> `90_research/` (non-canonical). Precedence **Doctrine > Constitution > Implementation** is unchanged;
> all canonical change routes through Framework 001 and the **owner** ratifies. See `ZONE_GROUNDING_RULES.md`
> for the filing rules. *(Some narrative layout descriptions below predate the move and read against the
> old `01–05` domains; path references are current.)*

**Purpose:** the fast "where is X?" map for a new Claude Code instance, engineer, PM, or architect. For every major OSLO concept, this points to the **canonical** source (and notes when something is deferred or NOT DISCOVERABLE). Created per **KIA-6** (`00_owner/audits/OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001.md`).

> **Authority order (when sources disagree):** Doctrine > Constitution > Implementation; the **append-only ledger** (`00_owner/decisions/decision_log.md` DL-029–DL-049 + `changelog/changelog.md` CHG-001–069) is current and wins over any summary. Two canonical-definitions surfaces exist — where they conflict, **Doctrine prevails (DL-036)**.

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
| Cognitive spine (Perceive→Retain→Infer→Evaluate→Advise→Disclose) | `30_engineering/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`; glossary |
| Act/Adapt · Render · Authority (inactive R1) | same + `CANONICAL_GLOSSARY.md` |
| Epistemic invariants (Attested/Derived, append-only, recompute-appends) | DL-043 (`decision_log.md`); `START_HERE.md` §1 |
| Runtime Object / Behavior Models | `30_engineering/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…_BEHAVIOR_MODEL_V1.md` |
| `Principal` identity (reviewer→user) | Object Model DL-049 Additions; DL-049 |
| ~~Layer model (Judgement/Governance/Communication)~~ | **DEPRECATED** — `30_engineering/legacy_layer_engineering/` (do not build from) |

## Canon / doctrine concepts
| Concept | Canonical file |
|---|---|
| Foundational thesis (what OSLO is) | `00_owner/doctrine/` (DL-001) |
| Outcome Orchestration | `00_owner/canonical_definitions/canonical_definitions.md`; `ontology/ontology_registry.md` |
| **Outcome Orchestration** (the discipline/category) | `CANONICAL_GLOSSARY.md`; `OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md`; `canonical_definitions.md` |
| ~~Outcome Management~~ | **RETIRED (DL-050)** → use **Outcome Orchestration** / Outcome Integrity (glossary banned synonym) |
| Planning Intelligence | `10_product/scope/OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` |
| Execution Intelligence | Future/R2 — `00_owner/backlog/RELEASE_2_BACKLOG_CANDIDATES.md` |
| CAF (Clarity/Alignment/Feasibility) | `10_product/domain/` + `constitution/`; Evaluate |
| Outcome Confidence · Reliability · False-Confidence | `10_product/domain/OUTCOME_CONFIDENCE_*`; DL-047 (false-confidence); Evaluate |
| Confidence ≠ probability/health | `CANONICAL_GLOSSARY.md`; Seam Audit 001 S6; Visual Spec §1.2 |
| **Product Vision / positioning / Intralign mission** | ⚠ **DRAFT skeleton** `10_product/scope/OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md` (KIA-2 — `[OWNER TO COMPLETE]` strategy fields) |

## Product
| Concept | Canonical file |
|---|---|
| Capability matrix (R1 scope) | `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md` |
| Canonical R1 scope | `10_product/scope/OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` |
| Freemium / tier behavior + upgrade prompts (UP-1…8) | `10_product/strategy/tiering/12_freemium_tier_behavior_logic.md` |
| 5-tier taxonomy (Free·Basic·Pro·Team·Enterprise) | `CANONICAL_GLOSSARY.md`; Calibration §4c |
| Limit-reached interaction (Seam Audit) | freemium spec + `30_engineering/product_audits_reviews/RELEASE_1_CROSS_LAYER_SEAM_AUDIT_001.md` |
| UX surfaces (MRI, Panels, Chat, Onboarding, Dashboard, Nav) | `10_product/experience/` |
| Visual design / brand tokens | `10_product/experience/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` |
| Virality / k-factor | `10_product/scope/RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md`; Calibration §4f |

## Engineering / architecture / data
| Concept | Canonical file |
|---|---|
| Wave contracts (IC/QA/OBS build spec) | `20_handoff/contracts/WAVE_*` + `RELEASE_1_CONTRACT_INVENTORY_V1.md` |
| API contract | `20_handoff/data_api_nfr/RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` |
| Event model (system/cognitive) | `20_handoff/data_api_nfr/RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` |
| Logical data model (**current = V1.2**) | `20_handoff/data_api_nfr/RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (V1/V1.1 superseded) |
| Calibration defaults (numeric config) | `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` |
| Cost governance / unit economics | DL-048; Calibration §4c; NFR §12 |
| Starter kit (app-repo seed) | `30_engineering/delivery/starter_kit/` |
| Implementation phases I–VI | `30_engineering/implementation/Phase_*/IMPLEMENTATION_PLAN.md` |

## Telemetry / trust / testing / governance
| Concept | Canonical file |
|---|---|
| Telemetry + AI economics platform | `30_engineering/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1.md` |
| Trust Index / cost-to-value ratios | same |
| Cognitive Observability Governance (two-axis replay) | `00_owner/build_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` |
| Trust & Confidence models + fixtures | `10_product/domain/`; `30_engineering/testing_fixtures/RELEASE_1_CONFIDENCE_*` |
| Testing strategy / fixtures / subsystem tests | `30_engineering/testing_fixtures/` |
| QA + Deployment governance (gates, release criteria) | `00_owner/build_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `…/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md` |
| Governance lifecycle / frameworks | `00_owner/frameworks/framework_001.md` · `…_001A.md` |
| Decisions / changelog (the ledger) | `00_owner/decisions/decision_log.md` · `00_owner/changelog/changelog.md` |
| Backlogs (revision + R2 candidates) | `00_owner/backlog/revision_backlog.md` · `…/RELEASE_2_BACKLOG_CANDIDATES.md` |
| Audits | `00_owner/audits/`; `30_engineering/product_audits_reviews/`; `30_engineering/reviews/` |

---
*Non-canonical orientation aid (KIA-6). The linked files are authoritative; where this index and a source differ, the source wins. NOT-DISCOVERABLE items are open backlog (KIA-2, KIA-4).*

# Document Consolidation Plan

**Type:** Repository-wide document classification (consolidation & simplification — **no files moved or deleted**)
**Date:** 2026-05-31

> **Purpose.** Classify every document into one of four buckets so engineers know which documents are current truth. **Recommended Locations are recommendations only** — this plan moves and deletes nothing. The repository contains ~200 markdown files; the bulk (`raw/notion/`, ~120 files, and the `01_governance/` tree) is classified at the **group** level, with the small active set itemized precisely. That itemization *is* the simplification.

**Buckets:** **Active Canonical** (must remain active — source of truth) · **Active Supporting** (useful reference, not source of truth) · **Future Architecture** (preserved for future development) · **Archive** (historical decision-support, purpose served).

---

## Active Canonical — the source-of-truth set (target: < 10)

| Document | Reason | Recommended Location |
|---|---|---|
| `CURRENT_TRUTH.md` *(new)* | Single entry point; first read | `02_product/specs/` (or repo root) |
| `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` *(new)* | Definitive Release 1 scope; governs on scope conflicts | `02_product/specs/` |
| `OSLO_RELEASE_1_MASTER_SPEC.md` | Authoritative product specification | `02_product/specs/` |
| `OSLO_CAPABILITY_MATRIX_V2.md` | Current capability inventory (98) | `02_product/specs/` |
| `OSLO_LINEAR_INITIATIVES_V2.md` | Current initiative map (20 / 45 epics) | `02_product/specs/` |
| `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md` | Current milestone + workstream plan | `02_product/specs/` |
| `OSLO_ARCHITECTURE_BASELINE_V1.md` | Architecture baseline *(active layers; its Governance/Execution layers are Future Architecture per Canonical Scope)* | repo root or `02_product/specs/` |
| *UI Specification (when created)* | UX source of truth | `02_product/specs/` |

---

## Active Supporting — reference, not source of truth

| Group / Document | Reason | Recommended Location |
|---|---|---|
| **Understanding Domain models (8)** — CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, Overlay, Finding, Recommendation | Active architecture detail behind the scope | `02_product/specs/models/active/` |
| **Notification Model** | Active Supporting Service spec | `02_product/specs/models/active/` |
| `MODEL_LINEAGE_INDEX_V1.md` | Navigational architecture map | `02_product/specs/models/` |
| `OSLO_RELEASE_1_DEPENDENCY_GRAPH.md`, `OSLO_RELEASE_1_SCOPE_OPTIMIZATION_REVIEW.md` | Planning/sequencing detail | `02_product/specs/` |
| Change records: `OSLO_ARCHITECTURE_V1_SIMPLIFICATION_PLAN.md`, `ARCHITECTURE_V1_REFACTOR_REPORT.md`, `ARCHITECTURE_V1_REFACTOR_IMPACT_MATRIX.md`, `ARCHITECTURE_V1_FINAL_CONSISTENCY_AUDIT.md`, `DEEP_ANALYSIS_PASS_APPLY_REPORT.md`, `MODEL_COVERAGE_AUDIT_V1.md` | Decision/change history (recent, still informative) | `02_product/specs/refactors/` |
| `02_product/` UX/PLG/collaboration/tiering/workflows (`user_experience/*`, `plg/*`, `collaboration/*`, `tiering/*`, `workflows/*`) | Active product/UX for Release 1 (collaboration, sharing, reporting, 60-second flow) | keep in `02_product/` |
| `OSLO_CAPABILITY_MATRIX_V1.md`, `OSLO_LINEAR_INITIATIVES_V1.md` (root) | Contain active Context Plane / Planning Intelligence detail; **superseded by V2 for product scope** | repo root (mark "superseded by V2") |
| `01_governance/` constitution, doctrine, canonical_definitions, manifest, frameworks | Governing authority (constitutional layer; reference for engineering) | `01_governance/` (unchanged) |
| `01_governance/decisions`, `changelog`, `backlog`, `ontology`, `protocols` | Governance record | `01_governance/` (unchanged) |
| `README.md`, `REPOSITORY_ARCHITECTURE.md`, `CLAUDE.md` | Repo orientation / AI-contributor rules | repo root (unchanged) |

---

## Future Architecture — preserved for future development

| Group / Document | Reason | Recommended Location |
|---|---|---|
| **Governance Domain models (5)** — Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding | Outcome Orchestration / Agent Governance; banner-classified Future Architecture | `02_product/specs/models/future_architecture/` |
| `03_architecture/governance_layer/*`, `judgement_layer/*` | 7-layer governance/judgment runtime (future orchestration) | `03_architecture/` (unchanged; mark Future) |
| `raw/notion/.../Governance Layer*`, `Execution Layer*`, `Judgment Layer*`, `Communication Layer*`, `System-wide Contracts/*` (Agent Execution Authorization, Execution Posture, Compute Budget, Action Class Catalog, Governance Decision Matrix, Tier Capability, etc.) | Future Outcome-Orchestration / Agent-Governance engineering material | `raw/notion/` (preserved) or `/future_architecture/reference/` |
| `01_governance/doctrine/07_governance_policy_doctrine.md`, `10_execution_orchestration_maturity.md` | Future-orchestration doctrine | `01_governance/doctrine/` (unchanged) |

---

## Archive — historical decision-support, purpose served (preserved, not deleted)

| Group / Document | Reason | Recommended Location |
|---|---|---|
| `raw/notion/` — historical Notion export (prior 7-layer architecture, layer playbooks/specs, transcripts, `Archive/*`, ~120 files) | Historical source material; superseded by the active set | `/archive/raw_notion/` (or leave in place; mark Archive) |
| `04_research/transcripts/*`, `04_research/historical_artifacts/*` | Research transcripts / historical drafts | `04_research/` (unchanged; already non-canonical) |
| Terminology artifacts: `TERMINOLOGY_RECONCILIATION_AUDIT_V1.md`, `TERMINOLOGY_RECONCILIATION_DECISION_001.md`, `FOUNDER_TERMINOLOGY_DECISION_WORKBOOK_001.md` | Decision-support whose decisions are now **Future Scope** (parked with governance); not on V1 path | `02_product/specs/refactors/` (mark Archive/parked) |
| `DEEP_ANALYSIS_PASS_REFACTOR_AUDIT.md` | Superseded by `DEEP_ANALYSIS_PASS_APPLY_REPORT.md` (changes applied) | `02_product/specs/refactors/` (mark Archive) |
| `MASTER_SPEC_ALIGNMENT_REVIEW.md` *(in the Claude project workspace, not the git repo)* | Historical alignment analysis | keep as reference; not in active set |

---

## Classification summary

| Bucket | Count (approx.) | Notes |
|---|---|---|
| Active Canonical | **7–8** | The single source-of-truth set (+ UI spec when created) |
| Active Supporting | ~35 | Models, planning detail, UX, governance doctrine/record, repo orientation |
| Future Architecture | ~40+ | 5 governance models + 7-layer governance/execution + future contracts |
| Archive | ~120+ | `raw/notion/` export, research transcripts, parked terminology + superseded audits |

*Recommended Locations are advisory; no document is moved or deleted by this plan.*

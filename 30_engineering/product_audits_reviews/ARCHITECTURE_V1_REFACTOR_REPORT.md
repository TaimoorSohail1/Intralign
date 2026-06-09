# Architecture V1 Refactor Report

**Document:** ARCHITECTURE_V1_REFACTOR_REPORT.md
**Type:** Refactor report (documentation-consistency refactor; founder decision implemented)
**Date:** 2026-05-31

> **Founder decision implemented (final, not re-opened).** Architecture V1 is a **Planning Intelligence / Understanding-Improvement System**. **Active Architecture V1** = CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, Overlay, Finding, Recommendation, **Notification**. **Future Architecture** (Outcome Orchestration / Agent Governance / Enterprise Governance / Autonomous Execution) = Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding — **preserved and specified, not active V1.** This refactor only **reclassifies**; it deletes, deprecates, invalidates, and rewrites nothing.

---

## 1. Rationale

The founder has decided that Governance Domain concepts are **not part of the active V1 Planning Architecture**. Planning-stage OSLO is an understanding-improvement system whose active loop is **Evidence → Understanding → Assessment → Recommendation → User Action → Updated Evidence**, with the user retaining authority. The Governance Domain (controlled acceptance of understanding) is the substrate of Outcome Orchestration / Agent Governance and is therefore reclassified as **Future Architecture**.

The refactor's job was a **documentation-consistency pass**: ensure every architecture/lineage/audit/terminology/index document reflects this classification, while **preserving all governance work, all audit artifacts, and all historical reasoning** for later activation.

This refactor evaluates nothing, proposes no alternatives, re-opens no governance analysis, and creates no new model. It is a reclassification only.

---

## 2. Files Reviewed

Every model, lineage, audit, terminology, index, summary, and roadmap document in `02_product/specs/` was reviewed for governance references.

| File | Reviewed | Governance-lineage references? | Action |
|---|---|---|---|
| CAF_ASSESSMENT_MODEL_V1.md | ✓ | None | No change (active V1) |
| CAF_SCORING_MODEL_V1.md | ✓ | Incidental ("CAF Review Requests" = Master Spec *feature*, not the governance model) | No change (active V1) |
| RELIABILITY_MODEL_V1.md | ✓ | None | No change (active V1) |
| CONFIDENCE_MODEL_V1.md | ✓ | None | No change (active V1) |
| MRI_MODEL_V1.md | ✓ | None | No change (active V1) |
| OVERLAY_MODEL_V1.md | ✓ | None | No change (active V1) |
| FINDING_MODEL_V1.md | ✓ | Incidental ("Finding review requests" in a future-evolution list) | No change (active V1) |
| RECOMMENDATION_MODEL_V1.md | ✓ | None | No change (active V1) |
| NOTIFICATION_MODEL_V1.md | ✓ | Trigger list references governance objects (conceptual) | No change; classified active Supporting Service (see §4) |
| RESOLUTION_CANDIDATE_MODEL_V1.md | ✓ | Self (governance model) | **Banner added** (reclassify → Future Architecture); content preserved |
| REVIEW_REQUEST_MODEL_V1.md | ✓ | Self (governance model) | **Banner added**; content preserved |
| DISPOSITION_MODEL_V1.md | ✓ | Self (governance model) | **Banner added**; content preserved |
| GOVERNANCE_MODEL_V1.md | ✓ | Self (governance model) | **Banner added**; content preserved |
| ACCEPTED_UNDERSTANDING_MODEL_V1.md | ✓ | Self (governance model) | **Banner added**; content preserved |
| MODEL_LINEAGE_INDEX_V1.md | ✓ | Presented governance as active/specified domain | **Refactored** (Active V1 / Future split) |
| MODEL_COVERAGE_AUDIT_V1.md | ✓ | Treated governance as a completed active domain | **Reframed** (V1 complete without governance); findings preserved |
| TERMINOLOGY_RECONCILIATION_AUDIT_V1.md | ✓ | Governance terminology analysis | **Framing note added** (Future Scope, off V1 critical path); findings preserved |
| TERMINOLOGY_RECONCILIATION_DECISION_001.md | ✓ | Governance terminology decisions | **Framing note added**; package preserved |
| FOUNDER_TERMINOLOGY_DECISION_WORKBOOK_001.md | ✓ | Governance terminology decisions | **Framing note added**; workbook preserved |
| OSLO_ARCHITECTURE_V1_SIMPLIFICATION_PLAN.md | ✓ | Already classifies governance as Future Scope | No change (already consistent; this report executes its recommendations) |
| OSLO_RELEASE_1_MASTER_SPEC.md | ✓ | "CAF Review Requests" = collaboration *feature*; "governance" generic | No change (does not reference governance model lineage — see §5) |
| OSLO_CAPABILITY_MATRIX_V2.md | ✓ | "CAF Review Requests" = capability *feature* | No change (out of scope) |
| OSLO_LINEAR_INITIATIVES_V2.md | ✓ | "CAF Review Requests" = initiative *feature* | No change (out of scope) |
| OSLO_RELEASE_1_DEPENDENCY_GRAPH.md | ✓ | Feature references only | No change (out of scope) |
| OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md | ✓ | Feature references only | No change (out of scope) |
| OSLO_RELEASE_1_SCOPE_OPTIMIZATION_REVIEW.md | ✓ | Feature references only | No change (out of scope) |

---

## 3. Files Changed

**Governance models (reclassified, content preserved) — 5:** Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding. *Change:* one additive **classification banner** per file, immediately after the header, stating the model is **Future Architecture — Outcome Orchestration / Agent Governance**, preserved and not part of active V1. **No definition, position, principle, example, or body text was altered.**

**Model Lineage Index (refactored) — 1:** MODEL_LINEAGE_INDEX_V1.md. *Changes:* header classification line; §2 Architectural Overview reframed to Active V1 vs Future Architecture with an explicit Active/Future block; §5 responsibility-matrix classification note; §7 Governance Domain Overview reframed to Future Architecture (deferred) with the lineage chain and Human-Evaluation note preserved verbatim; §8 governance models relabeled "Future Architecture — Governance Domain Models"; §8 Knowledge-Layer note reframed (active, not governance-gated); §9 governance principles marked Future Architecture; §10 Summary reframed (Active V1 = 9; Future = 5); Validation tables/checklist reclassified.

**Coverage Audit (reframed) — 1:** MODEL_COVERAGE_AUDIT_V1.md. *Changes:* top reclassification note; §6 Domain Completeness reframed (Active V1 complete without governance; Governance Domain = Future Architecture); §9 maturity reframed. **All findings preserved.**

**Terminology artifacts (framing notes) — 3:** Terminology Audit, Decision 001, Workbook 001. *Change:* one framing note each — governance terminology is Future Scope, off the V1 critical path, non-blocking for V1. **All findings, options, and decision fields preserved.**

**Total files changed: 10.** Files deleted: 0. Governance models deleted/deprecated/invalidated: 0.

---

## 4. Notification Classification

Notification is **active Architecture V1, Supporting Service**. It supports Findings, Recommendations, understanding improvements, and awareness of relevant changes, and **requires no Governance Domain participation**. The Notification Model's conceptual trigger list still enumerates governance objects (Review Request, Disposition, Governance outcomes, Accepted Understanding); under Architecture V1 those **governance-object triggers are dormant** (they activate only when governance does), while the **active-object triggers (Findings, Recommendations) are operative**. This is a scoping fact, not a model change — the Notification Model was **not modified**.

---

## 5. Scope Clarification — "CAF Review Requests" vs the "Review Request Model"

A deliberate distinction, important to avoid over-reaching: the Release 1 product documents (Master Spec, Capability Matrix, Initiatives, Dependency Graph, Implementation Plan, Scope Optimization) contain the term **"CAF Review Requests"** — a Release 1 **collaboration capability** (sharing a CAF finding with a stakeholder for review). This is **not** the governance **"Review Request Model."** The founder decision concerns the **governance model lineage**, not the Release 1 collaboration feature. Therefore the Release 1 product documents were reviewed and **left unchanged**; reclassifying them would have incorrectly deferred an active V1 feature.

---

## 6. Governance References Reclassified (summary)

- **From** "fully specified active Governance Domain," "two specified domains," "final output Accepted Understanding," "no future models remain" — **to** "Future Architecture (Outcome Orchestration / Agent Governance); specified and preserved; not active V1."
- **Active V1 loop** restated everywhere as Evidence → Understanding → Assessment → Recommendation → User Action → Updated Evidence, with **governance removed from the active loop** and **no active lineage terminating in Accepted Understanding.**
- **Knowledge Layer** reframed as an existing active capability **not gated by governance** (no Accepted-Understanding prerequisite, no governance-promotion requirement in active V1).
- **Notification** held as **active V1 Supporting Service**.
- **Context Plane capabilities** (ambiguity, assumption, clarification, interpretation, confirmation, knowledge updates) — these live in the Understanding Domain (e.g., CAF Assessment finding types: Missing Information, Ambiguity, Assumption, Inference, Conflict, Constraint, Coverage Gap) and were **not touched**; they remain active V1 and are not governance.

---

## 7. Summary of Changes

The repository now consistently presents OSLO Architecture V1 as a **Planning Intelligence / Understanding-Improvement System** of nine active models (eight Understanding Domain + Notification), with the five Governance Domain models preserved intact as **Future Architecture** for Outcome Orchestration / Agent Governance. No governance work was lost: every governance model, audit artifact, terminology package, and historical reasoning trail remains in place and re-activatable. The change set is a pure reclassification — additive banners, framing notes, and index/audit re-framing — with zero deletions and zero edits to governance model definitions.

*Companion documents: `ARCHITECTURE_V1_REFACTOR_IMPACT_MATRIX.md` (per-file detail) and `ARCHITECTURE_V1_FINAL_CONSISTENCY_AUDIT.md` (final verification).*

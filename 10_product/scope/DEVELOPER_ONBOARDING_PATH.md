# Developer Onboarding Path

**Type:** Reading order for a new engineer (smallest practical set)
**Date:** 2026-05-31

> **Goal:** a new engineer understands Release 1 after reading **fewer than 10 documents.** Read the required list in order; everything else is optional reference.

---

## Required reading (in order) — 7 documents

1. **`CURRENT_TRUTH.md`** — current status, active architecture, scope summary, roadmap, deferred list. *(Start here.)*
2. **`OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md`** — the definitive Release 1 scope, user journey, milestones, and what is deferred. *(Governs on scope.)*
3. **`OSLO_ARCHITECTURE_BASELINE_V1.md`** — the architecture (Context Plane, Knowledge Layer, Planning Intelligence; Fast/Deep Analysis horizons). *Note: its Governance/Execution layers are Future Architecture — see Canonical Scope.*
4. **`OSLO_CAPABILITY_MATRIX_V2.md`** — the capability inventory (what gets built).
5. **`OSLO_LINEAR_INITIATIVES_V2.md`** — the initiative map (how capabilities group into work).
6. **`OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`** — milestones (M0–M6), workstreams, critical path.
7. **UI Specification** — *(when created)* the UX source of truth.

After these seven, an engineer understands **what Release 1 is, what's in/out of scope, the architecture, the capabilities, the initiatives, and the build plan.**

---

## Optional reference (read only as needed)

- **Architecture model detail:** the 8 Understanding Domain model specs (CAF Assessment, CAF Scoring, Reliability, Confidence, MRI, Overlay, Finding, Recommendation) + Notification; `MODEL_LINEAGE_INDEX_V1.md` (the map).
- **Planning detail:** `OSLO_RELEASE_1_DEPENDENCY_GRAPH.md`, `OSLO_RELEASE_1_SCOPE_OPTIMIZATION_REVIEW.md`.
- **Change history:** the `ARCHITECTURE_V1_REFACTOR_*`, `OSLO_ARCHITECTURE_V1_SIMPLIFICATION_PLAN.md`, `DEEP_ANALYSIS_PASS_APPLY_REPORT.md`, `MODEL_COVERAGE_AUDIT_V1.md`.
- **Product/UX:** `02_product/user_experience/*`, `02_product/plg/*`, collaboration/tiering/workflows.
- **Governance authority:** `01_governance/` constitution, doctrine, canonical_definitions (read if your work touches doctrine).

---

## Do not start here (Future Architecture / Archive)

- **Future Architecture** (not Release 1): the 5 governance model specs (Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding); `03_architecture/governance_layer`, `judgement_layer`; the `raw/notion/` governance/execution/agent layer material.
- **Archive** (historical): the `raw/notion/` export, `04_research/` transcripts, the parked terminology artifacts, and superseded audits.

Reading these first is the most common source of confusion — they describe **future** governance/orchestration or **historical** architecture, not active Release 1.

---

*Seven required documents. Everything else is optional. If you've read items 1–7, you can build Release 1.*

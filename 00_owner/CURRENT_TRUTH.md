# CURRENT TRUTH — OSLO Release 1

**The first document every engineer reads.** Concise, current, authoritative for Release 1.
**Date:** 2026-05-31 · **Status:** **Secondary representation under DL-043 (2026-06-04).** Capability set preserved; architecture vocabulary superseded.

> **⚠ DL-043 reconciliation (2026-06-04).** The **canonical architecture** is now the **Cognitive Responsibility Architecture** (`OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`). This page's **layer vocabulary** (Context Plane / Knowledge Layer / Planning Intelligence / Judgment / Governance / Communication) is a **secondary dependency-ordering view**, mapped as: Context Plane→**Perceive**, Knowledge Layer→**Retain**, Planning Intelligence→**Infer + Evaluate**, Communication→**Disclose/Render**. The **Release 1 capability set on this page remains valid** (re-expressed, not invalidated). Two scope clarifications from DL-043: **(1)** R1 admission is **integrity-gated, not governance-gated** — consistent with this page's "Knowledge Layer not governance-gated"; **(2)** R1 **records user acceptance events** as attested project history (User Acceptance Record + Acceptance-Impact Assessment) while OSLO-level acceptance/Outcome Governance remains deferred — consistent with this page's deferral of the Governance Domain. **For canonical architecture, read the Cognitive Responsibility spec and DL-043 first.**

> If you read only one page, read this. For the definitive scope, read `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` next. Everything else is reference.

---

## 1. Current development status

OSLO Release 1 is in **planning-stage engineering**. It is a **Planning Intelligence / Understanding-Improvement System**: it helps a user understand project reality, assess that understanding, and improve it. The user retains authority; OSLO recommends, the user decides, and only action and evidence change understanding.

**Governance is deferred.** The Governance Domain (controlled acceptance of understanding) is **Future Architecture (Outcome Orchestration / Agent Governance)** — specified and preserved, but **not part of Release 1**.

---

## 2. Active architecture (Release 1)

- **Context Plane** — extraction & enrichment, across two horizons (Fast Extraction → orientation; Deep Extraction → enrichment: assumption/relationship expansion, additional claim discovery).
- **Knowledge Layer** — the active persistence/knowledge capability (not governance-gated).
- **Planning Intelligence** — assessment, across two horizons (Fast Assessment → orientation; Deep Assessment → confidence recalculation, expanded findings, expanded recommendations).
- **Two analysis horizons:** **Fast Analysis Pass → 60-Second Orientation**, then **Deep Analysis Pass → Confidence Recalculation → Expanded Findings → Expanded Recommendations**.
- **Understanding Domain Models (8):** CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation.
- **Notification Service** (Supporting Service).
- **Collaboration & Sharing**, **Reporting**.

The active loop: **Evidence → Understanding → Assessment → Recommendation → User Action → Updated Evidence.** Governance does not appear in it.

---

## 3. Current Release 1 scope (summary)

**In scope:** Context Plane, Knowledge Layer, Planning Intelligence, Fast/Deep Analysis Pass, Confidence Recalculation, Expanded Findings, Expanded Recommendations, the 8 Understanding Domain models, Notification, Collaboration & Sharing, Reporting. *(Full detail: `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md`.)*

**Out of scope (Future Architecture):** Resolution Candidate, Review Request, Disposition, Governance, Accepted Understanding, Agent Governance, Execution Intelligence, Autonomous Execution, Program Management, Portfolio Management.

---

## 4. Current capability inventory

The Release 1 capability inventory is **`OSLO_CAPABILITY_MATRIX_V2.md`** (98 capabilities across the active domains: Project Foundation, Evidence Ingestion, Planning Synthesis, Analysis Engine — Fast/Deep Pass, CAF, Confidence, MRI, Issues, Recommendations, CAF Overlays, Artifact Workspace, OSLO Chat, Collaboration, **CAF Review Requests¹**, Sharing, Telemetry, Monetization, Security, Platform). The deferred governance models are **not** capabilities in this inventory.

¹ *"CAF Review Requests" is a Release 1 **collaboration feature** (share a finding with a stakeholder). It is **not** the deferred governance "Review Request Model."*

---

## 5. Current roadmap / milestones

| Milestone | Delivers |
|---|---|
| **M0 — Foundation** | Identity, data model, persistence/event bus, security baseline, telemetry infra |
| **M1 — 60-Second Orientation** | Fast Analysis Pass → Initial Confidence, Initial Findings, Initial Recommendations, MRI (*not the final analysis state*) |
| **M2 — Deep Analysis Completion** | Deep Analysis Pass → Confidence Recalculation, Expanded Findings, Expanded Recommendations, Expanded Understanding; overlays, suggested fixes |
| **M3 — AI Assistance** | OSLO Chat |
| **M4 — Collaboration** | Comments, mentions, CAF Review Requests (feature) |
| **M5 — Virality** | Sharing, MRI sharing, Reporting/exports |
| **M6 — Monetization** | Tier limits, upgrade prompts |

Full plan: `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`. Initiative map: `OSLO_LINEAR_INITIATIVES_V2.md`.

---

## 6. Current implementation plan (one line)

Build the foundation (M0), reach the 60-second orientation (M1), complete deep analysis + the improvement loop (M2), then chat (M3), collaboration (M4), sharing/reporting (M5), monetization (M6). Critical path pivots on **CAF (I5)** and converges at **Fast Pass (I7)**.

---

## 7. Deferred architecture (preserved, not active)

The five Governance Domain models — **Resolution Candidate · Review Request · Disposition · Governance · Accepted Understanding** — plus **Agent Governance, Execution Intelligence, Autonomous Execution, Program Management, Portfolio Management**, are **Future Architecture (Outcome Orchestration / Agent Governance)**. They are fully specified and preserved for later activation and are **not** part of Release 1 engineering planning.

---

*Next read: `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` (definitive scope). Then the Architecture Baseline, Capability Matrix V2, Linear Initiatives V2, and Implementation Plan. Reading order: `DEVELOPER_ONBOARDING_PATH.md`.*

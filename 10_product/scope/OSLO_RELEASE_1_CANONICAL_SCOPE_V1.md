# OSLO Release 1 — Canonical Scope v1

**Type:** Canonical scope specification — **the governing source of truth for Release 1 scope**
**Date:** 2026-05-31 · **Status:** Active Canonical
**Consolidates (does not replace):** `OSLO_RELEASE_1_MASTER_SPEC.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md`

> **Definitive answer to the scope question — "If engineering builds everything described here, is Release 1 complete?" → Yes.** Everything required for Release 1 is enumerated below; everything in §8 is Future Architecture and is not required. Where this document and any other planning document differ on Release 1 *scope*, **this document governs.**

---

## 1. Purpose

This document exists to **eliminate scope ambiguity** for OSLO Release 1. Scope has been defined across several files (Master Spec, Capability Matrix, Linear Initiatives, Implementation Plan, Architecture Baseline); engineers needed one place that says, definitively, what is in Release 1 and what is not. This is that place.

It is a **consolidation artifact**: it gathers and reconciles existing scope definitions, but it does not replace those documents — each remains the detailed reference for its area (§10). It introduces no new capability, initiative, model, or doctrine, and it changes no scope; it states the current, founder-approved Release 1 scope clearly. **This document is the Release 1 scope source of truth.**

---

## 2. Release 1 Objective

Release 1 delivers a **Planning Intelligence / Understanding-Improvement System**. A user provides incomplete project evidence and receives a useful, evolving understanding of project reality:

- **Project understanding** is constructed from the user's evidence and context.
- **Confidence** in that understanding is produced and explained.
- **Findings** expose where the understanding is weak, ambiguous, or unsupported.
- **Recommendations** suggest how to improve it.
- **Understanding improvement** continues beyond the initial orientation, through a deeper analysis that recalculates confidence and expands findings and recommendations.

The user retains authority; OSLO recommends and the user decides. Only action and resulting evidence change understanding. Release 1 is about **understanding and improving** — not governing, accepting, or executing.

---

## 3. Release 1 User Journey

```text
Intent
  → Context Plane            (Fast Extraction + Deep Extraction; enrichment)
  → Knowledge Layer          (canonical storage, retrieval, versioning, relationship graph)
  → Fast Analysis Pass
  → 60-Second Orientation    (Initial Confidence · Initial Findings · Initial Recommendations)
  → Deep Analysis Pass
  → Confidence Recalculation
  → Expanded Findings
  → Expanded Recommendations
  → Expanded Understanding
```

**Narrative.** The user expresses **Intent**. The **Context Plane** extracts and enriches context — rapidly first (**Fast Extraction**, feeding orientation), then more deeply (**Deep Extraction**: context enrichment, claim discovery, assumption discovery, relationship discovery). Extracted understanding is held in the **Knowledge Layer**. **Planning Intelligence** then assesses it across two horizons: the **Fast Analysis Pass** produces the **60-Second Orientation** (initial confidence, findings, recommendations) within seconds; the **Deep Analysis Pass** continues *after* orientation to **recalculate confidence** and produce **expanded findings**, **expanded recommendations**, and ultimately **expanded understanding**. The 60-Second Orientation is **not** the final analysis state — Deep Analysis is part of Release 1 and runs after it.

---

## 4. Active Release 1 Architecture

### Context Plane
- **Purpose:** Extract and enrich all external context before it informs understanding.
- **Capabilities:** Fast Extraction; Deep Extraction; Context Enrichment; Claim Discovery; Assumption Discovery; Relationship Discovery.
- **Outputs:** Normalized, enriched context (claims, assumptions, relationships) available to the Knowledge Layer and Planning Intelligence.

### Knowledge Layer
- **Purpose:** Hold the canonical knowledge OSLO reasons over.
- **Capabilities:** Canonical Storage; Retrieval; Versioning; Relationship Graph.
- **Outputs:** Versioned canonical knowledge and relationships consumable by Planning Intelligence. *(Active capability; not governance-gated — no Accepted-Understanding prerequisite.)*

### Planning Intelligence
- **Purpose:** Assess understanding and produce confidence, findings, and recommendations across two horizons.
- **Capabilities:** Fast Analysis Pass; Deep Analysis Pass; Confidence Recalculation; Expanded Findings; Expanded Recommendations.
- **Outputs:** 60-Second Orientation (initial confidence/findings/recommendations) and Deep Analysis results (recalculated confidence, expanded findings/recommendations, expanded understanding).

### Understanding Domain
- **Purpose:** The reasoning models behind assessment, scoring, reliability, confidence, visualization, attention, the actionable object, and prescriptive improvement.
- **Models:** CAF Assessment · CAF Scoring · Reliability · Confidence · MRI · Overlay · Finding · Recommendation.
- **Outputs:** CAF assessment + scores, reliability, outcome confidence, MRI visualization, overlays, findings, recommendations.

### Supporting Services
- **Notification** — **Purpose:** surface awareness of relevant changes (Findings, Recommendations, understanding improvements). **Outputs:** awareness notifications. Performs no governance.

### Collaboration
- **Purpose:** Let users collaborate around understanding.
- **Capabilities:** comments, replies, mentions; CAF Review Requests (a collaboration feature — sharing a finding with a stakeholder); sharing with permission levels.
- **Outputs:** collaboration activity; shared artifacts/links.

### Reporting
- **Purpose:** Communicate understanding outside the workspace.
- **Capabilities:** Reporting & Analytics; exports (e.g., PDF).
- **Outputs:** reports, exports, analytics views.

---

## 5. Release 1 Capability Inventory

Consolidated from the existing sources (`OSLO_CAPABILITY_MATRIX_V2.md`, `OSLO_RELEASE_1_MASTER_SPEC.md`, `OSLO_LINEAR_INITIATIVES_V2.md`); **no capability is invented here.** Active Release 1 capability domains:

- **Project Foundation, Evidence Ingestion, Planning Synthesis** (Context Plane extraction/enrichment, claim/assumption/relationship discovery).
- **Analysis Engine — Fast Analysis Pass / Deep Analysis Pass** (Confidence Recalculation, Expanded Findings, Expanded Recommendations).
- **CAF** (Assessment + Scoring), **Reliability**, **Confidence**.
- **MRI**, **CAF Overlays**, **Artifact Workspace**.
- **Issues** (Findings), **Recommendations** (incl. Suggested Fixes).
- **OSLO Chat**.
- **Collaboration**, **CAF Review Requests** (feature), **Sharing**, **Reporting & Analytics**.
- **Notification** (Supporting Service).
- **Cross-cutting:** Telemetry, Security & Compliance baseline, Platform Services, Monetization/Tier limits (as defined in the Master Spec / Matrix).

The deferred Governance Domain models are **not** in this inventory. *(Capability-level detail with IDs: `OSLO_CAPABILITY_MATRIX_V2.md`.)*

---

## 6. Release 1 Initiative Mapping

Using existing initiative names only; **no new initiative is created.**

### Active Initiatives
- **Product (Linear Initiatives V2):** Project Foundation · Evidence Ingestion · Planning Synthesis Engine · Artifact Workspace · CAF Engine · Confidence Engine · **Fast Pass** · **Deep Pass** · CAF Overlay System · Issue Engine · Recommendation Engine · OSLO Chat · MRI · Collaboration · CAF Review Requests · Sharing · Telemetry · Monetization · Security/Compliance · Performance.
- **Architecture-baseline vocabulary:** **Context Plane Implementation** and **Planning Intelligence Foundation** — where Deep Analysis is a *capability within* these initiatives (Fast/Deep Extraction; Fast/Deep Assessment), **not** a new initiative.

### Deferred Initiatives (Future Architecture — not Release 1)
- Governance Domain (Resolution Candidate, Review Request — governance model, Disposition, Governance, Accepted Understanding); Agent Governance; Execution Intelligence / Outcome Orchestration Runtime / Actuation; Team & Program Management; Portfolio Management.

---

## 7. Release 1 Milestones

Canonical user-facing milestone structure (implementation sequencing detail — including foundation and monetization phases — is elaborated in `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`):

| Milestone | Definition |
|---|---|
| **M1 — 60-Second Orientation** | The Fast Analysis Pass delivers the 60-Second Orientation: **Initial Confidence, Initial Findings, Initial Recommendations**, with the MRI visible. This is the first usable understanding; it is **not** the final analysis state. |
| **M2 — Deep Analysis Completion** | The Deep Analysis Pass completes after orientation, delivering **Confidence Recalculation, Expanded Findings, Expanded Recommendations, Expanded Understanding** (with CAF overlays and suggested fixes). Active Release 1. |
| **M3 — Collaboration & Sharing** | Collaboration around understanding: comments, mentions, CAF Review Requests (feature), and sharing with permission levels. |
| **M4 — Reporting & Analytics** | Reporting and analytics over understanding: reports, exports, and shareable outputs. |

---

## 8. Explicitly Out of Scope (Future Architecture — deferred, preserved)

The following are **Future Architecture** and are **not** part of Release 1. They are specified and preserved for later activation; none is built, planned, or required for Release 1.

- **Governance Domain:** Resolution Candidate · Review Request (governance model) · Disposition · Governance · Accepted Understanding.
- **Agent Governance.**
- **Execution Intelligence.**
- **Actuation** (mutations to external systems).
- **Outcome Orchestration Runtime.**
- **Autonomous Execution.**
- **Team & Program Management.**
- **Portfolio Management.**

**Why deferred.** Release 1 is a Planning Intelligence / understanding-improvement system. These capabilities concern **governed acceptance of understanding** and **execution/orchestration** — controlling what becomes accepted truth, governing AI/agent action, and acting on external systems. That belongs to **Outcome Orchestration / Agent Governance**, a later phase, not to a planning-stage product whose purpose is to help users understand and improve while retaining authority. Deferring them keeps Release 1 focused, smaller, and faster to validate, while preserving the work for activation when OSLO moves from planning to governed orchestration.

---

## 9. Success Criteria (user outcomes — Release 1 is complete when)

- A user can provide incomplete evidence and **receive a useful understanding** of project reality.
- Within ~60 seconds, the user **sees a 60-Second Orientation**: initial Outcome Confidence, initial Findings, and initial Recommendations, with an MRI.
- The **Deep Analysis Pass completes** after orientation: confidence is recalculated and findings and recommendations are expanded into an **expanded understanding** — i.e., orientation is demonstrably *not* the final state.
- The user can **act on recommendations**, and the understanding **improves through use** (confidence and findings respond to evidence and action).
- Users can **collaborate** around understanding (comments, mentions, CAF Review Requests) and **share/report** it.
- Throughout, **the user retains authority** and no governance/acceptance step is required to produce or improve understanding.

If these user outcomes hold, **Release 1 is complete** — no Future-Architecture (governance/execution/orchestration) capability is needed to satisfy them.

---

## 10. Relationship To Other Documents

- **`OSLO_ARCHITECTURE_BASELINE_V1.md`** — the architecture reference (Context Plane, Knowledge Layer, Planning Intelligence; Fast/Deep Analysis horizons). *Its Governance/Execution layers are Future Architecture per §8.* This scope doc governs *what is in Release 1*; the Baseline details *how the architecture is structured*.
- **`OSLO_CAPABILITY_MATRIX_V2.md`** — the capability-level inventory (with IDs/acceptance refs). This scope doc references it; the Matrix details capabilities.
- **`OSLO_LINEAR_INITIATIVES_V2.md`** — the initiative/epic decomposition. This scope doc maps to it; the Initiatives document details the work breakdown.
- **`OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`** — the implementation sequencing (foundation, phases, critical path, monetization). This scope doc defines the canonical milestones (M1–M4); the Implementation Plan elaborates the finer implementation phases beneath them.

**This document governs Release 1 scope.** The others remain the detailed references for architecture, capabilities, initiatives, and implementation, respectively, and are subordinate to this document on questions of *what is in or out of Release 1*.

---

*Definitive for Release 1 scope. Build everything In Scope (§4–§7) and Release 1 is complete.*

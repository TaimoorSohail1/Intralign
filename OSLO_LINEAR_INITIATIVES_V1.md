# OSLO Linear Initiatives v1

*Linear-ready initiative structure for engineering planning. Synthesized from OSLO_ARCHITECTURE_BASELINE_V1.md and OSLO_CAPABILITY_MATRIX_V1.md. Designed for direct use in Linear: each initiative becomes a top-level Linear Initiative; Projects within become Linear Projects; Capabilities map to Linear Issues / Epics.*

**Status:** Engineering Planning Artifact (v1, 2026-05-30)
**Audience:** Engineering leadership and Linear backlog setup
**Purpose:** Direct conversion to Linear workspace structure

---

## Initiative Map (At a Glance)

```
Foundation Layer (Critical / Foundational)
├── I1 — Planning Intelligence Foundation
├── I2 — Knowledge Layer Implementation
├── I3 — Context Plane Implementation
├── I4 — Governance Engine
└── I5 — Communication Layer Implementation

Value-Surface Layer (Critical / High)
├── I6 — Outcome Confidence Scoring
└── I7 — Recommendation Engine

Execution & Integration Layer (High)
├── I8 — Execution Coordination (Observability Phase)
├── I9 — Integrations Framework + Connectors v1
└── I12 — Execution Coordination (Actuation Phase)  [follows I8]

Multi-User & Reporting Layer (High)
├── I10 — Collaboration + Sharing
└── I11 — Reporting & Analytics

Advanced & Enterprise Layer (Medium)
├── I13 — Agent Governance
└── I14 — Team & Program Management
```

---

## Sequencing Strategy

The initiatives below are sequenced into three operational waves. Wave 1 must be substantially complete before Wave 2 begins; Wave 2 enables Wave 3.

- **Wave 1 (Months 0–6):** I1 + I2 + I3 + I4 + I5 + I6 — foundation through headline confidence experience.
- **Wave 2 (Months 6–12):** I7 + I8 + I9 + I10 + I11 — value surface and execution observability and team adoption.
- **Wave 3 (Months 12–18):** I12 + I13 + I14 — actuation, agent governance, program orchestration.

Within each wave, initiatives proceed in parallel where dependencies permit. Cross-initiative milestones (e.g., 60-Second Orientation) span multiple initiatives.

---

## I1 — Planning Intelligence Foundation

**Initiative Name:** Planning Intelligence Foundation

**Purpose:** Establish the production-ready intake → claim extraction → Reasoning → Judgment pipeline that produces scored Issues per outcome. This is the analytical core of OSLO. Planning Intelligence operates across **two active Release 1 analysis horizons** — a **Fast Assessment Pass** (powering the 60-Second Orientation) and a **Deep Assessment Pass** (continuing after orientation to recalculate confidence and expand findings and recommendations). Both horizons are Active V1; Deep Analysis improves understanding and performs no governance.

**Capabilities Included:**
- Reasoning Rule Engine + Rule Library v1
- Judgment Layer Scoring (severity + confidence + epistemic state)
- SMART Validation
- Issue Detection
- Assumption Detection
- Conflict Identification
- Relationship Discovery
- Determinism + Replay Infrastructure
- Resolution Candidate Generation
- Clarification Engine
- Alignment Analysis (initial)
- Feasibility Analysis (logical, initial)
- **Fast Assessment Pass** *(Active V1 — produces the 60-Second Orientation)*
- **Deep Assessment Pass** *(Active V1 — continues after orientation)*
- **Confidence Recalculation** *(Active V1 — Deep Analysis output)*
- **Expanded Issue Discovery** *(Active V1 — Deep Analysis output)*
- **Expanded Recommendation Generation** *(Active V1 — Deep Analysis output)*

**Dependencies:**
- Upstream: I2 (Knowledge Layer) for canonical storage; I3 (Context Plane) for ingestion of inputs.
- Downstream: I6 (Confidence Scoring) consumes Findings + Issues; I7 (Recommendation) consumes Issues.

**Suggested Priority:** Critical.

**Suggested Timeline:** Months 0–6 (Wave 1). Substantial implementation required before downstream initiatives can deliver value.

**Notes:**
- Replay infrastructure underpins audit and trust; cannot be deferred to later wave.
- Reasoning rule library expands continuously; v1 covers SMART_GAP, STRUCTURE_GAP, ALIGNMENT_GAP, FEASIBILITY_RISK, CONTENT_QUALITY_GAP at minimum.
- AI-assisted inference is an enabling capability within this initiative; it must be deterministic, replayable, and posture-aware.

---

## I2 — Knowledge Layer Implementation

**Initiative Name:** Knowledge Layer Implementation

**Purpose:** Build the production canonical Knowledge Layer per Specification: append-only versioned storage, epistemic status enforcement, immutable snapshots, replayability.

**Capabilities Included:**
- Knowledge Layer Canonical Store
- Command & Write Contract implementation
- Snapshot & Projection Infrastructure
- Multi-Tenant Isolation
- Schema Versioning
- Replay Infrastructure (Knowledge-side)
- Relationship Graph

**Dependencies:**
- Upstream: I4 (Governance Engine) for write authorization gate.
- Downstream: I1 (Reasoning consumes snapshots); all downstream layers depend on Knowledge state.

**Suggested Priority:** Critical.

**Suggested Timeline:** Months 0–6 (Wave 1). Must be in production before Reasoning + Judgment can scale.

**Notes:**
- Schema evolution strategy must be decided early (forward-only vs versioned vs in-place migration).
- Multi-tenant isolation guarantees define operational shape of Pro/Enterprise tiers.
- Append-only storage with efficient querying at scale is the central engineering challenge.

---

## I3 — Context Plane Implementation

**Initiative Name:** Context Plane Implementation

**Purpose:** Build the production Context Plane handling ingestion, normalization, staging, identity, time semantics, and promotion-readiness for all external context. The Context Plane operates across **two active Release 1 extraction horizons** — a **Fast Extraction Pass** (feeding the 60-Second Orientation) and a **Deep Extraction Pass** (enriching context after orientation through assumption and relationship expansion and additional claim discovery). Both horizons are Active V1 and are Context Plane enrichment, not governance.

**Capabilities Included:**
- Context Plane Ingestion
- Multi-source ingestion (free-text, document upload, structured form, API, signals)
- Normalization Pipeline
- Staging Storage
- Raw Record Identity & Idempotency
- Time Semantics & Ordering
- Promotion Readiness
- Promotion Candidate Generation
- Quarantine & Rejection
- Resolution Candidate Generation (Context Plane side)
- **Fast Extraction Pass** *(Active V1 — feeds the 60-Second Orientation)*
- **Deep Extraction Pass** *(Active V1 — continues after orientation)*
- **Context Enrichment** *(Active V1)*
- **Assumption Expansion** *(Active V1 — Deep Extraction)*
- **Relationship Expansion** *(Active V1 — Deep Extraction)*
- **Additional Claim Discovery** *(Active V1 — Deep Extraction)*

**Dependencies:**
- Downstream: I2 (Knowledge Layer) for promotion target; I9 (Integrations) for connector ingestion at scale.

**Suggested Priority:** Critical.

**Suggested Timeline:** Months 0–6 (Wave 1). Foundational to all downstream value; cannot be deferred.

**Notes:**
- Two integrity contracts are already operative (Raw Record Identity & Idempotency; Time Semantics & Ordering); implementation should align.
- Context → Knowledge Promotion Contract specification needs completion (currently listed as required follow-on document).
- Connector framework (I9) is paired with this initiative; initial connectors are needed to exercise the ingestion pipeline.

---

## I4 — Governance Engine

**Initiative Name:** Governance Engine

**Purpose:** Build the production policy-driven authorization engine implementing the Triple Intersection Rule (Tier ∩ Posture ∩ Governance) for exposure decisions and action authorization.

**Capabilities Included:**
- Governance Policy Engine
- Triple Intersection Rule implementation
- Governance Decision Matrix (Tier × Posture × Action Class)
- Posture System
- Tier Capability System
- Per-Tenant Policy Customization
- Outcome Resolution Workflows
- Audit Log Infrastructure
- Compliance Export (Enterprise)
- Data Retention Policies (Enterprise)
- PII / Sensitive Data Handling (Enterprise)
- Compute Budget Enforcement

**Dependencies:**
- Upstream: I1 (Judgment Layer) for Issues; Posture Contract, Tier Capability Contract, Action Class Catalog (specifications).
- Downstream: I5 (Communication) consumes Dispositions; I7 (Recommendations) constrained by Authorizations; I8/I12 (Execution) gated by Authorizations.

**Suggested Priority:** Critical.

**Suggested Timeline:** Months 0–6 (Wave 1). Required for any non-trivial AI behavior; required for enterprise readiness.

**Notes:**
- The Governance Decision Matrix (Tier × Posture × Action Class) requires per-action-class population — significant content engineering effort.
- Audit Log Infrastructure is cross-cutting across all layers but anchored in this initiative.
- Per-tenant policy customization scope and Enterprise compliance features can be deferred to later iterations within this initiative but must be on the roadmap.

---

## I5 — Communication Layer Implementation

**Initiative Name:** Communication Layer Implementation

**Purpose:** Build the production Communication Layer that renders and discloses governed system behavior across surfaces, with posture-aware honesty.

**Capabilities Included:**
- Communication Rendering Pipeline
- Surface-Specific Renderers (UI, Summary, Detail, Export)
- Posture Disclosure
- Delegated-Execution Disclosure
- Confidence Display
- Compression Rules
- Notifications (in-app initial)

**Dependencies:**
- Upstream: I4 (Governance) for Dispositions and Authorizations.
- Cross-initiative: I6 (Confidence Display); I10 (Sharing renders shared artifacts); I11 (Reporting renders reports).

**Suggested Priority:** Critical (paired with each upstream initiative).

**Suggested Timeline:** Months 0–6 (Wave 1). Paced with I4 to deliver early end-to-end value loop.

**Notes:**
- Posture honesty (Invariant: any posture-influenced behavior must be disclosed) is a core OSLO trust commitment; cannot be deferred.
- Communication is the user's primary contact surface; UX investment here pays disproportionate adoption dividend.

---

## I6 — Outcome Confidence Scoring

**Initiative Name:** Outcome Confidence Scoring

**Purpose:** Build the production composite confidence scoring per outcome, decomposed by driver, explainable back to evidence. The headline OSLO output.

**Capabilities Included:**
- Outcome Confidence Scoring
- Clarity Analysis
- Alignment Analysis (deeper integration)
- Feasibility Analysis (deeper integration)
- Per-Driver Confidence Sub-Scoring
- Driver Aggregation Logic
- Confidence Trajectory Tracking
- Confidence Display & Drilldown
- Confidence Trend Display
- Evidence Drilldown UX

**Dependencies:**
- Upstream: I1 (Planning Intelligence — Findings + Issues with evidence); I2 (Knowledge Layer for evidence retrieval).
- Cross-initiative: I5 (Communication Layer renders confidence).

**Suggested Priority:** Critical.

**Suggested Timeline:** Months 0–6 (Wave 1) substantial scoring framework in production; refinement continues into Wave 2.

**Notes:**
- Per-driver weighting strategy is an open question; v1 may default to uniform weighting with calibration in later iterations.
- The confidence model framework is well-specified (Doctrine 06); production scoring is the gap.
- Headline metric for product success — invest in display UX accordingly.

---

## I7 — Recommendation Engine

**Initiative Name:** Recommendation Engine

**Purpose:** Build the production Issue-anchored action proposal system constrained by current Posture, Tier, and Governance policy.

**Capabilities Included:**
- Recommendation Generation
- Action Class Catalog
- Recommendation UI with Acceptance Flow
- Refinement & Acceptance
- Recommendation-to-Execution Handoff
- Per-Posture Recommendation Behavior
- Recommendation Rejection Capture

**Dependencies:**
- Upstream: I1 (Judgment Layer Issues); I4 (Governance Engine for authorization).
- Downstream: I8/I12 (Execution Coordination receives accepted recommendations for delegated actions).

**Suggested Priority:** High.

**Suggested Timeline:** Months 6–9 (early Wave 2). Builds on stable Issues + Governance.

**Notes:**
- Action Class Catalog is a content engineering effort; per-class definition is non-trivial.
- Recommendation rejection feedback loop is important for learning loop (I-tbd) but not blocking for v1.

---

## I8 — Execution Coordination (Observability Phase)

**Initiative Name:** Execution Coordination — Observability Phase

**Purpose:** Build the always-on observability path of Execution Layer: signal ingestion + recompute triggers, without actuation.

**Capabilities Included:**
- Execution Signal Ingestion (signals from external execution tools)
- Execution Signal Normalization
- Recompute Trigger Orchestration
- Drift Detection
- Outcome Monitoring (continuous)
- Recompute Triggers (always-on)

**Dependencies:**
- Upstream: I3 (Context Plane); I1 (Reasoning + Judgment); I9 (Integrations connectors).
- Downstream: I12 (Actuation Phase) builds on this foundation.

**Suggested Priority:** High.

**Suggested Timeline:** Months 6–12 (Wave 2). Requires stable foundational layers.

**Notes:**
- Observability path is posture-invariant (recompute is always-on regardless of posture); actuation is posture-gated and deferred to I12.
- This initiative delivers the differentiating "drift detection" capability that makes OSLO superior to static planning tools.

---

## I9 — Integrations Framework + Connectors v1

**Initiative Name:** Integrations Framework + Connectors v1

**Purpose:** Build the connector framework plus an initial connector library across PM, communication, identity, and calendar.

**Capabilities Included:**
- Connector Framework (auth, rate limiting, mapping, error recovery)
- Jira Connector
- Asana Connector
- Linear Connector
- Microsoft Planner / Project Connector
- Slack Connector
- Microsoft Teams Connector
- Google Calendar Connector
- Microsoft Outlook Calendar Connector
- SSO / SAML / SCIM
- (Later) CRM Connector (Salesforce, HubSpot)
- (Later) Analytics Connector (Mixpanel, Amplitude, etc.)
- (Later) Custom Connector SDK

**Dependencies:**
- Upstream: I3 (Context Plane for ingestion); I4 (Governance for authorization); I5 (Communication for notification routing).

**Suggested Priority:** High.

**Suggested Timeline:** Months 3–12 (Wave 1 framework + initial connectors; Wave 2 expanded library). Continuous expansion.

**Notes:**
- Connector framework architecture decisions (e.g., self-hosted vs SaaS connectors) significantly affect operational scope.
- SSO/SAML/SCIM required for Enterprise tier; should be on Wave 1 deployment roadmap.
- First connectors paced with I8 to exercise the Execution Observability path.

---

## I10 — Collaboration + Sharing

**Initiative Name:** Collaboration + Sharing

**Purpose:** Build multi-user OSLO instances with role-aware access, immutable shared artifacts, and external sharing controls.

**Capabilities Included:**
- Multi-User Workspaces
- Role Model + Permission Scopes
- Concurrent-User UX
- Immutable Shared Artifacts (Executive Summary, Charter, OSLO Explanations)
- External Sharing with Audit
- Comment Threading
- Collaboration Notifications
- Workspace Roles

**Dependencies:**
- Upstream: Stable Planning Intelligence + Confidence; I5 (Communication for shared artifact rendering); I9 (Identity / SSO for enterprise collaboration).
- Cross-initiative: I11 (Reporting renders shared artifacts).

**Suggested Priority:** High (for Basic / Pro tier launch).

**Suggested Timeline:** Months 6–12 (Wave 2). Enables team adoption.

**Notes:**
- Collaboration role model is currently unanchored (RB-012); a v1 model should be specified early in this initiative.
- Immutability of shared artifacts is a key trust commitment; align with Communication Layer architecture.

---

## I11 — Reporting & Analytics

**Initiative Name:** Reporting & Analytics

**Purpose:** Build the production reporting and analytics layer: Executive Summary, Charter Report, OSLO Explanation Generator, versioned reports, portfolio analytics.

**Capabilities Included:**
- Executive Summary
- Charter Report
- OSLO Explanation Generator
- Versioned Reports
- Comment Threading on Reports
- Export (PDF/CSV)
- Outcome Inventory
- (Later) Portfolio Confidence
- (Later) Portfolio Analytics

**Dependencies:**
- Upstream: I5 (Communication for rendering); I10 (Collaboration for sharing); I6 (Confidence for confidence display in reports).
- Cross-initiative: I14 (Team & Program Management for portfolio views).

**Suggested Priority:** High.

**Suggested Timeline:** Months 6–12 (Wave 2). Pacing with Collaboration.

**Notes:**
- Reports are a primary stakeholder consumption surface; UX investment matters.
- Versioning + comments + immutability per shared artifact create powerful collaboration affordance.

---

## I12 — Execution Coordination (Actuation Phase)

**Initiative Name:** Execution Coordination — Actuation Phase

**Purpose:** Build posture-gated coordinated mutations to external tools under explicit Governance authorization. Activates the write path of the Execution Layer.

**Capabilities Included:**
- Action Class Registry (Execution Coordination side)
- Assisted-Posture Confirmation Flow
- Delegated-Posture Authorization Workflows
- Rollback Infrastructure (per ActionClass)
- Cross-Tool Action Coordination
- Coordinated Mutations (Assisted, Delegated)
- Execution Recommendations

**Dependencies:**
- Upstream: I4 (Governance Engine); I7 (Recommendation Engine); I8 (Execution Observability foundation); I9 (Integrations connectors for actuation).

**Suggested Priority:** Medium (post foundational stability).

**Suggested Timeline:** Months 12–18 (Wave 3). After Wave 1 and Wave 2 stability.

**Notes:**
- Rollback infrastructure is critical; cannot ship Actuation without it.
- Per-ActionClass design is a major content engineering effort; should be planned and resourced explicitly.
- Cross-tool coordination is the orchestration endpoint — long-term differentiator.

---

## I13 — Agent Governance

**Initiative Name:** Agent Governance

**Purpose:** Build authorization, posture-gating, and audit for AI/agent actions per the Agent Execution Authorization Contract.

**Capabilities Included:**
- Agent Identity Model
- Per-Agent Posture Mapping
- Per-Agent Tier Mapping
- Agent Action Class Registry
- Agent Audit Log
- Agent Rollback
- Agent Authorization Workflows
- Agent Compute Budget

**Dependencies:**
- Upstream: I4 (Governance Engine); I12 (Execution Coordination Actuation Phase); identity framework.

**Suggested Priority:** Medium (Pro / Enterprise differentiator).

**Suggested Timeline:** Months 12–18 (Wave 3). Builds on actuation infrastructure.

**Notes:**
- Agent identity model is foundational and must be settled early in this initiative.
- Agent identity is a distinct dimension from user identity; conflation will cause governance gaps.

---

## I14 — Team & Program Management

**Initiative Name:** Team & Program Management

**Purpose:** Build multi-outcome views, cross-outcome dependencies, program-level confidence, and portfolio orchestration foundation.

**Capabilities Included:**
- Multi-Outcome Workspace
- Cross-Outcome Dependencies
- Program-Level Confidence
- Program-Level Posture Configuration
- Project MRI (subject to doctrinal scoping)
- Portfolio Posture Lifecycle
- Portfolio Confidence (re-platforming for portfolio scale)
- Portfolio Analytics

**Dependencies:**
- Upstream: All foundational initiatives stable at single-outcome scale.
- Cross-initiative: I11 (Reporting for portfolio views).

**Suggested Priority:** Medium.

**Suggested Timeline:** Months 12–18 (Wave 3). Requires foundational stability.

**Notes:**
- Multi-outcome data model is a non-trivial Knowledge Layer evolution; should be considered during I2 design.
- Project MRI scope is currently uncertain (RB-015 partial unblock); doctrinal scoping needed before implementation.

---

## Cross-Initiative Milestones

Milestones spanning multiple initiatives that represent integrated product capability.

### M1 — 60-Second Orientation (cross-initiative)

**Spans:** I1, I3, I5, I6.

**Purpose:** A new user provides intent and receives outcome confidence within 60 seconds.

**Suggested Timeline:** End of Wave 1 (Month 6). Major release milestone.

### M2 — Single-Outcome Production OSLO (cross-initiative)

**Spans:** I1, I2, I3, I4, I5, I6, I7.

**Purpose:** Production-ready single-outcome experience for Basic tier.

**Suggested Timeline:** End of Wave 1 (Month 6) or beginning of Wave 2 (Month 7).

### M3 — Execution-Connected OSLO (cross-initiative)

**Spans:** I8, I9, I5.

**Purpose:** Continuous outcome awareness as execution unfolds. Single-outcome with external execution signals integrated.

**Suggested Timeline:** Mid-Wave 2 (Month 9).

### M4 — Team OSLO (cross-initiative)

**Spans:** I10, I11, I5, I9 (SSO/SAML).

**Purpose:** Multi-user OSLO with sharing, reporting, role-aware access.

**Suggested Timeline:** End of Wave 2 (Month 12).

### M5 — Delegated Execution OSLO (cross-initiative)

**Spans:** I12, I7, I4.

**Purpose:** OSLO acts on the user's behalf within Delegated-posture bounds. Action class catalog populated; rollback operative; cross-tool coordination available.

**Suggested Timeline:** Mid-Wave 3 (Month 15).

### M6 — Enterprise & Program OSLO (cross-initiative)

**Spans:** I13, I14, I4 (Enterprise features), I9 (SCIM, custom connectors).

**Purpose:** Enterprise-grade OSLO with agent governance, program / portfolio capabilities, custom policies.

**Suggested Timeline:** End of Wave 3 (Month 18).

---

## Linear Workspace Setup Notes

Recommended Linear configuration:

- **Each initiative (I1 through I14) becomes a Linear Initiative.**
- **Each project (P1.1, P1.2, etc.) becomes a Linear Project under its parent Initiative.**
- **Each capability from the Capability Matrix becomes a Linear Issue / Epic under its associated Project.**
- **Cross-initiative milestones (M1 through M6) can be tracked as Linear Cycles or as a separate Roadmap view.**
- **Priorities translate directly:** Critical → Urgent or High; High → High; Medium → Medium; Low → Low.

Suggested top-level Linear teams:

- **Foundation Team** owns I1, I2, I3.
- **Governance & Communication Team** owns I4, I5.
- **Intelligence Team** owns I6, I7.
- **Execution & Integrations Team** owns I8, I9, I12.
- **Collaboration & Reporting Team** owns I10, I11.
- **Advanced & Enterprise Team** owns I13, I14.

Adapt team structure to actual engineering org shape; the initiative shape itself is platform-agnostic.

---

## Open Sequencing Questions

1. **Wave 1 scope vs duration trade-off.** Can Wave 1 deliver M2 (Single-Outcome Production OSLO) in 6 months, or should the milestone be at 9 months with sequenced foundational initiative completion?
2. **Connector library breadth.** First-tier connectors (Jira, Asana, Slack) or broader initial set? Affects pacing of I9 and dependent initiatives.
3. **Enterprise tier deferral.** Should Enterprise-specific capabilities (per-tenant policy, agent governance, SCIM, compliance export) be wholly deferred to Wave 3, or staged across Waves 2 and 3?
4. **Project MRI scope.** Whether to scope Project MRI as a separate initiative within I14 or as a follow-on after I14 stabilizes.
5. **Posture activation sequencing.** Should Assisted posture activate at end of Wave 1 (with M2) or only after M5 in Wave 3? Affects user experience and trust ramp.

---

*Linear Initiatives v1 complete. Initiative structure ready for direct Linear workspace setup. Cross-initiative milestones identified. Sequencing recommendations provided. Engineering leadership and product leadership may adapt timing and team assignments per organizational realities; the initiative shape itself remains stable.*

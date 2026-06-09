# OSLO Capability Matrix v1

> **📦 ARCHIVED 2026-06-04 — historical.** Superseded by `OSLO_CAPABILITY_MATRIX_V2.md`. Moved to `04_research/historical_artifacts/` to keep the active tree clean; content preserved for history and does **not** govern implementation.

*Engineering planning matrix. Foundation for roadmap planning and backlog decomposition. Companion to OSLO_ARCHITECTURE_BASELINE_V1.md and OSLO_LINEAR_INITIATIVES_V1.md.*

**Status:** Engineering Planning Artifact (v1, 2026-05-30)
**Audience:** Product leadership, engineering leadership, Linear backlog organization

---

## Legend

**Status values:**
- **Implemented** — In production; available to users today.
- **Partial** — Framework defined; production scoring/logic/UX incomplete or fragmented.
- **Planned** — Specified but not yet built.

**Priority values:**
- **Critical** — Required for core OSLO value proposition; foundational; blocking other capabilities.
- **High** — Required for paid-tier value; major adoption driver.
- **Medium** — Differentiator; deepens existing capability; nearer-term but not foundational.
- **Low** — Refinement or long-tail; deferrable without blocking core roadmap.

---

## Foundation Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Context Plane Ingestion | Multi-source ingestion (text, docs, API, signals) with normalization, identity, time semantics, source attribution, promotion-readiness scoring | Partial | Critical | External integration framework | I3 — Context Plane Implementation |
| Fast Extraction Pass | Rapid context extraction feeding the 60-Second Orientation | **Active V1 (Release 1)** | Critical | Context Plane Ingestion | I3 — Context Plane Implementation |
| Deep Extraction Pass | Post-orientation context enrichment: Assumption Expansion, Relationship Expansion, Additional Claim Discovery | **Active V1 (Release 1)** | High | Fast Extraction Pass; Context Plane Ingestion | I3 — Context Plane Implementation |
| Context Enrichment | Enrichment of extracted context during the Deep Extraction Pass (not governance) | **Active V1 (Release 1)** | High | Deep Extraction Pass | I3 — Context Plane Implementation |
| Knowledge Layer Canonical Store | Append-only versioned canonical storage with epistemic status enforcement, immutable snapshots, replayability | Partial | Critical | Governance Layer (write authorization) | I2 — Knowledge Layer Implementation |
| Reasoning Rule Engine | Externalized versioned rules for structural inference, gap detection, consistency reasoning, feasibility logic | Partial | Critical | Knowledge Layer | I1 — Planning Intelligence Foundation |
| Judgment Layer Scoring | Severity assignment, confidence estimation, epistemic state labeling for Issues | Partial | Critical | Reasoning Layer | I1 — Planning Intelligence Foundation |
| Governance Policy Engine | Triple Intersection Rule (Tier ∩ Posture ∩ Governance) implementation for exposure and action authorization | Partial | Critical | Judgment Layer; Posture/Tier/ActionClass contracts | I4 — Governance Engine |
| Communication Rendering | Posture-aware rendering and disclosure across UI, summary, detail, export surfaces | Partial | High | Governance Layer | I5 — Communication Layer Implementation |
| Determinism + Replay | Deterministic outputs across Reasoning/Judgment/Governance; replayability for audit | Partial | Critical | All layers; identity contracts | I1 — Planning Intelligence Foundation (replay sub-project) |
| Posture System | Three postures (Deliberate / Assisted / Delegated) with disclosure rules and per-action mapping | Partial | Critical | Governance Engine; Communication Layer | I4 — Governance Engine |
| Tier Capability System | Tier-based capability availability per Tier Capability Contract | Partial | High | Per-feature tier mapping | I4 — Governance Engine |

---

## Planning Intelligence Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Outcome Confidence Scoring | Composite confidence per outcome, decomposed by driver, explainable to evidence | Partial | Critical | Reasoning + Judgment Layers | I6 — Outcome Confidence Scoring |
| Fast Assessment Pass | Rapid assessment producing the 60-Second Orientation (initial confidence, findings, recommendations) | **Active V1 (Release 1)** | Critical | Reasoning + Judgment Layers | I1 — Planning Intelligence Foundation |
| Deep Assessment Pass | Post-orientation assessment that continues understanding improvement (not the final analysis state; not governance) | **Active V1 (Release 1)** | High | Fast Assessment Pass | I1 — Planning Intelligence Foundation |
| Confidence Recalculation | Recalculation of confidence during the Deep Assessment Pass | **Active V1 (Release 1)** | High | Deep Assessment Pass; Outcome Confidence Scoring | I1 — Planning Intelligence Foundation |
| Expanded Issue Discovery | Additional/maturing findings discovered during the Deep Assessment Pass | **Active V1 (Release 1)** | High | Deep Assessment Pass | I1 — Planning Intelligence Foundation |
| Expanded Recommendation Generation | Additional/improved recommendations generated during the Deep Assessment Pass | **Active V1 (Release 1)** | High | Deep Assessment Pass | I1 — Planning Intelligence Foundation |
| Clarity Analysis | Per-statement articulation/ambiguity/completeness evaluation aggregated to outcome-level clarity | Partial | Critical | Reasoning SMART_GAP + CONTENT_QUALITY_GAP findings | I6 — Outcome Confidence Scoring |
| Alignment Analysis | Multi-stakeholder / multi-stage convergence vs divergence analysis | Planned | High | Reasoning ALIGNMENT_GAP findings; Knowledge stakeholder records | I1 — Planning Intelligence Foundation |
| Feasibility Analysis | Logical feasibility (current); quantitative feasibility (future) | Partial | High | Reasoning FEASIBILITY_RISK findings; Knowledge constraint records | I1 — Planning Intelligence Foundation |
| SMART Validation | Detection of Specific/Measurable/Achievable/Relevant/Time-bound gaps | Partial | High | Reasoning rule library | I1 — Planning Intelligence Foundation |
| Issue Detection | Surfacing of structural gaps, ambiguities, conflicts, risks | Partial | Critical | Reasoning + Judgment Layers | I1 — Planning Intelligence Foundation |
| Assumption Detection | Per-statement epistemic distinction (Fact / Inference / Assumption / Recommendation / Conflict) | Partial | High | Knowledge Layer epistemic status; Doctrine 03 | I1 — Planning Intelligence Foundation |
| Conflict Identification | Detection of incompatible claims, conflicting stakeholder positions, contradicting evidence | Partial | High | Reasoning Layer | I1 — Planning Intelligence Foundation |
| Relationship Discovery | Cross-entity relationships, dependency chains, traceability | Partial | High | Knowledge graph; Reasoning Layer | I1 — Planning Intelligence Foundation |
| Pattern Recognition | Cross-instance pattern detection (recurring drift signatures, planning anti-patterns) | Planned | Medium | Multi-outcome data; Reasoning Layer | I14 — Team & Program Management |

---

## User Workflow Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Free-Text Intake | Natural-language intake from user input | Partial | Critical | Context Plane Ingestion | I3 — Context Plane Implementation |
| Document Upload | PDF, DOCX, etc. ingestion with content extraction | Planned | High | Context Plane Ingestion | I3 — Context Plane Implementation |
| Structured Form Intake | Multi-field structured intake (planning forms; scope; constraints) | Planned | High | Context Plane Ingestion | I3 — Context Plane Implementation |
| 60-Second Orientation | First-time experience producing outcome confidence in 60 seconds | Planned | Critical | All foundation layers | I1 + I3 + I6 (cross-initiative milestone) |
| Resolution Candidate Generation | Alternative interpretations presented with evidence and trade-offs | Planned | Medium | Reasoning Layer; Communication Layer | I1 — Planning Intelligence Foundation |
| Promotion Candidate Generation | Items eligible for canonical promotion presented for user authorization | Planned | High | Context Plane; Governance Layer | I3 — Context Plane Implementation |
| Clarification Engine | Targeted clarification prompts when ambiguity blocks promotion | Planned | High | Reasoning Layer; Communication Layer | I1 — Planning Intelligence Foundation |
| Recommendation Generation | Issue-anchored action proposals constrained by Posture/Tier/Governance | Partial | High | Judgment Layer; Governance Engine; Action Class Catalog | I7 — Recommendation Engine |
| Refinement & Acceptance | User accept/modify/defer/reject of recommendations | Planned | High | Recommendation Generation; Execution Coordination | I7 — Recommendation Engine |
| Recompute Triggers | Always-on recomputation on mutation or signal | Planned | Critical | Execution Layer; Reasoning Layer | I8 — Execution Coordination (Observability Phase) |

---

## Communication & Disclosure Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Surface-Specific Rendering | UI / Summary / Detail / Export rendering with preserved meaning | Planned | High | Communication Layer | I5 — Communication Layer Implementation |
| Posture Disclosure | Active posture name + behavior disclosure on every relevant surface | Planned | Critical | Communication Layer; Posture System | I5 — Communication Layer Implementation |
| Delegated-Execution Disclosure | Explicit labeling when actions are applied without explicit confirmation | Planned | Critical | Communication Layer; Execution Coordination | I5 — Communication Layer Implementation |
| Confidence Display | Composite confidence + per-driver breakdown + trend; on-click drilldown | Planned | Critical | Outcome Confidence Scoring | I6 — Outcome Confidence Scoring |
| Notifications | Posture-aware notifications across email, in-app, mobile, integrations | Planned | High | Communication Layer; Integrations | I5 + I9 (cross-initiative) |
| Compression Rules | Bundling and verbosity reduction without compromising epistemic disclosure | Planned | Medium | Communication Layer | I5 — Communication Layer Implementation |

---

## Collaboration & Sharing Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Multi-User Workspaces | Concurrent users on same outcome with role-aware access | Planned | High | Identity; Governance Engine | I10 — Collaboration + Sharing |
| Role Model | Workspace roles with permission scopes | Planned | High | Identity; Authorization framework | I10 — Collaboration + Sharing |
| Immutable Shared Artifacts | Executive Summary, Charter Report, OSLO Explanations rendered as immutable shareable artifacts | Planned | High | Communication Layer; Reporting Engine | I10 + I11 (cross-initiative) |
| External Sharing | Share with external stakeholders via link with audit, expiration, revocation | Planned | High | Sharing infrastructure | I10 — Collaboration + Sharing |
| Comment Threading | Comments on shared artifacts; collaboration around (not inside) canonical knowledge | Planned | Medium | Sharing infrastructure | I10 — Collaboration + Sharing |
| Collaboration Notifications | Notifications on collaborator actions, comments, shared updates | Planned | Medium | Communication Layer; Notifications | I10 — Collaboration + Sharing |
| SSO / SAML / SCIM | Enterprise identity integration | Planned | High (Enterprise tier) | Identity framework | I9 — Integrations Framework + Connectors v1 |

---

## Reporting & Analytics Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Executive Summary | Templated executive view of outcome with confidence and key Issues | Planned | High | Communication Layer; Reporting Engine | I11 — Reporting & Analytics |
| Charter Report | Structured charter-style outcome statement with provenance | Planned | High | Reporting Engine | I11 — Reporting & Analytics |
| OSLO Explanation Generator | Templated explanations of OSLO's reasoning and recommendations | Planned | High | Reporting Engine; Communication Layer | I11 — Reporting & Analytics |
| Versioned Reports | Reports versioned over time with diff/history view | Planned | Medium | Reporting Engine | I11 — Reporting & Analytics |
| Portfolio Confidence | Aggregate confidence across multiple outcomes | Planned | High (Pro tier) | Multi-outcome data model | I14 — Team & Program Management |
| Portfolio Analytics | Cross-outcome analytics (issue trends, confidence trajectories, drift patterns) | Planned | Medium | Multi-outcome data model | I14 — Team & Program Management |
| Outcome Inventory | List/table view of all outcomes in a workspace or program | Planned | High | Multi-outcome data model | I14 — Team & Program Management |
| Comment Threading on Reports | Comments threaded on report sections | Planned | Medium | Reporting; Collaboration | I11 — Reporting & Analytics |
| Export (PDF/CSV) | Export reports to PDF and structured data | Planned | Medium | Reporting Engine | I11 — Reporting & Analytics |

---

## Execution Intelligence Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Execution Signal Ingestion | Continuous ingestion from external execution tools (Jira, Asana, Planner, Linear, etc.) | Planned | Critical | Context Plane; Integrations | I8 — Execution Coordination (Observability) |
| Execution Signal Normalization | Mapping external signals to canonical references | Planned | Critical | Context Plane | I8 — Execution Coordination (Observability) |
| Drift Detection | Continuous comparison of plan to execution reality | Planned | Critical | Reasoning Layer; Knowledge Layer | I8 — Execution Coordination (Observability) |
| Recompute Trigger Orchestration | Trigger-based recomputation on mutation or signal | Planned | Critical | Execution Layer; Reasoning Layer | I8 — Execution Coordination (Observability) |
| Outcome Monitoring | Drift between Intended Reality and Current Reality per Doctrine 04 | Partial | Critical | Drift Detection; Knowledge Layer | I8 — Execution Coordination (Observability) |
| Execution Recommendations | Recommended actions based on drift detection and outcome monitoring | Planned | High | Recommendation Engine; Drift Detection | I7 + I8 (cross-initiative) |
| Coordinated Mutations (Assisted) | Posture-Assisted coordinated changes after explicit confirmation | Planned | High | Execution Coordination Actuation; Governance | I12 — Execution Coordination (Actuation Phase) |
| Coordinated Mutations (Delegated) | Posture-Delegated coordinated changes within authorized bounds | Planned | Medium | Execution Coordination Actuation; Governance; Action Class Catalog | I12 — Execution Coordination (Actuation Phase) |
| Rollback Infrastructure | Per-ActionClass rollback for coordinated mutations | Planned | Critical (for Actuation) | Execution Coordination Actuation | I12 — Execution Coordination (Actuation Phase) |
| Multi-Tool Action Coordination | Cross-tool action coordination (e.g., Jira issue + Slack notification + Calendar block) | Planned | Medium | Execution Coordination; Integrations | I12 — Execution Coordination (Actuation Phase) |

---

## Agent Governance Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Agent Identity Model | First-class identity for AI agents acting in OSLO | Planned | High | Identity framework | I13 — Agent Governance |
| Per-Agent Posture Mapping | Posture binding per agent (each agent operates at a posture) | Planned | High | Posture System; Agent Identity | I13 — Agent Governance |
| Per-Agent Tier Mapping | Tier binding per agent (each agent operates within tier capabilities) | Planned | High | Tier Capability System; Agent Identity | I13 — Agent Governance |
| Agent Action Class Registry | Action classes available to agents (subset of system action classes) | Planned | High | Action Class Catalog; Governance Engine | I13 — Agent Governance |
| Agent Audit Log | All agent actions logged with full trace | Planned | High | Audit Log Infrastructure | I13 — Agent Governance |
| Agent Rollback | Rollback capability for agent-initiated actions | Planned | High | Rollback Infrastructure | I13 — Agent Governance |
| Agent Authorization Workflows | Workflows for granting / revoking agent authorities | Planned | Medium | Authorization framework | I13 — Agent Governance |
| Agent Compute Budget | Per-agent compute budget enforcement | Planned | Medium | Compute Budget Contract | I13 — Agent Governance |

---

## Integration Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Connector Framework | Authentication, rate limiting, mapping, error recovery framework | Planned | Critical | Context Plane Ingestion | I9 — Integrations Framework + Connectors v1 |
| Jira Connector | Bidirectional integration with Jira | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Asana Connector | Bidirectional integration with Asana | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Linear Connector | Bidirectional integration with Linear | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Microsoft Planner / Project Connector | Integration with Microsoft Planner / Project | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Slack Connector | Notifications and signal ingestion from Slack | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Microsoft Teams Connector | Notifications and signal ingestion from Teams | Planned | High | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Google Calendar Connector | Calendar signal ingestion | Planned | Medium | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Microsoft Outlook Calendar Connector | Calendar signal ingestion | Planned | Medium | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| CRM Integration (Salesforce, HubSpot) | CRM signal ingestion | Planned | Medium | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| ERP Integration | ERP signal ingestion (Pro/Enterprise) | Planned | Low | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Analytics Integration | Analytics platform signal ingestion (Mixpanel, Amplitude, etc.) | Planned | Medium | Connector Framework | I9 — Integrations Framework + Connectors v1 |
| Custom Connector SDK | Customer-built connectors via SDK | Planned | Medium (Enterprise) | Connector Framework | I9 — Integrations Framework + Connectors v1 |

---

## Team & Program Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Multi-Outcome Workspace | Workspace with many outcomes; per-outcome OSLO instance | Planned | High | Multi-outcome data model | I14 — Team & Program Management |
| Cross-Outcome Dependencies | Explicit dependencies between outcomes | Planned | High | Multi-outcome data model; Knowledge Layer relationship graph | I14 — Team & Program Management |
| Program-Level Confidence | Aggregate confidence across program outcomes | Planned | High | Outcome Confidence Scoring; Multi-outcome data | I14 — Team & Program Management |
| Program-Level Posture Configuration | Posture set at program level applied to constituent outcomes | Planned | Medium | Posture System; Multi-outcome | I14 — Team & Program Management |
| Project MRI | Whole-portfolio outcome integrity scan | Planned | Medium | Multi-outcome data; Reasoning; Doctrine (RB-015 partial) | I14 — Team & Program Management |
| Portfolio Posture Lifecycle | Posture transitions per lifecycle stage | Planned | Medium | Posture System; Lifecycle | I14 — Team & Program Management |

---

## Audit & Compliance Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Audit Log Infrastructure | Comprehensive audit logs across all layers (writes, decisions, dispositions, actions) | Partial | Critical | All layers' observability | I4 — Governance Engine |
| Audit Query API | Programmatic audit query | Planned | High | Audit Log Infrastructure | I4 — Governance Engine |
| Replay Infrastructure | Deterministic replay for audit | Partial | High | Determinism guarantees; identity contracts | I1 — Planning Intelligence Foundation |
| Compliance Export | Export audit data for compliance reporting | Planned | Medium (Enterprise) | Audit Query API | I4 — Governance Engine |
| Data Retention Policies | Tenant-configurable data retention | Planned | Medium (Enterprise) | Knowledge Layer; per-tenant policy | I4 — Governance Engine |
| PII / Sensitive Data Handling | Identification, classification, and policy handling of PII | Planned | High (Enterprise) | Per-tenant policy; data classification | I4 — Governance Engine |

---

## Foundational Infrastructure Capabilities

| Capability | Description | Current Status | Priority | Dependencies | Potential Linear Initiative |
|---|---|---|---|---|---|
| Multi-Tenant Isolation | Logical and / or physical tenant isolation | Planned | Critical | Platform infrastructure | I2 — Knowledge Layer Implementation |
| Per-Tenant Policy Customization | Tenant-level policy overrides within platform constraints | Planned | High (Enterprise) | Governance Engine | I4 — Governance Engine |
| Schema Versioning | Knowledge Layer schema evolution | Planned | High | Knowledge Layer | I2 — Knowledge Layer Implementation |
| Compute Budget Enforcement | Per-tenant, per-action compute budgets | Planned | High | Compute Budget Contract | I4 — Governance Engine |
| Observability (System-Level) | Platform monitoring, alerting, performance metrics | Planned | Critical | Platform infrastructure | I2 + Platform initiatives |
| Reliability & Degradation | System Reliability & Degradation Spec; Safe Mode; Freeze / Last-Known-Good | Planned | Critical | All layers | Platform initiatives |
| SSO / SAML / SCIM | Enterprise identity provider integration | Planned | High (Enterprise) | Identity framework | I9 — Integrations Framework + Connectors v1 |

---

## Matrix Aggregate Statistics

- **Total capabilities cataloged:** ~95
- **Implemented:** 0
- **Partial (framework defined; production incomplete):** ~25
- **Planned:** ~70
- **Critical priority:** ~25
- **High priority:** ~45
- **Medium priority:** ~20
- **Low priority:** ~5

**Critical capability concentration:** Foundation Capabilities (Context Plane, Knowledge, Reasoning, Judgment, Governance, Communication) plus Outcome Confidence Scoring plus Execution Signal Ingestion / Drift Detection plus Audit Log Infrastructure.

**Highest-leverage cluster for initial release:** Context Plane + Knowledge Layer + Reasoning + Judgment + Confidence Scoring + Communication. Together this cluster delivers the headline OSLO experience: intake → governed knowledge → understanding → explainable confidence.

---

*Capability Matrix v1 complete. To be revised as capabilities are implemented, refined, or added.*

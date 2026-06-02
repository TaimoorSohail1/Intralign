# OSLO Architecture Baseline v1

*Engineering-oriented architecture baseline synthesized from the OSLO corpus. Optimized for engineering onboarding, roadmap planning, feature decomposition, and Linear initiative creation. Founder-intent-aligned synthesis: where multiple representations exist, this document prioritizes the founder's intended product vision.*

**Status:** Engineering Planning Artifact (v1, 2026-05-30)
**Audience:** Engineering leadership, product leadership, new engineers, founder
**Purpose:** Establish the primary engineering planning baseline for OSLO

---

## 1. Executive Summary

### What OSLO Is

OSLO (Outcome-Driven Strategic Lifecycle Orchestration) is a **governed cognitive architecture** that preserves trustworthy organizational understanding of outcomes as conditions evolve. It is not a project management tool; it is a layered reasoning system for outcome integrity under dynamic conditions.

OSLO sits beneath and alongside execution tools (Jira, Asana, Planner, etc.) and answers a category of questions those tools cannot:

- What did we intend?
- What do we now believe about whether we will achieve it?
- What changed?
- What did OSLO do on our behalf, and why was it allowed?

### What Problem It Solves

Organizations lose outcome integrity as plans encounter reality. Conventional tools record activity but cannot reason about meaning, drift, alignment, or confidence. AI tools generate output but cannot govern themselves. The result: silent assumption decay, unaccountable AI behavior, opaque trade-offs, and organizational drift.

OSLO solves four interlocking problems:

1. **Outcome drift** — intended reality diverges from observed reality without anyone noticing.
2. **Epistemic conflation** — facts, inferences, assumptions, and AI guesses get treated as equivalent.
3. **AI accountability** — autonomous and assisted AI behavior occurs without traceable authority, disclosure, or rollback.
4. **Confidence opacity** — organizations cannot tell what they actually believe about outcome achievability.

### How It Relates to Outcome Orchestration

OSLO is the substrate for Outcome Orchestration. Outcome Orchestration is the long-term product capability: continuously aligning execution to declared outcomes by detecting drift, recommending action, and (where authorized) coordinating execution across people, agents, and external systems. OSLO provides the layered cognitive architecture that makes orchestration trustworthy: separating what is known, what is implied, what is judged, what is allowed, and what is explained.

### How It Creates Value

- **Outcome Confidence** — explainable, evidence-bound confidence scores that consumers can trust.
- **Issue Detection** — surfacing of gaps, ambiguities, conflicts, and risks before they become failures.
- **Governed AI** — AI capability bounded by explicit posture, tier, and authorization at every step.
- **Drift Detection** — continuous comparison of intended versus current reality, with timing-sensitive response.
- **Decision Continuity** — auditable trace of every decision, its evidence, and its authorization.
- **Multi-Stakeholder Alignment** — explicit alignment surfaces preventing silent misunderstanding.

The core OSLO bet: trustworthy organizational understanding under dynamic conditions is the foundation that enables intelligent action.

---

## 2. Current Architecture Overview

OSLO is a **layered cognitive architecture** with strict separation of concerns. Each layer has a single responsibility, a defined input contract, a defined output contract, and explicit non-responsibilities.

### Architectural Diagram (Conceptual)

```
                    ┌───────────────────────────┐
                    │    Communication Layer    │
                    │    Render / Disclose      │
                    └────────────▲──────────────┘
                                 │
                    ┌────────────┴──────────────┐
                    │     Governance Layer      │
                    │   Authorize / Disposition │
                    └────────────▲──────────────┘
                                 │
                    ┌────────────┴──────────────┐
                    │      Judgment Layer       │
                    │  Severity / Confidence    │
                    └────────────▲──────────────┘
                                 │
                    ┌────────────┴──────────────┐
                    │     Reasoning Layer       │
                    │   Findings / Implications │
                    └────────────▲──────────────┘
                                 │
                    ┌────────────┴──────────────┐
                    │     Knowledge Layer       │
                    │  Canonical Assertions     │
                    └────────────▲──────────────┘
                                 │
                    ┌────────────┴──────────────┐
                    │       Context Plane       │
                    │ Ingestion / Normalization │
                    │ (cross-cutting)           │
                    └────────────▲──────────────┘
                                 │
                    External: users, signals, tools

                    ┌───────────────────────────┐
                    │   Execution Coordination  │
                    │   (Emerging / Activated   │
                    │    by Posture + Tier)     │
                    └───────────────────────────┘
                         Posture-gated;
                         feeds back to Reasoning
                         on signals or mutations
```

### Context Plane (Cross-Cutting)

**Purpose.** Manage all external context (planning, execution, validation inputs) before promotion into canonical Knowledge.

**Inputs.** User-authored inputs (text, documents, forms); execution signals (tool events, status updates, communications); validation signals (KPIs, CRM/ERP data, analytics).

**Outputs.** Normalized intermediate representations (events, entities, claims, metrics, interpretations) with source attribution, time semantics, identity, epistemic status, and promotion-readiness flags.

**Responsibilities.** Ingestion; normalization; staging (non-canonical intermediate state); source attribution; raw record identity and idempotency; temporal ordering; promotion-readiness assessment. **Two active Release 1 extraction horizons:** **Fast Extraction** (rapid extraction feeding the 60-Second Orientation) and **Deep Extraction** (post-orientation enrichment), comprising **Context Enrichment**, **Assumption Expansion**, **Relationship Expansion**, and **Additional Claim Discovery**. These extraction horizons are Active V1 Context Plane enrichment and perform no governance.

**Dependencies.** External system integrations; identity contracts; time semantics contracts; downstream Knowledge Layer for promotion.

**Current State.** Recognized canonically as a cross-cutting architectural plane. Two integrity contracts (Raw Record Identity & Idempotency; Time Semantics & Ordering) operative. Specification and follow-on documents not yet adopted.

**Planned Evolution.** Full Context Plane Specification; Context → Knowledge Promotion Contract; Context Source & Signal Taxonomy; Knowledge Layer Impact Addendum; Context Assembly Interface; 60-Second Onboarding Flow integration; Failure & Abuse Case matrix; Implementation Checklist.

**Key Engineering Challenges.** Scale-out integration with diverse external systems; idempotency under concurrent ingestion; multi-source temporal reconciliation; provenance preservation; quarantine and rejection handling; permissions-scoped ingestion.

---

### Knowledge Layer

**Purpose.** Sole system of record for canonical project knowledge. Memory, not intelligence.

**Inputs.** Authorized write commands (from governed sources via Command & Write Contract).

**Outputs.** Immutable snapshots consumable by Reasoning; canonical assertion records with explicit epistemic status.

**Responsibilities.** Store canonical assertions, entities, relationships; preserve append-only versioned history; enforce schema and integrity; record explicit assumptions, intents, estimates, constraints; record execution facts as observed reality; record governance authorization events; provide deterministic, replayable inputs to downstream layers.

**Non-Responsibilities.** No inference; no synthetic data; no promotion of epistemic status; no scoring; no exposure decisions; no language generation.

**Dependencies.** Governance Layer authorization for all writes; Knowledge Layer Command & Write Contract; Knowledge Definition File Specification.

**Current State.** Layer Specification mature (v1.x Canonical within architecture corpus); Command & Write Contract specified; Knowledge → Reasoning Projection specified; implementation pending.

**Planned Evolution.** Engineering implementation; multi-tenant scale; graph-aware relationship modeling; epistemic tagging at scale.

**Key Engineering Challenges.** Append-only versioned storage at scale; graph-aware relationship queries; epistemic status enforcement at write time; replayability across long histories; multi-tenant isolation.

---

### Reasoning Layer

**Purpose.** Derive structural implications from canonical knowledge. Answer: *given this structure, what must logically follow?*

**Inputs.** Canonical Knowledge artifacts (read-only via immutable snapshots); rule and invariant definitions; LifecycleContext; ComputeContext.

**Outputs.** **Findings** — structural claims about implications. Each Finding carries: finding_id, finding_type (e.g., STRUCTURE_GAP, CONTENT_QUALITY_GAP, SMART_GAP, ALIGNMENT_GAP, FEASIBILITY_RISK), structural_claim, implicated_objects, reasoning_rule_id, determinism_hash, generated_at.

**Responsibilities.** Structural inference (dependency order, coverage gaps, orphans, cycles); consistency reasoning (misaligned dates, broken traceability, invalid references); feasibility reasoning (logical impossibilities, constraint violations); AI-assisted inference (bounded and labeled).

**Non-Responsibilities.** No severity assignment; no confidence; no recommendations; no canonical mutations; no posture or tier sensitivity; no permission logic.

**Dependencies.** Knowledge Layer (read-only via snapshots); externalized versioned rules; Inference Policy Specification.

**Current State.** Layer Specification mature; rule execution model defined; AI-assisted inference framework specified; implementation pending.

**Planned Evolution.** Production rule library; AI-assisted inference activation; expanded finding-type taxonomy; pattern recognition (future).

**Key Engineering Challenges.** Determinism with AI components; rule versioning and rule conflict resolution; computational efficiency on large knowledge graphs; deferred reasoning under compute constraints; replayability with versioned rules.

---

### Judgment Layer

**Purpose.** Assign meaning and weight to inferred findings. Answer: *how serious is this, and how confident should we be?*

**Inputs.** Finding[] from Reasoning; canonical Knowledge artifacts (read-only); judgment rule definitions; LifecycleContext; ComputeContext.

**Outputs.** **Issues** with: issue_id, issue_type, severity (potential impact), confidence (belief strength), judgment_rationale, implicated_objects, supporting_findings, epistemic_state (inferred / supported / confirmed), generated_at.

**Responsibilities.** Severity assignment (potential impact, not urgency or priority); confidence estimation (belief strength, not correctness); epistemic state labeling; issue formulation.

**Non-Responsibilities.** No exposure decisions; no authorization; no execution; no posture/tier sensitivity; no remediation recommendations; no severity adjustment for UX reasons.

**Dependencies.** Reasoning Layer outputs (consumed via Reasoning → Judgment Consumption Contract); judgment rule definitions.

**Current State.** Layer Specification mature; Consumption Contract specified; implementation pending.

**Planned Evolution.** Confidence model maturation (per Doctrine 06 Confidence & Understanding); multi-driver scoring with clarity, alignment, feasibility, evidence strength, assumption stability dimensions; supersession and retention rules.

**Key Engineering Challenges.** Confidence calibration across diverse domains; severity taxonomy stability; epistemic state classification reliability; determinism within evidence bounds; explicit uncertainty preservation under compression.

---

### Governance Layer

**Purpose.** Control authority. Answer: *what may be surfaced, authorized, or resolved, and under what conditions?*

**Inputs.** Issue[] from Judgment; JudgementDecision; GovernanceContextEnvelope; PostureContext (required); TierContext; LifecycleContext; ComputeContext; ActionClass (if applicable).

**Outputs.** **IssueDispositions** (expose / suppress / defer / block) + **ActionAuthorizations** (allow / deny per Tier ∩ Posture ∩ Governance).

**Responsibilities.** Exposure governance; action authorization (triple-intersection rule: Tier ∩ Posture ∩ Governance); outcome resolution (achieve / retire / invalidate); enforcement of tier, posture, and lifecycle constraints; delegated execution controls.

**Non-Responsibilities.** No execution; no truth claims; no severity reframing; no reasoning.

**Dependencies.** Judgment Layer outputs; Execution Posture Contract; Tier Capability Contract; Action Class Catalog; Governance Decision Matrix.

**Current State.** Layer Specification mature; Consumption Contracts specified; Posture, Tier, Action Class contracts specified; implementation pending.

**Planned Evolution.** Policy framework expansion; posture × tier × action class matrix completion; per-tenant policy customization; delegated authorization workflows.

**Key Engineering Challenges.** Authorization performance at scale; multi-tenant policy isolation; posture state propagation; lifecycle-aware authorization; audit completeness.

---

### Communication Layer

**Purpose.** Make governed system behavior understandable without implying authority, correctness, or safety beyond what was authorized.

**Inputs.** IssueDisposition[] from Governance; ActionAuthorization[] (if applicable); referenced Issue[] / Finding[] (by ID, read-only); PostureContext (required); TierContext; LifecycleContext.

**Outputs.** **Communication Units (CUs)** — rendered, posture-disclosed, surface-appropriate messages with: cu_id, source references, posture/tier context, surface, message_type, content, disclosures, references.

**Responsibilities.** Rendering and delivery; posture-aware disclosure; epistemic safety guarantees; surface-invariant meaning preservation.

**Non-Responsibilities.** No reasoning; no severity reframing; no authorization; no recommendation generation; no implicit safety claims.

**Dependencies.** Governance Layer outputs; surface-specific renderers; Communication Authorization State Machine.

**Current State.** Layer Specification mature; Consumption Contract specified; implementation pending.

**Planned Evolution.** Multi-surface rendering (UI, summary, detail, export); posture-aware disclosure templates; delegated-execution narrative; compression rules.

**Key Engineering Challenges.** Meaning preservation across surfaces; disclosure consistency under compression; surface-specific UX while preserving epistemic integrity; multi-channel notification consistency.

---

### Execution Coordination Layer (Emerging — Posture-Gated)

**Purpose.** Keep OSLO anchored to reality while work and outcomes evolve. Answer: *what is happening, and what authorized coordination may occur as a result?*

**Inputs.** ActionAuthorization (when mutation requested); ActionClass; PostureContext (required); TierContext; LifecycleContext; ComputeContext; canonical artifact references.

**Outputs.** Applied mutations (when authorized); recompute triggers (always-on, posture-invariant); execution telemetry; audit records.

**Responsibilities.** Signal ingestion (observational, non-canonical); coordination of authorized actions; recompute triggers (always-on); enforcement of Tier ∩ Posture ∩ Governance for any mutation.

**Non-Responsibilities.** No interpretation; no severity; no outcome modification; no reprioritization; no communication of meaning directly to users.

**Dependencies.** Governance Layer authorization; Posture Contract; Action Class Catalog; Execution Signal Ingestion Contract; Execution–Reasoning Trigger Contract.

**Current State.** Layer Specification mature. **Observability path** (signal ingestion, recompute triggers) intended to be always-on. **Actuation path** (mutations to external systems) posture-gated and currently disabled by default. Phased activation via posture configuration.

**Planned Evolution.** Phase 1: signal ingestion and recompute triggers operative. Phase 2: Assisted-posture coordinated mutations with confirmation. Phase 3: Delegated-posture pre-authorized coordination within tier and action-class bounds.

**Key Engineering Challenges.** Rollback guarantees per ActionClass; cross-tool integration breadth; signal-to-trigger latency; posture-state-aware execution; multi-stream coordination at orchestration scale.

---

## 3. Current User Workflow

The end-to-end OSLO planning workflow synthesizes inputs from multiple sources into governed, confidence-bearing outcome understanding.

### Workflow Narrative

**Stage 1 — Intake.** The user describes intent through structured forms, free text, uploaded documents, or imported planning artifacts. Multi-modal intake is normalized through the Context Plane.

**Stage 2 — Ingestion.** External signals (execution events, validation data) are continuously ingested through the Context Plane. Sources are attributed, timestamped (event-time vs ingest-time vs source-recorded-time), and identity-keyed for idempotency.

**Stage 3 — Claim Extraction.** Context Plane normalization converts raw inputs into candidate structured claims: events, entities, claims, metrics, interpretations. Each carries source attribution, epistemic status (user-asserted, system-observed, third-party reported), and confidence (if available).

**Stage 4 — Normalization.** Heterogeneous inputs are mapped to canonical schemas. Structural transformations propose candidate canonical entities with explicit Mapping Explanations including ambiguity notes and alternative mappings.

**Stage 5 — Context Quality Scan.** The Context Plane assesses promotion readiness. Inputs are checked for completeness, freshness, duplication, conflicts, and validation. Items not ready are staged; items ready proceed to promotion.

**Stage 6 — Resolution Candidate Generation.** Where the user must choose between alternative interpretations (e.g., which mapping to accept), resolution candidates are presented with their evidence and trade-offs.

**Stage 7 — Promotion to Knowledge.** Approved candidates are promoted into the canonical Knowledge Layer under explicit authorization (G-03 UI-Authorized Mutation Rules). Provenance, version, and epistemic status are preserved.

**Stage 8 — Reasoning Pass (two active Release 1 horizons).** Reasoning Layer derives Findings: structure gaps, content quality gaps, SMART gaps, alignment gaps, feasibility risks, traceability issues. Findings are non-normative implications. Reasoning runs as **Fast Analysis Pass → 60-Second Orientation → Deep Analysis Pass**: the Fast Analysis Pass produces the initial orientation rapidly; the **Deep Analysis Pass continues after orientation** (it is not the final analysis state) to recalculate confidence and expand findings and recommendations. Both passes are Active Release 1; Deep Analysis improves understanding and performs no governance.

**Stage 9 — Judgment Pass.** Judgment Layer converts Findings into Issues with severity, confidence, and epistemic state. Issues are interpretations bounded by evidence and rules.

**Stage 10 — Scoring.** Confidence scores (Clarity, Alignment, Feasibility) are computed per-driver and aggregated. Scores are explainable back to underlying Findings and Issues.

**Stage 11 — Issue Detection.** Open Issues are surfaced to Governance for disposition. Governance determines exposure (which Issues surface, on which surfaces, with what timing).

**Stage 12 — Recommendation Generation.** Where actions are available, Recommendations are proposed as candidate next steps, anchored to specific Issues and constrained by current Posture, Tier, and Governance policy.

**Stage 13 — Refinement.** User accepts, modifies, defers, or rejects recommendations. Confirmed actions flow to Execution Coordination (in posture-permitted scope); deferred items return to the queue; rejected items are recorded.

**Stage 14 — Recompute Loop.** Any mutation (user-confirmed or delegated) and any new external signal triggers recomputation across Reasoning → Judgment → Governance, ensuring meaning propagation is always-on regardless of posture.

### Workflow Diagram (Text)

```
User Input ─┐
            ├─→ [Context Plane: Ingest / Normalize / Stage / Quality Scan]
Signals  ─┘                              │
                                         │ (promotion ready?)
                                         ▼
                            [Knowledge Layer: Canonical Store]
                                         │
                                         ▼
                            [Reasoning Layer: Findings]
                                         │
                                         ▼
                            [Judgment Layer: Issues + Scores]
                                         │
                                         ▼
                            [Governance Layer: Disposition + Authorization]
                                         │
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
              [Communication]  [Execution Coord]  [Knowledge updates]
                  Render            (posture-       (canonical writes
                  Disclose          gated)          when authorized)
                                         │
                                         └────► Recompute Trigger
                                              (back to Reasoning)
```

---

## 4. Intelligence Models

OSLO's intelligence is organized around three primary confidence drivers, each producing a scored, explainable signal.

### Clarity

**Purpose.** Measure how clearly the intent, scope, success criteria, and constraints are understood.

**Scoring Approach.** Per-statement evaluation of articulation specificity, ambiguity load, and completeness. Aggregated to claim-level, then to outcome-level Clarity score.

**Inputs.** Intent statements, scope statements, success criteria, constraints; ambiguity annotations from Mapping Explanations; SMART gaps from Reasoning.

**Outputs.** Clarity score (0.0–1.0 or band); per-driver clarity sub-scores; specific ambiguity findings.

**Dependencies.** Reasoning Layer SMART_GAP and CONTENT_QUALITY_GAP finding types; Judgment Layer evidence-strength evaluation.

**Future Evolution.** Multi-stakeholder clarity (where different stakeholders interpret the same statements differently); domain-specific clarity templates; clarity decay over time as new evidence surfaces.

### Alignment

**Purpose.** Measure how aligned stakeholders, intent, plan, and execution are with each other.

**Scoring Approach.** Pairwise position evaluation across stakeholders or across stages (intent vs plan; plan vs execution; current vs intended reality). Convergence vs divergence is assessed; alignment is the coherence measure.

**Inputs.** Stakeholder positions; intent representation; plan representation; execution observations; outcome targets.

**Outputs.** Alignment score; specific misalignment findings (where, between whom, on what dimension).

**Dependencies.** Reasoning Layer ALIGNMENT_GAP finding type; Knowledge Layer stakeholder position records.

**Future Evolution.** Multi-party alignment with weighted stakeholder influence; alignment trajectory over time; alignment thresholds gating progression.

### Feasibility

**Purpose.** Measure how achievable the plan is under current constraints, capacity, and dependencies.

**Scoring Approach.** Per-constraint evaluation (resources, capacity, dependencies, timeline, technical viability). Constraint satisfaction is aggregated to outcome-level feasibility.

**Inputs.** Plan claims (what, when, by whom); declared constraints; capacity records; dependency graph; external execution signals.

**Outputs.** Feasibility score; specific feasibility-risk findings; constraint-satisfaction breakdown.

**Dependencies.** Reasoning Layer FEASIBILITY_RISK finding type; logical impossibility detection; Knowledge Layer constraint records.

**Future Evolution.** Quantitative feasibility (probabilistic modeling beyond logical feasibility); resource simulation; sensitivity analysis showing which constraint changes would most affect feasibility.

### Composite Confidence

Per Doctrine 06 (Confidence & Understanding), composite confidence aggregates the three driver scores plus additional dimensions:

- Clarity
- Alignment
- Feasibility
- Evidence strength
- Assumption stability
- Stakeholder coverage
- Dependency stability
- Governance state
- Understanding boundaries

Composite confidence is the headline OSLO output — the explainable, evidence-bound trustworthiness of the organization's outcome understanding.

---

## 5. Capability Inventory

| Capability | Current State | Description |
|---|---|---|
| Outcome Confidence | Partial | Composite confidence score per outcome, decomposed by Clarity / Alignment / Feasibility + drivers. Per Doctrine 06; framework exists; production scoring pending. |
| Issue Detection | Partial | Detection of gaps, conflicts, ambiguities via Reasoning + Judgment Layers. Finding-type taxonomy specified; rule library partial. |
| Recommendation Engine | Partial | Action proposals anchored to Issues, constrained by Posture/Tier/Governance. Framework specified; action class catalog in development. |
| SMART Validation | Partial | Detection of SMART_GAP findings (specific, measurable, achievable, relevant, time-bound). Reasoning rule type defined. |
| Clarification Engine | Planned | Targeted clarification prompts when ambiguity blocks promotion or confidence. Workflow integration pending. |
| Assumption Detection | Partial | Per Doctrine 03 epistemic distinction (Facts, Inferences, Assumptions, Recommendations, Conflicts). Knowledge Layer epistemic status mandatory at write; assumption-expiration semantics pending (RB-017). |
| Alignment Analysis | Planned | Multi-stakeholder convergence / divergence analysis. Reasoning ALIGNMENT_GAP finding type defined; production analysis pending. |
| Feasibility Analysis | Planned | Logical (and eventually quantitative) feasibility assessment. Reasoning FEASIBILITY_RISK finding type defined; capacity / resource integration pending. |
| Collaboration | Planned | Multi-user OSLO instances with role-aware UX. Collaboration role model not yet anchored (RB-012). |
| Sharing | Planned | Immutable shared artifacts (Executive Summary, Charter Report, structured narratives). Collaboration around knowledge, not inside it. |
| Reporting | Planned | Versioned, commentable outputs (Executive Summary; Charter; OSLO Explanations; structured narratives). |
| Execution Monitoring | Planned | Continuous signal ingestion from Jira/Asana/Planner/etc., feeding back into Reasoning for drift detection. |
| Agent Governance | Planned | Authorization, posture-gating, and audit for AI / agent action under Agent Execution Authorization Contract. |
| Outcome Monitoring | Partial | Drift detection between intended and current reality (per Doctrine 04 Outcome Integrity). Framework specified; continuous monitoring pending. |
| Integrations | Planned | Connectors to PM tools, communication tools, CRM/ERP, calendar, analytics. Execution Signal Ingestion Contract defines categories. |
| Notifications | Planned | Posture-aware, surface-appropriate notifications. Communication Layer responsibility; delivery infrastructure pending. |
| Context Plane Ingestion | Partial | Cross-source ingestion with normalization. Two integrity contracts operative (Identity, Time Semantics); full ingestion pipeline pending. |
| Promotion Pipeline | Partial | Context → Knowledge promotion with explicit authorization. G-03 mutation rules specified; promotion contract specification pending. |
| Posture System | Partial | Three postures (Deliberate / Assisted / Delegated) with disclosure rules. Posture Contract specified; posture state propagation pending. |
| Tier Capability System | Partial | Tier-based capability availability per Tier Capability Contract. Framework specified; per-feature tier mapping pending. |
| Governance Decision Matrix | Partial | Tier × Posture × Action Class authorization rules. Matrix v1.0 defined; production policy engine pending. |
| Recompute Triggers | Planned | Always-on recompute on mutation or signal. Execution–Reasoning Trigger Contract defined. |
| Audit & Replay | Partial | Deterministic replay of governance decisions and reasoning. Determinism hashes specified; replay infrastructure pending. |
| 60-Second Orientation | Planned | First-time experience producing core outcome understanding in 60 seconds. Workflow specified; implementation pending. |
| Project MRI | Planned | Whole-portfolio outcome integrity scan. Subsystem stub; doctrinal scoping pending (RB-015 partial unblock per DL-034). |

---

## 6. Product Scope (Tiers)

Synthesized from Tier Capability Contract and Execution Posture Contract. Tier and posture interact: tier determines which capabilities are available; posture determines how much coordination authority is granted within the tier.

### Free

- **Capabilities:** 60-second orientation; outcome confidence (single outcome); basic Issue Detection; limited Recommendation Generation.
- **Posture:** Deliberate only (no coordinated mutations applied).
- **AI Limits:** Bounded compute budget; reasoning frequency throttled; AI-assisted inference unavailable or strictly bounded.
- **Sharing:** None or single-user only.
- **Integrations:** None or read-only sample integrations.
- **Intended Goal:** Demonstrate value to the individual user; convert to paid tier.

### Basic

- **Capabilities:** Full single-outcome OSLO; expanded Issue Detection; Recommendation Generation; basic reporting.
- **Posture:** Deliberate and Assisted postures available.
- **AI Limits:** Increased compute budget; AI-assisted inference enabled with disclosure.
- **Sharing:** Limited (small team; immutable shared artifacts).
- **Integrations:** Limited connector set (one or two PM tools).
- **Intended Goal:** Individual professional and small-team adoption.

### Pro

- **Capabilities:** Multi-outcome; Project MRI; Alignment Analysis; Feasibility Analysis (quantitative); advanced reporting; portfolio confidence aggregation.
- **Posture:** Deliberate, Assisted, and Delegated (where action class is delegatable and tier-permitted).
- **AI Limits:** Higher compute budget; full AI-assisted inference; learning loop active.
- **Sharing:** Team and cross-team sharing with role-aware access.
- **Integrations:** Expanded connector set; CRM/ERP read; analytics ingestion.
- **Intended Goal:** Team and program leadership; mid-market organizations.

### Enterprise

- **Capabilities:** Multi-tenant policy customization; portfolio orchestration; agent governance; full Execution Coordination including Delegated actuation; enterprise reporting; audit and compliance export.
- **Posture:** All three postures with custom-tier delegation; per-workspace posture configuration; lifecycle-gated posture transitions.
- **AI Limits:** Enterprise compute budget; on-prem / in-VPC inference options; custom rule and policy libraries.
- **Sharing:** Enterprise sharing controls; SSO; permission scopes; audit logs.
- **Integrations:** Full integration suite; custom connector framework; SCIM; SAML.
- **Intended Goal:** Enterprise-scale outcome orchestration with governance, compliance, and integration depth.

**Note on tier × posture × action class:** The Governance Decision Matrix (Tier × Posture × Action Class) is the canonical reference for what is authorized in which combination. Each ActionClass declares its tier requirements, posture requirements, and delegation eligibility.

---

## 7. Roadmap Capability Areas

### Planning Intelligence

- **Description.** Intake, normalization, claim extraction, SMART validation, alignment analysis, feasibility analysis — the analytical pass that converts user inputs into governed canonical knowledge with confidence scoring. Planning Intelligence runs across **two active Release 1 assessment horizons**: a **Fast Assessment** pass (producing the 60-Second Orientation) and a **Deep Assessment** pass (continuing after orientation), which performs **Confidence Recalculation**, **Expanded Issue Discovery**, and **Expanded Recommendation Generation**. Both horizons are Active V1; Deep Analysis improves understanding and does not govern or accept it.
- **Current Maturity.** Partial. Framework specified; per-driver scoring frameworks defined; production rule library partial.
- **Major Missing Capabilities.** Full Reasoning rule library; AI-assisted inference activation; multi-stakeholder alignment analysis; quantitative feasibility modeling.
- **Strategic Importance.** Critical. Planning Intelligence is the entry-point capability; without it, downstream value (Confidence, Issues, Recommendations) cannot be produced.
- **Suggested Sequencing.** First. Foundation for all other capabilities.

### Outcome Confidence

- **Description.** Composite confidence scoring per outcome, decomposed by driver, explainable back to evidence. Per Doctrine 06.
- **Current Maturity.** Partial. Confidence model framework defined; per-driver evaluation specified; aggregation logic pending.
- **Major Missing Capabilities.** Production scoring pipeline; per-driver weighting calibration; confidence trajectory tracking; confidence decay rules.
- **Strategic Importance.** Critical. Confidence is the headline OSLO output — what users see first and reference throughout.
- **Suggested Sequencing.** First. Pairs with Planning Intelligence as the core value loop.

### Context Plane

- **Description.** Cross-cutting ingestion, normalization, staging, identity, time semantics, promotion-readiness for external context.
- **Current Maturity.** Partial. Two integrity contracts operative; classification ratified; specification and follow-on documents pending.
- **Major Missing Capabilities.** Full Specification; Promotion Contract; signal taxonomy; assembly interface; failure-mode coverage; ingestion connectors at scale.
- **Strategic Importance.** Critical. Context Plane gates everything else; without robust ingestion and provenance, downstream layers cannot trust their inputs.
- **Suggested Sequencing.** First. Parallel to Planning Intelligence; both foundational.

### Governance Engine

- **Description.** Policy-driven authorization, exposure governance, outcome resolution. Tier × Posture × Action authorization at runtime.
- **Current Maturity.** Partial. Layer Specification mature; Decision Matrix defined; policy engine implementation pending.
- **Major Missing Capabilities.** Production policy engine; per-tenant policy customization; lifecycle-aware authorization; delegated authorization workflows; audit log infrastructure.
- **Strategic Importance.** Critical. Required for any non-trivial AI behavior; required for enterprise adoption.
- **Suggested Sequencing.** Second. Depends on Planning Intelligence + Judgment producing Issues to disposition.

### Collaboration

- **Description.** Multi-user OSLO instances; role-aware access; collaboration around (not inside) canonical knowledge.
- **Current Maturity.** Planned. Collaboration role model not yet anchored (RB-012).
- **Major Missing Capabilities.** Role model; permission scopes; concurrent-user UX; collaboration notifications; immutable shared artifacts.
- **Strategic Importance.** High for team adoption; required for Pro and Enterprise tiers.
- **Suggested Sequencing.** Third. Depends on Planning Intelligence + Confidence having stabilized.

### Sharing

- **Description.** Immutable shared artifacts (Executive Summary, Charter, OSLO Explanations); external sharing with audit.
- **Current Maturity.** Planned.
- **Major Missing Capabilities.** Artifact rendering; immutability enforcement; external share controls; expiration; revocation.
- **Strategic Importance.** High for cross-team and stakeholder communication; viral adoption surface.
- **Suggested Sequencing.** Third. Pairs with Collaboration and Reporting.

### Reporting & Analytics

- **Description.** Versioned, commentable outputs; analytics across outcomes; portfolio views.
- **Current Maturity.** Planned.
- **Major Missing Capabilities.** Report templates; comment threading; versioning; portfolio aggregation; analytics dashboards.
- **Strategic Importance.** High. Required for Pro tier value; required for executive consumption.
- **Suggested Sequencing.** Third. After Collaboration and Sharing.

### Execution Intelligence

- **Description.** Continuous signal ingestion from external execution tools; drift detection between plan and reality; recompute triggers.
- **Current Maturity.** Planned. Execution Layer Specification defined; observability path designed.
- **Major Missing Capabilities.** Signal connectors at scale; normalization; drift detection rules; recompute trigger orchestration; multi-source temporal reconciliation.
- **Strategic Importance.** High. Differentiates OSLO from static planning tools; foundation for orchestration.
- **Suggested Sequencing.** Fourth. Depends on stable Knowledge + Reasoning + Judgment.

### Agent Governance

- **Description.** Authorization, posture-gating, audit for AI/agent actions. Per Agent Execution Authorization Contract.
- **Current Maturity.** Planned. Contract specified; implementation pending.
- **Major Missing Capabilities.** Agent identity model; per-agent posture/tier mapping; action class registry; rollback infrastructure; audit log integration.
- **Strategic Importance.** High. Foundational for any autonomous behavior; enterprise requirement.
- **Suggested Sequencing.** Fourth. Depends on Governance Engine maturity.

### Integrations

- **Description.** Connector library across PM, communication, CRM/ERP, calendar, analytics, identity.
- **Current Maturity.** Planned.
- **Major Missing Capabilities.** Connector framework; per-connector implementation; auth flows; rate limiting; mapping libraries.
- **Strategic Importance.** Critical for adoption; OSLO must meet users where they work.
- **Suggested Sequencing.** Fourth-Fifth. Connector breadth grows continuously; first connectors paired with Execution Intelligence and Context Plane.

### Team & Program Management

- **Description.** Multi-outcome views; cross-outcome dependencies; program-level confidence and integrity; portfolio orchestration.
- **Current Maturity.** Planned.
- **Major Missing Capabilities.** Multi-outcome data model at scale; cross-outcome dependency graph; portfolio aggregation; program-level posture configuration.
- **Strategic Importance.** High. Required for Pro and Enterprise tiers; differentiates from single-outcome tools.
- **Suggested Sequencing.** Fifth. Depends on single-outcome maturity across all foundational areas.

### Outcome Orchestration (Long-Term)

- **Description.** Closed-loop continuous alignment of execution to outcomes via authorized action coordination across humans, agents, and external tools.
- **Current Maturity.** Future. Architecture supports; activation phased.
- **Major Missing Capabilities.** Closed-loop control mechanisms; orchestration policy framework; multi-tool action coordination; orchestration audit at scale.
- **Strategic Importance.** Long-term strategic differentiator. The vision endpoint.
- **Suggested Sequencing.** Sixth and ongoing. Activated incrementally per posture and tier.

---

## 8. Engineering Initiative Recommendations

Initiative-level decomposition for engineering planning. Project-level breakdown included; user stories and tasks deliberately out of scope.

### Initiative I1 — Planning Intelligence Foundation

- **Purpose.** Production-ready intake → claim extraction → Reasoning → Judgment pipeline producing scored Issues per outcome.
- **Projects.** P1.1 Intake & Multi-Source Normalization; P1.2 Reasoning Rule Engine + Rule Library v1; P1.3 Judgment Layer with Confidence/Severity Scoring; P1.4 Determinism + Replay Infrastructure.
- **Potential Features.** Free-text intake; document upload; structured form intake; SMART validation; gap detection; severity assignment; confidence aggregation; replay testing harness.
- **Dependencies.** Context Plane (I3) for ingestion; Knowledge Layer (I2) for canonical storage.
- **Expected User Value.** First measurable OSLO output: an Issue-and-Confidence view of an outcome.
- **Suggested Priority.** Critical.

### Initiative I2 — Knowledge Layer Implementation

- **Purpose.** Production canonical Knowledge Layer per Specification, with append-only versioning, epistemic status enforcement, immutable snapshots.
- **Projects.** P2.1 Canonical Schema and Storage Engine; P2.2 Command & Write Contract Implementation; P2.3 Snapshot & Projection Infrastructure; P2.4 Replay and Determinism Guarantees.
- **Potential Features.** Knowledge writes with epistemic tagging; snapshot generation; versioned history queries; relationship graph queries; replay test fixtures.
- **Dependencies.** Governance Layer (I4) for authorization gate; Context Plane (I3) for source of promotion-ready content.
- **Expected User Value.** Stable, trustworthy memory underlying all OSLO output.
- **Suggested Priority.** Critical.

### Initiative I3 — Context Plane Implementation

- **Purpose.** Production Context Plane handling ingestion, normalization, staging, identity, time semantics, and promotion-readiness.
- **Projects.** P3.1 Ingestion Framework + Source Taxonomy; P3.2 Normalization Pipeline; P3.3 Staging Storage; P3.4 Identity + Time Semantics Enforcement; P3.5 Promotion Contract Implementation.
- **Potential Features.** Multi-source ingestion (text, docs, API, signals); idempotent ingestion; raw record identity; time-bundle storage; promotion-readiness scoring; quarantine and rejection.
- **Dependencies.** Knowledge Layer (I2) downstream; integration connectors (I9) upstream.
- **Expected User Value.** Reliable, traceable, provenance-preserving ingestion across all sources.
- **Suggested Priority.** Critical.

### Initiative I4 — Governance Engine

- **Purpose.** Production policy-driven authorization, exposure governance, action authorization implementing Triple Intersection Rule.
- **Projects.** P4.1 Policy Engine; P4.2 Governance Decision Matrix Implementation; P4.3 Per-Tenant Policy Customization; P4.4 Audit Log Infrastructure; P4.5 Outcome Resolution Workflows.
- **Potential Features.** Authorization API; policy versioning; per-tenant overrides; audit query API; outcome resolution UI.
- **Dependencies.** Judgment Layer (I1) for Issues to disposition; Posture, Tier, Action Class contracts.
- **Expected User Value.** Trustworthy, configurable governance enabling tiered AI behavior.
- **Suggested Priority.** Critical.

### Initiative I5 — Communication Layer Implementation

- **Purpose.** Production rendering and disclosure of governed system behavior across surfaces, with posture-aware honesty.
- **Projects.** P5.1 Communication Unit Pipeline; P5.2 Surface Renderers (UI, Summary, Detail, Export); P5.3 Posture Disclosure Templates; P5.4 Multi-Channel Notification Delivery.
- **Potential Features.** Posture badges; delegated-execution disclosures; surface-invariant meaning preservation; templated disclosures; notification routing.
- **Dependencies.** Governance Layer (I4) outputs.
- **Expected User Value.** Trustworthy, transparent, posture-honest user experience.
- **Suggested Priority.** High (paired with each upstream initiative).

### Initiative I6 — Outcome Confidence Scoring

- **Purpose.** Production composite confidence scoring per outcome, decomposed by driver, explainable back to evidence.
- **Projects.** P6.1 Per-Driver Scoring Implementation (Clarity, Alignment, Feasibility); P6.2 Driver Aggregation Logic; P6.3 Confidence Trajectory Tracking; P6.4 Confidence Display & Drilldown.
- **Potential Features.** Composite score; driver breakdown; trend display; evidence drilldown; confidence-band UX.
- **Dependencies.** Planning Intelligence (I1); Knowledge Layer (I2).
- **Expected User Value.** The headline OSLO signal — explainable outcome confidence.
- **Suggested Priority.** Critical.

### Initiative I7 — Recommendation Engine

- **Purpose.** Issue-anchored action proposals constrained by current Posture, Tier, and Governance policy.
- **Projects.** P7.1 Action Class Catalog; P7.2 Recommendation Generation Logic; P7.3 Recommendation UI with Acceptance Flow; P7.4 Recommendation-to-Execution Handoff.
- **Potential Features.** Per-Issue recommendation; confirmation flow; delegation flow; rejection capture; rationale display.
- **Dependencies.** Judgment Layer (I1); Governance Engine (I4); Execution Coordination (I8) for delegated actions.
- **Expected User Value.** Actionable forward path from understanding to action.
- **Suggested Priority.** High.

### Initiative I8 — Execution Coordination (Observability Phase)

- **Purpose.** Always-on observability path of Execution Layer: signal ingestion + recompute triggers, without actuation.
- **Projects.** P8.1 Signal Ingestion Connectors (Jira, Asana, Planner, Linear, calendar, communication); P8.2 Signal Normalization + Linking; P8.3 Recompute Trigger Logic; P8.4 Drift Detection Rules.
- **Potential Features.** Multi-tool signal ingestion; auto-link to canonical elements; trigger-based recompute; drift surfacing.
- **Dependencies.** Context Plane (I3); Reasoning + Judgment (I1).
- **Expected User Value.** Continuous outcome awareness as execution unfolds.
- **Suggested Priority.** High.

### Initiative I9 — Integrations Framework + Connectors v1

- **Purpose.** Connector framework + initial connector library across PM, communication, identity, calendar.
- **Projects.** P9.1 Connector Framework (auth, rate limiting, mapping); P9.2 Jira Connector; P9.3 Asana / Linear / Planner Connector; P9.4 Slack/Teams Connector; P9.5 Google/Microsoft Calendar Connector; P9.6 SSO/SAML.
- **Potential Features.** Per-connector OAuth flows; mapping configuration; sync status; error recovery.
- **Dependencies.** Context Plane (I3) for ingestion; Communication Layer (I5) for notifications.
- **Expected User Value.** Meet users where they work; expand OSLO's signal coverage.
- **Suggested Priority.** High.

### Initiative I10 — Collaboration + Sharing

- **Purpose.** Multi-user OSLO instances with role-aware access, immutable shared artifacts, external sharing controls.
- **Projects.** P10.1 Role Model + Permission Scopes; P10.2 Concurrent-User UX; P10.3 Immutable Artifact Rendering; P10.4 External Sharing with Audit; P10.5 Comment Threading on Shared Artifacts.
- **Potential Features.** Workspace roles; per-outcome access; shareable Executive Summary; comment threads; expiration; revocation.
- **Dependencies.** Stable Planning Intelligence + Confidence; Communication Layer (I5).
- **Expected User Value.** Team adoption; stakeholder visibility.
- **Suggested Priority.** High (for Basic/Pro tier launch).

### Initiative I11 — Reporting & Analytics

- **Purpose.** Versioned, commentable reports; analytics across outcomes; portfolio views.
- **Projects.** P11.1 Report Template Engine; P11.2 Executive Summary; P11.3 Charter Report; P11.4 OSLO Explanation Generator; P11.5 Portfolio Analytics.
- **Potential Features.** Templated reports; commentable; versioned; portfolio confidence; outcome inventory.
- **Dependencies.** Collaboration + Sharing (I10).
- **Expected User Value.** Executive consumption; cross-stakeholder communication.
- **Suggested Priority.** High.

### Initiative I12 — Execution Coordination (Actuation Phase)

- **Purpose.** Posture-gated coordinated mutations to external tools under explicit Governance authorization.
- **Projects.** P12.1 Action Class Registry; P12.2 Assisted-Posture Confirmation Flow; P12.3 Delegated-Posture Authorization Workflows; P12.4 Rollback Infrastructure; P12.5 Cross-Tool Coordination.
- **Potential Features.** Per-action confirmation; delegated boundaries; rollback per-action; tool-specific mutation libraries.
- **Dependencies.** Governance Engine (I4); Execution Observability (I8); Integrations (I9).
- **Expected User Value.** OSLO acts on the user's behalf within explicit, trustworthy bounds.
- **Suggested Priority.** Medium (post foundational stability).

### Initiative I13 — Agent Governance

- **Purpose.** Authorization, posture-gating, audit for AI/agent actions per Agent Execution Authorization Contract.
- **Projects.** P13.1 Agent Identity Model; P13.2 Per-Agent Posture / Tier Mapping; P13.3 Agent Action Class Registry; P13.4 Agent Audit Log Integration; P13.5 Agent Rollback.
- **Potential Features.** Agent registration; agent-scoped authorization; agent action audit; agent rollback API.
- **Dependencies.** Governance Engine (I4); Execution Coordination (I12).
- **Expected User Value.** Enterprise-grade governed agent behavior.
- **Suggested Priority.** Medium (Pro/Enterprise differentiator).

### Initiative I14 — Team & Program Management

- **Purpose.** Multi-outcome views; cross-outcome dependencies; program-level confidence; portfolio orchestration foundation.
- **Projects.** P14.1 Multi-Outcome Data Model; P14.2 Cross-Outcome Dependency Graph; P14.3 Portfolio Confidence Aggregation; P14.4 Program-Level Posture Configuration.
- **Potential Features.** Outcome list; dependency view; portfolio dashboard; program posture controls.
- **Dependencies.** Stable single-outcome OSLO across foundational initiatives.
- **Expected User Value.** Pro and Enterprise scale.
- **Suggested Priority.** Medium.

---

## 9. Open Questions

Captured during baseline synthesis. Documented for engineering and product context; not subject to governance analysis here.

1. **Per-driver confidence aggregation weighting.** The composite confidence formula across Clarity, Alignment, Feasibility, evidence strength, assumption stability, etc., is not yet specified. Whether weights are uniform, domain-dependent, tenant-configurable, or learned is undefined.

2. **Quantitative feasibility threshold.** Current feasibility is logical (binary-ish). The threshold at which quantitative feasibility (probabilistic modeling) is required is undefined; near-term scope likely remains logical with quantitative as future-state.

3. **Multi-stakeholder alignment scoring.** Whether stakeholder positions are weighted (e.g., by role; by influence) or treated equally is undefined.

4. **Recommendation acceptance fallback.** What happens when a user rejects a recommendation without providing a reason — does the recommendation suppress for some interval; recur immediately; require explanation? Not specified.

5. **Drift detection sensitivity.** Continuous monitoring will generate drift signals; the threshold between "noise" and "actionable drift" is undefined and likely tenant-tunable.

6. **Connector taxonomy.** The complete connector roadmap (which tools, in what order, at what depth) is not enumerated in the corpus.

7. **Agent identity model.** Whether agents are first-class users, special workspace members, or distinct identity classes is not specified.

8. **Lifecycle stages.** Several specs reference LifecycleContext but the canonical lifecycle stage set (Initiation / Planning / Execution / Monitoring / Closure or alternative) is not fully unified.

9. **Tier × Posture × Action Class matrix completeness.** The Governance Decision Matrix is specified at v1.0 but per-action-class population is incomplete.

10. **Per-tenant policy customization scope.** What can each tenant customize at the policy level versus what is platform-fixed is undefined.

11. **Rollback per ActionClass.** Each ActionClass declares rollback requirements; whether universal rollback is achievable or whether some actions are necessarily irreversible (and therefore Deliberate-posture-only) requires per-action analysis.

12. **Knowledge Layer schema evolution.** As OSLO matures, canonical schema will evolve. Migration strategy (in-place migration vs versioned schemas vs forward-only) is not specified.

13. **Multi-tenant isolation guarantees.** The specific isolation model (shared infrastructure with logical partitioning vs single-tenant deployments vs hybrid) is not specified.

14. **Determinism guarantee scope.** Determinism is required for Reasoning and Judgment; the scope of "identical inputs" (including model versions for AI-assisted inference) requires precise specification.

15. **Project MRI scope and capabilities.** Project MRI subsystem is stub-only; its analytical scope, output format, and integration with main OSLO loop require doctrinal scoping.

16. **First-time experience (60-Second Standard).** The exact intake → first-confidence-display flow within 60 seconds is conceptually defined but not implementation-specified.

17. **Communication compression rules.** What may be compressed (verbosity, step-by-step detail, bundling) versus what must be preserved (epistemic state, posture influence, governance authorization, uncertainty) is bounded conceptually but requires per-surface specification.

18. **Notification delivery infrastructure.** Channels (email, in-app, mobile, integration-routed) and priority tiers are undefined at implementation level.

19. **AI inference posture interactions.** How AI-assisted inference behaves across the three postures (Deliberate / Assisted / Delegated) requires explicit specification.

20. **Surface B / native repository reconciliation.** The relationship between the architectural Layer Specifications and the native repository's doctrinal framing remains under governance review (GOV-ARCH-001, GOV-ARCH-001A, GOV-ARCH-000); resolution may affect implementation reference choices.

---

*Engineering Architecture Baseline v1 complete. Designed for engineering execution and roadmap planning. To be revised as architecture matures and as governance work resolves outstanding items.*

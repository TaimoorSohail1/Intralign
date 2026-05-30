# Canonical Definitions

## Status

**Operative — Governance-Tier Orientation Registry (per DL-036)**

This file is the canonical Governance-tier orientation registry. It compiles canonical concepts with citations to their Content-tier sources. It does not establish authority. It is the citation index for contributors and AI systems. Authority resides in the Content tier (Doctrine and Constitution) per DL-033.

### Surface Authority Rule (per DL-036 R1)

- **Root `canonical_definitions.md` (this file)** — Governance-tier orientation registry. Compiles citations.
- **Constitution Article 10** (`01_governance/constitution/10_canonical_definitions.md`) — Content-tier (Constitution) definitional surface.
- **Synchronization rule:** Where a concept is defined in both surfaces, Article 10's definition is the authoritative operational expression; this file compiles citation to Article 10 and to the doctrinal source (where applicable).
- **Where defined in Doctrine only:** Doctrine is authoritative; both surfaces reference the doctrinal source.
- **Doctrine vs Article 10 substantive conflict (per DL-036 Clarification #1):** Doctrine prevails per DL-033. The divergence is a Conflicting-status item; reconciliation occurs through the appropriate downstream backlog item.
- **New canonical definitions** enter through the Content tier first via Proposal-Review-Decision, then propagate to this registry as clerical updates.

### Status Taxonomy (per DL-036 R2)

Each entry carries exactly one status flag:

- **Canonical** — established with a defining statement in a Content-tier source (Doctrine or Constitution), consistent across all references.
- **Provisional** — established with a defining statement but explicitly marked as not yet ratified to its final status (e.g., Portfolio Cognition per DL-034).
- **Proposed** — referenced as if canonical but lacking a unified defining statement; placeholder pending Decision.
- **Conflicting** — defined or referenced with divergent meanings across multiple canonical sources; reconciliation pending under a specific backlog item.
- **Undefined** — named in canonical or implementation content but has no defining statement in any source; doctrinal-stub candidate.
- **Duplicate** — appears under two or more names referring to the same conceptual entity; one canonical, the others formally deprecated.

### Status-Change Rules (per DL-036 R3)

- Transitions to Canonical require Proposal-Review-Decision under Framework 001/001A.
- Clerical registry updates for concepts with established Content-tier sources do not require fresh PRD; they are recorded in the changelog under the authority of DL-036 (precedent established per Clarification #3).
- Downgrades (e.g., Canonical → Conflicting) require PRD that records the source of conflict.

### Tie-Breaking Rule for Status-Flag Exclusivity (per DL-036 Clarification #8)

When multiple flags could plausibly apply, the higher-priority flag prevails. Priority order:

1. Conflicting
2. Undefined
3. Proposed
4. Provisional
5. Duplicate
6. Canonical

### "Provisional" Disambiguation (per DL-036 R6)

- **Provisional (Epistemic Label)** — Used in `03_implementation_specs/05_component_system_specification.md` as one of the Epistemic Label types. Reserved for RB-007 reconciliation.
- **Provisional (Governance Status)** — Used in this taxonomy and in Decisions (e.g., Portfolio Cognition per DL-034).

Registry entries use qualified forms where ambiguity could arise.

### Legacy Flag Migration (per DL-036 Clarification #2)

- Pre-DL-036 entries flagged "Established" are migrated to "Canonical".
- Pre-DL-036 entries flagged "Established (split source)" are migrated to "Conflicting", except where Clarification #7 applies (Organizational Cognition Arc → Duplicate).

All entries cite their source location.

---

## Foundational Concepts

### OSLO

**Status:** Conflicting
**Source:** `repository_manifest.md` (Purpose, What OSLO Is)
**Definition (manifest):** OSLO is a governed cognitive architecture designed to preserve organizational understanding, outcome integrity, and decision continuity as work systems become increasingly dynamic, distributed, and autonomous.
**Acronym (manifest):** Outcome-Driven Strategic Lifecycle Orchestration.
**Note:** The acronym is asserted only in the manifest. It has no anchoring in doctrine or Constitution. The term *Lifecycle* is in potential tension with doctrinal claims that integrity states are "not workflow phases." Reconciliation pending.

### Foundational Thesis

**Status:** Canonical
**Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` (Article 1)
**Definition:** OSLO exists to preserve trustworthy organizational understanding under dynamic conditions.

---

## Reality and Integrity Concepts

### Outcome Space

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/constitution/03_workspace_constitution.md` (Article 13)
**Definition:** A governed workspace representing the evolving synthesis of organizational understanding surrounding intended outcomes.

### Outcome Integrity

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` (Article 3)
**Definition:** The degree of coherence between Intended Reality and Current Reality under evolving organizational conditions.

### Intended Reality

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/04_outcome_integrity_framework.md`
**Definition:** What the organization believes should exist.

### Current Reality

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/04_outcome_integrity_framework.md`
**Definition:** What OSLO currently believes actually exists based on evidence and interpretation.

### Integrity Gap

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/04_outcome_integrity_framework.md`
**Definition:** The degree of divergence between Intended Reality and Current Reality.

---

## Epistemic Concepts

### Dynamic Epistemic Synthesis

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` (Article 7)
**Definition:** The continuously evolving synthesis of evidence, assumptions, interpretations, governance conditions, intended reality, current reality, confidence, organizational overrides, and understanding boundaries. Identified as the canonical truth structure of OSLO.

### Epistemic Object Types

**Status:** Conflicting
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` (Article 8)
**Definition:** Five distinguished epistemic kinds — Facts, Inferences, Assumptions, Recommendations, Conflicts.
**Note:** `03_implementation_specs/05_component_system_specification.md` lists nine "types" by combining the canonical five with additional confidence-state labels (Unknown, Provisional, Weakly Supported, Validated). The conflation between *epistemic kind* and *epistemic strength* requires governance reconciliation.

### Facts

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** Verified organizational reality.

### Inferences

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** OSLO interpretations based on evidence.

### Assumptions

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** Accepted conditions lacking full validation.

### Recommendations

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** Proposed interventions or optimizations.

### Conflicts

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** Competing interpretations or unresolved divergence.

### Ambiguity

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md` (Understanding Boundaries section)
**Definition:** A condition in which the organization lacks clarity.

### Understanding Boundary

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` (Article 9)
**Definition:** A condition in which OSLO lacks sufficient evidence or visibility. Distinct from Ambiguity.

### Progressive Epistemic Depth

**Status:** Canonical
**Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` (Article 10)
**Definition:** OSLO exposes complexity progressively, proportional to consequence, uncertainty, and governance importance.

### Organizational Epistemic Memory

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/03_epistemic_system_model.md`
**Definition:** The preserved historical record of what the organization believed, why it believed it, confidence conditions, unresolved ambiguity, governance conditions, and rationale.

---

## Confidence Concepts

### Confidence

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/06_confidence_understanding_model.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` (Article 30)
**Definition:** The trustworthiness of organizational understanding. Not prediction certainty.

### Confidence Maturity

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` (Article 32); `01_governance/doctrine/04_outcome_integrity_framework.md`
**Definition:** The maturity and quality of the system's understanding and evidence foundation. Stated progression: Initial → Expanded → Validated → Continuous.

### Understanding Evolution

**Status:** Canonical
**Source:** `01_governance/constitution/10_canonical_definitions.md`; `01_governance/doctrine/06_confidence_understanding_model.md`
**Definition:** The longitudinal evolution of organizational understanding over time.

---

## Governance Concepts

### Outcome Integrity Policies

**Status:** Canonical
**Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` (Article 20)
**Definition:** Human-readable organizational doctrine governing outcome integrity. Explicitly not raw workflow rule engines or automation scripting.

### Human Override

**Status:** Canonical
**Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` (Article 21)
**Definition:** A human decision that diverges from OSLO's interpretation. Overrides are permitted; divergence must remain visible and historically preservable.

### Governance Escalation

**Status:** Canonical
**Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` (Article 22)
**Definition:** Escalation that scales proportionally to consequence, confidence degradation, governance severity, and organizational doctrine.

---

## Workspace and Surface Concepts

### Understanding (workspace center)

**Status:** Canonical
**Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` (Article 12)
**Definition:** The conceptual center of the system. Artifacts support understanding; understanding does not support artifacts.

### What OSLO Understands

**Status:** Canonical
**Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` (Article 14)
**Definition:** The primary workspace surface, comprising confidence, integrity state, intended vs current reality, understanding evolution, key concerns, recommendations, and governance conditions.

### Artifact

**Status:** Proposed
**Source:** Used throughout doctrine and Constitution; primary categories enumerated in `01_governance/doctrine/05_workspace_navigation_doctrine.md` and `01_governance/constitution/03_workspace_constitution.md` (Article 15) as Intent, Context, Execution, Schedule, Resources.
**Definition:** *No single defining statement exists in the canon. Placeholder pending governance ratification.*

### Attention Queue

**Status:** Proposed
**Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `03_implementation_specs/03_outcome_space_workspace_wireframes.md`; `03_implementation_specs/04_core_navigation_information_architecture.md`
**Definition:** *No single defining statement exists in the canon. Referenced as a "persistent operational intelligence surface" in doctrine and as a queue sorted by outcome impact in specs. Reconciliation required.*

### Persistent Confidence Shell

**Status:** Canonical
**Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` (Article 17)
**Definition:** Persistent epistemic infrastructure that keeps confidence and integrity state globally visible. Not a report.

### Companion Intelligence Panel

**Status:** Canonical
**Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` (Article 18)
**Definition:** A contextual right-side panel for OSLO conversation. Conversation supports understanding; understanding does not support conversation.

### Project MRI

**Status:** Proposed
**Source:** `repository_manifest.md` (section `04_project_mri`); referenced as a PLG moment in `00_raw_transcript/00_transcript_index.md` and in `03_implementation_specs/02_plg_60_second_flow_wireframes.md`
**Definition:** *Manifest scope only — a structural intelligence surface that helps users understand ambiguity, fragility, confidence, outcome integrity risk, understanding gaps, and interpretation drift exposure. Subsystem remains under active development.*

---

## Maturity and Progression Concepts

### Confidence Maturity Progression

**Status:** Canonical
**Source:** `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` (Article 32); `03_implementation_specs/08_state_logic_state_machines.md`
**Stated progression:** Initial → Expanded → Validated → Continuous.

### Outcome Integrity States

**Status:** Conflicting
**Source:** `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` (Article 33); `03_implementation_specs/08_state_logic_state_machines.md`
**Definition:** Epistemic and governance states, not workflow phases.
**Note:** Three layers list different state sets. Doctrine 04 lists: Initial, Clarified, Aligned, Feasible, Governed, Execution Ready, Fragile, Drift Emerging. Article 33 omits Initial. Spec 08 adds "At Risk." Wireframes use compound "Clarified but Fragile." Reconciliation required.

### Organizational Cognition Arc (Deprecated — see Cognition Scope)

**Status:** Duplicate (per DL-036 R5; extends DL-034 reframing per Clarification #7)
**Canonical Name:** Cognition Scope (Axis A)
**Source:** `01_governance/doctrine/02_organizational_cognition_model.md` (historical doctrinal source for the concept now named Cognition Scope).
**Deprecation Note:** Predecessor name for the Cognition Scope axis of the OSLO Evolution Framework. Substantive content is canonized through the Cognition Scope entry below. This entry extends the DL-034 reframing (CHG-019) into a formal Duplicate-status deprecation per DL-036 Clarification #7. Contributors should cite Cognition Scope (Axis A) rather than this predecessor name.

### OSLO Evolution Framework

**Status:** Canonical
**Source:** `01_governance/decisions/rb_003_disposition.md`; DL-034.
**Definition:** The canonical multi-axis progression taxonomy for OSLO's evolution. Comprises four distinct but correlated axes: Cognition Scope, Product Identity, Trust Gradient, Execution Depth. The four axes are independently measurable and converge structurally at terminal Outcome Orchestration Infrastructure (Trust Gradient terminates at Orchestration Authority, the trust-dimensional articulation of the same endpoint).

### Cognition Scope (Axis A)

**Status:** Canonical
**Source:** `01_governance/doctrine/02_organizational_cognition_model.md`; DL-034.
**Definition:** The scale-of-cognition axis of the OSLO Evolution Framework. Stages: Individual Cognition → Shared Understanding → Governed Organizational Cognition → Outcome Orchestration Infrastructure. Four stages, ratified. Portfolio Cognition is a provisional long-term capability, not a ratified stage.

### Product Identity (Axis B)

**Status:** Canonical
**Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md`; DL-034.
**Definition:** The product-perception axis of the OSLO Evolution Framework. Stages: Planning and Understanding Intelligence → Strategic Cognition Environment → Governed Organizational Cognition → Outcome Orchestration Infrastructure. Stage 3 label "Governed Organizational Cognition" (Doctrine 09) prevails over Article 40's provisional "Governance Infrastructure" label.

### Trust Gradient (Axis C)

**Status:** Canonical
**Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md`; `01_governance/constitution/08_product_evolution_constitution.md` (Article 41); DL-034.
**Definition:** The trust-grant axis of the OSLO Evolution Framework. Steps: OSLO Observations → OSLO Recommendations → OSLO Operational Influence → OSLO Orchestration Authority. Doctrine and Constitution aligned at ratification.

### Execution Depth (Axis D)

**Status:** Canonical
**Source:** `01_governance/doctrine/10_execution_orchestration_maturity.md`; `01_governance/constitution/08_product_evolution_constitution.md` (Article 43); DL-034.
**Definition:** The execution-interaction-depth axis of the OSLO Evolution Framework. Phases (zero-indexed): Phase 0 Execution-State Ingestion → Phase 1 Observational Intelligence → Phase 2 Guided Optimization → Phase 3 Assisted Coordination → Phase 4 Outcome Orchestration Infrastructure. Doctrine and Constitution aligned at ratification. Doctrine 10's Long-Term Direction items (Portfolio Cognition, organizational systems cognition, cascading dependency awareness, organizational drift analysis, cross-initiative consequence modeling) remain provisional long-term capabilities.

---

## Emotional Posture Concepts

### Calm Strategic Augmentation

**Status:** Canonical
**Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md`; `01_governance/constitution/09_emotional_interaction_constitution.md` (Article 45)
**Definition:** The dominant emotional posture of OSLO.

### Progressive Visibility

**Status:** Canonical
**Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md`; `01_governance/constitution/05_intelligence_visibility_constitution.md` (Article 25)
**Definition:** The more stable understanding becomes, the more OSLO recedes. The more uncertainty or consequence emerges, the more visible OSLO becomes.

---

## Doctrinal Concepts Registered by DL-036 (R4)

The following nine canonical doctrinal concepts are registered using existing Doctrine sources only. No new doctrine is introduced. Each registration cites the existing doctrinal source. Status: Canonical. Per Clarification #3, R4 is PRD-authorized at the Resolution level by DL-036; per-entry registrations are clerical.

### Dynamic Systems Orientation

**Status:** Canonical
**Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md` (Dynamic Systems Orientation section)
**Definition:** The doctrinal stance that organizations evolve, interpretations drift, assumptions weaken, evidence changes, and stakeholder understanding diverges. Therefore truth cannot be static; OSLO must continuously synthesize understanding.

### Constitutional Principle (Design Tradeoff Test)

**Status:** Canonical
**Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md` (closing section)
**Definition:** The design tradeoff test: "Does this improve or degrade trustworthy organizational understanding under dynamic conditions?" Applied as the highest-order evaluation criterion for major design tradeoffs.

### Epistemic Governance

**Status:** Canonical
**Source:** `01_governance/doctrine/02_organizational_cognition_model.md` (Governed Organizational Cognition section)
**Definition:** The form of governance in which an organization governs understanding quality, confidence conditions, assumptions, drift, escalation, and outcome integrity. Distinct from procedural or workflow governance.

### Flawed Intended Reality Handling

**Status:** Canonical
**Source:** `01_governance/doctrine/07_governance_policy_doctrine.md` (Flawed Intended Reality Handling section)
**Definition:** Four-stage progressive escalation when intended reality appears structurally incoherent: (1) Clarification; (2) Structural concern; (3) Coherence challenge; (4) Alternative intended realities.

### Stability vs Movement

**Status:** Canonical
**Source:** `01_governance/doctrine/06_confidence_understanding_model.md` (Stability vs Movement section)
**Definition:** The doctrinal posture that OSLO should feel structurally calm and intellectually evolving. Stable structures: workspace, navigation, understanding shell. Evolution appears where meaning changes.

### Shared Cognition Principle

**Status:** Canonical
**Source:** `01_governance/doctrine/08_collaboration_shared_cognition.md` (Shared Cognition Principle section)
**Definition:** OSLO optimizes for shared understanding quality, not merely for communication or commenting.

### Narrative Views

**Status:** Canonical
**Source:** `01_governance/doctrine/08_collaboration_shared_cognition.md` (Narrative Views section)
**Definition:** Contextual understanding narratives generated by OSLO (executive summaries, sponsor updates, governance reviews, outcome briefings). Views of understanding, not static reports.

### Freemium Doctrine

**Status:** Canonical
**Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md` (Freemium Doctrine section)
**Definition:** Freemium must demonstrate real intelligence value. Includes fast-pass confidence, deeper refinement, limited fixes, and meaningful understanding.

### Strategic UX Doctrine

**Status:** Canonical
**Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md` (Strategic UX Doctrine section)
**Definition:** Stable structure. Visible evolution. Progressive complexity. Governed intelligence.

---

## Deprecated Predecessor Names (per DL-036 R5)

Four predecessor names formally deprecated in the registry. Source files (Doctrine, Constitution) are not edited; deprecation operates in this registry only. Contributors encountering predecessor names in source files should consult the canonical entries indicated below.

### Strategic Arc

**Status:** Duplicate (per DL-036 R5)
**Canonical Name:** Cognition Scope (Axis A)
**Source:** `01_governance/doctrine/02_organizational_cognition_model.md` (historical doctrinal source)
**Deprecation Note:** Predecessor name for the Cognition Scope axis. Superseded by DL-034. Contributors should cite Cognition Scope (Axis A).

### Trust Evolution

**Status:** Duplicate (per DL-036 R5)
**Canonical Name:** Trust Gradient (Axis C)
**Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md` (historical doctrinal source)
**Deprecation Note:** Predecessor name for the Trust Gradient axis. Superseded by DL-034. Contributors should cite Trust Gradient (Axis C).

### Intelligence Visibility Doctrine

**Status:** Duplicate (per DL-036 R5)
**Canonical Name:** Progressive Visibility
**Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md` (Intelligence Visibility Doctrine section); substantively aligned with Article 25 (Progressive Visibility).
**Deprecation Note:** Predecessor name for Progressive Visibility. Anchored on DL-016 (Stated, grandfathered per DL-032; substantively aligned with Article 25) per DL-036 Clarification #4. Contributors should cite Progressive Visibility.

*Note: Organizational Cognition Arc is also Duplicate per R5 and Clarification #7; its entry is preserved in the Maturity and Progression Concepts section above.*

---

## Concepts Used But Not Defined

The following concepts are referenced in canonical layers without a defining statement. Each is a candidate for a doctrine-stub revision (see `revision_backlog.md`, RB-004).

- Working Memory (`03_implementation_specs/13_implementation_backlog.md`)
- Outcome Map (`03_implementation_specs/13_implementation_backlog.md`)
- Alternative Outcome Models (`03_implementation_specs/13_implementation_backlog.md`)
- Confidence Scoring Methodology (`03_implementation_specs/14_open_questions_design_risks.md` — Open Question 1)
- Assumption Expiration (referenced as example policy in `01_governance/doctrine/07_governance_policy_doctrine.md`)
- Policy DSL / Policy Grammar (implied across governance specs)
- Collaboration Role Model (Viewer, Commenter, Clarifier, Approver, Governance Reviewer, Owner — `03_implementation_specs/10_collaboration_sharing_logic.md`)
- Agent Governance (`03_implementation_specs/12_freemium_tier_behavior_logic.md`; `01_governance/doctrine/02_organizational_cognition_model.md`)
- Portfolio Cognition (`01_governance/doctrine/10_execution_orchestration_maturity.md`; `01_governance/constitution/08_product_evolution_constitution.md` Article 44)

---

## Governance Notes

1. This file is the operative Governance-tier orientation registry per DL-036. Status taxonomy declared in the Status section above.
2. The relationship between this file and `01_governance/constitution/10_canonical_definitions.md` is declared by the Surface Authority Rule (per DL-036 R1) in the Status section above.
3. Legacy "Established" entries have been migrated to "Canonical"; legacy "Established (split source)" entries have been migrated to "Conflicting" (with one exception per Clarification #7).
4. New canonical definitions must enter through the Content tier (Doctrine or Constitution) first via Proposal-Review-Decision, then propagate here as clerical updates.
5. Clerical updates that register concepts with already-canonical Content-tier sources may proceed without fresh PRD under the precedent of DL-036 R4 (Clarification #3), recorded in the changelog.

# Decision Log

## Status

**Operative — Governance Framework Active**

Repository governance is operative under Framework 001 (per DL-030) and Framework 001A (per DL-031). The founding bootstrap stipulation is recorded as DL-029. The transitional rule for pre-framework Stated decisions is recorded as DL-032.

**Grandfathered Range:** DL-001 through DL-028 are grandfathered as Stated per DL-032. They remain in effect and may be cited. Conversion of any grandfathered entry to Ratified requires a Proposal processed under Framework 001/001A.

**Post-Bootstrap Range:** DL-029 through DL-032 and all subsequent entries are processed under the operative governance lifecycle.

---

## Entry Schema

Each decision entry contains:

- **ID** — Decision identifier (DL-NNN).
- **Title** — Short descriptive title.
- **Date Recorded** — Date this entry was logged.
- **Layer** — Doctrine, Constitution, Implementation Spec, Raw Transcript, Manifest, or Root Governance.
- **Source** — Source proposal or document.
- **Decision** — The decision text.
- **Rationale** — Stated rationale.
- **Disposition** — Per Framework 001A (Accepted / Accepted with Conditions / Rejected / Deferred / Returned for Revision). Pre-framework entries use **Stated**.
- **Conditions** — Recorded only if Disposition is Accepted with Conditions.
- **Supersedes** — Prior decisions or definitions superseded.
- **Affected Artifacts** — Artifacts impacted by the decision.
- **Resulting Actions** — Repository actions taken or required.
- **Status** — Stated, Ratified, Ratified with Conditions, or other Framework 001A disposition state.

---

## Recorded Decisions

### DL-001 — Adopt the Foundational Thesis

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/01_core_philosophical_doctrine.md`; `02_ux_constitution/01_foundational_constitutional_doctrine.md` Article 1
- **Decision:** OSLO exists to preserve trustworthy organizational understanding under dynamic conditions.
- **Rationale:** Stated as the foundational thesis and the highest-order design principle.
- **Status:** Stated.

### DL-002 — Adopt Outcome Integrity as Coherence Between Realities

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/04_outcome_integrity_framework.md`; `02_ux_constitution/01_foundational_constitutional_doctrine.md` Article 3
- **Decision:** Outcome Integrity is defined as the degree of coherence between Intended Reality and Current Reality under evolving organizational conditions.
- **Status:** Stated.

### DL-003 — Adopt Dynamic Epistemic Synthesis as the Canonical Truth Structure

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 7; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q65
- **Decision:** OSLO's canonical truth object is Dynamic Epistemic Synthesis.
- **Rationale:** Truth cannot be static under evolving conditions.
- **Status:** Stated.

### DL-004 — Adopt Five Epistemic Object Types

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 8
- **Decision:** OSLO distinguishes Facts, Inferences, Assumptions, Recommendations, and Conflicts as canonical epistemic object types.
- **Status:** Stated. Conflict exists with `03_implementation_specs/05_component_system_specification.md`, which extends the list. Reconciliation pending (see `revision_backlog.md`, RB-001).

### DL-005 — Distinguish Ambiguity from Understanding Boundary

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/03_epistemic_system_model.md`; `02_ux_constitution/02_epistemic_constitution.md` Article 9
- **Decision:** Ambiguity (organizational lack of clarity) and Understanding Boundary (system lack of evidence or visibility) are distinct epistemic conditions.
- **Status:** Stated.

### DL-006 — Adopt Anti-False-Certainty Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/01_core_philosophical_doctrine.md`; `02_ux_constitution/01_foundational_constitutional_doctrine.md` Article 5
- **Decision:** OSLO must never imply unjustified certainty, hide ambiguity, obscure assumptions, or conceal interpretation instability. Uncertainty must remain structurally inspectable.
- **Status:** Stated.

### DL-007 — Adopt Human Judgment as Authoritative

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/01_core_philosophical_doctrine.md`; `02_ux_constitution/01_foundational_constitutional_doctrine.md` Article 6
- **Decision:** OSLO augments judgment, does not replace it. Human authority is final. Divergence from OSLO understanding remains visible and governable.
- **Status:** Stated.

### DL-008 — Adopt Understanding as the Center of the System

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; `02_ux_constitution/03_workspace_constitution.md` Article 12
- **Decision:** Understanding is the center of the system. Artifacts support understanding; understanding does not support artifacts.
- **Status:** Stated.

### DL-009 — Adopt the Top-Level Navigation Structure

- **Date Recorded:** Initial
- **Layer:** Doctrine; Implementation Spec; Raw Transcript
- **Source:** `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; `03_implementation_specs/04_core_navigation_information_architecture.md`; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q68
- **Decision:** Top-level navigation is Understanding, Artifacts, Attention, Simulations, Evolution, Governance.
- **Status:** Stated.

### DL-010 — Adopt Outcome Space as the Primary Operating Object

- **Date Recorded:** Initial
- **Layer:** Constitution
- **Source:** `02_ux_constitution/03_workspace_constitution.md` Article 13; `02_ux_constitution/10_canonical_definitions.md`
- **Decision:** The Outcome Space is the primary operating object — a governed workspace representing the evolving synthesis of organizational understanding surrounding intended outcomes.
- **Status:** Stated.

### DL-011 — Adopt Confidence as Trustworthiness of Understanding

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/06_confidence_understanding_model.md`; `02_ux_constitution/06_confidence_integrity_constitution.md` Article 30
- **Decision:** Confidence represents the trustworthiness of organizational understanding, not prediction certainty.
- **Status:** Stated.

### DL-012 — Adopt the Confidence Maturity Progression

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Implementation Spec
- **Source:** `01_doctrine_ontology/04_outcome_integrity_framework.md`; `02_ux_constitution/06_confidence_integrity_constitution.md` Article 32; `03_implementation_specs/08_state_logic_state_machines.md`
- **Decision:** Confidence Maturity progresses: Initial → Expanded → Validated → Continuous.
- **Status:** Stated.

### DL-013 — Persistent Confidence Shell

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; `02_ux_constitution/03_workspace_constitution.md` Article 17
- **Decision:** Confidence is persistent epistemic infrastructure, not a report. Confidence and integrity state remain globally visible.
- **Status:** Stated.

### DL-014 — Outcome Integrity States Are Not Workflow Phases

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/04_outcome_integrity_framework.md`; `02_ux_constitution/06_confidence_integrity_constitution.md` Article 33; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q57
- **Decision:** Outcome Integrity States are epistemic and governance states, not workflow phases.
- **Status:** Stated. The exact state set is inconsistent across sources; reconciliation pending (see `revision_backlog.md`, RB-001).

### DL-015 — Conversation Supports Understanding

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/05_workspace_navigation_doctrine.md`; `02_ux_constitution/03_workspace_constitution.md` Article 18; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` (OSLO Chat and Confidence Placement)
- **Decision:** Conversation supports understanding; understanding does not support conversation. OSLO Chat is contextual, not primary navigation.
- **Status:** Stated.

### DL-016 — Adopt Progressive Visibility Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/11_emotional_interaction_philosophy.md`; `02_ux_constitution/05_intelligence_visibility_constitution.md` Article 25; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q66
- **Decision:** The more stable understanding becomes, the more OSLO recedes. The more uncertainty or consequence emerges, the more visible OSLO becomes.
- **Status:** Stated.

### DL-017 — Adopt Calm Strategic Augmentation as Emotional Posture

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/11_emotional_interaction_philosophy.md`; `02_ux_constitution/09_emotional_interaction_constitution.md` Article 45; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q60
- **Decision:** OSLO should feel like calm strategic augmentation.
- **Status:** Stated.

### DL-018 — Outcome Integrity Policies Are Human-Readable Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 20
- **Decision:** Outcome Integrity Policies exist as human-readable governance doctrine, not workflow automation scripting.
- **Status:** Stated.

### DL-019 — Override Visibility

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 21
- **Decision:** Human overrides remain permissible; divergence from OSLO understanding remains visible and historically preservable.
- **Status:** Stated.

### DL-020 — Governance Escalation Is Proportional

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 22
- **Decision:** Governance escalation scales proportionally to consequence, confidence degradation, governance severity, and organizational doctrine.
- **Status:** Stated.

### DL-021 — Intended Reality Is Governable

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 24; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q64
- **Decision:** Intended Reality is a governable organizational construct, not immutable truth. OSLO may progressively clarify, challenge, and propose alternatives.
- **Status:** Stated.

### DL-022 — Disagreement Posture Is Facilitator

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_doctrine_ontology/07_governance_policy_doctrine.md`; `02_ux_constitution/04_governance_constitution.md` Article 23; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q56
- **Decision:** OSLO acts primarily as facilitated understanding refinement. It exposes divergence, compares evidence, clarifies assumptions, and illuminates tradeoffs. It avoids authoritarian posture.
- **Status:** Stated.

### DL-023 — Adopt Trust Evolution Sequence

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/09_plg_product_evolution_strategy.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 41
- **Decision:** Trust evolves: observations → recommendations → operational influence → orchestration authority.
- **Status:** Stated.

### DL-024 — Adopt Execution Maturity Phases

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_doctrine_ontology/10_execution_orchestration_maturity.md`; `02_ux_constitution/08_product_evolution_constitution.md` Article 43
- **Decision:** Execution maturity progresses: Phase 0 (ingestion) → Phase 1 (observational intelligence) → Phase 2 (guided optimization) → Phase 3 (assisted coordination) → Phase 4 (orchestration infrastructure).
- **Status:** Stated.

### DL-025 — Freemium Must Include Deep Refinement

- **Date Recorded:** Initial
- **Layer:** Doctrine; Implementation Spec
- **Source:** `01_doctrine_ontology/09_plg_product_evolution_strategy.md`; `03_implementation_specs/02_plg_60_second_flow_wireframes.md`; `03_implementation_specs/12_freemium_tier_behavior_logic.md`
- **Decision:** Freemium includes both Fast Pass and Deep Refinement. The free experience must demonstrate real intelligence value.
- **Status:** Stated.

### DL-026 — Adopt Repository Layer Precedence

- **Date Recorded:** Initial
- **Layer:** Manifest
- **Source:** `repository_manifest.md` (Repository Structure)
- **Decision:** Repository content is organized into four canonical layers. `00_raw_transcript` is source material rather than canonical doctrine. `01_doctrine_ontology` is the primary conceptual foundation. `02_ux_constitution` takes precedence over individual implementation decisions. `03_implementation_specs` must remain aligned with doctrine and constitutional principles.
- **Status:** Stated. The relationship between doctrine and Constitution (derivation, peer, or supremacy) is not declared. See `revision_backlog.md`, RB-005.

### DL-027 — Adopt Manifest Governance Principles

- **Date Recorded:** Initial
- **Layer:** Manifest
- **Source:** `repository_manifest.md` (Governance Principles)
- **Decision:** Seven governance principles are adopted for reviewing and evolving repository content: (1) seek understanding before proposing change; (2) preserve canonical terminology whenever possible; (3) distinguish doctrine from implementation; (4) distinguish source material from canonical knowledge; (5) identify conceptual conflicts explicitly; (6) avoid introducing terminology drift; (7) prefer governed evolution over ad hoc modification.
- **Status:** Stated.

### DL-028 — Recognize Immature Subsystems

- **Date Recorded:** Initial
- **Layer:** Manifest
- **Source:** `repository_manifest.md` (Repository Status)
- **Decision:** Project MRI, ontology governance tooling, canonical definition management, revision governance workflows, and decision lineage tracking are formally recognized as immature areas requiring further development.
- **Status:** Stated.

---

## Post-Bootstrap Ratified Decisions

### DL-029 — Adopt Founding Bootstrap Stipulation

- **Date Recorded:** 2026-05-28
- **Layer:** Root Governance (Founding Act)
- **Source:** Repository Owner Action Plan
- **Decision:** Frameworks 001 and 001A are admitted to the repository by founding stipulation. This is the only canonical change made without prior Proposal-Review-Decision. All subsequent canonical changes — including amendments to the frameworks themselves — proceed under the operative governance lifecycle declared by Framework 001 and refined by Framework 001A.
- **Rationale:** The governance framework requires a bootstrap event. A single founding stipulation is simpler and more durable than attempting to recursively govern the framework's own adoption. Standard constitutional bootstrap convention.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** None. This is the founding act.
- **Affected Artifacts:** Framework 001; Framework 001A; all future canonical content; `decision_log.md`; `revision_backlog.md`; `changelog.md`; `repository_manifest.md` (Governance Principles operationalized).
- **Resulting Actions:** Frameworks 001 and 001A become operative; DL-030, DL-031, and DL-032 are ratifiable under this stipulation; subsequent canonical changes follow the operative lifecycle.
- **Status:** Ratified.

---

### DL-030 — Adopt Framework 001

- **Date Recorded:** 2026-05-28
- **Layer:** Root Governance
- **Source:** Repository Owner Action Plan
- **Decision:** Framework 001 is adopted as the canonical governance framework. It declares the five governance object types (Frameworks, Proposals, Decisions, Backlog Entries, Changelog Entries), the canonical lifecycle (Backlog Entry → Proposal → Review → Decision → Repository Change → Changelog Entry), the ratification rule (no canonical change without Proposal + Review + Decision + Traceability Record), the supersession rule (each decision identifies affected artifacts, superseded decisions, superseded definitions, resulting modifications), and the conflict resolution rule (conflicts resolved through proposals rather than direct edits). It restates the repository objective as ontology consistency, governance traceability, and outcome integrity.
- **Rationale:** Framework 001 is operationally sufficient. The repository should not delay governance adoption while perfecting traceability mechanics.
- **Disposition:** Accepted with Conditions
- **Conditions:** Traceability Record schema remains an open governance item. The provisional changelog schema established with this decision is to be revisited by future governance work. The condition is recorded against this decision and will be addressed through subsequent Proposals; no new backlog entry is created at this time, in observance of the governance discipline directive.
- **Supersedes:** None.
- **Affected Artifacts:** `revision_backlog.md` (RB-002 closed); `decision_log.md` (now operates under Framework 001); `changelog.md` (provisional schema instantiated); `repository_manifest.md` (Governance Principles operationalized).
- **Resulting Actions:** Governance lifecycle becomes active; RB-002 closed with disposition; provisional changelog schema instantiated; future canonical changes governed by Framework 001.
- **Status:** Ratified with Conditions.

---

### DL-031 — Adopt Framework 001A

- **Date Recorded:** 2026-05-28
- **Layer:** Root Governance
- **Source:** Repository Owner Action Plan
- **Decision:** Framework 001A is adopted as an amendment to Framework 001. It declares the five review disposition states (Accepted, Accepted with Conditions, Rejected, Deferred, Returned for Revision), the five-element review output schema (Findings, Concerns, Dependencies, Recommendation, Status), and the authority constraint reserving ratification, rejection, supersession, and adoption to the repository owner while scoping AI systems to analysis, consistency checking, conflict identification, and recommendation generation.
- **Rationale:** Framework 001A establishes review states, review outputs, owner authority, and AI authority limitations. These are foundational governance controls.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** None. 001A extends 001 by addition.
- **Affected Artifacts:** Framework 001 (extended); all future Reviews; AI contribution scope.
- **Resulting Actions:** Review lifecycle becomes active; AI authority boundaries become explicit.
- **Status:** Ratified.

---

### DL-032 — Transitional Rule for Pre-Framework Stated Decisions

- **Date Recorded:** 2026-05-28
- **Layer:** Root Governance
- **Source:** Repository Owner Action Plan
- **Decision:** DL-001 through DL-028 are grandfathered as Stated. They remain in effect, may be cited, and are subject to ratification or supersession only through future Proposals processed under Framework 001/001A. Any future Proposal that touches a grandfathered entry must reach Decision through the operative lifecycle and must explicitly note the conversion from Stated to Ratified in its supersession record.
- **Rationale:** Retroactively ratifying all historical decisions would create governance overhead without proportional value. Grandfathering preserves repository history while allowing future ratification through the new governance process.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** None. The Stated entries are preserved as-is; this decision establishes their forward-looking status under the framework regime.
- **Affected Artifacts:** All 28 Stated entries (DL-001 through DL-028); backlog entries that touch grandfathered decisions (RB-001, RB-006 through RB-012, RB-015, RB-019).
- **Resulting Actions:** Decision log header annotated to reflect grandfathered status; backlog entries that touch grandfathered decisions implicitly reference this transitional rule.
- **Status:** Ratified. First decision processed under the operative governance lifecycle.

---

### DL-033 — Adopt Doctrine-Centered Repository Architecture per Proposal 000

- **Date Recorded:** 2026-05-29
- **Layer:** Root Governance
- **Source:** Proposal 000 (Canonical Repository Architecture); Repository Owner Principles (Doctrine as ultimate source of truth; Constitution as distilled operational expression of Doctrine; preservation of original understanding over governance flexibility); Proposal 000 Disposition Document (`07_governance/proposal_000_disposition.md`).
- **Decision:** Adopt the doctrine-centered repository architecture as defined in `07_governance/proposal_000_disposition.md`. The architecture comprises two parallel tiers. The Content tier contains Doctrine, Constitution, Implementation Specifications, and Source Material, ordered by precedence: Doctrine > Constitution > Implementation Specifications; Source Material is non-canonical. The Governance tier contains the Manifest, Governance Frameworks, Proposals, Reviews, Decisions, Revision Backlog, and Changelog; Frameworks carry procedural authority; the Manifest provides orientation with non-doctrinal force. Conflicts are resolved through Proposals under the operative Framework, never by direct edit. Subsystems must anchor to canonical content. Full architectural detail is recorded in the disposition document.
- **Rationale:** This architecture is the only architecture among the Proposal 000 options that satisfies all three repository owner principles. Doctrine retains primary status (Principle 1); Constitution is positioned as a derived operational expression subordinate to Doctrine (Principle 2); the two-tier separation preserves doctrinal autonomy from procedural drift, accepting higher classification and reconciliation cost as the price of fidelity to original understanding (Principle 3). Alternative options each violate one or more of the owner's principles; their rejection is recorded in the disposition document.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** No prior Decision. Resolves Proposal 001 as absorbed. Closes RB-019 and RB-011. Partially closes RB-005 and RB-010. Stated decisions DL-001 through DL-028 are not superseded and continue to operate under the now-ratified architecture per DL-032.
- **Affected Artifacts:** `07_governance/proposal_000_disposition.md` (created); this entry in `07_governance/decision_log.md`; `repository_manifest.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `canonical_definitions.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `ontology_registry.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `01_doctrine_ontology/12_constitutional_principles_draft.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `07_governance/revision_backlog.md` (RB-019 and RB-011 closed; RB-005 and RB-010 partially closed); `07_governance/changelog.md` (CHG-007 through CHG-012 recorded); `REPOSITORY_ARCHITECTURE.md` at repository root (created); Proposal 001 (closed as absorbed; no separate file modified); the full body of canonical content (now operating under the ratified architecture).
- **Resulting Actions:** Disposition document placed at `07_governance/proposal_000_disposition.md`. Proposal 001 closed as absorbed (recorded by reference in this entry and in the changelog). Affected backlog entries updated with closure status referencing DL-033. DL-XXX placeholders replaced with DL-033 in four pre-ratification-annotated files. `REPOSITORY_ARCHITECTURE.md` placed at repository root as the contributor-facing entrypoint. Changelog entries CHG-007 through CHG-012 recorded.
- **Status:** Ratified.

---

## Open Questions Not Recorded as Decisions

The following appear in `03_implementation_specs/14_open_questions_design_risks.md` and remain explicitly open. They are not decisions and are listed here for reference only.

- Confidence scoring methodology
- Minimum viable evidence model
- First governance policies
- Artifact versioning approach
- Distinguishing user-authored from AI-generated changes

---

## Governance Notes

1. The decision log is operative as of DL-029. DL-029 through DL-033 are Ratified under Framework 001/001A.
2. DL-001 through DL-028 are grandfathered as Stated per DL-032. They remain in effect but require future Proposals to convert to Ratified.
3. Future entries must cite the source Proposal, follow the Entry Schema, and adhere to the supersession rule declared by Framework 001.
4. Decisions that reconcile conflicts among grandfathered entries must explicitly reference the superseded statements.
5. The Traceability Record schema is open per the condition on DL-030. The provisional changelog schema is to be revisited by future governance work.

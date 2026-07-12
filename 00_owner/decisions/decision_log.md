# Decision Log

## Status

**Operative — Governance Framework Active**

Repository governance is operative under Framework 001 (per DL-030) and Framework 001A (per DL-031). The founding bootstrap stipulation is recorded as DL-029. The transitional rule for pre-framework Stated decisions is recorded as DL-032.

**Grandfathered Range:** DL-001 through DL-028 are grandfathered as Stated per DL-032. They remain in effect and may be cited. Conversion of any grandfathered entry to Ratified requires a Proposal processed under Framework 001/001A.

**Post-Bootstrap Range:** DL-029 through DL-032 and all subsequent entries are processed under the operative governance lifecycle.

> **❄️ FROZEN — Recording discipline (DL-065).** This monolithic log is **frozen as the historical ledger through DL-064.** **DL-065 and onward are individual record files** under `00_owner/decisions/records/` (one file per decision) — see the generated **Individual Decision Records** index at the end of this file. **Do not append new `### DL-###` entries here.** Draft new decisions as `records/DL-PENDING-slug.md`; the number is assigned at merge (`python3 tools/dl_records.py next`). The doc-integrity gate enforces the records rules (DL-065 R4).

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
- **Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` Article 1
- **Decision:** OSLO exists to preserve trustworthy organizational understanding under dynamic conditions.
- **Rationale:** Stated as the foundational thesis and the highest-order design principle.
- **Status:** Stated.

### DL-002 — Adopt Outcome Integrity as Coherence Between Realities

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` Article 3
- **Decision:** Outcome Integrity is defined as the degree of coherence between Intended Reality and Current Reality under evolving organizational conditions.
- **Status:** Stated.

### DL-003 — Adopt Dynamic Epistemic Synthesis as the Canonical Truth Structure

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 7; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q65
- **Decision:** OSLO's canonical truth object is Dynamic Epistemic Synthesis.
- **Rationale:** Truth cannot be static under evolving conditions.
- **Status:** Stated.

### DL-004 — Adopt Five Epistemic Object Types

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 8
- **Decision:** OSLO distinguishes Facts, Inferences, Assumptions, Recommendations, and Conflicts as canonical epistemic object types.
- **Status:** Stated. Conflict exists with `03_implementation_specs/05_component_system_specification.md`, which extends the list. Reconciliation pending (see `revision_backlog.md`, RB-001).

### DL-005 — Distinguish Ambiguity from Understanding Boundary

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/03_epistemic_system_model.md`; `01_governance/constitution/02_epistemic_constitution.md` Article 9
- **Decision:** Ambiguity (organizational lack of clarity) and Understanding Boundary (system lack of evidence or visibility) are distinct epistemic conditions.
- **Status:** Stated.

### DL-006 — Adopt Anti-False-Certainty Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` Article 5
- **Decision:** OSLO must never imply unjustified certainty, hide ambiguity, obscure assumptions, or conceal interpretation instability. Uncertainty must remain structurally inspectable.
- **Status:** Stated.

### DL-007 — Adopt Human Judgment as Authoritative

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/01_core_philosophical_doctrine.md`; `01_governance/constitution/01_foundational_constitutional_doctrine.md` Article 6
- **Decision:** OSLO augments judgment, does not replace it. Human authority is final. Divergence from OSLO understanding remains visible and governable.
- **Status:** Stated.

### DL-008 — Adopt Understanding as the Center of the System

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` Article 12
- **Decision:** Understanding is the center of the system. Artifacts support understanding; understanding does not support artifacts.
- **Status:** Stated.

### DL-009 — Adopt the Top-Level Navigation Structure

- **Date Recorded:** Initial
- **Layer:** Doctrine; Implementation Spec; Raw Transcript
- **Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `03_implementation_specs/04_core_navigation_information_architecture.md`; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q68
- **Decision:** Top-level navigation is Understanding, Artifacts, Attention, Simulations, Evolution, Governance.
- **Status:** Stated.

### DL-010 — Adopt Outcome Space as the Primary Operating Object

- **Date Recorded:** Initial
- **Layer:** Constitution
- **Source:** `01_governance/constitution/03_workspace_constitution.md` Article 13; `01_governance/constitution/10_canonical_definitions.md`
- **Decision:** The Outcome Space is the primary operating object — a governed workspace representing the evolving synthesis of organizational understanding surrounding intended outcomes.
- **Status:** Stated.

### DL-011 — Adopt Confidence as Trustworthiness of Understanding

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/06_confidence_understanding_model.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` Article 30
- **Decision:** Confidence represents the trustworthiness of organizational understanding, not prediction certainty.
- **Status:** Stated.

### DL-012 — Adopt the Confidence Maturity Progression

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Implementation Spec
- **Source:** `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` Article 32; `03_implementation_specs/08_state_logic_state_machines.md`
- **Decision:** Confidence Maturity progresses: Initial → Expanded → Validated → Continuous.
- **Status:** Stated.

### DL-013 — Persistent Confidence Shell

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` Article 17
- **Decision:** Confidence is persistent epistemic infrastructure, not a report. Confidence and integrity state remain globally visible.
- **Status:** Stated.

### DL-014 — Outcome Integrity States Are Not Workflow Phases

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/04_outcome_integrity_framework.md`; `01_governance/constitution/06_confidence_integrity_constitution.md` Article 33; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q57
- **Decision:** Outcome Integrity States are epistemic and governance states, not workflow phases.
- **Status:** Stated. The exact state set is inconsistent across sources; reconciliation pending (see `revision_backlog.md`, RB-001).

### DL-015 — Conversation Supports Understanding

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/05_workspace_navigation_doctrine.md`; `01_governance/constitution/03_workspace_constitution.md` Article 18; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` (OSLO Chat and Confidence Placement)
- **Decision:** Conversation supports understanding; understanding does not support conversation. OSLO Chat is contextual, not primary navigation.
- **Status:** Stated.

### DL-016 — Adopt Progressive Visibility Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md`; `01_governance/constitution/05_intelligence_visibility_constitution.md` Article 25; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q66
- **Decision:** The more stable understanding becomes, the more OSLO recedes. The more uncertainty or consequence emerges, the more visible OSLO becomes.
- **Status:** Stated.

### DL-017 — Adopt Calm Strategic Augmentation as Emotional Posture

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/11_emotional_interaction_philosophy.md`; `01_governance/constitution/09_emotional_interaction_constitution.md` Article 45; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q60
- **Decision:** OSLO should feel like calm strategic augmentation.
- **Status:** Stated.

### DL-018 — Outcome Integrity Policies Are Human-Readable Doctrine

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 20
- **Decision:** Outcome Integrity Policies exist as human-readable governance doctrine, not workflow automation scripting.
- **Status:** Stated.

### DL-019 — Override Visibility

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 21
- **Decision:** Human overrides remain permissible; divergence from OSLO understanding remains visible and historically preservable.
- **Status:** Stated.

### DL-020 — Governance Escalation Is Proportional

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 22
- **Decision:** Governance escalation scales proportionally to consequence, confidence degradation, governance severity, and organizational doctrine.
- **Status:** Stated.

### DL-021 — Intended Reality Is Governable

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 24; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q64
- **Decision:** Intended Reality is a governable organizational construct, not immutable truth. OSLO may progressively clarify, challenge, and propose alternatives.
- **Status:** Stated.

### DL-022 — Disagreement Posture Is Facilitator

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution; Raw Transcript
- **Source:** `01_governance/doctrine/07_governance_policy_doctrine.md`; `01_governance/constitution/04_governance_constitution.md` Article 23; `00_raw_transcript/04_ontology_strategy_constitutional_principles.md` Q56
- **Decision:** OSLO acts primarily as facilitated understanding refinement. It exposes divergence, compares evidence, clarifies assumptions, and illuminates tradeoffs. It avoids authoritarian posture.
- **Status:** Stated.

### DL-023 — Adopt Trust Evolution Sequence

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md`; `01_governance/constitution/08_product_evolution_constitution.md` Article 41
- **Decision:** Trust evolves: observations → recommendations → operational influence → orchestration authority.
- **Status:** Stated.

### DL-024 — Adopt Execution Maturity Phases

- **Date Recorded:** Initial
- **Layer:** Doctrine; Constitution
- **Source:** `01_governance/doctrine/10_execution_orchestration_maturity.md`; `01_governance/constitution/08_product_evolution_constitution.md` Article 43
- **Decision:** Execution maturity progresses: Phase 0 (ingestion) → Phase 1 (observational intelligence) → Phase 2 (guided optimization) → Phase 3 (assisted coordination) → Phase 4 (orchestration infrastructure).
- **Status:** Stated.

### DL-025 — Freemium Must Include Deep Refinement

- **Date Recorded:** Initial
- **Layer:** Doctrine; Implementation Spec
- **Source:** `01_governance/doctrine/09_plg_product_evolution_strategy.md`; `03_implementation_specs/02_plg_60_second_flow_wireframes.md`; `03_implementation_specs/12_freemium_tier_behavior_logic.md`
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
- **Source:** Proposal 000 (Canonical Repository Architecture); Repository Owner Principles (Doctrine as ultimate source of truth; Constitution as distilled operational expression of Doctrine; preservation of original understanding over governance flexibility); Proposal 000 Disposition Document (`01_governance/decisions/proposal_000_disposition.md`).
- **Decision:** Adopt the doctrine-centered repository architecture as defined in `01_governance/decisions/proposal_000_disposition.md`. The architecture comprises two parallel tiers. The Content tier contains Doctrine, Constitution, Implementation Specifications, and Source Material, ordered by precedence: Doctrine > Constitution > Implementation Specifications; Source Material is non-canonical. The Governance tier contains the Manifest, Governance Frameworks, Proposals, Reviews, Decisions, Revision Backlog, and Changelog; Frameworks carry procedural authority; the Manifest provides orientation with non-doctrinal force. Conflicts are resolved through Proposals under the operative Framework, never by direct edit. Subsystems must anchor to canonical content. Full architectural detail is recorded in the disposition document.
- **Rationale:** This architecture is the only architecture among the Proposal 000 options that satisfies all three repository owner principles. Doctrine retains primary status (Principle 1); Constitution is positioned as a derived operational expression subordinate to Doctrine (Principle 2); the two-tier separation preserves doctrinal autonomy from procedural drift, accepting higher classification and reconciliation cost as the price of fidelity to original understanding (Principle 3). Alternative options each violate one or more of the owner's principles; their rejection is recorded in the disposition document.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** No prior Decision. Resolves Proposal 001 as absorbed. Closes RB-019 and RB-011. Partially closes RB-005 and RB-010. Stated decisions DL-001 through DL-028 are not superseded and continue to operate under the now-ratified architecture per DL-032.
- **Affected Artifacts:** `01_governance/decisions/proposal_000_disposition.md` (created); this entry in `01_governance/decisions/decision_log.md`; `repository_manifest.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `canonical_definitions.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `ontology_registry.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `01_doctrine_ontology/12_constitutional_principles_draft.md` (DL-XXX placeholder replaced with DL-033 in pre-ratification annotation); `01_governance/backlog/revision_backlog.md` (RB-019 and RB-011 closed; RB-005 and RB-010 partially closed); `01_governance/changelog/changelog.md` (CHG-007 through CHG-012 recorded); `REPOSITORY_ARCHITECTURE.md` at repository root (created); Proposal 001 (closed as absorbed; no separate file modified); the full body of canonical content (now operating under the ratified architecture).
- **Resulting Actions:** Disposition document placed at `01_governance/decisions/proposal_000_disposition.md`. Proposal 001 closed as absorbed (recorded by reference in this entry and in the changelog). Affected backlog entries updated with closure status referencing DL-033. DL-XXX placeholders replaced with DL-033 in four pre-ratification-annotated files. `REPOSITORY_ARCHITECTURE.md` placed at repository root as the contributor-facing entrypoint. Changelog entries CHG-007 through CHG-012 recorded.
- **Status:** Ratified.

---

### DL-034 — Adopt Multi-Axis Progression Taxonomy per RB-003

- **Date Recorded:** 2026-05-29
- **Layer:** Doctrine; Constitution; Root Governance
- **Source:** RB-003 (Progression Model Reconciliation); RB-003 Progression Model Comparison Report; Repository Owner Guidance (seven principles cited in the disposition document); RB-003 Disposition Document (`01_governance/decisions/rb_003_disposition.md`).
- **Decision:** Adopt the OSLO Evolution Framework as the canonical progression taxonomy. The framework comprises four distinct but correlated axes: Cognition Scope (Doctrine 02 four-stage arc), Product Identity (Doctrine 09 four-stage arc), Trust Gradient (Doctrine 09 / Article 41 four-step progression), and Execution Depth (Doctrine 10 / Article 43 five-phase progression). Doctrine prevails over Constitution where stage labels or counts conflict, consistent with DL-033. Portfolio Cognition is a provisional long-term capability, not a ratified stage. Doctrine 09's "Governed Organizational Cognition" label prevails over Article 40's "Governance Infrastructure" at Product Identity Stage 3. Draft Principle 17's substantive content is absorbed by Doctrine 02. Full architectural detail is recorded in the disposition document.
- **Rationale:** The four progressions describe distinct facets of OSLO's evolution that are conceptually independent but empirically correlated. Collapsing them loses analytical resolution; treating them as a single arc misrepresents the doctrine. Under DL-033, doctrinal precedence governs label conflicts. Portfolio Cognition is anticipated in Doctrine 10 but absent from Doctrine 02; the four-stage Cognition Scope arc therefore prevails until Portfolio Cognition is separately governed. The owner privileges fidelity to doctrinal source material.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** No prior Decision. Closes RB-003. Partially resolves RB-010 with respect to Draft Principle 17 (substantive content absorbed by Doctrine 02; the file's overall disposition under RB-010 remains Partially Closed pending future Proposal). Partially unblocks RB-015 (Project MRI scoping). Article 40 Stage 3 label and Article 44 five-stage arc are dispositioned as provisional and do not constitute amendments to the Constitution Articles; their reconciliation with doctrine is governed by the Conflict Resolution Model from DL-033 and applied here.
- **Affected Artifacts:** `01_governance/doctrine/02_organizational_cognition_model.md` (confirmed canonical for Cognition Scope); `01_governance/doctrine/09_plg_product_evolution_strategy.md` (confirmed canonical for Product Identity and Trust Gradient); `01_governance/doctrine/10_execution_orchestration_maturity.md` (confirmed canonical for Execution Depth; Long-Term Direction items provisional); `01_doctrine_ontology/12_constitutional_principles_draft.md` (Draft 17 absorbed by Doctrine 02; annotation applied); `01_governance/constitution/08_product_evolution_constitution.md` (Article 40 and Article 44 annotated with provisional-status notes); `canonical_definitions.md` (OSLO Evolution Framework and four axes registered); `ontology_registry.md` (four axes registered; Long-Term Direction items marked Provisional); `01_governance/decisions/rb_003_disposition.md` (created); `01_governance/backlog/revision_backlog.md` (RB-003 closed; RB-010 Draft-17 absorption noted; RB-015 partial unblock noted); `01_governance/changelog/changelog.md` (CHG entries recorded).
- **Resulting Actions:** Disposition document placed at `01_governance/decisions/rb_003_disposition.md`. Annotations applied to Article 40, Article 44, and Doctrine 12 Draft 17. `revision_backlog.md` updated. `canonical_definitions.md` and `ontology_registry.md` updated to register the framework and four axes. Changelog entries authorized by DL-034 recorded.
- **Status:** Ratified.

---

### DL-035 — Convert Constitutional Principles Draft to Historical Artifact per RB-010

- **Date Recorded:** 2026-05-29
- **Layer:** Doctrine; Source Material; Root Governance
- **Source:** RB-010 (Resolve Constitutional Principles Draft vs Constitution Articles); RB-010 Disposition Report; RB-010 Disposition Document (`01_governance/decisions/rb_010_disposition.md`); DL-033 (Doctrine-Centered Architecture); DL-034 (Draft Principle 17 absorption).
- **Decision:** Convert `01_doctrine_ontology/12_constitutional_principles_draft.md` to a historical artifact by relocating it to `00_raw_transcript/05_constitutional_principles_draft.md` and reclassifying it as non-canonical Source Material under the ratified architecture. Of the 20 original Draft principles, Principle 17 is already absorbed by Doctrine 02 per DL-034. The remaining 19 principles are dispositioned by reclassification: 18 of 19 are substantively represented by Constitution Articles 1, 2, 3, 5, 6, 7, 10, 11, 12, 18, 19, 21, 24, 25, 28, 31, 35, and 45, which retain their operational authority; Draft 18 ("Outcome integrity supersedes workflow optimization") is substantively captured by Article 2 (Understanding Before Execution) and Constitutional Drift Warning 2 (Workflow Drift). The Draft file becomes a historical record; it cannot be cited as authority and carries no doctrinal precedence under DL-033.
- **Rationale:** Option C is the only disposition path that satisfies both ratification criteria. Doctrinal integrity is preserved because all 19 remaining principles' substantive content is recoverable from existing canonical content and the historical record is explicitly preserved. Duplicate authority is minimized because reclassification to non-canonical Source Material eliminates the Drafted-Doctrinal surface that previously outranked 18+ ratified Constitution Articles under DL-033 precedence. Option A loses explicit historical preservation. Option B maximizes duplicate authority. Option D leaves the file in a canonical content surface. Option E collapses to Option C in effect while adding procedural overhead.
- **Disposition:** Accepted
- **Conditions:** None.
- **Supersedes:** No prior Decision. Closes RB-010. The pre-ratification annotation on the original file path is superseded by the Historical Artifact header in the relocated file. Draft Principle 17's prior partial disposition per DL-034 (absorption by Doctrine 02) is unchanged; this Decision dispositions the file as a whole by reclassification.
- **Affected Artifacts:** `01_doctrine_ontology/12_constitutional_principles_draft.md` (removed from this location); `00_raw_transcript/05_constitutional_principles_draft.md` (placed with reclassified header); `00_raw_transcript/00_transcript_index.md` (index entry added); `01_governance/decisions/rb_010_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry); `01_governance/backlog/revision_backlog.md` (RB-010 closed); `01_governance/changelog/changelog.md` (CHG entries recorded). Constitution Articles 1–50 are unaffected; their operational authority increases by removal of the Drafted-Doctrinal counterpart surface.
- **Resulting Actions:** Disposition document placed. File relocated with header reclassification. Raw transcript index updated. RB-010 closed in the revision backlog. Changelog entries authorized by this Decision recorded.
- **Status:** Ratified.

---

### DL-036 — Adopt Bounded Registry Foundation per Proposal 002 / RB-001

- **Date Recorded:** 2026-05-29
- **Layer:** Root Governance
- **Source:** RB-001 (Canonical Registry Consolidation); RB-001 Scope Directive (owner guidance); RB-001 Preparation Analysis; RB-001 Scope Control Package; Proposal 002 (RB-001 Bounded Registry Foundation); Framework 001A Review of Proposal 002; RB-001 Disposition Document (`01_governance/decisions/rb_001_disposition.md`).
- **Decision:** Adopt the bounded Registry Foundation defined by Proposal 002 Resolutions R1 through R8, with the eight closing-Decision clarifications recorded in the disposition document. R1 declares the operational rule between root `canonical_definitions.md` (Governance-tier orientation) and Constitution Article 10 (Content-tier definitional surface); Doctrine prevails over Article 10 where they substantively conflict (Clarification #1). R2 adopts a six-flag status taxonomy (Canonical, Provisional, Proposed, Conflicting, Undefined, Duplicate); the legacy "Established" flag migrates automatically to "Canonical" and "Established (split source)" migrates to "Conflicting" except where Clarification #7 applies (Clarification #2). R3 declares status-change rules; R4 is PRD-authorized at the Resolution level with per-entry registrations clerical (Clarification #3). R4 registers nine canonical doctrinal concepts using existing Doctrine sources only. R5 deprecates four predecessor names; the DL-016 anchor is qualified as Stated (grandfathered) per Clarification #4; the Organizational Cognition Arc deprecation extends the existing DL-034 reframing per Clarification #7. R6 disambiguates "Provisional" between Epistemic Label and Governance Status usages; the relationship to Inventory I-A and RB-007 is recorded per Clarification #6. R7 produces Inventories I-A (13 unanchored implementation concept groups) and I-B (4 registry entries lacking authoritative definitions), placed inline in `ontology_registry.md` per Clarification #5. R8 declares canonical citation paths for the four OSLO Evolution Framework axes. A tie-breaking rule for status-flag exclusivity is declared per Clarification #8.
- **Rationale:** Proposal 002 satisfies the bounded scope defined by the RB-001 Scope Directive. All eight Scope Directive items are addressed without absorbing RB-004, without resolving ontology conflicts, without introducing new doctrine, and without amending Constitution Articles or Implementation Specifications. The Framework 001A Review identified ten Concerns; the eight that required closing-Decision clarification are folded into this Decision as narrative qualifications. The Proposal's substance is adopted without revision.
- **Disposition:** Accepted with Conditions.
- **Conditions:** Eight closing-Decision clarifications recorded in the disposition document (Clarifications #1 through #8 in `01_governance/decisions/rb_001_disposition.md`). The clarifications operate as narrative guidance binding future contributors and AI systems; they do not require additional governance work.
- **Supersedes:** No prior Decision. Closes RB-001. The legacy "Established" and "Established (split source)" status flags in `canonical_definitions.md` and `ontology_registry.md` are superseded by the R2 taxonomy via the migration declared in Clarification #2. The existing Organizational Cognition Arc reframing note in `canonical_definitions.md` (per CHG-019) is extended by R5's Duplicate-status deprecation per Clarification #7.
- **Affected Artifacts:** `canonical_definitions.md` (root) — Surface Authority rule, status taxonomy migration, 9 new entries, 4 deprecation entries, Provisional disambiguation, axis citation paths; `ontology_registry.md` (root) — same updates plus inline placement of Inventories I-A and I-B; `01_governance/decisions/decision_log.md` (this entry); `01_governance/changelog/changelog.md` (CHG-026 through CHG-034 recorded); `01_governance/backlog/revision_backlog.md` (RB-001 closed); `01_governance/decisions/rb_001_disposition.md` (created). Constitution Article 10, Doctrine 01–11, Implementation Specifications, Manifest, REPOSITORY_ARCHITECTURE.md, and Frameworks are unaffected.
- **Resulting Actions:** Disposition document placed. `canonical_definitions.md` and `ontology_registry.md` updated per the Effects on Canonical Surfaces section of the disposition. RB-001 closed in the revision backlog. CHG-026 through CHG-034 recorded in the changelog authorized by this Decision.
- **Status:** Ratified with Conditions.

---

### DL-037 — Adopt Repository Domain Restructure per Proposal 003

- **Date Recorded:** 2026-05-29
- **Layer:** Root Governance (structural reorganization affecting all tiers)
- **Source:** Proposal 003 (Repository Domain Restructure); Repository Restructure Scope Directive (owner guidance); Bounded Executor Package (planning substrate, 11 deliverables); Framework 001A Review of Proposal 003 (Accepted with Conditions); Final Ratification Readiness Review; Comprehensive Editorial Pass (Corrections A through I); Final Micro-Correction Pass (R-1, R-2); Proposal 003 Disposition Document (`01_governance/decisions/proposal_003_restructure_disposition.md`, relocating to `01_governance/decisions/` during Phase 1).
- **Decision:** Adopt the repository domain restructure as a single bounded Decision authorizing five sequenced execution phases. Phase 1 (Governance Stabilization) relocates Doctrine, Constitution, governance objects, and root-level governance files into `01_governance/` with nine subdirectories; Framework 001 and 001A materialized from already-ratified content. Phase 2 (Product Organization) relocates Implementation Specs 01, 02, 03, 04, 06, 07, 10, 12 into `02_product/` with five subdirectories; Specs 10 and 12 move whole. Phase 3 (Architecture Extraction) relocates Implementation Specs 05, 08, 09, 11 into `03_architecture/` with four subdirectories; future-architecture-roadmap section in README documents potential domains. Phase 4 (Execution Tracking) relocates Implementation Specs 13, 14 into `05_execution/implementation_tracking/`. Phase 5 (Research, Subsystems, and Root Cleanup) relocates raw transcripts and Historical Artifact into `04_research/`, relocates Project MRI stub into `subsystems/`, relocates `03_implementation_specs/00_index.md` and `README.md` to `04_research/historical_artifacts/` per Clarification #8 (which supersedes the retirement treatment in Proposal 003 Artifact 2 and converts both items into relocations; total 61 relocations, 0 retirements), populates root README.md and CLAUDE.md, revises REPOSITORY_ARCHITECTURE.md, and removes emptied legacy directories. Path-reference updates are mechanical housekeeping. No doctrinal, constitutional, or implementation spec body content is amended. No ontology conflicts are resolved. No doctrinal stubs are introduced. No new backlog entries are created. RB-020 remains Open through DL-037 closure per Clarification #1. Ten closing-Decision clarifications recorded in the disposition document.
- **Rationale:** Proposal 003 satisfies the bounded scope defined by the Repository Restructure Scope Directive. All five phases are coherently sequenced. The Framework 001A Review identified ten Concerns; all are addressable by closing-Decision narrative clarifications rather than Proposal revision. The migration operationalizes the doctrine-centered architecture (DL-033) physically by separating Governance, Product, Architecture, Research, and Execution into distinct domains. Specs 10 and 12 move whole to avoid splits that would constitute substantive content reorganization; splits are deferred to follow-on Proposals if owner directs. Only directories that receive content are created; speculative subdirectories are documented in READMEs as future-roadmap content rather than created as empty folders.
- **Disposition:** Accepted with Conditions.
- **Conditions:** Ten closing-Decision clarifications recorded in the disposition document. Clarifications govern: RB-020 disposition (remains Open); owner verification of Framework drafts (pre-Phase-1 gate); no header notes on Specs 10/12; Historical Artifact reference treatment; Manifest annotation path check; orientation-only constraint enforcement on README/CLAUDE.md/REPOSITORY_ARCHITECTURE.md; DL-036 Surface Authority Rule path verification (including Article 08 Governance Notes path housekeeping); index file retirement disposition (relocated to historical_artifacts/ with no Historical Artifact header); Phases 2–4 sequencing default to sequential; RB-005 residual unchanged. Rollback authority granted to AI to halt and revert a phase upon constraint violation. Rollback authority applies only to migration execution actions performed under DL-037 and does not extend to reversing, nullifying, or invalidating owner-ratified Decisions (DL-029 through DL-036, or DL-037 itself), Frameworks 001 or 001A, the Manifest's substantive content, pre-ratification annotations, the Clarifications #1–#10 of this Decision, or Stated decisions DL-001 through DL-028 preserved under DL-032.
- **Supersedes:** No prior Decision. Closes no backlog item (Proposal 003 is not a backlog item; RB-001 already closed by DL-036). Establishes the post-migration repository structure as the canonical physical organization.
- **Affected Artifacts:** 10 files created or populated explicitly (Framework 001, Framework 001A, five top-level domain READMEs, this disposition document, root README, root CLAUDE.md); inherited or new minimal subdirectory READMEs counted at Phase 5 close (recorded in CHG-041); 61 files relocated total (all 61 items in the File Move Matrix per Proposal 003 Artifact 2; Clarification #8 reclassifies items 52 and 53 from retirement to relocation, leaving the matrix item count unchanged); 0 retirements; 14 files receive path-reference housekeeping updates; 6 legacy directories removed after verification. Doctrine 01–11, Constitution Articles 1–50, Implementation Specs 01–14 body content, raw transcripts, and Historical Artifact body content are unchanged. DL-033, DL-034, DL-035, DL-036 substantive content preserved; only path citations within them update mechanically. Frameworks 001 and 001A introduce no new procedural rules.
- **Resulting Actions:** Disposition document placed at pre-Phase-1 path. Phases 1–5 to be executed sequentially per the Repository Execution Plan with rollback authority. Per-phase changelog entries (CHG-035 through CHG-043) recorded across phases. Post-Migration Validation Checklist executed before DL-037 marked complete. RB-020 reviewed post-migration; closure deferred to owner direction.
- **Status:** Ratified with Conditions.

---

### DL-038 — Ratify Context Plane Classification as Cross-Cutting Architectural Plane per GOV-CP-000

- **Date Recorded:** 2026-05-30
- **Layer:** Root Governance (architectural classification)
- **Source:** GOV-CP-000 (Context Plane Classification Ratification), presented by repository owner; Context Plane Status Reconciliation Analysis; Context Plane vs Ingestion & Transformation Reconciliation; OSLO Architecture Reconciliation Disposition; Framework 001A Review of GOV-CP-000 (Findings F1–F5, Concerns C1–C7, Dependencies D1–D6, Recommendation: Returned for Owner Decision with Procedural Conditions); GOV-CP-000 Disposition Document (`01_governance/decisions/gov_cp_000_disposition.md`); Context Plane — System Design Change Description (v1.0); OSLO Raw Record Identity & Idempotency Contract v1.0; OSLO Time Semantics & Ordering Contract v1.0.
- **Decision:** Recognize the Context Plane as a cross-cutting architectural plane responsible for managing external context before canonical entry into the Knowledge Layer. The Context Plane is not a canonical epistemic layer in the OSLO layer stack. It is a pre-canonical architectural plane that governs ingestion, normalization, staging, source attribution, identity, temporal ordering, and promotion readiness for external inputs. This Decision establishes Context Plane classification only. It does not define its relationship to Ingestion & Transformation, does not create a Context Plane Specification, and does not modify existing contracts. The classification corresponds to Option B (Cross-cutting architectural plane) of the five candidate classifications evaluated during governance review (A: canonical peer layer; B: cross-cutting architectural plane; C: platform component; D: integration boundary; E: architectural concern without formal construct status).
- **Rationale:** Corpus reconciliation determined that Context Plane classification was unresolved across the OSLO engineering corpus, with evidence distributed across five candidate classifications. The Context Plane Design Description's own explicit self-classification — "cross-cutting system plane / not a new epistemic layer" — provides the strongest single corpus signal in favor of Option B. Layer Authority assignments in OSLO Raw Record Identity & Idempotency Contract v1.0 and OSLO Time Semantics & Ordering Contract v1.0 reinforce the formal-construct interpretation. Operational treatment in OSLO Pre-UI Testing Approach and OSLO Test Case Scenario Suite is consistent with plane-level rather than component-level status. Architectural-overview documents' silence on Context Plane is consistent with the Proposed-status framing and does not contradict positive classification. Option A is contradicted by the Design Description's explicit non-layer self-classification. Option C is inconsistent with the layer-level authority terminology in the two integrity contracts. Option D understates the functional scope (normalization, staging, promotion). Option E does not account for the formal authority assignments in two canonical contracts. Classification ratification precedes relationship definition (GOV-CP-001) to prevent implicit classification adoption through a relationship decision.
- **Disposition:** Accepted with Conditions.
- **Conditions:** Five clarifying conditions recorded in the disposition document (Conditions 1–5 in `01_governance/decisions/gov_cp_000_disposition.md`): (1) Context Plane is not a canonical peer layer; (2) Context Plane is a formal architectural construct / plane; (3) DL-038 constitutes partial adoption of Context Plane status (no Specification, Contract, layer-stack inclusion, diagram inclusion, or follow-on documents are adopted); (4) GOV-CP-001 (Context Plane Relationship Ratification) pause is lifted but GOV-CP-001 does not automatically re-activate; its disposition becomes a separate future governance action; (5) Follow-on alignment items are deferred — alignment of architectural-overview documents, disposition of the two integrity contracts' Layer Authority attributions, production of the eight follow-on documents listed in the Design Description, modification of Layer Specifications' dependency declarations, and modification of the Ingestion & Transformation Contract are explicitly not bundled into this Decision.
- **Supersedes:** No prior Decision. The Context Plane Design Description v1.0 retains "Proposed architectural extension" status as its self-declared label; DL-038 constitutes partial adoption of one aspect of that proposal (classification only) and does not constitute full adoption of the Design Description as canonical. The two integrity contracts' Layer Authority assignments are not modified.
- **Affected Artifacts:** `01_governance/decisions/gov_cp_000_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry); `01_governance/changelog/changelog.md` (CHG-044 recorded). The Context Plane Design Description, OSLO Raw Record Identity & Idempotency Contract v1.0, OSLO Time Semantics & Ordering Contract v1.0, OSLO Pre-UI Testing Approach, OSLO Test Case Scenario Suite, Ingestion & Transformation Contract v1.0, OSLO Canonical Architecture One-Pager, The OSLO Architecture, OSLO — Layer Interaction Invariants, OSLO Contract Index, and all Layer Specifications (Knowledge, Reasoning, Judgment, Governance, Communication, Execution) are unaffected; no body content edits performed. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Resulting Actions:** Disposition document placed at `01_governance/decisions/gov_cp_000_disposition.md`. CHG-044 recorded in the changelog authorized by this Decision. GOV-CP-001 pause condition satisfied; GOV-CP-001 available for re-issue, re-review, modification, or withdrawal as a separate future governance action. No other repository modifications authorized.
- **Status:** Ratified with Conditions.

---

### DL-039 — Ratify Context Plane Explicit Authority Attribution per GOV-CP-001B

- **Date Recorded:** 2026-05-30
- **Layer:** Root Governance (architectural authority attribution)
- **Source:** GOV-CP-001B (Context Plane Explicit Authority Attribution Ratification — Narrow), presented by repository owner; GOV-CP-001A (Context Plane Containment Reconciliation); OSLO Architecture Reconciliation Disposition; OSLO Repository Stabilization and Governance Consolidation Audit (Phase 5 Candidate 3 readiness 19/20); Framework 001A Review of GOV-CP-001B (Findings F1–F5, Concerns C1–C7, Dependencies D1–D7, Recommendation: Returned for Owner Decision with Conditions Advisory); GOV-CP-001B Disposition Document (`01_governance/decisions/gov_cp_001b_disposition.md`); OSLO Raw Record Identity & Idempotency Contract v1.0; OSLO Time Semantics & Ordering Contract v1.0; DL-038 (Context Plane Classification Ratification).
- **Decision:** Within the current corpus, Context Plane has explicit authority over raw record identity and idempotency, and shared authority with Knowledge Layer over time semantics and ordering for externally sourced signals. This explicit authority attribution does not resolve Context Plane containment for Ingestion & Transformation, Execution Signal Ingestion, Capture → Transform → Commit Boundary, Raw Input Isolation, Knowledge Layer Command & Write Contract, or Evidence Chain Integrity. The Decision is a Type-C (Authority) ratification that consolidates two pre-existing canonical authority attributions at the Decision Log level without introducing new authority. The owner-selected path was MODIFY (refining Review Concern C1 wording from "makes this structural asymmetry canonical" to "makes this structural asymmetry explicit in the governance record") followed by APPROVE.
- **Rationale:** The two integrity contracts already explicitly attribute Layer Authority to Context Plane (Raw Record Identity & Idempotency Contract v1.0 line 7: "Layer Authority: Context Plane"; Time Semantics & Ordering Contract v1.0 line 5: "Layer Authority: Context Plane + Knowledge Layer"). DL-038 ratified Context Plane as a formal cross-cutting architectural plane, providing the construct that can hold authority. DL-039 records the consolidated explicit authority attribution while explicitly bounding the scope: six adjacent constructs touching Context Plane concerns remain in their pre-existing authority states and their relationships to Context Plane are not resolved by this Decision. The C1 refinement preserves the substantive observation of structural asymmetry between DL-038's eight Context Plane concerns and the two canonical authority contracts while removing the implication that ratification endorses the asymmetry as a desirable or permanent state. The two conditions (Terminology preservation; Shared authority operational mechanics deferred) reflect explicit deferral of scope-definition and arbitration-mechanism work to avoid bundling.
- **Disposition:** Accepted with Conditions.
- **Conditions:** Two conditions recorded in the disposition document. Condition 1 (Terminology preservation): the ratification preserves "externally sourced signals" terminology as it appears in the OSLO Time Semantics & Ordering Contract v1.0 without redefining its scope; definition of terminology scope relative to "execution signals," "external inputs," and similar parallel terms remains a future governance action. Condition 2 (Shared authority operational mechanics deferred): the ratification establishes shared authority between Context Plane and Knowledge Layer over time semantics for externally sourced signals without defining an arbitration mechanism for divergent interpretations; the arbitration mechanism remains a future governance action.
- **Supersedes:** No prior Decision. Affirms pre-existing Layer Authority attributions in OSLO Raw Record Identity & Idempotency Contract v1.0 and OSLO Time Semantics & Ordering Contract v1.0 as the post-DL-038 canonical Context Plane explicit authority. GOV-CP-001 (Context Plane Relationship Ratification) remains paused per DL-038 Condition 4; DL-039 does not determine its disposition but may serve as one input to future interpretation per Review Concern C7.
- **Affected Artifacts:** `01_governance/decisions/gov_cp_001b_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry); `01_governance/changelog/changelog.md` (CHG-045 recorded). The OSLO Raw Record Identity & Idempotency Contract v1.0, OSLO Time Semantics & Ordering Contract v1.0, OSLO Canonical Architecture One-Pager, The OSLO Architecture, OSLO — Layer Interaction Invariants, OSLO Contract Index, Layer Specifications (Knowledge, Reasoning, Judgment, Governance, Communication, Execution), Ingestion & Transformation Contract v1.0, Execution Signal Ingestion Contract v1.0, Knowledge Layer Command & Write Contract v1.0, Evidence Chain Integrity Contract v1.0, Capture → Transform → Commit Boundary, Raw Input Isolation, Pre-UI Testing Approach, and Test Case Scenario Suite are unaffected; no body content edits performed. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Resulting Actions:** Disposition document placed at `01_governance/decisions/gov_cp_001b_disposition.md`. CHG-045 recorded in the changelog authorized by this Decision. Integration Moratorium directive remains operative with respect to OGAP v1.0 and GOV-FWK-001A-DECISION-READY adoptions. GOV-CP-001 disposition remains paused; not affected by DL-039.
- **Status:** Ratified with Conditions.

---

### DL-040 — Adopt OSLO Governance Acceleration Protocol (OGAP) v1.0 as a Protocol

- **Date Recorded:** 2026-05-30
- **Layer:** Root Governance (governance instrument category introduction + Protocol adoption)
- **Source:** GOV-OGAP, articulated by repository owner; OSLO Governance Acceleration Protocol (OGAP) v1.0 text (in-session); OSLO Repository Stabilization and Governance Consolidation Audit (Phase 5 Candidate 1 readiness 18/20; Phase 6 Step 2 sequencing recommendation); OGAP Self-Triage performed during preceding turns; GOV-OGAP Disposition Document (`01_governance/decisions/gov_ogap_disposition.md`); OGAP v1.0 Protocol Artifact (`01_governance/protocols/ogap_v1.md`).
- **Decision:** Adopt the OSLO Governance Acceleration Protocol (OGAP) v1.0 as a Protocol (not a Framework) operative under DL-040. The full OGAP v1.0 text is recorded at `01_governance/protocols/ogap_v1.md` and includes nine stages (Governance Triage; Discovery Governance; Evidence Sufficiency Gate; Decision Readiness Assessment; Decision Ready Rule; Proposal Generation with Type A–E Templates; Review; Owner Decision; Disposition Processing) plus the Governance Stop Rule and Expected Outcome. The adoption introduces the Protocol instrument category as a parallel governance instrument class distinct from Frameworks. OGAP routes governance items into Framework 001 and Framework 001A more efficiently; it does not replace or modify their lifecycle stages or Review semantics.
- **Rationale:** OSLO Repository Stabilization Audit Phase 5 scored OGAP at 18/20 with two objective blockers: adoption vehicle selection (B1.1) and Governance Discipline directive interaction (B1.2). Both are resolved by the five clarifications attached to this Decision. The Protocol category is introduced as the adoption vehicle, distinct from Frameworks, leaving the CLAUDE.md prohibition on creating new Frameworks unchanged. The empirical case for OGAP is the iteration overhead observed across the GOV-CP-000 → GOV-CP-001A → GOV-CP-001B sequence; OGAP's stages address each contributing cause. Phase 6 sequencing recommendation placed OGAP at Step 2 (after GOV-CP-001B as DL-039 and before GOV-FWK-001A-DECISION-READY); DL-040 honors this sequencing.
- **Disposition:** Accepted with Clarifications.
- **Conditions:** Five clarifications recorded in the disposition document. Clarification 1: OGAP is a Protocol category, not a new Framework. Clarification 2: OGAP does not modify Framework 001 or Framework 001A. Clarification 3: OGAP operates as a routing and acceleration protocol layered over Framework 001 and Framework 001A. Clarification 4: The CLAUDE.md prohibition on creating new Frameworks remains unchanged. Clarification 5: OGAP is authorized because it is owner-ratified as a Protocol, not because AI created a new governance Framework.
- **Supersedes:** No prior Decision. Introduces the Protocol governance instrument category. Does not modify Framework 001 (DL-030), Framework 001A (DL-031), or the CLAUDE.md Governance Discipline directive. GOV-FWK-001A-DECISION-READY's dependency on OGAP being canonical is satisfied by DL-040; that amendment remains a separate pending decision.
- **Affected Artifacts:** `01_governance/protocols/ogap_v1.md` (created — new directory created); `01_governance/decisions/gov_ogap_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry; Governance Notes operative range updated from DL-029–DL-039 to DL-029–DL-040); `01_governance/changelog/changelog.md` (CHG-046 recorded). Framework 001, Framework 001A, CLAUDE.md, doctrine, constitution, ontology registry, canonical definitions, contracts, layer specifications, and all other repository content are unaffected. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Resulting Actions:** Protocol artifact placed at `01_governance/protocols/ogap_v1.md` (new directory `01_governance/protocols/` created). Disposition document placed at `01_governance/decisions/gov_ogap_disposition.md`. CHG-046 recorded in the changelog authorized by this Decision. Integration Moratorium directive partially satisfied (two of three Decision Ready items now integrated: DL-039 and DL-040); one Decision Ready item remains (GOV-FWK-001A-DECISION-READY). GOV-CP-001 remains paused per DL-038 Condition 4; not affected by DL-040. OGAP discipline becomes operative for all future governance items.
- **Status:** Ratified with Clarifications.

---

### DL-041 — Adopt DECISION-READY as a Framework 001A State per GOV-FWK-001A-DECISION-READY

- **Date Recorded:** 2026-05-30
- **Layer:** Root Governance (Framework 001A state-vocabulary supplement)
- **Source:** GOV-FWK-001A-DECISION-READY, articulated by repository owner; DECISION-READY state text (in-session); OSLO Repository Stabilization and Governance Consolidation Audit (Phase 5 Candidate 2 readiness 18/20; Phase 6 Step 3 sequencing recommendation); DECISION-READY Self-Triage performed during preceding turns; GOV-FWK-001A-DECISION-READY Disposition Document (`01_governance/decisions/gov_fwk_001a_decision_ready_disposition.md`); Framework 001A DECISION-READY State Supplement (`01_governance/frameworks/framework_001A_decision_ready.md`); DL-040 (OGAP v1.0 adoption).
- **Decision:** Adopt DECISION-READY as a Framework 001A state operative under DL-041. The full DECISION-READY state definition is recorded at `01_governance/frameworks/framework_001A_decision_ready.md`. DECISION-READY is entered when ambiguity is confirmed, the Evidence Sufficiency Gate (OGAP v1.0 Stage 3) passes, the Decision Readiness Score (OGAP v1.0 Stage 4) reaches 16 or greater, candidate options are known, and no material unresolved evidence gaps remain. Upon entering DECISION-READY, proposal generation is permitted, Review is constrained to evidence quality / scope correctness / contradictions / dependencies / risks, and additional reconciliation is prohibited unless new evidence appears, a contradiction is discovered, or owner requests additional discovery. DECISION-READY does not replace any existing Framework 001A Review state (Accepted, Accepted with Conditions, Rejected, Deferred, Returned for Revision); it is a pre-decision governance state preceding the Review states in the governance lifecycle.
- **Rationale:** OSLO Repository Stabilization Audit Phase 5 scored DECISION-READY at 18/20 with two objective blockers: dependency on OGAP v1.0 mechanics (B2.1) and unspecified repository recording vehicle (B2.2). Both are resolved by DL-041 sequencing (after DL-040 OGAP adoption) and the Framework 001A supplement artifact (B2.2 satisfied). The supplement adds a state to Framework 001A's vocabulary without modifying Framework 001A's existing Review schema or Review states. The empirical case is the iteration overhead documented across the recent governance sequence; DECISION-READY codifies the threshold at which Discovery transitions to Decision Governance, complementing OGAP's procedural discipline with an explicit Framework 001A state.
- **Disposition:** Accepted with Clarifications.
- **Conditions:** Five clarifications recorded in the disposition document. Clarification 1: DECISION-READY is a Framework 001A state. Clarification 2: DECISION-READY is entered when ambiguity is confirmed, Evidence Sufficiency Gate passes, Decision Readiness Score ≥ 16, candidate options are known, and no material unresolved evidence gaps remain. Clarification 3: Upon entering DECISION-READY, proposal generation is permitted, Review is constrained to the five permitted focus areas, and additional reconciliation is prohibited unless a Stop Rule trigger is satisfied (new evidence, contradiction discovered, or owner direction). Clarification 4: DECISION-READY does not replace any existing Framework 001A state; it is a pre-decision governance state. Clarification 5: Framework 001 and Framework 001A otherwise remain unchanged.
- **Supersedes:** No prior Decision. Supplements Framework 001A (DL-031) without modifying its text. Does not modify Framework 001 (DL-030), OGAP v1.0 (DL-040), or the CLAUDE.md Governance Discipline directive. References OGAP Stages 3, 4, and 5 by attribution.
- **Affected Artifacts:** `01_governance/frameworks/framework_001A_decision_ready.md` (created — Framework 001A supplement); `01_governance/decisions/gov_fwk_001a_decision_ready_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry; Governance Notes operative range updated from DL-029–DL-040 to DL-029–DL-041); `01_governance/changelog/changelog.md` (CHG-047 recorded). Framework 001A's existing text, Framework 001, OGAP v1.0 protocol artifact, CLAUDE.md, doctrine, constitution, ontology registry, canonical definitions, contracts, layer specifications, and all other repository content are unaffected. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Resulting Actions:** Framework 001A supplement placed at `01_governance/frameworks/framework_001A_decision_ready.md`. Disposition document placed at `01_governance/decisions/gov_fwk_001a_decision_ready_disposition.md`. CHG-047 recorded in the changelog authorized by this Decision. Integration Moratorium lift conditions ("until existing governance artifacts are integrated into the operating repository model") are satisfied with respect to the three Decision Ready items the Moratorium addressed (DL-039, DL-040, DL-041 all integrated); whether the Moratorium lifts automatically or requires explicit owner declaration is owner-determined. GOV-CP-001 remains paused per DL-038 Condition 4; not affected by DL-041. DECISION-READY state becomes operative for all future governance items meeting the entry criteria.
- **Status:** Ratified with Clarifications.

---

### DL-042 — Integration Moratorium Closure / Governance Stabilization Complete

- **Date Recorded:** 2026-05-30
- **Layer:** Root Governance (governance phase closure; operational state declaration)
- **Source:** Direct owner stipulation following completion of OSLO Repository Stabilization and Governance Consolidation Audit Phase 6 sequence (Steps 1, 2, 3 complete via DL-039, DL-040, DL-041 respectively). DL-042 Disposition Document (`01_governance/decisions/gov_moratorium_closure_disposition.md`).
- **Decision:** The governance stabilization effort initiated during GOV-CP-000 is complete. DL-039 established Context Plane explicit authority attribution. DL-040 established OGAP v1.0 as the operative governance protocol. DL-041 established DECISION-READY as a Framework 001A state. The temporary Integration Moratorium is therefore closed. Future governance items shall be processed under Framework 001, Framework 001A, OGAP v1.0, and DECISION-READY. No additional governance acceleration mechanisms are presently authorized unless separately ratified through the standard governance process.
- **Rationale:** The governance stabilization sequence successfully resolved the iteration overhead problem that motivated OGAP v1.0 and DECISION-READY introduction. The three integration items identified in the Stabilization Audit Phase 5 readiness assessment (GOV-CP-001B at 19/20; OGAP at 18/20; DECISION-READY at 18/20) were each ratified in the Audit's Phase 6 sequence as DL-039, DL-040, DL-041. The Integration Moratorium served its purpose during integration; continuation would be permanent block without stabilization purpose. DL-042 closes the Moratorium explicitly and confirms future acceleration mechanisms require ratification through the standard governance process. Transition from stabilization phase to operational governance state shifts focus from governance-on-governance work to substantive subject-domain governance activities (architecture, doctrine, ontology, contract governance).
- **Disposition:** Accepted.
- **Conditions:** None. DL-042 is an unconditional closure.
- **Supersedes:** Supersedes the temporary Integration Moratorium directive issued by owner stipulation following the GOV-CP-001B Framework 001A Review. The Moratorium is canonically Closed. The stabilization phase is canonically Complete. Does not modify or supersede any prior ratified Decision (DL-001 through DL-041). Does not lift the GOV-CP-001 pause established by DL-038 Condition 4; GOV-CP-001 remains paused as a separate governance item.
- **Affected Artifacts:** `01_governance/decisions/gov_moratorium_closure_disposition.md` (created); `01_governance/decisions/decision_log.md` (this entry; Governance Notes operative range updated from DL-029–DL-041 to DL-029–DL-042); `01_governance/changelog/changelog.md` (CHG-048 recorded). Framework 001, Framework 001A, OGAP v1.0 protocol artifact, DECISION-READY supplement, CLAUDE.md, doctrine, constitution, ontology registry, canonical definitions, contracts, and layer specifications are unaffected. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Resulting Actions:** Integration Moratorium marked Closed. Governance stabilization phase marked Complete. Repository governance state considered Operational. Future governance work returns to architecture, doctrine, ontology, and contract governance activities. Disposition document placed at `01_governance/decisions/gov_moratorium_closure_disposition.md`. CHG-048 recorded in the changelog authorized by this Decision.
- **Status:** Ratified.

---

### DL-043 — Release 1 Architecture & Epistemic Foundation (Consolidated)

- **Date Recorded:** 2026-06-04
- **Layer:** Implementation Spec (Architecture) — cross-checked against Doctrine/Constitution.
- **Source:** Convergent architecture investigation. Disposition document: `01_governance/decisions/RELEASE_1_ARCHITECTURE_FOUNDATION_CONSOLIDATED_RATIFICATION_DL043_DISPOSITION.md`. Constituent sources: `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1`, `…RECONCILIATION_DECISION_001`/`…RECOMMENDATION_001`, `…INTERPRETATION_ACCEPTANCE_ANALYSIS_001`, `CANONICALIZATION_CONTROL_CHALLENGE_REVIEW_001`, `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`, `DERIVED_COGNITION_LIFECYCLE_DECISION_001`, `USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001`, `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1`, `QA_GOVERNANCE_SPECIFICATION_V1`, `OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1`, `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001`, `GOV_ARCH_001_CANONICAL_ARCHITECTURE_GOVERNANCE_REVIEW`.
- **Decision:** Ten constituent decisions ratified as a single act: **(A)** adopt the **Cognitive Responsibility Architecture** as canonical representation (layers retained as secondary dependency-ordering view; layer-engineering artifacts re-homed under owning responsibilities); **(B)** **"Integrity, not Authority"** — defer Authority-as-governance from R1, reclassify R1 promotion as integrity (Perceive/Retain) and R1 exposure as epistemic-safety disclosure (Disclose); Authority plane specified but inactive in R1; **(C)** adopt the **Epistemic Boundary Invariant** and reject elevating "Canonicalization Control" to a responsibility; **(D)** adopt the **Epistemic State Model** (Canonical = Attested; Derived non-canonical; Accepted deferred; labels **Attested | Derived**); **(E)** adopt the **Derived Cognition Lifecycle** (live cognition recomputable/non-canonical; Attested self-attested Cognition History Records; two-axis replay; snapshot-based drift; recompute appends, never overwrites); **(F)** ratify the **Autonomous Implementation Control System**; **(G)** **User Acceptance Recording & Reconciliation** (user-attested sub-class of Attested Assertion; version-pinned **User Acceptance Record** object; **Acceptance-Impact Assessment** Derived type; additive, non-governance); **(H)** ratify **QA Governance** (mandatory positive+negative validation; failure classification; tiered determinism); **(I)** ratify **Observability Governance** (two-axis replay; Outcome-Drift-as-feature vs trust-failure drift); **(J)** ratify the **Application/Platform Capability Classification** (Categories A–F; no governance contracts for C/E/F; no P1–P5 platform track; access control distinct from Authority exposure).
- **Rationale:** The architecture investigation converged; the apparent layer-vs-responsibility conflict was a settled representation question plus one genuine scope question resolved by first principles (R1 "Authority" decomposes into integrity + disclosure-safety; epistemic acceptance is the user's). The epistemic model and cognition lifecycle preserve uncertainty and understanding-change history without canonicalizing any interpretation. User acceptance recording slots in additively as attestation + Derived Cognition, validating the cost-of-being-wrong asymmetry. Ratifying as a package closes ESC-0 and gives every downstream contract and the Runtime Environment Constraint Profile a single canonical target.
- **Disposition:** Accepted with Conditions.
- **Conditions:** (1) Refined foundational assumption confirmed — OSLO performs no interpretation acceptance; user acceptance is recorded as attested project history. (2) Implementation-tier; does not supersede Doctrine/Constitution. (3) Downstream artifact revisions authorized as Resulting Actions. (4) Numeric calibration values (determinism/drift/band tolerances) are an owner-supplied input required before the affected outputs are implemented, not a blocker to ratification. (5) Preserved invariants of constituent (G): user acceptance does not make content true, canonical-as-truth, or activate Authority; a User Acceptance Record is not a Governance Decision; acceptance is append-only history; comparison against prior acceptance is Derived Cognition; OSLO-level acceptance/approval/override/execution remains deferred Outcome Governance.
- **Supersedes:** The layer-as-primary representation of `OSLO_ARCHITECTURE_BASELINE_V1.md` (demoted to secondary view, not deleted); the "Grounded/Candidate" labeling proposal (→ Attested/Derived); the in-flight contract assumption of Authority-in-R1 (Pkg 003-as-governance and Wave D as R1 scope). Does not supersede any Doctrine/Constitution decision; reconciles, does not modify, the open conflict noted at DL-004 (overlay only). GOV-ARCH-001 ratified under constituent (A).
- **Affected Artifacts:** Adopt as canonical: Cognitive Responsibility Architecture Spec, Autonomous Implementation Control System, QA Governance Spec, Observability Governance Spec, Application/Platform Classification Decision 001. Revise: `WAVE_A_CONTRACT_PACKAGE_002` (integrity-gated admission; add Cognition History Record + User Acceptance Record, append-only). Rescope: Contract Inventory, Contract Generation Plan, Capability Coverage Review, Runtime Object Model, Runtime Behavior Model (remove Authority-as-R1; add User Acceptance Record, user-attested sub-class, Acceptance-Impact type). Drop from R1: Wave A Package 003 (Authority-as-governance) and Wave D. Re-home: governed layer-engineering dirs + integrity contracts. Add to roadmap: non-governance User Acceptance & Reconciliation package. Unaffected: Doctrine, Constitution, ontology registry, canonical definitions (except DL-004 overlay note), CLAUDE.md.
- **Resulting Actions:** ESC-0 marked Closed. Constituent specs flipped to canonical/ratified status. Pkg 002 / object / behavior / inventory / plan revisions authorized (execution pending). Runtime Environment Constraint Profile authorized as the next artifact and the single remaining hard gate to coding. CHG-049 recorded. Numeric calibration values remain an open owner input.
- **Status:** Ratified with Conditions.

---

### DL-044 — Release 1 Engineering Handoff Ratification (Consolidated)

- **Date Recorded:** 2026-06-04
- **Layer:** Implementation Spec (engineering enablement) + Governance Specification.
- **Source:** `01_governance/decisions/RELEASE_1_ENGINEERING_HANDOFF_RATIFICATION_DL044_DISPOSITION.md` (full disposition) · `RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` §7. **Builds on:** DL-043.
- **Decision:** Ratifies the Release 1 **engineering-enablement layer** as four constituents, unlocking environment-bound implementation: **(A)** `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1` adopted as the governing coding standard and pre-code gate (responsibility-organized code-tree, no Authority module in R1, canonical/derived store separation with append-only receipts, ratified-stack-only deps behind interfaces, canonical vocabulary, stop/escalate/human-approval gates); **(B)** the **Wave A (001 re-issue · 002 · 00R), B, C, U, E** contract packages approved as CONFORMANT environment-independent sets per `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001` (no Critical/Major; four Minor clarifications MF-A…MF-D non-blocking; Wave D out of R1); **(C)** `RELEASE_1_CALIBRATION_DEFAULTS_V1` adopted as operative, **tunable** default configuration; **(D)** `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1` ratified (protected `main`, Dev→Staging→Production with production deploy human-only, CI gates incl. epistemic-invariant gate, append-only canonical migration discipline, reversible releases, secrets, Claude Code STOP conditions). Also records the **Runtime Environment Constraint Profile** as the canonical environment-binding anchor with R1–R5 reconciliations owner-confirmed.
- **Rationale:** DL-043 made the architecture buildable; this layer makes it safely build-able by Claude Code. The coding standard binds construction to the ratified contracts; the conformance review confirmed the packages are internally consistent and invariant-preserving; calibration defaults remove the last numeric blocker; deployment governance closes the readiness audit's final Critical and keeps production human-gated. Readiness ≈93% (Ready With Controls); per-wave environment-bound implementation may begin.
- **Disposition:** Accepted with Conditions.
- **Conditions:** (1) calibration values are tunable defaults — owner may retune any tolerance/band/threshold without a new Decision; (2) per-wave coding proceeds only after this ratification **and** that wave's package approval (B) **and** the readiness gate (Control System D7); (3) production stays human-gated — Claude Code never self-deploys to Production; (4) build-time residuals (R1–R5 application, physical store/schema binding, audit-retention vs. compliance) applied at environment-bind.
- **Supersedes:** Nothing. Extends DL-043 by adding the engineering-enablement layer. The pre-DL-043 readiness audit's "NOT READY" verdict is historical (already bannered).
- **Affected Artifacts:** Adopt as canonical/operative: Claude Code Implementation Constraints; Deployment Governance; Calibration Defaults; the approved Wave packages. No architecture/Doctrine/Constitution change.
- **Resulting Actions:** Four constituent docs flipped to ratified/approved; MF-A…MF-D recorded as logical-data-model/config clarifications; per-wave environment-bound implementation authorized under the Control System gate; CHG-051 recorded; concrete CI/CD pipeline config to be produced at environment-bind under Deployment Governance.
- **Status:** Ratified with Conditions.

---

### DL-045 — Tool-Neutral Autonomous-Agent Terminology

- **Date Recorded:** 2026-06-05 (ratified; previously a pending draft)
- **Layer:** Root Governance (terminology generalization).
- **Source:** `PROPOSAL_TOOL_NEUTRAL_AGENT_TERMINOLOGY_DL045_DRAFT.md`. **Builds on:** DL-044.
- **Decision:** Generalize tool-specific naming from **"Claude Code"** to **"autonomous coding agent"** (Claude Code / OpenAI Codex / other AGENTS.md-aware agents as interchangeable examples) so the governance reads accurately for any tool. **(A)** `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1` — tool-neutral scope note (filename retained to avoid reference churn). **(B)** `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1` §9 retitled "Autonomous coding agent at the Deployment Boundary (STOP conditions)" + generalized phrasing. **(C)** `AGENTS.md` (repo root + starter-kit) recorded as the **tool-neutral twin** of `CLAUDE.md`.
- **Rationale:** the enforcement surface (contract-traceability, positive+negative tests, epistemic-invariant gate, branch protection, human review) is tool-agnostic by design; the naming should be too. Removes a false impression of vendor lock-in; makes Codex / mixed-tool teams first-class without re-opening any decision.
- **Disposition:** Accepted.
- **Conditions:** **No rule, gate, invariant, STOP condition, readiness gate, or the human-only-production rule changes — identical regardless of tool.** Application's runtime LLM routing (OpenAI primary / Anthropic fallback) is unrelated and untouched.
- **Supersedes:** Nothing. Generalizes DL-044 naming only.
- **Affected Artifacts:** `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1`, `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1` §9; AGENTS.md convention recorded.
- **Resulting Actions:** Scope notes + §9 retitle applied; CHG-075 recorded.
- **Status:** Ratified.

---

### DL-046 — Fast/Deep Analysis Modes + <60s Time-to-First-MRI (Wave B Contract Amendment)

- **Date Recorded:** 2026-06-04
- **Layer:** Implementation Spec (contract amendment) + NFR.
- **Source:** `03_architecture/contracts/WAVE_B_CONTRACT_AMENDMENT_FAST_DEEP_60S_DISPOSITION.md` · backlog `BACKLOG_FAST_DEEP_CONTRACT_FORMALIZATION_DRAFT.md`. **Builds on:** DL-043/DL-044.
- **Decision:** Formalizes the **Fast Pass** and **Deep Pass** analysis modes and the owner-approved **Time-to-First-MRI < 60 s** target as **explicit obligations** in the ratified Wave B contracts (`IC/QA/OBS-WB-INFER`, `IC/QA/OBS-WB-EVAL`), with clarifying notes to `IC-WA-001` (intake feeds Fast Pass; must not block 60 s) and `IC-WA-00R` (00R is the Deep Pass engine; async/coalesced; must not block Fast). Adds: required behavior for both modes; `mode` + `confidence_stage` (Orientation→Expanded→Validated) as **emission attributes** (no new object/responsibility); a **QA performance gate asserting Time-to-First-MRI < 60 s**; mode/stage observability. Adopts the 60 s as a **ratified Release 1 NFR acceptance gate** (Master Spec §20/M1).
- **Rationale:** Fast/Deep are confirmed R1 product scope and the 60 s is the only owner-approved numeric target, but the responsibility-organized contracts had abstracted them away — leaving a Critical capability + its performance target *implicit*. This makes them contracted and testable without changing architecture (modes are timing of the existing Infer/Evaluate + recompute).
- **Disposition:** Accepted.
- **Conditions:** p50/p95 latency distribution and the supported-project-size envelope for the 60 s target remain **`TBD – Owner Decision Required`** (Performance/NFR spec §20).
- **Supersedes:** Nothing. Amends (adds to) the DL-044-approved Wave B contracts; introduces no new responsibility or object.
- **Affected Artifacts:** `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` (amended); `WAVE_A_CONTRACT_PACKAGE_001` / `…_00R` (notes); `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001` (§1 re-checked CONFORMANT); `RELEASE_1_CONTRACT_INVENTORY_V1` (noted). Disposition + backlog drafts retired.
- **Resulting Actions:** Edits applied to the contracts; Wave B conformance re-confirmed; CHG-053 recorded.
- **Status:** Ratified.

---

### DL-047 — Release 1 Contract-Coverage Resolution (Synthesis Engine · Interaction/Collaboration · Enumeration)

- **Date Recorded:** 2026-06-04
- **Layer:** Implementation Spec (architecture-additive) + contract amendments.
- **Source:** `01_governance/decisions/PROPOSAL_CONTRACT_COVERAGE_RESOLUTION_DL047_DISPOSITION.md` · audit `03_architecture/reviews/RELEASE_1_CONTRACT_COVERAGE_AUDIT_002.md`. **Builds on:** DL-043/044/046.
- **Decision:** Closes the cognitive contract-coverage gaps found in Audit 002 (the Fast/Deep class). **(A)** the evidence→plan engine — **Perceive performs source-attributed claim extraction** (evidence-attested, no Derived cognition), and **Infer is extended to synthesize a `SynthesizedPlanningModel` and generate `PlanningArtifact`s as Derived Cognition** (recomputable, CHR-per-generation, user-editable, never Attested-as-truth); Evaluate seeds CAF/Confidence from the synthesized model. **No new responsibility** (Option 1). **(B)** classify: **OSLO Chat** = R1 Disclose-class interaction surface (consumes/triggers cognition, writes no canonical); **CAF Review Requests** = contract the response→evidence→Deep-Pass seam (Perceive), workflow UI is Category-E commodity; **Suggested Fixes** = Advise candidate + **user-applied** edit (no autonomous OSLO write); **Validation Recommendations** = Advise type. **(C)** enumerate False-Confidence Detection, Understanding State Model, Progressive Disclosure, MRI sub-components, assisted editing into Wave B/E. **(D)** adopt a **capability-to-contract traceability gate** (Framework §E+) to prevent recurrence.
- **Rationale:** the responsibility-organized contracts captured the cognitive spine but not several named Alpha capabilities; most criticially the generative synthesis engine had no contracted home. Modeling synthesis as Derived (extended Infer) makes it buildable within the ratified epistemic model without inventing a responsibility.
- **Disposition:** Accepted (as a whole).
- **Conditions:** generated Planning Artifacts are Derived (never Attested-as-truth); OSLO performs no autonomous artifact writes (Suggested Fixes are user-applied); CRR workflow UI remains commodity; Chat writes no canonical and changes no assessment.
- **Supersedes:** Nothing. Additive within existing responsibilities; preserves all DL-043 epistemic invariants.
- **Affected Artifacts:** Architecture spec, Object Model, Behavior Model (DL-047 sections added); Wave A-001, Wave B, Wave C, Wave E contracts (DL-047 Additions); Contract Inventory; Contract Generation Framework (§E+ gate); phase plans II/III/IV/VI. Audit 002 + DL-047 proposal retired.
- **Resulting Actions:** Additions applied; conformance to be re-confirmed at contract regeneration; CHG-054 recorded.
- **Status:** Ratified with Conditions.

---

### DL-048 — Cost Governance / Freemium Unit Economics (Tier-1 Token-Cost Enforcement)

- **Date Recorded:** 2026-06-05
- **Layer:** Implementation Spec (contract amendment) + NFR + Calibration config.
- **Source:** `01_governance/decisions/PROPOSAL_COST_GOVERNANCE_FREEMIUM_UNIT_ECONOMICS_DL048_DISPOSITION.md`. **Builds on:** DL-043/044/046/047.
- **Decision:** Makes **tier-1 freemium unit economics (token-cost management) an enforced, tested, observable Release 1 criterion** rather than a soft NFR principle + commodity billing. Separates the **cap value** (tier-keyed, owner-set, env-bound **configuration**; Calibration Defaults §4c; TBD-tracked) from the **enforcement mechanism** (a contracted **cost-governance obligation on the Fast/Deep analysis engine** — Wave B `IC/QA/OBS-WB-INFER/EVAL` + Wave S `IC/QA/OBS-WS-SYNTH`, with chat/fix caps in Wave I `IC-WI-INTERACT`). **(A)** every Fast/Deep run operates within a per-tier token budget read from config; per-run over-budget → **graceful degradation** (Fast truncates scope; Deep coalesces/defers), per-user daily/monthly rollup over-budget → **gate** further AI spend; free tier enforces single-active-project + single-active-deep + coalescing + daily fix/chat caps; **model routing is tier-keyed config** (free → cheap class). No new responsibility or object. **(B)** QA gate: free-tier run ≤ configured budget on envelope fixtures; **negatives** — budget bypass, runaway re-analysis (coalescing must hold), silent overspend, wrong-tier routing. **(C)** new observability event **`AI Spend Recorded`** (tokens + est. cost per run/user/tier/mode/model) + over-budget trust signal. **(D)** owner-selected **Balanced (~$3/mo)** Free/Tier-1 starting defaults adopted into Calibration Defaults §4c. **(E)** paid-tier limits remain an open scope item (parameterize by tier; not resolved here).
- **Rationale:** the free tier is backed by LLM calls, so unit economics is existential; it was stated (NFR §12 principle 5; MON commodity) but not contracted/tested/observed, with budgets `TBD`. Same class of gap as DL-046's 60s target. Enforcement is bounded behavior of the existing Infer/Evaluate/Synthesize engines + recompute/coalescing backbone — no architecture change. Values start conservative because the contracted cost telemetry lets the owner re-tune from measured medians.
- **Disposition:** Accepted.
- **Conditions:** dollar/token cap **values remain owner-tunable configuration** (Calibration Defaults §4c); the **enforcement mechanism, QA gate, and `AI Spend Recorded` event are contracted** (non-optional); over-budget must **degrade/gate and emit**, never overspend silently; **paid-tier limits TBD** (Open-TBD A6/E); starting defaults are estimate-based pending first-weeks telemetry.
- **Supersedes:** Nothing. Amends (adds to) the DL-044-approved Wave B + DL-047 Wave S/I contracts; introduces no new responsibility or object. MON-01…04 remain commodity billing that consume the same tier config.
- **Affected Artifacts:** `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`, `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md`, `WAVE_I_CONTRACT_PACKAGE_INTERACTION_COLLABORATION.md` (DL-048 Additions); `RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4c cost config); `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` (§12 → ratified gate); `OPEN_TBD_REGISTER.md` (A6 → proposed defaults; E paid-tier); `RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` (MON-COST row); `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (re-checked CONFORMANT).
- **Resulting Actions:** Edits applied; conformance re-confirmed; CHG-055 recorded.
- **Status:** Ratified with Conditions.

---

### DL-049 — External-Stakeholder / Reviewer Identity + Reviewer→User Promotion

- **Date Recorded:** 2026-06-05
- **Layer:** Implementation Spec (architecture-additive: object model + identity/auth).
- **Source:** `01_governance/decisions/PROPOSAL_EXTERNAL_STAKEHOLDER_REVIEWER_IDENTITY_DL049_DISPOSITION.md` · `01_governance/backlog/BACKLOG_EXTERNAL_STAKEHOLDER_EXPERIENCE.md` · `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001` (P0). **Builds on:** DL-043/047/048.
- **Decision:** Resolves Capability-Matrix gap #337 (owner elected Option A). Introduces a **single `Principal` identity object** with attribute **`type: reviewer | user`** — **not** two distinct objects. **Reviewer** = lightweight, email-verified principal **scoped to shared items** (CRR finding / MRI), may view + respond, **no Workspace/projects**; **User** = `Principal` + Workspace/Account + projects + tier (default **Free**). **Reviewer→User promotion is an in-place state transition** (flip `type`, provision Workspace, assign Free tier) on the **same `Principal` ID** — not a data migration. A `StakeholderResponse` (DL-047) is authored by a `Principal` and remains **evidence-attested**; the CRR response→evidence→Deep-Pass seam (Wave A/I) is **preserved, not redefined**.
- **Rationale:** the single-principal model makes conversion a clean promotion with **stable provenance** (prior responses never re-attributed — append-only preserved), whereas two distinct objects re-introduce copy/merge + provenance-rewrite risk. Unblocks the virality audit's P0 conversion path within the ratified epistemic model.
- **Disposition:** Accepted.
- **Conditions:** single-`Principal`-with-`type` (not two objects); promotion = state transition, not data copy; **scope to the inviter's project never widened** on promotion (account-type ≠ share-scope); provenance/history **immutable**; default tier **Free**; promotion **audited** (SEC-06); reviewer-driven recompute **DL-048-bounded**; CRR seam preserved. **Separable scope call — RESOLVED (2026-06-05, CHG-064): recipient experience is fast-follow → Release 2** (R1 = owner validation vehicle; generates + measures invitations only). Identity model unchanged.
- **Supersedes:** Nothing. Additive; introduces the `Principal` identity object; preserves all DL-043 epistemic invariants.
- **Affected Artifacts:** `RELEASE_1_RUNTIME_OBJECT_MODEL_V1` (DL-049 Object Additions — `Principal`); `OSLO_CAPABILITY_MATRIX_V2` (gap #337 resolved); `WAVE_I_CONTRACT_PACKAGE_INTERACTION_COLLABORATION` (note: StakeholderResponse author = Principal); backlog + virality audit (status); link-security (#339) routed to the commodity recipient-experience spec.
- **Resulting Actions:** Object Model updated; gap #337 resolved; CHG-060 recorded. Commodity recipient UI/convert-moment/link-security and the R1-vs-fast-follow scope call remain owner-scoped follow-ups.
- **Status:** Ratified with Conditions.

---

### DL-050 — Resolve "Outcome Management" (retire & map to Outcome Orchestration)

- **Date Recorded:** 2026-06-05
- **Layer:** Canon / ontology (terminology).
- **Source:** `PROPOSAL_OUTCOME_MANAGEMENT_RESOLUTION_DL050_DISPOSITION.md`; KIA-4 (`OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001`). **Builds on:** DL-002 (Outcome Integrity).
- **Decision:** **Option B (retire & map).** "Outcome Management" is **not** a canonical OSLO concept — it was undefined and unused, and "management" connotes acting-on/coordinating work, which conflicts with OSLO's **advise-never-act** posture. **Outcome Orchestration is the discipline/category** (per the Product Vision, CHG-072). Surviving "Outcome Management" references are **historical terminology**, to be **mapped into the Outcome Orchestration framework** during reconciliation/cleanup. Recorded in `CANONICAL_GLOSSARY.md` as a banned synonym (→ Outcome Orchestration / Outcome Integrity).
- **Rationale:** removes a dangling, drift-prone undefined term; aligns terminology with the owner-adopted category (Outcome Orchestration) and the epistemic posture.
- **Disposition:** Accepted (Option B).
- **Supersedes:** Nothing (the term was never canonical). Maps historical usages to Outcome Orchestration.
- **Affected Artifacts:** `CANONICAL_GLOSSARY.md` (outcome-family + banned synonym); `REPOSITORY_INDEX.md`; `OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md` (names Outcome Orchestration the category); KIA-4 closed.
- **Resulting Actions:** Glossary + index updated; CHG-073 recorded.
- **Status:** Ratified.

---

### DL-051 — Adopt Ownership-Zone Repository Taxonomy; Supersede DL-037 Structural Taxonomy

- **Date Recorded:** 2026-06-09
- **Layer:** Root Governance (structural reorganization affecting all tiers)
- **Source:** `PROPOSAL_REPOSITORY_ZONE_RESTRUCTURE_DL051_DRAFT.md` (this disposition); `PROPOSAL_PRODUCT_ENGINEERING_OWNERSHIP_MODEL_DRAFT.md` (operating model + amendments); `REPO_RESTRUCTURE_MIGRATION_MAP_DRAFT.md` (current→target file map); `CODEOWNERS.proposed` (authority map); `ZONE_GROUNDING_RULES.md` (classification method, merged). **Builds on:** DL-033 (doctrine-centered architecture); supersedes part of DL-037.
- **Decision:** Adopt the five-zone **ownership** taxonomy (`00_owner / 10_product / 20_handoff / 30_engineering / 90_research`) as the canonical physical organization, replacing the `01–05` domain taxonomy established by DL-037. Execute as a single atomic migration commit per the migration map: pure moves + ~18 path-reference fixes + meta-file updates (`START_HERE.md`, `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md`, `CLAUDE.md`/`AGENTS.md`) + `tools/doc_integrity_check.py` allowlist updates; mixed folders (`02_product/specs/{data_api_nfr, telemetry, models}`, `03_architecture/runtime_models`) **split by ownership**, not relocated intact; **no body-content edits.** Gate the merge on a green doc-integrity run (0 errors). Capture the product↔engineering boundary principle in `CLAUDE.md`/`AGENTS.md`. Swap the interim `.github/CODEOWNERS` for `CODEOWNERS.proposed` after the move lands.
- **Rationale:** The ownership taxonomy operationalizes DL-033 (doctrine-centered architecture) more strongly by filing Doctrine/Constitution under `00_owner`, reinforcing precedence Doctrine > Constitution > Implementation. R1 implementation has not started (engineering-lead confirmed no `01–05` paths encoded), so the move is at its lowest-cost window before code/contracts reference paths. Mechanical cost is bounded (~18 path-style references break; ~1,442 bare-filename references survive). The classification method (`ZONE_GROUNDING_RULES.md`, incl. the four owner amendments + ratify≠author) is already ratified-as-merged.
- **Disposition:** Accepted with Conditions.
- **Conditions:** **C-1** all zones sit under owner ratification ("authoritative" = default author of realization; `00_owner` governs all zones). **C-2** doctrine/constitution/frameworks/canonical-definitions/glossary/ontology/epistemic-invariants → `00_owner` (ratify ≠ author: owner ratifies policy *intent*; engineering authors *realization* and proposes policy). **C-3** owner breaks `20_handoff` **deadlocks** (not routine contract authorship; precedence Doctrine > Constitution > Implementation). **C-4** mixed folders split by ownership at migration time; **no body-content edits in the migration commit**; green doc-integrity gate. **C-5** build-governance (deployment/QA/observability governance, Anti-Assumption Protocol, implementation constraints, AI-First delivery rules, epistemic invariants) is owner-ratified policy that binds engineering and changes only by owner ratification.
- **Supersedes:** The **structural-taxonomy establishment of DL-037 only** (the `01–05` split as canonical physical organization). **Preserves:** all substantive content relocated under DL-037 (Doctrine 01–11, Constitution Articles 1–50, Implementation Spec bodies, contracts, research — unedited); DL-037's historical validity; its non-structural Clarifications #1–#10; DL-033; DL-036; and Decisions DL-001 through DL-050. Supersedes/retires `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` (sub-foldering within `01–05`).
- **Affected Artifacts:** repository-wide file relocations per the migration map; ~18 path-style references updated; `START_HERE.md`, `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md`, `CLAUDE.md`, `AGENTS.md` updated; `tools/doc_integrity_check.py` allowlists/excludes updated; `.github/CODEOWNERS` replaced by `CODEOWNERS.proposed`; `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` retired/superseded. No Doctrine/Constitution/Spec body content edited.
- **Resulting Actions:** Execute the migration as one commit on a branch → PR → green doc-integrity gate → owner merge. Record a changelog entry (next CHG-###) authorized by DL-051. Activate `CODEOWNERS.proposed` as `.github/CODEOWNERS`.
- **Status:** Ratified with Conditions.

---

### DL-052 — DL-051 Pass 2: Split the Whole-Moved Folders by Ownership Tier

- **Date Recorded:** 2026-06-09
- **Layer:** Root Governance (structural; affects content tiers)
- **Source:** `PROPOSAL_PASS2_ZONE_SPLITS_DL052_DRAFT.md` (this disposition). **Builds on / completes:** DL-051 (Pass 1 moved these folders whole).
- **Decision:** Split the five folders DL-051 relocated whole, routing each file to its correct ownership tier (pure relocation; **no body-content edits**), executed as one atomic commit gated on a green doc-integrity run. **`10_product/domain`:** ~20 founder-approved product domain models stay; the two **Doctrine** files (Interpretation, Leadership) + the **Doctrine Discovery** reconstruction → `00_owner/doctrine`; **Doctrine Decision 001** + **Calibration Decision 001** → `00_owner/decisions`; **Refinement Assessment** → `00_owner/backlog`; calibration governance review, model coverage audit, stack index → `00_owner/audits`; CAF scoring models (`CAF_SCORING_MODEL_V1/V2`, `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1`) + the two `*_V2` "L4 realization" models → `30_engineering/scoring`. **Reviews by grade:** three decision-grade governance/ratification reviews (`GOV_ARCH_001…GOVERNANCE_REVIEW`, `OSLO_ADVISORY_COGNITION_RATIFICATION_REVIEW_002`, `RECOMMENDATION_SYSTEM_SPECIFICATION_V1_GOVERNANCE_REVIEW`) → `00_owner/audits`; remaining working audits stay in `30_engineering`. **`data_api_nfr` split:** API/event/state contracts → `20_handoff/interfaces`; data model + reconciliations → `30_engineering/data`; analysis-engine spec → `30_engineering/analysis_engine`; NFR/performance **targets** → `10_product/acceptance`. **`telemetry`:** stays in `30_engineering` (observability realization).
- **Rationale:** Completes DL-051's deferred splits using the Zone Grounding Rules (doctrine/decision/product-meaning/interface/realization/working-trail). Strengthens precedence by moving doctrine and decisions out of the product zone into `00_owner`. Pure renames; basename-resolved references survive; doc-integrity stays green.
- **Disposition:** Accepted.
- **Conditions:** Owner-confirmed the four ⚠ judgment calls (doctrine relocation; CAF scoring → engineering; doctrine analyses → `00_owner`; full-scope execution) via governance review prior to ratification.
- **Supersedes:** Nothing. Completes DL-051's deferred Pass-2 splits; preserves all content (no body edits).
- **Affected Artifacts:** ~30 file relocations across `00_owner/{doctrine,decisions,backlog,audits}`, `30_engineering/{scoring,data,analysis_engine}`, `20_handoff/interfaces`, `10_product/acceptance`; new target dirs created; no Doctrine/Constitution/Spec body content edited; doc-integrity gate green.
- **Resulting Actions:** Execute as one commit on a branch → PR → green doc-integrity gate → owner merge. Record a changelog entry (next CHG-###) authorized by DL-052.
- **Status:** Ratified.

---

### DL-053 — Terminology Disambiguation (process-word collisions & semantic landmines)

- **Date Recorded:** 2026-06-09
- **Layer:** Canon / ontology (terminology)
- **Source:** `PROPOSAL_TERMINOLOGY_DISAMBIGUATION_DL053_DRAFT.md` (this disposition); engineering-lead collision analysis. **Builds on:** the Canonical Glossary (one-name-per-concept) — adds the inverse (one-word-many-senses).
- **Decision:** Address words carrying multiple concepts across frames (product / build / repo-governance). **Additive (no concept redefinition):** add a **Disambiguation Register** to `00_owner/CANONICAL_GLOSSARY.md` qualifying each colliding word (Governance→Authority-Plane/Build/Repository Governance; Gate→Integrity/Build Gate; Review, Decision, Authority, Validation, Acceptance, State, Policy; and semantic landmines Canonical, Drift, Model, Attested/Derived). **Rename-grade (owner-confirmed):** (i) the dedup field `canonical_key` → **`dedup_key`** so "Canonical" only ever means the truth tier; (ii) the product Authority-Plane artifact `GOVERNANCE_MODEL_V1` → **`AUTHORITY_PLANE_MODEL_V1`** so the product-vs-build governance split is structural. **Enforcement:** doc-integrity adds a DL-053 **regression guard** (retired identifiers `canonical_key`/`GOVERNANCE_MODEL_V1` may not reappear in active specs); bare-word qualification remains an authoring norm in the glossary (not regex-enforced — too many legitimate uses to flag without noise). Also fixed a latent `decision_log` path in the checker (post-restructure).
- **Rationale:** The collisions are real and acute — "Governance/Authority" can lead an autonomous builder to build the **INACTIVE-in-R1 Authority Plane** (violating the `No Authority engine in R1` hard rule). The register defuses ~90% additively; the two renames make the highest-risk splits structural; the regression guard keeps the renames from regressing without flooding the WARN list.
- **Disposition:** Accepted.
- **Conditions:** Owner-confirmed the three rename-grade calls (canonical_key→dedup_key; GOVERNANCE_MODEL_V1→AUTHORITY_PLANE_MODEL_V1; add CI enforcement) via governance review prior to ratification.
- **Supersedes:** Nothing. Additive to the glossary; preserves all canonical concepts. Retires the identifiers `canonical_key` and `GOVERNANCE_MODEL_V1` (renamed, history-traceable).
- **Affected Artifacts:** `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register added); `10_product/domain/AUTHORITY_PLANE_MODEL_V1.md` (renamed from `GOVERNANCE_MODEL_V1.md`, title + disambiguation banner); 9 `30_engineering/analysis_engine/*` files (`canonical_key`→`dedup_key`, incl. `analysis_contracts.py`/`analysis_constants.py`); 3 active `10_product/domain/*` inbound refs updated; `tools/doc_integrity_check.py` (regression guard + `decision_log` path fix). No doctrine/constitution/spec concept redefined.
- **Resulting Actions:** Execute as one commit on a branch → PR → green doc-integrity gate → owner merge. Record a changelog entry (next CHG-###) authorized by DL-053.
- **Status:** Ratified.

---

### DL-054 — Revised Phase 1 Foundation Environment Binding (ENV-REV-001)

- **Date Recorded:** 2026-06-10
- **Layer:** Implementation / environment binding (`30_engineering/environment`). Amends the **owner-provided** Runtime Environment Constraint Profile; **platform architecture (DL-043) unchanged** — this binds implementation/environment only.
- **Source:** `90_research/design_artifacts/REVISED_PHASE_1_FOUNDATION_STACK_PROPOSAL.md` (ENV-REV-001, engineering decision candidate); Review `90_research/design_artifacts/ENV_REV_001_REVIEW_001.md`; condition redline `90_research/design_artifacts/ENV_REV_001_CONDITION_REDLINE.md`.
- **Decision:** Ratify the environment-binding revision: consolidate relational + auth + vector + object storage onto **Supabase** (Postgres + Auth/GoTrue + pgvector + Storage, local via the Supabase CLI); **remove MongoDB** (roles → Supabase Storage + Postgres `jsonb`) and **remove Qdrant** (→ pgvector); **keep Neo4j** (graph) and **Redis** (cache/sessions/streams); **LangGraph** orchestration with a **Postgres checkpointer** for durable, resumable Fast/Deep-Pass runs; **Pydantic AI + an OSS adapter** behind the canon-mandated `/services/llm_provider` interface (OpenAI primary / Anthropic fallback, structured outputs, streaming); add **LangSmith** (self-hosted) for run/trace/cost observability; **app code runs natively** (only backing services Dockerized — already permitted by Profile §6); Heroku + Vercel unchanged.
- **Rationale:** Simplifies the local foundation (one Supabase stack replaces Postgres + Mongo + Qdrant + bespoke auth) while preserving every epistemic and deployment invariant. The revision is faithful to the owner-provided profile, folds in the DL-043 reconciliation (CHR + User Acceptance Record as canonical append-only; Governance Decisions out-of-R1), routes through Framework 001, and escalates rather than assumes on the high-risk items (observability coverage, owner-pending retention).
- **Disposition:** Accepted with Conditions.
- **Conditions:** **(1) Observability is additive, not a replacement** — LangSmith **complements** OpenTelemetry → Grafana for runs/traces/cost and does not retire mandated service-health, queue/event-stream monitoring, two-axis derivation replay, governed-output event emission, drift/trust signals, or retention; CI gate-5 stays satisfied at the app level (governed-output events + `CognitionHistoryRecord` recording provider/model/version + LangSmith run linkage). **(2) Audit retention remains owner-pending (OPEN_TBD C1)** — any "≥1-year audit" figure is a proposed default, not a ratified requirement. **(3) The `/services/llm_provider` adapter must preserve Profile §5 controls** — workload-based routing, usage quotas, model-consumption auditability; provider/routing choice approved here per `starter_kit/CLAUDE.md` (human approval required). **(4) Terminology** — ENV-REV-001 refers to the profile as "owner-provided (pending DL-043 reconciliation)," not "ratified."
- **Supersedes:** Nothing wholesale. On enactment, **amends** `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` §2 (Database Ownership Matrix), §5 (LLM strategy), §7 (Observability). Preserves DL-043 architecture. **Does not resolve** the Master Spec §8 ↔ State Model recommendation-action conflict, nor the Template / Guided-Intake intake-scope question — both tracked separately.
- **Affected Artifacts (each enacted via branch → PR → green doc-integrity gate → owner merge):** `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md`; the Database Ownership Matrix; `30_engineering/data/RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` / `RELEASE_1_LOGICAL_DATA_MODEL_V1.md` physical-binding notes (remove Mongo/Qdrant → Supabase Storage / pgvector); the sibling `ORIENT_PHASE` stage matrix (Mongo/Qdrant → revised bindings); starter-kit templates (`docker-compose.dev.yml`, `.env`, `ci.yml` gate-5 wording) — **blocked until the app repo / starter kit exists**.
- **Resulting Actions:** Dev lead applies the condition redline to ENV-REV-001 on `foundation-phase-1`; execute the canon amendments above as separate commits on branches → PR → green doc-integrity gate → owner merge; record a changelog entry (next CHG-###) authorized by DL-054.
- **Status:** Ratified with Conditions.

---

### DL-055 — Recommendation Action/State Reconciliation (Master Spec §8 ↔ State Model)

- **Date Recorded:** 2026-06-10
- **Layer:** Implementation / canonical terminology (product). Reconciles the Master Spec (product source of truth) with the State Model (lifecycle authority); no doctrine/constitution change.
- **Source:** `90_research/design_artifacts/REC_ACTION_RECONCILIATION_RECOMMENDATION_001.md` (conflict identification + recommendation); surfaced by Review 001 (Concern 6) and the workflow-diagram correction.
- **Decision:** Resolve the conflict between Master Spec §8 ("Recommendation actions include **Accept, Reject, Modify, Discuss, Apply, and Share For Review**") and the State Model §11 lifecycle (`Generated → Accepted → Rejected → Deferred → Implemented (+Superseded)`). The **State Model §11 is canonical for recommendation states.** Master Spec §8 is amended so that: **state-changing actions = Accept, Defer, Reject, Apply** (Apply = Implemented); **"Modify" is not a state** — a user edit triggers re-analysis and **supersedes** the prior recommendation; **"Discuss" (OSLO Chat) and "Share For Review" (CAF Review Request) are collaboration affordances**, not recommendation states; and §8 now **points to the State Model §11 as the lifecycle authority**.
- **Rationale:** §8's prose predated the RS-R3 "Deferred" ratification and conflated state transitions with collaboration affordances. The State Model is the named lifecycle authority and the Data Model v1.2 enum already matches it; aligning §8 to it is the precedence-correct, lower-risk direction. No data-model change required.
- **Disposition:** Accepted.
- **Conditions:** None.
- **Supersedes:** Nothing wholesale. Amends Master Spec §8 wording (and two consistency mentions, §15 Flow 5 and §16 Capability 8) to the reconciled action set. The State Model and Data Model v1.2 are unchanged.
- **Affected Artifacts:** `10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` (§8 Recommendations actions + lifecycle pointer; §15 Flow 5; §16 Capability 8 acceptance criterion). State Model / Data Model unchanged (already canonical).
- **Resulting Actions:** Execute the Master Spec edit as one commit on a branch → PR → green doc-integrity gate → owner merge. Record a changelog entry (next CHG-###) authorized by DL-055.
- **Status:** Ratified.

---

### DL-056 — Intake Scope Ruling: Templates In (R1), Guided Intake Deferred (R2)

- **Date Recorded:** 2026-06-10
- **Layer:** Product scope / experience (intake). Resolves a Master-Spec-vs-UI-Spec scope ambiguity; no doctrine/constitution change.
- **Source:** Review 001 (`ENV_REV_001_REVIEW_001.md`, Concern 5) and `REC_ACTION_RECONCILIATION_RECOMMENDATION_001` context; Capability Matrix V2 §22 #3/#4; owner scope ruling (2026-06-10).
- **Decision:** Of the four start methods named in Master Spec §14/§15 (Upload, Describe, Start From Template, Guided Intake): **Upload, Describe, and Start From Template are in scope for Release 1**; **Guided Intake is deferred to Release 2.** **Start From Template** is defined by `RELEASE_1_TEMPLATE_INTAKE_SPECIFICATION_V1` (ratified herein): a **fully worked fictitious sample plan** the user selects, **instantiated as a populated sample project** (one editable Artifact, `source="template"`) on the standard Fast Pass path — reaching a Project MRI in ~60s on a realistic example, then editable into the user's own project; an **owner-curated catalog of five** (Office Relocation, "Pulse" launch, "Brew & Co" campaign, "DevNorth 2026" event, EU expansion OKR); **owner-curated only** (no user-created templates in R1); `project_type` **pre-filled, non-gating**; project **flagged as a sample**; **no system-generated content** — instantiation is copying static pre-authored content (Onboarding OB-C3 preserved).
- **Rationale:** Templates lower activation cost for the name+one-artifact minimum-to-value without violating the "generates nothing" rule, since a template is static pre-provided content. Guided Intake (a question-flow) is unspecified and heavier; deferring it keeps R1 minimal while Template start covers the curated-start need. Resolves the three-document disagreement (Master Spec listed all four; Onboarding deferred templates; Capability Matrix marked both under-specified).
- **Disposition:** Accepted.
- **Conditions:** None. (R1 catalog body copy may be refined by the owner before GA without a new decision.)
- **Supersedes:** The prior deferral of "Start from templates" in `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1` §L (now in scope). Preserves the deferral of AI-generated starting content.
- **Affected Artifacts:** `10_product/experience/RELEASE_1_TEMPLATE_INTAKE_SPECIFICATION_V1.md` (new); `10_product/experience/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` (§L, owner-approved-defaults note, OB-C3, deferred list, summary); `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md` (§22 #3 resolved / #4 → R2; EI-03 row).
- **Resulting Actions:** Execute as one commit on a branch → PR → green doc-integrity gate → owner merge. Record a changelog entry (next CHG-###) authorized by DL-056.
- **Status:** Ratified.

---

### DL-057 — ADR-0001 Ratification: Application Code in Knowledge-Base Monorepo (Conditional, Time-Boxed)

- **Date:** 2026-06-13 · **Status:** Ratified with Conditions
- **Decision:** ADR-0001 (`code/docs/adr/0001-app-code-in-knowledge-base-monorepo.md`, PR #21) is **ratified with conditions**. The Release 1 application may live under `code/` in this repository as a deliberate, time-boxed deviation from the DL-044 separate-repo default. The separate `oslo` application repo remains the ratified destination; this decision authorizes the deviation, it does not retire the default.
- **Conditions:**
  1. **Zone declaration:** `code/` is declared an **engineering-authoritative, non-canonical** path (DL-051 taxonomy appendix). Nothing under `code/` is canon; content precedence (Doctrine > Constitution > Implementation) is unaffected. `ZONE_GROUNDING_RULES.md` amended accordingly.
  2. **Doc-integrity isolation:** the doc-integrity gate is confirmed (or amended) to exclude `code/`; the app-ci workflow remains path-scoped to `code/**`. Neither gate may weaken the other.
  3. **Review-authority split:** CODEOWNERS activated with `/code/` assigned to engineering review; owner-required review applies to canon zones. Owner gates are preserved where DL-044 places them: per-wave build authorization and production deployment (Gate 8). Branch protection on `main` stays ON.
  4. **Extraction trigger (binding):** `code/` is extracted to the existing `idris-manley/oslo` repository at the **earlier of** (a) the Release 1 exit gate, or (b) a second regular committer or autonomous agent working `code/`. The empty `oslo` repo is retained as the destination. Extraction is pre-authorized by this decision; execution requires no new proposal, only a changelog entry.
  5. **No scope creep:** this decision covers repository placement only. The three policy nods in PR #21 (attribution-missing hard-reject; no-unarchive-in-R1; `failed→stale` transition) remain open owner-queue items and are **not** ratified herein.
- **Rationale:** the deviation was correctly escalated (Anti-Assumption protocol), the reversal path is clean (self-contained `code/` with own pyproject/CLAUDE.md/ADRs), CI separation is verified, and mid-Wave extraction would cost momentum without a present safety gain. Conditions convert an open-ended deviation into a bounded one with a pre-decided exit.
- **Supersedes/Amends:** amends the DL-044 repository-structure assumption for the duration of the deviation; extends DL-051 with the `code/` path declaration. No other DL-044 content (gate sequence, deployment governance, wave authorization) is modified.
- **Source:** PR #21 (`foundation-phase-1` → Wave A); ADR-0001.
- **Affected artifacts:** `ZONE_GROUNDING_RULES.md`, `CODEOWNERS.proposed` → `CODEOWNERS` (with `/code/` rule), `.github/workflows/doc-integrity.yml` (verify/exclude), `code/docs/adr/0001-…` (status → Accepted), changelog (CHG-###).

### DL-058 — Archive Reversibility in R1: UP-3 Affirmed; "No Unarchive in R1" Rejected

- **Date:** 2026-06-15 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Layer:** Implementation Spec. No doctrine/constitution change.
- **Source:** Owner ruling 2026-06-15 (Cowork session); PR #21 owner review; UP-3.
- **Decision:** The PR #21 implementation policy-nod **"no unarchive in R1" is rejected**. Ratified **UP-3 holds**: archive is **reversible in R1** — unarchive is in scope (the Free-tier cap resolution stands). UP-3 itself is unchanged.
- **Rationale:** A documented contradiction between a ratified spec (UP-3, archive reversible) and an implementation nod (no-unarchive). Under content precedence (Doctrine > Constitution > Implementation), the ratified spec governs; the owner adjudicated for UP-3.
- **Supersedes:** the "no unarchive in R1" policy nod escalated in PR #21.
- **Affected artifacts:** `code/` Wave A build (PR #21) — assumes no-unarchive; M6 prompt/cap behavior.
- **Resulting actions:** (1) Unarchive-in-R1 is a confirmed plan-vs-build gap — implement in/with Wave B. (2) M6 hold lifted; prompt/cap behavior builds on reversible archive. DL-057 (ADR-0001) unaffected.
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris; re-landed clean on `decision/governance-catchup` (original PR #25 / branch `decision/dl-058-unarchive-r1` closed and superseded by this catch-up).

### DL-059 — Phase 1 "Prove Understanding": Ratify a Falsifiable Exit Criterion (P-4)

- **Date:** 2026-06-16 · **Status:** Ratified
- **Layer:** Implementation Spec / Delivery governance (Phase 1 sign-off gate). No doctrine/constitution change.
- **Source:** Owner ruling 2026-06-16 (Founder Console Decide lane → OSLO governance handoff); `note_to_eng_phase1_signoff.md`; `MASTER_SPEC_ALIGNMENT_REVIEW.md` (pattern P-4).
- **Decision:** The owner directs that Phase 1 "Prove Understanding" be governed by a **falsifiable, explicit pass/fail exit criterion**, ratified via Framework 001. Engineering's revised Phase 1 sign-off date is **pinned to** that ratified gate — no sign-off against an undefined criterion.
- **Rationale:** Phase 1 sign-off was blocked because its exit criterion was unfalsifiable (P-4): engineering cannot validate against a gate that states no pass/fail line. Defining the gate is the upstream unblocker for the ~7-day slip.
- **Conditions / Resulting actions:** (1) Author the concrete falsifiable Phase 1 pass/fail gate (explicit, measurable) — **owner-authored canon; not inferred** — and land it under Framework 001. (2) Ask Kashif (mkashifse) for a revised sign-off date pinned to that gate. (3) This entry records the owner disposition; the gate text itself is the deliverable it authorizes.
- **Supersedes:** none (resolves the open owner-action item P-4).
- **Affected artifacts:** `00_owner/decisions/decision_log.md` (this entry); `note_to_eng_phase1_signoff.md`; the Phase 1 gate spec to be authored.
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris.

### DL-061 — Project MRI Definition (C-1): Adopt the R1 Per-Project MRI; Rename the Portfolio-Level Concept

- **Date:** 2026-06-16 · **Status:** Ratified
- **Layer:** Canonical terminology / Implementation Spec (flagship-term disambiguation). Relates to the DL-053 Disambiguation Register; no doctrine/constitution change.
- **Source:** Owner ruling 2026-06-16 (Founder Console Decide lane → OSLO governance handoff); `MASTER_SPEC_ALIGNMENT_REVIEW.md` (C-1); `note_to_eng_phase1_signoff.md`.
- **Decision:** Resolve the C-1 flagship-term conflict by adopting the **Master Spec R1 per-project "Project MRI"** (the per-project understanding visualization, R1 core) as the canonical R1 meaning of "Project MRI." The **whole-portfolio integrity-scan** concept (Baseline / Capability Matrix, I14 / Wave 3) is **renamed to a distinct term** to remove the collision — proposed **"Portfolio Integrity Scan"** (final term owner-confirmed at landing). Reconcile via Framework 001; **MRI validation is held until this lands.**
- **Rationale:** The same canonical term named two different things at different scope and timing (per-project, R1 core vs whole-portfolio, I14 / Wave 3) — flagship-term drift that leaves engineers and validators unable to tell which is meant. Adopting the R1 per-project definition unblocks Phase 1 MRI work; renaming the portfolio concept preserves it without the collision.
- **Conditions / Resulting actions:** (1) Propagate the canonical "Project MRI = per-project understanding visualization (R1)" definition and the portfolio-concept rename into the affected specs under Framework 001 — **owner/engineering-authored, not inferred here.** (2) Add a **Disambiguation Register** entry (per DL-053) and a doc-integrity regression guard for the renamed term. (3) Confirm the final portfolio-concept name (proposed: Portfolio Integrity Scan). (4) Hold MRI validation until landed. (5) Record the resulting Change(s).
- **Supersedes:** none — resolves the open C-1 owner-action item; complements the DL-053 disambiguation pattern.
- **Affected artifacts:** `10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` (Project MRI definition — propagation); `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md` (portfolio integrity-scan rename — propagation); glossary Disambiguation Register (new disambiguation entry — propagation); `MASTER_SPEC_ALIGNMENT_REVIEW.md` (C-1 marked resolved); `00_owner/decisions/decision_log.md` (this entry).
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris.

---

### DL-062 — C-2 Confidence-Dimension Reconciliation: CAF First-Class, Reliability Qualifies, Decomposability Preserved

- **Date:** 2026-06-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Layer:** Reconciliation — Doctrine (06) governs intent; Implementation (`30_engineering/scoring/CONFIDENCE_MODEL_V2`, `CAF_SCORING_MODEL_V2`, `RELIABILITY_MODEL_V2`) governs realization.
- **Source:** `MASTER_SPEC_ALIGNMENT_REVIEW.md` (C-2); `note_to_eng_phase1_signoff.md`.
- **Decision:** For Release 1, the **first-class confidence dimensions are CAF — Clarity, Alignment, Feasibility** (three co-equal dimensions). **Reliability** (Coverage / Evidence Availability / Assessability) is the **qualifier**, not a peer dimension. **Outcome Confidence** is the consolidate-then-qualify synthesis of CAF and Reliability (band + reliability qualifier + basis) — never a bare value, never project health, never probability. The Master Spec "CAF are the only first-class confidence dimensions" claim is **affirmed for R1** as an implementation-tier structure consistent with Doctrine 06.
- **Rationale:** Doctrine 06 lists "**Potential dimensions**" (non-exhaustive, no fixed count) and binds only on confidence being **inspectable / explainable / decomposable / historically traceable**. The "nine peer dimensions" appear only in non-canonical `OSLO_ARCHITECTURE_BASELINE_V1.md` §4 (`90_research/`), which cannot create a doctrinal contract. Every Doctrine-06 driver is preserved as a Reliability sub-axis or an inspectable CAF contributor, so CAF-as-first-class narrows structure without losing any driver and does **not** supersede doctrine. Doctrine prevails on intent (decomposability); Implementation authors realization (CAF triad) — ratify ≠ author.
- **Conditions:** (1) **Decomposability preserved (Doctrine 06 prevails):** drivers folded into a CAF dimension (esp. assumption stability, interpretation stability) and the Reliability sub-axes MUST remain individually inspectable in the confidence basis/explanation; an opaque Clarity rollup is non-conformant (QA **negative test required**). (2) No new dimensions/entities/arithmetic; adopts the Active V2 models unchanged (numeric calibration remains Open-TBD F1). (3) Disambiguation-Register entry (DL-053): "first-class confidence dimension" = CAF only. (4) Mark `OSLO_ARCHITECTURE_BASELINE_V1.md` §4 (nine-dimension peer composite) **superseded-for-R1 / non-binding**.
- **Supersedes/Amends:** Supersedes nothing canonical (the nine-dimension claim was never canon). Affirms the Active V2 confidence/CAF/reliability models. Clears C-2 in `MASTER_SPEC_ALIGNMENT_REVIEW.md` and the C-2 blocker in `note_to_eng_phase1_signoff.md`.
- **Affected artifacts:** `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register entry); `90_research/historical_artifacts/OSLO_ARCHITECTURE_BASELINE_V1.md` (§4 superseded-for-R1); affirms (no change) the V2 scoring models. CHG-090.
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris.

---

### DL-063 — Governance v2: Risk-Tiered Routing (Class-A canon; model ratified, Class-D delegation staged, EM seat deferred)

- **Date:** 2026-06-16 · **Status:** Ratified with Conditions · **Decided by:** Idris (Founder Console)
- **Layer:** Class-A canon — amends how Framework 001 routes work. Full lifecycle. Owner-directed (overrides the standing "no new governance frameworks" hold for this change).
- **Source:** `PROPOSAL_GOVERNANCE_V2_RISK_TIERED_ROUTING.md` (v1.1); `REVIEW_GOVERNANCE_V2_RISK_TIERED_ROUTING.md`; `note_to_eng_governance_v2.md`. References DL-030/031, DL-051, DL-053, DL-057.
- **Decision:** Adopt the **5-class change-classification model** (§4): A Canon (owner ratifies) · B Co-governed seam (owner, lightweight) · C Product realization (owner as product lead) · D Engineering realization (EM behind green gates) · E Operational/reversible (pre-authorized). Adopt the **role model** (§3): Owner (Idris) = governance owner + product lead; **EM = Hamza**; Developer = Kashif — separate seats, no self-approval. Ratify the delegation **safety rail**: classifier + automated **path→class guard** + owner sample-audit (§5); **reversibility test** + bounded **lightweight review** (§6); **standing pre-authorizations** (§7); **lazy consensus** with guardrails, **Class A excluded** (§10).
- **Rationale:** Routes work by stakes = zone × reversibility, separating *ratify intent* (owner-only, rare) from *approve realization* (EM + gates, frequent). Builds on existing canon, invents no new structure, preserves the load-bearing core. Cuts the owner's decision surface without weakening enforcement; enforcement becomes a gate, not the owner's eyes.
- **Conditions / staging (per owner resolution 2026-06-16):** (1) **Class-D delegation staged, not live** — flips to "owner: none" only after the per-gate **red-proof** lands (Kashif) and the EM seat activates. (2) **EM-seat activation deferred ~3 weeks** (Hamza unavailable); interim, the **Owner remains the Class-D approver**. (3) **CODEOWNERS:** do not set the absent EM as required reviewer in the interim (would stall engineering PRs); owner stays required reviewer on `code/`/`30_engineering` until activation; re-scope to EM concurrently with the Class-D flip. (4) Activate now (no EM needed): §7 pre-authorizations and §10 lazy-consensus; build §5 path→class guard + red-proof. (5) Classification-table owner = owner (interim). (6) Revisit on Hamza's return.
- **Preserved (unchanged):** canon ratification, precedence ladder, conflict adjudication, DL/changelog audit trail, Anti-Assumption, never-push-to-main, owner-only CODEOWNERS on canon paths.
- **Supersedes/Amends:** Amends Framework 001 routing (adds the 5-class model + safety rail); narrows the uniform-gating default without removing it. Framework 001 doc amendment encoding the §4 table is the Stage-1 realization follow-on.
- **Affected artifacts:** `00_owner/decisions/PROPOSAL_GOVERNANCE_V2_RISK_TIERED_ROUTING.md` + `REVIEW_...md` (copied into repo); CHG-091.
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris.

---

### DL-064 — C-3 Experience↔Architecture Crosswalk: responsibility-primary §0 mapping

- **Date:** 2026-06-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Layer:** Co-governed seam (`20_handoff`) — traceability/interface mapping; non-doctrinal. Realizes already-ratified canon (DL-043); authors no new structure.
- **Source:** `MASTER_SPEC_ALIGNMENT_REVIEW.md` (C-3); `note_to_eng_phase1_signoff.md`. Artifact: `20_handoff/traceability/EXPERIENCE_SURFACE_RESPONSIBILITY_CROSSWALK_V1.md`.
- **Decision:** Ratify the **§0 experience↔architecture crosswalk** mapping every Master Spec experience surface to a canonical responsibility. Per **DL-043 and the glossary (DL-053)** the crosswalk is **responsibility-primary** (Perceive · Retain · Infer · Evaluate · Advise · Disclose · Act/Adapt; Render = non-cognitive); the legacy seven-**layer** names are **deprecated/secondary, orientation only**. C-3 is resolved as a **documentation close-out, not a contradiction.** The artifact is the source for **§0 of Architecture Baseline V2**.
- **Rationale:** C-3 was a missing mapping, not a conflict. The "two vocabularies" were already reconciled by DL-043 (responsibility-primary canonical; layer-names deprecated). Every mapping row traces to ratified canon (glossary + DL-046/047/055/061); no mapping was inferred (Anti-Assumption honored). The owner's "→ architecture layers" framing is realized as "→ responsibilities" to conform to DL-043.
- **Conditions:** (1) Responsibility-primary only; layer names secondary/orientation. (2) Commodity surfaces (monetization/telemetry/collaboration/sharing/notifications/CRUD/auth) are intentionally non-cognition (DL-043 C/E/F) and map to no cognitive responsibility. (3) Incorporate as §0 when `OSLO_ARCHITECTURE_BASELINE_V2` is authored; Baseline V1 remains non-canonical. (4) Does **not** resolve the adjacent *Outcome Integrity States* conflict — tracked separately.
- **Supersedes/Amends:** Supersedes nothing canonical. Closes C-3 in `MASTER_SPEC_ALIGNMENT_REVIEW.md` and the C-3 blocker in `note_to_eng_phase1_signoff.md`.
- **Affected artifacts:** `20_handoff/traceability/EXPERIENCE_SURFACE_RESPONSIBILITY_CROSSWALK_V1.md` (new); CHG-092.
- **Provenance:** Founder Console Decide log, decided 2026-06-16 by Idris.

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

1. The decision log is operative as of DL-029. DL-029 through DL-057 are Ratified under Framework 001/001A. **DL-061 Ratified** (Project MRI definition / C-1: adopt the R1 **per-project** Project MRI as the canonical R1 meaning; **rename the whole-portfolio integrity-scan concept** — proposed *Portfolio Integrity Scan* — to remove the flagship-term collision; Disambiguation Register entry + doc-integrity regression guard per DL-053; MRI validation held until the rename lands). **DL-057 Ratified with Conditions** (ADR-0001 ratification: Release 1 application code under `code/` in this repository as a **time-boxed deviation** from the DL-044 separate-repo default; `code/` declared **engineering-authoritative, non-canonical** (DL-051 appendix; ZONE_GROUNDING_RULES amended); doc-integrity gate confirmed/amended to exclude `code/`; CODEOWNERS activated with `/code/` under engineering review, owner review on canon zones, branch protection retained; **binding extraction trigger** — `code/` extracts to the `oslo` repo at the earlier of R1 exit gate or a second regular committer/agent, pre-authorized; placement only — PR #21's three policy nods remain open owner-queue items). **DL-056 Ratified** (intake scope ruling: Start From Template **in scope for R1** — defined by `RELEASE_1_TEMPLATE_INTAKE_SPECIFICATION_V1`, single planning doc, curated catalog of five, owner-curated, `project_type` pre-fill non-gating, no generated content; **Guided Intake deferred to R2**). **DL-055 Ratified** (recommendation action/state reconciliation: State Model §11 is canonical for recommendation states; Master Spec §8 amended — Accept/Defer/Reject/Apply, "Modify"→supersession, Discuss/Share For Review reclassified as collaboration affordances). **DL-054 Ratified with Conditions** (revised Phase 1 foundation environment binding / ENV-REV-001: Supabase consolidation of relational+auth+vector+object storage, remove MongoDB + Qdrant, LangSmith observability **complement** to OTel→Grafana, native app execution; conditions 1–4; platform architecture DL-043 unchanged). **DL-053 Ratified** (terminology disambiguation: Disambiguation Register added to the glossary; `canonical_key`→`dedup_key`, `GOVERNANCE_MODEL_V1`→`AUTHORITY_PLANE_MODEL_V1`; doc-integrity regression guard; additive, no concept redefinition). **DL-052 Ratified** (DL-051 Pass 2: split the five whole-moved folders by ownership tier — doctrine/decisions out of the product zone into `00_owner`, scoring → `30_engineering`, interfaces → `20_handoff`, NFR targets → `10_product/acceptance`; pure relocation, no body edits). **DL-051 Ratified with Conditions** (ownership-zone repository taxonomy `00_owner/10_product/20_handoff/30_engineering/90_research`; supersedes the `01–05` structural-taxonomy establishment of DL-037 only, preserving all relocated content; conditions C-1…C-5). **DL-045 Ratified** (tool-neutral autonomous-agent terminology; generalizes naming only, changes no rule). **DL-049 Ratified with Conditions** (`Principal` identity, reviewer→user). **DL-050 Ratified** ("Outcome Management" retired & mapped to Outcome Orchestration). DL-036, DL-037, DL-038, and DL-039 are Ratified with Conditions; DL-040 and DL-041 are Ratified with Clarifications; DL-042 is Ratified (unconditional); **DL-043 is Ratified with Conditions** (consolidated Release 1 architecture & epistemic foundation, constituents A–J); **DL-044 is Ratified with Conditions** (Release 1 engineering-enablement layer, constituents A–D: Claude Code Constraints, Wave packages, Calibration Defaults, Deployment Governance); **DL-046 is Ratified** (Fast/Deep analysis modes + <60s Time-to-First-MRI as explicit Wave B contract + NFR obligations); **DL-047 is Ratified with Conditions** (contract-coverage resolution: synthesis engine as Derived/extended-Infer, Chat/CRR/Suggested-Fix classification, sub-feature enumeration, capability→contract traceability gate); **DL-048 is Ratified with Conditions** (cost governance / freemium unit economics: contracted per-tier token-budget enforcement on the Fast/Deep engine + QA gate + `AI Spend Recorded` observability; Balanced ~$3/mo Free-tier config defaults; paid-tier limits TBD). **DL-058 Ratified** (archive reversible in R1; UP-3 affirmed, "no unarchive" nod rejected; unarchive → Wave B). **DL-062 Ratified** (C-2 confidence dimensions: CAF — Clarity/Alignment/Feasibility — are first-class for R1; Reliability qualifies, not a peer; Doctrine-06 drivers preserved as Reliability sub-axes / inspectable CAF contributors; **decomposability is a binding condition**, QA negative test required; the "nine peer dimensions" claim existed only in non-canonical Baseline V1 §4; numeric calibration remains Open-TBD F1). **DL-063 Ratified with Conditions** (Governance v2 — Risk-Tiered Routing, Class-A: 5-class model A–E + role seats [Owner = governance + product lead; EM = Hamza; Developer = Kashif] + delegation safety rail; **Class-D delegation staged behind the per-gate red-proof; EM-seat activation deferred ~3 weeks** — owner remains Class-D approver in the interim; Framework 001 doc amendment is the Stage-1 follow-on). **DL-064 Ratified** (C-3 experience↔architecture crosswalk: responsibility-primary §0 mapping per DL-043; legacy layer names deprecated/secondary; resolved as documentation close-out; artifact `20_handoff/traceability/EXPERIENCE_SURFACE_RESPONSIBILITY_CROSSWALK_V1.md`). Operative governance framework set: Framework 001, Framework 001A, OGAP v1.0, DECISION-READY.

---

<!-- RECORDS-INDEX:START (generated by tools/dl_records.py index — do not hand-edit) -->

## Individual Decision Records (DL-065+)

_One file per decision per DL-065. Generated — do not hand-edit._

- DL-065 — Decision-Recording Discipline (sequencing & conflict elimination) → `00_owner/decisions/records/DL-065-decision-recording-discipline.md`
- DL-066 — Resolve the DL-060 Numbering Gap (retire as reserved-unused; folded into DL-059) → `00_owner/decisions/records/DL-066-resolve-dl-060-gap.md`
- DL-067 — Console-Driven DL Landing (automate the DL-065 flow server-side) → `00_owner/decisions/records/DL-067-console-driven-dl-landing.md`
- DL-068 — Wave A sign-off + Wave B authorization → `00_owner/decisions/records/DL-068-wave-a-signoff-wave-b-authorization.md`
- DL-069 — Internal Gemma (local Llama runtime) as the primary LLM (amends DL-054 §5) → `00_owner/decisions/records/DL-069-internal-gemma-primary-llm.md`
- DL-070 — Ratify the Phase 1 "Prove Understanding" falsifiable exit gate (P-4 / DL-059 realization) → `00_owner/decisions/records/DL-070-phase1-prove-understanding-exit-gate.md`
- DL-071 — DL-053 Disambiguation Register: 'Founder Console' (Intralign Founder Console vs OSLO Observability Console) → `00_owner/decisions/records/DL-071-founder-console-disambiguation.md`
- DL-072 — Wave B exit-gate pass (with conditions) + Phase IV/Wave C authorization → `00_owner/decisions/records/DL-072-wave-b-exit-gate-wave-c-authorization.md`
- DL-073 — Two-mode stage-conditioned onboarding (deferred-signup) + save-to-keep signup trigger → `00_owner/decisions/records/DL-073-two-mode-onboarding-deferred-signup.md`
- DL-074 — Hybrid pricing — tier subscription + per-Deep-Pass overage (single-governor / multi-meter); extends DL-048 → `00_owner/decisions/records/DL-074-hybrid-pricing-multi-meter.md`
- DL-075 — Ratify the Outcome-Lifecycle (Planning/Execution/Validation) orientation crosswalk → `00_owner/decisions/records/DL-075-outcome-lifecycle-orientation-crosswalk.md`
- DL-076 — Ratify the OSLO release model & Alpha release ladder (R1-R5 reconciled with Alpha/Beta/§20) → `00_owner/decisions/records/DL-076-release-model-alpha-ladder.md`
- DL-077 — Ratify the planning-artifact model architecture - Option C hybrid core (fixed understanding core + extensible execution-planning layer) → `00_owner/decisions/records/DL-077-planning-artifact-model-hybrid-core.md`
- DL-078 — Ratify the artifact-profile mechanism & registry realization design (DL-077 Option C realization intent) → `00_owner/decisions/records/DL-078-artifact-profile-realization-design.md`
- DL-079 — Ratify the third-party evaluation-lens cognition boundary (E4): governed input, never silent disposition → `00_owner/decisions/records/DL-079-e4-lens-cognition-boundary.md`
- DL-080 — Ratify the GA deferred-signup realization (provisional identity · pre/post-signup gating · pre-signup retention & privacy) → `00_owner/decisions/records/DL-080-ga-deferred-signup-realization.md`
- DL-081 — Layer-Before-Depth roadmap sequencing (cross-platform planning-governance breadth before execution-governance depth) → `00_owner/decisions/records/DL-081-roadmap-layer-sequencing.md`
- DL-082 — Alpha exit criteria (specify "proven" for Alpha→Beta; amends DL-076) → `00_owner/decisions/records/DL-082-alpha-exit-criteria.md`
- DL-083 — Execution-monitoring tier placement & phase (T3/Pro+, Beta-built; out of Alpha exit) + capability tier split → `00_owner/decisions/records/DL-083-execution-monitoring-tier-and-phase.md`
- DL-084 — R2 candidate-epic phase/tier placement + Foundational-Architecture-in-Alpha principle → `00_owner/decisions/records/DL-084-r2-phase-tier-placement.md`
- DL-085 — User-facing Confidence movement & quantified progress presentation → `00_owner/decisions/records/DL-085-confidence-presentation.md`
- DL-086 — Outcome Confidence index calibration (measurement) — 5-band scheme + v0 defaults → `00_owner/decisions/records/DL-086-confidence-index-calibration.md`
- DL-087 — Strategic chain & onboarding positioning (+ plain-language labels) → `00_owner/decisions/records/DL-087-strategic-chain-positioning.md`
- DL-088 — R1 UX-surface reconciliation (prototype-as-baseline) → `00_owner/decisions/records/DL-088-ux-surface-reconciliation.md`
- DL-089 — Clarification flow contract (object-free; in-panel + chat — Option B) → `00_owner/decisions/records/DL-089-clarification-flow.md`
- DL-090 — Overview cognitive-load trim + Attention-map as its own surface (amends DL-088) → `00_owner/decisions/records/DL-090-overview-trim.md`
- DL-091 — Wave C (Advise) exit-gate pass + Phase V / Wave U authorization → `00_owner/decisions/records/DL-091-wave-c-exit-gate-phase-v-authorization.md`
- DL-092 — Wave C (Advise) exit-gate pass + Phase V / Wave U authorization → `00_owner/decisions/records/DL-092-wave-c-exit-gate-phase-v-authorization.md`
- DL-093 — Finding type + epistemic basis presentation (two-axis; RB-033 Phase R1) → `00_owner/decisions/records/DL-093-finding-type-and-epistemic-basis-r1.md`
- DL-094 — Finding flow simplification: no-Acknowledge lifecycle + single-action resolution (RB-035) → `00_owner/decisions/records/DL-094-finding-flow-simplification.md`
- DL-095 — Findings to Issues user-facing label (RB-036) → `00_owner/decisions/records/DL-095-findings-as-issues-user-facing-label.md`
- DL-096 — Overview surface redesign: confidence-led, low-cognitive-load (RB-037) → `00_owner/decisions/records/DL-096-overview-redesign.md`
- DL-097 — Canonical CAF-dimension maturity band vocabulary (RB-038) → `00_owner/decisions/records/DL-097-caf-dimension-band-vocabulary.md`
- DL-098 — Reconcile CAF-dimension bands to the DL-086 5-band scheme (supersedes DL-097) (RB-039) → `00_owner/decisions/records/DL-098-caf-dimension-band-reconcile.md`
- DL-099 — Reliability qualifier presentation — single quiet-by-default state (loud on CONF-06 divergence) → `00_owner/decisions/records/DL-099-reliability-qualifier-presentation.md`
- DL-100 — Reliability qualifier — finalize copy + confirm CONF-06 trigger reuse (closes RB-040) → `00_owner/decisions/records/DL-100-reliability-qualifier-copy-finalize.md`
- DL-101 — VOID (duplicate of DL-102; landed outside the serializer) → `00_owner/decisions/records/DL-101-controlled-release-and-tiering-in-alpha.md`
- DL-102 — Controlled Release & Tiering-in-Alpha (reconciles CHG-061; amends DL-048 scope, extends DL-049/DL-055/DL-062) → `00_owner/decisions/records/DL-102-controlled-release-and-tiering-in-alpha.md`
- DL-103 — Analysis cost basis & tier re-derivation — never tier judgment quality; commission incremental recompute + prompt caching (supersedes 'Pro adds model quality'; suspends the §4c numeric basis) → `00_owner/decisions/records/DL-103-analysis-cost-basis-and-tier-rederivation.md`
- DL-104 — Errata to DL-103 — strike the priority/latency residue; retire UP-1/UP-2/UP-5; number UP-APPLY and UP-REPORT; refresh DL-102 E; add the P1 health-framing defect class → `00_owner/decisions/records/DL-104-errata-dl-103-priority-lever-and-up-taxonomy.md`
- DL-105 — Commission E1–E3 analysis cost optimization into R1 — prompt caching, scoped recompute (Evaluate always full + equivalence gate), evidence coalescing; instrument, do not gate → `00_owner/decisions/records/DL-105-commission-e1-e3-analysis-cost-optimization.md`
- DL-106 — Commission the DL-069 model-judgment evaluation — and record that DL-103 §1 raised its bar (no 'Gemma for Free, frontier for Pro' hatch); per-call-site qualification; AC-V3 is disqualifying → `00_owner/decisions/records/DL-106-commission-dl069-model-judgment-evaluation.md`
- DL-107 — Obey the doctrine, don't narrate it — and commission the two specs the repo has cited but never possessed: RELEASE_1_TIER_DEFINITIONS_V1 and RELEASE_1_REPORTING_SPECIFICATION_V1 (M4) → `00_owner/decisions/records/DL-107-obey-dont-narrate-commission-tier-definitions-and-reporting.md`

<!-- RECORDS-INDEX:END -->

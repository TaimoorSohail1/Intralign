# Repository Changelog

## Status

**Operative — Provisional Schema**

The changelog records canonical repository changes authorized by ratified Decisions. Each entry references the authorizing Decision and identifies the artifacts modified.

The current changelog schema is **provisional** per the condition on DL-030. The Traceability Record schema remains an open governance item to be addressed by future governance work. Entries recorded under the provisional schema are durable; the schema itself may be amended without invalidating prior entries.

---

## Provisional Entry Schema

Each changelog entry contains:

- **ID** — Change identifier (CHG-NNN).
- **Date** — Date the change was recorded.
- **Authorizing Decision** — The ratified Decision (DL-NNN) that authorizes the change.
- **Affected Artifacts** — Repository files or sections modified.
- **Change Summary** — Brief description of the modification.
- **Supersession Reference** — Any prior change, decision, or definition superseded by this change.

---

## Entries

### CHG-001 — Founding Bootstrap Stipulation Recorded

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-029
- **Affected Artifacts:** `decision_log.md` (DL-029 entry added; header annotated to indicate operative status).
- **Change Summary:** Founding bootstrap stipulation recorded. Frameworks 001 and 001A admitted to the repository by stipulation. The stipulation is the only canonical change made without prior Proposal-Review-Decision; all subsequent canonical changes proceed under the operative lifecycle.
- **Supersession Reference:** None. Founding act.

### CHG-002 — Framework 001 Adopted

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-030
- **Affected Artifacts:** `decision_log.md` (DL-030 entry added); `revision_backlog.md` (RB-002 closed); `changelog.md` (this file instantiated under provisional schema); `repository_manifest.md` (Governance Principles operationalized in effect).
- **Change Summary:** Framework 001 adopted as the canonical governance framework with disposition Accepted with Conditions. The condition (Traceability Record schema remains open) is recorded against DL-030. The provisional changelog schema established by this entry is itself subject to future governance refinement.
- **Supersession Reference:** None.

### CHG-003 — Framework 001A Adopted

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-031
- **Affected Artifacts:** `decision_log.md` (DL-031 entry added); Framework 001 (extended by 001A); future Reviews and AI contributions (now governed by 001A authority and output schemas).
- **Change Summary:** Framework 001A adopted as an amendment to Framework 001. Review disposition states, review output schema, repository owner authority, and AI authority limitations become operative.
- **Supersession Reference:** None. 001A extends 001 by addition.

### CHG-004 — Transitional Rule for Pre-Framework Decisions Adopted

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-032
- **Affected Artifacts:** `decision_log.md` (DL-032 entry added; header annotated to indicate grandfathered range DL-001 through DL-028); `revision_backlog.md` (entries that touch grandfathered decisions implicitly reference DL-032).
- **Change Summary:** Pre-framework Stated decisions (DL-001 through DL-028) grandfathered as Stated. They remain in effect; conversion to Ratified requires future Proposals processed under the operative lifecycle.
- **Supersession Reference:** None. Grandfathered entries are preserved as-is; this change establishes their forward-looking status.

### CHG-005 — RB-002 Closed

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-030 (closure authority); DL-031 (refinement).
- **Affected Artifacts:** `revision_backlog.md` (RB-002 status changed from Proposed to Closed; disposition and closing decisions recorded).
- **Change Summary:** RB-002 (Governance Traceability Spine) closed as resolved through the adoption of Framework 001 with the condition that the Traceability Record schema remains an open governance item.
- **Supersession Reference:** Closure satisfies the substantive scope of RB-002; the residual schema condition is tracked on DL-030.

### CHG-006 — Governance Framework Declared Operative

- **Date:** 2026-05-28
- **Authorizing Decision:** DL-029 (bootstrap); DL-030 (substance); DL-031 (refinement).
- **Affected Artifacts:** `decision_log.md` and `revision_backlog.md` headers updated to reflect operative-under-framework status; `changelog.md` instantiated.
- **Change Summary:** The repository governance framework is declared operative. All subsequent canonical changes proceed under Framework 001/001A.
- **Supersession Reference:** None.

### CHG-007 — Pre-Ratification Annotations Applied

- **Date:** 2026-05-29
- **Authorizing Decision:** Repository Owner Action (Pre-Ratification Minimum Remediation directive). Subsequently bound to DL-033 by reference at ratification.
- **Affected Artifacts:** `01_doctrine_ontology/12_constitutional_principles_draft.md` (Governance Status header added); `repository_manifest.md` (Governance Status header added); `canonical_definitions.md` (Status section updated with Governance-tier acknowledgment and dual-surface note); `ontology_registry.md` (Status section updated with Governance-tier acknowledgment).
- **Change Summary:** Minimum pre-ratification header annotations applied to four files to make Proposal 000 ratification-safe without expanding scope. Doctrine 12 acknowledged as Drafted doctrinal content with nominal precedence over Constitution Articles pending RB-010 full disposition. Manifest acknowledged as Governance-tier orientation with advisory force on substantive claims. Root canonical_definitions.md and ontology_registry.md acknowledged as Governance-tier orientation surfaces.
- **Supersession Reference:** None. Annotations added without modifying body content.

### CHG-008 — Proposal 000 Ratified

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-033 entry appended; header note updated to reflect operative range DL-029 through DL-033).
- **Change Summary:** Proposal 000 ratified. The doctrine-centered repository architecture is the canonical architecture of the OSLO knowledge base. Content tier and Governance tier are functionally distinct. Precedence within Content tier: Doctrine > Constitution > Implementation Specifications. Source Material is non-canonical. Manifest sits in Governance tier as orientation with non-doctrinal force. Subsystems must anchor to canonical content.
- **Supersession Reference:** None. Establishes architecture; does not supersede prior Decisions. Grandfathered Stated decisions DL-001 through DL-028 continue under DL-032.

### CHG-009 — Proposal 000 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `01_governance/decisions/proposal_000_disposition.md` (created).
- **Change Summary:** The full Proposal 000 Disposition Document placed in `07_governance/` as the canonical record of the ratified architecture. Document includes the architecture, role definitions for each repository object class, rejected options and reasoning, accepted tradeoffs, backlog impacts, and resulting repository actions.
- **Supersession Reference:** None.

### CHG-010 — Backlog Updates Recording Proposal 000 Outcomes

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `01_governance/backlog/revision_backlog.md` (RB-019 and RB-011 closed; RB-005 and RB-010 partially closed; each entry annotated with Disposition, Closed/Partially Closed By, Date, and Status fields).
- **Change Summary:** Backlog updated to reflect Proposal 000 outcomes. RB-019 (Manifest precedence) closed by placing Manifest in Governance tier. RB-011 (Lifecycle terminology) closed by Manifest's non-doctrinal status. RB-005 (Layer promotion and citation) partially closed; precedence and promotion model resolved, citation requirements residual. RB-010 (Constitutional Principles Draft vs Articles) partially closed; precedence resolved, full Draft disposition residual.
- **Supersession Reference:** RB-019 and RB-011 superseded as open items by their closure. RB-005 and RB-010 scope reduced.

### CHG-011 — Proposal 001 Closed as Absorbed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** No separate file modified; closure recorded by reference in DL-033 and this entry.
- **Change Summary:** Proposal 001 (Repository Hierarchy) closed as absorbed by Proposal 000. All seven of Proposal 001's candidate questions are answered by DL-033 and the disposition document.
- **Supersession Reference:** Proposal 001 absorbed by Proposal 000.

### CHG-012 — REPOSITORY_ARCHITECTURE.md Placed at Repository Root

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `REPOSITORY_ARCHITECTURE.md` (created at repository root).
- **Change Summary:** Contributor-facing architecture summary placed at the repository root. Document explains the doctrine-centered architecture in plain language for contributors and reviewers. Includes the six principles (Doctrine defines truth; Constitution operationalizes doctrine; Implementation realizes doctrine; Governance controls repository evolution; Source Material informs but does not bind; Subsystems must anchor to canonical content), a placement table, conflict-handling guidance, and pointers to deeper governance reading.
- **Supersession Reference:** None. New orientation surface; does not supersede the Manifest.

### CHG-013 — DL-XXX Placeholders Replaced with DL-033

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `repository_manifest.md`; `canonical_definitions.md`; `ontology_registry.md`; `01_doctrine_ontology/12_constitutional_principles_draft.md`.
- **Change Summary:** Pre-ratification DL-XXX placeholders in the four annotated files replaced with the ratified Decision identifier DL-033. No other content modified; annotations now cite the ratified Decision.
- **Supersession Reference:** None. Reference update only.

### CHG-014 — RB-003 Ratified as DL-034

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-034 entry appended; header note updated to reflect operative range DL-029 through DL-034).
- **Change Summary:** RB-003 (Progression Model Reconciliation) ratified as DL-034. The OSLO Evolution Framework is the canonical multi-axis progression taxonomy. Four distinct but correlated axes ratified: Cognition Scope (Doctrine 02 canonical), Product Identity (Doctrine 09 canonical), Trust Gradient (Doctrine 09 / Article 41 aligned), Execution Depth (Doctrine 10 / Article 43 aligned). Doctrine prevails over Constitution where stage labels or counts conflict.
- **Supersession Reference:** Closes RB-003. Partially resolves RB-010 with respect to Draft Principle 17. Partially unblocks RB-015.

### CHG-015 — RB-003 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `01_governance/decisions/rb_003_disposition.md` (created).
- **Change Summary:** Full RB-003 disposition document placed in `07_governance/`. Document records the OSLO Evolution Framework, the four ratified axes, the ratified vs provisional status of each label, affected artifacts, and backlog impacts.
- **Supersession Reference:** None.

### CHG-016 — Constitution Articles 40 and 44 Annotated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `01_governance/constitution/08_product_evolution_constitution.md` (inline Governance Notes added to Article 40 and Article 44).
- **Change Summary:** Article 40 annotated to record that Doctrine 09's "Governed Organizational Cognition" label prevails over the Article's "Governance infrastructure" label at Stage 3 of Product Identity. Article 44 annotated to record that Doctrine 02's four-stage Cognition Scope arc prevails over the Article's five-stage arc, and that Portfolio Cognition is a provisional long-term capability. Article body text is not amended; the annotations declare doctrinal precedence and provisional status.
- **Supersession Reference:** Article 40 Stage 3 label and Article 44 five-stage arc are dispositioned as provisional under doctrinal precedence (DL-033 conflict resolution model; DL-034 application).

### CHG-017 — Draft Principle 17 Annotated as Absorbed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `01_doctrine_ontology/12_constitutional_principles_draft.md` (absorption note added inline to Draft 17).
- **Change Summary:** Draft Principle 17's substantive content is absorbed by Doctrine 02. Annotation added inline to record that Draft 17 no longer carries independent doctrinal force and that its substantive content is canonized through Doctrine 02's four-stage Cognition Scope arc. The remaining 19 Draft principles are unaffected and continue under the file-level Governance Status acknowledgment pending RB-010 full disposition.
- **Supersession Reference:** Draft 17 superseded as an independent doctrinal statement; its content is now sourced from Doctrine 02.

### CHG-018 — Backlog Updates for DL-034

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `01_governance/backlog/revision_backlog.md` (RB-003 closed; RB-010 updated to record Draft 17 absorption; RB-015 annotated with partial unblock).
- **Change Summary:** RB-003 closed with DL-034 as the closing Decision. RB-010 updated to record that Draft Principle 17 is absorbed by Doctrine 02 (RB-010 remains Partially Closed; the remaining 19 Draft principles continue pending RB-010 full disposition). RB-015 annotated to record that the progression-model ambiguity that previously blocked Project MRI's analytical placement is now resolved; RB-015 remains Open with RB-004 as the upstream blocker for the scoping decision itself.
- **Supersession Reference:** RB-003 closed; RB-010 partial scope reduced.

### CHG-019 — canonical_definitions.md Updated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `canonical_definitions.md` (Maturity and Progression Concepts section updated; OSLO Evolution Framework and four axes registered).
- **Change Summary:** Registered the OSLO Evolution Framework as an Established term. Registered Cognition Scope, Product Identity, Trust Gradient, and Execution Depth as Established axis entries with canonical doctrinal sources. The pre-existing Organizational Cognition Arc entry annotated to indicate reframing as the Cognition Scope axis.
- **Supersession Reference:** None. New entries; the prior Organizational Cognition Arc entry retained with a reframing note.

### CHG-020 — ontology_registry.md Updated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `ontology_registry.md` (Cognition and Progression Plane section updated; four axes registered; Portfolio Cognition and Long-Term Direction items marked Provisional).
- **Change Summary:** Cognition and Progression Plane reorganized around the ratified OSLO Evolution Framework. Four axes registered as Established entries with canonical sources. Portfolio Cognition reclassified from Proposed to Provisional. Long-Term Direction items registered as Provisional. Predecessor entries (Organizational Cognition Arc, Trust Evolution, Execution Maturity Phases, Product Evolution Stages) noted as reframed by the ratified axes. Reconciled conflicts recorded.
- **Supersession Reference:** Predecessor entries reframed (not deleted) as components of the ratified framework.

### CHG-021 — RB-010 Ratified as DL-035

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-035.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-035 entry appended; header note updated to reflect operative range DL-029 through DL-035).
- **Change Summary:** RB-010 (Resolve Constitutional Principles Draft vs Constitution Articles) ratified as DL-035. The Constitutional Principles Draft is reclassified as non-canonical Source Material and relocated from the Doctrine layer to `00_raw_transcript/`. Of 20 original Draft principles, Draft 17 remains absorbed by Doctrine 02 per DL-034; the remaining 19 are dispositioned by reclassification (18 represented by Constitution Articles; Draft 18 captured by Article 2 and Drift Warning 2).
- **Supersession Reference:** Closes RB-010. Supersedes the pre-ratification "Governance Status" annotation on the original file path and the DL-034 inline Draft 17 absorption note (both folded into the Historical Artifact header at the new file location).

### CHG-022 — RB-010 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-035.
- **Affected Artifacts:** `01_governance/decisions/rb_010_disposition.md` (created).
- **Change Summary:** Full RB-010 disposition document placed in `07_governance/`. Document records the selected Option C disposition, rationale, rejected options, effects on Doctrine and Constitution, effects on DL-033 and DL-034, backlog impacts, citation rule changes, affected artifacts, and required repository actions.
- **Supersession Reference:** None.

### CHG-023 — Constitutional Principles Draft Relocated and Reclassified

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-035.
- **Affected Artifacts:** `01_doctrine_ontology/12_constitutional_principles_draft.md` (removed); `00_raw_transcript/05_constitutional_principles_draft.md` (placed with Historical Artifact header).
- **Change Summary:** File relocated from the Doctrine layer to the Source Material layer. The pre-ratification "Governance Status" header section and the DL-034 inline Draft 17 absorption note are superseded by a single "Historical Artifact" header section in the relocated file. The 20 principles are preserved verbatim in their original drafted form. The file is now non-canonical and cannot be cited as authority.
- **Supersession Reference:** Pre-ratification annotation and DL-034 inline Draft 17 note folded into the Historical Artifact header.

### CHG-024 — Raw Transcript Index Updated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-035.
- **Affected Artifacts:** `00_raw_transcript/00_transcript_index.md` (entry 5 added).
- **Change Summary:** Index updated to register the relocated Constitutional Principles Draft as entry 5, noting its historical-artifact provenance and non-canonical status. Existing entries 1–4 unchanged.
- **Supersession Reference:** None.

### CHG-025 — RB-010 Closed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-035.
- **Affected Artifacts:** `01_governance/backlog/revision_backlog.md` (RB-010 status changed from Partially Closed to Closed; Disposition, Closed By, and Date Closed fields updated).
- **Change Summary:** RB-010 closed in the revision backlog with DL-035 recorded as the final closing Decision. Prior partial closures by DL-033 and DL-034 preserved in the historical record of the entry.
- **Supersession Reference:** Supersedes the prior Partially Closed status of RB-010.

### CHG-026 — RB-001 Ratified as DL-036

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-036 entry appended; header note updated to reflect operative range DL-029 through DL-036; DL-036 noted as Ratified with Conditions).
- **Change Summary:** RB-001 (Canonical Registry Consolidation) ratified as DL-036 with disposition Accepted with Conditions. The bounded Registry Foundation (Resolutions R1–R8) is adopted. Eight closing-Decision clarifications are recorded in the disposition document as narrative guidance. Bounded scope respected: no doctrinal introduction, no Constitution amendment, no Implementation Spec edits, no ontology conflict resolution, no new backlog entries.
- **Supersession Reference:** Closes RB-001. Supersedes the legacy "Established" and "Established (split source)" status flags in registry surfaces.

### CHG-027 — RB-001 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `01_governance/decisions/rb_001_disposition.md` (created).
- **Change Summary:** Full disposition document placed in `07_governance/`. Document records the eight Resolutions as ratified, the eight Clarifications, effects on canonical surfaces, effects on backlog items, and required repository actions.
- **Supersession Reference:** None.

### CHG-028 — Surface Authority Rule Recorded in Registry Surfaces

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (Status section updated); `ontology_registry.md` (Status section updated).
- **Change Summary:** Resolution R1 ratified: root `canonical_definitions.md` is the Governance-tier orientation registry; Constitution Article 10 is the Content-tier definitional surface; Article 10's definition is authoritative operational expression where consistent with Doctrine; Doctrine prevails over Article 10 where they substantively conflict (Clarification #1). The relationship between the two surfaces is now operationally declared. Constitution Article 10 is NOT amended; only its status is recorded in the Governance-tier registry.
- **Supersession Reference:** Supersedes the pre-ratification DL-033 dual-surface note in `canonical_definitions.md` Status section with the now-ratified operational rule.

### CHG-029 — Status Taxonomy Adopted and Legacy Flags Migrated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (Status section + existing entries reclassified); `ontology_registry.md` (Status section + existing entries reclassified).
- **Change Summary:** Resolution R2 ratified: six status flags adopted (Canonical, Provisional, Proposed, Conflicting, Undefined, Duplicate). Resolution R3 ratified: status-change rules declared. Clarification #2 applied: existing "Established" entries migrated to "Canonical" via clerical bulk replacement; existing "Established (split source)" entries migrated to "Conflicting" except Organizational Cognition Arc (Clarification #7 applies; reclassified as Duplicate). Clarification #8 applied: tie-breaking priority order declared (Conflicting > Undefined > Proposed > Provisional > Duplicate > Canonical). Migration is clerical; no individual entry review required.
- **Supersession Reference:** Supersedes legacy "Established" and "Established (split source)" flag usage.

### CHG-030 — Nine Doctrinal Concepts Registered

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (nine entries added in new section "Doctrinal Concepts Registered by DL-036 (R4)"); `ontology_registry.md` (nine entries added in new section "Doctrinal Concepts Registered by DL-036 (R4)" with plane assignments).
- **Change Summary:** Resolution R4 ratified: nine canonical doctrinal concepts registered using existing Doctrine sources only. Concepts registered: Dynamic Systems Orientation; Constitutional Principle (test question); Epistemic Governance; Flawed Intended Reality Handling; Stability vs Movement; Shared Cognition Principle; Narrative Views; Freemium Doctrine; Strategic UX Doctrine. Each entry cites existing doctrinal source. Status: Canonical. Per Clarification #3, R4 is PRD-authorized at the Resolution level by DL-036; per-entry registrations are clerical executions under the umbrella authorization. Doctrine files are not edited.
- **Supersession Reference:** None (registrations of previously unregistered concepts).

### CHG-031 — Four Predecessor Names Deprecated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (Organizational Cognition Arc entry updated to Duplicate status; new section "Deprecated Predecessor Names (per DL-036 R5)" added with Strategic Arc, Trust Evolution, Intelligence Visibility Doctrine entries); `ontology_registry.md` (Predecessor Entries section replaced with formal Duplicate-status deprecation table; new Emotional-and-Visibility deprecation table added for Intelligence Visibility Doctrine).
- **Change Summary:** Resolution R5 ratified: four predecessor names formally deprecated with Duplicate status. Strategic Arc → Cognition Scope (DL-034). Organizational Cognition Arc → Cognition Scope (DL-034; extends existing CHG-019 reframing per Clarification #7). Trust Evolution → Trust Gradient (DL-034). Intelligence Visibility Doctrine → Progressive Visibility (DL-016 Stated grandfathered per Clarification #4; substantively aligned with Article 25). Source files (Doctrine, Constitution) are NOT edited; deprecation operates only in registry surfaces.
- **Supersession Reference:** Extends CHG-019 (Organizational Cognition Arc reframing) into formal Duplicate-status deprecation per Clarification #7.

### CHG-032 — Provisional Term Disambiguated in Registry

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (Provisional disambiguation declared in Status section).
- **Change Summary:** Resolution R6 ratified: "Provisional" disambiguated between Epistemic Label usage (Spec 05) and Governance Status usage (R2 taxonomy). Registry context uses qualified forms where ambiguity could arise. Per Clarification #6, R6 operates in registry context only; Spec 05's "Provisional" Epistemic Label is unchanged and reserved for RB-007 reconciliation. Inventory I-A item 1 flags the Spec 05 additional labels as unanchored; the three references (R6, I-A item 1, RB-007) operate at distinct layers without contradiction.
- **Supersession Reference:** None.

### CHG-033 — Inventories I-A and I-B Placed Inline in Ontology Registry

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `ontology_registry.md` (two new sections added).
- **Change Summary:** Resolution R7 ratified: two inventories placed inline in `ontology_registry.md` per Clarification #5. Inventory I-A — Unanchored Implementation Concepts (13 conceptual groups) added as a new section after the existing "Concepts Used But Not Registered" section. Inventory I-B — Registry Entries Lacking Authoritative Definitions (4 entries: Artifact, Attention Queue, Project MRI, Outcome Space) added immediately following I-A. Both inventories are open and updateable; future Decisions may add or remove items via clerical changelog entries. Inventories feed RB-004 (general doctrine stubs), RB-012, RB-013, RB-014, RB-015, RB-016, RB-017, RB-018 as input.
- **Supersession Reference:** None (new observation artifacts).

### CHG-034 — Citation Paths for Four Axes Declared; RB-001 Closed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-036.
- **Affected Artifacts:** `canonical_definitions.md` (axis entries reflect ratified citation paths); `ontology_registry.md` (Cognition and Progression Plane axis entries reflect ratified citation paths); `01_governance/backlog/revision_backlog.md` (RB-001 status changed from Proposed to Closed; Disposition, Closed By, Date Closed recorded).
- **Change Summary:** Resolution R8 ratified: canonical citation paths formalized for the four OSLO Evolution Framework axes. Cognition Scope cites Doctrine 02. Product Identity cites Doctrine 09. Trust Gradient cites Doctrine 09 and Article 41 (aligned). Execution Depth cites Doctrine 10 and Article 43 (aligned). Citation paths consistent with DL-034 and formally promoted into the registry as operational citation rules. RB-001 closed in revision backlog with DL-036 as closing Decision.
- **Supersession Reference:** Closes RB-001.

### CHG-035 — DL-037 Ratified; Phase 1 Pending Framework Verification Gate

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-037 entry appended; header note updated to reflect operative range DL-029 through DL-037; DL-037 noted as Ratified with Conditions); `01_governance/decisions/proposal_003_restructure_disposition.md` (created at pre-Phase-1 location). Both files will be relocated to `01_governance/decisions/` during Phase 1 execution.
- **Change Summary:** Repository Domain Restructure (Proposal 003) ratified as DL-037 with disposition Accepted with Conditions. Ten closing-Decision clarifications recorded in the disposition document. Five-phase migration authorized as execution steps within the single Decision. Rollback authority granted to AI for constraint violations, scoped exclusively to migration execution actions under DL-037 and not extending to reversing owner-ratified Decisions, Frameworks, or Stated decisions DL-001 through DL-028 preserved under DL-032. Bounded scope respected: no doctrinal/constitutional/spec body edits; no ontology conflict resolution; no doctrinal stubs; no new backlog entries; RB-020 remains Open through closure. Phase 1 execution pending owner Framework 001 and 001A verification gate per Clarification #2.
- **Supersession Reference:** No prior Decision superseded. Establishes the post-migration repository structure as canonical physical organization.

### CHG-036 — Phase 1 Complete (Governance Stabilization)

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `01_governance/` directory created with 9 subdirectories (`doctrine/`, `constitution/`, `canonical_definitions/`, `ontology/`, `decisions/`, `backlog/`, `changelog/`, `frameworks/`, `manifest/`); `01_governance/README.md` created; `01_governance/frameworks/framework_001.md` created from already-ratified content per Clarification #2 (owner verified substantive match); `01_governance/frameworks/framework_001A.md` created from already-ratified content per Clarification #2 (owner verified substantive match with one revision: Purpose section omitted to preserve strict verbatim alignment with originally-issued text). 38 governance content files relocated (13 Doctrine; 14 Constitution; 6 governance objects from `07_governance/` to `01_governance/decisions/` — including `proposal_003_restructure_disposition.md` newly placed pre-Phase-1; `revision_backlog.md` to `01_governance/backlog/`; `changelog.md` to `01_governance/changelog/`; root `canonical_definitions.md`, `ontology_registry.md`, `repository_manifest.md` to their respective `01_governance/` subdirectories). Path-reference updates executed mechanically across 12 files per the Reference Update Matrix. Substitution patterns: `01_doctrine_ontology/` → `01_governance/doctrine/`; `02_ux_constitution/` → `01_governance/constitution/`; `07_governance/{decision_log, proposal_000_disposition, proposal_003_restructure_disposition, rb_001_disposition, rb_003_disposition, rb_010_disposition, revision_backlog, changelog}.md` → appropriate `01_governance/{decisions, backlog, changelog}/` paths. Remaining `07_governance/` references in change summaries are historical narrative describing past placement events; preserved per the Clarification #4 historical-vs-forward distinction.
- **Change Summary:** Phase 1 of the Repository Domain Restructure complete. All Doctrine, Constitution, and Governance content relocated to `01_governance/`. No body content modified. Framework files materialized faithfully from DL-030 and DL-031 dispositions per owner verification (Clarification #2). Framework 001A draft revised to remove Purpose section per owner direction for strict verbatim preservation of originally-issued content. DL-036 substantive content preserved; only path citations updated (Clarification #7). Manifest pre-ratification annotation verified to contain no path references; no annotation updates required (Clarification #5). Legacy directories `01_doctrine_ontology/`, `02_ux_constitution/`, and `07_governance/` are now empty pending final removal in Phase 5.
- **Supersession Reference:** Legacy paths superseded: `01_doctrine_ontology/*`, `02_ux_constitution/*`, `07_governance/*`, root `canonical_definitions.md`, `ontology_registry.md`, `repository_manifest.md` now operative at their `01_governance/` paths.

### CHG-037 — Phase 2 Complete (Product Organization)

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `02_product/` directory created with 5 subdirectories (`user_experience/`, `plg/`, `workflows/`, `collaboration/`, `tiering/`); `02_product/README.md` created; 8 Implementation Specs relocated from `03_implementation_specs/` to `02_product/`: Spec 01 (Product Shell Layout Wireframe) → `02_product/user_experience/`; Spec 02 (PLG 60-Second Flow Wireframes) → `02_product/plg/`; Spec 03 (Outcome Space Workspace Wireframes) → `02_product/user_experience/`; Spec 04 (Core Navigation & Information Architecture) → `02_product/user_experience/`; Spec 06 (Interaction Rules) → `02_product/user_experience/`; Spec 07 (Workflow Specifications) → `02_product/workflows/`; Spec 10 (Collaboration & Sharing Logic) moved whole → `02_product/collaboration/`; Spec 12 (Freemium / Tier Behavior Logic) moved whole → `02_product/tiering/`.
- **Change Summary:** Phase 2 of the Repository Domain Restructure complete. Product-shaped Implementation Specs relocated to `02_product/`. Spec body content unchanged. Specs 10 and 12 moved whole per Clarification #3 — no header notes added, splits deferred to follow-on Proposals if owner directs. Future product subdirectories (positioning, product_strategy, onboarding, sharing, virality, security_and_compliance) documented in README as potential expansion areas, not pre-created as empty folders.
- **Supersession Reference:** Legacy paths superseded for relocated specs.

### CHG-038 — Phase 3 Complete (Architecture Extraction)

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `03_architecture/` directory created with 4 subdirectories (`runtime_architecture/`, `judgement_layer/`, `governance_layer/`, `components/`); `03_architecture/README.md` created with future-architecture-roadmap section listing 16 potential architecture domains as documentation (not pre-created as empty folders); 4 Implementation Specs relocated from `03_implementation_specs/` to `03_architecture/`: Spec 05 (Component System Specification) → `03_architecture/components/`; Spec 08 (State Logic & State Machines) → `03_architecture/runtime_architecture/`; Spec 09 (Confidence & Integrity Logic) → `03_architecture/judgement_layer/`; Spec 11 (Governance & Override Logic) → `03_architecture/governance_layer/`.
- **Change Summary:** Phase 3 of the Repository Domain Restructure complete. Architecture-shaped Implementation Specs relocated to `03_architecture/`. Spec body content unchanged. Future architecture subdirectories documented in README only; no empty folders pre-created per the bounded-scope principle.
- **Supersession Reference:** Legacy paths superseded for relocated specs.

### CHG-039 — Phase 4 Complete (Execution Tracking)

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `05_execution/implementation_tracking/` directory created; `05_execution/README.md` created (future operational subdirectories roadmap, initiatives, milestones documented but not created); 2 Implementation Specs relocated from `03_implementation_specs/` to `05_execution/implementation_tracking/`: Spec 13 (Implementation Backlog) and Spec 14 (Open Questions & Design Risks).
- **Change Summary:** Phase 4 of the Repository Domain Restructure complete. Operational tracking Specs relocated to `05_execution/implementation_tracking/`. Spec body content unchanged. Future operational subdirectories documented in README only.
- **Supersession Reference:** Legacy paths superseded for relocated specs.

### CHG-040 — Phase 5 Research and Subsystems Relocations Complete

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `04_research/` directory created with 2 subdirectories (`transcripts/`, `historical_artifacts/`); `04_research/README.md` created; 7 raw transcript items relocated to `04_research/transcripts/` (00_transcript_index.md, 01_foundational_product_experience.md, 02_plg_freemium_intake_confidence.md, 03_collaboration_governance_epistemics.md, 04_ontology_strategy_constitutional_principles.md, README.md); Historical Artifact `05_constitutional_principles_draft.md` relocated to `04_research/historical_artifacts/` with Clarification #4 reference treatment applied (historical origin path `01_doctrine_ontology/12_constitutional_principles_draft.md` preserved verbatim; forward-looking references to disposition documents updated to `01_governance/decisions/rb_003_disposition.md` and `01_governance/decisions/rb_010_disposition.md`); `03_implementation_specs/00_index.md` relocated to `04_research/historical_artifacts/03_implementation_specs_index_historical.md` per Clarification #8 (supersedes Proposal 003 Artifact 2 retirement treatment; converts retirement to relocation); `03_implementation_specs/README.md` relocated to `04_research/historical_artifacts/03_implementation_specs_readme_historical.md` per Clarification #8; `subsystems/` directory created with `project_mri/` subdirectory; `04_project_mri/README.md` relocated to `subsystems/project_mri/README.md`; `04_research/transcripts/00_transcript_index.md` Entry 5 reference updated to point to new historical artifact location while preserving historical origin reference.
- **Change Summary:** Phase 5 Research and Subsystems relocations complete. Raw transcripts and Historical Artifact preserved at non-canonical locations per DL-033 and DL-035. Index file disposition executed per Clarification #8: relocated as historical content with `_historical.md` suffix; no Historical Artifact headers added (header treatment per Clarification #8 preserved no-spec-edits constraint). Cursor-like AI-native IDE identity claim remains visible in historical record; Inventory I-A item 9 continues to flag it as unanchored.
- **Supersession Reference:** Legacy `00_raw_transcript/` and `04_project_mri/` paths superseded.

### CHG-041 — Phase 5 Root Files Updated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** Root `README.md` populated per Bounded Executor Package Deliverable 5 (after Clarification #6 owner confirmation); root `CLAUDE.md` populated per Bounded Executor Package Deliverable 6 (after Clarification #6 owner confirmation); root `REPOSITORY_ARCHITECTURE.md` revised per Bounded Executor Package Deliverable 7 (after Clarification #6 owner confirmation).
- **Change Summary:** Root orientation files populated. Each file content traces to existing ratified Decisions (DL-029 through DL-037), Framework provisions, or structural descriptions of the post-migration repository. No new normative claims introduced. Owner reviewed drafts against orientation-only constraint before placement per Clarification #6.
- **Supersession Reference:** Empty pre-existing `README.md` and `CLAUDE.md` superseded; prior `REPOSITORY_ARCHITECTURE.md` superseded by revised version.

### CHG-042 — Legacy Directories Removed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** Removed: `00_raw_transcript/`, `01_doctrine_ontology/`, `02_ux_constitution/`, `03_implementation_specs/`, `04_project_mri/`, `07_governance/` (all empty after Phases 1–5 relocations).
- **Change Summary:** Legacy directories removed after grep audit confirmed remaining old-path references are limited to historical-narrative descriptions in changelog change summaries and disposition documents (preserved per Clarification #4 historical-vs-forward distinction). Removal preceded by Post-Migration Validation Checklist verification.
- **Supersession Reference:** Legacy top-level directory structure fully superseded by the new domain taxonomy.

### CHG-043 — DL-037 Migration Complete

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-037.
- **Affected Artifacts:** `01_governance/changelog/changelog.md` (this entry); `01_governance/decisions/decision_log.md` (DL-037 status confirmed Ratified with Conditions; migration complete).
- **Change Summary:** Repository Domain Restructure migration (DL-037) complete. All five phases executed sequentially under owner phase gates. 61 files relocated (matrix item 52 and 53 reclassified from retirement to relocation per Clarification #8; total relocation count 61, retirements 0). 12 files explicitly created or populated (Framework 001, Framework 001A with Purpose section omitted per owner direction, five top-level domain READMEs, this disposition document, root README, root CLAUDE.md, project_mri README inherited from migration). 14 files received path-reference housekeeping updates. 6 legacy directories removed after empty-state verification. Zero substantive content edits performed. Repository operates under the new domain taxonomy: `01_governance/`, `02_product/`, `03_architecture/`, `04_research/`, `05_execution/`, `subsystems/`. RB-020 remains Open per Clarification #1; owner reviews post-migration README and CLAUDE.md content for potential clerical closure under DL-036 R3 precedent. Rollback authority not invoked during execution. No constraint violations detected.
- **Supersession Reference:** Migration complete. No further phases required.

### CHG-044 — GOV-CP-000 Ratified as DL-038 (Context Plane Classification)

- **Date:** 2026-05-30
- **Authorizing Decision:** DL-038.
- **Affected Artifacts:** `01_governance/decisions/gov_cp_000_disposition.md` (created); `01_governance/decisions/decision_log.md` (DL-038 entry appended; Governance Notes operative range updated from DL-029–DL-037 to DL-029–DL-038); `01_governance/changelog/changelog.md` (this entry).
- **Change Summary:** Repository owner ratified GOV-CP-000 (Context Plane Classification Ratification) as DL-038 with five clarifying conditions. The Context Plane is canonically classified as a cross-cutting architectural plane responsible for managing external context before canonical entry into the Knowledge Layer. The classification corresponds to Option B of the five candidates evaluated during governance review. The Decision constitutes partial adoption of Context Plane status (classification only); no Specification, Contract, layer-stack inclusion, diagram inclusion, or follow-on documents are adopted. GOV-CP-001 (Context Plane Relationship Ratification) pause is lifted but GOV-CP-001 does not automatically re-activate. Follow-on alignment items (architectural-overview document alignment, integrity contracts' Layer Authority attributions, eight follow-on documents listed in the Design Description, Layer Specifications' dependency declarations, Ingestion & Transformation Contract) are explicitly deferred. No body content edits performed on any other repository file. Canonical layer stack unchanged. Runtime behavior unchanged.
- **Supersession Reference:** No prior Decision superseded. Context Plane Design Description v1.0 retains "Proposed architectural extension" status; DL-038 is partial adoption of one aspect (classification only).

### CHG-045 — GOV-CP-001B Ratified as DL-039 (Context Plane Explicit Authority Attribution)

- **Date:** 2026-05-30
- **Authorizing Decision:** DL-039.
- **Affected Artifacts:** `01_governance/decisions/gov_cp_001b_disposition.md` (created); `01_governance/decisions/decision_log.md` (DL-039 entry appended; Governance Notes operative range updated from DL-029–DL-038 to DL-029–DL-039); `01_governance/changelog/changelog.md` (this entry).
- **Change Summary:** Repository owner ratified GOV-CP-001B (Context Plane Explicit Authority Attribution Ratification — Narrow) as DL-039 with two clarifying conditions. The Decision consolidates two pre-existing canonical authority attributions at the Decision Log level: Context Plane has explicit authority over raw record identity and idempotency (per OSLO Raw Record Identity & Idempotency Contract v1.0 line 7), and shared authority with Knowledge Layer over time semantics and ordering for externally sourced signals (per OSLO Time Semantics & Ordering Contract v1.0 line 5). The Decision explicitly does not resolve Context Plane containment for Ingestion & Transformation, Execution Signal Ingestion, Capture → Transform → Commit Boundary, Raw Input Isolation, Knowledge Layer Command & Write Contract, or Evidence Chain Integrity. The owner-selected path was MODIFY (refining Framework 001A Review Concern C1 wording from "makes this structural asymmetry canonical" to "makes this structural asymmetry explicit in the governance record") followed by APPROVE. The two conditions (Terminology preservation; Shared authority operational mechanics deferred) explicitly defer scope-definition and arbitration-mechanism work. No body content edits performed on any other repository file. Canonical layer stack unchanged. Runtime behavior unchanged. Integration Moratorium directive remains operative with respect to OGAP v1.0 and GOV-FWK-001A-DECISION-READY adoptions.
- **Supersession Reference:** No prior Decision superseded. Two pre-existing Layer Authority attributions in the two integrity contracts are affirmed as the post-DL-038 canonical Context Plane explicit authority. GOV-CP-001 remains paused per DL-038 Condition 4; not affected by DL-039.

### CHG-046 — OGAP v1.0 Ratified as DL-040 (Protocol Adoption)

- **Date:** 2026-05-30
- **Authorizing Decision:** DL-040.
- **Affected Artifacts:** `01_governance/protocols/` (directory created); `01_governance/protocols/ogap_v1.md` (created — OSLO Governance Acceleration Protocol v1.0 full text); `01_governance/decisions/gov_ogap_disposition.md` (created); `01_governance/decisions/decision_log.md` (DL-040 entry appended; Governance Notes operative range updated from DL-029–DL-039 to DL-029–DL-040; status taxonomy updated to reflect "Ratified with Clarifications" for DL-040); `01_governance/changelog/changelog.md` (this entry).
- **Change Summary:** Repository owner ratified the OSLO Governance Acceleration Protocol (OGAP) v1.0 as DL-040 with five clarifications. OGAP is adopted as a Protocol (a newly-introduced governance instrument category), not as a Framework. The five clarifications establish: (1) OGAP is a Protocol category, not a new Framework; (2) OGAP does not modify Framework 001 or Framework 001A; (3) OGAP operates as a routing and acceleration protocol layered over Framework 001 and Framework 001A; (4) The CLAUDE.md prohibition on creating new Frameworks remains unchanged; (5) OGAP is authorized because it is owner-ratified as a Protocol, not because AI created a new governance Framework. OGAP v1.0's nine stages (Triage, Discovery, Sufficiency Gate, Readiness Score, Decision Ready Rule, Proposal Generation with Type A–E Templates, Review, Owner Decision, Disposition Processing) and Governance Stop Rule become operative governance discipline. Framework 001, Framework 001A, CLAUDE.md, doctrine, constitution, ontology registry, canonical definitions, contracts, and layer specifications are unaffected. Canonical layer stack unchanged. Runtime behavior unchanged. Integration Moratorium directive partially satisfied (DL-039 and DL-040 integrated; one Decision Ready item remains: GOV-FWK-001A-DECISION-READY).
- **Supersession Reference:** No prior Decision superseded. Introduces the Protocol governance instrument category. Does not modify Framework 001 (DL-030), Framework 001A (DL-031), or the CLAUDE.md Governance Discipline directive.

### CHG-047 — GOV-FWK-001A-DECISION-READY Ratified as DL-041 (DECISION-READY State Adoption)

- **Date:** 2026-05-30
- **Authorizing Decision:** DL-041.
- **Affected Artifacts:** `01_governance/frameworks/framework_001A_decision_ready.md` (created — Framework 001A supplement defining the DECISION-READY state); `01_governance/decisions/gov_fwk_001a_decision_ready_disposition.md` (created); `01_governance/decisions/decision_log.md` (DL-041 entry appended; Governance Notes operative range updated from DL-029–DL-040 to DL-029–DL-041; status taxonomy updated to reflect DL-040 and DL-041 as "Ratified with Clarifications"); `01_governance/changelog/changelog.md` (this entry).
- **Change Summary:** Repository owner ratified GOV-FWK-001A-DECISION-READY (DECISION-READY State Adoption) as DL-041 with five clarifications. DECISION-READY is added as a Framework 001A state with explicit entry criteria (ambiguity confirmed; Evidence Sufficiency Gate passes; Decision Readiness Score ≥ 16; candidate options known; no material unresolved evidence gaps), governance effects (proposal generation permitted; Review constrained to five focus areas; additional reconciliation prohibited absent Stop Rule trigger), and Stop Rule triggers (new evidence, contradiction discovered, owner direction). The five clarifications establish: (1) DECISION-READY is a Framework 001A state; (2) entry criteria are as enumerated; (3) governance effects upon entry are as enumerated; (4) DECISION-READY does not replace any existing Framework 001A state and is a pre-decision governance state; (5) Framework 001 and Framework 001A otherwise remain unchanged. Framework 001A's existing Review schema and Review states are unmodified. Framework 001 lifecycle is unmodified. OGAP v1.0 (DL-040) text unmodified; DECISION-READY references OGAP Stages 3, 4, and 5 by attribution. CLAUDE.md unmodified. Doctrine, constitution, ontology registry, canonical definitions, contracts, layer specifications unaffected. Canonical layer stack unchanged. Runtime behavior unchanged. Integration Moratorium lift conditions satisfied with respect to the three Decision Ready items the Moratorium addressed (DL-039, DL-040, DL-041); lift status owner-determined.
- **Supersession Reference:** No prior Decision superseded. Supplements Framework 001A (DL-031) by adding the DECISION-READY state without modifying Framework 001A's existing text.

### CHG-048 — DL-042 Ratified (Integration Moratorium Closure / Governance Stabilization Complete)

- **Date:** 2026-05-30
- **Authorizing Decision:** DL-042.
- **Affected Artifacts:** `01_governance/decisions/gov_moratorium_closure_disposition.md` (created); `01_governance/decisions/decision_log.md` (DL-042 entry appended; Governance Notes operative range updated from DL-029–DL-041 to DL-029–DL-042; status taxonomy updated to record DL-042 as Ratified unconditional; operative governance framework set enumerated as Framework 001, Framework 001A, OGAP v1.0, DECISION-READY); `01_governance/changelog/changelog.md` (this entry).
- **Change Summary:** Repository owner ratified DL-042 closing the temporary Integration Moratorium and marking the governance stabilization phase complete. The Moratorium served its purpose during the integration of GOV-CP-001B (DL-039), OGAP v1.0 (DL-040), and DECISION-READY (DL-041); its lift conditions were satisfied; closure is by explicit owner ratification rather than auto-lift. The repository governance state is now considered Operational. Future governance items shall be processed under Framework 001, Framework 001A, OGAP v1.0, and DECISION-READY. No additional governance acceleration mechanisms are presently authorized unless separately ratified through the standard governance process. Framework 001, Framework 001A, OGAP v1.0 protocol artifact, DECISION-READY supplement, CLAUDE.md, doctrine, constitution, ontology registry, canonical definitions, contracts, and layer specifications are unaffected. Canonical layer stack unchanged. Runtime behavior unchanged. GOV-CP-001 remains paused per DL-038 Condition 4 as a separate governance item; DL-042 does not address its disposition.
- **Supersession Reference:** Supersedes the temporary Integration Moratorium directive (operative-by-articulation from prior owner direction following GOV-CP-001B Review). The Moratorium is canonically Closed. The stabilization phase is canonically Complete. No prior ratified Decision superseded.

### CHG-049 — DL-043 Ratified (Release 1 Architecture & Epistemic Foundation, Consolidated A–J)

- **Date:** 2026-06-04
- **Authorizing Decision:** DL-043.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-043 entry appended; Governance Notes operative range updated DL-029–DL-042 → DL-029–DL-043; DL-043 recorded as Ratified with Conditions); `01_governance/decisions/RELEASE_1_ARCHITECTURE_FOUNDATION_CONSOLIDATED_RATIFICATION_DL043_DISPOSITION.md` (disposition document; status set to Ratified with Conditions); status banners flipped to canonical/ratified on `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1`, `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1`, `QA_GOVERNANCE_SPECIFICATION_V1`, `OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1`, `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001`, and the constituent decision documents (Reconciliation, Recommendation, Interpretation-Acceptance, Canonicalization-Control, Epistemic-State, Derived-Cognition-Lifecycle, User-Acceptance). **Authorized but execution-pending (separate change records):** revisions to `WAVE_A_CONTRACT_PACKAGE_002`, `RELEASE_1_RUNTIME_OBJECT_MODEL_V1`, `RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1`, `RELEASE_1_CONTRACT_INVENTORY_V1`, `RELEASE_1_CONTRACT_GENERATION_PLAN_V1`, `RELEASE_1_CAPABILITY_COVERAGE_REVIEW_V1`; re-homing of governed layer-engineering dirs; reconciliation of `CURRENT_TRUTH.md` / `OSLO_ARCHITECTURE_BASELINE_V1` to secondary-representation status.
- **Change Summary:** Repository owner ratified DL-043 as a single act consolidating ten constituent decisions (A–J): Cognitive Responsibility Architecture as canonical representation; Integrity-not-Authority R1 scope (Authority plane inactive in R1; Pkg 003-as-governance and Wave D dropped from R1); the Epistemic Boundary Invariant with rejection of a Canonicalization Control responsibility; the Epistemic State Model (Canonical = Attested; Derived non-canonical; Accepted deferred; Attested/Derived labels superseding Grounded/Candidate); the Derived Cognition Lifecycle (Attested self-attested Cognition History Records; two-axis replay; snapshot-based drift); the Autonomous Implementation Control System; User Acceptance Recording & Reconciliation (user-attested sub-class; version-pinned User Acceptance Record; Acceptance-Impact Assessment; additive and non-governance); QA Governance; Observability Governance; and the Application/Platform Capability Classification. ESC-0 (active-architecture conflict) is closed. The Runtime Environment Constraint Profile is authorized as the next artifact and the single remaining hard gate to coding. Numeric calibration values (determinism/drift/band tolerances) remain an open owner-supplied input required before the affected outputs are implemented. Doctrine, Constitution, ontology registry, canonical definitions (except the DL-004 overlay note), and CLAUDE.md are unaffected.
- **Supersession Reference:** Supersedes the layer-as-primary representation of `OSLO_ARCHITECTURE_BASELINE_V1.md` (demoted to secondary dependency-ordering view, not deleted); the "Grounded/Candidate" labeling proposal (superseded by Attested/Derived); and the in-flight contract assumption of Authority-in-R1. No prior ratified Decision superseded; reconciles but does not modify the open conflict at DL-004.

### CHG-050 — Repository Reorganization (03_architecture + 02_product/specs sub-foldering)

- **Date:** 2026-06-04
- **Authorizing Decision:** Owner approval of `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` (structural, content-neutral; no DL ratification required).
- **Affected Artifacts:** `03_architecture/` 43 root files relocated into specifications/runtime_models/contracts/decisions/reviews/environment + legacy_layer_engineering/ (README.md retained at root); `02_product/specs/` 133 files relocated into ux/models/decisions/audits_reviews/data_api_nfr/testing_fixtures/planning (CURRENT_TRUTH.md retained at root); 14 per-folder README indexes added; one path reference updated in `OSLO_ARCHITECTURE_BASELINE_V1.md`; `REPOSITORY_ARCHITECTURE.md` sub-folder conventions added; `.gitignore` updated for `.obsidian/`.
- **Change Summary:** Moves-only reorganization executed via `git mv` (history preserved). Top-level 01–05 domain split unchanged. No document content edited except the single path-reference fix, the README indexes, and the REPOSITORY_ARCHITECTURE conventions note. Bare-filename cross-references (~1,442) are unaffected by relocation; only ~1 full-path reference required updating. No Doctrine, Constitution, contract, or architecture content was modified.
- **Supersession Reference:** None. Structural change; supersedes no Decision.

### CHG-051 — DL-044 Ratified (Release 1 Engineering Handoff, Consolidated A–D)

- **Date:** 2026-06-04
- **Authorizing Decision:** DL-044.
- **Affected Artifacts:** `01_governance/decisions/decision_log.md` (DL-044 entry appended; Governance Notes operative range updated DL-029–DL-043 → DL-029–DL-044; DL-044 recorded as Ratified with Conditions); `01_governance/decisions/RELEASE_1_ENGINEERING_HANDOFF_RATIFICATION_DL044_DISPOSITION.md` (disposition document; status set to Ratified with Conditions; renamed from `…_DRAFT.md`); status flipped to ratified/approved on `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`, `01_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md`, `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`, and `03_architecture/contracts/WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (Wave A/B/C/U/E packages owner-approved).
- **Change Summary:** Repository owner ratified DL-044 as a single act consolidating the four-constituent Release 1 engineering-enablement layer (A–D): adopting the Claude Code Implementation Constraints as the governing coding standard and pre-code gate; approving the Wave A (001 re-issue, 002, 00R), B, C, U, and E contract packages as CONFORMANT environment-independent sets per the consolidated conformance review (no Critical/Major; four Minor clarifications MF-A…MF-D non-blocking; Wave D out of R1); adopting the Calibration Defaults as tunable operative configuration; and ratifying the Deployment Governance Specification (protected `main`, Dev→Staging→Production with production deploy human-only, ordered CI gates including an epistemic-invariant gate, append-only canonical migration discipline, reversible releases, per-environment secrets, and Claude Code deployment STOP conditions). The Runtime Environment Constraint Profile is recorded as the canonical environment-binding anchor with R1–R5 reconciliations owner-confirmed. Release 1 readiness ≈93% (Ready With Controls); per-wave environment-bound implementation is authorized under the Control System readiness gate. Conditions: calibration values remain tunable; per-wave coding is gated on package approval and the readiness gate; production stays human-gated; build-time residuals (R1–R5 application, physical schema binding, audit-retention vs. compliance) applied at environment-bind. No Doctrine, Constitution, or architecture content modified.
- **Supersession Reference:** None. Extends DL-043 with the engineering-enablement layer; supersedes no prior Decision.

### CHG-052 — Archival of Superseded V1 Artifacts to historical_artifacts

- **Date:** 2026-06-04
- **Authorizing Decision:** Owner direction (repository hygiene; non-canonical artifacts only — no DL ratification required).
- **Affected Artifacts:** Seven already-superseded V1 documents relocated via `git mv` into `04_research/historical_artifacts/`, each given a one-line "Archived 2026-06-04 — superseded by <successor>" banner (content preserved; history retained): `OSLO_CAPABILITY_MATRIX_V1.md` and `OSLO_LINEAR_INITIATIVES_V1.md` (from repo root; replaced by their V2s); `CLARIFICATION_CANDIDATE_MODEL_V1.md` and `CLARIFICATION_CANDIDATE_INTEGRATION_SPEC_V1.md` (retired/superseded by the Recommendation system + Resolution Paths approach); `FINDING_WORKSPACE_SPECIFICATION_V1.md` and `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` (superseded/repositioned by the Finding/Recommendation Panel specs); and `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` (its stale "Active Release 1" status corrected to Historical before archival — it no longer governs implementation per its own banner).
- **Change Summary:** Repository-hygiene move to keep the active tree clean ahead of engineering handoff. Only documents that are explicitly retired/superseded with a named successor and no governing role were moved; no content was edited except the archive banners and the one stale-status correction. **Deliberately NOT moved** (intentionally retained, with reasons): the three model V1s (Confidence/CAF/Reliability — authoritative foundations that their V2s implement); the five "Future Architecture" deferred models (Resolution Candidate, Accepted Understanding, Governance, Review Request, Disposition — future-scope, preserved); `OSLO_ARCHITECTURE_BASELINE_V1.md` and `RELEASE_1_RUNTIME_LAYER_OWNERSHIP_SPECIFICATION_V1.md` (DL-043-ratified secondary representations); `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md` (ratified active under DL-043 constituent F); and the pre-DL-043 review/audit docs under `03_architecture/reviews/` (the designated historical reasoning trail). All inbound references were bare filenames and resolve from the new location; zero broken full-path references. No Doctrine, Constitution, contract, or architecture content modified.
- **Supersession Reference:** None. Structural/hygiene change; the artifacts were already superseded by prior decisions and successor documents. Supersedes no Decision.

### CHG-053 — DL-046 Ratified (Fast/Deep Modes + <60s Time-to-First-MRI, Wave B Contract Amendment)

- **Date:** 2026-06-04
- **Authorizing Decision:** DL-046.
- **Affected Artifacts:** `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` (amended — new §0.1 Analysis Modes clause; IC-WB-INFER/EVAL required-behavior item (5); QA-WB-INFER/EVAL positives, negatives, **a Time-to-First-MRI < 60 s performance gate**, and failure classifications; OBS-WB-INFER/EVAL mode+stage events and latency/completion metrics); `WAVE_A_CONTRACT_PACKAGE_001_ARTIFACT_INTAKE.md` and `WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` (DL-046 notes); `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (§1 re-checked — still CONFORMANT); `RELEASE_1_CONTRACT_INVENTORY_V1.md` (noted); `decision_log.md` (DL-046 entry; operative range → DL-029–DL-046); disposition + backlog drafts retired.
- **Change Summary:** Repository owner ratified DL-046, formalizing the **Fast Pass** and **Deep Pass** analysis modes and the owner-approved **Time-to-First-MRI < 60 s** target as explicit obligations in the ratified Wave B contracts, with clarifying notes to the Wave A intake and recompute contracts. `mode` (fast|deep) and `confidence_stage` (Orientation→Expanded→Validated) are added as **emission attributes** — no new responsibility or object — and a **QA performance gate** asserts the 60 s target; the 60 s is adopted as a ratified Release 1 NFR acceptance gate (Master Spec §20/M1). The Wave B conformance review was re-checked and remains CONFORMANT. Open: p50/p95 distribution and supported-project-size envelope remain `TBD – Owner Decision Required`. No architecture, Doctrine, or Constitution change.
- **Supersession Reference:** None. Amends (adds to) the DL-044-approved Wave B contracts; supersedes no Decision.

### CHG-054 — DL-047 Ratified (Contract-Coverage Resolution: Synthesis Engine · Interaction/Collaboration · Enumeration)

- **Date:** 2026-06-04
- **Authorizing Decision:** DL-047.
- **Affected Artifacts:** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1` (DL-047 Architecture Update — Perceive extraction; Infer synthesis/generation as Derived; Chat/CRR/Suggested-Fix placement); `RELEASE_1_RUNTIME_OBJECT_MODEL_V1` + `…BEHAVIOR_MODEL_V1` (new Derived/interaction objects + events); `WAVE_A_CONTRACT_PACKAGE_001`, `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING`, `WAVE_C_AND_U…`, `WAVE_E…` (DL-047 Additions); `RELEASE_1_CONTRACT_INVENTORY_V1`; `CONTRACT_GENERATION_FRAMEWORK_V1` (§E+ capability-to-contract traceability gate); phase plans II/III/IV/VI; `decision_log.md` (DL-047; range → DL-029–DL-047). Audit 002 + the DL-047 proposal retired.
- **Change Summary:** Owner ratified DL-047 as a whole, closing the cognitive contract-coverage gaps from Audit 002. The evidence→plan engine is now contracted: **Perceive performs source-attributed claim extraction** (evidence-attested, no Derived cognition) and **Infer is extended to synthesize a `SynthesizedPlanningModel` and generate `PlanningArtifact`s as Derived Cognition** (recomputable, CHR-per-generation, user-editable, never Attested-as-truth), with Evaluate seeding CAF/Confidence from the model — **no new responsibility**, preserving all DL-043 epistemic invariants. OSLO Chat is contracted as a Disclose-class interaction surface (writes no canonical); CAF Review Requests contract the response→evidence→Deep-Pass seam (workflow UI commodity per DL-043 J); Suggested Fixes are Advise candidates **applied only by the user** (no autonomous OSLO write); Validation Recommendations are an Advise type. False-Confidence Detection, the Understanding State Model, Progressive Disclosure, MRI sub-components, and assisted editing are enumerated into Wave B/E. A capability-to-contract traceability gate (Framework §E+) is adopted to prevent recurrence. Conformance to be re-confirmed at contract regeneration. No Doctrine or Constitution change.
- **Supersession Reference:** None. Additive within existing responsibilities; supersedes no Decision.

### CHG-055 — DL-048 Ratified (Cost Governance / Freemium Unit Economics — Tier-1 Token-Cost Enforcement)

- **Date:** 2026-06-05
- **Authorizing Decision:** DL-048.
- **Affected Artifacts:** `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md`, `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE.md`, `WAVE_I_CONTRACT_PACKAGE_INTERACTION_COLLABORATION.md` (DL-048 Additions — cost-governance obligation, QA negatives, `AI Spend Recorded` event); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (new §4c tier-keyed cost config, Balanced ~$3/mo Free defaults); `02_product/specs/data_api_nfr/RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` (§12 Cost Constraints → ratified enforcement gate referencing DL-048); `OPEN_TBD_REGISTER.md` (A6 → DL-048 proposed defaults; paid-tier limits remain TBD); `RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` (new MON-COST cognitive-enforcement row); `WAVE_CONTRACT_PACKAGES_CONFORMANCE_REVIEW_001.md` (re-checked — CONFORMANT); `decision_log.md` (DL-048 entry; operative range → DL-029–DL-048); the DL-048 disposition draft flipped to Ratified.
- **Change Summary:** Repository owner ratified DL-048, making **tier-1 freemium unit economics (token-cost management) an enforced, tested, and observable Release 1 criterion** rather than a soft NFR principle plus commodity billing. The decision **separates the cap value from the enforcement mechanism**: cap values are tier-keyed, owner-set, env-bound **configuration** (Calibration Defaults §4c; tracked in the Open-TBD Register), while the **enforcement** is a **contracted cost-governance obligation on the Fast/Deep analysis engine** (Wave B Infer/Evaluate + Wave S Synthesis, chat/fix caps in Wave I) — every run operates within a per-tier token budget read from config; per-run over-budget triggers **graceful degradation** (Fast truncates, Deep coalesces/defers) and per-user daily/monthly over-budget **gates** further AI spend, with **tier-keyed model routing** (free → cheap class) as the primary cost lever. A **QA acceptance gate** asserts free-tier runs stay within budget on envelope fixtures, with negative tests rejecting budget bypass, runaway re-analysis, silent overspend, and wrong-tier routing; a new **`AI Spend Recorded`** observability event emits tokens + estimated cost per run/user/tier/mode/model with an over-budget trust signal. The owner selected the **Balanced (~$3/active-free-user/month)** posture; the starting Free/Tier-1 defaults (1 active project; nano-extraction/mini-synthesis routing with Haiku fallback; Fast per-run cap 150k, Deep per-run cap 600k; Deep 2/day single-active + coalescing; 5 fixes/day; 20 chats/day; 500k daily / 4M monthly token budget; ~$3 monthly alert ceiling) were adopted into Calibration Defaults §4c, reconciled against verified June 2026 token pricing (4M tok/mo ≈ $3.04 worst-case). No new responsibility or object is introduced; all DL-043 epistemic invariants are preserved; MON-01…04 remain commodity billing consuming the same tier config. Paid-tier limits remain an explicit open scope item. No Doctrine, Constitution, or architecture change.
- **Supersession Reference:** None. Amends (adds to) the DL-044-approved Wave B and DL-047 Wave S/I contracts; supersedes no Decision.

### CHG-056 — Tier-1 Fast-Pass Envelope Confirmed (Calibration config; Open-TBD A1)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction under DL-044 (Calibration Defaults are tunable operative configuration); scopes the DL-046 <60s gate and the DL-048 Tier-1 cost math. No new Decision required (config confirmation, no contract/architecture change).
- **Affected Artifacts:** `OPEN_TBD_REGISTER.md` (A1 → Tier-1 owner-confirmed; tier-keyed; paid-tier envelopes TBD via E3); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4b envelope marked Tier-1 owner-confirmed + tier-keyed).
- **Change Summary:** The repository owner confirmed the **Free / Tier-1** Fast-Pass project-size envelope at **~20 artifacts / ~50,000 words / 1 active project** (the single highest-priority open owner decision, Open-TBD A1), scoped explicitly to **tier-1 (free) use**. This is the **guaranteed Tier-1 envelope** within which the ratified <60s Time-to-First-MRI gate (DL-046) and the DL-048 ~$3/mo Tier-1 unit-economics math hold; projects larger than the envelope are **not rejected** but degrade gracefully (partial orientation within budget + coalesced Deep Pass). The envelope is recorded as a **tier-keyed dimension** alongside the §4c cost caps and model routing; **paid-tier envelopes remain TBD** (parameterize as config rows, Open-TBD A1/E3), and the Tier-1 figure is to be **re-confirmed against measured Fast-Pass latency post-build (Phase III)**. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Resolves (for Tier-1) the A1 placeholder; supersedes no Decision.

### CHG-057 — Tier-2 (Basic) Subscription Tier Confirmed + Canonical Tier Taxonomy Recorded

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction under DL-044 (Calibration Defaults are tunable operative configuration) + DL-048 (tier-keyed cost governance). Config confirmation + canonical terminology record; no new Decision required (no contract/architecture change).
- **Affected Artifacts:** `CANONICAL_GLOSSARY.md` (canonical subscription-tier taxonomy added: Tier 1 Free · 2 Basic · 3 Pro · 4 Team · 5 Enterprise, with banned synonyms; `tier` as config/telemetry key); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4c — Tier-2 Basic config rows, owner-confirmed); `01_governance/backlog/BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md` (5-tier ladder; T1/T2 marked confirmed); `OPEN_TBD_REGISTER.md` (E3 → Tiers 3–5 remaining).
- **Change Summary:** The repository owner set the **canonical five-tier subscription taxonomy — Tier 1 Free · Tier 2 Basic · Tier 3 Pro · Tier 4 Team · Tier 5 Enterprise** (recorded in the glossary with banned synonyms to prevent drift) and **confirmed Tier-2 (Basic)** as the first paid step at **$12/mo**. Basic differentiates on **capacity, not model quality** (routing stays cheap-class; full-quality routing is the Tier-3 Pro upsell, protecting Basic's margin and the Pro differentiator): **3 active projects, ~40 docs / ~100k-word envelope, Deep 6/day, 20 fixes / 75 chats per day, 1.5M daily / 10M monthly token budget**, with the monthly token budget as the binding cost governor (~12 Deep or ~80 Fast passes/mo across 3 projects). Worst-case cost ≈ **$7.90/mo** (≈$2 at typical 25% utilization), giving ~34% worst-case / ~84% typical gross margin at the $12 price. Tiers 3–5 remain owner-decision (Open-TBD E3); enforcement is tier-parameterized so they are added as config rows, not code. All values are estimate-based starting defaults to be re-tuned from the contracted `AI Spend Recorded` telemetry. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Resolves the Tier-2 portion of Open-TBD E3; supersedes no Decision.

### CHG-058 — Freemium Upgrade-Prompt Timing Audit Applied (MON-04 trigger taxonomy + criteria)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (applied `FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001`). Config + product-spec definition + one clarifying Wave E note; no new Decision required (MON-04 is commodity; the one contracted touch is an epistemic-safety clarification already implied by DL-046/047/048).
- **Affected Artifacts:** `02_product/tiering/12_freemium_tier_behavior_logic.md` (Upgrade-Prompt two-class model + UP-1…8 trigger taxonomy + global guards + optimality objective; tier-name drift fixed Professional→Pro, Business→Team, Enterprise headers numbered); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (new §4d Tier-1 Upgrade-Prompt timing config — cooldowns, per-day cap, guards, auto-suppress threshold); `03_architecture/contracts/WAVE_E_CONTRACT_PACKAGES_DISCLOSE_SURFACES.md` (honest-limit disclosure = UP-4 surface; QA negative); `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (MON-04 note → trigger taxonomy + timing references); `02_product/tiering/FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001.md` (status → APPLIED).
- **Change Summary:** Applied the owner-directed upgrade-prompt timing audit, which found MON-04 Upgrade Prompts defined in principle but **not by trigger/timing criteria.** Defines a **two-class trigger model** (value-moment vs friction-moment) and an enumerated **trigger taxonomy (UP-1…UP-8)** mapping each Tier-1 constraint/value event — daily fix/chat caps, 2nd-project intent, envelope-exceeded partial orientation, Deep/day cap, monthly budget gate, confidence-improved value peak, first-MRI activation — to a value-framed, tier-specific prompt and a timing rule. Friction triggers **consume the DL-048 constraint-detection signals**; **UP-4 is unified with the Wave E honest-limit (partial-analysis) disclosure as one surface** (epistemic-safety first, the upgrade affordance rendered alongside — never instead-of), with a QA negative against presenting a scope/budget-limited result as complete. Timing **numbers** (≤2 prompts/day, 24h cooldowns, ≥7-day value-trigger cooldown, first-value + no-interrupt guards, dismiss>60%/convert<2% auto-suppress) are added as **tunable Calibration §4d config**, tuned via TEL-07 against an explicit optimality objective (maximize conversion, bound annoyance). Canonical tier-name drift in the freemium spec corrected to Pro/Team. Now concrete because CHG-057 gives prompts a defined Basic target. No Doctrine, Constitution, or architecture change.
- **Supersession Reference:** None. Specifies the timing of MON-04 (commodity); adds one clarifying Wave E epistemic-safety note; supersedes no Decision.

### CHG-059 — Internal Test-Bypass Entitlement (designated accounts bypass Free-tier constraints)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (recorded as a Proposed backlog item; commodity MON/SEC config + capability — no DL required). Builds on DL-048 tier-keyed cost governance.
- **Affected Artifacts:** `01_governance/backlog/BACKLOG_INTERNAL_TEST_BYPASS_ENTITLEMENT.md` (new — design + grant controls + QA); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4c — Internal non-consumer entitlement row); `CANONICAL_GLOSSARY.md` (Internal recorded as a non-consumer entitlement, not part of the 1–5 ladder, with banned synonyms).
- **Change Summary:** Recorded how to accommodate a system flag letting **designated test accounts bypass Free-tier constraints**: model it as a **non-consumer `Internal` entitlement** — a tier-keyed config row with **unlimited caps** that the existing **contracted DL-048 enforcement reads** — rather than a divergent `if (isInternal) skipChecks()` code path. This keeps the change entirely in the **commodity monetization/security layer** with **no impact on cognition or any epistemic invariant** (an Internal account gets the identical analysis, Attested/Derived handling, and recompute discipline; only its quota differs). Mandatory controls: grant is **server-side, admin-only, allowlisted, audited (SEC-06), default-off, staging/test-only by default** (production-allowed only with monitoring + time-box, owner's choice), and **not self-grantable**. The bypass lifts the **limit but not the `AI Spend Recorded` telemetry**, and Internal accounts are **excluded from TEL-07 conversion metrics + unit-economics medians** and have **Upgrade Prompts suppressed**, so test traffic cannot skew tuning or cost data. Seven-point QA acceptance defined. Owner choices (model: Internal tier vs override attribute; environment scope) remain open in the backlog. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. New commodity entitlement; supersedes no Decision.

### CHG-060 — DL-049 Ratified (External-Stakeholder / Reviewer Identity + Reviewer→User Promotion)

- **Date:** 2026-06-05
- **Authorizing Decision:** DL-049.
- **Affected Artifacts:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` (DL-049 Object Additions — `Principal` with `type: reviewer | user`; `StakeholderResponse` author = Principal; promotion semantics); `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (gap #337 → RESOLVED); `03_architecture/contracts/WAVE_I_CONTRACT_PACKAGE_INTERACTION_COLLABORATION.md` (DL-049 note: response author = Principal, promotion does not re-attribute); `01_governance/decisions/decision_log.md` (DL-049 entry; operative range → DL-029–DL-049); `01_governance/decisions/PROPOSAL_EXTERNAL_STAKEHOLDER_REVIEWER_IDENTITY_DL049_DISPOSITION.md` (→ Ratified); `01_governance/backlog/BACKLOG_EXTERNAL_STAKEHOLDER_EXPERIENCE.md` + `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md` (status → identity model ratified).
- **Change Summary:** Owner ratified DL-049, resolving Capability-Matrix gap #337 by introducing a **single `Principal` identity object** with a **`type: reviewer | user`** capability attribute (Option A from the virality-audit P0 scoping). A **Reviewer** is a lightweight, email-verified principal scoped to shared items (CRR finding / MRI) that may view + respond but owns no Workspace/projects; a **User** is the same principal plus a Workspace/Account, projects, and a tier (default Free). **Reviewer→User conversion is an in-place state transition** — flip `type`, provision a Workspace, assign Free tier — on the **same `Principal` ID**, *not* a data migration, which keeps provenance stable: prior `StakeholderResponse` attribution is **immutable** (append-only, never re-keyed), response remains **evidence not truth**, scope to the inviter's project is **never widened** on promotion (account-type ≠ share-scope), and the promotion is **audited** (SEC-06). The contracted CRR response→evidence→Deep-Pass seam (Wave A/I) is **preserved, not redefined** — its author is simply a `Principal` of `type = reviewer`; reviewer-driven recompute stays **DL-048-bounded**. Edge cases (different-email later signup = new principal with optional deferred linking; email de-dup; non-converting reviewers; default Free tier on promotion) are recorded. The **commodity recipient UI / convert-moment / link-security (#339)** and the **R1-vs-fast-follow** scope call remain owner-open follow-ups. No Doctrine or Constitution change; introduces the `Principal` identity object additively, preserving all DL-043 epistemic invariants.
- **Supersession Reference:** None. Additive identity object; supersedes no Decision.

### CHG-061 — Virality Amplifiers P1–P3 Applied (attribution/CTA · viral primitives on Free · share-prompt timing)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (applied P1–P3 of `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001`). Commodity (SHARE/MON/SEC) config + product-spec definition; no DL required; reuses the upgrade-prompt timing pattern.
- **Affected Artifacts:** `02_product/tiering/12_freemium_tier_behavior_logic.md` (viral primitives guaranteed on Free incl. limited CRR; viral-surface attribution+CTA; Share/Invite prompt SP-1…4 timing); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4e share-prompt timing config); `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (SHARE-02/04 + CRR-01 notes); `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md` (P1–P3 status).
- **Change Summary:** Applied the value-aligned, no-dependency virality amplifiers. **P2 — viral primitives guaranteed on Free:** MRI share links, PDF export, comments, and **CRR (limited, cost-governed under DL-048)** are explicit Free-tier capabilities — the loop seeds on Free; monetize depth/capacity, never the seed. **P1 — artifact attribution:** PDF exports and shared MRI links carry tasteful, honest **"Made with OSLO — map your own project's understanding" attribution + CTA** (the cheapest i×c lever; not a misleading watermark). **P3 — share/invite prompt timing:** a value-moment two-class trigger set (SP-1 strong/first MRI, SP-2 invite-a-stakeholder on a finding, SP-3 confidence/milestone, SP-4 post-export) reusing the upgrade-prompt guards, with timing numbers as tunable Calibration §4e config, foregrounding SP-2 because a stakeholder response becomes evidence (value = virality). All bound by the value-alignment guardrails (user-initiated, no autonomous sends, no dark patterns) and tuned via TEL-06. P0 (DL-049) prior; P5 (referral) and the recipient-experience R1-vs-fast-follow remain owner-open. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Commodity product/config specification; supersedes no Decision.

### CHG-062 — Virality P6 Applied (k-factor instrumentation)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (applied P6 of `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001`). Commodity (TEL) measurement definition + config; no DL.
- **Affected Artifacts:** `02_product/tiering/12_freemium_tier_behavior_logic.md` ("Virality measurement — k-factor" definition); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4f virality/k-factor targets); `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (TEL-06 note); `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md` (P6 status).
- **Change Summary:** Defined virality as a tracked objective. **k = i × c** (exposures-per-active-user × conversion-to-activation; k > 1 self-sustaining) is computed from TEL-06 + TEL-02 **per loop** (active CRR / passive MRI-share / portable PDF), with **cycle-time T** per loop, **Internal accounts excluded** (CHG-059, so test traffic can't inflate k). Measurement window, k target, conversion-attribution window, and decline alert are tunable **Calibration §4f** config — with the **k target deliberately track-only until a measured baseline exists** (set from data, not guessed). A virality dashboard (k/i/c/T per loop, segmented) is the natural surface. This is the objective function the other virality optimizations (P1–P5) tune against; pure measurement, no cognition. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Commodity measurement specification; supersedes no Decision.

### CHG-063 — Virality P7 Applied (share-link hygiene; gap #339 addressed) + P5 referral drafted

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (applied P7; drafted P5 of `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001`). Commodity (SEC/SHARE/MON); no DL.
- **Affected Artifacts:** `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (gap #339 share-link security → addressed; SHARE-05 note); `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4g share-link hygiene); `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md` (P7 status); `01_governance/backlog/BACKLOG_REFERRAL_REWARD.md` (new — P5 draft).
- **Change Summary:** **P7 applied** — share links (SHARE-02/03/04) are now specified as **read-only by default, scoped to the shared item only** (no project access, mirroring DL-049's scope-not-widened guard), **owner-revocable any time**, with a **default 90-day expiry** (tunable, Calibration §4g); private links require an authenticated `Principal` (DL-049), public links are unauthenticated read-only carrying the P1 attribution+CTA. This closes Matrix gap #339 and lets the passive loop (MRI links) spread without becoming a data-leak surface; SEC-audited. **P5 referral reward drafted** (`BACKLOG_REFERRAL_REWARD`, Proposed) — a bounded, conversion-credited capacity bump for inviting users who join, designed defensively (finite tier-keyed config from a bounded pool, monthly per-user cap, DL-048-bounded, email de-dup + velocity + fraud guards, Internal accounts excluded, value-aligned), with ROI folded into the P6 k-factor metric; its **in/out-of-R1 decision and reward values are routed to the owner.** No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Commodity spec + a proposed backlog draft; supersedes no Decision.

### CHG-064 — Recipient Experience scoped to Release 2 (DL-049 separable scope call resolved)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (resolves the DL-049 separable scope call). Scope decision; no contract/architecture change.
- **Affected Artifacts:** `PROPOSAL_EXTERNAL_STAKEHOLDER_REVIEWER_IDENTITY_DL049_DISPOSITION.md` + `decision_log.md` (DL-049 separable scope call → resolved, R2); `BACKLOG_EXTERNAL_STAKEHOLDER_EXPERIENCE.md` (recipient build → R2); `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001.md` (scope outcome); `BACKLOG_REFERRAL_REWARD.md` (P5 → R2); `OSLO_CAPABILITY_MATRIX_V2.md` (gap #337 note).
- **Change Summary:** The owner resolved the DL-049 separable scope call: **Release 1 is the owner's own test/validation vehicle** (bottleneck = proving the product, not acquiring users), so the **external-stakeholder recipient experience is fast-follow → Release 2.** R1 ships the **invitation-generation + measurement** side (CRR/MRI/PDF sharing, attribution+CTA P1, viral primitives on Free P2, share-prompt timing P3, k-factor instrumentation P6, link hygiene P7) and the **ratified identity model (DL-049 `Principal`)**, so the loop is instrumented and ready; **Release 2** builds the recipient UI + external auth + reviewer→user promotion + convert-moment, plus the **P5 referral reward** (which credits on join and therefore depends on the R2 recipient experience), all tuned against R1's real funnel data. The identity model is unchanged — zero rework, clean drop-in. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Scope decision; supersedes no Decision.

### CHG-065 — Second-Project Attempt → Upgrade-Trigger Path Specified (UP-3 precondition)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (close an under-specified UX moment). Commodity (MON/UX) interaction clarification; no DL.
- **Affected Artifacts:** `02_product/tiering/12_freemium_tier_behavior_logic.md` (UP-3 precondition); `02_product/specs/ux/PROJECT_DASHBOARD_AND_PROJECT_LIST_EXPERIENCE_SPECIFICATION_V1.md` (§D active-project-limit behavior); `02_product/specs/ux/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` (§I); `02_product/specs/planning/OSLO_CAPABILITY_MATRIX_V2.md` (PF-03 note).
- **Change Summary:** Closed an under-specified gap between the API and the UX: the `422` free-tier active-project limit (API) and the UP-3 upgrade trigger (freemium behavior) both existed, but no UX spec stated what a Free user sees when they try to add a second project. Specified the **attempt→trigger path**: the **Create Project affordance stays enabled at the active-project cap** (Free = 1 *active* project; archiving is reversible and frees the slot, so the limit is on the active set, not lifetime count); a Free user may **attempt** a second active project; the attempt is **gated server-side (`POST /projects` → `422`)** and surfaces **UP-3 with two resolutions — upgrade, or archive the current project.** The control is **never disabled or hidden** at the limit (which would suppress the highest-intent upgrade trigger). Kept as presentation/interaction (limit values per Tier Definitions, presented not computed) — no governance, no computation in the UX surfaces. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Interaction clarification; supersedes no Decision.

### CHG-066 — Cross-Layer Seam Audit 001 Applied (shared limit-reached interaction rule)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (broader audit prompted by CHG-065; applied `RELEASE_1_CROSS_LAYER_SEAM_AUDIT_001`). Commodity (MON/UX) interaction clarification; no DL.
- **Affected Artifacts:** `02_product/tiering/12_freemium_tier_behavior_logic.md` (shared **limit-reached interaction rule** + cap→affordance→gate→prompt→resolution table); `02_product/specs/ux/RECOMMENDATION_PANEL_SPECIFICATION_V1.md`, `…/OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md`, `…/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` (limit-reached pointers); `OSLO_CAPABILITY_MATRIX_V2.md` (MON-02/MON-03 notes; gap #5 reconciled as stale — S4); `RELEASE_1_CROSS_LAYER_SEAM_AUDIT_001.md` (status → APPLIED).
- **Change Summary:** Generalized the CHG-065 second-project fix into a **shared "limit-reached interaction" rule** covering **all** monetization caps (S1–S3): the daily **fix cap** (UP-1, Recommendation/Issue/Artifact surfaces), daily **chat cap** (UP-2, OSLO Chat), and **deep-runs/budget caps** (UP-5/UP-6, Project Overview). The rule: every limit-bearing affordance **stays enabled**, the attempt is **gated server-side** (`429`/`422` + `Retry-After`), and the surface presents the **matching UP prompt + resolution(s)** — **never** disabled/hidden (which would suppress the upgrade trigger) and **never** a raw error. Specified once in the freemium behavior spec (with a cap→surface→gate→prompt→resolution table) and pointed to from each UX surface + matrix anchors, mirroring how UP-1…8 share their §4d/§4e timing config. **S4:** reconciled the stale Matrix gap #5 — the Notification & Awareness surface spec exists (the gap predated it); flagged confirming the reviewer/comment/mention → notification wiring. **S5** (multi-user edit-conflict handling) recorded for R2 Team (low R1 risk — single-user validation release); **S6** (explicit UI guard against rendering Confidence as a probability) flagged for the epistemic-safety presentation rules. Kept presentation/interaction only (values per Tier Definitions, presented not computed); no governance/computation in the surfaces. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Interaction clarification + a stale-gap reconcile; supersedes no Decision.

### CHG-067 — Visual Design & Branding Spec (token contract) + brand registered as owner-TBD

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (the corpus deliberately defers visual styling; owner chose clean-default-now / designer-delivers brand). Commodity presentation/Render layer; no DL.
- **Affected Artifacts:** `02_product/specs/ux/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` (new); `OPEN_TBD_REGISTER.md` (E4 visual branding = escalate-not-invent; E2 accessibility → proposed WCAG AA).
- **Change Summary:** Filled the deliberate visual/brand gap with a **design-token contract** as the designer↔code seam: all color/type/spacing/radius/motion are tokens (Tailwind + shadcn/ui), so R1 builds to a clean accessible default now and the designer's brand applies later as a **single token-swap**, guaranteed total by a **token-adherence lint** (no hardcoded brand). Encodes OSLO-specific epistemic constraints on the visuals (Confidence/CAF as a neutral **maturity** ramp, **never** a red/green health palette — protects the no-fabricated-health fail-conditions + S6; honest, no-dark-pattern microcopy), a WCAG 2.1 AA baseline, a designer-input checklist mapping 1:1 to the tokens, and a two-track verification process (behavioral conformance from each UX spec's fail-conditions, runnable now; visual conformance — token lint + Storybook + visual-regression + Figma diff — when the brand lands). Interim palette seeded from **intralign.ai** (exact hexes TBD — client-rendered site; not fabricated). **Visual branding registered as Open-TBD E4 (escalate, don't invent)** per the Anti-Assumption Protocol. R1 is the owner's validation vehicle → clean default sufficient, brand is a fast-follow. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. New commodity presentation spec; supersedes no Decision.

### CHG-068 — Canonical Intralign Brand Palette Formalized

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner direction (provided the formalized Intralign palette). Commodity presentation; no DL.
- **Affected Artifacts:** `02_product/specs/ux/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` (§1.1 color tokens set to the canonical palette; §1.2 confidence ramp aligned; AA accent note); `OPEN_TBD_REGISTER.md` (E4 → palette formalized).
- **Change Summary:** The owner formalized the canonical **Intralign brand palette** — core: **Charcoal Black `#111315`, Warm White `#F5F4F0`, Intralign Orange `#D97A3A`** (dark-theme-primary; strategic/executive/AI-native/premium, deliberately not blue/purple), with the supporting UI ramp (graphite surfaces, soft/cool-gray text, slate borders, muted green/amber/red system states). Wired into the §1.1 design tokens, replacing the interim placeholders. The **Confidence/CAF maturity ramp** was set to a neutral **gray→warm-white** scale (Cool-Gray → Soft-Gray → Warm-White = understanding clarifying), explicitly **never** a red/green health palette and **not** using the orange action-accent — protecting the no-fabricated-health fail-conditions + confidence≠probability guard (S6). Captured the AA contrast detail (charcoal-on-orange 4.8:1 passes; white-on-orange large/bold only). Type/spacing/logo/microcopy remain designer-pending (Open-TBD E4); the token contract + lint keep everything swappable. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. Fills the CHG-067 interim palette with canonical values; supersedes no Decision.

### CHG-069 — Knowledge Integrity Audit (KIA) 001 produced (permanent governance artifact)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner-directed independent audit. Findings + backlog; no canonical content changed (audit is read-only over the corpus).
- **Affected Artifacts:** `01_governance/audits/OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001.md` (new — permanent governance artifact).
- **Change Summary:** Produced an independent **Knowledge Integrity Audit** evaluating the repository as a knowledge system (not code) against the core question — can a new Claude Code instance reconstruct + continue OSLO without material interpretation drift. **Verdict: qualified YES** (Overall Knowledge Health **79/100**) — the cognitive-spine/contract/governance core is purpose-built against drift (Anti-Assumption Protocol, Glossary, Traceability Matrix, Wave contracts, append-only ledger) and scores high-80s–low-90s; material risk concentrates in **addressable knowledge-surface defects**, not architecture. Includes 11 domain scorecards (6 dimensions each), a canonical-concept coverage matrix, a knowledge dependency graph (Vision + Outcome Management flagged orphaned), the top-25 interpretation-drift risks, conflict/discoverability/missing-knowledge reports, a 4-persona readiness assessment, and an 11-item prioritized **governance backlog (KIA-1…11)**. **NOT DISCOVERABLE** flagged for Product Vision/positioning, Intralign mission, and "Outcome Management". Highest-leverage fixes: **KIA-1** refresh stale `START_HERE` (hides DL-046–049 + recent specs), **KIA-2** author canonical Vision, **KIA-6** add a repository concept index — together ~+9 health points. No Doctrine, Constitution, contract, or architecture change.
- **Supersession Reference:** None. New governance artifact; supersedes no Decision.

### CHG-070 — KIA Governance Backlog Applied (knowledge-surface fixes, KIA-1/3/5/6/7/8/9/10)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner-directed (execute the Claude-ownable KIA-001 backlog). Documentation/discoverability fixes; no Doctrine/Constitution/contract/architecture change.
- **Affected Artifacts:** `START_HERE.md` (KIA-1/7 — surfaces DL-046–049 + telemetry/visual specs; DL-036 dual-definition rule; ledger-wins note); `README.md` (KIA-8 — telemetry/visual/index links; cognitive-spine framing; fixed deprecated "judgement/governance layer" wording); `REPOSITORY_INDEX.md` (KIA-6 — new concept→canonical-file map); `03_architecture/legacy_layer_engineering/README.md` (KIA-3 — "DO NOT BUILD FROM THESE" banner); `RELEASE_1_DATA_MODEL_SPECIFICATION_V1/.1/.2` (KIA-5 — v1.2 confirmed canonical, v1+v1.1 bannered superseded); `REPOSITORY_ARCHITECTURE.md` (KIA-9 — canonical-architecture precedence section); `01_governance/audits/OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001.md` (execution status).
- **Change Summary:** Executed the highest-leverage knowledge-surface fixes from the Knowledge Integrity Audit. **The headline fix (KIA-1):** `START_HERE.md` — whose curated "read 6 docs" path lagged the ledger — now surfaces the operative decisions ratified since DL-044 (DL-046 Fast/Deep+60s, DL-047 synthesis/Chat/CRR, DL-048 cost governance, DL-049 Principal identity) plus the telemetry/economics + visual/brand specs, the DL-036 dual-canonical-definitions rule, and an explicit "the ledger wins over any summary" note. **KIA-6:** a new root `REPOSITORY_INDEX.md` maps every major concept to its canonical file (with NOT-DISCOVERABLE flags for Vision and Outcome Management). **KIA-3:** the `legacy_layer_engineering/` README now carries a prominent DO-NOT-BUILD banner (cognitive spine is canonical; layer names are deprecated). **KIA-5:** the data-model version conflict (v1, v1.1, **and** v1.2 all claiming "authoritative") is resolved — v1.2 confirmed canonical, v1/v1.1 bannered superseded. **KIA-8/9:** README links the telemetry + visual specs and the index (and its deprecated "judgement/governance layer" wording is corrected to the spine); `REPOSITORY_ARCHITECTURE.md` states the canonical-architecture precedence (Cognitive Responsibility Spec > baseline > legacy > not-applied proposals). These convert the audit's largest latent discoverability + drift risks into resolved. **Owner-gated remain:** KIA-2 (canonical Product Vision), KIA-4 (define/retire "Outcome Management"), KIA-11 (CAF/Confidence formula). No canonical model content changed.
- **Supersession Reference:** None. Discoverability/clarity fixes; supersedes no Decision (data-model v1/v1.1 marked historical in favor of the already-current v1.2).

### CHG-071 — KIA-2 Vision skeleton drafted + KIA-4 Outcome-Management resolution proposed (owner-gated)

- **Date:** 2026-06-05
- **Authorizing Decision:** Owner-directed (advance the owner-gated KIA items to owner-ready drafts). No canon changed (both are drafts pending owner input/ratification).
- **Affected Artifacts:** `02_product/specs/planning/OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md` (new — DRAFT Vision skeleton); `01_governance/decisions/PROPOSAL_OUTCOME_MANAGEMENT_RESOLUTION_DL050_DISPOSITION.md` (new — DL-050 draft); `REPOSITORY_INDEX.md` + `OSLO_KNOWLEDGE_INTEGRITY_AUDIT_001.md` (status pointers).
- **Change Summary:** Advanced the two owner-gated KIA items to owner-ready state without inventing strategy or ontology. **KIA-2:** a canonical **Product Vision & Positioning** skeleton — grounded sections filled from existing canon (foundational thesis DL-001, outcome-integrity DL-002, the epistemic-honesty differentiator, R1-as-validation, the Curiosity→Trust→Habit→Conversion model, and the high-confidence non-goals) and cited, with the genuinely strategic fields (Intralign mission, aspirational end-state, category name + competitive set, ICP, value-prop wording, strategic-objective ladder, positioning statement) marked **`[OWNER TO COMPLETE]`** and deliberately not invented (Anti-Assumption Protocol). **KIA-4:** a **DL-050 draft** resolving "Outcome Management" (NOT DISCOVERABLE / undefined) — routes the canon decision to the owner with two options (define as a distinct concept; or — recommended — **retire & map** to the defined Outcome Integrity/Orchestration with a glossary ban), recommending retirement because the term is undefined/unused and "management" connotes acting-on/controlling outcomes, conflicting with OSLO's advise-never-act posture. Index + KIA status updated (Vision ⚠ skeleton; Outcome Management ⚠ proposed). Owner-gated remaining: KIA-2 completion, KIA-4 ratification, KIA-11. No Doctrine/Constitution/contract/architecture change.
- **Supersession Reference:** None. Owner-ready drafts; supersede no Decision.

### CHG-072 — Product Vision & Positioning completed + adopted (KIA-2 closed)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner Decision Responses Q1–Q9.
- **Affected Artifacts:** `02_product/specs/planning/OSLO_PRODUCT_VISION_AND_POSITIONING_V1.md` (DRAFT skeleton → owner-completed & adopted canonical); `REPOSITORY_INDEX.md`; KIA-2 closed.
- **Change Summary:** The owner completed and adopted the canonical Product Vision & Positioning. **Intralign mission:** build AI-native systems for better outcomes via governed planning/execution/orchestration. **OSLO vision:** the **system of record for outcome integrity** — the governance/orchestration layer above human + AI execution. **Category: create a new one — Outcome Orchestration** (secondary: AI-Native Planning Intelligence + Outcome Governance), wedge = 60-second project intelligence + governed planning QA, entering via planning intelligence and expanding to execution intelligence + outcome orchestration; competitive set = Jira/Asana/Monday/Smartsheet/MS Project/Planview/Primavera/AI planning copilots. **ICP** = anyone responsible for project outcomes (beachhead PM/PgM/PMO/coordinators/delivery/transformation; mid-market+enterprise), bought on outcome responsibility not title. Includes per-persona value, a 7-level strategic ladder (individual outcomes → … → Outcome Orchestration as a discipline), the moat, the non-goals (incl. "not a work-coordination tool"), and the positioning statement. Resolves the KIA NOT-DISCOVERABLE Vision finding; becomes the canonical strategic anchor. No Doctrine/Constitution/architecture change.
- **Supersession Reference:** None.

### CHG-073 — DL-050 Ratified ("Outcome Management" retired → Outcome Orchestration; KIA-4 closed)

- **Date:** 2026-06-05 · **Authorizing Decision:** DL-050 (owner Q10 = Option B).
- **Affected Artifacts:** `decision_log.md` (DL-050; range → DL-029–DL-050); `PROPOSAL_OUTCOME_MANAGEMENT_RESOLUTION_DL050_DISPOSITION.md` (→ Ratified); `CANONICAL_GLOSSARY.md` (outcome-family section + banned synonym); `REPOSITORY_INDEX.md`.
- **Change Summary:** Owner ratified **Option B** — **"Outcome Management" is retired** as a primary concept (it was undefined/unused and "management" connotes acting-on/coordinating work, conflicting with OSLO's advise-never-act posture). **Outcome Orchestration is the discipline/category** (per the Vision, CHG-072); surviving references are historical and map into the Outcome Orchestration framework during reconciliation. Glossary records the banned synonym and the outcome-family (Orchestration / Integrity / Confidence). No model/contract/architecture change.
- **Supersession Reference:** None (term was never canonical).

### CHG-074 — Owner Decision Queue confirms applied (Q11, Q13–Q29)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner Decision Responses.
- **Affected Artifacts:** `OPEN_TBD_REGISTER.md` (owner-confirmation block; E1 evergreen; E2 WCAG 2.1 AA; new F1 CAF-formula-TBD); `02_product/specs/ux/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` (§3 AA owner-adopted); `OWNER_DECISION_QUEUE.md`; KIA-11 closed.
- **Change Summary:** Applied the owner's confirmations: **all proposed Open-TBD numeric defaults (Q17–Q27, Sections A–E) confirmed as R1 working values**, to be refined from telemetry (rationale: R1 = learning velocity; defaults hold unless implementation constraints emerge). **Accessibility = WCAG 2.1 AA adopted** (E2; Visual §3). **Browser = evergreen** (E1). **CAF/Confidence scoring formula marked TBD-by-design** (Q11=B; new Open-TBD **F1** — scaffold + calibrate from data, confidence stays maturity-not-probability; KIA-11 closed). **Paid tiers 3–5 / P5 referral / exec-monitoring confirmed R2; Free/Basic numbers held for telemetry** (Q13–Q16). **Q12 (DL-045)** remains pending owner review; **Q30 (brand type/logo/microcopy)** is designer-driven. No canonical model/contract/architecture change.
- **Supersession Reference:** None.

### CHG-075 — DL-045 Ratified (tool-neutral autonomous-agent terminology)

- **Date:** 2026-06-05 · **Authorizing Decision:** DL-045 (owner Q12).
- **Affected Artifacts:** `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md` (tool-neutral scope note); `01_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md` (§9 retitled "Autonomous coding agent at the Deployment Boundary" + generalized phrasing); `decision_log.md` (DL-045 entry recorded; governance note updated — DL-045 no longer pending); `PROPOSAL_TOOL_NEUTRAL_AGENT_TERMINOLOGY_DL045_DRAFT.md` (→ Ratified); `OWNER_DECISION_QUEUE.md` (Q12 resolved).
- **Change Summary:** Owner ratified DL-045, generalizing the governance naming from **"Claude Code"** to **"autonomous coding agent"** (Claude Code / OpenAI Codex / other AGENTS.md-aware agents interchangeable) so the standard reads accurately for any tool or a mixed-tool team. Applied as **scope notes** (filenames retained to avoid repo-wide reference churn) plus the Deployment Governance §9 retitle; `AGENTS.md` (root + starter-kit) is recorded as the tool-neutral twin of `CLAUDE.md`. **No rule, gate, epistemic invariant, STOP condition, readiness gate, or the human-only-production constraint changes** — the enforcement surface is tool-agnostic by design; only the noun is generalized. Runtime LLM routing (OpenAI primary / Anthropic fallback) is unrelated and untouched. This closes the last open item in `OWNER_DECISION_QUEUE.md` (Q12). No Doctrine/Constitution/contract/architecture change.
- **Supersession Reference:** None. Generalizes DL-044 naming.

### CHG-076 — Knowledge Integrity Audit (KIA) 002 — re-audit + path to upper-90s

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed re-audit.
- **Affected Artifacts:** `01_governance/audits/OSLO_KNOWLEDGE_INTEGRITY_AUDIT_002.md` (new).
- **Change Summary:** Re-audited the repository after the KIA-001 remediation + owner decisions. **Overall Knowledge Health 79 → 89 (+10)** — the largest latent risks (stale entry path, missing Vision, undefined Outcome Management, version conflicts, layer drift) are verified closed, with zero inbound references to the superseded telemetry spec. Finds the path from **89 to the upper-90s** is a different class of work: **KIA2-1** an automated doc-integrity CI (broken-link / superseded-reference / banned-synonym / stale-DL-range checks — the #1 lever, lifts the lagging Reliability dimension); **KIA2-2** archive the bannered-but-present legacy layer dirs + superseded data-model versions so the active tree is pure canon; **KIA2-3** consolidate the dual canonical-definitions surfaces; **KIA2-4** close the ~40% acceptance-criteria coverage gap; **KIA2-5** recognize intentional deferrals as integrity strengths, not defects. Projected ~96–97. Notes honestly that 96–97 is the appropriate target (a living, reasoned-in corpus should not chase 100) and that durable upper-90s comes from **permanent automated enforcement**, not more documentation. No canonical content changed (audit is read-only).
- **Supersession Reference:** None.

### CHG-077 — KIA2-1: Doc-Integrity CI built (mechanical knowledge-integrity gate)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (KIA-002 path to upper-90s; owner confirmed the CI is a read-only gate).
- **Affected Artifacts:** `tools/doc_integrity_check.py` (new); `.github/workflows/doc-integrity.yml` (new); `tools/README.md` (new); `OSLO_KNOWLEDGE_INTEGRITY_AUDIT_002.md` (KIA2-1 status).
- **Change Summary:** Built the KIA2-1 automated doc-integrity gate — the mechanical-enforcement lever KIA-002 identified as #1 for the upper-90s (it guards the lagging Reliability dimension). It is a **read-only verification gate**: runs autonomously on every push/PR (and locally), **detects** drift and reports pass/fail, and **never edits, auto-fixes, merges, or deploys** — preserving OSLO's never-autonomously-writes posture and human-only-production rule. Checks: **ERROR** (fails build) = broken internal doc links in the active tree (bare-filename-aware; reasoning/governance trail + prose/glob/shorthand exempt); **WARN** = active→superseded references, retired-terminology use (`Judgement Layer`/`Context Plane`/`Outcome Management`), and stale operative-DL-range claims. Tuned against the live repo to near-zero ERROR false-positives: current run = **0 errors (PASS), 248 warnings** — and those warnings are the KIA2-2 worklist the CI found automatically (18 active specs referencing the superseded data-model v1.1; 219 retired-layer-term uses concentrated in the baseline + Fast/Deep docs; 11 stale DL ranges). Flip CI to `--strict` once the warn backlog is cleared to lock the score. No canonical content changed (the tool reads, it does not write).
- **Supersession Reference:** None.

### CHG-078 — KIA2-2 + KIA2-3: residue archived (active tree = pure canon) + dual-definitions disambiguated

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (KIA-002 path to upper-90s).
- **Affected Artifacts:** **archived (git mv → `04_research/historical_artifacts/`):** `OSLO_ARCHITECTURE_BASELINE_V1.md`, `03_architecture/legacy_layer_engineering/` (whole dir), `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` + `…_V1.1.md`. **Repointed to data-model v1.2:** 13 active specs (data_api_nfr, testing, ux, Fast/Deep pack). **Disambiguated:** `01_governance/constitution/10_canonical_definitions.md` + `01_governance/canonical_definitions/canonical_definitions.md` (mutual cross-reference banners + DL-036 rule). `README.md` (operative DL range surfaced; stale-range line fixed). `tools/doc_integrity_check.py` (tuned: `raw/` excluded as source export; ledger files exempt from stale-DL).
- **Change Summary:** **KIA2-2** — archived the bannered-but-present historical residue so the **active tree is pure canon** (the DL-043 secondary baseline, the deprecated layer directories, and the superseded data-model v1/v1.1 now live under `historical_artifacts/`), and repointed the 13 active specs that referenced the superseded data model to **v1.2**. **KIA2-3** — the two canonical-definitions surfaces now each carry a banner naming the other and the DL-036 "Doctrine prevails" rule, so a reader needs no external knowledge to know which is authoritative for what (content-tier = operational expression; governance-tier = orientation registry). Net effect on the doc-integrity gate: **248 → 56 warnings, 0 errors (PASS)**; the residual ~56 are now mostly *legitimate* (a doc naming a retired term to deprecate/map it, or citing what it superseded), not drift. **Projected Knowledge Health ~94–95** (up from 89). Remaining to ~96–97: KIA2-4 (acceptance-criteria coverage) + optional inline-allow annotations to reach `--strict`. No canonical model/contract/architecture content changed — only relocation, reference-repointing, and disambiguation banners.
- **Supersession Reference:** None. Relocates already-superseded artifacts to their historical home.

### CHG-079 — KIA2-4 + KIA2-5: Acceptance-Criteria coverage reconciled (gap #11 closed)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (KIA-002 path to upper-90s).
- **Affected Artifacts:** `03_architecture/reviews/RELEASE_1_ACCEPTANCE_CRITERIA_COVERAGE_RECONCILIATION_001.md` (new); `OSLO_CAPABILITY_MATRIX_V2.md` (gap #11 → RECONCILED); `OSLO_KNOWLEDGE_INTEGRITY_AUDIT_002.md` (KIA2-4/5 status).
- **Change Summary:** Closed Capability-Matrix gap #11 (the "39 of 97 capabilities have no AC") by **reconciliation, not fabrication** (per the Anti-Assumption Protocol — AC is *located*, never invented). Demonstrated with evidence that the acceptance bases the original audit thought missing now exist: **cognitive** capabilities draw AC from the **Wave QA contracts** (`QA-WB/WC/WU/WE/WS/WI`) and the **Build/Test/Observe Traceability Matrix** (Test-basis column, 21 capability groups); the **Telemetry, Security, and Platform** categories the audit specifically flagged are covered by the Observability & Economics Platform spec, Deployment Governance, the Calibration/Environment profile, and this session's QA additions (DL-048 cost gate, Seam-Audit limit-reached, Internal-bypass) plus intentional commodity normal-engineering (DL-043 J). All 19 categories mapped to an acceptance basis; the **only genuinely-open AC is the CAF/Confidence numeric scoring formula** (intentionally TBD-by-design pending calibration, Open-TBD F1 — the structural AC is present). **KIA2-5** recorded as a standing principle: an intentional commodity non-contract is an **integrity strength, not an AC defect**, so counting it as a gap understates real coverage. **Projected Knowledge Health ~95–96 — upper-90s reached;** the full KIA2 path (1–5) is applied. No canonical model/contract/architecture content changed.
- **Supersession Reference:** None.

### CHG-080 — CAF/Confidence v0 scoring formula authored (closes the "no formula to test against" gap)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (owner refined Q11 — a default placeholder formula is needed for R1 build/test).
- **Affected Artifacts:** `02_product/specs/models/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (new); `OPEN_TBD_REGISTER.md` (F1 → v0 present); `RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4h v0 parameters); `03_architecture/reviews/RELEASE_1_ACCEPTANCE_CRITERIA_COVERAGE_RECONCILIATION_001.md` (residual updated).
- **Change Summary:** Corrected an over-rotation: the CAF/Confidence/Reliability v2 models deferred **all** scoring arithmetic to "future calibration," which would leave R1 with **no formula to compute or acceptance-test against** (the engine cannot produce the 0–100 confidence the MRI needs). Authored a **v0 provisional formula** that **provably satisfies the ratified doctrine** — per-dimension = `100 × Π(1 − impact_i)` (findings reduce via Impact-Assessment magnitude, **not** type), Outcome Confidence = a **symmetric power mean** of the co-equal dimensions (default geometric `p=0`, provably "between an average and a minimum," with a floor `ε` against weakest-link domination), **Reliability as a non-arithmetic qualifier** (high-confidence/low-reliability → false-confidence flag), banded per Calibration §2. It carries its own acceptance criteria (no-findings→100; material weakness felt; exact replay; negatives: no static weights / not simple-average / not weakest-link / reliability-not-arithmetic / not-probability). Parameters (`impact_i` table, `p`, `ε`) are tunable Calibration §4h, **calibrated from real data** — the v0 is what calibration refines, not a blank; the **canonical** formula remains owner-open (F1). This is the same track-and-tune discipline as the DL-048 cost defaults, Trust Index, and envelope, and closes the AC residual that earlier read "no formula to test against." No meaning redefined; no new dimension/finding/entity/probability/health concept; provisional and owner-ratifiable.
- **Supersession Reference:** None. Realizes the v2 models' deferred arithmetic as a v0; supersedes nothing.

### CHG-081 — CAF/Confidence v0 pressure-tested; default `p` revised 0 → −0.5

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (pressure-test the v0).
- **Affected Artifacts:** `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (§7 pressure-test findings; §2 default revised); `RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4h `p` default 0 → −0.5).
- **Change Summary:** Ran a reproducible pressure-test battery (dimension profiles × `p`, finding-stacking, monotonicity, edge cases). **Structure validated** — monotonic, saturating in [0,100], output always between the arithmetic mean and the minimum, ε-floor prevents weakest-link domination (true-zero dimension → Low ~37, not 0). **Two findings:** (1) geometric `p=0` is *lax* on a single severe weakness (`(85,85,20)`→52 Med; `(100,100,45)`→High), conflicting with OSLO's "surface over suppress" posture — **default revised to `p=−0.5`** (severe weakness → Low 46; moderate weakness stays High/Med edge; re-verified strictly between min and mean for all profiles); (2) small findings **compound** multiplicatively (10×minor → dim 43 Low) — flagged as a **calibration watch-item** for the `impact_i` magnitudes vs real finding-count distributions (structure unchanged). Both are calibration levers, not structural changes; the v0 remains owner-ratifiable and data-calibratable. No meaning/contract/architecture change.
- **Supersession Reference:** None.

### CHG-082 — Phase I Build Kickoff Packet (day-one onramp)

- **Date:** 2026-06-05 · **Authorizing Decision:** Owner-directed (begin the build).
- **Affected Artifacts:** `05_execution/implementation/Phase_I_Foundation_and_Environment/PHASE_1_BUILD_KICKOFF_PACKET.md` (new); `START_HERE.md` (§4 pointer).
- **Change Summary:** Produced the day-one build onramp that operationalizes the existing START_HERE + Onboarding Runbook into a single ordered Phase-I checklist for the developer + autonomous coding agent (Claude Code or Codex, DL-045). Confirms the build-ready state (cognitive spine, Wave contracts, traceability matrix, data-model v1.2, Calibration Defaults incl. the CAF/Confidence v0 formula, doc-integrity CI; knowledge health ~95–96), lists the owner-pending-but-non-blocking items to build around (canonical formula → v0; NFR numerics → confirmed defaults; brand → design tokens; paid tiers/recipient/referral/exec-monitoring → R2), and gives the ordered setup steps (read → clone → seed starter kit → `docker compose up` the five datastores → scaffold the cognitive-spine code-tree → wire-and-fail-test the CI gates → bind append-only schema → provision locked Staging/Production with OTel→Grafana), the first contract target (Wave A 00R) and build order, the per-increment build loop, the non-negotiable drift-control guardrails, the CI gates, and the exit-gate checklist to Phase II. Linked from START_HERE §4. No canonical content changed.
- **Supersession Reference:** None.

### CHG-083 — Environment Profile amended for the revised Phase 1 foundation binding (ENV-REV-001)

- **Date:** 2026-06-10 · **Authorizing Decision:** DL-054.
- **Affected Artifacts:** `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` (§2 Database Ownership Matrix, §5 LLM Provider Strategy, §7 Observability — each marked *Amended per DL-054*, plus a header amendment banner); `00_owner/decisions/decision_log.md` (DL-054 recorded).
- **Change Summary:** Enacted the DL-054 environment-binding revision (ENV-REV-001). **§2:** relational provider → **Supabase Postgres**; identity/authz → **Supabase Auth (GoTrue) + RLS** + app-level authorization; artifact bodies → **Supabase Storage**; snapshots/projections → Postgres **`jsonb`**; embeddings → **Supabase pgvector**; **MongoDB and Qdrant removed**; **Cognition History Records + User Acceptance Records** added as canonical append-only stores (DL-043 reconciliation §R2 enacted); Findings/Issues/Recommendations marked **Derived**. **§5:** provider abstraction realized as **Pydantic AI + OSS adapter** behind `/services/llm_provider`, with **workload routing / quotas / model-consumption auditability preserved** (condition 3); no `/authority` module. **§7:** **LangSmith added as a complement, not a replacement** to OpenTelemetry → Grafana (retained for service-health/queue-stream/retention); two-axis derivation replay + governed-output events + drift/trust remain **app-level**; **audit retention remains owner-pending (OPEN_TBD C1)** (condition 2). Platform architecture (DL-043) unchanged; conditions 1–4 apply. **Remaining DL-054 propagations (separate changes):** `RELEASE_1_LOGICAL_DATA_MODEL_V1.md` physical bindings (Mongo/Qdrant → Supabase Storage/pgvector); the non-canonical `ORIENT_PHASE` stage matrix; starter-kit templates (**blocked until the app repo exists**).
- **Supersession Reference:** None. Amends the owner-provided Runtime Environment Constraint Profile per DL-054; supersedes no prior Decision.

### CHG-084 — DL-054 follow-on propagations: Logical Data Model + ORIENT_PHASE store bindings

- **Date:** 2026-06-11 · **Authorizing Decision:** DL-054.
- **Affected Artifacts:** `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` (§6 physical-binding notes + scope line + summary); `90_research/design_artifacts/ORIENT_PHASE_FAST_PASS_WORKFLOW_DIAGRAMS.md` and its two HTML renders (stage-matrix store column + mermaid).
- **Change Summary:** Propagated the DL-054 storage binding into the remaining artifacts: **MongoDB → Supabase Storage** (artifact bodies/units), **Qdrant → Supabase pgvector** (embeddings), **PostgreSQL → Supabase Postgres** (+ Supabase Auth/RLS), CHR/MRI snapshots → Postgres `jsonb`. Historical "was MongoDB/Qdrant" notes retained for traceability. Logical model unchanged (no schema/DDL); ORIENT_PHASE is non-canonical orientation only.
- **Supersession Reference:** None. Completes the DL-054 propagation noted as pending in CHG-083.

### CHG-085 — DL-055: recommendation action/state reconciliation (Master Spec §8 ↔ State Model)

- **Date:** 2026-06-11 · **Authorizing Decision:** DL-055.
- **Affected Artifacts:** `10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` (§8 Recommendations actions + lifecycle pointer; §15 Flow 5; §16 Capability 8); `00_owner/decisions/decision_log.md` (DL-055 recorded).
- **Change Summary:** Made the **State Model §11** canonical for recommendation states. Master Spec §8 amended: state-changing actions = **Accept / Defer / Reject / Apply** (Apply = Implemented); **"Modify" removed** → editing supersedes the prior recommendation; **"Discuss" and "Share For Review" reclassified** as collaboration affordances; §8 now points to the State Model as the lifecycle authority. Consistency mentions in §15 Flow 5 and §16 Capability 8 aligned. Data Model v1.2 unchanged (already aligned).
- **Supersession Reference:** None. Reconciles §8 prose to the ratified State Model; supersedes no Decision.

### CHG-086 — DL-056: Template Intake (Start From Template in R1; Guided Intake → R2)

- **Date:** 2026-06-11 · **Authorizing Decision:** DL-056.
- **Affected Artifacts:** `10_product/experience/RELEASE_1_TEMPLATE_INTAKE_SPECIFICATION_V1.md` (new) + `10_product/experience/templates/` (five worked-sample bodies + README index, new); `10_product/experience/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` (§L + owner-defaults note + OB-C3 + deferred list + summary); `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md` (§22 #3 resolved / #4 → R2; EI-03 row); `00_owner/decisions/decision_log.md` (DL-056 recorded).
- **Change Summary:** Defined **Start From Template** for Release 1: selecting a template **instantiates a populated sample project** from a **fully worked fictitious sample plan** (one editable Artifact, `source="template"`, project flagged a **sample**), analyzed on the standard Fast Pass path → Project MRI in ~60s, then editable into the user's own project. **Owner-curated catalog of five** (Office Relocation, "Pulse" launch, "Brew & Co" campaign, "DevNorth 2026" event, EU expansion OKR); owner-curated only; `project_type` pre-filled, non-gating; **no system generation** — instantiation is copying static pre-authored content (OB-C3 preserved). **Guided Intake deferred to Release 2.** Reconciled Onboarding §L (templates Deferred → in scope) and Capability Matrix §22 (#3 resolved, #4 → R2). *(Note: the `Project.is_sample` flag is recorded as a build-detail in the spec; no Project field schema was invented in the data model.)*
- **Supersession Reference:** Supersedes the prior template deferral in `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1` §L. Preserves the deferral of AI-generated starting content.

### CHG-088 — DL-061: Project MRI definition (C-1) — adopt R1 per-project MRI; rename portfolio concept

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-061.
- **Affected Artifacts:** `00_owner/decisions/decision_log.md` (DL-061 recorded + Governance-Notes summary line added); `00_owner/changelog/changelog.md` (this entry). *(Propagation into `OSLO_RELEASE_1_MASTER_SPEC.md`, `OSLO_CAPABILITY_MATRIX_V2.md`, and the glossary Disambiguation Register is a resulting action under DL-061, landed as a separate owner/engineering-authored change.)*
- **Change Summary:** Recorded the owner ruling resolving **C-1**, the "Project MRI" flagship-term conflict. **Adopted** the Master Spec **per-project** "Project MRI" (R1 core: the per-project understanding visualization) as the canonical R1 meaning. The **whole-portfolio integrity-scan** concept (Baseline / Capability Matrix, I14 / Wave 3) is **renamed** to a distinct term (proposed **Portfolio Integrity Scan**, final term owner-confirmed) to remove the collision; a **Disambiguation Register** entry + doc-integrity regression guard will track the split (per DL-053). **MRI validation is held until the rename lands.** Unblocks Phase 1 MRI work (cross-refs DL-059 / the P-4 exit-gate track). This entry records the decision only; the spec edits are a resulting action, not yet applied.
- **Supersession Reference:** None. Resolves the open C-1 owner-action item.

### CHG-089 — DL-058: archive reversibility in R1 (UP-3 affirmed)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-058.
- **Affected Artifacts:** `00_owner/decisions/decision_log.md` (DL-058 recorded in numeric slot + Governance-Notes summary).
- **Change Summary:** Recorded the owner ruling that **archive is reversible in R1** (UP-3 holds); the PR #21 "no unarchive in R1" nod is rejected. Unarchive-in-R1 is a plan-vs-build gap to implement in Wave B; M6 hold lifted. (Re-landed clean via the governance-catchup PR after the original PR #25 was closed.)
- **Supersession Reference:** Supersedes the "no unarchive in R1" implementation nod from PR #21.

### CHG-090 — DL-062: confidence-dimension reconciliation — CAF first-class (C-2)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-062.
- **Affected Artifacts:** `00_owner/decisions/decision_log.md` (DL-062); `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register: first-class confidence dimension = CAF); `90_research/historical_artifacts/OSLO_ARCHITECTURE_BASELINE_V1.md` (§4 Composite Confidence marked superseded-for-R1, non-binding). Affirms (no change) the V2 scoring models.
- **Change Summary:** Affirmed **CAF (Clarity/Alignment/Feasibility) as the first-class confidence dimensions** for R1, with **Reliability** (Coverage/Evidence Availability/Assessability) as the qualifier. Doctrine-06 drivers preserved as Reliability sub-axes or inspectable CAF contributors; **decomposability is a binding condition** (no opaque Clarity rollup; QA negative test required). The "nine peer dimensions" claim (only in non-canonical Baseline V1 §4) is marked superseded-for-R1. Numeric calibration remains Open-TBD F1.
- **Supersession Reference:** None canonical. Marks Baseline-V1 §4 superseded-for-R1.

### CHG-091 — DL-063: Governance v2 — Risk-Tiered Routing (Class-A; model ratified, delegation staged)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-063.
- **Affected Artifacts:** `00_owner/decisions/decision_log.md` (DL-063 + Governance Notes); `00_owner/decisions/PROPOSAL_GOVERNANCE_V2_RISK_TIERED_ROUTING.md` + `REVIEW_GOVERNANCE_V2_RISK_TIERED_ROUTING.md` (copied into repo). **Follow-on:** Framework 001 doc amendment encoding the §4 table; CODEOWNERS re-scope + Class-D flip (Stage 3, on EM-seat activation).
- **Change Summary:** Ratified **Governance v2 Risk-Tiered Routing** — the 5-class model (A Canon · B Seam · C Product · D Engineering · E Operational), role seats (Owner = governance + product lead; EM = Hamza; Developer = Kashif), and the delegation safety rail. **Class-D delegation staged behind the per-gate red-proof; EM-seat activation deferred ~3 weeks** (owner remains Class-D approver in the interim; absent EM not set as required CODEOWNER until activation). §7/§10 activate now.
- **Supersession Reference:** None. Amends Framework 001 routing; narrows the uniform-gating default without removing it.

### CHG-092 — DL-064: C-3 experience↔architecture crosswalk (responsibility-primary §0)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-064.
- **Affected Artifacts:** `20_handoff/traceability/EXPERIENCE_SURFACE_RESPONSIBILITY_CROSSWALK_V1.md` (new — the §0 crosswalk); `00_owner/decisions/decision_log.md` (DL-064).
- **Change Summary:** Resolved **C-3** (missing experience→layer mapping) by ratifying a **responsibility-primary** crosswalk: every Master Spec experience surface maps to one of the seven canonical responsibilities; commodity surfaces map to none (DL-043 C/E/F). Legacy layer names deprecated/secondary per DL-043 + DL-053. Every mapping traces to ratified canon — none inferred. The artifact is the source for §0 of Architecture Baseline V2.
- **Supersession Reference:** None. C-3 was a gap, not a contradiction; documentation close-out.

### CHG-093 — DL-061 realization completion + doc-integrity fix (post-catchup cleanup)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-061 (realization of its already-ratified resulting actions, which PR #27 recorded but did not apply).
- **Affected Artifacts:** `00_owner/canonical_definitions/canonical_definitions.md` (Project MRI **Proposed → Canonical (R1)** + per-project definition + scope note); `00_owner/ontology/ontology_registry.md` (Project MRI status promoted, 2 entries); `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register: MRI / Project MRI); `90_research/historical_artifacts/OSLO_ARCHITECTURE_BASELINE_V1.md` (portfolio-MRI row superseded-for-R1, non-binding); `20_handoff/traceability/EXPERIENCE_SURFACE_RESPONSIBILITY_CROSSWALK_V1.md` (doc-integrity fix — de-linked the non-repo `MASTER_SPEC_ALIGNMENT_REVIEW` reference).
- **Change Summary:** Completed the **DL-061 realization edits** that PR #27 recorded but left unapplied (Project MRI was still "Proposed" on `main`): promoted Project MRI to **Canonical (R1)** with the per-project definition, added the MRI Disambiguation-Register entry, and marked the Baseline portfolio-MRI line superseded-for-R1. Also fixed the lone doc-integrity broken-link error from the governance-catchup PR (#31). doc-integrity now passes (errors = 0).
- **Supersession Reference:** None. Realizes DL-061; closes the broken-link error on `main`.

### CHG-094 — DL-065: Decision-Recording Discipline (one-file records + CI guard)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-065.
- **Affected Artifacts:** `00_owner/decisions/records/DL-065-decision-recording-discipline.md` (new — first record under the new discipline) + `00_owner/decisions/records/README.md` (new); `tools/dl_records.py` (new — `next`/`index`/`check`); `tools/doc_integrity_check.py` (new check #6 — records-regime guard); `00_owner/decisions/decision_log.md` (frozen-through-DL-064 note + generated records index); `CLAUDE.md` (Decision-Recording Discipline section, R1–R5).
- **Change Summary:** Adopted the **decision-recording discipline** that makes the 2026-06-16 sequencing tangle structurally impossible: **R1** one file per decision (DL-065+) with `decision_log.md` frozen through DL-064 and an auto-generated index; **R2** number-at-merge (DL-PENDING until landing); **R3** one canon PR in flight, merged linearly; **R4** a doc-integrity guard over the records regime; **R5** the Founder Console as sole serializer. Freeze-not-migrate: legacy entries are untouched and grandfathered. doc-integrity passes (0 errors).
- **Supersession Reference:** None. Amends the decision-recording mechanics of Framework 001 (additive). Framework 001 doc gets the formal R1–R5 amendment as a follow-on.

### CHG-095 — DL-066: resolve the DL-060 numbering gap (first decision under the new discipline)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-066.
- **Affected Artifacts:** `00_owner/decisions/records/DL-066-resolve-dl-060-gap.md` (new — first record authored via the DL-065 number-at-merge flow); `00_owner/decisions/decision_log.md` (records index regenerated to include DL-066).
- **Change Summary:** Retired **DL-060** as **reserved-but-unused (void)** — no content was ever ratified under it, and DL-059 (the Phase-1 falsifiable exit *criterion*) already governs sign-off. The number is recorded as an explicit void marker so the DL-059→DL-061 gap is intentional, not an omission. This is the **first decision processed end-to-end under DL-065**: drafted as `DL-PENDING`, numbered at merge (`dl_records.py next` → DL-066), index regenerated, and the records guard green.
- **Supersession Reference:** None. Closes the parked DL-060 item.

### CHG-096 — DL-067: Console-driven DL landing (scope + design)

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-067.
- **Affected Artifacts:** `00_owner/decisions/records/DL-067-console-driven-dl-landing.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated to include DL-067).
- **Change Summary:** Ratified the **scope + design** for making the Founder Console Decide lane the one-click front door for landing decisions, by automating the DL-065 flow as a **server-side GitHub Actions workflow** (`dl-land.yml`) — author + number-at-merge + index + changelog + gate + open PR — with **the owner's merge kept as the explicit human step** (never auto-merge canon; fail-closed on the gate; R3/R5 preserved). Server-side execution avoids the local-sandbox credential/`.git/index.lock` and stale-clone mis-numbering problems. The engineering **build** (`dl-land.yml` + Console button wiring) is the follow-on realization.
- **Supersession Reference:** None. Realizes DL-063 R5 atop DL-065; additive.

### CHG-097 — DL-067 realization: the `dl-land` workflow + helper

- **Date:** 2026-06-16 · **Authorizing Decision:** DL-067.
- **Affected Artifacts:** `.github/workflows/dl-land.yml` (new — server-side DL landing); `tools/dl_records.py` (new `land` + `next-chg` subcommands; GITHUB_OUTPUT integration); `00_owner/decisions/records/README.md` (preferred-landing-path section).
- **Change Summary:** Built the **`dl-land` GitHub Actions workflow** (workflow_dispatch: `title`/`body`/`slug`/`class`/`decided_by`) that realizes DL-067: it numbers the decision off current `main` (no stale-clone risk), writes the record, regenerates the index, appends the changelog, runs the **fail-closed** doc-integrity gate, refuses to start if a `decision/*` PR is already open (R3), pushes a branch, and **opens a PR — never merges** (owner-gated). `dl_records.py land` centralizes the record/index/changelog logic and is unit-tested in isolation. **Follow-on:** wire the Founder Console "Approve & Land" button to dispatch this workflow.
- **Supersession Reference:** None. Engineering realization of DL-067.

### CHG-098 — DL-068: Wave A sign-off + Wave B authorization

- **Date:** 2026-06-17 · **Authorizing Decision:** DL-068.
- **Affected Artifacts:** `00_owner/decisions/records/DL-068-wave-a-signoff-wave-b-authorization.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Wave A sign-off + Wave B authorization. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-099 — DL-069: Internal Gemma (local Llama runtime) as the primary LLM (amends DL-054 §5)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-069.
- **Affected Artifacts:** `00_owner/decisions/records/DL-069-internal-gemma-primary-llm.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Internal Gemma (local Llama runtime) as the primary LLM (amends DL-054 §5). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-100 — DL-070: Ratify the Phase 1 "Prove Understanding" falsifiable exit gate (P-4 / DL-059 realization)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-070.
- **Affected Artifacts:** `00_owner/decisions/records/DL-070-phase1-prove-understanding-exit-gate.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Ratify the Phase 1 "Prove Understanding" falsifiable exit gate (P-4 / DL-059 realization). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-101 — DL-071: DL-053 Disambiguation Register: 'Founder Console' (Intralign Founder Console vs OSLO Observability Console)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-071.
- **Affected Artifacts:** `00_owner/decisions/records/DL-071-founder-console-disambiguation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** DL-053 Disambiguation Register: 'Founder Console' (Intralign Founder Console vs OSLO Observability Console). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-102 — DL-072: Wave B exit-gate pass (with conditions) + Phase IV/Wave C authorization

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-072.
- **Affected Artifacts:** `00_owner/decisions/records/DL-072-wave-b-exit-gate-wave-c-authorization.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Wave B exit-gate pass (with conditions) + Phase IV/Wave C authorization. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-103 — DL-051: Repair stale `0X_` path references in engineering operational docs (clerical)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-051 (ownership-zone reorganization; follow-through).
- **Affected Artifacts:** 12 files under `30_engineering/` — the 8 phase `IMPLEMENTATION_PLAN.md`s + `implementation/README.md` + `PHASE_1_BUILD_KICKOFF_PACKET.md`; `delivery/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md`; `delivery/RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`; `delivery/starter_kit/CLAUDE.md` + `AGENTS.md`. 130 stale `01_/02_/03_` references repaired to current ownership-zone paths (`00_owner/` · `10_product/` · `20_handoff/` · `30_engineering/`). **No content change** — reference paths only.
- **Change Summary:** Bucket 1 of the DL-051 path-migration follow-through (see `00_owner/decisions/PROPOSAL_IMPLEMENTATION_TREE_PATH_MIGRATION_DL051_FOLLOWTHROUGH_DRAFT.md`). Forward-pointing developer-facing references only; every rewritten `.md` path existence-verified as a full path; doc-integrity gate green. Five bare-prefix/historical references in the Handoff Package left for owner review; owner-canon cross-references (Bucket 2) and append-only ledgers / restructure-description docs (Bucket 3) intentionally untouched.
- **Supersession Reference:** None.

### CHG-104 — DL-051: Repair stale `0X_` cross-references in owner-canon registries (clerical, Bucket 2)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-051 (ownership-zone reorganization; follow-through).
- **Affected Artifacts:** `00_owner/canonical_definitions/canonical_definitions.md`, `00_owner/ontology/ontology_registry.md`, `00_owner/build_governance/AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md`, `00_owner/build_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`. 168 stale `01_/02_/03_` cross-references repaired to current ownership-zone paths. **No content/definitional change** — reference paths only.
- **Change Summary:** Bucket 2 of the DL-051 path-migration follow-through (live owner-canon cross-references). Every rewritten `.md` path existence-verified as a full path; doc-integrity gate green. Append-only ledgers (changelog, decision_log) and restructure-description docs untouched (Bucket 3). Adjacent live-canon files (`constitution/10_canonical_definitions.md`, `CANONICAL_GLOSSARY.md`, `backlog/revision_backlog.md`, `architecture_decisions/*`, `OPEN_TBD_REGISTER.md`) **deliberately NOT auto-edited** — surfaced for separate owner decision.
- **Supersession Reference:** None.

### CHG-105 — DL-051: Repair stale `0X_` cross-references in adjacent owner-canon docs (clerical, Bucket 2b — completes follow-through)

- **Date:** 2026-06-18 · **Authorizing Decision:** DL-051 (ownership-zone reorganization; follow-through).
- **Affected Artifacts:** `00_owner/CANONICAL_GLOSSARY.md` (1), `00_owner/constitution/10_canonical_definitions.md` (1), `00_owner/backlog/revision_backlog.md`, `00_owner/backlog/BACKLOG_FAST_DEEP_CONTRACT_FORMALIZATION_DRAFT.md`, `00_owner/OPEN_TBD_REGISTER.md`, `00_owner/architecture_decisions/ACTIVE_ARCHITECTURE_RECONCILIATION_RECOMMENDATION_001.md`, `00_owner/decisions/PROPOSAL_TOOL_NEUTRAL_AGENT_TERMINOLOGY_DL045_DRAFT.md`. 16 stale `01_/02_/03_` cross-references repaired to current ownership-zone paths. **No content/definitional change** — reference paths only.
- **Change Summary:** Bucket 2b — completes the DL-051 path-migration follow-through across live owner canon. The **constitution** and **CANONICAL_GLOSSARY** edits are each a single pure path-string swap (governance-tier registry cross-ref; tier-ladder backlog cross-ref) with no definitional change. Every rewritten `.md` path existence-verified; doc-integrity gate green. Remaining `0X_` mentions are bare-prefix prose or the legacy layer dir `03_architecture/components/`, intentionally left. Append-only ledgers + restructure/disposition docs untouched (Bucket 3). **DL-051 path migration now complete** across engineering (CHG-103) and owner canon (CHG-104, CHG-105).
- **Supersession Reference:** None.

### CHG-106 — DL-073: Two-mode stage-conditioned onboarding (deferred-signup) + save-to-keep signup trigger

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-073.
- **Affected Artifacts:** `00_owner/decisions/records/DL-073-two-mode-onboarding-deferred-signup.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Two-mode stage-conditioned onboarding (deferred-signup) + save-to-keep signup trigger. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-107 — DL-073: Onboarding spec amendment (§0 two-mode, stage-conditioned model)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-073.
- **Affected Artifacts:** `10_product/experience/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` — amended: new **§0** (governing two-mode / stage-conditioned model + permutation matrix + phasing); status line; cross-reference markers on §A/§D/§E/§G/§H/§I; behavioral edits to §H (auto-provisioned, ingestion-first landing) and §S (disclosure order); **OB-C1** amended to the two-mode journey with `[GA-pending]` tags.
- **Change Summary:** Realizes DL-073 in the canonical onboarding spec. First-time = ingestion-first / deferred-signup / auto-provisioned identity·workspace·project; resume = auth-entry; release-stage auth-gate position (Alpha/Beta front gate → ingestion; GA no front gate); save-to-keep GA signup trigger. Supersedes the single-mode linear flow and OB-C1's account-first journey for the empty case. **Alpha/Beta conformant now**; GA-specific behaviors tagged `[GA-pending]` pending the DL-073 §4.2–4.4 engineering proposals. All §T integrity invariants, epistemic safety, the DL-046 60s definition, and minimum-to-value (name + one artifact) preserved. No doctrine or constitution change.
- **Supersession Reference:** Amends conformance **OB-C1** and §A/§D/§E/§G/§H/§I/§S of the onboarding spec (per DL-073).

### CHG-108 — DL-074: Hybrid pricing — tier subscription + per-Deep-Pass overage (single-governor / multi-meter); extends DL-048

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-074.
- **Affected Artifacts:** `00_owner/decisions/records/DL-074-hybrid-pricing-multi-meter.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Hybrid pricing — tier subscription + per-Deep-Pass overage (single-governor / multi-meter); extends DL-048. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-109 — DL-075: Ratify the Outcome-Lifecycle (Planning/Execution/Validation) orientation crosswalk

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-075.
- **Affected Artifacts:** `00_owner/decisions/records/DL-075-outcome-lifecycle-orientation-crosswalk.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Ratify the Outcome-Lifecycle (Planning/Execution/Validation) orientation crosswalk. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-110 — DL-076: Ratify the OSLO release model & Alpha release ladder (R1-R5 reconciled with Alpha/Beta/§20)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-076.
- **Affected Artifacts:** `00_owner/decisions/records/DL-076-release-model-alpha-ladder.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Ratify the OSLO release model & Alpha release ladder (R1-R5 reconciled with Alpha/Beta/§20). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-111 — DL-077: Ratify the planning-artifact model architecture - Option C hybrid core (fixed understanding core + extensible execution-planning layer)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-077.
- **Affected Artifacts:** `00_owner/decisions/records/DL-077-planning-artifact-model-hybrid-core.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Ratify the planning-artifact model architecture - Option C hybrid core (fixed understanding core + extensible execution-planning layer). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-112 — DL-074: Realize Tiers 3-5 (Pro·Team·Enterprise) + hybrid overage/governor config in Release-1 Calibration Defaults §4c

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-074.
- **Affected Artifacts:** `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (§4c — added Pro/Team/Enterprise tier-knob rows; per-Deep-Pass overage + normalized-compute-governor config; forward monitoring/agent meter rows; resolved Open-TBD A1/E3; corrected stale ladder cross-reference path).
- **Change Summary:** Realize the DL-074 hybrid pricing model as owner-tunable §4c configuration — Tiers 3-5 starting values (re-tunable from `AI Spend Recorded` telemetry) plus the paid-tiers-only per-Deep-Pass overage under a normalized compute governor (tokens × model-tier weight), with forward monitoring/agent meters marked GA-pending. Config realization of a ratified decision; no new decision, no doctrine, epistemic invariants unaffected.
- **Supersession Reference:** None.

### CHG-113 — DL-078: Ratify the artifact-profile mechanism & registry realization design (DL-077 Option C realization intent)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-078.
- **Affected Artifacts:** `00_owner/decisions/records/DL-078-artifact-profile-realization-design.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Ratify the four-surface realization design for the DL-077 hybrid-core planning-artifact model — profile-aware generation generalizing the single Wave S step (Derived/CHR/recompute invariants and the five Critical negatives unchanged), fixed-core boundary (Requirements stays core + additive compliance modules), compositional multi-signal profile resolver (not a domain×methodology matrix), and an owner-governed artifact-profile registry (E6 substrate; first-party→certified→open, build-time-first; admits L2 structure, never L3 cognition — CAF/scoring stay first-party). R1 stays fixed; methodology-cadence is a later separately-escalated sub-phase. Realization intent only; engineering authors the mechanism. No epistemic invariant or doctrine changed.
- **Supersession Reference:** None. Realizes DL-077; the E4 lens cognition boundary is the separate DL-079.

### CHG-114 — DL-079: Ratify the third-party evaluation-lens cognition boundary (E4)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-079.
- **Affected Artifacts:** `00_owner/decisions/records/DL-079-e4-lens-cognition-boundary.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `00_owner/architecture_decisions/E4_THIRD_PARTY_EVALUATION_LENS_GOVERNANCE_ESCALATION_001.md` (status → RESOLVED); `00_owner/backlog/BACKLOG_ECOSYSTEM_MARKETPLACE_AND_CREATOR_PROGRAM.md` (E4 gate resolved).
- **Change Summary:** Ratify the E4 cognition boundary — a third-party evaluation lens is governed input to first-party cognition, never third-party cognition; it may surface attributed, confidence-qualified considerations but never alters CAF/confidence/scores and never disposes (OB-5; advise proposes never disposes). Reference-only (A) first; governed Derived overlay (B) north-star; Option C (certified scoring contribution) explicitly not adopted and fenced as a separate future doctrine decision; CAF stays first-party. Draws the boundary within the existing epistemic model; affirms (does not alter) the invariants; no new invariant. E4 remains design-only.
- **Supersession Reference:** None. Resolves the E4 escalation. Option C not adopted (separate future doctrine decision).

### CHG-115 — DL-080: Ratify the GA deferred-signup realization (provisional identity · pre/post-signup gating · retention & privacy)

- **Date:** 2026-06-19 · **Authorizing Decision:** DL-080.
- **Affected Artifacts:** `00_owner/decisions/records/DL-080-ga-deferred-signup-realization.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `00_owner/decisions/PROPOSAL_GA_DEFERRED_SIGNUP_ENGINEERING_REALIZATION_DRAFT.md` (status → ratified-intent); `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` (GA note → ratified); `00_owner/decisions/PROPOSAL_TWO_MODE_ONBOARDING_DEFERRED_SIGNUP_DRAFT.md` (§6.3 authorization → ratified DL-080). **Clerical status reconciliation reflecting the prior DL-078 ratification:** `00_owner/architecture_decisions/ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001.md` and `00_owner/architecture_decisions/PLANNING_ARTIFACT_MODEL_EXTENSIBILITY_ESCALATION_001.md` (status → ratified-intent DL-078).
- **Change Summary:** Ratify the GA deferred-signup realization (DL-073 §Phasing a/b/c) as one decision — provisional `Principal` with claim-as-promotion and full identity/record continuity (OB-5); anonymous gating = one project / Fast Pass only / Free per-run envelope / rate-capped, Deep+persistence behind signup, with pre-signup consumption resetting to the Free governor at claim; pre-signup data Operational-class with a 30-day unclaimed TTL, canonical retention attaching at claim, never-claimed purgeable/non-linkable. Settles the two open owner values (reset-at-claim; 30-day TTL). Realization intent only (engineering authors data model, §4c anonymous row, §4 provisional retention class, purge); GA-gated; no doctrine; epistemic invariants preserved.
- **Supersession Reference:** None. Realizes DL-073 §Phasing; discharges the two-mode proposal §6.3 authorization.

### CHG-116 — DL-081: Ratify Layer-Before-Depth roadmap sequencing

- **Date:** 2026-06-28 · **Authorizing Decision:** DL-081.
- **Affected Artifacts:** `00_owner/decisions/records/DL-081-roadmap-layer-sequencing.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `00_owner/backlog/revision_backlog.md` (RB-027 added); `00_owner/decisions/PROPOSAL_ROADMAP_LAYER_SEQUENCING_DRAFT.md` (status → adopted).
- **Change Summary:** Ratify the **Layer-Before-Depth** roadmap sequencing principle — OSLO establishes cross-platform planning-governance breadth (**≥ 2** governed platforms, real per-platform depth) at the understanding/governance altitude before descending into execution-phase governance; advisory-only (DL-047) preserved throughout; sequences existing Positioning §7 ladder levels and the DL-034 Execution Depth axis; R1 scope unchanged (CHG-064). Non-doctrinal product-roadmap orientation.
- **Supersession Reference:** None. Additive; traces up to Positioning §7; consistent with DL-076, DL-047, DL-034.

### CHG-117 — DL-082: Ratify Alpha exit criteria (amends DL-076)

- **Date:** 2026-06-28 · **Authorizing Decision:** DL-082.
- **Affected Artifacts:** `00_owner/decisions/records/DL-082-alpha-exit-criteria.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` (new §3a Alpha exit criteria); `00_owner/backlog/revision_backlog.md` (RB-028 added); `00_owner/decisions/PROPOSAL_ALPHA_EXIT_CRITERIA_DRAFT.md` (status → adopted).
- **Change Summary:** Amend DL-076 by ratifying the **Alpha → Beta exit criteria** — (1) build/prove gates pass; (2) value validated by behavioral retention / repeat use; (3) **≥ 2** governed planning platforms with real per-platform depth; (4) execution visibility operational = read-only outcome ingest (≥ 1 platform) + closed feedback loop, drift-surfacing deferred to Beta+; (5) 50+ users + engagement (§20) unchanged. Strictly observational — advisory-only (DL-047) preserved. Non-doctrinal.
- **Supersession Reference:** Amends DL-076 (adds §3a to `RELEASE_MODEL_AND_ALPHA_LADDER_V1.md`). No prior change superseded.

### CHG-118 — DL-083: Execution-monitoring tier placement & phase (T3/Pro+, Beta; out of Alpha exit) + capability tier split

- **Date:** 2026-06-28 · **Authorizing Decision:** DL-083.
- **Affected Artifacts:** `00_owner/decisions/records/DL-083-execution-monitoring-tier-and-phase.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` (§3a amended — execution monitoring → Beta; three-way capability tier split); `00_owner/backlog/revision_backlog.md` (RB-029 added; RB-028 status → adopted); `00_owner/decisions/PROPOSAL_EXECUTION_MONITORING_TIER_AND_PHASE_DRAFT.md` (new).
- **Change Summary:** Amend DL-082 and extend DL-074. **Three-way capability tier split:** Export-Share-Out = Free/no-account; plan export → execution tool = Tier 2/Basic (distinct, separately scoped); execution monitoring (inbound outcome ingest + closed loop) = Tier 3/Pro+, built in Beta. **Phase move:** execution monitoring relocated from the Alpha exit criteria to **Beta** (a Beta-built capability cannot gate Alpha graduation). Amended Alpha exit = build/prove + value-by-retention + ≥ 2 governed planning sources + 50+ users (§20). Alpha validates **engagement**; Beta validates **outcome impact**. Advisory-only (DL-047) preserved; non-doctrinal.
- **Supersession Reference:** Amends DL-082 (removes the execution-visibility Alpha exit criterion; relocates to Beta); extends DL-074 (capability tier placement). No epistemic invariant, doctrine, or constitution touched.

### CHG-119 — DL-084: R2 candidate-epic phase/tier placement + Foundational-Architecture-in-Alpha principle

- **Date:** 2026-06-28 · **Authorizing Decision:** DL-084.
- **Affected Artifacts:** `00_owner/decisions/records/DL-084-r2-phase-tier-placement.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated); `00_owner/backlog/revision_backlog.md` (RB-032 added); `00_owner/decisions/PROPOSAL_R2_PHASE_TIER_PLACEMENT_DRAFT.md` (new). Reflects the placements already annotated in `00_owner/backlog/RELEASE_2_BACKLOG_CANDIDATES.md` (CHG-118-era PR #78).
- **Change Summary:** Bind the R2 candidate-epic phase/tier placement — **Execution Intelligence (R2-C) → Beta**, **Team Collaboration depth (R2-D) → Team tier (Tier 4)**, **Governance & Authority (R2-E) → Beta** — and ratify the **Foundational-Architecture-in-Alpha** build-sequencing principle: architectural foundation for a gated capability may be laid early in Alpha (R2) where it measurably reduces later effort/complexity, kept advisory-only / non-activating / specified-but-inactive and routed through scoping (+ DL where architectural). Sibling to DL-081 (Layer-Before-Depth). Non-doctrinal; no capability or epistemic invariant introduced.
- **Supersession Reference:** None. Additive; consistent with DL-074, DL-076, DL-081, DL-083, DL-047.

### CHG-120 — DL-085: User-facing Confidence movement & quantified progress presentation

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-085.
- **Affected Artifacts:** `00_owner/decisions/records/DL-085-confidence-presentation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** User-facing Confidence movement & quantified progress presentation. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-121 — DL-086: Outcome Confidence index calibration (measurement) — 5-band scheme + v0 defaults

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-086.
- **Affected Artifacts:** `00_owner/decisions/records/DL-086-confidence-index-calibration.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Outcome Confidence index calibration (measurement) — 5-band scheme + v0 defaults. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-122 — DL-087: Strategic chain & onboarding positioning (+ plain-language labels)

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-087.
- **Affected Artifacts:** `00_owner/decisions/records/DL-087-strategic-chain-positioning.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Strategic chain & onboarding positioning (+ plain-language labels). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-123 — DL-088: R1 UX-surface reconciliation (prototype-as-baseline)

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-088.
- **Affected Artifacts:** `00_owner/decisions/records/DL-088-ux-surface-reconciliation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** R1 UX-surface reconciliation (prototype-as-baseline). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-124 — DL-089: Clarification flow contract (object-free; in-panel + chat — Option B)

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-089.
- **Affected Artifacts:** `00_owner/decisions/records/DL-089-clarification-flow.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Clarification flow contract (object-free; in-panel + chat — Option B). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-125 — DL-090: Overview cognitive-load trim + Attention-map as its own surface (amends DL-088)

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-090.
- **Affected Artifacts:** `00_owner/decisions/records/DL-090-overview-trim.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Overview cognitive-load trim + Attention-map as its own surface (amends DL-088). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-126 — DL-091: Wave C (Advise) exit-gate pass + Phase V / Wave U authorization

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-091.
- **Affected Artifacts:** `00_owner/decisions/records/DL-091-wave-c-exit-gate-phase-v-authorization.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Wave C (Advise) exit-gate pass + Phase V / Wave U authorization. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-127 — DL-092: Wave C (Advise) exit-gate pass + Phase V / Wave U authorization

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-092. **VOID — accidental duplicate of CHG-126 / DL-091 (double-land); no independent effect.**
- **Affected Artifacts:** `00_owner/decisions/records/DL-092-wave-c-exit-gate-phase-v-authorization.md` (voided in place — duplicate of DL-091).
- **Change Summary:** Duplicate land of the Wave C exit-gate + Phase V authorization already recorded by DL-091 (CHG-126). DL-092 marked Void; number retained for monotonicity (DL-065).
- **Supersession Reference:** Voided as a duplicate of DL-091.

### CHG-128 — DL-093: Finding type + epistemic basis presentation (two-axis; RB-033 Phase R1)

- **Date:** 2026-07-02 · **Authorizing Decision:** DL-093.
- **Affected Artifacts:** `00_owner/decisions/records/DL-093-finding-type-and-epistemic-basis-r1.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Finding type + epistemic basis presentation (two-axis; RB-033 Phase R1). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-129 — DL-094: Finding flow simplification: no-Acknowledge lifecycle + single-action resolution (RB-035)

- **Date:** 2026-07-08 · **Authorizing Decision:** DL-094.
- **Affected Artifacts:** `00_owner/decisions/records/DL-094-finding-flow-simplification.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Finding flow simplification: no-Acknowledge lifecycle + single-action resolution (RB-035). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-130 — DL-095: Findings to Issues user-facing label (RB-036)

- **Date:** 2026-07-08 · **Authorizing Decision:** DL-095.
- **Affected Artifacts:** `00_owner/decisions/records/DL-095-findings-as-issues-user-facing-label.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Findings to Issues user-facing label (RB-036). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-131 — DL-096: Overview surface redesign: confidence-led, low-cognitive-load (RB-037)

- **Date:** 2026-07-08 · **Authorizing Decision:** DL-096.
- **Affected Artifacts:** `00_owner/decisions/records/DL-096-overview-redesign.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Overview surface redesign: confidence-led, low-cognitive-load (RB-037). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-132 — DL-097: Canonical CAF-dimension maturity band vocabulary (RB-038)

- **Date:** 2026-07-08 · **Authorizing Decision:** DL-097.
- **Affected Artifacts:** `00_owner/decisions/records/DL-097-caf-dimension-band-vocabulary.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Canonical CAF-dimension maturity band vocabulary (RB-038). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-133 — DL-098: Reconcile CAF-dimension bands to the DL-086 5-band scheme (supersedes DL-097) (RB-039)

- **Date:** 2026-07-09 · **Authorizing Decision:** DL-098.
- **Affected Artifacts:** `00_owner/decisions/records/DL-098-caf-dimension-band-reconcile.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Reconcile CAF-dimension bands to the DL-086 5-band scheme (supersedes DL-097) (RB-039). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-134 — DL-099: Reliability qualifier presentation — single quiet-by-default state (loud on CONF-06 divergence)

- **Date:** 2026-07-10 · **Authorizing Decision:** DL-099.
- **Affected Artifacts:** `00_owner/decisions/records/DL-099-reliability-qualifier-presentation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Reliability qualifier presentation — single quiet-by-default state (loud on CONF-06 divergence). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-135 — DL-100: Reliability qualifier — finalize copy + confirm CONF-06 trigger reuse (closes RB-040)

- **Date:** 2026-07-10 · **Authorizing Decision:** DL-100.
- **Affected Artifacts:** `00_owner/decisions/records/DL-100-reliability-qualifier-copy-finalize.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Reliability qualifier — finalize copy + confirm CONF-06 trigger reuse (closes RB-040). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-136 — DL-102: Controlled Release & Tiering-in-Alpha (reconciles CHG-061; amends DL-048 scope, extends DL-049/DL-055/DL-062)

- **Date:** 2026-07-11 · **Authorizing Decision:** DL-102.
- **Affected Artifacts:** `00_owner/decisions/records/DL-102-controlled-release-and-tiering-in-alpha.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Controlled Release & Tiering-in-Alpha (reconciles CHG-061; amends DL-048 scope, extends DL-049/DL-055/DL-062). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-137 — DL-103: Analysis cost basis & tier re-derivation — never tier judgment quality; commission incremental recompute + prompt caching (supersedes 'Pro adds model quality'; suspends the §4c numeric basis)

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-103.
- **Affected Artifacts:** `00_owner/decisions/records/DL-103-analysis-cost-basis-and-tier-rederivation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Analysis cost basis & tier re-derivation — never tier judgment quality; commission incremental recompute + prompt caching (supersedes 'Pro adds model quality'; suspends the §4c numeric basis). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-138 — DL-104: Errata to DL-103 — strike the priority/latency residue; retire UP-1/UP-2/UP-5; number UP-APPLY and UP-REPORT; refresh DL-102 E; add the P1 health-framing defect class

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-104.
- **Affected Artifacts:** `00_owner/decisions/records/DL-104-errata-dl-103-priority-lever-and-up-taxonomy.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Errata to DL-103 — strike the priority/latency residue; retire UP-1/UP-2/UP-5; number UP-APPLY and UP-REPORT; refresh DL-102 E; add the P1 health-framing defect class. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-139 — DL-105: Commission E1–E3 analysis cost optimization into R1 — prompt caching, scoped recompute (Evaluate always full + equivalence gate), evidence coalescing; instrument, do not gate

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-105.
- **Affected Artifacts:** `00_owner/decisions/records/DL-105-commission-e1-e3-analysis-cost-optimization.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Commission E1–E3 analysis cost optimization into R1 — prompt caching, scoped recompute (Evaluate always full + equivalence gate), evidence coalescing; instrument, do not gate. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-140 — DL-106: Commission the DL-069 model-judgment evaluation — and record that DL-103 §1 raised its bar (no 'Gemma for Free, frontier for Pro' hatch); per-call-site qualification; AC-V3 is disqualifying

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-106.
- **Affected Artifacts:** `00_owner/decisions/records/DL-106-commission-dl069-model-judgment-evaluation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Commission the DL-069 model-judgment evaluation — and record that DL-103 §1 raised its bar (no 'Gemma for Free, frontier for Pro' hatch); per-call-site qualification; AC-V3 is disqualifying. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-141 — DL-107: Obey the doctrine, don't narrate it — and commission the two specs the repo has cited but never possessed: RELEASE_1_TIER_DEFINITIONS_V1 and RELEASE_1_REPORTING_SPECIFICATION_V1 (M4)

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-107.
- **Affected Artifacts:** `00_owner/decisions/records/DL-107-obey-dont-narrate-commission-tier-definitions-and-reporting.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Obey the doctrine, don't narrate it — and commission the two specs the repo has cited but never possessed: RELEASE_1_TIER_DEFINITIONS_V1 and RELEASE_1_REPORTING_SPECIFICATION_V1 (M4). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-142 — DL-108: Reconcile design-guidance 'Executive Translation' with the reporting doctrine — tailor the ask, never the read

- **Date:** 2026-07-12 · **Authorizing Decision:** DL-108.
- **Affected Artifacts:** `00_owner/decisions/records/DL-108-executive-translation-reconciliation.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Reconcile design-guidance 'Executive Translation' with the reporting doctrine — tailor the ask, never the read. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-143 — DL-109: Surface the provenance OSLO already tracks — grounded vs inferred, load-bearing inferences, the assumption register, the Inference Map; REJECT the 'Understanding Debt' frame (AE-06 not adopted); escalate inference lineage as a schema decision

- **Date:** 2026-07-13 · **Authorizing Decision:** DL-109.
- **Affected Artifacts:** `00_owner/decisions/records/DL-109-surface-provenance-reject-the-debt-frame.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Surface the provenance OSLO already tracks — grounded vs inferred, load-bearing inferences, the assumption register, the Inference Map; REJECT the 'Understanding Debt' frame (AE-06 not adopted); escalate inference lineage as a schema decision. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-144 — DL-110: Outcome-positioning standard — understand & steer toward outcomes, never forecast

- **Date:** 2026-07-13 · **Authorizing Decision:** DL-110.
- **Affected Artifacts:** `00_owner/decisions/records/DL-110-outcome-positioning-standard.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Outcome-positioning standard — understand & steer toward outcomes, never forecast. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-145 — DL-111: Progress panel adopts the owner LOCK foundation-bar (amends D176/D194c/D187/D179d/DL-109 for the Overview panel)

- **Date:** 2026-07-14 · **Authorizing Decision:** DL-111.
- **Affected Artifacts:** `00_owner/decisions/records/DL-111-progress-panel-foundation-bar.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Progress panel adopts the owner LOCK foundation-bar (amends D176/D194c/D187/D179d/DL-109 for the Overview panel). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-146 — DL-112: Erratum to DL-111 — grounded facts are attested-only; two provenance states; load-bearing is a superset

- **Date:** 2026-07-14 · **Authorizing Decision:** DL-112.
- **Affected Artifacts:** `00_owner/decisions/records/DL-112-progress-panel-erratum-grounded-attested-only.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Erratum to DL-111 — grounded facts are attested-only; two provenance states; load-bearing is a superset. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-147 — DL-113: Progress panel unifies on one named unit — the statement (adds a DL-053 entry; amends DL-111)

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-113.
- **Affected Artifacts:** `00_owner/decisions/records/DL-113-progress-panel-statement-unit.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Progress panel unifies on one named unit — the statement (adds a DL-053 entry; amends DL-111). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-148 — DL-114: A finding/statement impacts a set of CAF dimensions — data-model conformance + by-dimension inference

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-114.
- **Affected Artifacts:** `00_owner/decisions/records/DL-114-caf-multidimension-conformance.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** A finding/statement impacts a set of CAF dimensions — data-model conformance + by-dimension inference. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-149 — DL-115: Erratum to DL-114 — the dimensional Inference Map (Phase 3) is included; scope-boundary bullet corrected

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-115.
- **Affected Artifacts:** `00_owner/decisions/records/DL-115-dl114-phase3-scope-erratum.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Erratum to DL-114 — the dimensional Inference Map (Phase 3) is included; scope-boundary bullet corrected. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-150 — DL-116: CAF drill-down — quantify the drivers, never the dimension (adds a finding-type field)

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-116.
- **Affected Artifacts:** `00_owner/decisions/records/DL-116-caf-dimension-drilldown.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** CAF drill-down — quantify the drivers, never the dimension (adds a finding-type field). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-151 — DL-117: Confidence and CAF coupling: episodic trend leaves the state/CAF seam; the required read stays

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-117.
- **Affected Artifacts:** `00_owner/decisions/records/DL-117-confidence-caf-coupling.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Confidence and CAF coupling: episodic trend leaves the state/CAF seam; the required read stays. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-152 — DL-118: Overview surface roles (governing boundary model) + Start-here charter extension: guidance ranks confirmations alongside issues

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-118.
- **Affected Artifacts:** `00_owner/decisions/records/DL-118-overview-surface-roles-and-start-here.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Overview surface roles (governing boundary model) + Start-here charter extension: guidance ranks confirmations alongside issues. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-153 — DL-119: Amendment to D253: statement type-decomposition moves from resident to an on-demand disclosure (density pass)

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-119.
- **Affected Artifacts:** `00_owner/decisions/records/DL-119-d253-decomposition-disclosure.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** Amendment to D253: statement type-decomposition moves from resident to an on-demand disclosure (density pass). Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

### CHG-154 — DL-120: R1.x intermediate enhancements fold into the R1 build; R1 feature-freezes before dev handoff

- **Date:** 2026-07-16 · **Authorizing Decision:** DL-120.
- **Affected Artifacts:** `00_owner/decisions/records/DL-120-r1-foldin.md` (new); `00_owner/decisions/decision_log.md` (records index regenerated).
- **Change Summary:** R1.x intermediate enhancements fold into the R1 build; R1 feature-freezes before dev handoff. Landed via the dl-land workflow (DL-067).
- **Supersession Reference:** None.

---

## Governance Notes

1. The changelog is operative as of CHG-001. All subsequent canonical changes must be recorded here, authorized by a ratified Decision.
2. The current schema is provisional pending governance refinement of the Traceability Record (open condition on DL-030).
3. Entries do not require Proposal-Review-Decision in their own right when they merely record changes authorized by a ratified Decision. The authorizing Decision provides the governance traceability.
4. Amendments to the changelog schema require a Proposal under Framework 001/001A.

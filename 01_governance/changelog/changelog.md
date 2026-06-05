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

---

## Governance Notes

1. The changelog is operative as of CHG-001. All subsequent canonical changes must be recorded here, authorized by a ratified Decision.
2. The current schema is provisional pending governance refinement of the Traceability Record (open condition on DL-030).
3. Entries do not require Proposal-Review-Decision in their own right when they merely record changes authorized by a ratified Decision. The authorizing Decision provides the governance traceability.
4. Amendments to the changelog schema require a Proposal under Framework 001/001A.

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
- **Affected Artifacts:** `07_governance/decision_log.md` (DL-033 entry appended; header note updated to reflect operative range DL-029 through DL-033).
- **Change Summary:** Proposal 000 ratified. The doctrine-centered repository architecture is the canonical architecture of the OSLO knowledge base. Content tier and Governance tier are functionally distinct. Precedence within Content tier: Doctrine > Constitution > Implementation Specifications. Source Material is non-canonical. Manifest sits in Governance tier as orientation with non-doctrinal force. Subsystems must anchor to canonical content.
- **Supersession Reference:** None. Establishes architecture; does not supersede prior Decisions. Grandfathered Stated decisions DL-001 through DL-028 continue under DL-032.

### CHG-009 — Proposal 000 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `07_governance/proposal_000_disposition.md` (created).
- **Change Summary:** The full Proposal 000 Disposition Document placed in `07_governance/` as the canonical record of the ratified architecture. Document includes the architecture, role definitions for each repository object class, rejected options and reasoning, accepted tradeoffs, backlog impacts, and resulting repository actions.
- **Supersession Reference:** None.

### CHG-010 — Backlog Updates Recording Proposal 000 Outcomes

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-033.
- **Affected Artifacts:** `07_governance/revision_backlog.md` (RB-019 and RB-011 closed; RB-005 and RB-010 partially closed; each entry annotated with Disposition, Closed/Partially Closed By, Date, and Status fields).
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
- **Affected Artifacts:** `07_governance/decision_log.md` (DL-034 entry appended; header note updated to reflect operative range DL-029 through DL-034).
- **Change Summary:** RB-003 (Progression Model Reconciliation) ratified as DL-034. The OSLO Evolution Framework is the canonical multi-axis progression taxonomy. Four distinct but correlated axes ratified: Cognition Scope (Doctrine 02 canonical), Product Identity (Doctrine 09 canonical), Trust Gradient (Doctrine 09 / Article 41 aligned), Execution Depth (Doctrine 10 / Article 43 aligned). Doctrine prevails over Constitution where stage labels or counts conflict.
- **Supersession Reference:** Closes RB-003. Partially resolves RB-010 with respect to Draft Principle 17. Partially unblocks RB-015.

### CHG-015 — RB-003 Disposition Document Placed

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `07_governance/rb_003_disposition.md` (created).
- **Change Summary:** Full RB-003 disposition document placed in `07_governance/`. Document records the OSLO Evolution Framework, the four ratified axes, the ratified vs provisional status of each label, affected artifacts, and backlog impacts.
- **Supersession Reference:** None.

### CHG-016 — Constitution Articles 40 and 44 Annotated

- **Date:** 2026-05-29
- **Authorizing Decision:** DL-034.
- **Affected Artifacts:** `02_ux_constitution/08_product_evolution_constitution.md` (inline Governance Notes added to Article 40 and Article 44).
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
- **Affected Artifacts:** `07_governance/revision_backlog.md` (RB-003 closed; RB-010 updated to record Draft 17 absorption; RB-015 annotated with partial unblock).
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

---

## Governance Notes

1. The changelog is operative as of CHG-001. All subsequent canonical changes must be recorded here, authorized by a ratified Decision.
2. The current schema is provisional pending governance refinement of the Traceability Record (open condition on DL-030).
3. Entries do not require Proposal-Review-Decision in their own right when they merely record changes authorized by a ratified Decision. The authorizing Decision provides the governance traceability.
4. Amendments to the changelog schema require a Proposal under Framework 001/001A.

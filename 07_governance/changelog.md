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

---

## Governance Notes

1. The changelog is operative as of CHG-001. All subsequent canonical changes must be recorded here, authorized by a ratified Decision.
2. The current schema is provisional pending governance refinement of the Traceability Record (open condition on DL-030).
3. Entries do not require Proposal-Review-Decision in their own right when they merely record changes authorized by a ratified Decision. The authorizing Decision provides the governance traceability.
4. Amendments to the changelog schema require a Proposal under Framework 001/001A.

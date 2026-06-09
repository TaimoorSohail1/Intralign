# RB-001 / Proposal 002 — Disposition Document

## Decision Identifier

DL-036

## Title

Adopt the Bounded Registry Foundation per Proposal 002 / RB-001

## Disposition

**Accepted with Conditions**

The conditions are the eight closing-Decision clarifications identified by the Framework 001A Review. Each is recorded in the Closing Decision Clarifications section below and operates as a narrative qualification of the Resolutions, not as a deferred amendment.

## Date Ratified

2026-05-29

## Authorizing Backlog Item

RB-001 — Canonical Registry Consolidation

## Authorizing Proposal

Proposal 002 — RB-001 Bounded Registry Foundation

## Source Material

- RB-001 Scope Directive (owner guidance)
- RB-001 Preparation Analysis
- RB-001 Scope Control Package
- Proposal 002 — RB-001 Bounded Registry Foundation
- Framework 001A Review of Proposal 002

## Repository Owner Principles

The decision is bounded to Registry Foundation work only, per the owner's principles:

1. RB-001 does not absorb RB-004.
2. RB-001 does not perform implementation cleanup.
3. RB-001 establishes the registry and ownership foundation needed to unblock downstream backlog items.
4. The goal is governable, bounded, executable closure.

## Rationale

Proposal 002 satisfies the bounded scope defined by the Scope Directive. All eight Scope Directive items are addressed by Resolutions R1 through R8. The Framework 001A Review identified ten Concerns, of which eight required closing-Decision clarification and two were acceptable as scope-bounded properties. The eight clarifications are folded into this Decision as narrative qualifications. The substance of Proposal 002 is adopted without revision. The closing Decision narrative clarifies points of potential confusion without expanding scope.

---

## Ratified Resolutions

### R1 — Canonical-Definitions Surface Authority

Root `canonical_definitions.md` is the Governance-tier orientation registry. Constitution Article 10 (`01_governance/constitution/10_canonical_definitions.md`) is the Content-tier (Constitution) definitional surface. Synchronization rule: where a concept is defined in both surfaces, Article 10's definition is the authoritative operational expression; the root file's entry compiles citation. Where a concept is defined in Doctrine only, Doctrine is authoritative; both surfaces reference the doctrinal source. New canonical definitions must enter through the Content tier first, then propagate to the root registry as clerical updates.

### R2 — Canonical Registry Status Taxonomy

Six status flags adopted: **Canonical**, **Provisional**, **Proposed**, **Conflicting**, **Undefined**, **Duplicate**. Definitions per Proposal 002 Resolution R2. Each registry entry carries exactly one status flag; the tie-breaking rule for cases where multiple flags appear to apply is declared in the Closing Decision Clarifications below (Clarification #8).

### R3 — Status-Change Rules

Transitions between status flags follow the rules declared in Proposal 002 Resolution R3. Clerical registry updates that register existing canonical concepts with established Content-tier sources do not require fresh Proposal-Review-Decision; they are recorded in the changelog under the authority of this Decision. The framing of R4 as PRD-authorized at the Resolution level (with per-entry registrations clerical under the umbrella) is declared in Clarification #3 below.

### R4 — Register Currently Unregistered Canonical Doctrinal Concepts

Nine canonical doctrinal concepts are registered using existing Doctrine sources only. The full list, with source citations, is incorporated from Proposal 002 Resolution R4. Status assigned to each entry: Canonical.

### R5 — Deprecate Predecessor Names

Four predecessor names are formally deprecated in the registry. The predecessor-to-current-name mapping is incorporated from Proposal 002 Resolution R5. Clarifications #4 and #7 below qualify the table entries.

### R6 — Disambiguate "Provisional"

Two technical usages of "Provisional" are declared (Epistemic Label per Spec 05; Governance Status per the R2 taxonomy). Registry context uses qualified forms where ambiguity could arise. Source files are not edited. Clarification #6 below records the relationship of R6 to Inventory I-A and to RB-007.

### R7 — Inventory Outputs

Inventories I-A (unanchored implementation concepts; 13 conceptual groups) and I-B (registry entries lacking authoritative definitions; 4 entries) are produced as registry-tracked observation artifacts. Placement of the inventories is declared in Clarification #5 below.

### R8 — Citation Paths for the Four Axes

Canonical citation paths declared for Cognition Scope, Product Identity, Trust Gradient, and Execution Depth, consistent with DL-034. Specific citations per Proposal 002 Resolution R8.

---

## Closing Decision Clarifications

The Framework 001A Review identified eight points of potential confusion that the closing Decision should clarify. Each clarification operates as narrative guidance for interpreting the Resolutions and binds future contributors and AI systems.

### Clarification #1 — Doctrine > Article 10 Precedence Rule for Substantive Definitional Conflicts

When a concept is defined in both Doctrine and Constitution Article 10 and the definitions substantively conflict, **Doctrine prevails** per the Conflict Resolution Model declared by DL-033. Article 10's definition operates as the operational expression where consistent with Doctrine. Where Article 10's definition diverges from Doctrine, the divergence is a Conflicting-status item and requires reconciliation through the appropriate downstream backlog item.

This clarification extends R1's three explicit cases (concept in both surfaces; concept in Doctrine only; new definitions through Content tier first) with the doctrinal-precedence rule for the fourth case (Doctrine vs Article 10 substantive disagreement).

### Clarification #2 — Migration of Existing "Established" Flags

Existing registry entries carry the legacy flags "Established" and "Established (split source)" rather than the new R2 taxonomy. The closing Decision authorizes an automatic clerical migration:

- All existing entries flagged **"Established"** (without qualifier) are reclassified as **"Canonical"**.
- All existing entries flagged **"Established (split source)"** are reclassified as **"Conflicting"**, except where Clarification #7 applies (Organizational Cognition Arc, which is reclassified as Duplicate via R5 extension).

The migration is clerical, applied as part of the registry update plan.

### Clarification #3 — R4 Authorization Framing

R4 is **PRD-authorized at the Resolution level** by this Decision. Each per-entry registration of the nine doctrinal concepts is executed as a clerical action under the umbrella authorization established here. This Decision sets the precedent: future registrations of already-canonical doctrinal concepts that have not yet been registered may proceed as clerical updates under the precedent of R4, without requiring a fresh Proposal-Review-Decision for each entry. Such future clerical registrations are recorded in the changelog with citation to DL-036 as the establishing precedent.

### Clarification #4 — DL-016 Qualified as Stated (Grandfathered)

In Resolution R5's deprecation table, the Intelligence Visibility Doctrine → Progressive Visibility deprecation is anchored on DL-016. DL-016 is a Stated decision grandfathered under DL-032 and has not been promoted to Ratified status under Framework 001/001A. The deprecation is supported by the substantive doctrinal equivalence between Doctrine 11 (Intelligence Visibility Doctrine section) and Constitution Article 25 (Progressive Visibility); the formal anchor is therefore "Stated (grandfathered per DL-032); substantively aligned with Article 25." The registry entry should reflect this qualification.

### Clarification #5 — Placement of Inventories I-A and I-B

Inventories I-A and I-B are placed **inline within `ontology_registry.md`** as named sections under the existing structure. Specifically:

- Inventory I-A is added as a new section titled "**Inventory I-A — Unanchored Implementation Concepts**" near the end of the file, after the existing "Concepts Used But Not Registered" section.
- Inventory I-B is added as a new section titled "**Inventory I-B — Registry Entries Lacking Authoritative Definitions**" immediately following I-A.

Inline placement is chosen to keep the inventory visible alongside the registry it informs, and to avoid introducing a new file or subdirectory without a separate Decision. The inventories are open and updateable; future Decisions may add or remove items via clerical changelog entries.

### Clarification #6 — Relationship Among R6, I-A Item 1, and RB-007

The three references to "Epistemic Label" types and "Provisional" operate at distinct layers and are not contradictory:

- **R6 (Disambiguate "Provisional"):** Registry-side declaration that "Provisional (Epistemic Label)" and "Provisional (Governance Status)" are distinct technical usages. Operates only in registry surfaces.
- **Inventory I-A item 1 (Epistemic Label additional types):** Flags the four additional labels in Spec 05 (Unknown, Provisional, Weakly Supported, Validated) as unanchored at the doctrinal layer. This is an inventory observation, not a disposition.
- **RB-007 (Epistemic Object Types vs Epistemic Labels):** Reserved for the substantive reconciliation of Spec 05's nine "Label" types against Doctrine 03's five canonical Epistemic Object Types. The disposition of RB-007 will determine the final status of Spec 05's additional labels.

This Decision does not anticipate or constrain RB-007's outcome. R6 and I-A item 1 are upstream observation artifacts that feed RB-007.

### Clarification #7 — R5's Organizational Cognition Arc Deprecation Extends the Existing Reframing

The existing `canonical_definitions.md` entry for Organizational Cognition Arc carries a reframing note added per CHG-019 (under DL-034) indicating the concept is reframed as the Cognition Scope axis. R5's deprecation does not introduce a new status; it **formally extends the existing reframing into a full Duplicate-status deprecation**. The reframing note is replaced by a Duplicate-status entry pointing to Cognition Scope as the canonical name. This is a continuation of the DL-034 reframing, not a supersession of it.

### Clarification #8 — Tie-Breaking Rule for Status-Flag Exclusivity

When a registry entry could plausibly carry multiple status flags from R2, the following priority order applies (higher priority prevails):

1. **Conflicting** — definitions disagree across canonical sources; reconciliation pending.
2. **Undefined** — no defining statement in any source; doctrinal stub required.
3. **Proposed** — referenced as if canonical but lacking unified defining statement.
4. **Provisional** — defining statement exists but not yet ratified to final status.
5. **Duplicate** — synonym of a Canonical concept; deprecation applies.
6. **Canonical** — stable; no governance action required.

The rule orders flags by the urgency of governance action required. Higher-priority flags signal more immediate governance work. Where the most informative flag is ambiguous between two non-Canonical flags, the higher-priority flag in this list prevails. A registry entry that would otherwise be Canonical but is also a synonym (Duplicate) carries the Duplicate flag in the synonym's entry, with the canonical name's entry remaining Canonical.

---

## Effects on Existing Backlog

- **RB-001** transitions from Proposed to **Closed**. Disposition: Accepted with Conditions; full disposition recorded in this document.
- **RB-004** (Doctrine Stubs) remains Open. Inventory I-A produced by this Decision feeds RB-004 as input. RB-001's closure does not advance RB-004's substantive work, but provides the registry framework within which RB-004 will operate.
- **RB-006, RB-007, RB-008, RB-009** (ontology reconciliations) remain Open. Their substantive scope is unchanged. The registry framework established here clarifies the surfaces those items will modify when ratified.
- **RB-012, RB-013, RB-014, RB-015, RB-016, RB-017, RB-018** remain Open. Inventory I-B and I-A feed these items as appropriate.
- **RB-020** (Populate Root README and CLAUDE.md) remains Open. Not directly affected.
- **RB-005** (Layer Promotion and Citation Rule) remains Partially Closed. R8's citation paths complement DL-033's promotion model; residual citation requirements for Implementation Specs remain.

No new backlog entries created.

## Effects on Canonical Surfaces

### canonical_definitions.md (root)

- Header updated to declare the R1 Surface Authority rule.
- Status section updated to declare the R2 taxonomy.
- Existing "Established" entries automatically migrated to "Canonical" per Clarification #2.
- Existing "Established (split source)" entries automatically migrated to "Conflicting" per Clarification #2, except Organizational Cognition Arc per Clarification #7.
- Nine new entries added per R4.
- Deprecation entries added for four predecessor names per R5 with Clarifications #4 and #7 qualifications applied.
- Provisional disambiguation note added per R6.
- Axis citation paths added per R8.

### ontology_registry.md (root)

- Header updated to reference R1.
- Status section updated to declare R2 taxonomy.
- Same migration as canonical_definitions.md per Clarification #2.
- Nine new entries added per R4 (with planes appropriately assigned).
- Deprecation entries added per R5.
- Inventory I-A placed inline per Clarification #5.
- Inventory I-B placed inline per Clarification #5.
- Axis entries updated per R8.

### Constitution Article 10

**Not edited.** R1 operates without amending Article 10. The Surface Authority rule declares Article 10's status; the Article body is unchanged.

### Doctrine 01–11

**Not edited.** R4 registrations cite existing doctrinal sources; no doctrine is amended.

### Implementation Specifications

**Not edited.** Inventory I-A names spec-layer concepts; the Specs themselves are unchanged. R6 disambiguation is registry-side only.

## Effects on DL-033, DL-034, DL-035

- **DL-033** is unaffected as a Decision. The Surface Authority rule in R1 implements DL-033's two-tier architecture for the canonical-definitions surfaces. The Doctrine > Article 10 precedence rule in Clarification #1 reaffirms DL-033's Conflict Resolution Model.
- **DL-034** is unaffected. The deprecations in R5 (for Strategic Arc, Organizational Cognition Arc, Trust Evolution) cite DL-034 as the ratifying Decision. The axis citation paths in R8 formalize DL-034's canonical sources.
- **DL-035** is unaffected. The Constitutional Principles Draft remains relocated to Source Material. No interaction with this Decision.

## Affected Artifacts

- `canonical_definitions.md` (root) — updated per Effects on Canonical Surfaces above.
- `ontology_registry.md` (root) — updated per Effects on Canonical Surfaces above.
- `01_governance/decisions/decision_log.md` — DL-036 entry appended.
- `01_governance/changelog/changelog.md` — CHG-026 through CHG-034 appended.
- `01_governance/backlog/revision_backlog.md` — RB-001 closed.
- `01_governance/decisions/rb_001_disposition.md` — this document, created.

No Doctrine, Constitution, Implementation Specification, Manifest, Framework, REPOSITORY_ARCHITECTURE.md, or other Governance-tier file is affected.

## Status

**Ratified.** This disposition is operative as of 2026-05-29.

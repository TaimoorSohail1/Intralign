# Proposal 000 — Disposition Document

## Decision Identifier

DL-033

## Title

Adopt the Doctrine-Centered Repository Architecture per Proposal 000

## Disposition

**Accepted**

## Date Ratified

2026-05-29

## Authorizing Proposal

Proposal 000 — Canonical Repository Architecture

## Repository Owner Principles

The architecture is selected on the basis of three principles supplied by the repository owner:

1. Doctrine is the ultimate source of truth for OSLO.
2. The Constitution is a distilled operational expression of Doctrine.
3. Preserving original understanding and intent is more important than maximizing governance flexibility or minimizing governance overhead.

These principles together require a doctrine-centered architecture: Doctrine is canonical and foundational; Constitution derives from and operationalizes Doctrine; preservation of meaning is privileged over procedural convenience.

## Rationale

The doctrine-centered architecture is the only architecture among the Proposal 000 options that satisfies all three principles. It places Doctrine at the apex of the Content tier and treats Constitution as a derived operational expression. It separates the Governance tier from the Content tier so that procedural objects cannot override doctrinal content. It accepts the classification and reconciliation cost that this fidelity requires.

Alternative options (Constitution-Supreme, Doctrine-Constitution Peers, and Unified Precedence Ladder) each violate at least one of the owner's principles. Their rejection is recorded in the Rejected Options section.

---

## Repository Architecture

The repository is organized into two parallel object tiers.

**Content tier.** Carries the substantive knowledge of OSLO. Contains the canonical content from which all assertions about OSLO derive authority.

**Governance tier.** Carries the procedural objects that govern how Content evolves. Does not assert doctrine. Does not declare positions about OSLO; declares positions about how the repository changes.

The two tiers are functionally distinct. Governance does not override Content. Content does not dictate governance procedure. Cross-tier disputes are resolved through Proposals under the operative Governance Framework.

---

## Content Object Model

The Content tier contains four object classes, ordered by precedence:

1. **Doctrine.** Foundational conceptual content. The primary canonical layer.
2. **Constitution.** Distilled operational expression of Doctrine.
3. **Implementation Specifications.** Derived expressions applied to specific surfaces, workflows, components, and states.
4. **Source Material.** Non-canonical. Historical record and interpretive substrate.

Precedence within the Content tier: Doctrine > Constitution > Implementation Specifications. Source Material sits outside the canon.

Subsystems are sub-categories within the Content tier and are addressed in the Subsystem Treatment section.

---

## Governance Object Model

The Governance tier contains seven object classes:

1. **Manifest.** Orientation charter for contributors and AI systems.
2. **Governance Frameworks.** Procedural rules governing the lifecycle.
3. **Governance Proposals.** Proposed canonical changes.
4. **Reviews.** Analyses produced under the Framework 001A output schema.
5. **Decisions.** Ratified outcomes recorded in the Decision Log.
6. **Revision Backlog.** Queue of identified work pending Proposal.
7. **Changelog.** Record of canonical changes authorized by Decisions.

Within the Governance tier, Frameworks carry procedural authority. The Manifest provides orientation but does not override Frameworks. Process objects are governed by Frameworks.

---

## Role of Doctrine

Doctrine is the ultimate source of truth for OSLO. All canonical claims derive authority from Doctrine. Doctrine is what is preserved across changes in operational expression.

Modifications to Doctrine require Proposal-Review-Decision under the operative Framework. Doctrinal supersession is the highest-impact governance act.

Where Doctrine is silent on a concept the system depends on, the absence is itself a governance concern and is tracked in the Revision Backlog as a doctrinal-stub candidate.

---

## Role of Constitution

The Constitution is the distilled operational expression of Doctrine. Constitutional Articles articulate doctrinal positions for UX, governance, and operational application. Articles inherit authority from their doctrinal grounding.

Where a Constitutional Article expresses a position not anchored in Doctrine, the Article is provisional and subject to doctrinal review through a Proposal.

Where a Constitutional Article conflicts with Doctrine, the conflict resolves in favor of Doctrine. The Article must be amended, or the Doctrine must be clarified through a Proposal. The resolution may not be a unilateral Constitutional override of Doctrine.

---

## Role of Implementation Specifications

Implementation Specifications are derived expressions of Doctrine and Constitution applied to specific surfaces, workflows, components, and states. They are subordinate to both Doctrine and Constitution.

Concepts introduced at the Implementation Spec layer without doctrinal or constitutional anchoring are provisional. They remain in force operationally pending Proposal-Review-Decision.

Implementation Specifications should cite the doctrinal or constitutional source they implement. Where citation is not yet possible because the source is absent, the gap is tracked in the Revision Backlog.

---

## Role of Governance Frameworks

Governance Frameworks are the procedural authority over Content tier evolution. They declare the lifecycle, ratification rule, supersession rule, conflict resolution rule, review states, output schemas, and authority constraints.

Frameworks do not assert doctrine. They govern process, not content.

A Framework that conflicts with Doctrine resolves in favor of Doctrine. Doctrine governs what is preserved; Frameworks govern how preservation occurs.

Amendments to Frameworks require Proposal-Review-Decision under the currently operative Framework.

---

## Role of Manifest

The Manifest is the orientation charter for contributors and AI systems. It describes the repository, its purpose, and its current state.

The Manifest carries non-doctrinal force. Substantive claims about OSLO in the Manifest — including the OSLO acronym expansion, the "Lifecycle" framing, and the substantive scope of any Governance Principle the Manifest articulates — are advisory unless promoted to the Content tier via Proposal-Review-Decision.

The Manifest sits within the Governance tier as orientation. It does not sit above Doctrine. It does not sit above Frameworks. Authority resides in Content; the Manifest exists to onboard contributors to that authority.

---

## Role of Source Material

Source Material is non-canonical. It preserves the historical record of ideation, design conversations, and source documents that informed the canonical layers.

Source Material may not be cited as authoritative. Where canonical content is ambiguous, Source Material may provide interpretive context, but the resolution of ambiguity is a governance act requiring a Proposal, not a citation of Source Material as authority.

Source Material continues to be valuable as historical traceability and as a substrate for future doctrinal extraction.

---

## Subsystem Treatment

Subsystems are sub-categories within the Content tier. Each subsystem must anchor to canonical content by declaring its parent Content class:

- A subsystem's doctrinal scope is recorded within Doctrine.
- A subsystem's constitutional articulation is recorded within Constitution.
- A subsystem's implementation specifications are recorded within Implementation Specifications.

A subsystem may exist at multiple Content layers if scope warrants. A subsystem may not exist solely at the Implementation Spec layer unless it is explicitly scoped as provisional pending doctrinal anchoring.

`04_project_mri` is acknowledged as a subsystem whose doctrinal scope is incomplete. Scoping is tracked in the Revision Backlog.

Promotion of a subsystem to a top-level domain requires a Proposal demonstrating doctrinal scope sufficient to warrant the promotion.

---

## Conflict Resolution Model

Conflicts are resolved by tier and by precedence within tier.

**Within the Content tier.** Doctrine > Constitution > Implementation Specifications. Conflicts surface as Proposals; resolution favors the higher tier.

**Within the Governance tier.** Frameworks govern process; the Manifest provides orientation; process objects are governed by Frameworks. Conflicts resolve via Proposal under the operative Framework.

**Cross-tier.** Governance objects do not override Content. Content does not dictate Governance procedure. Cross-tier disputes resolve via Proposal. A Framework conflict with Doctrine resolves in favor of Doctrine.

**Direct edits prohibited.** Per Framework 001's Conflict Resolution Rule, conflicts are resolved through Proposals rather than direct edits to canonical content.

---

## Concept Promotion Model

Concepts originate in Source Material (informally), in Implementation Specifications (during specification work), or directly in Doctrine (when foundational scope is identified at origin).

A concept at the Implementation Spec layer that lacks doctrinal or constitutional grounding is provisional.

**Promotion paths:**

- Implementation Spec → Constitution. Requires a Proposal that demonstrates the Constitutional Article the concept would form and the doctrinal grounding it requires.
- Constitution → Doctrine. Requires a Proposal that demonstrates foundational scope.
- Doctrine → Constitution. Requires a Proposal that articulates the doctrinal position in operational form and demonstrates consistency with the source.

**Skipping layers.** A concept may not skip Content-tier layers without explicit justification in the Proposal.

**Manifest claims.** Substantive claims in the Manifest are not concepts in the Content tier. They may be cited in a Proposal but cannot themselves be promoted.

---

## Rejected Options and Reasoning

**Constitution-Supreme.** Rejected. Inverts Principle 1 by making Doctrine subordinate to a derived layer.

**Doctrine-Constitution Peers.** Rejected. Does not honor Principle 2; would make Constitution co-canonical rather than a derived operational expression of Doctrine.

**Unified Precedence Ladder.** Rejected. Violates Principle 1 by placing the Manifest and Governance Frameworks above Doctrine. Also conflicts with Principle 3 by elevating the Manifest's substantive claims into doctrinal weight, distorting original understanding rather than preserving it.

---

## Tradeoffs Accepted

The owner's principles privilege preservation of original understanding over reduction of governance overhead. The following tradeoffs are accepted as the cost of fidelity.

- The Manifest weakens substantially as a normative source. Substantive claims become advisory.
- Doctrine bears the burden of authoritativeness even where it is under-specified.
- Constitutional drift remains possible; Articles may be challenged on doctrinal grounds.
- Two-tier separation creates ongoing classification cost for new artifact types.
- Continued reconciliation work at the Doctrine-Constitution boundary.

---

## Backlog Items Resolved

- **RB-019** (Place the Manifest in the Precedence Hierarchy). Closed by placing the Manifest in the Governance tier as orientation with non-doctrinal force.
- **RB-011** (Lifecycle Terminology Tension). Closed by the Manifest's non-doctrinal status; the "Lifecycle" term carries no doctrinal weight.

## Backlog Items Partially Resolved

- **RB-005** (Layer Promotion and Citation Rule). Precedence hierarchy declared. Concept promotion model declared. Residual scope (citation requirements for Implementation Specs) remains.
- **RB-010** (Constitutional Principles Draft vs Constitution Articles). The Draft (Doctrine 12) sits at the Doctrine layer; Constitution Articles sit at the Constitution layer. Doctrinal precedence applies. The Draft's status as a draft creates a residual instability that requires a follow-up Proposal to either ratify or formally retire the Draft. The instability is acknowledged in the header of Doctrine 12 per the pre-ratification minimum remediation.

## Backlog Items Remaining Open

The following items remain open and continue to operate under the ratified architecture. No new entries are created in this disposition.

- RB-001 (Canonical Registry Consolidation)
- RB-003 (Progression Model Reconciliation)
- RB-004 (Doctrine Stubs for Under-Specified Systems)
- RB-006 (Outcome Integrity States)
- RB-007 (Epistemic Object Types vs Epistemic Labels)
- RB-008 (Confidence Drivers)
- RB-009 (Override State Model vs Severity Tiers)
- RB-012 (Collaboration Role Model)
- RB-013 (Attention Queue Canonical Definition)
- RB-014 (Artifact Canonical Definition)
- RB-015 (Project MRI Doctrinal Scoping)
- RB-016 (Confidence Scoring Methodology)
- RB-017 (Assumption Expiration Semantics)
- RB-018 (Policy Grammar Doctrine)
- RB-020 (Populate README and CLAUDE.md)

## Proposals Absorbed

- **Proposal 001** (Repository Hierarchy). Closed as absorbed. All seven candidate questions in Proposal 001 are answered by this disposition.

---

## Resulting Repository Actions

1. Record DL-033 in `07_governance/decision_log.md`.
2. Place this disposition document at `07_governance/proposal_000_disposition.md`.
3. Close Proposal 001 as absorbed (recorded in the decision log entry and changelog; no separate file modified).
4. Update `07_governance/revision_backlog.md` to mark RB-019 and RB-011 as Closed, RB-005 and RB-010 as Partially Closed.
5. Place `REPOSITORY_ARCHITECTURE.md` at the repository root.
6. Replace pre-ratification DL-XXX placeholders with DL-033 in `repository_manifest.md`, `canonical_definitions.md`, `ontology_registry.md`, and `01_doctrine_ontology/12_constitutional_principles_draft.md`.
7. Record corresponding entries in `07_governance/changelog.md`.

## Status

**Ratified.** This disposition is operative as of 2026-05-29.

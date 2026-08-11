# RB-043 — Issue classification + load-bearing criteria (durable, enforceable model)

- **Opened:** 2026-08-09 · **Source:** owner (R&D working session) · **Status:** ✅ **CLOSED — ratified 2026-08-09 → DL-209** (proposal `GOVERNANCE_PROPOSAL_load-bearing-sensitivity-architecture.md`; decision `canon/decisions/DL-209_…md`). Realization scoping is downstream.
- **Class:** A (doctrine) + B (architecture).

## Trigger
Owner observed (1) some issue cards offer an evidence CTA while others don't, and (2) inconsistency even within Grounding — e.g. the "Catering headcount" card is tagged Grounding, its basis is "OSLO's inference," yet the primary action is "Apply this fix" with evidence demoted. Root cause: classification and the resolution affordance are set ad-hoc (`primaryMove`), decoupled from the pillar, allowing a fix to (risk) raising Grounding — manufactured confidence, the DL-197 failure.

## Ask
A **clear, thoughtful, durable, enforceable** model for classifying issues and gating what is load-bearing, so issues are classified properly and can be resolved properly — critically challenged for durability and rationale before adoption.

## Outcome (this session)
Five first principles settled by critical analysis (Roots 1–5); the load-bearing criterion refined to **magnitude-of-sensitivity ≥ calibrated-threshold** (two-sided; catches false confidence) with two named residues; the honesty invariant sharpened to **only verify moves Grounding**; and a layered architecture (L0 graph → L1 deterministic sensitivity → L2 thin learnable calibration → L3 static classification table → L4 optional feedback) with a "quarantine the fuzziness" thesis and cold-start-safe sequencing. See the proposal.

## Next
Owner ratification of the roots + architecture → DL-209; then realization scoping (build) and the finding-type → (pillar, resolution) table population as a downstream task. No R2 freemium-build impact.

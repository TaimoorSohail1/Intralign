# DL-084 — R2 candidate-epic phase/tier placement + Foundational-Architecture-in-Alpha principle

- **Date:** 2026-06-28 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (product-roadmap / build-sequencing orientation; non-doctrinal)

- **Source:** Owner direction 2026-06-28 — bind the phase/tier placement of the R2 candidate epics and ratify the build-sequencing exception that lets foundational architecture be laid early. Proposal: `PROPOSAL_R2_PHASE_TIER_PLACEMENT_DRAFT.md`; backlog: RB-032. Grounded in DL-076 (Alpha/Beta release model), DL-074 (tier ladder), DL-083 (execution monitoring → Beta/Tier-3), DL-081 (Layer-Before-Depth), DL-047 (advisory-only), CHG-064 (R1 scope); reflected in `RELEASE_2_BACKLOG_CANDIDATES.md` (Phase & tier placement note).
- **Layer:** Product scope / roadmap + build-sequencing orientation (`10_product`). **Non-doctrinal.** Binds candidate-index placements; introduces no capability, doctrine, or responsibility.

## Decision

**1. R2 candidate-epic phase/tier placement.**
- **Execution Intelligence (R2-C: monitoring → operational confidence → simulations/sync) → Beta.** Does not begin until the Beta phase. (C1 execution monitoring is already Beta/Tier-3 per DL-083; this binds the dependent C2/C3 to Beta as well.)
- **Team Collaboration depth (R2-D) → Team tier (Tier 4).** Does not begin until the Team tier.
- **Governance & Authority (R2-E) → Beta.** Does not begin until the Beta phase (largest, most architectural epic; likely multi-release).

**2. Foundational-Architecture-in-Alpha principle (the durable rule).** *Architectural foundation* work for a phase-/tier-gated capability **may be performed earlier — in Alpha (R2) — when laying it early measurably reduces later effort or complexity.** Build the seams/abstractions now; ship the user-facing capability at its gated phase/tier. This is **build-sequencing, not capability activation**: any such early foundation must remain **advisory-only / non-activating** (DL-047), **specified-but-inactive**, and route through normal scoping (and a DL where it touches architecture). Sibling to **DL-081 (Layer-Before-Depth)** — foundation/altitude first, depth at its proper phase.

## Conditions
1. **Phase/tier gating governs the user-facing capability**, not necessarily its foundational architecture (see §2).
2. **Advisory-only preserved (DL-047).** Early foundation is non-activating and specified-but-inactive; it never ships behavior ahead of the capability's gated phase/tier.
3. **Justified, not default.** The Alpha-foundation exception applies only where early placement **measurably** reduces later effort/complexity; it is not a license to pull gated capabilities forward. Each instance routes through scoping (+ DL where architectural).
4. **R1-safe.** Does not alter R1 scope (CHG-064). Placements apply R2+ / Beta as stated.
5. **Consistent with canon.** Aligns with DL-076 (Alpha/Beta), DL-074 (tiers), DL-083 (exec monitoring → Beta), DL-081 (Layer-Before-Depth). The `RELEASE_2_BACKLOG_CANDIDATES.md` Phase & tier placement note is the candidate-index reflection of this decision.

## Supersedes / Amends
None superseded. Additive: binds the phase/tier placement recorded as candidate annotations in `RELEASE_2_BACKLOG_CANDIDATES.md`, and ratifies the Foundational-Architecture-in-Alpha build-sequencing principle. Consistent with DL-074/076/081/083.

## Provenance
Owner working session, 2026-06-28: owner directed that Execution Intelligence and Governance & Authority do not begin until Beta, Team Collaboration depth not until the Team tier, and that foundational architecture beneficial to lay early may be done in Alpha (R2) to save later effort/complexity. AI drafted and recommended (Framework 001A); the owner ratifies. Numbered at landing under the DL-065 records discipline.

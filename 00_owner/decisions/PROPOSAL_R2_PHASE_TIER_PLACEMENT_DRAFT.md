# Proposal — R2 candidate-epic phase/tier placement + Foundational-Architecture-in-Alpha principle

**Document Type:** Governance Proposal (Framework 001 / 001A) — **plan only; nothing ratified** · **Status:** **DRAFT · Pending Owner Ratification** · **Date:** 2026-06-28
**Origin:** Owner direction (working session, 2026-06-28).
**Backlog:** RB-032. **Draft record:** `records/DL-084-r2-phase-tier-placement.md`. **Reflected in:** `00_owner/backlog/RELEASE_2_BACKLOG_CANDIDATES.md` (Phase & tier placement note).
**Layer:** Product scope / roadmap + build-sequencing orientation (`10_product`). **Non-doctrinal.**

---

## Context

The R2 candidate index gathered deferred capabilities but did not bind *when* each begins. The owner has set the phase/tier gates and a build-sequencing exception. Most of this is consistent with existing canon; the new, owner-directed parts are the Team-tier gate for collaboration depth, the Beta gate for Governance & Authority, and the general Foundational-Architecture-in-Alpha principle.

## Proposed decision (content)

1. **Phase/tier placement:** Execution Intelligence (R2-C) → **Beta**; Team Collaboration depth (R2-D) → **Team tier (Tier 4)**; Governance & Authority (R2-E) → **Beta**.
2. **Foundational-Architecture-in-Alpha:** architectural foundation for a gated capability **may be laid early in Alpha (R2) where it measurably reduces later effort/complexity** — advisory-only, non-activating, specified-but-inactive; routes through scoping (+ DL where architectural). Sibling to DL-081.

## Findings

1. **Mostly consistent with canon; partly new.** R2-C→Beta already follows from DL-083; R2-D→Team-tier follows DL-074's tier intent; R2-E→Beta is the natural placement for the largest architectural epic. The **Foundational-Architecture-in-Alpha principle** is the genuinely new, durable rule worth ratifying.
2. **Resolves a planning ambiguity** — the index listed these under "R2" labels without phase gates; this binds them.
3. **Preserves epistemic invariants.** Early foundation stays advisory-only / non-activating (DL-047); no capability ships ahead of its gate.

## Concerns

1. **Exception could be over-used.** "Lay it early" must be justified by measurable effort/complexity reduction, not convenience — else gated capabilities creep into Alpha. Condition 3 binds this.
2. **Non-activation discipline.** Early architecture must remain specified-but-inactive; QA/observability must prove no behavior ships early. Realization concern, flagged for the relevant scoping/DL.
3. **Index vs binding.** The placements were recorded as non-binding candidate annotations (PR #78); this proposal elevates them to canon via the DL.

## Dependencies

- **Consistent with / builds on:** DL-076 (Alpha/Beta), DL-074 (tiers), DL-083 (exec monitoring → Beta), DL-081 (Layer-Before-Depth), DL-047 (advisory-only), CHG-064 (R1 scope).
- **Reflected in:** `RELEASE_2_BACKLOG_CANDIDATES.md` Phase & tier placement note.
- **Routes to later scoping:** each early-foundation instance (per §2) via its own scoping item / DL where architectural.

## Recommendation

**Adopt** the three placements and the Foundational-Architecture-in-Alpha principle as product-roadmap / build-sequencing canon, non-doctrinal, additive. No engineering action required at ratification; specific early-foundation work is authorized per-instance through scoping.

## Status

**DRAFT — pending owner ratification.** On approval: land via the Founder Console "Approve & Land" / `dl-land` workflow (stamps the DL number, regenerates the index, appends the changelog, opens the PR), committing the record + RB-032 alongside.

---
*Owner decision options: **(A)** adopt as proposed (recommended; written for A); **(B)** adopt placements only, defer the foundational-architecture principle; **(C)** defer. AI drafted and recommends; only the owner ratifies (Framework 001A).*

# Proposal — Execution-monitoring tier placement & phase + capability tier split (amends DL-082, extends DL-074)

**Document Type:** Governance Proposal (Framework 001 / 001A) — **plan only; nothing ratified** · **Status:** **DRAFT · Pending Owner Ratification** · **Date:** 2026-06-28
**Origin:** Owner direction (working session, 2026-06-28) — confirm the three-way capability tier split and move execution monitoring from Alpha exit to Beta.
**Backlog:** RB-029. **Draft record:** `records/DL-083-execution-monitoring-tier-and-phase.md`. **Artifact amended:** `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a.
**Layer:** Product scope / roadmap + monetization orientation (`10_product`). **Non-doctrinal**; amends DL-082, extends DL-074.

---

## Context

Aligning product tiering with the DL-082 Alpha exit criteria surfaced that "vendor support for planning" and "execution visibility" had been collapsed into one idea. They are **three distinct capabilities** with different directions and cost profiles: (1) **Export-Share-Out** (read-only orientation share, outbound, viral — G4/Wave E); (2) **plan export → execution tool** (outbound push of the plan, cheap, one-shot); (3) **execution monitoring** (inbound outcome ingest + closed loop, continuous, costly). DL-082's "execution visibility operational" gate is capability (3) — the inbound one. The owner's Tier-2 rationale ("export plans into the execution tool without upgrading") describes capability (2) — the outbound one.

Separately, the Tier-3 execution-monitoring build lands in the **Beta** phase, so it cannot serve as an **Alpha** exit gate.

## Proposed decision (content)

**1. Capability tier split (extends DL-074):** Export-Share-Out = Free/no-account; plan export → execution tool = **Tier 2 / Basic**; execution monitoring = **Tier 3 / Pro+** (Team/Enterprise inherit), built in Beta.
**2. Phase move (amends DL-082):** execution monitoring is a **Beta** capability; **removed from Alpha exit**. Amended Alpha exit = (1) build/prove; (2) value by retention; (3) ≥ 2 governed planning sources; (4) 50+ users (§20).
**3. Alpha validates engagement; Beta validates outcome impact.**
**4. Plan export-out is a distinct, not-yet-scoped capability** — placed at Tier 2 but routed to its own scoping (tools, one-way vs round-trip, task mapping).

## Findings

1. **Resolves a real contradiction.** DL-082 gated Alpha graduation on a capability whose build lands in Beta; the move makes the gate satisfiable.
2. **Separates conflated capabilities.** Direction (outbound vs inbound) and cost (one-shot vs continuous polling) differ sharply; tiering them together would have mispriced both and eroded the Pro upsell DL-074 protects.
3. **Consistent with canon.** Aligns with Layer-Before-Depth (DL-081, read-only visibility permitted-not-required in Alpha), the DL-076 R1–R5 ladder, and DL-074's "monitoring = Pro+ capacity add-on" framing and the 2026-06-05 tier-progression note.
4. **Preserves the moat logic.** Execution monitoring (the outcome-corpus feeder) stays Pro+, fed by the users who actually track delivery.

## Concerns

1. **Alpha loses the outcome-truth instrument.** Value-validation in Alpha = behavioral retention (engagement), not measured outcome lift; outcome-impact validation shifts to Beta. Owner-accepted trade; flagged so Alpha success isn't over-read as "proven outcome improvement."
2. **Corpus-growth trade-off.** Keeping monitoring at Pro+ narrows who feeds the outcome corpus vs. a wider-tier placement. Owner weighed margin/upsell over corpus breadth; revisit if corpus growth lags.
3. **Plan export-out scope risk (Anti-Assumption).** Capability (2) is undefined in canon (G4 is share-out). Placing it at Tier 2 must not be read as authorizing a build; it needs its own scoping decision.
4. **"Real per-platform depth" / plan-export task-mapping** definitions remain product-scope authorship at realization.

## Dependencies

- **Amends:** DL-082 (`RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a — execution monitoring out of Alpha; relocate to Beta).
- **Extends:** DL-074 (capability tier placement; consistent with the 2026-06-05 tier-progression note).
- **Constrained by (unchanged):** DL-047 (advisory-only), DL-081 (Layer-Before-Depth), CHG-064 (R1 scope), §20 graduation gate.
- **Routes to later scoping:** plan export-out capability (tools, semantics, task mapping); execution-monitoring realization (which platforms, Beta build, Calibration §4c tier rows).

## Recommendation

**Adopt** the three-way tier split and the Alpha→Beta phase move for execution monitoring, encoded in §3a, amending DL-082 and extending DL-074. Keep the §20 gate and R1 scope unchanged. Route plan export-out and monitoring realization to their own scoping.

## Status

**DRAFT — pending owner ratification.** On approval: land via the Founder Console "Approve & Land" / `dl-land` workflow (stamps the DL number, regenerates the index, appends the changelog, opens the PR), committing the §3a amendment + RB-029 + this proposal alongside.

---
*Owner decision options: **(A)** adopt as proposed (recommended; written for A); **(B)** adjust a tier placement or keep a light read-only visibility proxy in Alpha; **(C)** defer. AI drafted and recommends; only the owner ratifies (Framework 001A).*

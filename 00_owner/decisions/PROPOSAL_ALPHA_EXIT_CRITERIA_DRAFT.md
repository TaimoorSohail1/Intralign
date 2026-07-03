# Proposal — Alpha Exit Criteria (specify "proven" for Alpha→Beta; amends DL-076)

**Document Type:** Governance Proposal (Framework 001 / 001A) — **plan only; nothing ratified** · **Status:** **Adopted (DL-082)** · **Date:** 2026-06-28
**Origin:** Owner direction (working session, 2026-06-28) — the Alpha phase's three pillars are exit criteria; capture and bind them by amending DL-076's release-ladder artifact.
**Backlog:** RB-028. **Draft decision record:** `records/DL-082-alpha-exit-criteria.md`. **Artifact amended:** `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` (new §3a).
**Layer:** Product scope / roadmap orientation (`10_product`). **Non-doctrinal**; amends DL-076.

---

## Context

DL-076 established the Alpha→Beta model as two gate types — **build/prove** (the engine works) and **graduation/outcome** (§20: 50+ users + engagement) — and stated both must hold to advance. The owner has now specified the Alpha phase's three substantive pillars — **project-intelligence value validation, planning-vendor breadth, execution visibility** — as **exit criteria**. These principally enrich the "**proven**" side of the DL-076 model: Alpha must prove not just that the engine works, but that it delivers recognized value, travels across planning sources, and closes the outcome loop. The §20 engagement gate is unchanged.

## Proposed exit criteria (the decision content)

Advancing Alpha → Beta requires **all** of:

1. **Build / prove gates pass** — Phase 1/2 (unchanged, DL-076 §3).
2. **Value validated** — by **behavioral retention / repeat use** (unprompted re-runs on real projects); sentiment alone does not pass.
3. **Planning-vendor breadth** — **≥ 2** governed platforms, each with real per-platform depth (not shallow connectors).
4. **Execution visibility operational** — **read-only outcome ingest** (≥ 1 platform) **+ closed feedback loop**; strictly observational (DL-047); **drift-surfacing deferred to Beta+**.
5. **Audience / engagement reached** — **50+ users + engagement (§20)**, unchanged (DL-076).

## Findings

1. **Amends, not supersedes, DL-076.** Preserves the two-axis model and the build/prove-vs-graduation distinction; specifies the "proven" side and leaves §20 intact. Same non-doctrinal roadmap-orientation genre.
2. **Coherent with the moat thesis.** The three owner pillars map to value, altitude/neutrality, and the feedback signal — the assets the defensibility analysis identified as durable.
3. **Internally consistent.** The ≥ 2 breadth threshold and the depth-deferral (drift → Beta+) align with the in-flight Layer-Before-Depth principle (`DL-081-roadmap-layer-sequencing`).
4. **Falsifiable.** Each criterion now carries a pass/fail bar — required for an exit gate (behavioral retention; ≥ 2 platforms; ingest + closed loop).

## Concerns

1. **Cross-record consistency.** Threshold (≥ 2) and scope (drift deferral) must stay reconciled with the Layer-Before-Depth record; if one changes at ratification, reconcile both. (Condition 4 of the draft record.)
2. **"Real per-platform depth" needs an operational definition** at realization time to avoid the shallow-connector trap; left to product-scope authorship, not fixed here.
3. **Buyer vs user.** Criterion 2 validates *user* behavioral retention; the buyer/willingness-to-pay assumption (and "neutrality matters to buyer") remain monitored assumptions (per the defensibility memo), not Alpha exit gates by this decision. Owner may add later.
4. **Advisory-only drift risk.** Execution visibility must remain strictly observational; "operational" must not creep into execution management. (Condition 2.)

## Dependencies

- **Amends:** DL-076 (`RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a).
- **Constrained by (unchanged):** DL-047 (advisory-only), §20 graduation gate, CHG-064 (R1 scope), Positioning §9.
- **Consistent with:** `DL-081-roadmap-layer-sequencing` (Layer-Before-Depth), DL-075/DL-076 pattern.
- **Sequencing:** lands after the in-flight canon PR (DL-080) per DL-065 R3. Recommend landing **after** Layer-Before-Depth so the ≥ 2 threshold is set there first; either order is acceptable since both are owner-ratified together.

## Recommendation

**Adopt the Alpha exit criteria** as an amendment to DL-076, encoded in `RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a, with the owner-set thresholds (≥ 2 vendors; behavioral retention/repeat use; read-only ingest + closed loop) and drift-surfacing deferred to Beta+. Keep the §20 engagement gate unchanged.

## Status

**Adopted (DL-082).** Nothing ratified. On approval: land via the Founder Console "Approve & Land" / `dl-land` workflow (stamps the DL number, regenerates the index, appends the changelog, opens the PR), committing the §3a amendment + RB-028 + this proposal alongside.

---
*Owner decision options: **(A)** adopt as DL-076 amendment with the owner-set thresholds (recommended; this proposal is written for A); **(B)** adjust thresholds; **(C)** defer. AI drafted and recommends; only the owner ratifies (Framework 001A).*

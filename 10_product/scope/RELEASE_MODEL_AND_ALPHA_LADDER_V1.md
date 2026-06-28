# OSLO Release Model & Alpha Release Ladder v1

- **Status:** **Ratified — DL-076** (2026-06-19). Reconciles the **audience-scale release axis** (R1–R5) with the **maturity-gate axis** (Alpha / Beta / GA · §20 · the Phase 1/2 prove-gates). **Non-doctrinal roadmap orientation** — introduces no new structure; every row cites existing canon. Living/roadmap reference (re-versioned as the ladder is realized).
- **Type:** Product scope / roadmap (`10_product/scope`).
- **Source:** Owner direction 2026-06-19 — "Alpha = 3–5 releases; R1 = owner + <5; R2 = 10–20; 50+ users remains the gate for proceeding to Beta." Grounded in Master Spec §19–§20, DL-049, DL-060/DL-070, DL-073, and `BACKLOG_ADOPTION_ACCELERATION_AND_GROWTH_LOOPS`.

---

## 1. Two axes (the reconciliation)

These had been conflated; they are **orthogonal** and this note keeps them distinct:

- **Audience-scale (release) axis — R1, R2, R3 …** — how widely the product is rolled out, by user count. The owner's rollout ladder.
- **Maturity-gate axis — Alpha → Beta → GA** — the canon's stages, governed by two *different kinds* of gate (see §3).

A product that has passed its **build/prove gates** can still be rolled out to a tiny audience (R1) and **grow** (R2 …) until it reaches the **graduation metric**. **Build-readiness ≠ audience-scale** — that distinction is the whole point of this note.

## 2. The Alpha release ladder (owner-set)

**Alpha spans 3–5 releases**, ramping the audience toward the §20 Beta gate:

| Release | Audience | Purpose | Growth mechanism |
|---|---|---|---|
| **R1** | owner + **<5** | private validation — the **owner's own validation vehicle** (DL-049) | manual onboarding; **"generates + measures invitations only"** (DL-049) |
| **R2** | **10–20** | extended validation; **build the growth loops** | G3/G4 growth loops built, on the R1 foundations (CRR seam / Wave I; Export-Share-Out / Wave E) |
| **R3–R5** | ramp toward 50+ | scale-up | the growth loops drive acquisition toward the gate |
| **→ gate** | **50+ users + engagement (§20)** | **Alpha → Beta graduation** | — |

R1/R2 are *early Alpha releases* **below** the gate; the **50+ metric is reached at the end of the Alpha ladder**, not in R1/R2.

## 3. Two kinds of gate (do not conflate)

- **Build / prove gates** — *gate that the product WORKS* (engineering sign-off). Alpha **Phase 1 "Prove Understanding"** (Fast Pass; DL-060/DL-070) and **Phase 2 "Prove Improvement"** (Deep Pass), across the wave build sequence (A → B → C → U → E). **The one currently open is PR #46 / Wave C.** These are build sign-offs and are explicitly **not** the §20 metrics.
- **Graduation / outcome gate** — *gate that you SCALE* (market). **§20 = 50+ users + engagement** = Alpha → Beta. The Phase-1 exit gate is explicit: the §20 metrics are **"Beta-advancement outcome criteria, not a build sign-off gate."** Reached across the R1–R5 ladder via growth.

**To advance Alpha → Beta, both must hold:** the product **proven** (build gates) **and** the audience/engagement **reached** (§20).

## 3a. Alpha exit criteria (owner-set)

> **Authorized by `DL-082-alpha-exit-criteria` (amends DL-076).** Specifies what "**proven**" means at Alpha exit, alongside the unchanged §20 graduation gate.

Advancing Alpha → Beta requires **all** of the following — the three owner-set "proven" gates plus the existing engagement gate:

1. **Build / prove gates pass** (unchanged, §3) — the engine works (Phase 1 "Prove Understanding" / Phase 2 "Prove Improvement").
2. **Value validated** — the project-intelligence value proposition is validated by **behavioral retention / repeat use**: users return and re-run OSLO on real projects **unprompted** (the hardest-to-fake usage signal). Sentiment alone does not pass.
3. **Planning-vendor breadth** — **≥ 2** planning/execution platforms are governed sources, each with **real per-platform depth** (governed-source depth, **not** shallow connectors / a "row of logos"). This establishes the cross-platform **neutrality/altitude** that constitutes the layer; the ≥ 2 threshold is consistent with the Layer-Before-Depth sequencing principle (`DL-081-roadmap-layer-sequencing`).
4. **Execution visibility operational** — **read-only outcome ingest** from **≥ 1** execution platform **plus a closed feedback loop** (governed understanding compared against observed outcomes). Strictly observational — advisory-only preserved (DL-047). **Drift-surfacing from execution data is deferred to Beta+** (an execution-intelligence behavior, Positioning §7 levels 4–5; out of Alpha scope per Layer-Before-Depth).
5. **Audience / engagement reached** — **50+ users + engagement (§20)** — **unchanged** (DL-076). The market/outcome graduation gate.

**Relationship to the two-gate model (§3):** criterion 1 is the build/prove gate; criterion 5 is the graduation/outcome gate; criteria 2–4 **enrich the "proven" side** — Alpha proves not just that the engine works, but that it delivers recognized value, travels across planning sources, and closes the outcome loop. Criteria 2–4 are **owner-set Alpha exit gates**; they do not alter R1 scope (CHG-064) and apply across the R1–R5 ladder.

## 4. Access model across the ladder (DL-073)

- **Alpha (R1–R5) + Beta — controlled access:** invite/allowlist, **auth-gated**, ingestion-first landing.
- **GA — open access:** the deferred-signup model — **ratified intent (DL-080)**: provisional `Principal` claim-as-promotion, DL-048 pre/post-signup gating (anonymous one-project/Fast-only/Free-envelope, **reset-at-claim**), and pre-signup retention/privacy (Operational-class, **30-day unclaimed TTL**). **GA-gated**; engineering authors the realization before GA. Record: `00_owner/decisions/records/DL-080-ga-deferred-signup-realization.md`.

## 5. Where capabilities land (from the growth backlog)

- **R1:** cognition + the R1 foundations (CRR seam / Wave I; Export-Share-Out / Wave E) + **G1 data-capture**.
- **R2:** **G3 + G4** full growth loops.
- **R3–R5:** the loops drive the scale to the **§20** gate.
- **Beta+ / forward:** G1's learning, G2 benchmarking, G5 (Pro+) connectors, G6 template gallery; the GA onboarding proposals; the DL-074 tier-row + overage-metering realization.

## 6. Status / routing

DRAFT reconciling the two axes — **non-doctrinal roadmap orientation**, introducing no new structure (cites §20, DL-049, DL-060/070, DL-073, the growth backlog). Recommend **light owner ratification** (the DL-075 / DL-064 crosswalk pattern) so the **R1–R5 ↔ Alpha/Beta/§20** mapping is the single authoritative reference and the audience-vs-maturity distinction can't drift back into conflation.

---

*This note establishes the OSLO release model as two orthogonal axes — the R1–R5 audience-scale rollout ladder and the Alpha/Beta/GA maturity stages — with Alpha spanning 3–5 releases (R1 owner+<5 → R2 10–20 → … → 50+ users), the §20 50+ metric as the Alpha→Beta graduation gate (an outcome gate, distinct from the Phase 1/2 build/prove gates), controlled access through Alpha/Beta and open access at GA (DL-073), and the growth loops sequenced R1 foundations → R2 build → R3–R5 scale. It introduces no new structure and is routed for owner ratification.*

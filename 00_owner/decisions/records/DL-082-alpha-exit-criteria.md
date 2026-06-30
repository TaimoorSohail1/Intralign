# DL-082 — Alpha exit criteria (specify "proven" for Alpha→Beta; amends DL-076)

- **Date:** 2026-06-28 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (product-roadmap orientation; non-doctrinal)

- **Source:** Owner direction 2026-06-28 — the Alpha phase's three pillars (project-intelligence value validation, planning-vendor breadth, execution visibility) are **exit criteria**. Specifies what "proven" means at Alpha→Beta, alongside the unchanged §20 50+-users graduation gate. Proposal: `PROPOSAL_ALPHA_EXIT_CRITERIA_DRAFT.md`; backlog: RB-028. Grounded in DL-076 (release ladder / two-gate model), Master Spec §20, CHG-064 (R1 scope), DL-047 (advisory-only), Positioning §4/§7/§8; consistent with `DL-081-roadmap-layer-sequencing` (Layer-Before-Depth).
- **Layer:** Product scope / roadmap orientation (`10_product`). **Non-doctrinal**; amends DL-076 by specifying Alpha exit criteria. Artifact: `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a.

## Decision
Amend DL-076 by ratifying the **Alpha exit criteria**. Advancing Alpha → Beta requires **all** of:

1. **Build / prove gates pass** — the engine works (Phase 1 "Prove Understanding" / Phase 2 "Prove Improvement"). Unchanged (DL-076 §3).
2. **Value validated** — project-intelligence value proposition validated by **behavioral retention / repeat use**: users re-run OSLO on real projects **unprompted**. Sentiment alone does not pass.
3. **Planning-vendor breadth** — **≥ 2** planning/execution platforms governed as sources, each with **real per-platform depth** (not shallow connectors). Establishes cross-platform neutrality/altitude; ≥ 2 is consistent with the Layer-Before-Depth threshold.
4. **Execution visibility operational** — **read-only outcome ingest** from **≥ 1** execution platform **plus a closed feedback loop** (governed understanding compared against observed outcomes); strictly observational (DL-047). **Drift-surfacing deferred to Beta+** (execution-intelligence, §7 levels 4–5).
5. **Audience / engagement reached** — **50+ users + engagement (§20)**, unchanged (DL-076).

Criterion 1 = build/prove gate; criterion 5 = graduation/outcome gate; criteria 2–4 enrich the "proven" side and are the owner-set Alpha exit gates.

## Conditions
1. **Amends, does not supersede, DL-076.** The two-axis model and the two-gate distinction (build/prove vs graduation/outcome) are preserved; criteria 2–4 specify the "proven" side; criterion 5 (§20) is unchanged.
2. **Advisory-only preserved.** Execution visibility is read-only observation/feedback; never execution or coordination (DL-047, Positioning §9).
3. **R1-safe.** Does not alter R1 scope (CHG-064); criteria 2–4 apply across the R1–R5 Alpha ladder, met by Alpha exit.
4. **Consistency with Layer-Before-Depth.** The ≥ 2 breadth threshold and the depth-deferral (drift-surfacing → Beta+) align with `DL-081-roadmap-layer-sequencing`; if that record's threshold changes at ratification, reconcile this one to match.
5. **Living reference.** Thresholds are owner-set as of 2026-06-28 and re-versioned as the ladder is realized.

## Supersedes / Amends
**Amends DL-076** (adds §3a Alpha exit criteria to `RELEASE_MODEL_AND_ALPHA_LADDER_V1.md`). No prior decision superseded; additive specification.

## Provenance
Owner working session, 2026-06-28: owner confirmed the three Alpha pillars are exit criteria and set the thresholds (≥ 2 vendors; behavioral retention/repeat use; read-only ingest + closed feedback loop), delegating the execution-visibility definition to an AI recommendation which the owner adopted. AI drafted and recommended (Framework 001A); the owner ratifies. Numbered at landing under the DL-065 records discipline.

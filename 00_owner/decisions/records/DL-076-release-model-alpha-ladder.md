# DL-076 — Ratify the OSLO release model & Alpha release ladder (R1-R5 reconciled with Alpha/Beta/§20)

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-19 — "Alpha = 3–5 releases; R1 = owner + <5; R2 = 10–20; 50+ users remains the gate for proceeding to Beta." Reconciles the **audience-scale axis (R1–R5)** with the **maturity-gate axis (Alpha/Beta/GA · §20 · Phase 1/2)**. Grounded in Master Spec §19–§20, DL-049, DL-060/DL-070, DL-073. Artifact: `RELEASE_MODEL_AND_ALPHA_LADDER_V1.md`.
- **Layer:** Product scope / roadmap orientation (`10_product`). **Non-doctrinal** reconciliation (DL-064 / DL-075 pattern). No doctrine, structure, or responsibility introduced.

## Decision
Ratify `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` as the canonical reference for the OSLO release model: **two orthogonal axes** — the **R1–R5 audience-scale rollout ladder** and the **Alpha / Beta / GA maturity stages**. **Alpha spans 3–5 releases** (R1 owner+<5 → R2 10–20 → … → 50+ users); the **§20 50+-users metric is the Alpha→Beta graduation (outcome) gate**, distinct from the **Phase 1/2 build/prove gates** (DL-060/DL-070; the open one is PR #46 / Wave C). **Advancing Alpha→Beta requires both** — the product *proven* (build gates) **and** the audience/engagement *reached* (§20). Access is **controlled** through Alpha/Beta and **open** at GA (DL-073).

## Conditions
1. **Orientation only.** Build-readiness ≠ audience-scale; the two gate types (build/prove vs graduation/outcome) **must not be conflated**.
2. **Bridge only.** Introduces no new structure or doctrine; reconciles existing canon (§20, DL-049, DL-060/070, DL-073).
3. **Living reference.** Re-versioned as the R1–R5 ladder is realized.

## Supersedes / Amends
None. Additive scope/roadmap reconciliation; mirrors the DL-064 / DL-075 crosswalk pattern. No canonical content superseded.

## Provenance
Owner decision via working session, 2026-06-19; the owner defined Alpha = 3–5 releases (R1 <5 → R2 10–20 → … → 50+) with 50+ users as the Beta gate, and directed capturing + ratifying the model to reconcile the audience-scale and maturity axes. AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.

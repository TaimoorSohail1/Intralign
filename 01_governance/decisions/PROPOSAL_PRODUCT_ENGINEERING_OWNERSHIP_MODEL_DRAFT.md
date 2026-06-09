# Proposal — Product↔Engineering Ownership Model + Repository Restructure

**Document Type:** Governance Proposal (Framework 001A) — **plan only; nothing moved/ratified** · **Status:** **DRAFT · Pending Owner Ratification** · **Date:** 2026-06-08
**Origin:** Engineering-lead proposal (ownership-zone model) → owner critical review → this disposition.
**Companion docs:** `REPO_RESTRUCTURE_MIGRATION_MAP_DRAFT.md` (current→target file map), `CODEOWNERS.proposed` (authority map). Supersedes/absorbs `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` if adopted.

---

## Context

The engineering lead proposed a product↔engineering operating model with three parts: (1) a **boundary principle**, (2) explicit **handoff lists**, and (3) a **repository restructured by ownership zones** (`00_owner / 10_product / 20_handoff / 30_engineering / 90_research`). R1 implementation has **not started**, so a physical restructure is at its lowest-cost window (before code/contracts reference paths). The owner reviewed it, found it ~85% congruent with the existing system, and supports adoption **with amendments**.

## The boundary principle (adopt)

> **Product owns Problem, Behavior, and Domain Rules ("what must be true"). Engineering owns Structure, Mechanism, and Realization ("how it's built"). The two meet at one shared artifact: the Contract.**

Corollaries adopted: domain expressed as **rules, not object models**; experience as **behavior, not component markup**; acceptance as **outcome-level goals + NFR targets, not test code**; the **Contract is the single co-governed seam** (changes require both sides).

> **Owner-constraint clause (binding):** The Owner may issue **binding build constraints at any time, ratified via Framework 001; engineering realizes within them.** "Engineering authoritative" governs **default authorship of realization**, never the Owner's right to constrain *how* OSLO is built. Build-governance (deployment/QA/observability governance, the Anti-Assumption Protocol, implementation constraints, the AI-First delivery rules, epistemic invariants) is **owner-ratified policy** that binds engineering regardless of which directory it physically lives in.

## Proposed zone structure (adopt, with Amendment 2)

| Zone | Authority | Holds |
|---|---|---|
| `00_owner` | **Owner only** (governs all zones) | ratified decisions, owner-decision queue, Open-TBD register, **doctrine, constitution, frameworks, canonical definitions, glossary/ontology, manifest, changelog, audits** (Amendment 2) |
| `10_product` | Product authoritative · Eng reads | strategy (vision/PLG/tiering/collaboration), domain *expression*, scope (master spec/capability matrix/backlog/release scope), experience (journeys/UX behavior), acceptance (AC + NFR targets) |
| `20_handoff` | **Co-governed seam** (both sides) | contract triads (Impl/QA/Obs), capability→contract→test→observability traceability matrix, interfaces (API contract, event/state model) |
| `30_engineering` | Engineering authoritative · Product reads | architecture, data (logical+physical schema), analysis engine, environment (stack/calibration/CI-CD/deploy), QA (specs/fixtures/determinism), delivery (phase plans/runbook/sequencing) |
| `90_research` | Non-canonical, either side | `04_research/`, `raw/` |

## Findings

1. **High congruence.** The model re-expresses the existing system around *ownership* rather than *topic*; the contract is already the seam (DL-043), and the escalation path already exists (Anti-Assumption Protocol). The eng lead has demonstrably read the canon.
2. **Genuine improvements:** explicit per-zone editing authority; the contract framed as the **single bilateral seam**; the rules/behavior/goals abstraction line.
3. **Low mechanical cost (per reorg-proposal-v1 scan):** only **~18 path-style references** break on a move; **~1,442 are bare filenames** that survive. Reference-update burden is small; the move is a single commit verified by the doc-integrity CI.
4. **Timing window is open:** R1 not started → cheapest possible moment to restructure.

## Concerns

1. **⚠ Constitutional collision (DL-037).** The top-level `01–05` split is **constitutional per DL-037**. The zone model **replaces** it → adoption requires **superseding DL-037** via a new ratified Decision (a constitution-level change, not a routine reorg). *This is the gating governance step.*
2. **Authority labels could erode owner supremacy.** "Engineering authoritative" must mean *default author / owns-the-how* — **not** authority to change ratified architecture canon unilaterally. All zones operate **under** Framework 001 (owner ratifies canonical changes). → **Amendment 1.**
3. **Doctrine misfiled as product.** The eng-lead sketch places doctrine/epistemic-invariants under `10_product`. They are **founder/owner canon** (precedence: Doctrine > Constitution > Implementation) and must not become routinely PM-editable. → **Amendment 2** (doctrine→`00_owner`).
4. **Seam needs an arbiter.** "Co-governed" requires a tiebreaker when product and engineering disagree on a contract. → **Amendment 3** (owner decides, per precedence).
5. **Mixed folders need splitting, not moving wholesale.** `02_product/specs/{data_api_nfr, telemetry, models}` contain *both* product (intent/AC/NFR) and engineering (schema/realization) content — see migration map's "split" flags.
6. **Stage fit.** The model presupposes distinct PM + Eng functions; today they're largely the owner + a lead + agents. Adopt as the **target operating model**, not heavy ceremony now.

## Amendments (conditions of adoption)

1. **All zones sit under owner ratification.** "Authoritative" = default author/owner-of-the-how; canonical changes route through Framework 001. `00_owner` governs all zones.
2. **Doctrine, constitution, frameworks, canonical definitions, glossary/ontology → `00_owner`** (not `10_product`).
3. **Owner is the seam tiebreaker.**
4. **Mixed folders are split by ownership** at migration time (per the map), not relocated intact.
5. **Build-governance is owner-ratified policy** (per the owner-constraint clause above): deployment/QA/observability governance, the Anti-Assumption Protocol, implementation constraints, AI-First delivery rules, and epistemic invariants bind engineering and change only by owner ratification — preserving the Owner's standing right to prescribe *how* OSLO is built.

## Dependencies

- **New Decision superseding DL-037** (top-level split is no longer constitutionally fixed at `01–05`). Must be ratified before any move.
- **Reference/infra rewire:** the ~18 path-style refs + `START_HERE.md`, `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md`, `CLAUDE.md`/`AGENTS.md`, the Phase-1 kickoff packet, and `tools/doc_integrity_check.py` allowlists/excludes.
- **Doc-integrity CI** run post-move to prove zero broken refs (gate the commit on green).
- Reconcile/retire `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` (sub-foldering within 01–05) — superseded by the zone model if adopted.

## Proposed CLAUDE.md / AGENTS.md insert (boundary principle) — for review, not yet applied

```
## Product↔Engineering Boundary (ownership model)
- Product owns Problem, Behavior, Domain Rules ("what must be true"); Engineering owns
  Structure, Mechanism, Realization ("how it's built"); they meet at the Contract.
- Zones: 00_owner (owner-only, governs all) · 10_product (product-authoritative) ·
  20_handoff (co-governed SEAM — contract changes need both sides) · 30_engineering
  (engineering-authoritative) · 90_research (non-canonical).
- "Authoritative" = default author, NOT authority to supersede ratified canon. All
  canonical changes route through Framework 001; the OWNER ratifies and breaks seam ties.
- Doctrine/constitution/epistemic invariants are owner canon (00_owner), never product-editable.
- The OWNER may issue binding build constraints at any time (ratified via Framework 001);
  engineering realizes within them. Build-governance is owner-ratified policy, not
  engineering-editable — regardless of which directory it sits in.
```

## Recommendation

**Adopt the ownership model and zone structure, with Amendments 1–4, executed now (pre-R1) as a single restructure commit** — *conditional on* ratifying a new Decision that supersedes DL-037. Capture the boundary principle in `CLAUDE.md`/`AGENTS.md`. Run the doc-integrity CI as the merge gate.

## Status

**DRAFT — pending owner ratification.** No files moved, no canon edited, DL-037 not yet superseded. On owner approval: (1) ratify the DL-037-superseding decision; (2) finalize the migration map + CODEOWNERS; (3) execute the move as one commit; (4) verify via doc-integrity CI; (5) apply the CLAUDE.md/AGENTS.md insert.

---
*Owner decision options: **(A)** adopt zone model + amendments + supersede DL-037 (recommended, full physical adoption now); **(B)** adopt the boundary principle + CODEOWNERS overlay only, keep 01–05 (no DL-037 change); **(C)** defer. This proposal is written for (A).*

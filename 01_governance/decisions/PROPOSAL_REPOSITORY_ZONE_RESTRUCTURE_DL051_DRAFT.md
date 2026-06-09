# Proposal / Disposition (DRAFT) — Adopt Ownership-Zone Repository Taxonomy; Supersede DL-037 Structural Taxonomy

> **Status:** **DRAFT · Pending Owner Ratification** — AI-drafted recommendation; not ratified.
> Per `CLAUDE.md`, AI may assist with analysis and recommendation generation only. **Only the
> repository owner may ratify, reject, supersede, or adopt canonical content.** Nothing in this
> document moves a file or supersedes a Decision until the owner ratifies it under Framework 001/001A.
>
> **Proposed Decision ID:** **DL-051** (next free identifier; DL-050 is current max).
> **Date drafted:** 2026-06-09 · **Layer:** Root Governance (structural reorganization affecting all tiers).
> **Companion docs:** `PROPOSAL_PRODUCT_ENGINEERING_OWNERSHIP_MODEL_DRAFT.md` (the operating model + amendments),
> `REPO_RESTRUCTURE_MIGRATION_MAP_DRAFT.md` (current→target file map), `CODEOWNERS.proposed` (authority map),
> `ZONE_GROUNDING_RULES.md` (the classification method — already merged on `main`).

---

## 1. Purpose

DL-051 is the **gating Decision** that authorizes replacing the `01–05` domain taxonomy with the
five-zone **ownership** taxonomy (`00_owner / 10_product / 20_handoff / 30_engineering / 90_research`).
It exists because the `01–05` split was made canonical by **DL-037** (Repository Domain Restructure,
Ratified with Conditions, 2026-05-29), which "establishes the post-migration repository structure as
the canonical physical organization." A reorganization that *replaces* that taxonomy therefore cannot
proceed as a routine edit — it requires a Decision that **supersedes the structural-taxonomy
establishment of DL-037.** This is that Decision, drafted for owner ratification.

`ZONE_GROUNDING_RULES.md` (the *method* for classifying content into zones) is already merged, but it
carries an explicit scope guard: *"does NOT enact the zone restructure or supersede DL-037 … separate
Framework 001 decisions."* DL-051 is the separate decision that guard points to.

---

## 2. What is superseded — and what is preserved (precise scope)

**Superseded (narrow):**
- **Only the structural-taxonomy establishment of DL-037** — i.e., the clause establishing the
  `01_governance / 02_product / 03_architecture / 04_research / 05_execution` domain split as "the
  canonical physical organization." That physical taxonomy is replaced by the ownership-zone taxonomy.

**Expressly preserved (NOT superseded):**
- **All substantive content** relocated under DL-037 — Doctrine 01–11, Constitution Articles 1–50,
  Implementation Spec bodies, contracts, research. DL-051 moves files; it edits **no** body content.
- **DL-033** (doctrine-centered architecture). The zone model *operationalizes* it more strongly:
  Doctrine/Constitution move to `00_owner`, reinforcing precedence **Doctrine > Constitution >
  Implementation**, not weakening it.
- **DL-036** (Surface Authority Rule) and its R-clauses — canonical-definition surfaces keep their
  authority relationships; only their *paths* update mechanically.
- **All other Decisions** DL-001 … DL-050, Frameworks 001 / 001A, the Manifest, and the Clarifications
  #1–#10 of DL-037 (which governed the *previous* migration's execution).
- **DL-037's historical validity.** DL-037 remains a valid, Ratified Decision of record; DL-051
  supersedes only its forward-looking structural-taxonomy establishment, not its existence or its
  non-structural conditions.

> **Net:** DL-051 is a *taxonomy* supersession, not a content supersession. Same canon, new shelving.

---

## 3. Framework 001A Review

### Findings

1. **The gating dependency is real and specific.** DL-037 made `01–05` canonical; only a superseding
   Decision can replace it. Absent DL-051, any file move is an ungoverned edit in violation of
   `CLAUDE.md` ("conflicts resolved through governance proposals, not direct edits").
2. **The replacement is congruent with existing doctrine.** The ownership model re-expresses the system
   around *authority* rather than *topic*; the contract is already the seam (DL-043), the escalation
   path already exists (Anti-Assumption Protocol), and doctrine→`00_owner` strengthens DL-033 precedence.
3. **Mechanical cost is low and bounded** (per the v1 reorg scan): ~18 path-style references break on a
   move; ~1,442 bare-filename references survive. The move is one atomic commit verifiable by the
   doc-integrity CI.
4. **Timing window is open.** R1 implementation has not started — the lowest-cost moment to restructure,
   before code and contracts encode paths.
5. **The method is ratified-as-merged.** `ZONE_GROUNDING_RULES.md` (incl. the four owner amendments and
   the ratify≠author boundary) is already on `main`, so the classification rules the migration applies
   are settled.

### Concerns

1. **Constitutional weight.** Replacing a DL-037-established canonical taxonomy is a constitution-level
   act, not a convenience reorg. It must be ratified explicitly, with the supersession scope stated
   narrowly (§2) so no one later reads it as having reopened content. *(Mitigated by §2.)*
2. **Mixed folders must be split, not moved intact.** `02_product/specs/{data_api_nfr, telemetry,
   models}` and `03_architecture/runtime_models` contain *both* product and engineering content; moving
   them wholesale would mis-file content under the new authority lines. *(Mitigated: migration map flags
   each SPLIT.)*
3. **Execution atomicity.** Content edits must not ride along in the migration commit. The move +
   ~18 path fixes + meta-file updates + CI-config must be one commit with **no body edits**, gated on a
   green doc-integrity run. *(Mitigated: condition C-4 below.)*
4. **Authority labels.** "Engineering authoritative" must mean *default author of realization*, never
   authority to change ratified canon — already settled by the ratify≠author boundary in the merged
   rulebook, restated here as condition C-2.
5. **DL-037 Clarification carryover.** A handful of DL-037 clarifications (e.g. RB-020 disposition,
   RB-005 residual) are content/backlog matters independent of taxonomy; DL-051 must leave them
   untouched. *(Mitigated by §2 "expressly preserved.")*

### Dependencies

- **The five amendments** from `PROPOSAL_PRODUCT_ENGINEERING_OWNERSHIP_MODEL_DRAFT.md` are conditions of
  adoption (carried as C-1…C-5 below).
- **Reference/infra rewire:** the ~18 path-style refs + `START_HERE.md`,
  `REPOSITORY_ARCHITECTURE.md`, `REPOSITORY_INDEX.md`, `CLAUDE.md` / `AGENTS.md`, the Phase-1 kickoff
  packet, and `tools/doc_integrity_check.py` allowlists/excludes (`raw/`→`90_research/raw/`).
- **Doc-integrity CI** run post-move as the merge gate (0 errors).
- **CODEOWNERS swap:** retire the interim `.github/CODEOWNERS` in favour of `CODEOWNERS.proposed`
  (zone paths) only *after* the move lands.
- **Reconcile/retire** `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md` (sub-foldering within `01–05`) —
  superseded by the zone model if DL-051 is adopted.

### Recommendation

**Adopt** the ownership-zone taxonomy and supersede the DL-037 structural-taxonomy establishment
(§2 scope), **with conditions C-1…C-5**, executed **now (pre-R1)** as a single atomic restructure commit
gated on a green doc-integrity run. Record the boundary principle in `CLAUDE.md` / `AGENTS.md`.
*Rationale:* high doctrinal congruence, low mechanical cost, open timing window, method already ratified;
the only true cost is the one-time governed move, and the window will not be cheaper later.

### Status

**DRAFT — pending owner ratification.** No files moved, no canon edited, DL-037 structural taxonomy not
yet superseded. AI does not ratify.

---

## 4. Conditions of adoption (C-1 … C-5)

These mirror the five amendments already accepted in the ownership-model proposal and the merged rulebook:

- **C-1. All zones sit under owner ratification.** "Authoritative" = default author / owns-the-how;
  canonical changes route through Framework 001; `00_owner` governs all zones.
- **C-2. Doctrine, constitution, frameworks, canonical definitions, glossary/ontology, epistemic
  invariants → `00_owner`** (not `10_product`). Ratify ≠ author: owner ratifies policy *intent*;
  engineering authors *realization* and proposes policy.
- **C-3. Owner is the seam tie-breaker** — scoped to deadlock-breaking on contested `20_handoff`
  contracts, not routine contract authorship (precedence: Doctrine > Constitution > Implementation).
- **C-4. Mixed folders are split by ownership at migration time** (per the migration map's SPLIT flags),
  not relocated intact. **No body-content edits in the migration commit;** gate on green doc-integrity CI.
- **C-5. Build-governance is owner-ratified policy** (deployment/QA/observability governance, the
  Anti-Assumption Protocol, implementation constraints, AI-First delivery rules, epistemic invariants):
  binds engineering, changes only by owner ratification — preserving the owner's standing right to
  prescribe *how* OSLO is built; engineering authors the realization.

---

## 5. Proposed Decision-Log entry (ready to paste into `decision_log.md` ON RATIFICATION)

> Provided in house schema so the owner can paste it verbatim if ratifying. **Do not paste until
> ratified** — it is proposed text, not a recorded Decision.

```
### DL-051 — Adopt Ownership-Zone Repository Taxonomy; Supersede DL-037 Structural Taxonomy

- **Date Recorded:** <ratification date>
- **Layer:** Root Governance (structural reorganization affecting all tiers)
- **Source:** PROPOSAL_PRODUCT_ENGINEERING_OWNERSHIP_MODEL_DRAFT.md; REPO_RESTRUCTURE_MIGRATION_MAP_DRAFT.md;
  CODEOWNERS.proposed; ZONE_GROUNDING_RULES.md (method, merged); this disposition.
- **Decision:** Adopt the five-zone ownership taxonomy (00_owner / 10_product / 20_handoff /
  30_engineering / 90_research) as the canonical physical organization, replacing the 01–05 domain
  taxonomy established by DL-037. Execute as a single atomic migration commit per the migration map:
  pure moves + ~18 path-reference fixes + meta-file updates (START_HERE, REPOSITORY_ARCHITECTURE,
  REPOSITORY_INDEX, CLAUDE.md/AGENTS.md) + doc-integrity-CI config; mixed folders split by ownership;
  no body-content edits. Gate the merge on a green doc-integrity run (0 errors). Capture the
  product↔engineering boundary principle in CLAUDE.md/AGENTS.md. Swap the interim .github/CODEOWNERS for
  CODEOWNERS.proposed after the move lands.
- **Rationale:** The ownership taxonomy operationalizes DL-033 (doctrine-centered architecture) more
  strongly by filing Doctrine/Constitution under 00_owner, reinforcing Doctrine > Constitution >
  Implementation precedence. R1 has not started, so the move is at its lowest-cost window. Mechanical
  cost is bounded (~18 path refs break; ~1,442 bare-filename refs survive). The classification method is
  already ratified-as-merged.
- **Disposition:** <Accepted with Conditions | Accepted | Returned for Revision | Deferred>.
- **Conditions:** C-1 all zones under owner ratification; C-2 doctrine/invariants→00_owner (ratify≠author);
  C-3 owner breaks 20_handoff deadlocks (not routine authorship); C-4 mixed folders split, no body edits in
  the migration commit, green doc-integrity gate; C-5 build-governance is owner-ratified policy.
- **Supersedes:** The structural-taxonomy establishment of DL-037 ONLY (the 01–05 split as canonical
  physical organization). Preserves all substantive content relocated under DL-037, DL-037's historical
  validity, its non-structural Clarifications #1–#10, DL-033, DL-036, and Decisions DL-001…DL-050.
- **Affected Artifacts:** repository-wide file relocations per the migration map; ~18 path-style references
  updated; START_HERE.md, REPOSITORY_ARCHITECTURE.md, REPOSITORY_INDEX.md, CLAUDE.md, AGENTS.md updated;
  tools/doc_integrity_check.py allowlists/excludes updated; .github/CODEOWNERS replaced by CODEOWNERS.proposed;
  REPOSITORY_REORGANIZATION_PROPOSAL_V1.md retired/superseded. No Doctrine/Constitution/Spec body content edited.
- **Resulting Actions:** Execute the migration as one commit on a branch → PR → green doc-integrity gate →
  owner merge. Record a changelog entry (next CHG-###) authorized by DL-051. Activate CODEOWNERS.proposed.
- **Status:** <Ratified with Conditions | Ratified | …>.
```

---

## 6. Owner decision options

- **(A) Adopt** the zone taxonomy + supersede DL-037 structural taxonomy, with C-1…C-5, executed now
  (pre-R1) as one atomic migration commit. *(Recommended — full physical adoption at the cheapest window.)*
- **(B) Overlay only** — keep `01–05`, adopt the boundary principle + CODEOWNERS overlay (already partly
  live via the interim CODEOWNERS), defer the physical move. No DL-037 supersession. *(Lowest disruption;
  forgoes the open timing window.)*
- **(C) Defer** — hold until a later milestone. *(Cost rises once R1 encodes paths.)*

This proposal is written for **(A)**.

---

*Authority note: this document is an AI-generated recommendation under `CLAUDE.md`. It ratifies nothing.
On owner ratification, the owner records DL-051 in `decision_log.md` (using §5), and only then is the
migration authorized to execute.*

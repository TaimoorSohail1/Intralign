# Proposed Edits (REDLINE) — execution-monitoring tier split

> **Staged change-spec for DL-206** (ratified 2026-08-09, staged in `release-2/`). These edits are the
> exact changes to R1-`main` canon that DL-206 mandates; they are **deliberately NOT applied to `main`
> now** — they are held in `release-2/` and applied **when R2 folds into `main` at R1 graduation**,
> together with the other R2-staged decisions (DL-172, DR-7, …). Three files change: the Tier Definitions
> register (§1, §2c), the Canonical Glossary disambiguation register, and a one-line note in the Release
> Model / Alpha Ladder. When applied: branch → PR → green doc-integrity gate → **owner merge. Never push
> to main.**

---

## Edit 1 — `10_product/strategy/tiering/RELEASE_1_TIER_DEFINITIONS_V1.md` §1 (the ladder)

Two cells change: sync leaves Basic (→ Pro), manual execution-stage monitoring joins Basic, and Pro's
line is made explicit.

**BEFORE**

```
| **T2 · Basic** | **Capacity / scope** — more plans, bigger plans. Plus connected sources, the reporting suite, export/sync | Projects · envelope |
| **T3 · Pro** | **Execution & programme support** (DL-083) | Capability |
```

**AFTER**

```
| **T2 · Basic** | **Capacity / scope** — more plans, bigger plans. Plus connected sources, the reporting suite, plan export-out, and **manual execution-stage monitoring** (on-demand). *(Two-way sync is Pro — see §2c.)* | Projects · envelope |
| **T3 · Pro** | **Automated execution & programme support** — continuous monitoring + auto-import / two-way sync + programme / cross-plan support (DL-083; DL-206) | Capability |
```

---

## Edit 2 — `RELEASE_1_TIER_DEFINITIONS_V1.md` §2c (capability register)

Replace the single **Execution monitoring** row with a manual/continuous split, and add an explicit
**Auto-import / two-way sync** row so the register (not just DL-172/DR-7 prose) is the authoritative
surface for sync placement. Adjacent rows shown for anchoring — leave them unchanged.

**BEFORE**

```
| Connected sources / integrations | — | ✅ | ✅ | **RATIFIED** *(shape)* | freemium Constrain list; DL-103 §7f |
| Plan export → execution tool | — | ✅ | ✅ | **RATIFIED** | **DL-083** |
| Execution monitoring | — | — | ✅ **Pro+** | **RATIFIED** | **DL-083** (built in Beta) |
```

**AFTER**

```
| Connected sources / integrations *(read-only, inbound)* | — | ✅ | ✅ | **RATIFIED** *(shape)* | freemium Constrain list; DL-103 §7f |
| Plan export → execution tool *(outbound, one-shot)* | — | ✅ | ✅ | **RATIFIED** | **DL-083** |
| **Execution-stage monitoring (manual)** — on-demand ingest of execution actuals vs. plan; drift/trend maintained over time | — | ✅ | ✅ **Pro+** | **RATIFIED** | **DL-206** (amends DL-083; built in Beta) |
| **Continuous monitoring (automated)** — event/schedule-triggered watch; no user action | — | — | ✅ **Pro+** | **RATIFIED** | **DL-083** (built in Beta) |
| **Auto-import / two-way sync** *(automation)* | — | — | ✅ **Pro+** | **RATIFIED** | **DL-206** (resolves DL-172 §7 ↔ DR-7 → Pro) |
```

> Doctrine unchanged: both monitoring rows deliver the **same one accuracy bar** — Basic buys *access to
> the execution stage*, never a better read (DL-103 §1). The record, reviewers/CRR, and Viewers stay
> free/unmetered (DL-102 D128/CR-2/E).

---

## Edit 3 — `00_owner/CANONICAL_GLOSSARY.md` — Disambiguation Register (DL-053), "Semantic landmines" table

Add two rows so the two "monitoring" senses and the loaded word "phase" cannot drift. Insert after the
existing **MRI / Project MRI** row (currently the last row of the Semantic-landmines table).

**INSERT**

```
| **Monitoring** | **Execution-stage monitoring** — manual, on-demand actuals ingest (Basic) | **Continuous monitoring** — automated event/schedule watch (Pro) | bare "monitoring" banned; qualify manual vs. continuous (DL-206) |
| **Phase / Stage** | **Phase** = the **supply/release** limit (Alpha/Beta), D124 — never conflate with **tier** | plan lifecycle → **planning stage / execution stage** (also ≠ `confidence_stage` / Understanding State) | reserve **"phase"** for the D124 supply sense; use **"stage"** for the plan lifecycle; always qualify which |
```

---

## Edit 4 — `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a (note, not a re-placement)

DL-083's phase call is unchanged (execution monitoring builds in Beta; both the manual and continuous
forms are Beta). Add a one-line amendment note only.

**INSERT (after the §3a execution-monitoring line)**

```
> **Amended by DL-206 (2026-08-09):** execution monitoring is split by who drives updates —
> *manual execution-stage monitoring* (Tier 2 / Basic, on-demand) and *continuous monitoring* (Tier 3 /
> Pro+, automated). Both remain **Beta** capabilities; this changes tier placement, not phase.
```

---

## Apply order & checks (at R1 graduation, when R2 folds into `main`)

1. Branch off the canon line; apply Edits 1–4 (DL-206 is already stamped throughout).
2. Run the doc-integrity gate — expect it to now find the sync placement in the register (Edit 2) and the
   qualified "monitoring"/"phase" terms (Edit 3), clearing the DL-172 §7 ↔ DR-7 conflict and any bare
   colliding-word WARNs the new terms would otherwise trip.
3. Land the DL-206 record onto `main` alongside the other R2-staged decisions per the graduation plan.
4. Owner approves the PR → squash merge. **AI does not land canon.**

_Not touched (deliberately): DL-172 §2 multi-outcome-per-plan at Basic (given); Free tier; judgment-
quality / record / reviewer / Viewer / forecast / flat-per-account doctrine. Still open (from the
proposal): final Pro price; exact canonical terms (owner's DL-053 call); manual-monitoring +
programme-support scoping; land-to-main vs. R2-isolated staging._

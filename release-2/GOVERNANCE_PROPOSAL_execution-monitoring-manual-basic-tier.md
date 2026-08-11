# Governance Proposal (DRAFT) — Manual execution-stage monitoring at Basic; automation + programme at Pro

> **Status: RATIFIED as DL-206** — Idris (Founder Console), 2026-08-09. Staged in `release-2/`;
> **withheld from `main` until R1 graduation** (parity with the DL-172 / DR-7 staging posture). AI
> drafted and recommended; the owner ratified (Framework 001 / 001A — AI does not decide). Ratified
> record: `release-2/canon/decisions/DL-206_EXECUTION_MONITORING_TIER_SPLIT.md`. This packet is
> self-contained: Backlog framing → Proposed canon → Review (five outputs) → Decision body → landing.
>
> **Origin:** Owner working session, 2026-08-09 (Idris). **Backlog:** RB-041. **Decision:** DL-206.
> **Layer:** Product scope / monetization orientation (`10_product`). **Non-doctrinal** (re-maps tier
> *placement*; changes no doctrine). **Amends** DL-083; **extends** DL-172 §7 and DR-7; **resolves** a
> standing DL-172 §7 ↔ DR-7 conflict; **updates** the `RELEASE_1_TIER_DEFINITIONS_V1` register and the
> DL-053 disambiguation register.

---

## 1. Backlog entry (framing)

The current execution-handoff ladder places **all** execution monitoring at Pro+ (DL-083, capability 3:
"inbound outcome ingest + closed loop, continuous, costly"). The owner is reconsidering this on a
value-sequencing thesis: **the full value loop is execution monitoring + plan revision**, so the sooner
a user can experience that loop, the faster they realize the value of Outcome Orchestration. Gating the
*entire* loop to Pro delays first value; capacity meters — not capability walls — should drive upgrades.

Pressure-testing that thesis (this session) surfaced that moving *continuous* monitoring to Basic would
(a) break the flat-per-account cost posture (continuous monitoring is recurring compute) and (b) hollow
out Pro's only defined value line (DR-7 already marks Pro PROVISIONAL for exactly this reason). The
resolution the owner adopted: **split execution monitoring by who drives the updates.** A **manual,
on-demand** form of execution-stage monitoring is capacity-shaped (bounded by user effort, no recurring
compute), so it can sit at Basic and deliver the loop early; the **automated, continuous** form —
plus auto-import / two-way sync — stays Pro, where its cost and its upgrade narrative belong.

This also revisits a concern DL-083 itself flagged and deferred: *"Corpus-growth trade-off — keeping
monitoring at Pro+ narrows who feeds the outcome corpus… revisit if corpus growth lags."* Widening the
manual form to Basic widens the outcome-corpus feeder without the continuous-polling cost.

## 2. Proposed canon (content)

**Organizing axis (new, replaces feature-by-feature placement): Basic = manual / on-demand (you drive
it); Pro = automated / continuous (it drives itself).**

**2.1 — Split execution monitoring (amends DL-083 capability 3).** Execution monitoring is divided into:

- **Execution-stage monitoring (manual) → Tier 2 / Basic.** User-driven, on-demand ingestion of
  execution **actuals** (status, %-complete, actual dates, spend) against the plan, producing a refreshed
  read on delivery drift and a **monitored state maintained over time** (delta / trend across updates).
  The user triggers each update. Capacity-shaped; no recurring compute.
- **Continuous monitoring (automated) → Tier 3 / Pro+** (Team/Enterprise inherit). Event/schedule-
  triggered watch that ingests and re-interprets without user action. Unchanged from DL-083 in substance;
  DL-083's cost rationale (continuous polling) applies to **this** form only.

**2.2 — Resolve the sync conflict (DL-172 §7 ↔ DR-7).** Canon currently contradicts itself: DL-172 §7
places "auto-import + two-way sync" at **Basic**; DR-7 lists it under **Pro**'s value line. Under the
manual/automated axis, sync is automation → **Pro**. This adopts DR-7's placement and **supersedes
DL-172 §7's "auto-import + two-way sync = Basic"** clause. Basic retains **manual/one-shot** connection:
plan export → execution tool (DL-083 capability 2, unchanged) and manual execution-actuals ingest (2.1).

**2.3 — Confirm Pro's value line (extends DR-7).** Pro = automated continuous monitoring + auto-import /
two-way sync + **programme / cross-plan execution support** (already assigned to Pro by
`RELEASE_1_TIER_DEFINITIONS_V1` §1 "Execution & programme support", DL-083). Automation alone is a thin
story for the 2.7× Basic→Pro step (DR-7's own open note); programme support is what carries it. The
precise programme-support scope routes to its own scoping (as DL-083 routed realization). This eases —
does not by itself close — Pro's PROVISIONAL status; final Pro price stays open pending its capability set.

**2.4 — Free unchanged.** Free = the full plan read (planning stage), manual re-upload to refresh, export
a file. No execution-stage monitoring at Free.

**2.5 — Resulting ladder.**

| Rung | Plan (planning stage) | Execution stage | Who drives |
|---|---|---|---|
| **Free** | Full read; re-upload to refresh; export a file | — | User (snapshot) |
| **Basic** | Multi-outcome per plan + multiple plans (DL-172, given); plan export → execution tool | **Manual execution-stage monitoring** (actuals in, on-demand; drift/trend over time) | User (on-demand) |
| **Pro+** | — | **Continuous monitoring + auto-import + two-way sync + programme/cross-plan support** | System (automated) |

**2.6 — Phase.** Like all execution monitoring (DL-083), the manual form is a **Beta / post-R2**
capability. **No R2 build impact** (DL-172 §5: R2 is freemium-only; paid capabilities are post-R2, mapped
not built). This proposal re-maps the *placement* the walls point toward; it authorizes no build.

**2.7 — Terminology (routes to the DL-053 register; terms proposed, not fixed).**

| Proposed canonical term | Meaning | Banned / not this |
|---|---|---|
| **Execution-stage monitoring (manual)** | Basic. User-driven, on-demand ingest of execution actuals vs. plan; maintained monitored state. | "continuous monitoring", "manual sync" |
| **Continuous monitoring** | Pro. Automated, event/schedule-triggered watch + auto-import + two-way sync. | "manual monitoring", "execution-stage monitoring" |

⚠️ **"phase" is already load-bearing.** DL-102 **D124** uses PHASE for the *supply* limit (Alpha/Beta),
and "stage" appears in `confidence_stage` (Understanding State). The plan→execution lifecycle must NOT be
called "phase". Proposed here as **planning stage / execution stage**; the exact term is the owner's call
via the DL-053 register.

## 3. Doctrine preserved (unchanged — this proposal touches none of it)

One accuracy bar for all — **judgment quality is never tiered** (DL-103 §1): Basic buys *access to the
execution stage*, never a better interpretation. The **epistemic record is never metered** (DL-102 D128).
**Reviewers/CRR and Viewers stay free forever** (DL-102 CR-2/E). **No forecast / probability of success**
(D003/D183b). **Flat per-account, never per-seat** (DR-7). **Limit-reached is a named choice, never a
dark pattern** (DL-102 D124/E-1) — and because Basic opens a *new stage* Free never had (rather than
re-walling the free read), no comprehension is metered.

## 4. Review (Framework 001A — five outputs)

- **Findings.** (1) The split is well-founded: DL-083's Pro-only placement rested on the *continuous-
  polling* cost, which the manual form does not incur — so the cost rationale does not bind the manual
  form. (2) It resolves a live self-contradiction in canon (DL-172 §7 vs DR-7 on sync) in DR-7's favor.
  (3) It *strengthens* Pro rather than hollowing it: automation + programme support is a more defensible
  $79 line than the status quo, and gives a legible, honest upgrade trigger ("stop doing this by hand").
  (4) It directly answers DL-083 Concern 2 (corpus breadth) — more users feed execution actuals.
  (5) The owner's capacity-drives-upgrade logic is consistent with the ratified capacity meters (active
  projects Free 1 / Basic 3, envelope) and with "gate capacity, not judgment quality."

- **Concerns.** (a) **Differentiator discipline (the trap).** Basic's manual monitoring must remain a
  *maintained execution-stage state* (actuals + delta/trend over time), not merely the free plan re-read
  behind a wall — otherwise it meters comprehension (D126 / DL-102 D124/E-1). Mitigated by scoping the
  execution stage as a distinct capability (2.1); realization must hold this line. (b) **Pro still
  PROVISIONAL.** This eases but does not close Pro's price/value question; final Pro price stays open
  pending its full capability set (2.3). (c) **Anti-Assumption — "manual monitoring" scope undefined.**
  The exact mechanics (what actuals, ingest surface, one-shot vs. maintained state semantics) are not
  canon; placed at Basic here, this must not be read as authorizing a build — it routes to its own
  scoping. (d) **Cost re-derivation.** Even bounded, manual ingest carries some cost; Basic economics are
  a telemetry re-derivation (DL-103/105 O-1/O-3), never a spec guess.

- **Dependencies.** **Amends** DL-083 (execution-monitoring tier split) → `RELEASE_MODEL_AND_ALPHA_
  LADDER_V1` §3a. **Extends / partially supersedes** DL-172 §7 (sync → Pro). **Extends** DR-7 (Pro value
  line; PROVISIONAL note). **Updates** `RELEASE_1_TIER_DEFINITIONS_V1` §1 + §2c (the authoritative per-
  tier register). **Adds to** the DL-053 disambiguation register (§2.7). **Constrained by (unchanged):**
  DL-103 §1 (judgment quality never tiered), DL-102 D128/D124/CR-2, DL-048 (Free cost posture),
  DL-047 (advisory-only). **Given (not reopened):** DL-172 §2 (multi-outcome per plan at Basic).

- **Recommendation.** **Adopt** the manual/automated split and the ladder in §2, encoded as amendments
  to DL-083 and the Tier Definitions register, with the sync-conflict resolution and the terminology
  entries. Route the manual-monitoring mechanics and the programme-support scope to their own scoping.
  No engineering action at ratification; the capability builds in Beta per DL-083 phasing.

- **Status.** **Ratified as DL-206 (2026-08-09, Idris/Founder Console); staged in `release-2/`.** **Blocking questions: none** (the two definitions the owner
  set this session — execution-stage differentiator; sync → Pro — are incorporated). **Open (non-
  blocking):** final Pro price; exact canonical terms (DL-053 owner call); manual-monitoring + programme-
  support scoping; whether this lands to `main` or stays R2-isolated (see landing note).

## 5. Decision record body (for dl-land)

```
title: Manual execution-stage monitoring at Basic; automation + programme at Pro — execution-monitoring tier split
slug: execution-monitoring-manual-basic-tier
class: B (product scope / monetization placement; non-doctrinal)
decided_by: Idris (Founder Console)

## Decision
Amend DL-083: split execution monitoring by who drives updates. (1) Manual execution-stage monitoring — user-driven, on-demand ingest of execution actuals vs. plan, maintained as monitored state over time — is placed at Tier 2 / Basic (capacity-shaped; no continuous-polling cost). (2) Continuous/automated monitoring stays Tier 3 / Pro+, together with auto-import + two-way sync, resolving the DL-172 §7 vs DR-7 sync conflict in DR-7's favor (sync → Pro) and superseding DL-172 §7's "auto-import + two-way sync = Basic" clause. (3) Pro's value line = continuous monitoring + auto-import/two-way sync + programme/cross-plan execution support (Tier Definitions §1 / DL-083), easing but not closing Pro's PROVISIONAL price. Free is unchanged (plan read; re-upload; export a file). Organizing axis: Basic = manual/on-demand; Pro = automated/continuous. Non-doctrinal: judgment quality is never tiered, the record is never metered, reviewers/Viewers free, no forecast, flat per-account (all preserved). Phase: manual form is Beta/post-R2 (DL-083); no R2 build impact (DL-172 §5). Adds DL-053 register terms (execution-stage monitoring vs continuous monitoring); "phase" reserved for D124 supply limit. Manual-monitoring mechanics and programme-support scope route to their own scoping.

## Status
Ratified.
```

## 6. Landing steps (owner runs — AI does not land canon)

1. Commit this proposal + the amended register/artifacts on a branch → PR → green doc-integrity gate →
   owner merge. **Never push to main.** Update `RELEASE_1_TIER_DEFINITIONS_V1` §1/§2c, note the DL-083
   amendment in `RELEASE_MODEL_AND_ALPHA_LADDER_V1` §3a, and add the §2.7 terms to the DL-053 register.
2. Land the decision via dl-land (numbers stamp at merge):
   `gh workflow run dl-land.yml -R idris-manley/oslo-knowledge-base -f title="Manual execution-stage monitoring at Basic; automation + programme at Pro — execution-monitoring tier split" -f slug="execution-monitoring-manual-basic-tier" -f class="B" -f decided_by="Idris (Founder Console)" -f body="$(cat body.md)"`
   (Pass the §5 body via `$(cat file)` — the Actions web form strips newlines and fails `dl_records.py`.)
3. Owner approves the bot PR (approve-workflows → code-owner review → squash) to merge.

_Placement note: staged under `release-2/` (active working line). It amends DL-083 and the Tier
Definitions register (main canon) **and** R2 decisions (DL-172, DR-7); whether it lands to `main` or
stays R2-isolated is an owner call, consistent with the open staging thread (canon main tops at DL-156;
R2 DLs staged in `release-2/`)._

---
*Owner decision options: **(A)** adopt as proposed (recommended; written for A); **(B)** adopt the split
but keep two-way sync at Basic (declines the DR-7 conflict resolution); **(C)** adopt placements, defer
the Pro programme-support confirmation; **(D)** defer. AI drafted and recommends; only the owner ratifies
(Framework 001A).*

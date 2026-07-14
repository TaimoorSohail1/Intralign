## Decision

**1. Never tier the quality of judgment. (Doctrinal.)**
**One judgment-quality bar for every tier.** Tiers differentiate on **capacity, scope, speed, collaboration and capability — never on the accuracy of the read.** Model routing is chosen **by step** (cheap models for extraction; the best available for judgment) **for all users**, never **by tier**.
**Supersedes the design rule "Basic sells capacity; *Pro adds model quality*"** (`BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE`; `RELEASE_1_CALIBRATION_DEFAULTS_V1` §4c T3 routing row; DL-074 §4).
**Pro's differentiator becomes execution & program support** (+ speed/priority); **Team/Enterprise add governance & portfolio** (per-seat). Basic + Pro = the **individual** motion; Team + Enterprise = the **org** sale.

**2. The cost basis is stale and is hereby reopened.**
**DL-069** (Ratified, 2026-06-18) made an **internal Gemma on a local Llama runtime** the primary LLM and **demoted OpenAI/Anthropic to a disabled-by-default fallback**, expressly to remove external token cost. But **§4c (2026-06-05) and DL-074 (2026-06-19) derive every governor, price and the ~$3/mo Free ceiling from rented frontier pricing** — DL-074 postdating DL-069 by one day. **Every tier number in canon therefore inherits an assumption canon itself abandoned.** The tier ladder's numeric basis is **suspended pending re-derivation** (item 4).

**3. Commission the missing engine economics (E1–E3).**
A grep of `30_engineering/analysis_engine/` for *prompt caching · incremental · differential · scoped recompute · cache* returns **zero hits**: **Deep Pass is specified as a full re-derivation on every run.** AE-03 ratifies *"no change → no reanalysis"* but **nothing ratifies *scoped* reanalysis.** Commission:
- **E1 — Prompt caching / KV-cache reuse.** The plan corpus is stable between runs; pay full price only for the delta.
- **E2 — Incremental / scoped recompute.** A fix to one artifact re-analyzes **that artifact and its dependency closure**, not the whole corpus. (This is what AE-03 should have said.)
- **E3 — Evidence coalescing.** Reviewer responses arriving in a window settle into **one** run. Without it, collaborators silently consume the user's analysis budget and **CR-2 dies in practice** — users learn that asking for evidence costs them their own read and stop asking, killing the loop DL-102 exists to protect.

**Computed impact (§4c June-2026 price basis; 450k in / 50k out; 85% cache-hit; 5× scope reduction):**

| Scenario | $/analysis | Analyses/month at the $3 Free ceiling |
|---|---|---|
| Today (rented, brute-force) | $0.260 | **12** |
| + E1 prompt caching | $0.122 | 25 |
| + E2 incremental | $0.068 | 44 |
| **E1 + E2** | **$0.040** | **~74 (6.4×)** |

**No model change. No quality trade.** The Free tier's "~8 analyses/month" is **not an economic fact** — it is an artifact of a superseded rental basis and an unoptimized engine. **E1–E3 are the highest-leverage unbuilt work in the product.**

**4. Order of operations — tier numbers are re-derived, not tuned.**
(a) **Judgment-quality eval of the local model (DL-069)** against the CAF / issue-detection task — *empirical; cannot be settled on paper*. (b) Build **E1–E3**. (c) **Re-derive cost per analysis** from the real engine. (d) **Then** set tier numbers. **Tuning the ladder on the current basis would bake a ~6× penalty into pricing permanently.**

**5. The re-derived ladder sells scope, capability and collaboration — not analysis volume.**
Once E1–E3 land, analysis volume **ceases to be a scarce good** for an individual (a working month is ~20–40 analyses; the engine can deliver ~74 at Free's existing ceiling). Therefore:
- **Free** — the full core read on **one** plan; viral primitives (comments, sharing, **CRR**). Analyses generous: an **abuse ceiling, not a product limit**.
- **Basic** — capacity/scope: more plans, bigger plans.
- **Pro** — execution & program support (+ speed/priority).
- **Team** — collaboration as the product; **per seat**; governance.
- **Enterprise** — portfolio + org governance.

**6. One honest limit, in the user's currency: analyses per month — never tokens.**
Daily caps are demoted to **invisible rate-limits (burst-smoothers), not product limits** — §4c already concedes they are a *"burst ceiling, not the governor."* Consequently:
- **UP-1 (daily fix cap) and UP-2 (daily chat cap) are RETIRED.** They meter near-free actions and tax the two behaviours we most want: **applying a fix is the activation moment** (*fix → the read moves*), and **chat is comprehension — metering it violates D126 ("never meter who gets an answer")**. The analysis run, not the fix or the message, is what costs.
- **UP-6 (the monthly analysis budget) becomes the single primary limit**, disclosed honestly in analyses.
- **Seats stay tight below Team.** A $12 Basic granting 10 collaborator seats cannibalizes a $99–149-**per-seat** tier. **CHG-061 is unaffected** — virality runs on **unlimited Viewers** and **free Reviewers (CR-2)**, neither of which consumes a seat.

## Rationale

Tiering model quality means **Free and Basic users receive a less accurate read**. OSLO's core epistemic signal — **Reliability** (Coverage · Evidence availability · Assessability) — is a statement about **the plan and its evidence**. If judgment quality is tier-keyed, **Reliability becomes partly a function of the plan the user is billed on**, and the product must say *"your read is less reliable because you are on Free."* That converts a **truth signal into an upsell** and poisons the one number the entire product rests on. It is the same family as D126 and D128, and worse: metering **access** to understanding is uncomfortable; metering the **accuracy** of understanding is **self-refuting** for a product whose whole claim is that it tells you the truth about your plan.

Separately, the tier ladder was built on a cost-per-analysis figure that is both **derived from a superseded rental basis** and **inflated ~6× by a brute-force engine**. Pricing decisions taken on that basis are unsound.

## Conditions

1. **Epistemic invariants preserved.** Advisory-only; confidence = understanding maturity; issues close only via an analysis update; the three epistemic classes; **CR-2** (evidence-seeking never metered); **D124** (always name which limit); **D128** (never meter the epistemic record; never sell safety).
2. **DL-069 is reaffirmed, not amended** — this decision finally reflects it in the cost basis. Whether local inference *clears the judgment bar* is an **empirical** question and is **not** decided here.
3. **DL-074's structure and guardrails are preserved** — hybrid subscription + metered overage, per-Deep-Pass unit, **visible meter, user-set spend cap, threshold alerts, no silent overspend, no bill shock**, overage on **paid tiers only** (no Free purchase path). Only its **"Pro adds model quality"** clause and its rental-derived numeric basis are superseded.
4. **No tier numbers are set by this decision.** They are re-derived after (4a)–(4c). Any number stated here is illustrative arithmetic, not a ratified value.
5. **Anti-Assumption.** The judgment-quality eval, the seat counts, OD-10's coalescing window, the Free CRR cost ceiling and MON-04's global prompt cap remain **owner-open**.

## Supersedes / Amends

- **Supersedes** the design rule *"Pro adds model quality"* (`BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE`; §4c T3 routing row; **DL-074 §4**).
- **Suspends the numeric basis** of `RELEASE_1_CALIBRATION_DEFAULTS_V1` **§4c** (governors, daily caps, per-tier prices) pending re-derivation.
- **Retires MON-02 / MON-03 daily caps and UP-1 / UP-2** as product limits (they persist only as invisible rate-limits).
- **Amends DL-102 E** — the Basic collaborator-seat count (10) is withdrawn as commercially unsound against a per-seat Team tier; seats remain **owner-open**.
- **Extends AE-03** — scoped/incremental recompute (E2) and evidence coalescing (E3).
- **Reaffirms** DL-069 · DL-102 (CR-2, D124, D126, D128) · CHG-061 · DL-074's hybrid structure and guardrails.

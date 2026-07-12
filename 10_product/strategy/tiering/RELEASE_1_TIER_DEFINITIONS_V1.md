# Release 1 Tier Definitions v1

**Type:** Product Specification — **the single authoritative surface for every per-tier value**
**Status:** Realization of **DL-107** · **Product-authoritative.** · **Date:** 2026-07-12
**Consolidates (does not decide):** `RELEASE_1_CALIBRATION_DEFAULTS_V1` §4c · `BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE` · `12_freemium_tier_behavior_logic` (MON-01…04, UP-*) · **DL-048** · **DL-074** · **DL-083** · **DL-102** · **DL-103** · **DL-104** · CHG-061
**Cited as authoritative by:** ~18 documents, which have referred to *"Release 1 Tier Definitions"* since before it existed.

> ## Why this document exists
> **Eighteen canonical documents cite "Release 1 Tier Definitions" for seat, tier and sharing limits. It was never written.** The values lived instead in the **engineering** zone (`RELEASE_1_CALIBRATION_DEFAULTS_V1` §4c) and in a **backlog** item — invisible to any product-scoped reader, human or machine.
>
> **The consequence is documented, not hypothetical.** An AI contributor twice proposed numbers that canon had already settled — *"Basic = 10 projects"* against a ratified **Basic = 3** (UP-3), and *"Basic's price is undecided"* against a confirmed **$12/mo**. One reached an open pull request. **A reader who cannot find a number will invent one.**
>
> **This document is a REGISTER, not a decision.** It **states each value and its status**. It decides nothing. Where a value is suspended or open, it says so — because *"this is unset"* is information, and its absence is what caused the failures above.

---

## 0. How to read the status column

| Status | Meaning |
|---|---|
| **RATIFIED** | Settled canon. **Cite it. Do not re-propose it.** |
| **SUSPENDED** | Ratified, but its **numeric basis is suspended by DL-103** pending re-derivation from the real engine. **Do not treat as settled; do not replace with an invention.** |
| **RETIRED** | Ratified, then **withdrawn**. Kept visible so it is not re-derived from a blank. |
| **OPEN** | **No canonical value exists.** `TBD – Owner Decision Required`. **Do not fill it.** |

---

## 1. The ladder — what each tier SELLS (structure: RATIFIED)

| Tier | What it sells | Metered on |
|---|---|---|
| **T1 · Free** | **The full core read on ONE plan** + the viral primitives (comments · sharing · **CRR**) | 1 project · small envelope. **Analyses are an abuse ceiling, not a product limit** (DL-103 §5) |
| **T2 · Basic** | **Capacity / scope** — more plans, bigger plans. Plus connected sources, the reporting suite, export/sync | Projects · envelope |
| **T3 · Pro** | **Execution & programme support** (DL-083) | Capability |
| **T4 · Team** | **Collaboration as the product** — governance | **Per seat** |
| **T5 · Enterprise** | **Portfolio** + org governance | Contract |

**Basic + Pro = the individual motion. Team + Enterprise = the org sale.** *(Owner, 2026-07-11.)*

> ### ⛔ **JUDGMENT QUALITY IS NEVER TIERED** (DL-103 §1 — doctrinal)
> **Model routing is chosen BY STEP (cheap for extraction; best-available for judgment) — NEVER BY TIER.** Every user receives the same judgment.
> **This SUPERSEDES** §4c's tier-keyed routing rows and the design rule *"Pro adds model quality"* (**RETIRED**, DL-103 §1 / DL-104 §1).
> **Rationale:** a tier-keyed model would make **Reliability a function of the billing plan** — converting OSLO's core truth signal into an upsell.

---

## 2. Per-tier values — the register

### 2a. Scope

| Value | Free | Basic | Pro | Team | Enterprise | Status | Source |
|---|---|---|---|---|---|---|---|
| **Active projects** | **1** | **3** | 10 | many | custom | **RATIFIED** | **UP-3**; §4c |
| **Project envelope** (docs / words) | ~20 / 50k | ~40 / 100k | ~80 / 200k | ~150 / 400k | custom | **RATIFIED** | §4c; UP-4 |
| **Collaborator seats** | — | — | — | *per seat* | custom | **OPEN** ⚠️ | *see 3a* |
| **Viewers** | unlimited | unlimited | unlimited | unlimited | unlimited | **RATIFIED** | DL-102 E |
| **Reviewers (CRR)** | **free · unmetered** | free · unmetered | free · unmetered | free · unmetered | free · unmetered | **RATIFIED** | **DL-102 CR-2** |

### 2b. Analysis

| Value | Free | Basic | Status | Source |
|---|---|---|---|---|
| **Monthly analysis budget** *(expressed in **ANALYSES**, never tokens)* | — | — | **SUSPENDED** ⚠️ | DL-103 §2/§6 — **re-derived from DL-105 §4 telemetry** |
| Monthly token governor *(the old basis)* | 4M | 10M | **SUSPENDED** | §4c — **derived from a rented-token model DL-069 abandoned** |
| Deep runs / day | 2 | 6 | **RETIRED** as a product limit | DL-103 §6 / DL-104 §2 — survives only as an **invisible rate-limit** |
| Suggested fixes / day (**assisted apply**) | — | — | **OPEN** ⚠️ | **UP-APPLY** (DL-104 §3). *Above activation, below power use — **set from Alpha instrumentation, never from a cost model**. Until that data exists: **no cap**.* |
| Chat messages / day | **uncapped** | uncapped | **RETIRED** | DL-103 §6 — *metering comprehension violates D126* |
| **Free monthly cost posture** | ~$3 / active user | — | **RATIFIED** (posture) · basis **SUSPENDED** | DL-048 |

### 2c. Capability

| Value | Free | Basic | Pro+ | Status | Source |
|---|---|---|---|---|---|
| **The core read** (intake → orientation → attention → issues → **CRR**) | ✅ **full** | ✅ | ✅ | **RATIFIED** | MON-01 + **CHG-061** |
| **Artifacts · History** | **unlimited · permanent** | ✅ | ✅ | **RATIFIED** | **DL-102 D128** — *the epistemic record is NEVER metered* |
| **Link security** (revocation · scoped expiry) | ✅ | ✅ | ✅ | **RATIFIED** | **DL-102 D128** — *never sell safety* |
| Export | **PDF only** | all formats | all | **RATIFIED** | MON-01; SHARE-04 |
| Reporting — the readout | **read snapshot (PDF)** | **composable + persistence + branding + scheduling** | ✅ | **RATIFIED** *(shape)* | **DL-108** (M4); CHG-061 |
| **Report editing** | ✅ **free** | ✅ free | ✅ | **RATIFIED** | **DL-108 / D154** — *the gate is REUSE, never the ability to own your own words* |
| Connected sources / integrations | — | ✅ | ✅ | **RATIFIED** *(shape)* | freemium Constrain list; DL-103 §7f |
| Plan export → execution tool | — | ✅ | ✅ | **RATIFIED** | **DL-083** |
| Execution monitoring | — | — | ✅ **Pro+** | **RATIFIED** | **DL-083** (built in Beta) |

### 2d. Commercial

| Value | Free | Basic | Pro | Team | Enterprise | Status | Source |
|---|---|---|---|---|---|---|---|
| **Price** | $0 | **$12 / mo** | ~$39 / mo | ~$99–149 **/ seat** | custom | **RATIFIED** · basis **SUSPENDED** | §4c (owner-confirmed 2026-06-05); **DL-074** |
| **Overage** | **none — no Free purchase path** | per-Deep-Pass | ✅ | ✅ | contract | **RATIFIED** | **DL-074 §3** |
| Overage guardrails | — | **visible meter · user-set spend cap · threshold alerts · no silent overspend · no bill shock** | ✅ | ✅ | ✅ | **RATIFIED** | **DL-074 §5** |
| **Outcome-based pricing** | **PROHIBITED** | PROHIBITED | PROHIBITED | PROHIBITED | PROHIBITED | **RATIFIED** | **DL-103 §7h** — *it would require charging against delivery results OSLO deliberately refuses to predict* |

---

## 3. OPEN — `TBD – Owner Decision Required`. **Do not fill these.**

### 3a. ⚠️ Collaborator seats — the one undefined dimension in the whole ladder
**§4c has no seat row below Team.** The only proposal on record (**Free 3 / Basic 10**, DL-102 E) was **withdrawn as commercially unsound**:
> **Team is priced ~$99–149 PER SEAT. A $12 Basic granting 10 collaborator seats means a ten-person team buys ONE Basic instead of Team. It cannibalizes Tier 4.**

**The constraint is structural, and CHG-061 is not at risk:** the viral primitives run on **unlimited Viewers** and **free Reviewers (CR-2)** — **neither consumes a seat**. So **seats can be tight across Free/Basic/Pro without gating the seed.** *Individual tiers grant enough collaboration to do your own work; **Team is where collaboration becomes the product**.*
**The number is the owner's. The constraint is not.**

### 3b. The rest

| # | Open value | Note |
|---|---|---|
| **O-1** | **Monthly analyses** (Free / Basic) | **In analyses, never tokens.** Re-derived from **DL-105 §4 telemetry** — *cost-per-analysis cannot be derived from a specification.* |
| **O-2** | **UP-APPLY threshold** (assisted-apply cap) | From the **observed fixes-per-session distribution** in Alpha. **Never from a cost model** — under coalescing the fix itself is near-free. **No data → no cap.** |
| **O-3** | **Basic price *basis*** | The **$12 is confirmed**; the **derivation is suspended** (rented-token model). Re-derive; the number may stand. |
| **O-4** | **Extended-Analysis budget shape → numbers** | Shape ratified (Free small / Basic generous). |
| **O-5** | **Free CRR cost ceiling** (B-1) | **An abuse/cost guard only. It may NEVER fire an upgrade prompt** (DL-102 B-1). |
| **O-6** | **MON-04 global prompt cap / day** | Required by MON-04; never set. Build **errs toward silence.** |
| **O-7** | **OD-10 coalescing window** · **OD-CRR** | See `RELEASE_1_ANALYSIS_COST_OPTIMIZATION_SPECIFICATION_V1`. |
| **O-8** | **Report names** · scheduling R1-vs-fast-follow · branding tier · report length | See `RELEASE_1_REPORTING_SPECIFICATION_V1`. |
| **O-9** | **Billing rail** | Engineering. |
| **O-10** | **Reverse-trial duration** | Mechanic ratified (DL-103 §7e); duration is not. |

---

## 4. Standing constraints — these bind every tier value, forever

1. **Never tier judgment quality** (DL-103 §1). Routing by **step**, never by **tier**.
2. **Never meter the epistemic record** (DL-102 D128). **Artifacts uncapped. History never expires.**
3. **Never sell safety** (DL-102 D128). Link revocation and scoped expiry are **free on every tier**.
4. **Never meter evidence-seeking** (DL-102 **CR-2**). Reviewer grants and review requests are **free and unmetered — on every tier, in every phase.**
5. **Two limits, never conflated** (DL-102 D124). **PHASE** (supply) ≠ **TIER** (depth). **Always name which one blocked the user.** Presenting a supply constraint as an upsell is a **prohibited dark pattern**.
6. **Limit-reached rule** (DL-102 E-1). The affordance **stays enabled**; the *attempt* is gated; the prompt names **the specific limit AND the specific tier that relieves it**, with resolutions. **Never disabled, never hidden, never a raw error.**
7. **No eviction on downgrade** (DL-102). **No human is ever removed** to enforce a billing change.
8. **Outcome-based pricing is PROHIBITED** (DL-103 §7h).
9. **Numbers are instrumented hypotheses, not truths.** Chosen to be **easy to loosen and painful to tighten**. Re-derived from telemetry — **never from a specification.**

---

## 5. Amendment rule

**Every per-tier value in Release 1 belongs HERE.** A number that lives only in an engineering config, a backlog item, or a decision body **will not be found by the people who need it** — and **a reader who cannot find a number will invent one.** That is the failure this document exists to end.

**Adding or changing a value: route through Framework 001 → `dl-land` → update this register.**

# Tier-Definitions Census — Slice 10 (D140)

---

# ⚠️⚠️ AMENDED 2026-07-12 — **DL-103 IS RATIFIED. READ THIS FIRST; EVERYTHING BELOW IT IS SUBORDINATE.**

**`00_owner/decisions/records/DL-103-analysis-cost-basis-and-tier-rederivation.md` (Ratified, Class A)** supersedes the tier model this slice was built on. **Nothing prior to this section is deleted** — per the house rule, the correction must stay legible — but where it conflicts with what follows, **DL-103 wins.**

## The ten changes

| # | DL-103 | What changed in the build |
|---|---|---|
| **§1** | **NEVER TIER JUDGMENT QUALITY. (Doctrinal.)** One judgment bar for every tier. Routing is chosen **by step** (cheap models to extract; the best available to judge) — **never by tier**. **Supersedes "Basic sells capacity; *Pro adds model quality*"** (§4c T3 · DL-074 §4 · the monetization backlog). | The `ROUTING` per-tier ladder is **struck** → `MODEL_ROUTING_BY_STEP`. Every "Pro is where the models get better" / "the quality upsell" line is gone. Pro = **execution & programme support**. Guard: `_assertNoTierKeyedModelQuality()`. |
| **§2/§4** | **The cost basis is stale; the §4c numeric basis is SUSPENDED.** §4c/DL-074 derive every governor and price from **rented frontier pricing** — which **DL-069 had already abandoned** (local Gemma/Llama runtime) *one day earlier*. Tier numbers are **re-derived, not tuned**. | Every former "RATIFIED" number sourced from §4c's cost model now renders **PENDING RE-DERIVATION**. `BASIC_PRICE = 12` is kept **with a pending-basis marker** — the value is owner-confirmed; its **basis** is not. |
| **§3** | **E1–E3 commissioned** — prompt caching · incremental/scoped recompute · evidence coalescing. **~6.4× cheaper. No model change. No quality trade.** *(E3 is load-bearing for CR-2: without it, collaborators silently consume the user's budget, users learn that asking for evidence costs them their own read — **and stop asking**.)* | Surfaced honestly in UP-6, the budget meter and chat: *"the limit you are looking at is an artifact of an engine we are fixing, not an economic fact."* Illustrative arithmetic (~12 today → ~74 with E1+E2) is shown **labelled as illustrative**. |
| **§5** | **The re-derived ladder.** Free = the full core read on **one** plan + viral primitives; analyses are an **abuse ceiling, not a product limit**. Basic = **capacity/scope** (3 projects · bigger plans · connected sources · reporting · export/sync). Pro = **execution & programme support**. Team = **collaboration, per seat**. Enterprise = **portfolio + governance**. | `renderPlans()` rebuilt end-to-end on this ladder. |
| **§6** | **ONE honest limit, in the user's currency: ANALYSES per month — never tokens.** **UP-1 (daily fix cap) and UP-2 (daily chat cap) are RETIRED.** Daily caps are demoted to **invisible rate-limits (burst-smoothers)**. **UP-6 becomes the primary prompt.** | The token governor is gone. `ANALYSIS_BUDGET = {free:null, basic:null}` → **pending; nothing is enforced.** **Chat is uncapped, on every tier** (the gate in `sendChat` is deleted). UP-5 also goes as a product limit; UP-6 carries its honest *"keep the last analysis"* resolution. Guards: `_assertBudgetInAnalyses()`, `_assertChatNeverCapped()`. |
| **§7d** | **The daily ASSISTED-APPLY cap is RETAINED** — it is *labour*, not comprehension. **BINDING: the recommendation is ALWAYS visible · only the assisted apply is metered · MANUAL EDITING IS ALWAYS FREE.** Placement: **above activation, below power use.** **Number from Alpha instrumentation, NEVER a cost model → until the data exists, NO CAP.** | New prompt **UP-APPLY** (⚠️ no canon UP-number — escalated). `ASSISTED_APPLY_CAP.free = null` ⇒ **inactive**. First resolution is a real one-click action: **"Make the edit yourself — free, right now."** Basic gets **"Apply all recommended fixes."** Guard: `_assertRecommendationNeverHidden()`. |
| **§7d-bis** | **Refresh cadence.** The coalescing window keys off **the user's journey (new ▸ established), NEVER the tier.** The tier lever is **auto vs manual refresh**. **BINDING: "Update now" is FREE ON EVERY TIER.** | `updateNow()` — **no tier check exists, and none may be added.** Free: slow auto + Update now. Basic: continuous. Refresh still draws on the monthly budget. Guard: `_assertUpdateNowFreeOnEveryTier()`. |
| **§7c** | **LABOUR, NOT LATENCY. The priority-queue / speed lever is STRUCK.** An async product cannot sell speed. Fast Pass never queues — **a product guarantee (DL-046), not a lever**. **Artificial delay PROHIBITED.** | **Not built.** Said out loud on the Plans page (*"the upgrade we deliberately did not build"*). Guard: `_assertNoPriorityQueueLever()`. |
| **§7e** | **Reverse trial** (~14 days on Basic, then Free) — **a GA-phase mechanic**. **BINDING: TAKE BACK THE PIPES, NEVER THE READ.** | Gated behind `PHASE==='ga'` (DL-102: in Alpha everyone is invited). Downgrade takes **integrations · reports · continuous auto-refresh · extra live plans**; it **never** takes **History · issues · artifacts · chat · the read**. Guard: `_assertDowngradeNeverRemovesUnderstanding()`. |
| **§7h** | **OUTCOME-BASED PRICING IS PROHIBITED.** OSLO deliberately refuses to predict delivery outcomes. | Nothing prices or markets on outcomes. Said out loud on Plans. Guard: `_assertNoOutcomePricingCopy()`. |
| **§7j** → **D143–D147** | **REPORTING (M4) is the #1 lever — and it is a STATUS lever.** ⚠️ **SUPERSEDED 2026-07-12 (owner: "accept all"): there are NOT six report types. There is ONE composable readout.** Free = the **read snapshot** (spine §1–§5, PDF, OSLO-marked — CHG-061, the seed is never gated); Basic = the **composable readout** (optional sections, branding, scheduling, all export formats). | **REBUILT surface: Readout** (nav + modal + live composer). **Fixed spine §1–§5** (`_spineRead()` + `_spineAsk()`), optional sections at Basic, **live composer → dated snapshot** on export. **BINDING: tailor the ASK, never the READ** — §1–§3 are byte-identical for every recipient. Reliability-qualified throughout · **confidence = understanding maturity, never health/readiness/RAG/probability (a P1 defect class — DL-104 §5)** · analysis-currency marker (stale = **"previous analysis"**) · standing disclaimer · **packages, never produces** · no fabricated completeness. **Names are owner/glossary — descriptive, "naming pending"; "status report" is ruled out by design.** Guards: `_assertReadoutSpineComplete()` · `_assertAskTailoredNeverTheRead()` · `_assertReportPackagesNeverProduces()` · `_assertScheduledReportRechecksCurrency()` · `_assertReportsNoHealthFraming()`. |

## §7f — the in-plan conversion moments, surfaced honestly (not sprung)

connected sources (day 1, forever) · reporting (weekly) · export/sync → execution tool (DL-083, Basic) · bulk actions · **one live understanding** (archived = read-only, the read freezes; **archive stays reversible**, DL-058) · the **envelope** (UP-4 partial read, honestly disclosed) · **plan 2** (a pull, not a wall).

## §7g — upgrade mechanics

**One click. Self-serve. Price on the button. No sales call, ever.** Triggers on **behaviour and realized value, never a calendar** — the value-moment class (UP-7/UP-8) is **strengthened**, not an afterthought.

## The guardrails that did NOT move

Never meter the epistemic record (artifacts uncapped · History never expires) · never sell safety · **CR-2** (evidence-seeking never bounded) · **D124** (never present a PHASE limit as a TIER upsell) · no eviction on downgrade · no fabricated scarcity · **MON-04** (no upgrade wallpaper) · every prompt names the specific limit **and** the specific tier · **no invented numbers — unset renders unset** · advisory-only (chat never mutates).


**REWRITTEN 2026-07-11.** The first version of this census said **21 RATIFIED / 11 UNSET**. **That was wrong**, and the reason it was wrong is the most important finding in this document.

---

## ⚠️ Correction of record — read this before the table

> ### The tier values were never missing. They were in the engineering zone, and we did not look there.
>
> This census was built from a scan of **`10_product/`** and **`00_owner/`** — the product-grill discipline. **The full, owner-confirmed tier ladder does not live there.** It lives in:
>
> **`30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1` — §4c** *(Cost Governance / Freemium Unit Economics)*
>
> §4c carries **owner-confirmed rows for every tier**: price, active projects, project-size envelope, deep runs/day, fixes/day, chat/day, model routing, per-run token caps, daily token budget, and the **monthly token governor**. Free and Basic were **owner-confirmed on 2026-06-05**; Pro, Team and Enterprise were **ratified via DL-074 on 2026-06-19**.
>
> **Consequently, five values this build rendered as "owner-TBD / UNSET" were ratified all along:**
>
> | Rendered as | Actually |
> |---|---|
> | Basic price — *"owner-TBD (T-3)"* | **$12/mo** — §4c, owner-confirmed 2026-06-05 |
> | Basic chat/day — *"UNSET; canon gives direction only"* | **75/day** — §4c |
> | Basic deep runs/day — *"UNSET; canon says only 'more'"* | **6/day** — §4c (and §4c calls it a **burst ceiling**, not the gate) |
> | Free / Basic size envelope — *"UP-4's ~100k words is illustrative, not ratified"* | **Free ~20 docs / ~50k words · Basic ~40 / ~100k** — §4b (CHG-056, owner-confirmed) + §4c. The "~100k words" is **not** an illustration; it is **Basic's envelope**. |
> | Monthly budget gate (UP-6) — *"threshold never decided; the build enforces nothing"* | **The monthly token governor** — Free **4M** · Basic **10M**. §4c calls it, verbatim, **"the binding governor."** |
>
> And one value the build marked **RATIFIED is not**: the **collaborator seat caps**.

### The root cause — and it is not a missing number

**18 product documents cite a `RELEASE_1_TIER_DEFINITIONS_V1` that has never been written.** The values it would contain **already exist** — but in **engineering configuration**, under a different name, consolidated nowhere. A product-scoped reader (a person, or a model) does not find them. An AI that cannot find a number **invents one**.

That has now happened **twice** in this engagement:

1. **"Basic = 10 projects"** — canon (§4c / UP-3) says **3**. Reached an open PR; **withdrawn on the record** (DL-102 Correction #3).
2. **"Basic's price is undecided"** — canon (§4c) says **$12/mo**, owner-confirmed. Corrected here.

> **`RELEASE_1_TIER_DEFINITIONS_V1` must therefore be written as a product-authoritative surface that CONSOLIDATES AND NAMES what is already ratified — not as a document that decides anything new.** It has roughly **six** real decisions left to make. They are listed at the end.

**A hole you cannot find is worse than a hole you can.** The fix is a product-authoritative surface, not a better guess.

---


---

# ⬛ THE RE-DERIVED CENSUS (DL-103, 2026-07-12) — **THIS TABLE SUPERSEDES THE ONE BELOW IT**

**58 values · 39 ratified · 3 PENDING RE-DERIVATION · 8 RETIRED/STRUCK · 5 UNSET · 3 RECOMMENDATION.**

> **The headline finding of the previous pass has itself been superseded.**
> That pass concluded: *"the numbers were never missing — they were in the engineering zone (§4c) and we did not look there."* **That was true, and it was not enough.** DL-103 establishes that **the numbers we finally found are derived from a cost basis canon had already abandoned.**
>
> **§4c (2026-06-05)** and **DL-074 (2026-06-19)** derive every governor, price and the ~$3/mo Free ceiling from **rented frontier-model pricing**. But **DL-069 (2026-06-18)** had already made an **internal Gemma on a local Llama runtime** the primary LLM — expressly to remove external token cost. **DL-074 postdates DL-069 by one day.**
>
> **So every tier number in canon inherits an assumption canon itself abandoned** — and the engine compounds it: a grep of the analysis engine for *prompt caching · incremental · scoped recompute* returns **zero hits**. Deep Pass is a **full re-derivation on every run** — roughly **6× more expensive than it needs to be**.
>
> **Therefore: the ladder's numeric basis is SUSPENDED. Tier numbers are RE-DERIVED, NOT TUNED.** Tuning them now would bake a ~6× penalty into pricing permanently.

## Five statuses now, not three — and the difference is the whole point

| Status | Meaning |
|---|---|
| ✅ **RATIFIED** | Canon decided it and the basis holds. Adopted + cited at the consuming site. |
| ⏳ **PENDING RE-DERIVATION** | The owner **did** decide — **on a basis canon has since abandoned**. The number is **shown, marked, not enforced, and never sold against**. It is *not* "unset" (nobody decided) and *not* "ratified" (settled). |
| ⛔ **RETIRED / STRUCK** | It was ratified, and a later decision **struck it**. **Kept in the census, visibly struck, so nobody re-derives it from a blank in six months.** |
| ⬜ **UNSET** | Nobody has decided. Renders visibly unset. Enforces nothing. Never guessed. |
| ⚠️ **RECOMMENDATION** | The build carries a number canon has not ratified, labelled as exactly that, in-product. |

## ⏳ PENDING RE-DERIVATION (3) — *was: "RATIFIED"*

| Value | Was | Now | Why |
|---|---|---|---|
| **Monthly budget — Free** | *"4,000,000 tokens — the binding governor (§4c), RATIFIED"* | ⏳ **pending; in ANALYSES, never tokens; nothing enforced** | Suspended basis (§2/§4). Illustrative arithmetic only: ~**12** analyses/mo on today's engine ⇒ ~**74** with E1+E2. **Free's "~8 analyses/month" is not an economic fact.** |
| **Monthly budget — Basic** | *"10,000,000 tokens"* | ⏳ **pending** | Same. |
| **Basic price** | *"$12/mo — RATIFIED (§4c, owner-confirmed)"* | ⏳ **$12 kept, with a pending-BASIS marker** | The **value** is owner-confirmed. Its **basis** is suspended. The build neither changes the number nor drops it — it says what is unsettled about it. |

## ⛔ RETIRED / STRUCK (8) — *all were "RATIFIED" one pass ago*

| Value | Was | Struck by |
|---|---|---|
| Daily fix cap — Free | **5/day** (§4c · MON-02 · UP-1) | **§6.** Fires **during activation** — and *"applying a fix is the activation moment."* Activated users convert at **35–65%** vs **2–8%**. Replaced by the **assisted-apply** cap (§7d) with a different placement and **no number yet**. |
| Daily fix cap — Basic | **20/day** | §6 |
| Daily chat cap — Free | **20/day** (MON-03 · UP-2) | **§6.** *"Chat is comprehension — metering it violates D126."* **Chat is now uncapped on every tier.** |
| Daily chat cap — Basic | **75/day** (the value the *previous* pass proudly "recovered" from §4c) | §6 |
| Daily analysis cap — Free | **2/day** (UP-5) | **§6 — demoted to an invisible rate-limit.** Not a product limit; never surfaced as one; **no upgrade prompt may key off it.** |
| Daily analysis cap — Basic | **6/day** | §6 |
| **Model-routing ladder** (Free nano/mini · Basic "same class" · **Pro "the quality upsell"** · Team "premium") | §4c routing rows + DL-074 §4 | **§1 — DOCTRINAL.** Routing is **by step, for everyone**. Tier-keying judgment would make **Reliability partly a function of the user's bill**. |
| **Priority queue / "Basic runs it now"** · **Outcome-based pricing** | *(candidate levers)* | **§7c / §7h — struck and prohibited.** |

## ⬜ UNSET (5) and ⚠️ RECOMMENDATION (3) — the genuinely open list

| # | Item | Status | The decision the owner owes it |
|---|---|---|---|
| **1** | **Daily ASSISTED-APPLY cap — Free** *(NEW)* | ⬜ UNSET | **From Alpha instrumentation** (observed fixes-per-session distribution), **NEVER from a cost model**. **Placement is the whole decision: above activation, below power use.** **Until the data exists: no cap.** It is a **monetization lever and the record says so plainly.** |
| **2** | **Monthly analyses — Free / Basic** | ⏳ PENDING | Re-derive after (a) the judgment-quality eval of the local model, (b) **E1–E3**, (c) a real cost-per-analysis measurement. **Then** set it. Expect an **abuse ceiling, not a product limit**. |
| **3** | **Collaborator seats — Free / Basic** | ⚠️ REC | Unchanged, and **sharpened**: DL-103 **withdraws Basic = 10** as commercially unsound (Team is **per seat**). Still the only structurally undefined dimension. **The build does not invent a replacement.** |
| **4** | **OD-10 coalescing window** | ⬜ UNSET | **Sharpened by §7d-bis: it keys off the USER'S JOURNEY (new ▸ established), never the tier.** Tight while new (they *see* the read move — the aha); settle-based once established. |
| **5** | **Free CRR cap** | ⬜ UNSET | Unchanged (B-1 cost ceiling; may gate depth/volume, never existence; **never fires an upgrade prompt**). |
| **6** | **MON-04 global prompt cap / day** | ⬜ UNSET | Unchanged. |
| **7** | **CR-2 vs the budget gate** | ⚠️ REC | Unchanged (**record · defer · disclose**) — and **§3's E3 (evidence coalescing) is the real fix**: without it, reviewers silently consume the user's budget and **CR-2 dies in practice**. |
| **8** | **Billing rail** | ⬜ UNSET | Unchanged (T-4). Must carry DL-074 §5 **and** §7g (one click, self-serve, no sales call). |

## ✅ NEWLY RATIFIED BY DL-103 (adopted + cited in the build)

| Value | Setting |
|---|---|
| Model routing — **every tier** | **By step, never by tier** — cheap models to extract; **the best available model to judge**, for everyone |
| What Pro adds | **Execution & programme support** — *not* a better brain |
| What the budget is counted in | **ANALYSES — never tokens** |
| What counts against the budget | **The analysis run** — not the fix, not the message |
| Free's budget — what *kind* of limit | **An abuse ceiling, not a product limit** |
| **Manual editing** | **Always free, every tier** *(this is what makes the assisted-apply cap legitimate)* |
| **OSLO chat** | **Never capped, any tier** |
| **"Update now" (manual refresh)** | **FREE ON EVERY TIER** *(binding condition)* |
| Auto-refresh | Free: slow · Basic: continuous *(the permitted lever is **automation**)* |
| Coalescing window keys off | **The user's journey — never the tier** |
| Assisted apply — Basic | **Apply freely + "Apply all recommended fixes"** |
| Reporting — Free *(D147)* | **The read snapshot: the FULL SPINE §1–§5, as a PDF, OSLO-marked — the seed is never gated (CHG-061)** |
| Reporting — Basic *(D147)* | **The composable readout: optional sections + branding + scheduling + all export formats.** *The seed is not gated; the depth is.* |
| Reporting — how many report types *(D143)* | **ONE.** A composable readout — **not six.** *(The six-type scaffold is deleted.)* |
| Reporting — scheduling: R1 or fast-follow | ⬜ **OWNER-OPEN** — built and flagged (`SCHEDULING_R1 = null`) |
| Reporting — branding tier | ⚠️ **Built at Basic** (D147) — **owner-open** whether it belongs there or higher |
| Reporting — the artifact's NAME | ⬜ **UNSET** — owner/glossary (DL-053). Descriptive label + "naming pending". **"Status report" and any health/readiness name are ruled out by design.** |
| Priority queue / latency lever | **STRUCK — not built** |
| Outcome-based pricing | **PROHIBITED** |

*(The table below this line is the pre-DL-103 census. It is retained, unedited, so the correction remains legible. Where it conflicts with the above, **the above wins.**)*

## Summary *(SUPERSEDED — pre-DL-103)*

| | Count |
|---|---|
| Values the product consumes | **53** |
| ✅ **RATIFIED** (canon decided; adopted + cited at the consuming site) | **46** |
| ⚠️ **RECOMMENDATION** (the build carries a number canon has *not* ratified; labelled in-product) | **3** |
| ⬜ **UNSET** (owner decision required; renders visibly unset) | **4** |

The 3 + 4 collapse to **6 genuinely open decisions** (the two seat rows are one dimension):

1. **Collaborator seats — Free / Basic / Pro** *(RECOMMENDATION — and the ONLY undefined dimension in the ladder)*
2. **OD-10 — the Deep-Pass coalescing window** *(UNSET — the highest-leverage number in the product)*
3. **Free CRR cap** *(UNSET — B-1 cost ceiling)*
4. **MON-04 global upgrade-prompt cap / day** *(UNSET)*
5. **CR-2 vs the binding governor** *(RECOMMENDATION — what happens to evidence that arrives after the gate)*
6. **Billing rail** *(UNSET — engineering, T-4)*

**Everything else is ratified and should be cited, not re-decided.**

---

## The ratified ladder (all of it — nothing here is proposed by this build)

| | **Free (T1)** ✓ | **Basic (T2)** ✓ | **Pro (T3)** | **Team (T4)** | **Enterprise (T5)** |
|---|---|---|---|---|---|
| **Price** | **$0** (CAC/subsidy) | **$12 / mo** | **~$39 / mo** | **~$99–149 / SEAT** | custom / contract |
| Active projects | 1 | 3 | 10 | many (per seat) | custom |
| Envelope (docs / words) | ~20 / 50k | ~40 / 100k | ~80 / 200k | ~150 / 400k | custom |
| Extended (deep) runs / day | 2 | 6 | 15 | on-demand | custom |
| Fixes · chat / day | 5 · 20 | 20 · 75 | 50 · 200 | high / unmetered | custom |
| Model routing | nano / mini | nano / mini *(same class)* | mini + full-quality fallback | **premium** | premium + dedicated |
| **Monthly token governor** | **4M** | **10M** | 25M | 50M / seat | negotiated |
| Worst-case cost / mo | ~$3 | ~$8 | ~$20 | ~$97 | — |
| **Collaborator seats** | **⚠️ undefined** | **⚠️ undefined** | **⚠️ undefined** | **per seat** *(that IS the pricing unit)* | custom |

**Sources:** `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4b/§4c` (T1/T2 owner-confirmed 2026-06-05; T3–T5 via DL-074) · `00_owner/decisions/records/DL-074-hybrid-pricing-multi-meter.md` (Ratified 2026-06-19) · `00_owner/backlog/BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md` (taxonomy, owner-set 2026-06-05) · UP-1/2/3/5 · DL-048 · DL-083.

**Design rule (ratified):** *Basic sells **capacity**; Pro adds **model quality**; Team/Enterprise are **per-seat** with premium routing.*
**Owner clarification (2026-07-11):** Pro also adds **execution & program support**; Team/Enterprise add **governance & portfolio**. **Basic + Pro = the individual motion; Team + Enterprise = the org sale.**

**Hybrid pricing (DL-074, Ratified):** each tier = subscription (capacity + quality + a usage envelope) **+ metered overage above the envelope**, unit = **per Deep Pass**, under a "usage-based" umbrella. Guardrails: **visible meter · user-set spend cap · threshold alerts — no silent overspend, no bill shock.** **Overage is PAID TIERS ONLY.** *"Free converts via upgrade… no Free purchase path."* Abstract token credits were weighed and **rejected**.

---

## The census

Status key: ✅ **RATIFIED** (adopted + cited) · ⚠️ **RECOMMENDATION** (carried, labelled in-product, not canon) · ⬜ **UNSET** (renders unset; owner decision required).

### Scope

| # | Value | Setting | Status | Source / decision required |
|---|---|---|---|---|
| 1 | Active projects — Free | **1** | ✅ | §4c Free ("Max active projects — 1") · UP-3 |
| 2 | Active projects — Basic | **3** | ✅ | §4c Tier 2 (owner-confirmed 2026-06-05: *"the primary upgrade trigger"*) · UP-3. **Corrects the AI-invented "10"** (DL-102 Correction #3) |
| 3 | Active projects — Pro | **10** | ✅ | §4c Tier 3 (DL-074 starting value) |
| 4 | **Collaborator seats — Free** | **3** *(incl. the owner)* | ⚠️ **RECOMMENDATION** | **§4c has NO seat row for Free/Basic/Pro.** D129 X-1 / DL-102 B/E is a product-grill recommendation, never owner-ratified. **Owner decision required.** |
| 5 | **Collaborator seats — Basic** | **10** | ⚠️ **RECOMMENDATION — and commercially wrong** | See finding **S5** below. Team is priced **~$99–149 per seat**; a $12/mo Basic granting **ten** seats means a ten-person team buys **one Basic** instead of Team. **Owner decision required. The build does not invent a replacement number.** |
| 6 | Collaborator seats — Team / Enterprise | **per seat** *(the pricing unit)* | ✅ | §4c T4/T5 · DL-074 §1 — "per-seat at Team/Enterprise" |
| 7 | Viewers — every tier | **∞ unlimited** | ✅ | D129 X-1 — read-only access holds no seat |

### Cost meters (daily — burst-smoothers, *not* the gate)

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 8 | Suggested fixes / day — Free | **5** | ✅ | §4c Free · MON-02 / UP-1 |
| 9 | Suggested fixes / day — Basic | **20** | ✅ | §4c Tier 2 ("removes daily-limit friction") |
| 10 | Chat messages / day — Free | **20** | ✅ | §4c Free ("bound interactive burn") · MON-03 / UP-2 |
| 11 | **Chat messages / day — Basic** | **75** | ✅ **CORRECTED** | **§4c Tier 2** (owner-confirmed 2026-06-05). *Was rendered UNSET on the strength of UP-2's "Basic raises your daily chat limit". The value was ratified all along.* |
| 12 | Extended (deep) runs / day — Free | **2** | ✅ | §4c Free ("gate the expensive path") · UP-5 |
| 13 | **Extended (deep) runs / day — Basic** | **6** | ✅ **CORRECTED** | **§4c Tier 2** — and §4c is explicit: *"burst ceiling (**not the governor**)"*. *Was rendered UNSET.* |
| 14 | Extended (deep) runs / day — Pro | **15** | ✅ | §4c Tier 3 |
| 15 | **Deep-Pass coalescing window (OD-10)** | **— UNSET —** | ⬜ | §4c ratifies coalescing is **ON** ("Deep concurrency 1 + coalescing on — structural"); the **window** is `TBD – Owner Decision Required` (OPEN_DECISIONS OD-10). **See finding S-OD10.** |

### The binding governor (§4c) — *the limit that actually gates*

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 16 | **Monthly token governor — Free** | **4,000,000 tokens** | ✅ **CORRECTED** | **§4c** — *"Monthly token budget / user (hard rollup): 4,000,000 — **the binding governor**."* Monthly $ ceiling ~$3.00 (DL-048 Balanced posture). |
| 17 | **Monthly token governor — Basic** | **10,000,000 tokens** | ✅ **CORRECTED** | **§4c** — *"the binding governor (~12 Deep or ~80 Fast/mo across 3 projects)"*. Worst case ~$7.90 against a $12 price. |
| 18 | Monthly token governor — Pro | **25,000,000** | ✅ | §4c Tier 3 |
| 19 | Monthly token governor — Team | **50,000,000 / seat** | ✅ | §4c Tier 4. Enterprise: negotiated. |
| 20 | What the governor counts | **normalized compute unit = tokens × model-tier weight** | ✅ | **DL-074 §2** — one governor, absorbing *any* compute source (Fast · Deep · monitoring · agents) |
| 21 | Daily token budget (burst smoothing) | Free **500k** · Basic **1.5M** | ✅ | §4c — explicitly *not* the gate |
| 22 | Per-run token caps → degrade | Fast **150k** / Deep **600k** (Free) · **300k / 1M** (Basic) | ✅ | §4c — over the cap → partial orientation / coalesce-defer |
| 23 | **Monthly budget gate — the UP-6 trigger point** | **= the monthly token governor** | ✅ **CORRECTED** | UP-6 ratifies the trigger and its copy; **§4c supplies the threshold**. *The first build rendered this UNSET and **enforced nothing**. The gate is real, and it is the governor.* |

### Project-size envelope

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 24 | **Project size envelope — Free** | **~20 documents / ~50k words** | ✅ **CORRECTED** | **§4b CHG-056** — *"✓ Tier-1 **owner-confirmed** (2026-06-05): the Free/Tier-1 envelope is ~20 artifacts / ~50k words / 1 active."* Outside it, projects are **not rejected** — they **degrade gracefully** (partial orientation + coalesced Deep). |
| 25 | **Project size envelope — Basic** | **~40 documents / ~100k words** | ✅ **CORRECTED** | **§4c Tier 2** — *"Fast Pass per-run token cap 300,000 — 2× envelope (**40 docs / ~100k words**)"*. *The build called UP-4's "~100k words" **illustrative, not ratified**. It **is** ratified — it is Basic's envelope.* |
| 26 | Project size envelope — Pro / Team | Pro **~80 / ~200k** · Team **~150 / ~400k** | ✅ | §4c Tiers 3–4. Enterprise: custom. |

### Model routing — *the ratified value story*

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 27 | Model routing — Free | nano extraction · mini synthesis · Haiku fallback | ✅ | §4c — *"the primary cost lever"* |
| 28 | Model routing — Basic | **nano / mini — the SAME class as Free** | ✅ | §4c Tier 2 — *"differentiates on **capacity, not model quality** (routing stays cheap-class — full-quality model is the Tier-3 Pro upsell)"* |
| 29 | Model routing — Pro | mini + **full-quality (GPT-4.1) fallback** | ✅ | §4c Tier 3 — *"the quality upsell"*. Plus **execution monitoring** (Pro+ forward capability; DL-083 / backlog). |
| 30 | Model routing — Team / Enterprise | **premium** full-quality synthesis · + dedicated | ✅ | §4c T4/T5 · DL-074 — *"routing quality, not token volume, is the dominant cost driver at the top."* |

### Price — the whole ladder

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 31 | Free price | **$0** | ✅ | §4c — CAC/subsidy; ~$3.00/active-free-user/month cost ceiling (DL-048 Balanced, owner-selected) |
| 32 | **Basic price** | **$12 / mo** | ✅ **CORRECTED** | **§4c** — *"Tier 2 — Basic (**owner-confirmed 2026-06-05**; first paid step, **$12/mo**)"*. Reaffirmed by **DL-074 §4**. *D129 T-3 ("the price is the owner's to set") is **superseded by the owner having set it**.* |
| 33 | Pro price | **~$39 / mo** | ✅ | DL-074 §4 (Ratified 2026-06-19) — starting value, re-tunable from `AI Spend Recorded`. **Not purchasable in R1.** |
| 34 | Team price | **~$99–149 / SEAT / mo** | ✅ | DL-074 §4 · §4c T4 — **per seat**. *This is why Basic's seat count matters commercially.* **Not purchasable in R1.** |
| 35 | Enterprise price | **custom / contract** | ✅ | §4c Tier 5. **Not purchasable in R1.** |
| 36 | R1 purchasability | Free ✓ · **Basic ✓** · Pro/Team/Enterprise ✗ | ✅ | D123 (tier gating live in Alpha) + DL-074. The forward ladder is **shown and priced, with no Buy button** — a "coming soon" with a Buy attached is a pre-order. |
| 37 | **Billing / payment rail** | **— UNSET —** | ⬜ | T-4 — engineering. **The price is not the open question. The rail is.** It must carry DL-074 §5's guardrails (visible meter · user-set spend cap · threshold alerts). |

### Overage (DL-074, Ratified)

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 38 | Overage unit | **per Extended Analysis (Deep Pass)** | ✅ | DL-074 §2 — presented under a **"usage-based"** umbrella, *not* "Deep-Pass pricing". **Abstract token credits were weighed and rejected.** |
| 39 | **Who may buy overage** | **PAID TIERS ONLY — Basic · Pro · Team** | ✅ | **DL-074 §3** — *"Free converts via **upgrade**… **no Free purchase path**."* ⚠️ **DO NOT BUILD A FREE TOP-UP.** |
| 40 | Overage guardrails | **visible meter · a spend cap YOU set · threshold alerts** | ✅ | DL-074 §5 — *"no silent overspend, no bill shock"*. Per-run caps still degrade; per-user rollups still gate. Overage is an **explicit, priced** relaxation — never silent, never automatic. |

### Export

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 41 | Export formats — Free | **PDF only** | ✅ | MON-01 / SHARE-04 / D112 — a Free-tier viral primitive, never taken away (CHG-061) |
| 42 | Export formats — Basic | **PDF · Copy summary · Export link** | ✅ | D112 |

### Prompts (MON-04)

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 43 | **Global upgrade-prompt cap / day** | **— UNSET —** | ⬜ | MON-04's global guards **require** a per-day cap. §4d's *"≤ 2/day, ≤ 1/session"* is **proposed calibration config**, never owner-ratified. The build enforces the **guard** with a conservative prototype-local value, labelled as such, and renders the **product** value unset. |
| 44 | Per-trigger cooldowns | once/day · once/month · once ever · none (UP-3) | ✅ | MON-04 trigger table |

### CRR / evidence

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 45 | Review requests & reviewer grants | **∞ free and unmetered** | ✅ | **CR-2 / D120 / D126** — every tier, every phase. Structurally load-bearing. |
| 46 | **Free CRR cap** | **— UNSET —** | ⬜ | D118 / B-1 — the bounded-cap **mechanism** is canon (CRR-01, cost-governed under DL-048); **the number is not.** Doctrine constrains it hard: virality **seeds on Free** (CHG-061) and evidence-seeking is **never bounded** (CR-2) — so it may gate **depth/volume**, never the **existence** of the loop. **It must never fire an upgrade prompt.** |
| 47 | **Evidence that arrives after the governor has gated** | **record · defer · disclose** | ⚠️ **RECOMMENDATION** | **Canon has never decided this.** See finding **S2′** below. |

### Never metered (D128) — *in the census precisely so nobody ever adds a tier check here*

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 48 | Plan artifacts | **∞ uncapped, every tier** | ✅ | D128 P1 — the epistemic record is never metered |
| 49 | History retention | **∞ never expires, never truncates** | ✅ | D128 P1 / D096 |
| 50 | Link revocation + purpose-scoped expiry | **free, every tier** | ✅ | D128 P2 / CR-6 — safety is never sold |

### Phase limits (NOT tier — kept separate, never merged: D124)

| # | Value | Setting | Status | Source |
|---|---|---|---|---|
| 51 | Invite allocation — Free / Basic | **2 / 5 per calendar month** | ✅ | CR-1 / T-2 (D125), X-3. **Retires at GA. Never presented as a tier upsell.** |
| 52 | Pending-invite expiry | **14 days**, refunded | ✅ | X-2a / D132 |
| 53 | Share-link / review-grant lifetime | **30 days** · *until the issue resolves, or 14 days* | ✅ | CR-6 (D125) |

---

## Findings the owner should see

### S5 — Collaborator seats are the ONE undefined dimension in the entire ladder *(the sharpest item)*

§4c sets **every other row for every tier**. It sets **no seat row for Free, Basic or Pro**. Seats appear in canon only at **Team/Enterprise** — where the price **is** per seat.

The existing proposal (Free 3 / Basic 10, D129 X-1 / DL-102 E) is a **product-grill recommendation, and Basic = 10 is commercially wrong:**

> **Team is priced ~$99–149 *per seat*. If Basic ($12/mo) grants 10 collaborator seats, a ten-person team buys ONE Basic subscription instead of Team. That guts Tier 4.**

**And the fix costs nothing.** CHG-061 requires the viral primitives on Free — but those run on **unlimited Viewers** and **free, unmetered Reviewers (CR-2)**, *neither of which consumes a seat*. So **seats can be tight across Free/Basic/Pro without breaching CHG-061.** Individual tiers grant enough collaboration to do **your own** work; **Team is where collaboration becomes the product.**

**Basic's seat count must fall well below the point where a team would rationally buy Basic over Team.** The number is the owner's; the constraint is structural. **This build does not invent a replacement** — it carries the existing recommendation, renders it in-product as *"recommendation — not ratified"*, and escalates.

### S2′ — CR-2 vs the binding governor *(the real conflict)*

Three ratified things collide, and canon has never reconciled them:

- **CR-2 / D126** — evidence-seeking is **never metered**; a reviewer's answer must **never be refused**.
- **CRR-04** — every reviewer response **triggers an Extended Analysis**.
- **§4c** — the monthly rollup **"gates further AI spend — never silent overspend."**

**What happens when a reviewer's evidence arrives after the governor has gated?** *Undecided.*

**Recommendation (implemented, labelled in-product, NOT ratified): record the evidence · defer the run · disclose honestly.** The attestation is appended immediately and unconditionally (**CR-2 holds — evidence is never refused**); the *run* defers, with an honest line:

> *"Priya's answer is recorded. Your read will update when your monthly analysis budget resets, or on upgrade."*

Cost bounded · evidence never lost · the product honest about what it has not yet done. **It is the only resolution in which all three constraints survive.** **Owner decision required.**

### S-OD10 — the coalescing window is the highest-leverage unset number

Coalescing is **on** and ratified (§4c). The **window** is `TBD` (OD-10). It determines whether five fixes cost **five** Extended Analyses or **one** — **a bigger cost lever than any cap, and it costs the user nothing.**

**Recommendation (escalated, not built as canon):** settle/idle-based, single-active, plus the canonical **manual** trigger (which the Deep Pass spec already lists). **UX rationale, not just cost:** a read that recomputes on every keystroke reads as a **live score, not a considered judgment**. Confidence is *understanding maturity*; it should move when understanding changes, not when a character does. Show the **causal delta** after each settled run — *"You changed 3 things → Clarity ↑, Feasibility unchanged"* — which is a **stronger** payoff than a twitching number, because it is attributable.

### S3 — 5 fixes/day may still cap activation

The activation moment is **fix → the read moves**. A freshly analyzed plan routinely surfaces more than 5 issues, so a natural first session can hit the cap mid-activation. Canon's counter is explicit — MON-02 gives the allowance's value as *"Habit + re-engagement"* — so the cap **deliberately** trades activation for return-rate. **Recommendation:** instrument *fixes-applied-before-first-cap-hit* in Alpha. If most first sessions hit it, a **first-project grace** fixes it without touching the steady-state number. (Coalescing means 5 fixes ≠ 5 runs, so the grace is cheap.)

### S4 — the chat cap brushes D126 in principle

*"Never meter who gets an answer."* Chat is how a user gets an answer **from OSLO** about their own read. Defensible as a **cost** control (Free 20/day and Basic 75/day both sit above genuine use) — **but the copy must never imply you must pay to understand what OSLO already told you.**

### S7 — the project cap is concurrency, not volume

Archiving is reversible and frees the slot (DL-058; UP-3's own resolution), so Free users can work unlimited plans **sequentially**. The cap bites only when two plans must be open at once. Honest — but it converts fewer people than "1 vs 3" implies.

### Superseded findings *(kept, per house rule — do not delete history)*

The first census carried three "structural findings". Two are now **withdrawn**:

- ~~**"Two ratified sources disagree about Basic's project cap (UP-3 says 3; D129 T-1 says 10)"**~~ — the conflict is real but it is not between two ratified sources. **§4c and UP-3 both say 3.** D129 T-1's "10" was the product-grill's own AI-proposed number. **Not a canon conflict; a build error, already withdrawn** (DL-102 Correction #3).
- ~~**"UP-5 presumes an affordance D006 forbids"**~~ — **partially dissolves.** The Deep Pass spec lists a **manual trigger**; with OD-10 settled as settle/idle + manual, UP-5 has a real affordance to gate and D006 is not violated. *Still worth confirming which triggers the deep-run cap attaches to.*
- **Still standing:** the seat cap (`UP-SEAT`) and export formats (`UP-EXPORT`) have **no slot in the ratified UP-1…UP-8 taxonomy**, though D138 governs *every* cap. Their taxonomy slot is an owner decision; the build did not assign them canon numbers.

---

## The 8 open decisions, for `RELEASE_1_TIER_DEFINITIONS_V1`

Ordered by how much they block.

| # | Decision | Class | Why it blocks |
|---|---|---|---|
| 1 | **Collaborator seats — Free / Basic / Pro** | ⚠️ RECOMMENDATION carried | The only undefined ladder dimension. Basic = 10 **cannibalises Team's per-seat sale**. Must be set before Basic is marketed. |
| 2 | **CR-2 vs the binding governor** | ⚠️ RECOMMENDATION carried | Three ratified rules collide. The build implements *record-defer-disclose* and labels it. Owner must ratify or replace. |
| 3 | **OD-10 — coalescing window** | ⬜ UNSET | The highest-leverage cost lever in the product, and it costs the user nothing. |
| 4 | **Free CRR cap (B-1 cost ceiling)** | ⬜ UNSET | Mechanism canon; number never set. May gate depth/volume, **never** the existence of the loop. **Must never fire an upgrade prompt.** |
| 5 | **MON-04 global upgrade-prompt cap / day** | ⬜ UNSET | The guard is canon; §4d's number is *proposed* config, not ratified. |
| 6 | **Billing rail** | ⬜ UNSET | Engineering (T-4). Must carry DL-074 §5: visible meter · user-set spend cap · threshold alerts. |
| 7 | **Readout scheduling — R1 or fast-follow?** *(NEW — D147)* | ⬜ UNSET | **Built and flagged** (`SCHEDULING_R1 = null`). Automating the weekly readout is the **labour half of the strongest lever in the product** — but whether it lands in R1 is the owner's call, not the build's. |
| 8 | **Readout branding — Basic or higher?** *(NEW — D147)* | ⚠️ REC (Basic) | D147 places branding at Basic. **Not settled.** It is the one Basic feature that is pure vanity rather than depth, so it is also the easiest to move up the ladder. |

**Everything else in this census is RATIFIED and should be cited, not re-decided.**

---

*Source of truth: `TIER_DEFS` in `prototype.html` — the same registry the product renders from. The in-product **Usage & limits** screen shows the user this same table, ratified rows, recommendation rows and unset rows alike.*

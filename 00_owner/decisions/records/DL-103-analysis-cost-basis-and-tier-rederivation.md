# DL-103 — Analysis cost basis & tier re-derivation — never tier judgment quality; commission incremental recompute + prompt caching (supersedes 'Pro adds model quality'; suspends the §4c numeric basis)

- **Date:** 2026-07-12 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

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

**7. The Free → Basic conversion model (added 2026-07-11, before ratification).**

This clause exists because §6 retires UP-1/UP-2 and would otherwise leave a hole where the monetization engine should be. **It states what converts, and why each lever is safe.**

#### 7a. The principle — corrected

An earlier draft of this decision said *"friction belongs on the boundary of scope — never on thinking itself."* **Too broad.** It left no lever that fires during the weeks a plan is actually being built, which is where the user spends most of their life in the product.

> **Meter the inputs and the outputs. Never the understanding in between.**

**This is what canon already said.** The `12_freemium_tier_behavior_logic` **"Constrain:"** list reads: *number of Outcome Spaces · number of daily fixes · number of simulations · continuous monitoring · integrations · team collaboration depth · governance policies · export/sync capabilities.* **Every item is an input or an output — except the daily-fix cap, the one outlier, which §6 retires.**

**Permitted:** tier **how much OSLO looks at** (sources, size — *always honestly disclosed*, as UP-4 does) and **what OSLO does with the read** (report, export, sync, simulate, package).
**Forbidden:** tier **how well OSLO thinks** about what it saw (judgment quality — §1), or **the user's access to understanding already produced** (chat, issues, History, artifacts — D126/D128).

#### 7b. Friction is not one thing — disaggregate it

| Type | Trust cost | Verdict |
|---|---|---|
| **Latency** (same result, later) | none | **Permitted — the strongest lever (7c)** |
| **Automation** (manual vs connected) | none | Permitted |
| **Packaging** (the artifact, not the understanding) | none | Permitted |
| **Bulk/convenience** (one-at-a-time vs apply-all) | none | Permitted |
| **Concurrency** (one live understanding) | none | Permitted |
| **Volume** (stop after N) | **depends entirely on where N sits** | Permitted **only** per 7d |
| **Quality** (a worse read) | **fatal** — makes Reliability a function of billing | **PROHIBITED (§1)** |
| **Access** (can't see your own issues/History/chat) | **fatal** | **PROHIBITED** |
| **Attention** (nags, interstitials, wallpaper) | corrosive | **PROHIBITED** (MON-04 already bans wallpaper) |
| **Hostage** ("your read expires unless you pay") | **fatal** | **PROHIBITED** |

**Operational test (binding):** **Would you be comfortable saying this friction out loud, to the user, in the product?**
*"Basic runs your analysis immediately"* — fine. *"Basic gives you a more accurate read"* — you would never say it. **That is the tell.**

#### 7c. The primary lever: **labour, not latency** *(corrects an earlier draft)*

> **WITHDRAWN — an earlier draft of this clause made *latency* the primary lever** ("Free queues; Basic runs now"). **It is struck.** The argument that kills it is this decision's own:
> **Latency only bites when the user is blocked — and OSLO is deliberately designed so that they never are.** Settle-based coalescing (OD-10) makes the read lag the edits *by design*; *"Analysis is behind your edits"* is a normal, honest state. A PM heads-down on edits does not care whether the re-read lands in 30 seconds or 10 minutes. **An async product cannot sell speed.**
> There is exactly **one** moment latency would truly bite — *"I have a stakeholder meeting in ten minutes and I need the current read"* — and that is precisely the moment **§7b prohibits monetizing** ("never interrupt at peak need").
> **Latency friction is therefore either worthless (they are not waiting) or predatory (they are, at the worst possible moment). There is no useful middle.**

**The correct frame: OSLO's users are not time-blocked; they are EFFORT-blocked.** They do not need the answer *faster* — they need **less work** to get it and to use it. **Meter labour, not latency.**

**Ranked levers (by real value to a PM):**
1. **REPORTING (§7j)** — **the strongest lever in the product.** Not because it saves labour, but because it confers **status**: it makes the PM look strategic in front of their leadership. People pay far more to look good than to save time.
2. **Connected sources / auto-sync** — kills the largest recurring tedium (re-uploading; the plan drifting from the source of truth). Fires **day 1 and forever**.
3. **Export/sync → execution tool** (DL-083, at Basic) — the plan becomes actual work.
4. **Reverse trial (7e)** — the mechanism that makes all of the above *felt*, during the plan-building weeks.
5. **Assisted-apply volume (7d)** and **bulk actions** — labour reduction, every session.
6. **One live understanding · projects · envelope** — scope.

**The Fast Pass / 60-second Time-to-First-MRI (DL-046) NEVER queues — but as a PRODUCT GUARANTEE, not a monetization lever.** A new user gets their first read instantly because that is the promise, not because we are being generous. **Artificial delay remains PROHIBITED** in all cases (fabricated latency is fabricated scarcity).

#### 7d. Volume caps: legitimate — and the **placement is the whole decision**

**The daily suggested-fix cap is retained** (owner, 2026-07-11), against an earlier draft that retired it outright.

**Why it is legitimate.** *"Apply this fix"* is **OSLO doing the editing for you** — a **labour-saving** action, not comprehension. Capping it meters **leverage**, never **understanding**. It is the same family as bulk actions (7c #5), and it fits *meter the inputs and the outputs* exactly.

**BINDING LINE — this is what keeps it legitimate:**
> **The recommendation is ALWAYS visible. Only the assisted apply is metered. Manual editing is ALWAYS free.**
> At the cap the user still sees the issue and the full recommendation — **what to change and why** — can still make the edit by hand, and the analysis still runs. What Basic buys is **OSLO applying it for you, at volume**.
> **If the cap ever hides the recommendation itself, it stops metering labour and starts metering understanding — and becomes PROHIBITED (D126/D128).**

**Ladder:** **Free** — see every recommendation, apply *N* per day. **Basic** — apply freely, plus **apply-all** in one action.

**PLACEMENT IS THE DECISION:**
> **Set the cap ABOVE the activation threshold and BELOW the power-use threshold.**

§6 retired the cap at **5/day** because at that level it fires **during activation**, on a first-timer working their initial issue list. That is an argument about **placement, not mechanism**. Set above activation, it fires **only on users for whom the product is demonstrably working** — who are also the likeliest to pay — and **never on users still deciding whether it works**.

**Set the number from Alpha instrumentation** (the observed fixes-per-session distribution), **NEVER from a cost model** — under coalescing the fix itself is near-free, so **this is a monetization lever and the record says so plainly** rather than dressing it as a cost control. **Until that data exists: no cap.**

#### 7d-bis. Refresh cadence: **auto vs manual** — and the window adapts to the USER, not the tier

**The coalescing window (OD-10) is an activation instrument, not a paywall.**
- **Tight window while the user is new** — they *see* the read move as they fix things. That is the aha (*fix → the read moves*), and activated users convert at **35–65%** vs **2–8%** un-activated.
- **Settle-based once established** — calm, no twitching, no churn. (Owner feedback during the Slice-5 grill: *"the reanalysis is too responsive."*)
**The window keys off where the user is in their journey — NEVER off their tier.**

**The tier lever is auto-refresh vs manual refresh:**
- **Free:** **"Update now" — always available, always free, on every tier** (the Deep Pass spec already lists **`manual`** as a qualifying trigger) — plus slow auto-refresh.
- **Basic:** continuous auto-refresh.

**BINDING CONDITION:** *"Update now" is free on every tier.* **This is load-bearing.** With it, the lever is **automation** (permitted — the user is never stuck with a stale read; what Basic buys is **not having to ask**). Without it, it gates the **currency of understanding** and is **PROHIBITED**. Refresh runs still draw on the monthly analysis governor, which is the legitimate cost control.

#### 7e. **Reverse trial** — the answer to the multi-week plan problem

**A plan takes weeks. Scope drivers (more plans, bigger plans) only fire *after* it is finished.** That leaves the whole plan-building period without a conversion moment.

**Every new user starts on Basic (or Pro) for a bounded trial (~14 days), then downgrades to Free.** Market evidence: a reverse trial lifts freemium→premium conversion by roughly **10–40%**, and freemium+premium-trial hybrids are now used by ~65% of PLG SaaS. The user experiences **connected sources, reporting, priority analysis, multiple plans** during the exact weeks they are building the plan — then feels their absence.

**BINDING CONDITION — what the downgrade may take back:**
> **Take back the pipes. Never the read.**
> On downgrade the user loses **leverage** — integrations, reports, priority queue, extra live plans. The user **never** loses **understanding**: History, issues, artifacts, chat and their read remain **fully intact and accessible** (D128). Removing understanding on downgrade would be a betrayal of the product's core promise and is **PROHIBITED**.

*Phase note:* a reverse trial is a **GA-phase** mechanic. In Alpha every user is invited and hand-curated (DL-102), so it does not apply yet.

#### 7f. In-plan conversion moments (they fire early and repeat)

| When | Moment | Lever |
|---|---|---|
| **Day 1, then continuously** | "Connect Jira/Confluence so OSLO stays current with your plan" | **Integrations** *(canon Constrain list; "≥2 governed planning sources" is an Alpha exit criterion)* |
| **Every session, once activated** | "You've used today's assisted fixes — Basic applies them freely, and all at once" *(the recommendation stays visible; manual editing stays free)* | **Assisted-apply cap + bulk actions (7d)** |
| **Weekly** | The stakeholder readout / exec update | **Reporting & Analytics (M4, scoped R1)** |
| **Ongoing** | "Push these fixes into Jira" | **Export/sync — plan → execution tool (DL-083, at Basic)** |
| **Every session** | "Apply all recommended fixes" | **Bulk actions** |
| **Every plan switch** | Archived plans go **read-only — the read freezes** | **One live understanding** *(makes §4c's "primary upgrade trigger" actually bite; DL-058 archive stays reversible)* |
| **On large plans** | Partial read, **honestly disclosed** | **Envelope (UP-4)** — *Free's envelope must be large enough to fully read a **real** plan, or it is a demo, not a tier* |
| **Mid-plan** | "What if the vendor slips?" | **Simulations** *(canon Constrain list; likely post-R1 — do not count on it for Alpha)* |
| **Plan 2** | "You got value here — do it again" | **Projects** — a **pull**, not a wall |

#### 7g. Upgrade mechanics

- **One click. Self-serve. Transparent price. No sales call.** Market evidence is blunt: *"any friction — complex forms, sales calls required, unclear pricing — kills conversion."* Consistent with Basic+Pro = the **individual** motion (§5).
- **Trigger on behaviour and realized value, never on a calendar.** Canon's **value-moment** class (UP-7/UP-8) is to be **strengthened**, not left as an afterthought.

#### 7h. **Outcome-based pricing is PROHIBITED for OSLO**

It is the loudest trend in AI monetization (investor preference ~26%) and it is **wrong for this product.** OSLO's doctrine is that **Confidence is understanding maturity — explicitly NOT project health, readiness, or probability of success.** Outcome pricing would require charging against delivery results the product **deliberately refuses to predict**. Recorded here so it is not re-litigated.

#### 7i. The trade, stated honestly

**Frustration converts faster than desire.** Freemium converts at ~2–5% (great: 8–12%); trials at 8–25%. This decision **deliberately chooses a slower-converting model** — but far less slow than a pure no-friction stance, because 7c (labour levers — connected sources, reporting, export/sync), 7d (correctly-placed assisted-apply caps) and 7e (reverse trial) recover most of the conversion pressure **at zero cost to trust.**

**And the market evidence says the trade is smaller than it looks:**
- *"Gating usage **intensity** was a more powerful monetization lever than gating model **intelligence**."* — the doctrinal choice in §1 is **also the better-converting one**.
- **Activated users convert at 35–65%; un-activated at 2–8%** — a gap an order of magnitude wider than freemium-vs-trial. **Activation is the dominant variable in the funnel**, which is why a cap that fires during activation (§6) is not a UX quibble but a revenue decision.
- *"Credits mapping to customer-legible value outperform credits that abstract away meaning"* — corroborates **analyses, not tokens** (DL-074).

**Sources (market evidence, July 2026):** Lenny's Newsletter (*why SaaS freemium playbooks don't work in AI*) · Appcues (*free-to-paid conversion benchmarks*) · Metronome (*2026 trends from cataloging 50+ AI pricing models*) · Digital Applied (*freemium vs free trial, 2026*) · Growth Unhinged (*2026 State of B2B SaaS & AI Monetization*).

#### 7j. **Reporting — the strongest lever, and it is unspecified**

**M4 "Reporting & Analytics" is a named R1 milestone with ZERO capability rows and NO specification.** SHARE-01…05 are *sharing*, not reporting; `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1` explicitly disclaims the role (*"not a reporting engine… it packages existing understanding; it never produces new understanding"*). **The strongest conversion lever in the product currently exists only as a name.**

**Why reporting is a status lever, not a labour lever (owner, 2026-07-11).**
A status report — *"60% done, three tasks late"* — makes a PM look like a **clerk**; every PM produces it and it confers no standing. **PMs will readily distribute a NEW KIND of report if it makes them appear strategic, smart, and high-value to their stakeholders.** What makes someone look **senior** is naming what nobody else has named:
- *"The sponsor and engineering hold different definitions of done — here is where they diverge."* (**Alignment**)
- *"This plan rests on three assumptions nobody has validated."* (**clarification / assumption register**)
- *"Here are the two decisions I need from you, and what each unblocks."* (**decision brief** — turns the PM from reporter into agenda-setter)
- *"Our understanding matured from Orientation to Validated this month — here is what changed and why."* (**maturity narrative**; History already holds it)
- *"The single change that would most improve this plan."* (**leverage read**)

**This is exactly OSLO's existing output** — CAF, the clarification register, unresolved assumptions, understanding-maturity-over-time, evidence provenance. **Therefore: OSLO's epistemic honesty IS what makes the PM look strategic. There is no trade-off between the doctrine and the commercial value — they are the same artifact.** *"Here is what we know, here is what we are assuming, here is what we have not validated"* is how senior people talk.

**A triple lever:** **labour** (a weekly obligation) + **status** (far higher willingness to pay) + **the best viral surface in the product** — a PM sends this to **eight executives**. That is the passive loop (SHARE-02) aimed **upward**, landing OSLO's fingerprint in front of budget holders rather than peers.

**THE BINDING RISK — the PM stakes their own credibility on OSLO's output, in front of their leadership.** A hallucinated claim in a status update is embarrassing; **a hallucinated claim in a board-level strategic read can end a career.** Reports must therefore be **rigorously reliability-qualified — not despite the status goal, but BECAUSE of it.** Overclaiming would detonate in the PM's face in front of the exact people whose opinion they are trying to shift. **Epistemic discipline in reporting is not doctrine — it is protection of the user's reputation, which is what they are actually buying.**

**Doctrine held:** a report **packages existing understanding** for a different audience; it **produces no new assessment**. Confidence remains **understanding maturity — never project health, readiness, or probability of success**. Every package carries the disclaimer.

**Tiering:** **CHG-061 guarantees PDF export on Free**, so **Free keeps a shareable artifact** (the read snapshot — which already carries OSLO's fingerprint and already reaches executives). **Basic gets the strategic suite** (alignment read · assumption register · decision brief · maturity narrative) plus branding and scheduling. **The seed is not gated; the depth is.**

**BLOCKING WORK ITEM: commission a Reporting specification** (M4). It is the strongest conversion lever, the best viral surface, and the **highest-reputational-risk output** in the product — and it is unspecified. Report **names** are owner/glossary decisions and are **not** set here (Anti-Assumption).

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
- **Adds §7 — the Free → Basic conversion model** (added before ratification): the corrected principle (*meter the inputs and the outputs; never the understanding in between* — which canon's own "Constrain:" list already implied), a disaggregated friction taxonomy with a binding say-it-out-loud test, **labour (not latency) as the primary lever** — an earlier draft made latency primary and it is **struck**: an async product cannot sell speed, and the one moment latency would bite is the one §7b forbids monetizing; the levers are **connected sources · reporting · export/sync · bulk actions** — **the daily assisted-apply cap RETAINED** with **placement as the whole decision** (above activation, below power use, from instrumentation; recommendation always visible, manual editing always free), the **reverse trial** (*take back the pipes, never the read*), in-plan conversion moments, one-click self-serve upgrade, and **outcome-based pricing PROHIBITED** (it would require charging against delivery results OSLO deliberately refuses to predict).
- **Reaffirms** DL-069 · DL-102 (CR-2, D124, D126, D128) · CHG-061 · DL-074's hybrid structure and guardrails.

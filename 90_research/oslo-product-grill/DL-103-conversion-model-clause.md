## 7. The Free → Basic conversion model (added 2026-07-11, before ratification)

This clause exists because §6 retires UP-1/UP-2 and would otherwise leave a hole where the monetization engine should be. **It states what converts, and why each lever is safe.**

### 7a. The principle — corrected

An earlier draft of this decision said *"friction belongs on the boundary of scope — never on thinking itself."* **Too broad.** It left no lever that fires during the weeks a plan is actually being built, which is where the user spends most of their life in the product.

> **Meter the inputs and the outputs. Never the understanding in between.**

**This is what canon already said.** The `12_freemium_tier_behavior_logic` **"Constrain:"** list reads: *number of Outcome Spaces · number of daily fixes · number of simulations · continuous monitoring · integrations · team collaboration depth · governance policies · export/sync capabilities.* **Every item is an input or an output — except the daily-fix cap, the one outlier, which §6 retires.**

**Permitted:** tier **how much OSLO looks at** (sources, size — *always honestly disclosed*, as UP-4 does) and **what OSLO does with the read** (report, export, sync, simulate, package).
**Forbidden:** tier **how well OSLO thinks** about what it saw (judgment quality — §1), or **the user's access to understanding already produced** (chat, issues, History, artifacts — D126/D128).

### 7b. Friction is not one thing — disaggregate it

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

### 7c. The primary lever: **latency, not count** — activation instant, iteration queued

Once analyses are cheap but **throughput-bound** (local inference, DL-069), the scarce good stops being *count* and becomes **time**.

- **Free:** Extended Analysis runs in a **shared queue**.
- **Basic:** it runs **now**.
- **Same model, same evidence, same answer — sooner.**

Honest (nothing hidden), non-degrading (the read is identical), **genuinely scarce** (GPU capacity is real, not manufactured), and it fires on **every iteration** — the recurring drumbeat the retired volume caps were supposed to supply.

**HARD CONSTRAINT: the Fast Pass / 60-second Time-to-First-MRI (DL-046) NEVER queues.** **Protect the activation moment; monetize the iteration loop.** A new user always gets their first read instantly.
**Artificial delay is PROHIBITED** — the queue must reflect real contention. Fabricated latency is fabricated scarcity.

### 7d. Volume caps: the placement *is* the decision

§6 retires the daily fix cap because at **5/day it fires during activation**. That is a statement about **placement**, not about volume caps as such.

> **Set volume caps ABOVE the activation threshold and BELOW the power-use threshold.**

A first-time user working their initial issue list **never sees it.** A heavy user — who is extracting the most value, and is therefore the likeliest to pay — **hits it regularly.** The cap fires precisely on the users for whom the product is working, and never on those still deciding whether it works.

**The number must be set from instrumentation** (the fixes-per-session distribution observed in Alpha), **never from a cost model.** Until that data exists, **no cap.**

### 7e. **Reverse trial** — the answer to the multi-week plan problem

**A plan takes weeks. Scope drivers (more plans, bigger plans) only fire *after* it is finished.** That leaves the whole plan-building period without a conversion moment.

**Every new user starts on Basic (or Pro) for a bounded trial (~14 days), then downgrades to Free.** Market evidence: a reverse trial lifts freemium→premium conversion by roughly **10–40%**, and freemium+premium-trial hybrids are now used by ~65% of PLG SaaS. The user experiences **connected sources, reporting, priority analysis, multiple plans** during the exact weeks they are building the plan — then feels their absence.

**BINDING CONDITION — what the downgrade may take back:**
> **Take back the pipes. Never the read.**
> On downgrade the user loses **leverage** — integrations, reports, priority queue, extra live plans. The user **never** loses **understanding**: History, issues, artifacts, chat and their read remain **fully intact and accessible** (D128). Removing understanding on downgrade would be a betrayal of the product's core promise and is **PROHIBITED**.

*Phase note:* a reverse trial is a **GA-phase** mechanic. In Alpha every user is invited and hand-curated (DL-102), so it does not apply yet.

### 7f. In-plan conversion moments (they fire early and repeat)

| When | Moment | Lever |
|---|---|---|
| **Day 1, then continuously** | "Connect Jira/Confluence so OSLO stays current with your plan" | **Integrations** *(canon Constrain list; "≥2 governed planning sources" is an Alpha exit criterion)* |
| **Every iteration** | "Your analysis is queued — Basic runs it now" | **Priority queue (7c)** |
| **Weekly** | The stakeholder readout / exec update | **Reporting & Analytics (M4, scoped R1)** |
| **Ongoing** | "Push these fixes into Jira" | **Export/sync — plan → execution tool (DL-083, at Basic)** |
| **Every session** | "Apply all recommended fixes" | **Bulk actions** |
| **Every plan switch** | Archived plans go **read-only — the read freezes** | **One live understanding** *(makes §4c's "primary upgrade trigger" actually bite; DL-058 archive stays reversible)* |
| **On large plans** | Partial read, **honestly disclosed** | **Envelope (UP-4)** — *Free's envelope must be large enough to fully read a **real** plan, or it is a demo, not a tier* |
| **Mid-plan** | "What if the vendor slips?" | **Simulations** *(canon Constrain list; likely post-R1 — do not count on it for Alpha)* |
| **Plan 2** | "You got value here — do it again" | **Projects** — a **pull**, not a wall |

### 7g. Upgrade mechanics

- **One click. Self-serve. Transparent price. No sales call.** Market evidence is blunt: *"any friction — complex forms, sales calls required, unclear pricing — kills conversion."* Consistent with Basic+Pro = the **individual** motion (§5).
- **Trigger on behaviour and realized value, never on a calendar.** Canon's **value-moment** class (UP-7/UP-8) is to be **strengthened**, not left as an afterthought.

### 7h. **Outcome-based pricing is PROHIBITED for OSLO**

It is the loudest trend in AI monetization (investor preference ~26%) and it is **wrong for this product.** OSLO's doctrine is that **Confidence is understanding maturity — explicitly NOT project health, readiness, or probability of success.** Outcome pricing would require charging against delivery results the product **deliberately refuses to predict**. Recorded here so it is not re-litigated.

### 7i. The trade, stated honestly

**Frustration converts faster than desire.** Freemium converts at ~2–5% (great: 8–12%); trials at 8–25%. This decision **deliberately chooses a slower-converting model** — but far less slow than a pure no-friction stance, because 7c (latency), 7d (correctly-placed caps) and 7e (reverse trial) recover most of the conversion pressure **at zero cost to trust.**

**And the market evidence says the trade is smaller than it looks:**
- *"Gating usage **intensity** was a more powerful monetization lever than gating model **intelligence**."* — the doctrinal choice in §1 is **also the better-converting one**.
- **Activated users convert at 35–65%; un-activated at 2–8%** — a gap an order of magnitude wider than freemium-vs-trial. **Activation is the dominant variable in the funnel**, which is why a cap that fires during activation (§6) is not a UX quibble but a revenue decision.
- *"Credits mapping to customer-legible value outperform credits that abstract away meaning"* — corroborates **analyses, not tokens** (DL-074).

**Sources (market evidence, July 2026):** Lenny's Newsletter (*why SaaS freemium playbooks don't work in AI*) · Appcues (*free-to-paid conversion benchmarks*) · Metronome (*2026 trends from cataloging 50+ AI pricing models*) · Digital Applied (*freemium vs free trial, 2026*) · Growth Unhinged (*2026 State of B2B SaaS & AI Monetization*).

# Alignment review — do the ratified tier numbers still match our latest thinking?
2026-07-11. Owner-directed. **Not a canon-compliance check** — a test of whether June's numbers still serve July's model.

**What changed since §4c (2026-06-05) and DL-074 (2026-06-19):**
DL-102 (CR-2 — evidence-seeking never metered) · D126 (never meter who gets an answer) · D128 (never meter the epistemic record; never sell safety) · tier live in Alpha · **Alpha optimizes for activation/learning** · Basic+Pro = individual motion, Team+Enterprise = org sale · coalescing settle-based (OD-10) · legible units, no fabricated scarcity.

---

## A1 — **The daily caps are theatre. The monthly governor is the product.** (Biggest.)

§4c prices a Deep run at ~500k tokens. Divide the governors:

| | Monthly governor | **Real analyses/month** | Daily cap implies | Daily cap is… |
|---|---|---|---|---|
| **Free** | 4M tokens | **~8** | 60/mo (2/day) | **8× looser — never binds** |
| **Basic** | 10M tokens | **~20** *(§4c itself estimates ~12 across 3 projects)* | 180/mo (6/day) | **9× looser — never binds** |
| **Pro** | 25M tokens | **~50** | 450/mo (15/day) | 9× looser |

**A Free user gets roughly eight analyses a month — not "2 a day."** The daily cap is unreachable; the monthly budget is what people will actually hit. §4c even says so ("6/day — *burst ceiling, **not the governor***"), but **the product surfaces the wrong one.**

**Consequence:** the friction prompts (UP-1/2/5) are aimed at limits that never bind, while the limit that *does* bind (UP-6, the monthly gate) is specified as *"soft, gentle, once/month."* **That's backwards.** And it breaches D124 in spirit — the user cannot tell which limit they're actually up against.

**Recommendation.** Make the **monthly analysis budget the headline limit, expressed in analyses, not tokens.** *"8 analyses left this month"* — never *"4,000,000 tokens."* Demote the daily caps to invisible rate-limits (burst-smoothers), not product limits. This also gives the **analysis pack** a natural unit (DL-074: adding units is an ADD, never a reframe).

---

## A2 — **The fix cap meters the wrong thing.**

Applying a suggested fix is a **text edit**. The suggestion was already generated during analysis. The cost is in the **analysis run** — and under **coalescing (ratified, §4c: "Deep concurrency 1 + coalescing on")**, five fixes in a session collapse into **one or two runs**.

So **Free's 5-fixes/day cap meters an action that costs almost nothing**, while the run cap and the governor already meter the thing that costs. MON-02 is honest about why it exists: its stated value is **"Habit + re-engagement"** — a *retention* mechanic, not a cost control.

**But *fix → the read moves* is the activation moment of this product**, and Alpha is now optimizing for activation. A cap that fires UP-1 mid-first-session taxes the single most valuable thing a new user can do, to save money the coalescer already saved.

**Recommendation: drop the daily fix cap, or raise it far above genuine use.** Let deep-runs + the monthly governor bound cost. If the habit mechanic is wanted later, reintroduce it at GA on evidence — not in the phase whose only job is to find out whether the read lands.

---

## A3 — **The chat cap meters comprehension for near-zero saving.**

A chat turn is a fraction of a Deep run. Free's 20/day saves almost nothing — and chat is **how a user understands their own read** (D109 made it the epistemic advisor: reliability-qualified, cited, honest about what it can't answer).

**D126 says: never meter who gets an answer.** Capping chat meters exactly that. The reconciliation ("chat costs tokens, D128 P1 permits metering cost") is technically true and **practically hollow** — you are taxing comprehension to save pennies.

**Recommendation: remove the daily chat cap; let the monthly governor bound it.** If a user burns their budget on chat, the governor catches it — honestly, in the currency they already understand.

---

## A4 — **Your collaborators can silently eat your analysis budget. This defeats CR-2 in practice.**

Chain: **CR-2** — evidence-seeking is never metered · **CRR-04** — every reviewer response triggers a Deep run · **§4c** — a Free user has **~8 runs/month**.

So five reviewers answering consumes **five of your eight monthly analyses.** CR-2 is honoured in *letter* (no request is refused) and defeated in *practice*: users will learn that **asking for evidence costs them their own read**, and will stop asking. That kills the exact loop DL-102 exists to protect — OSLO's core value action *is* its viral action.

**Recommendation — coalesce evidence; don't meter it.** Reviewer responses arriving in a window settle into **one** analysis run. This is:
- **cheap** — five responses, one run;
- **UX-correct** — you don't want your read churning as each reviewer replies; you want it to settle once they've answered;
- **doctrinally right** — CR-2 survives in practice, not just on paper.

It is simply **OD-10 applied to CRR**, and it turns the biggest cost exposure into the cheapest path. If coalescing is not enough, evidence runs should draw on a **separate budget** — the cost of the viral loop is CAC, not user capacity.

---

## A5 — **Seats: Basic = 10 cannibalizes Team.**

Team is priced **~$99–149 per seat**. Basic is **$12/mo**. If Basic grants **10 collaborator seats**, a ten-person team buys **one Basic** instead of Team. §4c has **no seat row at all** below Team — seats are the one undefined dimension in the ladder, and my Free 3 / Basic 10 (DL-102 E) is the only proposal on the table.

**Latest thinking says where they belong:** Basic+Pro = the **individual** motion; **Team is where collaboration becomes the product.** And CHG-061 is not at risk — the viral primitives run on **unlimited Viewers** and **free Reviewers**, *neither of which consumes a seat*.

**Recommendation: seats stay tight across Free/Basic/Pro and scale per-seat at Team.** Basic's seat count must sit well below the point where a team would rationally buy Basic over Team. Owner sets the number; the constraint is structural.

---

## A6 — **Basic at $12 may be under-fed and under-priced for the individual tier we now say it is.**

Real uplift: **~8 → ~12–20 analyses/month.** For $12, that's a thin "capacity" story — and §4c already shows the squeeze (worst-case ~$8 COGS on a $12 price = 34% worst-case margin). **Basic can't afford to be much more generous at $12.**

But our latest positioning says **Basic + Pro carry the individual motion**, and my earlier advice — which you accepted — was to **price against the alternative (a plan review), not against PM tools.** **$12 is anchored to PM tools.**

**The question this raises:** is Basic a *token first step* or a *genuinely useful individual tier*? Right now it's the former. Making it the latter means either a higher price or a bigger analysis budget — and the ladder is already compressed ($12 → $39 → $99/seat).

**Not proposing a number.** Flagging that the June price was set before we decided Basic+Pro *is* the individual business.

---

## A7 — The prompt taxonomy is aimed at the wrong limits.

Falls out of A1: **UP-1 (fixes), UP-2 (chat), UP-5 (deep/day)** are friction prompts on caps that **never bind**. **UP-6 (the monthly gate)** is the one users will actually hit — and it's specified *"soft, gentle, once/month."*

**Recommendation:** UP-6 becomes the **primary** monetization prompt, and it must be an **honest limit disclosure in analyses** — *"You've used your 8 analyses this month. Basic gives you ~20."* If A2/A3 land, **UP-1 and UP-2 disappear entirely** (there's no cap to hit), which is a simplification, not a loss.

---

## Summary — what I'd change

| | Change | Why |
|---|---|---|
| **A1** | Lead with the **monthly analysis budget in analyses**; demote daily caps to invisible rate-limits | The governor binds 8–9× before any daily cap. The product surfaces the wrong limit. |
| **A2** | **Drop the daily fix cap** | Meters a near-free action; taxes the activation moment; coalescing already saved the cost. |
| **A3** | **Drop the daily chat cap** | Meters comprehension for pennies; collides with D126. |
| **A4** | **Coalesce reviewer evidence into one run** | Otherwise collaborators eat your budget and CR-2 dies in practice. |
| **A5** | **Seats tight below Team** | Basic-10 cannibalizes a $99–149/seat tier. |
| **A6** | Revisit **Basic $12** | Priced before we decided Basic+Pro is the individual business. |
| **A7** | **UP-6 becomes the primary prompt**; UP-1/UP-2 disappear | Prompts currently fire on limits that never bind. |

**Net effect:** *one* honest, legible limit — **analyses per month** — instead of four caps, three of which never fire and two of which tax the behaviours we most want. Fewer numbers, all of them true.

These supersede ratified values (§4c, MON-02/03, UP-1/2/5/6). **Owner ratifies; route via Framework 001 + `dl-land`.**

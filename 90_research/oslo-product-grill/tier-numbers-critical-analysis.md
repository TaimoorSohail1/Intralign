# Critical analysis — do the ratified tier numbers cohere?
Owner-requested, 2026-07-11. **REWRITTEN 2026-07-11 after finding `RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c`.**

> ## ⚠️ Correction of record — read this first
> The first version of this analysis rested on an **incomplete scan**. I scoped to `10_product/` and `00_owner/` per the product-grill discipline. **The full ratified tier ladder lives in `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c`** — the engineering zone.
>
> Consequently **three of my findings were wrong**, including two I called *blocking*:
> - **S1 (fix cap vs run cap "contradict")** — **WRONG.** §4c: *"Deep concurrency **1 + coalescing on** — structural; prevents runaway re-analysis."* Coalescing is ratified and on. The caps cohere.
> - **S2 ("nothing bounds Free analysis cost")** — **WRONG.** §4c sets a **monthly token budget of 4,000,000/user — explicitly "the binding governor"** — plus a 500k daily burst-smoother and a ~$3/mo alert KPI. Every path is bounded, CRR included.
> - **S6 ("Basic's headline numbers don't exist")** — **WRONG.** Basic is owner-confirmed (2026-06-05): **$12/mo · 3 projects · 6 deep runs/day · 20 fixes/day · 75 chat/day · 10M governor.**
>
> Also wrong: I called UP-4's "~100k words" *illustrative, not ratified*. It **is** ratified — Basic's envelope is ~40 docs / ~100k words.
>
> **This is the third time in this engagement that I reasoned from my own model where canon had already spoken** (see also: Basic = 10 projects; "Pro/Team is the org sale"). The pattern is the failure the Anti-Assumption protocol exists to catch, and the correction belongs on the record, not in a chat log.

---

## The ratified ladder (all of it — nothing here is proposed by me)

| | **Free (T1)** ✓ | **Basic (T2)** ✓ | **Pro (T3)** | **Team (T4)** | **Enterprise (T5)** |
|---|---|---|---|---|---|
| **Price** | $0 (CAC/subsidy) | **$12/mo** | ~$39/mo | ~$99–149 **/seat** | custom |
| Active projects | 1 | 3 | 10 | many | custom |
| Envelope (docs/words) | ~20 / 50k | ~40 / 100k | ~80 / 200k | ~150 / 400k | custom |
| Deep runs / day | 2 | 6 | 15 | on-demand | custom |
| Fixes · chat / day | 5 · 20 | 20 · 75 | 50 · 200 | high / unmetered | custom |
| Model routing | nano/mini | nano/mini *(same class)* | mini + full-quality fallback | **premium** | premium + dedicated |
| Monthly token governor | 4M | 10M | 25M | 50M / seat | negotiated |
| Worst-case cost/mo | ~$3 | ~$8 | ~$20 | ~$97 | custom |
| **Collaborator seats** | **—** | **—** | **—** | **per seat** | custom |

Sources: `RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` (T1/T2 owner-confirmed; T3–T5 via **DL-074**) · `BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE` (taxonomy, owner-set 2026-06-05) · **UP-1/2/3/5** · **DL-083** (execution monitoring = Pro+).

**Design rule (ratified):** *Basic sells **capacity**; Pro adds **model quality**; Team/Enterprise are **per-seat** with premium routing.*
**Owner clarification (2026-07-11):** Pro also adds **execution & program support**; Team/Enterprise add **governance & portfolio**. Consistent with DL-083 and the GTM "individual wedge → team → org/portfolio" motion. Basic + Pro = the **individual** motion; Team + Enterprise = the **org** sale.

---

## What survives — the findings that are still real

### **S5 — Collaborator seats are the ONE undefined dimension in the entire ladder. (Now the sharpest item.)**
Look at the seat row above: **empty for Free, Basic and Pro.** §4c never sets it. My **Free 3 / Basic 10** (DL-102 E) is the only proposal in existence — and it is **commercially wrong**:

> **Team is priced ~$99–149 *per seat*. If Basic ($12/mo) grants 10 collaborator seats, a ten-person team buys ONE Basic subscription instead of Team. That guts Tier 4.**

**Resolution, and it costs nothing:** CHG-061 requires the viral primitives on Free — but those run on **unlimited Viewers** and **free, unmetered Reviewers (CR-2)**, *neither of which consumes a seat*. So **collaborator seats can be tight across Free/Basic/Pro without breaching CHG-061.** Individual tiers grant enough collaboration to do *your own* work; **Team is where collaboration becomes the product.**
**Basic's seat count must fall well below the point where a team would rationally buy Basic over Team.** The number is the owner's; the constraint is structural.

### **S2′ — CR-2 vs. the binding governor. (The real conflict, replacing my wrong S2.)**
- **CR-2 (DL-102, load-bearing):** evidence-seeking is **never metered** — a reviewer's answer must never be refused.
- **CRR-04:** every reviewer response **triggers an Extended Analysis**.
- **§4c:** the monthly token rollup **"gates further AI spend — never silent overspend."**

**What happens when a reviewer's evidence arrives after the governor has gated?** Undecided.
**Recommendation (derived from canon's own graceful-degradation posture):** **record the evidence, defer the run, disclose honestly.** The attestation is never refused (append-only, CR-2 honoured); the analysis run **defers**, with an honest line — *"Priya's answer is recorded. Your read will update when your monthly analysis budget resets, or on upgrade."* Cost bounded, evidence never lost, product honest about what it hasn't yet done. It is the only resolution where all three constraints survive.

### **S3 — 5 fixes/day may still cap activation.**
The activation moment is **fix → the read moves**. A freshly analyzed plan routinely surfaces more than 5 issues, so the natural first session can hit the cap mid-activation. Canon's counter is explicit — MON-02 lists the allowance's value as **"Habit + re-engagement"** — so the cap is *designed* to trade activation for return-rate.
**Recommendation:** instrument fixes-applied-before-first-cap-hit in Alpha. If most first sessions hit it, the cap is eating activation. A **first-project grace** fixes it without touching the steady-state number. (Note: coalescing means 5 fixes ≠ 5 runs, so the cost of a grace is small.)

### **S4 — the chat cap brushes D126 in principle.**
*"Never meter who gets an answer."* Chat is how a user gets an answer **from OSLO** about their own read. Metering it meters comprehension. Defensible as a **cost** control (D128 P1) — Free 20/day and Basic 75/day both sit above genuine use — but the copy must never imply you must pay to understand what OSLO already told you.

### **S7 — the project cap is concurrency, not volume.**
Archiving is reversible and frees the slot (DL-058, UP-3's own resolution), so Free users can work unlimited plans **sequentially**. The cap bites only when two plans must be open at once. Honest, but it converts fewer people than "1 vs 3" implies.

### **OD-10 — the coalescing window is the highest-leverage unset number.**
Coalescing is **on** (§4c) but the **window** is `TBD – Owner Decision Required` (`OPEN_DECISIONS` OD-10). It determines how many runs a working session produces — i.e. whether 5 fixes cost 1 run or 5. **It is a bigger cost lever than any cap, and it costs the user nothing.**
**Recommendation:** **settle/idle-based**, single-active, plus the canonical **manual** trigger (which the Deep Pass spec already lists — so **T10-2 dissolves**: UP-5 has a real affordance to cap and D006 is not violated).
**UX rationale, not just cost:** you already rejected the eager model in Slice 5 — *"the reanalysis is too responsive."* A strategic read that recomputes on every keystroke reads as a **live score, not a considered judgment**; confidence is *understanding maturity* and should move when understanding changes, not when a character does. Preserve the aha by showing the **causal delta** after each settled run — *"You changed 3 things → Clarity ↑, Feasibility unchanged"* — which is a **stronger** payoff than a twitching number, because it is attributable.

---

## Token credit packages — canon already decided this, and against them

**DL-074 (Ratified)** adopted **tier subscription + metered overage**, unit = **per-Deep-Pass**, under a "usage-based" umbrella. Its provenance line answers the question directly:

> *"overage unit/scope selected by the owner after a PLG/AI-pricing best-practice review (**and a strong-form trade-off argument for per-Deep-Pass vs. abstract credits**)."*

**Abstract credits were weighed and rejected.** Reopening it supersedes a ratified Class-A decision.

**And the ratified choice is right for this product.** A token is a unit the user cannot value or predict. For a product whose promise is *clarity*, selling an unintelligible unit is self-undermining — and credits put a **taxi meter on comprehension**: if a user hesitates to ask OSLO a question because it burns credits, the product has failed at the thing it exists to do. **Per-Deep-Pass is legible** — *"one more analysis."*

**If the goal is prepaid ergonomics, keep the unit and change the packaging:** sell **analysis packs** — a prepaid balance denominated in **analyses, not tokens**. DL-074 permits exactly this: *"Adding units later is an **ADD, never a reframe**."* Same compute-unit governor underneath (tokens × model-tier weight); legible currency on top.

**Constraints any pack must inherit:**
- **DL-074 §3 — overage is PAID TIERS ONLY.** *"Free converts via upgrade… no Free purchase path."* A Free credit-purchase path would blunt the upgrade motion and muddy the honest-limit disclosure. Leave ratified.
- **DL-074 §5 guardrails** — visible meter, **user-set spend cap**, threshold alerts, **no silent overspend, no bill shock.**
- **Packs must not expire.** Breakage revenue is not a business a credibility-based product should be in.

---

## The real gap — restated correctly

**The tier values are not missing. They are in the wrong zone, under the wrong name, and nothing consolidates them.**

They live in **`30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c`** (engineering config) and in `BACKLOG_TIER_PROGRESSION` (a backlog item), while **18 product documents cite a *"Release 1 Tier Definitions"* that does not exist.** Product-scoped readers — human or AI — will not find them. I didn't.

**`RELEASE_1_TIER_DEFINITIONS_V1` should therefore be written as a product-authoritative surface that consolidates and names what is already ratified**, rather than as a document that decides anything new. What it must add:

| Genuinely open | Note |
|---|---|
| **Collaborator seats, Free/Basic/Pro** | The only undefined ladder dimension. Must protect Team's per-seat sale (S5). |
| **OD-10 coalescing window** | Highest-leverage unset value; bigger cost lever than any cap. |
| **CR-2 vs. the binding governor** | What happens to evidence that arrives after the gate (S2′). |
| **Free CRR cap** (B-1 cost ceiling) | Abuse/cost guard only; must never fire an upgrade prompt. |
| **MON-04 global prompt cap/day** | Required by canon, never set. |
| **Billing rail** | Engineering; T-4. |

Everything else in the census is **RATIFIED and should be cited, not re-decided.**

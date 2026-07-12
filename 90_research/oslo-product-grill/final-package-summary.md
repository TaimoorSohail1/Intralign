# OSLO R1 — Final Package Summary (product-grill close-out)

**Date:** 2026-07-12 · **Scope:** Release 1 (Alpha) product experience · **Status:** complete — 10/10 slices signed off
**Decisions:** D001–D142 (`decision-log.md` is authoritative)
**Canon ratified out of this engagement:** **DL-102** · **DL-103** · **DL-104**

> **Non-canonical.** This package is a product-grill output. It **recommends**; only the repository owner **ratifies**,
> and every canonical change routes through **Framework 001** and the **`dl-land`** serializer (DL-065 §5).
> Nothing here supersedes canon. Nothing here invents a product number.

---

## 1. What was built

**Ten cumulative vertical slices.** Each slice is a complete module — all of its major use cases, not a screen — and each
prototype contains every slice before it. Ten prototype files exist, but there is **one product**.

| # | Slice | Decisions |
|---|---|---|
| 1 | Access & Onboarding — invite-gated Alpha activation, four start methods, one-time strategic-chain orientation | D021–D034 |
| 2 | Intake & Fast-Pass Orientation — Initial Analysis → the 60-second orientation → Extended Analysis auto-runs and supersedes | D035–D049 |
| 3 | Project Overview & Understanding Console — confidence-led Overview, CAF maturity bars, reliability qualifier, false-confidence flag | D050–D056 |
| 4 | Attention Map (MRI) — 7 plan artifacts × Clarity·Alignment·Feasibility; cells route to scoped Issues | D057–D065 |
| 5 | Plan Artifacts / Artifact Workspace — type-aware editor, inline issue annotations, From OSLO / Confirmed by you, table provenance | D066–D085 |
| 6 | Issues & Recommendations (Panel Model) — all-issues surface, full Issue Panel, Open→Addressed→Resolved, Apply this fix, clarification loop; app shell + ⌘K palette | D086–D095 |
| 7 | History & Confidence Trend — append-only timeline grouped by analysis run, per-run deltas, understanding-over-runs trend | D096–D101 |
| 8 | Multi-Project Workspace & Awareness — Workspace Home, switcher, notifications, Settings/Appearance; OSLO chat made functional and advisory-only | D102–D109 |
| 9 | Collaboration, Sharing & Export — roles + snapshot links, comments/@mentions, export snapshot, CRR review loop + reviewer view, controlled release + waitlist | D110–D133 |
| 10 | **Tiering & Limits — THE DELIVERABLE** — live Free→Basic in Alpha, one honest limit, the upgrade-prompt engine, the limit-reached rule at every cap, the **Reports** surface, the tier-definitions census | D134–D142 |

### The deliverable

> **`vertical-slices/slice-10-tiering-limits/prototype.html` — 13,237 lines. Always demo the highest-numbered
> prototype.** Open it in a browser. No server, no build. `prototype-index.html` links all ten and marks it.

**Earlier slices are historical snapshots.** Refinements were folded **forward, never backward**: a defect corrected in
slice 8 was fixed in slices 8, 9 and 10 and was *not* back-ported into 1–7. Slices 1–9 therefore carry known refinement
debt — superseded copy, pre-cascade shells, decisions later reversed, and (in slice 9 and below) the entire pre-DL-103
tier model. **They are a record of the sequence, not a spec.**

The final prototype carries the whole R1 experience end to end — intake → Initial Analysis → confidence-led Overview →
Attention Map → Plan artifacts → Issues & recommendations → History → Workspace → sharing, comments, export and the CRR
evidence loop → Reports → tiering and limits — and it demonstrates the **doctrine**, not just the screens: advisory-only;
confidence = understanding maturity (never health, readiness, or probability of success); issues close only through an
analysis update; the three epistemic classes; the epistemic record never metered; safety never sold; evidence never
gated; owner-TBD values rendered **visibly unset** — with 17 runtime boot assertions that fail loudly if a future
contributor, human or model, quietly re-adds an invented number.

---

## 2. What canon gained — the real output

**The prototype was the assignment. The canon findings were the value.**

The grill was commissioned to build the R1 experience, and it did. But the act of trying to *implement* the tier model
forced three questions no document had ever been made to answer. The answers are now ratified canon. That is the durable
output of this engagement; the HTML is the instrument that surfaced it.

### DL-102 — Controlled Release & Tiering-in-Alpha

- **The invite IS the authentication.** A review-request link carries a token granting a **Reviewer Principal** (DL-049),
  scoped to that review package only. The reviewer is *identified and invited* — **never anonymous** — which resolves the
  standing tension between *"Alpha is never anonymous"* (DL-021) and the audit's no-account reviewer, with no signup wall
  and without breaking the CRR loop.
- **CR-2 — bound seats, never bound evidence. Load-bearing.** Review requests are **never metered for monetization**, on
  any tier, in any phase. This is the **sole resolution of the CHG-061 conflict**: with reviewer grants free, the seed of
  the viral loop is ungated on every tier and in every phase, and only **seats** are metered — so CHG-061 holds
  literally. It is not a preference. Nothing else reconciles the two rules.
- **Two limits, never conflated (D124).** PHASE (supply) and TIER (depth) are orthogonal, and both are live in Alpha. The
  product must **always name which limit blocked the user**. Presenting a supply constraint as an upsell is a prohibited
  dark pattern.
- **Never meter the epistemic record; never sell safety (D128).** Artifacts uncapped. History never expires. Link
  revocation and purpose-scoped expiry are free on every tier. **No eviction on downgrade** — no human is ever removed to
  enforce a billing change.

> **The governing principle:** *Meter who gets a seat. Never meter who gets an answer. And always say which limit you
> just hit.*

### DL-103 — Analysis cost basis & tier re-derivation

- **Never tier judgment quality. Doctrinal.** One judgment bar for every tier; model routing is chosen **by step** (cheap
  models to extract, the best available to judge) — **never by tier**. Tiering it would make **Reliability a function of
  the billing plan**, forcing the product to say *"your read is less reliable because you are on Free."* That is fatal
  for a product whose only asset is telling you the truth about your plan. And the market evidence says the doctrinal
  choice is *also* the better-converting one: gating usage **intensity** out-converts gating model **intelligence**.
  (Supersedes *"Pro adds model quality."* Pro's differentiator is execution & programme support.)
- **The cost basis was stale, and nobody had noticed.** The ladder was priced on **rented frontier tokens one day after
  canon ratified local inference.** DL-069 (2026-06-18) made an internal Gemma on a local Llama runtime the primary LLM
  expressly to remove external token cost — and §4c and DL-074 (2026-06-19) derive every governor, every price and the
  ~$3/mo Free ceiling from rented frontier pricing anyway. **Every tier number in canon inherited an assumption canon
  itself had abandoned.** §4c's numeric basis is now **suspended pending re-derivation**.
- **The engine does a full re-derivation on every run.** A grep of the analysis engine for *prompt caching · incremental
  · differential · scoped recompute · cache* returns **zero hits**. With **E1 (prompt caching) + E2 (incremental/scoped
  recompute)**, the same $3/month ceiling buys **~74 analyses instead of ~12**. No model change. No quality trade. Free's
  "~8 analyses/month" was never an economic fact — it was an artifact of a superseded rental basis and an unoptimized
  engine.
- **One honest limit, in the user's currency: analyses per month — never tokens.** Daily caps are demoted to invisible
  burst-smoothers.
- **§7 — the Free→Basic conversion model.** The principle: ***meter the inputs and the outputs; never the understanding
  in between*** — which is what canon's own "Constrain:" list already implied. **Latency was struck**: an async product
  cannot sell speed, and the one moment latency would truly bite is the one moment §7b forbids monetizing. **Labour, not
  latency.** The **assisted-apply cap is retained**, bound by *the recommendation is always visible; only the assisted
  apply is metered; manual editing is always free*. The **reverse trial** is bound by *take back the pipes, never the
  read*. **Outcome-based pricing is PROHIBITED** — it would require charging against delivery results OSLO deliberately
  refuses to predict. And **reporting is the #1 lever — a STATUS lever, not a labour one.**

### DL-104 — Errata to DL-103

**DL-103 contradicted itself, and the Slice-10 build could not implement it. That is how it surfaced.** §7c struck the
priority/latency lever; §7e, §1 and §5 still assumed it. A downgrade cannot take back a lever that was never built.

- **The priority/latency residue is struck** wherever it survived. No priority queue at any tier. Artificial delay
  remains prohibited. Fast Pass never queues — a **product guarantee** (DL-046), not a lever.
- **UP-1 / UP-2 / UP-5 retired at source** — struck in place in the ratified UP-* taxonomy (not deleted; the reasoning
  must stay inspectable). **UP-6 (the monthly analysis budget, expressed in analyses) is the primary limit.**
- **UP-APPLY and UP-REPORT numbered** — the two prompts DL-103 created without canon numbers. UP-APPLY's threshold is
  **owner-TBD, from Alpha instrumentation, never from a cost model — and until that data exists, no cap.**
- **DL-102 constituent E refreshed** — its numeric adoptions are superseded by DL-103; its **structural rules stand
  unaltered**, and **CR-2 is untouched**.
- **A new P1 defect class:** any report a reader could mistake for a **health rating, RAG status, readiness score, or
  probability of success**. Not a copy nit — a P1. *A hallucinated claim in a status update is embarrassing; in a
  board-level strategic read it can end a career.*

> **Canon that contradicts itself is canon that will be resolved by whoever implements it last.** The governance model
> exists to prevent exactly that — and the build is what caught it.

---

## 3. The convergence worth remembering

> ### OSLO's epistemic honesty is what makes the PM look strategic.
> **There is no trade-off between the doctrine and the commercial value. They are the same artifact.**

A status report — *"60% done, three tasks late"* — makes a PM look like a **clerk**. Every PM produces it; it confers no
standing. What confers standing is **naming what nobody else has named**:

- *"The sponsor and engineering hold different definitions of done — here is where they diverge."*
- *"This plan rests on three assumptions nobody has validated."*
- *"Here are the two decisions I need from you, and what each unblocks."*
- *"Our understanding matured from Orientation to Validated this month — here is what changed and why."*
- *"The single change that would most improve this plan."*

**That is exactly OSLO's existing output** — CAF, the clarification register, unresolved assumptions,
understanding-maturity over time, evidence provenance. *"Here is what we know, here is what we are assuming, here is what
we have not validated"* is how senior people talk.

Which is why the epistemic discipline is not a tax on the commercial model. It **is** the commercial model. The PM is
staking their own credibility on OSLO's output, in front of their leadership, under their own name — so rigorous
reliability-qualification is not *despite* the status goal, it is *because of* it. **Epistemic discipline in reporting is
protection of the user's reputation, and that is what they are actually buying.**

---

## 4. BLOCKING work items (owner) — and none of them are pricing decisions

**This is the section that matters.** The instinct after a tiering engagement is to go and set prices. That would be the
wrong move: **the numbers cannot be tuned, they must be re-derived** — and three things gate the derivation.

### 4.1 — Judgment-quality eval of the local model (DL-069)

Does the internal Gemma / local-Llama runtime clear the judgment bar on the **CAF / issue-detection** task? **This is an
empirical question and it cannot be settled on paper.** DL-103 §1 forbids tiering judgment quality, so there is exactly
one bar, and the local model either clears it or it does not. Everything downstream — the cost basis, the ladder, the
price — depends on the answer. **Nothing else in this list can be honestly completed before it.**

### 4.2 — E1–E3: the missing engine economics

- **E1 — prompt caching / KV-cache reuse.** The plan corpus is stable between runs; pay full price only for the delta.
- **E2 — incremental / scoped recompute.** A fix to one artifact re-analyzes *that artifact and its dependency closure*,
  not the whole corpus. (This is what AE-03 should have said.)
- **E3 — evidence coalescing.** Reviewer responses arriving in a window settle into **one** run. **Without it,
  collaborators silently consume the user's analysis budget; users learn that asking for evidence costs them their own
  read — and they stop asking. CR-2 dies in practice, and with it the loop DL-102 exists to protect.**

**E1–E3 are the highest-leverage unbuilt work in the product** (~6.4× on cost, at zero cost to quality). Tuning the
ladder before they land would bake a ~6× penalty into pricing permanently.

### 4.3 — The Reporting specification (M4)

**`Reporting & Analytics` is a named R1 milestone with ZERO capability rows and no specification.** SHARE-01…05 are
*sharing*, not reporting, and the Export spec explicitly disclaims the role (*"it packages existing understanding; it
never produces new understanding"*). So the surface that is simultaneously **the strongest conversion lever**, **the best
viral surface** (a PM sends it to eight executives — the passive loop aimed *upward*, at budget holders rather than
peers), and **the highest-reputational-risk output in the product** currently exists **only as a name**.

See **`reporting-specification-scope.md`** — six candidate report types, the binding epistemic constraints, the
Free/Basic split (*the seed is not gated; the depth is*), and what is explicitly out of scope. Report **names** are an
owner/glossary decision (DL-053) and are **not proposed** there.

---

## 5. OPEN — owner decisions required

Live list, from `slice-10-tiering-limits/open-items.md` and `tier-definitions-census.md`.
**The census now stands at 58 values: 39 ratified · 3 pending re-derivation · 8 retired/struck · 5 unset · 3
recommendation.** Nothing below is assumed, defaulted, or quietly filled in; each ships **visibly unset**.

| # | Decision | Status in the build | The decision the owner owes it |
|---|---|---|---|
| 1 | **Monthly analyses — Free / Basic** | ⏳ **pending re-derivation; nothing enforced** | §4c's numeric basis is suspended. Re-derive after the eval + E1–E3 + a real cost-per-analysis measurement. Expect an **abuse ceiling, not a product limit**. **Do not tune it now.** |
| 2 | **Basic price — the BASIS** | ⏳ **$12 kept, basis marked pending** | The **value** is owner-confirmed (§4c). Its **basis** is suspended. $12 may well survive — but it must survive a **derivation**, not an **inheritance**. |
| 3 | **UP-APPLY threshold** (daily assisted-apply cap, Free) | ⬜ **UNSET ⇒ no cap.** Mechanism + at-cap prompt built; threshold inactive | **From Alpha instrumentation, NEVER from a cost model.** **Placement is the whole decision: above activation, below power use.** It is a monetization lever, and the record says so plainly rather than dressing it as a cost control. |
| 4 | **Collaborator seats — Free / Basic** | ⚠️ **RECOMMENDATION** (3 / 10), rendered in-product as *not ratified* | **The only structurally undefined dimension in the ladder.** DL-103 **withdraws Basic = 10** as commercially unsound: a $12 Basic granting ten seats cannibalizes a ~$99–149-**per-seat** Team. **No replacement invented.** CHG-061 is safe either way — Viewers are unlimited and Reviewers are free, and neither consumes a seat. |
| 5 | **OD-10 — the Deep-Pass coalescing window** | ⬜ **UNSET** | The highest-leverage cost lever in the product, **and it costs the user nothing**. Bounded by §7d-bis: the window keys off the **user's journey** (new ▸ established), **never the tier**. |
| 6 | **Free CRR cost ceiling** | ⬜ **UNSET** | The bounded-cap **mechanism** is canon (D118 / B-1); the **number** is not. Doctrine bounds it hard: virality seeds on Free (CHG-061) and evidence-seeking is never bounded (CR-2). It may gate **depth/volume**, never the **existence** of the loop — and **it must never fire an upgrade prompt**. |
| 7 | **MON-04 global prompt cap / day** | ⬜ **UNSET** (guard enforced with a conservative prototype-local value, labelled as such) | MON-04 **requires** the guard; §4d's "≤2/day, ≤1/session" is *proposed* config, never ratified. The build errs toward **silence**. Set it, or ratify *"err toward silence."* |
| 8 | **Report names** | ⬜ **UNSET** — reports labelled descriptively and flagged *"naming pending"* | Owner / glossary decision (DL-053 Disambiguation Register). **The build does not name canon.** |
| 9 | **Which reports are R1 · scheduling · branding · `REP-*` capability rows** | ⬜ **UNSET** | Blocked on the Reporting specification (§4.3). |
| 10 | **Billing rail** | ⬜ **UNSET** (T-4) | Engineering. **The price is not the open question — the rail is.** It must carry DL-074 §5 (visible meter · user-set spend cap · threshold alerts) and §7g (one click, self-serve, no sales call). |
| 11 | **CR-2 vs the budget gate** | ⚠️ **RECOMMENDATION** implemented and labelled: **record · defer · disclose** | The evidence lands immediately and unconditionally; the *run* defers, honestly. The only resolution in which CR-2, CRR-04 and the governor all survive — **and E3 (evidence coalescing) is the real fix.** |
| 12 | **Reverse-trial duration (~14 days)** | ⚠️ **REC — GA-phase only; not live in Alpha** | The **mechanic** is ratified (§7e); the **duration** is not. |

**Also open, not blocking:**

- **The Suggest-Alternative alignment signal** — deliberately unbuilt. DL-102 F makes Approve and Reject Alignment
  evidence; treating *"here's a better way"* as a negative alignment input would bias against the most constructive
  response a reviewer can give, and nothing in canon says it should. **Not inferred. Not built. Owner to decide.**
- **Whether revenue ever expands onboarding capacity.** CR-7 prohibits pay-to-skip because **payment does not create
  capacity** — selling passage past the queue is a toll booth on an invented constraint. If revenue ever genuinely
  expands supply, **CR-7 re-opens** — and it must be said plainly when it does.

**Also worth doing:** commission `RELEASE_1_TIER_DEFINITIONS_V1` as a **product-authoritative surface that consolidates
and names what is already ratified** — not as a document that decides anything new. Writing it as a *decision* document
invites a second round of invented numbers.

---

## 6. Corrections of record

Stated plainly, because they are already public in canon.

1. **"CRR is a spec gap" was FALSE.** CRR-01…05 are ratified, Alpha-scope canon, and **DL-049 had already resolved gap
   #337** (external-reviewer identity: a single `Principal`, `type: reviewer|user`, promoted in place). The earlier
   "CRR out of scope — escalated spec gap" position was an **over-escalation on my part**. Corrected 2026-07-10; CRR is
   built (D114), and DL-102 A now makes the invite itself the authentication.
2. **The tier-vs-phase reconciliation of CHG-061 is DEAD.** It argued the two rules could never collide, because CHG-061
   is a *tier* rule that takes effect at GA while controlled release is a *phase* rule that sunsets there. The owner then
   confirmed that **Basic is purchasable during Alpha** — so the tier rule does not wait for GA, and both axes are live
   simultaneously. **CR-2 is the sole resolution**, and is therefore **load-bearing, not a preference**.
3. **"Basic = 10 projects" was AI-invented, against ratified canon.** **UP-3** states, in the product's own words:
   *"Free includes 1 active project — Basic gives you 3."* The invented 10 propagated from a recommendation → an owner
   ratification made **on my advice** → the D129 register → the Slice-9 prototype → **and into a hard-coded copy string**
   that would have survived a constant-only fix. It reached an open PR and was **withdrawn on the record**. Corrected
   everywhere (D141); the build implements **3**, cited to UP-3, and **every displayed tier number is now painted from
   its constant**, so copy cannot drift from canon again. *(The **seat** caps — Free 3 / Basic 10 — are a different
   quantity and were never in conflict, though DL-103 has since withdrawn Basic = 10 **seats** on commercial grounds.)*
4. **A decision record was hand-authored outside the `dl-land` serializer**, in breach of **DL-065 §5** ("the Founder
   Console is the sole path that authors, numbers, and releases decisions to `main`"). It produced a **duplicate
   (DL-101)** which had to be **voided and retained** for traceability. The canon that survives is **DL-102**, landed
   through the serializer. The rule exists precisely to prevent this — and it caught it.
5. **The tier ladder was never "missing." It was in the wrong zone.** The numbers were ratified all along — in the
   **ENGINEERING** zone, at `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1` **§4c** — while **18 product
   documents cite a `RELEASE_1_TIER_DEFINITIONS_V1` that does not exist.** A product-scoped reader, human or AI, does not
   find them. **An AI that cannot find a number invents one.** That is the mechanism behind correction 3. It is a
   governance defect, not a documentation nicety.
6. **The latency lever was recommended as primary, then struck.** An earlier draft made *"Free queues; Basic runs now"*
   the headline lever. It is **withdrawn: an async product cannot sell speed.** Latency only bites when the user is
   blocked, and OSLO is deliberately designed so that they never are — except for the one moment (*"I have a stakeholder
   meeting in ten minutes and I need the current read"*) that doctrine forbids monetizing. **Latency friction is
   therefore either worthless or predatory. There is no useful middle.** Sweeping up the residue of that reversal is what
   DL-104 exists to do.

**The pattern in all six:** every one is an **assumption that was not escalated**, or a **consequence that was not swept
through**. That is what `ANTI_ASSUMPTION_BUILD_PROTOCOL` forbids, and it is why Slice 10's governing rule was **canon
decides; the build adopts and cites; where canon is silent, the product says so** — and why the final prototype carries
17 runtime assertions that fail loudly if any of it is quietly undone.

---

## 7. Verification (final prototype)

| Check | Result |
|---|---|
| `node --check` on the extracted `<script>` | **PASS** (9,929 lines of JS) |
| jsdom parse **without** `runScripts` → body child count | **32** (healthy) |
| Boot assertions (`window._S10`) | **17/17 PASS** — `d138` · `mon04` · `tbd` · `record` · `cr2` · `nofreebuy` · `seats` · `viewers` · `noTierQuality` · `budgetInAnalyses` · `chatUncapped` · `recNeverHidden` · `updateNowFree` · `noLatencyLever` · `downgradeKeepsRead` · `noOutcomePricing` · `reportsNoHealth` |
| Runtime console (errors + warnings) | **0** |
| `prototype-index.html` links | **11/11 resolve** |

The boot assertions are the anti-drift mechanism, and the list is worth reading as one: it is the doctrine, executable.

---

## 8. Package contents

```
oslo-product-output/
├── prototype-index.html                  ← start here (links all 10; marks the deliverable)
├── final-package-summary.md              ← this file
├── slice-signoff.md                      ← the per-slice sign-off record
├── decision-log.md                       ← D001–D142 — AUTHORITATIVE
├── tier-alignment-review.md · tier-numbers-critical-analysis.md
├── analysis-cost-basis-and-tier-rederivation.md   ← the analysis behind DL-103
├── reporting-specification-scope.md              ← the M4 commissioning brief
├── controlled-release-demand-framework.md · open-questions.md · canonical-truth.md
├── vertical-slices/
│   ├── slice-01 … slice-09/              ← historical snapshots (refinement debt; folded forward only)
│   └── slice-10-tiering-limits/          ← ★ THE DELIVERABLE
│       ├── prototype.html                    Slices 1–10, cumulative · 13,237 lines
│       ├── tier-definitions-census.md        58 values · 39 ratified · 3 pending · 8 struck · 5 unset · 3 rec
│       ├── open-items.md                     the live owner-decision list
│       └── (7 house docs + edge-cases + success-criteria)
└── worker-reports/                       ← per-slice build reports
```

---

**Only the owner ratifies. This package recommends.**
Canonical changes route through **Framework 001** and land through **`dl-land`** — one PR in flight, merged linearly
(DL-065 §3).

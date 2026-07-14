# Slice 10 — Tiering & Limits · E2E Test Scenarios

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
| **§7j** → **D148–D154** | **REPORTING (M4) is the #1 lever — and it is a STATUS lever.** ⚠️ **REBUILT 2026-07-12 (owner-directed): D148–D154 REVISE D144/D146/D147.** Reports is a **WORKSPACE, not a modal**. The report is an **executive summary written for its reader, in their language** — **ZERO OSLO vocabulary in the body**. **Editing is FREE on every tier; the gate is REUSE** (Basic remembers your wording). | **Reports = a peer view** (`#pane-reports`, `showView('reports')`) — left the **live composer** (`#reportsBody`), right the **package wrapper** (`#rptPkg`) and the **document** (`#rptDoc`). **Seven sections, fixed order** (summary · what changed · **risks BEFORE assumptions** · assumptions · plan of action · decisions · appendix). **Two altitudes on every risk** — *for the plan* (deliverable) and *for the goal* (**does the plan, AS WRITTEN, still reach its intent — a structural claim, never a forecast**). **The plan of action is the PM's, in the first person** — OSLO seeds, the PM owns. **The disclaimer is on the PACKAGE, not in the prose**; the **currency marker stays in the body** as plain attribution. **Tailor the ask, never the read** (D145 stands): only §6 changes with the recipient. Guards: `_assertNoOsloVocabularyInReport()` · `_assertNoForecastLanguageInReport()` · `_assertReportStructure()` · `_assertPlanOfActionIsPMVoiced()` · `_assertDisclaimerOnPackageNotInBody()` · `_assertEditFreeOnEveryTier()` · `_assertAskTailoredNeverTheRead()` · `_assertReportPackagesNeverProduces()` · `_assertScheduledReportRechecksCurrency()` · `_assertReportsNoHealthFraming()`. |

## §7f — the in-plan conversion moments, surfaced honestly (not sprung)

connected sources (day 1, forever) · reporting (weekly) · export/sync → execution tool (DL-083, Basic) · bulk actions · **one live understanding** (archived = read-only, the read freezes; **archive stays reversible**, DL-058) · the **envelope** (UP-4 partial read, honestly disclosed) · **plan 2** (a pull, not a wall).

## §7g — upgrade mechanics

**One click. Self-serve. Price on the button. No sales call, ever.** Triggers on **behaviour and realized value, never a calendar** — the value-moment class (UP-7/UP-8) is **strengthened**, not an afterthought.

## The guardrails that did NOT move

Never meter the epistemic record (artifacts uncapped · History never expires) · never sell safety · **CR-2** (evidence-seeking never bounded) · **D124** (never present a PHASE limit as a TIER upsell) · no eviction on downgrade · no fabricated scarcity · **MON-04** (no upgrade wallpaper) · every prompt names the specific limit **and** the specific tier · **no invented numbers — unset renders unset** · advisory-only (chat never mutates).


> ## ⚠️ AMENDED 2026-07-11 — the tier ladder was RATIFIED all along
> `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` carries **owner-confirmed rows for every tier**. Five values this slice rendered as *"owner-TBD"* are ratified: **Basic price $12/mo · Basic chat 75/day · Basic deep-runs 6/day · envelope Free ~20 docs/50k words + Basic ~40/100k · the monthly gate = the token governor (Free 4M · Basic 10M — "the binding governor")**. One value marked RATIFIED is **not**: the **collaborator seat caps** (§4c has no seat row below Team). Superseded passages below are marked in place. Full detail: `tier-definitions-census.md`.


**Automated status: 55/55 behavioural · 24/24 non-regression · `node --check` PASS · jsdom body children = 31 (Slice 9: 29 + the 2 new surfaces) · 0 console errors.**

## S10-1 — The correction (the reason this slice exists)
1. Open the prototype → console: `BASIC_PROJECT_CAP`.
2. **Expect `3`, not `10`** — the value ratified by **UP-3**.
3. Open **Plans** → Basic reads **3 active projects**. Sidebar sub-line reads **3 projects** on Basic.
4. **Expect:** no string anywhere hard-codes a tier number — every displayed number is painted from the constant.

## S10-2 — Every capped affordance stays enabled, and the attempt prompts (D138)
| Step | Expect |
|---|---|
| `Sim daily fixes used` → open an issue → **Apply this fix** | button is **enabled**; clicking it opens **UP-1** (*"Basic gives you 20/day"*) with **upgrade · wait for the daily reset**; **the issue does not change state** |
| `Sim daily chat used` → type a question → **Send** | composer + Send **enabled**; **UP-2** appears; **the typed question is still in the box** |
| Workspace → **New project** (Free, 1 active) | button **enabled**; **UP-3** — *"Free includes 1 active project — Basic gives you 3"* — with **upgrade · archive DevNorth** (reversible) |
| Export → **Export link** (on Free) | button **enabled** (Slice 9 shipped it `disabled`); **UP-EXPORT** appears with **Export as PDF instead** offered first |
| `Sim seat cap reached` → Share → invite a new Collaborator | Invite button **enabled**; the dialog shows the **TIER-named** prompt with **Add as Viewer — no seat** and **Basic gives you 10 seats — compare** |
| Any of the above | **assert: none of these controls is `disabled` or hidden** (`window._S10.d138 === true`) |

## S10-3 — The seat-cap correction (Slice 9 blocked; Slice 10 prompts)
1. `Sim seat cap reached` → Share → type a brand-new email → role **Collaborator** → **Invite**.
2. **Expect:** the add is *attempted*, then gated; the dialog names the **TIER** limit (never the phase limit), states **nobody has been removed** (D132), and offers the **free** remedy **first** (Viewer, no seat, unlimited) and the paid one second.
3. Click **Add … as a Viewer** → **it works**, no seat consumed, no invite spent.
4. Probe: `checkAdmission('anyone@x.com','Viewer').tier` → **false** at any seat count (**X-1 — Viewers are unlimited**).

## S10-4 — Guards: never before first value, never mid-pass
1. Reset the demo (clear `localStorage`) → **before** the first MRI, force a cap and attempt it.
2. **Expect: no prompt at all** (`fireUP()` returns `false`; nothing renders).
3. During the Extended Analysis (`_S10_deepInFlight === true`), attempt a capped action.
4. **Expect: no prompt** — an analysis is never interrupted.
5. After the MRI lands: **UP-8** arrives in chat — a celebration, **no ask**, once ever.

## S10-5 — Deep runs: gated for the user, NEVER for evidence (CR-2)
1. `Sim deep runs used` (2/2 on Free).
2. **Apply this fix** → **the fix is applied and saved**; the analysis update **defers**; History records *"Analysis update deferred"*; the read stays at **last-good**; **UP-5** offers **keep the last analysis**.
3. Now `Sim reviewer response`.
4. **Expect: the Extended Analysis runs immediately** — at the cap, on Free, with zero invites left. It is **counted in the evidence lane** and **never blocked**. (`_deepAllowed('evidence') === true`, always.)

## S10-6 — CR-2 end to end (the regression guard that matters most)
1. `Sim allocation spent` (0 invites left) → open an issue → **Share for review** → type an address that has **never** been seen.
2. **Expect: the request sends.** No invite spent, no seat taken, no tier check. The reviewer gets a scoped ReviewGrant.
3. **Expect:** the typed email **survives** (the Slice-9 keystroke-wipe bug is fixed).

## S10-7 — UP-4: one surface, **ratified** envelope *(AMENDED)*
1. `Sim oversized project`.
2. **Expect:** the Overview shows **one** notice: *"OSLO did not read all of your plan… every number on this page describes only the part it saw… there may be issues in the unread portion, and OSLO cannot tell you what they are."*
3. **Expect (AMENDED):** the notice names the **ratified** envelope — Free **~20 documents / ~50k words** — states that the project was **not rejected** (graceful degradation, §4b), and the Basic note (**~40 / ~100k**, **$12/mo**) lives **inside the same notice**. ~~*the size renders unset; "~100k words" never appears*~~.
4. **Expect: no second modal opens** (`_upIsOpen() === false`).

## S10-8 — UP-6: the gate that blocks nothing
1. `Sim monthly budget gate`.
2. **Expect (AMENDED):** the gate is **REAL and ENFORCED** at the **monthly token governor** (Free **4M** · Basic **10M** — §4c). UP-6 shows the real number and the real reset date, names Basic (**$12/mo**), and — on Free — states there is **no purchase path** but the upgrade (DL-074 §3). ~~*the threshold UNSET… "OSLO is enforcing nothing here."*~~
3. **Then:** with the governor gated, have a reviewer respond (`simReviewerResponse()`). **Expect: the evidence is RECORDED (CR-2 — never refused), and the RUN defers**, disclosed honestly: *"…recorded. Your read will update when your monthly analysis budget resets, or on upgrade."* `window._S10.cr2 === true`.

## S10-9 — No wallpaper, no generic upgrade
1. Walk every screen.
2. **Expect:** the sidebar plan chip reads **"Your plan"** (never "Upgrade"); no standing upgrade badge anywhere.
3. `window._S10.mon04 === true` — every prompt names its specific limit **and** its specific tier.

## S10-10 — Unset renders unset
1. Open **Usage & limits**.
2. **Expect (AMENDED):** **46 rows ratified** (hover = the canon citation) · **3 rows `recommendation — not ratified`** (seats ×2, CR-2-vs-governor) · **4 rows unset** (coalescing window · Free CRR cap · global prompt cap · billing rail), tinted, with **no number**. ~~*21 ratified / 11 unset*~~.
3. **AMENDED —** open **Plans** → the Basic price reads **$12/mo** (ratified), and the full ladder is shown (Pro ~$39 · Team ~$99–149/seat · Enterprise custom) **with no Buy button on the forward tiers**. **No `owner-TBD` token appears anywhere on the Plans surface.** `window._S10.tbd === true` (the assertion now also fails on a *ratified* value rendered as unset). `window._S10.nofreebuy === true` · `window._S10.seats === true`.

## S10-11 — Chat explains, never acts
1. Hit a cap → ask *"which limit did I hit?"*
2. **Expect:** the exact limit, from live meters, with the real reset time; the **plan** vs **phase** distinction; and the closing line: *"I can't upgrade you, buy anything, or lift a limit."*
3. **AMENDED —** ask *"what does my plan include?"* → the **full ratified ladder** is quoted (price **$12**, projects, envelope, daily caps, the **monthly governor**), the value story is stated (*"Basic buys capacity, not a better answer"*), **seats are flagged as a recommendation**, and on Free chat says **there is nothing to buy but the upgrade**.

## S10-12 — The record is never metered (D128 P1)
1. Create many artifact versions; generate many History events.
2. **Expect:** no cap, no trim, no expiry, no tier check — on Free or Basic. `window._S10.record === true`.

---

## AMENDED 2026-07-11 — the new scenarios

## S10-13 — ⚠️ CR-2 UNDER THE BINDING GOVERNOR (the regression guard that matters most)
1. Deliver first value, then **Sim monthly budget gate** → the monthly token governor (Free **4M**) is spent to its ceiling. `_govGated() === true`.
2. Confirm the **user-initiated** deep path is gated: `_deepAllowed('user') === false`.
3. Ask a reviewer for their read; have them respond (`simReviewerResponse()`).
4. **Expect — ALL of it:**
   - The **evidence is RECORDED**: `_reviewById(id).response` exists, and a **`review_response`** History entry lands with *"Recorded as evidence — Attested by …"*. **It is never refused.** `_evidenceAccepted() === true`, `_deepAllowed('evidence') === true`.
   - The **run DEFERS**: a second History entry — *"Analysis update deferred — the monthly analysis budget is reached"* — and an on-screen notice: **"Priya's answer is recorded. Your read will update when your monthly analysis budget resets, or on upgrade."**
   - The notice is **labelled `recommendation — not ratified`** (canon has not decided CR-2-vs-governor).
   - The Overview still shows the **last completed analysis**, labelled as exactly that. **Nothing is faked.**
   - `window._S10.cr2 === true` — the CR-2 assertion **still passes under the gate**.

## S10-14 — There is NO Free purchase path (DL-074 §3)
1. On **Free**, reach the monthly governor.
2. **Expect:** the only path offered is **upgrade**. **No top-up, no credit pack, no per-analysis purchase, anywhere** — not in UP-6, not on the Plans surface, not in chat. The Free plans card says so in plain words.
3. `OVERAGE_ELIGIBLE.free === false` · `FREE_PURCHASE_PATH === false` · `window._S10.nofreebuy === true`.
4. On **Basic**, the same gate offers **metered overage** — *per Extended Analysis, against a spend cap you set, with threshold alerts* — and says **no silent overspend, no bill shock**.

## S10-15 — The seat cap renders as a RECOMMENDATION, not canon
1. Open **Usage & limits** → the **Collaborator seats** meter carries **`recommendation — not ratified`** (hover: §4c has no seat row below Team; Basic = 10 cannibalises a per-seat Team).
2. Open **Plans** → both the Free and Basic cards carry the same dashed *"this seat number is a recommendation"* token.
3. Open **Settings › Subscription** → the seats row says it plainly.
4. Ask chat *"what does my plan include?"* → *"The one number nobody has decided: collaborator seats."*
5. `window._S10.seats === true`. Re-mark either seat row `RATIFIED` in `TIER_DEFS` → **the assertion fails loudly**, naming the cannibalisation risk.

## S10-16 — The monthly governor is the binding gate, and the daily caps say so
1. Open **Usage & limits** → the **monthly analysis budget** meter is **first**, labelled **"the limit that actually gates"**, with the ratified number (Free **4M**) and a **real calendar-month reset date**.
2. The daily meters (fixes · chat · deep) are labelled **"A burst-smoother, not the gate (§4c)"**.
3. Hit the daily deep cap → **UP-5** names it **and** says the monthly budget is the real ceiling.
4. **Expect:** no countdown, no urgency colour, no "nearly full" pressure — on any meter.

## S10-17 — Basic sells capacity, not a better answer
1. Open **Plans** → the Basic card says, in the sell line: **"Basic sells CAPACITY — not a better answer… You get the same models Free gets… OSLO will not tell you Basic thinks better than Free."**
2. The **Pro** card names **model quality + execution & program support**; **Team/Enterprise** name **governance & portfolio, per seat**.
3. **Expect:** Pro/Team/Enterprise carry **real prices and NO Buy button** ("Nothing to buy — R1").
4. Upgrade to Basic → the History entry says *"What did not change: the models."*


---

# ⬛ E2E SCENARIOS ADDED BY DL-103 (2026-07-12)

**S10-DL103-A — chat is not a limit.** Send 50 messages on Free. → Nothing gates. No prompt. No counter turns red. The meter says **"uncapped."**

**S10-DL103-B — the one honest limit.** Open *Your plan → Usage & limits*. → The first meter is **Monthly analyses**, in **analyses**, marked **pending re-derivation**, with the arithmetic shown as *illustrative*. **No token figure appears anywhere.** Below it: **"Update now" — free, on every tier."**

**S10-DL103-C — the assisted-apply cap never hides a recommendation.** Click *Sim assisted-apply cap (demo threshold)* → open any issue → the **recommendation is fully visible** → click **Apply this fix** (still enabled) → **UP-APPLY** fires → its **first** resolution is **"Make the edit yourself — free, right now"**, which opens the artifact. Edit by hand → **the analysis still runs**.

**S10-DL103-D — Update now on Free.** On Free, click **Update now** in Usage & limits. → It runs. One analysis is spent against the monthly budget. History records: *"free on every tier… what Basic buys is not having to ask."*

**S10-DL103-E — ⚠️ SUPERSEDED by D143, then by D148–D154.** *(The six-card scaffold is deleted; so is the modal and the §1–§5 spine. See S10-M4-1…9 below.)*

**S10-DL103-F — the budget gate.** *Sim monthly analysis budget reached* → **UP-6** fires: *"You've reached this month's analyses"* — in analyses, with the honest note that **the number is pending re-derivation and is an artifact of an engine being fixed**. Then: chat still works · **Update now still offered** · a reviewer response is **still recorded immediately** (CR-2), with the re-read deferred.

**S10-DL103-G — downgrade.** Upgrade to Basic, then **Return to Free**. → History entry: *"we take back the pipes, never the read."* History, issues, artifacts, chat and the read are **all intact**. Nobody is evicted.

---

# REPORTING (M4) — **D148–D154 · REBUILT** · end-to-end scenarios

> ⚠️ **S10-M4-A…F (the D143–D147 scenarios) are SUPERSEDED.** The modal and the §1–§5 spine no longer exist.

**S10-M4-1 — it is a workspace, not a modal.** Sidebar → **Readout**. → **The view switches**, exactly like Overview or History: `#pane-reports` goes active, the sidebar item takes `aria-current="page"`, the crumb reads **Readout**. There is **no scrim, no dialog and no Esc-to-close**, because there is nothing to close. **Left:** the composer. **Right:** the memo, rendered as a document — a page with a byline, headings and a table.

**S10-M4-2 — read the memo as the sponsor.** → It is about **DevNorth 2026**, not about OSLO. Seven sections: summary (standalone) · what's changed since 5 July · key risks · key assumptions · plan of action · decisions needed from you · appendix. **Search it for the word *confidence*, *reliability*, *artifact*, *issue* or *OSLO*. There are none.** The honesty is in the sentences instead: *"a 500-device figure that **came from our own plan, not from The Grid**"* · *"dates without owners are estimates, not commitments"* · *"the weak point here is people, not process."*

**S10-M4-3 — two altitudes, and the line that must not be crossed.** Every risk carries **For the plan** (what breaks in the schedule/scope) and **For the goal** (*"As written, the plan rests that on a network nobody has confirmed… what the plan delivers is a day of talks — which is a different event from the one we sold."*). → **Structural claims about the plan.** Nowhere does it say what will happen. Type *"likely"* into a section and the boot guard fails the build.

**S10-M4-4 — the plan of action is the PM's.** → First person: *"I'm getting the network commitment out of The Grid in writing this week… **I'm driving all of these.** Back to you Friday."* Hit **Edit** on it, rewrite it, save. → **It goes out exactly as written.** OSLO is never named in that section.

**S10-M4-5 — editing is free (D154).** On **Free**, hover any section → **Edit** → rewrite → **Save**. → It lands in the document. **No prompt fires. No tier is checked.** The composer says so out loud: *"We will never sell you the ability to correct words that go out under your name."*

**S10-M4-6 — the gate is reuse.** Still on **Free**, click **Next week (demo)**. → The report re-seeds and **your wording is gone** — nothing was ever kept. The prompt that fires sells **persistence**: *"Basic remembers your readout so you don't rebuild it every week"*, and its first resolution is free (*write it again, now*). Switch to **Basic**, edit, **Next week** → **your wording comes back, applied** — while the numbers underneath are re-read from the **current** plan. **Basic remembers your words. It never remembers a stale read.**

**S10-M4-7 — tailor the ask, never the read.** Switch recipient Sponsor → Executive / board. → **Only section 6 changes.** The summary, the risks and the assumptions are byte-identical. Section 6 for the sponsor asks for the contingency budget and the lead definition; for the board it asks whether in-person-only stays a hard constraint. **One honest read. Many asks.**

**S10-M4-8 — what travels.** Export PDF. → A **dated snapshot**, wrapped in a **cover** that carries the mark, the analysis-currency marker and **the disclaimer**. The **memo body carries neither a disclaimer nor a meta-paragraph** — only the plain byline *"DevNorth 2026 · plan as of 12 July · ‹name›"*. **No analysis ran.** The meter, the governor and the trend are untouched.

**S10-M4-9 — the schedule never lies.** Turn scheduling on (Basic) → *Fire the schedule now* while the read is stale. → The package goes out **labelled "previous analysis"** and says so on its face. It is **not** refreshed to look current.

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157 · D158**

| # | Scenario | Steps | Expected |
|---|---|---|---|
| **T10-E-30** | **D158 — a Basic user boots cleanly.** | `localStorage['oslo-s1-tier'] = '"basic"'` → reload (pristine). | **ZERO console errors.** `window._S10` → **39 assertions, all `true`** — including `mon04`. *(Before the fix: `mon04:false` + a red MON-04 console error, because UP-6 correctly does not name "Basic" to a Basic user.)* |
| **T10-E-31** | **D158 — the guard still bites below the tier.** | On **Free**, replace any friction prompt's body with generic *"Upgrade now for more."* | `_assertNoGenericUpgradeCopy()` → **false**, naming the prompt. **The name requirement is gated by `_beneathTier()`, not removed.** |
| **T10-E-32** | **D155 — the note surfaces.** | Reports → Edit **Summary** → type *"We're 80% likely to hit 450, and the venue call is on track."* → Save. | A `.m-note` appears **beside** that section: *"Heads up — this reads as a forecast…"*, listing the matched words (*likely · on track*). **No console error.** The note appears **only** on `data-pm="1"` sections. |
| **T10-E-33** | **D155 — the note NEVER blocks.** | With the note live, click **Export (PDF)**. | **A snapshot is produced.** `REPORT_SNAPSHOTS.length` increments. **No send/export control is disabled.** `_assertForecastNoteNeverBlocks()` → `true`. |
| **T10-E-34** | **D155 — OSLO never rewrites.** | Inspect the rendered `[data-sec="summary"][data-pm="1"]`. | `section.innerHTML` contains `RPT_EDITS['summary']` **verbatim, byte for byte**, and `RPT_EDITS['summary']` is **unchanged** by the render. `_assertOsloNeverRewritesPMProse()` → `true`. |
| **T10-E-35** | **D155 — dismissible, and it sends.** | Click **Dismiss** → Export. | The note disappears. **The PM's text is untouched.** Export succeeds. Re-edit that section → **the note comes back** (new words, fresh advice). |
| **T10-E-36** | **D155 — the PM's prose never turns the console red.** | Type *"probability of success"* into the PM's own Summary. | **Advisory only.** `_assertNoOsloVocabularyInReport()` · `_assertNoForecastLanguageInReport()` · `_assertDisclaimerOnPackageNotInBody()` → **all `true`**. **OSLO grades its own writing, never the user's.** |
| **T10-E-37** | **D149/D151 still bind OSLO.** | Read the OSLO-authored sections (summary · changes · risks · assumptions · decisions · appendix) before any edit. | **Zero OSLO vocabulary. Zero forecast language.** Both guards `true`. Two altitudes on every risk; the goal altitude is a **structural claim about the plan**, never a prediction. |
| **T10-E-38** | **D156 — the `To:` line.** | Switch recipient across all of `REPORT_RECIPIENTS`. | The **`To:` line changes**; **§1–§4 (+ §5 + appendix) are byte-identical**; **only §6 varies**. `_assertAskTailoredNeverTheRead()` → `true`. |
| **T10-E-39** | **D157 — length.** | Read §3 and §7. | **≤ 5 risks**, highest impact first. The appendix opens *"For the leads — skip this if you are not one"* and walks **every** workstream. The composer carries the **open item**: *what gets cut, and who decides — M4 spec, not invented here.* |
| **T10-E-40** | **D154 — editing still free on every tier.** | On Free **and** Basic: edit any section. | Always allowed. `_reportEditAllowed()` → `true` on both. `_assertEditFreeOnEveryTier()` → `true`. **The gate is REUSE** — only persistence is tier-keyed. |


---

## T10-E-38 — **D167: the request stays visible in the opening turn**
1. Land on the app. Ask OSLO about **ISS-01** (an issue with an outstanding clarification).
2. **Expect:** the opening turn carries a **collapsed** one-line prompt — `❓ Has the venue confirmed Wi-Fi for 500+ concurrent… ▸` — with `getComputedStyle(.cc-body).display === 'none'`. **No open textarea.**
3. Click the head → it expands to the **full question** plus the input. `window._S10.chatOpeningCarriesAsk === true` · `window._S10.chatClarCollapsed === true`.
4. The **"Answer your question" chip is still in the handoff** — it is a shortcut, not the only door.
5. Answer it in chat → the History entry is **byte-identical** to the Issue-panel path (`chatClarSamePath`).

## T10-E-39 — **D167: the chat word budgets**
1. `window._S10.chatOpeningShort === true` — every issue's opening ≤ **50** words. **Measured 27–45.**
2. `window._S10.chatPullShort === true` — every pull turn ≤ **40** words. **Measured 20–36.**
3. **Repeat with prototype notes ON.** Both still `true` — **the notes rail is not product copy** and is not counted (D161).

## T10-E-40 — **D166: the guards bite** (the negative-control regime)
For each guard, inject the regression it exists to catch and assert it goes **red**. **53 controls; all bite.** The four
that did **not** — `d138` (the validation exemption swallowed the subject) · `noteNeverBlocks` (graded a closed drawer) ·
`budgetInAnalyses` (graded an absent `#meterBox`) · the shared copy scanner (silent coverage rot) — **were vacuous, and
are fixed.** One control is a deliberate **non-bite**: the Invite button disabled on an **empty** address is *validation,
not a limit*, and the guard must not fire.

---

# D170 / D170c / D171 — SCENARIOS

| # | Scenario | Expected | Verified |
|---|---|---|---|
| **S-D170-1** | ⛔ **THE P1.** Free · Format = *Export link* · Export. | The **UP-EXPORT prompt renders**: eyebrow *"Limit — Export formats"* · title *"Free exports as PDF"* · **2 resolutions**. | ✅ |
| **S-D170-2** | Do it **again**, same day. And again. | It renders **every time**. (It used to render **once**, then never — `cool:'day'` + a persisted prompt log.) | ✅ |
| **S-D170-3** | Free · toggle an extra section → then branding → then schedule. | **Three prompts, three times.** (Previously: the first fired, the rest were **silent**.) | ✅ |
| **S-D170-4** | `doExport('link')` **from inside the Export dialog**. | The prompt renders **on top of the dialog**, not behind it. | ✅ |
| **S-D170-5** | **Every** limit-bearing affordance, fired against a **saturated prompt log**. | **11/11 rows PASS** — a prompt renders, naming the limit, the tier that relieves it, and ≥1 resolution. | ✅ (table below) |
| **S-D170-6** | Free + **PDF** → Export. | It **exports**: a frozen memo is cut (`sent_via:'exported'`), History gains an event, **no prompt**, **no analysis**. | ✅ |
| **S-D170c-1** | Open each toolbar menu in turn. | Each is a **popover** (`position:fixed`), anchored, `aria-expanded=true`, **one open at a time**, and **the document does not move**. | ✅ |
| **S-D170c-2** | Esc · click-outside · Tab. | Closes · closes · **focus stays trapped** inside; focus returns to the anchor button. | ✅ |
| **S-D171-1** | **Free** · Send → *"Send to the sponsor"*. | A **frozen memo** (`sent_via:'shared'`), a History `share` event, a toast. **No prompt. No lock. No meter. No analysis.** | ✅ |
| **S-D171-2** | **Basic** · Send. | **Identical.** Sharing does not differ by tier. | ✅ |
| **S-D171-3** | History → click the **"Memo sent to …"** row. | Opens the **frozen memo**, read-only, on its cover, `data-via="shared"`. | ✅ |
| **S-D171-4** | History → click the **"Memo exported"** row. | Opens the **frozen memo**, read-only, `data-via="exported"`. **Same object, both roads.** | ✅ |
| **S-D171-5** | Send · then edit the report · then run a new analysis · then re-open the memo. | **Byte-identical.** Relabelled *"previous analysis."* **Never silently refreshed.** | ✅ (`_d169StateProof()`) |

## The affordance × prompt table (the D170b guard) — **every row must PASS**

| Affordance | Prompt | Renders | Names the limit | Names the relieving tier | Resolutions | |
|---|---|---|---|---|---|---|
| Export format — the readout toolbar (`genReport`) | UP-EXPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Export format — the Export dialog (`doExport`) | UP-EXPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — an extra section | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — your own branding | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — sending it on a schedule | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — keeping last week's wording | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Monthly analysis budget ("Update now") | UP-6 | ✅ | ✅ | ✅ | 2 | **PASS** |
| Assisted apply — the fix cap | UP-APPLY | ✅ | ✅ | ✅ | 2 | **PASS** |
| Active projects — the project cap | UP-3 | ✅ | ✅ | ✅ | 2 | **PASS** |
| Collaborator seats — the seat cap | UP-SEAT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Plan size envelope — partial analysis | UP-4 | ✅ | ✅ | ✅ | 2 | **PASS** |

---

# D172 — SCENARIOS

| # | Steps | Expected | Result |
|---|---|---|---|
| **S-D172-1** | **Free** · Send → *"Send to the sponsor"*, three times. | **Three frozen memos**, `sent_via:'shared'`, three scoped grants. **No prompt, no lock, no meter, no analysis.** The share is free and unlimited. | ✅ |
| **S-D172-2** | **Free** · Schedule → *"Schedule weekly"*. | **The schedule does NOT turn on.** A prompt renders: **"Basic sends it for you every Friday"** · limit *Sending it on a schedule* · **Basic** · two resolutions, **free first: _Send it now_**. | ✅ |
| **S-D172-3** | **Free** · after S-D172-2, send it manually. | **It sends.** Hitting the automation limit never disables the free primitive. | ✅ |
| **S-D172-4** | **Basic** · Schedule on → *Fire the schedule now (demo)*. | A frozen memo with `sent_via:'shared'` · a **scoped memo grant** · History: **"Scheduled memo sent to …"** (`type:'share'`, carrying the memo id) · **trend and governor unmoved** (no analysis). | ✅ |
| **S-D172-5** | Mark the read **stale**, then fire the schedule. | The memo goes out **labelled "previous analysis"** (`cover.currency`), and says so on its face. **Never passed off as current. No analysis was run to freshen it.** | ✅ |
| **S-D172-6** | History → click **"Scheduled memo sent to …"** — after editing the report. | Opens the **frozen memo**, **byte-identical** to what was sent. Nothing was re-run. | ✅ |
| **S-D172-7** | Notes ON · Send popover → *Open it as the recipient (demo)*. | The **grant landing**: *"Idris sent you the readout…"* · **one click, no password, no signup** · scope stated. Accept → the **read-only memo**, on its cover, with its disclaimer and currency marker. | ✅ |
| **S-D172-8** | Nav / crumb / toolbar. | Nav = **Reports** · crumb = **Reports** · the document's toolbar = **Readout**. Never swapped. | ✅ |
| **S-D172-9** | Look for a report-type picker. | **There isn't one.** One type in the registry (`readout`); no cards, no gallery, no chooser. **D143 holds.** | ✅ |

### Reports surface — Strategic Readout (WI-R1)

| ID | Steps | Expected | Status |
|----|-------|----------|--------|
| **S-WIR1-1** | Open **Export a snapshot**. Read the composer. Capture §1/§2/§3/§5 text. Switch across all four recipients **Sponsor → Programme lead → Operations → Executive-board** (WI-R2 — the shared `REPORT_RECIPIENTS` model). | The five-section spine renders (§1–§5). **§1/§2/§3/§5 are byte-identical across all four recipients**; **only §4 (the ask) changes**. The `.sro-bind` banner states the rule and cites **DL-108**. *(Proven headless: `readIdenticalAcrossAudience` ✅; §1/§2/§3/§5 identical across all four recipients; §4 distinct across all six pairs.)* | ✅ |
| **S-WIR1-2** | Inspect §1 and §5; check the audience never touches the read; check the epistemic markers. | §1 says the read is **understanding maturity — not project health / RAG / readiness / probability of success**. §5 carries reliability, the **currency marker** (stale ⇒ **"previous analysis"**) and the **derived (`From OSLO`) vs attested (`Confirmed by you`)** rule — derived never dressed as attested (**DL-104 P1**). | ✅ |
| **S-WIR1-3** | Toggle all four optional sections; then generate a snapshot. Watch `HISTORY`/`TREND` and the boot self-check. | Optional sections (Alignment · Unvalidated assumptions · How understanding matured · Artifact detail) render as **presentation only** (no assumption lifecycle). Generating **runs no analysis** — `HISTORY`/`TREND` unchanged (`readoutRunsNoAnalysis` ✅). Boot self-check **60/60 green**; the seven-section Readout document unchanged. | ✅ |

### Overview layout — D179

| ID | Steps | Expected | Status |
|----|-------|----------|--------|
| **S-D179-1** | Load the app. Look at the Overview, top to bottom. | **Confidence is the first panel.** Ramp · band word (**cool accent, not orange**) · *"on moderate reliability"* · *"Feasibility is holding it back."* · the small 0–100 index. **No "What changed" panel anywhere** — nothing has changed yet. Then **Start here**, then **Progress**: `Issues 6 · Critical 1 · Open questions 2 · Confirmed artifacts 0 / 7` — **no arrows** (there is no previous run to compute a delta against). | ✅ |
| **S-D179-2** | Run **Extended Analysis**. Watch the Overview. | **The Confidence card does not move.** A strip appears **inside it, under the read**: **WHAT CHANGED ✕ · "Extended Analysis landed." · "I looked deeper: found two more, and one more question. The read is firmer."** — **19 words.** | ✅ |
| **S-D179-3** | Look at the **Feasibility** row. | **⟨Very Low⟩ ⟶ [Low]** — the previous band **ghosted**, the current **lit**, an **arrow** between them. **Zero reading.** | ✅ |
| **S-D179-4** | Look at the **hero** ramp. | **No ghost.** The overall band **held at Moderate**, and OSLO does not draw a movement that did not happen. | ✅ |
| **S-D179-5** | Look at **Progress**. | `Issues **8** ↑2 · Critical **2** ↑1 · Open questions **3** ↑1 · Confirmed artifacts **0 / 7**`. **MORE ISSUES *AND* A HIGHER BAND** — and the page says both, once each, without arguing with itself. | ✅ |
| **S-D179-6** | Hunt for a duplicated number anywhere on the Overview. | **There isn't one.** No count in the confidence footer, none in the clarification pointer, none in *"See all open issues"*, none in the payoff. **Counts have one home.** | ✅ `_assertNoCountIsRenderedTwice()` |
| **S-D179-7** | Dismiss the payoff (**✕**). | The strip goes **and the ghost/arrow go with it.** The **read is untouched** — ramp, band, qualifier, limiter, index. The **Progress deltas stay** (*"since the last run"*). | ✅ |
| **S-D179-8** | Reload. | **The payoff does not come back.** The state does. | ✅ |
| **S-D179-9** | Apply a fix, or answer a clarification. | The strip returns with **its own** act line (*"You applied OSLO's fix to Resources."*), the **Feasibility ramp** draws the movement, and **Progress re-derives every delta against that run's baseline** (`Issues 5 ↓1 · Critical 0 ↓1 · Open questions 1 ↓1 · Confirmed artifacts 1 / 7 ↑1`). | ✅ |
| **S-D179-10** | Look for **orange** on the confidence card. | Only on the **links** (*Why ▾ · Timeline → · Attention map →*). **Never on the ramp, the band word, the limiter or the chip.** Those wear the **cool accent**. | ✅ |
| **S-D179-11** | Switch to **light theme**. Repeat S-D179-1 → S-D179-10. | Identical behaviour; the cool accent is `#3F6193`; **every accented element clears AA**. | ✅ |
| **S-D179-12** | Open the **Attention map**. | **Untouched.** Severity colour (red/amber) still on the heat cells — **those cells *are* issues** (D003). | ✅ |


---

# D180 — Progress (grounding, not clearing) — E2E

| # | Scenario | Steps | Expected |
|---|---|---|---|
| **T-D180-1** | **The star rises when the user grounds an artifact.** | Overview → open the top clarification → answer it → wait for the analysis update. | Progress: **GROUNDED 0 → 1 ↑1** · CLOSED: **Issues resolved 0 → 1 ↑1 · Questions answered 0 → 1 ↑1** · OPEN falls. **No bar, no %, no "remaining".** |
| **T-D180-2** | **Progress goes UP while issues go UP.** | Run the **Extended Analysis** pass. | OPEN: **Issues 6 → 8 ↑2 · Critical 1 → 2 ↑1 · Open questions 2 → 3 ↑1**, and the read **firms** (Feasibility Very Low → Low). **Both arrows are drawn identically. Nothing says "worse".** |
| **T-D180-3** | **Then ground an artifact on top of the deeper read.** | After the Extended pass, **Apply this fix** on the critical Resources issue. | **GROUNDED 0 → 1 ↑1** while the issue count is still **elevated** from the deeper read. **That is the doctrine, on screen, in one panel.** |
| **T-D180-4** | **The counts have one home.** | Read the whole Overview. | Every count appears **exactly once** — in Progress. The confidence card **points**; it does not tally. |
| **T-D180-5** | **No constant.** | Search the Overview for a number that cannot move. | None. *"Artifacts read 7/7"* does not exist. |

## DL-109 — the provenance surfaces

| # | Scenario | Steps | Expected |
|---|---|---|---|
| **T-DL109-1** | **The claim-level grounded facts (DL-111 foundation bar, erratum).** | Overview → Progress. | The **hero** = **17 of 28** — the grounded numerator is **attested claims only** (*Confirmed by you*), computed, **never** grounded + inferred; the **28** is the total-claims denominator (grounded + inferred), captioned *"grounded in your evidence / the rest of your read is OSLO's inference"* (WI-R6, variant B). The solid bar shows **two provenance states**: the grounded segment (cool accent, **label only**) and the inferred, **hatched** *From OSLO* **11** segment. **No percentage fill, no burndown; the denominator is a composition (grounded of total), not a target.** |
| **T-DL109-2** | ⭐ **The number.** | Overview → Progress, the load-bearing line below the bar. | ***"Your read leans on 12 inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →"*** — a **superset** of the 11 inferred *claims* in the bar, **never `+`-joined**. *See them →* opens the Inference map. **(D181a: (a) a critical issue cites it · (b) the limiting dimension rests on it · (c) ⭐ a strong-reading artifact's confidence rests on it — Scope.)** |
| **T-DL109-3** | **The user grounds an artifact.** | Open the critical Resources issue → **Apply this fix** → let the analysis update land. | **17 of 28 → 19 of 28 (grounded ↑2) · From OSLO (inferred claims) 11 → 9 ↓2 · leans on 12 → 7 ↓5** — the hero's numerator grows toward the fixed total, the inferred segment shrinks, the load-bearing superset falls. The plan is **grounded**, not paid down. *(Scope's four remain — Resources is not Scope.)* |
| **T-DL109-4** | ⛔ **A deeper read infers MORE, and that is not a regression.** | Run the **Extended Analysis** pass. | **I inferred 11 → 12 ↑1 · holding it up 12 → 20 ↑8**, *and* the band rises (Feasibility Very Low → Low). **Every arrow is drawn identically. Nothing says "worse".** |
| **T-DL109-5** | ⭐ **The Inference map names the artifact to verify.** | Nav → **Inference map**. | ***"Scope reads strong, and most of it is mine — 4 of its 7 items are inference. Worth verifying first."*** → **Open Scope →**. Neutral chrome; no severity colour anywhere on the pane. |
| **T-DL109-6** | **The map counts; it does not fill.** | Inspect any row. | **One pip per extracted item**, grounded first. **No bar, no track, no percentage.** *Resources: 5 grounded · 10 inferred.* |
| **T-DL109-7** | **The flag is computed.** | Open **Scope** → edit any block (it becomes *Confirmed by you*) → return to the Inference map. | **The flag is gone.** So is the **Verify** tag on the Scope row. |
| **T-DL109-8** | **The assumption register.** | Inference map → **Assumptions**. | **Load-bearing first**, each row carrying its **age** and *"N issues depend on it"*, linked to the issue. |
| **T-DL109-9** | **The Readout reads the register.** | Reports → Readout → optional **Unvalidated assumptions** ON. | The **assumptions** appear (load-bearing tagged) — **not** the open clarifications. |
| **T-DL109-10** | **"What I'd need to be sure."** | Reports → Readout → §5. | The unbacked **load-bearing** items **as asks**: *"Confirm: … · If it is wrong: …"*. Identical for all four recipients. |
| **T-DL109-11** | ⛔ **No debt vocabulary.** | Read every surface. | Nothing is *owed*, *outstanding as debt*, a *liability*, or something to *pay down*. |

## D181 — the read points at it · the clock ages, the past does not

| # | Scenario | Steps | Expected |
|---|---|---|---|
| **T-D181-1** | ⭐⭐ **SCOPE IS IN THE NUMBER.** | Inference map → the flag names **Scope** → Overview → Progress. | **The 12 includes Scope's four inferences** (CI-20 · CI-21 · CI-22 · CI-23). **Scope has no critical issue open and is not the limiting dimension — clause (c) catches it.** *A strong-looking artifact that is mostly inferred is the most dangerous thing in the plan.* |
| **T-D181-2** | **An inference nothing points at is not counted.** | Compare the count (**12**) with the number of inferences bearing on Feasibility (**11**). | They are **not** the same set. **CI-45 · CI-56 · CI-57 bear on the limiter and nothing points at them — excluded.** |
| **T-D181-3** | ⛔⛔ **The user grounds the flagged artifact.** | Run the Extended pass (**holding it up → 20**) → open **Scope** → **Apply this fix** / confirm it. | **Holding it up → 12. The flag goes. The Verify tag goes.** **Nothing turns red, and no guard fails: the fall is the user's success.** |
| **T-D181-4** | ⭐ **Advance the clock.** | Reports → **Next week (demo)** ×3 → Inference map → **Assumptions**. | *"Unvalidated for **3 weeks** · 1 issue depends on it."* The timeline's Initial run reads **"3 weeks ago"**. **Nothing was back-dated — the clock moved.** |
| **T-D181-5** | **Velocity is a direction, not a target.** | After advancing a week with nothing done, read **This week**. | **you grounded 0 · I inferred 0.** *Understanding is stalling* — said honestly. **No total, no denominator, no zero to reach.** |
| **T-D181-6** | **First run is still first run.** | Fresh session (week 0) → History. | **Minimal first-run state, and the Initial run reads `now − 2m`** (D100). **The project genuinely is minutes old, and the register says so** (*"Unvalidated for 2 minutes"*). |


---

## D190 — the recommendation block, corrected (owner, 2026-07-13)

| ID | Step | Do | Expect |
|---|---|---|---|
| **T-D190-1** | **The affordance is short and constant.** | Open **any** issue with a recommendation. Then open the other five. | The fix is **resident above the button**, and the button reads **"Apply this fix"** — **the same six times, over six different fixes.** *(Ask OSLO "what would you do?" in chat: the reply's action reads **"Apply this fix →"** — the same string, one reader.)* |
| **T-D190-2** | ⛔ **And the consent rule still bites.** | *(Console, probe-fenced)* `_d184NegativeControls()`. | `aButtonWithNoSubjectSurvives_bites: true` — **blank the recommendation and the guard goes RED.** The fix is still readable **before** it is appliable (D184/D001). |
| **T-D190-3** | **The options open in ONE place — under the recommendation.** | Open an issue → click **"Other options (2)"**. | The options expand **in place, directly beneath the recommendation** (`#ipAlts`): the two alternatives (**Select** · **Discuss**), the **Selected option** chip once you choose, and **"✎ Write my own fix in Resources →"**. **Scroll down: there is NO "Other options" row under Evidence.** The rows are **Evidence · Clarification · Comments**. |
| **T-D190-4** | ⛔⛔ **The assisted-apply cap still cannot hide the fix — and the free door is still open.** | Click *Sim assisted-apply cap (demo threshold)* → open any issue → click **Apply this fix**. | The **recommendation stays fully visible** (it is not in a drawer at all) · **the options are FORCED open** and **cannot be collapsed** · **"✎ Write my own fix in \<document\>"** is on screen · **UP-APPLY** fires, and its **first** resolution is the free manual edit. **The analysis still runs on the manual edit.** *(Metering understanding is PROHIBITED — D126/D128.)* |
| **T-D190-5** | **"Path" is gone.** | Select an option → open **History**. | The entry reads **"Resolution option selected — …"** / *Option "…"*. Nothing in the product says *path* in this sense — panel, chat, review kinds, tour, tooltips. |

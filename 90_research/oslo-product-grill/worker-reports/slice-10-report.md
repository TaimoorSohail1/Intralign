# Slice 10 — Tiering & Limits · Worker Report  ·  **FINAL SLICE**

**Status: COMPLETE.** `vertical-slices/slice-10-tiering-limits/` — cumulative Slices 1–10 in one openable `prototype.html` (11,725 lines), 7 house docs + `edge-cases.md` + `open-items.md` + **`tier-definitions-census.md`**.

---

## 1. The governing rule was the deliverable

**Canon decides. The build adopts and cites. I invented no tier number.**

The Slice-9 build carried `BASIC_PROJECT_CAP = 10` — an **AI-proposed number that contradicts ratified canon**. **UP-3** says, in the product's own words: *"Free includes 1 active project — **Basic** gives you **3**."* That invented 10 reached an open PR and was withdrawn on the record (DL-102 Correction #3).

**Corrected:** `BASIC_PROJECT_CAP = 3`, cited to UP-3, with the withdrawal recorded at the code site. And the *mechanism* that let it survive is closed too: **every displayed tier number is now painted from its constant.** Slice 9 hard-coded `'10 projects · 10 seats'` in a copy string in `renderTierChrome` — a hard-coded string is how an invented number outlives its correction.

---

## 2. What I built

- **D134** — every ratified number adopted with a citation **at the site that consumes it**.
- **D135** — real simulated Free→Basic upgrade · **`BASIC_PRICE = null`** renders as an explicit owner-TBD · **Pro named as a forward capability with no price and no button** (a "coming soon" with a Buy attached is a pre-order).
- **D136** — *Usage & limits*: live counters (projects · fixes · chat · deep runs · seats · the **uncapped evidence lane**) with **real reset times** (calendar day; calendar month for the allocation). Unset values render **visibly unset**. **No countdown, no urgency colour, no red counter** anywhere.
- **D137** — the full **UP-1…UP-8** engine: one table, **one fire path**, the ratified copy, the ratified cadence, and **all four global guards** (never before first value · never mid-pass · per-trigger cooldown · global per-day cap).
- **D138** — the limit-reached rule at **every** cap: projects · fixes · chat · deep runs · **export** · **seats**. Controls stay enabled; the **attempt** is gated; every prompt carries **resolutions with the free one first**.
- **D139** — partial orientation + honest disclosure on **ONE surface**, envelope size **unset** ("~100k words" never appears).
- **D140** — `tier-definitions-census.md`, generated from the live registry, and rendered **in-product** so the user sees the holes too.
- **Chat** — explains a limit from live meters, and **refuses to upgrade, purchase or lift anything**, in that sentence, every time.

### Two Slice-9 corrections (both required by D138)
1. **Seats** — the seat cap **blocked** the add. It now **prompts**: control stays enabled → attempt → **tier-named** prompt → resolutions as **buttons**, free one first (**Add as Viewer — no seat, unlimited**).
2. **Export** — the non-PDF formats were `disabled` buttons. Canon forbids that outright. They are **live**; the attempt prompts.

### One removal
**The persistent "Upgrade" button in the sidebar is gone.** It stood on every screen in Slice 9 — the definition of the **upgrade wallpaper** MON-04 bans. It now reads **"Your plan"** and opens facts.

---

## 3. Verification (all mandatory items)

| # | Check | Result |
|---|---|---|
| 1 | `<script>` extract → `node --check` | **PASS** |
| 2 | jsdom parse **without** `runScripts` → body children | **31** (Slice 9: 29 + `#upScrim` + `#limitsScrim`) — healthy |
| 3 | Grep **D110–D140** | **all present** (D110 ×17 · D124 ×37 · D128 ×70 · D132 ×42 · D134 ×6 · D137 ×2 · D138 ×18 · D139 ×9 · D140 ×6 · CR-2 ×91 …) |
| 4 | **Non-regression** (Slices 1–9) | **24/24 PASS** — activation, intake, Fast Pass, Overview, Attention, Artifacts, Issues, History, Workspace, Settings, dark default (D127), Share, Export, comments, CRR, D132, D133 |
| 5 | **Behavioural** | **55/55 PASS**, 0 console errors |

### Behavioural detail (the six the brief named)
- **(a) Every capped affordance stays ENABLED** and the attempt yields a prompt with resolutions — **asserted against the real DOM**: 0 disabled, 0 hidden. Apply-fix ENABLED at the cap (plan untouched); chat send ENABLED (**the typed question is not destroyed**); 3/3 export buttons enabled; New-project enabled.
- **(b) The seat cap prompts, it does not block** — tier-named, resolutions as buttons, **Viewer offered first**; Viewers remain admissible at any seat count (X-1).
- **(c) No prompt before the first MRI** (verified: `fireUP` returns false, nothing renders) and **none during an active pass**.
- **(d) `BASIC_PRICE` / envelope / budget / gate / Basic-chat / Basic-deep / CRR cap / prompt cap all render UNSET** — never numeric. Asserted.
- **(e) No generic "upgrade" copy** — asserted across the whole prompt table: every friction prompt names its **specific limit** and its **specific tier**.
- **(f) CR-2 holds** — **0 invites + a brand-new reviewer → the review request still sends**; an evidence-driven Extended Analysis runs **even at the deep-run cap**.
- **(g) Artifacts uncapped, History never truncated** — asserted.

### Runtime assertions (they run at every boot; `window._S10`)
`_assertNoDisabledLimitAffordances` (D138) · `_assertNoGenericUpgradeCopy` (MON-04) · `_assertNoFabricatedNumbers` (Anti-Assumption) · `_assertRecordNeverMetered` (D128 P1) · `_assertEvidenceNeverGated` (CR-2) · `_assertViewersUnlimited` (X-1) · `_assertNoEvictionOnDowngrade` (D132). **All green.** They exist because a comment does not stop a future contributor — or a future model — from "just adding a tier check". An assertion does.

### A real bug found and fixed (not in scope; found by the harness)
Typing a **brand-new reviewer's email** into the CRR dialog **wiped the input on every keystroke** (`renderCrr` rebuilt `#crrEmail` on each `oninput`). Picking an existing teammate from the chips worked, so it survived Slice 9. It broke **precisely the path CR-2 exists to protect** — asking someone who has never used OSLO for their read. **Fixed** (value + caret preserved).

---

## 4. The census — the real deliverable

**`vertical-slices/slice-10-tiering-limits/tier-definitions-census.md`**

| | |
|---|---|
| Values the product consumes | **32** |
| ✅ **RATIFIED** (adopted + cited) | **21** |
| ⬜ **UNSET** (owner decision required) | **11** |

**11 of the 32 numbers this product needs have never been decided. None is invented in the build; all 11 render visibly unset, in-product, to the user.**

The 11: Basic **price** · **billing rail** · Basic **daily chat** · Basic **deep-runs/day** · Free + Basic **monthly Extended-Analysis budget** · the **UP-6 gate threshold** · Free + Basic **size envelope** · Free **CRR cap** · the **global prompt cap/day**.

This is the evidence-based table of contents for **`RELEASE_1_TIER_DEFINITIONS_V1`** — cited as authoritative by **18 canonical documents**, never written, and escalated in **DL-102 Concern 7** as a **blocking prerequisite for shipping Basic in Alpha**. It proposes **no number**. It is a **commissioning brief**.

---

## 5. NEW canon tensions — **escalated, not invented**

**T10-1 — Two ratified sources disagree on Basic's project cap.** **UP-3 = 3.** **D129 T-1 = 10.** The build follows canon (**3**, per D134). **But D129 T-1 still says 10 on the record.** The Tier Definitions doc must state which governs, and **D129 T-1 should be corrected** if UP-3 stands. *(The seat caps 3/10 are a different number and are not in conflict — only the project cap "10" is withdrawn.)*

**T10-2 — UP-5 presumes an affordance D006 forbids.** UP-5 gates *"Analyze / trigger reanalysis (Project Overview)"*, but **D006 ratifies event-driven reanalysis only — there is no manual re-analyze control.** So the deep-run cap has no affordance of its own. The build gates **user-initiated triggers** (Apply this fix → the edit **saves**, the **re-read** defers, last-good stands — UP-5's own "keep last analysis" resolution) and **never** gates an **evidence** run (CR-2). A clarification answer is counted, not gated (the user is supplying evidence; canon does not name it). **Owner: which triggers does the cap attach to?**

**T10-3 — Two caps D138 governs have no slot in the UP-1…UP-8 taxonomy.** **Seats** and **export formats** have no UP-number in canon. Built as `UP-SEAT` / `UP-EXPORT`, following the ratified standing rule exactly. **I did not assign them canon numbers.** **Owner: give them slots, or state the rule applies without one.**

**T10-4 — MON-04 requires a global per-day prompt cap and never sets it.** The build enforces the **guard**, renders the **number** unset, and errs toward **silence**. **Owner: set it, or ratify "err toward silence".**

---

## 6. What I refused to do

I proposed **zero** tier numbers. Where canon decided, I cited it. Where canon did not, the product **says so, to the user**, and I escalated it. The **UP-6 monthly-budget gate** is the sharpest expression of that discipline: canon ratifies the trigger and its copy but never the threshold — so the gate **fires and enforces nothing**, and tells the user *"OSLO is enforcing nothing here… you are not being asked to buy your way out of a number that does not exist."* Inventing that threshold would have been a two-character change and fabricated scarcity. It is the shape of the mistake that produced "Basic = 10 projects", and it is exactly the mistake this slice existed to not repeat.

---
---

# ⚠️ AMENDMENT — 2026-07-11 · The tier-numbers correction

## 0. The headline, stated against myself

**The previous section of this report is wrong in its central claim.** I wrote that the discipline of Slice 10 was *"where canon did not decide, the product says so."* **Canon had decided.** I could not find the decisions because I scanned the zones the product-grill discipline scopes to — `10_product/` and `00_owner/` — and **the full tier ladder lives in the engineering zone:**

> **`30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1` — §4c** (Cost Governance / Freemium Unit Economics), with **owner-confirmed rows for every tier**. Free/Basic confirmed **2026-06-05**; Pro/Team/Enterprise ratified via **DL-074** (2026-06-19).

So the "sharpest expression of the discipline" I was proudest of — **UP-6 firing and enforcing nothing** — was not discipline. **It was blindness dressed as rigour.** The threshold existed. §4c names it, in those words, **"the binding governor."**

**Crying "unset" over a number the owner decided months ago is the same lie as inventing one — told backwards.** And it is arguably worse, because it teaches every future reader that the number does not exist. That failure is now **asserted against in code**, in both directions.

## 1. What was ratified all along (and rendered as owner-TBD)

| Rendered as | Actually (citation) |
|---|---|
| Basic price — *"owner-TBD (T-3)"* | **$12/mo** — §4c, owner-confirmed 2026-06-05; DL-074 §4 |
| Basic chat/day — *"UNSET"* | **75/day** — §4c |
| Basic deep runs/day — *"UNSET"* | **6/day** — §4c, and explicitly a **burst ceiling, NOT the governor** |
| Size envelope — *"UP-4's ~100k words is illustrative"* | **Free ~20 docs / ~50k words · Basic ~40 / ~100k** — §4b (CHG-056) + §4c. The "~100k" is **Basic's envelope**. |
| UP-6 gate — *"threshold never decided; enforces nothing"* | **The monthly token governor** — Free **4M** · Basic **10M**. §4c: *"the binding governor."* |

And the mirror error: **the collaborator seat caps were marked RATIFIED. They are not.**

## 2. What changed in `prototype.html` (amended in place)

1. **`BASIC_PRICE = 12`** (was `null`). D129 T-3 is **superseded by the owner having set the price**. Painted from the constant at every CTA; no `owner-TBD` token remains on any pricing surface.
2. **Basic chat = 75/day · deep runs = 6/day** — wired and enforced, cited to §4c.
3. **The project-size envelope is ratified and wired** (`ENVELOPE`). The UP-4 partial-orientation disclosure now names the real size **and** the ratified graceful-degradation fact (*the project is never rejected*).
4. **The monthly token governor is implemented as the binding gate** (`TOKEN_GOVERNOR`, `_govSpend`, `_govGated`), with a **visible meter** at the top of Usage & limits, a **real calendar-month reset date**, and the daily caps re-labelled **burst-smoothers, not the gate** (DL-074 §5: visible meter · user-set spend cap · threshold alerts · no silent overspend · no bill shock). UP-6 now **enforces a real, ratified threshold**.
5. **The plans surface shows the full 5-tier ladder** — Free · Basic **$12** · Pro **~$39** · Team **~$99–149/seat** · Enterprise **custom**. Basic purchasable in Alpha; **Pro/Team/Enterprise are the forward ladder — priced, and NOT purchasable in R1, with no Buy button on any of them.** The value story is stated, not implied: **Basic = capacity** (the same models as Free — the product says so) · **Pro = model quality + execution & program support** · **Team/Enterprise = governance & portfolio, per seat**. *Basic + Pro is the individual motion; Team + Enterprise is the org sale.*
6. **Overage (DL-074, ratified):** paid tiers get metered **per-Deep-Pass** overage with a **user-set spend cap** and **threshold alerts**. **Free has NO purchase path** — `FREE_PURCHASE_PATH = false`, `OVERAGE_ELIGIBLE.free = false`, and a new assertion `_assertNoFreePurchasePath()` fails loudly if anyone ever builds one.
7. **Seat caps render as `recommendation — not ratified`** — on the meter, on both plans cards, in Settings, and in chat. **I did not invent a replacement number.** New assertion `_assertSeatCapsFlagged()`.
8. **Still genuinely unset, still rendering unset:** OD-10 coalescing window · Free CRR cap · MON-04 global prompt cap/day · billing rail.
9. **CR-2 vs the governor** — implemented as the **labelled recommendation**: `_deferEvidenceRun()`. The reviewer's attestation is appended **before any budget check is reached**; the **run** defers with the honest line. New status `RECOMMENDATION` added to the census registry, and a third in-product mark (`_recSpan`) to render it.
10. **`_assertNoFabricatedNumbers()` now asserts in BOTH directions** — it fails on an invented number *and* on a **ratified value rendering as unset**.

## 3. Verification (all run against the amended file)

| Check | Result |
|---|---|
| `node --check` on the extracted `<script>` | **PASS** |
| jsdom **without** `runScripts` → body child count | **31** — unchanged from the prior baseline |
| Boot assertions (`window._S10`) | **8/8 PASS** — `d138 · mon04 · tbd · record · cr2 · nofreebuy · seats · viewers` (two are new) |
| Console errors on boot | **0** |
| (a) Basic price renders **$12**, not TBD | **PASS** — `BASIC_PRICE === 12`; no `owner-TBD` token anywhere on the Plans surface |
| (b) Basic chat **75** / deep runs **6** wired | **PASS** — `_limit('chat')===75`, `_limit('deep')===6` on Basic |
| (c) The monthly governor is the binding gate and is visible | **PASS** — governor meter renders first, labelled *"the limit that actually gates"*; `_govGated()` blocks user-initiated deep runs |
| (d) **No Free purchase/overage path exists** | **PASS** — `_assertNoFreePurchasePath() === true` |
| (e) Seat caps render as **recommendation-pending-ratification** | **PASS** — `_assertSeatCapsFlagged() === true`; both rows `status:'RECOMMENDATION'` |
| (f) Genuinely-unset values still render unset | **PASS** — `coalesce.window · crr.cap · prompt.globalcap · billing` all `val: null` |
| (g) **CR-2 holds under the gate** | **PASS** — with the governor at its ceiling, a reviewer response is **recorded** (attestation + History entry), the **run defers** with the honest disclosure, and `_assertEvidenceNeverGated()` still returns `true`. **Evidence is never refused.** |
| (h) No invented numbers anywhere | **PASS** — every displayed number painted from its constant, with its §4c/DL-074 citation in a comment at the site |
| (i) Slices 1–9 non-regression | **PASS** — 21-call smoke across every render/open/close/sim path; 0 errors |

## 4. Corrected census counts

~~**32 values · 21 RATIFIED · 11 UNSET.**~~

> **53 values · 46 RATIFIED · 3 RECOMMENDATION · 4 UNSET → 6 genuinely open decisions:**
> **collaborator seats (Free/Basic/Pro)** · **OD-10 coalescing window** · **Free CRR cap** · **MON-04 global prompt cap/day** · **CR-2-vs-governor behaviour** · **billing rail**.

**And the root cause, now stated prominently in the census:** the tier values live in the **engineering zone** while **18 product documents cite a "Release 1 Tier Definitions" that does not exist**. **The gap is not missing values — it is a missing product-authoritative surface that consolidates and names them.** `RELEASE_1_TIER_DEFINITIONS_V1` must be commissioned as a **consolidating, citing** surface, not as a document that decides anything new.

## 5. NEW tensions — escalated, not invented

- **T10-5 — the seat caps are not canon, and Basic = 10 cannibalises Team.** §4c sets no seat row below Team; Team is priced **per seat** (~$99–149). A $12/mo Basic granting **ten** seats means a ten-person team buys **one Basic** instead of Team. **CHG-061 is not at risk either way** — the viral primitives run on **unlimited Viewers** and **free, unmetered Reviewers**, and **neither consumes a seat**. **The number is the owner's; the constraint is structural. No replacement invented.**
- **T10-6 — CR-2 vs the binding governor.** CR-2 (evidence never refused) · CRR-04 (every response triggers a run) · §4c (the rollup gates AI spend) collide, and canon never reconciled them. Implemented as **record · defer · disclose**, labelled in-product as a recommendation.
- **T10-7 — `RELEASE_1_TIER_DEFINITIONS_V1` is a SURFACE problem, not a DECISION problem.** Commissioning it as a *decision* document invites a second round of invented numbers. It must **consolidate and cite** §4c + DL-074 + the backlog ladder + the UP-* table, leaving only the six open items.
- **Withdrawn:** ~~T10-1 (canon conflict on Basic's project cap)~~ — §4c and UP-3 **agree on 3**; the "10" was our own. ~~T10-2 (UP-5 has no affordance)~~ — largely dissolves once OD-10 is settled with the canonical manual trigger.

## 6. What I refused to do — restated, and it now means something different

I still proposed **zero** tier numbers. But the discipline that mattered this time was not *"refuse to invent"* — it was **"go and find out."** The seat cap is the one place I held the line correctly: it is genuinely undecided, it is commercially load-bearing, and **I did not pick a number to make the build look finished.** Everywhere else, the honest thing was not to say *"nobody has decided"* — it was to **read the engineering zone and adopt what the owner had already ratified.**

**A hole you cannot find is worse than a hole you can.** That is the finding, and it is bigger than Slice 10.

---

# ⬛ PASS 3 — **DL-103 FOLDED IN (Ratified 2026-07-12)**

`00_owner/decisions/records/DL-103-analysis-cost-basis-and-tier-rederivation.md` — Class A, Ratified. It supersedes most of what Pass 2 "corrected."

## 1. The finding that reframes both previous passes

Pass 1 said: *"the tier numbers are not in canon — render them unset."*
Pass 2 said: *"wrong — they were in the ENGINEERING zone (§4c) all along; adopt and cite them."*
**DL-103 says: the numbers we finally found are derived from a cost basis canon had already abandoned.**

- **§4c (2026-06-05)** and **DL-074 (2026-06-19)** derive every governor, price and the ~$3/mo Free ceiling from **rented frontier-model pricing**.
- **DL-069 (2026-06-18)** had already made an **internal Gemma on a local Llama runtime** the primary LLM — expressly to remove external token cost. **DL-074 postdates it by one day.**
- And the engine is unoptimised: **Deep Pass is a full re-derivation on every run** (~6× more expensive than necessary).

**So the tier ladder's numeric basis is SUSPENDED. Numbers are re-derived, not tuned.** Pass 2's proudest recoveries — Basic chat 75/day, Basic deep 6/day, the 4M/10M token governor — are now **retired or pending**. The lesson compounds: *a hole you cannot find is worse than a hole you can* — **and a number you found is not the same as a number that holds.**

## 2. What changed in the prototype

- **§1 — never tier judgment quality.** The `ROUTING` per-tier ladder is struck → `MODEL_ROUTING_BY_STEP` (identical for all tiers). Every *"Pro adds model quality / the quality upsell"* line is gone. **Pro = execution & programme support.** New guard.
- **§6 — one honest limit, in analyses.** The token governor is gone. `ANALYSIS_BUDGET = {free:null, basic:null}` → **pending re-derivation; nothing enforced.** **UP-1, UP-2 and UP-5 deleted from the prompt table.** **Chat is uncapped** (the gate in `sendChat` is deleted). Daily caps are shown as *counts*, explicitly *"not a product limit."*
- **§7d — assisted-apply cap.** New **UP-APPLY**. Threshold **UNSET ⇒ no cap.** The binding line is implemented and asserted: **recommendation always visible · only the assisted apply metered · manual editing always free** (offered as the *first*, one-click resolution). Basic gets **"Apply all recommended fixes."**
- **§7d-bis — refresh.** New **`updateNow()`** — **no tier check exists.** Free: slow auto + Update now. Basic: continuous. The coalescing window is documented as keying off **the user's journey, never the tier.**
- **§7c — no latency lever.** Not built; said out loud on the Plans page (*"the upgrade we deliberately did not build"*).
- **§7j — REPORTS (new surface).** Sidebar nav + modal + `REPORTS` registry. Six strategic reports + the free PDF snapshot. Reliability-qualified · **confidence = understanding maturity** · currency marker · disclaimer · **packages, never produces** (generating one runs no analysis — asserted against the function's own source) · no fabricated completeness. **Names labelled descriptively and flagged "naming pending."** The **binding reputational-risk note** is carried in-product.
- **§5 — Plans rebuilt** on the re-derived ladder. **§7f** conversion moments listed honestly, up front. **§7e** reverse trial **gated behind GA**. **§7h** outcome pricing prohibited and said so. **§7g** one-click, price-on-the-button, no sales call.
- **BASIC_PRICE = $12** kept, **with a pending-basis marker**.

## 3. Verification

| Check | Result |
|---|---|
| `node --check` on the extracted `<script>` | **PASS** |
| jsdom **without** `runScripts` → body children | **32** (was 31; +1 = the Reports modal) |
| Boot assertions `window._S10` | **17/17 PASS** (8 prior + 9 new) |
| Console errors, boot + full behavioural run | **none** |
| (a) chat uncapped | `_limit('chat') === null`, `_capHit('chat') === false` — **PASS** |
| (b) monthly budget = the single surfaced limit, in analyses, pending | `_budgetWord() === "pending re-derivation"`; no token figure rendered — **PASS** |
| (c) at the assisted-apply cap the recommendation is visible + manual editing works | recommendation present before **and** after the gated attempt; Apply button still enabled; `_applyManually()` opens the artifact — **PASS** |
| (d) "Update now" on Free | allowed; spends 1 analysis; guard passes — **PASS** |
| (e) Reports exist, reliability-qualified, no health framing | 7 cards, 7 "naming pending" badges; `genReport()` spends no meter — **PASS** |
| (f) Free retains a shareable artifact | the PDF read snapshot, `_reportAllowed` true on Free — **PASS** |
| (g) Slices 1–9 non-regression | Overview · Attention · Artifacts · Issues · History · Workspace · Share/Export/CRR · chat all intact; dark default held — **PASS** |

**New guards:** `_assertNoTierKeyedModelQuality` · `_assertBudgetInAnalyses` · `_assertChatNeverCapped` · `_assertRecommendationNeverHidden` · `_assertUpdateNowFreeOnEveryTier` · `_assertNoPriorityQueueLever` · `_assertDowngradeNeverRemovesUnderstanding` · `_assertNoOutcomePricingCopy` · `_assertReportsNoHealthFraming`.

*(The copy scanners are **denial-aware** — sentence-level — so the product may state a prohibition by naming it without tripping its own guard. Three initial false positives were found and fixed this way; a fourth was a **real** self-check bug: `_assertReportsNoHealthFraming` was matching `genReport`'s own comment. It now matches a **call**, not a mention.)*

## 4. The corrected census

**58 values · 39 RATIFIED · 3 PENDING RE-DERIVATION · 8 RETIRED/STRUCK · 5 UNSET · 3 RECOMMENDATION.**

- **PENDING (3):** monthly analyses Free · monthly analyses Basic · **Basic price (basis)**.
- **RETIRED (8):** daily fix cap Free/Basic · daily chat cap Free/Basic · daily analysis cap Free/Basic · the priority-queue lever · outcome pricing. *(Kept in the census, visibly struck — so nobody re-derives them from a blank.)*
- **UNSET (5):** **assisted-apply cap (NEW)** · coalescing window · Free CRR cap · MON-04 prompt cap · billing rail.
- **RECOMMENDATION (3):** seats Free · seats Basic *(Basic = 10 **withdrawn** by DL-103 as commercially unsound)* · CR-2-vs-gate behaviour.

## 5. ⚠️ NEW CANON TENSIONS — escalated, not invented

1. **T10-8 — §7e still lists "priority queue" among what a downgrade takes back, but §7c STRUCK the priority lever.** A downgrade cannot take back a lever that was never built. **The build followed §7c** (the later, explicitly-corrective clause) and left "priority" out of `DOWNGRADE_TAKES_BACK`. **Recommend striking the word from §7e's list.**
2. **T10-9 — §1 and §5 give Pro "+ speed/priority" as a differentiator, which §7c also strikes.** The build renders Pro as **execution & programme support only**, with **no speed claim on any card**. **Owner decision:** is there a *non-artificial* speed dimension at Pro (dedicated capacity/concurrency — real cost, not fabricated latency)? If so it needs its own clause; **as written it reads as the struck lever.** The build did not invent one.
3. **T10-10 — the ratified UP-* taxonomy is now stale.** UP-1/UP-2/UP-5 are retired by a decision record but still stand in `12_freemium_tier_behavior_logic.md`; and the two prompts the product now needs — **UP-APPLY** and **UP-REPORT** — **have no canon UP-number.** Shipped with an explicit "escalated" marker. **Re-issue the taxonomy.**
4. **T10-11 — the reputational-liability class.** §7j puts OSLO's read in front of the user's leadership **under the user's name**. "Confidence ≠ health/readiness/probability" is no longer only an internal-honesty constraint — it is a **career-risk constraint for the user**. **Recommend: "a report that could be mistaken for a health rating" becomes a P1 defect class in QA.** The build asserts it at runtime; the specification does not yet say it is a defect.
5. **T10-12 — DL-102 constituent E is internally stale** (it adopts the now-retired UP-1/UP-2/UP-5 numbers "unchanged"). DL-103's *Supersedes* block covers it, but DL-102's own text still reads as current. **Recommend annotating in place.**
6. **Blocking, restated:** `RELEASE_1_REPORTING_SPECIFICATION_V1` (M4 has **zero** capability rows) and `RELEASE_1_TIER_DEFINITIONS_V1` (18 documents cite a document that does not exist).

## 6. What I refused to do — pass 3

I set **no** analyses-per-month figure, **no** assisted-apply threshold, **no** seat count, **no** report name, and **no** reverse-trial duration. Where the mechanism was ratified and the number was not, **the mechanism ships and the number renders pending or unset — and the product says so, to the user, in plain language.** The demo triggers install labelled *illustrative* thresholds so the behaviour is testable; **not one of them is a product value, and every surface that shows one says so.**

---

# PASS 4 — REPORTING (M4) built properly · D143–D147 (owner: "accept all", 2026-07-12)

**The scaffold is gone.** The six-card "strategic suite" that the DL-103 §7j fold-in shipped has been **deleted** — the `REPORTS` array, the `.rpt-grid` card layout, the per-card `genReport(k)` path, all of it. In its place: **ONE composable readout**, built against the ratified design.

## 1. What changed

### D143 — one report object, not six
- **Deleted:** `REPORTS[]` (7 entries), `.rpt-grid`, `.rpt` cards, `_reportAllowed()`.
- **Built:** a single **live composer → readout** surface. *"Leverage read"* is now **§2**. *"Reliability disclosure"* is now **§5, in every report.** Alignment / assumptions / decisions are **optional sections of one memo**.
- The nav item and the toolbar `◕` both open it. Both are relabelled **"Readout"** — descriptive, **"naming pending"** (DL-053). The toolbar button was a dead `openReportStub()`; it is now live.

### D144 — the fixed spine (§1–§5)
`_spineRead()` → **§1 the read** (one line, understanding maturity, reliability-qualified) · **§2 what's limiting it** (the limiting CAF dimension **and the specific reason** — the top open issue bound to it) · **§3 what we don't know** (open clarifications + the derived-vs-attested artifact split) · **§5 how to read this** (Coverage · Evidence availability · Assessability, the analysis-currency marker, the standing disclaimer).
`_spineAsk()` → **§4 what I need from you** (decisions owed + **MRI-07 Understanding Dependencies**).
Everything is painted from **live state** — `_chatState()`, `currentRead()`, `_readCurrency()`, `_epiOf()`, `ISSUES`, `TREND`, `HISTORY`, `_allAwaiting()`. Nothing is fabricated and nothing is recomputed.

### D145 — tailor the ASK, never the READ (the binding one)
Enforced **structurally**, not just behaviourally:
- **`_spineRead()` takes no argument and reads no composer state.** It literally **cannot see who is receiving the report**, so it cannot shade the truth for them.
- **`_assertAskTailoredNeverTheRead()`** renders the read for **all four recipients** at boot and **byte-compares §1–§3**; it *also* greps `_spineRead`'s own source and fails if it so much as mentions the audience.
- §4 carries the rule on its face: *"This is the only section that changes when you change the recipient… One honest read. Many asks."*

### D146 — live composer → dated snapshot
`genReport(fmt)` produces a **dated snapshot** into `REPORT_SNAPSHOTS[]` — `{stamp, runIndex, run, when, to, sections, stale}` — rendered in a *"Snapshots — this is what travels"* list. Each carries its own **analysis-currency chip**, dated to the **analysis run**, never to the moment of export, and **relabelled "previous analysis"** once `TREND` advances past it. **No analysis is run by any of it.**

### D147 — tiering, scheduling, names
- **Free:** the **full spine §1–§5**, PDF, OSLO-marked (**CHG-061 — the seed is never gated**).
- **Basic:** optional sections + branding + scheduling + all export formats.
- Every locked control **stays enabled** (D138); the **attempt** fires `UP-REPORT`, rewritten to name the new limit and lead with the free resolution.
- **Scheduling:** `runScheduledReport()` **re-checks currency at send time** and, when stale, ships **labelled "previous analysis"** — it never runs an analysis to freshen itself. ⬜ **R1-vs-fast-follow: owner-open, built and flagged** (`SCHEDULING_R1 = null`).
- **Names:** `REPORT_BANNED_NAMES` now fails the render on **"status report"**, "health report", "readiness report", "rag report".

## 2. Verification (all run, all reported)

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted `<script>` | ✅ **PASS** |
| 2 | jsdom **without** `runScripts` → body child count | ✅ **32** (unchanged — healthy) |
| 3 | Boot assertions `window._S10` | ✅ **21/21 PASS** — the 17 prior + **`spineComplete` · `askNotRead` · `rptPackagesOnly` · `schedRechecks`** |
| 4a | Six-card scaffold gone | ✅ `.rpt-grid`/`.rpt` = **0 nodes**; `REPORTS` = **undefined**; one readout, **5 spine sections** |
| 4b | Recipient changes **§4 only** | ✅ sponsor→exec→ops: **only `[data-spine="4"]` differs**; §1–§3 **byte-identical** across all four |
| 4c | Free = PDF read snapshot; Basic = sections + branding + scheduling | ✅ 0 disabled controls on Free; `UP-REPORT` fires with the free resolution first; Basic renders the optional sections |
| 4d | Export → **dated** snapshot with the currency marker | ✅ `Snapshot 1 · 12 Jul 2026, 00:46 · Initial run · to the Sponsor` |
| 4e | Stale read exports labelled **"previous analysis"** | ✅ in §1, in §5, and on the snapshot card; the **scheduled** send too |
| 4f | **Packages, never produces** | ✅ `TREND.length` and the analysis meter **unchanged** after compose + export + scheduled send |
| 4g | Slices 1–9 + rest of Slice 10 non-regression | ✅ 38-step smoke run (all views, all modals, every demo trigger, Alpha→GA→Alpha): **zero console errors**; self-check green |

## 3. Docs updated
All ten Slice-10 house docs (the shared §7j row is rewritten to **D143–D147** in every one) · **product-detail** (new D143–D147 section) · **user-experience**, **frontend-ui**, **workflow**, **product-data** (new reporting sections) · **success-criteria** (15 new criteria, R1–R15) · **e2e-test-scenarios** (S10-M4-A…F) · **edge-cases** (E-M4-1…7; E-DL103-5/7 rewritten) · **open-items** (report names · scheduling R1-vs-fast-follow · branding tier) · **tier-definitions-census** (Reporting Free/Basic rows rewritten; 3 new rows; the open-decisions table is now **8**).

## 4. ⚠️ NEW — escalated, not invented

1. **T10-13 — a pre-existing guard false-positive, surfaced by the smoke run (NOT caused by this pass).** `_assertNoGenericUpgradeCopy()` (MON-04) returns **false when `TIER === 'basic'`**, because `UP-6`'s body only names the word *"Basic"* when it is selling *up* to Basic. A Basic user reloading the app therefore gets a **red console error at boot**. It is untouched by this pass (boot on Free — the default — is green, 21/21), and fixing it means changing the MON-04 guard so a prompt is only required to name its relieving tier **when the user is below it**. **I did not touch the guard.** Owner/engineering call.
2. **T10-14 — `UP-REPORT` still has no canon UP-number**, and its *limit* has now changed shape: it no longer gates "six strategic reports" but **optional sections + branding + scheduling**. The ratified UP-1…UP-8 taxonomy has no slot for it. **Re-issue the taxonomy** (this compounds T10-10).
3. **T10-15 — D147 makes scheduling a currency-safety surface, and canon has no rule for the case where the schedule fires while the read is stale AND the monthly analysis budget is exhausted.** The build does the only honest thing available: it **ships the package labelled "previous analysis" and does not run anything**. But nothing ratifies that the schedule should *silently* keep sending in that state rather than *pausing and telling the user*. **Owner: does a scheduled readout keep sending when the read cannot be refreshed, or does it pause?** I did **not** invent a pause.
4. **T10-16 — "how our understanding matured" is the one optional section that is unbounded in time**, and D128 guarantees History is never metered. On a long project the narrative section will grow without limit inside an artifact the PM sends to an exec. **No canon governs its length**, and I did **not** invent a truncation rule — truncating the epistemic record inside a report would be the thin end of metering it. **Owner: is there a summarisation rule, and if so, who authors it?**

## 5. What I refused to do — pass 4
I did **not** name the artifact. I did **not** decide whether scheduling is R1. I did **not** decide whether branding belongs at Basic. I did **not** invent a length rule for the History narrative, a pause rule for a stale schedule, or a UP-number for `UP-REPORT`. **Every one of them is flagged on the surface, in the docs, and above.**

---

# PASS 5 — REPORTING REBUILT (D148–D154, owner-directed, 2026-07-12)

> **The owner rejected pass 4's Reporting surface.** Two defects: it was a **modal**, and the report was **too meta** — *"it described OSLO's epistemic state instead of speaking to its reader."* D148–D154 **revise D144/D146/D147**. D143 (one composable readout) and D145 (tailor the ask, never the read) **stand**. This is the rebuild.

## 1. What changed

**D148 — Reports is a WORKSPACE.** The modal (`#reportsScrim`, `closeReports()`, `_reportsIsOpen()`, the Esc handler) is **deleted**. Reports is now `<section class="pane" id="pane-reports">` inside `.body`, a **peer view** to Overview · Attention · Artifacts · Issues · History — same nav, same `showView()` mechanism, same `_scrollMem` / `_syncNav` / crumb treatment. **Left:** the live composer (`#reportsBody`). **Right:** the package wrapper (`#rptPkg`) and the **document** (`#rptDoc`) — a real page with a byline, headings and one small table.

**D149 — the governing writing rule, and the heart of the rebuild.** The old spine (*"§1 The read · §2 What's limiting it · §3 What we don't know · §5 How to read this"*) was **OSLO describing itself to a sponsor**. Struck. The memo is now an **executive summary written for its reader, in their language** — **zero OSLO vocabulary**, enforced at runtime against the rendered DOM (`REPORT_OSLO_VOCAB`, word-boundary, **no denial exemption**). The epistemic honesty is re-rendered as **ordinary good writing**:

> *"We are planning for 450+ people on it at once against a 500-device figure that **came from our own plan, not from The Grid**."* — derived-vs-attested, in English.
> *"Dates without owners are estimates, not commitments."* — low reliability, in English.
> *"The weak point here is people, not process."* — the limiting dimension, in English.

**D150** — seven sections, fixed order, **risks before assumptions**. **D151** — two altitudes on every risk (*for the plan* / *for the goal*), with a **forecast guard** holding the knife-edge: outcome impact is *"does the plan, AS WRITTEN, still reach its stated intent?"* — a structural claim — never *"will this project succeed?"* **D152** — the plan of action is the **PM's, first person**; OSLO seeds, the PM owns; guarded (first person · never names OSLO · always editable). **D153** — the disclaimer moves to the **package cover**; the **currency marker stays in the body** as plain attribution. **D154** — **editing is free on every tier**; the gate is **reuse** (Basic remembers the wording; `simNextWeek()` makes it testable).

## 2. Verification

| Check | Result |
|---|---|
| `node --check` on the extracted script | ✅ **PASS** |
| jsdom **without** `runScripts` → healthy body | ✅ **PASS** — 31 children; the modal is gone, the pane is inside `.body` |
| Boot assertions (`window._S10`) | ✅ **26/26 TRUE** — 16 standing + 10 reporting |
| New guards | `_assertNoOsloVocabularyInReport` · `_assertNoForecastLanguageInReport` · `_assertReportStructure` · `_assertPlanOfActionIsPMVoiced` · `_assertDisclaimerOnPackageNotInBody` · `_assertEditFreeOnEveryTier` (all ✅) |
| Console errors, boot + full behavioural run (Free) | ✅ **zero** |

**Behavioural (jsdom, scripts executing):** (a) Reports is a workspace, reachable exactly like Overview/Issues/History ✅ · (b) **zero** banned OSLO vocabulary and **zero** forecast language in the body ✅ · seven sections in order, five risks each carrying **both** altitudes ✅ · (c) changing recipient changes **only** `[data-sec="decisions"]` ✅ · (d) **editing works on Free**, and Free persists nothing ✅ · (e) Basic persists and **re-applies** the wording across "weeks" ✅ · (f) the export snapshot is dated, carries the currency marker, and the **disclaimer is on the cover, not in the body** — while the body carries *"plan as of 12 July"* ✅ · generating a report moved the trend, the governor and the meter by **zero** ✅ · (g) **Slices 1–9 + the rest of Slice 10 non-regression** — all six views switch, everything intact ✅.

**Pre-existing observation (NOT a regression):** `_assertNoGenericUpgradeCopy()` (MON-04) returns **false while `TIER==='basic'`**, because **UP-6**'s body only names *"Basic"* in its Free branch. Reproduced on a pristine boot with `setTier('basic')` and **no Reports interaction**. Not caused by this pass; logged in `open-items.md` for the owner.

## 3. NEW TENSIONS — escalated, not invented

1. **T10-17 (the sharpest one) — the vocabulary and forecast guards EXEMPT the PM's own sections, and they have to.** Policing the user's prose would be *the tool writing the report again*, which D152 explicitly forbids. **But** a PM can type *"we're 80% likely to hit 450"* into their own summary, and it goes out **under OSLO's mark, on OSLO's cover, carrying OSLO's disclaimer**. Two defensible answers: **stay silent** (advisory-only; their words, their name) or offer a **gentle, non-blocking note** (*"that reads as a prediction; OSLO does not make those"* — advisory, not a gate). **I did not pick.** `open-items.md` R-2.
2. **T10-18 — the memo carries a normal `To:` line in its header.** D145 fixes §1–§5 for every recipient and lets §6 be addressed. A `To:` line is **addressing, not re-framing** — no assessment varies with it — so the guard is deliberately **section-scoped**. If the owner reads D145 as forbidding *any* recipient-varying byte in the document, the `To:` line must go. **Flagged, not assumed.** (R-3)
3. **T10-19 — the seven sections are sized for a one-page memo, and nothing bounds them.** Risks are capped at 5; the appendix walks every workstream and grows without limit on a large plan. **Selection is the value** — but *what gets cut, and who decides*, is a spec question and I invented no truncation rule. (R-4)
4. **T10-20 — the persistence prompt has no UP-number in canon.** D154 changed what the prompt sells (persistence, never the edit), and no `UP-*` covers it. The build reuses the `UP-REPORT` key and **says so on the surface.** (R-1)

## 4. What I refused to do — pass 5
I did **not** gate editing. I did **not** put the disclaimer back into the prose. I did **not** let the report forecast anything, and I did **not** let OSLO write the plan of action. I did **not** police the PM's own words. I did **not** name the artifact, decide scheduling's release, decide branding's tier, invent a truncation rule, or mint a UP-number. **Every one is flagged on the surface, in the docs, and above.**

---

# Slice 10 — fold-in: **D155 · D156 · D157 · D158** (2026-07-12)

Amended **in place**: `vertical-slices/slice-10-tiering-limits/prototype.html` (14,287 → 14,547 lines). No new files, no regressions.

## What changed

### 1. D158 — the real bug: `_assertNoGenericUpgradeCopy()` (MON-04)
**A Basic user got a red console at boot.** The guard demanded the relieving tier's **name** in the prompt copy **unconditionally**, but **UP-6 only names "Basic" in its Free branch** — correctly, because to a Basic user the honest copy is *"wait for the reset, or allow metered overage"*, not an upsell.

**The guard was checking the wrong condition.** MON-04 requires a prompt to name **the tier that RELIEVES the limit** — meaningful **only when the user is BENEATH that tier**.

**Fix:** `TIER_ORDER` → `_tierRank()` → `_beneathTier(p.tier)` gates the name requirement. The **limit name** and the **tier field** stay required unconditionally. ⚠️ **A fix to the GUARD, not a relaxation of MON-04** — verified negatively: on Free, generic copy still fails.

### 2. D155 — the gentle forecast note (the important one)
The vocabulary/forecast guards exempt `data-pm="1"` (the PM's own sections) **and must** — policing the user's prose is the tool writing the report again (D152). But a PM could type *"we're 80% likely to hit 450"* into their own summary and it would ship **under OSLO's mark, on OSLO's cover, carrying OSLO's disclaimer**.

**Built: an unobtrusive advisory beside that section.** Same vocabulary (`REPORT_ADVISORY_WORDS = REPORT_FORECAST_WORDS + REPORT_BANNED_FRAMINGS`), **opposite treatment — a FAILURE in OSLO's words, an ADVISORY in the PM's.**

| Binding property | How |
|---|---|
| **NEVER blocks** | **The send path cannot SEE the note.** `_assertForecastNoteNeverBlocks()` — structural (send path · note renderer) + behavioural (no disabled send control while a note is live; dismiss control present). |
| **NEVER edits** | PM prose rendered **byte-verbatim**; note appended **beside** it. `_assertOsloNeverRewritesPMProse()` — only `saveReportSection`/`resetReportSection` may write `RPT_EDITS[...]`. |
| **DISMISSIBLE** | `dismissForecastNote(k)` → send anyway. Always. Cleared on re-edit (new words, fresh advice). |
| **Rationale in code** | *Blocking would be the tool overruling the human (advisory-only, D001); silence would be OSLO lending its name to a claim it forbids itself. The note is the only honest position.* |

**Side-fix required by D155:** `_assertDisclaimerOnPackageNotInBody()` scanned the **whole** body, so a PM typing *"probability of success"* into their own summary **turned the console red** — OSLO grading the human's words, the exact failure D155 exists to prevent, arriving through a side door. It now **exempts `data-pm="1"`**, consistent with D149/D151/D152.

### 3. D156 — the `To:` line stays
Kept. Code comments at **both** the render site and the guard record why: **D145 forbids re-framing the assessment by audience, not addressing the document.** The guard stays **section-scoped** — §1–§4 (+ §5 + appendix) byte-identical across recipients, only §6 varies. `REPORT_TO_LINE_STAYS = true`.

### 4. D157 — length
Risks capped at **5**, highest impact first (`MEMO_RISK_CAP`, **explicitly labelled illustrative, not a ratified product value**). Appendix now **explicitly skippable** (*"For the leads — skip this if you are not one"*) and walks **every** workstream. ⬜ **What gets cut and who decides is carried as an M4 spec open item (`open-items.md` M4-O4) and surfaced in-product. No truncation rule invented.**

## Verification (all green)

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without** `runScripts` → body child count | **31** (unchanged) |
| 3 | Boot assertions `window._S10` on **Free** | **28/28 pass · 0 console errors** |
| 3 | Boot assertions `window._S10` on **Basic** (pristine, `oslo-s1-tier='basic'`) | **28/28 pass · 0 console errors** ← the D158 fix |
| 4a | Pristine boot `TIER='basic'` | **zero console errors** |
| 4b | Forecast language typed into a PM section | **note surfaces** (hits: *likely, on track*), **0 console errors** |
| 4c | Note live → export | **snapshot produced**; **0 disabled send controls**; PM text **byte-verbatim**; `RPT_EDITS` unchanged |
| 4d | Dismiss | note gone, **PM text intact**, export still works |
| 4e | OSLO-authored sections | **zero OSLO vocabulary, zero forecast language** (both guards `true`) |
| 4f | Editing free on every tier | `_reportEditAllowed()` `true` on Free **and** Basic; `_assertEditFreeOnEveryTier()` `true` |
| 4g | Slices 1–9 + rest of Slice 10 | all spot guards `true`; every view renders; **0 console errors** |
| — | **Negative tests (the guards still BITE)** | generic upgrade copy on Free → `false` · tampered PM DOM → `false` · disabled send control with a note live → `false` |

## Docs updated
`product-detail.md` · `user-experience.md` · `frontend-ui.md` · `e2e-test-scenarios.md` (T10-E-30…40) · `success-criteria.md` · `edge-cases.md` (E-M4-13…20; **E-M4-8 closed**) · `open-items.md` (**M4-O1…O6**: names · scheduling R1-vs-fast-follow · branding tier · **report length / what gets cut** · **UP-number for the persistence prompt** · reporting capability rows).

## New tension — escalated, not invented
**`_assertDisclaimerOnPackageNotInBody()` was silently policing the PM's prose.** It is now exempted for `data-pm="1"` sections, on the D155/D152 reasoning. **This is a guard-scope change, not a doctrine change** — the D153 requirement (*the package carries the disclaimer; the memo body does not*) is unchanged for **OSLO's** paragraphs. Flagging it because it was not in the fold-in brief and it is the same class of latent defect as D158: **a guard that grades the wrong author**. Recommend an owner glance; nothing else in the build depends on it.

---

# Fold-in — D159 · D160 · D161 (2026-07-12) · **"Obey the doctrine. Don't narrate it."**

**Owner-directed global simplification pass on the final Slice 10 prototype.** Presentation / IA only — **no behavioural regressions, every runtime guard still passes.**

## The rule

> **The doctrine governs what the product may CLAIM and DO. It must NEVER govern how much the product TALKS.**
> **Obey it everywhere. Speak it almost nowhere.**

The build was written under instructions to *"carry the note in-product"* and *"say it out loud."* The owner has named that as the error: **the say-it-out-loud test was a constraint on BEHAVIOUR, and it was turned into a CONTENT REQUIREMENT.** The app was explaining its own reasoning to its user — a museum placard about itself.

## What changed

### 1 · D161 — the "Prototype notes" toggle (OFF by default, persisted)
One toggle, in the demo scaffold bar. **Off ⇒ the app looks and reads like a product. On ⇒ every owner-TBD, canon citation, retired lever, guard name and escalation is revealed for governance review.**

**The governance content is RELOCATED, NOT DELETED.** `pn(html, kind)` returns an **empty string** when off, so the strings **never reach the DOM** — deliberately *not* `display:none`, because "hidden but present" is exactly how meta copy creeps back. Annotations are **never** stored in `data-*` attributes for the same reason; static markup is served from JS via `PN_SLOTS` / `PN_TITLES`. Styled as a hatched, monospaced annotation layer with `PROTOTYPE NOTE` / `OWNER-TBD` / `CANON CITATION` / `RUNTIME GUARD` / `ESCALATION` headers — **it cannot be mistaken for product copy.**

### 2 · D160 — Reports: the reading surface is sacred
The 360px composer is **gone**. It had carried six explanatory panels — the governing writing rule, quoted; a panel explaining that the document contains no OSLO vocabulary; the two-altitudes-of-risk explainer; the forecast-note explainer; the editing-is-free essay; and the open-items register. **All true. All correct. None of it the user's business.**

- **Default view = the document, and only the document.** `#rptDoc` is a centred page, ~74ch, generous whitespace.
- **Slim toolbar** (`#rptBar`): **Recipient · Sections · Format · Schedule · Export.** Each opens a drawer; **all closed by default**; one at a time; `Esc` returns you to the document.
- **The package wrapper** (`#rptPkg`) is **export metadata** — moved into `#rptPkgHost`, shown **only on the export preview**. It is still always rendered and still always carries the disclaimer.
- **Currency marker** stays in the body as plain attribution. **Forecast note (D155)** appears **only when triggered** — verified 0 resident.

### 3 · D159 — global sweep
Every surface: Reports · Plans · Limits ("Your plan") · Settings · Share · Export · Access & invites · all 9 UP prompts · chat (`_s10Reply`) · the demo scaffold bar · the reviewer-view ribbon · static chrome and tooltips.

## Word counts — user-visible copy, notes OFF

| Surface | Before | After | Δ |
|---|---:|---:|---:|
| **Reports workspace** (whole pane) | 3,282 | **1,817** | **−45%** |
| · the document itself | 1,749 | 1,693 | −3% |
| · **chrome around the document** | 1,533 | **124** | **−92%** |
| **Plans modal** | 3,786 | **707** | **−81%** |
| **Settings** | 2,090 | **1,433** | **−31%** |
| Limits / "Your plan" modal | 5,176 | **427** | **−92%** |
| Share modal | 902 | 743 | −18% |
| Export modal | 390 | 303 | −22% |
| Access & invites modal | 1,859 | 1,035 | −44% |
| **TOTAL** | **17,485** | **6,465** | **−63%** |

*The document barely moved (−3%) — that is correct. The report was never the problem; the scaffolding around it was.*

## Verification

1. **`node --check`** → **PASS**.
2. **jsdom without `runScripts`** → **31 body children** (healthy).
3. **Boot assertions (`window._S10`)** → **28/28 PASS** on **Free × Basic × notes-OFF × notes-ON**, **0 console errors** in all four quadrants.
4. **Behavioural**
   - Reports default view: **0** recipient chips, **0** drawers open, package wrapper **not shown** — and the package is **still populated and still carries the disclaimer** (canon satisfied).
   - Memo structure intact: `summary → changes → risks → assumptions → plan → decisions → appendix`; currency marker in the body; **0 resident forecast notes**.
   - Controls reachable: all five drawers open from the toolbar; the Export drawer surfaces the package + 2 export actions; `Esc` closes.
   - **Rendered-DOM meta grep** (`DL-` · `D###` · `CR-#` · `CHG-` · `UP-` · `MON-` · `§` · "owner-TBD" · "not ratified" · "naming pending" · `T-#` · `X-1` · `CRR-`): **0 hits with the toggle OFF · 672 hits with it ON**, on both tiers.
   - All Slices 1–9 + Slice 10 surfaces still work; **0 console errors**.
5. **Negative controls** (proving the guards are not vacuous): remove the toolbar Export button → **`d138` fails**; gate editing on Free → **`rptEditFree` fails**; strip the package disclaimer → **`rptDiscOnPackage` fails**.

## Guard changes — guards fixed, doctrine never

- **`SELLING_SURFACES` re-pointed.** `reportsBody` **was** the composer; under D160 it is the notes rail. Left alone, every copy prohibition (`_assertNoTierKeyedModelQuality`, `_assertNoPriorityQueueLever`, `_assertNoOutcomePricingCopy`, `_assertReportsNoHealthFraming`) would have started **scanning an empty div and passing for free** — a guard that passes because it is looking at nothing is worse than no guard. Now covers `rptBar` · `rptDrawer` · `rptDoc` · `plansBody` · `limitsBody` · `upBody`. **Coverage did not drop.**
- **`_assertNoDisabledLimitAffordances()` (D138) strengthened.** With the export drawer closed, `.rpt-act .btn` is not in the DOM — the check would have passed **vacuously**. It now **also demands a permanently-present, never-disabled `#rptExportBtn`** on the toolbar. **A drawer is a disclosure, not a hiding place.**
- **Defect found and fixed:** `renderAccess()` declared a local `const pn` that **shadowed the global `pn()` note-builder** for the whole function body — a TDZ `ReferenceError` waiting for the first note added above it. Renamed to `phEl`.

## Tensions — escalated, not invented

**1 — The Tier Definitions findability problem is NOT solved by this toggle.**
**D136** put the census **in the product** precisely so the numbers would be **findable**; the diagnosis was that *"a product-scoped reader (a person, or a model) never finds them, and a model that cannot find a number invents one."* That has already happened twice (`Basic = 10 projects` against ratified canon that says **3**; *"Basic's price is undecided"* when it is **$12/mo, owner-confirmed**). Moving the census behind the toggle is right **for the product** — a user does not need our ratification statuses — but **it does not fix the gap, and it must not be mistaken for a fix.** *The fix is writing the `RELEASE_1_TIER_DEFINITIONS` specification that eighteen canonical documents already cite and which has never been written.* **The escalation stands.**

**2 — D159 supersedes three earlier "label it in-product" instructions.**
The seat cap was to be *"labelled as a recommendation in-product"* (D129 / DL-102 E); the report artifact was to be flagged *"naming pending"* (D147 / DL-053); the reverse trial was to be stated *"NOT live in Alpha"* on the Plans page. **The brief's zero-hit grep list names `"not ratified"` and `"naming pending"` explicitly**, so all three moved behind the toggle. **In every case the BEHAVIOUR is unchanged** — the seat cap is still held as a `RECOMMENDATION` in config and never sold on; the artifact still avoids "status report" and any health/readiness framing; the reverse trial is still not live and not simulated. **Only the words shown to the user moved. If the owner intended any of those labels to remain user-visible, say so and they come back in one edit.**

## Docs updated
`frontend-ui.md` · `user-experience.md` · `product-detail.md` · `success-criteria.md` (all carry the D159–D161 amendment header) · `edge-cases.md` (**E-PN-1…5**, **E-RPT-D160-1…5**, **E-META-1…3**) · `open-items.md` (**O-D159-1…4**).

---

# D162 — Issue Panel: progressive disclosure + the copy rule (2026-07-12)

**Brief:** the owner rejected the Issue Panel as cognitively overwhelming. **The D159 sweep missed the panels** — which is exactly where the doctrine copy had accumulated worst. Presentation/IA pass on `vertical-slices/slice-10-tiering-limits/prototype.html`. No logic changes.

## What changed

**D162a — the copy rule (say it once, short, no rationale).** Deleted outright, from the Issue Panel **and** the share dialog:
- *"◆ This is a **validation recommendation** — the kind that a second pair of eyes settles fastest. Prime candidate for a review request."* → **design rationale said out loud.** Gone (both sites).
- *"0 review requests sent · **free and unlimited** — on every plan"* → **reassurance addressed to the owner.** Gone from the panel and the dialog; survives as a plain fact (*"N review requests sent"*) on the Settings usage surface, with the CR-2 sales pitch stripped.
- *"Sends the issue + its context + the recommendation + the artifact reference. It never changes the issue."* → **→ ⓘ tooltip on the button.**
- Comments: *"never change the assessment"* said **twice**, plus *"a conversation about the read, recorded next to it"*, plus the append-only lecture → **one short label at the moment it matters** (above the compose box) + the append-only contract on an **ⓘ**.
- Reviews: the *"evidence, not a verdict"* paragraph + the D133 alignment essay → **one line + an ⓘ**. The responses themselves stay in full, forever.
- Recommendations: *"Applying drafts the change… Discussing changes nothing"* and *"Recommendations live only inside the issue"* → **tooltips**.

**D162b — disclosure driven by intent.** Default panel = title · severity · dimension · artifact + jump link · lifecycle · the read (*Why this matters* + dimension impact) · **ONE primary action**. Everything else is a row: **Evidence · Recommendations · Clarification · Comments · Reviews**, then **[⤴ Share for review] ⓘ [✦ Discuss with OSLO]**.

**D162c — the three affordance defects.** New `.ip-rowh` component (**pointer cursor · hover background · rotating chevron · visible count · focus ring**, a real `<button>` so Enter/Space and `aria-expanded` come for free). **Clarification now defaults MINIMIZED** — the row names what OSLO needs (truncated question); the textarea appears on expand. **Share for review is just a button.**

**D162d — cascaded** to the Recommendation block, the Reviews block, the share dialog, and the artifact flyout (flyout = the read, truncated, + *Open issue →* + *Ask about this →*; the modal-firing *Share for review →* is off the hover).

## Word count — user-visible copy in the Issue Panel

| | Before | After | Δ |
|---|---|---|---|
| **Default state (what the user sees on open)** | **~206 words/panel** (~1,236 over 6 issues) | **71 words/panel** (427) | **−65%** |
| Copy present in the panel DOM at all (incl. collapsed rows) | 1,322 | 828 | **−37%** |

## Verification

1. **`node --check`** → **PASS**.
2. **jsdom WITHOUT `runScripts`** → **31 body children** (healthy, unchanged).
3. **Boot assertions (`window._S10`)** → **28/28 PASS** on **Free × Basic × notes-OFF × notes-ON**; **0 console errors** in all four quadrants.
4. **Behavioural** — (a) default panel: the read + **1** primary action + **4** collapsed rows, **0 visible textareas**, **0 explanatory paragraphs**; (b) Evidence row: hover rule + pointer cursor present, click → opens, 2 evidence items; (c) Clarification **collapsed by default**, row reads *"Has the venue confirmed Wi-Fi for 500+ concurrent…"*, expands to the input; (d) Share for review = **just a button**, `disabled=false`, contract on the ⓘ; (e) *"never change the assessment"* appears **exactly once** in the whole panel DOM, **"append-only" 0 times** on the surface (tooltip only); (f) rows are `<button>`s with `aria-expanded` flipping correctly; (g) same model on the recommendation block + flyout; (h) full smoke across every view, artifact editor, chat, CRR, comments, reports, history on both tiers → **0 console errors**.
5. **Negative control:** force the Recommendations row shut while the assisted-apply cap is hit → **`recNeverHidden` fails**. The guard is not vacuous.

## Guard change — closes a loophole, relaxes nothing

**`_assertRecommendationNeverHidden()` (DL-103 §7d) would have passed VACUOUSLY.** It checked `getComputedStyle('.ip-rec').display` — but under D162 the recommendation lives inside a collapsed row, and it is the **ancestor** that is `display:none`. The element's own computed display is still `block`, so the guard would have certified as "visible" something nobody could see. **Same failure class as the D160 export-drawer loophole.** Fixed on both sides: the guard now **also fails when `.ip-rec` sits inside `.ip-row:not(.open)`**, and **the product opens the row itself the moment the cap can bite** (`_ipRows()` defaults it open at `_capHit('fixes')`; `applyFix()` forces it open before raising the prompt). The binding line is intact.

## Tensions — escalated, not invented

1. **Primary-action precedence** when an issue has **both** a recommendation and an open clarification. Built to the letter of D162b (recommendation wins) — which means **"Answer" never becomes the primary action on the seeded data**, since every issue carries a recommendation. If the owner meant *"when OSLO is blocked on the user, Answer wins"*, it is a one-line change. **(O-D162-1)**
2. **The recommendation TEXT is now behind a chevron** while *"Apply this fix"* is resident. That is what D162b says. But the user's stated intent is *"what's wrong, **and what do I do about it?"* — an argument that OSLO's recommended sentence belongs next to the button. **Not decided unilaterally. (O-D162-2)**
3. **"Share for review →" removed from the artifact flyout** (a hover cannot carry rows; it fired a full modal). It survives, enabled and unmetered, in the panel. **CR-2 untouched. (O-D162-3)**
4. **The share dialog has NOT had a full sweep.** D162d named the recommendation panel and the flyout. The dialog still carries longer explanatory blocks — and **some of it is load-bearing at the moment of choosing a person** (a stranger needs to know a review grant costs them nothing). **A copy cut there could quietly become a CR-2 honesty cut, so it was not made without direction. (O-D162-4)**

## Docs updated
`frontend-ui.md` · `user-experience.md` · `product-detail.md` · `success-criteria.md` (all carry the D162 amendment header) · `edge-cases.md` (**E-D162-1…10**) · `open-items.md` (**O-D162-1…5**).

---

# D163 + D164 — the final Slice-10 pass (2026-07-12)

## TASK 1 — D163: comprehensive copy sweep with hard word budgets

### The exhibit, fixed

The Basic/report upgrade prompt shipped as a **~300-word, six-paragraph essay**. It is now **27 words**, and it still
does the three things MON-04 requires — **names the limit hit · names the tier that relieves it · offers the
resolutions.** The **standing prompt footer** (36 words of owner-reassurance on *every* prompt, forever) is **deleted
from product copy**; the promises it recited are behaviour, and they are still guarded.

### THE SURFACE TABLE — every surface, before → after → budget

**Measurement:** rendered DOM text, **prototype-notes OFF**, punctuation-only tokens excluded. *Prompt* = title +
body + honest label + resolution buttons (the owner's own model rewrite counts exactly this ≈27w); the
`Limit — <x>` **eyebrow** is measured separately against the ≤8 label budget. *Modal* = **prose** (narrative body
copy); feature rows / meter rows / settings rows are **labels** and are measured per-row (≤8 label, ≤20 helper).
Generated **content** (OSLO's read of the user's plan; the review package; the memo itself) is **not product copy**
and is excluded — see **O-D163-1**.

| Surface | Before | After | Budget | Result |
|---|---|---|---|---|
| **PROMPT — UP-REPORT** (the exhibit) | **307** | **27** | 30 | **PASS** |
| **PROMPT — UP-6** monthly analyses | 224 | **25** | 30 | **PASS** |
| PROMPT — UP-6 (deferred re-read) | 224+ | **29** | 30 | **PASS** |
| PROMPT — UP-6 (Basic, deferred) | 224+ | **27** | 30 | **PASS** |
| **PROMPT — UP-APPLY** assisted fixes | 145 | **26** | 30 | **PASS** |
| **PROMPT — UP-EXPORT** formats | 71 | **22** | 30 | **PASS** |
| **PROMPT — UP-7** (value) | 128 | **25** | 30 | **PASS** |
| **PROMPT — UP-3** upgrade-or-archive | 105 (+70 in the option cards) | **28** | 30 | **PASS** |
| **PROMPT — UP-4** partial analysis | 219 | **30** | 30 | **PASS** |
| **PROMPT — UP-SEAT** seat cap | 148 | **27** | 30 | **PASS** |
| Prompt **eyebrow** chips (all) | — | **3** | 8 | **PASS** |
| **Prompt FOOTER** (on every prompt) | 36 | **0** | — | **DELETED** |
| **MODAL — Plans** (prose) | 613 total | **59** prose / 323 total | 60 | **PASS** (rows ≤8) |
| **MODAL — Usage & Limits** (prose) | 351 total | **60** prose / 110 total | 60 | **PASS** (rows ≤8) |
| **MODAL — Access & invites** | 716 | **42 / 52 / 51 / 24** per block | 60/block | **PASS** |
| **MODAL — Export a snapshot** | 244 | **45** chrome (+34 ratified disclaimer) | 60 | **PASS** |
| **MODAL — Settings** (12 sections) | 1,108 | **6–128** per section; **every row ≤20** | per-row | **PASS** (O-D163-1) |
| **DIALOG — Share** (limit disclosures) | 82 | **60** | 60 | **PASS** |
| DIALOG — Share: role rows | 72 | **26** | 60 | **PASS** |
| DIALOG — Share: snapshot link **empty state** | 30 | **11** | 15 | **PASS** |
| **DIALOG — Share for review (CRR)** chrome | 197 | **42** | 60 | **PASS** |
| **PANEL — Issue panel** chrome | (D162) | **35** | 60 | **PASS** |
| **PANEL — Issue panel** longest row | — | **8** | 8 | **PASS** |
| **READOUT — toolbar** | 3 | **3** | 8 | **PASS** |
| READOUT — drawers (Recipient/Sections/Format/Schedule/Export) | 27/23/23/32/16 | **26/23/23/32/16** | 60 | **PASS** |
| READOUT — package wrapper | 63 | **43** | 60 | **PASS** |
| READOUT — prototype-notes rail (OFF) | 0 | **0** | 0 | **PASS** |
| **TOOLTIPS** (all, app-wide) | **16 over budget** (max 50) | **0 over budget** | 20 | **PASS** |
| **TOASTS** (54 call sites, 26 paths exercised) | **31 over budget** (max ~83) | **0 over budget** | 12 | **PASS** |
| **CHAT notices** (deferred-evidence, UP-8, CRR response) | 142 / 81 / 48 | **33 / 22 / 26** | — | **PASS** |

**Not one honest fact was cut.** Every honest label survives — *once, short*: "Editing is always free" · "Viewers take
no seat" · "Asking for a read is free — no invite, no seat" · "Nobody has been removed" · "previous analysis" ·
"Their answer is evidence — it does not resolve the issue" · "Comments never change the assessment" · every limit
disclosure that names the limit and the tier. **What was cut is the *explanation of why*** — and every word of it is
**relocated, not deleted**, behind the prototype-notes toggle.

### The share dialog and CRR — swept, honesty intact

The share dialog was deliberately left alone last pass because its copy is *partly load-bearing*. It is swept now, and
the load-bearing facts are kept **as short labels**: a new person costs an invite · the balance · the seat count ·
*Viewers take no seat* · **"Asking for a read is free — no invite, no seat."** In CRR, for a stranger: **"costs
nothing · no invite · no seat · they see this issue and nothing else · the grant ends when the issue resolves, or in
14 days."** **Cutting one of those would be a CR-2 honesty cut and is prohibited.** What went is the paragraph
explaining *why* OSLO never gates the seed of the loop.

---

## TASK 2 — D164: the Readout is a DOCUMENT. It gets the artifact editor.

**One editor. Two documents.** The readout's textarea stack (and its `**bold**` / `- bullet` markdown round-trip) is
**retired**. The PM edits the **rendered memo, in place**, with the **same editor as a plan artifact** (D066–D085):
inline rich text · the selection toolbar · ⌘B/I/U · undo/redo · the "/" slash menu · ⌘F find/replace · the link
popover · sanitised paste · the block model + drag-reorder · the same keyboard behaviour. **Bold, lists and the
decisions table survive editing intact.**

**Done without forking the editor.** The editor stops addressing `#artdoc` by name and addresses whichever document it
is driving: `_EDIT_HOST` (`'artdoc'` | `'rptEd'`) · `_edDoc()` · `_edKey()`. **47** `getElementById('artdoc')` lookups
inside the editor became `_edDoc()`. The **find bar moved out of `#artCenter` to body level** — nailed inside the
artifact pane it was *structurally unable* to reach the readout.

**Deliberately NOT shared (artifact semantics, not editor semantics):** epistemic provenance chips (they would put
**OSLO vocabulary into a document that forbids it** — D149) · the weakness stepper · artifact versioning + History
events · ⛔ **the reanalysis commit** — **a readout PACKAGES; it never PRODUCES** (D146). All five are gated at their
function heads by `_edIsArtifact()`, and the single structural-edit choke point returns early on the readout host.

**Constraints preserved and guarded:** PM sections byte-verbatim (D152/D155) · no OSLO vocabulary, reliability-
qualified (D149) · tailor the ask, never the read (D145) · editing free on every tier, the gate is REUSE (D154) ·
frame by outcome, never forecast (D151) · the gentle non-blocking note (D155) · the reading surface stays sacred
(D160) · packages, never produces (D146).

---

## DEFECTS FOUND AND FIXED (both real, both pre-existing)

1. **`renderShare()` declared `const pn` — shadowing the global `pn()` note-builder for the whole function scope.**
   Adding any prototype note to that function threw a **TDZ `ReferenceError` at runtime**. Renamed. **Nothing in this
   file may shadow `pn()`.**
2. ⛔ **`_ipRows()` decided the Recommendations row's state only on the panel's FIRST open.** So if the
   assisted-apply cap became hit **while the panel was already open** — which the demo trigger does, and a real user
   does by applying their last assisted fix — **the recommendation stayed COLLAPSED at the cap.** That is metering
   **understanding**, and it is **PROHIBITED** (DL-103 §7d · D126 · D128). **Fixed:** the row is **forced open for as
   long as the cap is hit**; `ipToggleRow()` refuses to collapse it while capped; the demo trigger re-renders an open
   panel.
3. **Guard defect (same area):** `_assertRecommendationNeverHidden()` scoped only its **first** check to "the panel is
   on screen"; the other two graded the panel's **stale innerHTML after it had been closed**. **A guard that fails on a
   surface nobody can see is as wrong as one that passes on a surface nobody can see.** All three checks are now scoped
   to a visible panel — **and both negative controls still bite.** `closeIssue()` now also clears the panel DOM.

---

## VERIFICATION

1. **`node --check`** → **PASS**.
2. **jsdom WITHOUT `runScripts`** → **31 body children** (healthy; unchanged).
3. **Boot assertions (`window._S10`)** → **31/31 PASS** (28 + the 3 new D164 guards) on **Free × Basic ×
   notes-OFF × notes-ON**. **0 console errors** in all four quadrants.
4. **NEGATIVE CONTROLS — 12 guards, every one BITES** (each sabotage → the guard returns `false`):

   | # | Sabotage | Guard | Result |
   |---|---|---|---|
   | NC1 | Put a **textarea** back on the readout | `_assertReadoutUsesArtifactEditor` | **BITES** |
   | NC2 | Wire the **reanalysis commit** into the readout edit path | `_assertReadoutEditorProducesNothing` | **BITES** |
   | NC3 | Forget to **restore the editor host** on close | `_assertReadoutEditorRestoresHost` | **BITES** |
   | NC4 | **Gate readout editing on Free** — via the NEW `onRptInput` path | `_assertEditFreeOnEveryTier` | **BITES** |
   | NC5 | Let **the editor** write the PM's words (`onRptInput` → `RPT_EDITS`) | `_assertOsloNeverRewritesPMProse` | **BITES** |
   | NC6 | Strip the **tier name** from the UP-REPORT prompt | `_assertNoGenericUpgradeCopy` (MON-04) | **BITES** |
   | NC7 | **Disable** the readout Export button | `_assertNoDisabledLimitAffordances` (D138) | **BITES** |
   | NC8 | Put **OSLO vocabulary** back in the memo body | `_assertNoOsloVocabularyInReport` (D149) | **BITES** |
   | NC9 | Let the **recipient change the READ** | `_assertAskTailoredNeverTheRead` (D145) | **BITES** |
   | NC10 | Make `genReport()` **run an analysis** | `_assertReportPackagesNeverProduces` (D146) | **BITES** |
   | NC11 | Force the **recommendation row shut** at the cap | `_assertRecommendationNeverHidden` (§7d) | **BITES** |
   | NC12 | **Delete the recommendation** at the cap | `_assertRecommendationNeverHidden` (§7d) | **BITES** |

   **NC4 and NC5 are the important ones:** they sabotage the **new** code (`onRptInput`), and they only bite because
   four existing guards had their **source lists extended** when the surface grew. Left at their old lists they would
   have passed **vacuously** — the exact failure that has now bitten twice (the D160 export-drawer loophole; the
   D162b recommendation-row loophole).
5. **The surface table** — above. **Every surface inside budget.**
6. **Behavioural — 32/32 PASS, 0 console errors:**
   - **(a)** the Basic/report prompt is **27 words** and still names the limit (`Limit — Your branding`), the tier
     (`Basic`) and **3 resolutions**; no banned sentence remains.
   - **(b)** the share dialog keeps the honest facts (invite cost · seat count · Viewers take no seat · asking is
     free) and **drops the explanations**; CRR keeps *costs nothing · no invite · no seat · scoped · expires* and
     drops *"the seed of the loop"*.
   - **(c)** the Readout is **WYSIWYG on the artifact editor** — contenteditable `.doc`, **0 textareas**, host flips
     to `rptEd`, **undo restores · redo re-applies · slash menu opens · find bar opens · formatting applies** — and
     **formatting runs NO analysis** (governor unchanged) with **no provenance chips leaked** into the memo.
   - **(d)** PM sections render **byte-verbatim**, and the PM's **markup survives** (`<b>chase The Grid</b>`).
   - **(e)** a recipient change moves **only** `data-sec="decisions"` — §1–§5 + appendix byte-identical.
   - **(f)** editing is free on **both** tiers; the tier lives **only** in `_editsPersist()`.
   - **(g)** **Slices 1–9 + the rest of Slice 10 non-regression:** activation → intake → fast pass → overview →
     attention → all 7 artifacts (editor: undo/redo/find/slash + table provenance still attach) → issues + panel +
     apply → history → workspace/settings/notifications → chat → share/export/CRR/reviewer view → access/waitlist/
     plans → tier flip → every UP prompt → every demo trigger → the readout edited on **all 7 sections** → the
     artifact editor still drives `#artdoc` afterwards → notes ON/OFF. **23/23 steps OK · 0 console errors ·
     boot self-check green at the end.**

## TENSIONS — escalated, not invented

- **O-D163-1** — **the ≤60 modal budget cannot apply to a surface that is a table of rows** (Plans · Limits ·
  Settings · Access). Applied structurally: **prose ≤60, every row ≤8, every helper ≤20.** Confirm the rule.
- **O-D163-2** — **where the ≤30 prompt budget is measured.** This build counts title + body + label + buttons and
  holds the `Limit — <x>` eyebrow to the ≤8 label budget separately. If the eyebrow is meant to be *inside* the 30,
  four prompts need ~3 words trimmed.
- **O-D163-3** — the **export disclaimer (34w) is ratified canon, verbatim.** Exempt from the budget. Cutting it is a
  canon change, not a copy edit.
- **O-D163-4** — the **demo bar** is prototype scaffolding on a product surface. Swept to budget; arguably belongs
  behind the notes toggle entirely. **Owner call.**
- **O-D164-1** — **table controls are not attached in the readout** (the §6 decisions table is text-editable, but no
  row/column ops and no per-cell provenance — the provenance chips would breach D149). If full table editing is
  wanted, the provenance layer must be separated from the table layer first.
- **O-D164-2** — **undo/redo is per SECTION**, exactly as it is per artifact. A PM may expect one history for "the
  readout".
- **O-D164-3** — **no autosave in the readout** (autosave would drag the versioning/reanalysis chain in behind it).
  Save is explicit; an unsaved draft shows **"Unsaved"**.
- **O-D164-4** — **`_rptCleanHTML()`** strips editor chrome on save. It removes nodes OSLO put there and touches
  nothing the PM typed (proven byte-for-byte), but *OSLO touching the PM's markup at all* deserves an owner's eye.

## Docs updated
`frontend-ui.md` · `user-experience.md` · `product-detail.md` · `success-criteria.md` · `workflow.md` (all carry the
D163/D164 amendment header) · `edge-cases.md` (**E-D163-1…9 · E-D164-1…10 · E-FIX-1**) · `open-items.md`
(**O-D163-1…4 · O-D164-1…4**).

---

# ⬛ D165 — OSLO Chat: a CONVERSATION, not a wall (2026-07-12)

## The word-count delta

| | Before | After |
|---|---:|---:|
| **OSLO's opening reply on an issue (prose body)** | **302** | **33** |
| Same, including the single action + the handoff chips | 307 | 45 |
| Evidence cards pushed into the opening | 2 | **0** (pulled) |
| Action cards in the opening | 4 | **1** |
| Action subtitles (`.ca-cons`) | 4 | **0** |
| Reliability paragraphs / epistemic blocks | 2 + 1 chip | **1 line** |
| Clarification textareas resident | 1 (open) | **0** (collapsed, one click away) |
| Suggestion sets on screen at once | **2** (3 in-message + 3 composer) | **1** |

**−89% on the opening turn. Nothing honest was deleted — it was moved one question away.**

The four pull turns, each one idea, each ending in a handoff:
`What's it resting on?` **31w** → the sources · `What are my options?` **25w** → the 3 routes ·
`What would you do?` **20w** → the recommendation + `Apply this fix →` · `How sure are you?` **27w** → Coverage ·
Evidence · How assessable.

## Verification

1. **`node --check`** → **PASS** (extracted script block, 934,238 bytes).
2. **jsdom WITHOUT `runScripts`** → **31 body children** (healthy; unchanged).
3. **Boot assertions (`window._S10`)** → **37/37 PASS** on **Free × Basic × notes-OFF × notes-ON** (4/4 configs),
   **0 console errors**. (31 → **37**: six new D165 guards.)
4. **Non-regression smoke, Slices 1–10** — every view, artifact editor, issue flow (`selectPath`, `applyFix`),
   attention cell, review request, History, limits, plans, export, all six `askOslo` context types, 16 chat intents,
   thread persist/restore → **0 console errors** on both tiers, all guards still green.
5. **Behavioural (a)–(h)** — all confirmed; see below.

## Negative controls — **10 injected regressions across 6 guards. All 10 BITE.**

| Injected regression | Guard | Result |
|---|---|---|
| Re-push the evidence cards into the opening | `chatOpeningShort` | ✅ fails |
| Restore the 4 action cards + subtitles | `chatOpeningShort` | ✅ fails |
| Drop the handoff chips from the opening | `chatOpeningShort` | ✅ fails |
| Composer chips stay visible once underway | `chatOneChipSet` | ✅ fails |
| Composer chips suppressed **always** (mirror failure) | `chatOneChipSet` | ✅ fails |
| Clarification form ships **expanded** | `chatClarCollapsed` | ✅ fails |
| A reply quietly resolves the issue | `chatNeverMutates` | ✅ fails |
| Evidence turn returns no sources | `chatDetailPullable` | ✅ fails |
| Reliability turn drops Coverage/Evidence/Assessability | `chatDetailPullable` | ✅ fails |
| Chat answers via a side channel (bypasses `_submitClarification`) | `chatClarSamePath` | ✅ fails |

### ⚠️ A VACUOUS GUARD WAS CAUGHT — BY ITS OWN NEGATIVE CONTROL
`_assertChatDetailIsPullable()` originally checked the reliability turn for the bare word `rb.coverage` — *"Moderate"*.
But the reliability **qualifier sentence already contains "Moderate"** (*"Reliability is Moderate — …"*), so **deleting
the entire basis still passed.** The negative control exposed it; the guard now requires the **labelled pairs**
(`Coverage Moderate` · `Evidence Moderate` · `How assessable Moderate`), which only the basis can produce. It now bites.
**This is the fourth vacuous guard in this prototype. The negative controls are not optional.**

Two further guards were built to *avoid* the same trap up front: `chatOneChipSet` carries a **mechanism proof** (it
drives the real `renderChatChips()` through both states) because the chat rail is **not seeded at boot** — the naive
live-DOM-only form of that guard passed for free. `chatNeverMutates` is a **state proof**, not a copy scan.

## Behavioural results
- **(a)** Opening reply: **33 words**, ends with 3 chips. ✅
- **(b)** Evidence / options / recommendation / reliability arrive **only when asked**, one per turn, each handing off. ✅
- **(c)** Composer chips: **5 at the empty state → 0 once underway.** Never two sets. ✅
- **(d)** A new context inserts a **visible `.chat-div` divider**; a repeat of the same context does **not**. ✅
- **(e)** Clarification: `open=false`, computed `display:none`, expands on click. ✅
- **(f)** Advisory-only: 12-question battery incl. *"Apply the fix for me"*, *"Close ISS-01"*, *"Select the first
  path"*, *"Upgrade me to Basic"* — **whole-model snapshot identical before and after.** ✅
- **(g)** Chat-answered clarification → History entry **byte-identical** to the panel path (both diffed):
  `{"type":"clarification","lab":"Clarification answered — Venue Wi-Fi capacity is unconfirmed","d":"You answered
  OSLO's question about Resources. Project information updated · ISS-01 → Addressed."}` ✅
- **(h)** Slices 1–9 + rest of Slice 10 non-regression: **0 console errors.** ✅

## Escalations — NOT invented (see `open-items.md`)
- **O-D165-1** — D165a ("the opening contains **only** 1-2-3") vs D165e ("the clarification form **collapses**").
  Built: the form is **not** resident; the opening's third chip is **"Answer your question"** and the collapsed prompt
  arrives in its own turn. **Owner decision required:** is a chip sufficient surfacing for an open OSLO question?
- **O-D165-2** — D165a's literal list allows **zero** actions in the opening; D165b and D162b both say **ONE**.
  Built: **one** (`Open this issue →`), consistent with the panel. **Owner confirmation required** — reverting is one
  line plus one assertion.
- **O-D165-3** — **D163 has no word-budget row for a chat turn.** The opening is now guarded at a hard ceiling of 55
  (observed 33); **no other turn is budget-enforced**, because no budget exists to enforce. **Owner: add the row.**
- **O-D165-4** — cosmetic: with prototype-notes **ON**, the `pn()` canon block renders below the handoff chips in the
  tier answers. Flagged, not silently reordered.

## Docs updated
`frontend-ui.md` · `user-experience.md` · `product-detail.md` · `workflow.md` · `success-criteria.md`
(all carry the D165 amendment header) · `edge-cases.md` (**E-D165-1…14**) · `open-items.md` (**O-D165-1…4**).

---

# D167 + D166 — the chat O-D closures, and the GUARD AUDIT (2026-07-12)

**Target:** `vertical-slices/slice-10-tiering-limits/prototype.html` (15,942 lines). **No behavioural regressions.**

## TASK 1 — D167: the chat O-D closures

### 1a (O-D165-1) — the clarification prompt stays VISIBLE in the opening turn, COLLAPSED
**The owner's reasoning, recorded because it is the durable part:** *a chip is enough surfacing for **detail** — but a
question OSLO needs answered is not detail, it is a **REQUEST**. Hiding a request one click deep means a **blocked issue
can sit unanswered because the ask was never seen.***

**Built:** `_ansIssue()` now emits `_chatClarBlock(id)` when the issue carries an **outstanding** clarification —
a **one-line collapsed prompt**, `❓ <question, truncated to 10 words>… ▸`, expanding to the input on click
(D162c/D165e). **The textarea is NOT re-opened.** The *"Answer your question"* chip **remains, as a shortcut**.

- **Nothing is lost to truncation.** The **full** question is the first line inside the body (`.cc-q`, new) and the
  head's `title=`. Truncation is presentation; the ask is intact.
- **Not re-surfaced once answered** (`st !== 'addressed'`). Re-prompting for an answer already given is nagging.
- ⚠️ **A hazard this introduced, and closed.** The opening turn now has a side effect (`_retireClarBoxes`) — and the
  guards **generate real opening turns for every issue at boot**. Un-fenced, a guard would have **disabled a live
  answer box the user was about to type into.** Generation is now fenced behind **`_CHAT_PROBE`** (`_chatProbeHTML`),
  and **`chatNeverMutates` now snapshots `_CHAT_MSGS` and the thread's `innerHTML`** — so "computing a reply changes
  the conversation" is now a *failing* condition, not an unnoticed one.

### 1b (O-D165-2) — ONE action. **Confirmed as built. No change.**

### 1c (O-D165-3) — chat word budgets, ENFORCED

| Surface | Budget | **Measured** |
|---|---|---|
| **Chat — opening turn** | **≤ 50** | **27 · 31 · 32 · 41 · 43 · 45** (max **ISS-02 = 45**) |
| **Chat — pull turn** — evidence · options · recommendation · reliability | **≤ 40** | **31 · 25 · 20 · 27** |
| *(same budget, same class of turn)* — tier answers | ≤ 40 | Basic **36** · never-limited **33** · which-limit **21** · my-plan **31** |

`CHAT_OPENING_WORD_BUDGET` **55 → 50**; new `CHAT_PULL_WORD_BUDGET = 40`. Two guards: `chatOpeningShort` ·
**`chatPullShort`** (new). **Identical counts with prototype notes ON and OFF.**

> ⚠️ **INTERPRETATION DECLARED (not invented).** D167's table names four pull turns. The **Slice-10 tier answers** are
> pull turns *by the same mechanism* — they arrive only when asked — so the build holds them to the **same** budget.
> All four already fit. **If the owner intends the 40 to bind only the four named turns, delete them from
> `CHAT_PULL_TURNS` — one line.**
>
> ⚠️ **One copy change fell out of it.** *"What does Basic add?"* measured **43**. The overrun was its second sentence
> — *"I run the same models for everyone."* — which **restates the sentence before it** *and* **explains why we do
> something**: **both banned outright by D163**. **Cut, not re-worded.** The claim — *"No plan gives you a better
> read."* — stands, once. **36 words.**

### 1d (O-D165-4) — `pn()` moved ABOVE the handoff chips
Both tier answers now emit `_cActs → pn → _hand`. **The handoff is the last thing in a turn** — it carries the
conversation forward, and a governance rail wedged between the answer and its next moves buries them. Verified with
notes ON: `chat-acts → pn → chat-follow`.

---

## TASK 2 — D166: THE GUARD AUDIT

**39 guards · 53 negative controls · 4 VACUOUS guards found and fixed · all 53 now bite.**
**The doctrine did not move. Only the guards did.**

### The four vacuous guards (each was passing while the thing it protected could be broken)

| Guard | The vacuity | The fix |
|---|---|---|
| **`d138`** *(no limit-bearing affordance disabled)* | ⛔ **The exemption swallowed the subject.** `el.disabled && !el.dataset.validation` — and **`#shareInviteBtn` carries `data-validation="email"` STATICALLY IN THE MARKUP.** The expression was **always false for it**. **A seat cap could have disabled the single most likely control in the product (UP-SEAT) and D138 would have reported green forever.** | Exemption now conditioned on the **LIVE INPUT STATE** (`_validationExcusesDisable()`). Validation may disable Send **only while the form is actually invalid**; a **valid** address with a dead button can only be a limit. An **unknown** `data-validation` value excuses **nothing**. |
| **`noteNeverBlocks`** *(the forecast note never blocks the send)* | ⛔ **The export-drawer trap (D166 §1), reintroduced one guard later.** It filtered `.rpt-act .btn` for disabled controls — but under **D160 those live in a drawer CLOSED BY DEFAULT**, so the list was **empty**. **The note could have disabled every send control in the product.** | Grades the **permanent toolbar entry point** (`#rptExportBtn`) plus any open drawer controls — **and FAILS if it finds nothing to grade.** |
| **`budgetInAnalyses`** *(the budget is in analyses, never tokens)* | ⛔ **`#meterBox` does not exist until the Limits surface is rendered.** At boot the DOM half graded **nothing** and passed for free. | Now a **MECHANISM proof**: renders the **real** meters via the **real** `renderMeters()` into a **detached host** and grades the output. Cannot be dodged by never opening the surface; **fails if the meter renders empty.** |
| **`_copyViolations`** *(the shared scanner: `noTierQuality` · `noLatencyLever` · `noOutcomePricing` · `reportsNoHealth`)* | ⛔ **Silent coverage rot.** `if(!el) return;` skipped a **missing** surface **without a word**. Rename all seven and **every copy prohibition passes on an empty set, forever.** **D160 already renamed the Reports surfaces once.** | `_copyScan()` returns the surfaces it **could not find**; every caller **FAILS** on a missing one. **EMPTY is legal (a closed drawer). ABSENT is not.** |

### Latent vacuities closed in the same pass
- **Seven report guards** opened with `if(!doc || !doc.innerHTML.trim()) return true;` — *"I could not find the
  document, so everything is fine."* **A missing subject is a failure to verify, not a pass.** They now route through
  **`_rptDocOrFail()`** and return **`false`**.
- **`_probeWords` stripped `.pnote` — a class that does not exist** (the real one is `.pn`). With notes **ON**, a
  36-word tier answer measured **234 words** and the budget guard fired **on the governance rail**. **Prototype notes
  are review apparatus (D161), never product copy.** One helper — **`_productText()`** — now defines what a guard may
  grade: **what the USER sees.**

### THE GUARD-AUDIT TABLE — all 39 guards

*Type: **S** = state proof · **M** = mechanism proof · **D** = DOM/copy scan.*

| # | Guard | Type | Negative control (the regression injected) | Result |
|---|---|---|---|---|
| 1 | `d138` | D→**M** | seat cap disables **Invite** while the address is **VALID** | **BITES** *(was **VACUOUS** — fixed)* |
| 1b | `d138` | M | remove `#rptExportBtn` from the toolbar (limit action unreachable) | **BITES** |
| 1c | `d138` | — | **CONTROL, must NOT bite:** Invite disabled on an **empty** address (validation, not a limit) | **correctly silent** |
| 2 | `mon04` | S | strip the relieving tier from every friction prompt | **BITES** |
| 3 | `tbd` | S | invent a number for an owner-TBD (`crr.cap = 5`) | **BITES** |
| 3b | `tbd` | S | reinstate a RETIRED limit (`chat.free` → RATIFIED) | **BITES** |
| 4 | `record` | S | cap the epistemic record (`artifacts = 50`) | **BITES** |
| 5 | `cr2` | M | gate an **evidence-driven** re-read behind the governor | **BITES** |
| 6 | `nofreebuy` | S | make Free overage-eligible (a Free purchase path) | **BITES** |
| 7 | `seats` | S | mark the un-ratified seat cap **RATIFIED** | **BITES** |
| 8 | `viewers` | M | make the seat cap block a **Viewer** | **BITES** |
| 9 | `noTierQuality` | S+D | tier-keyed model-quality copy on a selling surface | **BITES** |
| 9b | `noTierQuality` | D→**M** | **rename a selling surface** (coverage rot) | **BITES** *(scanner was **VACUOUS** — fixed)* |
| 10 | `budgetInAnalyses` | D→**M** | render the monthly limit in **tokens** | **BITES** *(was **VACUOUS** — fixed)* |
| 10b | `budgetInAnalyses` | M | put a token figure on the **usage meter itself** | **BITES** |
| 11 | `chatUncapped` | M | put a cap back on chat | **BITES** |
| 12 | `recNeverHidden` | D+S | **hide** the recommendation while the assisted-apply cap is hit | **BITES** |
| 12b | `recNeverHidden` | D | **collapse** the recommendation into a **closed** disclosure row at the cap | **BITES** |
| 12c | `recNeverHidden` | M | remove the free **manual-edit** resolution at the cap | **BITES** |
| 12d | `recNeverHidden` | S | invent an assisted-apply threshold for Free | **BITES** |
| 13 | `updateNowFree` | M | gate **"Update now"** by tier | **BITES** |
| 14 | `noLatencyLever` | S+D | sell a **priority queue** on a selling surface | **BITES** |
| 15 | `downgradeKeepsRead` | S | drop **History** off the never-taken list | **BITES** |
| 16 | `noOutcomePricing` | S+D | **outcome pricing** copy on a selling surface | **BITES** |
| 17 | `reportsNoHealth` | D | frame the readout as a **health rating** | **BITES** |
| 17b | `reportsNoHealth` | D | **remove `#rptDoc` entirely** (the classic vacuity) | **BITES** *(previously returned `true`)* |
| 18 | `rptStructure` | D | put the **assumptions before the risks** | **BITES** |
| 18b | `rptStructure` | D | delete the **currency marker** from the body | **BITES** |
| 19 | `rptNoOsloWords` | D | OSLO vocabulary in an OSLO-authored section | **BITES** |
| 20 | `rptNoForecast` | D | forecast language in an OSLO-authored section | **BITES** |
| 21 | `rptPlanIsPMs` | D | rewrite the plan of action **out of the first person** | **BITES** |
| 22 | `rptDiscOnPackage` | D | strip the disclaimer **off the package wrapper** | **BITES** |
| 22b | `rptDiscOnPackage` | D | move the disclaimer **into the memo body** | **BITES** |
| 23 | `rptEditFree` | M | gate editing on **Free** | **BITES** |
| 23b | `rptEditFree` | M | wire an **upgrade prompt** into the edit path | **BITES** |
| 24 | `askNotRead` | M+S | let the **risks** section see the recipient | **BITES** |
| 25 | `noteNeverBlocks` | M | let the **send path** consult the forecast note | **BITES** |
| 25b | `noteNeverBlocks` | D→**M** | **disable the export control** while a note is showing | **BITES** *(was **VACUOUS** — fixed)* |
| 25c | `noteNeverBlocks` | D | remove the **dismiss** control from the note | **BITES** |
| 26 | `neverRewritesPM` | M+D | let `renderReports` **rewrite the PM's stored words** | **BITES** |
| 27 | `rptPackagesOnly` | M | **run an analysis** while building the memo | **BITES** |
| 28 | `schedRechecks` | M | stop the scheduled readout **re-checking currency** | **BITES** |
| 29 | `rptIsWysiwyg` | M+D | go back to a **textarea** for readout editing | **BITES** |
| 30 | `rptEditProducesNothing` | M | stop the commit path **branching on the editor host** | **BITES** |
| 31 | `rptHostRestored` | M+S | leave the editor host pointed at a **dead readout node** | **BITES** |
| 32 | `chatOpeningShort` | M | pad an issue's `why` **first sentence** into a wall | **BITES** |
| 32b | `chatOpeningShort` | M | push the **evidence cards** back into the opening turn | **BITES** |
| 32c | `chatOpeningShort` | M | restore the **4-action stack** in the opening turn | **BITES** |
| 33 | `chatDetailPullable` | M | **delete the reliability BASIS** from the pull turn | **BITES** |
| 34 | `chatOneChipSet` | M | keep composer chips up once a conversation is underway | **BITES** |
| 35 | `chatClarCollapsed` | M+D | ship the clarification form **EXPANDED** | **BITES** |
| 36 | `chatNeverMutates` | **S** | let a chat answer **select a resolution path** | **BITES** |
| 36b | `chatNeverMutates` | **S** | let computing a reply **touch the live thread** | **BITES** *(new dimension — D167)* |
| 37 | `chatClarSamePath` | M | answer a clarification through a **side channel** | **BITES** |
| 38 | **`chatOpeningCarriesAsk`** *(new)* | M | **drop the request** from the opening turn (chip only) | **BITES** |
| 38b | **`chatOpeningCarriesAsk`** *(new)* | M | drop the **"Answer your question" chip** shortcut | **BITES** |
| 39 | **`chatPullShort`** *(new)* | M | let a pull turn **grow back into a wall** | **BITES** |
| — | `_assertNoEvictionOnDowngrade` *(not in `_S10`; runs on the downgrade path)* | **S** | **evict a Membership** on downgrade | **BITES** *(and restores the roster)* |

**Load-bearing guards, all with a biting control:** CR-2 evidence never metered (5) · the epistemic record never
metered (4) · recommendation never hidden (12·12b·12c·12d) · editing free on every tier (23·23b) · chat never mutates
(36·36b) · tailor-the-ask-never-the-read (24) · report packages-never-produces (27) · no tier-keyed judgment quality
(9·9b) · no outcome pricing (16) · "Update now" free on every tier (13) · downgrade never removes the read (15) ·
no eviction on downgrade (—).

---

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted `<script>` | **PASS** |
| 2 | jsdom **without** `runScripts` → body children | **31** — unchanged |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **39/39 pass, all four combinations. 0 console errors.** |
| 4 | **Guard audit** — 53 negative controls | **All 53 bite** (+1 deliberate non-bite control, correctly silent) |
| 5 | Chat word counts — opening (≤50) / pull (≤40) | **openings 27–45 · pulls 20–36.** Identical with notes ON. |
| 6a | Opening turn shows a **collapsed** prompt, no open textarea | `open=false` · `.cc-body` computed `display:none` · **1** action |
| 6b | It **expands on click** | `open=true` · `display:block` · full question + textarea present |
| 6c | Chip shortcut still works | handoff = *What's it resting on? / What are my options? / **Answer your question*** |
| 6d | Chat-answered clarification → History | **BYTE-IDENTICAL** to the panel path (both paths diffed) |
| 6e | Composer chips vanish once underway | composer **0** · in-message **3** — **never both** |
| 6f | Chat never mutates | `chatNeverMutates` **true** — now including the thread itself |
| 6g | Slices 1–9 + rest of Slice 10 | **22-step smoke** (every view · issue panel · artifact · chat · limits · plans · tier switch · reports · notes toggle) — **all ok, 0 console errors**, 39/39 guards still green afterwards |

## Escalations — none invented, one interpretation declared
1. **`CHAT_PULL_TURNS` includes the Slice-10 tier answers.** D167 names four pull turns; the tier answers are pull
   turns by the same mechanism. **Declared, not silent** — one line to revert if the owner intends otherwise.
2. **The *"I run the same models for everyone."* sentence was CUT** from the Basic answer (D163: a restatement **and**
   an explanation of why — both banned). The **claim** is untouched.
3. **No doctrine was changed. Four guards were.** Every fix in this pass makes a guard **more** able to fail.

## Docs updated
`frontend-ui.md` (guard table + the three new helpers) · `edge-cases.md` (**E-D167-1…7** + the **D166 guard-audit**
findings) · `open-items.md` (**O-D165-1…4 all CLOSED**, with the owner's ruling recorded) ·
`e2e-test-scenarios.md` (**T10-E-38/39/40**; assertion count 28 → **39**).

---

# D164 — **COMPLETION.** The Readout composer now matches the artifact composer. (2026-07-12)

> **Owner:** *"The Readout composer matching artifact composer doesn't appear to be completed."* **Correct.**

## THE DIAGNOSIS (confirmed)

**The PLUMBING was shared. The MODEL was not.**

| | Artifact (`#artdoc`) | Readout (`#rptEd`) — **as shipped** |
|---|---|---|
| Editing model | **ONE continuous document. Click anywhere, type.** | **Per-section EDIT MODE** — enter, edit, close |
| Chrome | full editor bar | a mini-bar + an "Editing" chip + Save/Cancel |
| Slash menu | wired | **hard-coded `#artdoc`** in shared paths |

Undo/redo and find already routed correctly. **The user-facing model was the defect.**

## WHAT WAS BUILT

**1. ONE continuous, always-editable document.** `#rptEd` is a single contenteditable `.doc` holding every section.
**Deleted: `editReportSection` · `saveReportSection` · `cancelReportEdit` · `_rptEdClose` · `_rptEditing` · the
Save/Cancel row · the "Editing" chip · the `.m-edit` button · the `.m-ed-*` CSS.** Sections stay **structural blocks**
(`data-sec`), not edit targets.

**2. The same editor chrome.** The four artifact-bar actions (`artUndo` · `artRedo` · `_insertBlockFromButton` ·
`openFind`) now sit in the **readout toolbar** — resident, not modal, because there is no mode to enter (D160 keeps
them off the reading surface). One undo stack for the whole document (`_edKey() === 'rpt'`).

**3. The host indirection, completed.** Added **`_edSel()`** (scoped selectors), **`_edContainerOf()` /
`_edContainers()`** (the block container), **`_edSyncHost()`** (the host follows the **VIEW**, since there is no mode
to leave). The **block model** now scopes to the enclosing section, so grips, drag-reorder, keyboard move and block
insert all work in the memo — and a block can never be dragged across D150's fixed structure or out of OSLO's prose
into the PM's.

**4. Ownership tracks the TEXT.** `_rptCommit()` (debounced ~900ms + on blur) reads each section out of the live DOM,
compares it to OSLO's live seed through the **same normaliser**, and sets `data-pm="1"` **on divergence** — **in
place, without re-rendering**, so the caret never moves. Type a section back to OSLO's wording and it stops being the
PM's. **Autosave. No Save button. No analysis.**

## CAPABILITY TABLE — every artifact-editor capability × does it work in the readout?

*(Exercised live in jsdom, not asserted — `caps.js`, 26/26.)*

| Capability | Readout? | Notes |
|---|---|---|
| Rich text (live HTML: `b` · lists · tables) | **YES** | bold/lists/the decisions table survive editing |
| Selection toolbar + formatting (`rtExec`, ⌘B/I/U) | **YES** | `_rtInDoc()` → `_edDoc()`; pushes undo; marks dirty |
| Slash menu ("/") | **YES** | **and it now suppresses inside a readout table cell** — the seam |
| Block insert (slash / toolbar ＋) | **YES** | lands **inside the section**, never at the document root |
| Markdown shortcuts (`# `, `- `, `> ` …) | **YES** | `_mdActiveBlock()` → `_edSel()` |
| Undo / redo | **YES** | one stack for the whole document |
| Find / replace (⌘F) | **YES** | 27 live matches; `_FIND_SKIP` now also skips `.m-note` |
| Keyboard shortcuts | **YES** | ⌘Z/⌘⇧Z/⌘B/I/U/⌘F all route through `_edDoc()` |
| Paste sanitize | **YES** | intercepted; `<script>`/`onclick`/`style` stripped |
| Block grips + drag-reorder + keyboard move | **YES** | scoped to the section (see below) |
| **Tables — row add/insert/delete, column ops, row reorder** | **YES** | ⚠️ **was NO.** `attachTableControls()` un-gated |
| Link popover | **YES** | `_currentLinkAnchor()` → `_edSel('a')` |
| Empty-state / placeholder | **artifact-only** | `_refreshEmptyState()` — an empty *artifact* is a plan gap; an empty memo section is not a defect |
| **Epistemic provenance chips** | **artifact-only** | ⛔ **D149** — OSLO vocabulary in a document that forbids it |
| **Weakness stepper** | **artifact-only** | a memo has **no issues** — it packages a read, it does not produce one |
| **Artifact versioning + History** | **artifact-only** | a readout is not a plan artifact |
| **The reanalysis commit** | **artifact-only** | ⛔ **D146** — **a readout PACKAGES; it never PRODUCES** |
| Block drag **across** containers | **section-scoped** | see **O-D164-6** — crossing sections would break D150 and corrupt the authorship boundary |
| Editable section headings | **NO — furniture** | see **O-D164-5** — an artifact's `<h1>` is also outside `#artdoc`; and one heading carries a live date |

**Two capability leaks were found and fixed by this sweep, not by the guards:**
- `attachTableControls()` was gated on `_edIsArtifact()` — so a readout table had **no row/column controls at all**.
  Table **structure** is editor capability; table **provenance** is artifact semantics. Split.
- `_attestNewBlock()` was **not** gated — with the slash menu and markdown now live in the readout, it was stamping
  **"Confirmed by you"** onto every block the PM inserted into their memo. **OSLO vocabulary, in the one document
  that forbids it.** Gated, and added to the guard's semantic list.

## EVERY REMAINING `artdoc` / `#artdoc` REFERENCE IN EXECUTABLE CODE

| Where | Verdict |
|---|---|
| `let _EDIT_HOST = 'artdoc'` · `_edIsArtifact()` · `_edSyncHost()`'s `'artdoc'` | **the indirection itself** |
| `<div class="doc" id="artdoc" …>` in `openArtifact()` | **the artifact editor element** |
| `_epiOf()` — `getElementById('artdoc')` | **artifact-only + justified in code:** epistemic **provenance of a plan artifact**. D149 forbids that vocabulary in a memo. Scoped to `_curArt`. **Must never be routed through `_edDoc()`** — that would make it read the memo. |
| `curAnnos()` — `#artdoc .anno` | **artifact-only + justified in code:** the **weakness stepper**. Annotations are open **issues on a plan artifact**; a readout has none. **The hard-code IS the guarantee** — scoped to `#artdoc`, it can never find anything in a memo. |
| `commitArtEdit()` — `getElementById('artdoc')` for LS | **artifact-only + justified in code:** **artifact versioning**. The function is gated at its head by `_edIsArtifact()`; it versions, writes History and starts the reanalysis chain. **None of those may happen to a readout** (D146). |
| Guided-tour step `{sel:'#artdoc', view:'artifacts'}` | **artifact-only + justified in code:** a **coordinate on screen**, not an editor code path. |
| `_d164NegativeControls()` — `'#artdoc td'`, `getElementById('artdoc')` | **the injected regressions.** Deliberate. |

**Every other `artdoc` occurrence in the file is prose in a comment.** `_assertNoArtdocHardcodeInSharedEditorPaths()`
reads **43 shared editor functions** and fails on an `#artdoc` literal in any of them — **with comments stripped
first** (a guard that graded its own explanation would be the copy-scan failure D166 exists to end, one level up).

**Routed through `_edSel()` / `_edDoc()` / `_edContainerOf()` in this pass:** `_caretBlock` · **`_syncSlashFromInput`
(the seam the owner's brief named)** · `_mdActiveBlock` · `_topBlockOf` · `_placeBlock` · `_isTopBlock` ·
`_attachBlockGrips` · `_moveBlock` · `_wireBlockDnD` · `_insertBlockFromButton` · `findReplaceAll` ·
`_currentLinkAnchor` · `_wireA11yReveals` · `_attestBlockOf` · `attachTableControls` · `_ensureRowDel`.

## GUARDS — MECHANISM, NOT COPY (D166)

**The old `d164` guard was itself vacuous, exactly as the brief said.** It checked that `#rptEd` was *"a
contenteditable carrying the `doc` class"* — **a DOM/copy scan that passed while the per-section edit mode was still
in place.** Replaced with five mechanism proofs:

| Guard | Proves |
|---|---|
| `_assertReadoutIsOneContinuousDocument()` | **exactly one** always-editable host; **every** section inside it; **the edit-mode machinery does not EXIST**; no edit chrome; the four actions are reachable |
| `_assertReadoutEditorIsTheArtifactEditor()` | **exercises the indirection** — `_edDoc()` · `_edIsArtifact()` · `_edKey()` · `_edSel()` · `_edContainerOf()` all resolve onto `#rptEd` |
| `_assertNoArtdocHardcodeInSharedEditorPaths()` | **no `#artdoc` literal in any of 43 shared editor functions**, comments stripped |
| `_assertReadoutEditorProducesNothing()` | the choke point branches on the host; **no artifact semantics can run on the memo**; no provenance chrome in the live document |
| `_assertEditorHostFollowsTheView()` | the host is **the document on screen**, and leaving the Readout **always** gives it back |

**Three existing guards were strengthened (fix the GUARD, never the doctrine — D166 §3):**
- `_assertOsloNeverRewritesPMProse()` — the behavioural half was `sec.innerHTML.indexOf(mine) >= 0`. **Wrong twice
  over:** a substring test only ever catches *deletion*, and once the editor attached **block grips** to the live
  document it would have gone **red on a correct document** — inviting a hurried reader to loosen it. Now **byte
  equality on the extracted body**, through the exact extractor the save path uses.
- `_assertPlanOfActionIsPMVoiced()` — looked for the **"Edit" button**, which *was* the edit mode. Now proves the
  **mechanism**: the plan section is inside the one live contenteditable and the caret can reach it.
- `_assertReadoutIsOneContinuousDocument()` — **its own first draft was vacuous and the harness caught it.** It
  checked `typeof window[f] === 'function'`; a `function` declaration lands on `window`, **a `let`/`const`/arrow
  binding does not** — so `const editReportSection = () => {}` would have restored the edit mode and the guard would
  have stayed green. Now checked **lexically as well**.

## NEGATIVE CONTROLS — `_d164NegativeControls()` — **14/14 HOLD** (13 bites + 1 state proof)

| Control | Injected regression | Bites |
|---|---|---|
| `oneDocument_editModeReturns` | re-add `editReportSection` | ✅ |
| `oneDocument_sectionOutside` | lift a section out of the editable host | ✅ |
| `oneDocument_editChromeReturns` | put an `.m-edit` button back | ✅ |
| `editorIsTheArtifactEditor` | make `_edDoc()` always return `#artdoc` | ✅ |
| `noArtdocHardcode` | re-add **the exact seam**: `.closest('#artdoc td')` | ✅ |
| `editorProducesNothing` | wire the analysis commit into the readout path | ✅ |
| `hostFollowsTheView` | leave the host on the readout while the view is elsewhere | ✅ |
| `osloNeverRewritesPMProse` | let `renderReports()` write `RPT_EDITS` | ✅ |
| `osloNeverRewritesPMProse_rendered` | OSLO "softens" the PM's rendered sentence | ✅ |
| `planOfActionIsPMVoiced` | make the plan of action read-only | ✅ |
| `forecastNoteNeverBlocks` | gate the save path on the forecast note | ✅ |
| `reportPackagesNeverProduces` | wire `_meterSpend()` into `genReport()` | ✅ |
| `pmProseSurvivesEveryOsloPath` | **STATE PROOF** — PM bytes survive render + recipient change; `data-pm` set by divergence; rendered byte-verbatim | ✅ holds |

## VERIFICATION

1. **`node --check`** → **PASS**.
2. **jsdom WITHOUT `runScripts`** → **31 body children**, `#rptDoc` present, **no textarea** on the readout.
3. **Boot assertions** → **41/41 PASS** on **Free × Basic × notes-OFF × notes-ON**, **0 console errors**.
4. **Negative controls** → **14/14 hold** (13 injected regressions all bite; the state proof holds).
5. **Capability sweep** → **26/26 YES** (live jsdom, every capability exercised).
6. **Behavioural (48/48)** — one continuous document, click-and-type · formatting/slash/find/undo all live ·
   PM sections **byte-verbatim** and `data-pm="1"` **set on divergence** (and **released** on convergence) ·
   recipient change moves **only** `[data-sec="decisions"]` · **PM edits survive a recipient change** (D145 is
   invariance across **audiences**, not across edits) · editing free on **both** tiers · `genReport()` runs **no
   analysis** and spends **no meter** · the D155 note fires, is dismissible, blocks nothing, and is never stored ·
   Slices 1–9 + the rest of Slice 10 sweep clean with **0 console errors** · the artifact editor is untouched
   (provenance chips still present in `#artdoc`).

## TENSIONS ESCALATED (not invented)

- **O-D164-5 — section headings are not editable.** The one place *"click anywhere and type"* does not literally
  hold. Justified by parity (an artifact's `<h1>` is outside `#artdoc` too), by D150's guarded fixed order, and by
  the live date in the *"What's changed since ‹date›"* heading — which, frozen into the PM's saved text, would
  quietly lie. **Owner's eye requested.**
- **O-D164-6 — blocks do not drag across sections.** Doctrine-derived (D150's order; the OSLO/PM authorship
  boundary the D149/D152/D155 exemptions rest on), not convenience-derived. **Flagged.**
- **O-D164-4 — `_rptCleanHTML()` still touches the PM's markup** (to strip OSLO's own chrome). Unchanged, still
  flagged: *"OSLO touching the PM's markup at all"* is the class of thing D152/D155 forbid.

**Closed by this pass:** O-D164-1 (table controls) · O-D164-2 (per-section undo) · O-D164-3 (no autosave). All three
existed **only because the edit mode existed.**

---

# D164 (VISUAL PARITY) — the readout is **DRAWN** as an artifact is drawn
**2026-07-12 · owner-directed · surgical CSS pass · no logic, no DOM, no copy changed**

## The owner's report
> *"The readout presentation is still different from artifacts. It is contained in a grey box with padded margins
> left and right, while the artifact starts at top-left of the space. Any reason the readout can't mimic the
> visual layout of artifacts?"*

**No. There was no good reason.** It was a design instinct — *"a memo should look like a memo"* — and it
contradicted the doctrine it was shipped under.

## The diagnosis (confirmed)

**The readout was drawn as a PAPER SHEET; the artifact is drawn as a DOCUMENT YOU WRITE IN.**

D164's *plumbing* and *model* were already shared — `#rptEd` genuinely carried `.doc`, the editor host genuinely
followed the view, every structural guard was green. **The RENDERING was not shared, and no DOM guard could see
it.** Two failures, one instinct:

1. **The card.** `.memo{background:var(--surface); border:1px; border-radius:6px; padding:34px 40px 30px;
   box-shadow:0 12px 34px; max-width:760px}` — plus `:root[data-theme="light"] .memo{background:#fff}`, a **white
   sheet inside a dark-default app (D127)** — floating inside a **centring** `.rw-page{display:flex;
   justify-content:center}`. **A card says PREVIEW.** The PM does not preview a readout; they write it.
2. **The typography.** `.memo p{font-size:13px;color:var(--muted)}` tied `.doc p` on specificity and **beat it on
   source order**. The same editor rendered two different-looking documents — **invisible to every DOM guard.**

## What changed (CSS only)

| | before | after |
|---|---|---|
| `.rw-page` | `padding:34px 24px 90px; display:flex; justify-content:center` | **`padding:24px 34px 90px`** — the `.aw-center` treatment |
| `.memo` | surface + border + radius + `34px 40px 30px` padding + `0 12px 34px` shadow + `760px`; `74ch`/`56px 60px` in `.rw-page`; `#fff` in light | **`background:none; border:0; border-radius:0; box-shadow:none; padding:0; margin:0; max-width:720px`** |
| `.memo p/li/ul/ol/table/th/td`, `.memo p b` | re-declared memo typography over `.doc` | **deleted** — `.doc` governs the body |
| `.m-doc` | `max-width:none!important; margin:0!important` (only needed to escape the card) | **deleted** |
| `.memo .m-t` | `20px/700`, `24px` in `.rw-page` | **`21px/600`** — the `.art-head h1` weight |
| `.rw-notes` | `max-width:900px; margin:0 auto; padding:0 24px` | `padding:0 34px 70px; max-width:1180px` — same flush left origin |
| `@media(max-width:640px)` | `.rw-page`/`memo` had their own 760px breakpoint + card padding | `.rw-page{padding:24px 16px 90px}`, `.memo{max-width:100%}` — the **artifact's** breakpoint |

**What the memo KEEPS:** everything that makes it a memo is its **furniture, not its font size** — title · byline +
currency marker (D153) · `To:` line (D156) · rule · the seven fixed section headings (D150) · `.m-risk` · `.m-alt`
· `.m-app` · `.m-sign` · the ownership badge · the D155 gentle note. **The BODY is now byte-for-byte the artifact
editor's body.**

**⛔ UNTOUCHED, as instructed:** `#rptPkgHost` / `#rptPkg` (export metadata, D153) · the D161 notes rail
(`#reportsBody`) · all doctrine (D145 · D149 · D151 · D152 · D153 · D154 · D155 · D160 · D164 · D166).

## New guard — `_assertReadoutIsFlushLikeAnArtifact()`

**It reads the CASCADE, not the DOM** — because the defect was never in the DOM. It parses the authored `<style>`
source (comments stripped — **load-bearing**: the comments now quote the removed `background:#fff` as a record of
what went, and a guard that read them would fail on its own documentation), walks top-level **and `@media`** rules,
and proves:

- **(a)** nothing whose selector ends in `.memo` paints a card — **in either theme, at any width**;
- **(b)** `.memo`'s measure **===** `.doc`'s measure;
- **(c)** `.rw-page`'s padding **===** `.aw-center`'s padding;
- **(d)** nothing re-centres `.rw-page` (`display:flex|grid` · `justify-content` · `align-items` · `max-width` · `margin:auto`);
- **(e)** nothing scoped to `.memo`/`.m-doc` re-declares `.doc`'s typography on `p · li · ul · ol · table · th · td · h3 · blockquote`;
- **(f)** `#rptPkg` still exists and is **not** inside `#rptDoc` — removing the card cannot quietly fold the cover into the page.

**It is DERIVED, not hardcoded.** It never asserts *"720px"*. It asserts **the readout matches the artifact**.
Change the artifact's metrics and the readout is *required to follow*. **The guard cannot go stale.**
**Vacuity bar (D166 §1):** it fails loudly with CANNOT VERIFY if any of the four reference selectors is absent, if
<200 rules parse, or if `.doc`/`.aw-center` lose the value being compared against.

Registered in `_s10SelfCheck()` (`rptFlushLikeArtifact`) **and** on every `renderReports()`.

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` (1 inline script, 1,040,570 bytes) | **PASS** |
| 2 | jsdom **WITHOUT `runScripts`** | **31 body children** (healthy); `#rptDoc` · `#rptPkg` · `#rptPkgHost` · `#reportsBody` all present |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **42/42 PASS in all 4 cells · 0 console errors in all 4 cells** |
| 4 | `_d164NegativeControls()` | **22/22 hold in all 4 cells** (14 pre-existing + **8 new**) |
| 5 | Side-by-side parity table (22 rows) | **0 DIFF** — see below |
| 6 | AA contrast, **light and dark**, 15 readout tokens | **0 failures**; dark **improves** |
| 7 | Behavioural (a)–(d) | **PASS** |

**The 8 new negative controls** (each must make the guard bite): `flush_passesAsShipped` (precondition — a control
suite whose subject is already failing proves nothing) · `flush_cardReturns` · `flush_lightCardReturns` (the `#fff`
sheet specifically) · `flush_cardPaddingReturns` · `flush_centringReturns` (**injected inside an `@media` block**) ·
`flush_measureDivorcedFromDoc` · `flush_typographyDrifts` (**the one no DOM guard could ever see**) ·
`flush_refusesToGradeNothing` (the guard's own vacuity trap).

### Side-by-side: artifact pane vs readout pane

| # | Property | ARTIFACT (`.aw-center` / `.doc#artdoc`) | READOUT (`.rw-page` / `.memo#rptDoc` › `.doc#rptEd`) | verdict |
|---|---|---|---|---|
| 1 | pane container | `.aw-pane › .aw-center` | `.rw › .rw-bar + .rw-drawer + .rw-page` | **PEER — justified exception (D160)**: the readout keeps a *sticky toolbar + closed-by-default drawers* above the document, because its controls must live off the reading surface. The artifact's `.art-bar` scrolls with the document. **This is the only structural difference, and it is doctrine.** |
| 2 | pane padding (flush origin) | `24px 34px 90px` | `24px 34px 90px` | **MATCH** |
| 3 | pane flow / centring | block, no `justify-content` | block, no `justify-content` | **MATCH** |
| 4 | document node | `.doc#artdoc` | `.memo#rptDoc` › `.doc.m-doc#rptEd` | **MATCH** (same `.doc` class; `.memo` is now a transparent flush wrapper carrying only the measure, exactly as `.art-head`+`.art-bar` are furniture around `#artdoc`) |
| 5 | background | none → pane `--bg` | none → pane `--bg` | **MATCH** |
| 6 | border | none | none | **MATCH** |
| 7 | border-radius | 0 | 0 | **MATCH** |
| 8 | box-shadow | none | none | **MATCH** |
| 9 | card padding | 0 | 0 | **MATCH** |
| 10 | side margins | 0 (flush left) | 0 (flush left) | **MATCH** |
| 11 | max-width (measure) | `720px` | `720px` | **MATCH** (derived — guard asserts equality, not the literal) |
| 12 | document top offset | `margin-top:12px` | `margin-top:12px` (`#rptEd`, via `.doc`) | **MATCH** |
| 13 | outline | `none` | `none` (via `.doc`) | **MATCH** |
| 14 | block-grip gutter | `--blkgrip-w:22px` | `--blkgrip-w:22px` (via `.doc`) | **MATCH** |
| 15 | typography `<p>` | `color:var(--text); font-size:14.5px; line-height:1.8; margin:11px 0` | identical (no `.memo` override) | **MATCH** |
| 16 | typography `<li>` | `position:relative; padding-left:18px; color:var(--text); font-size:14px; line-height:1.75; margin:5px 0` | identical | **MATCH** |
| 17 | typography `<ul>` | `margin:8px 0; list-style:none; padding:0` | identical | **MATCH** |
| 18 | typography `<ol>` | `margin:8px 0; padding-left:26px; list-style:decimal` | identical | **MATCH** |
| 19 | table `<td>` | `padding:8px 10px; border-bottom:1px solid var(--border); color:var(--muted); vertical-align:top` | identical | **MATCH** |
| 20 | table `<th>` | `text-align:left; font-size:10px; uppercase; letter-spacing:.5px; color:var(--subtle); font-weight:600; padding:8px 10px; border-bottom` | identical | **MATCH** |
| 21 | table `<table>` | `width:100%; border-collapse:collapse; font-size:13px; margin:8px 0; position:relative` | identical | **MATCH** |
| 22 | light-theme card override | (none) | (none) | **MATCH** — `:root[data-theme="light"] .memo{background:#fff}` **deleted** |

**Remaining memo-only declarations (justified — document FURNITURE, not a competing type scale):** `.m-t` (title,
now matched to `.art-head h1` at 21px/600) · `.m-by` / `.m-to` (byline · currency marker · recipient — D153/D156) ·
`.m-rule` · `.memo h2` (the seven section headings — D150 structure; `.doc h3`, the heading the PM *inserts*, is
untouched and still governs) · `.m-risk` / `.m-alt` / `.m-app` / `.m-sign` / `.m-mine` / `.m-reset` / `.m-note`
(memo components with no artifact equivalent). All were nudged up to the `.doc` scale where they carry prose.

### AA contrast — the readout document (15 tokens, both themes)

| token | light (on `--bg` `#FBFAF7`) | was (on `#fff` card) | dark (on `--bg` `#111315`) | was (on `--surface`) | bar | verdict |
|---|---|---|---|---|---|---|
| `--text` — body prose 14.5px, headings, title | **15.87:1** | 16.56:1 | **16.92:1** | 15.05:1 | 4.5 | **PASS** |
| `--muted` — table cells, `To:`, `.m-alt`, `.m-app`, `.m-sign` | **7.69:1** | 8.03:1 | **9.86:1** | 8.77:1 | 4.5 | **PASS** |
| `--subtle` — byline, table headers, block grips, bullets, D155 note | **5.01:1** | 5.23:1 | **6.01:1** | 5.34:1 | 4.5 | **PASS** |
| `--cool` — *"your words"* badge | **6.02:1** | 6.28:1 | **6.89:1** | 6.13:1 | 4.5 | **PASS** |

**Dark (the default, D127) gets MORE contrast**, because the document now sits on the darker `--bg` rather than a
`--surface` card. **Light loses ≈0.2–0.7:1 and clears AA on every token with margin.** **0 failures.**

### Behavioural

- **(a) Flush.** `#rptDoc.parentElement` = `.rw-page`; `.memo` = `background:none; border:0; border-radius:0;
  box-shadow:none; padding:0; margin:0; max-width:720px`. **No card, no shadow, no side margins. Starts top-left.**
- **(b) Still edits continuously.** `#rptEd` `contenteditable="true"`, `class="doc m-doc"`, `_EDIT_HOST === 'rptEd'`
  on the Readout and `'artdoc'` on Artifacts. **7/7 sections inside `#rptEd`**, 7 headings `contenteditable="false"`.
  Typing → `onRptInput()` → `_rptCommit()` → **`RPT_EDITS` populated.** No edit mode; no Save button.
- **(c) The package wrapper is intact.** `#rptPkg` exists · **not** inside `#rptDoc` · `_assertDisclaimerOnPackage
  NotInBody()` = `true` · `#rptPkgHost.open` = **`false` at rest → `true` on the export drawer → `false` on close.**
- **(d) Non-regression.** All 8 views opened; `openArtifact()` re-checked (`#artdoc` still `.doc`, contenteditable);
  theme flipped both ways (parity guard `true` in **both**); **42/42 assertions still pass after full navigation**;
  **0 console errors across the whole smoke run.** `#reportsBody` renders **0 chars** with notes OFF (D161).

## Tension — escalated, not invented

**⚠️ I removed the `.memo .m-doc` typographic re-application, and an in-file `⛔` comment defended it.** The D164
(completion) block said: *"What is re-applied below is only the MEMO's typography, because a memo must still read
like a memo and not like a plan artifact."*

**I judged that comment to be the same instinct as the card, and the brief explicitly directed the change** (*"the
same typographic scale, spacing, hover/selection affordances and block-grip gutter"*). **My reasoning:** a memo is
a memo because of its **furniture and its structure** — the title, the byline, the currency marker, the `To:` line,
the seven fixed sections — **not because its body text is 1.5px smaller and greyer**. And the 13px/`--muted` body
was **the card's companion**: it was tuned for dense prose inside a 74ch white sheet. With the sheet gone it had no
basis, and it was also the **one thing no DOM guard could ever catch**.

**This is a judgement call on a comment that reads as doctrine, so it is flagged rather than assumed settled.** If
the owner wants the memo's smaller voice back, the revert is **one hunk** (`.memo .m-doc p/li/ul/ol` + the `.memo`
table rules) and the parity guard's check **(e)** would need to be narrowed to exempt the body scale — **the card,
the centring and the measure are independent of it and would all stand.**

**Open items unchanged:** O-D164-4 (`_rptCleanHTML()` still touches the PM's markup) and the `_memoSections()`
epistemic-boundary question remain flagged from the previous pass.

---

# D168 — REPORT vs MEMO: two objects, one lifecycle (2026-07-12)

**The owner's clarification reconciles both prior instincts.** The paper sheet was **not wrong — it was applied to
the wrong object.** The escalation carried in the last pass ("the deleted 13px `--muted` body voice") is **closed
by this decision, in the owner's direction: that voice belongs to the MEMO, not the report.**

**You edit a REPORT; what travels is a MEMO.**

## What was built

1. **The live document became `.report`** (was `.memo` — a class named for the wrong object). **D164 artifact
   parity is byte-for-byte intact and did not regress:** flush, top-left, `.doc` typography, continuous WYSIWYG,
   `.rw-page` padding === `.aw-center` padding, `.report` measure === `.doc` measure.
2. **The memo became a real object.** `#rptMemo` / `.memo`, rendered by `_renderMemo()` into the **export preview**
   (never the reading surface — D160). It gets **the card** (surface · border · 14px radius · `34px 40px 40px` ·
   drop shadow), **the reading measure** (`64ch`), and **its own quieter typographic voice** (`.memo .m-body p` —
   13px / 1.75 / `var(--muted)`). It rides on the **cover** (`#rptPkg`) with the **ratified disclaimer** (D153) and
   carries the **currency marker** in its body as plain attribution.
3. **`REPORT_SNAPSHOTS[]` are MEMOS, and a memo is immutable.** `_mkMemo()` is the single factory; `_deepFreeze()`
   freezes the memo **and its cover** at creation. A memo carries the **words** (`body`), not just metadata.
4. **The furniture is shared** (`.m-t` · `.m-by` · `.m-to` · `.m-rule` · `.m-risk` · `.m-alt` · `.m-app` ·
   `.m-sign` · `.m-sec`, de-scoped to bare selectors). Furniture is what makes a memo a memo — **not a font size
   and not a drop shadow** — so both objects carry it and neither owns it.
5. **Language swept:** `_mkMemo` names them `Memo N`; the toast is *"Memo sent as PDF — dated …"*; History reads
   *"Memo sent — a dated snapshot (PDF)"* / *"Scheduled memo sent — …"*; the memo's identity line reads *"Memo
   sent · <date> · PDF"* or *"Memo preview — what travels"*; the Sent list is clickable and opens **that memo**.
   All inside the D163 budgets. No meta, no rationale (D159).

## Table (i) — REPORT vs ARTIFACT (parity: D164, NOT regressed)

| | artifact (`#artdoc` / `.doc` in `.aw-center`) | report (`#rptEd` / `.doc` in `.rw-page`) | |
|---|---|---|---|
| pane padding | `24px 34px 90px` | `24px 34px 90px` | **MATCH** (derived by the guard, not hardcoded) |
| measure | `720px` | `720px` | **MATCH** (derived: `.report` === `.doc`) |
| card fill / border / radius / shadow / box padding | *(none declared)* | `none` / `0` / `0` / `none` / `0` | **MATCH — justified exception:** `.report` declares neutrals **explicitly** where `#artdoc` simply has none. The values are identical; the declaration exists so the cascade guard has something to read and so a regression is loud. |
| centring | `.aw-center` — block flow | `.rw-page` — block flow, no `justify-content`, no `margin:auto`, no `max-width` | **MATCH** |
| body typography | `.doc p` 14.5 / 1.8 / `--text` | governed by `.doc` — **no override exists** | **MATCH** |
| block model · grips · gutter | `.doc` (`--blkgrip-w`) | same class, same gutter | **MATCH** |
| editor (undo/redo · slash · find · tables · selection toolbar · markdown · paste) | shared via `_edDoc()` / `_EDIT_HOST` | same functions, same bar | **MATCH** |
| edit mode | none | none | **MATCH** |
| provenance chips / attestation | **artifact-only** | **absent** | **JUSTIFIED EXCEPTION** — a provenance claim is a claim about the **plan**; a report has none (D149). |
| section headings editable | `<h1>` outside `#artdoc` | `<h2>` `contenteditable="false"` | **JUSTIFIED EXCEPTION** — D150 fixes the seven sections; one heading carries a live date. (Carried as **O-D164-5**.) |
| block drag across containers | free | scoped to `[data-sec]` | **JUSTIFIED EXCEPTION** — crossing sections would corrupt the authorship boundary (**O-D164-6**). |

## Table (ii) — MEMO vs REPORT (the deliberate differences)

| | **REPORT** (`.report`) | **MEMO** (`.memo`) | why |
|---|---|---|---|
| card fill | `none` | `var(--surface)` (light: `#FFFFFF`) | **a memo is paper.** A report is the surface you type on. |
| border | `0` | `1px solid var(--border-2)` (light: `var(--border)`) | ″ |
| radius | `0` | `14px` | ″ |
| shadow | `none` | `0 12px 34px rgba(0,0,0,.30)` (light: `0 10px 28px rgba(20,26,38,.10)`) | ″ |
| box padding | `0` | `34px 40px 40px` | ″ |
| measure | `720px` — **derived from `.doc`** | `64ch` — its **own reading measure** | a memo is **read**; a report is **written in**. *(The `64ch` figure is a build choice — **O-D168-1**.)* |
| body voice | `.doc p` — 14.5px / 1.8 / `var(--text)` | **13px / 1.75 / `var(--muted)`** | **the escalation, closed.** The quieter voice belongs here. Guarded as **different from** `.doc p` (derived — change the editor and the memo must still differ). |
| heading | 13px | 12px, wider tracking | the memo's voice |
| both themes | n/a (no card) | tokens + an explicit light rule; **a literal light hex in the base cascade is a guard failure** (D127) | no white sheet in a dark app |
| editable | **yes** — always, every tier (D154) | **no** — `contenteditable="false"` | a memo has left OSLO |
| chrome (gentle note · "your words" · Reset · grips) | **yes** | **none — stripped at capture** | chrome does not travel |
| cover · disclaimer | **no** (D153 — out of the prose) | **yes** — `#rptPkg`, ratified text verbatim | the disclaimer is a property of the **package** |
| currency marker | in the body (`.m-by`) | in the body (`.m-by`) — **frozen** | plain attribution, both places (D153) |
| mutability | tracks the read | **deep-frozen.** Byte-identical after the report is edited **and** an analysis re-runs. What changes is its **label** (*"previous analysis"*), never its words. | D146 · D168 §3 |

## Guards — mechanism, not copy (D166)

**Added:** `_assertMemoIsPaper()` (reads the **authored cascade** — the mechanism that caught the last invisible
defect) · `_assertMemoIsImmutable()` (freeze + source-read: **no render path may write `REPORT_SNAPSHOTS[]`**) ·
`_assertReportAndMemoAreNotConfused()` (mechanism + a **narrowly scoped** naming check) · **`_d168StateProof()`**
(the state proof: **cut a memo · edit the report · re-run an analysis · assert byte-identical**).

**Kept:** `_assertReadoutIsFlushLikeAnArtifact()` **still derives its expectations from `.doc` / `.aw-center`** —
and it now **pins its subject**: `#rptDoc` must wear `.report` and must **not** wear `.memo`. It grades the
**report**; the memo is *supposed* to have a card, and the guard says so out loud.

**Negative controls: 40 in the suite, 40 bite (or hold, for the two proofs). Zero vacuous.**
New: `memo_paperStripped` · `memo_whiteCardInDarkApp` · `memo_voiceDeleted` · `memo_voiceEqualsEditorVoice` ·
`memo_leaksOntoTheReport` · `memo_becomesEditable` · `report_wearsTheMemosClass` · `naming_liveDocumentCalledAMemo`
· `naming_sentArtifactCalledAReport` · `naming_memosNamedSnapshots` · **`naming_pmMayWriteTheWordMemo`** ·
`immutable_unfrozenMemo` · `immutable_shallowFreezeOnly` · `immutable_renderPathWritesMemos` ·
**`memoNeverMovesWhenTheReportDoes`**.

### ⚠️ A guard was fixed, never the doctrine (D166 §3)

The first draft of the naming guard scanned **the whole rendered memo** for the word *"report"*. It went red
immediately — on **"Badge printing, the booth kit, and *the report the sponsors are owed*."** That is a **true
sentence about the project**, and the guard was **policing the document's prose**. Prose is the user's (D152/D155):
a PM may write *"I'll send a memo to legal"* and OSLO has **no business** correcting them. **The naming rule is
about OSLO's names for OSLO's objects, not about English.** The guard now grades: the memo's **identity line**,
`_mkMemo()`'s **source** (so a closed drawer cannot make it vacuous — that is exactly how the export-drawer guard
went vacuous), and **OSLO's own seeded sections** only. `data-pm="1"` is exempt — and
**`naming_pmMayWriteTheWordMemo` is a control that proves the guard does NOT bite** on the PM's own words.

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | **PASS** |
| 2 | jsdom **without `runScripts`** | **31 body children** — healthy |
| 3 | Boot assertions × **Free/Basic × notes OFF/ON** | **45/45 pass, all four combinations, 0 console errors** |
| 4 | Negative controls | **40/40 bite or hold** |
| 5 | Parity tables | above — every row **MATCH** or a **justified exception** |
| 6 | **AA contrast, both themes, both surfaces** | **18/18 pass.** Worst case **5.01:1** (report byline, light). Memo body prose **8.77:1** dark / **8.03:1** light. |
| 7a | live report flush + continuously editable | `#rptDoc.report`, `#rptEd.doc`, 7 sections, one host, 4 toolbar editor actions, **no edit mode** |
| 7b | export produces a memo with paper + cover + disclaimer | `MEMO-1` / *"Memo 1"*; card; cover carries the disclaimer; **disclaimer NOT in the memo body**; currency marker in the body; **not on the reading surface** |
| 7c | **the memo is immutable** | report edited **and** analysis re-run → **byte-identical**. Report reads *"Rewritten AFTER the memo was sent"*; the memo still reads its original summary. Direct write rejected (deep-frozen). Label flips to **"previous analysis"** — the words do not. |
| 7d | naming | no surface calls the live document a memo or the snapshot a report; the PM may still write either word |
| 7e | **generating a memo runs NO analysis** | TREND `1 → 1` · governor unchanged · meter unchanged · confidence `58 → 58` |
| 7f | Slices 1–9 + rest of Slice 10 | every view renders; **45/45 assertions**, 0 console errors, after exercising every path |

## Escalations (not invented)

- **O-D168-1 — the memo's `64ch` reading measure is a build choice.** The report's measure is *derived* from the
  artifact and can never drift. The memo needs its own, and **no canon sets one.** Flagged, not asserted.
- **O-D168-2 — should a History export event OPEN its memo?** D168 §3 says *"every dated snapshot in History is a
  memo"*. History already records the event; it does **not** yet render the memo from there. Wiring it touches the
  History surface (Slice 7) and its read-only contract, so **it was not done unilaterally.**
- **O-D168-3 — a memo is frozen in memory, not on disk.** The prototype proves the **contract**; in the product,
  immutability is a **storage property** (a PDF, a hosted export link). **Engineering must prove the storage.**

---

# D169 — HISTORY OPENS THE SENT MEMO (2026-07-12) · closes **O-D168-2**

> *"What did I actually tell them in June?"* OSLO already held the answer — **frozen and byte-exact** — and left it
> unreachable. Now the record of the sending **opens the thing that was sent.**

## What changed (small and surgical — 6 touch points)

| # | Change | Where |
|---|---|---|
| 1 | **The History event carries the memo id.** `pushHistory(type, lab, {memo})` → `HISTORY[i].memo`. Both send paths (`genReport`, `runScheduledReport`) now pass `memo: memo.id`. **It is the record's only handle on the frozen bytes.** | `pushHistory()` · `genReport()` · `runScheduledReport()` |
| 2 | **The "memo sent" row opens the memo.** Clickable + keyboard-operable (`role="button"` · `tabindex="0"` · Enter/Space), affordance **"open the memo →"**. Every other row is untouched. | `_histRow()` |
| 3 | ⛔ **`openMemoFromHistory(id)` — the whole mechanism.** It does **exactly one thing**: selects the frozen memo out of `REPORT_SNAPSHOTS[]` by id (`_memoById` → `_rptMemoView`) and opens the export preview. **It cannot reach the live composer** (`_mkMemo` / `_memoBodyHTML` / `_rptCleanHTML` / `genReport`), **runs no analysis**, and **appends nothing.** | new, beside `viewMemo()` |
| 4 | **The COVER now belongs to the memo on screen, not to the live read.** `#rptPkg` renders from `_memoOnScreen()` (`mos.cover.mark` · `mos.cover.disclaimer` · `_memoCurrencyHTML(mos)`). **⚠️ This was a real defect:** the cover was derived from `_readCurrency()`, so opening June's memo would have shown **July's run on its cover** — the document unchanged, the paper around it silently rewritten. The **label** still moves (*"previous analysis"* once the read overtakes it — D146/D168); **the memo's own run and date do not.** | `renderReports()` §2 · new `_memoCurrencyHTML()` / `_memoIsPrevious()` |
| 5 | `_renderMemo(mos)` takes the same object the cover was drawn from, so the memo and its package can never disagree about which memo is on screen. | `_renderMemo()` |
| 6 | **Bug fixed in the D168 proof harness:** its teardown read `HISTORY.splice(keepHistN, …)` — but `pushHistory()` **unshifts**, so that removed the **oldest** events (the Initial Analysis) and left its own send event behind. **A proof harness may not corrupt the epistemic record it runs beside** (D096). Now `HISTORY.splice(0, …)`. | `_d168StateProof()` |

## The guards (D166 — mechanism, never copy)

- **`_assertHistoryOpensTheFrozenMemo()`** (boot, every tier) — a **mechanism proof**, not a DOM/copy scan:
  (1) the History row wires the open path; (2) both send paths record the memo id and `pushHistory` keeps it;
  (3) ⛔ **the open path cannot call the live composer, cannot run an analysis, and cannot mutate**, read from its
  own source; (4) `_memoOnScreen()` returns a sent memo **BY IDENTITY** out of the frozen register (graded live
  against the real register the moment one memo exists); (5) it must actually select (`_memoById` → `_rptMemoView`).
- **`_d169StateProof()`** — the end-to-end **state proof**: **cut a memo · move the report · move the read · open it
  from its History event** → assert **byte-identical**, the **sent** words on screen (not the current ones), the
  memo's **own cover** (its run, its disclaimer, relabelled *previous analysis*), **read-only**, **nothing appended**,
  **nothing run** — and the **live composer invoked ZERO times.** *A re-render is invisible on screen; it is caught
  by proving the code that could produce it never ran.*
- `_assertReportPackagesNeverProduces()` now also covers `openMemoFromHistory` and `_memoCurrencyHTML`.
- **`_memoGuardProbe`** — `_assertMemoIsImmutable()` cuts a throwaway memo on **every render** to prove the freeze is
  real. That is the guard talking to itself, so it raises this flag and is **excluded from the composer count**.
  Without it, the proof would have indicted the very guard that protects it.

## Negative controls — **every one bites** (5 new bites + 1 proof + 1 control ON the proof)

| Control | Injected regression | Result |
|---|---|---|
| `d169_historyRowNoLongerOpensTheMemo` | the row stops wiring the open path | **BITES** |
| **`d169_openPathReRendersFromCurrentUnderstanding`** | ⛔ **the load-bearing one** — the open path re-renders the memo from the live read | **BITES** |
| `d169_historyEventDropsTheMemoId` | `pushHistory()` drops the id → the bytes become unreachable | **BITES** |
| `d169_openingAMemoWritesToHistory` | opening appends an event — *looking at the record is not an event in it* | **BITES** |
| `d169_sentMemoIsRebuiltNotRetrieved` | `_memoOnScreen()` hands back a **copy** instead of the frozen entry | **BITES** |
| `memoOpenedFromHistoryIsTheOneThatWasSent` | **the state proof** (not a bite: a proof) | **HOLDS** |
| **`d169_stateProofDetectsASilentRerender`** | ⚠️ a control **on the proof**: force a silent re-render on every open — the state proof **must go FALSE** | **BITES** |

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | **PASS** |
| 2 | jsdom **without `runScripts`** | **31 body children** — unchanged, healthy |
| 3 | Boot assertions × **Free/Basic × notes OFF/ON** | **46/46 pass, all four combinations, 0 console errors** (was 45; `historyOpensTheMemo` added) |
| 4 | Negative controls | **47/47 bite or hold** (was 40) |
| 5a | a **"memo sent"** History event opens the memo | ✅ real DOM click on `.hrow.clickable[onclick="openMemoFromHistory('MEMO-1')"]` → view `reports`, drawer `exp`, `#rptMemo[data-memo="MEMO-1"]` |
| 5b | **it shows the exact bytes that were sent** | ✅ report rewritten (*"JULY: the venue fell through…"*) **and** a new analysis run pushed → opened memo is **byte-identical** to the send digest, shows *"JUNE: schedule holds…"*, and **does not** contain the July words |
| 5c | **read-only · runs no analysis** | ✅ `contenteditable="false"`, no editor chrome (`.m-mine` / `.m-reset` / `#rptEd` absent); TREND unchanged, meter unchanged, `RPT_EDITS` unchanged |
| 5d | **cover · disclaimer · currency marker** | ✅ package visible; disclaimer present on the cover; **"previous analysis"** label; the cover carries **the memo's own run**, not the newer one; *"plan as of …"* attribution in the body; identity line *"Memo sent · …"*; `To:` line and signature present |
| 5e | **History remains append-only** | ✅ opening appended **0** events; the oldest event is intact; post-suite integrity: `REPORT_SNAPSHOTS=0 · HISTORY=5 · TREND=1 · _rptMemoView=null` (everything restored) |
| 5f | **scheduled** memo | ✅ its event carries the memo id and opens it (*"PDF (scheduled)"*) |
| 5g | Slices 1–9 + rest of Slice 10 | ✅ every view renders (overview · issues · artifacts · history · reports · projects · settings · limits), **0 console errors**, 46/46 assertions still green with a memo open |

## Tension / escalation

- **None invented.** D169 was built exactly as ratified. **O-D168-1** (the memo's `64ch` measure) and **O-D168-3**
  (immutability is a *storage* property in the product, not an `Object.freeze`) **remain open and unchanged**.
- ⚠️ **Worth the owner's eye:** the cover was silently deriving its currency marker from the **live** read. Nothing
  surfaced it before D169 because a memo was only ever opened seconds after it was cut. **Opening one from History
  is what made it visible** — the exact class of defect D169's rule exists to prevent, found in the paper rather
  than the prose. Fixed, and now covered by the state proof's cover half.

---

# D170 (P1) · D170c · D171 — 2026-07-12

## TASK 1 — the P1: a gated attempt that surfaced nothing

### THE BROKEN-PROMPT LIST — **two independent causes, and BOTH were live**

**RC-1 — the cadence caps were applied to gated attempts. (This is the reported defect.)**
`fireUP()` ran GUARD 3 (per-trigger cooldown) and GUARD 4 (global per-day cap) against **every** prompt. But
`UP-EXPORT` is `cool:'day'`, `UP-REPORT` is `cool:'day'`, `UP-6` is `cool:'month'` — **and `promptLog` persists in
localStorage.** So the **second** gated attempt of the day returned `false` and **rendered nothing**. The owner's
browser had already fired UP-EXPORT once; from then on the Export button was **permanently dead for the rest of the
day**. Reproduced in jsdom before touching anything:

```
RENDERED | UP-REPORT (extra section) | log n=1
*** VOID | UP-REPORT (branding)      | log n=1     ← silent
*** VOID | UP-REPORT (schedule)      | log n=1     ← silent
RENDERED | UP-EXPORT (readout)       | log n=2
*** VOID | UP-EXPORT (export dialog) | log n=2     ← silent
```
**Every `cls:'friction'` prompt was affected** — UP-EXPORT · UP-REPORT · UP-6 · UP-APPLY · UP-3 · UP-4 · UP-SEAT.
Once three prompts had fired in a day, `_PROTOTYPE_PROMPT_GUARD = 3` swallowed **all** of them.

> ⛔ **The bug was already known at one call site and papered over.** `simBudgetGate()` carried a hand-rolled
> `l.n = 0; delete m['UP-6']` with the comment *"demo: don't let the day-cap swallow the preview."* **Someone hit
> this, worked around it locally, and left every other gated attempt in the product silently broken.** That
> workaround is deleted — it is no longer needed, and it was the evidence.

**RC-2 — the prompt rendered BENEATH the surface it was fired from.**
`.upx-scrim` was **`z-index: 96` — the lowest overlay in the entire product**:

| Surface | z-index | fires a gated attempt? |
|---|---|---|
| `#issueClose` / `#issueScrim` | 262 / **260** | ✅ `applyFix()` → **UP-APPLY** |
| `#palScrim` | 250 | |
| `.notifpanel` | 236 | |
| `.projmenu` | 230 | |
| `#phasebar` | 200 | |
| `.scrim` (**the Export dialog**) | **172** | ✅ `doExport()` → **UP-EXPORT** |
| `#settings` | 122 | |
| `#workspace` | 120 | |
| **`.upx-scrim` (the prompt)** | **96** ⛔ | — |

So **UP-APPLY fired from the issue flyout and UP-EXPORT fired from the export dialog both rendered behind them.**
The DOM said green. The screen said nothing. `.upx-scrim` is now **420** — strictly above every rule in the file.

### THE FIX
> **A cadence cap governs what the PRODUCT INITIATES. It may never silence the product's ANSWER to a click the user
> made and the product refused.**

- `_isGatedAttempt(id)` = `UPROMPTS[id].cls === 'friction'` — **derived from the ratified table**, never a flag at the
  call site (*a call site that forgets a flag is exactly how this comes back*).
- **GUARD 3 + GUARD 4 apply to `cls:'value'` only** (UP-7, UP-8 — the product started it).
- **GUARD 1 (before first value) and GUARD 2 (mid-pass) are preserved — but they DEFER, they never DROP.** Both are
  ratified and non-overridable, and both are right. **Neither reason survives contact with silence.** A gated attempt
  caught by either is **queued and fired at the first legal moment**, and the user is told immediately which limit they
  hit (toast, ≤12 words, **no CTA**). *(→ escalated as O-D170-2 — confirm the reconciliation.)*
- `fireUP()` → **`_upRoute()`**: **there is no path out of the router that renders nothing.**

## TASK 1b — the guard failure. **D138 has three clauses; the guards verified one.**

`_assertNoDisabledLimitAffordances()` proved the Export button **was not disabled**. It was not disabled. **It also did
nothing at all.** The guard graded the *paint*, never the *wiring*.

**Built (extending D166):** *do not merely prove the control is LIVE — prove the ATTEMPT HAS A CONSEQUENCE.*

- **`LIMIT_ATTEMPTS`** — a registry carrying **all three D138 clauses**: `sel` (never disabled) · **`fire`** (the gated
  attempt, **fired for real**) · **`read`** (the surface that must appear).
- **`_assertGatedAttemptSurfacesAPrompt()`** — for every row: force **Free**, **SATURATE the prompt log**
  (`n: 999`, every id already fired today, every month-cooldown burnt — **the exact state the owner's browser was in**),
  fire the **real** path, and assert a prompt renders naming **the limit**, **the tier that relieves it**, and its
  **resolutions**. Snapshot → fire → grade → **restore** (History, memos, meters, tier, view, log — *a guard leaves no
  trace*). **If a cadence cap can ever swallow a gated attempt again, every row goes red.**
- **`_assertEveryLimitAffordanceIsFireable()`** — every `friction` prompt must have a row that **fires** it. *A control
  graded on its paint is how this got in.*
- **`_assertPromptSurfaceIsOnTop()`** — **derived from the authored cascade** (max z-index of every rule), so it cannot
  go stale.

### ⛔ THE AFFORDANCE × PROMPT TABLE — **11/11 PASS**

| Affordance | Prompt | Renders | Names limit | Names relieving tier | Resolutions | |
|---|---|---|---|---|---|---|
| Export format — readout toolbar (`genReport`) | UP-EXPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Export format — Export dialog (`doExport`) | UP-EXPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — an extra section | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — your own branding | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — sending it on a schedule | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Readout — keeping last week's wording | UP-REPORT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Monthly analysis budget ("Update now") | UP-6 | ✅ | ✅ | ✅ | 2 | **PASS** |
| Assisted apply — the fix cap | UP-APPLY | ✅ | ✅ | ✅ | 2 | **PASS** |
| Active projects — the project cap | UP-3 | ✅ | ✅ | ✅ | 2 | **PASS** |
| Collaborator seats — the seat cap | UP-SEAT | ✅ | ✅ | ✅ | 2 | **PASS** |
| Plan size envelope — partial analysis | UP-4 | ✅ | ✅ | ✅ | 2 | **PASS** |

> **Two guard bugs the new guard caught in its first run, and both were fixed in the GUARD (D166 §3):**
> 1. It read only `#upBody` for the relieving tier — **UP-REPORT names Basic in its TITLE.** Widened to **title + body**
>    (the *disclosure*), matching `_assertNoGenericUpgradeCopy()`'s existing scope. **The resolution buttons are
>    deliberately excluded** — `_resUpgrade()` says "Basic" on every friction prompt, so scanning them would make the
>    clause **true for free**: a vacuous guard, which is the exact disease.
> 2. It found `.rvv` at **z-index 400**. `.upx-scrim` was raised **96 → 420**, above everything.

## TASK 2 — D170c: drawers → popovers
`.rw-drawer` (in the flow, displaced the document) → **`.rw-pop`**: `position:fixed`, **anchored to its button**
(`_anchorRptPop()`, viewport-clamped), **out of the flow**. Esc closes · click-outside closes · **focus trapped**
(Tab cycles; focus returns to the anchor) · `aria-expanded` + `aria-haspopup` · one open at a time.
`_rptDrawerOpen`/`toggleRptDrawer`/`closeRptDrawer` renamed to `_rptPopOpen`/`toggleRptPop`/`closeRptPop` (25 refs).
**The memo is not a menu:** `#rptPkgHost` → **`#rptMemoHost`**, shown only when the PM asks for it (preview · a sent
memo · from History). Opening a menu no longer drags the memo onto the screen. → `_assertToolbarMenusArePopovers()`.

> ✅ **The D166 machinery worked.** Renaming `#rptDrawer` made three existing copy scanners fail **loudly** at boot —
> *"GUARD COVERAGE LOST: the copy scanner cannot find rptDrawer"* — instead of quietly grading an empty div.
> `SELLING_SURFACES` / `REPORT_SURFACES` updated. **Nothing was relaxed.**

## TASK 3 — D171: SEND
- **`sendMemo()`** + `#rptSendBtn` in the toolbar, **beside Export, as the primary action**.
- **ONE factory.** `_mkMemo(f, scheduled, seq, via)` now carries **`sent_via: 'shared' | 'exported'`**, frozen with the
  rest. `genReport` → `'exported'` · `sendMemo` → `'shared'` · `runScheduledReport` → `'exported'` *(flagged — O-D171-2)*.
- ⛔ **SHARE IS FREE ON EVERY TIER.** `sendMemo()` has **no tier branch, no `fireUP`, no meter**.
  `_assertSharingIsFreeOnEveryTier()` proves it **three ways**: (1) **structural** — the source carries no `TIER` and no
  `fireUP`; (2) **behavioural** — on **Free**, the real path produces a **real frozen memo** with a cover, a disclaimer
  and a currency marker, plus a History event; (3) **DOM** — **no lock chip** on the button, on any tier.
- A shared memo is **read-only** (`contenteditable="false"`, never the editor host), carries its cover/disclaimer/
  currency marker, and is **relabelled "previous analysis"** — the label is **derived** from the memo's own run against
  the live trend (*a stored flag would go stale*), and **the words never move**.
- **History records how it travelled** (`share` / `export`), and **D169 opens the frozen memo from either**.
- Guards: `_assertOneMemoFactory()` · `_assertSendPackagesNeverProduces()` · `_assertSharedMemoIsReadOnly()`.

## NEGATIVE CONTROLS — `_d170NegativeControls()` → **16/16 BITE**
`cadenceCannotSwallowAGatedAttempt` *(the P1, part one)* · `dayCapCannotSwallowAGatedAttempt` ·
`promptCannotRenderUnderTheSurfaceItFiredFrom` *(the P1, part two)* · `promptMustActuallyBeShown` ·
`promptMustCarryResolutions` · `promptMustNameTheRelievingTier` · **`aGatedAttemptMayNotReturnSilently`** *(the reported
defect, injected verbatim)* · `registryMayNotLoseAnAffordance` · `popoverMayNotBecomeADrawerAgain` ·
`sendMayNotBeTierGated` · `sendMayNotWearALock` · `theReadoutMustHaveASend` · `thereMayBeOnlyOneMemoFactory` ·
`sendMayNotRunAnAnalysis` · `aSentMemoMayNotBeEditable` · `aSentMemoMayNotBeSilentlyReDated`.

## A PRE-EXISTING DEFECT FOUND AND FIXED — **the proof was indicting its own scaffolding**
`_d169StateProof()` wraps `window._mkMemo` with a counting probe, then calls `openMemoFromHistory()` → `renderReports()`
→ the per-render guard **`_assertReportAndMemoAreNotConfused()`**, which reads **`String(_mkMemo)`** — i.e. **the
probe's source**. It found no *"Memo"* in `function(){ mkCalls++; return realMk.apply(...) }` and **threw a red console
on a healthy build**. The probes now report the **real** source via `toString`. **A proof may not indict the code it is
protecting** — the same rule `_memoGuardProbe` already encodes one line above.

## VERIFICATION

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | ✅ **PASS** |
| 2 | jsdom **WITHOUT `runScripts`** | ✅ **31 body children** — unchanged baseline. `#rptPop` · `#rptMemoHost` · `#rptBar` · `#rptDoc` · `#rptPkg` · `#rptMemo` · `#upScrim` all present; **0** `.rw-drawer` |
| 3 | Boot assertions | ✅ **54 assertions, 0 failures**, on **Free × Basic × notes-OFF × notes-ON**. **0 console errors** across the whole matrix |
| 4 | Negative controls (new) | ✅ **16/16 bite** |
| 4b | Negative controls (D164, non-regression) | ✅ **47/47 still bite** |
| 4c | State proofs | ✅ `_d168StateProof()` **true** · `_d169StateProof()` **true** |
| 5 | **Affordance × prompt table** | ✅ **11/11 PASS** (against a **saturated** prompt log) |
| 6a | Free + "Export link" → **the UP-EXPORT prompt renders** | ✅ — *and again, and from the export dialog too* |
| 6b | Free + PDF → exports | ✅ memo cut · `sent_via:'exported'` · frozen · **no prompt** |
| 6c | Toolbar menus are **popovers** | ✅ `position:fixed` · one open · `aria-expanded` · **the document does not move** |
| 6d | **Send exists, is FREE on every tier, freezes a memo** | ✅ Free **and** Basic: memo · `sent_via:'shared'` · frozen · **no prompt, no lock** |
| 6e | Both append History · **run no analysis** | ✅ `share:MEMO-3` · `export:MEMO-1` · trend **flat** on both |
| 6f | **D169 opens the frozen memo from either road** | ✅ read-only · `data-via` = `shared` / `exported` |
| 6g | **Slices 1–9 + rest of Slice 10 non-regression** | ✅ all six views switch; 54 assertions green |

## ESCALATED, NOT INVENTED (→ `open-items.md`)
- **O-D170-1** — does the ratified **MON-04 per-day prompt cap** cover **limit-hit disclosures**, or only unsolicited
  nudges? **The build says only nudges, and says so out loud.** D170 settles the *behaviour*; the *taxonomy* is owner's.
- **O-D170-2** — GUARD 1 / GUARD 2 vs. D170, **reconciled by DEFERRAL** (never silence). **Confirm.**
- **O-D171-1** — a SEND has **no UP-number**, and needs none: there is no limit to hit.
- **O-D171-2** — ⬜ **is a SCHEDULED readout an automated SHARE or an automated EXPORT?** Scheduling is Basic; sharing
  is free. Built as `'exported'`. **Owner decision required.**
- **O-D171-3** — the **in-app notification** a share raises belongs to Slice 8's awareness surface. Not invented here.

---

# D172 FOLD-IN (a–d) — 2026-07-12

**Target:** `vertical-slices/slice-10-tiering-limits/prototype.html` (amended in place). Surgical.

## What changed

**D172a — a scheduled readout is an automated SHARE.**
`runScheduledReport()` now takes the manual send's path exactly: `_mkMemo(SHARE_CHANNEL, true, seq, 'shared')` (was
`'exported'`), a **scoped read-only grant** for the recipient, and a **`share`** History event ("Scheduled memo sent to
…") carrying the memo id — so **D169 opens the frozen memo** from it. **D147 is untouched and still binds:** the currency
re-check runs at send time, a stale read goes out **labelled "previous analysis"**, and **no analysis is ever run to
freshen it** (trend + governor provably unmoved).

**D172b — the tier rule.** The tier check lives **at the toggle and nowhere else**. `sendMemo()` still has **no tier
branch** (CHG-061). `toggleReportSchedule()` gates on Free and fires `UP-REPORT {sched:true}` → **"Basic sends it for you
every Friday"** (**27 user-visible words**, D163), two resolutions, **free one first: _Send it now_**. The prompt sells
**the automation**; it never sells the ability to share. `_renderUP()` and `_assertNoGenericUpgradeCopy()` now support a
**contextual title**, and the MON-04 naming check grades **every context a prompt can render in** (a prompt that names
Basic on one branch and nowhere on the other was previously invisible to it).

**D172c — the shared memo is the reviewer grant's mechanism.** Refactored `_grantReviewerAccess()` into **one admission
factory**, `_grantScopedAccess(kind, …)`, with `_grantReviewerAccess` (`kind:'issue'`) and `_grantMemoAccess`
(`kind:'memo'`) as thin wrappers. `_mkLink()` gained a `'memo'` kind (scoped to one memo, revocable). The recipient's view
renders on the **same `#reviewerView` surface** as the CRR grant: the grant landing (**the link IS the invite, the invite
IS the authentication** — no signup wall, no password, no account, nobody anonymous), then the memo, **read-only**, from
its **own frozen bytes** (`_memoPaperHTML()`, extracted from `_renderMemo()`), on its cover, with its disclaimer and
currency marker. The Access panel now counts **Review grants** and **Shared memos** separately (a memo grant is not a
reviewer).

**D172d — Reports (workspace) / Readout (document).** Nav, top-bar, crumb and tooltip → **Reports**; the readout's own
toolbar → **Readout** (from `_readoutDocName()`, so there is **one rename site**). Added `REPORT_TYPES` — a registry keyed
by type with **exactly one entry** — so a second report type is an **addition**, not a rebuild. ⛔ **No speculative UI was
built**, and a guard now enforces that: no picker, no gallery, no cards, and the six D143 names may not return.

## Guards — 4 new, 10 new negative controls (D166: mechanism, negative control mandatory)
- `_assertScheduledSendIsAShare()` (D172a) — structural (`'shared'`, never `'exported'`) **+ full state proof**: fire the
  real schedule → frozen memo, `sent_via:'shared'`, a scoped grant, a `share` event carrying the id, trend + governor
  unmoved. Restores every byte it touched (memo, history, link, grant, principal, notification, sequences).
- `_assertSchedulingIsTheGateNotTheShare()` (D172b) — the **pair**: the branch is in the toggle, not in the send; **on
  Free, in one pass: the automation refuses and the share delivers**; and the prompt's **free resolution is a send**.
- `_assertSharedMemoUsesTheGrantMechanism()` (D172c) — one admission path · one link factory · **no password field, no
  form, no account-creating call** · the recipient's path **cannot reach the live composer** · no tier/meter on the grant.
- `_assertReportsHostsOneReportType()` (D172d/D143) — registry (exactly one) **+ DOM** (no type chrome) **+ the names**
  (nav/crumb = Reports; toolbar = Readout). Runs on **every render** of the workspace.
- NCs (all bite): `aScheduledSendMayNotBeAnExport` · `aScheduledShareMayNotSkipTheGrant` · `theAutomationMayNotBeFreeOnFree`
  · `theShareMayNotBeGatedInstead` · `aShareMayNotInventASecondGrantMechanism` · `theRecipientViewMayNotRebuildTheMemo` ·
  `aSharedMemoMayNotAskForASignup` · `aSecondReportTypeMayNotBeRegistered` · `theSixCardScaffoldMayNotReturn` ·
  `theWorkspaceMayNotBeCalledAReadout`.

## Two guards were found broken **by the new guards**, and both were fixed (D166 §3 — fix the guard, never the doctrine)
1. **`_assertSharingIsFreeOnEveryTier()`** demanded **exactly one** new History event per send. A send now writes **two**
   (the grant, then the send) — both true facts the record is entitled to. The clause that matters is unchanged and not
   weakened: **the newest event is the send, it is `type:'share'`, and it carries the memo's id, so D169 can open it.**
2. **`_assertSharedMemoUsesTheGrantMechanism()`** (as first written) scanned for the **word** *"signup"* — and the grant
   landing's own honest promise (*"no password, no signup"*) tripped it. **A guard written against copy rots.** It now
   grades the **mechanism**: a password field, a `<form>`, or a call that creates an account.

## Verification
1. `node --check` → **PASS**.
2. jsdom **without** `runScripts` → **31 body children** (unchanged).
3. Boot assertions: **58 guards, all green**, on **Free × Basic × notes-OFF × notes-ON**, **0 console errors** in all four.
4. Negative controls: **73 total — 47 (`_d164NegativeControls`) + 26 (`_d170NegativeControls`) — every one bites.**
5. Behavioural: (a) manual share free + unlimited on Free (3 sends → 3 shared memos, 3 grants, no prompt, no invite spent)
   · (b) scheduling on Free → prompt renders, schedule stays OFF, names limit + Basic + 2 resolutions, sells the
   automation, free resolution = *Send it now*; **the share still delivers the same minute** · (c) scheduled send →
   `sent_via:'shared'`, `share` History event with the memo id, **no analysis** · (d) stale read → **"previous analysis"**
   · (e) **D169 opens the frozen memo byte-identically** after the report is edited · (f) Reports / Readout everywhere
   · (g) one report type, no speculative UI · (h) every view renders, all guards green, 0 errors.

## Open items raised (escalated, not invented)
**O-D172-1** the scheduling **cadence** (weekly is the build's single option, not a ratified value) · **O-D172-2** a
**stale plan does not stop the schedule** (it labels it) — an owner call · **O-D172-3** the **memo-grant lifetime** is
inherited from the 30-day snapshot link (CR-6 ratifies no lifetime for a memo-scoped grant) · **O-D172-4** the recipient's
in-app **notification** remains Slice-8 scope. **O-D171-2 is CLOSED. R-O1/M4-O1 is now closed on the naming; only the
glossary-tier ratification (DL-053) remains.**

---

# D173 — THE PAYOFF: numbers that are TRUE (owner-directed, 2026-07-12)

**Amended in place:** `vertical-slices/slice-10-tiering-limits/prototype.html`. **No regressions.**

## What was built
1. **D173b — the payoff.** `#payoff` on the Overview: **band transition** (headline) · **true counts** (computed
   from live state) · **the consequence** (the limiting dimension, named). ≤45 words. Fires on **every** analysis
   update: applied fix · answered clarification · a reviewer's evidence · the Extended pass.
2. **D173c — a fall is as legible as a rise.** One block, one set of classes, one weight, **no colour keyed to
   direction** anywhere. The neutral-ramp violations that already existed were fixed with it: the trend arrows and
   History confidence chips were **green ▲ / amber ▼**, and the Overview trend row was **hard-coded to rise** — a
   read that fell was *drawn as a read that rose*.
3. **D173d — the index demoted.** The band is the 40px hero; `62/100` survives at 15px as a secondary aggregate,
   with **no delta**. **Demoted, not deleted.** Calibration flagged in the notes layer only (D161).

## ⛔ NUMBER-PROVENANCE TABLE — every number the payoff can show
| Number shown | Computed from state? | Can OSLO defend it? | Source |
|---|---|---|---|
| **Band transition** *Feasibility: Very Low → Low* | **YES** — `_cafLevelFor(feasW)`, 5-band scale (DL-086/098) | **YES** — ordinal, discrete, derived; the level is never typed in | `_readSnapshot().caf` |
| **Issues** *6 → 5* | **YES** — `Object.keys(ISSUES).filter(_active).length` | **YES** — a count of live objects | `PAYOFF_COUNTS.issues` |
| **Critical** *1 → 0* | **YES** — active issues with `sev==='critical'` | **YES** | `PAYOFF_COUNTS.critical` |
| **Open questions** *2 → 1* | **YES** — `_openClarIds().length` | **YES** — unanswered clarifications on live issues | `PAYOFF_COUNTS.questions` |
| **Confirmed artifacts** *0 → 1 of 7* | **YES** — `PLAN_SECTIONS.filter(basis==='attested')` / `PLAN_SECTIONS.length` | **YES** — attestation is a state on the artifact | `PAYOFF_COUNTS.confirmed` |
| **Reliability** *Moderate → High* | **YES** — the weakest of coverage/evidence/assessable | **YES** — ordinal, from its own basis (D051) | `_readSnapshot().rel` |
| **Limiting dimension** *"Feasibility is still the limit"* | **YES** — lowest CAF width | **YES** — the same computation the Overview `lim` marker uses | `_limitingOf()` |
| ~~**Dependencies confirmed** *5 of 8 → 6 of 8*~~ | **NO — THERE IS NO DEPENDENCY REGISTER** | **NO** | ⛔ **REMOVED. Omitted, not invented.** → **O-D173-2** |
| ~~**0–100 index delta** *58 → 62*~~ | (formable, but) | **NO — the index is UNCALIBRATED (DL-062 F1)** | ⛔ **REMOVED.** `idx` is **not in the snapshot**, so the delta cannot be formed. → **O-D173-1** |
| ~~*"5 of 7 plan artifacts well-evidenced"*~~ (Overview "Why" box) | **NO — it was hard-coded; nothing computed it** | **NO** | ⛔ **REMOVED** (found in build) |

**Every remaining row is YES/YES.** Every NO was removed, not softened.

## Guards added (D166 — mechanism, not copy; negative control mandatory)
| Guard | Mechanism it proves |
|---|---|
| `_assertEveryPayoffCountIsComputed()` | every registry row has a `get()` that reads state · an **uncomputable** count never reaches the snapshot · **and a computable one does** (so the proof is not vacuous) · every snapshot key traces to a registry row and is a finite number · **every integer printed exists in the before/after snapshots** |
| `_assertNoIndexDelta()` | `idx` is **absent from the snapshot** (a delta is not formable) · the payoff prints no `/100` and no signed number · the index **still exists** (demote ≠ destroy) · its line reads exactly `N/100` · **CSS: band > index, index ≤ 20px** |
| `_assertRiseAndFallAreVisuallyEquivalent()` | the model **recognises** a fall from state · **identical DOM signature** rise vs fall · no colour token in the markup **or the copy generator** · **no `.payoff.up/.down` modifier and no colour in any `.payoff` CSS rule** · **the fall still says it fell** |
| `_assertPayoffWithinBudget()` | ≤45 words for **both** directions · and the fitter **never** drops the action, the band, the fall note or the limiter |

**Boot self-check: 60 → 64 guards. All green.**

## ⚠️ THE ELEVENTH GUARD FAILURE — found while building this, fixed here
`_assertGatedAttemptSurfacesAPrompt()`'s **UP-APPLY** probe hard-coded `Object.keys(ISSUES)[0]`. `applyFix()`
correctly refuses a **resolved** issue — so **the moment a user applied a fix to ISS-01, the guard fired at a dead
subject, saw no prompt, and reported a P1 defect that did not exist.** It now fires at a **live** issue, and says
**CANNOT VERIFY** if there is none. *(D166: fix the guard, never the doctrine — and never let a guard cry wolf.)*
**Same family as the ten before it: the guard was grading a subject that wasn't there.**

## Defects found and fixed during the build
- **The payoff snapshot was taken after the state moved** — so *"Confirmed artifacts 0 → 1"* silently vanished:
  **the user's own action was invisible in its own payoff.** `before` is now taken **before the user acted**.
- **My own guard graded its own comment** — `_payoffCssOK()` read the block comment (which *says* "there is no
  `.payoff.up`") as a rule declaring one. Comments are stripped before grading.
- **A negative control found a real hole**: the count guard only proved the mechanism for **its own probe key**; a
  snapshot special-casing any other key walked through. Now **every** snapshot key must trace to a registry row.

## Verification
| # | Check | Result |
|---|---|---|
| 1 | `node --check` (extracted script) | **PASS** |
| 2 | jsdom **without** `runScripts` | **PASS** — 31 healthy body children |
| 3 | Boot assertions, **Free × Basic × notes-OFF × notes-ON** | **64/64 green in all four · 0 console errors** |
| 4 | **Negative controls — 16, on every guard added or touched** | **16/16 BITE** |
| 5 | Number-provenance table | above — **every row YES/YES**; three removed |
| 6a | Applying a fix produces the payoff | **PASS** — band + 4 counts + limiter, **29 words** |
| 6b | A **fall** renders with identical weight/layout, no negative colour | **PASS** — 18 words · DOM signature identical (equal-cardinality) · **0 colour tokens · 0 inline styles** |
| 6c | No delta on the 0–100 index | **PASS** — 0 `/100` and 0 signed numbers in the payoff; index line reads `62/100` |
| 6d | The index is demoted, not deleted | **PASS** — `#ov-idx` present at 15px; `#ov-band` is the 40px hero |
| 6e | ≤45 words | **PASS** — 29 (fix) · 23 (clarification) · 18 (fall) |
| 6f | Slices 1–9 + rest of Slice 10 non-regression | **PASS** — every view, all 7 artifacts, all 6 issues, Plans, Reports, History, notes toggle: **0 console errors, 64/64 guards still green afterwards** |

## Open items raised (escalated, not invented)
**O-D173-1** the index: **CALIBRATE or DEMOTE — owner-open** (DL-062 F1) · **O-D173-2** *dependencies confirmed* is
**not counted because it cannot be** (no dependency register) · **O-D173-3** *unvalidated assumptions* renders as
**open clarifications** (the assumption lifecycle is RB-017, not built) · **O-D173-4** may **Reliability** headline
a payoff, or must a CAF band always lead?

---

# D174 — THE OVERVIEW HERO IS THE MATURITY RAMP (owner, 2026-07-12)

**D173d demoted the uncalibrated index and left one word in 40px. That is a label, not a hero.** The replacement
was already in canon and never drawn: **D003 mandates a neutral maturity ramp.** It is drawn now.

```
Very Low  ·  Low  ·  [ MODERATE ]  ·  High  ·  Very High      ← lit step, 32px, neutral
on moderate reliability
Feasibility is holding it back.
↗ Strengthened — deeper analysis firmed the read (Feasibility rose Very Low → Low)          58/100
```

## What the hero shows — and where every element comes from

| # | Element | Live copy | Provenance (computed, never typed) |
|---|---|---|---|
| **1** | **THE RAMP** — five bands, the current one lit and named | *Very Low · Low · **Moderate** · High · Very High* | `_rampHTML()` maps **`_BANDORD`** (DL-086/098); the lit step is `_BANDORD.indexOf(currentRead().band)`. **No band word exists in the static markup** — `#ov-ramp` ships empty |
| **2** | **THE RELIABILITY QUALIFIER** | *on **moderate reliability*** | `currentRead().rel` (D002/D051) — the read never stands bare |
| **3** | **THE LIMITER** | ***Feasibility** is holding it back.* | `_limitingOf(r).dim` — the lowest CAF dimension; the **same** computation that marks the `.cafrow.lim` row, the chat and the payoff |
| **4** | **THE DIRECTION + ITS NAMED CAUSE** | *↗ **Strengthened** — deeper analysis firmed the read (Feasibility rose Very Low → Low)* | `_readDirection()` (band first, index only as a tiebreak) + `_readCause()` = the last `TREND` run's cause. **D056: direction + cause, never a magnitude.** Rendered **only when `_directionIsComputable()`** (≥2 runs) |
| **5** | **THE 0–100 INDEX** | `58/100` — 15px, bottom-right | `currentRead().idx`. **Secondary, small, NO DELTA.** Demoted, not deleted (DL-062 F1 is open) |

**ONE painter:** `renderHero(r)` writes all five; `renderOverview()` and the **boot** both call it, so the hero is
never a stale hand-written value. **Word budget: 19 words** (D163 budget 40 — band labels are a *scale*, not prose).

## Neutrality — it is a MATURITY scale, not a HEALTH bar (D003 · DL-104 §5)
- **Colour ALLOWLIST, enforced in the CASCADE** (not the DOM — *a previous defect was invisible to DOM guards*):
  only `--text · --muted · --subtle · --border* · --surface*` may colour the ramp. **No `--success`/`--danger`/
  `--warning`, no `--conf-*`, and not even the brand `--primary`** — an amber-adjacent orange is exactly how a user
  reads *"at risk"*. A blacklist only catches the colours somebody already thought of; an allowlist catches the rest.
- **No percentage fill.** Five identical fixed segments; **exactly one lit**. Steps below the read are **not "done"**.
- **A fall is a step down, in the same weight and the same colour.** A rise is not green; a fall is not red.

## Defects found and fixed during the build
1. **⚠️ The Extended pass landed and the hero's direction stayed HIDDEN.** `deepComplete()` re-renders the read
   **before** it appends the run — so at render time there was still only **one** run to compute a direction from,
   and the row was (correctly, but uselessly) suppressed. **`pushTrend()` now re-paints the hero**: the direction
   lives on the record, so the hero follows the record whatever order a caller writes it in. *(Found by the
   behavioural test, not by a guard — no guard covered the ordering. One now does, by consequence.)*
2. **AA failure on the ramp's own scale.** The unlit segments are **meaningful graphics** (they *are* the scale) and
   `--border-2` gives **1.7:1** against the card — under the 3:1 floor, in **both** themes. Fixed to `--subtle`
   (**5.3:1** dark / **5.2:1** light). The lit step is separated by **weight**, not hue.

## Guards added (D166 — mechanism, not copy; negative control mandatory)
| Guard | Mechanism it proves |
|---|---|
| `_assertRampIsNeutral()` | reads the **CASCADE** (comments stripped) · **allowlist** on every colour-bearing declaration in every ramp rule · the **builder** writes no colour and no inline style · **no inline style reached the DOM** · **not vacuous** (≥4 ramp rules must exist) |
| `_assertLitBandIsComputedFromState()` | walks **all five** bands through the builder — right word, right ordinal position, exactly one lit, five steps in DL-086/098 order · then **moves the live read** and proves the card's ramp moved with it |
| `_assertRampIsNotAHealthBar()` | **no percentage fill** (cascade + DOM) · the unlit steps are **identical** (no 1..n progress fill) · **no health/RAG vocabulary** in the hero (the D161 notes layer is stripped first — it is not product copy) · no severity colour inline in the confidence focus |
| `_assertHeroElementsAreComputed()` | all five elements trace to state: lit band = `read.band` · qualifier = `read.rel` · limiter = `_limitingOf()` (**and `_limitingOf` is proved to derive, via a probe whose weakest dimension is Alignment**) · direction **shown ⇔ computable** and carries its cause and **no magnitude** · index = `read.idx`, **no signed delta anywhere in the hero** |
| `_assertHeroWithinBudget()` | ≤40 words of hero prose (D163) |
| `_assertNoIndexDelta()` *(touched)* | its CSS clause now grades **the lit band** (`.ramp .rstep.on .bandhero`) vs the index — demote ≠ destroy, and the index may not climb back |

**Boot self-check: 64 → 69 guards. All green.**

## Verification
| # | Check | Result |
|---|---|---|
| 1 | `node --check` (extracted script) | **PASS** |
| 2 | jsdom **without** `runScripts` | **PASS** — **31** healthy body children (unchanged) |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **69/69 green in all four · 0 console errors** |
| 4 | **Negative controls — 24, on every guard added or touched** | **24/24 BITE** (each verified green *before* the mutation) |
| 5 | **AA contrast, BOTH themes, on the hero** | **PASS** — lit word 15.1 / 16.6 · band labels 8.8 / 8.0 · qualifier·limiter·direction 8.8 / 8.0 · index 8.8 / 8.0 · `/100` 5.3 / 5.2 · lit bar 15.1 / 16.6 · **unlit bar 5.3 / 5.2** (was 1.7 — **fixed**) |
| 6a | The ramp renders **all five bands**, the current one lit **from state** | **PASS** — `Very Low · Low · Moderate · High · Very High`, lit = `currentRead().band` |
| 6b | It **moves when the band changes** | **PASS** — apply the critical fix ⇒ payoff *"Feasibility: **Very Low → Low**"*; the overall band did not cross, so the ramp correctly **holds at Moderate**. Drive the read to **High** ⇒ the ramp lights **High**. Drive it to **Low** ⇒ it lights **Low** |
| 6c | **A FALL renders with identical weight — no negative colour** | **PASS** — *"↘ Softened — a deeper look found a dependency that was always there"*; class + DOM signature **identical** to the rise (`SPAN.trend-arrow\|B.\|SPAN.tcause`); **0 colour tokens, 0 inline styles**; the ramp steps **down** with the same treatment |
| 6d | Qualifier · limiter · direction+cause present and computed | **PASS** — *on moderate reliability* · *Feasibility is holding it back.* · *↗ Strengthened — deeper analysis firmed the read (…)* |
| 6e | The index is **secondary, no delta** | **PASS** — `58/100` at 15px vs the 32px lit band; the line reads exactly `N/100` |
| 6f | **Zero severity/health colour in the hero** | **PASS** — the only inline style in `.conf-focus` is `display:flex` on the direction row |
| 6g | Slices 1–9 + rest of Slice 10 non-regression | **PASS** — all 10 views, issue flyout, apply-fix, Extended pass, Reports, History, notes toggle: **0 console errors**, **69/69 guards still green** afterwards |

## Open items raised (escalated, not invented)
**⚠️ O-D174-1 — the Provisional/Current chip is amber/green, inside the hero card.** `.ustate.prov` = `--warning`,
`.ustate.cur` = `--success` (**D040**, pre-existing, untouched). It is a fact about the **analysis**, not the
project — but **amber-and-green one line above a five-step scale is exactly the adjacency a user could read as
RAG** (DL-104 §5). The D174 guards deliberately scope their colour clauses to the **confidence focus**, so this
does **not** fail today. **Owner call: keep it, or neutralise it.** *Escalated rather than decided — otherwise the
guard would have been written to bless whichever answer we picked.*
**⬜ O-D174-2 — the ramp shows the next rung POSITIONALLY, but cannot say what would move you onto it** — the model
holds no "what would raise the band" object, only the limiter and the open issues. **Omitted, not invented.**
**⬜ O-D174-3 — the 0–100 index: CALIBRATE or DEMOTE remains owner-open** (O-D173-1 stands, DL-062 F1).

---

# D175 — NEUTRALISE THE PROVISIONAL/CURRENT CHIP (owner, 2026-07-12) · closes O-D174-1 · amends D040

> **The defect was not in what either element SAID. It was in what they said TOGETHER.**
> `.ustate.prov` = `--warning` (amber) · `.ustate.cur` = `--success` (green) — **inside the confidence hero card,
> one line above the five-step maturity ramp.** Each was technically honest on its own; **together they were RAG.**
> That is the **P1 health-framing class (DL-104 §5)** arriving **through a side door**.
> **And the guard could not see it — because the guard was scoped to an ELEMENT, and the defect was an ADJACENCY.**

## What changed

| | Before (D040) | After (D175) |
|---|---|---|
| **Provisional** | `--warning` text · amber border · `rgba(217,164,65,.08)` wash | **hollow ring dot** · `--muted` · weight **600** · `--surface-2` |
| **Current** | `--success` text · green border · `rgba(77,139,107,.10)` wash | **filled dot** · `--text` · weight **700** · `--surface-3` · `--subtle` border |
| **Last-good** | the provisional treatment | the provisional treatment (**the read on screen *is* the last good one**) |

- **The labels are UNCHANGED.** *Provisional · Current · Last-good* are honest (D040) and they stay. **Only the
  colour went.** The information was **de-judged, not deleted**: Provisional/Current is a **STATE**, not a
  **JUDGMENT**, and **a dot and a word carry it**.
- **Legible by WEIGHT and SHAPE, never by HUE** — the D174 precedent (the lit ramp step is separated by weight, not
  hue). A colour-blind reader sees the same two states everyone else does.
- ⚠️ **The amber was written as a RAW LITERAL** (`rgba(217,164,65,.08)` is `--warning` with the label filed off). A
  token blacklist would have missed it. **Every colour literal in the card is now graded by CHROMA.**

## THE GUARD — the scope is now the CARD (this is the real lesson)
`_assertHeroCardCarriesNoSeverityColour()` · `_assertAnalysisStateChipIsNeutral()` · `_assertAnalysisStateIsLegible()`

- **No severity/health token may colour ANY rule that can select a hero-card element** (`--success` · `--warning` ·
  `--danger` · `--conf-*`), **and no chromatic literal**. Inline styles too — that is the second door.
- **Read from the AUTHORED CASCADE, not the DOM.** The green lived on **`.cur` — a state that was not on screen.**
  No DOM guard was ever going to see it.
- **The scope is DERIVED from the live card** — every class/id on a hero element, minus generic state modifiers
  (`.on` may *ride* a hero class but may never *pull a rule into scope*), plus the card's real ancestor chain. It
  **cannot go stale**, and it **does not leak**: `.issue .card{--danger}` and `.tog.on{--success}` stay out (proven
  by a **must-not-fire** control — the whole app is full of legitimate severity colour on issues).
- **Two tiers, deliberately — brand ≠ severity.** `--primary` stays legal **on the card** (the CAF limiter row, the
  footer links — pre-existing) but is **banned on the chip and the ramp**, where an amber-adjacent orange is exactly
  how a user reads *"at risk"* (D174's own reasoning). NC-08 proves the tiers are independent.
- **The D161 notes rail is excluded** — it *legitimately* speaks in `--warning`; a guard that graded it would fail on
  its own documentation (the exact D166 failure mode).

### ⚠️ The guard's own negative control found a hole in the guard
The first draft read a selector as **everything before the first `{`** — so a severity rule hidden inside an
**`@media` block** (`@media(…){.ustate.cur{color:var(--danger)}}`) was **invisible to it**. **NC-06 went red, and it
was right.** `_cssSelOf()` / `_cssBodyOf()` now shed the at-rule prefix (and `_rampCssRules()` was fixed with them).
**Fix the guard, never the doctrine** (D166 §3).

## THE ADJACENCY SWEEP — every severity/health colour on or beside a maturity/confidence surface

| Surface | Element | Colour | Verdict |
|---|---|---|---|
| **Overview hero card** | `.ustate.prov` / `.ustate.cur` | `--warning` / `--success` **+ raw amber/green literals** | ⛔ **THE DEFECT — FIXED (D175).** Neutralised; dot + weight carry the state |
| **Overview hero card** | `.cafrow.lim .cn` / `.caffil` / `.cafband` (the **limiting** CAF row) | `--primary` / `--primary-light` (**#D97A3A**, brand orange) | ⚠️ **ESCALATED → O-D175-1.** Brand ≠ severity, so the card guard permits it **by design** — but D174 banned `--primary` from the *ramp* for exactly the amber-adjacency reason, and this sits on a **maturity surface three lines under the ramp**. Pre-existing, deliberate, marks *the limiter* (not a grade). **Not restyled unilaterally.** |
| **Overview hero card** | ramp · qualifier · limiter · trend row · index · false-confidence flag · Why box · footer | neutral (+ `--primary-light` on links) | ✅ correct — and **now guarded card-wide** (64 rules) |
| **Confidence pill** (top bar) | `.conf-dot` | `--conf-medium` | ✅ correct — `--conf-*` is the **neutral greyscale** maturity ramp (**no hue in either theme**), exactly what D003 mandates |
| **Confidence popover** `#confpop` | CAF bars — `width:N%` + `background:var(--conf-high\|medium\|low)` | neutral greyscale | ✅ **no hue** → not RAG. ⬜ **Noted (O-D175-2):** they are *percentage fills* on a confidence surface, and D174 banned fills **on the ramp**. Per-dimension levels, not an aggregate metre; pre-existing. **Owner's call, not mine.** |
| **Workspace project cards** | `.conf-dot` via `_bandDot(band)` | `--conf-high / medium / low` | ✅ correct — a **band → greyscale** map. **Never RAG**: High is not green, Low is not red |
| **Attention map** | `.heat-cell.l1 / .l2 / .l3` | amber → red (`--warning`, `--danger`) | ✅ **CORRECT AS IS — THESE ARE ISSUES.** Cells are shaded by **open-issue severity only** (`l0` = *no open issues*). **D003 assigns severity colour to issues**; D060 says the cells use the severity ramp and *"confidence/CAF stay neutral"*. **Not touched.** |
| **Attention map** | CAF column headers / confidence elements | neutral | ✅ correct |
| **Trend row** (hero) + **History trend** | `.trend-arrow` `--muted` · line `--subtle` · point `--text` | neutral | ✅ correct — **a rise is not green, a fall is not red** (D173c) |
| **Payoff card** (sits **directly above** the hero) | — | no colour token at all | ✅ correct — guarded by `_payoffCssOK()` |
| Waitlist bands `.wl-band.b1` | `--cool` (blue) | — | ✅ out of scope — a **release waitlist**, not a maturity surface |
| Artifact cell `.cell-epi.attested` · `.save-confirm` | brand orange · `--success` | — | ✅ out of scope — an attestation chip and a *save* confirmation, not a read |

**Nothing was restyled that the owner did not name.** The two ambiguous items are **escalated**, not decided.

## Verification
| # | Check | Result |
|---|---|---|
| 1 | `node --check` (extracted script) | **PASS** |
| 2 | jsdom **without** `runScripts` | **PASS** — **31** healthy body children (**unchanged**) |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **72/72 green in all four · 0 console errors** (69 → 72) |
| 4 | **Negative controls — 17** (every guard touched or added) | **15/15 BITE · 2/2 must-not-fire stay GREEN** (positive control green first, every time) |
| 5 | **AA contrast, BOTH themes**, on the neutralised chip | **PASS** — *Provisional* **7.67** (dark) / **7.29** (light) · *Current* **11.61 / 13.39** (4.5:1 floor) · dot as a meaningful graphic: hollow **4.67 / 4.75**, filled **11.61 / 13.39** (3:1 floor) |
| 6a | The chip is **neutral** — zero severity/health tokens in the hero card | **PASS** — cascade (64 rules) + inline + DOM all clean |
| 6b | Provisional vs Current still legible at a glance, **without hue** | **PASS** — hollow vs **filled** dot · 600 vs **700** · `--muted` vs `--text` |
| 6c | The **labels are unchanged** | **PASS** — `Provisional` · `Current` · `Last-good`, driven through `renderOverview()` from `ANALYSIS_STATE` |
| 6d | The ramp / hero still render **from state** | **PASS** — lit band = `currentRead().band` (Moderate) · idx 58 · *on moderate reliability*; land the Extended pass ⇒ chip flips to **Current** and the hero re-paints |
| 6e | **Slices 1–9 + rest of Slice 10 non-regression** | **PASS** — 9 views, every artifact, every issue, report generation, apply-fix, Extended pass, notes toggle: **0 console errors**, **72/72 guards green afterwards** |

### The negative controls, in full
| NC | Injection | Must |
|---|---|---|
| 00 | *(as shipped)* | **green** ✅ |
| 01 | `--warning` back on `.ustate.prov` | bite `heroCardNoSeverity` + `chipIsNeutral` ✅ |
| 02 | raw amber literal `rgba(217,164,65,.08)` (**token name filed off**) | bite both ✅ |
| 03 | `--success` back on `.ustate.cur` | bite both ✅ |
| 04 | `--danger` on `.conf-foot .lnk2` (**in the card, outside the focus**) | bite `heroCardNoSeverity` ✅ |
| 05 | `--warning` on `.card-flag` (**in the card, outside the focus**) | bite `heroCardNoSeverity` ✅ |
| 06 | `--danger` on `.ustate.cur` **hidden in an `@media` block** | bite ✅ *(**it did not, before the guard was fixed**)* |
| 07 | **inline** `style="color:var(--danger)"` in the card | bite ✅ |
| 08 | brand `--primary-light` on the **chip** | bite `chipIsNeutral` **only** — *not* `heroCardNoSeverity` ✅ (the two tiers are independent) |
| 09 | both chip states made **identical** ("neutral" = invisible) | bite `chipIsLegible` ✅ |
| 10 | the label rewritten (`Current` → `OK`) | bite `chipIsLegible` ✅ |
| 11r | the chip **removed at runtime** | guard green before, **bites after** ✅ (a missing subject is a FAILURE, not a pass) |
| 12 | every `.ustate` rule **deleted** (vacuity) | bite ✅ (CANNOT VERIFY ⇒ fail) |
| 13 | `--danger` on the **lit ramp bar** | bite `heroRampNeutral` **and** `heroCardNoSeverity` ✅ |
| 14 | `--success` on the **lit band word** | bite both ✅ |
| 15 | `.issue .card{--danger}` + `.tog.on{--success}` (**other surfaces**) | **NOT fire** ✅ (the scope does not leak) |
| 16 | **notes ON** — `.pn` renders `--warning` inside the hero card | **NOT fire** ✅ (D161: the governance rail is not product copy) |

## Escalations raised (not decided)
- **⚠️ O-D175-1 — the CAF limiter row is brand-orange, three lines under the ramp.** `--primary` is a **brand**
  token, not a severity token, so the D175 guard permits it — but **D174 banned `--primary` from the ramp for
  exactly this reason** ("an amber-adjacent orange could let a user read *amber = at risk*"). Pre-existing and
  deliberate: it marks **which row is the limiter**, which the hero also states in prose. **Owner call: keep it, or
  carry the limiter by weight/position as the ramp's lit step is.** *Escalated, not restyled.*
- **⬜ O-D175-2 — the confidence popover's CAF bars are percentage fills** (neutral greyscale, so **not** RAG — but
  D174 forbade a fill on the ramp because *a bar that fills to N% is a metre*). Per-dimension levels, not an
  aggregate health metre. **Noted; not changed.**

---

# D176 — THE LIMITER ROW LOSES THE ORANGE; THE CAF BARS WERE FALSE PRECISION (owner: approved, 2026-07-12)

**Closes O-D175-1 and O-D175-2.** Both fixes are in `vertical-slices/slice-10-tiering-limits/prototype.html`
(amended in place). **No regressions; every standing guard still passes.**

## D176a — the CAF limiter row is neutral (closes O-D175-1)
`--primary` is not a severity token, so D175's card guard permitted it **by design**. **D174's own reasoning
reaches it**: it banned `--primary` from the ramp *precisely because an amber-adjacent orange invites "amber = at
risk"* — and the limiter row sat **three lines under the ramp, inside the same card**.

> **The limiter is a FACT — *"Feasibility is holding it back"* — not a WARNING.** It needs **emphasis**, and
> **weight gives emphasis**.

**The hero card's banned list is now** `--success · --warning · --danger · --error · --crit · --conf-* · --primary*`
**+ every chromatic literal** (`HERO_CARD_BANNED_TOKEN_RE`). Restyled inside the card: the limiter row's name and
band word (**weight**, `--text`), a rendered **"the limit"** marker (`_limitingOf()`), the footer links (dotted
underline instead of orange), the how-calc bullet, and the popover's stage word. **Zero hue in the hero card.**

## D176b — the CAF dimensions are BANDS, not percentages (closes O-D175-2)
Both surfaces (the Overview hero card **and** the confidence popover) now draw each dimension on **the hero's own
five-step ordinal ramp** — *Very Low · Low · Moderate · High · Very High* (DL-086/098) — **one builder,
`_rampHTML(lvl,{compact:true})`, one mental model** — with the **limiter marked in words and weight**.
`.caftrk` / `.caffil` / `.cpp-bar` are gone; `_RELPCT` / `_RELCOLOR` are deleted; the reliability basis carries its
**level word** alone. **`feasW`/`alignW` stay in the MODEL** and still compute the band through `_cafLevelFor()` —
they are simply never rendered as a fill again.

## ⛔ THE PERCENTAGE-FILL SWEEP (every partial fill in the product)
| # | Element | Where | Fill | Maturity surface? | Verdict |
|---|---|---|---|---|---|
| 1 | `#cpp-feas-bar` (Feasibility) | Confidence popover | `style.width = r.feasW + '%'` (30/38/52%) | **YES — CAF** | ⛔ **REMOVED** → five-step band |
| 2 | `#cpp-align-bar` (Alignment) | Confidence popover | `style.width = alignW + '%'` (55%) | **YES — CAF** | ⛔ **REMOVED** → five-step band |
| 3 | Clarity bar (static) | Confidence popover | `style="width:76%"` | **YES — CAF** | ⛔ **REMOVED** → five-step band (now rendered from `_cafOf()`, not typed) |
| 4 | `#cpp-cov-bar` (Coverage) | Confidence popover | `_RELPCT` → `width:60%` | **YES — reliability** | ⛔ **REMOVED** → level word only (**scale escalated → O-D176-1**) |
| 5 | `#cpp-evd-bar` (Evidence availability) | Confidence popover | `_RELPCT` → `width:60%` | **YES — reliability** | ⛔ **REMOVED** → level word only |
| 6 | `#cpp-asr-bar` (How assessable) | Confidence popover | `_RELPCT` → `width:55%` | **YES — reliability** | ⛔ **REMOVED** → level word only |
| 7 | `#cg-feas-fill` (`.caffil`) | **Hero card** CAF row | `style.width = r.feasW + '%'` | **YES — CAF** | ⛔ **REMOVED** → five-step band |
| 8 | `#cg-align-fill` (`.caffil`) | **Hero card** CAF row | `style.width = alignW + '%'` | **YES — CAF** | ⛔ **REMOVED** → five-step band |
| 9 | Clarity `.caffil` (static) | **Hero card** CAF row | `style="width:76%"` | **YES — CAF** | ⛔ **REMOVED** → five-step band |
| 10 | `.cafrow.lim .caffil` | **Hero card** | brand-orange fill | **YES — CAF** | ⛔ **REMOVED** (fill **and** hue) |
| 11 | `#pg-deps-fill` — *Dependencies confirmed **2 / 3*** | Progress card | `width = confirmed/total` | **No** — a **true count**, denominator on screen | ✅ **CORRECT AS-IS**, and **ESCALATED → O-D176-2** (D173b blesses true counts; a must-not-fire control proves the fill guard does not reach it) |
| 12 | Plan artifacts read — *7 / 7* | Progress card | `width:100%` | **No** — a true count | ✅ **CORRECT AS-IS** (a full box is not a metre) |
| 13 | Attention heat cells `.l1/.l2/.l3` | Attention map | *(no fill — severity shading)* | **No — these are ISSUES** | ✅ **CORRECT AS-IS. NOT TOUCHED.** Severity colour belongs to issues (D003/D060) |
| 14 | Usage meters (`3 of 5 projects`) | Limits / Plans | *(no bar at all — text)* | n/a | ✅ correct — already numbers, not metres (D138) |
| 15 | `width:100%` on the popover's "Open full breakdown" button · `width:13px` on ⓘ · census table column widths · the spotlight mask | chrome / layout | layout | No | ✅ **layout, not a measurement** |
| 16 | `.pn` hatch (`rgba(217,164,65,.045)`) | D161 notes rail | — | **Not product copy** | ✅ excluded by design (a guard that graded the governance rail would be grading its own documentation) |

**Nothing else in the product fills to a percentage.**

## The guards (all mechanism proofs — D166)
| Guard | Mechanism |
|---|---|
| `_assertHeroCardCarriesNoSeverityColour()` **(extended)** | The **authored cascade**, chroma-graded, `@media`-aware, inline styles included — **now bans `--primary*` as well**. ⚠️ **Its own negative control forced a scope fix:** a rule with a **bare subject** (`.cr-limit b{color:rgb(217,122,58)}`) was **invisible** to it, because it required the *subject* compound to carry a card class. Bare subjects anchored by an ancestor are now in scope. **Fix the guard, never the doctrine.** |
| `_assertNoPercentageFillOnMaturitySurfaces()` **(new)** | **Three proofs at once:** the **cascade** (any rule mentioning a maturity class), the **DOM** (inline styles under the hero card / popover), and — **the load-bearing one** — the **RENDER PATH**: the source of every painter (`renderOverview` · `renderCafRows` · `renderConfPop` · `renderHero` · `renderRamp` · `_rampHTML` · `_cafRampInto` · `renderFalseConfidence`) must contain **no `style.width`**. *The original fill was written by JavaScript; a cascade-only guard would have been theatre.* Vacuity trap: < 15 rules ⇒ CANNOT VERIFY ⇒ fail. |
| `_assertCafDimensionsRenderAsBands()` **(new)** | Each row's ramp is compared **byte-for-byte** with `_rampHTML(lvl,{compact:true})` for the level **on the read**; five steps, exactly one lit, at `_BANDORD.indexOf(lvl)`; the level word matches; `.lim` is exactly what `_limitingOf()` names — **on both surfaces**. Then **the read is MOVED and the whole grade re-runs** (a hard-coded band passes the first pass and fails this one). Vacuity trap: < 12 dimension-renders ⇒ fail. |

## Verification
| # | Check | Result |
|---|---|---|
| 1 | `node --check` (extracted script) | **PASS** |
| 2 | jsdom **without** `runScripts` | **PASS** — **31** healthy body children (**unchanged**) |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **74/74 green in all four · 0 console errors** (72 → 74: the two new D176 guards) |
| 4 | **Negative controls** (`_d176NegativeControls()`) | **15/15 BITE · 2/2 must-not-fire stay GREEN · 3/3 subjects pass as shipped** |
| 5 | **AA contrast, BOTH themes** — limiter row & CAF ramps | **PASS** (below) |
| 6 | **Percentage-fill sweep** | **16 rows, above — 10 removed, 6 correct-as-is, 2 escalated** |
| 7 | Behavioural (a)–(e) | **PASS** (below) |

**AA (dark / light, both themes):**
| Element | Dark | Light | Floor |
|---|---|---|---|
| Limiter row name + band word (`--text` on `--surface`) | **15.05** | **16.56** | 4.5 |
| Level word + "the limit" marker (`--muted`) | **8.77** | **8.03** | 4.5 |
| CAF ramp **lit** bar (`--text`, meaningful graphic) | **15.05** | **16.56** | 3.0 |
| CAF ramp **unlit** bar (`--subtle` — *it is the scale*) | **5.34** | **5.23** | 3.0 |
| Popover ramp unlit / lit (on `--surface-2`) | **4.67 / 13.15** | **4.75 / 15.05** | 3.0 |
| Popover limiter note (`--subtle` body, `--text` bold) | **4.67 / 13.15** | **4.75 / 15.05** | 4.5 |
| Hero-card links (`--text` + dotted underline) | **15.05** | **16.56** | 4.5 |

*One AA fix made in passing:* the how-calc bullet went from `--primary-light` to `--muted`, not `--subtle`
(`--subtle` on `--surface-3` is **4.12:1**, under the 4.5 floor).

**Behavioural:**
- **(a)** The limiter row is **neutral**: **zero hue in the hero card** — cascade (chroma-graded), inline and DOM all
  clean, `--primary*` included. The limiter is marked by **weight** + the word **"the limit"**.
- **(b)** **No percentage fill on any CAF / confidence / reliability element** — cascade, DOM **and** render path.
- **(c)** The CAF dimensions render as **five-step bands, computed from state**, on **both** surfaces, with the
  limiter marked: at boot *Clarity — step 4 (High)* · *Alignment — step 3 (Moderate)* · *Feasibility — **step 1
  (Very Low) — the limit***. Move the read and every ramp moves (state proof inside the guard).
- **(d)** **The Attention heat map is UNCHANGED** — 21 cells, l1/l2/l3 severity shading intact. Not touched.
- **(e)** **Slices 1–9 + the rest of Slice 10, non-regression:** all 10 views walked, notes toggled, phase advanced,
  confidence popover opened, report generated, a fix applied → **74/74 guards green afterwards, 0 console errors**.

## Escalations (raised, not decided)
- **⬜ O-D176-1 — reliability has no drawn scale, on purpose.** The basis rows lost their fills and now show **only
  their level word**. They were **not** put on the five-band ramp: **D051 states reliability's levels as High /
  Moderate / Low**, while the prototype's `_RELORD` also carries **Very Low**. Drawing a ramp would mean **choosing
  a step count canon has not fixed** — the exact assumption the Anti-Assumption Build Protocol forbids.
  **Owner call: leave it as words · ratify a reliability scale and give it a ramp · or fold it into the five bands.**
- **⬜ O-D176-2 — the Progress card's TRUE-COUNT bars were kept.** *Dependencies confirmed **2 / 3*** and *Plan
  artifacts read **7 / 7*** are partial fills — but each is a ratio OSLO can defend **exactly**, with its
  **denominator printed beside it**, and **D173b explicitly blesses true counts**. They are not on a
  confidence/CAF/reliability surface. A **must-not-fire** control proves the new guard does not reach them, so *"no
  fills"* never quietly becomes *"no counts"*. **But a partial fill is still progress-bar grammar wherever it
  appears (DL-104 §5) — owner call: keep them, or reduce them to the numbers alone.**

## One note on the harness
The D170 guard (`d170AttemptSurfacesPrompt`) reports RED in a **virgin** jsdom session — on the **untouched
baseline** as well as on this build — because `fireUP()` **defers** every prompt until `_firstValue()` (the first
MRI delivered) is true, and a brand-new session has never delivered one. Seed `oslo-s1-firstMRI` (i.e. any session
that has actually seen its first read) and it is **green on both**. **Not a D176 regression** — stated here so the
next worker does not chase it.

---

# D177 — THE HOLLOW PAYOFF, FIXED (2026-07-12)

**The diagnosis held exactly.** `_readSnapshot()` / `_payoffModel()` / `renderPayoff()` were correct; a count that
did not move was correctly omitted. **The Extended pass simply changed nothing countable.** It was a **data**
defect, and it is fixed as one.

## The payoff, verbatim, as rendered — **30 words** (budget 45)

```
What changed
Extended Analysis landed.
Feasibility: Very Low → Low.
Issues 6 → 8   Critical 1 → 2
I looked deeper and found two more. The read is firmer because I know more.
Feasibility is still the limit.
```

Every number computed from state. `learned` / `foundN` are **read off the transitions** — no flag is passed in, so
a run that did not earn the sentence cannot claim it. **DOM order is the argument:** act · band · **counts** · the
line about them · consequence. **No colour token enters `.payoff`, in either direction.**

## The two findings — and why a deeper read of the EXISTING evidence surfaces them

The Fast Pass reads each artifact. **The Deep Pass reads them against each other.** That is what the extra budget
buys, and it is where both of these live. **No new facts; every citation is an artifact already on the record.**

- **ISS-07 · critical · Feasibility · Schedule — "Sponsor funding closes after the costs are committed."**
  *Schedule*: sponsor sales close **Aug 15**; run-of-show freezes **Sep 1**. *Resources*: **AV vendor — Confirmed**,
  **Caterer — Confirmed**. *Intent*: the event is **sponsor-funded**. Read together: **the plan commits the spend
  before the revenue is signed**, and names no minimum floor. Anchored to the `Sponsor sales close · Pending` cell.
- **ISS-08 · moderate · Clarity · Scope — "Recording is resourced but never scoped."**
  *Scope*: recording is in the logistics list, and the event is **in-person only**. *Resources*: the **AV vendor
  does recording**. *Requirements*: **no recording deliverable, capture standard or consent**. Read together: **the
  plan is paying for a deliverable it never defines.** Anchored to the word `recording` in the Scope draft.

**The weak text was always there.** Both spans are authored into `ARTBODY` at boot and left **inert (plain text)**
by `_artBodyLive()` until `_istatus[id]==='open'`. The Fast-Pass draft reads exactly as it did before; **the mark
is what is new.** That is the honest mechanism: *the words did not change, the understanding did.*

## Verification

| Check | Result |
|---|---|
| `node --check` on the extracted script | **PASS** |
| jsdom **without `runScripts`** | **31 body children** (healthy; 1 script tag) |
| Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **ALL PASS in all four**, `deepPassMovesCounts: true` in all four |
| Console errors at boot + self-check | **0** |
| `_d177NegativeControls()` | **9/9 bite**, incl. **the bug itself**; must-not-fire control **green** |
| `_d176NegativeControls()` / `_d164NegativeControls()` | **still all green** — no regression |
| Payoff word count | **30** ≤ **45** |
| The guard leaves no trace | after boot: HISTORY **1** · TREND **1** · chat **0** · ISSUES **6** · `provisional` · payoff hidden |

**Negative controls, each verified to bite:** `theBugItself_deepPassMovesNoCounts` (the pass surfaces nothing and
the payoff claims a deeper read anyway — **the shipped defect**) · `bandDoesNotMove` · `nothingCriticalIsFound` ·
`thePayoffDropsTheCounts` (model moved, surface didn't) · `thePlainLineIsLost` · `aFindingCitesEvidenceThatDoesNotExist`
· `aFindingIsFiledAgainstNothing` · `refusesToGradeNothing` (vacuity). **Must not fire:**
`mustNotFire_moreIssuesAndAHigherBandIsFine` — **green**, because more issues with a higher band **is the shipped
state and it is correct**. A guard that reddened there would be enforcing *"confidence = health"*.

## Behavioural

Issues **6 → 8**, critical **1 → 2** · *Open questions* **stays 2** and is correctly **absent** from the payoff (the
findings carry no clarification) · Attention map **openTotal 8**, **new cell Scope × Clarity**, **Schedule ×
Feasibility now 2 (critical)** · badges/`cf-open`/`pg-crit` all move · Issues list **8 rows** · ISS-07/ISS-08 open a
full panel with evidence, recommendation, paths and share-for-review · both appear in the memo's risks and plan
seed · History gains *"2 further issues surfaced by the deeper read"* and the Extended run's delta carries
`opened: 2` · chat says the same true thing, plainly. **Slices 1–9 and the rest of Slice 10: no regression.**

## Escalations (open-items.md)

**O-D177-1** the demo Deep Pass always finds these two (prototype boundary; nothing assumes *two* — every number is
computed) · **O-D177-2** **owner call: does a Deep Pass ASK QUESTIONS, or only FIND ISSUES?** A clarification on
ISS-07 would legitimately move a third count; D177a's model names two, so **OSLO did not add one on its own
authority** · **O-D177-3** Feasibility **rises** and takes a **second critical** on the same dimension in the same
breath — coherent, and the first place in the product where that happens. **Watch it in usability testing.**

---

# D178 — A DEEP PASS **ASKS**, IT DOES NOT ONLY FIND (2026-07-12 — closes O-D177-2)

> **Finding an issue and knowing what would close it are different acts — and OSLO can do both.**

**The owner answered the escalation I raised as O-D177-2: yes, a Deep Pass asks.** This is the completion of the
D177 demo moment — and it is **one `clar` field plus the transitions that were already there.** No new surface, no
new component, no new count registry.

## What changed

| # | Change | Where |
|---|---|---|
| 1 | **The ask.** `DEEP_FINDINGS['ISS-07'].clar` — *"Is there a minimum signed-sponsorship floor — or a cancellation point — that has to be cleared before the AV and catering commitments go firm?"* Same field, same shape as ISS-01/ISS-02. | `DEEP_FINDINGS` |
| 2 | **The third true count.** **Nothing was added.** `_openClarIds()` already backs the `questions` row of `PAYOFF_COUNTS`, so surfacing ISS-07 moves **Open questions 2 → 3** by itself. | *(no code)* |
| 3 | **`asked`** — the **rise** in the `questions` row, read off the transitions exactly like `learned`. **No flag is passed in**: a pass that raised nothing cannot claim an ask, and **answering** (the row *falls*) yields `asked = 0`. | `_payoffModel()` |
| 4 | **`_payoffNote()`** (new) — assembles the note from the transitions; each clause is spoken **only if the count behind it moved**. | `_payoffParts()` |
| 5 | **The ask cannot outlive its count** — if the budget ever trimmed the `questions` row, `asked` is dropped with it. | `_payoffFit()` |
| 6 | **The pass raises it in the chat too**, collapsed — `postDeepPassComplete(found, crit, asked)` ends with `_chatClarBlock(id)`. Derived from `_found.filter(id => ISSUES[id].clar)`. | `deepComplete()` |

## THE PAYOFF, VERBATIM AS RENDERED — **39 words** (budget 45)

> **What changed**
> **Extended Analysis landed.**
> **Feasibility: Very Low → Low.**
> Issues **6 → 8**   Critical **1 → 2**   Open questions **2 → 3**
> *I looked deeper and found two more. I have one more question. The read is firmer because I know more.*
> **Feasibility is still the limit.**

**Every number computed.** `before {issues:6, critical:1, questions:2}` → `after {issues:8, critical:2,
questions:3}`; `asked = 1`, `foundN = 2`, both equal to the state deltas. **No meta, no doctrine vocabulary. Never
apologetic, never alarmed** — the ask renders in the **same** classes and weight as a rise and a fall (D003/D173c).

## The clarification, and the evidence it rests on

**⛔ No fabricated facts.** The question **re-reads the evidence ISS-07 already cites** and asks about **what is
absent from those inputs**:

| evidence (already on the record) | what it says |
|---|---|
| **Schedule** | *"Sponsor sales close **Aug 15**"* · *"Run-of-show final Sep 1"* |
| **Resources · Vendors** | *"AV vendor — **Confirmed**"* · *"Caterer — **Confirmed**"* |
| **Intent** | *"A **sponsor-funded** event for ~450 attendees"* |

The plan commits the spend before the revenue is signed — and **states no floor and no cancellation point.** So
OSLO asks for exactly that. **It does not know the answer, and it says so.** Answering closes the gap through an
**analysis update — never by hand** (`open → Addressed → (analysis update) → Resolved`, D088).

## VERIFICATION

1. **`node --check`** on the extracted script → **PASS**.
2. **jsdom without `runScripts`** → **31 healthy body children** (unchanged).
3. **Boot assertions** — **75/75 pass, 0 console errors**, on **Free × Basic × notes-OFF × notes-ON** (all four).
4. **Negative controls — every one bites.** `_d177NegativeControls()` = **13/13 true**, incl. the three new ones:
   - **NC-D178-01 `theDeepPassAsksNothing`** — the pass raises **no clarification** → **guard RED** ✅
   - **NC-D178-02 `thePayoffSwallowsTheAsk`** — the count moved and the payoff never said so → **RED** ✅
   - **NC-D178-03 `osloAssertsInsteadOfAsking`** — the `clar.q` becomes an assertion (*"the floor is $250k"*) → **RED** ✅
   - **must-not-fire `mustNotFire_moreIssuesAndAHigherBandIsFine` → GREEN.** *More issues **and** a higher band is
     the shipped state and it is CORRECT.* A guard that reddened there would be enforcing **"confidence = health"**.
   - Non-regression: `_d170NegativeControls()` **26/26** · `_d164NegativeControls()` **47/47** ·
     `_d176NegativeControls()` **17/17** — all green.
5. **Behavioural** (jsdom, real `deepComplete()`):
   - **(a)** the pass raises **1 clarification**, bound to **ISS-07**, citing **Schedule · Resources · Vendors · Intent** ✅
   - **(b)** `_openClarIds()` `[ISS-01, ISS-02]` → `[ISS-01, ISS-02, **ISS-07**]` — **Open questions 2 → 3**, computed ✅
   - **(c)** answered in the **panel** and in the **chat** → History entries compared field-for-field: **BYTE-IDENTICAL** ✅
   - **(d)** both paths: `open → addressed → (analysis update) → resolved`. **Never resolved by hand** ✅
   - **(e)** renders **collapsed**: panel row `aria-expanded="false"`, no `.open`; chat `.chat-clar` has no `.open` ✅
   - **(f)** post-answer payoff correctly reads **`Open questions 3 → 2`** and carries **no ask sentence**
     (`asked = 0`) — **the ask cannot outlive its count** ✅

## ⛔ A GUARD MUST LEAVE NO TRACE — one real trap, closed

The real pass now **raises a clarification in the chat**, and raising one **retires any earlier live answer box for
that issue** (`_retireClarBoxes` — otherwise duplicate DOM ids make the newest answer silently fail). Run **inside a
guard**, that would have reached into the **user's own thread** and **disabled a box they were about to type into**.
`_CHAT_PROBE` already exists to fence exactly this housekeeping; the guard now raises it around the real
`deepComplete()`. **Verified: the live `chatClarBox-ISS-07` is byte-for-byte unchanged after the guard and all 13
controls run** (D166).

## Open items

- **O-D177-2 — CLOSED.**
- **O-D178-1** the demo pass asks exactly **one** question (prototype boundary — nothing assumes *one*; `asked`
  scales and the copy pluralises).
- **O-D178-2** a clarification is a **property of an open issue** (`_openClarIds()` filters on `_istatus`), so
  there is **no home for an ask not tied to a finding**. **Not invented — owner call if it is ever needed.**
- **O-D178-3** ISS-07 now carries **both** a recommendation and a question, and D162b shows **one** primary action
  (**Apply this fix**), so **Answer** is not the primary — the ask still renders as a collapsed row *and* rides the
  chat turn. **Consistent with ISS-01, which has the same shape.** Flagged because ISS-07 is the first **critical**
  where *the question is arguably the better first move than the fix.* **Watch in usability testing; the fix, if
  any, is a D162b amendment — not a special case for one issue.**

**No tension with canon.** D178 is built exactly as ratified; nothing was inferred.

---

# D179 — OVERVIEW LAYOUT REDESIGN (owner, 2026-07-12)

**Four owner findings, all correct. Amended in place in `vertical-slices/slice-10-tiering-limits/prototype.html`.**

**RESULTING LAYOUT: HERO (state) → PAYOFF (the event: dismissible, movement on the ramp, ≤20 words) → PROGRESS (the counts, one home, deltas annotated).**

## What changed

| Finding | Fix |
|---|---|
| **D179a — the state always outranks the event** | The payoff card was authored **above** the hero. It is no longer a card, and **`.card.hero` is the first panel of the Overview**. Guarded on **DOM order**. |
| **D179b — the payoff is a DELTA, not a panel** | It renders **inside `.card.hero`, under `.conf-focus`** — a strip, not a card. **Dismissible**; **not persisted** (no storage on any payoff path). `dismissPayoff()` clears the strip **and the ghosts**. |
| **D179c — make it visual** | The movement is **drawn on the ramp**: previous band **ghosted**, current **lit**, **arrow** between (`⟶` / `⟵`). `_rampHTML(band,{prev})` is the one builder; `_MOVE` is computed by `renderPayoff()` from the **`before` snapshot**. **Word budget 45 → 20.** |
| **D179d — neutral ≠ monochrome** | New token **`--maturity`** (`#7FA0C9` / `#3F6193`) — **a cool accent, outside the RAG vocabulary** — on the lit step, the band word, the limiter marker and the arrow. **`--primary` restored to LINKS ONLY**, graded by subject. **Severity colour untouched on issues.** |
| **D179e — counts have one home** | The counts moved to **Progress**, with **computed deltas** (`Issues 8 ↑2`), all through the **`PAYOFF_COUNTS` registry**. Removed from: the payoff, the confidence footer, the clarification pointer, the "See all N" link. **Two fabricated counts deleted** (`Dependencies confirmed 0/3` + fill; `Plan artifacts read 7/7` + fill). |

## The payoff, verbatim as rendered — **19 words** (budget 20)

> **WHAT CHANGED** ✕
> **Extended Analysis landed.**
> *I looked deeper: found two more, and one more question. The read is firmer.*

Plus, on the Feasibility ramp: **⟨Very Low⟩ ⟶ [Low]** · and in Progress: **Issues 8 ↑2 · Critical 2 ↑1 · Open questions 3 ↑1**.
*(The hero ramp draws **no** ghost: the overall band held at Moderate. **Never fake a movement that did not happen.**)*

## Count-location table — **no count is rendered twice**

| Count | Value (after the Extended pass) | Rendered where | Rendered more than once? |
|---|---|---|---|
| Issues | 8 ↑2 | `.pg-chip` (Progress) | **NO** |
| Critical | 2 ↑1 | `.pg-chip` (Progress) | **NO** |
| Open questions | 3 ↑1 | `.pg-chip` (Progress) | **NO** |
| Confirmed artifacts | 0 / 7 | `.pg-chip` (Progress) | **NO** |
| *0–100 index (62)* | — | `#ov-idx` (hero) | *not a count — a secondary, uncalibrated aggregate (DL-062 F1)* |
| *nav badges (8)* | — | `#vsAttnBadge` / `#vsIssuesBadge` — **left nav rail, outside `#pane-overview`** | *wayfinding, not a count home (O-D179-6)* |

**Deleted homes:** confidence footer (*"6 issues open · 0 resolved"*) · Progress ledger numbers · `Dependencies confirmed 0/3` · `Plan artifacts read 7/7` · clarification pointer (*"OSLO has **2** things to confirm"*) · *"See all **8** open issues"*.

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | **PASS** |
| 2 | jsdom **without `runScripts`** | **31 healthy body children**; Overview panels in DOM order = **Confidence → Start here → Progress**; `#payoff` is **not** a `.card`; parent chain `payoff < card hero < uc < pane`; **no numbers and no band words in the Progress/ramp markup** |
| 3 | Boot assertions — **Free × Basic × notes-OFF × notes-ON** | **83/83 PASS in all four**, **0 console errors** |
| 4 | Negative controls | **`_d179NegativeControls()` 28/28 bit** (incl. all four owner findings re-injected) · **`_d176NegativeControls()` 17/17** · **`_d177NegativeControls()` 13/13**. **Must-not-fire stayed green: issue severity · the cool accent · MORE ISSUES + A HIGHER BAND.** |
| 5 | AA contrast, both themes | **0 failures.** Lit step / band word / limiter marker / arrow **6.13:1 dark · 6.28:1 light** · payoff label on its strip **4.87 / 5.45** · hero links **7.20 / 5.93** · delta chip **4.67 / 4.75** |
| 6 | Payoff verbatim + word count | **19 / 20** (above) |
| 7 | Count-location table | **above — every count: NO** |
| 8 | Behavioural | (a) Confidence **first** ✅ (b) payoff **inside** the card, dismissible, not persisted ✅ (c) movement **on the ramp** (ghost · lit · arrow) ✅ (d) Progress carries the counts with **computed** deltas ✅ (e) **no count duplicated** ✅ (f) cool accent, **no severity colour, no fills** ✅ (g) **Slices 1–9 + rest of Slice 10 non-regression**: every view renders, 0 errors, **83/83 after visiting all of them** ✅ |

## Two REAL defects found — both **guard** defects, both **order-dependent** (D166)

Neither was a product defect. Both guards were **green at boot and would have gone red the moment a user acted** — the classic shape D166 names.

1. **`_assertDeepPassMovesBandAndCounts()` could not survive a user fix.** `applyFix()` **mutates `READ.provisional`** (raising `feasW` — correctly). After one fix, **the Fast-Pass read no longer exists in the model**, and the guard, which must run the Extended pass *from* that read, had nothing honest to run from. **Fixed:** `_READ0` freezes the read at load, and the guard stages **only the pass's INPUT** (`READ.provisional`) — leaving `READ.current`, the pass's **output**, exactly as it stands, so a control that breaks the output (**NC-D177-02: *the band does not move***) is still fully visible. *(The first draft staged the whole `READ` and silently killed that control — caught by re-running the D177 suite: **a guard that resets what a control injects into is a guard that can no longer fail.**)* **Self-check is now 83/83 after a fix, a clarification answer and the deep pass, in any order.**

2. **`_assertChatOpeningIsShort()` never graded the Extended pass's own issues** — it walked `ISSUES`, and **ISS-07 / ISS-08 do not exist until the pass runs**. **The newest copy in the product was the one copy no word budget could see**, and **ISS-07's chat opening was 57 words against a budget of 50** (D167/D163). **Fixed both ends:** the sentence is split (nothing lost — the run-of-show detail moves to the second sentence, still shown in full in the panel), **and the guard now stages `DEEP_FINDINGS` into `ISSUES` for the length of the check** and **refuses to run** if a deep finding is not being graded.

**A third, in my own new guard, caught by the behavioural harness:** `_countSinksOnOverview()` first counted `Confirmed artifacts 1 / 7 ↑1` as **two** renders (the value and the delta are two *leaves* of **one** chip) and went red on a correct surface. **The host is the unit, not the leaf.** Fixed and documented in the guard.

## Tension — escalated, not invented

- **D179c says "then the count deltas as chips (they already work — keep them)"; D179e says counts live in Progress and *"What changed" keeps ONLY the band movement and the one-line reason*** — and the required guard says **no count may be rendered twice**. **These cannot all be true of the payoff strip.** Resolved in favour of **D179e + the stated RESULTING LAYOUT + the guard**: the **chips are kept** (the mechanism, the visual form, the computed deltas) and they **live in Progress**. The payoff strip carries **no counts**. Flagged here because it is a reading, not a transcription.
- **"Artifacts read 7/7" does not exist in the model and is NOT invented** (O-D179-1). The Progress row ships the honest neighbour — **`Confirmed artifacts 0 / 7`**, computed from `basis === 'attested'` — and the hard-coded `7 / 7` is deleted. In **partial-analysis** mode (D139/UP-4) a hard `7 / 7` would be **false on the one surface where honesty matters most**. **Owner decision owed if "artifacts read" is wanted as a count.**
- **"Issues resolved" is no longer shown** (O-D179-3) — D179e names the Progress row exactly and resolved is not in it. It is derivable and still reachable (Attention map · History). **One row in `PAYOFF_COUNTS` if the owner wants it back.**
- **Reliability has no ramp** (O-D179-4) — canon states no scale for it, so a reliability move is the one transition that still travels in **words**. It does not occur in the demo data.
- **`--maturity` is a new token** (O-D179-5) sharing a hue with the existing `--cool`. **Owner: confirm the name and whether they stay distinct.**


---

# D180 — PROGRESS IS GROUNDING, NOT CLEARING (owner: approved, 2026-07-12)

**Amended IN PLACE:** `vertical-slices/slice-10-tiering-limits/prototype.html`. **No regressions.**

## The panel, verbatim (as rendered, notes OFF)

**At boot — 25 words, zero arrows (no previous run ⇒ no delta):**

```
Progress                                                    (i)
GROUNDED   0 of 7 artifacts rest on your evidence
OPEN       Issues 6 · Critical 1 · Open questions 2
CLOSED     Issues resolved 0 · Questions answered 0
```

**After the Extended pass, then one applied fix — 41 words:**

```
Progress                                                    (i)
GROUNDED   1 of 7 artifacts rest on your evidence   ↑1
OPEN       Issues 7 ↓1 · Critical 1 ↓1 · Open questions 2 ↓1
CLOSED     Issues resolved 1 ↑1 · Questions answered 0

The arrows are the change since the last analysis update. Timeline →
```

**And the moment that carries the doctrine — the Extended pass alone (grounding held, issues rose, the read firmed):**

```
GROUNDED   0 of 7 artifacts rest on your evidence
OPEN       Issues 8 ↑2 · Critical 2 ↑1 · Open questions 3 ↑1
CLOSED     Issues resolved 0 · Questions answered 0
```
*(with Feasibility ⟨Very Low⟩ ⟶ [Low] on its ramp, and the payoff line: "I looked deeper: found two more, and one
more question. The read is firmer.")*

## Number provenance — every number on the Overview

| Number | Surface | Computed from state? | Rendered exactly once? |
|---|---|---|---|
| **GROUNDED numerator** (`1`) | Progress · `.pg-say[data-count-key=grounded]` | **YES** — `PLAN_SECTIONS.filter(p => p.basis === 'attested').length` | **YES** |
| **GROUNDED denominator** (`7`) | same host | **YES** — `PLAN_SECTIONS.length` (a real population, not a constant dressed as progress) | **YES** |
| **Issues** (`7`) | Progress · `[data-count-key=issues]` | **YES** — `Object.keys(ISSUES).filter(_active).length` | **YES** |
| **Critical** (`1`) | Progress · `[data-count-key=critical]` | **YES** — active + `sev === 'critical'` | **YES** |
| **Open questions** (`2`) | Progress · `[data-count-key=questions]` | **YES** — `_openClarIds()` (clar-bearing, unresolved, **unanswered**) | **YES** |
| **Issues resolved** (`1`) | Progress · `[data-count-key=resolved]` **(CLOSED row)** | **YES** — `_istatus[id] === 'resolved'` | **YES** |
| **Questions answered** (`0`) | Progress · `[data-count-key=answered]` **(CLOSED row)** | **YES** — `_clarAnswered` (written only by `_submitClarification`) | **YES** |
| **Every delta** (`↑2`, `↓1`) | Progress | **YES** — `live − _PREV_RUN` (the snapshot before the last run). **No previous run ⇒ no delta.** | **YES** |
| **`58 / 100`** (the index) | Confidence hero (secondary, demoted) | **YES** — `currentRead().idx`; **carries no delta** (D056/D173d) | **YES** |
| *"…the **450** target"* | Hero limiter cause | **YES** — a quoted plan fact, not a count | **YES** |

**Everything else on the Overview points; it does not tally.** `_assertNoCountIsRenderedTwice()` grades **all six**
registry counts across the whole pane (vacuity floor raised 3 → 6).

## Verification

1. **`node --check`** on the extracted script — **PASS**.
2. **jsdom WITHOUT `runScripts`** — **31 body children** (healthy).
3. **Boot assertions — 87/87 PASS, 0 console errors**, across **Free × Basic × notes-OFF × notes-ON** (4/4 combos).
   View sweep (overview · attention · artifacts · issues · history · projects · reports · limits · chat) clean.
4. **Negative controls — every one bites:** `_d180NegativeControls()` **19/19 true** (incl. the burndown controls and
   the constant); `_d179NegativeControls()` **28/28**, `_d177NegativeControls()`, `_d176NegativeControls()` — all
   still true. **The must-not-fire controls stay green:** *more issues + a higher band* (D177) **and** *grounding
   rising while the issue count rises* (D180c).
5. **AA contrast, both themes** — `.pg-k` **5.34 / 5.23** · `.pg-say` **8.77 / 8.03** · `.pg-say b` **15.05 / 16.56** ·
   `.pg-chip` **7.67 / 7.29** · `.pg-chip b` **13.15 / 15.05** · `.pg-d` **4.67 / 4.75** · `.prog-since` **5.34 / 5.23**.
   **Zero failures.**
6. **Behavioural (jsdom, real paths — no stubs):**
   (a) **GROUNDED rises** on `_submitClarification()` (0 → 1 ↑1) **and** on `applyFix()` (0 → 1 ↑1);
   (b) the Extended pass moves **Issues 6 → 8 ↑2 · Critical 1 → 2 ↑1 · Open questions 2 → 3 ↑1** while the read
       **firms** — and **nothing reads as regression** (identical delta class on every row, no severity colour in the
       Progress cascade, no regression vocabulary);
   (c) ***resolved* is present, in CLOSED, with no denominator / % / "remaining"**;
   (d) **no "artifacts read 7/7"** and **no other constant** — proven by perturbing state and requiring every row to move;
   (e) **no fills, no severity colour, no burndown grammar** (registry · copy · DOM · cascade · render path);
   (f) **Slices 1–9 + the rest of Slice 10 — non-regression** (87 boot assertions include every prior guard).

## Guard work (D166 — mechanism, negative control, fix the guard never the doctrine)

- **NEW `_assertGroundingRisesWhileIssuesRise()`** — the **state proof**. It grounds a real artifact (flips `basis`
  to `attested`) **while** surfacing real issues and a real question, then requires **GROUNDED to rise** and
  **nothing to treat the rising issue count as a regression**. Baseline (`_PREV_RUN`) is set inside the probe so the
  **arrows actually render** — without it the guard would have graded a panel with no deltas on it and passed for
  free (the D166 §1 vacuity, caught by its own negative control).
- **NEW `_assertNoBurndownGrammar()`** — four doors: **registry** (a denominator on an OPEN/CLOSED count *is* a
  burndown) · **copy** · **DOM** (`<progress>`/`<meter>`/`role=progressbar`/inline % fill) · **cascade + render path**
  (the door the CAF bars came through, D176b).
- **NEW `_assertNoConstantDressedAsProgress()`** — **perturbs state and requires every rendered row to move.** A
  registry row returning `PLAN_SECTIONS.length` ("artifacts read 7/7", *computed* but immovable) goes **red**. This is
  the guard that makes D180b enforceable rather than aspirational.
- **NEW `_assertClosedIsNeverATarget()`** — *resolved* exists, is computed, sits in CLOSED, and carries no
  denominator/%/"remaining".
- **STRENGTHENED `_assertNoCountIsRenderedTwice()`** — six counts now, and two share a noun (*Issues* / *Issues
  resolved*). Each Progress host **declares** its count (`data-count-key`) and is graded for that count alone;
  **hosts that declare nothing are prose and are still graded on the noun**, so the shipped footer defect
  (*"8 issues open"*) still bites. **Without this, the guard would go red on a correct surface the moment two counts
  coincided** — the D166 failure in reverse.

## ⛔ ESCALATION — a REAL defect found, NOT fixed (it is an owner call)

**O-D180-1 — the chat's *"What's it resting on?"* pull turn is 41 words against a budget of 40 — and the overflow is
CITED EVIDENCE.**
**Repro:** boot → Extended pass → `applyFix('ISS-01')` → `_assertChatPullTurnsAreShort()` goes **red**. The top open
issue is then **ISS-07** (a D177 deep finding) whose evidence answer carries **three cited lines**.
**It is NOT a D180 regression** — it reproduces byte-for-byte with the pre-D180 `_openClarIds()` restored at runtime,
and D180 touches neither the chat nor the evidence copy.
**It is the D166 vacuity, one surface over:** `_assertChatPullTurnsAreShort()` grades only the **boot** state's top
issue — so **the newest copy in the product is again the one copy no budget guard can see** (E-D179-12 fixed the
*opening* guard and left the *pull* guard un-staged).
**Not resolved here, because it is a doctrine-level trade:** **D163 (word budgets) vs D177/D178 (cite the evidence)**.
Three honest options — raise the budget for evidence turns · exclude citation chips from the word count (the same
reasoning that already excludes chips and actions) · cap the citations shown. **DO NOT ASSUME.**

## Docs updated

`frontend-ui.md` · `user-experience.md` · `success-criteria.md` (C-D180-1..8) · `e2e-test-scenarios.md` (T-D180-1..5) ·
`edge-cases.md` (E-D180-1..9) · `open-items.md` — **O-D179-1 CLOSED** (the constant is killed) · **O-D179-3 CLOSED**
(*resolved* restored under CLOSED, fenced) · **O-D180-1/2/3 opened**.

---

# DL-109 — Surface the provenance · reject the debt frame (2026-07-13)

**Ratified canon:** `00_owner/decisions/records/DL-109-surface-provenance-reject-the-debt-frame.md`.
**Amended in place:** `vertical-slices/slice-10-tiering-limits/prototype.html`.

## What was built

**A `CONTEXT_ITEMS` model that mirrors the ratified data model** (`ContextItem.item_type` ∈ *claim · assumption ·
relationship · entity · metric · interpretation*; **nullable `evidence_id`**; `extraction_horizon` fast/deep).
**69 items, every one traceable to a real artifact or a real span already on the record** — `ev:'EV-01'` items are
sentences in the pasted brief, `ev:null` items are all findable in `ARTBODY`. **No fabricated facts.**

| § | Built |
|---|---|
| **2a** | **The GROUNDED row is CLAIM-LEVEL** — *"Your evidence: 17 claims · I inferred: 11."* The Reliability qualifier, made countable. |
| **2b** | ⭐ **LOAD-BEARING INFERENCES** — *"11 things I inferred are holding up your plan."* **Computed. Given weight.** |
| **2c** | **The assumption register** — and **the Readout's "Key assumptions" is repointed at it**, off the clarification proxy. |
| **2d** | **Structural counts** — 4 assumed dependencies · 5 unowned parties · 3 sourceless metrics. |
| **2e** | ⭐ **THE INFERENCE MAP** — a new peer surface beside the Attention map. |
| **2f** | **"What I'd need to be sure"** — Readout §5, the unbacked load-bearing items **as asks**. |
| **4a/4b** | **Ageing** and **grounding velocity** — real timestamps, a direction, never a target. |

## THE NUMBER-PROVENANCE TABLE

| Number | Computed from state? | Rendered exactly once? |
|---|---|---|
| **Grounded claims (17)** — `type='claim' AND evidence_id IS NOT NULL` | **YES** — `_ciGroundedClaims()`, through `_ciEvidenceId()` | **YES** — Progress, `data-count-key="grounded"` |
| **Inferred claims (11)** — `type='claim' AND evidence_id IS NULL` | **YES** — `_ciInferredClaims()` | **YES** — Progress, `data-count-key="inferred"` |
| ⭐ **Load-bearing inferences (11)** — `IS NULL AND (critical issue OR limiting dim)` | **YES** — `_ciLoadBearingItems()`; **state proof: bind an inferred item to a critical issue and it rises by one** | **YES** — Progress, `data-count-key="loadbearing"` |
| **Assumed dependencies (4)** | **YES** — `_ciAssumedDeps()` | **YES** — Inference map · Structure |
| **Unowned parties (5)** | **YES** — `_ciUnownedEntities()` (no incoming `owns`) | **YES** — Inference map · Structure |
| **Sourceless metrics (3)** | **YES** — `_ciSourcelessMetrics()` | **YES** — Inference map · Structure |
| **Per-artifact grounded / inferred (7 rows)** | **YES** — `_ciArtStats()`; **the pips equal the model, proven per row** | **YES** — Inference map |
| **Assumption ages** | **YES** — `_ciAgeMs()` off the producing run's stamp | **YES** — the register |
| **"N issues depend on it"** | **YES** — `_ciActiveSup()` (open issues only) | **YES** — the register |
| **Velocity (you 0 · I 37)** | **YES** — `_ciVelocity()`, windowed on the last run | **YES** — Inference map |
| **The flagged artifact (Scope)** | **YES** — `_ciFalseConfidentArtifacts()`; **ground it and the flag goes** | **YES** — the flag + the row's Verify tag |

**All YES / YES.** Nothing is typed in; there is nowhere to type one in.

## THE INFERENCE MAP'S FLAGGED ARTIFACT — **SCOPE**

> **Scope reads strong, and most of it is mine — 4 of its 7 items are inference. Worth verifying first.** → **Open Scope →**

**Why Scope, and why it is the right finding:** OSLO's own reliability on Scope is **High**, and nothing critical is
open in it — **it looks fine.** And **the brief says one word: *in-person*.** From that, OSLO wrote **an entire
out-of-scope boundary**: *a virtual or hybrid stream is out of scope · no remote attendance is planned · the
boundary applies to this year.* **None of it is in anything the user gave OSLO.**

> ## ⛔ **It looks fine BECAUSE OSLO invented a coherent story. Coherence is not evidence.**

**It discriminates.** Intent is also **High** reliability and also derived — and it is **not** flagged (5 grounded /
4 inferred). **Resources** is the most inferred artifact in the plan (5 / 10) and is **not** flagged either —
because it **does not read strong** (reliability Low, a critical issue open). **The finding is the intersection, and
the intersection is the dangerous one.**

## NEGATIVE CONTROLS — `_d109NegativeControls()` · **22/22 TRUE**

**Every injected regression bites:**
`theRejectedFrame_understandingDebtReturns` (AE-06, by name) · `theFrame_inThePainter` · `theFrame_inTheRegistry`
(the count **renamed** as a liability) · `theFrame_aDebtClassInTheCascade` · **`theNumberIsTyped`** (the
load-bearing count becomes a constant — *it still looks right on screen*) · `theNumberIsHidden` ·
`theMapBecomesABar` · **`inferenceIsPaintedAsSeverity`** (the inferred pip goes amber — *the debt frame arriving as
a colour*) · `thePipsStopCounting` · **`theFindingIsHardCoded`** · `theFindingIsSilent` · **`theProxyReturns`** (the
Readout goes back to reading clarifications) · **`theChainIsSmuggledIn`** (`derived_from` appears on a ContextItem).

**MUST-NOT-FIRE — both stay GREEN:**
**`mustNotFire_moreInferencesAndAHigherBand`** — the deeper read runs, **the inference counts RISE**, and
**six guards stay green through it** (debt · burndown · grounding-property · map-neutrality · load-bearing ·
no-constant). **A rising inference count is not a regression, and no guard treats it as one.**
`mustNotFire_groundingRisesWhileIssuesRise`.

## Verification

1. **`node --check` → PASS.**
2. **jsdom without `runScripts` → 31 body children.** Healthy.
3. **95 boot assertions · ALL TRUE · 0 console errors** — Free × Basic × notes-OFF × notes-ON, **and** after the
   Extended pass, **and** after the user grounds artifacts.
4. **Negative controls: D109 22/22 · D180 19/19 · D179 28/28 · D177 13/13 · D176 17/17 · D170 26/26 · D164 47/47.**
   **Every control bites; every must-not-fire stays green.**
5. **AA both themes.** Worst case **5.23 : 1** on text. **One real AA defect found and fixed:** the inferred pip's
   edge was **1.58 : 1** — below the **3:1 non-text minimum** for a mark that carries information.
6. **Behavioural:** GROUNDED is claim-level ✅ · load-bearing computed and prominent ✅ · the register exists and the
   Readout reads it ✅ · the Inference map renders and **names Scope** ✅ · ageing + velocity present ✅ · **zero debt
   vocabulary** ✅ · a rising inference count reads neutrally ✅ · **Slices 1–9 + the rest of Slice 10: no
   regressions** ✅.

## ⚠️ THREE GUARD DEFECTS FOUND BY THE GUARDS' OWN RUNS (D166 §3 — fix the guard, never the doctrine)

1. **The debt scanner matched SUBSTRINGS.** *"lowest"* contains **"owes"**; *"reliability"* contains
   **"liability"**. It went **red on the Confidence hero — a surface that is entirely correct.** **A guard that
   fires on a correct surface is the D166 failure in reverse**, and the temptation at that moment is to soften the
   doctrine. **The doctrine was right; the matcher was lazy.** Word boundaries.
2. **Two guards were ORDER-DEPENDENT — green at boot, red after the user did the right thing.** The rising-inference
   proof re-ran the real deep pass (a second run finds nothing new, so it declared itself vacuous), and every probe
   item was pinned to the **Scope** artifact — **so the moment the user GROUNDED Scope, the probe items became
   grounded too and the counts stopped moving under them.** Both fixed: the rise is now **constructed** in any
   state, and probe items hang off an artifact that is not in the plan.
3. **The false-confidence guard called the user's own success a failure.** Ground the flagged artifact and the
   condition is *legitimately* gone — the first draft reported "GUARD IS VACUOUS" and went red. **A guard that
   punishes the user for doing the work is a guard defect.** It now **constructs** the condition itself, both ways.

## ⛔ ESCALATED — NOT INVENTED

- **O-DL109-1 — the demo history is young.** §4a wants *"unvalidated for six weeks."* **The ageing mechanism is
  real and computed** — but this project's Initial run is stamped **`now − 2m`** (a fresh signup → intake → first
  analysis), so the surface honestly says **"Unvalidated for 2 minutes."** **OSLO does not invent a longer past to
  make a surface look better.** Owner call: age the demo project (touches Slice 7's D100 first-run state), or accept
  minutes in the demo.
- **O-DL109-2 — inference chains.** `derived_from` is **not in the schema**. **Not approximated, not faked** —
  guarded against.
- **O-DL109-3 — "load-bearing" second clause.** *"Bears on the limiting dimension"* is implemented as
  `item.dim === limiting`. A stricter reading (*"supports an open issue on the limiting dimension"*) would give a
  smaller number. **Which one the owner means is the owner's.**
- **O-DL109-4 / O-DL109-5** — *unowned entity* is derived from an `owns` relationship **that is itself OSLO's
  inference**; *assumed dependencies* counts `depends` links only. **Both stated, not assumed.**

## Docs updated

`product-data.md` (the context plane) · `frontend-ui.md` (Progress + the Inference map + AA) · `user-experience.md` ·
`success-criteria.md` (C-DL109-1..12) · `e2e-test-scenarios.md` (T-DL109-1..11) · `edge-cases.md` (E-DL109-1..12) ·
`open-items.md` (**O-D180-2 amended**; **O-DL109-1..5 opened**).

---

# D181 — "LOAD-BEARING" = THE READ POINTS AT IT · AGE THE CLOCK, NOT THE PAST (owner, 2026-07-13)

Closes **O-DL109-3** and **O-DL109-1**. Amends the Slice-10 prototype **in place**.

## D181a — THE NUMBER, WITH ITS CLAUSES BROKEN OUT

> **AN INFERENCE IS LOAD-BEARING IF THE READ WOULD CHANGE WERE IT FALSE. Operationally: THE READ POINTS AT IT.**

| | Clause | Boot | After the Extended pass |
|---|---|---|---|
| **(a)** | a **CRITICAL ISSUE** cites it (`_ciLB_a`) | **3** — CI-58 · CI-60 · CI-62 | 7 |
| **(b)** | the **LIMITING DIMENSION's** assessment rests on it **and something open actually rests on it** (`_ciLB_b`) | **8** | 12 |
| **(c)** | ⭐ a **STRONG-READING ARTIFACT's** confidence rests on it — **false confidence** (`_ciLB_c`) | **4** — **CI-20 · CI-21 · CI-22 · CI-23 (SCOPE)** | 8 |
| | **THE NUMBER (union)** | **BEFORE: 11 (loose) → AFTER: 12** | **20** |

**THE SCOPE PROOF (explicit).** Scope reads **High** reliability, has **no critical issue open**, and is **not** the
limiting dimension — **the strict definition would have excluded it entirely**, on the artifact the Inference map
flags as *the most dangerous thing in the plan*. **Clause (c) puts its four inferences in the number**, and the guard
grades them **by identity** (`_assertLoadBearingIsComputed()` requires **every** inference of **every** flagged
artifact to be in `_ciLoadBearingItems()`), live **and** constructed.
***Scope reads fine BECAUSE OF four things OSLO made up.***

**The over-count is gone:** the loose reading's **11** included **CI-45 · CI-56 · CI-57** — inferences bearing on
Feasibility that **nothing points at**. They are inferences; **they are not holding anything up.** Not counted.

**ONE DOOR.** `_ciLB_c` reads **`_ciFalseConfidentArtifacts()` — the same function the map's flag reads.** The number
and the flag can never disagree, and **grounding the flagged artifact retires both together.**

## D181b — AGE THE CLOCK, NOT THE PAST

**The demo project is NOT back-dated.** `simNextWeek()` now advances **the clock** (`RPT.week` → `_demoWeeks()` →
**`_ciNow()`**, the single "now" every provenance surface reads).

- **The assumptions AGE:** *"Unvalidated for **2 minutes** · 1 issue depends on it"* → after three weeks →
  ***"Unvalidated for 3 weeks · 1 issue depends on it."*** **Computed from the clock, never typed.** The
  dependent-issue count is computed from `_ciActiveSup()`.
- **Grounding velocity moves with the weeks** — the window is the current demo week. Three weeks on with nothing
  done: **0 · 0**, *understanding is stalling*, honestly. **A direction, never a target.** (Card header: **This week**.)
- **The timeline ages on the same clock** (`HISTORY.H0` carries a real `at`; its `ts` is computed) — so no surface can
  call the same run *two minutes old* while the register calls it *three weeks stale*.
- **At week 0 the offset is ZERO. D100 holds byte-for-byte** (`now − 2m`; ages in minutes).

## GUARDS (D166 — mechanism, negative control mandatory)

**New/rewritten:** `_assertLoadBearingIsComputed()` (all three clauses, state proofs) ·
`_assertSimNextWeekAgesTheAssumptions()` · `_assertD100FirstRunStateHoldsAtWeek0()`.

**⚠️ A GUARD DEFECT CAUGHT BY ITS OWN MUST-NOT-FIRE CONTROL (the 17th).** The first draft of the clause-(c) proof read
the **live** flag — so the moment the user **GROUNDED Scope** (the very thing OSLO asked them to do), no artifact
qualified, the guard reported *"cannot verify"* and went **RED ON A CORRECT PRODUCT**. *That is the defect D181a
names by hand: calling the user's success a failure.* **Fixed: the condition is CONSTRUCTED** (make an artifact read
strong on mostly-inference → every inference in it must be load-bearing → **then ground it** → exactly the
clause-(c)-only items must leave, and **nothing may go red**). The guard is now **order-independent**.

**⚠️ A SECOND CONTROL WENT VACUOUS.** `theNumberIsHidden_bites` yanked `data-count-key` off the DOM — and the new
state-exercising guard **repaints the panel**, putting it straight back. **A control written against the DOM rots
exactly as a guard written against copy does.** It now regresses the **painter** (`_progressHTML`), which no repaint
can undo.

**NEGATIVE CONTROLS — all bite:** **`clauseC_isDeleted_bites`** (the mandated one — delete clause (c) → **RED**, Scope
drops out) · `clauseA_isDeleted_bites` · `clauseB_isDeleted_bites` · `theLooseReadingReturns_bites` (the over-count
comes back) · `ageingIsTyped_bites` · **`thePastIsBackDated_bites`** (the demo project is aged instead of the clock →
D100 dies quietly) · plus all 13 pre-existing DL-109 NCs and all 19 D180 NCs.
**MUST-NOT-FIRE — all green:** `mustNotFire_moreInferencesAndAHigherBand` · `mustNotFire_groundingRisesWhileIssuesRise`
· **`mustNotFire_groundingTheFlaggedArtifactRetiresClauseC`** (deep pass → 20; user grounds Scope → 12; flag gone;
**six guards stay green**) · `mustNotFire_theClockAdvances`.

## VERIFICATION

1. **`node --check`** → **PASS.**
2. **jsdom WITHOUT `runScripts`** → **body.children = 31**, 7 panes, `#pane-inference` + `#inf-rows` present.
3. **Boot assertions: 97/97 PASS × Free × Basic × notes-OFF × notes-ON · 0 console errors** (all four configs).
4. **Negative controls: D109 32/32 · D180 19/19 — every one bites; every must-not-fire control green.**
5. **AA both themes** — no new tokens. New copy uses `.inf-ch h3` (`--text`: **15.05** dark / **16.56** light) and
   `.inf-note` (`--subtle` on `--surface`: **5.34** dark / **5.23** light). All ≥ 4.5:1.
6. **Behavioural (real doors only):** boot **12** → Extended pass **20** (rise = correct, D177) → user grounds Scope
   via **Apply this fix** → **12**, clause (c) → **0**, flag gone, **zero guard failures, zero console errors**.
   `simNextWeek()` ×3 → **"Unvalidated for 3 weeks"** on screen, timeline **"3 weeks ago"**, velocity **0 · 0**.
   Week 0 → **`now − 2m`**, ages in minutes (**D100**).
7. **Vocabulary:** word-boundaried scan of every pane. **No debt/burndown framing of inference.** Controls confirm
   `lowest` ≠ *owes* and `reliability` ≠ *liability*.

## FOUND, NOT INVENTED — one pre-existing defect fixed

**A D163/D167 breach the boot guards could not see.** Act on the deep-pass Scope issue, then ask chat about it → the
opening turn was **55 words against a 50-word budget**. It never showed at boot **because no issue is `addressed` at
boot**. The overflow was *"You've acted on it — it's Addressed, waiting on an analysis update"* — **the first half
restates the second**, exactly the sentence D163 bans. **Copy fixed (budget untouched):** ***"Addressed — waiting on
an analysis update."*** **The honest label survives, once, short.** Verified pre-existing: with the **loose**
definition restored, the same guard fails identically.

## ESCALATED — NOT INVENTED

- **The packet's "strict → 4" does not reproduce.** On the live model, *supports an open issue on the limiting
  dimension* computes **8**, and *cites an open critical issue* computes **3**. **Neither is 4.** The number in the
  D181a packet appears to be an artefact of the earlier note, not of the model. **It changes nothing** — the
  three-clause definition is what was built, and every clause is computed — but the figure is **corrected on the
  record**, not quietly matched.
- **"Owed" appears once in the DEMO PLAN's own prose** — *"the report the sponsors are owed"* (a sponsor deliverable
  in the sample project). **It is not inference framed as a debt**, and DL-109 §3 governs how OSLO frames **its own
  epistemic state**. **Not edited** — *do not change correct product copy to satisfy a naive scanner* (D166 §3).
- **`_ciVelocity()` counts ITEMS; the Progress `inferred` row counts CLAIMS.** At week 0 the map reads *"I inferred
  **37**"* while Progress reads *"I inferred: **11**"*. Both are true and neither is typed, but **they are different
  populations wearing the same verb.** Pre-existing (DL-109 §2a is claim-level; §4b is item-level). **Flagged, not
  unilaterally reconciled** — the fix is a wording or a scope decision, and it is the owner's.

## Docs updated

`product-data.md` (the three clauses + the D181b clock) · `frontend-ui.md` · `user-experience.md` · `workflow.md` ·
`success-criteria.md` (**C-D181-1..8**) · `e2e-test-scenarios.md` (**T-D181-1..6**) · `edge-cases.md`
(**E-D181-1..11**) · `open-items.md` (**O-DL109-1 and O-DL109-3 CLOSED**).

---

# D182 (P1) + D183 (a–g) — 2026-07-13

## TASK 1 — D182: THE GUARDS WERE SELLING TO THE USER. **REPRODUCED, FIXED, GUARDED.**

**Reproduced first, then fixed.** With the product in the normal post-first-value state,
`_d170NegativeControls()` **raised 34 live upgrade prompts**, **spent the user's `promptLog` cadence budget**, and
**left an entry in the deferral queue** — which drains on a 400 ms timer, landing a prompt on the user's screen
**with no attempt behind it.** That is the owner's symptom verbatim: *"an upgrade prompt appears without any
user-derived event/trigger."*

**Root cause, confirmed:** NC-10 / NC-20 monkeypatch `window.sendMemo` and NC (D164) monkeypatches
`window._rptCommit` — **the readout's autosave path** — to call `fireUP('UP-REPORT')` in order to prove the guard
bites. `_assertSharingIsFreeOnEveryTier()` and `_assertSchedulingIsTheGateNotTheShare()` then call the **real**
send. The scaffolding reached into the live product and sold.

### The fix — ONE PROBE FENCE (`_PROBE`), applied BY CONSTRUCTION

`_CHAT_PROBE` generalised. `_fenceEveryProbe()` runs at boot, before any probe, and wraps **every `_assert*`
guard, every `_d*NegativeControls()` suite, `_upAffordanceTable()` and `_s10SelfCheck()` itself** (`toString` is
preserved, because a dozen guards read other functions' **source** — a wrapper that hid it would make them grade
the wrapper and pass for free). While the fence is up:

- **prompts** are **computed and recorded** (`_PROBE.prompts` — this is what makes the fence guard non-vacuous)
  but **blinded** (`html[data-probe]`) and **never persisted** — `_upFired()` and the month-cooldown are no-ops;
- **`_deferUP()` never enqueues**, and the two **asynchronous** fire paths (`_markFirstValue` → UP-8,
  `_maybeUP7` → UP-7) **do not arm** — a `setTimeout` escapes a synchronous fence entirely;
- **chat, History, Trend, the memo register, localStorage and the open prompt surfaces are restored byte-for-byte.**

**A prompt may fire ONLY from a real user attempt** (D138/D170) — and that is a **must-not-fire** control, because
a fence that gagged the product would have traded one P1 for a worse one.

## ⛔ THE GUARD-LEAK AUDIT — every guard × every NC suite

Runtime audit (not a source grep): wrap `_renderUP` / `_upRoute` / `pushChat` / `pushHistory` / `LS.set`, run
**107 guards and 9 NC suites** individually, and diff a fingerprint of localStorage · HISTORY · TREND ·
REPORT_SNAPSHOTS · the chat thread · the deferral queue · the open prompt surfaces · ISSUES · `_istatus` · TIER.

**BEFORE (the leak):**

| Probe | Reached the user | Residue |
|---|---|---|
| `_assertGatedAttemptSurfacesAPrompt` | **8 prompts + 1 upgrade modal** | 66 localStorage writes |
| `_assertSchedulingIsTheGateNotTheShare` | **1 prompt** | ⛔ **localStorage NOT restored** |
| `_assertSharingIsFreeOnEveryTier` | — | 2 History writes |
| `_assertScheduledSendIsAShare` | — | 2 History writes |
| `_assertDeepPassMovesBandAndCounts` | — | ⛔ **1 chat message left in the user's thread** (found by the new guard) |
| `_upAffordanceTable` | prompts | ⛔ **invents 5 localStorage keys** (`LS.set(k, LS.get(k,null))` writes the string `"null"`) |
| `_d170NegativeControls` | ⛔ **34 prompts + 4 upgrade modals** | ⛔ **localStorage NOT restored** + deferral queue armed |
| `_d164NegativeControls` | — | ⛔ localStorage NOT restored |
| `_d177 / _d179 / _d180 NC` | — | chat + History writes (restored) |

**AFTER (post-fence):**

| Probe | Prompts **computed** (fenced, recorded, never raised) | **Reached the user** | **Residue** |
|---|---|---|---|
| `_assertGatedAttemptSurfacesAPrompt` | 10 | **0** | **clean** |
| `_assertSchedulingIsTheGateNotTheShare` | 1 | **0** | **clean** |
| `_assertNoProbeCanRaiseAPrompt` | 62 | **0** | **clean** |
| `_assertProbeLeavesNoResidue` | 83 | **0** | **clean** |
| `_d170NegativeControls` | 62 | **0** | **clean** |
| *all other 103 guards · 7 other NC suites* | 0 | **0** | **clean** |
| `_d182NegativeControls` *(the one **named** exemption — it must stand outside the fence to prove it reddens, and to prove a real user attempt still prompts)* | 0 | *102, all deliberate injections + the user-attempt control* | **clean** |
| **TOTALS** | **218 computed under the fence** | ⛔ **0** | ⛔ **0 dirty** |

### THREE MORE GUARD DEFECTS, FOUND BY THE NEW GUARDS (18th, 19th, 20th)

1. **`_upAffordanceTable()` was inventing five localStorage keys in every user's browser.**
   `LS.set('promptLog', LS.get('promptLog', null))` does **not** undo a write — it stores the string `"null"`.
   → `_lsFullSnap()` / `_lsFullRestore()`: **raw, byte-for-byte. Absent means ABSENT.**
2. **`_assertDeepPassMovesBandAndCounts()` was leaving an OSLO message in the user's chat.**
   Its restore trimmed `scroll.children` back to a saved **count** — but `pushChat()` **replaces the first-run
   empty state**: one child out, one child in. **The count never moved, so the trim never fired**, and
   `_chatPersist()` wrote the message to the user's storage. → restored **byte-for-byte**, never by arithmetic.
3. ⛔⛔ **THE RETURNING USER — the sharpest of the three.** The boot guards looked clean **only because at boot
   `firstMRI` is false and `fireUP()` refuses at GUARD 1.** A **returning** user has first value, so the prompts
   actually **route**, and `_upFired()` wrote `promptLog` / `promptSeen` **on every boot**. The test suite was
   eating the user's nudge budget — **so the next prompt they actually earned would be swallowed by a cadence
   guard. That is D170's P1 arriving by a second road.** → `_upFired()` and the month-cooldown are no-ops under
   the fence, and **the boot matrix now includes first-value = YES.**

Plus two **guard-on-itself** defects, both self-matches: `_assertNoProbeCanRaiseAPrompt()` failed on **its own
regex literals**, and `_assertInferencesAreCalledInferences()` failed on **its own comment**. Both fixed —
*a scanner must not be its own subject*, and *the copy is not the commentary* (`_edCodeOf`).

## TASK 2 — D183 (a–g)

- **a. OSLO says "I" only in chat.** Panels swept (`_payoffNote`, Progress, the Inference map's velocity and
  false-confidence callout). **The PM keeps the first person in the readout — D152 requires it** — and the chat
  keeps it. **Both are must-not-fire controls:** a sweep that could not tell *who is speaking* would have broken a
  ratified decision to satisfy a copy rule.
- **b. Outcome Confidence adopted · the 0–100 index DELETED** from the hero, the pill, the popover, the chat and
  the reports — element, render path, snapshot **and CSS rules**. `_assertNoIndexDelta()` / `_idxDemotionOK()`
  retired with it. The guard's **non-vacuity clause requires the LABEL to be present**, so deleting the number and
  quietly losing the positioning is itself a red. Prototype-notes entry added (D161) recording the two conditions
  for its return.
- **c. Grounding vocabulary** — *barely / thinly / partly / largely / well grounded*, **computed from
  `CONTEXT_ITEMS`** through `_ciEvidenceId()` (the one door), sharing **no token** with `_BANDORD`, checked on
  word boundaries. The payoff's transition moved with it (*"Grounding: thinly → largely grounded."*).
- **d. "inferences", not "things".**
- **e. Documents** across every user-facing surface **including tooltips and aria-labels** (~45 strings). The
  canonical entity remains `Artifact`.
- **f. The trend line's cause text is deleted.** Sparkline + direction word. The cause keeps its **one home** in
  "What changed".
- **g. The Overview order is computed** from first-value and flips.

**The word budget nearly cost the user the ASK.** The grounding transition is longer than the reliability one and
blew the 20-word payoff budget, so `_payoffFit()` dropped the ask and **D178 went red — the guard caught it.**
Fixed by ordering the drops: **grounding drops before the ask**, because grounding is *also* readable in Progress
and **the ask is the one thing the user can act on next.**

## VERIFICATION

1. **`node --check` → PASS.**
2. **jsdom without `runScripts`** → body children **31**, panes **7**, 1 `<script>`, 2 `<style>` — unchanged.
3. **Boot assertions: 106, all pass, across 8 configurations** — Free × Basic × notes-OFF/ON × **first-value
   NO/YES** — **0 console errors** in every one.
4. **Negative controls: 9 suites, 204 controls, every one bites.** Includes *a probe fires a prompt → the fence
   guard goes **RED***. Every **must-not-fire** control green (a real user attempt still prompts · the PM still
   says "I" · the chat still says "I" · more inferences is still not a regression · more issues + a higher band is
   still correct).
5. **AA both themes** — `--text` 16.92 / 16.56 · `--muted` 9.86 / 8.03 · `--subtle` 6.01 / 5.23. **No new colour
   token**; the one new CSS rule (the probe blind) carries no colour and no z-index.
6. **Behavioural:** prompts reaching the user across the **entire** guard suite + 8 NC suites = **0**; deferral
   queue = **0**. Pill: *"Outcome Confidence · Moderate · largely grounded"*. Zero `/100` rendered. Progress:
   *"12 inferences are holding up your plan"*. Trend: *"↗ Strengthened"*. Order flips on first value. A real user
   attempt on Free → prompt shown, limit named, 2 resolutions.
7. **Slices 1–9 + the rest of Slice 10: no regression** (all pre-existing guards green in every configuration).

## ESCALATED, NOT INVENTED

**O-D183-1** (does "after activation" mean *first value delivered* or *the user's own work has landed*?) ·
**O-D183-2** (the grounding band cut-points are prototype-grade) · **O-D183-3** (the reliability **basis** rows
still use Low/Moderate/High — canon states no other scale for them) · **O-D183-4** (D049 is now split
user-facing/canonical and the log should say so) · **O-D182-1** (*a probe may never produce a user-facing effect*
belongs in `00_owner/build_governance/`, not in one prototype).

---

# D184 (P1) + D185 — the consent defect, and the panel that lectured (2026-07-13)

## 1. D184 — "Apply this fix" did not show the fix

**Owner:** *"Issues panel lists an 'Apply this fix' button, but it doesn't display the fix/recommendation it applies
to. How would the user know what fix is to be applied?"*

**They couldn't. And it was worse than it looked:** three recommendations, **collapsed**, in a disclosure row,
**below** the button. The button did not even identify which.

> ### ⛔ **A FIX THE USER CANNOT READ IS A FIX THEY CANNOT CONSENT TO.**
> **OSLO is advisory-only (D001). Advice the user cannot see is not advice — it is an instruction.**

### Built
| # | Rule | Mechanism |
|---|---|---|
| 1 | The recommendation is **resident, above the button, in the button's own block** | `.ip-rec` moved **out of `.ip-rows` entirely** — it is not a disclosure at any time, in any state |
| 2 | The button **names its subject** — *"Apply: Confirm the venue's 500-person Wi-Fi capacity…"* | the label is built from the **same object** the block renders (`_recSubject(_primaryRec(id).text)`) |
| 3 | **More than one recommendation** ⇒ the button applies the one on screen; the rest are **one tap away**, ranked | `_otherRecs(id)` → *Other paths (2)* |
| 4 | **Rank = the recommendation that moves the LIMITING dimension.** Computed, never an index | `_recRankScore()` (appliable · limiter · the user's selection · OSLO's rec) and `_leadRecId()` across issues |
| 5 | **No renderable recommendation ⇒ NO BUTTON** | `_primaryRec()` → `null` → the block is not built (**D173, applied to actions**) |
| 6 | **DL-103 §7d is now STRONGER** | the cap cannot hide a recommendation that was **never inside a collapsible row**. The cap opens the *Other paths* row, because that is where the **free manual door** lives |

The **chat's** apply affordance is bound by the same rule and graded on its **render path**.
`_ansRecommendation` now offers *"Apply: <the change> →"*, and the "what would you do?" route with no issue named
leads with **the ranked recommendation**, not the severity sort's first row.

## 2. D185 — the Confidence popover

**~90 words of prose defending the panel, ~10 words of information.** Three paragraphs, each justifying the row
above it. **Deleted — not shortened.** All three are now behind the ⓘ.

```
OUTCOME CONFIDENCE  ⓘ                         Stage  Orientation ▸ Expanded ▸ Validated ⓘ
● Moderate   thinly grounded
Clarity      ▮▮▮▮▯  High
Alignment    ▮▮▮▯▯  Moderate
Feasibility  ▮▮▯▯▯  Low            ← the limit (weight, never hue)
Feasibility — the lowest. Ground it to lift the read.
[            Ground Feasibility →            ]
RELIABILITY BASIS ⓘ                                                            All three ▾
Thinnest: Evidence — Low.
```

**Resident prose: 12 words** (budget 25). **Resident explanatory sentences: 0.** **ⓘ affordances carrying the
doctrine: 4.**

- **The limiter has a VERB** — *a limiter the user cannot act on is trivia.*
- **One way out**, computed: *"Ground Feasibility →"* opens the issue the limiter rests on (`_leadRecId()`); it
  falls back to the full breakdown when there is nothing to point at.
- **Reliability basis surfaces what is THIN**, ranked from state: *"Thinnest: Evidence — Low."* Two tied → both
  named. **All three level → *"Even across the basis — Moderate."* — a tie has no weakest and OSLO does not invent
  one (D173).** The three-row table is **on demand**.

## 3. The standing sweep — *a surface that explains why it is trustworthy is not*

**Fixed (unambiguous):**
1. ⛔ **The TOUR was still teaching the DELETED 0–100 index** — *"The 0–100 read is the focal point"* — **in the one
   surface written to explain the product.** The DOM guard could not see it: a tour step is a string in a registry
   until it is spotlit. **`_assertNoZeroToHundredIndexAnywhere()` now reads the TOUR copy registry too.**
   *A guard that only reads the DOM cannot see copy that is one click from the DOM.*
2. **The same self-justifying sentence had THREE homes** — the popover, the Overview "why" box, and the Project
   summary. It now lives in one place: the ⓘ.
3. **"Brighter = more attention — not a health score" was resident TWICE on the Attention map** (lead + legend).
   *Say the honest thing once* (D162a).

**Escalated, not touched:** the advisory footer (D001/D027 — ratified, and it may be the one line that must stay
resident) · the Project summary's closing caveat · the chat's *"not a grade"* (chat is a conversation) · the
Overview card's fuller false-confidence disclosure (a **disclosure** is not narration, and a word budget may not
delete one). See `open-items.md` → **O-SWEEP-1…4**.

## 4. Guards (4 new) and negative controls (2 new suites)

| Guard | Proves |
|---|---|
| `_assertApplyAffordanceShowsItsRecommendation()` | every live apply-affordance (panel **+ chat render path**) shows its recommendation, **above** the button (document order), **outside any disclosure row**, with a label that names it — **and no recommendation ⇒ no button** (state proof: blank the `rec`, the button must vanish) |
| `_assertRecommendationRankIsComputed()` | move the limiting dimension → the lead recommendation moves (**ISS-01 Feasibility → ISS-05 Alignment**). Never a fixed index into the issue set |
| `_assertConfPopIsAReadout()` | resident prose ≤ 25 words · **zero** resident explanatory sentences (graded **within each text node**, tagged or not) · zero narration frames · **the ⓘ still carries the doctrine** · the limiter has a verb |
| `_assertReliabilityBasisSurfacesTheWeakest()` | state proof: make one dimension weakest → it is **named**; make all three level → **no weakest is invented**; the three-row table is **not resident** |
| `_assertRecommendationNeverHidden()` **(strengthened)** | the recommendation may not live inside a `.ip-row` **at all** — not "the row is open" |

**`_d184NegativeControls()`** — 5 bite, 2 must-not-fire green:
the fix goes back into a closed drawer · the button forgets its subject · a button with no subject survives · the
button climbs above the change · the rank becomes `Object.keys(ISSUES)[0]`.
**Must not fire:** the assisted-apply cap still never hides the recommendation · manual editing is still free.

**`_d185NegativeControls()`** — 6 bite, 2 must-not-fire green:
a narration paragraph returns · a self-justifying frame returns · **a paragraph tagged `data-cpp-state` to dodge the
budget** · the limiter loses its verb · the basis stops ranking · a tie invents a weakest.
**Must not fire:** the doctrine is still one tap away (strip the tips → the guard must go RED) · the D052
false-confidence flag still fires.

### ⚠️ TWO GUARD DEFECTS, CAUGHT ON THE FIRST RUN OF THE GUARDS THEMSELVES (D166 §3 — fix the guard, never the doctrine)
1. **The sentence clause JOINED every resident text node** before splitting on punctuation — so the panel's labels
   ("Outcome Confidence", "Stage", "Clarity", "High"), which carry no full stops, **fused into one 20-word
   "sentence"**, and the guard **reddened on a readout doing exactly what it was told.** **A label is not a
   sentence.** Sentences are now graded **within each text node**.
2. **The rank guard scanned `_leadRecId`'s source for `[0]`** — and `_leadRecId` **ends in `.sort(…)[0]`**, which is
   the *correct* way to take the head of a **computed** ranking. **The guard called the fix a defect.** The subject
   is a **fixed index into the issue set** (`Object.keys(ISSUES)[0]`), which is the shape of the bug that shipped.
3. **A third, caught by the NC and not by review:** the D184 guard originally only asked *"is the recommendation in
   the same block?"* — and a `.ip-rec` **pushed back inside a disclosure row** still satisfied it. `theFixGoesBack
   IntoAClosedDrawer_bites` went RED. The guard now asserts the recommendation is **not inside a `.ip-row` at all**.

## 5. Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without `runScripts`** | **31 body children** — unchanged |
| 3 | **Boot guards, full matrix** — Free × Basic × notes OFF/ON × first-value NO/YES (**8 configs**) | **110 assertions, all true, 0 console errors** in every configuration |
| 4 | **Negative controls** | **11 suites · 219 controls · every one bites**; every must-not-fire control green |
| 5 | **D182 regression** — prompts raised by the guard suite | **`_promptReachesTheUser(): false` · `d182FenceLifted: true` · deferral queue empty** |
| 6 | **AA, both themes** (on `--surface-2`) | `--subtle` **4.67 / 4.75** · `--primary-light` **6.30 / 5.39** · `--text` **13.15 / 15.05**. **No new colour token introduced.** |
| 7a | The recommendation is visible above its button, ranked by limiter | lead = **ISS-01** (Feasibility = the limit, critical); rec text on screen; button **after** it in document order; *Other paths (2)*; **printed once** |
| 7b | No recommendation ⇒ no button | blank the `rec` → **0** apply affordances in the panel |
| 7c | Popover | **12 resident prose words · 0 explanatory sentences · 4 ⓘ tips carry the doctrine** |
| 7d | Reliability basis | *"Thinnest: Evidence — Low."* / *"Thinnest: Coverage · Evidence — Low."* / *"Even across the basis — Moderate."* — three-row table **on demand** |
| 7e | Slices 1–9 + the rest of Slice 10 | **no regression** — every prior guard and NC suite green |

---

# D186 · D187 · D188 · D189 — the Overview/Progress surfaces (owner, 2026-07-13)

**Target:** `vertical-slices/slice-10-tiering-limits/prototype.html` (amended in place).

## D186 — "Holding it up" is dead

The phrase was doing **two opposite jobs on one page**: *"Feasibility is holding it **back**"* (obstructing) and
*"20 inferences are holding it **up**"* (**supporting** — D181 load-bearing). **The owner read the support as a
delay.** *"Hold up" is ambiguous in English, and it sat on the single most valuable number in the product.*

- Label → **`YOUR READ RESTS ON`** · copy → ***"N inferences your read rests on"*** (D183d: *inferences*, never
  *things*).
- The CAF limiter **stays a limiter** — **"Blocker" appears nowhere.** It would tell the user to *remove the thing
  carrying their plan*, and on the limiter it reads as *"the PROJECT is blocked"* — the health framing **D003
  forbids**. Shipped form (D185.4): **"Feasibility — the lowest. Ground it to lift the read."** **ESCALATED
  (O-D186-1): the owner may override; it was not done silently.**
- **11 user-facing sites swept** + the count registry's prose `word` + the guard messages + the notes/comments.
- **Guard `_assertNoHoldingItAnywhere()`** grades the **DOM · attributes · the TOUR registry · `PN_SLOTS` · the
  render paths** (comments stripped — **a scanner must not be its own subject**), proves the **replacement is on
  screen** (deleting the phrase must not delete the number), and proves **"Blocker" never arrived**.

## D187 — the valence table

**Green — only — on counts nothing but the user's own work can move.** Declared, computed, and each row **states
why**:

| user-driven ⇒ **GREEN on a rise** | OSLO can move it ⇒ **NEUTRAL, both directions** |
|---|---|
| `resolved` · `answered` · `vel_you` (*you grounded*) | `issues` · `critical` · `questions` · `inferred` · `loadbearing` · **`grounded`** · `vel_oslo` |

**No red. Anywhere.** There is no token, no CSS rule, and **no `red` field in the table to set** — the guard fails
if one appears.

**⚠️ The one that surprised us — reported, not invented:** the Progress **`grounded`** row (*"Claims on your
evidence"*) is **NOT** user-driven. A deeper read can extract a **new** claim from a document the user had
**already** confirmed (`_ciEvidenceId()` reads the artifact attestation, so `CI-69` on Resources is born grounded).
**OSLO can move it without the user ⇒ the mechanical test says NEUTRAL.** The green D187 names — *"you grounded"* —
is the week's **grounding velocity** (`_ciVelocity().you`, gated on `_ATTEST_AT`), which genuinely cannot move
without the user. **Escalated as O-D187-1.**

**The token is not the severity token.** `--earned` #4FC3A1 / #0A6E52 vs `--success` #4D8B6B / #3E7357 — **chroma
distance 77.8 / 52.5**, AA in both themes. **The guard grades the VALUE, not the name** (that defect has bitten
before) and reads the **last** `:root` declaration, because that is what the cascade does.

**Measured:** user resolves an issue → **only `resolved ↑1` is green**. OSLO runs a deeper read → `issues ↑2 ·
critical ↑1 · questions ↑1 · inferences ↑` and **zero greens, zero reds**. **D180 intact:** the arrow's direction is
still `delta > 0 ? '↑' : '↓'`.

## D188 — labels, not sentences

**4 · Unconfirmed dependencies ⓘ** · **5 · Unowned parties ⓘ** · **3 · Untraceable numbers ⓘ** (≤ 3 words each; the
vivid sentence is **behind the ⓘ**, not resident). **The velocity strip got the same treatment** and now carries its
own ⓘ. **Those are the only two stat strips on the surface** — the Progress chips (*Issues · Critical · Open
questions · Issues resolved · Questions answered*) were already ≤ 3 words.

## D189 — the caption sweep, and two guard defects

- ***"A direction, not a target"* — DELETED.** DL-107 for the third time. The rule it narrated is enforced **in the
  code**; the explanation is **behind the ⓘ**.
- ***"I inferred"* / *"20 things I inferred"*** were **already** correct on Progress (`OSLO inferred` /
  `N inferences`) — **the re-sweep found no first person left on any non-chat surface.** What it *did* find:

### ⚠️⚠️⚠️ GUARD DEFECT #24 — the first-person guard was BLIND to the Issue panel
`_OSLO_VOICE_SURFACES` carried **`#issuePanel`** and **`#ipBody`**. The real id is **`issuepanel`**; **`ipBody` does
not exist.** *CSS id selectors are case-sensitive* — **both matched ZERO elements**, so **the most-opened surface in
the product had never been graded for first person by any guard. The guard passed because it never looked.**
**Fixed:** selectors corrected; four more non-chat panes added; **the guard now FAILS if any surface in its list
resolves to nothing** (*a selector that matches nothing is not a passing test — it is a blind one*); it **opens
every issue under the probe fence** and grades the panel OSLO actually paints; and the **user's own controls**
(*"✎ Write **my** own fix"*) are exempt **by declaration** (`data-voice="user"`), never by regex. **A copy rule that
cannot tell who is speaking is not a copy rule.**

### ⚠️⚠️ GUARD DEFECT #25 — the documents guard only graded what had been PAINTED
`#limitsBody` is empty until `renderLimits()` runs, so a live **D183e** violation — *"**Plan artifacts** · History"*
and *"**Artifacts** · History · asking for a read…"* in the **What's metered** modal — **sat there for the whole
build**, surfacing only under a notes repaint. **An unpainted surface is not a clean surface.** Copy fixed
(**"Documents"**); **the guard now paints the deferred surfaces before grading them.**

### The caption sweep — what it did NOT touch
**A DISCLOSURE IS NOT NARRATION, AND A WORD BUDGET MAY NOT DELETE ONE.** The sweep's subject is the **caption slot**
(`.inf-note`) and nothing else. **O-SWEEP-1…4 remain ESCALATED, not swept** (the advisory footer, the
project-summary caveat, chat's *"not a grade"*, the Overview false-confidence disclosure), and a **must-not-fire
control now proves the sweep did not reach them.**

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without `runScripts`** | body children **31**, unchanged |
| 3 | **113 boot guards × full config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | **113/113 PASS, 0 console errors, every configuration** |
| 4 | Negative controls | **12 suites, 245 controls, every one bites**; all must-not-fire green |
| 5 | **D182 probe fence** | `d182FenceLifted: true` · `_PROBE.depth: 0` · `_promptReachesTheUser(): false` · `_upDeferred: 0` — **zero prompts raised by the guard suite** |
| 6 | **AA, both themes, incl. the new green** | `--earned` **7.61:1** dark / **6.24:1** light; **distance from `--success` 77.8 / 52.5** — *not the severity token wearing a different name* |
| 7a | *"holding it"* nowhere, **tour included** | **true** (DOM · attrs · `TOUR` · `PN_SLOTS` · render paths) |
| 7b | Green only on user-driven, no red, direction data-driven | **true** (state proofs both ways) |
| 7c | Stat labels ≤ 3 words, consequence behind the ⓘ | **true** (5 cells, all 2 words, all with ⓘ) |
| 7d | No first person outside chat | **true** — and the guard can finally **see** the Issue panel |
| 7e | Slices 1–9 + rest of Slice 10 | **no regression** (all pre-existing guards + NC suites green) |

**Guard count 109 → 113. NC suites 11 → 12 (219 → 245 controls).**

## Escalations (owner call — nothing invented)
1. **O-D186-1** — the CAF limiter is **not** called a "Blocker". Reasoned, shipped as a limiter, **escalated**.
2. **O-D186-2** — the load-bearing row **stutters by direction** (`YOUR READ RESTS ON` · *"9 inferences your read
   rests on"*). Both strings are individually directed and the same redundancy existed in the build it replaces, so
   the structure was **not** changed unilaterally. **One word from the owner collapses it to `YOUR READ RESTS ON ·
   9 inferences`.**
3. **O-D187-1** — Progress `grounded` is **neutral**, not green, because **OSLO can move it**. The green went to
   the count that genuinely passes the test (*you grounded*, on the Inference map).

---

# D190 — The recommendation block, corrected (owner, 2026-07-13)

**Three corrections, amended in place in `vertical-slices/slice-10-tiering-limits/prototype.html`.**

## D190a — the button says "Apply this fix." Nothing more.

`APPLY_LABEL = 'Apply this fix'`, read by **one function** (`_applyLabel()`) that **both** the panel and the chat
call — so the affordance cannot drift apart across surfaces. `_recSubject()` is **deleted**: the label-building
machinery is gone, not merely unused.

### The guard: I amended the LABEL clause, and nothing else
The owner's warning was exact — **D184's guard never required the label to carry the text**, and re-reading it
confirmed that: clause (2) grades *the recommendation is visible in the same block*, the drawer clause grades *it is
not inside an `.ip-row`*, and the document-order clause grades *it precedes the button*. **All three are untouched.**
Only clause (3) moved: it used to fail on `/^apply this fix/i`; it now asserts the label **IS** the constant — so it
bites **the other way**, on a label that eats the fix.

**And it got a mechanism it did not have:** clause **(3b)** proves *constant* by **perturbing the subject** — it
opens **every** issue with a renderable recommendation and requires **one** label across **six different fixes**. A
single-panel read cannot tell "a constant" from "a label that happens to match on this issue."

**The consent clause still bites — proven, not asserted:** NC `aButtonWithNoSubjectSurvives_bites` blanks
`#ipRecText` and the guard goes **RED**. So do `theFixGoesBackIntoAClosedDrawer_bites` and
`theButtonClimbsAboveTheChange_bites`.

## D190b — "Other paths" → "Other options"

**Zero occurrences of "path" in this sense** in rendered copy — DOM text, `title` / `data-tip` / `aria-label`
attributes, the chat render paths, the review kinds, **History**, and the **tour**:

- *Other options (2)* · *Select* / *✓ Selected option* · **Selected option** chip
- History: **"Resolution option selected — …"** · *Option "…"*
- Chat: *"compare the **resolution options** on an issue"* · *"You've already selected an option here"*
- Reviews: *"You'd take a different option"* · *"proposed a different option"*
- Tour: *"You commit to an option."*
- The demo issue's own prose: *"no recovery path is noted"* → **"no fallback is noted"**

**Internals keep their names** (`paths[]`, `_selpath`, `selectPath`, the `selected_path` History type) — the D183e
split: the canonical entity keeps its name; the product speaks plain English.

## D190c — the options live UNDER the recommendation

**The disclosure row under Evidence is DELETED.** The options expand **in place**, in `#ipAlts` **inside
`#ipRecBlock`**, directly beneath the recommendation. The panel's rows are now **Evidence · Clarification ·
Comments · Reviews**. Everything the row carried moved with it: the **ⓘ**, **Select**, **Discuss**, the **Selected
option** chip, and the **free manual door** — *"✎ Write my own fix in \<document\>"* (D183e).

**The cap's reach moved with the door.** `_ipRows()` still forces the key `rec` open while `_capHit('fixes')`, and
that key now opens `#ipAlts` — where the free door lives. **The user cannot collapse it at the cap.** The
recommendation is **outside** the container entirely, so the cap cannot hide it **by construction**.
**`.ip-alts` is deliberately not an `.ip-row`** — the D184 drawer clause forbids it, and this container must never
become one.

### The new guard: `_assertOptionsHaveOneHome()` — mechanism, not a string scan
Over **every** issue that carries alternatives, on the live DOM:
1. **ONE CONTAINER** — each option renders in exactly **one LEAF site** (`_leafRenderSites()` walks for the deepest
   element carrying the text). **Render the set twice and it bites, whatever the second copy is called.**
2. **ONE OPENER** — exactly one element declares `aria-controls="ipAlts"`, **and no undeclared handler in the panel
   can open the set** (`ipToggleAlts` / an `ipOpenRow`/`ipToggleRow` on the same state key).
3. **AND IT LIVES UNDER THE RECOMMENDATION** — inside `#ipRecBlock`, **after** the recommendation text in document
   order, and **not** inside `.ip-rows` / `.ip-row`.

**Non-vacuity (D166 §1):** if no issue carries alternatives, the guard **FAILS** — it does not pass for free.

## ⚠️ AA — a PRE-EXISTING defect this move surfaced (and did not ship)

The options moved from the panel background (`--surface`) onto the recommendation card (`--surface-2`). Two labels
were **already below AA in dark theme**: the **"Confirmed by you"** pill (**3.74:1**) and the **✓ Selected option**
tick (**3.72:1**) — because **`--success` is a fill/border green being used as TEXT**, and it fails **wherever those
labels appear** (artifacts and the memo included, not only this panel). The move made a failing contrast **worse**
(3.25 / 3.27), so it was **fixed, not shipped**:

**`--success-fg`** — dark **#6FB894** (AA on every surface it lands on: 7.07 `--surface` · 6.18 `--surface-2` · 5.45
`--surface-3` · 5.61 on the green tint), light **#3E7357** (**unchanged** — light already passed).
**`--success` itself is UNTOUCHED**, so D187's `--earned` chroma-distance guard grades exactly the values it always
did, and no severity/valence semantics moved. Distance from `--earned` #4FC3A1 = **36.2** — this is not the earned
green wearing a new name.

**It is a global token, so it is on the record as O-D190-1, not buried in the diff.**

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without `runScripts`** | body children **31**, unchanged |
| 3 | **114 boot guards × the full config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES, 6 configs) | **114/114 PASS, 0 console errors, every configuration** |
| 4 | Negative controls | **12 suites, 251 controls, every one bites**; all must-not-fire green |
| 5 | **D182 probe fence** | `_PROBE.depth: 0` · prompts captured **0** · `_upDeferred: 0` · `_promptReachesTheUser(): false` · `html[data-probe]` cleared · residue guard green — **zero prompts from the harness** |
| 6 | **AA, both themes** | new `--success-fg` **5.61 / 5.58** dark · **4.63 / 4.66** light (was **3.74 / 3.72 — below AA**); every other foreground on the moved block passes (`--muted` 7.67/7.29 · `--subtle` 4.67/4.75 · `--primary-light` 6.30/5.39) |
| 7a | Button label **short and constant**, **and the D184 consent guard still bites** | **true** — one label (`"Apply this fix"`) across **6** issues; chat `"Apply this fix →"`; **blank the recommendation → RED** |
| 7b | Zero occurrences of *"path(s)"* in this sense | **true** (DOM text · attributes · chat render paths · review kinds · History · tour) |
| 7c | The options open in **exactly ONE place**, beneath the recommendation | **true** — **1** opener · **1** leaf render per option · `#ipAlts` inside `#ipRecBlock`, after the recommendation, **not** in `.ip-rows` |
| 7d | The assisted-apply cap **still never hides the recommendation**; the free manual door survives | **true** — at a simulated cap: recommendation visible & out of every drawer · options **forced open** and **uncollapsible** · *"✎ Write my own fix in Resources →"* on screen |
| 7e | Slices 1–9 + the rest of Slice 10 | **no regression** (all pre-existing guards + NC suites green) |

**Guard count 113 → 114. NC controls 245 → 251 (12 suites, unchanged).**
**New guard:** `_assertOptionsHaveOneHome()`. **New NCs:** `theLabelEatsTheFix_bites` ·
`theLabelVariesWithTheSubject_bites` · `theAffordanceHasNoName_bites` · `aSecondOpenerForTheSameSet_bites` ·
`theOptionsAreRenderedTwice_bites` · `theOptionsGoBackUnderEvidence_bites` · must-not-fire
`mustNotFire_atTheCapTheFixIsVisibleAndTheFreeDoorIsOpen`.
**Retired NC:** `theButtonForgetsItsSubject_bites` — **it enforced the D184.2 clause the owner has now corrected.**
The doctrine moved; the control moved with it, and it now bites the other way.

## Escalations (owner call — nothing invented)
1. **O-D190-1 — a GLOBAL colour token changed.** `--success-fg`, above. It fixes a real dark-theme AA failure that
   exists **outside** this panel too. **If the owner would rather the dark green stay as it was, say so** — the pill
   and the tick are the only things that read `--success` as text.
2. **O-D190-2 — "ONE HOME" now has a mechanism; it should probably be a standing sweep.** The product has shipped
   the same defect **three times** in three registers — **counts** (D179e), **causes** (D183f), **actions** (D190c).
   `_assertOptionsHaveOneHome()` could be generalised into a `oneHome(set)` primitive pointed at all three.
   **Not built unilaterally — that is a new guard class, not a fix.**
3. **O-D184-1 stands** (unchanged by D190): *apply* is assisted, *select an option* is not — so selecting an option
   and then clicking Apply still drafts **OSLO's** recommendation. Two honest options, both owner-owed.

---

# D191 — P1: a decision, once made, could not be unmade — and it attested the user's document in their name

**Target:** `vertical-slices/slice-10-tiering-limits/prototype.html` (amended in place).
**Guards 114 → 120. NC suites 12 → 13; controls 251 → 272. All green. No regressions.**

## The four objects, and where each one lives in the code

| Object | Undoable? | Mechanism |
|---|---|---|
| **The SELECTION** | **YES — freely, to NO selection** | `clearSelection()` — no consent step, **no meter, no analysis run**. Nothing in the plan changed. |
| **The EDIT + the ATTESTATION** | **YES — and ALWAYS TOGETHER** | **`_withdrawUnit()` is the only function in the product that may drop an attestation, and it cannot return without having restored the document.** Uses the **existing** `_artVersion` / `_artKey` body / `_pushUndo` machinery — **no new snapshot mechanism invented.** |
| **The READ** | **NO** | `_withdrawCore()` (hand-path) **holds no read and cannot write one** — `_decision` carries **no band, no width, no Confidence**. `_rereadAfterWithdrawal()` runs **inside the analysis update** and **re-derives from state**; it never reads the withdrawal record. **Last-good (D098g) in the interval.** |
| **HISTORY** | **NO — APPEND-ONLY** | The withdrawal is a **new event**; the origin is **never touched**. `pushHistory` gained `opts.iss` — a **pointer**, so the row can carry the affordance without the record ever being rewritten. |

## The transition table (D191 §7a) — enumerated, not remembered

| Forward | Into | Attests? | Inverse |
|---|---|---|---|
| `selectPath` | `addressed` | no | **`clearSelection`** |
| `applyFix` | `addressed` + `attested` | **yes** | **`withdrawDecision`** |
| `_submitClarification` | `addressed` + `attested` | **yes** | **`withdrawDecision`** |

**The sweep scans every function in the product for writers of `_istatus[…]='addressed'` and `.basis='attested'`.
Any writer not in this table, with a declared and existing inverse, FAILS THE BUILD.** *(It is this sweep that found
`_submitClarification` — see O-D191-1.)* Probe helpers are **named** (`_ATTEST_PROBE_HELPERS`), never inferred.

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without `runScripts`** | body children **31**, unchanged |
| 3 | **120 boot guards × the full config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | **120/120 PASS · 0 console errors · every configuration** |
| 4 | Negative controls | **13 suites, 272 controls, every one bites**; all must-not-fire green |
| 5 | **D182 probe fence** | `_PROBE.depth: 0` · **164 prompts computed, 0 shown** · `_upDeferred: 0` · `_promptReachesTheUser(): false` · `html[data-probe]` cleared · **residue guard green — and it now grades the six new state-staging guards explicitly** |
| 6 | **AA, both themes** | `.ip-wd .wd-line` **7.92/7.39** · `.ip-wd-absent` **4.80/4.73** · `.hwd` **7.20/5.93** · `.meter .mref` **4.67/4.75** |
| 7 | **Behavioural, end to end** | see below |

**7 — apply a fix → withdraw it (ISS-01, document `Resources`):**

| | status | version | basis | reliability | fixes meter | History rows | read |
|---|---|---|---|---|---|---|---|
| **before** | open | **v2** | derived | **Low** | 0 | 1 | `Moderate/Very Low/30/58` |
| **applied** | addressed→resolved | **v3** | **attested** | **Moderate** | **1** | 4 | `Moderate/Low/38/62` |
| **withdrawn** | **open** | **v2** ✓ | **derived** ✓ | **Low** ✓ | **0** ✓ *(+1 recorded refund)* | **7** ✓ | `Moderate/Very Low/30/58` |

- **The read did NOT roll back — it RE-RAN.** Immediately after the hand-path the read is **byte-identical**
  (last-good, D098g). The **analysis update** then moves it, appending **1 new run event** and **1 new trend point**.
- **History has MORE rows, not fewer** (1 → 4 → **7**). The withdrawal is its own event; the origin event
  *"Applied OSLO's fix — Venue Wi-Fi capacity is unconfirmed"* survives **byte-identical**.
- **Consent came first:** *"This removes the change from Resources and withdraws your confirmation. OSLO will
  re-read the plan."* — and **the state was untouched at the consent step**.
- **Zero occurrences of "undo"** in the panel.
- **Select an option → clear it:** back to **Open**, **no selection**, History grew, **no analysis ran, no meter moved**.
- **A RESOLVED issue offers no withdraw** — and the absence is **stated**, not hidden.

**Guard defects found and fixed during this build (D166 — fix the guard, never the doctrine):**
1. `_applyProgressProbe` (a pre-existing probe helper) attests — it was tripping the new sweep. **Named**, not exempted by pattern.
2. The new guards leaned on the **outer** D182 fence to restore History/LS. **The fence is re-entrant** — when
   `_assertProbeLeavesNoResidue()` calls them, it takes **no second snapshot**, so they were dirty *inside* the
   residue measurement. **The residue guard caught it.** `_withDecisionState()` now restores its **own** bytes.
3. `.hwd:hover` → `--primary` = **3.09:1 in light theme**. **A hover state below AA is still a state the user reads.**
   **Fixed, not shipped.**

## Escalations (owner call — nothing invented)

1. **⛔⛔⛔ O-D191-4 — THE BIG ONE. AS BUILT, THE ATTESTATION BECOMES UN-WITHDRAWABLE AGAIN ~1.9s AFTER THE FIX IS
   APPLIED.** The instruction was explicit twice (*"a RESOLVED issue is NOT withdrawable by hand"* · *"withdraw is
   absent on a RESOLVED issue"*), and that is what is built. **But the analysis update resolves the issue ~1.9
   seconds after an apply** — measured — **and the document is still `attested`, with Reliability still raised, and
   there is now no way out of it.** **In the ordinary happy path the withdraw affordance lives for about two
   seconds, and the P1 D191 was written to kill re-enters through §5.** *The attestation lives on the DOCUMENT, not
   on the issue.* **D191's own sentence points at the other reading — *"Withdraw the FIX; the read follows"*: bar the
   user from hand-moving the ISSUE, not from withdrawing the FIX; the analysis update re-opens it, because the gap is
   genuinely back.** **The mechanism for that is one line** (`_wdAvailable()` drops its resolved clause — nothing else
   changes, because `_withdrawCore` already refuses to write the issue status and `_withdrawRun` already triggers the
   update). **NOT CHANGED UNILATERALLY. OWNER CALL.**
2. **⬜ O-D191-1 — answering a clarification ATTESTS too**, on the same two lines as `applyFix`. D191's prose names
   the fix and the selection; **guard clause §7a is absolute**, and it pulled the clarification into scope. Given the
   same record and the same inverse (*"Withdraw this answer"*). **No new doctrine — D191's own clause, applied to the
   transition it names.** The owner may want different copy, different behaviour, or it out of scope.
3. **⬜ O-D191-2 — edits made AFTER an applied fix.** Withdrawing rolls the document back past them. **Nothing is
   silent** (the consent line names it; `_pushUndo` snapshots first), but **what *should* happen is a product question
   D191 does not settle.**
4. **⬜ O-D191-3 — two decisions attesting one document.** `_attestBy[art]` records whose word attests each document;
   withdrawing drops **only that decision's** attestation, and History says so. **A rule the build had to choose —
   stated, not assumed.**
5. **⬜ O-D191-5 — the `Open → Addressed → Resolved` chevron still draws a ratchet** that no longer exists.

---

# D192 / D193 — the erratum, and the two questions D191 exposed (owner, 2026-07-13)

> ## ⛔ **WITHDRAWING A FIX IS NOT HAND-MOVING THE READ.** It is the user **editing their own document and retracting their own word.** The read then moves **BY ANALYSIS** — which re-opens the issue, **because the gap is genuinely back.**
> ## ⛔ **OSLO MAY NEVER DELETE THE USER'S OWN WRITING.**

**The owner ruled on all five escalations. All five are landed.** Target: `vertical-slices/slice-10-tiering-limits/prototype.html`.

## What changed

| Ruling | Built |
|---|---|
| **D192a** — withdraw is available on a **RESOLVED** issue *(the escalation was right: §5 reinstated the P1 — the analysis update resolves the issue **~1.9s** after the apply, so the affordance lived for two seconds)* | `_wdAvailable()` = *"is there a decision?"*, nothing more. ⛔ **The standing prohibition is unchanged and is PROVEN:** `_withdrawCore()` **does not touch a `resolved` status** — an analysis update put it there (D088) — and `_analysisUpdateAfterWithdrawal()` **re-opens the issue by analysis**, with its own lifecycle event. The panel states the standing word (`.ip-wd-still`) instead of stating an absence. |
| **D192b** — the chevron lies | `⇄` separators · **no trailing fill** (only the state the issue is in is lit) · the ⓘ states reversibility · `data-life` + `aria-current` on the chips. |
| **D192c** — clarification answers get the same inverse | Already built; the escalation flag is now a ratification note. |
| **D193a** — ⛔ **the restore is CONDITIONAL** | `_docTouchedSince()` — **real detection: content + version identity** against the document exactly as OSLO left it (`bodyAfter`/`verAfter`, captured in `applyFix`). **Untouched ⇒ restore. Edited since ⇒ DO NOT RESTORE**, withdraw the attestation alone, and **say so plainly** — in the consent line **and** on the record. The attestation drops in **both** cases; an analysis update runs in **both** cases. `confirmWithdraw()` **commits a pending keystroke first**, so a mid-typing burst is never eaten by the restore. |
| **D193b** — attestation is **refcounted** | `_attestBy[art]` (the list) + `_ATTEST_BASE[art]` (**captured at the 0 → 1 edge**, before the document is marked — which is why `_attestWith()` now runs *before* the `basis='attested'` line in both `applyFix` and `_submitClarification`). It stands while **any** decision attests it; drops on the **last**; **Reliability restores to its pre-*first*-attestation value.** |

## ⚠️ THE GUARD THE OWNER ORDERED WAS THE DEFECT — AND MEASURING IS WHAT CAUGHT IT

`_assertWithdrawIsAbsentOnAResolvedIssue()` (D191 §5(e)) **passed**. It was proving the wrong thing: it asserted the
absence of the affordance in the exact state where the attestation becomes permanent. **A guard that encodes a
doctrinal error will hold the defect in place and fail the build for fixing it.** It is **deleted** and replaced by
the positive proof:

**`_assertWithdrawSurvivesResolution()`** — apply → drive the **real** analysis update to `resolved` → the withdraw
is **still there** (panel · History row · `_wdAvailable`) → drive it → **the document is restored, the attestation
drops, and ⛔ the RESOLVED STATUS IS NOT TOUCHED BY THE HAND-PATH** → run the analysis update → **the issue is OPEN,
by analysis.**

## Guards (D166) — 119 → 123 boot guards, 4 new, 1 deleted

| Guard | Proves |
|---|---|
| `_assertWithdrawSurvivesResolution()` | **D192a** — the affordance survives resolution · **the hand-path never moves a resolved status** · the analysis update re-opens the issue. *(Replaces the §5 guard.)* |
| `_assertWithdrawalNeverDeletesTheUsersWriting()` | **D193a** — the user's sentence **survives** a withdrawal, byte for byte; the document is **not reduced**; the attestation drops **anyway**; OSLO **says so**. ⛔ It also proves an **untouched** document **is** still restored — otherwise it would pass by the restore being dead everywhere. |
| `_assertAttestationIsRefcountedByDecision()` | **D193b** — **it CONSTRUCTS the two-decision document** (`_d193PairSubjects()`, computed from `ISSUES`, never hardcoded): withdraw one ⇒ **still attested**; withdraw both ⇒ **drops**, to the **pre-first** Reliability. **A vacuous pass here is a FAILURE, and it declares itself.** |
| `_assertLifecycleIsNotDrawnAsARatchet()` | **D192b** — glyphs · fill · **and the MECHANISM: the issue is driven Resolved → withdrawn → re-opened, and the rendered track must FOLLOW.** |

**Negative controls: `_d191NegativeControls()` 17 → 30** (13 suites, **272 → 281 controls, every one bites**). New:
`theWithdrawDiesOnResolution_bites` *(**D191 §5, put back** — the P1 itself)* · `theHandPathReopensTheIssueItself_bites` ·
`theAnalysisUpdateNeverReopens_bites` · `theRestoreDestroysTheUsersEdits_bites` · `theNonRestoreIsNotStated_bites` ·
`theAttestationSurvivesAnEditedDocument_bites` · `withdrawingOneOfTwoDropsTheAttestation_bites` ·
`theReliabilityRestoresOneStepBack_bites` · `theLifecycleDrawsAOneWayArrow_bites` · `theLifecycleFillsInThePast_bites`.
**Must-not-fire (6, all green):** the read still moves on an analysis update · an analysis update still **resolves**
(and the decision behind it stays **withdrawable**) · **an untouched document is still restored** · the recommendation
is still never hidden · the record is still never metered · a selection still costs nothing.

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | **PASS** |
| 2 | jsdom **without `runScripts`** | body children **31**, unchanged |
| 3 | **123 boot guards × the full config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | **123/123 PASS · 0 console errors · every one of the 6 configurations** |
| 4 | Negative controls | **13 suites · 281 controls · every one bites**; all 6 must-not-fire green |
| 5 | **D182 probe fence** | `_PROBE.depth: 0` · **164 prompts computed, 0 shown** · `_upDeferred: 0` · `_promptReachesTheUser(): false` · residue guard green — **and it grades the four new state-staging guards explicitly** |
| 6 | **AA, both themes** | `.ip-wd .wd-line` **7.92 / 7.39** · `.ip-wd-still` **7.88 / 7.27** · `.hwd` **7.20 / 5.93** · `.meter .mref` **4.67 / 4.75** |
| 7 | Behavioural, **end-to-end and TIMED** | below |

**(a) apply → wait PAST resolution → withdraw** *(ISS-01 · document `Resources`)*

| | status | ver | basis | rel | fixes | History | read |
|---|---|---|---|---|---|---|---|
| before | open | v2 | derived | Low | 0 | 1 | `Moderate/Very Low/30` |
| applied *(+2.5s)* | **resolved** | v3 | **attested** | **Moderate** | 1 | 4 | `Moderate/Low/38` |
| **withdraw offered?** | — | — | — | — | — | — | ⛔ **YES** — panel *"Withdraw this fix"* · History row · the standing word stated |
| the instant after the hand-path | ⛔ **still resolved** | **v2** ✓ | **derived** ✓ | **Low** ✓ | **0** ✓ *(+1 refund recorded)* | 6 | ⛔ **unchanged** *(last-good, D098g)* |
| after the analysis update *(+2.5s)* | ⛔ **OPEN — by analysis** | v2 | derived | Low | 0 | **8** | `Moderate/Very Low/30` *(re-ran: 1 new run event · 1 new trend point)* |

**The user did not move the read.** The status stayed `resolved` through the entire hand-path; the **analysis update**
re-opened it and filed *"Venue Wi-Fi capacity is unconfirmed — **Open again**"*.

**(b) apply → the user WRITES in the document → withdraw**

- user's edit lands through the **real editor commit path** (v3 → **v4**, +1 sentence, stored body 12,299 bytes)
- `_docTouchedSince()` ⇒ **true** *(content + version identity — not a flag)*
- consent line: *"This withdraws your confirmation. **Your edits since are kept** — OSLO's change is still in Resources, and **you can remove it yourself if you want it gone.** OSLO will re-read the plan."*
- ⛔⛔⛔ **THE USER'S EDIT SURVIVES** — their sentence is still in the stored document, and it did **not shrink** (12,299 → **12,299**)
- **no restore** (still **v4**) · **the attestation dropped anyway** (`attested` → `derived`, `Moderate` → `Low`) · **an analysis update ran** · **History grew** (5 → 7)

**(c) two decisions, one document** *(`Resources`: ISS-01 + ISS-03 — the state is CONSTRUCTED, not hoped for)*

| | basis | reliability | standing decisions |
|---|---|---|---|
| before | derived | **Low** | `[]` |
| +decision 1 | attested | Moderate | `[fix:ISS-01]` |
| +decision 2 | attested | **High** | `[fix:ISS-01, fix:ISS-03]` |
| **withdraw ONE** | ⛔ **still attested** | High | `[fix:ISS-03]` — *History: "though Resources stays Confirmed by you, because another decision of yours still attests it."* |
| **withdraw the LAST** | ⛔ **derived** | ⛔ **Low** — its **pre-FIRST** value | `[]` |

**(d) History grew in every case** — 1 → 4 → **8** (a) · 5 → **7** (b) · 7 → **13** (c). Every withdrawal is a **new
event**; every origin event survives **byte-identical**.
**(e) the chevron** — `Open[on] ⇄ Addressed ⇄ Resolved` → `Addressed[on]` → `Resolved[on done]` → **withdraw + analysis
update** → **`Open[on]`**. **The track came back.** Zero one-way arrows.
**(f) no regression** — Slices 1–9 + the rest of Slice 10: **123/123 guards green in all 6 configurations, 0 console
errors**, 281 NCs bite.

## ⬜ Escalated — one thing, and it is a rule the build had to choose

- **O-D193-1 — what does the analysis update FIND when the document was NOT restored?** D193a settles the document
  (kept) and the attestation (dropped) and says an analysis update runs — **but not what that run should find.**
  **Built by derivation:** OSLO's change is **still in the text**, so the gap it closed is **still closed in the
  text** — the run **does not re-open an issue it cannot see**; what it *does* find is that the document is **no
  longer confirmed by the user**, so the basis falls to *From OSLO*, Reliability falls with it, and the History event
  says exactly that. *(Re-opening the issue anyway would be OSLO asserting a gap the text does not have, on the
  strength of a withdrawn confirmation — that looked like inventing a read.)* **If the owner wants it re-opened
  regardless, it is one clause in `_analysisUpdateAfterWithdrawal()`.**


---

# D194 — The Progress rows: say it once, and say it in the ratified vocabulary (2026-07-13)

**Target:** `vertical-slices/slice-10-tiering-limits/prototype.html`, amended in place. **No regressions.**

## What changed

**1. D194a — the LOAD-BEARING row stopped saying it twice.**
It rendered **label** `YOUR READ RESTS ON` **and value** *"13 inferences **your read rests on**"* — a straight
**D179e** violation (one home), in the row carrying the single most valuable number in the product.
> **`YOUR READ RESTS ON` · *12 inferences* ↓7 · *See them →*** — ~60% less text, nothing said twice.
**The delta and the Inference-Map link are byte-for-byte unchanged.**

**2. D194c — the GROUNDED row adopted the ratified epistemic classes.**
It said *"Your evidence: 17 claims · OSLO inferred: 12"* — true, and in words the product used nowhere else.
> **`Grounded` · From OSLO **11** · Confirmed by you **17***  (D011/D069)

**The owner proposed *"AI Interpretation | Your Understanding."* The instinct is exactly right — the epistemic
classes ARE that distinction — and both words are already canonical at a different size:**
- **`interpretation` is ONE of the six `ContextItem.item_type`s.** Using it for ALL inferences makes the word mean
  two sizes (**DL-053 Disambiguation Register**).
- ⛔ **"Understanding" is the most load-bearing word in the product — Confidence IS understanding maturity.**
  *"Your Understanding"* meaning *"the claims you grounded"* would make **understanding** name **OSLO's assessment**
  and **the user's evidence** on the same screen. **Drift, day one, in the highest-value term we own.**
- **The product never calls itself "AI." It calls itself OSLO.**

**Using the class names instead TEACHES them** — the user meets *From OSLO* / *Confirmed by you* on issues,
documents, reports and the Inference Map. **One vocabulary, everywhere.**

**3. The names are single-sourced.** `EPI_CLASSES` (registry) → `epiClassName()` (one reader) → `_epiLabelHTML()` /
`_paintEpiClassLabels()` (one painter). **18 label sites routed**; every class label carries `data-epi-class`; the
**static** labels (the Outcome-Confidence chip, the Inference-map key) now carry **no class name in the markup at
all**. The **third class (*Attested by \<name\>*) is REPRESENTABLE**: the row is a **map over the registry**, not two
slots. It is **ABSENT today** — reviewer evidence attaches to an ISSUE, not a `ContextItem` (D115) — and **absent is
correct** (D173: never a zero).

**4. D194d — the rows were NOT merged**, and a guard now forbids it structurally.

**5. The sweep.** *"Your evidence:"* / *"OSLO inferred:"* are gone from rendered copy, the **TOUR registry** and
**`PN_SLOTS`**. The **Inference-map key** now names the same two classes the ledger does.

## ⛔⛔⛔ THE FINDING — the two rows do not share a denominator

**The D194d guard found it; nobody read it.**
- **GROUNDED counts CLAIMS** (`item_type='claim'`, DL-109 §2a) → **11 From OSLO · 17 Confirmed by you**.
- **YOUR READ RESTS ON counts INFERRED ITEMS OF ANY TYPE** (DL-109 §2b / D181) → **12**, from **37** inferred items.

> **So load-bearing (12) legitimately EXCEEDS "From OSLO" (11). Both numbers are right.**
> **Merged, the panel would read *"12 of the 11 things OSLO made up"* — not a ratio, not a subset, not true.**

**This is the sharpest argument for D194d there is** — and it does **not** resolve the *adjacency*. **ESCALATED as
O-D194-1** with three honest options and no assumption made.

## D166 — three guard defects, caught by the harness, fixed in the guard

| # | Defect | Fix |
|---|---|---|
| **#30** | `_assertInferencesAreCalledInferences()` (D183d) read `el.textContent`, which **welds adjacent elements**. Removing the trailing phrase produced **`"12 inferencesSee them"`**, and the guard's own `\binferences\b` boundary **could not see the word it was looking for. It reddened a correct panel.** | New reader `_pgReadableText()` — leaf by leaf, joined by whitespace, **the way the eye reads it**. *(Padding the markup with a cosmetic space would have been shaping the product to fit a broken instrument.)* |
| **#31** | My own `_assertNoProgressRowSaysItTwice()` tested *"value contains label"* on every row → the **OPEN** heading reddened on its own count ***"Open questions"***. **Had it been "fixed" by renaming the count, a guard would have edited ratified canon to satisfy a regex.** | The rule, stated precisely: **(i)** a **phrase label (≥2 words)** may not reappear as a phrase in its own value; **(ii)** **no cell may BE its heading**, on any row. A shared **noun** is neither. Must-not-fire control added. |
| **#32** | My own source-literal test required the literal to **BE** the class name — but a painter types `'<span…>From OSLO</span>'`, with the name **embedded**. **It matched zero things.** **Its own NC caught it** (D166 §2, earning its keep). | The name is searched **inside** every literal; **case-sensitive**, so ordinary English (*"not confirmed by you"*) is not graded as a class name. |

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` on the extracted script | **PASS** |
| 2 | jsdom **without** `runScripts` | body children **31 → 31, byte-identical structure** |
| 3 | **All boot guards × full config matrix** (first-run · signed-in · first-value · Basic · Pro+light · notes-on) | **128/128 green in all 6 configs · 0 console errors** *(123 → 128: +4 D194 guards, +`d182FenceLifted`)* |
| 4 | **Negative controls — every suite** | **14 suites · 302 controls · every one bit or held.** `_d194NegativeControls()`: **21 controls (13 bite + 8 must-not-fire)** |
| 5 | **D182 — zero prompts from the harness** | `_promptReachesTheUser() === false` after the **entire** suite · probe blind down · `d182FenceLifted === true` |
| 6 | **AA, both themes** | `.pg-cl` = `var(--muted)`, the token this panel already uses — **no new colour**. Dark **8.77:1** · Light **8.03:1** (AA = 4.5:1). Count `<b>`: **15.05** / **16.56** |
| 7a | Neither row repeats its own label | *"your read rests on"* — **exactly 1 occurrence** (the label) |
| 7b | Class names render from the single registry; a third class is representable | Registry rename → **every label follows**. `EV-AT3-Dana Whitfield` on a live claim → **a third cell appears**, named *"Attested by Dana Whitfield"*, with its own home, displacing neither other class |
| 7c | The two rows stay distinct | **2 separate `.pg-row` hosts** · no ratio grammar on either |
| 7d | Orphaned phrasing gone — **DOM, TOUR registry, PN_SLOTS** | **GONE from all three** |
| 7e | Delta arrows + Inference-Map link, D187 valence intact | `↓7` load-bearing = **neutral** · `↑2` issues = **neutral** · `↑1` resolved = **`earned` (green)** · **no `red` field exists** |
| 7f | Slices 1–9 + the rest of Slice 10 | **No regression** — every pre-existing guard and NC still green |

## Constraints held
Counts **computed** (D173) — the third class is **ABSENT, not zero** · one home (D179e) · **no red; green only on
user-driven counts** (D187) · **`grounded` is still NOT user-driven** (O-D187-1 — respected as built) · severity
colour issues-only (D003) · no *"Blocker"* / *"holding it"* (D186) · no first person outside chat (D183a) ·
**"documents"** (D183e) · no 0–100 index (D183b) · **Outcome Confidence** · **the probe fence holds** (D182) ·
**withdraw/attestation machinery (D191–D193) untouched.**

## Escalated — not invented
- **O-D194-1** — the two rows count **different populations** and sit adjacent. **Owner decision.**
- **O-D194-2** — *"Attested by \<name\>"* has **no ratified name when there is more than one attester.** The registry
  therefore **requires** the name and draws nothing without it. **Owner decision.**
- **O-D194-3** — prose that *mentions* a class name is **not** registry-wired (several such sentences live in the
  D191–D193 withdraw machinery, which was explicitly out of bounds). **Stated, scoped, on the record.**

---

# D195 (owner P1, 2026-07-13) — a class that resolves to NOTHING shipped a dialog with no background

## The defect, and why it is the important one

The *Usage & limits* dialog was `<div class="wm">`. **`.wm` is defined nowhere.** Five other dialogs carry
`.wmodal`. **No background, no border, no radius — the page bled straight through the modal.**

> **It was never a colour bug. It was a NAME bug — and the name looked perfect.**
> **The THIRD defect of this shape:** twice a **guard selector** matched **ZERO elements** and passed for free;
> now a **CSS class** matched **ZERO rules** and rendered a transparent modal. **The pattern is the bug.**
> *(A class name is never declared, never imported and never checked. It is just a string that either hits a rule
> or silently does not. That hole is now closed.)*

## What was built

**Four new boot guards (128 → 132) and a 15th NC suite (302 → 327 controls).**

| Guard | What it proves |
|---|---|
| **`_assertEveryDialogHasAnOpaquePanel()`** | The **COMPUTED background** of **all 25** dialog / modal / popover / drawer / menu panels — `getComputedStyle` → **resolve the `var()` chain** → parse to RGBA → **alpha exactly 1** — **in BOTH themes.** ⛔ **It grades the computed style, never the class name.** The apparatus **proves itself first** on four probes; an **empty enumeration**, a **selector that matches nothing**, or a **blind resolver** ⇒ RED **without grading a single panel**. **Two completeness sweeps** (every `*Scrim` that holds anything · every `role="dialog\|alertdialog\|menu"`) make **forgetting mechanical, not moral.** |
| **`_assertEveryClassNameResolves()`** | **A name must resolve to SOMETHING** — a CSS rule that paints it **or** code that reads it. **A WRITE IS NOT A READER.** Swept on the **live DOM**, the **render paths**, and the **writes**. |
| **`_assertOsloIsTheInferringActor()`** | **PLANS DO NOT INFER. OSLO DOES.** The rule, not the string — and the **positive** half is measured too. |
| **`_assertFalseConfidenceFlagCountsAreComputed()`** | **STATE PROOF** (D173): add three inferences to the flagged document and **the numbers must move** (**4 of 7 → 7 of 10**). |

## The dangling-class sweep — 8 found, 8 fixed, 0 remain

| Name | Where | Consequence | Fix |
|---|---|---|---|
| ⛔⛔⛔ **`.wm`** | *Usage & limits* dialog | **transparent modal** — the P1 | → `.wmodal` *(lead's fix, verified)* |
| ⛔⛔ **`.in`** | Readout **Signed** input — **a RENDER PATH** | **the field the memo goes out under rendered as a RAW BROWSER INPUT** (white box, black text, square corners) inside a dark themed popover — **and only when the popover opens, which is why no DOM scan ever saw it** | → `.wm-in` |
| ⚠️ **`.referral`** | waitlist signal chip | a **data value interpolated into the class namespace** (`class="wl-sig <key>"`); `.review` has a rule, `.referral` never did — **and the next key added would have dangled too** | → `class="wl-sig" data-sig="<key>"` + `.wl-sig[data-sig="review"]`. **Byte-identical rendering; the latent class of defect is gone.** |
| `.attach-hint` | intake attach hint | none — the span is fully inline-styled | **removed** |
| `.hart` | Attention-map row header | none — `.heat-rowh` already carries the cursor + hover | **removed** |
| `.pg-star` | Progress GROUNDED row | none — every reader keys on `[data-row="grounded"]` | **removed** |
| `.hli` | History list-item wrapper | none — the wrapper's job is `role="listitem"`; the styled row inside is `.hrow` | **removed** |
| `.pn-on` | `<body>` (**write-only**) | none — nothing painted it, nothing read it | **removed** |
| `.superseded` | retired chat clarification boxes (**write-only**) | none — the stand-down is the id removal + disabled controls, which still happen | **removed** · **⬜ ESCALATED (O-D195-1)** |

⛔ **NO RULE WAS INVENTED TO MAKE A DEAD NAME RESOLVE.** A dangling class on a decorative element is harmless —
and it is still a name that means nothing. Each dead name was **deleted, not styled**; **inventing a look so a
guard goes green would be inventing product design to satisfy an instrument** (D166 §3, inverted).
**Zero false positives:** `.pn-slot`, `.sb-art` and `.anno-peek` paint nothing and **do real work** — the product
finds elements by them — and the guard correctly leaves them alone.

## Verification (all run; all green)

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | ✅ **PASS** |
| 2 | jsdom **without** `runScripts` → body children | ✅ **31** (unchanged) |
| 3 | **All boot guards × the full config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | ✅ **8/8 configs · 132/132 guards green · 0 console errors** |
| 4 | **Every NC bites; must-not-fire green** | ✅ **15 suites · 327 controls · 0 dead** (`_d195NegativeControls()` = **25**: 19 bite · 6 must-not-fire) |
| 5 | **D182 — zero prompts from the harness** | ✅ `promptsOpen=0` · `_PROBE.depth=0` · no `data-probe` · **0 deferred prompts** · fence lifts clean in all 8 configs · **body children 31 → 31** after the full suite |
| 6 | **AA, both themes** | ✅ `.wm-in` **13.15 / 15.05** · `.wmodal` **15.05 / 16.56** · `.wm-sub` **8.77 / 8.03** · `.wl-sig` **4.67 / 4.75** · `.inf-sub` **8.77 / 8.03** · `.inf-flag` **15.05 / 16.56** — **no new colour token** |
| 7a | **The *Usage & limits* dialog has an opaque panel — MEASURED** | ✅ `<div class="wmodal">` · computed bg **`#1B1F24`** dark / **`#FFFFFF`** light · **alpha 1.0** · border 1px · radius 16px |
| 7b | **Every dialog does** | ✅ **25 panels × 2 themes, alpha 1** |
| 7c | **No dangling class names** | ✅ **0** across DOM + render paths + writes |
| 7d | **The copy renders, with COMPUTED counts** | ✅ subtitle: **"Where OSLO inferred"** · flag: ***"Scope reads strong — but 4 of 7 items read as inference, most from OSLO. Worth verifying first."*** → **+3 inferences → "7 of 10"** |
| 7e | **Slices 1–9 + the rest of Slice 10** | ✅ no regression — every pre-existing guard and all 302 pre-existing NC controls still green |

## Guard defect #33 — mine, and the guard caught itself

The first draft of `_assertOsloIsTheInferringActor()` walked the text of `<body>` — **and `<script>` lives inside
`<body>` in this file.** So the guard was handed **the entire source of the product, including its own doctrine
comment explaining why *"the plan inferred"* is wrong**, and reddened on it. **A guard that is its own subject.**
Fixed with **`_screenText()`** — `SCRIPT` / `STYLE` / `NOSCRIPT` / `TEMPLATE` subtrees rejected. **Code is not
copy.** *(The same discipline from the other side: guards and their NCs are excluded from the class-name sweep by
the same rule the probe fence uses — otherwise an NC's own `.ip-probe` scaffolding would fail the build.)*

## Doctrine held

Counts **computed** (D173 — the flag's numbers proved by **moving the state**) · one home (D179e) · no first
person outside chat (D183a) · **"documents"** (D183e) · no *"Blocker"* / *"holding it"* (D186) · **no red; green
only on user-driven counts** (D187) · no 0–100 index; **Outcome Confidence** (D183b) · severity colour issues-only
(D003) · **the probe fence holds** (D182) · **withdraw/attestation machinery (D191–D193) untouched** · **the two
Progress rows stay distinct** (D194d).

## Escalated — not invented

- **O-D195-1** — should a **retired clarification box LOOK retired**? The dead `superseded` class is removed; **a
  visual treatment was not invented.** **Design decision.**
- **O-D195-2** — **only the band-1 waitlist signal is accented.** Previously an *accident* of naming; now a
  deliberate rule with identical rendering. **Whether `referral` should also be accented is an owner call.**
- **O-D195-3** — the sweep reads every product function **reachable from `window`**. A `class="…"` literal inside
  a function closed over by an IIFE would not be swept. **None exists today; the boundary is stated, not assumed.**
  A true build-time sweep of the raw file would close it — **build-tooling decision.**
- **O-D195-4** — `#annoPop` is the only **lazily-created** panel; the guard instantiates the real element and puts
  it back. **This works because the factory is idempotent.** A future non-idempotent factory must say so in its
  registry entry.

---

# D196 — "Stabilize" REJECTED. The VERB becomes "Confirm"; the STATE stays "grounded." (owner, 2026-07-13)

> # **THE USER CONFIRMS. THE READ IS GROUNDED.**

**One vocabulary change. Five copy sites, one of which no human grep found — and one GUARD that was holding the
old word in place and would have reddened the build for obeying the newer decision.**

## The sweep — every site, changed and deliberately not changed

### CHANGED — the imperative addressed to the user (D196a)

| # | Site | Kind | Before | After |
|---|---|---|---|---|
| 1 | `#ov-limit` (line ~3274) | **static DOM** | *"**Feasibility** — the lowest. Ground it to lift the read."* | *"…**Confirm it** to lift the read."* |
| 2 | `renderLimiter()` (~7716) | **render path** | same string, rebuilt on every read | **Confirm** |
| 3 | `#cpp-limnote` in `renderConfPop()` (~7897) | **render path** | same | **Confirm** |
| 4 | `#cpp-out` — the way-out CTA (~7904) | **render path, object is a VARIABLE** | `'Ground ' + lim + ' →'` | `'Confirm ' + lim + ' →'` |
| 5 | ⛔ **`#cg-feas-tipb` — the CAF-row tooltip (~3356)** | **static DOM, HOVER-ONLY, lowercase** | *"…the lowest dimension — **ground it** to lift the read."* | *"…**confirm it** to lift the read."* |

> ## ⛔ **SITE 5 IS THE STORY.**
> **I grepped the file for the imperative and found four sites. The GUARD found five** — on its first run, before
> I ever ran it against a negative control. `#cg-feas-tipb` is a hover-only `.caftip` body, lowercase, inside the
> hero. **A manual sweep does not see it. `_screenText()` does.**
> **This is exactly what D196c is for: *the split must be MECHANICAL, not remembered.***

### CHANGED — the guard that had become the doctrine

**`_assertConfPopIsAReadout()` clause (5)** asserted **`/\bground\b/i`** on the limiter (D185.4: *a limiter without
a verb is trivia*). **So the instant the copy obeyed D196, the build would have gone RED for being right.**
> ⛔ **A GUARD THAT PINS A WORD THE DOCTRINE HAS MOVED HAS BECOME THE DOCTRINE.**
> Clause (5) now asserts **`/\bconfirm\b/i`**. **Fix the GUARD, never the doctrine (D166 §3). Guard defect #34.**
> Its NC (`theLimiterLosesItsVerb_bites`) still bites — it injects *"is holding it back"*, which has neither verb.

### DELIBERATELY NOT CHANGED — and each one is a rule, not an omission

| Site | Still says | Why |
|---|---|---|
| `_GROUNDING_WORDS` — the Reliability band | *barely · thinly · partly · largely · well **grounded*** | **D196b.** ⛔ *"evidenced"* collides with **Evidence**, one of the three Reliability components — **the two-sizes-of-one-word error of *interpretation*** (D194b). ⛔ *"confirmed"* cannot carry it: **a read is grounded by EVIDENCE and by *Attested by \<name\>* — and that is NOT the user confirming.** |
| `.inf-lead` | *"Your evidence is **solid ground**."* | **A NOUN.** The foundation metaphor **D186** built (*"your read **rests on**…"*). Replacing it would leave *"rests on"* with nothing to rest on. → **O-D196-3** |
| §4b velocity card | *"**you grounded** 3"* | **PAST TENSE — a measured fact about the user's own work, not an order.** **See the escalation below.** |
| Chat off-script line | *"I don't have a **grounded** answer to that"* | **The STATE sense** (*an answer resting on evidence*). Legal under D196b. |
| Progress panel doctrine | *"Progress is **grounding**, not clearing"* | **A gerund with no object, addressed to nobody.** Not an imperative. |
| Code · guard names · doctrine comments | *"the user **grounds** an artifact"* | **D196a's scope is copy addressed to the user.** Internally the state machine already writes **`basis='attested'`**. **No user-facing surface says it** — guard-proven: **0 hits across 9 views, the tour, the notes and 8,499 render-path literals.** → **O-D196-2** |

## ⚠️ ESCALATED — O-D196-1: the grounding VELOCITY row. **DECIDED, and named rather than buried.**

**The brief: *"If that phrase is an imperative it changes; if it is a past-tense STATE of the user's own action,
decide and say which. Escalate if ambiguous — do not guess."***

**It is a PAST-TENSE STATE. It does not change. Two reasons, and the second is the load-bearing one:**
1. **It is not addressed to the user — it reports on them.** *"you grounded"* is a **stat-cell label on a computed
   count** (`_ciVelocity().you`, gated on `_ATTEST_AT[art]`), subject *"you"*, verb in the past. **D196a's scope is
   *"every imperative / call-to-action / button / link addressed to the user."* This is none of those.**
2. ⛔ ***"you confirmed"* WOULD HAVE IMPORTED THE VERY ERROR D196 EXISTS TO PREVENT.** It would put **the user's
   verb and the ratified class name *"Confirmed by you"* on TWO COUNTS, one panel apart, over TWO DIFFERENT
   POPULATIONS** — **this week's** newly-attested claims (§4b) versus **every** claim the user has ever confirmed
   (the Progress ledger, D194c). **That is D194b's two-sizes-of-one-word error, arriving through the fix.**

**And the product already says the chain out loud, in that cell's own tooltip:** *"Claims that became yours this
week, **because you confirmed** the document they came from."* → **THE USER CONFIRMS. THE CLAIMS BECOME GROUNDED.**
**D187's green — the only green in the panel — is untouched.**
**⬜ The owner may override.** The honest override is **not** *"you confirmed"* (it collides) but a **re-cut of the
cell around a different object** (*"documents you confirmed"* — a different population, a different number).
**That is a product-design change, not a copy sweep. It has NOT been made.**

## `_assertConfirmIsTheVerbAndGroundedIsTheState()` — D196c, made mechanical

**Two prohibitions, BOTH directions. Graded by ROLE, never by substring.**

| Clause | What it measures | Vacuity bar |
|---|---|---|
| **(a)** | **The vocabulary itself**: every `_GROUNDING_WORDS` entry ends in *grounded* and contains no *confirm*; `_groundingWord()` returns one of them | fails if the vocabulary is absent |
| **(b)** | **The STATE, on screen** — `#cpp-grdword` · `#ov-rel` · `#cp-grd` each read *"… grounded"* | fails if **not one** qualifier is on screen |
| **(c)** | **The VERB, on screen** — `#ov-limit` · `#cpp-limnote` each carry **Confirm** | fails if **no limiter** is on screen |
| **(d)** | **THE PROHIBITIONS, SWEPT — five surfaces** | fails on < 400 chars of screen text, an empty TOUR, an empty `PN_SLOTS`, or < 500 literals |
| **(e)** | ⛔ **The sweep did not eat its own justification** — `epiClassName('you')` is still **"Confirmed by you"** *and it still renders in the GROUNDED row* | measured on the rendered ledger |

**The five surfaces** (because the words reach a human through all five):
**the DOM** (`_screenText()`, SCRIPT/STYLE rejected) · **the attributes a user reads** (`title` · `aria-label` ·
`data-tip` · `placeholder`) · **the TOUR registry** (*twice caught teaching a dropped concept*) · **`PN_SLOTS`** ·
**the RENDER PATHS** (`_edCodeOf()` per function, comments stripped — with a **tail rule** for
`'Confirm ' + lim`, a CTA whose **object is a variable** and which **no DOM scan can see until the state that
renders it arrives**).

**The role test:**
- the VERB rule fires **only on the bare-form verb + a DIRECT OBJECT** (*"Ground it" · "Ground Feasibility"*), and a
  **noun-context determiner** (*"solid ground"*) **drops the hit**;
- the STATE rule fires **only on an intensity adverb + "confirmed"** (*"well confirmed"*) — **never on the class
  name.**
- ⚠️ **WORD BOUNDARIES:** *"back**ground**"*; *"lowest" contains "owes"* (DL-109 §3).
- ⚠️ **THE SCANNER IS NOT ITS OWN SUBJECT** (D166 — it has bitten this file before): `_screenText()` rejects
  SCRIPT/STYLE, `_edCodeOf()` strips the doctrine comments **which necessarily quote the dead imperative to explain
  why it died**, and guards/NC suites are excluded by the same rule the probe fence uses.

## `_d196NegativeControls()` — 18 controls, 0 dead

| Bites (11) | Must not fire (6) |
|---|---|
| *"Ground it to lift the read"* back **on a button** | ✅ ***"Confirmed by you"*** — a ratified **epistemic class** |
| *"Ground Feasibility →"* back **on the CTA** | ✅ ***"largely grounded"*** — the **STATE** |
| a **PAINTER** rebuilds the imperative (*not on screen in this state*) | ✅ ***"you grounded"*** — **past tense**, D187's green |
| the **TOUR** teaches *"Ground the document…"* | ✅ ***"Your evidence is solid ground."*** — a **NOUN** |
| a **prototype note** teaches it | ✅ ***"background" · "groundbreaking" · "Progress is grounding, not clearing"*** — **word boundaries / objectless gerund** |
| a **tooltip** gives the order | ✅ the **Progress doctrine is intact** (D179e · D187 · D194d · D183c · D194c) |
| the limiter **loses its verb** entirely | |
| the band renders **"well confirmed"** | |
| the **vocabulary itself** is rewritten to *"largely confirmed"* | |
| the state says *"largely **evidenced**"* | |
| ⛔ the sweep **mangles the epistemic class** to *"Grounded by you"* | |

*(plus `passesAsShipped` — the guard is green on the shipped build, or every "bites" above would be meaningless.)*

## Verification (all run; all green)

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | ✅ **PASS** |
| 2 | jsdom **without** `runScripts` → body children | ✅ **31** (unchanged) |
| 3 | **All boot guards × the full 8-config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | ✅ **8/8 · 132/132 guards green · 0 console errors** (131 → **132**: `confirmIsTheVerb`) |
| 4 | **Every NC bites; must-not-fire green** | ✅ **16 suites · 345 controls · 0 dead** (327 + **18** = 345) |
| 5 | **D182 — zero prompts from the harness** | ✅ `_PROBE.depth 0` · **164 prompts captured, 0 shown** · `_promptReachesTheUser() false` · `_upDeferred 0` · no `html[data-probe]` · no modal on screen · body children **31 → 31** |
| 6 | **AA, both themes** | ✅ `.cr-limit` **5.34 / 5.34** · `.cr-limit b` **15.05 / 15.05** · `.cpp-limnote` **4.67 / 4.67** · `.caftip` **4.67 / 4.67** · `.cpp-grd` **4.67 / 4.67** — **D196 added ZERO CSS rules, ZERO colour tokens, ZERO class names** |
| 7a | **Every user-facing imperative says CONFIRM** | ✅ `#ov-limit` · `#cpp-limnote` · `#cpp-out` · `#cg-feas-tipb` — **4/4** |
| 7b | **Every Reliability state still says GROUNDED** | ✅ `_GROUNDING_WORDS` = *barely/thinly/partly/largely/well **grounded*** · `#cpp-grdword` · `#ov-rel` · `#cp-grd` — **3/3** |
| 7c | **"Confirmed by you" still renders as the epistemic class** | ✅ `epiClassName('you')` = **"Confirmed by you"**, live in the GROUNDED row: ***From OSLO 11 · Confirmed by you 17*** |
| 7d | **The tour and the notes teach the same split** | ✅ **TOUR: 0** ground-imperatives · **PN_SLOTS: 0** (7 slots) |
| 7e | **No regression — Slices 1–9 + the rest of Slice 10** | ✅ **9 views swept, 0 violations** · every pre-existing guard and all **327** pre-existing NC controls still green |

## Doctrine held

Confidence = understanding maturity, **never** health/readiness/probability · **Confidence band and Reliability
vocabulary share NO word** (D183c — and D196 *widened* the separation: the band speaks *grounded*, the user is told
*Confirm*) · counts computed (D173); one home (D179e) · no first person outside chat (D183a) · **"documents"**
(D183e) · no *"Blocker"* / *"holding it"* (D186) · **no red; green only on user-driven counts** (D187 — *"you
grounded"* untouched) · no 0–100 index; **Outcome Confidence** (D183b) · severity colour issues-only (D003) ·
**OSLO is the inferring actor** (D195) · every class name resolves; every dialog panel is opaque (D195) · **the
probe fence holds** (D182) · **withdraw/attestation machinery (D191–D193) untouched** · **the two Progress rows
stay distinct** (D194d).

---

# D197 · D198 · D199 — the NAME, the MARKER, and the guard that was never built (2026-07-13)

## TASK 1 — D197: the term is **LOAD-BEARING**

**One registry, `TERMS`, and every surface reads its name from it.**

| Surface | Was | Is |
|---|---|---|
| Progress row **label** | `YOUR READ RESTS ON` | **`LOAD-BEARING`** |
| Progress row **value** | *"12 inferences ↓7 · See them →"* | **unchanged** (see the escalation below) |
| Count-registry **name** | *"Inferences your read rests on"* | **"Load-bearing inferences"** |
| Assumption row **chip** | `YOUR READ RESTS ON THIS` | **deleted — it is a MARKER now** (D198) |
| Section header | *"The ones your read rests on come first"* | **unchanged — PROSE** |

**Swept:** the DOM · every `title`/`aria-label`/`data-tip`/`placeholder` · the **TOUR** · **`PN_SLOTS`** · the render
paths. **0 surviving hits of the dead label.** ***"Rests on" survives as prose*** — the header, the chat's *"What
this rests on"*, the popover's reliability basis — **and a guard clause FAILS if that prose ever disappears.**

**`_assertLoadBearingIsTheOneName()` is a mechanism, not a grep:** it swaps `TERMS` for a **sentinel**, repaints, and
requires every naming surface to show the sentinel. *A surface still showing the real word has the name typed into
it — which is exactly how D199 happened.*

> ## ⛔ **ESCALATION — O-D197-1. D197's VALUE LINE COLLIDES WITH D194a, AND I CHOSE D194a.**
> D197 says the value becomes ***"13 load-bearing inferences."*** **But the value is already *"13 inferences"* —
> D194a stripped the trailing phrase, because the LABEL IS THE SENTENCE (one home, D179e).** Rendering *"12
> **load-bearing** inferences"* **beneath a `LOAD-BEARING` label puts the name in two homes**, and
> `_assertNoProgressRowSaysItTwice()` goes **RED** on it. **So the row renders `LOAD-BEARING · 12 inferences ↓7`,
> and the full phrase is `TERMS.loadbearing.name`, spoken where there is no separate label.**
> **If you want the literal D197 line, D194a must be amended for this row — one line, plus the guard.**

## TASK 2 — D198: **a MARKER, not a LABEL**

**The chip and `VERIFY` are gone. A gutter is reserved on EVERY row, in the ROW's own rule; the marker paints into
it, `position:absolute`, and cannot enter the flow.** `.mk-on` **declares no flow property at all.**

### The geometry — **measured**

| | marked | unmarked |
|---|---|---|
| `.inf-item` in-flow children | `span.tx \| span.inf-src` | **`span.tx \| span.inf-src`** |
| `.inf-item` box (`pad-l \| pad-r \| mar-l \| mar-r \| display \| gap`) | `20px \| 2px \| 0px \| 0px \| flex \| 11px` | **identical** |
| `.inf-row` in-flow children | `span.inf-nm \| span.inf-pips \| span.inf-ct` | **identical** |
| `.inf-row` box | `20px \| 8px \| 0px \| 0px \| flex \| 12px` | **identical** |

**Three clauses, none of them an assertion:** *(1)* the **in-flow child signature** (out-of-flow nodes excluded **by
declaration** — `data-flow="none"` — and the declaration then **proven** against the cascade); *(2)* the **computed
box model**; *(3)* **real pixels**, within 1px — ⚠️ **jsdom has no layout engine, so every rect is zero and clause
(3) DECLARES that it measured nothing and does not pass on its own.** *Rects that are all zero are ABSENT, not
identical* (D166 §1). **No headless browser exists in the build environment; the Chrome extension cannot read
`file://`. Escalated as O-D198-1.**

- **Not colour alone:** the discriminator is the **existence of a box** (`content` ≠ `none`, `width` > 0) — graded on
  the **values**, not on "is the property mentioned". `--cool` on the card: **6.13 : 1 (dark) / 6.28 : 1 (light)**
  (WCAG 1.4.11 wants 3:1). **No severity token** (D003).
- **`VERIFY` left the number column.** **7/7** rows are `role="button"` + `tabindex="0"` + Enter/Space →
  `openArtifact()`, and the `.inf-flag` callout keeps the **named** keyboard-reachable *"Open Resources →"*.
  **Two keyboard paths, zero resident buttons — a11y was not traded for tidiness.**
- **The meaning is on demand:** a new **ⓘ** on **both** section headers + the row's own `title` (DL-107/D185).

## TASK 3 — D199: the trend said "CONFIDENCE" **because a rule was ratified with no guard behind it**

**D183b bound the label AND the number. Only the number got a guard.** `_assertTheConceptIsCalledOutcomeConfidence()`
is the guard that should have existed.

**Fixed (the sweep found more than the screenshot):** the **hero `<h3>`** (the first panel of the Overview!) · the
**ramp's `aria-label`** (static **and** rendered) · the **trend ⓘ** and the **trend chart's `aria-label`** (the
owner's miss) · the **Overview "why" line** · *"the Confidence pill ↗"* · the **Slice-7 History placeholder** ·
**chat** (`_ansConfidence` · `_ansSummary` · `_ansChanged` · the Extended-pass notice · the citation chip) · the
**export package** and the **copied-to-clipboard text** · **four reviewer-view footers** · **two prototype notes**.

**Grade the ROLE, not the substring.** **(L1)** whole label · **(L2)** followed by a band or a number · **(L3)**
compounded into the concept's name (*trend/band/pill/score*) · **(L4)** subject of a state verb. ⚠️ ***"is" is a hit
ONLY when a band follows it*** — *"Confidence is understanding maturity — not project health"* **is the doctrine**,
and a guard that reddened on it would be a word filter (D166). **Must-not-fire: 3/3 green.**

**8 label sites, every one of which must RESOLVE.** ⛔ **The trend and the export package are DORMANT at boot — and
*"it wasn't on screen"* is exactly how D199 happened** — so the guard **paints them from their own render paths,
reads them, and restores every byte** (D182). **`NC-D199-11` hides the trend host → the guard goes BLIND and RED,
never quietly green.**

### ⛔⛔ THE SECOND MISS, FOUND BY THE SWEEP THIS DECISION ORDERED

**`PN_SLOTS.pnPayoff` still taught the SUPERSEDED D173d** — *"THE 0–100 INDEX IS NOT CALIBRATED … **DEMOTED, NOT
DELETED**: calibrate it and it earns its hero slot back."* — **live in the notes layer for the whole build.**
`_assertNoZeroToHundredIndexAnywhere()` read the DOM, the render paths, the snapshot, the cascade and the **TOUR**
— **and not `PN_SLOTS`.** **The note is rewritten and the guard now reads `PN_SLOTS`.** ⛔ **And the notes layer no
longer prints the index in ANY framing** — including the note that printed it *in order to say it was deleted*: *a
note that keeps printing it keeps it alive* (DL-107), **and a scanner cannot tell "teaching it" from "recording its
death" by looking at the digits.**

## D166 — FOUR MORE GUARD DEFECTS (#35–#38). Every one is a shape already on the list.

| # | Defect | Fix |
|---|---|---|
| **35** | ⛔⛔⛔ **A GUARD HELD THE OLD WORD IN PLACE AND WOULD HAVE GONE RED FOR BEING RIGHT.** `_assertNoHoldingItAnywhere()` clause (f) demanded the literal *"rests on"* in `#pg-counts`. **Under D197 the only way to green it was to put the DEAD LABEL BACK.** | It grades what it always existed to prove — **the count and its NAME survived the rename** — reading the name from `TERMS`. **A guard that pins a word the doctrine has moved is a RATCHET.** |
| **36** | ⛔⛔⛔ **A GUARD WOULD HAVE GONE QUIETLY VACUOUS.** `_assertNoProgressRowSaysItTwice()` only graded labels of **≥2 words** — and D197 makes the label ONE word. **It would have stopped grading the only row it was written for.** | The rule is *a row's name may not reappear in its own value* — **one word or five**, graded on the row's prose. |
| **37** | ⛔⛔ **A NEGATIVE CONTROL WOULD HAVE DIED SILENTLY.** `NC-D194-01` injected *"…your read rests on"*; under the new label **that injects nothing** — it would have gone on reporting `true` while testing **nothing**. | It injects **`TERMS.loadbearing.label`**, so it cannot drift out of alignment with the label again. |
| **38** | ⛔⛔ **A GUARD WITH A HOLE IN EXACTLY THE SHAPE OF THE NEXT DEFECT.** `_assertNoZeroToHundredIndexAnywhere()` swept five surfaces and **not `PN_SLOTS`** — where the superseded decision was still being taught. | It reads `PN_SLOTS` now, and the notes layer may not print the index at all. |

## Verification

| # | Check | Result |
|---|---|---|
| 1 | `node --check` | ✅ **PASS** |
| 2 | jsdom **without** `runScripts` → body children | ✅ **31** (unchanged) |
| 3 | **All boot guards × the full 8-config matrix** (Free/Basic × notes OFF/ON × first-value NO/YES) | ✅ **8/8 · 136/136 guards green · 0 console errors** (132 → **136**: `loadBearingIsTheName` · `markedRowsKeepGeometry` · `verifyIsNotAButton` · `itIsOutcomeConfidence`) |
| 4 | **Every NC bites; must-not-fire green** | ✅ **19 suites · 389 controls · 0 dead** (345 + **12** D197 + **16** D198 + **16** D199) |
| 5 | **D182 — zero prompts from the harness** | ✅ `_PROBE.depth 0` · `_promptReachesTheUser() false` · `_upDeferred 0` · no `html[data-probe]` · **0 modals on screen** · body children **31 → 31** |
| 6 | **AA, both themes** | ✅ the marker `--cool` on the card: **6.13 / 6.28** (WCAG 1.4.11 needs **3:1**) · **no new text colour token; no severity token** |
| 7a | **LOAD-BEARING everywhere, tour and notes included** | ✅ label `Load-bearing` · registry name *"Load-bearing inferences"* · marker `title` + a11y name · **0 dead-label hits** across DOM/attrs/TOUR/`PN_SLOTS`/render paths |
| 7b | **Marked and unmarked rows have identical text geometry — MEASURED** | ✅ in-flow signature **identical** on both surfaces · computed box model **identical** on both (`20px \| 2px \| …` and `20px \| 8px \| …`) · pixel clause live (⚠️ no layout engine in the harness — **O-D198-1**) |
| 7c | **VERIFY is out of the number column and still keyboard-reachable** | ✅ **0** actionable elements inside the stat rows · `.inf-verify`/`.inf-lbt` gone from **markup AND cascade** · **7/7** rows keyboard-activatable · the panel-level *"Open Resources →"* survives |
| 7d | **"Outcome Confidence" on every labelling surface** | ✅ hero · pill · popover · ramp aria · **trend ⓘ** · **trend aria** · whybox · export — **8/8**, with the guard proving it |
| 7e | **No regression — Slices 1–9 + the rest of Slice 10** | ✅ **9 views swept, 0 violations** · every pre-existing guard and all **345** pre-existing NC controls still green |

## Doctrine held

Confidence = understanding maturity, **never** health/readiness/probability · **no 0–100 index; the concept is
OUTCOME CONFIDENCE** (D183b/D199) · **Confirm is the verb; grounded is the state** (D196) · **OSLO is the inferring
actor** (D195) · counts computed (D173); one home (D179e) · no first person outside chat (D183a) · **"documents"**
(D183e) · no *"Blocker"* / *"holding it"* (D186) · **no red; green only on user-driven counts** (D187) · **severity
colour is ISSUES-ONLY — and the new marker carries none** (D003) · every class name resolves (`.mk` `.mk-on`
`.mk-sr`); every dialog panel is opaque (D195) · **the probe fence holds** (D182) · withdraw/attestation
(D191–D193) untouched · **the two Progress rows stay distinct** (D194d).

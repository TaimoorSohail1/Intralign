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

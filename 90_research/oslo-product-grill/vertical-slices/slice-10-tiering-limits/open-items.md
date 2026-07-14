# Slice 10 — Tiering & Limits · Open Items

---

# ⚠️⚠️ AMENDED 2026-07-12 — **D162 IS RATIFIED. READ THIS FIRST; EVERYTHING BELOW IT IS SUBORDINATE.**

**The owner rejected the Issue Panel as cognitively overwhelming.** The D159 sweep hit the modals and the big surfaces and **missed the panels — which is where the doctrine copy had accumulated worst**, because every doctrinal rule has a touchpoint on an issue (evidence · provenance · comments · share · append-only · CR-2) and each one had grown a paragraph explaining itself. **The panel had become a museum placard about the product.**

This is a **presentation / IA pass** — *no logic changes, no behavioural regressions, every runtime guard still passes.* Where anything below conflicts, **D162 wins** (and D162 extends D159, which still governs everywhere else).

## D162a — the copy rule (extends D159)

> **Say the honest thing ONCE, in the fewest words, at the moment it matters. Never twice. Never with its rationale.**

- Honest **labels** stay — *"Comments never change the assessment"* (D111), *"Evidence, not a verdict"*, *"previous analysis"*, *"Analysis is behind your edits"*, the reliability qualifier. **Once, and short.**
- **Contracts, rationale and reassurance move to an info affordance (ⓘ) — never resident.**
- **Deleted outright, and they stay deleted:** the *"◆ this is a validation recommendation — the kind a second pair of eyes settles fastest / prime candidate"* hint (**design rationale, said out loud**) · the *"0 review requests sent · free and unlimited — on every plan"* counter (**reassurance addressed to the OWNER, not the user**) · the duplicated *"never change the assessment"* sentence and *"a conversation about the read, recorded next to it"* · the append-only lecture · the *"Sends the issue + its context + the recommendation + the artifact reference. It never changes the issue."* contract (**→ ⓘ tooltip on the button**).

## D162b — progressive disclosure, driven by INTENT

The user opens an issue to learn **"what's wrong, and what do I do about it?"** Everything else is an action they *may* want.

**Always visible (the default state):** title · severity · dimension · where it lives (artifact + jump link) · lifecycle track · the plain-language read (*Why this matters* + the dimension impact) · **ONE primary action** — *Apply this fix* where there is a recommendation, *Answer* where OSLO is the one asking, otherwise none.

**Everything else is ONE scannable row** — label · count · chevron · **real hover state** — expanding in place, independently, keyboard-accessible (`<button>`, so Enter/Space work natively), with correct `aria-expanded`:

```
▸ Evidence · 2
▸ Clarification · Has the venue confirmed Wi-Fi for 500+ concurrent…
▸ Comments · 0
▸ Reviews · 1 · 1 awaiting        (only when reviews exist)
  [⤴ Share for review] ⓘ   [✦ Discuss with OSLO]
```
> ⛔ **D184 / D190c — THE RECOMMENDATIONS ROW IS GONE.** The recommendation is **resident above its button**
> (D184.1), and its **alternatives expand in place, directly beneath it** (`Other options (2)` → `#ipAlts`).
> **The disclosure row under Evidence was DELETED** — *the alternatives to a recommendation are part of the
> DECISION; Evidence is the RECORD.* Nothing about the fix is behind a chevron any more.

Row state persists **while the panel is open** (a re-render from `selectPath` / `addComment` must not collapse what the user opened) and **resets on close** — a fresh open is a fresh, minimal read.

## D162c — the three affordance defects, fixed

| Defect (owner-reported) | Fix |
|---|---|
| **Evidence looked FLAT** — it had a `▸` but no hover state, no cursor change, no affordance. The user could not tell it expanded. | The `.ip-rowh` component: **pointer cursor · hover background · chevron that rotates on expand · visible count · focus ring**. Every secondary section now uses it — one component, not five bespoke headers. |
| **Clarification defaulted EXPANDED**, with a large empty textarea dominating the panel. **A big empty textarea shouts "do work now"** at a user who came to *read*. | **Default MINIMIZED.** The row names what OSLO needs (question preview, truncated to 54 chars); the input appears on expand. *"Answer in chat →"* stays inside the expanded state. The **primary "Answer" button** (when OSLO has no recommendation) opens the row and drops the caret in it. |
| **Share for review carried three lines of explanation.** | **Just the button.** The contract lives on an **ⓘ**. The prime-candidate hint and the CR-2 counter are **deleted**. |

## D162d — cascaded

- **Recommendation panel** (the `.ip-rec` block): the *"Applying drafts the change into your plan. Discussing changes nothing."* note and the *"Recommendations live only inside the issue"* rationale → **ⓘ / button tooltips**. *"Possible resolution paths"* → **"Other options"** (D190b — *"path" is jargon dressed as plain English*). *"— recorded as your chosen approach"* → dropped (the **Confirmed by you** tag already says it).
- **Reviews block:** the responses stay **in full, forever** (that is the record) — the lecture around them does not. *"This is evidence, not a verdict … it went into an analysis run … OSLO did not accept it on your behalf"* + the D133 alignment essay collapse to **one line + an ⓘ**: *"**Evidence, not a verdict.** ISS-03 is still **Open**. · Attested by \<name\> · Folded into **Alignment**."*
- **Artifact flyout** (`.anno-pop`): the read (severity · dimension · what's wrong, truncated to 150 chars) + **Open issue →** and the span-specific **Ask about this →**. **"Share for review →" is gone from the flyout** — it fired a full modal out of a hover, and it lives one click away in the panel where its contract can sit on an ⓘ. **CR-2 is untouched: nothing disabled, nothing metered.**
- **Share dialog:** prime-candidate hint and CR-2 counter deleted there too.

## Word count — user-visible copy in the Issue Panel

| | Before | After | Δ |
|---|---|---|---|
| **Default state (what the user actually sees on open)** | **~206 words/panel** (1,236 across the 6 issues) | **71 words/panel** (427) | **−65%** |
| Copy present in the panel DOM at all (incl. collapsed rows) | 1,322 | 828 | **−37%** |

*The first row is the one that matters: the second measures what we **moved**; the first measures what the user is **made to read**.*

## What did NOT change — behaviour, guards, honesty

- **All 28 runtime guards (`window._S10`) still pass**, on **Free × Basic × notes-OFF × notes-ON**, **0 console errors**.
- **CR-2 holds absolutely** — *Share for review* is **never disabled, never metered**, on any tier, in any phase, to anyone (new or not). We stopped **narrating** it, not honouring it.
- Advisory-only; issues are **never resolved by hand**; the three epistemic classes (**From OSLO** / **Confirmed by you** / **Attested by \<name\>**) are untouched.
- **Clarification → History entries are byte-identical from the panel and from chat** (one path: `_submitClarification`).
- Manual editing stays free; *"Write my own fix in \<artifact\> →"* stays.
- All D159–D161 rules stand — prototype-notes toggle **OFF by default**, no meta in product copy, explanations on demand.

## Guard change — one, and it CLOSES a loophole (it does not relax anything)

**`_assertRecommendationNeverHidden()` (DL-103 §7d) would have passed VACUOUSLY** under the new disclosure model. It checked `getComputedStyle('.ip-rec').display !== 'none'` — but under D162 the recommendation sits inside a collapsed row, and it is the **ancestor** row body that is `display:none`, not the element. The element's own computed display is still `block`, so the guard would have reported "visible" about something nobody could see. **Same failure class as the D160 export-drawer loophole.**

**Fixed two ways, both required:**
1. The guard now **also fails if `.ip-rec` sits inside a `.ip-row:not(.open)`**. *(Negative control: force the row shut at the cap → the guard fails. It is not vacuous.)*
2. **The product opens the row itself the moment the cap can bite** — `_ipRows()` defaults the Recommendations row **open** when `_capHit('fixes')`, and `applyFix()`'s cap branch forces it open **before** raising the prompt. **The binding line is intact: the recommendation is always visible; only the assisted apply is metered; manual editing is always free.**

> ⛔ **Progressive disclosure is a disclosure, not a hiding place.** Do not "simplify" either half of this back out.

---


# ⚠️⚠️ AMENDED 2026-07-12 — **D159 · D160 · D161 ARE RATIFIED. READ THIS FIRST; EVERYTHING BELOW IT IS SUBORDINATE.**

**The owner has rejected the product's over-explanation of itself.** This is a **presentation / IA pass**, not a logic pass — *no behavioural regressions, every runtime guard still passes.* Where anything below this section conflicts, **D159–D161 win.**

## The rule (D159)

> **The doctrine governs what the product may CLAIM and DO. It must NEVER govern how much the product TALKS.**
> **Obey it everywhere. Speak it almost nowhere.**

The prototypes were built under instructions to *"carry the note in-product"* and *"say it out loud."* That was an error, and the owner has named it: **the say-it-out-loud test was a constraint on BEHAVIOUR** — *don't do things you'd be embarrassed to explain* — **and it was turned into a CONTENT REQUIREMENT** — *explain everything*. They are not the same thing. Conflating them turned the app into **a museum placard about itself**.

## What changed

| # | Decision | What changed in the build |
|---|---|---|
| **D159** | **No meta in product copy.** No canon references (`DL-###`, `D###`, `CR-2`, `CHG-061`, `UP-#`, `MON-04`, `§4c`), no rationale paragraphs, no governance vocabulary, no design commentary, no owner-TBD scaffolding. **Progressive disclosure:** explanations exist **on demand**, never resident. **Bias to simplicity everywhere — modals included.** | **Every** surface swept: Reports · Plans · Limits ("Your plan") · Settings · Share · Export · Access & invites · every UP prompt · chat · the demo scaffold bar · the reviewer-view ribbon · static chrome and tooltips. **User-visible copy across the measured surfaces: 17,485 → 6,465 words (−63%).** With the toggle **off**, a grep of the rendered DOM for `DL-` · `D###` · `CR-#` · `CHG-` · `UP-` · `MON-` · `§` · "owner-TBD" · "not ratified" · "naming pending" returns **ZERO hits**. |
| **D160** | **Reports: the reading surface is SACRED.** Default view = **the document, and only the document** — full-width, centred, comfortable measure, generous whitespace. Controls move **off** the surface into a slim toolbar/drawers, **closed by default**. | The 360px composer is **gone**. `#rptDoc` is now a centred page (~74ch, 56–60px padding). A slim `#rptBar` carries **Recipient · Sections · Format · Schedule · Export**; each opens a drawer in `#rptDrawer`, **all closed by default**, `Esc` returns you to the document. **Chrome around the document: 1,533 → 124 words (−92%).** |
| **D160** | The **package wrapper** (`#rptPkg`) is **export metadata**, not reading material. | Moved into `#rptPkgHost`, shown **only on the export preview**. It is still **always rendered and always carries the disclaimer** — canon requires it, and `_assertDisclaimerOnPackageNotInBody()` still proves it on every render. |
| **D160** | **Mandatory items keep their homes.** | **Currency marker** — stays in the memo body as plain attribution (D153): *"DevNorth 2026 · plan as of 12 July · ‹PM›"*. **Disclaimer** — on the package wrapper, seen at export. **Forecast note (D155)** — appears **only when triggered**, inline, subtle, dismissible. **Never resident** (verified: 0 resident notes on the default view). |
| **D161** | **ONE global "Prototype notes" toggle — OFF by default, persisted.** Off ⇒ it looks and reads like a product. On ⇒ every owner-TBD, canon citation, retired lever, guard name and escalation is revealed for governance review. | Lives in the demo scaffold bar (`#pnToggle`, `LS: protoNotes`). **The governance content is RELOCATED, NOT DELETED.** `pn(html, kind)` returns an **empty string** when off — the strings **never reach the DOM**. This is deliberately *not* `display:none`: "hidden but present" is exactly how meta copy creeps back. Styled as a hatched, monospaced annotation layer so it **can never be mistaken for product copy**. |

## What did NOT change — and this is the point

**The behaviour.** Every guard, every limit, every honest label. **28/28 boot assertions pass on Free AND Basic, with the toggle OFF and ON, with zero console errors.**

**Honest plain-English product copy stays**, because a product would actually say it: *"Analysis is behind your edits"* · *"previous analysis"* · *"Comments never change the assessment"* · *"From OSLO" / "Confirmed by you" / "Attested by ‹name›"* · the limit disclosures · the reliability qualifier · *"Nobody is ever removed"* · *"Asking anyone for their read is always free"* · *"Every plan gets the same read."*

**The test applied to every string:** *"Would a product actually say this to a user, or is this the team explaining itself?"* If the latter → it went behind the toggle.

## Guard changes (guards fixed, doctrine never)

- **`SELLING_SURFACES` re-pointed.** `reportsBody` **was** the composer; it is now the notes rail. Left alone, every copy prohibition would have started scanning an **empty div and passing for free**. The list now covers `rptBar` · `rptDrawer` · `rptDoc` · `plansBody` · `limitsBody` · `upBody`. **Coverage did not drop.** A new `REPORT_SURFACES` list scopes the report-specific scans.
- **`_assertNoDisabledLimitAffordances()` (D138) strengthened.** With the export drawer closed, `.rpt-act .btn` is not in the DOM — a selector-only check would have passed **vacuously**. The guard now **also demands a permanently-present, never-disabled entry point** (`#rptExportBtn`) on the toolbar. **Progressive disclosure is legitimate; an unreachable limit-bearing affordance is not.**
- **`renderAccess()` bug fixed:** a local `const pn` shadowed the global `pn()` note-builder for the whole function body (TDZ `ReferenceError`). Renamed to `phEl`.

## Verification

`node --check` PASS · jsdom without `runScripts` → 31 body children · **28/28 boot assertions on Free × Basic × notes-off × notes-on, 0 console errors** · rendered-DOM meta grep: **0 hits off / 672 hits on** · **negative controls fail correctly** (remove the toolbar Export → `d138` fails; gate editing on Free → `rptEditFree` fails; strip the package disclaimer → `rptDiscOnPackage` fails).

---

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


Owner-decision-required items **surfaced, not resolved**. **Nothing below was assumed.**

> ## ⚠️ REWRITTEN 2026-07-11 — the correction of record
>
> ~~**The headline.** `RELEASE_1_TIER_DEFINITIONS_V1` — cited as authoritative by 18 canonical documents — has never been written… **`tier-definitions-census.md` is that proof: 32 values · 21 ratified · 11 unset.**~~
>
> **That framing was half right and half wrong, and the wrong half mattered.**
>
> The missing document is real: **18 product documents cite a `RELEASE_1_TIER_DEFINITIONS_V1` that does not exist.** But the conclusion drawn from it — *"therefore the numbers have not been decided"* — was **false**. The numbers **were decided**, and they live in the **engineering zone**:
>
> **`30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1` — §4c**, with **owner-confirmed rows for every tier** (Free/Basic 2026-06-05; Pro/Team/Enterprise via **DL-074**, 2026-06-19).
>
> **The gap is not missing values. It is a missing product-authoritative surface that consolidates and names them.** A product-scoped reader — human or AI — does not find them. An AI that cannot find a number **invents one**. That has now happened twice: *"Basic = 10 projects"* (canon: **3**) and *"Basic's price is undecided"* (canon: **$12/mo**).
>
> **Corrected count: 53 values · 46 ratified · 3 recommendations · 4 unset → 6 genuinely open decisions.**
>
> **`RELEASE_1_TIER_DEFINITIONS_V1` must be written as a product-authoritative surface that CONSOLIDATES AND NAMES what is already ratified — not as a document that decides anything new.**

---


---

# ⬛ OPEN ITEMS AFTER DL-103 (2026-07-12) — **THIS SECTION SUPERSEDES SECTION A BELOW**

## The open list, re-derived

| # | Decision | Status in the build | Why it is open |
|---|---|---|---|
| **1** | **Monthly analyses per tier** | ⏳ **PENDING RE-DERIVATION — nothing enforced** | §4c's numeric basis is **suspended** (DL-103 §2/§4). Re-derive after the judgment-quality eval + **E1–E3** + a real cost-per-analysis measurement. **Do not tune it now** — that would bake a ~6× penalty into pricing permanently. |
| **2** | **Daily ASSISTED-APPLY cap — Free** *(NEW)* | ⬜ **UNSET ⇒ NO CAP.** Mechanism + at-cap prompt built; threshold inactive | **From Alpha instrumentation, never a cost model.** **Placement is the whole decision: above activation, below power use.** It is a **monetization lever**, and the record says so rather than dressing it as a cost control. |
| **3** | **Basic price — the BASIS** | ⏳ **$12 kept, basis marked pending** | The value is owner-confirmed; the **basis** is suspended. $12 may well survive — but it must survive a **derivation**, not an **inheritance**. |
| **4** | **Collaborator seats** | ⚠️ REC (Free 3 · Basic 10) — **Basic = 10 withdrawn by DL-103 as commercially unsound** | Still the only structurally undefined dimension. Team is **per seat**; a $12 Basic with ten seats cannibalises it. **No replacement invented.** |
| **5** | **OD-10 coalescing window** | ⬜ UNSET | **Now bounded by §7d-bis: it keys off the USER'S JOURNEY, never the tier.** |
| **6** | Free CRR cap · MON-04 prompt cap · CR-2-vs-gate · Billing rail | ⬜/⚠️ unchanged | See below. |
| **7** | **The report NAME** *(UPDATED — D148–D154)* | ⬜ **UNSET** — the build labels the artifact **DESCRIPTIVELY** ("Readout") and flags **"naming pending"** | Owner / glossary decision (**DL-053 Disambiguation Register**). **Anti-Assumption: the build does not name canon.** Two names are **ruled out by design and enforced at runtime** (`REPORT_BANNED_NAMES`): **"status report"** — the clerk artifact this feature exists to escape — and **anything implying health or readiness** (DL-104 §5, P1). |
| **8** | **Scheduling — R1 or fast-follow?** *(UPDATED — D148–D154)* | ⬜ **OWNER-OPEN.** **Built and flagged** (`SCHEDULING_R1 = null`) | A weekly readout is the PM's **recurring obligation**, and automating it is the **labour half of the lever** — so it is built. Whether it lands in **R1** or as a **fast-follow** is the owner's call, and the build does **not** assume it. **Binding either way:** a scheduled send **re-checks currency** and never ships a stale read as current. |
| **8b** | **Branding — Basic, or higher?** *(UPDATED — D148–D154)* | ⚠️ **Built at Basic** per D147 (`REPORT_BRANDING_TIER = 'basic'`) — **owner-open** | Branding sits at Basic alongside the extra sections and scheduling. Whether it belongs there or at a higher tier is **not settled**, and the build says so on the surface rather than asserting it. |
| **8c** | **`REP-*` capability rows for M4** *(NEW)* | ⬜ UNSET | `RELEASE_1_REPORTING_SPECIFICATION_V1` remains a **BLOCKING work item**. **M4 "Reporting & Analytics" is a named R1 milestone with ZERO capability rows.** D143 + **D145 + D148–D154** lock the **design**; the **spec** must still be commissioned, and reporting still has no capability rows to trace tests and observability events against. |
| **9** | **Reverse-trial duration (~14d)** *(NEW)* | ⚠️ REC — **GA-phase only; not live in Alpha** | The **mechanic** is ratified (§7e); the **duration** is not. Gated behind `PHASE==='ga'` per DL-102. |

---

## ⚠️ NEW CANON TENSIONS FOUND WHILE FOLDING IN DL-103 — **ESCALATED, NOT RESOLVED**

### **T10-8 (NEW) — DL-103 §7e still lists "priority" among the things a downgrade takes back, but §7c STRUCK the priority lever.** ⚠️

**§7e (binding condition):** *"On downgrade the user loses **leverage** — integrations, reports, **priority queue**, extra live plans."*
**§7c (same decision):** *"**WITHDRAWN** — an earlier draft of this clause made latency the primary lever… **It is struck.**"* And: *"**Artificial delay remains PROHIBITED in all cases.**"*

**These cannot both stand.** A downgrade cannot take back a lever that was never built.

**What the build did:** followed **§7c** (the later, explicitly-corrective clause). **`DOWNGRADE_TAKES_BACK` = integrations · reports · continuous auto-refresh · extra live plans.** **"Priority" is not in it, and no priority queue exists.** `_assertNoPriorityQueueLever()` fails loudly if one appears.
**Owner decision required:** strike the word *priority* from §7e's list (recommended — it is residue from the withdrawn draft), or re-open §7c.

### **T10-9 (NEW) — §1/§5 give Pro "+ speed/priority" as a differentiator, which §7c also strikes.** ⚠️

**§1:** *"**Pro's differentiator becomes execution & program support** (+ speed/priority)."* **§5:** *"**Pro** — execution & program support (**+ priority/speed**)."*
**§7c:** the latency lever is **struck**; *"an async product cannot sell speed"*; **artificial delay is prohibited**.

**What the build did:** Pro is rendered as **execution & programme support only** — *"it is not a better brain… it follows the work."* **No speed or priority claim appears on any tier card.**
**Owner decision required:** is there a *non-artificial* speed dimension at Pro (e.g. dedicated capacity / concurrency, which costs real money and is not fabricated latency)? If so it needs its own clause, because **as written it reads as the struck lever.** **The build does not invent one.**

### **T10-10 (NEW) — DL-103 retires UP-1/UP-2 and demotes UP-5, but the UP-* taxonomy is ratified canon.** ⚠️

MON-02/MON-03 and UP-1/UP-2/UP-5 are ratified rows in `12_freemium_tier_behavior_logic.md`. DL-103 §6 retires them **in a decision record**, but the **taxonomy document still carries them**, and the new prompts the build needs — **UP-APPLY** (assisted-apply cap) and **UP-REPORT** (strategic suite) — **have no canon UP-number at all**.

**What the build did:** deleted UP-1/UP-2/UP-5 from the prompt table (a prompt that merely *cannot fire* is a prompt somebody re-wires), and shipped **UP-APPLY / UP-REPORT** with an explicit **"no canon UP-number — escalated"** marker.
**Owner decision required:** re-issue the UP-* taxonomy against DL-103, and assign numbers.

### **T10-11 (NEW) — "Confidence = understanding maturity" now has a commercial surface, and that raises the stakes of any drift.** ⚠️ *(observation, not a conflict)*

DL-103 §7j puts OSLO's read **in front of the user's leadership, under the user's name**. Doctrine (confidence ≠ health/readiness/probability) was previously an internal-honesty constraint; it is now **a reputational-liability constraint for the user**. **Recommendation:** treat "a report that could be mistaken for a health rating" as a **P1 defect class** in QA, not a copy nit. The build asserts it at runtime (`_assertReportsNoHealthFraming()`), but **the specification does not yet say it is a defect.**

### **T10-12 (NEW) — DL-102 E is now internally stale.** ⚠️ *(bookkeeping)*

DL-102 constituent **E** adopts *"Daily fixes: Free 5 · Basic 20 (UP-1) · Daily chat: Free 20 (UP-2) · Deep runs/day: Free 2 (UP-5) — all ratified; adopted unchanged."* **DL-103 §6 retires all of them.** DL-103's *Supersedes* block says so, but **DL-102's own text still reads as current**. Recommendation: annotate DL-102 E in place.

*(Sections A–E below are the pre-DL-103 open items. Retained; superseded where they conflict.)*

## A. The 6 genuinely open decisions *(SUPERSEDED — pre-DL-103)*

See `tier-definitions-census.md` for the full table with citations and consuming surfaces.

| # | Decision | Status in the build | Why it is open |
|---|---|---|---|
| **1** | **Collaborator seats — Free / Basic / Pro** | ⚠️ **RECOMMENDATION** carried (Free 3 · Basic 10), rendered in-product as *"recommendation — not ratified"* | **THE ONLY UNDEFINED DIMENSION IN THE LADDER.** §4c sets every other row for every tier and sets **no seat row below Team** — where the price **is** per seat. **And Basic = 10 is commercially wrong:** a $12/mo Basic granting ten seats means a ten-person team buys **one Basic** instead of a ~$99–149/seat Team. **The build does NOT invent a replacement number.** CHG-061 is safe either way — Viewers are unlimited and Reviewers are free, and **neither consumes a seat**. |
| **2** | **CR-2 vs the binding governor** | ⚠️ **RECOMMENDATION** implemented and labelled: **record · defer · disclose** | Three ratified rules collide and canon never reconciled them — **CR-2** (evidence never metered, never refused) · **CRR-04** (every response triggers a run) · **§4c** (the monthly rollup gates AI spend). The build **records the evidence unconditionally** and **defers the run**, honestly. It is the only resolution where all three survive. |
| **3** | **OD-10 — the Deep-Pass coalescing window** | ⬜ **UNSET** | Coalescing is **on** and ratified (§4c); the **window** is not. **The highest-leverage number in the product:** it decides whether five fixes cost five Extended Analyses or one — a bigger cost lever than any cap, **and it costs the user nothing.** *Recommendation: settle/idle-based, single-active, plus the canonical manual trigger.* |
| **4** | **Free CRR cap** (B-1 cost ceiling) | ⬜ **UNSET** | D118 — mechanism canon, number not. Doctrine bounds it hard: virality **seeds on Free** (CHG-061) and evidence-seeking is **never bounded** (CR-2). It may gate **depth/volume**, never the **existence** of the loop — and **it must never fire an upgrade prompt.** |
| **5** | **MON-04 global upgrade-prompt cap / day** | ⬜ **UNSET** (the guard is enforced with a conservative prototype-local value, labelled as such) | MON-04 **requires** the guard; §4d's *"≤2/day, ≤1/session"* is **proposed** calibration config, never owner-ratified. Errs toward **silence** — the right direction of error for a prompt. |
| **6** | **Billing rail** | ⬜ **UNSET** (T-4) | Engineering. **The price is not the open question — it is $12/mo, ratified. The rail is.** It must carry DL-074 §5: **visible meter · user-set spend cap · threshold alerts.** |

---

## B. NEW canon tensions found while building — **escalated, not resolved**

> **AMENDED 2026-07-11.** T10-1 and T10-2 are **withdrawn / dissolved** against §4c. **T10-5 and T10-6 are new and are the sharp ones.**

### **T10-5 (NEW) — the seat caps are not canon, and Basic = 10 cannibalises Team.** ⚠️
`RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` sets **every** ladder row for **every** tier — and **no seat row for Free, Basic or Pro.** Seats appear in canon only at **Team/Enterprise**, where **the price is per seat** (~$99–149/seat/mo — §4c T4 / DL-074 §4).

The build's `SEAT_CAP = {free:3, basic:10}` came from **D129 X-1 / DL-102 E** — a product-grill **recommendation**, not an owner ratification — and the first Slice-10 build **marked it RATIFIED in code and in the census. It is not.**

> **A $12/mo Basic that grants ten collaborator seats means a ten-person team rationally buys ONE Basic instead of Team. That guts Tier 4.**

**Resolution costs nothing:** CHG-061 requires the viral primitives on Free, but those run on **unlimited Viewers** and **free, unmetered Reviewers (CR-2)** — **neither consumes a seat**. So seats can be tight across Free/Basic/Pro without breaching CHG-061.
**The build does NOT invent a replacement number.** It carries the recommendation, renders it as *"recommendation — not ratified"* in-product, and `_assertSeatCapsFlagged()` fails loudly if anyone re-marks it canon. **Owner decision required.**

### **T10-6 (NEW) — CR-2 vs the binding governor.** ⚠️
- **CR-2 / D126 (load-bearing):** evidence-seeking is **never metered**; a reviewer's answer is **never refused**.
- **CRR-04:** every reviewer response **triggers an Extended Analysis**.
- **§4c:** the monthly token rollup **"gates further AI spend — never silent overspend."**

**What happens when a reviewer's evidence arrives after the governor has gated?** **Canon has never said.**

**Recommendation (implemented, labelled in-product, NOT ratified): record the evidence · defer the run · disclose honestly.** The attestation lands immediately and unconditionally (CR-2 holds); the *run* defers — *"Priya's answer is recorded. Your read will update when your monthly analysis budget resets, or on upgrade."* Cost bounded, evidence never lost, product honest about what it has not done. **The only resolution in which all three ratified constraints survive. Owner decision required.**

### **T10-7 (NEW) — `RELEASE_1_TIER_DEFINITIONS_V1` is a *surface* problem, not a *decision* problem.**
The 18 product documents that cite it are not waiting on decisions — **they are waiting on a place to read the decisions that already exist.** Writing it as a *decision* document invites a second round of invented numbers. It must be written as a **consolidating, citing, product-authoritative surface** over `§4c` + `DL-074` + `BACKLOG_TIER_PROGRESSION` + the `UP-*` table, with **only the six open items above** left to decide. **Owner decision required: commission it that way.**

---

### ~~T10-1 — Two ratified sources disagree on Basic's project cap.~~ **WITHDRAWN 2026-07-11.**
**There is no canon conflict.** **§4c** (Tier 2, owner-confirmed 2026-06-05) says **3 active projects**, and **UP-3** says **3**. They agree. D129 T-1's "10" was **the product-grill's own AI-proposed number**, already withdrawn on the record (DL-102 Correction #3). *The original text is kept below for the history.*

#### ~~(superseded) T10-1 — Two ratified sources disagree on Basic's project cap. The build follows canon (3).~~
- **UP-3** (`12_freemium_tier_behavior_logic.md`, ratified): *"Free includes 1 active project — **Basic** gives you **3**."*
- **D129 T-1** (product-grill register, ratified by the owner): *"Basic = **10** projects."*

D134 resolves in canon's favour and the build ships **3**, cited. **But D129 T-1 still says 10 on the record.** `RELEASE_1_TIER_DEFINITIONS_V1` must state which governs, and if UP-3 stands, **D129 T-1 should be corrected on the record**. (The seat caps — Free 3 / Basic 10 — are a *different* number and are **not** in conflict. Only the *project* cap "10" is withdrawn.)

### ~~T10-2 — UP-5 presumes an affordance that D006 forbids.~~ **LARGELY DISSOLVES 2026-07-11.**
The Deep Pass spec **already lists a manual trigger**, and §4c ratifies that **coalescing is on**. With **OD-10** settled as settle/idle + the canonical manual trigger, UP-5 **has** a real affordance to gate, and D006 is not violated. *What is still worth confirming: which triggers the deep-run cap attaches to.* Original text kept below.

#### ~~(superseded) T10-2 — UP-5 presumes an affordance that D006 forbids.~~
UP-5's limit-reached table gates *"**Analyze / trigger reanalysis** (Project Overview)"*. **OSLO has no manual re-analyze control** — **D006 ratifies event-driven reanalysis only** ("no manual reanalyze"). So the deep-run cap has **no affordance of its own to gate**.

**What the build does (a recommendation, not an assumption):** it gates the **user-initiated events that trigger a run** (Apply this fix → the edit **still saves**, only the **re-read** defers, the read stays at last-good — which is exactly UP-5's ratified *"keep last analysis"* resolution), and it **never** gates an **evidence-driven** run (a reviewer responding — CR-2/D120/D126). A **clarification answer** is counted but **not gated**, because the user is *supplying evidence* and canon does not name it in the table.
**Owner decision required:** which triggers does the deep-run cap attach to?

### T10-3 — Two caps that D138 governs have no slot in the ratified UP-1…UP-8 taxonomy.
D138 says the rule applies to **every** cap. Two caps have **no UP-number in canon**:
- **Collaborator seats** (Free 3 / Basic 10) → built as **`UP-SEAT`**.
- **Export formats** (Free = PDF only) → built as **`UP-EXPORT`**.

Both follow the ratified standing rule exactly (specific limit + specific tier + resolutions, free one first). **The build did not assign them canon numbers.** **Owner decision required:** give them taxonomy slots, or state that D138's rule applies without one.

### T10-4 — The global per-day prompt cap is a canon guard with no canon number.
MON-04's global guards **require** "a global per-day cap". The value is Calibration §4d config and was never set. The build **enforces the guard** (with a conservative prototype-local value, labelled as such at every site) and **renders the product value unset**. It errs toward **silence** — the right direction of error for a prompt: too few is a missed sale; too many is the product nagging a user who trusted it. **Owner decision required:** set the number, or ratify "err toward silence" as the rule.

---

## C. Carried forward, still open (from Slice 9 / D129–D132)
- **Configurable link expiry for Basic** — **CLOSED, NOT BUILT** (D128 P2: never sell safety). Recorded here so nobody re-opens it by accident.
- **Whether revenue ever expands onboarding capacity** — would re-open CR-7 (pay-to-skip). Not modelled.
- **D130 stands:** every ratified number here is an **instrumented hypothesis**, chosen to be **easy to loosen and painful to tighten**. They must be revisited against real alpha behaviour — including the ones this slice adopted from canon.

---

## D. What this slice deliberately did NOT do
- It did **not** propose a single number. Not one. **That is the deliverable.** *(Amended: it now **adopts** 46 ratified numbers, each cited at the site that consumes it — and still proposes none.)*
- It did **not** resolve T10-1…T10-7. They route through **Framework 001** (Backlog → Proposal → Review → Decision).
- It did **not** build a billing rail (T-4), and it says so at every upgrade touchpoint.
- **AMENDED — it did not invent a seat number** to replace the commercially-wrong Basic = 10. It flagged it and escalated.
- **AMENDED — it did not build a Free purchase path**, and `_assertNoFreePurchasePath()` fails loudly if anyone ever does (DL-074 §3).

---

## E. The lesson on the record (2026-07-11)

**Three times in this engagement, an AI pass reasoned from its own model where canon had already spoken:**

1. **"Basic = 10 projects"** — canon says **3**. Reached an open PR. Withdrawn (DL-102 Correction #3).
2. **"Basic's price / chat / deep-runs / envelope / monthly gate are all owner-TBD"** — **all five were ratified**, in `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c`, owner-confirmed **2026-06-05**.
3. **"Pro/Team is the org sale; Basic + Pro is not"** — corrected by the owner, 2026-07-11: **Basic + Pro = the individual motion; Team + Enterprise = the org sale.**

**The scan was the failure, not canon.** The product-grill discipline scopes to `10_product/` + `00_owner/` — and **the tier ladder lives in `30_engineering/`.** Two consequences, both now built in:

- **The build asserts in both directions.** `_assertNoFabricatedNumbers()` fails on an invented number **and** on a **ratified number rendered as unset**. *Crying "unset" over a decided value is the same lie, told backwards — and it is more corrosive, because it teaches every future reader that the number does not exist.*
- **A hole you cannot find is worse than a hole you can.** The fix is a **product-authoritative surface**, not a better guess. That is **T10-7**.

---

# ⬛ OPEN ITEMS RAISED BY THE REPORTING REBUILD (D148–D154, 2026-07-12)

| # | Item | Status | Why it is open — and why the build did NOT close it |
|---|---|---|---|
| **R-1** | **The UP-number for the persistence prompt** | ⬜ **UNSET — ESCALATED** | D154 makes the gate **reuse, not edit**, so the prompt now sells **persistence of the PM's wording**. **No `UP-*` in canon covers that.** The build reuses the `UP-REPORT` key and **flags it on the surface**. Naming a canonical prompt is not the build's to do. |
| **R-2** | **Does OSLO ever comment on the PM's OWN wording?** *(NEW TENSION — escalated, not invented)* | ⬜ **OWNER-OPEN** | D149's vocabulary guard and D151's forecast guard **exempt sections the PM has rewritten** (`data-pm="1"`) — because policing the user's prose would be **the tool writing the report again**, which D152 forbids. **But:** a PM could type *"we're 80% likely to hit 450"* into their own summary, and it would go out **under OSLO's mark, on OSLO's cover**. Two defensible answers, and **the build refuses to pick**: (a) **stay silent** — advisory-only, their words, their name; (b) offer a **gentle, non-blocking note** — *"that reads as a prediction; OSLO does not make those"* — which is advisory rather than a gate. ⚠️ **This is the sharpest new tension in the rebuild.** |
| **R-3** | **Does the "To:" line count as tailoring?** | ⚠️ **Built as a header, flagged** | D145 fixes §1–§5 for every recipient and lets **§6** be addressed. The memo also carries a normal memo **`To:` line** in its header. It is **addressing, not re-framing** — no assessment varies — and the guard is **section-scoped** on purpose. Owner may strike it; the build will not assume. |
| **R-4** | **The seven-section memo is one page. What happens on a plan five times this size?** | ⬜ **UNSET** | Risks are capped at **5** and the appendix walks every workstream. On a large plan the appendix grows without bound while the summary stays fixed. **Selection is the value** — but *what gets cut, and who decides*, is a spec question. The build does not invent a truncation rule. |
| **R-5** | **`REP-*` capability rows / observability events for the readout** | ⬜ **UNSET — BLOCKING** | Unchanged, and now larger: the rebuild adds **edit · persist · re-seed · package** as real user actions with **no capability rows, no tests and no observability events** to trace them against. |

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157 · D158** (owner: accepted)

## Closed by this pass

| Was open | Closed by | Resolution |
|---|---|---|
| *Should OSLO offer a gentle, non-blocking note when the PM's **own** wording reads as a forecast?* (escalated at the D148–D154 rebuild) | **D155** | **Yes — and it is guarded.** OSLO surfaces an unobtrusive advisory beside the PM's section. **It never blocks · it never edits · it is always dismissible.** *Blocking would be the tool overruling the human (advisory-only, D001); silence would be OSLO lending its name to a claim it forbids itself. The note is the only honest position.* Guards: `_assertForecastNoteNeverBlocks()` · `_assertOsloNeverRewritesPMProse()`. |
| *Does the `To:` line breach D145?* | **D156** | **No. It stays.** D145 forbids **re-framing the assessment** by audience, not **addressing** the document. The guard stays **section-scoped** (§1–§4 + §5 + appendix byte-identical; only §6 varies). Recorded in code so nobody "fixes" it. |
| *`_assertNoGenericUpgradeCopy()` red console on Basic* | **D158** | **Defect fixed.** The guard demanded the relieving tier's name unconditionally; **UP-6 only names "Basic" in its Free branch** (correctly). MON-04 requires the name of the tier that **relieves** the limit — meaningful **only when the user is beneath it**. `_beneathTier()` now gates the requirement. **A fix to the guard, not a relaxation of MON-04.** |

## ⬜ STILL OPEN — the M4 (Reporting) specification. **Owner / spec decisions. THE BUILD DECIDES NONE OF THEM.**

| # | Open item | Status | Why it is not invented here |
|---|---|---|---|
| **M4-O1** *(a.k.a. **R-O1**)* | **The NAME of the artifact.** | 🟨 **PARTIALLY CLOSED — D168 §4 + D172d (2026-07-12)** | **CLOSED by D168:** the **living document inside OSLO is a REPORT**; the **dated snapshot that has left OSLO is a MEMO**. <br>**CLOSED by D172d:** the **WORKSPACE is "Reports"**; the **DOCUMENT inside it is the "Readout."** Binding in nav, crumb, tooltip, toolbar, History and toasts, and guarded (`_assertReportsHostsOneReportType()` + `_assertReportAndMemoAreNotConfused()`). **Never call the workspace a Readout; never call the document Reports; never call the live document a memo; never call the sent artifact a report.** <br>**STILL OPEN (the remainder):** the **glossary-tier ratification of these names** in canon (**DL-053**) — the build now uses them consistently but does not *ratify* them. **"Status report" remains banned by design** (`REPORT_BANNED_NAMES`), as does any name implying health or readiness (DL-104 §5). |
| **M4-O2** | **Scheduling — R1 or a fast-follow?** | ⬜ **OWNER-OPEN** | Built and **flagged**: `SCHEDULING_R1 = null`. A weekly readout is the PM's recurring obligation and automating it is the labour half of the lever — but whether it lands in R1 is a scope call, not a design one. |
| **M4-O3** | **Branding — Basic, or a higher tier?** | ⬜ **OWNER-OPEN** | Built at Basic and **flagged**: `REPORT_BRANDING_TIER = 'basic'`, marked unsettled on the surface. |
| **M4-O4** | ⚠️ **REPORT LENGTH — what gets CUT when it runs long, and WHO DECIDES.** (**D157**) | ⬜ **M4 SPEC ITEM — NOT INVENTED** | The build renders **5 risks, highest impact first** (`MEMO_RISK_CAP = 5`, **explicitly labelled illustrative, NOT a ratified product value**) plus a **full, explicitly skippable appendix** that walks **every** workstream — so **nothing is hidden**, it is simply not in the sponsor's five. **But the truncation RULE — OSLO's ranking? the PM's pick? a hard cap? a "show more"? — is a specification decision, and inventing one is exactly how "Basic = 10 projects" happened.** *Selection is the value; the cut is spec'd, not invented.* |
| **M4-O5** | **The UP-number for the PERSISTENCE prompt** (the Free → Basic prompt that sells *"your edits come back"*). | ⬜ **NO CANON SLOT EXISTS** | **No UP-\* in the ratified MON-04 taxonomy (UP-1…UP-8) covers reporting persistence.** Built as `UP-REPORT`; the taxonomy slot is the owner's to assign. Same class of gap as **T10-3** (`UP-SEAT` / `UP-EXPORT`). |
| **M4-O6** | Does reporting get its **own capability rows** in the traceability matrix? | ⬜ **OWNER-OPEN** | M4 "Reporting & Analytics" is a named R1 milestone with **zero capability rows and no specification**. D148–D158 lock the **design**; the **spec must still be commissioned**. |

> **The standing rule, restated:** an owner-decision-required value **renders visibly unset** and is **never** filled in with a plausible guess. `_assertNoFabricatedNumbers()` fails the build if one ever carries a number.

---

# D159 / D160 / D161 — open items (2026-07-12)

## O-D159-1 — **The Tier Definitions findability problem is NOT solved by the toggle. ESCALATED.**
**D136** put the tier-definitions census **in the product** precisely so the numbers would be **findable** — the diagnosis being that *"a product-scoped reader (a person, or a model) never finds them, and a model that cannot find a number invents one."* That failure has already happened **twice** (`Basic = 10 projects` against ratified canon that says **3**; *"Basic's price is undecided"* when it is **$12/mo, owner-confirmed**).

**D159/D161 move that census out of product copy and behind the toggle.** That is the right call for the *product* — a user does not need our ratification statuses — but it **does not fix the underlying gap**, and it must not be mistaken for a fix.

> **The findability problem is solved by writing the `RELEASE_1_TIER_DEFINITIONS` specification** — the document eighteen canonical files already cite and which **has never been written**. **The escalation stands.** The census is preserved in full behind the toggle so nothing is lost, but **the spec is still owed.**

## O-D159-2 — **Owner-visible tension: "say it out loud" vs. "labelled in-product".**
Several earlier decisions instructed the build to carry a label **to the user**: the seat cap *"labelled as a recommendation in-product"* (D129/DL-102 E), the report artifact flagged *"naming pending"* (D147/DL-053), the reverse trial *"NOT live in Alpha"* stated on the Plans page. **D159/D161 supersede all of these for user-visible copy** — the brief's zero-hit grep list names `"not ratified"` and `"naming pending"` explicitly.

**Recorded, not resolved by the build.** In every case the **behaviour** is unchanged (the seat cap is still held as a RECOMMENDATION in config and never sold on; the artifact still avoids "status report" and any health/readiness framing; the reverse trial is still not live and not simulated). Only the **words shown to the user** moved. **If the owner intended any of those labels to remain user-visible, say so and they come back.**

## O-D159-3 — Reporting (M4) open items — unchanged, now behind the toggle
The M4 spec is still owed, and the build still decides none of it: **the NAME** of the artifact (glossary / DL-053) · whether **scheduling** is R1 or a fast-follow · whether **branding** belongs at Basic or higher · whether reporting gets its own **capability rows** · the **UP-number for the persistence prompt** (no UP-* in canon covers it) · **report length — what gets cut when it runs long, and who decides** (the build shows 5 risks + a skippable appendix; **the truncation rule is NOT invented here** — D157).

## O-D159-4 — The `UP-APPLY` and `UP-REPORT` taxonomy slots
Still **escalated, not invented**: canon has assigned **no UP-number** to either the assisted-apply prompt or the report-persistence prompt. D138 requires the *behaviour* at every cap, so both are implemented; their taxonomy slot remains an owner decision.

---

# D162 — open items raised by the Issue Panel disclosure pass (2026-07-12)

| # | Item | Why it is open | Disposition |
|---|---|---|---|
| **O-D162-1** | **Primary-action precedence when an issue has BOTH a recommendation and an open clarification.** | D162b names the rule *"Apply this fix if there is a recommendation; Answer if OSLO is asking for a clarification"* — in that order. **Every seeded issue has a recommendation**, so in practice **"Answer" never becomes the primary action** and the clarification is reachable only through its row (which is where the D162c fix wants it: collapsed, named, one click). Built to the letter of the rule. **If the owner intended the clarification to WIN the primary slot when OSLO is blocked on the user, it is a one-line change** — say so. | **Escalated, not invented.** |
| **O-D162-2** | **The recommendation TEXT is now one click away, not resident.** | D162b lists *"Recommendations"* among the rows that collapse, and names *"Apply this fix"* as the primary action — so the user can apply a fix whose text is behind a chevron. That is the owner's instruction and it is built exactly. **The tension:** the user's own stated intent is *"what's wrong, **and what do I do about it?"* — an argument that OSLO's recommended sentence belongs in the always-visible layer, next to the button. **Not decided unilaterally.** | **Owner call.** Cheap either way. |
| **O-D162-3** | **"Share for review →" removed from the artifact flyout.** | D162d says cascade the disclosure model to the flyout. A hover popover cannot carry collapsible rows, so the cascade reduces it to *the read + the actions that belong in a peek*. Share fired a full modal out of a hover; it survives (enabled, unmetered) in the panel one click away. **CR-2 is untouched.** If the owner wants it back in the flyout, it returns in one line. | **Flagged.** |
| **O-D162-4** | **The share dialog (CRR modal) has NOT had a full D162 pass.** | D162d names the **Recommendation panel** and the **artifact flyout**. The obvious D162c copy was removed from the share dialog too (prime-candidate hint, CR-2 counter), but the dialog still carries longer explanatory blocks (*"what their answer will and will not do"*, the reviewer-grant explanation, the token-budget note). **Some of it is genuinely load-bearing at the moment of choosing a person** (a new reviewer needs to know a grant costs them nothing). **Not swept without direction — a copy cut there could quietly become a CR-2 honesty cut.** | **Escalated.** |
| **O-D162-5** | **Row counts are unlabelled numbers** (*Evidence · 2*, *Recommendations · 3*). | Matches the owner's sketch exactly. "Recommendations · 3" = OSLO's recommendation **plus** the 2 other options. *(D190c: that row is now DELETED — the options live under the recommendation.)* If the owner reads "3" as "3 alternatives", the label needs a word. | **Watch.** |

---

# D163 + D164 — open items (2026-07-12)

| # | Item | Why it is open | Disposition |
|---|---|---|---|
| **O-D163-1** | **The ≤60 "modal body" budget cannot be applied to a surface that is a TABLE OF ROWS.** | The **Plans** page is five tier cards with ~13 feature rows each; **Usage & Limits** is nine meter rows; **Settings** is twelve sections of labelled rows; **Access & invites** is four blocks. Their *totals* are 323 / 110 / 719 / 307 words — and **no honest pricing page or settings screen can be 60 words.** So the budget was applied structurally: **prose (narrative body copy) ≤60** and **every row/label ≤8, every helper note ≤20**. Both hold everywhere (Plans prose **59**, Limits prose **60**, every Settings row inside budget). **This is an interpretation, not an invention — and the owner should confirm it.** | **Escalated.** State the rule for row-based surfaces. |
| **O-D163-2** | **Where the ≤30 prompt budget is measured.** | The owner's own model rewrite counts **the lead line + the body + the one honest label + the buttons ≈ 27 words** and shows no eyebrow chip. This build measures **title + body + label + resolution buttons ≤30**, and holds the **"Limit — \<x\>" eyebrow** (which is how MON-04's *"name the limit hit"* is satisfied) to the **≤8 label budget** separately. Every prompt is inside both. **If the owner intends the eyebrow inside the 30, four prompts need ~3 words trimmed.** | **Escalated.** One-line change either way. |
| **O-D163-3** | **The export disclaimer is 34 words and is RATIFIED CANON, verbatim.** | *"This reflects OSLO's understanding maturity … not a measure of project health, readiness, or probability of success."* The Export & Share-Out spec **requires every package to carry an explicit disclaimer**, and `_assertDisclaimerOnPackageNotInBody()` reads this exact string. **It is exempt from the word budget, and it must be** — a copy cut here is a canon change. | **Flagged, not cut.** |
| **O-D163-4** | **The demo bar and its toasts are prototype scaffolding, but they are on-screen product surfaces.** | They were swept to ≤12 words like every other toast. **They arguably belong behind the prototype-notes toggle entirely** (D161), which would remove them from the product read completely. **Not done unilaterally** — it changes what a reviewer can reach in one click. | **Owner call.** |
| **O-D164-1** | ~~Table controls in the readout~~ — **CLOSED (2026-07-12).** | The old disposition conflated two things. **Table STRUCTURE is editor capability; table PROVENANCE is artifact semantics.** Adding a row to the §6 decisions table is **editing**, not asserting a plan fact — so `attachTableControls()` is now **shared** (row add/insert/delete, column ops, row drag-reorder all work in the readout). The **row provenance dot** and the **cell reveal chip** stay artifact-only (`_ensureCellReveal`), because those *would* put OSLO vocabulary into a document that forbids it (D149). | **CLOSED.** |
| **O-D164-2** | ~~Undo/redo is per SECTION~~ — **CLOSED (2026-07-12).** | It was per-section because the *editor* was per-section. The readout is now **one document**, so it has **one undo stack** (`_edKey()` returns `'rpt'`). Undo reaches across the whole memo, which is what a PM expects of a document. The stack resets on a full re-render, exactly as an artifact's resets on open. | **CLOSED.** |
| **O-D164-3** | ~~The readout editor has no autosave~~ — **CLOSED (2026-07-12).** | It had no autosave because it had a **Save button**, and the Save button existed because it had an **edit mode**. All three are gone. The readout now **autosaves on a debounced commit** (`_rptCommit()`, ~900ms idle, plus on blur) — and it is **provably free of `commitArtEdit()`**: `_commitFromStructuralEdit()` returns early on the readout host, and `_assertReadoutEditorProducesNothing()` reads its source. **Autosave runs NO analysis.** A transient *"Saved"* / *"Saved · not kept next week"* confirmation appears in the toolbar (fixed slot, opacity only — no reflow). | **CLOSED.** |
| **O-D164-4** | **`_rptCleanHTML()` strips editor chrome on commit.** | It removes block grips, table controls, zero-width caret spaces, `contenteditable`/`draggable` attributes, event handlers and any provenance chrome; it **unwraps** find highlights (never removes them — they wrap the PM's own words). **It removes nodes OSLO put there; it touches nothing the PM typed** — and `_assertOsloNeverRewritesPMProse()` now proves the stored text and the rendered body are **byte-equal**. It is also the **normaliser both sides of the divergence test go through**, so "changed" can never mean "re-serialised". **It is a sanitiser, not a rewriter.** Still called out because *"OSLO touching the PM's markup at all"* is the class of thing D152/D155 forbid, and it deserves an owner's eye. | **Flagged (unchanged).** |
| **O-D164-5** | **The section HEADINGS are not editable.** | The `<h2>` of each section is `contenteditable="false"` — **document furniture**, exactly as an artifact's `<h1>` lives *outside* `#artdoc`. Two reasons: (a) D150 fixes the seven sections and their order, and the guard reads `data-sec`; (b) one heading carries a **live date** (*"What's changed since 5 July"*) which, if stored as the PM's text, would freeze at last week's date and quietly lie. **This is the one place "click anywhere and type" does not literally hold**, and it is a deliberate parity with the artifact editor, not an oversight. **Owner's eye requested.** | **Escalated, not invented.** |
| **O-D164-6** | **A block cannot be dragged ACROSS sections.** | The block model is scoped to the nearest `[data-sec]` container: a paragraph reorders **within** its section. Crossing sections would (a) break D150's fixed order and (b) move OSLO's prose into the PM's section — or the reverse — **corrupting the authorship boundary the whole D149/D152/D155 exemption model rests on.** An artifact has no such boundary, which is why its blocks move freely. **Called out because it is a real difference between the two documents**, arrived at from the doctrine rather than from convenience. | **Flagged.** |
| **O-D168-1** | **The MEMO's reading measure is `64ch` — a build choice, not a ratified number.** | The **report** measure is *derived* (`.report` max-width **=== `.doc`**, guarded, so it can never drift from the artifact). The **memo** is a different object and needs its own reading measure — but **no canon sets one.** `64ch` is a typographic judgment (a comfortable memo column), and it is **flagged, not asserted**. **The build does not name canon.** | **Escalated.** Owner may set it, or leave it a design choice. |
| ~~**O-D168-2**~~ | ~~**Where a memo lives after it is sent.**~~ | ✅ **CLOSED — D169 (owner: approved, 2026-07-12).** A **"memo sent"** History event now **opens the memo**: the exact bytes that travelled, with its cover, disclaimer and currency marker. **Read-only, always** — opening changes nothing and **runs no analysis**. **The memo is shown AS IT WAS SENT — never re-rendered from current understanding**, because re-rendering it would silently rewrite history. `openMemoFromHistory()` selects the frozen entry out of `REPORT_SNAPSHOTS[]` by id and **cannot reach the live composer**. | **CLOSED.** Guards: `_assertHistoryOpensTheFrozenMemo()` (mechanism) + **`_d169StateProof()`** (state) + 5 negative controls + a control **on the proof itself**. |
| **O-D168-3** | **A memo is frozen in memory, not on disk.** | `REPORT_SNAPSHOTS[]` is session state, like every other register in this prototype. In the product a memo is a **real artifact** (a PDF, a hosted export link) and immutability is a **storage property**, not a `Object.freeze`. The prototype proves the **contract** (cut · edit · re-analyse · byte-identical); **the product must prove the storage.** | **Flagged for engineering.** The contract is the deliverable; the persistence is not. |


---

# D165 — open items — **ALL FOUR CLOSED by D167 (owner: approved, 2026-07-12)**

> The four O-D165 items were escalated, not invented. **The owner ruled on all four.** They are recorded here with
> the ruling and what was built, because the *reasoning* is the durable part.

## O-D165-1 — **The opening turn drops the clarification form. Is a CHIP enough?** — ✅ **CLOSED: NO.**
**The ruling (D167):** *"A chip is enough surfacing for **detail**. But a question OSLO needs answered is not detail —
it is a **REQUEST**."* Hiding a request one click deep means **a blocked issue can sit unanswered because the ask was
never seen.**
**What is now built:** the opening turn carries a **one-line collapsed prompt** naming what OSLO needs (the question,
truncated to 10 words — the full text is the first thing inside, one click away). It expands to the input on click
(D162c/D165e). **The "Answer your question" chip remains, as a shortcut — not as the only door.** The textarea is
**not** re-opened: collapsed is still the decision; *visible* is the other half of it.
**Guarded by:** `chatOpeningCarriesAsk` (it is THERE) **paired with** `chatClarCollapsed` (it is CLOSED). *Neither
alone is the decision* — delete the block and the first bites; open the textarea and the second bites.

## O-D165-2 — **The opening turn carries ONE action.** — ✅ **CLOSED: confirmed as built.**
**The ruling (D167):** the opening carries **ONE action** (*Open this issue →*), consistent with D162b. No change.
**Guarded by:** `chatOpeningShort` (`≤1` action card; `.ca-cons` subtitles banned).

## O-D165-3 — **D163 has no row for a chat turn.** — ✅ **CLOSED: D163 gains chat word budgets.**
**The ruling (D167):**

| Surface | Budget |
|---|---|
| **Chat — opening turn** | **≤ 50** |
| **Chat — pull turn** (evidence · options · recommendation · reliability) | **≤ 40** |

**What is now built:** `CHAT_OPENING_WORD_BUDGET = 50` (was 55) and a **new** `CHAT_PULL_WORD_BUDGET = 40`, each with
its own guard, each with a negative control. **Measured:** openings **27–45** (max ISS-02 = 45) · pull turns **20–36**.
**Guarded by:** `chatOpeningShort` · `chatPullShort`.

> ⚠️ **ONE INTERPRETATION, DECLARED — not invented.** D167's table names four pull turns (evidence · options ·
> recommendation · reliability). The **Slice-10 tier answers** (*"What does Basic add?"* · *"What's never limited?"* ·
> *"Which limit did I hit?"* · *"What does my plan include?"*) are pull turns **by the same mechanism** — they arrive
> only when asked — so the build holds them to the **same 40-word budget**. All four already fit (21–36). This is the
> **named budget applied to the same class of turn**, not a new budget invented. **If the owner intends the 40-word
> budget to bind only the four named turns, remove them from `CHAT_PULL_TURNS` — one line.**
>
> ⚠️ **One copy change fell out of it.** *"What does Basic add?"* measured **43**. The overrun was its second
> sentence — *"I run the same models for everyone."* — which **restates the line before it** and **explains why we do
> something**: both **banned outright by D163**. Cut, not re-worded. The claim (*"No plan gives you a better read"*)
> stands, once. **36 words.**

## O-D165-4 — **The prototype-notes block renders BELOW the handoff chips.** — ✅ **CLOSED: moved above.**
**The ruling (D167):** cosmetic — move it above them.
**What is now built:** in both tier answers `pn(...)` now emits **before** `_hand(...)`. **The handoff is the last
thing in a turn** — it is what carries the conversation forward, and a governance rail wedged between the answer and
its next moves buries them. Verified with notes **ON**: `chat-acts → pn → chat-follow`.

---

# D170 / D171 — OPEN ITEMS RAISED BY THIS BUILD

## O-D170-1 — ⛔ **Does the ratified MON-04 per-day prompt cap apply to LIMIT-HIT DISCLOSURES, or only to unsolicited nudges?**
**This is the seam the P1 fell through, and the build has taken a position. It needs the owner's.**

MON-04 ratifies a **global per-day prompt cap** (its *value* is unset — Calibration §4d — and renders unset). The build
enforced it, and the per-trigger cooldowns (`UP-EXPORT` = once/day · `UP-REPORT` = once/day · `UP-6` = once/month),
**against every prompt**. But **the friction prompts are not nudges** — they are the product's **answer to a click the
user made and the product refused**. Suppressing one leaves a **live button that does nothing at all** (D170).

**What is now built, and the reasoning:**
> **A cadence cap governs what the PRODUCT INITIATES. It may never silence the product's ANSWER to a click the user
> made and the product refused.** So the caps apply to `cls:'value'` (UP-7, UP-8 — the product starts it) and **not**
> to `cls:'friction'` (the user hit a limit). The distinction is **derived from the ratified table**, never hand-flagged
> at the call site — a call site that forgets a flag is exactly how this comes back.

D170 directs *"every `fireUP(...)` path must render its prompt"* and *"a gated attempt that produces no visible outcome
is a P1 defect"*, which settles the behaviour. **What is NOT settled is the taxonomy**: does canon regard a limit-hit
disclosure as a "prompt" for the purposes of the MON-04 cap at all? **The build says no, and says so out loud here.**
⛔ **If the owner rules that the cap DOES cover limit disclosures, the only canon-compatible design is the deferral
path** (below) — never silence.

## O-D170-2 — GUARD 1 (never before first value) and GUARD 2 (never mid-pass) vs. D170. **Resolved by DEFERRAL — confirm.**
Both are **ratified and explicitly non-overridable**, and both are *right*: do not sell before you have delivered; do not
interrupt the one thing the user is waiting for. **But neither reason survives contact with *silence*.**

**What is now built:** a gated attempt caught by either guard is **DEFERRED, never dropped** — queued and fired at the
first legal moment — and the user is told **immediately** which limit they hit (a toast, ≤12 words, **no upgrade CTA**).
Canon is honoured (no prompt mid-pass, none before first value) **and** the attempt has a consequence.
**Confirm the deferral is the intended reconciliation.**

## O-D171-1 — ⬜ **A SEND has no UP-number, and should not need one.**
Canon assigns no UP-* to sharing. **It does not need one: there is no limit to hit** — sharing is free on every tier
(CHG-061). Recorded so it is not mistaken for an omission. **Nothing was invented.**

## O-D171-2 — ✅ **CLOSED by D172a/D172b (owner, 2026-07-12).**
*Is a SCHEDULED readout an automated SHARE or an automated EXPORT?*
**It is an automated SHARE.** *Nobody schedules a PDF onto their own disk* — a schedule means *"send my sponsor the
readout every Friday,"* and that goes **to people**. Built as `sent_via:'shared'`, with a **scoped read-only grant** for
the recipient (D172c), a **sent** History event that **opens the frozen memo** (D169), and the **D147 currency re-check**
still binding at send time.
**The apparent collision is resolved by D172b:** **the SHARE is free; the AUTOMATION is Basic.** Sharing is guaranteed on
Free as a **viral primitive** (CHG-061); **cron is not a viral primitive.** What Basic sells is **not having to
remember** — the same shape as D154 (*editing free; persistence gated*). **Meter the labour, never the understanding.**

## O-D171-3 — ⬜ **The in-app notification a share raises is out of this slice's scope.**
D171 §1 describes *"an in-app notification + a link that routes into OSLO."* The **memo, the freeze, the History event,
the read-only recipient view and the "previous analysis" relabel** are built. The **notification surface itself** belongs
to Slice 8's awareness/notifications work and is **not invented here**.

## O-D170-3 — ⬜ **`PROMPT_GLOBAL_CAP_PER_DAY` is still UNSET (Calibration §4d).**
Unchanged, and still owed. It now governs **only** the value prompts (UP-7 / UP-8), which narrows what the number has to
do — but it is still an owner value and still renders unset. The prototype's local `_PROTOTYPE_PROMPT_GUARD = 3` is a
demonstrable mechanism, **not a product value**, and is labelled as such.

---

# D172 — OPEN ITEMS RAISED BY THIS BUILD

## O-D172-1 — ⬜ **The scheduling CADENCE is a build placement, not a ratified value.**
The build ships **one** cadence — **weekly** (`RPT_SCHED.cadence = 'weekly'`) — because *"every Friday"* is the shape the
decision itself uses. **Whether the product offers other cadences (daily / fortnightly / monthly / on-change), and whether
the choice is itself tiered, is not settled and is NOT invented here.** `SCHEDULING_R1 = null` still stands (M4-O2).

## O-D172-2 — ⬜ **The scheduled share cannot be "paused" — and a stale plan does not stop it.**
D147 says a scheduled share **labels** a stale read; it does not say the schedule should **stop**. The build therefore
**keeps sending, honestly labelled**, on the reasoning that a sponsor's Friday note going silent is itself a signal the PM
did not choose to send. ⛔ **But "the schedule keeps firing while the analysis is stale" is an owner call, not a build
call.** Recorded, not assumed.

## O-D172-3 — ⬜ **The memo-grant LIFETIME is inherited, not ratified.**
CR-6 ratifies **two** lifetimes: a **snapshot link = 30 days**, a **review grant = until the issue resolves, or 14 days**.
A **shared memo** is neither — it is scoped to *one dated memo*, which has no "resolution" event. The build gives it the
**30-day snapshot lifetime** (revocable, D117) as the nearest ratified neighbour, and **flags it**. ⛔ **The number is the
owner's.** *(A memo arguably never goes stale — it is a dated fact — which is an argument for no expiry at all. Not
assumed.)*

## O-D172-4 — ⬜ **The recipient's NOTIFICATION is still out of scope (unchanged from O-D171-3).**
The memo, the freeze, the grant, the link, the History event and the read-only recipient view are built. **The in-app
notification the share raises** belongs to Slice 8's awareness work and is **not invented here.**

---

## WI-R1 — ✅ **Strategic Readout composer folded into the Reports/export surface (2026-07-12).**

Realizes **DL-107** (five-section spine) + **DL-108** (tailor the ask, never the read) + **DL-104** (P1 guards),
folded into the existing export/snapshot modal (`#exportScrim`). Seven-section editable Readout document
(`#rptDoc`, D148–D172) **untouched**. Two boot guards added: `readIdenticalAcrossAudience` · `readoutRunsNoAnalysis`.
Boot self-check **58 → 60, all green; 0 page errors** (Playwright/Chromium headless). Slice-10's own data model,
theme and boot-guard pattern were used; v4 was **not** imported.

**Confirmed OUT of scope / not built (guardrails honored):** cognitive-event / Understanding-Debt feed (R2-F/AE-06);
assumption validated/invalidated lifecycle (RB-017 — the "Unvalidated assumptions" optional section is
presentation-only); cross-project pattern call-outs (R2-E); Uncertainty/Trade-off first-class objects (foreclosed);
audience-reframed *reads* (forbidden by DL-108).

### Open items carried forward (owner decisions, not settled by this build)
- **O-WIR1-1 — ⬜ Report NAME is owner/glossary (DL-053).** The surface is labelled descriptively ("Strategic
  readout — the five-section read · naming pending"). The final name is not set by this build.
- **O-WIR1-2 — ✅ RESOLVED by WI-R2 (2026-07-13) — §4 audience taxonomy UNIFIED.** The composer no longer carries a
  separate axis: it now keys §4 on the workspace Readout's own **`REPORT_RECIPIENTS`** (Sponsor / Programme lead /
  Operations / Executive-board). **"Practitioner" was dropped** — it is the PM's own view, not a memo recipient.
  ONE audience model is now shared across the composer (`#sroDoc`) and the memo (`#rptDoc`); the two SURFACES stay
  distinct (the composer keeps OSLO's register and renders §4 itself — never via `_memoDecisions()`). DL-108
  invariance re-proven across all four recipients. See `worker-reports/WI-R2-audience-convergence.md`.
- **O-WIR1-3 — ⬜ §4 asks are curated demo strings.** They are grounded in the live open issues but are not
  generated from a decision model; the real "who owns which decision" mapping is an M4 spec item.
- **O-WIR1-4 — ⬜ Reopen re-signoff.** WI-R1 reopened the signed-off Reports surface; the Reports portion of
  Slice 10 needs owner re-signoff (per the WI-R1 record).

---

## D173 — THE PAYOFF: open items (owner decisions, not settled by this build)

- **⬜ O-D173-1 — THE 0–100 INDEX: CALIBRATE OR DEMOTE. OWNER-OPEN.**
  **DL-062 F1 (numeric calibration) is Open-TBD — the index is NOT CALIBRATED.** OSLO cannot defend **62** against
  **63**. This build ships the owner's **recommendation** (D173d): **DEMOTED** to a secondary aggregate, **no delta,
  ever**, and the **band transition carries the change**. It is **demoted, not deleted** — the day the owner
  calibrates it, `.bandhero` and `.idx` swap sizes and the number gets its hero slot back, with its delta. The flag
  lives in the **prototype-notes layer** (D161, `PN_SLOTS.pnPayoff`), **never in product copy**. **The decision is
  the owner's and remains open.**

- **⬜ O-D173-2 — "DEPENDENCIES CONFIRMED" IS NOT BUILT, BECAUSE IT CANNOT BE COUNTED.**
  D173b names the row *"Dependencies confirmed 5 of 8 → 6 of 8"*. **The model holds no dependency register**:
  `REVIEWS` is a list of *review requests* (awaiting / responded), not a set of dependencies with a
  confirmed/unconfirmed state. Counting it would mean **inventing** it. **The row is OMITTED and escalated**
  (Anti-Assumption Build Protocol). If the owner wants it, the ask is a **dependency register** — an object with
  identity and a confirmed state — and the row is then **one entry** in `PAYOFF_COUNTS`.

- **⬜ O-D173-3 — "Unvalidated assumptions" is rendered as *Open questions*.**
  D173b's example row is *"Unvalidated assumptions: 5 → 4"*. What the model actually holds is **open clarifications**
  (`_openClarIds()` — issues carrying an unanswered question). An **assumption** with a validated/invalidated
  lifecycle is **RB-017**, and it is **not built** (confirmed out of scope in the WI-R1 fold-in). The payoff shows
  what it can count, under the name of what it is.

- **⬜ O-D173-4 — The reliability transition rides in the band row.**
  A reviewer's evidence moves **Reliability** (an ordinal level OSLO computes) more often than it moves a CAF band.
  This build states it as a transition alongside the CAF bands (*"Reliability: Moderate → High"*). Whether
  reliability is allowed to headline a payoff, or must always sit behind a CAF band, is an owner call.

---

## D174 — THE MATURITY-RAMP HERO: open items (escalated, not invented)

- **✅ O-D174-1 — CLOSED BY D175 (owner, 2026-07-12): NEUTRALISE THE CHIP.**
  `.ustate.prov` rendered **`--warning` (amber)** and `.ustate.cur` **`--success` (green)** — the Provisional ↔
  Current chip (**D040**), in the hero card's header, **one line above the five-step maturity ramp**. Each was
  *technically* honest on its own (it describes the **analysis state**, not the project) — **but amber-and-green
  above a five-step scale is exactly the adjacency a reader turns into RAG**: the **P1 health-framing class
  (DL-104 §5)** arriving **through a side door**, not from what either element says but from **what they say
  together**. **Owner: neutralise it.** *Provisional/Current is a **STATE**, not a **JUDGMENT** — a **dot and a
  word** carry it.* **The labels are unchanged (D040); only the colour went.** It is still legible at a glance —
  **by weight and shape, never by hue**: provisional = **hollow dot**, `--muted`, 600 · current = **filled dot**,
  `--text`, 700 (the D174 precedent: the lit ramp step is separated by **weight**, not hue).
  **And the real lesson was about the GUARD:** D174's neutrality guard was scoped to the confidence **focus**, and
  the defect sat **outside the focus, inside the same card**. **The D003 colour allowlist now governs the WHOLE
  HERO CARD** — `_assertHeroCardCarriesNoSeverityColour()`, read from the **authored cascade**, not the DOM (the
  green lived on `.cur`, a state that was not on screen — invisible to every DOM guard).

- **⬜ O-D174-2 — Does the ramp show the NEXT RUNG as an ask?**
  D174 says the ramp is motivating because it shows *"what the next rung is"*. The build shows the next rung
  **positionally** (it is the next step on the scale) but says **nothing** about what would move you onto it —
  because **the model cannot compute that**: there is no "what would raise the band" object, only the limiter and
  the open issues. Naming a next-rung condition would be **inventing** one (Anti-Assumption). **If the owner wants
  it, the ask is a rule that maps the limiting dimension to a band-raising condition OSLO can defend.**

- **⬜ O-D174-3 — The 0–100 index remains OWNER-OPEN (O-D173-1 stands).**
  D174 keeps the index **secondary, small, no delta**. The **CALIBRATE-or-DEMOTE** decision (DL-062 F1) is
  unchanged and still owed. The day it is calibrated, the ramp and the index can share the hero — the guard fails
  today only because an **uncalibrated** number must not look like a measurement.

---

## D175 — THE ADJACENCY SWEEP: what it found (escalated, not decided)

- **✅ O-D175-1 — CLOSED BY D176a (owner: approved, 2026-07-12). THE CAF LIMITER ROW LOSES BRAND ORANGE.**
  Owner: *"`--primary` is not a severity token, so D175's rule did not reach it — **but D174's own reasoning does**:
  it banned `--primary` from the ramp precisely because an amber-adjacent orange invites 'amber = at risk'."*
  **The limiter is a FACT — *"Feasibility is holding it back"* — not a WARNING.** It needs **emphasis**, and
  **weight gives emphasis**; orange gives it a temperature it has not earned.
  **Shipped:** the hero card's colour allowlist now excludes **`--primary`** alongside every severity/health token
  and every chromatic literal (`HERO_CARD_BANNED_TOKEN_RE`). The limiter row is marked by **weight** (`--text`,
  600/700) and by the words **"the limit"** — both computed from `_limitingOf()`. The card's links and the
  how-calc bullet lost their orange with it: **zero hue in the hero card**.
  **Guard:** `_assertHeroCardCarriesNoSeverityColour()` — the cascade read (chroma-graded, `@media`-aware) now bans
  the brand token too. **It also took a scope fix that its own negative control forced:** a rule with a **bare
  subject** (`.cr-limit b{color:rgb(217,122,58)}` — an orange on the limiter's bold text, through a plain `b`) was
  **invisible** to the old scan, which required the *subject* compound to carry a card class. NC-D176-04 caught it;
  the guard now grades bare subjects anchored by an ancestor. *(Fix the guard, never the doctrine — D166.)*

- **✅ O-D175-2 — CLOSED BY D176b (owner: approved, 2026-07-12). THE CAF BARS WERE PERCENTAGE FILLS. THEY ARE GONE.**
  Owner: *"A bar filled to 55% asserts a **CARDINAL MAGNITUDE OSLO cannot defend**, on the same uncalibrated scale
  (**DL-062 F1**). It is **worse than the 0–100 index**, because **a filled bar reads as a measurement without even
  showing its number** — and a **partial fill is the visual grammar of a PROGRESS / HEALTH bar** (**DL-104 §5 —
  P1**)."*
  **Shipped:** every CAF dimension — Clarity · Alignment · Feasibility — now renders as a **BAND on the hero's own
  five-step ordinal ramp** (Very Low · Low · Moderate · High · Very High; DL-086/098), on **both** surfaces (the
  Overview hero card and the confidence popover), with the **limiter marked**. **One builder, one mental model:**
  `_rampHTML(lvl,{compact:true})` — the very function that draws the hero. The reliability-basis rows lost their
  fills too and carry their **level word** alone. `_RELPCT` / `_RELCOLOR` are deleted.
  **The widths (`feasW`/`alignW`) stay in the MODEL** — they compute the band through `_cafLevelFor()`. They are
  simply never drawn again. **The Attention heat map is untouched: those cells are ISSUES (D003).**
  **Guards:** `_assertNoPercentageFillOnMaturitySurfaces()` (the cascade **+** the DOM **+** the **render path** —
  the fill was written by JavaScript, so a cascade-only guard would have been theatre) ·
  `_assertCafDimensionsRenderAsBands()` (the row's ramp is graded **byte-for-byte** against `_rampHTML`, the band is
  computed from state, the limiter is `_limitingOf()`). **`_d176NegativeControls()`: 15 injected regressions all
  bite; 2 must-not-fire controls stay green.**

---

## D176 — WHAT IT LEFT OPEN (escalated, not decided)

- **⬜ O-D176-1 — RELIABILITY HAS NO DRAWN SCALE, ON PURPOSE.** The reliability-basis rows (Coverage · Evidence
  availability · How assessable) lost their percentage fills and now show **only their level word**. They were
  **not** redrawn on the five-step maturity ramp: **reliability is a DIFFERENT scale** — D051 states its levels as
  **High / Moderate / Low**, while the prototype's `_RELORD` also carries a **Very Low**. Drawing a ramp would mean
  **choosing a step count canon has not fixed** — the assumption the Anti-Assumption Build Protocol forbids.
  **Owner call: (a) leave reliability as words, (b) ratify a reliability scale and give it its own ramp, or (c)
  fold it into the five bands.** *Escalated, not invented.*

- **⬜ O-D176-2 — THE PROGRESS CARD'S TRUE-COUNT BARS (kept, and flagged).** `Dependencies confirmed 2 / 3` and
  `Plan artifacts read 7 / 7` are drawn as **partial fills** (`.prog-trk i`). They were **kept**: each encodes a
  ratio OSLO can defend **exactly**, the **denominator is printed beside it**, and **D173b explicitly blesses true
  counts** (*"Evidence coverage 3 of 7 artifacts"*). They are **not** on a confidence/CAF/reliability surface and
  assert **no uncalibrated magnitude** — and a negative control (`mustNotFire_trueCountBarSurvives`) proves the new
  fill guard does **not** reach them, so *"no fills"* never quietly becomes *"no counts"*.
  **But a partial fill is still progress-bar grammar wherever it appears** (DL-104 §5). **Owner call: keep the
  count bars, or reduce them to the numbers alone.** *Escalated, not changed.*

---

# D177 — open items

- **O-D177-1 — the Deep Pass finds exactly two things, forever.** `DEEP_FINDINGS` is **demo data**: a fixed pair
  of findings a deeper read of the DevNorth brief genuinely supports. **The real product's Deep Pass finds what it
  finds** — the count is an output, not a constant. Nothing in the payoff, the guard or the copy assumes *two*
  (every number is computed; `_numWord(foundN)` scales), but the **demo** will always find these two.
  **Not a defect — a prototype boundary. Flagged so nobody reads it as a product rule.**
- ~~**O-D177-2 — no clarification request rides with the new findings.**~~ **✅ CLOSED by D178 (owner: approved,
  2026-07-12).** The owner answered the escalation: **a Deep Pass ASKS, it does not only find.** ISS-07 now carries
  a `clar` — *"Is there a minimum signed-sponsorship floor — or a cancellation point — that has to be cleared before
  the AV and catering commitments go firm?"* — bound to the issue it would close and to the evidence already on the
  record (Schedule `Aug 15` · AV/Caterer `Confirmed` · sponsor-funded Intent). **No new facts.** It moves the third
  true count (**Open questions 2 → 3**, computed by `_openClarIds()`), it renders **collapsed** in the panel and in
  the chat, it is answerable on **either** surface through `_submitClarification()` (byte-identical History), and
  answering it closes the gap through an **analysis update — never by hand**. Guarded (`_assertDeepPassMovesBandAndCounts()`
  now grades the ask) with three new negative controls, incl. **the Deep Pass raises nothing → red**.
- **O-D177-3 — the critical count rose, and the limiter did not change.** Feasibility rose **and** took a second
  critical issue in the same run, and it is **still the limit**. That is coherent (the band is understanding
  maturity; the issue is a finding about the plan) — but it is the first place in the product where a **rise** and
  a **new critical** land on the **same dimension** in the same breath. **Watch it in usability testing.** If a
  reader hears *"Feasibility went up"* as *"feasibility got better"*, the defect is in the **word**, not the model.

---

# D178 — open items

- **O-D178-1 — the Deep Pass asks exactly one question, forever.** Like `DEEP_FINDINGS` itself (O-D177-1), the ask
  is **demo data**: one `clar` on ISS-07 that a deeper read of the DevNorth brief genuinely supports. **Nothing
  assumes *one***: `asked` is the rise in the `questions` row, `_numWord(asked)` scales, and the chat line
  pluralises. The real product's Deep Pass asks what it needs to ask. **A prototype boundary, not a defect.**
- **O-D178-2 — the ask is bound to an issue, so it cannot outlive it.** `_openClarIds()` filters on
  `_istatus[id] !== 'resolved'`, so a clarification is a **property of an open issue**, never a free-standing
  question. If a Deep Pass ever needed to ask something **not tied to a finding** (*"who signs off the run-of-show?"*),
  the model has **no home for it** — there is no clarification register independent of `ISSUES`. **Not invented.**
  **Owner call if it is ever needed** (it would also change what *Open questions* counts).
- **O-D178-3 — ISS-07 now carries BOTH a recommendation and a question, and the panel shows only one primary
  action.** `openIssue()` prefers **Apply this fix** when `rec` exists, so the **Answer** button is not the primary
  on ISS-07 — the ask still renders as a collapsed row (and rides the chat turn), exactly as on ISS-01, which has
  the same shape. **Consistent, and pre-existing** (D162b: one contextual primary). Flagged because ISS-07 is the
  first **critical** where *the question is arguably the better first move than the fix*. **Watch in usability
  testing; the fix, if any, is a D162b amendment — not a special case for one issue.**

---

# D179 — open items

- **O-D179-1 — CLOSED by D180b. "Artifacts read 7 / 7" IS KILLED, and nothing replaced it.** **OSLO always reads all
  seven: it is a CONSTANT, not progress** — and it was hard-coded *because* it was meaningless. **A number that can
  never move is not information; it is decoration.** *"Read"* was never the interesting question. ***"Grounded in
  evidence"* is** — so the star row of Progress is now **`GROUNDED — 2 of 7 artifacts rest on your evidence`**,
  computed from the artifact **basis** (`attested`), which **moves when the user acts**. **Guarded by a MECHANISM,
  not a phrase:** `_assertNoConstantDressedAsProgress()` perturbs real state (ground an artifact · a deeper read
  finds and asks more · an update resolves one · the user answers one) and **requires every row on screen to move**.
  A constant cannot survive it, whatever it is called. *(The partial-analysis caveat that made a hard-coded `7/7`
  dishonest — D139/UP-4's size envelope — is moot: nothing counts "artifacts read" any more.)*

- **O-D179-2 — there is still NO DEPENDENCY REGISTER, so "Dependencies confirmed" is still absent.** The Progress
  card used to show `Dependencies confirmed 0 / 3` **with a percentage fill**. It was counting **clarification-bearing
  ISSUES** and calling them dependencies. `REVIEWS` is a list of review *requests*; `ISSUES[].clar` is a *question*.
  **Neither is a dependency with a confirmed/unconfirmed state.** The row is **omitted, not invented** — the day a
  dependency register exists, it is **ONE row** in `PAYOFF_COUNTS` and it appears in Progress automatically.
  *(Carried forward from the D173 escalation; the fill is now gone too, per D179e.)*

- **O-D179-3 — CLOSED by D180a·3. *Resolved* is BACK — under CLOSED, and never as a target.** The owner's ruling:
  **it is the one number that tells a PM their work worked.** It is now one row of `PAYOFF_COUNTS`
  (`resolved`, computed as `_istatus[id] === 'resolved'`), it renders in the **CLOSED** row beside
  **`Questions answered`**, and it is **FENCED so it can never become a burndown**: **no denominator, no
  percentage, no "remaining", and it may not leave the CLOSED row.** → `_assertClosedIsNeverATarget()` grades the
  registry (a `of()` on a closed count is a violation), the DOM (`.pg-row[data-row="closed"]` must hold it) and the
  copy. **Negative controls:** `theSubtleBurndown_aDenominatorOnResolved` · `c_resolvedLeavesTheClosedRow` — both
  bite.

- **O-D179-4 — RELIABILITY has no ramp, so a reliability move is the ONE transition that still travels in words.**
  Canon states **five bands** for confidence and the CAF dimensions (DL-086/098). It states **no scale** for
  reliability — so OSLO does not draw one (Anti-Assumption; the same reasoning that removed the popover's
  reliability bars in D176b). A reliability transition therefore renders as *"Reliability: Moderate → High."* in the
  payoff line. **It does not occur in the demo data** (both reads are *Moderate*), so it is **unexercised on screen**.
  **OWNER: if reliability is to be drawn, its scale is an owner decision.**

- **O-D179-5 — the cool accent is a NEW TOKEN in the palette, and it is not in the ratified visual spec.**
  `--maturity` (`#7FA0C9` dark / `#3F6193` light) reuses the hex values of the existing `--cool` token — which is
  already in the palette and already carries the *Attested by <name>* / *awaiting* semantics — but under a **new
  name with a new meaning: emphasis on a maturity surface.** Two tokens now share a hue. **AA verified in both
  themes** (6.13:1 · 6.28:1). **OWNER: confirm the token name and whether `--cool` and `--maturity` should remain
  distinct** (they mean different things, and collapsing them would let a maturity rule inherit an epistemic one).

- **O-D179-6 — the count-uniqueness guard is scoped to `#pane-overview`, and that scope is a JUDGMENT.**
  The left **nav rail** badges (`#vsAttnBadge`, `#vsIssuesBadge`) render the open-issue count, and the **Attention
  map** counts issues per cell. Neither is on the Overview, and both are **wayfinding**, not a second home for a
  number the reader is asked to reconcile. **D179e's finding is about the Overview arguing with itself**, and that
  is what the guard grades. **Stated, not assumed.** **OWNER: if "one home" is meant globally, the guard's scope is
  a one-line change** — but a nav badge with no number is a worse product.

- **O-D179-7 — two guard defects were found by the D179 behavioural harness, and both were ORDER-DEPENDENT.**
  Neither was a product defect; both were guards that were green at boot and would have gone red the moment a user
  acted. **Fix the guard, never the doctrine** (D166 §3):
  1. **`_assertDeepPassMovesBandAndCounts()` could not survive a user fix.** `applyFix()` **mutates
     `READ.provisional`** (it raises `feasW` — correctly: the read moves when the user acts). After one fix, **the
     Fast-Pass read no longer exists in the model**, and the guard — which must run the Extended pass *from* the
     Fast-Pass read — had nothing honest to run from. **`_READ0` now freezes the read at load**, and the guard stages **only the
     pass's INPUT** (`READ.provisional`), leaving `READ.current` — the pass's **output** — untouched, so a negative
     control that breaks the output (**NC-D177-02**) stays visible. *(The first draft staged the whole `READ` and
     silently killed that control: **a guard that resets what a control injects into is a guard that can no longer
     fail.**)*
  2. **`_assertChatOpeningIsShort()` never graded the Extended pass's own issues.** It walked `ISSUES` — and
     **ISS-07 / ISS-08 do not exist until the pass runs.** **The newest copy in the product was the one copy no word
     budget could see**, and **ISS-07's opening turn was 57 words against a budget of 50** (D167/D163). The sentence
     is split (nothing is lost — the run-of-show detail moves into the second sentence, which the panel still shows
     in full), and **the guard now stages `DEEP_FINDINGS` into `ISSUES` for the length of the check** and **refuses
     to run** if a deep finding is not being graded.


---

# D180 — open items

- **⛔ O-D180-1 (FOUND, ESCALATED — NOT FIXED). The chat's "What's it resting on?" pull turn is 41 words against a
  budget of 40 — but ONLY in a state the guard cannot see, and the overflow is CITED EVIDENCE.**
  **Repro (jsdom, deterministic):** boot → Extended pass → `applyFix('ISS-01')` → `_assertChatPullTurnsAreShort()`
  goes **red**. The top open issue is then **ISS-07** (a D177 deep finding), whose evidence answer carries **three
  cited lines** from the plan artifacts — and `_probeWords()` counts the citation chips as prose.
  **This is NOT a D180 regression:** it reproduces byte-for-byte with the pre-D180 `_openClarIds()` restored at
  runtime, and the D180 work touches neither the chat nor the evidence copy.
  **It is the D166 vacuity again, one surface over:** `_assertChatPullTurnsAreShort()` grades **only the boot
  state's top issue**, so **the newest copy in the product is again the one copy no budget guard can see** — the
  exact lesson of E-D179-12, which fixed the *opening* guard and left the *pull* guard un-staged.
  **The tension is real and it is an OWNER call, so it is not resolved here (Anti-Assumption):** the overflow is
  **evidence citations (D177/D178), not padding.** Trimming it means deleting a cited line. **Three honest options:**
  (a) **raise the pull budget** for evidence turns; (b) **exclude citation chips from the word count** (they are
  affordances/evidence, on the same reasoning that already excludes `.chat-acts`/`.chat-follow`); (c) **cap the
  citations shown** and put the rest one click away. **DO NOT ASSUME — D163 (budgets) vs D178 (cite the evidence)
  is a doctrine-level trade, and it is the owner's.**

- **O-D180-2 — GROUNDED counts ARTIFACTS, not evidence, and the denominator is the seven plan artifacts.**
  The star row says *"N of 7 artifacts rest on your evidence"*: an artifact counts as grounded when its **basis**
  is `attested` (*Confirmed by you* — D011), which happens when the user **applies a fix**, **answers a
  clarification** or **edits the artifact**. It is **a true, defensible count of a real population.** What it is
  **not** is a measure of *how much evidence* sits behind each artifact — the model holds **no evidence register**,
  so **OSLO does not count what it does not hold** (the same discipline that keeps "Dependencies confirmed" absent,
  O-D179-2). **OWNER: if "grounded" should mean *weight of evidence* rather than *user-attested*, that needs a
  model — it is not assumed.**

- **O-D180-3 — "Questions answered" is a NEW piece of state (`_clarAnswered`), written by the ONE clarification
  door.** A question leaves **OPEN** the moment the user answers it and appears under **CLOSED** — so the same
  question is never counted twice (D179e). It is written only by `_submitClarification()` (panel **and** chat —
  D108/D096), so the count can never outrun what the user actually did. **This is a modelling choice, not canon:
  it is flagged, not decided.** *(Before D180, an answered-but-not-yet-resolved question kept counting as OPEN,
  which would have shown it in both rows at once.)*

---

# DL-109 — Provenance: what is owner-open

- **⚠️ AMENDS O-D180-2 — GROUNDED IS NO LONGER ARTIFACT-LEVEL.** DL-109 §2a makes it **claim-level**:
  *"Your evidence: 17 claims · I inferred: 11."* Both counts come from `ContextItem.evidence_id`, and an artifact
  the user **confirms** grounds the items read out of it (`EV-ATT-<art>` — *that confirmation IS evidence*). The
  old open item asked whether "grounded" should mean **weight of evidence** rather than **user-attested**; DL-109
  answers it **at the item level**, and the answer is: **an item is grounded when it traces to evidence** —
  the pasted brief, the linked sponsor brief, **or the user's own attestation.**

- **✅ O-DL109-1 — CLOSED by D181b (owner, 2026-07-13): AGE THE CLOCK, NOT THE PAST.**
  **Neither option (a) nor (b).** The owner rejected ageing the demo project: it **genuinely is new**, **Slice 7's
  D100 first-run state assumes exactly that**, and a three-week history on a first-run project is *"a small lie told
  to make a surface look better"* — which this build had correctly refused.
  **Built instead: `simNextWeek()` now advances the CLOCK** (`_WEEK_MS` · `_demoWeeks()` → **`_ciNow()`**, the one
  "now" every provenance surface reads). **Advancing a week AGES the assumptions** — the viewer *watches*
  *"Unvalidated for 2 minutes"* become ***"Unvalidated for 3 weeks · 1 issue depends on it."*** **Grounding velocity
  moves with the weeks too** (the window is the current demo week; a week in which nothing happened honestly reads
  **0 · 0** — *understanding is stalling*). The timeline's Initial run ages on the same clock, so **no two surfaces
  can disagree about how old the run is.**
  **DEMONSTRATE AGEING; DO NOT ASSERT IT.** *A number you watch climb argues better than a label that asserts.*
  **At week 0 the offset is ZERO — D100 holds, byte-for-byte.** Guards: `_assertSimNextWeekAgesTheAssumptions()` ·
  `_assertD100FirstRunStateHoldsAtWeek0()`. NCs: `ageingIsTyped_bites` · **`thePastIsBackDated_bites`** — both bite.

- **⬜ O-DL109-2 — INFERENCE CHAINS ARE ESCALATED (DL-109 §5). A SCHEMA DECISION, AND IT IS THE OWNER'S.**
  *"Your Schedule rests on an inference that rests on an inference."* **`ContextItem` has no `derived_from`.**
  Item-to-item lineage is **not modelled**, is **not approximated here**, and is guarded against
  (`_assertNoInferenceChains()`). **R1 already carries three blocking items** (the DL-069 model-judgment eval ·
  E1–E3 · the M4 Reporting spec). **Chains would be a fourth.** DL-109's own sequencing note: **ship §2 and §4,
  watch what alpha users ask for, and let the chain work earn its place.**

- **✅ O-DL109-3 — CLOSED by D181a (owner, 2026-07-13): "LOAD-BEARING" = THE READ WOULD CHANGE WERE IT FALSE.**
  **The owner rejected BOTH candidates.** **Loose** (`item.dim === limiting`) → **11: over-counts**, sweeping in
  inferences **nothing rests on** (CI-45 · CI-56 · CI-57). **Strict** (*supports an open issue*) → **under-counts,
  with a fatal blind spot: it says SCOPE's inferences are NOT load-bearing** — and **Scope is the artifact the
  Inference map flags as the most dangerous thing in the plan.** *It misses **FALSE CONFIDENCE** entirely — the exact
  case the feature exists to catch.*
  > **AN INFERENCE IS LOAD-BEARING IF THE READ WOULD CHANGE WERE IT FALSE. Operationally: THE READ POINTS AT IT.**
  > **(a)** a **critical issue** cites it · **(b)** the **limiting dimension's** assessment rests on it · **(c)** ⭐ **a
  > **STRONG-READING artifact's** confidence rests on it** *(the false-confidence case)*.
  **Built. Boot: 12** — clause (a) **3** · (b) **8** · (c) **4** (**Scope: CI-20 · CI-21 · CI-22 · CI-23**).
  **Clause (c) is NON-NEGOTIABLE:** *an inference is load-bearing in two ways — it supports a **WARNING**, or it
  supports a **REASSURANCE** — and the reassurance is the more dangerous, because nobody is looking at it.*
  ***Scope reads fine **because of** four things OSLO made up.***
  **Items nothing points at are inferences — they are not holding anything up, and they are not counted.**
  Every clause is **computed** (`_ciLB_a` · `_ciLB_b` · `_ciLB_c`); clause (c) reads the **same** function as the map's
  flag, so **grounding the flagged artifact retires both together — and that fall is the USER'S SUCCESS, not a
  regression** (must-not-fire control). **Delete clause (c) → the guard goes RED** (`clauseC_isDeleted_bites`).

- **⬜ O-DL109-4 — "UNOWNED ENTITY" IS DERIVED FROM AN `owns` RELATIONSHIP, WHICH IS ITSELF INFERRED.**
  §2d asks for *"unowned entities"*. The model has no owner field on `entity`, so the prototype computes it the way
  the analysis describes: **an entity with no `owns` relationship bound to it.** ⛔ **But every `owns` relationship
  in this plan is itself OSLO's inference** (the brief names no owners; the WBS owner column is OSLO's). So
  *"5 named parties with nobody accountable"* means **"nobody OSLO could find, including in the owners OSLO itself
  invented."** **That is honest and it is worth saying — but it is a modelling choice, and it is flagged.**

- **⬜ O-DL109-5 — THE "ASSUMED DEPENDENCIES" COUNT EXCLUDES `owns` RELATIONSHIPS.**
  `relationship` items carry a `kind` (`depends` / `owns`). **"Assumed dependencies" counts only `depends`** — an
  ownership link is not a dependency, and counting it as one would inflate a number DL-109 wants to be sharp
  (*"a dependency nobody confirmed is the classic way plans die"*). **Stated, not assumed.**

---

# OPEN ITEMS — D182 / D183 (2026-07-13)

- **⬜ O-D183-1 — "AFTER ACTIVATION" WAS READ AS "AFTER FIRST VALUE". OWNER TO CONFIRM.**
  D183g says *"First run → Start here first · **After activation** → Progress first"*, and the direction added
  *"computed from state (**first-value delivered**)"*. **Built against `_firstValue()`** (the first MRI landed) —
  the one "activation" state the model actually holds, and the state D100's first-run copy already keys off.
  **A second, defensible reading exists:** *activation* = **the user's own work has landed something** (they have
  grounded a document, resolved an issue, or answered a question) — i.e. **there is progress to read**, which is
  the literal justification D183g gives (*"there is no progress to read yet"*). Under that reading Progress would
  lead **later**, and the Overview would show *Start here* first for the whole of a user's first session even
  after the read arrives. **Not assumed — escalated** (Anti-Assumption Build Protocol). Both are one line in
  `_overviewLeadsWithProgress()`.

- **⬜ O-D183-2 — THE GROUNDING BAND THRESHOLDS ARE PROTOTYPE-GRADE.**
  The five grounding words are cut at **10 / 35 / 60 / 85 %** of live claims resting on the user's evidence.
  **The cut-points are not canon** — there is no ratified scale for reliability/grounding (the Anti-Assumption
  note already standing against the reliability basis applies here too). The **word is computed and the ordering
  is defensible**; the **boundaries are an owner decision.** Nothing else depends on them: the qualifier is
  ordinal, it carries no number, and the guard proves only that it *moves with state* and *shares no word with
  the band*.

- **⬜ O-D183-3 — THE RELIABILITY *BASIS* ROWS STILL SPEAK IN BAND WORDS.**
  D183c retires band vocabulary from the **qualifier** (pill · hero · popover headline · payoff). The popover's
  **basis** rows — *Coverage: Moderate · Evidence availability: Moderate · How assessable: Moderate* — are the
  **disclosed detail** behind it and still use Low/Moderate/High, which is the vocabulary canon gives them.
  **The owner's complaint was the headline stutter, and that is closed.** Whether the basis rows should also move
  to grounding language is **not assumed** — it would mean inventing a scale for three dimensions canon states no
  scale for. **Escalated.**

- **⬜ O-D183-4 — `D049` IS NOW SPLIT AND SHOULD BE MARKED SO.**
  D183e supersedes D049's **user-facing** term ("plan artifacts" → **documents**) while D049's **canonical**
  entity (`Artifact`) stands. The decision log entry for D049 is not annotated. **Owner to record the split**, as
  DL-095 did for *Finding* / *Issue*.

- **✅ O-DL062-F1 / O-D173d — CLOSED BY D183b.** The "calibrate or demote the 0–100 index" question is answered:
  **DELETE.** The index may return **iff** it is calibrated (DL-062 F1) **AND** the forecast misread the
  *Outcome Confidence* label creates is closed. That note lives in the **prototype-notes layer only** (D161).

- **⬜ O-D182-1 — THE FENCE IS A PROTOTYPE MECHANISM AND SHOULD BE A BUILD RULE.**
  `_probeFence` / `_fenceEveryProbe` exist inside the prototype. **The rule they encode is general and belongs in
  build governance:** *a test, probe, guard or negative control may never produce a user-facing effect, and must
  restore every byte it touches.* **Three leaks of this class have now shipped in one prototype** (a live chat box
  retired · the append-only History corrupted · an upgrade prompt fired at a user who did nothing). **Recommended
  for `00_owner/build_governance/`** — engineering proposes, owner ratifies.

## Opened by D184 / D185 (2026-07-13)

- **⬜ O-D185-1 — THE RELIABILITY BASIS IS STILL FLAT IN THE DEMO DATA, AND THAT IS WHY THE OWNER SAW THREE
  "MODERATE"s.** `READ.current.reliability` is `{coverage:'Moderate', evidence:'Moderate', assessable:'Moderate'}`.
  The panel now *handles* that honestly (*"Even across the basis — Moderate."*) and *ranks* correctly the moment the
  three differ (proven by state perturbation). **But the underlying question is a MODEL question, not a copy
  question: does OSLO actually judge Coverage · Evidence · How assessable INDEPENDENTLY — and if it does, why do
  they never differ?** Either the three are genuinely independent (and the demo data should show it), or they are
  one judgment wearing three labels (and the panel is showing a distinction the model does not make).
  **ESCALATED — DO NOT ASSUME.** A worker may not invent reliability sub-levels to make a surface look informative;
  that is exactly the class of thing D173 forbids. **Owner decision owed.**

- **⬜ O-D185-2 — RELIABILITY HAS NO SCALE OF ITS OWN** (carried forward, now sharper). It is drawn with level
  words (High / Moderate / Low) and is deliberately **not** on the five-band maturity ramp — reliability is a
  different scale and OSLO does not invent one. **With the basis now RANKED (`_RELORD`), the prototype is asserting
  an ORDER on that scale.** The order is safe (it is only ever used to say which is *weakest*), but the **scale
  itself remains owner-open.**

- **⬜ O-D184-1 — "APPLY" AND "SELECT A PATH" ARE STILL TWO DIFFERENT VERBS, AND ONLY ONE OF THEM IS ASSISTED.**
  D089 gives OSLO's recommendation an **assisted apply** (OSLO drafts the change) and gives the *other options* a
  **select** (the user writes it themselves). So if a user selects a path and then clicks Apply, the apply still
  drafts **OSLO's** recommendation. The rank function already prefers the user's own selection where it *can* —
  but **it cannot make an unappliable path appliable.** Two honest options, both owner-owed:
  **(a)** assisted apply extends to any path (OSLO drafts whichever change the user chose), or
  **(b)** selecting a path **removes** the Apply button for that issue (there is nothing OSLO can draft).
  **Today the product does neither, and the seam is real.** **ESCALATED — DO NOT ASSUME.**

- **✅ FOUND BY THE D185 SWEEP, FIXED: the TOUR was still teaching the DELETED 0–100 index** — *"The 0–100 read is
  the focal point"* — in the one surface written to explain the product. The DOM guard could not see it (a tour step
  is a string in a registry until it is spotlit). **`_assertNoZeroToHundredIndexAnywhere()` now reads the TOUR
  copy registry too.** *A guard that only reads the DOM cannot see copy that is one click from the DOM.*

- **✅ FOUND BY THE D185 SWEEP, FIXED: the same self-justifying sentence had THREE homes.** *"Reliability is judged
  independently of Clarity · Alignment · Feasibility — it's about the evidence behind the read, not the plan's
  integrity, and it can rise as evidence improves"* was resident in the **popover**, the **Overview "why" box** and
  the **Project summary**. It now lives in exactly one place: **the ⓘ, on demand.**

- **✅ FOUND BY THE D185 SWEEP, FIXED:** *"Brighter = more attention — not a health score"* was resident **twice on
  the Attention map** (the lead and the legend). **Say the honest thing once** (D162a). The lead keeps it (with its
  ⓘ); the legend states the axes and stops.

### The standing DL-107 sweep — what else it found (ESCALATED, not touched)

*"A surface that explains why it is trustworthy is not."* Swept: every popover, tooltip, drawer and panel.
**Fixed (unambiguous):** the Confidence popover · the Overview "why" box · the Project summary · the Attention-map
legend · the tour's 0–100 copy. **Escalated (a ratified decision or a real judgment call sits behind each):**

- **⬜ O-SWEEP-1 — THE ADVISORY FOOTER** (`#advisoryFoot`): *"OSLO advises; you decide — you stay in control at
  every step."* **Resident, global, and ratified (D001/D027).** It is the purest example of the pattern — a line
  asserting trustworthiness — **and it may be exactly the line that must never move behind an ⓘ.** *Owner call.*
- **⬜ O-SWEEP-2 — THE PROJECT SUMMARY'S CLOSING CAVEAT:** *"This reflects OSLO's understanding of the plan — how
  clear, aligned, and feasible it is."* Resident, at the foot of a surface the user opened to read a summary.
  **Arguably a definition (useful) rather than a defence (noise).** *Owner call.*
- **⬜ O-SWEEP-3 — THE CHAT SAYS *"not a grade"*** (`_ansConfidence`): *"Confidence sits at Moderate — how mature my
  understanding is, not a grade."* **Chat is a conversation and may say "I" (D165/D183a)** — and a person asked a
  question deserves an answer that heads off the misread. **But it is still the product defending itself.** *Owner
  call.* One clause; within budget; **not swept unilaterally.**
- **⬜ O-SWEEP-4 — THE FALSE-CONFIDENCE FLAG ON THE OVERVIEW CARD** keeps its full paragraph (the popover's does
  not). **Deliberate:** the card is a reading surface, the popover is a 300 px console — and **D052's flag is a
  DISCLOSURE, which a word budget may not delete.** Flagged so the asymmetry is a decision, not an oversight.

---

## D186–D189 (owner, 2026-07-13) — open items

- **⬜ O-D186-1 — THE CAF LIMITER IS NOT CALLED A "BLOCKER". ESCALATED, NOT DECIDED.** The owner's directive was
  *"replace 'Holding It Up' label/copy with 'Blocker'."* **The load-bearing row could not take it** — *"Blocker"*
  tells the user to **remove the thing carrying their plan** (D186a), so it became **`YOUR READ RESTS ON`**. The CAF
  limiter **also** did not take it: *"Feasibility is a Blocker"* reads as *"the PROJECT is blocked"*, and a low
  Feasibility band means **OSLO's READ of feasibility is immature — a fact about the read, not a warning about the
  plan** (D003). It imports the project-health framing the doctrine forbids, in the panel most likely to be
  screenshotted into a status deck. **Shipped form (D185.4 + D196a): *"Feasibility — the lowest. Confirm it to lift the
  read."*** **The owner may override. It has not been done silently.**
- **⬜ O-D186-2 — THE ROW STUTTERS, AND IT DOES SO BY DIRECTION.** D186a fixes the **label** (`YOUR READ RESTS ON`)
  and D186b fixes the **copy** (*"N inferences your read rests on"*), and the row therefore reads
  **`YOUR READ RESTS ON` · *"9 inferences your read rests on"***. **Both strings are individually directed**, and the
  same redundancy existed in the shipped build it replaces (*"Holding it up" · "…are holding up your plan"*), so the
  structure was **not** changed unilaterally. **If the owner wants it read as one sentence, the copy shortens to
  *"9 inferences"* and the row reads `YOUR READ RESTS ON · 9 inferences`** — word-for-word the same words, no
  stutter. *Owner call.*
  **⛔ DL-111 + erratum supersede this row: the panel carries no `YOUR READ RESTS ON` label at all — load-bearing is
  its own *leans* line below the bar, a superset with the single caption *"Your read leans on N inferences — the
  inferred claims above plus inferred assumptions, relationships and metrics · See them →"*, so the stutter this item
  raised is gone.**
- **⬜ O-D187-1 — `grounded` IS NEUTRAL, AND THIS MAY SURPRISE.** D187.1 names *"you grounded"* as green-eligible.
  **The Progress `grounded` row is NOT that count.** *"Claims on your evidence"* also rises when a deeper read
  extracts a **new** claim from a document the user had **already** confirmed (`_ciEvidenceId()` reads the artifact
  attestation — `CI-69` on Resources is born grounded). **OSLO can move it without the user, so the mechanical test
  says NEUTRAL.** The green went to the count that genuinely passes: the week's **grounding velocity**
  (`_ciVelocity().you`, gated on `_ATTEST_AT`), on the Inference map. *Flagged so the asymmetry is a decision, not
  an oversight.*
- **⬜ O-SWEEP-1…4 — STILL ESCALATED, STILL NOT SWEPT.** D189's standing sweep was applied **only to the caption
  slot** (`.inf-note`). **A DISCLOSURE IS NOT NARRATION, AND A WORD BUDGET MAY NOT DELETE ONE** — the advisory
  footer, the project-summary caveat, chat's *"not a grade"*, and the Overview false-confidence disclosure remain
  exactly as they were, and remain **owner calls**. A must-not-fire control now **proves** the sweep did not reach
  them.


---

## Opened / closed by D190 (2026-07-13)

- **✅ O-D162-2 — CLOSED BY D184, AND NOW SETTLED BY D190.** *"The recommendation TEXT is one click away, not
  resident"* — the tension the build flagged and refused to resolve unilaterally. **The owner resolved it:** the fix
  is **resident above its button** (D184.1), the button is **short and constant** (D190a), and **the alternatives sit
  under it, in one place** (D190c). **Nothing about the recommendation is behind a chevron any more.**

- **⬜ O-D190-1 — A GLOBAL COLOUR TOKEN CHANGED, AND THE OWNER SHOULD KNOW.** Moving the options onto the
  recommendation card (`--surface-2`) surfaced a **pre-existing AA failure**: `--success` is a **fill/border** green,
  and it was being used as **TEXT** on the *"Confirmed by you"* pill and the *✓ Selected option* tick — **3.74:1 and
  3.72:1 in dark theme, below AA, everywhere those labels appear** (artifacts and the memo included, not just this
  panel). The move made a failing contrast worse, so it was **fixed rather than shipped**: a new **`--success-fg`**
  token (dark **#6FB894**, light **#3E7357** — unchanged, already passing) now carries success **as text**.
  **`--success` itself is untouched**, so D187's `--earned` distance guard grades exactly the values it always did,
  and no severity/valence semantics moved. **This is a legibility fix, not a product decision — but it is a
  product-wide visual change, and it is on the record rather than in the diff.** *(If the owner would rather the
  dark-theme green stay as it was, say so — the two labels are the only things that read it as text.)*

- **⬜ O-D190-2 — "ONE HOME" NOW HAS A MECHANISM. IT SHOULD PROBABLY BE A STANDING SWEEP.**
  `_assertOptionsHaveOneHome()` proves *"no affordance opens the same set from two places"* by **counting leaf
  renders and declared openers** — not by scanning strings. **D179e (counts have one home) and D183f (causes have one
  home) are the same rule**, and the product has now shipped the same defect **three times** in three registers.
  **Recommendation: generalise this guard into a `oneHome(set)` primitive and point it at counts, causes and actions
  alike.** *Not built unilaterally — it is a new guard class, not a fix.* **ESCALATED.**

---

## D191 — a decision, once made, could not be unmade (owner P1, 2026-07-13)

> ## ✅ **ALL FIVE ESCALATIONS ARE RULED AND LANDED (D192 · D193, owner, 2026-07-13). NOTHING FROM D191 IS OPEN.**

| Escalation | Owner ruling | Landed as |
|---|---|---|
| **O-D191-4** — *the attestation becomes un-withdrawable again ~1.9s after the apply; D191 §5 reinstated the P1* | **D192a — the worker was right. DROP THE RESOLVED CLAUSE.** *"Withdrawing a fix is not hand-moving the read. It is the user editing their own document and retracting their own word — the read then moves BY ANALYSIS, which re-opens the issue, because the gap is genuinely back."* **The standing prohibition is unchanged: the user may never move the READ by hand.** The status guard binds **the read**, not **the document**. | `_wdAvailable()` drops its resolved clause · `_withdrawCore()` **does not touch a `resolved` status** · `_analysisUpdateAfterWithdrawal()` re-opens the issue **by analysis** · **guard (e) REWRITTEN as the positive proof** (`_assertWithdrawSurvivesResolution`) — *the guard the owner ordered encoded the doctrinal error and would have held the defect in place* · NC ×3 |
| **O-D191-1** — *answering a clarification attests too* | **D192c — approved as proposed. Consistent.** | `_submitClarification` keeps the same record and the same inverse; `_ISSUE_TRANSITIONS` unchanged |
| **O-D191-2** — *edits made after an applied fix* | **D193a — ⛔ OSLO MAY NEVER DELETE THE USER'S OWN WRITING.** The restore is **CONDITIONAL**: untouched ⇒ restore; **edited since ⇒ DO NOT RESTORE** — withdraw the **attestation only**, and say so plainly. The attestation drops in **both** cases; an analysis update runs in **both** cases. Detection must be **real**. | `_docTouchedSince()` (content + version identity) · `_withdrawUnit()` conditional restore · the plain line in the consent step **and** on the record · `confirmWithdraw()` commits a pending keystroke first · guard (f) `_assertWithdrawalNeverDeletesTheUsersWriting` · NC ×3 |
| **O-D191-3** — *two decisions, one document* | **D193b — REFCOUNTED BY DECISION, COMPUTED.** It stands while **any** standing decision attests it; it drops only when the **last** one is withdrawn. **Reliability restores to its pre-*first*-attestation value.** | `_attestBy[]` + `_ATTEST_BASE[]` (captured at the 0 → 1 edge) · guard (g) `_assertAttestationIsRefcountedByDecision` — **it constructs the two-decision document** · NC ×2 |
| **O-D191-5** — *the lifecycle chevron draws a ratchet* | **D192b — the diagram must stop asserting otherwise.** | `⇄` arrows · **no trailing fill** · the ⓘ says the states move both ways · guard (h) `_assertLifecycleIsNotDrawnAsARatchet` (**it drives the issue backwards and the track must follow**) · NC ×2 |

**⬜ ONE THING THE OWNER MAY WANT TO RULE ON (built the honest way; NOT invented):**

- **⬜ O-D193-1 — WHAT DOES THE ANALYSIS UPDATE DO WITH THE ISSUE WHEN THE DOCUMENT WAS *NOT* RESTORED?**
  D193a settles the **document** (kept) and the **attestation** (dropped) and says **an analysis update runs in both
  cases** — but it does not say what that run should *find*. **Built by derivation, not by assumption:** the run
  re-reads the plan **as it now stands**, and when the user's later edits kept OSLO's change **in the text**, the gap
  it closed is **still closed in the text** — so the run **does not re-open an issue it cannot see.** What it does
  find is that **the document is no longer confirmed by the user**, so the basis falls to *From OSLO* and Reliability
  falls with it, and the History event says exactly that. *(The alternative — re-open the issue anyway — would be the
  product asserting a gap that the text does not have, on the strength of a withdrawn confirmation. That looked like
  inventing a read.)* **If the owner wants the issue re-opened regardless, it is one clause in
  `_analysisUpdateAfterWithdrawal()`.**

## D194 (owner, 2026-07-13) — open items

- **⬜ O-D194-1 — THE TWO PROGRESS ROWS COUNT DIFFERENT POPULATIONS, AND THEY SIT NEXT TO EACH OTHER. OWNER DECISION.**
  **Found by the D194d guard, not by reading.** The **GROUNDED** row counts **CLAIMS** (`item_type='claim'` — DL-109
  §2a): live, **From OSLO 11 · Confirmed by you 17**. The **YOUR READ RESTS ON** row counts **INFERRED ITEMS OF ANY
  TYPE** (claim · assumption · relationship · entity · metric · interpretation — DL-109 §2b / D181): live, **12**,
  drawn from **37** inferred items.
  > **So the load-bearing count (12) legitimately EXCEEDS the "From OSLO" claim count (11) — and both numbers are
  > correct.** Nothing is wrong with either. **But they are adjacent, and they do not share a denominator.**
  **This is the strongest possible support for D194d** (do not merge: merged, the panel would read *"12 of the 11
  things OSLO made up"*, which is not a ratio, not a subset, and not true). **It does not, however, resolve the
  adjacency.** Three honest options, and the build does **not** choose between them:
  1. **Leave it.** The rows are structurally distinct, carry no ratio grammar, and the guard forbids the merge. *(The
     current state. It relies on the user not doing arithmetic across two rows.)*
  2. **Make the load-bearing count CLAIM-LEVEL too** — one population, two rows, no possible cross-read. **Cost: it
     would silently drop the assumptions, entities and metrics the read rests on — and D181's whole point is that
     the read rests on those.** *(This would be a doctrinal change to DL-109 §2b, not a copy fix.)*
  3. **Name the population in the row** (e.g. the ⓘ says which items each row counts). **Cost: DL-107/D189 — a
     caption that pre-empts a misreading is deleted.** *(A ⓘ is one tap away, so this is the least bad of the three,
     and it is what the Progress ⓘ now does in part.)*
  **ESCALATED. DO NOT ASSUME** (Anti-Assumption Build Protocol).
  **⛔ DL-111 + erratum note:** the two rows are now the foundation bar's **solid segments** (grounded *Confirmed by
  you* — cool accent · inferred *From OSLO* — hatched; a claim-level provenance comparison) and a separate
  **load-bearing *leans* line below the bar** (the any-type **superset** the read leans on, e.g. 20 ⊇ the 12 inferred
  claims). The line is **never `+`-joined** to the bar — a form of option 1 that makes the cross-read materially
  harder — but the **incommensurable-populations** point stands, and the adjacency remains an owner call.

- **⬜ O-D194-2 — "ATTESTED BY \<NAME\>" WITH MORE THAN ONE ATTESTER HAS NO RATIFIED NAME. OWNER DECISION.**
  The third epistemic class is `Attested by <name>` (D011/D069/D115). **The registry therefore REQUIRES the name**:
  a class OSLO cannot NAME is not drawn (D173), and *"Attested by them"* / *"Attested by others"* would be a **new
  string, invented at the render path** — exactly what the Anti-Assumption Protocol forbids. `_ciThirdPartyWho()`
  returns the attester **only when there is exactly one**; with two or more it returns `null` and the cell is
  **absent**. **The aggregate name is an owner decision.** *(It cannot bite today — no `ContextItem` carries a
  third-party attestation — but it will the moment reviewer evidence becomes claim-level.)*

- **⬜ O-D194-3 — PROSE THAT *MENTIONS* A CLASS NAME IS NOT SINGLE-SOURCED. STATED, NOT SWEPT.**
  `EPI_CLASSES` governs every element whose **job is to NAME a class** (`.elabel`, `.epi-tag`, `.sro-epi`, `.pg-cl`,
  the map key) — all now carry `data-epi-class` and repaint from the registry. **Sentences that mention a class
  inside prose are sentences, not labels**, and several of them live in the **withdraw/attestation machinery
  (D191–D193), which this task was explicitly forbidden to touch.** They are correct today; they are simply not
  wired to the registry. **If the owner ever renames a class, those sentences are the manual work.** *(Deliberate,
  scoped, and on the record — not an oversight.)*

## D195 (owner, 2026-07-13) — escalated, not invented

- **⬜ O-D195-1 — SHOULD A RETIRED CLARIFICATION BOX *LOOK* RETIRED? OWNER/DESIGN DECISION.**
  `_retireClarBoxes()` and `_chatRestore()` wrote a **`superseded`** class onto stood-down in-chat clarification
  boxes. **Nothing painted it and nothing read it** — a write-only name that *looked* like it was doing the
  stand-down while the stand-down was actually the id removal and the disabled controls (which still happen).
  The dead name is **removed**; **a visual treatment was NOT invented.** *(Giving a dangling class a rule so that
  the guard goes green would be inventing product design to satisfy an instrument — the exact inversion D166 §3
  forbids.)* **If a superseded box should read as superseded, that is a design decision. ESCALATED.**

- **⬜ O-D195-2 — ONLY THE BAND-1 WAITLIST SIGNAL IS ACCENTED. IS THAT INTENDED?**
  `.wl-sig[data-sig="review"]` (review-requested — the strongest signal, CR-4/CR-5 band 1) carries the cool accent;
  `referral` and every other key render in the base chip style. **This was previously an ACCIDENT** — the key was
  interpolated into the class name and `.referral` simply resolved to nothing. It is now a **deliberate,
  addressable rule** and the rendering is byte-identical to what shipped. **Whether the referral signal should
  also be accented is an owner call — no rule was invented for it.**

- **⬜ O-D195-3 — THE DANGLING-NAME SWEEP DOES NOT SEE FUNCTIONS THAT ARE NOT ON `window`.**
  `_assertEveryClassNameResolves()` reads the source of every **product function reachable from `window`** (guards
  and their negative controls are excluded **by the same rule the probe fence uses** — apparatus is not product,
  and a guard that graded its own `.ip-probe` scaffolding would be its own subject). **A `class="…"` literal
  inside a function closed over by an IIFE and never exposed would not be swept.** *(No such literal exists today —
  the sweep found and closed all 8 dangling names — but the boundary is stated rather than assumed.)* **A true
  build-time sweep of the raw file would close it; that is a build-tooling decision, not a prototype one.**

- **⬜ O-D195-4 — `#annoPop` IS THE ONLY LAZILY-CREATED PANEL, AND THE GUARD INSTANTIATES IT TO GRADE IT.**
  It is created on first hover, so the guard **calls the real factory, measures the real element, and removes it
  again** (body children **31 → 31**; D182 — a probe leaves no residue). **This works because the factory is
  idempotent.** If a future panel's factory is *not* idempotent, the registry entry must say so. **Noted, not
  assumed.**

---

## D196 — the verb/state split (owner, 2026-07-13)

- **⬜⬜ O-D196-1 — ⚠️ THE GROUNDING-VELOCITY LABEL: *"you grounded"*. DECIDED — NOT CHANGED. ESCALATED, NOT INVENTED.**
  **The brief asked whether the velocity row's *"you grounded 3"* is an IMPERATIVE (⇒ it changes) or a PAST-TENSE
  STATE of the user's own action (⇒ it stays). It is unambiguously the second — and I am naming the call rather
  than burying it, because the deeper question it opens is an OWNER call.**
  - **It is not an order.** *"you grounded"* is a **stat-cell label on a measured count** (`_ciVelocity().you`,
    gated on `_ATTEST_AT[art]`), with the subject **"you"** and the verb in the **past**. It **reports on the user;
    it does not address them.** D196a's scope is *"every **imperative / call-to-action / button / link** addressed
    to the user"* — **this is none of those.** The guard therefore correctly leaves it alone, and
    `mustNotFire_youGroundedIsPastTenseNotAnImperative` **proves it stays legal.**
  - ⛔ **AND RENAMING IT WOULD HAVE COST MORE THAN IT BOUGHT.** *"you **confirmed** 3"* would put **the user's verb
    and the ratified class name *"Confirmed by you"* on two counts, one panel apart, over TWO DIFFERENT
    POPULATIONS** — the **week's** newly-attested claims (§4b) versus **every** claim the user has ever confirmed
    (the Progress ledger, D194c). **That is the two-sizes-of-one-word error the whole decision exists to prevent
    (D194b), arriving through the fix.**
  - **The product already says the causal chain out loud, in that cell's own tooltip:** *"Claims that became yours
    this week, **because you confirmed** the document they came from."* → **The user CONFIRMS; the claims become
    GROUNDED.** *(D187 named this count *"you grounded"* and put the **only green in the panel** on it, precisely
    because nothing but the user's own work moves it. That green is untouched.)*
  - ⬜ **OWNER DECISION:** if the owner wants the past tense to carry the new verb anyway, the honest form is
    **not** *"you confirmed"* (it collides) but a **re-cut of the cell around the object** — e.g. *"documents you
    confirmed"* (a different population, and therefore a different number). **That is a product-design change, not
    a copy sweep, and it has NOT been made.**

- **⬜ O-D196-2 — THE INTERNAL VOCABULARY DID NOT MOVE, AND THAT IS A CHOICE.**
  The code, the guard names (`_assertGroundingRisesWhileIssuesRise`) and the doctrine comments still say *"the user
  **grounds** an artifact"*. **D196a's scope is user-facing copy** — and internally the state machine has always
  written **`basis='attested'`**, so nothing is drifting. **But the CANONICAL_GLOSSARY may want the internal action
  named `confirm` too**, so that the code and the screen use one word. **Not assumed. Owner/glossary call.**

- **⬜ O-D196-3 — *"Your evidence is solid ground."* (the Inference-map lead) IS A NOUN, AND IT STAYS.**
  It is the **foundation metaphor D186 built** (*"your read **rests on** 13 inferences"* → rests on → foundation →
  **ground**) — the very metaphor family whose coherence was one of the four reasons *"stabilize"* was rejected.
  **It is not an imperative and the guard does not touch it.** **If the owner reads it as jargon too, it is a
  separate copy call** — but **replacing it would leave "rests on" with nothing to rest on.**

## D197 · D198 · D199 (owner, 2026-07-13)

- **⬜ O-D197-1 — ⛔ D197's VALUE LINE COLLIDES WITH D194a, AND THE BUILD CHOSE D194a. ESCALATED.**
  **D197a says:** *Value: "13 inferences your read rests on" → **"13 load-bearing inferences."*** **But the value
  today is already *"13 inferences"*** — **D194a stripped the trailing phrase**, because *the LABEL is the sentence*
  (one home, D179e). **Rendering *"13 load-bearing inferences"* beneath a `LOAD-BEARING` label puts the name in TWO
  HOMES** — the exact defect D194a removed, and `_assertNoProgressRowSaysItTwice()` goes **RED** on it.
  **The build therefore renders:** **`LOAD-BEARING` · 12 inferences ↓7 · *See them →*** — and the full phrase
  ***"Load-bearing inferences"*** is `TERMS.loadbearing.name`, spoken on the surfaces that carry **no separate
  label** (the count registry, and any surface that needs the standalone name).
  ⛔ **This is a reading of D197 against a ratified guard, not a silent choice.** **If the owner wants the LITERAL
  D197 value line, D194a must be amended for this row** — say so and it is a one-line change (plus the guard).
  **⛔ DL-111 + erratum supersede this on the panel:** load-bearing is now its **own *leans* line below the bar**
  with **no `LOAD-BEARING` label** — the fixed copy *"Your read leans on N inferences — the inferred claims above
  plus inferred assumptions, relationships and metrics · See them →"* — so the D197-vs-D194a collision no longer
  arises here. The standalone name **`TERMS.loadbearing.name` = "Load-bearing inferences"** still governs the
  count registry and the Inference-map surfaces that carry no separate label.

- **⬜ O-D198-1 — THE MARKER'S PIXEL CLAUSE CANNOT BE MEASURED IN THE HARNESS.**
  Clause (3) of `_assertMarkedRowsKeepTheirGeometry()` compares real content start-x/end-x. **jsdom has no layout
  engine — every rect is zero** — so the clause **declares that it measured nothing and does not pass on its own**
  (*rects that are all zero are ABSENT, not identical*). **The in-flow child signature and the computed box model
  carry the proof, and both are real measurements** (of the DOM and of the resolved cascade). **The pixel clause is
  live and fires in any real browser.** ⚠️ **No headless browser is available in the build environment**, so the
  pixel numbers in this report were **not** captured — they are asserted by the two mechanisms above. **If the owner
  wants a captured pixel measurement, it needs a browser in CI.**

- **⬜ O-D199-1 — THE NOTES LAYER MAY NO LONGER PRINT THE DELETED INDEX, IN ANY FRAMING.**
  Two prototype notes were rewritten so that neither prints *"0–100"* or *"62/100"* — **including the one that
  printed it in order to explain that it was deleted.** *A note that keeps printing the number keeps the number
  alive in the reader's head* (DL-107 — obey, don't narrate), **and it made the guard unwritable: a scanner cannot
  tell "teaching it" from "recording its death" by looking at the digits.** **The rule is now mechanical, on every
  note, forever.** ⚠️ **If the owner wants the notes to be able to QUOTE dead copy verbatim**, that needs a
  *declared* exemption (the `data-voice="user"` precedent) — **it has not been invented here.**

- **⬜ O-D199-2 — THE INTERNAL VOCABULARY STILL SAYS "confidence".**
  `ConfidenceState` · `currentRead()` · `falseConfidenceHolds()` · `_ansConfidence()` · `.conf-pill` · `--conf-*`.
  **Canon's own entity is `ConfidenceState`, whose definition is *"Per-run **Outcome Confidence** snapshot"** — so
  the internal name is not drifting. **D199's scope is user-facing copy.** **Whether the CANONICAL_GLOSSARY wants
  the internal names to carry the full term too is an owner/glossary call. Not assumed.**

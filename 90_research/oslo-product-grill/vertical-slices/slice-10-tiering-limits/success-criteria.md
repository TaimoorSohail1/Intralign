# Slice 10 — Tiering & Limits · Success Criteria

---

# ⚠️⚠️ AMENDED 2026-07-12 — **D163 + D164 ARE RATIFIED. READ THIS BEFORE ANYTHING BELOW IT.**

## D163 — hard word budgets (binding, every surface)

| Surface | Budget (user-visible words, notes-toggle OFF) |
|---|---|
| Upgrade / limit prompt | **≤ 30** (title + body + the one honest label + the resolution buttons) |
| Tooltip / ⓘ | ≤ 20 |
| Modal body (prose) | ≤ 60 |
| Empty state | ≤ 15 |
| Panel row / label | ≤ 8 |
| Toast | ≤ 12 |

**BANNED, everywhere in product copy:** any sentence explaining **why** we do something · any sentence about what we
**"will never do"** · any sentence **naming or paraphrasing a doctrine** (*spin · credibility · epistemic · "at any
price" · "under your name"*) · any **second sentence restating the first** · any **reassurance addressed to the owner**
rather than the user (*"free and unlimited — on every plan"*).

**WHAT SURVIVES:** the **honest label**, once, short. *"Editing is always free."* · *"Comments never change the
assessment."* · *"Viewers take no seat."* · *"Asking for a read is free — no invite, no seat."* · *"previous analysis"*
· the reliability qualifier · *"From OSLO" / "Confirmed by you" / "Attested by \<name\>"* · limit disclosures that name
the limit and the tier. **A paragraph explaining any of them — NO.** Contracts and rationale live on an **ⓘ (≤20
words)** or in the **prototype-notes layer** (`pn()`, OFF by default).

**The exhibit:** the Basic/report upgrade prompt shipped as a **~300-word, six-paragraph essay** (*"What we are NOT
selling you is the right to your own words"* · *"spin, in front of the exact people you are trying to impress, is what
would end you"* · *"OSLO does not produce those, at any price."*). **That was the decision log pasted into a dialog.**
It is now **27 words**, and it still does the three things MON-04 requires: **names the limit hit · names the tier that
relieves it · offers the resolutions.**

**The standing prompt FOOTER is deleted from product copy.** It carried 36 words of owner-reassurance on *every*
prompt, forever. The promises it recited are **behaviour** and are still guarded.

## D164 — the Readout is a DOCUMENT. It gets the artifact editor.

**One editor. Two documents.** The readout's stack of textareas (with a `**bold**` / `- bullet` markdown round-trip)
is **retired**. The PM now edits the **rendered memo, in place**, with the **same editor as a plan artifact**
(D066–D085): inline rich text · the selection toolbar · **⌘B/I/U** · **undo/redo** · the **"/" slash menu** ·
**⌘F find/replace** · the link popover · sanitised paste · the block model + drag-reorder · the same keyboard
behaviour. **Bold, lists and the decisions table survive editing intact.**

**How, without forking the editor:** the editor stops addressing `#artdoc` by name and addresses **whichever document
it is driving** — `_EDIT_HOST` (`'artdoc'` | `'rptEd'`), `_edDoc()`, `_edKey()`. Every `getElementById('artdoc')`
inside the editor is now `_edDoc()`. The find bar moved out of `#artCenter` to body level, because a bar nailed inside
the artifact pane was **structurally unable** to reach the readout.

**Deliberately NOT shared — these are ARTIFACT semantics, not editor semantics:**
- **epistemic provenance chips** (*From OSLO / Confirmed by you*) — they would put **OSLO vocabulary into a document
  that forbids it** (D149);
- the **weakness stepper** — a memo has no issues;
- **artifact versioning + History events** — a readout is not a plan artifact;
- ⛔ **the reanalysis commit** — **a readout PACKAGES; it never PRODUCES** (D146). Editing a readout runs **no
  analysis**, spends no meter, and does not move the read by a degree.

All five are gated at their own function heads by `_edIsArtifact()`, and the single structural-edit choke point
(`_commitFromStructuralEdit()`) returns early on the readout host.

**Constraints preserved and guarded:** PM sections stay **PM-owned and byte-verbatim** (D152/D155) · OSLO-authored
sections stay reliability-qualified and free of OSLO vocabulary (D149) · **tailor the ask, never the read** (D145 —
§1–§5 + appendix byte-identical across recipients) · **editing free on every tier; the gate is REUSE** (D154) · frame
by outcome, never forecast (D151) · the gentle non-blocking note (D155) · the reading surface stays sacred (D160).

**Three new guards** — `_assertReadoutUsesArtifactEditor()` · `_assertReadoutEditorProducesNothing()` ·
`_assertReadoutEditorRestoresHost()` — and **four existing guards had their source lists extended** so they cover the
new edit path and cannot pass vacuously (`_assertEditFreeOnEveryTier` · `_assertForecastNoteNeverBlocks` ·
`_assertOsloNeverRewritesPMProse` · `_assertReportPackagesNeverProduces`).


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
▸ Recommendations · 3
▸ Clarification · Has the venue confirmed Wi-Fi for 500+ concurrent…
▸ Comments · 0
▸ Reviews · 1 · 1 awaiting        (only when reviews exist)
  [⤴ Share for review] ⓘ   [✦ Discuss with OSLO]
```

Row state persists **while the panel is open** (a re-render from `selectPath` / `addComment` must not collapse what the user opened) and **resets on close** — a fresh open is a fresh, minimal read.

## D162c — the three affordance defects, fixed

| Defect (owner-reported) | Fix |
|---|---|
| **Evidence looked FLAT** — it had a `▸` but no hover state, no cursor change, no affordance. The user could not tell it expanded. | The `.ip-rowh` component: **pointer cursor · hover background · chevron that rotates on expand · visible count · focus ring**. Every secondary section now uses it — one component, not five bespoke headers. |
| **Clarification defaulted EXPANDED**, with a large empty textarea dominating the panel. **A big empty textarea shouts "do work now"** at a user who came to *read*. | **Default MINIMIZED.** The row names what OSLO needs (question preview, truncated to 54 chars); the input appears on expand. *"Answer in chat →"* stays inside the expanded state. The **primary "Answer" button** (when OSLO has no recommendation) opens the row and drops the caret in it. |
| **Share for review carried three lines of explanation.** | **Just the button.** The contract lives on an **ⓘ**. The prime-candidate hint and the CR-2 counter are **deleted**. |

## D162d — cascaded

- **Recommendation panel** (the `.ip-rec` block): the *"Applying drafts the change into your plan. Discussing changes nothing."* note and the *"Recommendations live only inside the issue"* rationale → **ⓘ / button tooltips**. *"Possible resolution paths"* → **"Other paths"**. *"— recorded as your chosen approach"* → dropped (the **Confirmed by you** tag already says it).
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


> ## ⚠️ AMENDED 2026-07-11 — the tier ladder was RATIFIED all along
> `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` carries **owner-confirmed rows for every tier**. Five values this slice rendered as *"owner-TBD"* are ratified: **Basic price $12/mo · Basic chat 75/day · Basic deep-runs 6/day · envelope Free ~20 docs/50k words + Basic ~40/100k · the monthly gate = the token governor (Free 4M · Basic 10M — "the binding governor")**. One value marked RATIFIED is **not**: the **collaborator seat caps** (§4c has no seat row below Team). Superseded passages below are marked in place. Full detail: `tier-definitions-census.md`.


Cumulative Slices 1–10. A criterion passes only if it holds in the single openable `prototype.html`.
**All boxes below are verified by the automated runtime suite: 55/55 behavioural + 24/24 non-regression, 0 console errors.**

## D134 — the adopted numbers (canon decides; the build cites)
- [x] `FREE_ACTIVE_CAP = 1`, **`BASIC_PROJECT_CAP = 3`** — cited to **UP-3**, with the withdrawal of the invented `10` recorded at the code site.
- [x] **AMENDED —** daily fixes **5 / 20** · daily chat **Free 20 / Basic 75** · deep runs **Free 2 / Basic 6** — **all four Basic values ratified in §4c** (owner-confirmed 2026-06-05), all cited at the site. ~~*Basic chat/deep unset*~~.
- [x] **AMENDED — the monthly token governor (§4c) is wired as the binding gate:** Free **4M** · Basic **10M** · Pro 25M · Team 50M/seat. §4c: *"the binding governor."*
- [x] **AMENDED — the project-size envelope is ratified and wired:** Free **~20 docs / ~50k words** · Basic **~40 / ~100k** (§4b CHG-056 · §4c).
- [x] Export: **Free = PDF only** (MON-01/SHARE-04).
- [x] **AMENDED — Seats 3 / 10 render as `recommendation — not ratified`.** §4c has **no seat row** for Free/Basic/Pro; Team is priced **per seat**, and **Basic = 10 cannibalises it**. **No replacement number invented — escalated.** **Viewers unlimited · reviewers free/unmetered** (ratified, unchanged).
- [x] **No copy string hard-codes a tier number.** Every displayed number is painted from the constant.

## D135 — plans / upgrade surface
- [x] Real, reversible, **simulated** Free→Basic upgrade; every touchpoint says it is simulated and that billing is out of scope (T-4).
- [x] **AMENDED — `BASIC_PRICE = 12`** → **$12/mo, RATIFIED** (§4c, owner-confirmed 2026-06-05; DL-074 §4). Painted from the constant at every CTA. ~~*renders as an explicit owner-TBD*~~ — it was never a TBD.
- [x] **AMENDED — the FULL 5-TIER LADDER is shown:** Free · Basic (**$12**) · Pro (**~$39**) · Team (**~$99–149/seat**) · Enterprise (custom). **Basic purchasable in Alpha; Pro/Team/Enterprise = the forward ladder — priced, and NOT purchasable in R1, with no Buy button on any of them.**
- [x] **AMENDED — the value story is explicit:** Basic = **capacity** (same models as Free) · Pro = **model quality + execution & program support** · Team/Enterprise = **governance & portfolio, per seat**. Basic+Pro = individual; Team+Enterprise = the org sale.
- [x] **AMENDED — overage (DL-074):** paid tiers only, per Deep Pass, **user-set spend cap + threshold alerts**. **NO Free purchase path** — `_assertNoFreePurchasePath()` proves it.

## D136 — honest counters
- [x] Live counters for **projects · daily fixes · daily chat · deep runs/day**, with **real values**.
- [x] **Real reset times** — daily meters: *"midnight — in Xh Ym"*; allocation: calendar month (X-3).
- [x] **AMENDED — the MONTHLY TOKEN GOVERNOR is the headline meter and the binding gate:** Free **4M** · Basic **10M** (§4c, *"the binding governor"*), with a **visible meter** and the **real** calendar-month reset date (DL-074 §5). The daily caps are labelled **burst-smoothers, not the gate**. ~~*Extended-Analysis budget · size envelope · monthly budget gate render visibly unset*~~ — all three were **ratified**. Genuinely unset values (coalescing window · Free CRR cap · global prompt cap · billing rail) **still render unset**.
- [x] **AMENDED — seat caps render as `recommendation — not ratified`** (the ONE undefined ladder dimension). `_assertSeatCapsFlagged()` fails loudly if anyone re-marks them canon.
- [x] **No countdown, no urgency colour, no red counter, no "only N left"** anywhere in the file.

## D137 — UP-1…UP-8 (ratified taxonomy, implemented exactly)
- [x] **UP-1** at the fix cap → friction → **Basic** → *"You've used today's fixes — Basic gives you 20/day."* · once/day.
- [x] **UP-2** at the chat cap → friction → Basic · once/day. **The typed question is not destroyed.**
- [x] **UP-3** on the 2nd-project attempt → *"Free includes 1 active project — Basic gives you 3."* · **immediate, no cooldown.**
- [x] **UP-4** envelope → partial orientation + honest disclosure → **fires WITH the disclosure, ONE surface** (no second modal).
- [x] **UP-5** at the deep-run cap → friction → Basic · once/day · resolution **"keep the last analysis"**.
- [x] **AMENDED — UP-6** monthly budget gate → once/month, and it **enforces the real, ratified threshold** (the monthly token governor). It names what a limit never touches, and — on Free — that **there is nothing to buy but the upgrade**. ~~*enforces nothing, because the threshold is unset*~~.
- [x] **UP-7** at a value peak → **value** → **Pro** (continuous monitoring, forward capability) · rare · **says it is not for sale.**
- [x] **UP-8** first MRI → **value** → celebrate · **no hard sell** · once, first project.
- [x] **Standing rule:** no persistent upgrade wallpaper (the sidebar CTA is gone).
- [x] **Standing rule:** every prompt names **the specific limit** AND **the specific tier** — asserted at runtime (`_assertNoGenericUpgradeCopy`). **No generic "upgrade" copy exists in the file.**
- [x] **Guard:** never fires before first value (first MRI) — verified: no prompt fires pre-MRI.
- [x] **Guard:** never interrupts an active Fast/Deep pass — verified.
- [x] **Guard:** per-trigger cooldown **+ a global per-day cap** (the guard is enforced; **the number renders unset**).

## D138 — the limit-reached interaction rule, at EVERY cap
- [x] **Apply this fix** stays **enabled** at the cap → the attempt prompts (UP-1) → the plan is untouched.
- [x] **Chat send** stays **enabled** → the attempt prompts (UP-2).
- [x] **Create project** stays **enabled** → the attempt prompts (UP-3) → resolutions **upgrade · archive** (reversible — DL-058).
- [x] **Export formats** stay **enabled** (Slice 9 shipped them `disabled` — **corrected**) → the attempt prompts (UP-EXPORT) → **free PDF resolution first**.
- [x] **SEATS — the Slice-9 correction:** the seat cap **prompts, it does not block**. The Add control is never disabled; the attempt yields a **tier-named prompt with resolutions as buttons** — **Add as Viewer (no seat, unlimited)** first, upgrade second.
- [x] **NONE** of these controls is disabled or hidden — asserted against the real DOM at boot (`_assertNoDisabledLimitAffordances`).
- [x] **Never a raw error** — every gate produces the value-framed prompt.

## D139 — envelope exceeded → partial orientation
- [x] A **partial** analysis is delivered with an **honest disclosure**: OSLO says it only read part of the plan, and that every figure describes only that part.
- [x] The disclosure and UP-4 are **ONE notice on ONE surface** — never two competing notices.
- [x] The disclosure ships **regardless of upgrade** — it is an epistemic-honesty requirement first.
- [x] **AMENDED — the envelope renders its RATIFIED size:** Free **~20 docs / ~50k words**, Basic **~40 / ~100k** (§4b CHG-056 · §4c). ~~*"~100k words" (illustrative in canon) never appears*~~ — **it is Basic's envelope, and it appears.** The disclosure also states the ratified graceful-degradation fact: the project is **never rejected**.

## D140 — the census
- [x] **AMENDED — `tier-definitions-census.md`: 53 values · 46 RATIFIED (cited) · 3 RECOMMENDATION (labelled) · 4 UNSET** → **6 genuinely open decisions** (seats · coalescing window · Free CRR cap · global prompt cap · CR-2-vs-governor · billing rail). ~~*32 values · 21 RATIFIED · 11 UNSET*~~. The census also records the **root cause**: the values live in the **engineering zone**, and 18 product documents cite a Tier Definitions document that does not exist.
- [x] The same census renders **in-product** (Usage & limits), so the user sees the holes too.

## The hard guardrails (all still binding, all verified)
- [x] **Never meter the epistemic record** — artifacts uncapped, History never expires or truncates (D128 P1). Asserted.
- [x] **Never sell safety** — link revocation + purpose-scoped expiry free on every tier (D128 P2).
- [x] **Evidence-seeking never bounded (CR-2)** — 0 invites + a brand-new reviewer → **the review request still sends**; an evidence-driven Extended Analysis runs **even at the deep-run cap**. Asserted.
- [x] **Never present a PHASE limit as a TIER upsell** (D124) — the phase message carries **no upgrade CTA**.
- [x] **No eviction on downgrade** (D132) — verified: Basic→Free removes nobody.
- [x] **Advisory-only** (D001) — chat **never upgrades, purchases, or lifts a limit**; it explains and hands back.
- [x] **No fabricated scarcity, no dark patterns** — asserted (`_assertNoFabricatedNumbers`).

## Non-regression (Slices 1–9)
- [x] 24/24: activation · intake · Fast Pass · Overview · Attention map · Artifact workspace · Issues · Issue panel · History · trend · Workspace home · Settings · notifications · **dark default (D127)** · Share · Export + disclaimer · comments · CRR + reviewer view · D133 · D132 · D124 · D128 · advisory-only chat.
- [x] **Bonus fix:** a **real latent Slice-9 defect** found by the harness — typing a brand-new reviewer's email into the CRR dialog wiped the input on every keystroke (`renderCrr` rebuilt it). That broke the **exact path CR-2 exists to protect** (asking someone who has never used OSLO for their read). Fixed: value + caret preserved.


---

# ⬛ SUCCESS CRITERIA ADDED BY DL-103 (2026-07-12) — all verified

| # | Criterion | Verified |
|---|---|---|
| 1 | `node --check` on the extracted script | ✅ PASS |
| 2 | jsdom **without** `runScripts` → healthy body (**31**; ⚠️ **the Reports modal is GONE** — D148 makes Reports a pane inside `.body`) | ✅ PASS |
| 3 | **26/26 boot assertions pass** (`window._S10`) — the 9 DL-103 guards **+ the 10 reporting guards** (D145 · D148–D154) | ✅ PASS |
| 4 | **Chat is uncapped** — `_limit('chat') === null` on every tier; no gate in `sendChat` | ✅ PASS |
| 5 | **The monthly analysis budget is the single surfaced limit** — in **analyses**, marked **pending re-derivation**, enforcing **nothing** | ✅ PASS |
| 6 | **No token figure** is rendered as a product limit anywhere | ✅ PASS |
| 7 | At the assisted-apply cap: **the recommendation is fully visible**, the Apply button **stays enabled**, and **manual editing is offered first, free** | ✅ PASS |
| 8 | **"Update now" works on Free** — no tier check exists; it draws only on the monthly budget | ✅ PASS |
| 9 | ⚠️ **SUPERSEDED by D143, then rebuilt by D148–D154.** Not *"7 report cards"*, and no longer a *"§1–§5 spine"* either. See the reporting block below. | — |
| 10 | **Free retains a shareable artifact** — and under D154 it is **the whole memo, fully editable**, as a PDF | ✅ PASS |
| 11 | **No tier-keyed model-quality copy** on any selling surface | ✅ PASS |
| 12 | **No priority-queue / latency lever**; **no outcome-based pricing copy** | ✅ PASS |
| 13 | **Downgrade never removes** History · issues · artifacts · chat · the read | ✅ PASS |
| 14 | **Slices 1–9 non-regression** — Overview · Attention · Artifacts · Issues · History · Workspace · Share/Export/CRR · chat all intact; dark default (D127) held | ✅ PASS |
| 15 | **Zero console errors** across boot + the full behavioural run | ✅ PASS |

---

# ⬛ SUCCESS CRITERIA — REPORTING (M4), **D148–D154 · REBUILT** (2026-07-12) — all verified

> The previous build was **rejected**: a modal, and a report that described OSLO's epistemic state instead of speaking to its reader. These criteria replace the D143–D147 set.

| # | Criterion | Verified |
|---|---|---|
| M4-1 | `node --check` on the extracted script | ✅ PASS |
| M4-2 | jsdom **without** `runScripts` → healthy body (**31** children; the Reports modal is gone, the Reports **pane** is inside `.body`) | ✅ PASS |
| M4-3 | **26/26 boot assertions pass** (`window._S10`) — 16 standing + **10 reporting guards** | ✅ PASS |
| M4-4 | **D148 — Reports is a WORKSPACE**, reachable exactly like Overview / Issues / History (`showView('reports')` → `#pane-reports.active`, sidebar `aria-current="page"`, crumb = *Readout*). **`#reportsScrim` no longer exists.** | ✅ PASS |
| M4-5 | **D149 — ZERO OSLO vocabulary in the report body.** Every `[data-sec]` in `#rptDoc` swept against `REPORT_OSLO_VOCAB` (word-boundary, no denial exemption) → **clean** | ✅ PASS |
| M4-6 | **D151 — no forecast/probability/likelihood language** anywhere in the body (`REPORT_FORECAST_WORDS`) → **clean** | ✅ PASS |
| M4-7 | **D150 — seven sections, fixed order**, `summary,changes,risks,assumptions,plan,decisions,appendix` — **risks BEFORE assumptions** | ✅ PASS |
| M4-8 | **D151 — every risk carries BOTH altitudes** (*For the plan* + *For the goal*) — 5/5 | ✅ PASS |
| M4-9 | **D152 — the plan of action is PM-voiced** (first person, never names OSLO, always carries an edit affordance) | ✅ PASS |
| M4-10 | **D153 — the disclaimer is on the PACKAGE** (`#rptPkg`, `snap.cover.disclaimer`) and **not in the body**; the **currency marker IS in the body** as plain attribution (*"plan as of 12 July"*) | ✅ PASS |
| M4-11 | **D154 — editing works on FREE** (`_reportEditAllowed()` is `true` on every tier; no tier check, no `fireUP` in the edit path) | ✅ PASS |
| M4-12 | **D154 — Free persists NOTHING** (no `rptEdits` key written); **Basic persists and re-applies** the wording next week (`simNextWeek()`) | ✅ PASS |
| M4-13 | **D145 — tailor the ask, never the read.** Changing the recipient changes **only** `[data-sec="decisions"]` — proven behaviourally (byte-diff of every section across all four recipients) **and** structurally (the read-builders cannot see the recipient) | ✅ PASS |
| M4-14 | **Packages, never produces** — `genReport()` moved `TREND`, the governor and the usage meter by **zero** | ✅ PASS |
| M4-15 | **A scheduled send re-checks currency** and labels a stale package **"previous analysis"** | ✅ PASS |
| M4-16 | **P1 (DL-104 §5)** — no health / readiness / RAG / probability framing anywhere on the surface | ✅ PASS |
| M4-17 | **Slices 1–9 + the rest of Slice 10 non-regression** — all six views switch; Overview, Attention, Artifacts, Issues, History, chat, share/export/CRR intact; dark default held; **zero console errors** on boot and through the full behavioural run | ✅ PASS |

**Pre-existing observation (NOT a regression, and NOT caused by this rebuild):** `_assertNoGenericUpgradeCopy()` (MON-04) returns **false while `TIER==='basic'`**, because **UP-6**'s body only names *"Basic"* in its Free-tier branch. Reproduced on a pristine boot with `setTier('basic')` and **no Reports interaction at all**. Logged in `open-items.md`.

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157 · D158**

- [x] **D158 — a pristine boot on `TIER='basic'` produces ZERO console errors.** `window._S10` = **28 assertions, all pass**, on **Free and Basic**. The MON-04 guard now demands the relieving tier's name **only when the user is beneath it** — a fix to the **guard**, not a relaxation of MON-04 (it still bites on Free).
- [x] **D155 — forecast/probability/RAG/health language in the PM's OWN prose surfaces a gentle advisory beside that section.** Same vocabulary as the guards; **advisory, not failure.**
- [x] **D155 — the note NEVER blocks.** Send and export always work. **The send path cannot see the note.** `_assertForecastNoteNeverBlocks()`.
- [x] **D155 — the note NEVER edits the PM's words.** Every `data-pm="1"` section renders **byte-verbatim**. `_assertOsloNeverRewritesPMProse()`.
- [x] **D155 — the note is DISMISSIBLE, always.** The PM dismisses it and sends anyway.
- [x] **D155 — the PM's prose never turns the console red.** `_assertDisclaimerOnPackageNotInBody()` now exempts `data-pm="1"`, consistent with D149/D151/D152.
- [x] **D156 — the `To:` line stays**; the D145 guard stays **section-scoped** (§1–§4 + §5 + appendix byte-identical; only §6 varies). Recorded in code so nobody "fixes" it.
- [x] **D157 — risks capped at 5**, highest impact first; the appendix walks **every** workstream and is **explicitly skippable**. ⬜ **The truncation rule is an M4 spec item and is NOT invented.**
- [x] **No regressions.** `node --check` PASS · jsdom (no `runScripts`) body child count **31** · every Slice 1–9 guard and the rest of Slice 10 still pass on both tiers.

---

# ⬛ AMENDED 2026-07-12 — **D165 · acceptance criteria**

| # | Criterion | Result |
|---|---|---|
| **SC-D165-1** | OSLO's opening turn on an issue is **~40 words** | **33** (prose body) · 45 incl. 1 action + 3 chips · **was 302** |
| **SC-D165-2** | The opening ends with **2–3 contextual next moves** | 3 chips, on every issue |
| **SC-D165-3** | Evidence · options · recommendation · reliability arrive **only when asked**, one per turn | 31 · 25 · 20 · 27 words respectively; each ends in a handoff |
| **SC-D165-4** | The four action cards and their subtitles are **cut**; ONE action, contextual | 1 action per turn · **0** `.ca-cons` anywhere |
| **SC-D165-5** | Composer chips **vanish** once a conversation is underway | 5 → **0**. Never two competing sets. |
| **SC-D165-6** | A new context inserts a **visible divider** | `.chat-div` per context change; none on a repeat of the same context |
| **SC-D165-7** | The clarification form is **collapsed** by default | `display:none` on `.cc-body`; the one-line head expands it |
| **SC-D165-8** | Epistemic honesty preserved as **ONE line** | *"I inferred this — it isn't in your inputs."* Same trigger as D109. |
| **SC-D165-9** | Reliability basis available **on request** | "How sure are you?" → Coverage · Evidence · How assessable |
| **SC-D165-10** | Chat **never mutates** | `chatNeverMutates` — 12-question battery, whole-model snapshot |
| **SC-D165-11** | Chat-answered clarification ⇒ **byte-identical** History entry | verified by diffing both paths — identical |
| **SC-D165-12** | 37 boot assertions pass on Free × Basic × notes-OFF × notes-ON | **37/37 × 4** · **0 console errors** |

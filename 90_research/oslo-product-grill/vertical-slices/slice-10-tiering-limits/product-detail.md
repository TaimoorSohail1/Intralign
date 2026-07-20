# Slice 10 — Tiering & Limits · Product Detail  ·  **FINAL SLICE**

# ⚠️⚠️ RECONCILED 2026-07-20 — DL-143 → DL-156 LANDED AFTER THIS DOC. READ THE DELTA FIRST.

**This doc was last reconciled 2026-07-17 (through DL-124).** DL-143 → DL-156 landed afterward — the **reports trio + Summary/Full depth + export** (DL-143/144), the **execution-ready planning direction** (DL-145 identity; DL-146–150 the authored task tree · task-altitude issues · computed critical path · the eighth "Full plan" consolidated view; DL-151 the structured Asana export), and the **Overview two-beat journey** (DL-152–156: Understand → ⟮Optimize: Validate · Improve⟯ → Execute, persistent read, beat-aware Start here). These are **built into the frozen prototype** (`prototype.html`, md5 **a327d702** · boot 157/157) but **not folded into this doc**. On those surfaces, where this doc disagrees with the **frozen prototype / the DLs**, they win. See `RECONCILIATION-2026-07-20-DL143-156.md` (same folder) for the full delta and `../../RELEASE_1_BUILD_SPEC.md` for the R1 freeze marker (zero open R1 items).


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


Cumulative Slices 1–10. Plain JS · localStorage · fake data · simulated AI. No backend, no auth, no real AI, **no billing** (T-4).

> ## The governing rule of this slice
> **Canon decides. The build adopts and cites. NEVER invent a tier number.**
>
> An earlier AI pass proposed **"Basic = 10 projects"**. Ratified canon (**UP-3**, and **§4c**) says **Basic = 3**. The invented number reached an open PR and had to be **withdrawn on the record** (DL-102 Correction #3). Every number in this slice is marked **RATIFIED (with citation)**, **RECOMMENDATION (carried, labelled, not canon)**, or **UNSET (owner decision required)** — at the code site, in the product, and in `tier-definitions-census.md`. *"A sensible default for now"* is not a fourth state: it is exactly how the 10 got here.

> ## ⚠️ AMENDED 2026-07-11 — THE CORRECTION OF RECORD
> **The tier ladder was ratified all along — in the ENGINEERING zone.**
> `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` carries **owner-confirmed rows for every tier** (Free/Basic 2026-06-05; Pro/Team/Enterprise via **DL-074**, 2026-06-19). This slice's first pass scanned only `10_product/` and `00_owner/` — the product-grill scope — and therefore rendered **five ratified values as "owner-TBD"**:
>
> | Was rendered | Is actually (§4c) |
> |---|---|
> | Basic price *"owner-TBD"* | **$12/mo** |
> | Basic chat/day *"unset"* | **75/day** |
> | Basic deep runs/day *"unset"* | **6/day** (a **burst ceiling**, not the gate) |
> | Size envelope *"illustrative, not ratified"* | **Free ~20 docs/50k words · Basic ~40/100k** |
> | Monthly gate *"threshold unset; enforces nothing"* | **The monthly token governor** — Free **4M** · Basic **10M** ("the binding governor") |
>
> **And one value marked RATIFIED is not:** the **collaborator seat caps** (§4c has **no seat row** below Team).
>
> **The root cause is not missing values. It is a missing product-authoritative surface.** 18 product documents cite a `RELEASE_1_TIER_DEFINITIONS_V1` that does not exist, so a product-scoped reader never finds the numbers — and a model that cannot find a number invents one. **The document must be written to CONSOLIDATE AND NAME what is already ratified, not to decide anything new.**
> Superseded passages below are marked in place. Full detail: `tier-definitions-census.md`.
>
> **The one-line principle this whole slice serves (D126):**
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

---

## D134 — The adopted numbers (cited, not re-decided)

| Value | Setting | Source |
|---|---|---|
| **Price** | Free **$0** · **Basic $12/mo** · Pro ~$39 · Team ~$99–149 **/seat** · Enterprise custom | ✅ **§4c** (owner-confirmed 2026-06-05) · **DL-074 §4** |
| Active projects | Free **1** · Basic **3** · Pro **10** | **§4c · UP-3** |
| **Project-size envelope** | Free **~20 docs / ~50k words** · Basic **~40 / ~100k** · Pro ~80 / ~200k · Team ~150 / ~400k | ✅ **§4b CHG-056 · §4c** |
| Suggested fixes / day | Free **5** · Basic **20** · Pro 50 | **§4c · MON-02 / UP-1** |
| Chat messages / day | Free **20** · Basic **75** · Pro 200 | ✅ **§4c** *(was rendered unset)* |
| Extended (deep) runs / day | Free **2** · Basic **6** · Pro 15 — **burst ceilings, NOT the gate** | ✅ **§4c** *(was rendered unset)* |
| **Monthly token governor — THE BINDING LIMIT** | Free **4M** · Basic **10M** · Pro 25M · Team 50M/seat | ✅ **§4c** — *"the binding governor"* |
| **Model routing — the value story** | Free/Basic **nano+mini (same class)** · Pro **+ full-quality fallback** · Team **premium** | ✅ **§4c** — *Basic sells **capacity**; Pro adds **model quality*** |
| **Overage** | **paid tiers only** — per Deep Pass, user-set spend cap, threshold alerts. **Free has NO purchase path.** | ✅ **DL-074 §2/§3/§5** |
| Export | Free = **PDF only** | **MON-01 / SHARE-04 / D112** |
| Free scope | full Workspace · Confidence · CAF · MRI · Issues · Recommendations · Sharing · Comments · **CRR** | **MON-01 + CHG-061** |
| **Collaborator seats** | Free **3** · Basic **10** — ⚠️ **RECOMMENDATION, NOT RATIFIED**; Viewers **unlimited**; reviewers **free/unmetered** | ⚠️ **§4c has NO seat row below Team.** D129 X-1 / DL-102 E is a recommendation, and **Basic = 10 cannibalises a ~$99–149/seat Team.** Escalated; no replacement invented. |

*Superseded rows (kept for the record): ~~Chat/day Basic **unset**~~ · ~~Deep runs/day Basic **unset**~~ · ~~Collaborator seats **RATIFIED**~~. See the amendment banner above.*

**The correction, in code:** `BASIC_PROJECT_CAP = 3` — cited to UP-3, with the withdrawal of the invented 10 recorded at the site. Every copy string that previously hard-coded "10 projects" is now **painted from the constant** (`renderTierChrome`, the UP-3 modal, the Plans surface), so a copy line can never drift from the ratified number again. That drift is *how* the invented number survived.

## D135 — Plans / upgrade surface

- **Free → Basic is a real, reversible, simulated upgrade** (`setTier`). Tier gating is **live in Alpha** (D123).
- ~~**`BASIC_PRICE = null`.** The price renders as an explicit owner-TBD everywhere it would appear (T-3).~~ **AMENDED: `BASIC_PRICE = 12`.** The price is **RATIFIED** — **$12/mo**, §4c, owner-confirmed 2026-06-05, reaffirmed by DL-074 §4. It is painted from the constant at every CTA. *D129 T-3 ("the price is the owner's to set") is **superseded by the owner having set it**.* What remains out of scope is the **billing rail** (T-4) — the upgrade is simulated and says so.
- **AMENDED — the plans surface shows the FULL 5-TIER LADDER.** ~~Pro is named once, in prose, with no price.~~ **Free · Basic ($12) · Pro (~$39) · Team (~$99–149/seat) · Enterprise (custom).** **Basic is purchasable in Alpha; Pro/Team/Enterprise are the forward ladder — shown, priced, and NOT purchasable in R1, with no Buy button on any of them.** A "coming soon" with a Buy attached is a pre-order, and OSLO does not take pre-orders. *"We have not decided" and "we have decided and are not selling it yet" are different sentences, and only one of them was ever true.*
- **AMENDED — the value story is stated, not implied.** **Basic = capacity** (the same models as Free — §4c: *"capacity is the differentiator"*). **Pro = model quality + execution & program support.** **Team/Enterprise = governance & portfolio, per seat.** **Basic + Pro is the individual motion; Team + Enterprise is the org sale** (owner clarification, 2026-07-11). OSLO explicitly tells the user Basic does **not** think better than Free — implying otherwise is how software lies about itself.
- **AMENDED — overage (DL-074, ratified).** Paid tiers may buy **metered per-Deep-Pass overage** above the envelope, with a **visible meter**, a **spend cap the user sets**, and **threshold alerts** — *no silent overspend, no bill shock*. **Free has NO purchase path** (DL-074 §3: *"Free converts via upgrade"*), and `_assertNoFreePurchasePath()` fails loudly if anyone ever builds one.
- **What Basic never sells** (stated on the surface): the epistemic record (artifacts, History — D128 P1), safety (link revocation / purpose-scoped expiry — D128 P2), evidence-seeking (review requests — CR-2), or passage past a **phase** limit (D124).

## D136 — Honest counters

**Surface:** *Usage & limits* (`openLimits()`), reached from the sidebar plan chip (which reads **"Your plan"**, not "Upgrade" — see MON-04 below). Also mirrored in Settings › Subscription.

| Meter | Value | Reset |
|---|---|---|
| Active projects | real (`_activeProjects()` / `_projectCap()`) | n/a (scope) |
| Suggested fixes today | real | **calendar day** — "midnight — in Xh Ym" |
| Chat questions today | real | calendar day |
| Extended Analyses today | real | calendar day |
| **Extended Analyses from evidence** | real, **uncapped**, shown in its own lane | never — CR-2 |
| Collaborator seats | real | n/a (scope) |
| Artifacts · History | **∞** | never — D128 P1 |
| Invite allocation | real | **calendar month** (X-3) — "resets 1 August" |

~~**Unset meters render unset.** Extended-Analysis budget, size envelope and the monthly budget gate show the **use** and say the **limit is unset**.~~

**AMENDED 2026-07-11 — the meters now carry the ratified numbers, and the MONTHLY GOVERNOR is the headline meter.**
- **The monthly analysis budget is shown first**, labelled **"the limit that actually gates"** — Free **4M** · Basic **10M** tokens (§4c: *"the binding governor"*), with the **real** calendar-month reset date. **The daily caps are labelled for what §4c says they are: burst-smoothers, not the gate.** This is DL-074 §5's *visible meter*, and it is the honest answer to "how much have I got left?"
- **The seat meter renders "recommendation — not ratified"** — the one number in the ladder canon has not set.
- **Still unset, still rendering unset:** the coalescing window (OD-10), the Free CRR cap, the global prompt cap, the billing rail.
- Unchanged: no invented denominators, **no countdown, no urgency colour, no "only 1 left!"** — a counter is a fact about your plan, not a sales instrument.

## D137 — Upgrade prompts (UP-1…UP-8, MON-04)

One table (`UPROMPTS`), one fire path (`fireUP`), zero generic prompts.

| # | Trigger | Class | Target | Copy (ratified) | Cadence | Resolutions |
|---|---|---|---|---|---|---|
| **UP-1** | daily fix cap (5/day) | friction | Basic | "You've used today's fixes — **Basic** gives you 20/day." | at cap-hit; once/day | upgrade · **wait for the daily reset** |
| **UP-2** | daily chat cap (20/day) | friction | Basic | "More questions? **Basic** raises your daily chat limit." | at cap-hit; once/day | upgrade · wait for reset |
| **UP-3** | 2nd active project (Free = 1) | friction (high-intent) | Basic | "Free includes 1 active project — **Basic** gives you 3." | **immediate; no cooldown** | upgrade · **archive current** (reversible, frees the slot — DL-058) |
| **UP-4** | envelope exceeded → partial orientation | friction + **honest disclosure** | Basic | partial-analysis disclosure + the Basic note, **one notice** | with the disclosure; **ONE surface** | compare Basic · see what was/wasn't read |
| **UP-5** | deep-runs/day cap (2/day) | friction | Basic | "You've used today's Extended Analyses." | at cap-hit; once/day | upgrade · wait · **keep the last analysis** |
| **UP-6** | monthly budget gate | friction (soft) | Basic | "You've reached this month's analysis limit." | once/month; gentle | understood (**nothing was blocked**) · see limits · compare |
| **UP-7** | confidence improved / outcome achieved | **value** | **Pro** | "**Continuous monitoring** can protect this confidence over time." | at value peak; rare | acknowledge (**Pro is not purchasable**) |
| **UP-8** | first MRI delivered (activation) | **value** | — | celebrate; **no hard sell** | once, first project | none (a chat message, not a modal) |

**Standing rules (enforced, and asserted at runtime).**
- **No persistent upgrade wallpaper.** The sidebar chip said "Upgrade", permanently, on every screen in Slice 9 — the definition of wallpaper. It now reads **"Your plan"** and opens *Usage & limits*. The upgrade path is reached **from a prompt at the moment a limit is actually hit**, or from a comparison the user chose to open.
- **Every prompt is contextual, value-based, and names the specific limit hit AND the specific tier that relieves it.** `_assertNoGenericUpgradeCopy()` walks `UPROMPTS` at boot and fails loudly on any prompt that names no limit or no tier.

**Global guards (all four, in `fireUP`).**
1. **Never before first value** — first MRI delivered (`_markFirstValue()` in `afterOrientation()`). Before it, `fireUP` refuses *every* trigger.
2. **Never interrupt an active Fast/Deep pass** (`_passActive()` — the analyzing screen, `_S10_deepInFlight`, or an evidence run in flight).
3. **Per-trigger cooldown** — the ratified cadence per trigger.
4. **Global per-day cap** — the **guard is canon; the number is Calibration §4d config and was never set.** The product value renders **unset**; the prototype enforces the guard with a conservative local value, labelled as such everywhere. It errs toward **silence** — the right direction of error for a prompt.

## D138 — The limit-reached interaction rule (applies to EVERY cap)

**A limit-bearing affordance STAYS ENABLED. The *attempt* is gated (the simulated 422/429) and surfaces the matching prompt WITH resolutions. Never disabled, never hidden. Never a raw error.**

| Cap | Affordance | Behaviour | Prompt | Resolutions |
|---|---|---|---|---|
| Active project | Create project (Workspace) | stays enabled → attempt → prompt | **UP-3** | upgrade · archive current |
| Daily fix | **Apply this fix** (Issue Panel) | stays enabled → attempt → prompt | **UP-1** | upgrade · wait for reset |
| Daily chat | Chat send | stays enabled → attempt → prompt; **the typed question is not thrown away** | **UP-2** | upgrade · wait for reset |
| Deep runs/day | any user-initiated analysis update | the **edit still saves**; the **run** defers | **UP-5** | upgrade · wait · keep last analysis |
| Export format | Export dialog | **was `disabled` in Slice 9 — CORRECTED**; now live → attempt → prompt | **UP-EXPORT** | **export as PDF instead (free)** · upgrade |
| **Collaborator seat** | Invite / promote | **CORRECTS SLICE 9** — the attempt now yields a **tier-named prompt with resolutions as buttons**, free one first | **UP-SEAT** | **add as Viewer (no seat, unlimited)** · upgrade |

**Why this matters and is not a detail:** disabling the control **suppresses the highest-intent moment in the product** — the second a user *wants* more. It also replaces an honest disclosure with a dead end. And a prompt whose only button is *Buy* is a wall, not a disclosure: **every friction prompt here carries a free resolution wherever one exists, and lists it first.**

`_assertNoDisabledLimitAffordances()` walks the real DOM at boot and fails loudly if any limit-bearing control is disabled or hidden. (The Invite button's `disabled` state is form validation on an empty/invalid email — marked `data-validation` so the assertion can tell the two apart. **A limit may never disable a control; an invalid email may.**)

## D139 — Envelope exceeded → partial orientation (UP-4)

**This is an epistemic-honesty requirement first and a monetization surface second.** If OSLO only read part of the plan, it says so — plainly, immediately, and **whether or not anyone ever upgrades**. The disclosure would ship even if Basic did not exist.

- **ONE surface.** The disclosure **is** the prompt (`renderPartial()`); `fireUP('UP-4')` routes to it and **never opens a second modal**. A scary honesty banner plus a separate ad is a dark pattern assembled out of two honest parts.
- It states what is **true**: OSLO did not read all of the plan; every figure on the Overview (confidence, reliability, issues) describes **only the part it saw**; **there may be issues in the unread portion and OSLO cannot tell you what they are.**
- ~~**The envelope size is owner-TBD.** UP-4's "~100k words" is **illustrative in canon, not ratified** (D139).~~ **AMENDED: the envelope is RATIFIED.** §4b (CHG-056, owner-confirmed 2026-06-05): Free **~20 documents / ~50k words**. §4c Tier 2: Basic **~40 / ~100k** — *the "~100k words" is not an illustration; it **is** Basic's envelope.* The notice now names the real size, and adds the ratified graceful-degradation fact: **the project is never rejected** — OSLO reads what the envelope allows, says the read is partial, and keeps working (§4b). **A precise honest limit is a better disclosure than a vague one.**

## D148–D154 — REPORTING (M4), **REBUILT**: a workspace, and a memo that speaks to its reader

> **Owner rejected the previous build.** It was a **modal**, and the report was **too meta** — it described OSLO's epistemic state instead of speaking to its reader. **D148–D154 revise D144/D146/D147.** D143 (one composable readout) and D145 (tailor the ask, never the read) **stand**.

**D148 — Reports is a WORKSPACE, not a modal.** A peer view: Overview · Attention · Artifacts · Issues · History · **Readout**. Left, the live composer. Right, the readout **rendering as an actual document** — a page, not a form preview.

**D149 — THE GOVERNING WRITING RULE.**
> **The doctrine governs what the report may CLAIM. It must NEVER govern how the report SOUNDS.**

The old spine was **OSLO describing itself** — a section called *"How to read this"*, headings like *"What we don't know"* and *"What's limiting it."* **Struck.** The report is an **executive summary, written for its reader, in their language.** **ZERO OSLO vocabulary in the body** — enforced at runtime against the rendered DOM.

**The epistemic honesty appears as ordinary good writing.** The canonical technique, and the reason this works:

> *"80% support coverage is sufficient. **This came from the plan, not from Support.**"*

That is derived-vs-attested, in English. The sponsor now knows exactly how far to trust the number, **and no doctrine was spoken.** In the build: *"the 500-device figure came from our plan, not from The Grid"* · *"Not yet confirmed with The Grid"* · *"dates without owners are estimates, not commitments"* · *"the weak point here is people, not process."*

**D150 — Structure (fixed order).**

| § | Section | Why it is here |
|---|---|---|
| 1 | **Summary** | **Standalone.** A sponsor who reads only this has the whole picture. |
| 2 | **What's changed since previous week** | Live from the record. If nothing moved, **it says nothing moved** — no fabricated movement. |
| 3 | **Key risks** | **Before** the assumptions. A reader who stops reading must stop after the thing that could change the plan. |
| 4 | **Key assumptions** | What the plan rests on that is unconfirmed. **This is derived-vs-attested, rendered in English.** |
| 5 | **Plan of action** | **The PM's. First person. OSLO seeds; the PM owns.** |
| 6 | **Decisions needed from you** | decision · owner · what it unblocks. **The ONLY section addressed to the recipient** (D145). |
| 7 | **Appendix — per-workstream detail** | For the leads. The sponsor can skip it. |

**D151 — TWO ALTITUDES on every risk.** *For the plan* (deliverable impact) and *for the goal* (outcome impact). A delay is a schedule problem; a delay that means you miss the thing the project exists for is an outcome problem. **Same fact, different altitude** — and knowing which one you are looking at is what separates a senior read from a status update.

> ⚠️ **KNIFE-EDGE.** **Outcome impact = "does the plan, AS WRITTEN, still reach its stated intent?"** — a **structural claim about the plan** (Intent is part of the plan). **It is NOT "will this project succeed?"** — a **prediction**, which doctrine forbids, and which is the same P1 defect class as a health rating (DL-104 §5). **Frame BY outcome; never FORECAST the outcome.** Guarded: `_assertNoForecastLanguageInReport()`.

**D152 — The plan of action is the PM's, in the PM's first person.**
> **If that section reads as OSLO's plan, the PM becomes a PASSENGER IN THEIR OWN REPORT — and the status lever collapses.** The sponsor does not think *"my PM is sharp"*; they think *"the tool wrote this."*

OSLO **seeds** the steps from its own recommendations; **the PM edits and owns them.** It is also the only form compatible with **advisory-only**. **Everything above it is OSLO's read in plain English; the plan of action is the PM's judgment.**

**D153 — The disclaimer is a property of the PACKAGE, not a paragraph in the PROSE.** Canon (Export & Share-Out spec, ratified) requires every package to carry an explicit disclaimer — so it **stays**, on the **PDF cover / share-link metadata**, and comes **out of the memo body**. *A line saying "this isn't a forecast" invites the reader to wonder whether it was trying to be one.* The real protection is that the memo **never makes a forecast claim**. The **currency marker stays in the body** as plain attribution: *"DevNorth 2026 · plan as of 12 July · ‹name›"*.

**D154 — Editing is FREE. The gate is REUSE.**
- **Free** — full edit, every section, every week, **from scratch**. The whole seven-section memo, PDF export. **Nothing persists.**
- **Basic** — **the edits come back**: standing text, tone, section choices and boilerplate carry week to week and auto-apply. Plus the extra sections, branding, scheduling, all formats.

**Why gating the edit was rejected:** (1) it would make the PM **sign words they could not correct**, in the one artifact where their name is on the line; (2) it is a **commercial own-goal** — they would export to Word and edit there, **stripping the currency marker, the provenance and OSLO's fingerprint**, and killing the viral surface. **You would be gating your way out of your own loop.** The at-limit prompt therefore sells **persistence** and says the editing is free, out loud: *"Basic remembers your readout so you don't rebuild it every week."*

**Still binding, unchanged:** reliability-qualified in substance (never in jargon) · **never health / readiness / RAG / probability** (P1, DL-104 §5) · currency marker on every package, stale = **"previous analysis"** · **packages, never produces** · no fabricated completeness · **tailor the ask, never the read**.

## Chat (Slice-10 scope)

Chat **explains a limit and hands back to the surface that owns the action.** It **never upgrades, never purchases, and never lifts a limit** — every limit answer ends with that sentence, unprompted. Answers are computed from the **live meters** and the **ratified census**, never fabricated; an unset value is reported as unset (including the price).

- *"Which limit did I hit?"* → names it exactly, from live meters, with the real reset time; distinguishes **plan** (tier) from **phase** (invites) and says which one bit; closes with what is *never* limited (the record; evidence).
- *"What does my plan include?"* → **the full ratified ladder** (price, projects, envelope, daily caps, the **monthly governor**), the value story (*"Basic buys capacity, not a better answer"*), the **one** number nobody has decided (**seats**) marked as a recommendation, and — on Free — the plain statement that **there is nothing to buy except the upgrade** (DL-074 §3). ~~*the price marked **not set***~~ — **the price is $12/mo, and chat says so.**
- Suggested chips surface contextually (*"Which limit did I hit?"* appears only when a cap is actually hit).

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157 · D158**

## D155 — the PM's own prose: **a gentle note, never a block**

The vocabulary guard (**D149**) and the forecast guard (**D151**) **exempt the PM's own sections** (`data-pm="1"`) — **and they must**: policing the user's prose would be the tool writing the report again, which **D152** forbids. But the exemption left a real hole — **a PM can type *"we're 80% likely to hit 450"* into their own summary, and it ships under OSLO's mark, on OSLO's cover, carrying OSLO's disclaimer.** A forecast wearing OSLO's credibility.

**Resolution — the note.** When PM-authored prose contains the **same** forecast / probability / RAG / health vocabulary the guards apply to OSLO's own writing, OSLO surfaces an **unobtrusive advisory beside that section**:

> *"Heads up — this reads as a forecast. OSLO doesn't predict outcomes, and this goes out under OSLO's mark, on OSLO's cover. Your words are untouched and nothing is stopped."*

**Same vocabulary, opposite treatment: a FAILURE in OSLO's words, an ADVISORY in the PM's.**

| Binding property | Mechanism | Guard |
|---|---|---|
| **It NEVER blocks.** Send and export always work. | **The send path cannot SEE the note.** `genReport()` / `runScheduledReport()` may not reference `_pmForecastHits` / `RPT_NOTE_DISMISSED` / `_rptForecastNote`. | `_assertForecastNoteNeverBlocks()` (structural ×2 + behavioural) |
| **It NEVER edits the PM's words.** | The PM's stored text is rendered **verbatim**; the note is appended **beside** it. Only `saveReportSection()` / `resetReportSection()` may write `RPT_EDITS`. | `_assertOsloNeverRewritesPMProse()` (structural + byte-verbatim DOM check) |
| **It is DISMISSIBLE — always.** | `dismissForecastNote(k)`. Per-section, in-memory, never metered, never a monetization surface. Re-editing brings it back — new words, fresh advice. | `_assertForecastNoteNeverBlocks()` requires the dismiss control whenever a note renders |
| **It is ADVISORY, never a failure.** | Rendered in the UI. **No console error. No gate.** | — |

**Rationale (carried in a code comment at `REPORT_ADVISORY_WORDS`):** *blocking would be the tool overruling the human (violates advisory-only, D001); silence would be OSLO lending its name to a claim it forbids itself. The note is the only honest position.*

**Also fixed:** `_assertDisclaimerOnPackageNotInBody()` scanned the **whole** document body, so a PM typing *"probability of success"* into their own summary would trip a red console — OSLO grading the human's words. It now **exempts `data-pm="1"` sections**, consistent with D149/D151/D152.

## D156 — the `To:` line stays

**D145 forbids RE-FRAMING THE ASSESSMENT by audience. It does not forbid ADDRESSING the document.** A memo without a recipient is not a memo. The `To:` line stays; the D145 guard stays **section-scoped**: §1–§4 (plus §5 and the appendix) are **byte-identical across every recipient** — proven behaviourally *and* structurally (the read-builders cannot so much as **see** `RPT.to`) — and **only the decisions section (§6) varies**. Recorded in code comments at the render site **and** at the guard (`REPORT_TO_LINE_STAYS`), so nobody "fixes" it later. **One honest read. Many asks.**

## D157 — length

**Risks capped at 5, highest impact first** (`MEMO_RISK_CAP`). The **appendix walks every workstream and is explicitly skippable** (*"For the leads — skip this if you are not one"*), so **nothing is hidden**: the sponsor reads the five that matter; the leads read the lot. **A dump makes the PM look like a clerk — selection and framing is the value, not volume.**

⬜ **WHAT GETS CUT AND WHO DECIDES IS AN OPEN ITEM FOR THE M4 SPEC. NO TRUNCATION RULE IS INVENTED HERE.** `MEMO_RISK_CAP = 5` is labelled **illustrative, not a ratified product value**, in code and on the surface. See `open-items.md` **M4-O4**.

## D158 — defect fix: `_assertNoGenericUpgradeCopy()` (MON-04)

**A Basic user got a red console at boot.** Root cause: **UP-6 only names "Basic" in its Free branch** — correctly, because on Basic the honest copy is *"wait for the reset, or allow metered overage"* — while the guard demanded the relieving tier's name **unconditionally**.

**The guard was checking the wrong condition.** MON-04 requires a prompt to name **the specific tier that RELIEVES the limit** — which is only meaningful **when the user is BENEATH that tier**. At or above it, the honest copy is the *other* resolution, and demanding an upsell name there would be the very thing the rule forbids: selling for the sake of selling.

**Fix:** `TIER_ORDER` / `_tierRank()` / `_beneathTier()` — the tier name is required **only when the user is beneath the relieving tier**. The **limit name** and the **tier field** remain required **unconditionally**. ⚠️ **This is a fix to the GUARD, not a relaxation of MON-04** — below the relieving tier, every friction prompt must still name it.

---

# ⬛ AMENDED 2026-07-12 — **D165 · OSLO Chat: a conversation, not a wall**

**The rule.** OSLO's opening turn on an issue is **what it is · why it matters · one honest epistemic line**, and then
it **stops**. Every turn ends with **2–3 contextual next moves**. **Detail is PULLED, never pushed** — evidence,
options, the recommendation and the reliability basis each arrive **only when asked for**, one at a time, each itself
short and each ending in another handoff. **ONE IDEA PER TURN.**

**Opening issue reply: 302 words → 33 words** (prose body; 45 including the single action and the three chips).

**Actions.** The four resident action cards and their explanatory subtitles are **cut**. **One** action, the one that
fits the moment — after the recommendation, `Apply this fix →`. The rest are **reachable, not resident**.

**Suggestions.** In-message chips are the conversation's next moves. Composer chips are an **empty-state affordance
only** — they disappear once a conversation is underway. **Never both.**

**Preserved, compressed, never removed:** the epistemic line · the reliability basis (on request) · traceable
citations (on request) · the honest capability-scoped fallback · the byte-identical clarification path · and
**advisory-only**, absolutely: the chat never mutates, never selects a path, never resolves an issue.

---

# D172 — THE SCHEDULED SHARE · THE TIER RULE · THE GRANT · THE NAMES

| Clause | Decision | Implementation |
|---|---|---|
| **D172a** | **A scheduled readout is an automated SHARE, not an automated export.** *Nobody schedules a PDF onto their own disk.* | `runScheduledReport()` now cuts `_mkMemo(SHARE_CHANNEL, true, seq, **'shared'**)`, calls `_shareMemoGrant()` (a scoped read-only grant for the recipient) and pushes a **`share`** History event carrying the memo id — **D169 opens it.** **D147 still binds:** the currency re-check runs **at send time**, a stale read goes out **labelled "previous analysis"**, and **no analysis is ever run to freshen it.** Guard: `_assertScheduledSendIsAShare()` (structural + full state proof) · `_assertScheduledReportRechecksCurrency()`. |
| **D172b** | ⛔ **THE TIER RULE: the SHARE is free; the AUTOMATION is Basic.** | The tier check lives **at the toggle and nowhere else**: `toggleReportSchedule()` gates on `TIER` and fires `UP-REPORT {sched:true}` → title **"Basic sends it for you every Friday"**, body *"Sending is free on every plan… Basic is what remembers to."* (**27 words**, D163), resolutions **free-first: _Send it now_**. `sendMemo()` has **no tier branch and may never have one** (CHG-061). **Cron is not a viral primitive.** Same shape as **D154**. Guard: `_assertSchedulingIsTheGateNotTheShare()` — structural (the branch is in the toggle, not the send) **and** a Free state proof (*the automation refused; the share delivered — same account, same minute*) **and** the prompt's free resolution IS a send. |
| **D172c** | **A shared memo is a SCOPED, TOKEN-GRANTED, READ-ONLY view** — the **CRR reviewer grant's mechanism** (DL-102 A). | **ONE admission path:** `_grantScopedAccess(kind, …)` — `_grantReviewerAccess` (`kind:'issue'`) and `_grantMemoAccess` (`kind:'memo'`) are thin wrappers over it. **ONE link factory:** `_mkLink('memo', memo.id)` — scoped, revocable (D117/CR-6). **The link IS the invite, and the invite IS the authentication** — no signup wall, no password, no account; **nobody is anonymous** (DL-021). The recipient's view renders on the **same `#reviewerView` surface**, `contenteditable="false"`, from the memo's **own frozen bytes** (`_memoPaperHTML`) — the open path **cannot reach** `_mkMemo` / `_memoBodyHTML`. **No seat (N-2), no invite (CR-2), no meter, no tier check.** Guard: `_assertSharedMemoUsesTheGrantMechanism()` (5 clauses) · `_assertSharedMemoIsReadOnly()` (now grades the recipient's surface too). |
| **D172d** | **The workspace is "Reports"; the document is the "Readout."** | `REPORT_TYPES` — a registry keyed by type, with **exactly one entry** (`readout`). Nav / crumb / tooltip = **Reports**; the readout's toolbar = **Readout** (from `_readoutDocName()`, one rename site). ⛔ **NO SPECULATIVE UI for report types that do not exist** — *that is exactly how the six-card scaffold happened the first time.* **D143 stands: the six "report types" it killed were sections of one memo, and they stay dead.** Guard: `_assertReportsHostsOneReportType()` (registry **and** DOM **and** the names) · NCs `aSecondReportTypeMayNotBeRegistered` · `theSixCardScaffoldMayNotReturn` · `theWorkspaceMayNotBeCalledAReadout`. |

**Tier census delta (D172b):** *Sharing/sending the readout* — **FREE on every tier, manual, unlimited** (CHG-061; no
UP-number, because there is no limit to hit). *Scheduling the readout* — **Basic** (`UP-REPORT`, `{sched:true}`);
the R1-vs-fast-follow question is still owner-open (`SCHEDULING_R1 = null`, M4-O2).

---

## Reports surface — Strategic Readout (WI-R1)

**Realizes:** DL-107 (five-section readout spine) · DL-108 (tailor the ASK, never the READ) · DL-104 (P1
health-framing / overclaim defect classes). Folded into the **existing** Reports surface — the export/snapshot
modal (`#exportScrim`, opened by `openExport()`) — as a **Strategic Readout composer**. Non-regressive: the
signed-off seven-section editable Readout **document** (`#rptDoc`, D148–D172) is untouched; this is additive over
"packages-never-produces / no-health."

**Why the export modal, not `#rptDoc`.** The composer deliberately **speaks OSLO's epistemic vocabulary**
(understanding maturity · *From OSLO* / *Confirmed by you* · the explicit "not health/RAG/readiness/probability"
line). That framing is required by DL-104 P1 but is **banned inside the reader-facing memo** by D149. The two are
different surfaces: `#rptDoc` is what a sponsor reads (D149 keeps doctrine out of it); the export composer is
**OSLO-facing packaging metadata**. The composer renders into `#sroDoc` and is **intentionally kept out of
`REPORT_SURFACES`**, so the §7j / D149 document scanners never grade it — and, symmetrically, its own DL-108
invariant is proven by a dedicated guard rather than by the memo's guards.

**The spine (assembled LIVE, from existing understanding — no analysis on generate).**

| § | Section | Source (slice-10 data model) | Audience-dependent? |
|---|---------|------------------------------|---------------------|
| §1 | The read | `_readCurrency()` band + reliability; carries the DL-104 P1 line + `From OSLO` derived marker | **No** |
| §2 | What's limiting it | `_chatState().limiting.dim` + sharpest open `ISSUES` in that dimension (`.caf`) | **No** |
| §3 | What we don't know yet | `ISSUES[*].clar` inferred items + `_openClarIds()` (deduped) | **No** |
| §4 | What I need from you | keyed on the shared `REPORT_RECIPIENTS` taxonomy (Sponsor / Programme lead / Operations / Executive-board — WI-R2), grounded in the live open issues; **the only section that reads `SRO.aud`** | **YES** |
| §5 | How to read this | reliability + currency marker (stale = "previous analysis") + derived-vs-attested rule | **No** |

**Optional sections (Basic):** Alignment · Unvalidated assumptions · How understanding matured · Artifact detail —
all presentation-only. "Unvalidated assumptions" **lists** items; it is **not** an assumption
validated/invalidated lifecycle (that is RB-017, deferred, not ratified).

**Tiering.** Free = the five-section read snapshot (§1–§5), PDF. Basic = optional sections + branding + scheduling.
**The seed — the read itself — is never gated.** Report **names** stay owner/glossary (DL-053): the surface is
labelled descriptively ("Strategic readout — the five-section read · naming pending"); "status report" and any
health/readiness name are banned by design.

**New boot guards (alongside `reportsNoHealth`):** `readIdenticalAcrossAudience` (DL-108 — §1–§3+§5 byte-identical
for every audience; only §4 varies; also asserts the three asks are distinct) and `readoutRunsNoAnalysis`
(packages-never-produces — assembling the whole spine for every audience with every optional section on leaves
`HISTORY` and `TREND` byte-for-byte unchanged). Boot self-check moves **58 → 60**, all green.

---

## D176 — the limiter row loses the orange; the CAF bars were false precision (owner: approved, 2026-07-12)

| Decision | What it binds | How it is implemented |
|---|---|---|
| **D176a** | **The hero card's colour allowlist now excludes `--primary`.** `--primary` is not a severity token, so D175's rule did not reach the CAF **limiter row** — **but D174's own reasoning does**: it banned `--primary` from the ramp *precisely because an amber-adjacent orange invites "amber = at risk"*, and the row sits **three lines under the ramp, in the same card**. **The limiter is a FACT, not a WARNING: emphasis by weight, never by hue.** | `HERO_CARD_BANNED_TOKEN_RE` = `--(success\|warning\|danger\|error\|crit\|conf-\|primary)`, applied by `_assertHeroCardCarriesNoSeverityColour()` to the **authored cascade** (chroma-graded literals, `@media`-aware, inline styles included, **bare-subject rules now in scope**). Restyled: `.cafrow.lim .cn` / `.cafband` (weight, `--text`) · a `.cafmark` **"the limit"** written from `_limitingOf()` · `.conf-foot .lnk2` (dotted underline) · `.howcalc-pop li .d` · `.cpp-stage b`. |
| **D176b** | **The CAF dimensions are BANDS, not percentages.** A bar filled to 55% asserts a **cardinal magnitude** OSLO cannot defend on an **uncalibrated** scale (**DL-062 F1**) — **worse than the 0–100 index**, because a filled bar reads as a **measurement without even showing its number**, in **progress/health-bar grammar** (**DL-104 §5 — P1**). | **One builder:** `_rampHTML(lvl,{compact:true})` — the hero's own ramp — drawn by `_cafRampInto()` into every CAF row on **both** surfaces (`renderCafRows()` for the hero card, `renderConfPop()` for the popover). `.caftrk` / `.caffil` / `.cpp-bar` and `_RELPCT` / `_RELCOLOR` are **deleted**. The reliability basis carries its **level word** alone. **`feasW`/`alignW` stay in the model** (they compute the band via `_cafLevelFor()`); they are never rendered. Guards: `_assertNoPercentageFillOnMaturitySurfaces()` (cascade **+** DOM **+** **render path**) · `_assertCafDimensionsRenderAsBands()` (byte-for-byte against `_rampHTML`; band computed from state; limiter derived). NCs: `_d176NegativeControls()` — **15 bite, 2 must-not-fire stay green**. **The Attention heat map is untouched — those cells are ISSUES (D003).** |

Boot self-check moves **72 → 74**, all green (Free × Basic × notes-OFF × notes-ON, **0 console errors**).

---

## D191 — a decision, once made, could not be unmade (owner P1, 2026-07-13)

| Object | Undoable? | How it is implemented |
|---|---|---|
| **The SELECTION** | **YES — freely, including back to NO selection.** | `clearSelection(id)` — `delete _selpath[id]` · `_istatus[id]='open'` · the decision record is dropped · a **new** History event. **No consent step, no meter, no analysis run** — an intention is not an act, and nothing in the plan changed. **Open ⇄ Addressed is not a ratchet.** |
| **The APPLIED EDIT + the ATTESTATION** | **YES — and ALWAYS TOGETHER.** | **`_withdrawUnit(id)` is the ONLY function in the product that may drop an attestation, and it cannot return without having restored the document too.** The document goes back via the machinery that already existed (`_artVersion` / `_artKey` body / `_pushUndo`, D084) — **no new snapshot mechanism was invented.** Reliability goes back to `_decision[id].relBefore`, **captured before the fix moved it**. `_attestBy[art]` records **whose word** attests each document, so withdrawing drops **only that decision's** attestation. |
| **The READ** | **NO.** | `_withdrawCore()` (the hand-path) contains **no read write, and cannot**: `_decision` carries **no band, no CAF width, no Confidence**. `_rereadAfterWithdrawal()` runs **inside the analysis update** and **re-derives** Feasibility from the state it finds (the gap is open again; the document is no longer confirmed) — **it never consults the withdrawal record.** A **new run event** and a **new trend point**; **last-good honesty (D098g)** in the interval. |
| **HISTORY** | **NO. APPEND-ONLY.** | The withdrawal is a **new event** (`type:'withdrawn'`, category *Your decision*, icon `↩`). The origin event is **never touched, never relabelled, never removed** — `pushHistory` gained `opts.iss` (a **pointer** to the issue) so the row can carry the affordance without the record ever being rewritten. |

**The transition table (`_ISSUE_TRANSITIONS`) — enumerated, not remembered:**

| Forward | Moves into | Attests? | Inverse |
|---|---|---|---|
| `selectPath` | `addressed` | no | **`clearSelection`** |
| `applyFix` | `addressed` + `attested` | **yes** | **`withdrawDecision`** |
| `_submitClarification` | `addressed` + `attested` | **yes** *(D192c — approved)* | **`withdrawDecision`** |

**The sweep:** every function in the product is scanned for writers of `_istatus[…]='addressed'` and
`.basis='attested'`. **Any writer not in the table, with a declared and existing inverse, FAILS THE BUILD.**
Probe helpers that stage-and-restore are **named** (`_ATTEST_PROBE_HELPERS`), never inferred.

**The meter (D191 §6):** `_meterRefund('fixes')` decrements the count **and** records it (`usage.refunds.fixes`),
surfaced on the Usage & Limits row — *"0 applied · no limit / **1 refunded (withdrawn)**"*. **The analysis run is
not refunded: it really happened.**

**Guards: 114 → 123, all green.** `_assertEveryDecisionTransitionHasAnInverse()` ·
`_assertWithdrawMovesEditAndAttestationTogether()` · `_assertWithdrawalNeverShrinksHistory()` ·
`_assertNoHandPathMovesTheRead()` · `_assertWithdrawalRefundsTheAssistedApply()` · **and the D192/D193 four:**
`_assertWithdrawSurvivesResolution()` *(replaces `_assertWithdrawIsAbsentOnAResolvedIssue()`, which encoded the
doctrinal error)* · `_assertWithdrawalNeverDeletesTheUsersWriting()` · `_assertAttestationIsRefcountedByDecision()` ·
`_assertLifecycleIsNotDrawnAsARatchet()`. **NC suites: 13; controls 272 → 281, every one bites.**

---

## D192 / D193 — the amendments (owner, 2026-07-13)

| Object | Amended rule | How it is implemented |
|---|---|---|
| **A RESOLVED ISSUE** | **D192a — withdraw is AVAILABLE.** *The analysis update resolves the issue ~1.9s after the apply; barring the withdraw there made the attestation permanent again.* | `_wdAvailable(id)` = `!!_decision[id]` — the resolved clause is **gone**. ⛔ `_withdrawCore()` **does not touch a `resolved` status** (an analysis update put it there). `_analysisUpdateAfterWithdrawal()` re-derives it: **document restored ⇒ the gap is back ⇒ OPEN**, with a lifecycle event. |
| **THE DOCUMENT** | **D193a — the restore is CONDITIONAL. OSLO may never delete the user's own writing.** | `_docTouchedSince(r)` — **content + version identity** against `bodyAfter`/`verAfter` (captured in `applyFix` at the moment OSLO's change landed). Touched ⇒ `docKept`, **nothing is written to the document**. `confirmWithdraw()` commits a pending keystroke first, so an uncommitted burst is never lost. |
| **THE ATTESTATION** | **D193b — refcounted by decision; Reliability restores to its pre-*first* value.** | `_attestBy[art]` (the list of decision keys) + `_ATTEST_BASE[art]` (captured by `_attestWith()` at the **0 → 1 edge**, before the document is marked). `_withdrawUnit()` restores from the base **only when the last decision goes**. |
| **THE LIFECYCLE DIAGRAM** | **D192b — it stops drawing a ratchet.** | `⇄` separators · `data-life` on each chip · only the current state carries `on`/`done` · the ⓘ states reversibility. |

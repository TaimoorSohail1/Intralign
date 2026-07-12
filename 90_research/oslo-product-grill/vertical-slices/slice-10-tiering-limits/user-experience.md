# Slice 10 — Tiering & Limits · User Experience

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

## D164 — the Readout is a DOCUMENT. It gets the artifact editor. **(COMPLETED 2026-07-12)**

> ⚠️ **The first pass was HALF DONE, and the owner flagged it:** *"The Readout composer matching artifact composer
> doesn't appear to be completed."* **The PLUMBING was shared; the MODEL was not.** The readout still had a
> **per-section EDIT MODE** — enter a section, edit it, close it — with a mini-bar and an "Editing" chip, while an
> artifact is **one continuous document you just type into**. And `#artdoc` was still hard-coded in shared editor
> paths, so e.g. the **slash menu behaved differently inside a readout table**. **Both are now gone.**

**ONE continuous, always-editable document. There is no edit mode.**
`#rptEd` is a single contenteditable `.doc` — the same class `#artdoc` carries — holding **every** section. **Click
anywhere and type.** No Edit button, no Save/Cancel row, no "Editing" chip, no enter/exit. The **sections remain
structural blocks** (`data-sec` — D150's seven, fixed order) but they are **not edit targets**.

**The section headings (`<h2>`) are `contenteditable="false"`** — document **furniture**, exactly as an artifact's
`<h1>` lives *outside* `#artdoc`. (They also carry a live date — *"What's changed since 5 July"* — which the PM must
not have frozen into their saved text.)

**The editor chrome lives in the TOOLBAR** (D160 — the reading surface is sacred), and it is **the same four actions
the artifact bar carries, calling the same four functions**: `artUndo` · `artRedo` · `_insertBlockFromButton` ·
`openFind`. They are **resident, not modal**, because there is no mode to enter.

**Every artifact-editor capability works in the readout, identically:** inline rich text · the selection toolbar ·
⌘B/I/U · undo/redo · the "/" slash menu · markdown shortcuts · ⌘F find/replace · the link popover · sanitised paste ·
the block model, grips and drag-reorder · **table row + column controls** · keyboard behaviour. **Bold, lists and the
decisions table survive editing intact.**

**How, without forking the editor:** the editor addresses **whichever document it is driving** —
`_EDIT_HOST` (`'artdoc'` | `'rptEd'`) · `_edDoc()` · `_edKey()` · **`_edSel()`** (scoped selectors) ·
**`_edContainerOf()`** (the block container). **The host follows the VIEW** (`_edSyncHost()` in `showView`), because
there is no longer a mode to enter or leave. Leaving the Readout **always** gives the host back to `#artdoc`.

**The BLOCK CONTAINER, and why it exists.** In an artifact the document *is* the block container. In a readout the
document is a set of structural **sections**, and the blocks live inside them. So the block model is scoped to the
nearest section: a paragraph reorders **within** its section and can never be dragged across the memo's fixed
structure (D150) or out of OSLO's prose into the PM's (which would corrupt both sections' authorship).

**Ownership tracks the TEXT, not a mode.** `data-pm="1"` is set on a section when its content **diverges** from
OSLO's generated seed — computed from the live DOM against the live seed, on a debounced commit (`_rptCommit()`),
**in place, without ever re-rendering the document** (a re-render would take the caret away — which is precisely why
the old build needed an edit mode). Type a section back to OSLO's exact wording and it **stops** being the PM's.

**Deliberately NOT shared — these are ARTIFACT semantics, not editor semantics** (each justified in a code comment):
- **epistemic provenance chips** (*From OSLO / Confirmed by you*) — they would put **OSLO vocabulary into a document
  that forbids it** (D149). *(`_attestNewBlock` was caught leaking these into inserted memo blocks; now gated.)*
- the **weakness stepper** — a memo has no issues;
- **artifact versioning + History events** — a readout is not a plan artifact;
- ⛔ **the reanalysis commit** — **a readout PACKAGES; it never PRODUCES** (D146). Editing a readout runs **no
  analysis**, spends no meter, and does not move the read by a degree.

⚠️ **Table CONTROLS are NOT on that list, and that is deliberate.** Adding a row to the decisions table is **editing**,
not asserting a plan fact. What stays artifact-only is the **provenance** (the row dot, the cell chip) — the epistemic
claims. `attachTableControls()` is therefore shared; `_ensureCellReveal()` and the row dot are gated.

All artifact semantics are gated at their own function heads by `_edIsArtifact()`, and the single structural-edit
choke point (`_commitFromStructuralEdit()`) returns early on the readout host.

**Guards (MECHANISM, not copy — D166), each with a negative control:**
`_assertReadoutIsOneContinuousDocument()` · `_assertReadoutEditorIsTheArtifactEditor()` ·
`_assertNoArtdocHardcodeInSharedEditorPaths()` · `_assertReadoutEditorProducesNothing()` ·
`_assertEditorHostFollowsTheView()`. Run **`_d164NegativeControls()`** in the console: **11 injected regressions;
every one must bite.**

---

# ⚠️⚠️ AMENDED 2026-07-12 — **D168 IS RATIFIED. YOU EDIT A REPORT; WHAT TRAVELS IS A MEMO.**

**Two objects, one lifecycle.** Everything below about *writing* the document is about the **REPORT**. Everything
about *sending* it is about the **MEMO**. They are not two views of one thing — they are **two things**.

| | **REPORT** | **MEMO** |
|---|---|---|
| **Where the PM meets it** | the Reports workspace. It is open, it is theirs, they are typing into it. | the **export preview**, and the **Sent** list behind the Export drawer. |
| **What it looks like** | **a document.** Flush at the top-left, no card, no shadow, the artifact's typography. **It looks like the thing they are writing, because it is.** | **a memo.** A card on the pane, a comfortable reading measure, a **quieter voice** — and a cover carrying the disclaimer. **It looks like the thing that lands in the sponsor's inbox, because it is.** |
| **What it does when the read moves** | **it tracks it.** Edit the plan, re-run the analysis, and the report follows. | **nothing.** It is fixed. What changes is its **label** — *"previous analysis"* — never its words. |

## The journey

1. **The PM writes.** They click anywhere in the report and type (D164). Editing is free, on every tier (D154).
   OSLO seeds; the PM owns (D152). Nothing about this changed.
2. **The PM opens Export.** The drawer opens, and with it the **package** — the cover, the mark, the disclaimer —
   and **the memo**, on paper, exactly as it will land. The identity line reads **"Memo preview — what travels"**.
3. **The PM exports.** The report **becomes a memo**: dated, frozen, named *Memo 1*, listed under **Sent**. The
   toast says *"Memo sent as PDF — dated 12 Jul 2026, 13:49, current analysis."* **No analysis runs** (D146).
4. **The PM keeps working.** They rewrite the summary. A new analysis lands and the read moves on. **The memo does
   not move.** Open it from the Sent list and it still says what it said when it left. It is now labelled
   *"previous analysis"* — because it is, and because saying so is the honest thing.
5. **Weeks later, the PM asks: *"what did I actually tell them in June?"*** (**D169**, closes O-D168-2.) They open
   **History**, find *"Memo sent — a dated snapshot (PDF)"*, and click **"open the memo →"**. The memo opens — **the
   exact bytes that travelled**, on the cover they travelled on, with the disclaimer and the currency marker of
   **the run it was cut from**. **Nothing is re-run. Nothing is written. Nothing is re-rendered.**

> **D169, in one line:** a **sent memo is the most auditable artifact in the product** — it went to the board,
> under the PM's name, on a date — and OSLO already holds it frozen. Leaving it unreachable wasted the one
> immutable record the product has. **Now the record of the sending opens the thing that was sent.**
>
> ⛔ **And it is never re-rendered from current understanding.** That is the whole rule. A re-render would look
> perfectly ordinary on screen and would be **history, silently rewritten**: June's memo showing July's read, under
> June's date, over the PM's signature. The memo is read out of its **frozen bytes**, and the open path is
> *structurally incapable* of reaching the live composer.

> **Why this matters, in one line:** a PM who sends a memo has **signed something**. If the words could change
> afterwards — silently, because the tool "refreshed" it — they did not sign a document, they signed a subscription
> to whatever OSLO thinks next week. **A memo that can change is not a memo.**

## What the PM never sees

- The report **never calls itself a memo**, and the memo **never calls itself a report**. One is being written; the
  other has left. *(Whether the workspace is called "Reports" is still an owner/glossary decision — DL-053.)*
- The **card never appears on the reading surface** (D160). The paper is for the thing that travels.
- The **gentle note (D155), the "your words" badge and the Reset affordance never travel.** They are app chrome and
  the memo is stripped of every scrap of it.

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


> **The experience promise of this slice:** you always know **which limit you hit**, **what it costs you**, **what relieves it**, and **what it can never touch**. And when OSLO does not know a number, it tells you that too.

## The emotional design problem

A limits system is where a trust product usually betrays itself. The standard playbook is: grey out the button, show a lock, put a permanent Upgrade badge in the chrome, and let a little manufactured anxiety do the selling. **Every one of those moves is banned here** — not because they don't convert, but because OSLO's entire product claim is *"I will tell you the truth about your plan."* A product that lies in its billing surfaces has already told you what its claims are worth.

So this slice is built on an uncomfortable discipline: **the limit surfaces must be as honest as the analysis surfaces, even when honesty costs a sale.**

## What the user sees

### Nothing, most of the time
There is **no persistent upgrade wallpaper**. The sidebar shows a quiet plan chip that reads **"Your plan"** and opens *Usage & limits* — a screen of **facts**, not a pitch. (In Slice 9 that button said **"Upgrade"**, permanently, on every screen. That is wallpaper, and it is gone.)

### At a cap: the control still works
Every limit-bearing control **stays enabled**. The user clicks *Apply this fix*, or *Send*, or *Export as a link*, or *Add collaborator* — and the **attempt** is what surfaces the prompt. Nothing is greyed out and nothing is hidden.

This is deliberate and it is doctrine (D138): **disabling the control suppresses the highest-intent moment in the product** — the exact second a user wants more — and it replaces an honest disclosure with a dead end. A user who clicks a live button and gets a clear explanation is being treated as an adult. A user who finds a grey button is being managed.

### The prompt names the limit and the tier — never "upgrade"
> *"You've used today's fixes — **Basic** gives you 20/day."*
> *"Free includes 1 active project — **Basic** gives you 3."*

Never *"Upgrade for more!"*. The user learns **exactly which limit bit them** and **exactly what relieves it** — including when the answer is *"a number nobody has decided yet"*, which the prompt says out loud rather than pretending.

### The free way out is offered first
Every friction prompt carries **resolutions**, and where a free one exists it is **listed first**:
- 2nd project → **archive the current one** (reversible; frees the slot) · or upgrade.
- Fix / chat cap → **wait for the reset** (a real time: *"midnight — in 4h 12m"*) · or upgrade.
- Deep-run cap → **keep the last analysis** (your edit is saved; the *re-read* defers) · or upgrade.
- Seat cap → **add them as a Viewer** (no seat, unlimited on every plan) · or upgrade.
- Export → **export as PDF instead** (free, the complete snapshot) · or upgrade.

A prompt whose only button is *Buy* is a wall. None of these is a wall.

### The footer of every prompt says what a limit never touches
> Your **artifacts** and your **History** are uncapped and permanent on every plan. **Asking anyone for their read is free and unmetered, forever.**
> **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

### When OSLO only read part of your plan, it says so — before it sells you anything
The partial-orientation notice (UP-4) leads with the **honesty**, not the offer: *"OSLO did not read all of your plan… every number on this page describes only the part it saw… there may be issues in the unread portion, and OSLO cannot tell you what they are."* The Basic note lives **inside that same notice**, in one sentence, at the bottom. **One surface, one notice** — because you should never have to read two notices to learn one fact.

~~And when the user asks *how much* larger the project is than the envelope, OSLO says: **that number has not been decided**, and refuses to invent one.~~
**AMENDED 2026-07-11 — the envelope is ratified, so OSLO names it.** *"Free analyses projects up to **~20 documents / ~50k words**. This one is larger."* And it adds the ratified fact that matters more: **the project was not rejected.** OSLO reads what it can, tells you the read is partial, and keeps going (§4b). **A precise honest limit is a better disclosure than a vague one.**

### ~~The gate that fires and blocks nothing~~ → **The gate that is real, and says exactly what it is**
~~UP-6 shows the **ratified copy** with the threshold **UNSET** — *"OSLO is enforcing nothing here."*~~

**AMENDED — the threshold was ratified all along.** It is the **monthly token governor**: Free **4M** · Basic **10M** (§4c calls it, verbatim, *"the binding governor"*). So UP-6 shows a **real number**, a **real calendar-month reset date**, and it **actually gates**.

What makes it honest is not that it enforces nothing — it is **what it does not touch**, said in the prompt itself:
- *"Your plan, your artifacts, your History and every issue OSLO has already given you are exactly where you left them."*
- *"**Asking anyone for their read stays free and unmetered.** If a reviewer answers you today, OSLO **records their evidence immediately** — it is never refused — and tells you plainly that the **re-read** is deferred until your budget resets."*
- And on **Free**: *"**There is nothing else to buy here.** OSLO does not sell Free users a top-up — Free converts by upgrading, and that is the whole of it."* (DL-074 §3.)

**Evidence is never rationed. Only compute is.** That sentence is the whole design, and the product says it out loud.

### The one number OSLO admits it made up
The **collaborator seat caps** (Free 3 · Basic 10) are **not in canon** — §4c sets no seat row below Team. So the product **says so**, on the meter, on the plans card, in Settings and in chat: *"recommendation — not ratified."* It is enforced provisionally, **nobody is ever removed** to enforce it (D132), and it is **never** the reason OSLO asks anyone to buy anything.
**A product that enforces a number it invented while calling it a rule is lying — even when the number is reasonable.**

### The value moments are not sales moments
- **UP-8** (first MRI): a chat message that *celebrates* — and explicitly says **Free is not a demo of OSLO; on one project it IS OSLO.** No ask. Once, ever.
- **UP-7** (confidence improved): names **Pro / continuous monitoring** as the honest next capability — and says, unprompted, **"Pro is a forward capability. It is not on sale, and there is nothing to buy here."**

### Chat explains; it never acts
*"Which limit did I hit?"* gets a precise answer from the live meters, with the real reset time, distinguishing the **plan** limit (depth) from the **phase** limit (supply), and ending with:

> **I can't upgrade you, buy anything, or lift a limit** — that is yours to decide, and it lives on the plan screen, not in a chat window. I explain; you act.

An assistant that can spend your money on your behalf is not an advisor.

## What the user never sees
- A greyed-out or hidden limit-bearing control.
- A generic "Upgrade" prompt, or a permanent upgrade badge.
- A countdown, an urgency colour, a red counter, or *"only 1 left!"*.
- An invented number (a price, an envelope, a budget) dressed up as a real one.
- A **phase** (supply) limit presented as a reason to **upgrade** (D124 — that is manufacturing an upsell out of a constraint we created).
- A cap on their **artifacts** or their **History**, ever, on any plan.
- A metered request for someone else's read.

---

# The readout (M4) — **D148–D154 · REBUILT** · what the user actually does

> **The last build was rejected: a modal, and a report that talked about OSLO.** This one is a workspace, and the report talks about the event.

### It is a place, not a pop-up
**Readout** sits in the sidebar with Overview · Issues · History · Attention map. Clicking it **switches the view**, exactly like the others. **Left: the composer. Right: the memo, rendered as a document** — a page with a byline, headings and one small table, not a form preview.

### What the reader gets
A one-page executive summary about **DevNorth 2026** — not about OSLO. It opens with a summary that **stands alone**, then what changed since last week, then the **risks** (before the assumptions), the assumptions, the PM's plan of action, the decisions needed, and an appendix the sponsor can skip.

**Not one word of OSLO's vocabulary appears in it.** No confidence figure. No CAF. No reliability band. No section explaining how to read it. The epistemic honesty is *in the sentences*:

> *"We are planning for 450+ people on it at once against a 500-device figure that **came from our own plan, not from The Grid**."*

The sponsor now knows exactly how far to trust that number — and no doctrine was spoken.

### Every risk lands twice
**For the plan** — what breaks in the schedule or the scope. **For the goal** — whether the plan, *as written*, still reaches what it was set up to achieve. *A delay is a schedule problem; a delay that means you miss the thing the project exists for is an outcome problem.* Same fact, different altitude — and knowing which one you are looking at is what separates a senior read from a status update. **OSLO never says whether the project will succeed.** It says whether the plan still joins up to its own intent.

### The plan of action is theirs
OSLO seeds the next steps from what it already recommended. **The PM edits them and owns them.** They read in the first person — *"I'm getting the network commitment out of The Grid in writing this week… I'm driving all of these. Back to you Friday."* If that section read as OSLO's plan, **the PM would be a passenger in their own report** and the sponsor would think *"the tool wrote this"* rather than *"my PM is sharp"*.

### Editing is free. Always.
Hover any section, hit **Edit**, rewrite it. **On every tier. Every week. From scratch.** This memo goes out **under the PM's name**, and OSLO will not sell them the right to correct their own words.

**What Basic buys is that they stop rebuilding it.** Standing text, tone, section choices and boilerplate carry from week to week and apply themselves. The prompt says exactly that — *"Basic remembers your readout so you don't rebuild it every week"* — and it says, out loud, that the editing itself is free and always will be. **"Next week (demo)"** proves it: on Free the wording is gone; on Basic it comes back, applied.

### Tailor the ask, never the read
Changing the recipient changes **section 6 and nothing else**. The summary, the risks and the assumptions are byte-identical for every reader. **One honest read. Many asks.**

### What travels
Export produces a **dated snapshot**. The memo sits inside a **wrapper** — the PDF cover — which carries the mark, the analysis-currency marker and **the disclaimer**. The disclaimer is *not* in the prose: a line saying *"this isn't a forecast"* invites the reader to wonder whether it was trying to be one. The real protection is that **the memo never makes a forecast claim**.

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157**

## The gentle note (D155) — what the PM actually experiences

1. The PM hits **Edit** on the Summary (free, every tier, every week — D154) and types: *"Registration is going well. We're 80% likely to hit 450."*
2. They **Save**. **The words go in exactly as typed. Nothing is rewritten, nothing is hedged, nothing is refused.**
3. **Beside** that section — not over it, not as a modal, no red, no urgency colour — a quiet margin note appears:
   > **Heads up — this reads as a forecast.** OSLO doesn't predict outcomes, and this goes out under OSLO's mark, on OSLO's cover. *"likely", "on track"*
   > **Your words are untouched and nothing is stopped.** This is a note, not a gate — send it if you mean it.
   > *Only you can say what your plan will do. OSLO can only say what it can see.*  **[Dismiss]**
4. They **Dismiss** it and **Export**. **It sends.** Every time. On every tier.
5. If they edit that section again, the note comes back — **new words, fresh advice.** It attaches to the sentence, not to the person.

**It is a margin note from a careful colleague, and it is the only honest position available.** Blocking would be the tool overruling the human (**advisory-only, D001**). Silence would be OSLO lending its name to a claim it forbids itself. **The PM may dismiss it and send anyway. Always.**

The composer explains it **once**, on OSLO's own surface — **never in the document**:
> *"OSLO will say so — quietly, beside the section. Then it will send it anyway. **OSLO does not police your prose.** These are your words, and they go out under your name. But they also go out under OSLO's mark… **It never blocks. It never changes a word. It is always dismissible.**"*

## The `To:` line (D156)

**Stays.** *To: Marcus Hale (Sponsor)*. Changing the recipient changes **section 6 and nothing else** — the surface says so, in as many words, and the guard proves it byte-for-byte. **Tailor the ask, never the read.**

## Length (D157)

**Five risks, highest impact first.** The appendix opens with *"For the leads — skip this if you are not one"* — the sponsor's five, and every workstream underneath for the people who need it. ⬜ **What gets cut and who decides is an M4 spec item; the build invents no truncation rule.**

---

# ⬛ AMENDED 2026-07-12 — **D165 · the chat is a CONVERSATION**

## What the user now experiences, turn by turn

**They click "Ask OSLO" on an issue.** A **divider** drops in — *Venue Wi-Fi capacity is unconfirmed (ISS-01)* — so
the new thread reads as a new thread. Then OSLO says **33 words**:

> **Venue Wi-Fi capacity is unconfirmed** — Critical, on Feasibility, in Resources.
> The plan requires 450+ on-site attendees, but the venue's 500-person Wi-Fi capacity is not confirmed.
> *I inferred this — it isn't in your inputs.*
>
> `Open this issue →`
> **What's it resting on?** · **What are my options?** · **Answer your question**

**And it stops.** The composer's own chips **vanish** the moment the conversation starts — there is exactly one set
of suggestions on screen, and it belongs to the conversation.

**Then the user pulls.** One idea per turn, each ending in another handoff:

| They ask | OSLO answers, and stops | Words |
|---|---|---|
| *What's it resting on?* | "2 lines in your inputs." + the **evidence cards** (clickable, they open the source) | 31 |
| *What are my options?* | "3 routes." + the three paths, named. **No advocacy** — that is the next turn. | 25 |
| *What would you do?* | "I'd confirm the venue's 500-person Wi-Fi capacity…" + **`Apply this fix →`** — the ONE action that fits **this** moment | 20 |
| *How sure are you?* | "Reliability is **Moderate** — … Basis: Coverage Moderate · Evidence Moderate · How assessable Moderate." | 27 |

## What did NOT change
- **The epistemic honesty.** It is still there, on exactly the same trigger — it is now **one sentence** instead of a
  chip *plus* a paragraph *plus* a reliability block.
- **Advisory-only.** The chat still never applies a fix, never selects a path, never resolves an issue, never sends a
  review, never buys anything. Every action is a **link the user clicks**, running the owning surface's function.
- **The clarification loop.** Answering in chat still produces a **byte-identical** History entry to answering in the
  panel. The form is simply **collapsed** now: a one-line question, expanding to the input on click.
- **The honest fallback.** Off-script, OSLO still says *"I don't have a grounded answer to that — so I won't invent
  one"* and lists what it actually can do.

## The feeling the owner asked for
Before: a wall arrives, and the user has to **read a document to ask a question**.
After: OSLO says one thing, and **offers the user the next move**. The depth is identical. **The user chooses when to
go and get it.**

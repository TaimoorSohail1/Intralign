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

- **Recommendation panel** (the `.ip-rec` block): the *"Applying drafts the change into your plan. Discussing changes nothing."* note and the *"Recommendations live only inside the issue"* rationale → **ⓘ / button tooltips**. *"Possible resolution paths"* → **"Other options"** (D190b). *"— recorded as your chosen approach"* → dropped (the **Confirmed by you** tag already says it).
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

---

# D170 / D171 — WHAT CHANGED FOR THE USER

**Before:** on Free, with an "Export link" format selected, the PM clicked **Export** and **nothing happened.** No file.
No explanation. No prompt. The button looked alive, the click landed, and the product went quiet. **An enabled control
that silently does nothing is worse than a disabled one** — a disabled control at least tells you something.

**Now:** the click always has a consequence. The prompt appears — *"Free exports as PDF. **Export link** comes with
**Basic**."* — with **two ways out**: export as PDF, free, right now; or upgrade. **Every time, not once a day.**

**Before:** the PM opened *Recipient* to check who the memo was addressed to, and **the paragraph they were reading slid
down the screen.**

**Now:** the menus are popovers. **The document does not move.** You act *on* the reading surface, not *around* it.

**Before:** the PM could address a readout **to the Sponsor** — and then had **no way to send it to the Sponsor.** The
toolbar could address it and export it. The History event was called *"memo sent."* Sent by what?

**Now:** **Send** sits beside Export. It goes to the person, as a **read-only copy on a link back into OSLO**. It is
**free on every plan** — a Free user can put a memo in an executive's inbox, because that is the whole point.
When the read moves on, their copy is **relabelled "previous analysis"** — **never silently refreshed.**

---

# D172 — WHAT CHANGED FOR THE USER

**The schedule sends it to people.** *Nobody schedules a PDF onto their own disk.* A schedule now means what a PM means
by it — **"send my sponsor the readout every Friday."** It goes out as a **share**: a read-only memo, on a link back
into OSLO, recorded in History as **sent** — and openable there, exactly as it left.

**And it still tells the truth about its own age.** If the analysis is behind the plan when the schedule fires, the memo
goes out **labelled "previous analysis."** It is **never quietly shipped as current**, and OSLO **never runs an analysis
to make it look fresh.**

**The share is free. The automation is Basic.**
You can send the readout **manually, to anyone, on any plan, as often as you like** — that is never limited, and it never
will be. **What Basic sells is not having to remember.** Try to schedule it on Free and the prompt says the honest thing:
***"Basic sends it for you every Friday"*** — and the first way out it offers you is **Send it now, free.**

**The person who receives it just opens it.** No signup, no password, no account. **The link is their invite, and the
invite is their key** — the same mechanism a reviewer gets. They see **that one memo**, read-only, on its cover, with its
disclaimer and its currency marker. When the read moves on, their copy is **relabelled "previous analysis."** It is
**never silently refreshed, and never rewritten.**

**Names.** The workspace is **Reports**. The document inside it is the **Readout**. There is **one** report type today,
and the product does not pretend otherwise: **no pickers, no galleries, no cards for reports that do not exist.**

---

## Reports surface — Strategic Readout (WI-R1)

**The moment.** A PM about to share out opens **Export a snapshot**. Before choosing a format they see the
**Strategic Readout composer**: one honest read, assembled live, with a single choice — *who is the ask for?*

**What they do.**
1. Read the five-section spine as it stands: **§1 The read**, **§2 What's limiting it**, **§3 What we don't know
   yet**, **§4 What I need from you**, **§5 How to read this**.
2. Toggle the audience — **Sponsor → Programme lead → Operations → Executive-board** (the four shared `REPORT_RECIPIENTS`, WI-R2). **Only §4 changes.** §1–§3 and §5 do not move a
   pixel. The banner above says why, in plain terms, and cites the rule: *tailor the ask, never the read.* This is
   the felt proof that OSLO will not spin the same plan three ways to three rooms.
3. Optionally add **Basic** sections (Alignment · Unvalidated assumptions · How understanding matured · Artifact
   detail) — presentation only.
4. Export. **Free** takes the read snapshot (§1–§5) as PDF; **Basic** adds the optional sections, branding and
   scheduling. Generating **runs no analysis** — it packages what OSLO already understands.

**The honesty on the face of it.** §1 states plainly that this is *understanding maturity — not project health,
readiness, a RAG status, or the probability of success.* §5 tells the reader how far to trust it: the reliability,
the currency marker (a stale snapshot reads **"previous analysis"**, never passed off as current), and that
*From OSLO* content is derived while *Confirmed by you* is attested — **a derived read is never dressed as
attested.** This is the DL-104 P1 guard, worn openly, because the PM stakes their name on the output.

**Why here and not in the memo.** The composer speaks OSLO's language on purpose — it is the PM's **workbench**,
not the thing that lands in the sponsor's inbox. The memo that travels (the Readout document) still reads in the
recipient's language, doctrine-free (D149). The workbench is where the PM sees the machinery; the memo is where
it disappears.

---

# D173 — THE PAYOFF: the moment the read moves

**The user acts. The analysis updates. The product says what changed — in numbers it can defend.**

> **You applied OSLO's fix to Resources.**
> **Feasibility: Very Low → Low.**
> **Issues 6 → 5 · Critical 1 → 0 · Open questions 2 → 1 · Confirmed artifacts 0 → 1 of 7**
> **Feasibility is still the limit.**

Three things, always: **the band transition** (discrete, earned, visible — an ordinal scale is still a scale) ·
**counts OSLO knows exactly** (every one computed from live state) · **the consequence** (what the limit is now).
≤45 words. No meta, no doctrine, no rationale.

## A fall is stated exactly like a rise
The read can **fall** when you improve the plan — a stakeholder disagrees on the record, and Alignment drops. That
is better understanding, not a worse project.

> **Chris's response landed as evidence.**
> **Alignment: Moderate → Low.** Your read fell — because you learned something.
> **Feasibility is still the limit.**

**Same block. Same classes. Same weight. No red, no alarm, no apology.** If a rise were a celebration, a fall would
be a punishment — and the product would be training people to avoid answering the hard clarification and to avoid
surfacing the ugly dependency. **That is the one behaviour OSLO cannot afford to create.**

## The 0–100 index stepped down
It used to be a 52px hero. It is **not calibrated** (DL-062 F1), so it did not get to look like a measurement — and
`58 → 62` handed the user a magnitude by subtraction, which is precisely the fabricated magnitude D056 forbids. The
index is now a small secondary aggregate that **states itself and nothing more**.

## ⛔⛔ THE OVERVIEW HERO: WHERE YOU ARE ON THE RAMP (D174)

Demoting the index left **one word in 40px** — a label, not a hero. So the Overview now shows **the thing the
doctrine always asked for and nobody drew** (D003): **the neutral maturity ramp.**

> **Very Low · Low · [ MODERATE ] · High · Very High**
> **on moderate reliability**
> **Feasibility is holding it back.**
> **↗ Strengthened — deeper analysis firmed the read (Feasibility rose Very Low → Low)**
> <sub>58/100</sub>

**Why the ramp and not a number.** Confidence *is* understanding maturity — **five ordinal steps**. The ramp shows
**how far along you are and what the next rung is**, which motivates **without being a score**; and because it is
**ordinal**, OSLO can defend every pixel of it. (It cannot defend 62 against 63.)

**It is a maturity scale, not a health bar.** A rise is **not green**; a fall is **not red** (D003 — severity colour
belongs to issues alone). Nothing fills to a percentage. Nothing says *on track*. The steps below your position are
**not "done"** — you are not progressing through a bar, you are **standing on a rung**.

**Everything in it is computed.** The lit band is the read. The qualifier is the reliability. The limiter is the
lowest of Clarity · Alignment · Feasibility — the same one marked on the bars below. The direction names **its
cause** and never a magnitude (D056), and it appears **only once there are two runs to compare** — before that,
there is no direction, so OSLO shows none.

**When the read falls, the ramp simply moves down a step** — same weight, same colour, no alarm. *Your read fell,
because you learned something.*

---

## D176 — what the user actually sees now

**The hero card has no colour in it at all.** The ramp, the qualifier, the limiter, the direction, the index, the
Provisional/Current chip — and now the **CAF rows** and the **footer links**. **Emphasis is carried by weight**, and
nothing on a maturity surface has a temperature.

**"What's driving it" is three little ramps, not three little bars.**

| | Before | Now |
|---|---|---|
| Clarity | a bar filled to **76%** | **five steps, the 4th lit** · **High** |
| Alignment | a bar filled to **55%** | **five steps, the 3rd lit** · **Moderate** |
| Feasibility | an **orange** bar filled to **30%** | **five steps, the 1st lit** · **Very Low** · **the limit** |

- **Nothing fills.** A filled bar says *"55 out of 100"* without showing the number — a measurement OSLO cannot
  defend (the scale is **uncalibrated**, DL-062 F1). A **position on five named steps** says exactly what OSLO knows
  and no more.
- **The limiter is marked by weight and by the words "the limit"** — because *"Feasibility is holding it back"* is a
  **fact**, not a warning. It is the same sentence the hero already speaks, on the row it is about.
- **The same three ramps appear in the confidence popover**, under a line that names the limiter. **One ramp, one
  mental model** — the dimension ramps and the hero ramp are the same scale and the same drawing.
- **Reliability's basis** (Coverage · Evidence availability · How assessable) is now **just its level word**. No bar.
- **The Attention map still uses red and amber** — because those cells are **issues**, and that is where severity
  colour belongs.

---

# D177 — MORE ISSUES **AND** HIGHER CONFIDENCE (owner, 2026-07-12)

**The most important demo moment in the product was hollow.** The Extended Analysis payoff claimed a deeper read
and **moved not one number**. Now it moves **both** — because a real Deep Pass **finds what the Fast Pass had no
budget to find** *and* **firms the assessment**.

## The payoff, as it renders (**39 words** · budget 45) — *amended by D178*

> **What changed**
> **Extended Analysis landed.**
> **Feasibility: Very Low → Low.**
> `Issues 6 → 8`  `Critical 1 → 2`  `Open questions 2 → 3`
> *I looked deeper and found two more. **I have one more question.** The read is firmer because I know more.*
> **Feasibility is still the limit.**

**The order is the argument:** the event · the band · **the counts that moved** · then the plain line that explains
them · then the consequence. The counts land **before** the sentence about them, so the sentence is read **against
numbers already on screen — never instead of them.**

**Three counts, three acts.** *It firmed the read* (the band) · *it found more* (`Issues` · `Critical`) · **and it
knows what it still needs to ask** (`Open questions`). **Every one computed from state.**

## ⛔ Why this is the best demonstration of the doctrine in the product

**MORE ISSUES *AND* HIGHER CONFIDENCE. That is not a contradiction — it is the point.** It is the clearest
illustration anywhere in OSLO that **confidence is UNDERSTANDING MATURITY, not project health**. If confidence
were health, finding two more issues would have to push it **down**. It goes **up**, because OSLO **knows more**.
**No other moment in the product makes that case so plainly.**

**Never apologetic. Never alarmed.** No negative colour anywhere on the block (D003/D173c — a rise is not green,
a fall is not red); the finding of two more issues is stated **plainly**, in the same weight as everything else.
**Severity colour stays where it belongs — on the issues themselves** (the Attention map, the panel, the spans).

## What the user sees, in order

1. **Two new marks appear in artifacts they have already read** — *Schedule → Sponsor sales close* (critical) and
   *Scope → recording* (moderate). **The words did not change. The understanding did.**
2. **The Attention map gains a cell** (Scope × Clarity) and deepens another (Schedule × Feasibility, now 2).
3. **Every count on the Overview moves together** — 8 open · 2 critical · the badges · the Progress card.
4. **OSLO says the same true thing in chat:** *"I looked deeper and found 2 more issues (1 critical) — things the
   first pass had no budget to reach. The read is firmer because I know more."*
5. **History records it** — the Extended run's *what changed* delta carries **opened: 2**, and a timeline event
   names both findings and where they live.
6. **They behave exactly like the six before them** — open the panel, read the evidence, take the recommendation
   or a path, share for review, resolve through an analysis update. **Nothing about them is special-cased.**

---

# D178 — AND OSLO **ASKS** (owner, 2026-07-12 — closes O-D177-2)

> **Finding an issue and knowing what would close it are different acts — and OSLO can do both.**

A deeper read that spots the **funding-vs-commitment gap** should **ask about the sponsor floor**, not merely flag
it. So the Extended pass now **raises a question** alongside its findings:

> ❓ **Is there a minimum signed-sponsorship floor — or a cancellation point — that has to be cleared before the AV
> and catering commitments go firm?**

**OSLO does not know the answer, and says so.** It re-reads the evidence it already cited — *sponsor sales close
**Aug 15***, *AV and catering **Confirmed***, *a **sponsor-funded** event* — and asks about **what is missing from
those inputs**. **It invents nothing.**

## What the user sees

7. **The ask arrives with the findings** — a **one-line, collapsed** request in the completion turn (*"There's 1
   thing I still need from you"*), and a **collapsed Clarification row** on ISS-07 in the Issue panel. **No open
   textarea shouting *do work now* at someone who came to read** (D162c/D165e).
8. **A third number moves in the payoff** — **`Open questions 2 → 3`** — and the note says so plainly:
   *"**I have one more question.**"* **The count is the proof the ask is real.**
9. **They answer it wherever they are** — in the panel, or right there in the chat. **It is the same event**: the
   same project-information update, the same lifecycle, the same analysis update, the **same History entry**.
10. **Answering does not close the issue by hand.** ISS-07 goes **Addressed**, and **only the analysis update**
    makes it **Resolved** — then the payoff runs again, and *Open questions* falls **3 → 2**. **Advisory-only.**

## Why this completes the demo moment

**The payoff now carries the full shape of a deeper read:** *it firmed the read* · *it found more* · **and it knows
what it still needs to ask.** A system that only **finds** hands the user a problem. A system that also **asks**
hands them **the next move**. **Never apologetic, never alarmed** — the question is stated as plainly as the band,
in the same weight, with **no colour keyed to it** (D003/D173c).

---

# D179 — THE OVERVIEW, REDESIGNED: **STATE OUTRANKS EVENT** (owner, 2026-07-12)

## What the user sees now, in order

1. **CONFIDENCE — the first thing on the page, always.**
   The five-step maturity ramp, the lit band in a **cool accent**, *"on moderate reliability"*, *"**Feasibility** is holding it back."*, and the demoted 0–100 index. **This is what is true all the time.**

2. **"What changed" — a strip *inside* the confidence card, only when something did.**
   It sits **under** the read it annotates. It has a **✕**. It is **gone by the next visit**. It never pushes the state down the page.

3. **PROGRESS — the counts, in the only place they appear.**
   > Issues **8** ↑2 · Critical **2** ↑1 · Open questions **3** ↑1 · Confirmed artifacts **0 / 7**

## The four things that were wrong, and why they mattered

**1. The event outranked the state.** The payoff panel sat **above** Confidence. But *"what changed"* is true for **one moment**; **confidence is true all the time.** A user landing on the Overview a week later would still have met the event first. **Confidence is now the top panel. Always.**

**2. The payoff presented as a standing surface** — *"as if it is always relevant to the audience."* It is not. It is a **delta on the card**: it annotates the state, it is dismissible, and it does not survive a reload.

**3. It was a paragraph doing a picture's job.** Five sentences that restated what the ramp could simply *show*. Now the movement is **drawn**:

```
Very Low  ·  ⟨Low⟩ ⟶ [ MODERATE ]  ·  High  ·  Very High
```

**Zero reading.** Previous band **ghosted**, current band **lit**, an **arrow** between them.

⛔ **And when the overall band did NOT move, the hero ramp says so by standing still.** In the demo, the Extended pass moves **Feasibility Very Low → Low** while the overall band **holds at Moderate** — so the movement appears on the **Feasibility row's** ramp, and the hero draws **no ghost**. **A movement that did not happen is never drawn.**

**4. Colourless was an over-correction.** *Neutral ≠ monochrome.*

> **OSLO's brand colour is ORANGE. Orange reads as AMBER. Amber reads as "AT RISK."**

That is a genuine **brand-vs-doctrine collision** on a maturity surface — and the answer was not to strip the card to grey. The answer is a **COOL ACCENT (blue/violet)**, which is **not in the RAG vocabulary** and cannot be read as health. It lights the ramp step, the band word, the limiter marker and the movement arrow. **Brand orange goes back to what brand orange is for: actions and links.** **Severity colour (red/amber/green) stays on issues alone** — the Attention heat map is untouched.

## The sharpest one: **counts had two homes**

*"What changed"* said **Issues 6 → 8**. Progress said **8 open**. **The same fact, twice, in two grammars, on one page** — and the reader has to work out that they are the same fact.

**Now:** the counts live in **Progress**, with the change **annotated** (`8 ↑2`), and *"What changed"* keeps only what Progress **cannot** say: **the band movement** (a picture) and **the one-line reason**.

## The payoff, as it renders — **19 words** (budget 20; it was 39 against a budget of 45)

> **WHAT CHANGED** ✕
> **Extended Analysis landed.**
> *I looked deeper: found two more, and one more question. The read is firmer.*

And on the ramp beside it: **Feasibility ⟨Very Low⟩ ⟶ [Low]**. And in Progress below: **Issues 8 ↑2 · Critical 2 ↑1 · Open questions 3 ↑1**.

**MORE ISSUES *AND* A HIGHER BAND.** Still the point. Still not a contradiction — and now it is **visible in one glance** instead of being argued for in five sentences.

## When the read FALLS

**Identical.** Same strip, same classes, same weight, same colour. The ramp ghosts the **higher** band and the arrow points **back** (`⟵`). The line reads *"Your read fell — you learned something."* — **plainly, without alarm and without apology.**

**A rise is not green. A fall is not red.** In Progress, `↑` and `↓` wear the same class, the same weight and the same colour: **a count going up is not bad news, and a count going down is not a prize.** If a rise were a celebration, a fall would be a punishment — and the product would train users away from the actions that teach them the most.


---

# D180 — Progress: what the user actually reads

**Before:** four chips of *stuff OSLO is tracking* — one of them (`Artifacts read 7/7`) a number **that could never
move**, and none of them answering the question a PM actually has.

**Now, three lines, and the first one is the whole product:**

> **GROUNDED — 1 of 7 artifacts rest on your evidence.** ↑1

**That is the only number in OSLO that says how much of this read is REAL versus INFERRED.** Everything else on the
Overview is a judgment; **this is the count of how much of the judgment is standing on the user's own evidence
rather than OSLO's inference.** It rises when they confirm an artifact, apply a fix, or answer a question. **It is
the progress narrative** — and it is why *progress* here means **grounding**, never **clearing**.

**OPEN** says what is outstanding. **CLOSED** says what their work landed — *"Issues resolved 1 · Questions answered
1"* — because **that is the one number that tells a PM their work worked** (O-D179-3, restored). **It is never a
target.** There is no "6 remaining", no completion bar, no percentage, no burndown.

## The moment that teaches the doctrine

The user answers a hard question. **GROUNDED goes 0 → 1.** The deeper read that follows finds two more issues.
**Issues goes 6 → 8.** Both arrows are the **same colour, the same weight, the same class.**

> **Progress went UP while the issue count went UP.** **That is not a bug — it is the point.**
> **You cannot game grounding. You can only game a burndown.**

Nothing in the panel calls the new issues a setback, because they are not one: **more issues + a firmer read means
OSLO looked harder and now knows more** (the same lesson as the Extended pass, D177, showing up in a second place).

---

# DL-109 — "How much of this did you actually know, and how much did you infer?"

**The question a PM has before acting on OSLO's read was never *"how many issues?"*** It is this one. **OSLO could
answer it exactly, from data it already extracts — and it never did.** The Reliability qualifier, the product's
central epistemic promise, was **three band words with nothing underneath them.**

## What the user now sees

**On the Overview, in Progress:**

> **Your evidence: 17 claims · I inferred: 11**
> **12 things I inferred are holding up your plan.**  *See them →*

**That second line is the sentence no competitor is in a position to say.** It is not a warning and it is not a
score. It is a **fact about the read**, and it is the fact a PM would change a decision over.

**⭐ D181a — what "holding up" MEANS: the read would change were it false. Operationally, THE READ POINTS AT IT** —
a **critical issue** cites it, **or** the **limiting dimension's** assessment rests on it, **or** ⭐ **a
STRONG-READING artifact's confidence rests on it.**

> **An inference is load-bearing in two ways: it supports a WARNING, or it supports a REASSURANCE.**
> **The reassurance case is the more dangerous, because nobody is looking at it.**
> ***Scope reads fine BECAUSE OF four things OSLO made up.*** **Those four are in the number.**

**An inference nothing points at is still an inference — but it is not holding anything up, and it is not counted.**

**On the Inference map:**

> **Scope reads strong, and most of it is mine — 4 of its 7 items are inference. Worth verifying first.**

> ## ⛔ **A strong-looking artifact that is mostly inferred is the most dangerous thing in the plan.**
> **It looks fine BECAUSE OSLO invented a coherent story. COHERENCE IS NOT EVIDENCE.**

**And it names the document to go and verify** — which is what makes it more actionable than the whole-read
false-confidence flag. **Confirm it, and the flag goes — and the four inferences it was holding up leave the
load-bearing number with it (20 → 12 after a deep pass). That fall is the user's success, not a score going down.**

## ⭐ D181b — the clock moves, and the assumptions age

**The demo project is NOT back-dated. It genuinely is new** — and Slice 7's first-run state depends on that.
**Advance a week (`Next week`) and the viewer WATCHES the ageing happen:**

> *"Promotion delivers 450 registrations from a Jul 1 open."*
> **Unvalidated for 2 minutes · 1 issue depends on it**   →   **Unvalidated for 3 weeks · 1 issue depends on it**

**Demonstrate ageing; do not assert it. A number you watch climb argues better than a label that asserts.**
**Grounding velocity moves with the weeks too:** a week in which nothing was grounded reads **0 · 0** —
*understanding is stalling*, said honestly. **It is a direction, never a target.** *(In this demo it is **Scope**: the brief says the word **in-person**, and OSLO wrote an
entire out-of-scope boundary from it — a virtual stream excluded, no remote attendance planned, "this year". None
of that is in anything the user gave OSLO.)*

**In the Readout, to put in front of a sponsor:**

> **§5 What I'd need to be sure**
> • Confirm: **The venue can carry 500 concurrent devices.** · *If it is wrong: Venue Wi-Fi capacity is unconfirmed.*
> • Confirm: **Sponsor revenue covers the commitments made before Aug 15.** · *If it is wrong: Sponsor funding closes after the costs are committed.*

**"Here is exactly what I need confirmed, and here is what breaks if it isn't."**

## ⛔ What the user never sees: a debt

**AE-06 — "Understanding Debt" — is NOT adopted, and the metaphor is rejected on doctrine, not merely on scope.**

- **"Debt" is a burndown in a hoodie.** Something **owed**, something **bad**, something to **pay down to zero** —
  exactly the grammar D180 banned from Progress. Re-admitting it under a new name re-opens the door the doctrine
  just closed.
- **It would make OSLO's core function a liability.** PS-01: *"construct a usable planning model from incomplete
  evidence."* **Inference is what OSLO is FOR.** If inference is debt, **the product generates liability by doing
  its job.**
- **It is not even true.** **Some assumptions never need validating.** A plan that assumes the sun rises needs no
  clarification. Treating every unbacked item as debt manufactures anxiety and **buries the few that matter under
  the many that do not** — which is precisely why the register is sorted **load-bearing first**, and why the
  headline number counts **only** what is actually holding the plan up.

**No surface says *owed*, *debt*, *liability*, *pay down*, or *drive to zero*.** `_assertNoDebtVocabulary()` grades
the **cascade**, the **copy**, the **render path** and the **registry** — four doors, because copy is only one of
them.

## ⛔ And a rising inference count reads neutrally

Run the Extended pass and the inference counts **go up** (11 → 12 inferred claims · 11 → 13 load-bearing) **while
the band goes up too.**

> ## **MORE INFERENCES *AND* A HIGHER BAND.**
> **That is not a contradiction — it is the point.** A deeper read of the same evidence **works out more about the
> plan**, and holds it **more firmly**. Nothing in the panel calls that a decline: **same class, same weight, same
> colour, on every arrow.**

**And when the user does the work, the number falls — because the plan is grounded, not because a debt was paid.**
Apply the fix on the venue Wi-Fi issue and Resources becomes *Confirmed by you*: **your evidence 17 → 19 claims ·
OSLO inferred 11 → 9 · holding it up 11 → 4.**


---

# D183 — WHAT THE USER NOW READS (owner, 2026-07-13)

## a. OSLO says "I" **only in chat**

> **"OSLO looked deeper: found two more, and one more question. The read is firmer."**

Chat is a **conversation**; a panel is not. **First person is a voice, not a default.** The chat keeps saying "I";
so does the **readout**, because there the first person is the **PM's** and **D152 requires it**.

## b. ⭐ It is **Outcome Confidence** — and the 0–100 index is **gone**

Canon's entity is `ConfidenceState` — *"Per-run **Outcome Confidence** snapshot."* The product said only
"Confidence": **canon drift and a positioning loss**, because association with **Outcomes** is the category.

> ⛔ **But the label makes the number dangerous.** *"Outcome Confidence **62/100**"* reads as
> ***"62% likely to hit your outcome"*** — **the forecast the doctrine forbids, arriving through the label.**
> The **ramp** cannot be misread: *"Outcome Confidence: **Moderate**"* on a five-step ordinal scale **is not a
> probability.**

**The label is adopted. The number is deleted** — hero, pill, popover, chat, reports. *(Closes the D173d /
DL-062-F1 "calibrate or demote" question: **DELETE**. It may return the day it is calibrated **and** the forecast
misread is closed — a note that lives in the **prototype-notes layer only**, D161.)*

## c. Confidence and Grounding do not share a word

Before: *"Confidence 62 MODERATE | Moderate reliability"* — **two different things wearing the same word.**

> **Outcome Confidence: Moderate** · *thinly grounded*
> **Outcome Confidence: High** · *well grounded*

**Confidence says how MATURE the read is. Grounding says how much of it is REAL.** The grounding word is
**computed from the provenance model** (`CONTEXT_ITEMS` — grounded vs inferred), never typed, and it **shares no
token with the band vocabulary.**

## d. **inferences**, not "things"

> *"**12** inferences are holding up your plan."*

## e. Plan artifacts are **documents**

Everywhere the user reads: the sidebar, the Attention map's rows, the Issues filter, the workspace, Plans, the
export dialog, every tooltip. **The canonical entity stays `Artifact`** — the same split DL-095 made for *Finding*
(canonical) / *Issue* (user-facing).

## f. The trend line is a sparkline and a direction word

> **↗ Strengthened**

The **cause** lives in **"What changed"**, and nowhere else. **Causes have one home, exactly as counts do (D179e).**

## g. The Overview reorders itself around the user

**First run** → *Start here* leads (there is no progress to read). **After first value** → *Progress* leads
(the user knows what to do; they want to know where they stand). **Computed, never a static order.**

---

# D184 — You read the change, then you consent to it (P1)

**Before:** *"Apply this fix"* — and the fix was three taps down, collapsed, below the button.

**Now:** the Issue panel leads with **what OSLO would change, in your language**, and the button sits underneath
it. **The button is short and constant — *Apply this fix*** (D190a): **the fix above it is the subject**, so the
label does not repeat it and truncate. The **other options** are one tap away — and they open **right there, under
the recommendation they are alternatives to** (D190c) — ranked so the one that moves the **limiting dimension**
leads. If OSLO has **no** recommendation it can render, **there is no button** — an action whose subject is absent
is removed, not degraded.

> **OSLO is advisory-only. Advice you cannot see is not advice — it is an instruction.**

**And what you get instead of a fix you cannot read:** *"◆ OSLO recommends — Confirm the venue's 500-person Wi-Fi
capacity before locking the in-person-only format."* → **[ Apply this fix ] [ Discuss ] [ Other options (2) ] ⓘ** →
and under it, when you ask for them: the two alternatives (**Select** · **Discuss**), your **Selected option**, and
the door that is always free — ***"✎ Write my own fix in Resources →"***.

# D185 — The Confidence popover reads like a readout

You open it to learn **where the read stands**. So it says that, and stops:

> **Outcome Confidence · Moderate** · *thinly grounded*
> Clarity **High** · Alignment **Moderate** · **Feasibility Low** *(the limit)*
> **Feasibility — the lowest. Confirm it to lift the read.**
> **[ Confirm Feasibility → ]**
> **Reliability basis** · *Thinnest: Evidence — Low.*  · **All three ▾**

**Twelve words of prose. Zero paragraphs.** Everything OSLO used to say about itself — *"not health, readiness or
probability" · "a fact about the read, not a warning about the project" · "determined independently of Clarity ·
Alignment · Feasibility"* — is **behind the ⓘ**, one tap away, where a curious user finds it and an ordinary user
is not taxed by it.

**And the reliability basis says what is THIN,** not that everything is average. Three rows all reading "Moderate"
is a table with no information in it. If the three really are level, it says that — once.

---

## D186–D189 — the Overview/Progress surfaces (owner, 2026-07-13)

### D186 — "Holding it up" dies. It meant the opposite of what it looked like.

**The owner — who wrote the doctrine — read *"20 inferences are holding it up"* as *"delaying it."*** It means
**SUPPORTING**: these are the inferences the read **points at**, the ones that would **change the read if they were
false** (D181). ***"Hold up" is ambiguous in English — support or delay — and it was sitting on the single most
valuable number in the product.* If he misreads it, every user will.**

> **YOUR READ RESTS ON**
> **9 inferences** ↓3 · *See them →*

*(**D194a** later took the repetition out of the copy: the row was rendering the label **and** saying it back —
*"9 inferences **your read rests on**"* — a straight **D179e** violation, in the row carrying the single most
valuable number in the product. **The label IS the sentence.**)*

**"Blocker" was not the answer.** It would have told the user to **remove the thing carrying their plan**. And on
the CAF limiter it reads as *"the PROJECT is blocked"* — the health framing **D003 forbids**. The limiter stays a
limiter, in D185.4's form:

> **Feasibility — the lowest. Confirm it to lift the read.**

**Swept everywhere**, including the two places no DOM guard can see: the **TOUR registry** (a tour step is copy one
click from the DOM) and the **prototype-notes registry**.

### D187 — trend colour: GREEN where the user earned it. NEVER red.

> ## **"Issues 8 ↑2" after an Extended analysis does not mean the plan got worse. It means OSLO looked harder.**

Red would tell the user their plan degraded **at the exact moment it was finally seen.** So:

| | |
|---|---|
| **GREEN** (`--earned`) | **`issues resolved` · `questions answered` · `you grounded`** — nothing but the user's own work can move them. **Honest, and earned.** |
| **NEUTRAL** | **everything else**, in **both** directions — `issues` · `critical` · `open questions` · `inferences` · `your read rests on` · **`From OSLO`** · **`Confirmed by you`** · **`Attested by <name>`**. **OSLO can move every one of them by itself** — and the third class is moved by a **reviewer**, not by the user (**D194c**/D187: green is for what nothing but the *user's own work* can move). |
| **RED** | **does not exist.** There is no token, no CSS rule, and no field in the valence table to set. |

**The test is mechanical, not aesthetic:** *"Could this count rise for a reason that is GOOD?"* **Yes ⇒ no colour.**
It is a **declared valence table**, computed — never a colour typed into markup — and every row **states why**.
**The cause still lives in "What changed", and nowhere else** (D179e / D183f). **Colour is not a cause.**

### D188 — the Structure panel: labels, not sentences.

**Before:** *"**6** dependencies OSLO assumed, and nobody confirmed" · "**5** named parties with nobody accountable
for them" · "**3** numbers in the plan that trace to nothing"* — three sentences doing a label's job, in a strip
meant to be scanned in one pass.

**Now:** **4 · Unconfirmed dependencies ⓘ** · **5 · Unowned parties ⓘ** · **3 · Untraceable numbers ⓘ**

**The number carries the weight; the label names it; the ⓘ explains it.** The vivid consequence was the right
instinct in the wrong place — **it is one tap away, not deleted.**

### D189 — kill "A direction, not a target."

**DL-107, for the third time.** The product kept narrating its own epistemics as a subheading. **Nobody reads a
caption and forms a belief about targets — they read the number.** *If it were a target, the panel would say
"goal". It doesn't. That is the whole protection.* **Deleted.** The rule is enforced **in the code** and explained
**behind the ⓘ**.

**And the first-person sweep now has eyes.** The guard's surface list carried **`#issuePanel`** — the real id is
**`issuepanel`** — so **the most-opened surface in the product had never been graded.** It is graded now, with an
issue actually open in it. **The user's own controls still say "my"** (*"✎ Write **my** own fix"*) — declared, not
guessed. **A copy rule that cannot tell who is speaking is not a copy rule.**

---

## D191 — you can undo the decision. you cannot undo the fact that you made it. (owner P1, 2026-07-13)

**Owner: *"can decisions such as fix selection be undone?"*** **No — and the code showed why that was worse than a
missing button.** `applyFix()` marked the user's document **"Confirmed by you"** and **raised Reliability**, and
`selectPath()` moved **Open → Addressed**. **There was no path out of either.**

> ⛔ **"Confirmed by you" is the USER'S WORD.** An attestation that cannot be withdrawn is a claim OSLO holds the
> user to **after they have disavowed it** — and **Reliability is computed from attestation**, so the read would rest
> on a confirmation the user no longer stands behind. **A truth defect, not a UX gap.**
> ⛔ **And it cuts at D001.** A product that gives **advice** but makes **accepting** it irreversible has converted
> advice into **commitment**.

### What the user sees

**Wherever the decision is visible, the way out of it is visible.** Two places, and only two: **the issue panel**
(in the banner that records what they did) and **the History row** (on the record of the decision itself).

**It is named for what it does — and it never says "Undo."**

| What they did | What the button says |
|---|---|
| Selected an option | **Clear selection** |
| Applied OSLO's fix | **Withdraw this fix** |
| Answered OSLO's question | **Withdraw this answer** |

> ***"Undo" implies the world returns to how it was. The read does not.***

### One line, before it acts

> **"This removes the change from Resources and withdraws your confirmation. OSLO will re-read the plan."**

**Consent, not a surprise** — the same rule as D184: **no irreversible-feeling act without its subject on screen.**
A withdraw raised from the **History** row **opens the issue first**, so the subject is always there. *("Keep it"
is the way out of the way out.)* **A selection carries no consent step: nothing in the plan changed, and it clears
freely.**

### What comes back, and what does not

- **The document** goes back to its **pre-fix version**, using the version snapshot that already existed.
- **The attestation** is dropped **in the same breath** — never separately. *An edit withdrawn while the
  attestation stands would leave OSLO asserting "confirmed by you" about text that is no longer there.*
- **Reliability** goes back to the value **captured before the fix** — not re-derived by guessing.
- **The issue returns to Open**, with **no option selected**. *"No option chosen" is a real state.*
- **The assisted apply is refunded** — *you cannot bill a user for labour you then took back* — **and the refund is
  recorded** on the Usage row: *"1 refunded (withdrawn)"*.
- **The read does NOT come back.** **An analysis update runs.** In the interval the read is the **last good** one
  (**D098g**) — *it has not been rolled back, and it will not be: only an analysis update moves it.* The update
  produces a **new run** and a **new trend point**, because it is **a new read, not the old one restored**.
- **History does not come back either — it GROWS.** The withdrawal is a **new event**, sitting above the decision it
  withdraws. **The decision stays on the record, because it happened.**

### The document comes back — unless the user has written in it since

- **Untouched since the fix** ⇒ **the document goes back to its pre-fix version.** Nothing of the user's exists to lose.
- **Edited since the fix** ⇒ ⛔ **OSLO DOES NOT TOUCH IT.** Restoring would **destroy every word they wrote afterwards — to undo a change OSLO made.** So the **attestation is withdrawn alone**, and OSLO says so, in the consent line and on the record:

> **"This withdraws your confirmation. Your edits since are kept — OSLO's change is still in Resources, and you can remove it yourself if you want it gone. OSLO will re-read the plan."**

**The confirmation drops in both cases** — *the user's word is theirs to retract, whatever happened to the text* — and **an analysis update runs in both cases.**

### What comes back, and what does not

- **The attestation** is dropped **in the same breath as the document** — never separately.
- **Reliability** goes back to the value **captured before the first confirmation** — not re-derived by guessing.
- **The selection** goes back to **none**. *"No option chosen" is a real state.*
- **The assisted apply is refunded** — *you cannot bill a user for labour you then took back* — **and the refund is recorded**.
- **The read does NOT come back.** **An analysis update runs.** In the interval the read is the **last good** one (**D098g**). The update produces a **new run** and a **new trend point**, because it is **a new read, not the old one restored**.
- **History does not come back either — it GROWS.** The withdrawal is a **new event**. **The decision stays on the record, because it happened.**

### A resolved issue is still withdrawable — and it re-opens BY ANALYSIS

**The analysis update resolves the issue about two seconds after the fix is applied.** If the way out died there, *"Confirmed by you"* — on the user's own document, with Reliability raised — **would be permanent again on every fix that worked.**

> ## **Withdrawing a fix is not hand-moving the read. It is the user editing their own document and retracting their own word.**

So the withdraw **survives resolution**, and the panel says the word still stands: *"Your confirmation still stands on Resources — and it is still yours to withdraw. OSLO will re-read the plan, and re-open this issue if the gap is back."*

**And the user still never moves the read by hand.** The moment they withdraw, the issue is **still Resolved** and the read is **unchanged**. Then the **analysis update** lands, finds the change gone from the document, and **re-opens the issue — because the gap is genuinely back.** *The user withdraws the fix. The read follows.*

### Two decisions, one document

If a fix **and** an answer (or two fixes) both confirmed the same document, **withdrawing one does not retract the other.** The document stays **Confirmed by you** while **any** of the user's decisions still stands, and the History event says why. **It drops only when the last one is withdrawn** — and Reliability then goes back to where it was **before the first**.

### The lifecycle is not a ratchet, and the diagram stops saying it is

`Open ⇄ Addressed ⇄ Resolved`. **The states move both ways.** Only the state the issue is *actually in* is lit — a filled-in trail would claim the progression is settled, and it is not. **What moves it is still never the user's hand.**

---
## D194 — the Progress rows: say it once, and say it in the ratified vocabulary (owner, 2026-07-13)

### D194a — the load-bearing row was saying it twice

It rendered the **label** `YOUR READ RESTS ON` **and then said it again in the value** — *"13 inferences **your read
rests on**."* **One home** (D179e). **The label is the sentence.**

> *(DL-111 + erratum — the load-bearing *leans* line, below the bar)*
> **Your read leans on 20 inferences** ↓7 — *the inferred claims above plus inferred assumptions, relationships and
> metrics* · *See them →*

**~60% less text than the phrase D194a replaced.** The neutral ↓ delta rides along, and the *See them →* link to the
Inference map stays on this line. Under the erratum the load-bearing count is its **own line below the bar** — a
**superset** of the inferred *claims* shown in the bar (assumptions, relationships and metrics included), so it is
**never `+`-joined** to them, its surface untouched.

### D194c — the GROUNDED row now speaks the ratified epistemic classes

It said *"Your evidence: 17 claims · OSLO inferred: 12"* — **true, and in words the product used nowhere else.**

> **17 grounded facts** — *your read is built on*   *(the hero = ATTESTED claims only, computed)*
> **Confirmed by you** *(grounded — the solid, cool-accent segment; label only, its count is the hero)* · **From OSLO 12** *(inferred — hatched)*
> *Grounded — your evidence · Inferred — OSLO's read*

**The owner proposed *"AI Interpretation | Your Understanding."* The instinct is exactly right — the epistemic
classes ARE that distinction. Both words are already canonical at a different size:**

- **`interpretation` is ONE of the six `ContextItem.item_type`s** (*claim · assumption · relationship · entity ·
  metric · interpretation*). Using it as the heading for **all** inferences makes the word mean **two sizes** —
  exactly what the **DL-053 Disambiguation Register** exists to prevent.
- ⛔ **"Understanding" is the most load-bearing word in the product. Confidence *IS* understanding maturity.** If
  *"Your Understanding"* came to mean *"the claims you grounded,"* then **understanding** would name **OSLO's
  assessment** and **the user's evidence** on the same screen. **Drift, on day one, in the highest-value term we
  own.**
- **The product never calls itself "AI." It calls itself OSLO.**

**Saying it in the class names TEACHES them.** The user meets *From OSLO* and *Confirmed by you* on issues, on
documents, in reports and on the Inference Map. **One vocabulary, everywhere.**

**The third class is representable, not decorative.** The row is **computed over the classes** — not two slots with
a third bolted on. *Attested by \<name\>* (D115) is **absent today**, because reviewer evidence attaches to an
**issue**, not to a claim — and **a count OSLO cannot compute is not shown** (D173). **It is never drawn as a zero.**
The day a claim carries a third-party attestation, a third cell appears with no change to the render path.

### D194d — the two rows are not one ledger, and they may never be merged

> **The solid bar** answers *"how much of this is grounded vs inferred?"* — **a COMPARISON** (two provenance states).
> **The load-bearing *leans* line** answers *"how much of the READ is LEANING on inference?"* — **a SUPERSET.**

**Folding the leans line into the bar invites the user to read the inferred-claims count against the load-bearing
count as a RATIO. It is not one — so the erratum keeps load-bearing as its OWN line below the bar, never `+`-joined.**

**And they do not even share a population.** **The bar's inferred segment counts inferred CLAIMS** (e.g. 12);
**the leans line counts inferred items of *every* type** (e.g. 20) — assumptions, relationships and metrics
included, because **the read leans on those too** (D181). So the load-bearing count (20) *legitimately exceeds* the
inferred-claims count (12), and **both numbers are right — the old panel `+`-joined them as if disjoint, which was a
lie about what they meant.** *(The adjacency is escalated to the owner as **O-D194-1**; the build does not choose.)*


---

## ⭐⭐ D196 — "Confirm it to lift the read." (owner, 2026-07-13)

**The owner asked whether *ground / grounding* should become *stabilize / stabilizing*. It should not — but he was
right that *"ground"* reads as jargon to a PM.**

> ⛔ ***"Stabilize"* would call the FALSE-CONFIDENCE CASE A SUCCESS.** *"Scope reads strong — but 8 of 11 items are
> inference"* is **a perfectly stable read. Its stability is what makes it dangerous.** And *"stabilize the read"*
> makes **stillness** the goal — when the whole product exists to give **honest, revisable confidence.**

**So the verb and the state separate — and both words are ones canon already owns:**

> # **THE USER CONFIRMS. THE READ IS GROUNDED.**

**What the user now reads on the hero:**

> **Outcome Confidence · Moderate** · *largely grounded*   ← **the STATE (unchanged)**
> Clarity **High** · Alignment **Moderate** · **Feasibility Low** *(the limit)*
> **Feasibility — the lowest. Confirm it to lift the read.**   ← **the ACTION (new word)**
> **[ Confirm Feasibility → ]**

**And in the Progress panel, one panel down, the same word is already waiting for them:**

> **Confirmed by you** — the grounded (cool-accent) segment of the foundation bar, its **17 grounded facts** in the hero · **From OSLO 12** (inferred, hatched) *(DL-111 + erratum)*

**That is the point.** *"Confirm"* is not a new word the user has to learn — **it is the word on the class name they
meet on every issue, every document, every report and the Inference Map** (D011/D069/D194c). **The verb the product
asks for and the class it writes back are now the same word.**

### What did NOT change, and why

| Surface | Still says | Why |
|---|---|---|
| The Reliability qualifier | *barely · thinly · partly · **largely** · well **grounded*** | **D196b.** *"Evidenced"* would collide with **Evidence**, one of the three Reliability components. *"Confirmed"* cannot carry it: a read is grounded by **evidence** *and* by ***Attested by \<name\>*** — **and that is not the user confirming.** |
| The Inference-map lead | *"Your evidence is **solid ground**."* | **A noun, not an order.** It is the foundation metaphor D186 built (*"your read **rests on**…"*). |
| The velocity card (§4b) | *"**you grounded** 3"* | **Past tense — a measured fact about the user's own work, not an imperative** (D187's one green count). Its tooltip already says *"…because **you confirmed** the document they came from."* **The user confirms; the claims become grounded.** ⚠️ **Escalated as O-D196-1** — see `open-items.md`. |

---

# D197 · D198 · D199 — what the user actually sees now (owner, 2026-07-13)

## The Progress panel

> **17 grounded facts** — *your read is built on*   *(the hero = ATTESTED claims only, computed)*
> **[ Confirmed by you · grounded ]  [ From OSLO 12 · inferred, hatched ]**
> *Grounded — your evidence · Inferred — OSLO's read*
> **Your read leans on 20 inferences** — *the inferred claims above plus inferred assumptions, relationships and metrics* · *See them →*
> **OPEN** Issues 6 · **Critical** 1 · Open questions 2   ·   **CLOSED** Issues resolved 0 · Questions answered 0

**A foundation bar, not a ledger (DL-111 + erratum).** The hero is the computed **grounded-facts count — attested
claims only** (`17`, never grounded + inferred). The solid bar shows the read's claims in **two provenance states**:
the *Confirmed by you* (grounded) segment carries the cool-blue accent that **echoes the Outcome Confidence ramp's
lit band** and holds **only its label — its count is the hero**; the *From OSLO* segment **is the inferred state**,
rendered **hatched**. *A load-bearing wall is the thing you do not knock out:* the inferences the read **leans on**
are a **line below the bar — a superset** (inferred items of every type), never `+`-joined to the claims above.

⛔ **The bar and the leans line are still NOT one ledger** (D194d). The solid bar is a *comparison* (*grounded vs
inferred?*); the leans line is a *superset* (*how much of the READ leans on inference?*). Fused, the user reads the
inferred-claims count against the load-bearing count as a **ratio** — it is not one; **20 legitimately exceeds 12
because they count different populations.** **Severity red shows only on Critical, the deltas are neutral, and brand
orange stays on actions/links (`See them →`, `Timeline →`), never on state** — a harmony pass so the panel reads as
one page with the Outcome Confidence panel.

## The Inference map — the rows got their left edge back

**Before:** six consecutive assumption rows each wore a `YOUR READ RESTS ON THIS` chip, and each marked row's text
started at a different x from the unmarked ones. The section header **already said it** (*"The ones your read rests
on come first"*). **The chip restated it six times and broke the alignment of the list it was annotating.**

**Now:** a **quiet bar in the left margin**. Every row — marked or not — **reserves the same gutter and starts at
the same x.** Nothing on the row moved.

- **The sort order is the signal**, and the header says so.
- **What the bar MEANS lives on the ⓘ** (new, on both section headers) and on the row's own hover — **on demand,
  never resident** (DL-107/D185).
- **`VERIFY` is gone from the number column.** It was a button wedged into a stat row, and the counts justified
  around it. **The row is a readout.** The action is where it belongs: **click the row, or press Enter on it** — and
  the flag above the map still names it in full: *"**Resources** reads strong — but 8 of 11 items read as inference,
  most from OSLO. Worth verifying first. **Open Resources →**"*
- **A colour-blind user sees the bar.** A screen-reader user hears *"Load-bearing."* / *"Worth verifying first."*
  from an **out-of-flow** node that moves no character on the row.

## Everywhere the concept is named, it is **Outcome Confidence**

| Surface | Was | Is |
|---|---|---|
| **The hero — the FIRST panel of the Overview** | `Confidence` | **`Outcome Confidence`** |
| **The trend ⓘ and the trend chart's accessible name** | *"Confidence trend across analysis runs"* | **"Outcome Confidence trend…"** ⛔ **the miss the owner caught** |
| **The ramp's accessible name** | *"Confidence: Moderate. Step 3 of 5…"* | **"Outcome Confidence: Moderate…"** |
| **The Overview's "why" line** | *"Confidence sits at **Moderate**…"* | **"Outcome Confidence sits at Moderate…"** |
| **Chat — the read, the summary, what changed** | *"Confidence **strengthened**"* | **"Outcome Confidence strengthened"** |
| **The export package + the copied text** | *"Confidence Moderate · moderate reliability"* | **"Outcome Confidence Moderate…"** |
| **The reviewer footer** | *"Confidence is understanding maturity…"* | **"Outcome Confidence is understanding maturity…"** |
| **The prototype notes** | *"the 0–100 index is **DEMOTED, NOT DELETED**"* | ⛔ **a note still teaching a decision D183b superseded** — rewritten |

**What did NOT change, and must not:** *"**how sure are you?**"* · *"why is **my confidence** where it is?"* · *"the
**false confidence** case"* · *"**Confidence is understanding maturity** — not project health."* **These are prose.
The guard grades the ROLE, not the substring — a guard that reddened on the doctrine would get the doctrine deleted
to make it green.**

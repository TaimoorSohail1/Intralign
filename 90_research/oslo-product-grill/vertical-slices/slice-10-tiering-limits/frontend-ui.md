# Slice 10 — Tiering & Limits · Frontend / UI

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

## D164 (VISUAL PARITY) — the readout is **DRAWN** as an artifact is drawn **(2026-07-12, owner-directed)**

> ⚠️ **The owner flagged the last half of the same gap:** *"The readout presentation is still different from
> artifacts. It is contained in a grey box with padded margins left and right, while the artifact starts at
> top-left of the space. Any reason the readout can't mimic the visual layout of artifacts?"*
> **There was no good reason.** It was a design instinct — *"a memo should look like a memo"* — and it directly
> contradicted D164.

**The readout was drawn as a PAPER SHEET; the artifact is drawn as a DOCUMENT YOU WRITE IN.** The plumbing and the
model were already shared (above); the **rendering** was not. `.memo` was a card — surface fill, 1px border, 6px
radius, `34px 40px` padding, a 12px drop shadow, and in light mode a literal `background:#fff` **white sheet in a
dark-default app (D127)** — floating inside a **centring** `.rw-page` flex box at its own `74ch` measure. `#artdoc`
is none of those things: it sits **flush at the top-left of `.aw-center`**, on the pane's own background, at 720px.

**A card says PREVIEW.** It was the single loudest signal telling the PM that the readout was something a machine
produced for them to approve — rather than the document they write. **One editor, two renderings, is two mental
models, and D164 permits one.**

**What changed (CSS only — no logic, no DOM, no copy):**

| | before | after |
|---|---|---|
| `.rw-page` | `padding:34px 24px 90px; display:flex; justify-content:center` | **`padding:24px 34px 90px`** — the `.aw-center` treatment, byte for byte |
| `.memo` | `background:var(--surface); border:1px; radius:6px; padding:34px 40px 30px; box-shadow:0 12px 34px; max-width:760px` (+ a `#fff` light-mode card) | **`background:none; border:0; radius:0; box-shadow:none; padding:0; margin:0; max-width:720px`** |
| `.memo p/li/ul/ol/table/th/td` | re-declared 13px muted memo typography — **same specificity as `.doc p`, later in the sheet, so it won on source order** | **deleted.** `.doc` governs the readout body outright |
| `.m-doc` | `max-width:none !important; margin:0 !important` (only needed to escape the card) | **deleted** |

**What the memo KEEPS, and why.** Everything that makes a memo a memo is its **furniture**, not its font size:
the title (`.m-t`, now 21px/600 — the `.art-head h1` weight), the byline + **currency marker** (D153), the **`To:`
line** (D156), the rule, the **seven fixed sections** (D150), `.m-risk` / `.m-alt` / `.m-app` / `.m-sign`, the
**ownership badge**, and the **D155 gentle note**. **The BODY is now byte-for-byte the artifact editor's body** —
same 14.5px/1.8 prose, same bullet, same table chrome and row/column controls, same hover and selection
affordances, same `--blkgrip-w:22px` grip gutter.

**⛔ UNTOUCHED: `#rptPkgHost` / `#rptPkg`.** The package wrapper is **export metadata**. It is still always
rendered, still always carries the ratified disclaimer, and is still shown **only** on the export preview (D153).
*A cover is something the document travels ON, not something you read THROUGH.*

**Themes.** The document now sits on `--bg` in both. Contrast **improves in dark** (the darker `--bg` behind the
same tokens) and every readout token still clears **AA on light**: body prose 15.87:1 · table cells 7.69:1 ·
byline/table headers/grips 5.01:1 · *your words* badge 6.02:1. **The `#fff` card is gone and is not coming back.**

**Guards (MECHANISM, not copy — D166), each with a negative control:**
`_assertReadoutIsOneContinuousDocument()` · `_assertReadoutEditorIsTheArtifactEditor()` ·
`_assertNoArtdocHardcodeInSharedEditorPaths()` · `_assertReadoutEditorProducesNothing()` ·
`_assertEditorHostFollowsTheView()` · **`_assertReadoutIsFlushLikeAnArtifact()`**.

> **`_assertReadoutIsFlushLikeAnArtifact()` reads the CASCADE, not the DOM** — because the defect was never in the
> DOM (`#rptEd` already carried `.doc`; every DOM guard passed while the two documents looked nothing alike). It
> parses the authored `<style>` source (comments stripped — *load-bearing*, since the comments now quote the
> removed `background:#fff`) and proves: **(a)** nothing targeting `.memo` paints a card, in either theme, at any
> width; **(b)** `.memo`'s measure **=== `.doc`'s** measure; **(c)** `.rw-page`'s padding **=== `.aw-center`'s**
> padding; **(d)** nothing re-centres `.rw-page`; **(e)** nothing scoped to `.memo`/`.m-doc` re-declares `.doc`'s
> typography on a generic block element; **(f)** `#rptPkg` still exists and is **not** inside `#rptDoc`.
> **It is DERIVED, not hardcoded** — it never asserts "720px"; it asserts *the readout matches the artifact*.
> Change the artifact's metrics and the readout is **required to follow**. The guard cannot go stale.

Run **`_d164NegativeControls()`** in the console: **22 controls; every one must hold.** Eight are the parity
controls — they re-inject the card, the light-mode `#fff` sheet, the card padding, the centring flex box, a
divorced measure, and the memo typography, and each must make the guard bite; one proves the guard **passes as
shipped**; one proves it **refuses to grade nothing** when `.doc` loses its measure (D166 §1).

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


> ## ⚠️ AMENDED 2026-07-11 — the tier ladder was RATIFIED all along
> `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c` carries **owner-confirmed rows for every tier**. Five values this slice rendered as *"owner-TBD"* are ratified: **Basic price $12/mo · Basic chat 75/day · Basic deep-runs 6/day · envelope Free ~20 docs/50k words + Basic ~40/100k · the monthly gate = the token governor (Free 4M · Basic 10M — "the binding governor")**. One value marked RATIFIED is **not**: the **collaborator seat caps** (§4c has no seat row below Team). Superseded passages below are marked in place. Full detail: `tier-definitions-census.md`.


Cumulative Slices 1–10 in a single openable `prototype.html` (11,725 lines). Same CSS variables, same dark/light theme (**dark is the default** — D127), same component vocabulary as Slices 1–9. No new dependencies.

## Two visual rules govern everything in this slice

1. **A limit is never sold as scarcity.** No countdown, no urgency colour, **no red on a counter**. Severity colour is reserved for **finding severity** (D003) and is never borrowed to manufacture pressure. A meter bar is neutral grey; at the cap it turns the brand tint (`--primary-light`) — a *state*, not an alarm.
2. **An unset number LOOKS unset.** `.tbd` / `.m-unset` (dashed warning border, "unset") are the only ways a not-yet-decided value may render. **There is no styling in the file that can make a fabricated number look ratified.**

## New surfaces

| Surface | Id | Entry | Notes |
|---|---|---|---|
| **Usage & limits** | `#limitsScrim` | sidebar plan chip ("Your plan") · prompt footers · chat | Live meters + the **in-product census** (every value, ratified or unset) |
| **Upgrade prompt** | `#upScrim` | `fireUP()` only | ONE renderer for UP-1/2/5/6/7 + UP-EXPORT. Kind chip · title · body · **resolutions** · the "what a limit never touches" footer |
| **Partial-orientation disclosure** | `#partialBox` (Overview, above Confidence) | `renderPartial()` / UP-4 | **The disclosure IS the prompt** — one notice, never two |
| **Forward ladder** *(AMENDED)* | inside `#plansBody` | Plans | **Pro (~$39) · Team (~$99–149/seat) · Enterprise (custom)** — ratified prices (DL-074 §4), **no Buy button on any of them** (not purchasable in R1). ~~*Named, no price, no button*~~ |
| **Governor meter** *(new)* | top of `#meterBox` | Usage & limits | The **binding limit** — Free 4M · Basic 10M tokens/month (§4c), visible meter + real reset date (DL-074 §5) |

*(UP-3 keeps its dedicated high-intent modal `#upgradeScrim` — archive-or-upgrade — and UP-SEAT renders inside the Share dialog, next to the control that was attempted.)*

## New components

| Class | Purpose |
|---|---|
| `.meters` / `.meter` | a counter row: name · provenance chip · why it exists · **real reset time** · `used of limit` |
| `.mbar` / `.mbar.full` | neutral progress; brand tint at the cap. **Never red.** |
| `.m-src.rat` | "ratified" chip — hover gives the canon citation |
| `.m-unset` | "unset" chip — dashed, hover gives the owner decision required. **AMENDED: also carries the "recommendation — not ratified" state** (seats · CR-2-vs-governor) — a number the build carries that canon has **not** ratified. |
| `.census` | the in-product tier-definitions table; `.unsetrow` tints the undecided rows |
| `.upx*` | the prompt modal (kind chip `.upx-k`, `.upx-k.val` for value-class prompts) |
| `.partial` | the partial-orientation notice — warning-bordered, honesty-first |

## Chrome changes (Slice-9 corrections)

| Was | Now | Why |
|---|---|---|
| Sidebar chip button = **"Upgrade"** (permanent, every screen) | **"Your plan"** → opens *Usage & limits* | MON-04: **no persistent upgrade wallpaper** |
| Sidebar sub-line hard-coded `'10 projects · 10 seats'` | painted from `_projectCap()` / `_seatCap()` / `_allocCap()` | a hard-coded copy string is **how the invented "10" survived**. Numbers are painted from constants now, everywhere. |
| Workspace chip = "Free · **Upgrade**" | "Free · **Your plan**" | same |
| Export non-PDF buttons = `disabled` + lock chip | **enabled**; label chip reads "Basic"; the **attempt** prompts | D138 — never disabled, never hidden |
| Seat cap = a prose block with a compare link | prose + **resolution buttons**, free one first (**Add as Viewer — no seat**) | D138 — a prompt without a resolution is a wall |

## Runtime assertions (they run at boot, on every load)

`window._S10` carries the result of `_s10SelfCheck()`:

| Assertion | Fails loudly if… |
|---|---|
| `_assertNoDisabledLimitAffordances()` | any limit-bearing control is `disabled` (without `data-validation`) or hidden — **D138** |
| `_assertNoGenericUpgradeCopy()` | any friction prompt names no specific limit or no specific tier — **MON-04** |
| `_assertNoFabricatedNumbers()` *(AMENDED)* | (a) any genuinely unset value (**coalescing window · Free CRR cap · global prompt cap · billing rail**) has acquired a number — **Anti-Assumption**; **and (b) the MIRROR error** — a **ratified** value (price $12 · chat 75 · deep 6 · the envelopes) rendering as *unset*. *Crying "unset" over a decided value is the same lie, told backwards.* |
| `_assertNoFreePurchasePath()` *(new)* | a Free overage/top-up path exists — **DL-074 §3: overage is paid tiers only; Free converts via upgrade** |
| `_assertSeatCapsFlagged()` *(new)* | the seat caps are marked RATIFIED — **they are not** (§4c has no seat row below Team, and Basic=10 cannibalises a per-seat Team) |
| `_assertRecordNeverMetered()` | a cap appears on artifacts or History — **D128 P1** |
| `_assertEvidenceNeverGated()` | an evidence-driven analysis run is gated — **CR-2** |
| `_assertViewersUnlimited()` | the seat cap ever blocks a Viewer — **X-1** |
| `_assertNoEvictionOnDowngrade()` | a tier change removes a Membership — **D132** (from Slice 9; still green) |

These exist because a comment does not stop a future contributor (or a future model) from "just adding a tier check". **An assertion does.**

## Demo triggers (phase bar)

`Sim oversized project` (UP-4) · `Sim daily fixes used` (UP-1) · `Sim daily chat used` (UP-2) · `Sim deep runs used` (UP-5) · `Sim monthly budget gate` (UP-6) — plus the Slice-9 triggers (`Sim seat cap reached`, `Sim allocation spent`, `Sim reviewer response`). They **spend real meter units**; they never fake a state the product cannot actually reach.

---

# The readout (M4) — **D148–D154 · REBUILT** · components, state, guards

> **The last build was rejected.** It was a **modal**, and the report was **too meta** — it described OSLO's epistemic state instead of speaking to its reader. D148–D154 revise D144/D146/D147. What follows is the rebuild.

## D148 — Reports is a WORKSPACE, not a modal
`#reportsScrim` (the modal) is **DELETED**, along with `closeReports()` / `_reportsIsOpen()` and the Esc handler that closed it. Reports is now `<section class="pane" id="pane-reports">`, inside `.body`, **peer to Overview · Attention · Artifacts · Issues · History** — same nav (`#sbReports` → `showView('reports')`), same `.pane.active` switching, same `_scrollMem` / `_syncNav` / `_setCrumb` treatment. The toolbar `◕` (`#tbReport`) routes to the same view. `openReports()` survives only as a legacy alias → `showView('reports')`.

> ⚠️ **The two-column composer below was SUPERSEDED by D160 (reading surface sacred) and D161 (prototype-notes
> rail), and the document's rendering by D164 (visual parity).** The current zones are:

| Zone | Element | What it is |
|---|---|---|
| Toolbar | `.rw-bar` / **`#rptBar`** | **The only chrome resident on the reading surface** (D160). Recipient · Sections · Format · Export · Schedule, each opening a drawer — **every drawer CLOSED by default** — plus the D164 editor actions (undo · redo · insert · find), **resident, because there is no mode to enter**. It is a `SELLING_SURFACES` member (MON-04 / §7h guards run here). |
| Drawers | `.rw-drawer` / **`#rptDrawer`** | The controls, **on demand**. One open at a time. Esc closes. |
| **The MEMO** (export only) | `.rw-pkghost` / **`#rptPkgHost`** → `.pkg` / **`#rptPkg`** + **`.memo`** / **`#rptMemo`** | **The package wrapper** — PDF cover / share-link metadata. **The disclaimer lives here** (D153), with the mark and the analysis-currency chip — and **inside it, the MEMO** (`#rptMemo`): the card, the reading measure, its own quieter voice, **frozen and inert** (D168). **Always rendered; shown ONLY on the export preview.** *A cover is what the document travels ON, not something you read THROUGH.* |
| **The REPORT** | `.rw-page` → **`.report`** / **`#rptDoc`** → `.doc.m-doc` / **`#rptEd`** | **The living document (D168).** **Flush at the top-left of the pane, 720px, no card, no shadow, no side margins — the `.aw-center` / `.doc#artdoc` treatment exactly** (D164 visual parity). Furniture (title · byline · `To:` · rule · seven section headings) sits outside `#rptEd`, as `.art-head` sits outside `#artdoc`; `#rptEd` is **one always-editable `.doc`**. **ZERO OSLO vocabulary.** No selling. No meta. |
| Notes rail | `.rw-notes` / **`#reportsBody`** | **D161 prototype notes.** Renders **nothing** when the toggle is off. Sits **under** the document, never beside it. |

---

# ⚠️⚠️ AMENDED 2026-07-12 — **D168 IS RATIFIED. TWO OBJECTS, NOT ONE.**

> **The document has TWO STATES, and they are DIFFERENT OBJECTS.**

| | **REPORT** | **MEMO** |
|---|---|---|
| **What it is** | the **living document inside OSLO** | a **dated snapshot that has LEFT OSLO** — exported · shared · sent |
| **State** | editable · current · tracks the read | **fixed. It never changes again.** |
| **Presentation** | a **working document — artifact parity**: flush, top-left, `.doc` typography, continuous WYSIWYG. **No card. No shadow. No paper.** | a **memo — PAPER**: the card, the reading measure, **its own quieter typographic voice**; plus the cover, the **disclaimer** and the **currency marker** |
| **Doctrine** | **live understanding** | **a package** — *"packages existing understanding"* (Export spec) |
| **Element** | `#rptDoc` / **`.report`** → `#rptEd` / `.doc.m-doc` | `#rptMemo` / **`.memo`**, riding on `#rptPkg` / `.pkg` |

**This reconciles both prior instincts — each was right, in the wrong place.** The paper sheet was **not wrong; it
was applied to the wrong object.** A memo *should* look like a memo — but only once it **is** one. While it is
being written it is a **report**, and a report is a document. It lands exactly on D146: **you edit a REPORT; what
travels is a MEMO.**

## What changed

| | before (D164 state) | after (D168) |
|---|---|---|
| the live document | `.memo` — a class named for the wrong object | **`.report`** — flush, no card, `.doc` typography. **UNCHANGED visually. D164 parity is intact and guarded.** |
| the memo | did not exist as an object; the export preview showed only a cover | **`#rptMemo` / `.memo`** — the card (surface · border · 14px radius · `34px 40px 40px` · drop shadow), the reading measure (`64ch`), and **the quieter voice** |
| the quieter voice | **deleted** from `.memo p` (it beat `.doc p` on source order — a real defect, correctly removed) | **reinstated on `.memo .m-body`** — 13px / 1.75 / `var(--muted)`. **This closes the escalation: the voice belongs to the MEMO.** It cannot leak back: the memo body carries **no `.doc`**, and `.report` re-declares nothing. |
| both themes | the old card was a literal `background:#fff` — a **white sheet in a dark-default app** (D127) | the card is drawn from **tokens** (`var(--surface)`) with an explicit `:root[data-theme="light"] .memo` rule. **AA in both themes, on both surfaces.** |
| the furniture | `.memo .m-*` (scoped to one object) | **bare class selectors** — `.m-t` · `.m-by` · `.m-to` · `.m-rule` · `.m-risk` · `.m-alt` · `.m-app` · `.m-sign` · `.m-sec`. **Furniture is what makes a memo a memo** — not a font size and not a drop shadow — so both objects carry it and neither owns it. |
| `REPORT_SNAPSHOTS[]` | metadata only (`{id, fmt, stamp, run…}`) | **MEMOS**: `{title, by, toLine, body, sign, cover{disclaimer, mark, currency}, …}` — the **words**, frozen. `_deepFreeze()` at creation. |

## The memo surface

- Rendered by `_renderMemo()` into **`#rptMemo`**, inside `#rptPkgHost` — the **export preview**. It is **never on
  the reading surface** (D160: *the reading surface is sacred*).
- `_rptMemoView === null` → a **frozen PREVIEW** of what would travel, from the same factory (`_mkMemo`), so the
  PM previews **byte-for-byte** the memo they will get. A sent memo id → **that memo**, rendered from its own
  frozen bytes — never re-derived.
- The memo is `contenteditable="false"` and carries **no editor chrome**: no grips, no gentle note (D155), no
  "your words" badge, no Reset. `_rptCleanHTML()` strips all of it at capture. **Chrome does not travel.**
- The **cover** (`#rptPkg`) carries the ratified **disclaimer** (D153) and the mark; the **currency marker** is in
  the memo **body**, as plain attribution (`.m-by`). Unchanged from D153 — only the object it wraps is now real.

## D169 — History opens the sent memo (closes O-D168-2)

| Surface | Selector / function | Behaviour |
|---|---|---|
| **The History row** | `.hrow.clickable[onclick^="openMemoFromHistory"]` inside `#hist-list` | A **"memo sent"** event (`HISTORY[i].memo` = the memo id, set by `pushHistory`) renders as a **clickable, keyboard-operable** row (`role="button"` · `tabindex="0"` · Enter/Space) carrying **"open the memo →"**. Every other row is unchanged. |
| **The open path** | `openMemoFromHistory(id)` | Does **exactly one thing**: `_memoById(id)` → `_rptMemoView = m.id` → opens the export preview (`_rptDrawerOpen = 'exp'`) and re-renders. **It never calls the live composer** (`_mkMemo`), never touches the live report body (`_memoBodyHTML` / `_rptCleanHTML`), never re-cuts (`genReport`), **never runs an analysis** and **never appends to History**. |
| **The memo surface** | `_memoOnScreen()` → `_renderMemo(mos)` | For a selected sent id, returns the **frozen register entry itself** (identity — not a copy, not a rebuild); the `_mkMemo()` preview line is **unreachable** in that state. |
| **The cover** | `#rptPkg` (rendered from `mos`, **not** from `_readCurrency()`) | The memo arrives **on the cover it travelled on**: its mark, the ratified **disclaimer** (D153), and the currency marker of **its own run**. ⚠️ *Previously the cover was derived from the live read* — which would have silently **re-dated** a sent memo to today's run. **The only thing that moves is the LABEL** (*"previous analysis"* once the read overtakes it — D146/D168: a fact is qualified, never edited). |

> ⛔⛔ **THE LOAD-BEARING RULE.** *The memo is shown as it was sent — never re-rendered from current understanding.*
> Re-rendering it **silently rewrites history.** It is enforced by **mechanism**, because a re-render looks
> completely ordinary on screen: the open path is proven incapable of reaching the composer (source), the surface is
> proven to receive the **frozen object itself** (identity), and the state proof **counts composer invocations and
> requires zero**.

## Naming (D168 §4/§5 — partially closes the naming open item)

- The **live document** is a **report**. The **sent artifact** is a **memo**. In code, in labels, in History, in
  toasts. `_mkMemo()` names them `Memo N`; `genReport()` toasts *"Memo sent as PDF…"*; History reads *"Memo sent —
  a dated snapshot (PDF)"*; the memo's identity line reads *"Memo sent · 12 Jul 2026, 13:49 · PDF"*.
- **Still owner/glossary (DL-053):** whether the **workspace** is called "Reports"/"Readout". The toolbar still
  labels descriptively.

## The guards (D166 — mechanism, not copy)

| Guard | What it proves | Negative controls |
|---|---|---|
| `_assertReadoutIsFlushLikeAnArtifact()` | **the REPORT** is drawn as `#artdoc` is drawn. **Still derives its expectations from `.doc` / `.aw-center`** — it asserts `.report`'s measure **=== `.doc`'s** and `.rw-page`'s padding **=== `.aw-center`'s**, so it cannot go stale. It now also **pins its subject in the DOM**: `#rptDoc` wears `.report` and **not** `.memo`. | `flush_cardReturns` · `flush_lightCardReturns` · `flush_cardPaddingReturns` · `flush_centringReturns` · `flush_measureDivorcedFromDoc` · `flush_typographyDrifts` · `flush_refusesToGradeNothing` · `report_wearsTheMemosClass` |
| `_assertMemoIsPaper()` | **the MEMO** has the card, a reading measure, **its own voice** (`.memo .m-body p` font-size **≠** `.doc p`'s — derived, not hardcoded), a **light-theme rule**, no literal light hex in the base cascade, and it **cannot leak onto the report**. Reads the **authored cascade** — the same mechanism that finally caught the last invisible defect. | `memo_paperStripped` · `memo_whiteCardInDarkApp` · `memo_voiceDeleted` · `memo_voiceEqualsEditorVoice` · `memo_leaksOntoTheReport` · `memo_becomesEditable` |
| `_assertMemoIsImmutable()` | every memo is **deep-frozen** (cover included — a shallow freeze is caught); a live write is attempted and **must not land**; **no render path may write `REPORT_SNAPSHOTS[]`**. | `immutable_unfrozenMemo` · `immutable_shallowFreezeOnly` · `immutable_renderPathWritesMemos` |
| `_d168StateProof()` | **THE STATE PROOF.** Cut a memo → edit the report → **re-run an analysis** → the memo is **byte-identical** (`JSON.stringify`) and still renders the words it was cut with. | `memoNeverMovesWhenTheReportDoes` (a proof, not a bite) |
| `_assertReportAndMemoAreNotConfused()` | the two objects never wear each other's classes; the editor is never hosted on the memo; the memo's identity line says **memo**; `_mkMemo()` names them **Memo** (read from **source**, so a closed drawer cannot make it vacuous); **OSLO's own seeded prose** never calls the live document a memo. | `naming_liveDocumentCalledAMemo` · `naming_sentArtifactCalledAReport` · `naming_memosNamedSnapshots` · **`naming_pmMayWriteTheWordMemo`** (the exemption, proven) |
| **`_assertHistoryOpensTheFrozenMemo()`** *(D169)* | **the open path CANNOT reach the live composer.** Read from its own source: `_mkMemo` / `_memoBodyHTML` / `_rptCleanHTML` / `genReport` are forbidden on it, as is any analysis call and any mutation (`pushHistory`, `HISTORY.unshift`, `RPT_EDITS[…]=`). It **must** select the frozen entry (`_memoById` → `_rptMemoView`); the History row **must** wire it; both send paths **must** record the memo id, and `pushHistory()` **must** keep it. And `_memoOnScreen()` returns a sent memo **BY IDENTITY** out of the frozen register — graded live against the real register the moment one memo exists. | `d169_historyRowNoLongerOpensTheMemo` · **`d169_openPathReRendersFromCurrentUnderstanding`** · `d169_historyEventDropsTheMemoId` · `d169_openingAMemoWritesToHistory` · `d169_sentMemoIsRebuiltNotRetrieved` |
| **`_d169StateProof()`** *(D169)* | **THE STATE PROOF.** Cut a memo → **move the report AND the read** → **open it from its History event** → it is **byte-identical**, it renders the words it was **sent** with (not the current ones), it arrives **on its own cover** (its run, its disclaimer, relabelled *previous analysis*), it appends **nothing**, it runs **nothing** — and the **live composer was invoked ZERO times**. *A re-render is invisible on screen; it is caught by proving the code that could produce it never ran.* | `memoOpenedFromHistoryIsTheOneThatWasSent` (a proof) + **`d169_stateProofDetectsASilentRerender`** — a negative control **on the proof** |

> ⚠️ **A guard was fixed, not the doctrine (D166 §3).** The first draft of the naming guard scanned the **whole
> rendered memo** for the word *"report"* — and went red on *"Badge printing, the booth kit, and **the report the
> sponsors are owed**."* That is a **true sentence about the project**. The guard was **policing the document's
> prose**, and prose is the user's (D152/D155): a PM may write *"I'll send a memo to legal"* and OSLO has no
> business correcting them. The rule is about **OSLO's names for OSLO's objects** — so the guard now grades the
> memo's identity line, `_mkMemo()`'s source, and OSLO's own seeded sections only. **`data-pm="1"` is exempt, and
> `naming_pmMayWriteTheWordMemo` proves the exemption is real.**

## D150 — the seven sections (`[data-sec]`, fixed order)
`summary → changes → risks → assumptions → plan → decisions → appendix`. **Risks come BEFORE assumptions**: a reader who is going to stop reading must stop after the thing that could change the plan, not after the caveats. `_assertReportStructure()` walks the rendered document and fails on any other order.

## D149 — the governing writing rule
> **The doctrine governs what the report may CLAIM. It must NEVER govern how the report SOUNDS.**

`REPORT_OSLO_VOCAB` is the banned list (*confidence · CAF · clarity · alignment · feasibility · reliability · understanding maturity · assessability · artifact(s) · the read · issue(s) · derived · attested · recommendation · dimension · OSLO …*), word-boundary matched against the rendered `#rptDoc`, **with no denial exemption** — the memo may not even *deny* doctrine, because naming it is already speaking it. Sections the PM has rewritten carry `data-pm="1"` and are **exempt**: those are the PM's words, and OSLO does not police them (D152, advisory-only).

**The honesty is re-rendered as ordinary good writing:** *"The 500-device figure came from our plan, not from The Grid"* (derived-vs-attested) · *"Not yet confirmed with The Grid"* (evidence gap) · *"dates without owners are estimates, not commitments"* (low reliability) · *"the weak point here is people, not process"* (limiting dimension).

## D151 — two altitudes, and the knife-edge
Every risk renders `.m-alt` twice: **For the plan** (deliverable impact) and **For the goal** (outcome impact). Outcome impact is **"does the plan, AS WRITTEN, still reach its stated intent?"** — a **structural claim about the plan**. It is **not** *"will this project succeed?"*, which is a prediction and is forbidden (same P1 class as a health rating, DL-104 §5). `REPORT_FORECAST_WORDS` + `_assertNoForecastLanguageInReport()` guard the line.

## D152 — the plan of action is the PM's
`_memoPlan()` seeds first-person steps from `MEMO_PLAN_SEED` (built off the same recommendations OSLO already made). `_assertPlanOfActionIsPMVoiced()` requires first-person voice, **forbids the word OSLO in that section**, and requires the section to carry an **edit affordance** — a seed the PM cannot rewrite is not a seed; it is the tool writing the report.

## D153 — the disclaimer is a property of the package
`EXPORT_DISCLAIMER` renders in `#rptPkg` (and rides on `snap.cover.disclaimer` in every exported snapshot). The **memo body carries the currency marker as plain attribution** — *"DevNorth 2026 · plan as of 12 July · ‹name›"* — and **no disclaimer paragraph at all**. `_assertDisclaimerOnPackageNotInBody()` checks **both halves**.

## D154 — editing is free; the gate is reuse
| | Free | Basic |
|---|---|---|
| Edit any section, every week, from scratch | ✅ | ✅ |
| Full seven-section memo · PDF | ✅ | ✅ |
| **Your wording comes back next week** | ❌ | ✅ |
| Extra sections · branding · scheduling · all formats | ❌ | ✅ |

`_reportEditAllowed()` returns `true` unconditionally and **contains no tier check** — `_assertEditFreeOnEveryTier()` simulates every tier, reads the edit path's own source for a tier check or a `fireUP(`, and separately proves the tier lives in `_editsPersist()`. `RPT_EDITS` is in memory on every tier; `_saveEdits()` writes to localStorage **only on Basic**. `simNextWeek()` is the demo trigger that makes the gate testable rather than merely asserted.

## Runtime guards (`window._S10` — now **26** boot assertions)
`_assertReportStructure` · `_assertNoOsloVocabularyInReport` · `_assertNoForecastLanguageInReport` · `_assertPlanOfActionIsPMVoiced` · `_assertDisclaimerOnPackageNotInBody` · `_assertEditFreeOnEveryTier` · `_assertAskTailoredNeverTheRead` · `_assertReportPackagesNeverProduces` · `_assertScheduledReportRechecksCurrency` · `_assertReportsNoHealthFraming` — plus the 16 standing Slice-10 / DL-103 guards.

## Struck by this rebuild
`_assertReadoutSpineComplete()` · the `§1–§5` spine · `_spineRead()` / `_spineAsk()` / `_readoutSections()` (kept only as thin shims onto `_memoRead()` / `_memoDecisions()` / `_memoExtras()`) · the section titled *"How to read this"* · the headings *"What we don't know"* / *"What's limiting it"* · `#rptReadout` · `#reportsScrim` · `#reportsFoot`.

---

# ⬛ AMENDED 2026-07-12 — **D155 · D156 · D157 · D158**

## New DOM / CSS

| Element | Where | Notes |
|---|---|---|
| `.m-note` (`[data-oslo-note="1"]`, `role="note"`) | **inside** the `data-pm="1"` section of `#rptDoc`, **after** the PM's body HTML | **The gentle forecast note (D155).** Dashed border, `--cool` left rule, `--surface-2` fill. **No red, no urgency colour, no modal, no overlay** — nothing that reads as a refusal. **App chrome: like `.m-edit`, it does not travel in the exported package.** |
| `.m-note-b` / `.m-note-w` / `.m-note-s` | inside `.m-note` | body · the matched words (up to 3, then "and N more") · the closing line. |
| `.m-note-x` | inside `.m-note` | **The Dismiss button. Always present.** *A note the user cannot dismiss is a block wearing a friendlier face.* |
| *"If your words read as a forecast"* block | `#reportsBody` (the composer) | Explains the note **once**, on **OSLO's** surface. **Never in the document.** |

## New JS

| Symbol | Purpose |
|---|---|
| `REPORT_ADVISORY_WORDS` | `REPORT_FORECAST_WORDS.concat(REPORT_BANNED_FRAMINGS)` — **the same vocabulary the guards apply to OSLO's own prose.** |
| `_pmForecastHits(html)` | Word-boundary match over PM prose. Returns the hits. **Pure. Touches nothing.** |
| `RPT_NOTE_DISMISSED` / `dismissForecastNote(k)` | Per-section, in-memory dismissal. Cleared on save/reset (**new words, fresh advice**). |
| `_rptForecastNote(k, hits)` | **A pure renderer.** It cannot disable a control, fire an upgrade prompt, or reach the PM's text. |
| `_assertForecastNoteNeverBlocks()` | **D155 (1).** Send path cannot see the note · the note cannot disable/prompt/confirm · behaviourally, no send control is disabled while a note is live · the dismiss control exists. |
| `_assertOsloNeverRewritesPMProse()` | **D155 (2).** Only `saveReportSection` / `resetReportSection` may write `RPT_EDITS[...]` · every rendered PM section contains its stored text **byte-verbatim**. |
| `TIER_ORDER` / `_tierRank()` / `_beneathTier()` | **D158.** The tier name is demanded **only when the user is beneath the relieving tier**. |
| `MEMO_RISK_CAP = 5` | **D157.** ⬜ **Illustrative, not a ratified product value.** The truncation rule is an M4 spec item. |
| `REPORT_TO_LINE_STAYS = true` | **D156.** Addressing ≠ re-framing. The guard stays section-scoped. |

**`window._S10` now carries 28 boot assertions** (was 26): `+ noteNeverBlocks` `+ neverRewritesPM`. Both also run on **every** `renderReports()`.

---

# ⬛ AMENDED 2026-07-12 — **D165 · OSLO Chat is a CONVERSATION, not a wall**

## What was cut from the reply
The "ask about this issue" reply was a **document pretending to be a message** — 302 words of prose plus 2 evidence
cards, 4 action cards each with an explanatory subtitle, a clarification form with an **open textarea**, 3 in-message
chips **and** 3 different composer chips underneath. All of it **pushed**, in one turn, to answer one question.

| Removed from the resident reply | Where it lives now |
|---|---|
| *Why it matters* (full) + *What it weakens* | first sentence of `why` only; the rest is in the Issue panel |
| *My recommendation* + the paths | **"What would you do?"** · **"What are my options?"** |
| 2 evidence cards (`.chat-cites`) | **"What's it resting on?"** |
| reliability-basis paragraph (`.chat-rely`) | **"How sure are you?"** |
| epistemic **chip** + "I inferred this" **paragraph** | **one line**: *"I inferred this — it isn't in your inputs."* |
| 4 action cards + `.ca-cons` subtitles | **ONE** action, contextual. `_cAct()` now **ignores** its third argument. |
| clarification **open textarea** | **collapsed** one-line prompt, expands on click (`.chat-clar .cc-head` / `.cc-body`) |
| composer chips shown alongside in-message chips | composer chips are an **empty-state affordance only** |

## New DOM / CSS
- `.chat-div` — **context divider** (D165d). A record with `role:'div'`; a new context inserts one so a new issue's
  thread **reads as a new thread**. Emitted by `_chatDivider(label, key)`, keyed on `_pinKey(ctx)` — same context, no
  new divider.
- `.chat-clar .cc-head` / `.cc-chev` / `.cc-body` — the **collapsed** clarification (D165e), with hover, pointer and a
  rotating chevron. `.chat-clar.open .cc-body{display:block}`. Mirrors the Issue-panel affordance (D162c).
- `.chat-chips:empty{display:none}` — the composer chip row collapses to nothing when a conversation is underway.
- `.chat-act .ca-cons{display:none}` — the subtitles are gone; the class is retained only so a **pre-D165 persisted
  thread** in localStorage still renders sanely.

## New JS
- `_chatConvUnderway()` — a conversation is underway once the **user has spoken** or OSLO has produced a turn that
  carries **its own next moves**. The seed greeting is the empty state wearing a bubble; it does not count.
- `renderChatChips()` — clears the composer chips when underway. **Never two competing sets** (D165c).
- `_firstSentence(s)` · `_hand(list)` — the "why it matters" line (never a paraphrase — no fabrication) and the
  2–3-move handoff that **every** turn ends with.
- **The pull turns:** `_ansEvidence(ref,S)` · `_ansOptions(id,S)` · `_ansRecommendation(id,null,S)` ·
  `_ansReliability(S)`. Routed in `_oslloReply()` **before** the older broad routes, resolving against the issue
  named → in context → top.
- `chatClarToggle(id)` — the collapsed prompt expands to the input.
- `_clarHead(q)` — **D167:** truncates the question to **10 words** for the collapsed head. The **full** question is the first line inside the body (`.cc-q`) and the head's `title=`. **Truncation is presentation; the ask is intact.**
- `_chatProbeHTML(fn)` — **D167:** fences generation-with-side-effects. A guard that renders a real reply must **leave no trace**: while `_CHAT_PROBE` is up, `_retireClarBoxes()` is a no-op.
- `_productText(el)` — **D166:** the single definition of *what a guard may grade* — **what the USER sees**. It strips `.pn` / `.pn-i` (prototype notes: review apparatus, OFF by default, **never product copy** — D161).
- `_thinBasis()` compressed to a **single sentence**. **The trigger is unchanged** (derived-only basis + thin
  reliability): nothing became less honest, only shorter.

## Runtime guards (`window._S10` — now **37** boot assertions, +6)
| Guard | Proves |
|---|---|
| `chatOpeningShort` | the opening turn on **every** issue is **≤ 50 words** (D167), ends in a handoff, and carries **no** evidence cards, **no OPEN** clarification form, **≤1** action, **no** subtitles |
| `chatOpeningCarriesAsk` | **D167 (O-D165-1)** — for every issue with an **outstanding** clarification, the opening carries the **collapsed request** (expanding head + textarea behind it) **and** the *"Answer your question"* chip. **A request is not detail: it stays visible.** |
| `chatPullShort` | **D167 (O-D165-3)** — every pull turn (evidence · options · recommendation · reliability, **plus** the tier answers) is **≤ 40 words** and ends in a handoff |
| `chatDetailPullable` | the other half: evidence · options · recommendation · reliability each come back **in full** when asked, each ending in a handoff, and the reliability turn still states **Coverage · Evidence · How assessable** |
| `chatOneChipSet` | live DOM: never two suggestion sets **+ a mechanism proof** that drives the real `renderChatChips()` through both states (so it cannot pass vacuously on an unseeded rail) |
| `chatClarCollapsed` | the clarification block renders **collapsed**, computed `display:none` on the body, and the head really expands |
| `chatNeverMutates` | a **state proof**: a battery of **15** replies (including "apply the fix", "close ISS-01", "select the first path", "upgrade me") moves **nothing** — not a status, not a path, not a meter, not the read, not History — **and, since D167, not the thread either** (`_CHAT_MSGS` + `#chatscroll` innerHTML are in the snapshot) |
| `chatClarSamePath` | a chat-answered clarification still runs `_submitClarification()` → **byte-identical** History entry |

## Struck by this amendment
- `.ca-cons` action subtitles · `_CONS_OPEN_ISSUE` / `_CONS_DISCUSS` / `_consApply()` / `_consSelect()` (now no-ops).
- `_S10_CHAT_DISCLAIMER` — *"I can't upgrade you, buy anything, or lift a limit…"*, reprinted on every tier answer.
  It is a sentence about **what OSLO will never do** (banned, D163) and it is already stated **once**, in the
  composer's `↳ advisory ⓘ`. **The boundary is enforced in code, not recited in copy.**

---

# D170 / D170c / D171 — THE PROMPT ENGINE, THE POPOVERS, AND THE SEND

## The prompt surface — `.upx-scrim`
| | |
|---|---|
| **z-index** | **420** — strictly above **every** other rule in the cascade. It was **96**: the **lowest overlay in the product**, below the export dialog (`.scrim` 172), the issue flyout (`#issueScrim` 260 / `#issueClose` 262), the palette (250), the notifications panel (236), the phase bar (200), settings (122) and the workspace home (120). **Gated attempts are made from those surfaces** — the prompt rendered *behind the thing the user was looking at.* |
| **Guard** | `_assertPromptSurfaceIsOnTop()` — parses the **authored cascade**, takes the max z-index of every rule, and demands `.upx-scrim` beat it. **Derived, so it cannot go stale**: add a surface above the prompt and it goes red at the next boot. |

## The prompt engine — two kinds of prompt
| | **SOLICITED** (`cls:'value'`) | **GATED ATTEMPT** (`cls:'friction'`) |
|---|---|---|
| Who started it | **the product** (UP-7, UP-8) | **the user** — they clicked a live control and the product refused |
| What it is | a nudge | **the reason the click did nothing**, plus the way out |
| Cadence caps (cooldown · per-day) | **apply** | ⛔ **never apply.** A cap on nagging may not silence an answer. |
| Before first value / mid-pass | not fired | **DEFERRED, never dropped** — queued, fired at the first legal moment; the user is told immediately (toast, ≤12 words, no CTA) |
| Derived from | `UPROMPTS[id].cls` — **the ratified table**, never a flag at the call site | same |

**Router:** `fireUP()` → `_upRoute()`. **There is no path out of `_upRoute()` that renders nothing.**
UP-8 → chat · UP-4 → `renderPartial()` · UP-3 → `openUpgrade()` · UP-SEAT → the Share dialog · everything else → `_renderUP()`.

## The Readout toolbar — **popovers, not drawers** (D170c)
`Readout` · undo/redo/insert/find · **Recipient** · **Sections** · **Format** · **Schedule** · ⟶ · **Send** *(primary)* · **Export**

| | |
|---|---|
| **Was** | `.rw-drawer` — a full-width band **in the flow**. Opening *Recipient* **pushed the document down the screen**; closing it yanked it back. **The user was reading a paragraph, and the paragraph moved.** |
| **Now** | `.rw-pop` — `position:fixed`, **anchored to the button that opened it** (`_anchorRptPop()` measures the button and clamps to the viewport). **Out of the flow entirely: the document does not move by a pixel** (D160). |
| **Keyboard** | **Esc closes** · **focus trapped** (Tab cycles inside) · focus **returns to the anchor button** on close · `aria-expanded` + `aria-haspopup="dialog"` on every button |
| **Mouse** | click-outside closes · one open at a time |
| **Guard** | `_assertToolbarMenusArePopovers()` — reads the cascade (**last `position:` wins**, as the cascade does) and the live DOM |

**The memo is not a toolbar menu.** `#rptMemoHost` (was `#rptPkgHost`) shows **only when the PM asks for it** — a
preview ("Preview what travels"), a memo they sent, or a memo opened from History. Opening a *menu* no longer drags the
memo onto the screen.

## SEND (D171) — `#rptSendBtn` → `sendMemo()`
| | **SHARE / SEND** | **EXPORT** |
|---|---|---|
| What | the memo goes to **named people** — a read-only copy on a link that routes **back into OSLO** | the memo becomes a **file** the PM handles themselves — **it leaves OSLO** |
| Tier | ⛔ **FREE ON EVERY TIER.** No lock chip. No tier branch. No meter. **CHG-061 — the seed is never gated.** | **formats** are tier-bound (MON-01 — Free = PDF) |
| Both | freeze a **MEMO** through **ONE factory** (`_mkMemo`, `sent_via:'shared'\|'exported'`) · run **NO analysis** (D146) · append a **History event** that **opens that exact memo** (D169) | |

---

# D172 — REPORTS (the workspace) · READOUT (the document)

## The registry — `REPORT_TYPES`
```js
const REPORT_TYPES = [ {k:'readout', nm:'Readout', doc:'Readout', workspace:'Reports', render:…} ];
```
**One entry. The Readout.** A second report type is an **ADDITION to this array**, not a rebuild of the workspace.
⛔ **NO SPECULATIVE UI FOR REPORTS THAT DO NOT EXIST** — no picker, no gallery, no cards. *That is exactly how the
six-card scaffold happened the first time.* **D143 stands.** → `_assertReportsHostsOneReportType()` (registry **and**
DOM **and** the names) · NCs `aSecondReportTypeMayNotBeRegistered` · `theSixCardScaffoldMayNotReturn`.

| Surface | Says |
|---|---|
| Sidebar `#sbReports` · top-bar `#tbReport` · crumb (`_viewLabel('reports')`) | **Reports** — the workspace |
| The readout toolbar `.rb-t` (from `_readoutDocName()`) | **Readout** — the document |
| The thing that travels (`_mkMemo` → `.m-stamp`) | **Memo** — dated, frozen, gone (D168) |

## SCHEDULE (D172a/D172b) — `#rptSchBtn` → `toggleReportSchedule()` → `runScheduledReport()`
- **The automation is Basic** — the tier check lives at the **toggle**, and nowhere else. The control stays **live** on
  Free (D138); the **attempt** fires `UP-REPORT {sched:true}` → **"Basic sends it for you every Friday"**, ≤30 words,
  resolutions **free-first** (*Send it now*).
- **The send is free** — `sendMemo()` has **no tier branch and may never have one** (CHG-061).
- When it fires it takes the **manual send's path exactly**: `sent_via:'shared'`, a scoped grant, a **`share`** History
  event that **opens the frozen memo** (D169) — and a **currency re-check** (D147) that labels a stale read
  **"previous analysis."**

## THE SHARED MEMO (D172c) — `openSharedMemo()` → `#reviewerView`
Rendered on the **reviewer-grant surface**, because it **is** a reviewer-grant: a **scoped, token-granted, read-only
view**. `_mkLink('memo', id)` + `_grantScopedAccess('memo', …)` — **the same two functions the CRR grant uses.**
**The link IS the invite, and the invite IS the authentication** — no signup wall, nobody anonymous (DL-021).
The recipient's memo (`#rvvMemo`) is `contenteditable="false"`, wears `.memo` (never `.report`), and is rendered from
**the memo's own frozen bytes** (`_memoPaperHTML`) — the open path **cannot reach** `_mkMemo` / `_memoBodyHTML`.

---

## Reports surface — Strategic Readout (WI-R1)

**Where it lives.** Inside the existing **export/snapshot modal** (`#exportScrim`), rendered by `renderExport()`
(which now calls `sroRender()`). No new route, nav item or modal — the composer sits between the export
currency/disclaimer block and the Format picker. The reference `#exportModal` → this `#exportScrim` is the 1:1
mapping (the reference upgraded "only the export surface").

**Markup (inside `.wm-b`).**
- `.wm-lab` — "Strategic readout — the five-section read · naming pending".
- `.sro-draftbar` — "Assembled from what OSLO already understands… Generating a snapshot runs no analysis."
- `.sro-bind` — the **DL-108 binding banner**: "The read (§1–§3 and §5) is identical for every audience. Only §4
  is addressed to the recipient… forbidden by DL-108."
- `.sro-aud#sroAud` — audience selector: **four** `.sro-audbtn` built by `sroRender()` from `REPORT_RECIPIENTS` (Sponsor / Programme lead / Operations / Executive-board — WI-R2); `.on` marks the active
  one; each `onclick="sroSetAudience(k)"`.
- `.sro-doc#sroDoc` — the live spine, assembled by `sroRender()` into `.sro-sec` blocks (`.sro-sh`/`.sro-num` head,
  `.sro-sb` body; §4 carries `.sro-ask` dashed outline + `.sro-askmark` note).
- `.sro-opts` — four optional-section checkboxes with a `.sro-tier` "Basic" chip; `onchange="sroToggleOpt(k,…)"`.
- `.sro-cap` — Free-vs-Basic framing; "the seed… is never gated".

**CSS.** All classes are **namespaced `.sro-*`** on purpose — the Readout **workspace** already owns `.ro-*`
(`.ro-h` / `.ro-cur` / `.ro-foot`); the two must never be merged. Tokens are the slice-10 theme (`--primary`,
`--surface`, `--success`, etc.); nothing hard-codes a colour.

**JS.** `const SRO = {aud, opts}` holds composer state. Builders: `sroRead` `sroLimit` `sroUnknowns` `sroAsk`
`sroHow` `sroOpt`; `sroRender()` re-assembles `#sroDoc` and syncs the audience buttons; `sroSetAudience` /
`sroToggleOpt` mutate `SRO` then re-render. Every builder reads slice-10's own data (`ISSUES`, `_istatus`,
`_readCurrency`, `_chatState`, `_openClarIds`, `_epiOf`, `_ARTORDER`, `dispName`, `TREND`) — **v4's model was not
imported.** Only `sroAsk()` reads `SRO.aud`.

---

# D173 — THE PAYOFF (owner-directed, 2026-07-12)

## The card
`#payoff` — a `.card.payoff` at the **top of the Overview**, above Confidence. Hidden until an analysis update
lands. Five slots, in this order, always: `#pay-act` (what you did) · `#pay-band` (the band transition) ·
`#pay-note` (the fall sentence, or the released-limiter clause) · `#pay-counts` (the true counts, as `.pay-count`
pills) · `#pay-limit` (what the limit is now). `.pn-slot#pnPayoff` carries the D161 notes layer.

⛔ **There is no `.payoff.up` and no `.payoff.down`.** The block has **one** styling, and it contains **no colour
token at all** (`--success` / `--danger` / `--warning` / `--conf-*` are absent from every `.payoff` rule). A rise
and a fall render through the same classes at the same weight (D173c / D003).

## The engine
| Function | What it does |
|---|---|
| `_cafOf(r)` / `_limitingOf(r)` | the CAF triple and the lowest dimension. **One source** — `_chatCaf()` now delegates here, so the chat, the payoff and the Overview cannot disagree about the limit. |
| `PAYOFF_COUNTS[]` | **the only numbers the payoff may speak.** Each row is `{key, label, get(), of?}`; `get()` reads live state. There is nowhere to type a number in. |
| `_readSnapshot()` | `{caf, rel, limiting, counts, of}`. A `get()` that cannot produce a number ⇒ **the key is absent** ⇒ it cannot be rendered. ⛔ **`idx` is deliberately not in the snapshot**, so a delta on the index is not formable. |
| `_payoffModel(before, after, act)` | differences only: band transitions (CAF + reliability), moved counts, `fell`, `limitHeld`, `released`. |
| `_payoffParts(m)` / `_payoffProbe(m)` | the copy and a detached render — **the same parts the card uses**, so the guards grade the real thing. |
| `_payoffFit(m)` | D163 budget (**≤45 words**). Drops the optional clause, then trailing counts. **Never** the action, the band, the fall note or the limiter. |
| `renderPayoff(before, act)` | called by `applyFix` · `_submitClarification` · `deepComplete` · `_reviewAnalysisRun`. `before` is snapshotted **before the user acted**. |
| `_firmFeasibility(f)` | the one place Feasibility moves on a cleared critical resourcing gap. Width moves; **the band is derived** by `_cafLevelFor` — never typed in. |

## ⛔⛔ THE HERO IS THE MATURITY RAMP (D174 — supersedes the D173d band-word hero)

D173d demoted the index and left **one word in 40px**. That is a *label*, not a hero. **D003 already mandated a
neutral maturity ramp** and it had never been drawn. It is drawn now: **five ordinal steps, the current one lit.**

```
Very Low   ·   Low   ·   [ MODERATE ]   ·   High   ·   Very High
 ▬▬▬▬       ▬▬▬▬        ██████████        ▬▬▬▬        ▬▬▬▬
```

| Element | DOM / CSS | Computed from |
|---|---|---|
| **1. The ramp** | `#ov-ramp` · `.ramp > .rstep(.on) > .rbar + (.rlab \| .bandhero)` | `_rampHTML(band)` maps **`_BANDORD`** (DL-086/098). The lit step is `_BANDORD.indexOf(currentRead().band)`. **No band word exists in the static markup.** |
| **2. The reliability qualifier** | `.cr-qual` → `#ov-rel` | `currentRead().rel` — *"on moderate reliability"* (D002/D051) |
| **3. The limiter** | `#ov-limit` | `_limitingOf(r).dim` — the lowest CAF dimension. The same computation that marks the `.cafrow.lim` row |
| **4. The direction + its cause** | `#ov-trend` / `#ov-trend-lab` | `_readDirection()` + `_readCause()` (= the last `TREND` run's cause). **Only rendered when `_directionIsComputable()`** — a direction needs two runs; one run ⇒ it is not shown (D173) |
| **5. The 0–100 index** | `.conf-focus .num .idxline` → `#ov-idx` (**15px**) | `currentRead().idx`. **Secondary aggregate. No delta, ever** |

**ONE painter:** `renderHero(r)` writes all five; `renderOverview()` and the boot both call it, so the hero is never
a stale hand-written value. **`pushTrend()` re-paints the hero** — the direction lives on the record, and
`deepComplete()` re-renders the read *before* it appends the run (defect found in build: the direction stayed
hidden after the Extended pass).

### Neutrality — the ramp is a MATURITY scale, not a HEALTH bar (D003 · DL-104 §5)
- **Colour allowlist, enforced in the CASCADE** (`RAMP_ALLOWED_COLOUR_TOKENS`): only `--text · --muted · --subtle ·
  --border · --border-2 · --surface*` may colour the ramp. **No `--success` / `--danger` / `--warning`, no
  `--conf-*`, and not even the brand `--primary`** — an amber-adjacent orange is exactly how a user reads "at risk".
- **No percentage fill.** Every step is an identical fixed segment; **exactly one is lit** (`.rstep.on`). Steps
  below the read are **not** filled in — a 1..n fill is a progress bar, and a progress bar is a health bar with
  better manners.
- The lit step is separated by **weight**, never hue: `--text` at 9px vs `--subtle` at 7px; the word is 32px.
- **AA, both themes**: lit word 15.1:1 (dark) / 16.6:1 (light) · labels 8.8 / 8.0 · unlit bar **5.3 / 5.2** (it was
  `--border-2` at **1.7:1** — under the 3:1 graphics floor — and was fixed to `--subtle`).

## ⛔⛔ D175 — THE ANALYSIS-STATE CHIP IS NEUTRAL, AND THE ALLOWLIST NOW GOVERNS THE WHOLE CARD

**The D174 guard was scoped to the confidence FOCUS. The defect was one element outside it, inside the same CARD.**

`.ustate.prov` was `--warning` (**amber**) and `.ustate.cur` was `--success` (**green**) — the Provisional ↔ Current
chip (**D040**), sitting in the hero card's header **one line above the five-step maturity ramp**. Each was
*technically* honest on its own: it describes the **analysis state**, not the project. **But amber-and-green
directly above a five-step scale is exactly the adjacency a reader turns into RAG** — the **P1 health-framing class
(DL-104 §5)** arriving **through a side door**: not from what either element *says*, but from **what they say
together**. *(And the amber was written as a raw literal — `rgba(217,164,65,.08)` — so a token blacklist would have
missed it too.)*

| | Before (D040) | After (D175) |
|---|---|---|
| **Provisional** | `--warning` text · amber border · amber wash | **hollow ring dot** · `--muted` · weight **600** · `--surface-2` |
| **Current** | `--success` text · green border · green wash | **filled dot** · `--text` · weight **700** · `--surface-3` · `--subtle` border |
| **Last-good** | (the provisional treatment) | (the provisional treatment — the read on screen *is* the last good one) |

- **The labels are UNCHANGED** (D040). *Provisional · Current · Last-good* are honest and they stay. **Only the
  colour went.** The information was **de-judged, not deleted** — Provisional/Current is a **STATE**, not a
  **JUDGMENT**, and **a dot and a word carry it**.
- **Legible by WEIGHT and SHAPE, never by HUE** — the D174 precedent (the lit ramp step is separated by weight, not
  hue). A colour-blind reader sees the same two states everyone else does.
- **AA, both themes:** *Provisional* **7.7:1** (dark) / **7.3:1** (light) · *Current* **11.6 / 13.4** · the dot (a
  meaningful graphic, 3:1 floor) **4.7 / 4.8** hollow, **11.6 / 13.4** filled. All pass.

### The guard's scope is now THE CARD (`_assertHeroCardCarriesNoSeverityColour()`)
- **No severity/health token may colour ANY rule that can select a hero-card element** — `--success` · `--warning` ·
  `--danger` · `--conf-*` — **and no chromatic literal** (graded by **chroma**, because the defect was written as a
  raw `rgba()` with the token name filed off; greyscale and transparent pass, hue does not). Inline styles too.
- **Read from the AUTHORED CASCADE, not the DOM.** The green lived on `.cur` — **a state that was not on screen**.
  No DOM guard was ever going to see it.
- **The scope is DERIVED from the live card** (every class/id on a hero element, minus generic state modifiers like
  `.on`, plus the card's real ancestor chain), so it cannot go stale — and it **does not leak** onto other surfaces
  (`.issue .card`, `.tog.on` stay out; proven by a must-not-fire control).
- ~~**Two tiers, deliberately: brand ≠ severity.** `--primary` stays legal **on the card**…~~ ⛔ **SUPERSEDED BY
  D176a: `--primary` IS NOW BANNED CARD-WIDE.** *Brand ≠ severity* was the right distinction and the wrong
  conclusion: **D174 banned `--primary` from the ramp precisely because an amber-adjacent orange invites "amber =
  at risk"**, and the CAF **limiter row** wore it **three lines under the ramp, inside the same card**. The card's
  banned list is now `HERO_CARD_BANNED_TOKEN_RE` = `--success · --warning · --danger · --error · --crit · --conf-* ·
  --primary*` **+ every chromatic literal**. **Emphasis by weight, never by hue.**
- **The D161 notes rail is excluded** — it *legitimately* speaks in `--warning`; a guard that graded it would be
  failing on its own documentation.
- ⚠️ **Its own negative control found a hole in it:** the first draft read a selector as everything before the
  *first* `{`, so a severity rule hidden in an **`@media` block** was invisible. `_cssSelOf()` / `_cssBodyOf()` now
  shed the at-rule prefix. **Fix the guard, never the doctrine** (D166 §3).

## The index (D173d, unchanged in substance)
`#ov-idx` survives at **15px** in `.idxline` — a **secondary aggregate**, printing `58/100` and **nothing else**:
no delta, no arrow, no verdict. **Demoted, not deleted** — the owner may calibrate it (DL-062 F1) and take the hero
slot back; `_assertNoIndexDelta()` fails **both** if a delta appears **and** if the number is deleted or climbs back
above the lit band (the CSS clause now grades `.ramp .rstep.on .bandhero` vs `.conf-focus .num .idx`).

## Neutral direction, everywhere
`.trend-arrow`, the History run chips and the `.ct-x` trend arrows were **green ▲ / amber ▼**. They are now
`var(--muted)` in both directions (D003), and the Overview trend row is computed (`renderOvTrend()` /
`_readDirection()`) — it was **hard-coded to rise**, so a read that fell was drawn as a read that rose.

## ⛔⛔ D176 — THE LIMITER ROW LOSES THE ORANGE; THE CAF BARS WERE FALSE PRECISION

### D176a — the limiter is a FACT, not a WARNING (closes O-D175-1)
`.cafrow.lim` marked the limiting CAF dimension in **brand orange** (`--primary` / `--primary-light`, **#D97A3A**) —
the row name, the bar fill and the band word — **three lines under the maturity ramp, inside the same hero card**.
`--primary` is not a severity token, so D175's rule did not reach it. **D174's own reasoning does:** it banned
`--primary` *from the ramp* **precisely because an amber-adjacent orange invites "amber = at risk."**

> **The limiter is a FACT — *"Feasibility is holding it back"* — not a WARNING.** It needs **emphasis**, and
> **weight gives emphasis**. Orange gives it a temperature it has not earned.

| | Before | After (D176a) |
|---|---|---|
| **Limiter row name** (`.cafrow.lim .cn`) | `--primary-light` | `--text`, weight **600**, `--subtle` underline |
| **Limiter band word** (`.cafrow.lim .cafband`) | `--primary-light` | `--text`, weight **700** |
| **Limiter marker** | *(the colour was the marker)* | the **word "the limit"** (`.cafmark`), rendered from `_limitingOf()` |
| **Footer links** (`.conf-foot .lnk2`) | `--primary-light` | `--text` + a dotted underline (the affordance, without the hue) |
| **How-calc bullet** (`.howcalc-pop li .d`) | `--primary-light` | `--muted` (AA: `--subtle` on `--surface-3` is 4.1:1) |
| **Stage word** (`.cpp-stage b`, popover) | `--primary-light` | `--text` (same rule, one line above the CAF ramps) |

**Zero hue in the hero card.** AA holds in both themes: limiter row **15.1 : 1** (dark) / **16.6 : 1** (light);
level word and marker `--muted` **8.8 / 8.0**; links **15.1 / 16.6**.

### D176b — the CAF dimensions are BANDS, not percentages (closes O-D175-2)
The confidence popover drew each dimension as **a bar filled to a percentage** (`cpp-feas-bar`,
`style.width = r.feasW + '%'`), and the hero card's rows did the same (`.caftrk` / `.caffil`).

> **A bar filled to 55% asserts a CARDINAL MAGNITUDE OSLO cannot defend**, on the same uncalibrated scale
> (**DL-062 F1 — Open-TBD**). **It is WORSE than the 0–100 index**, because **a filled bar reads as a measurement
> without even showing its number** — and a **partial fill is the visual grammar of a PROGRESS / HEALTH bar**
> (**DL-104 §5 — P1**).

- **Every CAF dimension now renders on the hero's own five-step ordinal ramp** — *Very Low · Low · Moderate · High ·
  Very High* (**DL-086/098**) — on **both** surfaces (Overview hero card **and** confidence popover).
- **ONE BUILDER, ONE MENTAL MODEL.** `_rampHTML(lvl, {compact:true})` — the same function that draws the hero.
  Equal segments, **exactly one lit**, no fill, no hue. The level word sits beside the row; the ramp's `aria-label`
  states the ordinal position (*"Feasibility: Very Low. Step 1 of 5 — Very Low, Low, Moderate, High, Very High."*).
- **The limiter is marked in words and weight**, on both surfaces, from `_limitingOf()`. The popover carries a
  one-line note: ***"Feasibility is holding it back — the lowest of the three. It is a fact about the read, not a
  warning about the project."***
- **The reliability basis rows lost their fills too** (Coverage · Evidence availability · How assessable). They now
  carry **their level word alone**. They are **not** drawn on the five-band ramp: reliability is a **different
  scale** and OSLO does not invent one → **O-D176-1**.
- **`_RELPCT` and `_RELCOLOR` are deleted.** A level is not a percentage; a maturity level is not a colour.
- **The widths stay in the MODEL.** `feasW` / `alignW` still compute the band through `_cafLevelFor()` — the model
  may hold a number the product may not draw.
- ⛔ **The Attention heat map is UNCHANGED and CORRECT AS-IS.** Those cells **are issues**, and **severity colour
  belongs to issues alone** (D003 / D060).

### The guards (mechanism, not copy — D166)
| Guard | What it proves |
|---|---|
| `_assertHeroCardCarriesNoSeverityColour()` | **No hue on the hero card** — severity **and** `--primary` **and** any chromatic literal, graded from the **authored cascade** (chroma, not token names; `@media`-aware), inline styles included. Its own NC forced a scope fix: a **bare subject** (`.cr-limit b{color:rgb(217,122,58)}`) used to slip through. |
| `_assertNoPercentageFillOnMaturitySurfaces()` | **No percentage fill on any confidence/CAF/reliability element** — proven in **three places**: the **cascade** (any rule mentioning a maturity class), the **DOM** (inline styles), and the **RENDER PATH** (no painter may write `style.width`). The old fill was written by **JavaScript** — a cascade-only guard would have been theatre. |
| `_assertCafDimensionsRenderAsBands()` | Each dimension's ramp is graded **byte-for-byte** against `_rampHTML(lvl,{compact:true})`; the **lit step is computed from the read**; the **limiter is `_limitingOf()`**; and the whole thing is re-graded after **moving the read** (a hard-coded band passes the first pass and fails this one). |

**`_d176NegativeControls()` — 15 injected regressions, every one bites; 2 must-not-fire controls stay green**
(severity colour on **ISSUES** is untouched; the Progress card's **true-count** bars with their denominators on
screen are not reached → **O-D176-2**).

---

# D177 — THE EXTENDED PASS MOVES BOTH THE BAND AND THE COUNTS (owner, 2026-07-12)

**A data fix, not a code fix.** `_readSnapshot()` / `_payoffModel()` / `renderPayoff()` were already correct. What
was missing was a Deep Pass that **changed anything countable**.

## The mechanism

| Symbol | Contract |
|---|---|
| `DEEP_FINDINGS` | The two issues a deeper read of the **same** artifacts surfaces (ISS-07 critical · ISS-08 moderate). Same shape as `ISSUES`. **Absent from `ISSUES` and `_istatus` at boot.** |
| `_deepPassSurfaceFindings()` | **The one door.** Merges them into `ISSUES` + `_istatus`, idempotently, and **returns the ids it surfaced** — so the payoff, the chat line and the History delta are all computed from what actually happened. |
| `deepComplete()` | `before = _readSnapshot()` → **surface the findings** → `ANALYSIS_STATE='current'` → re-render the issue surfaces (focus · clarifications · heat · counts · issues list · the open artifact) → `renderPayoff(before, 'Extended Analysis landed.')`. |
| `_payoffModel()` | Adds **`learned`** — true when a CAF band rose **and** the `issues` count rose **and** nothing fell. **No flag is passed in**: it is read off the transitions, so **a run that did not earn the sentence cannot claim it.** `foundN` is the count delta. |
| `_payoffParts()` | The note: *"I looked deeper and found two more. The read is firmer because I know more."* — `_numWord(foundN)`, computed. |
| `_payoffFit()` | If the budget ever trimmed the `issues` row away, **`learned` is dropped with it** — the sentence may never outlive the count it describes. |
| Markup order | `pay-act` · `pay-band` · **`pay-counts`** · `pay-note` · `pay-limit`. The counts land **before** the line about them. `_payoffProbe()` renders the same order, so the guards grade the real thing. |
| `_a()` | Resolves its popover copy through `ISSUES` **or** `DEEP_FINDINGS` — the span is authored into the artifact at boot; `_artBodyLive()` keeps it **inert (plain text)** until `_istatus[id]==='open'`. **The weak text was always there.** |
| CSS | `.pay-note{margin-top:9px}` (now under the counts). **No colour token enters `.payoff`, in either direction.** |

## The guard

**`_assertDeepPassMovesBandAndCounts()` — a STATE proof.** It snapshots the world, puts the app back on the
Fast-Pass read with the findings unfound, **runs the real `deepComplete()`** (not a re-implementation), and asserts
from state: the band **rose** · the issue count **rose** · the critical count **rose** · the payoff rendered **all
three parts** plus the plain line · `foundN` equals the state delta · **≤45 words**. It also proves the findings
are **not invented** (real artifact · real CAF dimension · real citations · a real span in `ARTBODY`). Then it
restores `ISSUES` · `_istatus` · `HISTORY` · `TREND` · the chat · the payoff — **it leaves no trace** (D166).

**`_d177NegativeControls()` — 11 injected regressions, every one bites; 1 must-not-fire control stays green.**
**NC-D177-01 is the bug that shipped:** the Extended pass surfaces nothing, and the payoff claims a deeper read
anyway. The must-not-fire control is the shipped state itself — **more issues with a higher band must stay green**,
or the guard would be enforcing *"confidence = health"*, the exact misreading the doctrine exists to prevent.

---

# D178 — AND IT **ASKS** (owner, 2026-07-12 — closes O-D177-2)

> **Finding an issue and knowing what would close it are different acts — and OSLO can do both.**

**No new surface. No new component. One `clar` field, and the machinery that already existed does the rest.**

| Symbol | Contract |
|---|---|
| `DEEP_FINDINGS['ISS-07'].clar` | The ask the deeper read raises: *"Is there a minimum signed-sponsorship floor — or a cancellation point — that has to be cleared before the AV and catering commitments go firm?"* Same field, same shape as ISS-01/ISS-02. **It re-reads the evidence ISS-07 already cites — no new facts.** |
| `_openClarIds()` | **Unchanged** — and that is the point. It already backs the `questions` row of `PAYOFF_COUNTS`, so surfacing ISS-07 moves **Open questions 2 → 3** with no new code. **Computed, never typed in.** |
| `_payoffModel()` | Adds **`asked`** — the **rise** in the `questions` row. Read off the transitions, exactly like `learned`: **no flag is passed in**, so a run that raised nothing cannot claim an ask, and **answering** a question (the row *falls*) yields `asked = 0`. |
| `_payoffNote()` | **NEW** — assembles the note from the transitions: *found more* · *still asking* · *the read is firmer*. Each clause is spoken **only if the count behind it moved**. |
| `_payoffFit()` | If the budget ever trimmed the `questions` row, **`asked` is dropped with it** — the ask may never outlive the count that evidences it (the same discipline as `learned`). |
| `deepComplete()` | `_asked = _found.filter(id => ISSUES[id].clar)` — derived from what the pass **actually surfaced**. |
| `postDeepPassComplete(found, crit, asked)` | The completion turn now ends with *"There's 1 thing I still need from you:"* + `_chatClarBlock(id)` — the ordinary **collapsed** chat request (D165e). Answering it there runs `_submitClarification()` — **the same path the panel runs**. |

## The panel and the chat are the same event

The ask renders **collapsed** in both (D162c/D165e) — a one-line prompt that expands to the input on click:

| surface | rendered by | answered by | → |
|---|---|---|---|
| **Issue panel** | `_ipRowHTML(id,'clar',…)` | `answerClarification(id)` | `_submitClarification(id, val, **'panel'**)` |
| **OSLO chat** | `_chatClarBlock(id)` | `answerClarificationFromChat(id)` | `_submitClarification(id, val, **'chat'**)` |

**One path. One set of state changes. A byte-identical History entry** (D096 — verified field-for-field in jsdom).
The **only** difference is which surface reports back. **Advisory-only: answering triggers an analysis update; it
never resolves the issue by hand** (`open → Addressed → Resolved`, D088).

## The guard

**`_assertDeepPassMovesBandAndCounts()` now grades the ask, from state:** at least one finding carries a **real
question** (a `clar.q` containing a `?` — **OSLO asks, it never asserts**) · the **open-questions count rose** ·
`m.asked` **equals the state delta** · and the **`Open questions` row is on the rendered surface**, not merely in
the model. **Three new negative controls, all biting:**

- **NC-D178-01 — the Deep Pass raises no clarification.** It finds the gap and only **flags** it. **The guard goes red.**
- **NC-D178-02 — the payoff swallows the ask.** The count moved; the user was never told. **Red.**
- **NC-D178-03 — OSLO asserts instead of asking** (*"the sponsorship floor is $250k"*). **A fabricated fact. Red.**

**⛔ And the guard leaves no trace.** The real pass now **raises a clarification in the chat**, and raising one
retires any earlier live answer box for that issue (`_retireClarBoxes`) — which, run inside a guard, would reach
into the user's own thread and **disable a box they were about to type into**. `_CHAT_PROBE` fences exactly that
housekeeping. Verified: the live `chatClarBox-ISS-07` is **byte-for-byte unchanged** after the guard and all 13
controls run (D166).

---

# D179 — OVERVIEW LAYOUT: **STATE OUTRANKS EVENT · COUNTS HAVE ONE HOME · COLOUR WITHOUT RAG** (owner, 2026-07-12)

**Four owner findings, all correct.** The resulting layout:

> **HERO (the state)  →  PAYOFF (the event: dismissible, movement drawn on the ramp, ≤20 words)  →  PROGRESS (the counts, one home, deltas annotated)**

## D179a — the Confidence card is the **FIRST PANEL** of the Overview. Always.

| | |
|---|---|
| **Was** | `.card.payoff` was authored **above** `.card.hero` in `#pane-overview .uc`, pushing the state down the page. |
| **Now** | The hero is the **first** `.card` in the Overview column. The payoff is **not a `.card` at all**. |
| **Why** | *"What changed"* is **EPISODIC** — true for one moment after an analysis lands. **Confidence is PERMANENT.** An event may never outrank state in the layout. |
| **Guard** | `_assertConfidenceIsTheFirstPanel()` — **mechanism proof on DOM order** (`#pane-overview .card` → `[0]` must be `.card.hero`), plus a **vacuity check** (≥3 panels, or "first" is a statement about a list of one), plus: the payoff must not carry `.card`. |

## D179b — the payoff is a **DELTA ON THE CONFIDENCE CARD**, not a panel

| | |
|---|---|
| **Where** | Inside `.card.hero`, **immediately after `.conf-focus`** — under the hero it annotates, above the CAF rows. |
| **Chrome** | `.payoff` is a **strip**: `--maturity-soft` background, `--maturity-line` border, a 10px uppercase `.pay-k` label, and a `.pay-x` dismiss. **No card, no `<h3>`, no `.ch` header.** |
| **Dismissible** | `dismissPayoff()` hides the strip **and clears `_MOVE`**, then repaints the ramps — **the ghosts leave with the event**. |
| **Not persisted** | Nothing about the payoff touches `localStorage` / `sessionStorage` / cookies. **Reload ⇒ gone.** |
| **Guards** | `_assertPayoffLivesInsideTheConfidenceCard()` (descendant of `.card.hero` · sits *after* `.conf-focus` · the dismiss affordance is genuinely interactive · **dismiss removes the ghost**, proven by injecting a movement, asserting a ghost renders, then dismissing) · `_assertPayoffIsNotPersisted()` (source proof on every payoff path). |

## D179c — the movement is **DRAWN ON THE RAMP**, not written in a paragraph

```
Very Low  ·  ⟨Low⟩ ⟶ [ MODERATE ]  ·  High  ·  Very High
```

| Piece | Mechanism |
|---|---|
| `_rampHTML(band, {prev})` | **ONE builder, one new option.** The step at `_BANDORD.indexOf(prev)` gets `class="rstep ghost"` and carries `<span class="rarr">⟶</span>` (or `⟵` for a fall). `prev === band` (or absent) ⇒ **no ghost, no arrow.** |
| `_MOVE` | `{band:{from,to}|null, dims:{Feasibility:{from,to},…}}` — written **only** by `renderPayoff()`, from the **`before` snapshot**; read **only** by `renderRamp()` / `renderCafRows()`; cleared by `dismissPayoff()`. |
| `_ghostBandFor(dim)` | The single reader. `'__band'` ⇒ the hero ramp; a dimension name ⇒ that CAF row. **Null when nothing moved.** |
| **The demo case** | The Extended pass moves **Feasibility Very Low → Low** while the **overall band holds at Moderate**. So the **Feasibility row** ghosts step 0, lights step 1 and draws the arrow — and **the hero ramp draws nothing**. **NEVER FAKE A MOVEMENT THAT DID NOT HAPPEN.** |
| **Reliability** | The one transition that still travels in **words** (in the strip): reliability has **no ramp**, because canon states no scale for it and OSLO does not invent one (Anti-Assumption). |
| **Word budget** | `PAYOFF_WORD_BUDGET` **45 → 20**. The strip carries the **act** and **one short line**; the movement is a picture (uncounted) and the counts are in Progress. **A budget can no longer cost the user a number or a transition.** |
| **Guards** | `_assertGhostBandIsComputedFromPreviousSnapshot()` — walks **all 25 (prev, current) band pairs**: same band ⇒ no ghost; different ⇒ exactly one ghost, **at the previous band's index**, with an arrow. Then the **live surfaces** with `_MOVE` set and cleared. · `_assertRampIsNotAHealthBar()` extended: **at most ONE** unlit step may wear `ghost`, and only when `_MOVE` says so — a *trail* of filled-in steps would be a progress bar. · `_assertCafDimensionsRenderAsBands()` now compares **byte-for-byte against `_rampHTML(lvl,{compact:true, prev:_ghostBandFor(dim)})`**, so the ghost is inside the one-builder proof. |

## D179d — **NEUTRAL ≠ MONOCHROME.** A cool accent, and orange for actions only.

> **OSLO's brand colour is ORANGE. Orange reads as AMBER. Amber reads as "AT RISK."** A real brand-vs-doctrine collision on a maturity surface. D175/D176 removed severity colour — correctly — and then removed **all** colour, which left the hero grey and dead.

| Token | Dark | Light | Used for |
|---|---|---|---|
| `--maturity` | `#7FA0C9` | `#3F6193` | **the lit ramp step · the current band word · the limiter marker · the movement arrow · the payoff label** |
| `--maturity-soft` | `rgba(127,160,201,.14)` | `rgba(63,97,147,.10)` | the payoff strip's ground |
| `--maturity-line` | `rgba(127,160,201,.45)` | `rgba(63,97,147,.35)` | the payoff strip's edge |

- **Blue/violet is NOT in the RAG vocabulary** and cannot be misread as health. It is the one hue that can carry emphasis on a maturity surface.
- **`--primary` (brand orange) is reserved for ACTIONS and LINKS — never for STATE.** In the hero card that means exactly the `.conf-foot .lnk2` links. `HERO_INTERACTIVE_CLASSES` is the only door it has.
- **Severity colour (red/amber/green) stays on ISSUES alone (D003).** The Attention heat map is **untouched** — those cells *are* issues.

**The guard was AMENDED, not weakened:**

| | |
|---|---|
| `HERO_CARD_BANNED_TOKEN_RE` | still `--success\|--warning\|--danger\|--error\|--crit\|--conf-*` — **severity is banned everywhere in the card, always.** |
| `HERO_BRAND_TOKEN_RE` | `--primary*` — graded **by subject**: allowed on an interactive selector, **banned on state**, in the cascade *and* inline. |
| `_chromaticLiterals()` | **still grades CHROMA, not token names** — and now also **HUE**. The RAG arc is hue ∈ [340°..360°] ∪ [0°..170°]. The original defect `rgba(217,164,65,.08)` is **39° (amber) → still bites**. `rgb(217,122,58)` is **26° → still bites**. `rgba(127,160,201,.14)` is 214° (cool) → passes. Greyscale (chroma ≤ 12) passes. |
| `RAMP_ALLOWED_COLOUR_TOKENS` | neutrals **+ `--maturity*`**. Still no `--primary`, no `--conf-*`, no severity. |
| `_assertBrandOrangeIsActionsOnly()` | **NEW.** Proves the half a cascade cannot see: **every element in the card wearing an interactive class is genuinely operable** (`<a>`/`<button>`/onclick/role=button/tabindex), **no state class is enrolled in the action list**, and **the cool accent is actually present** (a card that went back to grey has re-run the over-correction, not obeyed D179d). |
| **AA** | every accented element clears AA in **both** themes: lit step / band word / limiter marker / arrow **6.13:1 (dark) · 6.28:1 (light)**; the payoff label on its own strip **4.87 / 5.45**; the hero links **7.20 / 5.93**; the delta chip **4.67 / 4.75**. |

## D179e — **COUNTS HAVE ONE HOME** (the sharpest finding)

**The payoff and Progress showed the same numbers twice** — one as a delta, one as an absolute.

**Progress now carries the counts, with the delta annotated:**

> Issues **8** ↑2 · Critical **2** ↑1 · Open questions **3** ↑1 · Confirmed artifacts **0 / 7**

| | |
|---|---|
| `_progressRows()` | Reads the **`PAYOFF_COUNTS` registry** — the *same* registry the payoff model reads. A row whose `get()` cannot produce a number is **absent from the snapshot, therefore absent from the chips.** |
| `_progressChipHTML()` | The one builder. `.pg-chip` = label + `<b>value [/ of]</b>` + `.pg-d` delta. |
| **The delta** | `value − _PREV_RUN.counts[key]`, where `_PREV_RUN` is the **`before` snapshot of the last analysis update**. **No previous run ⇒ no delta. No movement ⇒ no delta.** |
| **A rise is not green** | `↑` and `↓` wear **one** class (`.pg-d`), one weight, one colour. There is no `.pg-d.up` to style. **More issues is not bad news** (D177). |
| **What was deleted** | · `.conf-foot`'s *"6 issues open · 0 resolved"* (a second home for the issue count) · the Progress ledger's `pg-resolved`/`pg-open`/`pg-crit` numbers · **`Dependencies confirmed 0/3` + its fill** (the model holds **no dependency register** — it was counting clarification-bearing *issues* and calling them dependencies) · **`Plan artifacts read 7/7` + its 100% fill** (**hard-coded in the markup; nothing computed it**) · the count in the clarification pointer (*"OSLO has **2** things to confirm"*) · the count in *"See all **8** open issues"*. |
| **Guards** | `_assertNoCountIsRenderedTwice()` — a DOM scan of the **whole Overview**: for each registry count, find every **host** that renders its value *with its label beside it*; **more than one host is a violation, zero hosts is vacuity.** · `_assertProgressCountsAreComputed()` — the chips are byte-for-byte what `_progressRows()` builds; every chip traces to a registry row; an **uncomputable probe never reaches the chips** (and a **computable** one does, or the proof is vacuous); the **delta is derived**, and with `_PREV_RUN = null` there is **no delta at all**. · `_assertNoFabricatedProgressCount()` — *"N of 7 artifacts well-evidenced"* is gone from the Overview and cannot return. · `_assertEveryPayoffCountIsComputed()`'s **text proof was re-pointed at Progress** — it used to grade the payoff strip, which now prints **no numbers at all**, so it would have passed for free (**exactly the vacuity D166 §1 forbids**). |

**Scope, stated rather than assumed:** the guard grades `#pane-overview`. The left **nav rail** badges (`#vsAttnBadge`, `#vsIssuesBadge`) are **wayfinding affordances on a different surface**, not a second home for the count; the **0–100 index** is a secondary aggregate, not a count.

## The payoff, verbatim (Extended pass) — **19 words, budget 20**

> **What changed**
> **Extended Analysis landed.**
> *I looked deeper: found two more, and one more question. The read is firmer.*

…with **Feasibility ⟨Very Low⟩ ⟶ [Low]** drawn on its ramp, and **Issues 8 ↑2 · Critical 2 ↑1 · Open questions 3 ↑1** in Progress. **MORE ISSUES *AND* A HIGHER BAND — not a contradiction, the point** (D177).

## Negative controls — `_d179NegativeControls()` · **28 rows, every one `true`**

**The four owner findings, re-injected:** `theDefect_payoffIsAPanelAboveTheHero` · `theFakeMovement_ghostIsHardCoded` · `theSharpestDefect_theCountIsRenderedTwice` · `d_brandOrangeOnTheBandWord`.
**And the three that must NOT fire:** severity colour on **issues** (the heat map is correct as-is) · the **cool accent** on the maturity surface (that *is* D179d) · **more issues + a higher band** (that *is* D177).


---

# D180 — PROGRESS IS GROUNDING, NOT CLEARING (owner: approved, 2026-07-12)

**Progress toward WHAT?** **Not project completion — that is forbidden. Progress in UNDERSTANDING.**

> ## ⛔ **PROGRESS IS NOT A BURNDOWN.**
> If it looks like *issues → 0*, the product has rebuilt a **project-health tracker under another name** — and the
> doctrine leaks out through **the one panel nobody was watching**.

## The panel, verbatim (as rendered) — **25 words at boot, 41 after a run**

```
Progress                                                     (i)

GROUNDED   1 of 7 artifacts rest on your evidence   ↑1        ← the star
OPEN       Issues 7 ↓1 · Critical 1 ↓1 · Open questions 2 ↓1
CLOSED     Issues resolved 1 ↑1 · Questions answered 0

The arrows are the change since the last analysis update. Timeline →
```

## The three rows

| Row | What it says | Where the number comes from |
|---|---|---|
| **GROUNDED** *(the star)* | *"N of 7 artifacts rest on your evidence."* **The only number that says how much of this read is REAL versus INFERRED** — *derived vs attested* (D011), made countable. **It is the product's entire epistemic claim, as a count**, and **it rises as the user confirms artifacts, applies fixes and answers questions.** | `PLAN_SECTIONS.filter(p => p.basis === 'attested').length` **/** `PLAN_SECTIONS.length` |
| **OPEN** | What is outstanding. | `ISSUES` (active) · active `critical` · `_openClarIds()` |
| **CLOSED** | What the user's work **landed**. *(Closes O-D179-3.)* | `_istatus[id] === 'resolved'` · `_clarAnswered` |

**Every row is a row of `PAYOFF_COUNTS`** — the same registry the payoff model reads, whose `get()` reads live
state. **There is no number in the Progress markup at all**, and **a count that cannot be computed is absent from
the snapshot, therefore absent from the panel** (D173).

## What was KILLED, and why

| Killed | Why |
|---|---|
| **`Plan artifacts read 7 / 7`** *(closes O-D179-1)* | **OSLO always reads all seven. It is a CONSTANT, not progress** — hard-coded *because* it was meaningless. **A number that can never move is not information; it is decoration.** *"Read"* is not the interesting question; ***"grounded in evidence"* is.** |
| **`Confirmed artifacts 0 / 7`** *(the chip that stood in for it)* | Same count, **wrong frame**. It is now the **star sentence**, carrying the weight the epistemic claim deserves. |
| **`Dependencies confirmed 0 / 3` + fill** | The model holds **no dependency register**. **Omitted, not invented** (O-D179-2). |

## The property that must hold (**D180c**)

> **They ground more artifacts → reliability rises → confidence rises. AND ISSUES MAY RISE TOO, because grounding
> reveals things.** **PROGRESS GOES UP WHILE THE ISSUE COUNT GOES UP. THAT IS NOT A BUG — IT IS THE POINT.**
> **You cannot game GROUNDING. You can only game a BURNDOWN.**

## Guards — **mechanism, not copy** (D166)

| Guard | What it proves |
|---|---|
| `_assertGroundingRisesWhileIssuesRise()` | **THE STATE PROOF.** It grounds an artifact **while the issue count rises** (real state: the artifact basis flips to `attested`, a critical clar-bearing finding is surfaced, an update resolves one, the user answers one) and requires: **GROUNDED rises**, and **nothing treats the rising issue count as regression** — the `↑` on *Issues* and the `↑` on *Grounded* must carry **the identical class**, no direction class exists, **no severity colour reaches the panel's cascade**, and no regression vocabulary is printed. |
| `_assertNoBurndownGrammar()` | **Four doors, all shut.** The **REGISTRY** (a denominator on an OPEN/CLOSED count *is* a burndown) · the **COPY** (`%`, "remaining", "complete", "to go", "on/off track", "target") · the **DOM** (`<progress>`/`<meter>`/`role=progressbar`/inline % fill) · the **CASCADE** and the **RENDER PATH** (the door the CAF bars came through — D176b). |
| `_assertNoConstantDressedAsProgress()` | **PERTURBS STATE and requires every rendered row to MOVE.** A constant cannot survive it — a registry row returning `PLAN_SECTIONS.length` (i.e. "artifacts read 7/7", computed but immovable) goes **red**. |
| `_assertClosedIsNeverATarget()` | *Resolved* **exists, is computed, lives in the CLOSED row**, and carries **no denominator, no %, no "remaining"**. |
| `_assertNoCountIsRenderedTwice()` **(strengthened)** | Six counts now, and two share a noun (*Issues* / *Issues resolved*). Each Progress host **declares its count** (`data-count-key`) and is graded for that count alone; **a host that declares nothing is prose, and prose is still graded on the noun** — so the shipped footer defect (*"8 issues open"*) still bites. |

## Negative controls — `_d180NegativeControls()` · **19 rows, every one `true`**

**The defects, re-injected through the real mechanism:** `theDefect_aConstantReturnsAsProgress` (a registry row that
returns a constant) · `theBurndown_aCompletionPercentage` · `theBurndown_aBarTowardZero` ·
`theSubtleBurndown_aDenominatorOnResolved` · **`theLeak_theRisingIssueCountIsPaintedAsBad`** (the delta on *Issues*
goes red — **this is the doctrine leak, and the guard bites**) · `theLeak_groundingDoesNotRise` ·
`c_aDirectionClassReturns` · `c_resolvedLeavesTheClosedRow` · `c_refusesToGradeNothing` (vacuity).
**And the two that must NOT fire:** **more issues + a higher band** (D177) · **grounding rising while the issue
count rises** (D180c — *the property, not a bug*).

## AA contrast — Progress, **both themes**

`.pg-k` **5.34 / 5.23** · `.pg-say` **8.77 / 8.03** · `.pg-say b` **15.05 / 16.56** · `.pg-chip` **7.67 / 7.29** ·
`.pg-chip b` **13.15 / 15.05** · `.pg-d` **4.67 / 4.75** · `.prog-since` **5.34 / 5.23**. **Zero failures.**

---

# DL-109 — The provenance surfaces

## 1. Progress — the GROUNDED read is CLAIM-LEVEL, and the panel is a FOUNDATION BAR (DL-111)

```
   17 of 28  grounded in your evidence
             the rest of your read is OSLO’s inference
  [ Confirmed by you │ From OSLO 11 ]      ← solid bar: grounded segment (cool accent, label only) + inferred/From OSLO (hatched)
  Grounded — your evidence · Inferred — OSLO's read
  Your read leans on 12 inferences — the inferred claims above plus
  inferred assumptions, relationships and metrics                See them →
OPEN           Issues 6 · Critical 1 · Open questions 2
CLOSED         Issues resolved 0 · Questions answered 0
```

- **The hero's PRIMARY number IS the grounded-facts count — ATTESTED ONLY** (claims with `evidence_id` present),
  now shown as a **fraction** — *"17 of 28"* (grounded of **total claims** = grounded + inferred) — captioned
  *"grounded in your evidence / the rest of your read is OSLO's inference"* (**WI-R6, variant B**). **Erratum to
  DL-111:** grounded facts are **not** attested + derived — the big **`17`** is the grounded count **alone**,
  **never** `grounded + inferred`; the **`28`** denominator is the **total-claims composition** (what rests on you
  vs on OSLO) — **not a burndown target**, since inference is not driven to zero. Both are **computed from state,
  never typed**. *"Confirmed by you"* is **retained** on the grounded segment (**D196 / D194c**).
- **`grounded` / `inferred` / `loadbearing` are three `PAYOFF_COUNTS` rows.** Every one reads live state
  through `_ciEvidenceId()`. **There is nowhere to type a number in.**
- **The solid bar shows the read's claims in TWO provenance states, proportional to the real counts:** the
  **Confirmed by you** segment (grounded — **the grounded number lives in the hero, so the segment carries only its
  label**, sized to its share; cool-blue accent that echoes the Outcome Confidence ramp's lit band) and the
  **From OSLO** segment (inferred — carries its own count, rendered **hatched**). *From OSLO* **is** the inferred
  state; there is **no third "derived — supported" class**. A **two-swatch legend**: *Grounded — your evidence ·
  Inferred — OSLO's read*.
- **Each count declares its own home** (`data-count-key`) — two counts in one host would leave one of them
  homeless, and the one-home guard would grade it as never rendered (D179e).
- **Load-bearing is its OWN line BELOW the bar, and it is a SUPERSET — never `+`-joined.** *"Your read leans on 12
  inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →"*. The
  **12** counts inferred items of **every** type, so it legitimately **exceeds** the 11 inferred *claims* in the bar
  (§2a). The old panel `+`-joined the two as if disjoint — a lie; both numbers are right, they count different
  populations.
- **⭐ D181a — the number is 12, and it INCLUDES SCOPE.** *"The read would change were it false"* → **the read points
  at it**: (a) a critical issue cites it · (b) the limiting dimension's assessment rests on it · **(c) a
  strong-reading artifact's confidence rests on it.** **Clause (c) is why Scope's four inferences are in the number** —
  *Scope reads fine **because of** four things OSLO made up*, and **nobody is looking at it.**
  **An inference nothing points at is not counted** — that was the over-count (11) the loose reading shipped.
- **The old star is gone:** *"2 of 7 artifacts rest on your evidence"* was true but coarse — it could not say
  **what** rests on you and what rests on OSLO. **The denominator went with it:** a total on an inference count is
  a total to reach, and **inference is not a thing to drive to zero** (DL-109 §3a).

## 2. The Inference map — a new peer surface, in the nav beside the Attention map

> **The Attention map shows where the plan is WEAK. The Inference map shows where OSLO is GUESSING.**

| Block | What it draws | Rule |
|---|---|---|
| **The finding** (`.inf-flag`) | ***"Scope reads strong, and most of it is mine — 4 of its 7 items are inference. Worth verifying first."*** + **Open Scope →** | **CONF-06 at the ARTIFACT level.** Computed by `_ciFalseConfidentArtifacts()`. **Neutral chrome only** — a thing to CHECK, not a severity (D003). |
| **The map** (`.inf-rows`) | 7 artifacts × **countable pips**, grounded first, then the counts in words | ⛔ **NOT a percentage fill** (D176). **One pip = one extracted item.** `_assertInferenceMapIsNeutral()` proves the pips **equal the model**, per row. **Counting is not filling.** |
| **Assumptions** (`.inf-list`) | the **unbacked** assumption register — **load-bearing first**, then by how much rests on it, then **oldest first** | each row carries its **age** and *"N issues depend on it"* — both computed (§4a) |
| **Structure** (`.inf-facts`) | *4 dependencies OSLO assumed · 5 named parties with nobody accountable · 3 numbers that trace to nothing* | §2d. A count the model cannot compute **is not shown** (D173). |
| **This week** (`.inf-facts`) | *you grounded **0** · I inferred **37*** | §4b. **A direction, never a target.** Both numbers drawn identically. ⛔ **D181b — the window is THE CLOCK's**: advance a week with nothing done and it honestly reads **0 · 0** (*understanding is stalling*). Ground an artifact, or run a deeper read, and it moves again. |

**Colour:** the cool accent (`--cool`) only — **blue is not in the RAG vocabulary**. Brand orange stays on links
(`.pg-go`, the flag's action). **No severity token may appear on this pane** (`_assertInferenceMapIsNeutral()`
grades the cascade, the DOM and the render path).

## 3. The Readout

- **§B "Unvalidated assumptions" is REPOINTED** — it read **open clarifications whose hint contained the word
  "inferred"**, a **proxy**. It now reads **the assumption register** (`item_type='assumption'`, unbacked,
  load-bearing first). `_assertKeyAssumptionsReadTheRegister()` proves it **both ways**: a new assumption must
  **appear**, and a new clarification must **not**.
- **§5 "What I'd need to be sure" is new** (DL-109 §2f) — the unbacked **load-bearing** items, **as a list of asks**:
  *"Confirm: **The venue can carry 500 concurrent devices.** · If it is wrong: Venue Wi-Fi capacity is unconfirmed."*
  **Audience-independent** (DL-108): what OSLO needs confirmed does not change with who is being asked.
  "How to read this" moves to **§6**.

## AA contrast — the Inference map, **both themes** (dark / light)

`.inf-nm`, `.inf-ct b` **8.77 / 8.03** · `.inf-ct`, `.fl` **5.34 / 5.23** · `.inf-fact b` **15.05 / 16.56** ·
`.inf-verify`, `.inf-lbt`, `.inf-flag .ic` (`--cool`) **6.13 / 6.28** · `.inf-flag .bd` **9.43 / 7.10** ·
`.pg-go` (`--primary-light`) **7.20 / 5.93**. **Zero failures.**

**⛔ One AA fix made during the build:** the **inferred pip** was drawn with a `--border-2` dashed edge — **1.58 : 1**
against the card, **below the 3:1 non-text minimum** (WCAG 1.4.11) for a mark that *carries information*. It now uses
`--subtle` (**5.34 / 5.23**). The two pip states differ by **fill** and **border style** as well as colour, so the
distinction survives without colour at all (WCAG 1.4.1).

---

# D182 — THE PROBE FENCE (`_PROBE`) · D183 — COPY AND POSITIONING (2026-07-13)

## D182 — one fence over every user-facing effect

`_CHAT_PROBE` was the right idea scoped to one surface. It is now **one fence** (`_probeFence`), applied to
**every `_assert*` guard and every `_d*NegativeControls()` suite by construction** (`_fenceEveryProbe()`, run at
boot before any probe).

| Effect | Under the fence |
|---|---|
| **Prompts** (`fireUP`) | **Computed and recorded** (`_PROBE.prompts`) so the guard can still grade the mechanism — **blinded** by the one CSS rule `html[data-probe] { visibility:hidden; pointer-events:none }` over every prompt surface, and **never persisted**: `_upFired()` and the month-cooldown write are no-ops. **A probe's prompt is not the product's prompt.** |
| **Deferred prompts** (`_deferUP`) | **Never enqueued.** The queue drains on a 400 ms timer — a probe's deferred prompt would land on the user **after** the guard finished. This was the owner's symptom verbatim. |
| **Async fires** (`_markFirstValue` → UP-8, `_maybeUP7` → UP-7) | **Do not arm.** A `setTimeout` escapes a synchronous fence entirely. |
| **Chat** | `_retireClarBoxes()` is a no-op; the thread is restored **byte-for-byte** (`innerHTML`), never by child count. |
| **History · Trend · memos · localStorage · prompt surfaces** | Snapshotted on entry, **restored byte-for-byte** on exit. `_lsFullSnap()` / `_lsFullRestore()` — **absent means ABSENT** (`LS.set(k, LS.get(k, null))` writes the string `"null"`; it does not undo a write). |

**The one exemption, named:** `_d182NegativeControls()` stands outside the fence, because it must prove that an
**un-fenced probe DOES reach the user** (the P1, injected back) and that **a real user attempt still raises a real
prompt** (D138). It takes its own snapshot and restores it. Clause (d) of `_assertNoProbeCanRaiseAPrompt()` fails
if a second exemption appears, or if any `_assert*` lowers the fence by hand.

## D183 — the surfaces

| Element | Before | Now |
|---|---|---|
| **Confidence pill** | `● Confidence  58  Moderate  Moderate reliability ▾` | `● Outcome Confidence  Moderate  largely grounded ▾` |
| **Hero** | ramp · `moderate reliability` · limiter · direction **+ cause** · **`58 /100`** | ramp · **`the read is largely grounded`** · limiter · **direction only** · *(no index — element and CSS rules **deleted**)* |
| **Confidence popover** | `Moderate  58/100` · *"Qualified by moderate reliability."* | `Moderate` · *"It is **thinly grounded**."* |
| **Trend line** | `↗ Strengthened — deeper analysis firmed the read (Feasibility rose Very Low → Low)` | `↗ Strengthened` |
| **Progress** | `I inferred: 11` · `12 things I inferred are holding up your plan` | `OSLO inferred: 11` · `12 inferences are holding up your plan` |
| **Payoff** | *"I looked deeper: found two more…"* · `Reliability: Moderate → High.` | *"**OSLO** looked deeper: found two more, and one more question. The read is firmer."* · `Grounding: thinly → largely grounded.` |
| **Sidebar / Attention rows / Issues filter / workspace / Plans / export** | *Plan artifacts · By artifact · Artifact detail* | **Documents · By document · Document detail** |
| **Overview order** | static: Confidence → Start here → Progress | **computed**: first run → *Start here* first; after first value → **Progress first** |

**Colour:** no new token was introduced. The grounding qualifier reuses `--muted` (pill, hero) and `--subtle`
(popover). **AA both themes:** `--text` 16.92 / 16.56 · `--muted` 9.86 / 8.03 · `--subtle` 6.01 / 5.23.
The one new CSS rule (the probe blind) carries **no colour token and no z-index**, so it is invisible to the
ramp / severity / z-order guards by construction.

---

# D184 — THE APPLY AFFORDANCE SHOWS THE FIX IT APPLIES (P1, owner, 2026-07-13)

> ## ⛔ **A FIX THE USER CANNOT READ IS A FIX THEY CANNOT CONSENT TO.**
> **OSLO is advisory-only (D001). Advice the user cannot see is not advice — it is an instruction.** The moment
> the product asks *"apply?"* about a change it has not shown, **it has stopped advising and started acting.**

**The defect:** the Issue panel rendered a bare **"Apply this fix"** button, and the fix was **not on the screen**.
The three recommendations sat **collapsed, in a disclosure row, BELOW it.** The button did not even identify which.

## The block, rebuilt (the change, THEN the button — in that order)

```
◆ OSLO recommends                                   [From OSLO]
Confirm the venue’s 500-person Wi-Fi capacity before locking
the in-person-only format.
[ Apply this fix ]  [ Discuss ]  [ Other options (2) ] ⓘ
   └── (expands IN PLACE, here, under the recommendation — D190c)
```

| Rule | Mechanism |
|---|---|
| The recommendation is **resident**, in the button's own block, **above** the button | `.ip-rec` moved **out of `.ip-rows` entirely** — it is no longer a disclosure at any time |
| ~~The button **names its subject**~~ — **CORRECTED BY D190a.** The affordance is **short and constant** (`APPLY_LABEL`); **the fix above it is the subject.** | The guard's **label clause** was amended; **the consent clause is untouched** — the recommendation must still be visible, out of any drawer, and **above** the button |
| **More than one recommendation** ⇒ the button applies **the one on screen**; the others are **one tap away** | `_otherRecs(id)` → **`#ipAlts`, expanded in place UNDER the recommendation** (D190c) — never a row under Evidence |
| **Rank** | `_recRankScore()` — appliable · **moves the LIMITING dimension** · the user's own selection · OSLO's own recommendation. **Computed, never an index.** Across issues: `_leadRecId()` |
| **No renderable recommendation ⇒ NO BUTTON** | `_primaryRec()` returns `null` → the block is not built (D173, applied to actions: **an action whose subject is absent is REMOVED, not degraded**) |
| The **assisted-apply cap** (DL-103 §7d) | **stronger than before:** the cap cannot hide a recommendation that was never inside a collapsible row. The cap opens **`#ipAlts`** — the *Other options* — because that is where **the free manual door** lives |

**Guards:** `_assertApplyAffordanceShowsItsRecommendation()` (issue panel **and** the chat's render path) ·
`_assertRecommendationRankIsComputed()` (state proof: move the limiter → the lead moves) ·
`_assertRecommendationNeverHidden()` **strengthened** (the recommendation may not live in a `.ip-row` at all).
**NC:** `_d184NegativeControls()` — **10 controls bite, 3 must-not-fire green** (D190 folded in; see below).

---

# D190 — THE RECOMMENDATION BLOCK, CORRECTED (owner, 2026-07-13)

## D190a — the button says **"Apply this fix."** Nothing more.

> **This CORRECTS D184 clause 2, which the owner wrote when the recommendation was INVISIBLE.**
> With the fix now **resident directly above the button** (D184 clause 1), a label that repeats it produced
> *"Apply: Confirm the venue's 500-person Wi-Fi capacity…"* — **too long to scan, truncated before it could be
> read. The worst of both.**

**The affordance is SHORT and CONSTANT; the fix above it is the SUBJECT.** One string — `APPLY_LABEL` — read by
**both** the panel and the chat (`_applyLabel()`), so the affordance cannot drift apart across surfaces.

| Rule | Mechanism |
|---|---|
| The label is the constant **"Apply this fix"** (chat: `Apply this fix →`) | `_applyLabel()` — a single reader |
| **D184's consent guard is UNCHANGED and still bites** | the recommendation must be **visible in the same block, out of every drawer, ABOVE the button** (document order). **Blank the recommendation → the guard goes RED** (NC `aButtonWithNoSubjectSurvives_bites`) |
| The guard's **label clause** is amended — and it bites **the other way** | a label that **eats the fix** is now the violation (NC `theLabelEatsTheFix_bites`), as is a label that **varies with its subject** (NC `theLabelVariesWithTheSubject_bites` — proven by opening **every** issue: one label, six different fixes) |

## D190b — **"Other paths" → "Other options."**

Every occurrence — the panel button, the option rows, *Selected option*, the **History** entry (*"Resolution option
selected"* · *Option "…"*), the chat (*"compare the resolution options"*, *"You've already selected an option
here"*), the **review kinds** (*"You'd take a different option"*), and the **tour** (*"You commit to an option"*).
**Internals keep their names** (`paths[]`, `_selpath`, `selectPath`) — the D183e split: *the canonical entity keeps
its name; the product speaks plain English.*

## D190c — the options live **UNDER the recommendation**, not under Evidence

> ***The alternatives to a recommendation are part of the DECISION. Evidence is the RECORD. They are not the same
> row.*** *"Other options (2)"* existed **TWICE** — a button in the recommendation block **and** a disclosure row
> below Evidence. **The same door, offered in two places, in two registers.**

| Rule | Mechanism |
|---|---|
| **ONE HOME** (D179e, applied to actions) | the options expand **in place**, in `#ipAlts` **inside `#ipRecBlock`**, directly beneath the recommendation. **The disclosure row under Evidence is DELETED** (the panel's rows are now *Evidence · Clarification · Comments · Reviews*) |
| Everything the row carried moved **with** it | the **ⓘ** (*"Applying is OSLO doing the edit. Writing your own fix is always free."*) · **Select** · **Discuss** · the **Selected option** chip · and the **free manual door** — *"✎ Write my own fix in \<document\>"* (**D183e: documents**) |
| **The cap still never hides the recommendation** | the cap opens `#ipAlts` (`_ipRows()` forces it open for as long as `_capHit('fixes')`), and **the user cannot collapse it while the cap is hit.** The recommendation is **outside** it, resident, by construction. **Metering understanding is PROHIBITED (D126/D128)** |
| **`.ip-alts` is deliberately NOT an `.ip-row`** | the D184 guard forbids anything in this block from living in a drawer, and this container must never become one |

**Guard:** `_assertOptionsHaveOneHome()` — **mechanism, not a string scan**, three clauses on the live DOM, over
**every** issue that carries alternatives: **(1)** each option renders in exactly **one** leaf site in the panel ·
**(2)** exactly **one** affordance controls the set (`aria-controls`) **and no undeclared handler can open it** ·
**(3)** the container sits **inside the recommendation block, after the recommendation text**, and **not** inside
`.ip-rows`/`.ip-row`. **Non-vacuity:** no alternatives anywhere ⇒ the guard **FAILS**, it does not pass for free.

**NC:** `aSecondOpenerForTheSameSet_bites` (the owner's control, verbatim) · `theOptionsAreRenderedTwice_bites` ·
`theOptionsGoBackUnderEvidence_bites` · must-not-fire
`mustNotFire_atTheCapTheFixIsVisibleAndTheFreeDoorIsOpen`.

## AA — a pre-existing defect this move surfaced

The options moved from the panel background (`--surface`) onto the recommendation card (`--surface-2`). Two labels
were **already below AA in dark theme** — the **"Confirmed by you"** pill (3.74:1) and the **✓ Selected option**
tick (3.72:1) — because `--success` is a **fill/border** green being used as **text**. The move made a failing
contrast worse, **so it is fixed, not shipped**: a new **`--success-fg`** token (dark **#6FB894**, light
**#3E7357** — unchanged) carries success **as text**. **`--success` itself is untouched**, so D187's `--earned`
distance guard grades the same values it always did. **AA now: 5.61 / 5.58 dark · 4.63 / 4.66 light.**

---

# D185 — THE CONFIDENCE POPOVER IS A READOUT, NOT AN ESSAY (owner, 2026-07-13)

> ## **The doctrine is a CONSTRAINT ON WHAT THE PRODUCT MAY CLAIM. It is not a SCRIPT the product must recite.**
> **The user opened this to read a state. They got a lecture.** *If the design is honest, it does not need to say so.*

**Before:** ~90 words of prose defending the panel, ~10 words of information. **Three paragraphs, each justifying
the row above it** — deleted, **not shortened**. Every one of them now lives **behind the ⓘ**.

## The panel, in order — and nothing else

| # | Slot | Copy | Source |
|---|---|---|---|
| a | **THE STATE** | **Outcome Confidence · Moderate** · *thinly grounded* | `r.band` + `_groundingWord()` (D183b/c) |
| b | **THE THREE DIMENSIONS** | Clarity · Alignment · Feasibility, each on the one five-step ramp, limiter marked by **weight** | `_cafOf()` / `_limitingOf()` |
| c | **THE LIMITER — with a VERB** | **"Feasibility — the lowest. Confirm it to lift the read."** | computed; ≤ 8 words + the dimension. ⛔ **D196a — the verb is `CONFIRM`** (*"Confirmed by you"* is a ratified epistemic class; *"Ground it"* was jargon) |
| d | **ONE WAY OUT** | **"Confirm Feasibility →"** (D196a) — opens the issue the limiter rests on | `_leadRecId()`; falls back to the full breakdown when there is nothing to point at |
| e | **RELIABILITY BASIS** | **"Thinnest: Evidence — Low."** — *what is THIN*, not that everything is average. All three **on demand**. | `_relRanked()` / `_relThin()` |

**A tie has no weakest, and OSLO does not invent one** (D173): three level dimensions read
**"Even across the basis — Moderate."**

**Budget, as a mechanism:** resident prose **≤ 25 words** (measured: **12**) **AND zero resident explanatory
sentences** (a sentence > 8 words is an explanation, not a readout). `data-cpp-state` marks a state token or an
action label; **tagging a paragraph `data-cpp-state` does not hide it** — the sentence clause grades all resident
text, tagged or not.

**Guards:** `_assertConfPopIsAReadout()` (budget · sentences · narration frames · **the ⓘ still carries the
doctrine** · the limiter has a verb) · `_assertReliabilityBasisSurfacesTheWeakest()` (state proof).
**NC:** `_d185NegativeControls()` — 6 controls bite, 2 must-not-fire green.

**Colour:** **no new token.** `.cpp-grd` / `.cpp-thin` reuse `--subtle`; `.cpp-morebtn` reuses `--primary-light`
(an action). **AA both themes on `--surface-2`:** `--subtle` 4.67 / 4.75 · `--primary-light` 6.30 / 5.39 ·
`--text` 13.15 / 15.05.

---

## D186–D189 — Overview / Progress / Inference map (owner, 2026-07-13)

### The valence table (D187) — the only thing that may colour a count

```js
const COUNT_VALENCE = {
  resolved:   {userDriven:true,  why:'Only the user resolves an issue…'},
  answered:   {userDriven:true,  why:'Only the user answers a clarification…'},
  vel_you:    {userDriven:true,  why:'Gated on _ATTEST_AT[art] — written by the user confirming a document…'},
  grounded:   {userDriven:false, why:'A deeper read can extract a NEW claim from an already-confirmed document…'},
  inferred:   {userDriven:false, why:'A deeper read infers more (D177) — not a regression…'},
  loadbearing:{userDriven:false, why:'It rises when a deeper read finds more that the read points at…'},
  issues:     {userDriven:false, why:'THE ONE THE OWNER ASKED ABOUT — "Issues 8 ↑2" is OSLO looking HARDER…'},
  critical:   {userDriven:false, why:'A critical issue FOUND is a critical issue AVOIDED…'},
  questions:  {userDriven:false, why:'A Deep Pass ASKS (D178)…'},
  vel_oslo:   {userDriven:false, why:'Inference is what OSLO is FOR (PS-01 / DL-109 §3b)…'}
};
_deltaIsEarned(key, delta) === _isUserDriven(key) && delta > 0;   // green iff USER-DRIVEN and RISING
```

**There is no `red` field**, no `.pg-d.bad` rule, and no severity token anywhere on a progress/trend surface.
`.earned` is written by `_progressDeltaHTML()` and `_statCellHTML()` — **computed, never typed into markup.**

**Token.** `--earned: #4FC3A1` (dark) / `#0A6E52` (light). **It is NOT `--success`** (#4D8B6B / #3E7357 — the
**severity** green, D003: issues only). **Chroma distance 77.8 / 52.5.**
**AA both themes:** dark **7.61:1** on `--surface` · **6.65:1** on `--surface-2` · light **6.24:1** / **5.67:1**.
`_assertTrendColourIsEarnedOnly()` resolves both tokens from the **authored cascade, last-declaration-wins**, and
grades the **VALUE** — *a guard that graded the token NAME would sail straight past a renamed severity green.*

### Copy (D186 / D188 / D189)

| Surface | Was | Is |
|---|---|---|
| Progress · load-bearing | `Holding it up` · *"12 inferences are holding up your plan"* | **the *leans* line below the bar** · *"Your read leans on 12 inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →"* (DL-111 + erratum; a superset population, never `+`-joined to the bar) |
| Hero limiter (`#ov-limit`) | *"**Feasibility** is holding it back."* | *"**Feasibility** — the lowest. **Confirm** it to lift the read."* (D196a) |
| CAF tip (`cg-feas-tipb`) | *"…the dimension holding your confidence back."* | *"…the lowest dimension — **confirm** it to lift the read."* (D196a) |
| How-calculated list | *"…the weakest of the three holds it back."* | *"…the weakest of the three sets the level."* |
| Inference map · Assumptions caption | *"The ones holding the plan up come first"* | *"The ones your read rests on come first"* |
| Inference map · assumption tag | `Holding it up` | **`Your read rests on this`** |
| Inference map · Structure strip | *"6 dependencies OSLO assumed, and nobody confirmed"* ×3 | **`4 · Unconfirmed dependencies ⓘ`** · **`5 · Unowned parties ⓘ`** · **`3 · Untraceable numbers ⓘ`** |
| Inference map · "This week" caption | *"A direction, not a target"* | **deleted** |
| Readout §5 / §B | *"holding the plan up"* | *"the read rests on it"* |
| Chat capability list | *"…what's holding it back"* | *"…what is setting the level"* |
| Limits modal (D183e, pre-existing) | *"**Plan artifacts** · History"* | *"**Documents** · History"* |

### Guards added (4) · guard defects fixed (2)

- `_assertNoHoldingItAnywhere()` — DOM · attributes · **`TOUR`** · **`PN_SLOTS`** · render paths (`_edCodeOf`
  strips comments: **a scanner must not be its own subject**) · **non-vacuity** (the replacement is on screen) ·
  **"Blocker" never arrived**.
- `_assertTrendColourIsEarnedOnly()` — the declared table · **no red in the cascade** · **the chroma, not the name**
  · **two state proofs** (the user resolves ⇒ green appears; OSLO runs a deeper read ⇒ **nothing** goes green) ·
  every `.earned` on screen declares a user-driven key · **the direction is still the data's** (D180).
- `_assertStatLabelsAreLabels()` — **≤ 3 words**, the ⓘ carries the consequence, the sentence is not still resident.
- `_assertNoPreemptiveCaptions()` — grades the **shape** of a caption, not a string · **must-not-sweep** clause
  keeps the **disclosures** (*"not a guarantee of success"*).
- **GUARD DEFECT #24 — `_OSLO_VOICE_SURFACES` carried `#issuePanel` / `#ipBody`.** The ids are `issuepanel` and
  *nothing*. **Both matched zero elements: the Issue panel was never graded for first person.** Fixed; the guard now
  **fails if any surface resolves to nothing**, **opens every issue under the probe fence**, and exempts the
  **user's own controls by declaration** (`data-voice="user"`).
- **GUARD DEFECT #25 — `_assertPlanDocumentsAreCalledDocuments()` only graded what had been PAINTED.** `#limitsBody`
  is empty until `renderLimits()` runs, so a live D183e violation sat in the *What's metered* modal for the whole
  build. **An unpainted surface is not a clean surface.** The guard now paints deferred surfaces before grading.

**Verification:** `node --check` PASS · inert jsdom body children **31** (unchanged) · **113 boot guards × 6
configurations (Free/Basic × notes OFF/ON × first-value NO/YES), 0 console errors** · **12 NC suites, 245 controls,
every one bites**, every must-not-fire green · **D182: zero prompts raised by the guard suite.**

---

## D191 — the withdraw affordance (owner P1, 2026-07-13)

**Two homes, and only two** (D179e/D190c applied to actions): **the issue panel** and **the History row**.

| Element | Class | Where | Copy |
|---|---|---|---|
| Panel affordance | `.ip-wd > button.btn-ghost` (`#ipWdBtn`) | inside `.ip-addressed` — **with the decision it withdraws** | **"Withdraw this fix"** / **"Withdraw this answer"** / **"Clear selection"**. ⛔ **Never "Undo."** |
| Consent step | `.ip-wd.confirm > .wd-line` + `.wd-acts` | **replaces the button in place**, subject on screen (D184) | *"This removes the change from \<Document\> and withdraws your confirmation. OSLO will re-read the plan."* · **[Withdraw this fix] [Keep it]** |
| History affordance | `.hwd` | on the **origin row** of a decision that still stands (`_decision[id].evId`) | same word; **opens the issue and raises the consent step** — it never acts from the timeline |
| The standing word | `.ip-wd-still` | inside `.ip-resolved`, **above the affordance — which is now THERE (D192a)** | *"Your confirmation still stands on \<document\> — and it is still yours to withdraw. OSLO will re-read the plan, and re-open this issue if the gap is back."* |
| The refund | `.meter .mv .mref` | Usage & Limits, the assisted-apply row | *"1 refunded (withdrawn)"* — **neutral: a refund is not a reward** |

**Colour:** the affordance is an **action**, so it wears `--primary-light` (**D179d** — orange for actions and
links; the cool accent for state; RAG for issues). **No severity colour anywhere on these elements.**

**AA, both themes (dark / light):** `.ip-wd .wd-line` **7.92 / 7.39** · `.ip-wd-still` **7.88 / 7.27** ·
`.hwd` **7.20 / 5.93** · `.meter .mref` **4.67 / 4.75**.
⚠️ **A defect caught before it shipped:** `.hwd:hover` recoloured to `--primary` = **3.09:1 in the light theme**.
**A hover state below AA is still a state the user reads.** The hover **no longer changes colour** — the underline
weight carries the feedback, and it costs no contrast.


---

## D192b — the lifecycle track (owner, 2026-07-13)

`.ip-life` no longer draws a **one-way ratchet**.

| Element | Before | Now |
|---|---|---|
| Separator | `.a` = **`→`** | `.a` = **`⇄`**, `aria-hidden` — *the states move both ways* |
| Fill | every state **before** the current one carried `.done` | ⛔ **no trailing fill.** Only the state the issue is *actually in* carries `.on` (and `.done` when that state is Resolved). *A filled-in past is a claim the past is settled.* |
| Chips | — | each carries `data-life="open|addressed|resolved"`; the current one carries `aria-current="step"`; the group carries an `aria-label` naming the current state **and** the reversibility |
| The ⓘ | *"Issues close as OSLO's understanding updates — you don't close them by hand."* | *"These states move both ways. An analysis update moves an issue forward; withdrawing a decision can bring it back. Either way it is the analysis that moves it — never a manual step."* |

**Guard:** `_assertLifecycleIsNotDrawnAsARatchet()` — glyphs · fill · **and the mechanism: the issue is driven
Resolved → withdrawn → re-opened by the analysis update, and the rendered track must FOLLOW.**

---
## D194 — the Progress rows (owner, 2026-07-13)

### The panel, as it renders (DL-111 — the foundation bar)

```
PROGRESS ⓘ
   17 of 28  grounded in your evidence
             the rest of your read is OSLO’s inference
  [ Confirmed by you │ From OSLO 11 ]      grounded segment (cool accent, label only) + inferred/From OSLO (hatched)
  Grounded — your evidence · Inferred — OSLO's read
  Your read leans on 12 inferences — the inferred claims above plus
  inferred assumptions, relationships and metrics                See them →
OPEN     Issues 6 · Critical 1 · Open questions 2
CLOSED   Issues resolved 0 · Questions answered 0
                                     The arrows are the change since the last analysis
                                     update.  Timeline →
```

The **hero**'s primary number is the computed **GROUNDED FACTS** count — **attested claims only** (`evidence_id`
present); it is `17`, **never** `grounded + inferred` (erratum to DL-111). It is presented as a **fraction — `17 of
28`** (grounded of total claims), captioned *"grounded in your evidence / the rest of your read is OSLO's inference"*
(**WI-R6, variant B**); the `28` is the total-claims composition denominator — **context, not a target** (inference
is not driven to zero). The **solid bar** shows the read's claims in **two
provenance states**: the *Confirmed by you* segment (grounded; **label only — the number is in the hero**; cool-blue
accent that echoes the Outcome Confidence ramp's lit band) and the *From OSLO* segment (inferred; carries its count,
rendered **hatched**). *From OSLO* **is** the inferred state — there is no third "derived — supported" class; the
**two-swatch legend** reads *Grounded — your evidence · Inferred — OSLO's read*. **Load-bearing is a separate line
below the bar, a SUPERSET** — *"Your read leans on 12 inferences — the inferred claims above plus inferred
assumptions, relationships and metrics · See them →"*; the **12** counts inferred items of every type and so exceeds
the 11 inferred *claims*, and it is **never `+`-joined** into the bar. **OPEN** and **CLOSED** are big-numeral stat
rows; **red appears only on Critical**; deltas are neutral ↑/↓ over the *"change since the last analysis update"*
footer and the `Timeline →` link.

### The epistemic-class registry — one registry, one reader, one painter

The three ratified classes (**D011/D069**) live in **`EPI_CLASSES`** and nowhere else:

| key | class name | claim count | valence (D187) |
|---|---|---|---|
| `oslo` | **From OSLO** | `inferred` — `_ciInferredClaims()` | neutral (a deeper read infers more — D177) |
| `you` | **Confirmed by you** | `grounded` — `_ciGroundedClaims()` | neutral (**O-D187-1**: OSLO can extract a new claim from a document the user already confirmed) |
| `third` | **Attested by \<name\>** | `attested3` — `_ciThirdPartyClaims()` | neutral (**a reviewer** moves it, not the user) |

- **`epiClassName(key, who)`** — the **one reader**. Every class name in the product comes through it.
- **`_epiLabelHTML(key, cls, who)`** — the **one painter**. It emits `data-epi-class` on every label it builds.
- **`_paintEpiClassLabels(root)`** — repaints every `[data-epi-class]` element from the registry, **including the
  static ones** (the Outcome-Confidence chip, the Inference-map key). Those carry **no class name in the markup at
  all**, so there is nothing to drift. Called once at boot, before any surface is read.
- **The third class REQUIRES its attester.** `name(who)` returns `null` without one — *"Attested by them"* would be
  a **new, invented string**, not the ratified one. **A class OSLO cannot NAME is not drawn** (D173). The
  multi-attester aggregate name is **owner-open** (**O-D194-2**).

**Scope, stated:** the registry governs every element whose **job is to name a class** — `.elabel` · `.epi-tag` ·
`.sro-epi` · `.pg-cl` · `.cell-epi` · the map key. **Prose that *mentions* a class inside a sentence is a sentence,
not a label** — out of scope, and **escalated (O-D194-3)**, not silently swept. *(Several such sentences live in the
D191–D193 withdraw/attestation machinery, which was explicitly not to be touched.)*

### Markup

```html
<!-- DL-111 + erratum + WI-R6 (`_progressHTML`). The class names come from the ONE painter (`_epiLabelHTML`).
     GROUNDED FACTS = ATTESTED ONLY: the grounded number is the HERO (big number), shown as "N of TOTAL"
     where TOTAL = grounded + inferred; the grounded segment carries only its label. -->
<div class="pgx">
  <div class="pgx-hero">
    <div class="pgx-big-host" data-count-key="grounded"><span class="pgx-big n num">17</span><span class="pgx-of num"> of 28</span></div>
    <div class="pgx-cap"><div class="l1">grounded in your evidence</div><div class="l2">the rest of your read is OSLO’s inference</div></div></div>
  <div class="pgx-barwrap">
    <div class="pgx-solid" style="flex:28">
      <!-- grounded — cool-accent segment, LABEL ONLY (its count is the hero numerator), sized to the grounded share -->
      <div class="pgx-seg att" style="flex:17">
        <span class="pgx-sl" data-epi-class="you">Confirmed by you</span></div>
      <!-- inferred — From OSLO, hatched, carries its own count. No third "derived — supported" class. -->
      <div class="pgx-seg der" data-count-key="inferred" style="flex:11">
        <span class="sn num">11</span><span class="pgx-sl" data-epi-class="oslo">From OSLO</span></div>
    </div>
  </div>
  <!-- TWO provenance states only: grounded / inferred -->
  <div class="pgx-legend">
    <span class="pgx-lg"><span class="pgx-sw att"></span>Grounded — your evidence</span>
    <span class="pgx-lg"><span class="pgx-sw inf"></span>Inferred — OSLO's read</span>
  </div>
  <!-- load-bearing: its OWN line below the bar, a SUPERSET (inferred items of every type), never +-joined -->
  <div class="pgx-leans" data-count-key="loadbearing">Your read leans on <b class="n num">12</b> inferences
    <span class="pgx-leans-x">— the inferred claims above plus inferred assumptions, relationships and metrics</span>
    <a class="pgx-go" onclick="showView('inference')">See them →</a></div>
</div>
```

### Tokens

Under the DL-111 erratum the bar shows **two provenance states** (`.pgx-sl` labels from the ONE painter). The
*From OSLO* segment **is the inferred state**, rendered **hatched**; the *Confirmed by you* (grounded) segment
carries a **cool-blue accent** (`--cool`) — **deliberately echoing the Outcome Confidence ramp's lit band**, so the
two Overview panels read as one page. **NEUTRAL in both directions** (D003/D179d): the cool accent is a **harmony
cue, not a RAG/severity token** — *From OSLO* is not a warning and *Confirmed by you* is not a prize. **Severity red
is scoped to Critical alone**, and brand orange stays on actions/links (e.g. `See them →`, `Timeline →`), never on
state. **AA holds in both themes.**

### Guards

| Guard | What it proves |
|---|---|
| `_assertNoProgressRowSaysItTwice()` | **D194a.** Every row: a **phrase label (≥2 words)** may not reappear as a phrase in its own value; **no cell may BE its heading.** Measures the **happy path** too — the count, the noun, the delta (by **moving the baseline**) and the map link all survive. |
| `_assertEpistemicClassNamesAreSingleSourced()` | **D194b.** **Renames the classes in the registry, repaints, and requires every label to follow.** A label that does not is a **literal**. Plus a **source scan** of the render paths (a path not on screen now will be next). |
| `_assertThirdEpistemicClassIsRepresentable()` | **D194c.** Gives a live `ContextItem` an `EV-AT3-` evidence id and re-renders: **a third cell must appear**, correctly named, with its own home, displacing neither other class. |
| `_assertProgressRowsStayDistinct()` | **D194d.** **Structural, not textual:** two `.pg-row` hosts; no denominator / percentage / "of" / ratio on either; the subset ⊆ the **inferred items**. |
| `_pgReadableText(el)` | **The reader that replaced `textContent`** — leaf by leaf, joined by whitespace, **the way the eye reads it**. `textContent` welds neighbours (`"inferencesSee"`) and every word-boundary regex on it is one markup change from measuring a word that is not there. *(This is guard defect #30: the D183d guard reddened a correct panel.)* |

**Negative controls:** `_d194NegativeControls()` — **21 controls (13 bite · 8 must-not-fire)**, including *the
owner's own proposal adopted as written* (`AI Interpretation | Your Understanding`) and *the merged row, built*.

> **⛔ DL-111 + erratum (2026-07-14).** The panel was rebuilt from this two-`.pg-row` ledger into the **foundation
> bar** above. The ledger-**structure** guards (D194a *"no row says it twice"*, D194d *two `.pg-row` hosts*) are
> retired for this panel; **single-source** survives — D194b (`_assertEpistemicClassNamesAreSingleSourced()`) and
> D194c (`_assertThirdEpistemicClassIsRepresentable()`, the *"Attested by \<name\>"* epistemic class — unrelated to
> provenance state) still grade the class names on the bar's segments. Three **population** guards were added,
> because the old guards passed the erratum's three lies — **they only proved *computed* and *registry-sourced*,
> neither of which was the thing that was wrong:**
> - `_assertPgxBarIsComputedFromRealCounts()` — **the hero equals GROUNDED (attested) ALONE**, and goes RED if it
>   equals `grounded + inferred`, or if the grounded segment's width is not the real grounded count (defect 1).
> - `_assertPgxTwoProvenanceStates()` — the legend names **exactly TWO** provenance classes (grounded / inferred);
>   RED on any *derived / supported* third class (defect 2).
> - `_assertPgxBarStructure()` — load-bearing is **its own line, a SUPERSET**; RED if it is drawn inside the bar,
>   `+`-joined, or shown as a disjoint addition to the inferred claims (defect 3).
> The colour guard scopes **red to Critical**, keeps **orange off state**. **Build guards pass, 0 page errors,
> dark + light.**

---

## D195 (owner, 2026-07-13) — a class that resolves to NOTHING shipped a dialog with no background

### The defect

The *Usage & limits* dialog was `<div class="wm">`. **`.wm` is defined nowhere.** Five other dialogs carry
`.wmodal`. So the panel had **no background, no border and no radius** — and the page bled straight through it.

> **It was never a colour bug. It was a NAME bug, and the name looked perfect.**
> **This is the THIRD defect of this shape:** twice a **guard selector** matched **ZERO elements** and passed for
> free; now a **CSS class** matched **ZERO rules** and rendered a transparent modal. **The pattern is the bug.**

### The dialog registry — `_DIALOG_PANELS`

**25 panels**: 6 × `.wmodal` (limits · plans · share · export · reviewer · access) · 3 × `.modal` (signup ·
delete · upgrade) · `.upx` (**every** UP-* prompt) · `.issuepanel` · `.palette` · `.scopedpanel` · the
History-seam dialog (inline-styled — **graded exactly the same way**) · the Notifications drawer · `#confpop` ·
`#rptPop` · `#linkPop` · `#tourtip` · `#projmenu` · `#acctmenu` · `#rtTurnMenu` · `#rtToolbar` · `#findBar` ·
`#annoPop` (lazily created — the guard **instantiates the real element**, measures it, and puts it back).

### Guards

| Guard | What it proves |
|---|---|
| `_assertEveryDialogHasAnOpaquePanel()` | **D195a — THE P1.** For **every** panel: `getComputedStyle()` → **resolve the `var()` chain** against that theme's `:root` → parse to RGBA → **alpha must be exactly 1**. **In BOTH themes.** ⛔ **It grades the COMPUTED STYLE, never the class name** — *that is the whole point: the class name looked right.* **The apparatus proves itself first** (opaque · `rgba(…,0)` · `transparent` · **unpainted** probes); a blind resolver ⇒ **RED without grading a single panel**. **An empty enumeration or a selector that matches nothing ⇒ RED.** **Completeness:** every `*Scrim` that holds anything must yield a registered panel, and every `role="dialog\|alertdialog\|menu"` must **be** one or **contain** one — **so forgetting is mechanical, not moral.** |
| `_assertEveryClassNameResolves()` | **D195a — the general rule.** **A name must resolve to SOMETHING**: a CSS rule that paints it, **or** code that reads it (`querySelector` / `closest` / `matches` / `contains`). ⛔ **A WRITE IS NOT A READER** — `classList.add('wm')` proves nothing. Swept on **three** surfaces: **the live DOM · the render paths (`class="…"` literals — *this is where the second one hid*) · the writes.** **Guards and their NCs are apparatus, not product, and are excluded by the same rule the probe fence uses.** |
| `_assertOsloIsTheInferringActor()` | **D195b.** **PLANS DO NOT INFER. OSLO DOES.** No surface — DOM, render path or **TOUR registry** — may make the plan / document / artifact / report the **SUBJECT** of an inference verb. *"Inferred **FROM** the plan"* is a **SOURCE** and stays legal. **And the positive half is measured:** the subtitle must be on screen **and name OSLO**, or the map has lost its point. |
| `_assertFalseConfidenceFlagCountsAreComputed()` | **D195c / D173.** **STATE PROOF:** construct the false-confidence condition on the real model, **add three inferences to the flagged document, and the numbers on screen must move with them** (measured: **4 of 7 → 7 of 10**). **A literal cannot follow the state.** Both counts read off `_ciArtStats()` — **one home** (D179e). Does **not** duplicate `NC-D109-10`, which proves the flag's *subject*. |
| `_screenText(el)` | **The text a user can actually READ.** `<script>` and `<style>` live inside `<body>` in this file, so a naive text walk hands a copy guard **the entire source of the product — including its own doctrine comments — and the guard becomes its own subject.** `SCRIPT` / `STYLE` / `NOSCRIPT` / `TEMPLATE` subtrees are rejected. **Code is not copy.** *(Guard defect #33: the first draft of the D195b guard reddened on the sentence explaining why it exists.)* |

### The eight dangling names the sweep found

| Name | Where | Consequence | Fix |
|---|---|---|---|
| **`.wm`** | *Usage & limits* dialog | ⛔⛔⛔ **transparent modal** | → `.wmodal` |
| **`.in`** | Readout **Signed** input (**render path**) | ⛔⛔ **raw browser input** in a themed popover | → `.wm-in` |
| **`.referral`** | waitlist signal chip | ⚠️ a **data value in the class namespace** — the next key would dangle too | → `data-sig="<key>"` + `.wl-sig[data-sig="review"]` |
| `.attach-hint` · `.hart` · `.pg-star` · `.hli` | decorative / semantic hooks | none (each element's look is carried by a sibling class or its own inline styles) | **removed — not styled** |
| `.pn-on` · `.superseded` | **write-only** classes | none | **removed** *(whether a retired clarification box should LOOK retired is **escalated** — O-D195-1)* |

**Negative controls:** `_d195NegativeControls()` — **25 controls (19 bite · 6 must-not-fire)**, including **the P1
itself** (point the dialog back at `.wm`), the **85%-opaque panel that looks fine**, a panel pointed at an
**undefined token** (the same bug one level down), a panel broken **in the light theme only**, an **empty
enumeration**, a **blinded resolver**, an **unregistered dialog**, **the owner's own words adopted as written**
(*"Where the plan inferred"*), and **half-computed counts**. Must-not-fire: *a class with no rule but a real JS
reader is not dead* · *a plan may be the **SOURCE** of an inference* · *the flag's absence is correct* · *the guard
leaves no residue*.

---

## ⭐⭐ D196 — THE USER CONFIRMS. THE READ IS GROUNDED. (owner, 2026-07-13)

**The owner proposed replacing *ground / grounding* with *stabilize / stabilizing*. REJECTED — and the rejection
is the whole design of the fix.**

| Why *"stabilize"* fails | |
|---|---|
| ⛔ **It calls the FALSE-CONFIDENCE CASE a success** | *"Scope reads strong — but 8 of 11 items are inference"* is a **perfectly STABLE read. Its stability is what makes it DANGEROUS.** |
| ⛔ **It makes STILLNESS the goal** | OSLO's line is ***"honest, revisable confidence."*** A well-grounded read **should** move when new evidence arrives. That is the product working. |
| ⛔ **It has no opposite** | ***Grounded ↔ Inferred*** is the pair the whole provenance model teaches (**DL-109**). *"Stabilized ↔ Inferred"* is not an opposition at all. |
| ⛔ **It breaks the metaphor family** | *"Your read **RESTS ON** 13 inferences"* (**D186**) → rests on → foundation → **ground.** One picture. *"Stabilize"* belongs to balance and wobble. |

✅ **But the objection underneath is right — *"ground"* reads as jargon to a PM. So the VERB and the STATE split.**

> # **THE USER CONFIRMS. THE READ IS GROUNDED.**

| | Word | Where it lives | Why it is the right word |
|---|---|---|---|
| **D196a — THE ACTION** | **CONFIRM** | every **imperative · CTA · button · link** addressed to the user | **Already ratified.** *"Confirmed by you"* is one of the three epistemic classes (**D011/D069**) and now sits in the Progress ledger (**D194c**). **One vocabulary, everywhere.** |
| **D196b — THE STATE** | **GROUNDED** | *barely · thinly · partly · largely · well grounded* (**D183c**) — the Reliability qualifier on the hero, the pill and the popover | **Nothing else means *"resting on evidence"* without colliding.** ⛔ *"evidenced"* collides with **Evidence**, one of the three Reliability components — the **two-sizes-of-one-word** error (**D194b**). ⛔ *"confirmed"* **cannot** carry it: a read is grounded by **evidence** *and by* ***Attested by \<name\>*** — **and that is not the user confirming.** |

### The five copy sites that changed — and the one the grep missed

| # | Site | Before | After |
|---|---|---|---|
| 1 | `#ov-limit` — the hero limiter (**static DOM**) | *"**Feasibility** — the lowest. **Ground it** to lift the read."* | *"…**Confirm it** to lift the read."* |
| 2 | `renderLimiter()` — its **render path** | same string, rebuilt every read | **Confirm** |
| 3 | `#cpp-limnote` — the popover limiter (**render path**) | same | **Confirm** |
| 4 | `#cpp-out` — **the way-out CTA** (**render path**, object is a variable) | `'Ground ' + lim + ' →'` | `'Confirm ' + lim + ' →'` |
| 5 | ⛔ **`#cg-feas-tipb` — the CAF-row tooltip.** *A hover-only surface, lowercase, in the hero.* **No manual grep found it — the GUARD did.** | *"…the lowest dimension — **ground it** to lift the read."* | *"…**confirm it** to lift the read."* |

### And ONE guard was holding the old word in place

`_assertConfPopIsAReadout()` clause (5) asserted **`/\bground\b/`** on the limiter — so the moment the copy obeyed
the newer decision, **the build would have gone RED for being right.**
> ⛔ **A GUARD THAT PINS A WORD THE DOCTRINE HAS MOVED HAS BECOME THE DOCTRINE.** Clause (5) now asserts
> **`/\bconfirm\b/`**. **Fix the GUARD, never the doctrine (D166 §3).**

### `_assertConfirmIsTheVerbAndGroundedIsTheState()` — the split, made mechanical (D196c)

**Two prohibitions, in BOTH directions, graded by ROLE and never by substring:**
1. ⛔ **"ground/grounds/grounding" may never appear as an IMPERATIVE addressed to the user.**
2. ⛔ **"confirm/confirmed" may never appear as the RELIABILITY STATE BAND.**

**Five surfaces** — *the DOM · the attributes a user reads · the **TOUR registry** (twice caught teaching a dropped
concept) · **`PN_SLOTS`** · the **RENDER PATHS*** (`'Confirm ' + lim` is a CTA whose object is a **variable** — no
DOM scan can see it until the state that renders it arrives).

**The role test, not the word:**
- the VERB rule fires only on the **bare-form verb + a DIRECT OBJECT** (*"Ground it" · "Ground Feasibility"*);
- ✅ *"largely grounded"* (**the STATE**), ✅ *"you grounded"* (**past tense — D187's green count; a measured fact,
  not an order**), ✅ *"Your evidence is solid ground."* (**a NOUN**), ✅ *"Progress is grounding, not clearing"*
  (**a gerund with no object, addressed to nobody**) — **all legal, all still on screen**;
- ✅ *"Confirmed by you"* (**the epistemic CLASS**) is legal against the STATE rule — and the guard **measures that
  it still renders**, because *the verb moved to Confirm precisely BECAUSE the class name already said it*.
- ⚠️ **WORD BOUNDARIES:** *"background"* contains *"ground"*; *"lowest"* contains *"owes"* (DL-109 §3).
- ⚠️ **THE SCANNER IS NOT ITS OWN SUBJECT:** `_screenText()` rejects `SCRIPT`/`STYLE`; the source sweep uses
  `_edCodeOf()`, which **strips the doctrine comments — which necessarily quote the dead imperative to explain why
  it died.**

**`_d196NegativeControls()` — 18 controls, 0 dead.** 11 bite (*"Ground it"* back on a **button** · on the **CTA** ·
in a **render path** · in the **TOUR** · in a **prototype note** · in a **tooltip** · the limiter loses its verb ·
the band renders *"well confirmed"* · the **vocabulary itself** is rewritten · the state says *"largely evidenced"*
· the sweep **mangles the epistemic class name**) + **6 must-not-fire** (*Confirmed by you* · *largely grounded* ·
*you grounded* · *solid ground* · *background/groundbreaking* · the Progress doctrine is intact).

---

# D197 · D198 · D199 — the NAME, the MARKER, and the guard that was never built (owner, 2026-07-13)

## D197 — the term is **LOAD-BEARING**, and it lives in ONE registry

**D186 rejected *"load-bearing"* as *"internal vocabulary."* That was wrong.** *A **load-bearing wall** is the most
intuitive metaphor in the language for **"remove this and the thing falls down."*** Two words, **zero ambiguity** —
unlike *"holding it up"*, which the owner read **backwards** — **and it pairs exactly with *"rests on."***

```js
const TERMS = {
  loadbearing:       {label:'Load-bearing', noun:'inferences', name:'Load-bearing inferences'},
  outcomeConfidence: {label:'Outcome Confidence'}
};
```

| Surface | Was | Is |
|---|---|---|
| **Progress · load-bearing** (`.pgx-leans`) | `YOUR READ RESTS ON` | **DL-111+erratum: no labelled row** — a *leans* line **below the bar** (a superset), not a `TERMS` label |
| **Progress load-bearing value** | *"13 inferences ↓7 · See them →"* | **DL-111+erratum: *"Your read leans on 12 inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →"*** — the neutral ↓ delta and the `See them →` link stay, on the leans line |
| **Count registry name** (`PAYOFF_COUNTS.loadbearing.label`) | *"Inferences your read rests on"* | **`TERMS.loadbearing.name` = "Load-bearing inferences"** |
| **Assumption row** | chip: `YOUR READ RESTS ON THIS` | **a MARKER** (D198) + `title` + `.mk-sr` — all named from `TERMS` |
| **Section header** | *"The ones your read rests on come first"* | **unchanged — PROSE. The metaphor is the point.** |

> ⚠️ **D194a vs D197 — the one place the two decisions collide, resolved conservatively and escalated.**
> D197 wrote the value as ***"13 load-bearing inferences."*** But the value *today* is already **"13 inferences"** —
> **D194a stripped the trailing phrase, because the LABEL is the sentence** (one home, D179e). Rendering *"13
> **load-bearing** inferences"* **beneath a `LOAD-BEARING` label puts the name in two homes** — the exact defect
> D194a removed, and its guard goes RED. **So the label carries the name and the value carries the number and the
> noun**, and the full phrase *"Load-bearing inferences"* is `TERMS.loadbearing.name`, spoken on the surfaces that
> carry **no separate label**. → **O-D197-1** in `open-items.md`.

**The guard is a MECHANISM, not a grep.** `_assertLoadBearingIsTheOneName()` swaps `TERMS` for a **sentinel**,
repaints, and requires every naming surface to show the sentinel. *A surface that still shows the real word has the
name typed into it — which is exactly how **D199** happened.*

## D198 — **a MARKER, not a LABEL**

> ### **A ROW THAT NEEDS ATTENTION SHOULD BE *MARKED*, NOT *CAPTIONED*.**
> **A label competes with the content for the row. A marker sits beside it and lets the content keep its alignment.**

**Two offenders, one disease.** The `YOUR READ RESTS ON THIS` chip sat on **six consecutive rows** — and was
**redundant with its own section header** (*"The ones your read rests on come first"*): **the sort order was already
the signal.** It re-stated it six times and **shoved every marked row's content sideways.** `VERIFY` did the same to
the by-document stat row: a **button in a number column**, and the counts justified around it.

```css
/* the GUTTER is reserved on EVERY row, in the ROW's own rule */
.inf-row {padding:6px 8px 6px 20px}
.inf-item{padding:10px 2px 10px 20px}
/* the MARKER paints INTO it — and cannot enter the flow */
.mk{position:relative}
.mk-on::before{content:'';position:absolute;left:6px;top:11px;bottom:11px;width:3px;border-radius:2px;background:var(--cool)}
.mk-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}   /* out of flow, by cascade AND by data-flow="none" */
```

- **Every row carries `.mk`.** Only the marked ones carry `.mk-on`. **`.mk-on` declares NO flow property at all** —
  no padding, no margin, no width, no display, no gap. **It can only paint.**
- **Not colour alone** (WCAG 1.4.1): the discriminator is the **existence of a bar**, not its hue. `--cool` on the
  card clears **6.13 : 1 (dark) / 6.28 : 1 (light)** — WCAG 1.4.11 wants 3:1. **And it is not severity colour**
  (D003 — a load-bearing inference is a thing to *read first*, not a fault).
- **The meaning is on demand** (DL-107/D185): the **section header** + a new **ⓘ** on each of the two sections.
- **`VERIFY` left the number column.** The **row itself** is `role="button"` + `tabindex="0"` and **Enter/Space opens
  the document** (7/7 rows), and the `.inf-flag` callout carries the same action **named** (*"Open Resources →"*),
  keyboard-reachable. **Two keyboard paths, zero resident buttons.** *An action that only exists on hover is
  unreachable — a11y was not traded for tidiness.*

### The geometry proof — **measured, three ways**

| Clause | What it measures | Result |
|---|---|---|
| **(1) in-flow child signature** | the marked row and the unmarked row have the **same sequence of in-flow children** (out-of-flow nodes excluded **by declaration**, `data-flow="none"`, then **proven** against the cascade) | `.inf-item` **`span.tx \| span.inf-src`** — identical · `.inf-row` **`span.inf-nm \| span.inf-pips \| span.inf-ct`** — identical |
| **(2) computed box model** | `padding-left/right`, `margin-left/right`, `display`, `gap` off a marked and an unmarked row | `.inf-item` **`20px \| 2px \| 0 \| 0 \| flex \| 11px`** — **identical** · `.inf-row` **`20px \| 8px \| 0 \| 0 \| flex \| 12px`** — **identical** |
| **(3) real pixels** | content start-x and end-x, compared across marked/unmarked, within 1px | live in the guard; **fires in any real browser.** ⚠️ In jsdom every rect is zero, so the clause **says so and does not pass on its own** — *rects that are all zero are ABSENT, not identical* (D166 §1) |

## D199 — **the concept is called OUTCOME CONFIDENCE**, and now it is guarded

**D183b bound TWO things: *(a)* delete the 0–100 index, *(b)* adopt the label. A guard was built for (a) and NOT for
(b).** So the index is provably gone — and **the NAME was left to be remembered.**

> ## **WHAT IS NOT GUARDED IS NOT TRUE.**

**`_assertTheConceptIsCalledOutcomeConfidence()` — grade the ROLE, not the substring.** The bare word may appear
inside prose. It may **never be the LABEL for the concept**:

- **(L1)** the word standing as the **complete text** of a labelling node or a readable attribute;
- **(L2)** the word **immediately followed by a BAND or a number** (*"Confidence Moderate"* · *"Confidence: High"*);
- **(L3)** the word **compounded into the concept's name** (*"Confidence **trend**/**band**/**pill**/**score**"*);
- **(L4)** the word as the **subject of a state verb** (*"Confidence **sits at**…"* · *"Confidence **strengthened**"*).
- ⚠️ ***"is"* is deliberately NOT a state verb here.** *"Confidence **is** understanding maturity — not project
  health"* is **the doctrine, written as prose**, and a guard that reddened on it would be a **word filter** (D166).
  *"is"* is a hit **only when a band follows it.**

**Eight label sites, each of which must RESOLVE** (a selector matching nothing is a **FAILURE**): `pill` · `hero` ·
`popover` · `ramp` (aria) · **`trendTip`** · **`trendSvg`** · `whybox` · `export`. **The trend and the export package
are DORMANT at boot** — *and "it wasn't on screen" is exactly how D199 happened* — so **the guard paints them from
their own render paths, reads them, and puts every byte back** (D182).

**Swept:** the DOM · every `title`/`aria-label`/`data-tip`/`placeholder` · the **TOUR** · **`PN_SLOTS`** · the
**render paths**.

# Slice 10 — Tiering & Limits · Workflow

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


## The one fire path — every prompt in the product goes through it

```
attempt (the control is ALWAYS enabled)
   └─> gate  (_capHit / _deepAllowed / checkAdmission — the simulated 422/429)
         └─> fireUP(id, ctx)
               ├─ GUARD 1  first value delivered?  (first MRI)              — no → SILENT
               ├─ GUARD 2  is a Fast/Deep pass running? (_passActive)       — yes → SILENT
               ├─ GUARD 3  per-trigger cooldown (ratified cadence)          — no → SILENT
               ├─ GUARD 4  global per-day cap (guard canon; number UNSET)   — no → SILENT
               │            [AMENDED 2026-07-11 — the MONTHLY TOKEN GOVERNOR is the binding gate (§4c):
               │             Free 4M · Basic 10M tokens/month. Daily caps = burst-smoothers.
               │             Evidence path: RECORD (never refused, CR-2) → DEFER the run → DISCLOSE.]
               └─> render the RATIFIED prompt + its RESOLUTIONS (free one first)
```
There is exactly one `fireUP`. A prompt that cannot pass all four guards **does not appear** — the attempt simply proceeds or is quietly refused with the state left untouched. **Silence is an acceptable outcome; nagging is not.**

## Cap → attempt → prompt (D138), per cap

| Cap | User does | Product does | Prompt | Free resolution |
|---|---|---|---|---|
| Projects (1/3) | Workspace → **New project** | `wsNewProject()` → `_projectCap()` hit → `openUpgrade()` | **UP-3** | **archive** (reversible, frees the slot) |
| Fixes (5/20) | Issue Panel → **Apply this fix** | `applyFix()` → `_capHit('fixes')` → prompt; **the plan is untouched** | **UP-1** | **wait for reset** (real time) |
| Chat (20/—) | Chat → **Send** | `sendChat()` → `_capHit('chat')` → prompt; **the typed question stays in the box** | **UP-2** | wait for reset |
| Deep runs (2/—) | applies a fix / edits the plan | the **edit saves**; `_deepAllowed('user')` false → the **run defers**; History records the deferral; the read stays at **last-good** (D098g) | **UP-5** | **keep the last analysis** |
| Export (PDF/all) | Export → **Copy summary / Export link** | `doExport()` → prompt | **UP-EXPORT** | **export as PDF instead** |
| Seats (3/10) | Share → **Invite** as Collaborator | `checkAdmission()` → `tier` → prompt **inside the dialog** | **UP-SEAT** | **add as Viewer** (no seat, unlimited) |

## The evidence lane — never gated (CR-2)

```
reviewer responds  ──> _reviewAnalysisRun()
                        ├─ _meterSpend('deep', {evidence:true})   ← COUNTED (it costs tokens, DL-048)
                        ├─ NO _capHit.  NO _deepAllowed.  NO tier check.   ← by design
                        └─ Extended Analysis runs IMMEDIATELY, on every tier, in every phase
```
`_assertEvidenceNeverGated()` fails loudly at runtime if a gate ever appears on this path. **A stakeholder's read is how the user gets their answer** — metering it would degrade their understanding *on purpose*, in order to sell them an upgrade (D126).

Evidence runs are shown to the user in **their own counter lane**, labelled **"never metered · uncapped"**, next to the metered ones. The user can see that the thing that matters most is the thing that is never rationed.

## Deep runs: which triggers are gated, and which are not

| Trigger | Gated? | Why |
|---|---|---|
| Initial Fast/Deep pass (first read) | **No** — counted only | It is the first delivery of value. Gating it gates the product. |
| Apply this fix → analysis update | **Yes** (UP-5) | User-initiated; costs real tokens. The **edit still saves**; only the **re-read** defers. |
| Reviewer response → analysis update | **NEVER** | CR-2 / D120 / D126. Load-bearing, not a preference. |
| Clarification answer → analysis update | **No** (counted) | The user is *supplying evidence*. Canon does not name it in the limit-reached table → **escalated, not invented.** |

## First value → the engine arms

```
intake → Fast Pass → MRI delivered → afterOrientation()
                                        ├─ _markFirstValue()   ← the ONLY place the engine is armed
                                        │     └─ UP-8 (celebrate; no hard sell; once ever)
                                        └─ startDeepPass()     ← _S10_deepInFlight = true (Guard 2 active)
```
Before `_markFirstValue()`, **`fireUP` refuses every trigger** — verified: a fix cap hit during onboarding produces no prompt at all.

## Meter lifecycle

- **Daily** (`fixes`, `chat`, `deep`): keyed to the calendar date in `localStorage`; a new day = a fresh object. Reset shown as a **real time** ("midnight — in 4h 12m").
- **Monthly** (invite allocation): calendar month (X-3) — "replenishes 1 August".
- **Never** (artifacts, History, viewers, review requests): no counter to reset, because there is no cap. They appear in *Usage & limits* as **∞**, precisely so that nobody can quietly add a cap without deleting a ratified constant.

---

# The readout (M4) — **D148–D154 · REBUILT** · the flows

## Open (a view switch, not a modal)
`showView('reports')` → `#pane-reports` goes `.active`, `_syncNav()` highlights the sidebar item, the crumb reads **Readout**, and `renderReports()` paints **three** surfaces: the composer (`#reportsBody`), the package wrapper (`#rptPkg`) and the document (`#rptDoc`). **No analysis. No meter. No governor.**

## Compose → send
1. **Pick a recipient** → `setReportRecipient()`. **Only section 6 changes.** (`_assertAskTailoredNeverTheRead()` byte-compares the whole read across all four recipients on every boot.)
2. **Rewrite anything** → `editReportSection()` → a real editor (plain prose; `**bold**`, `- bullets`) → `saveReportSection()`. **Free on every tier.** `RPT_EDITS` holds it in memory; `_saveEdits()` writes it down **only on Basic**.
3. **Add an extra section** (Basic) → on Free the chip is live and the *attempt* fires `UP-REPORT` (D138), whose first resolutions are both free: *write it yourself now* and *export the whole thing as PDF*.
4. **Export** → `genReport()` → a **dated snapshot** carrying `cover.disclaimer`, `cover.mark` and `cover.currency`. It spends **no meter**, touches **no governor**, and moves the read by **zero degrees**.

## Next week
`simNextWeek()` — the demo trigger for the only gate on this surface. **Free:** `RPT_EDITS` is wiped, the report re-seeds from the *current* plan, and the persistence prompt fires. **Basic:** the wording comes back, applied — and the numbers underneath are re-read from the current plan. **Basic remembers your words; it never remembers a stale read.**

## Schedule → send (Basic)
`toggleReportSchedule()` → `runScheduledReport()` **re-checks currency at send time**. If the plan has moved on, the package **says so on its face** and goes out labelled **"previous analysis"**. It never quietly ships a stale read as current, and it **never runs an analysis to freshen itself** — that would make a report *produce* understanding.

## What none of these paths ever do
Run an analysis · spend a meter unit · touch the governor · move the read · re-frame the assessment for the audience · gate the edit · put a disclaimer in the prose · forecast the outcome.

---

# ⬛ AMENDED 2026-07-12 — **D165 · the chat conversation loop**

```
askOslo({type:'issue', id})
  → _chatDivider(label, key)          ← D165d: a NEW context inserts a VISIBLE divider (same context ⇒ none)
  → _ansIssue(id, S, true)            ← D165a: ~40 words · what it is · why it matters · one epistemic line
      · ONE action  (Open this issue →)
      · HANDOFF     (What's it resting on? · What are my options? · Answer your question / What would you do?)
  → renderChatChips()                 ← D165c: the composer's chips VANISH — a conversation is underway

user clicks a chip → sendChat() → _oslloReply(q) → the PULL routes (matched FIRST):
  "What's it resting on?"  → _ansEvidence(ref,S)        → the sources        → handoff
  "What are my options?"   → _ansOptions(id,S)          → the paths          → handoff
  "What would you do?"     → _ansRecommendation(id,S)   → the recommendation → ONE action: Apply this fix → → handoff
  "How sure are you?"      → _ansReliability(S)         → Coverage · Evidence · Assessability → handoff
  "Answer your question"   → _ansClarifications(S)      → COLLAPSED one-line prompt (D165e)

clarification answered in chat:
  chatClarToggle(id) → expand → answerClarificationFromChat(id)
    → _submitClarification(id, val, 'chat')   ← THE SAME function the Issue panel calls
    → byte-identical History entry.  No side channel. Ever.
```

**The chat still acts on nothing.** Every action above is a link the **user** clicks, running the function that the
**owning surface** already owns. `_assertChatNeverMutates()` proves it at every boot by snapshotting the whole model
across a 12-question battery.

---

# D171 — THE SEND PATH

```
REPORT (living, editable, artifact-parity)
   │
   ├── SEND ─────────► _mkMemo(SHARE_CHANNEL, false, ++seq, 'shared')
   │                     · freezes a MEMO (cover · disclaimer · currency marker) — D168
   │                     · NO tier check · NO meter · NO prompt        — CHG-061 (free on every tier)
   │                     · runs NO analysis                            — D146
   │                     · pushHistory('share', …, {memo: id})         — D169
   │                     · read-only for the recipient; relabelled "previous analysis" when the read moves on
   │
   └── EXPORT ───────► _mkMemo(format,        false, ++seq, 'exported')
                         · the SAME factory, the SAME freeze, the SAME cover  — D171 §2
                         · FORMATS are tier-bound (Free = PDF)               — MON-01
                         · runs NO analysis                                   — D146
                         · pushHistory('export', …, {memo: id})               — D169

HISTORY ── click a memo row ──► openMemoFromHistory(id) ──► the FROZEN bytes, from either road.
                                 Selects out of the register. Never re-renders. Runs nothing.
```
**One factory. One freeze. One immutability. `sent_via` records the journey — never the object.**

---

# D172 — THE SCHEDULED SHARE, AND THE GRANT

```
SCHEDULE (Basic) ── cron fires ──► runScheduledReport()
                                     │  ⛔ re-checks currency FIRST (D147) — of the LIVE state
                                     │  ⛔ runs NO analysis. Ever. (D146)
                                     ├─► _mkMemo(SHARE_CHANNEL, scheduled, seq, 'shared')   — ONE factory (D171 §2)
                                     ├─► _shareMemoGrant(memo, recipient)
                                     │     ├─ _mkLink('memo', memo.id)        — scoped · revocable (D117/CR-6)
                                     │     └─ _grantMemoAccess(…) ─► _grantScopedAccess('memo', …)
                                     │           ⛔ THE ONE ADMISSION PATH — the same one the reviewer grant takes.
                                     │           no seat (N-2) · no invite (CR-2) · no tier check (CHG-061)
                                     └─► pushHistory('share', 'Scheduled memo sent to …', {memo: id})   — D169

RECIPIENT ── opens the link ──► openSharedMemo(id) ──► the grant landing (the link IS the invite)
                                  └─ rvvAcceptGrant() ──► _renderSharedMemoView()
                                       SELECTS the frozen memo. Never rebuilds it. Runs nothing.
                                       read-only · cover · disclaimer · currency marker · "previous analysis" when overtaken

THE TIER RULE (D172b):   sendMemo()            → NO tier check, and there may never be one.   THE SHARE IS FREE.
                         toggleReportSchedule() → TIER check + fireUP('UP-REPORT', {sched}).  THE AUTOMATION IS BASIC.
```
**Meter the labour, never the understanding.** The same shape as D154: *editing is free; persistence is the gate.*

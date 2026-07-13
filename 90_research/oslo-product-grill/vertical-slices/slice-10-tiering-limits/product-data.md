# Slice 10 — Tiering & Limits · Product Data

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


Client-side only. `localStorage` (`oslo-s1-*`), fake data, simulated AI. **No billing rail** (T-4).

## `TIER_DEFS` — the registry (the single source of truth)

Every number the product consumes lives in **one array**, and every surface renders from it. `tier-definitions-census.md` is generated from this same array, so the doc cannot drift from the code.

```js
{ k, grp, lab, val, unit, status:'RATIFIED'|'RECOMMENDATION'|'UNSET', src, note?, esc?, surf[] }
```
- `status:'RATIFIED'` → `src` is the **canon citation**; `val` is authoritative.
- `status:'RECOMMENDATION'` *(added 2026-07-11)* → the build carries a number **canon has not ratified**. It renders **visibly as a recommendation, in-product**. Never dressed as canon; never used to sell anything.
- `status:'UNSET'` → `val` is **null**, it **renders unset**, and `esc` states the decision the owner still owes.

> **⚠️ AMENDED 2026-07-11.** ~~**32 rows · 21 RATIFIED · 11 UNSET.**~~ **The tier ladder was ratified all along, in `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1 §4c`** — the zone the product-grill scan does not cover.
> **Corrected: 53 rows · 46 RATIFIED · 3 RECOMMENDATION · 4 UNSET.**

## Constants (with their citations, at the site)

| Constant | Value | Source |
|---|---|---|
| `FREE_ACTIVE_CAP` | `1` | §4c Free · UP-3 |
| `BASIC_PROJECT_CAP` | **`3`** | **§4c Tier 2 · UP-3 — supersedes the AI-invented `10` carried by Slice 9 (DL-102 Correction #3)** |
| **`BASIC_PRICE`** | ~~`null`~~ → **`12`** | ✅ **§4c — "$12/mo", owner-confirmed 2026-06-05; DL-074 §4.** *Was rendered as an owner-TBD. It was never one.* |
| `PRO_PRICE` / `TEAM_PRICE` / `ENT_PRICE` | `39` · `'99–149'` **per seat** · `'custom'` | ✅ DL-074 §4 (Ratified 2026-06-19, starting values) · §4c T3–T5 |
| `PURCHASABLE_R1` | `{free:✓, basic:✓, pro:✗, team:✗, enterprise:✗}` | D123 + DL-074 — the forward ladder is **shown and priced, with no Buy button** |
| **`TOKEN_GOVERNOR`** | `{free:4_000_000, basic:10_000_000, pro:25M, team:50M/seat}` | ✅ **§4c — "the binding governor". THE LIMIT THAT ACTUALLY GATES.** |
| `DAILY_TOKEN_BUDGET` | `{free:500_000, basic:1_500_000}` | §4c — **burst smoothing, not the gate** |
| **`ENVELOPE`** | ~~`{free:null, basic:null}`~~ → `{free:{20 docs, 50k words}, basic:{40, 100k}, pro:{80, 200k}, team:{150, 400k}}` | ✅ **§4b CHG-056 (owner-confirmed 2026-06-05) + §4c.** *UP-4's "~100k words" is **not** illustrative — it is **Basic's envelope**.* |
| `ROUTING` | Free/Basic **nano+mini (same class)** · Pro **+ full-quality fallback** · Team **premium** | ✅ §4c — **Basic sells capacity; Pro adds model quality** |
| `OVERAGE_ELIGIBLE` | `{free:false, basic:true, pro:true, team:true}` | ✅ **DL-074 §3 — paid tiers only** |
| `FREE_PURCHASE_PATH` | `false` | ✅ **DL-074 §3 — "Free converts via upgrade… no Free purchase path." NEVER build one.** |
| `OVERAGE_UNIT` / `OVERAGE_GUARDRAILS` | per Deep Pass · visible meter + user-set spend cap + threshold alerts | ✅ DL-074 §2/§5 — *no silent overspend, no bill shock* |
| **`SEAT_CAP`** | `{free:3, basic:10}` — ⚠️ **RECOMMENDATION, NOT RATIFIED** (`SEAT_CAP_STATUS`) | ⚠️ **§4c has NO seat row for Free/Basic/Pro.** D129 X-1 / DL-102 E is a recommendation. **Basic = 10 cannibalises a ~$99–149/seat Team.** Escalated; **no replacement number invented.** |
| `VIEWER_CAP` | `{free:∞, basic:∞}` | X-1 — there is no number to set |
| `CR2_GOVERNOR_BEHAVIOUR` | `'record-defer-disclose'` — ⚠️ **RECOMMENDATION** | ⚠️ Canon has not decided what happens when evidence arrives after the governor gates (CR-2 · CRR-04 · §4c). |
| `EXPORT_FORMATS[].free` | PDF only on Free | MON-01 / SHARE-04 / D112 |
| `COALESCING_WINDOW` | `null` | ⬜ **OD-10** — coalescing is **on** (§4c); the **window** is unset. The highest-leverage number in the product. |
| `CRR_CAP_FREE` | `null` | ⬜ D118 / B-1 |
| `PROMPT_GLOBAL_CAP_PER_DAY` | `null` | ⬜ MON-04 (the **guard** is canon; §4d's number is *proposed*, not ratified) |
| `BILLING_RAIL` | `null` | ⬜ T-4 — engineering. **The price is decided; the rail is not.** |
| `ARTIFACTS_METERED` / `HISTORY_METERED` | `false` | **D128 P1 — never metered** |
| `EVICT_ON_DOWNGRADE` | `false` | D132 — no eviction, ever |
| `REJECT_MOVES_CAF` | `true` | D133 |
| ~~`ANALYSIS_BUDGET`~~ | **REMOVED** | ~~`{free:null, basic:null}` — "monthly Extended-Analysis run count, owner-TBD"~~ — **it was never a canon dimension.** The real monthly limit is `TOKEN_GOVERNOR`. |
| ~~`ENVELOPE_WORDS`~~ | **REMOVED** | ~~`{free:null, basic:null}`~~ — superseded by `ENVELOPE` (ratified). |

## Persisted state (localStorage)

| Key | Shape | Reset |
|---|---|---|
| `usage` | `{day:'Y-M-D', fixes, chat, deep, deepEv}` | **calendar day** — a new day yields a fresh object |
| **`gov`** *(new)* | `{month:'Y-M', tok}` — the **monthly token governor** rollup | **calendar month** — the binding gate (§4c). Every AI run rolls up here via `_govSpend()`. |
| `promptLog` | `{day, n, fired:{UP-x:ts}}` | calendar day (drives the per-day cooldown + the global cap) |
| `promptSeen` | `{UP-x: count}` | never (drives "once ever" — UP-8) |
| `promptMonth` | `{UP-x: 'month-year'}` | calendar month (UP-6) |
| `firstMRI` | `bool` | never (the prompt engine's arming flag) |
| `tier` | `'free'｜'basic'` | user action (simulated upgrade) |
| *(Slice 1–9 keys unchanged)* | | |

**`deepEv` is a separate lane.** Evidence-driven Extended Analyses are counted there and **never** against `deep` — CR-2 (they are shown to the user, labelled uncapped).

## What is deliberately NOT modelled

- **Billing / payment** (T-4) — the upgrade is simulated end-to-end and says so at every touchpoint.
- **Server-side enforcement** — the 422/429 is simulated in the client; the *interaction contract* (D138) is what this prototype proves.
- **The unset numbers** — no default, no placeholder, no "reasonable guess". `null` renders unset. **This is the whole point of the slice.**

---

# The readout (M4) — **D148–D154 · REBUILT** · data

## Registries
| Name | Shape | Notes |
|---|---|---|
| `REPORT_RECIPIENTS` | `{k, lab, email, ask}` | Grounded in `TEAMMATES` + an *Executive / board* option. **Drives §6 only.** |
| `MEMO_WORKSTREAM` | `artifact → English label` | *Intent → "What the event is for"*, *WBS → "Who does what"* … The plan's internal names are OSLO's business, **not the sponsor's** (D149). |
| `MEMO_RISK` | `issueId → {t, p, plan, goal}` | The risk copy. **`plan` and `goal` are the two altitudes** (D151). `goal` is always a claim about **the plan as written** — never a prediction. |
| `MEMO_PLAN_SEED` | `issueId → first-person step` | **The seed only.** The PM edits and owns it (D152). |
| `MEMO_ASKS` | `recipientKey → [{iss, d, own, un}]` | §6. A row renders **only while its issue is still open** — no manufactured asks. |
| `REPORT_OSLO_VOCAB` | `string[]` | **The banned vocabulary** (D149). Word-boundary matched against the rendered `#rptDoc`. **No denial exemption.** |
| `REPORT_FORECAST_WORDS` | `string[]` | probability · likelihood · likely · forecast · predict · on track … (D151). |
| `REPORT_OPTIONAL` | `{k, lab, sub}` | The **extras** (Basic): *Where we do not yet agree* · *How the picture has changed*. **NOT the seven sections** — those are free, in full. |
| `REPORT_SNAPSHOTS` | `{id, n, fmt, fmtName, stamp, runIndex, run, when, to, toLab, cover{disclaimer, mark, currency}, edits, persisted, brand, stale, scheduled}` | The dated snapshots. **`cover` is the wrapper** — where the disclaimer lives (D153). |

## Persisted state (localStorage)
| Key | Shape | Notes |
|---|---|---|
| `rptComposer` | `{to, opt{}, brand, week, signed}` | Composer prefs. `to` drives §6 only. |
| `rptSchedule` | `{on, cadence, to}` | Scheduling (Basic). |
| **`rptEdits`** | `{sectionKey → html}` | ⛔ **D154 — WRITTEN ONLY ON BASIC.** `RPT_EDITS` lives in memory on **every** tier (editing is free); `_saveEdits()` writes it down only when `_editsPersist()` is true. **On Free, nothing is kept — and nothing is taken away either.** |

## Derived, never stored
The whole memo. `_memoSummary()` / `_memoChanges()` / `_memoRisks()` / `_memoAssumptions()` / `_memoPlan()` / `_memoAppendix()` read live `ISSUES` · `_istatus` · `HISTORY` · `TREND` · `_epiOf()` and are **blind to the recipient** (D145). `_memoDecisions()` is the only builder that knows who is receiving it.

## Flags that are deliberately UNSET / owner-open
`SCHEDULING_R1 = null` (R1 or fast-follow?) · `REPORT_BRANDING_TIER = 'basic'` (owner-open) · `REPORT_NAMES_PENDING = true` (DL-053) · **the UP-number for the persistence prompt** (no `UP-*` in canon covers it — ESCALATED).

## What is NOT modelled
Real PDF generation · a real mail send · a real schedule · a rich-text editor (the section editor is prose with `**bold**` and `- bullets`, converted on save) · any second copy of the plan. **The report packages; it never produces.**

---

# D177 — THE DEEP PASS FINDS THINGS. `DEEP_FINDINGS` (owner, 2026-07-12)

**The payoff machinery was correct. The DEMO DATA was the defect.** The Extended pass fired the payoff, said
*"deeper analysis firmed the read"* — and **changed nothing countable**. The narrative claimed something happened;
the counts said nothing did.

**A real Deep Pass re-reads the SAME evidence more thoroughly.** So it does **both**, in one run: it **finds issues
the Fast Pass had no budget to find** (counts go **up**) **and** it **firms the read** (the band goes **up**).

## The registry

`DEEP_FINDINGS` — two issues, in the **same shape** as `ISSUES` (`rectype · title · sev · dim · sec · why · ev ·
caf · rec · paths`). **They are NOT in `ISSUES` and NOT in `_istatus` at boot** — so every count, list, heat cell
and artifact annotation treats them as *not yet found*. `_deepPassSurfaceFindings()` is **the one door**; it is
idempotent and returns the ids it actually surfaced, so **every downstream number is computed from what happened**.

| id | sev | CAF | artifact | what a deeper read of the EXISTING evidence surfaces |
|---|---|---|---|---|
| **ISS-07** | **critical** | Feasibility | **Schedule** | **Sponsor funding closes after the costs are committed.** *Schedule* says sponsor sales close **Aug 15**; *Resources* already carries **AV vendor — Confirmed** and **Caterer — Confirmed**; *Intent* says the event is **sponsor-funded**. The Fast Pass read each artifact. The Deep Pass reads them **against each other**: the plan commits the spend before the revenue is signed, and names no minimum floor. |
| **ISS-08** | moderate | Clarity | **Scope** | **Recording is resourced but never scoped.** *Scope* lists recording in the logistics and puts the event **in-person only**; *Resources* has the **AV vendor doing recording**; *Requirements* sets **no recording deliverable, capture standard or consent**. The plan is paying for something it never defines. |

**⛔ No new facts.** Every citation is an existing plan artifact; both bind to a real CAF dimension; both are
anchored to a **real span** in the artifact they came from (`data-fid="ISS-07"` in Schedule, `ISS-08` in Scope).
**The weak text was always there** — `_artBodyLive()` leaves the span **inert (plain text)** until `_istatus`
says the issue is open, so the Fast-Pass draft reads exactly as it did before, and the *mark* is what is new.

---

# D178 — AND THE DEEP PASS **ASKS**. `DEEP_FINDINGS['ISS-07'].clar` (owner, 2026-07-12 — closes O-D177-2)

> **Finding an issue and knowing what would close it are different acts — and OSLO can do both.**

A deeper read that spots the **funding-vs-commitment gap** should **ask about the sponsor floor**, not merely flag
it. So **ISS-07 now carries a `clar`** — the same field ISS-01 and ISS-02 carry, with the same shape (`q` · `hint`):

| field | value |
|---|---|
| `clar.q` | *"Is there a minimum signed-sponsorship floor — or a cancellation point — that has to be cleared before the AV and catering commitments go firm?"* |
| `clar.hint` | *"Your inputs state the sponsor close date and the confirmed vendors, but no floor and no cancellation terms."* |

**⛔ No new facts.** The question **re-reads the evidence ISS-07 already cites** — *Schedule* (`sponsor sales close
Aug 15`), *Resources · Vendors* (`AV vendor — Confirmed` · `Caterer — Confirmed`), *Intent* (sponsor-funded). It
asks about **what is absent from those inputs** (a floor, a cancellation point). **OSLO does not know the answer,
and says so.**

## The third true count

`_openClarIds()` = *every issue with a `clar` that is not resolved*. It is already the `get()` behind the
**`questions`** row of `PAYOFF_COUNTS`. So surfacing ISS-07 **moves the count by itself**:

> **Open questions 2 → 3** — **computed, never typed in.** A question that is not in state cannot move it; a
> question that **is** in state cannot be hidden.

Verified in jsdom: `_openClarIds()` → `[ISS-01, ISS-02]` before the pass → `[ISS-01, ISS-02, ISS-07]` after.

## Nothing is special-cased

The ask is an **ordinary `clar` on an ordinary issue**, so everything downstream is the code that already existed:
the **collapsed** panel row (D162c) · the **collapsed** chat block (`_chatClarBlock`, D165e) · the clarification
pointer on the Overview · §3 of the Strategic Readout (*"what we don't know yet"*) · and `_submitClarification()`,
which is **the only path** either surface can answer through — so panel and chat write a **byte-identical History
entry** (D096, verified). **Answering closes the gap through an analysis update — never by hand** (D088):
`open → Addressed → (analysis update) → Resolved`.

**`_deepPassSurfaceFindings()` remains the one door.** `deepComplete()` derives the asked ids from what it actually
surfaced (`_found.filter(id => ISSUES[id].clar)`) — **so the ask cannot be claimed by a pass that found nothing.**

**Confirmed artifacts stays at `0 of 7` through the pass and is correctly absent** — a count that did not move is
not news (D173). **A Deep Pass re-reads; it attests nothing.**

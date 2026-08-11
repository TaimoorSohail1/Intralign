# R2 Slice 7 — Reports & Export / Hand-off — Build Design

*Grill artifact · 2026-08-06 · DRAFT — awaiting sign-off. Grounding: capability #10; the export objective audit (2026-08-05); underspecification audit §4.6 (R2G6/R2G11) + §6; the prototype reports + export flow.*

## 1. Locked decisions
- **LD-1** Four reports: **one authored** (`briefing`, editable) + **three generated** read-only (`readiness`/`assumptions`/`decision`); each generated report is a **projection of the committed read, producing NO new assessment**. *[RATIFIED]*
- **LD-2** Depth toggle (Summary⇄Full) on **`assumptions` + `decision` only**; Outcome Readiness + the authored briefing have no generated depth chip. *[RATIFIED]*
- **LD-3** Export is a **REAL flow, not a stub** — **supersedes capability #10's stale "stubbed toasts" wording** (which described the pre-2026-08-05 prototype the audit walked). Current: `openExport→_exportModalHTML→_doExport→_exportDoneHTML`. #10's "R2 must provide … real export (PDF/PM-tool)" stands; only the "stubbed" clause is retired. Guard `exportFlowReal`. *[RATIFIED — audit rec #2]*
- **LD-4** Three formats (`_EXPORT_FMTS`): **PDF package** (dated, D153 disclaimer cover), **Asana/PM-tool hand-off** (task·owner·dates·provenance), **Copy summary** (clipboard). *[RATIFIED]*
- **LD-5** Export runs **no new analysis**, but **reanalyzes first if pending** (`_exportGuard` forces one consolidated re-read when `_pendingCount()>0`). *[RATIFIED — cap #1]*
- **LD-6** **Optimized-for-outcomes scope is stated**; Free = primary only (`_exportScope.all = _TIER!=='free'`), multi-outcome routes to the Slice-4 gate; the modal names which outcome(s) it optimized for. *[RATIFIED — audit rec #3]*
- **LD-7** Export is **never maturity-gated; shows an honest readiness signal** (`_exportReady.min = min(via,grd,ada)`, `sound=mn>=2`); always allows export ("you can export now, but it firms as you confirm more"). *[RATIFIED — audit rec #4; "OSLO advises, you decide"]*
- **LD-8** Report scheduling: **automation Basic, share free; re-reads for currency before each send** (`toggleReportSchedule` gates on `_tierUnlocked('basic')`, free path `_scheduleSendNow`). *[RATIFIED — D172b]*
- **LD-9** **D153 advisory disclaimer on every package** (PDF cover, done-state, memo wrapper). *[RATIFIED — D153; audit rec #2]*

## 2. State Model
**Report (authored — Executive Briefing):** `compose → authored → sent` (`_reportStage`). `authored` = a living `contenteditable` draft (`_reportEdited`); `sent` freezes an immutable memo (`sendReportMemo`). Transitions: `genReportDraft`, `sendReportMemo`, `reportStartOver`, `regenReport`.
**Report (generated):** no lifecycle — computed live each render from the read (`renderOutcomeReadiness`/`renderAssumptionsEvidence`/`renderDecisionRecord`). Only client state = `_repDepth[k]∈{summary,full}` for the two depth reports.
**Export:** `requested (openExport) → [reanalyze-if-pending via _exportGuard] → rendered (_exportModalHTML: format/scope/readiness) → done (_doExport → _exportDoneHTML)`. `_export={fmt,done,via}`. From done: "Export another format" resets.
**Schedule:** boolean on/off + recipient (`_reportSched`). On Free, ON → pay gate; free path sends now.

## 3. Data / Object model
- **Report** `{id, kind:authored|generated, key, depth?:summary|full, stage?, draftHtml?, edited?, recipient:sponsor|team|board}`.
- **ReportSnapshot (immutable memo)** `{id, reportId, recipient, depth, at, sig:readSignature, bodyHtml}` — append-only (`_sentMemos`); `sig=grounded()+'-'+_settledN()+'-'+_CHKPTS`; a snapshot whose `sig` ≠ current read is flagged **stale / "Previous analysis"** at view time. Reuses R1 `ReportSnapshot`.
- **ExportPackage** `{id, format:pdf|asana|copy, scope:OptimizedForOutcomes, readiness:ReadinessSignal, disclaimer:AdvisoryDisclaimer(D153), planName, generatedAt, provenance}`.
  - **OptimizedForOutcomes** `{primary, others:n-1, all:bool, n}`; Free `all=false`, package states the primary + discloses declared-but-unoptimized outcomes with the upgrade path.
  - **ReadinessSignal** `{min:mn, band, sound:mn>=2, grounded, total, inferred}` — min of the three pillars.
  - **AdvisoryDisclaimer (D153)** — "a read of the plan's maturity, not a forecast of success, dated to the analysis behind it."
- **PM-tool hand-off mapping** (net-new, R2G6): the executable plan only — `{task, owner, dates, provenance}` per leaf (`exLeaves()`). No read/assessment content crosses.
- **Schedule** `{reportId, on, recipient, cadence:weekly, tier:basic}`.

## 4. Event Model
`report.generated` (`genReportDraft`/`regenReport` — no assessment) · `report.edited` (`_reportOnEdit` — author's voice only, never touches the read) · `report.sent → ReportSnapshot created` (`sendReportMemo` — immutable) · `export.requested` (`openExport`) · **`export.guard.reanalyze`** (if `_pendingCount()>0`, `_exportGuard` runs one consolidated re-read via the existing engine, cap #1 — the only place export touches analysis) · `export.rendered` (`_exportModalHTML`) · `export.done` (`_doExport` records History with format + optimized-for + band) · `schedule.toggled` (Basic-gated or free `_scheduleSendNow`) · **`schedule.send → currency re-read → deliver`** (each send re-reads before it goes, so a stale memo never ships).

## 5. Honesty invariants (testable)
1. **Generated reports produce no new assessment** — rendering reads current-state functions, never writes; no band changes on render (Decision Record: integrity "moves only at the next analysis update — never from the decision alone").
2. **Export runs no new analysis, but reanalyzes if pending** — `_pendingCount()===0` → zero recompute; pending → exactly one consolidated re-read first.
3. **Export never maturity-gated, always shows the readiness signal** — no path blocks on `mn`; at `mn=0` (Very Low) export still completes and shows the "◑ early" signal.
4. **D153 disclaimer on every package** — no export/memo render path omits it.
5. **PM-tool export pushes only the executable plan, with provenance** — the hand-off payload contains no assessment/read fields.
6. **Tailor the ask, never the read (D145)** — recipient variants change only the closing ask; assessment sections identical for every audience.
7. **A sent memo is immutable and stale-flagged** — `_sentMemos` append-only; a moved read flags "Previous analysis."

## 6. FE↔BE integration bindings
| FE surface | Handler | Backend binding |
|---|---|---|
| Report tabs (1 authored + 3 generated) | `REPORT_TABS`/`switchReport` | `GET /reports?planId`; generated = projection (no compute) |
| Depth toggle | `setRepDepth`/`_genDepthHTML` | client-side view param; no round-trip |
| Generate/author/edit briefing | `genReportDraft`/`_reportOnEdit`/`regenReport` | `POST /reports/{id}/draft` (model draft); PATCH body |
| Send memo | `sendReportMemo` | `POST /reports/{id}/snapshots` → immutable ReportSnapshot (R1) |
| Export format picker | `_EXPORT_FMTS`/`_setExpFmt` | `POST /exports {planId, format}` |
| Export optimized-for scope | `_exportScope` | entitlement check (`_TIER`); primary resolver; multi-outcome gate → Slice 4 |
| Export readiness signal | `_exportReady` | `min()` integrity model (#7) — no gate, disclose only |
| Export reanalyze-if-pending | `_exportGuard` | reanalysis engine (#1): consolidated batch re-read |
| Export render/done | `_exportModalHTML`/`_doExport`/`_exportDoneHTML` | artifact generation: PDF renderer (D153 cover); PM-tool connector; clipboard |
| PM-tool hand-off | Asana done-state, `exLeaves()` | **net-new** Asana/MS Project/Smartsheet connector (auth, mapping, direction, idempotency) |
| Schedule on/off | `toggleReportSchedule`/`_scheduleSendNow` | entitlement (Basic) + recurring job; per-send currency re-read |

## 7. R1 reuse vs net-new
**Reuse (§6):** `Report` + immutable `ReportSnapshot` (objects/endpoints/states/events); the one ratified export surface as a **projection** on #7/#2/#3 ("no new backend beyond #2/#3/#7"); the recompute/stale backbone for `_exportGuard` + per-send currency re-read.
**Net-new:** PM-tool connectors + mapping (R2G6 — Asana/MS Project/Smartsheet: auth, task·owner·dates·provenance, direction, idempotency); the D153 package cover; recipient-tailoring enum + auto-supersession (R2G11); generated-report export (previously inexportable).

## 8. Open items / placeholders
- **OI-1** which PM tools ship first — placeholder: Asana first (Maya's backlog), MS Project/Smartsheet fast-follow (Ron); owner confirms order.
- **OI-2** recipient-tailoring enum (`sponsor|team|board`) — author-with-placeholder; auto-supersession trigger deferred (R1 Open-Q7).
- **OI-3** report names (owner may rename before GA).
- **OI-4** readiness-signal threshold (`sound=mn>=2` is the proto cut; suggested-vs-required deferred per cap #1 §S).
- **OI-5** copy/clipboard payload serialization shape.

## 9. Acceptance criteria
1. **Four reports render** (1 authored editable + 3 generated read-only); each exportable (guard `reportsTabsGenerated`).
2. **A generated report never changes a band** — rendering performs no write and moves no band.
3. **Depth toggle** on Assumptions & Evidence + Decision Record only; Summary = shortlist, Full = complete register.
4. **Export with pending items reanalyzes first**; with none, zero analysis.
5. **Export not blocked by low maturity** — at `mn=0` export completes and shows min-of-three + "firms as you confirm more."
6. **Every PDF carries the D153 disclaimer** on the cover, dated to the analysis (guard checks "advisory disclaimer").
7. **A Free export states "optimized for [primary]"** and discloses unoptimized outcomes with the upgrade path; a paid export states "all N outcomes."
8. **PM-tool hand-off pushes only the executable plan** (task·owner·dates·provenance); no assessment/read content crosses.
9. **Sending a report freezes an immutable memo**, stale-flagged ("Previous analysis") when the read moves.
10. **Report scheduling** is Basic-gated with a free "send now"; every scheduled send re-reads for currency before delivery.

*Grounded in the prototype reports/export flow, capability #10 (reconciled per LD-3), the 2026-08-05 export objective audit (recs #1–5), and audit §4.6 (R2G6/R2G11) + §6.*

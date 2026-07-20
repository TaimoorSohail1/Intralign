# Slice 11 — Execution-Ready Planning & Export · Frontend / UI

Single openable HTML; dark default + light override on the same tokens (D015); WCAG 2.1 AA. No framework; plain JS + CSS variables. Colour discipline (D003): the task tree, critical path, and Full plan use **neutral / cool `--maturity`/`--cool` accents only** — no percentage-health fill, no RAG; **severity red/amber/green appears only on issue badges**. The `low confidence` grade and the critical-path accent are neutral epistemic/sequencing cues, never severity.

> NEW slice. The task tree renders inside the Work breakdown artifact (a Slice 5 surface — the generic editor chrome is documented there); Slice 11 adds the critical-path panel, the Full plan view, and the Asana export modal. The Asana connector is **simulated**.

## The authored task tree — inside `#artdoc` (Work breakdown document)

| Element | Selector / class | Notes |
|---|---|---|
| Intro | `<p data-epi="derived">` | "OSLO has decomposed the plan…" + `_epiTag('derived')`; names the `low confidence` grade |
| Table | `<table>` (Task · Owner) | **unchanged format** — all Slice 5 table machinery keeps working |
| Outline number | `.wbs-n` | `1 · 1.1 · 1.3.1` |
| Task text | `.wbs-t` + `data-lvl="0|1|2"` | indentation via `data-lvl` (an attribute, not a class); workstream headers also `.wbs-h` |
| Low-confidence grade | `.conf-low` (`contenteditable="false"`) | dashed/subtle neutral mark + confirm-first tooltip; on rows 1.2, 1.3.1, 1.3.2 |
| Issue anchors | `_a('ISS-11',…)` on 1.3.1 · `_a('ISS-10',…)` on 2.1 · `_a('ISS-05',…)` on the CFP owner cell | inline weak-span anchors |

Class-resolve clean (D195a): `.wbs-n`, `.wbs-t`, `.wbs-h`, `.conf-low` all carry CSS.

## The critical-path panel — `.cpath` (outside `#artdoc`)

Appended **after** the editable doc when `name === 'WBS'` (`openArtifact`) — furniture, never editable plan content (D160).

| Element | Selector / class | Notes |
|---|---|---|
| Panel | `.cpath` | surface-2 card, neutral chrome |
| Header | `.cp-h` + `.cp-epi` | "Sequencing & critical path" + a **From OSLO** chip |
| Sub-line | `.cp-sub` | "OSLO sequenced the tasks and inferred their durations…" |
| Chain | `.cp-chain` → `.cp-node` (`.cp-end` last) | each node = name + `.cp-dur` (`~N wk`; milestone shows "Sep 1"); `.cp-end` cool accent |
| Arrow | `.cp-arrow` (`→`, aria-hidden) | between nodes |
| Footer | `.cp-foot` | "~5 weeks of sequenced work feeds the fixed Sep 1 freeze… `low confidence`… confirm them to firm the path" + `.cp-link` to ISS-10 **when live** |

## The Full plan view — `#pane-fullplan`

Nav `#sbFullPlan` (`.sb-nav`, `⊞` icon, "Full plan", `onclick="showView('fullplan')"`); pane `<section class="pane" id="pane-fullplan"><div class="uc" id="fullPlanBody">`; breadcrumb "Full plan"; written by `renderFullPlan()`.

| Element | Selector / class | Notes |
|---|---|---|
| Head | `.fp-head` (`.fp-kicker` / `.fp-title` / `.fp-meta`) | "Full plan" · "*<Project>* — the whole plan, before export" · analysis state + date |
| Export button | `.fp-exp` | "Export to Asana ↗" → `openAsanaExport()` |
| **Readiness** | `.fp-sec` → `.fp-card.fp-ready` | section "Execution readiness" |
| State word | `.fp-state` | *Mostly OSLO's draft* / *Load-bearing confirmed* / *Fully validated* |
| Coverage | `.fp-cov` | "**N** of **M** … Confirmed by you · **K** still From OSLO" |
| Coverage bar | `.fp-bar` / `.fp-barfill` | `role="img"`, aria "N% confirmed by you"; **Confirmed-by-you coverage, never health** (D003) |
| Note | `.fp-note` | "…how much of the plan you have validated — not a prediction that it will succeed…" |
| **Consolidated plan** | `.fp-sec` → `.fp-card` | section "The plan — every workstream, consolidated" |
| Intro | `.fp-plan-intro` | every task From OSLO until confirmed; critical-path tasks marked |
| Header row | `.fp-plan-hd` | Task · Owner · Est. · sequence |
| Workstream label | `.fpt-ws` | group heading |
| Task row | `.fpt-row` (`.fpt-cp` on path) | `.fpt-n` number · `.fpt-name`+`data-lvl` (+`.conf-low`, +`.fpt-cptag` "critical path") · `.fpt-owner` · `.fpt-est` (+`.fpt-dep` "after 1.1") |
| **Critical path** | `.fp-sec` + `_wbsCriticalPathHTML()` | section "The sequence that drives the date" (reused panel) |
| **Confirm list** | `.fp-sec` → `.fp-card` → `.fp-conf-list` | section "Confirm before you hand it off"; severity-ordered |
| Confirm row | `.fp-conf-row` | `.fp-conf-sev` word · `.fp-conf-t` title + `.fp-conf-loc` · `.fp-conf-go` "Confirm →" → `openIssue` |
| Empty state | `.fp-kv` | "Nothing execution-critical is unconfirmed right now." |
| Foot | `.fp-foot` | "OSLO advises; you decide…" |

Class-resolve clean (D195a): `fp-*` / `fpt-*` classes carry CSS; `.conf-low` is global so it paints here and in the reused panel.

## The Asana export modal — `#asanaExportScrim`

| Element | Selector / id | Notes |
|---|---|---|
| Scrim | `#asanaExportScrim` (`.scrim`) | `onclick` closes on backdrop; `.show` toggled by `openAsanaExport`/`closeAsanaExport` |
| Modal | `.wmodal` | `role="dialog"`, `aria-modal="true"`, `aria-labelledby="asanaExportTitle"`, `max-width:760px`; registered opaque in `_DIALOG_PANELS` (D195a) |
| Header | `.wm-h` (`#asanaExportTitle` "Export to Asana" + `.wm-sub`) + `.wm-x` close | "The executable plan, mapped to Asana — a preview before you send." |
| Body | `.wm-b` `#asanaExportBody` | written by `renderAsanaExport()` |
| Boundary banner | `.ax-boundary` | "OSLO sends the executable plan. Its intelligence… stays in OSLO…" |
| Map legend | `.ax-legend` → `.ax-map` (`.ax-arrow`) | Task→Asana task · Owner→Assignee · Duration→Due · Depends→Dependency · Provenance→**OSLO Provenance** field · OSLO task id→**OSLO Task ID** field |
| Mapping table | `.ax-tbl` (`.ax-hd` / `.ax-row`) | columns `.ax-c-name` (+`.ax-dep` "after …") · `.ax-c-asg` · `.ax-c-due` · `.ax-c-prov` (`.ax-pv`, `.ax-pv-low` tint) — 14 rows |
| Free-tier note | `.ax-free` (`.wm-note`) | custom fields need Premium; free-tier → provenance as a **tag** (degraded for monitoring) |
| Readiness line | `.ax-ready` | "N of M Confirmed by you; the rest cross flagged From OSLO. You can export now — nothing is blocked." |
| Footer | `.wm-f` | "Simulated hand-off. Runs no analysis; OSLO keeps the plan of record." + Cancel + `.ax-send` "Export to Asana" → `doAsanaExport()` |

Class-resolve clean (D195a): `ax-*` classes carry CSS.

## Color discipline (D003)

The task tree, critical path, Full plan, and export use the **neutral / cool** palette — no percentage-health fill, no RAG, no completion bar. The critical-path accent (`.cp-end`, `.fpt-cp`) is a cool sequencing cue; the `low confidence` grade is a dashed neutral epistemic mark; the readiness bar (`.fp-barfill`) is a **Confirmed-by-you coverage** read, not health. Severity red/amber/green stays on issue badges only (ISS-10/11 in the confirm list show a severity word, `_sevword`).

## Accessibility

- Full plan nav item, export buttons, Confirm links, and issue anchors: keyboard-operable (`role="button"`, `tabindex="0"` on the routing links).
- Coverage bar: `role="img"` with a percentage aria-label.
- Asana modal: `role="dialog"`, `aria-modal`, labelled title, Esc/backdrop/✕ close; opaque panel verified (D195a).
- Critical-path arrows are `aria-hidden`; the chain reads as text. Focus-visible rings and reduced-motion inherited; colour is never the sole signal (provenance and grades are words).

## App shell (inherited)

The left sidebar carries the eighth item **Full plan (⊞)** alongside Overview · Issues · History · Inference map · Reports · Documents. `showView('fullplan')` toggles `#pane-fullplan.active`, syncs the nav (`#sbFullPlan aria-current`) and breadcrumb, and calls `renderFullPlan()` on entry.
</content>

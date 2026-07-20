# Slice 6 — Issues & Recommendations (Panel Model) · Product Data

Client-side prototype only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no API, no real AI.** "Persistence" below means browser localStorage; real-store tech is owner-TBD and out of scope. These are the **product entities, visible fields, and prototype-local data concepts** the issue engine reads — not a schema.

> Regenerated to the frozen build. The retired **"Acknowledge"** lifecycle value and any hand-`resolved` writer are **gone**. The separate "Attention map" nav row is retired into the Map ⇄ List view state (DL-136).

---

## Issue (the engine's unit) — `ISSUES` + `_istatus`

Internal object = **Finding**; user-facing label = **Issues** (D017). The static model is `ISSUES` (ISS-01…09 base + deep); mutable per-issue status is a separate map `_istatus` (kept apart so the model object stays clean).

| Field | Values | Notes |
|---|---|---|
| `title` | string | The user-facing issue title. |
| `sev` | `critical · moderate · warning` | Severity. **Severity colour only on issues** (D003); `_sevrank`/`_SEVORDER` order it. |
| `dim` | `Clarity · Alignment · Feasibility` | Primary CAF dimension (scalar, back-compat). |
| `dims` | array of dimensions | Multi-dimensional findings (CAF §8.3); `_dimsOf` reads it — the issue appears under **each** dimension. |
| `sec` | one of the 7 documents (`Intent · Context · Scope · Requirements · WBS · Schedule · Resources`) | Where the issue lives; the panel's Artifact link. |
| `status` (→ `_istatus[id]`) | `open · addressed · resolved` (`_LIFE`) | Lifecycle. **No `acknowledged`** (D094). `_active(id)` = not resolved. |
| `rectype` / `ftype` | e.g. `validation·definition·planning·alignment` / `Assumption·Coverage Gap·Missing Information·Ambiguity·Conflict` | Finding taxonomy; `ftype` drives the CAF drill's Level-2 finding-type cut (`_FTYPE_ORDER`). |
| `why` | string | "Why this matters" — the plain-language read. |
| `ev` | `[[document, quote], …]` | Cited evidence (the Evidence row). |
| `caf` | string | "`<dimension>` impact" — what it weakens. |
| `rec` | string | OSLO's own recommendation — the one the assisted apply can DRAFT (`apply:true`). |
| `paths` | array of strings | Alternative **options** the user selects and writes themselves (D089). User-facing term is **option**, never "path" (D190b). |
| `clar` | `{q, hint}` (optional) | A clarification request tied to the issue (D090). Present ⇒ the panel offers **Answer**; absent ⇒ the panel offers **Apply this fix**. |

- **Lifecycle is `open → addressed → resolved`** and **reversible** (D192b): a selection clears, a fix/answer is withdrawn, and an analysis update re-opens. **Only an analysis update writes `resolved`** (D088).

## Per-issue decision state (D191/D089)

| Map | Meaning |
|---|---|
| `_selpath[id]` | the selected option: `'rec'` (OSLO Recommended = Confirmed by you) or `'p'+index`. Internal key stays `paths[]`; the product speaks "option" (D183e). |
| `_decision[id]` | `{kind:'selection'\|'fix'\|'answer', key, art, verBefore, verAfter, bodyBefore, bodyAfter, basisBefore, relBefore, attestBefore, metered, evId}` — the record of what the user did and everything it changed, **captured before it changed it**. **Deliberately carries NO band, NO CAF width, NO confidence** — the mechanism behind "no hand-path moves the read." |
| `_clarAnswered[id]` | a question the user has answered is countable state — written only by the one clarification door. |
| `_wdConfirm[id]` | the on-screen consent step (D184: no irreversible-feeling act without its subject). |

## Attestation refcount (D193b) — computed, never a boolean

| Map | Meaning |
|---|---|
| `_attestBy[art]` | list of decision keys attesting the document — the **refcount** (`_attestedBy(art).length > 0` ⇔ attested). Two decisions can attest one document. |
| `_ATTEST_BASE[art]` | the document's basis + Reliability **before the first standing decision** attested it — captured at the 0→1 edge, restored at the 1→0 edge (`_assertAttestationIsRefcountedByDecision`). |

`applyFix` and `_submitClarification` mark `PLAN_SECTIONS[].basis='attested'` and raise `.rel` (Low→Moderate→High); withdrawing drops that decision's share and restores Reliability to the pre-first-attestation value when the last share goes.

## Lifecycle transition table (D191 §7a) — enumerated, not remembered

`_ISSUE_TRANSITIONS` declares every writer of `addressed`/`attested` with its inverse:

| by | into | attests | kind | inverse |
|---|---|---|---|---|
| `selectPath` | addressed | no | selection | `clearSelection` |
| `applyFix` | addressed · attested | yes | fix | `withdrawDecision` |
| `_submitClarification` | addressed · attested | yes | answer | `withdrawDecision` |

`_assertEveryDecisionTransitionHasAnInverse` sweeps the product and fails the build on any un-inverted writer. Named probe helpers (`_ATTEST_PROBE_HELPERS`) are the only exemption.

## List filter + group state (D086)

| Concept | Values | Notes |
|---|---|---|
| `_filt` | `{art, dim, sev, status}` | Document · Dimension · Severity · Status (`active·resolved·all`, `_statusMatch`). `clearFilt` resets art/dim/sev. |
| `_group` | `dim · sev · art` | By dimension (default) · By severity · By document. |
| `_issuesState` | `ready · analyzing · unavailable` | drives the not-yet-analyzed / unavailable empty states (D091). |
| order keys | `_DIMORDER` (Feasibility·Clarity·Alignment) · `_SEVORDER` · `_ISSARTORDER` | fixed display order. |

## Map ⇄ List view state (DL-136)

| Concept | Values | Notes |
|---|---|---|
| `_iaView` | `map` (default) · `list` | last-seen view of the combined Issues destination; set by `showView` (`attention`→map, `issues`→list). `showIssuesView` re-enters the last view. |
| crumb | "Issues · Map" / "Issues · List" | `_viewLabel`. |
| `_scrollMem` | per-pane scroll offsets | restored on return. |

## CAF drivers (Option C · DL-116) — computed, never typed

`_ciDimDrivers(dim)` returns `{grounded, inferred, total, issues, bySeverity, byFtype, lift}` — every number a WHERE clause over live `_istatus` + `_ciDimInferenceStats`. `_evWord` gives the provenance cue; `_cafLiftText` reuses the top open issue's own `rec`. **The band is a band; only drivers are quantified.**

## Alignment evidence (D133) — live CAF input

| Concept | Values | Notes |
|---|---|---|
| `ALIGN_EVIDENCE` | `[{rid, issueId, by, kind:'approve'\|'reject'}]` | attested stakeholder inputs; both kinds are Alignment evidence. |
| `ALIGN_STEP` | `8` (symmetric) | the **same** step for Approve (+) and Reject (−) — never split. Clamped `ALIGN_MIN…ALIGN_MAX`. |
| `READ[*].alignW / alignLvl` | width → band (`_cafLevelFor`) | Alignment is a live dimension like Feasibility; moved by `_reviewAnalysisRun`, symmetrically. A review **never** resolves/re-opens/invalidates the tied issue. |

## Deep (task-altitude) findings — `DEEP_FINDINGS` → `_deepPassSurfaceFindings()`

Not in `ISSUES`/`_istatus` at boot; surfaced by the one idempotent door (returns the ids it added), then ordinary issues.

| id | fields | note |
|---|---|---|
| ISS-07 | critical · Feasibility+Alignment · Schedule; has `clar`, `draft` | sponsor funding closes after costs committed. |
| ISS-08 | moderate · Clarity+Alignment · Scope | recording resourced but never scoped. |
| ISS-09 | moderate · Alignment · Scope | intended outcomes have no scoped activity. |
| **ISS-10** | moderate · Feasibility · **WBS**; `rec` + 2 `paths` (no `clar`) | **task-altitude** (DL-145 2B): the freeze rests on undated tasks. |
| **ISS-11** | moderate · Clarity · **WBS**; `rec` + 2 `paths` (no `clar`) | **task-altitude**: part of the breakdown is OSLO's low-confidence inference — honest self-read, never a warning (DL-109). |

ISS-10/11 raise **WBS open count 1 → 3** (ISS-05 was the only prior WBS issue). The **analysis that produces them is Slice 11's**; this engine only carries them. Supporting context items `CI-71/72/73` (`hz:'deep'`) tie to ISS-10/11.

## Plan documents ×7 (INHERITED, D035) — `PLAN_SECTIONS`

Intent · Context · Scope · Requirements · Work breakdown (WBS) · Schedule · Resources. Each carries `basis` (`derived`/`attested`) and `rel` (Reliability). An applied fix / answered clarification flips the tied document to `attested` and raises `rel`; withdrawing restores it (refcounted).

## localStorage keys (browser-local persistence)

- Per-artifact body + version (`_artKey`, `-ver`) — read by `_docTouchedSince` to decide whether a withdraw may restore.
- CAF drill open/L2 state persisted on container classes (survives refresh).
- Inherited Slice 1–5 keys (phase, orientation/tour-seen, account, artifact autosave). `_issuesState` preview toggles and `_iaView` are ephemeral/UI state.

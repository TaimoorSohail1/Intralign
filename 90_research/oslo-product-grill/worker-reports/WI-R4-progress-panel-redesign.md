# WI-R4 — Progress panel redesign — WORKER REPORT (STOPPED: hard conflict)

**Status:** ⛔ **STOPPED — did not patch the prototype.** The owner-approved LOCK redesign hard-conflicts with the current state of the slice-10 device file. Reconciling would require fabricating the panel's headline numbers, which the task forbids ("do NOT hardcode") and which violates OSLO's central anti-fabrication canon. Details, evidence, and 3 reconciliation options below.

**Worker:** WI-R4 · **Date:** 2026-07-14
**Target:** `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` (device; 2.62 MB, mtime 1784002109508)
**Reference (unmodified):** `progress_panel_LOCK.html` (device)

---

## 1. What the brief expected vs. what the file contains

The WI-R4 brief describes the panel as built by **`renderProgress()`** (~line 11085), with design commentary at **lines 1040–1240** ("GROUNDED is the star", "a sentence with a bar", "epistemic-class name is a LABEL in the GROUNDED row", "YOUR READ RESTS ON" chip history), and data hooks for **attested / derived / inferred / grounded counts, questions, resolved/answered, per-metric deltas**.

**None of that is in the current device file.** A concurrent process has rewritten it (the brief warned this could happen). Verified by direct search of the staged device copy:

| Brief expectation | Reality in current file |
|---|---|
| `renderProgress()` (~11085) | **absent** — 0 matches. Line 11085 is reviewer-view code (`rvvConvert`). |
| Commentary 1040–1240 "GROUNDED is the star" | **absent** — lines 1040–1240 are the doc-editor CSS (D082–D084). 0 matches for "GROUNDED is the star", "grounded facts", "YOUR READ RESTS ON". |
| "grounded facts" / "Inferences" strings | **absent** — 0 matches each. |
| attested/derived/**inferred** FACT counts | **absent** — no fact-level ledger exists. |
| questions / answered counts | **absent** — no `openQuestions`/`answered` count hook. |
| per-metric deltas "since last update" | **absent** — only a single `run.delta = {opened:6}` on the Initial run (line 4114). |

## 2. The panel that actually exists (the real "already-ratified" panel)

The live Overview Progress panel is a static `.card` / `.prog-grid` at **prototype.html lines 2849–2862**, populated by **`updateIssueCounts()` (lines 8626–8657)**. It is the **canonical v4 issues-ledger** (per **D047**, prototype ~line 9105: *"the Progress ledger no longer carries a state line (matches canonical v4 renderLedger)"*):

- Hero number = **issues resolved** · `{open}` open · view→  (id `pg-resolved`/`pg-open`)
- **critical issues open** (id `pg-crit`, `.danger` only when >0 — severity-only-on-critical already holds)
- Bar: **Dependencies confirmed** `X / 3` (id `pg-deps`)
- Bar: **Plan artifacts read** `7 / 7` (id `pg-sections`)

This is a **work-progress** ledger. The LOCK is an **epistemic grounded-facts** ledger. They are two different data objects, not two skins of the same data.

## 3. Why this is a hard conflict (not a compatible evolution)

The owner may of course approve a new *look* — that authority is not in question. The blocker is the **mandatory, twice-stated requirement to wire it to real data** ("pull the real counts/deltas from the existing data hooks; do NOT hardcode"), which is **impossible** here:

- **Hero (grounded = attested + derived facts):** no fact-level provenance counts exist. The only epistemic data is the **7 PlanSections** (lines 4034–4042, **D035**), all `basis:'derived'`, **zero attested at boot**. That is per-*artifact*, not per-*fact*, and it is 7 artifacts — not "17 confirmed / 12 from OSLO / 29 grounded facts."
- **Foundation bar — inferred segment ("Inferences · provisional", the set-apart hatched element that is the heart of the LOCK):** **no data source of any kind.** There is no inference count anywhere in the file.
- **Attested "Confirmed by you" segment:** would render at **0 / zero-width** at boot (no confirmed artifacts yet).
- **OPEN · Questions** and **CLOSED · Answered:** no question/answered counts; at most a single clarification exists.

So a "real-data" wiring yields: hero **7** (mislabeling 7 plan artifacts as "grounded facts your read is built on"), a full-width gray "From OSLO 7" bar, **no** attested segment, **no** inferred segment, Questions **0**, Closed **0/0**. That is a semantically wrong, mostly-empty rendering of the LOCK — exactly the "broken output" the brief says not to write back.

The only way to make the panel *look* like the LOCK screenshot (17/12/20/8/2/3/0/0) is to **hardcode those numbers** — which:
- violates the brief's explicit **"do NOT hardcode"**, and
- violates OSLO's core canon — **D001** (advisory/never-fabricated), the `_assertNoFabricatedNumbers` discipline (line 14045), and the product thesis that *"the one number the whole product rests on"* is never invented (lines 11390, 12483, 14806).

**Cited signed-off decisions in conflict:** **D047** (ratified v4 issues-ledger is the current Progress panel), **D035** (epistemic data is per-artifact `basis`, not a fact ledger), **D001 / anti-fabrication canon** (numbers must trace to real state). The LOCK's data model (grounded/derived/**inferred** FACT counts + questions/answered + per-metric deltas) is **not implemented in this prototype**, and WI-R4 was not scoped to build it.

## 4. Boot self-check — baseline (file UNCHANGED by me)

Headless Chromium (playwright), `file://` load of the current device file:

```
guards total : 58
failing      : 0
reportsNoHealth : true  ✅
pageerrors   : 0
```

The file boots clean. I made **no edits**, so before == after. (Side note: 58 guards, not the ~87 the brief cites — consistent with the file having drifted.)

## 5. What I did NOT do (and why)

- **Did not patch `prototype.html`.** Writing a fabricated or half-empty panel into a live, guard-protected, concurrently-edited 2.6 MB file would be reckless and dishonest.
- **Did not append a "Progress panel redesign (WI-R4)" section to the 5 slice-10 docs.** There is no ratified, wired redesign to document; recording one as done would be false. This step is deferred pending owner disposition (Section 6).
- Did not touch v5 or the LOCK reference.

## 6. Reconciliation options (owner decision required)

**A — Recommended: scope a data WI first, then wire.** Before the LOCK can be honest, the prototype needs a real epistemic **fact ledger**: per-fact attested/derived provenance counts, an **inferences** ledger, a questions(clarifications)/answered ledger, and per-metric "since last analysis update" deltas — plus guard(s) to keep them honest. Then WI-R4 wires the LOCK to those hooks unchanged. Preserves both the owner's design *and* the anti-fabrication canon. (Also re-baseline WI-R4 against the current file — its line refs and `renderProgress` assumption are stale.)

**B — Re-map the LOCK look onto the data that EXISTS (needs owner sign-off, changes semantics).** Keep the LOCK's *treatment* (display hero + `--primary` underline, proportional foundation bar, OPEN/CLOSED work stats, neutral solidity ramp, severity-only-on-Critical) but re-point the numbers to the ratified v4 ledger's real quantities (issues resolved/open/critical, Dependencies-confirmed and Plan-artifacts-read ratios, clarifications as Questions). Ships a real data-driven panel now — **but it changes what the hero MEANS** (it would no longer be "grounded facts"), so it contradicts the LOCK spec's caption/semantics and must be owner-approved, not chosen by a worker.

**C — Ship the LOCK as a static, clearly-labelled DESIGN PREVIEW only** (not in the live product path, guard-inert) to lock the visual, with wiring deferred to Option A. Satisfies "reproduce the look" but not "wired to real data" — owner decides if that interim is acceptable.

## 7. Residue / notes

- Guardrails that would have held either way: severity red already appears only on Critical (`pg-crit.danger`); the current bars use neutral tint (no RAG); `reportsNoHealth` scans REPORT_SURFACES only (line 14397), not the Overview — so the panel swap would not have tripped it.
- The brief's demo values (17/12/20/8/2/3/0/0) exactly equal the LOCK screenshot; the current file's real values are open issues **6**, critical **1**, resolved **0**, plan artifacts **7/7** — further evidence the LOCK numbers are illustrative, not drawn from slice-10 state.

---

## ADDENDUM — 2026-07-14 (session correction + COMPLETION)

**The STOP above was based on a STALE mount snapshot, and its conclusion does not hold for the live file.**

`device_stage_files` served a **1.59 MB** older revision of `prototype.html` (no `renderProgress`, no `_progressHTML`, `updateIssueCounts`-only, 58 guards). The **live device file is 2,623,666 bytes** and *does* contain the full epistemic Progress panel — verified by direct `grep` on disk: `function renderProgress` ×1, `_progressHTML` ×56, `_progressRows` ×36, `_infMapHTML` ×9, `epiClassName` ×22, `_assertNoPercentageFillOnMaturitySurfaces` ×6, `_s10SelfCheck` ×6. The registry (`PAYOFF_COUNTS`) already computes every number the LOCK wants: grounded / inferred claims, load-bearing, issues / critical / open-questions, resolved / answered. **No fabrication was required and none was done.**

**What was actually shipped (CSS-only, guard-safe):** a hero-scale typographic enhancement of the existing canon-legal panel — the counts made **bigger, more vivid, more pronounced** in the owner's LOCK language, using **weight in TYPE ONLY** (D180 / DL-109). Inserted as one `WI-R4 START … END` block keyed to `.pg-go:hover`. New size **2,625,411 bytes** (+1,745).

**What was deliberately NOT wired, and why (canon):**
- The LOCK's **proportional foundation bar** is a fill / proportion-of-a-total — forbidden by **D176 / D194c** ("never a fill, never a proportion of a total"; "a bar that fills is a burndown with better manners"). The grounded-vs-inferred proportion lives canon-legally as **countable pips** on the Inference Map ("See them →").
- The LOCK's **red-on-Critical** is forbidden by **D187** (`_assertTrendColourIsEarnedOnly` flags any red / `--danger` / `--success` on a progress-or-trend rule). Critical gets **weight, not colour**.

**Verification:** headless Chromium (Playwright), `file://` load of the live file → `window._S10` = **137 / 137 guards pass, 0 failing** (incl. `noBurndownGrammar`, `trendColourEarned`, `cafNoPercentageFill`, `noDebtFrame`); **0 pageerrors**; panel renders real computed counts (From OSLO 11 · Confirmed by you 17 · Load-bearing 12 · Issues 6 · Critical 1 · Open questions 2 · resolved 0 · answered 0) in both dark and light.

**Owner fork still open (unchanged by this work):** if the literal continuous **fill bar** and/or **red-on-Critical** are wanted, they require a **Framework 001 amendment to D176 / D194c / D187** (owner-ratified) — not a worker edit. Otherwise this hero-typography treatment stands.

**Status:** ✅ COMPLETE (canon-legal adaptation). Pre-edit backup preserved at `slice-10-tiering-limits/_to_delete/prototype.prewi_r4.bak`.

---

## ADDENDUM 2 — 2026-07-14 — OWNER OVERRIDE: LITERAL LOCK IMPLEMENTED

Owner directed **"I want the original image I provided implemented."** The canon-legal typographic version (Addendum 1) is **superseded**. The Progress panel now renders the **literal LOCK foundation-bar**: 28-hero grounded facts (17 Confirmed by you + 11 From OSLO, computed), proportional attested/derived bar, set-apart "12 Inferences · provisional" tail, legend, and OPEN/CLOSED stats with **red on Critical** — all wired to real `_progressRows()` counts (no hard-coding).

Because this reverses ratified doctrine (D176/D194c/D187/D179d/DL-109/D194d/D197/D186 for this panel), the change is routed through a **Framework 001 amendment** (`DL-PENDING-progress-panel-foundation-bar-BODY.md`, owner ratification owed). Ten guards that police the superseded rules are **SUSPENDED behind `_PGX_AMEND`, each logging a named `⚠️ PGX` warning at boot** (never silent); a new positive guard `_assertPgxBarIsComputedFromRealCounts()` protects what still matters (computed counts, single-sourced labels, CLOSED-never-a-target).

**Verification:** `window._S10` = **138/138 pass, 0 failing**; **0 pageerrors**; dark + light render the bar proportional to real counts. Backups: pre-WI-R4 original and the WI-R4-typography interim are both in `slice-10-tiering-limits/_to_delete/`.

**On ratification:** rewrite the ten suspended guards to the new doctrine (red-only-on-Critical; grounding-rises proven against the bar segments; third-party attestation → a third solid segment) and remove `_PGX_AMEND`.

---

## ADDENDUM 3 — 2026-07-14 — RECONCILED VARIANT SHIPPED

Harmony review of the Overview found the literal bar fought the Outcome Confidence panel (two quantity-grammars; inverted hierarchy; orange-on-state; deficit-toned tail). Owner selected the **reconciled** variant, now live: calmer 28-hero (no orange underline), bar recoloured to surface tones with a **cool accent on "Confirmed by you"** echoing the Confidence ramp, **neutral deltas**, **red kept only on Critical**, and a **de-exiled tail** ("inferences your read leans on"). Bar, proportions, real counts preserved. Live: **138/138 self-check, 0 pageerrors**, dark + light. Amendment (`DL-PENDING-progress-panel-foundation-bar-BODY.md`) revised — the reversal is now narrower (colour-on-state and the DL-109 debt-frame are back in canon; only the bar geometry, merged rows, and red-on-Critical remain to ratify). Backups in `slice-10-tiering-limits/_to_delete/` (pre-WI-R4 original, WI-R4 typography, literal-LOCK).

---

## ADDENDUM 4 — 2026-07-14 — RATIFIED · GUARDS RE-BASED

Owner ratified the amendment. The suspension scaffold (`_PGX_AMEND` / `_pgxAmended`) is **removed**; the ten guards run live and enforce the reconciled doctrine:
- **Adapted (rule still holds):** payoff-counts-computed (the grounded-facts hero is the computed sum of two real counts), closed-is-never-a-target, grounding-rises-while-issues-rise, rising-inference-is-not-a-regression, no-"holding-it" (the load-bearing count survives with its noun in the tail). Compat hooks: deltas carry `.pg-d`; number+delta share one `data-count-key` host; work groups carry `data-row`.
- **Replaced:** the earned-only/no-red colour guard → `_assertPgxColourDiscipline()` (severity red scoped to `.pgx-ws.crit`; `--success`/orange forbidden on panel state).
- **Added:** `_assertPgxBarStructure()` (single-sourced class labels; the inference tail keeps its count+noun; hero present), alongside `_assertPgxBarIsComputedFromRealCounts()`.
- **Retired as superseded (tracked):** D194a no-double-say, D197 load-bearing-is-the-name, D194c third-class-map, D194d distinct-rows — one-home/count-survival covered by `_assertNoCountIsRenderedTwice()` + the two PGX guards. Third-party attestation as a third bar segment is the one deferred follow-up.

Live self-check: **135/135 pass, 0 pageerrors**, both themes (count 138→135 as three ledger guards retired). Reconciled(suspended) interim backed up in `_to_delete/`.

# Slice 11 — Execution-Ready Planning & Export · User Experience

**Release:** OSLO R1 (ALPHA). **Slice:** 11 — Execution-Ready Planning & Export.
**Baseline of record:** frozen prototype (md5 `a327d702`, boot 157/157).
**Boundary:** advisory-only (D001); Outcome Confidence = understanding maturity, neutral, never health/readiness/probability (D002/D003/D183b); severity colour only on issues (D003); dark default + WCAG 2.1 AA (D015). Client-side prototype only (D016) — fake data, simulated AI, simulated Asana connector, `localStorage`.

> This is a **NEW slice** (no prior baseline). It documents the execution-ready planning direction ratified by **DL-145** and built by **DL-146 → DL-151**, all frozen in `a327d702`. It notes what is **INHERITED** from earlier slices (the artifact editor, the issue engine, the reader-export, History) and what is **NEW in Slice 11**.

---

## What Slice 11 is

Slice 11 is the beat where OSLO stops being only a reader of the plan and becomes the **author and certifier of an execution-ready plan** — one detailed and exact enough to export into an execution tool and run (DL-145). It is the answer to "OSLO understands my plan; now hand me something I can execute."

OSLO **both authors and certifies** (DL-145 §2): where the user gave no execution-level detail, OSLO **infers** the decomposition; where the user gave partial detail, OSLO **uses it and infers the gaps**. In both cases **every inferred element is marked From OSLO and awaits the user's validation** (D011/D069, DL-109). Authoring never breaks "computed, then marked, never invented" (D173): OSLO may infer *plan structure*, but it never presents inference as fact.

Slice 11 adds **four surfaces**, all built on machinery that already exists:

1. **The authored, graded task tree** — the Work breakdown document, decomposed to task/subtask altitude (DL-146).
2. **Task-altitude assessment** — two new task-level issues on the deeper read (DL-147).
3. **Sequencing + the computed critical path** — a From-OSLO analysis panel in the Work breakdown view (DL-148).
4. **The eighth "Full plan" consolidated view** — the pre-export surface (DL-149/150) — leading to **the structured Asana export** (DL-151).

The single most important invariant of the slice: **the plan crosses the export handoff; OSLO's analysis stays in OSLO** (DL-151, `_assertExportSendsPlanNotAnalysis`).

---

## INHERITED (unchanged, cross-referenced)

- **The Work breakdown artifact + editor** (Slice 5) — the task tree renders *inside* the Work breakdown document (`#artdoc`), and confirming a row reuses the existing table-provenance/attestation engine (`_seedTableProvenance`, per-cell hover chips, row/column ops, autosave, version bumps). Slice 11 owns the *execution-planning semantics*; the generic artifact-editing mechanics belong to Slice 5 (see there).
- **The issue engine** (Slices 2/4) — the two new task-altitude findings (ISS-10/ISS-11) are ordinary issues: dimension, severity, citations, recommendation, resolution paths, Attention-map/Jump-to-issue/CAF wiring, and `_submitClarification`/analysis-update routing.
- **The reader-export + share** (Slice 9) — the generic frozen human-readable snapshot and the share/invite flow stay in Slice 9. The Asana execution-export is a **distinct object** (D107) — note the distinction; it is not the same as the reader-export.
- **History** (Slice 8) — the Asana export appends a hand-off record to History.
- **The Outcome Confidence read** (Slice 3) — untouched; a deeper, still-inferred plan is not a more mature one (completeness ≠ readiness, DL-145 §3).

---

## NEW in Slice 11 — surface by surface

### 1. The authored, graded task tree (DL-146)

The Work breakdown is no longer a flat five-row deliverable table. OSLO has decomposed the plan into **workstreams → tasks → subtasks**, outline-numbered (`1 · 1.1 · 1.3.1`) with indentation showing the hierarchy. An intro line states plainly: *OSLO decomposed the plan to the task level needed to execute and export; where your inputs didn't specify a task, OSLO inferred it — so every row is From OSLO until you confirm it.*

- **Everything is From OSLO until confirmed.** Every row is marked *From OSLO* by the existing provenance engine; the user confirms a row the same way they always have — by editing/accepting the cell, which flips it to **Confirmed by you**. **No new validation path was built** (DL-145 §3).
- **Graded inference.** The thinnest, most speculative inferences carry a neutral **`low confidence`** grade (e.g. *Confirm 500-person Wi-Fi capacity*, *Map AV power drops*, *Lay out badging & check-in stations*) — a louder prompt to confirm those first. The grade is **epistemic, never a severity colour** (D003) — low confidence names the evidence, not a defect in the plan.

### 2. Task-altitude assessment (DL-147)

Now that the plan is decomposed, OSLO can find gaps that were invisible at deliverable altitude. Two findings surface on the **deeper read** (the Extended pass), through the **same issue engine** as every other issue:

- **ISS-10 — *The freeze rests on undated tasks*** (Feasibility · Work breakdown). The Sep 1 run-of-show freeze depends on *Close the CFP* and *Select the program*, and the breakdown dates neither — so OSLO can't confirm the upstream work fits. Anchored on task **2.1 (Close the CFP)**.
- **ISS-11 — *Part of the breakdown is inferred*** (Clarity · Work breakdown). OSLO's honest read on **its own low-confidence decomposition**: three tasks are its inferences, so the plan's completeness rests partly on OSLO's read of the work. Named as **evidence honesty, never a warning about the plan** (DL-109). Anchored on task **1.3.1 (Map AV power drops)**.

Both raise the Work breakdown's open-issue count (1 → 3 after the deeper read) and light the CAF, Attention map, and issue panel like any other issue.

### 3. Sequencing + the computed critical path (DL-148)

OSLO **sequences** the plan: it models task dependencies and inferred durations, and **computes the critical path** — the longest dependency chain that decides the earliest the Sep 1 freeze can be met.

- It renders as a **"Sequencing & critical path"** panel in the Work breakdown view, marked *From OSLO*, durations *low confidence*, linked to ISS-10 when that finding is live.
- For the DevNorth sample it computes **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show (~5 weeks)** into the fixed **Sep 1** freeze.
- It is **computed, not authored** (D173): change an edge or a duration and the path moves (`_assertCriticalPathComputed`).
- It is **feasibility analysis on OSLO's side of the handoff** — OSLO analysing the plan's sequence, not tracking execution — and renders **outside the editable document** (`#artdoc`), so it never becomes editable plan content.

### 4. The eighth "Full plan" consolidated view (DL-149/150)

The seven documents stay focused per-slice surfaces; the **eighth view — "Full plan" (⊞ in the left nav) — is the whole sequenced plan in one place**, the **pre-export surface**. Read-only with confirm routing, re-rendered live on entry. It renders, all computed:

- **(a) Execution readiness** (`_execReadiness`) — the **provenance coverage of the execution-critical set** (Work breakdown · Schedule · Resources statements): how many are **Confirmed by you** vs still **From OSLO**, surfaced as a **named validation-progress state**: *Mostly OSLO's draft → Load-bearing confirmed → Fully validated*. It describes **what you have validated, never a "will-succeed" verdict**; it is **non-blocking**; and its coverage bar is a **Confirmed-by-you read, never a health bar** (D003).
- **(b) The consolidated plan itself** — all 14 tasks × 5 workstreams from `WBS_TASKS`, each with owner · inferred duration · dependency · critical-path mark · low-confidence grade. Every task is From OSLO until confirmed.
- **(c) The sequence that drives the date** — the computed critical path from (3), reused verbatim.
- **(d) Confirm before you hand it off** — the open execution issues, severity-ordered, each routing to the existing confirm surface (validation, not a shadow path — D088).
- **(e) *Export to Asana ↗*** — opens the structured export.

### 5. The structured Asana export (DL-151)

*Export to Asana* opens a **mapping preview** (`#asanaExportScrim`) — what will land, before it sends — then a **simulated hand-off** with a History record. The connector is **simulated in the prototype (no live Asana API)**.

- **Only the executable plan crosses:** tasks/subtasks → Asana tasks · owners → assignees · durations/dates → due dates · dependencies → dependencies.
- **OSLO's analysis does NOT cross** — the critical path, the issues, the maturity read stay in OSLO, live. The preview opens with a plain statement of this boundary. `_assertExportSendsPlanNotAnalysis` enforces an allowlist (`id · name · assignee · due · deps · prov`); any analysis field fails the build.
- **Provenance rides as a native field** — an **OSLO Provenance** custom field (*Confirmed by you / From OSLO / From OSLO · low confidence*), an OSLO-owned read-only honesty signal — **plus an OSLO Task ID** custom field, the stable anchor a future execution-monitoring phase would need to reconcile Asana's state back to OSLO's plan of record.
- **Tag fallback** covers free-tier Asana (custom fields require Premium) — enough for the honesty signal, a degraded mode for monitoring.
- **Non-blocking** (DL-145 §4): export is always available; the preview states how many statements are Confirmed by you vs cross flagged From OSLO. It never gates.
- **Export ≠ share** (D107) and **an export is a read that produces no assessment** (D112) — it appends a hand-off record and moves no read.

---

## Journey (Slice 11 lens)

1. Open the **Work breakdown** document → see the authored task tree (workstreams → tasks → subtasks, outline-numbered), every row *From OSLO*, the thinnest inferences flagged *low confidence*. Below the editable doc, the **Sequencing & critical path** panel shows the ~5-week CFP chain into the Sep 1 freeze.
2. Run the deeper read (Extended pass) → **ISS-10** and **ISS-11** surface as ordinary issues on the Work breakdown; the open count goes 1 → 3.
3. Open the **Full plan** view (⊞) → read execution readiness (*Mostly OSLO's draft*, coverage of the execution-critical set), the consolidated plan, the critical path, and the confirm-before-hand-off list.
4. Confirm execution issues from the list → each routes to the existing confirm surface; the read catches up at the next analysis update (D088).
5. Click **Export to Asana** → the mapping preview shows how the plan maps, the boundary statement (intelligence stays in OSLO), the 14 tasks with assignees/dates/dependencies/provenance, and the free-tier note. Click **Export to Asana** → a simulated hand-off, a toast, and a History record.

All calls stay with the user (D001). OSLO advises; you decide — this is your plan to review and confirm before it runs.

---

## Out of scope / future

**Execution monitoring** (Execute → In execution → Outcome) is a **future phase, explicitly out of R1.** The *OSLO Task ID* custom field in the export is the deliberate runway for it (the stable anchor that would let a monitoring phase read Asana's execution state back and re-run OSLO's analysis) — but the read-back, the live Asana OAuth/API connector, and any percent-complete tracking are **not built** in R1.
</content>
</invoke>

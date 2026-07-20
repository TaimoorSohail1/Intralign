# Slice 11 — Execution-Ready Planning & Export · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype; fake data, simulated AI, **simulated Asana connector — no live API**). Load the sample project (DevNorth). "Deeper read" = the Extended / Outcome-Analysis pass. Generic artifact-editing lives in Slice 5; generic share/reader-export lives in Slice 9.

1. **The Work breakdown is an authored task tree.** Open the Work breakdown document. **Expect:** workstreams → tasks → subtasks, outline-numbered (`1 · 1.1 · 1.3.1`) with indentation; an intro saying OSLO decomposed the plan and every row is **From OSLO** until you confirm it — **not** a flat five-row table.

2. **Graded low-confidence inferences.** Scan the tree for the `low confidence` marks. **Expect:** exactly three — **1.2 Confirm 500-person Wi-Fi capacity · 1.3.1 Map AV power drops · 1.3.2 Lay out badging & check-in stations** — rendered as a neutral dashed grade (never red/amber/green), each with a "confirm this first" tooltip.

3. **Confirm a row reuses the existing engine.** Edit/accept a task cell. **Expect:** it flips **From OSLO → Confirmed by you** via the same table attestation you already use (no new confirm path); the rest of the tree still reads From OSLO.

4. **Detail does not move the read.** Note the Outcome Confidence band, then review the deeper task tree. **Expect:** the band is unchanged by decomposition — a more detailed, still-inferred plan is **not** a more mature one (completeness ≠ readiness).

5. **The deeper read finds task-altitude gaps.** Run the deeper read. **Expect:** two new Work breakdown issues appear — **ISS-10 "The freeze rests on undated tasks"** (Feasibility) and **ISS-11 "Part of the breakdown is inferred"** (Clarity); the WBS open-issue count goes **1 → 3**.

6. **ISS-11 is honest self-assessment, not a warning.** Open ISS-11. **Expect:** it names OSLO's **own** low-confidence decomposition (three inferred tasks) as evidence honesty — worth confirming before you rely on it — never phrased as a defect/warning about the plan.

7. **A finding resolves only at an analysis update.** From ISS-10, follow a resolution path / confirm. **Expect:** the issue does not self-resolve on click; it firms and the read catches up at the **next analysis update** (D088).

8. **The critical-path panel renders in the WBS view.** Stay on the Work breakdown document and scroll below the editable area. **Expect:** a **"Sequencing & critical path"** panel marked **From OSLO**, showing **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show (~5 weeks) → Sep 1**, durations flagged `low confidence`.

9. **The path is outside the editable plan.** Try to edit inside the critical-path panel. **Expect:** it is furniture outside `#artdoc` — not editable, not saved by the table engine; only the tree above it is editable.

10. **The path links to the undated-freeze finding.** With ISS-10 live, read the panel footer. **Expect:** a link "The freeze rests on undated tasks →" that opens ISS-10; resolve ISS-10 and the link is gone.

11. **The path is computed, not authored.** (Conceptual / guard.) **Expect:** the reported ~5-week chain is the longest dependency chain **to the Sep 1 milestone** — the longer ~8-week marketing chain is **not** the critical path because it does not reach the milestone (`_assertCriticalPathComputed`).

12. **Open the Full plan view.** Click **Full plan (⊞)** in the left nav. **Expect:** the pane `#pane-fullplan` opens (nav + breadcrumb in sync) showing, in order: execution readiness, the consolidated plan, the sequence that drives the date, and a confirm-before-hand-off list.

13. **Execution readiness is a validation-progress state.** Read the readiness card. **Expect:** a named state (e.g. **Mostly OSLO's draft**), "N of M execution-critical statements **Confirmed by you** · K still **From OSLO**", and a note that this is **how much you have validated — not a prediction it will succeed.**

14. **The readiness bar is coverage, not health.** Inspect the bar. **Expect:** it fills to the **Confirmed-by-you percentage** in a neutral/cool accent — no red/amber/green, no health verdict; it is a validation-coverage read (D003).

15. **The consolidated plan shows the whole model.** Read the "The plan — every workstream, consolidated" section. **Expect:** all **14 tasks across 5 workstreams**, each with owner · inferred duration (`~N wk`) · dependency (`after 1.1`) · a **critical path** tag on the chain tasks · the `low confidence` grade where it applies; every task From OSLO until confirmed.

16. **Confirm before hand-off routes to the real surface.** In "Confirm before you hand it off", click a **Confirm →**. **Expect:** the open execution issues are **severity-ordered**; Confirm opens the existing issue/confirm surface (validation, not a shadow path) — the read catches up at the next analysis update.

17. **Export is never gated.** At any readiness state, look for the export control. **Expect:** **Export to Asana ↗** is always available on the Full plan; nothing blocks it (non-blocking, DL-145 §4).

18. **The export preview maps only the plan.** Click **Export to Asana**. **Expect:** a mapping preview (`#asanaExportScrim`) with a boundary banner ("OSLO sends the executable plan… its intelligence stays in OSLO"), a How-it-maps legend, and all **14 tasks** with assignee · due · dependency · **OSLO Provenance** — and **no** critical path, issues, CAF, band, or reliability in the mapping.

19. **Provenance + monitoring anchor + free-tier fallback.** In the preview, read the legend and free-tier note. **Expect:** provenance → **OSLO Provenance** custom field (Confirmed by you / From OSLO / From OSLO · low confidence) and OSLO task id → **OSLO Task ID** custom field; and a note that free-tier Asana lands provenance as a **tag** (a degraded mode for monitoring). Custom fields require Premium.

20. **Simulated hand-off, a read that moves nothing.** Click **Export to Asana** in the modal footer. **Expect:** a **simulated** hand-off — a toast ("Plan exported to Asana — simulated…") and a **History** record noting the analysis stayed in OSLO and the export ran no analysis and moved no read (export ≠ share, D107; an export is a read, D112). No band or issue changes.
</content>

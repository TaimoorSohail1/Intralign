# Slice 5 — Plan Artifacts / Artifact Workspace · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype). "Restart" = phase-bar Restart (clears flags). Reach the workspace from the **Plan artifacts** rows in the left sidebar (or an Attention cell / issue that routes to a document).

1. **Open the explorer.** Restart → activate → load sample → run Fast Pass → look at the sidebar. **Expect:** **Plan artifacts** split into **Understanding** (Intent · Context · Scope · Requirements) and **Execution** (Work breakdown · Schedule · Resources); artifacts with open issues carry a severity-coloured count badge; artifacts with none carry **no badge**.

2. **Open an artifact.** Click **Resources**. **Expect:** the center editor fills with the drafted document; the head shows "✎ Editable" + the layer label ("Execution plan"); the toolbar shows prev/next, the version `vN`, the weakness stepper, and the save/analysis chip "Analysis up to date".

3. **Type-aware rendering.** Open **Intent**, then **Schedule**. **Expect:** Intent renders as **prose** (with a bulleted goals list); Schedule renders as a **table** (Milestone · Date · Status).

4. **From OSLO by default.** On any freshly opened artifact, read the epistemic notation. **Expect:** prose blocks tagged **From OSLO**; table cells read **From OSLO** (row gutter dot + per-cell reveal on hover). Nothing is presented as a confirmed fact you didn't confirm (D173).

5. **Edit a sentence → Confirmed by you.** In Intent, click a paragraph and type a change. **Expect:** its tag flips to **Confirmed by you** immediately; no "Editing…"/"Saving…" churn appears while typing.

6. **Edit settles → Reanalyzing → Up to date.** Stop typing (or click out). **Expect:** the version bumps, and the save/analysis chip runs **Reanalyzing…** (pulsing) then **Analysis up to date** — with **no manual reanalyze button** anywhere (D070).

7. **Saving changes no assessment (D088).** Watch the Outcome Confidence read while you edit. **Expect:** the read does **not** jump on the keystroke; the content is firmed (Confirmed by you) but the read catches up only when the analysis update lands.

8. **Edit a table cell → Confirmed by you (D083/D196a).** Open Schedule, edit a Status cell. **Expect:** that cell's reveal chip and its row's gutter dot flip to **Confirmed by you** live; editing the cell **is** confirming it (the verb is Confirm).

9. **Restructure a table.** In Resources, use the row gutter to insert a row and type into it; add a column. **Expect:** the new authored row is **Confirmed by you**; a new empty column stays **From OSLO** until typed; the same quiet Reanalyzing → Up to date runs (no manual reanalyze).

10. **Weakness annotation → light issue panel.** In Resources, hover a red/amber weak span, then click it. **Expect:** a one-line summary on hover; clicking opens the **light issue panel** — the weakness is **never resolved inline**.

11. **Weakness stepper.** Click "Jump to issue ⌃ / ⌄" in the toolbar. **Expect:** it walks between the weak spots in the open artifact ("k of N"), scrolling and highlighting each; when an artifact has none it reads "✓ No issues in view".

12. **Resolved weakness drops its mark.** Resolve an artifact's issue (via the clarification loop / analysis update) and reopen it. **Expect:** the previously coloured span is now plain text (only live annotations render).

13. **Work breakdown task tree.** Open **Work breakdown**. **Expect:** an authored graded **task tree** — workstreams → tasks → subtasks, **outline-numbered** (`1 · 1.1 · 1.3.1`), indented by level, rendered inside a table.

14. **Every WBS row is From OSLO; thin ones graded.** Read the WBS rows. **Expect:** every row **From OSLO** until confirmed; the thinnest inferences carry a **neutral `low confidence`** pill — no red/amber on the grade (it is epistemic, not severity, D003).

15. **Confirm a WBS task via the cell edit.** Edit a WBS task (or owner) cell. **Expect:** it flips **Confirmed by you** exactly like any other cell — the same generic engine, the same verb (Confirm, D196a).

16. **Critical-path panel is read-only and outside the doc.** In the Work-breakdown view, find the **"Sequencing & critical path"** panel. **Expect:** it reads **From OSLO** with **low confidence** durations, sits **below** the editable document, and is **not editable** here (its semantics live in Slice 11).

17. **Undo / redo.** Make an edit, click Undo, then Redo. **Expect:** the change reverts and re-applies; provenance/controls/annotations re-attach correctly after each; the quiet reanalysis re-runs.

18. **Ask OSLO about this document (D108).** Click the toolbar **✦**. **Expect:** the chat reports the artifact's epistemic basis (From OSLO / Confirmed by you) and reliability and links to the live issue; the editor is untouched — it changed nothing.

19. **Explorer badge is live.** Resolve an issue in an artifact, then look at its sidebar badge. **Expect:** the count drops (or the badge disappears); the colour reflects the remaining most-severe open issue.

20. **Theme + a11y.** Toggle light theme; keyboard-tab through the explorer rows, the doc nav, the stepper, and the row/column controls; check reduced-motion. **Expect:** light parity holds; every control is keyboard-operable with visible focus; the "Reanalyzing…" pulse and scroll-into-view respect reduced-motion; colour is never the sole signal (provenance + the `low confidence` grade carry text).

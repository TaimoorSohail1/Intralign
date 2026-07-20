# Slice 6 — Issues & Recommendations (Panel Model) · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype). The Simulate ▾ menu carries the demo triggers (Sim reviewer response · Deep pass, etc.). "Restart" = phase-bar Restart (clears flags).

1. **Reach the issue engine — Map default.** Click the single **Issues** sidebar item. **Expect:** the **Map** view opens by default (heading "Where your plan needs attention"); the crumb reads "Issues · Map"; there is **no separate "Attention map" nav row**; the Issues item is the active one.

2. **Map ⇄ List toggle + persistence.** Toggle to **List**, navigate away (Overview), return via Issues. **Expect:** the toggle switches panes; the crumb tracks "Issues · Map" / "Issues · List"; re-entry lands on the **last-seen** view (`_iaView`); the Issues nav item stays active for both.

3. **Map cell → panel routing.** In the Map, click a cell with exactly one open issue; then a cell with more than one. **Expect:** one issue → its panel opens; many → the **List scoped** to that document × dimension with both filters lit + "Ask OSLO about this cell →".

4. **List grouping + filters.** In the List, switch By dimension / By severity / By document and set Document · Dimension · Severity · Status filters. **Expect:** cards regroup; a triage strip (Critical · Moderate · Warning) shows under By severity; a multi-dimensional issue appears under **each** of its dimensions; an honest "N hidden by filters · clear" appears when a filter conceals issues.

5. **Four honest empty states.** Filter to an empty lens, then use the preview switch for not-yet-analyzed and unavailable. **Expect:** four distinct states — none-found ("plan looks clear") · none-under-lens ("Nothing under this lens") · not-yet-analyzed · unavailable ("a technical problem, **not** an all-clear"). An all-clear and a failure never look the same.

6. **Open an issue — the panel.** Open any card. **Expect:** always visible — severity · title · Dimension · Artifact link · Issue id · lifecycle chip · **Why this matters** · **`<dim>` impact** · the recommendation · ONE primary action; everything else (Evidence · Reviews · Comments) is a collapsible row with a chevron and hover.

7. **Lifecycle chip is not a ratchet.** Read the lifecycle chip. **Expect:** `Open ⇄ Addressed ⇄ Resolved` with **`⇄` arrows and no trailing fill** — only the current state is lit; the ⓘ says an analysis update moves it, withdrawing brings it back, never a manual step. There is **no "Acknowledge"** and **no manual "Resolve."**

8. **Apply this fix — the recommendation is on screen.** Open an issue with an appliable recommendation. **Expect:** the recommendation text is **resident above** the button; the button label is exactly **"Apply this fix"**; an issue with no renderable recommendation shows **no button** (it offers "Answer" instead).

9. **Apply → Addressed → Resolved by analysis.** Click "Apply this fix". **Expect:** the tied document is marked **Confirmed by you**, the issue moves to **Addressed** ("updating…"), and ~2s later an **analysis update** moves it to **Resolved** ("✓ Resolved by the analysis update") — resolution comes only from the update, never the click.

10. **Other options + write your own.** Expand **Other options**. **Expect:** the alternatives expand **in place** beneath the recommendation — each Selectable (→ *Confirmed by you*) or Discussable — plus a free **"Write my own fix in `<document>` →"**; the options have exactly one home (no duplicate opener).

11. **Select an option is an intention.** Click **Select** on an alternative, then **Clear selection**. **Expect:** selecting moves Open → Addressed with nothing attested; clearing returns it to **Open** with no plan change; an append-only history event records both.

12. **Withdraw a fix survives resolution.** After a fix resolves, open the issue and click **"Withdraw this fix"**. **Expect:** a consent line names the document and says OSLO will re-read (not roll back); withdrawing drops the attestation and the **analysis re-opens** the issue if the gap is back — the read is never moved by hand.

13. **Withdraw never deletes your writing.** Apply a fix, then edit that document in the editor, then withdraw. **Expect:** the document is **not** restored (your edits are kept); OSLO says so plainly and withdraws only the attestation.

14. **Clarification — one door, panel or chat.** On an issue that carries a question, answer in the panel; on another, answer the same question in chat. **Expect:** identical behaviour — project info updated, the tied document Confirmed by you, Open → Addressed, then resolved by the update; byte-identical timeline; the chat never claims to have closed it.

15. **CAF drill — level ≠ trust.** On the Overview read, read a CAF row's level word and its separate evidence cue, then click the row. **Expect:** a drill-down (Rests on · Held back by · the top open issue card · To lift it · a finding-type cut), each routing to an issue panel; the band stays a band — only the drivers are quantified.

16. **Alignment is live — Approve.** Simulate ▾ → "Sim reviewer response" with an **Approve** on an issue. **Expect:** it lands as **Attested by `<name>`**, Alignment **rises** on the read, reliability firms — and the tied **issue does not move** (a review never resolves or invalidates it).

17. **Alignment can fall — Reject.** Trigger a reviewer **Reject**. **Expect:** Alignment **falls** by the same step (symmetric), the read can go down, and it is drawn **exactly like a rise** — no alarm, no negative colour; it is evidence about alignment, not a verdict that the plan is wrong.

18. **Awaiting-review chip.** Share an issue for review, then view it in the List and the panel. **Expect:** an "◷ Awaiting review · `<who>`" chip that is **not a severity** and **does not change the issue's status**; Share for review is never disabled or metered.

19. **Task-altitude findings on the deeper read.** Run the deep pass (Simulate ▾ / on land). **Expect:** **ISS-10 "The freeze rests on undated tasks"** (Feasibility · WBS) and **ISS-11 "Part of the breakdown is inferred"** (Clarity · WBS) surface into the same lists/map/counts; the **WBS open count rises 1 → 3**; the count rises **and** the read firms in the same payoff.

20. **ISS-11 is honest inference, not a warning + a11y.** Open ISS-11. **Expect:** it reads as OSLO's honest self-assessment of its own low-confidence decomposition (never framed as a plan warning, DL-109) and resolves through the ordinary confirm/options paths; then toggle light theme, keyboard-tab through the panel rows and CAF drill, and check reduced-motion — focus rings visible, rows keyboard-operable, no analysis animation under reduced-motion, severity colour on issues only.

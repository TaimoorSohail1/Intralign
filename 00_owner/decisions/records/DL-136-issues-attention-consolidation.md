# DL-136 — Issues and the Attention map become one destination — a Map ⇄ List view toggle, Map default, last view persisted

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Issues and the Attention map become one destination — a Map ⇄ List view toggle, Map default, last view persisted

**Class:** A (experience-doctrine — navigation architecture) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-issues-attention-consolidation.md`.
**Amends** D062 (Attention map co-primary placement) and the D038 landing/switch model. **Leaves untouched** D057–D061 (the heatmap's construction + neutrality) and the **Inference map** (DL-109 §2e — a different question).

---

## Decision

"Issues" and the "Attention map" were two top-level navigation destinations that both routed to the same data — a map cell merely sets the `art × dimension` filter (`_filt`) the Issues list already uses, so the map was, in the build, a graphical selector into the list. Two front doors to one system forced a "which do I click?" decision and split one mental model. They are now **one destination with two views**.

1. **One nav item.** The separate "Attention map" nav row is retired; a single **"Issues"** destination carries both views. Its badge and active-state cover both.
2. **A Map ⇄ List toggle.** At the top of the destination, a neutral segmented control switches between the **Map** view (the artifact×dimension heatmap, including the *clean* cells — coverage the list cannot show) and the **List** view (the enumerated, filterable issues). Selecting a hot map cell scopes the list and flips to it.
3. **The Map leads (owner-directed).** First entry shows the **Map** — OSLO's differentiator is *where to look*, and the map is the more strategic landing; the list is the drill-in.
4. **The last view persists (owner-directed).** `_iaView` remembers whichever view the user last saw; re-entering the destination for any reason restores it, so the experience is consistent across visits. It is kept current automatically — every map cell-click and every "open the list" path already flows through `showView('attention'|'issues')`, so the last-seen view is tracked without touching those call sites.
5. **The word "Attention" is not used as the label (owner-directed).** The nav item is "Issues"; the map view is titled *"Where your plan needs attention"* (the concept, in a sentence) rather than "Attention map" (a section name); the breadcrumb reads "Issues · Map" / "Issues · List". "Attention" survives as OSLO's *concept*, not as a nav label.

## Why — the constraint that shaped it

Best practice for several representations of one dataset is a **view-switch inside one section** (list ⇄ map: Airbnb, Linear, Maps), not separate destinations — and the scope that must survive a switch was **already wired** (`_filt` persists), so this is a restructure, not a rebuild. The one thing the merge had to protect is the map's unique job: the list can only show issues that *exist*, while the map also shows the **zeros** — where the plan is clean. So the map is kept as a first-class view, never reduced to a filter. The move is combine-as-views; nothing is deleted.

## What was deliberately kept out

- **The Inference map** is untouched — it answers a *different* question (grounded-vs-inferred **provenance**, not where issues cluster) and stays its own surface, not a third tab.
- **The limiter, the read, the counts** — unchanged; the issue count still lives once, now on the single "Issues" nav item.

## Guardrails

- **Both views survive** — the coverage map (with its clean cells) and the enumerated list are both reachable; the map is not a filter.
- **One scope, preserved on switch** — `_filt` carries the active `art × dimension × severity` across Map and List; a cell selection scopes the list; toggling back keeps context (extends D062's "preserves prior context").
- **One home for the count** — the badge is on the single nav item; no double-count. → consistent with `_assertNoCountIsRenderedTwice()`.
- **The map stays neutral** — "brighter = more attention," never a health/RAG score (D003 / D057–D061 unchanged).
- **The tour + palette follow** — the tour's map step and the command palette point at the combined destination (Issues — Map / Issues — List); no dangling "Attention map" nav reference.

## Governance

Lands as Class-A canon via `dl-land`, amending D062 and the D038 switch model. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the merged nav, the Map-default entry, the persist-last-view behavior, and both toggles verified). AI drafted + built; **only the owner ratifies.**

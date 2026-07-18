# DL-140 — The Readout document is renamed to Executive Briefing

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The Readout document is renamed to "Executive Briefing"

**Class:** B (display terminology — the Reports workspace's document name) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Amends** D172d (the document the Reports workspace holds is now named **Executive Briefing**, not "Readout"; the workspace stays **Reports**). **No behaviour change** — the composer, the editor, the send/export/schedule machinery are untouched.

---

## Decision

The editable, PM-authored document in the Reports workspace — the one you **write and send** — is renamed from **"Readout"** to **"Executive Briefing."** The name clarifies its purpose (an authored briefing for an audience) and distinguishes it from the *generated* reports coming on the roadmap (Outcome Readiness · Assumptions & Evidence · Decision Record), which are OSLO-produced snapshots, not authored documents. **They address different needs and are not merged.**

The rename happens in **one place** — the document's display name (`doc`) in the `REPORT_TYPES` registry, surfaced everywhere through `_readoutDocName()`, so the toolbar title and every display surface follow. Two deliberate scoping decisions:

- **Display only.** The internal key (`k:'readout'`), the type-name (`nm:'Readout'`), the element ids (`#rptEd`, `#rptPop`), the guard/function names (`_assertReadout*`), and the doctrine/notes references are **unchanged** — none are user-facing. Only what the user reads moves: the toolbar title, the ARIA labels, and the (dormant) upsell/limit labels that named the document.
- **`nm` stays "Readout" on purpose.** The D143 dead-type guard reads `nm` and matches on first words; "**Executive** Briefing" would false-match the dead *"executive report"* type. Keeping `nm:'Readout'` (internal) avoids that while `doc` carries the new user-facing name.

## Why — the distinction it protects

The Reports workspace will hold two *kinds* of thing: the **authored briefing** you write (this document) and the **generated snapshots** OSLO produces (the roadmap reports). Conflating them was a real risk — the briefing is editable and composed; a generated report is read-only and computed. Naming the authored one "Executive Briefing" makes its purpose legible and keeps the two kinds from blurring as the report set grows.

## Guardrails

- **D172d preserved, amended in one clause** — the workspace is still **Reports**; the document it holds is now **Executive Briefing**. The name guard was made **robust**: it asserts the document toolbar title **equals the registry `doc` name** (whatever it is), and that the document is never called "Reports" — so the name lives in one place and the toolbar can never drift from it. → `_assertReportsHostsOneReportType()` (amended).
- **One report type still (D143)** — this is a rename, not a new type; the six dead "report types" stay dead; no speculative type-picker chrome.
- **No behaviour change** — the composer/editor and send/export/schedule are untouched (`_assertReadoutEditorProducesNothing`, `_assertReadoutIsOneContinuousDocument`, etc. all green under their unchanged internal names).

## Governance

Lands as Class-B canon via `dl-land`, amending D172d's document-name clause. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the toolbar renders "Executive Briefing," the workspace stays "Reports"). AI drafted + built; **only the owner ratifies.**

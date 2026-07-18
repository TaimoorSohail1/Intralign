# DL-141 — The Reports workspace holds multiple reports; the first generated report, Outcome Readiness, ships

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# The Reports workspace holds multiple reports — and the first generated report, Outcome Readiness, ships

**Class:** A (product scope — the Reports workspace becomes multi-report; a new generated report) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-reporting-roadmap.md`.
**Amends** D143 (the "exactly one report type" guard — real reports may now be added) and extends D172d (the workspace holds the authored Executive Briefing **plus** generated reports). **Upholds** D183b (no composite/forecast), D003 (maturity, not health), D160 (the reading surface).

---

## Decision

The Reports workspace no longer holds a single document. It now hosts **more than one report**, switched by a slim tab strip, and the **first generated report — Outcome Readiness — is built.**

1. **Multi-report workspace.** A tab strip (`#rptTabs`) at the top of the workspace switches between the workspace's real documents: **Executive Briefing** (Authored) and **Outcome Readiness** (Generated), each tab labelled by kind. `switchReport(k)` toggles the surfaces; `enterReports()` is the view entry.
2. **Two kinds, kept distinct.** The **authored** Executive Briefing is the editable composer (unchanged — its `#rptDoc`/`#rptEd` stay in the DOM, just hidden, when a generated report is shown, so every Briefing guard still verifies). The **generated** Outcome Readiness renders read-only into its own surface (`#rptGenPage`). They address different needs and are never merged.
3. **Outcome Readiness — generated from live state.** Every value is computed (`currentRead` / `_cafOf` / `_limitingOf` / reliability / `_ovGroundingHTML` / issues / `_readRung`): the Outcome Confidence band + neutral ramp, the CAF drivers with per-dimension evidence, the limiter, the reliability basis (Sound / gap), where the read stands (grounding counts, issues, rung), and the one next move (the top issue's load-bearing assumption). No authored text; **no number is invented, no forecast, no composite score** (D183b); the framing is maturity, not health (D003). It matches the reviewed sample (`report-samples.html`).

## Why — the constraint that shaped it (D143)

D143's protection was against **speculative report types** — a gallery of types with no document behind them (the six-card scaffold). That protection is preserved, not discarded: the "exactly one type" guard is **replaced** by "**only REAL types** — every registered report must carry a `render` function, and the authored Briefing must be present." A registered type with no document behind it still fails the build. What changed is only that *real, implemented* reports may now be added — which the D172d guard's own comment always anticipated ("a second type is an ADDITION to `REPORT_TYPES`, not a rebuild").

## Guardrails

- **Real reports only (D143 preserved)** — every `REPORT_TYPES` entry must have a `render`; the six dead types stay dead (the dead-type check is unchanged; `nm:'Outcome Readiness'` carries no dead first-word). → `_assertReportsHostsOneReportType()` (amended: real-types-only, not one-type).
- **The Briefing is intact** — its editable document stays in the DOM; the D172d name guard, the one-continuous-document and editor-host guards all verify at boot on the unchanged Briefing.
- **The tabs are navigation, not the scaffold** — a switcher among documents that *exist*, not a picker for types to create; it uses none of the forbidden scaffold selectors and is not resident in `#reportsBody`.
- **No forecast / no composite** (D183b); **maturity, not health** (D003); **computed, never invented** (D173) — the report prints only what OSLO computes.

## Scope note (follow-ons, not in this DL)

Export/send for generated reports, and the **Summary ⇄ Full depth** (per the roadmap packet), are **not** in this DL — this ships the multi-report workspace + Outcome Readiness's Summary view. **Assumptions & Evidence** and the **Decision Record** are the next two generated reports.

## Governance

Lands as Class-A canon via `dl-land`, amending D143 and extending D172d, realizing part of the reporting-roadmap packet. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the tab switch, the live-computed report, and the untouched Briefing all verified). AI drafted + built; **only the owner ratifies.**

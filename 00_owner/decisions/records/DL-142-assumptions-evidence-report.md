# DL-142 — Generated report #2 — Assumptions & Evidence

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Generated report #2 — Assumptions & Evidence

**Class:** B (an addition within the ratified multi-report framework — no new architecture) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-reporting-roadmap.md`. **Realizes** the second of the three generated reports; **extends** DL-141 (the multi-report workspace). **Upholds** D183b (no composite/forecast), D003 (maturity, not health), DL-109 (inference named honestly, never as a warning), D143 (real types only).

---

## Decision

The second generated report, **Assumptions & Evidence**, ships into the Reports workspace's tab strip (alongside the authored Executive Briefing and the generated Outcome Readiness). It is OSLO's due-diligence snapshot — *what the plan rests on* — and it is **computed entirely from live state**, read-only, distinct from the authored Briefing.

It renders three things, all from data already on the read:
1. **The evidence split** — of the plan's N statements, how many are Confirmed by you vs still resting on OSLO's inference (`_progressRows()`).
2. **Load-bearing assumptions still unconfirmed** — the statements that hold up the read AND that OSLO still infers (`_ciLoadBearingStatements().filter(_ciInferred)`), severity-ranked by the issues they support (`_ciActiveSup` → `ISSUES[].sev`), each with its dimension and artifact. These are the "confirm these first" list.
3. **Open questions** OSLO is still asking (`_openClarIds()` → the clarification `q`), and **where each dimension leans on inference** (`_ciDimInferenceStats()` + `_evWord()`), with the Option-C honesty line: *a dimension's level is not its trustworthiness.*

No value is authored or invented; **no forecast, no composite score** (D183b); the framing is maturity + evidence, and inference is named as *what OSLO is for*, never as a warning about the plan (DL-109).

## Guardrails

- **Real report, guarded the same way** — `nm:'Assumptions & Evidence'` carries no D143 dead first-word; the type has a `render`, so `_assertReportsHostsOneReportType()` (real-types-only, per DL-141) stays green; the six dead types stay dead.
- **Computed, never invented** (D173) — every count/list is read from live state; nothing is hard-coded.
- **Honest inference** (DL-109) — "unconfirmed / still inferred" is stated as evidence honesty, not risk; the report never reframes inference as a defect.
- **No composite / no forecast** (D183b); **maturity, not health** (D003).
- **Class-resolve clean** — dynamic severity classes are built outside the `class="…"` literal so `_assertEveryClassNameResolves()` sees whole names (no dangling prefix).

## Scope note

Export/send and the **Summary ⇄ Full depth** (this report is one of the two that gets depth, per the packet) are a **later pass** across the report set, not in this DL — this ships the Summary view. The **Decision Record** is the third and final generated report.

## Governance

Lands as Class-B canon via `dl-land`, realizing part of the reporting-roadmap packet and extending DL-141. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the report renders live from state, the tab switch verified across all three reports). AI drafted + built; **only the owner ratifies.**

# DL-143 — Generated report #3 — Decision Record

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Generated report #3 — Decision Record

**Class:** B (an addition within the ratified multi-report framework — no new architecture) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-reporting-roadmap.md`. **Realizes** the third and final generated report; **extends** DL-141 (the multi-report workspace) and completes the trio begun in DL-141/DL-142. **Upholds** D088 (the read moves by analysis, never by the hand-path), D183b (no composite/forecast), D003 (maturity, not health), D173 (computed, never invented).

---

## Decision

The third and final generated report, **Decision Record**, ships into the Reports workspace's tab strip (alongside the authored Executive Briefing and the generated Outcome Readiness and Assumptions & Evidence). It is **the human-judgement half of the strategic chain** — the owner's own decisions, each paired with what it firmed — and it is **computed entirely from live state** (the `_decision` register), read-only, distinct from the authored Briefing.

It renders, for each standing decision the owner has made:
1. **What was decided** — the decision, named honestly by kind: *Applied OSLO's fix*, *Answered OSLO's question*, or *Chose a path*, against the issue it addressed and its dimension.
2. **What it firmed** — the document it touched, now **Confirmed by you**, and the reliability move it produced (e.g. *Moderate → High*), read from the captured `relBefore` and the live document state. A pure path-selection is named honestly as *addressed, not yet confirmed into the plan* — because a selection attests nothing (`attests:false`).
3. **Whether the read has taken it up** — a per-decision status: **Live in the read** if an analysis update has run since the decision, or **Awaiting the next analysis update** if not.

A closing summary states how many documents are now Confirmed by you and how many decisions await the next update, with the D088 line in full: *a decision firms the document it touches and can raise its reliability, but it does not move the Outcome Confidence read by itself — that moves only when the next analysis update takes the change up.*

## Why — D088 is the law of this report

The obvious-but-wrong version of a "decision record" is a vanity trail: *"your decisions raised confidence from Low to High."* That is exactly the attribution **D088 forbids** — the hand-path (a fix, an answer, a selection) **addresses** an issue and **firms** a document, but only an **analysis update** moves the read and resolves the issue. So this report is built to *separate* the two: it shows what the owner's judgement firmed (real, immediate, document-level) and marks, per decision, whether the read has actually caught up. The honesty *is* the feature — the report is the human-judgement half of the read, shown as distinct from what the analysis has since confirmed.

## Guardrails

- **Real report, guarded the same way** — `nm:'Decision Record'` carries no D143 dead first-word; the type has a `render`, so `_assertReportsHostsOneReportType()` (real-types-only, per DL-141) stays green; the six dead types stay dead.
- **D088 honesty, structural** — the report never writes a band, a width, or a Confidence; it reads the `_decision` register and the append-only HISTORY, and computes "taken up" as *an analysis run newer than the decision's own event*. No decision is ever credited with moving the read.
- **Computed, never invented** (D173) — every row, count, and reliability move is read from live state (`_decision`, `PLAN_SECTIONS`, `HISTORY`); nothing is hard-coded.
- **No composite / no forecast** (D183b); **maturity, not health** (D003) — the decision marker is a **neutral** accent (the owner's earned judgement), never a severity colour.
- **Class-resolve clean** — the dynamic status class (`gr-dstat-live` / `gr-dstat-await`) is built outside the `class="…"` literal so `_assertEveryClassNameResolves()` sees whole names; both variants carry CSS rules.

## Scope note

Export/send and the **Summary ⇄ Full depth** (this report is one of the two that gets depth, per the packet) are a **later pass** across the report set, not in this DL — this ships the Summary view. With this, **all three generated reports are built** (Outcome Readiness · Assumptions & Evidence · Decision Record); the roadmap's remaining work is the cross-report export/depth pass.

## Governance

Lands as Class-B canon via `dl-land`, realizing the last of the reporting-roadmap packet and extending DL-141. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the report renders live from state, the four-tab switch verified, and the D088 taken-up transition verified — a decision made before an analysis run reads *Live in the read*, one made after reads *Awaiting the next analysis update*). AI drafted + built; **only the owner ratifies.**

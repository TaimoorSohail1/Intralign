# DL-144 — Generated reports — Summary ⇄ Full depth + Export

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Generated reports get Summary ⇄ Full depth, and an Export affordance

**Class:** B (an addition within the ratified multi-report framework — no new architecture) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-reporting-roadmap.md`. **Completes** the reporting roadmap begun in DL-141/DL-142/DL-143 — the cross-report pass the earlier DLs scoped out. **Upholds** D088 (the read moves by analysis, not the hand-path), D183b (no composite/forecast), D003 (maturity, not health), D160 (the reading surface), D107 (an export is a frozen snapshot; a share link is view-only access to the live project — different objects, different names), DL-109 (inference named honestly).

---

## Decision

The three generated reports gain the two follow-ons the roadmap packet scoped as a later pass: a **Summary ⇄ Full depth** toggle on the two reports that warrant it, and an **Export** affordance on all three.

1. **Depth — Summary ⇄ Full, on two reports.** **Assumptions & Evidence** and **Decision Record** carry a persisted depth toggle (registry `depth:true`; state `repDepth`, per report, restored on re-entry). **Outcome Readiness is single-depth** (short by design — it says so). **Summary** is the decision-useful shortlist a sponsor reads; **Full** is the complete, computed register the PM does due diligence in. Every added value in Full is read from live state — nothing authored, nothing invented:
   - **Assumptions & Evidence · Full** adds, to each load-bearing assumption, the open issues that break if it is wrong (`_ciActiveSup`), and a new **complete inferred register** — *every* statement OSLO still infers (`_ciStatements().filter(_ciInferred)`), grouped by Clarity · Alignment · Feasibility, each with its artifact and a load-bearing flag — plus the confirmed-side count. Summary is the shortlist; Full is the whole set.
   - **Decision Record · Full** adds, to each standing decision, the issue it addressed and what confirming it unblocks (its severity + recommendation), and a **Withdrawn — the append-only trail** section built from `HISTORY` (`type==='withdrawn'`): the decisions you took back, shown honestly, because *a withdrawal is a new event, never an erasure* (D096–D100 · D128).

2. **Export — one surface, reused.** Every generated report carries an **Export** control that opens the **existing, ratified export modal** (`openExportSeam()`) — the same surface the authored Briefing and the read use, carrying the analysis-currency marker, the understanding-maturity disclaimer, tier gating (Free = PDF; PDF is never taken away), and the append-only export record. **No parallel export machinery was built.** "Send" is that modal's **view-only share link** — a share of the *live project*, kept distinct from an export (a *frozen snapshot*) per D107. There is no compose-and-send here; composing a note that goes out remains the authored Executive Briefing's distinct job.

## Why — the depth is real, and the export is honest

The packet's rule was that reports are **shareable documents**, and that two of them get depth. The risk in "depth" is padding — a Full view that just repeats Summary in a bigger font. This build avoids that: Full adds *provenance and completeness* a sponsor doesn't need but a PM auditing the plan does — the issues each assumption props up, the entire inferred set (not just the top of it), and the withdrawn trail. The risk in "export" is inventing a second export path that drifts from the product's one honest export surface. This build avoids that too: it **reuses `openExportSeam()`**, so the currency marker, the disclaimer, the tier rule, and the D107 export-vs-share distinction all hold with zero new surface to keep true.

## Guardrails

- **D088 unbroken** — depth changes *how much* the Decision Record shows, never *what it claims*: Full still never credits a decision with moving the read; the "taken up" status is unchanged. No band, no width, no Confidence is written anywhere in these renders.
- **Computed, never invented** (D173) — every Full addition (the inferred register, the supporting issues, the withdrawn trail, the counts) is read from live state; nothing is hard-coded.
- **No composite / no forecast** (D183b); **maturity, not health** (D003); **inference named honestly** (DL-109) — the register is *what OSLO is for*, not a defect list.
- **One export surface (D107)** — the Export control opens the ratified modal; no second export path; share (live, view-only) stays distinct from export (frozen snapshot) by name and by object.
- **Class-resolve clean** (D195a) — the dynamic depth-state class (`gd on`) and every new class carry CSS rules; the modifier is built outside the `class="…"` literal.
- **The reports guard holds** — `_assertReportsHostsOneReportType()` stays green (real types only, each with a `render`; the six dead types stay dead); the authored Briefing is untouched.

## Scope note

This **completes** the reporting roadmap: three generated reports (Outcome Readiness · Assumptions & Evidence · Decision Record), each exportable, two with Summary ⇄ Full depth, alongside the authored Executive Briefing. No further report work is scoped in the packet.

## Governance

Lands as Class-B canon via `dl-land`, completing the reporting-roadmap packet and extending DL-141/142/143. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; both depth states rendered and verified across both reports, the Full inferred register and withdrawn trail confirmed live from state, and the Export control confirmed to open the ratified export modal). AI drafted + built; **only the owner ratifies.**

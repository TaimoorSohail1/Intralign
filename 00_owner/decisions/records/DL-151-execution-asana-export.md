# DL-151 — Execution-ready planning, Phase-3 — the structured Asana export

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-3 — the structured Asana export; the execution-ready direction complete

**Class:** B (a build within the ratified execution-ready framework — no new scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** **DL-145** (execution-ready planning identity), **Phase-3** — *the structured, provenance-preserving Asana export* (DL-145 §7) — and with it **completes the execution-ready direction.** **Consumes** the Phase-2 model (DL-146–150: the task model, its provenance/grades, and the critical path). **Upholds** DL-145 §1 (the export handoff), §7 (deep connector, Asana first, provenance as a native field), **D107** (export ≠ share), **D003/D183b** (no analysis leaks as health/score), **D112** (an export is a read; it produces no assessment).

---

## Decision

OSLO can now **export the executable plan to Asana** — the structured hand-off across the boundary. The *Export to Asana* control on the Full plan view opens a **mapping preview** (what will land, before it sends), then a **simulated hand-off** with a History record. Two owner-directed decisions shape it, both refined against the owner’s stated vision — *OSLO remains the source of truth for the plan; its intelligence stays in OSLO; the next phase is OSLO monitoring execution:*

1. **Only the executable plan crosses; the intelligence stays in OSLO.** Tasks · subtasks → Asana tasks; owners → assignees; durations/dates → due dates; dependencies → dependencies. **OSLO’s analysis — the critical path, the open issues, the maturity read — does NOT cross;** it stays in OSLO, live, so the user returns to OSLO during execution and so the coming **execution-monitoring** phase can read Asana’s state back and re-run OSLO’s analysis rather than fighting a stale copy of it baked into Asana. `_assertExportSendsPlanNotAnalysis()` enforces this — the mapping carries only the execution allowlist (id · name · assignee · due · deps · provenance); any analysis field fails the build.
2. **Provenance lands as an OSLO-owned custom field, plus a monitoring anchor.** Each task carries an **OSLO Provenance** custom field — *Confirmed by you / From OSLO / From OSLO · low confidence* (carrying the 2A grade) — reframed against the vision as an **OSLO-owned, read-only honesty signal** (so the execution team never runs an inferred task as if it were firm) rather than a validate-in-Asana worklist (validation stays in OSLO). And — a requirement the vision surfaced, not in the original DL — each task also carries an **OSLO Task ID** custom field, the **stable anchor the execution-monitoring phase needs** to reconcile Asana’s execution state back to OSLO’s plan of record. **Tag fallback** covers free-tier Asana for the honesty signal; the DL notes free-tier is a degraded mode for monitoring (the structured fields are what monitoring reads back).

The export is **non-blocking** (DL-145 §4) — always available; it plainly states how many statements are Confirmed by you vs cross flagged From OSLO. It is prototype-**simulated** (no live Asana API), like the reader-export (DL-144), and it is distinct from that reader-export (a frozen human snapshot) — this is the *structured, executable* hand-off (D107: different objects).

## Why the boundary is drawn here (the owner’s vision)

The vision gives a sharp test for what crosses: *does Asana need it to **execute**, or does OSLO need it to **reason**?* Execution mechanics cross (structure, sequencing, assignees, provenance-as-honesty, the id anchor); reasoning stays (critical path, issues, the read). This keeps OSLO the source of truth, pulls the user back to OSLO during execution, and — decisively — sets up the **next phase (execution monitoring)** correctly: Asana holds execution truth, OSLO holds plan truth + live intelligence and reads execution back through the OSLO Task ID anchor. Exporting the analysis (a superficially “more complete” hand-off) would freeze it, disconnect it from OSLO’s live monitoring, and compete with what OSLO recomputes — undermining the very phase it is meant to feed.

## Guardrails

- **The plan crosses, not the analysis** — `_assertExportSendsPlanNotAnalysis()`: the mapping carries only the execution allowlist and **no** critical-path flag, issue, CAF/band or reliability; and every task carries the two non-negotiables (provenance + OSLO Task ID). (Boot self-check now **154/154** — one new guard.)
- **Export ≠ share, and it produces no assessment** (D107 / D112) — a distinct execution-export, separate from the reader-export; it appends a hand-off record and moves no read.
- **No analysis leaks as health/score** (D003/D183b) — nothing crosses that could read as a forecast or a health verdict; the provenance field is an epistemic state, not a rating.
- **OSLO is the record** — the provenance field is OSLO-owned and read-only; OSLO’s plan governs; the field points back to OSLO.
- **Non-blocking** (DL-145 §4) — export is always available; the preview says what is still From OSLO, it never gates.
- **Class-resolve clean + dialog registered** (D195a) — new `ax-*` classes carry CSS; `#asanaExportScrim` is in `_DIALOG_PANELS` (opaque panel verified).

## Scope — Phase-3 completes the direction; the runway to monitoring

With this, the execution-ready direction ratified in DL-145 is **complete**: identity (DL-145) → the model, 2A–2D (DL-146–150) → the structured Asana export (this DL). The design deliberately lays the runway for the **next major direction — execution monitoring** (the OSLO Task ID anchor, intelligence kept in OSLO, the read-back architecture). Real-world follow-ons when it leaves the prototype: the live Asana OAuth/API connector, the custom-field/tag write, and the round-trip read for monitoring.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing DL-145 Phase-3 and completing the execution-ready direction. Built + verified in the deliverable prototype (boot self-check **154/154**, 0 pageerrors; the mapping preview renders all 14 tasks with assignees · dates · dependencies · the OSLO Provenance field (3 low-confidence carried) · the OSLO Task ID anchor; the boundary guard confirms the analysis does not cross; the hand-off is simulated with a History record). AI drafted + built; **only the owner ratifies.**

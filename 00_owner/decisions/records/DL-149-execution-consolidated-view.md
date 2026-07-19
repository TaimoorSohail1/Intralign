# DL-149 — Execution-ready planning, Phase-2 · 2D — the eighth consolidated view (Full plan)

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Execution-ready planning, Phase-2 · 2D — the eighth consolidated view (Full plan); Phase-2 model complete

**Class:** B (a build within the ratified execution-ready framework — no new scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** **DL-145** (execution-ready planning identity), Phase-2 slice **2D** — *the eighth consolidated view* (DL-145 §6) — and with it **completes the Phase-2 model.** **Ties together** DL-146 (the task tree), DL-147 (task-altitude assessment), DL-148 (the critical path). **Upholds** DL-145 §4 (readiness = coverage → a validation-progress state, non-blocking, artifact-readiness not outcome-likelihood), D183b (no composite/forecast), D003 (maturity, not health), D088, D160.

---

## Decision

The seven documents stay focused surfaces for reviewing and editing in isolation; the **eighth consolidated view — “Full plan” — is the whole sequenced plan in one place, the pre-export surface** (DL-145 §6). It is a peer view in the nav (`showView('fullplan')`), read-only with confirm routing, re-rendered live on entry. It renders, all computed:

1. **Execution readiness** (DL-145 §4). The **provenance coverage of the execution-critical set** — of the plan’s execution-document statements (Work breakdown · Schedule · Resources), how many are **Confirmed by you** vs still **From OSLO** — surfaced as a **named validation-progress state derived from that coverage** (*Mostly OSLO’s draft → Load-bearing confirmed → Fully validated*). The state describes **what the user has validated, never a “will-succeed” verdict**; it is **scoped to artifact-readiness, not outcome-likelihood**; it is **one substrate** (a read-off of grounding, `_execReadiness()`); and it is **non-blocking** — Export is always available, and OSLO says plainly it carries what is still From OSLO into the hand-off, flagged. The coverage bar is a validation-coverage read (Confirmed-by-you), **never a health bar** (D003).
2. **The sequence that drives the date.** The **computed critical path** from 2C, reused verbatim (`_wbsCriticalPathHTML()`) — the chain into the Sep 1 freeze, durations low-confidence, linked to the undated-freeze finding.
3. **Confirm before you hand it off.** The open execution issues — severity-ordered, each with its document and a **Confirm →** that routes to the existing confirm surface. This draws the task-altitude findings from 2B (the undated freeze · the inferred breakdown) into the pre-export review alongside the rest. **Validation, not a shadow path** — confirming firms the item and the read catches up at the next analysis update (D088).
4. **The export** (DL-145 §7). *Export to your tool* opens the **ratified export surface** (`openExportSeam()`) — non-blocking, no parallel machinery.

## Why this is the finish for Phase-2

2A decomposed the plan, 2B assessed it at task altitude, 2C sequenced it. 2D is where those become a **single reviewable picture the user acts on before export**: what the plan is, what drives its date, how much of it they’ve validated, and what to confirm first. It is the surface Phase-3 (the Asana export) hands off from. With it, the Phase-2 model — **decomposition · task-altitude assessment · sequencing/critical-path · the consolidated view** — is **complete.**

## Guardrails

- **Readiness is coverage + a validation-progress state, never a score** (D183b / DL-145 §4) — computed by `_execReadiness()`; the state is a threshold read-off of the coverage, in validation language, not a fitness verdict; the bar is Confirmed-by-you coverage, not health (D003).
- **Non-blocking** (DL-145 §4 / D138) — Export is always live; the view never gates the hand-off, it only says what is still inferred.
- **Computed, never invented** (D173) — the coverage, the state, the critical path and the confirm list are all read from live state; nothing is authored.
- **The seven documents are untouched** — this is an eighth *view*, added as a peer pane; the focused documents, their editors and every existing guard verify unchanged. Class-resolve clean (D195a): new `fp-*` classes carry CSS; `.conf-low` made global so it paints in the reused critical-path panel and here.
- **The read still moves by analysis** (D088) — the confirm affordances route to the existing attestation/clarification paths; nothing here moves the Outcome Confidence read by hand.

## Scope — 2D completes Phase-2; Phase-3 is next

The Phase-2 model is done (2A–2D). **Phase-3** remains: the structured, provenance-preserving **Asana export** (the *Export to your tool* button is its entry; today it opens the ratified snapshot-export surface). Possible refinements: literal inline confirm in this view (today it routes to the confirm surface), and richer per-task readiness inputs.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing DL-145 Phase-2 · 2D and completing the Phase-2 model. Built + verified in the deliverable prototype (boot self-check **153/153**, 0 pageerrors; the view renders live — readiness *Mostly OSLO’s draft · 7 of 29 confirmed*, the computed critical path, 7 execution items to confirm, the export entry — as a peer pane with nav + breadcrumb in sync). AI drafted + built; **only the owner ratifies.**

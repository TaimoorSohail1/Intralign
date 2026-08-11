# OSLO — UX Audit: "Export a plan optimized for outcomes"

**Date:** 2026-08-05 · **Target file:** `oslo-prototype-r2.html` (AI-first R2, canonical per DR-1) ·
**Method:** oslo-journey-audit (persona walk to a target funnel milestone) · **Build:** verified green
(`window._S10` = 54/54, no `false`) so the audit reflects a working build, not a malfunction.

**Objective audited:** a PM user reaches the terminal **Execute** milestone — *export a plan optimized for
outcomes*. **Lens:** underspecified / undefined elements (stubs, dead-ends, undefined next-steps, ambiguous
gates) that PREVENT the PM from reaching it.

**Personas walked** (two Delivery-PM archetypes spanning the methodology axis — the sharpest fit lever for
"optimize" + "export"):
- **P1 · Maya** — Delivery PM · seasoned · software · **scrum/agile** · AI-eager. Natural hand-off = a
  backlog / Asana.
- **P2 · Ron** — Delivery PM · seasoned · construction · **waterfall/sign-off** · AI-skeptical. Export = a
  baselined, signable plan/report.

---

## Headline

**The objective is not reachable.** Both personas activate and optimize (I drove the read to **Moderate**
integrity, 5/6 grounded, 3 checkpoints), but **every export path terminates in a "Stubbed" placeholder toast** —
no artifact, no hand-off, no confirmation. The blocker is largely **universal**; each persona adds a
persona-specific miss on top.

## The path, and where it dead-ends

- Execution → **Combined · export** → **⇪ Export plan** → toast *"…to Asana / MS Project. **Stubbed.**"*
- Reports → Executive Briefing → **⇪ Export this memo** → `_exportSnapshot()` → toast *"a frozen PDF snapshot…
  **Stubbed.**"*
- Reports → **⧉ Copy** → `_exportNarrative()` → toast *"Narrative copied… **(Stubbed.)**"*

Verified: all three functions literally contain `"Stubbed"`. The only non-stub action, "Send as a memo," writes
an in-app `_sentMemos` record — nothing leaves OSLO.

## Underspecified / undefined elements (ranked)

**BLOCKER — Export is entirely unimplemented and unspecified (universal).**
Every export CTA is a dead-end toast. Beyond "not built," it is *undefined*: no spec for the output **format**,
the **destination**, **what crosses** (tasks only? the read? provenance?), or a **success/done state**. The
objective is "export a plan," and export has no definition to build toward. Blocks P1 and P2 identically.

**HIGH — "The plan" that gets exported is undefined and fragmented.**
Three competing candidates, none named canonical, none referencing the others: the Execution **Combined table**
("what a PM tool consumes"), the Reports **Executive Briefing** memo, and the generated **Outcome Readiness**
report. *Maya* expects a backlog/Asana hand-off and finds a static task table; *Ron* expects a signable
document. Neither can tell which artifact *is* "the plan optimized for outcomes." Axis: **methodology**.

**HIGH — "Optimized for *outcomes*" (plural) is paywalled and never self-described.**
On Free, OSLO optimizes only the **primary** outcome; optimizing for *all* outcomes is a Basic commitment gate
(`vmOutcomeCap → _payGate('multiOutcome')`). A Free PM's exported plan is optimized for **one** outcome, not
"outcomes" — the objective's plural is unreachable without paying, and the export never states which outcome(s)
it was optimized for. The objective's condition is silently unmet and undisclosed.

**HIGH — No definition of "optimized *enough* to export."**
Export is not gated on maturity (`_exportGuard` only re-reads pending items). A PM can export a "Very Low" plan
with inferred/unowned tasks — in the captured screen, "Catering" is *inferred/unowned* and "Secure backup
keynote" is *proposed/unscheduled*, yet **Export plan** is fully available. The product never tells the PM
whether the plan meets the "optimized" bar the objective requires, so they cannot know when they've reached it.

**MEDIUM — The Execute milestone is a non-state; there is no "ready to export" moment.**
The journey shows Understand · Validate · Optimize · **Execute**, but Execute is "a destination, never active."
Nothing concludes the journey with "your plan is optimized — export it now." No arrival signal, no terminal CTA.

**MEDIUM — The most outcome-optimized artifact (Outcome Readiness) cannot be exported at all**, and the ratified
**advisory disclaimer / export package (D153)** has nowhere to live because no export package exists. (Both
connect to the reporting-gap audit of the same day.)

## Persona × milestone matrix

| | Understand | Optimize | **Export (objective)** |
|---|---|---|---|
| **P1 Maya** (scrum/agile) | reaches (friction: document-not-backlog) | reaches | **BLOCKED** — stub; also no backlog/Asana hand-off |
| **P2 Ron** (waterfall/sign-off) | reaches | reaches | **BLOCKED** — stub; no signable PDF/package |

Both segments activate and optimize; **both are lost at the last step** — one universal cause plus one
persona-specific cause each.

## Recommendations (to make the objective meetable)

1. **Name the canonical export artifact** — "the plan optimized for your outcome(s)" = the Execution combined
   plan with the outcome read attached — so the three fragments resolve into one.
2. **Implement at least one real export** — PDF/package for Ron; the Asana/PM-tool **mapping-preview →
   simulated hand-off** for Maya (replacing the stub) — producing a visible artifact and a done state, with the
   **D153 disclaimer on the package**.
3. **Define "optimized for outcomes" at export** — state which outcome(s) the plan is optimized for; surface the
   multi-outcome gate honestly.
4. **Add an export-ready signal** tied to optimization (integrity / grounding), so the PM knows the "optimized"
   condition is met — without hard-blocking export (OSLO advises; you decide).
5. **Give the generated Outcome Readiness report an export.**

**Honesty note:** these are demo stubs in a prototype — but relative to *this specific objective* they are the
exact terminal step, and the surrounding underspecification (what the artifact is, what "optimized" means,
whether it is gated) is real product-definition debt that must be resolved before any PM can export a plan
optimized for outcomes.

---
*Evidence: `/tmp/oslo/audit.mjs` (walk + stub verification), screenshots `audit_export_view.png` (Combined·export
surface), `audit_export_toast.png`. Guards green at capture.*

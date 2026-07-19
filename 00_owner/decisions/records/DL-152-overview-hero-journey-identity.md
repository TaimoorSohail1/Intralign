# DL-152 — The Overview hero is the plan's journey to a hand-off — Understand, Confirm, Hand off (Direction C-1)

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# The Overview hero is the plan's journey to a hand-off — Understand → Confirm → Hand off (Direction C-1)

**Class:** A (an identity call — the hero is the product's front door and its self-description) · **Framework 001** — AI drafts; **only the owner ratifies.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Basis:** packet `DECISION-PACKET-overview-hero-repositioning` (owner-reviewed mocks: `overview-hero-options.html` → `overview-hero-C-adapted.html` → `overview-hero-composition.html` → `overview-hero-hierarchy.html`). **Reframes** **D199** (the concept is *Outcome Confidence*), **D174 / DL-104 §5** (the hero is the maturity ramp). **Preserves** **D003 / D183b** (no health, no forecast, no composite index), **D196a** (the verb is *Confirm*), **D179e** (counts have one home). **Surfaces** the **DL-149** execution-readiness signal on the Overview. **Serves** the **DL-145** execution-ready north star.

---

## Decision

The Overview hero is repositioned from **Outcome Confidence alone** to the **plan's journey to a hand-off** — a three-node arc, **Understand → Confirm → Hand off** — with the Outcome Confidence read kept fully intact as the first stage's detail. The north star (DL-145: OSLO's deliverable is an outcome-optimized plan **ready for export**) changed what a user comes to the front door asking — *"where is my plan on the way to a hand-off?"* — and the hero now answers that question directly, without giving up OSLO's differentiator: leading with the honest signal, not a green light.

The three nodes:

1. **Understand** — measured by **Outcome Confidence**, the maturity of OSLO's read (unchanged as concept **and** metric: the ramp, CAF, the limiter, the reliability basis — all present, none moved behind a click). This is the active stage while the read is still firming.
2. **Confirm** — measured by **execution-readiness coverage** (`_execReadiness`: the execution-critical details you've Confirmed vs what is still From OSLO). Validation-progress language, never a "will-succeed" verdict.
3. **Hand off** — the **destination** (export to Asana), **always reachable** because export is non-blocking (DL-145 §4). It is rendered as a destination marker (a dashed ↗), **not** a stage you occupy and **not** a "ready" verdict.

*"How ready is my plan?"* is answered by **position on the arc**, never by a fitness node. **This is the structural fix (C-1):** because export was always non-blocking, the third node was never a threshold to unlock — so it is honestly a destination, and the forbidden "ready to *succeed*" reading is removed **by construction, not by disclaimer.** It is *more* accurate than an "Export-ready" state, which would have implied a gate that does not exist.

**Composition — additive, with the Understand read nested (V1).** The arc is a slim top-line frame; the Outcome Confidence panel sits **directly beneath it as the Understand stage, opened** — an inset detail card carrying the cool maturity accent on its left edge and an *Understand* tab, so the panel visibly belongs to that node rather than reading as a disjoint section (owner-directed, 2026-07-19). The panel's markup is **byte-for-byte the ratified hero**, so its guards keep verifying unchanged; the nesting is a wrapper and a tab around it. Rejected: folding the confidence detail into an expandable stage — it would demote the honest maturity read, the exact signal OSLO must lead with.

## What stays intact · what changes

**Stays:** Outcome Confidence as the honest maturity read (D003 / D183b) — now framed as the *Understand* stage's measure, its ramp / CAF / limiter / reliability all first-class and never behind a click; the top-bar Outcome Confidence chip; export non-blocking (DL-145 §4); counts have one home (D179e); no forecast, no health, no 0–100 index anywhere.
**Changes:** the hero **gains the journey framing**; **execution-readiness surfaces on the Overview** (the *Confirm* stage) instead of only in Full plan; the **hand-off destination** appears as the arc's endpoint; the confidence panel is **nested** under the Understand node (V1).

## Why this is an identity call (Class A)

The hero is the product's self-description — the first thing a user reads and the frame every other surface inherits. Changing what it leads with is a change to what OSLO says it *is*. It reframes two identity doctrines (D199, D174) without overturning them: Outcome Confidence remains the concept and the maturity ramp remains its shape; they are now the *Understand* stage of a lifecycle rather than the whole story. Because it touches identity, it lands as a ratified decision **before** the build DL that implements it.

## Guardrails carried into the build

- **No verdict node** — the third node is a destination, always reachable; no "ready/green" state, no "you've arrived" treatment.
- **Outcome Confidence unchanged** as the maturity read; its existing hero guards stay green on an unchanged panel.
- **Readiness = coverage, not likelihood**; and the two front-door counts (whole-read grounding vs execution-readiness) must each name their scope so they cannot read as a contradiction (D179e — one substrate, scoped views, not a second competing tally).
- **No forecast, no health** (D003 / D183b) in any stage name, colour, or the arc — the accent is the permitted cool maturity token, never brand orange, never RAG.
- **Computed, not authored** (D173) — the arc position and both stage metrics are read from live state.
- **The nesting is a build fact** — the Understand read is a genuine descendant of the inset, tabbed and spined, or the hierarchy silently reverts to two disjoint sections.

## Forward note — the hero across the planning → execution boundary (owner-raised)

The arc today is a **planning** arc; it ends at *Hand off*. When OSLO reaches the **execution-monitoring** direction, the hero must disclose execution state and progress. Captured for that phase (not in scope here): keep the **arc as the lifecycle spine** — it *extends* past *Hand off* into execution nodes (e.g. *In execution → Outcome*) rather than being replaced — and make the **detail panel phase-aware** (the maturity read during planning's *Understand*; an execution read once in an execution stage). The V1 nesting generalizes cleanly: each stage opens into its own detail the same way. The anti-health-tracker spine (D003 / D183b) carries across the boundary — execution disclosure stays OSLO's honest voice (*what's moving, what I'm flagging, what I'd do*), never a green/red "on-track" gauge. This is a point in favour of C-1: a static "how mature is my read" hero would not have extended into execution at all; the journey spine does.

## Governance

Lands as **Class-A** canon via `dl-land`, reframing D199 / D174 and surfacing the DL-149 readiness signal on the Overview. The C-1 framing, the naming (*Understand · Confirm · Hand off*), and the additive/V1-nested composition were owner-reviewed against four mock iterations and the live prototype before ratification. The build follows in a **Class-B** DL (the journey arc, the V1 nesting, the new guards, the two-count scope reconciliation), verified in the deliverable prototype. AI drafted; **only the owner ratifies.**

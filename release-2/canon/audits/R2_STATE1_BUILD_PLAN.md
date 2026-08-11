# R2 State-1 — sequenced build plan

**Status:** ✍️ **Plan for approval (Idris, Framework 001) — nothing cut into the prototype until approved.** Sequences DL-194 §4's eight dependencies + DL-195 (Adaptability / checkpoint proposal). Build proceeds phase-by-phase; each phase ends green (guards + on-screen evidence) before the next starts.

## 0. Starting point (already in R2)
DL-193 increment 1 (queue re-anchored to outcome-integrity exposure), "What changed" card removed. **Guards 168/168.** Canonical `prototype-r2.html` synced + committed.

## 1. Critical path
**Phase A** (integrity engine) → **Phase B** (indicator + read-panel reframe) → **Phase C** (checkpoint-proposal capability) → **Phase D** (high-Adaptability fixture + tab relabel + polish). Phase A is the foundation every visual reads from; Phase B is the risk concentration (heavily-guarded hero); C and D are additive.

---

## 2. Two decisions to settle BEFORE Phase B (Phase A can start regardless)

**2a. The "Outcome Confidence → Outcome Integrity" ripple — scope call.** The reframe makes **Outcome Integrity** (the composite of Viability × Grounding × Adaptability) the new top-level concept, with **Outcome Confidence surviving as the Viability pillar** beneath it (it *is* the CAF band). "Outcome Confidence" appears on many surfaces — the hero, the top-bar pill, the Confidence popover, the trend surface, chat, reports. Question: which reframe in R2?
- **Recommendation:** R2 reframes the **hero + the top-bar pill** (the primary read surfaces the PM sees first); the deeper surfaces (popover, trend, reports, chat phrasing) align in a **contained fast-follow inside R2** so Phase B stays bounded and the hero rework isn't fighting six surfaces at once. All still ship in R2 (State-1 gate) — this is *ordering within R2*, not a cut.

**2b. Endpoint labels for the integrity band — still open.** Fragile → Sound vs Unfounded → Well-founded vs Exposed → Intact (from the earlier read-vs-outcome discussion). Now that State 1 *is* outcome integrity (with the moment-in-time + ongoing-pending guardrails), integrity-framed ends are appropriate; the call is which word pair. **Recommendation:** settle this as a 2-minute pick before Phase B (the indicator can't render without it). My lean: **Fragile → Sound** for glance-legibility, held honest by the pending-state framing.

---

## Phase A — the three-pillar integrity engine (foundation; low risk)
**Build (computation only, no UI):**
- `_adaptabilityBand()` — the three DL-195 checks (outcome checkpoints defined · runway · correction linkage), graded → a 5-step Fragile→Sound band, deterministic + legible (each check retained as the "why").
- Map **Viability (CAF)** and **Grounding** onto the *same* 5-step Fragile→Sound scale (commensurability — §DL-195 6).
- `_outcomeIntegrity()` → `{ level, limitingPillar, decomposition:[viability,grounding,adaptability] }` via **weakest-gates** (min of three; foundation-first tie-break Viability→Grounding→Adaptability).

**Guards (new):** weakest-gates-is-the-min; adaptability-band-deterministic-from-its-checks; three-pillars-commensurable (same scale); integrity-is-decomposed-not-blended (the three parts always recoverable). 
**Verify:** instrument the three pillar bands + composite level + named limiter on the DevNorth fixture; full suite green (168 → 172-ish). No UI touched → additive, reversible.

## Phase B — the integrity indicator + read-panel reframe (RISK CONCENTRATION)
**Build:**
- The **decomposed integrity indicator** (DL-194 §3): ordinal Fragile→Sound band + **named limiting pillar** + the three-pillar decomposition (visible/on-demand) + the endpoint labels (2b) + the **always-visible "ongoing pending" affordance** (moment-in-time; live tracking begins at execution).
- **Reframe the hero** ("Where you stand"): lead with the integrity indicator; the old maturity band becomes the **Viability** pillar within the decomposition; limiter → facet-diagnostic; grounding inline; **"Your next move" preserved** as the action (no duplication).
- Reframe the **top-bar pill** to Outcome Integrity (per 2a).

**Guards:** REWORK the hero/confidence guards that encode the old structure (`_assertConfidenceIsTheFirstPanel`, band/limiter/hero-elements-computed, payoff-inside-card); NEW: indicator-decomposed-on-screen, pending-state-present, **D183b reconciliation** (ordinal only, no 0–100 number, framing = moment-in-time outcome integrity not fate). 
**Verify:** full-page screenshot on the real engaged Overview (low-Adaptability fixture) + guards green. **Approach:** change one guarded element at a time, re-running the suite after each — this is where a careless edit reddens five guards at once.

## Phase C — the checkpoint-proposal capability (additive; medium risk)
**Build:** when Adaptability is the limiter, OSLO **proposes concrete checkpoints** — each with (a) the outcome leading-indicator to read, (b) timing positioned for runway, (c) the adjustable lever — carrying **From-OSLO / Confirmed-by-you provenance**, confirmable/editable/declinable. Wire it as the next-move for a low-Adaptability plan (ties to DL-193's exposure/leverage queue).
**Guards:** proposed-checkpoints-carry-provenance; confirming-a-checkpoint-is-a-real-attest (moves state honestly); proposal-surfaces-only-when-Adaptability-limits (no over-surfacing); confirmIsTheVerb / no-fabricated-certainty hold. 
**Verify:** drive the low fixture → proposal appears → confirm one → Adaptability band + integrity recompute; guards green; residue-safe.

## Phase D — high-Adaptability fixture + tab relabel + polish (low risk)
**Build:** a **checkpoint-optimized fixture variant** (Adaptability high → integrity gated by a different pillar — demos the strong end and the tie-break); **tab relabel** "Interpretation" → "Viability"; the 2a fast-follow surfaces; final copy polish. 
**Verify:** both ends (low/high Adaptability) demoable; full suite green; optional PM-persona re-audit of the reframed Overview.

---

## Verification discipline (every phase)
1. `window._s10SelfCheck()` green (no false), 0 page errors — boot-authoritative.
2. On-screen evidence (instrumented readouts and/or full-page screenshot).
3. Sync `_16`→canonical, deliver, commit to `release-2/`, log in `RELEASE_2_TRACK.md`.
4. Framework 001: each phase's substantive calls owner-ratified; nothing is canon until ratified.

## Risk map
- **Phase B is the one to watch** — the hero is the most heavily-guarded surface; budget for guard rework and go element-by-element.
- Phases A/C/D are additive and reversible.
- The 2a ripple is the scope lever: contain it (hero+pill now, rest fast-follow) or the hero rework fights six surfaces at once.

## Approval asks
- OK the phase sequence.
- Settle **2a** (hero+pill now, rest fast-follow — recommended) and **2b** (endpoint labels — Fragile→Sound recommended).
- Then Phase A starts.

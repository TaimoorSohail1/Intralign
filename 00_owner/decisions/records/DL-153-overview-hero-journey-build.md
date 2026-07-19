# DL-153 — The Overview journey hero, built — the arc, the nested Understand read, and the guards that hold them

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The Overview journey hero, built — the arc, the nested Understand read, and the guards that hold them

**Class:** B (a build within the ratified reposition — no new identity scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Realizes** the Class-A identity DL *(the Overview hero is the plan's journey to a hand-off — Direction C-1)*. **Consumes** **DL-149** (`_execReadiness`) and the **DL-146–150** task model. **Upholds** **D199 / D174** (Outcome Confidence unchanged as concept and ramp), **D003 / D183b** (no health, no forecast), **D179e** (counts have one home), **D196a** (*Confirm*), **D195a** (every class resolves).

---

## Decision

The journey hero is **built into the deliverable prototype** on the Overview. Three things ship together, each guarded:

1. **The arc** (`renderHeroArc` / `_planStage`) — a slim top-line frame, *Understand → Confirm → Hand off*, written from live state. The active node is **computed** (`_planStage`: *Understand* while the read is below High, then *Confirm*); the third node is the **hand-off destination** (a dashed ↗), never active and never a verdict. `_assertHeroArcIsHonest()` enforces exactly one computed active node, a destination third node named "Hand off", and **no forecast/health vocabulary** anywhere in the arc.

2. **The nested Understand read (V1)** — the Outcome Confidence panel is wrapped in an inset detail card (`.ch-nest`) carrying the cool **maturity** accent on its left edge and an *Understand* tab, and the active arc node **drops a maturity spine** into it. The panel now reads as **the Understand node, opened**, not a disjoint section beneath the arc. The panel markup is **byte-for-byte the ratified hero** — a wrapper and a tab are the only additions — so every existing hero guard keeps verifying on unchanged content. `_assertUnderstandDetailIsNested()` makes the hierarchy a build fact: the Outcome Confidence heading and the maturity ramp must be genuine **descendants** of the inset, the *Understand* tab must be present, the arc must sit **above** the detail, and the active node must drop its spine — or the boot fails.

3. **The two front-door counts, scoped (§5B).** The *Confirm* node shows **execution-readiness coverage** (`_execReadiness`: the execution-critical details — Work breakdown · Schedule · Resources — you've Confirmed vs From OSLO; *7 of 23*). The nested panel shows **whole-read grounding** (all statements; *20 of 48*; D179e's one home for grounding). These are **not the same tally rendered twice** — they are one statement ledger filtered to two scopes — so there is no D179e breach. To ensure they can never *read* as a contradiction, the arc names its scope: the body sentence says "load-bearing **execution details** … (7 of 23 execution-critical)" and the Confirm node carries a tooltip naming the WBS · Schedule · Resources scope and its narrower reach, while the panel says "**statements**." Different nouns, legibly different scopes.

## Why §5B resolves to two scoped counts, not one

The *Confirm* stage measures how execution-ready the plan is — the north-star question (a plan detailed enough to export). That is the execution-critical subset, correctly narrower than the whole-plan grounding the maturity read reports. Collapsing them into a single number would either drop the whole-read grounding (OSLO's honest coverage signal) or misreport execution-readiness against the wrong denominator. Keeping both, each scope-named and drawn from the same underlying ledger, is the honest resolution and honors D179e (one home for the data; the arc is a scoped view of it, not a rival count).

## Guardrails

- **The arc is honest** — `_assertHeroArcIsHonest()`: three nodes, exactly one computed active node equal to `_planStage()`, a destination third node ("Hand off"), and none of *on track · likely · probability · will succeed · ready to succeed · at risk · green light* anywhere in the arc (D003 / D183b).
- **The Understand read is genuinely nested** — `_assertUnderstandDetailIsNested()`: the confidence heading + ramp are descendants of `.ch-nest`, the *Understand* tab exists, the arc precedes the detail, and the active node drops its spine. What is not guarded is not true — so the hierarchy the owner asked for cannot silently regress.
- **Outcome Confidence unchanged** (D199 / D174) — the panel is byte-for-byte the ratified hero; `heroRampNeutral`, `heroLitBandFromState`, `heroNotAHealthBar`, `confidenceIsFirst`, `payoffLivesInside`, `heroCardNoSeverity` all stay green on unchanged markup.
- **Maturity accent only, no severity** (D179d) — the inset's left edge, the tab, the spine, and the active dot all use `--maturity` (hue ≈ 214°, cool); the whole-card colour cascade (`_assertHeroCardCarriesNoSeverityColour`) confirms no RAG hue and no `--primary` on any state element.
- **Counts have one home** (D179e) — two scopes, one substrate, each scope named; no count is rendered twice.
- **Every class resolves** (D195a) — the new `ovj-drop`, `ch-nest`, and `dtab` classes all carry CSS.

## Scope

Overview hero only. The top-bar Outcome Confidence chip and the confidence popover are untouched. The arc's *Confirm* node links to Full plan (the readiness detail's home). Real-world follow-on when the product reaches execution monitoring: the arc extends past *Hand off* into execution nodes and the detail panel becomes phase-aware (recorded in the identity DL's forward note; not built here).

## Governance

Lands as **Class-B** canon via `dl-land`, realizing the Class-A reposition. Built + verified in the deliverable prototype: boot self-check **156/156**, 0 pageerrors, FAILS none (guard count 155 → 156 for `_assertUnderstandDetailIsNested`; `_assertHeroArcIsHonest` already present). The Overview renders the arc with the active node computed, the Understand read nested in its inset with the *Understand* tab and spine, and the two counts scope-named (7 of 23 execution-critical · 20 of 48 statements). AI drafted + built; **only the owner ratifies.**

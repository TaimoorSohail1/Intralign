# DL-154 — The journey hero speaks the north star — stages become Understand, Optimize, Execute (amends DL-152)

- **Date:** 2026-07-20 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# The journey hero speaks the north star — the stages become Understand → Optimize → Execute (amends DL-152)

**Class:** A (an identity call — the stage names are the hero's self-description) · **Framework 001** — AI drafts; **only the owner ratifies.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-20 · **Amends** **DL-152** (the Overview hero repositioned to the plan's journey, Direction C-1) — the *framing* it ratified is unchanged; only the *stage names* sharpen. **Carries** the build update into the prototype (realized in DL-153). **Preserves** everything DL-152 held: **D003 / D183b** (no health, no forecast), **D179e** (counts have one home), **D196a** (per-item, the verb is still *Confirm*), and the C-1 structural fix (the third node is a destination, never a verdict).

---

## Decision

The journey hero's three stages are renamed from **Understand → Confirm → Hand off** to **Understand → Optimize → Execute**, and the arc's frame line from *"on the way to a hand-off"* to **"on the way to the outcome."** The reason: OSLO's job is to **optimize the plan for outcomes** (the DL-145 north star), and the front door should narrate *that* journey — not generic project workflow. "Confirm" named a mechanic (ticking boxes) and "Hand off" named logistics; neither said *the plan is getting better at hitting your outcome*, which is the value the arc exists to show.

The three stages, restated:

1. **Understand** (unchanged) — OSLO builds its read of the plan, measured by **Outcome Confidence** (the maturity read; unchanged as concept and metric, still nested beneath the node as the Understand stage opened).
2. **Optimize** (was *Confirm*) — the plan is firmed for the outcome: the user confirms what OSLO inferred and resolves what's weak (the limiter, the thin dimensions). Measured by the same **execution-readiness coverage** (`_execReadiness`) — only the framing sharpens from "validate" to "optimize toward the outcome."
3. **Execute** (was *Hand off*) — the **destination**: the plan goes to the tool a team runs it in. Still always reachable (export non-blocking, DL-145 §4), still a dashed ↗ destination marker, still **never a "ready" verdict**.

The whole arc now points at the **outcome** — which is also where the lifecycle spine extends when execution-monitoring ships (*Execute → In execution → Outcome*), so the front door has been pointing at the outcome all along.

## What this changes — and, deliberately, what it does not

**Changes:** two stage labels, the arc frame line, and the body copy (it now speaks the optimize-for-the-outcome journey). The arc-honesty guard's destination check is repointed from the text "hand off" to "Execute."
**Does NOT change:** the C-1 framing (three nodes; the third a destination, never a verdict; position computed from state); the nested Understand read (byte-for-byte the ratified hero, all its guards green); the two-scope §5B counts (arc = execution-critical coverage, panel = whole-read grounding); no forecast, no health (D003 / D183b); non-blocking export.

## Two doctrine notes

- **"Confirm" is not retired — it drops a level.** **D196a** ratified *Confirm* as the verb for validating a single inference; that stays as the **per-item action** (the button still says Confirm, the provenance class is still *Confirmed by you*). **Optimize** is the **stage** name above it. Different altitudes; no conflict. The node's tooltip states this explicitly.
- **"Optimize" is an activity, not a verdict.** It mirrors the north-star language (DL-145: the outcome-*optimized* plan), so it aligns the front door with the product's identity. It stays clear of the forbidden forecast reading because it names what you are *doing* (optimizing), never a claim that the outcome *will* succeed — the honesty spine (D003 / D183b) is untouched. (*Rejected register: none forced — "Strengthen" was offered as a humbler synonym; the owner chose "Optimize" for mission-match.*)

## Why this is still a Class-A call

The stage names are what the hero says the product *does* — they are identity, the same reason DL-152 was Class A. Renaming two of the three a few minutes after ratifying them is a deliberate revision, recorded as an amendment rather than drift: the framing DL-152 ratified stands; its vocabulary is sharpened to speak the north star.

## Governance

Lands as **Class-A** canon via `dl-land`, amending DL-152's stage naming; the build was applied in the deliverable prototype (arc labels, body copy, the one-line guard repoint) and verified — **md5 `3d7ab6cb` · boot self-check 156/156 · 0 pageerrors, FAILS none** (guard count unchanged; `_assertHeroArcIsHonest` now keys the destination on "Execute" and the active stage on "Optimize"). The Overview renders *Understand → Optimize → Execute*, "on the way to the outcome," with the nested Understand read and the two-scope counts intact. AI drafted; **only the owner ratifies.**

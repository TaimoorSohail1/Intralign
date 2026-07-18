# DL-129 — The maturity ladder — stage is earned evidence-maturity

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# The maturity ladder — "stage" is earned evidence-maturity, not analysis depth

**Class:** A (experience-doctrine — the maturity-stage model) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Amends D053** · **Packet:** `DECISION-PACKET-maturity-ladder.md`.
**Additive to** the recognition layer (DL-126): the rung-crossings become its milestones.

---

## Decision

"Stage" is redefined from **analysis depth** to the read's **earned evidence-maturity** — a five-rung ladder the user climbs through their own confirmations, computed from signals OSLO already has, never advanced by running an analysis.

**The ladder (the current rung = the highest whose earned condition is met):**
1. **Oriented** — the read exists but rests on OSLO's inference. Baseline; never celebrated; persists until the user's evidence begins to ground it (grounding below "partly").
2. **Corroborated** — your confirmations have begun grounding the read (grounding ≥ *partly grounded*). The first earned rung — a lighter recognition.
3. **Grounded** — the read largely rests on your evidence, not OSLO's (≥ *largely grounded*). Recognition milestone.
4. **Anchored** — nothing critical rests on a guess (no load-bearing statement remains). Recognition milestone.
5. **Validated** — anchored **and** corroborated by stakeholders/reviewers (external attestation). The earned pinnacle; loud recognition.

## Why — and what it fixes

The old model (D053: Orientation → Expanded → Validated) wore one label over two different axes. **Orientation → Expanded was *analysis depth*** — Fast Pass vs Deep Pass — which is OSLO's work and a near-universal default; that is why Orientation felt valueless (it evaporated on the first deep pass) and why stage-Expanded was pulled from recognition. Only → Validated was *evidence maturity*, and it had a single far-off rung.

The ladder drops analysis-depth from the stage concept entirely: **Fast vs Deep is now a run type that fires a notification, never a stage.** Orientation stops being fleeting — as *earned* maturity it becomes a persistent, honest state ("your read still rests on OSLO's inference") that lasts until the user does the work. And the model gains real fidelity: five rungs, every one earned, none a default, a track the user climbs and is recognized for across the life of the project.

## How it composes

- **Unifies stage + recognition.** The rung-crossings ARE the recognition milestones: Corroborated (light), Grounded, Anchored, Validated. This supersedes DL-126's stage-based milestone (stage-Validated → rung Validated) and adds Corroborated; the grounding/anchored milestones are unchanged, now named as rungs 3 and 4.
- **Three read descriptors, complementary.** The Outcome-Confidence band (how firm the read is) stays the headline; the grounding word (barely → well grounded) stays the fine-grained measure; the ladder is the synthesis layer above it — the earned-progress narrative. The confidence popover shows the current rung + position ("Grounded · 3 of 5"), the full climb on its ⓘ tip.
- **The deep pass no longer claims a stage advance** — its chat and History copy now say the deeper read firmed the assessment, and that only the user's confirmations advance the read up the ladder.

## Guardrails (executable — `_assertLadderRungsAreEarned`)

- **Earned, never a default** — the current rung is computed from `_isCorroborated` / `_isLargelyGrounded` / `_isFullyAnchored` / `_isValidated`, and `_readRung` may reference **no analysis-depth signal** (ANALYSIS_STATE / the retired stage). No recognition milestone tests an analysis-depth stage.
- **Highest-rung-met ordering** — Validated → Anchored → Grounded → Corroborated → Oriented, tested highest-first.
- **Monotonic-with-work; never band-tied** — rungs rise only as the user grounds/anchors/validates; a fall (from a deeper read) is drawn neutrally (D187/D173c). No rung is a game/XP; each reflects real evidence.
- **Oriented is not a failure state** — the honest starting point, framed neutrally.

## Governance

Lands as Class-A canon via `dl-land`, **amending D053** and folding the recognition milestones (DL-126) into the ladder. Built + verified in the deliverable prototype (boot self-check **150/150**, 0 pageerrors; new guard `ladderRungsAreEarned` green; recognition/ display guards still green). AI drafted + built; **only the owner ratifies.**

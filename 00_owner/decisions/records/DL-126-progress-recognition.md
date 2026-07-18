# DL-126 — Earned-maturation recognition

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Earned-maturation recognition — rewarding progress without gamifying it

**Class:** A (experience-doctrine) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-17 · **Packet:** `DECISION-PACKET-progress-recognition.md`
**Additive to** D187 (earned accent) · D096–D101 (History-trend) · the maturity-stage model. **Supersedes nothing.**

---

## Decision

OSLO acknowledges the user's progress through an **earned-maturation recognition layer** — deliberate, sparse, and reputation-framed — **without any gamification mechanic** (no points, badges, streaks, scores, targets, health, or burndown). The layer composes primitives OSLO already has; it introduces **no new invariant beyond the guardrails below.**

**The doctrine-safe insight:** recognition attaches **only to signals that (a) the user's own work moves and (b) cannot fall from an honest deeper read** — grounding, confirmations, understanding-maturity (stage). It **NEVER** attaches to the confidence **band**: the band can honestly fall, and OSLO draws a fall identically to a rise on purpose (D187/D173c). The instant a rise is celebrated, a fall becomes a failure — which would break the product's core honesty. So the reward is the **maturation of understanding** ("the read you'd take to leadership now rests on your evidence"), never the read going "up."

**The firing set — only genuinely EARNED crossings, each monotonic-with-work:**
1. **Largely grounded** — the read first crosses to ≥ largely grounded (grounding rises only as the user confirms).
2. **Fully anchored** — the first time nothing critical rests on a guess (no load-bearing statement remains).
3. **Validated** — the understanding reaches the Validated stage (currently the aspirational pinnacle; fires when the model advances a read to Validated through evidence work).

**⛔ Stage advance to *Expanded* is NOT recognized (owner, 2026-07-18).** Orientation → Expanded is the expected default — it is just running the Extended Analysis, which nearly every user does, and the thing that advances is OSLO computing harder, **not the user's evidence work.** Recognizing it would fire for essentially everyone (trivializing recognition) and would attribute OSLO's work to the user (D187 — the same error the pre-activation gate prevents). The deep pass is OSLO's work, so it belongs in the **notification** lane ("Extended Analysis landed"), which it already fires — never a recognition.

Dimension-earned-through-evidence is **not** a firing moment (3 dimensions × shifting levels = fatigue + regression-prone); it lives on the History arc only. *(A broader redefinition of the maturity-stage model into an earned ladder is proposed separately — see `DECISION-PACKET-maturity-ladder.md`; on ratification the stage-based firing here folds into that ladder.)*

**Cadence — a milestone is a timestamped historical EVENT, not a revocable badge:** it fires **once, at first achievement, ever**; never re-fires; and there is **no code path that fires a "milestone lost" moment.** If the state later slips (a deeper read adds inference), that is the read maturing — drawn neutrally (D173c) — never "you lost it." Density target: ~4 moments over a project's life.

**The early-engagement curve — recognition is warm early, sparse later, WITHOUT a timer.** Rather than throttle by user-age (manipulative, and risks shaming a gap), OSLO recognizes **firsts**: the first occurrence of each genuine maturation act — `first-confirm`, `first-resolve`, `first-answer`, `first-reviewer-evidence`. A new user crosses many firsts in session one; each fires **once ever**, so density is intrinsically high early and **self-decays** to the sparse threshold-milestone set as the firsts are spent. The firsts are a **curated allowlist of real maturation acts** — never a UI event (first click / open / login / view), which would be engagement-hacking and would break ungameable-ness. A first is a **lighter** earned touch than a milestone (shorter, no woven marker). This gives three tiers by weight: the per-action **payoff** (exists), the **first-time** acknowledgment (the early density, new), and the sparse **milestone** (durable).

**Pre-activation is value-framed, NOT earned.** Before the user has done any work — the anonymous / pre-activation first run — the honest frame is **value** (what OSLO did: "read your plan in ~12s, surfaced N issues"), carried by the existing first-value / Fast-Pass path, **never** the earned accent. Earned recognition — "you did this" — begins only at the user's first real maturation act. Calling OSLO's output the user's achievement would break *"green where the user earned it"* (D187), so the earned toast is gated on `_firstValue()`.

**Presentation — a two-part rhythm, both `--earned` only:**
- the **crossing → a transient earned toast** (rides the notification lane in the earned treatment so it reads as recognition, not an alert; auto-dismisses);
- the **persistent acknowledgment → a `✓ largely grounded` marker woven into the read** (the grounding rollup at the foot of the CAF rows). The marker tracks **live state**, so it stays true only as long as the read is and quietly isn't there if the read slips — never a "you lost it" negative;
- the **durable record → the History arc.** A standalone card is **declined** as the default (closest to a reward-popup) and a dedicated milestones/achievements surface is **declined outright** (it reintroduces the gamification frame).

**Copy register — B (advisory / consequential):** names the consequence in professional terms, no flattery, no bare fact (e.g. *"Your read is largely grounded — its conclusions now rest on your evidence, not inference."*). The persistent marker stays plain (`✓ largely grounded`, no "earned" suffix, which edges toward the badge frame).

---

## Guardrails (executable — proven at runtime, `_assertMilestonesFireOnceAndEarnedOnly`)

- **Monotonic-with-work signals only** — grounding, confirmations, stage; **never the band.**
- **`--earned` only** (D187/D003) — the recognition toast wears the earned accent, never a severity/success token.
- **Fire-once** — a `MILESTONES_FIRED` record prevents re-fire; the guard proves the fired set does not grow on re-check.
- **No regression moment** — no code path clears a fired milestone or renders a negative recognition; the marker tracks live state and vanishes neutrally (D173c).
- **Probe-fenced (D182)** — both the milestone check and the earned toast consult `_probeActive()`; the self-check never fires one.
- **Seeded silently at boot** — milestones (and, for a returning user past first value, firsts) already achieved when the app opens are recorded without a toast (a returning user's already-grounded read is not a crossing they just made); only in-session crossings toast.
- **Firsts reward work, not clicks** — the first-time set is a curated allowlist of maturation acts; a guard rejects any first tied to a UI event, proves fire-once + probe-fence, and proves earned recognition never fires before first value.

---

## Governance

Lands as Class-A canon via `dl-land`, additive to D187 / D096–D101 / the maturity-stage model; supersedes nothing. Built + verified in the deliverable prototype (`slice-10-tiering-limits/prototype.html`, boot self-check **146/146**, 0 pageerrors; new guards `milestonesFireOnceEarnedOnly` + `firstsRewardWorkNotClicks` green). Covers both the threshold-milestone tier and the early-engagement first-time tier. AI drafted + built; **only the owner ratifies.**

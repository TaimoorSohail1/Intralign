# DL-195 — Adaptability: the outcome-checkpoint-optimization assessment (R2 State-1 keystone)

**Status:** ✍️ **Scribe-drafted 2026-07-26 — first design pass; key calls owner-ratified (Idris, Framework 001), rest pending.** The keystone capability for DL-194 State 1 (moment-in-time outcome integrity), and the resolution of DL-194 §5's scoping question. **Owner criterion: durability is the PRIMARY driver; simplicity is secondary.**
**⛔ Owner-ratified 2026-07-26:** (1) **Name = Adaptability.** (2) **Advisory depth = OSLO PROPOSES the specific checkpoints** for the plan — the fuller orchestration capability, not merely flag-and-recommend (see §4).

---

## 1. Scoping resolution — a standalone third integrity axis (durability-primary)
Decision, on durability first: **establish the INTEGRITY layer as a three-pillar model — Viability (CAF) · Grounding · Adaptability — where CAF is the *computation under* Viability, Grounding is its own pillar, and Adaptability is a new pillar peer to Grounding.** Adaptability is **not** a 4th CAF dimension and **not** a property buried in Feasibility.

**Why this is the most durable, not merely the simplest** — the tempting "most durable" option is a 4th CAF dimension (first-class, permanent, on equal footing with C/A/F). It is the *less* durable choice, for three structural reasons:

1. **It conflates two different *kinds* of assessment.** CAF grades the plan's **static soundness** — is it clear/coherent/feasible *right now*. Adaptability grades a **temporal/governance** property — can you see and correct the outcome *over time*. Forcing a temporal axis into a static-soundness framework blurs the one distinction the whole outcome-integrity reframe rests on (this is exactly why "outcome integrity" needed a name distinct from "read maturity"). A blurred core concept is the opposite of durable.
2. **It distorts the machinery it joins.** CAF dimensions compose into the maturity band and the limiter ("how mature is the read of feasibility"). Adaptability doesn't compose that way — it's "is the plan *structured* to adapt," not "how mature is our read of it." Bending it to fit the CAF band/limiter apparatus would deform both.
3. **Precedent already exists for a non-CAF integrity pillar.** Grounding was never a CAF dimension — it is its own axis (level ≠ trust), and it has held up. Adaptability takes the same, proven shape. Reusing an established structural pattern is more durable than inventing a 4th-dimension exception.

The three-pillar model is also the clean **anchor for State 2**: static *Adaptability* (is the plan structured to adapt) becomes live *adaptation* (are you adapting it) with no rework — the axis is already the right home. And it matches the actual algebra: outcome integrity = **Viability × Grounding × Adaptability** (three factors), so three pillars is the honest structure, not a convenience.

*(Simplicity — zero change to the CAF triple, one self-contained new module — is a real benefit, but here it's the consequence of the durable choice, not the reason for it.)*

**Name: Adaptability (owner-ratified).** "Can you see the outcome drift and correct it while runway still exists." The name spans the roadmap: the static assessment — *is the plan structured to adapt as the outcome reveals itself* — becomes live *adaptation* in State 2, so one word carries both states.

---

## 2. The three-pillar integrity model + composition (weakest-gates)
**Outcome integrity = Viability (CAF) × Grounding × Adaptability.** Three orthogonal pillars:
- **Viability (CAF)** — is the plan clear · aligned · feasible toward the outcome. *(existing)*
- **Grounding** — how much of that read is confirmed vs. inference (level ≠ trust). *(existing)*
- **Adaptability** — is the plan structured so the outcome is examinable and correctable over execution. *(NEW — this packet)*

They don't reduce to each other: a plan can be sound but ungrounded (untrustworthy read); sound + grounded but waterfall (unadaptable — drift only visible at the end). All three are required for integrity.

**Composition = weakest-gates (the limiter pattern, applied to integrity).** Integrity is *wholeness* — it is only as strong as its weakest pillar, so the integrity level = the **weakest** of the three, and the indicator **names** it. Not a weighted blend (that hides which pillar is weak — the level ≠ trust failure, generalized) and not a number (D183b). This is the simplest durable composition *and* the conceptually correct one for "integrity."
> e.g. *"Outcome integrity: Fragile — no outcome checkpoints; you'd only see drift at the end"* · or *"— most of it still rests on inference"* · or *"— Feasibility is thin."*

---

## 3. The Adaptability assessment — three static checks (moment-in-time, no telemetry)
All three are readable from the **plan structure** at analysis time — which is exactly why State 1 is reachable without the State-2 feedback loops.

1. **Outcome checkpoints defined & tied to leading indicators.** Does the plan name points during execution where the **outcome** is examined (leading indicators the outcome is materializing) — not only delivery/task milestones? *Low:* none (delivery milestones only). *High:* outcome checkpoints defined at multiple points.
2. **Runway — checkpoints early enough to correct.** Are the checkpoints positioned so drift is catchable **while there is still time/budget to adjust**? *Low:* the outcome only surfaces at/near delivery (waterfall — no runway). *High:* a first outcome-read well before the end, recurring.
3. **Correction linkage — each checkpoint has an adjustable lever.** Is each checkpoint tied to something the PM can actually change if it shows drift (scope · sequence · resource · approach)? A checkpoint with no lever is a *report*, not a *control*. *Low:* checkpoints with no defined response. *High:* each carries an adjustment path.

→ an **ordinal Adaptability band** on the same five-step grammar as CAF (e.g. Unstructured → Optimized), computed deterministically from the three checks. Legible (each check is shown as the "why"), never a number.

---

## 4. What it produces on-screen
- **Feeds the decomposed integrity indicator (DL-194 §3):** Adaptability is one of the three pillars weakest-gates chooses from and names.
- **When Adaptability is the limiter, OSLO PROPOSES the specific checkpoints** *(owner-ratified — the fuller capability, not merely flag-and-recommend)*. Not "define an outcome checkpoint" in the abstract — OSLO generates a concrete, plan-specific checkpoint proposal: **for each proposed checkpoint (a) what outcome leading-indicator to read, (b) when in the timeline (positioned for runway), and (c) the adjustable lever to pull if it shows drift.** The PM confirms/edits/declines each (OSLO advises, you decide). Example (DevNorth): *"Add a checkpoint at T-8 weeks: read registration pace + qualified-lead signal against the 450/pipeline target; if short, the lever is scope of outreach + sponsor-driven promotion."* This is the orchestration promise made concrete — OSLO helps *structure the plan to protect the outcome*, not just grade it. Ties to DL-193's exposure/leverage queue: an unadaptable plan is a high-exposure integrity threat, and the proposed checkpoints are its move.
- **Build implication (scope note):** proposing checkpoints means OSLO must *define candidate outcome leading-indicators for the plan* — which is **Requirement 1 of State 2, pulled forward but only statically.** R2 proposes *what to measure and when* (structure); State 2 wires up *live measurement* of those signals (the feedback loop). Clean split: R2 = design the checkpoints; State 2 = run them.
- **The "ongoing pending" state (DL-194):** high Adaptability means the plan is *set up* to be tracked; the tracking itself is State 2. So even at "Optimized," the indicator still reads moment-in-time with live tracking pending execution.

---

## 5. Durability rationale (primary), with simplicity as the secondary benefit
- **Durable (the driver):** three orthogonal, non-colliding pillars — Viability (CAF — the plan's static soundness), Grounding (trust), Adaptability (temporal). Each measures a distinct *kind* of thing, so the model stays conceptually crisp as the product grows; it reuses the proven "integrity axis outside CAF" pattern (grounding), so it doesn't deform CAF or its band/limiter machinery; it maps 1:1 to the orchestration concept (the lifecycle/drift axis CAF can't express); and it is the anchor State 2 plugs into with **no rework** (static adaptability → live adaptation). A 4th CAF dimension would have been *less* durable — a temporal concept jammed into a static framework (see §1).
- **Simple (secondary, a consequence):** because the axis is standalone, the CAF triple, bands, limiter, heat map, rows, tab, and guards are **untouched**. Build surface = (1) the Adaptability assessment (one self-contained module → one ordinal), (2) the weakest-of-three composition, (3) the indicator UI. Contained and testable in isolation — welcome, but not why the choice was made.

---

## 6. Ratified (2026-07-26)
- **Name = Adaptability.**
- **Advisory depth = OSLO proposes the specific checkpoints** (§4) — indicator/leading-indicator + timing + lever per checkpoint; PM confirms/edits/declines.
- **Band granularity = five-step**, on the *same* Fragile→Sound scale as Viability. Rationale: weakest-gates needs one commensurable scale so the min is apples-to-apples and the headline band inherits it with no translation layer (durability). The three checks are graded (checkpoint count + runway are spectrums), so they map onto 5 steps without false precision; the checks still show as the "why."
- **Fixture:** DevNorth (low Adaptability) stays the **primary** demo — it's where OSLO surfaces the gap and *proposes* checkpoints (the core new value). A **high-Adaptability variant** (a checkpoint-optimized plan, integrity gated by a different pillar) is a secondary **build task** for the high-end view.
- **Weakest-gates tie-break = foundation-first: Viability → Grounding → Adaptability.** Follows the logical dependency (a plan must be sound, then trusted, then steerable; don't optimize checkpoints on a plan that isn't sound/believed). Low-stakes — it decides only the one headline word; the underlying moves surface regardless. *(Possible later refinement, not R2: tie-break by which fix most reduces outcome exposure, per DL-193's leverage spine.)*
- **Checkpoint-proposal provenance = adopted.** A proposed checkpoint and its leading-indicator are OSLO *inference*, not fact — each carries the same From-OSLO / Confirmed-by-you provenance as any other inference and is confirmable. This keeps the propose capability inside the grounding model (no fabricated certainty).

**DL-195 is now fully specced.** Clear to sequence into the R2 build (DL-194 §4 dependency set).

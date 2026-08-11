# DL-194 — The outcome-integrity indicator: a three-state roadmap (read-integrity → moment-in-time outcome integrity → continuous outcome status)

**Status:** ✍️ **Scribe-drafted 2026-07-26 — pending owner ratification (Idris, Framework 001).** Supersedes the earlier "continuous drift detection" stub (that is now State 2 here). Origin: owner reframed the lead indicator toward an "outcome-okay" status and specified the conditions that make it honest.
**⛔ R2 SCOPE (owner-directed 2026-07-26):** **State 1 is committed to Release 2.** R2 will NOT ship until every dependency of State 1 is satisfied — the outcome-integrity headline reframe AND the outcome-checkpoint-optimization assessment capability (see §4/§5). State 0 is a build milestone *toward* State 1, not a ship target. State 2 (continuous status + feedback loops) stays **post-R2**.
**Relationship:** consumes DL-193 (outcome-integrity = CAF × grounding; exposure/leverage spine) and outcomeorchestration.org (integrity = "the work still serves the outcome"; drift = "execution looks healthy while the outcome degrades"; the discipline "sits above execution").

---

## 1. The governing principle (why this is doctrine-consistent, not a loophole)
OSLO's rule was never "don't forecast." It is **"don't fake confidence you haven't earned"** (D003/D183b — the anti-forecast doctrine). A one-shot "outcome okay" on a static plan is *unearned* → forbidden. The **same principle licenses an outcome status the moment it becomes *earned*** — grounded in real evidence, continuously re-measured, and conditional on adaptation. So the doctrine that bans the forecast today is what permits it once grounded. The whole roadmap is: **earn the confidence, then show it.**

Corollary — **the outcome status has its own grounding** (level ≠ trust, generalized): an "outcome okay" resting on weak proxy signals is *low-trust* and OSLO must say so, even when it's green. And its confidence is **bounded by two things it does not control**: how examinable the execution is, and whether the PM keeps adapting. OSLO's forecast is accurate *only while the PM keeps steering to stay aligned* — a **conditional, adaptive** read, never a fatalistic guarantee.

---

## 2. The three states of the indicator

### State 0 — Read-integrity (today, shipping)
- **What it reflects:** CAF (clear · aligned · feasible, as OSLO reads the plan) + grounding (how much confirmed). A fact about the **read**, not the outcome.
- **Honest framing:** "OSLO's read of your plan." (DL-193 Option A: ordinal band + grounding sub-line.)
- **Why not more yet:** OSLO has neither an outcome-checkpoint assessment, outcome telemetry, nor an execution feedback loop. Claiming "outcome" here would be unearned.

### State 1 — Moment-in-time OUTCOME integrity (near-term; a build, not a relabel)
- **What earns the "outcome" framing without feedback loops:** OSLO assesses whether **the plan is optimized for the outcome checkpoints OSLO defines** — i.e., is the plan *structured* so the outcome is examinable and drift is catchable during execution. This is a **static, plan-time property** OSLO can judge now; it is the plan-time proxy for §3's examinability requirement. A waterfall plan scores low here **even with high CAF** — which is exactly where outcome integrity diverges from read maturity.
- **What it reflects:** outcome integrity = **Viability (CAF) × Grounding × Adaptability**, as of this analysis.
- **Honest framing — the "pending" marker is load-bearing:** it is a **point-in-time posture** ("as of now, your outcome integrity is X, and your plan is/isn't structured to keep it that way"), explicitly **not** a claim the outcome will hold through delivery. **"Ongoing tracking begins at execution"** is a first-class state — that pending marker is what licenses the moment-in-time call to be honest (stops "Integrity: Sound" being misread as "you'll succeed").
- **The near-term unlock:** the **outcome-checkpoint-optimization assessment** — a new dimension in the read: *"is this plan structured to protect its outcome over its life?"* Until it exists, State 0 (read-integrity) remains the interim; the indicator cannot truthfully claim the outcome framing without it.

### State 2 — Continuous outcome status (pending; the destination)
- **What it reflects:** a **live, evidence-grounded, conditional** outcome trajectory — "on track *while you keep steering*; here's the drift, here's the runway to correct." This is drift detection (the old stub).
- **Requires two things OSLO doesn't have yet:**
  1. **An outcome-leading-indicator feedback loop.** Real-time signals monitoring **outcome** progress, not **delivery** progress. (Booked venue / on-schedule = delivery health; pipeline actually filling = outcome health. Drift = the first green while the second sags.) **Step one is a Clarity/Alignment task OSLO already does:** help the PM *define* the few leading indicators that would show the outcome materializing *before* delivery, and confirm they're aligned to the outcome (not vanity output metrics) — because an outcome you can't measure early can't be monitored.
  2. **An outcome-examinable execution.** Iterative/incremental structure so the outcome is readable *throughout*, with runway to correct — not exposed only at the end (waterfall). Where execution is opaque, OSLO **honestly caps its own outcome-confidence** (nothing to re-ground on).

---

## 3. Composition of the single indicator (don't blend — show the limiting driver)
The owner wants **one** indicator. Since integrity = Viability (CAF) × Grounding × Adaptability, a lone ordinal band that *averages* them hides which is weak (level ≠ trust, generalized). The clean form is the **limiter pattern applied to integrity**: **one ordinal level + the named driver holding it there** — e.g. *"Outcome integrity: Fragile — its checkpoints aren't defined"* or *"— because most of it still rests on inference."* Decomposed, so it reads as a summary, not an opaque score. Ordinal, never a 0–100 number/dial (still the D183b forecast-misread).

---

## 4. Sequencing & build implications — **R2 = State 1**
State 0 is a *build milestone*, not a ship. R2 ships when State 1 is whole.

**R2 dependency set (all required before R2 ships):**
1. **Outcome-checkpoint-optimization assessment** (the keystone) — the new capability that earns the "outcome" framing: does the plan define/optimize for the outcome checkpoints OSLO names, so the outcome is examinable and drift is catchable. (§5 scoping: new dimension vs property of Feasibility/Alignment.)
2. **The outcome-integrity headline indicator** — decomposed single indicator per §3 (ordinal level + named limiting driver across Viability · Grounding · Adaptability); replaces the read-maturity band framing.
3. **The read-panel reframe** (DL-193 increment 2) — the read leads with the integrity indicator; limiter → facet-diagnostic; next-move panel preserved as the action.
4. **The "ongoing pending" state** — always-visible affordance that this is a moment-in-time posture; live tracking begins at execution (State 2).
5. **Integrity-framed endpoint labels** for the ordinal band (doctrine-safe: grades the outcome integrity OSLO reads, not the outcome's fate).
6. **Tab relabel** — "Interpretation" → "Viability" (the CAF half, paired with Grounding).
7. **D183b reconciliation** — the band moves from read-maturity to moment-in-time outcome integrity; the reconciliation is: moment-in-time + ongoing-pending + decomposed + checkpoint-grounded + ordinal (never a 0–100 number).
8. **Guards** — for the new dimension, the decomposed indicator, and the pending state.

**Post-R2 (State 2):** the outcome-leading-indicator feedback loop (+ OSLO helping *define* those indicators) and outcome-examinable execution support → continuous outcome status / live drift detection. The largest lift; defines OSLO as an outcome **orchestrator**, not a plan-reader.

Each step only shows the confidence it has earned — the through-line from the interim build milestone to R2's State-1 finish line.

## 5. Open for ratification
- Confirm the three-state model and that **State 1 requires the checkpoint-optimization assessment** (not a relabel).
- Confirm the **decomposed single-indicator** form (§3) over a blended band.
- Confirm the **"ongoing pending"** state as a first-class, always-visible affordance in State 1.
- Whether §2 State-1's checkpoint-optimization is a **new CAF-adjacent dimension** or a **property of Feasibility/Alignment** (scoping call).

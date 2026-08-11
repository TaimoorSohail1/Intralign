# DL-193 — Priority re-anchor: the limiter governs the *read*, outcome-integrity de-risk governs the *queue*

**Status:** ⛔ **RATIFIED 2026-07-26 by Idris** (sole ratifier, Framework 001). §7 resolutions agreed inline; **reverses D184.3** (limiter-first lead → highest-leverage outcome-de-risk lead). Cleared for build. Continuous drift-detection split to **DL-194** (roadmap).
**Builds on / touches:** DL-192 (positioning — outcome risk is the value) · DL-190 (limiter standalone confirmation) · DL-189 (stageless, computed next move) · DL-191 (issue-forward lead) · CAF-definitions.md (Clarity/Alignment/Feasibility). 
**Origin:** owner re-opened the limiter construct — "is it the optimal way to inform read and issue priority?" — under a stated product goal: **the continuous orchestration of outcomes across the lifecycle**, i.e. enabling the PM to optimize plan/execution for **outcome de-risk**.

---

## 1. The product goal this is measured against (owner-stated + canonical)

**Outcome Orchestration** (per outcomeorchestration.org, adopted as the conceptual frame): *"the governance discipline for preserving **outcome integrity** as work scales — keeping the intended outcome clear, real, and feasible over time"*; *"the continuous governance of outcome integrity across dynamic work systems as conditions evolve."* It **"sits above execution"** and is **"not a replacement for project management or delivery control."**

**Outcome integrity:** whether *"the work still serves the outcome it was meant to produce"* as conditions change and assumptions break.

**Outcome drift:** the central threat — execution looks healthy (scope/schedule/activity on-track) while the outcome *"quietly degrades."* The discipline is *"catching drift while execution still looks healthy."*

**Operational definition of integrity for OSLO (from "clear, real, and feasible"):**
> **Outcome integrity = CAF (clear · coherent · feasible) × Grounding (real / evidenced), on the outcome-bearing path.**
An integrity threat is any CAF gap or grounding gap that reaches the outcome. Clarity = the outcome is well-defined; Alignment = the plan coheres toward it; Feasibility = it can actually be delivered; Grounding = the read of all three is evidence, not inference. ("Real" in the canon = grounded.)

**OSLO's role (custodial, resolves the DL-192 agency tension):** OSLO governs the *read* of outcome integrity **from above execution** — it keeps the PM's read true and their attention on the biggest threats to integrity. **The PM preserves integrity; OSLO is the custodian of the read, not the conductor of the project.** ("Orchestration" is safe as this internal governance frame; it stays wrong as the *external category term* — the market hears autopilot — so DL-192's "outcome-based risk intelligence" remains the outward label. No contradiction; a clean split.)

**Drift ⇒ maturity-not-health is a mechanism, not a preference.** A green RAG/health dashboard is precisely the instrument that *masks* drift (visible progress hiding erosion). OSLO's refusal of health/probability scoring (D003/D186c) is therefore the direct expression of the orchestration discipline, not merely house style.

---

## 2. What the limiter does today — its two jobs (verified in the build)

`_limitingOf(r) = _cafOf(r).sort(by band-weight ascending)[0]` — the **lowest-band CAF dimension**, computed, never typed. It drives two separable things:

1. **The read headline.** Names the weakest CAF dimension — the bridge from the read into the rows; keeps the read from standing bare.
2. **Issue/action priority.** Improve-stage `_beatOrder` sorts **limiter-first, then severity**; `_leadRecId` / `_recRankScore` lead with the recommendation that moves the limiting dimension (D184.3). Consequence: **a *moderate* issue on the limiter currently outranks a *critical* issue on a non-limiter dimension.**

(There is already inconsistency across surfaces: validate-stage order is *de-risk-first*, improve-stage is *limiter-first*, and the confidence hero sorts *pure severity* — three different notions of "priority.")

---

## 3. The finding — the limiter is strong at job 1, wrong-for-the-goal at job 2

**Keep it for the read (job 1).** A computed, single-word answer to "where is my read weakest?" is honest, legible, and fits a *maturity* model: understanding of the whole is gated by its weakest dimension. Under §1 it demotes cleanly to a **diagnostic: which facet of integrity — clear / coherent / feasible — is most compromised.** No change needed except its status (subordinate, not spine).

**Re-anchor the queue (job 2).** Limiter-first-then-severity was right when the frame was "mature the read." Under the orchestration goal it is wrong on three counts:
- **It contradicts the goal.** The goal is preserving outcome integrity / reducing outcome risk. Limiter-first can bury a critical, integrity-threatening issue under a moderate limiter issue — i.e. it does *not* lead with what most threatens the outcome (against DL-192 and §1).
- **It's internally mis-defined.** The limiter's own rationale is "lead the user to their weakest / least-certain point." But the limiter is a **band** fact, and DL-190 §2 establishes that certainty/trust is the **grounding** axis (a confirmation raises grounding without moving the band). So "least certain" is better served by grounding or by outcome-exposure than by lowest-band. Even on its own logic, lowest-band is the wrong definition of "weakest point."
- **It doesn't travel the lifecycle.** The limiter is a *planning-maturity* signal (CAF bands grade plan understanding). It has no natural meaning in execution, where integrity is threatened by **drift** — the very thing the goal centers on. Outcome-integrity de-risk is defined at *every* phase; the limiter is not. Continuity across the lifecycle is the strongest reason to move the queue off it.

---

## 4. The decision (proposed)

**Re-anchor priority to outcome-integrity de-risk. Demote the limiter to a diagnostic. Two layers, never conflated:**

- **D1 — Exposure is the visible risk map (surfacing layer).** OSLO surfaces *what threatens the outcome and how much* — the integrity/drift map — ranked by outcome-exposure. This map stays **complete and visible**; a high-exposure item is **never hidden**. (Maps to DL-192's "shows you what threatens your outcome," verbatim.)
- **D2 — Leverage orders the recommended next move (action layer).** The lead move is the one that **most reduces outcome risk *and* is actually actionable** — de-risk leverage = outcome-exposure among items that have a real move (`apply`-able), on the outcome-bearing path. This replaces limiter-first-then-severity as the queue's sort key.
- **D3 — Leverage guides, it does not gatekeep (NON-NEGOTIABLE — the advise-don't-decide line).** Leverage orders the *recommended* next move; it may **never suppress** a high-exposure item from the visible map. OSLO must not silently decide a large threat is "not worth addressing" — that overclaims agency and can hide something the PM could act on. Surface the threat; recommend the highest-leverage move; the PM decides.
- **D4 — Legibility (doctrine-safe).** Leverage is an **ordering rendered as the load-bearing story** ("your outcome leans hardest on this; here's the move that settles it"), **never a magnitude/score.** The moment it becomes a number it reads as health/probability (forbidden). The reveal's propagation model (`_grExpo`) is the computed, legible basis; recommendations already gate on `apply`.
- **D5 — The limiter stays, demoted.** It remains the read's headline and the "which facet of integrity is most compromised" diagnostic; it becomes a **secondary tie-break** in the queue, not the primary sort. CAF answers *why* the outcome is exposed; grounding answers *how sure* that read is ("real"). Limiter ≠ spine.

**One line:** *outcome-integrity de-risk is the spine; the queue ranks by highest-leverage de-risk move (exposure stays the visible map); CAF/limiter and grounding become the "why" and "how-sure" diagnostics beneath it — lifecycle-portable by construction.*

---

## 5. What reverses / what holds
- **Reverses D184.3** ("across issues, the lead recommendation is the one that moves the limiting dimension"). The lead becomes the highest-leverage outcome-de-risk move. **Flagged for explicit owner ratification** — this is the ratified clause being overturned.
- **Reframes DL-190** (limiter standalone confirmation): still valid, but re-expressed as "the highest-leverage un-flagged integrity threat on the outcome path" rather than "the limiter's standalone support." May generalize beyond the limiter dimension. Needs re-derivation in the new model.
- **Holds:** DL-192 positioning (outcome risk = value; grounding = trust); level ≠ trust; maturity-not-health (D003/D186c — now justified by drift); confirmIsTheVerb; brand-orange-actions-only; OSLO-advises-you-decide (strengthened by D3).

## 6. Guard implications (to design during build)
- **New — leverage-orders-the-queue.** The lead move is the max-leverage `apply`-able item on the outcome path, computed from state; assert it is *not* simply limiter-first, and that it degrades sensibly when no item is actionable.
- **New — exposure map is complete (the no-gatekeep lock, D3).** Assert no high-exposure item is ever suppressed from the visible map by the leverage ordering. This is the doctrinal spine of the change.
- **Rework — `_assertStartHereFollowsTheBeat` / the DL-190 limiter-scope locks.** These encode limiter-first; they must be re-expressed for the leverage model or they will (correctly) fail.
- **Keep — no-magnitude / no-health / no-fabricated-count.** Leverage must never surface as a number (D4).

## 7. Resolutions (agreed with owner 2026-07-26 — binding)

1. **Exposure model — propagation topology YES, `_grExpo` quantity NO.** `_grExpo(n)` measures the fraction of a node's leaf-descendants still `inferred` — a **grounding/coverage (trust)** measure, the same one that paints the reveal's "hollow" nodes. Adopting it as outcome-exposure would re-conflate level ≠ trust. **Reuse the reveal's propagation *mechanism* (uncertainty aggregates upward toward the outcome); change the quantity flowing through it to integrity-threat.** Outcome-exposure of an issue = **severity (threat magnitude) × structural reach toward the outcome**, with **grounding as a modifier** (an inferred load-bearing threat scores higher — the false-confidence premium — but grounding sharpens exposure, it does not define it). **Two-step delivery:** ship the **legible proxy now** — severity (the outcome-threat floor) among actionable items, boosted when the issue reaches the outcome (spans Alignment / carries a load-bearing support on the outcome path), grounding as modifier — and flag the **full propagation model** for when a real issue→outcome mapping exists to compute reach honestly (the fixture's issue/CI graph has no explicit outcome path like the reveal's synthetic tree). Don't claim a model we can't compute truthfully.
2. **Leverage form — exposure among actionable, ordered, rendered as the story. NO "estimated integrity restored."** The composite (weight by integrity actually restored) is unshowable, drifts to opaque-magnitude/health-score, and has OSLO estimating value the PM should judge. Tie to **D3**: actionability orders the *recommended next move*; it never removes a threat from the visible map. A large but currently-unactionable threat keeps its true rank on the map; it just isn't the recommended move.
3. **Read headline — lead with the outcome-integrity threat; demote the limiter to the facet-diagnostic.** The read leads with what most threatens the outcome (exposure-forward); the limiter becomes "which facet of integrity — clear / coherent / feasible — is most compromised," shown beneath. **Anti-drift credibility is preserved by riding maturity + grounding *inline on every threat*** ("here's what most threatens your outcome — and how well-understood and evidenced that read is"), not by keeping the limiter as the marquee. Consistent with the reveal reframe (lead with the threat; grounding/maturity as mechanism) and DL-192 (value leads, credibility beneath). The limiter word survives as a diagnostic detail.
4. **Drift/lifecycle — SPLIT to DL-194 (roadmap).** Continuous integrity preservation needs change/drift detection over time (temporal state, "execution looks healthy while the outcome degrades") — a larger build than re-anchoring a snapshot's priority. DL-193 stays the snapshot priority re-anchor; **DL-194** opens continuous drift detection, named now as the direction the orchestration concept points (drift-catching is its core).

## 8. Validation — fixture head-to-head (RUN 2026-07-26)

Ran limiter-first-then-severity vs a leverage proxy (most outcome-threatening, actionable, **dimension-agnostic**) against the live fixture. Real limiter = **Feasibility** (bands: Clarity 76 · Alignment 55 · Feasibility 30). Both critical issues (ISS-01, ISS-07) are Feasibility.

**① Today they nearly agree** — both lead **ISS-01 [critical/Feasibility]**; they differ only mid-order (limiter-first clusters the Feasibility *moderates* ISS-03/04 ahead of the Clarity moderate ISS-02). So on the current screen the model looks fine — **but only because the limiter happens to coincide with the critical issue's dimension.**

**② Under limiter rotation, it breaks — and rotation is *earned progress* (DL-190).** As Feasibility issues resolve, its band rises and the limiter rotates to **Alignment**. Limiter-first then leads with **ISS-05 [moderate/Alignment]** and drops **ISS-01 [critical/Feasibility] to #2** — a *moderate* issue over a *critical* outcome threat.

**③ Structural worst case (limiter = Clarity):** limiter-first leads **ISS-02 [moderate]** then **ISS-06 [warning]** *ahead of* **ISS-01 [critical]** — a **warning-level** issue outranking a **critical** one, purely by dimension membership.

**Leverage keeps ISS-01 [critical] at #1 in all three.** 

**Conclusion:** the current construct is correct *by coincidence* (limiter == critical dimension) and becomes wrong *precisely as the user succeeds* (rotation surfaces a moderate, or even a warning, over a critical outcome threat). This is the pathology §3 predicted, realized on the real fixture — the change earns itself. **Caveat:** the proxy is severity-among-actionable, a floor stand-in for true outcome-exposure; a propagation model (§7.1) would refine *mid-order*, but the headline (never bury a critical under limiter membership) holds under any reasonable exposure measure, since severity is a lower bound on outcome-threat.

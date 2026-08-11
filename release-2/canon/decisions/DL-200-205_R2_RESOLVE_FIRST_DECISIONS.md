# R2 Resolve-First Decision Records — DL-200…DL-205 (drafts for ratification)

*2026-08-04 · Formal capture of the six DR rulings from `R2_RESOLVE_FIRST_DECISION_BRIEF.md`. **Framework 001: AI-drafted; Idris ratifies.** All staged in `release-2/`, withheld from `main` until R1 graduation. Each section can split into its own `DL-2xx_*.md` on landing. Numbers **198/199 are the ratified collision renumbers** (freemium DL-172 → **DL-198**, owner-activation DL-173 → **DL-199**; ratified 2026-08-04 per the re-adjudication worksheet). DR-7 (pricing) is now **RATIFIED** (Idris, 2026-08-04) in its own file `DR-7_PRICING_RATIFICATION.md`.*

---

## DL-200 — The AI-first prototype is the canonical R2 source of truth (+ DL-164…197 re-adjudication)

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (governance / source of truth) · **Framework 001.**
- **Basis:** `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md` §1 (the two-lineage divergence) + `R2_DL_READJUDICATION_WORKSHEET.md`.

**Decision.** `oslo-prototype-r2.html` (the AI-first prototype) is the single canonical R2 source of truth for the build. The earlier R2 "canon track" (`prototype-r2_15.html` + DL-164…197) is **re-adjudicated against it** per the ratified worksheet: **28 carry/carry-mods (incl. DL-165 → carry-mods: explainer intent onto the integrity band), 3 supersede (DL-176, DL-178, DL-194 drift-stub), 1 defer (DL-180 two-layer optimize web — post-R2/optional), 2 renumber (the newer Lineage-B pair: freemium DL-172 → DL-198, owner-activation DL-173 → DL-199).** The integrity core — DL-193/194(indicator)/195/196/197 + the two drafts — **carries** as the ratified specification of the three-pillar model, to be implemented in the AI-first shell.

**Why.** Two lineages had diverged (the AI-first prototype does not implement the DL-196/197 issue layer) and collided on decision numbers (DL-172, DL-173). A developer cannot build against two contradictory sources. Declaring one source and adjudicating the other is the prerequisite to every downstream contract; it also converts the audit's "undefined" integrity gaps (OI-3/OI-4/OI-7) into "carry the existing canon spec."

**Supersedes / affects.** Reclassifies DL-164…197 dispositions per the worksheet. Supersedes DL-176, DL-178, DL-194(drift-stub). Triggers the DL-172/DL-173 renumber.

**Preserves.** All product doctrine unchanged (this is a governance decision).

---

## DL-201 — Unit of persistence: the Outcome, first-class above the Plan

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (data-model identity) · **Framework 001.**
- **Basis:** decision brief DR-2; extends **DL-198 (freemium, unit = outcome; renumbered from DL-172)**.

**Decision.** The **Outcome** is a first-class, persisted, metered object.
1. Hierarchy: **Workspace → Plan → Outcome** (the Plan is the outcome's container).
2. Cardinality: **Free = 1 active Outcome : 1 Plan** (narrow); **Basic+ = N outcomes per plan and N plans.**
3. This **supersedes** R1's "outcome = Canonical Fact" / "`Intend` — do not add in R1" for the *metered* unit (the alignment-reference Canonical Fact may remain).

**Why.** DL-172 ratified the outcome as the unit of value; the persistence model must follow, or metering, archive/reactivate, sharing scope, and the roll-up have no object to act on.

**Preserves.** The outcome's **record is never metered** — archive keeps it fully viewable.

**Affected artifacts.** R2 data/object model; the freemium entitlement model (DL-202); sharing scope + roll-up aggregation.

---

## DL-202 — Freemium enforcement in Alpha: the commitment gate *(supersedes DL-172's non-gating stance)*

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (freemium strategy) · **Framework 001.**
- **Basis:** decision brief DR-3. **Supersedes** the non-gating clauses of **DL-198 (freemium; renumbered from DL-172)**.

**Decision.** Paid capabilities are **gated in Alpha**, via a **commitment gate**:
1. At a wall: **block → show the named capability + price → the user commits to pay** (hosted checkout captures a real card) **→ grant access.** Full subscription lifecycle (proration, dunning, self-serve plan changes) is deferred.
2. This **deliberately supersedes** DL-198's (freemium) "nothing gated in Alpha," "intent-capture only (VM mirrors)," and "neutral copy / premature pricing." It **re-aligns** R2 with R1's existing gating canon (the `422` limit, the upgrade/checkout funnel, the upgrade-intent score).
3. **Gate only scope/capacity capabilities** — 2nd outcome, 2nd plan, bigger intake envelope, auto-import, continuous monitoring.
4. **Never gate** — the append-only record, the reviewer/CRR loop, Viewers, or **judgment quality** (one accuracy bar for all).
5. Creates open decision **DR-7 (pricing)**: a named paid tier + a price. Tier names + capability→tier mapping already exist (DL-198 ladder); the price number is the open piece. Price is **config** for the build; it blocks user-facing copy + launch, not the architecture.

**Why.** Passive intent logging shows that users *clicked*; only a real gate plus a genuine chance to pay reveals whether they'd *pay*. Earned access is the truer willingness-to-pay signal, and Alpha exists to learn exactly that.

**Preserves.** The honesty hard-lines: judgment quality is never tiered; the record, reviewer loop, and Viewers are never metered. The gate is about **capacity/scope**, never the quality or integrity of the read.

**Affected artifacts.** The prototype's freemium layer (VM-1a/1b/2 intent mirrors, `_INTENT_LOG`, `_recordIntent`, neutral copy) is **reworked into real gates + commitment checkout + named/priced copy**; the entitlement model; `oslo-backend-capabilities.md` #16.

---

## DL-203 — The Outcome-Integrity computation model (three pillars, weakest-gate)

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (the core assessment model) · **Framework 001.**
- **Basis:** decision brief DR-4a/b/c. **Consolidates/ratifies** DL-193, DL-194 (indicator), DL-195, DL-196, DL-197, and the "collapse Outcome-Confidence into Viability" draft, reconciled to the AI-first spine.

**Decision.**
1. **Weakest-gate composite.** Outcome Integrity = **min(Viability, Grounding, Adaptability)**. This **supersedes R1 Confidence-Model IR-4 (not-weakest-link) and IR-8 (non-collapse) at the composite level only.** Each pillar's *internal* computation still obeys R1's "between average and minimum." The output is a **word-band maturity read, never a number/%/probability**; a "Very Low" always presents as "your weakest pillar is X — here's the worklist," never a health/RAG verdict.
2. **Adaptability = a distinct pillar** (not a property of Feasibility). Ordinal maturity from **outcome-checkpoint coverage** (per DL-195) against OSLO-identified critical decision/drift points; **never a "% protected."** A simpler, honest v1 (checkpoint presence/coverage) is permitted if the full checkpoint-optimization model isn't build-ready, with the full model (DL-195) as the follow-on.
3. **Grounding = a distinct gating pillar.** The **pure share of load-bearing details resting on confirmed evidence vs. OSLO's inference.** It **can drive the composite down (supersedes IR-8).** Assessability/coverage, if surfaced, rides alongside as a **non-gating qualifier**, never an input to the gate.
4. **Viability = the CAF composite** (the old single "Outcome Confidence" collapses into this pillar — lands the collapse draft). Its internal math is R1 CAF/Confidence V2; remove any evidence-free band bumps (a band never rises without new evidence).

**Why.** Integrity is only as trustworthy as its weakest load-bearing dimension; averaging would let a strong pillar mask a fatal weak one — the exact false-confidence failure DL-197 exists to catch. R1's non-collapse rules were written for a single-score model with Reliability as a qualifier; R2 re-conceived the pillars as gates, so the min() is appropriate and the R1 constraint no longer transfers.

**Preserves.** No forecast/probability (D003/D183b); maturity ≠ health; "OSLO advises, you decide."

**Affected artifacts.** The R2 scoring/integrity spec; the issue-layer implementation (DL-196/197) in the AI-first prototype; `oslo-backend-capabilities.md` #7; audit OI-1…OI-8.

---

## DL-204 — Issue lifecycle: the phased resolution model + the D088 amendment

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (issue lifecycle) · **Framework 001.**
- **Basis:** decision brief DR-5. **Lands** the ratified `DL-DRAFT_phased-resolution-model` (2026-07-30) and **amends D088.**

**Decision.**
1. The issue lifecycle is **Inferred → Settled → "Settled — needs a fix" → Resolved.** Every item is first **Settled on Grounding** (its truth is known), then either resolves or **forks to "Settled — needs a fix"** when the confirmed truth exposes a Viability gap requiring a plan change; it reaches **Resolved only after the plan changes and re-analysis confirms it.**
2. **Amend D088:** only **re-analysis** moves an item to a resolution state — never the click handler. Map the prototype's `inf/routed/addressed/you/fixed` onto the phased states.

**Why.** The prototype's model lets a confirmed-yet-infeasible item read "Resolved" — false confidence at the issue level, the same failure DR-4 eliminates at the band level. The phased model maps 1:1 onto the Grounding-then-Viability pillar split, so it's required for consistency with DL-203.

**Preserves.** "Only re-analysis resolves"; the append-only record; honest resolution.

**Affected artifacts.** R2 state model; the attestation/basis schema; `oslo-backend-capabilities.md` #1/#2; audit R2-I1/R2-I2.

---

## DL-205 — Activation metric: Activated = the second grounding act *(amends DL-173's "first act")*

- **Date:** 2026-08-04 · **Status:** Draft → Ratified (Idris) · **Class:** A (the activation metric) · **Framework 001.**
- **Basis:** decision brief DR-6. **Amends DL-199 (owner-activation; renumbered from DL-173)** — from "first grounding act" to "the second (the unlock)."

**Decision.**
1. **Activated = the second grounding act** (the freeze-unlock / payoff moment).
2. Instrument **three milestones off one durable `grounding_act` event stream:** **Initiated** (1st act) → **Activated / Unlocked** (2nd act) → **Engaged** (an act past unlock; the readiness-survey trigger bar).
3. A **route counts** as a grounding act (per DL-199's symmetry point); this **supersedes** the telemetry spec's "Activated = score_viewed."
4. Activation is **derived from the event**, not hard-wired to the first-run freeze (so it holds for a returning user opening a new outcome). The activation event is **immutable once emitted** — a later withdraw may re-lock the live gate but never deletes the event.

**Why.** One grounding act can be a curious poke; two is real work, and the second act is the unlock — the moment the product visibly delivers value. Instrumenting all three milestones keeps the 1→2 drop-off (the biggest first-run leak) visible instead of collapsing it into one number.

**Preserves.** Confirm/flag/route symmetry (D133); honest delegation (route = an owner's activation); append-only record.

**Affected artifacts.** The `grounding_act` event; the freeze/unlock state contract; the readiness-survey trigger; funnel telemetry; audit R2-RE-4/FB-G7/FB-G10.

---

## Resolved
- **DR-7 (pricing).** ✅ **RATIFIED (Idris, 2026-08-04)** — see `DR-7_PRICING_RATIFICATION.md`. **Basic = $29/mo flat per account** (annual $290/yr, 2 months free); placeholder dropped in the prototype. **Pro = $79/mo provisional** (post-R2 capabilities; revisit at launch, consider ~$69). Model is **flat, never per-seat** (doctrine — reviewers/Viewers free forever). Closes the last open Resolve-First item.

## Ratification
- Accept DL-200…205 as drafted? (or amend which) ____________________
- Split into individual `DL-2xx_*.md` files on landing? ______ · Date: ______ · Idris

# R2 Resolve-First Decision Brief — unblock product-grill

*2026-08-04 · Companion to `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md` (§5). Six decisions that must be ruled before the product-grill can turn R2 gaps into vertical slices. **Framework 001:** the options below are AI-drafted; only the owner (Idris) ratifies. Each item has a recommendation, the trade-offs, the doctrine check, what the ruling unblocks, and a ratification line to fill in.*

**How to use:** walk top to bottom. **DR-1 is the master gate** — the other five inherit its ruling. For each, either accept the recommendation or pick an alternative; record the ruling in the block at the bottom of the item. When all six are ruled, product-grill has a single, non-contradictory source of truth to slice against.

**Dependency order:** DR-1 → (DR-2, DR-3, DR-4, DR-5, DR-6 can then be ruled in any order; DR-6 lightly depends on DR-5's state names).

---

## ✅ RATIFIED DECISIONS — 2026-08-04 (Idris) — authoritative

*This block is the record of ruling. Where a per-section draft recommendation differs from the ruling (DR-3, DR-6), the ruling here governs.*

- **DR-1 = AI-first prototype is canonical.** `oslo-prototype-r2.html` is the R2 source of truth; DL-164…197 are re-adjudicated against it (carry / supersede / renumber). *Follow-on: the re-adjudication worksheet.*
- **DR-2 = Outcome is first-class, above Plan.** Workspace → Plan → Outcome; **Free = 1 active Outcome : 1 Plan**, Basic+ = N/N. Supersedes R1 "outcome = Canonical-Fact / Intend do-not-add" for the metered unit.
- **DR-3 = ENFORCE, via a commitment gate** *(override of the draft's "observe-only")*. Paid capabilities are **gated** in Alpha: block → show the named capability + price → user commits to pay (hosted checkout captures a real card) → grant access; defer full subscription lifecycle. **This deliberately supersedes DL-172's "nothing gated in Alpha," "intent-capture only," and "neutral copy / premature pricing" clauses.** Re-aligns R2 with R1's existing 422 + checkout + upgrade-intent-score canon. **Hard-line preserved:** gate only *scope/capacity* capabilities (2nd outcome, 2nd plan, bigger envelope, auto-import, continuous monitoring) — **never** the record, the reviewer/CRR loop, Viewers, or judgment quality. **New open item it creates → DR-7 (pricing).**
- **DR-4a = Weakest-gate wins.** Composite integrity = min(Viability, Grounding, Adaptability), superseding R1 IR-4/IR-8 at the composite; each pillar keeps R1's "between average and minimum" internally; maturity-not-forecast framing mandatory.
- **DR-4b = Adaptability is a distinct pillar.** Ordinal maturity from checkpoint coverage vs. OSLO-identified drift points; never a "%"; phased/simpler v1 computation allowed if the full checkpoint model isn't build-ready.
- **DR-4c = Grounding is a distinct gating pillar.** Pure grounded-vs-inferred share of load-bearing details; supersedes IR-8 at the composite; assessability (if surfaced) rides alongside as a **non-gating** qualifier.
- **DR-5 = Phased issue lifecycle.** Inferred → Settled → "Settled — needs a fix" → Resolved; map the prototype's states onto it; land the D088 amendment ("only re-analysis resolves").
- **DR-6 = Activated = the 2nd grounding act (the unlock)** *(amends the draft's "first act")*. Instrument three milestones off one `grounding_act` event stream — **Initiated** (1st act) → **Activated/Unlocked** (2nd act) → **Engaged** (act past unlock; the readiness-survey bar). Route counts as an act (DL-173); supersede "score_viewed"; activation is derived from the event, not hard-wired to the first-run freeze.

### New decision this session created
- **DR-7 (pricing) — OPEN.** A real commitment gate (DR-3) needs a **price** and at least one **named paid tier**. Tier names + the capability→tier mapping already exist (DL-172's ladder); the open piece is the **price number(s)**. Does **not** block product-grill's architecture (build price as config), but **does** block user-facing paywall copy and launch. Recommend a dedicated pricing decision before launch.

### Canon actions that follow (Framework 001 — draft → you ratify)
These rulings should be captured as ratified decision records: a governance DL (DR-1 + the re-adjudication), a freemium-strategy DL **superseding DL-172's non-gating/neutral-copy clauses** (DR-3), the integrity-model DL (DR-4a/b/c), the issue-lifecycle DL + D088 amendment (DR-5), and the activation-metric DL **superseding DL-173's "first act"** (DR-6).

---

## DR-1 — Declare the canonical R2 source of truth *(master gate)*

**The question.** R2 exists in two divergent, colliding lineages (audit §1). Which is the go-forward source a developer builds from — and what happens to the other's ratified decisions?

**Why now.** A dev told "build from the prototype and the DLs" today has two contradictory truths: the AI-first prototype (`oslo-prototype-r2.html`) does **not** contain the DL-196/197 issue-layer that those ratified decisions call "built," and DL-172/DL-173 each name two different decisions. Every other gap inherits this ambiguity; nothing downstream is estimable until it's settled.

**Options.**
- **A — AI-first prototype is canonical; re-adjudicate DL-164…197 against it *(recommended)*.** `oslo-prototype-r2.html` (already promoted to official, your designated primary build file) is the source of truth. Every DL-164…197 is then re-adjudicated: **carry** (rebuild + re-verify in the AI-first model), **supersede** (retire, with a note), or **renumber** (end the collision). Likely carries: the issue-layer *as the backend model* (DL-196) and the graph schema (DL-184) even though the AI-first UI simplified them; likely supersedes: canon-track first-run/reveal specifics replaced by the AI-first reveal.
- **B — R2-canon track is canonical.** Keep `prototype-r2_XX` + DL-164…197 as the truth; treat the AI-first candidate as exploration to fold back. Preserves the DL-164…197 investment but discards the AI-first reimagining you promoted and the freemium/feedback work built on it.
- **C — Split by layer.** AI-first is the product/UX shell; named canon decisions (DL-184 graph schema, DL-196 issue layer, DL-197 false-confidence) are imported as the backend architecture beneath it. In practice this is Option A with a pre-committed "carry" list.

**Recommendation: A.** It matches your stated intent ("convert this candidate to the official R2 prototype… my primary file"), and it's the only option where the freemium + feedback + survey work already built has a home. The re-adjudication pass is where A absorbs the best of B/C — it is not "throw away DL-164…197," it's "decide each one deliberately against the new model."

**Doctrine check.** Neutral — this is a governance/traceability decision, not a product-doctrine one.

**Unblocks.** Everything. Also defines a concrete follow-on task for product-grill (or a DL-sweep): the carry/supersede/renumber adjudication of DL-164…197.

**Ratification —** Decision: ____________________  · Re-adjudication owner/when: ____________  · Date: ______ · Idris

---

## DR-2 — Unit of persistence: promote Outcome above Plan

**The question.** Is the **Outcome** a first-class persisted object, and what is the Outcome ↔ Plan ↔ Workspace hierarchy and cardinality?

**Why now.** DL-172 already ratified the *outcome* as the unit of value, but R1's data model persists a flat **Project** and explicitly says "do not add an `Intend`/outcome object in R1." Metering, archive/reactivate, sharing scope, and the roll-up all hang off what the persisted unit is. Undefined → nothing to count, cap, rotate, or aggregate.

**Options.**
- **A — Promote Outcome to first-class, above Plan *(recommended)*.** Hierarchy **Workspace → Plan → Outcome**; cardinality **Free = 1 active Outcome : 1 Plan** (narrow), **Basic+ = N Outcomes/Plan and N Plans**. Reverses the R1 "Intend deferred" call for the metered unit (the alignment-reference Canonical Fact can remain).
- **B — Keep Plan/Project as the unit; "outcome" is a label/attribute.** Least disruption to R1, but contradicts DL-172 and leaves the freemium metering with nothing real to meter.

**Recommendation: A**, with your confirmation of the exact cardinality wording above — that specific hierarchy is genuinely yours to set, and the whole freemium/roll-up model keys off it.

**Doctrine check.** The Outcome's **record is never metered** (archive keeps it fully viewable); confirm the promotion doesn't introduce any per-outcome record limit.

**Unblocks.** Freemium entitlement model (DR-3), archive/reactivate contract, sharing scope, owner roll-up aggregation.

**Ratification —** Decision (incl. cardinality): ____________________ · Date: ______ · Idris

---

## DR-3 — Enforcement mode (Alpha: gate or observe?)

> ▶ **RULED: ENFORCE, via a commitment gate.** The owner chose to gate paid capabilities in Alpha — a paywall as *earned access*, to measure real willingness-to-pay. The "observe-only" recommendation drafted below is **superseded**; the reasoning is retained for context, and the R1-gating-landmine it describes is now a *re-alignment*, not a thing to suppress. See the ratified block above and DR-7 (pricing).

**The question (as originally drafted).** In Alpha, do freemium "walls" actually gate, or only capture intent?

**Why now.** This is the single highest-risk build error. R1 canon *actively specifies hard gating* — `POST /projects → 422` at the second project (UP-3), `429` caps, and an `upgrade_page_viewed → started → completed` checkout funnel. A developer handed R1 canon + R2's prose **builds the 422 gate by default**, directly violating "nothing gated in Alpha."

**Options.**
- **A — `enforcement_mode ∈ {observe, enforce}`; Alpha ships `observe` *(recommended)*.** Entitlement checks evaluate, **emit the intent signal, and always return allow**. R1's 422/429 gates + checkout funnel are explicitly marked **superseded-in-Alpha**; `enforce` is built but latent for post-Alpha.
- **B — Build enforcement now.** Gates at the second outcome. Violates doctrine; also wrong for an Alpha whose purpose is to *measure* demand, not convert it.

**Recommendation: A** — doctrine-mandated. Write "superseded-in-Alpha" loudly next to the R1 gate specs so no one wires them.

**Doctrine check.** Directly serves "nothing gated in Alpha." Pair with the **never-metered exemption list** (record, reviewer/CRR loop, Viewers) so "entitlement checks" don't accidentally meter the growth engine.

**Unblocks.** The entitlement data model, the intent-signal stream, and the whole freemium slice.

**Ratification —** Decision: ____________________ · Date: ______ · Idris

---

## DR-4 — The Outcome-Integrity computation model

The three-pillar model (Integrity = weakest of Viability, Grounding, Adaptability) is positionally ratified but not specified as a *computable* model, and it collides with R1's ratified scoring rules. Three sub-decisions:

### DR-4a — The `min()` pillar gate vs R1 non-collapse
**Question.** R2 makes Integrity the **minimum** of the three pillars. R1's Confidence Model forbids exactly this (IR-4: "not weakest-link"; IR-8: "reliability alone must not drive the band to Very Low"). Which governs?
- **Recommended:** Ratify the `min()` pillar gate as a **new construct that supersedes IR-4/IR-8 for the composite only** — while Viability's *internal* CAF consolidation still obeys IR-4 (between average and minimum). Preserve the maturity-not-forecast framing so a gate to "Very Low" reads as "weakest pillar," never health/RAG.
- **Alternative:** Keep IR-4/IR-8 (no hard gate) — but then the "weakest-gate" story the whole R2 model rests on doesn't hold.

### DR-4b — Adaptability: new dimension or property of Feasibility?
**Question.** DL-194 §5 left this open. Adaptability = "is the plan structured so the outcome stays examinable and drift is catchable?"
- **Recommended:** A **distinct pillar** (the model already surfaces it as one), computed from outcome-checkpoint coverage against OSLO-identified critical decision/drift points — expressed as an **ordinal maturity** read ("can it catch drift"), never a "% protected" (which would be a forecast).
- **Alternative:** Fold it into Feasibility/Viability — simpler, but collapses the three-pillar story to two.

### DR-4c — Grounding: re-homed R1 Reliability, or a distinct measure?
**Question.** Is the Grounding pillar R1's Reliability moved over (which by IR-8 must never collapse the band), or a distinct grounded-vs-inferred measure that *is* allowed to gate?
- **Recommended:** A **distinct first-class pillar** = the share of load-bearing details resting on confirmed evidence vs. inference; explicitly note it **supersedes IR-8** as a gating pillar. State whether coverage/assessability also feed it.

**Doctrine check (all three).** The output must stay a **word-band maturity read, never a number/%/probability** (D003/D183b). The prototype's anti-forecast surface copy is strong; the risk is entirely in the computation beneath — keep it ordinal, and remove the prototype's evidence-free "+1 band on 2 fixes" bump (a band must not rise without new evidence).

**Unblocks.** The band-threshold spec, the issue→pillar function, the false-confidence type, and the reanalysis event→pillar table.

**Ratification —** 4a: __________ · 4b: __________ · 4c: __________ · Date: ______ · Idris

---

## DR-5 — One issue lifecycle (and land the D088 amendment)

**The question.** Which issue lifecycle is canon for the build?

**Why now.** Three incompatible vocabularies are live: the prototype's `inf/routed/addressed/you/fixed`, R1's finding lifecycle, and the **ratified-but-unbuilt** phased model. The prototype treats "grounded" and "plan-fixed" as *mutually exclusive terminal states* — so an item you confirm that turns out genuinely infeasible reads as "Resolved." The ratified phased model was written specifically to kill that dishonesty.

**Options.**
- **A — The phased model: Inferred → Settled → "Settled — needs a fix" → Resolved *(recommended)*.** Every item touches Grounding, then (if needed) Viability, in sequence, with an explicit settled-but-unresolved fork. Land the D088 amendment. This is the honest lifecycle and it's already ratified in draft.
- **B — The prototype's 5-state as-is.** Simpler to build from what exists, but ships the dishonest "confirm-an-infeasible-item = Resolved" behavior.

**Recommendation: A**, reconciled with the prototype's state names (map `you`→Settled, `fixed`→Resolved, add the "needs a fix" fork). Resolves the D088 open items.

**Doctrine check.** Serves honesty directly (no false "Resolved"); preserves that **only reanalysis moves the assessment** — the item flips to a resolution state only after the batch re-read, never in the click handler.

**Unblocks.** The R2 state model, the issue→pillar contract, the attestation/basis schema, and the reanalysis event table.

**Ratification —** Decision: ____________________ · Date: ______ · Idris

---

## DR-6 — The activation definition

> ▶ **RULED: Activated = the 2nd grounding act (the unlock)** — an amendment to the draft's "first act." Instrument three milestones off one `grounding_act` event stream: **Initiated** (1st act) → **Activated/Unlocked** (2nd act) → **Engaged** (act past unlock; the survey bar). Route counts; supersede "score_viewed"; activation is derived from the event, not the freeze. See the ratified block above.

**The question.** What event marks "activation," and what is the unlock threshold?

**Why now.** Two definitions conflict: DL-173 says activation = the **first grounding act (confirm | flag | route)**, segmented by role; the R1 telemetry spec says **"Activated = score_viewed"** (mere viewing). The freeze/unlock gate, the activation funnel, and the readiness-survey trigger all key off this — and if the survey fires on "viewed" rather than "experienced value," it inflates "not disappointed" and misreads the ~40% PMF bar.

**Options.**
- **A — Activation = first grounding act (DL-173), emitted as a durable `grounding_act` event *(recommended)*.** Supersede the telemetry spec's "score_viewed" as the activation milestone; segment by role (confirm-led delivery-PM vs route-led owner); confirm the freeze **unlock threshold = 2** grounding acts. The activation event is immutable once emitted (a later withdraw may re-lock the live gate but must not delete the event).
- **B — Keep "score_viewed" as activation.** Under-measures owners (whose honest path is to route, not confirm) and misaligns the survey trigger.

**Recommendation: A** — it matches the product's own behavior (routing already advances the unlock) and the honest survey-targeting rule.

**Doctrine check.** Route-counts-as-activation preserves confirm/flag/route symmetry (D133) and honest delegation; the activation event must survive withdraw (append-only record).

**Unblocks.** The grounding-act event, the freeze/unlock state contract, the survey-trigger audience, and the funnel telemetry.

**Ratification —** Activation event: __________ · Unlock threshold N = ____ · Date: ______ · Idris

---

## After these six are ruled

Product-grill runs against a single source of truth and produces the R2 delta contracts (State / Event / Data-Object / API / Integration Map) as vertical slices — using the slice seeds in audit §8 and building on the R1 canon the audit §6 says to reuse. The developer-facing handoff packet is assembled last, on top of the resolved decisions.

**Standing constraints that carry into every slice (encode as tests/lints, audit §3):** enforcement-mode = observe · never-metered exemptions (record, reviewer loop, Viewers) · freeze is presentation-only · feedback/survey structurally cannot touch the read + free-text sanitization boundary · integrity stays maturity-not-forecast · external-reviewer scope is hard-enforced · activation event survives withdraw.

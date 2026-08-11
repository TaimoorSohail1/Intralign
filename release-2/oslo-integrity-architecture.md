# OSLO — Outcome Integrity Architecture

**Current single-outcome model + the multi-outcome design**
Owner review · 2026-08-08 · prototype `oslo-prototype-r2.html` (guards 63/63 green)

This document has two jobs: (1) explain how integrity, pillars, issues, and proposals compute **today**, and confirm the invariant you asked for — *resolving every open issue drives every pillar to its top tier and opens a path to maximum outcome integrity*; and (2) design the **multi-outcome** extension so a project can carry several outcomes, each cascading to its own goals → success criteria → KPIs, with a clean, reconciled integrity computation.

---

## Part A — The current architecture (single outcome)

### A.1 The three pillars and how each is computed

Every score in OSLO derives from three independent **pillars**, each a function of concrete, user-earnable signals — never a click counter.

| Pillar | Measures | Computed from | Top tier reached when |
|---|---|---|---|
| **Grounding** | Does the read rest on *your* evidence, not OSLO's inference? | count of read items you've grounded (`grounded()`), gated: capped at the bottom while the outcome itself is still inferred | all 6 load-bearing items grounded |
| **Viability** | Are the plan's *definitions* sound and feasible? | ratio of understanding artifacts that are no longer weak (`clear / UND`), with a bounded bump for applied plan-fixes | every understanding artifact cleared (all inferred definition lines grounded) |
| **Adaptability** | Can the plan catch drift before it costs you? | outcome-checkpoint coverage (`_CHKPTS`) | full checkpoint coverage in place |

Each pillar maps its raw signal onto the shared **band ladder**: `Fragile → Weak → Developing → Solid → Sound`. Grounding uses a finer 7-step internal ramp onto the same five labels; Viability and Adaptability map directly.

### A.2 Outcome integrity = the weakest pillar

```
outcome integrity = min( Grounding, Viability, Adaptability )
```

This is the **weakest-gates** doctrine: a read is only as trustworthy as its least-sound dimension. It is why "one pillar at Solid" holds the whole read at Solid, and why the single most valuable next move is always whichever pillar is currently the floor (the *gate*). The gate-handoff banner exists to narrate the moment the floor moves from one pillar to another.

### A.3 The issue layer — the atomic unit of work

Underneath the pillars sits a single **exposure-ranked issue layer** (`_allIssues()`). Every weakness, across all three pillars, is one issue carrying:

- **`dim`** — which pillar it threatens (`grd` / `via` / `ada`)
- **`ftype`** — the finding type (No deadline, Unowned, Inference gap, False confidence, Coverage gap, …)
- **`sev`** — severity, and an **exposure** score = severity, bumped when the issue sits on the current gating pillar
- **`target`** — where it's resolved (a read item, a plan artifact, or an execution-plan lens)

Issues resolve through `issueOpen(x)`, which reads the *same* underlying state the pillars read, so the two cannot drift:

- item-targeted issue → closes when that read item is grounded (feeds **Grounding**)
- artifact-targeted issue → closes when that artifact is no longer weak (feeds **Viability**)
- execution-plan issue → closes when the execution plan is firmed; the checkpoint-coverage issue closes as checkpoints reach full coverage (feeds **Viability** / **Adaptability**)

> **Fix applied 2026-08-08.** Three execution issues (`sponsor-deadline`, `catering-owner`, `no-checkpoints`) previously hardcoded `issueOpen = true` — they could never close, and they stayed "open" in the issue layer even while Viability and Adaptability read Sound. That silently broke the invariant below. They now reconcile with their pillar's real signal. Guard: `issuesResolvableNoDeadEnds`.

### A.4 Proposals — additive, optional, band-neutral

Proposals (`artifact.props`) are a **separate primitive** from issues. An issue is a *gap that drags a pillar down*; a proposal is *OSLO-drafted content you accept or reject*. Deliberately:

- an undecided proposal **does not** penalize any band (you're not scored down for OSLO's suggestions), and
- accepting one **does not** move a band (a click on OSLO's idea is not a grounding act — this preserves "clicks can't pump a pillar").

Proposals are now folded **into the read** as workable accept/reject rows (not a separate inbox), labeled *optional*. They round out plan completeness; they are orthogonal to the integrity score. This is why a fully-grounded read can read **Sound** while optional proposals still sit pending — and that is honest, not a contradiction.

### A.5 The invariant — verified

> **Resolving every open issue drives each pillar to its top tier (Sound) and outcome integrity to Sound, with no dead-ends.**

Empirically confirmed by driving every guided lever to maximum (ground all 6 items, firm all 3 viability rows, add full checkpoint coverage, confirm the outcome):

```
Grounding: Sound   Viability: Sound   Adaptability: Sound   →   Outcome integrity: Sound
open issues remaining: 0        worklist rows remaining: 0        (proposals: optional, independent)
```

Two honesty guards hold the invariant in both directions: nothing stays open while its pillar is maxed (`issuesResolvableNoDeadEnds`), and the "what's next" guidance names the *real* lever to Sound rather than a false finish (`nextStepToSoundLegible`). **The current design supports your stated requirement.**

The one deliberate exclusion: a *held secondary outcome* is governed by the outcome-disclosure flow, not by plan-definition Viability, so it does not permanently cap the primary read. That exclusion is the seam the multi-outcome model formalizes next.

---

## Part B — The multi-outcome architecture

### B.1 The object model — one cascade per outcome

A project holds **N outcomes**. Each outcome is the root of its own tree; the tree the current product flattens into a single "intent" is simply the **N = 1** case of this.

```
Project
├── Outcome[1]  (primary)                     ← one outcome is the primary/headline
│   ├── Goal[1]
│   │   ├── SuccessCriterion[1]
│   │   │   └── KPI[1..q]                      ← the cascade bottoms out at measurable KPIs
│   │   └── SuccessCriterion[2] → KPI…
│   └── Goal[2] → SuccessCriterion… → KPI…
├── Outcome[2]  (secondary)
│   └── Goal… → SuccessCriterion… → KPI…
└── Shared artifacts  (budget, constraints, calendar, resource pool)
        └── referenced by ≥1 outcome
```

Two node kinds carry weight:

- **Cascade nodes** (Outcome → Goal → Success → KPI): the *definition* tree. A node is **grounded** (yours) or **inferred** (OSLO's read). Grounding flows the same way it does today, now scoped to a node.
- **Plan artifacts**: some are **outcome-scoped** (a schedule for one outcome's launch), some are **shared** (the budget cap, the calendar). Shared artifacts are referenced by multiple outcomes.

### B.2 Issue attribution — every issue belongs to an outcome

The issue layer stays the atomic unit; it gains one field: **`outcome`** (the owning outcome id), in addition to `dim` / `ftype` / `sev` / `target`.

- An issue on an **outcome-scoped** node or artifact attributes to that one outcome.
- An issue on a **shared** artifact **fans out**: it attributes to *every* outcome that depends on the shared element, but is **resolved once** — closing it closes it for all dependents. (Example: an unset budget cap is one issue that weakens three outcomes; you fix it once.)
- A new type, **cross-outcome conflict** (`dim: via`, feasibility): two outcomes contend for the same constrained resource (dollars, dates, a person). It attributes to both and resolves by re-allocation or re-prioritization. This is the genuinely *new* class multi-outcome introduces — it cannot exist at N = 1.

### B.3 Pillar and integrity computation — nested min

Each pillar is computed **per outcome**, from that outcome's issues, exactly as today:

```
Grounding(O)     = f( O's grounded cascade nodes / grd-dim issues )
Viability(O)     = f( O's cleared definition artifacts / via-dim issues )
Adaptability(O)  = f( O's checkpoint coverage / ada-dim issues )

Integrity(O)     = min( Grounding(O), Viability(O), Adaptability(O) )     ← weakest-gates, per outcome
```

Then the project rolls up. Because both levels compose with `min`, the rollup is associative — you can aggregate pillars-then-outcomes or outcomes-then-pillars and get the same number:

```
Grounding(Project)   = agg over O of Grounding(O)
Viability(Project)   = agg over O of Viability(O)
Adaptability(Project)= agg over O of Adaptability(O)

Integrity(Project)   = min( pillar rollups )  ≡  agg over O of Integrity(O)
```

The masthead keeps its three pillar pills (now project rollups) and its single integrity band; **drilling into any pillar reveals the per-outcome breakdown**. This is what "reconciles with each of the pillars separately" means concretely: each pillar has its own cross-outcome rollup, and each is inspectable per outcome.

### B.4 The one real decision — how `agg` treats non-primary outcomes

`agg` is the only genuine product choice, and it matters because a strict `min` lets a single fragile secondary outcome tank the whole project.

| Option | Project integrity | Pro | Con |
|---|---|---|---|
| **Strict min** | weakest outcome gates the project, full stop | purest weakest-gates; brutally honest | one barely-sketched secondary outcome drags a strong primary to Fragile |
| **Primary-gates** *(recommended)* | headline = the primary (and any outcome you've *committed to optimizing*); other outcomes shown with their own integrity but don't gate the headline | matches the existing primary/secondary + deferred-disclosure model and the freemium gate (optimizing >1 outcome is the paid step); still weakest-gates *within* each outcome's scope | needs a clear notion of which outcomes are "in scope for the headline" |
| **Priority-weighted** | weighted blend across outcomes | soft, no cliff | abandons weakest-gates; a weighted average can read "Solid" while a committed outcome is Fragile — dishonest by the product's own doctrine |

**Recommendation: primary-gates.** The project's headline integrity is the `min` over the set of outcomes the user has *committed to* (the primary always; secondaries as they're activated). Weakest-gates stays intact *inside* every outcome and *across* the committed set — so the headline can never read sounder than the weakest committed outcome — while a merely-inferred secondary outcome sits in the breakdown with its own honest band and does not punish a strong primary. This also reconciles cleanly with the commitment-gate: activating a second outcome for optimization is exactly the act that pulls it into the headline `min`.

### B.5 Reconciliation summary

- **With proposals.** Proposals attach to an outcome-scoped or shared artifact, scoped to their outcome(s), still optional and still band-neutral. The read rolls them up as "*N optional additions across your outcomes*," decidable inline per outcome. No change to the honesty rule.
- **With the pillars.** Each pillar rolls up per outcome → project (§B.3); the integrity band is `min` of the rollups over the committed set (§B.4). Pillars remain independently inspectable and independently gateable.
- **With the invariant.** It holds at scale by nesting: resolving every issue across every outcome → each outcome's three pillars max → each outcome integrity Sound → project integrity Sound. No dead-ends, because every issue — outcome-scoped, shared (fan-out), or cross-outcome conflict — has an explicit resolution path, the same property Part A now guarantees at N = 1.

### B.6 Migration path

The current prototype is already the N = 1 slice of this model. Two things seed the extension and are worth building toward deliberately:

1. **The held secondary outcome** (today excluded from the primary's Viability) is literally *Outcome[2]* waiting for a home — the disclosure flow that manages it is the embryonic multi-outcome UI.
2. **The issue layer** already carries `dim` / `ftype` / `sev` / `target`; adding `outcome` and the fan-out/conflict semantics is an additive change, not a rewrite. Pillars already read from issues via the reconciled `issueOpen`, so making them per-outcome is a scoping change, not a new computation.

The safe build order: (1) add the `outcome` field and make the current single outcome `Outcome[1]`; (2) render the cascade tree per outcome; (3) scope pillar computation per outcome with the `min` rollup and primary-gates aggregation; (4) introduce shared-artifact fan-out; (5) add the cross-outcome conflict issue type. Each step keeps the invariant guard green.

---

## One-line status

The current design **now supports** your invariant (verified + guarded); the multi-outcome model is a clean nesting of the same weakest-gates composition, with **primary-gates aggregation** as the single recommended decision and **cross-outcome conflict** as the only genuinely new issue class it introduces.

# DL-211 — Proposal-resolution model (build vs inference vs optional) + cross-surface resolution sync + itemized atomic findings

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (doctrine — amends a ratified honesty invariant) with a B (prototype/Slice realization).
- **Framework 001** — AI drafts; only the owner ratifies.
- **Basis:** owner observation — accepting an OSLO proposal *in the artifact* left the linked issue card open (double-work), and a card carrying multiple proposals merged distinct findings into one prose row. Chain: **RB-045** → this record (review embedded) → owner Decision.
- **Extends / reconciles:** DL-196 (all pillars resolve through the issue layer) · DL-209 (verify/build/decide acts; only-verify-moves-Grounding) · DL-210 (atomic findings; decompose, never merge) · DL-197 (false confidence). **Amends:** the ratified `proposalsFoldedIntoRead` invariant (proposals were *all* treated as additive).
- **Placement:** staged in `release-2/`; folds into `main` at R1 graduation. No freemium-build impact.

---

## The trigger (why this isn't just a bug)

Accepting a proposal is guarded to be **additive — it must not move the integrity band** (`proposalsFoldedIntoRead`). That guard is deliberate: accepting *OSLO's own suggestion* must never let OSLO grade its own homework up (manufactured confidence — the DL-197/DL-209 prohibition). So "accept-in-artifact didn't resolve the issue" was partly the guard doing its job. But the owner's frustration is legitimate: a proposal that genuinely *is* an issue's fix should resolve it, from any surface, once. The reconciliation is a doctrine refinement, not an override.

## Decision

### A. Proposals are three kinds (assigned by what accepting them does)

1. **Build proposals** — add a *missing structural element* (a backup-keynote task, an on-site owner, a sponsor deadline, an outcome KPI, a backup-speaker requirement). Accepting one is a **build act** (DL-209): it fills a structural gap, so it **resolves the structural finding** and may firm Viability/Adaptability via reanalysis. This is **not** manufactured confidence — it is a real, user-accepted change to the plan's structure.
2. **Inference proposals** — accept *OSLO's guessed value or assumption* (e.g. a show-rate assumption). Accepting is **additive and never moves Grounding**; the Grounding finding resolves **only by verifying the real value** (only-verify-moves-Grounding, GT-35). Accepting OSLO's guess is not evidence.
3. **Optional proposals** — round out the plan (e.g. an undecided boundary). **Additive; resolve nothing**, as today.

### B. Cross-surface resolution sync (one finding, one resolution)

A finding and the proposal(s) that resolve it are **one object**. Resolving it from any surface — the issue card, the artifact, or the folded read row — writes the **one finding**, through the **single reanalysis path** (only-reanalysis-resolves, GT-10). Resolved once, reflected everywhere; never re-presented, never redone.

### C. Multiple resolvers (partial keeps it honestly open)

A finding with **N build-resolvers stays open until all N are accepted** — accept one, it stays open; accept the last, it resolves. A finding with one resolver resolves on the single accept. (Owner ruling: keynote-backup requires **both** its requirement and its task.)

### D. Itemized atomic findings (group, never merge)

Findings render as **individual, independently-resolvable rows** grouped under a shared container — **never merged into one prose row** (which cannot show one resolving while its sibling stays open). Only **load-bearing** findings become rows; the benign tail stays on the map (DL-196 §3). This is distinct from DL-210 **precedence-deferral**: a downstream finding blocked by an upstream cause is *deferred behind it*, not merged with it.

### E. Amends `proposalsFoldedIntoRead`

The additive / no-band-move invariant holds for **inference and optional** proposals. **Build proposals resolve their finding** (and may firm the band via reanalysis) — a real structural change, not OSLO grading itself. The guard is refined to test the additive invariant on an inference/optional proposal and the resolution invariant on a build proposal.

## Enforceable guards (extends the firewall)

`buildProposalResolvesFinding` (accepting a build proposal enqueues reanalysis and closes its finding; partial keeps it open) · `inferenceProposalStaysAdditive` (accepting an inference/optional proposal moves no band and grounds nothing — only verify grounds) · `resolutionSyncedAcrossSurfaces` (a finding resolves from card/artifact/row through the one reanalysis path, once) · `findingsItemizedNotMerged` (multiple findings render as separate resolvable rows, never one prose row).

## Doctrine preserved (unchanged)

Only-verify-moves-Grounding (GT-35) · only-reanalysis-resolves (GT-10) · the manufactured-confidence prohibition (DL-197) · the load-bearing discipline (DL-196 §3) · atomic, decomposed findings (DL-210).

## Review (five outputs — Framework 001)

- **Findings.** Accepting a proposal was uniformly additive; some proposals are genuinely structural fixes; the merge of findings into one prose row is what prevented one-resolving-while-sibling-stays and drove the double-work.
- **Concerns.** Amends a *pinned* honesty guard — must not weaken the manufactured-confidence prohibition; mitigated by confining band-movement to *build* proposals (real structural changes) and keeping inference acceptance strictly additive.
- **Dependencies.** DL-196/209/210/197; the `proposalsFoldedIntoRead` guard; Slice 2 (issue lifecycle) — the contract lands there.
- **Recommendation.** Ratify A–E; amend the guard; itemize findings; wire cross-surface resolution through reanalysis.
- **Status.** ✅ Ratified 2026-08-09. Realization: prototype + Slice 2 contract + guard set; verified via the headless `_S10` gate.

## Affected artifacts

`BACKLOG_RB-045_proposal-resolution-model.md` · `slices/02-issue-lifecycle-grounding-acts.md` (the sync contract) · `slices/09-…` §3 (guards) · prototype `oslo-prototype-r2.html` (resolution sync + itemized rows + amended guard). At graduation: reconcile with `FINDING_MODEL_V1` / `RECOMMENDATION_MODEL_V1` (proposal-as-build-fix) per `R2_TO_MAIN_CAF_RECONCILIATION_CATALOG.md`.

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09**. Staged in `release-2`; folds into `main` at R1 graduation._

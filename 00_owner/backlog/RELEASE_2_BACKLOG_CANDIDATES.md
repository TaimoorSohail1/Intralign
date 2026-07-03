# Release 2 — Backlog Candidates (index)

**Status:** **Candidate list — owner-directed (2026-06-05). NOT ratified R2 scope; NOT prioritized.** A gathering point for everything deferred past Release 1, so R2 starts from one picture instead of scattered notes. Each candidate gets its **own scoping item** (and DL where it touches architecture) **when promoted**. Per `CLAUDE.md`: this introduces no doctrine and resolves no ontology — it **indexes**, it does not decide.

> **R1 context:** Release 1 is the owner's **own test/validation vehicle** — a tight **owner + 2–3** cohort (DL-076: owner + <5) whose purpose is to surface **issues, refinements, and enhancements** before authorizing the 10–20-user R2. R1 therefore yields **qualitative product-correctness signal — not statistically meaningful usage / funnel / cost data.** R2 starts from R1's **fix / refine / enhance findings**; the **quantitative calibrations** (cost medians, conversion / k-factor, upgrade-prompt timing) **accrue from R2+ (10–20) and mature across the Alpha ladder**, not from R1. *(Owner clarification 2026-06-28.)* Sources below are cited so each candidate traces to where it was deferred.

---

## Phase & tier placement (owner direction, 2026-06-28)

These candidate epics are **gated by phase/tier**, independent of the "R2-" index labels (this file is a deferral-candidate index, not a ship-release plan):

- **R2-C — Execution Intelligence → Beta.** Does **not** begin until the Beta phase (consistent with **DL-083**, which placed execution monitoring at Tier 3 / Pro+, Beta-built). C1 → C2 → C3 are Beta capabilities.
- **R2-D — Team Collaboration depth → Team tier (Tier 4).** Does **not** begin until the Team tier.
- **R2-E — Governance & Authority → Beta.** Does **not** begin until the Beta phase (the largest, most architectural epic; likely multi-release).

**Foundational-architecture exception (applies to all three):** *architectural foundation* work for a phase-/tier-gated capability **may be done earlier, in Alpha (R2), when laying it early reduces later effort or complexity** — build the seams/abstractions now, ship the user-facing capability at its gated phase/tier. This is **build-sequencing, not capability activation**: any such early foundation stays **advisory-only / non-activating** (DL-047), specified-but-inactive, and routes through normal scoping (and a DL where it touches architecture). Mirrors **Layer-Before-Depth (DL-081)** — altitude/foundation first, depth at its proper phase.

---

## Epic R2-A — Growth & Conversion *(the committed fast-follow)*

| # | Candidate | Source | Notes / dependency |
|---|---|---|---|
| A1 | **External-stakeholder recipient experience** — scoped view/respond UI, external email-verified auth, **reviewer→user promotion**, convert-moment | CHG-064; `BACKLOG_EXTERNAL_STAKEHOLDER_EXPERIENCE`; DL-049 | Identity model (`Principal`) **already ratified** → clean drop-in. The conversion half of k = i×c. **Anchor of R2.** |
| A2 | **Referral reward** — bounded, conversion-credited capacity bump | CHG-064; `BACKLOG_REFERRAL_REWARD` | Credits on *join* → **depends on A1**. Cost-bounded (DL-048) + abuse guards; values owner-set. |
| A3 | **Pre-account interaction (PF-05)** — begin using before signup (Lovable/Bolt/v0-style) | Matrix PF-05 (Future) | Complements A1's low-friction entry; an acquisition/onboarding lever. |

*All three tuned against **R2+** TEL-06 / k-factor data (R1's cohort is too small for meaningful funnel signal — see R1 context); bound by the value-alignment guardrails (no autonomous sends, no dark patterns).*

## Epic R2-B — Paid Tiers & Monetization

| # | Candidate | Source | Notes |
|---|---|---|---|
| B1 | **Define paid tiers 3–5 (Pro · Team · Enterprise)** — envelope, caps, routing, token budget, price per tier | Open-TBD E3; `BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE` (costed ladder) | Tier-keyed config rows, **not code** (enforcement already tier-parameterized). Set values from **R2+ real-usage cost telemetry** (not R1 — cohort too small; see R1 context). |
| B2 | **Paid-tier upgrade experience at scale** — extend the upgrade-prompt taxonomy + tier-progression to the paid ladder | `12_freemium_tier_behavior_logic.md` (Free/Basic applied) | Reuses the ratified pattern; new prompts/targets per tier. |

## Epic R2-C — Execution Intelligence *(clusters; ties to the Outcome-Integrity doctrine's "Current Reality")* — **Beta phase** (owner 2026-06-28; see Phase & tier placement)

| # | Candidate | Source | Notes |
|---|---|---|---|
| C1 | **Project-execution monitoring via 3rd-party platforms** — connector layer + the contracted evidence-intake seam | tier-progression backlog (Pro forward note) | **New capability — needs its own scoping** (platforms, architecture, Capability-Matrix entry). Integration history: DL-042 moratorium — scope deliberately. |
| C2 | **CONF-07 Operational Confidence** — confidence derived from actual execution reality | Matrix CONF-07 (Future) | **Enabled by C1** (execution data → execution-grounded confidence). The Current-Reality sensor. |
| C3 | **Simulations + execution synchronization** — "more simulations" (Pro), "execution synchronization" (Team) | freemium tier unlock lists | Advanced execution features; depend on C1/C2. |

*Doctrinal note: C1→C2 feed the **Current-Reality** side of Outcome Integrity (coherence between Intended and Current Reality) — they extend the model, not bypass it.*

## Epic R2-D — Team Collaboration *(depth beyond R1's seed)* — **Team tier (Tier 4)** (owner 2026-06-28)

| # | Candidate | Source | Notes |
|---|---|---|---|
| D1 | **Team collaboration depth** — shared spaces, approvals, advanced shared views | Team tier unlock; freemium constraints ("collaboration depth" gated) | R1 ships seed primitives (comments, CRR, MRI share); R2 adds depth. Multi-user concurrency/edit-conflict model (Matrix gap #340) lands here. |

## Epic R2-E — Governance & Authority *(largest, most architectural — likely multi-release)* — **Beta phase** (owner 2026-06-28)

| # | Candidate | Source | Notes |
|---|---|---|---|
| E1 | **Authority engine** — exposure/suppression/authorization governance (specified-but-inactive in R1) | Glossary; DL-043 (no Authority in R1) | The major deferred architecture. Pulls in the **5 preserved future models**: Governance, Disposition, Resolution-Candidate, Accepted-Understanding, Review-Request. **A DL-class epic when promoted.** |
| E2 | **Governance policies / org thresholds / agent governance** | Enterprise tier unlock | Enterprise-tier capability; built on E1. |
| E3 | **Portfolio cognition / cross-system orchestration** | Enterprise tier unlock | Multi-project/org-scale cognition; furthest out. |

## Epic R2-F — Deferred cognitive surfacing

| # | Candidate | Source | Notes |
|---|---|---|---|
| F1 | **AE-06 Understanding Debt** — surface accumulated unresolved ambiguity/assumptions/conflicts | Matrix AE-06 (Future); gap #14 | Defined but deliberately not surfaced in R1; a Disclose-side addition. |

## Epic R2-G — Smaller deferred items

| # | Candidate | Source | Notes |
|---|---|---|---|
| G1 | **SHARE-05 permission-level enumeration** (§22) | Matrix SHARE-05 | Link hygiene applied in R1 (P7); the *permission levels* themselves remain to enumerate. |
| G2 | **Richer artifact optimization** | Pro tier unlock | Advanced Advise/editing capability. |
| G3 | **Export / sync beyond PDF** | freemium constraints (Free = PDF only) | Full export/sync formats as a paid/future capability. |

---

## Sequencing observations (not a commitment)

- **R2-A is the natural first epic** — it's the committed fast-follow, the identity model is already ratified (zero rework), and it converts the loop R1 instruments.
- **R2-B** is low-effort (config rows from R1 cost data) and pairs naturally with A (a growing user base needs upgrade paths).
- **R2-C (Execution Intelligence)** is a **coherent cluster** (C1 enables C2/C3) and the most strategically distinctive — it extends OSLO into Current-Reality sensing. Largest *new* product surface; deserves its own scoping pass (esp. the DL-042 integration history).
- **R2-E (Authority)** is the **largest and most architectural** — realistically multi-release, and a DL-class undertaking that re-activates the 5 preserved future models. Don't underestimate it; don't start it before C/A prove the product's growth + execution value.
- **R1 hygiene carry-over (not R2 product):** task #121 (apply env-profile R1–R5 at env-binding) and the post-build re-tune of the estimate-based Calibration defaults (cost, envelope, prompt timing) from real telemetry.

## What this is / isn't
- **Is:** a living candidate index, traced to sources, to seed R2 planning.
- **Isn't:** ratified scope, a priority order, or a commitment. Promotion of any item = its own scoping item (+ DL where it touches architecture: A1 auth, C1 integrations, E1 Authority), owner-decided.

---
*This owner-directed index gathers every Release-1 deferral into one candidate picture for Release 2 — the committed growth/conversion fast-follow (external-stakeholder recipient experience, referral reward, pre-account interaction), paid tiers 3–5 and the paid upgrade experience, the Execution-Intelligence cluster (3rd-party execution monitoring → operational confidence → simulations/sync, which extend the Outcome-Integrity Current-Reality side), team-collaboration depth, the large and architectural Governance/Authority epic that re-activates the five preserved future models, deferred cognitive surfacing (Understanding Debt), and smaller deferred items (permission levels, richer optimization, export/sync) — each traced to where it was deferred and annotated with dependencies and whether it is commodity or architecture. It records non-binding sequencing observations (A first as the rework-free committed fast-follow; B as low-effort config; C as the distinctive Execution-Intelligence cluster; E as the largest multi-release architectural epic) and the R1 hygiene carry-overs, while explicitly stating it ratifies nothing and that each candidate is promoted via its own owner-decided scoping item.*

**Release 2 Backlog Candidates index prepared (candidates, not scope).**

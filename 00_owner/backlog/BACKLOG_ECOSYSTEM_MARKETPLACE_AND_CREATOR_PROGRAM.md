# Backlog — OSLO Ecosystem: Creator Marketplace, Expert Program & Domain Extensions (Candidate Capabilities)

- **Status:** **Candidate — owner triage.** AI-drafted from the 2026-06-19 ecosystem brainstorm + owner-aligned prioritization. **Not adopted, not contracts; introduces no doctrine.** Each capability carries its **stage** and **gating dependency** so it surfaces at the right time.
- **Thesis:** a third-party ecosystem (creators, PM experts/influencers) on top of OSLO as a **distribution channel + content/outcome value + supply-side network effect** that compounds the data moat. The Notion-marketplace pattern, **governed by OSLO's epistemic invariants**.
- **Source:** owner direction 2026-06-19; grounded in DL-056 (templates), DL-074 (pricing), DL-049 (reviewer identity), DL-073 (access), DL-076 (release model), and `BACKLOG_ADOPTION_ACCELERATION_AND_GROWTH_LOOPS` (G3/G5/G6).

> **Governing design principle (load-bearing — read first).** Every contribution is one of two kinds. **(A) Structure / content** (templates, scaffolds, reference packs) = pre-authored content the user *adopts* → an **Attested** user artifact (DL-056: adopting pre-authored content is **not generation**) — epistemically safe. **(B) Cognition / assessment** (anything that changes how OSLO *scores, finds, or recommends*) = touches the **governed epistemic core** and **cannot be third-party-injected ungoverned.** This boundary gates the whole ecosystem; **E4 is the only capability that crosses it** and is therefore governance-gated. The governed boundary is also a *trust differentiator* — "the marketplace that can't manipulate your judgment."
>
> **Three levels of customization** (so the layers don't blur): **L1 content** = templates filling the *fixed* artifacts (E1). **L2 schema** = the planning *artifact set itself* — which artifact types exist, per domain/methodology (E6). It is structural (not cognition), but it changes the planning **model**, so it is gated on a prior architecture decision — `PLANNING_ARTIFACT_MODEL_EXTENSIBILITY_ESCALATION_001` (is the 7-artifact model fixed or extensible?). **L3 cognition** = how OSLO *assesses* — evaluation lenses (E4).

## Prioritization (owner-aligned, 2026-06-19)

- **v1:** **E1 Template marketplace** + **E2 Expert/partner + affiliate program** — mutually reinforcing (the same PM experts are both creators *and* distributors); lowest risk/effort, highest distribution.
- **North-star:** **E4 Evaluation lenses** — highest outcome value + deepest moat, but **governance-gated** (design the boundary early, build last).
- **Parallel / forward:** **E5 Connectors** (developer ecosystem — extends G5; rides the Validation/execution-monitoring roadmap).
- **Folded:** **E3 Knowledge packs** → into E1 templates.
- **Gated (architecture decision first):** **E6 Domain packs** (custom artifact schema + methodology — the deepest, most defensible layer) — **blocked** on `PLANNING_ARTIFACT_MODEL_EXTENSIBILITY_ESCALATION_001` (is the planning-artifact model fixed or extensible?). A domain pack is the natural *bundling unit*: artifact set (E6) + templates (E1) + reference (E3) + a governed lens (E4) for one domain.

## Capabilities

### E1 — Template marketplace (v1) — *commodity content + monetization · post-R1*
- **What:** domain/industry-specific artifact/workflow plan templates, created and sold by third parties; users adopt + edit.
- **Builds on:** DL-056 (template mechanism — *marketplaces / user-created templates are explicitly deferred there*, i.e. this is the un-defer); **G6** (community gallery = the seed); DL-074 (rev-share / payouts).
- **Governance:** Structure/content — Attested on adoption, **not generation** (DL-056). **Low risk.** Needs curation / quality / rating + creator IP/licensing.
- **Stage / gating dependency:** **post-R1** (DL-056 defers marketplaces); bridges from the **G6** community gallery. Raise as a dependency when G6 / R2+ template work is scoped.
- **Owner decisions:** rev-share model; curation/certification; per-org custom catalogs.

### E2 — Expert / Partner + Affiliate program (v1) — *commodity GTM + program · phased*
- **What:** PM influencers/experts as a distribution channel — a certified-expert/partner program + affiliate/referral for promoting OSLO and selling their templates/services ("done-with-you" planning).
- **Builds on:** **G3** (the collaborative/invite loop + k-factor), DL-074 (affiliate payouts / rev-share), DL-049 (`Principal`/reviewer identity — experts as external principals).
- **Governance:** **Low** — services + promotion; an expert-built plan is Attested *user* content.
- **Stage / gating dependency:** the **program + recruiting (GTM) can begin in Alpha** (low build); **affiliate-monetization mechanics are post-R1** (DL-074 pricing + G3 loops). Raise alongside the G3 / DL-074 realization.
- **Owner decisions:** certification bar; affiliate economics; expert vetting.

### E3 — Knowledge / reference packs — *folded into E1*
- Best-practice domain guidance surfaced as **reference** (via the Chat/Disclose surface), Attested to the creator, **not altering assessment**. Ship as a *template + guidance bundle* under E1, not standalone.

### E4 — Evaluation lenses / domain rubrics (NORTH-STAR — governance-GATED) — *frontier · post-R1+*
- **What:** a domain expert's "what good looks like / what risks to watch" for a plan type, applied as a **governed Derived lens** — OSLO controls application; confidence-qualified; transparently attributed ("flagged per *[Expert]*'s lens").
- **Value:** highest outcome improvement + deepest moat (governed domain expertise).
- **Governance:** **HIGHEST** — touches **Evaluate / Advise** (the epistemic core). The **one** capability that crosses the structure↔cognition boundary.
- **✅ ESCALATION — RESOLVED (DL-079, 2026-06-19):** the boundary is ratified — a lens is **governed input to first-party cognition, never third-party cognition**; it may surface **attributed, confidence-qualified** considerations but **never alters CAF/scores and never disposes** (OB-5; "advise proposes, never disposes"). **Reference-only (A) first; governed overlay (B) north-star; Option C (scoring contribution) fenced** as a separate future doctrine decision; **CAF stays first-party.** **E4 remains design-only** until its realization is proposed under this boundary. See `00_owner/decisions/records/DL-079-e4-lens-cognition-boundary.md` (analysis: `00_owner/architecture_decisions/E4_THIRD_PARTY_EVALUATION_LENS_GOVERNANCE_ESCALATION_001.md`).
- **Stage / gating dependency:** **post-R1, after the governance boundary is ratified.** Design the boundary early; build last.

### E5 — Connectors / developer ecosystem — *extends G5 · forward / Pro+*
- **What:** third-party-built connectors to PM/execution systems (the Validation connectors). Distribution via their marketplaces + switching cost + feeds the data moat (G1).
- **Builds on:** **G5** (integration-as-distribution), the **Pro+ execution-monitoring** scoping (DL-073/backlog), **G1** (data loop).
- **Note:** a **developer** ecosystem — distinct audience from E1/E2 PM creators; sequences with execution-monitoring, **not** the creator marketplace.
- **Stage / gating dependency:** **forward / Pro+**; raise with the execution-monitoring / G5 scoping.

### E6 — Domain packs / custom planning-artifact schema (L2) — *architecture-gated · post-decision*
- **What:** domain/methodology-specific **planning-artifact sets** (construction adds submittals/RFIs/permits; agile replaces WBS/Schedule with epics/stories/sprints; manufacturing adds BOM/routing) — i.e. extending **which artifact types exist and the planning cadence**, not just content. The natural creator unit is a **domain pack** bundling the artifact set + templates (E1) + reference (E3) + a governed lens (E4).
- **Why it matters:** the R1 model (Intent→…→Schedule) is **classical-PM-leaning** and does not universally fit; domain packs make OSLO a *platform* (domain-native planning), the deepest moat — but they change the planning **model**.
- **⚠ GATING DEPENDENCY (architecture/doctrine):** **RESOLVED in principle — DL-077** ratified Option C (hybrid core: fixed understanding core + extensible execution-planning layer). The **registry that is E6's substrate** is designed in `00_owner/architecture_decisions/ARTIFACT_PROFILE_MECHANISM_REALIZATION_DESIGN_001.md` (Framework 001 Proposal stage, post-R1) — E6 stays **design-only** until that realization-design intent is ratified and the **registry-governance model + E4 cognition boundary** are set (synthesis/CAF/MRI handle variable artifact sets, CAF stays first-party).
- **Governance:** L2 is structural (not cognition-injection), but it touches Infer (synthesis), Evaluate (CAF), Disclose (MRI). Any artifact set must preserve Attested/Derived, CAF, Confidence, recompute; methodology changes cadence → affects drift/Outcome-Integrity.
- **Stage / dependency:** **post the architecture decision**; deeper than E1. Raise with the extensibility escalation.

## Defensibility

Stacks a **supply-side network effect** (creators → domain coverage → users → creators) + a **domain content library** competitors can't clone quickly + the **data moat** (per-domain templates/outcomes → per-domain calibration, G1). The **governed-cognition boundary** is itself the trust differentiator.

## Release-stage map (per DL-076 release model)

| Capability | Earliest stage | Gating dependency |
|---|---|---|
| **E2** program / recruiting | **Alpha** (GTM) | low build |
| **E1** template marketplace | **post-R1 (R2+)** | DL-056 un-defer · G6 gallery · DL-074 rev-share |
| **E2** affiliate monetization | **post-R1** | DL-074 + G3 |
| **E4** evaluation lenses | **post-R1+** | **the E4 governance escalation (ratify first)** |
| **E5** connectors | **forward / Pro+** | G5 + execution-monitoring scoping |
| **E6** domain packs (artifact schema) | **architecture-gated → post-decision** | the extensibility escalation (resolve first) |

## Status / routing

Candidate backlog for owner triage. **Introduces no contract or doctrine;** cross-references DL-056, DL-074, DL-049, DL-073, DL-076, and growth-backlog G3/G5/G6. The **E4 evaluation-lens governance question** is the one item escalated as an owner/doctrine decision and is set as a **hard gate on E4** so it is raised before any cognition-contribution build.

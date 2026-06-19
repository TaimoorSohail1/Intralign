# Backlog — OSLO Ecosystem: Creator Marketplace, Expert Program & Domain Extensions (Candidate Capabilities)

- **Status:** **Candidate — owner triage.** AI-drafted from the 2026-06-19 ecosystem brainstorm + owner-aligned prioritization. **Not adopted, not contracts; introduces no doctrine.** Each capability carries its **stage** and **gating dependency** so it surfaces at the right time.
- **Thesis:** a third-party ecosystem (creators, PM experts/influencers) on top of OSLO as a **distribution channel + content/outcome value + supply-side network effect** that compounds the data moat. The Notion-marketplace pattern, **governed by OSLO's epistemic invariants**.
- **Source:** owner direction 2026-06-19; grounded in DL-056 (templates), DL-074 (pricing), DL-049 (reviewer identity), DL-073 (access), DL-076 (release model), and `BACKLOG_ADOPTION_ACCELERATION_AND_GROWTH_LOOPS` (G3/G5/G6).

> **Governing design principle (load-bearing — read first).** Every contribution is one of two kinds. **(A) Structure / content** (templates, scaffolds, reference packs) = pre-authored content the user *adopts* → an **Attested** user artifact (DL-056: adopting pre-authored content is **not generation**) — epistemically safe. **(B) Cognition / assessment** (anything that changes how OSLO *scores, finds, or recommends*) = touches the **governed epistemic core** and **cannot be third-party-injected ungoverned.** This boundary gates the whole ecosystem; **E4 is the only capability that crosses it** and is therefore governance-gated. The governed boundary is also a *trust differentiator* — "the marketplace that can't manipulate your judgment."

## Prioritization (owner-aligned, 2026-06-19)

- **v1:** **E1 Template marketplace** + **E2 Expert/partner + affiliate program** — mutually reinforcing (the same PM experts are both creators *and* distributors); lowest risk/effort, highest distribution.
- **North-star:** **E4 Evaluation lenses** — highest outcome value + deepest moat, but **governance-gated** (design the boundary early, build last).
- **Parallel / forward:** **E5 Connectors** (developer ecosystem — extends G5; rides the Validation/execution-monitoring roadmap).
- **Folded:** **E3 Knowledge packs** → into E1 templates.

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
- **⚠ ESCALATION — gating dependency (must resolve before any E4 build):** *May a third-party rubric influence Evaluate/Advise, and under what governance?* An **owner + doctrine decision** (Anti-Assumption: do not let third-party content bypass governance). Any lens must stay **Derived, confidence-qualified, attributed**, and must never silently bias an assessment (**OB-5**; "advise proposes, never disposes"). **Until this is ratified, E4 is design-only.**
- **Stage / gating dependency:** **post-R1, after the governance boundary is ratified.** Design the boundary early; build last.

### E5 — Connectors / developer ecosystem — *extends G5 · forward / Pro+*
- **What:** third-party-built connectors to PM/execution systems (the Validation connectors). Distribution via their marketplaces + switching cost + feeds the data moat (G1).
- **Builds on:** **G5** (integration-as-distribution), the **Pro+ execution-monitoring** scoping (DL-073/backlog), **G1** (data loop).
- **Note:** a **developer** ecosystem — distinct audience from E1/E2 PM creators; sequences with execution-monitoring, **not** the creator marketplace.
- **Stage / gating dependency:** **forward / Pro+**; raise with the execution-monitoring / G5 scoping.

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

## Status / routing

Candidate backlog for owner triage. **Introduces no contract or doctrine;** cross-references DL-056, DL-074, DL-049, DL-073, DL-076, and growth-backlog G3/G5/G6. The **E4 evaluation-lens governance question** is the one item escalated as an owner/doctrine decision and is set as a **hard gate on E4** so it is raised before any cognition-contribution build.

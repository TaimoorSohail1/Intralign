# Canonical Glossary — One Name Per Concept (anti-drift)

**Status:** Authoritative vocabulary · **Date:** 2026-06-04
**Rule (see `ANTI_ASSUMPTION_BUILD_PROTOCOL.md`):** use the **canonical term** for each concept in code, tests, comments, and docs. **Do not invent a synonym; do not reuse a banned term.** If a concept you need isn't here, it may be unspecified — **escalate, don't coin.** Authoritative definitions live in the architecture spec, object model, and DL-043/046/047; this glossary is the quick index.

## Epistemic core

| Canonical term | Meaning (one line) | Banned / not this |
|---|---|---|
| **Attested** | Canonical state: source-attributed **and** re-derivable. The only thing the canonical store holds. | "Grounded", "verified", "true" |
| **Derived** | Non-canonical cognition (Findings, Issues, Confidence, generated artifacts) — recomputable, history-tracked. | "Candidate", "draft truth" |
| **AttestedAssertion** | A canonical record (content types: **Canonical Fact · Assumption · Constraint · Dependency**) — canonical only when attested. | "Fact" (bare), "Knowledge" |
| **evidence-attested / OSLO-self-attested / user-attested** | The three attesting sources (a source asserts P / a Cognition History Record / a user acceptance). | — |
| **CognitionHistoryRecord (CHR)** | OSLO-self-attested, append-only record of one cognition emission. **Recompute appends a new CHR; never overwrites.** | "log entry", "audit row" (when it's a CHR) |
| **UserAcceptanceRecord** | User-attested record that a user accepted an item; **version-pinned** to a CHR. **Not a Governance Decision.** | "approval", "sign-off record" |
| **PlanFact** | A user-attested AttestedAssertion — "factual **in the plan**", distinct from world-truth. | "truth", "verified fact" |
| **epistemic_state** | Explicit attribute on every cognition entity: `attested-*` \| `derived`. | a bare "knowledge" type that hides it |

## Responsibilities (the cognitive spine — code organized by these)

`Perceive` (intake + **source-attributed claim extraction**, no Derived cognition) · `Retain` (canonical append-only store) · `Infer` (Findings **and** synthesis/generation of the planning model — Derived) · `Evaluate` (Issues, Confidence, Reliability, CAF, Outcome Confidence, False-Confidence, Understanding State) · `Advise` (Recommendations, Clarifications, Suggested Fixes — candidate responses only) · `Disclose` (presentation incl. Chat surface) · `Act/Adapt` (recompute/stale backbone). `Render` = non-cognitive service. **No `Authority` engine in R1.** **Banned as *primary* identifiers:** layer names — Context Plane, Knowledge Layer, Judgment, Communication.

## Cognition outputs

| Canonical term | Owner | Banned / not this |
|---|---|---|
| **Finding** (Gap / Conflict / Risk Signal) | Infer | "issue" (Issue is distinct), "problem" |
| **Issue** | Evaluate | "finding" (distinct) |
| **Confidence** (= trust in **understanding**) | Evaluate | "project health/readiness/score/probability" |
| **Reliability** | Evaluate | "accuracy", "trust score" |
| **CAFAssessment** (Clarity · Alignment · Feasibility) | Evaluate | "quality score" |
| **OutcomeConfidence** | Evaluate | "success probability" |
| **Recommendation** (+ Suggested-Action / Candidate-Improvement / **Validation** types) | Advise | "decision", "action taken" |
| **ClarificationRequest** | Advise | "question" (when it's the object) |
| **SuggestedFix** | Advise (candidate); **user applies** (no autonomous OSLO write) | "auto-fix", "applied edit by OSLO" |

## DL-046 / DL-047 additions

| Canonical term | Meaning | Banned / not this |
|---|---|---|
| **Fast Pass** | Latency-bound first pass → Orientation-stage confidence + initial MRI, **< 60s Time-to-First-MRI**. | "quick scan" |
| **Deep Pass** | Async, coalesced, event-triggered expansion. **Never blocks the user.** | "full scan", "background job" (loosely) |
| **confidence_stage / Understanding State** | Orientation → Expanded → Validated (a.k.a. Initial→Partial→Refined→Validated→Mature). Emission attribute, **not** a new object. | "status" |
| **SynthesizedPlanningModel** | Derived planning model constructed from Attested assertions. | "the plan" (bare) |
| **PlanningArtifact** | Derived, **generated**, user-editable: Intent · Context · Scope · Requirements · WBS · Resources · Schedule. A user edit = **new Attested input → recompute** (not in-place mutation). | "document" (when it's this object), "Attested artifact" |
| **ReviewRequest / StakeholderResponse** (CRR) | Stakeholder review; a submitted response = **evidence** (Perceive) → triggers Deep Pass. | "approval workflow" (the cognitive seam is not commodity) |
| **ChatSession / ChatExchange** | Disclose-class interaction; consumes/triggers cognition, **writes no canonical, changes no assessment**. | "assistant that edits" |
| **Time-to-First-MRI** | The one ratified numeric target: **< 60 seconds** (Master Spec §20/M1). | any other latency name for this |

## Subscription tiers (canonical names — owner-set 2026-06-05)

| Tier | Canonical name | Banned / not this |
|---|---|---|
| **Tier 1** | **Free** | "freemium tier" (as a name), "starter" |
| **Tier 2** | **Basic** | "Lite", "Standard", "Plus" |
| **Tier 3** | **Pro** | "Premium", "Professional", "Advanced" |
| **Tier 4** | **Team** | "Business", "Group", "Squad" |
| **Tier 5** | **Enterprise** | "Org", "Custom", "Corporate" |
| **(non-consumer)** | **Internal** | "test tier", "admin tier", "god mode" — a **non-consumer** test-bypass entitlement, **not** part of the 1–5 ladder |

Tiers are a **tier-keyed config dimension** (DL-048 §4c + CHG-056 envelope): each knob (project-size envelope, active projects, Deep/day, fix·chat caps, model routing, token budget) is set **per tier**, increasing up the ladder. Use `tier` as the config/telemetry key; values for **Tier 1 (Free)** and **Tier 2 (Basic)** are owner-confirmed (Calibration §4c), **Tiers 3–5 (Pro · Team · Enterprise) are TBD** (Open-TBD A1/E3; ladder draft in `01_governance/backlog/BACKLOG_TIER_PROGRESSION_MONETIZATION_EXPERIENCE.md`). **Do not hard-code tier behavior** — read it from config.

## Canon — outcome family (DL-050)

| Canonical term | Meaning (one line) | Banned / not this |
|---|---|---|
| **Outcome Orchestration** | **The discipline/category OSLO creates** — continuously governing outcome integrity as work, context, and understanding evolve. | — |
| **Outcome Integrity** | Coherence between **Intended Reality** and **Current Reality** (DL-002). | "outcome correctness" |
| **Outcome Confidence** | Evaluate's confidence in the *understanding* of an outcome (Derived; maturity, **not** probability). | "success probability" |
| **~~Outcome Management~~** | **RETIRED (DL-050, 2026-06-05).** Not a canonical concept. **"Management" implies acting on/coordinating work — which OSLO does NOT do** (advise-never-act). | **banned** → use **Outcome Orchestration** (discipline) or **Outcome Integrity** (the coherence sense); historical references map into the Outcome Orchestration framework. |

## Modes that are NOT cognition (don't contract as such)

**Commodity / platform** (DL-043 J, Categories C/E/F — normal engineering, not cognition-contracted): auth, RBAC, project CRUD, settings, notifications-**state**, sharing, monetization/limits, product telemetry, the CRR **workflow UI** (the cognitive response→Deep-Pass seam *is* contracted). **Render** is a non-cognitive service. **Authority** is specified-but-inactive in R1 — do not build it.

## Disambiguation Register — one word, many senses (DL-053)

Some words carry **different concepts across frames** — OSLO-the-**product**, the **build** process, and the
**repository governance** process. **Rule: never use the bare colliding word where the frame is ambiguous; use the
qualified canonical form below.** (This register *qualifies* — it does not redefine the underlying concepts.)

**Process-word collisions:**

| Bare word | Sense → **canonical qualified name** | Frame |
|---|---|---|
| **Governance** | OSLO governing its own outputs → **Authority-Plane Governance** *(specified, INACTIVE R1)* | product |
| | engineering ship-controls (CI gates, deploy) → **Build-Governance** | build (`00_owner/build_governance`) |
| | Framework-001 / DL- ratification process → **Repository Governance** | repo-process |
| **Gate** | canonical-admission / inactive Authority gate → **Integrity Gate** | product |
| | CI · exit · owner · readiness gate → **Build Gate** | build |
| **Review** | OSLO CAF stakeholder review → **ReviewRequest (CRR)** | product |
| | Framework 001A review → **Governance Review** · code review → **Code Review** | repo / build |
| **Decision** | OSLO governance-decision object → **Governance Decision (object)** | product |
| | ratified repo decision → **Ratified Decision (DL-)** | repo-process |
| **Authority** | OSLO Authority Plane → **Authority Plane** *(INACTIVE R1 — do not build)* | product |
| | owner's ratification right → **Owner Authority** | repo-process |
| **Validation** | OSLO validation response → **Validation (Recommendation type)** | product |
| | QA validation → **QA Validation** | build |
| **Acceptance** | user-attested → **UserAcceptanceRecord** · target met → **NFR Acceptance** | product / build |
| **State** | product maturity → **Understanding State** · machine status → **run state** (`run_status`) | product / eng |
| **Policy** | OSLO product policies → **Product Policy** · build constraints → **Build-Policy** | product / build |

**Semantic landmines** (same word, unrelated/opposite meaning):

| Bare word | Sense A | Sense B | Rule |
|---|---|---|---|
| **Canonical** | "Canonical = Attested" (truth tier) | the dedup field → **`dedup_key`** (renamed, DL-053) | "Canonical" = truth tier only; never name the act "make canonical" for dedup |
| **Drift** | **Outcome Drift** — understanding changed, *surfaced as value* (feature) | **Determinism Drift** — *a bug that fails the build* | bare "Drift" banned; always qualify |
| **Model** | **Domain Model** (`CONFIDENCE_MODEL` — conceptual, no formula) | **Data Model** (schema) · **Scoring Model** (formula) · **LLM model** | bare "Model" banned in specs; qualify which |
| **Attested / Derived** | doctrine concepts (truth vs interpretation) | the `epistemic_state` field value | concept stays capitalized; the column is `epistemic_state` |

> **Structural reinforcement (DL-053):** the product Authority-Plane governance artifact is named
> `AUTHORITY_PLANE_MODEL_V1` (renamed from `GOVERNANCE_MODEL_V1`) so the product sense is unmistakable; the
> dedup field is `dedup_key` (renamed from `canonical_key`). doc-integrity WARNs on bare colliding words in active specs.

---
*This glossary fixes one canonical name per concept across the epistemic core (Attested/Derived, the assertion + record types), the seven cognitive responsibilities, the cognition outputs (Finding/Issue/Confidence/CAF/Recommendation/SuggestedFix), and the DL-046/047 additions (Fast/Deep, confidence stages, SynthesizedPlanningModel, PlanningArtifact, CRR objects, Chat, Time-to-First-MRI), listing the banned synonyms beside each so an external team/LLM cannot silently drift terminology; it also marks what is commodity/non-cognition so those terms aren't mistaken for governed concepts.*

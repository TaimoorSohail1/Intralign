# PROPOSAL — The Strategic Chain & Onboarding Positioning (Understanding → Judgement → Decision → Oversight)

> **DRAFT for owner ratification (Framework 001).** AI-drafted at owner direction; AI analyzes/recommends, the **owner ratifies**. Route: Backlog → **Proposal (this)** → Review → Decision → Change (glossary + positioning) → Changelog. Introduces **no** new responsibility, object, epistemic invariant, or implementation. **Now bundles the onboarding positioning + product descriptor** (§ below) as one ratifiable package.

- **Date:** 2026-06-30 (rev. 2026-07-01) · **Status:** Proposed (owner direction 2026-06-30; onboarding positioning 2026-07-01) · **Class:** A (positioning/doctrine orientation)
- **Layer:** Positioning + doctrine orientation — `10_product/scope` (positioning) and a `00_owner/CANONICAL_GLOSSARY` Disambiguation entry. **Non-structural.**
- **Grounded in:** DL-043 ("Integrity, not Authority"), advisory-only (DL-047 / Positioning §9), Outcome Orchestration (DL-050), the cognition lifecycle (Perceive→…→Disclose), DL-053 (Disambiguation Register).

## Proposal

Adopt the **strategic chain** as the canonical articulation of *what makes planning strategic* — and of **OSLO's role within it**:

> **Understanding → Judgement → Decision → Oversight**

The chain is a **human-facing positioning frame**, not an OSLO architecture relabel. Its power for the strategic-PM audience is the clean division of labor it expresses, which OSLO's doctrine already implies:

| Stage | The strategic act | OSLO's role | Canon mapping | Owner |
|---|---|---|---|---|
| **Understanding** | Know what the plan is and where it's weak | **OSLO does this** | Perceive→Infer→Evaluate → CAF · Reliability · Confidence · MRI · Findings | OSLO |
| **Judgement** | Weigh findings and options | **OSLO supports** (never performs) | Evaluating Recommendations; epistemic acceptance (DL-043) | The PM |
| **Decision** | Commit a path | **OSLO records** (never makes) | Accept a Recommendation → Selected Path → **Plan Fact** (Attested, attested-user) | The PM |
| **Oversight** | Watch outcomes; re-judge as reality moves | **OSLO surfaces** (read-only) | Outcome Integrity / Drift · reanalysis · Acceptance-Impact (Wave U) · execution-monitoring (R2) | The PM |

**Positioning thesis:** *OSLO supplies the Understanding; the strategic PM brings Judgement, Decision, and Oversight — and OSLO instruments each step without taking it over.* This **reinforces** advisory-only rather than straining it.

## Banned-term resolution (the one real conflict)

`CANONICAL_GLOSSARY` (DL-053) bans **"Judgment"** as a *primary identifier* — it is a **retired OSLO layer name** (Reasoning · Judgment · Governance · Communication), superseded by the seven cognitive responsibilities. The strategic chain uses **"Judgement"** in a **different sense**: the *human strategic act*, not an OSLO cognitive layer.

**Resolution (required condition):** add a Disambiguation Register entry so the two senses never drift:

| Word | Sense A (this proposal) | Sense B (banned) |
|---|---|---|
| **Judgement / Judgment** | **Strategic Judgement** — the *human* act of weighing OSLO's understanding (positioning) | **~~Judgment Layer~~** — retired OSLO cognitive layer; **banned** as a primary identifier (use **Evaluate**) |

OSLO's cognition responsibilities are **unchanged**; OSLO never gains a "Judgement" stage.

## Related user-facing label mapping (owner direction 2026-06-30)

Alongside the chain, the owner directed friendlier **user-facing** labels for the DL-046 analysis passes. This is a **presentation label** change only — the internal DL-046 terms stay in specs, code, and contracts. Add a Disambiguation Register entry:

| User-facing label | Canonical (internal, unchanged) |
|---|---|
| **Initial Analysis** | **Fast Pass** / *Fast Analysis Pass* (DL-046) — produces the 60-Second Orientation |
| **Extended Analysis** | **Deep Pass** / *Deep Analysis Pass* (DL-046) — runs automatically after orientation; expands understanding |

Rationale: least drift from DL-046 (keeps "Analysis"); "Extended" fits Deep's *"continues/expands understanding"* meaning; and **"Review" is deliberately avoided** — it would collide with the human **Judgement** role (this chain) and with the canonical **CAF Review Requests (CRR)** object. Advisory-only preserved (OSLO analyzes; it does not "review").

## Onboarding positioning & product descriptor (owner direction 2026-07-01)

The strategic chain is the doctrinal basis for how OSLO is **positioned to users**. Owner-approved framing (full copy in `OSLO_ONBOARDING_POSITIONING_DRAFT.md`, applied illustratively in the `product-design/` prototype):

- **Spine:** *OSLO makes you a more strategic PM* — the human is the operator (Judgement · Decision · Oversight); OSLO supplies the **Understanding**. A direct, user-facing expression of this chain.
- **AI-first PM capability:** onboarding frames OSLO as enabling the PM's transformation into an **AI-first PM** — leading with AI-grade understanding at their side, *augmented, never on autopilot*. This is an **augmentation** claim (reinforces advisory-only), never automation/replacement. It is **distinct from** the internal **AI-First delivery** term (engineering build governance). **Owner decision (2026-07-01): keep "AI-First delivery" internal — user-facing positioning uses only "AI-first PM."** Add a Disambiguation entry:

| User-facing term | Canonical (internal, unchanged) |
|---|---|
| **AI-first PM** — a project manager who leads augmented by OSLO's understanding (user positioning) | **AI-First delivery** — build/delivery governance rules (`00_owner/build_governance/`); unrelated scope |
- **Product descriptor (user-facing):** **"Strategic project leadership"** replaces "Planning Intelligence" under the OSLO wordmark. This is a **presentation label only** — the internal/technical descriptor is unchanged. Add a Disambiguation Register entry:

| User-facing descriptor | Canonical (internal, unchanged) |
|---|---|
| **Strategic project leadership** (product tagline) | *Planning Intelligence* — governed cognitive architecture in the **Outcome Orchestration** category (DL-050; repository manifest) |

- **Outcomes language (bounded):** onboarding may say the user *"steers toward the outcomes you want."* Outcomes are always **human-attributed**; OSLO is never framed as predicting, delivering, or guaranteeing outcomes (Confidence ≠ success probability; advisory-only).
- **Teaching surfaces:** onboarding hero copy · a **one-time orientation** presenting this chain (shown once, not persistent) · in-flow analysis interstitials · dismissible first-project coach tips.
- **Voice/audience:** confident & credible (executive), for PMs who want to be more strategic; hook = *the strategic layer above your task tools* (not another tracker).

## Conditions (binding if ratified)

1. **No structural change** — the seven responsibilities, the epistemic invariants (Attested/Derived, CAF, Confidence, recompute/CHR), and the object model are untouched.
2. **Advisory-only preserved** — OSLO never *performs* Judgement, Decision, or Oversight; it supports/records/surfaces. The chain must never be drawn as OSLO acting on the world.
3. **Disambiguation entry** added (above) to prevent collision with the banned layer term.
4. **UI usage** of the chain is **human-side framing** (orientation/positioning), not a relabel of OSLO's cognition stages.
5. **Descriptor is positioning-only** — "Strategic project leadership" is a user-facing tagline; the **Outcome Orchestration** category and the internal "Planning Intelligence / governed cognitive architecture" descriptor are unchanged.
6. **Bounded outcomes claim** — user-facing copy attributes outcomes to the **human** and never presents OSLO as predicting/delivering/guaranteeing outcomes or as project health/readiness/success probability (Confidence Doctrine).
7. **AI-first = augmentation** — the "AI-first PM" framing means the PM is *augmented* (they make every call); it never implies OSLO automates, replaces, or performs the PM role. Kept distinct from internal "AI-First delivery" via the Disambiguation entry above.
8. **Control-anchored copy (future-safe)** — user-facing promises anchor on **human control** ("you decide; you stay in control; nothing changes without you"), not on **capability negations** ("never runs/executes your project"). Rationale: OSLO's roadmap includes execution and outcome-validation; a capability-negation promise would eventually contradict the product, whereas a control/human-in-the-loop promise stays true across releases and reinforces advisory-only + augmentation. All app copy was swept to this standard (2026-07-01).

## Concerns

- **Term collision** with the banned "Judgment" — mitigated by Condition 3, but worth owner attention.
- **Side-conflation risk** — the chain spans OSLO-side (Understanding) and human-side (the rest); presentation must keep the split explicit or it muddies advisory-only.
- **Doctrine scope** — this is positioning/doctrine orientation; per current governance discipline ("do not introduce new doctrine" without owner direction), it proceeds **only** on the owner direction recorded here.
- **Outcomes-claim drift** — "steer toward the outcomes you want" is potent but sits near the doctrine line; sub-copy and Condition 6 keep it human-attributed. Worth owner attention that marketing/UI never harden it into a results promise.
- **Descriptor divergence** — a user-facing "Strategic project leadership" tagline that differs from the internal "Planning Intelligence" descriptor must be kept reconciled via the Disambiguation entry so the two never drift into competing category claims.

## Recommendation

**Accept-in-substance as positioning doctrine, with Conditions 1–8.** It is a strong, on-doctrine articulation for the strategic-PM audience — the strategic chain plus the onboarding positioning and "Strategic project leadership" descriptor codify the human/OSLO division DL-043 already implies. Owner ratifies; on ratification it lands as a Positioning addition + the glossary Disambiguation entries (analysis-pass labels + product descriptor), with a Changelog record.

## Provenance

Owner direction 2026-06-30 to formalize the strategic chain and align UI framing to it; 2026-07-01 to fold in the onboarding positioning and product descriptor as one package. AI drafted, mapped to canon, and surfaced the banned-term and outcomes-claim risks (Framework 001A — analysis / conflict identification / recommendation). The **owner ratifies**. Clearly-marked, non-canon prototype copy accompanies this proposal (`OSLO_ONBOARDING_POSITIONING_DRAFT.md` + the `product-design/` prototype) for evaluation only.

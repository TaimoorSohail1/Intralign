# DRAFT DL — Ratify "Living Hypothesis" as a canonical term

> **Status: DRAFT for owner ratification.** AI-authored proposal under Framework 001. Only the owner ratifies and lands (dl-land / Founder Console). This packet is self-contained: proposed canon → review (five outputs) → decision body for dl-land → landing steps. Origin: onboarding-arc storyboard, Decision 2 (owner, 2026-08-08).

## 1. Backlog framing
The onboarding narration (Scene 2) names a plan a **"living hypothesis for how the outcome will be achieved."** The *concept* is already doctrine (evolving-understanding: a plan is revisable, not truth), but there is **no canonical term** for it — a grep of canon returns zero hits for "living hypothesis." Introducing it in product copy without ratifying it would create an un-governed synonym, against the DL-053 disambiguation discipline. This proposal ratifies the term so it is canon, not drift.

## 2. Proposed canon
**Intended homes:** `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register) and `00_owner/canonical_definitions/canonical_definitions.md`.
**Proposed definition:**

> **Living Hypothesis** — OSLO's canonical framing of a project plan: a plan is a **provisional, revisable hypothesis for how the outcome will be achieved**, not a fixed truth or a guarantee. It is the artifact OSLO reads as *evolving understanding* — surfacing what rests on evidence versus OSLO's inference, so the plan can be continuously judged and steered toward the outcome. A plan's status as a living hypothesis is why maturity (not a forecast) is the honest read, and why grounding/adaptability are first-class: the hypothesis strengthens as evidence replaces inference and as it adapts to change.
>
> *Relation to existing canon:* the operational expression of the **evolving-understanding** philosophy; consistent with maturity-not-forecast (the band reads how sound the hypothesis is, never a probability) and with **Outcome Orchestration** (continuous judgment over a living hypothesis toward a fixed outcome). Not a synonym for "plan document" (the artifact) — it names the plan's epistemic *status*.

## 3. Review (Framework 001A — five outputs)
- **Findings:** The term fills a real lexical gap (concept is canon; term is not). It is doctrinally load-bearing for onboarding (Scene 2) and for the three-pillar honesty story.
- **Concerns:** (a) Risk of it reading as a *competing* term to "evolving understanding" — mitigated by defining it as that philosophy's operational expression, not a rival. (b) "Hypothesis" could imply a scientific-test rigor OSLO doesn't claim — mitigated by "provisional, revisable… for how the outcome will be achieved," which is intent, not experiment.
- **Dependencies:** evolving-understanding philosophy; maturity-not-forecast doctrine; Outcome Orchestration; the DL-053 disambiguation register (add the term there).
- **Recommendation:** **Adopt** as a canonical term with the definition above; add to the glossary + disambiguation register. Low blast radius (additive, no existing definition changes).
- **Status:** Ready for owner ratification. Blocking questions: none.

## 4. Decision record body (for dl-land)
```
title: Ratify "Living Hypothesis" as a canonical term
slug: living-hypothesis-canonical-term
class: A
decided_by: Idris (Founder Console)

## Decision
Adopt "Living Hypothesis" as a canonical term: a project plan is a provisional, revisable hypothesis for how the outcome will be achieved — not a fixed truth. It is the operational expression of the evolving-understanding philosophy and the artifact OSLO reads as evolving understanding (evidence vs. inference), continuously judged and steered toward a fixed outcome; consistent with maturity-not-forecast and with Outcome Orchestration. Add the term + definition to 00_owner/CANONICAL_GLOSSARY.md (Disambiguation Register, DL-053) and 00_owner/canonical_definitions/canonical_definitions.md. It names the plan's epistemic status, not the plan document (artifact).

## Status
Ratified.
```

## 5. Landing steps (owner runs — AI does not land canon)
1. Add the term to `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register) and `00_owner/canonical_definitions/canonical_definitions.md`, per the Git/Branch workflow (branch → PR → green doc-integrity → owner merge).
2. Land the decision via dl-land (numbers at merge; pass the §4 body via `$(cat body.md)`, not the web form):
   `gh workflow run dl-land.yml -R idris-manley/oslo-knowledge-base -f title="Ratify \"Living Hypothesis\" as a canonical term" -f slug="living-hypothesis-canonical-term" -f class="A" -f decided_by="Idris (Founder Console)" -f body="$(cat body.md)"`
3. Owner approves the bot PR (approve-workflows → code-owner review → squash) to merge.

_Note: staged in `release-2/` because that is the active line; the ratified term targets `00_owner/**` on the canon line. Landing to main vs. R2-isolated staging is an owner call (consistent with the open decision-log staging thread)._

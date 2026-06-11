# Recommendation 001 — Reconcile Master Spec §8 Recommendation Actions with the State Model Lifecycle Authority

**Document Type:** Conflict-reconciliation recommendation (analysis & recommendation only — non-canonical) · **Status:** Recommendation — owner decision required
**Date:** 2026-06-10 · **Author:** AI contributor (conflict identification + recommendation generation — per `CLAUDE.md` Authority Constraint)
**Surfaced by:** Review 001 (`ENV_REV_001_REVIEW_001.md`, Concern 6) and the end-to-end workflow diagram correction.

> **Non-canonical.** Lives in `90_research/` (informs but does not bind, DL-033). This identifies a conflict and recommends a resolution; it does **not** ratify, author, or amend canon. Only the owner may ratify, and the canonical edits route through Framework 001 (Proposal → Review → Decision → Change → Changelog).

---

## 1. The conflict

Two canonical sources describe what a user can do with a Recommendation, and they disagree.

- **Master Spec §8** (product source of truth): *"Recommendation actions include **Accept, Reject, Modify, Discuss, Apply, and Share For Review**."*
- **State Model §11** (`RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md`, the designated **lifecycle/behavior authority**): recommendation **states** are `Generated → Accepted → Rejected → Deferred → Implemented` plus `Superseded`. Clarification: *"Accept/Reject/Defer/Implement are user choices."* Data Model v1.2 enum is **aligned**: `{generated, accepted, rejected, deferred, implemented, superseded}`.

The divergences: §8 lists **Modify** and **Discuss** (neither is a State Model state); the State Model has **Deferred** (not in §8); and §8's **Apply** is the State Model's **Implemented**.

The State Model is explicit about precedence: *"Where a state name here differs from an enum value in the Data Model, this document governs the behavior."* So for **states**, the State Model already wins. The open question is what to do with §8's extra items.

## 2. Analysis — the lists are at two different layers

§8 conflates two distinct things: **state-changing actions** and **collaboration affordances**. Separating them resolves most of the conflict without a true contradiction.

| §8 item | Nature | Maps to |
|---|---|---|
| Accept | state-changing action | → `Accepted` (State Model) |
| Reject | state-changing action | → `Rejected` |
| Apply | state-changing action | → `Implemented` (rename: "Apply" is the verb, "Implemented" the state) |
| (Defer) | state-changing action | → `Deferred` (in State Model; **missing from §8**) |
| Modify | **not a state** | editing the recommendation/artifact → triggers Deep Pass → prior rec `Superseded` by a new `Generated` one |
| Discuss | **collaboration affordance** | OSLO Chat — not a recommendation state |
| Share For Review | **collaboration affordance** | CAF Review Request — not a recommendation state |

So: Accept/Reject/Apply(=Implement)/Defer are the **state transitions** (State Model authoritative); **Modify** is an edit that produces supersession, not a terminal state; **Discuss** and **Share For Review** are **collaboration affordances** that live alongside the lifecycle, not within it.

## 3. Recommended resolution (owner to ratify)

1. **Adopt the State Model §11 lifecycle as canonical for recommendation states** — `Generated → Accepted → Rejected → Deferred → Implemented (+Superseded)`. (Already the lifecycle authority; this just makes the precedence explicit against §8.)
2. **Amend Master Spec §8 prose** to: (a) **add Defer**; (b) **remove "Modify" from the action list** and instead describe editing as producing **supersession** (edit → Deep Pass → new `Generated`, prior `Superseded`); (c) **reclassify "Discuss" and "Share For Review" as collaboration affordances**, not recommendation actions, cross-referencing OSLO Chat (§9) and CAF Review Requests (§7/§14 Flow 11).
3. **Add a one-line pointer in §8** naming the State Model as the lifecycle authority for recommendation states, so the two never drift again.

Net canonical action set for a recommendation: **Accept · Defer · Reject · Apply (→ Implemented)**, with **edit→supersede** and the **Discuss / Share-for-Review** affordances available throughout. (This is what the corrected end-to-end diagram now shows.)

## 4. Why this and not the alternative

The alternative — amend the State Model to re-add "Modify"/"Discuss" as states — is wrong: it would inflate the lifecycle with a non-terminal "Modify" and conflate collaboration affordances with state, breaking the clean Data Model v1.2 enum (RS-R2/RS-R4) and the supersession model. The State Model is the lifecycle authority by ratified design; §8 is product-narrative prose that predates the RS-R3 "Deferred" ratification. Aligning §8 to the State Model is the lower-risk, precedence-correct direction (Doctrine > Constitution > Implementation; and among implementation docs, the State Model is the named lifecycle authority).

## 5. Owner decision required

- Ratify the precedence (State Model lifecycle is canonical for recommendation states).
- Approve the §8 prose amendment (add Defer; Modify→supersession; Discuss/Share→affordances; add the lifecycle-authority pointer).
- On ratification: route the §8 edit via branch → PR → green doc-integrity gate → owner merge; record a decision-log entry + changelog.

## 6. Dependencies / scope notes

- Touches **canonical** content (Master Spec §8) → owner ratifies; AI only recommends.
- No data-model change needed (Data Model v1.2 already matches the State Model).
- Independent of DL-054 (ENV-REV-001); can proceed on its own track.
- The corrected end-to-end workflow diagram already reflects the recommended action set, so no diagram rework is needed once this is ratified.

## 7. Status

**Recommendation — owner decision required.** Not ratified; AI analysis only (Authority Constraint).

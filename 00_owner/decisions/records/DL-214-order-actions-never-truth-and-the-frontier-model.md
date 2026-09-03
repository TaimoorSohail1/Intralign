# DL-214 — Finding-ordering honesty invariant ("order actions, never truth") + the finding-dependency / frontier resolution model

> ⚠️ **GRADUATED TO THE CONTROL PLANE 2026-08-31 — RATIFIED CONTENT UNCHANGED.**
> The body below is **byte-identical** to the record ratified 2026-08-11 and staged at
> `release-2/canon/decisions/DL-214_FINDING_ORDERING_HONESTY_AND_DEPENDENCY_MODEL.md`
> (md5 `ddadb605`). **This graduation executes an instruction the record itself contains** — its
> Placement line reads *"Staged in `release-2/`; folds to main product doctrine (`00_owner`) at
> graduation."*
>
> **Why it was needed.** `main` is the control plane and carries no release line, so a record living
> only under `release-2/` resolves on a release ref and **nowhere on `main`**. Every citation of this
> decision on the control plane therefore read as unresolved — measured 2026-08-31, when the citation
> gate rejected a document in `20_handoff/` for citing it.
>
> **Decision:** *Ordering may gate ACTIONS. It may never gate TRUTH.* (stated in full at §1 below).
>
> ⚠️ **TWO ADDITIONS, both declared, neither ratified content.**
> ① The `Decision:` line above — required by the records/ regime, which post-dates this record. It
> quotes §1 verbatim rather than paraphrasing, so the added field cannot drift from the ratified
> statement.
> ② The graduation-ripple section at the foot of this file — **not written at graduation.** It was
> authored **2026-08-13 under DL-220** and carries its own attribution line. It is restored here from
> `rescue/worktree-2026-08-19` (md5 `33fd34e3`), the only ref carrying it.
> ⚠️ This block deliberately does **not** spell that section's heading: a DL-220 check greps for the
> heading, and a note describing a section must not make the section look present. (RB-109's trap,
> caught before it landed rather than after.)
>
> ⚠️ **CORRECTION — an earlier draft of this header claimed the body was *"identical across every ref
> carrying it."* That is measurably false and is withdrawn.** Measured 2026-09-01 across all 221 refs:
> **`ddadb605` on 7 refs (no ripple) · `33fd34e3` on 1 ref (`ddadb605` + the ripple).** The two are not
> competing drafts — the second is the first plus the section **DL-220 makes mandatory**. Graduating
> the 7-ref majority unchanged would have carried a fourth DL-220 omission into `00_owner`, after the
> three already recorded against DL-230 and DL-231. **The section is restored, never re-authored;
> nothing in §1–§4 or the Changelog is touched.**

- **Date:** 2026-08-11 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (product doctrine — a Durable honesty invariant + a resolution-model extension).
- **Framework 001** — AI drafts; only the owner ratifies. Proposal: `release-2/BACKLOG_RB-047_finding-dependency-frontier-model.md` (RB-047), with its twelve-scenario acceptance suite and Framework-001 five-output review.
- **Basis:** owner-led critical assessment of the "Success metrics" multi-flaw use case (Alignment + Grounding on one element), a first-principles derivation of the multi-pillar resolution workflow, and an adversarial pressure-test (structural + honesty axes) that converged every failure mode on **disclosure and escalation**.
- **Placement:** the §1 invariant is a **Durable Invariant** (never regresses, re-asserted every release) — joins the registry beside **DL-213**. The §2 model is ratified **design direction**; its realization is an **Altering** build (F002 gate). Staged in `release-2/`; folds to main product doctrine (`00_owner`) at graduation. **This decision does not authorize/complete the build.**

---

## 1. The honesty invariant (Durable) — RATIFIED, binding now

> **Ordering may gate ACTIONS. It may never gate TRUTH.**

A finding-ordering layer must present as **two layers that never collapse**:
- **Truth layer — always complete.** Every load-bearing finding is disclosed: its **dimension**, its **exposure/severity**, and its **status** (actionable now · blocked-by-X · genuinely lower-stakes-deferred). **The gating finding is always visible.** Total count/depth is always honest. No load-bearing truth is ever removed from view.
- **Action layer — ordered.** Only a finding's **CTA** is sequenced; a blocked finding still shows its face, its exposure, and an honest reason.

Corollaries (also durable): **bias to disclosure** — when a prerequisite edge is uncertain, show findings as peers; suppressing an *action* needs high confidence, suppressing a *truth* is never allowed. **"Blocked" ≠ "lower stakes"** — never conflate deferred-because-minor with deferred-because-prerequisite-but-bigger.

Rationale: a frontier that *removes* downstream findings would make the read look calmer, shorter, and safer than it is — a dark pattern OSLO cannot ship. This is DL-213's honesty wall one level down: **the read may sequence what you do, never what you're allowed to know.** Extends `no-manufactured-confidence`, `level ≠ trust`, and the gate-honesty (`integrity = weakest pillar`).

## 2. The finding-dependency / frontier resolution model — RATIFIED design direction (Altering realization)

Topological-frontier resolution over a dynamically re-derived dependency graph of **atomic** findings (one deficiency · one dimension · one element, DL-210):
1. **Prerequisite edges** — `A → B` iff resolving B while A is open is *premature, wasted, or misleading*; no edge ⇒ **peers**.
2. **Frontier** — findings with no unresolved prerequisite; highlights the next **action** (subject to §1's truth layer).
3. **One act per finding** — never bundle `build` + `verify`. A build that outputs an *inferred claim* surfaces a downstream **Grounding** finding on reanalysis; a build that is a pure *decision/structure* surfaces none (`build → ground` is **conditional**).
4. **Re-derive on every act** — only reanalysis resolves (DL-211); edges may point any direction (grounding can create a Feasibility finding).
5. **Escalate the unclassifiable** — a finding OSLO can't place, or an ordering it can't derive.

**Amendments (from the adversarial pass — all the same escalation/honesty reflex):** cycle → **escalate to owner to set an anchor**; empty-frontier-with-open-findings → **escalate the blockage** (no dead-end); non-monotonic reopening → **carry provenance** ("reopened because X"); **accept ≠ fix but accept unblocks** (exposure stays live in the register); **the frontier is advisory, never a gate** (OSLO advises; you decide — any-order resolution reconciles via re-derivation).

## 3. Relationship to canon (extends, never contradicts)
- **DL-209** — only-verify-moves-Grounding (a build never grounds); escalate-the-unclassifiable. Preserved + generalized.
- **DL-210** — dimension-from-structural-target; **C→A→F precedence is a special case** of a prerequisite chain. Preserved.
- **DL-211** — itemize atomic findings; build/inference/optional; only-reanalysis-resolves. The frontier is the ordering layer over itemized findings.
- **DL-213** — honesty wall; §1 here is its resolution-surface analog.

## 4. Realization & obligations (routes via Framework 001/002 — NOT built by this decision)
- **Guards (via `guard-add`), pinned negatives:** *ordering never removes a load-bearing finding's exposure/visibility* · *the gate is always visible* · *no bundled build+verify resolution* · *blocked ≠ lower-stakes*. Plus the twelve RB-047 scenarios as acceptance (GT) cases.
- **Prototype gaps to close (current):** no dependency layer (exposure-only ranking); viability cards **bundle build+verify** (metrics), under-decomposing and hiding the grounding dimension.
- **Change class:** **Altering** (changes issue-layer behavior + adds GTs) → impact assessment + dev-lead sign-off via `release-refine` when built.
- **Open decisions remain owner-escalated (RB-047 §8):** deterministic-vs-judgment edge derivation (prefer structural; escalate/bias-to-peers when uncertain), client-oracle vs Slice-10 server placement, migration of bundled viability cards.

## Changelog
- New Durable Invariant (§1) registered beside DL-213. Frontier model (§2) ratified as design direction; realization is Altering. RB-047 status → Ratified (DL-214). Add to the R2 decision index + Durable Invariant Registry.

## Graduation ripple
- **Main-canon documents touched:** `FINDING_SYSTEM_SPECIFICATION_V1` (new structure: finding-dependency edges + frontier; a blocked finding is disclosed at its REAL severity) · `MRI_MODEL_V1` (the frontier orders ACTIONS, never truth) · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1` (next-best-action derives from the frontier; advisory, never a gate)
- **Amends / extends an earlier decision:** no — extends DL-209/210/211
- **Class:** AMEND — the largest net-new structure of the R2 set

*Backfilled 2026-08-13 under DL-220; ratified with the `R2_TO_MAIN_GRADUATION_INDEX.md` drafts.*

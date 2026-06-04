# Recommendation / Finding Coupling Specification v1

**Type:** Implementation specification (narrow) — resolves the §11a/§11b coupling backlog
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` (§11a/§11b) · Recommendation Model v1 · Finding Model · CAF Scoring v2 · Confidence v2 · Reliability v2 · State Model · Data Model v1.1.
**Resolves:** Recommendation System Spec §11a (Finding/Recommendation Coupling Backlog) and §11b (Alternative Recommendation Paths Backlog).

> **Scope (narrow).** This document answers **only** how recommendations behave when their source findings change, and how recommendation↔finding multiplicities coexist. It introduces **no scoring, ranking, automation, agents, governance, or execution**, modifies **no** CAF/Reliability/Confidence/Finding/Data/State model, and creates **no new doctrine**. Coupling outcomes are **lifecycle bookkeeping** (supersession), **not** project actions; **only users perform actions** and **assessment changes only through reanalysis** (Recommendation System Spec §3/§11).

---

## 1. Purpose & Scope

A recommendation always **traces to one or more findings** (Recommendation System Spec REC-1/REC-8). When a source finding's lifecycle state changes, the recommendation's coupling to it must be well-defined so the system never holds an **unattributed**, **opaque**, or **silently deleted** recommendation. This document defines that coupling for the five finding state-changes and for the two multiplicities, and nothing else.

**Finding states referenced** (Data Model v1.1 `Finding.status`, unchanged): `detected · acknowledged · addressed · closed · reopened · superseded` (plus *removed* — a finding determined invalid / no longer present).
**Recommendation states referenced** (Recommendation System Spec §8, unchanged): `generated · presented · accepted · rejected · deferred · completed · superseded`.

---

## 2. Coupling Principles

- **Attribution is mandatory and continuous.** A recommendation must, at all times, trace to **≥1 finding**; if it can no longer trace to any active finding, it is **superseded** (never left unattributed, never deleted) (REC-1/REC-6/REC-8).
- **Append-only.** Coupling responses are **supersession** transitions; superseded recommendations are **retained**, never overwritten or resurrected (REC-6/REC-11).
- **Bookkeeping, not action.** A coupling transition (e.g., superseding a recommendation whose finding was removed) is **lifecycle bookkeeping**, not a project action and not execution — it changes **no** CAF/Reliability/Confidence signal (REC-2/REC-3/REC-9/REC-10).
- **Triggers live in the Event/reanalysis flow.** *Finding state change → recommendation coupling response* is carried by the existing event/reanalysis loop; **this spec defines the response, not the trigger mechanism** (Recommendation System Spec §3).
- **Explainability preserved.** After any coupling transition, the recommendation remains explainable, showing which source findings are active vs resolved and what last changed its state (REC-5).

---

## 3. Finding State-Change Coupling Rules

For a recommendation **R** and a source finding **F** (where F is among R's `finding_references`):

### 3.1 F is **superseded**
F has been replaced by a newer finding F′ (e.g., a deep run reassessed it).
- If R traces **only** to F → **R is superseded** (its basis is no longer current); retained in history. If F′ still warrants a recommendation, a **new** recommendation is generated for F′ (not a resurrection of R).
- If R traces to F **and** other still-active findings → **R persists**, **re-attributed** to its remaining active findings (and to F′ if applicable); R is superseded only if **no** active source finding remains (§4).

### 3.2 F is **closed**
F is resolved / no longer an open concern.
- If R traces **only** to F → **R is superseded** (its work is no longer applicable); retained. *If F closed as a result of the user acting on R and reanalysis weakening/removing F, that is **success** per Recommendation System Spec §11 — recorded as the success condition, not a new state.*
- If R traces to F and other active findings → **R persists**, re-attributed to the remaining active findings.

### 3.3 F is **reopened**
A previously `closed` F returns to active.
- **No recommendation is resurrected** (append-only). Instead, a **new** recommendation **may be generated** for the reopened F by the normal generation model (Recommendation System Spec §6); any earlier recommendation that was superseded when F closed remains in history.

### 3.4 F is **removed**
F is determined invalid / no longer present.
- If R traces **only** to F → **R is superseded** (it has lost its basis); retained.
- If R traces to F and other active findings → **R persists**, re-attributed to the remaining active findings; superseded only if none remain (§4).

### 3.5 F is **weakened**
F still exists but its severity/impact is reduced (still `detected`/`acknowledged`/`addressed`).
- **R persists and remains coupled** — weakening alone does **not** supersede R, because the finding still exists and the improvement opportunity remains.
- R's `rationale`/`expected_impact` may be **re-inherited/refreshed** by the normal generation cycle on reanalysis (consumed from the updated finding, not recomputed here). No state change is required by weakening alone.

**Summary table**

| Finding change | R traces only to F | R also traces to active findings |
|---|---|---|
| **Superseded** | R → superseded (new rec may be generated for F′) | R persists, re-attributed |
| **Closed** | R → superseded (success if via action+reanalysis, §11) | R persists, re-attributed |
| **Reopened** | new rec may be generated (no resurrection) | unchanged for R; new rec may be generated |
| **Removed** | R → superseded | R persists, re-attributed |
| **Weakened** | R persists (coupled; rationale may refresh) | R persists |

---

## 4. One Recommendation → Multiple Findings

When R traces to multiple findings:
- **R persists while it traces to ≥1 active source finding.** "Active" = not removed, not superseded, not closed.
- **Re-attribution on change.** When some of R's source findings change state, R's effective attribution is the **set of its remaining active source findings**; R is **superseded only when none remain active** (Attribution-mandatory principle, §2).
- **Explainability.** R must expose, per source finding, whether that finding is **active or resolved**, so it is never ambiguous *why* R still exists or *why* it was superseded (REC-5).
- **No merging/splitting** of recommendations is defined here (out of scope); R simply tracks its source-finding set.

---

## 5. Multiple Recommendations → One Finding (Alternative Paths)

Recommendation Model v1 (Example C) affirms **multiple valid improvement paths** for a single finding. Coupling rules:
- **Parallel valid options by default.** Multiple recommendations addressing one finding **coexist** as parallel valid options; they are **not mutually exclusive by default**.
- **Independent user choice.** A user **may accept one while leaving the others open** (e.g., `deferred`/`presented`); accepting or completing one recommendation does **not** auto-reject the others.
- **Resolution supersedes the remaining alternatives.** When the shared finding is **resolved** (closed/removed, or weakened-to-resolution via reanalysis after the accepted action), the **still-open alternative recommendations for that now-resolved finding are superseded** (their opportunity is gone); retained in history.
- **No ranking among alternatives.** This spec does **not** order, score, or auto-select among alternatives — selecting/ordering among valid paths is **Deferred** (§8). Prioritization remains the conceptual ordering of Recommendation System Spec §7.
- **Mutual exclusivity is not asserted.** Whether specific alternatives are *inherently* mutually exclusive (beyond shared-finding resolution) is **not** modeled in Release 1 (§8) — by default they coexist until the finding resolves.

---

## 6. Coupling Integrity Rules

*Structurally testable; each realizes existing doctrine; none is new doctrine.*

- **RFC-1.** A recommendation must always trace to **≥1 active source finding**, or be **superseded** (never unattributed, never deleted).
- **RFC-2.** Coupling transitions are **supersession** (append-only); superseded recommendations are **retained** and **never resurrected** (reopen → new recommendation).
- **RFC-3.** A coupling transition changes **no** CAF/Reliability/Confidence signal (bookkeeping only).
- **RFC-4.** **Weakening** of a source finding does **not** supersede a recommendation.
- **RFC-5.** A multi-finding recommendation is superseded **only** when **none** of its source findings remain active; otherwise it persists, re-attributed.
- **RFC-6.** Multiple recommendations for one finding **coexist** as parallel options; resolving the finding supersedes the remaining open alternatives.
- **RFC-7.** No alternative is auto-selected, ranked, or scored against another (Deferred).
- **RFC-8.** After any coupling transition, the recommendation remains **explainable**, exposing per-source-finding active/resolved status and the cause of its last state change.
- **RFC-9.** Coupling responses are driven by the **existing event/reanalysis loop**; no trigger mechanism, automation, or autonomous action is introduced here.

---

## 7. Conformance Requirements

A conforming implementation MUST (structural — **no percentages, thresholds, or pass-rate language**):
- **C-1.** Re-evaluate a recommendation's attribution when any source finding changes state, applying §3–§5 (RFC-1/RFC-5).
- **C-2.** Supersede (never delete) a recommendation that loses all active source findings; retain it (RFC-1/RFC-2).
- **C-3.** Generate a **new** recommendation (not resurrect) on finding reopening, if warranted (RFC-2; §3.3).
- **C-4.** Preserve recommendation coexistence for shared findings and supersede remaining alternatives only on finding resolution (RFC-6; §5).
- **C-5.** Guarantee no coupling transition alters CAF/Reliability/Confidence (RFC-3).
- **C-6.** Keep every post-transition recommendation explainable with per-finding active/resolved status (RFC-8).
- **C-7.** Introduce no ranking/auto-selection among alternatives (RFC-7).

Conformance is **all-or-nothing on these rules**; any unattributed/deleted/resurrected recommendation, any coupling-induced assessment change, or any auto-selection among alternatives **fails conformance**.

---

## 8. Deferred Items

Explicitly **Deferred** (Release 1 does not define; out of this narrow scope):
- **Ranking / selection among alternative recommendations** — ordering or choosing among parallel valid paths.
- **Inherent mutual-exclusivity modeling** — declaring specific alternatives mutually exclusive beyond shared-finding resolution.
- **Recommendation merging/splitting** behavior.
- **Effectiveness analytics** — measuring coupling/resolution outcomes over time.
- **Automation** of any coupling response beyond deterministic lifecycle bookkeeping.

These remain future work and must, if defined, conform to this spec and the doctrine/model layers above it, introducing no scoring/automation/governance/execution into Release 1.

---

## 9. Relationship to Resolution Candidate

This specification **unblocks** Resolution Candidate modeling (which the Recommendation System Spec §11a/§11b flagged as a prerequisite) by fixing how recommendations behave under finding change and multiplicity. It **does not** model Resolution Candidate, Disposition, Governance, or any Future-Architecture concept — those remain deferred and out of scope. Resolution Candidate modeling, when undertaken, consumes this coupling behavior; it does not redefine it here.

---

*This document narrowly resolves recommendation/finding coupling for Release 1: attribution-continuous, append-only, explainable, bookkeeping-only. It changes no CAF/Reliability/Confidence/Finding/Data/State model, introduces no scoring/automation/governance/execution, and defers ranking, mutual-exclusivity, merging, and analytics. It resolves Recommendation System Spec §11a and §11b.*

**Recommendation / Finding Coupling Specification v1 complete.**

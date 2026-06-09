# Finding System Specification v1

**Type:** Implementation specification — the canonical Release 1 Finding model (descriptive object)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** Finding Model v1 (founder positions) · CAF Assessment Model · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` · `CONFIDENCE_MODEL_V2.md` · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` · State/Data/Event Models v1.1.

> **Non-negotiable.** Findings are **descriptive, not prescriptive** — they identify; they never suggest actions (Recommendations do that). Findings **never directly modify CAF, Reliability, or Confidence**; they **contribute evidence consumed by CAF Scoring** (via Impact Assessment), and CAF changes only through **assessment/reanalysis**. **No governance** (no Resolution Candidate, Accepted Understanding, Governance, Disposition) and **no execution** (no agents, automation, project execution) concepts are introduced. Findings are **append-only**, **explainable**, and **human-readable** first-class user-facing objects.

---

## 1. Purpose

This document is the **authoritative Release 1 Finding model**: what a Finding is, how it is represented, generated, attributed, explained, evolved (lifecycle/supersession/history), how it relates to CAF/Reliability/Confidence/Recommendations, and the integrity/conformance rules that govern it. It implements the Finding Model founder positions as an operational system reference for engineering and testing.

---

## 2. Scope

**In scope:** Finding definition, representation, generation, attribution, explainability, lifecycle, supersession, history, the Finding↔CAF/Reliability/Confidence/Recommendation relationships, integrity rules, and conformance.

**Out of scope (Deferred / owned elsewhere):** CAF scoring arithmetic (CAF Scoring v2), Reliability/Confidence behavior (their v2 models), Recommendation behavior (Recommendation System Spec), severity numeric calibration, UI design, and **all governance/execution concepts**.

---

## 3. Model Relationships

```text
Evidence ─▶ Inference ─▶ FINDING (descriptive) ─▶ Impact Assessment ─▶ CAF (via CAF Scoring v2)
                                │                                         (+ Reliability, determined independently)
                                │                                              ─▶ Confidence (consolidate-then-qualify)
                                └─▶ Recommendation (prescriptive; originates from the finding)
```

- A Finding **contributes to CAF** only through its **Impact Assessment** (CAF Scoring v2 §5/§7); it **never** modifies a CAF dimension directly.
- A Finding **does not influence Reliability** — Reliability is determined independently from Coverage/Evidence Availability/Assessability, **not from findings** (Reliability v2 RR-2).
- A Finding **reaches Confidence only through CAF** (Confidence v2 IR-6); it **never** modifies Confidence directly.
- A Finding is the **origin of Recommendations** (Recommendation System Spec REC-1) and, transitively, of a recommendation's **Possible Resolution Paths**.

---

## A. Finding Definition

> **A Finding is a descriptive observation about the integrity of project understanding** — it identifies *what is unclear, unsupported, conflicting, constrained, or incomplete* in the understanding. It **states a condition; it never prescribes an action.**

A Finding identifies conditions such as: **ambiguity, conflict, assumption, dependency issue, constraint issue, coverage gap, and feasibility / alignment / clarity concerns**. A Finding **never suggests actions** — proposing what to do about a Finding is the job of a **Recommendation** (and its Possible Resolution Paths). Findings are **first-class, human-readable, user-facing objects**.

---

## B. Finding Representation

A Finding is represented with the following attributes (Data Model v1.1 `Finding`, consistent):

| Attribute | Meaning |
|---|---|
| `finding_id` | stable unique identifier |
| `project_id` | project scope |
| `finding_type` | the canonical flat taxonomy (below) |
| `affected_dimensions` | the CAF dimension(s) the finding bears on — array of `clarity` / `alignment` / `feasibility` |
| `severity` | `critical` / `moderate` / `warning` (descriptive; basis = a finding's Impact Assessment significance/scope, CAF Scoring v2 §6; numeric basis Deferred) |
| `status` | lifecycle state (§C) |
| `evidence_links` | the evidence / context items the finding is grounded in (≥1; attribution) |
| `artifact_id` / `artifact_version_id` | the artifact location it concerns (if applicable) |
| `rationale` | the human-readable explanation of the observed condition |
| `first_seen_run_id` | the analysis run that first produced it (deep ⇒ Expanded Finding) |
| `last_updated_run_id` | the run that last touched it |
| `supersedes_finding_id` | prior finding it supersedes (append-only chain), nullable |
| `created_at` / `updated_at` / `closed_at` | timestamps; history preserved |

**Canonical finding-type taxonomy** (flat; Finding Model Position #13 / Data Model v1.1 — authoritative; **not redefined here**):
`missing_information · ambiguity · assumption · inference · conflict · constraint · coverage_gap`.

**Mapping of the descriptive conditions to the canonical model** (presentation grouping — introduces **no** new `finding_type`):

| Condition (as described) | Canonical representation |
|---|---|
| Ambiguity | `finding_type = ambiguity` (affects Clarity) |
| Conflict / contradiction | `finding_type = conflict` (affects Alignment) |
| Assumption | `finding_type = assumption` (affects the underpinned dimension) |
| Dependency issue | `finding_type = constraint` or `coverage_gap` with `affected_dimensions ⊇ {feasibility}` |
| Constraint issue | `finding_type = constraint` (affects Feasibility) |
| Coverage gap | `finding_type = coverage_gap` |
| Clarity concern | any finding with `affected_dimensions ⊇ {clarity}` |
| Alignment concern | any finding with `affected_dimensions ⊇ {alignment}` |
| Feasibility concern | any finding with `affected_dimensions ⊇ {feasibility}` |
| (Missing information / Inference) | `finding_type = missing_information` / `inference` (canonical types) |

> *Note: "clarity/alignment/feasibility concerns" are expressed via **`affected_dimensions`**, not as separate finding types; "dependency issue" maps under `constraint`/`coverage_gap`. Any change to the canonical `finding_type` enum is a Data Model / Finding Model reconciliation, **not** made here.*

**Finding generation.** Findings are **generated by analysis runs** (Fast or Deep). A Fast run produces initial findings; a Deep run produces **Expanded Findings** (`first_seen_run_id` = the deep run) and may supersede prior findings (Planning Intelligence §6/§19; Analysis Engine §11). **Magnitude/locality** of a finding's effect on CAF is governed by its **Impact Assessment**, never by its type (CAF Scoring v2 §4).

**Finding attribution.** Every Finding **traces to ≥1 evidence/context item** (`evidence_links`) and to its producing run (`first_seen_run_id`). A finding **cannot exist unattributed**.

---

## C. Finding Lifecycle

States (State Model §10 / Data Model v1.1 — unchanged): `detected → acknowledged → addressed → closed`; `closed → reopened`; `{detected, acknowledged, addressed} → superseded`.

| State | Meaning |
|---|---|
| `detected` | surfaced by an analysis run |
| `acknowledged` | a user has accepted it as real |
| `addressed` | work targeting it has been done |
| `closed` | resolved — no longer an open concern |
| `reopened` | a closed finding returns to active (new evidence) |
| `superseded` | a run determines it no longer holds / replaces it (retained) |

**Transitions.** detected→acknowledged→addressed→closed; closed→reopened; {detected,acknowledged,addressed}→superseded. **Invalid:** detected→closed (must be addressed); superseded→any active (terminal). Findings remain **descriptive** in every state — a status describes the condition's status, never an action.

---

## D. Finding Explainability Model

Every Finding MUST expose (never opaque):
- **Source evidence** — the `evidence_links` (evidence/context items) it is grounded in.
- **Rationale** — the human-readable explanation of the observed condition.
- **Affected CAF dimensions** — `affected_dimensions` (which of Clarity/Alignment/Feasibility it bears on).
- **Finding type** — the canonical `finding_type`.
- **Supporting context** — the producing run (`first_seen_run_id`), artifact location, and (where relevant) the Impact Assessment context that sizes/locates its CAF contribution.
- **Supersession context** — the prior finding it superseded (if any) and what changed.

A Finding for which any required component cannot be produced is **non-conformant** (§H). Explanation reduces to **basis** (evidence + rationale + dimensions), never to a number or a prescribed action.

---

## E. Finding History Model

Using existing state concepts (State Model §10; Data Model v1.1) — **append-only**:
- **Current finding** — the active finding in effect now.
- **Superseded finding** — a prior finding replaced by a newer one; **retained**, never deleted.
- **Historical finding** — any finding in the supersession chain.

Behavior: findings are **superseded, not overwritten**; a reopened condition yields lifecycle reactivation (`reopened`), while a replaced finding is **superseded** (a new finding may take its place — no destructive mutation). The chain **must be reconstructable** (replay/audit), mirroring the subsystem-wide supersession discipline (CAF Scoring v2 §11; Confidence v2 §10).

---

## F. Finding / Recommendation Relationship Model

- **Recommendations originate from Findings.** Every Recommendation traces to ≥1 Finding (Recommendation System Spec REC-1/REC-8); a Finding may give rise to **one or more** recommendations (alternative improvement paths).
- **Findings are descriptive; Recommendations are prescriptive.** A Finding states the condition; a Recommendation proposes the advisory action, and its **Possible Resolution Paths** enumerate the options (Recommendation System Spec §4; Resolution Paths Spec).
- **Findings do not contain or imply actions.** Any "what to do" lives in the Recommendation, never in the Finding.
- **Coupling.** When a Finding changes state (superseded/closed/reopened/removed/weakened), its recommendations behave per `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md` — the Finding is the upstream object; recommendations couple to it, not the reverse.
- **No feedback.** Recommendations (and their selection/paths) **never** modify a Finding's content; they may, via user action → reanalysis, lead to the Finding being weakened/removed (the success condition), but only through reanalysis.

---

## G. Finding Integrity Rules

*Structurally testable; each realizes existing doctrine; none introduces governance/execution.*

- **FND-1.** A Finding is **descriptive** — it states a condition and **never prescribes an action**.
- **FND-2.** A Finding **never directly modifies CAF**; it contributes to CAF **only via Impact Assessment** (CAF changes through assessment/reanalysis).
- **FND-3.** A Finding **never directly modifies Reliability**, and Reliability is **not influenced by findings** (determined independently).
- **FND-4.** A Finding **never directly modifies Confidence**; it reaches Confidence **only through CAF**.
- **FND-5.** A Finding **must trace to ≥1 evidence/context item** and to its producing run (attributable; never unattributed).
- **FND-6.** A Finding **must declare** its `finding_type` (canonical taxonomy) and its `affected_dimensions`.
- **FND-7.** A Finding **must be explainable** (§D) — never opaque.
- **FND-8.** Findings are **append-only** — superseded (retained), never overwritten; the chain is reconstructable.
- **FND-9.** Finding **type is a label, not a coefficient** — it does not set the magnitude/locality of CAF effect (Impact Assessment does).
- **FND-10.** A Finding **may give rise to Recommendations**; Recommendations never alter the Finding (no feedback).
- **FND-11.** A Finding is **human-readable and user-facing** (first-class object).
- **FND-12.** **No governance** (Resolution Candidate, Accepted Understanding, Governance, Disposition) and **no execution** (agents, automation, project execution) semantics attach to a Finding.

---

## H. Conformance Requirements

Structural (**no percentages, thresholds, or pass-rate language**) — a conforming implementation MUST:
- **C-1.** Produce findings from analysis runs with `first_seen_run_id` and ≥1 `evidence_links`; reject unattributed findings (FND-5).
- **C-2.** Apply each finding's CAF effect **only via Impact Assessment**; guarantee a finding never writes a CAF/Reliability/Confidence value (FND-2/FND-3/FND-4).
- **C-3.** Enforce the canonical lifecycle (§C) and append-only supersession; retain superseded findings; reconstruct the chain (FND-8).
- **C-4.** Surface the full explanation (source evidence, rationale, affected dimensions, type, supporting + supersession context) without recomputation (FND-7).
- **C-5.** Declare `finding_type` (canonical) and `affected_dimensions` on every finding (FND-6).
- **C-6.** Link findings to the recommendations they give rise to; prevent any recommendation from mutating a finding (FND-10).
- **C-7.** Present findings as human-readable user-facing objects (FND-11).
- **C-8.** Introduce no governance/execution semantics on findings (FND-12).

Conformance is **all-or-nothing on these rules**; any prescriptive finding, any direct CAF/Reliability/Confidence write, any unattributed/opaque/overwritten finding, or any governance/execution attachment **fails conformance**.

---

## I. Deferred Items

Explicitly **Deferred to future calibration / out of scope**:
- **Severity numeric basis** — what numerically separates critical/moderate/warning (CAF Scoring v2 §6; calibration).
- **Impact Assessment arithmetic** — how significance/scope/evidence-support size a finding's CAF contribution (CAF Scoring v2; calibration).
- **`finding_type` enum reconciliation** — any change to the canonical taxonomy (e.g., a distinct "dependency" type) is a Data Model / Finding Model reconciliation, owner-ratified.
- **Finding generation heuristics** — how the engine detects conditions (Analysis Engine / calibration).
- **Effectiveness analytics** — finding-resolution-rate measurement over time.
- **All governance/execution capabilities** — Future Architecture / excluded.

Future work must conform to this specification and the layers above it, introducing no prescriptive-finding behavior, no direct assessment modification, and no governance/execution into Release 1.

---

*This document specifies the canonical Release 1 Finding: a descriptive, attributable, explainable, append-only, human-readable object that contributes to CAF only via Impact Assessment, never modifies CAF/Reliability/Confidence directly, never influences Reliability, gives rise to (but is never altered by) Recommendations, and carries no governance or execution semantics. It is consistent with CAF Scoring v2, Reliability v2, Confidence v2, the Recommendation System Specification, and the Recommendation Resolution Paths Specification.*

**Finding System Specification v1 complete.**

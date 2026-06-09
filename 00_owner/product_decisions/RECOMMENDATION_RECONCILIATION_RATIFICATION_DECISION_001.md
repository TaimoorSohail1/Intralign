# Recommendation Reconciliation Ratification Decision 001

**Type:** Governance decision (ratification artifact — decisions, not review)
**Status:** Proposed Release 1 (pending decision-log entry) · **Date:** 2026-05-31
**Resolves:** RS-R1 … RS-R7 (Recommendation System Spec §13a; Governance Review; Audit 001/002).
**Authoritative inputs:** Recommendation Model v1 · Recommendation System Spec v1 · Coupling Spec v1 · Finding System Spec v1 · CAF Scoring v2 · Reliability v2 · Confidence v2 · Data Model v1.1 · State Model · Event Model · Architecture Audit 001/002 · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md`.

> **Constraints honored.** No new doctrine, recommendation behavior, governance, execution, agents, scoring/ranking/probability/calibration arithmetic, Resolution/Clarification Candidate, or unratified lifecycle states. **AMB-1 is not reopened.** Where uncertain, **preserve the ratified model.** Findings remain descriptive; Recommendations advisory; CAF/Reliability/Confidence meaning unchanged.

---

## A. Executive Summary

- **Overall assessment:** the Recommendation domain is **internally consistent and bounded**; the only open items are the seven enum/field/cardinality reconciliations, all additive or simplifying — none touches behavior or assessment.
- **Readiness determination:** **Implementation-ready for Release 1** once the **two ratified additive changes** (RS-R3 `deferred` status; RS-R7 fields) land in a **Data Model v1.2** and the State/Event additions are applied. The simplifying decisions (RS-R1/R2/R4 keep ratified; RS-R5/R6 deferred) require **no** new modeling.
- **Maturity:** **Mature.** The canonical Recommendation model (types, lifecycle, attribution, fields) is now fixed; AMB-1 is resolved (paths are presentation-only).
- **Verdict:** **Release 1 Recommendation architecture is ready for implementation** after the Data Model v1.2 + State/Event additive application below.

---

## B. Item-by-Item Ratification Decisions

### RS-R1 — Recommendation type taxonomy (9 vs ratified 3)
- **Current state:** Spec proposes 9 finer types; ratified Data Model `recommendation_type = {improvement, validation, suggested_fix}` (3).
- **Evaluation:** The 9 add no behavior; the ratified 3 are sufficient and already mapped (the 9 refine the 3). "Prefer ratified / avoid expansion" applies. No doctrine/Data/State conflict from keeping 3.
- **Decision:** **Reject** the enum expansion. **Canonical = the ratified 3 types.** The 9 may be used as **non-persisted presentation labels** (UI sub-categorization), never as a persisted enum.
- **Rationale:** Preserves the ratified Data Model; avoids enum churn; presentation can still show friendly type names.
- **Consequences:** Recommendation Spec §4 type list re-marked as **presentation labels over the canonical 3**; **no** Data Model change.

### RS-R2 — `Presented` lifecycle state
- **Current state:** Spec §8 lists `Presented`; Data Model v1.1 **R-2 removed** it as a UI concern.
- **Evaluation:** "Presented" is a **presentation** event, not a persisted assessment/lifecycle status; reinstating it would reverse a ratified decision and duplicate UI responsibility (now owned by the Presentation Spec).
- **Decision:** **Reject** `Presented` as a persisted status. (Surfacing is a UI concern.)
- **Rationale:** Upholds ratified R-2; keeps the lifecycle behavioral, not presentational.
- **Consequences:** Recommendation Spec §8 drop `Presented` from the **persisted** lifecycle (UI surfacing handled by the Presentation Spec). No Data/State/Event change.

### RS-R3 — `Deferred` lifecycle state
- **Current state:** Spec §8 lists `Deferred`; doctrinally supported (Recommendation Model **Position #12**: "may be accepted, rejected, deferred, or ignored") but absent from the ratified status enum.
- **Evaluation:** **Doctrinally grounded**, low-risk, additive; a genuine user outcome (postpone, still valid). Governance Review recommended advancing it.
- **Decision:** **Ratify.** Add `deferred` to the Recommendation status enum.
- **Rationale:** Aligns the persisted model with existing doctrine; the only ratified lifecycle addition.
- **Consequences:** **Data Model v1.2** (`status += deferred`); **State Model** (+`deferred` state + transitions); **Event Model** (+`recommendation_deferred`); API (`:defer` command + state); UI (deferred state shown).

### RS-R4 — `Completed` vs `implemented`
- **Current state:** Spec uses `Completed`; ratified terminal action state is `implemented`.
- **Evaluation:** Pure naming; ratified term is `implemented`. The Success Model already distinguishes "implemented ≠ success."
- **Decision:** **Ratify `implemented`** as the canonical terminal state; **Reject `Completed`** as a separate state. "Completed" is allowed only as a **UI display synonym** for `implemented`.
- **Rationale:** Preserves the ratified term; avoids a duplicate state.
- **Consequences:** Recommendation Spec/Presentation use `implemented` (display "Completed/Implemented" allowed). No Data/State change.

### RS-R5 — Finding cardinality (single → multiple)
- **Current state:** Spec/Coupling reference **one-or-more** `finding_references`; ratified Data Model `finding_id` is **single**; Recommendation Model **Position #2** frames a recommendation as operating on **the** Finding (singular).
- **Evaluation:** Single-finding is consistent with the ratified Data Model **and** Recommendation Model Position #2; AMB-1's "alternatives = multiple Recommendations per Finding" works with single `finding_id` (one finding → many recs). Multi-finding (one rec → many findings) is an enhancement, not required for R1.
- **Decision:** **Defer.** **Release 1 = single `finding_id`** (one Recommendation → one Finding). Multi-finding attribution is future.
- **Rationale:** Preserve ratified model + Position #2; keep Tier 1/2 simple.
- **Consequences:** Recommendation Spec §4 `finding_references` → **single `finding_id`** for R1; **Coupling Spec §4 (one rec → many findings) is deferred** (R1 governed by §3 single-finding coupling); no Data Model change.

### RS-R6 — Affected-dimension cardinality (single → multiple)
- **Current state:** Spec proposes plural `affected_caf_dimensions`; ratified Data Model `expected_dimension` is **single**.
- **Evaluation:** A recommendation typically targets one primary dimension; single `expected_dimension` is adequate for R1 and matches the ratified model. Plural pairs naturally with multi-finding (RS-R5), also deferred.
- **Decision:** **Defer.** **Release 1 = single `expected_dimension`.** Plural is future.
- **Rationale:** Preserve ratified model; keep simple; consistent with deferring RS-R5.
- **Consequences:** Recommendation Spec dimension field → **single `expected_dimension`** for R1; no Data Model change.

### RS-R7 — New recommendation fields
- **Current state:** Spec/Presentation need `title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference`; ratified Data Model `Recommendation` lacks some.
- **Evaluation:** Purely **additive** fields required for the recommendation **card** (Presentation Spec §E); no behavior change; consistent with all models.
- **Decision:** **Ratify** the additive fields: `title`, `description`, `effort` (Low/Medium/High), `artifact_reference`, `artifact_element_reference`.
- **Rationale:** Needed for presentation/traceability; additive and low-risk.
- **Consequences:** **Data Model v1.2** (+5 fields on `Recommendation`); API (expose fields); UI (card uses them). No State/Event change.

---

## C. Final Canonical Recommendation Decisions (Release 1)

### Recommendation Types
**Canonical `recommendation_type` = `improvement` · `validation` · `suggested_fix` (3, ratified).** Finer type names are **presentation labels only**, not a persisted enum.

### Recommendation Lifecycle
**Canonical states:** `generated · accepted · rejected · deferred · implemented · superseded` (6 — the ratified 5 + ratified `deferred`). **Not** `presented` (UI), **not** `completed` (display synonym of `implemented`).
**Transitions:** `generated → {accepted, rejected, deferred}`; `deferred → {accepted, rejected}`; `accepted → implemented`; any active → `superseded`. (Reopen/ignore are user outcomes within these states.)

### Recommendation Attribution
**One Recommendation → one Finding** via **single `finding_id`** (Release 1). Multi-finding deferred (RS-R5). Recommendations remain **always attributable to a finding** (REC-1).

### Recommendation Dimension Attribution
**Single `expected_dimension`** (one of Clarity/Alignment/Feasibility) per Recommendation (Release 1). Multi-dimension deferred (RS-R6).

### Recommendation Metadata (authoritative field set)
`recommendation_id` · `project_id` · `finding_id` · `first_seen_run_id` · `recommendation_type` · `status` · `rationale` · `expected_dimension` · **`title`** · **`description`** · **`effort`** · **`artifact_reference`** · **`artifact_element_reference`**.

---

## D. Data Model Impact

- **Approved (Data Model v1.2):** add `deferred` to `Recommendation.status` (RS-R3); add `title`, `description`, `effort`, `artifact_reference`, `artifact_element_reference` (RS-R7).
- **Rejected:** type-enum expansion (RS-R1); `presented` status (RS-R2); `completed` state (RS-R4).
- **Deferred:** `finding_id → finding_references` (RS-R5); `expected_dimension → affected_caf_dimensions` (RS-R6).
- **Verdict:** **Data Model v1.2 is required** (additive: 1 enum value + 5 fields). v1.1 is otherwise preserved.

---

## E. State Model Impact

- **Addition:** `deferred` state (RS-R3) with transitions `generated→deferred`, `deferred→{accepted, rejected}`.
- **Removals:** none (the spec's `presented`/`completed` are not adopted as states).
- **Clarifications:** terminal action state = `implemented`; supersession unchanged (append-only).
- **Verdict:** **State Model change required** (add `deferred` to the Recommendation lifecycle).

---

## F. Event Model Impact

- **Addition:** `recommendation_deferred` (emitted on a user defer; sets `deferred`).
- **Removals:** none.
- **Clarifications:** no `presented` event (UI surfacing only); no resolution-path events (AMB-1 — withdrawn).
- **Verdict:** **Event Model change required** (add `recommendation_deferred`).

---

## G. API Impact

- **Required:** add `POST /recommendations/{rid}:defer` (→ `deferred`; emits `recommendation_deferred`); expose the new fields (`title`/`description`/`effort`/`artifact_reference`/`artifact_element_reference`) and `deferred` state in recommendation payloads.
- **Rejected:** `presented`-as-status endpoints; resolution-path endpoints/sub-resources (AMB-1); type-enum expansion.
- **Deferred:** multi-`finding_references` / plural `affected_caf_dimensions` payload arrays.

---

## H. UI Impact

- **Presentation implications:** `deferred` is a visible recommendation state (Presentation Spec §G already accommodates it); `implemented` shown (display "Completed/Implemented" allowed).
- **Recommendation-card implications:** card uses the ratified fields incl. `title`, `description`, `effort` (RS-R7); type shown via friendly label over the canonical 3.
- **"Possible Resolution Paths" implications:** unchanged — a **presentation grouping of multiple Recommendations** per finding (AMB-1); **not** affected by these decisions.
- **User-selection implications:** selecting = accepting a Recommendation (**Selected Path**), which may differ from **OSLO Recommended**; `deferred` available as a "set aside" affordance. No execution/automation.
- *(No UI designs created here — implications only.)*

---

## I. Backlog Impact

**Closed reconciliation items (decided):** RS-R1 (Reject), RS-R2 (Reject), RS-R3 (Ratify), RS-R4 (Ratify `implemented`), RS-R7 (Ratify). Plus **AMB-1** (already resolved).

**Remaining open (Deferred → future):** RS-R5 (multi-finding attribution), RS-R6 (multi-dimension attribution). *(Also: Coupling Spec §4 multi-finding handling is deferred with RS-R5.)*

**New follow-on artifacts & sequencing:**
1. **Data Model v1.2** — **required now** (apply RS-R3 + RS-R7; additive). *(Highest priority — unblocks persistence/API/UI for the ratified changes.)*
2. **State/Event additive application** — add `deferred` state + `recommendation_deferred` event; add `:defer` API.
3. **`RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md`** — **already created** ✅ (conforms to these decisions).
4. **`FINDING_PRESENTATION_SPECIFICATION_V1.md`** — recommended next (the descriptive surface beneath recommendations).
5. **`RECOMMENDATION_TEST_SPECIFICATION_V1.md`** + **`RECOMMENDATION_FIXTURE_LIBRARY_SPECIFICATION_V1.md`** — cover REC-* + the ratified lifecycle/fields.
6. **`FINDING_TEST_SPECIFICATION_V1.md`** + **`FINDING_FIXTURE_LIBRARY_SPECIFICATION_V1.md`** — cover FND-*.

**Recommended order:** Data Model v1.2 (+State/Event/API additive) → Finding Presentation Spec → Recommendation Test/Fixture specs → Finding Test/Fixture specs. *(Calibration decisions proceed on the parallel owner track.)*

---

*This decision ratifies the canonical Release 1 Recommendation model: 3-type taxonomy (ratified; 9 = presentation labels); lifecycle generated/accepted/rejected/deferred/implemented/superseded (adds `deferred`, drops `presented`/`completed`); single-finding and single-dimension attribution (multi deferred); and additive card fields (title/description/effort/artifact refs). It requires a Data Model v1.2 plus additive State/Event/API changes; preserves all existing doctrine and CAF/Reliability/Confidence/Finding meaning; introduces no governance/execution/automation; and does not reopen AMB-1.*

**Recommendation Reconciliation Ratification Decision 001 complete.**

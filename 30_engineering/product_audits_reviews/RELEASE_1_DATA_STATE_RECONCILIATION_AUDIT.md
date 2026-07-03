# Release 1 Data / State Reconciliation Audit

**Type:** Read-only audit — compares the Data Model and State Model; identifies divergences. **No specification modified.**
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Inputs:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md`
**Aligned with:** `OSLO_RELEASE_1_CANONICAL_SCOPE_V1.md` · `OSLO_ARCHITECTURE_BASELINE_V1.md` · `OSLO_CAPABILITY_MATRIX_V2.md` · `OSLO_LINEAR_INITIATIVES_V2.md` · `OSLO_RELEASE_1_IMPLEMENTATION_PLAN.md`

> Active Release 1 only. No Governance Domain concepts, Future Architecture, or Release 2. This is a **read-only** audit producing **recommendations and backlog items only** — it changes neither specification. Reconciliation decisions are owner-ratified per governance discipline.

---

## 1. Purpose

The Data Model and State Model were authored in sequence. The Data Model fixed entity enums first; the State Model — declared the **lifecycle authority** — then specified lifecycle state names that in several places differ from those enums. Before the Event Model binds events to transitions, the two specs must be compared so engineering builds against **one** agreed set of states per entity. This audit surfaces every divergence (lifecycle conflicts, enum mismatches, naming inconsistencies, missing state fields, duplicate concepts, implementation risks) and records reconciliation as backlog proposals. It resolves nothing unilaterally.

---

## 2. Scope

**Reviewed:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` (entity/field enums) and `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` (lifecycle state machines, §4–§14).
**Referenced for alignment only:** Canonical Scope V1, Architecture Baseline V1, Capability Matrix V2, Linear Initiatives V2, Implementation Plan.
**Out of scope:** schema/DDL, API, UI, Governance behavior, anything Future/Release 2.

---

## 3. Entity Alignment Matrix

| Entity | Data Model representation | State Model representation | Alignment |
|---|---|---|---|
| **Project** | `lifecycle_state` ∈ {created, orienting, oriented, deep_analyzing, analyzed, archived} | Draft → Orientation Running → Orientation Complete → Deep Analysis Running → Deep Analysis Complete → Archived | ⚠️ **Rename only** (1:1 mapping, different labels) |
| **Analysis Run** | `run_status` ∈ {queued, running, completed, failed, superseded}; `run_type` ∈ {fast_analysis_pass, deep_analysis_pass}; `previous_run_id` | Queued → Running → Completed + Failed/Cancelled/Superseded; retry/replacement/historical | ⚠️ **Near-aligned** — State Model adds **`Cancelled`** (absent in Data Model) |
| **CAF State** | per-run CAFState; latest = current; prior retained | Current / Superseded / Historical | ✅ **Aligned** |
| **Confidence State** | per-run ConfidenceState; `supersedes_confidence_state_id`; project current pointer | Current / Superseded / Historical | ✅ **Aligned** |
| **Finding** | `status` ∈ {detected, validated, recommended, addressed, resolved, reopened}; `first_seen_run_id` | Detected → Acknowledged → Addressed → Closed + Superseded/Reopened | ❌ **Conflict** — enum mismatch + missing `superseded`; extra `recommended` |
| **Recommendation** | `status` ∈ {generated, presented, accepted, modified, rejected, applied, verified}; `recommendation_type`; `first_seen_run_id` | Generated → Accepted → Rejected → Implemented + Superseded | ❌ **Conflict** — wider enum vs narrow lifecycle; missing `superseded`; `Implemented` vs `applied/verified` |
| **Notification** | `state` ∈ {created, viewed, dismissed, acted_upon, historical} | Created → Viewed → Dismissed + Expired | ⚠️ **Minor** — `Expired` vs `historical`; `acted_upon` unused |
| **Report** | `Report` + versioned `ReportSnapshot`; `current_snapshot_id`; **no `status` field** | Draft → Published → Superseded → Archived | ❌ **Missing state field** |
| **Shared Artifact** | `visibility`, `permission_level`, `expires_at`, `revoked_at`; **no `status` field** | Created → Shared → Viewed → Revoked + Expired | ❌ **Missing state field** |

---

## 4. Lifecycle Conflict Analysis

**C-1 · Finding lifecycle mismatch** — **High.**
Current (Data Model): {detected, validated, recommended, addressed, resolved, reopened}. Conflicting (State Model): {Detected, Acknowledged, Addressed, Closed, Superseded, Reopened}. `validated`≈Acknowledged, `resolved`≈Closed; `Superseded` **missing** from the Data Model; `recommended` has **no** lifecycle counterpart (it duplicates information already carried by an associated Recommendation — a duplicate-concept smell). **Risk:** engineers persisting `Finding.status` cannot represent a superseded finding, breaking the §16 supersession invariant; ambiguous `recommended` vs `validated`.

**C-2 · Recommendation lifecycle mismatch** — **High.**
Current: {generated, presented, accepted, modified, rejected, applied, verified}. Conflicting: {Generated, Accepted, Rejected, Implemented, Superseded}. `Implemented`≈`applied`/`verified` (two Data-Model values collapse to one lifecycle state); `presented`/`modified` have no lifecycle state; `Superseded` **missing**. **Risk:** non-deterministic mapping (is `verified` = Implemented?); supersession of a recommendation is unrepresentable; the Event Model's `recommendation_superseded` would have no target state.

**C-3 · Notification lifecycle mismatch** — **Low.**
`Expired` (State Model) vs `historical` (Data Model); `acted_upon` (Data Model) unused by the lifecycle. **Risk:** cosmetic/naming; minor confusion only. Notifications never drive analysis, so blast radius is contained.

**C-4 · Missing Report status** — **Medium.**
State Model defines Draft/Published/Superseded/Archived; Data Model carries only snapshot versioning, no `status`. **Risk:** report state must be inferred from snapshot pointers/timestamps — not directly queryable; `report_published`/`report_superseded` events have no field to set.

**C-5 · Missing Shared Artifact status** — **Medium.**
State Model defines Created/Shared/Viewed/Revoked/Expired; Data Model has only `expires_at`/`revoked_at` timestamps. **Risk:** "is this share live?" requires deriving state from two nullable timestamps; `artifact_shared`/revoke/expire events have no status target; collaboration (M3) surface logic becomes ad-hoc.

**C-6 · Analysis Run `Cancelled`** — **Medium.**
State Model adds `Cancelled` (user/system pre-completion stop); Data Model `run_status` omits it. **Risk:** cancelled runs would be mislabeled `failed`, corrupting failure metrics and recovery logic (§17).

**C-7 · Project enum naming** — **Low.**
Pure rename (1:1). **Risk:** traceability friction only; no behavioral conflict.

---

## 5. Recommended Reconciliation Decisions

*(Recommendations only — neither spec is modified here. Owner ratification required.)*

- **R-1 (C-1):** Adopt the State Model Finding set {detected, acknowledged, addressed, closed, reopened, **superseded**}; map `validated→acknowledged`, `resolved→closed`; **retire `recommended`** (the Recommendation link already conveys it).
- **R-2 (C-2):** Adopt {generated, accepted, rejected, implemented, **superseded**} as the canonical lifecycle; treat `presented` as a UI/notification concern (not a status), and document `applied`+`verified` as collapsing into `implemented` (or keep `verified` as an optional post-implementation sub-flag outside the canonical machine).
- **R-3 (C-3):** Rename Data Model `historical → expired`; **drop `acted_upon`** unless a product need is shown.
- **R-4 (C-4):** Add `Report.status` ∈ {draft, published, superseded, archived} to the Data Model.
- **R-5 (C-5):** Add `SharedArtifact.status` ∈ {created, shared, viewed, revoked, expired}; keep timestamps as evidence fields.
- **R-6 (C-6):** Add `cancelled` to `AnalysisRun.run_status`.
- **R-7 (C-7):** Rename `Project.lifecycle_state` values to the State Model labels for 1:1 traceability (optional; behaviorally neutral).
- **Direction:** since the State Model is the declared **lifecycle authority**, reconcile the **Data Model toward the State Model** in all conflicts above.

---

## 6. Engineering Risk Assessment

| ID | Mismatch | Risk |
|---|---|---|
| C-1 | Finding lifecycle / missing `superseded` / `recommended` duplicate | **High** |
| C-2 | Recommendation lifecycle / missing `superseded` / `applied`↔`implemented` | **High** |
| C-4 | Missing `Report.status` | **Medium** |
| C-5 | Missing `SharedArtifact.status` | **Medium** |
| C-6 | Missing `AnalysisRun.cancelled` | **Medium** |
| C-3 | Notification `expired` vs `historical`, unused `acted_upon` | **Low** |
| C-7 | Project enum rename | **Low** |

**Highest risk:** C-1 and C-2 — both break the supersession invariant the whole replayable model depends on, and both are directly referenced by Event Model events (`finding_superseded`, `recommendation_superseded`).

---

## 7. Readiness Assessment

- **Reconciliation items identified:** ✅ seven (C-1…C-7), all recorded as backlog proposals R-1…R-7.
- **Event Model may proceed:** ✅ **Yes.** None of the divergences are conceptual — they are enum/field gaps with a clear reconciliation direction (Data Model → State Model). The Event Model can be authored against the **State Model's** lifecycle vocabulary (the authority) and reference these backlog IDs where it touches a contested field, so it remains correct regardless of when the Data Model is reconciled.
- **Backlog items recorded:** ✅ R-1…R-7 staged for owner ratification before the Data Model is edited.

**Condition:** the Event Model must use State-Model state names and cite R-1…R-7 at the `finding_superseded` / `recommendation_superseded` / report / shared-artifact / cancellation touchpoints.

---

## 8. Validation

- No specifications modified — ✅ (audit only; zero edits to Data or State Model)
- Read-only audit — ✅
- No Governance concepts introduced — ✅
- Divergences enumerated with risk + recommendation — ✅ (§3–§6)
- Event Model readiness determined — ✅ (§7)

**Data / State reconciliation audit complete.**

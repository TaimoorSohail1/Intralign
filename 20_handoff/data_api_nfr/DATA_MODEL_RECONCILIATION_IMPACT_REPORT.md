# Data Model Reconciliation Impact Report

**Type:** Impact assessment of the v1 → v1.1 Data Model reconciliation
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Inputs:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` · `DATA_MODEL_RECONCILIATION_CHANGE_LOG.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_DATA_STATE_RECONCILIATION_AUDIT.md`

> Assesses the downstream impact of applying R-1, R-2, R-4, R-5, R-6 to the Data Model. Read-only assessment; no specs modified beyond the v1.1 successor already produced.

---

## 1. Data Model impact

Five entities changed; **no entities added, none removed.** Finding and Recommendation `status` enums were reconciled (renames, removals, one collapse, one addition each); Notification `state` reconciled (`historical→expired`, drop `acted_upon`, add `expired_at`); Report and SharedArtifact each gained an explicit `status` field (plus supporting evidence timestamps / a published pointer). All changes are **forward enum/field definitions** — pre-GA, so they are definitions rather than live migrations. The model is now a faithful persistence mirror of the State Model lifecycles and Event Model transitions, with two bounded exceptions tracked as Outstanding items (O-1 `cancelled`, O-2 `Delivered`). **Risk: Low.** No relationship, tenancy, versioning, or lineage structure changed.

## 2. State Model impact

**None — by design.** The State Model is the lifecycle authority and was not modified. v1.1 conforms to it. The reconciliation actually *validates* the State Model: every State Model lifecycle now has a persisted home. The single place where the prompt diverged from the State Model (`Delivered`) was resolved in the State Model's favor (not added to persistence), preserving the State Model as canonical and avoiding terminology drift.

## 3. Event Model impact

**Positive, no modification.** Every reconciled lifecycle gives an Event Model transition an explicit persisted target: `finding_superseded` → `Finding.status=superseded` (R-1); `recommendation_superseded`/`recommendation_implemented` → `Recommendation.status` (R-2); `notification_expired` → `Notification.state=expired` (R-4); `report_*` → `Report.status` (R-5); `artifact_shared`/`share_revoked`/`share_expired` → `SharedArtifact.status` (R-6). **One gap remains:** Event `analysis_cancelled` (§8) still has no persisted target because `AnalysisRun.run_status` lacks `cancelled` (Outstanding O-1). All other Event transitions are now fully persistable. The R-2/R-3 citations the Event Model embedded now resolve.

## 4. API Contract implications

The API spec can now define request/response enums and command results against **stable, single-source lifecycle values** — the chief blocker (ambiguous/duplicated status enums) is removed for five of six lifecycles. Contracts should: expose the reconciled enums verbatim; treat status transitions as the result of commands that emit Events; and **defer** only the `cancel analysis` command's persisted status until O-1 lands (the contract can still define the command, marked pending O-1). **Net: API contracts are unblocked.**

## 5. UI implications

UI state rendering now maps to deterministic enums (finding chips: detected/acknowledged/addressed/closed/reopened/superseded; recommendation states; share liveness via `SharedArtifact.status`; report status badges). The removed values (`presented`, `modified`, `acted_upon`) should be dropped from any UI mock that referenced them. UI can proceed from Master Spec §15 + wireframes against the v1.1 enums; a "cancelled run" UI state should be held pending O-1. **Risk: Low.**

## 6. Testing implications

Test matrices can now assert exact lifecycle transitions and supersession against persisted values. New/updated test obligations: Finding `superseded`/`reopened` paths; Recommendation `implemented`/`superseded`; Notification `expired` + `acted_upon→dismissed` migration mapping; Report status + `published_snapshot_id` invariant; SharedArtifact status↔timestamp constraints. Determinism/replay tests are unaffected (set-to-state transitions preserved). Add one **negative** test that `analysis_cancelled` is not yet persistable until O-1.

---

## Readiness Assessment

| Dimension | Status after v1.1 |
|---|---|
| Finding lifecycle aligned | ✅ |
| Recommendation lifecycle aligned | ✅ |
| Notification lifecycle aligned | ✅ (with `Delivered` correctly deferred) |
| Report lifecycle persisted | ✅ |
| Shared Artifact lifecycle persisted | ✅ |
| AnalysisRun lifecycle aligned | ⚠️ `cancelled` outstanding (O-1) |
| Project lifecycle aligned | ✅ (rename-only, 1:1) |
| Replayability / event-sourcing / tenancy / Confidence / Expanded F&R | ✅ preserved |
| New architecture / governance / future concepts | ✅ none introduced |

Five of the six entity lifecycles are fully reconciled and persistable; the sixth (AnalysisRun) is aligned except for one deferred enum value (`cancelled`) that is low-risk and was simply outside the approved batch. No lifecycle is **conceptually** ambiguous anymore — the only residue is two recorded, owner-scoped enum decisions (O-1 `cancelled`, O-2 `Delivered`).

---

## Final Assessment

**Can `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` be generated without unresolved lifecycle ambiguity?**

**API Contract Specification may proceed.**

**Rationale.** The lifecycle backbone is now single-sourced: Data Model v1.1 persists exactly what the State Model defines and the Event Model transitions. All five high-value enum/field conflicts (Finding, Recommendation, Notification, Report, Shared Artifact) are resolved, so contract enums, command results, and read schemas can be written deterministically against one vocabulary. The two residual items are **not lifecycle ambiguities** that would churn contracts: O-1 (`AnalysisRun.cancelled`) is a single additive enum value affecting only the `cancel analysis` command — the contract can define that command now and mark its persisted status pending O-1; O-2 (`Delivered`) is a deferred owner decision that does not block any currently-defined transition. Neither prevents coherent contract definition. Recommend the API spec (a) adopt the v1.1 enums verbatim, (b) note O-1/O-2 at the two affected endpoints, and (c) proceed with UI in parallel and Testing to follow.

*Impact assessment only. No specifications modified beyond the already-produced v1.1 successor.*

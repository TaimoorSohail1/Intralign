# Data Model Reconciliation — Patch 001

**Type:** Patch record — two follow-up decisions applied to `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md`
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Target:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` (in place)
**Authority order:** State Model (lifecycle) > Event Model (transitions) > Data Model (persistence)
**Constraint:** State Model and Event Model **not modified.**

> Resolves the two Outstanding items (O-1, O-2) recorded in `DATA_MODEL_RECONCILIATION_CHANGE_LOG.md`. One value added; one value deferred with explicit rationale. No new entities, architecture, governance, or future concepts.

---

## Decision 1 — `AnalysisRun.run_status += cancelled` (O-1 → applied)

- **Decision:** Add `cancelled` to `AnalysisRun.run_status`.
- **Before:** `enum(queued, running, completed, failed, superseded)`
- **After:** `enum(queued, running, completed, failed, cancelled, superseded)`
- **Why:** The State Model (§5) already defines a **Cancelled** run state and the Event Model (§8) already emits `analysis_cancelled`. The Data Model was the only layer missing the value, leaving that transition without a persisted target. Adding it conforms the persistence layer to the already-approved lifecycle/transition definitions — no new behavior.
- **Authority check:** State Model and Event Model unchanged; Data Model updated to match them (correct direction).
- **Effect:** `analysis_cancelled` (Queued/Running → Cancelled) is now fully persistable. `cancelled` is a terminal, retained state (distinct from `failed`); recovery/retry semantics are unchanged (a retry creates a new run via `previous_run_id`).
- **Migration:** forward enum value; no live data assumed pre-GA. Any run previously mislabeled `failed` due to user/system cancellation can be reclassified to `cancelled` if such data exists.

## Decision 2 — Notification `delivered` (O-2 → deferred, not added)

- **Decision:** Do **not** add `delivered` to `Notification.state`. **Defer until delivery-channel semantics exist.**
- **State unchanged:** `enum(created, viewed, dismissed, expired)`
- **Why:** The State Model (§12) does not define a `Delivered` notification state, and the governing rules forbid modifying the State Model in this work and forbid inventing new behavior. More substantively, **`delivered` is only meaningful once a delivery channel exists** — a transport (in-app/push/email) capable of confirming receipt. Release 1 models Notification as in-product awareness with **no routing or delivery logic** (Data Model §13); without a channel there is no observable "delivered" transition to persist. Adding it now would be a persistence state with no lifecycle and no producer — drift.
- **Authority check:** State Model not modified; no behavior invented.
- **Re-entry path:** when/if Release 1 (or later) introduces delivery-channel semantics, the sequence is: (1) add `Delivered` to State Model §12 via owner-ratified governance, (2) add the producing transition to the Event Model, (3) then persist `delivered` in the Data Model. Until step 1, this remains deferred.

---

## Net effect on lifecycle alignment

| Entity | Lifecycle alignment after Patch-001 |
|---|---|
| Finding | ✅ (R-1) |
| Recommendation | ✅ (R-2) |
| Notification | ✅ (R-4) — `delivered` deferred by design |
| Report | ✅ (R-5) |
| Shared Artifact | ✅ (R-6) |
| **Analysis Run** | ✅ **(Patch-001 `cancelled`)** |
| Project | ✅ (rename-only, 1:1) |

All six entity lifecycles plus Project are now persistence-aligned with the State Model, and **every Event Model transition has a persisted target.** The only open notification value (`delivered`) is intentionally gated on a capability that does not yet exist.

## Validation

- `cancelled` added to `AnalysisRun.run_status` — ✅
- `delivered` **not** added to `Notification.state` — ✅
- Deferral note for `delivered` (delivery-channel semantics) present in Data Model §13 — ✅
- State Model not modified — ✅
- Event Model not modified — ✅
- No new entities / architecture / governance / future concepts — ✅
- All Event Model transitions now persistable — ✅

*Patch record only. Changes applied in place to v1.1; State Model and Event Model untouched.*

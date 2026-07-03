# Data Model Reconciliation Change Log

**Type:** Change log for the v1 → v1.1 Data Model reconciliation
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**From:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.md` · **To:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md`
**Authority order:** State Model (lifecycle) > Event Model (transitions) > Data Model (persistence — updated to conform)

> Records each approved reconciliation item applied to the Data Model. **Only persistence enums/fields changed — no new entities, no architecture, no governance/future concepts.** Item IDs follow the reconciliation prompt (R-1, R-2, R-4, R-5, R-6); the parenthetical `C-n` is the originating finding in `RELEASE_1_DATA_STATE_RECONCILIATION_AUDIT.md`.

---

## R-1 · Finding lifecycle (audit C-1)

- **Original definition:** `Finding.status` ∈ {`detected`, `validated`, `recommended`, `addressed`, `resolved`, `reopened`}; timestamp `resolved_at`.
- **Updated definition:** `Finding.status` ∈ {`detected`, `acknowledged`, `addressed`, `closed`, `reopened`, `superseded`}; timestamp `resolved_at` → `closed_at`.
- **Reason:** Conform persistence to State Model §10 (lifecycle authority). `validated`→`acknowledged`, `resolved`→`closed`; `recommended` removed (duplicate concept — the Recommendation FK already conveys it); `superseded` added so the §16 supersession invariant and Event `finding_superseded` have a target.
- **Impacted entities:** Finding (and any read model filtering by status).
- **Migration notes:** `validated→acknowledged`, `resolved→closed`, rename column `resolved_at→closed_at`; `recommended` rows → `acknowledged` (rely on Recommendation FK for "has recommendation"); `superseded` is a new terminal value. Forward enum definition; no production data assumed pre-GA.

---

## R-2 · Recommendation lifecycle (audit C-2)

- **Original definition:** `Recommendation.status` ∈ {`generated`, `presented`, `accepted`, `modified`, `rejected`, `applied`, `verified`}.
- **Updated definition:** `Recommendation.status` ∈ {`generated`, `accepted`, `rejected`, `implemented`, `superseded`}.
- **Reason:** Conform to State Model §11 + Event Model §11. Narrows a 7-value persistence enum to the 5-state lifecycle; removes ambiguity (which of `applied`/`verified` = "done?").
- **Removed states:** `presented` (surfacing is UI/notification, not lifecycle), `modified` (a modified rec is an `accepted` rec whose content changed).
- **Renamed/collapsed states:** `applied` + `verified` → `implemented` (single terminal "done" state).
- **Added states:** `superseded` (target for Event `recommendation_superseded`).
- **Impacted entities:** Recommendation (and status-filtered read models).
- **Migration impact:** `applied→implemented`, `verified→implemented`, `presented→generated`, `modified→accepted`; `superseded` new. If post-implementation verification must be tracked later, add a `verified_at` flag (not a state). Forward enum; no live data pre-GA.

---

## R-4 · Notification lifecycle (audit C-3)

- **Original definition:** `Notification.state` ∈ {`created`, `viewed`, `dismissed`, `acted_upon`, `historical`}; timestamps `created_at`/`viewed_at`/`dismissed_at`.
- **Updated definition:** `Notification.state` ∈ {`created`, `viewed`, `dismissed`, `expired`}; added timestamp `expired_at`.
- **Reason:** Conform to State Model §12. A notification only surfaces awareness; its lifecycle is Created→Viewed→Dismissed + Expired.
- **Mappings:** `historical → expired`.
- **Deprecated values:** `acted_upon` removed (no lifecycle counterpart; the *source object's* state records action, not the notification). Migrate `acted_upon → dismissed`.
- **Migration path:** `historical→expired`, `acted_upon→dismissed`; add `expired_at`. Forward enum; no live data pre-GA.
- **Impacted entities:** Notification.
- **⚠️ Discrepancy recorded (not applied):** the reconciliation prompt listed a `Delivered`/`delivered` state for both models. The **State Model §12 does not define `Delivered`.** Per "State Model wins / State Model not modified this pass / do not invent behavior," `delivered` was **not** added to persistence (a persistence-only state with no lifecycle = drift). See **Outstanding O-2**.

---

## R-5 · Report lifecycle persistence (audit C-4)

- **Original definition:** `Report` had **no `status` field** (lifecycle inferred from `current_snapshot_id`/timestamps).
- **Updated definition:** added `Report.status` ∈ {`draft`, `published`, `superseded`, `archived`} and `published_snapshot_id` (FK ReportSnapshot, nullable).
- **Reason:** Conform to State Model §13; give Event Model `report_generated`/`report_published`/`report_superseded`/`report_archived` an explicit persisted target. No reporting redesign — `ReportSnapshot` versioning unchanged.
- **Constraints / lineage:** `status` = lifecycle; snapshot chain = version history (complementary). `published` ⇒ non-null `published_snapshot_id`; publishing a newer snapshot moves the prior Report to `superseded` (snapshots retained).
- **Impacted entities:** Report (field add only); ReportSnapshot unchanged.
- **Migration notes:** backfill `status` from current pointer (existing reports with a head snapshot → `published`, else `draft`). Forward field; no live data pre-GA.

---

## R-6 · Shared Artifact lifecycle persistence (audit C-5)

- **Original definition:** `SharedArtifact` had **no `status` field** (liveness inferred from `expires_at`/`revoked_at`).
- **Updated definition:** added `SharedArtifact.status` ∈ {`created`, `shared`, `viewed`, `revoked`, `expired`}; added evidence timestamps `shared_at`, `first_viewed_at` (retaining `expires_at`/`revoked_at`).
- **Reason:** Conform to State Model §14; give Event Model `artifact_shared`/`share_revoked`/`share_expired` an explicit persisted target; make share liveness directly queryable (strengthens isolation, §16). No sharing redesign.
- **Constraints / storage:** `status=revoked` ⇒ `revoked_at` set; `status=expired` ⇒ `expires_at` ≤ now; `status` is set at transition time; timestamps remain nullable evidence fields.
- **Impacted entities:** SharedArtifact (field adds only).
- **Migration notes:** backfill `status` from timestamps (`revoked_at`set→`revoked`; past `expires_at`→`expired`; else `shared`). Forward fields; no live data pre-GA.

---

## Outstanding (recorded, NOT applied in this pass)

| ID | Item | Why not applied | Recommended action |
|---|---|---|---|
| **O-1** | `AnalysisRun.run_status` lacks **`cancelled`** | State Model §5 & Event Model §8 (`analysis_cancelled`) define it, but it was **not** in the approved R-1/R-2/R-4/R-5/R-6 batch | Add `cancelled` to `run_status` in the next reconciliation increment (low risk; one-value enum add) — **blocks full validity of Event `analysis_cancelled`** |
| **O-2** | Notification **`Delivered`** state | Referenced in prompt but **absent from State Model §12**; cannot be added to persistence without first amending the State Model (owner-ratified) | If desired, add `Delivered` to State Model §12 via governance, then persist; otherwise close as not-needed |
| **O-3** | Project enum **rename** to State Model labels | Behaviorally aligned 1:1 already (rename-only, no conflict); not part of this batch | Optional cosmetic rename for 1:1 traceability |
| **O-4** | Recommendation **`verified`** sub-state | Collapsed into `implemented`; tracking verification separately is a product decision | Add `verified_at` flag (not a state) if/when verification tracking is required |

---

*Change log only. v1 retained unchanged; v1.1 is the reconciled successor. State Model and Event Model were not modified.*

# Fast Pass Ratification Workbook 001

**Type:** Owner-decision workbook — ratifies the Fast Analysis Pass proposal/TBD items and specifies the exact canonical edits that follow each approval.
**Status:** Pending owner ratification · **Date:** 2026-05-31
**Governance:** Per `CLAUDE.md`, only the repository owner may ratify, reject, supersede, or adopt canonical content. This workbook **proposes**; it changes nothing canonical until an owner records a decision in the Decision column. AI does not self-ratify.

> How to use: for each item, mark **Decision** = `Approve` / `Approve-with-change` / `Reject` / `Defer`. On `Approve`, the listed **Edit on approval** is applied verbatim (proposal/TBD tag → canonical). Nothing is applied while Decision is blank.

---

## A. Items that flip `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` §9 tags

| ID | Item | Recommendation | Edit on approval | Decision (owner) |
|---|---|---|---|---|
| OD-13 | **Global Skeleton stage** (Stage 2) adoption | Approve — adopt the 2-stage global-skeleton + parallel-local pattern | Remove 〔proposal〕 from §9 Stage 2; add Stage 2 as canonical to Engine §9 + Planning Intelligence flow ref; keep fallback clause | ☐ |
| OD-2 | **Fast ingestion envelope** | Approve value: design point **20,000 tokens**, hard ceiling **33,000 tokens** | Replace 〔proposal: …`TBD`〕 in §9 Stage 0 with the ratified numbers; set `INGESTION_ENVELOPE_TOKENS` / `INGESTION_HARD_CEILING_TOKENS` canonical in `analysis_constants.py`; update NFR §3 envelope (TBD→value) | ☐ |
| OD-3 | **Fast claim-count bound** | Approve range **50–100 salient claims** | Replace 〔proposal — `TBD`〕 in §9 Stage 3 with the ratified range; promote `FAST_CLAIM_COUNT_TARGET` to canonical | ☐ |
| OD-17 | **Oversize-input routing** | Approve — accept but route Deep-only with "large project" message | Remove 〔proposal〕 from §9 Stage 0 routing clause | ☐ |
| (map) | **Finding-type → recommendation-type mapping** (Stage 6) | Approve as a deterministic rule mapping | Remove 〔proposal〕 from §9 Stage 6; add the mapping table to Recommendation Model as canonical | ☐ |
| (key) | **`dedup_key` for dedup/determinism** (Stage 3) | Approve | Remove 〔proposal〕 from §9 Stage 3; add `dedup_key` to the Data Model claim fields (see OD-15) | ☐ |

---

## B. Items that add fields to `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (→ v1.2)

These are **schema reconciliation** edits; on approval they follow the same backlog path as the R-1…R-6 reconciliation (new successor `…_V1.2.md` + change-log entry). State/Event/Engine specs already reference them.

| ID | Item | Recommendation | Edit on approval | Decision (owner) |
|---|---|---|---|---|
| OD-15 | **Claim attribute schema** on `ContextItem` (claim): `verbatim_span`, `normalized_text`, `modality`, `support_status`, `is_measurable`, `vagueness_flags`, `dedup_key`, `structured_proposition`, `relationship_links`, `extraction_confidence` | Approve (additive; no existing field changes) | Add fields to Data Model §9 ContextItem; promote `PROPOSED_CLAIM_FIELDS` → required/optional in `analysis_constants.py`; drop `proposal` tags in `analysis_contracts.py` Claim | ☐ |
| OD-16 | **CAFState attribute additions**: `evaluation_completeness`, `contributing_findings`, `direction_vs_prior`, `dimension_coverage` | Approve (additive) | Add fields to Data Model §10 CAFState; promote `PROPOSED_CAF_STATE_FIELDS`; drop `proposal` tags in contracts | ☐ |

---

## C. Calibration values still required (owner sets the number; no formula)

These are not §9 tag-flips — they are the values the engine needs to emit results. **No formula/weight/threshold may be introduced** (founder CAF decisions); the owner sets only the qualitative-to-value mapping / target.

| ID | Item | Needed for | Decision (owner) |
|---|---|---|---|
| OD-1 | Model choice / tier per stage | latency, cost, determinism | ☐ value: __________ |
| OD-5 | LLM per-call output limits / per-claim token budget | latency, cost | ☐ value: __________ |
| OD-6 | CAF assessed-level scale (qualitative ↔ value) | CAF state, UX | ☐ value: __________ |
| OD-7 | CAF → Confidence synthesis method (formula-free) | confidence | ☐ method: __________ |
| OD-8 | Reliability scale (High/Moderate/Low ↔ value) | reliability qualifier | ☐ value: __________ |
| OD-11 | Retry limits / backoff (LLM call + run) | reliability | ☐ value: __________ |
| OD-12 | Bounded-equivalence determinism tolerance | determinism tests | ☐ value: __________ |
| OD-14 | Severity assignment basis (critical/moderate/warning) | findings | ☐ rule: __________ |

*(Deep-pass and platform-wide items — OD-4, OD-9, OD-10, OD-18, OD-19, OD-20, OD-21, OD-22, OD-23 — are tracked in `OPEN_DECISIONS.md` and are out of scope for this Fast-Pass workbook.)*

---

## D. Apply procedure (after sign-off)

On receipt of this workbook with Decisions recorded, the mechanical canonization is:

1. **Section A approvals** → edit Engine §9 in place (drop 〔proposal〕/`TBD`, insert ratified values); update `analysis_constants.py` (proposal constants → canonical, fill TBD markers); add the recommendation-mapping table to the Recommendation Model.
2. **Section B approvals** → produce `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (additive field adds) + a `DATA_MODEL_RECONCILIATION_CHANGE_LOG` entry; drop `proposal` tags in `analysis_contracts.py`.
3. **Section C values** → record in a calibration decision note; the engine consumes them; `TBD` constants are replaced with the approved values.
4. **Traceability** → update `TRACEABILITY_MATRIX.md` (proposal → canonical) and close the corresponding `OPEN_DECISIONS.md` rows.
5. **Changelog** → one entry per the governance lifecycle (Backlog → Proposal → Review → Decision → Repository Change → Changelog).

No step in D is executed without a recorded owner Decision for its item.

---

*Workbook only. No canonical content is modified by this document. Approvals authorize the listed edits; rejections/defers leave the current proposal/TBD status intact.*

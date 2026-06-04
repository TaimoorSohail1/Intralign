# Clarification Candidate (Resolution Path) — Integration Specification v1 — SUPERSEDED

> ## ⛔ SUPERSEDED — founder decision (2026-05-31)
> **This integration direction is no longer in effect.** Per founder decision, Clarification Candidate is **not** a first-class persisted object; Resolution Paths are a **Recommendation substructure**. The standalone entity/lifecycle/events/endpoints below are **withdrawn**.
> - **Superseded by:** `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md`.
> - **Do not implement** the ClarificationCandidate entity, lifecycle, events, or top-level endpoints described here. Retained for history only.
> - The Future-Architecture Resolution Candidate remains untouched.

**Type:** Cross-document integration specification — **SUPERSEDED** (was: wire Clarification Candidate into the Release 1 stack)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Defines changes to (ready-to-apply, pending owner ratification):** Data Model v1.1 · State Model · Event Model · API Contract · UI Specification · Recommendation System Specification · Confidence/Recommendation Testing & Fixtures
**Source object:** `CLARIFICATION_CANDIDATE_MODEL_V1.md`

> **Governance posture.** This specification **states the exact additive changes** each ratified document needs; it **does not edit those ratified documents in place**. On owner ratification, each change is applied (Data Model → a `…_V1.2` successor + change-log entry, per the established reconciliation pattern; others additively). Every change is **additive** and introduces **no governance, scoring, formulas, thresholds, weighting, probability, autonomous action, or new doctrine**.
>
> **Critical (per owner directive):** the Future-Architecture **`RESOLUTION_CANDIDATE_MODEL_V1.md` (governance object) is NOT modified** by any change here. **Release 1: Clarification Candidate = persisted Resolution Path** (user-facing recommendation options). **Future Architecture: Resolution Candidate = governance object.** They are distinct.

---

## 0. Naming & invariants (carried into every change)

- **Internal name:** `ClarificationCandidate`. **User-facing label:** **"Resolution Path"** (sets shown as **"Possible Resolution Paths"**).
- One **Finding** → **many** Clarification Candidates (parallel options).
- A **Recommendation** may mark **one** candidate as OSLO's **recommended path** (`is_recommended`, advisory).
- The **user** may **select any** candidate, including a non-recommended one (`is_selected`). **recommended ≠ selected.**
- **Non-governance.** Selecting/recommending changes **no** CAF/Reliability/Confidence directly; only **user action → reanalysis** does.
- **Append-only** lifecycle; **explainable**; traces to ≥1 finding; coupling per `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md`.

---

## 1. Data Model v1.1 → v1.2 (additive entity + links)

**Add entity `ClarificationCandidate`:**

| Field | Type | Notes |
|---|---|---|
| `clarification_candidate_id` | UUID (PK) | identity |
| `project_id` | UUID (FK) | tenant/project scope |
| `finding_references` | array(UUID FK Finding) | **≥1** (one-or-more; cf. RS-R5 cardinality) |
| `candidate_type` | enum | Clarification · Definition · Information_Provision · Assumption_Validation · Conflict_Reconciliation · Constraint_Resolution · Dependency_Resolution · Coverage_Improvement 〔proposal taxonomy — CC-R2〕 |
| `title` | string | user-facing path label |
| `description` | text | what the path entails |
| `rationale` | text | why it could resolve the finding(s) (inherited) |
| `status` | enum(`identified`,`surfaced`,`selected`,`dismissed`,`acted_upon`,`resolved`,`superseded`) | lifecycle (§2) |
| `is_recommended` | bool | set when a Recommendation marks it OSLO's recommended path (advisory) |
| `recommended_by_recommendation_id` | UUID (FK Recommendation, nullable) | which recommendation recommends it |
| `is_selected` | bool | set by the **user**; may differ from `is_recommended` |
| `selected_by_user_id` | UUID (FK User, nullable) | who selected it |
| `first_seen_run_id` | UUID (FK AnalysisRun) | run that produced it |
| `supersedes_candidate_id` | UUID (FK self, nullable) | supersession chain (append-only) |
| `created_at` / `updated_at` | timestamp | |

**Links/constraints (additive):**
- **Finding ↔ ClarificationCandidate:** one Finding → many candidates; each candidate → ≥1 finding.
- **Recommendation ↔ ClarificationCandidate:** a `Recommendation` gains an optional `recommended_clarification_candidate_id` (FK, nullable) — the one path it recommends; **at most one recommended candidate per finding** at a time.
- Invariant: a candidate with no active source finding is **superseded** (never deleted); `is_recommended`/`is_selected` are independent booleans (both, neither, or one may be true).

*Apply as `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` + a `DATA_MODEL_RECONCILIATION_CHANGE_LOG` entry. Depends on RS-R5 (`finding_references`).*

---

## 2. State Model (additive lifecycle)

**Add "Clarification Candidate (Resolution Path) Lifecycle":**

States: `identified → surfaced → {selected | dismissed}`; `selected → acted_upon → resolved`; **any active → superseded**.

| State | Entry | Notes |
|---|---|---|
| identified | OSLO produces the candidate | created |
| surfaced | shown to the user | UI surfacing, not a decision |
| selected | user chooses to pursue it | user choice, not approval |
| dismissed | user sets it aside | user choice, not governance rejection |
| acted_upon | user acts in its direction | produces information change |
| resolved | source finding weakened/removed via reanalysis | downstream outcome (success) |
| superseded | replaced by a newer candidate | retained, append-only |

- **Append-only / no resurrection** (a dismissed/superseded candidate is not reactivated; a new one may be identified).
- **No new dimensions/assessment states**; this lifecycle changes no CAF/Confidence state. *Apply additively to the State Model (new section); consistent with §11 success semantics.*

---

## 3. Event Model (additive events)

Add events (envelope per Event Model §4; **producers/consumers** noted; **no new event semantics beyond surfacing/selection**):

| Event | Producer | Resulting transition | Consumers |
|---|---|---|---|
| `clarification_candidate_identified` | analysis/recommendation engine | → `identified` | UI |
| `clarification_candidate_surfaced` | surface | → `surfaced` | UI |
| `clarification_candidate_recommended` | recommendation cmd | sets `is_recommended` | UI |
| `clarification_candidate_selected` | **user** cmd | → `selected`, sets `is_selected` | UI |
| `clarification_candidate_dismissed` | **user** cmd | → `dismissed` | UI |
| `clarification_candidate_acted_upon` | user action signal | → `acted_upon` (feeds existing evidence/reanalysis triggers) | scheduler (existing reanalysis loop) |
| `clarification_candidate_superseded` | engine/coupling | → `superseded` | UI |

- **No new reanalysis trigger is introduced** — `acted_upon` feeds the **existing** evidence-change → reanalysis path (Event Model §15); this spec adds no autonomous trigger.
- Fan-out ordering and idempotency follow existing Event Model rules. *Apply additively.*

---

## 4. API Contract (additive endpoints/fields)

**Queries**
- `GET /findings/{fid}/resolution-paths` → list a finding's Clarification Candidates (user-facing "Possible Resolution Paths"), incl. `is_recommended`/`is_selected`.
- `GET /resolution-paths/{ccid}` → one candidate (+ basis: findings, type, rationale, linked recommendation, supersession).
- Optional embed on recommendations: `GET /recommendations/{rid}?include=recommended_resolution_path`.

**Commands (user-initiated only)**
- `POST /resolution-paths/{ccid}:select` → user selects this path (`is_selected=true`; status `selected`); emits `clarification_candidate_selected`.
- `POST /resolution-paths/{ccid}:dismiss` → user dismisses; emits `clarification_candidate_dismissed`.

**Engine/recommendation-side (not user commands)**
- A recommendation marks its recommended path via `recommended_clarification_candidate_id` (set on recommendation generation); surfaced read-only to clients as `is_recommended`.

- **No endpoint** allows OSLO to *act on* or *apply* a path, or to *select* on the user's behalf (human-in-the-loop; CC-4). *Apply additively under `/v1`.*

---

## 5. UI Specification (additive)

Under a finding's recommendation area, add **"Possible Resolution Paths"**:
- List the finding's Resolution Paths (Clarification Candidates), each with title, type, and rationale.
- **Mark OSLO's recommended path** distinctly (the `is_recommended` candidate) — labeled as OSLO's suggestion, clearly **advisory**.
- **Allow the user to select** any path (including a non-recommended one); reflect `is_selected`; allow dismiss/defer.
- Show state (identified/surfaced/selected/…); show superseded paths collapsed (append-only history).
- **Never** present selection as an approval/decision; **never** auto-select; surface the "recommended ≠ selected" distinction honestly.
- Refresh on the §3 events (event-driven, per UI §20). *Apply additively to UI §7/§9 (recommendation surfaces).*

---

## 6. Recommendation System Specification (additive clarification)

Add to the Recommendation System Spec (§3/§4 or a new note):
- **A Recommendation may be generated from, or linked to, a Clarification Candidate (Resolution Path):** the recommendation may **identify one candidate as OSLO's recommended path** (`recommended_clarification_candidate_id` / `is_recommended`).
- **The user may act on a different path** than the recommended one; the recommendation remains advisory and its success is still measured by finding weakening/removal via reanalysis (§11), regardless of which path the user took.
- This is a **clarification of the existing advisory relationship** — it adds **no** new lifecycle state to the Recommendation and no governance. *(Record alongside §11b, now realized by the Clarification Candidate object.)*

---

## 7. Testing & Fixtures (additive)

**Tests (structural; map to CC-1…CC-10 / coupling RFC-*):**
- **Multiple paths:** a finding with multiple Clarification Candidates coexisting as parallel options.
- **Recommended path:** exactly one candidate flagged `is_recommended` by a recommendation; others not.
- **Selected = recommended:** user selects OSLO's recommended path.
- **Alternate path:** user selects a **non-recommended** path (`is_selected ≠ is_recommended`); recommendation remains advisory; no CAF/Confidence change from selection.
- **No-direct-assessment-change:** selecting/dismissing changes no CAF/Reliability/Confidence (CC-3).
- **Acted-upon → reanalysis:** acting on a selected path produces information change → reanalysis → finding weakened/removed (success, §11) via the existing loop.
- **Supersession:** a candidate superseded (e.g., source finding removed) is retained, not deleted; not resurrected on finding reopen (coupling spec §3).
- **Coupling:** multi-finding candidate re-attributes / supersedes per `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md`.

**Fixture families (per `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md` framework):**
- **Multiple-path fixtures** (one finding, several candidates).
- **Recommended-vs-selected fixtures** (divergent selection).
- **Path-supersession fixtures** (finding change → candidate supersession).

*Apply additively to the Recommendation/Confidence test + fixture specs; no numeric criteria introduced.*

---

## 8. Application order & dependencies

1. **RS-R5** (`finding_id` → `finding_references`) and **Data Model v1.2** (§1) — foundational.
2. **State Model** (§2) + **Event Model** (§3) — lifecycle/events.
3. **API** (§4) + **UI** (§5) — surfaces.
4. **Recommendation System Spec** (§6) clarification.
5. **Tests/Fixtures** (§7).

Each step is owner-ratifiable independently; none modifies the Future-Architecture governance Resolution Candidate.

---

## 9. Reconciliation / proposal status

| ID | Item | Status |
|---|---|---|
| CCI-1 | `ClarificationCandidate` entity + links (Data Model v1.2) | **Proposal** — apply on ratification |
| CCI-2 | Lifecycle (State Model) | **Proposal** |
| CCI-3 | Events (Event Model) | **Proposal** |
| CCI-4 | API endpoints/fields | **Proposal** |
| CCI-5 | UI "Possible Resolution Paths" | **Proposal** |
| CCI-6 | Recommendation System clarification | **Proposal** |
| CCI-7 | Tests/fixtures | **Proposal** |
| CCI-8 | Depends on RS-R5 (finding cardinality) | **Linked** |
| CCI-9 | Taxonomy reconciliation (CC-R2) | **Proposal** |

**Governance:** all additive; owner ratifies before application; the Future-Architecture Resolution Candidate is untouched throughout.

---

*This integration specification wires the Clarification Candidate (user-facing Resolution Path) into the Release 1 stack as concrete, additive, ready-to-apply changes — persisted entity, lifecycle, events, API, UI, recommendation linkage, and tests — without editing any ratified document in place and without modifying the Future-Architecture governance Resolution Candidate. Apply on owner ratification.*

**Clarification Candidate Integration Specification v1 complete.**

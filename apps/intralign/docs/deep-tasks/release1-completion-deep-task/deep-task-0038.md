# DTM-0038 — Read-shape additions (Issue DTO + GET issues, overview/counts, CHR history feed)

**Status:** In progress · **Module:** DTM-0038 · **Phase:** Completion · **Contract:** API §5 + LDM
§2–3 + Data Model v1.2 · **Depends:** DTM-0018 (render/read), DTM-0030 (materializer). **Branch:**
`feat/release1-completion`.

## Goal / observable behavior

The three read-surface gaps the Wave E surfaces flagged are closed with first-class reads:
- **Issue:** an `Issue` DTO (`shared/entities.py`) + render mapper + `GET /v1/projects/{pid}/issues`
  reading the **existing `derived.issue_current` projection** (the materializer DTM-0030 already
  populates `issue` CHRs → `issue_current`). (DTM-0023 currently derives issues from
  finding-with-severity — this gives them first-class identity.)
- **Overview/counts:** an `Overview`/counts DTO + `GET /v1/projects/{pid}/overview` aggregating the
  governed objects (finding/issue/recommendation counts + aggregate outcome confidence/CAF). Counts
  are presentation of governed objects, not a computed health metric.
- **History feed:** a unified CHR-trail DTO + `GET /v1/projects/{pid}/history` reading the CHR log
  (via the chr repo / a history read seam) — the "what OSLO said when" trail (DTM-0027 currently
  reconstructs from analysis-runs).
All read-only, workspace-scoped, epistemic labels preserved.

## Source docs / constraints

- API §5 (the read operations the screens need) + the UI_SCREEN_INVENTORY (issues/overview/history
  reads). LDM §2.2 (CHR) + §3.1 (projection) + §2 (Issue = prioritized Finding). Data Model v1.2
  (`shared/entities.py` — add the Issue/Overview/History DTOs, Data-Model-aligned). decisions #4, #6.
- Code: `backend/services/render/read_seam.py` (`list_projection("issue", …)` already works;
  add overview aggregation + a history/CHR read), `backend/services/render/mappers.py` (add
  issue_to_dto + overview + history mappers), `backend/api/v1/routers/` (ADD issues/overview/history
  GET routers beside the existing reads), `backend/responsibilities/retain/repository.py`
  (`ChrRepository` — `latest_for_output`/`lineage_chain` for the history feed), `shared/entities.py`.

## Locked decisions (do not re-derive)

- **Issue is first-class via `derived.issue_current`** (the materializer populates it). The Issue DTO
  carries its epistemic label (Derived + band + conflict) + source-finding lineage. No invented field
  (Data Model v1.2). The render mapper maps `issue_current` → Issue DTO (mirror finding_to_dto).
- **Overview = counts + aggregates, NOT health** — present finding/issue/recommendation counts +
  outcome confidence/CAF (each labelled); never a health/readiness/probability score (the Wave E
  not-project-health rule). Counts come from the governed lists.
- **History feed = the CHR trail** — read-exact, append-order; each entry Derived-labelled; plan
  facts/UARs user-attested if the feed includes them (or keep the feed CHR-only + the existing UAR/
  plan-fact reads — confirm the screen's need; don't over-build).
- All **read-mostly** (the DTM-0018 read-mostly negatives extend to these — GET only, no verbatim
  internal-type leak). No new dependency. No migration (issue_current exists).

## Owned files / boundaries

- **OWN:** `shared/entities.py` (Issue/Overview/History DTOs — additive) · `backend/services/render/
  {mappers,read_seam}.py` (add the mappers + overview/history reads) · `backend/api/v1/routers/`
  (issues/overview/history GET routers) + include · `tests/{positive,negative}/{api,render}/**`.
- **READ-ONLY:** the materializer + chr repo (read, don't change), the command routers, migrations,
  cognition.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest): `issue_to_dto` maps `issue_current` → Issue DTO (label + lineage); `GET …/issues`
   returns them; overview aggregates counts + confidence/CAF (labelled, not-health); history feed
   returns the CHR trail (append-order, Derived-labelled). **Negatives:** no internal cognition type
   leaked verbatim; overview never reads health/probability; GET-only (read-mostly); workspace-scoped.
2. Build the DTOs + mappers + read-seam reads + the 3 GET routers; include in `v1/__init__.py`.

## API / data / schema contracts

- Issue/Overview/History DTOs (Data Model v1.2), each carrying epistemic labels where Derived. No
  schema change (issue_current + CHR log exist).

## Test plan

- **Positive:** issues (labelled + lineage); overview (counts + aggregates, labelled); history
  (CHR trail, append-order); workspace-scoped.
- **Negative:** no verbatim internal-type leak; overview not-health; GET-only; cross-workspace 404.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 green.

## Manual checks (EM)

- `GET …/issues` → Issue DTOs from issue_current; `GET …/overview` → counts + confidence/CAF, no
  health wording; `GET …/history` → the CHR trail in append order.

## Done criteria

- Issue DTO + GET issues (from issue_current), overview/counts, CHR history feed — first-class reads,
  labels preserved, read-mostly, not-health, no verbatim leak (negative-proven), no new dep/migration,
  gates green. PR cites API §5 / LDM. Ready for DTM-0039 (frontend wiring).

## Worker report

**Status: Ready for review.**

Closed the three Wave E read-surface flags with first-class, read-only,
workspace-scoped reads. All additive; no command router / materializer / chr repo
/ migration touched; no new dependency.

### The 3 reads (DTO + mapper + endpoint)

1. **Issue** — first-class via `derived.issue_current`.
   - DTO `Issue` (`shared/entities.py`): the Finding field set (`finding_type` /
     `severity` / `summary` / `evidence_links` / `status` / dims) + its own
     identity `issue_id` + the **source-Finding lineage `finding_id`** + the
     `DerivedEnvelope` `label` (Derived + band + conflict). No field invented:
     Object Model §8 makes Issue the Derived prioritized Finding (`Issue ──from──>
     Finding`, severity an attribute); Data Model v1.2 introduces no new entity, so
     the DTO mirrors the Finding field set + Issue identity/lineage.
   - Mapper `issue_to_dto` (mirrors `finding_to_dto`, reuses `_finding_type`):
     reads `issue_current` `current_payload` + envelope; drops the internal-only
     payload fields (`mode` / `confidence_stage` / `understanding_state` /
     `epistemic_state`).
   - Endpoint `GET /v1/projects/{pid}/issues` (+ `?finding_id=` filter) and
     `GET /v1/issues/{issue_id}` (404 outside scope). Reads the EXISTING
     `list_projection("issue", …)` — the DTM-0030 materializer populates it.

2. **Overview / counts** — `GET /v1/projects/{pid}/overview` → `Overview` DTO.
   - Aggregates the governed lists: labelled `GovernedCount` for
     finding/issue/recommendation + the Derived `outcome_confidence` (band
     pass-through) + `caf` (mapped through their existing Derived mappers, band
     travels). Mapper `overview_to_dto` computes nothing new — every number is a
     count of, or a labelled pass-through of, an already-governed object.
   - **NOT health:** the DTO has no `health` / `readiness` / `score` /
     `probability` field by construction (negative-proven on the DTO field set AND
     the serialized OpenAPI schema).

3. **History feed** — `GET /v1/projects/{pid}/history` → `list[HistoryEntry]`.
   - Reads the append-only `cognition_history_record` log via a new SELECT-only
     `HistoryReader` / `SupabaseHistoryReader` (`order(emitted_at, asc)` —
     append-order, oldest first). Mapper `history_entry_to_dto` reads each CHR
     EXACT (`chr_id` / `output_kind` / `recompute_trigger` / `supersedes_chr_id` /
     `emitted_at`), Derived-labelled `attested-oslo` (a CHR is OSLO-self-attested).
     Drops the internal CHR fields (`output_payload` / `model_or_rule_version` /
     `upstream_lineage` / `input_attestation_version`).

### History: CHR-only vs with UAR/plan-fact — **CHOSE CHR-only.**

The history feed is the "what OSLO said when" Cognition-History trail (CHR log).
The user-attested receipts (UAR / plan facts) are ALREADY exposed by the existing
DTM-0018 reads (`GET …/acceptance`, `GET …/plan-facts`) — folding them in would
duplicate those reads and mix two epistemic classes on one feed. CHR-only keeps
the trail a single Derived/OSLO-self-attested append-order surface; the existing
user-attested reads cover the rest (the task explicitly permits this).

### Negatives proven

- **No verbatim internal-type leak** (extends the DTM-0018 negative): the
  Issue/HistoryEntry OpenAPI schemas carry none of the internal cognition fields
  (`mode` / `confidence_stage` / `understanding_state` / `model_or_rule_version` /
  `output_payload` / `upstream_lineage` / `input_attestation_version`); the Issue
  render mapper drops the internal payload fields while the label still travels;
  `entities.Issue` is a distinct type from the internal Evaluate Issue.
- **Overview not-health:** no health/readiness/score/probability field on the DTO
  or its OpenAPI schema.
- **GET-only / read-mostly:** the `issues`/`overview`/`history` tags are added to
  the read-surface guard — proven no mutating method, no `:verb` path; the new
  `SupabaseHistoryReader` has no insert/update/delete/upsert/append.
- **Cross-workspace 404:** issue detail for a missing id → 404; the existing
  out-of-workspace project → 404 guard covers scoping.

### Verify (exact commands + results)

- `cd code && .venv/bin/pytest tests/positive tests/negative -q`
  → **737 passed, 65 skipped, 3 warnings** (no regression; the OTel
  export-failure lines are the pre-existing collector-absent warnings, unrelated).
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS**.
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS** (reads emit no
  events; CHR-append vocab unchanged).
- Confirmed: **no new dependency, no migration**; the command routers, the
  materializer (`disclose/projection_writer.py`), and the chr repo
  (`retain/repository.py`) are **unchanged** (`git diff --name-only` touches only
  `shared/entities.py`, `services/render/{mappers,read_seam,__init__}.py`,
  `api/deps.py`, `api/v1/__init__.py`, the 3 new routers, and tests).

### Data-Model flag

**None.** Every Issue field maps onto the Finding Data-Model field set + the
Object-Model Issue identity/lineage; Overview/History carry only governed-object
counts / CHR-receipt fields. No screen-needed field is absent from the model, so
no STOP/escalation was required.

### Files

- `shared/entities.py` — `Issue`, `GovernedCount`, `Overview`, `HistoryEntry` DTOs.
- `backend/services/render/mappers.py` — `issue_to_dto`, `overview_to_dto`,
  `history_entry_to_dto`.
- `backend/services/render/read_seam.py` — `HistoryReader` protocol +
  `SupabaseHistoryReader` (CHR-log SELECT).
- `backend/services/render/__init__.py` — exports.
- `backend/api/deps.py` — `get_history_reader` provider.
- `backend/api/v1/routers/{issues,overview,history}.py` — the 3 GET routers;
  included in `backend/api/v1/__init__.py`.
- Tests: `tests/positive/render/test_mappers.py`,
  `tests/positive/api/{conftest,test_read_endpoints}.py`,
  `tests/negative/render/test_no_verbatim_leak.py`,
  `tests/negative/api/test_read_surface_negatives.py`.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Three first-class reads close the Wave E flags: Issue DTO + `GET …/issues` (+ `/issues/{id}`) from
  `derived.issue_current` (materializer-populated), with source-Finding lineage; Overview DTO +
  `GET …/overview` (governed counts + outcome confidence/CAF, not-health); History DTO +
  `GET …/history` (CHR trail, append-order, Derived-labelled, CHR-only). API §5 / LDM §2–3.

Verification (EM re-ran): `.venv/bin/pytest` → **737 passed, 65 skipped** (16 new; no regression).
ruff clean; gate-4 PASS; gate-5 PASS. No new dep, no migration; command routers/materializer/chr
repo untouched.

Negatives proven: no verbatim internal-type leak (Issue/HistoryEntry schemas + mappers); Overview
has no health/readiness/score/probability field (DTO + OpenAPI schema); GET-only read surface;
cross-workspace/missing-id 404.

Decisions: History feed is CHR-only (UAR/plan-fact already exposed by existing reads — no
duplication, no epistemic-class mixing). No Data Model flag (Issue = Object-Model prioritized
Finding; no invented field).

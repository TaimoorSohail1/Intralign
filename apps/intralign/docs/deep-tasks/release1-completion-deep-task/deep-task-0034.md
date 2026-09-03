# DTM-0034 — REST: project CRUD + evidence/artifact intake

**Status:** In progress · **Module:** DTM-0034 · **Phase:** Completion · **Contract:** API §5
(98–116) + Event §8 · **Depends:** DTM-0031 (project table/repo) + the existing intake seam.
**Branch:** `feat/release1-completion`.

## Goal / observable behavior

A user can create a project and feed it evidence (the start of the flow). New command endpoints:
- `POST /v1/projects` `{title?, description?}` → Project(`created`), emits `project_created`.
- `PATCH /v1/projects/{pid}` `{title?, description?}` → Project, `project_updated`.
- `POST /v1/projects/{pid}:archive` → Project(`archived`), `project_archived` (owner/admin).
- `POST /v1/projects/{pid}/evidence` `{source_type, content_ref, provenance?}` → Evidence, emits
  `evidence_added`; wires the EXISTING intake/admission seam (promotion candidate → attested
  assertion) where applicable.
- `POST /v1/projects/{pid}/artifacts` (+ `POST /artifacts/{aid}/versions`) → Artifact/version,
  `artifact_created`/`artifact_version_created`.
Project writes via the DTM-0031 `project_repo`; evidence/artifact via the EXISTING intake store
(`backend/services/persistence/` `SupabaseIntakeStore` / promotion candidate) + admission. Returns
the affected DTO; `Idempotency-Key`; workspace-scoped; RBAC for archive.

## Source docs / constraints

- API §5 (98–116) — the endpoints (path/method/request/response/idempotency/events/roles). Event §8
  (`project_*`, `evidence_added`, `artifact_*`). LDM §2.3 (Artifact/Promotion Candidate — canonical
  evidentiary anchors, append-only/versioned). `code/CONTEXT.md` (intake → promotion candidate →
  admission → attested assertion). decisions #4, #5.
- Code: `backend/platform/project_repo.py` (DTM-0031), the intake seam (`backend/services/
  persistence/` intake store + `backend/responsibilities/perceive`/`retain` admission —
  `admit_candidate` builds a TriggerClaim), `backend/api/v1/routers/projects.py` (existing GET — ADD
  a command router) + any artifacts/evidence GET, `backend/api/deps.py` (Principal/RBAC/idempotency),
  `shared/entities.py` (Project/Evidence/Artifact DTOs), events + gate-5.

## Locked decisions (do not re-derive)

- **Wire the existing seams** — project_repo for project CRUD; the intake store + admission for
  evidence/artifacts. Invent no intake/admission logic. Admission writes the attested assertion via
  the EXISTING append-only path (do not write canonical directly from the router).
- **RBAC:** archive requires owner/admin (Principal.role); 403 otherwise (API §3).
- **Evidence intake does NOT auto-run analysis here** — it persists + emits `evidence_added` (a
  Fast/Deep precondition); the user triggers analysis via the DTM-0032 endpoint (keep slices
  separate). (If the contract mandates auto-Fast-on-first-evidence, wire `submit_trigger` like
  DTM-0032 — confirm from API §5/Event §8.8; else flag.)
- Additive command router; GET readers + negatives stay green. Emit the §8 events (gate-5 vocab).
  `Idempotency-Key`; workspace-scoped. No new dep/migration (project/artifact tables exist via
  DTM-0031 + the intake migration; if an `evidence`/`artifact` table is genuinely missing ⇒
  STOP/flag, do not add a migration in this slice).

## Owned files / boundaries

- **OWN:** `backend/api/v1/routers/project_commands.py` (+ evidence/artifact commands) + include ·
  `backend/api/v1/schemas/` · DI in `deps.py` · `tests/{positive,negative}/api/**`. Event vocab +
  gate-5 fixtures.
- **READ-ONLY:** the intake/admission internals + project_repo (call, don't change), read routers/
  seam, migrations, cognition.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest, TestClient + overrides): create/patch/archive project (repo asserted, events,
   lifecycle); add evidence → intake seam called + `evidence_added`; create artifact/version.
   **Negatives:** 401 unauth; 404 cross-workspace; 403 archive without owner/admin; the command
   writes no canonical row directly (admission does, via the frozen path); idempotency; read routers
   unchanged.
2. Build the command router wiring project_repo + intake; include in `v1/__init__.py`.

## API / data / schema contracts

- Returns Project/Evidence/Artifact DTOs (Data Model v1.2). Emits `project_created/updated/archived`,
  `evidence_added`, `artifact_created/version_created`. No schema change (STOP/flag if a needed table
  is missing).

## Test plan

- **Positive:** project create/patch/archive (+events+lifecycle); evidence add (intake + event);
  artifact + version; idempotency; scoping; RBAC.
- **Negative:** 401/403/404; no direct canonical write from the command; read routers unchanged.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 (new vocab) green.

## Manual checks (EM)

- POST /projects → a project row (created) + event; it appears in GET /projects (the dashboard);
  POST evidence → persisted + `evidence_added`; archive needs owner/admin.

## Done criteria

- Project CRUD + evidence/artifact intake wire the existing seams + repos, emit §8 events, RBAC on
  archive, idempotent + scoped, no direct canonical write, read routers unchanged, gates green, no
  new dep/migration. PR cites API §5. Ready for DTM-0035.

## Worker report

**Status: Ready for review.** Additive command router for the start of the flow
(create project → add evidence/artifacts). Every endpoint wires an EXISTING seam;
the transport writes no canonical store and adds no dep/migration.

### Endpoints + how each wires the seam

New router `backend/api/v1/routers/project_commands.py` (included in `v1/__init__.py`
after the DTM-0033 acceptance router); request schemas in
`backend/api/v1/schemas/projects.py`; DI providers in `backend/api/deps.py`.

| Endpoint | Seam wired | Event | Notes |
|---|---|---|---|
| `POST /v1/projects` `{title?,description?}` | `project_repo.create` (DTM-0031 platform `project` table) | `project_created` | Project(`created`); `workspace_id`/`created_by_user_id` scoped from the Principal; returns the `Project` DTO; 201. |
| `PATCH /v1/projects/{pid}` `{title?,description?}` | `project_repo.update` | `project_updated` | metadata-only patch (`exclude_none`); 404 cross-workspace before any write. |
| `POST /v1/projects/{pid}:archive` | `project_repo.update_lifecycle('archived')` | `project_archived` | **owner/admin only** (`Principal.role`) → 403 otherwise; 404 checked first so a member learns nothing about out-of-scope projects. |
| `POST /v1/projects/{pid}/evidence` `{source_type,content_ref,provenance?}` | EXISTING `perceive.intake.submit_artifact` (body→Storage `ArtifactBodyStore`; metadata+provenance→append-only `artifact` anchor + `promotion_candidate` via `SupabaseIntakeStore`) | `evidence_added` | returns the persisted intake `artifact` row (the LDM §2.3 evidence anchor); idempotent on `dedup_key` (identical resubmit → one artifact). |
| `POST /v1/projects/{pid}/artifacts` `{artifact_type,content}` | same `submit_artifact` seam | `artifact_created` | version 1 artifact. |
| `POST /v1/artifacts/{aid}/versions` `{content,authored_by_kind?}` | same seam — resubmits the parent's project+source | `artifact_version_created` | the intake seam appends `version+1` / `supersedes_id`; 404 if parent absent or cross-workspace. |

All commands accept `Idempotency-Key` (the DTM-0032/0033 in-process store, keyed by
`(key, route)`) — a retry replays the first resource, no second persist. The DI
pattern mirrors DTM-0032/0033 (`get_project_repo`, `get_intake_store`,
`get_body_store`, plus the shared `get_event_emitter`/`get_idempotency_store`/
`get_projection_reader`/`require_principal`), all overridable via
`app.dependency_overrides`.

### Auto-Fast-on-evidence finding (checked from the contract)

**The contract does NOT mandate auto-Fast on first evidence.** API §5 lists
`evidence_added` as "*(Fast precondition / Deep trigger)*" and `artifact_created`
as "*(may satisfy Fast precondition)*"; Event Model §5 says `project_created`
"arms the Fast Analysis trigger (fires once first analyzable input exists, §15)",
and §15 Fast Analysis is "**Triggered by** `project_created` **followed by** the
first analyzable input". "Arms / precondition / qualifies" — not "runs". The
Start-Fast-Analysis command is itself a separate explicit endpoint (`POST
…/analysis-runs:fast`, DTM-0032). **What I did:** the evidence/artifact commands
persist + emit only; they do NOT call `submit_trigger`. The user runs analysis via
the DTM-0032 command (slices kept separate, matching the locked decision). This is
consistent with the §5 contract.

### Missing-table flag

**No table is missing — no STOP required.** There is no standalone `evidence` or
`artifact` (DTO-named) table, and that is correct: the intake migration
`supabase/migrations/20260612100000_intake_artifact_candidate.sql` defines
`public.artifact` as the LDM §2.3 **"canonical append-only Artifact (evidence
anchor)"** plus `public.promotion_candidate`. Evidence AND artifacts both flow
through this one intake anchor (the `submit_artifact` seam), exactly as the LDM
intends (intake → promotion candidate → admission → attested assertion). The
attested `attested_assertion` rows are written downstream by `retain.admission.
admit_candidate` over the existing append-only canonical migration — the command
router never touches them. The platform `project` table exists via DTM-0031
(`20260626120000_platform_tables.sql`).

Note: `shared/entities.py` has no `Evidence` DTO and its `Artifact`/`PlanningArtifact`
is the Wave-S Derived planning artifact, not the intake anchor. Per the
ANTI_ASSUMPTION protocol I did NOT invent a new canonical Pydantic DTO; the
evidence/artifact endpoints return the persisted intake `artifact` row (the seam's
output) as the affected resource. Project commands return the canonical `Project`
DTO via the existing `project_to_dto` mapper.

### Events + gate-5

Added three command vocabularies, verbatim against the Event Model, to BOTH
`backend/services/observability/events.py` and `ci/gate_observability.py`, plus the
union legs (appended after RECOMMENDATION — grows, never reorders) and the
`_CONTRACT_VOCABULARIES`/`_UNION_NAME_ORDER` tuples:

- `EVENT_NAMES_PROJECT` = `("project_created","project_updated","project_archived")` (EM §5)
- `EVENT_NAMES_ARTIFACT` = `("artifact_created","artifact_version_created")` (EM §6; `artifact_updated` is a later state-command slice, intentionally NOT pinned)
- `EVENT_NAMES_EVIDENCE` = `("evidence_added",)` (EM §7; `context_item_*` are extraction-engine emissions, not this command)

Both gate-5 fixtures updated: the positive `test_gate_observability.py` (imports,
the live-seam drift assertion, the 15-way union concatenation, a new verbatim pin
test) and the negative `test_gate_observability_negative.py` (the self-contained
`GOOD_EVENTS_PY` + its union legs, the missing-assignment count `13`→`16` with the
three new `not found` assertions, and the `union_dropping` literal).

### Negatives proven (the Critical guards)

- **RBAC on archive:** a `member` → 403 and `repo.update_lifecycle` is never called;
  `admin` is allowed (owner/admin both pass).
- **No direct canonical write:** the evidence command wires only the intake store
  (which has no `insert_assertion`/CHR surface) — the attested assertion is written
  by admission downstream, never by the router.
- **401** unauth (create + add-evidence) with nothing persisted; **404**
  cross-workspace (evidence + archive, existence not leaked) with no intake/lifecycle
  write; idempotency replay (one persist); GET projects reader stays GET-only.

### Verify — exact commands + results

```
cd code && .venv/bin/pytest tests/positive tests/negative -q
  → 661 passed, 65 skipped, 1 warning  (no regression; the 65 skips are the
    pre-existing live-Supabase/LLM suites; OTLP export errors at the tail are
    pre-existing harness noise — no collector running)

.venv/bin/pytest tests/positive/api/test_project_commands.py \
  tests/negative/api/test_project_command_negatives.py \
  tests/positive/observability/test_gate_observability.py \
  tests/negative/observability/test_gate_observability_negative.py -q
  → 63 passed

.venv/bin/ruff check .                  → All checks passed!
.venv/bin/python ci/gate_invariants.py  → [gate-4 epistemic-invariant] PASS
.venv/bin/python ci/gate_observability.py → [gate-5 observability] PASS (new names)
```

Confirmed: **no new dependency** (no requirements/pyproject change), **no new
migration** (`supabase/` untouched), **GET readers untouched**
(`routers/projects.py` unchanged), and the intake/admission internals +
`project_repo` are call-only (none of those modules appear in the diff). Changes
staged for review; unrelated working-tree state preserved.

PR cites **API §5 (98–116)** + Event Model §5/§6/§7. Ready for DTM-0035.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- New additive `project_commands` router: project create/patch/`:archive` (via DTM-0031 project_repo,
  RBAC on archive) + evidence/artifact intake (via the EXISTING `perceive.intake.submit_artifact` →
  append-only `artifact` anchor + promotion candidate). Emits project_*/evidence_added/artifact_*.
  API §5.

Verification (EM re-ran): `.venv/bin/pytest` → **661 passed, 65 skipped** (63 new; no regression).
ruff clean; gate-4 PASS; gate-5 PASS (project/artifact/evidence vocab pinned). No new dep, no
migration; GET `projects.py` reader unchanged; intake/admission/project_repo call-only.

Negatives proven: 401 unauth; 404 cross-workspace; 403 archive without owner/admin (no lifecycle
write); command writes no canonical row directly (admission does, via frozen path); idempotency replays.

Findings (correct ANTI_ASSUMPTION calls): auto-Fast-on-evidence is NOT mandated (evidence_added is a
Fast precondition; the user triggers via DTM-0032) — no submit_trigger here. No missing table:
`public.artifact` IS the LDM §2.3 evidence anchor (evidence + artifacts both flow through intake).

Remaining risks / follow-up: evidence/artifact endpoints return the raw intake `artifact` dict
(`response_model=dict`) — no `Evidence`/intake-`Artifact` DTO exists in `shared/entities.py` and
inventing one would breach ANTI_ASSUMPTION. Typed external DTOs for these = a Data Model follow-up.

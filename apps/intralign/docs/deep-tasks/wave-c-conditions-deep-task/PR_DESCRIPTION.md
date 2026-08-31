# Wave C exit-gate conditions — RB-025 (unarchive) + RB-026 (CAF decomposability) + latency harness

**Branch:** `feat/wave-c-conditions` · **Discharges:** DL-072 carried conditions (RB-025, RB-026, DL-046/DL-070 latency) · **Layer:** engineering realization (`code/`, non-canonical) + one LDM §2.5 vocabulary edit

**Contracts:** `IC-WA-002` (Retain — unarchive / RB-025), `IC-WB-EVAL` (Evaluate — CAF decomposability / RB-026). Observability: `OBS-WA-002` (retention events — see escalation).

## Why

DL-072 passed the Wave B exit gate with three binding conditions to land in/by Wave C. This PR
clears the two buildable ones and ships a runnable harness for the third, so the Wave C exit gate
(the Wave C exit-gate review — a separate governance draft) can be ratified and Phase V / Wave U
authorized. No canonical content is ratified here — owner ratifies the gate separately.

## What changed

### Slice 1 — CAF decomposability negative test (RB-026 / DL-062 C1)
- **New:** `tests/negative/evaluate/test_b3_caf_decomposability.py`.
- Proves the DL-062 Condition 1 invariant (Doctrine 06 prevails): CAF drivers + per-dimension
  reliability sub-axes stay **individually inspectable**; an **opaque rollup is rejected**; the
  three drivers can't collapse to fewer.
- No production change — the evaluate models already decompose; this closes the missing QA negative.

### Slice 2 — Unarchive (RB-025 / DL-058; UP-3 affirmed)
- **`backend/responsibilities/retain/archival.py`:** add `unarchive_assertion` (+ `UnarchivalResult`,
  `NotArchivedError`); append-only reversal (`event_type='unarchived'`), emits `knowledge_unarchived`
  + `knowledge_mutation_recorded`, no row mutated/deleted. `is_archived` now derives status as the
  **latest of `archived`/`unarchived`** over oldest-first history (archive → reverse → re-archive).
- **`backend/responsibilities/retain/__init__.py`:** export the new symbols.
- **`30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` §2.5:** add `unarchived` to the
  `History Record.event_type` vocabulary.
- **Event registries:** register `knowledge_unarchived` in `backend/services/observability/events.py`
  and `ci/gate_observability.py`.
- **New tests:** `tests/positive/retain_retention/test_b2_unarchival.py` (6 cases: reversal appends +
  emits; status flips to active; non-destructive; re-archive latest-wins; missing → `AssertionNotFoundError`;
  not-archived → `NotArchivedError`, no spurious event). Updated the two observability vocabulary
  assertions (positive + negative fixture) to the six-event set.

### Slice 0 — Live-Gemma latency proof (DL-072 C3 / DL-046 / DL-070)
- **New:** `code/scripts/latency_proof/run_latency_proof.py` + `README.md`.
- Measures Time-to-First-MRI on a **live internal-Gemma** Fast-Pass (CI's "live" e2e uses recorded
  fixtures — zero provider calls — which is why the live-Gemma latency is unproven). Gates on the
  **ratified <60s ceiling** at the Tier-1 envelope; reports p50/p95 as **owner-TBD (OPEN_TBD A2)**.
- **Runs in the owner/engineering environment only** (needs live Gemma + Supabase); produces the
  JSON evidence to attach to the exit-gate review.

## ⚠️ Escalation — contract change (owner / EM review)

Unarchive adds a **sixth** retention event, expanding the **OBS-WA-002** contract's "five retention
events, exactly" to six. OBS-WA-002 is a **co-governed `20_handoff` contract**. The code/registries/
tests here are kept coherent, but the **contract doc + the RELEASE_1 traceability matrix must be
updated to match** — intentionally **not** edited in this PR (co-governed seam, not unilateral).
Flagged in-code at both registries.

(Minor, also engineering-to-confirm: the live latency harness may need a `prompt_suffix_for` argument
the recorded e2e supplies as a fixture concept — `E-harness` note in the script.)

## Test plan

- **Static (done in-branch):** `py_compile` + `ruff` clean across all 9 changed files.
- **Verified against real models:** Slice 1's DL-062 invariants executed green against
  `shared.epistemic` (3 inspectable dims; opaque-rollup rejected; can't-collapse). Slice 2's
  `is_archived` latest-wins algorithm verified across archive→unarchive→re-archive sequences.
- **Required in CI (Python 3.11 — could not run in the authoring sandbox):**
  - `pytest tests/negative/evaluate/test_b3_caf_decomposability.py`
  - `pytest tests/positive/retain_retention/test_b2_unarchival.py`
  - `pytest tests/positive/observability tests/negative/observability` (vocabulary now six events)
  - full offline + live(env-gated) suite; **ruff + gate-4 + gate-5 + gate-observability green**; no
    baseline regression (Wave C head was live 587 / 0).
- **Owner environment:** run `scripts/latency_proof/run_latency_proof.py --runs 30`; attach the JSON
  + Grafana/Tempo trace IDs to the exit-gate review.

## Out of scope / follow-ups

- OBS-WA-002 contract + traceability-matrix update (escalation above).
- Wave C exit-gate **ratification** (owner, Founder Console) and the Phase IV plan status reconcile.
- Paid-tier latency envelopes (OPEN_TBD A1/A3) — Tier-1 only is proven here.

## Governance

Lands on a branch → PR → green doc-integrity + app-CI gates → **owner merge**. Never pushed to
`main`. AI authored realization + recommended; the owner ratifies policy intent and the exit gate.

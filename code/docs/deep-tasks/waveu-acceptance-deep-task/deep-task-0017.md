# DTM-0017 — Acceptance-Impact Assessment: reconcile-on-drift (Derived), via the 00R recompute

> **Ready for review.**

**Status:** **Approved** (EM, 2026-06-18) · **Module:** DTM-0017 · **Phase:** V
(Wave U) · **Contract:** **IC/QA/OBS-WU-ACCEPT** (U1.3) + **Calibration §3** · **Depends:**
DTM-0016 (UAR + plan fact, landed), Wave B (the values that drift), the 00R recompute backbone.

## Goal / observable behavior

When the understanding behind a **user-accepted** item later moves, OSLO surfaces it. After a
recompute produces new values, Evaluate scans the project's **active version-pinned UARs**; for
each, it compares the **latest** value for the accepted item against the value at the
**version-pinned** CHR; if the drift is **≥10 pts or a band change** (Calibration §3), it emits
an **`AcceptanceImpactAssessment`** — Derived, recomputable, `output_kind=acceptance_impact`,
appends a CHR, supersedes a prior assessment for that UAR — and emits `acceptance_impact_assessed`
("a decision you confirmed is affected"). The impact comparison is **Derived cognition**, never
canonical; it mutates neither the UAR nor the plan fact.

## Source docs / constraints

- `WAVE_C_AND_U…ADVISORY_AND_ACCEPTANCE.md` **Wave U** U1.3 (reconcile-on-drift, Derived,
  appends CHR), U2 (positive: drift raises an assessment; negative: impact-as-canonical), U3
  (events/audit/replay). **Calibration §3** (Acceptance-Impact drift = ≥10 pts or band change vs
  the version-pinned acceptance).
- ADR-0009 (reconcile owned by Evaluate, runs post-Evaluate in the recompute); `deep-task-
  decisions.md` #5–#8, #10; DTM-0013 CHR-model pattern; ADR-0004.

## Locked decisions (from decisions file — do not re-derive)

- **Owner: Evaluate** (owns value/band semantics). Add `evaluate/acceptance_impact.py` — a
  **pure compare**: (pinned CHR value, latest CHR value) → drift? (≥10 pts or band change). No
  LLM (rule comparison).
- **Wiring (least-invasive):** run the reconcile in the recompute **after Evaluate**, via the
  smallest additive change — extend the evaluate stage OR an additive `orchestration/wave_u.py`
  that composes A→B→C + reconcile. **Do NOT edit** `deep_pass.py` topology, `state.py`,
  `runner.py`, `wave_b.py`, or the frozen `wave_c.py`/`evaluate/stage.py` core logic beyond an
  additive call-out. If wiring needs a frozen-core edit ⇒ **STOP and escalate.**
- **Emission:** one `AcceptanceImpactAssessment` per drifted UAR; **CHR via the DTM-0013 model
  pattern** (`CognitionHistoryRecord(project_id=…, output_kind="acceptance_impact",
  provenance_ref={"emitted_by":"evaluate"}, upstream_lineage={uar_id, pinned_chr, latest_chr},
  recompute_trigger=…, supersedes_chr_id=<prior assessment for this UAR>, **spec)`) →
  `ctx.chr_repo.append` → emit `cognition_history_record_appended` + `acceptance_impact_assessed`.
  **No new output_kind, no migration** (`acceptance_impact` already in the CHECK).
- **Define `AcceptanceImpactAssessment`** in `shared/epistemic.py` (reserved in
  `CANONICAL_OUTPUTS`): Derived, `epistemic_state=derived`, `extra='forbid'`, carries the UAR
  ref, pinned vs latest value + delta, band-change flag. **Never canonical.**
- **Determinism:** the drift comparison is rule-derived (**exact**); any AI-derived input value
  it reads carries that value's own tier (band-stable). Recorded-fixture CI unchanged.

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/evaluate/acceptance_impact.py` (the compare) +
  the minimal additive wiring (extend the evaluate stage call OR `orchestration/wave_u.py`) ·
  `shared/epistemic.py` (ADD `AcceptanceImpactAssessment`) · `events.py` (ADD
  `acceptance_impact_assessed` to `EVENT_NAMES_WU_ACCEPT`) · `ci/gate_observability.py`
  (additive) + both gate-5 test files · `tests/{positive,negative}/acceptance/**` + an
  env-gated live e2e (accept → mutate knowledge → recompute → impact CHR).
- **READ-ONLY:** `deep_pass.py`, `state.py`, `runner.py`, `wave_b.py`, `wave_c.py`, the
  DTM-0016 acceptance path + UAR/plan-fact rows, `retain/**`, `infer/**`, ALL migrations,
  gate_invariants/allowlist.

## Packages / refactors

- None new. No migration. Additive reconcile + wiring only.

## Implementation instructions (TDD)

1. Red: `test_u2_*` (drift ≥10pts/band vs pin → one Acceptance-Impact Assessment, Derived, CHR
   appended; recompute supersedes a prior assessment; no-drift → none; below-threshold → none)
   + negatives (impact treated as canonical; assessment mutating the UAR/plan fact).
2. `AcceptanceImpactAssessment` type; `evaluate/acceptance_impact.py` compare; additive wiring
   after Evaluate scanning active UARs; CHR (model pattern) + events + gate-5 vocab + both test
   files; OBS audit (uar_id, pinned vs latest CHR lineage).

## API / data / schema contracts

- `AcceptanceImpactAssessment`: Derived, `epistemic_state=derived`, `uar_ref`, `pinned_chr`,
  `latest_chr`, `delta`/`band_changed`, `mode`/`confidence_stage`. CHR
  `output_kind=acceptance_impact`. **No schema change.**

## Test plan (QA-WU-ACCEPT)

- **Positive:** drift surfaces an assessment (Derived, CHR appended); recompute supersedes prior;
  no-drift / below-threshold → none; assessment references the UAR + pinned & latest CHRs.
- **Negative:** impact comparison treated as **canonical** *(Critical)*; the assessment mutating
  the UAR/plan fact *(Critical)*; an alert below the ≥10pts/band threshold *(Major)*.
- **Determinism:** comparison exact; band-stable on replay. AI offline.
- ruff + gate-4 + gate-5 green; live e2e (accept → mutate → recompute → impact) passes; baseline
  no regression.

## Manual checks (EM)

- Live: accept a recommendation; mutate the underlying knowledge; recompute → an
  `acceptance_impact` CHR appears for the accepted item, referencing pinned vs latest; the UAR +
  plan fact rows are byte-intact; no drift → no assessment.

## Done criteria

- U1.3 reconcile delivered; Acceptance-Impact surfaces at ≥10pts/band; Derived + CHR-appended +
  supersedes; impact-as-canonical and UAR-mutation negative-proven; no migration/package; PR
  cites `IC-WU-ACCEPT`. **Wave U candidate-complete → owner exit-gate before Phase VI.**

## Worker report

**Ready for review.**

### What was built (additive only; no frozen-core edit)

- **`shared/epistemic.py`** — defined `AcceptanceImpactAssessment` (Derived;
  `epistemic_state` PINNED to `derived`, `extra='forbid'`, frozen). Carries
  `uar_ref` + `pinned_chr` + `latest_chr` (read-only references, never the rows),
  `delta` (signed value move) + `band_changed`, plus `pinned_band`/`latest_band`
  audit fields. NO field marks canonical / world-truth / approval / governance
  (structurally unrepresentable). It was already reserved in `CANONICAL_OUTPUTS`.
- **`backend/responsibilities/evaluate/acceptance_impact.py`** (NEW) — the PURE
  compare `compare_acceptance_impact(pinned, latest)`: drift = `(|delta| ≥ 10)
  OR (band changed)` per Calibration §3. Reads the threshold from config
  (`ACCEPTANCE_IMPACT_DRIFT_POINTS`); no LLM, no network. Returns a `DriftResult`
  (exact, band-stable).
- **`backend/responsibilities/evaluate/config.py`** — added
  `ACCEPTANCE_IMPACT_DRIFT_POINTS = 10.0` citing Calibration §3 (the ≥10 dial was
  not previously a constant; the band-change half reuses the band already on each
  value). Owner-tunable dial, transcribed verbatim.
- **`backend/orchestration/wave_u.py`** (NEW — the wiring choice) —
  `reconcile_acceptance_impact(...)`: after a recompute, scans the project's
  active version-pinned UARs (`store.acceptances_for_project`, accept/direct_edit
  only); for each, reads the value at the pinned CHR + the latest CHR for the same
  accepted item; on drift appends ONE Derived `AcceptanceImpactAssessment` via the
  **DTM-0013 model pattern** (`CognitionHistoryRecord(output_kind="acceptance_impact",
  provenance_ref={"emitted_by":"evaluate"}, upstream_lineage={uar_id, pinned_chr,
  latest_chr}, recompute_trigger=…, supersedes_chr_id=<prior assessment for THIS
  uar>)`) → `chr_repo.append` → emits `cognition_history_record_appended` +
  `acceptance_impact_assessed`. Also `build_and_register_wave_u_chain(...)` which
  composes A→B→C by CALLING the frozen `build_and_register_wave_c_chain` (no new
  graph stage; reconcile runs post-Evaluate in the recompute, ADR-0009).
- **Additive READ seams** (SELECT only — append-only surface unchanged):
  `SupabaseRetentionStore.acceptances_for_project` and
  `ChrRepository.latest_acceptance_impact_for_uar` (the per-UAR supersede lookup).
- **`events.py` + `ci/gate_observability.py`** — added `acceptance_impact_assessed`
  to `EVENT_NAMES_WU_ACCEPT` (now the 3 IC/OBS-WU-ACCEPT C3 names, verbatim) and
  to `EXPECTED_EVENT_NAMES_WU_ACCEPT`. Both gate-5 test files updated for the new
  name (positive vocab assertion + negative `GOOD_EVENTS_PY` tuple + missing-tuple
  replace block) — no test left on the old 2-name union.
- **No migration, no new output_kind** (`acceptance_impact` already in the CHECK +
  `OutputKind` Literal). No new package. No new responsibility.

### Wiring choice + no frozen-core edit

Chose the **NEW `orchestration/wave_u.py`** option (mirrors `wave_c.py`): it CALLS
the frozen Wave C builder for A→B→C and adds the reconcile as a separate
post-recompute call. **No frozen-core file was edited** — `deep_pass.py`,
`state.py`, `runner.py`, `wave_b.py`, `wave_c.py`, the frozen `evaluate/stage.py`
core, `retain/**` + the DTM-0016 acceptance path, and all migrations are
untouched. The reconcile is read-only over the UAR and the plan fact.

### Derived-not-canonical + supersede-on-recompute — how proven

- **Derived, never canonical:** `epistemic_state` is a pinned `Literal[DERIVED]`;
  negatives prove every `attested-*` value is rejected by Pydantic and that no
  truth/approval/governance field is representable (`extra='forbid'`); `is_canonical`
  is `False`. The appended CHR is the OSLO-self-attested receipt (`attested-oslo`),
  the assessment payload it carries stays Derived.
- **Read-only over UAR + plan fact (Critical):** negatives snapshot the UAR rows +
  the pinned/latest value CHRs before/after a drifting reconcile and assert byte-
  equality; every appended CHR is asserted to be `acceptance_impact` (never a
  value rewrite). The live e2e re-reads the UAR + plan-fact rows and asserts
  `== before`.
- **Supersede-on-recompute:** a second reconcile after a further move appends a
  second `acceptance_impact` CHR carrying `supersedes_chr_id` = the prior
  assessment's id (resolved via `latest_acceptance_impact_for_uar`), and the prior
  CHR is asserted byte-intact (append-only).
- **Below-threshold raises nothing (Major):** −8 pts / same band → `is_drift=False`,
  no assessment, no event.

### U2 / U3 → test map

| Contract item | Test |
|---|---|
| U2 pos — drift ≥10pts/band → ONE Derived assessment, CHR appended, events | `tests/positive/acceptance/test_u2_reconcile.py::test_drift_raises_one_derived_assessment_with_chr_and_events` |
| U2 pos — references uar + pinned & latest CHRs | same test (asserts `uar_ref`/`pinned_chr`/`latest_chr` + `upstream_lineage`) |
| U2 pos — recompute supersedes prior for same UAR | `…::test_recompute_supersedes_prior_assessment_for_same_uar` |
| U2 pos — no-drift / below-threshold → none | `…::test_no_drift_below_threshold_raises_nothing` |
| U2 pos — only accept/direct_edit reconciled | `…::test_only_accept_and_direct_edit_uars_are_reconciled`, `…::test_direct_edit_uar_is_reconciled` |
| Drift rule (≥10 / band / exact) | `tests/positive/acceptance/test_u2_acceptance_impact_compare.py` (6 cases) |
| U2 neg — impact treated as canonical (Critical) | `tests/negative/acceptance/test_u2_acceptance_impact_negative.py::test_assessment_cannot_be_attested_canonical`, `…::test_assessment_carries_no_truth_or_governance_field`, `…::test_assessment_is_listed_as_derived_in_canonical_outputs_vocab` |
| U2 neg — assessment mutating the UAR/plan fact (Critical) | `…::test_reconcile_never_mutates_the_uar_rows`, `…::test_reconcile_never_mutates_the_pinned_or_latest_value_chrs` |
| U2 neg — alert below ≥10/band threshold (Major) | `…::test_below_threshold_raises_no_assessment_major` |
| U3 — `acceptance_impact_assessed` event verbatim + pairing | gate-5 (`ci.gate_observability`), `tests/positive/observability/test_gate_observability.py::test_wu_accept_vocabulary_is_the_three_ic_wu_accept_c3_names_verbatim`, negative gate-5 tamper tests |
| U3 — live e2e (accept → mutate → recompute → impact; UAR/plan fact intact) | `tests/positive/acceptance/test_u2_live_reconcile_e2e.py` (env-gated) |

### Exact commands + results

OFFLINE:
```
env -u SUPABASE_URL -u SUPABASE_SERVICE_ROLE_KEY -u SUPABASE_DB_URL -u OSLO_LLM_LIVE \
  .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q
→ 568 passed, 71 skipped   (baseline 551 passed / 70 skipped — +17 acceptance tests, +1 skipped live e2e; no regression)
```
LIVE:
```
set -a; source .env; set +a; unset OSLO_LLM_LIVE; \
  .venv/bin/python -m pytest tests/positive tests/negative tests/replay -q
→ 639 passed   (baseline live 621 — +18; the acceptance-impact live e2e passes)
```
Gates:
```
.venv/bin/ruff check .                       → All checks passed!
.venv/bin/python -m ci.gate_invariants       → [gate-4 epistemic-invariant] PASS
.venv/bin/python -m ci.gate_observability    → [gate-5 observability] PASS
```

### Flags / notes (no STOP)

- The CHR model rejects `recompute_trigger=None`; the reconcile runs inside a
  recompute, so its default is `"reanalysis"` (a valid LDM §2.2 trigger).
- Three pre-existing append-only **surface-introspection negatives** locked the
  exact public method set of `ChrRepository` / `SupabaseRetentionStore`. The two
  new methods are **SELECT-only READS** (no update/delete/upsert), so I added them
  to the locked allowed-sets and kept the in-memory fake in lockstep — append-only
  is preserved (the `_MUTATION_NAMES` checks still pass). No gate_invariants /
  allowlist edit; no migration.
- No frozen-core edit was required; no spec gap was inferred.

## Engineering-manager review notes

**Review (2026-06-18).** Single worker, no STOP, additive. EM independently verified:

- **Scope correct:** new `evaluate/acceptance_impact.py` (pure compare) + `orchestration/wave_u.py`
  (reconcile + A→B→C composition by *calling* the frozen Wave C builder); `evaluate/config.py`
  (`ACCEPTANCE_IMPACT_DRIFT_POINTS=10.0`, Calibration §3); `shared/epistemic.py`
  (`AcceptanceImpactAssessment`); 2 **SELECT-only** read methods on `retention_store.py` /
  `retain/repository.py`; `events.py` + gate-5 (both test files); new `acceptance/` test dirs +
  3 surface-introspection negatives updated. **Frozen-core untouched** (empty diff):
  `graphs/deep_pass.py`, `state.py`, `runner.py`, `wave_b.py`, `wave_c.py`, `evaluate/stage.py`
  core, `retain/acceptance.py` (DTM-0016), migrations, `gate_invariants`. **No migration, no new
  output_kind, no package.**
- **Read-only over the canonical rows (verified):** the 2 new methods are `.select().eq()` only
  (no insert/update/delete/upsert); the append-only **mutation guard still holds** (the
  surface-introspection negatives pass — only reads were added to the locked allowed-set, no
  mutation surface). Negatives prove the reconcile never mutates the UAR or the pinned/latest CHRs.
- **Derived-not-canonical (proven):** `epistemic_state` pinned `derived` (attested-* rejected),
  `extra='forbid'` (no truth/governance/approval field), listed Derived in CANONICAL_OUTPUTS.
- **Drift semantics:** ≥10 pts (from config) **or** band change (Calibration §3); below-threshold
  raises nothing; one assessment per drifted UAR; recompute **supersedes** the prior (prior CHR
  intact). Comparison rule-derived (exact / band-stable). No LLM.

**EM-run verification (independent, 2026-06-18):**
- OFFLINE → **568 passed, 71 skipped, 0 failed** (DTM-0016 baseline 551 → +17). LIVE (Supabase up)
  → **639 passed, 0 failed** (baseline 621 → +18); the accept→mutate→recompute→impact e2e passes.
  acceptance suites: 18 passed. ruff clean · gate-4 PASS · gate-5 PASS.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0017 delivers IC-WU-ACCEPT U1.3: when the value behind a user-accepted item drifts ≥10 pts
  or a band change vs the version-pinned acceptance (Calibration §3), Evaluate emits a Derived
  `AcceptanceImpactAssessment` (CHR `acceptance_impact`, superseding the prior for that UAR) +
  `acceptance_impact_assessed`. Wired additively via `orchestration/wave_u.py` (calls the frozen
  Wave C builder; reconcile is a post-recompute scan of active version-pinned UARs) — no
  frozen-core edit, no migration. The assessment is Derived and never mutates the UAR/plan fact
  (negative-proven). **Wave U complete.**

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · OFFLINE 568/71/0 · LIVE 639/0 (impact e2e green).
  Scope-checked: frozen-core untouched; reads SELECT-only; mutation guard intact.

Manual test plan:
- Live (Supabase up): accept a recommendation; mutate the underlying knowledge; recompute → an
  `acceptance_impact` CHR appears for the accepted item (referencing pinned vs latest); the UAR +
  plan fact rows are byte-intact; no-drift / below-threshold → no assessment.

Remaining risks:
- Disclose surfacing of the alert is Wave E (Phase VI) — Wave U emits the event only.
- Branch still carries the inherited gate-3 fix gap until synced with main.

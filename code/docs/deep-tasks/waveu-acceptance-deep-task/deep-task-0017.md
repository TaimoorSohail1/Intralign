# DTM-0017 — Acceptance-Impact Assessment: reconcile-on-drift (Derived), via the 00R recompute

**Status:** Planned — BLOCKED on DTM-0016 approval · **Module:** DTM-0017 · **Phase:** V (Wave U)
· **Contract:** **IC/QA/OBS-WU-ACCEPT** (U1.3) + **Calibration §3** · **Depends:** DTM-0016
(UAR + plan fact), Wave B (the values that drift), the 00R recompute backbone.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

# DTM-0010 — Finding (Infer): gap/conflict/risk derivation, evidence-anchored, Fast/Deep

**Status:** Planned — BLOCKED on DTM-0009 approval · **Module:** DTM-0010 · **Phase:** III
(Wave B) · **Contract:** **IC/QA/OBS-WB-INFER** (+ DL-046) · **Depends:** DTM-0009 (LLM seam,
fixture harness, synthesized model).

## Goal / observable behavior

Infer derives **Findings** (types: **Gap, Conflict, Risk Signal**) from Attested knowledge
(Retain) + the synthesized model + the declared-outcome reference, **each anchored to the
Attested evidence it derives from**. Each emission emits `finding_detected` and **appends a
CHR** (via `ctx.chr_repo`); recompute re-derives and **supersedes** prior Findings (history
appended, prior CHR intact). Conflicts are **surfaced, not resolved**. Runs under both modes:
**Fast Pass** orientation-sufficient Findings; **Deep Pass** expanded/matured; `mode` +
`confidence_stage` (Orientation→Expanded→Validated) on each emission + CHR.

## Source docs / constraints

- `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING.md` §1 (IC-WB-INFER 1.1 required/forbidden/states/
  invariants; QA 1.2 positive/negative/classification; OBS 1.3 events/audit/replay/drift) +
  §0/§0.1 shared invariants & modes.
- `WAVE_B_CONTRACT_AMENDMENT_FAST_DEEP_60S_DISPOSITION.md` B (Infer required-behavior #5), D
  (positives/negatives), E (OBS mode/stage + Time-to-First-MRI latency).
- ADR-0004 (fixtures), decisions #2–#6, #9–#11. Calibration §1 tiers, §4c routing/budget.

## Locked decisions

- **Producer boundary:** Infer is the **single producer of Findings**. It **must not**
  compute severity/confidence (Evaluate), generate recommendations/clarifications (Advise),
  write canonical / promote a Finding to Attested, govern exposure, or resolve a conflict into
  canonical truth. Reuses the DTM-0009 `llm_provider` + recorded-fixture harness.
- **Replace the `infer` placeholder** via `register_stage("infer", …)` — `deep_pass.py`
  topology unchanged. Findings append their CHRs through `ctx.chr_repo` (decisions #4); emit
  via `ctx.emitter`.
- **Evidence anchor mandatory:** every Finding traces to the `AttestedAssertion`(s) it derives
  from (Major failure if missing).
- **Persistence default:** generic `derived` projection + CHR (`output_kind=finding`). No new
  migration (typed-table need ⇒ STOP/escalate).
- **Modes:** Fast Pass produces orientation Findings without blocking; Deep Pass (the 00R
  async engine) expands; `confidence_stage` changes **only via recompute**; `mode`/stage are
  attributes, never new objects.
- Determinism: rule-structural gaps **exact**; AI-derived Findings **semantic**; set-level
  ≥90% stable identities across recompute.

## Owned files / boundaries

- **OWN (additive):** `backend/responsibilities/infer/**` (Finding engines: gap [alignment/
  coverage/quality/SMART], conflict, risk — additive to DTM-0009's synthesis modules) ·
  `events.py` (ADD `EVENT_NAMES_WB_INFER`, extend union) · `ci/gate_observability.py`
  (additive) · `shared/` (ADD `Finding` type if not already) · `tests/{positive,negative}/
  infer_finding/**`, `tests/replay/**`, additive recorded fixtures.
- **READ-ONLY:** `orchestration/**` (register_stage + StageContext only) · `retain/**`,
  `perceive/**`, `adapt/**`, DTM-0009 synthesis modules (consume the model; do not edit) ·
  ALL migrations · Wave A/S event tuples (extend only).

## Packages / refactors

- None new. No refactors (placeholder replaced via registry).

## Implementation instructions (TDD)

1. Red: `test_b2_*` (Findings typed + anchored + CHR + supersession + both modes + stage
   transitions) and `test_b3_*` (every forbidden behavior) first.
2. Gap/Conflict/Risk engines reading Attested knowledge + synthesized model; anchor each
   Finding; classify type; flag conflicts (surfaced).
3. Inject as the `infer` stage; CHR per Finding via `ctx.chr_repo`; emit `finding_detected`/
   `finding_superseded`; events + gate-5 vocab.
4. Fast/Deep: orientation-sufficient set on Fast; Deep expansion via 00R recompute; carry
   `mode`+`confidence_stage`; emit Fast-Pass Time-to-First-MRI latency.
5. OBS audit (assertions a Finding derived from, model/rule version, recompute lineage) +
   replay (record-exact emission; semantic derivation, exact for rule-structural gaps).
6. Integration: recompute (00R) re-derives + supersedes; prior Finding CHR intact; two
   emissions show surfaced drift; Deep Pass does not block the user.

## API / data / schema contracts

- `Finding`: Derived, `epistemic_state=derived`, `finding_type ∈ {gap, conflict, risk}`,
  `evidence_anchors=[assertion ids]`, `mode`, `confidence_stage`. CHR per emission
  (`output_kind=finding`). No schema change.

## Test plan (QA-WB-INFER)

- **Positive (`test_b2_*`):** Findings derived + Gap/Conflict/Risk typed + evidence-anchored;
  emission appends CHR; recompute supersedes (prior intact); both modes; stage
  Orientation→Expanded→Validated observable.
- **Negative (`test_b3_*`):** Infer computing severity/confidence; generating recs/
  clarifications; writing canonical / promoting to Attested *(Critical)*; resolving a conflict
  into canonical truth; Finding changed **without recompute** / CHR overwritten *(Critical)*;
  Deep Pass blocking the user; `confidence_stage` regressing or changing without recompute;
  `mode`/stage modeled as a new object *(Critical)*; missing evidence anchor *(Major)*.
- **Determinism:** rule-structural exact; AI semantic; ≥90% set overlap.
- AI offline via recorded fixtures (no provider call in PR CI).
- Full suite + ruff + gate-4 + gate-5 green; baseline must not regress.

## Manual checks (EM)

- AST/grep: `infer/` exports no severity/confidence/recommendation producer; only Finding.
- Studio: Finding rows are Derived + anchored; recompute leaves prior Finding CHR byte-intact.

## Done criteria

- WB-INFER B2/B3 traceability in report; conflicts surfaced-not-resolved proven; Fast/Deep +
  stage maturation demonstrated; PR cites `IC-WB-INFER`; no migration/package. Ready for
  DTM-0011.

## Worker report

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

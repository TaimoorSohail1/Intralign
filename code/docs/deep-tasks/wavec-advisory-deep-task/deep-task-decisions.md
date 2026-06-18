# Deep-task decisions — Wave C: Advisory (Advise)

Implementation-control record for Phase IV / Wave C. Cites source-of-truth; does not restate it.
Two slices (DTM-0014, DTM-0015). **Branch:** `feat/phase4-wavec-advisory` (do NOT create another).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **Contract:** `20_handoff/contracts/WAVE_C_AND_U_CONTRACT_PACKAGES_ADVISORY_AND_ACCEPTANCE.md`
  — **Wave C section** C0–C3 (IC/QA/OBS-WC-ADVISE) + the DL-047 Additions block (REC-04
  SuggestedFix, REC-05 Validation). The contract WINS over any summary.
- **Plan:** `30_engineering/implementation/Phase_IV_Wave_C_Advisory/IMPLEMENTATION_PLAN.md`
  (Goal, Scope, DoD, Invariants, Exit gate, DL-047 additions L56–58).
- **ADR-0008** (`code/docs/adr/0008-wave-c-advisory-build-plan.md`) — the locked build plan +
  the 18 locked decisions behind it; **CONTEXT.md** Wave C glossary (Recommendation,
  Clarification, SuggestedFix, Validation, Resolution-Path-presentation-only, DL-055 state).
- **DL-055** (decision_log.md) — Recommendation state model (Generated→{Accept/Reject/Defer}→
  Implemented +Superseded; user-owned; Modify→supersession; Discuss/Share = affordances).
- **DL-043** (Derived/recompute/no-Authority), **DL-046** (mode/confidence_stage), **DL-048**
  (ai_spend_recorded; SuggestedFix daily cap = commodity MON). Arch spec §4/§6/§10 (Advise);
  LDM §2.2/§3.1; State Model §11; ADR-0004 (recorded-fixture CI); ANTI_ASSUMPTION protocol.

## Repo facts (current code — the seams Wave C extends)

- `responsibilities/advise/__init__.py` — **stub** (docstring only): *"Advise — advisory. Sole
  producer of Recommendation. OSLO never autonomously applies a SuggestedFix; the user applies it."*
- Orchestration: `stages.py` — `CHAIN_STAGE_ORDER = (retain, infer, evaluate, advise)`;
  `wave_c_placeholder_advise` (no-op); `register_stage("advise", …)`. `graphs/deep_pass.py`
  already has a `stage_advise` node + routing → **NO topology change**. `wave_b.py` is the
  composition reference (`build_and_register_wave_b_chain`, per-run `_RunHandoff` closure keyed
  by `run_id`, `register_stage("infer"/"evaluate")`).
- CHR: `retain/models.py` `OutputKind` already includes **`recommendation`** + **`clarification`**
  (14-value Literal/CHECK) → **NO migration**. `ChrRepository.append(record)` needs a
  `CognitionHistoryRecord` **model** (DTM-0013 contract).
- Types: `shared/epistemic.py` lists `Recommendation`, `ClarificationRequest`, `SuggestedFix` in
  `CANONICAL_OUTPUTS` but **they are not yet classes** (Finding/Issue/Confidence/CAF/etc. are).
- Events: `events.py` per-contract tuples (WA00R/WA001/WA002/WS/WB_INFER/WB_EVAL/COST) + union;
  gate-5 (`ci/gate_observability.py`) asserts vocab verbatim + tamper. `CollectingEventEmitter`
  rejects unknown names.
- LLM: `config.py` `RoutingStage = Literal["extraction","synthesis","generation"]` — **no
  `advise` stage yet**; `TierRouting` has extraction/synthesis/generation/fallback. Internal
  Gemma is primary (DL-069). Recorded-fixture harness: `tests/_fixtures/recorded_model_responses/`.

## Locked decisions (apply to both slices unless noted)

1. **One fresh worker per slice, sequential** (ADR-0008): DTM-0014 → DTM-0015. No slice starts
   until the prior is reviewed/fixed/verified/approved.
2. **Inject behind the frozen seam:** replace `wave_c_placeholder_advise` via
   `register_stage("advise", …)`. Add an **additive `orchestration/wave_c.py`** that composes
   the full A→B→C chain by *calling* the Wave B chain builder + adding the advise stage — do
   **NOT** edit the frozen `wave_b.py`, `deep_pass.py` topology, `state.py`, `runner.py`,
   `registry.py`. (Mirror the Wave B `_RunHandoff` closure to pass Findings/Issues to advise.)
3. **CHR-append = DTM-0013 model contract:** construct
   `CognitionHistoryRecord(project_id=…, provenance_ref={"emitted_by":"advise"},
   recompute_trigger=…, supersedes_chr_id=…, **spec)` and `ctx.chr_repo.append(record)`, then
   emit `cognition_history_record_appended` (gate-5 pairing). **Never a dict.** `output_kind ∈
   {recommendation, clarification}` (already in CHECK) → **NO migration**.
4. **Anchoring (hard):** every Recommendation/SuggestedFix anchors to a Finding/Issue
   (Recommendation-only-in-Finding-context). Standalone = rejected (Major).
5. **Advise generates; the user disposes (DL-055):** emit Recommendations in the **`Generated`**
   state only. **Do NOT implement Accept/Defer/Reject/Apply** (those are user actions recorded
   by **Wave U**, a later phase). "Modify"→supersession (recompute); Discuss/Share = affordances.
6. **Forbidden negatives (C1/C2):** no evaluate/score; no canonical write / promote-to-Attested;
   no govern/authorize/execute; **no self-accept**; no change outside recompute; **no standalone
   Resolution-Path object** (presentation-only); **no autonomous SuggestedFix write (Critical,
   DTM-0015)**.
7. **Derived + recompute:** all output `epistemic_state=derived`; recompute re-derives +
   supersedes (prior CHR intact). Carry `mode` + `confidence_stage` attributes (DL-046).
8. **Determinism:** AI-text → **semantic** (recommendations never exact-replay); record-exact
   emission; set-level ≥90% stable identities across recompute.
9. **LLM:** Advise uses the model (recommendations are AI-text) → add **`"advise"`** to
   `RoutingStage` + an `advise` ref in `TierRouting` (internal Gemma primary, DL-069). Reuse the
   `LLMProvider` seam + recorded-fixture harness — **zero provider calls in PR CI** (ADR-0004).
   Emit `ai_spend_recorded` for advise spend (DL-048).
10. **Types:** define `Recommendation`, `ClarificationRequest` (DTM-0014) and `SuggestedFix`
    (DTM-0015) classes in `shared/epistemic.py` (reserved in `CANONICAL_OUTPUTS`), Derived,
    `extra='forbid'`, with the Finding/Issue anchor field + recommendation `type`.
11. **Events (additive + gate-5 + both test files):** `EVENT_NAMES_WC_ADVISE =
    (recommendation_generated, clarification_requested)` (DTM-0014, verbatim per OBS-WC C3) +
    `EVENT_NAMES_WC_FIX = (suggested_fix_offered,)` (DTM-0015, per DL-047 OBS). `cognition_
    history_record_appended` reused. Update both gate-5 test files (do **not** repeat the
    DTM-0009 regression).
12. **No new package; no new migration** (the only canonical kinds are already present). If a
    *new* output_kind is thought necessary ⇒ **STOP and escalate**.

## Packages / refactors

- **No new package** (`pydantic-ai` already declared). No refactor of frozen modules — advise
  injected via `register_stage`; `wave_c.py` is additive; `wave_b.py`/`deep_pass.py` read-only.

## Open items

- **GATE — Wave C coding is BLOCKED on:** (a) the **Wave B owner exit-gate** (PR #39 merge /
  DL-044 per-wave sign-off), and (b) per-wave authorization + readiness gate. **These task files
  are planning only; no worker is spawned until the owner authorizes Wave C start.**
- **Residual (minor, scaffold-safe):** exact OBS-WC event snake_case — worker pins verbatim vs
  OBS-WC C3 / the DL-047 OBS line. SuggestedFix/Validation persist on the existing
  `recommendation` kind + a payload `type` discriminator (no new kind); a *new* kind ⇒ STOP.

## Slice index

| Task | Scope | File |
|---|---|---|
| DTM-0014 | IC/QA/OBS-WC-ADVISE core — Recommendation + Clarification, advise stage, wave_c.py | `deep-task-0014.md` |
| DTM-0015 | DL-047 — SuggestedFix (REC-04) + Validation Recommendation (REC-05) | `deep-task-0015.md` |

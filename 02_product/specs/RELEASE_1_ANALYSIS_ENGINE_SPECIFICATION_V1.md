# Release 1 Analysis Engine Specification v1

**Type:** Core Analysis Engine Specification (execution mechanics)
**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Revision:** 2026-05-31 — §9 Fast Analysis Pipeline refined to the full 9-stage (0–8) flow incl. the Global Skeleton stage; aligned to `FAST_DEEP_WORKFLOW_PACK/FAST_PASS_STAGE_IO_SPEC.md`. Proposal/TBD items unchanged in canonical status (owner ratification pending; see `FAST_DEEP_WORKFLOW_PACK/OPEN_DECISIONS.md`).
**Implements (does not redefine):** `PLANNING_INTELLIGENCE_SPECIFICATION_V1.md` *(authority)* · CAF Assessment Model · Finding Model · Recommendation Model · Confidence Model · Reliability Model
**Authoritative inputs:** Planning Intelligence Spec · `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` · `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1.md` · `RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` · `RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` · `RELEASE_1_TESTING_STRATEGY_V1.md`

> **Scope guardrails.** Active Release 1 only. **No Governance, Execution Intelligence, Agent Governance, or Future Architecture.** This document defines **execution mechanics** — *how* the engine runs the reasoning. It **does not redefine reasoning; it implements it.** **Where any conflict arises, the Planning Intelligence Specification wins.** Consistent with the founder CAF decisions and Planning Intelligence, the engine introduces **no scoring formulas, weights, percentages, or numeric thresholds**, and **no new entities, states, or events.** The only approved numeric target is the **60-second Time-to-First-MRI**; all other quantitative values are **`TBD – Owner Decision Required`.**

---

## 1. Purpose

The **Analysis Engine** is the runtime that executes Planning Intelligence. It turns project inputs into the Release 1 outputs — **findings, recommendations, CAF states, confidence states** — by running the Fast and Deep analysis passes as concrete, ordered, observable, recoverable processes. Within Release 1 it is the *doing* of the reasoning the Planning Intelligence Spec *describes*: same inputs, same output types, same descriptive/advisory discipline — now with pipelines, determinism, replay, event/state integration, and failure handling.

---

## 2. Architectural Position

```text
Intent
  → Context Plane        (extracts evidence → context items)
    → Knowledge Layer    (canonical storage, versioning, relationship graph)
      → Planning Intelligence   (the reasoning framework — authority)
        → ANALYSIS ENGINE        (executes that reasoning, per-run)
          → Findings · Recommendations · CAF States · Confidence States
```

The engine sits **below** Planning Intelligence (it obeys it) and **above** the persisted outputs (it produces them). It reads from the Context Plane / Knowledge Layer, executes a run, and writes results the API/UI then expose. It never reaches around Planning Intelligence to invent reasoning, nor around the Data/State/Event models to invent storage or signals.

---

## 3. Analysis Engine Responsibilities

The engine **owns**:

- **Analysis execution** — running Fast and Deep passes as `AnalysisRun`s (queued→running→completed).
- **Finding generation** — producing the 7-type descriptive findings from understanding.
- **Recommendation generation** — producing the 3-type advisory recommendations from findings.
- **Confidence generation** — producing CAF states and the reliability-qualified Outcome Confidence summary.
- **Confidence recalculation** — producing superseding confidence on later runs.
- **Expanded understanding generation** — deep-pass expansion of findings/recommendations and contradiction discovery.
- **Result publication** — persisting outputs and emitting the defined events that drive state transitions.

---

## 4. Analysis Engine Non-Responsibilities

The engine explicitly **does not**:

- **Govern** — no acceptance, disposition, review, or accepted-understanding (governance is future; out of scope).
- **Execute** — no autonomous action; no execution intelligence; no agent behavior.
- **Make user decisions** — accept/reject/implement are user acts; the engine only proposes.
- **Deliver notifications** — it emits source events; the notification service surfaces awareness.
- **Produce reports** — reporting consumes engine outputs; the engine doesn't render reports.
- **Run collaboration** — comments/mentions/shares are separate; the engine doesn't manage them.

The engine reasons and publishes; everything prescriptive, governing, or delivering is someone else's job.

---

## 5. Core Engine Inputs

| Input | Source | Use |
|---|---|---|
| Project intent | Project | the frame for alignment/coverage |
| Artifacts / ArtifactVersions | Knowledge Layer | the structured plan under assessment |
| Evidence | Context Plane | ground truth; basis for explainability |
| Context items (fast & deep horizon) | Context Plane | claims/assumptions/relationships working set |
| Prior findings / recommendations | persisted state | what to re-evaluate, expand, or supersede |
| Prior analysis runs (`previous_run_id`) | persisted state | baseline understanding to refine |
| User actions (acknowledge/implement/etc.) | persisted state | legitimate change signals for the next run |

The engine consumes only these; it asserts nothing beyond what they support (unsupported → a finding, not a conclusion).

---

## 6. Core Engine Outputs

| Output | Entity (Data Model v1.1) | Notes |
|---|---|---|
| Analysis run record | `AnalysisRun` | the execution itself; `run_type`, `run_status` |
| CAF assessment | `CAFState` (1:1 per run) | Clarity/Alignment/Feasibility + per-dimension reliability |
| Outcome confidence | `ConfidenceState` (1:1 per run) | reliability-qualified summary; supersession chain |
| Findings | `Finding` | 7-type, descriptive; `first_seen_run_id` |
| Recommendations | `Recommendation` | 3-type, advisory; tied to findings |
| MRI snapshot | `MRISnapshot` (derived) | visualization of understanding |

All outputs use existing entities/enums verbatim — **no new entities or fields.**

---

## 7. Fast Analysis Architecture

- **Purpose:** produce the 60-Second Orientation — a trustworthy *first* understanding, fast.
- **Objectives:** speed within the 60s budget; initial CAF + confidence; initial findings/recommendations; communicate reduced reliability where depth was traded.
- **Processing scope:** fast-horizon extraction; shallow relationship discovery; surface ambiguity/assumption/coverage detection. **Bounded work** — it deliberately defers depth to the Deep Pass.
- **Outputs:** one completed `AnalysisRun(fast_analysis_pass)` → CAFState, initial ConfidenceState, initial Findings (`detected`), initial Recommendations (`generated`), MRISnapshot.
- **Expected behavior:** runs once per project on first analyzable input; optimized for latency; never presented as final.

---

## 8. Deep Analysis Architecture

- **Purpose:** improve understanding through deeper reasoning. **Performs no governance.**
- **Objectives:** enrich context, expand assumptions/relationships, discover contradictions, reassess CAF, recalculate confidence, expand findings/recommendations.
- **Expansion scope:** deep-horizon extraction; fuller relationship web; deeper assumption/claim discovery; contradiction discovery the fast pass can't reach.
- **Outputs:** one completed `AnalysisRun(deep_analysis_pass)` → recalculated ConfidenceState (supersedes prior), new CAFState, Expanded Findings (`first_seen_run_id`=this run), Expanded Recommendations.
- **Expected behavior:** event-triggered and **coalesced** (single active deep run per project; rapid triggers merged); recurs as evidence/action accumulate; each run supersedes prior assessment while preserving history.

---

## 9. Fast Analysis Pipeline

> **Revision note (2026-05-31).** This section is refined into the full **9-stage (0–8)** Fast flow. Stages map 1:1 to `FAST_DEEP_WORKFLOW_PACK/FAST_PASS_STAGE_IO_SPEC.md`, which carries the per-stage I/O, entry/exit criteria, events, and validation. Items marked **〔proposal〕** or **`TBD – Owner Decision Required`** are not yet owner-ratified and do not change any canonical value; the only canonical numeric target remains the **< 60s** Time-to-First-MRI.

Ordered execution stages (mechanics; reasoning per Planning Intelligence). Execution type: `rule` (deterministic) · `llm` · `hybrid` (see `RULE_LLM_GUIDELINES.md`).

| # | Stage | Exec | What happens |
|---|---|---|---|
| 0 | **Intake & Acquisition** | rule | Gather intent, artifacts/versions, evidence; validate against the ingestion envelope 〔proposal: ~20k-token design point / ~33k ceiling — `TBD`〕; oversized input accepted but routed Deep-only 〔proposal〕. Run enqueued; Project `created → orienting`; emit `fast_analysis_requested`. |
| 1 | **Normalization** | rule | Canonicalize inputs into the working representation; segment + tag source spans (span fidelity mandatory for explainability). |
| 2 | **Global Skeleton** 〔proposal〕 | hybrid | Over the whole corpus (≤ envelope ⇒ single model context, no capacity chunking), build a compact, output-light global map: restated intent + entity index + relationship skeleton + cross-references. This map is carried into every later isolated/parallel evaluation so Alignment/Feasibility stay globally informed and chunk boundaries don't become determinism hazards. Fallback: skeleton failure ⇒ degrade to isolation-only with **reduced reliability** (Coverage ↓), not run failure. |
| 3 | **Claim Extraction** | hybrid | Extract the **bounded salient** claim subset (not exhaustive — fast horizon). Rule pre-filter (assertion patterns) bounds LLM load; LLM identifies claims incl. implicit; `canonical_key` for dedup/determinism 〔proposal〕. Target ≈ **50–100 claims** 〔proposal — `TBD`〕. Parallel chunks each carry the Stage-2 map. |
| 4 | **CAF Evaluation** | hybrid | Assess Clarity/Alignment/Feasibility (Planning Intelligence §9–§11). **Clarity** is fully evaluable and largely rule-detectable (vagueness lexicon, missing-units, unsupported-assertion graph check, coverage-gap set-difference vs the 8 artifact types). **Alignment/Feasibility** get a *preliminary* read off the global map, **marked lower-reliability** (Reliability Model). Produces one `CAFState`. **No formula/weight/threshold.** |
| 5 | **Finding Generation** | hybrid | Emit initial 7-type **descriptive** findings (`status=detected`) with basis links (§11). Detection may be rule (Stage 4); object emission is rule. |
| 6 | **Recommendation Generation** | hybrid | Emit initial 3-type **advisory** recommendations (`status=generated`) from findings (§12). Finding-type→recommendation-type selection is a near-deterministic mapping 〔proposal〕; rationale is LLM. |
| 7 | **Confidence & State** | rule | Produce CAFState's reliability-qualified `ConfidenceState` summary (§13). Confidence **derived from CAF + Reliability only**, never bare. Synthesis method is formula-free (`TBD`). |
| 8 | **MRI & Publication** | rule | Build `MRISnapshot`; **atomic** all-or-nothing persist (§20); mark run `completed`; Project `orienting → oriented`; emit `fast_analysis_completed` → ordered fan-out `confidence_created → finding_created → recommendation_created → notification_created` (§17). Orientation surfaced as **"not final — Deep Analysis to follow."** |

**Horizon discipline.** Stages 2–4 deliberately do *less* than Deep: a bounded claim set and preliminary relational assessment. This is what protects the **< 60s** budget (§19) while keeping the orientation honest (lower reliability on Alignment/Feasibility). The deferred depth is Deep's job (§10).

**Budget (proposal — load-test pending; only < 60s is canonical):** the LLM-bound stages (2, 3, and the relational half of 4) dominate the budget; stages 0, 1, 5, 8 and the mechanics of 7 are deterministic and cheap. Per-stage budgets and the claim bound are owner-calibration (`OPEN_DECISIONS.md`).

---

## 10. Deep Analysis Pipeline

Ordered execution stages:

1. **Context Expansion** — deep-horizon extraction; enrich context items.
2. **Relationship Expansion** — extend the relationship web among claims/entities/artifacts.
3. **Assumption Expansion** — surface more/deeper assumptions.
4. **Conflict Discovery** — detect contradictions revealed by the enriched web.
5. **Additional Claim Discovery** — surface claims the fast pass missed.
6. **CAF Reassessment** — re-evaluate Clarity/Alignment/Feasibility on the enriched understanding.
7. **Confidence Recalculation** — produce a new ConfidenceState superseding prior (§14).
8. **Expanded Findings** — new/deepened findings (`first_seen_run_id`=this run).
9. **Expanded Recommendations** — recommendations for the new/updated findings.
10. **Publication** — persist; supersede prior assessment (history preserved); mark `completed`; emit events.

Stages 1–5 build the deeper understanding; 6–9 assess and express it; 10 publishes.

---

## 11. Finding Generation Mechanics

Findings **emerge** from evaluating understanding against the 7 conditions (Planning Intelligence §6). Mechanically, each evaluation stage inspects the working understanding and **emits a Finding** when a condition holds, attaching: type, affected dimension(s), severity (qualitative — critical/moderate/warning, owner-calibrated), and **basis links** (evidence/context). Relationships:

- **Ambiguity** → multiple readings of a claim/term → affects **Clarity**.
- **Assumption** → claim with no supporting evidence link → affects the dimension it underpins.
- **Conflict** → incompatible claims / drift from intent → affects **Alignment**.
- **Constraint / Coverage Gap** → limiting condition / unaddressed area → affects **Feasibility**.
- **Missing Information / Inference** → absent input / over-reach beyond evidence → affects the relevant dimension.

**No scoring formulas** — emission is condition-driven and basis-linked, not threshold-arithmetic. Findings are **descriptive** outputs only.

---

## 12. Recommendation Generation Mechanics

For each finding, the engine generates an advisory recommendation aimed at improving the affected dimension. **Type selection** follows the finding's nature (Planning Intelligence §7):

- Unsupported assumption / uncertain inference → **Validation** (confirm/source it).
- Resolvable weakness with a clear corrective action → **Suggested Fix**.
- General strengthening of plan/understanding → **Improvement**.

Each recommendation carries a rationale (basis) and the expected dimension. **No governance** — the engine proposes; it never accepts, applies, or decides. Recommendations are emitted `generated`; the user drives them onward.

---

## 13. Confidence Generation Mechanics

The engine produces confidence **from understanding, never as a primary input**:

1. assess each CAF dimension on the current understanding → `CAFState` (with per-dimension reliability),
2. qualify each dimension's reliability (supportability, per Reliability Model),
3. summarize into one reliability-qualified Outcome Confidence → `ConfidenceState`.

**Confidence derives from understanding; it is not primary** — it exists only as a summary of CAF, and changes only because CAF changed (because understanding changed). **No weights, no percentages, no formulas** are specified here — the summarization *relationship* is fixed (CAF + reliability → summary); the *arithmetic/calibration* is owner-track (Planning Intelligence §8; Matrix §22 g1). The engine must keep confidence and its reliability qualifier inseparable — never emit a bare value.

---

## 14. Confidence Recalculation Mechanics

- **When:** on every completed run after the first (each completion yields a new ConfidenceState); deep runs are the typical recalculators.
- **Triggers:** the recompute rules (Event Model §15 / State Model §15) — orientation completion, substantive artifact/context change, fix applied, manual, collaboration-derived evidence. **No-change → no-recompute** (determinism, §15): re-running on identical understanding does not manufacture a new value.
- **Supersession chains:** the new `ConfidenceState` sets `supersedes_confidence_state_id` → prior current; the project's current pointer advances; prior states are **retained** (history). Same chaining applies to CAFState (latest current; prior historical) and to superseded findings/recommendations. **No destructive mutation.**

---

## 15. Determinism Contract  *(most important)*

The engine must behave **deterministically with respect to understanding**, so results are explainable, testable, and replayable.

- **Same-input behavior:** given the **same inputs and the same engine configuration (model version + settings)**, a run yields **equivalent** outputs — the same set of findings (by type and basis), the same recommendations, the same CAF assessment and confidence band/qualifier.
- **Replayability:** because outputs are persisted and events are append-only/idempotent, a historical run's *recorded* result is the source of truth; replay reconstructs persisted state exactly (§16). Determinism governs *fresh* re-execution; replay governs *reconstruction*.
- **Idempotency:** re-emitting a run's events or re-applying its transitions converges to the same state (set-to-state). Duplicate triggers are coalesced; identical-input re-runs do not fabricate new states (no-change → no-recompute).
- **Acceptable variation / bounded equivalence:** any non-determinism inherent to the underlying model must be constrained to a **bounded-equivalence** band such that the *governable outputs* (finding type set, recommendation set, confidence band, reliability qualifier) are stable even if incidental phrasing differs. **The exact tolerance is `TBD – Owner Decision Required`** (Testing §20.1) — **no numerical tolerance is invented here**; the contract specifies *that* equivalence must be bounded and over *which* outputs, not a number.
- **Configuration pinning:** the engine records the configuration (model version/settings) used by each run so determinism is evaluated against a fixed configuration and changes are attributable.

This contract is the conformance target for the Testing Strategy determinism and replay suites (§6–§7 there).

---

## 16. Replay Contract

- **How historical runs are replayed:** by replaying the append-only event log into a clean store (Event Model §17). Persisted run outputs (CAFState/ConfidenceState/findings/recommendations) and their supersession chains are reconstructed from the recorded events — **not** by re-executing the model.
- **Expected outcomes:** reconstructed state is **identical** to the original (modulo suppressed external side effects); the AnalysisRun chain, confidence chain, and finding/recommendation statuses rebuild exactly.
- **Required guarantees:** deterministic reconstruction; external side effects (notifications) suppressed during replay; duplicate/out-of-order events deduped and reordered to the same result. Replay is the authoritative mechanism for history/audit; live determinism (§15) is separate and governs new computation.

---

## 17. Event Integration

Engine stages map to **existing** Event Model events (no new events):

| Stage / moment | Event |
|---|---|
| Fast run accepted / queued | `fast_analysis_requested` |
| Fast run begins | `fast_analysis_started` |
| Fast run publishes | `fast_analysis_completed` → `confidence_created`, `finding_created`×N, `recommendation_created`×M |
| Deep run accepted / queued | `deep_analysis_requested` |
| Deep run begins | `deep_analysis_started` |
| Deep run publishes | `deep_analysis_completed` → `confidence_recalculated` + `confidence_superseded`, expanded `finding_created` / `finding_superseded`, expanded `recommendation_created` / `recommendation_superseded` |
| Prior run replaced | `analysis_superseded` |
| Run errors | `analysis_failed` |
| Run cancelled | `analysis_cancelled` |

Fan-out is ordered `confidence → finding → recommendation → notification` under one `correlation_id` (Event Model §16).

---

## 18. State Integration

Engine outputs cause **existing** State Model transitions (no new states):

| Engine action | Transition |
|---|---|
| Fast run queued→running→completed | Project `orienting → oriented`; run `queued→running→completed` |
| Deep run lifecycle | Project `deep_analyzing → analyzed` (recurring); run `queued→running→completed` |
| New confidence published | ConfidenceState `current`; prior → `superseded` |
| Finding emitted / expanded | Finding `detected`; (deep) prior may → `superseded` |
| Recommendation emitted / expanded | Recommendation `generated`; prior may → `superseded` |
| Run error / cancel | run `failed` / `cancelled`; Project reverts to last completed state |

The engine never sets a state the State Model doesn't define and never performs a transition it doesn't sanction.

---

## 19. Performance Integration

- **60-Second Orientation:** the Fast pipeline (§9) must publish orientation **< 60s** for in-envelope projects (the one approved target; NFR §3). Queue-time counts against the budget and is monitored separately (NFR §18).
- **Deep Analysis lifecycle:** asynchronous, coalesced, recurring; completion target, timeout, and debounce window are **`TBD – Owner Decision Required`** (NFR §4). The engine must be cancellable mid-run and must not block the UI.
- **No new latency targets invented** — the engine inherits NFR targets; non-60s values remain TBD.

---

## 20. Failure Handling

| Condition | Behavior |
|---|---|
| **Analysis failure** | run → `failed`; emit `analysis_failed`; Project reverts to last completed state; prior outputs intact |
| **Partial failure** | no partial commit — a run publishes atomically or not at all; an incomplete run does not leave half-written CAF/confidence/findings (all-or-nothing publication) |
| **Recovery** | on restart, a `running` run with no progress → `failed` (idempotent re-run safe); recompute rules re-trigger as needed |
| **Retries** | failed run is **not** restarted in place — a **new** `AnalysisRun` is queued (`previous_run_id` linked); the failed run is retained; retry bound `TBD` |
| **Cancellation** | `:cancel` from `queued`/`running` → `cancelled`; no partial commit; terminal, retained |
| **Supersession** | a completed run supersedes the prior current run/states; superseded artifacts retained — never deleted to change state |

Invariant: failures and cancellations **never corrupt prior understanding** — the last completed run and its states remain current until a new run completes (State Model §17).

---

## 21. Traceability

Every output is traceable end to end, from stored relationships (no recomputation needed for explanation):

```text
Input (evidence / context item)
  → Reasoning (the evaluation stage that fired)
    → Finding (type + affected dimension + basis links)
      → Recommendation (type + rationale, on that finding)
        → Confidence (CAFState + ConfidenceState the run produced)
```

Requirements: each Finding records `first_seen_run_id` + `evidence_links`; each Recommendation records its `finding_id` + producing run; each ConfidenceState records `analysis_run_id` + `supersedes_confidence_state_id`. The engine must persist these links on publication so any signal answers "why is this here, and what changed?" directly.

---

## 22. Worked Examples

**Fast Analysis example.** New project, evidence "must integrate with the existing CRM, must be fast." Fast pipeline: acquire→normalize→fast extract (claims: CRM-integration, "fast"); evaluate → **Ambiguity** finding ("fast" undefined, Clarity) + **Assumption** finding (CRM API availability, unsupported); generate **Validation** recommendations; produce CAFState (Clarity lower) + reliability-qualified ConfidenceState; publish MRI. Orientation < 60s. Project `oriented`; "not final" banner condition holds.

**Deep Analysis example.** Triggered after orientation. Deep pipeline enriches context, expands relationships (links the CRM assumption to 3 requirements), **discovers a Conflict** (a requirement needs offline mode the CRM dependency can't support). Emits an **Expanded Finding** (Conflict, Alignment, `first_seen_run_id`=deep run) + **Expanded Recommendation** (Improvement: reconcile offline vs CRM dependency).

**Confidence recalculation example.** The deep run's CAF reassessment lowers Alignment but at **higher reliability**; a new ConfidenceState is published, `supersedes_confidence_state_id` → the fast run's; the fast confidence is retained as history; the project's current pointer advances. UI confidence chip updates.

**Expanded finding example.** The Conflict above did not exist in the fast result; it appears only after relationship expansion — exactly an Expanded Finding, basis-linked to the CRM assumption and the offline requirement.

**Expanded recommendation example.** The Improvement recommendation reconciling the conflict is generated for that expanded finding; if a later run finds a better corrective, the earlier recommendation is `superseded` (retained), preserving the improvement trail.

*(Illustrative mechanics; no new types, formulas, or values.)*

---

## 23. Open Questions (not solved here)

1. **Determinism tolerance value** — the bounded-equivalence band over governable outputs (`TBD – Owner Decision Required`).
2. **Fast/Deep horizon boundary** — precisely what extraction the fast horizon defers (engine tuning).
3. **Severity assignment basis** — principled critical/moderate/warning (owner-calibrated, no thresholds here).
4. **CAF→Confidence summarization method** — owner-track calibration (Matrix §22 g1).
5. **Reliability qualifier scale** — owned by Reliability Model calibration.
6. **Coalescing/debounce window** for deep recompute — NFR/ops.
7. **Model configuration governance** — how model-version changes are rolled out vs determinism guarantees.
8. **Expansion prioritization/ordering** — for large finding/recommendation expansions.

---

## 24. Validation

- Release 1 only — ✅
- No governance — ✅ (§4; Deep pass performs none)
- No future architecture — ✅
- No new states — ✅ (§18; State Model verbatim)
- No new events — ✅ (§17; Event Model verbatim)
- No new entities — ✅ (§6; Data Model v1.1 entities)
- Planning Intelligence remains authority — ✅ (conflict rule; implements, never redefines)
- Determinism contract defined — ✅ (§15; no invented tolerance)
- Replay contract defined — ✅ (§16)
- Fast Analysis defined — ✅ (§7, §9)
- Deep Analysis defined — ✅ (§8, §10)
- No scoring formulas / weights / thresholds introduced — ✅

**Release 1 Analysis Engine Specification complete.**

# Wave S Contract Package — Synthesis Engine (Extraction · Synthesis · Generation)

**Contract Set:** IC-WS-SYNTH / QA-WS-SYNTH / OBS-WS-SYNTH · **Owning Responsibilities:** **Perceive** (extraction) + **Infer** (synthesis/generation) · **Status:** **Ratified under DL-047 (2026-06-04)** · **Date:** 2026-06-04
**Consumes (authoritative — must not redefine):** Cognitive Responsibility Architecture Specification (+ DL-047 Architecture Update) · Runtime Object Model (+ DL-047 Object Additions) · Runtime Behavior Model (+ DL-047 Behavior Additions) · QA Governance · Observability Governance · Calibration Defaults · DL-043 (Epistemic State Model · Derived Cognition Lifecycle) · DL-046 (Fast/Deep modes) · `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1` · `FAST_DEEP_WORKFLOW_PACK/` · `RELEASE_1_PLANNING_*` / Master Spec planning-artifact definitions.

> **Mode:** the front of the cognitive pipeline — **evidence → structured, evaluated planning model.** Sits **between Wave A (intake/retain/recompute) and Wave B (understanding)**: Perceive extracts attributed claims (Attested); Infer synthesizes the planning model and **generates planning artifacts as Derived Cognition**. **No new responsibility** (DL-047 Part A2 Option 1 — synthesis is an Infer extension). **Build order: after Wave A backbone, with/before Wave B.** Per `CLAUDE.md`, the owner ratifies.

---

## 0. Package Orientation

- **Capabilities owned:** `EI-02` Claim Extraction · `PS-01` Planning Synthesis Engine · `PS-02` Planning Artifact Generation · `PS-03` Understanding Evaluation seam.
- **Objects:** `AttestedAssertion` (evidence-attested; extraction output — existing type) · **`SynthesizedPlanningModel`** (Derived) · **`PlanningArtifact`** (Derived; generated; user-editable: Intent / Context / Scope / Requirements / WBS / Resources / Schedule) · `CognitionHistoryRecord` (per generation).
- **Upstream:** admitted evidence (Wave A-001 Perceive) → Retain canonical store (Wave A-002).
- **Downstream:** Wave B Evaluate seeds initial CAF/Confidence from the `SynthesizedPlanningModel`; the model + artifacts are presented by Disclose (Wave E) and recomputed by 00R (Wave A) on change.

---

## 1. Implementation Contract — IC-WS-SYNTH

### A1. Identity
- **Owners:** **Perceive** (A-extraction) and **Infer** (B-synthesis/generation) — one producer per output; no new responsibility.
- **Produces:** evidence-attested `AttestedAssertion`s (Perceive); `SynthesizedPlanningModel` + `PlanningArtifact`s (Infer, **Derived**).
- **Consumed by:** Evaluate (seed), Disclose (present), Act/Adapt (recompute).

### A2. Purpose
Turn admitted evidence into (a) **source-attributed claims** (what each source asserts — Attested) and (b) a **synthesized, generated planning model** (OSLO's interpretation — Derived, recomputable), so the rest of the pipeline (Evaluate/Advise/Disclose) has a structured project to reason over even from incomplete evidence.

### A3. Required Behavior
**Perceive (extraction) must:**
1. **Extract source-attributed claims** from admitted evidence into `AttestedAssertion`s of the correct content type (Canonical Fact / Assumption / Constraint / Dependency), **each attributed to its source artifact and re-derivable**; hand them to Retain.
2. Perform **no Derived cognition** — no Findings, severity, confidence, or synthesis (those are Infer/Evaluate).

**Infer (synthesis + generation) must:**
3. **Synthesize a `SynthesizedPlanningModel`** from Attested assertions (Evidence Extraction → Context Expansion → Planning Construction), filling gaps with **explicitly-flagged assumptions** (never silent).
4. **Generate `PlanningArtifact`s** (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) from the model — as **Derived Cognition**: non-canonical, recomputable, **append a Cognition History Record per generation**, two-axis replay (semantic for AI-generated content), and **user-editable** (a user edit is a **new Attested input** to Retain that **triggers recompute** — it does not mutate the Derived record in place).
5. On recompute (00R), **re-synthesize and supersede** the prior model/artifacts (live replaced; history appended).
6. Carry `epistemic_state = derived`, `mode` (fast|deep, DL-046), and `confidence_stage`/Understanding-State on each emission.

### A4. Forbidden Behavior
- Perceive emitting a Finding/assessment, or admitting an **unattributable** "fact."
- **Writing a generated `PlanningArtifact` (or `SynthesizedPlanningModel`) into the canonical store as Attested-truth** (it is Derived; only the *user's edit* is a new Attested input).
- Changing a generated artifact **outside recompute**; **overwriting** a Cognition History Record.
- **Silent gap-filling** — every inferred assumption/constraint/dependency in the model is flagged as such (Derived), never presented as evidence-attested fact.
- Governing exposure or accepting an interpretation as truth.

### A5. States
`Derived (this synthesis) → Superseded (re-synthesis)`; never deleted (history append-only). User edit → new Attested input → recompute → new Derived version.

### A6. Inputs / Outputs
- **Inputs:** admitted evidence (Perceive); Attested assertions (Retain).
- **Outputs / events:** `Claim Extracted` (Perceive); `Planning Artifact Generated` / `Planning Artifact Regenerated` / `Synthesized Model Updated` (Infer) — each appends a CHR.

### A7. Bound Invariants
Canonical = Attested (extracted claims are evidence-attested; generated artifacts are **Derived**, never Attested-as-truth); one-way flow (Derived never promoted to Attested); recompute-appends-never-overwrites; one producer per output; assumptions explicit; no Authority; OSLO never self-accepts.

---

## 2. QA Contract — QA-WS-SYNTH

- **Positive:**
  - Extraction produces **source-attributed, correctly-typed** assertions from evidence; each is re-derivable to its source.
  - Synthesis produces a `SynthesizedPlanningModel`; generation produces the **seven `PlanningArtifact` types**, each **Derived** with `epistemic_state=derived` and a CHR appended per generation.
  - A **user edit** to a generated artifact is admitted as a **new Attested input** and **triggers recompute**; the prior Derived version is **superseded** (prior CHR intact).
  - Evaluate can seed initial CAF/Confidence from the `SynthesizedPlanningModel` (PS-03 seam exercised).
  - Inferred assumptions in the model are **flagged Derived**, not presented as evidence-attested.
- **Negative (impossible / rejected — each a test):**
  - Perceive emitting a Finding/severity/confidence; admitting an **unattributed** assertion.
  - A generated artifact **written to the canonical store as Attested-truth** *(Critical)*.
  - A generated artifact **changed without recompute**, or a **CHR overwritten** *(Critical)*.
  - **Silent gap-filling** — an inferred assumption presented as evidence-attested fact *(Critical)*.
  - OSLO **autonomously editing the user's artifact** (artifact mutation must originate from the user) *(Critical)*.
- **Failure classification:** Critical — Derived-as-Attested / change-without-recompute / history overwrite / silent gap-fill / autonomous artifact write. Major — wrong assertion type; missing source attribution; generation without CHR; missing assumption flag. Minor — metadata/label gaps.
- **Determinism tier (QA Governance):** extraction of explicit attributions = **exact-if-rule**; AI-synthesized model/artifacts = **semantic-equivalence** replay (same plan identity/intent; wording may differ); set-level ≥90% stable-identity overlap of generated sections.

---

## 3. Observability Contract — OBS-WS-SYNTH

- **Events:** `Claim Extracted`, `Planning Artifact Generated/Regenerated`, `Synthesized Model Updated`, `CognitionHistoryRecord appended` — each carrying `mode` + `confidence_stage`.
- **Audit:** for every generated artifact — which Attested assertions it derived from, model/prompt/rule version, upstream lineage, and the flagged assumptions used (answers *why this Scope says X*).
- **Replay:** record-exact for each emission; derivation **semantic** for generated content (exact for rule-structural parts).
- **Drift / Trust:** a generated artifact changing without recompute, a missing source-attribution on an extracted claim, a missing assumption flag, or an autonomous artifact write = **trust failures**; **evolution of the synthesized model across history = product feature** (the "understanding keeps improving" capability).

---

## 4. Triad Consistency & Conformance (Framework §E/§H/§K)

- **§E traceability** ✅ — Extraction→Perceive, Synthesis/Generation→Infer, seed→Evaluate, present→Disclose, recompute→Act/Adapt; objects (`SynthesizedPlanningModel`, `PlanningArtifact`) trace to the DL-047 Object Additions; behaviors to the DL-047 Behavior Additions. One producer each.
- **§H triad consistency** ✅ — QA positives↔IC required, negatives↔IC forbidden; IC-emitted events ⊆ OBS-observed; invariants bound (IC) / validated (QA) / observed (OBS); the **generated-artifact = Derived, user-edit = new Attested input → recompute** discipline is consistent across all three.
- **§K pre-use** ✅ — no orphan behavior; no new responsibility (Perceive/Infer extensions); no Authority; no env binding; preserves DL-043 invariants and DL-046 modes.

---

## 5. Verdict

**CONFORMANT — ready for owner approval.** The evidence→plan engine is now contracted at full IC/QA/OBS depth with the hard negative tests that protect the epistemic boundary for **generative** output (Derived-not-Attested; no silent gap-fill; no autonomous artifact write; recompute-appends). It introduces no new responsibility and preserves every DL-043/046 invariant.

---

*This Wave S contract package contracts OSLO's evidence→plan synthesis engine at full depth: Perceive extracts source-attributed claims into evidence-attested assertions (no Derived cognition), and Infer synthesizes a planning model and generates the seven planning-artifact types as Derived Cognition — recomputable, history-tracked, user-editable (a user edit is a new Attested input that triggers recompute, never an in-place mutation), with explicitly-flagged assumptions and no autonomous OSLO artifact writes. It specifies required and forbidden behavior, positive and negative QA including the Critical negatives that guard the generative boundary (Derived-as-Attested, change-without-recompute, history overwrite, silent gap-fill, autonomous artifact write), determinism tiers (exact for explicit attributions, semantic for AI-synthesized content), and observability (events, audit lineage, replay, drift/trust signals), and confirms triad consistency with no new responsibility — implementing DL-047 Part A as the front of the cognitive pipeline between Wave A and Wave B.*

**Wave S Contract Package — Synthesis Engine complete (DL-047).**

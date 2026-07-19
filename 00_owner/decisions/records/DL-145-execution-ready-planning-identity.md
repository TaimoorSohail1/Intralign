# DL-145 — Execution-ready planning — OSLO produces the detailed, exportable plan (Phase-1 identity)

- **Date:** 2026-07-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Execution-ready planning — OSLO produces the detailed, exportable plan, and certifies it honestly (Phase-1 identity)

**Class:** A (product identity / scope — the largest since the reporting roadmap; it names what OSLO's deliverable *is*) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-19 · **Packet:** `DECISION-PACKET-execution-ready-planning.md` (resolutions recorded there).
**Amends / retires** the **"no dependency register" implementation stance** (OSLO may now model task-sequencing dependencies as inferred, marked plan structure). **Distinguishes** the new *sequencing* dependencies from **D114 "Understanding dependencies"** (waiting on a person's response — unchanged). **Extends** D172d/DL-141 (the workspace and its documents). **Upholds and reinforces** D003 (maturity, not health), the Progress guard (progress = understanding, not completion), D183b (no composite/forecast score), D173 + DL-109 (computed, then marked — inference named honestly), D011/D069 (the From OSLO / Confirmed by you classes), D088 (the read moves by analysis), D160 (the reading surface).

---

## Decision

**OSLO's deliverable is an outcome-optimized plan that is detailed and exact enough to export into an execution tool and run.** Assessment — Outcome Confidence via Clarity · Alignment · Feasibility, the issue model, the maturity read — is the *mechanism* that drives a plan toward being trustworthy enough to execute; the **plan is the end.** A plan that stops at deliverable altitude is a table of contents, not an executable plan. This DL ratifies the identity and scope of that objective. It is **Phase 1** — the model build and the export are follow-on DLs (see Scope).

Seven components are ratified:

1. **The boundary is the export handoff.** OSLO owns *producing and certifying* the plan — decomposition, sequencing, owners, dates, acceptance, and grounding — **detailed and exact**. The execution tool owns *running* it — live status, percent-complete, actuals, day-to-day tracking. Task-level depth is therefore **not** scope creep into a task-tracker; it is the required content of the artifact OSLO hands off. This boundary *reinforces* the anti-health-tracker spine: OSLO produces the plan, the execution tool tracks completion, and the handoff is exactly that line.

2. **OSLO both authors and certifies.** Where the user provides no execution-level detail, OSLO **infers** the decomposition needed to make the plan complete and executable; where the user provides partial detail, OSLO **uses it and infers the remaining gaps**. In both cases **every inferred element is marked, and the user validates it.** This is not a new epistemic model — it is the ratified **From OSLO / Confirmed by you** engine (D011/D069), pushed down to execution-task altitude. Authoring is reconciled with "computed, never invented" (D173) by the marking rule: OSLO may now infer *plan structure*, but it never presents inference as fact — every inferred task, owner, date, and dependency is labelled From OSLO and awaits validation (DL-109).

3. **Depth rule — infer to completeness; honesty comes from grounding, not from refusing to infer.** OSLO decomposes to the depth needed to execute and export, inferring gaps — but completeness and trust are kept as **separate axes**: an inferred plan reads as low-maturity until validated, so readiness is *earned by confirmation, not by how decomposed the plan looks*. Two disciplines bound it: depth is **outcome-driven at competent-planner granularity** (sufficient to execute, not maximally decomposed — "detailed and exact" never becomes "invented and false"), and inference is **graded** (thin/speculative structure is flagged low-confidence, a louder prompt to validate, so attention goes to the shakiest invented structure first).

4. **Execution-readiness is a coverage read surfaced as a validation-progress state — never a score.** Readiness is measured as the **provenance coverage of the execution-critical set** — how many execution-critical elements are Confirmed by you vs still From OSLO (countable, honest, reusing the grounded/inferred engine; **no composite, no forecast**, per D183b). For legibility it is surfaced as a **named state in validation-progress language** — describing *what the user has validated* (e.g. mostly-OSLO's-draft → load-bearing confirmed → fully validated), **never a fitness verdict** ("ready / will-succeed"). The state is **derived from the coverage** (one substrate — counts have one home), scoped to **artifact-readiness, not outcome-likelihood**, and **non-blocking** (export is always available; OSLO plainly says what is still inferred in what you are about to hand off).

5. **Task-sequencing dependencies are in — modelled as inferred, marked plan structure — to the depth of edges + critical path.** OSLO models which tasks depend on which (inferred + marked), and computes the **critical path** — the chain driving the outcome date — as **feasibility analysis** (a CAF dimension), which stays cleanly on OSLO's side of the handoff (analysing the plan, not tracking execution). Task durations required for the path are themselves inferred-and-marked (flagged low-confidence), so the critical path is a validate-able artifact that firms as estimates are confirmed. **Resource leveling is deferred** as a separate later decision (most tool-like; needs the least-inferable inputs — per-owner capacity, effort — so the highest false-precision risk). ⛔ This **retires the "no dependency register" implementation stance** and is **distinct from D114 "Understanding dependencies"** (waiting on a person's response), which is unchanged; the two must be named apart (sequencing dependency vs understanding dependency) so they do not collide.

6. **One converged task model underneath; the seven documents stay as focused views; an eighth consolidated view is the pre-export surface.** Underneath, each task carries its decomposition, date, owner, and dependencies together (the coherence a clean export requires). On screen, **Work breakdown · Schedule · Resources remain focused views** for reviewing and editing in isolation — the seven-document model and the reading surface (D160) are preserved. An **eighth, consolidated view** shows the whole sequenced plan for pre-export review; it is the natural home of the **readiness state** (§4) and the **critical path** (§5), and is expected to be validate-enabled (confirm inferred elements inline before export).

7. **The execution-export is a structured, provenance-preserving hand-off — a deep connector, Asana first.** Distinct from the reader-export shipped in DL-144 (a frozen human snapshot), the execution-export maps tasks→tasks, owners→assignees, dates→dates, dependencies→dependencies into a real execution tool. **First target: Asana** (matches OSLO's general/cross-functional PM ICP and the event demo; task/subtask hierarchy, dependencies, and custom fields for provenance; modern API). **Jira** is the fallback if the ICP shifts to software teams. ⛔ **Non-negotiable acceptance criterion:** inferred-vs-confirmed **provenance must land as a native field** (custom field / label / status) so the validation loop continues *inside* the execution tool — a hand-off that drops provenance silently turns OSLO's inference into "the plan," and is forbidden.

## What stays intact — and is reinforced

- **Maturity, not health** (D003) — OSLO reads how mature/grounded the plan is; it does not emit project health or a success probability.
- **Progress = understanding, not completion** — *reinforced* by §1: completion tracking lives past the export handoff, in the execution tool. OSLO never becomes a percent-complete tracker.
- **No composite / no forecast score** (D183b) — readiness is coverage + a validation-progress state, never a number or a fitness verdict.
- **Computed, then marked — never silently invented** (D173 / DL-109) — the bridge that lets OSLO *author* plan structure: every inference is surfaced for validation, and named honestly, never as a defect and never as a certainty.
- **OSLO advises; you decide** — the user validates every inferred element; OSLO never commits the plan on the user's behalf.

## Guardrails (to be enforced when the model is built — Phase 2/3)

- **Completeness ≠ readiness.** A fully-decomposed, fully-inferred plan must **never** read as ready — the readiness state is a function of *grounding*, not of decomposition. (The assumptions doctrine, at plan scale.)
- **Depth is bounded by inferability.** OSLO infers the decomposition a competent planner would draft from the evidence; where it cannot infer at reasonable confidence, it **names the gap** rather than inventing detail.
- **Provenance survives every boundary** — the on-screen marks, the eighth-view review, and the execution-export all carry inferred-vs-confirmed; no surface may present inferred structure as fact.
- **Sequencing dependency ≠ understanding dependency** — the new model is named apart from D114 so the two never conflate.
- **The read still moves by analysis** (D088) — confirming inferred structure firms the read at the next analysis update, never by the hand-path alone.

## Scope — this is Phase 1 (identity); the build follows

- **Phase 1 (this DL):** the objective, the boundary, the role, the depth rule, the readiness signal, the dependency-stance retirement, the converged-model + eighth-view shape, and the Asana-first export direction — **ratified as identity/scope.**
- **Phase 2 (follow-on DLs):** the model — task-altitude decomposition with graded inference-marking; assessment (CAF + issues) scaled to task/subtask altitude; the sequencing-dependency model + critical path; the converged model and eighth view.
- **Phase 3 (follow-on DLs):** the structured, provenance-preserving Asana export; and the Work breakdown mock deepened to demonstrate the whole — the mock **follows** the decision, it does not front-run it. (This is the observation that raised the packet; it is deliberately the last thing built, not the first.)

## Governance

Lands as **Class-A** canon via `dl-land`, retiring the "no dependency register" implementation stance and establishing the execution-ready planning objective. It is drafted from a reviewed packet whose sub-decisions the owner resolved one at a time (depth · readiness · dependencies · model + eighth view · export target · scoping). No product code changes in this DL — it is the identity ratification the Phase-2/3 build DLs will realize and verify. AI drafted + built the analysis; **only the owner ratifies.**

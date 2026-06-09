# Consolidated Architecture Guidelines

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** Architecture Baseline · Planning Intelligence · Analysis Engine · Data/State/Event Models · CAF/Reliability/Confidence models. Tags: `canonical` / `derived` / `proposal` / `TBD`.

> The locked architectural rules the Fast/Deep workflow must preserve. These bind implementation; the workflow specs in this pack conform to them.

## 1. Layer responsibilities (canonical)

| Layer | Owns | Does NOT |
|---|---|---|
| **Context Plane** | extracts, normalizes, enriches evidence into context items | reason / assess |
| **Knowledge Layer** | stores canonical, versioned understanding; relationship graph | reason / assess |
| **Planning Intelligence** | defines the reasoning (how OSLO understands/assesses) | execute / persist |
| **Analysis Engine** | executes Fast and Deep passes per Planning Intelligence | redefine reasoning / govern |

Authority order when sources conflict: **Planning Intelligence > State Model > Event Model > Data Model > Analysis Engine > NFR > API/UI/Testing > Supporting models > Proposal notes.**

## 2. Pass rules (canonical)

- **Fast Pass produces the 60-second orientation.**
- **The 60-second orientation is NOT final understanding.**
- **Deep Pass runs after orientation and expands understanding.**
- Deep performs **no governance**.
- Both execute the same reasoning and produce the same object types; they differ by horizon/latency/completeness/reliability.

## 3. Object discipline (canonical)

- **Findings are descriptive.** **Recommendations are advisory.**
- **Confidence is derived from CAF + Reliability** — not primary, never bare.
- **CAF dimensions:** Clarity, Alignment, Feasibility (integrity of understanding); independent assessment targets.
- **Reliability** = supportability of the assessment, determined from Coverage / Evidence Availability / Assessability, independent of CAF; qualifies CAF, consumed by Confidence.
- **Prior outputs are superseded, not deleted.**
- **User retains authority; OSLO recommends, the user decides.**

## 4. Execution invariants (canonical/derived)

- **Event-driven:** state changes are caused by events; no-change → no-recompute.
- **Deterministic** w.r.t. understanding under a pinned model configuration (bounded-equivalence; tolerance `TBD`).
- **Replayable:** event-log replay reconstructs state exactly; side effects suppressed in replay.
- **Traceable:** every output explainable to basis from stored lineage.
- **Atomic publication:** a run publishes all outputs or none (no partial commit).
- **Tenant isolated:** every operation scoped by `workspace_id`; cross-tenant only via a valid `SharedArtifact`.

## 5. Global-skeleton pattern (PROPOSAL)

`proposal` — At Release 1 ingestion sizes (≤ ~33k-token ceiling), the corpus fits a single model context; chunking is a **latency** optimization, not a capacity requirement. To preserve global semantics while parallelizing:

1. **Stage A — global pass** (whole corpus, output-light): build intent restatement + entity index + relationship skeleton + cross-references.
2. **Stage B — local evaluation** (parallel chunks): each chunk **carries the Stage-A map** as shared context.

This keeps Alignment/Feasibility evaluable (relational), avoids chunk-boundary determinism hazards, and unlocks absence/coverage findings. It is a **proposal** pending owner ratification (OPEN_DECISIONS). Fallback: isolation-only with reduced reliability.

## 6. CAF "globality" gradient (derived)

- **Clarity** — intrinsic/local → most rule-amenable, fully evaluable in Fast.
- **Alignment / Feasibility** — relational/global → LLM, preliminary + lower-reliability in Fast, full in Deep.
- Reliability and `evaluation_completeness` therefore differ across the three dimensions in a Fast pass by design.

## 7. Forbidden (canonical — scope guardrails)

Governance Domain · Accepted Understanding · Agent Governance · Autonomous execution · Actuation · Outcome-orchestration runtime · invented formulas/weights/percentages/thresholds · treating Fast output as final understanding. (See SCOPE_GUARDRAILS.)

## 8. Open architectural decisions

Global-skeleton adoption; ingestion envelope; claim-count bounds; model tier; determinism tolerance; CAF/Confidence/Reliability scales; Deep timeout/debounce/retry — all **`TBD – Owner Decision Required`** (OPEN_DECISIONS).

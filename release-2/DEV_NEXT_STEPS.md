# OSLO R2 — Next Steps & Build Sequence (dev handoff)

**From:** Idris (owner) · **Date:** 2026-08-09 · **Scope:** how to pick up and build the R2 delta.

**Build from this `release-2/` tree — it is the single source of truth.** The old standalone `oslo-r2-build` snapshot is retired; do not build from it. Ten slice build-designs are signed off (`SIGNOFF.md`), with a behavioral reference prototype and a doctrine-guardrail acceptance suite.

---

## 1. Read first (orientation)

Before scheduling work, read, in order: the repo's top-level `REPOSITORY_ARCHITECTURE.md` and `00_owner/` manifest → `README.md` (this tree) → `BUILD_SEQUENCE.md` → `SIGNOFF.md` → `acceptance/README.md`. The "why" behind any locked rule traces to a ratified decision in `canon/decisions/`; the canonical terms are in the glossary — preserve them, don't coin new ones.

**The non-negotiable spine (if a design seems to break one of these, it's almost certainly wrong):** OSLO advises, you decide. The read only moves when the plan or its evidence moves — *only reanalysis resolves*. Maturity is a **read**, never a success **forecast** (ordinal bands Fragile→Sound, never a 0–100 score). Capacity is gated; **judgment quality never is**.

## 2. What's ready to build against

- **`slices/01…10`** — the spec. Each is self-contained (locked decisions, state/data/event models, honesty invariants, FE↔BE bindings, R1-reuse vs net-new, acceptance criteria). **Slice 10** is the new load-bearing sensitivity + issue-classification engine (realizes DL-209 + DL-210).
- **`oslo-prototype-r2.html`** (root) + `PROTOTYPE_REFERENCE.md` — the canonical reference implementation (DR-1) with the embedded `_S10` self-check harness (77/77 green, md5 `72068597`). Behavioral source of truth.
- **`acceptance/`** — the FE↔BE integration map + the **GT-01…GT-50** doctrine-guardrail test register (Slices 9 + 10). Wire these as CI gates.
- **`canon/decisions/`** — every locked rule's ratification (DL/DR records).

## 3. Build sequence (from `BUILD_SEQUENCE.md`)

1. **Phase 0 — establish the contract.** Adopt Slice 9's FE↔BE integration map as the build contract (a surface not in the map isn't shippable). Stand up the `_S10` → GT-01…GT-50 harness skeleton in CI as pending/allowed-red so guards go green slice-by-slice. Apply the Phase-A prototype corrections listed in `BUILD_SEQUENCE.md`.
2. **Phase A — foundation (parallel pair):** **Slice 1** (integrity engine, weakest-gate `min(V,G,A)`) + **Slice 3** (reanalysis engine + freeze/unlock). Freeze the *only-reanalysis-resolves* invariant (GT-10, pinned) before proceeding.
3. **Phase B — core lifecycle:** **Slice 2** (issue lifecycle & grounding acts).
4. **Phase B+ — the engine:** **Slice 10** (load-bearing sensitivity + issue classification). See §4.
5. **Phase C — read surfaces:** **Slice 5** (multi-outcome read) + **Slice 4** (freemium/commitment gate).
6. **Phase D — collaboration & output:** **Slice 6** + **Slice 7**.
7. **Phase E — telemetry:** **Slice 8**.
8. **Continuous — the keystone:** **Slice 9** (guardrails-as-tests + integration map). Read first (Phase 0), close last; all of GT-01…GT-50 green, pinned negatives red-if-violated forever, before R2 ships.

## 4. Slice 10 — the load-bearing sensitivity engine (build notes)

- **Ship L0→L3 first** with a conservative global `LB_THRESHOLD` (the ratified launch policy) — deterministic and defensible on day one. **L4 (feedback) + domain segmentation are v2**; they snap onto L2 without touching the invariants.
- **Quarantine the fuzziness:** only L0 (plan → dependency graph) is probabilistic; L1 (sensitivity + the top-down alignment traversal), L2 (calibration gate), and L3 (deterministic structural-target classification) are pure, decomposable functions.
- **Dimension is derived from the finding's *structural target*, not its finding-type** (definition→Clarity · edge→Alignment · achievability→Feasibility · truth→Grounding · coverage→Adaptability). Where the target is ambiguous/unmapped, **escalate — never default-classify.**
- Full detail: `slices/10-…` (esp. §3b) and `BUILD_SPEC_DL-209_load-bearing-sensitivity-engine.md`.

## 5. Owner-in-the-loop touchpoints (loop me in — these are not dev decisions)

- **L2 threshold calibration.** `LB_THRESHOLD` + asymmetric-loss/floor are set by a procedure, not guessed: ship the conservative-floor policy → shadow-run against the first real plans → I review the surfaced-vs-suppressed boundary → lock → telemetry-confirm. Build the mechanism; leave the value in config.
- **`MODELGAP_LEVERAGE_GATE`** (DL-210) — owner-config.
- **Other owner-open config numbers** are catalogued in `BACKLOG.md` → *Owner-Open Decisions* and `DEMO_CONFIG_REGISTER.md` (reanalysis window, delegate role/access matrix, tracker choice, readiness-gate stats, band cutpoints, etc.). Build the mechanism; keep the value in config; flag me when you reach one.

## 6. Honesty invariants — hard constraints (the pinned guards)

Never build a path that violates these; each is a pinned/negative test:

- **Only reanalysis resolves** (GT-10) — a click enqueues; a batch re-read is the sole writer of any band/issue move.
- **Only *verify* moves Grounding** (GT-35) — a build moves Viability/Adaptability, never Grounding; a decide manufactures no certainty.
- **Dimension derived from structural target, not finding-type** (GT-46); **alignment is edge-keyed and outcome-traced** (GT-47).
- **Unknown ≠ bad** — a load-bearing region OSLO can't assess reads *incomplete*, never Fragile, and never takes a numeric penalty (GT-49/GT-50).
- **Never-metered exemptions** (GT-02) and **no-write projections** (GT-14/31/06) stay intact.

## 7. Working rules (governance)

- **Never push to `main`.** Work on a branch → PR → green doc-integrity gate → owner merge.
- **Anti-Assumption:** if a spec is silent or two rules seem to conflict, **escalate it — don't infer, don't edit canon directly.** Raise a proposal; the owner ratifies. Dev authors the realization and *proposes* policy; the owner ratifies policy intent.
- Preserve canonical terminology (the glossary's Disambiguation Register) — no drift.

## 8. Verification & graduation (what's yours vs mine)

- **Your verification is the GT suite** (GT-01…GT-50 as server-side twins of the `_S10` oracle). Green suite = shippable; red suite blocks.
- **Canon reconciliation / the product-grill pass is owner-governed, not yours.** DL-209/DL-210 are staged in `release-2` and fold into `main` at R1 graduation via a separate integration branch (see `R2_TO_MAIN_INTEGRATION_PLAN.md` + `R2_TO_MAIN_CAF_RECONCILIATION_CATALOG.md`). That's my track; you don't reconcile product canon.
- **When the grill runs (owner-side sequence, for shared visibility):** *(1)* you build the engine against `release-2/` with the GT suite green → *(2)* at R1 graduation, the reconciliation-catalog edits are applied to the `10_product/domain` canon on the `integration/r2-to-main` branch → *(3)* **only then** the owner runs the full product-grill pass to verify whole-canon coherence → *(4)* PR → green doc-integrity gate → owner merge to `main`. The grill is triggered by **graduation** (canon landing in `main`), **not** by the engine build — and its timing is the owner's call. Your engine build and canon graduation are independent tracks: build against `release-2/` regardless of when graduation happens.

---

*Questions on any locked rule → trace it to its `canon/decisions/` record first; if still unclear, raise it with me rather than assuming. Build the mechanism, keep tunable values in config, and keep the honesty invariants green.*

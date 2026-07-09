# R1 Build Sequence & Gates — engineering handoff

**Purpose.** The outstanding work must be built in a specific order, and each step should be **enforced by a gate**, not left to memory. This note sequences the current PRs/branches and binds each step to the control that holds it. It is a co-governed handoff artifact (`20_handoff`); the owner ratifies.

**Read-first invariant.** Precedence is **Doctrine > Constitution > Implementation**. Build only to **ratified** canon. A proposal is not canon until the owner ratifies its DL.

---

## The sequence

### Step 1 — Integrate the R1 app onto `main` — **BLOCKER** (Issue #113)
- **What.** Merge `feat/phase6-wavee-disclose` → `main` (the R1 Disclose application; the app code is **not** yet on `main`).
- **Conflict rule.** `main` wins on governance/docs, `product-design/`, and `30_engineering/visual_regression/baselines/`; the branch wins on `code/**`.
- **Gate (enforces the step).** The integration PR must be green on the **six-gate CI + `doc_integrity_check.py` + visual-regression** before owner merge. It cannot merge otherwise.
- **Depends on.** Nothing — this is the root. Everything app-side is blocked until it lands.

### Step 2 — Reconcile the Disclose UI to the **updated** reference prototype
- **What.** PR #116 (merged) moved the reference-of-record prototype (`product-design/oslo_r1_experience_mockup_v4.html`) substantially — heatmap layout, finding panel, onboarding chat, closed-findings filter, share/export icons, tour anchoring, artifact-editable affordance — and refreshed **all 9** visual-regression baselines. The built UI must match the new target.
- **Gate (enforces the step).** **Visual-regression** (behavioral + pixel) compares the app against the updated baselines; divergence **fails CI**. This step is enforced automatically — no manual sign-off needed.
- **Depends on.** Step 1 (app on `main`).

### Step 3 — Do **NOT** build RB-035 — **GUARDRAIL** (PR #117)
- **What.** The no-Acknowledge lifecycle (D1) and single-action resolution (D2) are a **proposal, not ratified**. Build to the **current** `FINDING_SYSTEM_SPECIFICATION_V1 §C` (`detected → acknowledged → addressed → closed`, multi-step resolution).
- **Gate — existing.** `doc_integrity_check.py` blocks a `DL-PENDING` record from reaching `main`, so RB-035 cannot silently become canon.
- **Gate — to add (see below).** A **finding-lifecycle conformance gate** that fails CI if the *implementation* diverges from the ratified spec's state set — binding code to ratified canon so the proposed model cannot be built before the spec is amended.
- **On ratification.** When the owner numbers the DL, amends `§C` + the status enum, and lands the realization (spec → panel spec → prototype → baselines), the conformance gate's expected set updates in lockstep.

---

## How the order is *governed*, not just documented

Precedence (Doctrine > Constitution > Implementation) means **implementation must conform to ratified spec.** Each step is bound to an automated gate, so the ordering is enforced by "you can't merge X until gate Y is green":

| Step | Enforcing gate | Type |
|---|---|---|
| 1 — integrate app | six-gate CI + doc-integrity + visual-regression (on the #113 PR) + owner review | existing |
| 2 — reconcile UI | visual-regression (app vs updated baselines) | existing, automatic |
| 3 — don't build RB-035 | doc-integrity DL-PENDING guard **+** finding-lifecycle conformance gate (below) | existing + **proposed** |

---

## Proposed enforcement — Finding-Lifecycle Conformance Gate (FL-CONF)

A **negative-proven** conformance gate in the app CI, added as a row to `20_handoff/traceability/RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` (owner to adopt):

> | **FL-CONF** | Finding lifecycle conformance | `FINDING_SYSTEM_SPECIFICATION_V1 §C` · Wave B `IC-WB-*` | implemented `finding.status` set **==** ratified §C set `{detected, acknowledged, addressed, closed, reopened, superseded}`; transition rules match (**neg: `acknowledged` absent**; **neg: `detected → closed` permitted**; **neg: closure without a reanalysis run**) | `finding_lifecycle_changed` | III |

- **What it does.** The app carries a test asserting its finding-status enum and transition rules **equal** the ratified spec. If a developer builds the RB-035 model (drops `acknowledged`, or collapses to a state jump) before `§C` is amended, the assertion **fails CI** — the change literally cannot land against unratified canon.
- **Self-updating.** The gate reads the ratified state set from `§C`; when the owner amends `§C` (ratifying RB-035), the gate's expectation moves with it. No drift window.
- **Why this is the right control.** It operationalizes the precedence rule for the one place the proposal touches — the finding lifecycle — so "don't build the unratified proposal" is enforced by CI, not by this note.

---

## Quick status (as of this note)

- **PR #116** — merged. Reference prototype + baselines updated (Step 2 target moved).
- **PR #117** — open, green. RB-035 proposal (Step 3 guardrail); **not** ratified.
- **Issue #113** — open. R1 app integration (Step 1 blocker); on a daily read-only watch.

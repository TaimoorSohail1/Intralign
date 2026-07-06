# Proposal — Finding Flow Simplification (RB-035)

- **Status:** Proposed — awaiting owner decision (Framework 001 · Review complete, Decision pending)
- **Class:** A (domain-spec + data-model touch; presentation realization)
- **Backlog:** RB-035 (this proposal)
- **Author (analysis/recommendation only):** AI contributor under Framework 001A / DL-033. **AI does not ratify.**
- **Owner decision:** required to adopt, reject, or amend.

> Governance note: this is an **analysis + recommendation** routed through Framework 001 (Backlog → Proposal → **Review** → Decision → Change → Changelog). It proposes two **separable** decisions. The owner may ratify either, both, or neither. No canonical artifact is changed by this document; the `DL-PENDING-finding-flow-simplification` record carries the ratifiable decision text.

---

## 1. Problem

Two friction points in the Release‑1 finding flow, surfaced during the R1 UX refinement pass, appear to be **ceremony that the epistemic model does not require**:

1. **The `acknowledged` state.** `FINDING_SYSTEM_SPECIFICATION_V1 §C` defines the lifecycle `detected → acknowledged → addressed → closed`, where `acknowledged` = *"a user has accepted it as real."* But OSLO's own epistemic invariant is that **the user does not adjudicate a finding's validity — only reanalysis changes the assessment** ("acceptance alone isn't success"). A user "accepting a finding as real" therefore has **no effect on the assessment**: it records sentiment, not a state change OSLO acts on. The step is epistemically inert.

2. **Multi‑step resolution.** Resolving a finding today is *select an approach → (addressed) → update the plan → reanalysis → closed* — and where OSLO has drafted the fix, the UI splits "choose this approach" from "now apply it" into separate clicks. Since **OSLO drafts its own recommendation**, choosing it and applying it are the same act; the separate "now go update the plan" step is ceremony *when OSLO can draft the change*.

## 2. Proposed changes (two separable decisions)

### D1 — Collapse the lifecycle: drop `acknowledged`

New lifecycle: **`detected/open → addressed → closed`**; `closed → reopened`; `{detected, addressed} → superseded`.

- Removes the user‑validation gate. Findings remain **descriptive** in every state.
- **Preserves every epistemic invariant:** `open → addressed → closed` still passes through `addressed` (the `§C` rule *"Invalid: detected→closed (must be addressed)"* is honored); closure is still **only by reanalysis**; findings are still append‑only / retained.
- Semantics: not resolving leaves a finding **Open** — its realness stays OSLO's open call until reanalysis, which is the canonical stance.

### D2 — Single‑action resolution (where OSLO can draft)

Collapse "choose approach → apply to plan" into one confirm — **"Apply this fix"** — that applies OSLO's drafted change to the artifact and triggers reanalysis.

- **Preserves the invariants:** the click *is* the user's confirmation of the plan change ("nothing changes without you"); **reanalysis — not the click — closes** the finding; `addressed → closed` still holds.
- **Scope:** single‑action applies where OSLO has a draftable fix (its recommendation, and any alternative it proposed). Where OSLO cannot draft (e.g. "assign an owner"), the user edits the plan themselves — the two‑step remains, and a **"Write my own fix"** path is always available.

## 3. Framework 001A Review

**Findings.**
- The `acknowledged` state records user sentiment with no assessment effect, which is in tension with the canonical rule that only reanalysis changes the assessment (`FINDING_SYSTEM_SPECIFICATION_V1 §C`; `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`).
- The proposed lifecycle and resolution **strengthen** consistency with the epistemic model rather than weaken it; no invariant is removed.
- The acceptance subsystem (Wave U) is **architecturally decoupled** from finding lifecycle states — `acceptance_capture.py`, `retain/acceptance.py`, `evaluate/acceptance_impact.py` record accept/reject/defer/direct‑edit on version‑pinned items and never read/write `finding.status`. Dropping `acknowledged` does **not** touch acceptance code.
- The **Wave C & U contracts are silent** on finding lifecycle states — they govern recommendations (advisory) and user‑acceptance records, not `finding.status`. No contract clause requires `acknowledged` or the multi‑step resolution.

**Concerns.**
- **C1 — "reviewed‑but‑parked" signal.** Without `acknowledged`, a user who has seen a finding, agrees, but isn't resolving it now has only *Open* (looks untouched) or *Defer*. Mitigation: **Defer** covers "seen, parked"; a lightweight non‑assessment "pin/flag" could be added later if needed. Recommend confirming Defer is sufficient before adopting D1.
- **C2 — upstream state enum.** `§C` states are annotated *"(State Model §10 / Data Model v1.1 — unchanged)"*. Removing `acknowledged` requires amending **the State Model + Data Model enum**, not just `§C`. This is the primary realization dependency.
- **C3 — coupling check.** `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1 §3` keys on `closed` / `superseded` / `weakened`, **not** `acknowledged` — so coupling is unaffected. To be confirmed, not assumed.
- **C4 — migration.** Any persisted findings in `acknowledged` map losslessly to `open` (the state had no assessment effect). Trivial, but state‑enum migrations should be noted for the persistence layer.
- **C5 — D2 draftability.** Single‑action presumes OSLO carries a concrete `SuggestedFix`/draft for its recommendation. R1 demo data is sparse here; the realization must ensure the recommended path is draftable (else fall back to the two‑step). This is a **product/engineering realization** detail, not a doctrine question.

**Dependencies.**

| Artifact | Zone | Impact | Action |
|---|---|---|---|
| `FINDING_SYSTEM_SPECIFICATION_V1 §C` | 10_product/domain | **HARD** | Amend state table + transitions (remove `acknowledged`) |
| State Model §10 / Data Model v1.1 (finding‑status enum) | 10_product/domain | **HARD** | Amend the enum; note persistence migration |
| `FINDING_PANEL_SPECIFICATION_V1` / `FINDING_PRESENTATION_SPECIFICATION_V1` | 10_product/experience | **MED** | Update panel flow (no Acknowledge; single‑action Apply) |
| `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1 §3` | 10_product/domain | **CHECK** | Confirm unaffected (keys on closed/superseded, not acknowledged) |
| Wave B Infer/Evaluate contract (finding generation + transitions) | 20_handoff/contracts | **CHECK** | Confirm state transitions reference no `acknowledged` obligation |
| Wave C & U contracts (advisory + acceptance) | 20_handoff/contracts | **NONE** | Silent on finding states — no change |
| Acceptance code (`perceive`/`retain`/`evaluate`) | 30_engineering (code) | **NONE** | Decoupled from finding states — no change |
| Reference prototype (`product-design/…mockup_v2.html`) | product-design | **REALIZE** | On ratification, apply Prototype B (see `90_research/design_artifacts/`) + refresh visual‑regression baselines |

**Recommendation.**
- **Adopt D1 and D2**, conditioned on the HARD/CHECK dependencies above being realized and confirmed. Both are epistemically sound and reduce cognitive load without weakening any invariant.
- **Scope as Release 2** (domain‑spec + data‑model + persistence touch), unless the owner wants D1/D2 in an R1.x — in which case the panel presentation is the only R1 surface and the enum change gates it.
- The two decisions are **separable**: D2 (single‑action resolution) can be adopted independently of D1 (it works with or without `acknowledged`), and D1 independently of D2.

**Status.** Proposed — Review complete; **owner Decision pending**.

## 4. Realization artifacts (non‑binding, for evaluation)

- **Prototype B** — `90_research/design_artifacts/oslo_r1_proposed_findings_lifecycle.html`: the R1 prototype with D1 + D2 applied, for the owner to *feel* the flow. Non‑canonical; informs, does not bind.
- The shipped reference prototype (`product-design/…mockup_v2.html`, PR #116) is **canon‑compliant** (retains `acknowledged` + multi‑step) and does not depend on this proposal.

## 5. On ratification (owner)

If adopted: number this decision (`python3 tools/dl_records.py next`), stamp the `DL-…-finding-flow-simplification` record **Ratified**, then route the realization (spec + enum + panel + prototype + baselines) as normal repository changes with traceability.

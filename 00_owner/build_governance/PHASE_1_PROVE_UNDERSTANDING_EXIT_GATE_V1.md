# Phase 1 "Prove Understanding" — Falsifiable Exit Gate (V1)

**Status:** **RATIFIED — DL-070 (2026-06-18).** Owner-ratified build policy; binds engineering. The §4 values are owner-set and ratified (Framework 001A: AI recommended the harness; the owner ratifies intent — ratify ≠ author). Engineering authors the realizing test harness.
**Date Ratified:** 2026-06-18 · **Ratifying decision:** DL-070 (CHG-100). **Authorizing directive:** DL-059 (P-4 falsifiable-criterion ruling).
**Date Drafted:** 2026-06-16
**Layer:** Implementation Spec / Delivery governance — Phase 1 sign-off gate. No doctrine/constitution change.
**Zone:** `00_owner/build_governance/` — owner-ratified build policy that **binds** engineering. CODEOWNERS co-review: `@idris-manley` (ratifies) + `@mkashifse` (engineering reviewer; sets the sign-off date).

---

## 0. Scope and phase identity

This gate governs **Alpha Phase 1 — Prove Understanding Generation** (`10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` §19: Evidence → Planning Synthesis → Artifact Workspace → CAF → Confidence → **Fast Pass**). It is **not** the engineering "Phase I — Foundation & Environment" (which has its own day-1 exit checklist). It covers the **Fast Pass only.** Deep Pass, CAF Overlays, Issues, and Recommendation *improvement* belong to **Alpha Phase 2 — Prove Improvement Loop** and must **not** gate Phase 1. The whole-Alpha §20 graduation metrics (50+ users, engagement %, etc.) are **Beta-advancement outcome** criteria, **not** a build sign-off gate, and must **not** be pinned to the engineering sign-off date.

---

## 1. Single pass/fail line

> **Phase 1 PASSES if and only if** — over the **version-pinned evaluation corpus** (§3) — a **Fast Pass** run satisfies **every** Required Condition in §2 for **> 90%** of corpus projects, **with zero occurrences of any FAIL Trigger in §2.B.**
> **Phase 1 FAILS** if any single Required Condition falls below its threshold, **or** any one FAIL Trigger occurs. **There is no partial sign-off.**

---

## 2. Conditions

### 2.A Required Conditions (measurable; each maps to a canonical Acceptance Criterion)

Source: `30_engineering/analysis_engine/ACCEPTANCE_CRITERIA.md`; Master Spec §20.

| # | Condition (Given a corpus project, When a Fast Pass completes, Then…) | Threshold | AC |
|---|---|---|---|
| G1 | exactly **one** `CAFState` and **one** `ConfidenceState` exist for the run | 100% | AC-F1 |
| G2 | **CAF and Confidence are generated** for the analyzed project | 100% | §20 |
| G3 | ≥1 `Finding` exists with `status=detected`, each carrying **≥1 `evidence_link`** | 100% | AC-F2 |
| G4 | `Recommendation`s exist with `status=generated`, each referencing a `finding_id` | 100% | AC-F3 |
| G5 | Confidence is **reliability-qualified** (no bare value) | 100% | AC-F5 |
| G6 | project reaches `oriented`; orientation labelled **non-final** | 100% | AC-F4 |
| G7 | project is **successfully synthesized** (no synthesis failure) | **> 90%** | §20 |
| G8 | **Time-to-First-MRI** within the latency line | **p50 ≤ 25s / p95 ≤ 50s**, **< 60s** hard ceiling, at the **Tier-1 envelope** (§4) | AC-L1 |
| G9 | basis is **resolvable without recomputation** for every Finding, Recommendation, ConfidenceState | 100% | AC-T1–T4 |

### 2.B FAIL Triggers (any single occurrence fails the gate)

| # | Trigger | AC |
|---|---|---|
| F-1 | a **governance / Accepted-Understanding / execution / orchestration** artifact appears anywhere in the workflow | AC-S1 |
| F-2 | Fast output is **stored or presented as final** understanding | AC-S3 |
| F-3 | a `Finding` exists with **no resolvable evidence link** | AC-F2 |
| F-4 | an LLM output **introduces a formula / weight / percentage / threshold or a bare confidence value** | AC-V3 |
| F-5 | a publication is **not atomic** (partial outputs committed) | AC-FAIL4 |

---

## 3. Evaluation corpus

A **version-pinned, owner-approved corpus of N ≥ 20 in-envelope projects** (within the Tier-1 envelope, §4), representative of R1 intake (Upload / Describe / Start From Template per DL-056). The corpus and its expected-output fixtures are frozen at a tagged commit; the gate is evaluated against that tag.

---

## 4. Owner-set values (ratified DL-070)

The four values that previously made the criterion unfalsifiable are now owner-set and ratified. Engineering scaffolds the metric/harness; these numbers are canon.

1. **X% — corpus pass rate (G7 + the §1 aggregate line): `> 90%`.** Matches the Master Spec §20 "Synthesized > 90%" baseline. G1–G6 and G9 remain at **100%** (structural invariants).
2. **N — corpus size: `≥ 20` in-envelope projects**, owner-approved and version-pinned, spanning the three R1 intake modes (Upload / Describe / Template, DL-056).
3. **G8 latency: `p50 ≤ 25s / p95 ≤ 50s` under the ratified `< 60s` ceiling, at the Tier-1 envelope.** Percentile split per DL-046 register **A2** (p50 ≤ 25s / p95 ≤ 50s); Tier-1 envelope per register **A1** (≈ 20 artifacts / 50k words / 1 active project). **Validation note:** with the internal Gemma local model now primary (DL-069), local-inference latency is unproven against this line — Kashif validates G8 against a live Gemma Fast-Pass run before pinning the sign-off date; if local inference cannot meet p95 ≤ 50s, that is a fast-follow amendment to this value, not a relaxation made in advance.
4. **Determinism (D1): deferred to the Phase 2 "Prove Improvement" gate.** Bounded-equivalence tolerance (register D1) remains owner-open and is **not** part of this Phase 1 gate, to avoid re-blocking on an unsettled tolerance.

---

## 5. Status & resulting actions

Ratified as **DL-070** (2026-06-18): the owner set §4 and ratified this gate; the decision is recorded in `00_owner/decisions/records/DL-070-…md` + changelog CHG-100; the engineering Phase 1 sign-off note (`note_to_eng_phase1_signoff` — a Founder Console artifact, external to this repo) references this gate. **Remaining action:** Kashif (`@mkashifse`) (1) validates G8 latency against a live Gemma Fast-Pass run, then (2) pins the revised Phase 1 sign-off date to this gate. Supersedes: none — resolves the open P-4 action item under DL-059. The prior "DL-060" proposal/stub drafts are **void** (DL-066) and are not part of canon.

---

*Ratified canon (DL-070). Phase 1 "Prove Understanding" Fast-Pass sign-off is evaluated against this gate; no sign-off against an undefined criterion.*

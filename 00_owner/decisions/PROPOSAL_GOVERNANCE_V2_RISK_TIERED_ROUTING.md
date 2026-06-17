# Proposal — Governance v2: Risk-Tiered Routing (v1.1, Decision-ready)

**Type:** Framework 001 Proposal — **Class A / canon** (amends how Framework 001 routes work). Full owner ratification; no lazy/expedited path.
**Date:** 2026-06-15 · **Rev:** v1.1 (folds in `REVIEW_GOVERNANCE_V2_RISK_TIERED_ROUTING.md`).
**Author role:** AI contributor (proposes realization; owner ratifies intent — Ratify ≠ author).
**References:** Framework 001/001A (DL-030/031); zones DL-051; `code/` non-canonical DL-057; DL-053; `ANTI_ASSUMPTION_BUILD_PROTOCOL`; CODEOWNERS / branch protection; `OSLO_DEV_READINESS_MONITOR.md` (Decide lane); PR #21 + Issue #24 (worked examples).

> **Governance caveat.** Recommends; does not ratify. Being a canon change, it routes through the full Framework 001 lifecycle and is ratified only by the owner.

### What changed in v1.1 (from the Review)
Added the **delegation safety rail** the Review flagged as the missing 20%: a **classifier + audit** (#1), a **reversibility test** and bounded "lightweight review" (#3), **lazy-consensus guardrails** (#4), **CODEOWNERS scoping** (#5), gate red-proof staged as a **Class-D precondition** (#2), table-drift ownership (#8), and a corrected **role model** (#6/#7): post-v2 **owner = governance owner + product lead; EM = Hamza; developer = Kashif** (separate seats — no one approves their own code).

---

## 1. Problem
The process gates **every** change at ~the same weight and keeps the owner in the loop for both *ratifying intent* (rare, owner-only) and *approving realization* (frequent, engineering's). Single-person bottleneck; the cost is mostly context-switching. PR #21: of all its owner touchpoints, only **UP-3** was irreducibly owner-only. **Objective:** cut the owner's decision surface without weakening enforcement of what engineering may do.

## 2. Principle
Route by **stakes = zone × reversibility**. Owner ratifies the irreducible core; the **EM** approves engineering realization behind **automated gates**; only **exceptions** reach the owner, cleared in one **weekly** pass. Enforcement is a **gate**, not the owner's eyes.

## 3. Roles & seats (post-v2)
- **Owner (Idris)** — **governance owner** (Class A canon ratifier) **+ product lead** (Class C authority). **Not the EM.**
- **EM (Hamza)** — **engineering realization approver** (Class D), independent of **both** the owner and the author. This is the seat v2 leans on.
- **Developer (Kashif)** — **authors / proposes** engineering realization; his work is **EM-approved (by Hamza) behind green gates**. He proposes; he does not self-approve.
- **Consequence (resolves Review #6/#7):** engineering realization now has an **independent human approver (the EM — separate from both owner and author) *and* the gates**. The owner is no longer the sole check, and no one approves their own code. Product realization (Class C) is the owner's call *as product lead* — lighter than canon, but still the owner's; the time savings come from Classes D (EM), E (pre-authorized), B (lightweight), and exception-batching, not from removing the owner from product.

## 4. Change-classification model
Classify once, then route:

| Class | What | Zone | Approver | Record | Owner |
|---|---|---|---|---|---|
| **A — Canon** | Doctrine, Constitution, architecture baseline, product guardrails, ontology/DL-053, precedence, the governance process | `00_owner` | **Owner ratifies** — full Framework 001 | DL + changelog | **Ratify** |
| **B — Co-governed seam** | Contracts, interfaces, traceability | `20_handoff` | **Owner ratifies — lightweight review** | DL / seam log | **Ratify (light)** |
| **C — Product realization** in guardrails | Feature/spec choices inside approved product canon | `10_product` | **Owner as product lead** (not canon ceremony) | product changelog | **Decide (product-mode)** |
| **D — Engineering realization** | Code, in-zone ADRs, tests, build — no canon touched | `30_engineering`/`code/` | **EM (Hamza)** behind green gates (author: Kashif) | PR + app changelog | **None** (exception only) |
| **E — Operational / reversible** | Dep bumps, CI/gate upkeep, infra within policy | non-canon | **Pre-authorized** | log / PR | **None** |

## 5. Classifier + audit (Review #1 — the bypass guard)
- **Who tags:** the proposer tags a class; the **approver of record** (EM for D/E, owner for A/B/C) confirms it.
- **Automated guard (machine, not trust):** a gate check maps **changed paths → minimum class** — any diff touching `00_owner` (canon) or a `20_handoff` contract **cannot** be ratified as C/D/E and is force-escalated. Misclassification is caught by the gate, not by the owner noticing.
- **Default:** *when in doubt, the higher class wins*; genuine ambiguity is an Anti-Assumption escalation.
- **Class is a field of record** (PR label + changelog), and the owner **sample-audits** delegated (C/D/E) changes in the weekly pass.

## 6. Reversibility test + "lightweight review" (Review #3)
- **Reversible** = undoable by a **single revert PR** with **no data loss, no irreversible external side-effect** (no publish/send/spend/un-rollback-able migration), and **no change to a ratified contract or canon**. Anything failing this is **not** reversible → not Class E and not lazy-consensus-eligible.
- **Lightweight review** (Class B) = **one named reviewer** (the seam counterpart) + a **fixed checklist** (contract honored, traceability intact, no canon touched) + **single pass** (no multi-round).

## 7. Standing pre-authorizations
One-time ratified rules, each with a boundary + escalate-if:
- **Security/patch dependency bumps** (the form-data / Issue #24 case) — pre-approved within a fixed major. *Escalate if:* major or API-breaking.
- **In-zone ADRs** (scoped wholly within `code/`/engineering) — EM-approved, owner notified. *Escalate if:* affects a `20_handoff` contract or canon.
- **CI/gate maintenance** that doesn't loosen a canon invariant. *Escalate if:* a gate's enforcement strength drops.
All limited to **reversible** items per §6.

## 8. Enforcement by gate + its limits (Review #2)
Gates are the enforcer; deviation goes **red automatically**:

| Canon enforced | Gate |
|---|---|
| Zone/path rules, structure, cross-refs, terminology (DL-053), **the §5 path→class guard** | doc-integrity gate |
| Spec ↔ build linkage | app-ci gate-2 |
| Build / contract / tests / epistemic invariants / observability / security | app-ci gates 1–6 |
| Never-push-to-main; canon paths owner-only | branch protection + CODEOWNERS (§9) |

**Stated limit (no over-claim):** doctrinal/architectural *judgment* and product-fit are **not** machine-checkable. Those are caught by Class A/B human review + the owner's weekly **sample-audit**, not by a gate. Any canon rule that *is* checkable but isn't yet encoded is a backlog item.
**Sequencing gate:** because v2 makes gates load-bearing, **full Class-D delegation is staged behind the per-gate red-proof** (PR #21 item 2). Ratify the model now; flip D to "owner: none" only once each gate is proven to fail-when-it-should.

## 9. CODEOWNERS scoping (Review #5)
- **Owner-required** review on `00_owner` (canon) and `20_handoff` contracts.
- **EM-required** review on `code/` and `30_engineering`.
- **Dependency:** verify the **live** CODEOWNERS reflects this before delegating Class D (today it may require the owner on all paths — that would contradict Class D and must be re-scoped first).

## 10. Exception inbox + lazy consensus (Review #4)
- **Owner inbox = four things only:** a red gate needing a ruling, a canon conflict (C-pattern), an Anti-Assumption escalation, and Class A/B proposals. The **Dev Readiness Decide lane** is this inbox.
- **Lazy consensus** (reversible implementation-tier nods only): auto-adopted **unless objected in the weekly session**; eligible **only if** reversible (§6) **and** non-gate-affecting **and** touches no `20_handoff` contract **and** not Class A; recorded `lazy-ratified` with the window; **revert path = single PR** if later found wrong; the owner may pull any item into explicit review at any time.
- **Batch, don't interrupt:** clear the queue in one weekly governance pass.

## 11. Preserved (unchanged)
Canon/doctrine ratification; precedence ladder; conflict adjudication; the DL/changelog audit trail; Anti-Assumption; never-push-to-main; owner-only CODEOWNERS on canon paths. v2 shrinks the surface the **owner** gates, never the system's memory or enforcement.

## 12. Tradeoffs (honest)
Realization approval moves to the **EM (independent of the owner) + gates**, so reversible engineering mistakes may land and be corrected rather than prevented up front — the right trade for the engineering zone, never for canon. Concentration risk is **materially reduced vs. v1.0** because the EM is a separate seat; the residual is that gate integrity is now load-bearing (hence §8 sequencing). Periodic governance retro recommended.

## 13. Build sequencing
| Stage | Delivers |
|---|---|
| **1 — Ratify model + rail** | 5-class table, classifier+audit (§5), reversibility test (§6), pre-auths (§7), lazy guardrails (§10) → DL entries + Framework 001 amendment. |
| **2 — Scope + prove gates** | Re-scope CODEOWNERS (§9, verified live); land the per-gate red-proof; encode/​backlog the path→class guard and any checkable canon rule. |
| **3 — Flip delegation + wire inbox** | Class D → "owner: none"; Decide lane = governance inbox; weekly batch session; `lazy-ratified` status live. |

## 14. Requested owner decisions
1. Adopt the **5-class model** (§4) and the **role model** (§3: owner = governance + product lead; EM = Hamza; developer = Kashif).
2. Ratify the **classifier + audit** (§5), incl. the automated path→class guard.
3. Ratify the **reversibility test** + lightweight-review definition (§6).
4. Ratify the **standing pre-authorizations** (§7).
5. Approve **lazy consensus** with the §10 guardrails (Class A excluded).
6. Authorize **CODEOWNERS re-scoping** (§9) and confirm the **gate red-proof as the Class-D precondition** (§8).
7. Assign the **classification-table owner** (drift control, Review #8).

## 15. Traceability & Status
Derived from: owner request (2026-06-15) + role clarification; `REVIEW_GOVERNANCE_V2_RISK_TIERED_ROUTING.md`; PR #21 + Issue #24; DL-030/031/051/053/057.

**Status: Decision-ready**, conditioned on three external confirmations that don't change the text: (a) **Hamza accepts the EM seat** + gives independent Findings/Concerns (Kashif, as author, provides the gate red-proof); (b) **live CODEOWNERS** verified/re-scoped (§9); (c) **gate red-proof** scheduled as the Class-D flip precondition (§8). The model itself may be ratified now; Class-D delegation activates at Stage 3.

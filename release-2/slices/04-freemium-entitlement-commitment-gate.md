# R2 Slice 4 — Freemium: Entitlement, Commitment Gate, Outcome-Unit, Archive — Build Design

*Grill artifact · 2026-08-06 · DRAFT — awaiting slice sign-off. Derived from DL-201 (Outcome above Plan), DL-202/DR-3 (commitment gate, ENFORCE), DL-198 (freemium value moments; renumbered from DL-172), DR-7 (Basic $29/mo flat, Pro $79 provisional), capabilities #16/#11, audit §4.4 (F1…F13) + landmines DL-L1/L2/L3, and the prototype freemium block.*

**Scope:** the entitlement/tier model (Free = 1 active outcome), the commitment gate (block → named capability + price → real hosted checkout → grant), Outcome as the metered object with Plan as container, reversible self-service archive/reactivate, and the durable intent-signal stream. **Central correction (audit F2 = DL-L1):** enforcement is REVERSED from the audit's original "observe" — DL-202/DR-3 supersede DL-198's "nothing gated in Alpha," re-aligning R2 with R1's 422/checkout canon, which is therefore NOT superseded now.

## 1. Locked decisions
| # | Decision | Source |
|---|---|---|
| L1 | **Outcome is the first-class, persisted, metered object.** Hierarchy: Workspace → Plan → Outcome. | DL-201 §1; cap #16 |
| L2 | **Free = 1 active Outcome : 1 Plan**; Basic+ = N outcomes/plan and N plans. | DL-201 §2; DL-198 §2 |
| L3 | **Enforcement = ENFORCE via commitment gate** (Alpha): block → named capability + price → commit-to-pay (real card) → grant. | DL-202 §1; DR-3 |
| L4 | Reverses the audit's "observe": DL-202 **supersedes** DL-198's "nothing gated"; **re-aligns** R1 422/429/checkout (now live). | DL-202 §2; DL-L1 |
| L5 | **Gate CAPACITY only** — 2nd outcome, 2nd plan, bigger intake envelope, auto-import, continuous monitoring. | DL-202 §3 |
| L6 | **NEVER gate** the record, reviewer/CRR loop, Viewers, or judgment quality. The never-metered exemption list. | DL-202 §4; DL-L2; DR-7 |
| L7 | **Archive/reactivate = reversible, self-service, record-stays-viewable** — NOT R1's terminal admin-gated archive. | DL-201; DL-198 §3; DL-L3 |
| L8 | **Basic = $29/mo flat per account** (annual $290/yr); **Pro = $79/mo PROVISIONAL** (`ph:true`). Flat, never per-seat. | DR-7 |
| L9 | **Intent-signal event stream** (which wall, when, chosen path) = durable demand data feeding #15. | DL-202; cap #16; F5/F6 |
| L10 | **Ingest limits content-metered** (extracted words vs Free ~50k); file rails loose config. | F11 |
| L11 | **Price is config**, blocks copy/launch, never the build. | DL-202 §5; DR-7 |

## 2. State Model
**Outcome:** `active` (occupies the tenant's active slot; Free = exactly 1; metered) ↔ `archived` (self-service, reversible, **record stays fully viewable**, frees the slot, **never metered**). `active→archived` (`archiveOutcome`); `archived→active` (`reactivateOutcome`, guarded by slot availability — F10). Nothing deleted (contrast R1 terminal `Project:archive`, DL-L3).
**Entitlement enforcement-mode** (workspace-scoped): `enforce` (Alpha ships this — capacity check blocks, shows capability + price, requires commit, grants) vs `observe` (config value only, not the Alpha default).
**Checkout funnel** (re-aligned with R1 `upgrade_page_viewed→started→completed`): `gate_hit` → **pending** (`_openCheckout`, real card capture) → **committed** (`_commitPay` → `CommitmentLog`) → **granted** (`_TIER` raised). Decline → back to `gate_hit`, intent still logged. Full subscription lifecycle (proration/dunning/self-serve) deferred.

## 3. Data / Object model
- **Outcome** `id · plan_id · workspace_id · title · status{active,archived} · is_primary · provenance{declared,inferred} · created_at · archived_at?`. The record (findings/attestation/integrity history) hangs off it and is **never gated by status**.
- **Plan** (container) `id · workspace_id · title · outcomes[]`. Free = 1 Plan; active-slot invariant at workspace level. Resolves the F13 "plan" naming collision (document container vs subscription).
- **Entitlement/Tier** (F1) `workspace_id · tier{free,basic,pro} · enforcement_mode=enforce · grants{max_active_outcomes · max_plans · intake_word_envelope · auto_import · continuous_monitoring · report_scheduling} · never_metered_exemptions[]=[record, reviewer_loop, CRR, viewers, judgment_quality]`. Exemption list is a first-class field asserted by tests (F9/DL-L2). Free grants: `max_active_outcomes:1, max_plans:1, envelope:~50k`.
- **CommitmentLog** (F2) `id · workspace_id · gate_key · tier · price · placeholder · ctx · committed_at`. One row per real commit — the primary Alpha monetization signal.
- **IntentSignal** (F5/F6) `id · workspace_id · wall_key{multiOutcome,multiPlan,envelope,schedule} · tier_mapped(internal) · chosen_path{committed,free_path,declined,keep_both} · full_option_set[] · ctx · ts`. **Every branch emits** (fixes the missing denominator). `tier_mapped` internal-only (neutral-copy).

## 4. Event Model
| Event | When | Consumers |
|---|---|---|
| `gate_hit` | capacity check blocks (`_payGate` enforce) | IntentSignal; funnel |
| `intent_signal` | user chooses any branch | demand analytics (#15) |
| `checkout_started` | `_openCheckout` (card capture begins) | checkout funnel (R1-aligned) |
| `checkout_committed` | `_commitPay` succeeds | CommitmentLog; grant |
| `entitlement_granted` | tier raised | entitlement store |
| `outcome_archived` / `_reactivated` | self-service, never metering/gate | slot state; roll-up |

Flow: `gate_hit` → `intent_signal` (always) → if commit: `checkout_started` → `checkout_committed` → `entitlement_granted`. Archive/reactivate independent, self-service, never emit metering; archive is not a grounding act and never touches the read.

## 5. Honesty invariants (testable)
- **INV-1 never-metered exemptions** — reading a record, routing to a reviewer, adding a Viewer all succeed at `free` with zero `gate_hit` (DL-L2; DR-7 "reviewers/Viewers free forever").
- **INV-2 archive-reversible-record-viewable** — archive→reactivate restores with nothing deleted; record readable in both states (DL-L3).
- **INV-3 gate is capacity-only never quality** — integrity output byte-identical at `free` vs `basic` for the same plan (DL-202 §4).
- **INV-4 neutral→now-priced copy** — with DR-7 the gate names tier + price ($29/mo); Pro renders a `placeholder` tag. Failing case = a *missing* price at an enforced wall.
- **INV-5 intent-signal captured every branch** — 4 branches → 4 rows with distinct `chosen_path` (computable denominator).
- **INV-6 commit is a real card, never a silent bypass** — no path raises `_TIER` without a `CommitmentLog` row.
- **INV-7 content-metered ingest** — one small over-envelope file trips `envelope`; ten tiny in-envelope files do not.

## 6. FE↔BE integration bindings
| UI (proto fn) | Trigger | BE contract |
|---|---|---|
| Commitment-gate modal (`_payGate`) | 2nd outcome/plan/envelope/schedule | `GET /entitlement`; if blocked, return named capability + price (config); emit `gate_hit`+`intent_signal` |
| Checkout (`_openCheckout`→`_commitPay`) | "commit to pay" | hosted checkout captures real card; on success raise tier + write CommitmentLog; `POST /commitments` |
| Outcome-cap wall (`vmOutcomeCap`) | add outcome/plan at cap | `POST /outcomes` returns **422** at cap in enforce (drives the gate — never a silent 422); or free path `outcome_archived` |
| Archive/reactivate (`vmArchiveSwitch`/`reactivateOutcome`) | "Archive to switch (free)" / "Reactivate" | `POST /outcomes/{id}:archive`/`:reactivate`; reversible, record stays viewable; guard reactivate when slot full |

## 7. R1 reuse vs net-new
**Reuse (re-aligned — DL-202 restores R1 gating canon):** the 422 gating apparatus (now drives the outcome-cap gate, not superseded); 429 caps + the upgrade/checkout funnel; the telemetry envelope/`analytics_events` pipeline; tenant/Principal/auth primitives host the Entitlement object.
**Net-new (F1/F3/F4/F5):** Outcome-as-unit (reversing R1 "Intend do-not-add"); reversible outcome-level archive; the enforce-mode entitlement contract + never-metered exemption list; the every-branch intent-signal stream.

## 8. Open items / placeholders
- **Pro price provisional** ($79, `ph:true`); nothing gates to Pro in R2 (its value line is post-R2); consider $79→~$69 (DR-7).
- **Exact envelope numbers** (~50k-word Free, 10-file/10-MB rails) = entitlement config placeholders.
- **Subscription lifecycle deferred** (proration/dunning/self-serve/annual mechanics).
- **Checkout provider** selection (Stripe-style assumed).

## 9. Acceptance criteria
1. A **2nd active outcome** at `free` blocks, shows "Optimize all your outcomes · Basic · $29/mo", requires commit-to-pay through **real hosted checkout** before granting — **never a silent 422**.
2. A 2nd plan and exceeding the intake envelope hit the same gate with the correctly named capacity capability.
3. The **record, reviewer/CRR loop, and Viewers are never metered** (zero `gate_hit` at `free`).
4. **Judgment quality identical across tiers** (integrity output byte-identical `free` vs `basic`).
5. **Archive → record still readable; reactivate → restored**, nothing deleted, self-service.
6. Reactivate **when the slot is full** is guarded (archive-to-switch offered, not a broken state).
7. **Every wall branch** emits one `intent_signal` with a distinct `chosen_path`.
8. A real commit writes a `CommitmentLog` row and raises the tier; **no grant without a commitment row**.
9. The gate **names tier + $29/mo** and renders Pro with a `placeholder` tag; enforcement-mode = enforce.
10. Ingest is **content-metered** — one over-envelope file trips `envelope`; many small in-envelope files do not.

*The enforcement reversal is the load-bearing correction: the audit (DL-L1/F2) recommended enforce→observe; DL-202/DR-3 reverse that — 422/checkout is now live, not superseded. Copy rule also inverted (DR-7 names the price). The prototype already implements the reversed model; the every-branch intent-logging gap (proto only logs keep-both) is net-new (INV-5).*

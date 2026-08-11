# Governance Proposal — Framework 002: Release Lifecycle & Change Control

- **Status:** ✅ **RATIFIED 2026-08-09 by Idris → DL-212** (establishes **Framework 002**; dev-lead Hamza aligned on push-via-PR delivery + convention enforcement). This proposal is the review record. AI drafts; the owner ratifies (Framework 001).
- **Class:** A (governance doctrine — a process framework, companion to Framework 001).
- **Basis:** owner directive 2026-08-09 — R2 is delivered to dev and **frozen** from a product-design perspective; R2.x begins as **refinements** dev absorbs while building. Need a systematic, enforced structure to govern releases and protect build integrity across the product↔dev seam.
- **Relationship:** **Framework 001** governs a single *decision* (backlog → proposal → review → decision → change → changelog). **Framework 002** governs a *release's lifecycle* and, immediately, **change control over a frozen release**. F002 invokes F001 for every decision it produces; it does not replace it.
- **Placement:** staged in `release-2/`; intended canonical home `00_owner/frameworks/framework_002_release_lifecycle.md` (process doctrine, not product canon) — lands at the next graduation or by direct owner ratification into main, owner's call.

---

## 1. Problem

R2 is frozen and handed to dev, but refinement continues (DL-206…211, Slice 10, GT-34…GT-56, and prototype fixes all landed *after* the 2026-08-06 freeze). Today that flows through Framework 001 decision-by-decision, with no standing structure that (a) records the frozen baseline, (b) classifies each post-freeze change by its impact on the dev contract, (c) gives dev one authoritative "what changed since freeze / what to absorb" view, or (d) guarantees refinements never regress the doctrine spine. Without that, product refinement and an in-flight build silently diverge.

## 2. The lifecycle (the phase machine)

Every release passes through phases, each with an **entry gate**, **exit gate**, **owner**, and **required deliverables**:

**Open → Design → Freeze → Handoff → Build → Graduate → Retire.**

For **R2.x specifically**, R2 is already past *Handoff* and in *Build*; R2.x lives entirely in the **Build phase under Change Control** (§3–§5). The Open/Design/Graduate machinery is defined here in skeleton for the next full release and fleshed out when first needed — *don't build ahead of need*.

## 3. The frozen baseline — the Freeze Manifest

Freeze produces a **Freeze Manifest** (`release-2/R2_FREEZE_MANIFEST.md`): the exact state at handoff — the signed slice set, the GT acceptance register at freeze, the reference-prototype md5, the ratified decision set, and the backend-capability count. It is the immutable reference every post-freeze change is measured against. R2's baseline = the 2026-08-06 nine-slice sign-off (`_S10` 59 / GT-01…GT-33).

## 4. Change classification (the core discipline)

The **dev handoff contract** = the signed slices + the GT acceptance register + the FE↔BE integration map (interfaces) + the reference prototype's behavioral invariants. Every post-freeze refinement is classified by its impact on that contract, and **nothing lands without a classification**:

| Class | Definition | Ceremony | Dev impact |
|---|---|---|---|
| **Neutral** | Touches only prototype presentation/copy that maps to no GT and no slice behavior, or a doc outside the handoff package | Log it; dev may pull the updated oracle | None — nothing dev builds changes |
| **Additive** | Adds a new slice, new GT(s), or a new decision that **extends** the contract without invalidating signed work | Log it + a **handoff-delta** entry | Dev absorbs new scope; existing build stands |
| **Altering** | Changes an existing signed slice's behavior, changes/removes a shipped GT, or changes an interface | **Impact assessment + explicit re-handoff + owner sign-off** before it lands | In-flight work may need rework |

**Delivery is push, via labeled PRs (dev-lead preference, 2026-08-09).** Every refinement lands as a PR carrying its class as a label — `neutral` / `additive` / `altering` — so GitHub's own review/notification machinery enforces the gate:
- `neutral` → owner merges after the green doc-integrity gate; dev auto-notified (FYI), non-blocking.
- `additive` → review *requested* for awareness (the new scope is on dev's radar), but non-blocking — owner may merge.
- `altering` → **the dev lead's PR approval IS the re-handoff sign-off**; the owner does not merge until it's approved, with the impact assessment attached to the PR. **Enforcement: convention to start** (owner discipline — no `altering` PR merges without the dev lead's approval), owner + dev-lead aligned 2026-08-09. A GitHub Action that hard-fails an `altering` PR lacking a dev-team approval is deferred until a miss warrants it.

This one rule — *altering doesn't merge without dev approval* — is what protects build integrity across the seam, and it rides the existing `branch → PR → gate → owner merge` flow rather than adding a parallel process.

**Draft → owner-confirms → capture.** Refinements iterate freely on the prototype (a draft phase). **Nothing is classified, logged, or PR'd until the owner explicitly confirms the use case is complete** — work-in-progress is invisible to the release process. The owner's confirmation is the gate (it carries the criteria — self-contained, no open sub-decisions); the one objective check, `_S10` green on clean load, runs automatically at capture, not as an owner checklist.

**Front-end ↔ back-end synchronization — the use case is the unit.** A prototype simulation is a promissory note for backend behavior, so **the back-end specification required to support a simulation is designed as part of the same use case's prototyping — never deferred.** Capturing a use case that adds/changes a simulation must synchronize its backend obligation in the same pass: **SIM-tag** the behavior (`/* SIM:#NN */`), register/extend the **backend-capability register**, source every new simulated **value** in **Demo-Config**, and extend the **slice / build-spec** that realizes it. A simulation is never captured without its backend obligation — this keeps the prototype (the reference oracle) and the backend spec from drifting, so dev never inherits a simulation with no spec behind it. Extends the standing *prototype-simulation ⇒ backend-obligation* rule + the `demoSimsTagged` gate.

## 5. The Refinement Ledger (dev's single source of "what changed")

A running `release-2/R2_REFINEMENT_LEDGER.md` — every post-freeze change as one row: *date · what · class (neutral/additive/altering) · PR # + label · DL/RB it traces to · guard delta · reference-prototype md5 after · dev-absorb note*. It **mirrors the merged-PR stream** (each row generated from its labeled PR), so it's a changelog nobody maintains by hand — the PR is the push, the Ledger is the durable index. Dev's day-to-day is the PR notifications; the Ledger is the "everything since freeze" view for onboarding or audit.

## 6. Durable invariants (carried forward, never regressed)

Split the guard set into two tiers. The **Durable Invariant Registry** — the doctrine spine (only-reanalysis-resolves, only-verify-moves-Grounding, maturity-not-forecast, capacity-gated-not-judgment-quality, level≠trust, the manufactured-confidence prohibition, decomposability/single-hue) — is **re-asserted in every release's harness and can never go red or be removed**, in any release. Release-acceptance guards are scoped to their release. Every guard carries its doctrine anchor. This is what stops R2.x (or R3) from eroding what R2 established.

## 7. Traceability chain (a freeze/land gate, not a hope)

Enforce the chain as a checkable gate: every build artifact → a ratified decision → a backlog item; every guard → a doctrine anchor; every demo value → a Demo-Config source. "Chain complete" becomes a gate check, using what already exists (GT→DL, SIM tags, Demo-Config register).

## 8. Realization — skills that operationalize the phases

- **`release-refine`** (build now) — classify a refinement (§4), append the Ledger row, update the Freeze Manifest deltas, and — for *altering* — require the impact assessment before proceeding. Enforces the change-control discipline every time.
- **`guard-add`** (build now) — author a new honesty invariant *consistently*: `_S10` oracle + GT twin + doctrine anchor + register row (so guards never drift in form; tags each Durable vs release-scoped).
- **`product-freeze`** / **`release-open`** / **`graduate`** — defined in F002, built when the next full release reaches those phases.

These sit alongside the existing design-phase skills (oslo-product-grill, oslo-journey-audit, oslo-ux-optimizer), which produce content; F002's skills govern the lifecycle.

## 9. Retroactive seed — R2.x refinements to date (2026-08-09)

The framework is validated against the real post-freeze changes this session, which become the first Ledger entries:

| Change | Class | Traces to | Guard delta |
|---|---|---|---|
| Slice 10 engine + load-bearing/classification model | Additive | DL-209 | GT-34…GT-44 |
| CAF boundaries + deterministic structural-target assignment | Additive (amends main CAF at graduation) | DL-210 | GT-45…GT-50 |
| Proposal-resolution model + cross-surface sync + itemized findings | Additive | DL-211 | GT-51…GT-55 |
| Start-here guides cleared-worklist/pending state | Neutral→Additive (added a guard) | (prototype fix) | GT-56 |
| Execution-monitoring tier split · Pro program/$79 · plan-export tiering | Neutral (pricing/tier canon; no build-contract change) | DL-206/207/208 | — |
| Export rebuild · masthead · read-reflow · terminal card · dim-derivation | Neutral→Additive | (prototype UX passes) | various |

None was *altering* (no shipped GT changed or was removed; no signed slice's behavior was reversed) — which is why dev's in-flight work stands. That is exactly the property F002 makes visible and enforceable going forward.

## 10. Review (five outputs — Framework 001)

- **Findings.** The machinery exists (F001, guards, zones, doc-integrity, sign-offs, reconciliation catalog) but isn't composed into an enforced lifecycle; post-freeze change is ungoverned as a class.
- **Concerns.** Over-ceremony risk — mitigated by the three-tier classification (neutral changes stay near-zero ceremony). Retroactive seeding is a reconstruction — owner confirms the classifications.
- **Dependencies.** Framework 001; the `_S10`/GT register; the Demo-Config register; DL-051 ownership zones; the reconciliation catalog (graduation phase).
- **Recommendation.** Ratify Framework 002 with the Build-phase change-control track (§3–§7) fleshed out and the other phases skeletal; build `release-refine` + `guard-add` first; seed the Ledger with §9.
- **Status.** ✅ RATIFIED 2026-08-09 → DL-212. Delivery = push-via-labeled-PR; `altering` gate = dev-lead approval (convention to start). Realization: DL-212 record, framework doc (staged), seeded Freeze Manifest + Refinement Ledger, and the `release-refine` + `guard-add` skills.

## 11. Open for ratification

1. The **phase machine** (§2) as the release lifecycle.
2. The **Freeze Manifest** + the **three-class change model** (§3–§4) and the *altering ⇒ impact-assessment + re-handoff* gate.
3. The **Refinement Ledger** as dev's authoritative post-freeze changelog (§5).
4. The **Durable Invariant Registry** tier (§6) — re-asserted every release, never regressed.
5. Building **`release-refine`** + **`guard-add`** first (§8); seeding the Ledger with this session's refinements (§9).

---

_AI-drafted (Framework 001). On ratification: create the DL-212 record, author `00_owner/frameworks/framework_002_…` (staged), generate `R2_FREEZE_MANIFEST.md` + `R2_REFINEMENT_LEDGER.md` (seeded), and build the `release-refine` + `guard-add` skills._

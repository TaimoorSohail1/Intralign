# Review — Governance v2: Risk-Tiered Routing (pressure-test)

**Type:** Framework 001 Review (five outputs — analysis & recommendation; non-canonical, does not ratify).
**Date:** 2026-06-15
**Reviewer role:** AI contributor. **Independence caveat:** this is a *self*-Review — same author as the proposal. It is a pressure-test, not an independent check; pair it with the engineering lead's independent Findings/Concerns (requested in `note_to_eng_governance_v2.md`) before Decision.
**Subject:** `PROPOSAL_GOVERNANCE_V2_RISK_TIERED_ROUTING.md`.
**Canon referenced:** Framework 001/001A (DL-030/031); zones DL-051; `code/` non-canonical DL-057; DL-053; Anti-Assumption protocol; CODEOWNERS / branch protection.

---

## 1. Findings

- **Coherent and correctly self-classified.** The proposal routes itself through the full Class A path; it doesn't exempt itself. Good.
- **Targets the real bottleneck.** Separating *ratify intent* (owner) from *approve realization* (EM/gates) is the correct diagnosis; PR #21 evidences it.
- **Low conceptual debt.** It builds on existing canon (DL-051 zones, DL-057, the Dev Readiness Decide lane) rather than inventing structure.
- **Preserves the load-bearing core** explicitly (canon ratification, precedence, conflict adjudication, audit trail, Anti-Assumption, never-push-main, owner-only canon).
- **Honest about its central tradeoff** (reversible mistakes corrected vs. prevented).

The direction is sound. The concerns below are about *safety of the delegation mechanics*, not the principle.

## 2. Concerns (blocking unless noted)

1. **[BLOCKING] No classifier — the misclassification bypass.** The model routes by class but never says *who assigns the class* or what stops a canon-touching change being mis-tagged Class D/E to skip the owner. The classifier is itself a governance control; as written, v2 can be *routed around* — the precise failure more approvals were meant to prevent. *Fix:* a "when in doubt, the higher class wins" rule; class recorded as a field of record; periodic owner/independent **sample-audit** of delegated (C/D/E) changes.
2. **[BLOCKING-as-sequencing] Gates are load-bearing but unproven.** v2 shifts enforcement to the gates, yet the **per-gate red-proof (PR #21 item 2) is still open** — gates aren't demonstrated to fail-when-they-should. Don't fully delegate Class D until the red-proof lands. Also a slight **over-claim**: doctrinal/architectural *judgment* and product-fit aren't machine-checkable; name the canon that no gate covers and how it's caught (seam review / sampling), so "gates catch deviation" isn't read as total.
3. **[BLOCKING] "Reversible" and "lightweight review" are unfalsifiable.** Both carry weight (reversibility gates Class E and lazy consensus) yet have no test — the P-4 pattern. *Fix:* define reversible crisply (e.g., "revertible by a single PR, no data loss, no external side-effect") and bound "lightweight review" (one reviewer, fixed checklist).
4. **[BLOCKING] Lazy-consensus silent-adoption.** Auto-adopt-unless-objected means a missed weekly session ratifies by inattention. *Fix:* restrict to reversible + non-gate-affecting + non-contract items; require an explicit objection-window length; define the revert path for a lazy item later found wrong; Class A categorically excluded (already stated — keep).
5. **[BLOCKING] CODEOWNERS / branch-protection conflict (verify live).** Main is protected and CODEOWNERS auto-requests the owner. If CODEOWNERS currently requires owner review on **all** paths, Class D "owner: none" contradicts the merge mechanics. *Fix + dependency:* scope CODEOWNERS so the EM is the required reviewer for `code/`/`30_engineering` and the owner remains required only on canon paths. Verify against the live file, don't assume.
6. **Single-person concentration (structural).** Owner = EM = product-lead today makes C/D delegation nominal; the gates become the *only* independent check. Acceptable **only if** gates are strong (see #2). State this explicitly and treat gate integrity as the compensating control, with a plan to seat a real EM.
7. **Class C product-lead is undefined.** No named product-lead role exists; "notified, not gating" collapses to the owner. Either name the seat or fold C into "owner-notified" until seated.
8. **No drift control on the classification table itself.** As zones/canon evolve, class boundaries go stale (the C-1 drift pattern). Assign an owner for the table and version it.

## 3. Dependencies

- **Per-gate red-proof** complete (PR #21 item 2) — precondition for full Class D delegation.
- **CODEOWNERS scoped** to canon paths (verified against live config).
- A crisp **reversibility test** + bounded "lightweight review" definition.
- A **classification-of-record + audit cadence** mechanism.
- **EM seat** decision (Kashif) and **product-lead** seat (or fold Class C).
- Backlog to **encode each named canon rule** not yet machine-checked, plus an explicit list of canon that stays judgment-only.
- DL entries to ratify the model + the pre-authorizations (themselves Class A).

## 4. Recommendation (advisory — owner ratifies)

**Adopt the direction; return for one revision** before Decision. Must-fix-before-Decision: Concerns **#1 (classifier + audit), #3 (definitions), #4 (lazy-consensus guardrails), #5 (CODEOWNERS scoping)**. Treat **#2** as a sequencing gate — you may *ratify the model* now, but **stage Class D delegation behind the gate red-proof**. Resolve #6/#7 by naming seats (or stating the owner=EM compensating-control posture explicitly). Obtain Kashif's **independent** Findings/Concerns — this Review is not independent.

Net: the proposal is ~80% Decision-ready; the missing 20% is the delegation **safety rail** (who classifies, what's reversible, gate proof, CODEOWNERS), which is exactly the part that determines whether v2 strengthens or quietly weakens enforcement.

## 5. Status

**Returned for revision.** Decision-ready once the four must-fix concerns (#1, #3, #4, #5) are addressed and the gate red-proof (#2) is set as a Class-D delegation precondition. Class A change — full Framework 001 path only; no lazy/expedited route.

---

*Traceability:* `PROPOSAL_GOVERNANCE_V2_RISK_TIERED_ROUTING.md`; PR #21 (items 2, the worked example) + Issue #24; DL-030/031/051/053/057; Anti-Assumption protocol. *Produces the five Framework 001 Review outputs; feeds the owner Decision.*

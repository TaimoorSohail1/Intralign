# Review 001 — ENV-REV-001 + Phase 1 Foundation Artifacts

**Document Type:** Framework 001A Review (analysis & recommendation only — non-canonical) · **Status:** Recommend, with conditions — owner decision pending
**Date:** 2026-06-10 · **Reviewer role:** AI contributor (analysis, consistency checking, conflict identification, recommendation generation — per `CLAUDE.md` Authority Constraint)
**Subject:** `foundation-phase-1` branch — `REVISED_PHASE_1_FOUNDATION_STACK_PROPOSAL.md` (ENV-REV-001) + sibling design artifacts
**Reference canon:** `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md`, `20_handoff/interfaces/RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` (§11), `30_engineering/delivery/starter_kit/CLAUDE.md`, `00_owner/OPEN_TBD_REGISTER.md` (C1), `00_owner/canonical_definitions/canonical_definitions.md`, `10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` (§8/§14), `10_product/experience/RELEASE_1_UI_SPECIFICATION_V1.md`

> **Governance note.** This Review analyzes and recommends; it does not ratify, reject, supersede, or adopt. Only the repository owner may do so (Authority Constraint). It lives in `90_research/` (non-canonical; informs but does not bind, DL-033).

---

## Findings

The branch adds five files, all under `90_research/design_artifacts/` — correct non-canonical zone (DL-033/DL-051). The diff is all-additive; no `00_owner` / `10_product` / `20_handoff` / `30_engineering` canon is touched. This honors "AI may not author or supersede canon."

ENV-REV-001's "ratified profile" column is faithful to the owner canon — each row checks against `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` (§2 DB matrix, §5 LLM, §6 hosting, §7 observability). The §9 invariants (append-only, canonical/derived separation, no `/authority` module, recompute-appends, secrets never committed, production human-only) all match `starter_kit/CLAUDE.md`. The data mapping correctly folds in the DL-043 reconciliation (Cognition History Record + User Acceptance Record as canonical append-only; Governance Decisions excluded as out-of-R1). It correctly routes through Framework 001 rather than self-ratifying and flags that the LLM provider/routing change needs human approval (accurate — `starter_kit/CLAUDE.md`).

On the corrected diagram: its recommendation-action fix is correct. The authoritative State Model (`RELEASE_1_STATE_MODEL_SPECIFICATION_V1`, the designated "lifecycle authority") defines recommendation states as `Generated → Accepted → Rejected → Deferred → Implemented (+Superseded)`. "Deferred" is canonical (RS-R3); there is no "Modify" state. The prior diagram's "Modify" came from Master Spec §8's looser prose list. The event-driven Deep Pass note and the "response = evidence" framing are also accurate.

## Concerns

1. **Observability (highest).** The profile mandates OTel→Grafana plus service-health, queue/event-stream monitoring, two-axis derivation replay, governed-output events, and retention. LangSmith covers runs/traces/cost but not those. The proposal admits this and escalates "replace vs complement" — good — but as worded, replacing OTel→Grafana would under-satisfy CI gate-5. Ratify only as **complement**, not replace, unless Grafana is explicitly retired.
2. **Assumed owner-pending value.** §6 cites "≥1-year audit" retention. The profile leaves audit retention "per compliance/governance," and `OPEN_TBD_REGISTER` C1 marks it TBD. That figure should read as a proposed default pending C1, not a requirement (anti-assumption).
3. **LLM routing.** Profile §5 specifies a workload-routing matrix + quotas + model-consumption auditability. The proposal carries the abstraction and cost/token capture but does not explicitly preserve the routing matrix/quotas — confirm the `/services/llm_provider` adapter does.
4. **Diagram drift introduced while fixing drift.** The corrected diagram renames "Project MRI"→"MRI" and "CAF Overlay"→"Overlay." "Project MRI" is canonically defined (`canonical_definitions.md`); the shortenings depart from canonical names — keep the canonical names.
5. **Intake deferral presented as settled.** It marks "Start From Template" and "Guided Intake" as deferred. Defensible (the UI Spec defines neither; only Upload appears) — but Master Spec §14/§15 lists all four, and the scope authority (`OSLO_RELEASE_1_CANONICAL_SCOPE_V1`) does not explicitly defer them. This is a Master-Spec-vs-UI-Spec ambiguity that needs an owner scope ruling, not a baked-in "correction."
6. **Unresolved canon conflict surfaced.** Master Spec §8 lists "Modify"/"Discuss" as recommendation actions; the State Model has neither and adds "Deferred." The diagram rightly follows the lifecycle authority, but the §8 conflict itself should be reconciled via a proposal, not left implicit.
7. **Minor terminology (DL-053).** The proposal calls the profile "ratified" in places; its actual status is "Owner-Provided, pending DL-043 reconciliation."
8. **Intra-PR consistency.** The sibling `ORIENT_PHASE` stage matrix still binds Mongo/Qdrant (current canon) while ENV-REV-001 removes them — fine now, but must be reconciled if ratified. Also verify its "±7" determinism band traces to a ratified calibration default vs an assumed value (the band is owner-pending per OPEN_TBD).

## Dependencies

- The five ratifications in proposal §12.
- App-repo / starter-kit existing for the template edits (build-realization → app-repo relocation parked pending the app repo).
- Owner-ratified updates to the Database Ownership Matrix and Logical Data Model v1.2 (remove Mongo/Qdrant).
- NFR Acceptance Matrix / OPEN_TBD C1 (audit retention) and the determinism band.
- A Master Spec §8 ↔ State Model reconciliation (for the diagram and the recommendation-action canon).
- Owner scope ruling on Template / Guided Intake.

## Recommendation

ENV-REV-001 is well-governed and ready to route through Framework 001 as Proposal → Decision. If ratified, condition it on: observability = complement (not replace) until owner says otherwise; audit retention labeled proposed-pending (C1); the LLM adapter confirmed to preserve workload routing + quotas; and the "ratified → owner-provided" wording fixed. For the diagram: keep the recommendation-action and event-driven fixes, keep canonical "Project MRI"/"CAF Overlay" names, and label the intake deferral as "pending owner scope ruling."

## Status

**Recommend, with conditions.** Not ratified — owner decision required (Authority Constraint). AI analysis only.

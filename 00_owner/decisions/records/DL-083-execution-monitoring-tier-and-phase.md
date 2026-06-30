# DL-083 — Execution-monitoring tier placement & phase (T3/Pro+, Beta-built; out of Alpha exit) + capability tier split

- **Date:** 2026-06-28 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (product-roadmap / monetization orientation; non-doctrinal)

- **Source:** Owner direction 2026-06-28 — confirm the three-way capability tier split and **move execution monitoring from Alpha exit to Beta** (the Tier-3 monitoring build lands in the Beta phase, so it cannot gate Alpha graduation). Proposal: `PROPOSAL_EXECUTION_MONITORING_TIER_AND_PHASE_DRAFT.md`; backlog: RB-029. Grounded in DL-082 (Alpha exit criteria), DL-074 (hybrid pricing / tier ladder), DL-081 (Layer-Before-Depth), DL-076 (release ladder), DL-073 (deferred-signup / share-out), DL-047 (advisory-only); tier-progression note (2026-06-05).
- **Layer:** Product scope / roadmap + monetization orientation (`10_product`). **Non-doctrinal.** Amends DL-082 (phase) and extends DL-074 (capability tier placement). Artifact: `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a.

## Decision

**1. Capability tier split (extends DL-074).** Distinguish three previously-conflated capabilities and place each:
- **Export-Share-Out** (read-only orientation share, G4 / Wave E) — **Free / no-account** (acquisition loop; DL-073). Unchanged.
- **Plan export → execution tool** (outbound push of the plan into Jira/Asana/MS Project as tasks) — **Tier 2 / Basic**. A **distinct, separately-scoped** capability — *not* the G4 share-out and *not* execution monitoring. Low cost (one-shot, no polling); reinforces neutrality ("your plan, your execution tool").
- **Execution monitoring** (inbound execution-outcome ingest + closed feedback loop) — **Tier 3 / Pro+**, inherited by Team/Enterprise. Continuous polling is a recurring-cost + rate-limit surface (DL-074); kept above Basic to protect low-tier margin and the Pro upsell.

**2. Phase placement (amends DL-082).** **Execution monitoring/visibility is a Beta capability**, built at Tier 3 in the Beta phase. It is **removed from the Alpha exit criteria** — a capability built in Beta cannot gate Alpha→Beta graduation. The amended Alpha exit criteria are: (1) build/prove gates pass; (2) value validated by behavioral retention / repeat use; (3) ≥ 2 governed planning sources (vendor breadth); (4) 50+ users + engagement (§20). **Outcome-impact validation** (did governed understanding improve delivery?) becomes a **Beta** gate, once monitoring exists.

**3. Alpha validates engagement; Beta validates outcome impact.** With monitoring deferred, Alpha value-validation rests on **behavioral retention** (engagement). The outcome-truth loop (compare governed understanding against observed outcomes) is a **Beta** capability/gate. Accepted scoping consequence.

**4. Plan export-out is not yet scoped.** Capability #2 is a **distinct, not-yet-defined** capability (the G4 contract is share-out, not push-to-execution-tool). It routes to its own scoping (which tools, one-way vs round-trip, task mapping). **Do not assume it exists or is built.**

## Conditions
1. **Advisory-only preserved (DL-047).** Execution monitoring is read-only observation; never execution or coordination. Plan export-out is an outbound artifact push, not OSLO acting on the execution system.
2. **Consistent with Layer-Before-Depth (DL-081).** Read-only visibility is *permitted but not required* in Alpha; execution-phase depth (monitoring, then drift-surfacing) lands later — Beta and beyond.
3. **R1-safe.** Does not alter R1 scope (CHG-064). Tier placement values are owner-set starting points (DL-074 pattern), re-tunable from telemetry.
4. **Plan export-out requires separate scoping** before build (Anti-Assumption); this decision only places it at Tier 2, it does not define or authorize its realization.
5. **Cross-record reconciliation.** §3a of `RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` is amended to match; DL-082's Alpha exit list is superseded by the four-criterion list above.

## Supersedes / Amends
**Amends DL-082** (removes the execution-visibility Alpha exit criterion; relocates execution monitoring to Beta). **Extends DL-074** (adds the three-way capability tier placement). No epistemic invariant, doctrine, or constitution touched.

## Provenance
Owner working session, 2026-06-28: after the AI critical assessment distinguished Export-Share-Out vs. plan-export-out vs. execution-monitoring, the owner confirmed the three-way tier split (Free / T2 / T3) and directed moving execution monitoring from Alpha exit to Beta because the Tier-3 build lands in Beta. AI drafted and recommended; the owner ratifies. Numbered at landing under the DL-065 records discipline.

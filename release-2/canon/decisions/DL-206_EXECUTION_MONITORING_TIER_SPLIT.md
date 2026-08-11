# DL-206 — Execution-monitoring tier split: manual execution-stage monitoring at Basic; automation + programme at Pro (R2, staged)

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** B (product scope / monetization *placement* — non-doctrinal)
- **Framework 001** — AI drafts; only the owner ratifies.
- **Basis:** owner working session 2026-08-09. Chain: **RB-041** → Proposal (`release-2/GOVERNANCE_PROPOSAL_execution-monitoring-manual-basic-tier.md`) → Review (five outputs, in the proposal) → this Decision. Staged change-spec: `release-2/PROPOSED_EDITS_execution-monitoring-manual-basic-tier.md`.
- **Amends:** DL-083 (execution-monitoring tier placement). **Extends:** DL-172 §7, DR-7. **Supersedes:** the DL-172 §7 clause "auto-import + two-way sync = **Basic**" (→ **Pro**).
- **Placement:** staged in `release-2/` (R2 copy-of-record); **withheld from `main` until R1 graduation**. R1/Alpha canon (≤ DL-156) untouched. The edits to `RELEASE_1_TIER_DEFINITIONS_V1` (§1/§2c), `CANONICAL_GLOSSARY` (DL-053 register), and `RELEASE_MODEL_AND_ALPHA_LADDER_V1` (§3a note) are **captured as the redline and applied when R2 folds into `main`** — consistent with the current DL-172 / DR-7 staging posture.

---

## Decision

**Organizing axis:** Basic = **manual / on-demand** (the user drives updates); Pro = **automated / continuous** (the system drives them).

1. **Split execution monitoring (amends DL-083 capability 3).**
   - **Execution-stage monitoring (manual) → Tier 2 / Basic.** User-driven, on-demand ingestion of execution **actuals** (status, %-complete, actual dates, spend) against the plan, producing a refreshed read on delivery drift and a **monitored state maintained over time** (delta / trend). Capacity-shaped; no recurring compute. DL-083's cost rationale (continuous polling) does **not** apply to this form.
   - **Continuous monitoring (automated) → Tier 3 / Pro+** (Team/Enterprise inherit). Event/schedule-triggered watch; no user action. Unchanged from DL-083 in substance.

2. **Resolve the sync conflict (DL-172 §7 ↔ DR-7) → Pro.** Auto-import + two-way sync is automation → **Pro**. This adopts DR-7's placement and **supersedes** the DL-172 §7 "sync = Basic" clause. Basic retains **manual/one-shot** connection: plan export → execution tool (DL-083 cap 2) and manual execution-actuals ingest (§1).

3. **Pro value line (extends DR-7).** Pro = automated continuous monitoring + auto-import / two-way sync + **programme / cross-plan execution support** (`RELEASE_1_TIER_DEFINITIONS_V1` §1; DL-083). This eases — does not close — Pro's PROVISIONAL status; **final Pro price stays OPEN** pending its full capability set. Precise programme-support scope routes to its own scoping.

4. **Free unchanged.** Full plan read (planning stage), manual re-upload to refresh, export a file. No execution-stage monitoring at Free.

5. **Phase unchanged.** Both monitoring forms are **Beta / post-R2** capabilities (DL-083). **No R2 build impact** (DL-172 §5: R2 is freemium-only). This decision re-maps *placement*; it authorizes no build.

6. **Terminology (routes to the DL-053 register).** Canonical: **execution-stage monitoring (manual)** vs **continuous monitoring (automated)**; and **"phase"** is reserved for the D124 *supply* limit (Alpha/Beta) — the plan lifecycle uses **planning stage / execution stage**. Exact terms are the owner's DL-053 call.

## Doctrine preserved (unchanged)

Judgment quality is **never tiered** — one accuracy bar for all; Basic buys *access to the execution stage*, never a better read (DL-103 §1). The epistemic record is **never metered** (DL-102 D128). Reviewers/CRR and Viewers are **free forever** (DL-102 CR-2/E). No forecast / probability of success (D003/D183b). Flat **per-account**, never per-seat (DR-7). Because Basic opens a *new stage* Free never had (not a re-wall of the free read), no comprehension is metered (D126 / DL-102 D124/E-1).

## Open (non-blocking)

Final Pro price; exact canonical terms (DL-053 owner call); manual-monitoring mechanics + programme-support scoping (route to their own scoping); the land-to-`main` timing (at R1 graduation, with the rest of the R2-staged DLs).

## Given (not reopened)

DL-172 §2 — multi-outcome-per-plan at Basic.

## Affected artifacts

`GOVERNANCE_PROPOSAL_execution-monitoring-manual-basic-tier.md` · `PROPOSED_EDITS_execution-monitoring-manual-basic-tier.md` (staged redline) · `BACKLOG_RB-041_execution-monitoring-tier-split.md` · at graduation: `RELEASE_1_TIER_DEFINITIONS_V1` §1/§2c, `CANONICAL_GLOSSARY` DL-053 register, `RELEASE_MODEL_AND_ALPHA_LADDER_V1` §3a.

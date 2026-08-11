# Backlog entry RB-041 (DRAFT) — ready to append to `00_owner/backlog/revision_backlog.md`

> Companion to `GOVERNANCE_PROPOSAL_execution-monitoring-manual-basic-tier.md` +
> `PROPOSED_EDITS_execution-monitoring-manual-basic-tier.md`. Completes the Framework 001 chain from the
> top: **Backlog (RB-041) → Proposal → Review → Decision (DL-206) → Change (staged redline) → Changelog
> (at graduation).** Append the block below to `00_owner/backlog/revision_backlog.md` when R2 folds into
> `main`.

---

### RB-041 — Execution-monitoring tier split: manual execution-stage monitoring at Basic; automation + programme at Pro

- **Source Finding:** 2026-08-09 — owner working session (Idris). The current execution-handoff ladder gates **all** execution monitoring to Pro+ (DL-083, capability 3). Owner value-sequencing thesis: the full value loop is **execution monitoring + plan revision**, so gating the whole loop to Pro delays first value; **capacity** meters — not capability walls — should drive upgrades. Pressure-testing found *continuous* monitoring cannot move to Basic (recurring-compute cost breaks the flat-per-account posture; and it hollows out Pro's only value line, already marked PROVISIONAL in DR-7). The resolution is to **split monitoring by who drives updates**. The same review surfaced a standing self-contradiction in canon: **DL-172 §7 places auto-import / two-way sync at Basic; DR-7 lists it under Pro.**
- **Affected Layer(s):** `00_owner` (decision amending DL-083; extends DL-172 §7 and DR-7; adds DL-053 register terms) · `10_product/strategy/tiering` (`RELEASE_1_TIER_DEFINITIONS_V1` §1 + §2c) · `10_product/scope` (`RELEASE_MODEL_AND_ALPHA_LADDER_V1` §3a note).
- **Affected Concepts:** execution-monitoring tier placement; **execution-stage monitoring (manual)** vs **continuous monitoring (automated)**; auto-import / two-way sync placement; Pro value line (automation + programme / cross-plan support); DL-053 disambiguation ("monitoring", "phase/stage"). **Doctrine untouched** — judgment quality never tiered (DL-103 §1), record/reviewer/Viewer never metered (DL-102 D128/CR-2/E), no forecast (D003/D183b), flat per-account (DR-7).
- **Proposal Scope:** One decision (**Class B**, non-doctrinal *placement*). (1) Manual execution-stage monitoring → **Basic** (capacity-shaped; no continuous-polling cost — the cost basis DL-083 used to justify Pro-only). (2) Continuous monitoring + auto-import / two-way sync → **Pro+**, resolving DL-172 §7 ↔ DR-7 in DR-7's favor (sync → Pro; supersedes the DL-172 §7 "sync = Basic" clause). (3) Confirm Pro = **automation + programme / cross-plan support**. Free unchanged. **Phase unchanged** (both forms Beta; DL-083). **No build authorized** — manual-monitoring mechanics and programme-support scope route to their own scoping.
- **Dependencies:** DL-083 (**AMEND**) · DL-172 §7 (**EXTEND / partial supersede** — sync → Pro) · DR-7 (**EXTEND** — Pro value line; eases PROVISIONAL, final Pro price still OPEN) · `RELEASE_1_TIER_DEFINITIONS_V1` §1/§2c (**UPDATE**) · DL-053 register (**ADD** terms). Constrained by DL-103 §1, DL-102 D128/D124/CR-2, DL-048 (Free cost posture). **Given, not reopened:** DL-172 §2 (multi-outcome-per-plan at Basic).
- **Status:** **Ratified as DL-206** (2026-08-09, Idris / Founder Console); staged in `release-2/` (R2-isolated; folds into `main` at R1 graduation). Non-blocking opens: final Pro price; exact canonical terms (DL-053 call); manual-monitoring + programme-support scoping.

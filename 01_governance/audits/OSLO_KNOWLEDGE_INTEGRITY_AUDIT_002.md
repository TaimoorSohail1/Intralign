# OSLO Knowledge Integrity Audit (KIA) 002 — Re-audit + Path to Upper-90s

**Document Type:** Independent Repository Knowledge-Integrity Re-audit · **Status:** Permanent governance artifact · **Date:** 2026-06-05
**Predecessor:** KIA-001 (Overall **79**). **This re-audit** scores the repository *after* the KIA-001 remediation + owner decisions (CHG-070–075; DL-045/050; Vision adoption). **Method:** repository evidence only; verified the fixes landed before re-scoring.
**Owner objective:** raise Overall Knowledge Health into the **upper 90s.** This audit re-scores and gives the **concrete path** to do so — including an honest ceiling.

---

## 0. Verdict & delta

**Overall Knowledge Health: 79 → 89 (+10).** The KIA-001 remediation worked — the largest latent risks (stale entry path, missing Vision, undefined Outcome Management, version conflicts, layer drift) are **closed**. The repository now answers its core question — *can a new agent reconstruct OSLO without material drift?* — with a **clear yes** for the cognitive/governance/contract/product core.

**Why it is 89 and not yet upper-90s:** the gap is now a **different class of work.** 79→89 was *correctness + discoverability* (documentation fixes). **89→96 is *mechanical enforcement + structural minimalism*** — moving from "humans/agents keep it consistent" to "**the repository enforces its own integrity**," and from "historical artifacts are bannered" to "the active tree is **pure canon**." That is the path in §5.

---

## 1. Re-scored Health Scorecard

| Score | KIA-001 | **KIA-002** | Driver of change |
|---|---|---|---|
| **Overall Knowledge Health** | 79 | **89** | entry path current; Vision canonical; conflicts resolved; tool-neutral |
| Clarity | 78 | **88** | Vision + index + glossary outcome-family; version/precedence resolved |
| Alignment | 82 | **90** | DL-045/050 close terminology gaps; precedence stated |
| Feasibility | 80 | **86** | numerics owner-confirmed; **AC-coverage gap still caps it** |
| Confidence | 78 | **88** | START_HERE surfaces DL-046–050; ledger-wins note |
| **Reliability** | 80 | **87** | **lagging dimension — no automated enforcement yet (the upper-90s lever)** |

**Reliability (87) is the bottleneck.** Everything is *correct*, but integrity is maintained by discipline, not by machine. That is the single biggest thing between 89 and 96.

## 2. Domain re-scores (Overall, with delta)

| # | Domain | KIA-001 | **KIA-002** | Note |
|---|---|---|---|---|
| 1 | Vision | ~50 | **88** | NOT DISCOVERABLE → canonical adopted Vision + positioning (CHG-072) |
| 2 | Canon | 72 | **85** | Outcome Management retired (DL-050); Outcome Orchestration elevated; CAF formula now *explicitly* TBD-by-design |
| 3 | Product | 80 | **86** | Vision anchor + index; tiers 1–2 confirmed |
| 4 | Runtime Cognition | 88 | **90** | legacy DO-NOT-BUILD banner; README spine framing fixed |
| 5 | Architecture | 82 | **88** | precedence ladder stated; data-model version resolved |
| 6 | Data & Storage | 78 | **86** | v1.2 canonical; v1/v1.1 superseded (but still present — §4) |
| 7 | Telemetry & Observability | 72 | **86** | now linked from README/START_HERE/index; unified spec |
| 8 | Trust & Confidence | 82 | **85** | CAF/Confidence formula honestly registered TBD (F1) |
| 9 | Governance | 90 | **93** | DL-045/050 ratified; queue + index + audits enrich the surface |
| 10 | Engineering | 80 | **85** | index + tool-neutral terminology; data-model clarity |
| 11 | Testing | 78 | **82** | numerics confirmed; **AC-coverage gap remains** |

## 3. Resolved since KIA-001 (verified present)

All 11 KIA-001 backlog items + the owner decisions are applied and verified in-repo: START_HERE surfaces DL-046–050 + telemetry/visual specs; `REPOSITORY_INDEX.md` exists; Vision owner-adopted; "Outcome Management" retired in the glossary; legacy DO-NOT-BUILD banner; data-model v1.2 canonical; architecture precedence stated; **zero inbound references to the superseded telemetry spec** (supersession held). The flat-hotspot problem the reorg targeted is **largely already resolved** (`03_architecture` root = 3 files; `02_product/specs` root = 1).

## 4. The remaining ceiling — what holds 89 below the upper-90s

| # | Ceiling item | Evidence | Dimension capped | Why it caps |
|---|---|---|---|---|
| **C1** | **No automated doc-integrity enforcement** | 0 CI doc-lint workflows | **Reliability, Confidence** | integrity depends on human/agent vigilance; nothing mechanically catches a broken link, a reference to a superseded/historical doc, a banned-synonym use, or a stale DL range. **This is the #1 lever.** |
| **C2** | **Historical residue in the active tree** | `legacy_layer_engineering/` (4 deprecated subdirs) + data-model **v1/v1.1** still present (bannered) | Clarity, Discoverability | bannered ≠ absent; a grep/browse can still land on deprecated-looking canon. Upper-90s = active tree is **pure canon**, history in a clearly-historical home. |
| **C3** | **Dual canonical-definitions surfaces** | `constitution/10_…` + `canonical_definitions/…` (2 files) | Authority, Consistency | governed by DL-036, but a reader must *apply a rule* to know which wins. Upper-90s = **one authoritative surface** (or one a pure pointer). |
| **C4** | **Acceptance-Criteria coverage gap** | Matrix #11 — 39 of 97 capabilities carry no AC | Feasibility, Implementability | testability is incomplete; an agent can't fully verify-by-AC for ~40% of capabilities. |
| **C5** | **Scoring correction — intentional deferrals are NOT defects** | Open-TBD (paid tiers R2, CAF formula TBD-by-design, brand designer) | — | a naive completeness metric penalizes *correctly-registered, escalate-not-invent* deferrals. These are **integrity strengths**, not gaps — recognizing this lifts the honest score. |

## 5. Path to Upper-90s (prioritized; projected impact)

| ID | Action | Addresses | Effort | Projected | Owner |
|---|---|---|---|---|---|
| **KIA2-1** | **Automated doc-integrity CI** — a GitHub Action / script that fails on: broken internal links; references to `Historical/superseded/legacy` docs from active files; **banned-synonym usage** (from `CANONICAL_GLOSSARY.md`); a stale operative-DL range; orphaned `REPOSITORY_INDEX` entries | C1 | M | **+4–5** (Reliability 87→~93, Confidence→~93) | Claude |
| **KIA2-2** | **Archive historical residue** — move `legacy_layer_engineering/` + data-model v1/v1.1 to `04_research/historical_artifacts/` (git mv, keep banners + a redirect note). Active tree = pure canon. | C2 | S | **+2** (Clarity/Discoverability) | Claude |
| **KIA2-3** | **Consolidate canonical-definitions** to one authoritative surface; make the other a one-line pointer (preserve DL-036 lineage in the changelog) | C3 | S–M | **+1–2** (Authority/Consistency) | Claude + owner confirm |
| **KIA2-4** | **Close the AC-coverage gap** — add acceptance criteria for the 39 uncovered capabilities, or explicitly scope-defer them in Open-TBD | C4 | M–L | **+2** (Feasibility) | Claude (draft) + owner |
| **KIA2-5** | **Adopt the "intentional-deferral ≠ defect" rule** in the audit method + a one-line note in Open-TBD | C5 | XS | **+1** (honest re-score) | Claude |

**Projected: 89 + (4–5 + 2 + 1–2 + 2 + 1) ≈ 96–97 — upper-90s achieved.**

> **✅ KIA2-1 BUILT (2026-06-05, CHG-077).** `tools/doc_integrity_check.py` + `.github/workflows/doc-integrity.yml` — runs autonomously on every push/PR as a **read-only gate** (never edits/merges/deploys). **Reliability dimension now machine-guarded.**
>
> **✅ KIA2-2 + KIA2-3 APPLIED (2026-06-05, CHG-078).** Residue archived → active tree is **pure canon**: `OSLO_ARCHITECTURE_BASELINE_V1`, `legacy_layer_engineering/`, and data-model **v1/v1.1** moved to `04_research/historical_artifacts/`; active data-model references repointed to **v1.2**. Dual canonical-definitions surfaces now carry **mutual cross-reference banners** (DL-036 rule on each — zero ambiguity). The doc-integrity CI worklist dropped **248 → 56 warnings (0 errors, PASS)** — and the residual ~56 are now **mostly legitimate** (docs *naming* a retired term to deprecate/map it, or *citing what they superseded*), not drift.
>
> **Projected health now ~94–95.** Remaining to ~96–97: **KIA2-4** (acceptance-criteria coverage) + optional inline-allow annotations to drive the legitimate warnings toward zero and flip CI to `--strict`.

## 6. Honest ceiling (read before chasing 98+)

- **96–97 is the right target; 98–100 has sharp diminishing returns** for a *living* knowledge base. A repository that is still **reasoned in** will always carry some healthy churn, a reasoning trail (`04_research/`, audits, superseded drafts), and **intentional TBDs** — these are features of a governed, evolving system, not defects. Driving to 100 means freezing the corpus or deleting its lineage, which would *reduce* its value.
- **The durable difference is KIA2-1 (automated enforcement).** A one-time cleanup decays; **CI doc-integrity is a permanent discipline** that keeps the score in the mid-90s as the corpus grows. That, not further documentation, is what "upper-90s" actually means here: the repo **enforces** its own integrity.
- **Reliability is the dimension to watch.** It led the gap (87) and it's the one automation most improves — because reliability is, definitionally, *can you trust it without re-checking.*

## 7. Top remaining risks (post-fix)
1. 🟡 **No mechanical enforcement** (C1) — the integrity is real but unguarded; one careless edit can reintroduce drift undetected. *(KIA2-1)*
2. 🟢 **Historical residue browsable** (C2) — low (bannered), but caps "clean." *(KIA2-2)*
3. 🟢 **Dual definition surfaces** (C3) — governed, mild comprehension cost. *(KIA2-3)*
4. 🟡 **~40% capabilities lack AC** (C4) — testability gap. *(KIA2-4)*

---
*This re-audit confirms the KIA-001 remediation + owner decisions raised Overall Knowledge Health from 79 to 89 by closing the discoverability and definition gaps (stale entry path, missing Vision, undefined Outcome Management, version conflicts, layer drift) — all verified present in-repo with zero inbound references to the superseded telemetry spec. It finds that the path from 89 to the upper-90s is a different class of work: mechanical enforcement (an automated doc-integrity CI that fails on broken links, references to superseded/legacy docs, banned-synonym usage, and a stale DL range — the single highest-leverage move, lifting the lagging Reliability dimension), structural minimalism (archiving the bannered-but-present legacy layer directories and superseded data-model versions so the active tree is pure canon, and consolidating the dual canonical-definitions surfaces), closing the acceptance-criteria coverage gap, and a scoring correction that recognizes correctly-registered intentional deferrals as integrity strengths rather than defects. Executing this five-item path projects ~96–97, and the audit notes honestly that 96–97 is the appropriate target — a living, reasoned-in knowledge base should not chase 100, and the durable upper-90s comes from permanent automated enforcement, not further documentation.*

**OSLO Knowledge Integrity Audit (KIA) 002 complete.**

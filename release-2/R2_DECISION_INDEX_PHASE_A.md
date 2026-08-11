# R2 Decision Index — Phase-A consolidation worksheet (DL-157…206 + DR-1…7)

**Date:** 2026-08-09 · **Author:** AI (assembled from ratified sources; owner ratifies the ⚠️ rows). · Companion to `R2_TO_MAIN_INTEGRATION_PLAN.md`.
**Purpose:** the single ordered ledger of every R2 decision, with status + record source + land-readiness. Once the ⚠️ rows are resolved by the owner, THIS is the delta that Phase B appends to `00_owner/decisions/decision_log.md` (which today tops at DL-156).

**Sources:** the **ratified** `R2_DL_READJUDICATION_WORKSHEET` (2026-08-04, adjudicates DL-164…197) · the standalone records in `release-2/canon/decisions/` · `DL-200-205` (DR-1…6) · `DR-7` · references to DL-158/162.

**Readiness key:** ✅ ready to land · ⚠️ needs owner action · ⛔ do-not-land (supersede/defer/retire) · ❓ reconcile (record missing/unclear).

---

## A. DL-157…163 — RECONCILE (owner) · **investigated 2026-08-09, definitive**
Searched **all branches, full git history, and the whole filesystem** (`code/` included).
| ID | Finding | Owner action |
|---|---|---|
| DL-157, 159, 160, 161, 163 | **Occur nowhere** — no record, no reference, on any branch or in history. | Confirm **never-issued** → the ledger skips these numbers (main runs 151…156 with no gaps). |
| **DL-158** (outcome-forward positioning) · **DL-162** (funnel telemetry) | Referenced-only; no record existed. **AI drafted reconstruction STUBS 2026-08-09** — `DL-158_OUTCOME_FORWARD_POSITIONING.md`, `DL-162_FUNNEL_TELEMETRY.md` — from the downstream references, clearly marked provisional (originals decided off-repo). | **Owner:** verify each stub matches the real ruling → **ratify** (set Date/Status); **or** supersede with the authoritative record; **or** re-cite the referencing docs. |

## B. DL-164…197 — canon-track, ADJUDICATED + RATIFIED 2026-08-04 (worksheet)
*These have **no standalone record files** — the ratified worksheet IS their record. Disposition per its verdict.*

| ID | Title | Verdict (ratified) | Readiness |
|---|---|---|---|
| DL-164 | Guidance system (coaching + lifecycle) | CARRY-MODS | ✅ |
| DL-165 | Confidence-pill redesign | CARRY-MODS (explainer → integrity band; ring retired) | ✅ |
| DL-166 | Notifications quiet mode | CARRY | ✅ |
| DL-167 | Coaching triggers = earned events | CARRY | ✅ |
| DL-168 | Soliciting input as utility (reviewer ask) | CARRY | ✅ |
| DL-169 | Loop-close + k-factor invite | CARRY | ✅ |
| DL-170 | Evidence vs comment legible | CARRY | ✅ |
| DL-171 | Grounding framing + onboarding + Reports graph | CARRY-MODS | ✅ |
| DL-172 *(canon-track)* | First-run prompt orchestration | RENUMBER-kept + CARRY-MODS | ✅ (keeps 172) |
| DL-173 *(canon-track)* | Fold strategic chain into grounding reveal | RENUMBER-kept + CARRY | ✅ (keeps 173) |
| DL-174 | Optimize reveal (Ground→Optimize crossing) | CARRY-MODS | ✅ |
| DL-175 | Onboarding identity + inference framing | CARRY | ✅ |
| DL-176 | Overview anchored/stage-aware tabs | **SUPERSEDE** (read-primary successor) | ⛔ retire, record successor |
| DL-177 | Read vs interpretation vocabulary | CARRY | ✅ |
| DL-178 | Compact confidence hero | **SUPERSEDE** (integrity masthead) | ⛔ retire |
| DL-179 | Grounding web full 1:1 render | CARRY-MODS (target render) | ✅ |
| DL-180 | Optimize-lens two-layer web | **DEFER (post-R2/optional)** | ⛔ not R2 |
| DL-181 | Severity colour on optimize marks | CARRY (independent of 180) | ✅ |
| DL-182 | Linked-highlight + hover tip on map | CARRY | ✅ |
| DL-183 | What-to-strengthen group-by | CARRY | ✅ |
| **DL-184** | R2 graph schema ratification | CARRY (**load-bearing backend**; standalone record) | ✅ |
| DL-185 | Grounding list group-by + deliverable issue CTA | CARRY | ✅ |
| DL-186 | Onboarding consolidation (continuous reveal) | CARRY-MODS | ✅ |
| DL-187 | First-run activation rework + role capture | CARRY-MODS (reconcile w/ DR-6) | ✅ |
| DL-188 | Post-activation hand-off (unlock→engaged) | CARRY | ✅ |
| DL-189 | Retire the stage model | CARRY | ✅ |
| DL-190 | Limiter standalone confirmation (next-move) | CARRY | ✅ |
| DL-191 | Issue-forward onboarding lead | CARRY | ✅ |
| DL-192 | Positioning (outcome-based risk intelligence) | CARRY | ✅ |
| **DL-193** | Priority re-anchor (limiter↔read, integrity↔queue) | CARRY (standalone record, RATIFIED) | ✅ |
| DL-194 (drift stub) | Continuous drift detection | **SUPERSEDE** (→ State 2 of the indicator) | ⛔ retire |
| **DL-194** (integrity indicator, 3-state) | State 1 = committed R2 scope | CARRY — **"confirm ratify"** (record is scribe-drafted; DR-4 effectively ratifies core) | ⚠️ confirm ratification |
| **DL-195** | Adaptability checkpoint-optimization (State-1 keystone) | CARRY — key calls ratified, **spec unfinished** | ⚠️ finish spec / confirm |
| **DL-196** | Integrity via the exposure-gated issue layer | CARRY (standalone, RATIFIED) | ✅ |
| **DL-197** | Grounding false-confidence issue type (`ISS-FC-<art>`) | CARRY (standalone, RATIFIED) | ✅ |

## C. Renumbered + newer decisions (DL-198…206) + DR series
| ID | Title | Status | Readiness |
|---|---|---|---|
| **DL-198** *(was DL-172 freemium)* | Freemium value moments; **unit = the OUTCOME**; extends DL-158 | **Ratified** (2026-08-04) — file still named `DL-172_FREEMIUM_…`, **rename to DL-198** | ⚠️ rename file/ID to 198 |
| **DL-199** *(was DL-173 owner-activation)* | Owner activation = first grounding act (DR-6 amends → 2nd act) | Ratified — **rename to DL-199** | ⚠️ rename file/ID to 199 |
| DL-200–205 | The six Resolve-First rulings = **DR-1…DR-6** (canonical R2 hierarchy: outcome-first, enforce-via-commitment-gate, integrity indicator, phased resolution, activation=2nd act) | **DRAFTS for ratification** (some DR-4/5/6 already applied in-process) | ⚠️ **owner ratify** the formal records |
| **DL-206** | Execution-monitoring tier split (manual→Basic; continuous/sync/programme→Pro; amends DL-083) | **Ratified** (2026-08-09) | ✅ |
| **DL-207** | Plan export & PM-tool tiering (file export=Free · one-way push=Basic · two-way sync+monitoring=Pro; **realizes DL-206** §2/§4, extends DR-7/DL-083) | **Ratified** (2026-08-09) | ✅ |
| **DL-208** | Pro program / cross-plan **execution-cognition** scope (Bundle A: roll-up · dependency mapping · program monitoring, program-envelope cap; aggregate never a health score) + **Pro price set $79** (amends DR-7, drops placeholder; adopts US "program") | **Ratified** (2026-08-09) | ✅ |
| **DL-209** | Load-bearing sensitivity + issue-classification/resolution model — 5 first principles (load-bearing = magnitude-sensitivity ≥ calibrated threshold; **only verify moves Grounding**; verify/build/decide), L0–L4 architecture (deterministic core + thin learnable calibration), global-threshold-with-dormant-segmentation; **completes DL-196/197** | **Ratified** (2026-08-09) | ✅ |
| **DL-212** | **Establish Framework 002 — Release Lifecycle & Change Control.** Phase machine (Open→…→Retire); R2.x = Build-phase change control over the frozen baseline; **Freeze Manifest** + three-class change model (neutral/additive/altering) + **push-via-labeled-PR** delivery (`altering` gated on dev-lead approval, convention to start); **Refinement Ledger** (mirrors merged PRs); **Durable Invariant Registry** (spine never regresses); skills `release-refine`/`guard-add` to follow. Companion to Framework 001 (decisions) | **Ratified** (2026-08-09) | ✅ |
| **DL-211** | **Proposal-resolution model** — proposals split **build** (adds a missing structural element → accepting resolves the finding + may firm the band via reanalysis) · **inference** (accept OSLO's guess → additive, grounds only by verifying) · **optional** (additive); **cross-surface resolution sync** (one finding, one resolution, any surface, only reanalysis resolves); multiple resolvers close only when all accepted (keynote-backup = requirement + task); **itemized atomic findings** (never merged); amends `proposalsFoldedIntoRead`; guards GT-51…GT-54 | **Ratified** (2026-08-09) | ✅ |
| **DL-210** | CAF dimension boundaries + **deterministic structural-target dimension assignment** (Clarity=definition · Alignment=edge/relational · Feasibility=achievability; Clarity→Alignment→Feasibility precedence); **Alignment relational**, top-down outcome→roots; escalation model (runtime→user clarify/verify · model-gap→governance + leverage-gated known-unknown, load-bearing gap ceilings integrity **incomplete not Fragile**); **amends CAF Positions #10/#11** (preserves #2/#13); reconciles DL-209 decompose ⇄ CAF multi-dimension by layer; extends DL-209/Slice 10, guards GT-45…GT-50 | **Ratified** (2026-08-09) | ✅ |
| **DR-1** | `oslo-prototype-r2.html` = the single canonical R2 prototype (retires two-lineage divergence) | Ratified (drove the worksheet) | ✅ |
| DR-2…DR-6 | = DL-200–205 (see above) | drafts | ⚠️ ratify |
| **DR-7** | Pricing (Basic $29/mo; Pro $79/mo — **provisional/placeholder status removed by DL-208**) | **Ratified** · **amended by DL-208** (Pro price set) | ✅ |

---

## Readiness rollup
- **✅ Ready to land (ratified, CARRY):** DL-164–175, 177, 179, 181–193, 196, 197, 198*, 199*, 206, 207, 208, 209, DR-1, DR-7. (*after the file/ID rename.)
- **⚠️ Needs owner action before landing:** DL-194 (confirm ratify) · DL-195 (finish/confirm spec) · DL-200–205 / DR-2…6 (ratify the formal records) · DL-198 & DL-199 (rename file/ID from 172/173).
- **⛔ Do-not-land (supersede/defer):** DL-176, DL-178, DL-194-drift-stub (record the successors, don't add as active) · DL-180 (post-R2, defer).
- **❓ Reconcile (owner/dev):** DL-157, 159, 160, 161, 163 (likely unused/R1.x) · DL-158, DL-162 (real earlier decisions, records not in-tree — locate / confirm already-canon).

## Owner action list (unblocks Phase B)
1. **Ratify** DL-200–205 (DR-2…6) formal records; **confirm** DL-194 + finish/confirm DL-195.
2. **Rename** the freemium/owner-activation records to **DL-198 / DL-199** (the worksheet's ratified renumbering).
3. **DL-157–163 (investigated — definitive):** confirm 157/159/160/161/163 are **never-issued** (skip in ledger); DL-158 + DL-162 now have **drafted reconstruction stubs** — verify/ratify, or supersede with the real records.
4. **Confirm** the ⛔ supersede/defer set is retired-not-landed.
Once done, this table (minus ⛔) is the exact ledger delta for `R2_TO_MAIN_INTEGRATION_PLAN.md` Phase B.

## Phase-A mechanical steps (realization of the ratified renumbering — owner runs; not ratification)
The worksheet already ratified: freemium → **DL-198**, owner-activation → **DL-199**. Only the **freemium record is a standalone file**; owner-activation (DL-173) has no file (it's a worksheet row → ledger-only ID). So:
```
cd ~/GitHub/oslo-knowledge-base
git mv release-2/canon/decisions/DL-172_FREEMIUM_VALUE_MOMENTS_OUTCOME_UNIT.md \
       release-2/canon/decisions/DL-198_FREEMIUM_VALUE_MOMENTS_OUTCOME_UNIT.md
# then update the record's own ID header/self-refs 172→198 (keep the "extends DL-158" ref):
#   the title line "DL-172 —" → "DL-198 —"; any "this decision (DL-172)" self-reference → DL-198
```
DL-199 (owner-activation) needs no file move — assign the ID when the Phase-B ledger delta is written. (The canon-track DL-172/173 KEEP their numbers per the worksheet.)

_AI assembled this from ratified sources; it does not ratify. DL-164–197 dispositions are already owner-ratified (2026-08-04) — the ⚠️ items are the remaining formalizations._

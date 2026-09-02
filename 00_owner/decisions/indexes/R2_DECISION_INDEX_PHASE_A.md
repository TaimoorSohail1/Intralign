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
| **DL-158** (outcome-forward positioning) · **DL-162** (funnel telemetry) | Referenced-only; no record existed. **AI drafted reconstruction STUBS 2026-08-09** — `DL-158_OUTCOME_FORWARD_POSITIONING.md`, `DL-162_FUNNEL_TELEMETRY.md` — from the downstream references, clearly marked provisional (originals decided off-repo). | **Owner:** verify each stub matches the real ruling → **ratify** (set Date/Status); **or** supersede with the authoritative record; **or** re-cite the referencing docs. [R]|

## B. DL-164…197 — canon-track, ADJUDICATED + RATIFIED 2026-08-04 (worksheet)
*These have **no standalone record files** — the ratified worksheet IS their record. Disposition per its verdict.*

| ID | Title | Verdict (ratified) | Readiness |
|---|---|---|---|
| DL-164 | Guidance system (coaching + lifecycle) | CARRY-MODS | ✅ [R]|
| DL-165 | Confidence-pill redesign | CARRY-MODS (explainer → integrity band; ring retired) | ✅ [R]|
| DL-166 | Notifications quiet mode | CARRY | ✅ [R]|
| DL-167 | Coaching triggers = earned events | CARRY | ✅ [R]|
| DL-168 | Soliciting input as utility (reviewer ask) | CARRY | ✅ [R]|
| DL-169 | Loop-close + k-factor invite | CARRY | ✅ [R]|
| DL-170 | Evidence vs comment legible | CARRY | ✅ [R]|
| DL-171 | Grounding framing + onboarding + Reports graph | CARRY-MODS | ✅ [R]|
| DL-172 *(canon-track)* | First-run prompt orchestration | RENUMBER-kept + CARRY-MODS | ✅ (keeps 172) [R]|
| DL-173 *(canon-track)* | Fold strategic chain into grounding reveal | RENUMBER-kept + CARRY | ✅ (keeps 173) [R]|
| DL-174 | Optimize reveal (Ground→Optimize crossing) | CARRY-MODS | ✅ [R]|
| DL-175 | Onboarding identity + inference framing | CARRY | ✅ [R]|
| DL-176 | Overview anchored/stage-aware tabs | **SUPERSEDE** (read-primary successor) | ⛔ retire, record successor [R]|
| DL-177 | Read vs interpretation vocabulary | CARRY | ✅ [R]|
| DL-178 | Compact confidence hero | **SUPERSEDE** (integrity masthead) | ⛔ retire [R]|
| DL-179 | Grounding web full 1:1 render | CARRY-MODS (target render) | ✅ [R]|
| DL-180 | Optimize-lens two-layer web | **DEFER (post-R2/optional)** | ⛔ not R2 [R]|
| DL-181 | Severity colour on optimize marks | CARRY (independent of 180) | ✅ [R]|
| DL-182 | Linked-highlight + hover tip on map | CARRY | ✅ [R]|
| DL-183 | What-to-strengthen group-by | CARRY | ✅ [R]|
| **DL-184** | R2 graph schema ratification | CARRY (**load-bearing backend**; standalone record) | ✅ [R]|
| DL-185 | Grounding list group-by + deliverable issue CTA | CARRY | ✅ [R]|
| DL-186 | Onboarding consolidation (continuous reveal) | CARRY-MODS | ✅ [R]|
| DL-187 | First-run activation rework + role capture | CARRY-MODS (reconcile w/ DR-6) | ✅ [R]|
| DL-188 | Post-activation hand-off (unlock→engaged) | CARRY | ✅ [R]|
| DL-189 | Retire the stage model | CARRY | ✅ [R]|
| DL-190 | Limiter standalone confirmation (next-move) | CARRY | ✅ [R]|
| DL-191 | Issue-forward onboarding lead | CARRY | ✅ [R]|
| DL-192 | Positioning (outcome-based risk intelligence) | CARRY | ✅ [R]|
| **DL-193** | Priority re-anchor (limiter↔read, integrity↔queue) | CARRY (standalone record, RATIFIED) | ✅ [R]|
| DL-194 (drift stub) | Continuous drift detection | **SUPERSEDE** (→ State 2 of the indicator) | ⛔ retire [R]|
| **DL-194** (integrity indicator, 3-state) | State 1 = committed R2 scope | CARRY — **"confirm ratify"** (record is scribe-drafted; DR-4 effectively ratifies core) | ⚠️ confirm ratification [R]|
| **DL-195** | Adaptability checkpoint-optimization (State-1 keystone) | CARRY — key calls ratified, **spec unfinished** | ⚠️ finish spec / confirm [R]|
| **DL-196** | Integrity via the exposure-gated issue layer | CARRY (standalone, RATIFIED) | ✅ [R]|
| **DL-197** | Grounding false-confidence issue type (`ISS-FC-<art>`) | CARRY (standalone, RATIFIED) | ✅ [R]|

## C. Renumbered + newer decisions (DL-198…206) + DR series
| ID | Title | Status | Readiness |
|---|---|---|---|
| **DL-198** *(was DL-172 freemium)* | Freemium value moments; **unit = the OUTCOME**; extends DL-158 | **Ratified** (2026-08-04) — file still named `DL-172_FREEMIUM_…`, **rename to DL-198** | ⚠️ rename file/ID to 198 [R]|
| **DL-199** *(was DL-173 owner-activation)* | Owner activation = first grounding act (DR-6 amends → 2nd act) | Ratified — **rename to DL-199** | ⚠️ rename file/ID to 199 — **RESOLVE-MARKER WITHDRAWN 2026-09-02: DL-199 was CLOSED 2026-08-14 and absorbed into DL-205 §0/§0a; this row predates the closure and may not answer for it. Debt recorded in `UNRECORDED_DECISIONS.md` §C.** ⚠️ *The marker is not written here in its literal form — writing it would restore it.*|
| DL-200–205 | The six Resolve-First rulings = **DR-1…DR-6** (canonical R2 hierarchy: outcome-first, enforce-via-commitment-gate, integrity indicator, phased resolution, activation=2nd act) | **DRAFTS for ratification** (some DR-4/5/6 already applied in-process) | ⚠️ **owner ratify** the formal records — **RESOLVE-MARKER WITHDRAWN 2026-09-02: this row's own status is "DRAFTS for ratification", and a draft may not answer a citation. Debt recorded in `UNRECORDED_DECISIONS.md` §C; the marker returns when DR-1…DR-6 are ratified as records.** ⚠️ *The marker is not written here in its literal form — writing it would restore it.*|
| **DL-206** | Execution-monitoring tier split (manual→Basic; continuous/sync/programme→Pro; amends DL-083) | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-207** | Plan export & PM-tool tiering (file export=Free · one-way push=Basic · two-way sync+monitoring=Pro; **realizes DL-206** §2/§4, extends DR-7/DL-083) | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-208** | Pro program / cross-plan **execution-cognition** scope (Bundle A: roll-up · dependency mapping · program monitoring, program-envelope cap; aggregate never a health score) + **Pro price set $79** (amends DR-7, drops placeholder; adopts US "program") | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-209** | Load-bearing sensitivity + issue-classification/resolution model — 5 first principles (load-bearing = magnitude-sensitivity ≥ calibrated threshold; **only verify moves Grounding**; verify/build/decide), L0–L4 architecture (deterministic core + thin learnable calibration), global-threshold-with-dormant-segmentation; **completes DL-196/197** | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-218** | **A band must be EARNED — too few load-bearing details cannot buy the top band** — found pre-launch with **zero production data** (`CALIBRATION_READINESS_PLAN_2026-08-12.md` §1): a 1-detail plan jumped **Fragile → Sound on one confirm** (4 bands); N=2–3 jumped two; N≥4 well-behaved. **"Sound" keeps meaning 100% grounded** — deliberately NOT made size-aware (a threshold varying invisibly with plan size can't be explained: *"why is mine Sound at 38/40 when hers needed 6/6?"*). Instead a **minimum-N floor**: below `N_MIN_FOR_SOUND` the read caps at Developing **and says why** ("only 2 load-bearing details — too few for OSLO to call this Sound"); never lowers an earned band; monotonicity holds at every setting. `N_MIN_FOR_SOUND` (provisional **4**) ships **owner-open/quarantined** per DL-209 L4. Guard **GT-71**; RB-050. **Class: Altering** (changes band computation) | **Ratified** (2026-08-12) | ✅ [R]|
| **DL-217** | **An unclassifiable finding is DISCLOSED but never SCORED — and escalates to governance as a model gap** — closes the runtime hole found by the model-robustness run (`MODEL_ROBUSTNESS_REPORT_2026-08-12.md` §3): a finding whose structural target the model can't map correctly got **no** dimension (DL-210 holds) but appeared on **no user surface** while open in the model — hidden, not escalated (**DL-214 §1 violation**). Now: a pinned **"Needs OSLO's attention"** tray shows headline · location · severity · exposure with "not scored into any pillar", excluded from every band, integrity and ledger count; never silently dropped; never a dumping ground (count above threshold = governance escalation); build-time `issueLayerUnified` protection stays. **Internal loop (owner requirement):** every failure emits a model-gap record → aggregated by target signature, ranked frequency × exposure → triaged as *extend the model* (DL-210 amendment via Framework 001), *out of scope*, or *known-unknown* → classification re-derives affected findings so the user sees them rejoin the read; critical/threshold breaches alert immediately. Guard **GT-70**; capability **#26**; RB-049 | **Ratified** (2026-08-12) | ✅ [R]|
| **DL-216** | **An overloaded outcome is disclosed at SAVE; the owner chooses the root (never OSLO)** — closes the edit-path gap (multi-outcome detection ran only at intake; an overloaded root silently corrupted every top-down Alignment finding per DL-210). When typed outcome text carries 2+ distinct outcomes, the save **discloses and asks** instead of committing: the owner picks the steering root, the other is **preserved as a declared secondary** (declaring is free), and **"keep as one"** is a recorded owner call (compound-accepted, never re-asked). Guardrails: **semantic judgment never keyword matching** (retired `_splitOutcomes` stays retired), **silence under uncertainty**, never a paywall moment (DR-7), one ask per text, both edit surfaces (app + arc), never blocks. Guard `outcomeOverloadNeverSilentlySplit`; RB-048 | **Ratified** (2026-08-12) | ✅ [R]|
| **DL-215** | **Viability measures FORM, never PROVENANCE (amends DL-210)** — Viability weakness = missing/malformed structure (an open structural finding), never a well-formed line resting on inference; provenance is **Grounding's** dimension (routes to grounding items per DL-214 Part 3, clears only by verify). Retires the 2026-08-07 **CEILING FIX** (a build flipping provenance as a rider); the read reaches Sound by **verifying** the promoted `metricset`/`effort` items. `artWeak` (form: `_ART_STRUCT`/VSTATE + boundary decision-state) split from `artInferred` (provenance: drives false-confidence Grounding issues). Opening bands re-tuned (Viability opens Weak — the honest form/provenance split). Realized same day: guards **GT-62/GT-63**, browser-verified Sound-path | **Ratified** (2026-08-11) | ✅ [R]|
| **DL-214** | **Finding-ordering honesty invariant + dependency/frontier resolution model** — **"ordering may gate ACTIONS, never TRUTH"** (Durable Invariant, beside DL-213): a finding-ordering layer must keep a **truth layer always complete** (every load-bearing finding's dimension·exposure·status disclosed, the gate always visible, depth honest) while only the **action/CTA is sequenced**; bias-to-disclosure, "blocked" ≠ "lower-stakes". Plus the **finding-dependency/frontier model** (atomic findings · peer-vs-prerequisite edges · topological frontier · one act per finding, build≠ground-bundle · re-derive every act · escalate unclassifiable; cycle→anchor-escalate, empty-frontier→escalate, reopening→provenance, accept-unblocks, advisory-not-gate). Extends DL-209/210/211; realization is **Altering** (not built). RB-047, 12-scenario acceptance suite | **Ratified** (2026-08-11) | ✅ [R]|
| **DL-213** | **Lifecycle honesty wall** (Durable Invariant) — forecast + delivery-health render only in the **Execution/Validation** phases, never in **Planning**, and **never recolor the maturity band**; maturity (readiness, single-hue) and delivery-health (RAG, actuals) are distinct axes; a forecast always ships with its uncertainty range; live data carries provenance (synced/entered/estimate). Ratifies the honesty constraint governing the "Your Outcome" lifecycle console (`DESIGN_PROPOSAL_your-outcome-console-lifecycle.md`); extends maturity-not-forecast / single-hue / manufactured-confidence. Guard via `guard-add` when Execution is built. Does **not** authorize the build (Part A = R2.x altering; Part B = new Pro epic per DL-206) | **Ratified** (2026-08-11) | ✅ [R]|
| **DL-212** | **Establish Framework 002 — Release Lifecycle & Change Control.** Phase machine (Open→…→Retire); R2.x = Build-phase change control over the frozen baseline; **Freeze Manifest** + three-class change model (neutral/additive/altering) + **push-via-labeled-PR** delivery (`altering` gated on dev-lead approval, convention to start); **Refinement Ledger** (mirrors merged PRs); **Durable Invariant Registry** (spine never regresses); skills `release-refine`/`guard-add` to follow. Companion to Framework 001 (decisions) | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-211** | **Proposal-resolution model** — proposals split **build** (adds a missing structural element → accepting resolves the finding + may firm the band via reanalysis) · **inference** (accept OSLO's guess → additive, grounds only by verifying) · **optional** (additive); **cross-surface resolution sync** (one finding, one resolution, any surface, only reanalysis resolves); multiple resolvers close only when all accepted (keynote-backup = requirement + task); **itemized atomic findings** (never merged); amends `proposalsFoldedIntoRead`; guards GT-51…GT-54 | **Ratified** (2026-08-09) | ✅ [R]|
| **DL-210** | CAF dimension boundaries + **deterministic structural-target dimension assignment** (Clarity=definition · Alignment=edge/relational · Feasibility=achievability; Clarity→Alignment→Feasibility precedence); **Alignment relational**, top-down outcome→roots; escalation model (runtime→user clarify/verify · model-gap→governance + leverage-gated known-unknown, load-bearing gap ceilings integrity **incomplete not Fragile**); **amends CAF Positions #10/#11** (preserves #2/#13); reconciles DL-209 decompose ⇄ CAF multi-dimension by layer; extends DL-209/Slice 10, guards GT-45…GT-50 | **Ratified** (2026-08-09) | ✅ [R]|
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

# Slice Signoff — OSLO R1

| Slice | Status | Prototype | Docs | Open P1/P2 | Signed off |
|---|---|---|---|---|---|
| 1 · Access & Onboarding | **Signed off** (re-applied D049 term) | vertical-slices/slice-01-access-onboarding/prototype.html | 7 slice docs ✓ | none | 2026-07-09 |
| 2 · Intake & Fast-Pass Orientation | **Signed off** | vertical-slices/slice-02-intake-fastpass-orientation/prototype.html | 8 files ✓ | none | 2026-07-09 |
| 3 · Project Overview & Understanding Console | **Re-signed** (reopened for DL-143→156; re-grilled to the frozen build) | acceptance vs frozen `slice-10/prototype.html` a327d702 (157/157) | **7 docs regenerated** ✓ (20 e2e · 29 SC) | none | **2026-07-20** (orig 2026-07-09) |
| 4 · Attention Map (MRI) | **Signed off** | vertical-slices/slice-04-attention-map/prototype.html | 8 files ✓ | none | 2026-07-09 |
| 5 · Plan Artifacts / Artifact Workspace | **Signed off** | vertical-slices/slice-05-artifact-workspace/prototype.html | 8 files + editor gap fold-in | none | 2026-07-09 |
| 6 · Issues & Recommendations (Panel Model) | **Signed off** | vertical-slices/slice-06-issues-recommendations/prototype.html | 8 files + shell/palette + fixes | none | 2026-07-09 |
| 7 · History & Confidence Trend | **Signed off** | vertical-slices/slice-07-history-trend/prototype.html | 8 files + D101 refinements | none | 2026-07-09 |
| 8 · Multi-Project Workspace & Awareness | **Signed off** | vertical-slices/slice-08-workspace-awareness/prototype.html | 8 files + D107 refinements | none | 2026-07-09 |
| — · OSLO Chat integration (cross-cutting) | **Done** (D108 cascade to Slices 2–8; D109 refinements in Slice 8) | all slices 2–8 | analyses + docs | none | 2026-07-09 |
| 9 · Collaboration, Sharing & Export | **Signed off** (D110–D132) | vertical-slices/slice-09-collaboration-sharing-export/prototype.html | 9 files ✓ | none (3 owner-open, not blocking) | 2026-07-10 |
| 10 · Tiering & Limits **(THE DELIVERABLE)** | **Signed off** (D134–D142) · **DL-103 folded in 2026-07-12** | vertical-slices/slice-10-tiering-limits/prototype.html | 7 files + edge-cases + open-items + **tier-definitions-census.md** | none (owner-open values → §"Final state") | **2026-07-12** |

---

## RE-GRILL PASS — 2026-07-20 (post-freeze, docs-only; freeze intact)

R1 was frozen 2026-07-20 at `slice-10/prototype.html` **md5 a327d702 · 157/157** after the DL-143→156 enhancements (reports trio + depth/export; the execution-ready planning direction; the Overview two-beat journey). Those landed as canon + into the frozen prototype but the **per-slice test plans** predated them, so impacted slices are being re-grilled to the frozen build (no product change — regenerating specs/test plans only).

- **Slice 3 · Project Overview & Understanding Console — RE-SIGNED 2026-07-20.** 7 docs regenerated to the frozen build (full current Overview: two-beat journey arc · persistent Outcome Confidence read · Option C CAF · maturity ladder · lead-line · beat-aware Start here · chip/popover trust-check). Stale surfaces removed (0–100 index, "How this is calculated" pill, Orientation▸Expanded▸Validated stages, "Extended Analysis"). Test plan = **29 success criteria + 20 e2e** with guards/doctrine baked in. Worker-generated, owner-ratified. *(The slice-03 folder's own `prototype.html` remains the historical cumulative-through-3 snapshot; acceptance is against the frozen slice-10 build.)*

- **Slice 11 · Execution-Ready Planning & Export — SIGNED OFF 2026-07-20 (NEW slice).** Fresh grill from the frozen build (DL-145→151): authored graded task tree · task-altitude ISS-10/11 · computed critical path · the eighth "Full plan" consolidated view · structured Asana export (the plan crosses, OSLO's analysis stays in OSLO) · the DL-145 identity. Boundaries A/B owner-accepted (task-editing mechanics → Slice 5; share/reader-export → Slice 9, distinct object D107). Test plan = **35 success criteria + 20 e2e**. Two DL-body stale-example notes surfaced (DL-146 "4"→ build renders **3**; DL-149 "7 of 29"→ build computes **7 of 23**) — the build is correct, the DL example numbers drifted. Worker-generated, owner-ratified. New folder `vertical-slices/slice-11-execution-ready-planning-export/` (7 docs).

- **Slice 5 · Plan Artifacts / Artifact Workspace — RE-SIGNED 2026-07-20.** 7 docs regenerated to the frozen build (generic editor mechanics current: explorer · type-aware tables · autosave/event-driven reanalysis · From OSLO/Confirmed-by-you flip · weakness stepper). The WBS authored task tree documented as *carried + edited via the unchanged engine*; model/decomposition/critical-path cross-ref Slice 11 (Boundary A). Test plan = **24 SC + 20 e2e**. No flags.
- **Slice 6 · Issues & Recommendations — RE-SIGNED 2026-07-20.** 7 docs regenerated (Map⇄List DL-136 · panel · lifecycle-not-a-ratchet D094/D088 · Apply/withdraw D191-193 · clarification one-door · CAF drill DL-116 · Alignment live D133 · task-altitude ISS-10/11 through the engine, cross-ref Slice 11). Test plan = **33 SC + 20 e2e**. Docs follow the build over brief imprecisions (ISS-10/11 carry real `rectype`/`ftype`, resolve via confirm/options not a clarification Q&A).
- **Slice 9 · Collaboration, Sharing & Export (+ Reports) — RE-SIGNED 2026-07-20.** 7 docs regenerated (sharing/roles/seats · comments append-only · the one export modal, currency+disclaimer, D107/D112 · Strategic Readout tailor-the-ask · the **Reports trio** + Summary/Full depth DL-144 + Decision Record D088 "taken up"). Asana execution-export cross-ref Slice 11 (Boundary B, distinct object D107). Test plan = **27 SC + 20 e2e**. Surfaced pre-existing owner-open items (report scheduling · report branding tier · collaborator seat caps — illustrative/owner-TBD, a Slice-10 tier subject) + a harmless duplicate `openExportSeam` stub (left per freeze-intact).

**✅ RE-GRILL PASS COMPLETE 2026-07-20** — every impacted slice is current to the frozen build (a327d702 · 157/157): **Slices 3 · 5 · 6 · 9 (+Reports) · 11**. See `RELEASE_1_BUILD_SPEC.md` freeze marker + `vertical-slices/slice-10-tiering-limits/RECONCILIATION-2026-07-20-DL143-156.md`.

## FINAL STATE — 2026-07-12 · engagement closed

**DL-102, DL-103 and DL-104 are RATIFIED canon.** The package is closed against them.

| Decision | What it settles |
|---|---|
| **DL-102** — Controlled Release & Tiering-in-Alpha | The **invite IS the authentication** (token-granted Reviewer Principal, DL-049) · **CR-2: bound seats, never bound evidence** — load-bearing, and the **sole** resolution of the CHG-061 conflict · two limits never conflated (D124) · never meter the epistemic record, never sell safety (D128) · no eviction on downgrade. |
| **DL-103** — Analysis cost basis & tier re-derivation | **Never tier judgment quality** (doctrinal) · the §4c numeric basis is **suspended** — the ladder was priced on rented frontier tokens **one day after canon ratified local inference** (DL-069) · **E1–E3 commissioned** (~12 → ~74 analyses at the same $3) · **one honest limit, in analyses** · §7 — the Free→Basic conversion model (*meter the inputs and the outputs; never the understanding in between*; **latency struck**; assisted-apply retained; **outcome pricing prohibited**; **reporting is the #1 lever — a STATUS lever**). |
| **DL-104** — Errata to DL-103 | DL-103 **contradicted itself** (§7c struck the priority queue; §7e/§1/§5 still assumed it) — **and the Slice-10 build could not implement it. That is how it surfaced.** Residue struck · **UP-1/UP-2/UP-5 retired at source** · **UP-APPLY + UP-REPORT numbered** · **DL-102 E refreshed** · **new P1 defect class:** any report mistakable for a health rating / RAG / readiness / probability of success. |

### DL-103 fold-in — Slice 10 (the deliverable), 2026-07-12

The tier model Slice 10 was originally built on was **superseded before sign-off dried**. It was rebuilt, not patched:

- **Prototype → 13,237 lines.** The per-tier `ROUTING` ladder is **struck** → `MODEL_ROUTING_BY_STEP`; every "Pro is where
  the models get better" line is gone. Pro = **execution & programme support**.
- **One honest limit.** The token governor is gone; the budget is **in ANALYSES, never tokens**, and renders **pending
  re-derivation — nothing enforced**. **Chat is uncapped on every tier.** UP-1 / UP-2 / UP-5 removed from the prompt
  table outright (a prompt that merely *cannot fire* is a prompt somebody re-wires).
- **UP-APPLY** built with **no cap** (threshold owner-TBD, from Alpha instrumentation, never a cost model) and the binding
  line enforced: *recommendation always visible · only the assisted apply is metered · manual editing always free*.
- **"Update now" is free on every tier** — no tier check exists in `updateNow()`, and none may be added.
- **NEW: the Reports surface** (nav + modal + `REPORTS` registry) — reliability-qualified throughout, currency-marked,
  standing disclaimer, **packages, never produces** (generating a report runs **no** analysis), report names labelled
  descriptively and flagged *"naming pending"*.
- **The retired levers are shown as struck, out loud, on the Plans page** — the priority queue is named as *"the upgrade
  we deliberately did not build"*; outcome-based pricing is named as prohibited.
- **Boot guards → 17/17.** Eight new ones added by this fold-in: `noTierQuality` · `budgetInAnalyses` · `chatUncapped` ·
  `recNeverHidden` · `updateNowFree` · `noLatencyLever` · `downgradeKeepsRead` · `noOutcomePricing` · `reportsNoHealth`.
  They are the doctrine, executable — each fails loudly if a future contributor undoes it.
- **Census → 58 values: 39 ratified · 3 pending re-derivation · 8 retired/struck · 5 unset · 3 recommendation.**
  Struck values are **kept, visibly struck**, so nobody re-derives them from a blank in six months.

**Verification (final):** `node --check` **PASS** (9,929 JS lines) · jsdom body children **32** · **17/17 boot assertions**
· **0 console errors/warnings** · `prototype-index.html` **11/11 links resolve**.

**Escalations raised by the fold-in (T10-8…T10-12) were all resolved by DL-104** — the priority-lever residue, the Pro
"+ speed/priority" claims, the stale UP-* taxonomy, the health-framing P1 class, and DL-102 E's staleness.

**Still owner-open** (nothing assumed; each renders visibly unset): monthly analyses (Free/Basic) · Basic price **basis** ·
UP-APPLY threshold · collaborator seats (Basic = 10 withdrawn as cannibalizing a per-seat Team) · OD-10 coalescing window ·
Free CRR cost ceiling · MON-04 global prompt cap · report names · which reports are R1 / scheduling / branding / `REP-*`
rows · billing rail · CR-2-vs-budget-gate (*record · defer · disclose*, recommended) · reverse-trial duration.
See `final-package-summary.md` §5.

---

## Slice 10 — signed off 2026-07-11 · FINAL SLICE, and the deliverable
*(The record below is the sign-off as it stood before the DL-103 fold-in. Retained; superseded where it conflicts with
the Final State section above — the correction must stay legible.)*
Decisions **D134–D142**. Governing rule: **canon decides; the build adopts and cites; zero tier numbers invented.**
Live Free→Basic tier in Alpha (D135; `BASIC_PRICE = null` renders owner-TBD; Pro named, not purchasable) · honest counters with real reset times (D136) · the full **UP-1…UP-8** prompt engine with all four MON-04 global guards (D137) · **the limit-reached rule at every cap** — controls stay enabled, the *attempt* is gated, every prompt names the specific limit **and** the specific tier that relieves it (D138) · partial-orientation disclosure on one surface, envelope unset (D139) · **`tier-definitions-census.md`** — 32 values, **21 ratified · 11 UNSET** (D140) · **D141: Basic = 3 projects (UP-3)**, correcting the AI-invented 10, with every displayed tier number now painted from its constant.
**Slice-9 defects corrected:** the seat cap **blocked** instead of prompting; non-PDF export buttons were `disabled`; the persistent sidebar "Upgrade" button was upgrade wallpaper (MON-04) — all fixed. A real bug was also found and fixed: typing a new reviewer's email into the CRR dialog wiped the input on every keystroke — it broke precisely the path CR-2 exists to protect.
**Consolidation pass (2026-07-11):** terminology sweep (user-facing "finding" → **Issues**, DL-095/D017 · "Fast Pass" → **Initial Analysis**, D012 · mechanism-language "reanalysis" → **analysis update**, D092) + four hard-coded tier numbers repainted from their constants (D141 anti-drift).
**Verification:** `node --check` PASS · jsdom body 31 · **6/6 boot assertions** (`window._S10`) · **0 console errors** · handler integrity 292/292 · light-mode AA PASS · non-regression 10/10 slices.
**Escalated, not invented:** the 11 UNSET values · the missing `RELEASE_1_TIER_DEFINITIONS_V1` (DL-102 Concern 7 — blocking Basic in Alpha) · **T10-2** (UP-5 caps an affordance D006 forbids) · **T10-3** (seats/export have no UP slot) · **T10-4** (MON-04's global prompt cap is never set) · Suggest-Alternative alignment signal (deliberately unbuilt) · whether revenue expands onboarding capacity (would reopen CR-7).

## Slice 9 — signed off 2026-07-10
Decisions **D110–D132**. Sharing (Owner/Collaborator/Viewer + view-only snapshot link) · threaded comments + @mentions on issues (append-only; "Comments never change the assessment") · export snapshot (currency marker + disclaimer; Free = PDF-only) · collab notifications un-gated · **CRR-01…05 reinstated as ratified canon** (my earlier "spec gap" escalation was wrong: DL-049 had already resolved gap #337) · **D115** third epistemic class "Attested by <name>" — evidence, not truth; never auto-resolves; OSLO never self-accepts · **controlled release + waitlist** (D119–D126) · **tier live in Alpha** (D123) · **two-limit model, never conflated** (D124) · **never meter the epistemic record; never sell safety** (D128) · seats/viewers/refunds/no-eviction (D129–D132) · **dark default** (D127).
**Governing principle (D126):** *Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.*
**Defects caught & fixed:** Share-for-review disabled itself at the cap (D120 violation); Plans/Settings were **selling the epistemic record** ("more artifacts", "longer retention") — deleted, with comment guards + runtime assertions so neither can be reintroduced.
53/53 behavioural assertions pass. **Zero escalations carried out.**
**Owner-open (not blocking):** Basic price (T-3) · "Does a Reject move CAF?" (recommend: yes, via Alignment — needs Framework 001) · whether revenue ever expands onboarding capacity (would reopen CR-7 pay-to-skip).
**Framework 001:** ONE consolidated proposal — *"Controlled Release & Tiering-in-Alpha"* (D131).

## OSLO Chat (cross-cutting, 2026-07-09)
D108 — chat was non-functional (inert composer/Send); made it work + integrated into workflows (context handoff + pill; entry points: Ask-why, Ask-about-issue, **Discuss** on recommendations, artifact/span ask, Attention-cell ask, History "what changed"); clarifications route through one shared path with byte-identical History entries. Cascaded to Slices 2–7 (each wired only to its own surfaces). D109 — epistemic (reliability-qualified, derived/attested) replies, clickable citations, honest capability-scoped fallback (never fabricates), streaming + message actions (copy/retry/feedback/save-to-History), follow-ups, @-mention multi-context, expand mode, persistence. Advisory-only held throughout: chat mutates nothing.

## Slice 8 — signed off 2026-07-09
Decisions D102–D106 (Workspace Home, project switcher, notifications, Settings, Appearance) + D107 refinements (dead Settings links removed → Profile/Workspace/notification-prefs/Account functional; collab notif categories gated; Alpha 1-project dashboard; light-mode AA sweep 21/21 pass; polish) + GA save-bar hidden-state fix. No open P1/P2.

## Slice 7 — signed off 2026-07-09
Decisions D096–D100 (append-only timeline, understanding-over-runs trend, last-good/read-only, version lineage, first-run) + D101 refinements (type-leak removed, run-grouping + what-changed deltas, trend↔timeline link, type filters, polish) + lifecycle Resolved→green fix. No open P1/P2.

## Slice 6 — signed off 2026-07-09
Decisions D086–D095: full Issues surface (Artifact/Dimension/Severity filters + By dimension/severity/artifact grouping), full Issue Panel, Open→Addressed→Resolved, recommendations + Apply this fix (Panel Model), clarification loop, empty states; panel declutter (D092) + drop user-facing "reanalysis"; issue-flyout scroll fix; **persistent left sidebar + top bar (D093) + command palette (D094)** cascaded to Slices 3–5 (D095, which re-signs those under this approval); top/bottom layout fix; annotation-popover stacking fix; link-popover close. History/Share/Export/project-switcher are seams to Slices 7/8/9.
Note: Slices 3–5 re-signed under D095 shell cascade.

## Slice 5 — signed off 2026-07-09
Decisions D066–D085 (type-aware editor, annotations, epistemic notation + table provenance, event-driven reanalysis, weakness→issue stepper, tables add/insert/delete/reorder + columns, phase-bar fix, hover fixes, calm indicator, rich-text toolbar, and the full editor gap fold-in Batches A/B/C incl. undo/redo, reanalysis-merge, cell nav, paste sanitize, slash menu, image embed, a11y reveals, markdown, block drag, find/replace, link mgmt, save affordance, empty states, responsive, action buttons). Verified structurally + syntactically; large owner-directed editor expansion beyond v4 (flagged for canon). No open P1/P2.

## Slice 4 — signed off 2026-07-09
Decisions D057–D062 + feedback (D063 remove Dimensions view; D064 positive description; D065 stale-count/Timeline/how-calc/stage/CAF-hover fixes; D053 rev stage→popover-only; invitation copy → "Intralign Alpha" + AI-first value prop + "from the Intralign team"; Clarification-request casing sweep). No open P1/P2.

## Slice 3 — signed off 2026-07-09
Decisions D050–D056 + feedback fixes (stage sequence render, plain-language how-calc, concise "↗ Strengthened" trend label). No open P1/P2.

## Slice 2 — signed off 2026-07-09
Decisions D035–D048 + prototype revisions R1–R4 (chat notices, feature tour, confirmations→issue, DL-096 Overview reconcile, More=Project summary only, Progress v4-fidelity, "Plan artifacts read"). No open P1/P2.

## Slice 1 — signed off 2026-07-09
Decisions: D021 (Alpha invite-only; anonymous = GA-phase), D022 (invite-gated access, simulated), D023 (4 start methods; Guided Q&A out), D024–D026 (anonymous/save-to-keep/email signup — GA-phase), D027 (one-time orientation + advisory), D028 (logout + illustrative session), D029 (headline A + descriptor), D030 (sample = all-phase user-initiated), D031 (Fast Pass ≈30s), D032 (GA card hidden in Alpha), D033 (accepted file types), D034 (ingestion depth; no OCR R1).
Prototype revisions R1–R4 applied and verified (JS clean). No open P1/P2.
Re-signoff required if reopened: none.

## D049 term change (2026-07-09)
User-facing "Plan sections" → "Plan artifacts" applied across both prototypes + all slice/package docs (decision-log left as historical record). Slice 1 reopened for the copy change and re-applied under owner direction (no behavioral change; re-signed). Slice 2 in review carries the term.

---

## Reopened work items (post-closure)

| Item | Slice / surface | Status | Realizes | Design input | Opened |
|---|---|---|---|---|---|
| **WI-R1 — Strategic Readout composer** | 10 · **Reports surface** | **SIGNED OFF (re-signoff 2026-07-13)** — owner approved (a) | DL-107 (readout spine) · DL-108 (tailor the ask) · DL-104 (P1 guards) | `oslo_r1_experience_mockup_v5_readout_DRAFT.html` (verified) | 2026-07-12 |

**WI-R1 rationale:** Slice 10 signed off 2026-07-12 with a Reports surface, but **DL-108 (tailor the ASK, never the READ) was ratified after sign-off** and the surface doesn't yet encode it; DL-107's five-section readout spine is also not yet folded in. Additive over "packages-never-produces / no-health" (preserved). Detail + acceptance criteria + guardrails + worker task: `vertical-slices/slice-10-tiering-limits/work-item-WI-R1-readout-composer.md`. **Requires owner approval to reopen → worker fold-in → re-signoff of the Slice-10 Reports portion.**


**WI-R1 update (2026-07-12):** worker fold-in complete + verified (boot self-check 58→60 all green; 0 pageerrors before/after = non-regression; new guards `readIdenticalAcrossAudience` + `readoutRunsNoAnalysis` pass; DL-108 invariance proven at DOM level — §1–§3+§5 byte-identical across Practitioner/Sponsor/Executive, only §4 differs). **Finding:** slice-10 already carried a richer seven-section workspace Readout encoding tailor-the-ask (**D145 / D148–D172**), so WI-R1 added a composer variant into the export/snapshot modal (`#sroDoc`, deliberately outside `REPORT_SURFACES`) rather than net-new reporting. **Two open decisions for the owner: (a) re-signoff the Reports portion; (b) convergence — reconcile the new composer's Practitioner/Sponsor/Executive model with the existing workspace Readout `REPORT_RECIPIENTS`, or keep both. Also note the reference `v4` lags the slice-10 build on the Reports surface.**

**WI-R2 — Audience-model convergence (2026-07-13): COMPLETE + verified.** Owner approved (b) — consolidate onto the workspace Readout audience model *if it preserves objectives + Readout UX*. Safety analysis: convergence preserves DL-107/108/104 (invariants are taxonomy-independent) and leaves the `#rptDoc` memo (the anchor) untouched → **no conflict, no conditional stop**. The composer's audience set → the four `REPORT_RECIPIENTS` (Sponsor/Programme/Operations/Executive); internal "Practitioner" dropped (not a memo recipient). Surfaces stay distinct (composer OSLO-facing; `#rptDoc` doctrine-free). **Verified live on device:** prototype 1.90MB, boot 87/0-fail/0-pageerror; DL-108 invariance across all 4 recipients (§1–§3+§5 byte-identical, §4 distinct across all 6 pairs); `readIdenticalAcrossAudience`/`readoutRunsNoAnalysis`/`reportsNoHealth` ✅. **O-WIR1-2 (coexistence) → RESOLVED.** Report: `worker-reports/WI-R2-audience-convergence.md`. **Converged Reports surface RE-SIGNED OFF by owner 2026-07-13.**

**⚠ Concurrency note (2026-07-13):** during WI-R1→WI-R2 a **concurrent process edited the same slice-10 files** (prototype 1.60→1.90MB, boot 60→87). WI-R2 was applied as a **surgical atomic in-place patch** (assert-once-or-abort, backed up) to avoid clobbering ~300KB of that concurrent work — which is preserved. Recommend only one session edit the grill package at a time. Residual: 4 zero-byte scratch files in slice-10 (mount forbids unlink; delete from desktop) + open O-WIR1-1 (report name) / O-WIR1-3 (§4 asks curated).

**WI-R3 — reference `v4` Reports catch-up (opened 2026-07-13):** bring the baseline-of-record `v4` up to the slice-10 converged Reports surface (readout composer, 4-recipient `REPORT_RECIPIENTS` model). Executed as a non-canonical marked draft (`oslo_r1_experience_mockup_v5_readout_DRAFT.html`) → to land in repo `product-design/` via owner-gated PR; reference `v4` not overwritten in place.

---

## REOPEN — 2026-07-14 · WI-R5 (Slice 10 Overview / Progress panel)

**Slice 10 Overview/Progress portion → REOPENED** for the **DL-111 foundation-bar** fold-in. Status: **In review** (docs reconciling to the current prototype). The rest of Slice 10 (Tiering, Reports, Plans) remains **Signed off**. Re-signoff required for the Overview/Progress portion once docs reconcile. Record: `vertical-slices/slice-10-tiering-limits/work-item-WI-R5-progress-panel-foundation-bar.md`.

---

## SIGNOFF — 2026-07-14 · WI-R5 (Slice 10 Overview / Progress panel — corrected)

**Slice 10 · Overview/Progress → SIGNED OFF.** Owner re-signoff of the foundation-bar Progress panel **as corrected** (Decision 251 erratum): hero = grounded/attested only · two provenance states (grounded/inferred) · load-bearing as a superset line, never `+`-joined · population guards.

- **Status:** Signed off · **Slice 10 overall:** fully Signed off again (Tiering/Reports/Plans were never reopened).
- **Signed-off decisions:** DL-111 (foundation bar) as amended by Decision 251 (erratum); Decision 250.
- **Prototype:** `vertical-slices/slice-10-tiering-limits/prototype.html` (R6 build · md5 b5466e98 · 136/136 self-check · 0 pageerrors, both themes).
- **Docs:** frontend-ui · user-experience · success-criteria · e2e-test-scenarios · edge-cases · open-items (all reconciled to the corrected panel) + WI-R5 records.
- **Open P1/P2:** none for the panel. Owner-open (unchanged): the load-bearing/inferred adjacency copy (escalated in open-items) — cosmetic, not blocking.
- **Signoff date:** 2026-07-14.
- **Governance owed (not blocking signoff):** land the canon erratum to DL-111 (`DL-PENDING-progress-panel-erratum-BODY.md`); commit the corrected grill mirror files to the repo.

---

## REOPEN — 2026-07-14 · WI-R6 (Slice 10 Overview / Progress hero)

**Slice 10 Overview/Progress → REOPENED** for the fraction-hero refinement (Decision 252, variant B). In review; docs reconciling. Rest of Slice 10 unaffected. Re-signoff required once docs reconcile.

---

## SIGNOFF — 2026-07-14 · WI-R6 (Slice 10 Overview / Progress hero — fraction)

**Slice 10 · Overview/Progress → SIGNED OFF.** Owner sign-off of the fraction-hero refinement (Decision 252, variant B): hero **"17 of 28"** — grounded/attested **numerator only**, total-claims **denominator as composition** (not a burndown target) · caption *"grounded in your evidence / the rest of your read is OSLO's inference"* · **"Confirmed by you"** retained on the segment (D196 / D194c). **Consistent with DL-112** — no canon reversal, no new DL (Decision 252). Docs reconciled to the live build (11 inferred claims · 12 load-bearing · 28 denominator); doc-integrity eyeball clean (fences balanced, tables intact, canon refs resolve). Prototype **943db40d · 136/136 · 0 pageerrors**; committed + pushed to `main` (`c20ef5b`).

- **Status:** Signed off · **WI-R6: CLOSED.** · **Slice 10 overall:** fully Signed off again (Tiering / Reports / Plans were never reopened).

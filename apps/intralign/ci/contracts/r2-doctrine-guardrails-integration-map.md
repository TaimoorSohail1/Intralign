# R2 Slice 9 — Doctrine Guardrails as Acceptance Tests + the FE↔BE Integration Map — Build Design

*Grill artifact · authored 2026-08-06 · the KEYSTONE slice. It authors no new capability; it **binds and proves** the other eight. Two deliverables: (1) the consolidated **FE↔BE Integration Map** — the single artifact that ends R1's "underdefined" complaint by giving every dynamic UI surface an unambiguous Read / Written-by / Changed-by / Async contract; (2) the **doctrine-guardrail acceptance suite** — the prototype's 59 `_S10` self-checks, every slice's honesty invariants, and the DL-L1…L9 landmines promoted from copy into red-or-green build assertions. Per audit §8: "port the `_S10` guards into real build assertions." Status: **DRAFT — awaiting slice sign-off.***

---

## 1. Locked decisions

| # | Decision | Source |
|---|----------|--------|
| L1 | **Every honesty invariant is a real, running assertion**, not prose. The prototype's 59 `_S10` guards, Slices 1–8's INV-*/HI-*/H* invariants, and the DL-L1…L9 landmines all become tests in one acceptance suite. | audit §8; all slices §5 |
| L2 | **The Integration Map is the keystone contract.** One master table binds every dynamic surface to `{Reads, Written-by (act), Changed-by (event)}`. FE and BE build against this table; a surface not in it is not shippable. | R1 "underdefined" complaint; slices §6 |
| L3 | **A red suite blocks the build.** The guardrail suite is a merge gate, not a report. Any failing doctrine assertion fails CI. | audit §8; owner doctrine |
| L4 | **The `_S10` client guards are the *reference oracle*, not the enforcement.** Each client guard gets a **server-side twin** that asserts the same invariant on the real backend (a DOM/function-shape check client-side becomes a data/permission check server-side). | audit §8; DL-L6 |
| L5 | **The nine DL-L landmines are "developer-builds-the-wrong-thing-by-default" traps** — each gets ≥1 **negative or pinned assertion** that fails loudly if the default (wrong) implementation is written. | audit §3 DL-L1…L9 |
| L6 | **"Only reanalysis resolves" is the spine invariant.** It is asserted per-slice (S1 L13, S2 INV-1, S3 I1) and once globally: no `you`/`fixed`/band/integrity move exists outside `_completeReanalysis`. | S1 L13; S2 INV-1; S3 I1 |
| L7 | **Two classes of negative are *pinned*** (must stay red-if-violated forever): the **no-write projections** (roll-up, grounding-map, generated reports, feedback/survey) and the **never-metered exemptions** (record, reviewer/CRR loop, Viewers). | DL-L2/L6; S6 INV-2; S7 §5.1 |
| L8 | **Neutral-copy / no-numeric-score is a lint pass**, not just a unit test — it scans all rendered strings for a tier name/price on a non-gate surface and for any 0–100 integrity number. | S1 INV-3; S5 HI-7/LD-5.7 |
| L9 | **Placeholders stay explicitly un-asserted.** Owner-open numbers (reanalysis window, delegate matrix, tracker, readiness stats) are quarantined as `pending()` tests that neither pass nor fail the gate until ratified. | S3/S6/S8 §8 |
| L10 | **Every surface declares an async state.** The map carries an **Async** column (Fast Pass · Deep Pass · LLM stream · round-trip · optimistic · static · instant). Because the prototype simulates all backend interaction as instantaneous, a surface with no declared latency treatment is **not shippable** — the latency twin of L2. Detail: `LATENCY_AND_ASYNC_UX.md`. | `LATENCY_AND_ASYNC_UX.md`; S3 |

---

## 2. The consolidated FE↔BE Integration Map

One continuous map. Columns: **Surface · Slice · Reads · Written-by (act) · Changed-by (event) · Async**. `—` in Written-by marks a **read-only projection** (pinned no-write, L7). The spine rule: *the only event that ever changes a band/resolution is reanalysis (`reanalysis.landed`)*.

**Async column legend** (how backend delay shapes the surface — full detail in `LATENCY_AND_ASYNC_UX.md`): **A** Fast Pass (staged progress + skeleton) · **B** Deep Pass (ambient indicator + supersession notice) · **C** LLM stream (thinking → token stream, input locked, cancel/timeout) · **D** round-trip (action-pending → async confirm with a server result + error/retry, control disabled in flight) · **O** optimistic act (recorded → pending reanalysis → resolved — already built, Slice 3) · **S** static display (reflects last analysis; skeleton on first load; updates on `reanalysis.landed`) · **—** instant / client-only. Combined codes read left-to-right (e.g. `C → O` = LLM draft, then optimistic pending).

| Surface | Slice | Reads | Written-by (act) | Changed-by (event) | Async |
|---|---|---|---|---|---|
| Masthead integrity indicator (ordinal band + pending) | 1 | `Integrity.level`, `.posture` | — | `reanalysis.landed` (`min()` recompute) | S |
| Named limiting pillar | 1 | `Integrity.limitingPillar` (foundation-first tie-break) | — | `reanalysis.landed` (new floor) | S |
| 3-pillar decomposition chips | 1 | `Integrity.decomposition[*].band` | — | `reanalysis.landed` after any issue resolves | S |
| Pillar drill (chip → issues) | 1 | `openIssues()` by `dim` | resolve/attest → enqueue | resolve → `reanalysis.landed` | S · O |
| Read worklist ("Your next move", exposure-ranked) | 1 | `openIssues()` sorted `_issueExposure` desc | act on a row → enqueue | issue open/resolve → re-rank on `reanalysis.landed` | S · O |
| Viability / Grounding / Adaptability value | 1 | `f_V` / `f_G` (+root cap, ISS-FC set) / `f_A` → band | CAF-resolve / ground-attest / register-checkpoint | `reanalysis.landed` | S |
| Read item card (Inferred) | 2 | `openIssues()` `state='inf'` | `decide`/`quickConfirm`/`applyFix`/`routeTo` → enqueue | `reanalysis.landed` (batch) | S · O |
| Basis picker | 2 | `BASIS` enum | `confirmBasis`→`itemAct('confirm',{basis,evidence})` | `reanalysis.landed` | O |
| **"Acted on · not yet closed" folder** | 2 | `_needsFixItems()` (both kinds; `_nfKind`) | `fixFromFlag` (fix) / `groundMitigated` (ground) / `withdrawItem` | `reanalysis.landed` → Resolved | C → O |
| **Resolved tray** | 2 | `state === you(!flagged)` only (+ firmed V/A) — **`fixed` excluded** (INV-9) | `withdrawItem` | `reanalysis.landed` (settle) | S · O |
| Withdraw control | 2 | `Attestation` history | `withdrawItem`/`withdrawRoute` → **append** | live state reverts; ledger retained | O |
| Discussion panel | 2 | `comments[]` (isolated) | `postComment`/`cmMention` | **never** changes a band (INV-4) | D |
| Provenance line ("Confirmed by you/{name}") | 2 | `attestedBy`, `basisNote`, `flagged` | resolved-state render | `reanalysis.landed` | S |
| Act button (confirm/flag/route/fix/answer) | 3 | — | `POST /acts` → `addressed`, enqueue, STALE | never returns a new band | O |
| "recorded · pending reanalysis" + Undo | 3 | `ReadFreshness.state`, `pending_count` | `DELETE /acts/{id}` (`undoPending`) | STALE↔FRESH transition | O |
| "Reanalyze now" | 3 | — | `POST /reanalysis:run` (bypass debounce) | `reanalysis.landed` | O |
| Band "updating…" + pillar/band flash | 3 | `pending_count>0` | — | `reanalysis.landed` → `prev/new_integrity`, `rose[]`, `settled[]` | O |
| "your read moved" durable banner | 3 | `GET /notifications?type=read_moved` | — | `reanalysis.landed` when delayed/away only | S |
| First-run frozen workspace | 3 | `GET /workspace` → `first_run`, `confirm_count`, `ever_unlocked` | client-side freeze only | `activation.unlocked` (latch) | — |
| Unlock reveal | 3 | `ever_unlocked` | — | `activation.unlocked` (once) | — |
| First read render | 3 | Fast-Pass output = L1a (7 artifacts + outcomes + 3 pillars) | — | `reanalysis.landed` (fast) | A |
| Deep-Pass supersession | 3 | superseded findings | — | `reanalysis.superseded` (append-only) | B |
| Commitment-gate modal (`_payGate`) | 4 | `GET /entitlement` → capability + price (config) | — | `gate_hit` + `intent_signal` | D |
| Checkout (`_openCheckout`→`_commitPay`) | 4 | hosted-checkout session | "commit to pay" → `POST /commitments` | `checkout_committed` → `entitlement_granted` | D |
| Outcome-cap wall (`vmOutcomeCap`) | 4 | slot state | `POST /outcomes` → **422 at cap** (drives gate) or free path | `gate_hit` / `outcome_archived` | D |
| Archive / reactivate (`vmArchiveSwitch`/`reactivateOutcome`) | 4 | slot availability | `POST /outcomes/{id}:archive` / `:reactivate` | `outcome_archived`/`_reactivated` (**never metered**) | D |
| Reveal confirm card (primary only) | 5 | Fast-Pass primary confirm-ready + prov | `_confirmOutcome` → attestation + `confirmCount++` | `reanalysis.landed`; `activation.*` | A · O |
| Held-count note (Intent) | 5 | `_heldOutcomes().length` (rows suppressed) | — | `_ocDisclosed` flip (disclosure) | S |
| Disclosure nudge | 5 | `_ocNudgeEligible` (engaged && !frozen) | `_discloseOutcomes`/`_dismissOcNudge` (persist per-user/plan) | engagement signal; fire-once | — |
| Secondary rows (post-disclosure) | 5 | `_visibleSecondaries` | `_setPrimaryOutcome` / "optimize" → `vmOutcomeCap`→`_payGate` | `gate_hit` (declaring free) | O · D |
| Primary-edit re-flag | 5 | `outcomeStale` on inferred goals/metrics | `_grReReadFromOutcome` → enqueue | `reanalysis.landed` clears stale | O |
| Ask-for-evidence composer | 6 | `PM_CONTACT`/`EXT_CONTACT` | `routeTo(k,'pm'\|'ext')` → `review.requested` | scope token minted; enqueue on reply | D |
| Awaiting-evidence group (`_awaitingGroup`) | 6 | `state='routed'`, `routedTo` | `respondRoute`/`withdrawRoute` | reviewer reply → `reanalysis.landed` | S |
| Scoped reviewer surface (external) | 6 | scope token → `{question,source}` ONLY | reviewer confirm/reject | **403 on anything else** | D |
| Roll-up door (`rollupDoorHTML`/`_ovwDoorHTML`) | 6 | `min(V,G,A)`, risks, ledger, reviewer state, `_ownsOutcome()` | **—** (pinned no-write) | `rollupGo` deep-link into read | S |
| Grounding map (`groundMapHTML`) | 6 | `_mapNodeState(it)` | **—** (pinned no-write) | `_openMapItem(k)` opens the issue | S |
| Redesigned share panel (`doorBody('share')`) | 6 | `_shareRecipients`, `_shareReviewerCount/Rows`, folds | `shareAddRecipient`/`shareRevoke`/`shareCopyLink` | `share.created`/`.revoked` (Viewers **unmetered**) | D |
| Invite (`inviteToRead`/`shareInvite`) | 6 | `attestedBy` (fresh external) | `invite.drafted` → user sends | honest "awaiting them" (never "joined") | C → D |
| Awareness feed (notif door) | 6 | `HISTORY`, salience filter | — | `notify.routed_response` surfaces; comments quiet (DL-166) | S |
| Report tabs (1 authored + 3 generated) | 7 | `GET /reports?planId`; generated = projection | — | none on render (no compute) | S |
| Depth toggle (Summary⇄Full) | 7 | `_repDepth[k]` | `setRepDepth` (client view param) | no round-trip | — |
| Generate / author / edit briefing | 7 | draft state | `genReportDraft`/`_reportOnEdit`/`regenReport` | `report.generated`/`.edited` (never touches read) | C |
| Send memo | 7 | read signature | `sendReportMemo` → immutable `ReportSnapshot` | `report.sent` (stale-flag when read moves) | D |
| Export format picker (`_EXPORT_FMTS`) | 7 | PDF/Asana/Copy | `_setExpFmt` → `POST /exports` | `export.rendered` | D |
| Export optimized-for scope (`_exportScope`) | 7 | `_TIER`, primary resolver | multi-outcome → Slice-4 gate | `gate_hit` (Free) | — |
| Export readiness signal (`_exportReady`) | 7 | `min(via,grd,ada)` | — (disclose only, never gates) | `reanalysis.landed` | S |
| Export reanalyze-if-pending (`_exportGuard`) | 7 | `_pendingCount()` | one consolidated re-read if pending | `export.guard.reanalyze` → `reanalysis.landed` | A |
| Export render/done | 7 | package (D153 cover) | `_doExport` → History (fmt + optimized-for + band) | `export.done` | D |
| PM-tool hand-off (`exLeaves()`) | 7 | executable plan `{task,owner,dates,provenance}` | Asana/MS-Project/Smartsheet connector | connector push (no read fields cross) | D |
| Schedule on/off | 7 | `_reportSched` | `toggleReportSchedule` (Basic) / `_scheduleSendNow` (free) | `schedule.toggled`; `schedule.send`→currency re-read | D |
| Feedback door | 8 | — | `submitFeedback` → `POST feedback_svc/tickets` → sanitize | `feedback_filed` (no free-text in event) | D |
| "Filed this session" list | 8 | `GET feedback_svc/tickets?session` | — | tracker status back-sync | S · D |
| Defect auto-context | 8 | client-assembled allowlist metadata | `_fbContext` (metadata only) | — (no plan read) | — |
| Survey door | 8 | — | `submitSurvey` → `POST feedback_svc/survey` → sanitize | `survey_responded {pmf,csat,variant}` | D |
| Survey nudge (fire-once) | 8 | `GET funnel/eligibility` (durable per-user) | `openSurveyFromNudge`/`dismissSurveyNudge` | eligibility (activated+engaged, honors dismissal) | S |
| A/B assignment | 8 | `GET experiments/assign(survey_timing)` (sticky) | — | stamped on every survey event | — |
| Grounding-act emitters | 8 | `confirmCount++` in `itemAct`/`routeTo`/confirm-outcome | `POST telemetry/grounding_act` | `funnel_initiated/_activated/_engaged` | — |
| Intent walls (`_recordIntent`) | 8 | wall context | `POST telemetry/intent_signal` (+ History, L9 exemption) | `intent_signal` | — |

**Zero-unbound rule:** the acceptance suite enumerates every dynamic surface in the shipped read and asserts each appears in this map with a non-empty Reads column, a Changed-by that is either `reanalysis.landed`, a side-channel event, or `—`, **and a non-empty Async code** (L10). An orphan surface, or a surface with no declared async treatment, fails the gate (AC-1, AC-11).

---

## 3. Doctrine-guardrail test register

`Test ID · Doctrine · Assertion · Source · Type`. Types: **unit** (pure computation), **integration** (act→reanalysis→resolve flow), **negative** (must fail if the wrong-default is built; *pinned* = permanent), **lint** (string/copy scan).

| Test ID | Doctrine | Assertion | Source | Type |
|---|---|---|---|---|
| GT-01 | Enforce-mode not observe | 2nd active outcome at Free blocks → names capability + $29/mo → real checkout before grant; no silent 422 bypass, no silent grant | DL-L1 / S4 INV-4,6 / `commitmentGatePresent` | integration |
| GT-02 | Never-metered exemptions | Reading a record, routing to a reviewer, adding a Viewer succeed at `free` with **zero** `gate_hit` and no entitlement check | DL-L2 / S4 INV-1, S6 INV-3 / `archiveIsARealFreePath` | negative (pinned) |
| GT-03 | Reversible archive | archive→reactivate restores with nothing deleted; record readable in both states | DL-L3 / S4 INV-2 / `archiveIsARealFreePath` | integration |
| GT-04 | Freeze presentation-only | Read API returns the full read irrespective of `confirmCount`; freeze is client-only | DL-L4 / S3 I7, D9 | negative (pinned) |
| GT-05 | Feedback free-text sanitized | A defect body carrying a known plan figure is redacted at feedback-service egress before the tracker call | DL-L5 / S8 H2 / `defectTicketFormat` | integration |
| GT-06 | Feedback/survey isolation | `feedback_svc` principal has **no write grant** to plan/finding/attestation/History; an attempted write raises a permission error | DL-L6 / S8 H1 / `feedbackCapturePresent` | negative (pinned) |
| GT-07 | Integrity gate vs Non-Collapse | The `min(V,G,A)` composite supersedes IR-4/IR-8 for the composite only; a floor-to-Fragile band still renders maturity framing, never RAG/health | DL-L7 / S1 L2,L8 / `integrityIsWeakestGate` | unit |
| GT-08 | Reviewer scope enforced | A scoped token authorizes `{question,source}` ONLY; any other resource → **403** (access-control, not display) | DL-L8 / S6 INV-1 / `sharePanelSimplified` | negative (pinned) |
| GT-09 | Activation survives withdraw | Emit activation, withdraw below threshold → live freeze may re-lock but the activation event persists immutable | DL-L9 / S2 L8, S3 I3, S8 H6 / `unlockLatched` | integration |
| GT-10 | Only reanalysis resolves | No terminal `you`/`fixed`/integrity move exists outside `_completeReanalysis`; a click ends at `addressed`/`routed` only | S1 L13 / S2 INV-1 / S3 I1 / `needsFixFork` | negative (pinned) |
| GT-11 | Flag ≠ Viability | After a flag, the linked statement stays `inferred`, `artWeak` stays true, Viability band unchanged; Grounding item-credit rises | S1 INV-1, S2 INV-3 / `confirmFlagSymmetry` | unit |
| GT-12 | Comment never grounds | A comment/@mention leaves state, `prov`, basis, and every band unchanged; the issue stays open | S2 INV-4, S6 INV-4 / D133/CR-2 | negative (pinned) |
| GT-13 | Bands normalize to plan size | Proportionally scaling the plan (×k issues + load-bearing) leaves every band unchanged | S1 INV-4 / `pillarLevelsInRange` | unit |
| GT-14 | Projections cannot write | Roll-up & grounding-map handlers have **no write path** to plan/finding/attestation/History; every row deep-links into the read | S6 INV-2 / `ownerDashboardPresent` | negative (pinned) |
| GT-15 | Readiness never surfaced | No read/band/entitlement path consumes the PMF metric; no FE surface renders it | S8 L6, H4 | negative (pinned) |
| GT-16 | D153 on every package | No export/memo render path omits the advisory disclaimer; PDF cover dated to the analysis | S7 §5.4, LD-9 / `exportFlowReal`, `reportCurrencyDated` | integration |
| GT-17 | External-reviewer 403 (dup-anchor) | A stale/re-routed scoped link 403s; scope is single-question-bound | DL-L8 / S6 L1, spec §8 | negative |
| GT-18 | Unlock latched | After `confirmCount` first hits 2, a withdraw below 2 leaves `freezeOn()===false`; `everUnlocked` monotonic | S3 D7, I2 / `unlockLatched`, `freezeFormulaIntact` | integration |
| GT-19 | Integrity = weakest gate + tie-break | `level === min(decomposition)`; ties resolve Viability→Grounding→Adaptability | S1 INV-5,6 / `integrityIsWeakestGate` | unit |
| GT-20 | Maturity not forecast | No 0–100 number/dial/probability on any integrity surface; endpoints Fragile→Sound; pending marker present | S1 INV-3 / `bandsAreWordsNotNumbers`, `forecastFramingPresent` | lint |
| GT-21 | Neutral copy on disclosure | No tier name/price on any held/secondary/disclosure surface; only the gate names Basic | S5 HI-7, LD-5.7 / `deferredDisclosure` | lint |
| GT-22 | Deferred disclosure holds | While `!_ocDisclosed && held>0`, `_visibleSecondaries().length===0` and the lead shows no "+N more"; nudge never fires in freeze | S5 HI-1,3 / `deferredDisclosure` | negative |
| GT-23 | Fast-Pass emits 3 pillars | First-read Fast-Pass output has non-null V/G/A + outcomes + confirm-ready primary; any null pillar fails | S3 I6, D5 / `intakeMultiOutcome` | unit |
| GT-24 | One integrity step per batch | N acts in one window → exactly one `ReanalysisPass` and one integrity step | S3 I8 | integration |
| GT-25 | Withdraw appends never erases | `withdrawItem`/`withdrawRoute`/`groundMitigated` each append a reversal record; prior `HISTORY`/`Attestation` records persist | S2 INV-5, S6 INV-8 / L8 | integration |
| GT-26 | Basis required & typed | Every confirm/answer writes `basis ∈ BASIS`; a reviewer answer sets `answered` (never `null`); a flag writes a first-class attestation | S2 INV-2,7 / `confirmFlagSymmetry` | unit |
| GT-27 | Fix ≠ Grounding | A `fixed` item's figure stays inferred; Grounding rises only via `groundMitigated` + a basis | S2 INV-8, L5 | unit |
| GT-28 | Export not maturity-gated | At `mn=0` (Fragile) export still completes and shows the min-of-three "firms as you confirm more" signal; no path blocks on `mn` | S7 §5.3, LD-7 / `exportFlowReal` | negative |
| GT-29 | Intent is the only History side-channel | Feedback + survey produce zero `HISTORY` entries; `_recordIntent` is the single, deliberate exemption | S8 L9, AC-10 | negative (pinned) |
| GT-30 | Every intent branch emits | 4 wall branches → 4 `intent_signal` rows with distinct `chosen_path` (computable denominator) | S4 INV-5 / `intentCaptureSurfaces` | integration |
| GT-31 | Reports produce no assessment | A generated report render performs no write and moves no band; a sent memo is immutable + stale-flagged | S7 §5.1,5.7 / `reportsTabsGenerated` | negative (pinned) |
| GT-32 | Sticky survey A/B | The timing variant is assigned once per user, immutable for life, stamped on every survey event | S8 L8, AC-8 | integration |
| GT-33 | Mitigated never reads as closed | A `fixed` (mitigated-ungrounded) item is **excluded from the Resolved tray** and renders in "Acted on · not yet closed" with a Grounding pill + `groundMitigated`; the tray's settled-count excludes it; only `groundMitigated`→reanalysis moves it toward closure. Symmetric twin of GT-10's needs-a-fix fork | S2 INV-9, AC-11 / `mitigatedNeedsGrounding` | negative (pinned) |

**DL-209 load-bearing / issue-classification guards** (net-new — Slice 10, `../slices/10-load-bearing-sensitivity-engine.md`; ratified 2026-08-09). Server twins of the five prototype firewall guards + the engine-level sensitivity invariants. GT-34…GT-38 have a live `_S10` twin today; GT-39…GT-44 are engine invariants (`pending()` until the L1/L2 sensitivity engine is built, then gating).

| Test ID | Doctrine | Assertion | Source | Type |
|---|---|---|---|---|
| GT-34 | Resolution derived, not authored | Every issue's primary act is derived from finding-type + `basisInference`; no per-item `primaryMove` field exists on any issue | DL-209 A3 / S10 INV-7 / `resolutionDerivedFromModel` | negative (pinned) |
| GT-35 | Only verify moves Grounding | No `build`/`decide` act raises the Grounding pillar; only a `verify` (confirm **or refute**) does; a fix sets `addressed`/`fixed`, never `you` | DL-209 A4 / S10 INV-1 / `onlyVerifyMovesGrounding` | integration (pinned) |
| GT-36 | Load-bearing inference verifies | Every load-bearing inference-backed issue leads with a verify CTA (evidence never demoted below a fix) — the catering-card defect | DL-209 A4 / S10 INV-8 / `loadBearingInferenceVerify` | structural |
| GT-37 | Finding fully classified | Every issue carries a finding-type + basis; none is unclassified at render | DL-209 A3 / S10 INV-8 / `findingModelComplete` | structural |
| GT-38 | Escalate-on-new | An **unmapped** finding-type returns `escalate` and surfaces to the owner — it never silently default-classifies (Anti-Assumption in code); a synthetic unclassified finding escalates, a classified one resolves normally | DL-209 A2 / S10 INV-8 / `findingTypeExhaustiveOrEscalates` | negative (pinned) |
| GT-39 | Sensitivity is deterministic | Identical dependency graph ⇒ identical sensitivity score for every node (no run-to-run variance below L0) | DL-209 B / S10 INV-2 | unit |
| GT-40 | Sensitivity is decomposable | Every sensitivity score carries a trace to its counterfactual spans + leverage paths; no opaque score | DL-209 D / S10 INV-3 | unit |
| GT-41 | False confidence caught by span | A strong-reading inference-backed artifact qualifies as load-bearing via its two-sided (downside) span, not a severity feel; the one-sided/"moves the band" forms are rejected | DL-209 A2 / S10 INV-2 | unit |
| GT-42 | Zero-data segment = global | At zero labels for a segment, `effectiveThreshold === LB_THRESHOLD` (dormant segmentation is unbiased; no hand-tuned segments) | DL-209 C,D / S10 INV-4 | unit (pinned) |
| GT-43 | Critical floor never suppressed | No `LB_SURFACE_PREF` or segment/domain value can drop a `LB_CRITICAL_FLOOR` item below the surfacing line | DL-209 D / S10 INV-5 | negative (pinned) |
| GT-44 | Calibration never lowers honesty | L4 / segment / preference calibration changes surfacing only; the read's accuracy bar is invariant across segments and tiers (DR-7/DL-103) | DL-209 D / S10 INV-6 | negative (pinned) |

**DL-210 CAF-boundary / alignment / escalation guards** (net-new — Slice 10 §3b; ratified 2026-08-09). Engine-level; `pending()` until the L1 sensitivity/alignment engine is built, then gating.

| Test ID | Doctrine | Assertion | Source | Type |
|---|---|---|---|---|
| GT-45 | Endpoints complete | Every structural target (`definition/edge/achievability/truth/coverage`) declares its (X⁺, X⁻) perturbation endpoints; an unmapped target escalates rather than running without endpoints | DL-210 B / S10 §3b | structural |
| GT-46 | Dim from structural target | An issue's `dim`/`dims[]` is derived from the finding's structural target — never hand-set, never mapped from finding-type (CAF Position #11 preserved) | DL-210 A3 / S10 §3b | structural (pinned) |
| GT-47 | Alignment is relational-traced | An Alignment finding is edge-keyed and its sensitivity references the top-down outcome→roots reachability; a node-local alignment score fails | DL-210 A2 / S10 §3b | structural (pinned) |
| GT-48 | Escalation routes correctly | A runtime (plan-ambiguity) escalation generates a user Clarity/Alignment issue that runs the load-bearing gate; a model-gap (taxonomy) escalation routes to governance and never default-classifies | DL-210 C / S10 §3b | integration |
| GT-49 | Model-gap ceiling = incomplete | A load-bearing model gap marks its region *incomplete* and blocks a Sound claim; it is never scored Fragile or given a numeric penalty | DL-210 D / S10 §3b | negative (pinned) |
| GT-50 | Unknown never scored weak | No unassessed region contributes a band/numeric penalty anywhere; unknown ≠ bad | DL-210 D / S10 §3b | negative (pinned) |

**DL-211 proposal-resolution / cross-surface-sync guards** (net-new — Slice 2; ratified 2026-08-09). These have live `_S10` oracles today.

| Test ID | Doctrine | Assertion | Source | Type |
|---|---|---|---|---|
| GT-51 | Build proposal resolves its finding | Accepting a build proposal (one that adds a missing structural element) closes its finding via reanalysis when all its resolvers are accepted; a finding needing multiple resolvers stays open on partial acceptance (keynote-backup needs requirement + task) | DL-211 A/C / `buildProposalResolvesFinding` | integration |
| GT-52 | Inference/optional stays additive | Accepting an inference or optional proposal (accepting OSLO's guess) grounds nothing and moves no band — only *verify* grounds (GT-35 preserved) | DL-211 A / `inferenceProposalStaysAdditive` | negative (pinned) |
| GT-53 | Resolution synced across surfaces | A finding resolves from the card, the artifact, or the folded read row through the one shared resolver state + reanalysis path; resolved once, never redone | DL-211 B / `resolutionSyncedAcrossSurfaces` | integration |
| GT-54 | Findings itemized, never merged | Multiple findings render as separate, independently-resolvable rows — one row per proposal — never collapsed into a single prose row | DL-211 D / `findingsItemizedNotMerged` | negative (pinned) |
| GT-55 | Card itemizes its proposals | The issue **card** renders one accept/reject row per proposal (each labeled build-fix or optional) — the merged "Review the N proposals in <doc>" prose link is gone | DL-211 D / `cardProposalsItemized` | negative (pinned) |
| GT-56 | Start-here guides every cleared-worklist state | When the worklist is cleared, the "★ Start here" guidance still renders and points to the next real move (finish acted-on-not-closed items · review what's pending) — it is **not** blanked by items being out for review (`showStart` is not gated on `_pendingCount()===0`) | next-move honesty / `startHereGuidesClearedWorklist` | negative (pinned) |
| GT-57 | Every declared capability is simulated (reverse coverage) | Every backend capability in range `1..SIM_MAX_CAP` is referenced by at least one `SIM:#N` tag (or declared arc-only in `_SIM_ELSEWHERE`) — a capability registered but with no simulation pointing at it fails. Complements `demoSimsTagged` (forward: no placeholder/out-of-range tag); this is the reverse blind-spot that let capability #24 drift | build-integrity / prototype-simulation⇒backend-obligation / `capabilityHasSim` | negative (pinned) |

**Async / latency guards** (net-new — extend the honesty spine into the latency dimension; source `LATENCY_AND_ASYNC_UX.md`). These have no `_S10` twin yet because the prototype simulates zero latency; they are **`pending()` until the async/latency UX is built** (§5), then flip to gating.

| Test ID | Doctrine | Assertion | Source | Type |
|---|---|---|---|---|
| GT-A1 | Working ≠ done | No **server-authoritative** surface (checkout, export render, share-create, feedback-file, reviewer-send) shows a success/done state before the server confirms; a pending/in-flight state holds until confirmation — the latency twin of *recorded ≠ resolved* | LATENCY §3 / S3 honesty | negative (pinned) |
| GT-A2 | LLM surfaces show thinking | Chat, briefing drafting, and fix/option drafting render a thinking → streaming indicator before content and lock input while generating; none returns instant, fully-formed text with no pending affordance (Async class C) | LATENCY §2 | integration |
| GT-A3 | Every round-trip has a failure path | Every surface with a backend round-trip (Async class D) exposes an error/timeout + retry state; asserted by injecting a timeout into each round-trip — no silent hang, no frozen control | LATENCY §3 | negative |

**Note — mapping the 59 `_S10` client guards to server twins (L4).** The `_S10` guards fall into three enforcement classes, and each maps to a build-assertion type:
- **Computation guards** (`integrityIsWeakestGate`, `pillarLevelsInRange`, `groundingCountMatchesState`, `bandsAreWordsNotNumbers`, `itemStatesValid`, `metricsFoldedIntoIntent`, `viaCardsEvidenceSafe`) → **server unit tests** on the real pillar/issue engine (GT-07,13,19,20).
- **Flow / lifecycle guards** (`needsFixFork`, `unlockLatched`, `freezeFormulaIntact`, `reanalysisCauseLegible`, `readMovedBannerDurable`, `settleMotionSynced`, `refineReflagsDownstream`, `surveyTriggerFiresOncePostActivation`) → **integration tests** across act→enqueue→reanalysis→resolve (GT-09,10,18,22,24,32).
- **Doctrine-boundary guards** (`commitmentGatePresent`, `archiveIsARealFreePath`, `declareOutcomeFree`, `sharePanelSimplified`, `feedbackCapturePresent`, `defectTicketFormat`, `exportFlowReal`, `reportsTabsGenerated`, `reportSchedulingGate`, `reportReaderMemo`, `deferredDisclosure`, `intakeMultiOutcome`, `issueLayerUnified`, `rootOutcomeGrounding`, `intentTypedAndPrimary`, `confirmFlagSymmetry`) → **negative/pinned + lint** on the real access-control and copy layers (GT-01,02,04,06,08,14,15,21,29,31). The client guard proves *shape*; the server twin proves *behavior*. Guards that are purely presentational regression catches (`iconSystemPaints`, `mastheadCompactable`, `searchPalette`, `accountMenuWired`, `productTourWired`, `historyTrendFilters`, `resourcesTyped`, `growthInvitePresent`, `retentionHookPresent`, `resolvedDetailPresent`, `execFacetsPresent`, `needsTriagePresent`, `ownRunRolePresent`, `coachingFadesWhenEngaged`, `chatQuietTabDuringFreeze`, `freezeScopedToRead`, `integrityRewardFlashWired`, `pillarRewardFlashWired`, `statementUndoRedo`) stay as **client smoke assertions**, retained verbatim as the FE regression tier. The **async/latency guards (GT-A1…A3)** are a fourth tier that has no `_S10` twin yet — added when the latency UX is built.

---

## 4. Test infrastructure notes

- **Suite topology.** Three tiers, all gating: (1) **server unit** — pure pillar/issue/entitlement computation, no I/O; (2) **integration** — the act→`addressed`→`_completeReanalysis`→resolve loop, the checkout→grant flow, the route→reviewer-reply→batch flow, exercised against a real reanalysis engine with a fixture plan; (3) **negative/pinned + lint** — the doctrine boundaries. A fourth **async/latency** tier (GT-A1…A3) joins once the loading/streaming/error UX exists. A **red result in any active tier fails CI and blocks merge** (L3).
- **Porting the `_S10` self-checks.** Each `_s10ck(fn)` returns `true`/`false` today; the port keeps the *predicate* and swaps the *subject*: a `.toString().indexOf(...)` shape-check becomes a call against the real function/endpoint, and a DOM query becomes a data assertion. The 59 names are preserved as test names so the client guard and its server twin are greppably paired.
- **Pinned negatives (must stay red if violated).** Two families are non-negotiable and never allowed to silently pass by removal: **no-write projections** — a mock write-capable principal is handed to roll-up/grounding-map/generated-report/feedback handlers and the test asserts the call is *rejected* (GT-14,31,06); **never-metered exemptions** — the record/reviewer/Viewer paths are exercised at `free` and the test asserts **zero** `gate_hit`/entitlement evaluation (GT-02). A third pinned negative joins from the latency tier — **working ≠ done** (GT-A1): a server-authoritative surface is driven to a pre-confirmation state and the test asserts it does *not* read as complete. These are written as "the wrong default fails."
- **No-write-projection & never-metered are the canary pair.** Both encode "a dev builds this wrong by default" (DL-L2/L6) and both are asserted by *attempting the forbidden action and requiring failure*, not by observing absence. GT-A1 follows the same shape for latency: *fake a success early and require the UI to still read as pending.*
- **Lint tier.** A rendered-string scan enforces (a) **no numeric integrity score** — no 0–100 / dial / probability token on any integrity surface (GT-20); (b) **neutral copy** — no tier name/price string on held/secondary/disclosure surfaces (GT-21). Lint runs over the actual server-rendered read HTML, not source comments.
- **Placeholders quarantined.** Owner-open values (§5) are `pending()` tests: present, named, and neither green nor red until the number/matrix/tracker is ratified — so the gate never silently green-lights an unratified decision.

---

## 5. Open items / placeholders (carried from Slices 3/6/8 — cannot yet be asserted)

- **[async UX] GT-A1…A3** — the loading/streaming/error states of `LATENCY_AND_ASYNC_UX.md` are not in the prototype (it simulates zero latency). The async guards are `pending()` until that UX is built; the Async column in §2 declares the *intended* treatment now so nothing ships without one (L10).
- **[S3 R2-RE-1] Reanalysis window numbers** — debounce/cooldown/max-age are stubs (proto 1500/900/5000/16000 ms illustrative). The suite asserts *batching behavior* (one pass per window) but pins no literal; a timing test lands only when the numbers are ratified.
- **[S3 R2-RE-2] Fast-vs-Deep on the grounding-act batch** — tier choice open; the 3-pillar-emit assertion holds regardless.
- **[S6 R2G4] Owner vs delegate-PM role/access matrix** — display-only this release (DL-L8); only the *external* scope is asserted (GT-08). The enforced delegate matrix is deferred → `pending()`.
- **[S8 tracker] Which defect tracker (Linear/Jira/internal)** — field-map/auth/retry/back-sync unbound; GT-05 asserts the *sanitization boundary*, not the destination.
- **[S8 readiness stats] Cohort / rolling window / min-N for the ~40% PMF bar** — the bar is ratified, the statistics are not; GT-15 asserts *non-surfacing*, not the computation.
- **[S5 OI-2/OI-3] Rationale-generation contract + secondary-detection confidence floor** — `_OC_IMPACT_NOTE` must cite real signal (asserted), but the model prompt/schema and precision bar are owner-open.
- **[S2 owner] `answered` basis strength + reviewer-reject flag authority** — enum ordering deferred; GT-26 asserts *typed & non-null*, not rank.

---

## 6. Acceptance criteria

1. **AC-1 — Zero unbound surfaces.** The Integration Map enumerates every dynamic surface in the shipped read; each has a non-empty Reads column, a Changed-by that is `reanalysis.landed`, a named side-channel event, or `—`, and a non-empty Async code. An orphan surface fails the gate. (L2, L10, §2)
2. **AC-2 — Every DL-L landmine has ≥1 negative/assertion test.** DL-L1…L9 each map to at least one register row (GT-01…GT-09), and each fails loudly if the wrong-default implementation is built. (L5, §3)
3. **AC-3 — The spine invariant holds globally.** No `you`/`fixed`/band/integrity transition exists outside `_completeReanalysis`; asserted per-slice and once globally (GT-10). (L6)
4. **AC-4 — Never-metered is a pinned negative.** Reading a record, routing to a reviewer, and adding a Viewer at `free` produce **zero** `gate_hit`/entitlement evaluation; the test fails if any is metered (GT-02). (L7)
5. **AC-5 — No-write projections are pinned negatives.** Roll-up, grounding-map, generated reports, and feedback/survey are handed a write-capable principal and the write is rejected (GT-14,31,06). (L7)
6. **AC-6 — Freeze & readiness are presentation/internal only.** The read API returns the full read regardless of `confirmCount` (GT-04); the PMF readiness metric is never rendered and never consumed by a read/band/entitlement path (GT-15).
7. **AC-7 — Neutral copy & no numeric score pass lint.** No 0–100 integrity number on any integrity surface (GT-20); no tier name/price on any disclosure/held/secondary surface (GT-21).
8. **AC-8 — D153 on every package + reviewer 403 enforced.** No export/memo path omits the advisory disclaimer (GT-16); a scoped reviewer token 403s on anything but its one question (GT-08).
9. **AC-9 — All 59 `_S10` guards are ported.** Every client guard has a named server twin or a retained client smoke assertion; none is dropped. (L1, L4, §3 note)
10. **AC-10 — The suite is the build gate.** A red result in any active tier blocks merge; placeholders are quarantined `pending()` tests that neither pass nor fail until ratified. (L3, L9, §5)
11. **AC-11 — Every surface declares an async state.** The Integration Map's Async column is populated for every row; when the latency UX is built, server-authoritative surfaces never show success before confirmation (GT-A1), LLM surfaces show a thinking/streaming state (GT-A2), and every round-trip has a failure path (GT-A3). (L10, §2, §3)

---

*Slice 9 of the R2 delta — the keystone. It ships no new capability: it makes FE and BE agree unambiguously (§2, now including each surface's async state) and makes doctrine executable (§3). On sign-off, the 59 `_S10` guards, the DL-L1…L9 landmines, every Slice 1–8 honesty invariant, and the async/latency guards (GT-A1…A3, pending the latency UX) become a single red-or-green acceptance suite that gates the R2 build.*

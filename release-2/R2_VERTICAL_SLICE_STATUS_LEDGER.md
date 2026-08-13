# R2 Vertical Slice Status Ledger

**Purpose:** authoritative operational resumption ledger for the implementation status of the ten signed-off R2 delta slices.

**Status snapshot:** 2026-08-13

**Audited branch:** `codex/release-2-build`

**Audited implementation commit:** the conventional commit accompanying this ledger update

**Working tree at audit:** Slice 4 is implemented and automated-verification green. Completion remains withheld because the repository's contract-traceability gate has no approved entitlement/monetization contract identifier, live Stripe test configuration was unavailable, and the final Outcome-dialog browser rerun was interrupted by local disk exhaustion followed by the in-app browser URL policy. Slices 5–10 were not changed.

**Current owner-authorized work scope:** **Slices 1–4**

**Owner-blocked scope:** **Slices 5–10 until the owner explicitly reopens them**

**Scope authority:** slice requirements remain in `slices/01…10`; this ledger records delivery evidence and does not supersede doctrine, decisions, slice specifications, or `SIGNOFF.md`.

> **Resume rule:** every person or agent resuming R2 implementation must read this ledger before selecting work. Update the affected row in the same change that produces new evidence. Do not mark a gate complete from recollection, prototype behavior, inherited R1 functionality, or the existence of a test file.

---

## 1. Current release-level verdict

**R2 implementation state: SLICES 1–3 IN PROGRESS · SLICE 4 IMPLEMENTED / UNVERIFIED · SLICES 5–10 OWNER-BLOCKED.**

- All **10 slice build designs are signed off** (`SIGNOFF.md`).
- The owner explicitly reopened **Slice 4** for implementation on 2026-08-13. No implementation, UI/UX review, manual regression, functional-test activation, or prototype-parity work may begin for **Slices 5–10** until the owner explicitly changes this ledger.
- The R2 reference prototype is healthy: headless verification on 2026-08-11 returned **85 checks, 0 failures, 0 page errors**.
- The Phase 0 guardrail command is healthy: `pnpm test:r2-guardrails` returned **4 infrastructure + 21 active-runner tests passed**.
- The guard registry contains **60 guards**: `GT-01…GT-57` and `GT-A1…GT-A3`.
- **22 guards are active; 38 are pending.** Slice 1 activates `GT-07`, `GT-10`, `GT-11`, `GT-13`, `GT-19`, and `GT-20`; Slice 2 activates `GT-09`, `GT-12`, `GT-25`, `GT-26`, `GT-27`, `GT-33`, and `GT-51…GT-56`; Slice 4 activates `GT-01`, `GT-02`, `GT-03`, and `GT-30`. Slices 5–10 remain owner-blocked.
- Slice 9's FE↔BE contract currently contains **58 mapped dynamic surfaces**.
- All **6/6 Phase-A prototype corrections** checked by the gate are present.
- **Slices 1–3 are reopened by live QA.** The focused rerun passed 78 web tests, 13 API tests, 4 guardrail infrastructure tests, and 17 active guardrail tests, but those automated gates did not catch the live visual and semantic failures recorded below.
- First-time activation/intake and the guided animation work. Returning clients receive the same intake surface without replaying the first-time story and complete the returning analysis path.
- The Issues shell and lifecycle controls work, but expanded issue review reflows the page instead of using the prototype's stable focus layer.
- Real DOCX, PDF, and XLSX sources upload and reanalysis completes, but field-by-field comparison against the Atlas ground truth found missing structure, missed conflicts/gaps, and generic issue output.
- The OSLO advisor UI works, but a source-specific £45,000 evidence question returned the generic highest-priority issue response.
- A final live regression found and fixed accepted-proposal withdrawal: Accept → Resolved → Withdraw now reopens cleanly with an append-only lifecycle attestation.
- The owner explicitly requested that NVDA be stopped. The spoken NVDA session was therefore not restarted; keyboard, focus, ARIA, reduced-motion, and responsive accessibility checks pass and the spoken session is recorded as owner-excluded, not an open delivery blocker.

### Evidence commands

```powershell
cd code
pnpm test:r2-guardrails
```

Expected audited output:

```text
4 passed
21 passed
[R2 guardrails] 60 registered · 22 active · 38 pending · 58 mapped surfaces · 6/6 prototype corrections
```

The prototype was separately opened headlessly with Chromium and evaluated through `_s10SelfCheck()`:

```text
85 checks · 0 failures · 0 page errors
```

---

## 2. Status vocabulary

| Status | Exact meaning |
|---|---|
| **SIGNED OFF** | The owner approved the build design. This is not implementation completion. |
| **READY · NOT STARTED** | Dependencies permit work to begin, but no R2 production implementation evidence exists. |
| **WAITING ON DEPENDENCIES** | The design is signed off, but earlier slices or an owner touchpoint must land before implementation can complete safely. |
| **OWNER-BLOCKED** | The design remains signed off, but work is outside the current owner-authorized scope. Do not implement, review, test, or advance the slice until the owner explicitly reopens it. |
| **IN PROGRESS** | Production implementation has begun, but at least one required delivery gate remains incomplete. |
| **IMPLEMENTED · UNVERIFIED** | Code exists, but required automated, manual, UI/UX, or parity evidence is missing. |
| **VERIFIED** | Slice-specific automated tests and functional tests pass at the recorded commit. |
| **COMPLETE** | Implementation, functional tests, UI/UX review, manual regression, prototype-parity assessment, and required test cases all pass, with evidence recorded here. |
| **NOT RUN** | The activity has not been performed against the executable R2 application. It does not mean pass or fail. |
| **NOT VERIFIED** | No evidence supports a yes/no conclusion. It must never be shortened to “identical” or “complete.” |
| **N/A** | The gate genuinely does not apply; the row must state why. |

### Gate interpretation

- **UI/UX review** means review of the executable R2 application against the signed slice and reference prototype—not review of the standalone prototype itself.
- **Manual regression** means agent  has exercised the slice's happy path, failure path, permissions, async states, responsive behavior, and adjacent flows in a runnable environment.
- **Functional testing** means R2-specific production behavior has been exercised through active automated tests and, where required, a real integration environment.
- **Identical to prototype** means behavior, state transitions, copy, and applicable visual structure have been compared with `oslo-prototype-r2.html`. Server-only behavior explicitly absent from the prototype is judged against the slice specification instead.
- **Test cases** distinguishes cases that are merely designed in Markdown from tests that are active and passing in the real build.

---

## 3. Master vertical-slice ledger

**This table is the current authoritative resumption state.** The detailed table and dated notes that follow are retained as historical evidence and do not override these rows.

| Slice | Current delivery status | UI/UX review | Manual regression | Functional testing | Identical to prototype | Test cases | Next required action / dependency |
|---|---|---|---|---|---|---|---|
| **1 · Outcome-Integrity Engine** | **IN PROGRESS · REOPENED BY LIVE QA.** The shell, queue, workspace notice, and advisor rail run; visual and evidence-grounded behavior is not complete. | **FAIL · MAJOR.** Expanded issue review shifts the work column and grows the page instead of using the stable prototype focus layer. | **PARTIAL.** Navigation, toggles, expanders, focus controls, responsive shell, and analysis states work; live advisor evidence response failed. | **PARTIAL.** Focused automated gates pass, but the real-document advisor scenario fails. | **FAIL.** Issue expansion and the source-specific advisor result do not match the prototype/contract. | **PARTIAL.** Active guards are green; missing live-data and layout-shift cases must be added. | Fix issue-detail focus layout and evidence-qualified advisor response; rerun visual and live-document QA. |
| **2 · Issue Lifecycle & Grounding Acts** | **IN PROGRESS · REOPENED BY LIVE QA.** Confirm, reanalysis, Resolved, Withdraw, proposal Accept/Reject, and advisor controls work. | **FAIL · MAJOR.** Expanded issue is inline/reflowing, not the prototype's stable focus layer. | **PARTIAL PASS.** Lifecycle actions pass; exact UI comparison fails. | **PASS for exercised lifecycle mechanics.** Confirm/Withdraw and proposal decisions completed without error. | **FAIL.** Expanded issue geometry, position, and surrounding-shell behavior differ. | **PARTIAL.** Lifecycle tests pass; zero-layout-shift parity coverage is missing. | Implement stable issue focus presentation and add browser layout-shift regression coverage. |
| **3 · Reanalysis Engine + Freeze/Unlock** | **IN PROGRESS · REOPENED BY LIVE QA.** First-time and returning animation paths, handoff, and reanalysis completion work; real-document fidelity does not. | **PASS for the exercised onboarding/analysis motion.** | **FAIL for live-data acceptance.** Mixed and clean Atlas uploads completed, but extracted artifacts and issues did not match ground truth. | **PARTIAL.** Run mechanics and focused tests pass; semantic extraction/issue mapping fails. | **PARTIAL.** Kinetic flow matches applicable prototype states; resulting evidence read is not acceptance-complete. | **PARTIAL.** Flow tests pass; Atlas field-by-field and planted-conflict assertions must become active tests. | Fix structured extraction and evidence-derived issue coverage, then rerun the Atlas ground-truth suite. |
| **4 · Freemium Entitlement & Commitment Gate** | **IMPLEMENTED · UNVERIFIED.** Capacity-only Free/Basic policy, first-class Outcomes, reversible archive/reactivate, hosted Stripe Checkout and portal contracts, signature-verified webhook grant, durable commitment/intent records, cancellation/grace preservation, and direct-browser-grant refusal are implemented. | **PARTIAL PASS.** The in-app browser verified the second-Plan wall, Free/Basic comparison, $29/$290 interval states, never-metered copy, hosted-billing pending/error state, first analysis, and the Manage Outcomes entry. The final Outcome list/gate rerun was interrupted by local disk exhaustion; after recovery the browser URL policy blocked reloading the local tab. | **PARTIAL PASS.** The real Free plan wall and safe unconfigured-billing failure were exercised. A live Stripe test Checkout and signed webhook were not run because no Stripe test keys, webhook secret, or Price IDs were configured. | **PASS for local and provider-boundary automation.** API 351 passed; web 25 files/158 passed; lint, Ruff, Next production build, TypeScript, migrations, diff, invariants, observability, and 4 infrastructure + 21 active guard tests pass. Contract gate remains red because its approved-ID list contains no entitlement/monetization contract. | **PARTIAL.** Applicable gate copy, choices, prices, capacity semantics, and failure state match the signed Slice 4 design. Provider-hosted pages and the final Outcome browser sequence remain unverified. | **Active/passing:** `GT-01`, `GT-02`, `GT-03`, `GT-30`, plus checkout signature/idempotency, no-direct-grant, Outcome persistence/archive/reactivate, every-branch intent, grace/cancellation, and UI choice tests. | Owner must supply/approve an entitlement contract mapping for Gate 2 and Stripe test configuration; then run hosted Checkout → signed webhook → entitlement grant and repeat the final Outcome browser regression. Do not start Slice 5. |
| **5 · Multi-Outcome Read & Deferred Disclosure** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active production tests for this slice.** | Owner must explicitly reopen Slice 5. |
| **6 · Collaboration, Reviewer Roll-up & Share** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active R2 completion tests for this slice.** | Owner must explicitly reopen Slice 6. |
| **7 · Structured Data Import, Provenance & Validation** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active R2 completion tests for this slice.** | Owner must explicitly reopen Slice 7. |
| **8 · Analysis Observability & Operator Recovery** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active R2 completion tests for this slice.** | Owner must explicitly reopen Slice 8. |
| **9 · R2 Contract Consolidation** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active R2 completion tests for this slice.** | Owner must explicitly reopen Slice 9. |
| **10 · Product Grill Shell & Operational Closure** | **OWNER-BLOCKED.** | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT VERIFIED.** | **0 active R2 completion tests for this slice.** | Owner must explicitly reopen Slice 10. |

**Latest evidence:** `../code/reports/r2-full-flow-rerun-2026-08-13/FINAL_REPORT.md` and `../code/reports/r2-full-flow-rerun-2026-08-13/screenshots/12-expanded-issue-app-vs-prototype.png`. This rerun supersedes the earlier complete verdict in `../code/reports/r2-phases-2-6-qa-2026-08-13/FINAL_REPORT.md`.

### Historical detailed rows (superseded by the current table above)

| Slice | Current delivery status | UI/UX review | Manual regression | Functional testing | Identical to prototype | Test cases | Next required action / dependency |
|---|---|---|---|---|---|---|---|
| **1 · Outcome-Integrity Engine** | **IN PROGRESS · IMPLEMENTED AT `9d44040`.** Three-pillar composition, weakest-gate issues, API projection, exact R2 masthead, workspace-open notice, ranked queue, inline issue read, and governed OSLO rail are implemented. Completion is withheld only for the owner-deferred combined spoken screen-reader audit after Slices 1–3 are otherwise complete. | **PASS for current Slice 1 UI scope.** Physically combined queue and expanded-issue comparisons confirm the prototype masthead, SAMPLE badge, compact integrity read, 266px navigation, centered work column, ranked issue styling, inline expansion, and 330px advisor. No actionable P0/P1/P2 mismatch. Evidence: `../code/design-qa.md` and `../code/reports/r2-slice-1-qa-2026-08-12/`. | **PARTIAL PASS · OWNER-DEFERRED SHARED AT GATE.** Seeded Overview, timeout/last-good/retry, workspace notice, integrity expansion/collapse, issue opening/closing, keyboard focus, Escape/focus restoration, advisor, pillar navigation, desktop/responsive/no-overflow, 200%-zoom-equivalent reflow, and real reduced-motion preference pass. Accessibility-tree roles, landmarks, live region, dialog naming, expanded/control relationships, and focus behavior pass. The owner directed the spoken screen-reader session to run once Slices 1–3 are otherwise complete. | **PASS at `9d44040`.** Web: 23 files/128 passed; focused Overview: 38 passed; Slice 1 API contracts: 19 passed earlier in the same run; R2 guardrails: 4 infrastructure + 9 active selectors passed earlier in the same run; ESLint, TypeScript/Next.js production build, and diff check pass. The manual audit changed no product code. | **PASS for applicable Slice 1 state and structure.** Header, workspace-open notice, queue, advisor rail, inline issue hierarchy, timeout/retry states, and responsive structure match the prototype/slice contract while dynamic live project values remain truthful. OSLO Proposes and Resolved are Slice 2. | **Automated coverage passing:** AC-1…AC-10 through `GT-07`, `GT-10`, `GT-11`, `GT-13`, `GT-19`, `GT-20`, plus masthead, welcome notice, inline non-modal semantics, preserved queue, Affects/Holds up context, and focus behavior assertions. Manual completion evidence: `../code/reports/r2-slice-1-qa-2026-08-12/manual-completion/`. | Keep the spoken screen-reader audit open as the final shared Slices 1–3 gate. Slice 2 is the next executable work. |
| **2 · Issue Lifecycle & Grounding Acts** | **IN PROGRESS · IMPLEMENTED AND BROWSER-VERIFIED.** The durable owner-act loop remains based at `dd69e69`; the 2026-08-13 parity hardening adds prototype motion and final matched-state corrections. Completion is withheld only for the owner-deferred combined spoken screen-reader audit after Slices 1–3 are otherwise complete. | **PASS for current Slice 2 UI scope.** Fresh 1280 × 720 physical comparisons cover the masthead, workspace-open notice, ranked queue, expanded issue hierarchy, itemized OSLO Proposes group, lifecycle trays, and governed/Wider advisor rail. Issue order, auto-position, proposal labels, navigation order, and motion now match the prototype. Live backend values remain truthful. No actionable P0/P1/P2 mismatch remains. Evidence: `../code/reports/r2-slice-2-ui-qa-2026-08-13/REPORT.md`. | **PARTIAL PASS · OWNER-DEFERRED SHARED AT GATE.** A fresh live route created a real scoped review grant and Awaiting Evidence row; the 1 s cool-blue tray flash ran; Withdraw restored the ranked queue without error. Issue disclosure, focus, owner actions, proposal controls, responsive 390 × 844 layout, and no-overflow behavior pass. Spoken output remains deferred by owner direction. | **PASS.** API: 316 passed. Web: 24 files/145 passed. Focused Overview: 46 passed; focused Slice 2 total: 65. Guardrails: 4 infrastructure + 17 active-runner tests; 18/60 active. ESLint, Next.js production build, TypeScript, and responsive browser checks pass. | **PASS for applicable Slice 2 state, structure, and motion.** Prototype values were copied for the 340 ms entrance, 1 s lifecycle flash, 1.25 s row settle, and workspace unlock; reduced-motion disables them. Owner-act controls, lifecycle movement, OSLO Proposes, Resolved/Awaiting/Acted-on trays, and cross-surface decisions retain truthful backend behavior. | **Active coverage passing:** AC-1…AC-11 and DL-211 through `GT-09`, `GT-12`, `GT-25`, `GT-26`, `GT-27`, `GT-33`, `GT-51…GT-56`, plus issue auto-position/clarification disclosure, governed Wider/Narrower advisor, prototype nav order, no proposal-kind badge, proposal-history source-run regression, route/withdraw, reviewer flag, separate fix/ground, comment negative, no-blank-state, and cross-surface assertions. | Run the single combined spoken screen-reader gate for Slices 1–3. Keep Slices 4–10 blocked. |
| **3 · Reanalysis Engine + Freeze/Unlock** | **IN PROGRESS · IMPLEMENTED AND BROWSER-VERIFIED AT `6dfdebe`.** Fast/Deep pass metadata, project-level batching, STALE/reanalyzing/fresh state, explicit reanalysis, retry/last-good preservation, pending Undo, append-only Deep supersession, causal read-moved notification, first-run outcome confirmation, presentation-only freeze, and latched two-act unlock are implemented. The production first-analysis screen uses the actual prototype kinetic engine with real progress/outcome adapters. Completion is withheld only for the owner-deferred shared spoken screen-reader session. | **PASS for browser-executable Slice 3 scope.** Approved-browser comparison covers intake, graph reveal, pillar animation, outcome decision, production Overview, and reanalysis states. The core engine, layout, card geometry, typography, colors, and applicable controls match the signed prototype with no actionable P0/P1/P2 mismatch. Live project values and animation timing remain truthfully dynamic; prototype-only developer controls are intentionally absent. Evidence: `../code/reports/r2-slice-3-qa-2026-08-12/manual-live/`. | **PARTIAL PASS · OWNER-DEFERRED SHARED AT GATE.** The visible sample-plan first read, full kinetic sequence, all three outcome decisions (Confirm, Refine, Keep as inference), saving/handoff states, Overview landing, issue clarification, recommended action, immediate stale/Undo projection, reanalysis completion, queue/evidence refresh, reload persistence, advisor/navigation continuity, and narrow no-overflow layout pass. A late Undo correctly reports that analysis already acquired the change. Failure/retry, Deep supersession, read-moved, reduced-motion, and recovery paths remain passing automated coverage; synthesized spoken output is deferred. Control evidence: `../code/reports/r2-slice-3-button-qa-2026-08-12/`. | **PASS at `6dfdebe`.** Full API: 303 passed. Full web: 24 files/138 passed. Focused Slice 3 parity/flow: 2 files/10 passed. R2 guardrails: 4 infrastructure + 9 active-runner tests passed. ESLint, TypeScript/Next production build, and diff check pass. | **PASS for applicable Slice 3 states.** The prototype engine is preserved mechanically and the approved-browser graph/decision comparisons show the same kinetic language and decision UI. Dynamic content and event timing are intentionally real, so parity is state-based rather than claiming identical pixels at every animation millisecond. | **Active coverage passing:** batching/merge, Fast budget, Deep supersession, retry-once, STALE projection, explicit run, outcome actions, pending Undo, first-run count/latch, read-moved, exact kinetic source parity, all narration/decision states, live sync, confirm/refine/defer, save recovery, origin rejection, responsive/reduced-motion adapters, and immediate Overview stale/Undo projection. Shared spoken screen-reader output remains owner-deferred. | Begin Slice 2. After Slice 2 is otherwise complete, run the single combined spoken screen-reader gate for Slices 1–3. Keep Slices 4–10 blocked. |
| **4 · Freemium Entitlement & Commitment Gate** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. Existing subscription/tiering code is not evidence of the R2 Outcome-unit or capacity-only commitment gate. | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** No active R2 entitlement, real-checkout, never-metered, archive, or intent tests. | **BLOCKED · NOT VERIFIED.** | **Designed:** AC-1…AC-10; principal guards `GT-01`, `GT-02`, `GT-03`, `GT-30`. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 4. Its dependency on Slice 5 and owner choice O-6 remain recorded for later. |
| **5 · Multi-Outcome Read & Deferred Disclosure** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. No R2 Fast-Pass multi-outcome extraction, held pool, or disclosure implementation evidence. | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** Deferred-disclosure and neutral-copy guards remain pending. | **BLOCKED · NOT VERIFIED.** | **Designed:** AC-1…AC-10; principal guards `GT-21`, `GT-22`, with Fast-Pass output shared through `GT-23`. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 5 after the Slices 1–3 window. O-7 remains recorded for later. |
| **6 · Collaboration, Reviewer Roll-up & Share** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. R1 sharing/comment/notification functionality remains an unverified reuse candidate. | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** No R2 reviewer-scope 403, no-write projection, immutable withdrawal, or unmetered-access test is active. | **BLOCKED · NOT VERIFIED.** | **Designed:** AC-1…AC-10; principal guards `GT-02`, `GT-08`, `GT-12`, `GT-14`, `GT-17`, `GT-25`. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 6. Dependencies on Slices 1/2 and O-8 remain recorded for later. |
| **7 · Reports, Export & Hand-off** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. Existing R1 reports/export surfaces remain unverified against R2. | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** No active R2 tests for projection-only reports, D153, pending reanalysis, low-maturity export, immutable memo, or scheduling. | **BLOCKED · NOT VERIFIED.** | **Designed:** AC-1…AC-10; principal guards `GT-16`, `GT-28`, `GT-31`, plus applicable `GT-A1`/`GT-A3`. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 7. Dependencies on Slices 1–3 and O-9 remain recorded for later. |
| **8 · Feedback, Survey & Funnel Telemetry** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. Existing R1 telemetry remains an unverified reuse candidate. | **BLOCKED · NOT REVIEWED.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** No active R2 isolation, sanitization, activation, readiness, sticky-A/B, or History-boundary test. | **BLOCKED · NOT VERIFIED.** | **Designed:** AC-1…AC-10; principal guards `GT-05`, `GT-06`, `GT-09`, `GT-15`, `GT-29`, `GT-32`, plus applicable async guards. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 8. Dependencies on Slices 2/3 and O-10 remain recorded for later. |
| **9 · Doctrine Guardrails + FE↔BE Integration Map** | **SIGNED OFF · OWNER-BLOCKED AFTER PHASE 0.** Existing Phase 0 contract parser, registry, CI command, and tests remain valid and green; no further Slice 9 advancement is authorized. | **BLOCKED after contract review.** App-wide UI/UX review has not run. | **BLOCKED · NOT RUN for the executable R2 application.** | **EXISTING PHASE 0 PASS; FURTHER WORK BLOCKED.** Infrastructure: 4 tests passed. Business guards: 0 active / 60 pending. | **BLOCKED · NOT VERIFIED for the executable app.** Prototype remains green at 85/85. | **Designed:** AC-1…AC-11; registry `GT-01…GT-57` + `GT-A1…A3`. **Infrastructure tests passing: 4. Active production guard tests: 0.** | Preserve the existing Phase 0 gate only. **Do not activate or expand Slice 9 work** until the owner explicitly reopens it. |
| **10 · Load-Bearing Sensitivity + Issue Classification** | **SIGNED OFF · OWNER-BLOCKED.** Outside the current Slices 1–3 work window. Prototype L3 behavior exists, but no production engine implementation is accepted as R2 evidence. | **BLOCKED · PARTIAL REFERENCE ONLY.** | **BLOCKED · NOT RUN.** | **BLOCKED · NOT RUN.** `GT-34…GT-50` remain registered and pending. | **BLOCKED · NOT VERIFIED.** | **Designed:** 17 acceptance guards, `GT-34…GT-50`. **Active/passing production tests: 0.** | **Do not start.** Owner must explicitly reopen Slice 10 after Slices 1–3. Its dependencies and calibration procedure remain recorded for later. |

---

## 4. Build order and resumable next work

| Order | Work | Current gate |
|---:|---|---|
| 0 | Slice 9 Phase 0 contract and guard skeleton | **Already established and green; now owner-blocked from further advancement.** |
| 1 | Slices 1 + 3 | **IMPLEMENTED AND BROWSER-VERIFIED.** The shared spoken screen-reader audit remains deferred until Slice 2 is otherwise complete. |
| 2 | Slice 2 | **IMPLEMENTED AND BROWSER-VERIFIED AT `dd69e69`.** Only the owner-deferred combined spoken screen-reader gate remains. |
| 3 | Slice 4 | **IN PROGRESS · OWNER REOPENED.** Execute one public-behavior RED→GREEN cycle at a time. |
| 4 | Slices 5–10 | **OWNER-BLOCKED.** Do not start implementation, review, testing, or parity work until the owner explicitly reopens these slices. |

**Immediate next work:** close Slice 4's external verification gates without advancing Slices 5–10: approved contract mapping, configured Stripe test-mode Checkout/webhook, and a fresh in-app-browser Outcome archive/reactivate/capacity run. The previously recorded Slices 1–3 follow-ups remain separate work.

---

## 5. Ledger update protocol

For every implementation or verification change:

1. Update **Status snapshot**, **Audited branch**, **Audited commit**, and working-tree state.
2. Update only the affected slice rows; preserve prior uncertainty as a note if the new evidence is narrower than the row.
3. Record the exact automated command and result. A test-file path without a fresh result is not evidence.
4. Link or name the UI/UX review artifact, manual-regression record, screenshots, and parity comparison when those gates run.
5. Change a guard from `pending` to `active` only when it names a real test selector that proves the production behavior.
6. Never use an R1 test or inherited R1 feature as proof of R2 completion until it is traced to the R2 acceptance criterion and rerun under the R2 contract.
7. Never mark **Identical to prototype = Yes** from visual similarity alone. Check behavior, copy, state transitions, permissions, async/failure states, and responsive treatment.
8. If a slice requirement conflicts with doctrine, a ratified decision, or another slice, stop and escalate under Framework 001; do not resolve it in this ledger.
9. A slice may be marked **COMPLETE** only when all five requested gates—UI/UX review, manual regression, functional testing, prototype parity, and test cases—are evidenced as passing or explicitly owner-waived.
10. **Owner scope lock:** Slices 5–10 are blocked. Only an explicit owner instruction may change them from `OWNER-BLOCKED` to an active status.

### Required completion evidence per slice

```text
Implementation commit/PR:
Automated commands and results:
Active GT selectors:
UI/UX review artifact:
Manual regression artifact/environment:
Prototype parity artifact:
Known exceptions or owner waivers:
Reviewer / date:
```

---

## 6. Evidence index

- Build design and ten-slice status: `SIGNOFF.md`
- Build order and dependencies: `BUILD_SEQUENCE.md`, `WORK_BREAKDOWN.md`
- Requirements and acceptance criteria: `slices/01…10`
- FE↔BE contract and GT definitions: `slices/09-doctrine-guardrails-integration-map.md`
- Current prototype state: `R2_REFINEMENT_LEDGER.md`, `PROTOTYPE_REFERENCE.md`, `oslo-prototype-r2.html`
- Guard registry: `../code/ci/r2_guardrails.json`
- Guard gate: `../code/ci/gate_r2_guardrails.py`
- Gate infrastructure tests: `../code/tests/positive/ci/test_gate_r2_guardrails.py`, `../code/tests/negative/ci/test_gate_r2_guardrails.py`
- R2 import commit: `09befa5`
- Phase 0 gate commit: `9efa6ae`
- Slice 1 implementation commit: `8b8f702`
- Slice 1 masthead/parity follow-up: `2958c4a`
- Slice 1 verification-evidence ledger commit: `2388702`
- Slice 1 current browser-blocker evidence commit: `d609ff5`
- Slice 1 latest browser-blocker evidence commit: `98c1a13`
- Slice 1 R2 prototype-shell alignment: `fce7cc0`
- Slice 1 exact-prototype parity implementation: `e25f3ad`
- Slice 1 bounded-shell correction and exact-size evidence: `5489ca6`
- Slice 1 queue and inline-issue prototype-parity correction: `9d44040`
- Slice 1 durable evidence: `../code/reports/r2/slice-01/`

---

## 7. Active Slice 1 run plan — 2026-08-12

1. Review the preserved Slice-1-only UI, E2E, report, and screenshot candidates against AC-1…AC-10 and the six active GT guards; keep only behavior supported by canon and fresh evidence.
2. Complete the remaining manual timeout → stale/last-good → retry journey in the real application, plus full keyboard traversal, reduced-motion, 200% zoom, responsive, permissions, and adjacent-regression checks in the in-app browser.
3. Capture and inspect current-run desktop, tablet, and mobile implementation and matching-state prototype screenshots; fix any Slice-1 parity discrepancy and repeat the comparison.
4. Rerun the Slice-1 automated, guardrail, lint, build, migration, and scoped end-to-end gates; perform security/privacy/authorization/tenant-boundary/error-path Code Review.
5. Update durable evidence and this ledger. Mark Slice 1 COMPLETE only if every required gate passes, commit the verified implementation, then commit the final ledger evidence separately.

**Run result:** candidate review, automated parity capture, all scoped functional/guardrail/lint/build/migration gates, and Code Review passed. Manual timeout/recovery and accessibility gates remain blocked because the required in-app browser failed to attach a page on three fresh attempts. Slice 1 remains `IN PROGRESS`; no later slice was acquired.

---

## 8. Active Slice 1 resumption plan — 2026-08-12

1. Reconnect the required Codex in-app browser to the real local application without substituting another browser surface.
2. Exercise the forced timeout → stale/last-good → retry journey and verify the last successful read is preserved throughout recovery.
3. Complete manual keyboard traversal, dialog announcements/focus behavior, reduced-motion observation, 200% zoom, and desktop/tablet/mobile checks against the Slice 1 specification and prototype.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates if the manual gates pass; review security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and the ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** the required in-app browser connected, but two fresh-page requests timed out before a webview attached. The documented recovery procedure retained the existing browser binding, confirmed empty controlled/user-visible tab lists, requested a fresh tab, and attempted visibility; visibility remained false and the second page also failed to attach. Local Supabase, FastAPI, and Next.js services were healthy. No substitute browser was used, no valid manual evidence was produced, and no product code changed. Slice 1 remains `IN PROGRESS`; no later slice was acquired.

---

## 9. Active Slice 1 resumption plan — 2026-08-12 02:00 PKT

1. Reconnect the required in-app browser to the seeded local application and retain the browser binding through supported recovery.
2. If a page attaches, exercise timeout → stale/last-good → retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, and responsive checks.
3. Capture and inspect current-run screenshots before accepting UI/UX or prototype-parity evidence.
4. Rerun the scoped automated gates only if manual verification passes or product code changes.
5. Record the exact result and keep Slice 1 `IN PROGRESS` unless every open gate passes.

**Run result:** the required in-app browser connected, but two fresh-page requests timed out before a webview attached. Supported recovery retained the browser binding, confirmed empty controlled/user-visible tab lists, requested visibility and one fresh page; visibility remained false, the second page failed to attach, and both tab lists remained empty. Local Supabase, the seeded owner account, FastAPI, and Next.js were healthy. No substitute browser was used, no current-run screenshot or interaction was accepted, no automated suites were rerun because no code changed, and no product code changed. Durable manual/UI evidence is committed at `397c07e`. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4–10 remain untouched.

---

## 10. Active Slice 1 resumption plan - 2026-08-12 03:00 PKT

1. Reconnect the required in-app browser to the real local application and retain the browser binding through supported recovery.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, and responsive checks.
3. Capture and inspect current-run screenshots before accepting UI/UX or prototype-parity evidence.
4. Rerun the scoped automated gates only if manual verification passes or product code changes.
5. Record the exact result and keep Slice 1 `IN PROGRESS` unless every open gate passes.

**Run result:** the required in-app browser connected, but two fresh-page requests timed out before a webview attached. Supported recovery retained the browser binding, confirmed empty controlled/user-visible tab lists, exposed visibility, and requested one fresh page; the second request also failed before attachment. FastAPI returned `200` and Next.js returned `307`. Local Supabase could not be reseeded because Docker Desktop's service was unavailable to the scheduler account and `127.0.0.1:54321` remained closed; this would block the seeded journey after page attachment, but the browser failed first. No substitute browser, current-run screenshot, interaction, automated rerun, or product change was accepted. Durable manual/UI evidence is committed at `c19083a`. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 11. Active Slice 1 resumption plan - 2026-08-12 04:02 PKT

1. Restore the real seeded local application stack and reconnect the required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run implementation and matching-state prototype screenshots before accepting UI/UX or parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** the required in-app browser connected, but the first fresh-page request timed out before a webview attached. The documented browser-interaction recovery retained the binding, checked controlled and user-visible tab lists, requested visibility, and requested one fresh page; the retry also failed before attachment. Both tab lists were empty and visibility remained false afterward. Docker Desktop's user process and WSL distribution were running, but Docker Engine requests timed out and the stopped Windows service could not be started by the scheduler account; this would block the seeded journey after page attachment, but the browser failed before navigation. No substitute browser, current-run screenshot, interaction, automated rerun, or product change was accepted. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 12. Active Slice 1 resumption plan - 2026-08-12 05:03 PKT

1. Restore the real seeded local application stack and reconnect the explicitly required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run screenshots before accepting UI/UX or same-state prototype-parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** local Supabase Auth returned `200`, PostgreSQL accepted connections, FastAPI returned `200`, and Next.js listened on `127.0.0.1:3002`. The idempotent seed refresh timed out while the Supabase CLI waited on the unresponsive Docker Engine, but the already-running platform endpoints remained healthy. The required in-app browser connected; its initial fresh-page request timed out before attachment. Supported recovery retained the binding, confirmed empty controlled/user-visible tab lists, requested visibility, and requested one fresh page; visibility remained false and the retry also timed out before attachment. No substitute browser, current-run screenshot, interaction, automated rerun, product change, or completion claim was accepted. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 13. Active Slice 1 resumption plan - 2026-08-12 06:04 PKT

1. Restore the real seeded local application stack and reconnect the explicitly required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run implementation and matching-state prototype screenshots before accepting UI/UX or same-state prototype-parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** the required in-app browser connected, but its initial fresh-page request timed out before a webview attached. Supported recovery retained the binding, confirmed empty controlled and user-visible tab lists, requested visibility, and requested one fresh page; visibility remained false and the retry also timed out before attachment. Docker Desktop processes and its WSL distribution were running, but Docker Engine requests timed out and the stopped `com.docker.service` could not be opened by the scheduler account. The browser failed before navigation, so the application-stack condition did not cause the page-attachment failure. No substitute browser, current-run screenshot, interaction, automated rerun, product change, or completion claim was accepted. Durable manual/UI evidence is committed at `710bc82`. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 14. Active Slice 1 resumption plan - 2026-08-12 07:04 PKT

1. Restore the seeded local application stack and reconnect the explicitly required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run implementation and matching-state prototype screenshots before accepting UI/UX or same-state prototype-parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** Supabase Auth, PostgreSQL, FastAPI, and Next.js were reachable. The idempotent seed refresh stalled on the Docker control channel, but the existing seeded platform endpoints remained healthy. The required in-app browser connected, but its initial fresh-page request timed out before a webview attached. Supported recovery retained the binding, confirmed empty controlled and user-visible tab lists, requested visibility, and requested one fresh page; visibility remained false and the retry also timed out before attachment. The browser failed before navigation. No substitute browser, current-run screenshot, interaction, automated rerun, product change, or completion claim was accepted. Durable manual/UI/parity evidence is committed at `95ff3a2`. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 15. Active Slice 1 resumption plan - 2026-08-12 08:03 PKT

1. Restore the seeded local application stack and reconnect the explicitly required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run implementation and matching-state prototype screenshots before accepting UI/UX or same-state prototype-parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** Supabase Auth and REST returned `200`, PostgreSQL listened on `127.0.0.1:55322`, FastAPI returned `200` on `/health`, and Next.js returned `200` on `/login`. The idempotent seed refresh stalled for 49 seconds and was stopped; the existing platform endpoints remained healthy. The required in-app browser connected, but its initial fresh-page request timed out before a webview attached. Supported recovery retained the browser binding, loaded the browser-interaction recovery guidance, confirmed empty controlled and user-visible tab lists, requested visibility, and requested one fresh page; visibility remained false and the retry also timed out before attachment. No substitute browser, current-run screenshot, interaction, automated rerun, product change, or completion claim was accepted. Durable Slice 1 blocker evidence is committed at `98c1a13`. Scheduler-started FastAPI and Next.js processes were stopped. Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4-10 remain untouched.

---

## 16. Active Slice 1 resumption plan - 2026-08-12 09:02 PKT

1. Confirm the seeded local application stack is healthy, then reconnect the explicitly required Codex in-app browser without substituting another browser surface.
2. If a page attaches, exercise timeout to stale/last-good to retry and complete manual keyboard, announcement/focus, reduced-motion, 200% zoom, permissions, adjacent-regression, and desktop/tablet/mobile checks.
3. Capture, save, and inspect current-run implementation and matching-state prototype screenshots before accepting UI/UX or same-state prototype-parity evidence.
4. Rerun the scoped Slice 1 automated, guardrail, lint, build, migration, and end-to-end gates only if manual verification passes or product code changes; repeat Code Review for security, privacy, authorization, tenant boundaries, and error handling.
5. Update durable evidence and this ledger. Mark Slice 1 `COMPLETE` only if every open gate passes; otherwise record the exact blocker and keep Slice 1 `IN PROGRESS`.

**Run result:** the required Codex in-app browser attached successfully and opened the real seeded project. The R1 application was aligned to the R2 Slice 1 shell at `fce7cc0`: expanded Outcome Integrity masthead, three pillar cards, five-band rail, complete exposure-ranked queue, Views/Documents navigation, persistent OSLO advisor, and central governed issue review. Manual issue opening, pillar routing, Escape close/focus restoration, visible Viability detail, matched 956×1040 source/implementation comparison, and console inspection passed with zero browser errors. Automated verification passed: focused Overview 35, full web 125, Slice 1 API 19, guardrail infrastructure 4, active selectors 9, ESLint zero warnings, and production build/TypeScript. The prior attachment blocker is resolved. Manual timeout/stale/retry/last-good, screen-reader, reduced-motion, 200% zoom, and current mobile checks remain unexercised, so Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4–10 remain untouched.

---

## 17. Slice 1 bounded-shell correction - 2026-08-12

1. Compare the activated R2 prototype and real seeded Overview at the same desktop viewport.
2. Correct shell bounds, default integrity state, central reading width, issue-row width, and narrow-screen clipping without changing governed data or issue behavior.
3. Exercise integrity expansion/collapse, issue detail open/close, advisor prompt, Outcome-to-Intent navigation/back, and mobile queue access in the Codex in-app browser.
4. Rerun the focused/full web, Slice 1 API, R2 guardrail, lint, build, and diff gates.
5. Record exact-size visual evidence and update this ledger without advancing another slice.

**Run result:** commit `5489ca6` bounds the desktop shell to 1600px, starts with the compact prototype integrity read, centers the 900px reading body, caps issue rows at 820px, retains the 266px navigation and 330px advisor rails, and removes mobile intrinsic-width clipping. The physically combined 1600×900 comparison is stored at `../code/reports/r2-slice-1-qa-2026-08-12/exact-shell-pass/03-prototype-vs-implementation-1600x900.png`. Manual integrity, issue, advisor, navigation, and narrow mobile queue checks passed. Automated verification passed: focused Overview 37, full web 127, Slice 1 API 19, guardrail infrastructure 4, active selectors 9, ESLint, diff check, and production build/TypeScript. Forced timeout/stale/retry/last-good, screen-reader, reduced-motion, and 200% zoom remain open, so Slice 1 remains `IN PROGRESS`; no later slice was acquired and Slices 4–10 remain owner-blocked.

---

## 18. Slice 1 queue and inline-issue parity correction - 2026-08-12

1. Compare the owner-provided R2 Issues queue and expanded-issue states with the real seeded Overview.
2. Correct the masthead, workspace-open notice, ranked issue styling, and inline issue hierarchy while preserving governed live data and existing behavior.
3. Verify inline non-modal semantics, Escape/focus restoration, persistent OSLO advisor, pillar navigation, responsive layout, and horizontal overflow.
4. Rerun focused/full web, lint, production build, and diff gates; preserve the earlier same-run API and guardrail evidence because no API or guard mapping changed.
5. Store physically combined comparisons and update the source-of-truth ledger without advancing Slice 2 or any blocked slice.

**Run result:** commit `9d44040` adds the prototype masthead/OFFICIAL treatment, SAMPLE badge, workspace-open notice, ranked queue hierarchy, and inline issue card with Affects/Holds up, first-time guidance, recommendation, evidence, impact, weakening, and resolution paths. The queue stays visible while an issue is open and the OSLO rail remains persistent. Combined visual evidence is stored at `../code/reports/r2-slice-1-qa-2026-08-12/inline-issue-pass/`. Browser checks passed with no horizontal overflow; focused Overview 38, full web 128, ESLint, diff check, and production build/TypeScript pass. Slice 1 remains `IN PROGRESS` only for forced timeout/stale/retry/last-good, real screen-reader, reduced-motion, and 200% zoom checks. OSLO Proposes and Resolved remain Slice 2 scope. No later slice was acquired; Slices 4–10 remain owner-blocked.

## 19. Slice 1 remaining manual-gate audit - 2026-08-12

1. Open the real seeded Overview in the Codex in-app browser and capture a fresh baseline.
2. Force an extended-analysis timeout, verify that no incomplete read publishes, and confirm the last successful issue queue remains visible.
3. Retry the failed analysis, observe the running state, and verify completion returns to `completed` / `extended_transition` with the last-good read intact.
4. Exercise a 200%-zoom-equivalent narrow viewport, the real operating-system reduced-motion preference, accessibility roles/landmarks/live region, inline-dialog focus, Escape close, and focus restoration.
5. Inspect browser errors, restore temporary operating-system and viewport settings, and record durable evidence without changing product code or another slice.

**Run result:** timeout/last-good/retry, 200%-zoom-equivalent reflow, reduced-motion behavior, accessibility-tree semantics, keyboard focus, Escape, and focus restoration pass. The narrow check had no horizontal overflow, the reduced-motion preference reached the page and collapsed transitions, the retry completed, and the operating-system animation preference was restored. Browser console errors were zero; five repeated Next.js image-development warnings remain. Evidence is stored at `../code/reports/r2-slice-1-qa-2026-08-12/manual-completion/`. NVDA is not installed and the in-app browser cannot capture synthesized speech, so a real spoken screen-reader session remains unverified. Slice 1 stays `IN PROGRESS` only for that assistive-technology confirmation; no later slice was acquired and Slices 4–10 remain owner-blocked.

---

## 20. Slice 3 acquisition and implementation plan - 2026-08-12

1. Preserve Slice 1's passed evidence and record the owner's direction to defer the combined spoken screen-reader audit until Slices 1–3 are otherwise complete.
2. Trace AC-1…AC-10 to the existing Release 1 recompute backbone and active R2 tests; implement one RED → GREEN behavior at a time.
3. Deliver the act → addressed/STALE → consolidated scoped Fast reanalysis → one integrity update → FRESH tracer path, with last-good retention, failure/retry, and append-only supersession.
4. Implement the real-event first-analysis, personalized graph, outcome confirmation, pending/STALE/reanalysis, provisional, Deep refinement, read-moved, and presentation-only freeze/unlock UI states against the selected prototype targets.
5. Complete Code Review, in-app-browser regression, matched-state prototype comparison, automated gates, durable evidence, and Conventional Commits before advancing to Slice 2.

**Acquisition result:** branch `codex/release-2-build` was clean at acquisition and the hourly automation was paused, so no conflicting slice implementation was active. Slice 3 is now `IN PROGRESS`. This entry records operational delivery status only; it does not ratify or alter product canon. Slices 4–10 remain owner-blocked.

---

## 21. Slice 3 prototype-animation correction and QA - 2026-08-12

**Correction delivered:** the simplified production canvas approximation was removed and replaced with a production copy of the prototype's real 70 KB kinetic onboarding arc. Mechanical parity tests prove that the core `buildGraph` implementation and animation loop remain unchanged. The production wrapper feeds real analysis events, progress, project title, inferred outcome, confirm/refine/defer decisions, persistence success/failure, and navigation through a same-origin message contract. Prototype-only controls are hidden in embedded mode; responsive, reduced-motion, dialog naming, and focus-entry behavior were added without changing the visual engine.

**Verification result:** focused Slice 3 parity/flow tests pass 10/10; full web regression passes 24 files/138 tests; full API regression passes 303 tests; Ruff, ESLint, TypeScript/Next production build, static animation syntax, HTTP asset delivery, API health, and R2 guardrails pass. The production server was rebuilt and restarted on port 3002.

**Completion evidence update:** local production and prototype inspection now works in the approved in-app browser. The first-read kinetic journey, outcome decision, production landing, issue clarification/action, immediate stale/Undo projection, reanalysis completion, queue/evidence refresh, responsive reflow, and same-run prototype comparisons pass. Evidence is stored at `../code/reports/r2-slice-3-qa-2026-08-12/manual-live/`. The shared spoken screen-reader audit remains owner-deferred; Slice 3 therefore stays conservatively `IN PROGRESS`, and Slices 4–10 remain owner-blocked.

---

## 22. Slice 3 live manual correction and final browser gate - 2026-08-12

**Live defect and fix:** an issue clarification or recommended action queued the governed analysis correctly, but the Overview did not project the top-level stale-read banner and pending Undo control until a later refresh. Commit `6dfdebe` projects the queued freshness state immediately from both response paths and clears a withdrawn run's local in-progress latch. Focused assertions prove both paths expose `Your read is safely out of date.` and `Undo last change`.

**Visible browser run:** the approved in-app browser exercised sample intake → real analysis → graph/pillar animation → outcome confirmation → Overview → issue clarification/action → stale/Undo → completed reanalysis. The refreshed queue, advisor, navigation, evidence counts, reload behavior, and narrow no-overflow layout remained functional. A late Undo attempt correctly announced `The change can no longer be undone.` after the worker acquired the event.

**Parity result:** same-run prototype/production graph and decision captures show the actual signed kinetic engine and the same decision-card visual system. Live content and animation timestamps are intentionally dynamic, and prototype-only controls are intentionally absent in embedded production; no actionable P0/P1/P2 mismatch was found.

**Fresh verification:** `pnpm test:web` passed 24 files/138 tests; `pnpm test:api` passed 303 tests; `pnpm lint:web` passed; `pnpm test:r2-guardrails` passed 4 infrastructure tests plus 9 active-runner tests across 6 active guards; the production build and diff check pass. The shared spoken screen-reader session remains open by owner direction. Slice 2 is now the next executable slice; Slices 4–10 remain blocked.

---

## 23. Slice 2 acquisition and accepted owner choices - 2026-08-12

**Acquisition:** branch `codex/release-2-build` was clean and the scheduler remained paused. Slice 2 is the only newly acquired implementation scope; Slices 4–10 remain owner-blocked.

**Accepted implementation choices from the owner-directed Grill session:** `answered` is a typed BASIS ranked below `verified-directly`; reviewer rejection appends a first-class attributed flag and routes to needs-a-fix; withdrawal reopens live state, appends a reversal, preserves prior records and the activation latch, then triggers confirming reanalysis; `groundMitigated` appends a separate grounding attestation while retaining the fix record. These choices are implementation direction recorded for resumption and do not let this ledger supersede the signed slice or repository canon.

**Execution gates:** one public-behavior RED → GREEN cycle at a time; complete AC-1…AC-11 and DL-211; activate only the Slice 2 guard twins; compare the executable app against the signed R2 prototype; run full API/web/guardrail/lint/build regression; capture durable manual evidence; then run the combined spoken screen-reader gate for Slices 1–3 before marking any of them complete.

---

## 24. Slice 2 implementation and final browser gate - 2026-08-13

**Implementation delivered:** commit `dd69e69` adds typed append-only attestations for confirm, answer, flag, fix, ground, route, withdraw, and reviewer responses; reanalysis-only closure; immutable history; real scoped review grants; itemized build/inference/optional proposals; and shared proposal decisions across folded-read, issue-card, and artifact surfaces. The production UI adds the prototype's OSLO Proposes block, Awaiting evidence, Acted on—not yet closed, Resolved, and persistent cleared-queue guidance.

**Live defect and correction:** the first approved-browser proposal Reject reached the API but failed while recording History because a non-reanalyzing decision had no new run identifier. The service now records the decision event against the proposal's source read (falling back to the project's current read), and a database integration regression proves that association. The visible Reject retest passed and the proposal count changed from three to two without an API error.

**Visible browser run:** the approved in-app browser exercised issue expansion, secure evidence routing, Awaiting-evidence projection, withdrawal and queue restoration, proposal Reject, proposal-count refresh, confirmation, governed reanalysis, and the Resolved tray. Side-by-side queue and expanded-issue review used the owner-provided R2 references at matched desktop states; applicable shell, hierarchy, colors, borders, spacing, controls, proposal group, trays, and advisor structure match with no actionable P0/P1/P2 structural mismatch. Live findings and counts remain backend-driven.

**Fresh verification:** full API regression passed 316 tests in the split main plus isolated UI-contract run; full web regression passed 24 files/143 tests; focused Slice 2 coverage passed 63 tests; R2 guardrails passed 4 infrastructure tests plus 17 active tests across 18 active guards; Ruff, ESLint, Next.js production build/TypeScript, and diff check pass. The shared spoken screen-reader session remains open by owner direction. Slices 4–10 remain owner-blocked.

---

## 25. Slice 2 final prototype-parity hardening - 2026-08-13

**UI and motion correction:** matched 1280 x 720 comparisons identified and corrected the remaining applicable differences: the exact OFFICIAL masthead copy, prototype Understanding-document order, governed/Wider advisor header, inline issue auto-position and disclosure hierarchy, removal of implementation-only proposal-kind labels, and the prototype entrance/lifecycle motion timings. The production implementation now uses the prototype's 340 ms issue/proposal entrance, 1 s lifecycle flash, 1.25 s tray-row settle, and workspace-unlock motion, with all decorative motion disabled under `prefers-reduced-motion`.

**Visible functional run:** the approved in-app browser opened an issue, routed it through the real secure evidence flow, verified the Awaiting Evidence lifecycle projection and active tray animation, withdrew the route, and confirmed the ranked queue returned without an application error. The same run checked issue disclosure, proposal controls, governed Wider/Narrower behavior, 390 x 844 responsive reflow, and zero horizontal overflow.

**Matched evidence:** physically combined queue, expanded-issue, and proposal/lifecycle comparisons plus the written audit are stored at `../code/reports/r2-slice-2-ui-qa-2026-08-13/`. Dynamic project data, issue text, proposal counts, and reliability values remain backend-driven and therefore are not copied from prototype fixtures. No actionable P0/P1/P2 mismatch remains for the applicable Slice 2 states.

**Fresh verification:** full API regression passed 316 tests; full web regression passed 24 files/145 tests; focused Overview passed 46 tests; focused Slice 2 total passed 65 tests; R2 guardrails passed 4 infrastructure tests plus 17 active-runner tests; ESLint, Next.js production build, TypeScript, and diff checks pass. The single combined spoken screen-reader session for Slices 1-3 remains the only owner-deferred gate. Slices 4-10 remain owner-blocked.

---

## 26. Phases 2–6 completion — 2026-08-13

**Implementation and re-comparison:** invitation, activation, welcome, first-time intake, returning-client intake, real prototype animation, Issues shell, stable toggles, OSLO Proposes, lifecycle trays, and real-logo/brand presentation now match the applicable prototype states. Prototype-only controls marked “not shipped” remain excluded. The physically combined comparison is stored at `../code/reports/r2-phases-2-6-qa-2026-08-13/evidence/issues-prototype-vs-app.png`.

**Functional and live regression:** the new-client admin invitation, new-user activation, first guided project, existing-client second project, real DOCX/PDF/XLSX upload, field-by-field extraction, issue population, reanalysis, proposal decisions, and lifecycle transitions pass. A final accepted-proposal withdrawal defect was found, fixed test-first, and verified live: the accepted build proposal now records a lifecycle `fix` attestation and Withdraw appends its superseding reversal without an error.

**Final gates:** web `24 files / 152 tests`, API `319 passed`, guardrail infrastructure `4 passed`, active guardrails `17 passed`, Ruff, ESLint, and the Next.js production build pass. Slices 1–3 are **COMPLETE**. Slices 4–10 remain **OWNER-BLOCKED** and were not advanced.

_This is an operational delivery ledger created at the owner's direction. Product and governance authority remain with the owner; this ledger reports evidence and must not be used to ratify or redefine scope._

---

## 27. Exact UI parity remediation and final evidence — 2026-08-13

**Slices 1-3 status:** implementation, functional regression, UI/UX review, manual browser regression, prototype comparison, and automated test coverage are **COMPLETE** for the requested R2 scope. The previously owner-deferred combined spoken screen-reader session remains recorded as a separate non-visual accessibility follow-up; it does not reopen the completed UI remediation.

**Final corrections:** production now includes the onboarding prototype-control strip, source-derived first/returning animation states, prototype first-grounding-act blur/focus, recorded outcome and one-call-down lock, functional Resolved and OSLO Proposes close/reopen, Quick Tour and Feedback inside the sidebar, inline non-modal issue review with adjacent OSLO advisor, stable issue close with no scroll jump, and blue/green/magenta masthead pillar states.

**Final browser evidence:** Quick Tour and Feedback opened named dialogs; Resolved and OSLO Proposes moved `aria-expanded` true → false → true and returned their bodies to `aria-hidden=false` / `display:block`; issue opening created one inline `Issue details` region and zero dialogs; issue close preserved `window.scrollY` (`0` before and after). Physically combined prototype/application evidence is stored at `../code/reports/r2-exact-parity-2026-08-13/`.

**Final gates:** web **24 files / 154 tests passed**; API **323 tests passed**; R2 guardrails **4 infrastructure + 17 active tests passed** with 18 active guards and 6/6 prototype corrections; ESLint, Ruff, TypeScript, Next.js production build, and diff check passed. A Windows-only UTF-8 subprocess-decoding defect in the rendered Slice 2 guard was corrected and the guard rerun passed.

**Remaining work:** no requested P0/P1/P2 UI or functional defect remains. Live issue text, counts, recommendation copy, and analysis events intentionally remain backend-driven instead of copying prototype fixtures. Slices 4-10 remain **OWNER-BLOCKED**.

---

## 28. Sidebar, returning-client, and workspace-notice follow-up — 2026-08-13

**UI parity result:** the four owner-reported visual defects are fixed. Quick Tour, Feedback, plan, and account controls are contained inside the desktop sidebar; established workspaces carry an explicit returning-client state into the watch-it-work analysis; the Returning control remains visibly active after load/restart; and dismissing “Your workspace is open” removes the banner from layout so the issue queue moves up without a blank gap. The existing first-run `freeze_on` root-shell class continues to provide the prototype blur/focus state.

**Evidence:** `../code/reports/r2-parity-followup-2026-08-13/FINAL_REPORT.md` and `../code/reports/r2-parity-followup-2026-08-13/screenshots/prototype-vs-app-side-by-side.png`.

**Verification:** full web regression **24 files / 156 tests passed**; focused follow-up regression **4 files / 71 tests passed**; R2 guardrails **4 infrastructure + 17 active tests passed** with 6/6 prototype corrections; ESLint passed; Next.js production build and TypeScript passed; live browser checks passed for sidebar containment, workspace-notice reflow, visible prototype playback controls, and returning-client watch mode. This follow-up closes the listed UI defects only; previously recorded real-document semantic extraction and source-specific advisor-quality items remain separate open gates. Slices 4–10 remain owner-blocked.

_This is an operational delivery ledger created at the owner's direction. Product and governance authority remain with the owner; this ledger reports evidence and must not be used to ratify or redefine scope._

---

## 29. Slice 4 owner reopening and implementation acquisition — 2026-08-13

**Acquisition:** the owner explicitly directed implementation of Slice 4 after reviewing its flow, scheduler steps, and implementation plan. Slice 4 is therefore reopened as `IN PROGRESS`; Slices 5–10 remain `OWNER-BLOCKED`, and the R2 scheduler remains paused during active implementation.

**Accepted implementation direction:** the Free capacity applies to one active Plan and one active Outcome; Basic is $29 monthly or $290 annually with three active Plans and no marketed Outcome-count limit; checkout is real and hosted; only a signature-verified provider webhook may grant the entitlement; cancellation and payment failure preserve data; Outcome archival is reversible; records, reviewers, Viewers, manual file export, and judgment quality are never capacity-gated.

**Execution gate:** implement one observable public behavior at a time using RED → GREEN → REFACTOR. Do not infer or implement Slice 5 multi-outcome reading or deferred disclosure as part of this acquisition.

---

## 30. Slice 4 implementation and verification evidence — 2026-08-13

**Implementation delivered:** Free now includes one active Plan, one active Outcome, and an approximately 50k extracted-word envelope; Basic is $29 monthly / $290 annually, includes three active Plans, multiple active Outcomes, and the same judgment quality. Collaborators, reviewers, Viewers, the record, manual file export, and judgment quality are not monetized. A first analysis persists its inferred primary Outcome, and confirm/refine promotes that first-class record to declared provenance. Outcome archive/reactivate is reversible, preserves the record, and enforces the active slot under a workspace lock.

**Billing safety:** the browser cannot set a paid tier directly. The backend creates provider-hosted Stripe subscription Checkout and customer-portal sessions from server-owned Price IDs and metadata. A pending Checkout grants nothing. Only a Stripe-signature-verified, paid Basic `checkout.session.completed` event that matches a server-created session writes one idempotent CommitmentLog and grants Basic. Subscription events preserve existing work through payment grace and cancellation; cancelled over-limit work is grandfathered and no new capacity is granted. Every commitment/free-path/decline/keep-both choice is durably recorded.

**Fresh automated evidence:** `uv run pytest tests` passed **351 tests**; `pnpm --filter @oslo/web test` passed **25 files / 158 tests**; `pnpm lint:web`, `uv run ruff check src tests`, `pnpm build:web`, `git diff --check`, local migration listing, epistemic-invariant gate, and observability gate pass. `pnpm test:r2-guardrails` passed **4 infrastructure + 21 active-runner tests**, with **22 active / 38 pending** guards and `GT-01`, `GT-02`, `GT-03`, and `GT-30` active for Slice 4. The production build includes the new billing, intent, and Outcome routes.

**Manual browser evidence:** a real Free workspace showed the second-Plan wall and the full capacity-only comparison: Free one Plan / one Outcome / ~50k words, Basic $29 monthly or $290 annually, no per-seat price, and the explicit never-limited list. The annual toggle and server-authoritative pending state worked; with no local Stripe configuration, the UI returned the truthful `Billing is not configured in this environment` failure without changing entitlement. A real first analysis completed and exposed the Manage Outcomes dialog. During the final Outcome-list request, Turbopack exhausted the C: drive and panicked; the authenticated API itself returned 200 with the persisted primary Outcome. Dependency/build caches were pruned, the server was restored on port 3002, and no source or user data was removed. The in-app browser then blocked the required localhost reload under its URL policy, so no replacement browser was used and the final visual sequence remains unverified.

**Open gates:** Gate 2 contract traceability fails because `ci/gate_contract.py` has no approved entitlement/monetization contract identifier; selecting an unrelated cognition contract or using the Phase-I infrastructure bypass would be false evidence. Live Stripe test-mode Checkout and signed-webhook verification also require owner-provided environment configuration. These gaps keep Slice 4 at `IMPLEMENTED · UNVERIFIED`; they do not authorize Slice 5.

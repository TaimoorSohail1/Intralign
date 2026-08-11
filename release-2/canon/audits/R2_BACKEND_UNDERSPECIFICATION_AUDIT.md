# R2 Backend Underspecification Audit — pre-handoff

*2026-08-04 · Audit of `oslo-prototype-r2.html` (the official AI-first R2 prototype) + the R2 decision set, measured against the R1 engineering canon (`oslo-knowledge-base/20_handoff` + `/30_engineering`). Purpose: surface every place R2 is not explicit enough to BUILD against — **especially backend** — so gaps are resolved before the product-grill turns them into vertical slices. Directly answers the R1 dev complaint that "certain backend pieces were underdefined."*

*Method: six parallel domain audits, each grounded in the prototype's actual stubs, the ratified R2 decisions (DLs), and the R1 contract canon. Every gap is evidence-anchored (prototype fn / DL / canon file). Findings were verified against the prototype source and the canon before inclusion; two false positives were caught and are recorded in §7.*

---

## 0. The rigor bar this audit measures against

R1 eventually answered its own "underdefined" complaint by building a full contract stack: an **API Contract**, **Event Model**, **State Model**, a **Runtime Object/Data Model**, **scoring models** (CAF / Confidence / Reliability V2), a **telemetry/observability** spec, **testing fixtures**, and — the keystone — a **UI↔Backend Integration Map** that binds *every dynamic UI element* to a Read / Write / Event contract and lists the residual gaps (G1–G8) with "why it matters" + a recommendation.

**That stack is the definition of "specified enough to build."** This audit measures R2 against it. The top-line result: R2's *net-new and changed* behavior (the AI-first reimagining + freemium + feedback/survey) has **none of those five contract artifacts yet**, and in several places R2 doctrine **directly contradicts** ratified R1 canon that a developer would otherwise build by default.

---

## 1. HEADLINE FINDING — two divergent R2 lineages that collide (resolve before anything else)

This is the single most important thing to fix before handoff, and it is a *super-set* of the R1 "underdefined" problem: R2 is not merely under-specified in places, it is **doubly-specified with conflicts.**

There are two parallel R2 lineages:

- **Lineage A — the R2 "canon" track.** The `product-design/prototype-r2_XX.html` mockups in the knowledge base, against which **DL-164 … DL-197** (the `DL-1xx_NAMED_IN_CAPS` files) were ratified — including the **graph schema (DL-184)**, the **unified issue layer (DL-196)**, the **false-confidence issue type (DL-197)**, and a **158–183-check guard suite**.
- **Lineage B — the AI-first candidate track.** `oslo-r2-candidate.html`, promoted this session to **`oslo-prototype-r2.html`** (the file you designated as the primary build source), plus the freemium/feedback decisions **DL-172 (freemium), DL-173 (owner-activation)** and a **23-check `_S10`** suite.

**The two have diverged, and verification confirms it:**

1. **The ratified canon issue-layer is not in the official prototype.** DL-196/DL-197 describe a unified issue layer (per-issue `dim`/`ftype`/`exposure`, `_ciFalseConfidentArtifacts`, `readsStrong`, `_syncFalseConfidenceIssues`) and call it "built + green 183/183." A direct grep of `oslo-prototype-r2.html` returns **0** for every one of those identifiers; its `_S10` suite is **23** checks, not 183; and its `ISSUES` array is a separate hardcoded list using a `crit`/`mod` severity vocabulary that doesn't even match the worklist's own `critical/moderate/warning`. **The official prototype does not implement the ratified issue-layer/false-confidence architecture.**

2. **DL numbers collide.** `DL-172` is *both* "Freemium value moments / unit = outcome" (Lineage B, 2026-08-04) *and* "First-run prompt orchestration" (Lineage A). `DL-173` is *both* "Owner activation = first grounding act" (B) *and* "Fold the strategic chain into the grounding reveal" (A). Same numbers, different ratified content.

**Why this blocks the build:** a developer told "build R2 from the prototype and the DLs" has two contradictory sources of truth and no way to know which governs. This is precisely the failure mode that produced the R1 complaint, amplified.

**What's needed (owner decision, first):** declare the **canonical R2 source of truth** and reconcile. The likely intent — confirmed by your earlier direction ("convert this candidate to the official R2 prototype… my primary file") — is that **Lineage B (the AI-first prototype) is the go-forward**, and Lineage A's DLs must be **re-adjudicated against it**: each DL-164…197 decision is either (a) carried into the AI-first model (and re-built/re-verified there), (b) superseded, or (c) renumbered to end the collision. Until that reconciliation exists, every per-domain gap below inherits the ambiguity. **This is the prerequisite to product-grill.**

---

## 2. The meta-gap — R2 has none of the five R1 contract artifacts

Across all six domains, the same structural gap recurs: **R2's only backend documentation is capability *narrative* (`oslo-backend-capabilities.md`, 18 caps) plus decision records.** There is no R2 equivalent of:

| R1 artifact (exists) | R2 equivalent (missing) | Consequence |
|---|---|---|
| `RELEASE_1_STATE_MODEL_SPECIFICATION_V1` | R2 state model | Issue lifecycle, freeze/unlock, archive, ticket, survey-eligibility states all undefined as transitions |
| `RELEASE_1_EVENT_MODEL_SPECIFICATION_V1` | R2 event model | No grounding-act / intent-signal / feedback / survey / activation events defined |
| `RELEASE_1_API_CONTRACT_SPECIFICATION_V1` | R2 API contract | No endpoints for outcomes, archive/reactivate, review-requests, roll-up, feedback, survey |
| `RUNTIME_OBJECT_MODEL` / `DATA_MODEL` | R2 data model | Outcome/Plan/Entitlement/Ticket/SurveyResponse objects + cardinality undefined |
| `R1_UI_BACKEND_INTEGRATION_MAP` | R2 integration map | New surfaces (roll-up, grounding map, feedback door, VM moments) not bound to Read/Write/Event |

**Recommendation:** the product-grill's output should *be* these five artifacts for the R2 delta (not the whole system — most of R1's stack is reusable; see §6). The per-domain registers below are the raw input for them.

---

## 3. Cross-cutting doctrine landmines (a naive build breaks doctrine here)

These recur across domains and are the highest-risk items because a competent developer will build the *wrong* thing by default, silently violating doctrine. Each must be an explicit, testable build constraint.

- **DL-L1 — The freemium gate a dev builds by default.** R1 canon *actively specifies hard gating*: `project_limit_reached → POST /projects 422 (UP-3)`, `limit_reached → 429` caps, an `upgrade_page_viewed→started→completed` checkout funnel, and an Upgrade-Intent Score built on pricing-page visits (`TELEMETRY §…`, `API_CONTRACT §…`). R2 doctrine says **nothing is gated in Alpha — the walls are intent-capture only.** A dev handed R1 canon + R2's prose builds the 422 gate at the 2nd outcome. **Fix:** an explicit `enforcement_mode ∈ {observe, enforce}`; Alpha ships `observe` = evaluate + emit signal + **always allow**; R1's 422/429 gates are marked *superseded in Alpha*.
- **DL-L2 — Metering the growth engine.** "Entitlement checks" naturally get wrapped around every path. The record, the reviewer/CRR loop, and Viewers must **never** be metered. **Fix:** the entitlement contract must carry an explicit *never-metered exemption list*, asserted as tests.
- **DL-L3 — Terminal archive kills the free path.** R1's only archive (`Project:archive`) is **terminal + owner/admin-gated**. R2's "archive-to-switch" must be **reversible + self-service + record-stays-viewable**. Reusing R1's archive turns the honest free rotation into a destructive dead-end. **Fix:** a reversible outcome-level `archive`/`reactivate` contract.
- **DL-L4 — The freeze must be presentation-only.** The first-run freeze (`pointer-events:none` + blur until 2 grounding acts) must be a pure client pacing device; the server must **never** withhold the read based on `confirmCount`, or the freeze becomes a real capability gate (violates "nothing gated in Alpha"). **Fix:** spec states the freeze is presentation-only; the read API never gates on activation count.
- **DL-L5 — Feedback free-text can leak plan content.** Auto-context is metadata-only (good), but the user-typed feedback/defect fields ship verbatim to an external tracker with no scrub. The doctrine "no plan content leaves" is copy, not mechanism. **Fix:** a named sanitization boundary (allowlist for auto-context; redaction/scan for free text) at the feedback-service egress.
- **DL-L6 — Feedback/survey isolation is behavioral, not structural.** Today they don't touch the read only because the submit handlers happen not to call `pushHist`. Doctrine requires *structural* inability. **Fix:** isolated store, no write credentials to the plan/finding/attestation/History domain; assert with a test.
- **DL-L7 — The integrity gate vs R1 Non-Collapse.** R2's `min(Viability, Grounding, Adaptability)` gate directly overrides R1 Confidence-Model IR-8 ("reliability alone must not drive the band to Very Low") and IR-4 ("not weakest-link"). Unreconciled, the build either can't gate or silently breaks ratified canon — and a gate that slams to "Very Low" reads as health/RAG unless the maturity framing is airtight. **Fix:** owner ratifies that the pillar gate is a new construct that supersedes IR-4/IR-8 *for the composite only*, with maturity-not-forecast framing preserved.
- **DL-L8 — "Roles shown, not enforced" collides with reviewer scope.** The prototype says roles/links are "presentation-only this release," but the external-reviewer scope ("never sees the whole plan") is an **access-control guarantee that must be hard-enforced.** **Fix:** split — owner/delegate distinction may be display-only; external-reviewer scope is enforced (403 on anything but the one question).
- **DL-L9 — Activation event must survive withdraw.** Withdraw decrements `confirmCount`; if activation is a durable funnel event, decrementing would retroactively un-activate a user. The append-only record is never rewritten. **Fix:** the live freeze gate may re-lock, but the activation *event* is immutable once emitted.

---

## 4. Per-domain gap registers

Severity: **Blocker** (cannot build the capability without it) · **Major** (buildable but will be wrong/rework) · **Minor** (polish / can defer with a note). "O" = needs an **owner decision**; "S" = needs **spec-writing** only.

### 4.1 Outcome-Integrity assessment model (the #1 backend risk)
**Coverage: NOT build-ready.** The three-pillar model (Integrity = weakest of Viability/Grounding/Adaptability) is positionally ratified but not specified as a computable model, and the prototype computes pillars from hardcoded counts, not from the issue layer the decisions say drives them.

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| OI-1 | Blocker | `min()` pillar gate has no build spec and **collides with R1 IR-4/IR-8** (Confidence V2 forbids weakest-link + forbids reliability-alone collapse). Two contradictory consolidation laws. | Dev can't know which governs. | O |
| OI-2 | Blocker | Band enum/count/thresholds net-new & unspecified (proto: 4 word-bands + 7-slot map, thresholds hardcoded to DevNorth's 6 items / 3 checkpoints; R1 uses 5 bands). No rule maps analysis → word-band generically. | Doesn't generalize to an arbitrary plan; enum count unresolved. | S(+O for labels) |
| OI-3 | Blocker | **Adaptability** is fully net-new (checkpoint-optimization assessment) with no computation spec; DL-194 §5 open: new dimension vs property of Feasibility. Denominator ("how many checkpoints a plan *needs*") undefined. | The band is meaningless without the target model. | O+S |
| OI-4 | Blocker | The DL-196/197 issue-layer that is supposed to drive the pillars **is not in the prototype** (see §1); pillars compute from raw counts, not severity-weighted issues. | No source of truth for the issue→pillar contract. | O+S |
| OI-5 | Major | **Grounding** pillar's mapping to R1 Reliability is undefined and it *inverts* Non-Collapse (a gating pillar vs Reliability-never-collapses). Inputs (coverage/assessability vs grounded-count) undefined. | Can't tell if Grounding = re-homed Reliability or net-new. | O+S |
| OI-6 | Major | **Viability** contradicts the R1 CAF canon it claims to inherit (proto uses "weakest sub-dimension" + a `+1` band bump on 2 applied fixes — an evidence-free rise). | Ambiguous computation; doctrine risk (band rises without evidence). | S |
| OI-7 | Major | False-confidence type (DL-197) unspecified in the deliverable; depends on an undefined "reads strong" signal (circular with OI-5). | Type is uncomputable as written. | S |
| OI-8 | Minor | Exposure/leverage ranking is a self-acknowledged proxy (`sev*10+lev`); true structural-reach needs an issue→outcome graph that doesn't exist. | Fine as interim; must be labeled so build doesn't over-promise "reach." | S |

**Doctrine risks:** OI-1/OI-5 (gate vs Non-Collapse); top-band label "Sound" risks reading as "healthy/will-succeed" (forecast) — DL-194 §4.5 endpoint labels unshipped; OI-6 evidence-free band pump; OI-3 must stay ordinal maturity, never "% protected." *(Note: the prototype's anti-forecast **surface copy** is strong — the risk is entirely in the unspecified computation beneath the words.)*

### 4.2 Issues layer, grounding acts & provenance
**Coverage: prototype-only strings; no R2 state/event/data contract. R1 attestation *primitives* are strong and reusable, but R2's issue objects were never bound to them.**

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| R2-I1 | Blocker | Issue lifecycle defined by **three incompatible vocabularies**: proto `inf/routed/addressed/you/fixed` vs R1 finding `Detected→…→Closed` vs the ratified phased `Inferred→Settled→Resolved`. No authoritative state spec (R1 STATE_MODEL scopes R2 out). | No canonical states/transitions/enum. | O+S |
| R2-I2 | Blocker | The **ratified** phased-resolution model (with a "Settled — needs a fix" fork) is *not implemented* — proto treats `you` (grounded) and `fixed` (plan-changed) as mutually-exclusive terminals, the dishonest model the DL was written to kill. | Building from proto ships the model the DL retired. | O |
| R2-I3 | Blocker | BASIS taxonomy not a defined enum + data model; cap #2 says 4 bases, proto `_CONFIRM_BASES` has 3, reviewer-answered stores basis `null`. | Can't build the basis column / validate / render provenance. | O+S |
| R2-I4 | Blocker | **Withdraw/reversibility** unspecified and conflicts with R1 append-only ledger ("roll back" vs "never overwrite"). Three reversal shapes (withdraw item / withdraw route / groundMitigated) with no contract. | Immutable ledger + withdraw are contradictory without a reversal-record contract. | S |
| R2-I5 | Major | Route-as-activation (DL-173) has no event/metric contract; no unified `grounding_act` event exists (R1 has none). | The ratified activation metric is unbuildable/unsegmentable. | S |
| R2-I6 | Major | Evidence-vs-comment separation is UI-only; R1 event model has a comment→context→Deep-analysis path that would let a comment influence the read. | Doctrine invariant asserted in copy, breachable in the inherited event path. | O+S |
| R2-I7 | Major | FLAG is not a first-class ledger attestation (proto sets only `flagged=true`); breaks confirm/flag symmetry in provenance. | Ledger can't answer "who flagged, on what basis" for half the grounding acts. | S |
| R2-I8 | Minor | Routed reviewer round-trip states not mapped to R1 `ReviewRequest`/`StakeholderResponse`; reviewer-reject→flag authority undefined. | Round-trip states unbound. | S |

**Doctrine risks:** DL-L9 (withdraw un-firing activation); unmetered-record under reversal/archive; "addressed" must never imply the read moved (a few paths set `you` directly, bypassing reanalysis); flag must render equal to confirm (D133).

### 4.3 Reanalysis engine + first-run reveal / freeze / unlock
**Coverage: R1 recompute backbone is strong and reusable; R2 adds a faster grounding-act batch, a freeze/unlock orchestration, and a stale contract — none specified to build-grade.**

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| R2-RE-1 | Blocker | Grounding-act batch window/trigger has no real thresholds (proto stubs 1500ms/900ms; R1 OPEN_DECISIONS OD-10 debounce = TBD). R2 adds a *seconds-scale* window class R1 never scoped (R1 = hours-scale Deep coalescing). | Can't build the queue (window/cooldown/max-age/consolidation key). | O+S |
| R2-RE-2 | Blocker | Fast-vs-deep pass on the batch unresolved (R1 gap **G7** carried forward); "~1–2s perceived" ≠ any real R1 pass. | Can't wire events/latency/reliability qualifier. | O |
| R2-RE-3 | Blocker | Freeze/unlock has no backend state contract; `firstRun` set true and **never cleared**; `withdrawItem` calls `applyFreeze()` → **workspace re-freezes on withdraw** (almost certainly unintended). | Latched-vs-live unlock, persistence, per-user vs per-project all undefined. | O+S |
| R2-RE-4 | Major | `confirmCount` as a server metric unspecified (which acts count, decrement-on-withdraw, durability); activation="confirmCount≥1" not a real server signal. | Freeze threshold + activation funnel + survey gate all key off it. | S |
| R2-RE-5 | Major | STALE contract: what's labeled where; the main read is deliberately **ambient** (no stale banner) while egress surfaces show it — no spec, and in tension with doctrine "must be labelled." | Needs first-class `read_freshness` state + product ruling on ambient-vs-egress. | O+S |
| R2-RE-6 | Major | R2 event→recompute table untabulated (which act enqueues, which pass, which pillar each moves — Viability vs Grounding). | Batch consolidation + supersession can't be wired deterministically. | S |
| R2-RE-7 | Major | Post-stage-model progress + next-move thresholds are client stubs (DL-189 retired stages; DL-190 limiter cap=1; `frac≥0.5` crossing). | Backend now owns "next best move" as a computed contract. | S |
| R2-RE-8 | Minor | Reveal seen-once persistence + graph/exposure data provenance under-specified (otherwise pure client). | Reveal re-fires cross-session; exposure % must be real grounded/inferred data. | S |

**Doctrine risks:** DL-L4 (freeze presentation-only); DL-L (ambient stale read vs "must be labelled" — needs owner ruling); "only reanalysis changes the assessment" — proto flips to `addressed` + celebration before the batch; guarantee the *integrity move* happens only in `_completeReanalysis`.

### 4.4 Freemium — tiering, entitlements, intent-capture, archive
**Coverage: NET-NEW-UNSPECIFIED and actively contradicted by R1 (which specs the opposite, gating doctrine). Highest count of doctrine landmines.**

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| F1 | Blocker | No entitlement/tier data model; no Alpha-vs-post-Alpha **enforcement-mode** contract (`tier` is a bare Principal string with no grants). | Can't represent "Free = 1 active outcome" or know whether a check blocks. | O+S |
| F2 | Blocker | R1's gating apparatus (422/UP-3, 429 caps, checkout funnel) **contradicts** non-gating doctrine and isn't retired/reconciled. *(= DL-L1)* | Dev builds the 422 gate at the 2nd outcome by default. | O+S |
| F3 | Blocker | OUTCOME not modeled as a first-class metered object; outcome↔plan↔workspace cardinality undefined. R1 says outcome = Canonical Fact and `Intend` = "do not add in R1." | Nothing to count/cap/rotate; contradicts an R1 modeling call. | O+S |
| F4 | Blocker | Archive/reactivate unspecified as reversible + self-service + record-viewable; R1 archive is terminal + admin-gated. *(= DL-L3)* | The free rotation path breaks. | O+S |
| F5 | Blocker | Intent-signal event stream has no schema/storage/query; proto logs in-memory `{vm,tier,ctx,ts}`. | The sole Alpha monetization deliverable (demand data) isn't captured. | S |
| F6 | Major | "Chosen path" + full option set not captured (only the keep-both branch emits); no denominator → can't compute intent rate. | Signal uninterpretable. | S |
| F7 | Major | R1 Upgrade-Intent Score depends on pricing/checkout R2 deliberately lacks; Alpha demand metric undefined. | R1 metric silently reads ~0; looks broken. | O+S |
| F8 | Major | Neutral-copy rule (no tier name/price user-facing) is prose, not a testable build constraint. | Copy drifts; a well-meaning CTA leaks a tier name with no failing test. | S |
| F9 | Major | Never-metered invariants (record, reviewer loop, Viewers) not expressed as explicit entitlement-check exclusions. *(= DL-L2)* | "Entitlement checks" accidentally meter the growth engine. | S |
| F10 | Major | Active-slot invariant + archive/reactivate side-effects (in-flight analysis, notifications, reactivate-when-full) unspecified. | Inconsistent state. | S |
| F11 | Minor | Intake-envelope limits (10 files/10MB) are magic numbers in copy, not entitlement config. | Two sources of truth; no per-tier variation. | S |
| F13 | Minor | Naming collision: "plan" = subscription vs "plan" = the document. | Data-model ambiguity. | S |

**Doctrine risks:** DL-L1, DL-L2, DL-L3 all live here, plus "quality-tiering leak" (VM-2 must stay about *ingest capacity*, never read quality — proto copy is correct; preserve it).

### 4.5 Feedback ticketing + readiness survey + trigger + funnel telemetry
**Coverage: almost entirely NET-NEW. The one reuse target — the R1 event pipeline — is real (see §7 correction) but R2's events aren't in the taxonomy, and `TelemetryEvent` is explicitly "not part of the R1 public contract."**

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| FB-G1 | Blocker | Ticket data model / server id authority / status lifecycle beyond "Filed" undefined; proto ids (`DEF-1001`) are in-memory and collide across users/sessions. | Can't build a durable, unique-id ticket table with transitions. | S |
| FB-G2 | Blocker | Delivery to a real tracker (which system, field mapping, auth, retry, status back-sync) unspecified. | Feedback goes nowhere. | O+S |
| FB-G3 | Blocker | Defect free-text **sanitization boundary** not specified/enforced (auto-context is metadata-only, but typed fields ship verbatim). *(= DL-L5)* | "No plan content leaves" is unenforceable as written. | S |
| FB-G4 | Blocker | Boundary invariant (feedback/survey structurally unable to change the read) is behavioral, not architectural. *(= DL-L6)* | A future edit re-introduces a write path. | S |
| FB-G5 | Blocker | PMF readiness-gate computation undefined: who computes the ~40% "very disappointed" bar, over what cohort, window, min-N. | The survey's whole purpose is uncomputable. | O+S |
| FB-G7 | Blocker | Trigger audience "post-activation + engaged" not server-computable, and the activation definition **conflicts** (DL-173 grounding-act vs R1 telemetry "Activated = score_viewed"). | Survey fires to the wrong cohort → biases the PMF gate. | O+S |
| FB-G8 | Blocker | Cross-session trigger state (fire-once-per-user, cooldown, dismissal persistence) unspecified (proto is single-session booleans). | Survey re-nags or never fires; core non-nagging UX unbuildable. | S |
| FB-G6 | Major | CSAT (1–5) trend storage/aggregation/window unspecified. | Trend surface unbuildable. | S |
| FB-G9 | Major | A/B variant assignment/persistence for `_SURVEY_TRIGGER_AB` (no assignment service, no sticky persistence, no event). | Timing A/B can't be run/measured. | S |
| FB-G10 | Major | Grounding-act event stream (confirm/flag/route) not emitted, yet activation depends on it; R1 taxonomy has no such event. *(shared with R2-I5)* | Activation/engagement not server-computable. | S |
| FB-G12 | Minor | De-dup / triage fields (dedup key, component, priority from impact) unspecified. | Ticket queue floods. | S |
| FB-G13 | Minor | Retention/consent policy for feedback/survey free text unspecified. | GDPR-style erasure path missing. | O+S |

**Doctrine risks:** DL-L5 (highest — free-text leak), DL-L6 (structural isolation), FB-G7 activation-definition conflict biases the readiness read, and the readiness metric must be explicitly non-gating and never surfaced back to the user. *(Cross-domain nuance: feedback/survey correctly avoid History, but the adjacent intent-capture `_recordIntent` **does** `pushHist` — decide whether "side channels don't touch History" spans all telemetry or intent is a deliberate exemption, and state it.)*

### 4.6 Collaboration / reports / roll-up / identity / persistence
**Coverage: MIXED — sharing, comments, reports, notifications, and the reviewer-response→evidence seam are COVERED by R1 (build against canon, §6). The external-reviewer *workflow*, the owner glance surfaces, the role model, and outcome-as-container are net-new.**

| ID | Sev | Gap | Why it blocks | O/S |
|---|---|---|---|---|
| R2G1 | Blocker | External-reviewer **scoped-surface** access contract undefined and conflicting: R2 = "one question only"; R1 DL-049 scopes reviewer to the whole MRI/read. | Can't build the scoped read; risk of leaking the plan. | O+S |
| R2G2 | Blocker | Reviewer round-trip workflow (request→deliver→pending→withdraw) declared "commodity" in R1, uncontracted; R2 needs it real. | No contract for how a route is created/delivered/tracked. | S |
| R2G3 | Blocker | Owner roll-up + grounding-map **server-side aggregation reads** undefined (no endpoint, no role-scoped projection, no per-detail provenance read). | R2's flagship read surfaces can't be wired. | S |
| R2G4 | Blocker | Owner vs delegate-PM role model + access/visibility matrix unspecified (R1 roles = owner/admin/member; no delegate-PM; DL-173 defines only a metric). | Role-scoped surfaces + scoped reviewer un-buildable. | O+S |
| R2G5 | Major | Outcome→plan container hierarchy + non-destructive archive/reactivate net-new & conflicts with R1 flat Project + terminal archive. *(shared with F3/F4)* | Foundational unit of persistence undefined. | O+S |
| R2G6 | Major | PM-tool export contracts (Asana / MS Project / Smartsheet) don't exist (auth, mapping, direction, idempotency); proto = toast stubs. | Named export deliverable unbuildable. | O+S |
| R2G7 | Major | Attestation-ledger reversibility (withdraw/rollback) has no contract. *(= R2-I4)* | Ledger can't honor Withdraw; roll-up can't clear a withdrawn route. | S |
| R2G8 | Major | R2 awareness feed broader than R1 (routed-response notification, salience/quiet-mode filtering per DL-166, drift alerts) uncontracted. | R1 emits-on-everything; R2 salience rule missing. | O+S |
| R2G9 | Minor | Share-the-**read** as a frozen revocable snapshot + stale-read labelling (R1 shares a live object; only reports are frozen). | Viewer sees a moving/silently-stale target. | S |
| R2G10 | Minor | k-factor invite delivery/persistence (OSLO drafts, user sends, nothing auto-sent). | Invite is ephemeral. | S |
| R2G11 | Minor | Report recipient-tailoring enum + auto-supersession trigger (R1 State Open-Q7 unresolved). | Recipient variants/supersession undefined. | S |

**Doctrine risks:** DL-L8 ("shown not enforced" vs reviewer scope — must hard-enforce the scope, 403 otherwise); roll-up/grounding-map must be read-only Disclose objects that **cannot emit a write** (add the QA negative); DL-L2 (Viewers/reviewers never metered) assumed by these surfaces; "comment never grounds" must hold when comments enter the awareness feed.

---

## 5. Consolidated resolve-first sequence (the critical path into product-grill)

Ordered so each step unblocks the next. Items marked **[OWNER]** need your decision; **[SPEC]** is authoring work the grill can drive.

1. **[OWNER] Resolve the two-lineage divergence (§1).** Declare the AI-first prototype the canonical source; re-adjudicate DL-164…197 against it (carry / supersede / renumber). *Nothing else is estimable until this is done.*
2. **[OWNER] Ratify the unit-of-persistence: Outcome-above-Plan** (F3/R2G5), reversing the R1 "Intend deferred / outcome=Canonical-Fact" call. Everything (metering, archive, sharing scope, roll-up) hangs off this.
3. **[OWNER] Ratify enforcement-mode = observe for Alpha** and mark R1's 422/429 gating + checkout funnel superseded (F1/F2 = DL-L1). The single highest-risk build error.
4. **[OWNER] Ratify the integrity model** (OI-1/OI-3/OI-5): the `min()` pillar gate as a construct that supersedes IR-4/IR-8 for the composite; whether Adaptability is a new dimension or a Feasibility property; whether Grounding = re-homed Reliability.
5. **[OWNER] Ratify one issue lifecycle** (R2-I1/R2-I2): pick the phased `Inferred→Settled→(needs-a-fix)→Resolved` model or the proto 5-state, and land the D088 amendment.
6. **[OWNER] Reconcile the activation definition** (FB-G7/R2-I5): grounding-act (DL-173) vs telemetry "score_viewed," and confirm N=2 as the unlock threshold.
7. **[SPEC] Author the five R2 delta contracts** (§2) over the resolved decisions: State, Event, Data/Object, API, Integration Map — reusing R1 where §6 says so.
8. **[SPEC] Encode the doctrine landmines (§3) as tests/lints** (enforcement-mode, never-metered exemptions, freeze presentation-only, sanitization boundary, feedback isolation, integrity maturity-framing, reviewer-scope enforcement, activation-survives-withdraw).

---

## 6. What is genuinely COVERED by R1 — build against canon, do NOT re-spec

To keep the grill focused on the real delta (and to avoid re-litigating settled work):

- **Sharing mechanics** — `SharedArtifact`, `POST /shares` (view=Viewer / comment=Collaborator), `:revoke`, lifecycle + events; tenant isolation via the share.
- **Comments + @mentions + "a comment never grounds the read"** — `Comment`/`Mention` objects, endpoints, events; the evidence/comment boundary is contracted at Critical depth in WAVE_I with QA negatives. DL-170 only makes the *choice* legible.
- **Reviewer-response → evidence seam** — `StakeholderResponse` admitted as evidence-attested, triggers Deep Pass; append-only attribution; `reviewer→user` promotion (DL-049). *(The seam is covered; the request/scoped-read *workflow* around it is not — R2G1/R2G2.)*
- **Reports generation** — `Report` + immutable `ReportSnapshot`, endpoints, states, events. *(Recipient-tailoring enum + PM-tool export are the gaps — R2G11/R2G6.)*
- **Notification core + mark-read/dismiss** — `Notification`, `GET /notifications`, states, `:view`/`:dismiss`. *(R2 salience/quiet-mode + routed-response source are the gaps — R2G8.)*
- **The recompute/stale backbone (principle)** — event-driven coalesced recompute, single-active-per-project, `no-change → no-reanalysis`, supersession/append-only history. *(R2's faster grounding-act batch window + fast/deep choice are the gaps — R2-RE-1/2.)*
- **Attestation ledger primitives** — Cognition History Record, User Acceptance Record, evidence/OSLO/user-attested sub-classes, append-only immutability. *(R2's issue objects + basis enum + reversal record must be built *on* these — R2-I3/I4.)*
- **The telemetry event envelope + pipeline** — typed envelope, `is_internal`, dual-write to `analytics_events`, PostHog/ClickHouse, internal-account exclusion, identity stitching. *(R2's new events + the ingestion contract are the gaps — FB-G10.)*

---

## 7. Corrections caught in verification (false positives removed)

Rigor requires reporting what did **not** survive checking:

- **The successor telemetry spec EXISTS.** One audit flagged `OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1` (the doc that supersedes the R1 telemetry/analytics spec) as "absent from the KB." It is present at `30_engineering/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1.md` (~39 KB); it simply wasn't staged for that subagent. **Downgrade:** not a gap — just re-anchor backend-caps #15/#17/#18 to this successor as the reuse target.
- **"DL-173 doesn't exist in canon" is expected, not a defect.** DL-172 (freemium) and DL-173 (owner-activation) are ratified but deliberately **staged in `release-2/` and withheld from `main`** until R1 graduation. Their absence from the canon KB is the graduation-gate working as intended. *However*, this feeds the real §1 finding: they collide on number with the Lineage-A DL-172/173.
- **`.dim` / `exposure` hits in the prototype are incidental.** The 50 `.dim` and 5 `exposure` matches are CSS/`_score`-proxy usages, not the DL-196 issue-layer `dim`/`exposure` fields — the issue-layer-specific identifiers are all 0 (confirming §1).

---

## 8. Raw material for product-grill vertical slices

The domain audits proposed these slice seeds (input for the grill, not the formal slices):

- **Integrity model** — slice each pillar separately (Viability = partial-inherits-R1; Grounding = mapping-undefined; Adaptability = fully net-new); make the `min()`-gate + Non-Collapse reconciliation its own decision first.
- **Issue lifecycle & resolution** — one slice (state set + phased-resolution + re-read-only invariant are inseparable). Grill question: *"A PM confirms a load-bearing assumption; the plan is genuinely infeasible — what state is the issue in, and what does the ledger say?"* (proto answers "Resolved"; the DL answers "Settled — needs a fix").
- **Grounding act & attestation ledger** — extend R1's Cognition/User-Acceptance/StakeholderResponse primitives (basis enum, reversal record, flag-as-attestation, routed↔CRR binding).
- **The grounding-act batch** — the act→enqueue→stale→batch-re-read→resolve loop (the honesty backbone); resolves G7 + the two window classes.
- **First-run freeze→unlock** — durable `firstRun`/`confirmCount`/`workspace_unlocked`; grill: *"Is unlock latched or live?"* (proto re-freezes on withdraw).
- **Entitlement & enforcement-mode** — `Entitlement` object + `observe/enforce`; acceptance test: 2nd-outcome moment returns allow + emits one signal, never 422.
- **Outcome as the unit** — `Outcome` entity + Workspace/Plan/Outcome cardinality + active-slot; reconcile R1 "Intend do-not-add."
- **Archive/reactivate lifecycle** — reversible, self-service, record-viewable; test: archive → record still readable; reactivate → restored; nothing deleted.
- **Intent-signal stream** — schema on the R1 envelope, every-branch `chosen_path`, re-derived Alpha demand metric.
- **Feedback ticketing** — ticket schema + id authority + status lifecycle + tracker delivery + the sanitization boundary + isolated-store constraint. (Owner: which tracker.)
- **Readiness survey storage + analytics** — `SurveyResponse` + server-computed readiness metric (cohort/window/min-N) + CSAT trend; non-gating.
- **Trigger/targeting engine** — the deepest slice; gated on ratifying activation (DL-173) + emitting the grounding-act event; durable per-user eligibility + sticky A/B.
- **Scoped reviewer round-trip** — R2G1+R2G2+R2G7+R2G8 on R2G4; the WAVE_I evidence seam is the only pre-contracted piece.
- **Owner glance** — roll-up + grounding map as read-only Disclose projections over #2/#3/#7 with a pinned no-write negative.
- **Handoff/export** — separate the read→PDF (`Report`) from the plan-structure→PM-tool (integration).
- **Doctrine guardrails as tests** — port the `_S10` guards into real build assertions (never-metered exemptions, neutral-copy lint, feedback isolation).

---

*Prepared for the R2 pre-handoff gate. The developer-facing handoff packet should be assembled AFTER the §5 resolve-first items are decided — building it now would index a source of truth that is still ambiguous (§1).*

# Demo-vs-Production Enforcement Audit — R2 prototypes

**Date:** 2026-08-09 · **Author:** AI (analysis only — no canon ratified) · **Scope:** `oslo-prototype-r2.html` + `onboarding-arc-prototype.html`
**Standard being audited:** *Any behavior, value, or config that is demo-specific must have a clearly-defined production behavior in the build design spec, so demo behavior never transfers into the real build.*
**Governance:** This is a Review under Framework 001. AI analyzes and recommends only; the owner ratifies. Gaps are **escalated, not resolved** (Anti-Assumption Protocol).

---

## Summary / Status

**Status: PARTIALLY ENFORCED — strong for backend *behaviors*, weak for demo *values* and not machine-gated.**

The enforcement mechanism already exists and is good: the **standing rule "prototype simulation ⇒ backend obligation"** plus the **`OSLO_BACKEND_CAPABILITIES.md` register (#1–22)**, which pairs every simulated behavior with a *"Prototype stub"* and a *"R2 backend must provide"* spec. Every major simulated **behavior** in the prototype maps to a register entry (coverage matrix below). That part of the standard is met.

Three things keep it from being fully enforced:
1. **Demo-tuned VALUES (timings, thresholds, numbers) are not systematically specified for production.** The register documents behaviors, not the specific numeric values the demo hard-codes — including one (`PASS_MS`) tied to a user-facing promise.
2. **Recently-added prompt-lifecycle behaviors are not yet registered**, so the standing rule has drifted out of sync.
3. **Enforcement is by convention, not a gate.** Unlike the new `noJargon` self-check, nothing mechanically fails the build when a demo stub lacks a production spec — it relies on the author remembering (and on audits like this).

---

## Coverage matrix — demo behavior → production spec

Every demo-specific **behavior** found in the prototype maps to a registered obligation:

| Demo behavior in prototype | Register entry |
|---|---|
| Re-analysis via `setTimeout` (fake per-fix re-read) | #1 |
| `HISTORY[]` / item-state / `attestedBy` (attestation) | #2 |
| "Ask for evidence" + "Simulate reply (demo)" routing | #3 |
| `commentOnIssue()` → local `COMMENTS[]` | #4 |
| Hardcoded `CLARIFY[key]` clarification Q&A | #5 |
| `_applyPlanChange()` mutating in-memory arrays | #6 |
| `viaLevel/grdLevel/adaLevel` counts + 4-level bands | #7 |
| `CHK_PROPOSALS[]` hardcoded checkpoints | #8 |
| Share door "revocable snapshot" (no real share) | #9 |
| `_narrativeProjection()` / roll-up / **simulated export** | #10 (+ `OSLO_EXPORT_OBJECTIVE_AUDIT`) |
| Single hardcoded project; state resets on reload | #11 |
| `roleType` var; **simulated sign-in / credentials** (`act-sub` "no real sign-in") | #12 |
| Bell/Awareness from local `HISTORY[]` | #13 |
| `sendChat`→`_osloExec` regex intent parser | #14 (deferred) |
| `_isActivated/_isEngaged` derived in-page; `_SURVEY_TRIGGER_AB` | #15 |
| Freemium: VM intent moments, `_INTENT_LOG`, `_COMMITMENT_LOG`, **stubbed hosted checkout (Stripe-style)**, `_switchPlan` stub, 10-file/10-MB envelope | #16 |
| `_FEEDBACK_LOG` ticketing | #17 |
| `_SURVEY_LOG` readiness survey + trigger | #18 |
| Hard-coded sponsor trade-off (`sponsor-tradeoff`) | #19 |
| Accepted-exposure register (`_acceptExposure`) | #20 |
| Arc: progressive analysis stream + `analysis-complete` | #21 |
| Arc: plan ingestion → typed tree + node-level finding provenance | #22 |
| **Sample dataset itself** (`ARTIFACTS`, `ISSUES`, `EXWBS`, `_PLANS`, DevNorth 2026) | #22 (extraction) + #11 (persistence) |

**Finding F1 (positive):** the register is comprehensive and the standing rule is explicit. No simulated *behavior* was found that is entirely absent from the build spec. Two are only *implicitly* covered and should be named explicitly (see G5).

---

## Gaps (escalated to owner — not resolved here)

### G1 — Demo-tuned VALUES have no defined production source *(highest-priority gap)*
The register specifies behaviors but not the **numeric values** the demo hard-codes. Each needs either a production value or an explicit "owner-config, TBD" designation, so a demo number never silently becomes the shipped number. Inventory:

| Constant (file) | Demo value | Production concern |
|---|---|---|
| `PASS_MS` (arc) | 60000 | **Tied to a user-facing promise** ("usually under a minute"). Production analysis SLA must actually meet this or the copy must change. |
| `GUIDED_MIN` (arc) | 47500 | Guided-arc floor; pure presentation, but total run ≈69s **exceeds** the 60s promise — reconcile. |
| `EV_DELAY` (arc) | outcome 8.4s / plan 13s / inference 20s / pillars 30s | Fake fast-pass event timings; real backend emits these when data is actually ready (#21). Demo values must not be read as SLAs. |
| `STEP` (arc ingest) | 1200ms | Cosmetic pacing of the 8 analysis steps. |
| `SV_NUDGE_TTL / SNOOZE / MAX` | 45s / 120s / 3 | Prompt-retirement cadence; **wall-clock** in demo — production should meter active engagement + persist cross-session. Owner-config. |
| `COACH_MAX` | 2 | Coach auto-retire threshold; owner-config; session-scoped in demo. |
| `_isEngaged` threshold | confirmCount ≥ 3 (≥4 in `delayed` A/B) | **Demo proxy** for "value experienced." Real signal = durable per-user engagement (see G2). |
| freeze/activation gate | `confirmCount < 2` | Product number (2 calls unlock). Confirm it's the ratified value, not a demo pick. |
| `REANALYSIS_DEBOUNCE / REANALYSIS_MS / IMMEDIATE_THRESHOLD` | 1500 / 900 / 5000 ms | Perceived-pace fakes for #1; real thresholds are "deferred (§S)" per #1 — confirm they land in the reanalysis-engine spec. |
| Intake envelope | 10 files / 10 MB (Free) | Freemium limit (#16) — confirm ratified vs demo placeholder. |
| Stubbed prices / tiers | (Basic $29/mo etc. where shown) | Owner-ratified per DR-7; confirm no demo-only numbers leak. |

**Recommendation:** add a **"Demo values → production sourcing" table to the build spec** (either a section in `OSLO_BACKEND_CAPABILITIES.md` or a dedicated `DEMO_CONFIG_REGISTER.md`), one row per constant: demo value · is-it-owner-config-or-derived · production source/owner decision · linked capability. Route the open numbers through the BACKLOG "Owner-Open Decisions."

### G2 — The engagement / "onboarded" signal is a demo proxy that now gates real UX
`firstRun` resets on reload and stands in for "value experienced" (`_isEngaged`). This proxy now **gates prompt retirement** (tour chip hides when engaged; survey eligibility; coach). Touched by #11 (persistence) and #15 (funnel) but **not named as its own obligation.** Production needs a **durable, per-user engagement/onboarded signal** so prompts retire correctly and a returning engaged user never re-sees first-run prompts.
**Recommendation:** add an explicit line (under #15 or a new sub-entry) naming the per-user engagement/onboarded signal + cross-session prompt-seen/retired state as an owed capability.

### G3 — Newly-added prompt-lifecycle behaviors are not yet in the register *(standing-rule drift)*
Added 2026-08-09, all demo-timed/session-scoped, **none registered**:
- Readiness-survey **timeout → re-offer → cap** cycle (`SV_NUDGE_*`, wall-clock).
- Pillar-coach **auto-retire after `COACH_MAX` distinct cards** (session set `_coachCards`).
- Rail tour chip **hides once `_isEngaged()`**.
**Recommendation:** register them (see the draft register entry #23 added alongside this audit) — real engagement metering, cross-session persistence of "seen/retired," owner-config cadence, and the doctrine that no prompt persists to blindness.

### G4 — Enforcement is by convention, not a gate
The register + standing rule depend on the author remembering to add entries; nothing fails the build if a stub is unregistered. Contrast the new `noJargon` self-check, which is a hard `_S10` gate.
**Recommendation (owner decision):** make demo↔spec traceability machine-checkable. Lightest option: adopt a convention that **every demo stub carries a tag** in a comment, e.g. `/* SIM:#16 */` (or `/* SIM:UNREGISTERED */`), and add an `_S10` check that scans for `SIM:` tags lacking a matching capability number — the same pattern as `noJargon`. This turns "confirm this is enforced" from an audit into a build gate.

### G5 — Two behaviors are only implicitly covered — name them
- **Stubbed hosted checkout / commit-to-pay (Stripe-style)** — #16 covers tiering/entitlement/intent but not the *payment/checkout* capability itself. Add an explicit sub-line.
- **Simulated activation email + credential setup** (`im-sim` "simulated email", `act-sub` "no real sign-in") — #12 covers auth broadly; name the invite→email→credential onboarding flow explicitly.

---

## Review outputs (Framework 001)

- **Findings:** Every simulated *behavior* is registered (#1–22) under an explicit standing rule — the behavioral half of the standard is met. The *values* half is not: demo-tuned numbers/timings lack production sourcing (G1), the engagement proxy that gates UX is unspecified (G2), three new lifecycle behaviors are unregistered (G3).
- **Concerns:** (a) `PASS_MS`/run-time vs the "usually under a minute" promise is a live inconsistency, not just a config gap. (b) Enforcement is disciplinary, not gated (G4) — the register can silently drift, as G3 already shows.
- **Dependencies:** G2 depends on #11 (persistence) + #15 (telemetry). G1's SLA rows depend on #21 (analysis stream) and #1 (reanalysis engine). G4 is independent (tooling).
- **Recommendation:** (1) Add a **Demo-Config register** (G1). (2) Register #23 for the prompt-lifecycle behaviors (G3 — drafted). (3) Name G2/G5 obligations explicitly. (4) Owner to decide on the `SIM:` tag + `_S10` gate (G4). (5) Reconcile the run-time vs "under a minute" promise.
- **Status:** Enforcement **partially** in place. Behavioral coverage: complete. Value/timing coverage + machine-gating: **open — owner decisions required.**

## Owner-open decisions to ratify

**★ RATIFICATION LOG — all resolved 2026-08-09 (owner):** (1) "under a minute" = *analysis completion*; SLA = typical/p50 ≈45s, large uploads may exceed; walkthrough length decoupled. (2) Freeze gate = default **2**, owner-config; a "call" = confirm/flag/route. (3) **Engaged = a milestone** (≥½ the load-bearing read grounded OR integrity up ≥1 band, config), durable per-user cross-session + an **onboarded** flag — not a click count. (4) Intake envelope: per canon = content-metered ~50k-word config (10/10 = upload rails); exact per-tier words deferred to config. (5) Prompt cadences: survey retirement is **event/session-based** (not wall-clock), coach = per-card count; numbers = owner-config placeholders. (6) **Keep the SIM-tag gate** permanently + full tagging (both prototypes). Details in `DEMO_CONFIG_REGISTER.md`. Below is the original escalation list, now resolved.


1. Approve a **Demo-Config register** and populate production sourcing for each constant in G1 (which are owner-config vs derived vs SLA).
2. Ratify or correct the freeze gate (`confirmCount<2`), engagement threshold (≥3), and envelope (10/10) as production values vs placeholders.
3. Reconcile the arc run-time (~69s) with the "usually under a minute" analysis promise (`PASS_MS`).
4. Decide whether to adopt the `SIM:` tag + `_S10` gate to make demo↔spec traceability enforced, not conventional.
5. Ratify the drafted register entry #23 (prompt-lifecycle / engagement-gating).

# R2 Delta — Vertical Slice Map (for sign-off, 2026-08-06)

**Grill phase:** 3 (slice-map). **Scope:** the R2 *delta* on top of the signed-off R1 slices (01–10) — only the net-new / changed behavior of the AI-first reimagining. Single source of truth: DR-1 prototype + the ratified re-adjudication worksheet + DL-200–205 / DR-1–7.
**How to read each slice:** *Features/actors* · *Carries* (ratified decisions it implements) · *Contracts* (which of the five delta artifacts it feeds) · *Reuse* (R1 canon per audit §6, not re-spec'd).
**Sequencing note:** Slice 1 is the foundation every read renders from (State-1 Phase A) — recommended first; 6–9 are additive.

---

## Slice 1 — Outcome-Integrity engine (the three-pillar model) · **FOUNDATION**
- **Features/actors:** three pillars — Viability (=CAF composite), Grounding, Adaptability — resolved through the exposure-gated **issue layer**; weakest-gates `min()`; the decomposed integrity indicator + named limiting pillar. Actors: System/AI.
- **Carries:** DL-193 (priority re-anchor), DL-194 State-1 (moment-in-time integrity), DL-195 (Adaptability = checkpoint-coverage v1), DL-196 (issue layer `{dim,dims,ftype,sec,sev,status}`), DL-197 (false-confidence `ISS-FC-<art>`), band labels **Fragile→Sound**, tech-debt constraints (bands normalize to plan size; Viability from real per-issue weakness reduction; flag credits Grounding never Viability).
- **Contracts:** Data/Object (Issue, Pillar, Integrity), computation spec. **Reuse:** R1 CAF/Reliability primitives.

## Slice 2 — Issue lifecycle & grounding acts (attestation)
- **Features/actors:** lifecycle **Inferred→Settled→"needs a fix"→Resolved** (only re-analysis resolves); grounding acts confirm/flag/fix/route; the attestation ledger (who/basis/attributed). Actors: User, Reviewer, System.
- **Carries:** DR-5 phased resolution + D088 amendment, DL-204 needs-a-fix fork, BASIS taxonomy, withdraw/reversibility on an append-only ledger.
- **Contracts:** State, Event (grounding-act), Data (attestation ledger). **Reuse:** R1 Cognition/User-Acceptance/StakeholderResponse primitives.

## Slice 3 — Reanalysis engine + first-run freeze/unlock
- **Features/actors:** two-pass — **Fast Pass <60s P95 on the critical path**, Deep Pass non-blocking + supersedes; grounding-act **batch** (debounce/coalesce/cooldown); STALE contract; the **Fast-Pass output contract** (outcomes + all three pillar initial values); freeze→unlock **latched**; attributed "your read moved" notification. Actors: System/AI.
- **Carries:** ingestion-latency ratifications (≤60s NFR, per-run token caps + degrade, content-metered limits), DL-188 unlock→engaged, unlock-latch tech-debt fix, causal-clarity notification.
- **Contracts:** Event (recompute), State (freshness/freeze), API (analysis-runs Fast/Deep). **Reuse:** R1 recompute backbone + telemetry envelope.

## Slice 4 — Freemium: entitlement, commitment gate, outcome-unit, archive
- **Features/actors:** **Outcome** as the metered unit; **enforce via commitment gate** (block→price→checkout→grant); ingest envelope; reversible **archive/reactivate**; intent-signal stream. Actors: User, System, Billing.
- **Carries:** DL-201 (outcome unit), DL-202/DR-3 (commitment gate — supersedes observe), DR-7 (Basic $29 / Pro provisional), DL-198 (freemium value moments, renumbered), never-metered exemptions (record/reviewer/Viewers).
- **Contracts:** Data (Entitlement/Outcome/Plan), API (checkout/grant/archive), Event (intent signal). **Reuse:** R1 422/429 gating apparatus (now re-aligned, not superseded).

## Slice 5 — Multi-outcome read & deferred disclosure
- **Features/actors:** Fast-Pass multi-outcome NLU; primary/secondary **ranking + rationale**; **deferred disclosure** (primary-only reveal → post-engagement disclosure framed as engagement + multi-outcome upsell). Actors: User, AI.
- **Carries:** the 2026-08-06 funnel decision (primary-only reveal, protect activation; held outcomes as post-activation engagement/upsell moment), DL-198 multi-outcome gate.
- **Contracts:** Data (Outcome cardinality), Event (disclosure). **Reuse:** —.

## Slice 6 — Collaboration: scoped reviewer round-trip, roll-up, grounding map, share
- **Features/actors:** reviewer **request→deliver→pending→respond→evidence** (external **scoped**, hard-enforced 403; collaborator full read); owner **roll-up** + **grounding map** (read-only projections, no-write); redesigned **share** (view-only snapshot). Actors: Owner, Delegate-PM, Reviewer(scoped/collaborator), Viewer.
- **Carries:** DL-168 (evidence-forward ask), DL-169 (k-factor invite), DL-166 (quiet mode/salience), roll-up/grounding-map surfaces, share-panel redesign, role model (owner/delegate/external).
- **Contracts:** API (review-requests/roll-up reads), access model, Event (routed-response). **Reuse:** R1 SharedArtifact/Comment/StakeholderResponse/Notification.

## Slice 7 — Reports & export / hand-off
- **Features/actors:** the three generated reports (Outcome Readiness · Assumptions & Evidence · Decision Record) + authored Briefing; **export engine** (PDF package / Asana-PM-tool / clipboard) with the **D153 advisory-disclaimer** cover; report scheduling. Actors: User, System.
- **Carries:** reports-tabs, export-flow (openExport), D153 disclaimer, DL-144 depth+export.
- **Contracts:** API (export/hand-off, PM-tool mapping), Data. **Reuse:** R1 Report/ReportSnapshot.

## Slice 8 — Feedback, survey & funnel telemetry
- **Features/actors:** feedback **ticketing** (+ sanitization boundary + structural isolation from the read); PMF/readiness **survey** + **trigger/targeting** engine + A/B; activation/engagement/funnel events. Actors: User, System.
- **Carries:** DL-162 (funnel telemetry), the feedback/survey doctrine (side channels never touch the read), DR-6 (Activated = 2nd act) as the funnel definition.
- **Contracts:** Event, Data (Ticket/SurveyResponse). **Reuse:** R1 Observability/telemetry envelope.

## Slice 9 — Doctrine guardrails as acceptance tests · **CROSS-CUTTING**
- **Features/actors:** port the 58 `_S10` guards + doctrine invariants into the real acceptance suite. Actors: System/QA.
- **Carries:** never-metered exemptions, feedback sanitization + isolation, activation-survives-withdraw, unlock-latch, flag≠Viability, enforce-mode, maturity-not-forecast, external-reviewer-scope-enforced.
- **Contracts:** the keystone **FE↔BE Integration Map** binds every dynamic element on Slices 1–8's surfaces to Read/Write/Event contracts; this slice makes the invariants testable.

---

## Approval ask

Do you approve this R2 delta slice map (9 fat slices) as the scope for the build design?

**Recommended answer:** *Yes — approve, and start with Slice 1 (Outcome-Integrity engine = State-1 Phase A, the foundation every read renders from).*

*Override only specific slices if you'd cut, merge, or reorder any; all others are accepted. On approval I author Slice 1's decision packet + contract bindings for sign-off, then proceed slice-by-slice.*

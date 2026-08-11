# R2 Build Readiness — closure map (2026-08-06)

**Purpose:** the finite, ordered list of what remains between today's state and an unambiguous FE+BE build design for R2. Every item is tagged **[OWNER]** (a decision only Idris can make), **[AUTHOR]** (spec-writing I can do now that decisions are settled), or **[BUILD]** (dev-team engineering). The goal is to spend owner time only on the [OWNER] items and parallelize the rest.

---

## 1. Done — the finish line is closer than it looks
- **Decision state largely settled:** resolve-first DL-200–205 + DR-7, plus the nine open questions closed 2026-08-06 (Fast-Pass NFR ≤60s P95, ingest limits, Adaptability v1 = checkpoint coverage, band labels = Fragile→Sound, reframe scope 2a, Pro price provisional, DL-split, enforce = DL-202 final, canon-main landing deferred to R1 graduation).
- **Lineage canonicity resolved:** the AI-first prototype is the go-forward source of truth (Lineage B); DL-164…197 re-adjudicated in `R2_DL_READJUDICATION_WORKSHEET.md`. *(Note: this settled which source governs — it did NOT build the DL-196/197 issue layer; that's item 3.4 below.)*
- **Prototype refinements shipped + green (58/58):** center-rail scroll, chat composer border + placeholder, menu removal, Share panel redesign, DL-204 "Settled — needs a fix" fork.
- **Prototype honesty debt:** items 1 (flag≠Viability) and 5 (latched unlock) fixed; items 2/3/4 dispositioned to Phase A. See `OSLO_R2_PROTOTYPE_TECHDEBT_DISPOSITIONS_2026-08-06.md`.
- **Backend gap register exists:** `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md` (per-domain blockers/majors + slice seeds).
- **Latency + limits contract:** `OSLO_R2_INGESTION_LATENCY_AND_LIMIT_ENFORCEMENT_INSTRUCTIONS_2026-08-05.md` (two-pass, ratified caps, Fast-Pass output contract L1a).
- **FE build plan exists:** `R2_STATE1_BUILD_PLAN.md` (Phase A–D).

## 2. [OWNER] — the short list that needs you (do these first; they unblock authoring)
- **2.1 Confirm the two-lineage reconciliation is formally CLOSED** — that the re-adjudication worksheet is final and no DL-164…197 decision is still contested. One confirmation; it certifies a single source of truth for every downstream contract. *(Likely a yes.)*
- **2.2 Education-journey "held outcomes" surfacing** — the open design question: should the first-run reveal *mention* that OSLO also found other outcomes (held for later), or stay primary-only with disclosure deferred entirely to post-engagement? Affects the multi-outcome UX contract.
- **2.3 Any residual product calls** the authoring surfaces — e.g. which external tracker for feedback (FB-G2), report recipient-tailoring enum. These can be flagged as "author with a placeholder, owner ratifies" rather than blocking.

*(Pro price, canon-main landing, and the full DL-195 Adaptability model are already decided as deferred — not on the critical path.)*

## 3. [AUTHOR] — the bulk, unblocked once §2 is confirmed (I can produce these)
The R1 "underdefined" complaint was solved by five contract artifacts; R2's delta needs the same. Author over the settled decisions, reusing R1 where the audit §6 says (sharing, comments, reports, notifications, telemetry envelope, attestation primitives, recompute backbone):
- **3.1 R2 State Model** — issue lifecycle (Inferred→Settled→needs-a-fix→Resolved, DL-204), freeze/unlock latch, archive/reactivate, ticket, survey-eligibility as transitions.
- **3.2 R2 Event Model** — grounding-act / intent-signal / feedback / survey / activation events.
- **3.3 R2 API Contract** — outcomes, archive/reactivate, review-requests, roll-up, feedback, survey, export/hand-off, commitment-gate/entitlement.
- **3.4 R2 Data/Object Model** — Outcome (metered unit), Plan, Entitlement, Issue (with dim/ftype/severity for the DL-196/197 layer), Ticket, SurveyResponse + cardinality.
- **3.5 FE↔BE Integration Map (the keystone)** — bind every dynamic element on the new surfaces (integrity indicator, needs-a-fix folder, reviewer round-trip, export modal, share panel, roll-up, grounding map, feedback/survey, multi-outcome disclosure) to Read/Write/Event contracts.
- **3.6 Fast-Pass output contract** — formalize L1a: Fast Pass emits outcomes (primary confirm-ready + secondaries) + all three pillar initial values within the ≤60s gate.
- **3.7 Guardrails → tests plan** — port the 58 `_S10` guards + the doctrine invariants (never-metered exemptions, feedback sanitization, activation-survives-withdraw, flag≠Viability, enforce-mode) into real build assertions.

## 4. [BUILD] — dev-team engineering (runs against the §3 contracts)
- **4.1 State-1 Phase A** — the three-pillar integrity engine + DL-196/197 issue layer, built into the prototype first, then the prototype **frozen** as the FE reference. Absorbs tech-debt items 2/3/4. (Sequenced in the build plan.)
- **4.2 The real backends** — per the §3 contracts (analysis two-pass engine, entitlement/commitment gate, reviewer round-trip, roll-up aggregation, export/PM-tool connectors, feedback/survey pipeline, persistence/auth).

---

## 5. Recommended closure sequence (fastest wrap-up)
1. **[OWNER, ~1 sitting]** Confirm §2.1 and decide §2.2; let §2.3 be author-with-placeholder. → certifies one source of truth.
2. **[AUTHOR]** Produce §3.1–3.6 as the R2 delta contract set + integration map, reusing R1 per audit §6. Assemble into the **developer handoff packet** — this *is* the unambiguous build design.
3. **[BUILD, parallel]** Dev team starts §4.1 Phase A into the prototype and freezes it; §3.7 guards become the acceptance suite.
4. **[BUILD]** §4.2 real backends against the contracts.

**Net:** your remaining time is essentially §2 (a handful of decisions). The five contracts + integration map (§3) are the deliverable I can produce now; Phase A + backends (§4) are engineering. Once §2 is confirmed I can begin §3 immediately.

*Prepared 2026-08-06. This map supersedes the "assemble the packet later" hold — decision state is now settled enough to author.*

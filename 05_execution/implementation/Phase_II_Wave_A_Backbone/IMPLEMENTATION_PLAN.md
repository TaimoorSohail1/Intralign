# Phase II — Wave A: Backbone (Perceive · Retain · Recompute)

**Sequence:** After Phase I. The spine every later phase depends on. · **Status:** Not started · **Owner gate:** required before Phase III.
**Contracts:** `IC/QA/OBS-WA-00R`, `IC/QA/OBS-WA-001`, `IC/QA/OBS-WA-002` (`03_architecture/contracts/WAVE_A_*`).

## Goal
Build the ingestion → canonical-retention → recompute spine: artifacts come in (integrity-gated), become attested canonical records, and a recompute can re-run the pipeline appending history. This is the foundation the understanding/advisory/disclose waves all sit on.

## Scope & build order (within the phase)
1. **`IC-WA-00R` — Recompute & Stale Backbone (Act/Adapt)** — build **first**: recompute triggers; re-run Retain→Infer→Evaluate→Advise; **append a `CognitionHistoryRecord` per emission, never overwrite**; last-known-good on failure.
2. **`IC-WA-001` — Artifact Intake (Perceive)** — integrity-gated admission (no Authority step); upload ≠ canonical; provenance; idempotency; Promotion-Candidate → Attested handoff to Retain; user-acceptance capture input for Wave U.
3. **`IC-WA-002` — Canonical Knowledge Retention (Retain)** — `AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`; Canonical = Attested; persistence ≠ canonicalization; append-only.

## Depends on
Phase I (stores, schema, CI).

## Expected outcomes (definition of done)
- ✅ An artifact can be ingested; it is **not** canonical on upload; provenance + identity recorded.
- ✅ A promotion candidate is handed to Retain and stored as an **Attested Assertion** (attributed + re-derivable).
- ✅ Re-ingesting the same artifact is **idempotent** (no duplicate canonical record).
- ✅ A recompute **appends** a new `CognitionHistoryRecord`; the prior record is unchanged and still queryable (history is append-only).
- ✅ A forced recompute failure leaves the last-known-good projection intact (no canonical loss).
- ✅ Negative tests prove: a Derived value **cannot** be written to the canonical store as Attested; a recompute **cannot** overwrite a CHR.

## Invariants enforced
Canonical = Attested; persistence ≠ canonicalization; **recompute appends, never overwrites**; one producer per output; no Authority.

## Testing focus
Object + Behavior layers: object existence/ownership/lifecycle (Retain); event generation + recompute behavior (00R). **Negative tests are the heart of this phase** — they protect the epistemic boundary.

## Exit gate (owner-approved before Phase III)
Ingest → attested retention → recompute-appends demonstrated end to end, with the append-only and no-Derived-as-Attested invariants proven by passing negative tests.

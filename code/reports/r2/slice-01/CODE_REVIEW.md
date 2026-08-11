# R2 Slice 01 code review

**Run:** 2026-08-11 23:34 PKT
**Verdict:** actionable findings fixed; no unresolved code-level security finding.

## Security and privacy

- Integrity is projected only after the existing authenticated application boundary has returned an actor-authorized project snapshot.
- No new route bypasses workspace/project authorization; unauthorized/not-found behavior remains normalized to 404 at the API boundary.
- The integrity engine is pure domain code and imports no HTTP, SQL, Supabase, or token boundary.
- No raw access, invitation, refresh, or service-role token is persisted or logged.
- Derived checkpoint proposals require cited evidence before they may be marked registered; the model contract rejects fabricated registered checkpoints.

## Data and failure behavior

- The migration expands the existing issue-dimension check to the two authorized peer pillars only: Grounding and Adaptability.
- Persisted snapshots deserialize the new integrity/checkpoint fields with backward-compatible defaults.
- Direct acts and overlay reads do not mutate integrity; reanalysis remains the writer.
- Failed governed nodes preserve the last-good snapshot under the active GT-10 test.
- Size-normalized fractions reject negative or numerator-greater-than-denominator inputs.

## Fixed review findings

1. Grounding initially consumed only explicit assumption rows, contradicting the canonical provenance projection for evidence-cited snapshots. It now consumes the same evidence projection used by the UI and false-confidence detector.
2. Integrity breakdown close behavior lost keyboard focus. The trigger is now retained and restored on Escape/close.

## Complexity and consistency

- The engine is isolated in `analysis/integrity.py`; API models only serialize the domain result.
- Existing CAF details remain available as the Viability drill rather than being duplicated into the peer-pillar engine.
- Canonical terminology is preserved: Outcome Integrity, Viability, Grounding, Adaptability, Issue, From OSLO, moment-in-time.

# R2 Slice 01 code review

**Run:** 2026-08-12 00:17 PKT

**Reviewed implementation commits:** `8b8f702`, `2958c4a`

**Verdict:** actionable findings fixed; no unresolved code-level security finding.

**Current-run note (2026-08-12 05:10 PKT):** no product code changed, so Code Review was not repeated. The mandatory manual gate failed before a browser page attached; the prior implementation review remains the latest code evidence and does not close that manual gate.

**Latest-run note (2026-08-12 08:10 PKT):** no product code changed, so Code Review was not repeated. The mandatory manual gate again failed before a browser page attached; the prior implementation review remains the latest code evidence and does not close that manual gate.

## Security and privacy

- Integrity is projected only after the existing authenticated project snapshot boundary authorizes the actor.
- No new route bypasses workspace/project authorization; unauthorized/not-found behavior remains normalized to 404.
- The integrity engine is pure domain code and imports no HTTP, SQL, Supabase, or token boundary.
- No access, invitation, refresh, or service-role token is persisted or logged.
- Derived checkpoint proposals require cited evidence before registration; the model rejects fabricated registered checkpoints.
- The parity specification uses local seeded fixtures and repository assets only; it adds no production endpoint or credential path.

## Data and failure behavior

- The migration expands issue dimensions only to the two authorized peer pillars: Grounding and Adaptability.
- Persisted snapshots deserialize new integrity/checkpoint fields with backward-compatible defaults.
- Direct acts and overlay reads do not mutate integrity; reanalysis remains the writer.
- Failed governed nodes preserve the last-good snapshot under active `GT-10`.
- Size-normalized fractions reject negative or numerator-greater-than-denominator inputs.

## Fixed findings

1. Grounding consumed only explicit assumption rows instead of canonical provenance counts.
2. Integrity breakdown Escape handling lost focus.
3. The compact masthead omitted the prototype's all-pillar integrity shape; the three band chips now appear at widths where they fit and yield to the full card on smaller screens.
4. The first comparison harness captured a mismatched prototype state. Its fixture now deterministically produces the executable Fragile/Adaptability-gated state before every capture.

## Complexity and consistency

- The engine remains isolated in `analysis/integrity.py`; API models serialize the domain result.
- Existing CAF details remain the Viability drill rather than being duplicated into the peer-pillar engine.
- Canonical terms are preserved: Outcome Integrity, Viability, Grounding, Adaptability, Issue, From OSLO, moment-in-time.

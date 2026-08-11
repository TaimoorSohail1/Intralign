# DL-162 — Funnel telemetry (a durable event stream, not inferred)

- **Date:** (original ruling — off-repo; **owner to confirm**) · **Status:** ⚠️ **RECONSTRUCTION STUB — pending owner verification/ratification** · **Class:** A/B (measurement infrastructure)
- **Framework 001** — AI drafts; only the owner ratifies.

> ⚠️ **This is a back-reconstruction, not the authoritative original.** DL-162 is **referenced** by ratified R2 material but has **no formal record anywhere in this repo** (searched all branches, full history, filesystem — 2026-08-09). The original ruling appears to have been made off-repo and never formalized here. This stub captures only what the downstream references state. **Owner action:** verify + ratify, replace with the authoritative record, or re-cite.

## Reconstructed decision (from downstream references)
**Funnel/activation/engagement is measured as a DURABLE EVENT STREAM — real telemetry, not inferred from state.** From one `grounding_act` event stream the funnel milestones are derived (initiated → activated → engaged), and the stream feeds the readiness gate, the freemium intent signals, and the feedback/survey channels. (This is the decision behind backend capability **#15 — funnel instrumentation / analytics.**)

## Referenced by (evidence this decision exists and is load-bearing)
- **DL-198** *(freemium)* / `OSLO_R2_DELTA_SLICE_MAP` — *"Carries: DL-162 (funnel telemetry) …"*
- `slices/08-feedback-survey-telemetry` — *"Funnel events are a durable event stream feeding the readiness gate, intent signals (#16), and feedback/survey"*; *"Activated = 2nd grounding act (unlock); Engaged = an act past unlock — from one `grounding_act` stream, not the freeze."*

## Relationship
- **Realized by:** capability #15 (durable event telemetry); consumed by #16 (intent signals), #17/#18 (feedback/survey), and the readiness gate.
- **Consistent with:** DR-6 (Activated = 2nd grounding act; Engaged = an act past unlock) — the milestones are computed off this stream.

## Owner action to close
Confirm the reconstructed statement matches the real DL-162 ruling → ratify; or supersede with the authoritative record; or re-cite the referencing docs.

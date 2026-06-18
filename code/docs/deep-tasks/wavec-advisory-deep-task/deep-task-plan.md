# Deep-task plan — Wave C: Advisory (Advise)

Two vertical slices on `feat/phase4-wavec-advisory`. One fresh worker per task, EM review →
fix → verify → approve between tasks. **Coding gated on the Wave B owner exit-gate (PR #39) +
DL-044 per-wave authorization** — these files are planning only.

## Slices

| # | Module | Slice (vertical outcome) | Contract | Depends on |
|---|---|---|---|---|
| 1 | DTM-0014 | **Recommendation + Clarification (core IC-WC-ADVISE):** Recommendation engine (Finding/Issue-anchored, multiple alternatives) + Clarification engine; `Recommendation`/`ClarificationRequest` types; advise stage via `register_stage` + additive `wave_c.py` (A→B→C live); `EVENT_NAMES_WC_ADVISE`; advise LLM routing stage; CHR-per-emission (DTM-0013 model); governance-adjacent negatives | IC/QA/OBS-WC-ADVISE (C0–C3) | Wave B (Findings/Issues) approved; DL-044 gate |
| 2 | DTM-0015 | **SuggestedFix (REC-04) + Validation Recommendation (REC-05):** Advise generates a `SuggestedFix` candidate (Finding-anchored, Derived, CHR-appended) + the Validation recommendation type; `suggested_fix_offered` event; **headline Critical negative: OSLO never autonomously writes a fix** | IC-WC-ADVISE DL-047 additions | DTM-0014 |

## Test strategy

- **Recorded-fixture CI (ADR-0004):** AI (recommendation text) driven by recorded
  model-response fixtures; **zero provider calls in PR CI**; semantic-tier assertions.
- **QA-mapped (`test_c2_*` positive, `test_c2_neg_*`/`test_c3_*` negative):**
  - DTM-0014 positives: Recommendation generated + anchored; Clarification on blocking ambiguity;
    emission appends a CHR; recompute supersedes (prior intact); multiple alternatives coexist;
    both modes + `confidence_stage`.
  - DTM-0014 negatives (the heart of Wave C): **standalone/unanchored Recommendation rejected**;
    **Resolution-Path-as-object rejected**; Advise evaluating/scoring; Advise govern/authorize/
    execute; **Advise self-accepting**; value changed without recompute; history overwrite.
  - DTM-0015 positives: SuggestedFix + Validation generate as Derived, Finding-anchored,
    CHR-appended; application observed as a *user* edit + recompute (not an OSLO write).
  - DTM-0015 negative (Critical): **OSLO autonomously writing/applying a fix** — impossible.
- **Determinism:** AI-text semantic; record-exact emission; ≥90% set overlap on recompute.
- ruff + gate-4 + gate-5 green; the live A→B→C e2e (env-gated) passes; baseline (offline 455 /
  live 523 at the Wave-B head) must not regress.

## Manual checks (EM / owner)

- Live (Supabase up, recorded fixtures): admit evidence → infer → evaluate → **advise** →
  `recommendation` + `clarification` CHR rows persist, each anchored to a Finding/Issue; a
  recompute supersedes with prior CHRs byte-intact.
- Grep/AST: `advise/` exports no evaluate/accept/execute surface; Recommendation carries an
  anchor; no canonical write.

## Done = Wave C complete

Both contracts' C2 positive/negative sets covered; "advise proposes, never disposes" proven by
the negative suite; Resolution-Paths presentation-only proven; SuggestedFix non-autonomous-write
proven; events + two-axis replay present; A→B→C live. **Phase IV candidate-complete for owner
exit-gate review before Phase V (Wave U / Disclose).**

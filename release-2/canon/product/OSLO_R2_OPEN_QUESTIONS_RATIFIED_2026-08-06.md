# R2 — Open Questions Ratified (2026-08-06)

**Owner:** Idris · **Session:** open-question settling, one at a time.
**Purpose:** record the nine open items settled this session, each with rationale, the doc it amends, and follow-up. These carry the same weight as the resolve-first ratifications (DL-200–205); land alongside them per item 9. Kept in `release-2/` (Framework 001).

---

## The nine

**1. Fast-Pass first-read NFR — RATIFIED.** Time-to-First-MRI (Fast Pass) = **≤60s P95 / ~45s target, hard acceptance gate** (D036, was owner-TBD). Measured against the Free envelope + the 150k Fast-Pass token cap. Gates **time-to-first-read only, never completeness** — an over-envelope doc passes by returning a `Provisional` partial read in ≤60s and deferring depth to the non-blocking Deep Pass.
- *Why:* honors the stated 60s bar; the ≈30s in canon is demo pacing, not real analysis; a gate (not a soft target) is warranted because the absence of one is exactly what produced the 6-minute result. Latency-to-first-read is a UX contract, unlike token/monthly budgets (instrument-only until Beta).
- *Amends/updates:* `OSLO_R2_INGESTION_LATENCY_AND_LIMIT_ENFORCEMENT_INSTRUCTIONS_2026-08-05.md` (Rec 0 + status flags updated to RATIFIED).

**2. Ingest boundary — RATIFIED (content-metered + loose file rails).** The real gate is **extracted words vs the Free ~50k envelope + the 150k token cap + degrade-to-fit**. File limits are **loose abuse rails only**, per-tier config: **~10 MB/file · ~10 files · ~25 MB total**. **No page ceiling** (no OCR in R1 — pages aren't content). D033's ~10 MB/~10-files values are thereby set as config, not folklore.
- *Why:* MB is a weak proxy for analysis cost (image-heavy files yield little without OCR); the ratified word envelope + token cap + degrade already govern latency/quality precisely.
- *Amends/updates:* same build doc (E2 + status flags updated to RATIFIED).

**3. Adaptability v1 — RATIFIED (simple checkpoint-coverage).** Ship Adaptability as **checkpoint presence/coverage across workstreams** (ordinal maturity, buildable now); defer the full DL-195 steerability + course-correction model (and its undefined checkpoint-need denominator, audit OI-3) to a later pass that supersedes without changing the pillar's identity. Permitted by DL-203 §2.
- *Build guardrail:* frame as "does the plan have checkpoints to adapt," **never** "the plan will adapt well" — presence ≠ quality.

**4. Integrity band endpoint labels — RATIFIED: Fragile → Sound.** Settles State-1 §2b. Best fit for the weakest-gates `min()` metaphor and dimension-neutral (doesn't misattribute low integrity to any one pillar, as "Unfounded → Well-founded" would to Grounding).
- *Build guardrail:* "Sound" carries a flagged forecast risk — hold it honest with the moment-in-time / ongoing-pending maturity framing (same discipline that keeps Confidence from reading as a forecast).

**5. Reframe scope (2a) — RATIFIED: hero + pill now, deeper surfaces fast-follow within R2.** Phase B reframes only the hero + top-bar pill to Outcome Integrity; the popover, trend, reports, and chat phrasing align in a contained fast-follow inside R2. All six surfaces still ship in R2 — this is ordering, not a cut. Keeps the heavily-guarded hero rework (the build's risk concentration) from fighting six surfaces at once. (Outcome Confidence survives as the **Viability** pillar — already decided.)

**6. Pro pricing — RATIFIED: keep provisional ($79/mo), finalize post-R2.** No R2 build depends on it (every commitment-gate wall points to Basic $29, DR-7); Pro's value-drivers (continuous monitoring, sync) aren't in R2. Finalize $79 vs ~$69 when those capabilities ship. Basic $29/mo (flat, per account) stands.

**7. DL-200–205 — RATIFIED: split into individual DL-2xx files on landing.** Each decision (DL-200 lineage · 201 outcome-unit · 202 commitment-gate · 203 integrity-model · 204 issue-lifecycle · 205 activation) becomes its own canonical file, matching the one-DL-per-file convention so each is independently citable/supersedable. Split happens at landing (see item 9).

**8. Enforcement mode — CONFIRMED FINAL: enforce via commitment gate (DR-3/DL-202).** The stale standing-constraints line "enforcement-mode = observe" in `R2_RESOLVE_FIRST_DECISION_BRIEF.md` (§ standing constraints) **contradicted** the ratified ENFORCE ruling and has been **corrected** to "enforce (commitment gate — DR-3/DL-202)". Gate only scope/capacity capabilities; never the record, reviewer/CRR loop, Viewers, or judgment quality.
- *Done this session:* brief corrected + committed.

**9. Landing to canon main — RATIFIED: keep in release-2/ until R1 graduation.** The ratified R2 decisions (DL-164…205 + DR-1…DR-7) stay in `release-2/`, withheld from `main` per the Framework 001 graduation gate (R1 is merged + prototype frozen but not yet GA). Land them — including the item-7 split — when R1 actually graduates. `main` continues to represent shipping-R1 canon only.

---

## Cross-references & unblocks
- **Items 4 + 5** settle the two gates State-1 §2 required before **Phase B**; **item 3** defines the Adaptability computation for **Phase A / Phase C**. Phase A can start regardless (already noted).
- **Items 1 + 2** are now-ratified build instructions in the ingestion-latency doc (updated this session).
- **Item 8** removes the last internal contradiction in the decision brief.
- **Items 6, 7, 9** are governance/landing calls with no build dependency in R2 State-1.

## Follow-ups (deferred, not blocking)
- Pro price finalization when monitoring/sync ship (item 6).
- Execute the DL-200–205 split at R1 graduation (items 7 + 9).
- Full DL-195 Adaptability model + checkpoint-need denominator, later pass (item 3).

---
*Recorded 2026-08-06. Amends: D036 (item 1), D033 (item 2), R2_STATE1_BUILD_PLAN §2a/§2b (items 4–5), R2_RESOLVE_FIRST_DECISION_BRIEF standing constraints (item 8). Under DL-203 §2 (item 3), DR-7 (item 6), Framework 001 (items 7, 9).*

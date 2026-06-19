# DL-080 — Ratify the GA deferred-signup realization (provisional identity · pre/post-signup gating · pre-signup retention & privacy)

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-19 (ratify the GA deferred-signup package after advice). Ratifies `00_owner/decisions/PROPOSAL_GA_DEFERRED_SIGNUP_ENGINEERING_REALIZATION_DRAFT.md`; discharges the open authorization in `PROPOSAL_TWO_MODE_ONBOARDING_DEFERRED_SIGNUP_DRAFT.md` §6.3 and **DL-073 §Phasing ("Before GA")** items (a)/(b)/(c). Grounded in DL-073, DL-046, DL-048, DL-049, DL-074, DL-076.
- **Layer:** Product↔engineering seam (identity / DL-048 gating / retention-privacy). Owner-ratified realization **intent**; **engineering authors** the data model, enforcement wiring, and purge (ratify ≠ author). **GA-gated** — Alpha/Beta runs authenticated and needs none of this. No doctrine; epistemic invariants preserved.

## Decision — adopt the GA deferred-signup realization (three parts)
1. **Provisional identity (Part A).** A **provisional `Principal`** (`is_provisional`) is created at first touch; **claim = in-place promotion** (bind the auth identity, flip the flag) with **full identity and record continuity** — the **same principal**, records created anonymously **carry through claim unchanged** (claim is **not** reanalysis; **OB-5** preserved). Reuses the existing `anonymous_id → principal_id` join and the **DL-049 promotion-not-migration** precedent. *(Claim transaction, token security, multi-device/collision handling = engineering realization.)*
2. **Pre/post-signup gating (Part B).** Anonymous entitlement = **exactly one project, Fast Pass only**, within the **Free / Tier-1 per-run envelope** (§4b) and Free routing (§4c), **per-session/per-device rate-capped**; **Deep Pass, project #2, and persistence require signup.** **Pre-signup consumption resets to the standard Free monthly governor at claim** *(owner decision — don't penalize the conversion).* Implemented as a **new "anonymous" identity-state row in §4c config**, not new code — the contracted **DL-048 enforcement** and the **DL-074 normalized-compute governor** are reused; honest-limit disclosure (UP-4) applies at the cap; internal/test excluded.
3. **Pre-signup retention & privacy (Part C).** An unclaimed provisional project is **Operational-class**, retained for a **30-day unclaimed TTL, then hard-deleted** *(owner decision)*; **canonical retention (project-lifetime + 1 yr, §4) attaches at claim**, when a durable owner exists. A **never-claimed session is purgeable and non-linkable** to a person (GDPR/CCPA erasure); **minimal PII** pre-signup; the provisional-session token is **unguessable, single-session, expiring**. Adds a **"provisional / unclaimed" retention class** to §4.
4. **Packaging.** Ratified as **one decision** (this DL) covering all three parts (owner's call on the proposal's packaging question).
5. **Invariants preserved (binding).** OB-1 / OB-5 (provisioning computes/generates/governs nothing; only reanalysis changes assessment); **identity continuity**; the DL-046 60-second Time-to-First-MRI definition; the **contracted DL-048 enforcement reused via config**; no fabricated assessment / honest limits.

## Opportunity (why this direction)
Realizes the ratified **save-to-keep** model (DL-073) end-to-end: a first-time user reaches the 60-second aha **anonymously**, then signs up only to **keep** their work — the dominant PLG activation pattern — while the **anonymous cap bounds cost/abuse** and **reset-at-claim** keeps conversion economics clean. The provisional-`Principal`/claim-as-promotion design makes continuity structural, protecting record integrity at the conversion seam.

## Realization (engineering follow-on)
Engineering **proposes**: the provisional-`Principal` data model + the claim transaction (atomic/idempotent, collision handling, token security); the **§4c "anonymous" tier row**; the **§4 provisional/unclaimed retention class**; the purge job + erasure guarantees; a **claim-continuity test** in the traceability matrix. **Built before GA; not before** (Alpha/Beta authenticated).

## Supersedes / Amends
**Realizes DL-073 §Phasing (a/b/c)**; discharges the two-mode proposal §6.3 authorization; settles the two open owner values (**reset-at-claim**; **30-day unclaimed TTL**) and the packaging (one DL). Reconciles with DL-046 (60s unchanged), DL-048 (envelope/enforcement reused), DL-049 (`Principal`), DL-074 (governor), DL-076 (GA stage). **No ratified content superseded; no doctrine; epistemic invariants preserved.**

## Provenance
Owner decision via working session, 2026-06-19; the owner requested advice and ratified the recommended positions (provisional `Principal` claim-as-promotion; anonymous one-project/Fast-only/Free-envelope with **reset-at-claim**; provisional Operational-class with a **30-day unclaimed TTL**). AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.

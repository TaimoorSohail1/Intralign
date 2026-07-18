# DL-130 — Read-signal role-clarity — grounding cut + reliability trust-check

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Read-signal role-clarity — cut the redundant grounding scale; reliability becomes a trust-check

**Class:** A (experience-doctrine — how the read's quality signals are presented) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-read-signal-roles.md`.
**Refines** DL-123/124 (read architecture), DL-129 (the maturity ladder), **D051** (reliability basis), **D196b** (grounded-is-the-state). **Does NOT touch** the composite band (Enh #6 — explicitly deferred).

---

## Decision

The read had four overlapping quality scales — band, grounding, reliability, and the ladder — that read as redundant clutter. The fix is **role-clarity, not a merged value**: three elements, each with one unmistakable job — **the read** (band + CAF, what OSLO concludes), **your progress** (the maturity ladder), and **the trust check** (reliability) — via two moves.

### Part A — Cut the redundant grounding scale
The standalone **grounding word** (barely→well grounded), shown as the top-bar chip's companion, was redundant with the ladder rungs (*Corroborated* = partly, *Grounded* = largely). The chip now carries the **rung** — strictly more informative, since it also reflects anchoring and validation. Grounding is **not** lost: it survives as the fine measure under the confirm-vs-fix **limiter** (DL-123), the per-dimension **CAF evidence cues** (Option C), the **`#ov-grounding` rollup** (DL-124), and the **popover qualifier**. Only the duplicate top-level word is cut. **D196b amended:** the "grounded" grounding-state vocabulary is now required on the popover qualifier + the read rollup (where grounding is specifically shown); the top-bar chip carries the earned rung (a maturity state, never the user's verb "confirm").

### Part B — Reliability becomes an adaptive trust-check
Reliability stops reading as a quality word alongside the band and becomes a **guardrail** with two states:
- **Sound basis** — no leg (Coverage · Evidence · Assessability) is a concern and no false-confidence condition holds → a quiet, confirming **"✓ Sound basis"** check (calm, neutral — the tick in `--cool`, **never** `--earned`), the level kept when the basis is even, the per-leg detail on demand.
- **A gap** — a leg is thin, or false-confidence holds (high band on low reliability, D052) → it goes **loud**: the resident line names the thin leg, and the D052 "Read this with care" flag surfaces as the primary reliability voice, naming the shortfall.

This is the honest behavior — reliability looks like a *check*, not a scale you climb; quiet when you're fine, insistent when you're not — and it strengthens the trust differentiator rather than diluting it.

## Why — the constraint that shaped it

A single blended value was rejected: it is the composite score D183b forbids (reads as a forecast) and it would hide *which* lever is stuck (haven't-validated vs. can't-trust-the-inputs). Merging reliability into the ladder fails on dynamics — the ladder only rises and is **celebrated**, reliability must be able to **fall** and is **never** celebrated. Even co-locating them on one surface was rejected: visual proximity invites *"I climbed it, so it's trustworthy"* — the exact false-confidence conflation the separation prevents. So the win is cutting the redundant scale and sharpening roles, not merging.

## Guardrails (executable)

- **Reliability stays a truth signal** — independent of the ladder, able to be low and to fall, **never celebrated** (the sound check is `--cool`, never `--earned`), and **always available** (quiet ≠ hidden). → `_assertReliabilityIsATrustCheck`.
- **Grounding survives as the fine measure** — the limiter, CAF cues, `#ov-grounding` rollup, and popover qualifier are untouched; D196b still requires "grounded" where grounding is shown. → `_assertConfirmIsTheVerbAndGroundedIsTheState` (amended).
- **No composite score** (D183b); **the band is untouched** (Enh #6 deferred to a tripwire).
- **The ladder stays earned/monotonic** — the top-bar chip carries the rung; `_assertLadderRungsAreEarned` unchanged.

## Governance

Lands as Class-A canon via `dl-land`, refining DL-123/124, DL-129, D051, and amending D196b. Built + verified in the deliverable prototype (boot self-check **151/151**, 0 pageerrors; new guard `relIsATrustCheck` green; `confirmIsTheVerb` / `relBasisShowsThin` / `ladderRungsAreEarned` still green). The composite **band** stays out of scope. AI drafted + built; **only the owner ratifies.**

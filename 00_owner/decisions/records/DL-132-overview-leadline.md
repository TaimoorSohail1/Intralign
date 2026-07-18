# DL-132 — The Overview lead-line — OSLO's read as one plain sentence, retiring after first engagement

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# The Overview lead-line — OSLO's read as one plain sentence, retiring after first engagement

**Class:** A (experience-doctrine — how the read leads for a first-time user) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Packet:** `DECISION-PACKET-overview-leadline.md`.
**Amends** D179a (read-first order — adds a plain-language preface *inside* the confidence card). **Refines** DL-123/124 (the read architecture). **Upholds** D183b (no composite/forecast), D003 (maturity, not health), D002/D051 (the read never stands bare), D179e (counts have one home).

---

## Decision

The Overview's first-time problem was **density of guidance, not information**: a newcomer met the ramp, the limiter, the CAF rows, and several competing CTAs before anything told them, in plain words, what OSLO concluded and what to do. The fix is a **plain-language lead-line** at the top of the read plus a **sunset** so it never becomes standing clutter.

### 1. The lead-line
A single plain-language sentence now leads the read, rendered by `_leadLineHTML()` from live state and placed **inside** the confidence card, above the ramp — so the confidence card stays the first panel (D179a intact; the lead-line is its plain-language preface, never a panel above it). Three clauses, each a paraphrase of a signal the read already shows:

1. **The band, in plain maturity words** — a words-only paraphrase (`_LEAD_BAND_PLAIN`: "just getting started" → "well-formed"). Never a number, never a probability.
2. **The weakest part** — the computed limiter (`_limitingOf`), named plainly.
3. **The one next step** — a clickable pointer into "Start here" that names the top open issue when its title carries no figure, and otherwise points cleanly ("start where OSLO points, in 'Start here' below").

It reads *outside-in*: plain language first, then the structured ramp/CAF for fidelity. It is a **synthesis of what the read already says**, not a new fact and not a score.

### 2. The sunset — it retires after first engagement
The lead-line is a **first-time nudge**, not a permanent echo of the read. It retires **permanently** the first time the user engages with Start here — opens an issue (`openIssue`), confirms the load-bearing assumption (`startInlineConfirm`), or follows the lead-line's pointer (`_gotoStartHere`). A `leadLineDone` flag remembers it; it **never cycles to the next issue** and never returns. Before first engagement it is the newcomer's entry point; after, the structured read stands on its own and the limiter carries the permanent plain-language read.

### 3. What cleared the field (the safe dedupes)
So the one next step could win, two genuine duplicates were removed: the **Start-here overflow "See all open issues in the Attention map →"** (the map stays in the nav and — until the companion footer declutter — the confidence-card footer), and the **verbatim echo inside the Feasibility CAF-row hover tip** ("This is the lowest dimension — confirm it to lift the read"), which restated the limiter line word-for-word. The doctrine-required limiter line itself (`#ov-limit`, D002/D051/D186c) was **kept** — its overlap with the lead-line is only during the first-time nudge and disappears when the lead-line retires.

## Why — the constraint that shaped it

The lead-line earns its place **only** as a plain-language synthesis, never a forecast. A one-liner at the top of the read is one careless edit away from *"your plan is 72% ready"* — the exact composite-forecast misread D183b forbids, arriving through the top line. So the line carries **no number and no percentage**, and it must be **computed from state** (it names the live limiter, proving it is not hand-typed). Both are enforced.

## Guardrails (executable)

- **The lead-line is a synthesis, never a score** — no digit, no percentage; computed from the live limiter; present while live. → `_assertLeadLineIsASynthesisNotAScore()`.
- **The confidence card is still the first panel** — the lead-line lives *inside* `.card.hero`, above the ramp. → `_assertConfidenceIsTheFirstPanel()` (unchanged).
- **The read never stands bare** — the limiter line stays; the transient lead-line does not replace it. → `_assertConfidenceCafCoupled()` (unchanged).
- **No composite score** (D183b); **counts have one home** — the lead-line names no tally (D179e).
- **The nudge sunsets** — `leadLineDone` retires it on first engagement and it never re-renders; the guard treats a legitimately-retired lead-line as valid, not empty.

## Governance

Lands as Class-A canon via `dl-land`, amending D179a and refining DL-123/124. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; new guard `leadLineIsSynthesisNotScore` green; verified across fast-pass, deep-pass, false-confidence, and all-clear reads, and across the retire-on-engagement transition). AI drafted + built; **only the owner ratifies.**

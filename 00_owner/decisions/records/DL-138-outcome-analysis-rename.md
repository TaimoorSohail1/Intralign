# DL-138 — Extended Analysis is renamed to Outcome Analysis

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# "Extended Analysis" is renamed to "Outcome Analysis"

**Class:** B (canonical terminology — presentation, no behaviour change) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Amends** the canonical term established under D040 (the two-pass analysis model) and governed by DL-053 (preserve canonical terminology — this is the owner-directed amendment that changes it). **No behaviour changes.**

---

## Decision

The product term **"Extended Analysis"** is renamed to **"Outcome Analysis"** everywhere it appears in the product — every user-facing surface (the analysis-state tooltip, the completion chat notices, the notification labels, the History records, the reviewer-response copy) and the paired configuration labels (e.g. the overage unit *"per Outcome Analysis (Deep Pass)"*). All 44 occurrences in the deliverable were updated in one pass; none remain.

The rename is **terminology only** — the two-pass model is unchanged: the Fast Pass still delivers the initial read, and the deeper second pass (informally the *Deep Pass*, a name left as-is) still firms it, runs non-blocking (D040), and costs a token budget (DL-048). What changes is only what it is *called*.

"Outcome Analysis" also **coheres with the core concept**: OSLO's read is **Outcome Confidence**, and the **Outcome Analysis** is the run that firms it — the noun now names the two halves of the same idea, where "Extended" only described the run's depth.

## Guardrails

- **Terminology only** — no analysis behaviour, cost, cadence, or state-machine change; the Fast/Deep two-pass model (D040) and the token budget (DL-048) are untouched.
- **Complete + consistent** — zero occurrences of "Extended Analysis" remain in the build; the paired config labels (overage unit, census) were renamed too, so no surface says the old name.
- **"Deep Pass" is retained** — the informal run name is unchanged; only "Extended Analysis" moved.
- **No index/forecast implication** — "Outcome Analysis" names a *run*, not a score; it does not reintroduce a composite (D183b).

## Governance

Lands as Class-B canon via `dl-land`, amending the D040 terminology (and the DL-053 preserve-terminology default, by the owner's direction). Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; no guard pinned the old string). AI drafted + built; **only the owner ratifies.**

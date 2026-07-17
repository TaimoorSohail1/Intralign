# DL-124 — Grounding leaves Progress — the read owns grounding

- **Date:** 2026-07-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Grounding leaves Progress entirely — the read owns grounding; Progress is work-state

**Class:** A (read-architecture refinement of Option C) · **Framework 001** — AI drafts; **owner ratifies at land.** · **Amendment with explicit supersession.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-17 · **Follows:** DL-123 (Option C) · **Prototype:** `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` (md5 **b66a8276**, boot **144/144**).

---

## Decision

DL-123 consolidated grounding onto the read but **left a compact grounded summary on Progress** (as the D180 anti-burndown anchor). This amendment finishes the consolidation: **grounding leaves Progress entirely.** The whole-read grounded/inferred total now lives **on the read**, as a one-line rollup at the **foot of the CAF rows** (`#ov-grounding`) — directly under the per-dimension evidence it summarizes — so grounding reads at both resolutions in one place: *per dimension* on each CAF row, *whole-read* on the rollup. **Progress becomes a pure work-state panel** — Open (what is outstanding) · Closed (what the user's work landed) — and nothing else. Load-bearing remains on the Inference map (DL-123 fork 3a). The per-dimension evidence cue is also given a legible, roomier treatment (bar + labelled fraction, e.g. "Mostly inferred · 1 of 3").

**Why the read is a better home than Progress ever was:** the overall grounding total belongs beside the per-dimension detail, not stranded on a separate panel; a PM reads "how grounded is my plan" — overall and by dimension — without a surface-switch. And Progress, freed of the grounding anchor, states honestly what it is for: the work.

**Why this does not re-open the burndown hole (D180):** the anti-burndown protection moves from *"grounding is the star of Progress"* to *executable structure*. Progress carries no denominator, no percentage, no target, no completion/remaining vocabulary, and no provenance count — each enforced at boot. The maturity signal the grounding anchor used to carry now lives, unmistakably, on the read.

---

## What this supersedes / amends (explicit)

- **DL-123 — "Progress keeps a compact grounded summary."** *Superseded.* Grounding leaves Progress; the compact summary is retired and its content moves to the read's grounding rollup. Every other clause of DL-123 stands (CAF leads; per-dimension evidence; global qualifier retired; load-bearing on the Inference map).
- **D180 / D180a — "Progress is grounding, not clearing; the grounded row is the star."** *Amended.* Under Option C the maturity signal lives on the read, so grounding is no longer Progress's anchor. Progress is **work-state**, and its freedom from the burndown frame is now carried by the **no-burndown-grammar / no-denominator / no-provenance-count guards**, not by a resident grounding number. **D180c (grounding rises while issues rise — not a regression) is preserved**, now proven across the two surfaces (grounding on the read, issues on Progress), drawn identically and neutrally.
- **D179e — counts have one home.** *Consistent, not weakened.* The grounded/inferred counts' one Overview home moves from Progress to the read's rollup; the guards (`_assertNoCountIsRenderedTwice` / `_assertProvenanceCountsHaveOneHome`) follow them there. Every provenance count still has exactly one home.
- **D253 / D194c / D196** *(statement unit · epistemic-class naming · confirm-is-the-verb)* — *preserved, relocated.* The rollup names the statement unit and both ratified classes (Confirmed by you · From OSLO, single-sourced); the guards that proved this on Progress now prove it on the read.

---

## Scope boundary — what did NOT change

Neutral maturity levels + neutral evidence cue (D003/D175). The statement model, the load-bearing definition, and every count's computed-from-state guarantee (D173). The confidence read's band, limiter (which still carries "the read never stands bare," D002/D051), and per-dimension evidence. Tiering / Reports / Plans and the Progress **issue counts** themselves (open/closed) are untouched.

---

## The architecture lock (Condition 2, executable)

Two guards register in the boot self-check to hold this across future edits:

- **`progressIsWorkStateOnly`** — fails the build if any provenance count (grounded · inferred · load-bearing) reappears on Progress, or if Progress renders any count that is not an open/closed work count.
- **`groundingLivesOnTheRead`** — fails the build if the read's grounding rollup is stripped or stops carrying the grounded/inferred counts + the statement unit.

Together with the standing D180 no-burndown guards, a future edit cannot re-make Progress a grounding panel *or* let it drift into a burndown — either goes red at boot.

---

## Governance

**Slice 3 (Overview)** and **Slice 10** re-sign on the new build (md5 b66a8276). Lands as **Class A canon via `dl-land`**, an amendment with explicit supersession of DL-123's Progress clause + D180. AI drafted + built on ratification; **only the owner ratifies.**

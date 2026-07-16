# DL-117 — Confidence and CAF coupling: episodic trend leaves the state/CAF seam; the required read stays

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Confidence ⇄ CAF coupling: the episodic trend leaves the state↔CAF seam (D179a); the required read stays

**Class:** A (Overview-hero presentation realization) · **Framework 001A** (AI drafts realization; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-16 · Grill record: **Enhancement #5** (intermediate release).

## Problem
On the Overview confidence card the episodic **trend** (sparkline + direction word, "↗ Strengthened") sat in the seam **between** the Outcome Confidence band (the STATE) and the "What's driving it" CAF rows (its three dimensions). Because Outcome Confidence **is the roll-up of the three CAF dimensions**, an episodic event wedged between them split two surfaces that should read as **one indicator** — the friction the owner named between the confidence and CAF indicators. The redundant grounding restatement had already been absorbed by the DL-116 drill-down, sharpening the split.

## Decision (recommended — owner ratifies)
The episodic trend **relocates out of the seam into the card footer** (beside Timeline), and the CAF rows are pulled **flush beneath the band**, so the overall band and its three dimensions read as one coupled indicator. What **stays** in the state head is the required read, unchanged:
- the **grounding qualifier** — **D002/D051**: the read never stands bare;
- the **limiter** ("Feasibility — the lowest. Confirm it to lift the read.") — **D186c/D185.4**: name the limit + the verb — which now doubles as the **bridge into the CAF rows** (it names the limiting dimension, the first row below).

The sparkline is hidden in the footer; the **direction + word** carry the trend (**D056** — direction, never a magnitude), with the same computed render path and element ids.

## Conformance basis (no canonical definition is changed)
This is presentation **realization that conforms to already-ratified doctrine**:
- **D179a** (state outranks event; the trend is episodic) is realized more fully by moving the episodic trend **off** the resident state seam;
- **D002/D051** and **D186c** are **preserved** (qualifier + limiter retained — proven by guard, below);
- **D176b** (CAF is bands, not percentages), **D175/D003** (the card is a neutral maturity zone) — untouched;
- the DL-116 drill-down continues to carry the "how to lift it" detail under each dimension.

## Scope boundary (explicitly NOT in this decision)
Removing the **grounding qualifier** or the **limiter** from the card face — that would require a **doctrine amendment** to D002/D051 or D186c (an owner-ratified escalation). It was reviewed and **deliberately not taken**: the doctrine-safe coupling (relocate the episodic trend only) delivers the de-friction without weakening the read.

## Guard (executable — boot `window._S10`)
`_assertConfidenceCafCoupled` (aggregate key `confCafCoupled`): proves (1) the trend has left `.conf-focus` and now lives in `.conf-foot`; (2) no trend row sits between the state and the CAF rows; (3) **the doctrine guardrail** — the grounding qualifier (`.cr-qual`) and the limiter (`#ov-limit`) **remain** in the focus, so a future edit that couples by *deleting the required read* fails the build. Live self-check: **145/145, 0 pageerrors**, both themes; the pre-existing hero/neutrality/bands guards are unchanged.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). The confidence-hero layout is product-authored realization proposed for owner ratification; **no canonical definition is touched**. Overview + Slice-10 reopened; re-signoff required. AI recommends; only the owner ratifies.

## Provenance
Owner request 2026-07-16 — "better couple/integrate the confidence indicator with CAF and remove the content in between that creates friction." Design collaborated via mockup → a realistic preview rendered in the prototype's own stylesheet; the review surfaced that most of the "content in between" is **doctrine-required** (D002/D051, D186c), so the owner locked the **doctrine-safe** coupling (relocate the episodic trend only). Built into the slice-10 prototype and verified (145/145). AI implemented; owner ratifies.

### Sources
- Doctrine: **D179a** (state outranks event / episodic trend), **D002/D051** (the read never stands bare), **D186c/D185.4** (name the limit + the verb), **D056** (direction, never a magnitude), **D176b** (bands, not percentages), **D175/D003** (neutral maturity zone).
- Prototype: `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` — the `.card.hero` confidence card + `_assertConfidenceCafCoupled`.

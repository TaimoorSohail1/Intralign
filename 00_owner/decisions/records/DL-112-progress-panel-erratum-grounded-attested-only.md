# DL-112 — Erratum to DL-111 — grounded facts are attested-only; two provenance states; load-bearing is a superset

- **Date:** 2026-07-14 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Erratum to DL-111: grounded facts are attested-only; two provenance states; load-bearing is a superset

**Class:** A (owner-directed correction) · **Framework 001A** (AI drafts; owner ratifies; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-14 · Erratum to **DL-111**.

## Decision
DL-111 adopted the foundation-bar design and, from the parallel-session "blend / 29-hero" lock, inherited three defects. The **design is kept**; the **arithmetic and vocabulary are corrected**:

1. **Grounded facts = ATTESTED ONLY.** The hero counted `_ciGroundedClaims() + _ciInferredClaims()` and captioned it "grounded facts" — but the inferred half has `evidence_id === null`. An inferred claim is not a grounded fact. The hero is now the **grounded (attested) count alone**; the "Confirmed by you" bar segment carries only its label.
2. **Two provenance states, not three.** The registry is `{basis:'derived', countKey:'inferred'}` — one state wearing two names. The legend's "Derived — supported" advertised a class the model does not have. There are two states: **grounded** (evidence) and **inferred** (none). "From OSLO" **is** the inferred state, rendered hatched. Legend: "Grounded — your evidence" · "Inferred — OSLO's read".
3. **Load-bearing is a superset, not a disjoint addition.** The inferred *claims* are a subset of the load-bearing *inferred items of every type* (assumptions, relationships, metrics…). The bar `+`-joined the two as if disjoint. Load-bearing is now its own line — "Your read leans on N inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →" — never summed into the bar. (The load-bearing count legitimately exceeds the inferred-claims count because it counts items of every type, not claims; both numbers were right — the panel lied about what they meant.)

## Guards — grade the population, not the string
The DL-111 guards passed this because they proved the counts were *computed* and the class names came from the *registry* — neither of which was the defect. Added/changed:
- `_assertPgxBarIsComputedFromRealCounts` — hero **== grounded** (RED if it equals grounded+inferred).
- `_assertPgxTwoProvenanceStates` — the legend names exactly two classes; "derived/supported" is forbidden.
- `_assertPgxBarStructure` — load-bearing may not be drawn inside the bar or `+`-joined to the inferred claims.
Live prototype: **136/136 self-check, 0 pageerrors**, both themes.

## Supersedes / Amends
Amends **DL-111** (the Overview Progress panel arithmetic + provenance vocabulary). Design unchanged. No other surface affected.

## Provenance
Owner defect report, 2026-07-14, naming the P1 (`total = grounded + inferred` captioned "grounded facts"), the fake third class (`{basis:'derived',countKey:'inferred'}`), and the disjoint `+`. AI implemented the correction and the population guards; owner ratifies.

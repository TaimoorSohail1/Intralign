# DL-113 — Progress panel unifies on one named unit — the statement (adds a DL-053 entry; amends DL-111)

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Progress panel unifies on one named unit, the "statement" (amends DL-111/DL-112 for this panel; adds a DL-053 entry)

**Class:** A (owner-directed UX + vocabulary change) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-14 · AI implementation + owner ratification owed. · Grill record: **Decision 253**.

## Problem
The Overview Progress panel measured grounding without ever naming its unit. The hero read "N of M grounded in your evidence" ("M **what**?"), and the panel reported three numbers over three different populations — the hero and bar over **claims**, the load-bearing line over **inferred items of every type** — with no shared, understandable unit. Comprehension suffered: a reader could not tell that the hero's denominator and the load-bearing count measured different things.

## Decision
The Progress panel counts **one user-facing unit — the "statement."**

1. **Definition.** A **statement** is a `ContextItem` (RELEASE_1_DATA_MODEL_SPECIFICATION §9) of a **decision-bearing type: `claim` · `assumption` · `metric` · `relationship` (dependency).** `entity` and `interpretation` are **excluded** from the count. Each statement is either **grounded** (`evidence_id` present → "your evidence" / *Confirmed by you*) or **inferred** (`evidence_id` null → *From OSLO*). This is the same nullable-`evidence_id` distinction the schema already carries — no new object, no new extraction.
2. **Hero names the unit.** "N of M statements grounded in your evidence" — N = grounded statements (computed; the primary number is the grounded count **alone**, never grounded + inferred, per the DL-111 erratum); M = grounded + inferred statements. Caption unchanged ("grounded in your evidence / the rest of your read is OSLO's inference").
3. **Bar.** Two provenance states over statements: a grounded segment (label *Confirmed by you*, no number — the hero owns it) and a hatched *From OSLO* inferred segment carrying its count.
4. **Type-decomposition line.** "M statements = X claims · Y assumptions · Z metrics · W dependencies" — computed, secondary styling; the one unit visibly decomposes into the named types.
5. **Load-bearing as an honest subset.** "Of your P inferred statements, K are load-bearing — they hold up a Critical issue or the limiting dimension." K counts load-bearing **statements** (`_ciLoadBearingStatements()`), so K ≤ P **by construction**. This retires the DL-111-erratum awkwardness where load-bearing (all item types) exceeded inferred claims and could not be drawn as a subset. The **all-type** load-bearing figure (which may include load-bearing `interpretation` items) is retained on the separate **Inference-map** surface, which speaks in all inference, not statements.

## New DL-053 Disambiguation Register entry
| User-facing term | Internal object | Note |
|---|---|---|
| **statement** | `ContextItem` where `item_type ∈ {claim, assumption, metric, relationship}` | The panel's counted unit. **Distinct from "claim"**, which is one `item_type`; "statement" is the decision-bearing superset. Provenance-neutral (a statement may be grounded or inferred) — deliberately **not** "fact", which the DL-111 erratum reserves for grounded items only. |

## Amends / supersedes
- **Amends DL-111** (Progress panel): the panel's denominator/population is **decision-bearing statements**, not claims. The two-provenance-state model and "hero = grounded-only" erratum are **unchanged** and now expressed over statements.
- **Consistent with DL-112 / supersedes WI-R6 for this panel**: the hero's primary number is still the grounded count alone; the "of M" remains denominator context, not a burndown target. The WI-R6 claim-scoped "17 of 28" hero is superseded by the statement-scoped hero **for this panel only**. No other surface changes.
- **No change** to the Inference map, Reports, Confidence/CAF, or any tiering surface.

## Guards (executable doctrine — live at boot, `window._S10`)
- `_assertPgxHeroNamesTheUnit` — the rendered hero contains the unit noun "statements" (fails loudly if a future edit drops it).
- `_assertStatementDecompositionSumsToTotal` — the four type counts sum to M, computed (perturb-proof).
- `_assertLoadBearingIsHonestSubset` — every item in the panel's load-bearing count is an **inferred statement**, and K ≤ inferred statements.
- `_assertPgxBarIsComputedFromRealCounts` — hero numerator == grounded **statements** (RED if it equals grounded + inferred).
- Live self-check: **139/139, 0 pageerrors**, both themes.

## Boundary (owner-affirmed)
Stays within **AE-06 Understanding Debt** (Future, not surfaced in R1): this **reads out existing `ContextItem` state** and names its unit. It introduces **no accumulated "debt" aggregate**, no new object, and no new lifecycle.

## Provenance
Owner critique, 2026-07-14 ("18 of 29 grounded in your evidence… never specifies the unit of measurement"), grounded in `evidence-units-analysis.md` and the R1 Data Model §9. Concept approved by the owner after a before/after panel mock; prototype + six panel docs folded in and verified; owner re-signed the Overview/Progress panel 2026-07-14. AI drafted this record and the guards; **owner ratifies**. Route through `dl-land` (never the web form); numbered at land per DL-065.

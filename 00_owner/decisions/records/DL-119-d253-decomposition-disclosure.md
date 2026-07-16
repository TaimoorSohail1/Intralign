# DL-119 — Amendment to D253: statement type-decomposition moves from resident to an on-demand disclosure (density pass)

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — Amendment to D253: the statement type-decomposition moves from resident to an on-demand disclosure (density pass)

**Class:** A (Progress-panel presentation amendment) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-16 · **Amends:** D253 · Grill record: **Enhancement #8** (Progress density pass).

## Problem
The Progress panel is the densest surface on the Overview (~14 resident figures). After the Overview role-model work removed the *duplication*, the remaining issue is *hierarchy*: the statement **type decomposition** — "N statements = claims · assumptions · metrics · dependencies" — sits resident at similar weight to the panel's star (the grounded-vs-inferred ledger), competing for the eye. Most PMs don't need the type breakdown at a glance.

## Decision (recommended — owner ratifies)
The statement **type decomposition** moves from a **resident** element to an **on-demand disclosure** ("▸ what the N statements are"). **D253's substance is fully preserved:**
- the panel still counts **one unit — the statement** (claim · assumption · metric · relationship);
- the **hero still names its unit** ("N statements grounded…") — `_assertPgxHeroNamesTheUnit` unchanged;
- the four type counts **still sum to the total**, computed from state — `_assertStatementDecompositionSumsToTotal` unchanged and green (the decomposition remains in the DOM; only its *visibility* is toggled).

**Only the decomposition's resident visibility changes.** Nothing else is touched: the grounded/inferred ledger, the confirmed-by-you vs from-OSLO bar, and the counts stay resident in their one home (D179e).

## Scope boundary (explicitly NOT changed)
- The **provenance legend STAYS resident.** It is guarded — `_assertPgxTwoProvenanceStates` (DL-111 erratum) requires it to prove "two provenance states, never three." Folding it into the bar was attempted and correctly **rejected by the guard**; it is not part of this amendment.
- The **load-bearing line, the ledger, and the open/closed counts** are unchanged (their density is intrinsic state, and D179e homes the counts here).

## Guard (executable — boot `window._S10`)
`_assertStatementDecompositionSumsToTotal` (D253) remains green — the four type counts sum to the total, read from state, whether the disclosure is open or closed (the decomposition element is always in the DOM). `_assertPgxTwoProvenanceStates`, `_assertPgxHeroNamesTheUnit`, `_assertEveryClassNameResolves`, and the counts-one-home guard (D179e) all hold. Live self-check: **145/145, 0 pageerrors**, both themes.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). A bounded **presentation amendment to D253** — no data-model or unit change; the decomposition's *computation* is untouched, only its default *visibility*. Slice-3 (Overview/Progress) reopened; re-signoff required. AI recommends; only the owner ratifies.

## Provenance
Owner asked whether Progress needed further optimization (2026-07-16); density/hierarchy pass proposed and mocked; owner chose to tuck the decomposition (Option B), accepting a D253 amendment. Built into slice-10 `_progressHTML` (the decomposition wrapped in `.pgx-decwrap` behind `togglePgxDecomp()`), verified 145/145. The legend fold was tried and **guard-rejected** — kept. AI implemented; owner ratifies.

### Sources
- Doctrine: **D253** (the panel counts one unit — the statement; the decomposition sums to the total), **DL-111 erratum** (`_assertPgxTwoProvenanceStates` — two states, never three), **D179e** (counts one home).
- Prototype: `oslo-product-output/vertical-slices/slice-10-tiering-limits/prototype.html` — `_progressHTML` (`.pgx-decwrap` / `.pgx-disc`), `togglePgxDecomp()`.

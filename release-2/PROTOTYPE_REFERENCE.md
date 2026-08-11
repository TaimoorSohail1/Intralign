# Reference Prototype — `oslo-prototype-r2.html`

The **canonical AI-first reference implementation** (DR-1). A single self-contained HTML file — no build step, no server, no external dependencies — that demonstrates the full R2 read experience with simulated analysis and an embedded self-check harness.

## What it is (and isn't)

It **is** the behavioral source of truth: the exact interaction model, state transitions, copy, and honesty affordances the R2 build must reproduce. When a slice doc and the prototype agree, the prototype settles any ambiguity the prose leaves open.

It **is not** production code. Analysis is fixture-driven (the "DevNorth 2026" sample plan), the pillars read from hardcoded counts pending the real issue layer, and there is no backend. The slice docs' "prototype-vs-canon correction" notes flag every place the prototype knowingly deviates from ratified canon — those deviations are the Phase-A corrections in `BUILD_SEQUENCE.md`, not bugs to copy.

## Issue model — what's simulated (DL-209 / DL-210)

The prototype simulates the **derived** issue model, not the hand-authored one:

- **Resolution is derived (DL-209).** `_issueModel`/`_primaryMove` derive the leading act (verify vs fix) from each item's `basisInference`; there is no hand-set `primaryMove`. An unclassified finding **escalates** rather than default-classifying (`findingTypeExhaustiveOrEscalates`).
- **Dimension is derived (DL-210).** Each issue declares a **structural `target`** (`definition | edge | achievability | truth | coverage`) — the one L0 extraction input — and `_dimOf` maps it deterministically to the pillar (`_TARGET_DIM`). No issue hand-sets `dim`. Guard: `dimDerivedFromStructuralTarget` (GT-46).

**Server-side only (Slice 10 — not fixture-simulable, and deliberately absent from the prototype):** the L1 **relational top-down alignment traversal** (outcome→roots over the real dependency graph), the **escalation resolution lifecycle** (runtime → user clarify/verify issue; model-gap → governance), the **leverage-gated known-unknown** display, and the **incompleteness ceiling** (a load-bearing model gap reads *incomplete*, never Fragile). These need the real graph; the prototype's fixture is fully classified, so none of them fire here. See `slices/10-load-bearing-sensitivity-engine.md` §3b.

## Open it

The canonical file is `release-2/oslo-prototype-r2.html` (this doc sits beside it). Open it in any modern browser (Chromium/Chrome/Firefox/Safari) — everything runs client-side.

## The `_S10` self-check harness

The prototype boots a suite of self-checks into `window._S10`, computed by `_s10SelfCheck()`. Each check (`_s10ck(fn)`) asserts one honesty/behavior invariant and returns `true`/`false`. **Build is green when no value is `false`.** The count grows as invariants are added (78 as of 2026-08-09, incl. the DL-209/DL-210 twins) — green means no value is `false`, not a fixed number.

These guards are the *reference oracle* for the acceptance suite — Slice 9 ports each into a real build assertion (`GT-01…GT-33`) with a server-side twin. The guard names are preserved as test names so the client guard and its server twin stay greppably paired (see `acceptance/README.md`).

### Verify green headless

Chromium is the only requirement. Run from `release-2/` (the prototype is a sibling of this doc). With Playwright available:

```js
// verify_green.mjs
import pkg from 'playwright-core';        // or your local playwright
const { chromium } = pkg;
const b = await chromium.launch({ headless: true });
const p = await b.newPage();
const errs = [];
p.on('pageerror', e => errs.push(e.message));
await p.goto('file://' + process.cwd() + '/oslo-prototype-r2.html', { waitUntil: 'networkidle' });
await p.waitForTimeout(400);
const r = await p.evaluate(() => {
  const s = (typeof _s10SelfCheck === 'function') ? _s10SelfCheck() : window._S10;
  const fails = Object.keys(s).filter(k => s[k] === false);
  return { total: Object.keys(s).length, fails };
});
console.log(`_S10: ${r.total} checks · fails: ${JSON.stringify(r.fails)} · page errors: ${errs.length}`);
await b.close();
```

Green = `fails: []` and `page errors: 0`.

## Using it during the build

For each ticket, the reference behavior is: find the relevant function(s) in the prototype (the slice doc's FE↔BE bindings name them — e.g. `_needsFixGroup`, `_payGate`, `_completeReanalysis`), reproduce that behavior on the real stack, and make the corresponding `GT-` assertion green. The prototype is the "does it feel right" check; the slice doc's acceptance criteria + the GT test are the "is it correct" check.

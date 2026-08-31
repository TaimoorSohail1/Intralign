# Diagnosis — the provenance contradiction (R2.0 handoff, Batch 3.5)

**Asked:** is *"Host DevNorth 2026…"* rendering `is-yours` in Intent and `OSLO inference` on Your
Outcome **a wrong-label bug**, or **Your Outcome showing Purpose where it should show the primary
Outcome**? The handoff refused to infer it. Measured against the R2.1 design-line prototype
(`release-2.1/oslo-prototype-r2.1.html`, 10,915 lines), which is what staging matches.

---

## ⚠️ Neither. There is a THIRD source of provenance, and it is a static string

**CONFIRMED — reproducible, one user action, no guard covers it.**

Every artifact carries a hardcoded prose `read:` that **asserts provenance**:

```js
{ key:'intent', title:'Intent',
  read:'Your outcomes, goals and how you’ll know — clear, though the success metrics are still
        OSLO’s inference.' }
```

It renders in the artifact head, **directly above the live per-item chips, in the same card**:

```js
+ '<div class="art-read"><b>OSLO’s read:</b> '+a.read+'</div>';
  ... var rows=_typedItemRows(a);
```

⚠️⚠️ **`.read` is never recomputed. No assignment to it exists anywhere in the file** — searched for
`.read =`, zero hits. It is fixture text, fixed for the life of the session.

**The reachable path that breaks it** — resolving the `metricset` issue:

```js
if(it.key==='metricset' && !it.flagged){ var _ai=A('intent');
  _ai.items.forEach(function(x){
    if(x.prov==='inferred' && (x.type==='goal'||x.type==='success'||x.type==='kpi')) x.prov='you'; }); }
```

**So: resolve one issue → every success criterion and KPI chip flips to `✓ yours` → and the line
directly above them still reads "the success metrics are still OSLO's inference."** The product
contradicts itself inside one card, about the same statements, on the honesty claim.

**13 of the static `read:` strings assert provenance** (*"one is OSLO's inference"*, *"Owners
inferred"*, *"most are OSLO's reconstruction"*, *"one confirmed, one OSLO inferred"*). Every one of
them can be falsified by the user acting on the thing it describes.

### ⚠️ Why no guard caught it

**Zero guards assert read-vs-items consistency.** The guard set covers provenance on the *items*
(GT-75 / GT-80 / GT-90 / GT-91) and consent on *content* (GT-64) — nothing checks the artifact's own
narration against the items it narrates. **A provenance claim in prose is not covered by a guard on
the field.**

---

## What this does NOT settle

⚠️ **It is NOT established that this is the production observation.** The exact string *"Host DevNorth
2026…"* **does not exist in the prototype** — the nearest fixture item is *"Run DevNorth 2026 as a
sold-out, well-rated one-day developer conference"* (`o1`, `type:'outcome'`, `primary:true`,
`prov:'inferred'`). Production carries different fixture text, so the report cannot be matched to a
line here. **Escalated, not inferred.**

**The decisive test, one minute, on the production plan:**

| observation | conclusion |
|---|---|
| the two labels sit in **one card** — an `OSLO's read:` line contradicting chips beneath it | **this defect.** Fix = derive the read from the items, or stop asserting provenance in it |
| the labels are on **different sentences** — Intent's Purpose vs Your Outcome's headline | **presentation.** Both correct for their own field; they read as one claim because both are about hosting DevNorth. Fix = disambiguate the two surfaces |
| the labels are on the **character-identical sentence across two surfaces** | **build defect.** Not reproducible in the reference prototype, so production has a divergent provenance source. Jumps in class |

⚠️ **The three have different fixes. Do not scope before this is read off the screen.**

---

## Two incidental findings, same measurement

**1. `_outcomeProv()` is dead code.** Defined at line 4923, **called nowhere.** It also carries a
silent default — `return p ? p.prov : 'inferred'` — so if it is ever wired up, a plan with no outcome
would assert *"OSLO's inference"* about nothing. **Delete it, or wire it and remove the default.**

**2. `_primaryOutcome()` falls back silently.**

```js
function _primaryOutcome(){ var os=_intentByType('outcome');
  return os.filter(function(x){return x.primary;})[0] || os[0] || null; }
```

⚠️ **`|| os[0]`** — with no item flagged `primary`, the first outcome is used, and the Overview labels
it **`◎ Primary`**. A designation the user never made is displayed as one. Related to the
`_setPrimaryOutcome` / Free-tier one-outcome model, and worth a ruling rather than a quiet fallback.

---

## Does this explain Batch 3.4?

**No, and that matters.** 3.4 reports *"The purpose of the initiative or gate is not stated"* rendered
**in the outcome slot**. In the prototype that slot cannot do this: `_rootOutcomeHTML()` returns `''`
when there is no primary outcome, and the Overview renders `'—'`. **So production's outcome slot has
fallback behaviour the reference prototype does not have.** 3.4 stays open and stays undiagnosed — but
it is now a *narrower* question: what does production render in the outcome slot when extraction
yields no primary outcome, and where does that string come from?

---

## Recommendation

**Split the handoff item in two.**

**3.5a — CONFIRMED, and it is Altering** (it changes a displayed judgment): the artifact `read:`
asserts provenance it cannot maintain. Two candidate fixes, and this is an owner call:

- **derive** the read from the items' live `prov` — honest, and the read stays informative; more work
- **stop asserting provenance in the read** — the chips already carry it per item; cheapest, and it
  removes a whole class of drift

⚠️ **Either way it needs a guard**, because the current state is a provenance claim no invariant
covers. That is what the existing guard set is for.

**3.5b — the original report, still NOT ESTABLISHED.** Run the one-minute test above first. **Do not
let 3.5a's confirmation be read as closing 3.5b** — they may be the same defect and may not.

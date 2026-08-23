# DL-237 — A numeric confidence value may exist server-side; it may never be serialized

- **Date:** 2026-08-23 · **Status:** Ratified · **Decided by:** Idris (staging review 2026-08-22)
- **Class:** A

## Context — what was measured

`GET /api/workspace` returns, per project, `confidence_band: "Fragile"` alongside `confidence_index: 42`.
Confirmed on two independent projects (42 and 32), observed to swing 32 → 5 on a single confirm, and
shipped to the client on every workspace load.

The UI is not at fault: it renders words throughout, and five views were swept for numeric scores with
none found in the DOM. **The violation never reaches the render layer.**

## This is a SCOPE EXTENSION, not new doctrine

The prohibition already exists and is ratified:

- **Slice 01 L2** (`ratified-DL · DL-195 §2, DL-194 §3`) — *"Never a weighted blend, never a 0–100 number."*
- **Slice 01 INV-3** — *"no 0–100 number/dial/probability anywhere; endpoints Fragile→Sound."*
- **Slice 09 GT-20** — *"Maturity not forecast — no 0–100 number/dial/probability on any integrity
  surface"*, enforced as a lint.

⚠️ **History matters here.** **DL-086 (CHG-121) DID ratify a 0–100 index** as a *"clean, focal,
user-facing"* figure — **for R1**. **R2 reversed it via the D183b reconciliation** (*"ordinal only, no
0–100 number"*). The number in the payload is therefore **not a rogue invention; it is the R1 model that
R2 superseded, still present.**

**What this record adds is one word of scope.** Existing canon forbids the number on any integrity
**SURFACE**. It is **silent on SERIALIZATION**. `confidence_index` never reaches a surface and is
therefore, as written, not prohibited. **That gap is what is closed here.**

## Decision

1. **A numeric confidence value MAY exist server-side** for calculation, comparison and ordering. The
   doctrine cannot forbid arithmetic — bands are derived from ratios.
2. **It MUST NEVER be serialized.** No numeric confidence, maturity or integrity value may cross into any
   client response, be persisted as a trend, or be exposed to a partner, integration or export.
3. **The boundary is SERIALIZATION, not rendering.**

**Why the boundary sits there.** *"Not displayed"* is a choice each surface makes; *"not serialized"* is a
property of the system. A number in a payload is readable in devtools, by any API consumer, and by any
future surface. **A rule that depends on every future engineer declining to render an available number
will fail eventually — quietly, in a dashboard someone builds because the field was there.** This is the
same argument the acceptance register already makes about **GT-104**: *a paywall asserted in client state
is not a paywall.* An invariant asserted at the render layer is not an invariant.

## Why the existing guard could not catch it

**GT-20 is correctly built for the scope it was given** — Slice 09 specifies it as a lint that *"runs over
the actual server-rendered read HTML, not source comments."*

⚠️ `confidence_index` is in the **JSON payload** and never in the rendered HTML, so **GT-20 cannot see
it**. `bandsAreWordsNotNumbers` cannot either — both inspect what the client renders, and the client
correctly renders words. **Every guard in the product is green while the payload carries a 0–100 score.**

**This is not a guard failure. It is a scope gap between "surface" and "serialization".**

## Obligations arising

1. **Engineering** — remove `confidence_index`, and any numeric confidence/maturity field, from every
   client-facing response, starting with `GET /api/workspace`.
2. **Engineering** — extend **GT-20** (or add its server twin) to assert the invariant **at the API
   boundary**. ⚠️ **Schema-level, not string-level:** a renamed field must still fail.
3. **Owner** — record the **bounded exemption** so it cannot be widened by precedent: internal calculation
   and ordering only, with the serialization prohibition stated explicitly.
4. **Owner** — **DL-053 Disambiguation Register** entry for `confidence_index`: what it is, and that it is
   non-serializable.

## Two questions this record does NOT answer

- **What consumes `confidence_index` today?** If nothing does, removal is free. If ordering depends on it,
  that dependency is internal and unaffected by this ruling.
- ⚠️ **Does the band derive from the index?** **Measured evidence says NO:** the index moved **42 → 38**
  while the band moved **Weak → Solid** — **opposite directions.** If the band derived from the index they
  could not disagree on sign. That implies **two independently computed representations of one judgment**,
  very likely related to the Grounding defect recorded against **RB-101** (*"two different Grounding
  numbers exist — `grdLevel` capped vs `_grdWord` uncapped"*).

**Both are engineering questions. Neither changes the decision above.**

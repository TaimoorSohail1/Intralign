# OBLIGATION — N-7 · N-8: the surfaces that leave the building state a different judgment, in a different vocabulary, from the one the mechanism holds

**Status:** OPEN
**Fix:** TaimoorSohail1
**Accepts:** idris-manley
**Class:** R2.0 production blocker · blocking for production
**Raised:** 2026-08-29 / 2026-08-31 staging fitness audit, findings R1 · R5 · R6 · R7; filed 2026-09-01 on discovering that both failing Tier-2 criteria had no obligation object
**Invariants violated:** ⚠️ NOT YET DETERMINED — the acceptance register lives on the design line. **Escalated, not guessed.** Candidate anchors named below in §2 as *doctrine*, not as register ids; owner or dev lead to bind the GT ids before this row is accepted.

## 1 · What was measured

Two criteria in the production-gating subset, both recorded ⚠️ **FAILS**:

- **N-7** one judgment, one word, every surface — findings **R1 · R5**
- **N-8** stakeholder output states only what the mechanism supports — findings **R6 · R7**

### N-7 · R1 — the composite contradicts itself on one page

`MEASURED-BY:` `/OUTCOME INTEGRITY\s*\n\s*([A-Za-z ]+)/g` over `document.body.innerText` at the project `/outcome` route → **two matches on one page: `Under review` and `Fragile`.**

`/workspace`, `/grounding` and `/full-plan` all read **Fragile**. The project masthead is the single outlier, and on `/outcome` it sits directly above a card contradicting it. `Fragile` is a band word; **`Under review` is in no ramp at all.**

### N-7 · R5 — the generated briefing states a different read from the product

The Executive Briefing summary reads: *"The read is **very low confidence**, limited by **clarity**; 27 open findings identify the main uncertainty."* Two defects in one sentence:

1. **"very low confidence"** is confidence vocabulary. The ramp is Fragile · Weak · Developing · Solid · Sound, and the product's own line two paragraphs later is *"maturity, not a forecast"*. **The band word never appears in the briefing.**
2. **"limited by clarity"** contradicts every other surface. The masthead reads *"limited by Grounding"*, `/outcome` chips Grounding **`GATING →`**, and `/full-plan` opens *"Grounding is the current gate."* **The briefing names a different limiting pillar than the product does.**

### N-8 · R6 — engine churn reported to stakeholders as plan change

`MEASURED-BY:` the rendered Executive Briefing body at the project `/reports` route, read via `innerText` from the `Summary` heading, 2026-08-31, cross-checked against the History trail's `ISSUES` entries recorded in B1.

Under **"What changed"** the briefing states **"8 opened · 2 resolved"**. Per B0, the eight openings are re-derivation artifacts of the identity churn — **the plan was never edited** — while only the two resolutions were user acts.

### N-8 · R7 — two smaller defects on stakeholder-facing surfaces

`MEASURED-BY:` `innerText` of the Key risks section at `/reports`, and `/[↑↓] ?[a-z ]*this session/` at `/outcome` → `"↑ weakened this session"`. 2026-08-31.

- A **raw evidence token** reaches exec-facing prose: the Key risks section renders `[description:1]` inline mid-sentence.
- A **directional glyph contradicts its own word**: `/outcome` renders **"↑ weakened this session"** — an up arrow labelled *weakened*.

## 2 · Why these are one row, and why that matters

Filed together because they are one cause with four faces: **each surface re-states the judgment instead of rendering the one the mechanism holds.** Where the restatement is authored separately — a briefing generator, a masthead, a glyph — it drifts, and nothing detects the drift because nothing requires the surfaces to agree.

The doctrine each face breaks is the same one: **prose may not assert what the mechanism does not make true**, and its visual corollary — R7's up-arrow-labelled-*weakened* is the visual channel asserting what the words deny, the same shape as the "steady this session" sparkline in R4.

Two doctrine anchors are implicated directly, named here as doctrine and **not** as register ids: the **maturity read is never a forecast**, which "very low confidence" breaks by substituting a confidence register for the band ramp; and the **single-hue maturity ramp**, of which `Under review` is not a member at all.

⚠️ **Splitting these into two rows would get the cause fixed twice and the drift detected never.** The closure paths differ, so they are separated in §4 — but the mechanism that keeps them closed is one.

⚠️ **R5 is the surface that leaves the building.** A sponsor reading the briefing receives a different assessment, in a different vocabulary, from the one the owner sees. Of everything in the R2.0 subset, this is the finding a customer encounters first and the owner sees last.

## 3 · Dependency — R6 does not close on this row's own work

**R6 is not independently fixable.** The audit is explicit: the eight openings are re-derivation artifacts of the identity churn, so *fixing B0 fixes this; nothing else does.* R6 closes when B0 closes **and the briefing is re-measured** — not when a briefing-layer change is made.

⚠️ This means R6 must not be marked done by inspecting briefing code. It is a re-measurement obligation sitting on top of another row, and a fix applied here that makes the number look right without B0 landing would be a masking change, not a repair.

## 4 · DONE CONDITION

### Path A — N-7 · one judgment, one word

1. **The judgment has one source.** Every surface that renders the composite reads it from one place rather than restating it. Name that place.
2. **`Under review` is resolved, not translated.** Either it is a real state that belongs in a named vocabulary — in which case say which, and where that vocabulary is defined — or the masthead is corrected to the band word. It may not remain a fifth word outside the ramp.
3. **The briefing uses the band vocabulary.** The band word appears in the briefing; confidence vocabulary does not appear on any surface.
4. **The limiting pillar agrees everywhere.** Masthead, `/outcome` gating chip, `/full-plan` opener and the briefing name the same pillar, measured in one pass on one project.
5. **RED proof.** Re-run R1's own probe — the `OUTCOME INTEGRITY` regex over `innerText` at `/outcome` — and record **one distinct band value** rather than two conflicting values. Repeated rendering of the same value in the masthead and card is allowed. The probe that found the defect is the probe that closes it.

### Path B — N-8 · output states only what the mechanism supports

6. **No raw token reaches prose.** `[description:1]` and any token of its shape are absent from the rendered Key risks section, measured by `innerText` rather than by reading the template.
7. **The glyph agrees with its word.** No directional indicator contradicts the word it labels; `"↑ weakened"` and its family are gone. Prove it in both directions — a genuine improvement still renders an up arrow.
8. **R6 re-measured after B0 lands.** The briefing's "What changed" counts are re-read against the History trail, and every reported opening corresponds to a user act rather than a re-derivation. Cite B0's closure as the dependency.

### Both paths

9. **A mechanism, not a sweep.** Fixing four instances closes four instances. Name what would fail if a fifth surface restated the judgment differently — a shared renderer, a check on the rendered text, a guard — so the next surface cannot drift silently. Without this the row records a cleanup, and the cleanup is what the audit already did once.
10. **Measured on the deployed build**, each result citing its command or observation and the build identity, per N-5.

## 5 · Adjacent, filed as pointers

- **GT-20** — no numeric confidence on any surface — reads ✅ passing, and *"very low confidence"* carries no number, so it does not falsify that row. It sits close enough that the two should be read together when the vocabulary is fixed, rather than one being taken as cover for the other.
- The audit's **colour-encoding finding** — colour encoding pillar identity rather than maturity, so Grounding/Fragile renders green while Adaptability/Fragile renders pink — is the same class of defect as R7's glyph: a visual channel asserting something the words deny. It is recorded as a pointer inside B3 §5 and **still has no row of its own.** It is not covered here.

## Decision

**Surface the provenance OSLO already tracks. Reject the "debt" frame. Escalate inference lineage as a model change.**

---

**1. THE FINDING — OSLO has always known what it made up. It never said so.**

`RELEASE_1_DATA_MODEL_SPECIFICATION` §9 (Context Plane): **`ContextItem.item_type`** is an enum of **six extracted units** — **`claim` · `assumption` · `relationship` · `entity` · `metric` · `interpretation`** — each carrying `extraction_horizon` (`fast`/`deep`), the run that produced it, and:

> **`evidence_id` — NULLABLE.**
> **That nullable foreign key IS the derived-vs-attested distinction, at the data layer.** `evidence_id IS NULL` means **OSLO produced this item from nothing but inference.**

**EI-02 (Alpha, Critical)** already extracts assumptions. **CAF-02 (Alpha, Critical)** already makes **"inference reliance"** a Clarity contributor. **The data exists, in Alpha scope, unsurfaced.**

**Every count in §2 below is a `WHERE` clause. No new object. No new extraction. No new spec.**

---

**2. ADOPT — surface the provenance (Alpha-scoped; reading out existing state).**

**2a. The GROUNDED row becomes claim-level.** *"Your evidence: 12 claims · I inferred: 22"* — **the Reliability qualifier, made countable.** Today Reliability is three band words (Coverage · Evidence · Assessability) with **nothing underneath them.**

**2b. ⭐ LOAD-BEARING INFERENCES — the single most valuable number OSLO can produce.**
`evidence_id IS NULL` **AND** the item supports a **critical issue** or the **limiting dimension**.
> ***"Nine things I made up are holding up your plan."***
**No competitor is in a position to say that sentence.**

**2c. The ASSUMPTION REGISTER** — `item_type='assumption'`, load-bearing first. **The Readout's "Key assumptions" section is currently populated from open CLARIFICATIONS — a proxy. This is the object it was always supposed to read from.** Repoint it.

**2d. Structural counts** — **assumed dependencies** (`relationship` with `evidence_id IS NULL` — *a dependency nobody confirmed is the classic way plans die*) · **unowned entities** · **sourceless metrics** (*"where did 450 come from?"*).

**2e. ⭐ THE INFERENCE MAP — the most valuable new surface available.**
> **The Attention Map shows where the plan is WEAK. An Inference Map shows where OSLO is GUESSING. Different questions. Both matter.**
Seven plan artifacts × their **grounded-vs-inferred proportion**. It produces a finding nothing else in the product can:
> ⛔ **A strong-looking artifact that is 90% inferred is the most dangerous thing in the plan — it looks fine BECAUSE OSLO invented a coherent story. Coherence is not evidence.**
This is **CONF-06 (false confidence) at the ARTIFACT level** — and **more actionable** than the whole-read flag, because it names **exactly which document to go and verify.**

**2f. ⭐ "WHAT I'D NEED TO BE SURE" in the Readout** — the unbacked **load-bearing** items, rendered **as a list of asks**.
> *The single most senior thing a PM can put in front of a sponsor:* **"Here is exactly what I need confirmed, and here is what breaks if it isn't."**

---

**3. ⛔ REJECT the "Understanding Debt" frame (AE-06 is NOT adopted).**

**AE-06** — *"accumulated unresolved ambiguity/assumptions/conflicts"* — is **`Future`**, and canon says *"Defined but explicitly NOT surfaced in Release 1."* **It stays deferred, and the METAPHOR is rejected outright, not merely postponed.**

**3a. "Debt" is a BURNDOWN in a hoodie.** It means something **owed**, something **bad**, something to **pay down to zero**. **D180 banned exactly that grammar from Progress** — *Progress is grounding, not clearing.* Re-admitting it under a new name re-opens the door the doctrine just closed.

**3b. It makes OSLO's CORE FUNCTION a liability.** **PS-01: "construct a usable planning model from incomplete evidence."** **Inference is what OSLO is FOR.** If inference is *debt*, **the product generates liability by doing its job** — a frame that would leak into every surface and quietly indict the thing the user is paying for.

**3c. It is not even true.** **Some assumptions never need validating.** A plan that assumes the sun rises needs no clarification. **Treating every unbacked item as debt manufactures anxiety and noise**, and buries the few items that matter under the many that do not.

> **The DATA is right. The METAPHOR is wrong. Take the useful parts under honest names.**

---

**4. ADOPT the two honest temporal signals (cheap; no new object).**

**4a. AGEING** — *"This assumption has been unvalidated for six weeks, and three issues now depend on it."*
**An assumption raised yesterday and one rotting since week 1 are not the same animal, and OSLO cannot presently tell you which is which.** Timestamps already exist.

**4b. GROUNDING VELOCITY** — *"You grounded 3 claims this week. I inferred 8."*
**A direction, honestly stated — never a target.** Run history already exists. **It is NOT a burndown:** it reports whether understanding is **maturing or stalling**, and a rising inference count alongside a rising band is **correct, not a regression** (D177/D180).

---

**5. ⛔ ESCALATE — INFERENCE CHAINS require a MODEL CHANGE. Do not smuggle them in.**

**The highest-value idea in this decision, and the most expensive.**

If OSLO inferred **A**, then inferred **B from A**, then **C from B**, the plan rests on a **tower of guesses**. **If A is wrong, B and C collapse with it.**
> ***"Your Schedule rests on an inference that rests on an inference."***
**A claim at inference-depth 3 is three guesses away from any evidence — and it will look exactly as confident as one read straight off a document.** **This is invisible today**, and **no other tool is even in a position to try.**

**BUT — the schema does not support it.** `ContextItem` carries `evidence_id` (→ **Evidence**) and `source_attribution` (json). **There is NO `derived_from_context_item_id`.** **Item-to-item lineage is not modelled.**

> **Snapshot provenance is a `WHERE` clause. CHAINS ARE A REAL MODEL CHANGE.**

**Therefore: chains are ESCALATED, not built.** They require **`derived_from` lineage on `ContextItem`**, and that is **a ratified schema decision — never something smuggled in under "we already had AE-06."**

**Sequencing caution (stated, not hidden):** **R1 already carries three blocking items** — the **DL-069 model-judgment eval**, **E1–E3** (DL-105), and the **M4 Reporting spec** (DL-107). **Chains would be a fourth.** **The snapshot counting in §2 delivers roughly 80% of the insight for ~5% of the work.** **Ship §2 and §4, watch what alpha users actually ask for, and let the chain work earn its place.**

## Rationale

The most important question a PM has, before acting on OSLO's read, is not *"how many issues?"* It is **"how much of this did you actually know, and how much did you infer?"** **OSLO can answer that exactly, today, from data it already extracts — and it does not.**

The Reliability qualifier — the product's central epistemic promise — is presented as **three band words with nothing underneath them.** The counts that would justify those words exist in the schema and are never shown.

**AE-06 was deferred for good reasons, and the "debt" metaphor is one of them.** Adopting it would import a burndown frame into a product whose doctrine forbids burndowns, and would indict inference — the thing OSLO is for.

## Conditions

1. **No new object, no new extraction, for §2 and §4.** Anything requiring one is **escalated**, not built (§5).
2. **AE-06 is NOT adopted.** The **accumulated-debt aggregate** stays deferred, and **the metaphor is rejected**, not merely postponed. **No surface may frame inference as a liability, a debt, or a thing to drive to zero.**
3. **No burndown grammar** (D180): no completion %, no bar toward zero, no "N remaining". **A rising inference count alongside a rising band is CORRECT** (D177) — **any guard or surface that treats it as regression is a P1 defect.**
4. **Every count computed from state** (D173). **A count that cannot be computed is not shown, and is never invented.**
5. **Anti-Assumption:** **inference lineage** (`derived_from`) is a **schema decision** and is **owner-open**. **Do not infer it, do not fake it, do not approximate it.**

## Supersedes / Amends

- **Amends** the Progress surface and the GROUNDED row (**D180**) — grounding becomes **claim-level**, and gains **load-bearing inferences**.
- **Amends** `RELEASE_1_REPORTING_SPECIFICATION_V1` — *"Key assumptions"* is repointed from the **clarification proxy** to the **assumption register**; adds *"What I'd need to be sure."*
- **Reaffirms and does NOT adopt AE-06** — Understanding Debt remains **Future**, and the **debt metaphor is rejected on doctrine, not merely on scope**.
- **Reaffirms** EI-02 · CAF-02 (*inference reliance is a Clarity contributor*) · CONF-06 (this extends false-confidence to the **artifact** level) · D173 (true numbers) · **D180** (progress is grounding, not clearing).
- **Opens** a schema decision: **`derived_from` lineage on `ContextItem`** (inference chains).

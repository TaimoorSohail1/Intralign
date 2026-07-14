# The evidence units OSLO already tracks — and what they unlock
2026-07-12 · Owner-directed analysis. **Inventory → usefulness → what becomes possible.**
Grounded in `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1` §9 (Context Plane), **EI-02**, **CAF-02**, **AE-06**.

> ## The finding
> **The data model already carries everything needed. Nothing here requires a new object.**
> `ContextItem.item_type` is an enum of **six extracted unit types**, and `evidence_id` is **nullable** —
> **that nullable foreign key IS the derived-vs-attested distinction, at the data layer.**
> **OSLO has always known what it made up. It just never said so.**

---

## 1. INVENTORY — what is extracted and tracked

### 1a. `Evidence` — the raw inputs
| Field | Values |
|---|---|
| `source_type` | `free_text` · `uploaded_document` · `structured_input` · `imported_content` |
| `provenance` | json |

### 1b. `ContextItem` — the extracted units (**this is the goldmine**)
| Field | Values | What it means |
|---|---|---|
| **`item_type`** | **`claim` · `assumption` · `relationship` · `entity` · `metric` · `interpretation`** | **Six unit types.** |
| **`evidence_id`** | **UUID — NULLABLE** | ⛔ **NULL = OSLO inferred it. There is no evidence behind it.** |
| **`extraction_horizon`** | `fast` · `deep` | Which pass produced it — *the Deep-Pass-found-more story, in the data.* |
| `produced_by_run_id` | FK AnalysisRun | Traceable to the run that created it. |
| `source_attribution` | json | Where it came from. |

**The six units, in plain terms:**

| Unit | What it is |
|---|---|
| **claim** | An assertion the plan makes — a goal, an outcome, a constraint, a commitment. |
| **assumption** | Something taken as true **without evidence**. |
| **relationship** | A dependency or link between two things. |
| **entity** | A stakeholder, vendor, system, team. |
| **metric** | A number or target. |
| **interpretation** | **OSLO's own reading.** Derived by definition. |

**And the epistemic fact that falls straight out of the schema:**
> **`evidence_id IS NULL` ⇒ OSLO produced this from nothing but inference.**
> **Every count below is a `WHERE` clause. No new object. No new extraction. No new spec.**

---

## 2. USEFULNESS — ranked by *"would a PM change a decision because of this?"*

### ⭐ TIER 1 — the numbers that change behaviour

| # | The number | The query | Why it matters |
|---|---|---|---|
| **1** | **Load-bearing inferences** | `evidence_id IS NULL` **AND** the item supports a **critical issue** or the **limiting dimension** | ***"Nine things I made up are holding up your plan."*** **This is the single most valuable number OSLO can produce.** No competitor can say it. |
| **2** | **Unbacked assumptions** | `item_type='assumption' AND evidence_id IS NULL` | *"Things your plan depends on that nobody wrote down."* This is what a steering committee actually needs to hear. |
| **3** | **Inferred claims** | `item_type='claim' AND evidence_id IS NULL` | *"I filled these gaps myself."* **The Reliability qualifier, made countable.** |
| **4** | **Grounded claims** | `item_type='claim' AND evidence_id IS NOT NULL` | *"This much rests on what you actually gave me."* **The honest GROUNDED row.** |

### TIER 2 — structural (the classic project killers)

| # | The number | Why it matters |
|---|---|---|
| **5** | **Assumed dependencies** — `item_type='relationship' AND evidence_id IS NULL` | **A dependency nobody confirmed is the classic way plans die.** OSLO inferred the link; nobody validated it. |
| **6** | **Unowned entities** — an `entity` with no owner claim bound to it | *"Four vendors are named and none has an owner."* |
| **7** | **Sourceless metrics** — `item_type='metric' AND evidence_id IS NULL` | **A target nobody can trace.** *"Where did 450 come from?"* |

### TIER 3 — coverage and provenance

| # | The number | Why it matters |
|---|---|---|
| **8** | **Evidence sources ingested**, by `source_type` | What OSLO actually had to work with. |
| **9** | **Fast vs deep split** (`extraction_horizon`) | *"The deeper read found 14 more."* The D177 payoff, drilled down. |
| **10** | **Interpretations** | Always derived. Should always be visible as such. |

---

## 3. WHAT THIS UNLOCKS — new surfaces, none of which needs a new object

### ⭐ A. **THE INFERENCE MAP** — the most important new surface in the product

> **The Attention Map shows where the plan is WEAK.**
> **An Inference Map shows where OSLO is GUESSING.**
> **They are different, and both matter.**

Plot the **seven plan artifacts × their grounded-vs-inferred proportion**.

**And here is the finding it produces, which nothing else in the product can:**

> ## ⛔ **A strong-looking artifact that is 90% inferred is the most dangerous thing in the plan.**
> **It looks fine *because* OSLO invented a coherent story.** Coherence is not evidence.

That is **CONF-06 (the false-confidence flag) at the artifact level** — and it is arguably more actionable than the whole-read version, because it tells the PM **exactly which document to go and verify.**

### B. **The Assumption Register** — a real surface, not a workaround
Every `item_type='assumption'`, **sorted by load-bearing first**.
*(Today the Readout's "Key assumptions" section is populated from **open clarifications** — a workaround. **This is the object it was always supposed to read from.**)*

### C. **The Dependency Graph** — with the assumed edges marked
`item_type='relationship'`, **unbacked ones drawn distinctly**. *"Four of your dependencies are assumed, not confirmed."*

### D. **Evidence Coverage** — which artifacts rest on which sources
Surfaces **orphan artifacts**: an artifact with **no evidence behind it at all**. Entirely OSLO's construction.

### E. **"What the deeper read found"** — `extraction_horizon='deep'`
The D177 payoff, drilled into. *"Here are the 14 things the Fast Pass missed."*

### F. **For the Readout — the senior move**
Two new sections, both from this data:
- **"What we're assuming"** — from the actual assumption register (not a proxy).
- **⭐ "What I'd need to be sure"** — the **unbacked load-bearing items**, rendered **as a list of asks.**
  > *This is the single most senior thing a PM can put in front of a sponsor:* **"Here is exactly what I need confirmed, and here is what breaks if it isn't."**

---

## 4. ⛔ THE CANON BOUNDARY — an owner call, not an assumption

**`AE-06 Understanding Debt`** — *"accumulated unresolved ambiguity/assumptions/conflicts"* — is **`Future`**, and canon says: ***"Defined but explicitly NOT surfaced in Release 1."***

**The line I would draw:**

| | |
|---|---|
| ✅ **PERMITTED — Alpha-scoped** | **Counting and listing `ContextItem`s that EI-02 already extracts**, and reading the `evidence_id IS NULL` distinction the schema already carries. **This is reading out existing state. No new object, no new concept.** |
| ⛔ **DEFERRED — stays deferred** | **Understanding Debt** as an **accumulated aggregate** — a running "debt" total, a new concept with its own lifecycle. **AE-06. Not R1.** |

**It is close enough to AE-06 that it is the owner's call, not mine.**

---

## 5. Recommendation

**Build in this order:**
1. **The GROUNDED row, claim-level** — *your evidence · inferred · **load-bearing inferences***. It is the Reliability qualifier made countable, and it costs almost nothing.
2. **The Assumption Register** — and repoint the Readout's *"Key assumptions"* at it, replacing the clarification proxy.
3. **⭐ The Inference Map** — *where is OSLO guessing?* **The most valuable new surface available**, and it is the only one that catches **a confident-looking artifact built on nothing.**
4. **"What I'd need to be sure"** in the Readout — the ask list, from the unbacked load-bearing items.

**Everything above is a `WHERE` clause on data OSLO already extracts. Not one new object.**

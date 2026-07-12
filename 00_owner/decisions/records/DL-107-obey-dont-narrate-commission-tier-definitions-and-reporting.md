# DL-107 — Obey the doctrine, don't narrate it — and commission the two specs the repo has cited but never possessed: RELEASE_1_TIER_DEFINITIONS_V1 and RELEASE_1_REPORTING_SPECIFICATION_V1 (M4)

- **Date:** 2026-07-12 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision

Three constituents. **1** is a global product principle. **2** and **3** commission the two specifications the repository has been citing without possessing.

---

**1. OBEY THE DOCTRINE. DON'T NARRATE IT.** *(Global — every surface.)*

> **The doctrine governs what the product may CLAIM and DO. It must NEVER govern how much the product TALKS.**
> **Obey it everywhere. Speak it almost nowhere.**

**The failure, recorded plainly.** Across the R1 prototypes the product **explained its own reasoning to the user** — canon citations (DL-/D-numbers, CR-2, CHG-061, §4c), rationale paragraphs, governance vocabulary, escalation notes, design commentary. The Reports workspace carried *the writing rule quoted at the user*, an essay on why editing is free, and the open-items register. The Plans surface narrated *"the upgrade we deliberately did not build."*

**Cause:** the **"say-it-out-loud test"** — *don't do things you would be embarrassed to explain to a user* — is a constraint on **BEHAVIOUR**. It was misapplied as a **CONTENT REQUIREMENT** — *explain everything*. **They are not the same thing.** Conflating them turned the application into a museum placard about itself. *(AI-authored error, recorded rather than silently corrected.)*

**Binding:**
1. **Default to the content.** The user's work is the surface. Chrome, options and explanation are **not resident** on it.
2. **No meta in product copy.** No canon references, no rationale, no governance vocabulary, no design commentary — **on any surface, including modals.**
3. **Progressive disclosure.** Explanations exist **on demand** (info affordance / hover / "why"), **never resident**.
4. **Bias to simplicity and readability everywhere.**

**What is UNCHANGED:** every behaviour the doctrine requires — every limit, every guard, and every **honest plain-English label** (*"Analysis is behind your edits"* · *"previous analysis"* · *"Comments never change the assessment"* · *"From OSLO"* / *"Confirmed by you"* / *"Attested by \<name\>"* · the limit disclosures · the reliability qualifier). **This decision removes the product's commentary about itself. It removes no honesty.**

*Measured effect on the R1 prototype: user-visible copy **−63%**; the Reports **document** −3%, the **chrome around it −92%**; the Plans surface −81%. **The report was never the problem.***

---

**2. Commission `RELEASE_1_TIER_DEFINITIONS_V1`** (`10_product/strategy/tiering`) — **the single authoritative surface for every per-tier value.**

**~18 canonical documents cite "Release 1 Tier Definitions" for seat, tier and sharing limits. IT WAS NEVER WRITTEN.** The values lived in the **engineering** zone (`RELEASE_1_CALIBRATION_DEFAULTS_V1` §4c) and in a **backlog** item — **invisible to any product-scoped reader, human or machine.**

**The consequence is documented, not hypothetical.** An AI contributor twice proposed numbers canon had already settled — ***"Basic = 10 projects"*** against a ratified **Basic = 3** (UP-3), and ***"Basic's price is undecided"*** against a confirmed **$12/mo**. One reached an open pull request.

> **A reader who cannot find a number will invent one.**

**It is a REGISTER, not a decision.** It **states each value and its STATUS** — **RATIFIED · SUSPENDED** (basis suspended by DL-103, pending re-derivation) **· RETIRED** (kept visible, so it is not re-derived from a blank) **· OPEN** (`TBD`, **do not fill**). **It decides nothing.** *"This is unset"* **is information**, and its absence is what caused the failures above.

**Amendment rule (binding):** **every per-tier value in R1 belongs there.** A number that lives only in an engineering config, a backlog item, or a decision body **will not be found by the people who need it.**

**It records as OPEN, and does not fill:** **collaborator seats** (the one undefined dimension in the ladder — *Basic = 10 would cannibalize a ~$99–149-**per-seat** Team; and CHG-061 is not at risk, because the viral primitives run on unlimited **Viewers** and free **Reviewers**, neither of which consumes a seat*) · **monthly analyses** · **UP-APPLY threshold** · Basic price *basis* · Free CRR ceiling · MON-04 global prompt cap · OD-10 · billing rail · reverse-trial duration.

---

**3. Commission `RELEASE_1_REPORTING_SPECIFICATION_V1`** (`10_product/experience`) — **the M4 surface.**

**"Reporting & Analytics" is a named R1 milestone (M4) with ZERO capability rows and no specification.** SHARE-01…05 are *sharing*; the Export spec explicitly disclaims the role. **The strongest conversion lever in the product existed only as a name.**

**Reporting is a STATUS lever, not a labour one.** A status report — *"60% done, three tasks late"* — makes a PM look like a **clerk**. **PMs will readily distribute a NEW KIND of report if it makes them appear strategic to their stakeholders.** What confers standing is **naming what nobody else has named** — which is **exactly OSLO's existing output**.

> **OSLO's epistemic honesty is what makes the PM look strategic. There is no trade-off between the doctrine and the commercial value — they are the same artifact.**

**Binding content rules:**
- **THE WRITING RULE:** **the doctrine governs what the report may CLAIM; never how it SOUNDS.** The report is an **executive summary in the reader's language**. **ZERO OSLO vocabulary** in the body (mechanically enforced). The honesty appears as **ordinary good writing** — *"80% coverage is sufficient. **This came from the plan, not from Support.**"*
- **TWO ALTITUDES** on every risk — *for the plan* (deliverable impact) and *for the goal* (outcome impact). ⛔ **KNIFE-EDGE:** **outcome impact = "does the plan, AS WRITTEN, still reach its stated intent?"** — a **structural claim**. **NOT "will this project succeed?"** — a **prediction, which doctrine forbids.** **Frame BY outcome; never FORECAST the outcome.**
- **"Plan of action" is the PM's, in first person. OSLO seeds; the PM owns.** *If it reads as OSLO's plan, **the PM becomes a passenger in their own report** and the status lever collapses.* Also the only form compatible with **advisory-only**.
- **Tailor the ASK, never the READ.** §1–§4 identical for every audience; only the decisions section is addressed to the recipient. **Re-framing the assessment by audience is SPIN**, and would destroy the PM's credibility with the very people they are trying to impress.
- **EDITING IS FREE ON EVERY TIER. The gate is REUSE (persistence).** Gating editing is **PROHIBITED**: it would make the PM **sign words they could not correct** — monetizing their credibility in the one artifact where it is on the line — and they would simply export to Word, **stripping the currency marker, the provenance and OSLO's fingerprint**, gating you out of your own viral loop.
- **The disclaimer lives on the PACKAGE, not in the prose.** *A line saying "this isn't a forecast" invites the reader to wonder whether it was trying to be one.* The real protection is that the memo **never makes a forecast claim.**
- **The PM's own prose: a gentle, non-blocking, dismissible note — never a block, never a rewrite.** *Blocking would be **the tool overruling the human** (advisory-only). Silence would be **OSLO lending its name to a claim it forbids itself**.*

**⛔ THE BINDING RISK:** **the PM stakes their own reputation on this, in front of their leadership, under their own name.** A mis-framed claim in a status update is **embarrassing**; **in a board-level strategic read it can end a career.** **Rigorous reliability-qualification is not doctrine — it is protection of the user's reputation, which is what they are buying.**

## Rationale

Two named artifacts that the repository **cited as authoritative but never possessed** have now caused measurable harm: the missing Tier Definitions produced **two invented numbers against settled canon, one of which reached a pull request**; the missing M4 spec left **the strongest lever in the product** unbuilt and unowned. Meanwhile the prototypes had drifted into **narrating the governance to the end user** — an error introduced by instructing builders to *"carry the note in-product."*

**All three are the same failure in different clothes: the boundary between *the governance* and *the product* was not held.** Governance content belongs in canon, where it is findable. **The product should simply obey it.**

## Conditions

1. **No honesty is removed.** Constituent 1 removes the product's **commentary about itself** — never a limit, a guard, or an honest label.
2. **Tier Definitions decides nothing.** It is a **register**. Filling an **OPEN** value requires a decision through Framework 001.
3. **The Reporting spec's content rules are binding**, in particular: **frame by outcome, never forecast it**; **editing free on every tier**; **the note never blocks**.
4. **Anti-Assumption.** Every value marked **OPEN** or **SUSPENDED** stays so. **Do not fill them.**

## Supersedes / Amends

- **Establishes** `RELEASE_1_TIER_DEFINITIONS_V1` — **the single authoritative surface for every per-tier value.** All ~18 citing documents now resolve.
- **Establishes** `RELEASE_1_REPORTING_SPECIFICATION_V1` — the **M4** surface. **Recommends `REP-*` capability rows** (M4 has none).
- **Amends** the presentation of every R1 surface (constituent 1). **Supersedes three earlier "label it in-product" instructions** (the seat-cap *"recommendation"* label · the report *"naming pending"* label · the reverse-trial *"not live in Alpha"* label) — **behaviour unchanged in all three; only the user-facing words move behind an off-by-default reviewer layer.**
- **Reaffirms** DL-102 (CR-2 · D124 · D126 · D128) · DL-103 (never tier judgment quality · §7j) · DL-104 (P1 health-framing) · DL-074 · DL-083 · CHG-061 · the Export spec (*packages, never produces*).

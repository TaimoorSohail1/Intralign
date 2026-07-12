# Release 1 Reporting Specification v1

**Type:** Product Experience Specification — the **M4 Reporting & Analytics** surface
**Status:** Realization of **DL-108** · **Product-authoritative.** · **Date:** 2026-07-12
**Implements (does not redefine):** `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1` *(packages existing understanding; never produces new understanding)* · **DL-102** (D124/D126/D128, CR-2) · **DL-103** §7j · **DL-104** §5 (the **P1 health-framing defect class**) · Confidence · Reliability · CAF · History
**Consistent with:** `RELEASE_1_TIER_DEFINITIONS_V1` (per-tier values)

> **Scope guardrail.** A report **packages existing understanding for a reader outside OSLO**. It **produces no new assessment**, and **generating one runs no analysis**. It introduces no new entities, states or events. All numeric values are **`TBD – Owner Decision Required`**.

---

## 0. The gap this closes

**"Reporting & Analytics" is a named Release 1 milestone (M4) with ZERO capability rows and no specification.** `SHARE-01…05` are *sharing*, not reporting; the Export spec explicitly disclaims the role. **The surface DL-103 §7j identifies as the strongest conversion lever, the best viral surface, and the highest-reputational-risk output in the product existed only as a name.**

---

## 1. Why reporting is a **status** lever, not a labour one

**A status report — *"60% done, three tasks late"* — makes a project manager look like a CLERK.** Every PM produces it; it confers no standing.

**PMs will readily distribute a NEW KIND of report if it makes them appear strategic and high-value to their stakeholders.** What confers standing is **naming what nobody else has named** — and that is precisely what OSLO already knows.

> ### **OSLO's epistemic honesty is what makes the PM look strategic.**
> **There is no trade-off between the doctrine and the commercial value — they are the same artifact.** *"Here is what we know, here is what we are assuming, here is what we have not validated"* is **how senior people talk.**

**A triple lever:** **labour** (a weekly obligation) · **status** (far higher willingness to pay than time-saving) · and **the best viral surface in the product** — the PM sends it to **eight executives**, aiming the passive loop **upward**, at budget holders rather than peers.

---

## 2. ⛔ THE BINDING RISK — the PM stakes their own reputation on this

> **The user puts OSLO's output in front of their leadership, under their own name.**
> A mis-framed claim in a status update is **embarrassing**. **In a board-level strategic read it can end a career.**

**Reports are therefore rigorously reliability-qualified — NOT despite the status goal, but BECAUSE of it.** Overclaiming would detonate in front of the exact people whose opinion the PM is trying to shift.

**Epistemic discipline in reporting is not doctrine. It is protection of the user's reputation — which is what they are buying.**

---

## 3. THE WRITING RULE (governing)

> ## **The doctrine governs what the report may CLAIM. It must NEVER govern how the report SOUNDS.**

**The report is an EXECUTIVE SUMMARY, written for its reader in their language.**

**Prohibited in the report body — ZERO OSLO vocabulary:** *confidence · CAF · Clarity/Alignment/Feasibility (as labels) · reliability · understanding maturity · assessability · plan artifacts · "the read" · Outcome Orchestration.* **Enforce mechanically.**

**The epistemic honesty appears as ORDINARY GOOD WRITING.** Canonical renderings:

| Doctrine | How the report says it |
|---|---|
| **Derived, not attested** | *"80% coverage is sufficient. **This came from the plan, not from Support.**"* |
| **Evidence gap** | *"Not yet confirmed with the landlord."* |
| **Low reliability** | *"Dates without owners are estimates, not commitments."* |
| **Limiting dimension** | *"The weak point is people, not process."* |

**The sponsor now knows exactly how much to trust each claim — and no doctrine was spoken.**

---

## 4. Structure (fixed order)

| § | Section | Note |
|---|---|---|
| **1** | **Summary** | Executive-level. **STANDALONE** — a sponsor who reads only this has the whole picture. |
| **2** | **What's changed since previous week** | *(versus \<date\>)* |
| **3** | **Key risks** | **Before** assumptions. |
| **4** | **Key assumptions** | What the plan rests on that is **unconfirmed**. |
| **5** | **Plan of action** | **The PM's.** See §6. |
| **6** | **Decisions needed from you** | Decision · owner · **what it unblocks**. |
| **7** | **Appendix — per-workstream detail** | For the leads. **The sponsor can skip it.** |

**Currency marker** in the body as plain attribution: *"\<Project\> · plan as of \<date\> · \<PM\>"*.
**The disclaimer lives on the PACKAGE** (PDF cover / share-link metadata) — **never as a paragraph in the prose.** *A line saying "this isn't a forecast" invites the reader to wonder whether it was trying to be one; the real protection is that the memo never makes a forecast claim.*

---

## 5. ⚠️ TWO ALTITUDES — the strategic differentiator

**Every risk is framed at both:**
- **For the plan** — what breaks in schedule/scope (**deliverable impact**).
- **For the goal** — what it means for what the project exists to achieve (**outcome impact**).

*A delay is a schedule problem. A delay that means you miss the thing the project exists for is an **outcome** problem. **Same fact, different altitude** — and knowing which one you are looking at is what separates a senior read from a status update.*

> ### ⛔ **KNIFE-EDGE — binding.**
> **Outcome impact = *"does the plan, AS WRITTEN, still reach its stated intent?"*** — a **structural claim about the plan** (Intent is a plan artifact; it is what Clarity and Alignment are measured against).
> **It is NOT *"will this project succeed?"*** — a **prediction**, which the doctrine forbids.
> **Frame BY outcome. Never FORECAST the outcome.** **Enforce mechanically** (no probability / likelihood / forecast / RAG / readiness language).

---

## 6. §5 "Plan of action" is the PM's — OSLO seeds; the PM owns

> **If that section reads as OSLO's plan, the PM becomes A PASSENGER IN THEIR OWN REPORT — and the status lever collapses.** The sponsor does not think *"my PM is sharp."* They think *"the tool wrote this."*

**OSLO seeds the next steps from its recommendations. The PM edits and owns them**, in first person. This is also the only form compatible with **advisory-only** — OSLO never decides.

**Everything above §5 is OSLO's honest read in plain English. §5 is the PM's judgment.** That division is what makes the artifact **both trustworthy and career-safe**.

### 6a. The PM's own prose — a gentle note, **never a block**
The mechanical guards **exempt the PM's sections — they must** (policing the user's prose would be the tool writing the report again). But a PM may type *"we're 80% likely to hit the date"* and it would ship **under OSLO's mark**.

**OSLO offers a gentle, NON-BLOCKING, DISMISSIBLE note.** e.g. *"Heads up — this reads as a forecast. OSLO doesn't predict outcomes, and this goes out under OSLO's mark."*
- **It never blocks.** Send/export always works.
- **It never edits the PM's words.**
- **The PM may dismiss it and send anyway. Always.**

*Blocking would be **the tool overruling the human** (violates advisory-only). Silence would be **OSLO lending its name to a claim it forbids itself**. The note is the only honest position.*

---

## 7. ⛔ Tailor the ASK, never the READ

**Re-framing the assessment by audience is SPIN** — the *"make me look good by shading the truth"* failure — **and it would destroy the PM's credibility in front of the exact people they are trying to impress.**

- **§6 (decisions needed) IS addressed to the recipient.** ✅
- **§1–§4 are IDENTICAL for every audience.** ❌ **never re-framed.** **Enforce mechanically.**

**One honest read. Many asks.** *(Addressing the document — a `To:` line — is addressing, not re-framing, and is permitted.)*

---

## 8. The surface

**Reporting is a WORKSPACE** — peer to Overview · Attention · Artifacts · Issues · History. **Not a modal.**

**THE READING SURFACE IS SACRED.** **Default view = the report, and only the report.** Controls (Recipient · Sections · Format · Schedule · Export) live in a **slim toolbar / drawer, closed by default**. **No meta, no rationale, no design commentary on the reading surface** (see §11).

**Live composer → dated snapshot.** The composer assembles from **current understanding**; **export produces a DATED SNAPSHOT**, which is what travels. It carries the **currency marker**; a stale one is labelled **"previous analysis"** — never presented as current.

---

## 9. Tiering

| | |
|---|---|
| **Free** | The **read snapshot** — §1–§7, **PDF**, OSLO-marked. **CHG-061: the seed is never gated** — it must travel into an exec's inbox. **Full editing.** |
| **Basic** | The **composable readout** — optional sections, **persistence**, branding, scheduling, all formats. |

### 9a. ⛔ Editing is FREE on every tier. **The gate is REUSE.**
**Gating editing is PROHIBITED.** Two reasons:
1. **It would make the PM sign words they could not correct** — the report goes out **under their name**. Selling back control of it **monetizes their credibility**, in the one artifact where it is on the line.
2. **It is a commercial own-goal.** They would export and edit in Word — **stripping the currency marker, the provenance and OSLO's fingerprint** — and you would be **gating your way out of the viral loop.**

**The gate is PERSISTENCE:** **Free** edits from scratch every time; **Basic** carries standing text, tone, section choices and boilerplate **week to week**. *The readout is a **recurring obligation**. Rewriting the same framing every Friday is the tedium; **not having to** is the product.*

**Scheduled reports MUST re-check currency at send time.** A stale read **says so**. **A scheduled report never quietly ships a stale read as current.**

---

## 10. Hard rules (mechanically enforced)

1. **Zero OSLO vocabulary** in the report body (§3).
2. **No forecast / probability / RAG / readiness / health framing** anywhere (§5). **A report a reader could mistake for a health rating is a P1 defect** (DL-104 §5).
3. **Reliability-qualified in substance** — *derived* never dressed as *attested*.
4. **Currency marker** on every package; stale = **"previous analysis."**
5. **Packages, never produces.** **Generating a report runs NO analysis.**
6. **No fabricated completeness.** If OSLO read only part of the plan, the report **says so**.
7. **§1–§4 invariant across recipients** (§7).
8. **Editing free on every tier** (§9a).
9. **The forecast note never blocks and never rewrites** (§6a).

---

## 11. ⛔ **Obey the doctrine. Don't narrate it.** (DL-109)

> **The doctrine governs what the product may CLAIM and DO. It must NEVER govern how much the product TALKS.**

**No canon references, rationale, governance vocabulary or design commentary in product copy — anywhere.** The user's work is the surface. **Explanations exist on demand (info affordance / hover / "why") — never resident.** *Applies to every surface, not only reporting.*

---

## 12. Out of scope

Approvals · governance publication · audit logs · execution/task reporting · **portfolio analytics** (Team/Enterprise, forward) · **continuous execution monitoring** (Pro+, DL-083, Beta) · delivery infrastructure · document-generation logic · **any new assessment generation**.

## 13. OPEN — `TBD – Owner Decision Required`

| # | Item |
|---|---|
| **R-O1** | **Report names** (glossary / DL-053). **Avoid "status report"** — that is the clerk artifact this feature exists to escape — and anything implying **health** or **readiness**. |
| **R-O2** | **Scheduling** — R1 or fast-follow? |
| **R-O3** | **Branding / white-labelling** — Basic, or Pro+? |
| **R-O4** | **Report length — what gets cut, and who decides.** *(Selection is the value; no truncation rule is invented here.)* |
| **R-O5** | **`REP-*` capability rows** — M4 has none. **Recommended: add them.** |
| **R-O6** | **UP-number for the persistence prompt** (`UP-REPORT`, DL-104 §3). |

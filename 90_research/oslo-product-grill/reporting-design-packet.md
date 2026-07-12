# Slice 10 — Reporting design packet (grill)
2026-07-12 · Designs the M4 surface DL-103 §7j identifies as **the strongest lever in the product**. Owner decisions marked. **No canonical names proposed** (glossary/DL-053).

---

## The design question that matters

**What makes a report *strategic* rather than a data dump?**

A data dump says: *"here are 12 issues."* It makes the PM look like a **clerk**.
A strategic artifact says: *"here are the three things that decide whether this plan works, here's what we don't yet know, and here's what I need from you."* It makes the PM look **senior**.

**The difference is selection and framing, not volume.** So a report must **select and frame** — it cannot merely list. Which gives every OSLO report the same spine, and it's the spine of every good executive memo:

> **So what · How do we know · What now.**

---

## The spine (every report carries it — non-negotiable)

| # | Section | Source in OSLO | Why it's here |
|---|---|---|---|
| **1** | **The read** — one line. Understanding maturity, reliability-qualified. **Never health, readiness, RAG, or probability of success.** | Confidence + Reliability | The "so what" |
| **2** | **What's limiting it** — the limiting CAF dimension and the *specific* reason | Limiting dimension + top issues | Prioritization **with a reason**, not a list |
| **3** | **What we don't know** — the honest unknowns: unvalidated assumptions, open clarifications | Clarification register · derived-vs-attested | **The status-conferring part.** *"Here's what we haven't validated"* is how senior people talk |
| **4** | **What I need from you** — decisions owed, evidence outstanding | Open clarifications + **MRI-07 Understanding Dependencies** | Turns the PM from **reporter** into **agenda-setter** |
| **5** | **How to read this** — reliability basis (Coverage · Evidence · Assessability), analysis-currency marker, the standing disclaimer | Reliability model | **Protects the PM in the room** (see the risk below) |

**Sections 1–5 are always present.** A report without §5 is not shippable.

---

## ⚠️ THE BINDING PRINCIPLE — tailor the ASK, never the READ

A report to the sponsor is not a report to the eng lead. The temptation is **audience-tailoring** — and it is a trap.

> **Re-framing the assessment by audience is spin.** It is the *"make me look good by shading the truth"* failure — and it would destroy the PM's credibility in front of the exact people they are trying to impress.

**The rule:**
- **§4 (what I need from you) is addressed to the recipient.** ✅
- **§1–§3 (the read, the limiter, the unknowns) are IDENTICAL for every audience.** ❌ never re-framed.

**One honest read. Many asks.**

---

## F11.1Q1 — **ONE composable readout, not six report types** *(this revises my own scope brief)*

My earlier brief proposed six report types (alignment read · assumption register · decision brief · maturity narrative · leverage read · reliability disclosure). **Grilling it, that's wrong.**

- **"Leverage read"** is not a report — it **is §2** (what's limiting it).
- **"Reliability disclosure"** is not a report — it **is §5**, and it's in *every* report.
- The remaining three (**alignment · assumptions · decisions**) are not separate artifacts a PM would send separately. **They are sections of one memo.**

*Recommended:* **One report object — a composable readout.** Fixed spine (§1–§5), plus **optional sections the PM includes for the room**:

| Optional section | Content |
|---|---|
| **Alignment** | Where stakeholders hold different definitions of done / scope / success |
| **Assumptions** | What the plan rests on that nobody has validated |
| **How our understanding matured** | The narrative from History — a story of **rigor over time** |
| **Artifact detail** | Per-artifact issues, for a working audience rather than an exec one |

**Fewer objects. Less to name. Less to spec.** And it matches what a PM actually wants: **one artifact they can shape for the room** — while the *read itself* stays fixed (the binding principle above).

---

## F11.2Q1 — Live composer → snapshot artifact

**Export doctrine (ratified):** a package **"packages existing understanding; it never produces new understanding."**

*Recommended:* the readout is a **live composer in-app** (pick sections, see it assemble from current understanding) that produces a **dated snapshot** on export. **The snapshot is what travels.** It carries the **analysis-currency marker**, and a stale one is labeled **"previous analysis"** — never presented as current. **Generating a report runs NO analysis** (already asserted in the Slice-10 build).

---

## F11.3Q1 — Free vs Basic

**CHG-061 guarantees PDF export on Free** — the viral primitive. **The seed is never gated.**

*Recommended:*
- **Free** — the **read snapshot**: spine §1–§5, PDF, OSLO-marked. Enough to travel, enough to carry OSLO's fingerprint into an exec's inbox.
- **Basic** — the **composable readout**: optional sections, branding, scheduling, all export formats.

**The seed is not gated; the depth is.**

---

## F11.4Q1 — Scheduling

*Recommended:* **Basic**, and **R1 if cheap** — a weekly readout is the PM's *recurring obligation*, and automating it is the labour half of the lever. **But a scheduled report must re-check currency**: if the analysis is stale, it says so; it never quietly ships a stale read as current.
**Owner-open:** R1 or fast-follow.

---

## F11.5Q1 — Names

**Not proposed here.** Report names are an **owner/glossary decision** (DL-053 Disambiguation Register). The build labels them descriptively and flags **"naming pending."**
⚠️ **One caution:** avoid *"status report"* — that is the clerk artifact this feature exists to escape. Avoid anything implying **health** or **readiness** (DL-104 P1).

---

## ⚠️ THE BINDING RISK (carried in-product)

> **The PM is putting OSLO's output in front of their leadership, under their own name.**
> A hallucinated or mis-framed claim in a status update is **embarrassing**. **In a board-level strategic read it can end a career.**

**Therefore:** rigorous reliability-qualification is **not doctrinal fussiness — it is protection of the user's reputation, which is what they are buying.** Overclaiming would detonate in front of the exact people whose opinion the PM is trying to shift.

**Hard rules, every report:**
1. **Reliability-qualified throughout**; **derived** (From OSLO) is never dressed as **attested** (Confirmed by you / Attested by \<name\>).
2. **Confidence = understanding maturity. NEVER** health / readiness / RAG / probability of success. **A report a reader could mistake for a health rating is a P1 defect (DL-104 §5).**
3. **Analysis-currency marker** on every package; stale = **"previous analysis."**
4. **Packages, never produces.** No new assessment. **Generating a report runs no analysis.**
5. **No fabricated completeness.** If OSLO read only part of the plan, the report says so.

---

## Recommendation summary (accepted unless overridden)

**F11.1Q1** one composable readout (fixed spine §1–§5 + optional sections) — **not six report types** · **F11.2Q1** live composer → dated snapshot · **F11.3Q1** Free = read snapshot (PDF); Basic = composable + branding + scheduling · **F11.4Q1** scheduling at Basic, R1 if cheap, must re-check currency · **F11.5Q1** names = owner/glossary, build labels descriptively.

**Binding:** *tailor the ask, never the read* · the five hard rules above.

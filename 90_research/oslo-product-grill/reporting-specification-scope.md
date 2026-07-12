# Scoping brief — `RELEASE_1_REPORTING_SPECIFICATION_V1`
2026-07-11 · **Draft scope for owner commissioning.** Not canon. AI authored as scribe; **non-ratifying**.
Fills the M4 gap identified in **DL-103 §7j**.

---

## The gap

**`Reporting & Analytics` is a named R1 milestone (M4) with ZERO capability rows and NO specification.**
- `SHARE-01…05` are **sharing**, not reporting.
- `EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1` **explicitly disclaims the role**: *"not a reporting engine… it **packages** existing understanding; it never **produces** new understanding."*

So the surface DL-103 §7j identifies as **the strongest conversion lever, the best viral surface, and the highest-reputational-risk output in the product** currently exists **only as a name**.

---

## What reporting is for (the strategic premise)

**A status report makes a PM look like a clerk.** *"60% complete, three tasks late"* — every PM produces it; it confers no standing.

**PMs will readily distribute a new kind of report if it makes them appear strategic, smart, and high-value to stakeholders.** What confers standing is **naming what nobody else has named** — and that is precisely what OSLO already knows.

> **OSLO's epistemic honesty is what makes the PM look strategic.** The doctrine and the commercial value are **the same artifact**.

---

## Candidate report types (content, not names)

**Names are an owner/glossary decision (DL-053 Disambiguation Register) and are NOT proposed here.**
Each is a **rendering of existing understanding** for an external audience — **no new assessment is produced**.

| # | Content | Source in OSLO | Why it confers standing |
|---|---|---|---|
| **R-1** | **Alignment read** — where stakeholders hold different definitions of done / scope / success | CAF **Alignment** dimension; issues bound to Alignment | Naming a misalignment **before it explodes** is the single most senior thing a PM can do |
| **R-2** | **Assumption / open-question register** — what this plan rests on that nobody has validated | Clarification requests; derived-vs-attested epistemic classes; unresolved issues | *"Here is what we don't yet know"* is how senior people talk. It looks like rigor, not ignorance |
| **R-3** | **Decision brief** — the decisions the PM needs from leadership, and what each unblocks | Open clarifications + issues blocked awaiting stakeholder review (**MRI-07 Understanding Dependencies**) | Turns the PM from **reporter** into **agenda-setter** |
| **R-4** | **Understanding-maturity narrative** — how understanding evolved, and why | **History** (append-only) + confidence trend + run deltas | A story of **rigor over time**; the antithesis of a snapshot |
| **R-5** | **Leverage read** — the single change that would most improve this plan | Limiting CAF dimension + highest-severity issues + recommendations | Prioritization *with a reason*, not a list |
| **R-6** | **Reliability disclosure** — what this read rests on, and how far it can be trusted | Coverage · Evidence availability · Assessability | **Protects the PM in the room** (see the binding risk below) |

---

## BINDING RISK — the PM stakes their own reputation on this output

**The user is putting OSLO's output in front of their leadership, under their own name.**

> A hallucinated claim in a status update is **embarrassing**.
> A hallucinated claim in a board-level strategic read **can end a career**.

**Therefore reports must be rigorously reliability-qualified — not despite the status goal, but BECAUSE of it.** Overclaiming would detonate in the PM's face in front of the exact people whose opinion they are trying to shift.

**Epistemic discipline in reporting is not doctrine. It is protection of the user's reputation — which is the thing they are actually buying.**

**Non-negotiable, every report:**
1. **Reliability-qualified throughout** — every claim carries its basis; *derived* (From OSLO) is never dressed as *attested* (Confirmed by you / Attested by \<name\>).
2. **Confidence = understanding maturity.** **NEVER** project health, readiness, RAG status, or probability of success. A report that a reader could mistake for a health rating is a **defect**.
3. **Analysis-currency marker** on every package. Stale is labeled **"previous analysis"**, never presented as current.
4. **The standing disclaimer** — this presents *understanding*, not project health or approval.
5. **Packages, never produces.** A report renders existing understanding for a new audience. **It generates no new assessment**, and **only an analysis update changes the read** (D001, D115, DL-096).
6. **No fabricated confidence, no fabricated completeness.** If OSLO only read part of the plan, the report says so.

---

## Tiering (per DL-103 §7j)

| | |
|---|---|
| **Free** | **A shareable artifact is guaranteed** (CHG-061 — PDF export is a viral primitive; the seed is never gated). The read snapshot already carries OSLO's fingerprint and already reaches executives. |
| **Basic** | The **strategic suite** (R-1…R-6), plus **branding** and **scheduling**. |

**The seed is not gated; the depth is.**

---

## Virality note

**This is the best viral surface in the product.** A PM sends a report to **eight executives** — aiming the passive loop (**SHARE-02**) **upward**, landing OSLO's fingerprint in front of **budget holders** rather than peers. It is a strictly better vector than peer invites, and the report is the artifact that carries it.

---

## Explicitly OUT of scope

Approvals · governance publication · audit logs (deferred per the History spec) · execution/task reporting · portfolio analytics (**Team/Enterprise**, forward) · continuous execution monitoring (**Pro+**, DL-083, Beta) · delivery infrastructure · document-generation logic · **any new assessment or finding generation** · **report names** (owner/glossary).

## Open — owner decision required

1. **Report names** (glossary; DL-053 Disambiguation Register).
2. **Which of R-1…R-6 are R1** vs forward.
3. **Scheduling** — is a scheduled/recurring report R1 or a fast-follow?
4. **Branding** — is white-labelling a Basic feature, or Pro+?
5. Whether reporting warrants its **own capability rows (`REP-*`)** in the capability matrix — **recommended: yes**, since M4 is a scoped milestone with none.

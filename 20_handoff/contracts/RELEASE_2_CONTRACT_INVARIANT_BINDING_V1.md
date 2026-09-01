# Release 2 Contract Invariant Binding v1

**Document Type:** Contract binding annex (structure only — supplies an existing specification's §G and §D-14 for R2; defines no new contract shape) · **Status:** **DRAFT · Pending Owner Ratification** · **Date:** 2026-08-31 · **Zone:** `20_handoff/` — co-governed seam (DL-053 filing).

**Subordinate to / must not redefine:** [Implementation Contract Specification v1](IMPLEMENTATION_CONTRACT_SPECIFICATION_V1.md).

> ⚠️ **AI-drafted; AI ratifies nothing.** Unmarked rows are recommendations for the owner to accept, amend or reject. Rows marked **▶ RULED \<date\>** record an owner ruling made on that date — captured here, still routed through Framework 001 (Backlog → Proposal → Review → Decision) to become canon. **AI may analyze, check consistency and recommend; it may never ratify or author canon.**
>
> ⚠️ **This annex adds no field, no section and no lifecycle.** The contract structure — twenty-two required fields, dual positive/negative acceptance, ambiguity handling, human review — is unchanged and governs. This document supplies only **which invariants bind** and **which vocabulary is current** when the contract is for Release 2. **Extend, don't mint.**

---

## §1 — The problem, measured

**Implementation Contract Specification v1 §G binds eleven invariants by name, and every one is Release 1's.** They include *"Recommendation Panel only in Finding context"*, *"Confidence is trust in understanding, never project health/readiness/probability/score"*, and *"Chat and Companion are not destinations"*. §G names no Release 2 invariant, and it does not reference the acceptance register at all.

That is not a documentation gap. §G says a contract **fails** conformance if it omits an applicable invariant, and §D-14 makes the bound set a required field. **So an R2.1 contract authored against the specification as written would bind R1's invariants and carry none of R2's — and still pass conformance.**

The surrounding vocabulary confirms the shape.

MEASURED-BY: `git grep -il "<term>" work/release-cycle-2026-08-30 -- 20_handoff`, 2026-08-31, over the 40 markdown files at the seam.

| vocabulary | files, of 40 |
|---|---|
| "Finding" | 36 |
| "Recommendation" | 31 |
| maturity | 6 |
| load-bearing | 4 |
| Adaptability | 3 |
| Viability | 2 |
| **`Grounded g of N`** | **0** |

The ratified Release 2 reading of grounding appears **nowhere** in the seam that hands work to engineering.

---

## §2 — What this supplies, and what it must not do

**Supplies:** the applicable invariant set for §G, and the current terminology, when a contract's construct belongs to Release 2.

**Must not do**, and a reviewer should reject this document if it does: define APIs, schemas, frameworks, tooling, deployment or styling; add or remove a required contract field; redefine acceptance, ambiguity handling or review; or restate product behaviour that a canonical specification already governs. **Source specs govern.**

---

## §3 — §G's applicable set for Release 2 is the acceptance register, not a prose list

**Recommendation.** For an R2 contract, the bound invariants are the **applicable rows of the acceptance register (`GT-…`)**, cited by id, rather than a list transcribed into this document.

**Why a register and not a list.** §G's own list is the demonstration: it was written once, was correct for Release 1, and has drifted silently ever since because nothing reconciles prose against the guard set. A register has an authority that can be re-run; a prose list has only its author's memory. This is the same correction already applied on the governance side — the rule is not new, only its application here.

MEASURED-BY: register enumeration 2026-08-31 — `GT-01…GT-118` contiguous with zero gaps, plus `GT-A1…GT-A3`; **121 ids**. ⚠️ Every enumeration of the register is reproducible; every *count* claiming completeness found in prose has so far been stale, including one asserting `67+34+18=120` which sums to 119. **Cite ids, never a total.**

Each R2 contract therefore satisfies §D-14 by naming the `GT-` ids applicable to its construct, and those ids appear as **negative acceptance** (must-not-occur) per §H, validated by the bound QA Contract per §L.

---

## §4 — The Release 1 invariant list, adjudicated

**Three rows were RULED by the owner on 2026-08-31; the rest are recommendations.** ⚠️ Anti-Assumption still governs the unruled rows: where the Release 2 position is not established by a ratified record, this document **escalates rather than resolves**.

| §G invariant (R1) | recommendation |
|---|---|
| only reanalysis changes assessment | **KEEP** — unchanged in R2 (*only-reanalysis-resolves*). |
| stale means previous analysis, never current | **KEEP** — unchanged. |
| history append-only | **KEEP** — unchanged. |
| Awareness creates no tasks/obligations | **KEEP**, and R2 sharpens it — ordering acts on actions, never on truth. ⚠️ The decision record for that ruling is **not on the control plane yet**; cite the id only once it lands. |
| Invite/share defines no permission enforcement | **KEEP** — unchanged. |
| no forbidden capabilities | **KEEP** — unchanged. |
| classify before specifying | **KEEP** — unchanged. |
| Export packages existing understanding only | **KEEP the constraint, RESTATE the noun** — "understanding" is retired (§6). The obligation (export packages what is already established; it establishes nothing) is unchanged. |
| Chat and Companion are not destinations | ▶ **RULED 2026-08-31: RETIRE this clause; bind DL-230 instead.** *A deferred capability ships no governed behaviour* is already ratified, is **strictly stronger** — it reaches any deferred capability, not only these two surfaces — and resolves on the control plane today. One binding replaces two, and it generalizes to capabilities not yet named. |
| Recommendation Panel only in Finding context | ▶ **RULED 2026-08-31: CARRY, restated in R2 terms.** The R1 noun goes; the constraint stays — **a proposal is presented only in the context of the finding it resolves.** It is not a surface convention: `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1` is live product canon, so dropping the clause with the panel would let a real honesty constraint lapse silently. Bind the applicable `GT-` ids. |
| Confidence is trust in understanding, never project health/readiness/probability/score | ▶ **RULED 2026-08-31: KEEP THE NEGATIVE HALF ONLY.** Bind *no measure shown may be read as project health, readiness, probability or score.* ⚠️ **The positive half is dropped, not restated** — "Confidence is trust in understanding" contradicts `level ≠ trust` and names a retired term (§6). A restatement would be new canon phrasing and needs its own ratification; an annex may not mint it. |

---

## §5 — Release 2 invariants that must bind

**Recommendation:** these are added to the applicable set for R2 contracts and appear as negative acceptance. Each is stated as the must-not-occur form, because that is the form §H requires.

- **A read is not an execution.** A read that can execute the plan is not a read (DL-238).
- **A deferred capability ships no governed behaviour** (DL-230). A capability recorded as deferred must not perform a governed write, on any surface, in any build a user can reach. ▶ Bound by the 2026-08-31 ruling in §4, replacing the R1 Chat/Companion clause.
- **A proposal appears only in the context of the finding it resolves.** It must not be presented, listed or acted on outside that context. ▶ The R1 clause carried forward by the 2026-08-31 ruling, with the surface noun removed.
- **No measure shown may be read as project health, readiness, probability or score.** ▶ The surviving half of the R1 Confidence clause; its positive half is retired rather than restated (§4).
- **Ordering acts on actions, never on truth.** Ordering must not change what is asserted to be true. ⚠️ **Record pending on the control plane** — this binding may not be cited by id until it lands, and this annex deliberately does not cite it. It is the live instance of §8's last clause.
- **The fixed core is Intent · Constraints · Scope · Requirements** (DL-240). A contract must not introduce a fifth core element or rename one.
- **Maturity is a read, never a forecast.** It must not be presented as a prediction, and it must not be rendered as a red/amber/green judgement — the ramp is single-hue.
- **`level ≠ trust`.** A level must not be presented as a measure of how much the user should trust the reading.
- **Only verification moves grounding.** No other act may move it.
- **Capacity, never judgment quality.** A tier boundary must not degrade the quality of judgement offered; it may only limit capacity.
- **Deep Pass performance is a bound, not an aspiration** — 120s target, 180s P95 (DL-239). A contract must not accept an unbounded pass.

⚠️ Items in this section that do not resolve to a decision record are **proposed bindings**, not canon, and are marked for ratification in §7.

---

## §6 — Terminology: retired → current

Per the Disambiguation Register discipline (DL-053), a retired term in an active document is a defect, not a style choice.

| retired | current | note |
|---|---|---|
| `Understanding` (as the measure) | **`Grounded g of N`** | ⚠️ **Zero occurrences at the seam today.** Grounding is **two measures under two names**; a contract must not collapse them into one number. |
| RAG / red-amber-green maturity | single-hue maturity ramp | the colour carries magnitude, never judgement |

⚠️ **This table is deliberately short.** Extending it is a Disambiguation Register act, not an annex act; entries belong in the canonical glossary and are referenced from here.

---

## §7 — Ambiguities and owner questions (the register this document owes)

▶ **Three of the five were RULED 2026-08-31 and are recorded in §4: the coupling clause carries restated,
the Confidence clause keeps its negative half only, and the Chat/Companion clause is retired in favour
of DL-230.** They are listed here struck rather than deleted, because what a document escalated and how
it was answered is part of its record.

1. ~~Recommendation-Panel-in-Finding-context — superseded or carried?~~ **RULED: carried, restated.**
2. ~~The Confidence invariant's R2 statement.~~ **RULED: negative half only; the positive half is retired, not restated.**
3. ~~Chat/Companion and the stronger deferred-capability form.~~ **RULED: bind DL-230, retire the R1 clause.**
4. **Which §5 bindings need a decision record** before an R2 contract may cite them, and which are already carried by an existing record. ⚠️ **Still open.** Measured 2026-08-31: DL-230, DL-238, DL-239 and DL-240 resolve on the control plane; the ordering ruling does not, and its citation closure needs eleven records that do not exist.
5. **Does an R2 contract bind `GT-` ids only, or also a QA Contract reference** naming the server-side twin that proves each? ⚠️ Relevant because the register currently has **61 ids with no registered twin** (`GT-58…GT-118`), so a contract could bind an invariant nothing can validate.

---

## §8 — Conformance

An R2 Implementation Contract is **incomplete** (§K) and **fails conformance** (§N) if it:

- binds no `GT-` id, or binds one whose applicability is not stated;
- carries an invariant this annex marks **OWNER RULING NEEDED** as though it were settled;
- uses a retired term from §6;
- states positive acceptance without the corresponding negative acceptance (§H is unchanged and governs);
- cites a decision id that resolves to no record.

⚠️ **This annex adds no enforcement of its own.** It states what must be true; whether a checker enforces it is engineering's under the specification's existing boundaries, and is not decided here.

---

> **Reminder:** this document is a recommendation. It becomes canon only via Framework 001 — Backlog → Proposal → **Review** → **Decision** → Change → Changelog — and only on owner ratification.

# PROPOSAL — R2.0-2: the deferred criteria, counted and tranched

**Document Type:** Proposal — supplies the count R2.0-2 deliberately refused to invent, and a tranche shape for owner ruling · **Status:** **RATIFIED 2026-09-02** · **Date:** 2026-09-02 · **Ratified:** 2026-09-02 · **Zone:** `20_handoff/` — co-governed seam.

> ⚠️ **WHAT RATIFICATION COVERS, AND WHAT IT DOES NOT.** **Ratified:** §2's rule that the deferred set is tranched by **requirement, not by id**, with the two straddling pairs carried on the gating side; §3's partition; and §4's iteration-2 / iteration-3 split **as scope**. **Not ratified:** §4's counts as a **capacity** claim — whether 40 RED-proofs fit an iteration is a scheduling question this document does not answer. **Not closed:** B1's coverage gap (§5), which remains escalated. **Not minted:** no criterion is added, removed or retired; R2.0-6's four mints and RB-109's range of record are untouched. **Not made startable:** iteration 3's block B still waits on #290's harness, which is behind the R2 relocation.

> ⚠️ **AI-drafted; AI ratifies nothing.** This document was drafted by AI and **ratified by the owner on 2026-09-02**; that ruling, not the drafting, is what makes it binding. Every count below carries the command that produced it. Where a grouping rests on an existing owner ruling that is said. The items listed as **not** ratified in the banner above were **not** settled by ratification and remain open.

---

## 1 · The number R2.0-2 was scoped to and could not have

R2.0-2 splits the deferred criteria across iterations 2 and 3. Its own correction records why the count was withheld:

> *"'The remaining 113' was derived against 18. #277 marks it for re-derivation against 20 and deliberately refuses to substitute a number: **'inventing the total would be the same failure in a new place.'** R2.0-2 is therefore scoped to a set whose size is not yet established — the split stands as a shape; the count does not."*

**The count is now established: 111 deferred criterion ids.**

```
MEASURED-BY: register enumeration + §4b re-extraction, 2026-09-02
  register            GT-01…GT-118 (118) + GT-A1…GT-A3 (3)          = 121
  non-doctrine        N-1…N-10                                       =  10
  TOTAL                                                              = 131
  production-gating subset, re-extracted from §4b col.1              =  20   (15 GT + 5 N-)
  ⇒ DEFERRED COMPLEMENT                                              = 111   (106 GT + 5 N-)
```

⚠️ **113 was 131 − 18** — the *classified* count, which is the exact error #277 caught. The subset is **20 ids across 17 rows**; three rows carry two ids each.

---

## 2 · ⚠️ The split is by ID, but the work is by REQUIREMENT — and two requirements straddle the gate

§3's table maps each `N-` criterion to its origin. Two map onto register ids, and in both cases the pair is split across the gate:

| requirement | on the GATING side | on the DEFERRED side |
|---|---|---|
| every round-trip has a failure path | **N-4** — in the subset; **ruled a FAIL** for gating (R2.0-10) | **GT-A3** |
| entitlement enforced server-side | **GT-106 · GT-110** — in the subset; *"highest-value unrun check"* | **N-9** |

**Consequences, stated before the remedy:**

1. **111 over-counts the deferred work.** `GT-A3` and `N-9` are not additional criteria; they are two requirements already carried on the gating side.
2. **Worse than the count.** If R2.0 closes on the subset and the complement is deferred, `GT-A3` is scheduled to a later iteration as though unaddressed **while N-4 is a production-blocking FAIL**, and `N-9` is deferred **while GT-106/110 block production**. A requirement would be simultaneously gating and deferred.

★ **This is the next layer of a warning the criteria document already carries.** §4b says *"the count is of criterion IDS, not table rows — the row is a proxy, the id is the subject."* Measured here: **the id is a proxy too. The requirement is the subject.**

▶ **RULED 2026-09-02 — tranche by REQUIREMENT, not by id.** A straddling pair is one requirement; it is carried by its gating twin and is **excluded from the deferred set**, with both ids recorded against it. Nothing that gates production may also be deferred.

⇒ **109 deferred requirements, across 111 ids.** The two numbers differ for a stated reason; neither is wrong.

---

## 3 · The deferred set, partitioned by the work it needs

```
MEASURED-BY: complement partitioned by id range and twin status, 2026-09-02
```

| block | ids | count | the work | basis |
|---|---|---|---|---|
| **A** | `GT-39…GT-50` | **12** | none possible yet — **PENDING-SUBJECT**; the L1/L2 sensitivity engine is their subject | **already ruled** to iteration 3 (R2.0-3, R2.0-7) |
| **B** | `GT-58…GT-118`, minus subset members | **53** | **author a twin, then RED-prove it** | §5: 61 missing twins |
| **C** | `GT-01…GT-38`, minus subset members | **31** | twin exists — **RED-proof only** | §3a |
| **D** | `GT-51…GT-57` | **7** | twin exists — RED-proof only | §3a |
| **E** | `GT-A1 · GT-A2` | **2** | annex criteria | |
| **F** | `N-2 · N-3 · N-6 · N-10` | **4** | performance envelopes and untested surfaces | §3 |
| | | **109** | | |

⚠️⚠️ **TWO DIFFERENT 53s — do not conflate them.** Block **B** is 53 **untwinned** criteria in `GT-58…GT-118`. The **53 active twins** awaiting RED-proof are a different set, living in `GT-01…GT-57` and **including subset members**. They share a number and nothing else. #290's six tranches cover the *active twins*, not block B.

---

## 4 · Recommended tranche split — by kind of work, not by id range

**Recommendation, not a ruling.** The grouping principle is that a tranche should contain one kind of work, because a tranche mixing "author a twin" with "prove an existing twin" cannot be estimated or closed as a unit.

**Iteration 2 — 40 requirements: C + D + E.**
Every one already has a registered twin; the work is RED-proof, the same motion #290's tranche plan establishes for the active set. No authoring. This tranche can begin as soon as the harness is reachable.

**Iteration 3 — 65 requirements: A (12) + B (53).**
A is already ruled here and has no subject to test. B requires authoring 53 twins before any can be proved — the larger job, and it cannot start until #290's harness lands, which is itself behind the R2 relocation (#279/#280).

**F (4) splits on evidence type rather than by iteration:**
- `N-2` (Fast Pass envelope) and `N-3` (Deep Pass 120s / 180s P95) need a **deployed build with instrumentation** — they follow **N-5**, and cannot be evidenced before it.
- `N-6` (every advertised intake format) and `N-10` (accessibility) are **WALK** criteria needing only a reachable build.

⚠️ **Iteration 2's 40 is not a capacity claim.** It is the count of requirements whose work is of one kind. Whether 40 RED-proofs fit an iteration is a scheduling question this proposal does not answer, and T1/T2 already compete for the same two people.

---

## 5 · What this proposal does NOT do

- It does **not** close, mint, or retire any criterion. R2.0-6 already mints four ids and **RB-109's range of record is unsettled**; nothing here adds to the register.
- It does **not** rule on **B1's coverage gap** — no criterion in the subset catches *the finding set changing across re-analyses of an unedited plan*. That is a third instance of the pattern §3 names about N-1 and N-4, and it is escalated separately.
- It does **not** re-open the subset. The 20 gating ids are unchanged.
- It does **not** claim the deferred criteria are safe to defer. **A deferred criterion with no named iteration is PENDING-SUBJECT, which is not a pass** (§2). Naming the iteration is exactly what R2.0-2 owes, and what this proposal supplies for ruling.

---

## 6 · Review — the five outputs

- **Findings.** The deferred count is **111 ids / 109 requirements**, not 113. Two requirements straddle the gate. Two distinct sets both number 53.
- **Concerns.** The straddling pairs mean the id-based split, if ruled as-is, would defer work that is simultaneously production-blocking. Iteration 3's 65 is gated by a harness that is itself behind an unmerged relocation.
- **Dependencies.** #290 (twin harness self-test) → blocked by #279/#280 · N-5 for the F-block performance criteria · R2.0-6's four mints and RB-109's range for any future count.
- **Recommendation.** Adopt §2's requirement-based rule and §4's split; treat §4's counts as scope, not capacity.
- **Status.** ▶ **ADOPTED 2026-09-02** — the recommendation above was ruled as written, and the R2.0-2 deliverable owed at the **2026-09-11** boundary is met by this document. ⚠️ **Met is not finished:** iteration 3's block B cannot start until #290's harness lands, and B1's coverage gap stays open. Naming the iterations was what R2.0-2 owed; doing the work is not.

> **Status of this document:** ratified by the owner on **2026-09-02** through Framework 001 — Backlog → Proposal → **Review** → **Decision** → Change → Changelog — and binding for the R2.0-2 tranche split. Its **unratified items are listed in the banner at the head of this document** and are not settled by that ratification; a reader must not read "RATIFIED" as an answer to them. **AI ratifies nothing.**

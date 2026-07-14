## Decision

**Errata to DL-103.** Corrects residue left by DL-103's own §7c reversal, and closes the canon staleness DL-103 created. **No new product policy is introduced.** Every item below was surfaced by the Slice-10 build attempting to implement DL-103 and finding it self-inconsistent.

**1. Strike the priority/latency lever wherever it survives.**
**DL-103 §7c STRUCK the latency lever** (*"an async product cannot sell speed"*; the one moment latency would bite is the one moment §7b forbids monetizing — *"never interrupt at peak need"*). But it survived in three places, which the implementation could not reconcile:
- **§7e (reverse trial)** lists **"priority queue"** among what a downgrade reclaims. **STRUCK** — a downgrade cannot take back a lever that was never built.
- **§1** and **§5** give **Pro "+ speed/priority."** **STRUCK.** **Pro's differentiator is execution & programme support** (DL-083), **not speed**, and not "a better brain" (§1).
- **No priority queue is to be built at any tier.** **Artificial delay remains PROHIBITED.** The **Fast Pass / 60-second Time-to-First-MRI (DL-046) never queues** — a **product guarantee**, not a lever.
*If a genuine, non-artificial speed dimension is ever wanted (e.g. **dedicated capacity** for very large plans), it is a **capacity** claim, not a **speed** claim, and requires its own clause. It is **not** authorized here.*

**2. Retire UP-1, UP-2 and UP-5 from the source of truth.**
DL-103 §6 retired the **daily fix cap (UP-1)**, the **daily chat cap (UP-2)** and the **deep-runs/day cap (UP-5)** as product limits — but the ratified **UP-\*** taxonomy in `10_product/strategy/tiering/12_freemium_tier_behavior_logic.md` still carries them. **Amend that document:** UP-1, UP-2 and UP-5 are **RETIRED**, marked struck in place (not deleted — the reasoning must remain inspectable). **UP-6 (the monthly analysis budget, expressed in ANALYSES) is the primary limit.** Daily caps persist only as **invisible rate-limits (burst-smoothers), never as product limits.**

**3. Number the two new prompts.**
DL-103 §7d and §7j create prompts with no canon number. Assign them in the UP-\* taxonomy:
- **UP-APPLY** — the **assisted-apply** cap (friction; target Basic). **Binding line carried into the taxonomy:** *the recommendation is **always visible**; only the **assisted apply** is metered; **manual editing is always free**.* At the cap the user still sees the issue and the full recommendation (**what to change and why**), can still edit by hand, and the analysis still runs. **If the cap ever hides the recommendation, it is PROHIBITED** (D126/D128). **Threshold is owner-TBD** — set from Alpha instrumentation, **never** from a cost model; **until that data exists, no cap.**
- **UP-REPORT** — the **reporting** value-moment (target Basic; §7j).

**4. Refresh DL-102 constituent E.**
DL-102 E adopted the §4c daily caps *"unchanged."* **Those caps are retired (item 2) and §4c's numeric basis is suspended by DL-103.** DL-102 E is amended accordingly: its **structural** rules stand unaltered — **never meter the epistemic record** (artifacts uncapped, History never expires), **never sell safety**, **no eviction on downgrade**, **two limits never conflated (D124)** — but its **numeric adoptions are superseded by DL-103.** **CR-2 is untouched and remains load-bearing.**

**5. New P1 defect class — "mistakable for a health rating."**
Per DL-103 §7j, **the PM stakes their own reputation on OSLO's reports, in front of their leadership.** A report a reader could mistake for a **health rating, RAG status, readiness score, or probability of success** is therefore not a copy nit — **it is a P1 defect.** Add it to the QA gate:
- **P1 — Health-framing defect:** any surface (especially a **report** or **export**) that could be read as project health, readiness, RAG, or probability of success. **Confidence is understanding maturity. Always.**
- **P1 — Overclaim defect:** any report claim not **reliability-qualified**, or any **derived** (From OSLO) content presented as **attested** (Confirmed by you / Attested by \<name\>).
**Rationale:** a hallucinated or mis-framed claim in a status update is embarrassing; **in a board-level strategic read it can end a career.** Epistemic discipline in reporting is not doctrine — **it is protection of the user's reputation, which is what they are buying.**

## Rationale

DL-103 reversed its own primary lever mid-flight (latency → labour) and retired three ratified prompts, but did not sweep the consequences through the documents that carry them. The Slice-10 implementation could not satisfy DL-103 as written: **§7c forbids the priority queue that §7e, §1 and §5 still assume.** Canon that contradicts itself is canon that will be resolved by whoever implements it last — which is exactly the failure the governance model exists to prevent.

## Conditions

1. **No new product policy.** This is errata: it strikes residue, sweeps consequences, and numbers what DL-103 created. Anything that looks like a new lever is **not** authorized here.
2. **Epistemic invariants untouched.** Advisory-only · Confidence = understanding maturity · issues close only via an analysis update · the three epistemic classes · **CR-2** · **D124** · **D126** · **D128**.
3. **Anti-Assumption.** The **UP-APPLY threshold**, the **monthly analyses figures** (Free/Basic), the **Basic price basis**, the **report names** (glossary/DL-053), **OD-10's window**, the **Free CRR cost ceiling** and **MON-04's global prompt cap** all remain **owner-open**. **No numbers are set here.**

## Supersedes / Amends

- **Amends DL-103** — strikes the priority/latency residue from **§7e, §1, §5**; numbers **UP-APPLY** and **UP-REPORT**.
- **Amends `12_freemium_tier_behavior_logic.md`** — **UP-1, UP-2, UP-5 RETIRED** (struck in place, not deleted); **UP-6 primary**; **UP-APPLY** and **UP-REPORT** added.
- **Amends DL-102 constituent E** — numeric adoptions superseded by DL-103; **structural rules stand** (never meter the epistemic record · never sell safety · no eviction on downgrade · D124). **CR-2 untouched.**
- **Amends the QA gate** — adds the **P1 health-framing** and **P1 overclaim** defect classes.
- **Reaffirms** DL-046 (Fast Pass never queues — a guarantee, not a lever) · DL-083 (execution monitoring = Pro+) · DL-069 · CHG-061.

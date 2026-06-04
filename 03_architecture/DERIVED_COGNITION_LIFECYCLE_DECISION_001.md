# Derived Cognition Lifecycle Decision 001

**Document Type:** Convergent Architecture Decision (lifecycle of Derived Cognition) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-04

> **Mode:** first-principles, convergent — **one** model, no options. Builds on the (provisionally accepted) Epistemic State Model: Canonical = Attested Assertions · Derived Understanding = OSLO-generated interpretation (non-canonical) · Accepted = deferred · Retain owns canonical knowledge. Authority/Governance/Canonicalization/epistemic-state definitions are **not** revisited except where strictly required. Per `CLAUDE.md`, the owner ratifies.

---

## 0. Convergence Statement (the resolving distinction)

Derived Cognition has **two faces that must not be conflated:**

- **Live Derived Cognition** — the *content* of an interpretation (Finding A, Confidence 82, Recommendation X). It is **non-canonical, recomputable, replaceable.** Owned by Infer/Evaluate/Advise.
- **Cognition History Record** — the *event* that *"OSLO, at time T, under conditions K (Attested-knowledge version, model/rule version, upstream lineage), emitted cognition C."* This is an **Attested Assertion — self-attested by OSLO — and therefore canonical, immutable, append-only.**

**The interpretation is Derived; the record that the interpretation was made is Attested.** This single split lets OSLO preserve the full history of how understanding changed **without** making any *interpretation* canonical — because what is canonical is the **emission event**, never the **claim's correctness.**

---

## Part 1 — What Is Derived Cognition?

**All of the following are Derived Cognition** (none is canonical knowledge; each is OSLO-authored, recomputable). Uniform lifecycle: **Produced → Emitted (history record appended) → Live → Recomputed (replace live, append new record) → never deleted.**

| Cognition | Owner | Lifecycle | Persistence | Replay (derivation) |
|---|---|---|---|---|
| **Findings** | Infer | produce→emit→recompute | live projection + emission history | semantic (interpretive); exact where rule-structural |
| **Issues** | Evaluate | same | same | semantic |
| **Recommendations** | Advise | same | same | **semantic** (many valid phrasings; never exact) |
| **Clarifications** | Advise | same | same | semantic |
| **Confidence** | Evaluate | same | same | exact if formula-derived; else **band-semantic** |
| **Reliability** | Evaluate | same | same | exact if formula; else semantic |
| **CAF** | Evaluate | same | same | band-semantic (formula over AI-assessed inputs) |
| **Outcome Confidence** | Evaluate | same | same | band-semantic (aggregate) |
| **Alignment Assessments** | Infer (structure) + Evaluate (score) | same | same | semantic |
| **Feasibility Assessments** | Infer | same | same | semantic |
| **Risk Assessments** | Infer (risk) + Evaluate (severity) | same | same | semantic |

**The record of every one of these emissions is Attested (exact-replayable); the derivation of each is exact-if-rule / semantic-if-AI.** (Replay detail: Part 3.)

## Part 2 — Historical Truth Test (Day 1 vs Day 180)

Day 1: Finding A / Confidence 82 / Rec X. Day 180 (same evidence, improved model): Finding B / Confidence 63 / Rec Y.

**Architecturally correct answer: C (both) — structured as *current foreground + historical record*, not two co-equal "currents."**

- **Current understanding** = the latest: Finding B / 63 / Rec Y (the live Derived projection).
- **History** = the Day-1 emission record (A / 82 / X) preserved as an **Attested Cognition History Record**, with the **change explained** (what input/model changed; §6).
- **Why not A (latest only):** destroys drift — the very signal Outcome Orchestration exists to surface; and makes "why did it change?" unanswerable.
- **Why not B (original only):** OSLO would present stale understanding as current.
- **Why C and not "two currents":** only one interpretation is *current* (recompute supersedes). The prior is **history**, not a competing present. The user sees today's understanding **and** the auditable trail of how it got there.

## Part 3 — Replay (derived from first principles)

Replay has **two independent axes** — conflating them is the usual error:

**Axis 1 — Record replay ("what did OSLO emit?"):** because a Cognition History Record is an Attested, stored fact, it is **always exactly replayable** — you reproduce the *record verbatim.* This is audit/provenance and is **mandatory for every cognition type.** (You can always show precisely what OSLO said at time T.)

**Axis 2 — Derivation replay ("can we reproduce the cognition from its inputs?"):** depends entirely on the **determinism of the producer:**
- **Rule/deterministic producers** (formula-based confidence/reliability/CAF components, structural findings): **exact** derivation replay — same inputs + same rule version ⇒ identical output.
- **AI-assisted producers** (interpretive findings, issues, recommendations, clarifications, judgmental confidence): **semantic** replay — same inputs + same model version ⇒ **semantically equivalent**, not bit-identical (and for confidence, **band-stable**). Demanding exact replay here is a category error — generative reasoning is not bit-deterministic.

| Cognition | Record replay | Derivation replay |
|---|---|---|
| Findings | exact | semantic (exact if rule-structural) |
| Issues | exact | semantic |
| Recommendations | exact | **semantic** |
| Confidence | exact | exact-if-formula / **band-semantic** |
| CAF | exact | band-semantic |
| Outcome Confidence | exact | band-semantic |

**First-principles rule:** *the record is always exactly replayable (it is Attested); the derivation is exactly replayable only to the degree its producer is deterministic.* Audit relies on Axis 1; reproducibility claims rely on Axis 2 at the producer's determinism tier.

## Part 4 — Retain Boundary

**Answer: A, correctly understood — Retain stores Attested Assertions only — and historical cognition *is* Attested, so it lives in Retain as self-attested emission records.** The apparent A-vs-B dilemma dissolves:

- **In Retain (canonical, Attested):** (i) **evidence-attested** assertions ("source S asserts P"); (ii) **self-attested** Cognition History Records ("OSLO@T emitted C under conditions K"). Both are attestations, both immutable, both append-only.
- **NOT in Retain:** **Live Derived Cognition** — the current interpretation projection. It is non-canonical, recomputable, owned by **Infer/Evaluate/Advise**, and held as a recomputable working state, **not** canonical knowledge.

**Cleanest ownership model:** Retain owns the **canonical record** (evidence attestations + cognition-emission attestations); Infer/Evaluate/Advise own the **live cognition** (recomputable). The history is canonical because *that OSLO said X at T* is a settled fact; the live cognition is non-canonical because *whether X is currently OSLO's best reading* is recomputable. **No new owner; "Retain = Attested" is preserved exactly — emission records are simply Attested-by-OSLO.**

## Part 5 — Outcome Orchestration / Drift

**Best: Option 2 — preserve cognition *snapshots* as append-only emission records (the Cognition History).** Decisive reasoning:

- **Option 4 (recompute everything from evidence) structurally cannot recover historical cognition** — because **drift is exactly the case where the reasoning model changed.** Recomputing today yields *today's* answer, not Day-1's. You cannot reconstruct the past by recomputation precisely when the past differs — which is the only interesting case for drift. **This is the killer argument and the reason history must be preserved, not recomputed.**
- **Option 3 (deltas only)** has no stable base to reconstruct absolute prior state; fragile.
- **Option 1 (preserve *all* cognition continuously)** over-retains (every transient intermediate); wasteful and noisy.
- **Option 2 (snapshots at each emission/recompute that changes a governable output)** is exactly the Cognition History Record stream: append-only, Attested, minimal-yet-sufficient. Drift = a **Derived** computation *over* this canonical history.

So drift detection is supported by **canonical emission history (Retain) + a Derived drift analysis (Infer/Evaluate) computed over it.** History preserved as fact; drift explained as recomputable interpretation.

## Part 6 — User Expectation ("Why did Outcome Confidence drop 84 → 61?")

To answer **what / when / why** unambiguously, the minimum retained history is **two (or more) Cognition History Records**, each capturing:

- **Value + identity** — Outcome Confidence = 84 (record T1); = 61 (record T2).
- **Timestamp** — *when* (T1, T2). Answers **when**.
- **Input Attested-knowledge version** — which evidence/attestations it was computed over. Answers part of **what changed** (new/changed attestations).
- **Model/rule version** — which reasoning version produced it. Answers **what changed** (model drift vs evidence change).
- **Upstream cognition lineage** — which findings/issues fed the score. Answers **why** (which upstream change propagated).

**Minimum retained history:** the append-only Cognition History Records for the affected output **and** its lineage. **Ownership:** Retain (the historical *facts* — Attested emission records); the **causal "why" itself** is a **Derived drift explanation** computed by Infer/Evaluate over that history. **Audit:** each emission record is exactly replayable (Axis 1), so the answer is reconstructable and non-ambiguous: *"Confidence fell because attestation set changed from V to V′ (new conflicting stakeholder input) and model went m→m′; the driving lineage was Finding F whose confidence dropped."*

## Part 7 — Contract Impact (implications only)

- **Package 002 (Retain):** add the **Cognition History Record** as an **Attested (self-attested) object** — append-only, immutable, capturing {output identity, value, timestamp, input-attestation version, model/rule version, upstream lineage}. State invariants: **recompute appends a new record, never mutates/overwrites a prior one**; **live Derived Cognition is not stored as canonical** (only its emission records are). Retain stays *Attested-only.*
- **Observability:** the emission records **are** much of the audit/replay substrate; the Observability contract consumes them; **drift monitoring observes the history stream** (drift-as-feature surfaced, not failed).
- **Replay:** adopt the two-axis model — **record replay = exact for all** (audit), **derivation replay = exact-if-rule / semantic-if-AI** by producer tier.
- **Recompute:** "only recompute changes assessment" is preserved and extended — **recompute replaces the live projection and appends an emission record**; it never edits history.
- **Future waves:** Wave B/C (Infer/Evaluate/Advise) produce Derived Cognition **and** emit history records; Wave E (Disclose) surfaces **current foreground + historical timeline** (the drift narrative, MRI/History surfaces); Observability threads throughout.

## Part 8 — Final Recommendation (single, convergent)

**1. Lifecycle model for Derived Cognition:**
```text
Produced (Infer/Evaluate/Advise compute from current Attested knowledge)
   └─▶ Emitted ──▶ append Cognition History Record (Attested, Retain): {output, value, T, input-version, model-version, lineage}
          └─▶ Live (current Derived projection — non-canonical, recomputable, the "present understanding")
                 └─▶ Recomputed on trigger (Attested change · model change · user action):
                        live projection REPLACED · new history record APPENDED (append-only)
                            └─▶ prior live cognition becomes History (never deleted, never "current")
```

**2. What is retained:** Attested evidence-assertions **+** Attested **Cognition History Records** (the immutable emission trail). *(Canonical, in Retain.)*

**3. What is recomputed:** the **live/current Derived Cognition** (Findings, Issues, Recommendations, Clarifications, Confidence, CAF, Outcome Confidence, Alignment/Feasibility/Risk). *(Non-canonical projection.)*

**4. What is replayable:** **every emission record exactly** (audit, Axis 1); **derivations** exactly-if-rule / semantically-if-AI (Axis 2).

**5. What users see historically:** the **current understanding in the foreground**, plus the **historical timeline** of prior emissions with the **explained drift** (Part 2 = C, structured).

**6. Minimum architecture for drift analysis:** append-only **Cognition History** (Attested emission records carrying input-version + model-version + lineage) **+** a **Derived drift explanation** computed over it **+** **Disclose** timeline surfacing. Nothing more.

**How OSLO understands changes in understanding while Canonical = Attested only:**
Because **the history of cognition is a sequence of Attested facts — "OSLO emitted C at T" — not Derived claims of truth.** The *interpretation* stays Derived (recomputable, non-canonical); the *emission event* is Attested (canonical, immutable). Drift is then a **Derived analysis over a canonical emission history.** OSLO can therefore reconstruct, explain, and visualize exactly how understanding evolved — **without ever canonicalizing an interpretation** — because what it canonicalizes is the **record that the interpretation was made**, never the interpretation's correctness. Canonical remains strictly Attested; understanding-of-change is fully preserved.

---

> ### Proposed Owner Resolution
> **Ratify the convergent Derived Cognition lifecycle:** all listed cognition types are **Derived** (non-canonical), produced/owned by Infer/Evaluate/Advise, recomputable, with the lifecycle Produced → Emitted (append Attested Cognition History Record) → Live → Recomputed (replace live, append record) → never deleted. **Adopt** the canonical/derived split for history: the **live interpretation is Derived**; the **emission event is an Attested (self-attested) Cognition History Record** in Retain — so Retain remains Attested-only. **Adopt** the **two-axis replay** (record = exact always; derivation = exact-if-rule / semantic-if-AI). **Adopt** drift support via append-only Cognition History (Option 2) + a Derived drift explanation, rejecting recompute-from-evidence (Option 4) as structurally unable to recover historical cognition under model drift. **Revise Package 002** to add the Cognition History Record (Attested, append-only, recompute-appends-never-overwrites) and to confirm live Derived Cognition is not canonical.
> **Out of bounds:** no new responsibility is created; the Cognition History Record is an Attested classification of an existing emission, routed to the owner; nothing is adopted unilaterally.

---

*This decision converges the lifecycle of Derived Cognition by distinguishing the live interpretation (Derived: non-canonical, recomputable, owned by Infer/Evaluate/Advise) from the Cognition History Record (the Attested, self-attested event that OSLO emitted a given cognition at a time under stated conditions — canonical, immutable, append-only in Retain). It classifies Findings, Issues, Recommendations, Clarifications, Confidence, Reliability, CAF, Outcome Confidence, and Alignment/Feasibility/Risk assessments all as Derived Cognition with a uniform produce→emit→recompute lifecycle; resolves the Day-1-vs-Day-180 test as "both, structured as current foreground plus explained history" (Option C); derives a two-axis replay model where the emission record is always exactly replayable (audit) while derivation replay is exact only to the degree the producer is deterministic (exact for rule-based, semantic/band for AI-assisted); shows Retain stores Attested only, with cognition history qualifying as Attested self-attested emission records while live Derived cognition stays out of canonical; argues drift must be supported by append-only emission snapshots (Option 2) because recompute-from-evidence (Option 4) structurally cannot recover historical cognition once the reasoning model has drifted; specifies the minimum history to answer a confidence-drop question (emission records carrying value, timestamp, input-attestation version, model/rule version, and upstream lineage, with the causal explanation itself a Derived analysis over canonical history); and identifies Package 002, observability, replay, recompute, and future-wave implications. The single recommendation preserves Canonical = Attested while fully preserving understanding-of-change, because OSLO canonicalizes the record that an interpretation was made — never the interpretation's correctness — making drift a Derived analysis over a canonical emission history. It invents no new responsibility or object and routes all ratification to the owner.*

**Derived Cognition Lifecycle Decision 001 complete.**

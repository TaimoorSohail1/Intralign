# Release 1 Epistemic State Model Decision 001

**Document Type:** Convergent Architecture Decision (epistemic structure of canonical knowledge) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-04

> **Mode:** first-principles, convergent — **one** model, no options. Scope is exclusively the **epistemic states of knowledge inside Retain in Release 1.** Authority/Governance are not revisited except where strictly required. Provisional conclusions assumed: Responsibility Architecture primary · Outcome Governance deferred · integrity controls exist · epistemic labeling exists · canonical ≠ accepted truth. **Proposed terms ("Attested," "Derived") are routed to the owner for ratification.** Per `CLAUDE.md`, the owner ratifies.

---

## 0. Convergence Statement (the whole model in four lines)

1. **Evidence** is the raw source (Perceive).
2. **Attested Assertion** is the only thing that is **canonical** (Retain): *"source S asserts proposition P," re-derivable from S.*
3. **Derived Understanding** (Infer/Evaluate) is OSLO's interpretation — **never canonical**, always recomputable, carried with confidence/conflict.
4. **Accepted** is a fourth state that **does not exist in Release 1** (deferred to the user/Future).

**Canonical = Attested. Interpretation is Derived and is not canonical.** Everything below derives this and shows it is sufficient.

---

## Part 1 — Knowledge Types (reduced; unnecessary categories rejected)

First principle: separate **content type** (what a thing is about) from **epistemic state** (how grounded/settled it is). Most proposed "types" are content or conditions, not epistemic states, and collapse.

| Candidate type | Verdict | Definition / Owner / Persistence / Can be canonical? |
|---|---|---|
| **Evidence** | **KEEP** | Raw source artifact. **Perceive.** Append-only. *Not itself canonical knowledge* — it is the **anchor** attestations point to. |
| Observation | **REJECT** | An extraction event; collapses into Evidence + the attestation it produces. Not a distinct state. |
| Statement | **MERGE → Attested Assertion** | "S said P." Atomic canonical unit. |
| Claim | **MERGE → payload** | The proposition P. The *content* of an Attested Assertion, not a separate state. |
| **Fact** | **MERGE → Attested Assertion** | In OSLO the only "fact" is the **attestation** ("S asserts P"), not the truth of P. So Fact ≡ Attested Assertion. **Retain. Canonical: YES.** |
| **Assumption / Constraint / Dependency** | **KEEP as content sub-types** | Content categories of an assertion. **Canonical ONLY when Attested** (stated in evidence). **Inferred** ones are Derived, not canonical. Owner: Retain (if Attested) / Infer (if inferred). |
| Inference / Interpretation | **MERGE → Derived Understanding** | OSLO-authored reading. **Infer/Evaluate.** Recomputable. **Canonical: NO.** |
| Conflict | **KEEP as a Derived relation** | A detected contradiction among Attested Assertions. **Infer.** Recomputable. **Canonical: NO** (it is understanding *about* canonical items). |
| Ambiguity | **REJECT as a type** | Not an object — an **epistemic-quality condition** (competing Derived interpretations + low confidence). Represented, not stored. |
| Candidate Understanding | **REJECT the name → Derived Understanding** | "Candidate" presupposes a pending acceptance that R1 does not have (see Part 4). |
| Canonical Understanding | **REJECT** | A conflation. There is canonical **knowledge** (Attested) and derived **understanding**; "canonical understanding" fuses two states that must stay distinct. |

**Surviving irreducible set:** **Evidence** (anchor, Perceive) · **Attested Assertion** (canonical unit, Retain; content-typed fact/assumption/constraint/dependency/goal) · **Derived Understanding** (Infer/Evaluate, non-canonical, incl. inferences and conflicts) · an **epistemic-quality overlay** (confidence/reliability/conflict — attributes owned by Evaluate, not states).

## Part 2 — Canonical Knowledge, Defined Operationally

> **Canonical Knowledge** is the **append-only, provenance-bearing record of assertions that are attributable to an identified evidentiary source and re-derivable from that source without OSLO inference.**

**Operational test (an engineer decides "does this belong in Retain?"):**
1. **Attribution** — can OSLO name the specific source (who/where in which artifact) that asserts this? *If no → not canonical.*
2. **Re-derivability** — can the item be reproduced from that source **without OSLO inference/enrichment/judgment**? *If it required OSLO to author it → it is Derived, not canonical.*

Both true ⇒ canonical (Attested). Either false ⇒ **Derived Understanding**, not canonical.

- **What canonical means:** "this assertion exists in this evidence, attributed and re-derivable." A record of *what was asserted.*
- **What canonical does NOT mean:** true · accepted · best · trusted · resolved · or *merely persisted* (Derived is persisted too, yet not canonical).
- **Relationship to truth:** canonical asserts *"S asserts P,"* **not** *"P is true."* The truth of P is never canonical.
- **Relationship to confidence:** canonical items are near-certain **as attestations** (we are sure it was said); meaningful uncertainty attaches to **Derived** interpretations, not to the attestation. (Source *reliability* is a quality attribute on the attestation, distinct from interpretive confidence.)
- **Relationship to ambiguity:** ambiguity never resides in canonical; canonical may hold **multiple competing attested assertions** (each true as an attestation); which one is "right" is Derived.
- **Relationship to acceptance:** orthogonal and **deferred** for **OSLO**. Canonical ≠ accepted *by OSLO*; OSLO never self-accepts. **But the *user* is a third attesting source:** when a user **confirms/authors** a planning item (accepts a recommendation, edits directly, or otherwise commits), that act creates a **user-attested Attested Assertion of the content — a *plan fact*** (canonical, attributed to the user). See the **Plan-Fact Clarification** (owner-directed, 2026-06-04) in `USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001.md` §0.1.

> **Plan-Fact Clarification (owner-directed, 2026-06-04).** "Canonical = Attested" includes a **user-attested** sub-class covering both (a) the **acceptance event** ("U confirmed I at T") and (b) the **confirmed content itself** (a Canonical Fact attributed to the user — the *plan fact*). A confirmed item is **factual in the plan** (the user committed to it); this is **not** a claim of **world-truth** (OSLO never certifies real-world correctness and may still raise an Acceptance-Impact flag on later conflict). **One-way flow is preserved:** OSLO does not promote its Derived recommendation to Attested; rather, a **user act authors a new user-attested fact** whose content may match the recommendation, while OSLO's recommendation object stays Derived/recomputable.

## Part 3 — The Minimum Epistemic States

Derived, not assumed. The minimum set is **three active states + one deferred:**

```text
Evidence ──(Perceive: extract + attribute + readiness)──▶ Attested Assertion ──(Infer/Evaluate: interpret + score)──▶ Derived Understanding
   (raw source)            integrity persistence            (CANONICAL)         recomputable, non-canonical        (Understanding)
                                                                                         │
                                                                              (Accepted) ─┘  ✗ NOT IN R1 (deferred to user/Future)
```

| State | Purpose | Owner | Transition criteria | Persistence rule |
|---|---|---|---|---|
| **Evidence** | hold the raw source as the attestation anchor | **Perceive** | artifact intake + readiness | append-only, immutable, provenance |
| **Attested Assertion** *(canonical)* | record what evidence asserts, attributed & re-derivable | **Retain** | Evidence→Attested: source-attributed + re-derivable + integrity-recorded | append-only, versioned, history-preserving; **admits only Attested** |
| **Derived Understanding** *(non-canonical)* | OSLO's interpretation/inference/conflict over Attested items | **Infer / Evaluate** | computed from Attested knowledge; carries confidence/reliability/conflict | **recomputable projection**; versioned by recompute; **never promoted to Attested** |
| **Accepted** *(deferred)* | trusted-as-true understanding | **User** (Future) | **n/a in R1** | n/a in R1 |

**Key property:** the pipeline flows **one way**; **Derived never flows up into Attested** (no promotion path). That single rule is what keeps interpretation out of canonical.

## Part 4 — Grounded vs Candidate: Challenged and Replaced

1. **True epistemic states?** The **grounding** distinction is real and intrinsic — *Attested* (evidence-authored) vs *Derived* (OSLO-authored). **"Candidate"** is **not** a grounding state; it names a *pending-acceptance* relationship to a future "accepted" — which R1 does not have.
2. **Attributes or states?** Grounding is an **intrinsic state fixed at creation** (a thing is born Attested or Derived). Confidence is an *attribute*. "Grounded/Candidate" blurred a state with a teleological label.
3. **Lifecycle states?** **No.** Nothing transitions Attested↔Derived; grounding is permanent. (Confidence updates via recompute; grounding does not.)
4. **Hidden governance?** **"Candidate" yes** — it implies an eventual promotion-to-accepted, i.e. an acceptance gate = smuggled governance. **"Derived" no** — it has no promotion endpoint.
5. **Necessary?** The **Attested/Derived** distinction is necessary; the **"Grounded/Candidate" naming is not.**

**Decision: reject "Grounded/Candidate"; adopt the grounding distinction Attested vs Derived — with the sharper claim that "canonical" is reserved for Attested and Derived is *non-canonical* (not a second label inside the canonical store).** This supersedes the earlier "two labels inside Retain" proposal: there is **one** canonical epistemic state (Attested); Derived persists as a clearly-demarcated, recomputable, non-canonical projection.

## Part 5 — Ambiguity & Conflict (the three-stakeholder case)

- **Enters Retain (canonical / Attested):** three Attested Assertions — *"A asserts objective = customer satisfaction," "B asserts objective = cost reduction," "C asserts objective = call-volume reduction."* All three are **canonical and coexist without contradiction** — they are three true records of *what was said.*
- **Does NOT enter canonical:** any single resolved *"the objective is X"*; the conflict; the alignment uncertainty.
- **Conflict representation:** a **Derived** conflict (Infer) referencing the three Attested Assertions.
- **Ambiguity representation:** the **epistemic-quality overlay** — competing Derived interpretations + low alignment **confidence** (Evaluate). Represented, never resolved.
- **Can competing interpretations coexist canonically?** The competing **attested assertions** coexist canonically (yes — they are settled facts about what was said). The competing **interpretations** coexist as **Derived** (not canonical).

**Can unresolved understanding become canonical? — NO.** Understanding is Derived; canonical is Attested. The settled fact ("these three things were said") is canonical; the unsettled part ("what the real objective is") remains Derived until **new evidence or user action** changes it. **Who prevents it / by what mechanism:** no actor — a **structural ownership boundary + invariant.** Retain admits only Attested (attributed + re-derivable); Infer/Evaluate own Derived; **no transition promotes Derived → Attested.** Prevention is a law, not a gate.

## Part 6 — Retain Contract (Package 002) Impact

**Implications only — no architecture redesign.**

- **Required revisions:**
  - State the **Canonical = Attested** invariant: Retain admits an item as canonical **only** if it is source-attributed and re-derivable without OSLO inference.
  - Clarify the content objects: **Assumption / Constraint / Dependency are canonical only when Attested**; **inferred** assumptions/constraints/dependencies are **Derived Understanding** (Infer/Evaluate), **not** Retain canonical.
  - Sharpen provenance: every canonical item names its evidentiary source and is re-derivable from it.
- **New invariants:**
  - **Canonical = Attested** (attributed + re-derivable).
  - **Persistence ≠ canonicalization** — Derived may be persisted as a recomputable projection but is **never** canonical and **never** promoted to Attested.
  - **One-way flow** — no Derived → Attested transition.
- **Unnecessary concepts to drop:** the "Candidate" label; any treatment of inferred content as canonical; residual "authorization-to-promote" framing (already reduced to integrity/readiness).
- **Ownership changes:** none new. Derived Understanding is owned by **Infer/Evaluate** (Retain may *persist* it as a demarcated projection but does not own its epistemic content). Retain's canonical ownership is unchanged and *narrowed to Attested.*

## Part 7 — Final Recommendation (single, convergent)

**1. The Release 1 Epistemic State Model:**
```text
Evidence (Perceive)
   └─▶ Attested Assertion (Retain) ── CANONICAL ── content-typed: fact | assumption | constraint | dependency | goal
          └─▶ Derived Understanding (Infer / Evaluate) ── NON-CANONICAL ── inferences, interpretations, conflicts
                 · epistemic-quality overlay (Evaluate): confidence · reliability · conflict
                 · [Accepted] — DEFERRED (user / Future) — absent in R1
```

**2. Canonical Knowledge (definition):** the append-only, provenance-bearing record of assertions **attributable to an identified evidentiary source and re-derivable from it without OSLO inference.** Canonical records *what was asserted*, not what is true, accepted, or best.

**3. Minimum labels/states inside Retain:** exactly **one canonical epistemic state — Attested.** The only label the persistence layer needs is the binary **Attested (canonical) | Derived (non-canonical projection)**, whose sole job is to keep Derived out of the canonical set. Content-typing (fact/assumption/constraint/dependency/goal) is **orthogonal metadata**, not an epistemic state.

**4. The exact mechanism preventing unstable understanding from being mistaken for settled understanding:**
**Structural, not procedural — two parts, no actor and no gate:**
- **(a) The Attested/Derived ownership boundary + one-way-flow invariant:** the canonical store admits *only* Attested assertions (settled-by-construction facts about what evidence asserts); all interpretation is Derived, owned by Infer/Evaluate, recomputable, and can never be promoted into canonical. Unstable understanding is therefore **never inside the canonical set**, so it cannot be read as a canonical fact.
- **(b) The Disclose obligation:** where Derived understanding is surfaced, **Disclose** must present it *as* Derived and *with* its confidence/conflict — so even in the understanding layer, instability is a first-class, visible attribute, never shown as settled.

Uncertainty is preserved **as a property of the data and a duty of disclosure**, not by any acceptance authority — which is why Release 1 needs **no governance** to keep unstable understanding from masquerading as settled.

---

> ### Proposed Owner Resolution
> **Ratify the convergent Release 1 Epistemic State Model:** three active states — **Evidence** (Perceive) → **Attested Assertion** (Retain, *canonical*) → **Derived Understanding** (Infer/Evaluate, *non-canonical, recomputable*) — with **Accepted** deferred to the user/Future and absent in R1. **Adopt** the operational definition **Canonical = Attested** (source-attributed + re-derivable; never true/accepted/best/merely-persisted). **Adopt** the single binary epistemic label **Attested | Derived** (replacing "Grounded/Candidate," which is rejected for smuggling an acceptance teleology). **Revise Package 002** to encode the invariants (Canonical = Attested; persistence ≠ canonicalization; one-way flow; inferred assumptions/constraints/dependencies are Derived). **Adopt the prevention mechanism** as structural (ownership boundary + one-way invariant) plus the Disclose surfacing obligation — no acceptance actor, no governance.
> **Out of bounds:** no new responsibility/object is created; "Attested/Derived" are epistemic classifications of existing objects, routed to the owner; nothing is adopted unilaterally.

---

*This decision converges the Release 1 epistemic structure of canonical knowledge to a single model. It reduces the proposed knowledge types by separating content from epistemic state — rejecting Observation (collapses into Evidence plus its attestation), merging Statement/Claim/Fact into a single Attested Assertion (the only "fact" OSLO holds is the attestation, not the truth of the proposition), keeping Assumption/Constraint/Dependency only as content sub-types that are canonical solely when attested, treating Conflict as a derived relation and Ambiguity as an epistemic-quality condition rather than a stored type, and rejecting both "Candidate Understanding" (teleological) and "Canonical Understanding" (a conflation). It defines Canonical Knowledge operationally as the append-only, provenance-bearing record of assertions attributable to an identified evidentiary source and re-derivable without OSLO inference — recording what was asserted, not what is true, accepted, best, or merely persisted — and specifies its relationships to truth (attestation, not proposition), confidence (near-certain as attestation; uncertainty attaches to derived interpretation), ambiguity (competing attested assertions may coexist; the resolution is derived), and acceptance (deferred). It derives the minimum epistemic states as Evidence → Attested Assertion (canonical) → Derived Understanding (non-canonical, recomputable), with Accepted deferred and absent in R1 and a strict one-way flow that never promotes Derived into Attested. It challenges and replaces the Grounded/Candidate proposal — keeping the intrinsic Attested-vs-Derived grounding distinction (fixed at creation, not a lifecycle, not hidden governance) while rejecting "Candidate" for implying a pending acceptance and reserving "canonical" for Attested alone (Derived being non-canonical rather than a second label inside the store). It resolves the three-stakeholder case as three coexisting canonical attested assertions with the conflict and ambiguity held as derived understanding plus low confidence, concluding that unresolved understanding never becomes canonical, prevented structurally by the ownership boundary and one-way invariant rather than any actor. It identifies the Package 002 implications (Canonical = Attested; persistence ≠ canonicalization; inferred assumptions/constraints/dependencies are Derived; provenance/re-derivability sharpened; no new owner) and gives a single convergent recommendation, including the prevention mechanism as a structural ownership boundary plus a Disclose surfacing obligation, requiring no governance and inventing no new responsibility or object — routing all ratification to the owner.*

**Release 1 Epistemic State Model Decision 001 complete.**

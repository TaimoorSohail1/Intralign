# User Acceptance Event — Impact Analysis 001

**Document Type:** Architecture Impact Analysis (refines DL-043 draft; evaluates the user-acceptance distinction) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-04

> **Mode:** first-principles evaluation of the owner's refinement — *OSLO never performs interpretation acceptance (deferred), but Release 1 may record and reason over **user** acceptance events as project history.* Tested with the same machinery used to defer Authority (truth-vs-attestation; the discretion test). **No concept is adopted unilaterally;** the new object/capability are routed to the owner. Per `CLAUDE.md`, the owner ratifies.

---

## 0. Headline

**The distinction is valid, important, and — critically — it does *not* reopen Authority or governance. It slots in *additively*, exactly as the cost-of-being-wrong asymmetry predicted.** A **user acceptance event** is a **user-attested Attested Assertion** — a *third source class* of attestation alongside evidence-attested and OSLO-self-attested. Recording it is **integrity**; reasoning over it is **Derived Cognition**. Neither is OSLO governance. The four prior conclusions **hold**, with **three additive extensions** and **one new R1 capability** that is explicitly *not* the removed Authority work:

- **Authority:** holds — OSLO-acceptance stays deferred; the **user** is the acceptance authority; OSLO only **records** and **reasons.**
- **Canonicalization / Epistemic State:** holds + extended — **Attested** gains a **user-attested** sub-class; the Epistemic Boundary Invariant is intact (OSLO still never accepts an interpretation as truth).
- **Derived Cognition:** holds + add one type — the **Acceptance-Impact (Reconciliation) Assessment.**
- **Package 003 / Wave D:** **stay removed** (they were OSLO-Authority); a **new, non-governance capability — User Acceptance Recording & Reconciliation — is required** and is *not* Pkg 003/Wave D.

**This is the architecture working as designed:** a genuinely needed acceptance-related capability is added on top of the integrity/disclosure foundation without resurrecting a governance plane or reworking anything.

---

## 0.1 Plan-Fact Clarification (owner-directed, 2026-06-04)

**Sharpening the earlier "the accepted interpretation stays Derived" wording.** When a user **confirms** a planning item — by **accepting a recommendation**, **directly editing/authoring** it, or otherwise **committing** to it — the user acts as an **attesting source**, which creates a **user-attested Attested Assertion of the confirmed content** — a **plan fact**. This plan fact is **canonical** (a Canonical Fact attributed to the **user**, not to OSLO). OSLO "preserves fact from no-fact" precisely here: the **human is the fact-maker**; OSLO records it.

**One confirmation produces two canonical records (plus preserved history):**
1. **User Acceptance Record** — the decision event ("U confirmed item I at T"), version-pinned to what was on screen.
2. **User-attested plan fact** — the **confirmed content itself**, now a Canonical Fact attributed to the user (this is what makes it "factual in the plan").
3. **OSLO's original recommendation stays Derived** in the Cognition History (a recomputable guess; never overwritten).

**Two senses of "factual" — keep distinct (the one guard):**
- **Plan-fact** (user committed → canonical, **user-attested**): **Yes**, the item is factual *in the plan.* OSLO treats it as fact.
- **World-truth** (is it actually correct in reality?): **OSLO never certifies this.** OSLO may still raise an **Acceptance-Impact** flag if new evidence later conflicts with what the user confirmed.

**One-way flow preserved.** Nothing flows Derived → Attested *by OSLO*. Instead, a **user act creates a new user-attested Attested Assertion** (the plan fact), whose content may match a recommendation; OSLO's Derived recommendation object remains Derived. The user — an attesting source — authors a canonical fact; OSLO does not promote its own interpretation. This is the **third attesting source (user)** the Epistemic State Model already admits, now explicitly extended from *acceptance events* to *confirmed content (plan facts)*. **Direct edits** produce a plan fact too (with normal intake provenance), even without a recommendation.

---

## 1. First-Principles: What Is a User Acceptance Event?

Strip the label and ask what it *is.* "User U, at time T, accepted interpretation I (e.g., Recommendation X as emitted at T₁)."

**Apply the truth-vs-attestation test.** The event does **not** assert *"I is correct / resolved / organizational truth."* It asserts *"U accepted I at T."* That is an **attestation of a human decision** — source-attributed (to U), re-derivable from the event record, and silent on I's truth. It is the **same shape** as the two attestations already canonical:

| Attestation | Source | Asserts | Canonical? |
|---|---|---|---|
| Evidence assertion | external stakeholder | "S asserts P" | yes (Attested) |
| Cognition history record | **OSLO** (self) | "OSLO emitted C at T" | yes (Attested, self-attested) |
| **User acceptance event** | **User** | **"U accepted I at T"** | **yes (Attested, user-attested)** |

**Apply the discretion test** (the test that deferred Authority): does OSLO exercise a *per-case judgment*? **No.** OSLO does not *decide* to accept — it **records** that the user did. Pure capture, no OSLO discretion ⇒ **integrity, not governance.** The acceptance *judgment* is the user's (human responsibility, per the refinement and DL-007); OSLO's roles are **record** (integrity) and **reason** (Derived Cognition).

**Conclusion:** a user acceptance event is a **user-attested Attested Assertion**. It is canonical as a *fact about a human decision*, never as a claim of truth.

## 2. Impact on Authority ("Integrity, not Authority")

**Holds. Authority-as-OSLO-governance stays deferred.** The refinement sharpens the boundary rather than crossing it:

- **OSLO acceptance** (deciding an interpretation is organizational truth) = the deferred **Outcome/Agent Governance** (Disposition, Accepted Understanding, Review Request models). **Still out of R1.**
- **User acceptance recording** (capturing that a human accepted something) = **project history**, integrity. **In R1.**

The user is the acceptance authority; OSLO is the **recorder and reasoner**, never the accepter. The Authority *plane* remains **specified but inactive** in R1. **Important guard:** "U accepted X" must never be silently upgraded to "X is organizational truth" — that upgrade is precisely the deferred OSLO-acceptance and must not occur. The acceptance record is a fact about U's decision, bounded to that meaning.

## 3. Impact on Canonicalization / Epistemic State Model

**Holds, additively extended.**

- **Attested gains a third source class — user-attested.** The Epistemic State Model's "Canonical = Attested (source-attributed + re-derivable)" already accommodates it: the source is the user; the record is re-derivable from the acceptance event. No change to the definition — only recognition that *user* joins *evidence* and *OSLO* as attesting sources.
- **The accepted interpretation stays Derived.** Accepting Recommendation X does **not** make X canonical-as-truth; X remains Derived/recomputable. What becomes canonical is the **separate** user-attested record *"U accepted X."* The interpretation and its acceptance are decoupled — which keeps Canonical = Attested clean.
- **Version-pinning (key mechanic).** Because Derived cognition recomputes, the acceptance must reference the **specific emission accepted** — i.e., the **Cognition History Record** (the immutable Attested emission from the Lifecycle decision), not the live projection. *"U accepted Recommendation X **as emitted at T₁ / record R₁.**"* This is why the Cognition History Record is load-bearing infrastructure: **acceptance records point at it.**
- **Epistemic Boundary Invariant intact.** OSLO still never performs epistemic acceptance; it records a human one. Persistence ≠ acceptance still holds — now joined by **acceptance-recording ≠ truth-assertion.**

## 4. Impact on Derived Cognition Lifecycle

**Holds; add one Derived type.** The reconciliation the owner describes — *does a change in evidence/confidence/feasibility/alignment/outcome-confidence affect a previously accepted decision?* — is a **new Derived Cognition type: the Acceptance-Impact (Reconciliation) Assessment.**

- **Owner:** **Infer** (the implication: "accepted decision D, pinned to record R₁, is now misaligned with current understanding") + **Evaluate** (severity/confidence of the impact).
- **Lifecycle:** identical to all Derived Cognition — produced → emitted (appends a Cognition History Record) → recomputed on drift → never deletes prior. Two-axis replay applies unchanged.
- **Mechanic:** reconciliation compares the **version-pinned acceptance** (record R₁ of the accepted item) against the **current** emission; a divergence beyond tolerance raises an **Acceptance-Impact finding** ("you accepted X under conditions that have since drifted"). This is exactly the capability the owner says is otherwise missing — and it is **Derived, recomputable, non-governance.**

## 5. Impact on Package 003 / Wave D Removal

**They stay removed — and this refinement actually *strengthens* their removal while adding a cleaner, non-governance home for disposition.**

- **Pkg 003 (Authority Promotion Authorization)** and **Wave D (Authority/Exposure)** were **OSLO-governance**. User acceptance recording is **not** that. So they remain **out of R1.** ✅
- **But a real R1 capability now needs a home — User Acceptance Recording & Reconciliation —** and it is **not** Pkg 003/Wave D. It spans existing responsibilities, no Authority engine:
  - **Capture** the user's acceptance action → **Perceive** (intake of a user action, parallel to artifact intake).
  - **Record** it as a user-attested Attested Assertion → **Retain** (append-only, references the Cognition History Record).
  - **Reconcile** against drift → **Infer / Evaluate** (the Acceptance-Impact Assessment, §4).
  - **Surface** it → **Disclose** (acceptance history + impact alerts on the timeline/MRI).
- **Reclassification of Classification Decision 001.** That decision mapped "Issue/Recommendation/Clarification **disposition** → Authority Governance Decision (Wave D), with the UI as platform." The refinement gives a **better R1 reading:** in R1, disposition **is a user acceptance event** — attested history (Perceive/Retain) + reconciliation (Infer/Evaluate), **not** an OSLO Governance Decision. This **removes the last vestige of Authority-in-R1** from the disposition workflows and replaces it with attestation + cognition. *(The OSLO-governance form of disposition — system-controlled acceptance into truth — remains the deferred Future model.)*

## 6. New Object (proposed, minimal, owner-ratified)

**User Acceptance Record** — a **user-attested Attested Assertion** capturing:
- **who** (user identity), **when** (timestamp),
- **what was accepted** (reference to the accepted item **and its version** — a **Cognition History Record** for Derived items; an attestation id for Attested items),
- optional **rationale/context** (user-provided).

It is append-only, immutable, canonical (user-attested), and **decoupled** from the accepted Derived item (which stays recomputable). One object, uniform across accepted recommendations / risk assessments / assumptions / clarifications. **This is the minimal addition; it is routed to the owner, not adopted here.** *(It is distinct from — and must not be conflated with — the deferred Disposition / Accepted-Understanding governance objects.)*

## 7. Impact on DL-043 (the consolidated ratification draft)

**The foundation does not collapse; it is refined additively** — which *validates* the cost-of-being-wrong asymmetry argued in `…RECOMMENDATION_001` (acceptance, now needed, is added over the integrity/disclosure foundation at low cost, no rework, no governance plane).

Proposed DL-043 changes:
- **Update Condition 1** to the owner's refined wording: *"Release 1 assumes OSLO never performs interpretation acceptance; acceptance remains a human responsibility. Release 1 **does** record and reason over **user** acceptance events as project history."*
- **Add constituent (G) — User Acceptance Recording & Reconciliation:** user acceptance events are **user-attested Attested records** (Retain), captured by **Perceive**, reconciled by a new Derived **Acceptance-Impact Assessment** (Infer/Evaluate), surfaced by **Disclose**. Authority plane remains inactive; Pkg 003/Wave D remain removed.
- **Affected-artifact updates:**
  - `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001` — note Attested includes a **user-attested** sub-class.
  - `DERIVED_COGNITION_LIFECYCLE_DECISION_001` — add **Acceptance-Impact Assessment** to the Derived catalog.
  - `WAVE_A_CONTRACT_PACKAGE_002` (Retain) — add **User Acceptance Record** (user-attested, append-only, references Cognition History Record).
  - `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001` — reclassify disposition (R1) as user-acceptance attestation + reconciliation, **not** Authority/Wave D.
  - Contract roadmap — add a **User Acceptance & Reconciliation** package (non-governance), distinct from the deferred Authority work; sequence after the Derived-cognition waves (it consumes Cognition History Records).
- **Guard to record:** "U accepted X" is a fact about U's decision; it **must not** be read as "X is organizational truth" (that remains deferred OSLO-acceptance).

---

> ### Proposed Owner Resolution
> **Accept the refinement and update DL-043:** (1) revise the foundational assumption to *OSLO performs no interpretation acceptance; the user does; R1 records and reasons over **user** acceptance events*; (2) add constituent **(G)** User Acceptance Recording & Reconciliation — user-attested Attested records (Perceive capture, Retain record, version-pinned to Cognition History Records) plus a Derived **Acceptance-Impact Assessment** (Infer/Evaluate) and Disclose surfacing; (3) confirm **Authority stays deferred, the Authority plane inactive, and Pkg 003/Wave D removed** — the new capability is **not** governance; (4) ratify the new **User Acceptance Record** object (minimal, distinct from deferred Disposition/Accepted-Understanding); (5) update the Epistemic State Model (user-attested sub-class), the Derived Cognition catalog (Acceptance-Impact), Package 002, the Classification Decision (disposition = user attestation + reconciliation), and the contract roadmap (add a non-governance User Acceptance & Reconciliation package).
> **Guard:** recording "U accepted X" must never upgrade X to organizational truth — that upgrade is the deferred OSLO-acceptance.
> **Out of bounds:** the new object/capability are routed to the owner; nothing is adopted unilaterally; no OSLO Authority engine is introduced.

---

*This analysis evaluates the owner's refinement that Release 1, while never performing OSLO interpretation acceptance, should record and reason over user acceptance events as project history. Applying the truth-vs-attestation and discretion tests, it concludes a user acceptance event is a user-attested Attested Assertion — a third attesting source alongside evidence and OSLO-self-attestation — so recording it is integrity and reasoning over it is Derived Cognition, neither of which is OSLO governance. The four prior conclusions hold with additive extensions: Authority stays deferred (the user is the acceptance authority; OSLO records and reasons; the Authority plane stays inactive; "U accepted X" must never be upgraded to organizational truth); the Epistemic State Model gains a user-attested sub-class while the accepted interpretation stays Derived and acceptance records are version-pinned to immutable Cognition History Records, preserving the Epistemic Boundary Invariant; the Derived Cognition lifecycle gains one type, the Acceptance-Impact (Reconciliation) Assessment owned by Infer/Evaluate, which compares version-pinned acceptances against current understanding to flag drift affecting accepted decisions; and Packages 003 and Wave D stay removed because they were OSLO-governance, while a new non-governance capability — User Acceptance Recording & Reconciliation spanning Perceive (capture), Retain (user-attested record), Infer/Evaluate (reconcile), and Disclose (surface) — is required and reclassifies R1 disposition from an Authority Governance Decision to a user-acceptance attestation plus reconciliation. It proposes a minimal new User Acceptance Record object (distinct from the deferred Disposition/Accepted-Understanding governance objects) and updates DL-043 with a revised acceptance assumption and a new constituent (G), noting the change is additive and validates the cost-of-being-wrong asymmetry. It introduces no OSLO Authority engine and routes all new objects/capabilities to the owner.*

**User Acceptance Event — Impact Analysis 001 complete.**

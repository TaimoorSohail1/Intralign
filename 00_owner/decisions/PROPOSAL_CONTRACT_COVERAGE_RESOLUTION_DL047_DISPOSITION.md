# DL-047 (DISPOSITION) — Release 1 Contract-Coverage Resolution (Synthesis Engine · Interaction/Collaboration · Sub-feature Enumeration)

**Status:** **RATIFIED AS A WHOLE — DL-047 (2026-06-04); applied across architecture/contracts/models/phase plans; CHG-054.** Recommended dispositions adopted (A1 Perceive-extracts; A2 Infer-extension; B1 Chat contract; B2 CRR split; B3 Suggested-Fix suggest-only; C enumerate; D traceability gate). Resolves the findings of `03_architecture/reviews/RELEASE_1_CONTRACT_COVERAGE_AUDIT_002.md` (owner-directed). **Adopts nothing; edits no ratified contract.** Per `CLAUDE.md`, only the owner ratifies. Structured in three parts (A→B→C) in the recommended resolution order; the owner may ratify part-by-part.

> **Why a Decision (not just an amendment):** Part A raises a genuine **architecture question** — whether OSLO's evidence→plan **synthesis/generation** is a behavior of an existing responsibility or needs a named one. That cannot be settled by a contract edit alone; the owner decides. Parts B and C are classification + enumeration that follow once A is set.

---

## Part A — The evidence → plan engine (CRITICAL; settle first, before Phase II/III)

**Capabilities:** `EI-02 Claim Extraction`, `PS-01 Planning Synthesis Engine`, `PS-02 Planning Artifact Generation`, `PS-03 Understanding Evaluation` (all **Alpha / Critical**). Today: unowned/uncontracted; Perceive is contracted as **non-cognitive** and Infer as **Finding-only**, so the "turn documents into a structured, evaluated plan" core falls between them.

### A1. Claim Extraction → evidence-attested assertions
Extraction turns evidence into source-attributed `AttestedAssertion`s (Canonical Fact / Assumption / Constraint / Dependency). These are **evidence-attested** (attributable + re-derivable), i.e. **Attested, not Derived**.
- **Architecture question:** does Perceive perform extraction, or is there a distinct step?
- **Recommended disposition:** **clarify that Perceive's "no cognition" means "no *Derived* cognition (no inference of Findings/assessments)" — Perceive DOES perform source-attributed extraction** of what evidence asserts, producing evidence-attested assertions for Retain. This is the least-churn option (no new responsibility) and is consistent with "evidence-attested = a source asserts P." *Alternative:* a thin named **Interpret/Extract** step between Perceive and Retain. **Owner chooses.**

### A2. Planning Synthesis + Generation → Derived synthesized model
OSLO **generates** Intent/Context/Scope/Requirements/WBS/Resources/Schedule artifacts from the extracted claims; they are **OSLO-interpreted and user-editable** → therefore **Derived Cognition** (recomputable, history-tracked, never canonical-as-truth) — exactly like Findings/Issues.
- **Architecture question:** generation has no home today (Advise generates candidate *responses*, not plan artifacts).
- **Recommended disposition:** model generated planning artifacts as a **Derived output type** produced by a **Synthesize activity**, fitting the ratified Derived Cognition Lifecycle (Derived · recompute-appends-CHR · two-axis replay · never promoted to Attested). **Owner chooses the home:**
  - **(Option 1, recommended) Extend Infer** — Infer already turns Attested content into Derived cognition (Findings); add "synthesized planning model" as a second Derived output of Infer. *No new responsibility.*
  - **(Option 2) A named `Synthesize` responsibility** between Retain and Infer — cleaner separation, but introduces a responsibility (a bigger architectural change DL-043 deliberately avoided).
- **PS-03 Understanding Evaluation** then slots into **Evaluate** (seed initial CAF/Confidence from the synthesized model) — its input becomes contracted once A2 is set.

### A3. New contract on ratification
Generate a contract set — **`IC/QA/OBS-WS-SYNTHESIS`** (a new wave, e.g. **Wave A.5 "Synthesis"** between Retain and Wave B, or folded into Wave B per Option 1) — covering: extraction (A1), synthesis/generation as Derived (A2), seeding Evaluate (A3). Build order: **after Wave A backbone, before/with Wave B**. Update the Cognitive Responsibility spec, Object Model (add `PlanningArtifact` Derived type + `SynthesizedModel`), Behavior Model, Inventory, and the phase plans (new sub-phase).

---

## Part B — Interaction / collaboration capabilities (classify: contract / commodity / defer)

For each: the matrix marks it **Alpha (R1)**; silence today = ambiguous. Recommended dispositions:

### B1. `CHAT-01…04` OSLO Chat (High) — **recommend: R1, CONTRACT**
Chat is *interactive cognition* central to the product ("reason with OSLO"). Model it as a **Disclose-class interaction surface** that **consumes** existing cognition (Explain/Clarify) and can **trigger** cognition (Improve → routes through Advise + Deep Pass) but **generates no canonical content itself**. Add to the Wave E Disclose contract (or a thin Wave "Interact"). Negative tests: Chat must not write canonical, must not self-accept, must not bypass recompute.

### B2. `CRR-01…05` CAF Review Requests (High) — **recommend: R1, SPLIT (contract the cognitive seam; classify the workflow UI as commodity)**
The cognitive seam — **stakeholder response becomes evidence → triggers Deep Pass (CRR-04)** — is a Perceive-intake + recompute behavior and **should be contracted**. The surrounding workflow (create request, package, status UI, notifications) is **Category E commodity** (DL-043 J) — UX-spec'd, not cognition-contracted. *Alternative:* defer all of CRR to fast-follow if R1 scope is pressured (owner scope call).

### B3. `REC-04` Suggested Fixes (High) + `REC-05` Validation Recommendations — **recommend: Advise + commodity application (no autonomous write)**
- **REC-05** is a Recommendation *type* → enumerate it in the **Advise** contract (light).
- **REC-04** "apply a fix to an artifact": the **suggestion** is Advise (candidate); the **application is a user-initiated artifact edit** (commodity editing) that then triggers recompute. **OSLO must not autonomously write to the artifact** (consistent with no-Authority / no-autonomous-action in R1). The daily-allowance gate is commodity (MON). Contract the suggestion; classify the application as user-action commodity; add a negative test: *no OSLO-autonomous artifact write.*

---

## Part C — Sub-feature enumeration (fold into existing contracts; light, after A/B)

Enumerate these named capabilities as obligations in the contracts that already own their responsibility (they have ratified UX specs — this is *naming*, not new scope):
- **`CONF-06` False-Confidence Detection** → Wave B Evaluate (QA: detect high-confidence-on-inaccurate-understanding; the "dangerous 4th state").
- **`AE-04` Understanding State Model** (Initial→…→Mature) + **`AE-05` Progressive Disclosure** → Wave B obligation + Wave E presentation (extends DL-046 confidence_stage).
- **`MRI-04/05/06/07`** Heatmap · CAF Triangle · Understanding Timeline · Understanding Dependencies → enumerate in the **Wave E** Disclose contract's MRI surface obligations.
- **`AW-04/05`** Assisted Editing · Persistent Intelligence Layer → Wave E Disclose-during-edit obligations (AW-04 routes to B1 Chat / B3 Suggested Fix).

---

## Part D — Prevent recurrence (structural)

Add a **capability-to-contract traceability gate** to the Contract Generation Framework (§E): every `OSLO_CAPABILITY_MATRIX_V2` **Alpha** capability must reference an owning contract (or an explicit commodity/defer classification). CI can assert it. This stops the next Fast/Deep before it reaches the build.

---

## Disposition / conditions
- **Disposition:** *(owner to record per part)*
- **No architecture is changed by this draft;** Part A *proposes* an architecture decision (A2 Option 1 vs 2 / A1 Perceive-extends vs new step) for owner choice; B/C are classification + enumeration.
- **Supersedes:** Nothing. Extends the DL-043/044/046 contract foundation by closing cognitive coverage gaps.

## Owner decision required
- [ ] **A1:** Perceive performs extraction *(rec)* — or a distinct Extract step.
- [ ] **A2:** Synthesis as **Derived**, owned by **Infer-extension** *(rec)* — or a new `Synthesize` responsibility. Then authorize the `WS-SYNTHESIS` contract + model/phase updates.
- [ ] **B1:** Chat → R1 contract *(rec)* / commodity / defer.
- [ ] **B2:** CRR → contract the response→Deep-Pass seam + commodity UI *(rec)* / defer all.
- [ ] **B3:** Suggested Fixes → Advise-suggest + commodity-apply, no autonomous write *(rec)*; enumerate REC-05 in Advise.
- [ ] **C:** Authorize the §C enumeration amendments.
- [ ] **D:** Adopt the capability→contract traceability gate.
- [ ] On ratification: generate/extend the contracts, update architecture spec + object/behavior models + inventory + phase plans, re-run conformance, record DL-047 + changelog.

---
*This draft consolidates the resolution of Contract Coverage Audit 002 into one owner-ratifiable decision in three parts: (A) the Critical evidence→plan engine — recommending Perceive perform source-attributed claim extraction (Attested) and planning synthesis/generation be modeled as Derived cognition owned by an extended Infer (or a new Synthesize responsibility, owner's choice), producing a new WS-SYNTHESIS contract before Wave B; (B) classification of OSLO Chat (contract), CAF Review Requests (contract the response→Deep-Pass seam, commodity workflow UI), and Suggested Fixes/Validation Recommendations (Advise-suggest + commodity user-applied edit, no autonomous OSLO write); (C) enumeration of named sub-capabilities (False-Confidence Detection, Understanding State Model, Progressive Disclosure, MRI components, assisted editing) into the existing Wave B/E contracts; and (D) a capability-to-contract traceability gate to prevent recurrence. It edits no ratified contract, flags the genuine architecture choices for the owner, and routes ratification and application to the owner.*

**DL-047 (DRAFT) — Release 1 Contract-Coverage Resolution prepared. Pending Owner Ratification.**

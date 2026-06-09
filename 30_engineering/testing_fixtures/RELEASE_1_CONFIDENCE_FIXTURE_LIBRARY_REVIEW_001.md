# Confidence Fixture Library Specification — Governance Review 001

**Type:** Governance review of proposed enhancements (recommendations only — nothing applied)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Subject:** `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md`
**Evaluated against:** the subject document + its authoritative stack (Doctrine/Interpretation/Leadership/Calibration 001 · Confidence/CAF/Reliability v2 · Confidence Subsystem Test Spec).

> Review only. **No** doctrine, calibration, implementation guidance, fixture content, or scope expansion is created. Each recommendation is assessed **solely** for consistency with existing doctrine, calibration, model, testing, and fixture-library principles. Proposed revisions are **drafts pending owner ratification** — not applied to the subject document.

---

## Recommendation 1 — Fixture Minimality Principle

### Finding
**Partially Supported** (consistent and additive, but partially implied already).

### Analysis
Minimality is **already implied** but never stated as a principle: §3 frames fixtures as *controlled* scenarios that trade realism for "control and repeatability"; §5 defines a fixture's Purpose as "the **specific** doctrinal behavior it exists to exercise" (singular); §6 requires deterministic/explainable/traceable fixtures. The recommendation **names** that implicit intent and adds a useful authoring discipline (avoid unrelated complexity that obscures attribution/explainability/determinism/replay/traceability). It introduces **no new doctrine** — it is a fixture-authoring principle, not a subsystem-meaning claim. It would **improve** attribution and determinism by discouraging incidental complexity.

On "should it be elevated to a conformance requirement?" — **no.** "Minimality" is partly subjective; as a hard gate it would invite disputes (see Rec 4). It belongs as a **principle**, not a conformance rule.

### Risks
If over-enforced as a gate: subjective rejections and reviewer disputes. If written as a heavy standalone section: redundancy with §3/§5/§6.

### Recommendation
**Accept with Modification** — add as a short **principle** under §3 (Fixture Philosophy), not as a conformance rule and not as a heavyweight new section.

### Proposed Revision *(draft — append to §3)*
> **Fixture Minimality (principle).** A fixture should contain **only** the information required to exercise its intended doctrinal behavior. **Single-behavior fixtures are preferred.** Composite fixtures are permitted **only when the interaction itself is the behavior being tested** (see Fixture Composition). Authors avoid unrelated complexity that would obscure attribution, explainability, determinism, replayability, or traceability. *(Principle, not a conformance gate; minimality is not adjudicated numerically.)*

---

## Recommendation 2 — Fixture Composition Principles

### Finding
**Supported** (formalizes behavior already implicitly present; protects existing invariants).

### Analysis
Composition is **already implicitly allowed and used**: §4's Conflict family is defined to "drive Alignment reduction **and** Deep-pass decreases"; §10's Fast/Deep family exercises "**All three** v2 models." A **Primary** notion already exists implicitly (§5 "Fixture Purpose"; §10 "Primary model exercised / Primary test areas"). The recommendation **formalizes** this with a Primary/optional-Secondary distinction and — importantly — keeps **attribution, explainability, and traceability intact** for composite fixtures, which directly protects the test spec's attribution/explainability requirements (EXPL-T6, INV-T2). It improves **scalability**: as the library grows, composite fixtures need an explicit rule to remain attributable. Governance burden is **minor** (one structural field).

The one alignment need: it touches §5, whose "Fixture Purpose" is currently singular. Adopting composition should clarify §5 to "**Primary Purpose** (+ optional **Secondary Purposes**)."

### Risks
Minor structure-field addition (Primary/Secondary) touching §5. If Secondary purposes were made mandatory, slight authoring overhead — avoid by keeping Secondary **optional**.

### Recommendation
**Accept with Modification** — add a short **Fixture Composition** subsection and align §5's "Fixture Purpose" to "Primary Purpose (+ optional Secondary Purposes)." Keep it tight; do not expand scope.

### Proposed Revision *(draft — new short subsection after §5, + a one-line §5 edit)*
> **Fixture Composition.** A fixture **may** exercise multiple behaviors. When it does: exactly **one** behavior is its **Primary Purpose**; additional behaviors **may** be recorded as **Secondary Purposes** (optional). A composite fixture **must keep attribution, explainability, and traceability intact** — it must never make it impossible to determine **why** a model state changed. Composite fixtures are used **only** where the interaction is the behavior under test (per Fixture Minimality).
> *§5 edit:* rename the **Fixture Purpose** component to **Primary Purpose**, with an optional **Secondary Purposes** component.

---

## Recommendation 3 — New Conformance Rule FC-9 (Composition Integrity)

### Finding
**Redundant** (already covered by existing conformance rules).

### Analysis
FC-9 would require composite fixtures to "preserve attribution, explainability, determinism, and traceability." But those are **already conformance rules for every fixture**: **FC-2** (traceable), **FC-3** (deterministic), **FC-4** (explainable, no opaque fixture), reinforced by §12. A composite fixture is still a fixture, so FC-2/FC-3/FC-4 already bind it. A new FC-9 would **duplicate** existing rules, creating ambiguity about which governs and inviting rule proliferation. It does **not materially strengthen** the framework.

### Risks
Duplicate/overlapping conformance rules reduce clarity and create governance ambiguity (two rules covering the same obligation).

### Recommendation
**Reject** as a new numbered rule. If composition is adopted (Rec 2), the *intent* is best captured as a **one-line clarifying clause** that the existing FC-2/FC-3/FC-4 apply to composite fixtures — not a new rule.

### Proposed Revision *(only if a clarifying clause is desired — not a new FC rule)*
> *(Clause appended to §14, FC-4):* "These conformance rules (FC-2/FC-3/FC-4) apply **equally to composite fixtures**; a composite fixture that obscures attribution or explainability fails FC-4."

---

## Recommendation 4 — New Conformance Rule FC-10 (Minimality)

### Finding
**Partially Supported** as a principle; **Unsupported** as a conformance rule.

### Analysis
The minimality *idea* is sound (Rec 1). As a **conformance rule**, "avoid unnecessary complexity" is **not objectively enforceable** — "unnecessary" is subjective, and a binding gate would create governance disputes and risk arbitrarily blocking valid fixtures (the recommendation's own review question raises exactly this). Conformance rules in this framework are **structural and objective** (classified, traceable, deterministic, explainable, fully-structured, doctrine-valid, covered, append-only); a subjective minimality gate would break that property.

### Risks
Subjective conformance failures; reviewer disputes; inconsistent adjudication; potential to block legitimate composite fixtures.

### Recommendation
**Reject** as a conformance rule (FC-10). The minimality intent is **already captured** as a principle via Rec 1 — that is the correct home for it.

### Proposed Revision
None (covered by Rec 1's principle; no FC-10 added).

---

## Final Assessment

**1. Should the Fixture Library Specification be modified?**
**Yes — minimally and additively.** Two small, governance-safe refinements (Recs 1 & 2) improve clarity on composite fixtures and authoring discipline without expanding scope or adding numerics. The spec is **not** deficient; these are clarity improvements, not gap-fills.

**2. Which recommendations should be adopted?**
- **Rec 1 — Accept with Modification** (add as a §3 principle, not a gate).
- **Rec 2 — Accept with Modification** (add a short Composition subsection; clarify §5 to Primary + optional Secondary).
- **Rec 3 — Reject** as a new FC rule (redundant with FC-2/FC-3/FC-4); optional one-line clarifying clause only.
- **Rec 4 — Reject** as a conformance rule (subjective/unenforceable); its intent lives in Rec 1.

**3. Which should remain review notes rather than specification content?**
- **Rec 3 and Rec 4** remain **review notes** — they do not become new numbered conformance rules. (Rec 3's intent may, at most, be a one-line clarifying clause under existing FC-4; Rec 4's intent is satisfied by Rec 1's principle.)
- **Rec 1 and Rec 2** become **specification content** (a principle + a composition subsection).

**4. Overall quality score (qualitative).**
- **Before changes:** **Strong / ratifiable.** The framework is complete, well-traced (bidirectional, FC-7 coverage), append-only, and consistent with the stack; its only soft spot is leaving composite-fixture handling implicit.
- **After adopting Recs 1 & 2:** **Stronger.** Composite fixtures and authoring minimality become explicit and attribution-protected, closing the one ambiguity — without adding rules, numerics, or scope. (Adopting Recs 3 & 4 would have *lowered* quality via redundancy and subjectivity.)

**5. Ready for ratification, or revise first?**
**Ready for ratification.** The document is ratifiable as-is. **Recommended:** fold Recs 1 & 2 in as a single small governance-safe refinement **before or concurrently with** ratification (they are clarity improvements, not blockers); **do not** adopt Recs 3 & 4 as rules. If the owner prefers, ratify as-is and apply Recs 1 & 2 as a fast follow.

**Governance discipline check:** no new doctrine, no implementation guidance, no calibration, no fixture content, and no expansion beyond the fixture framework were introduced by this review or its proposed revisions. ✅

---

*Review only. The subject document was not modified. Proposed revisions for Recs 1 & 2 are drafts pending owner ratification; Recs 3 & 4 are recommended for rejection as conformance rules and retained as review notes.*

**Confidence Fixture Library Specification governance review complete.**

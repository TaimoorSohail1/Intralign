# Canonicalization Control Challenge Review 001

**Document Type:** First-Principles Challenge Review (aggressively tests the proposed "Integrity + Canonicalization Control" refinement) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-04

> **Mode:** attack the proposed refinement, do not defend prior recommendations. First-principles. **No new responsibility/object/concept is adopted** — this review's *conclusion* is in fact that one should **not** be created. Per `CLAUDE.md`, the owner ratifies.

---

## 0. Headline — The Decisive Cut

The whole question turns on one distinction: **governance is required only where there is *discretion*.** Canonicalization splits cleanly along it:

- **Canonicalization as an INVARIANT** (no per-case judgment — *all* interpretations are labeled and persisted uniformly): this is **legitimate R1 content**, already owned across Perceive/Infer/Evaluate/Retain. It is **not a new responsibility** and **not Authority.**
- **Canonicalization as a DISCRETIONARY GATE** (a per-case judgment: "*this* interpretation is good enough to accept, *that* one isn't"): this **is** epistemic acceptance — i.e., **Authority/governance by another name** — and it is correctly **deferred.**

Therefore **"Canonicalization Control" should not be elevated to an architectural responsibility.** Naming it as a responsibility is a category error: it either (a) re-describes an invariant that existing responsibilities already enforce, or (b) smuggles discretion back in and becomes the very Authority we deferred. The correct R1 construct is the **Epistemic Boundary Invariant**, not a Canonicalization Control responsibility. (Final recommendation: Part 6, conclusion **4**.)

---

## Part 1 — Is Canonicalization Control a Distinct Responsibility?

### A. A genuinely distinct responsibility
- **For:** "what may become canonical" is a real decision point distinct from observing, inferring, judging, or storing; naming it makes the observed→canonical boundary explicit and un-collapsible.
- **Against:** a *responsibility* implies an **actor/engine** that performs a behavior others don't. Decompose canonicalization's sub-acts — classify grounding (the *producer* knows: Perceive knows an extraction is directly attributed; Infer knows its output is inferred), attach epistemic state/confidence (**Evaluate**), persist with provenance/idempotency/versioning (**Retain**), surface conflict (**Infer**), refuse to resolve (a *law*, not an act). **Every sub-act already has an owner.** What's left — "interpretation must not enter as grounded/accepted" — is a **constraint**, not an actor.
- **Consequence if adopted:** a new owner overlapping Evaluate (epistemic state) and Retain (persistence) ⇒ **duplicate ownership**, violating one-producer-per-output — the exact failure the architecture closed.

### B. Behavior already inside Perceive/Retain/Infer/Evaluate/Disclose
- **For:** as shown above, grounding-classification (Perceive/Infer), epistemic labeling/confidence (Evaluate), provenance/versioned persistence (Retain), conflict surfacing (Infer), epistemic-safe presentation (Disclose) **already cover every operation.** The "control" is the *invariant* binding them, like idempotency binds writes.
- **Against:** distributed behavior with no single owner risks the invariant being **unstated and therefore unenforced** (precisely the gap the prior review found). A law nobody is told to obey is a law that leaks.
- **Consequence:** adopt the behavior as-is **but** write the binding **invariant explicitly** (the Epistemic Boundary Invariant). No new owner; an enforced law. **This is the winning reading.**

### C. A disguised Authority/Governance reintroduced under a new name
- **For:** "deciding what becomes canonical" sounds like a gate that admits/rejects — structurally identical to Authority's expose/suppress/authorize. If Canonicalization Control ever exercises **judgment per case**, it *is* Authority.
- **Against:** an **invariant has no discretion** — *every* inferred claim is uniformly Candidate, *every* attributed evidence-claim is uniformly Grounded; there is no per-case acceptance judgment. Authority is an **actor making case-by-case judgments**; an invariant is a **uniform law**. No discretion ⇒ not Authority.
- **Consequence:** the danger is **real but conditional** — the moment Canonicalization Control is given discretion ("accept the good interpretations"), it becomes deferred Authority and breaches R1 scope. **This is the strongest reason NOT to name it a responsibility:** a named responsibility *invites* discretion to accrete into it. An invariant cannot accrete discretion.

### D. A product concept not belonging in the architecture
- **For:** "which understanding is trusted" is partly a product/UX concern (how uncertainty is shown), and doctrine ("only action and evidence change understanding") is product philosophy.
- **Against:** the *no-implicit-acceptance* rule is an **architectural invariant** with runtime consequences (what Retain may write), not merely UX. It is architectural, but as a **constraint**, not a **component.**
- **Consequence:** the *labeling/disclosure* of uncertainty is shared with product (Disclose/UX); the *entry rule* is architectural invariant. Neither requires a new responsibility.

**Part 1 verdict: B (already-owned behavior) bound by an explicit invariant — explicitly NOT A (new responsibility) and NOT C (Authority), with the C-risk being exactly why A must be refused.**

## Part 2 — What Does "Canonical" Mean in R1?

| Def | Benefits | Risks | CURRENT_TRUTH compat | CRA compat | Outcome-Orchestration impact |
|---|---|---|---|---|---|
| **A. Persisted** | trivial to implement | **collapses observed→canonical**; persistence masquerades as truth | violates "understanding" discipline | weak (Retain becomes de-facto acceptor) | **corrupts** future acceptance (already-"canonical" can't be cleanly accepted later) |
| **B. Provenance-preserving system-of-record** | integrity-true; no acceptance claim | says nothing about *uncertainty* | ✅ ("not governance-gated" = no acceptance) | ✅ (Retain) | clean substrate |
| **C. Accepted understanding** | strong trust semantics | **requires acceptance ⇒ governance** | ✗ (governance deferred) | needs Authority | this **is** the deferred Accepted-Understanding |
| **D. Best-known current understanding** | user-friendly | "**best**" implies OSLO *resolves* competing meanings ⇒ discretion ⇒ Authority | ✗ | needs Authority | **destroys** ambiguity OSLO should surface |
| **E. Epistemically-labeled understanding** | preserves uncertainty as data; refuses both mere-persistence and acceptance | requires disciplined labeling | ✅ | ✅ (Evaluate labels, Retain stores) | **ideal** — uncertainty travels with the record |

**Recommendation: E, grounded on B.** **Canonical = a provenance-preserving record that carries its own epistemic label.** Canonical does **not** mean *accepted* (C) or *best/resolved* (D), and must never decay to *merely persisted* (A). A low-confidence inferred assumption *is* "canonical" only in the sense that it is the system's **labeled, attributed record of that inference** — its label says *inferred, low-confidence, contested.* **Canonical ≠ trusted.** This single redefinition is what prevents the observed→canonical collapse — not a control actor.

## Part 3 — Ambiguity Stress Test (three conflicting objectives)

**What enters Retain?** Not any of the options cleanly — the right answer is **Option 4, grounded on the fact/interpretation split of Option 3:**

- **Grounded facts (enter as Canonical-Grounded):** *"Stakeholder A asserts the objective is customer satisfaction"*; *"B asserts cost reduction"*; *"C asserts call-volume reduction."* These are **true, attributed observations of what was said** — evidence-grounded, stable, integrity. (Note the subtlety: the *utterance* is a fact even though its *content* is a claim.)
- **Candidate interpretation (enters as Canonical-Candidate, labeled):** *"Project objective is contested — three competing goal interpretations; alignment uncertain."* A **conflict finding (Infer)** carrying **low confidence/reliability (Evaluate)**, persisted as labeled candidate.
- **Does NOT enter:** any single *"the objective is X"* as accepted/resolved truth.

**Why this aligns with Outcome Orchestration:** Option 1 (block until resolved) needs a **resolver/acceptor** — that is Authority, and it *defeats OSLO's purpose* (surfacing instability). Option 2 (all canonical) collapses fact and interpretation. Option 3 alone (interpretations don't enter) **loses** the contested-objective signal OSLO exists to raise. Option 4 alone is right but must specify that the *attributed utterances* are facts. **The synthesis preserves the conflict as first-class labeled knowledge and never resolves it — which is precisely what Outcome Orchestration will later consume.** Crucially, **no acceptance actor is needed**: surfacing the conflict *is* the deliverable.

## Part 4 — Accepted vs Canonical: Does R1 Need All Four States?

**No. R1 needs three active states; "accepted" is deferred.**

| State | R1? | Owner / transition |
|---|---|---|
| **Observed** | ✅ active | Perceive (intake/readiness) |
| **Interpreted** | ✅ active | Infer (findings, inferred assumptions, conflict) + Evaluate (confidence/reliability) |
| **Canonical** (= epistemically-labeled record, per Part 2E) | ✅ active | Retain persists; spans Grounded (attributed facts) + Candidate (labeled interpretations) |
| **Accepted** | ❌ **deferred** | The **user**, via action/evidence (Future Accepted-Understanding). OSLO never self-accepts in R1. |

**Transitions and why none needs governance:**
- **Observed → Canonical-Grounded:** Perceive readiness + Retain integrity. *Non-discretionary* (mechanical).
- **Interpreted → Canonical-Candidate:** Infer/Evaluate produce + label; Retain persists. *Non-discretionary* — **every** interpretation persists as labeled candidate; no selection.
- **Candidate → Accepted:** *Discretionary* — and therefore **deferred** (user/Future).

**The general law:** **governance is needed only for *discretionary* transitions.** R1's two active transitions are non-discretionary (integrity + uniform labeling), so they need **no governance actor**; the one discretionary transition is the deferred one. This is how ownership is represented **without reintroducing governance** — there is no per-case judgment to own, only an invariant to enforce.

## Part 5 — Architectural Consequences

**If Canonicalization Control is ADOPTED (as a responsibility):**
- **Contracts:** a new contract package; Retain/Infer/Evaluate contracts cede labeling/persistence-rule behavior to it → fragmentation.
- **Objects:** it would want a *"Canonicalization Decision"* record — **structurally a Governance Decision** → the Authority object reappears under a pseudonym.
- **Ownership:** a new owner overlapping **Evaluate** (epistemic state) and **Retain** (persistence) → **duplicate ownership.**
- **Readiness:** **negative** — adds a package + a cross-cutting concern + a new pre-Wave-A dependency; widens drift surface.

**If REJECTED (use the invariant instead):**
- **Risks:** if the invariant is unenforced, the persistence=acceptance leak returns. **Protections that remain:** the Epistemic Boundary Invariant; epistemic labels (Grounded/Candidate); Evaluate confidence/reliability; Infer conflict surfacing; Disclose epistemic-safety. **Assumptions to make explicit:** (1) all interpretation persists **only** as Candidate; (2) Retain **never** writes inferred-as-Grounded; (3) **no** actor accepts in R1; (4) canonical = epistemically-labeled, never "accepted/best."
- **Readiness:** **positive** — no new package/owner; one invariant + one object clarification (Grounded/Candidate label) folded into the existing Retain contract.

**Lowest long-term architectural debt: REJECT as responsibility; ADOPT as invariant.** A responsibility *accretes* scope and is the natural home for discretion to creep in and become Authority; an invariant is a stable, discretion-free law with zero actor and zero ownership overlap.

## Part 6 — Final Recommendation (single)

**Conclusion 4 (other): Retain "Integrity, not Authority," and make canonicalization an explicit *Epistemic Boundary Invariant* enforced by existing responsibilities — do NOT adopt "Canonicalization Control" as a responsibility, and do NOT restore Authority.**

Concretely: canonical means **epistemically-labeled, provenance-preserving record** (Part 2E/B). Retain stores **Grounded** (attributed evidence-claims) and **Candidate** (labeled interpretations); Evaluate owns the epistemic label/confidence; Infer surfaces conflict; **no actor accepts**; acceptance is the deferred user transition. This is a one-line-of-authority change from the prior recommendation — **it adds an invariant and a label, not a responsibility.**

### How R1 prevents unstable understanding from being mistaken for settled understanding
**By making uncertainty a first-class *attribute* of canonical knowledge, not a *gate* on entry.** Every canonical item carries its epistemic standing — **Grounded vs Candidate, confidence/reliability, conflict status** — and **Disclose** is obligated to surface that standing, so a contested low-confidence inferred assumption can never *appear* as a settled fact. "Canonical" is decoupled from "trusted": it means *recorded-and-labeled*, not *accepted*.

**Yes — R1 intentionally allows unstable understanding into the canonical store, as labeled Candidate, and that is architecturally correct.** Suppressing it would require **discretion = governance** (the thing we defer); and OSLO's entire value is to **surface** instability, not hide it. OSLO preserves uncertainty **without governance** because uncertainty is carried *in the data* (the epistemic label + confidence + conflict), recomputable and overturned by new evidence/action, and **never crosses into the "accepted" state**, which OSLO does not occupy in R1. The protection is **structural (a labeled state) rather than procedural (a gate)** — which is exactly why no Authority/Canonicalization-Control actor is needed.

---

> ### Proposed Owner Resolution
> **Ratify:** "Integrity, not Authority — with the Epistemic Boundary Invariant," and **reject** elevating Canonicalization Control to an architectural responsibility (it is either already-owned invariant behavior or, if given discretion, deferred Authority). **Adopt:** canonical = epistemically-labeled, provenance-preserving record (not accepted, not best, not merely persisted); Retain stores Grounded + Candidate; Evaluate owns the epistemic label; Infer surfaces conflict; acceptance deferred to the user; Authority plane inactive in R1. **Revise** Pkg 002 to carry the Grounded/Candidate label and enforce the invariant; keep Pkg 003-as-governance dropped and Wave D deferred. **Pre-Wave-A artifact:** the Epistemic Boundary Invariant + Grounded/Candidate clarification (one invariant + one label, no new package).
> **Out of bounds:** no new responsibility/object is created; the invariant and label are routed to the owner.

---

*This challenge review tests the proposed "Integrity + Canonicalization Control" refinement and concludes that Canonicalization Control should not be adopted as an architectural responsibility. The decisive distinction is that governance is required only for discretionary transitions: canonicalization as a uniform invariant (every interpretation labeled and persisted as candidate, every attributed evidence-claim grounded) is legitimate R1 behavior already owned across Perceive/Infer/Evaluate/Retain and is not Authority, whereas canonicalization as a discretionary gate (selecting which interpretations to accept) is epistemic acceptance — deferred Authority under another name — so naming it a responsibility is a category error that either duplicates existing ownership or invites discretion to accrete into Authority. It recommends defining canonical as an epistemically-labeled, provenance-preserving record (Definition E grounded on B) — explicitly not accepted (C), not best/resolved (D), and never merely persisted (A); resolves the three-stakeholder ambiguity test as attributed utterances entering as Grounded facts while the contested objective enters as labeled low-confidence Candidate with nothing resolved (Option 4 grounded on 3); establishes that R1 needs three active states (observed, interpreted, canonical-as-labeled-record) with accepted deferred to the user, and that both active canonicalization transitions are non-discretionary and therefore need no governance; shows that adopting Canonicalization Control as a responsibility fragments ownership, resurrects a Governance-Decision-like object, and worsens readiness, while rejecting it in favor of an explicit Epistemic Boundary Invariant yields the lowest long-term debt; and gives a single recommendation (Conclusion 4) to keep "Integrity, not Authority" with the Epistemic Boundary Invariant, make uncertainty a first-class attribute of canonical knowledge surfaced by Disclose rather than a gate on entry, and intentionally allow unstable understanding into the store only as labeled, recomputable, never-accepted Candidate — preserving uncertainty without governance, structurally rather than procedurally. It adopts nothing unilaterally and routes all ratification to the owner.*

**Canonicalization Control Challenge Review 001 complete.**

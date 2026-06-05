# Release 1 Contract Coverage Audit 002 — Cognitive Capabilities Not Explicitly Contracted

**Document Type:** Independent Coverage Audit (build/test/observe) · **Status:** Complete — findings below; owner-routed · **Date:** 2026-06-04
**Question (owner-directed):** *Beyond Fast/Deep + 60s (DL-046), are there other Release 1 product features not explicitly captured in the contracts for build, test, or observe?*
**Method:** mapped every capability in `OSLO_CAPABILITY_MATRIX_V2` (92 capabilities, 19 categories) to the authoritative build-spec contracts (`WAVE_A–E + U` packages, Runtime Object/Behavior Models, Contract Inventory) by name-presence + behavior coverage. Per `CLAUDE.md`, **no contract is edited here; gaps are routed to the owner.**

---

## 0. Verdict

**Yes — Fast/Deep was not isolated.** A set of **cognitive Release 1 (Alpha) capabilities — several Critical/High — are not explicitly named or obligated in the contracts**, the same class of gap DL-046 just closed. The single most important cluster is the **front of the pipeline: evidence → structured plan (Claim Extraction, Planning Synthesis, Planning Artifact Generation, Understanding Evaluation)** — Critical capabilities with no clear contracted owner, one of which (**Planning Artifact Generation**) is **generative** and may not map cleanly to the current responsibility model. Three interaction/collaboration capability sets (**OSLO Chat, CAF Review Requests, Suggested Fixes**) are also uncontracted and need an explicit owner classification (contract vs. commodity vs. defer).

**Important context (already settled):** the prior `RELEASE_1_CAPABILITY_COVERAGE_REVIEW_V1` already found the contracts are **cognition-scoped** and scored Overall ~68% (UI ~55%, Workflow ~50%); **DL-043 J (Application/Platform Classification)** then decided commodity/platform capabilities (project CRUD, auth, RBAC, settings, notifications-state, monetization, telemetry, sharing) are **Category C/E/F — intentionally uncontracted**. That part is *resolved by decision* and is **not** a finding here. This audit isolates capabilities on the **cognitive side** that still slipped through.

---

## 1. Correctly NOT a gap (excluded)

- **Commodity / platform — intentionally uncontracted per DL-043 J:** `PF-01/02/03/05`, `AW-01/02/03/06/07`, `COLLAB`, `SHARE`, `TEL-01…07`, `MON-01/03/04`, `SEC-01…07`, `PLAT-01…06`. (System observability is governed separately by Observability Governance; product telemetry is commodity.)
- **Future / deferred (not R1):** `AE-06 Understanding Debt` (Future/Low), `CONF-07 Operational Confidence` (Future/Low). Correctly absent.
- **Already contracted:** `EI-01` (Perceive intake, WA-001), `AE-01/02/03` (Fast/Deep/recompute — **DL-046** + 00R), `CAF-01…05` · `CONF-01…04` · `ISS-01…04` (Evaluate, Wave B), `REC-01/02/03` (Advise, Wave C), `MRI-01/02/03` + `OVL` (Disclose, Wave E — "overlay" appears in the surface contracts), user acceptance (Wave U).

---

## 2. Findings — cognitive R1 capabilities NOT explicitly contracted

### 2A. CRITICAL — the "evidence → structured plan" engine (highest priority)

| Cap | Name | Why it's a gap |
|---|---|---|
| **EI-02** | **Claim Extraction** (Critical) | "Extract goals/outcomes/stakeholders/assumptions/constraints/dependencies from evidence." Wave A *Perceive* explicitly does **no cognition** (admission/integrity only); Wave B *Infer* produces **Findings**, not extracted claims. **No responsibility is contracted to extract claims into the Attested assertion types** that Retain then stores. |
| **PS-01** | **Planning Synthesis Engine** (Critical) | "Construct a usable planning model from incomplete evidence (Extraction → Context Expansion → Planning Construction → Understanding Evaluation)." The synthesis pipeline is not contracted. |
| **PS-02** | **Planning Artifact Generation** (Critical) | "**Generate** Intent/Context/Scope/Requirements/WBS/Resources/Schedule artifacts; editable." **Generative.** The Contract Inventory has Retain *store* planning artifacts, but **nothing is contracted to *generate* them** — and the Cognitive Responsibility model has no "generate artifacts" responsibility (Advise generates candidate *responses*, not plan artifacts). **This is a contract gap AND a possible architecture question.** |
| **PS-03** | **Understanding Evaluation** (Critical) | "Evaluate synthesized model to seed initial CAF/Confidence." Maps to Evaluate, but its **input — the synthesized model from PS-01/02 — is uncontracted**, so the seam is undefined. |

> **This is the most consequential finding.** OSLO's core promise — *turn raw documents into a structured, evaluated planning model* — runs through EI-02→PS-01→PS-02→PS-03, and that chain has **no explicit contracted owner**. It was likely folded informally into "Perceive/Infer," but Perceive is contracted as non-cognitive and Infer as Finding-only. Recommend resolving **before** Phase II/III build.

### 2B. HIGH — interaction / collaboration capability sets (need owner classification)

| Cap set | Name | Status |
|---|---|---|
| **CHAT-01…04** | **OSLO Chat** (High) — project-aware reasoning interface; context inheritance; Explain/Clarify/Resolve/Improve; chat-generated improvements (may trigger Deep Pass) | **Entirely uncontracted.** No Wave, no surface in the Wave E list. It's *interactive cognition*, not obviously commodity. |
| **CRR-01…05** | **CAF Review Requests** (High) — Share-for-Review a finding; review package; stakeholder Comment/Approve/Reject/Suggest; **Response → Deep Pass**; status in MRI | **Entirely uncontracted.** A full stakeholder-review workflow that **feeds the cognitive loop** (CRR-04 → evidence → Deep Pass). |
| **REC-04** | **Suggested Fixes** (High) — one-step fixes **applied to artifacts** (gated by daily allowance) | **Uncontracted, and architecturally notable:** applying a fix **writes to an artifact** — that's an *action*, beyond Advise's "candidate response." Needs an owner (Act?) and an integrity story. |
| **REC-05** | **Validation Recommendations** (Alpha) — recommendations seeking stakeholder confirmation | Uncontracted; tied to CRR. |

### 2C. MEDIUM — named cognitive capabilities, uncontracted

| Cap | Name | Note |
|---|---|---|
| **CONF-06** | **False-Confidence Detection** (Medium) | "Detect high confidence built on inaccurate understanding (the dangerous 4th state)." A real, named cognitive capability — not in any QA/Evaluate contract. |
| **AE-04** | **Understanding State Model** (Medium) | Initial→Partial→Refined→Validated→Mature — partially echoed by DL-046's confidence_stage, but the full state model isn't contracted. |
| **AE-05** | **Progressive Disclosure** (Medium) | Present understanding progressively — a Disclose obligation, not enumerated. |
| **MRI-04/05/06/07** | Heatmap · CAF Triangle · Understanding Timeline · Understanding Dependencies | Wave E contracts the MRI *umbrella*; these **named sub-components** aren't enumerated (covered by UX specs, not the contract). MRI-04 is **High**. |
| **AW-04 / AW-05** | Assisted Editing · Persistent Intelligence Layer (High) | Editing-time AI assist + always-visible Confidence/CAF/state. Presentation-side (Disclose-during-edit); not contracted. |

---

## 3. The pattern

The contracts faithfully capture the **cognitive spine** (Perceive→Retain→Infer→Evaluate→Advise→Disclose→Accept) and its core objects (Finding/Issue/Confidence/CAF/Recommendation). What they **don't** enumerate are the **named product capabilities layered on that spine** — the front-end synthesis engine, the interaction surfaces (Chat), the collaboration loop (CRR), applied actions (Suggested Fixes), and specific sub-features (MRI components, false-confidence). Fast/Deep was the first instance found; this audit shows it was systemic on the cognitive side, not a one-off.

## 4. Recommendations (owner-routed; no contract edited here)

1. **Resolve §2A first — it's the build-critical one.** Decide the owner + contract for **Claim Extraction → Planning Synthesis → Planning Artifact Generation → Understanding Evaluation**, including the architecture question: **is there a generative responsibility, or is artifact generation a contracted behavior of an existing one?** This should precede Phase II/III. *(Likely a DL-class decision, not just an amendment, because PS-02 is generative.)*
2. **Classify §2B (Chat, CRR, Suggested Fixes, Validation Recs).** For each, decide: **(a) cognitive → contract it** (new/extended Wave), **(b) commodity interaction → intentionally uncontracted** (like DL-043 J), or **(c) defer from R1** (a scope cut). These are Alpha in the matrix today, so silence = ambiguous scope.
3. **Fold §2C into existing contracts** where they're sub-behaviors: CONF-06 and AE-04/05 into Wave B/E QA + obligations; MRI-04…07 and AW-04/05 enumerated in the Wave E Disclose contract (they already have ratified UX specs — this is naming, not new scope).
4. **Method going forward:** add a **capability-to-contract traceability check** to the contract pipeline (Framework §E), so any Matrix-V2 Alpha capability without a contract reference is flagged automatically — preventing the next Fast/Deep.

## 5. Honest caveats

- This is a **name-presence + behavior audit**; a capability could be *partially* covered under different vocabulary. The §2A chain and Chat/CRR are confirmed absent in object/behavior models too, so those are solid. The §2C items are more "not enumerated" than "absent in spirit."
- Whether Chat/CRR are truly R1 is a **scope question only the owner can answer** — the matrix marks them Alpha, but they may have been intended as fast-follow. The audit flags; it does not assume.

---
*This independent audit maps all 92 Release 1 capabilities in OSLO_CAPABILITY_MATRIX_V2 to the ratified build-spec contracts and finds that, beyond the Fast/Deep + 60s gap already closed by DL-046, a set of cognitive Alpha capabilities remain unconcontracted: most critically the evidence-to-plan engine (Claim Extraction, Planning Synthesis, Planning Artifact Generation, Understanding Evaluation — one of which is generative and may not map to the current responsibility model), plus the OSLO Chat interaction surface, the CAF Review Request collaboration loop, applied Suggested Fixes, and several named sub-capabilities (False-Confidence Detection, Understanding State Model, Progressive Disclosure, MRI components, assisted editing). It distinguishes these from the commodity/platform capabilities already intentionally left uncontracted by DL-043 J, recommends resolving the Critical synthesis-engine cluster before Phase II/III, routes the interaction/collaboration sets to an owner classification decision, and proposes a capability-to-contract traceability check to prevent recurrence. No contract is edited; all findings are owner-routed.*

**Release 1 Contract Coverage Audit 002 complete.**

# Wave E Contract Packages — Disclose Surfaces (Presentation)

**Document Type:** Release 1 Contract Packages (architecture-level, environment-independent) · **Status:** **DL-043-conformed (2026-06-04) — Ready for Review** · **Date:** 2026-06-04
**Contract Sets:** IC/QA/OBS-WE-DISCLOSE (per-surface obligations within) · **Owning Responsibility:** **Disclose** (cognitive presentation) with **Render** as its non-cognitive Service.
**Consumes (authoritative):** Cognitive Responsibility Architecture · Runtime Object Model (DL-043) · Runtime Behavior Model (DL-043) · Contract Inventory · QA Governance · Observability Governance · Calibration Defaults (bands/drift) · Wave A/B/C/U · ratified UX specs (MRI, Finding/Recommendation Panels, Notification/Awareness, History/Timeline, Export, Overview, Companion) · **DL-043** (Epistemic State Model · Derived Cognition Lifecycle · Plan-Fact). *(Environment binding deferred.)*

> **Mode:** Disclose **presents** governed cognitive outputs; it does **not** generate, evaluate, govern, accept, or alter them. It **consumes** Findings/Issues/Confidence/CAF/Recommendations/Clarifications, Cognition History, and User Acceptance/plan facts, and renders them **epistemically safely** — current understanding foregrounded, history available, uncertainty visible. **No Authority.** Parallelizable from object-model completion. Per `CLAUDE.md`, owner ratifies.

---

## DL-047 Additions (authoritative — ratified 2026-06-04)

**OSLO Chat (CHAT-01…04) — Disclose-class interaction surface.** Chat is a project-aware interaction surface that **consumes** existing cognition (Explain/Clarify) and may **trigger** cognition (Improve → routes through Advise + Deep Pass). It **generates no canonical content** and **changes no assessment** itself. Inherits context when launched from an issue/recommendation/artifact/CRR. **QA negative (Critical):** Chat writing canonical, self-accepting, mutating an artifact directly, or changing an assessment outside recompute. **OBS:** `Chat Exchange` events (non-canonical).
**MRI sub-components (MRI-04…07):** the Disclose MRI surface **must** present the **Artifact Understanding Heatmap**, **CAF Triangle**, **Understanding Timeline**, and **Understanding Dependencies (blocked-awaiting-review)** — each tracing to its governed objects + UX spec.
**Assisted Editing / Persistent Intelligence (AW-04/05):** during artifact editing, Disclose presents always-visible Outcome Confidence / Clarity / Alignment / Feasibility / Understanding-State, and routes assists to Chat (B1) or Suggested Fix (B3).
**CRR status visibility (CRR-05):** review status presented across the workspace + in MRI. *(The CRR workflow UI — create/package/notify — is Category E commodity per DL-043 J; the cognitive seam response→evidence→Deep Pass is contracted in Wave A DL-047 Additions.)*

---

## E0. Shared Orientation & Invariants (all surfaces)

**What Disclose owns:** posture-aware **disclosure**, **epistemic-safety**, **surface-invariant meaning preservation**. **Render** (Service) does pixel-level formatting. **MRI is the umbrella** (visualization + diagnostic experience); Finding/Recommendation are **Panels** (not Workspaces); the **Recommendation Panel opens only in Finding context** (RP-C1); "Possible Resolution Paths" is **presentation-only** (multiple Recommendations, no object — AMB-1).

**Shared invariants (every surface):**
- **Presents, never generates.** Disclose owns no cognition; it shows what Infer/Evaluate/Advise produced and what Retain holds. It **never** changes an assessment (only recompute does).
- **Epistemic safety (the core duty).** Every shown item carries its **epistemic standing**: **Attested vs Derived**, **confidence band** (Calibration Defaults: 0–49 low / 50–74 med / 75–100 high, round-down at edges), and **conflict/ambiguity**. Nothing Derived is ever shown as settled fact; a **user-confirmed plan fact** is shown as user-attested (factual *in the plan*), distinct from world-truth.
- **Current foreground + history.** Shows the **latest** understanding prominently **and** the **history trail** (from Cognition History Records) — "today's view + how it got here." Drift is surfaced as a **product feature** (≥10 pts / band change).
- **Confidence = trust in understanding, never project health.**
- **No Authority / no acceptance by Disclose.** It may render the *acceptance affordance*, but the user's confirmation is captured by Perceive/recorded by Retain (Wave U) — Disclose doesn't accept.

---

## E1. Surface Obligations (Implementation Contract — IC-WE-DISCLOSE)

| Surface | Presents (consumes) | Surface-specific obligations |
|---|---|---|
| **MRI (umbrella)** | Findings, Issues, CAF, Confidence/Outcome Confidence, Overlays, history | Visualize understanding state + diagnostics; show confidence bands + conflict; current + history; never recompute |
| **Finding Panel** | a Finding + its evidence anchors (Attested) + confidence | Show finding with **Attested evidence lineage** and Derived/confidence labels; entry point for Recommendation Panel |
| **Recommendation Panel** | Recommendations for a Finding (RP-C1: **only in Finding context**) | Show advisory recommendations + alternatives (presentation grouping = "Resolution Paths", **no object**); render accept/reject/defer affordance (→ Wave U capture) |
| **Issue Cards** | Issues + severity/confidence | Show issue with severity + confidence band; link to source Findings |
| **Overview** | aggregate Outcome Confidence/CAF, counts | Project-level understanding summary; bands; **not** project-health |
| **Companion** | contextual understanding (route to Recommendation **via associated Finding**, Option B) | Surface-transition consistency; epistemic-safe summaries |
| **Notification / Awareness** | drift signals, Acceptance-Impact alerts, new emissions | Surface **Outcome Drift** + **Acceptance-Impact** ("a decision you confirmed is affected") as awareness; read/unread/dismiss is **platform state (Category E)**, not canonical |
| **History / Timeline** | Cognition History Records, User Acceptance Records, plan facts | Reconstruct **the trail** (what OSLO said when, what the user confirmed); record-exact; the "why did it change" narrative |
| **Export / Share-Out** | governed current outputs + history | Export **honors epistemic labels** (Derived/Attested, confidence, plan-fact attribution); preserves provenance; no new claims |

**Forbidden (all surfaces):** generate/evaluate/score/recommend; change any assessment; promote Derived→Attested; **accept** an interpretation; show Derived as settled or low-confidence as high; govern/suppress by Authority (inactive); treat notification state as canonical.

---

## E2. QA Contract — QA-WE-DISCLOSE
- **Positive:** each surface renders the correct governed objects with **epistemic labels** (Attested/Derived, confidence band, conflict); current foreground + history both available; Recommendation Panel opens **only** in Finding context (RP-C1); export preserves labels + provenance; drift/Acceptance-Impact surfaced per thresholds; plan facts shown as **user-attested**.
- **Negative (impossible/rejected):** Disclose generating/altering cognition or changing an assessment; **Derived shown as settled/world-true**; low-confidence shown as high (band-edge guard breached); Recommendation Panel opening **without** a Finding; a **Resolution-Path object** created; notification state written as canonical; export emitting a claim not in the governed source; acceptance performed by Disclose.
- **Failure classification:** Critical — Derived-as-settled / confidence overstated / Disclose mutating cognition / RP-C1 violation / acceptance-by-Disclose. Major — missing history view; missing epistemic label; export dropping provenance. Minor — formatting/label cosmetics (Render).

## E3. Observability — OBS-WE-DISCLOSE
- **Events:** Disclosure Rendered; Notification Raised; Acceptance-Impact surfaced; Export produced; (platform) notification read/dismissed. **Audit:** what governed version was shown, with which epistemic labels; export provenance. **Replay:** **what-was-shown** is reconstructable from the governed source + the Cognition History version it presented (record-exact source; rendering is Render-service). **Drift/Trust:** Derived-shown-as-settled, confidence overstated, export-claim-not-in-source = **trust failures**; Outcome/Acceptance drift surfaced = **product feature**.

---

## E4. Conformance (Framework §E/§H/§K)
- **§E** ✅ — every surface traces to a ratified UX spec + the governed objects it presents (Object Model) and the events it observes (Behavior Model); owner = Disclose (Render = service). No new responsibility.
- **§H** ✅ — QA positives↔IC obligations, negatives↔forbidden; IC surfaces ⊆ OBS observed; epistemic-safety invariant bound/validated/observed across all surfaces.
- **§K** ✅ — no orphan behavior; Disclose presents (one consumer role, not a producer); no invented concepts (MRI umbrella, Panels, RP-C1, AMB-1 all ratified); **no Authority**; no environment binding; no implementation/technology (Vercel/Render binding deferred).
- **Cross-wave** ✅ — consumes Wave A (Attested + history), B (Findings/Issues/Confidence/CAF), C (Recommendations/Clarifications), U (acceptance/plan facts/Acceptance-Impact). Live-data wiring binds at environment stage; presentation structure is env-independent.

## E5. Final Verdict
**READY FOR REVIEW — DL-043-conformed.** Wave E defines the **Disclose** presentation surfaces (MRI umbrella, Finding/Recommendation Panels with RP-C1, Issue Cards, Overview, Companion, Notification/Awareness, History/Timeline, Export) as **epistemic-safe consumers** of governed cognition: current foreground + history, Attested/Derived + confidence-band + conflict always visible, plan facts shown as user-attested, drift/Acceptance-Impact surfaced as product features, and **no generation/evaluation/governance/acceptance** by the presentation layer. Render remains the non-cognitive Service. No new responsibility; Authority inactive; environment binding deferred.

> ### Proposed Owner Resolution
> Approve Wave E (Disclose surfaces). With Waves A, B, C, U, and E complete, **all Release 1 cognitive + presentation contract packages exist** (the cognition chain end-to-end plus user acceptance and presentation). Proceed to the logical data model and the engineering enablement artifacts (coding constraints + code-tree, then the Engineering Handoff Package).

---

*This Wave E package defines the Release 1 Disclose presentation surfaces as epistemic-safe consumers of governed cognition under the ratified UX decisions (MRI umbrella; Finding/Recommendation Panels; Recommendation Panel opens only in Finding context per RP-C1; Resolution Paths presentation-only per AMB-1; Companion routes to Recommendation via the associated Finding per Option B), establishing that Disclose presents but never generates, evaluates, governs, accepts, or alters cognition, that every surface carries epistemic standing (Attested vs Derived, confidence band per the calibration defaults with conservative band-edge rounding, and conflict/ambiguity) so nothing Derived is shown as settled and confidence is never overstated, that current understanding is foregrounded with the history trail available from Cognition History Records, that user-confirmed plan facts are shown as user-attested (factual in the plan, distinct from world-truth), and that Outcome Drift and Acceptance-Impact are surfaced as product features while Derived-as-settled, overstated confidence, and unsourced exports are trust failures. It assigns Render as the non-cognitive formatting Service, includes mandatory positive-and-negative QA with severity, observability over what-was-shown with record-exact source reconstruction, and self-validates against Framework §E/§H/§K, introducing no new responsibility, no Authority, and no implementation or environment binding; routed to the owner for review.*

**Wave E Contract Packages — Disclose Surfaces complete.**

# Wave I Contract Package — Interaction & Collaboration (Chat · Review Requests · Suggested Fixes)

**Contract Set:** IC-WI-INTERACT / QA-WI-INTERACT / OBS-WI-INTERACT · **Owning Responsibilities:** **Disclose** (Chat surface, CRR status) + **Perceive** (CRR response intake) + **Advise** (Suggested Fix, Validation Rec) · **Status:** **Ratified under DL-047 (2026-06-04)** · **Date:** 2026-06-04
**Consumes (authoritative — must not redefine):** Cognitive Responsibility Architecture Spec (+ DL-047 Update) · Object/Behavior Models (+ DL-047 Additions) · QA + Observability Governance · DL-043 (epistemic invariants) · DL-046 (Fast/Deep) · Wave A/B/C/E/S contracts · the ratified UX specs (`OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1`, CRR/Sharing specs, `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1`, `RECOMMENDATION_SYSTEM_SPECIFICATION_V1`).

> **Mode:** the **interaction/collaboration layer over existing cognition.** Nothing here generates canonical content or changes an assessment outside recompute. The **CRR workflow UI (create/package/notify) is Category-E commodity** (DL-043 J); this contract owns only the **cognitive seams**: Chat (consume/trigger), the stakeholder-response→evidence→Deep-Pass intake, Suggested-Fix as an Advise candidate, and Validation Recommendations. **No new responsibility.** Per `CLAUDE.md`, the owner ratifies.

---

## DL-048 Additions (authoritative — ratified 2026-06-05)

**Cost-governance — interaction surfaces respect the per-tier daily caps + routing (Calibration Defaults §4c).** Chat and Suggested-Fix consume AI tokens, so they are bound by the DL-048 cost-governance config (tier-keyed; **no new responsibility/object**).
- **Per-tier daily caps (config):** **chat messages/day** and **suggested-fixes/day** are enforced from §4c (Free defaults: 20 chat/day, 5 fixes/day). On cap → **gate** (surface "limit reached" + upgrade prompt, commodity MON); the existing API `429 rate_limited` already covers the free-tier suggested-fix daily limit.
- A chat **Improve** that triggers Deep Pass (via 00R) inherits the **per-user rollup budget + routing** enforced at the Wave B/S engine seam — it cannot bypass the budget.
- **Model routing is tier-keyed config:** Free-tier chat/fix inference routes to the cheap class (§4c).
**QA:** positive — Free-tier chat/fix usage past the configured daily cap is **gated and emitted**; a chat-triggered Deep Pass stays within the per-user budget. **Negatives:** exceeding a daily cap without gating; a chat-triggered run **bypassing** the engine budget/routing; silent overspend.
**OBS:** chat/fix inference emits **`AI Spend Recorded`** (shared Wave B event shape: tokens/est-cost by `tier`/`mode`/`model`); daily-cap-hit = product signal, budget-bypass = trust signal.

---

## 1. Implementation Contract — IC-WI-INTERACT

### 1A. OSLO Chat (CHAT-01…04) — Disclose
- **Required:** present a project-aware interaction surface anchored to project context (artifacts, confidence, CAF, issues, recs, CRRs); **inherit context** when launched from an issue/recommendation/artifact/CRR; provide functions **Explain · Clarify · Resolve · Improve**; a chat-generated **Improve** routes through **Advise** (candidate) and may **trigger Deep Pass** via 00R.
- **Forbidden:** writing to the canonical store; mutating an artifact directly; **changing any assessment** (confidence/finding/issue) outside recompute; self-accepting; governing exposure.
- **Object:** `ChatSession` / `ChatExchange` — **non-canonical interaction records** (not Attested, not Derived cognition).

### 1B. CAF Review Request — cognitive seam (CRR-01…05)
- **Required (Perceive):** a submitted **`StakeholderResponse`** (Comment/Approve/Reject/Suggest-Alternative on a shared finding) is admitted as **new evidence** (evidence-attested) and **triggers Deep Pass** (00R); confidence/MRI update via recompute. **Required (Disclose):** present review **status** across workspace + MRI (CRR-05). **(DL-049)** the response is authored by a **`Principal`** (`type = reviewer`); provenance = that Principal; a later `reviewer→user` promotion **does not re-attribute** prior responses (append-only). Seam unchanged.
- **Forbidden:** treating a response as **world-truth** or as **OSLO self-acceptance**; a response **changing an assessment without recompute**.
- **Commodity (not this contract):** creating the request, building the package, notifications, the sharing UI — Category-E (DL-043 J).

### 1C. Suggested Fix (REC-04) + Validation Recommendation (REC-05) — Advise
- **Required:** Advise generates a **`SuggestedFix`** (a *candidate* edit to a named artifact, anchored to a Finding) and a **Validation** recommendation type (seeks stakeholder confirmation → routes to a CRR on user action). Both are **Derived**, recomputable, CHR-appended.
- **Forbidden (Critical):** **OSLO autonomously writing/applying a fix to the user's artifact.** Application is a **user-initiated artifact edit** (commodity editing) which then triggers recompute. The daily-allowance gate is commodity (MON).

### 1D. Bound Invariants
Interaction/collaboration **consumes/triggers** cognition; it **never** generates canonical content, accepts interpretations, changes assessments outside recompute, or autonomously edits artifacts. One producer per output; no Authority; OSLO never self-accepts.

---

## 2. QA Contract — QA-WI-INTERACT

- **Positive:**
  - Chat answers from project context; context inherited from the launching object; Improve produces an Advise candidate (and, when accepted, triggers Deep Pass).
  - A `StakeholderResponse` is admitted as evidence and **triggers a recompute**; MRI/confidence update via the new CHR.
  - `SuggestedFix` and `Validation` recommendations generate as **Derived**, anchored to a Finding, CHR-appended.
- **Negative (impossible / rejected — each a test, Critical unless noted):**
  - **Chat writes canonical / mutates an artifact / changes an assessment outside recompute.**
  - **A stakeholder response treated as world-truth or as OSLO self-acceptance**, or changing an assessment without recompute.
  - **OSLO autonomously applying a Suggested Fix to an artifact** (application must originate from the user).
  - A `ChatSession`/`ChatExchange` written as Attested or as Derived cognition (it is neither — interaction record).
- **Failure classification:** Critical — canonical write / artifact mutation / assessment-change-without-recompute / autonomous fix / response-as-truth. Major — missing context inheritance; Suggested-Fix/Validation not anchored or not CHR-appended. Minor — UI/metadata gaps.
- **Determinism tier:** Chat answers + Suggested-Fix text = **semantic** (no exact replay); the **seam behaviors** (response→recompute trigger; fix-application→recompute) = **exact** (rule-driven).

---

## 3. Observability Contract — OBS-WI-INTERACT

- **Events:** `Chat Exchange` (non-canonical); `Stakeholder Response Submitted` (→ Deep Pass); `Suggested Fix Offered`; `Validation Recommendation Emitted`. Fix **application** observed as a **user artifact edit + recompute** (not an OSLO write).
- **Audit:** for a CRR response — which finding/artifact it targets, who responded, what triggered the Deep Pass; for a Suggested Fix — the Finding it derives from + the user action that applied it.
- **Replay:** seam behaviors record-exact; chat/fix text semantic.
- **Drift / Trust:** Chat changing an assessment, a response mutating state without recompute, or an autonomous artifact write = **trust failures**.

---

## 4. Triad Consistency & Conformance (Framework §E/§H/§K)
- **§E** ✅ Chat→Disclose, response-intake→Perceive, status→Disclose, Suggested-Fix/Validation→Advise; objects (`ChatSession`/`Exchange`, `ReviewRequest`/`StakeholderResponse`, `SuggestedFix`) trace to the DL-047 Object Additions; events to the DL-047 Behavior Additions. One producer each; no new responsibility.
- **§H** ✅ QA positives↔IC required; negatives↔IC forbidden; IC events ⊆ OBS; the **"interaction never writes canonical / never autonomously edits / never changes assessment outside recompute"** discipline is consistent across all three.
- **§K** ✅ no orphan behavior; no Authority; CRR workflow UI correctly scoped out as commodity; preserves DL-043 invariants + DL-046 modes.

## 5. Verdict
**CONFORMANT — ready for owner approval.** The interaction/collaboration seams are contracted at full depth with the Critical negatives that keep them on the consume/trigger side of the epistemic boundary (no canonical writes; no autonomous artifact edits; no out-of-recompute assessment change; stakeholder responses are evidence, not truth). No new responsibility; commodity workflow UI correctly excluded.

---
*This Wave I contract package contracts OSLO's interaction and collaboration layer at full depth: OSLO Chat as a Disclose-class surface that consumes and triggers cognition but writes no canonical content and changes no assessment; the CAF Review Request cognitive seam where a stakeholder response is admitted as evidence (Perceive) and triggers Deep Pass while the surrounding workflow UI stays commodity; and Suggested Fixes plus Validation Recommendations as Advise candidates where OSLO never autonomously edits the user's artifact (application is a user-initiated edit that triggers recompute). It specifies required and forbidden behavior, positive and negative QA with the Critical negatives that protect the epistemic boundary, determinism tiers (semantic for chat/fix text, exact for the seam triggers), and observability, and confirms triad consistency with no new responsibility — implementing DL-047 Part B at build-grade rigor for an external team.*

**Wave I Contract Package — Interaction & Collaboration complete (DL-047).**

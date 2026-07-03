# Clarification Flow — Contract Package (R1)

> **DRAFT for owner ratification (Framework 001).** Closes Integration-Map gap **G1** now that clarification is **in R1 scope** (owner, 2026-07-01). AI-drafted; owner ratifies. Route: Proposal (this) → Review → Decision (`DL-PENDING-clarification-flow.md`) → contract/interface + spec edits → Changelog; one canon PR in flight (DL-065).

- **Date:** 2026-07-01 (surface decided 2026-07-02) · **Status:** Ratified 2026-07-02 — Accepted with Conditions; **surface = Finding Panel (Option B)** · **Class:** A (interface contract; R1 scope addition — **amends a ratified experience spec**) · **Decided by:** Idris (Founder Console)
- **Layer:** `20_handoff` (State/Event/API interface amendments) + reconciliation with `10_product/experience/OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1`.
- **Grounded in:** `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPEC` (Q3/Q9/§G — the ratified clarification model), `WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE` (information→stale→reanalysis), `RELEASE_1_STATE/EVENT/API` interfaces, `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW` (answer-treated-like-an-edit), DL-043 (advisory-only; Derived vs Attested).

## 1. Escalated conflict — owner decision required (Anti-Assumption)
The ratified experience spec and the prototype disagree on **where a clarification is answered**:

| | Ratified `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPEC` | Prototype `oslo_r1_experience_mockup_v2.html` |
|---|---|---|
| Surface | **Chat** (conversational); **explicitly not** Finding Panels (Q3) | **Finding Panel** (inline answer via `answerClarification`) |
| Object model | **No modeled object** (§122) | No object (a `.clar` flag on the finding) — **aligned** |
| Answer semantics | Project-information change → stale → reanalysis | Same (reanalysis closes the finding) — **aligned** |

Only the **surface** conflicts. **This is not mine to resolve** — see §7 for the two options. Everything in §2–§6 holds **either way** (they're the mechanics, not the surface).

## 2. Conformance guardrails (what must NOT be built)
Per the ratified spec §122, R1 **does not** create: a Clarification object, a clarification lifecycle/state machine, a disposition, a Resolution Candidate/Path, or any accepted-understanding construct. A clarification answer is **information capture**, nothing more. Answering **never** mutates CAF/Reliability/Confidence, and **never** closes a finding by itself — **only reanalysis** does (this preserves "acceptance ≠ success" and advisory-only).

## 3. State (no new domain entity)
- **No new entity.** A clarification **prompt** is a conversational element (Chat transcript); a clarification **answer** is a **project-information change** captured like an artifact edit / evidence add.
- On answer, the project's analysis transitions to **stale/pending** via the existing recompute-stale backbone (00R). The "pending clarification" indicator the prototype shows is the **existing stale/pending analysis state**, surfaced as "awaiting reanalysis" — not a new object.

## 4. Events (information-change class; not a new object lifecycle)
Add one **information-change** event, parallel to `evidence_added` / `artifact_version_created` (which already have recompute consumers):

- **`clarification_answer_captured`** — payload `{ project_id, answer_text, prompt_ref?, context_ref? (finding/artifact/dimension the prompt related to), actor=user, authorship=attested }`. **Has recompute consumers** (triggers stale → reanalysis). Standard envelope (idempotent on `event_id`; carries `causation_id` → the reanalysis run; `correlation_id`).
- **(Optional, presentation-only)** `clarification_prompt_shown` — awareness that OSLO raised a prompt; **zero recompute consumers** (like a notification). Include only if the surface decision (§7) needs it for the "pending" indicator; otherwise the stale state suffices.

*No `clarification_requested/answered/superseded` object-lifecycle events* — that would imply a modeled object the spec forbids.

## 5. API (capture, not object CRUD)
- **`POST /projects/{pid}/clarification-answers`** — body `{ answer_text, prompt_ref?, context_ref? }`; captures the answer as a project-information change, marks analysis stale, emits `clarification_answer_captured`. Idempotency-Key honored. **Reuses** the recompute trigger path (same as an artifact edit).
- **No** `GET /clarifications`, no `:accept/:resolve` — there is no object to list or dispose. The **prompt** and **answer** are presented in the **Chat transcript** (already specified by the experience spec); a pending answer is reflected by the **stale/pending analysis** read (existing `GET /analysis-runs/{rid}` / project state).
- *If §7 chooses the panel surface,* the same endpoint is called from the panel; the contract is unchanged — only the caller differs.

## 6. Determinism (two-axis replay, DL-043)
- **Attested / exact-replay:** the user's `answer_text` (an input, replays exactly).
- **AI-derived / semantic (±7-band):** whether OSLO *raises* a prompt and its wording — derived, not guaranteed bit-stable (same tolerance regime as finding detection).

## 7. Surface decision — RESOLVED 2026-07-02: **Option B (Finding Panel)**
Owner chose to keep the prototype's in-panel clarification and **amend the ratified `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPEC` Q3** to permit panel-based answering (Chat clarification, already specified, remains valid). Contract §2–§6 unchanged; the answer command is called from the Finding Panel. Consequence: this decision **edits a ratified experience spec** — the Q3 amendment must be part of the landing PR and pass the doc-integrity gate.

*(Original options, for the record — Where is a clarification answered in R1?)*
- **Option A — Conform to the ratified spec (Chat).** Answer in OSLO Chat; where the prototype shows an inline finding-panel answer, replace it with a **"Clarify in chat →"** pointer (finding may still show a "pending clarification" indicator that routes to Chat). *Prototype changes slightly; ratified spec unchanged; smallest canon footprint.*
- **Option B — Amend the ratified spec to allow in-panel answering.** Keep the prototype's inline finding-panel clarification; **amend `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPEC` Q3** to permit panel-based clarification as a second surface. *Prototype unchanged; requires editing a ratified experience spec (bigger canon change).*

Both use the identical §2–§6 contract. Recommendation: **Option A** — it honors "build the prototype exactly" on everything except the single interaction location, avoids amending a ratified spec, and keeps clarification where the spec deliberately centralized it (the conversational layer).

## 8. Traceability & acceptance
- **Capability:** user answers an OSLO clarification → **Contract:** `POST …/clarification-answers` + `clarification_answer_captured` → **Test:** answer marks analysis stale, next reanalysis consumes it, finding weakens/closes *only via that run*; answering alone mutates nothing → **Observability:** `clarification_answer_captured` emitted with causation → reanalysis run.
- **Negative (must fail):** any Clarification domain object/lifecycle; answering that mutates CAF/Confidence or closes a finding without a run; a clarification that blocks/gates the user.

## 9. Provenance
Owner included clarification in R1 (2026-07-01). AI checked canon first, found the ratified `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPEC`, and drafted a **conformant, object-free** contract riding the recompute-stale backbone — escalating the prototype-vs-spec **surface** conflict rather than resolving it (Anti-Assumption). Owner ratifies; numbered at landing (DL-065).

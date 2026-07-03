# ENV-REV-001 — Condition Redline (for the dev lead)

**Status:** Non-canonical working note. Apply these edits to `REVISED_PHASE_1_FOUNDATION_STACK_PROPOSAL.md` on `foundation-phase-1` before the owner ratifies. **Date:** 2026-06-10

These are the four conditions from Review 001 / the draft decision, translated into concrete edits. Nothing here is binding until the owner ratifies.

---

## 1. Observability — state "complement," not "replace"

**Where:** §2 delta table (Observability row), §6, §8 Step 8, §12 item 3.

- §2 Observability row → change action from "**Replace/Complement**" to "**Complement** (LangSmith additive; OTel→Grafana retained)."
- §6 → make the resolution explicit, not a question: "LangSmith = runs/traces/cost layer **in addition to** OTel→Grafana. OTel→Grafana **remains** the source for service-health, queue/event-stream monitoring, and retention. CI gate-5 satisfied at app level: governed-output events + `CognitionHistoryRecord`(provider/model/version) + LangSmith run id."
- §8 Step 8 → "LangSmith self-host **alongside** OTel→Grafana" (drop "instead of (or alongside)").
- §12 item 3 → reframe from open question to "confirm complement (resolved: complement)."

## 2. Audit retention — mark proposed-pending (OPEN_TBD C1)

**Where:** §6, §9 DoD, anywhere "≥1-year audit" appears.

- Change "≥90-day ops / ≥1-year audit" → "≥90-day ops (ratified); **audit retention = proposed default, pending OPEN_TBD C1 / NFR matrix — do not treat as a requirement**."

## 3. LLM adapter — preserve Profile §5 controls

**Where:** §1 table (Agent/LLM row), §3 LLM/agents bullet.

- Add explicitly: the `/services/llm_provider` adapter implements **workload-based routing** (Complex Reasoning → premium; Structured Extraction/Classification/Summarization → cost-optimized; Agent Workflows → premium), **usage quotas**, and **model-consumption auditability** — per Profile §5. Confirm these are in the adapter contract, not just provider abstraction + selection.
- Note: provider/routing choice carries human approval per app `CLAUDE.md` (record the approval reference).

## 4. Terminology — "owner-provided," not "ratified"

**Where:** §2 table header, §11 footer, the closing footnote.

- Replace "the **ratified** Runtime Environment Constraint Profile" → "the **owner-provided** Runtime Environment Constraint Profile (pending DL-043 reconciliation)."
- §2 column header "Ratified profile" → "Owner-provided profile."

---

## Also flag (not blocking ratification)

- **`ORIENT_PHASE` stage matrix** still binds Mongo/Qdrant — fine until ratification; reconcile to the revised bindings once the profile is amended.
- **`±7` determinism band** in `ORIENT_PHASE` — confirm it traces to a ratified/proposed-adopted calibration default; the band is owner-pending per OPEN_TBD. If not yet adopted, label it placeholder.
- **Corrected diagram** — keep canonical names "Project MRI" / "CAF Overlay" (don't shorten); label Template / Guided Intake "pending owner scope ruling" rather than "deferred."

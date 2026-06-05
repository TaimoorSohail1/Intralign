# DL-045 (DRAFT) — Tool-Neutral Autonomous-Agent Terminology

**Status of this file:** **DRAFT · Proposed · Pending Owner Ratification.** Per `CLAUDE.md`, only the owner ratifies. Prepared at owner direction (the developer may use OpenAI Codex instead of, or alongside, Claude Code). **Adopts nothing; changes no rule.** This is a **terminology-generalization** proposal only.

> **Why:** DL-044 ratified the engineering-enablement layer using the name **"Claude Code"** in two places. The governance *rules* are agent-behavior rules and already apply to any autonomous coding agent — but the *naming* reads as if it mandates one vendor. Generalizing the language keeps the governance accurate as the tool choice opens up (Claude Code, Codex, or both), without weakening a single rule.

---

## What is proposed

Generalize tool-specific naming to **"autonomous coding agent"** (with Claude Code / OpenAI Codex as interchangeable examples) across two ratified documents, and record the AGENTS.md convention. **No rule, gate, invariant, or obligation changes** — only the noun.

### Constituent edits (on ratification)

- **(A) `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1`** — add a scope note that the standard governs **any** autonomous coding agent; replace "Claude Code MUST / MAY …" phrasing with "the autonomous coding agent MUST / MAY …". *Filename retained* (to avoid reference churn across the repo); an alias line documents the generalized scope. The doc already operationalizes the (vendor-neutral) Autonomous Implementation Control System.
- **(B) `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1` §9** — retitle "Claude Code at the Deployment Boundary (STOP conditions)" → "Autonomous coding agent at the Deployment Boundary (STOP conditions)"; same generalization of the MUST-STOP / MAY phrasing. The human-only-production rule is unchanged.
- **(C) Record the AGENTS.md convention** — note that `AGENTS.md` is the tool-neutral twin of `CLAUDE.md`: an `AGENTS.md` at the knowledge-base root and one seeded into the application repo (`03_architecture/engineering/starter_kit/AGENTS.md`) carry the same guardrails to Codex and other AGENTS.md-aware agents. (These two files already exist as non-canonical enablement artifacts; this constituent records them as the sanctioned mechanism.)

## What does NOT change

- Every MAY/MUST-NOT, STOP condition, CI gate, epistemic invariant, readiness gate, and the human-only-production rule — **identical**, regardless of tool.
- The application's runtime LLM routing (OpenAI primary / Anthropic fallback) — **unrelated** to which agent writes the code; not touched.
- No Doctrine, Constitution, contract, object/behavior model, or architecture content.

## Rationale

The enforcement surface (contract-traceability, positive+negative tests, the epistemic-invariant gate, branch protection, human review) is tool-agnostic by design — a non-conforming change fails the gate no matter which agent produced it. The governing docs should read the same way. Generalizing the noun removes a false impression of vendor lock-in and makes Codex (or a mixed-tool team) first-class without re-opening any decision.

## Disposition / Conditions

- **Disposition:** *(owner to record — Accepted / Accepted with Conditions / Deferred / Returned)*
- **Proposed condition:** filenames and contract ids are retained as-is (terminology-only; no path/reference churn); the change is recorded via changelog (CHG-NNN), not as an architecture change.
- **Supersedes:** Nothing. Refines the *wording* of two DL-044 constituents; the rules stand.
- **Status:** **Proposed — Pending Owner Ratification.**

## Owner checklist
- [ ] Approve (A) generalize Implementation Constraints wording (filename retained).
- [ ] Approve (B) generalize Deployment Governance §9 wording.
- [ ] Approve (C) record the AGENTS.md convention as sanctioned.
- [ ] On ratification: apply the wording edits, record CHG-NNN, set this file's status to Ratified.

---
*This draft proposes generalizing two DL-044 documents' "Claude Code" naming to "autonomous coding agent" (Claude Code / OpenAI Codex as examples) and recording the AGENTS.md convention as the tool-neutral twin of CLAUDE.md, so a developer may use Codex instead of or alongside Claude Code. It is terminology-only: no rule, gate, invariant, STOP condition, readiness gate, or the human-only-production constraint changes; filenames and contract ids are retained to avoid reference churn; and it adopts nothing — ratification is routed to the owner.*

**DL-045 (DRAFT) — Tool-Neutral Autonomous-Agent Terminology prepared. Pending Owner Ratification.**

# AGENTS.md — OSLO Application Repo (autonomous coding agent instructions)

> **Where this goes:** the **root of the application repo** (`oslo`). Codex (and any AGENTS.md-aware tool — Cursor, Copilot, Gemini CLI) reads this automatically before touching code. It is the tool-neutral twin of `CLAUDE.md`. **Keep it under ~32 KiB** (Codex's per-file budget). This file **summarizes and points to** the authoritative governance — it does not replace it.

## Authoritative sources (read these; this file is a digest)

The binding rules live in the **`oslo-knowledge-base`** repo, ratified under **DL-043** and **DL-044**:

- `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md` — the engineering standard (applies to **any** autonomous coding agent, not just Claude Code).
- `01_governance/AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md` — precedence, MAY/MUST-NOT, escalation, readiness gate.
- `01_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md` — branch/promotion/CI gates/STOP conditions.
- `03_architecture/contracts/` — the Wave A–E + U contract packages (Impl/QA/Obs triads).
- `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` + the DL-043/DL-044 decision entries.

**If this digest and an authoritative source ever differ, the source wins.**

## Prime Directive

**Build nothing without an approved contract.** Every change cites a contract id (`IC-WA-001`, `IC-WB-INFER`, …) in its PR. Un-contracted code must not be written.

## Hard rules (the epistemic boundary — never violate)

1. **One producer per output.** Each governed output is produced in exactly one responsibility module; other modules consume, never re-produce.
2. **Canonical vs Derived are separate layers.** The canonical store (Attested: receipts) and the derived projection (recomputable cognition) are **separate modules**. **Nothing in the derived layer writes to the canonical store as Attested.**
3. **Recompute appends, never overwrites.** A recompute appends a new `CognitionHistoryRecord`; it never updates or deletes one. Canonical stores are **append-only**.
4. **No Authority engine in R1.** Do **not** implement an Authority/governance engine or an `/authority` module — it is specified-but-inactive.
5. **OSLO never self-accepts.** User acceptance is recorded as a user-attested `UserAcceptanceRecord` / `PlanFact`; OSLO does not accept interpretations or assert world-truth.
6. **Explicit epistemic state.** Every cognition entity carries `epistemic_state` (`attested-*` | `derived`). No bare "knowledge" type that hides it.

## Canonical vocabulary (use these; legacy terms forbidden in new code)

Use: `AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`, `Finding`, `Issue`, `Recommendation`, `ClarificationRequest`, `Confidence`, `CAFAssessment`, `OutcomeConfidence`, `AcceptanceImpactAssessment`.

Forbidden: `GovernanceDecision`, `Authority*`, "Grounded/Candidate", and layer names (Context Plane / Knowledge Layer / Judgment / Communication) as **primary** identifiers.

## Code-tree (mirror the responsibility model)

```text
/oslo
  /backend                      # Heroku
    /responsibilities
      /perceive  /retain  /infer  /evaluate  /advise  /disclose  /adapt  /acceptance
    /platform                   # commodity: auth/RBAC, projects, settings, notifications-state
    /services
      /llm_provider             # provider abstraction (OpenAI primary / Anthropic fallback)
      /render  /persistence  /observability
    /contracts                  # generated Impl/QA/Obs contracts referenced by code
  /frontend                     # Vercel: MRI, Panels, Overview, Timeline, Notifications, Export
  /shared                       # epistemic types (Attested/Derived), domain vocabulary
  /tests                        # mirrors structure; positive AND negative suites
```
No `/authority` module. Platform concerns never mixed into responsibility modules.

## Dependencies

Ratified stack only: LangGraph; Postgres, Neo4j, MongoDB, Qdrant, Redis (behind repository interfaces); OpenAI primary / Anthropic fallback (behind the `/llm_provider` abstraction); Heroku/Vercel; OpenTelemetry/Grafana. **No new dependency or technology without human approval.**

## Tests (every increment)

Mandatory **positive AND negative** suites, mirrored to the code structure. Determinism-tiered assertions per Calibration Defaults: **exact** for records/rules; **±7 points & same band** for AI-numeric; **semantic** for AI-text. A suite without negatives is invalid. Self-verify against the contract's QA before marking done.

## STOP and escalate — do NOT guess — when:

1. No approved contract exists for the increment.
2. The change would invent ownership/object/workflow/persistence/governance/UI not in a contract.
3. Two same-tier sources conflict and precedence can't resolve.
4. The change introduces a new dependency/technology beyond the ratified stack.
5. The change touches an epistemic invariant (Derived-as-Attested, overwriting a receipt, OSLO accepting an interpretation, implementing Authority).
6. Environment binding for the increment is missing.

## Human approval REQUIRED before:

- Any canonical-store schema/persistence change or new migration.
- Any change to contracts, architecture, or the governance standard.
- **Production deployment / release promotion** (you may build, test, open PRs, deploy to Dev, propose Staging — you may **never** self-deploy to Production).
- Adopting or altering an LLM model/provider routing.

---
*This AGENTS.md is a tool-neutral digest of the OSLO autonomous-development governance (DL-043/DL-044). It lets Codex or any AGENTS.md-aware agent inherit the same guardrails Claude Code gets from CLAUDE.md. Authoritative rules live in the knowledge-base governance docs; where they differ, they win.*

## DL-047 vocabulary additions
Use: `SynthesizedPlanningModel`, `PlanningArtifact` (Derived, generated, user-editable), `ChatSession`/`ChatExchange`, `ReviewRequest`/`StakeholderResponse`, `SuggestedFix`. Rules: planning artifacts are **Derived** (never written Attested-as-truth; recompute appends a CHR); **OSLO never autonomously writes a Suggested Fix** (user applies); **Chat writes no canonical and changes no assessment**; a stakeholder response is **evidence** that triggers Deep Pass.

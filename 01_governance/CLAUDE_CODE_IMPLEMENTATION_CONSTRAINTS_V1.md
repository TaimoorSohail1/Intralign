# Claude Code Implementation Constraints & Code-Tree Convention v1

**Document Type:** Engineering Standard for Autonomous Development (governance) · **Status:** **Draft · Pending Owner Ratification** · **Date:** 2026-06-04
**Operationalizes:** `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md` (precedence, MAY/MUST-NOT, escalation, readiness gate) into **code-time** rules. **Binds to:** Cognitive Responsibility Architecture · DL-043 · Runtime Object/Behavior Models · Logical Data Model · Runtime Environment Constraint Profile (+ DL-043 reconciliations) · Calibration Defaults.

> **Purpose:** give Claude Code (and any engineer) the concrete coding rules, directory convention, and **stop/escalate/human-approval** boundaries so implementation realizes the architecture **without invention or drift**. This is the "how Claude Code writes code" standard the readiness audit found missing. Per `CLAUDE.md`, owner ratifies.

---

## 1. The Prime Directive

**Build only what an approved contract specifies; stop at anything undefined.** Every increment must trace to an **owner-approved contract package** (Impl/QA/Obs) → responsibility → object → behavior. No contract ⇒ no code (escalate). This is the hard gate from the Control System, enforced at code time.

## 2. Architecture & Layering Rules (code must mirror the model)

- **One module-area per responsibility.** Code is organized by **Cognitive Responsibility** (Perceive, Retain, Infer, Evaluate, Advise, Disclose, Act/Adapt), **not** by the legacy layer stack. Render is a separate **service** module.
- **One producer per output.** Each governed output is produced in exactly one responsibility module; other modules **consume**, never re-produce (the no-duplicate-ownership invariant in code).
- **Dependency direction = the responsibility chain.** `Perceive → Retain → Infer → Evaluate → Advise → Disclose`; cross-cutting **Act/Adapt** (recompute) and **integrity** utilities. **No upward or cyclic dependencies** (e.g., Retain must not import Infer).
- **Epistemic boundary in code:** the **canonical store layer** (Attested: receipts) and the **derived projection layer** (recomputable cognition) are **separate modules**; **nothing in the derived layer writes to the canonical store as Attested**, and **recompute appends, never updates** a Cognition History Record. **Authority module is absent in R1** (specified-but-inactive — do not implement an Authority engine).
- **Provider abstraction mandatory** (Environment Profile §5): all LLM calls go through one provider-abstraction module; no direct vendor SDK calls elsewhere; each call records `model_or_rule_version`.

## 3. Naming Conventions

- **Domain terms = canonical vocabulary**, never legacy: `AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`, `Finding`, `Issue`, `Recommendation`, `ClarificationRequest`, `Confidence`, `CAFAssessment`, `OutcomeConfidence`, `AcceptanceImpactAssessment`. **Forbidden in new code:** `GovernanceDecision`, `Authority*`, "Grounded/Candidate", layer names (Context Plane / Knowledge Layer / Judgment / Communication) as *primary* identifiers.
- **Epistemic state explicit:** any cognition entity/variable carries an explicit `epistemic_state` (attested-* | derived); never a bare "knowledge" type that hides it.
- **Files/modules:** `snake_case` files, `responsibility/` top-level dirs (§5); tests mirror source path with a `_test`/`.spec` suffix per stack convention.

## 4. Dependency Rules

- **Allowed deps = the ratified stack only** (Environment Profile): LangGraph (StateGraph + subgraphs), the chosen relational/doc/graph/vector/cache stores via repository interfaces, the LLM provider abstraction, OpenTelemetry. **New third-party dependencies require escalation** (§6).
- **Persistence behind interfaces.** No business/cognition module talks to a DB driver directly; all through a **repository interface** so the canonical-vs-derived store binding (R2) is enforced in one place and physical stores stay swappable.
- **No store-class violations:** derived modules may read canonical; canonical modules never depend on derived; the dependency-graph is **append-only over Attested nodes** (Neo4j) behind its repository.

## 5. Code-Tree Convention (the governed home for code)

*(Logical layout; exact root path/language scaffolding set at environment bind. Frontend → Vercel, backend → Heroku per Profile §6.)*

```text
/oslo
  /backend                      # Heroku
    /responsibilities
      /perceive                 # intake, normalization, readiness, user-action capture
      /retain                   # canonical store: Attested/CHR/UAR/PlanFact (append-only)
      /infer                    # Findings (+gap/conflict/risk)
      /evaluate                 # Issues, Confidence/Reliability/CAF/OutcomeConfidence
      /advise                   # Recommendations, Clarifications
      /disclose                 # epistemic-safe presentation contracts (server side)
      /adapt                    # recompute/stale backbone (append CHR; never overwrite)
      /acceptance               # user acceptance + reconciliation (non-governance)
    /platform                   # commodity (Category E): auth/RBAC, projects, settings, notifications-state
    /services
      /llm_provider             # provider abstraction (OpenAI primary / Anthropic fallback)
      /render                   # non-cognitive formatting service
      /persistence              # repository interfaces (relational/graph/doc/vector/cache)
      /observability            # OTel tracing, two-axis replay hooks, drift signals
    /contracts                  # generated Impl/QA/Obs contracts referenced by code
  /frontend                     # Vercel: MRI, Panels, Overview, Timeline, Notifications, Export
  /shared                       # epistemic types (Attested/Derived), domain vocabulary
  /tests                        # mirrors structure; positive AND negative suites (QA Governance)
```

- **Authority is intentionally absent** (no `/authority` module in R1).
- **Platform vs cognition separated:** commodity app concerns live under `/platform`, never mixed into responsibility modules.

## 6. AI Development Controls — Stop / Escalate / Human-Approval

**Claude Code MUST STOP and escalate (no guessing) when:**
1. **No approved contract** exists for the increment (Prime Directive).
2. A behavior would **invent** ownership/object/workflow/persistence/governance/UI not in a contract.
3. Two same-tier sources **conflict** (precedence can't resolve) — per Control-System ESC-0 discipline.
4. A change would **introduce a new dependency/technology** beyond the ratified stack.
5. A change touches an **epistemic invariant** (would let Derived be written as Attested, overwrite a receipt, accept an interpretation by OSLO, or implement an Authority engine).
6. **Environment binding** for the increment is missing.

**Human approval REQUIRED before:**
- Any **schema/persistence** change to the canonical store; any new **migration**.
- Any change to **contracts**, the architecture, or this standard.
- **Production deployment / release promotion** (deployment governance — separate, still to be authored).
- Adopting/altering an **LLM model/provider** routing.

**Claude Code MAY proceed autonomously** only within an approved contract, in the correct module, using the ratified stack, preserving invariants, with positive+negative tests — and must **self-verify** against the contract's QA before marking done.

## 7. Documentation & Test Standards

- **Every module** documents: its owning responsibility, the contract(s) it implements, its epistemic class (canonical/derived), and its invariants.
- **Tests are mandatory and dual:** **positive AND negative** per QA Governance (a suite without negatives is invalid); determinism-tiered assertions (exact for rule/record; band/semantic for AI) per Calibration Defaults; regression anchors for the standing invariants.
- **Observability is not optional:** each governed output emits its events + appends its Cognition History Record; two-axis replay hooks present.
- **Traceability comment/header** on each contract-implementing file: contract id → responsibility → object.

## 8. Conformance & Residual

- Operationalizes the Control System into code rules; introduces **no new architecture**. ✅
- **Residual (not this doc):** **Deployment Governance** (branch/promotion/rollback/secrets/change-control) is referenced in §6 but remains to be authored before first production deploy.

> ### Proposed Owner Resolution
> Ratify the Claude Code Implementation Constraints & Code-Tree Convention as the engineering standard governing autonomous development: responsibility-organized modules (no Authority module in R1), one-producer-per-output, canonical/derived store separation with append-only receipts, ratified-stack-only dependencies behind repository/provider interfaces, canonical vocabulary, and the stop/escalate/human-approval gates. Authorize Deployment Governance as the remaining pre-production artifact.

---

*This engineering standard operationalizes the Autonomous Implementation Control System into concrete code-time rules for Release 1: a Prime Directive that nothing is built without an approved contract; architecture/layering rules organizing code by Cognitive Responsibility (with Render as a service and no Authority module in R1), one producer per output, a strict downward dependency direction, and a code-level epistemic boundary separating the append-only canonical store from the recomputable derived projection (recompute appends, never overwrites); naming conventions enforcing canonical vocabulary and explicit epistemic state while forbidding legacy/Authority terms; dependency rules limiting code to the ratified environment stack behind repository and LLM-provider-abstraction interfaces; a governed code-tree convention (backend on Heroku organized by responsibility plus platform/services, frontend on Vercel, shared epistemic types, mirrored positive-and-negative tests); AI development controls specifying when Claude Code must stop and escalate (no contract, would invent, same-tier conflict, new dependency, epistemic-invariant touch, missing environment binding) and what requires human approval (canonical schema/migrations, contract/architecture changes, production deployment, model/provider changes); and documentation/test/observability standards (dual positive-negative tests, determinism-tiered assertions, mandatory emission/observability, traceability headers). It introduces no new architecture, flags Deployment Governance as the remaining pre-production residual, and routes ratification to the owner.*

**Claude Code Implementation Constraints & Code-Tree Convention v1 complete.**

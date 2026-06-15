# CLAUDE.md — OSLO Application Code (`code/`)

> **Where this is:** the OSLO application lives in `code/` inside the knowledge base
> (monorepo override — recorded as a decision/ADR, pending owner ratification; the
> ratified default is a separate `oslo` app repo). **Claude Code reads this file before
> touching code here.** It is a digest. **If this and an authoritative knowledge-base
> source differ, the source wins.**

## Authoritative sources (binding; this file is a digest)

Live in this same repo (paths per DL-051/DL-052 ownership zones):

- `00_owner/build_governance/` — owner-ratified build policy (QA/observability/deployment).
- `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md` — never infer a spec gap; escalate. **Read first.**
- `00_owner/CANONICAL_GLOSSARY.md` — one name per concept + banned synonyms.
- `30_engineering/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`
- `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` (amended per **DL-054**)
- `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- `00_owner/decisions/decision_log.md` — DL-043, DL-044, **DL-054** (stack), DL-051/052 (zones).
- `20_handoff/` — contracts/traceability seam; wave contract packages (`IC-WA-001`, …).

## Prime Directive

**Build nothing without an approved contract.** Every change cites a contract id in its PR.
Un-contracted code must not be written.

## Hard rules (the epistemic boundary — never violate)

1. **One producer per output.** Each governed output is produced in exactly one responsibility module; others consume.
2. **Canonical vs Derived are separate layers.** Nothing in the derived layer writes to the canonical store as Attested.
3. **Recompute appends, never overwrites.** A recompute appends a new `CognitionHistoryRecord`; canonical stores are append-only.
4. **No Authority engine in R1.** No `/authority` module — specified-but-inactive.
5. **OSLO never self-accepts.** Acceptance is a user-attested `UserAcceptanceRecord` / `PlanFact`.
6. **Explicit epistemic state.** Every cognition entity carries `epistemic_state` (`attested-*` | `derived`).

## Canonical vocabulary

Use: `AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`, `Finding`,
`Issue`, `Recommendation`, `ClarificationRequest`, `Confidence`, `CAFAssessment`, `OutcomeConfidence`,
`AcceptanceImpactAssessment`; (DL-047) `SynthesizedPlanningModel`, `PlanningArtifact`, `ChatSession`,
`ChatExchange`, `ReviewRequest`, `StakeholderResponse`, `SuggestedFix`.
Forbidden: `GovernanceDecision`, `Authority*`, "Grounded/Candidate", plane/layer names as primary identifiers.

## Code-tree (ratified — `code/` is the `/oslo` app root)

```text
code/                           # = the ratified /oslo app root
  backend/                      # Heroku
    api/                        # transport — REST /v1 (ADR-0003); app.py serves /openapi.json
                                #   deps · errors · v1/routers/ · v1/schemas/ (request inputs)
    orchestration/              # ⭐ one-stop: ALL LangGraph wiring + durable runs (ADR-0002)
                                #   state · checkpointer · registry · runner · graphs/ · subgraphs/
    responsibilities/           # perceive retain infer evaluate advise disclose adapt acceptance
    platform/                   # commodity: auth/RBAC, projects, settings, notifications-state
    services/                   # llm_provider, render, persistence, observability
    contracts/                  # Impl/QA/Obs contract refs cited by code
  frontend/                     # Vercel: MRI, Panels, Overview, Timeline, Notifications, Export
  shared/                       # epistemic.py (internal cognition) + entities.py (Data Model v1.2 DTOs)
  tests/                        # mirrors structure; positive AND negative suites
```
No `/authority` module. Platform concerns never mixed into responsibility modules.
`backend/api/` and `backend/orchestration/` are deviations the literal ratified tree omits
but canon requires (the API Contract Spec and env §1 durable runs) — recorded in ADR-0002/0003.

## Ratified stack only (DL-043 + DL-054)

LangGraph (domain-specific StateGraphs + reusable subgraphs); **Supabase** (Postgres + Auth/GoTrue +
RLS + pgvector + Storage — replaces standalone Postgres, MongoDB, Qdrant); **Neo4j** (graph); **Redis**
(sessions/cache/streams); LLM via **Pydantic AI + adapter** (OpenAI primary / Anthropic fallback) behind
`/services/llm_provider`; Heroku/Vercel; OpenTelemetry→Grafana **+ LangSmith** (complement). App runs
natively; only backing services are Dockerized. **No new dependency/technology without human approval.**

## Tests (every increment)

Mandatory **positive AND negative** suites, mirrored to structure. Determinism tiers per Calibration
Defaults: **exact** for records/rules; **±7 points & same band** for AI-numeric; **semantic** for AI-text.
A suite without negatives is invalid.

## STOP and escalate — do NOT guess — when

1. No approved contract exists for the increment.
2. The change invents ownership/object/workflow/persistence/governance/UI not in a contract.
3. Two same-tier sources conflict and precedence can't resolve.
4. The change introduces a new dependency/technology beyond the ratified stack.
5. The change touches an epistemic invariant (Derived-as-Attested, overwriting a receipt, OSLO self-accepting, Authority).
6. Environment binding for the increment is missing.

## Human approval REQUIRED before

- Any canonical-store schema/persistence change or new migration.
- Any change to contracts, architecture, or the governance standard.
- Production deployment / release promotion (never self-deploy to Production).
- Adopting or altering an LLM model/provider routing.

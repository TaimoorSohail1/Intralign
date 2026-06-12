# OSLO Application (`code/`)

The OSLO Release 1 application: a Python cognition backend + a React frontend, built
against the ratified canon in the surrounding knowledge base. This glossary fixes the
terms used in the code so they don't drift from each other or from canon.

## Language

**Orchestration**:
The wiring of a workflow — the LangGraph graph topology, durable runs, and run lifecycle.
Lives in one place (`backend/orchestration/`). It sequences work; it does not perform it.
_Avoid_: pipeline, engine, flow controller.

**Responsibility**:
A domain module that is the single producer of one governed output (perceive, retain,
infer, evaluate, advise, disclose, adapt, acceptance). Holds the business logic.
_Avoid_: service, handler, manager.

**Wiring vs work**:
The split this codebase is organised around: orchestration holds the wiring (how steps
connect), responsibilities hold the work (what each step decides). A graph node is thin —
it delegates to a responsibility.

**Governed output**:
A cognition entity OSLO produces under contract (Finding, Issue, Recommendation,
Confidence, …). Each is produced by exactly one responsibility (hard rule #1).

**Epistemic state**:
The mandatory marker on every cognition entity: `attested-*` (a canonical receipt) or
`derived` (a recomputable projection). Canonical and derived are separate layers.
_Avoid_: status, kind, knowledge type.

**Durable run**:
A graph execution whose state is checkpointed (Supabase Postgres) so it is resumable
after interruption/deploy/failure and its history is auditable.
_Avoid_: job, task run.

**DTO**:
A request/response shape exposed over the API. Produced by the render service from a
derived projection; the FastAPI OpenAPI schema is the single source the frontend's Orval
client is generated from.
_Avoid_: model (ambiguous with domain/Pydantic models), payload.

**Data Model entity**:
An external, API-exposed resource (Project, Artifact, Finding, Recommendation, AnalysisRun…)
defined by Data Model v1.2 and exposed verbatim over REST. Distinct from the internal
cognition that backs it: the `render` service maps internal cognition (a derived Finding +
its CHR) into the Finding *entity*. Entities live in `shared/entities.py`; internal cognition
types live in `shared/epistemic.py`.
_Avoid_: model, record (ambiguous with CHR).

**Backing service**:
A datastore the app runs against: Supabase (Postgres + Auth + pgvector + Storage), Neo4j,
Redis. The app runs natively; only backing services are containerised (DL-054).

# Revised Phase 1 Foundation — Environment Binding Revision (PROPOSAL)

**Decision ref:** ENV-REV-001 (engineering decision candidate) · **Document Type:** Environment-binding revision proposal (non-canonical) · **Status:** 🔒 **Engineering-locked candidate — PENDING OWNER RATIFICATION** · **Date:** 2026-06-10 · **Author:** Engineering (recorded by AI assistant)

> **Governance note (Authority Constraint, Framework 001A).** This revises the **owner-provided** `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` and the Database Ownership Matrix. Engineering proposes; **the owner ratifies.** This document is a *locked engineering position*, not ratified canon — it does not supersede the profile until the owner approves the items in §12. It lives in `90_research/` (non-canonical; informs but does not bind). The **platform architecture (DL-043) is unchanged** — this is an implementation/environment binding only, exactly the class of decision the profile governs.

---

## 1. Decision summary (the locked engineering position)

| Concern | Decision |
|---|---|
| Language / typing | **Python** + **Pydantic** (typed domain + epistemic types) |
| Agent / LLM layer | **Pydantic AI** (typed agents + structured outputs) over an **open-source LLM adapter** for provider abstraction + model selection; **standard SDK streaming** |
| Structured output | Production-grade structured-output enforcement via **Pydantic AI / Pydantic models** (LLM outputs validated against contract schemas; non-conforming → retry) |
| Orchestration / durability | **LangGraph** (StateGraph + reusable subgraphs; **Postgres checkpointer** for durable, resumable runs) |
| Relational + Auth + Vector + Object storage | **Supabase** (local **Docker** via the Supabase CLI) — Postgres, **Auth (GoTrue)**, **pgvector**, **Storage** |
| Graph | **Neo4j** (Dockerized) |
| Cache / sessions / streams | **Redis** (Dockerized) |
| Document store | **MongoDB — REMOVED** (roles reassigned to Supabase Storage + Postgres `jsonb`) |
| Vector store | **Qdrant — REMOVED** (replaced by Supabase **pgvector**) |
| Runs / traces / observability | **LangSmith** (self-hosted, Dockerized) for LLM/agent run + trace logging |
| Hosting | **Heroku** backend · **Vercel** frontend |
| **App execution** | **Backend API, agent code, and frontend run NATIVELY on the local machine — NOT in Docker.** Only backing services (Supabase, Neo4j, Redis, LangSmith) are Dockerized. |

---

## 2. Delta vs the ratified Runtime Environment Constraint Profile

| Component | Ratified profile | Revised decision | Action | Owner ratification? |
|---|---|---|---|---|
| Relational system-of-record | PostgreSQL | **Supabase Postgres** (local Docker) | Change provider (still Postgres) | ⚠️ confirm |
| Auth / identity | "centrally enforced" RBAC (build) | **Supabase Auth (GoTrue)** + RLS for Platform→Org→Project RBAC | Adopt managed auth | ⚠️ confirm |
| Semantic embeddings | **Qdrant** | **Supabase pgvector** | **Remove Qdrant** | ✅ required |
| Documents / unstructured | **MongoDB** | **Supabase Storage** (bodies) + Postgres `jsonb` (snapshots/projections) | **Remove MongoDB** | ✅ required |
| Knowledge graph | Neo4j | **Neo4j (Docker)** | Keep | — |
| Cache / sessions / event buffers | Redis | **Redis (Docker)** | Keep | — |
| LLM strategy | OpenAI primary / Anthropic fallback, provider abstraction, routing | **Pydantic AI + OSS adapter** (abstraction + model selection); OpenAI/Anthropic behind it; **streaming** | Implements the abstraction intent | ⚠️ confirm (LLM routing change needs human approval per app `CLAUDE.md`) |
| Observability | **OpenTelemetry → Grafana** | **LangSmith** (self-hosted) for runs/traces | **Replace/Complement** — see §7 | ✅ required |
| Hosting | Heroku + Vercel | Heroku + Vercel | Keep | — |
| App packaging | (compose only ever held datastores) | App services **run natively**, not Dockerized | Clarify (consistent) | — |

---

## 3. Revised stack by layer

- **Language & typing:** Python; **Pydantic** models for the shared epistemic types (`AttestedAssertion`, `CognitionHistoryRecord`, `Finding`, `Issue`, `Recommendation`, `Confidence`, `CAFAssessment`, …) and contract I/O.
- **Orchestration & durability:** **LangGraph** StateGraphs + reusable subgraphs; **Postgres (Supabase) checkpointer** → the durable, resumable Fast/Deep-Pass jobs (checkpoint-after-stage, resume-on-crash) the profile requires.
- **LLM / agents:** **Pydantic AI** for typed agent calls and **structured outputs** (the structured-output guarantee directly satisfies the analysis-engine requirement that LLM outputs validate against `analysis_contracts` schemas and retry on mismatch). An **open-source adapter** sits behind the canon-mandated `/services/llm_provider` interface for **provider abstraction + model selection** (OpenAI primary, Anthropic fallback) with **standard streaming**.
- **Data layer (Supabase, local Docker):** Postgres (relational + canonical append-only), **pgvector** (embeddings), **Auth/GoTrue** (identity), **Storage** (artifact bodies / objects).
- **Graph:** Neo4j (Docker).
- **Cache/queue:** Redis (Docker) — cache, sessions, Streams (orchestration), Pub/Sub (notifications).
- **Observability:** LangSmith (self-hosted Docker) for run/trace/token-cost logging.
- **Hosting:** Heroku (backend/workers, Python buildpack — no Docker), Vercel (frontend).

---

## 4. Local dev topology (what's Dockerized vs native)

```
NATIVE on the local machine (NOT Docker):
  • backend API (FastAPI/uvicorn or similar) + LangGraph agents (Python)
  • frontend (Vercel dev / npm) 

DOCKERIZED backing services (three separately-managed stacks):
  • Supabase      → via the Supabase CLI:  `supabase start`
                    (its own container set: Postgres + pgvector + Auth + Storage + Studio)
  • Neo4j + Redis → a small project docker-compose.dev.yml (two services)
  • LangSmith     → self-hosted from LangChain's provided compose
                    (multi-container: api, frontend, postgres, redis, clickhouse; LICENSE KEY required)

App connects to all backing services over localhost ports.
```

> **Note:** Supabase local and LangSmith self-hosted each bring their **own** Postgres/Redis. These are *infrastructure-internal* to those tools and are **separate** from OSLO's canonical Supabase Postgres and OSLO's Redis cache. Keep the connection strings distinct.

---

## 5. Data-layer mapping (where each role lives now)

| Data role | Ratified | Revised |
|---|---|---|
| Canonical append-only (`AttestedAssertion`, `CognitionHistoryRecord`, `UserAcceptanceRecord`, `PlanFact`) | Postgres | **Supabase Postgres** (append-only tables) |
| Orgs / Users / Projects / Findings·Issues·Recommendations indexes | Postgres | **Supabase Postgres** |
| Artifact bodies / unstructured content | MongoDB | **Supabase Storage** (object storage) |
| CHR `output_payload` snapshots · derived projection blobs | MongoDB | **Postgres `jsonb`** (or Supabase Storage for large blobs) |
| Semantic embeddings | Qdrant | **Supabase `pgvector`** |
| Knowledge-graph relationships | Neo4j | **Neo4j** |
| Sessions / cache / event buffers | Redis | **Redis** |
| Identity / authz | (app-built RBAC) | **Supabase Auth + RLS** + app-level Org/Project authorization |

---

## 6. Observability reconciliation (the key governance item)

The ratified profile mandates **OpenTelemetry → Grafana** plus the **Observability Governance** guarantees: governed-output event emission, **two-axis replay**, drift/trust signals, system/queue health, and **≥90-day ops / ≥1-year audit** retention.

- **LangSmith covers well:** LLM/agent **run + trace** capture, prompt/response inspection, **agent-execution replay**, and **per-run token/cost** (a strong fit for **cost governance, DL-048**). Each LangGraph run gets a LangSmith trace id.
- **LangSmith does NOT cover by itself:** system/service **health metrics**, **queue/event-stream** monitoring, the **epistemic two-axis replay of *derivations*** (that is app-level — `CognitionHistoryRecord` + the determinism harness), **governed-output event emission**, **drift/trust signals**, and the mandated **retention** policy.
- **Proposed resolution (owner to ratify):** LangSmith = the **runs/traces (agent-replay + cost)** layer. The **Observability Governance gate (CI gate 5)** is still satisfied at the **app level**: every governed output emits its events + appends a `CognitionHistoryRecord` that **records provider + model + version** (so the AI-assisted semantic replay tier is reproducible) and **references its LangSmith run id**. A lightweight system-metrics/health path (minimal OTel exporter or Prometheus, or LangSmith's own metrics) is retained to meet health-monitoring + retention. → **Decision needed: does LangSmith *replace* or *complement* OTel→Grafana?**

---

## 7. Proposed template changes (apply on ratification)

**`docker-compose.dev.yml`** (project-owned; Neo4j + Redis only — Supabase & LangSmith run from their own stacks):
```yaml
services:
  neo4j:
    image: neo4j:5
    environment: { NEO4J_AUTH: ${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD:-oslo_dev_pw} }
    ports: ["7474:7474", "7687:7687"]
    volumes: [neo4j_data:/data]
  redis:
    image: redis:7
    ports: ["6379:6379"]
    volumes: [redis_data:/data]
volumes: { neo4j_data: , redis_data: }
```

**`.env` deltas** (vs the starter-kit example):
```
# REMOVED: MONGO_*  and  QDRANT_URL
# Supabase (local via `supabase start`)
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=...                 # from `supabase status`
SUPABASE_SERVICE_ROLE_KEY=            # secret-store only; never commit
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
# Neo4j / Redis (Docker)
NEO4J_URI=bolt://localhost:7687
REDIS_URL=redis://localhost:6379
# LLM (Pydantic AI + OSS adapter; OpenAI primary / Anthropic fallback)
LLM_PRIMARY_PROVIDER=openai
LLM_FALLBACK_PROVIDER=anthropic
OPENAI_API_KEY=        # secret store
ANTHROPIC_API_KEY=     # secret store
# Observability — LangSmith (self-hosted)
LANGSMITH_TRACING=true
LANGCHAIN_ENDPOINT=http://localhost:1984
LANGSMITH_API_KEY=     # secret store
LANGSMITH_PROJECT=oslo-r1
LANGSMITH_LICENSE_KEY= # self-host license; secret store
# Calibration defaults (unchanged — DL-044 constituent C): replay tolerances, bands, drift...
```

**CI `ci.yml`** — gate sequence is **unchanged** (build · contract-traceability · tests · epistemic-invariant · observability · security). Gate-5 (Observability) wording updates to assert governed-output events + `CognitionHistoryRecord` with model/version + **LangSmith run linkage** + replay hooks.

---

## 8. Impact on Phase 1 build steps

- **Step 3 (seed):** `docker-compose.yml` shrinks to Neo4j + Redis; add `supabase init`/`supabase start`; add the LangSmith self-host compose; `.env` updated per §7.
- **Step 4 (services up):** "five datastores healthy" → **Supabase stack + Neo4j + Redis + LangSmith healthy** (four backing stacks); **MongoDB and Qdrant removed**.
- **Step 5 (scaffold):** code-tree unchanged (cognitive-spine modules, no `/authority`); add `supabase/migrations/` for the append-only canonical schema; `/services/llm_provider` = the Pydantic AI + adapter layer; `/services/persistence` = Supabase + Neo4j + Redis repository interfaces.
- **Step 7 (schema):** canonical append-only tables + RLS in **Supabase migrations**; embeddings via pgvector extension; derived projections in `jsonb`.
- **Step 8 (observability):** LangSmith self-host instead of (or alongside) OTel→Grafana — pending §6 decision.

---

## 9. Invariants & DoD — UNCHANGED

The epistemic + deployment invariants do **not** change and remain the Phase-1 exit gate:
- Canonical stores **append-only** (now Supabase Postgres); **canonical vs derived separation**; **no `/authority` module**; OSLO **never self-accepts**; **recompute appends** (never overwrites a CHR).
- Secrets never committed; **production human-only**; every change cites a contract id.
- DoD: backing services healthy; skeleton mirrors the spine; CI **blocks** on a forced failure in each gate; canonical append-only + derived separate; Staging live (synthetic), Production locked; a trace + two-axis-replay hook visible (now LangSmith + app-level CHR replay).

---

## 10. Production topology implication (flag)

Supabase-local and LangSmith-local are **dev-only**. Production must resolve to managed equivalents the backend (Heroku) connects to: **hosted Supabase** (or self-managed Postgres+pgvector+Auth+Storage), **managed Neo4j** (e.g., Aura), **managed Redis** (e.g., Heroku Redis / Upstash), and **hosted or self-hosted LangSmith**. This is a production-architecture decision beyond Phase 1 but should be acknowledged now.

---

## 11. Risks & open questions

1. **Observability coverage (highest):** does LangSmith satisfy the full Observability Governance gate, or is a complementary metrics/health path required? (§6)
2. **LangSmith self-host licensing/cost** (enterprise license key) — confirm for dev and prod.
3. **pgvector vs Qdrant at scale** — fine for R1 volumes; revisit if embedding scale grows.
4. **Supabase coupling** — consolidating relational+auth+vector+storage into one system simplifies dev but couples concerns; ensure clean migration/backup story.
5. **Auth mapping** — the canonical 5-role Platform→Org→Project RBAC must map onto Supabase Auth + RLS + app authorization.
6. **Data-model docs** — the Database Ownership Matrix and any MongoDB/Qdrant references in the Logical Data Model need owner-ratified updates.

---

## 12. Owner ratifications required (to make this binding)

1. **Amend `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1`** for: Supabase (Postgres+Auth+pgvector+Storage), **remove MongoDB**, **remove Qdrant**, **LangSmith** for observability, native (non-Docker) app execution.
2. **Update the Database Ownership Matrix** (§5 mapping).
3. **Resolve §6:** LangSmith *replaces* vs *complements* OTel→Grafana; confirm gate-5 coverage + retention.
4. **Approve the LLM provider/adapter** choice (Pydantic AI + OSS adapter) — app `CLAUDE.md` requires human approval for LLM provider/routing.
5. **Acknowledge §10** production topology direction.

**Recommended next step:** route ENV-REV-001 through Framework 001 (Proposal → Review → Decision). On owner ratification, update the Environment Profile + Database Ownership Matrix + starter-kit templates (`docker-compose`, `.env`, `ci.yml`) accordingly. Until then, the ratified profile remains in force.

---
*Non-canonical engineering decision candidate. Synthesized against the ratified Runtime Environment Constraint Profile, the Logical Data Model, Deployment & Observability Governance, and DL-043/044/048. Where this differs from a ratified/owner-provided source, the source wins until the owner ratifies this revision.*

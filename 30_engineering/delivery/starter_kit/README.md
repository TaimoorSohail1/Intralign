# Release 1 Env-Bind Starter Kit (reference templates)

**Document Type:** Engineering Enablement — reference templates (non-canonical) · **Status:** Reference under DL-044 · **Date:** 2026-06-04

> **These files seed the new application repository — they are NOT run from the knowledge base.** The `oslo-knowledge-base` repo is a constitutional knowledge system, not a software project. Copy these templates into the application repo (e.g. `oslo`) during Phase 1 of the onboarding runbook, then fill and adjust them there.

## Contents

| File | Goes where (in the app repo) | Purpose |
|---|---|---|
| `docker-compose.yml` | repo root | Local Dev stack: Postgres, Neo4j, MongoDB, Qdrant, Redis |
| `.env.example` | repo root → copy to `.env` | All config keys (no secret values); fill from owner-provided secrets |
| `ci-pipeline.yml` | `.github/workflows/ci.yml` | CI implementing the Deployment Governance gate sequence |

## How to use

1. Create the application repo (owner-owned; see runbook Phase 0).
2. Copy these three files in (rename `ci-pipeline.yml` → `.github/workflows/ci.yml`).
3. `cp .env.example .env` and fill values from the secrets the owner provisioned. **Never commit `.env`.**
4. `docker compose up -d` — confirm all five datastores are healthy.
5. Scaffold the LangGraph application skeleton against these services.
6. Bind the physical schema / env-profile R1–R5 to the logical data model (task #121).

## Why it's a template, not finished code

The gate **logic** (contract-traceability, invariant checks) depends on the application's actual structure, which doesn't exist yet. The CI file gives you the **gate sequence and failure semantics** mandated by Deployment Governance §4 with clearly marked `TODO` hooks where the real checks attach. Treat the placeholders as the contract for what each gate must enforce — not as optional.

## Grounding

- Stack & platforms: `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` (+ DL-043 reconciliation)
- Gate sequence & environment separation: `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1`
- Numeric config in `.env.example`: `RELEASE_1_CALIBRATION_DEFAULTS_V1`
- Build rules Claude Code follows: `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1`

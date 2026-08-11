# ADR 0001: Application shape and local platform

- Status: accepted for Slice 1 implementation
- Date: 2026-07-20

## Context

OSLO needs an independently deployable web client and API, invite-only identity, tenant isolation, background work in later slices, and a local environment that resembles production.

## Decision

Use a pnpm monorepo with Next.js/React in `apps/web`, FastAPI/Python in `services/api`, contract and UI packages under `packages`, and Supabase Local for PostgreSQL, Auth, Storage, Studio, and local email capture. Supabase SQL migrations are the database source of truth. Business rules live in capability modules and remain independent of Supabase adapters.

## Consequences

- The knowledge repository remains read-only input to implementation.
- RLS is mandatory on tenant data even though privileged writes go through FastAPI.
- Raw invitation tokens never enter the database; only SHA-256 digests are stored.
- Provider-specific code is isolated so hosted infrastructure can change without rewriting the invitation and onboarding domain.

#!/usr/bin/env bash
# OpenAPI → Orval drift gate (ADR-0003).
# The generated client is gitignored and regenerated from the backend's live
# OpenAPI schema in CI. The gate: after regenerating, the frontend must still
# typecheck — if the backend contract dropped/renamed a DTO the frontend uses,
# tsc fails. This keeps frontend usage in sync with the backend contract
# (== Data Model v1.2). Run in CI after the backend is up at $OPENAPI_URL.
set -euo pipefail

export OPENAPI_URL="${OPENAPI_URL:-http://localhost:8000/openapi.json}"

echo "Regenerating Orval client from $OPENAPI_URL ..."
npm run api:gen

echo "Typechecking frontend against the regenerated client ..."
npx tsc --noEmit

echo "Frontend is in sync with the backend OpenAPI contract."

#!/usr/bin/env bash
set -euo pipefail

: "${PORT:?Heroku must provide PORT}"

case "${APP_COMPONENT:-}" in
  web)
    exec pnpm --filter @oslo/web exec next start --hostname 0.0.0.0 --port "${PORT}"
    ;;
  api)
    exec python -m uvicorn oslo_api.main:app \
      --app-dir services/api/src \
      --host 0.0.0.0 \
      --port "${PORT}"
    ;;
  *)
    echo "APP_COMPONENT must be set to 'web' or 'api'." >&2
    exit 1
    ;;
esac

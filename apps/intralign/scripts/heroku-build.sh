#!/usr/bin/env bash
set -euo pipefail

case "${APP_COMPONENT:-}" in
  web)
    pnpm --filter @oslo/web build
    ;;
  api)
    echo "API staging app: no Node.js build required."
    ;;
  *)
    echo "APP_COMPONENT must be set to 'web' or 'api'." >&2
    exit 1
    ;;
esac

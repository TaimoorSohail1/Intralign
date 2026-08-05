#!/usr/bin/env bash
set -euo pipefail

if [[ "${APP_COMPONENT:-}" != "api" ]]; then
  echo "The worker process is only valid for APP_COMPONENT=api." >&2
  exit 1
fi

export PYTHONPATH="services/api/src${PYTHONPATH:+:${PYTHONPATH}}"
exec python -m oslo_api.analysis.worker

# Slice 0 — Live-Gemma Time-to-First-MRI proof (GO / NO-GO)

Discharges **DL-072 Condition 3** (and clears the **DL-070** Phase 1 latency sign-off): proves the
Fast-Pass **Time-to-First-MRI** against the **ratified <60s ceiling** on a **live internal-Gemma**
model — the one thing CI never exercises (its "live" e2e uses recorded fixtures, zero provider calls).

**This must run in the owner/engineering environment** — it needs a live Gemma Llama runtime + a
local Supabase stack. It cannot run in the assistant sandbox (no live model endpoint).

## Run

```bash
# 1) Supabase up (see apps/intralign/README.md — use the ports `supabase status` PRINTS, DL-054):
supabase start
export SUPABASE_URL=...  SUPABASE_SERVICE_ROLE_KEY=...  SUPABASE_DB_URL=...

# 2) internal Gemma Llama runtime up (OpenAI-compatible); enable live calls + base_url:
export OSLO_LLM_LIVE=1
export <INTERNAL_BASE_URL_ENV>=http://127.0.0.1:<port>     # name/value per .env.example (adapter.py)

# 3) (recommended) point at a REAL Tier-1 project (~20 artifacts / ~50k words); else a
#    synthetic placeholder load is used and flagged in the output:
export OSLO_LATENCY_PROJECT=/path/to/tier1_project.json

# 4) from apps/intralign/:
python scripts/latency_proof/run_latency_proof.py --runs 30 --out latency_proof_result.json
```

## Verdict

- **GO** — every run < 60s at the Tier-1 envelope (the ratified gate). Exit code 0.
- **NO-GO** — any run ≥ 60s. Exit code 1. **Stop**: file an engineering finding (where the budget is
  spent — retrieval / synthesis / Gemma inference), recommend remediation, and escalate to the owner
  **before** any further Wave C / Phase V work. Do not "fix by assumption."

`p50` / `p95` are printed and saved but are **reported-only** — the DL-046 targets (p50 ≤ 25s /
p95 ≤ 50s) are owner-TBD (OPEN_TBD A2). Only the <60s ceiling gates.

## Output

`latency_proof_result.json` is the evidence to attach to the Wave C exit-gate review
(`00_owner/decisions/WAVE_C_EXIT_GATE_REVIEW_DRAFT.md`). Capture the Grafana/Tempo trace IDs too.

## Notes / escalations

- **Envelope (OPEN_TBD A1):** Tier-1 / Free = ~20 artifacts · ~50k words · 1 active run
  (owner-confirmed 2026-06-05). Larger projects degrade gracefully and are out of this pass/fail.
- **E-harness:** the live chain builder may need a `prompt_suffix_for` argument that the recorded
  e2e supplies as a fixture concept; confirm the live builder signature before the official run.
- The script writes nothing to the repo and makes no canonical change (engineering tooling, `apps/intralign/`).

# OSLO Release 1 — Implementation (phase-by-phase)

**Document Type:** Execution Planning — implementation roadmap (non-canonical tracking) · **Status:** Reference under DL-044 · **Date:** 2026-06-04

> **Purpose:** a developer-facing, phase-by-phase home for execution. Each phase folder holds an `IMPLEMENTATION_PLAN.md` with its goal, the contracts in scope, dependencies, and the **expected outcomes / definition of done**. The phases mirror the **ratified build order** (Engineering Handoff Package §3, DL-044) — they don't invent scope; the contracts in `03_architecture/contracts/` remain authoritative.

## Phase map (dependency spine — build in order)

| Phase | Name | Responsibility focus | Contracts | Folder |
|---|---|---|---|---|
| **I** | Foundation & Environment | (build-time setup) | env-bind, CI gates, schema | `Phase_I_Foundation_and_Environment/` |
| **II** | Wave A — Backbone | Act/Adapt · Perceive · Retain | `IC-WA-00R`, `IC-WA-001`, `IC-WA-002` | `Phase_II_Wave_A_Backbone/` |
| **III** | Wave B — Understanding | Infer · Evaluate | `IC-WB-INFER`, `IC-WB-EVAL` | `Phase_III_Wave_B_Understanding/` |
| **IV** | Wave C — Advisory | Advise | `IC-WC-ADVISE` | `Phase_IV_Wave_C_Advisory/` |
| **V** | Wave U — User Acceptance | Perceive/Retain/Infer/Evaluate (additive) | `IC-WU-ACCEPT` | `Phase_V_Wave_U_User_Acceptance/` |
| **VI** | Wave E — Disclose Surfaces | Disclose (+ Render service) | `IC-WE-DISCLOSE` | `Phase_VI_Wave_E_Disclose_Surfaces/` |

## How to use

- Work phases **top to bottom**; each presupposes the one above (the spine). Phase I unblocks everything; Wave A 00R is the backbone the rest depend on.
- Within a phase, follow the **per-wave build loop** (`RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md` §3): pick contract → agent builds + tests → PR cites contract id → CI gates → review → owner approves → merge.
- A phase is **done** only when its plan's *Expected Outcomes* are demonstrable and its *Exit Gate* is owner-approved (DL-044 Condition 2: per-wave start is owner-authorized).
- These plans are **tracking artifacts**, not specs. If a plan and a contract disagree, the **contract wins** — raise it as a backlog item, don't edit scope here.

## Related

- Build order + readiness: `03_architecture/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md`
- Who-does-what + loop + testing: `03_architecture/RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`
- Tracker import (issues per contract): `03_architecture/engineering/LINEAR_IMPORT_README.md`
- Contracts (authoritative): `03_architecture/contracts/`

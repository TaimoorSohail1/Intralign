# Note to Engineering — Build, Test & Observe are captured per phase

**Date:** 2026-06-04 · **For:** the developer building OSLO Release 1 with Claude Code · **Scope:** `05_execution/implementation/`

Each phase's `IMPLEMENTATION_PLAN.md` is self-sufficient for all three engineering capabilities. You don't hunt the repo — the phase's **Context Manifest** links what you need, and its **Definition of Done** gates all three. If a plan and a linked source ever differ, the **source wins**.

## What every phase gives you

- **Build** — the wave's **contract(s)** (IC sections), the canonical **architecture spec**, the **object / behavior / logical-data models**, the **code-tree + agent rules** (`AGENTS.md` / `CLAUDE.md` / Claude Code Constraints), the ratified **stack** (env profile), and **build order + dependencies**. Phase I covers environment, schema, and CI bring-up.
- **Test** — the **Testing Strategy** + **determinism note**, each contract's **QA section** (positive **and** negative), the **fixture-library + subsystem test specs** for the relevant subsystem (Finding/Confidence in Phase III, Recommendation in Phase IV), and the **calibration tolerances**. *You generate the fixture data + golden files from these specs during the build.*
- **Observe** — the **Observability Governance** spec + the wave's **OBS contract** (events · audit · two-axis replay · drift/trust signals). **Every governed output must emit and be replayable** — and this is now an explicit DoD criterion, so a phase is not "done" until its outputs are observable. (Functional success ≠ observed success.)

## How it's gated

A phase passes its **owner exit gate** only when its Definition of Done holds — which now includes an **observability** criterion alongside the functional and invariant ones. The CI pipeline enforces the matching gates on every PR: build, contract-traceability, positive+negative tests, the **epistemic-invariant** gate, **observability**, and security.

## Two things that are build-time, not pre-provided (by design)

1. **Fixture data + golden files** — generated from the fixture-library *specs* as you build.
2. **The determinism/replay harness + invariant-gate assertions** — these are code you write (they're in the phase plans), not docs.

## Where to start

`START_HERE.md` (repo root) → the Engineering Handoff Package → the Onboarding Runbook → then work the phases in order, beginning with **Phase I (Foundation)** and **Phase II (Wave A backbone)**. Each phase plan is the single place that tells you what to build, how to test it, and what it must emit.

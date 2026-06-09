# AGENTS.md — OSLO Knowledge Base (autonomous coding agent instructions)

> **Tool-neutral entry point.** This repository's authoritative contributor rules live in **`CLAUDE.md`** (read automatically by Claude Code). This `AGENTS.md` exists so that **any** AGENTS.md-aware agent — OpenAI Codex, Cursor, Copilot, Gemini CLI — inherits the **same** governance. **The rules in `CLAUDE.md` are authoritative; read it now and follow it exactly.**

## What this repository is

A **constitutional knowledge system**, not a software project. It holds OSLO's doctrine, constitution, decisions (the DL ledger), contracts, and specifications. Treat all content as subject to governance review before adoption.

## Non-negotiables (full text in `CLAUDE.md`)

- **Only the repository owner may ratify, reject, supersede, or adopt canonical content.** An agent may analyze, check consistency, identify conflicts, and recommend — never decide.
- **Do not introduce new doctrine, frameworks, proposals, or backlog entries without owner direction.**
- **Do not resolve ontology/spec conflicts unilaterally** — surface them as backlog-style proposals.
- **Preserve canonical terminology; avoid terminology drift.**
- **Content precedence:** Doctrine > Constitution > Implementation (`10_product/`, `30_engineering/`). Source Material (`90_research/`, `raw/`) is non-canonical and never an implementation source.

## Where to start

1. `REPOSITORY_ARCHITECTURE.md` — repository map.
2. `00_owner/manifest/repository_manifest.md` — charter.
3. `00_owner/frameworks/framework_001.md` + `framework_001A.md` — governance procedure.
4. `00_owner/decisions/decision_log.md` — ratified decisions (through DL-044).
5. For **building the application**: `30_engineering/delivery/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` → `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`. The app-repo agent instructions are seeded from `30_engineering/delivery/starter_kit/AGENTS.md`.

*Authoritative source: `CLAUDE.md`. This file mirrors it for tool neutrality; where they differ, `CLAUDE.md` governs.*

## Drift-control files (external team / LLM — read before building)
- `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` — never infer a gap; escalate. **Read first.**
- `CANONICAL_GLOSSARY.md` — one name per concept + banned synonyms.
- `RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` — capability → contract → test → event.
- `OPEN_TBD_REGISTER.md` — every owner-decision-required value; DO NOT ASSUME.

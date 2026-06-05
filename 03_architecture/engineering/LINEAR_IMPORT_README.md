# Linear Import — Release 1 (README)

**Document Type:** Engineering Enablement — tracker import guide (non-canonical) · **Status:** Reference under DL-044 · **Date:** 2026-06-04
**File:** `oslo_linear_import_release1.csv` (in this folder)

> **The boundary, first:** Linear is the **work tracker** for visibility and management. This Git repository remains the **source of truth and governance ledger**. Linear issues *reference* contracts and decisions; they never replace them. Do not let a contract's canonical definition, or any DL decision, live only in Linear. If the two ever disagree, the repo wins.

---

## What's in the CSV

13 issues across 6 projects, covering the full Release 1 path:

| Project | Issues | Build order |
|---|---|---|
| **Phase 1 — Environment Bring-Up** | stack, CI gates, env-bind (R1–R5 + schema), Staging+secrets, observability | do first |
| **Wave A — Backbone** | IC-WA-00R (spine), IC-WA-001 (Perceive), IC-WA-002 (Retain) | 1 |
| **Wave B — Understanding** | IC-WB-INFER (Infer), IC-WB-EVAL (Evaluate) | 2 |
| **Wave C — Advisory** | IC-WC-ADVISE (Advise) | 3 |
| **Wave U — User Acceptance** | IC-WU-ACCEPT (additive) | 4 |
| **Wave E — Disclose Surfaces** | IC-WE-DISCLOSE (Disclose) | 5 |

Each issue's description cites its **contract id** and the **source file** in this repo, and restates the PR rule: *every PR cites the contract id; positive + negative tests + the epistemic-invariant gate are required.* This is what makes the chain **PR → Linear issue → contract** fully traceable, exactly as Deployment Governance requires.

Priorities encode the dependency spine: the **00R backbone is Urgent** (everything depends on it); the rest of Wave A is High; later waves are Medium. Each Wave E surface can be split into per-surface sub-issues later if you want finer tracking.

---

## How to import

1. In Linear: **Settings → Import / Export → Import CSV** (or the workspace "Import issues" flow).
2. Upload `oslo_linear_import_release1.csv`.
3. Map the columns: **Title, Description, Status, Priority, Labels, Project** map to Linear's fields of the same name. Assignee/Estimate/Cycle are intentionally left for you to set after import.
4. Confirm the **Projects** are created (six, above) and issues land under them.
5. After import, set **issue dependencies** (Linear "blocked by") to enforce order: Phase 1 blocks Wave A; WA-00R blocks WA-001/002; Wave A blocks Wave B; and so on down the spine. (CSV import can't express blocking relations, so this is a quick manual pass.)

---

## Connect Claude Code to Linear (optional but recommended)

So Claude Code can move issues and comment as it builds each wave, add the Linear MCP server:

```
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

This uses Linear's hosted MCP with OAuth — nothing to run locally. Once connected, Claude Code can transition issues (Backlog → In Progress → Done) and post progress comments during the per-wave loop. Keep the boundary in mind: Claude updates **tracker state** in Linear; it updates **canonical state** only in the repo, under governance.

---

## Label scheme

- `wave-a` … `wave-e`, `wave-u` — which wave
- `responsibility-perceive | retain | infer | evaluate | advise | acceptance | disclose | act-adapt` — owning responsibility
- `contract` — a buildable contract issue
- `phase-1`, `env-bind`, `infra`, `ci`, `data-model`, `observability` — environment bring-up work
- `backbone` — the 00R spine

---

*This guide explains importing the Release 1 waves and contracts into Linear as a work tracker while preserving the Git repository as the source of truth: a 13-issue, 6-project CSV spanning Phase 1 environment bring-up and the Wave A–E + U contracts in dependency order, each issue citing its contract id and source file and restating the PR-cites-contract rule; CSV import steps with a manual pass to set blocking relations along the spine; the optional Linear MCP connection that lets Claude Code update tracker state during the build; and the label scheme. Linear tracks; the repo governs.*

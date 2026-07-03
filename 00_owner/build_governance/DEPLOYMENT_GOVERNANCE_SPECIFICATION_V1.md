# Deployment Governance Specification v1

**Document Type:** Governance Specification (deployment & release control) · **Status:** **Ratified (with Conditions) under DL-044 constituent D — 2026-06-04** · **Date:** 2026-06-04
**Binds to:** Runtime Environment Constraint Profile (Heroku/Vercel · Dev→Staging→Prod · CI/CD · secrets) · Autonomous Implementation Control System (human-approval gates) · Claude Code Implementation Constraints · DL-043 invariants (canonical append-only). **Governs:** how Release 1 code moves from commit to production safely, and what Claude Code may and may not do at the deployment boundary.

> **Purpose:** the readiness audit's last open Critical was the absence of deployment governance. This defines branch strategy, promotion, approval gates, rollback, environment separation, secrets, and change control — at the **governance level** (policy + gates), binding to the environment stack without prescribing vendor minutiae. **Per `CLAUDE.md`, the owner ratifies; deployment to production is a human-approval action — Claude Code never self-deploys to production.**

---

## 1. Prime Rule

**Claude Code may build, test, and open changes; it may NOT promote to Production.** Every production deployment is a **human-approved** action (Control System: production deploy requires owner approval). Claude Code MAY operate autonomously through **Dev** and propose to **Staging**; **Staging→Production is human-gated.**

## 2. Branch Strategy

- **`main`** — always releasable; protected; no direct pushes. Changes land via reviewed PRs.
- **Feature branches** — `feat/<wave-or-capability>` (e.g., `feat/wave-b-finding`); one increment per branch, traceable to its **approved contract** (PR description cites contract id → responsibility → object).
- **Release branches** (optional) — `release/<version>` cut from `main` for a hardening window.
- **Hotfix** — `hotfix/<id>` from `main`, fast-tracked through the same gates at reduced scope.
- **Protection rules (main):** required PR review (human), required green CI, required contract-traceability check, no force-push, linear history preferred.

## 3. Environment Separation (Dev → Staging → Production)

| Environment | Purpose | Data | Promotion in | Who promotes |
|---|---|---|---|---|
| **Development** | active build/integration | synthetic/seed only | merge to integration branch | **Claude Code (autonomous, within contracts)** |
| **Staging** | pre-prod verification; mirrors prod topology | anonymized/synthetic; **never raw production canonical data** | from `main` after CI green | Claude Code **proposes**; human approves |
| **Production** | live | real canonical store | tagged release | **human only (owner-approved)** |

- **Strict separation:** no shared databases/secrets across environments; each has its own Postgres/Neo4j/Mongo/Qdrant/Redis instances and credentials.
- **Config per environment** (12-factor): all environment-specific values injected via config/secrets, never committed.

## 4. CI/CD Pipeline Gates (every change, in order)

1. **Build** — compiles/installs on the ratified stack.
2. **Contract-traceability gate** — the increment cites an **approved contract**; un-contracted code **fails** (Control System hard gate).
3. **Test gate** — **positive AND negative** suites pass (QA Governance); determinism-tiered assertions (exact for rule/record; band/semantic for AI) per Calibration Defaults. A suite without negatives **fails**.
4. **Invariant gate** — automated checks for the epistemic invariants: no Derived→Attested write, recompute **appends** (no overwrite of a Cognition History Record), no Authority module present in R1, canonical stores append-only. Violation **fails** (Critical).
5. **Observability gate** — each governed output emits its events + Cognition History Record; two-axis replay hooks present.
6. **Security gate** — dependency scan, secret-scan (no secrets in diff), SAST on changed code.
7. **Human review** — required approval before merge to `main`.
8. **Promote** — to Staging automatically on green `main`; to **Production only on human-approved tagged release.**

## 5. Database Migration Discipline (DL-043-bound)

- **Canonical stores are append-only.** Migrations **must not** destructively alter or delete Attested Assertions, Cognition History Records, or User Acceptance Records. Schema evolution is **additive** (new columns/tables/versions); historical rows are immutable.
- **Forward-only migrations** with a tested **rollback/contra-migration** for non-canonical/structural changes; canonical-data migrations require **explicit owner approval** and a verified backup.
- **Migrations run as a gated pipeline step**, never ad-hoc against Production; every migration is logged (provenance).
- Derived-projection stores (Redis cache, materialized views) may be **rebuilt** freely (they carry no authority).

## 6. Rollback & Recovery

- **Every production release is reversible:** tagged, with the prior release retained for immediate rollback.
- **Rollback procedure** is a human-approved action: redeploy prior tag; canonical data is unaffected (append-only); derived projections recompute.
- **Last-known-good** for cognition: on a failed recompute/deploy, the live Derived projection retains last-known-good (per the 00R backbone); no canonical loss.
- **Recovery objective:** restore service from the prior tag without touching the canonical record; never "fix forward" against Production canonical data without owner sign-off.

## 7. Secrets Management

- **No secrets in the repo or in any commit** (enforced by the security gate).
- Secrets injected via the platform secret store (Heroku config vars / Vercel env), **per environment**, least-privilege.
- **Rotation** policy for LLM provider keys and DB credentials; rotation is a human-approved operational action.
- Claude Code **never reads, prints, or commits** secret values; it references config keys only.

## 8. Change Control & Audit

- **Every production change traces to:** an approved contract (what), a PR + human approval (who/when), a CI run (verification), and a tagged release (artifact).
- **Deployment audit log** (per Observability Governance): release tag, contract refs, approver, timestamp, migration refs. Retained per the audit-retention policy (Calibration Defaults; ≥1 year pending compliance).
- **Architecture/contract changes** follow governance (DL ledger) — code does not change architecture; a deploy never ratifies a decision.

## 9. Autonomous coding agent at the Deployment Boundary (STOP conditions)

> **(DL-045)** "Claude Code" below = **any autonomous coding agent** (Claude Code, OpenAI Codex, …); these STOP/MAY rules and the **human-only-production** constraint apply identically regardless of tool.

The **autonomous coding agent MUST STOP / escalate** (no autonomous action) when: a change reaches **Staging→Production**; a **canonical-data migration** is involved; a **new secret/credential or provider/model change** is needed; a **CI gate fails** (no overriding gates); a **rollback** is required; or any change would touch an **epistemic invariant** (§4 gate 4). The agent **MAY** autonomously: build on feature branches, run CI, open PRs, deploy to **Dev**, and propose Staging — within an approved contract.

## 10. Conformance & Residual
- Closes the readiness audit's last open Critical (deployment governance absent). ✅
- **Environment-bound but vendor-light:** binds to Heroku/Vercel/CI from the Profile without prescribing pipeline YAML — concrete pipeline config is produced at environment-bind, governed by this spec.
- Introduces **no new architecture**; reinforces DL-043 invariants at the deploy boundary.

> ### Proposed Owner Resolution
> Ratify Deployment Governance v1: protected `main` + contract-traceable PRs; Dev→Staging→Production separation with **production deploy human-only**; CI gates (build · contract-traceability · positive+negative tests · epistemic-invariant · observability · security · human review); append-only canonical migration discipline; reversible tagged releases with last-known-good recovery; per-environment least-privilege secrets with no secrets in repo; full deployment audit trail; and the Claude Code deployment STOP conditions. Concrete pipeline configuration is produced at environment-bind under this governance.

---

*This Deployment Governance Specification closes the readiness audit's last open Critical by defining, at the governance level, how Release 1 code moves safely from commit to production: a protected always-releasable main with contract-traceable feature branches; strict Development→Staging→Production environment separation (synthetic/anonymized data outside production, isolated stores and secrets per environment) where Claude Code may act autonomously only through Dev and propose to Staging while Production deployment is a human-approved owner action; an ordered CI/CD gate sequence (build, contract-traceability, mandatory positive-and-negative tests with determinism tiers, an epistemic-invariant gate enforcing no-Derived-as-Attested / recompute-appends / no-Authority-module / append-only canonical stores, observability, security/secret-scan, and required human review); DL-043-bound migration discipline making canonical stores append-only and additive-only with owner-approved, backup-verified canonical migrations and freely-rebuildable derived projections; reversible tagged releases with last-known-good recovery that never fixes forward against production canonical data without sign-off; per-environment least-privilege secrets with none committed and human-approved rotation; a full change-control audit trail tracing every production change to an approved contract, approver, CI run, and release tag; and explicit Claude Code STOP conditions at the deployment boundary. It binds to the Heroku/Vercel/CI environment stack without prescribing pipeline minutiae, introduces no new architecture, reinforces the DL-043 invariants at deploy time, and routes ratification to the owner.*

**Deployment Governance Specification v1 complete.**

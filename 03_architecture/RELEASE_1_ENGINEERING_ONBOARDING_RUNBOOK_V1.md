# Release 1 Engineering Onboarding Runbook v1

**Document Type:** Engineering Enablement — Operational Runbook (non-canonical; operational guide) · **Status:** Reference under DL-044 (engineering-enablement layer) · **Date:** 2026-06-04
**Audience:** Repository owner (Idris) and the developer beginning autonomous implementation with Claude Code.
**Binds to (authoritative sources — this runbook never overrides them):** `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1` · `CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1` · `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1` · `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` (+ DL-043 reconciliation) · `RELEASE_1_CALIBRATION_DEFAULTS_V1` · the Wave A–E + U contract packages · DL-043 / DL-044.

> **What this is:** the step-by-step "who does what" to go from the ratified specification repository to running autonomous development. It is an *operational guide*, not governance — it adopts nothing and changes no decision. Where it appears to conflict with a ratified spec, the spec wins.
>
> **The one-sentence model:** the developer runs **Claude Code on their own machine** against a clone of this repo (specs + guardrails) and the new **application repo** (code); Claude Code builds freely through **Dev and pull requests**; **humans gate at merge-to-main and production deploy.**

---

## 0. Two repositories (important distinction)

| Repo | Contains | Status |
|---|---|---|
| **`oslo-knowledge-base`** (this repo) | Doctrine, constitution, decisions, contracts, specs — the **governance source of truth** | Exists, on GitHub, ratified through DL-044 |
| **`oslo` application repo** (to be created) | The actual application code Claude Code builds | **Does not exist yet** — created in Phase 1 |

The knowledge base is a *constitutional knowledge system, not a software project* — application code does **not** go in it. The starter-kit files under `03_architecture/engineering/starter_kit/` are **reference templates** that seed the new application repo; they are not run from here.

---

## 1. Phase 0 — Owner setup (before any code)

These are **your** actions. None requires the developer yet.

### 1.1 Claude Code access — decide the model (you do *not* create an account for the developer)
Claude Code is a CLI the developer installs and signs into with **their own** Claude account. Pick one:

- **Recommended (single developer): developer uses their own Claude Max plan.** Claude Code is included with individual Pro/Max. You provision nothing; you don't pay for their seat.
- **Team Premium / Enterprise** — only if you want centralized billing/admin (Team Premium is $100/seat/yr, **5-seat minimum**; Claude Code is *not* in the cheaper Team Standard tier).
- **API key** (console billing, pay-per-token) — best reserved for **CI/headless** runs, not interactive dev.

> Tell the developer: on Team plans, Claude Code token usage bills on top of the seat at API rates; and if an `ANTHROPIC_API_KEY` env var is set locally, Claude Code silently uses the API key instead of their subscription.

**Decision to record:** which access model, and who pays.

### 1.2 GitHub access
The knowledge base is already on GitHub (`github.com/idris-cmyk/oslo-knowledge-base`, fully pushed).

1. **Create the application repo** (e.g., `oslo` or `oslo-app`) under your account/org — or decide the developer creates it and you own it. (Per Deployment Governance, you should own the repo that deploys to production.)
2. **Add the developer as a collaborator with write access** on both repos (knowledge base = read is enough; app repo = write). For tighter control on the knowledge base, keep them **read-only** there.
3. **Enable branch protection on `main`** in the application repo: require a PR, require **your** review, require green CI, no force-push. *This is the control that makes "autonomous" safe — it's already mandated by Deployment Governance §2.*

### 1.3 Cloud accounts & ownership (decide who owns what)
Per the Runtime Environment Constraint Profile:

| Resource | Purpose | Recommended owner |
|---|---|---|
| **Heroku** (backend) | Staging + Production hosting | **You** (prod), dev gets Staging access |
| **Vercel** (frontend) | Staging + Production hosting | **You** (prod), dev gets Staging access |
| **OpenAI API key** (primary LLM) | model calls | **You** issue; injected as a secret, never committed |
| **Anthropic API key** (fallback LLM) | model fallback | **You** issue; injected as a secret |
| **Managed DBs** (Postgres/Neo4j/Mongo/Qdrant/Redis) for Staging/Prod | data stores | **You** (prod); Dev runs them locally via Docker |
| **Grafana / OTel backend** | observability | You or dev (Staging), you (prod) |

> For a contractor: you typically own production accounts and keys; the developer gets Dev (local) and Staging. Nothing production-grade should sit only in the developer's personal accounts.

### 1.4 (Recommended) Set up Linear and import the work
The waves/contracts are pre-packaged for Linear import — see `03_architecture/engineering/LINEAR_IMPORT_README.md` and the CSV beside it. Import gives you per-wave visibility and lets Claude Code update issues via the Linear MCP. **Boundary: Linear is the tracker; this repo stays the source of truth.** Linear issues *reference* contracts; they never replace them.

### Phase 0 checklist
- [ ] Claude Code access model decided (and who pays)
- [ ] Application repo created; developer granted write; knowledge-base access set (read)
- [ ] Branch protection enabled on app-repo `main` (you = required reviewer)
- [ ] Cloud accounts + ownership decided (Heroku, Vercel, OpenAI, Anthropic, DBs, observability)
- [ ] Linear set up and Release 1 imported (optional but recommended)

---

## 2. Phase 1 — Developer environment bring-up (the deferred build-time step, task #121)

These are the **developer's** first actions. This is where the environment-profile R1–R5 reclassifications and physical schema get bound — the one residual the handoff intentionally deferred to build time.

1. **Install & authenticate Claude Code** on their machine; sign into the chosen account (or set the API key only where intended).
2. **Clone both repos.** Point Claude Code at the app repo, with the knowledge base available for reference (the `CLAUDE.md` and Implementation Constraints are read automatically as guardrails).
3. **Seed the app repo from the starter kit** (`03_architecture/engineering/starter_kit/`): copy in `docker-compose.yml`, `.env.example` (→ `.env`, filled from the secrets you provided), and the CI workflow template (→ `.github/workflows/ci.yml` **in the app repo**).
4. **Stand up the local stack:** `docker compose up` brings up Postgres, Neo4j, MongoDB, Qdrant, Redis. Scaffold the LangGraph application skeleton.
5. **Wire the CI pipeline** to implement the Deployment Governance gate sequence (§4 below). Confirm each gate runs and can fail the build.
6. **Bind the environment profile (R1–R5) and physical schema** to the logical data model — Attested vs Derived stores, append-only canonical tables. (This is task #121; it is *build-time*, correctly not done before handoff.)
7. **Provision Staging** (Heroku/Vercel) with **synthetic/anonymized data only** and per-environment secrets. Production stays empty/locked until a wave is ready and you approve.
8. **Stand up observability** (OpenTelemetry → Grafana) so the two-axis replay + Cognition History events have somewhere to land.

### Phase 1 checklist
- [ ] Claude Code installed + authenticated
- [ ] Both repos cloned; app repo seeded from starter kit
- [ ] Local stack up (`docker compose up`) — all five datastores healthy
- [ ] CI pipeline implements all Deployment Governance gates (and can fail)
- [ ] Env-profile R1–R5 + physical schema bound (task #121)
- [ ] Staging provisioned (synthetic data, per-env secrets); Production locked
- [ ] Observability wired (OTel/Grafana)

---

## 3. Phase 2 — Autonomous build, wave by wave

Build order follows the dependency spine. **Start with the backbone**, then understanding, then advisory/acceptance, then surfaces.

| Order | Wave / Package | Responsibility | Contract IDs |
|---|---|---|---|
| 1 | **Wave A — 00R Recompute & Stale Backbone** (the spine) | Act / Adapt | IC/QA/OBS-WA-00R |
| 2 | **Wave A — 001 Artifact Intake** | Perceive | IC/QA/OBS-WA-001 |
| 3 | **Wave A — 002 Canonical Knowledge Retention** | Retain | IC/QA/OBS-WA-002 |
| 4 | **Wave B — Finding** | Infer | IC/QA/OBS-WB-INFER |
| 5 | **Wave B — Issue/Confidence/Reliability/CAF/Outcome Confidence** | Evaluate | IC/QA/OBS-WB-EVAL |
| 6 | **Wave C — Recommendation & Clarification** | Advise | IC/QA/OBS-WC-ADVISE |
| 7 | **Wave U — User Acceptance & Reconciliation** | Perceive/Retain/Infer/Evaluate (additive) | IC/QA/OBS-WU-ACCEPT |
| 8 | **Wave E — Disclose Surfaces** | Disclose (+ Render service) | IC/QA/OBS-WE-DISCLOSE |

### Per-wave loop (the repeating cycle)
For each wave, in order:

1. **You authorize the wave start** (DL-044 Condition 2): the wave's contract package is approved (already CONFORMANT) **and** the Control System readiness gate (D7) is satisfied for the increment.
2. **Claude Code reads the contract** (IC/QA/OBS triad) and builds on a **feature branch** (`feat/<wave>-<capability>`).
3. **Tests run:** mandatory **positive AND negative** suites, determinism-tiered per Calibration Defaults (exact for records/rules; ±7-pts/same-band for AI-numeric; semantic for AI-text).
4. **The epistemic-invariant gate runs:** no Derived→Attested write, recompute **appends** (never overwrites a Cognition History Record), no Authority module, canonical stores append-only.
5. **Claude Code opens a PR** citing the **contract id** (and the Linear issue). Un-contracted code fails the traceability gate.
6. **You review and approve** → merge to `main` → **auto-deploy to Staging**.
7. **Production deploy is you** — a human-approved tagged release. Then the next wave.

### What "autonomous" means here (precisely)
Claude Code MAY act on its own through **Dev and PRs**: build on feature branches, run CI, open PRs, deploy to Dev, propose Staging. Claude Code **MUST STOP / escalate** at: Staging→Production, any canonical-data migration, new secret/credential or provider/model change, a failing CI gate, a rollback, or anything touching an epistemic invariant. (Deployment Governance §9.)

### Phase 2 checklist (repeats per wave)
- [ ] Owner authorized the wave start (package approved + readiness gate)
- [ ] Built on a feature branch against the contract
- [ ] Positive + negative tests pass; invariant gate green
- [ ] PR cites contract id (+ Linear issue); human review approved
- [ ] Merged → Staging deploy green
- [ ] Owner-approved production release (when the wave is shippable)

---

## 4. The CI gate sequence (reference — implemented from Deployment Governance §4)

Every change, in order; any failure stops the change:

1. **Build** — compiles/installs on the ratified stack.
2. **Contract-traceability** — increment cites an approved contract; un-contracted code **fails**.
3. **Tests** — positive **and** negative suites pass; determinism tiers per Calibration Defaults. A suite without negatives **fails**.
4. **Epistemic-invariant** — no Derived→Attested write; recompute appends; no Authority module; canonical append-only. Violation = **Critical fail**.
5. **Observability** — each governed output emits its events + Cognition History Record; two-axis replay hooks present.
6. **Security** — dependency scan, **secret-scan** (no secrets in diff), SAST on changed code.
7. **Human review** — required approval before merge to `main`.
8. **Promote** — Staging auto on green `main`; **Production only on human-approved tagged release.**

---

## 5. Testing tooling — frameworks by QA validation layer (non-canonical guidance)

> **Status of this section:** practical starting point, **not governance.** `QA_GOVERNANCE_SPECIFICATION_V1` is deliberately tool-agnostic ("*no test frameworks, tooling… not how tests are built*") — it defines *what* to validate and the gates; this section suggests *how*. Swap any tool freely; the governance is unaffected.

**Division of labor:** Claude Code **authors** the tests (positive **and** negative, tracing each to its contract) and runs them; **standard frameworks** execute them; **CI** enforces the gates; **you** approve. You do **not** need a managed third-party QA service — the suite below plus CI covers Release 1, and much of it (invariant + replay) is custom anyway.

| QA validation layer (spec §3) | What it checks | Suggested framework(s) | Who authors |
|---|---|---|---|
| **1. Object** | object existence, single ownership, lifecycle, legal state transitions | unit tests — **pytest** (Py) / **Jest/Vitest** (TS) | Claude Code; dev reviews |
| **2. Behavior** | event generation, recompute (only info-change recomputes), state transitions | integration tests — pytest/Jest against the LangGraph graph | Claude Code; dev reviews |
| **3. Governance** | exposure/authorization decisions; **Authority generates nothing** | integration + targeted **negative** tests | **dev-owned negatives** + Claude |
| **4. Contract** | Impl acceptance present; QA pos+neg present & passing; Observability present | the wave's contract test module (pytest/Jest) + the **contract-traceability CI gate** | Claude Code; dev curates |
| **5. Regression** | prior-approved behavior/conformance/invariants preserved | full suite on every PR in CI; snapshot/golden-file tests | CI (automated) |

**Cross-cutting / specialized (add as the relevant wave lands):**

- **Determinism / two-axis replay** (exact for records & rules; ±7-pts & same-band for AI-numeric; semantic for AI-text — per Calibration Defaults) → **custom replay harness** (pytest fixtures pinning a baseline). No off-the-shelf tool does this; Claude builds it against the Observability contract.
- **Epistemic-invariant gate** (no Derived→Attested write; recompute appends; no Authority module; canonical append-only) → **custom assertion suite + static checks**, wired as CI gate 4. Custom by nature.
- **End-to-end / UI** (Wave E Disclose surfaces) → **Playwright** (recommended) or **Cypress**.
- **Security** (CI gate 6) → **CodeQL** or **Snyk** (SAST/deps) + **gitleaks** (secret-scan).
- **Load / performance** (optional, later) → **k6** or **Locust**.

**The independence rule, kept real:** the spec requires that *the implementer does not validate itself.* Because tests trace to the **contract** (the independent source of truth) and you approve, Claude authoring tests is acceptable — **but** have your developer **own and curate the negative tests and the invariant-gate assertions** (the Governance-layer and gate-4 rows above) rather than accepting Claude-generated assertions on both sides unchecked. That preserves the principle in spirit.

---

## 6. Quick reference — who owns each gate

| Action | Claude Code (autonomous) | Developer | Owner (you) |
|---|---|---|---|
| Build on feature branch | ✅ | ✅ | |
| Run CI / tests | ✅ | ✅ | |
| Open PR (cite contract) | ✅ | ✅ | |
| Deploy to **Dev** | ✅ | ✅ | |
| Propose **Staging** | ✅ (proposes) | ✅ | approves |
| Merge to `main` | ❌ | ❌ | ✅ (review) |
| Deploy to **Production** | ❌ | ❌ | ✅ (only) |
| Canonical-data migration | ❌ (stop/escalate) | proposes | ✅ approves |
| New secret / provider change | ❌ (stop/escalate) | proposes | ✅ approves |
| Authorize a wave start | ❌ | | ✅ (ratify) |

---

*This runbook is an operational guide for taking the DL-044-ratified Release 1 specification into autonomous implementation. It distinguishes the governance knowledge base (source of truth) from the new application repository (code), and sequences the work in three phases: Phase 0 owner setup (choosing a Claude Code access model — recommended that a single developer uses their own Max plan rather than the owner provisioning anything — granting GitHub access with branch protection on the application repo's main, deciding cloud-account ownership across Heroku/Vercel/OpenAI/Anthropic/datastores/observability, and optionally importing the waves into Linear as a tracker that references but never replaces the repo); Phase 1 developer environment bring-up (installing and authenticating Claude Code, cloning both repos, seeding the app repo from the starter kit, standing up the local Docker stack of the five datastores, wiring the CI gate sequence, binding the environment-profile R1–R5 reclassifications and physical schema — the deferred build-time step — and provisioning Staging with synthetic data while Production stays locked); and Phase 2 wave-by-wave autonomous build along the dependency spine (00R backbone first, then Perceive/Retain, then Infer/Evaluate, then Advise, then User Acceptance, then Disclose surfaces) under a per-wave loop where Claude Code builds freely through Dev and pull requests while humans gate at merge-to-main and at production deploy, with owner authorization required to start each wave per DL-044. It reproduces the Deployment Governance CI gate sequence and an ownership matrix, and overrides nothing — every authoritative rule remains in the ratified specifications it binds to.*

**Release 1 Engineering Onboarding Runbook v1 complete.**

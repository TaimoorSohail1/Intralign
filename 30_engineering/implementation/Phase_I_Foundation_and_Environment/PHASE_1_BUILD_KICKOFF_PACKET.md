# Phase I — Build Kickoff Packet (day-one onramp)

**Purpose:** the **first-day path** for the developer + autonomous coding agent (Claude Code / Codex — tool-neutral per DL-045) to start building OSLO Release 1. It **ties together** the existing onboarding docs into an ordered checklist; it does not replace them. · **Date:** 2026-06-05
**Read order before code:** `README.md` → `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` → `START_HERE.md` (the 6 docs + the DL-046–050 note) → `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`. This packet is the **checklist that operationalizes their Phase 1.**

---

## 0. Readiness at kickoff (what's true today)

**Ready to build (ratified + de-risked):**
- **Architecture:** the cognitive spine (Perceive→Retain→Infer→Evaluate→Advise→Disclose) — `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1` + Object/Behavior Models (DL-043).
- **Build spec:** the **Wave contracts** (IC/QA/OBS) + `RELEASE_1_CONTRACT_INVENTORY_V1` + the **Build/Test/Observe Traceability Matrix** (capability→contract→test→event).
- **Data model:** `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` (**current canonical** — v1/v1.1 are archived).
- **Numbers:** `RELEASE_1_CALIBRATION_DEFAULTS_V1` — cost budgets (DL-048 §4c), Tier-1 envelope, the **CAF/Confidence v0 formula params** (§4h), determinism tolerances — all owner-confirmed working values.
- **Drift control:** Anti-Assumption Protocol · Canonical Glossary · Open-TBD Register · `REPOSITORY_INDEX.md` · the **doc-integrity CI** (`tools/doc_integrity_check.py`, runs on push/PR).
- **Knowledge health ~95–96** (KIA-002), self-enforcing.

**Owner-pending but NOT build-blocking** (build around them; escalate per the Protocol if you hit one):
- CAF/Confidence **canonical** formula → build to the **v0** (`CAF_CONFIDENCE_V0_SCORING_FORMULA_V1`); calibrate from data post-launch.
- Numeric NFR pass/fail values → scaffold the metric; v0 defaults confirmed; calibrate from telemetry.
- Brand **type/logo/microcopy** (Q30) → build to the **design tokens** (`RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1`); designer delivery = a token-swap.
- Paid tiers 3–5, recipient experience, referral, exec-monitoring → **Release 2** (don't build in R1).

> **Phase I builds no product behavior.** Its job is to make building *possible and governed*: environment + enforcement scaffolding. Product behavior starts in Phase II (Wave A).

---

## 1. Day-0 prerequisites (owner, before the dev starts)
- [ ] GitHub repo for the **app** (separate from this knowledge base); **branch protection on `main`** (human-only merge/production).
- [ ] Cloud accounts: **Heroku** (app/datastores), **Vercel** (frontend), per the Runtime Environment Constraint Profile.
- [ ] Autonomous-agent account for the dev (Claude Code **or** Codex — DL-045; both read `CLAUDE.md`/`AGENTS.md`).
- [ ] Confirm the dev has read access to **this knowledge base** (reference) + write access to the **app repo** (build).

## 2. Day-1 ordered steps
1. **Read** (≈90 min): the README→Protocol→START_HERE 6 docs + the DL-046–050 note → Runbook Phase 1.
2. **Clone** the knowledge base (reference) and **create/clone the app repo** (where code lands).
3. **Seed the app repo** from `03_architecture/engineering/starter_kit/`: copy in `docker-compose.yml`, `ci-pipeline.yml` (→ `.github/workflows/ci.yml`), and **`CLAUDE.md` + `AGENTS.md`** at the app-repo root. Create `.env` from the values described in the starter-kit `README.md` (per-environment secrets; **never commit secrets**).
4. **`docker compose up -d`** — confirm the five datastores are healthy: **Postgres · Neo4j · MongoDB · Qdrant · Redis**.
5. **Scaffold the code-tree** per `starter_kit/CLAUDE.md` (and `AGENTS.md`): `/backend/responsibilities/{perceive,retain,infer,evaluate,advise,disclose}` + `/services`, `/shared`, `/frontend`, `/tests`. **No `/authority` module** (Authority is inactive in R1).
6. **Wire the CI gates** (`ci.yml`, per Deployment Governance): build · **contract-traceability** · tests · **epistemic-invariant** · observability · security. **Prove each can FAIL the build** (force a failure in each, confirm red).
7. **Bind the schema** to the **Logical Data Model (v1.2)**: canonical stores **append-only** (Attested · CognitionHistoryRecord · UserAcceptanceRecord · PlanFact); derived projection stores separate.
8. **Provision Staging** (synthetic data) + **observability** (OpenTelemetry → Grafana). **Production exists but stays locked/empty.**

## 3. First build target + order (Phase II onward)
- **First contract:** **Wave A `00R` — Recompute / Stale Backbone** (`WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md`) — the spine everything else depends on.
- **Build order:** Wave A **`00R → 001 → 002`** → **B** → **C** → **U** → **E** (Wave S folds in with B; Wave I with C/E). Per Handoff Package §3.

## 4. The build loop (every increment)
1. **Pick the contract** for the increment. **No contract → don't build it.**
2. **Point the agent at the contract.** It reads `CLAUDE.md` + the contract, builds in `/backend/responsibilities/<owner>/` on a `feat/...` branch, writes **positive + negative** tests, self-verifies.
3. **Open a PR citing the contract id** (e.g. `IC-WA-00R`). CI re-runs the gates.
4. **Human reviews** — validate the negative tests + invariant assertions; exploratory test; approve.
5. **Owner approves + merges → Staging.** **Production is human-only.**

## 5. Non-negotiable guardrails (the drift-control)
- **Every change cites a contract id.** Un-contracted code is a defect.
- **Escalate, don't invent.** A missing detail is commodity (build normally) / an Open-TBD (escalate) / a genuine gap (STOP + owner). Never guess. (`ANTI_ASSUMPTION_BUILD_PROTOCOL.md`)
- **Canonical vocabulary only** (`CANONICAL_GLOSSARY.md`); no banned synonyms; no layer names.
- **The five epistemic invariants** (START_HERE §1): Canonical = Attested · cognition is Derived · recompute **appends**, never overwrites · **no Authority engine in R1** · OSLO **never self-accepts**. Touching one = STOP-and-escalate.
- **Positive AND negative tests, always.** **Production is human-only** — no agent/pipeline self-deploys.

## 6. CI gates you'll hit
- **App repo (`ci.yml`):** build · contract-traceability · tests (pos+neg) · **epistemic-invariant gate** · observability · security (per `DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1`).
- **Knowledge-base repo:** the **doc-integrity gate** (`tools/doc_integrity_check.py`) — read-only; fails on broken active-tree links; warns on superseded refs / retired terms. (Reference only; doesn't gate app code.)

## 7. Day-1 done = exit gate to Phase II
- [ ] `docker compose up` → all five datastores healthy.
- [ ] App skeleton compiles; module layout mirrors the cognitive-spine code-tree; **no `/authority`**.
- [ ] CI runs on a PR and **blocks** on a forced failure in **each** gate.
- [ ] Canonical stores exist as **append-only**; derived stores separate.
- [ ] Staging deploys from green `main` (synthetic data); Production locked/empty.
- [ ] A trace + a sample two-axis-replay hook visible in Grafana.
- [ ] **Owner sign-off** → Phase II (Wave A 00R) may begin.

## 8. When you're stuck
**Stop and escalate to the owner** — don't resolve a spec conflict or fill a gap in code. Use `OPEN_TBD_REGISTER.md` (owner-decision values), `REPOSITORY_INDEX.md` (where is X?), and the contract's own QA section (acceptance). The contract is the spec; where a summary differs from a contract, **the contract wins**; where a doc differs from the ledger, **the ledger wins**.

---
*This kickoff packet is the day-one operational checklist for starting OSLO Release 1: it confirms the build-ready state (ratified cognitive spine, Wave contracts, traceability matrix, data model v1.2, calibration defaults including the CAF/Confidence v0 formula, and a self-enforcing doc-integrity CI), lists the owner-pending-but-non-blocking items to build around (canonical formula → v0, NFR numerics → confirmed defaults, brand → tokens, R2 scope → deferred), and gives the ordered Phase-I steps (read → clone → seed from the starter kit → docker compose up the five datastores → scaffold the cognitive-spine code-tree → wire and fail-test the CI gates → bind the append-only schema → provision locked Staging/Production with OTel→Grafana), the first build target (Wave A 00R) and build order, the per-increment build loop, the non-negotiable drift-control guardrails, the CI gates, and the exit-gate checklist to Phase II — operationalizing the existing START_HERE and Onboarding Runbook into a single first-day path.*

**Phase I Build Kickoff Packet — ready for the developer.**

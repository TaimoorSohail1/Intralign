# START HERE — Engineering Onboarding (read this first)

> ## 🛑 Step 0 — the front door: read [`ANTI_ASSUMPTION_BUILD_PROTOCOL.md`](ANTI_ASSUMPTION_BUILD_PROTOCOL.md) before anything else
> This is **the engineering team's front door.** The one rule: **never fill a specification gap by inference — escalate it.** A missing detail is either intentionally-commodity, an owner TBD ([`OPEN_TBD_REGISTER.md`](OPEN_TBD_REGISTER.md)), or a genuine gap to STOP and raise — never something to invent. Read it, then continue below.

**You are here because you're about to build OSLO.** This repo has ~500 documents. **You need about six of them to start.** This page is the 90-minute path from "confused" to "first PR open." Everything else is governance history you can ignore until you need it.

> Tooling note: you're using **Claude Code**. Claude Code auto-reads **`CLAUDE.md`** (and the equivalent `AGENTS.md`), so it inherits the build rules without you configuring anything. Your job here is to understand the *mental model* and the *build loop* — not to memorize the repo.
>
> **🛑 Drift control (keep these four open while you build).** This team builds with **Claude Code**, which auto-reads **`CLAUDE.md`** — these are linked there too:
> 1. **[`ANTI_ASSUMPTION_BUILD_PROTOCOL.md`](ANTI_ASSUMPTION_BUILD_PROTOCOL.md)** — never infer a gap; escalate it (**read first**).
> 2. **[`CANONICAL_GLOSSARY.md`](CANONICAL_GLOSSARY.md)** — one name per concept + banned synonyms.
> 3. **[`RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md`](RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md)** — capability → contract → test → event.
> 4. **[`OPEN_TBD_REGISTER.md`](OPEN_TBD_REGISTER.md)** — every owner-decision-required value; do not assume.

---

## 1. The mental model (5 minutes)

**What OSLO is:** a Planning Intelligence system. It ingests project artifacts, builds an evidence-grounded understanding, assesses it (findings, issues, confidence), advises (recommendations), and shows how understanding **changes over time**. The user decides; OSLO never asserts truth or accepts interpretations.

**The architecture is organized by responsibility, not by layer:**
`Perceive → Retain → Infer → Evaluate → Advise → Disclose`, with **Act/Adapt** (recompute) cross-cutting and **Render** as a non-cognitive service. **One producer per output.**

**Five rules you must never break in code (the epistemic invariants):**
1. **Canonical = Attested.** The canonical store holds only attributed, re-derivable records (append-only).
2. **Cognition is Derived.** Findings/Issues/Confidence/Recommendations are non-canonical and recomputable.
3. **Recompute appends, never overwrites.** Each emission adds a new `CognitionHistoryRecord`.
4. **No Authority engine in R1.** Do not build a governance/Authority module.
5. **OSLO never self-accepts.** User acceptance is recorded as a user-attested record; OSLO doesn't certify truth.

If you internalize only this section, you'll understand 80% of the codebase decisions.

---

## 2. The six documents to read (in order, ~60 min)

| # | Read | Why | Path |
|---|---|---|---|
| 1 | **Engineering Handoff Package** | the map: what's ratified, the build order, the hard rules, the readiness score | `03_architecture/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` |
| 2 | **Cognitive Responsibility Architecture Spec** | the canonical architecture (the model above, in full) | `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` |
| 3 | **DL-043 + DL-044** (+ skim **DL-046–049**, see note ↓) | the ratified decisions that define R1 scope, the engineering layer, and the operative additions since | `01_governance/decisions/decision_log.md` |
| 4 | **Engineering Onboarding Runbook** | who-does-what: access, environment bring-up, the per-wave build loop, testing flow | `03_architecture/RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md` |
| 5 | **CLAUDE.md** (agent rules — Claude Code reads it) | the rules Claude Code follows — read so you know what the agent is bound to (`AGENTS.md` is the identical tool-neutral twin) | `CLAUDE.md` · app-repo: `03_architecture/engineering/starter_kit/CLAUDE.md` |
| 6 | **Wave A 00R contract** (your first build target) | the first thing you'll implement — the recompute backbone | `03_architecture/contracts/WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` |

That's it. Stop there. Do **not** read `01_governance/doctrine/`, the ~480 other specs, `04_research/`, or anything marked *Historical / superseded* — they're the reasoning trail, not the build spec.

> **🔁 Then — the decisions & specs ratified SINCE DL-044 (skim, ~15 min; not optional — they change the build):**
> - **DL-046** — Fast/Deep analysis modes + the **< 60 s Time-to-First-MRI** gate (Wave B).
> - **DL-047** — the evidence→plan **synthesis engine** (Wave S) + OSLO Chat / CAF Review Requests / Suggested Fixes (Wave I).
> - **DL-048** — **cost governance / freemium unit economics** — per-tier token budgets enforced on the Fast/Deep engine (`Calibration §4c`); the `AI Spend Recorded` event.
> - **DL-049** — the **`Principal`** identity (`type: reviewer|user`, in-place promotion) — resolves external-stakeholder identity.
> - **Read when you touch them:** `02_product/specs/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1.md` (telemetry + AI economics) · `02_product/specs/ux/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` (design tokens / brand).
> - **Two canonical-definitions surfaces exist** — `01_governance/canonical_definitions/canonical_definitions.md` (governance-tier) and `constitution/10_canonical_definitions.md` (content-tier). **Where they conflict, Doctrine prevails (DL-036).**
> - **The ledger is the source of truth:** `decision_log.md` (DL-029–DL-049) + `changelog.md` (CHG-001–069) are current — **when in doubt, the ledger wins over any summary, including this page.** Also see **`REPOSITORY_INDEX.md`** (concept → canonical file).

---

## 3. What to ignore (permission granted)

- **`01_governance/`** beyond the decision log + AGENTS rules — it's the constitutional/governance system; you don't need it to write code.
- *(Do read when testing:* `02_product/specs/testing_fixtures/` holds the Testing Strategy, determinism note, and fixture/subsystem test specs — the per-phase manifests link the relevant ones.*)*
- **`02_product/specs/`** — ~130 product/UX specs; you'll pull the relevant ones *per wave* (Wave E references the UX specs), not up front.
- **`04_research/`, `raw/`, anything "Historical/superseded/secondary"** — never an implementation source.
- The DL ledger **below DL-043** — earlier decisions are superseded/contextual. **(But DL-046–049 *above* DL-044 ARE operative — see the note in §2.)**

When in doubt about scope: a doc only matters if a **contract** you're building points to it.

---

## 4. Your first 30 minutes of *doing* (environment)

> **Day-one checklist:** `05_execution/implementation/Phase_I_Foundation_and_Environment/PHASE_1_BUILD_KICKOFF_PACKET.md` — the ordered Phase-I onramp (readiness state, setup steps, first contract, guardrails, exit gate).

Follow the runbook's **Phase 1**. Short version:

1. Install Claude Code; sign in (your own Pro/Max). Clone this repo (reference) and the **app repo** (where you build).
2. Seed the app repo from `03_architecture/engineering/starter_kit/`: copy in `docker-compose.yml`, `.env.example` (→ `.env`), `ci-pipeline.yml` (→ `.github/workflows/ci.yml`), and **`CLAUDE.md` + `AGENTS.md`** at the root.
3. `docker compose up -d` — confirm Postgres, Neo4j, MongoDB, Qdrant, Redis are healthy.
4. Scaffold the LangGraph skeleton using the code-tree in `CLAUDE.md` (`/backend/responsibilities/...`).

---

## 5. The build loop (how every increment goes)

1. **Pick the contract** for the increment (start: Wave A **00R**, then **001**, **002**, then Wave B…). Build order is in the Handoff Package §3.
2. **Point Claude Code at the contract.** It reads `CLAUDE.md` + the contract, builds in `/backend/responsibilities/<owner>/` on a `feat/...` branch, writes **positive + negative** tests, and self-verifies.
3. **Open a PR citing the contract id** (e.g. `IC-WA-00R`). CI re-runs the gates automatically.
4. **You review** — validate the agent's negative tests + invariant assertions, do exploratory testing, approve.
5. **Owner approves + merges** → Staging. Production is owner-only.

The contract is the spec for each increment — **build nothing without one.** If a contract is ambiguous or two sources conflict, **stop and escalate to the owner**; don't resolve it in code (that's the governance rule, and it's also how you avoid building the wrong thing).

---

## 6. If you remember nothing else

- **Read 6 docs, ignore ~488.** (§2)
- **Every PR cites a contract id.** No contract → don't build it.
- **Never violate the five epistemic invariants.** (§1)
- **Build order:** Wave A `00R → 001 → 002` → B → C → U → E.
- **Stuck or ambiguous? Escalate to the owner**, don't guess.

*This is a non-canonical orientation aid. The authoritative sources are the documents it links to; where they differ, they win.*

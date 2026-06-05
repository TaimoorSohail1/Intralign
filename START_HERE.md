# START HERE — Engineering Onboarding (read this first)

**You are here because you're about to build OSLO.** This repo has ~500 documents. **You need about six of them to start.** This page is the 90-minute path from "confused" to "first PR open." Everything else is governance history you can ignore until you need it.

> Tooling note: you're using **Claude Code**. Claude Code auto-reads **`CLAUDE.md`** (and the equivalent `AGENTS.md`), so it inherits the build rules without you configuring anything. Your job here is to understand the *mental model* and the *build loop* — not to memorize the repo.
>
> **🛑 If you're an external team / a different LLM, read `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` FIRST.** The one rule: **never fill a spec gap by inference — escalate it.** Then keep four files open while you build: **`ANTI_ASSUMPTION_BUILD_PROTOCOL.md`**, **`CANONICAL_GLOSSARY.md`** (terms + banned synonyms), **`RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md`** (capability → contract → test → event), and **`OPEN_TBD_REGISTER.md`** (do-not-assume items).

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
| 3 | **DL-043 + DL-044** (decision log entries) | the two ratified decisions that define R1 scope and the engineering layer | `01_governance/decisions/decision_log.md` |
| 4 | **Engineering Onboarding Runbook** | who-does-what: access, environment bring-up, the per-wave build loop, testing flow | `03_architecture/RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md` |
| 5 | **CLAUDE.md / AGENTS.md** (agent rules) | the rules Claude Code follows — read so you know what the agent is bound to (`CLAUDE.md` and `AGENTS.md` carry the same rules) | `CLAUDE.md` · `03_architecture/engineering/starter_kit/AGENTS.md` |
| 6 | **Wave A 00R contract** (your first build target) | the first thing you'll implement — the recompute backbone | `03_architecture/contracts/WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` |

That's it. Stop there. Do **not** read `01_governance/doctrine/`, the ~480 other specs, `04_research/`, or anything marked *Historical / superseded* — they're the reasoning trail, not the build spec.

---

## 3. What to ignore (permission granted)

- **`01_governance/`** beyond the decision log + AGENTS rules — it's the constitutional/governance system; you don't need it to write code.
- *(Do read when testing:* `02_product/specs/testing_fixtures/` holds the Testing Strategy, determinism note, and fixture/subsystem test specs — the per-phase manifests link the relevant ones.*)*
- **`02_product/specs/`** — ~130 product/UX specs; you'll pull the relevant ones *per wave* (Wave E references the UX specs), not up front.
- **`04_research/`, `raw/`, anything "Historical/superseded/secondary"** — never an implementation source.
- The DL ledger below DL-043 — earlier decisions are superseded/contextual.

When in doubt about scope: a doc only matters if a **contract** you're building points to it.

---

## 4. Your first 30 minutes of *doing* (environment)

Follow the runbook's **Phase 1**. Short version:

1. Install Claude Code; sign in (your own Pro/Max). Clone this repo (reference) and the **app repo** (where you build).
2. Seed the app repo from `03_architecture/engineering/starter_kit/`: copy in `docker-compose.yml`, `.env.example` (→ `.env`), `ci-pipeline.yml` (→ `.github/workflows/ci.yml`), and **`AGENTS.md` + `CLAUDE.md`** at the root.
3. `docker compose up -d` — confirm Postgres, Neo4j, MongoDB, Qdrant, Redis are healthy.
4. Scaffold the LangGraph skeleton using the code-tree in AGENTS.md (`/backend/responsibilities/...`).

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

# PROPOSAL — Stale `0X_` Path-Reference Repair (DL-051 follow-through)

- **Status:** **Bucket 1 DISPOSITIONED** — owner-approved 2026-06-18 ("approve Bucket 1, clerical under DL-051"); realized as **CHG-103** (130 refs across 12 `30_engineering/` files; doc-integrity gate green). Buckets 2 (owner-canon cross-refs) and 3 (historical/ledger — do-not-touch) remain open per §6. AI-authored proposal; owner ratified the disposition.
- **Framework 001 stage:** Proposal (Backlog → **Proposal** → Review → Decision → Change → Changelog).
- **Class:** Clerical / traceability. **No doctrine, constitution, contract, or scope content changes** — reference paths only.
- **Source / Finding:** Wave E (Phase VI) scope review, 2026-06-18 — the `30_engineering/implementation/` tree points at the pre-DL-051 `01_/02_/03_` directory names.
- **Supporting artifact:** `WAVE_E_DL051_PATH_MIGRATION_INVENTORY.md` (per-line inventory of the 107 implementation-tree references).

---

## 1. Finding

After **DL-051** moved all content into ownership zones (`00_owner/` · `10_product/` · `20_handoff/` · `30_engineering/`), the legacy `01_governance/` · `02_product/` · `03_architecture/` directories no longer exist. A repo-wide scan finds **859 `0X_` references across 83 files**. **These are NOT uniformly fixable** — see §2. The triggering case (the `30_engineering/implementation/` tree, 107 refs, plus the Onboarding Runbook, Handoff Package, and starter_kit) is genuinely stale: an engineer follows broken links to the authoritative contracts, specs, models, and agent rules.

**§4 precondition — RESOLVED (in-repo consumption confirmed).** The Onboarding Runbook states the developer "clones this repo (specs + guardrails)" for reference and the implementation plans are "a developer-facing, phase-by-phase home for execution"; the `oslo` application repo holds **code only** and **does not exist yet**. So these docs are read **in this repo** — the migration is valid (fix the pointers here), not an app-repo convention.

## 2. Scope — three buckets (the core of this proposal)

A blind repo-wide rewrite would **corrupt the record**. The 859 refs must be separated by intent:

**Bucket 1 — FIX NOW (clerical, low-risk, ~167 refs in `30_engineering/`).** Live forward-pointers engineers follow: the 8 phase `IMPLEMENTATION_PLAN.md`s + `README.md`, `RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md`, `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`, `LINEAR_IMPORT_README.md`, and `starter_kit/CLAUDE.md` + `AGENTS.md`. *(starter_kit files are copied into the app repo and resolve against the knowledge-base clone, so they must point at real zone paths too.)*

**Bucket 2 — FIX SEPARATELY (owner-canon, careful review).** Live cross-references inside canon: `00_owner/canonical_definitions/canonical_definitions.md` (~90), `00_owner/ontology/ontology_registry.md` (~74), build-governance precedence ladders (`AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md`, etc.). Genuinely stale, but this is **owner canon** — it warrants its own ratified pass, not a clerical sweep, and a separate decision.

**Bucket 3 — DO NOT TOUCH (historical / descriptive).** Rewriting these falsifies the record:
- **Append-only ledgers:** `00_owner/changelog/changelog.md` (138), `00_owner/decisions/decision_log.md` (125) — they record paths *as they were when authored*.
- **Restructure-description docs** where the old path is the subject: `REPO_RESTRUCTURE_MIGRATION_MAP_DRAFT.md`, `proposal_003_restructure_disposition.md`, `90_research/REPOSITORY_REORGANIZATION_PROPOSAL_V1.md`, `10_product/scope/DOCUMENT_CONSOLIDATION_PLAN.md`, `RELEASE_1_DOCUMENTATION_SIMPLIFICATION_REPORT.md`, and pre-DL-051 dispositions/audits.

**This proposal seeks approval for Bucket 1 only.** Buckets 2 and 3 are documented here so the boundary is explicit and no future sweep crosses it.

## 3. Verified mapping (applies to Bucket 1)

**A. Clean 1:1 prefixes:**

| OLD prefix | NEW prefix |
|---|---|
| `03_architecture/contracts/` | `20_handoff/contracts/` |
| `03_architecture/runtime_models/` | `30_engineering/runtime_models/` |
| `03_architecture/environment/` | `30_engineering/environment/` |
| `03_architecture/specifications/` | `30_engineering/specifications/` |
| `03_architecture/decisions/` | `00_owner/architecture_decisions/` |
| `03_architecture/` (delivery roots: handoff, runbook, LINEAR import) | `30_engineering/delivery/` |
| `03_architecture/engineering/starter_kit/AGENTS.md` | `30_engineering/delivery/starter_kit/AGENTS.md` |
| `01_governance/` (QA/observability/impl-constraints) | `00_owner/build_governance/` |
| `01_governance/decisions/` | `00_owner/decisions/` |
| `02_product/specs/ux/` | `10_product/experience/` |
| `02_product/specs/testing_fixtures/` | `30_engineering/testing_fixtures/` |

**B. Split folders (DL-051 fragmented these across zones — remap per-file, verified to exist):**

| OLD path | NEW path |
|---|---|
| `02_product/specs/models/{CONFIDENCE_MODEL_V2, RELIABILITY_MODEL_V2, CAF_SCORING_MODEL_V2}.md` | `30_engineering/scoring/` |
| `02_product/specs/models/RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` | `10_product/domain/` |
| `02_product/specs/data_api_nfr/RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` | `30_engineering/analysis_engine/` |
| `02_product/specs/data_api_nfr/RELEASE_1_PERFORMANCE_AND_NFR_SPECIFICATION_V1.md` | `10_product/acceptance/` |
| `02_product/specs/FAST_DEEP_WORKFLOW_PACK/*` | `30_engineering/analysis_engine/` |

## 4. Framework 001A Review

- **Findings:** 859 stale refs repo-wide, but only **Bucket 1 (~167, all in `30_engineering/`)** is in-scope clerical repair; in-repo consumption confirmed; all Bucket-1 targets located and verified, including the two split folders remapped per-file.
- **Concerns:** a naïve repo-wide `sed` would (a) rewrite append-only ledgers = falsified history, and (b) edit owner canon without review. Both are averted by the bucket boundary. Bucket 1 alone leaves Bucket 2's canon cross-refs stale — acceptable as a sequenced follow-on; flag it so it isn't forgotten.
- **Dependencies:** DL-051 (zone reorg) + DL-052 (zone splits) — this is their follow-through; doc-integrity gate must stay green; no contract/doctrine dependency.
- **Recommendation:** approve **Bucket 1** as a single clerical migration via the §3 mapping; land on a branch → green doc-integrity gate → owner merge; dispose as a **clerical changelog entry under DL-051** (no new DL needed). Open **Bucket 2** as a separate owner-reviewed item; ratify **Bucket 3** as out-of-bounds (historical record).
- **Status:** Ready for owner decision; §4 precondition cleared.

## 5. Risk & rollback

Bucket 1 is clerical and low-risk: no content or file-location change, every target verified, fully diffable, landed via branch → PR → gate → owner merge. Reversible by reverting the PR. The do-not-touch boundary (§2) protects the canonical record.

## 6. Owner decision required

1. **Approve Bucket 1** (the ~167 `30_engineering/` operational refs) via the §3 mapping.
2. **Disposition:** clerical changelog entry under DL-051, **or** assign a new DL.
3. **Bucket 2** (owner-canon cross-refs): authorize a separate reviewed pass now, or defer.
4. **Bucket 3**: confirm it stays untouched.

On owner direction (items 1–2), this routes through Framework 001 to a branch → PR → green gate → owner merge (one changelog entry).

# Repository Architecture

> **Organized by ownership zone (DL-051).** This repository is filed by *ownership*, not topic:
> `00_owner/` (doctrine, constitution, frameworks, decisions, canonical definitions, glossary/ontology,
> build-governance — owner-only) · `10_product/` (product-authoritative) · `20_handoff/` (co-governed
> seam: contracts, traceability, interfaces) · `30_engineering/` (engineering-authoritative) ·
> `90_research/` (non-canonical). Precedence **Doctrine > Constitution > Implementation** is unchanged;
> all canonical change routes through Framework 001 and the **owner** ratifies. See `ZONE_GROUNDING_RULES.md`
> for the filing rules. *(Some narrative layout descriptions below predate the move and read against the
> old `01–05` domains; path references are current.)*

This document explains how the OSLO knowledge base is organized and how to contribute to it. It is written for contributors and reviewers.

## The One-Sentence Version

OSLO is a doctrine-centered repository: doctrine defines what is true; everything else either expresses doctrine, implements doctrine, or governs how doctrine evolves.

## The Six Principles

### 1. Doctrine defines truth.

`00_owner/doctrine/` contains the canonical truth of OSLO. When the repository disagrees with itself, doctrine wins.

### 2. Constitution operationalizes doctrine.

`00_owner/constitution/` translates doctrine into Articles that govern UX, interaction, and product behavior. Articles inherit authority from doctrinal grounding.

### 3. Implementation realizes doctrine.

`10_product/` and `30_engineering/` realize what doctrine asserts. Concepts introduced here without doctrinal anchor are provisional.

### 4. Governance controls repository evolution.

`00_owner/decisions/`, `backlog/`, `changelog/`, and `frameworks/` govern how the repository changes. Governance objects do not assert doctrine.

### 5. Source Material informs but does not bind.

`90_research/` contains transcripts and historical artifacts. Non-canonical.

### 6. Subsystems must anchor to canonical content.

`00_owner/subsystems/` holds sub-categories that declare their doctrinal scope, constitutional articulation, and implementation specs.

## Multi-Repo Topology (objective-organized repos)

This repository — **`oslo-knowledge-base`** — is the **governed canon for the OSLO *product*** (dev / product / architecture). Intralign's other objectives live in **separate, physically-independent repositories**, organized by objective. The first is **`intralign-gtm`** — **Intralign's (the company's) go-to-market** repo (narrative, launch, campaigns, sales enablement, growth, GTM metrics). Note the level: **OSLO is the product; Intralign is the company going to market**, so GTM is company-scoped and currently centers on OSLO but may span future products.

**Dependency direction is one-way:** objective repos (e.g. `intralign-gtm`) **reference this repo's OSLO product canon** (positioning, tiers, pricing, capabilities) read-only; **this repo never depends on them.** Where an objective repo and this canon disagree on a product fact, **this canon wins** (ledger-wins). Canonical product/architecture/governance content is **not duplicated** into objective repos — it is **referenced** (links / a source-dependency index, pinned for campaigns where a fact must not drift). Each objective repo carries its **own lightweight governance** appropriate to its purpose; it does **not** inherit this repo's doctrine/constitution/decision-log apparatus.

Above the objective repos sits **`intralign-company`** — the **company operating system** (company-level decisions `CD-###`, strategy, customer-insight synthesis). It provides **parent context** and **creates no dependency** in either direction: this product repo does not depend on it, and it only *references* product canon (e.g. telemetry definitions) one-directionally. Note the distinct ledgers: company decisions are `CD-###` (in `intralign-company`); **product** decisions remain `DL-###` (here).

## Canonical-Architecture Precedence (read before trusting any architecture doc)

When two architecture documents disagree, this is the order (KIA-9, 2026-06-05):

1. **Cognitive Responsibility Architecture Spec** (`30_engineering/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`) + the **Runtime Object/Behavior Models** + the **Wave contracts** — **canonical** (ratified DL-043). The runtime is the **cognitive spine** (Perceive→Retain→Infer→Evaluate→Advise→Disclose), **not** layers.
2. **`OSLO_ARCHITECTURE_BASELINE_V1.md`** — a **secondary** representation (DL-043); informative, not authoritative on conflict.
3. **`30_engineering/legacy_layer_engineering/`** — **deprecated** layer model; do **not** build from it (see its README).
4. **Reorganization / simplification proposals** (`REPOSITORY_REORGANIZATION_PROPOSAL_V1.md`, `…SIMPLIFICATION_PLAN.md`, `…SIMPLIFICATION_REPORT.md`) — **PROPOSED, not necessarily applied**; never a build source.

The **decision log + changelog** are the live ledger; where any architecture summary differs from the ledger, the ledger wins.

## Where Do I Put Things?

| What you have | Where it goes |
|---|---|
| A foundational claim about OSLO | `00_owner/doctrine/` — requires Proposal |
| An operational principle | `00_owner/constitution/` — requires Proposal |
| A UX wireframe or workspace specification | `10_product/strategy/user_experience/` |
| A PLG flow | `10_product/strategy/plg/` |
| A workflow specification | `10_product/strategy/workflows/` |
| Collaboration or sharing logic | `10_product/strategy/collaboration/` |
| Tier behavior | `10_product/strategy/tiering/` |
| A component specification | `30_engineering/components/` |
| Runtime state logic | `30_engineering/runtime_architecture/` |
| Confidence/integrity engineering | `30_engineering/judgement_layer/` |
| Governance override engineering | `30_engineering/governance_layer/` |
| Implementation backlog or open questions | `30_engineering/implementation_tracking/` |
| A raw transcript or source document | `90_research/transcripts/` |
| A historical preserved artifact | `90_research/historical_artifacts/` |
| A proposed canonical change | Governance proposal — requires Review and Decision |

## What If I Find a Conflict?

1. Determine which tier each conflicting position lives at.
2. The higher tier wins. Doctrine > Constitution > Implementation.
3. Do not edit canonical content directly to resolve conflicts. Conflicts are resolved through Proposals.
4. Add the conflict to the Revision Backlog (`00_owner/backlog/`).

## Authority

Only the repository owner ratifies canonical content. AI systems assist under Framework 001A authority constraints. See `CLAUDE.md`.

## Migration Rationale

The repository was restructured under DL-037 to separate Governance, Product, Architecture, Research, and Execution into clear domains. The restructure preserved all existing content; no Doctrine, Constitution, or Implementation Spec content was edited. Path references were updated to reflect new locations.

The Architecture domain currently contains four populated subdirectories; additional architecture domains are documented in `30_engineering/README.md` as a future roadmap and will be created when content exists.

## Reading Pointers

- Repository orientation: this file and `00_owner/manifest/repository_manifest.md`.
- Doctrine: `00_owner/doctrine/`.
- Constitution: `00_owner/constitution/`.
- Decisions: `00_owner/decisions/decision_log.md`.
- Backlog: `00_owner/backlog/revision_backlog.md`.
- Changelog: `00_owner/changelog/changelog.md`.
- Frameworks: `00_owner/frameworks/`.


## Sub-folder Conventions (2026-06-04 reorganization)

The two formerly-flat hotspots were sub-foldered for retrieval (top-level domains unchanged; see `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md`):

- **`30_engineering/`** → `specifications/`, `runtime_models/`, `contracts/` (incl. Wave packages + conformance reviews), `decisions/`, `reviews/`, `environment/`, `engineering/` (engineering-enablement: onboarding runbook entry point at the `30_engineering/` root, Linear import, and the env-bind `starter_kit/` templates), and `legacy_layer_engineering/` (the secondary layer dirs). `README.md` stays at the root. **Engineering starts at `RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` → `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`.**
- **`10_product/specs/`** → `ux/`, `models/`, `decisions/`, `audits_reviews/`, `data_api_nfr/`, `testing_fixtures/`, `planning/`. `CURRENT_TRUTH.md` stays at the root as the entry point.

New files should land in the matching sub-folder. Cross-references use **bare filenames** (resilient to location); only full-path references encode directories.

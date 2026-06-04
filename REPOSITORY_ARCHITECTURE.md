# Repository Architecture

This document explains how the OSLO knowledge base is organized and how to contribute to it. It is written for contributors and reviewers.

## The One-Sentence Version

OSLO is a doctrine-centered repository: doctrine defines what is true; everything else either expresses doctrine, implements doctrine, or governs how doctrine evolves.

## The Six Principles

### 1. Doctrine defines truth.

`01_governance/doctrine/` contains the canonical truth of OSLO. When the repository disagrees with itself, doctrine wins.

### 2. Constitution operationalizes doctrine.

`01_governance/constitution/` translates doctrine into Articles that govern UX, interaction, and product behavior. Articles inherit authority from doctrinal grounding.

### 3. Implementation realizes doctrine.

`02_product/` and `03_architecture/` realize what doctrine asserts. Concepts introduced here without doctrinal anchor are provisional.

### 4. Governance controls repository evolution.

`01_governance/decisions/`, `backlog/`, `changelog/`, and `frameworks/` govern how the repository changes. Governance objects do not assert doctrine.

### 5. Source Material informs but does not bind.

`04_research/` contains transcripts and historical artifacts. Non-canonical.

### 6. Subsystems must anchor to canonical content.

`subsystems/` holds sub-categories that declare their doctrinal scope, constitutional articulation, and implementation specs.

## Where Do I Put Things?

| What you have | Where it goes |
|---|---|
| A foundational claim about OSLO | `01_governance/doctrine/` — requires Proposal |
| An operational principle | `01_governance/constitution/` — requires Proposal |
| A UX wireframe or workspace specification | `02_product/user_experience/` |
| A PLG flow | `02_product/plg/` |
| A workflow specification | `02_product/workflows/` |
| Collaboration or sharing logic | `02_product/collaboration/` |
| Tier behavior | `02_product/tiering/` |
| A component specification | `03_architecture/components/` |
| Runtime state logic | `03_architecture/runtime_architecture/` |
| Confidence/integrity engineering | `03_architecture/judgement_layer/` |
| Governance override engineering | `03_architecture/governance_layer/` |
| Implementation backlog or open questions | `05_execution/implementation_tracking/` |
| A raw transcript or source document | `04_research/transcripts/` |
| A historical preserved artifact | `04_research/historical_artifacts/` |
| A proposed canonical change | Governance proposal — requires Review and Decision |

## What If I Find a Conflict?

1. Determine which tier each conflicting position lives at.
2. The higher tier wins. Doctrine > Constitution > Implementation.
3. Do not edit canonical content directly to resolve conflicts. Conflicts are resolved through Proposals.
4. Add the conflict to the Revision Backlog (`01_governance/backlog/`).

## Authority

Only the repository owner ratifies canonical content. AI systems assist under Framework 001A authority constraints. See `CLAUDE.md`.

## Migration Rationale

The repository was restructured under DL-037 to separate Governance, Product, Architecture, Research, and Execution into clear domains. The restructure preserved all existing content; no Doctrine, Constitution, or Implementation Spec content was edited. Path references were updated to reflect new locations.

The Architecture domain currently contains four populated subdirectories; additional architecture domains are documented in `03_architecture/README.md` as a future roadmap and will be created when content exists.

## Reading Pointers

- Repository orientation: this file and `01_governance/manifest/repository_manifest.md`.
- Doctrine: `01_governance/doctrine/`.
- Constitution: `01_governance/constitution/`.
- Decisions: `01_governance/decisions/decision_log.md`.
- Backlog: `01_governance/backlog/revision_backlog.md`.
- Changelog: `01_governance/changelog/changelog.md`.
- Frameworks: `01_governance/frameworks/`.


## Sub-folder Conventions (2026-06-04 reorganization)

The two formerly-flat hotspots were sub-foldered for retrieval (top-level domains unchanged; see `REPOSITORY_REORGANIZATION_PROPOSAL_V1.md`):

- **`03_architecture/`** → `specifications/`, `runtime_models/`, `contracts/` (incl. Wave packages + conformance reviews), `decisions/`, `reviews/`, `environment/`, and `legacy_layer_engineering/` (the secondary layer dirs). `README.md` stays at the root.
- **`02_product/specs/`** → `ux/`, `models/`, `decisions/`, `audits_reviews/`, `data_api_nfr/`, `testing_fixtures/`, `planning/`. `CURRENT_TRUTH.md` stays at the root as the entry point.

New files should land in the matching sub-folder. Cross-references use **bare filenames** (resilient to location); only full-path references encode directories.

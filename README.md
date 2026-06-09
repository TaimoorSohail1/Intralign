# OSLO Knowledge Base

> **Organized by ownership zone (DL-051).** This repository is filed by *ownership*, not topic:
> `00_owner/` (doctrine, constitution, frameworks, decisions, canonical definitions, glossary/ontology,
> build-governance — owner-only) · `10_product/` (product-authoritative) · `20_handoff/` (co-governed
> seam: contracts, traceability, interfaces) · `30_engineering/` (engineering-authoritative) ·
> `90_research/` (non-canonical). Precedence **Doctrine > Constitution > Implementation** is unchanged;
> all canonical change routes through Framework 001 and the **owner** ratifies. See `ZONE_GROUNDING_RULES.md`
> for the filing rules. *(Some narrative layout descriptions below predate the move and read against the
> old `01–05` domains; path references are current.)*

OSLO is a governed cognitive architecture for preserving organizational understanding, outcome integrity, and decision continuity.

This repository is the canonical knowledge base for OSLO, organized as a doctrine-centered repository under the ratified architecture (DL-033 through DL-037).

## Where to Start

- **Engineers / external team / a different LLM:** Read **`ANTI_ASSUMPTION_BUILD_PROTOCOL.md`** first (never infer a gap — escalate), then **`START_HERE.md`** — the 90-minute path (read 6 docs, ignore the rest) to your first PR.
- **New to OSLO:** Read `REPOSITORY_ARCHITECTURE.md` for orientation.
- **AI contributors:** Read `CLAUDE.md` for governance posture and authority constraints.
- **What does OSLO mean?** Read `00_owner/doctrine/`.
- **How does OSLO behave in product?** Read `00_owner/constitution/` and `10_product/`.
- **How is OSLO built?** Read `30_engineering/` (organized by the **cognitive spine** Perceive→Retain→Infer→Evaluate→Advise→Disclose, not by layers).
- **How is OSLO measured?** Read `30_engineering/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1.md` (product analytics + trust + AI economics).
- **How does OSLO look?** Read `10_product/experience/RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1.md` (design tokens / brand).
- **Where is concept X?** Read `REPOSITORY_INDEX.md` (concept → canonical file).

## Repository Structure

| Domain | Purpose | Authority |
|---|---|---|
| `00_owner/` | What OSLO means: doctrine, constitution, ontology, decisions | Canonical (Content tier) and Governance tier |
| `10_product/` | What OSLO does for users: capabilities, UX, PLG, workflows, tiering, collaboration | Derived (Implementation tier) |
| `30_engineering/` | How OSLO is built: cognitive-spine responsibilities, runtime models, Wave contracts, engineering. *(`legacy_layer_engineering/` = deprecated layer docs, re-homed under DL-043 — do not build from them.)* | Derived (Implementation tier) |
| `90_research/` | Non-canonical source material, transcripts, historical artifacts | Non-canonical |
| `30_engineering/` | Implementation tracking, open questions, design risks | Operational |
| `00_owner/subsystems/` | Subsystems anchored to canonical content | Mixed (currently: Project MRI stub) |

## Authority Model

Only the repository owner ratifies canonical content. AI systems assist with analysis, consistency checking, conflict identification, and recommendation generation under Framework 001A. AI systems do not ratify decisions.

## Operative Governance State

- **Frameworks:** Framework 001 and Framework 001A operative (ratified under DL-030 / DL-031). **Operative decision range: DL-029–DL-050** (see `00_owner/decisions/decision_log.md`; the ledger is the source of truth).
- **Architecture:** Doctrine-centered (DL-033).
- **Progression taxonomy:** OSLO Evolution Framework with four axes (DL-034).
- **Source Material:** Constitutional Principles Draft as Historical Artifact (DL-035).
- **Registry foundation:** Bounded Registry Foundation operative (DL-036).
- **Repository structure:** Per the Repository Restructure (DL-037).

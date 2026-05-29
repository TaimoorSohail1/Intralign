# Repository Architecture

This document explains how the OSLO knowledge base is organized and how to contribute to it. It is written for contributors and reviewers. It is not a governance manual.

## The One-Sentence Version

OSLO is a doctrine-centered repository: doctrine defines what is true; everything else either expresses doctrine, implements doctrine, or governs how doctrine evolves.

## The Six Principles

### 1. Doctrine defines truth.

The folder `01_doctrine_ontology/` contains the canonical truth of the OSLO system. When the repository disagrees with itself, doctrine wins. If you want to know what OSLO is, read doctrine first.

### 2. Constitution operationalizes doctrine.

The folder `02_ux_constitution/` translates doctrine into operational language — Articles that govern UX, interaction, and product behavior. The Constitution is authoritative for operational guidance, but it is downstream of doctrine. If a Constitutional Article disagrees with doctrine, the Article is wrong, not the doctrine.

### 3. Implementation realizes doctrine.

The folder `03_implementation_specs/` contains wireframes, components, workflows, state logic, and other implementation-level specifications. Implementation specs realize what doctrine asserts and what the Constitution articulates. If you find a spec that introduces a concept with no doctrinal or constitutional source, that concept is provisional — it lives on borrowed authority until governance promotes it (or supersedes it).

### 4. Governance controls repository evolution.

The folder `07_governance/` contains the procedural objects that govern how the repository changes. Frameworks declare the lifecycle. Proposals propose changes. Reviews analyze them. Decisions ratify them. The Revision Backlog queues identified work. The Changelog records changes.

Governance objects do not assert what OSLO is. They assert how the repository evolves. They cannot override doctrine.

### 5. Source Material informs but does not bind.

The folder `00_raw_transcript/` (and any future source material) contains the conversations, transcripts, and documents that informed canonical content. It is preserved for interpretive context and historical traceability. It is not canonical and cannot be cited as authority.

### 6. Subsystems must anchor to canonical content.

A subsystem (for example, Project MRI in `04_project_mri/`) is a sub-category of the Content tier. Every subsystem must declare its doctrinal scope, constitutional articulation (if any), and implementation specifications. A subsystem cannot float — it must anchor to canonical content.

## Where Do I Put Things?

| What you have | Where it goes |
|---|---|
| A foundational claim about what OSLO is or how it should be understood | `01_doctrine_ontology/` — requires Proposal to add |
| An operational principle that articulates how doctrine is expressed in product behavior | `02_ux_constitution/` — requires Proposal to add |
| A wireframe, component spec, workflow, or state machine | `03_implementation_specs/` — should cite the doctrine or Constitution it implements |
| A raw transcript, design conversation, or source document | `00_raw_transcript/` — non-canonical; can be added freely |
| A proposed change to canonical content | `07_governance/` (Proposals subdirectory if/when created) — requires Review and Decision |
| A reviewer's analysis of a Proposal | `07_governance/` (Reviews subdirectory if/when created) |
| An identified concern or pending work | `07_governance/revision_backlog.md` — currently restricted; see Governance Discipline below |
| A subsystem with its own scope | A new content directory, anchored to doctrine via Proposal |

## What If I Find a Conflict?

If you find content in the repository that contradicts itself:

1. Determine which tier each conflicting position lives at.
2. The higher tier wins. Doctrine over Constitution. Constitution over Implementation Specs.
3. Do not edit canonical content directly to resolve the conflict. Conflicts are resolved through Proposals.
4. Add the conflict to the Revision Backlog if it is not already there.

## Authority

Only the repository owner may ratify, reject, supersede, or adopt canonical content. AI systems may assist with analysis, consistency checking, conflict identification, and recommendation generation. AI systems do not ratify decisions.

## Governance Discipline (Current)

The repository is in a phase where new governance work is restricted. Until the repository owner directs otherwise, contributors should not create new Governance Frameworks, new Proposals, or new Revision Backlog entries unless required to resolve open governance work. The current focus is execution, not analysis.

## Where to Read More

- `repository_manifest.md` — original orientation charter
- `canonical_definitions.md` — established terms and their sources
- `ontology_registry.md` — ontology entities and relationships
- `07_governance/proposal_000_disposition.md` — full architectural disposition
- `07_governance/decision_log.md` — record of ratified decisions
- `07_governance/revision_backlog.md` — identified work pending Proposal
- `07_governance/changelog.md` — record of canonical changes

## Final Note

This architecture exists to preserve the original understanding of OSLO across change. When in doubt, read doctrine, then ask whether the change you are proposing would weaken or strengthen what doctrine asserts. Then take the answer through governance.

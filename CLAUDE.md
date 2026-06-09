# Instructions for AI Contributors

This file governs how AI systems contribute to the OSLO knowledge base. It is operative under Framework 001A and DL-033.

> **Repository structure (per DL-051):** content is organized by **ownership zone**, not topic:
> `00_owner/` (owner-only: doctrine, constitution, frameworks, decisions, canonical definitions,
> glossary/ontology, build-governance) · `10_product/` (product-authoritative) · `20_handoff/`
> (co-governed seam: contracts, traceability, interfaces) · `30_engineering/` (engineering-authoritative)
> · `90_research/` (non-canonical). "Authoritative" = default author, NOT authority to supersede ratified
> canon; all canonical changes route through Framework 001 and the **owner** ratifies. Doctrine/constitution/
> epistemic invariants are owner canon (`00_owner`), never product-editable (ratify ≠ author).

## Authority Constraint

Repository governance authority resides with the repository owner. AI systems may assist with:

- analysis
- consistency checking
- conflict identification
- recommendation generation

AI systems may not:

- ratify decisions
- reject decisions
- supersede canonical content
- adopt canonical content

Only the repository owner may ratify, reject, supersede, or adopt canonical content.

## Content Precedence (per DL-033, DL-036)

1. **Doctrine** (`00_owner/doctrine/`) — foundational conceptual content; highest precedence.
2. **Constitution** (`00_owner/constitution/`) — distilled operational expression of doctrine.
3. **Implementation content** (`10_product/`, `20_handoff/`, `30_engineering/`) — derived; subordinate to Doctrine and Constitution.
4. **Source Material** (`90_research/`) — non-canonical; informs but does not bind.

Doctrine > Constitution > Implementation. Source Material is outside the precedence ladder.

## Surface Authority Rule (DL-036 R1)

For canonical definitions:

- `00_owner/constitution/10_canonical_definitions.md` — Content-tier authoritative operational expression.
- `00_owner/canonical_definitions/canonical_definitions.md` — Governance-tier orientation registry.
- Where they conflict substantively, **Doctrine prevails** (DL-036 Clarification #1).

## Governance Lifecycle (Framework 001)

Backlog Entry → Proposal → Review → Decision → Repository Change → Changelog Entry.

No canonical repository change occurs without:

1. Proposal
2. Review (Findings, Concerns, Dependencies, Recommendation, Status)
3. Decision
4. Traceability Record

## Review Output Schema (Framework 001A)

Every Review produces exactly five outputs:

- **Findings**
- **Concerns**
- **Dependencies**
- **Recommendation**
- **Status**

## Conflict Resolution

Conflicts between repository layers are resolved through governance proposals, not direct edits.

When citing a concept:

- For foundational claims: cite `00_owner/doctrine/`.
- For operational principles: cite `00_owner/constitution/`.
- For derived implementation: cite `10_product/`, `20_handoff/`, or `30_engineering/`, plus the doctrinal/constitutional source.

## Governance Discipline (Current)

Until the repository owner directs otherwise:

- Do not create new Governance Frameworks.
- Do not create new Proposals without owner direction.
- Do not create new Revision Backlog entries without owner direction.
- Do not introduce new doctrine.
- Do not resolve ontology conflicts unilaterally.

Open governance items continue under existing backlog tracking.

## What to Read First

1. `REPOSITORY_ARCHITECTURE.md` — repository orientation.
2. `00_owner/manifest/repository_manifest.md` — repository charter.
3. `00_owner/frameworks/framework_001.md` and `framework_001A.md` — governance procedure.
4. `00_owner/decisions/decision_log.md` — ratified decisions.
5. `00_owner/backlog/revision_backlog.md` — pending work.

## Drift-control files (read before building — this team uses Claude Code, which reads this file)
The engineering team builds with **Claude Code**, which loads **`CLAUDE.md`** automatically. Before writing any OSLO application code, read — and keep open:
- `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md` — **never infer a spec gap; escalate it.** Read first.
- `00_owner/CANONICAL_GLOSSARY.md` — one canonical name per concept + banned synonyms.
- `20_handoff/traceability/RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md` — every capability → contract → test → observability event.
- `00_owner/OPEN_TBD_REGISTER.md` — every owner-decision-required value; **DO NOT ASSUME**.
- `00_owner/build_governance/` — owner-ratified build policy (QA/observability/deployment governance, implementation constraints, AI-First delivery rules) that **binds** engineering; engineering proposes, owner ratifies.

For building the application: `30_engineering/delivery/RELEASE_1_ENGINEERING_HANDOFF_PACKAGE_V1.md` → `RELEASE_1_ENGINEERING_ONBOARDING_RUNBOOK_V1.md`. The app-repo build-rules file is `30_engineering/delivery/starter_kit/CLAUDE.md` (with `AGENTS.md` as its tool-neutral twin).

# Proposal 003 / Repository Domain Restructure — Disposition Document

## Decision Identifier

DL-037

## Title

Adopt the Repository Domain Restructure per Proposal 003

## Disposition

**Accepted with Conditions**

The conditions are the ten Framework 001A Review clarifications recorded in the Closing Decision Clarifications section below. Each operates as narrative guidance binding execution, not as a deferred amendment.

## Date Ratified

2026-05-29

## Authorizing Proposal

Proposal 003 — Repository Domain Restructure

## Source Material

- Repository Restructure Scope Directive (owner guidance)
- Bounded Executor Package (planning substrate — 11 deliverables)
- Proposal 003 Document
- Framework 001A Review of Proposal 003
- Final Ratification Readiness Review
- Comprehensive Editorial Pass (Corrections A through I)
- Final Micro-Correction Pass (R-1, R-2)

## Repository Owner Principles

1. The restructure is a single bounded Decision with five sequenced execution phases.
2. No doctrinal, constitutional, or implementation spec body content is amended.
3. Specs 10 and 12 are moved whole and are not split.
4. Path-reference updates are housekeeping only.
5. README, CLAUDE.md, and REPOSITORY_ARCHITECTURE.md updates are orientation only.
6. No ontology conflicts are resolved.
7. No doctrinal stubs are introduced.
8. No new backlog entries are created.
9. Only directories that receive content are created.

## Rationale

Proposal 003 satisfies the bounded scope defined by the Repository Restructure Scope Directive. All five phases align with the Scope Directive's phase model. The Framework 001A Review identified ten Concerns, all addressable by closing-Decision narrative clarifications. The substance of Proposal 003 is adopted without revision. The Decision authorizes a single coherent migration executed through five sequenced phases.

---

## Ratified Resolutions

### Phase 1 — Governance Stabilization

Create `01_governance/` with nine subdirectories (`doctrine/`, `constitution/`, `canonical_definitions/`, `ontology/`, `decisions/`, `backlog/`, `changelog/`, `frameworks/`, `manifest/`). Relocate 13 Doctrine files, 14 Constitution files, 7 governance objects from `07_governance/`, and 3 root-level governance files. Materialize Framework 001 and Framework 001A as standalone files (subject to Clarification #2). Update path references mechanically per the Reference Update Matrix.

### Phase 2 — Product Organization

Create `02_product/` with five subdirectories. Relocate Implementation Specs 01, 02, 03, 04, 06, 07, 10, 12. Specs 10 and 12 move whole; splits explicitly deferred (subject to Clarification #3).

### Phase 3 — Architecture Extraction

Create `03_architecture/` with four subdirectories (`runtime_architecture/`, `judgement_layer/`, `governance_layer/`, `components/`). Relocate Implementation Specs 05, 08, 09, 11. Populate `03_architecture/README.md` with future-architecture-roadmap section documenting potential domains as content, not as folders.

### Phase 4 — Execution Tracking

Create `05_execution/implementation_tracking/`. Relocate Implementation Specs 13 and 14.

### Phase 5 — Research, Subsystems, and Root Cleanup

Create `04_research/` with two subdirectories. Relocate raw transcripts and the Historical Artifact. Create `subsystems/project_mri/` and relocate the stub. Populate root README, CLAUDE.md, revise REPOSITORY_ARCHITECTURE.md (subject to Clarification #6). Remove emptied legacy directories after verification (subject to Clarification #7 grep audit).

---

## Closing Decision Clarifications

### Clarification #1 — RB-020 Remains Open Through DL-037 Closure

RB-020 does NOT close as part of DL-037. After Phase 5 completes and the owner reviews placed README.md and CLAUDE.md content, RB-020 may be closed via clerical action under DL-036 R3 precedent or follow-on Proposal. Default expectation: RB-020 closes via clerical action with reference to DL-037 as substantive content provider, pending owner confirmation of scope satisfaction.

### Clarification #2 — Owner Verification of Framework 001 and 001A Drafts Before Phase 1 Placement

The Framework 001 and Framework 001A draft files are materialized from already-ratified content extracted from the DL-030 and DL-031 dispositions. Before placement during Phase 1, the repository owner verifies that the drafts substantively match the originally-issued Framework content. Owner verification is a required gate. If wording variations alter substantive content, drafts are corrected before placement. The materialization introduces no new procedural rules.

**Optional verification record (per Review Issue I-6):** The owner may at their discretion record the comparison reference (chat record location, external archive reference, or similar) in brief verification notes placed alongside the Framework files at `01_governance/frameworks/framework_001_verification_note.md` and `01_governance/frameworks/framework_001A_verification_note.md`. The verification notes preserve auditable evidence of the substantive-match confirmation. This is permitted but not required; the closing Decision does not mandate verification note creation. If created, the verification notes are recorded in CHG-036 as additional Phase 1 affected artifacts.

### Clarification #3 — No Header Notes on Specs 10 and 12 During Migration

Specs 10 and 12 move whole without header annotations. No "mixed concerns" header note is added during the migration. If the owner later determines that Specs 10 and 12 warrant inline notes, those notes are added through a follow-on action under separate authority, not as part of DL-037.

### Clarification #4 — Historical Artifact References Distinguish Origin vs Forward Citations

The Historical Artifact header in `04_research/historical_artifacts/05_constitutional_principles_draft.md` contains both historical and forward-looking references:

- **Historical (preserve verbatim):** Origin path citation `01_governance/doctrine/12_constitutional_principles_draft.md` — preserved as historical record.
- **Forward-looking (update to new path):** Reference to Doctrine 02 (now `01_governance/doctrine/02_organizational_cognition_model.md`); reference to rb_003_disposition.md and rb_010_disposition.md (now at `01_governance/decisions/`).

The DL-035 substantive content is preserved unchanged.

### Clarification #5 — Manifest Annotation Path-Reference Check

During Phase 1, before moving `repository_manifest.md`, the pre-ratification annotation is verified for path references. Expected outcome: the annotation references DL-033 by Decision identifier (not by file path); no path updates required. If verification reveals any unexpected path reference, it is updated mechanically per the Reference Update Matrix; annotation's substantive content is preserved.

### Clarification #6 — README, CLAUDE.md, and REPOSITORY_ARCHITECTURE.md Reviewed Against Orientation-Only Constraint

During Phase 5, placed root README.md, CLAUDE.md, and revised REPOSITORY_ARCHITECTURE.md content is reviewed line-by-line against the orientation-only constraint. Any line introducing a new normative claim is removed before placement. Each line must trace to (a) an existing ratified Decision (DL-029 through DL-036), (b) a Framework provision, or (c) a structural description of the post-migration repository. Lines beyond these categories are not placed.

### Clarification #7 — DL-036 Surface Authority Rule Path Updates Verified

During Phase 1, DL-036 R1 references to Article 10 are verified to update consistently from `01_governance/constitution/10_canonical_definitions.md` to `01_governance/constitution/10_canonical_definitions.md`. The Rule's semantics are preserved unchanged. Verification points: `canonical_definitions.md` Surface Authority Rule section; `ontology_registry.md` cross-reference.

DL-036 substantive content (R1–R8, Clarifications #1–#8) preserved; only path citations update mechanically.

**Additional scope (per Review Issue I-4):** This Clarification also covers path-reference updates within DL-034-issued Governance Notes in Constitution Article 08 (`08_product_evolution_constitution.md`). The Governance Notes on Articles 40 and 44 cite doctrinal paths (Doctrine 02, 09, 10) that update mechanically post-migration to reflect the relocated doctrine path `01_governance/doctrine/*`. Such path updates are permitted housekeeping; the substantive operational claims of the Governance Notes — that Doctrine 09's "Governed Organizational Cognition" label prevails over Article 40's Stage 3 label, and that Doctrine 02's four-stage arc prevails over Article 44's Portfolio Cognition addition — are preserved unchanged. Updates to the Article 08 file are limited to path string substitution within the Notes; no other Constitution content is modified.

### Clarification #8 — Index File Retirement Disposition

`03_implementation_specs/00_index.md` and `03_implementation_specs/README.md` are NOT folded into domain READMEs. The "Primary UI Model" section in `00_index.md` contains the "Cursor-like AI-native IDE for Outcome Orchestration" identity claim (Inventory I-A item 9). Folding it into domain READMEs would violate the orientation-only constraint.

**Supersession:** This clarification supersedes the retirement treatment specified in Proposal 003 Artifact 2 for `03_implementation_specs/00_index.md` and `03_implementation_specs/README.md`, and converts those two retirements into historical-artifact relocations. There are no retirements under DL-037; both files are relocated.

**Disposition:** Both files are relocated to `04_research/historical_artifacts/` as preserved historical content:

- `03_implementation_specs/00_index.md` → `04_research/historical_artifacts/03_implementation_specs_index_historical.md`
- `03_implementation_specs/README.md` → `04_research/historical_artifacts/03_implementation_specs_readme_historical.md`

The "Cursor-like AI-native IDE" identity claim remains visible in the historical record. Inventory I-A item 9 continues to flag the claim as unanchored; RB-004 remains reserved.

**Header treatment:** The relocated files do NOT carry Historical Artifact headers analogous to the Constitutional Principles Draft (per DL-035). Their non-canonical status is communicated by their location in `04_research/historical_artifacts/` and by the `_historical.md` filename suffix. Adding headers would constitute body content modification, conflicting with the no-spec-edits and orientation-only constraints. This treatment is intentional. The header asymmetry between the Constitutional Principles Draft (which carries a structured Historical Artifact header per DL-035) and these two files (which carry only location/filename signals) is accepted as the cost of preserving the bounded scope.

### Clarification #9 — Phases 2–4 Default to Sequential Execution

Phases 2, 3, and 4 are logically independent, but default to sequential execution absent explicit owner direction for parallelization. Phase 1 must complete before Phases 2–4 may begin. Phase 5 must follow Phases 1–4.

### Clarification #10 — RB-005 Residual Remains Partially Closed

RB-005 (Layer Promotion and Citation Rule) is Partially Closed under DL-033 with residual scope: explicit citation requirements for Implementation Specs. Post-migration README-level citation declarations are orientation declarations, not enforced citation requirements. RB-005 residual is NOT satisfied by DL-037. RB-005 remains Partially Closed with its residual scope unchanged.

---

## Rollback Authority

In the event a constraint violation is detected during execution of any phase, AI executing the migration may halt and revert the offending phase to its pre-execution state without further authorization. This rollback authority is scoped to constraint violations of the kind enumerated in the Constraints Preserved section.

**Rollback authority does not extend to reversing, nullifying, or invalidating owner-ratified Decisions.** It applies only to migration execution actions performed under DL-037. Specifically:

- AI may revert file moves performed under DL-037 Phase 1–5 execution.
- AI may revert path-reference updates performed under DL-037 Phase 1–5 execution.
- AI may revert directory creations performed under DL-037 Phase 1–5 execution.
- AI **may not** alter, retract, or supersede DL-037 itself.
- AI **may not** alter, retract, or supersede DL-029, DL-030, DL-031, DL-032, DL-033, DL-034, DL-035, DL-036, or any other ratified Decision, including the substantive content of Stated decisions DL-001 through DL-028 preserved under DL-032's transitional rule.
- AI **may not** alter Framework 001, Framework 001A, the Manifest's substantive content, or any pre-ratification annotation.
- AI **may not** withdraw the closing Decision package's Clarifications.

**Rollback procedure (reverse-chronological from execution):**

1. Halt the offending phase immediately.
2. Revert path-reference updates performed within the phase, in reverse order of execution. (Path updates revert first so files at original locations carry consistent original-path references during subsequent reversals.)
3. Revert file moves performed within the phase, in reverse order of execution.
4. Revert directory creations performed within the phase, in reverse order of execution (subdirectories before parent directories; empty directories only).
5. Surface the violation to the repository owner with a brief description.
6. Do not proceed to subsequent phases until owner directs resolution.

Rollback within a single phase does not cascade to other phases. Rollback within a phase does not invalidate prior completed phases.

---

## Confirmation of Constraints

- **Specs 10 and 12 move whole.** No splitting under DL-037.
- **No doctrinal content amended.** Doctrine 01–11 relocate verbatim.
- **No constitutional content amended.** Constitution Articles 1–50 relocate verbatim; Article 40 and 44 Governance Notes preserved with path-only updates per Clarification #7.
- **No implementation spec body content amended.** Specs 01–14 relocate verbatim; no header notes added (Clarification #3).
- **No ontology conflicts resolved.** RB-006 through RB-009 remain Open.
- **No doctrinal stubs introduced.** RB-004 remains Open.
- **No new backlog entries created.**
- **DL-036 substantive content preserved.** Only path citations update mechanically.
- **Frameworks 001 and 001A introduce no new procedural rules.** Materialization is from already-ratified content with owner verification (Clarification #2).
- **README, CLAUDE.md, REPOSITORY_ARCHITECTURE.md are orientation only.** No new normative claims (Clarification #6).
- **RB-005 residual unchanged.**

---

## Confirmation of Migration Model

- **One bounded Decision (DL-037).** Authorizes the entire migration.
- **Five sequenced execution phases.** Phases are execution steps within DL-037.
- **Phase ordering:** Phase 1 first; Phases 2–4 sequential default (Clarification #9); Phase 5 last.
- **Per-phase changelog entries (CHG-035 through CHG-043).**
- **Final validation:** Post-Migration Validation Checklist is the operative completion gate.

---

## Effects on Existing Backlog

- **RB-001** Closed by DL-036. Unaffected.
- **RB-002** Closed by DL-030/031. Unaffected.
- **RB-003** Closed by DL-034. Unaffected.
- **RB-004** Open. Inventory I-A continues to feed it at new paths.
- **RB-005** Partially Closed. Residual unchanged (Clarification #10).
- **RB-006, RB-007, RB-008, RB-009** Open. Conflicting-status registry entries preserved.
- **RB-010** Closed by DL-035. Unaffected.
- **RB-011** Closed by DL-033. Unaffected.
- **RB-012, RB-013, RB-014, RB-015, RB-016, RB-017, RB-018** Open. Operate against new paths.
- **RB-019** Closed by DL-033. Unaffected.
- **RB-020** Remains Open through DL-037 closure (Clarification #1). Post-migration disposition pending owner review.

No new backlog entries created. No existing entries reopened.

---

## Effects on Canonical Surfaces

### Doctrine

Relocated verbatim from `01_governance/doctrine/` to `01_governance/doctrine/`. No content changes.

### Constitution

Relocated verbatim from `01_governance/constitution/` to `01_governance/constitution/`. Article 40 and 44 Governance Notes preserved with path-only updates (Clarification #7).

### Implementation Specifications

Relocated to product, architecture, or execution domains based on primary topic. Body content unchanged. Specs 10 and 12 move whole. `00_index.md` and `README.md` relocated to `04_research/historical_artifacts/` per Clarification #8.

### Source Material

Raw transcripts relocated to `04_research/transcripts/`. Historical Artifact relocated to `04_research/historical_artifacts/` with Historical Artifact header preserved; forward-looking references updated per Clarification #4.

### Governance Tier

Manifest, canonical_definitions, ontology_registry relocated to `01_governance/{manifest, canonical_definitions, ontology}/`. Pre-ratification annotations preserved (Clarification #5). DL-036 R1 path citations updated mechanically (Clarification #7).

### Decision Log, Backlog, Changelog

Relocated to `01_governance/{decisions, backlog, changelog}/`. Path references updated; historical references in DL-029 through DL-036 entries preserved as written.

---

## Effects on DL-033, DL-034, DL-035, DL-036

- **DL-033** Unaffected as a Decision. Two-tier separation operationalized physically.
- **DL-034** Unaffected. Canonical axis sources relocate to `01_governance/doctrine/`; citation paths update.
- **DL-035** Unaffected. File relocated to `04_research/historical_artifacts/`; Historical Artifact header preserved per Clarification #4.
- **DL-036** Unaffected. R1–R8 and Clarifications #1–#8 preserved; path citations update per Clarification #7.

---

## Affected Artifacts

### Quantitative Summary

- **10 files created or populated explicitly** (Framework 001, Framework 001A, five top-level domain READMEs [`01_governance/`, `02_product/`, `03_architecture/`, `04_research/`, `05_execution/`], this disposition document, root README.md [populated from empty], root CLAUDE.md [populated from empty]). Additional inherited or new minimal subdirectory READMEs may be created during Phase 5 cleanup; precise count to be recorded in CHG-041.
- **61 files relocated total.** All 61 items in the File Move Matrix (Bounded Executor Package Deliverable 3) are relocations under DL-037. Clarification #8 supersedes the retirement classification for items 52 (`03_implementation_specs/00_index.md`) and 53 (`03_implementation_specs/README.md`), converting them to relocations to `04_research/historical_artifacts/`. Total relocation count is unchanged from the matrix (61); only the classification of 2 items shifts from retirement to relocation.
- **0 retirements.** Clarification #8 supersedes the retirement treatment; no items are retired under DL-037.
- **14 files receive path-reference housekeeping updates** per the Reference Update Matrix.
- **6 legacy directories removed** after Phase 5 verification.
- **0 substantive content edits.**
- **0 new backlog entries.**
- **0 new Frameworks.**
- **0 ontology conflicts resolved.**

---

## Required Repository Actions

1. Place this disposition document at `01_governance/decisions/proposal_003_restructure_disposition.md` (pre-Phase-1). The file relocates to `01_governance/decisions/` during Phase 1.
2. Record DL-037 in the decision log (currently `01_governance/decisions/decision_log.md`; relocates during Phase 1).
3. Execute Phase 1 per the Repository Execution Plan, with rollback authority per the Rollback section. **Pre-execution gate: owner verification of Framework 001 and 001A drafts per Clarification #2.**
4. Execute Phase 2 sequentially after Phase 1 completion.
5. Execute Phase 3 sequentially after Phase 2 completion.
6. Execute Phase 4 sequentially after Phase 3 completion.
7. Execute Phase 5 after Phases 1–4 complete.
8. Record per-phase changelog entries (CHG-035 through CHG-043).
9. Execute the Post-Migration Validation Checklist before marking DL-037 complete.

## Status

**Ratified.** This disposition is operative as of 2026-05-29. Execution authorized per owner ratification directive. Phase 1 commences upon owner Framework verification gate per Clarification #2.

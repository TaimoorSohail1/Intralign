# Release 1 Logical Data Model v1

**Document Type:** Logical Data Model (environment-independent; maps to Runtime Object Model + DL-043) · **Status:** **DL-043-conformed (2026-06-04) — Ready for Review** · **Date:** 2026-06-04
**Consumes:** Runtime Object Model (DL-043 overlay) · Epistemic State Model · Derived Cognition Lifecycle · User Acceptance/Plan-Fact · Calibration Defaults · Environment Profile R2 store-binding. **Scope:** *logical* entities/fields/relationships/lifecycle only — **no physical schema, DDL, indexes, or DB-specific types.** Physical binding (Supabase Postgres + Auth + pgvector + Storage / Neo4j / Redis — per DL-054; MongoDB and Qdrant removed) is the environment layer.

> **Mode:** the field-level logical model engineering needs to build persistence — derived entirely from ratified objects. **R2 binding honored:** the **append-only receipts** (Attested Assertions · Cognition History Records · User Acceptance Records / plan facts) are the **system of record**; **live Derived cognition** is a **recomputable representation** (current-view), never the canonical copy. Per `CLAUDE.md`, owner ratifies.

---

## 1. Epistemic Backbone (the spine every entity hangs from)

**Two storage classes, by epistemic state:**
- **Canonical (Attested) — append-only, immutable, system-of-record.** Three attesting sub-classes: **evidence-attested**, **OSLO-self-attested** (Cognition History Records), **user-attested** (User Acceptance Records + plan facts).
- **Derived (non-canonical) — recomputable representation.** The live current-view of Findings/Issues/Confidence/CAF/Recommendations/Clarifications/Acceptance-Impact. Rebuildable from canonical + recompute; **never the source of truth**.

**Universal fields (every entity):** `id` · `project_id` · `created_at` · `created_by` (user | OSLO | source-system) · `epistemic_state` (attested-evidence | attested-oslo | attested-user | derived) · `provenance_ref` (lineage) · `version` · `supersedes_id` (nullable). Canonical entities are **never updated or deleted**; change = a new appended row.

## 2. Canonical Entities (System of Record — append-only)

### 2.1 Attested Assertion *(abstract; the canonical unit)*
- `assertion_id` · `content_type` (fact | assumption | constraint | dependency | goal) · `proposition` (the asserted claim) · `attesting_source` (evidence-source-id | oslo | user-id) · `source_ref` (artifact + locus, or emission ref, or acceptance ref) · `re_derivable` (bool, true for canonical) · `version` · `supersedes_id` · `created_at`.
- **Sub-classes by attesting_source:** Evidence-Attested (from an artifact), Self-Attested → **Cognition History Record** (§2.2), User-Attested → **Plan Fact** (§2.4).
- **Rule:** an assumption/constraint/dependency is an Attested Assertion **only when attested**; **inferred** ones are Derived (§3), not stored here.

### 2.2 Cognition History Record *(OSLO-self-attested; the emission receipt)*
- `chr_id` · `output_kind` (finding | issue | confidence | reliability | caf | outcome_confidence | recommendation | clarification | acceptance_impact | alignment | feasibility | risk) · `output_payload` (the emitted value/content snapshot) · `emitted_at` · `input_attestation_version` (which Attested set it was computed over) · `model_or_rule_version` (incl. provider+model identity) · `upstream_lineage` (refs to the CHRs/assertions it derived from) · `recompute_trigger` (promotion | knowledge-change | clarification | user-action | reanalysis) · `supersedes_chr_id`.
- **Append-only.** A recompute **appends** a new CHR; it **never** overwrites. This is the drift/"why did it change" backbone.

### 2.3 Evidence & Intake (canonical evidentiary anchors)
- **Artifact:** `artifact_id` · `source` · `uploaded_by` · `uploaded_at` · `content_ref` (unstructured body → document store) · `provenance` · `version`. Append-only/versioned.
- **Promotion Candidate** *(transient, not long-term canonical):* `candidate_id` · `artifact_ref` · `normalized_form` · `readiness_state` (pending | ready | failed) · `integrity_clearance` (attribution + idempotency-key + evidence-chain ok). Resolves into Attested Assertions on admission.

### 2.4 User Acceptance Record & Plan Fact *(user-attested)*
- **User Acceptance Record:** `uar_id` · `user_id` · `confirmed_at` · `action` (accept | reject | defer | direct_edit) · `target_kind` (recommendation | finding | assumption | plan_item | …) · `version_pin` (**CHR id** for Derived targets, or assertion id for Attested) · `rationale` (optional). Append-only. **Not a Governance Decision.**
- **Plan Fact:** an **Attested Assertion** with `attesting_source = user` — the **confirmed content** as a Canonical Fact attributed to the user. Created on `accept`/`direct_edit`. **Factual in the plan, not world-truth.** Decoupled from OSLO's (still-Derived) recommendation.

### 2.5 History Record *(generic append-only audit entry)*
- `history_id` · `event_type` (integrity-clearance | knowledge-versioned | superseded | archived | unarchived | emission-appended | acceptance-recorded | recompute) · `subject_ref` · `at` · `actor`. The integrity/audit trail (R3/R5 event mapping). *(`unarchived` = the append-only reversal of `archived`; archive is reversible in R1 per DL-058/RB-025. Active/archived status is the latest of `archived`/`unarchived`.)*

## 3. Derived Representation (recomputable current-view — NOT system of record)

### 3.1 Live Cognition Projection
- `projection_id` · `output_kind` · `current_payload` · `current_chr_ref` (the latest CHR this view reflects) · `epistemic_label` (derived) · `confidence_value` + `confidence_band` (low/med/high per Calibration Defaults) · `conflict_state` (none | contested) · `recomputed_at`.
- **Rebuildable** from the latest CHR per (project, output_kind, subject). May be cached (Redis) or materialized (Postgres view); **carries no authority** — if lost, recompute restores it. Findings/Issues/Recommendations/Clarifications/Confidence/CAF/Outcome-Confidence/Acceptance-Impact are all instances.

### 3.2 Derived attributes (not standalone entities)
- **Severity / Confidence / Reliability** are **attributes** on their Issue/assessment projection (per Object Model §8), each with value + band; never separate canonical rows.
- **Inferred assumption/constraint/dependency:** a Derived projection (Infer), distinct from the canonical (attested) ones in §2.1.

## 4. Relationships (logical; graph-friendly)

```text
Project 1───* Artifact 1───* Attested Assertion (evidence) ─┐
                                                            ├─derives→ Live Cognition Projection (Derived)
Attested Assertion ──asserted-in──> Evidence locus          │            │ reflects
Finding ──anchored-to──> Attested Assertion(s)              │            ▼
Issue ──from──> Finding ; Recommendation ──for──> Finding/Issue   Cognition History Record (append-only)
Dependency ──between──> Attested Assertions (Neo4j graph edge)            ▲ emitted
User Acceptance Record ──version-pins──> Cognition History Record ────────┘
Plan Fact (user-attested) ──confirms-content-of──> Recommendation/edit ; ──is-a──> Attested Assertion
Acceptance-Impact ──compares──> (Plan Fact / UAR version-pin) vs (current CHR)
```
- **Dependency / relationship graph** → naturally a **Neo4j** edge set over Attested Assertion nodes (R2 binding); the rest relational.

## 5. Lifecycle & Versioning Rules (logical invariants)
1. **Canonical = append-only.** No update/delete on Attested Assertions, CHRs, UARs, Plan Facts. Change ⇒ new `version` row with `supersedes_id`.
2. **Recompute appends a CHR; never overwrites.** Live projection replaced; history grows.
3. **One-way flow.** No Derived projection is ever written as Attested; only a **user act** authors a user-attested Plan Fact.
4. **Version-pin integrity.** Every UAR references the exact CHR/assertion version confirmed.
5. **Provenance everywhere.** Every canonical row names its source; re-derivable.
6. **Derived carries no authority.** Live projections are reconstructable; losing them loses nothing canonical.

## 6. Physical-Binding Notes (deferred — environment layer)
*(Logical → physical mapping, per Environment Profile R2 **as amended by DL-054**; recorded for engineering, not built here.)*
- **Supabase Postgres (system of record, append-only):** Attested Assertions, Cognition History Records, User Acceptance Records, Plan Facts, History Records, Projects, Users, Orgs, Artifacts(meta). *(Identity/authz via Supabase Auth + RLS.)*
- **Neo4j:** Dependency/relationship graph over Attested Assertions.
- **Supabase Storage:** unstructured artifact bodies (`content_ref`). *(Per DL-054 — was MongoDB; large derived blobs may also live here.)*
- **Supabase pgvector:** semantic embeddings (retrieval; derived, rebuildable). *(Per DL-054 — was Qdrant.)*
- **Redis:** live Derived projection cache, sessions, event buffers (all recomputable/transient).
- **No physical schema is specified here** — types/indexes/migrations belong to the environment-bound build.

## 7. Conformance
- **§E** ✅ — every entity/field traces to a ratified object (Object Model + DL-043 overlay); no invented entities; Severity/Confidence/Reliability kept as attributes; inferred-vs-attested split honored.
- **R2 honored** ✅ — receipts are system-of-record; live cognition is recomputable representation; no Governance Decision entity.
- **No physical/implementation content** ✅ — logical only; environment binding deferred.

## 8. Final Verdict
**READY FOR REVIEW.** A complete environment-independent logical data model: canonical append-only receipts (Attested Assertions incl. evidence/OSLO/user sub-classes, Cognition History Records, User Acceptance Records, Plan Facts) as system of record; live Derived cognition as recomputable representation; relationships (incl. the dependency graph), lifecycle/versioning invariants (append-only, recompute-appends, one-way-flow, version-pin, provenance), and deferred physical-binding notes mapping to the ratified stores. No new concept; no physical schema; environment binding deferred.

> ### Proposed Owner Resolution
> Approve the Release 1 Logical Data Model as the field-level foundation for environment-bound persistence. Proceed to the Claude Code coding constraints + code-tree convention, then the Engineering Handoff Package.

---

*This Release 1 Logical Data Model provides the environment-independent, field-level entity model engineering needs, derived from the ratified Runtime Object Model and DL-043: a two-class epistemic backbone (canonical append-only Attested Assertions — evidence-, OSLO-self-, and user-attested — plus Cognition History Records, User Acceptance Records, and Plan Facts as the system of record; and live Derived cognition as a recomputable, authority-free representation), with universal provenance/version fields, canonical entity definitions (Attested Assertion with content-typing; Cognition History Record with input/model versions and lineage; Artifact and transient Promotion Candidate; User Acceptance Record version-pinned to an emission; user-attested Plan Fact; generic History Record), Derived projection definitions with confidence band/conflict attributes, a graph-friendly relationship map (with the dependency graph suited to Neo4j), logical lifecycle/versioning invariants (canonical append-only, recompute-appends-never-overwrites, one-way flow, version-pin integrity, provenance everywhere, Derived carries no authority), and deferred physical-binding notes mapping entities to Supabase Postgres/Neo4j/Supabase pgvector/Supabase Storage/Redis per the Environment Profile R2 decision (amended by DL-054: MongoDB and Qdrant removed) — honoring receipts-as-system-of-record with no Governance Decision entity, specifying no physical schema, and routing to the owner for review.*

**Release 1 Logical Data Model v1 complete.**

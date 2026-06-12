# Deep-task decisions — Wave A completion: IC-WA-001 (Intake) + IC-WA-002 (Retention)

**Scope:** the two remaining Phase II Wave A contracts. Lineage: continues
`r1-foundation-deep-task` (DTM-0001..0006 approved; 00R backbone live).
**Branch:** continue `feat/phase1-wavea-00r` — Wave A lands as one PR (no PR opened yet).
**Module ids continue:** DTM-0007 (001), DTM-0008 (002).

## Source-of-truth docs

| Concern | Path |
|---|---|
| Intake contract | `20_handoff/contracts/WAVE_A_CONTRACT_PACKAGE_001_ARTIFACT_INTAKE.md` (IC/QA/OBS-WA-001 + DL-047 claim-extraction/CRR additions) |
| Retention contract | `20_handoff/contracts/WAVE_A_CONTRACT_PACKAGE_002_CANONICAL_KNOWLEDGE_RETENTION.md` — **DL-043 amendments at top govern over the older Authority-referencing clauses** (A4.1, A5, A8, A10.1: admission is integrity-gated; no Authority in R1) |
| Data fields | `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` §2.1 (attested_assertion), §2.3 (Evidence & Intake; PromotionCandidate transient), §2.4 (UAR), §2.5 (history_record) |
| Storage binding | env profile §2 (DL-054): **artifact bodies → Supabase Storage**; metadata/refs → Postgres |
| Prior sequence | `code/docs/deep-tasks/r1-foundation-deep-task/` (all decisions inherited unless overridden) |

## Build order

**DTM-0007 = IC-WA-001 (Perceive) first**, then **DTM-0008 = IC-WA-002 (Retain)** —
matches the chain (Perceive produces Promotion Candidates; Retain admits). 0007's
acceptance-capture ends at a handoff seam + event; 0008 records the UAR.

## Locked implementation decisions

1. **Event vocabulary extension (gate-5 seam):** `events.py` currently pins EXACTLY the 7
   A6 names and gate-5 asserts them verbatim. Extend ADDITIVELY: per-contract tuples
   (`EVENT_NAMES_WA00R` unchanged, + `EVENT_NAMES_WA001`, `EVENT_NAMES_WA002`) with the
   union accepted by emitters; `ci/gate_observability.py` check (b) updated to assert each
   contract set verbatim. Done in DTM-0007 (first task to touch events).
2. **Intake schema (new migration, DTM-0007):** `artifact` (raw intake: id, project_id,
   body_ref → Supabase Storage path, normalized_form jsonb, provenance jsonb, dedup_key
   UNIQUE for idempotency, timestamps) + `promotion_candidate` (LDM §2.3: candidate_id,
   artifact_ref, normalized_form, readiness_state pending|ready|failed, integrity_clearance
   jsonb). Candidates are transient-but-audited → plain tables, NOT append-only-locked.
   `artifact` IS append-only (evidence anchor; LDM §2.3 "canonical evidentiary anchors") —
   same revoke+trigger pattern; add `artifact` to the gate-4 linter CANONICAL_TABLES
   (additive ci edit).
3. **Artifact bodies → Supabase Storage** bucket `artifacts` (DL-054 binding); Postgres
   holds the ref + normalized form. Local supabase ships Storage.
4. **Idempotency** = `dedup_key` (DL-053 name; content hash + project scope) UNIQUE
   constraint; re-intake returns the existing artifact (B2.4, no double admission).
5. **Claim extraction (EI-02)** in R1 increment = deterministic, rule-based extraction
   seam (no LLM yet — Wave B/S wires Pydantic AI): extractor interface + a minimal
   rule-based implementation producing evidence-attested `AttestedAssertion` drafts
   (content_type fact|assumption|constraint|dependency) with source locus. LLM extractor
   is a later registered implementation behind the same seam.
6. **Archival (A7/0008):** NO schema change — `archived` is recorded as an append-only
   `history_record` event (`event_type='archived'`, already in the DTM-0002 CHECK list);
   active/archived status derived from history. Avoids forbidden ALTER on canonical tables.
7. **Versioning/supersession (0008):** new version = new `attested_assertion` row with
   `version=N+1` + `supersedes_id`; explicit `knowledge-versioned`/`superseded` history
   events (A4.9 no silent supersession). DB append-only enforcement already live.
8. **Stale/change signal (0007 → 00R):** re-submission with same dedup scope but changed
   content emits the change signal and constructs a valid 00R `knowledge-change` /
   `promotion` TriggerClaim — integration point is `runner.submit_trigger` (consume, not
   modify).
9. **Acceptance capture (0007→0008):** Perceive captures `{user, item, version_pin,
   action}` and emits `user_acceptance_captured`; Retain's `record_acceptance` (0008)
   writes the UAR row (table exists). Capture ≠ acceptance (B3.4): no truth/approval
   marking anywhere.
10. **No HTTP endpoints in this sequence** — contracts are architecture-level; the API
    surface binds in a later transport task (needs platform/projects, out of Wave A scope).

## Inherited constraints (from r1-foundation decisions — still binding)

Ratified stack only; no new packages without approval; positive AND negative suites;
forbidden vocabulary (gate-4); workers never commit; live tests skipif env; PRs cite the
contract id (these tasks: `IC-WA-001` / `IC-WA-002`).

## Package approvals

- No new packages anticipated. supabase-py covers Storage. **Anything else = stop and ask.**

## Owner review fences (PR #21, 2026-06-13)

- **No-unarchive-in-R1 CONFLICTS with ratified UP-3** (archive specified as *reversible*;
  Free-tier cap resolution). Owner adjudicates **before any M6 work starts** — do NOT
  build M6 prompt/cap behavior against either assumption until ruled.
- Attribution-missing hard-reject and `failed→stale` recovery: queued owner decisions;
  PR #21 merge does not ratify them.
- ADR-0001 (monorepo placement): provisional until owner dispositions; merge ≠ ratification.

## Open conflicts / notes

- 002's original A4.1/A5/A8/A10.1 mention Authority — **superseded by its own DL-043
  amendments**; workers implement the amended (integrity-gated) semantics.
- Evidence-locus granularity (artifact + locus in `source_ref`) kept minimal jsonb;
  Wave B refines.

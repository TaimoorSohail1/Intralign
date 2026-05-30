# RB-010 — Disposition Document

## Decision Identifier

DL-035

## Title

Convert the Constitutional Principles Draft to a Historical Artifact per RB-010

## Disposition

**Accepted**

## Date Ratified

2026-05-29

## Authorizing Backlog Item

RB-010 — Resolve Constitutional Principles Draft vs Constitution Articles

## Selected Option

**Option C — Convert the Draft into a Historical Artifact.**

The file `01_doctrine_ontology/12_constitutional_principles_draft.md` is reclassified as non-canonical Source Material and relocated to `00_raw_transcript/05_constitutional_principles_draft.md`. Its substantive content is preserved as a historical record of the principles that informed the Doctrine and Constitution. Under the ratified architecture (DL-033), Source Material is non-canonical and cannot be cited as authority. The reclassification eliminates the duplicate-authority paradox that the Draft created at the Doctrine layer.

## Rationale

Of the 20 Draft principles, Draft Principle 17 was previously absorbed by Doctrine 02 per DL-034. The remaining 19 principles are evaluated against the two ratification criteria:

- **Preserving doctrinal integrity.** All 19 principles' substantive content is preserved by existing canonical content. 18 of 19 are represented directly by Constitution Articles 1, 2, 3, 5, 6, 7, 10, 11, 12, 18, 19, 21, 24, 25, 28, 31, 35, 45, and Doctrine 01–11. Draft 18 ("Outcome integrity supersedes workflow optimization") is the sole principle without a direct Article equivalent; its substance is captured by Article 2 (Understanding Before Execution, which prioritizes the outcome-integrity cluster over workflow acceleration) and Constitutional Drift Warning 2 (Workflow Drift, which warns of inversion). The supersession claim is implicit in those two surfaces and is explicitly preserved in the historical record by this disposition. No doctrinal information is lost.

- **Minimizing duplicate authority.** Retaining the Draft at the Doctrine layer creates duplicate canonical surfaces for 18 of 19 principles — each is both Drafted-Doctrinal and Constitutional. Under DL-033, doctrinal precedence applies, so the Drafted statements nominally outrank ratified Articles even where they are substantively identical. This is the canonical-authority paradox RB-010 was created to resolve. Reclassification to non-canonical Source Material eliminates the duplicate-authority surface entirely.

Option C uniquely satisfies both criteria. Options A, B, D, and E are rejected for reasons recorded below.

## Rejected Options

**Option A — Retire the Draft entirely.** Rejected. Deletion preserves substance via Constitution and Doctrine but loses the historical record of how the principles were originally drafted. The owner's broader principle of preserving original understanding and intent (per Proposal 000) favors explicit preservation over implicit preservation through git history.

**Option B — Ratify the Draft as Doctrine.** Rejected. Ratification maximizes duplicate authority by establishing 19 Drafted doctrinal positions that overlap with 18+ ratified Constitution Articles. Under DL-033, the Drafted positions would outrank the Articles. This inverts the ratified-Constitution authority relationship and fails the minimize-duplicate-authority criterion directly.

**Option D — Convert into a non-authoritative summary document.** Rejected. A summary document remains in the canonical content surface (Doctrine or Constitution folder), preserving file-level proximity to authoritative content. Contributors may continue to cite it informally. The summary format is also inconsistent with Draft 18, which does not summarize any single Article. Option C achieves the same preservation goal with cleaner non-canonical classification.

**Option E — Split and disposition principles individually.** Rejected. Of the 19 remaining principles, 18 are already represented in canonical Content (Constitution) and would be disposed as "absorbed by Article N." Draft 18 alone has unique content; its disposition without a new Proposal would either repeat the Option C historical preservation logic or require splitting it into a new doctrinal claim (which Option E would propose but cannot complete within the no-new-Proposals constraint). Option E collapses to Option C in effect while adding procedural overhead for no incremental benefit.

## Effects on Doctrine

- `01_doctrine_ontology/12_constitutional_principles_draft.md` is removed from the Doctrine folder via relocation.
- Doctrine 01–11 are unchanged. They remain the canonical foundational layer.
- Doctrine 02 retains its canonical-source role for the Cognition Scope axis (per DL-034). Draft Principle 17's substance continues to be canonized through Doctrine 02.
- No new doctrine is introduced. No existing doctrine is amended or superseded.
- The Doctrine layer becomes structurally cleaner: it no longer contains a Drafted file that nominally outranks ratified Constitution Articles.

## Effects on Constitution

- Constitution Articles 1–50 are unchanged.
- The 18 Articles that substantively mirror Draft principles (1, 2, 3, 5, 6, 7, 10, 11, 12, 18, 19, 21, 24, 25, 28, 31, 35, 45) gain effective operational authority because no Drafted-Doctrinal counterpart now sits above them.
- Article 2 and Constitutional Drift Warning 2 (in `01_governance/constitution/12_constitutional_drift_warnings.md`) are implicitly load-bearing for the Draft 18 supersession concept. No edits are made to either; the disposition records that they substantively capture Draft 18's claim.
- No Articles are amended, superseded, or annotated. The Constitution is structurally untouched.

## Effects on DL-033

- DL-033 (Doctrine-Centered Repository Architecture) is unaffected as a Decision.
- The architecture's Conflict Resolution Model (Doctrine > Constitution) operates more cleanly because the Drafted-Doctrinal surface that previously triggered nominal precedence over 18 Articles is removed.
- The architecture's Concept Promotion Model is unaffected.
- The Manifest, canonical_definitions.md, and ontology_registry.md headers (which cite DL-033) are unaffected.

## Effects on DL-034

- DL-034 (OSLO Evolution Framework) is unaffected as a Decision.
- Draft Principle 17, already absorbed by Doctrine 02 per DL-034, remains absorbed. Its substantive content continues to be canonized through Doctrine 02's four-stage Cognition Scope arc. The historical artifact preserves Draft 17 only as a record of how the principle was originally articulated; it adds no doctrinal force.
- Portfolio Cognition's provisional status (per DL-034) is unaffected.
- The four-axis taxonomy is unaffected.

## Effects on Backlog

- **RB-010** transitions from Partially Closed to **Closed**. The remaining 19 Draft principles (post-DL-034) are dispositioned by reclassification.
- No new backlog entries are created.
- Backlog items that referenced RB-010 as dependency or context: none directly. RB-005 (Layer Promotion and Citation Rule) is unaffected — its residual citation scope remains open.

## Effects on Citation Rules

- Contributors may no longer cite `01_doctrine_ontology/12_constitutional_principles_draft.md` as canonical Doctrine. The file no longer exists at that path.
- Contributors may reference the relocated file (`00_raw_transcript/05_constitutional_principles_draft.md`) as Source Material for historical context only. Per DL-033, Source Material informs but does not bind; it cannot be cited as authority in Proposals.
- For each of the 18 represented principles, contributors should cite the corresponding Constitution Article(s) as identified in the RB-010 Disposition Report mapping table.
- For Draft 18's supersession concept, contributors should cite Article 2 and Constitutional Drift Warning 2 in combination.

## Affected Artifacts

- `01_doctrine_ontology/12_constitutional_principles_draft.md` — file removed from this location.
- `00_raw_transcript/05_constitutional_principles_draft.md` — file placed here as Source Material with non-canonical Historical Artifact header.
- `00_raw_transcript/00_transcript_index.md` — index updated to register the new file.
- `01_governance/constitution/01_foundational_constitutional_doctrine.md`, `01_governance/constitution/02_epistemic_constitution.md`, and other Constitution files — substantively unchanged; their Articles continue to express the principles that the Draft compiled.
- `01_governance/constitution/12_constitutional_drift_warnings.md` — substantively unchanged; Drift Warning 2 implicitly carries the Draft 18 supersession framing.
- `canonical_definitions.md` — no new definitions added; entries that reference Doctrine 12 may be reviewed for accuracy but require no modification (none reference Doctrine 12 as a primary source).
- `ontology_registry.md` — no new entries added.
- `01_governance/decisions/decision_log.md` — DL-035 entry appended.
- `01_governance/backlog/revision_backlog.md` — RB-010 closed.
- `01_governance/changelog/changelog.md` — corresponding CHG entries.
- `01_governance/decisions/rb_010_disposition.md` — this document, placed.

## Required Repository Actions

1. Place this disposition document at `01_governance/decisions/rb_010_disposition.md`.
2. Record DL-035 in `01_governance/decisions/decision_log.md`.
3. Relocate `01_doctrine_ontology/12_constitutional_principles_draft.md` to `00_raw_transcript/05_constitutional_principles_draft.md`. The principles content is preserved verbatim; the pre-ratification "Governance Status" header section and the DL-034 inline Draft 17 absorption note are superseded by a single "Historical Artifact" header section that records: (a) the file's pre-DL-033 location and Drafted-Doctrinal status; (b) DL-035 as the authorizing reclassification Decision; (c) the file's current status as non-canonical Source Material; (d) the disposition of Draft Principle 17 per DL-034; (e) the disposition of the remaining 19 principles by reclassification per DL-035.
4. Update `00_raw_transcript/00_transcript_index.md` to register the new file with a one-line entry noting its provenance and non-canonical status.
5. Update `01_governance/backlog/revision_backlog.md` to close RB-010 with DL-035 as the closing Decision.
6. Record CHG entries authorized by DL-035 for the placement, the relocation, the index update, and the backlog closure.

No edits to Constitution Articles. No new Doctrine introduced. No new Proposals, Frameworks, Reviews, or Backlog entries created.

## Status

**Ratified.** This disposition is operative as of 2026-05-29.

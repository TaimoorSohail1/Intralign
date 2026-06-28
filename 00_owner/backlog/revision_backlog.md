# Revision Backlog

## Status

**Operative — Governance Framework Active**

The revision backlog operates under Framework 001 (per DL-030) and Framework 001A (per DL-031) as of 2026-05-28. Entries record proposed revisions to repository content. Promotion of any entry from Proposed to Ratified for Work requires a Proposal processed through the operative governance lifecycle.

**Governance Discipline Directive (per Repository Owner Action Plan):** New backlog entries are temporarily restricted to items required to resolve Proposal 000 unless specifically directed by the repository owner.

Entries are not prioritized for scheduling at the backlog level. Sequencing is determined during Review under Framework 001A.

---

## Entry Schema

Each entry contains:

- **ID** — Backlog identifier (RB-NNN).
- **Title** — Short descriptive title.
- **Source Finding** — Where the gap or conflict was identified.
- **Affected Layer(s)** — Doctrine, Constitution, Implementation Spec, Manifest, or Root Governance.
- **Affected Concepts** — Ontology entries touched.
- **Proposal Scope** — What the revision would address (not implementation detail).
- **Dependencies** — Other backlog items this is blocked by or blocks.
- **Status** — Proposed, Under Review, Ratified for Work, Deferred, or Closed.

All entries below are **Proposed**.

---

## P0 — Foundational Governance

### RB-001 — Canonical Registry Consolidation

- **Source Finding:** Two canonical-definitions surfaces exist — `00_owner/constitution/10_canonical_definitions.md` is populated; root `canonical_definitions.md` and `ontology_registry.md` were empty until this initial draft. The manifest does not declare which is authoritative.
- **Affected Layer(s):** Constitution; Root Governance.
- **Affected Concepts:** All canonical definitions; all ontology entries.
- **Proposal Scope:** Declare a single source of truth for canonical definitions and the ontology registry. Reconcile divergent definitions (Outcome Integrity States, Epistemic Object Types, Confidence Drivers). Establish the relationship between the root registry, the root definitions file, and the Constitution's definitions article.
- **Dependencies:** Blocks RB-002, RB-003.
- **Disposition:** Closed — Resolved by DL-036 with disposition Accepted with Conditions. Scope was bounded to Registry Foundation work (Resolutions R1 through R8) per the owner's RB-001 Scope Directive. Ontology conflict reconciliation (the original split-source definitions for Outcome Integrity States, Epistemic Object Types, Confidence Drivers) was explicitly excluded and deferred to RB-006, RB-007, RB-008 respectively. Doctrine stubs were excluded and deferred to RB-004. R1 declared the Surface Authority rule between root `canonical_definitions.md` (Governance-tier orientation) and Constitution Article 10 (Content-tier definitional surface). R2 declared the six-flag status taxonomy. R3 declared status-change rules. R4 registered nine canonical doctrinal concepts using existing Doctrine sources. R5 deprecated four predecessor names. R6 disambiguated "Provisional" terminology. R7 produced Inventories I-A (13 unanchored implementation concept groups) and I-B (4 registry entries lacking authoritative definitions). R8 declared canonical citation paths for the four OSLO Evolution Framework axes. Eight closing-Decision clarifications are recorded in `00_owner/decisions/rb_001_disposition.md`.
- **Closed By:** DL-036 (Accepted with Conditions).
- **Date Closed:** 2026-05-29
- **Status:** Closed.

### RB-002 — Governance Traceability Spine

- **Source Finding:** `decision_log.md` and this file (`revision_backlog.md`) were empty prior to the initial governance review draft. `changelog.md` remained empty. No schema or workflow existed for recording governance decisions, revisions, or changes.
- **Affected Layer(s):** Root Governance.
- **Affected Concepts:** All canonical content.
- **Proposal Scope:** Define the schema and workflow for `decision_log.md`, `revision_backlog.md`, and `changelog.md`. Specify what a decision entry, backlog entry, and changelog entry must contain. Specify ratification triggers and supersession rules.
- **Dependencies:** None.
- **Disposition:** Closed — Resolved through adoption of Framework 001 (DL-030) with the condition that the Traceability Record schema remains an open governance item. The condition is recorded against DL-030 itself; no successor backlog entry is created at this time per the governance discipline directive.
- **Closed By:** DL-030 (Accepted with Conditions); DL-031 (Accepted).
- **Date Closed:** 2026-05-28
- **Status:** Closed.

### RB-003 — Progression Model Reconciliation

- **Source Finding:** The repository contains at least five overlapping progressions: Organizational Cognition Arc (Doctrine 02), Product Evolution Stages (Doctrine 09, Article 40), Trust Evolution (Doctrine 09, Article 41), Execution Maturity Phases (Doctrine 10, Article 43), and Organizational Cognition Expansion (Article 44, which adds Portfolio Cognition as a fifth stage). Stage counts and labels are inconsistent.
- **Affected Layer(s):** Doctrine; Constitution.
- **Affected Concepts:** Organizational Cognition Arc; Trust Evolution; Execution Maturity Phases; Product Evolution Stages; Portfolio Cognition.
- **Proposal Scope:** Reconcile the progressions into a single canonical Progression Model with named axes. Provide mappings showing how each existing progression projects onto it. Resolve the four-stage versus five-stage inconsistency. Do not eliminate any progression without explicit supersession.
- **Dependencies:** Blocked by RB-001.
- **Disposition:** Closed — Resolved by DL-034. The OSLO Evolution Framework is ratified as a four-axis taxonomy (Cognition Scope, Product Identity, Trust Gradient, Execution Depth). Doctrine 02 is canonical for Cognition Scope. Doctrine 09 is canonical for Product Identity and Trust Gradient. Doctrine 10 is canonical for Execution Depth. Article 40 Stage 3 label and Article 44 five-stage arc are provisional; doctrinal precedence applies. Portfolio Cognition is dispositioned as a provisional long-term capability, not a ratified stage. Full taxonomy detail recorded in `00_owner/decisions/rb_003_disposition.md`.
- **Closed By:** DL-034.
- **Date Closed:** 2026-05-29
- **Status:** Closed.

### RB-004 — Doctrine Stubs for Under-Specified Systems

- **Source Finding:** Several concepts are named in canonical or specification material without doctrinal definition. They include: Working Memory, Outcome Map, Alternative Outcome Models, Confidence Scoring Methodology, Assumption Expiration, Policy DSL, Collaboration Role Model, Agent Governance, Portfolio Cognition, Project MRI subsystem internals.
- **Affected Layer(s):** Doctrine; Constitution.
- **Affected Concepts:** As listed above.
- **Proposal Scope:** Establish a "doctrine-stub" convention. Each stub declares concept scope, dependencies on existing doctrine, and open questions blocking ratification. Stubs ensure specification cannot quietly fill in undefined doctrinal territory.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-005 — Layer Promotion and Citation Rule

- **Source Finding:** The manifest declares precedence among layers but does not declare the relationship between doctrine and Constitution, nor how a concept is promoted from doctrine to Constitution, nor how implementation specs must cite the Articles they implement.
- **Affected Layer(s):** Manifest; Root Governance.
- **Affected Concepts:** All canonical content.
- **Proposal Scope:** Constitutionalize the promotion rule between layers. Declare whether the Constitution is derived from, peer to, or supreme over doctrine. Define what evidence is required to promote a doctrinal concept into a Constitutional Article. Require implementation specs to cite the Article(s) they implement. Place the manifest itself in the precedence hierarchy.
- **Dependencies:** Blocks ratification of any Stated decision in `decision_log.md`.
- **Disposition:** Partially Closed — Resolved by DL-033 for the precedence hierarchy and concept promotion model (Doctrine > Constitution > Implementation Specifications; promotion paths declared in the disposition document). Residual scope remains: explicit citation requirements for Implementation Specs (how an Implementation Spec must cite the Doctrinal or Constitutional source it implements).
- **Partially Closed By:** DL-033.
- **Date Partially Closed:** 2026-05-29
- **Status:** Partially Closed.

---

## P1 — Conflict Reconciliation

### RB-006 — Reconcile Outcome Integrity States

- **Source Finding:** Three sources list different state sets. Doctrine 04 lists Initial, Clarified, Aligned, Feasible, Governed, Execution Ready, Fragile, Drift Emerging. Article 33 omits Initial. Spec 08 adds "At Risk." `03_implementation_specs/02_plg_60_second_flow_wireframes.md` Screen 5 uses the compound phrase "Clarified but Fragile."
- **Affected Layer(s):** Doctrine; Constitution; Implementation Spec.
- **Affected Concepts:** Outcome Integrity States.
- **Proposal Scope:** Ratify a single state set. Decide whether compound states are permitted, and if so, how they compose. Resolve whether "At Risk" is canonical or spec drift.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-007 — Reconcile Epistemic Object Types vs Epistemic Labels

- **Source Finding:** Constitution Article 8 names five Epistemic Object Types (Facts, Inferences, Assumptions, Recommendations, Conflicts). Component Spec section 3 lists nine "Epistemic Label" types by adding Unknown, Provisional, Weakly Supported, Validated — conflating epistemic kind with epistemic strength.
- **Affected Layer(s):** Constitution; Implementation Spec.
- **Affected Concepts:** Epistemic Object Types; Confidence (as strength dimension).
- **Proposal Scope:** Separate epistemic kind from epistemic strength. Decide whether the five canonical types form a closed set, and whether strength labels belong to a different concept entirely.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-008 — Reconcile Confidence Drivers

- **Source Finding:** `00_owner/doctrine/06_confidence_understanding_model.md` lists seven drivers. `03_implementation_specs/09_confidence_integrity_logic.md` lists nine, adding stakeholder coverage and dependency stability.
- **Affected Layer(s):** Doctrine; Implementation Spec.
- **Affected Concepts:** Confidence; Confidence Drivers.
- **Proposal Scope:** Ratify a single driver set. If specification needs additional inputs, route them through doctrine before adoption.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-009 — Reconcile Override State Model with Override Severity Tiers

- **Source Finding:** `03_implementation_specs/08_state_logic_state_machines.md` defines an eight-state Override state machine (Proposed, Low Impact Accepted, Rationale Required, Rationale Provided, Approved, Rejected, Escalated, Recorded). `03_implementation_specs/11_governance_override_logic.md` defines four severity tiers (Low, Moderate, High, Governance Critical). No mapping exists.
- **Affected Layer(s):** Implementation Spec.
- **Affected Concepts:** Human Override; Governance Escalation.
- **Proposal Scope:** Map states to severity tiers. Determine whether severity drives state transitions or vice versa.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-010 — Resolve Constitutional Principles Draft vs Constitution Articles

- **Source Finding:** `01_doctrine_ontology/12_constitutional_principles_draft.md` enumerates twenty principles. The Constitution enumerates fifty Articles. Significant overlap exists with different numbering and phrasing. No document declares which supersedes which.
- **Affected Layer(s):** Doctrine; Constitution.
- **Affected Concepts:** Constitutional Principles; all Articles.
- **Proposal Scope:** Decide the disposition of the draft principles. Either supersede them with the Articles, ratify them as a parallel summary, or fold them into the Constitution. Record the disposition.
- **Dependencies:** Blocked by RB-005.
- **Disposition:** Closed — Resolved by DL-035. The file `01_doctrine_ontology/12_constitutional_principles_draft.md` is reclassified as non-canonical Source Material and relocated to `00_raw_transcript/05_constitutional_principles_draft.md` with a Historical Artifact header. Draft Principle 17's substantive content remains absorbed by Doctrine 02 per DL-034. The remaining 19 principles are dispositioned by reclassification: 18 are substantively represented by Constitution Articles 1, 2, 3, 5, 6, 7, 10, 11, 12, 18, 19, 21, 24, 25, 28, 31, 35, and 45; Draft Principle 18 is substantively captured by Article 2 and Constitutional Drift Warning 2. Full disposition detail recorded in `00_owner/decisions/rb_010_disposition.md`.
- **Closed By:** DL-035 (final disposition). Prior partial closures recorded by DL-033 (precedence framework) and DL-034 (Draft Principle 17 absorption).
- **Date Closed:** 2026-05-29 (DL-035 final closure).
- **Status:** Closed.

### RB-011 — Resolve "Lifecycle" Terminology Tension

- **Source Finding:** `repository_manifest.md` discloses the acronym "Outcome-Driven Strategic Lifecycle Orchestration." The term *Lifecycle* is in tension with the doctrinal stance that Outcome Integrity States are not workflow phases (DL-014). No source anchors the *Strategic Lifecycle* compound.
- **Affected Layer(s):** Manifest; Doctrine; Constitution.
- **Affected Concepts:** OSLO (concept and acronym); Outcome Integrity States; Execution Maturity Phases.
- **Proposal Scope:** Reconcile the acronym with the non-lifecycle stance. Either anchor *Lifecycle* doctrinally with a definition that does not contradict existing doctrine, or revise the acronym, or add a manifest annotation acknowledging the historical compound.
- **Dependencies:** Blocked by RB-005.
- **Disposition:** Closed — Resolved by DL-033. Under the doctrine-centered architecture, the Manifest sits in the Governance tier as orientation with non-doctrinal force. The "Lifecycle" term in the OSLO acronym is therefore advisory and carries no doctrinal weight. The pre-ratification annotation on `repository_manifest.md` records the advisory status of substantive Manifest claims. Future promotion of *Lifecycle* to the Content tier would require a Proposal.
- **Closed By:** DL-033.
- **Date Closed:** 2026-05-29
- **Status:** Closed.

---

## P2 — Scoping and Anchoring

### RB-012 — Anchor the Collaboration Role Model

- **Source Finding:** `03_implementation_specs/10_collaboration_sharing_logic.md` introduces six collaboration roles (Viewer, Commenter, Clarifier, Approver, Governance Reviewer, Owner) without doctrinal or constitutional basis.
- **Affected Layer(s):** Doctrine; Constitution; Implementation Spec.
- **Affected Concepts:** Collaboration Role Model; Governance.
- **Proposal Scope:** Establish doctrinal grounding for the role model. Tie each role to existing collaboration layers (Artifact-Level, Intelligence-Level, Understanding-Level).
- **Dependencies:** Blocked by RB-004.
- **Status:** Proposed.

### RB-013 — Define the Attention Queue Canonically

- **Source Finding:** `00_owner/doctrine/05_workspace_navigation_doctrine.md` describes Attention Queue as a "persistent operational intelligence surface." Specs describe it as a queue sorted by outcome impact. No single defining statement exists.
- **Affected Layer(s):** Doctrine; Constitution; Implementation Spec.
- **Affected Concepts:** Attention Queue.
- **Proposal Scope:** Provide a single canonical definition. Reconcile the surface-versus-queue framings.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-014 — Define Artifact Canonically

- **Source Finding:** Artifact is referenced throughout doctrine, Constitution, and specs. The five Artifact Domains are enumerated. No single defining statement of *Artifact* itself exists.
- **Affected Layer(s):** Doctrine; Constitution.
- **Affected Concepts:** Artifact; Artifact Domains.
- **Proposal Scope:** Provide a single canonical definition that distinguishes Artifact from Understanding surfaces and from epistemic objects.
- **Dependencies:** Blocked by RB-001.
- **Status:** Proposed.

### RB-015 — Scope Project MRI Doctrinally

- **Source Finding:** `04_project_mri/README.md` is a stub. The manifest scopes Project MRI to ambiguity, fragility, confidence, outcome integrity risk, understanding gaps, and interpretation drift exposure. No doctrinal mapping exists between Project MRI concerns and the existing ontology.
- **Affected Layer(s):** Doctrine; Manifest.
- **Affected Concepts:** Project MRI; Confidence; Outcome Integrity; Understanding Boundaries.
- **Proposal Scope:** Map each of the six Project MRI concerns to existing ontology entries. Decide whether Project MRI is a workspace surface, a subsystem, or a doctrinal lens. Doctrine-stub required before specification.
- **Dependencies:** Blocked by RB-004.
- **Partial Unblock by DL-034:** The progression-model ambiguity that previously blocked Project MRI's analytical placement across axes is now resolved. Project MRI's positioning can be analyzed against the four ratified axes of the OSLO Evolution Framework (Cognition Scope, Product Identity, Trust Gradient, Execution Depth). The subsystem still requires doctrinal scoping; RB-004 remains the upstream blocker for the scoping decision itself.
- **Status:** Proposed (partially unblocked).

### RB-016 — Anchor Confidence Scoring Methodology

- **Source Finding:** `03_implementation_specs/14_open_questions_design_risks.md` Open Question 1 explicitly leaves confidence scoring methodology undefined. Confidence is load-bearing across every layer.
- **Affected Layer(s):** Doctrine; Implementation Spec.
- **Affected Concepts:** Confidence; Confidence Drivers; Confidence Maturity.
- **Proposal Scope:** Establish a doctrine-stub defining what a scoring methodology must satisfy (decomposable, explainable, evidence-linked, historically traceable) without specifying the methodology itself.
- **Dependencies:** Blocked by RB-004, RB-008.
- **Status:** Proposed.

### RB-017 — Define Assumption Expiration Semantics

- **Source Finding:** `00_owner/doctrine/07_governance_policy_doctrine.md` offers "Assumptions expire after 30 days" as an example policy. No expiration semantics, revival rules, or propagation to confidence are defined.
- **Affected Layer(s):** Doctrine.
- **Affected Concepts:** Assumption; Confidence; Outcome Integrity Policy.
- **Proposal Scope:** Doctrine-stub for assumption lifecycle states and confidence impact. Do not specify thresholds.
- **Dependencies:** Blocked by RB-004.
- **Status:** Proposed.

### RB-018 — Establish Policy Grammar Doctrine

- **Source Finding:** Outcome Integrity Policies are described as human-readable doctrine, not workflow scripting. Several example policies exist. No defining structure for what constitutes a policy is provided.
- **Affected Layer(s):** Doctrine; Constitution.
- **Affected Concepts:** Outcome Integrity Policy.
- **Proposal Scope:** Doctrine-stub for the structural requirements of a policy statement (condition, evidence basis, affected integrity dimension, required resolution). Do not specify a DSL.
- **Dependencies:** Blocked by RB-004.
- **Status:** Proposed.

---

## P3 — Manifest Governance

### RB-019 — Place the Manifest in the Precedence Hierarchy

- **Source Finding:** `repository_manifest.md` functions as orientation but has no declared governance status, version, or ratification record. It declares precedence among the four canonical layers but does not place itself among them.
- **Affected Layer(s):** Manifest; Root Governance.
- **Affected Concepts:** All canonical content.
- **Proposal Scope:** Declare whether the manifest is meta-doctrine, charter, README, or a fifth canonical layer. Establish version and ratification record for the manifest.
- **Dependencies:** Blocked by RB-002, RB-005.
- **Disposition:** Closed — Resolved by DL-033. The Manifest is placed within the Governance tier as an orientation charter with non-doctrinal force. The pre-ratification annotation on `repository_manifest.md` records this placement and the advisory status of substantive Manifest claims.
- **Closed By:** DL-033.
- **Date Closed:** 2026-05-29
- **Status:** Closed.

### RB-020 — Populate Root README and CLAUDE.md

- **Source Finding:** `README.md` and `CLAUDE.md` at the repository root are empty. The manifest exists but does not substitute for orientation files used by tooling and contributors.
- **Affected Layer(s):** Root Governance.
- **Affected Concepts:** Repository orientation.
- **Proposal Scope:** Populate both files using only existing canonical content. README must cite the manifest as the authoritative orientation document. CLAUDE.md must record the governance posture for AI contributors as established by the project instructions and manifest.
- **Dependencies:** Blocked by RB-019.
- **Status:** Proposed.

---

## P4 — Build Governance & Tooling (DL-067 follow-ups)

_Added 2026-06-17 by explicit owner direction. These three items were surfaced by real CI failures while landing DL-068 (PR #38) and the psycopg/form-data fix (PR #37). They concern the realization of DL-067 (server-side DL landing) and DL-065 (number-at-merge), not canonical doctrine._

### RB-021 — dl-land workflow cannot carry a multi-line decision body

- **Source Finding:** Landing DL-068 via the `dl-land.yml` `workflow_dispatch` form (2026-06-17). The `body` input is a single-line `<input type="text">`; per the HTML value-sanitization algorithm it strips newlines, so multi-line markdown (the `## Decision` / `## Conditions` sections every record needs) cannot be entered through the Actions UI or the Founder Console "Approve & Land" path. The record had to be landed via a local `dl_records.py land` run instead.
- **Affected Layer(s):** Build Governance (engineering tooling); realization of DL-067.
- **Affected Concepts:** Decision-Recording Discipline (DL-065); single-serializer landing (DL-067).
- **Proposal Scope:** Make the dl-land body input newline-tolerant — e.g. switch to a multi-line input type, accept a sentinel the workflow expands into newlines, or accept the body as an uploaded/committed file path the workflow reads. Goal: the "Approve & Land" path works end-to-end without a manual local fallback.
- **Dependencies:** Realizes DL-067. No upstream blocker.
- **Status:** Proposed.

### RB-022 — dl-land PR body fails the Gate 2 contract-traceability check

- **Source Finding:** DL-068 PR #38 (2026-06-17) failed `app-ci` Gate 2 (`gate_contract`) because the PR body cited no approved contract id; the gate scans `PR_BODY` for an `IC-*` id or a `phase-1-infra` label. Pure-governance PRs (a DL record + changelog + index) have no natural contract id, so the auto-generated dl-land PR body will reliably fail this gate. Worked around by hand-editing the PR body to cite IC-WB-INFER / IC-WB-EVAL / IC-WA-00R and pushing an empty commit to re-trigger (a body edit alone does not refresh the frozen event payload).
- **Affected Layer(s):** Build Governance (CI policy + dl-land realization).
- **Affected Concepts:** Contract-traceability gate (Deployment Governance §4 Gate 2); DL-067 landing workflow.
- **Proposal Scope:** Let canon-only PRs pass Gate 2 cleanly — e.g. have dl-land apply a governance-exemption label (analogous to `phase-1-infra`) or inject an appropriate contract/citation into the generated PR body; and/or have Gate 2 recognize `decision/*` branches as governance changes. Owner ratifies the CI-policy intent; engineering proposes the realization.
- **Dependencies:** Realizes DL-067; related to RB-021.
- **Status:** Proposed.

### RB-023 — Renumber the dormant OD-005 / Outcome Graph decision record

- **Source Finding:** The `decision/dl-068-outcome-graph-elevation-deferral` branch (the OD-005 Outcome Graph elevation deferral, drafted as DL-068) was never merged; DL-068 was instead assigned at merge to the Wave A sign-off (number-at-merge, DL-065). The dormant branch still hard-codes DL-068 in its filename and header and will fail the records gate (header↔filename vs. next-free number) if landed as-is.
- **Affected Layer(s):** 00_owner/decisions (records regime).
- **Affected Concepts:** Outcome Graph elevation (OD-005); number-at-merge (DL-065).
- **Proposal Scope:** When the owner resumes the OD-005 decision, renumber the record to the next free DL number (rename file + header), rebase onto current `main`, and land via the standard flow. No content change to the decision itself.
- **Dependencies:** None (owner-initiated when OD-005 is taken up).
- **Status:** Proposed (deferred — owner-initiated).

### RB-024 — Wave B exit-gate review before Phase IV (DL-044 per-wave sign-off)

- **Source Finding:** DL-068 authorized Wave B (Understanding); DL-044 requires an **owner per-wave exit-gate review before Phase IV**. PR #39 (`feat/phase3-waveb-understanding`: Synthesis IC-WS-SYNTH → Infer IC-WB-INFER → Evaluate IC-WB-EVAL) is the Wave B realization — once it merges, this gate is the next governance checkpoint. Surfaced 2026-06-17 during the PR #39 review.
- **Affected Layer(s):** Build Governance (delivery); `00_owner` (decision/exit-gate).
- **Affected Concepts:** DL-044 wave-authorization / exit gate; Wave B (Understanding); Phase IV; DL-046 (Fast/Deep + <60s Time-to-First-MRI); DL-062 (CAF decomposability).
- **Proposal Scope:** Define and run the Wave B exit-gate review (Framework 001A five outputs — Findings / Concerns / Dependencies / Recommendation / Status) against the DL-068 authorized scope, the DL-046 NFR obligations, and the DL-062 decomposability condition (including the still-open CAF driver-level decomposability test flagged in the PR #39 review). Owner sign-off required; **no Phase IV start without it.**
- **Dependencies:** Blocked by PR #39 merge (Wave B landed). Relates to DL-068, DL-044, DL-046, DL-062.
- **Disposition:** Closed — the Wave B exit-gate review was run and ratified as **DL-072** (Pass with conditions; Phase IV/Wave C authorized). The review surfaced three binding conditions, now tracked as RB-025 (unarchive), RB-026 (decomposability test), and a DL-046 live-Gemma latency validation (shared with the DL-070 Phase 1 sign-off).
- **Closed By:** DL-072.
- **Date Closed:** 2026-06-18
- **Status:** Closed.

### RB-025 — Unarchive (DL-058) not built in Wave B; carry into Wave C

- **Source Finding:** The Wave B exit-gate review (DL-072) verified `code/backend/responsibilities/retain/archival.py` on `main` still declares "an explicit unarchive is OUT of scope in R1" — i.e., DL-058 (archive reversible in R1, UP-3 affirmed), which **DL-068 Condition 3 folded into Wave B**, was not delivered.
- **Affected Layer(s):** `30_engineering` (`code/`); realization of DL-058.
- **Affected Concepts:** Unarchive / archive reversal (DL-058); Retain responsibility.
- **Proposal Scope:** Build unarchive in **Wave C or a dedicated near-term slice** — a new reversal event type in the LDM §2.5 vocabulary + the derive-status path, append-only (no destruction), with positive/negative tests. Owner-accepted gap per DL-072 Condition 1.
- **Dependencies:** DL-058, DL-068 (Cond 3), DL-072 (Cond 1).
- **Status:** Proposed (binding condition of DL-072).

### RB-026 — DL-062 CAF driver-decomposability negative test missing

- **Source Finding:** The Wave B exit-gate review (DL-072) verified the evaluate negatives (`tests/negative/evaluate/test_b3_confidence_semantics.py`) cover Confidence-isn't-health, Reliability non-collapse, CONF-06, and a non-empty `basis`, but **no test asserts CAF drivers stay individually inspectable** in the confidence basis ("no opaque rollup") — which **DL-062 Condition 1 explicitly requires** as a QA negative test.
- **Affected Layer(s):** `30_engineering` (`code/` tests); realization of DL-062.
- **Affected Concepts:** CAF decomposability (DL-062 Cond 1); Confidence basis / inspectability (Doctrine 06).
- **Proposal Scope:** Add a negative test proving each of Clarity / Alignment / Feasibility decomposes to its inspectable drivers in the basis/explanation; an opaque rollup must fail.
- **Dependencies:** DL-062 (Cond 1), DL-072 (Cond 2).
- **Status:** Proposed (binding condition of DL-072).

---

## P5 — Roadmap Sequencing (owner-directed)

_Added 2026-06-28 by explicit owner direction. Captures the roadmap-sequencing principle from the cognitive-layer defensibility analysis and routes it through Framework 001 to bind as product-roadmap canon._

### RB-027 — Layer-Before-Depth roadmap sequencing

- **Source Finding:** Cognitive-layer defensibility analysis (2026-06-28) concluded OSLO's durable moat is altitude + cross-system neutrality + accumulated outcome corpus — not the cognitive behaviors (which frontier models increasingly absorb). The entry wedge ("60-second planning intelligence", Positioning §4) is capability-shaped and at risk of collapsing into a feature of an incumbent execution tool unless OSLO reaches the layer position first. No canonical sequencing rule governs the order in which the §7 ladder is realized after R1.
- **Affected Layer(s):** Product scope / roadmap orientation (`10_product`). Non-doctrinal.
- **Affected Concepts:** Strategic Objective Ladder (Positioning §7); Execution Depth axis (Doctrine 10 / DL-034); advisory-only invariant (DL-047); cross-platform neutrality / "layer" altitude.
- **Proposal Scope:** Ratify the **Layer-Before-Depth** principle — establish cross-platform planning-governance breadth (≥2 governed platforms, real per-platform depth) at the understanding/governance altitude before descending into execution-phase governance; execution-phase read-only visibility permitted earlier as a feedback input; advisory-only invariant (DL-047) preserved throughout; R1 scope unchanged (applies R2+). Sequences existing ladder levels; introduces no new doctrine, capability, or responsibility.
- **Dependencies:** Traces up to Positioning §7; constrained by DL-047 and Doctrine 10 / DL-034; consistent with DL-076, CHG-064. Lands after the in-flight canon PR (DL-080) per DL-065 R3.
- **Proposal:** `00_owner/decisions/PROPOSAL_ROADMAP_LAYER_SEQUENCING_DRAFT.md`. **Draft record:** `records/DL-081-roadmap-layer-sequencing.md`.
- **Status:** Proposed.

### RB-028 — Alpha exit criteria (specify "proven"; amends DL-076)

- **Source Finding:** Owner direction 2026-06-28 — the Alpha phase's three pillars (project-intelligence value validation, planning-vendor breadth, execution visibility) are **exit criteria**, not just activities. DL-076 defined the Alpha→Beta two-gate model (build/prove vs §20 graduation) but did not specify what "proven" requires.
- **Affected Layer(s):** Product scope / roadmap orientation (`10_product`). Non-doctrinal.
- **Affected Concepts:** Alpha→Beta graduation; "proven" gate (DL-076 §3); §20 engagement gate; planning-vendor breadth / neutrality; execution visibility (read-only, DL-047); value validation.
- **Proposal Scope:** Amend DL-076 by ratifying Alpha exit criteria: (1) build/prove gates pass [unchanged]; (2) value validated by behavioral retention/repeat use; (3) ≥ 2 governed planning/execution platforms with real per-platform depth; (4) execution visibility operational = read-only outcome ingest (≥ 1 platform) + closed feedback loop, drift-surfacing deferred to Beta+; (5) 50+ users + engagement (§20) [unchanged]. Owner-set thresholds.
- **Dependencies:** Amends DL-076; constrained by DL-047, §20, CHG-064; consistent with RB-027 / `DL-081-roadmap-layer-sequencing` (≥ 2 threshold; depth deferral). Lands after DL-080 per DL-065 R3; recommend after RB-027.
- **Proposal:** `00_owner/decisions/PROPOSAL_ALPHA_EXIT_CRITERIA_DRAFT.md`. **Draft record:** `records/DL-082-alpha-exit-criteria.md`. **Artifact:** `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a.
- **Status:** Adopted — DL-082.

### RB-029 — Execution-monitoring tier placement & phase (amends DL-082, extends DL-074)

- **Source Finding:** Owner direction 2026-06-28 — aligning tiering with the DL-082 Alpha exit criteria surfaced that "planning-vendor support" and "execution visibility" conflated three distinct capabilities (Export-Share-Out; outbound plan export to execution tool; inbound execution monitoring). The Tier-3 monitoring build lands in Beta, so it cannot gate Alpha graduation.
- **Affected Layer(s):** Product scope / roadmap + monetization orientation (`10_product`). Non-doctrinal.
- **Affected Concepts:** Alpha exit criteria (DL-082); tier ladder / capability placement (DL-074); execution monitoring / visibility; plan export; Export-Share-Out (G4); Layer-Before-Depth (DL-081).
- **Proposal Scope:** (1) Three-way tier split — Export-Share-Out = Free/no-account; plan export → execution tool = Tier 2/Basic (distinct, separately-scoped); execution monitoring = Tier 3/Pro+. (2) Move execution monitoring from Alpha exit to Beta (built at T3 in Beta); amend Alpha exit to build/prove + value-by-retention + ≥2 planning sources + 50+ users. (3) Alpha validates engagement; Beta validates outcome impact. (4) Plan export-out is not-yet-scoped — placement only, not authorization.
- **Dependencies:** Amends DL-082; extends DL-074; constrained by DL-047, DL-081, CHG-064, §20. Routes plan-export and monitoring realization to separate scoping.
- **Proposal:** `00_owner/decisions/PROPOSAL_EXECUTION_MONITORING_TIER_AND_PHASE_DRAFT.md`. **Draft record:** `records/DL-083-execution-monitoring-tier-and-phase.md`. **Artifact:** `10_product/scope/RELEASE_MODEL_AND_ALPHA_LADDER_V1.md` §3a.
- **Status:** Proposed.

---

## Governance Notes

1. This backlog is a draft. Entries reflect findings from initial repository review, not ratified governance positions.
2. Promotion of any entry from Proposed to Ratified for Work requires the governance workflow established by RB-002 and the promotion rule established by RB-005.
3. New entries should cite the source finding explicitly. Entries inferred without source citation should not be added.
4. Entries that close existing items must reference them in a Supersedes field.

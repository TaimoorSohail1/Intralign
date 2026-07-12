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

### RB-017 — Define Assumption Lifecycle & Expiration Semantics

- **Source Finding:** `00_owner/doctrine/07_governance_policy_doctrine.md` offers "Assumptions expire after 30 days" as an example policy. No expiration semantics, revival rules, or propagation to confidence are defined. **(Elaborated 2026-07-12, owner-directed):** the design philosophy *"Designing for Evolving Organizational Understanding"* (§1, §3, §6, Examples 3 & 5) requests that an assumption's validation state be visible, that OSLO prompt for re-validation when confidence rests on unvalidated assumptions, and that a project be able to answer "which assumptions failed." These are surface behaviors that require this doctrine-stub to exist first.
- **Affected Layer(s):** Doctrine.
- **Affected Concepts:** Assumption; Confidence; confidence driver "assumption stability" (currently *Conflicting*, `ontology_registry.md`); Reliability qualifier; Outcome Integrity Policy; Understanding Timeline / History.
- **Proposal Scope:** Doctrine-stub for assumption **lifecycle states** and the **direction** of their confidence impact. Candidate state set for owner ratification: *unvalidated → validated / invalidated*, plus *expired* and *revived* (the expiration-policy transitions). **Do not specify thresholds, decay rates, or magnitudes** (those route to calibration, Class B). Constraints the stub must honor: (a) epistemic **grounding is permanent** (`RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`) — validation state lives on the **Confidence/quality plane**, never as an Attested↔Derived move; (b) **no new stored object** — Assumption stays a content sub-type of AttestedAssertion; (c) any re-validation prompt is governed by **Progressive Visibility** (Constitution Art. 25) and drift warning #6 — it fires on material consequence, never routinely.
- **Dependencies:** Blocked by RB-004. Related to **RB-007** (separate epistemic *kind* from *strength* labels incl. "Validated") and **RB-016** (confidence-scoring doctrine-stub); do **not** name a "Validated" state until RB-007's kind-vs-strength reconciliation is settled.
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
- **Status:** Adopted — DL-081.

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
- **Status:** Adopted — DL-083.

### RB-030 — Scope the plan-export-to-execution-tool capability (outbound)

- **Source Finding:** DL-083 placed **plan export → execution tool** at **Tier 2 / Basic** but flagged it as a **distinct, not-yet-scoped** capability — the G4 Export-Share-Out contract is a *read-only orientation share*, not a *push-to-execution-tool*. The capability is undefined in canon; tier placement is **not** build authorization (Anti-Assumption).
- **Affected Layer(s):** Product scope (`10_product`) → `20_handoff` / `30_engineering` for realization. Non-doctrinal (capability scoping).
- **Affected Concepts:** Plan export (outbound); Export-Share-Out / G4 (Wave E); planning artifact model (DL-077); execution-tool connectors; tier placement (DL-074 / DL-083); advisory-only (DL-047).
- **Proposal Scope:** Scope the outbound plan-export capability — **which** execution/planning platforms (Jira · Asana · MS Project · …); **one-way push vs round-trip**; **plan → work-item mapping** semantics (how the OSLO planning artifact maps to platform tasks); update/idempotency behavior; the **connector/auth surface** (commodity, Category-E) vs any contracted seam; **Tier-2 gating** (per DL-083) and cost profile (one-shot, low). Explicitly distinguish from **G4 share-out** and from **inbound execution monitoring (RB-031)**. Produce a Capability-Matrix entry + target Release. Carries integration-governance history (**DL-042** Integration Moratorium Closure) — scope deliberately, not by inference.
- **Dependencies:** Placed by DL-083 (Tier 2). Distinct from RB-031 (inbound) and G4 (share-out). Relates to DL-077 (planning artifact). Connector work under DL-042 history. Advisory-only (DL-047) preserved — an outbound artifact push, not OSLO acting on the execution system.
- **Status:** Proposed.

### RB-031 — Scope the execution-monitoring realization (inbound; Tier 3 / Pro+, Beta)

- **Source Finding:** DL-083 placed **execution monitoring** at **Tier 3 / Pro+**, built in **Beta**, and moved it out of the Alpha exit criteria — but the realization (which platforms, the intake seam, build, config) is unscoped. The 2026-06-05 tier-progression note flagged it as "not R1 unless scoped," with governance flags.
- **Affected Layer(s):** Product scope (`10_product`) → `20_handoff` / `30_engineering`; monetization (Calibration §4c). Non-doctrinal (capability scoping).
- **Affected Concepts:** Execution monitoring / visibility (inbound outcome ingest + closed loop); Outcome Integrity / Current Reality (Doctrine 04); Perceive intake / Attested provenance; Derived cognition (recompute / CHR); tier placement (DL-074 / DL-083); cost governance (DL-048); integration moratorium (DL-042); Internal/Alpha entitlement.
- **Proposal Scope:** Scope the inbound monitoring capability — **which** execution platforms; the **evidence-intake seam** (external outcome data → Perceive → **Attested** with provenance = external system → **Derived** "on-track / drifting" read, recomputable, CHR-appended) [**contracted**] vs the **connector/sync/field-mapping** layer [**commodity**, Category-E]; the **closed feedback loop** (governed understanding vs observed outcomes); **polling/coalescing** + the recurring-cost + rate-limit surface folded under DL-048 per-tier budgets; **Tier-3/Pro+ gating** + Calibration §4c rows; **Beta** build placement; **Alpha validation via the Internal/Alpha entitlement** (test-bypass backlog). Drift-surfacing remains a later execution-intelligence behavior (out of scope here). Maps to the **Current-Reality** side of Outcome Integrity — feeds the signal, no parallel truth path. Produce a Capability-Matrix entry + Release placement; **DL-042** integration history applies.
- **Dependencies:** Placed by DL-083 (Tier 3, Beta). Constrained by DL-047 (read-only / advisory-only), DL-048 (cost), Doctrine 04 (Outcome Integrity). Relates to DL-081 (Layer-Before-Depth — execution depth after breadth) and the Internal/Alpha entitlement backlog. Distinct from RB-030 (outbound export). DL-042 moratorium history.
- **Status:** Proposed.

### RB-032 — R2 candidate-epic phase/tier placement + Foundational-Architecture-in-Alpha principle

- **Source Finding:** Owner direction 2026-06-28 — the R2 candidate index gathered deferred epics without binding *when* each begins. Owner set the gates: Execution Intelligence (R2-C) → Beta; Team Collaboration depth (R2-D) → Team tier; Governance & Authority (R2-E) → Beta; plus a build-sequencing exception allowing foundational architecture to be laid early in Alpha where it reduces later effort/complexity.
- **Affected Layer(s):** Product scope / roadmap + build-sequencing orientation (`10_product`). Non-doctrinal.
- **Affected Concepts:** R2 candidate epics (R2-C/D/E); Alpha/Beta phases (DL-076); tier ladder (DL-074); execution monitoring (DL-083); Layer-Before-Depth (DL-081); advisory-only (DL-047); foundational-architecture build sequencing.
- **Proposal Scope:** Bind the three phase/tier placements and ratify the **Foundational-Architecture-in-Alpha** principle (early foundation permitted in Alpha when it measurably reduces later effort/complexity; advisory-only, non-activating, specified-but-inactive; routes through scoping + DL where architectural). Additive; no capability/doctrine introduced.
- **Dependencies:** Builds on DL-076, DL-074, DL-083, DL-081, DL-047, CHG-064. Reflected in `RELEASE_2_BACKLOG_CANDIDATES.md` (Phase & tier placement note).
- **Proposal:** `00_owner/decisions/PROPOSAL_R2_PHASE_TIER_PLACEMENT_DRAFT.md`. **Draft record:** `records/DL-084-r2-phase-tier-placement.md`.
- **Status:** Proposed.

### RB-033 — Epistemic basis on Findings (two-axis type + basis; R1 presentation, R2 sub-typing)

- **Source Finding:** Owner observation 2026-07-02 — Findings do not surface the epistemic language PMs use ("inferred," "assumed/assumption," "stated"), although canon already ratifies the vocabulary (Attested/Derived; assumption/constraint/dependency content types) and a **Disclose obligation** (`RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`). A consistency check found the Finding card non-conformant to `FINDING_PRESENTATION_SPECIFICATION_V1` §C (required "Finding type" not rendered), and that "inference" was conflated with a finding **type** rather than the Derived **basis** — conflicting with the ratified **Gap / Conflict / Risk** finding types (Architecture Foundation M-3; `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING`).
- **Affected Layer(s):** Product experience (`10_product/experience`) for R1 presentation; Finding object model + Wave B Infer/Evaluate contracts (`20_handoff`) for R2. Non-doctrinal.
- **Affected Concepts:** Finding type (Gap/Conflict/Risk); epistemic state (Attested/Derived); content types (assumption/ambiguity); Disclose obligation; finding-type-as-label-not-coefficient (Outcome-Confidence Calibration); DL-087 plain-language labels.
- **Proposal Scope:** A **two-axis** model — **type** (what the observation is: Gap/Conflict/Risk + finer kinds) separate from **basis** (how grounded: stated=Attested vs inferred=Derived). **Phase R1 (presentation — ready to ratify):** amend `FINDING_PRESENTATION_SPECIFICATION_V1` §C/§F + `FINDING_PANEL_SPECIFICATION_V1` so the card carries type + a stated/inferred basis tag and the panel names the basis in plain language (discharging the Disclose obligation at the finding level); drop "Inference" as a type. Realized in the reference prototype (baseline `03-findings`); presentation-only, no object/doctrine change. **Phase R2 (ontology — deferred):** formalize the finer kinds (Assumption/Ambiguity/Coverage-gap/Missing-info) as **sub-types of Gap/Conflict/Risk** in the Finding object model, and specify the **basis-assignment contract** (which of Infer/Evaluate sets a finding's Attested/Derived basis).
- **Dependencies:** `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`; Architecture Foundation M-3 + `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING` (Gap/Conflict/Risk); `CANONICAL_GLOSSARY` (Attested/Derived, DL-087); `FINDING_PRESENTATION_SPECIFICATION_V1` §C/§F; `FINDING_PANEL_SPECIFICATION_V1`; `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001` (type is a label, not a coefficient). R2 additionally: Finding object model + Wave B Infer/Evaluate contracts.
- **Proposal:** `00_owner/decisions/PROPOSAL_EPISTEMIC_BASIS_ON_FINDINGS_DRAFT.md`.
- **Status:** R1 presentation **Adopted — DL-093** (amends `FINDING_PRESENTATION_SPECIFICATION_V1` §C/§O→§P + `FINDING_PANEL_SPECIFICATION_V1` §E/§F + glossary label-map). R2 sub-typing + basis-assignment contract remains **Proposed** (deferred phase).

### RB-034 — Onboarding finding-coverage via grounded gap-detection (density without inference)

- **Source Finding:** Owner concern 2026-07-02 — onboarding must show a **material** number of findings even when inputs are sparse, but the orientation currently surfaces few (~6–8) and leans on **inferred** findings. With the DL-093 basis tags visible, an inference-heavy set reads as "OSLO is guessing," undercutting trust. The honest density lever is **grounded gap-detection** (coverage-gap set-difference vs the 8 artifact types × completeness criteria), which scales *up* with sparseness; inference should stay a bounded minority. Demonstrated in the reference prototype (`03-findings`: the DevNorth sample expanded 6→15 findings — 10 grounded / 5 inferred — for the same sparse brief).
- **Affected Layer(s):** Synthesis / understanding contracts (`20_handoff/contracts` — Wave S / Wave B) + Fast-Pass stage spec (`30_engineering/analysis_engine`). Non-doctrinal; **no new epistemic invariant**.
- **Affected Concepts:** Coverage-gap detection; finding grounding (Wave B "anchor each Finding to Attested evidence"); no-silent-gap-filling (Wave S); Fast/Deep (DL-046); cost governance (DL-048); epistemic basis (DL-093); finding-type taxonomy (RB-033); Reliability (Coverage / Evidence availability / Assessability).
- **Proposal Scope:** Ratify an **orientation-coverage rule** — the Fast Pass / Infer runs a **grounded completeness-criteria matrix** (8 artifact types × CAF dimensions × an owner-ratified completeness-criteria set); each unmet criterion is a **grounded** finding (`coverage_gap` / `missing_information` / `ambiguity`), anchored to the expected-artifact framework. Density is an **outcome** of the matrix, never a quota met by fabrication; inference remains explicitly flagged (`basis = inferred`) and a **bounded minority**. All numeric thresholds (criteria set, density floor, grounded:inferred target) **owner-set**; must stay within the DL-048 per-tier budget (graceful degradation → partial coverage deferred to Deep).
- **Dependencies:** `WAVE_S_CONTRACT_PACKAGE_SYNTHESIS_ENGINE` (DL-047); `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING`; `FAST_PASS_STAGE_IO_SPEC`; `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`; DL-093; DL-046; DL-048; RB-033.
- **Proposal:** `00_owner/decisions/PROPOSAL_ONBOARDING_FINDING_COVERAGE_DRAFT.md`.
- **Status:** Proposed — owner to ratify the rule and set thresholds (or defer to Alpha telemetry tuning).

---

### RB-035 — Finding flow simplification (no-Acknowledge lifecycle + single-action resolution)

- **Source Finding:** Owner-directed exploration during the R1 UX refinement pass (PR #116). The `acknowledged` lifecycle state records user sentiment with no effect on the assessment (contrary to "only reanalysis changes the assessment"), and resolution is a multi-step ceremony where OSLO can draft the fix.
- **Affected Layer(s):** `10_product/domain` (`FINDING_SYSTEM_SPECIFICATION_V1 §C` + finding-status enum / State Model §10 / Data Model v1.1) with `10_product/experience` (Finding Panel / Presentation specs) realization.
- **Affected Concepts:** Finding lifecycle states + transitions; acceptance-vs-reanalysis (only reanalysis changes the assessment); resolution flow (select → addressed → update → reanalysis → closed); recommendation/finding coupling.
- **Proposal Scope:** Two separable decisions — **D1:** drop `acknowledged` (lifecycle `open → addressed → closed`); **D2:** single-action "Apply this fix" resolution where OSLO can draft. Both preserve the epistemic invariants (addressed-before-closed; reanalysis-only closure). Confirmed decoupled from the Wave U acceptance model and the Wave C/U contracts.
- **Dependencies:** `FINDING_SYSTEM_SPECIFICATION_V1 §C` (HARD); State/Data Model finding-status enum (HARD); `FINDING_PANEL_SPECIFICATION_V1` / `FINDING_PRESENTATION_SPECIFICATION_V1` (MED); `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1 §3` (CHECK — keys on closed/superseded, not acknowledged); Wave B Infer/Evaluate contract (CHECK). No change to Wave C/U contracts or acceptance code.
- **Proposal:** `00_owner/decisions/PROPOSAL_FINDING_FLOW_SIMPLIFICATION_DRAFT.md`. Exploration artifact: `90_research/design_artifacts/oslo_r1_proposed_findings_lifecycle.html`.
- **Status:** Proposed — owner to ratify D1 and/or D2 (Framework 001A review complete; Decision pending). Realization recommended as Release 2.

---

### RB-036 — "Findings" → "Issues" user-facing label (presentation-only)

- **Source Finding:** Owner-directed R1 UX refinement, 2026-07-07 ("simplify UI labels; users see only 'Issues'; weaknesses read as issues"). The UI exposes three overlapping vocabularies — Findings, Issues, weaknesses — for one underlying signal.
- **Affected Layer(s):** `00_owner` (`CANONICAL_GLOSSARY` Disambiguation Register, DL-087 label table) with `10_product/experience` (`FINDING_PRESENTATION_SPECIFICATION_V1` / `FINDING_PANEL_SPECIFICATION_V1`, IssuePanel/OvlPanel copy) realization.
- **Affected Concepts:** user-facing terminology (Finding vs Issue vs weakness); the 1:1 Issue-per-Finding projection (ISS-01); overlay language (OVL-01). Finding stays the first-class internal object.
- **Proposal Scope:** One decision — adopt "Issues" as the single user-facing label; retire user-facing "Findings"/"weaknesses"; internals unchanged. Mechanism = the ratified **DL-087** user-facing-presentation-label pattern (as for CAF, Fast/Deep Pass). 1:1 finding→issue held for R1; aggregation is a separate future decision.
- **Dependencies:** `CANONICAL_GLOSSARY` Disambiguation Register (HARD — add two label rows); `FINDING_PRESENTATION_SPECIFICATION_V1` / `FINDING_PANEL_SPECIFICATION_V1` (MED); Issue Engine / Finding object / contracts (CHECK — none; presentation-only).
- **Proposal:** `00_owner/decisions/PROPOSAL_FINDINGS_AS_ISSUES_USER_FACING_LABEL_DRAFT.md`. Supporting analysis: `R1_ADDITIONAL_CAPABILITIES_SCOPING_BRIEF` (owner working session, 2026-07-07).
- **Status:** Proposed — owner to ratify (Framework 001A review complete; Decision pending). Recommend pairing with RB-035 (same Issue surface).

---

### RB-037 — Overview surface redesign: confidence-led, low-cognitive-load (presentation-only)

- **Source Finding:** Owner-directed UX refinement, 2026-07-08 (Confidence panel too prose-heavy, competing encodings, unclear focus; green delta reads as "health" — in tension with Visual §1.2).
- **Affected Layer(s):** `10_product/experience` (`PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1`; Confidence presentation; token usage vs `RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1 §1.2`) with `product-design` prototype (v-next) realization.
- **Affected Concepts:** Overview layout; Confidence presentation (focal score + neutral CAF maturity bars + band words + hover detail + Why disclosure); per-dimension CAF band surfacing (CAF-01); color discipline (amber = action/attention, green = good state, neutral maturity ramp). Confidence/CAF models unchanged.
- **Proposal Scope:** One decision — adopt the redesigned Overview (presentation-only); retire the ring gauge, the green "your change moved the read" box, and the persistent Current/From OSLO pills; align Start here / Progress / More to one grammar. Strengthens Visual §1.2 conformance.
- **Dependencies:** `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` (HARD); `VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1 §1.2` (CONFIRM); per-dimension CAF band surfacing (MED, CAF-01 supplies values); prototype Overview (MED); Confidence/CAF models (CHECK — none). **Open (anti-assumption):** canonical CAF band vocabulary must be pinned before build.
- **Proposal:** `00_owner/decisions/PROPOSAL_OVERVIEW_REDESIGN_DRAFT.md`. Visual reference of record: `product-design/oslo_r1_overview_redesign_mockup.html`.
- **Status:** Proposed — owner to ratify (Framework 001A review complete; Decision pending). Uses "Issues" per DL-095 (Start here).

---

### RB-038 — Canonical CAF-dimension maturity band vocabulary (glossary definition)

- **Source Finding:** DL-096 open item (2026-07-08): canon defines CAF and the Confidence bands (Low/Moderate/High) but not a per-dimension band vocabulary; the prototype used ad-hoc `Limited`/`Forming`. Owner selected a ramp 2026-07-09.
- **Affected Layer(s):** `00_owner` (`CANONICAL_GLOSSARY`) with `10_product/domain` (`CAF_ASSESSMENT_MODEL_V1`) and `10_product/experience` (Overview/Confidence presentation) reference.
- **Affected Concepts:** per-dimension CAF band labels (presentation of the CAF-01 assessment); distinct from the Confidence band, Understanding State (AE-04), and MRI states (MRI-03). Maturity ramp per Visual §1.2.
- **Proposal Scope:** One decision — adopt the canonical CAF-dimension maturity ramp **Limited · Forming · Solid · Strong** (low→high). Resolves the DL-096 open item. **Open (anti-assumption):** band→CAF-score thresholds are a separate owner/calibration item, not ratified here.
- **Dependencies:** `CANONICAL_GLOSSARY` (HARD — add the band set); `CAF_ASSESSMENT_MODEL_V1` (MED); Overview/Confidence presentation (MED); CAF scoring/calibration (OPEN — thresholds). Presentation-only; no model/scoring change.
- **Proposal:** `00_owner/decisions/PROPOSAL_CAF_DIMENSION_BAND_VOCABULARY_DRAFT.md`. Realized in `product-design/oslo_r1_experience_mockup_v4.html`.
- **Status:** Ratified as DL-097 (2026-07-09) — **superseded by RB-039 / DL-098** (reconciled to the DL-086 5-band scheme; the 4-band vocabulary retired).

---

### RB-039 — Reconcile CAF-dimension bands to the DL-086 5-band scheme (supersedes RB-038 / DL-097)

- **Source Finding:** 2026-07-09 — DL-097's 4-band CAF-dimension vocabulary (Limited/Forming/Solid/Strong) conflicts with the earlier-ratified **DL-086** scoring scheme, where CAF dimensions compute to 0–100 and the authoritative unit is the **5-band scheme** (Very Low/Low/Moderate/High/Very High). DL-097 was ratified on an incomplete read that missed the scoring formula spec.
- **Affected Layer(s):** `00_owner` (decision — supersede DL-097) with `10_product/experience` + `product-design` (relabel dimensions to the 5-band) and `30_engineering/scoring` (confirm §3 dimension bands).
- **Affected Concepts:** per-dimension CAF band vocabulary; single shared band ramp for Confidence + dimensions; DL-086 scoring formula (unchanged). Closes the DL-097 threshold open item (DL-086 owns the edges).
- **Proposal Scope:** One decision — CAF dimensions use the ratified DL-086 5-band scheme; DL-097's 4-band vocabulary is superseded and retired. No new thresholds; presentation-only.
- **Dependencies:** DL-097 (SUPERSEDE); `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1 §3` (CONFIRM); Overview/Confidence presentation + v4 prototype (relabel); glossary (none — DL-097 entry never added).
- **Proposal:** `00_owner/decisions/PROPOSAL_CAF_DIMENSION_BAND_RECONCILE_DL086_DRAFT.md`.
- **Status:** Proposed — owner to ratify (Framework 001A review complete; Decision pending). Supersedes RB-038 / DL-097.

---

### RB-040 — Reliability qualifier presentation: finalize copy + confirm CONF-06 divergence trigger (DL-099 follow-ups)

- **Source Finding:** 2026-07-10 — DL-099 ratified the single "read-solidity" reliability qualifier (quiet by default; loud only on CONF-06 divergence), but left two items open at ratification: (a) the user-facing qualifier **copy** ("Solid / Partial / Thin read" or similar) is TBD; (b) the Review's **binding condition** — that the "loud" divergence trigger reuses the **existing CONF-06 false-confidence flag** and introduces **no new, separately-tuned threshold** — must be confirmed against the calibration work.
- **Affected Layer(s):** `10_product/experience` (PROJECT_OVERVIEW §S / MRI §T copy) + `product-design` (v4 mockup labels) for the copy; `00_owner` / calibration (`PROPOSAL_CONFIDENCE_INDEX_CALIBRATION_DRAFT`) for the trigger confirmation.
- **Affected Concepts:** reliability qualifier presentation (DL-099); CONF-06 false-confidence divergence; anti-probability-misread copy posture (Interpretation Doctrine).
- **Proposal Scope:** (1) ratify final qualifier copy — presentation-only, no model/threshold change; (2) **confirm** (not create) that the divergence trigger is the existing CONF-06 flag; any genuinely new threshold routes to calibration (Class B), not here. Companion to DL-099 / DL-085.
- **Status:** Proposed — owner-directed 2026-07-10 (exempt from the Proposal-000 backlog restriction per owner direction); awaiting Proposal under Framework 001.

## Governance Notes

1. This backlog is a draft. Entries reflect findings from initial repository review, not ratified governance positions.
2. Promotion of any entry from Proposed to Ratified for Work requires the governance workflow established by RB-002 and the promotion rule established by RB-005.
3. New entries should cite the source finding explicitly. Entries inferred without source citation should not be added.
4. Entries that close existing items must reference them in a Supersedes field.

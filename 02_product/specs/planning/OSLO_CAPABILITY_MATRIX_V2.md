# OSLO Capability Matrix v2

**Document:** OSLO_CAPABILITY_MATRIX_V2.md
**Status:** Release 1 Capability Inventory (derived solely from the Master Spec)
**Source of Truth:** `02_product/specs/OSLO_RELEASE_1_MASTER_SPEC.md` — **exclusive authority**
**Supersedes for planning:** `OSLO_CAPABILITY_MATRIX_V1.md` (not used as an input; not treated as authority)
**Purpose:** Authoritative bridge — Master Spec → Capabilities → Linear Initiatives → Epics → Stories
**Date:** 2026-05-31

> **Provenance.** Every capability below traces to one or more Master Spec sections. No prior capability matrix, architecture baseline, or initiative document was used as an authority. Where the Master Spec is silent, the item is recorded in **§22 Gaps Discovered in the Master Spec** rather than invented.
>
> **Governance.** This is a non-canonical planning artifact (analysis & recommendation). It does not ratify, adopt, or supersede canonical content; the repository owner governs adoption. Canonical terminology is preserved from the Master Spec.

---

## Legend

**Release Scope** — `Alpha` = Release 1 (in scope per §13); `Beta` = explicitly deferred near-term; `Future` = out of Release 1 scope per §13 / future-GA notes.

**Priority** — `Critical` (Minimum Viable Alpha per §19, or a hard Release 1 constraint) · `High` (core Release 1 value, Alpha Phases 2–3) · `Medium` (Alpha Phases 4–6 / supporting) · `Low` (defined but not surfaced / refinement).

**Business Objective (Obj)** — `U` Understanding · `I` Improvement · `S` Sharing & Collaboration · `C` Conversion (§13 Primary Product Objectives) · `F` Foundation/Platform (enabling).

**Primary Objects** (§18) — Usr, WS (Workspace/Account), Proj, Evid (Evidence), Art (Artifact), ArtSec (Artifact Section), CAFst (CAF State), Confst (Confidence State), Find (CAF Finding), Ovl (CAF Overlay), Iss (Issue), Rec (Recommendation), Fix (Suggested Fix), CRR (CAF Review Request), Cmt (Comment), MRI, Shr (Share Link), Chat (OSLO Chat Session), Tel (Telemetry Event).

**Primary Surfaces** (§15) — Onbd (Onboarding/Email), Overview (Project Overview), ArtView (Intent/Context/Scope/Requirements/WBS/Resource/Schedule views), MRIv (MRI View), ChatPanel, CAFbar (Confidence/CAF bar), IssuePanel (Issues & Recs panel), OvlPanel (CAF Overlay panel), Sharing, Settings.

**AC** — Acceptance Criteria reference in Master Spec §16 (Capability 1–14), or `—` if none defined.

---

## Domain Index

| # | Domain | Prefix | Caps |
|---|---|---|---|
| 1 | Project Foundation | PF | 5 |
| 2 | Evidence Ingestion | EI | 4 |
| 3 | Planning Synthesis | PS | 4 |
| 4 | Analysis Engine (Fast Pass / Deep Pass) | AE | 6 |
| 5 | CAF | CAF | 5 |
| 6 | Confidence | CONF | 7 |
| 7 | MRI | MRI | 7 |
| 8 | Issues | ISS | 4 |
| 9 | Recommendations | REC | 5 |
| 10 | CAF Overlays | OVL | 3 |
| 11 | Artifact Workspace | AW | 7 |
| 12 | OSLO Chat | CHAT | 4 |
| 13 | Collaboration | COLLAB | 3 |
| 14 | CAF Review Requests | CRR | 5 |
| 15 | Sharing | SHARE | 5 |
| 16 | Telemetry | TEL | 7 |
| 17 | Monetization | MON | 4 |
| 18 | Security & Compliance | SEC | 7 |
| 19 | Platform Services | PLAT | 6 |

---

## 1. Project Foundation (PF)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PF-01 | Alpha Access & Invitation | Waitlist → invitation email → account activation; private Alpha, no public signup | C/F | Frictionless entry to Alpha | Alpha | Critical | SEC-01 | §15A, §14 F1 | — | Usr, WS | Onbd | N | Users pre-exist in waitlist |
| PF-02 | Project Initiation (multi-path) | Start a project via Upload / Describe / Template / Guided Intake; naming optional ("infer first, ask later") | U/F | Start in seconds, any input | Alpha | Critical | EI-01, EI-03 | §15A, §14 F1 | C1 | Proj, Evid | Onbd, Overview | N | Minimize clicks/forms |
| PF-03 | Project & Workspace Lifecycle | Persistent Project within Workspace/Account; container for all objects | F | Durable project state | Alpha | Critical | PLAT-01, PLAT-06 | §18 | — | Proj, WS, Usr | Overview, Settings | N | One active project on Free tier (see MON-01) |
| PF-04 | Project Overview Surface | Landing surface after Fast Pass / on reopen; combines MRI, Confidence, CAF, top issues/recs, entry points, analysis status, CTA, open CRRs | U | Single orientation view | Alpha | Critical | MRI-01, CONF-01, ISS-01, REC-01 | §15, §7 | — | Proj, MRI, Confst, CAFst | Overview | N | Primary reopen surface |
| PF-05 | Pre-Account Interaction | Begin interacting before account creation (Lovable/Bolt/v0-style) | C | Try before signup | Future | Low | PF-02 | §15A | — | Proj | Onbd | N | Explicit future-GA note; out of Alpha |

---

## 2. Evidence Ingestion (EI)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EI-01 | Artifact Ingestion (multi-format) | Ingest PDF, DOCX, TXT, prompts, meeting transcripts, planning artifacts | U/F | Bring any evidence | Alpha | Critical | — | §15B, §16 C1 | C1 | Evid, Proj | Onbd, ArtView | N | Intent/Context/Planning/Informal evidence types |
| EI-02 | Claim Extraction | Extract goals, outcomes, stakeholders, assumptions, constraints, dependencies from evidence | U | Turns docs into structure | Alpha | Critical | EI-01 | §15B, §16 C1 | C1 | Evid, Find | — | Y | First step before synthesis |
| EI-03 | Intake Paths (Describe/Template/Guided) | Free-form prompt, template start, and guided intake entry methods | U/F | Flexible starting point | Alpha | High | — | §15A, §15B | C1 | Evid, Proj | Onbd | N | Template catalog & guided steps under-specified (see §22) |
| EI-04 | Planning-Maturity-Agnostic Intake | Accept minimal (idea), partial (charter+reqs), or advanced (full plan) maturity | U | Works at any stage | Alpha | High | EI-01, PS-01 | §15B, §16 C1 | C1 | Evid, Art | Onbd | N | No mandatory review/validation gate |

---

## 3. Planning Synthesis (PS)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PS-01 | Planning Synthesis Engine | Construct a usable planning model from incomplete evidence (Evidence Extraction → Context Expansion → Planning Construction → Understanding Evaluation) | U | Plans built for you | Alpha | Critical | EI-02 | §15D, §16 C1 | C1 | Evid, Art, Find | — | Y | "OSLO constructs plans" |
| PS-02 | Planning Artifact Generation | Generate Intent, Context, Scope, Requirements, WBS, Resources, Schedule artifacts; editable | U/I | Structured plan from raw input | Alpha | Critical | PS-01 | §15D, §10, §16 C1 | C1 | Art, ArtSec | ArtView | Y | Generated artifacts trigger CAF eval |
| PS-03 | Understanding Evaluation | Evaluate synthesized model to seed initial CAF/Confidence | U | Knows what it knows | Alpha | Critical | PS-02, CAF-01 | §15D | — | Art, CAFst, Confst | — | Y | 4th synthesis step; feeds confidence |
| PS-04 | Artifact Lifecycle | Track artifact states: Generated → Modified → Reviewed → Validated → Evolving | I | Visible artifact maturity | Alpha | Medium | PS-02 | §15D | — | Art, ArtSec | ArtView | N | State, not analysis |

---

## 4. Analysis Engine — Fast Pass / Deep Pass (AE)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AE-01 | Fast Pass | Deliver Orientation Confidence, initial MRI, top issues, clarifications, suggested fixes, analysis status within ~60s; creates initial working planning model | U | Value in 60 seconds | Alpha | Critical | PS-01, CAF-01, CONF-01, ISS-01, REC-01, MRI-01 | §5, §16 C2 | C2 | Proj, Art, CAFst, Confst, MRI, Iss, Rec | Overview | Y | Core constraint, not an optimization; communicates confidence maturity/reliability |
| AE-02 | Deep Pass (Deep Analysis Pass) | Continuous understanding expansion after the Fast Analysis Pass / 60-Second Orientation. Deep Analysis outputs: **Confidence Recalculation**, **Expanded Findings** (matures/discovers findings), **Expanded Recommendations**; validates alignment/feasibility; evolves MRI. Active Release 1; improves understanding, performs no governance | U/I | Understanding keeps improving after orientation | Alpha | High | AE-01, AE-03 | §6, §16 C3 | C3 | Find, Iss, Rec, Confst, CAFst, MRI | Overview, ArtView | Y | User never waits for it; 60-Second Orientation is not the final analysis state |
| AE-03 | Event-Driven Recompute | Reanalyze only on understanding-relevant events (edits, fixes, chat, imports, collaboration, CRR responses); "no change → no reanalysis" | U/F | Stable, efficient analysis | Alpha | Critical | PLAT-02 | §6, §12 | C3 | Proj, Art | — | N | Integration hub for AW-03, CHAT, COLLAB, CRR |
| AE-04 | Understanding State Model | Classify understanding: Initial → Partial → Refined → Validated → Mature | U | Honest about certainty | Alpha | Medium | PS-03 | §2 | — | Confst, CAFst | Overview, MRIv | Y | Distinct from MRI display states (MRI-03) |
| AE-05 | Progressive Disclosure | Present understanding progressively (Initial → Expanded → Validated); never Unknown→Final Truth | U | No false certainty | Alpha | Medium | AE-02 | §11 | — | MRI, Confst | Overview, MRIv | N | UX principle across surfaces |
| AE-06 | Understanding Debt | Concept for accumulated unresolved ambiguity/assumptions/conflicts | U | Future debt visibility | Future | Low | CAF-05 | §21 | — | Find, Iss | — | N | Defined but explicitly **not surfaced** in Release 1 |

---

## 5. CAF (CAF)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CAF-01 | CAF Engine | Compute Clarity, Alignment, Feasibility — the only first-class confidence dimensions; visible throughout workspace | U | One model behind everything | Alpha | Critical | PS-03 | §4, §16 C5 | C5 | CAFst, Find | CAFbar | Y | Drives Confidence, Issues, Recs, MRI, Overlays |
| CAF-02 | Clarity Analysis | Measure interpretability; contributors: ambiguity, assumptions, inference reliance, missing info, conflict, undefined ownership/success criteria | U | Knows what's unclear | Alpha | Critical | CAF-01 | §4 | C5 | CAFst, Find | CAFbar, OvlPanel | Y | Inference is a Clarity finding type, not a dimension |
| CAF-03 | Alignment Analysis | Measure coherence between elements and intended outcomes; outcome/stakeholder/artifact/execution alignment | U | Are we doing the right thing | Alpha | Critical | CAF-01 | §4 | C5 | CAFst, Find | CAFbar, OvlPanel | Y | Live in Release 1 (not deferred) |
| CAF-04 | Feasibility Analysis | Measure achievability; resource/schedule/dependency/capability/scope realism | U | Can we achieve it | Alpha | Critical | CAF-01 | §4 | C5 | CAFst, Find | CAFbar, OvlPanel | Y | Future inputs (market/regulatory/execution) out of scope |
| CAF-05 | CAF Issue Taxonomy | Map every finding/issue to a CAF dimension and finding type | I | Consistent diagnosis | Alpha | High | CAF-01, ISS-01 | §4, §8 | — | Find, Iss | OvlPanel | Y | Every issue maps to CAF |

---

## 6. Confidence (CONF)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONF-01 | Outcome Confidence Engine | Derive Outcome Confidence from CAF — degree to which understanding is justified by evidence | U | Headline trust signal | Alpha | Critical | CAF-01 | §3, §16 C4 | C4 | Confst, CAFst | CAFbar, Overview | Y | Never exists independently of CAF |
| CONF-02 | Confidence Score & States | Numeric 0–100 plus state band (Very Low / Low / Moderate / High / Very High) | U | Readable at a glance | Alpha | Critical | CONF-01 | §3 | C4 | Confst | CAFbar | N | Exact thresholds may evolve (see §22) |
| CONF-03 | Confidence Explainability | Every confidence value/change is explainable to drivers and findings | U | Trust through transparency | Alpha | Critical | CONF-01, CAF-05 | §3, §16 C4 | C4 | Confst, Find | CAFbar, Overview | Y | Required by AC4 |
| CONF-04 | Confidence History & Trend | Maintain confidence history; show trend over time | U | See progress | Alpha | High | CONF-01, PLAT-01 | §3, §16 C4 | C4 | Confst | Overview, MRIv | N | "Confidence is historical" (§18) |
| CONF-05 | Progressive Confidence Stages | Orientation → Expanded → Validated confidence maturation | U | Confidence matures with evidence | Alpha | Medium | CONF-01, AE-02 | §3 | — | Confst | CAFbar | N | Operational Confidence is future (CONF-07) |
| CONF-06 | False-Confidence Detection | Detect high confidence built on inaccurate understanding (the dangerous 4th state) | U | Guards against illusion | Alpha | Medium | CONF-01, CAF-01 | §3 | — | Confst, Find | Overview | Y | "Should actively attempt to detect" |
| CONF-07 | Operational Confidence | Confidence derived from actual execution reality | U | Execution-grounded confidence | Future | Low | — | §3 | — | Confst | — | Y | Explicitly future execution-oriented releases |

---

## 7. MRI (MRI)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MRI-01 | Project MRI Generation | Continuously evolving representation of OSLO's current understanding of project reality | U | Understand reality fast | Alpha | Critical | CONF-01, CAF-01, ISS-01, REC-01 | §7, §16 C10 | C10 | MRI, Confst, CAFst, Iss, Rec | MRIv, Overview | Y | Signature artifact; always exists |
| MRI-02 | MRI Components | Outcome Confidence, CAF, Understanding State, top drivers/reducers, top issues/opportunities, confidence trend, heatmap, dependencies | U | Whole picture in one view | Alpha | High | MRI-01 | §7, §15C | C10 | MRI | MRIv | N | Assembles computed signals |
| MRI-03 | MRI Understanding States | Interpretation Unstable → Emerging → Actionable → Validated Understanding | U | Knows the MRI's reliability | Alpha | Medium | MRI-01, AE-04 | §7, §5 | — | MRI | MRIv | Y | Interpretation Unstable when clarity very low |
| MRI-04 | Artifact Understanding Heatmap | Per-artifact understanding strength (Intent/Context/Scope/Requirements/Resources/Schedule) | U | Where understanding is weak | Alpha | High | CAF-01 | §15C | C10 | MRI, Art | MRIv | N | Renders from CAF scores |
| MRI-05 | CAF Triangle Visualization | Visualize Clarity/Alignment/Feasibility relationship | U | Intuitive CAF read | Alpha | Medium | CAF-01 | §15C | — | MRI, CAFst | MRIv | N | Recommended Release 1 viz |
| MRI-06 | Understanding Timeline | Lightweight history of understanding events (confidence deltas, criteria defined, issues resolved, reviews) | U | See the journey | Alpha | Medium | CONF-04 | §11, §15C | — | MRI, Confst | MRIv | N | "Lightweight" in Release 1 |
| MRI-07 | Understanding Dependencies | Show where understanding is blocked awaiting stakeholder review | U/S | Knows what's blocking | Alpha | Medium | CRR-05 | §7 | — | MRI, CRR | MRIv | N | e.g., "2 findings awaiting sponsor review" |

---

## 8. Issues (ISS)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ISS-01 | Issue Engine | Generate issues from CAF findings; conditions that reduce confidence | I | See what to fix | Alpha | Critical | CAF-01 | §8, §16 C7 | C7 | Iss, Find | IssuePanel | Y | Issues are user-facing; findings are first-class |
| ISS-02 | Issue Severity | Classify severity: Critical / Moderate / Warning | I | Prioritize attention | Alpha | High | ISS-01 | §8 | C7 | Iss | IssuePanel | Y | Severity taxonomy per §8 |
| ISS-03 | Issue Lifecycle | Track Detected → Validated → Recommended → Addressed → Resolved | I | Follow issue to closure | Alpha | High | ISS-01 | §6, §8 | C7 | Iss | IssuePanel | N | Lifecycle tracked |
| ISS-04 | Issue ↔ Artifact Linkage | Link issues to artifacts; navigate Issue→Artifact and back | I | Jump to the source | Alpha | High | ISS-01, AW-07 | §8, §10 | C7 | Iss, Art, ArtSec | IssuePanel, ArtView | N | Supports artifact-centric navigation |

---

## 9. Recommendations (REC)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REC-01 | Recommendation Engine | Generate recommendations from findings; each states what/why/which CAF dimension improves/expected outcome | I | Clear path to improve | Alpha | Critical | ISS-01, CAF-05 | §8, §16 C8 | C8 | Rec, Find, Iss | IssuePanel | Y | Recommendations exist to improve confidence |
| REC-02 | Recommendation Actions | Accept, Reject, Modify, Discuss, Apply, Share For Review | I | Stay in control | Alpha | High | REC-01 | §8 | C8 | Rec | IssuePanel | N | "OSLO recommends. Users decide." |
| REC-03 | Recommendation Lifecycle | Generated → Presented → Explained → Accepted → Applied → Verified | I | Outcomes verified | Alpha | High | REC-01 | §8, §6 | C8 | Rec | IssuePanel | N | Standardized lifecycle |
| REC-04 | Suggested Fixes | One-step suggested fixes applied to artifacts (gated by daily allowance) | I/C | Fast improvement | Alpha | High | REC-01, MON-02 | §8, §5 | — | Fix, Art | IssuePanel, ArtView | Y | Counts against Free-tier daily fix limit |
| REC-05 | Validation Recommendations | Recommendations that seek stakeholder confirmation (validate expectation, confirm criteria/ownership, review inferred requirement) | I/S | Resolve via stakeholders | Alpha | Medium | REC-01, CRR-01 | §8 | — | Rec, CRR | IssuePanel | Y | Prime candidates for CAF Review Requests |

---

## 10. CAF Overlays (OVL)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OVL-01 | CAF Overlay Engine | Expose CAF findings directly within artifact content; every overlay maps to Clarity/Alignment/Feasibility | I/U | Findings in context | Alpha | Critical | CAF-01, AW-02 | §10, §15D, §16 C6 | C6 | Ovl, Find, Art, ArtSec | OvlPanel, ArtView | Y | Primary artifact intelligence mechanism |
| OVL-02 | CAF Overlay Panel | Panel showing dimension, finding type, explanation, confidence impact, recommendation, related findings | I | Understand each finding | Alpha | High | OVL-01 | §15 | C6 | Ovl, Rec | OvlPanel | N | Updates after Deep Pass |
| OVL-03 | Overlay Actions | Ask OSLO, Resolve, Comment, Dismiss, Share For Review on a finding | I/S | Act in place | Alpha | High | OVL-01, CHAT-01, CRR-01, COLLAB-01 | §15, §15D | C6 | Ovl, Cmt, CRR | OvlPanel | N | Bridges chat, collaboration, review |

---

## 11. Artifact Workspace (AW)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AW-01 | Artifact Workspace | Primary operating environment where reality is created/refined/validated/shared; center of gravity | I/U | Work where it matters | Alpha | Critical | PS-02 | §10 | — | Proj, Art | ArtView | N | Users spend most time here, not dashboards |
| AW-02 | Artifact Views | Per-domain views: Intent, Context, Scope, Requirements, WBS, Resources, Schedule | I/U | Organized plan | Alpha | Critical | AW-01 | §10, §15 | — | Art, ArtSec | ArtView | N | Three domains: Intent / Context / Execution Planning |
| AW-03 | Direct Editing | Edit artifact text directly; OSLO detects change and triggers event-driven reanalysis | I | Edit freely | Alpha | High | AW-02, AE-03 | §10, §14 F6 | — | Art, ArtSec | ArtView | N | Direct edits → Deep Pass |
| AW-04 | Assisted Editing | Invoke OSLO Chat or suggested fix to propose improvements; accept/modify/reject | I | AI helps you write | Alpha | High | AW-02, CHAT-01, REC-04 | §10 | — | Art, Rec, Fix | ArtView, ChatPanel | Y | Two improvement paths with direct editing |
| AW-05 | Persistent Intelligence Layer | Always-visible Outcome Confidence, Clarity, Alignment, Feasibility, Understanding State while editing | U | Context always present | Alpha | High | CONF-01, CAF-01 | §10 | — | Confst, CAFst | CAFbar, ArtView | N | Persistent across artifact views |
| AW-06 | Persistent Issues & Recs Panel | Always-available Critical/Moderate/Warning issues, recommendations, suggested fixes, CRRs | I | Never lose the worklist | Alpha | High | ISS-01, REC-01 | §10 | — | Iss, Rec, Fix, CRR | IssuePanel | N | Persistent panel |
| AW-07 | Artifact-Centric Navigation | Navigate Artifact↔Issue, Recommendation→Artifact, Overlay→Issue, CRR→Artifact | I | Move between context fast | Alpha | High | ISS-04, OVL-01 | §10 | — | Art, Iss, Rec, Ovl, CRR | ArtView, IssuePanel | N | Bidirectional linking |

---

## 12. OSLO Chat (CHAT)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CHAT-01 | OSLO Chat | Project-aware reasoning interface anchored to project context, artifacts, confidence, CAF, issues, recs, CRRs | I | Reason with OSLO | Alpha | High | PS-02, CAF-01 | §9, §16 C9 | C9 | Chat, Proj | ChatPanel | Y | Not a generic chatbot |
| CHAT-02 | Chat Context Inheritance | Inherit context automatically when launched from issue, recommendation, artifact, or CRR | I | No re-explaining | Alpha | High | CHAT-01 | §9 | C9 | Chat, Iss, Rec, Art, CRR | ChatPanel | N | Knows originating object |
| CHAT-03 | Chat Functions | Explain, Clarify, Resolve, Improve | I | Targeted help | Alpha | High | CHAT-01 | §9, §16 C9 | C9 | Chat | ChatPanel | Y | Release 1 chat functions |
| CHAT-04 | Chat-Generated Improvements | Generate artifact improvements from chat; may trigger Deep Pass | I | Turn talk into edits | Alpha | High | CHAT-01, AW-04, AE-03 | §9, §16 C9 | C9 | Chat, Art, Fix | ChatPanel, ArtView | Y | Chat interactions can trigger Deep Pass (AE-03) |

---

## 13. Collaboration (COLLAB)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLLAB-01 | Comments | Comment on artifacts/findings; activity preserved | S | Discuss in context | Alpha | High | AW-02 | §16 C11 | C11 | Cmt, Art, Ovl | ArtView, OvlPanel | N | Comment activity preserved |
| COLLAB-02 | Replies | Threaded replies to comments | S | Real conversation | Alpha | Medium | COLLAB-01 | §16 C11 | C11 | Cmt | ArtView | N | — |
| COLLAB-03 | Mentions | @-mention collaborators | S | Pull people in | Alpha | Medium | COLLAB-01 | §16 C11 | C11 | Cmt, Usr | ArtView | N | Collaboration events may trigger Deep Pass (AE-03) |

---

## 14. CAF Review Requests (CRR)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRR-01 | Review Request Creation | "Share For Review" a CAF finding to a stakeholder | S/I | Get the right input | Alpha | High | OVL-03, REC-05 | §8, §14 F11, §16 C14 | C14 | CRR, Ovl, Find | OvlPanel, IssuePanel | N | Active virality mechanism; **Free-tier with bounded cap (P2); recipient = Reviewer Principal (DL-049)** |
| CRR-02 | Review Package | Package includes finding, context, recommendation, artifact reference | S | Reviewer has full context | Alpha | High | CRR-01 | §16 C14 | C14 | CRR, Find, Rec, Art | Sharing | N | Sent to selected stakeholder |
| CRR-03 | Stakeholder Responses | Reviewer can Comment, Approve, Reject, Suggest Alternative | S | Structured stakeholder input | Alpha | High | CRR-02 | §16 C14 | C14 | CRR, Cmt | Sharing | N | Responses preserved |
| CRR-04 | Response → Deep Pass | Submitted responses become evidence and trigger Deep Pass; confidence/MRI update | U/S | Input improves understanding | Alpha | High | CRR-03, AE-03 | §8, §16 C14 | C14 | CRR, Evid, Confst, MRI | Overview | Y | "Review Requests create evidence" (§18) |
| CRR-05 | Review Status Visibility | Show review status throughout workspace and in MRI | S | Know what's pending | Alpha | Medium | CRR-01, MRI-07 | §7, §16 C14 | C14 | CRR, MRI | Overview, MRIv, IssuePanel | N | Drives Understanding Dependencies |

---

## 15. Sharing (SHARE)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SHARE-01 | Project Sharing | Share a project | S | Bring others in | Alpha | High | SEC-02 | §16 C12 | C12 | Shr, Proj | Sharing | N | — |
| SHARE-02 | MRI Sharing & Links | Share MRI via view sharing, public links, private links | S | Spread understanding | Alpha | High | MRI-01, SEC-02 | §7, §16 C12 | C12 | Shr, MRI | Sharing, MRIv | N | MRI is the passive virality mechanism; **Free-tier (P2); carries attribution+CTA (P1, Virality Audit 001)** |
| SHARE-03 | Artifact Sharing | Share individual artifacts | S | Targeted sharing | Alpha | Medium | SEC-02 | §16 C12 | C12 | Shr, Art | Sharing, ArtView | N | — |
| SHARE-04 | PDF Export | Export MRI/artifacts to PDF | S/C | Portable output | Alpha | Medium | MRI-01 | §7, §13, §16 C12 | C12 | Shr, MRI, Art | Sharing | N | Free tier: PDF export only; **carries attribution+CTA — viral surface (P1, Virality Audit 001)** |
| SHARE-05 | Permission Levels | Permission levels on shared content | S/F | Control access | Alpha | High | SEC-02 | §16 C12 | C12 | Shr | Sharing | N | Levels not enumerated (see §22) |

---

## 16. Telemetry (TEL)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TEL-01 | Telemetry Infrastructure | Capture Telemetry Events across the product | F | Learn what works | Alpha | High | PLAT-01 | §17, §18 | — | Tel | — | N | Optimize for Learning Velocity |
| TEL-02 | User Journey Telemetry | invited, accepted, activated, project created, evidence uploaded, fast_pass_completed, first MRI/artifact/overlay/recommendation viewed | F | Measure activation | Alpha | High | TEL-01 | §17 | — | Tel | — | N | — |
| TEL-03 | Understanding Telemetry | initial/current confidence, delta, initial/current CAF, understanding-state progression | F | Measure understanding | Alpha | High | TEL-01, CONF-01 | §17 | — | Tel, Confst | — | N | — |
| TEL-04 | Improvement Telemetry | issues generated/opened/resolved, recs generated/viewed/accepted/rejected, fixes applied, artifact edits | F | Measure improvement loop | Alpha | High | TEL-01 | §17 | — | Tel, Iss, Rec, Fix | — | N | — |
| TEL-05 | Collaboration Telemetry | comments, replies, mentions, CRRs created/opened/completed, approvals/rejections/alternatives | F | Measure collaboration | Alpha | Medium | TEL-01 | §17 | — | Tel, Cmt, CRR | — | N | — |
| TEL-06 | Virality Telemetry | MRI/artifact/CRR shared, external stakeholder invited/joined/returned/converted | F | Measure virality | Alpha | Medium | TEL-01 | §17 | — | Tel, Shr | — | N | **Computes k = i×c + cycle-time per loop (CRR/MRI/PDF); Internal excluded; targets Calibration §4f (P6, Virality Audit 001)** |
| TEL-07 | Conversion Telemetry | daily fix usage, limits reached (fix/chat/project), upgrade prompt displayed/clicked, upgrade completed | F/C | Measure conversion | Alpha | Medium | TEL-01, MON-04 | §17 | — | Tel | — | N | — |

---

## 17. Monetization (MON)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MON-01 | Free Tier Scope | One active project; full Workspace, Confidence, CAF, MRI, Issues, Recs, Sharing, Comments; limited fixes/chat; PDF export only | C | Real value free | Alpha | High | PF-03 | §13, §16 C13 | C13 | WS, Proj | Settings | N | Maximizes trust creation |
| MON-02 | Daily Fix Allowance & Reset | Daily suggested-fix allowance that resets automatically | C | Habit + re-engagement | Alpha | High | REC-04 | §13, §16 C13 | C13 | Fix, Usr | IssuePanel | N | Drives re-engagement and upgrade |
| MON-03 | Usage Limits | Limit recommendation applications and chat usage on Free tier | C | Clear upgrade reason | Alpha | Medium | CHAT-01, REC-02 | §13 | C13 | WS | Settings | N | Limited chat / limited rec applications |
| MON-04 | Upgrade Prompts | Contextual upgrade prompts when limits are reached | C | Timely upgrade path | Alpha | Medium | MON-02, MON-03 | §13, §16 C13 | C13 | WS, Usr | IssuePanel, Settings | N | Trigger taxonomy + timing defined: `12_freemium_tier_behavior_logic.md` (UP-1…8) · timing config Calibration §4d · UP-4 = Wave E honest-limit disclosure (FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001) |

---

## 18. Security & Compliance (SEC)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEC-01 | Authentication | Email/password, Google SSO, Microsoft SSO | F | Secure sign-in | Alpha | Critical | — | §12, §21 | — | Usr | Onbd, Settings | N | — |
| SEC-02 | Authorization & RBAC | Role-based access control | F | Right access only | Alpha | Critical | SEC-01 | §12, §21 | — | Usr, WS | Settings, Sharing | N | Underlies all sharing/permissions |
| SEC-03 | Data Isolation | Workspace and project access isolation | F | Tenant safety | Alpha | Critical | SEC-02 | §12, §21 | — | WS, Proj | — | N | Workspace data isolation |
| SEC-04 | Encryption | Encryption in transit and at rest | F | Data protected | Alpha | Critical | — | §12, §21 | — | — | — | N | — |
| SEC-05 | Secret Management | Secure secret management | F | Safe credentials | Alpha | High | — | §12, §21 | — | — | — | N | — |
| SEC-06 | Audit Logging | Audit logs + artifact-modification, recommendation-acceptance, review, sharing activity tracking | F | Accountability | Alpha | High | PLAT-01 | §12, §21 | — | WS, Art, Rec, CRR, Shr | Settings | N | Enterprise audit-readiness |
| SEC-07 | Privacy & Compliance Baseline | Privacy protections, SOC 2 readiness, GDPR considerations (Tier 1 & Tier 2 customers) | F | Enterprise trust | Alpha | High | SEC-03, SEC-06 | §12, §21 | — | WS, Usr | Settings | N | Baseline, not full certification |

---

## 19. Platform Services (PLAT)

| ID | Capability | Description | Obj | User Value | Scope | Pri | Deps | Spec §§ | AC | Objects | Surfaces | AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PLAT-01 | State Persistence | Persist Confidence, CAF, MRI, Issue, Recommendation, Understanding, and CRR state | F | Durable understanding | Alpha | Critical | PLAT-06 | §12 | — | Confst, CAFst, MRI, Iss, Rec, CRR | — | N | "OSLO must persist understanding" |
| PLAT-02 | Event-Driven Orchestration | Event-driven recompute orchestration; avoid continuous reprocessing | F | Fresh, efficient analysis | Alpha | Critical | PLAT-01 | §12 | — | Proj | — | N | Powers AE-03 |
| PLAT-03 | Deep Pass Trigger Efficiency | Debounce windows, event consolidation, analysis queues, cooldown, incremental reanalysis | F | No redundant compute | Alpha | High | PLAT-02 | §12 | — | — | — | N | Rapid edits must not re-trigger Deep Pass |
| PLAT-04 | Compute & Token Efficiency | Minimize token consumption, model invocations, context size, redundant AI calls; reuse claims/findings | F | Sustainable AI cost | Alpha | High | PLAT-02 | §12, §21 | — | — | — | N | AI usage must be intentional |
| PLAT-05 | Performance Architecture | Parallelization, async processing, queue-based processing, horizontal scaling, incremental recomputation | F | Responsive at scale | Alpha | High | PLAT-02 | §12, §21 | — | — | — | N | Fast Pass prioritizes responsiveness |
| PLAT-06 | Object & Data Model | Canonical object model: 19 core objects with derived/historical/first-class semantics | F | Coherent data foundation | Alpha | Critical | — | §18 | — | (all) | — | N | Findings first-class; MRI derived; Confidence historical |

---

## 20. Summary Statistics

| Metric | Count |
|---|---|
| **Total capabilities** | **98** |
| Domains | 19 |
| Critical priority | 31 |
| High priority | 44 |
| Medium priority | 20 |
| Low priority | 3 |
| Release Scope: Alpha | 95 |
| Release Scope: Future | 3 |
| AI Required: Yes | 29 |
| AI Required: No | 69 |
| Capabilities with §16 Acceptance Criteria | 52 |
| Capabilities without defined AC | 46 |

**Critical capabilities (31):** PF-01, PF-02, PF-03, PF-04, EI-01, EI-02, PS-01, PS-02, PS-03, AE-01, AE-03, CAF-01, CAF-02, CAF-03, CAF-04, CONF-01, CONF-02, CONF-03, MRI-01, ISS-01, REC-01, OVL-01, AW-01, AW-02, SEC-01, SEC-02, SEC-03, SEC-04, PLAT-01, PLAT-02, PLAT-06.

> Of the 31 Critical capabilities, 4 are security (SEC-01–04) and 3 are platform substrate (PLAT-01, PLAT-02, PLAT-06); the remaining 24 are the product/user-facing core. Security and platform substrate have the widest fan-in (see §21) and should land earliest despite not being user-visible.

**Minimum Viable Alpha chain (§19):** EI-01/EI-02 → PS-01/PS-02 → AW-01/AW-02 → CAF-01 → CONF-01 → AE-01 → OVL-01 → ISS-01 → REC-01. These nine capability clusters are the non-negotiable Release 1 spine.

---

## 21. Capability Dependency Observations

1. **CAF-01 is the central hub.** Confidence (CONF-01), Issues (ISS-01), Recommendations (REC-01), MRI (MRI-01), and CAF Overlays (OVL-01) all depend on the CAF Engine. CAF-01 is the single highest-leverage capability; a slip here cascades to every value surface.
2. **Two upstream gates feed everything:** Evidence Ingestion (EI) and Planning Synthesis (PS) precede all analysis. No CAF/Confidence/MRI value exists until PS-02 produces editable planning artifacts.
3. **AE-03 (Event-Driven Recompute) is the integration spine.** Direct editing (AW-03), assisted/chat edits (CHAT-04), collaboration (COLLAB-03), and CRR responses (CRR-04) all converge on AE-03 to trigger Deep Pass. It is the most cross-referenced non-CAF capability and should be designed as a shared service, not per-feature.
4. **MRI is purely derived.** MRI-01 consumes Confidence, CAF, Issues, Recommendations, and CRR status; it produces no primary data. It cannot be built or tested before its upstream signals exist.
5. **The improvement loop is genuinely circular.** Deep Pass (AE-02) updates Confidence/CAF/Issues/Recs/MRI → user acts (REC-02 / AW-03 / CHAT) → AE-03 re-triggers Deep Pass. Sequencing must account for the loop, not a linear pipeline.
6. **CRR is the collaboration↔understanding bridge.** CAF Review Requests turn stakeholder input into evidence (CRR-04 → AE-03), making collaboration a confidence-moving capability rather than a side channel. CRR-04 is the only collaboration capability that requires AI.
7. **Monetization gates a core action.** REC-04 (Suggested Fixes) depends on MON-02 (Daily Fix Allowance); the primary improvement action and the primary conversion lever are the same mechanic. Treat fixes and fix-limits as one design.
8. **Security and Platform are universal substrate.** SEC-02 underlies every Sharing capability; PLAT-01 underlies all persisted state and Telemetry. These have the widest fan-in and should land early despite not being user-visible.
9. **Telemetry fans in from everything.** TEL-02–07 depend on user-facing capabilities emitting events; instrument as capabilities are built, not retrofitted, or §20 success metrics cannot be measured.

---

## 22. Gaps Discovered in the Master Spec

Items the Master Spec references or implies but does not specify. Recorded for governance — **not resolved here** (per CLAUDE.md governance discipline, no new doctrine/proposals are introduced).

1. **CAF scoring methodology is unspecified.** How Clarity/Alignment/Feasibility are computed to 0–100, and how Confidence aggregates from the three dimensions, is not defined (§3, §4). The headline number has no stated formula.
2. **Confidence band thresholds are provisional.** §3 gives example ranges and states "exact thresholds may evolve." No canonical thresholds exist.
3. **Templates are referenced but undefined.** "Start From Template" (§15A/§15B) has no template catalog, schema, or count.
4. **Guided Intake steps are unspecified.** The guided path is named (§15A/§15B) without a defined question flow.
5. **No Notification object or surface.** CAF Review Requests, comments, and mentions all imply notifying users/stakeholders, but §18's object model has no Notification object and §15 has no notification surface. How a reviewer learns a request is waiting is undefined.
6. **External reviewer identity/auth — RESOLVED (DL-049, 2026-06-05).** ~~undefined~~ → a single **`Principal`** identity object with **`type: reviewer | user`** (email-verified Reviewer scoped to shared items; in-place `reviewer→user` promotion, provenance-stable, scope-preserving). See Runtime Object Model DL-049 Object Additions. *(Link security / scoping — #339 below — routes to the commodity recipient-experience spec; recipient experience R1-vs-fast-follow is an open owner scope call.)*
7. **Sharing permission levels are not enumerated.** §16 C12 requires "permission levels supported" without listing them.
8. **Share-link security is unspecified.** Public/private MRI links (§7) have no stated expiry, revocation, or access-scoping rules.
9. **Concurrency/multi-user edit conflicts are unaddressed.** Collaboration (§16 C11) and direct editing (§10) imply simultaneous editing, but no conflict-resolution or locking model is described.
10. **Paid tiers beyond Free are undefined.** §13 details the Free tier and §12/§21 reference "Tier 1 and Tier 2 customers," but no paid-tier capability matrix, "Tier limits" definition, or upgrade target is specified.
11. **Acceptance Criteria coverage is partial.** §16 defines AC for 14 capabilities; Telemetry (§17), Security (§12/§21), Platform (§12), and several MRI/Confidence sub-capabilities have no AC. 39 of 97 capabilities here carry no AC reference.
12. **Object lifecycle/retention is undefined.** §18 lists objects but no deletion, archival, or retention policy — relevant to GDPR considerations in §21.
13. **"Supported project sizes" for the 60-second Fast Pass constraint is undefined** (§5, §16 C2), leaving the core performance promise unbounded.
14. **Understanding Debt is defined but deliberately not surfaced** (§21) — recorded as AE-06 (Future); no Release 1 representation.
15. **Confidence ↔ probability boundary is asserted but not operationalized.** §3/§21 repeatedly state confidence is not a probability, but give no guidance preventing users/UI from reading the 0–100 score as one.

---

*Capability Matrix v2 complete. Derived exclusively from OSLO_RELEASE_1_MASTER_SPEC.md. Intended as the Master Spec → Capability → Linear Initiative → Epic → Story bridge. Subject to governance review before adoption.*

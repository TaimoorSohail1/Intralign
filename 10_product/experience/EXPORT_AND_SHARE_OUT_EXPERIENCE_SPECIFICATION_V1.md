# Export & Share-Out Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Construct type:** **Secondary Project-Context Surface / Share-Out Surface** — mapped to the ratified taxonomy as a **lightweight Companion-Surface-class action/affordance** (packages existing understanding + routes; hosts no structured understanding-actions; not a primary destination/Workspace/reporting engine) (§D).
**Consistent with and subordinate to (authoritative — must not redefine):** `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `FINDING_PANEL_SPECIFICATION_V1.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md` · `OSLO_CHAT_AND_CLARIFICATION_EXPERIENCE_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · Release 1 Tier Definitions · CAF Assessment · Reliability v2 · Confidence v2.

> **Non-negotiable constraints.** UX / interaction model only. The experience **computes nothing, generates no new assessment, generates no new findings or recommendations, governs nothing, executes nothing, and changes no assessment.** It must **NOT** define: APIs, events, implementation, styling, delivery infrastructure, or document-generation logic. **Only reanalysis changes assessment.** Artifacts remain the source of truth, Findings descriptive, Recommendations advisory, and **Outcome Confidence remains trust in understanding — never project health, readiness, or outcome probability.**

> **Position in the architecture.** Export & Share-Out lets users **package and share existing project understanding outside OSLO** — a snapshot of what OSLO already understands — **without** becoming governance, approvals, execution workflows, external-collaboration workflows, a reporting engine, or an assessment change. It **packages**; it never **produces** new understanding.

---

## A. Purpose

Define the canonical Release 1 **Export & Share-Out Experience**. It answers:

> **"How do users package and share project understanding outside OSLO?"**

It lets users assemble a **snapshot of existing understanding** (confidence, CAF, findings, recommendations, artifact references) into a shareable package or view-only link for outside review — packaging only, never generating, computing, governing, or changing assessment.

## B. Scope

**In scope:** the export/share-out **action and its lightweight configuration**; what can be exported; supported formats; the export **package structure** (visible content); stale-analysis handling; the **shareable-link** experience (UX); relationships to Collaboration, History, and Tiers; empty states; failure states; progressive disclosure; integrity rules; conformance.

**Out of scope:** APIs; events; implementation; styling; **delivery infrastructure** (how a file/link is transmitted/stored); **document-generation logic** (how a PDF is rendered); governance; approvals; execution; external-collaboration workflows; reporting engines; assessment/finding/recommendation **generation**; **billing/payment/entitlement implementation** (tier gating is *presented*, not enforced here); **access/permission enforcement** for links. The experience **packages existing understanding and routes**; it produces no new understanding and changes nothing.

## C. Export Philosophy

Export exists to let understanding **travel** — to put a faithful, honestly-labeled snapshot of what OSLO understands in front of people outside OSLO — **without** turning that snapshot into a report card, an approval, or a governance artifact. It **packages existing presented understanding**; it computes/generates nothing new. It keeps **understanding the center of gravity** and the doctrine intact: confidence is **trust in understanding** (never project health/readiness/probability), stale is **previous analysis** (never current), and **only reanalysis changes assessment**. Every package carries an explicit **disclaimer** that it presents understanding, not project health or approval.

## D. Construct Classification

Per the ratified governing taxonomy (`UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`), Export & Share-Out is a **lightweight Companion-Surface-class action/affordance** (the visibility + routing family), in a **share-out** variant — **not** a new construct type and **not** a Workspace:

| Attribute | Classification |
|---|---|
| **Type** | **Companion-Surface-class** action/affordance — a lightweight export/share-out action available from relevant surfaces, optionally opening a thin configuration panel. |
| **Purpose** | **package** existing understanding for outside review and **share** it (file/copy/link). |
| **Navigation** | invoked **from relevant surfaces** (Overview/MRI/Artifact/Finding Panel/Recommendation Panel/Companion); **not a primary destination/Workspace**. |
| **Context** | reads existing presented understanding (read-only); scopes to the source context. |
| **Independent?** | No — an action over existing surfaces. |
| **Destination?** | **No** (not a reporting workspace). |
| **Hosts actions?** | a **single packaging/share action** + lightweight selection; **no** understanding-changing actions (no accept/resolve/edit/approve/reanalyze). |
| **Contains?** | routes/produces a package; **does not contain** Workspaces/Panels. |
| **Not** | not a Workspace, not a Panel, not Chat, not an Understanding Object, **not a reporting engine / governance publication / approval workflow / audit log**. |

This binds the spec: anything that makes Export a reporting workspace, a governance/approval publication, an assessment-changer, or a content generator is **out of type** and forbidden (§R/§S).

## E. Owner-Level Decisions — Resolutions (Q1–Q13)

### Q1 — What is Export & Share-Out?
**Resolution: Option B — a lightweight action available from relevant surfaces** (optionally opening a thin configuration panel to pick scope/format). Not a project-level secondary *surface* as a destination (A — it's an action, not a place), **not** a full reporting workspace (C — Workspace inflation, forbidden), **not** a governance-ready publication workflow (D — excluded). Best Release 1 model: **B (lightweight action), Companion-Surface-class (§D).**

### Q2 — What can be exported in Release 1?
| Candidate | Classification |
|---|---|
| Full project understanding summary | **Release 1** |
| Project Overview snapshot | **Release 1** |
| MRI weakness-map summary | **Release 1** (qualitative summary; no scores) |
| Artifact content | **Release 1** |
| Artifact with CAF overlays | **Release 1** (overlay *summary*; high-fidelity visual overlay rendering deferred) |
| Findings list / finding summaries | **Release 1** |
| Recommendation summaries | **Release 1** |
| Selected finding package | **Release 1** |
| Selected recommendation package | **Release 1** (with its associated finding context) |
| History / timeline excerpt | **Deferred** (fast-follow) |
| Comments / discussion | **Deferred / opt-in** (stays in Collaboration unless explicitly included; explicit inclusion deferred) |
| Raw artifacts | **Release 1** |

All Release 1 exportables are **packagings of existing presented understanding** — no new content/assessment is generated.

### Q3 — What formats are supported?
**Resolution (Release 1):** **PDF**, **copyable summary** (text), and **shareable link** (view-only). **Deferred:** CSV, DOCX, image export, external-tool sync. *(PDF and which formats are available may be **tier-gated** per Release 1 Tier Definitions — §N; document-generation/rendering mechanics are out of scope, §T.)*

### Q4 — What does an exported/share-out package contain?
**Resolution (visible structure only — no document-generation implementation):** **project name · export/share timestamp · source context · analysis-currency marker (current / previous analysis / stale) · reliability-qualified confidence summary · CAF summary · selected findings · selected recommendations · artifact references or included artifact content · disclaimer** that the export **presents understanding, not project health or approval** (§I).

### Q5 — How is stale analysis handled?
**Resolution.** **Stale exports are allowed but must be clearly labeled "previous analysis"**; export **never refreshes assessment** and **never triggers reanalysis**; the user is **warned before exporting stale understanding** (and the package carries the stale marker). Stale is **never presented as current** (§J).

### Q6 — Does export change assessment or history?
**Resolution.** **Exporting changes no assessment**, **creates no finding/recommendation**, and **does not close the stale state.** Export **may appear as a history reference if History already retains such activity** — but this spec **does not define event/log infrastructure or export retention** (§M).

### Q7 — How does shareable link work?
**Resolution (UX only).** A **view-only link** to a **project-level or context-specific** snapshot that **routes to the OSLO context** (a read-only presentation of the packaged understanding). The link **does not create external-collaboration governance**, and **link access/permission enforcement is out of scope** (§K, §T).

### Q8 — Relationship to Collaboration & Sharing
**Resolution.** **Collaboration sharing gives people access inside OSLO**; **Export/share-out packages understanding for outside review.** **Comments remain in Collaboration** unless explicitly included (deferred, Q2); **export creates no comments**; **export does not notify collaborators** (§L).

### Q9 — Relationship to History
**Resolution.** An export **can reference the analysis state it came from**; **prior exports may be discoverable only if History already retains them**; this spec **does not define audit logs or export-retention policy** (§M).

### Q10 — Relationship to tiers
**Resolution (UX only).** **Free tier may export PDF only if Release 1 Tier Definitions say so**; **paid tiers may unlock additional formats/share-out options if tiers define them.** This spec **presents tier gating** but **defines no billing, payment, or entitlement implementation** (§N).

### Q11 — Empty states
**Resolution.** Distinguish: nothing exportable · not yet analyzed · no findings · no recommendations · unavailable (§O).

### Q12 — Failure states
**Resolution.** Define: export unavailable · package generation failed · link unavailable · stale-source warning · target context unavailable · no access; honest retry/return; no fabrication (§P).

### Q13 — Deferred items
**Resolution.** Compliance-grade reports · executive report builder · custom report templates · scheduled exports · external-tool sync · email delivery · signed/approved publications · audit-certified export logs · API-based export · detailed document-generation logic · branding/styling controls (§T).

## F. Surface / Action Architecture

A **lightweight share-out action** invoked from relevant surfaces, optionally opening a thin configuration panel:

```text
Relevant surface (Project Overview / MRI / Artifact Workspace / Finding Panel /
                  Recommendation Panel / Understanding Companion)
   └─ "Export / Share" action
        ▼
   Thin configuration (lightweight, optional)
     • scope (what to include — §G, pre-scoped by source context)
     • format (PDF / copyable summary / shareable link — §H, tier-aware §N)
     • currency marker (current / previous analysis / stale — §J)
        ▼
   Package (snapshot of existing understanding — §I)  or  view-only link (§K)
```

- **Action, not a destination** — invoked in context; pre-scoped by the surface it's launched from; **not** a reporting workspace (§D).
- **Packages existing understanding** — assembles a snapshot of what is already presented; it **computes/generates nothing** and **changes nothing**.
- Hosts **only** the packaging/share action + lightweight selection — **no** understanding-changing affordances.

## G. Exportable Content

The Release 1 exportables (§E Q2) are **packagings of existing presented understanding**, pre-scoped by source context:
- **From Project Overview** → full project understanding summary / overview snapshot.
- **From MRI** → weakness-map summary (qualitative).
- **From Artifact Workspace** → artifact content (raw) / artifact-with-overlay summary.
- **From Finding Panel** → selected finding package (explanation, evidence refs, CAF impact — descriptive).
- **From Recommendation Panel** → selected recommendation package (with associated finding; advisory; OSLO Recommended / Possible Resolution Paths / Selected Path presentation-only).
- **Aggregate** → findings list / recommendation summaries.
No exportable introduces a new object, score, or generated content; history-excerpt and comments are **deferred/opt-in** (Q2).

## H. Supported Formats

- **PDF** — a packaged snapshot (rendering mechanics out of scope, §T).
- **Copyable summary** — plain text the user can paste elsewhere.
- **Shareable link** — view-only route into the OSLO snapshot (§K).
- **Deferred:** CSV, DOCX, image export, external-tool sync.
Format availability may be **tier-gated** (§N). Formats **package** existing understanding; none generates new content or assessment.

## I. Export Package Structure

Every package presents exactly (visible structure only): **project name · export/share timestamp · source context · analysis-currency marker (current / previous analysis / stale) · reliability-qualified confidence summary (never bare) · CAF summary (qualitative) · selected findings (descriptive) · selected recommendations (advisory; presentation-only constructs) · artifact references or included artifact content · disclaimer.**

**Required disclaimer (always present):** the export **presents OSLO's understanding** — *what OSLO understands and where it is weak, reliability-qualified* — and **not project health, readiness, outcome probability, approval, or certification.** No document-generation implementation is defined here.

## J. Stale-Analysis Handling

- **Stale exports are allowed**, but the package and the share action **clearly label** the content as **"previous analysis"** (analysis-currency marker, §I).
- Export **never refreshes assessment** and **never triggers reanalysis**; it **does not close** the stale state (Q6).
- The user is **warned before exporting stale understanding** (a stale-source warning, §P), and the package never presents stale as current.
- Consistent with the editing workflow / Orientation State Model / History / Awareness stale doctrine.

## K. Shareable Link Experience

- A **view-only** link to a **project-level or context-specific** snapshot that **routes to the OSLO context** (read-only presentation of the packaged understanding).
- The link **creates no external-collaboration governance**, no comments, and no notifications.
- **Link access/permission enforcement is out of scope** (§T) — this spec defines the UX (view-only, routes to context, honestly labeled, stale-marked), not the access mechanism.

## L. Relationship to Collaboration & Sharing

- **Collaboration sharing** grants people access **inside** OSLO (participants, comments, in-context discussion); **Export/share-out** packages understanding for **outside** review.
- **Comments remain in Collaboration** unless explicitly included (deferred, Q2); **export creates no comments** and **does not notify collaborators** (notifications are the Awareness surface's domain; export triggers none).
- Distinct surfaces, distinct purposes; export never becomes collaboration or governance.

## M. Relationship to History & Timeline

- An export **can reference the analysis state it came from** (the currency marker ties the package to its analysis).
- **Prior exports may be discoverable only if History already retains such activity** (subordinate to `HISTORY_AND_TIMELINE_SURFACE_…`); this spec **defines no audit log, export retention policy, or event/log infrastructure**.
- Export **mutates no history**; if surfaced in History, it appears as a reference (append-only presentation, owned by History).

## N. Tier Visibility & Limits

- The experience **presents tier gating** per Release 1 Tier Definitions — e.g., **Free tier PDF-only** (if tiers say so); **paid tiers** may unlock additional formats/share-out options (if tiers define them).
- Tier limits are shown as **plan information** (visibility-first, consistent with Settings/Dashboard) — **no billing, payment, or entitlement implementation** is defined here.
- When a format is tier-locked, the experience presents it as **unavailable on the current plan** (honest, non-blocking to the rest of export), never fabricating access.

## O. Empty States

- **Nothing exportable** — neutral "nothing to export here" for the current scope.
- **Not yet analyzed** — exporting understanding requires analysis; show the not-yet-analyzed state (per Orientation State Model), distinct from "nothing exportable."
- **No findings** — a package may still export (overview/artifact) but notes "no findings," not an empty/failed shell.
- **No recommendations** — similarly noted, not fabricated.
- **Unavailable** — export temporarily unavailable (§P), distinct from "nothing exportable."

## P. Failure States

- **Export unavailable** — "export unavailable — retry"; the rest of the app remains usable; fabricate nothing.
- **Package generation failed** — reported honestly; no partial/corrupt package presented as complete; offer retry; *(generation mechanics out of scope — this is the UX of failure).*
- **Link unavailable** — the share link can't be produced/opened → "unavailable — retry/return"; no fabricated link/content.
- **Stale-source warning** — before exporting stale understanding, warn and label previous analysis (§J).
- **Target context unavailable** — if the source context can't be read, say so; never fabricate content.
- **No access** — if the user/plan can't export (tier-locked or access removed), present plainly; no fabricated access.
- **General principle:** honest, recoverable, non-fabricating; export never invents understanding, content, or access.

## Q. Progressive Disclosure

- **Always available (in context):** the lightweight **Export / Share** action on relevant surfaces.
- **One interaction away:** the thin configuration (scope · format · currency marker), tier-aware.
- **Result:** the package (PDF / copyable summary) or the view-only link.
- **Intentionally absent:** reporting-workspace/report-builder UI; governance/approval/publication affordances; assessment-changing or reanalysis-triggering controls; scores/percentages or any "project health/readiness/probability" framing; document-generation/styling controls; delivery configuration; access-enforcement controls.

## R. Integrity Rules

- **EX-1.** The experience **computes nothing** (no scoring/CAF/Reliability/Confidence).
- **EX-2.** The experience **generates no new assessment, findings, or recommendations** — it **packages existing presented understanding** only.
- **EX-3.** The experience **governs nothing, executes nothing, automates nothing** — not approval, publication governance, or external-collaboration workflow.
- **EX-4.** **Exporting changes no assessment**, **closes no stale state**, **triggers no reanalysis**; **only reanalysis changes assessment.**
- **EX-5.** Findings remain **descriptive**; Recommendations remain **advisory** (OSLO Recommended / Possible Resolution Paths / Selected Path presentation-only); a selected-recommendation package carries its **associated finding** context.
- **EX-6.** **Outcome Confidence is trust in understanding** — **never** project health, readiness, or outcome probability; every package carries the **disclaimer** (§I).
- **EX-7.** **Stale exports are labeled "previous analysis," never presented as current**; the user is warned before exporting stale.
- **EX-8.** **Shareable links are view-only**, route to OSLO context, create no governance/comments/notifications; **access enforcement is out of scope.**
- **EX-9.** **Export creates no comments and does not notify collaborators**; comments stay in Collaboration unless explicitly included (deferred).
- **EX-10.** Export **references** (does not define/own) History; it **mutates no history** and defines no audit log/retention.
- **EX-11.** Tier gating is **presented** (visibility-first); **no billing/payment/entitlement implementation**.
- **EX-12.** The experience is a **lightweight Companion-Surface-class action**, **not a Workspace/reporting engine/destination/governance publication**, and hosts **no understanding-changing actions**.
- **EX-13.** **No** APIs, events, implementation, styling, delivery infrastructure, or document-generation logic defined here; no existing model redefined; nothing fabricated.

## S. Conformance Requirements

A conforming Export & Share-Out experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **EX-C1.** Be a **lightweight action** invoked from relevant surfaces (optionally a thin config panel), **not a reporting workspace/destination** (§D, §F; EX-12). **Fail** if it becomes a reporting workspace or a primary destination.
- **EX-C2.** **Package existing presented understanding** only — generate **no** new assessment/finding/recommendation/content (§G; EX-2). **Fail** if export generates a finding/recommendation/assessment or new content.
- **EX-C3.** Produce a package with the §I structure including the **analysis-currency marker** and the **disclaimer** (understanding, not project health/approval) (§I; EX-6). **Fail** if confidence is framed as project health/readiness/probability or a score, or the disclaimer is omitted.
- **EX-C4.** Allow **stale export only when labeled "previous analysis,"** warn before exporting stale, and **never** refresh/trigger reanalysis or present stale as current (§J; EX-7/EX-4). **Fail** if stale is presented as current or export triggers reanalysis.
- **EX-C5.** Ensure **export changes no assessment, closes no stale state, creates no finding/recommendation** (§E Q6; EX-4). **Fail** if any export action changes assessment or closes stale.
- **EX-C6.** Make **shareable links view-only**, routing to OSLO context, creating no governance/comments/notifications; access enforcement out of scope (§K; EX-8). **Fail** if a link creates external governance or hosts editing.
- **EX-C7.** Keep **export distinct from Collaboration** — no comments created, no collaborator notifications (§L; EX-9). **Fail** if export creates comments or notifies collaborators.
- **EX-C8.** **Reference** (not define/mutate) History; define no audit log/retention/event infrastructure (§M; EX-10). **Fail** if export mutates history or defines audit/retention/event logic.
- **EX-C9.** **Present** tier gating (visibility-first) with **no** billing/payment/entitlement implementation (§N; EX-11). **Fail** if billing/entitlement implementation is defined.
- **EX-C10.** Implement empty states (nothing exportable / not yet analyzed / no findings / no recommendations / unavailable) and honest failure states (export/package/link unavailable / stale-source warning / target unavailable / no access) that fabricate nothing (§O, §P).
- **EX-C11.** Define **no** APIs, events, implementation, styling, delivery infrastructure, or document-generation logic (EX-13; §T). **Fail** if any is defined.

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if it: generates a new finding/recommendation/assessment or any new understanding content; changes any assessment, closes a stale state, or triggers reanalysis; frames confidence as project health/readiness/outcome-probability or a score, or omits the disclaimer; presents stale understanding as current or exports stale without a warning/label; makes a shareable link anything but view-only or creates external-collaboration governance; creates comments or notifies collaborators; mutates history or defines audit logs/retention/event infrastructure; defines billing/payment/entitlement implementation; becomes a reporting workspace/destination/governance publication or hosts understanding-changing actions; fabricates content/understanding/access on empty/failure; or defines APIs, events, implementation, styling, delivery infrastructure, or document-generation logic.

## T. Deferred Items

Explicitly **deferred / out of scope:** compliance-grade reports; executive report builder; custom report templates; scheduled exports; external-tool sync; email delivery; signed/approved publications; audit-certified export logs; API-based export; detailed document-generation logic; branding/styling controls; CSV/DOCX/image formats; history/timeline excerpt and comments/discussion inclusion (Q2 deferred/opt-in); high-fidelity CAF-overlay visual rendering; link access/permission **enforcement** (UX defined, enforcement deferred); billing/payment/entitlement implementation; delivery/retention infrastructure; mobile-specific export behavior; implementation; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Export & Share-Out Experience — a lightweight, Companion-Surface-class action invoked from relevant surfaces that answers "How do users package and share project understanding outside OSLO?" It packages existing presented understanding (full/overview summary, MRI weakness-map summary, artifact content/overlay summary, findings, recommendation summaries, selected finding/recommendation packages, raw artifacts) into PDF, a copyable summary, or a view-only shareable link; each package presents project name, timestamp, source context, an analysis-currency marker (current/previous/stale), a reliability-qualified confidence summary, a qualitative CAF summary, selected findings and recommendations, artifact references/content, and a required disclaimer that it presents understanding — not project health, readiness, outcome probability, approval, or certification. It generates no new assessment/findings/recommendations and changes nothing: stale exports are allowed only when labeled previous analysis (with a pre-export warning) and never refresh or trigger reanalysis; export creates no comments and notifies no collaborators; it references History without mutating it or defining audit logs; and it presents tier gating without billing/entitlement implementation. Shareable links are view-only, route to OSLO context, and create no external governance (access enforcement out of scope). It is UX/interaction only and defines no APIs, events, implementation, styling, delivery infrastructure, or document-generation logic. Outcome Confidence remains trust in understanding; only reanalysis changes assessment.*

**Export & Share-Out Experience Specification v1 complete.**

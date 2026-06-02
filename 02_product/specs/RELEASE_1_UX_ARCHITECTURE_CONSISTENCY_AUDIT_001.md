# Release 1 UX Architecture Consistency Audit 001

**Document Type:** Architecture Consistency Audit · **Status:** Draft · **Date:** 2026-05-31
**Mode:** **Evaluate only.** This audit modifies no specification, introduces no object, resolves no owner-level decision, and creates no new UX scope. It identifies conflicts, duplications, gaps, and risks across the Release 1 UX stack.

> ## ✅ Resolution update (2026-05-31) — UX-C1 / UX-C2 RESOLVED
> The headline conflict **UX-C1** (Finding/Recommendation as Panels vs. standalone Workspaces) and its follow-on **UX-C2** (title/status drift) are **RESOLVED** by owner-ratified `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` (**Option A — Panel Model**). Applied: `FINDING_PANEL_SPECIFICATION_V1.md` and `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` created; `FINDING_WORKSPACE_SPECIFICATION_V1.md` and `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` superseded/repositioned (banners, retained); Workspace→Panel references normalized across active UX docs. The body below is retained as the historical record that surfaced the conflict; per this resolution, the Release 1 UX architecture is now **Ready** on the surface-model axis (residual: older UI-layer docs noted in §N/§O hygiene).

> **Method.** Findings are grounded in the current file state of `02_product/specs/` (presence, titles, status banners, and targeted term checks). Where a conflict requires owner judgment, it is flagged **Owner decision required** and presented as a recommendation, not a resolution.

---

## Documents Audited (presence confirmed)

Present and in scope: `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `ORIENTATION_STATE_MODEL_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_EXPERIENCE_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_DASHBOARD_AND_PROJECT_LIST_EXPERIENCE_SPECIFICATION_V1.md` · `FINDING_PRESENTATION_SPECIFICATION_V1.md` · `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · `FINDING_WORKSPACE_SPECIFICATION_V1.md` · `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` · `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md` · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md`.

**Referenced but NOT present:** `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` — **does not exist.** Its absence is the root of the audit's headline conflict (Area C / UX-C1).

---

## A. Overall UX Architecture

**Verdict: Substantially coherent, with one structural conflict at the Finding/Recommendation step.**

The canonical flow — New User → Workspace Home → Project Creation → Project Ingestion → 60-Second Orientation → Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel → Reanalysis → Updated Understanding — is **supported end-to-end** by the stack:

- Onboarding defines New User → … → 60-Second Orientation → Project Overview.
- Global Navigation defines the lifecycle 60-Second Orientation → Overview → MRI → Artifact → Finding Panel → Recommendation Panel (reinforced, not enforced).
- MRI Workspace and Artifact Workspace define the discovery→content chain; the Artifact editing workflow defines edit→save→pending→reanalysis→updated understanding.

**The one break:** the flow's "Finding Panel → Recommendation Panel" steps are named as **Panels**, but two **Active Release 1** documents (`FINDING_WORKSPACE_SPECIFICATION_V1.md`, `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md`) define them as standalone **Workspaces**. The flow is coherent in intent; the surface terminology is not yet reconciled (see Area C).

---

## B. Primary Workspace Consistency

**Verdict: Consistent.** The primary surfaces are uniformly: **Workspace Home / Project List**, **Project Overview**, **MRI Workspace**, **Artifact Workspace**.

- Global Navigation §G designates Overview / MRI / Artifact as **primary** project destinations and Collaboration / History as **secondary** — matched by Project Dashboard (Workspace Home as landing) and MRI/Artifact specs.
- **No document contradicts** the four-primary set. The Finding/Recommendation **Workspace** specs do not claim to be among the four primaries, but their "Workspace" framing implies standalone destinations, which is in tension with the panel model (Area C) rather than with the primary set itself.

---

## C. Panel vs Workspace Consistency  ⚠ **HEADLINE CONFLICT**

**Verdict: Inconsistent — unresolved surface conflict.**

- The newer stack consistently treats Findings and Recommendations as **first-class model objects surfaced through contextual Panels**, explicitly **not** standalone destinations:
  - `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` §D: Findings/Recommendations "surfaced through contextual Finding Panels … rather than a dedicated Finding Workspace" / "… Recommendation Panels rather than a dedicated Recommendation Workspace."
  - `MRI_WORKSPACE_SPECIFICATION_V1.md` §4, `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` §J (NAV-8: "Finding and Recommendation are contextual Panels, not separate screens"), and `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` all use the **Panel** model.
- But `FINDING_WORKSPACE_SPECIFICATION_V1.md` and `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` are **both Status: Active Release 1**, titled "**Workspace** Specification," and self-describe as standalone **"investigative understanding workspace"** and **"recommendation evaluation and decision-support workspace."** Neither document contains the word "Panel" (0 occurrences each).
- **No reconciliation decision exists** (`FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` is absent).

**Net:** two Active Release 1 specs define Finding/Recommendation as **Workspaces** while ≥4 Active specs define them as **Panels**. This is a genuine architectural conflict about whether these are standalone destinations or contextual panels. **Owner decision required.** (Conflict **UX-C1**.)

*Note:* the **Presentation** specs (`FINDING_PRESENTATION_…`, `RECOMMENDATION_PRESENTATION_…`) are surface-agnostic (they define what is shown, consumable by either a panel or a workspace) and are **not** in conflict — they are the shared substrate both framings cite.

---

## D. MRI Consistency

**Verdict: Consistent — reconciled.** MRI is treated coherently as:

- **Umbrella concept** — `MRI_TERMINOLOGY_RECONCILIATION_DECISION_001.md` (owner-ratified) establishes MRI = umbrella over **MRI Experience**, **MRI Visualization Model**, **MRI Snapshot**, **MRI Navigation**.
- **Diagnostic discovery experience** (`MRI_EXPERIENCE_…`) and **primary diagnostic workspace** (`MRI_WORKSPACE_…`).
- **Not a findings list** (explicitly stated in both MRI specs) and **not merely a visualization component** (the Visualization Model is **one component** of the umbrella; `MRI_MODEL_V1.md` carries the reconciliation banner).

**No terminology/role conflict remains.** The earlier collision (visualization vs. diagnostic) is resolved by Decision 001. Minor residual: non-urgent hygiene — downstream prose that still says "MRI Model" (rather than "MRI Visualization Model") may be normalized on next touch (low severity, already flagged in Decision 001 §6). (Observation **UX-O2**, not a conflict.)

---

## E. Artifact Workspace Consistency

**Verdict: Consistent.** Across `ARTIFACT_WORKSPACE_…` and `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_…`, the Artifact Workspace is uniformly: a **content-centered operating surface**; **artifact as source of truth / center of gravity**; **CAF overlays embedded in content** (one overlay → one or multiple findings, no new objects); **finding discovery through content** (not a list); **recommendation access through finding context**. MRI Workspace and Global Navigation corroborate the "MRI = where to look / Artifact = what it says" complementarity. **No contradictions found.** (One dependency: the Panel framing here depends on UX-C1 being resolved in favor of Panels.)

---

## F. Reanalysis / Stale State Consistency

**Verdict: Consistent.** The reanalysis/stale invariants hold across `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_…` (canonical), `ARTIFACT_WORKSPACE_…`, `ORIENTATION_STATE_MODEL_…`, `COLLABORATION_…`, `GLOBAL_NAVIGATION_…`, and `PROJECT_DASHBOARD_…`:

- editing changes content only; saving changes no assessment; stale clearly marked; **only reanalysis changes assessment**; prior analysis visible until superseded; reanalysis failure preserves last-known-good.
- Dashboard (§K) and Navigation (NAV-11) both **present** stale honestly and never trigger reanalysis themselves. **No drift detected.**

---

## G. Collaboration Consistency

**Verdict: Consistent.** `COLLABORATION_AND_SHARING_EXPERIENCE_…` defines collaboration as **understanding collaboration**, **comments attached to existing objects** (Project/Artifact/Finding/Recommendation), **not governance**, **not execution**, **not assessment-changing**, **not the primary object** (CS-1…CS-15). Navigation (§K) and Settings (collaboration preferences) defer to it without contradiction. **No conflicts.** (Dependency on UX-C1: collaboration anchors comments to the Finding/Recommendation **objects**, which is surface-agnostic and holds under either framing.)

---

## H. Navigation Consistency

**Verdict: Consistent (modulo UX-C1).** `GLOBAL_NAVIGATION_…` represents global/workspace/project/object contexts coherently: Workspace Home as landing; Project Overview as understanding home; MRI + Artifact as primary; Collaboration + History as secondary; Settings as periphery; **Finding/Recommendation as Panels**. Dashboard and Onboarding corroborate Workspace Home as landing. The **only** inconsistency is the same UX-C1: navigation asserts Panels while two Active specs assert Workspaces.

---

## I. Settings / Account Consistency

**Verdict: Consistent.** `ACCOUNT_AND_WORKSPACE_SETTINGS_…` is uniformly the **management periphery**, **separate from project understanding**, **non-assessment-changing**, **not permissions architecture**, **not billing implementation** (SET-1…14; visibility-first subscription/billing/integrations). Navigation (§M) treats settings as periphery without disturbing project context. **No conflicts.**

---

## J. Onboarding / Project Creation Consistency

**Verdict: Consistent.** `ONBOARDING_AND_PROJECT_CREATION_…` supports: lightweight, **skippable** onboarding; **empty project creation allowed**; **project name required**; **artifacts required for value**; **minimum to first value = name + one artifact**; **no AI-generated starting content in Release 1** (deferred). Dashboard ("create your first project") and Navigation (returning-user landing) corroborate. **No conflicts.** *(These resolutions were spec-default decisions, not owner-ratified — see UX-O3 / Area O.)*

---

## K. Dashboard / Project List Consistency

**Verdict: Consistent.** `PROJECT_DASHBOARD_AND_PROJECT_LIST_…` is uniformly the **Workspace Home landing surface** and **project discovery layer**, explicitly **not a health dashboard, metrics cockpit, or work-management board** (PL-6/PL-13). It surfaces the existing reliability-qualified understanding indicator and **explicitly forbids** a "project health/readiness/outcome-probability" indicator — matching the Outcome Confidence doctrine. **No conflicts.**

---

## L. Terminology Audit

**Verdict: Largely consistent; reconciled terms holding.**

| Term | Status | Notes |
|---|---|---|
| Outcome Confidence | ✅ Consistent | trust in understanding, reliability-qualified, never bare; never "health/probability." |
| Reliability-qualified understanding | ✅ Consistent | used uniformly across MRI/Artifact/Dashboard/Overview. |
| MRI | ✅ Reconciled | umbrella per Decision 001 (Area D). |
| Artifact Workspace | ✅ Consistent | content surface; uniform. |
| CAF Overlay | ✅ Consistent | embedded, dimension-organized, no new objects. |
| Finding Panel | ⚠ Conflicted | used by newer stack; contradicted by `FINDING_WORKSPACE_…` (Workspace framing). UX-C1. |
| Recommendation Panel | ⚠ Conflicted | same as above vs. `RECOMMENDATION_WORKSPACE_…`. UX-C1. |
| OSLO Recommended | ✅ Consistent | presentation-only across specs. |
| Possible Resolution Paths | ✅ Consistent | UI pattern over multiple Recommendations (AMB-1 Decision A); resolution-paths spec RETIRED. |
| Selected Path | ✅ Consistent | derived UI state. |
| Stale Analysis | ✅ Consistent | uniform marking; never shown as current. |
| Updated Understanding | ✅ Consistent | post-reanalysis state across specs. |

Residual hygiene: "MRI Model" vs "MRI Visualization Model" naming in older prose (UX-O2, low).

---

## M. Forbidden Capability Audit

**Verdict: Clean in the audited UX specs.**

- **governance / execution / automation / agents / scoring / permissions architecture / APIs / events / implementation / styling:** appear in the UX specs **only as explicit exclusions/guards**, not as introduced capabilities. Each UX spec carries a non-negotiable constraints block and fail conditions forbidding them.
- **project health / outcome probability:** appear **only as negations** (e.g., Dashboard §L guard, Orientation/Confidence doctrine). No accidental introduction.
- **new assessment objects / Resolution Path object / Clarification Candidate / Resolution Candidate:** the active Release 1 UX specs reference these **only as forbidden** ("no Resolution Path / Clarification Candidate / Resolution Candidate object"). The standalone `CLARIFICATION_CANDIDATE_*` and `RESOLUTION_CANDIDATE_MODEL_V1` files are **retired/Future-Architecture** (outside Release 1 UX) and are not invoked as Release 1 objects.
- **Resolution Paths substructure:** `RECOMMENDATION_RESOLUTION_PATHS_SPECIFICATION_V1.md` carries a **RETIRED** banner (AMB-1 Decision A); not active. ✅

No forbidden capability is accidentally introduced by the audited UX documents.

---

## N. Missing UX Surface Audit

| Surface | Present? | Classification |
|---|---|---|
| **Notification Center / awareness UX** | `NOTIFICATION_MODEL_V1.md` exists (model); awareness referenced in Collaboration §O and Settings §J, but **no UX surface** defines where notifications are seen/managed. | **Important but can follow** (awareness is specced as preferences; a center can follow). |
| **Help / Support** | Absent. | **Important but can follow.** |
| **Export / PDF / Sharing-out** | Absent (sharing = collaborator access only; no artifact/understanding export). | **Important but can follow.** |
| **Global Search (content/in-project)** | Dashboard defines **project** search (§H); no global or in-project content search. | **Important but can follow** (project search covers Release 1 discovery). |
| **History / Timeline (dedicated)** | History defined *within* Artifact editing workflow (§M) and Collaboration activity (§L); Navigation §L treats it as secondary. **No standalone History/Timeline spec.** | **Important but can follow** (covered in-context; standalone optional). |
| **Invite / Share Modal details** | Collaboration §E defines sharing UX intent; modal-level detail deferred there. | **Important but can follow.** |
| **Mobile navigation** | Explicitly deferred (Global Nav §T). | **Deferred.** |
| **Tier-limit / Upgrade UX** | Settings (§K/§L) and Dashboard present **visibility-first** plan/usage/limits; **upgrade flow** deferred. | **Important but can follow** (visibility present; transactional upgrade deferred). |
| **Finding/Recommendation surface (Panel vs Workspace) reconciliation** | **Absent.** | **Critical for Release 1** (blocks Area C). |
| **Error/empty-state pattern library (cross-surface)** | Each spec defines its own; no shared catalog. | **Deferred** (consistency is adequate per-spec). |

**Only Critical-for-Release-1 gap:** the Finding/Recommendation **surface reconciliation** (decision artifact), because UX-C1 currently leaves two contradictory Active specs.

---

## O. Conflict Register

| ID | Documents | Nature | Severity | Recommended resolution | Owner decision? |
|---|---|---|---|---|---|
| **UX-C1** | `FINDING_WORKSPACE_SPECIFICATION_V1.md`, `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` **vs** `ARTIFACT_WORKSPACE_…` §D, `MRI_WORKSPACE_…` §4, `GLOBAL_NAVIGATION_…` §J (NAV-8), `COLLABORATION_…` | Two Active Release 1 specs define Finding/Recommendation as **standalone Workspaces**; ≥4 Active specs define them as **contextual Panels**. No reconciliation decision exists. | **High (structural / blocking)** | Ratify the **Panel** model as canonical for Release 1 (it is the majority, newer, navigation-anchored position); **reposition** the two Workspace specs as the **Panel content/behavior specs** (retitle/retag to "Finding Panel" / "Recommendation Panel," or add reconciliation banners subordinating them to the Panel framing) — mirroring how the MRI collision was reconciled. Author a `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`. | **Yes** |
| **UX-C2** | `FINDING_WORKSPACE_…` / `RECOMMENDATION_WORKSPACE_…` (title/status metadata) | Even if Panel model is ratified, the **titles/status** still say "Workspace / Active Release 1," creating naming drift in the index. | **Medium** | On UX-C1 ratification, retitle/retag or banner these two docs; normalize index references. | Follows UX-C1 |
| **UX-O2** | `MRI_MODEL_V1.md` and older prose | "MRI Model" vs reconciled "MRI Visualization Model" naming. | **Low (hygiene)** | Normalize on next touch (already noted in Decision 001 §6). | No |
| **UX-O3** | `ONBOARDING_…` (Release 1 resolutions) | Onboarding resolved open questions (name required; type/workflow optional; templates & AI-generated starts deferred) as **spec-defaults**, not owner-ratified. | **Low–Medium** | Confirm as owner-ratified or convert to backlog proposals. | Yes (confirm) |

No other substantive conflicts detected. (Forbidden-capability and stale/reanalysis/collaboration/settings/dashboard areas are clean.)

---

## P. Readiness Assessment

**Verdict: Conditionally ready for design/dev handoff.**

- **Why not "Ready":** **UX-C1** is a structural, blocking conflict — designers/developers cannot be told definitively whether Finding and Recommendation are **panels** or **workspaces**, and two Active specs say opposite things. This single decision shapes navigation, the Artifact/MRI surfaces, and the object-context model.
- **Why not "Not ready":** everything else is coherent. The end-to-end flow, the four primary surfaces, MRI (reconciled), the Artifact content model, the reanalysis/stale invariants, collaboration, settings, onboarding, navigation, and the dashboard are mutually consistent and free of forbidden-capability drift. The conflict is **localized and reconcilable** with one owner decision + a repositioning pass (the MRI reconciliation is a proven template).

**Condition for full readiness:** ratify UX-C1 (Panel vs Workspace) and reposition the two affected specs; confirm UX-O3 onboarding defaults. After that, the stack is handoff-ready (with the Area-N "important but can follow" surfaces tracked as fast-follows).

---

## Q. Recommended Next Artifacts

Prioritized by architectural risk → implementation risk → user value → release readiness:

1. **`FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`** *(highest — unblocks UX-C1).* Owner-ratified decision fixing whether Finding/Recommendation are **Panels** (recommended) or **Workspaces**, with the consequence map for `FINDING_WORKSPACE_…` / `RECOMMENDATION_WORKSPACE_…` (reposition as Panel specs). Directly resolves the only blocking conflict and the only Critical Release 1 gap.
2. **Repositioning pass on `FINDING_WORKSPACE_SPECIFICATION_V1.md` and `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md`** *(applies the decision — resolves UX-C2).* Retitle/retag to the ratified surface model (e.g., "Finding Panel Specification") or add subordinating reconciliation banners; align with the Presentation specs and Navigation §J.
3. **`NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md`** *(highest-value fast-follow).* Defines *where* the awareness model (mentions/replies/new comments/shared-project activity) is seen/managed, closing the most-referenced "important but can follow" gap and completing the collaboration loop. (Alternatively, an onboarding-defaults confirmation note for UX-O3 if the owner prefers to close governance items first.)

---

*This audit evaluated the complete Release 1 UX specification stack for one coherent OSLO product experience. The architecture is substantially coherent — the end-to-end flow, four primary surfaces, MRI umbrella reconciliation, Artifact content model, reanalysis/stale invariants, collaboration, settings, onboarding, navigation, and dashboard are mutually consistent and free of forbidden-capability drift. One structural conflict (UX-C1: Finding/Recommendation as Panels vs. standalone Workspaces) remains unresolved, with no surface-reconciliation decision present; it is localized, reconcilable, and owner-decidable. Release 1 UX is therefore **Conditionally Ready**: ratify the surface model and reposition two specs, confirm the onboarding spec-defaults, and the stack is handoff-ready. This audit modified no specification, introduced no object, and resolved no owner-level decision.*

**Release 1 UX Architecture Consistency Audit 001 complete.**

# Finding & Recommendation Surface Reconciliation Decision 001

**Document Type:** Architecture Reconciliation Decision
**Status:** **Ratified · Option A — Panel Model** (owner-ratified 2026-05-31) · **Date:** 2026-05-31
**Raised by:** `RELEASE_1_UX_ARCHITECTURE_CONSISTENCY_AUDIT_001.md` (Conflict **UX-C1**)
**Applied by:** `FINDING_PANEL_SPECIFICATION_V1.md`, `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` (new); supersession banners on the former Workspace specs; reference normalization across active UX docs.

> **Mode: Evaluate only.** This document modifies no specification, introduces no object, and **does not** redefine Findings, Recommendations, MRI, Artifact Workspace, or Navigation. It determines **only** the canonical Release 1 UX **surface model** for Findings and Recommendations. It does not assume owner approval and does not auto-resolve.

---

## Purpose

Resolve the Release 1 conflict over the canonical UX surface for Findings and Recommendations. The stack currently contains two competing definitions:

- **Surface Model A — Panel.** Findings/Recommendations are first-class **model objects** surfaced through **contextual panels**, opened from MRI and Artifact contexts, **not standalone destinations**. Referenced by `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md`, `MRI_WORKSPACE_SPECIFICATION_V1.md`, `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md`, `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`.
- **Surface Model B — Workspace.** Findings/Recommendations are **standalone workspaces** — separate navigable destinations, independently entered/exited. Referenced by `FINDING_WORKSPACE_SPECIFICATION_V1.md`, `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md`.

The Release 1 UX architecture cannot remain in both states. This document determines the canonical model. **Both models agree** that Findings remain the canonical **descriptive** object and Recommendations the canonical **advisory** object — this decision concerns **surface/navigation only**, not the object model.

---

## A. Decision Required

**Select one and only one.**

### Option A — Panel Model
Findings and Recommendations remain: first-class model objects; **contextual UX panels**; **subordinate to** Artifact Workspace and MRI Workspace; **not standalone destinations**.
**Consequences:** `FINDING_WORKSPACE_SPECIFICATION_V1.md` → repositioned as **Finding Panel Specification**; `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` → **Recommendation Panel Specification**; Navigation architecture **unchanged**; Object Context **intact**.

### Option B — Workspace Model
Findings and Recommendations remain: **standalone workspaces**; **primary navigable destinations**; entered through navigation transitions.
**Consequences:** `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` revised; `MRI_WORKSPACE_SPECIFICATION_V1.md` revised; `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` revised; `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` revised; **Object Context model revised**.

---

## B. Evaluation Criteria

### B1. Understanding Lifecycle Alignment
*Lifecycle: 60-Second Orientation → Project Overview → MRI Workspace → Artifact Workspace → Finding → Recommendation.*

- **Option A:** **Stronger.** The lifecycle terminates in **Finding → Recommendation as the explanation/evaluation steps reached *within* the surface the user is already in** (MRI or Artifact). A panel opens in place, continuing the flow without a destination change. The progression reads as a single deepening investigation.
- **Option B:** **Weaker.** Findings/Recommendations become separate destinations, turning the final lifecycle steps into **navigation jumps** away from the artifact/MRI context, breaking the "deepen in place" feel.
- **Edge:** **Option A.**

### B2. Context Preservation
*Preserve: MRI selection, artifact context, CAF overlay context, finding evidence, recommendation evaluation.*

- **Option A:** **Stronger.** A panel opens **over/beside** the current surface, so the MRI lens/selection, the artifact content and scroll position, and the originating CAF overlay all remain beneath the panel. Closing returns exactly to context. This is the explicit promise of the Object Context model (Nav NAV-7/NAV-8).
- **Option B:** **Weaker.** Entering a standalone workspace **leaves** the artifact/MRI surface; the overlay/selection context must be re-established on return, risking loss of "where was I."
- **Edge:** **Option A.**

### B3. Cognitive Load
*Support: orientation, navigation simplicity, reduced mode switching, reduced workspace proliferation.*

- **Option A:** **Stronger.** Fewer top-level surfaces (four primaries + panels), less mode switching, and no proliferation of destinations. The user stays oriented in MRI/Artifact while panels handle depth.
- **Option B:** **Weaker.** Adds two more standalone workspaces and more transitions; increases the number of "modes" a user must track and the chances of disorientation.
- **Edge:** **Option A.**

### B4. Collaboration Alignment
*Support: comments orbiting understanding objects, understanding-first collaboration, contextual discussion.*

- **Option A:** **Stronger.** `COLLABORATION_…` already specifies comments **orbiting** objects in context (Finding/Recommendation Panels). Panels keep discussion attached where the understanding lives.
- **Option B:** **Neutral-to-weaker.** Collaboration still attaches to the objects, but discussion would migrate to standalone screens, weakening the "orbit in context" intent and requiring `COLLABORATION_…` revision.
- **Edge:** **Option A.**

### B5. Navigation Consistency
*Align with Workspace / Project / Object contexts in `GLOBAL_NAVIGATION_…`.*

- **Option A:** **Stronger.** Findings/Recommendations map cleanly to **Object Context** (panels within a project surface). Navigation needs **no change**; NAV-8 already asserts the Panel model.
- **Option B:** **Weaker.** Findings/Recommendations would become **Project-Context destinations**, contradicting NAV-8 and forcing a Navigation rewrite and an Object-Context redefinition.
- **Edge:** **Option A.**

### B6. Architectural Simplicity
*Produce: fewer surfaces, fewer transitions, fewer duplicated concepts, clearer ownership boundaries.*

- **Option A:** **Stronger.** Fewer UX surfaces and transitions; no duplication between an "Artifact-with-finding-context" and a separate "Finding workspace"; clear ownership (Presentation specs define content; Panels host it; Artifact/MRI own context).
- **Option B:** **Weaker.** Adds surfaces and transitions and risks concept duplication (finding context exists both in the Artifact overlay/panel and in a standalone Finding workspace).
- **Edge:** **Option A.**

**Summary:** Option A is favored on **all six** criteria (B1–B6), most decisively on context preservation (B2), navigation consistency (B5), and architectural simplicity (B6).

---

## C. Impact Assessment

*Assessed for the **recommended** option (A). The owner may select either; Option B's heavier impact is summarized at the end.*

### C.A — Impact if Option A (Panel) is selected

**Affected specifications:**

| Specification | Required change |
|---|---|
| `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` | **No change** (already Panel / NAV-8). |
| `MRI_WORKSPACE_SPECIFICATION_V1.md` | **No change** (already routes to Panels). |
| `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` | **No change** (already Panel framing, §D). |
| `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` | **No change** (object-anchored, panel-aligned). |
| `FINDING_PRESENTATION_SPECIFICATION_V1.md` | **No change** (surface-agnostic). |
| `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` | **No change** (surface-agnostic). |
| `FINDING_WORKSPACE_SPECIFICATION_V1.md` | **Structural reposition** → **Finding Panel Specification** (retitle/retag; add reconciliation banner; reframe "workspace" → "panel"; subordinate to Artifact/MRI). Substantive UX content (descriptive-first, evidence-first, recommendation-enabled, reanalysis-driven) is **largely portable**. |
| `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` | **Structural reposition** → **Recommendation Panel Specification** (retitle/retag; banner; reframe; subordinate). Substantive content (advisory-first, finding-anchored, OSLO Recommended / Possible Resolution Paths / Selected Path) is **largely portable**. |
| `RELEASE_1_UX_ARCHITECTURE_CONSISTENCY_AUDIT_001.md` | **Terminology/status update** on next touch (UX-C1/UX-C2 marked resolved). |
| Index/orientation docs referencing the two specs | **Terminology update** (Workspace → Panel). |

**Migration impact (Option A):**
- **Obsolete documents:** none (no deletion).
- **Require renaming:** `FINDING_WORKSPACE_SPECIFICATION_V1.md`, `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md` (→ Panel specs).
- **Require repositioning:** the same two documents (workspace → contextual panel; add banners; subordinate to Artifact/MRI), mirroring the MRI umbrella reconciliation pattern (append-only banners, content preserved).

**Release 1 Risk (Option A): Low.**
Four of the affected specs (Navigation, MRI, Artifact, Collaboration) need **no change** because they already assume the Panel model. Only **two** specs are repositioned, and their substantive UX content is portable (the conflict is framing/title, not behavior). The Presentation specs are surface-agnostic and untouched. No object is redefined; the change is naming/positioning. This matches a proven reconciliation template (MRI Decision 001).

### C.B — Impact if Option B (Workspace) is selected *(for contrast)*

**Affected specifications:** `GLOBAL_NAVIGATION_…` (revise NAV-8 + Object Context), `MRI_WORKSPACE_…` (revise routing), `ARTIFACT_WORKSPACE_…` (revise §D + panel integration), `COLLABORATION_…` (revise contextual-discussion model); `FINDING_WORKSPACE_…` / `RECOMMENDATION_WORKSPACE_…` keep titles but must be re-cross-referenced as primary destinations.
**Migration impact:** redefine the **Object Context** model; add two **Project-Context destinations**; update navigation transitions and primary/secondary ordering.
**Release 1 Risk: Medium–High.** Requires revising the four newest, most cross-cutting specs (including the navigation constitution and the Object-Context model), with broader regression surface and higher chance of secondary drift.

---

## D. Recommended Resolution

**Architectural recommendation: adopt Option A — the Panel Model — as the canonical Release 1 surface model for Findings and Recommendations.**

**Rationale.** Option A wins on all six evaluation criteria, most decisively on context preservation, navigation consistency, and architectural simplicity. It keeps **understanding the center of gravity** by letting users deepen into Finding explanation and Recommendation evaluation **in place** (over MRI/Artifact context) rather than navigating away. It requires **no change** to four cross-cutting specs (Navigation, MRI, Artifact, Collaboration) that already assume it, and **Low** Release 1 risk because only two specs are repositioned and their behavior is portable. It is also the **majority and newer** position across the stack and aligns with the already-ratified Object-Context model.

**Tradeoffs.** (1) Panels must comfortably present rich Finding evidence and multi-Recommendation evaluation (Possible Resolution Paths) without feeling cramped — a design constraint, not an architectural blocker. (2) Deep, focused, long-session evaluation of a complex recommendation set is marginally better served by a full workspace; Option A accepts this in exchange for context preservation and simplicity. (3) Repositioning two specs is required, but is banner-based and non-destructive.

**Implementation-neutral consequences (Option A).** Finding and Recommendation remain first-class **model objects** (unchanged); their **surface** is a contextual panel opened from MRI/Artifact/Overview contexts; the two "Workspace" specs become **Panel** specs subordinate to Artifact/MRI; Navigation and Object Context remain intact; Presentation specs remain the shared content substrate. No object, lifecycle, or assessment behavior changes — **only the surface framing**.

*(This section is a recommendation only. The owner may select Option B; Section C.B documents its heavier but viable path.)*

---

## E. Owner Decision Section

### Owner Selection

```
[x] Option A — Panel Model        (recommended) — RATIFIED 2026-05-31
[ ] Option B — Workspace Model
```

### Effective Release 1 Canonical Surface Model

**Findings and Recommendations are first-class model objects surfaced through contextual panels, not standalone destinations.**

The canonical Release 1 flow is: **Project Overview → MRI Workspace → Artifact Workspace → Finding Panel → Recommendation Panel.** Findings remain first-class **descriptive** model objects; Recommendations remain first-class **advisory** model objects; their **surface** is a contextual panel opened from MRI/Artifact (Finding Panel) and from Finding context (Recommendation Panel). Object models, lifecycle models, CAF, Reliability, Confidence, and Recommendation attribution are **unchanged** — this is a UX surface/document repositioning only.

### Applied (owner-ratified)
- **Created:** `FINDING_PANEL_SPECIFICATION_V1.md`, `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` (former Workspace content adapted into panel language).
- **Superseded/repositioned (retained, banner-marked):** `FINDING_WORKSPACE_SPECIFICATION_V1.md`, `RECOMMENDATION_WORKSPACE_SPECIFICATION_V1.md`.
- **Normalized:** Workspace → Panel references across active UX docs; UX-C1 / UX-C2 marked resolved in `RELEASE_1_UX_ARCHITECTURE_CONSISTENCY_AUDIT_001.md`.
- **Unchanged:** `FINDING_PRESENTATION_SPECIFICATION_V1.md`, `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` (surface-agnostic; referenced by the new panel specs).

---

## Constraints Honored

Evaluate only · modified no specification · introduced no object · did not redefine Findings, Recommendations, MRI, Artifact Workspace, or Navigation · did not assume owner approval · did not auto-resolve. The sole purpose was to determine the canonical Release 1 surface model.

---

*This reconciliation evaluates the two competing Release 1 surface models for Findings and Recommendations — Panel (Model A) vs. standalone Workspace (Model B). Across all six criteria (lifecycle alignment, context preservation, cognitive load, collaboration alignment, navigation consistency, architectural simplicity), the Panel Model is favored; it requires no change to four cross-cutting specs, repositions only two, carries Low Release 1 risk, and keeps understanding the center of gravity. Option A is therefore recommended, with Option B documented as a viable but heavier (Medium–High risk) path. The decision remains Pending Owner Decision; no specification was modified and no owner-level decision was resolved.*

**Finding & Recommendation Surface Reconciliation Decision 001 complete.**

# Understanding Companion Reconciliation Decision 001

**Document Type:** Architecture Reconciliation Decision
**Status:** **Ratified · Option B — Finding-Context Entry** (owner-ratified 2026-05-31) · **Date:** 2026-05-31
**Raised by:** Conflict between `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md` and `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`
**Applied by:** Companion spec changes (Q6 replaced, §I replaced, open-reconciliation banner removed); flag cleared in `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md`.

> **Mode: Evaluate only.** This decision modifies no specification through its own text, introduces no object, and does not redefine Findings, Recommendations, Panels, MRI, Artifact Workspace, or Navigation. It determines **only** the canonical navigation path from the Understanding Companion to Recommendation Panels. (The application of the ratified decision to the Companion and Journey specs is recorded separately below.)

---

## Purpose

Resolve the conflict regarding how users navigate from **Top Recommendations** in the Understanding Companion. The Release 1 architecture contained two competing definitions:

### Model A — Direct Recommendation Entry
```text
Understanding Companion
        ↓
 Recommendation Panel
```
Referenced by: Understanding Companion Specification **Q6** and **§I**.

### Model B — Finding-Context Recommendation Entry
```text
Understanding Companion
        ↓
 Associated Finding Panel
        ↓
 Recommendation Panel
```
Referenced by: `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md` · `RECOMMENDATION_PANEL_SPECIFICATION_V1.md` · the canonical Finding → Recommendation lifecycle · the Object Context navigation model.

Both models **preserve Recommendation objects.** The conflict concerns **navigation and context preservation only.**

---

## A. Decision Required

**Select one and only one.**

### Option A — Direct Recommendation Entry
Users may open Recommendation Panels directly from Top Recommendations within the Understanding Companion.
**Consequences:** Recommendation Panel becomes reachable without Finding context; Recommendation → Finding attribution becomes optional during entry; Recommendation Panel navigation rules require revision.

### Option B — Finding-Context Entry
Users selecting a recommendation from the Understanding Companion are routed through the associated Finding.
**Canonical path:** Understanding Companion → Associated Finding Panel → Recommendation Panel.
**Consequences:** Recommendation → Finding attribution remains intact; Recommendation Panel remains subordinate to Finding context; existing Navigation and Panel architecture remain unchanged.

---

## B. Evaluation

| Criterion | Analysis | Advantage |
|---|---|---|
| **B1. Attribution Preservation** | Recommendations exist because Findings exist; a recommendation without its originating finding loses explanatory context. | **Option B** |
| **B2. Architectural Consistency** | Release 1 establishes Artifact → Finding → Recommendation (Finding Panel spec, Recommendation Panel spec, Surface Reconciliation Decision 001). Direct entry introduces a second navigation model. | **Option B** |
| **B3. Context Preservation** | Recommendation evaluation depends on the finding, its evidence, CAF impact, and confidence impact — Finding context provides that understanding. | **Option B** |
| **B4. Cognitive Consistency** | Users learn Problem → Recommendation, not Recommendation → discover underlying problem. | **Option B** |
| **B5. Release 1 Risk** | Option A modifies the Recommendation Panel spec, Navigation rules, and Companion spec; Option B updates only the Companion spec. | **Option B** |

**Summary:** Option B is favored on all five criteria.

---

## C. Recommended Resolution

**Adopt Option B — Finding-Context Entry** as the canonical Release 1 navigation model. Top Recommendations remain visible within the Understanding Companion; recommendation selection preserves the established hierarchy **Finding → Recommendation** by routing through the associated Finding. This maintains attribution integrity, navigation consistency, object-context integrity, and understanding-first investigation.

---

## D. Required Companion Specification Changes (authorized; applied)

### Replace Q6 with:
> **Q6 — Relationship to Recommendation Panels**
> **Resolution:** Top Recommendations do not open Recommendation Panels directly. Because Recommendation Panels are valid only in Finding context, selecting a Top Recommendation routes through the associated Finding.
> **Canonical path:** Understanding Companion → Associated Finding Panel → Recommendation Panel.
> This preserves Recommendation → Finding attribution and maintains Recommendation Panels as subordinate to Finding context.

### Replace Section I with:
> **I. Top Recommendations Visibility**
> The companion surfaces the most relevant existing recommendations from current understanding. Recommendations remain advisory, existing, previously produced. Selecting a Top Recommendation opens the **associated Finding Panel first** and then surfaces the **Recommendation Panel from that Finding context.** The Companion never opens a Recommendation Panel as a standalone destination and never bypasses the associated Finding.

### Remove:
The **Open Reconciliation Item** banner from the top of the Companion Specification. **Conflict resolved.**

---

## E. Owner Decision

### Owner Selection
```
[ ] Option A — Direct Recommendation Entry
[x] Option B — Finding-Context Entry (recommended) — RATIFIED 2026-05-31
```

### Effective Canonical Release 1 Navigation
```text
Understanding Companion
        ↓
 Associated Finding Panel
        ↓
 Recommendation Panel
```
**Recommendation Panels remain valid only in Finding context.**

### Applied (owner-ratified)
- `UNDERSTANDING_COMPANION_SURFACE_EXPERIENCE_SPECIFICATION_V1.md`: Q6 replaced; §I replaced; open-reconciliation banner removed.
- `UNDERSTANDING_JOURNEY_AND_SURFACE_TRANSITION_EXPERIENCE_SPECIFICATION_V1.md`: Companion→Recommendation flag cleared (now canonical Model B).
- **Unchanged:** `RECOMMENDATION_PANEL_SPECIFICATION_V1.md`, `FINDING_PANEL_SPECIFICATION_V1.md`, `FINDING_AND_RECOMMENDATION_SURFACE_RECONCILIATION_DECISION_001.md`, Navigation — Option B requires no change to them.

---

**Understanding Companion Reconciliation Decision 001 complete.**

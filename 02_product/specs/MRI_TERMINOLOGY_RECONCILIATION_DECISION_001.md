# MRI Terminology Reconciliation — Decision 001

**Type:** Reconciliation Decision (ontology / canonical terminology)
**Status:** Owner-ratified · Active Release 1 · **Date:** 2026-05-31
**Authority:** Repository owner (per `CLAUDE.md` — only the owner may adopt/reclassify canonical content)
**Affects:** `MRI_MODEL_V1.md` · `MRI_EXPERIENCE_SPECIFICATION_V1.md` · `MRISnapshot` (Data Model) · `Time-to-First-MRI` metric (Master Spec) · `SIXTY_SECOND_ORIENTATION_WORKFLOW_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md`

---

## 1. Issue

"MRI" had drifted toward **two meanings**:

1. **MRI as visualization** — `MRI_MODEL_V1.md` defines MRI as "OSLO's visual representation of project understanding," with `MRISnapshot` and the `Time-to-First-MRI` metric.
2. **MRI as diagnostic experience** — the new UX work (Missing · Risky · Incomplete) positions MRI as the primary diagnostic understanding experience between Project Overview and the Finding / Recommendation / Artifact workspaces.

Left unreconciled, this produces **two competing canonical meanings for one acronym** — terminology drift the governance rules prohibit.

## 2. Owner Decision

**MRI is reconciled as a single umbrella concept**, not two competing meanings. MRI's UX role has broadened beyond visualization to the **primary diagnostic understanding experience**; the umbrella keeps the architecture coherent.

**MRI (umbrella)** comprises these components:

| Component | Role | Canonical home |
|---|---|---|
| **MRI Experience** | The user-facing diagnostic understanding & navigation experience (Missing · Risky · Incomplete) between Project Overview and the deeper workspaces. | `MRI_EXPERIENCE_SPECIFICATION_V1.md` |
| **MRI Visualization Model** | The conceptual/behavioral model that makes understanding observable (CAF · Reliability · Outcome Confidence). *(Formerly "MRI Model.")* | `MRI_MODEL_V1.md` |
| **MRI Snapshot** | The visualization snapshot of understanding. **Unchanged.** | Data Model (`MRISnapshot`) |
| **MRI Navigation** | The navigation/drill-down behavior from MRI into Finding / Artifact / Recommendation surfaces. | Within `MRI_EXPERIENCE_SPECIFICATION_V1.md` (Release 1); may separate later. |

### 2.1 Ratified consequences

- **R1.** **MRI remains a single concept.** There are not two MRIs; there is one MRI with components.
- **R2.** **MRI Visualization becomes a component of MRI.** `MRI_MODEL_V1.md` is repositioned as the **MRI Visualization Model** under the umbrella; its substantive positions (Positions #1–#9, event-driven, descriptive-not-prescriptive, consumer-only) are **preserved unchanged**.
- **R3.** **MRI Snapshot remains valid** and unchanged.
- **R4.** **The new workspace/navigation behavior is the MRI Experience** — the user-facing diagnostic surface that **uses** the MRI Visualization Model and MRI Snapshot rather than competing with them.
- **R5.** **No second meaning of "MRI" is created.** The prior collision flag in `MRI_EXPERIENCE_SPECIFICATION_V1.md` is **resolved by this decision** and is to be removed in favor of the umbrella framing.

## 3. Relationship Between Components

```text
MRI (umbrella concept)
 ├─ MRI Experience          ← user-facing diagnostic experience (Missing · Risky · Incomplete)
 │     uses ▼
 ├─ MRI Visualization Model ← makes understanding observable (CAF · Reliability · Confidence)
 ├─ MRI Snapshot            ← visualization snapshot of understanding
 └─ MRI Navigation          ← drill-down into Finding / Artifact / Recommendation
```

- The **MRI Experience** is the diagnostic/navigation surface; it **consumes** the **MRI Visualization Model** (the observable understanding) and **MRI Snapshot**, and **routes** via **MRI Navigation**.
- This is consistent with `MRI_MODEL_V1.md` §12 (Future Evolution), which already anticipated **navigation mechanisms** and **interaction layers** as **separate components** extending how understanding is surfaced — not redefinitions of the Visualization Model.

## 4. Preserved Invariants (unchanged by this reconciliation)

- The **MRI Visualization Model** remains a **consumer** of CAF / Reliability / Outcome Confidence; it does not assess, score, calculate, or interpret. (Positions #1–#9 hold.)
- **Findings** remain the canonical **descriptive** object; **Recommendations** the canonical **advisory** object; **Artifacts** the canonical planning context.
- **Only reanalysis changes assessment.** MRI (any component) changes no CAF / Reliability / Confidence signal and resolves no finding.
- **No new ontology, governance, execution, automation, scoring, calculation, API, or event** is introduced by this reconciliation. It is a **naming/architecture reconciliation only**.
- `MRISnapshot` and `Time-to-First-MRI` retain their meaning; "first MRI" continues to denote the first observable understanding (the Visualization Model / Snapshot), now understood as a component of the MRI umbrella.

## 5. Application (this decision authorizes)

1. **`MRI_MODEL_V1.md`** — add a reconciliation header positioning it as the **MRI Visualization Model**, a component of the MRI umbrella; **no change to its substantive positions**.
2. **`MRI_EXPERIENCE_SPECIFICATION_V1.md`** — **remove the collision flag**; reframe under the umbrella; state that the Experience **uses** the MRI Visualization Model and MRI Snapshot.
3. **No edit required** to `MRISnapshot` or `Time-to-First-MRI` (semantics preserved); a future cross-reference pass may add umbrella-pointer notes where helpful.

## 6. Open / Deferred

- Whether **MRI Navigation** warrants its own standalone spec (vs. remaining a section of the MRI Experience) is **deferred** to a later release; Release 1 keeps it within the Experience spec.
- Any downstream document still calling the Visualization Model simply "MRI Model" should be updated to "**MRI Visualization Model**" on next touch (non-urgent terminology hygiene; not a substantive change).

---

*Owner-ratified reconciliation: MRI is a single umbrella concept comprising the MRI Experience (diagnostic), the MRI Visualization Model (observable understanding, formerly "MRI Model," substantively unchanged), MRI Snapshot (unchanged), and MRI Navigation. The new diagnostic experience uses the Visualization Model and Snapshot rather than competing with them. No second meaning of "MRI" exists; no new ontology, governance, execution, scoring, API, or event is introduced.*

**MRI Terminology Reconciliation — Decision 001 complete.**

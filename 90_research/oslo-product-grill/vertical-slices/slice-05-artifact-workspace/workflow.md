# Slice 5 — Plan Artifacts / Artifact Workspace · Workflow

**Cumulative (Slices 1–5).** The full journey from Slice 1 is preserved; this document covers the NEW Slice-5 flows and where they attach.

Decisions: **D066–D071**; inherited D006, D011, D042.

---

## Where the workspace attaches

Prior journey (unchanged): invite → activation → welcome → intake → Fast Pass ≈30s → land on **Overview** (Attention co-primary) → Extended Analysis auto-runs → clarification loop. Slice 5 adds a **third co-primary destination — Artifacts** — reachable at any point after landing.

```
[Overview]  ⇄  [Attention]  ⇄  [Artifacts]      (top-center co-primary switch)
                                   │
                                   ├─ explorer (7 artifacts, live issue badges)
                                   └─ editor (prose / mixed / table)
```

## Flow A — Open and read an artifact (D066/D067)

1. User selects **Artifacts** (top-center) → workspace opens, explorer shows the 7 artifacts with live open-issue badges.
2. User clicks an artifact (or Enter/Space) → `openArtifact(name)` renders it in the center editor with its type-aware format.
3. Understanding artifacts read as prose (mixing bullets/tables where useful); Execution artifacts read as tables.

## Flow B — Investigate a weakness (D068)

1. In the open artifact, a **colored span** marks a weak spot.
2. **Hover** → one-line summary.
3. **Click** → the **light Issue panel** opens for that issue (Why → Evidence → Clarification → Suggested fixes).
4. The user answers the clarification (inherited D042) → reanalysis → the issue resolves → the annotation drops from the artifact and the explorer badge updates.
   - The weakness is **never** resolved inline — resolution runs through the issue/reanalysis path.

## Flow C — Edit a sentence → Confirmed by you → reanalysis (D069/D070)

1. User types into a block. That block flips **From OSLO → Confirmed by you** (left-border accent) — it is now a plan fact.
2. The status chip runs **Saving… → Saved · analysis stale → Reanalyzing… → Up to date** automatically. The hint bar states: *saving changes no assessment; only reanalysis does.*
3. No manual reanalyze button is offered at any point (D070/D006).

## Flow D — Step through weaknesses / navigate artifacts (D071)

1. **Jump to weakness ⌃ k of N ⌄** cycles the weak spans in the open artifact, highlighting and scrolling to each.
2. **‹ / ›** move between artifacts in order; disabled at the ends.
3. Both are keyboard-operable.

## Flow E — Feature tour, artifact-edit step (D071/D044)

1. From the completion notice or the "Take a quick tour" affordance, the tour runs.
2. Its artifact-edit step opens the workspace on **Resources** and spotlights the editor — explaining edit → Confirmed by you, inline weakness colors, and auto-reanalysis with no manual button.
3. The tour then completes on the OSLO chat rail and sunsets (localStorage).

## Boundaries

- **Full Issues surface** (grouping/triage/By dimension·severity) → **Slice 6**. Annotations route to the light panel (seam).
- **History / version timeline** → **Slice 7**. The version chip bumps; the append-only timeline is not built here.
- **Apply-a-fix drafting into the artifact** → **Slice 6**.

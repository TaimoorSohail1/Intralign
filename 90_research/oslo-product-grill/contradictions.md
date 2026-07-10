# Contradictions — OSLO R1

## Contradiction C-001: MRI placement — nested vs co-primary
New request: —  (surfaced during scan)
Conflicting prior decision: Prototype nests MRI/Attention inside the Overview; GLOBAL_NAVIGATION NAV-C3 (owner-directed) calls MRI a **co-primary** top-center view alongside Overview and Artifact.
Affected slices: Slice 3 (Overview), Slice 4 (Attention Map).
Affected files: slice-03 docs, slice-04 docs, prototype nav.
Risk: Low. Both keep Attention reachable; difference is IA prominence.
Recommended resolution: Owner confirm. Default = Attention/MRI reachable as a co-primary top-center view (NAV-C3), while the Overview retains an Attention section pointer. Not blocking slice-map approval.
**RESOLVED 2026-07-09 (D038):** orientation lands on the confidence-led Overview; Attention Map is a co-primary top-center view. Owner may flip to Attention-first later.

## Contradiction C-002: "Recommendation Workspace" in UI inventory vs Panel Model
New request: —
Conflicting prior decision: UI_SCREEN_INVENTORY / RELEASE_1_UI_SPECIFICATION still list a "Recommendation Workspace"; ratified Decision 001 (Panel Model) says recommendations live only in the Finding context (no orphan surface).
Affected slices: Slice 6.
Affected files: slice-06 docs.
Risk: Low. Prototype already follows Panel Model.
Recommended resolution: Normalize the UI inventory to the Panel Model (owner doc task). Prototype needs no change. Not blocking.

## Escalated (genuine spec gap — not a contradiction)
- **CRR (CAF Review Requests / evidence-request → Deep-Pass virality loop):** not defined in any R1 surface spec. Per Anti-Assumption, escalated to owner — not invented. Out of scope for the prototype until a dedicated spec exists.

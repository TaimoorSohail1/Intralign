# Decision Progress — OSLO R1

**Updated:** 2026-07-09 (Phase 1 scan + v4 reconciliation; slice map approved)
**Baseline:** `oslo_r1_experience_mockup_v4.html`

## Totals
- Total tracked decisions: 24 (20 locked + 4 needs-decision)
- Done (Locked from docs): 20 (incl. D002/D008/D009 updated for v4; D017–D020 new)
- Pending (Needs decision): 4 (ND-1…ND-4)
- Superseded: v2 lifecycle, v2 confidence ring, 4-band vocabulary (folded into D002/D008/D018/D019/D020)
- **Doc-backed lock rate: 83%**

## By type
- Product Constraint: 1 · Product Requirement: 3 · Product Design: 5 · Product Data: 4 · Journey: 1 · AI Behavior: 1 · Screen/Interaction: 3 · Routing: 1 · Scope: 1 · Theme: 1 · Prototype: 1 · Needs decision: 4

## By slice
- Cross-cutting (All): D001, D003, D012, D013(shell), D015, D016, D017(copy)
- Slice 2: D005 · Slice 3: D002, D010, D019, D020 · Slice 4: D007 · Slice 5: D004, D006, D011 · Slice 6: D008, D009, D017, D018 · Slice 8: D013 · Slice 10: D014

## v4 reconciliation delta
- Updated: D002 (Overview redesign + 5-band), D008 (Issues label + lifecycle), D009 ("Apply this fix").
- Added: D017 (Issues label), D018 (lifecycle), D019 (Overview redesign), D020 (5-band).
- Files touched: decision-log, canonical-truth, decision-tree, theme-system, slice-map, source-summary, session-state.

## Slice 1 (locked 2026-07-09)
- D021–D029 locked (all recs accepted + GA-phase clarification). ND-1 resolved (D029).
- Prototype feedback R2: D030 (sample = all-phase user-initiated; anonymity GA-only), D031 (Fast Pass ≈30s). Applied via worker.
- Totals now: 35 decisions (31 locked + 3 needs-decision). Lock rate ~91%.

## Slice 2 (locked 2026-07-09)
- D035–D042 locked (all recs accepted). C-001 resolved (D038: land on Overview, Attention co-primary). ND-4 resolved.
- Totals now: 43 decisions (41 locked + 2 needs-decision: ND-2 confidence magnitude, ND-3 later-slice scope). Lock rate ~95%.

## Slice 3 (locked 2026-07-09)
- D050–D056 locked (all recs accepted). ND-2 resolved (D056: direction-only). Prototype feedback on Slices 1–2 folded (D043–D049).
- Running total: 56 decisions locked + 1 open (ND-3: later-slice scope). Lock rate ~98%.

## Slice 4 (locked 2026-07-09)
- D057–D062 locked (all recs accepted).
- Running total: 62 decisions locked + 1 open (ND-3: later-slice scope).

## Slice 5 (locked 2026-07-09)
- D066–D071 locked (all recs accepted + F5.2Q1 mixed-content clarification). Slice 4 feedback folded (D063–D065, D053-rev).
- Running total: 71 decisions locked + 1 open (ND-3: later-slice scope).

## Current active slice
- **Slice 5 — Plan Artifacts / Artifact Workspace.** Decisions locked; delegating cumulative prototype (Slices 1–5) + Slice 5 docs to worker.

## Next blocking decision
- Worker builds Slice 5 deliverables → client review → signoff. Then Slice 6 (Issues & Recommendations — Panel Model).

## Signed off
- Slice 1, Slice 2, Slice 3, Slice 4 (2026-07-09).

---
**2026-07-14 · WI-R5 (DL-111 fold-in):** +1 decision (Decision 250, foundation-bar). Slice-10 Overview/Progress **reopened → docs reconciled (6 files) → pending re-signoff**. Prototype 135/135, 0 pageerrors. Active: Slice 10 (Overview). Next blocking: owner re-signoff of Overview/Progress.

**2026-07-14 · WI-R5 erratum (Decision 251):** +1 decision. Progress bar P1 corrected (grounded=attested-only; two provenance states; load-bearing superset). Prototype R6 136/136. Canon erratum drafted.

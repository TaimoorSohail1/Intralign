# RB-045 — Proposal-resolution model + cross-surface sync + itemized atomic findings

- **Status:** ✅ CLOSED → **RATIFIED 2026-08-09 → DL-211** (`canon/decisions/DL-211_PROPOSAL_RESOLUTION_MODEL_AND_CROSS_SURFACE_SYNC.md`).
- **Raised:** 2026-08-09 (owner observation).
- **Trigger:** accepting an OSLO proposal *in the artifact* left the linked issue card open (double-work); a card carrying multiple proposals merged distinct findings into one prose row.
- **Scope (see DL-211):** proposals split into **build** (resolve the structural finding + may firm the band via reanalysis), **inference** (additive; grounding resolves only by verifying), **optional** (additive); cross-surface resolution sync (one finding, one resolution, only reanalysis resolves); multiple resolvers (all-accepted-to-close; keynote-backup needs requirement + task); itemized atomic finding rows (never merged); amends the `proposalsFoldedIntoRead` invariant.
- **Realization:** prototype (resolution sync + itemized rows + amended guard) + Slice 2 contract; guards `buildProposalResolvesFinding` / `inferenceProposalStaysAdditive` / `resolutionSyncedAcrossSurfaces` / `findingsItemizedNotMerged`. Verified via headless `_S10`.

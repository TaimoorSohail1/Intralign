# R2 Prototype Tech-Debt — Reviewed & Dispositioned (2026-08-06)

**Owner:** Idris · one-at-a-time review of prototype-behavior honesty debt (distinct from the backend-spec debt already enumerated in `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md`).
**Prototype:** `oslo-prototype-r2.html` · build green after fixes (`window._S10` = 57/57, 0 page errors).

Scope note: these are debts in the *prototype's own behavior* — they matter because the prototype is the R2 build reference, so a developer copying its logic would copy them. The comprehensive backend contract debt lives in the backend audit; this list is the honesty/state-model debt found by direct code inspection.

---

## Fixed in the prototype this session

**DL-204 — "Settled — needs a fix" lifecycle fork (owner-approved, built + verified).**
A flagged known-gap was landing in the **Resolved** tray while still weighing on a pillar. Now flagged items route to a distinct **"Settled — needs a fix"** folder with a **Fix-it** action that closes the gap via the existing re-analysis path (`fixFromFlag` → `_scheduleReanalysis`; only re-analysis resolves). Grounding credit retained. Guard: `needsFixFork`.

**Item 1 — flagging a known gap no longer firms Viability (fixed + verified).**
`_syncArtFromItem` was setting a flagged item's linked artifact statement to `prov='you'`, which drops it out of `artWeak` and can raise **Viability** — a named gap reading as a sounder plan. Now: a flagged item keeps its **item-level Grounding credit** (`grounded()` still counts `state==='you'`) but the linked statement stays **`inferred`**, so `artWeak`/Viability is not firmed. Weakest-gates honesty restored. Verified: flag → statement stays inferred, Grounding credited, Viability unchanged.

**Item 5 — first-run unlock is now latched (fixed + verified).**
`freezeOn()` = `firstRun && confirmCount<2`, `firstRun` was never cleared, and `withdrawItem` decrements `confirmCount` + calls `applyFreeze()` — so withdrawing an item after unlocking re-froze the workspace back into the onboarding gate. Fixed with a dedicated latch `_everUnlocked` (set when 2 calls are first reached): `freezeOn()` = `firstRun && confirmCount<2 && !_everUnlocked`. `firstRun`'s other roles (`.simple` 'other'-role UI, engagement signal) are untouched. Aligns with DL-L9 (activation is a one-way door). Guards: `freezeFormulaIntact` (updated), `unlockLatched` (new). Verified: unlock latches; a withdraw below 2 does not re-freeze.

---

## Deferred to R2 dev work (recorded as build constraints)

**Item 2 — Viability's +1 bump keys off a fix *count*, not what the fixes resolved → DEFERRED to Item 3.**
`viaLevel()` adds `if(_fixedCount()>=2 && lvl<3) lvl+1`. This is a symptom of the missing issue layer: item-level fixes don't clear `artWeak` (other inferred statements remain), so the bounded counter is the only way item-fixes move Viability. Patching the proxy now is throwaway once the real issue layer lands. **Build constraint:** *Viability must move from real per-issue weakness reduction, never a fix count.* Fixed as part of Item 3 (Phase A).

**Item 3 — pillars computed from hardcoded fixture counts, not the ratified DL-196/197 issue layer → CORE BUILD (State-1 Phase A).**
`grdLevel` (grounded-count 6/4/2), `viaLevel` (artifact-clearance fraction + the Item-2 bump), `adaLevel` (checkpoint count 3/2/1) — none use the severity-weighted issue layer DL-196 ratified (Viability←CAF issues, Adaptability←checkpoint issues, Grounding←false-confidence issues), and the DL-197 false-confidence issue type isn't implemented (0 identifier hits). This is not a prototype patch — it's the foundational **State-1 Phase A** three-pillar integrity engine already sequenced in `R2_STATE1_BUILD_PLAN.md`. Disposition: **build in R2 dev as Phase A**; Items 1/2/4 fold into it.

**Item 4 — band thresholds are absolute counts calibrated to the DevNorth fixture → BUILD CONSTRAINT (integrity model / audit OI-2).**
The 6/4/2, .6/.3, 3/2/1 cutoffs are sized to DevNorth's exact 6 items / 4 artifacts / 3 checkpoints and don't generalize (20 load-bearing details would read "Sound" at 6 grounded = 30%). No prototype change (single-fixture by design; hardcoded thresholds render correctly). **Build constraint:** *bands normalize to each plan's own size (grounded ÷ total load-bearing, checkpoint coverage ÷ needed, etc.), never absolute counts.* Implemented in Phase A.

---

## Summary
- **Fixed now (prototype):** DL-204 needs-a-fix fork · Item 1 (flag≠Viability) · Item 5 (latched unlock). Build green 57/57.
- **R2 dev (Phase A) with recorded constraints:** Item 3 (issue-layer integrity engine) absorbing Item 2 (Viability from real weakness reduction) and Item 4 (size-normalized bands).
- Backend-spec debt beyond these: see `R2_BACKEND_UNDERSPECIFICATION_AUDIT.md`.

*Recorded 2026-08-06 after a one-at-a-time owner review.*

# WI-R5 — Progress-panel foundation-bar fold-in (DL-111) — SLICE-10 REOPEN

**Opened:** 2026-07-14 · **Slice:** 10 (Overview / Progress panel) · **Status:** In review (docs reconciling to prototype)
**Trigger:** Owner-ratified **DL-111** — the Overview Progress panel adopts the reconciled "foundation-bar" design (record: `00_owner/decisions/records/DL-111-progress-panel-foundation-bar.md`).

## What changed in the prototype (source of truth)
The Overview **Progress panel** was rebuilt from the epistemic **class-ledger** ("From OSLO · Confirmed by you" sentence rows + load-bearing row) to a **foundation bar**:
- **Hero count of GROUNDED FACTS** = attested + derived, computed (`.pgx-big`).
- **Proportional foundation bar** — *Confirmed by you* (attested) + *From OSLO* (derived) solid segments sized to the real counts, with a **cool accent on Confirmed-by-you** echoing the Confidence ramp; a **set-apart provisional inferences tail** ("inferences your read leans on").
- **OPEN / CLOSED** work stats (Issues · Critical · Open questions / Resolved · Answered) with **severity red on Critical only**; neutral deltas.
- Reconciled with the Outcome Confidence panel (harmony pass): weight down, orange off-state, tail de-exiled.

## Guards (the doctrine, executable) — re-based, live
`_PGX_AMEND` suspension removed. Live self-check **135/135, 0 pageerrors** (both themes). New/adapted: `_assertPgxBarIsComputedFromRealCounts`, `_assertPgxColourDiscipline`, `_assertPgxBarStructure`; five ledger guards adapted, four retired as superseded (see DL-111).

## Reconciliation scope (docs → prototype)
Reconcile the **Progress/Overview** descriptions only; do not touch unrelated slice-10 content:
`frontend-ui.md` · `user-experience.md` · `success-criteria.md` · `edge-cases.md` · `open-items.md` · `product-detail.md` · `e2e-test-scenarios.md` · `product-data.md` · `workflow.md`.

## Re-signoff
Required for the **Overview/Progress portion of Slice 10** once docs reconcile. Rest of Slice 10 (Tiering, Reports, Plans) unaffected.

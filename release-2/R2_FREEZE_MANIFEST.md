# R2 Freeze Manifest — the frozen baseline handed to dev

**Framework 002 · §3.** The immutable state of the R2 product line at freeze. Every post-freeze change is measured against this and tracked in `R2_REFINEMENT_LEDGER.md`.

## Baseline

- **Frozen:** 2026-08-06 (owner: Idris) — consolidated nine-slice sign-off, `SIGNOFF.md`.
- **Signed slices:** 9 — `slices/01…09` (integrity engine · issue lifecycle · reanalysis/freeze · freemium/commitment · multi-outcome disclosure · collaboration · reports/export · feedback/telemetry · doctrine-guardrails/integration-map).
- **Acceptance register at freeze:** GT-01…GT-33 (+ async GT-A1…A3, `pending()`).
- **Reference prototype:** `oslo-prototype-r2.html`, `_S10` **59/59 green**, headless-verified. *(md5 not captured at freeze — future freezes should record it; the Refinement Ledger tracks md5 from the first post-freeze change forward.)*
- **Ratified decision corpus:** the R2 staged set at sign-off (DL-164…197 + DL-200–205 / DR-1…7), staged in `release-2/`; `main` decision_log frozen at DL-156 (R1).
- **Backend-capability register:** 23 capabilities (`OSLO_BACKEND_CAPABILITIES.md`).
- **Build source:** `release-2/` (single source of truth; the standalone `oslo-r2-build` snapshot is retired).

## Change control (from freeze)

Post-freeze refinements are governed by Framework 002 (DL-212): classified **neutral / additive / altering**, delivered as **push via labeled PRs**, with `altering` requiring the dev lead's PR approval (convention). All logged in `R2_REFINEMENT_LEDGER.md`.

## Durable invariants (never regress, any release)

only-reanalysis-resolves · only-verify-moves-Grounding · maturity-not-forecast · capacity-gated-not-judgment-quality · level≠trust · manufactured-confidence prohibition · decomposability / single-hue.

---

_Framework 002 realization (DL-212). Immutable — amend only by superseding manifest at the next freeze._

# Acceptance Suite — Doctrine Guardrails + Integration Map

The R2 build is gated by two artifacts, both authored in **Slice 9** (`../slices/09-doctrine-guardrails-integration-map.md`). This directory is the index; Slice 9 is the full spec (the map and the register live there in full so there is a single source of truth and no drift).

## 1. The FE↔BE Integration Map — the contract  (Slice 9 §2)

One continuous table binding every dynamic UI surface to `{Reads, Written-by (act), Changed-by (event)}`, across all nine slices.

> **A surface that is not in the integration map is not shippable.**

Build each surface to its row. New surfaces amend the map first. The spine rule holds across the whole map: **the only event that ever changes a band/resolution is reanalysis (`reanalysis.landed`).** A `—` in the Written-by column marks a read-only projection (a pinned no-write negative).

## 2. The doctrine-guardrail test register — the CI gate  (Slice 9 §3)

`GT-01 … GT-56` — every honesty invariant promoted from prose into a red-or-green assertion (GT-01…GT-33 = Slices 1–9; **GT-34…GT-44 = the DL-209 load-bearing / issue-classification twins**; **GT-45…GT-50 = the DL-210 CAF-boundary / alignment / escalation twins** — both authored in Slice 10; **GT-51…GT-55 = the DL-211 proposal-resolution / cross-surface-sync / itemized-card twins** — Slice 2; **GT-56 = start-here-guides-every-cleared-worklist-state** (next-move honesty); **GT-57 = every-declared-capability-is-simulated** (reverse SIM coverage — the #24 blind spot); GT-A1…A3 = async/latency). Types: **unit** (pure computation), **integration** (act→reanalysis→resolve flow), **negative** (fails if the wrong default is built; **pinned** = permanent), **lint** (string/copy scan).

> **A red suite blocks the build.** The register is a merge gate, not a report.

### The three enforcement classes (how each guard becomes a server assertion)

The 59 `_S10` client guards are the *reference oracle*, not the enforcement. Each gets a **server-side twin** that asserts the same invariant on the real backend — a `.toString().indexOf(...)` shape-check becomes a call against the real function/endpoint; a DOM query becomes a data assertion. The 59 names are preserved as test names so client guard and server twin stay greppably paired.

- **Flow / lifecycle guards** → integration tests across act→enqueue→reanalysis→resolve (e.g. `needsFixFork`, `mitigatedNeedsGrounding`, `unlockLatched`, `freezeFormulaIntact`, `surveyTriggerFiresOncePostActivation`).
- **Computation guards** → unit tests (e.g. `integrityIsWeakestGate`, `pillarLevelsInRange`, `bandsAreWordsNotNumbers`).
- **Structural / permission guards** → negative & pinned tests (e.g. the no-write projections, the never-metered exemptions, the feedback isolation boundary).

### The pinned negatives (red-if-violated forever)

Two classes must never regress:

1. **No-write projections** — roll-up, grounding-map, generated reports, feedback/survey have no write path to plan/finding/attestation/History. (`GT-14`, `GT-31`, `GT-06`)
2. **Never-metered exemptions** — the record, the reviewer/CRR loop, and Viewers consume no seat and hit no entitlement check. (`GT-02`)

Plus the spine: **only reanalysis resolves** (`GT-10`) and its symmetric honesty forks **needs-a-fix** (`needsFixFork`) and **needs-grounding** (`GT-33` / `mitigatedNeedsGrounding`).

3. **DL-209 load-bearing / classification pinned negatives** — **only verify moves Grounding** (`GT-35`), an **unmapped finding-type escalates, never default-classifies** (`GT-38`), the **critical floor is never suppressed** (`GT-43`), and **calibration never lowers the read's honesty for any segment or tier** (`GT-44`). Zero-data-segment-equals-global (`GT-42`) is pinned too.

4. **DL-210 CAF-boundary / escalation pinned negatives** — **dim is derived from structural target, never finding-type** (`GT-46`), **alignment is edge-keyed and outcome-traced** (`GT-47`), a **load-bearing model gap reads *incomplete*, never Fragile** (`GT-49`), and **no unassessed region ever takes a numeric/band penalty** (`GT-50`, unknown ≠ bad).

## 3. The nine DL-L landmines

`GT-01 … GT-09` each pin one of the nine "developer-builds-the-wrong-thing-by-default" traps (DL-L1…L9 in `../canon/audits/R2_BACKEND_UNDERSPECIFICATION_AUDIT.md`) with a negative/pinned assertion that fails loudly if the default (wrong) implementation is written — e.g. metering a Viewer, letting feedback write the read, or gating on `confirmCount` server-side.

## 4. Owner-open placeholders are quarantined

Owner-open numbers (reanalysis window, delegate matrix, tracker, readiness stats — see `../BACKLOG.md` → Owner-Open Decisions) are `pending()` tests that neither pass nor fail the gate until ratified. Building against a placeholder does not turn the suite red; shipping copy that hardcodes one should.

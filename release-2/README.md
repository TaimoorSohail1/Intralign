# OSLO / Intralign — R2 Build

Product-grill handoff package for the **R2 delta** build. This repo is the buildable specification: ten signed-off vertical slices, the reference implementation, the acceptance suite, and the full ratified decision canon that explains *why* every rule is what it is.

**Status:** all **ten** slices signed off (Slices 1–9 on 2026-08-06; **Slice 10 — the DL-209/DL-210 load-bearing sensitivity + issue-classification engine — on 2026-08-09**, owner: Idris). See [`SIGNOFF.md`](./SIGNOFF.md).
**Reference prototype build:** `_S10` self-check harness green at **77/77**, headless-verified (md5 `72068597`).

> **Source of truth — build from this `release-2/` tree.** This directory is the single canonical build source (owner decision 2026-08-09); the standalone `oslo-r2-build` snapshot is **retired/superseded** — do not build from it. The canonical prototype is `oslo-prototype-r2.html` at this root.

---

## What OSLO is (so the build stays honest)

OSLO reads a project manager's plan and shows where it is clear, aligned, and feasible — and where it is not — as a maturity **read**, never a success **forecast**. The whole product is a governed cognitive architecture with one non-negotiable spine:

> **OSLO advises, you decide. The read only moves when the plan or its evidence moves — never from a click alone.**

Concretely, that spine shows up everywhere as: *only reanalysis resolves* (an act enqueues; a batch re-read is the sole thing that changes a band), *maturity not forecast* (ordinal bands Fragile→Sound, never a 0–100 score), and *capacity is gated, judgment quality never is*. If a build decision seems to violate one of those, it is almost certainly wrong — check the canon before proceeding.

---

## How this repo is organized

| Path | What it is | How to use it |
|---|---|---|
| [`slices/`](./slices/) | The ten slice build designs — **the spec.** Each is self-contained: locked decisions, state/data/event models, honesty invariants, FE↔BE bindings, R1-reuse vs net-new, and acceptance criteria. Slice 10 is the DL-209/DL-210 load-bearing sensitivity + issue-classification engine. | Build against these. One slice per epic (see `BACKLOG.md`). |
| [`oslo-prototype-r2.html`](./oslo-prototype-r2.html) (+ [`PROTOTYPE_REFERENCE.md`](./PROTOTYPE_REFERENCE.md)) | The **canonical reference implementation** (DR-1) at this root — a single self-contained HTML file with an embedded `_S10` self-check harness. | The behavioral source of truth. When a slice doc and the prototype disagree, the slice doc's "prototype-vs-canon correction" note governs; otherwise the prototype is authoritative. |
| [`acceptance/`](./acceptance/) | The doctrine-guardrail acceptance suite: the FE↔BE integration map + the **GT-01…GT-50** test register (Slices 9 + 10). | Wire these as CI gates. A red suite blocks the build. |
| [`canon/`](./canon/) | The ratified **decision log** (`decisions/`), the **audits** that produced the slices (`audits/`), and **product references** (`product/`). | The "why." Trace any locked decision back to its DL/DR ratification here before overriding it. |
| [`BUILD_SEQUENCE.md`](./BUILD_SEQUENCE.md) | Dependency-ordered build plan across the ten slices (Slice 10 = Phase B+), plus the Phase-A prototype corrections. | Read this before scheduling work. |
| [`R2_VERTICAL_SLICE_STATUS_LEDGER.md`](./R2_VERTICAL_SLICE_STATUS_LEDGER.md) | The current implementation, UI/UX review, manual regression, functional-test, prototype-parity, and test-case status for every R2 slice. | **Read first whenever work resumes.** Update it in the same change that produces new evidence. |
| [`BACKLOG.md`](./BACKLOG.md) | Epics (one per slice) and derived tickets, each tagged with its acceptance criteria, the honesty invariant/guard it must satisfy, and any owner-open blocker. | Import into your tracker (Linear/Jira/GitHub Issues). |
| [`SIGNOFF.md`](./SIGNOFF.md) | The sign-off ledger and carried-forward items. | The scope contract. |

---

## Read this first: the integration map is the contract

Slice 9 §2 is the **consolidated FE↔BE Integration Map** — every dynamic UI surface bound to `{Reads, Written-by (act), Changed-by (event)}`. It is the keystone contract:

> **A surface that is not in the integration map is not shippable.**

Start there ([`acceptance/README.md`](./acceptance/README.md) → Slice 9). Build each surface to its row; the spine rule — *the only event that ever changes a band/resolution is reanalysis (`reanalysis.landed`)* — is enforced across the whole map.

---

## The acceptance suite: `_S10` guards → CI gates

The prototype boots **59 `_S10` self-checks** (`window._S10`, computed by `_s10SelfCheck()`); build is green when none is `false`. These are the *reference oracle*, not the enforcement. Slice 9 promotes each into a build assertion (`GT-01…GT-33`) with a **server-side twin** that asserts the same invariant on the real backend (a DOM/function-shape check becomes a data/permission check). The 59 guard names are preserved as test names so the client guard and its server twin stay greppably paired.

Two classes of assertion are **pinned negatives** — they must stay red-if-violated forever: the no-write projections (roll-up, grounding-map, generated reports, feedback/survey) and the never-metered exemptions (the record, the reviewer/CRR loop, Viewers).

To verify the reference prototype is green, see [`prototype/README.md`](./prototype/README.md).

---

## Build boundaries (what this package is and is not)

This is a **product** specification. It deliberately does **not** prescribe infrastructure: no database technology, framework, cloud/vendor, queue, model provider, or deployment choice is canonical here. Where a slice says "reuse R1," it means the R1 product behavior and its object/endpoint/event contracts — the engineering team owns the implementation substrate.

Prices, window timings, and similar tunables are **config placeholders** (marked `[owner]`/`[spec]` in each slice's "Open items"). They gate *copy and launch*, never the build — implement the mechanism, keep the number in config. The consolidated list lives in `BACKLOG.md` → Owner-Open Decisions.

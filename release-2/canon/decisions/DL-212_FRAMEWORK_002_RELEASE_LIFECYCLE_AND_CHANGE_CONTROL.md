# DL-212 — Establish Framework 002: Release Lifecycle & Change Control

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** A (governance doctrine — a process framework).
- **Framework 001** — AI drafts; only the owner ratifies. Dev lead (Hamza) aligned on the delivery mechanism + enforcement.
- **Basis:** owner directive — R2 delivered to dev and **frozen** from a product-design perspective; R2.x proceeds as **refinements** dev absorbs while building. Proposal + review: `release-2/GOVERNANCE_PROPOSAL_framework-002-release-lifecycle-and-change-control.md`.
- **Relationship:** **Framework 001** governs a single decision; **Framework 002** governs a release's lifecycle and, immediately, change control over a frozen release. F002 invokes F001 for every decision it produces.
- **Placement:** framework content = the ratified proposal (this session); canonical home `00_owner/frameworks/framework_002_release_lifecycle.md` at the next graduation (process doctrine, not product canon). Staged in `release-2/` until then.

---

## Decision

Establish **Framework 002 — Release Lifecycle & Change Control**:

1. **Lifecycle phases** — Open → Design → Freeze → Handoff → Build → Graduate → Retire, each with entry/exit gates, owner, and deliverables. R2.x lives in the **Build phase under Change Control**; Open/Freeze/Graduate machinery is skeletal until the next full release needs it.
2. **Freeze Manifest** — the immutable baseline captured at freeze (`R2_FREEZE_MANIFEST.md`): signed slices, GT register, reference-prototype md5, ratified decision set, backend-capability count. R2 baseline = the 2026-08-06 nine-slice sign-off.
3. **Three-class change model** — every post-freeze refinement is classified by impact on the dev contract (signed slices + GT register + interfaces + reference-oracle behavior): **Neutral** (no guard/slice change), **Additive** (extends without invalidating), **Altering** (changes an existing slice/GT/interface). Nothing lands without a classification.
4. **Delivery = push via labeled PRs** — each refinement is a PR labeled `neutral` / `additive` / `altering`. Neutral/Additive: dev notified, non-blocking, owner merges after the green gate. **Altering: the dev lead's PR approval is the re-handoff sign-off** — owner does not merge until approved, impact assessment attached. **Enforcement: convention to start** (owner discipline); a hard-enforcing GitHub Action is deferred until a miss warrants it.
5. **Refinement Ledger** (`R2_REFINEMENT_LEDGER.md`) — mirrors the merged-PR stream; the durable "everything since freeze" index, generated from labeled PRs, not hand-maintained.
6. **Durable Invariant Registry** — the doctrine spine (only-reanalysis-resolves · only-verify-moves-Grounding · maturity-not-forecast · capacity-gated-not-judgment-quality · level≠trust · manufactured-confidence prohibition · decomposability/single-hue) is re-asserted in every release's harness and **can never regress or be removed**, in any release. Release-acceptance guards are release-scoped; every guard carries its doctrine anchor.
7. **Traceability chain** — build artifact → ratified decision → backlog item; guard → doctrine anchor; demo value → Demo-Config source; enforced as a freeze/land gate.
8. **Draft → owner-confirms → capture.** Refinements iterate freely on the prototype (a draft phase); **nothing is classified, logged to the Refinement Ledger, or opened as a PR until the owner explicitly confirms the use case is complete.** Work-in-progress is invisible to the release process. (The one objective check — `_S10` green — runs automatically at capture, not as an owner checklist.)
10. **Build-Readiness Audit — the Freeze gate.** A passing audit is **mandatory before Freeze/handoff** (and run periodically during Build): it verifies nothing simulated is unbuildable. **Mechanical coverage** (no orphan `SIM:#NN` → capability → spec; every demo value sourced in Demo-Config; every `_S10` oracle ↔ GT twin; every surface in the FE↔BE map; traceability intact) + a **judgment under-specification review** (is each capability complete/unambiguous enough for dev to build without inferring?). Gaps are **escalated to the owner, never inferred**. Skill `build-readiness-audit`; the per-use-case inline version is `release-refine`'s back-end-synchronization step.

9. **Front-end ↔ back-end synchronization (the use case is the unit).** A prototype simulation is a promissory note for backend behavior. The **back-end specification required to support a simulation is designed as part of the same use case's prototyping — never deferred.** Every simulation a use case adds or changes carries its backend obligation, captured in the same pass: **SIM-tag** the simulated behavior (`/* SIM:#NN */`), register/extend the **backend-capability register** (`OSLO_BACKEND_CAPABILITIES.md`), source every new simulated **value** in the **Demo-Config register**, and extend the **slice / build-spec** that realizes it. A simulation is never captured without its backend obligation. Extends the standing *prototype-simulation ⇒ backend-obligation* rule and the `demoSimsTagged` gate.

## Realization

`R2_FREEZE_MANIFEST.md` (baseline) + `R2_REFINEMENT_LEDGER.md` (seeded with this session's post-freeze refinements) created now. Skills **`release-refine`** (classify + record + gate) and **`guard-add`** (author an invariant consistently: `_S10` oracle + GT twin + doctrine anchor + register row) to follow. Open/Freeze/Graduate skills built when the next full release reaches those phases.

## Doctrine preserved (unchanged)

Framework 001 remains the decision-governance loop. R2-isolation holds (never push to main; branch → PR → doc-integrity gate → owner merge). The honesty spine is the seed of the Durable Invariant Registry.

## Affected artifacts

`GOVERNANCE_PROPOSAL_framework-002-…md` (review record) · `R2_FREEZE_MANIFEST.md` · `R2_REFINEMENT_LEDGER.md` · at graduation: `00_owner/frameworks/framework_002_release_lifecycle.md`. Skills: `release-refine`, `guard-add` (to build).

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09**, dev-lead aligned. Staged in `release-2`; framework doc promotes to `00_owner/frameworks/` at graduation._

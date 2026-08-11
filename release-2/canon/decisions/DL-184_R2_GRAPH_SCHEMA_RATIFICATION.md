# DL-184 — R2 graph capabilities: the blocking schema/binding decisions, ratified

**Tag:** `R2/next-release`
**Framework:** 001 — Decision (Backlog → Proposal → **Decision** → Repository Change → Changelog).
**Basis:** owner direction 2026-07-24 — *"all of the remaining node and views work for graph work are for release 2 but
should be visible in the latest prototype. any decisions or approvals that would block building all capabilities (e.g.
schema changes, bindings, etc.) should be ratified now, such that development can proceed once they are assigned release 2
scope."*
**Status:** **Owner-ratified (Idris, 2026-07-24).** This packet moves the previously-**open, owner-gated** forks in
`DL-179 §7` (and the schema dependencies referenced by DL-180/181/183) from *open* to **ratified for R2 build**. AI is a
non-ratifying scribe under Framework 001; this records the owner's explicit ratification. **R1 canon (≤DL-156) FROZEN;**
all work lands on `release-2` / the appropriate backend line, withheld from `main`.

---

## 1. The directive, in two parts

1. **Prototype visibility (front-end, now).** Every remaining graph node/view capability is R2 scope and must be
   **visible in the latest prototype** — as a real view where the data supports it, and as a **clearly-flagged
   representative preview** where it does not yet (the D62/DL-179 honesty model). This is already how the Optimize
   deliverable view ships (DL-183) and how the grounding web's node identity is handled (DL-179).
2. **Unblock the build (backend/schema, now).** Any decision or approval whose *absence* would block building the full
   capabilities is **ratified now**, so engineering can proceed the moment the items are assigned R2 scope — rather than
   each waiting on a separate future approval.

## 2. What is ratified (the forks that were open in DL-179 §7)

All three are **approved to build for R2**. They were previously held as explicit owner decisions; they are now taken.

1. **Tier 1 — real statement nodes (front-end; no schema change).** Draw the grounding web from the live `ContextItem`
   set: every leaf a real statement, coloured by its real provenance state, grouped by real artifact/dimension, each
   node's click opening *that* statement's grounding chooser. Retires the representative-node-identity caveat and the
   generic tip. **Ratified — buildable on the `release-2` front-end line.**
2. **Statement lineage — add `derived_from` (reverses `DL-109 §5`).** Add an item-to-item lineage field to
   `ContextItem` and populate it in extraction, so the web can draw **real support edges** with uncertainty propagating
   up the chain (the literal dependency web, Tier 2). **Ratified as an R2 build target.** ⚠️ **This reverses a
   previously-ratified decision (`DL-109 §5`, which escalated item lineage out of scope and forbade approximating it).**
   The reversal is deliberate and owner-directed; the *anti-approximation* half of `DL-109 §5` still holds until the
   field is real — **no pseudo-edges in the prototype until lineage is genuine** (§4).
3. **Structured WBS + `issue → work-element` binding.** Parse the plan's real work-breakdown into
   workstreams/deliverables/tasks as objects, and bind both **statements** and **issues** to specific work elements
   (a `workstream_id`/`deliverable_id` on the issue, or equivalent). This single deliverable makes **two** things real at
   once: the Optimize **by-deliverable** view (DL-183 — retires its representative flag) and the grounding web's **real
   interior nodes** (DL-179 Tier 2). **Ratified as an R2 build target.**

## 3. What this unblocks (capability → dependency, now greenlit)

- **Grounding web 1:1 render** (DL-179) — Tier 1 on ratification #1; full literal dependency web on #2 + #3.
- **Optimize by-deliverable, live** (DL-183) — on ratification #3; the prototype's representative preview becomes the
  real view with no interaction-layer change (the element shape is already grouping-agnostic).
- **Node-level specific hover tips** (task #47 / DL-182) — grounding tips can name the specific statement/issue on
  ratification #1, with no change to the hover engine.
- **Real per-node linked-highlight in grounding** — the same exact 1:1 the Optimize lens already has, on #1/#3.

## 4. Doctrine that still binds (ratification is not a licence to fake)

Ratifying the *build* does not change what the *prototype* may show before the data is real. Until each dependency lands:

- **No approximated lineage / no pseudo-edges.** The anti-approximation rule of `DL-109 §5` outlives its scope reversal:
  real `derived_from` or nothing. A fake dependency web is strictly worse than the honest representative one (D62).
- **Representative stays flagged.** Any not-yet-real view (deliverable grouping, 1:1 identity) ships as a marked preview
  — banner, dashed marks, `rep`/`ids:[]`, no fabricated routing (DL-183, guarded).
- **Counts always reconcile; no severity/RAG/fill on the maturity layer; grounding stays a real attestation** — the
  DL-171/DL-181 guards are unchanged and hold.

## 5. Governance note

This is an owner ratification recorded by a non-ratifying scribe. One item (#2) **reverses a ratified decision**
(`DL-109 §5`); it is flagged here as consequential and taken on the owner's explicit direction. At R2 merge-back, fold
these ratifications into the canonical statements of `DL-109 §5` (now reversed re: lineage existence, retained re:
approximation) and `DL-179 §7` (forks closed → ratified). Instrument web/optimize comprehension alongside the activation
levers before graduating any 1:1 or live-deliverable render.

## 6. Scope

R2 divergence. Tier 1 and the front-end views are `release-2` work; the schema/extraction items (#2, #3) land on the
appropriate Alpha/backend line and feed back into `release-2` surfaces. R1 / `main` untouched.

---

*Recorded as a decision packet in the `release-2/` copy of record. Owner is the sole ratifier under Framework 001; this
records the owner's explicit ratification of the previously-open schema/binding forks so R2 development is unblocked.*

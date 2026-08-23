# DL-240 — The fixed understanding core is Intent · Constraints · Scope · Requirements — Context removed (amends DL-077 §1, DL-078 §2)

- **Date:** 2026-08-23 · **Status:** Ratified · **Decided by:** Idris (2026-08-23)
- **Class:** A

## Decision

**The fixed understanding core is Intent · Constraints · Scope · Requirements.**

**Context is removed as a planning artifact. Constraints replaces it.**

**Rationale (owner):** *Context as an artifact was too generalized. Constraints as an artifact held a
more specific boundary and clear purpose aligned with project understanding.*

## ⚠️ This AMENDS DL-077 §1. It is not the realization carve-out.

**DL-077 §1 reads, verbatim:**

> *"Fixed understanding core (domain-agnostic): **Intent · Context · Scope · Requirements** — the
> 'what / why / success' layer where the epistemic invariants and CAF live. **Fixed across all domains
> and methodologies.**"*

DL-077 does carry a carve-out — *"(the exact artifact-by-artifact boundary — e.g. the precise placement
of Requirements — is an engineering realization detail **to confirm**)"* — and it would be convenient to
file this under it.

⚠️ **It does not fit, and stretching it would be the more damaging choice.** The carve-out covers
**placement**; this is **membership** — one artifact removed, another added. A core described as *"fixed
across all domains and methodologies"* cannot lose a member by realization detail. **This record
therefore amends DL-077 §1 openly rather than claiming a carve-out that does not cover it.**

**DL-078 is affected in the same way.** It states that it *"confirms the fixed-core boundary"* and that
*"no ratified content superseded"* — both true when written, both now inaccurate on this point. **DL-078
§2's fixed-core enumeration is amended by this record.** ⚠️ **The rest of DL-078 stands**, including the
rule that profiles **may not remove** the core Requirements artifact.

## ⚠️ How this was found, recorded because the finding matters more than the fix

**The build has carried the new core for some time. Canon never did.** The divergence surfaced only
because the owner corrected an AI explanation of what an artifact is — **not because anything in the
repository detected it.**

**Measured 2026-08-23: ten files carry the superseded list**, including:

- **`00_owner/CANONICAL_GLOSSARY.md`** — ⚠️ **the DL-053 Disambiguation Register itself**, the artifact
  that exists specifically to stop terminology drift
- **`DL-077`** and **`DL-078`** — both ratified, both reading as current
- `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md`
- ⚠️ **`10_product/scope/OSLO_RELEASE_1_MASTER_SPEC.md` carries BOTH lists** and contradicts itself

⚠️⚠️ **`doc_integrity_check.py` passes on all of it — 1120 docs, 0 errors.** The glossary being wrong
about the product's fixed core is invisible to every gate in the repository.

**This is a concrete instance of the standing systemic finding:** *the build makes canonical decisions
by shipping* — not maliciously, but because **nothing compares the deployed artifact set to the
ratified one.**

## Obligations arising

1. **Owner — correct `CANONICAL_GLOSSARY.md`'s `PlanningArtifact` entry** to
   `Intent · Constraints · Scope · Requirements · WBS · Resources · Schedule`. ⚠️ **This should land
   with this record, not after it** — the glossary is what engineering is told to trust.
2. **Owner — sweep the remaining files** carrying the superseded list, and resolve
   `OSLO_RELEASE_1_MASTER_SPEC.md`'s internal contradiction. Batchable; not urgent.
3. **Engineering — a guard asserting the ratified fixed core matches the built one.** ⚠️ **This is the
   part that stops recurrence.** The check is small and exact: the prototype's `UND` is four keys, this
   record's fixed core is four artifacts — **assert they match, and RED-prove it by swapping one.**
   A guard that cannot fail is not a guard.
4. **Owner — a DL-053 Disambiguation Register entry for `Constraints`**, stating what it bounds and
   what distinguishes it from an `AttestedAssertion` of content type *Constraint*, which is a different
   thing under the same word.

## Where Context's content went — answered

**Context's content was DISTRIBUTED, where appropriate, across the other understanding artifacts.**
Nothing was dropped.

⚠️ **This is the difference between a removal and a redistribution, and it is why the change is
sound.** Context was too generalized to carry a boundary of its own; its concerns belonged with the
artifacts they actually qualified. **Constraints replaces it with a specific boundary and a clear
purpose aligned with project understanding** — the owner's stated rationale, recorded above.

**Consequence for the epistemic core:** the "why now / circumstances" concerns still have a home, so
DL-077's guarantee that the fixed core is *"the 'what / why / success' layer where the epistemic
invariants and CAF live"* is preserved. **The core changed membership without losing coverage.**

⚠️ **Not established here, and deliberately not inferred:** the artifact-by-artifact mapping of which
Context concerns went where. That is a realization detail, it is visible in the build, and it does not
change this decision. Recorded as unmapped rather than guessed.

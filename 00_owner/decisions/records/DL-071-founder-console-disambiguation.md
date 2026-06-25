# DL-071 — DL-053 Disambiguation Register: 'Founder Console' (Intralign Founder Console vs OSLO Observability Console)

- **Date:** 2026-06-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** `DL-053_FOUNDER_CONSOLE_ENTRY_DRAFT.md` (working dir); the DL-053 Disambiguation Register pattern; owner ratification via the Founder Console, 2026-06-18. Surfaced via E1 (`RECONCILIATION_FOUNDER_CONSOLE_TARGET.md`).
- **Layer:** Canonical terminology — additive Disambiguation Register entry (DL-053 pattern). Qualify-don't-redefine; no concept redefined; no doctrine/constitution change.

## Decision
Add a **"Founder Console"** row to the Disambiguation Register in `00_owner/CANONICAL_GLOSSARY.md`, qualifying the colliding bare word:
- **Intralign Founder Console** — the founder's single command surface (`intralign-founder-console`; GTM cockpit v2 + the build cockpit / Development-Readiness panel v3). This is the surface meant by unqualified prior uses; the Dev-Readiness panel renders here. Load-bearing for DL-067 (console-driven DL landing).
- **OSLO Observability Console** — *reserved name* for the OSLO product's observability/economics surface (`30_engineering/telemetry/OSLO_RELEASE_1_OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1`); **never** "Founder Console."

## Finding (scope correction vs. the draft)
The draft proposed (2) renaming the OSLO-product "Founder Console" surface and (3) correcting a host reference. **Verified unnecessary:** the telemetry spec contains no "Founder Console" (nor any "console") reference on `main`, and no `10_product` spec uses the term — every live canon usage refers to the Intralign Founder Console. The collision is **latent, not live**, so no product-spec rename is required; the register entry **reserves** "OSLO Observability Console" prospectively so the product surface cannot re-adopt the colliding name. The `PROPOSAL_FOUNDER_CONSOLE_DEV_READINESS_PANEL.md` host reference is a working-doc, not canon — no canon edit needed.

## Conditions / Authoring norm
Per the DL-053 lesson (the bare-word WARN produced ~314 false positives), enforcement stays a **regression guard on retired identifiers only** — qualifying "Founder Console" is an **authoring norm**, not an automated bare-word block ("founder console" appears too often in prose to gate mechanically).

## Supersedes / Amends
Additive to the DL-053 Disambiguation Register; supersedes nothing. Resolves the open `oaq-dl053-founder-console` owner action and closes the E1 reconciliation item.

## Provenance
Founder Console Decide log; ratified by Idris 2026-06-18. Realizes the DL-053 register pattern. Landed under the DL-065 number-at-merge records discipline.

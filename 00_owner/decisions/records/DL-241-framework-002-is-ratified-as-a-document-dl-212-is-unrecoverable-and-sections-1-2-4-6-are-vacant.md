# DL-241 — Framework 002 is ratified as a document; DL-212 is unrecoverable and sections 1, 2, 4, 6 are vacant

- **Date:** 2026-08-24 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision

**Framework 002 — Release Governance is ratified as a document, at
`00_owner/frameworks/framework_002.md`.**

⚠️⚠️ **This is a FRESH ratification, not a recovery — and that distinction is the whole record.**

## The finding

**Framework 002 has been cited by section number since 2026-08-14. It was never written.**

**Measured on `main`, 2026-08-23:**

- `00_owner/frameworks/` contained **only** `framework_001.md`, `framework_001A.md`,
  `framework_001A_decision_ready.md`.
- **`DL-212` — cited as Framework 002's founding decision — has no record file and no `decision_log.md`
  entry.**
- ⚠️ **Neither do `DL-227` (two trains) nor `DL-228` (corrective vs evolutionary)** — and **`DL-235`
  declares all three as dependencies while being itself ratified and landed on `main`.**
- The only F002 artifacts in `00_owner` were **DL-235**, which amends **§9 of a document that was not
  there**, and **DL-230**.
- ⚠️⚠️ **AND THE CITATIONS ARE NOT WHERE THE GOVERNANCE IS.** Measured per line:
  **`main` — the line §9 declares *the only delivery truth* — carries ZERO F002 citations.** Not one file.
  **The design line carries ~85** across nine sections: §8b ×18 · §8d ×16 · §9 ×13 · §8d-i ×11 · §7 ×9 ·
  §8c ×6 · §5 ×5 · §3 ×3 · §8c-i ×1. **The governance vocabulary exists only on a design branch.**

⚠️ **`doc_integrity` passes on all of it.** Nothing in the repository detects a framework cited ~85 times on one line,
zero on the other, and written on neither.

## Why fresh ratification rather than reconstruction

**DL-212's wording is not recoverable.** Reconstructing it from downstream citations is precisely how
**DL-162** came to carry its own *"back-reconstruction, not the authoritative original"* warning, and
**DL-231** set the governing precedent when the 2026-08-09 *engaged* wording proved unrecoverable:
**re-ratify fresh, and name it as a different act.**

**So: the rules as the project has been operating them are ratified fresh, and every section names the
evidence it was ratified from.**

## What is ratified

| section | content | evidenced by |
|---|---|---|
| **§3** | change classes — Neutral · Additive · Altering, and their gates. **A disputed class is Altering until ruled otherwise** | Freeze Manifest · DL-230 · DL-235 §9.2 |
| **§5** | capture — one Refinement Ledger row per change, with a fixed schema. **Capture is not delivery** | R2.1 Ledger header, in active use on both lines |
| **§7** | **Altering never batches.** A batched Altering change is an unreviewed one | remediation plan · ledger practice |
| **§8b** | ratification ripple, mechanically enforced — **a decision without a ripple section fails the PR** | Tier-1 audit check + `doc-integrity` step; **most-cited section — 18 on the design line, zero on `main`** |
| **§8c / §8c-i** | the Altering gate: code-owner review **blocking, not requested**; **an Altering PR must target `main`**, enforced in CI | `protect-main` ruleset |
| **§8d / §8d-i** | two trains; corrective vs evolutionary, **neither may take the other's path** | DL-235 §9.2 · Freeze Manifest |
| **§9** | two lines, one truth — `main` is the only delivery truth | **DL-235, carried in substance; DL-235 remains the record** |

## ⚠️ What is deliberately NOT ratified

**§1, §2, §4 and §6 are declared VACANT.** No citation of them in a Framework-002 context survives **on
either line**.

⚠️⚠️ **They must not be back-filled by inference.** If a future need arises they are ratified fresh
through Framework 001 — **never reconstructed from a citation.**

⚠️ **The numbering must not be closed up.** Renumbering to remove the gaps would **silently invalidate
~85 live citations on the design line** — the same class of failure this record exists to end.

## Ripple

1. **`20_handoff/R2.0_DEFECT_REMEDIATION_HANDOFF.md` §0** carries an inlined copy of the classification
   rules under an explicit sunset clause. ⚠️ **On merge of this framework, §0 is deleted and replaced by
   a citation.** If the two ever disagree, **the framework governs.**
2. **Every document citing `F002 §<n>` now resolves** — no change required to any of them.
3. ⚠️ **DL-212, DL-227 and DL-228 remain unrecorded.** This record does **not** manufacture them. It
   supersedes the *need* for DL-212 by ratifying the framework directly; **DL-227 and DL-228 remain open
   gaps whose substance survives only inside DL-235 §9.2.**

## ⚠️ The obligation this creates on the mechanism side

**A framework cited ~85 times on the design line, never cited on `main`, and never written on either,
is exactly what §8b's ripple check exists to prevent** — a ratification whose downstream obligations were never recorded.

**Owed, and not closed by this record:** a check that a cited framework or decision **resolves to a file
that exists**. `doc_integrity` passed on 1120 documents while F002 was missing, DL-212 was missing, and
two more of DL-235's declared dependencies were missing. ⚠️ **A citation that resolves to nothing should
fail a PR, exactly as a missing ripple section does.**

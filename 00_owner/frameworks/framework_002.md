# Framework 002 — Release Governance

**Zone:** `00_owner/frameworks/` — owner-governed. **Status: RATIFIED FRESH — see the ratification note.**

**Governs:** how a change to a release line is **classified**, **captured**, **gated** and **delivered**,
and the **branch topology** those rules run on.

---

## ⚠️⚠️ RATIFICATION NOTE — this is a FRESH ratification, not a recovery

**Framework 002 has been cited by section number since 2026-08-14 — and it was never written.**

⚠️⚠️ **AND THE CITATIONS ARE NOT WHERE THE GOVERNANCE IS.** Measured 2026-08-23, on the two lines
separately, because the difference is the finding:

| | Framework 002 cited? | `framework_002.md` present? |
|---|---|---|
| **`main`** — declared *the only delivery truth* (§9) | ⚠️⚠️ **ZERO files. Not one.** | no |
| **the design line** (`r2.1/rb126-deep-cap-doctrine`) | **~85 citations across nine sections** — §8b ×18 · §8d ×16 · §9 ×13 · §8d-i ×11 · §7 ×9 · §8c ×6 · §5 ×5 · §3 ×3 · §8c-i ×1 | no |

**So the governance vocabulary this project runs on exists ONLY on a design branch**, while the line
that is supposed to be the single source of delivery truth carries neither the framework nor a single
reference to it. ⚠️ **An earlier draft of this record claimed the citations were "across this corpus";
that was measured on the design line and is corrected here.**

**Also measured on `main`, 2026-08-23:**

- `00_owner/frameworks/` contained **only** `framework_001.md`, `framework_001A.md`,
  `framework_001A_decision_ready.md`.
- **`DL-212`, cited as Framework 002's founding decision, has no record file and no `decision_log.md`
  entry.** ⚠️ **Nor do `DL-227` (two trains) or `DL-228` (corrective vs evolutionary)** — and **DL-235
  declares all three as its dependencies while being itself ratified and landed.**
- The only F002 artifacts in `00_owner` were **DL-235** (which amends *§9 of a document that was not
  there*) and **DL-230**.

⚠️ **The wording of DL-212 is therefore NOT RECOVERABLE.** This document does not pretend to recover it.
**It is a fresh ratification of the rules as the project has been operating them** — the same act, and for
the same reason, as **DL-231's fresh re-ratification of *engaged*** when the 2026-08-09 wording proved
unrecoverable. **Reconstructing canon from downstream citations is how DL-162 came to carry its own
*"back-reconstruction, not the authoritative original"* warning; that is not repeated here.**

**Every section below names the evidence it was ratified from.** ⚠️ **Those sources are named in prose, not
linked — the release-line documents live on the DESIGN line and are not present on `main`, so a link
from this file could not resolve. That is itself worth noting: `main` is declared the only delivery
truth (§9) while carrying almost none of the release documentation.** ⚠️ **Sections with no surviving
evidence are declared VACANT rather than invented — see §10.**

---

## §1 — VACANT

⚠️ **No citation of `F002 §1` exists on either line.** Deliberately left vacant. See §10.

## §2 — VACANT

⚠️ **No citation of `F002 §2` exists on either line.** Deliberately left vacant. See §10.

---

## §3 — Change classes

**Every change to a release line carries exactly one class.** The class determines the gate.

| class | definition | gate |
|---|---|---|
| **Neutral** | no behaviour change, no guard impact, no data migration — strings, copy, dead tokens, comments, tooling that changes no output | standard PR + `doc_integrity`. **May be batched.** |
| **Additive** | adds or removes a field, signal or surface **without changing a judgment the user already sees** | own PR per item; may batch **only** if the items are independent |
| **Altering** | **changes a displayed judgment, a gate, or when something runs** | ⚠️ **its own PR. See §7.** Dev-lead gated per §8c |

**Classification is the author's claim and the reviewer's to reject.** ⚠️ **A change whose class is
disputed is Altering until ruled otherwise** — the conservative direction is the one that adds a gate,
never the one that removes it.

**Evidence:** the R2.1 Freeze Manifest (*"Framework 002 §3 + §8d"*) · the R2.0 remediation plan ·
`DL-230` · `DL-235` §9.2 (*"classified under §3 (Neutral/Additive/Altering)"*).

---

## §4 — VACANT

⚠️ **No citation of `F002 §4` in a Framework-002 context exists on either line.** The one apparent hit
was read in context and belongs to a different document's numbering. Deliberately left vacant. See §10.

---

## §5 — Capture

**Every captured change to a release line gets exactly one Refinement Ledger row on that line.**

The row carries: **date · what changed and why · class · train · PR/commit · what it traces to · guard
delta · reference md5 after · notes.**

⚠️ **Capture is not delivery.** A logged row is a record that a change happened; it does not by itself
put the change in front of anyone. Rows accumulate and are delivered per §8.

**Evidence:** the R2.1 Refinement Ledger header (*"Framework 002 §5 + §8d. Every captured change to the
R2.1 design line, one row each"*) and the row schema in active use on both lines.

---

## §6 — VACANT

⚠️ **No citation of `F002 §6` in a Framework-002 context exists on either line.** The two apparent hits
were read in context and belong to other documents' numbering. Deliberately left vacant. See §10.

---

## §7 — Altering never batches

⚠️ **An Altering change rides its own PR. It is never bundled with another change of any class.**

**Why, and it is not procedural fussiness:** an Altering change moves a judgment the user can see. If it
travels inside a batch, the review that would have caught it is spent on the batch, and the changelog
records a bundle rather than the alteration. **A batched Altering change is an unreviewed one.**

**Evidence:** the R2.0 remediation plan (*"Altering · each rides its own gated PR (F002 §7)"*) ·
the R2.1 Refinement Ledger practice · standing operating rule.

---

## §8 — Gates and delivery

### §8b — Ratification ripple, mechanically enforced

**A decision ratified without a ripple section fails the PR.** The ripple section names what the decision
touches downstream. ⚠️ **This is a Tier-1 audit check and a step in the `doc-integrity` workflow — not a
convention.**

**Evidence:** *"…is now a step in the `doc-integrity` workflow and a Tier-1 audit check (Framework 002
§8b) — a decision ratified without a ripple section now fails a PR instead of waiting to be noticed"* ·
**18 citations on the design line** — the most-cited section in F002, and **zero on `main`**.

### §8c — The Altering gate

**An Altering PR requires code-owner review, enforced by the repository ruleset `protect-main`.**

⚠️ **Approvals must be BLOCKING, not merely requested.** A PR that requests review without requiring it
has no gate. ⚠️ **An un-listed release path means GitHub requests no review, silently disabling this
gate — this is exactly how `release-2/` went unreviewed.**

⚠️ **A PR without a named requested reviewer is not delivered.**

### §8c-i — Altering targets `main`

⚠️ **An Altering PR must TARGET `main`.** **Ratified and enforced in CI.**

**Evidence:** *"§8c-i ratified: an Altering PR must TARGET `main` — and the rule is now ENFORCED IN
CI"* · `protect-main` ruleset.

### §8d — Two trains

**Two release lines run in parallel: a DELIVERY train (a frozen baseline being built) and a DESIGN train
(the next release under product design).** They exist so that development can complete a release without
obstruction from ongoing product design, and vice versa.

### §8d-i — Corrective vs evolutionary

- A **corrective** changes the frozen, delivered baseline. Classified under §3, gated per §8c, and
  **lands on `main`**.
- An **evolutionary** change is next-release design work. It lands **only** on the design line and
  reaches `main` **exclusively through freeze-and-promotion**.

⚠️ **No change may take the other's path.**

**Evidence:** `DL-235` §9.2 (which states DL-228's substance verbatim) · the R2.1 Freeze Manifest ·
the R2 Refinement Ledger.

---

## §9 — Two lines, one truth · `main` is the only delivery truth

**Ratified as DL-235 (Idris, 2026-08-19, on PR #227). Carried here in substance; DL-235 remains the
record.**

1. **`main` is the delivery/integration line and the only delivery truth.** One protected
   `design/release-<next>` branch isolates the next release's design work. **No long-lived delivery
   branch exists per release**; frozen baselines land on `main` and are marked by release tags.
2. **Corrective vs evolutionary** as in §8d-i, now with a branch topology.
3. **Promotion requires readiness evidence, complete** — the release's precondition register reads
   **N-of-N** · a **build-readiness audit at freeze with zero unresolved escalations** · the recorded
   state matrix **green at the frozen md5**, including the terminal-state journey · the **acceptance
   register synchronized** with the shipped guard set · an **owner freeze declaration naming the md5 and
   the tag**.
4. **Enforcement is mechanical.** Both lines protected; approvals **blocking** on both; an
   always-running `sdlc-policy` check enforcing branch/path/class topology; gate **reachability**
   verified, not assumed.
5. **Realization is engineering's** — rulesets, CODEOWNERS, CI, environments, migration — proposed and
   maintained via the `20_handoff/` seam. ⚠️ **This section fixes intent only. Ratify ≠ author.**

---

## §10 — ⚠️ Vacancies, and what must not be done with them

**§1, §2, §4 and §6 are VACANT.** No citation of them in a Framework-002 context survives **on either
line** — neither on `main` nor on the design line.

⚠️⚠️ **They are vacant, NOT reserved-and-forgotten, and they must not be back-filled by inference.**
Whatever DL-212 put there is unrecoverable. **If a future need arises for those sections, they are
ratified fresh through Framework 001 like any other canon — never reconstructed from a citation.**

⚠️ **Do not renumber.** The design line carries **~85 live citations** of §3, §5, §7, §8b, §8c, §8c-i, §8d,
§8d-i and §9. **Renumbering to close the gaps would silently invalidate every one of them** — which is
the same class of failure this document exists to end.

---

## §11 — What this framework does NOT cover

- **Framework 001** governs how canon is proposed, reviewed, decided and changed. F002 governs release
  lines. **Where they meet — a decision record that alters a release line — both apply.**
- **Realization** of any gate (CI, rulesets, CODEOWNERS) is **engineering's**, per §9.5.

---

## ⚠️ Standing obligation created by this ratification

**Every document citing `F002 §<n>` must now resolve against this file.** ⚠️ **The `20_handoff/`
R2.0 defect handoff carries an inlined copy of §3 under a sunset clause: on merge of this framework,
**that section is deleted and replaced by a citation.**

**And the finding that produced this document is itself the argument for the mechanism it describes:**
**a framework cited eighty times and never written is exactly what §8b's ripple check exists to
prevent** — a ratification whose downstream obligations were never recorded.

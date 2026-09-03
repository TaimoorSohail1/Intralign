# OSLO Identity, Role and Scope Model — V1

**Zone:** `20_handoff/interfaces/` — co-governed seam (DL-051) · **Capability #12** · **Framework 001**

**Status: REALIZATION AUTHORED — awaiting owner merge.** The owner ratified the **intent** on
2026-08-17 — rulings A2, B2, C1 and C2, recorded in the capability #12 proposal carried on the R2.1
design line (PR #217). That proposal is deliberately **not** cited by path: it lives on a release line
and this document lives on `main`, and a canon artifact must not depend on a release-line path.
This document authors the realization of that intent and proposes the policy text. It becomes canon on
owner merge through the `doc-integrity` gate, not before.

**✅ THE DECISION RECORD EXISTS: `DL-229` — Identity, role and scope model (capability #12)**, minted by
the owner **2026-08-18**. It names rulings **A2 · B2 · C1 · C2** and names this document as the
realization; it is the Framework 001 **Decision** step for this pair. *(When this branch was opened no
record existed, and this document said so rather than minting an id by inference — RB-099's defect. The
record was minted the following day; the id is cited here, the absence note it replaces is not restored.)*

**`DL-229` landed on `main` through PR #274 at `c1c7103`.** The Framework 001 sequencing dependency is
therefore discharged: the Decision now precedes this Repository Change. The record is cited by id rather
than by a release-line path so this main-bound artifact does not depend on the design line.

**This document supersedes nothing.** It **binds** existing ratified sources and closes the four items
Slice 06 §8 marks `[spec]`-open. Where a fact is already ratified elsewhere it is **cited, not
restated** — a second copy of a ratified fact is a stand-in waiting to diverge.

---

## 1. Normative sources this model binds

| Source | Provides | Status |
|---|---|---|
| **DL-049** (2026-06-05) — `10_product/scope/OSLO_CAPABILITY_MATRIX_V2.md` §337 | single `Principal` object, `type: reviewer \| user`; email-verified Reviewer scoped to shared items; in-place `reviewer→user` promotion, **provenance-stable, scope-preserving** | ratified |
| **P7** — Virality Audit 001, §339 | share links read-only by default, **scoped to the shared item only**, owner-revocable at any time, **default expiry (tunable, Calibration §4g)**; private links require an authenticated `Principal` | ratified |
| **R1 API contract** §3 / §14 — `20_handoff/interfaces/RELEASE_1_API_CONTRACT_SPECIFICATION_V1.md` | bearer token, session/JWT → `user_id`; role-gated commands `owner\|admin\|member`; least-privilege defaults | ratified |
| **Slice 06** L1/L2/L8, INV-1 | external scope hard-enforced; delegate sees the full read and co-grounds; owner-vs-delegate matrix display-only this release (DL-L8) | ratified |
| **GT-08** (pinned) | scoped token authorizes `{question, source}` ONLY; anything else → 403 | pinned guard |
| **GT-17** | a stale/re-routed scoped link 403s; scope is single-question-bound | guard — **see §6, pinning owed** |

⚠️ **R1 API contract §14 explicitly excludes the external reviewer** — line 57: *"No external-reviewer
role exists (governance/future — excluded)"*; line 312 lists external-reviewer identity as out of
scope. It is therefore bound here **for workspace-role gating only**. The external reviewer is
governed by DL-049 + P7 + §4 below. Binding #12 to §14 alone would have left the one hard-enforced
boundary uncovered.

⚠️ **On the record, because it explains the gap rather than excusing it:** DL-049's own note states
*"Recipient-experience build (auth, view/respond, promotion, convert-moment) = **Release 2
fast-follow** per CHG-064; R1 generates + measures invitations only."* R1 deliberately deferred this
build to R2. The specification was never missing; the build was scheduled and not done.

---

## 2. The model has three axes, not one enum (ruling A2)

The four vocabularies previously in circulation answer three different questions. They are declared
here as **orthogonal axes**. A principal holds exactly one value on each.

### Axis 1 — Identity class (`Principal.type`) · per person, global

| Value | Meaning |
|---|---|
| `reviewer` | email-verified, scoped to shared items only, no workspace membership |
| `user` | full authenticated account |

Source: DL-049. Promotion `reviewer → user` is **in-place, provenance-stable and scope-preserving**.

### Axis 2 — Plan relationship · per `(principal, plan)` pair

| Value | Meaning |
|---|---|
| `owner` | owns the outcome and its read |
| `delegate` | sees the full read and co-grounds (Slice 06 L2) |
| `external` | holds a scope token to one question; **hard-enforced** (Slice 06 L1 / INV-1, GT-08) |

**This axis is per-plan.** A principal may be `delegate` on plan A and hold no relationship to plan B.
This is the distinction a flat enum could not express, and it is why #11 (multi-project) depends on
this axis being pair-keyed rather than principal-keyed.

### Axis 3 — Workspace role · per `(principal, workspace)` pair

`owner | admin | member` — gates privileged commands (archive project, revoke share). Source: R1 API
contract §14. **Orthogonal to Axis 2:** workspace `admin` conveys no relationship to any individual
plan and grants no attestation authority.

### The prototype's `owner | pm | other` is a display projection, not a fourth vocabulary

It renders Axis 2 for the current plan: `owner→owner`, `pm→delegate`, `other→external`. It is a **view
concern** and must never be persisted or used for authorization.

### Mapping table (normative)

| Axis 2 value | Requires Axis 1 | Typical Axis 3 | Sees | May attest (§3) |
|---|---|---|---|---|
| `owner` | `user` | any | full read | **yes** |
| `delegate` | `user` | `member`+ | full read | **yes** (attributed) |
| `external` | `reviewer` or `user` | none required | `{question, source}` only | **no** — evidence only |

---

## 3. Attestation authority (ruling B2)

**Doctrine unchanged and reaffirmed:** only a verify moves Grounding (GT-35, pinned). This section
settles *whose* verify counts and *what provenance class* it carries — nothing else.

### 3.1 The rule

1. **`owner` grounds.** Provenance class `Confirmed by you`.
2. **`delegate` grounds.** Provenance class `Confirmed by {name}` — attributed, never anonymous.
   Slice 06 L2 is realized, not narrowed.
3. **`external` does not ground.** A scoped reviewer's answer is captured as **attributed evidence**
   (`addr.kind='confirm'`, `attestedBy={principal}`) and enters the read as evidence awaiting an
   owner-side act. Grounding requires that act.
4. **OSLO's own inference never grounds.** Provenance class `From OSLO`. Unchanged; stated so the
   three classes capability #2 names are all accounted for here.

### 3.2 Why the boundary sits where it does

The `external` boundary is already **hard-enforced** by GT-08's 403. Placing the grounding boundary at
the same line means scope enforcement and attestation authority are **one fact**, guarded once. Under
the alternative (B1) they would be two facts that must be kept in agreement, and this repository's
recorded experience is that two facts kept in agreement by intention drift.

### 3.3 Promotion clause (required by DL-049)

**An attestation's provenance class is fixed at the moment of the act.** When a principal is promoted
`reviewer → user`, attestations they made as a scoped reviewer **do not upgrade** — evidence recorded
under §3.1(3) stays evidence, and does not retroactively become grounding. This is what DL-049's
*"provenance-stable"* requires, made explicit because the failure mode is silent.

### 3.4 Interface obligations for the evidence path (raised in review 2026-08-19)

⚠️ **An "evidence only" rule is not sufficient on its own.** §3.1(3) states *what* a scoped reviewer's
answer is — attributed evidence, not grounding — and says nothing about the shape that carries it, so a
later implementation could satisfy this section's letter and still treat submission as grounding. The
following are **obligations on that seam**. Command and event names, transport and storage are
**engineering's to author** and return through this seam: **ratify ≠ author.**

An evidence submission from a scope-token principal must carry, and the server must enforce:

1. **Request identity** — the `review.requested` id the token was minted against. Not the plan, not the
   finding: the request.
2. **`{question, source}` binding, re-checked AT WRITE TIME** — the pair §4.2 binds the token to. A token
   valid for question A may not submit against question B.
3. **Actor principal** — the attributed identity recorded in `attestedBy`. **Never anonymous**, per
   §3.1(2)'s standard applied to the evidence class.
4. **Attestation version** — evidence is append-only; re-submission creates a new version rather than
   mutating the prior one, so §3.3's promotion clause has something stable to fix provenance to.
5. **Idempotency key** — a retried submission must not produce a second attestation. Duplicate evidence
   **inflates what the owner reads as independent corroboration**, which is a false-confidence surface,
   not a data-hygiene nicety.
6. **Expiry and revocation re-checked at write, not only at read** — a token that expired or was revoked
   between opening the link and submitting **must 403**, under §4.6's disclosure limits.
7. **The owner-side grounding act is a SEPARATE, LATER command** by an Axis-2 `owner`/`delegate`
   principal, referencing the attestation id. **No submission path may produce a Grounding state
   change**, whatever its payload.

**The guard below is what makes (7) falsifiable rather than declarative.**

### 3.5 Proposed guard (not authored here)

> **`attestation-authority-matches-enforced-scope`** — the set of principals whose act can move
> Grounding is exactly the set with Axis-2 ∈ {`owner`, `delegate`}; a principal holding a scope token
> can never produce a state change that moves the band. Negative, pinned. RED-prove by having a
> scoped-token principal attempt a grounding act and asserting the band does not move.

⚠️ **Not written into the acceptance register by this document.** The register lives on the delivery
line, which takes corrective changes only, dev-lead gated (F002 §8d). Routed as a follow-on.

---

## 4. Scope-token contract (rulings C1, C2)

### 4.1 Shape

A **scope token** is minted on `review.requested` when `scope='scoped'` (Slice 06 event table). It
authorizes read of **`{question, source}` and nothing else**; any other resource → **403**. This is
access control, not display filtering (GT-08, pinned).

### 4.2 Binding

**Single-question-bound.** One token authorizes exactly one review request. It conveys no access to
the plan, the read, other findings, or other questions.

### 4.3 The token permits ONE narrowly scoped mutation, and nothing else (raised in review 2026-08-19)

⚠️ **P7 makes share links read-only by default; §3.1(3) lets a scoped reviewer submit evidence. Left
implicit, the contract was ambiguous about whether the token authorizes a mutation at all.** It does —
that is the review-request exception ruling B2 created — and it is bounded here rather than inferred:

- **One capability, named:** *submit evidence against the bound request.* Not general write access, and
  **it does not widen read by one byte** — §4.1's *"`{question, source}` and nothing else"* governs the
  response path identically.
- **Every other mutation is `403`**, on the same access-control basis as an out-of-scope read (GT-08,
  pinned) and under §4.6's disclosure limits. There is no second 403 semantics for writes.
- **It cannot move the band** — §3.4(7) and the §3.5 guard. This states in *access-control* terms what
  §3 states in *provenance* terms; they are one boundary seen from two sides, which is the shape §3.2
  already argues for.
- **It expires and revokes with the token**, re-checked at write time per §3.4(6), so read-expiry and
  write-expiry cannot drift apart.

⚠️ **Left to engineering, deliberately:** whether the response rides the *same* token with a distinct
verb, or a paired write-scoped credential minted alongside it. Both satisfy every obligation above.
**The boundary is fixed; the carrier is not.**

### 4.4 Expiry (ruling C1)

A token **carries a default expiry**, owner-revocable at any time (P7).

⚠️ **The TTL value is deliberately not stated here.** No ratified value exists in canon —
`00_owner/OPEN_TBD_REGISTER.md` records the <60-second Time-to-First-MRI as the *one* ratified numeric
target. The value is **tunable configuration**, resolved at calibration per Calibration §4g, and is
**quarantined the way `N_MIN_FOR_SOUND` is**: the contract is complete without the constant, and a
number invented to fill the blank would be the defect Tier 1 finding 3 raised against `WEEKS = 8`.

**Implementation obligation:** the TTL must be read from configuration, never compiled in. A hard-coded
expiry satisfies this section's letter and breaks its purpose.

### 4.5 Re-issue on re-route (ruling C2)

Re-routing a question to a different reviewer **revokes the existing token and mints a new one**. The
prior link is stale and returns **403**. This ratifies what GT-17 already asserts — canon catches up to
the guard rather than the guard being loosened to match an unwritten spec.

### 4.6 Stale-link 403 copy

The 403 surface must state, without disclosing anything scoped: that the link is no longer active,
that this is expected rather than an error on the reader's part, and how to obtain a current link
(ask the person who sent it). It must **not** reveal the question, the source, the plan, the outcome,
or whether the underlying request still exists — the last of these because existence is itself scoped
information.

*Exact wording is a copy task, not a contract term, and is owed alongside the surface.*

---

## 5. What this closes — POLICY closure, which is not ENFORCEMENT completion

⚠️ **Corrected 2026-08-19 after review, and the correction is the substance.** This table previously read
as though these items were *done*. They are **decided**. Every row below closes a **policy** question and
not one asserts enforced behaviour, because **GT-17 is neither pinned nor quarantined and the §3.5 guard
does not exist** (§6). **A freeze must not be able to read a policy document as completed enforcement.**

| Item | Was | **Policy — closed** | **Enforcement — still owed** |
|---|---|---|---|
| **#12** Identity, roles & access | NOT BUILDABLE AS SPECIFIED | auth bound (DL-049 + P7 + §14), axes declared, token shaped | §3.5 guard + server twin · GT-17 pinned |
| **#2** Attestation ledger | blocked on provenance class for another person | §3.1 gives all three classes + §3.3 stability | §3.4 is an obligation set, not a built contract |
| **#3** Reviewer round-trip | blocked on scope-token shape | §4 complete | write-path 403 semantics and write-time expiry re-check unbuilt |
| **#4** Evidence-vs-comment | blocked on the identity directory | Axis 1 + Axis 2 published | no guard distinguishes evidence from comment at the boundary |
| Slice 06 §8 `[spec]` items | 4 open | **0 open as SPEC questions** — retire with an LD-3 reconciliation clause (the pattern Slice 07 used for #10) | the retirement edit is delivery-line, dev-lead gated |
| Delivery-line backlog row **R2-S6-1**, marker `⛔ token shape/TTL` | blocker | shape ratified; TTL deliberately unvalued (§4.4) | `⛔` clears on merge **of the delivery-line edit**, not of this document |

**Read both right-hand columns or neither.** Policy closed with enforcement owed is a legitimate state.
Policy closed *reported as* enforcement complete is how a freeze declares on paper.

## 6. What this owes, and to whom

1. **GT-17 must be pinned or quarantined.** It is currently neither, while asserting behaviour §4.5
   now ratifies. Per Slice 09 §4 a guard resting on an owner-open item belongs in `pending()`; that
   item is no longer open, so **pin it**. Delivery line, dev-lead gated.
2. **The §3.5 guard** — new GT, needs a number and a server twin.
3. **Slice 06 §8** — retire the four `[spec]` markers with a reconciliation clause; **delivery-line
   backlog row R2-S6-1** — clear `⛔`. Both delivery line, corrective, dev-lead gated.

## 7. What this does NOT close

**#11** still has no slice, epic or build-sequence slot — Axis 2 being pair-keyed makes multi-plan
*expressible*, not *built*. **#5, #6, #19, #23 and #25** are untouched. The **delegate role/access
matrix stays display-only this release** per DL-L8 / R2G4 — §3.1(2) grants delegates attestation
authority, which is an *attestation* rule, not the enforced permission matrix, and does not
un-defer R2G4.

---

*Framework 001 — Backlog → Proposal → Review → **Decision** → Change → Changelog. Owner ratified the
intent 2026-08-17 (A2 · B2 · C1 · C2); this document authors the realization and proposes the policy
text. Not canon until merged. No fact was restated where it could be cited, and no number was invented.*

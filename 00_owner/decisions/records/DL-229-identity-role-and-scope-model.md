# DL-229 — Identity, role and scope model (capability #12)

**Status: ✅ RATIFIED — id DL-229 minted by the owner 2026-08-18.** (Was an unnumbered draft; the id assignment is recorded in the session Ledger.)


⚠️ **The realization is referenced without its `.md` extension on purpose.** It is main-bound canon on
PR #218 and is **not a file on this branch**; writing it as a link would assert a resolution that does not
hold from where this draft is read. Same condition as RB-094/099/106/107/108/111 — recorded here rather
than worked around.


**What it records.** The owner ratified the **intent** on 2026-08-17 (rulings **A2 · B2 · C1 · C2**).
`20_handoff/interfaces/OSLO_IDENTITY_ROLE_AND_SCOPE_MODEL_V1` (PR **#218**) authors the realization.
This record is the Framework 001 **Decision** step for that pair.

---

## 1 · Decision

**OSLO's identity model is three orthogonal axes, not one role enum. Attestation authority and scope
enforcement are one fact, guarded once.**

| Axis | What it answers | Values |
|---|---|---|
| **1 — Account kind** | what the principal *is* to the system | `user` · `reviewer` (scope-token holder) |
| **2 — Plan relationship** | what they are *to this plan* — **per-plan**, so a principal may be `delegate` on plan A and hold no relationship to plan B | `owner` · `delegate` · `external` |
| **3 — Workspace membership** | organisational placement | `member` and above |

**Attestation authority follows Axis 2, and only Axis 2.** `owner` and `delegate` may move Grounding;
`external` may not, and a scope-token holder never can.

- **`delegate` grounds, attributed** — provenance class `Confirmed by {name}`, never anonymous.
- **An attestation's provenance class is fixed at the moment of the act.** Promotion `reviewer → user`
  does **not** upgrade attestations made while scoped. Evidence keeps the standing it was recorded under.
- **A scope token authorizes `{question, source}` and nothing else.** Any other resource is `403`. This is
  **access control, not display filtering** (GT-08, pinned).
- **Re-routing revokes and re-mints.** The prior link returns `403` — canon catching up to what GT-17
  already asserted, rather than the guard being loosened to match an unwritten spec.
- **The token's TTL is tunable configuration, deliberately unvalued here.** It must be read from config,
  never compiled in. A hard-coded expiry satisfies the letter and breaks the purpose.

## 2 · Why — the shape this replaces

The audit found #12 **NOT BUILDABLE AS SPECIFIED**, with **four role vocabularies live and unmapped**.
The tempting fix was one enum reconciling them. That would have been wrong, and the reason is the
interesting part: **the four vocabularies were not four names for one thing.** They were answering
different questions — what someone *is*, what they are *to a plan*, and where they sit organisationally.
Collapsing them into one enum would have produced a vocabulary that could not express "delegate on plan A,
nothing on plan B", and the gap would have reappeared as special cases.

**Binding attestation authority to the same axis that scope enforcement already uses** is the load-bearing
half. Two rules kept in agreement by discipline drift; one fact guarded once cannot.

## 3 · Scope — what this does and does not settle

- It makes multi-plan **expressible** (Axis 2 is pair-keyed). It does **not build #11** — no slice, epic
  or build-sequence slot exists.
- The **delegate role/access matrix stays display-only this release** per DL-L8 / R2G4. §3.1(2) grants
  delegates *attestation* authority, which is not the enforced permission matrix and does not un-defer R2G4.
- **#5, #6, #19, #23, #25 are untouched.**
- The TTL **value** is quarantined, not decided.

## Graduation ripple

- **Main-canon documents touched:** `20_handoff/interfaces/OSLO_IDENTITY_ROLE_AND_SCOPE_MODEL_V1`
  (the realization itself) · `RELEASE_1_API_CONTRACT_SPECIFICATION_V1` §3/§14 (bound, not amended — the
  external reviewer is explicitly excluded at §14 and this model states why that gap exists rather than
  papering it) · Slice 06 §8 (its four `[spec]` markers retire) · the capability register entry for #12.
- **Amends / extends an earlier decision:** ⚠️ **extends DL-049** (auth) and **binds** it to the reviewer
  case DL-049's own note flagged. Supersedes nothing.
- **Class:** EXTEND.

⚠️ **This record's ripple is unusual and the reason is worth stating:** the realization already lives on
`main`, so there is no later "graduation" event at which this ripple fires. The section is written anyway,
because DL-220 requires the question to be *asked at ratification* — and an empty answer given for the
right reason is not the same as an answer nobody sought.

## 4 · Five outputs (Framework 001)

- **Findings.** Four role vocabularies were live and unmapped; #12 had no authentication spec at all; the
  scope token was asserted by two guards (GT-08, GT-17) and specified nowhere.
- **Concerns.** The model is expressible ahead of being enforced — Axis 2 supports multi-plan that #11 does
  not build, and the access matrix stays display-only. Recorded so a reader does not mistake expressible
  for shipped.
- **Dependencies.** DL-049 · DL-051 (zone ownership — `20_handoff/` is the co-governed seam) · DL-L8 / R2G4
  · Slice 06 L1/L2/L8 · GT-08 · GT-17 · Calibration §4g (where the TTL resolves).
- **Recommendation.** Ratify, assign a DL id, merge PR #218 through `doc-integrity`.
- **Status.** **DRAFTED, NOT RATIFIED.** Owner assigns the id and ratifies.

## 5 · What ratification does not discharge

Four items the realization owes, **all already tracked** — items 1–4 of **RB-106**, delivery-line and
dev-lead gated, held until the release stack clears:

1. Pin GT-17 (or quarantine it) — it asserts what §4.4 now ratifies and is currently neither.
2. Number the `attestation-authority-matches-enforced-scope` guard and write its server twin.
3. Retire Slice 06 §8's four `[spec]` markers with an LD-3 reconciliation clause.
4. Clear delivery-line backlog row `R2-S6-1`'s `⛔ token shape/TTL` marker.

---

*Drafted by an AI session 2026-08-17 from PR #218's artifact and the rulings it cites. AI may analyse and
recommend — never ratify, never mint an id. Every clause above is traceable to a section of the realization
or to a source it binds; no fact was restated where it could be cited, and no number was invented.*

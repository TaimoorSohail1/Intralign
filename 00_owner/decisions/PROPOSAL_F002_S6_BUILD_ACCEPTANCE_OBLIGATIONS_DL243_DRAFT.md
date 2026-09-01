# Proposal / Disposition (DRAFT) — DL-243: Framework 002 §6 — Build Acceptance Obligations

> **Status:** **DRAFT · Pending Owner Ratification** — AI-drafted recommendation; **ratifies nothing.**
> Per `00_owner` `CLAUDE.md`: AI may analyze, check consistency and recommend — **never ratify or author
> canon.** Every clause below is a proposal for the owner to accept, amend or reject.
>
> **Proposed Decision ID:** **DL-243** · **Date drafted:** 2026-08-30 · **Layer:** Canon / framework.
> MEASURED-BY: `python3 tools/dl_records.py next` → `DL-243`. ⚠️ That tool warns its ceiling (242) comes
> from a **citation** rather than a record — DL-242 is real but rides open PR #245, so **re-run before
> landing.**
>
> **Origin:** `20_handoff/RELEASE_CYCLE_GAP_ANALYSIS_2026-08-30.md` (12 gaps) → owner rulings captured
> 2026-08-30 → this disposition. **Realizes owner ruling 1.**
> **Affects:** `00_owner/frameworks/framework_002.md` — fills **§6 (VACANT)** and amends the **Governs**
> line. **No existing section is renumbered, redefined or removed.**

---

## 1. Problem

**No framework governs the application.** Framework 002 §11 and §9.5 place realization with engineering
(*"rulesets, CODEOWNERS, CI, environments, migration"*), and DL-235 ratified engineering-owned SDLC.
Framework 001's objects are Frameworks, Proposals, Decisions, Backlog and Changelog entries. **Neither
says what a build must prove before the owner can accept it.**

That absence has a measured cost. On PR #248 — 990 files, +186,990/−495 — three document gates passed
in ≤15s while `OSLO application quality gates / verify` read **Cancelled after 75m**, and the PR
remained mergeable. The accompanying validation report asserted *"8 sections passed, 2 partial, 0
failed"* on 2026-08-28; a build-readiness audit of the same staging app on 2026-08-29 found **3
blocking** defects. Both cannot be right, and nothing in canon adjudicates between them.

⚠️ **One failure shape recurs across all three subsystems: a check that cannot evaluate its subject
reports success.** A test constructed so it cannot fail (`test_issue_identity.py` — one test guards
cross-run identity and both fixtures share the default `evidence_refs`, awarding the matcher's +0.15
bonus automatically); a validation narrative that names no command; and a scheduled governance check
that returns SKIP-OK because `main` carries no line pointer (RB-076). **Skip-as-pass, three times.**
The repository has already mechanized against this shape twice — `no_hardcoded_release_line.py` and
`report_measurement_check.py`. §6 states the rule those mechanisms enforce, so it stops being folklore.

---

## 2. Why §6 of Framework 002, and not Framework 003

**Permitted by §10, and only by this route.** *"If a future need arises for those sections, they are
ratified fresh through Framework 001 like any other canon — never reconstructed from a citation."*
This proposal reconstructs nothing; it ratifies fresh, and says so.

**Why not a new framework.** F002 already owns *classified · captured · gated · delivered* for a
release line, and §9.3 already enumerates promotion evidence — this is that question one level up. A
peer framework would create a second home for release rules with nothing arbitrating between them,
which is the drift that produced G4 and G11. Standing rule: **extend, don't mint.**

**Why §6 and not §1, §2 or §4.** ⚠️ **Owner's call — this is placement, not substance.** §6 sits
between **§5 Capture** and **§7 Altering never batches**, immediately before the gates-and-delivery
machinery, so the reading order becomes *classify → capture → **what a build must prove** → gate →
deliver*. §4 would place acceptance before capture; §1/§2 would strand it before change classes exist.
**Do not renumber** — the design line carries ~85 live citations of the existing sections.

---

## 3. Proposed text — Framework 002 §6

> ### §6 — Build Acceptance Obligations
>
> **What a build must prove before it may be promoted.** These are **obligations, not
> implementations.** How they are realized — CI topology, tooling, tiering, test frameworks — is
> engineering's under §9.5 and DL-235. This section states what must be true; it never states how.
>
> **§6a — An unfinished gate is not a passed gate.** A build whose software quality gate did not
> complete has not satisfied it. Cancellation, timeout and error are indistinguishable from failure
> for acceptance purposes.
>
> **§6b — Skip is not pass.** A check that cannot evaluate its subject must **fail**, not skip. A
> skip is legitimate only where the subject genuinely does not exist for that change; it is never
> legitimate where the subject exists and the check could not reach it.
>
> **§6c — Every doctrine invariant realized in software carries a test that fails when the invariant
> is violated.** A test that cannot fail is not a test. Invariants are enumerated in the acceptance
> register; each requires a server-side twin exercising the violating case, not only the honoured one.
>
> **§6d — Validation evidence names what produced it.** Every pass or fail claim in a release
> validation carries `MEASURED-BY:` (the command or gate run) or `NOT-MEASURABLE:` (why not). A
> narrative verdict that names nothing is not evidence. Human observation remains legitimate evidence
> under `NOT-MEASURABLE:`.
>
> **§6e — A build carries a resolvable identity.** Any build reachable by a user exposes an identity
> that a later reader can resolve to the source that produced it. **An unidentifiable build cannot be
> audited, rolled back to, or reasoned about after an incident**, and therefore cannot be accepted.
>
> **§6f — A defect that violates a doctrine invariant is a governed object.** It is recorded in the
> register and closed by the §6c test that proves it fixed. Defects that violate no invariant are
> engineering's to track and are **not** governance objects.
>
> **§6g — Acceptance is the owner's and requires readable evidence.** The owner cannot accept a build
> whose evidence the owner cannot read. Promotion evidence is enumerated at §9.3.

---

## 4. Proposed amendment to the **Governs** line

⚠️ **This is an amendment to a framework ratified fresh on 2026-08-23 (PR #241, `c15fa43`). Flag it
explicitly to the dev lead rather than letting it surface in a diff.**

**Current:** *"Governs: how a change to a release line is classified, captured, gated and delivered,
and the branch topology those rules run on."*

**Proposed:** *"Governs: how a change to a release line is classified, captured, gated and delivered;
what a build must prove to be accepted; and the branch topology those rules run on."*

Minimal by design — one clause added, nothing rewritten, no existing citation disturbed.

---

## 5. What §6 does NOT do

- **It does not design CI.** Job splitting, tiering, timeouts, runners and test frameworks are
  engineering's under §9.5 and DL-235. §6a says an unfinished gate is not passed; it does not say how
  to make it finish.
- **It does not make any check required.** Required-status configuration is a ruleset act. ⚠️ Live
  ruleset state is **NOT-MEASURABLE** from any ref — `CODEOWNERS:70-92` says so of itself.
- **It does not enumerate the invariants.** §6c points at the acceptance register; populating it with
  server-side twins is separate work (RB-123 records that GT-92 has no server twin).
- **It does not alter §9.3.** Promotion evidence is unchanged; §6 states what a *build* must prove,
  §9.3 what a *promotion* must carry.
- **It does not delegate or dilute ratification.** §6g reinforces owner acceptance.

---

## 6. Dependencies, conflicts and risks

| | |
|---|---|
| **DL-235** | Compatible. §6 states obligations; DL-235 keeps realization with engineering. **If the owner reads any clause as specifying realization, that clause should be cut** — the boundary matters more than the coverage. |
| **F002 §10** | Satisfied — fresh ratification, no reconstruction. |
| **F002 §11** | ✅ **VERIFIED — no conflict, no amendment needed.** §11 carries two bullets only: that F001 governs canon change while F002 governs release lines (*"where they meet, both apply"*), and that **realization of any gate is engineering's per §9.5**. It does **not** disclaim the application. §6 states obligations and never realization, so it sits inside that second bullet rather than against it. MEASURED-BY: `sed -n '208,232p' 00_owner/frameworks/framework_002.md`, 2026-08-30. |
| **RB-056** | §6a gives the standing reason to require the gate; the ruleset act stays separate. |
| **RB-123** | §6c makes the server twin an obligation rather than a backlog row. |
| **dl-land** | ⚠️ One canon PR in flight at a time; **#245 is open**. This cannot dispatch until #245 merges. |
| **Risk — scope creep** | §6c and §6f could be read as authorizing a testing mandate across `code/`. They do not: both are bounded by the acceptance register. |
| **Risk — §6b is broad** | It reaches every check in the repository, including ones written before it. **Expect existing green checks to turn red.** That is the intent, but it should be a deliberate acceptance, not a surprise. |

---

## ▶ OWNER RULINGS CAPTURED 2026-08-31 — not yet ratified

⚠️ **Captured intent, NOT ratification.** This still routes Backlog → Proposal → Review → Decision
under Framework 001. Recorded by AI; **AI ratifies nothing.**

| question (§7) | ruling |
|---|---|
| Placement | **§6**, as proposed — between §5 Capture and §7/§8, so the order reads *classify → capture → what a build must prove → gate → deliver*. **No renumbering.** |
| Clauses | **Accept §6a–§6g** as drafted. |
| Governs line | **Accept the amendment** — one clause added, nothing rewritten. ⚠️ Flag to the dev lead deliberately: it amends a framework ratified fresh 2026-08-23. |
| **§6b scope** | **Repo-wide, with a DATED grace period** — existing checks get a deadline to comply, never an exemption. |

**§6b grace period — SET 2026-08-31: expires `2026-09-14`.**

Chosen against the owner's fixed two-week cadence (iteration 1 = **2026-08-31 → 2026-09-11**;
boundaries **Sep 11 · Sep 25 · Oct 9**). **2026-09-14 is the start of iteration 2**, deliberately:

- it leaves **iteration 1's freeze untouched** — turning checks red days before a freeze already at
  risk would be the mechanism working against the cadence it serves;
- it surfaces reds at the **start** of a cycle, giving a **full iteration** to clear them before the
  **2026-09-25** freeze. A deadline landing *on* a freeze day is the one shape to avoid.

**Expect existing green checks to turn red on that date — that is the mechanism working, not a
regression.** Candidates already measured: RB-076's `SKIP-OK` on a missing line pointer, and
`gate_r2_guardrails.py`, which carries no self-test while twelve `tools/` checkers do. **Both are
bounded work, and RB-076's fix is already tasked.**

---

## 7. What the owner must decide

1. **Placement** — §6 as proposed, or §1/§2/§4 instead.
2. **§6b scope** — does *skip is not pass* apply repository-wide immediately, or to new checks only?
3. **§6e** — is build identity an acceptance obligation, or an engineering convention?
4. **The Governs amendment** — accept the added clause, or leave scope unchanged and site §6 as an
   explicit exception.

*(A fifth question — reconciling §11 — was raised and then closed by measurement: §11 does not
disclaim the application and needs no amendment. Recorded in §6 above rather than deleted.)*

**Recommendation: accept §6a–§6g and the Governs amendment; place at §6; apply §6b repository-wide
with a dated grace period** so existing checks are corrected rather than exempted — an allowlist that
only grows is the failure this framework exists to end.

---

> **Reminder:** this document is a recommendation. It becomes canon only via Framework 001 —
> Backlog → Proposal → **Review** → **Decision** → Change → Changelog — and only on owner ratification.

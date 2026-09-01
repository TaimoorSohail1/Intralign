# DL-243 — Build acceptance obligations: what a build must prove (Framework 002 §6)

- **Date:** 2026-08-31 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (canon — fills a vacant framework section and amends that framework's Governs line)
- **Framework 001** — AI drafts; only the owner ratifies. Proposal: `00_owner/decisions/PROPOSAL_F002_S6_BUILD_ACCEPTANCE_OBLIGATIONS_DL243_DRAFT.md`, accepted as drafted.

> ⚠️ **The owner's merge of this record is the ratifying act.** The clauses below were accepted as
> drafted on 2026-08-31; this file is the record that acceptance never had. **If the owner does not
> consider §6a–§6g settled, this record must not be merged** — a record that resolves a citation to a
> decision nobody made is the exact failure the citation gate exists to prevent.

## Decision

**Framework 002 gains a §6 — Build Acceptance Obligations — stating what a build must prove before it
may be promoted.** These are **obligations, not implementations**. How they are realized — CI topology,
tooling, tiering, test frameworks — remains engineering's under F002 §9.5 and DL-235. §6 states what
must be true; it never states how.

| | clause |
|---|---|
| **§6a** | **An unfinished gate is not a passed gate.** Cancellation, timeout and error are indistinguishable from failure for acceptance purposes. |
| **§6b** | **Skip is not pass.** A check that cannot evaluate its subject must **fail**. A skip is legitimate only where the subject genuinely does not exist for that change; never where the subject exists and the check could not reach it. |
| **§6c** | **Every doctrine invariant realized in software carries a test that fails when the invariant is violated.** A test that cannot fail is not a test. Invariants are enumerated in the acceptance register; each requires a server-side twin exercising the violating case, not only the honoured one. |
| **§6d** | **Validation evidence names what produced it.** Every pass or fail claim carries `MEASURED-BY:` or `NOT-MEASURABLE:`. A narrative verdict that names nothing is not evidence. Human observation remains legitimate under `NOT-MEASURABLE:`. |
| **§6e** | **A build carries a resolvable identity.** An unidentifiable build cannot be audited, rolled back to, or reasoned about after an incident, and therefore cannot be accepted. |
| **§6f** | **A defect that violates a doctrine invariant is a governed object.** It is recorded in the register and closed by the §6c test that proves it fixed. Defects violating no invariant are engineering's to track and are **not** governance objects. |
| **§6g** | **Acceptance is the owner's and requires readable evidence.** The owner cannot accept a build whose evidence the owner cannot read. Promotion evidence is enumerated at §9.3. |

**Placement: §6**, between §5 Capture and §7. The reading order becomes *classify → capture → what a
build must prove → gate → deliver*. ⚠️ **No section is renumbered** — the design line carries roughly
eighty-five live citations of the existing sections.

**Governs line amended**, one clause added and nothing rewritten:
*"…how a change to a release line is classified, captured, gated and delivered; **what a build must
prove to be accepted;** and the branch topology those rules run on."*

## Why now

**No framework governed the application.** F002 §11 and §9.5 place realization with engineering and
DL-235 ratified an engineering-owned SDLC; Framework 001's objects are Frameworks, Proposals,
Decisions, Backlog and Changelog entries. **Neither said what a build must prove before the owner
could accept it.**

The cost was measured. On one pull request — 990 files, +186,990/−495 — three document gates passed in
under fifteen seconds while the application quality gate read **Cancelled after 75m**, and the request
remained mergeable. A validation report asserted *"8 sections passed, 2 partial, 0 failed"* on
2026-08-28; a build-readiness audit of the same staging build on 2026-08-29 found **3 blocking**
defects. Both cannot be right, and nothing in canon adjudicated between them.

⚠️ **One failure shape recurs across all three subsystems: a check that cannot evaluate its subject
reports success.** A test constructed so it cannot fail — one test guarding cross-run finding identity
where both fixtures share the default evidence references, awarding the matcher's similarity bonus
automatically; a validation narrative naming no command; and a scheduled governance check returning
SKIP-OK because the control plane carries no line pointer. **Skip-as-pass, three times.** This
repository had already mechanized against that shape twice — `no_hardcoded_release_line.py` and
`report_measurement_check.py`. §6 states the rule those mechanisms enforce, so it stops being folklore.

## §6b scope and the dated grace period

**§6b applies repository-wide, with a grace period expiring `2026-09-14`** — never an exemption.

The date is the start of iteration 2 under the fixed two-week cadence (iteration 1 = 2026-08-31 →
2026-09-11; boundaries 2026-09-11 · 2026-09-25 · 2026-10-09), chosen deliberately:

- it leaves **iteration 1's freeze untouched** — turning checks red days before a freeze already at
  risk would be the mechanism working against the cadence it serves;
- it surfaces reds at the **start** of a cycle, giving a full iteration to clear them before the
  2026-09-25 freeze. **A deadline landing on a freeze day is the one shape to avoid.**

⚠️ **Expect existing green checks to turn red on that date. That is the mechanism working, not a
regression.** Two are already measured: a scheduled governance check's SKIP-OK on a missing line
pointer, and an application guardrail gate shipping with no self-test while twelve governance checkers
carry one.

## What this does NOT do

- **It does not design CI.** Job splitting, tiering, timeouts, runners and test frameworks are
  engineering's. §6a says an unfinished gate is not passed; it does not say how to make it finish.
- **It does not make any check required.** Required-status configuration is a ruleset act, and live
  ruleset state is not measurable from any ref.
- **It does not enumerate the invariants.** §6c points at the acceptance register; populating that
  register with server-side twins is separate work.
- **It does not alter §9.3.** §6 states what a *build* must prove; §9.3 what a *promotion* must carry.
- **It does not delegate or dilute ratification.** §6g reinforces owner acceptance.

## Ripple

1. **F002 §10 is satisfied** — this ratifies a vacant section fresh rather than reconstructing one from
   a citation, which is the only route §10 permits.
2. ⚠️ **§6c and §6f could be misread as authorizing a testing mandate across the application.** They do
   not: both are bounded by the acceptance register.
3. **§6e is currently unsatisfiable and that is a finding, not an oversight.** The deployed surface
   appears in zero repository files and the deployment configuration hardcodes a single origin, so
   staging and production cannot differ without a code change. **No build carries a resolvable identity
   today.**
4. ⚠️ **This record's own citation was rejected before it existed.** On 2026-08-31 the citation gate
   failed two apparatus files for citing DL-243 while it resolved to no record — including a checker
   whose docstring cited §6b as its justification. Both were corrected to name the proposal by filename
   instead. **The gate caught its author, which is the only evidence that it works.**

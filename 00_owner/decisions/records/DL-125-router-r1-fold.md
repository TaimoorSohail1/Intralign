# DL-125 — Notification router folds into R1

- **Date:** 2026-07-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# Notification router folds into R1 — amends DL-120's out-of-scope line

**Class:** B (scope amendment) · **Framework 001** — AI drafts; **owner ratifies at land.** · **Amends DL-120.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-17 · **Freeze manifest:** `RELEASE_1_BUILD_SPEC.md`.

---

## Decision

The **notification router** folds into **R1**. This amends **DL-120**, which listed the notification router as *"out of scope of R1 (Enh #4, unbuilt)"* on 2026-07-16 — a scoping made while the router did not yet exist.

The premise no longer holds: the router was commissioned, built, and its routing doctrine landed as **DL-122** on 2026-07-17 (one awareness record + a global toast at interrupt tier, attributed to no panel, probe-fenced per D182; wired to confirm / fix / answer / reviewer paths; the owner attribution fix in place — the notification is a global toast + badge, never the Confidence-card bar). It is **verified boot-clean and already ships inside the one deliverable prototype** (`slice-10-tiering-limits/prototype.html`) that dev builds against.

Keeping the router *out* of the R1 spec while it lives *in* the R1 prototype is exactly the spec-vs-build mismatch the freeze exists to prevent. Of the three items DL-120 deferred out of R1 — the notification router, the outcome-confidence-architecture "revisit at a tripwire," and the R1-test-driven fixes bucket — the router is the **only one that has since been built**; the other two remain correctly deferred. So this amendment touches the router alone.

**In scope of R1 (amended):** the notification router (DL-122). **Still out of R1 (unchanged):** the confidence-architecture tripwire revisit; the R1-test-driven fixes bucket.

---

## Scope boundary — what this does not change

DL-120's core stands: the enhancement layer folds into R1; R1 feature-freezes at handoff; "R1.x" holds only post-handoff, test-driven fixes. The router's own doctrine (DL-122) is unchanged — this decision moves only its **release scope**, not its behavior. No new capability is authored.

---

## Governance

Lands as canon via `dl-land`, amending DL-120. The freeze manifest (`RELEASE_1_BUILD_SPEC.md`) already reflects the router as in-scope. AI drafted; **only the owner ratifies.**

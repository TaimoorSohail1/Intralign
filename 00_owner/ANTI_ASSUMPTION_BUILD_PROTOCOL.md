# Anti-Assumption Build Protocol — READ BEFORE WRITING ANY CODE

**Audience:** the engineering team building OSLO Release 1 with **Claude Code** (which auto-reads `CLAUDE.md`, where this file is linked). · **Status:** Authoritative build rule · **Date:** 2026-06-04
**Why this exists:** this body of work is handed off to a team and a Claude Code instance that did **not** author it. The single biggest risk to a high-quality system is **drift** — the LLM or a person filling a gap with a plausible *assumption* instead of the specified truth. Claude Code inherits the build rules from `CLAUDE.md`, but this document makes the **anti-assumption rule unmissable for the whole team**: the default behavior must be **"escalate the gap," not "guess the gap."**

---

## The one rule

> **Do not infer. Do not assume. If a needed detail is not specified, STOP and escalate — never invent it.**

The specification corpus in this repository is intended to be **authoritative and, for Release 1, complete on the cognitive side.** If you (human or LLM) feel the urge to "fill in" something that isn't written down, that urge is the risk this protocol guards against.

## What to do when something appears missing

When a detail you need is not in the spec, it is **always** one of exactly three things — never a fourth ("I'll decide it myself"):

1. **Intentionally commodity** — application/platform plumbing (auth, project CRUD, settings, notifications-state, sharing, monetization, telemetry) is **deliberately not cognition-contracted** (DL-043 J, Categories C/E/F). Build it with normal engineering judgment; it does **not** touch the cognitive contracts. *If unsure whether something is commodity, treat it as cognitive and escalate.*
2. **An open owner decision (TBD)** — listed in **`OPEN_TBD_REGISTER.md`**. These are **DO NOT ASSUME** items. Escalate to the repository owner; do not pick a value to unblock yourself.
3. **A genuine gap / contradiction** — the spec should cover it but doesn't, or two sources disagree. **STOP, raise it as a backlog item, and get an owner decision.** Do not resolve a spec conflict in code.

## Non-negotiable build rules

- **Every change cites a contract id.** No code is written that doesn't trace to an approved contract (`IC-WA-001`, `IC-WB-INFER`, `IC-WS-SYNTH`, …). Un-contracted code is a defect, not a feature. (Use the **Build/Test/Observe Traceability Matrix** to find the contract for a capability.)
- **The named source wins.** When a plan/runbook/summary differs from the contract or spec it cites, the **cited source is authoritative** — never the convenience copy. When in doubt, follow the link.
- **Use canonical vocabulary only.** Every domain term is defined once in **`CANONICAL_GLOSSARY.md`** with its **banned synonyms**. Do not introduce a new name for an existing concept; do not reuse a forbidden term.
- **Preserve the epistemic invariants — they are not stylistic.** Canonical = Attested (source-attributed, re-derivable); cognition is Derived (recomputable); **recompute appends, never overwrites**; Derived is never written as Attested-truth; **OSLO never self-accepts**; **OSLO never autonomously writes to a user's artifact**; no Authority engine in R1. A change that touches any of these is **STOP-and-escalate**, not a judgment call.
- **Positive AND negative tests, always.** A test suite without the negative cases (proving the forbidden behavior is impossible) is invalid. The negatives are where assumptions get caught.
- **Production is human-only.** No LLM or pipeline self-deploys to production.

## How to start (so you don't drift on day one)

1. Read `START_HERE.md` → the Engineering Handoff Package → the Onboarding Runbook. (Claude Code auto-loads `CLAUDE.md`, which links this protocol + the glossary, matrix, and TBD register.)
2. Read `CANONICAL_GLOSSARY.md` and **this** protocol.
3. For any capability you build, open the **`RELEASE_1_BUILD_TEST_OBSERVE_TRACEABILITY_MATRIX.md`**, find its contract + acceptance test + observability event, and build **to those**, not to your model of what it "should" do.
4. Check `OPEN_TBD_REGISTER.md` — if your work depends on a TBD, escalate before proceeding.

## The mindset

A confident wrong answer is worse than an honest "this isn't specified — I'm escalating." You are not being judged on momentum; you are building a system whose entire purpose is to **preserve truth and never assert false certainty.** Build it the way it behaves: when the evidence isn't there, say so and ask.

---
*This protocol instructs the external engineering team and its LLM to never fill a specification gap by inference: any missing detail is either intentionally-commodity (build normally), an owner TBD (escalate, in the Open-TBD Register), or a genuine gap/contradiction (STOP and get an owner decision). It restates the non-negotiable build rules — every change cites a contract id, the named source wins over convenience copies, canonical vocabulary only, the epistemic invariants are STOP-conditions not style, mandatory positive+negative tests, and human-only production — and points to the glossary, traceability matrix, and TBD register as the tools that make "escalate, don't assume" the default.*

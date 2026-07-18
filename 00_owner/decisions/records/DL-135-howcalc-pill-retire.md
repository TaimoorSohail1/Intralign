# DL-135 — The 'How this is calculated' pill retires — the lead-line leads, the method lives on the concept's ⓘ

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The "How this is calculated" pill retires — the lead-line leads, the method lives on the concept's ⓘ

**Class:** B (experience-doctrine refinement — the confidence card's explainers) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Amends** D054 (the how-calculated affordance). **Refines** DL-132 (the Overview lead-line). **Upholds** D046/D051 ("Why" remains the reliability-basis home) and D183b (no index returns).

---

## Decision

The confidence card carried **two competing first-time explainers**: the standing **"How this is calculated"** pill (D054) and the footer **"Why ▾"** disclosure. With the plain-language **lead-line** (DL-132) now leading the read and doing the first-time orienting job, the standing pill was redundant — a second explainer competing for the newcomer's attention on the surface the lead-line exists to simplify.

The pill is **retired** (not merged). The only guard-legal merge direction would fold it into "Why ▾" — the guard-locked home of the reliability basis (D051) — which would **bury** the method behind a disclosure first-timers may not open, working against the audience it serves. So instead of burying it, the pill is removed and the method's **essence is preserved on the concept's own ⓘ** (the "Outcome Confidence" info tip): *OSLO reads how clear, aligned and feasible your plan is — the weakest of the three sets the level — flags a confident read built on thin evidence, and moves only when something real changes.* That is the method's one quiet, canonical home, reached where the concept is named rather than as a competing pill.

Net: the confidence card now has **one** explainer path (the ⓘ for the method, "Why ▾" for this read's reasons + reliability basis), and the read leads with plain language. The now-empty `.num` wrapper (which had held only the deleted 0–100 index and this pill) is removed with it; the orphaned pill handlers are null-guarded.

## Why — the constraint that shaped it

The recommendation was explicitly **retire, not bury**. Two standing explainers on the first-time surface is the guidance-density the Overview rework set out to cut; but the method itself is load-bearing OSLO copy (it is *how* the read is honest) and must not simply vanish. Retiring the pill removes the competition; moving the essence to the concept's ⓘ keeps the method reachable without a second competing affordance and without hiding it inside the reliability disclosure. The lead-line, not a pill, is now what orients a newcomer.

## Guardrails

- **The method survives** — its essence lives on the "Outcome Confidence" ⓘ; it is retired from the standing pill, not deleted.
- **"Why" is untouched** — the reliability basis (D051) and this read's reasons stay in the "Why ▾" disclosure; nothing was folded in.
- **No index returns** — removing the `.num` wrapper does not reintroduce the 0–100 index (D183b). → `_assertNoZeroToHundredIndexAnywhere()` (green).
- **No dangling handlers** — the retired pill's `openHowCalc` / `scheduleCloseHowCalc` / `toggleHowCalc` are null-guarded and inert.

## Governance

Lands as Class-B canon via `dl-land`, amending D054 and refining DL-132. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors). AI drafted + built; **only the owner ratifies.**

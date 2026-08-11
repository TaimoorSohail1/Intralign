# Governance Proposal (DRAFT) — Pro program / cross-plan support: scope + the $79 question

> **Status: RATIFIED as DL-208** — Idris (Founder Console), 2026-08-09. Adopted **Bundle A** scope and
> **ratified Pro at $79/mo** (amends DR-7; drops the placeholder). Staged in `release-2/`; withheld from
> `main` until R1 graduation. AI drafted and recommended; the owner ratified (Framework 001 / 001A).
> Ratified record: `release-2/canon/decisions/DL-208_PRO_PROGRAM_SCOPE_AND_PRICE.md`.
>
> **Origin:** Owner working session, 2026-08-09 (Idris). **Backlog:** RB-042. **Decision:** DL-208.
> **Layer:** Product scope / monetization (`10_product`). **Non-doctrinal** (defines capability scope +
> informs a price; changes no doctrine). **Extends** DL-206 §3, DR-7, DL-083; **bounded by** DL-172 §2/§5,
> `RELEASE_1_TIER_DEFINITIONS_V1` §1, DL-103/DL-104, DL-034 (Portfolio Cognition).

---

## 1. Backlog entry (framing)

DL-206 moved the *felt* value of the execution loop — manual execution-stage monitoring — down to **Basic**.
That leaves Pro selling automation (continuous monitoring + auto-import / two-way sync) **plus** "program /
cross-plan support." Automation alone is a thin story for the 2.7× Basic→Pro step ($29 → $79; DR-7's own
open note). So **whether $79 is realistic depends entirely on what "program support" actually is.**

The trap the scope must avoid: **Basic already grants multiple plans** (DL-172 §2 — "multiple outcomes per
plan AND multiple plans," a *capacity* grant). So Pro's differentiator **cannot** be "you can have several
plans." It must be a **cross-plan cognition layer** — relating and aggregating *across* an owner's set of
plans — which Basic does not do. Above Pro, org-scale **portfolio cognition is Enterprise** (E3;
Portfolio Integrity Scan, DL-034), and multi-user **collaboration/governance is Team** (per-seat). Pro sits
in between: still the **individual motion**, flat per-account, one owner, a *program* of related plans.

## 2. Proposed canon (content)

**2.1 — Canonical definition.** A **program** = a set of **related plans under one owner**, worked as one
effort. **Programme support** = cross-plan **execution cognition** over that set: it does not improve any
single-plan read (same accuracy bar) — it adds a layer that only exists *across* plans.

**2.2 — The four-way boundary (this is the load-bearing part).**

| Tier | Unit of cognition | What's new at this tier |
|---|---|---|
| **Free** | one plan | the read |
| **Basic** | *several plans, each read independently* (DL-172 §2 capacity) + manual execution-stage monitoring | parallel plans; on-demand execution monitoring |
| **Pro** | **the program — plans read *in relation to each other*** | automation (continuous monitoring + auto-import / two-way sync) **+ the cross-plan cognition layer (§2.3)** |
| **Team** | the program, worked by *many people* | collaboration + governance **as the product**, per-seat |
| **Enterprise** | the **portfolio** — org-/cross-system scale | portfolio cognition (DL-034), org governance, contract |

**2.3 — Pro program cognition layer (the candidate capability set).** Marked **[Pro]** = recommended in
scope; **[↑Ent]** = ceiling, belongs to Enterprise portfolio; **[owner]** = genuinely owner-gated inclusion.

- **[Pro] Programme roll-up view** — one surface aggregating each plan's *outcome integrity* read across the
  program (an aggregate of the same honest reads — **never a new composite "program health score,"
  never a forecast**; §3).
- **[Pro] Cross-plan dependency mapping** — surface where one plan's assertions/outputs are another plan's
  dependencies; flag cross-plan conflicts and gaps. *This is the capability Basic structurally cannot give.*
- **[Pro] Programme-level continuous monitoring** — aggregate execution drift across the program (the
  automated §DL-206 form, applied cross-plan).
- **[owner] Programme envelope** — how many plans constitute a "program" at Pro before Enterprise (a
  *capacity* cap on the program view; keeps flat-per-account safe and the Pro↔Enterprise line legible).
- **[↑Ent] Org-/cross-system portfolio, roll-up across *owners/teams*, portfolio governance** — **out of
  Pro**; Enterprise (E3 / DL-034).

**2.4 — Explicitly NOT in Pro.** Multi-user collaboration/governance (Team). Cross-owner or org-scale
portfolio (Enterprise). A better single-plan read (never — judgment quality is never tiered; DL-104: Pro is
not "a better brain").

## 3. Doctrine preserved (binds the roll-up especially)

The program roll-up is an **aggregate of the same maturity reads** — **single-hue outcome-integrity, never
red-amber-green health, never a probability/forecast of program success** (D003/D183b; honesty-first). Pro
buys **cross-plan scope of cognition**, never a higher-quality read (one accuracy bar; DL-103 §1 / DL-104).
Record, reviewers/CRR, Viewers stay free/unmetered (DL-102). Flat **per-account**, never per-seat (DR-7) —
seats begin at Team.

## 4. The $79 question — two coherent scope+price bundles

The price is a function of the scope. Two internally-consistent options:

- **Bundle A — "program cognition" (holds $79).** Pro = automation **+ the full §2.3 [Pro] layer**
  (roll-up, cross-plan dependencies, program monitoring). This is a **PMO / consultant / program-lead**
  capability — a *different, higher-WTP buyer* than Basic's individual PM. At $79 flat, radiating to a whole
  reviewer/Viewer team free, it is competitive-to-cheap for that buyer. **$79 is realistic; arguably low.**
- **Bundle B — "automation only" (implies ~$69 or a squeeze).** Pro = continuous monitoring + sync over
  Basic's existing multi-plan, **without** a real cross-plan cognition layer. That's automation-of-a-manual-
  thing — a weak 2.7× story. **$79 is not realistic here;** compress toward ~$69, or the tier gets squeezed
  between Basic (has the loop) and Team (has the org) and may fold into a Free→Basic→Team ladder.

**Recommendation:** adopt **Bundle A** scope. It is the only version in which $79 is defensible, it gives Pro
a clear buyer, and it uses the cross-plan layer Basic structurally lacks. Set the **final** number against
reverse-trial / intent telemetry at launch (DR-7 "finalize when these ship"; Tier-register standing rule —
numbers re-derived from telemetry, never a spec). Until then $79 stays PROVISIONAL, now with a scope behind it.

## 5. Review (Framework 001A — five outputs)

- **Findings.** (1) Post-DL-206, Pro's price realism reduces to a single question: does Pro carry a real
  cross-plan cognition layer? (2) Basic's existing multi-plan grant (DL-172 §2) forces the differentiator to
  be *cross-plan cognition*, not plan count. (3) The Pro/Team/Enterprise lines already exist in canon
  (Tier Def §1; DL-103; E3/DL-034) and this scope fits cleanly between them. (4) A genuine program layer
  shifts Pro's buyer to a higher-WTP program/PMO lead, which is what makes $79 (or more) coherent.
- **Concerns.** (a) **Ceiling creep** — roll-up/dependencies can drift toward Enterprise portfolio; the
  §2.3 [↑Ent] line and the [owner] program-envelope cap must hold it to *one owner's related plans*.
  (b) **Honesty risk** — a "program roll-up" invites a composite health/traffic-light score; §3 forbids it
  (aggregate of honest reads only). (c) **Anti-Assumption** — the program-envelope number and any [owner]
  inclusions are owner calls; placing capabilities here authorizes no build (routes to realization scoping).
  (d) **Price still telemetry-gated** — this proposal makes $79 *defensible*, not *final*.
- **Dependencies.** **Extends** DL-206 §3, DR-7 (Pro price), DL-083 (execution & program support).
  **Bounded by** DL-172 §2 (Basic multi-plan) and §5 (portfolio = Enterprise), Tier Def §1, DL-103/DL-104,
  DL-034 (Portfolio Cognition). **Updates on adoption:** Tier Def §1/§2c (a program-support row); DL-053
  register (program vs portfolio vs plan). **Spelling normalization:** adopt US **"program"** as the
  canonical term (Intralign is US-based), superseding the British **"programme"** in prior canon
  (Tier Def §1, DL-083, DL-104, DL-206) — a doc-integrity find-and-replace routed through the DL-053 register. **Feeds:** a realization/DL for the program layer build (Beta+).
- **Recommendation.** **Adopt Bundle A scope**; hold $79 as PROVISIONAL pending launch telemetry; set the
  program-envelope cap; route the build to its own realization. If the owner prefers Bundle B, ratify the
  compression to ~$69 (or the Pro-fold) explicitly.
- **Status.** **Ratified as DL-208 (2026-08-09, Idris/Founder Console): Bundle A adopted; Pro price set at $79 (amends DR-7); "program" spelling adopted.** Remaining owner calls are **non-blocking:** program-envelope number; launch-time telemetry confirmation of $79; exact DL-053 terms.

## 6. Decision record body (for dl-land — written for Bundle A)

```
title: Pro program / cross-plan support scope — cross-plan cognition layer; $79 held provisional
slug: pro-program-support-scope
class: B (product scope / monetization; non-doctrinal)
decided_by: Idris (Founder Console)

## Decision
Scope Pro's "program support" (DL-206 §3) as a cross-plan EXECUTION COGNITION layer over a set of related plans under one owner (a "program"), distinct from Basic's multi-plan capacity (DL-172 §2) and from Enterprise portfolio/org-scale cognition (DL-034). In scope at Pro: program roll-up view (aggregate of the same outcome-integrity reads — never a composite health score or forecast), cross-plan dependency mapping, program-level continuous monitoring, under a program-envelope capacity cap. Out of Pro: multi-user collaboration/governance (Team), cross-owner/org-scale portfolio (Enterprise), any higher-quality single-plan read (judgment quality never tiered; DL-104). This gives Pro a defined higher-WTP buyer (program/PMO lead) and makes Pro at $79/mo defensible; $79 stays PROVISIONAL, finalized against reverse-trial/intent telemetry at launch (DR-7). Non-doctrinal; honesty invariants preserved (single-hue integrity, no forecast, one accuracy bar, flat per-account). Phase: Beta+ (with execution monitoring, DL-083/DL-206); no R2 build impact. Programme-envelope number and build realization route to their own scoping.

## Status
Ratified.
```

## 7. Landing (owner runs — AI does not land canon)

Stage in `release-2/` (R2-isolated, parity with DL-206). On ratification: number the DL, add a program-
support row to Tier Def §1/§2c and the program/portfolio/plan terms to the DL-053 register (as a redline,
applied at graduation), and open the realization scoping item. Branch → PR → doc-integrity gate → owner
merge. **Never push to main.**

---
*Owner decision options: **(A)** adopt Bundle A scope, hold $79 provisional (recommended; written for A) ·
**(B)** adopt Bundle B (automation-only) and compress Pro to ~$69 or fold Pro · **(C)** defer scope + price
until reverse-trial telemetry, keep $79 provisional with no scope. AI drafted and recommends; only the owner
ratifies (Framework 001A).*

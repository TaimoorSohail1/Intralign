# Proposal — Overview surface redesign: confidence-led, low-cognitive-load (RB-037)

- **Status:** Proposed — awaiting owner decision (Framework 001 · Review complete, Decision pending)
- **Class:** A (UX presentation + Visual-token usage). **Presentation-only; no model, scoring, contract, or doctrine change.**
- **Backlog:** RB-037 (this proposal)
- **Author (analysis/recommendation only):** AI contributor under Framework 001A / DL-033. **AI does not ratify.**
- **Owner decision:** required to adopt, reject, or amend.
- **Visual reference of record:** `product-design/oslo_r1_overview_redesign_mockup.html` (illustrative; band words are placeholders — see C1).

> Governance note: analysis + recommendation routed through Framework 001 (Backlog → Proposal → **Review** → Decision → Change → Changelog). No canonical artifact is changed by this document; the `DL-PENDING-overview-redesign` record carries the ratifiable decision text, and the spec/prototype edits are **realization landed with the decision at owner merge**.

---

## 1. Problem

The Release-1 Overview — led by the **Confidence** section — carries high cognitive load. Three failures, surfaced in owner review 2026-07-08:

1. **The panel narrates in prose.** Reliability, the change since last run, and the causal story are all sentences competing for the same attention, so there is no clear focal point.
2. **Redundant / competing encodings.** A radial ring re-states the score the number already gives; a green "your change moved the read" box re-states the trend.
3. **A color-semantics conflict.** The green delta box reads as "good / healthy," which is in tension with **Visual Design spec §1.2** — *"Confidence & CAF are NOT health/traffic-light colored … never red=bad / green=good … orange is the action accent, not a confidence/health signal."*

The sections below (Start here, Progress, More) are individually fine but use slightly divergent header, chip, and accent conventions, so the page doesn't read as one system.

## 2. Proposed change (one decision, presentation-only)

Adopt the redesigned Overview per the reference mockup. Principle: **one focal signal, the rest encoded visually, narration behind progressive disclosure.**

**Confidence section**
- The **maturity score (66/100 + band)** is the single focal read; reliability folds into one qualifier line (`Moderate · qualified by moderate reliability`).
- The change since last run is a **quiet trend line** (`↗ 8 since your change · from 58`) — replacing the green delta box.
- The three CAF dimensions render as **neutral maturity bars** under a "What's driving it" label, each with an always-visible **band word** (Clarity / Alignment / Feasibility) and **hover/tap detail**. The **lowest dimension carries the single amber attention flag** ("the limit").
- Causal narration lives behind a **"Why"** disclosure — **auto-opened once** after a *material, user-initiated* change, collapsed thereafter (sunsets like the existing teaching copy).
- **Removed:** the ring gauge, the green "your change moved the read" box, and the persistent `Current` / `From OSLO` pills. Staleness is surfaced **conditionally** (a "previous analysis — reanalyzing" marker only when not current), never as a persistent badge.

**Lower sections aligned to the same grammar**
- Eyebrow + inline descriptor on every section; dot-and-label chips for status/severity; neutral tracks with the count right-aligned; **amber reserved for actions and attention; green reserved for a good state** (e.g. "all clear"); everything else neutral.

**Color discipline (one meaning per accent):** amber = act / attention; green = good state; the confidence/CAF maturity stays on the neutral ramp. This **strengthens** conformance to Visual §1.2 by removing the green-as-health delta.

## 3. Framework 001A Review

**Findings.**
- The redesign reduces the panel to three sequential reads — where you stand, where it's weak, why (on demand) — cutting prose without losing information.
- It **strengthens** Visual §1.2 conformance: the green "health" delta is removed and amber becomes the sole action accent; confidence/CAF stay on the neutral maturity ramp.
- It surfaces **per-dimension CAF band values**, which the CAF Engine (CAF-01) already computes — a presentation change, not new data.
- Progressive disclosure (Why, hover detail) aligns with the Confidence explainability intent (Confidence Model §10 — always name the cause) without putting the cause on-screen by default.

**Concerns.**
- **C1 — band vocabulary (OPEN, anti-assumption).** The per-dimension band words (Strong / Moderate / Limited) are **placeholders**. They must map to the **canonical CAF band set** before build; the exact vocabulary is an owner-decision item, not to be invented in the mockup.
- **C2 — accessibility of the detail layer.** The band word must remain the **always-visible** value; hover/tap only *adds* detail. Touch, keyboard, and screen-reader parity are required (tap-opens-detail on touch).
- **C3 — "understanding over runs" trend.** Reconcile with **Confidence Stages** (Orientation→Expanded→Validated, CONF-05) and the **Initial/Extended Analysis** labels (DL-046); it should render the **lightweight understanding timeline (MRI-06)**, not introduce a new object.
- **C4 — Why auto-open scope.** Must open only on a **material, user-initiated** change, not on every background Deep Pass recompute (AE-03), and must sunset — else it re-introduces the noise this removes.
- **C5 — staleness (doctrine).** With the `Current` pill removed, the **conditional** stale marker must still satisfy the rule that stale understanding is **always surfaced as previous/stale** and never presented as current.

**Dependencies.**

| Artifact | Zone | Impact | Action |
|---|---|---|---|
| `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` | 10_product/experience | **HARD** | Amend Overview layout + the Confidence/Start-here/Progress/More sections |
| `RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1 §1.2` | 10_product/experience | **CONFIRM** | Conformance strengthened; confirm token usage (amber = action only) |
| Confidence presentation + per-dimension CAF band surfacing | 10_product/experience, domain | **MED** | Surface CAF band per dimension + hover detail (CAF-01 supplies values) |
| Finding/Issue presentation (Start here) | 10_product/experience | **CHECK** | Uses "Issues" per DL-095; consistent |
| `oslo_r1_experience_mockup_v3.html` (prototype) | product-design | **MED** | Overview surface updated to this design (v-next) |
| CAF Model / Confidence Model | 10_product/domain | **CHECK — none** | Presentation-only; models unchanged |

**Recommendation.** Adopt. It lowers cognitive load, tightens Visual §1.2 conformance, and reuses data the CAF Engine already produces. **Pin the canonical CAF band vocabulary (C1) before the surface is built.** Realize as the Overview in the v-next prototype and the experience specs.

**Status.** Proposed — Review complete; **owner Decision pending.** Not ratified; not canon.

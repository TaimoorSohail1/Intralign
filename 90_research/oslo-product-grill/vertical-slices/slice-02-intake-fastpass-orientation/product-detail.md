# Slice 2 — Intake & Fast-Pass Orientation · Product Detail

Cumulative (Slice 1 + Slice 2). Decisions D035–D042 are the Slice-2 scope, plus the Revision-2 owner fixes **D043–D046**; all Slice-1 and cross-cutting decisions continue to bind. Illustrative values are flagged; real NFRs remain owner-TBD.

## Decision → behavior map

| Decision | Behavior in this slice | Where in prototype |
|---|---|---|
| **D035** — intake constructs all 7 plan artifacts | Fast Pass constructs Intent · Context · Scope · Requirements · Work breakdown · Schedule · Resources from any intake. Inferred content is labelled **From OSLO (Derived)** and reliability-qualified (High/Moderate/Low). Thin evidence → Clarification Requests, not fabricated certainty. | `PLAN_SECTIONS` model; `renderPlanSections()`; "Plan artifacts (7)" in Overview → More |
| **D036** — Fast Pass time measured, not fixed | Elapsed time is measured via `Date.now()` deltas and shown (in the **OSLO chat** completion message per D043) as "Initial Analysis complete in **N**s — **under the 60-second target**." No hardcoded canonical number. Pacing ≈30s (D031). | `_measuredStart/_measuredMs`; `postFastPassComplete()` |
| **D037** — six Fast Pass outputs at orientation | Overview surfaces: (1) Orientation Confidence hero, (2) Initial Attention (reachable map + badge), (3) Top issues (Start here), (4) Clarification requests (light pointer in Start here → tied Issue), (5) Suggested fixes (per-issue in the Issue detail), (6) Analysis status (Progress state line + chip). | Overview sections + `#vsAttnBadge` |
| **D038** — land on Overview; Attention co-primary | Post-Fast-Pass landing = confidence-led Overview. Attention Map reachable via top-center view switch (Overview · Attention) with an open-issue count badge. Sets the C-001 default (owner may flip). | `showView()`; `.vswitch` |
| **D039** — first-run orientation + fresh completion notice | Strategic-chain orientation fires first project only (persisted `orientSeen`). The fresh-analysis completion notice (now an **OSLO chat message**, D043) fires only on a fresh analysis (`FRESH_ANALYSIS`), not for returning users. | `orientationSeen()`; `FRESH_ANALYSIS` |
| **D040** — Extended Analysis auto-runs, supersedes | Deep Pass auto-starts after orientation, non-blocking. On success supersedes provisional→current; hero chip flips Provisional→Current; completion **chat** message + refined 58→62 / Feasibility Very Low→Low. | `startDeepPass()` → `deepComplete()`; `ustate` chip |
| **D041** — Deep Pass failure → last-good + retry | Demo trigger ("Sim Extended-Analysis fail") arms failure. On fail: keep last-good read, chip → "Last-good", **chat** notice "couldn't complete — showing your last-good understanding · Retry." Retry recovers → current. | `setDeepFail()`; `deepFail()`; `retryDeep()` |
| **D042** — clarifications at orientation + in-issue | Clarification surfaces as a **light pointer inside Start here** AND (question + answer box) inside the tied Issue. Answering → marks the section Confirmed by you, bumps its reliability, simulates reanalysis, closes the issue, refreshes Overview/Attention counts. | `renderClarifications()`; `openTopClarification()`; `answerClarification()` |
| **D043** — completion notices to OSLO chat (Rev 2) | Fast-pass and deep-pass completion notices (and failure/retry, claim-through) are **OSLO chat messages**, not Overview banners. The chip state and the Progress state line remain as **status**. | `pushChat()`; `postFastPassComplete()`; `postDeepPassComplete()`; chat rail `#chatp` |
| **D044** — optional feature tour (Rev 2) | Spotlight coachmarks (`.tourmask`/`.tourtip`, `startTour()`), opt-in, never gating. Launched from the chat completion message and a left-rail affordance. 4 steps spotlight Slice-2 surfaces (Confidence, Start here, Attention switch, chat). Marked seen in `localStorage`. Slice 5 artifact-edit step + Slice 8 Settings→Help re-open are code seams only. | `TOUR`; `startTour()`/`tourGo()`; `#railTour`; `tourSeen()` |
| **D045** — confirmations belong to the Issue detail (Rev 2) | Overview shows **summary counts only** ("N open · M resolved"). Clarification questions and the resolved-issue confirmation view live in the light Issue panel, not on the Overview. Full issue-confirmation UI = Slice 6. | `.conf-foot` counts; `openIssue()` resolved `.ip-resolved` block |
| **D046** — reconcile Overview to DL-096 (Rev 2) | Overview sections are EXACTLY **Confidence → Start here → Progress → More**. The standalone Reliability card was removed; reliability is an **inline qualifier** on Confidence with detail via the Why disclosure. Neutral maturity ramp kept; severity color only on issues. | `#pane-overview`; `.card.hero`; `#whybox` |

## Advisory & language guardrails (inherited)
- Advisory-only (D001): clarification/fixes never change the plan without the user; "OSLO asks; you answer; you decide."
- Plain labels (D012): Plan artifacts, Work breakdown, Clarity·Alignment·Feasibility, From OSLO / Confirmed by you, Initial/Extended Analysis, Issues (not Findings/weaknesses), Provisional/Current.
- Confidence = maturity (D002); focal number never bare — band + reliability + cause present. 5-band scale (D020). Ring removed (D019).
- Severity color only on issues (D003); confidence/CAF/heatmap-empty use the neutral maturity ramp.
- Dark default + WCAG 2.1 AA (D015): focus-visible rings, keyboard roles, reduced-motion.

## Seams left for later slices (do-not-over-build)
- **Slice 3** — deeper Overview interactions (full reliability drill, trend history, timeline).
- **Slice 4** — full Attention interactions (scoped filtered issue lists, field-view nodes).
- **Slice 5** — editing/confirming plan artifacts (attesting drives reanalysis).
- **Slice 6** — full Issues UI (By dimension / By severity, apply-fix drafting, full panel history) **and full issue-confirmation UI (D045)**. The Slice-2 Issue panel is intentionally light (confirmations viewable, not full).
- **Slice 8** — Settings→Help re-open control for the feature tour (D044); the Slice-2 tour leaves this as a code seam.

## Revision 2 (2026-07-09)
Owner-directed fixes **D043–D046** applied in place; Slice 1 funnel and the rest of Slice 2 (activation, intake, Fast Pass ≈30s, Attention map, analysis-state machine, clarification loop, theme, localStorage) not regressed. See the decision→behavior rows for D043–D046 above.

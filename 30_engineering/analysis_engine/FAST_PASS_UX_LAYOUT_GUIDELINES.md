# Fast Pass — UX Layout Guidelines

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** UI Specification §7 (60-Second Orientation), §11, §16, §20 · State/Event Models · Confidence/Reliability models. Tags: `canonical` / `derived` / `proposal` / `TBD`.

> The Fast Pass UX presents the **60-Second Orientation** and must make its **non-final** nature obvious. It uses only existing entities/enums; no governance or future surfaces.

## Purpose `canonical`
Give the user a trustworthy *first* read fast: current confidence, CAF drivers, top findings, top recommendations — with an explicit "not final, Deep Analysis to follow" frame.

## Layout regions `derived`
- **Confidence header** `canonical` — Outcome Confidence value + `confidence_band` + **reliability qualifier** (never a bare number). Click → Confidence Experience.
- **CAF drivers** `canonical` — Clarity / Alignment / Feasibility, each with assessed level + **per-dimension reliability**. Alignment/Feasibility carry a visible "preliminary" marker in Fast.
- **Top findings** `canonical` — highest-severity `detected` findings, with type + affected dimension(s).
- **Top recommendations** `canonical` — `generated` recommendations tied to those findings.
- **Evidence summary** `derived` — count/sources of evidence + key context items.
- **Orientation banner** `canonical` — persistent: **"This is your 60-Second Orientation, not final analysis. Deep Analysis is in progress."**

## State presentation `canonical`
- Project badge follows `lifecycle_state` (`orienting` → `oriented`).
- Findings show `detected`; actions enabled only on legal source states (acknowledge from `detected`) — prevents API `409`.
- Recommendations show `generated`; accept/reject enabled.

## Loading / progress `canonical`
- Analysis Progress: "Building your 60-Second Orientation" while the fast run is `queued`/`running`.
- Target < 60s; if exceeded, show honest continued-progress messaging — **never** fake completion.
- Skeleton placeholders for confidence/CAF/findings while loading (UI §16).

## Empty / error states `canonical`
- Pre-analysis empty state explains the journey.
- Errors map to the API error model (UI §17); analysis failure → retry affordance (new run); prior state preserved.

## Event-driven refresh `canonical`
- `fast_analysis_completed` → render orientation; `confidence_created`/`finding_created`/`recommendation_created` populate regions in place (UI §20). No manual reload.

## Explainability `canonical`
- Each finding/recommendation/confidence expands to its basis (evidence/context + producing run) from stored lineage; reliability explains via Coverage/Evidence Availability/Assessability.

## Reliability honesty `canonical`/`derived`
- Lower reliability on Alignment/Feasibility must be **visible**, not hidden; the UX should communicate "preliminary, improving with Deep Analysis."

## Forbidden `canonical`
- No governance/accepted-understanding/agent/execution surfaces; no email/SMS/Slack; no presentation of Fast output as final; no invented score visualizations implying weights/percentages beyond the model's qualitative vocabulary.

## Open decisions
- Visual design tokens, confidence/MRI charting style, microcopy, "still working" thresholds — **`TBD – Owner Decision Required`** (depend on visual design + NFR latency targets).

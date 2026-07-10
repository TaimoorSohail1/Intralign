# Decision Tree — OSLO R1

Node status: `Locked from docs` · `Accepted recommendation` · `Client override` · `Needs decision` · `Superseded`

## Theme & Product Experience
- Advisory-only doctrine — **Locked from docs**
- Confidence = understanding maturity, neutral ramp — **Locked from docs**
- Severity-only red/amber/green — **Locked from docs**
- Two-theme (dark default / light), WCAG 2.1 AA — **Locked from docs** → drives Phase 2 theme
- Voice: confident/credible, no hype — **Locked from docs**
  - Hero headline A/B/C + descriptor — **Needs decision**

## Personas & Actors
- Primary: PM moving to strategic influence ("AI-first PM") — **Locked from docs**
- Secondary: non-PM who manages projects — **Locked from docs**
- Actors: User · System · AI Agent · Collaborator/Viewer — **Locked from docs**

## Slice Boundaries (depend on flow spine)
- Intake → Fast Pass → Orientation/MRI → Deep Pass → Improvement Loop — **Locked from docs**
  - Slice 1 Access & Onboarding ← activation, intake, anonymous first-run, save-to-keep
  - Slice 2 Intake & Fast-Pass Orientation ← evidence provision, 60s orientation, MRI reveal
  - Slice 3 Project Overview & Understanding Console ← Confidence/CAF/Reliability/Findings/Recs/Summary
  - Slice 4 Attention Map (MRI) ← heatmap routing, section/dimension scoping
  - Slice 5 Plan Sections / Artifact Workspace ← editor, epistemic notation, event-driven reanalysis
  - Slice 6 Issues & Recommendations (Panel Model, DL-095) ← lifecycle Open→Addressed→Resolved (DL-094), evidence, resolution paths + "Apply this fix", clarifications
  - Slice 7 History & Confidence Trend ← append-only timeline, trend, false-confidence
  - Slice 8 Multi-Project Workspace & Awareness ← Dashboard, Notifications, Settings
  - Slice 9 Collaboration, Sharing & Export ← comments, share link, export (Alpha-scope)
  - Slice 10 Tiering & Limits (visibility-first) ← at-cap modal, upgrade/archive, plan chip

## Features → Routes/Screens (illustrative, from prototype ids)
- Intake composer (#onboarding, #analyzing) → Fast Pass trace (#fptrace)
- Orientation (#orient, #arrival) → MRI reveal (#mview-heat/#heatGrid)
- Overview (#exHome/Confidence hero, #confpill/#confpop, #ledger, #conftrend)
- Artifact editor (#artview/#artdoc, #artver)
- Finding panel (#findpanel), all-findings (#exFindings/#fa-list), filters (section/dimension/severity)
- History (#exHistory/#hist-list), Notifications (#notifpanel), Command palette (#cmdk)
- Limit modal (#limitModal), Export (#exportModal), Draft/Share (#draftModal)

## UX States
- Orientation state machine (provisional↔current, error/last-good/retry) — **Locked from docs** (subset wired)
- Empty states: none-found / none-under-lens / not-yet-analyzed / unavailable — **Locked from docs**
- Analysis state honesty (Still updating vs current) — **Locked from docs**

## AI Behaviors
- Event-driven reanalysis only — **Locked from docs**
- Clarification Requests (OSLO asks; you answer; you decide) — **Locked from docs**
- Simulated AI only in prototype (no real model/API) — **Locked from docs**

## Product Data Concepts
- Project · Plan artifacts (7 artifacts) · Issues→CAF (lifecycle Open→Addressed→Resolved) · Recommendations/Selected Path/"Apply this fix" · Confidence+band (5-band DL-086/098) · Reliability(Coverage·Evidence·Assessability) · PlanFact(Derived/Attested) · Clarification · History(append-only) · Comments · Notifications — **Locked from docs**

## User-Visible Constraints
- Free-tier visibility-first (honest limits, non-destructive archive, save-to-keep) — **Locked from docs**
- Tier numbers/prices illustrative (owner-TBD) — **Locked from docs**
- CRR (virality loop) — **Needs decision** (escalated spec gap; out of scope default)

## E2E User Scenarios (per slice, ≤20 each) — authored during slice grill

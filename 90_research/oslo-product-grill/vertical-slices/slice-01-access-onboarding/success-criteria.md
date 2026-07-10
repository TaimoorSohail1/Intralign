# Slice 1 — Access & Onboarding · Success Criteria

Acceptance criteria for the R1 (Alpha) access & onboarding funnel. Each maps to one or more decisions in `../../decision-log.md`.

## Access & phase gating
- **AC-1 (D021):** The Alpha default entry is the invitation/activation flow — the user is never anonymous. Anonymous access is presented only under a clearly-labelled GA preview.
- **AC-2 (D021):** The anonymous first-run, save-to-keep gate, and claim-through are visibly tagged "GA phase" and are inert in Alpha; they only fire when the phase preview is set to GA.
- **AC-3 (D022):** Activation is simulated end-to-end (invite email → activate → welcome) with no real auth; the invited email is pre-filled read-only; no password value is stored.

## Intake
- **AC-4 (D023):** Exactly four start methods are available — Describe, Attach documents, Templates, Sample project — and Guided step-by-step Q&A is absent.
- **AC-5 (D023):** The five template chips render with exact labels and order: Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan.
- **AC-6:** The primary CTA is disabled until there is a non-empty description, at least one attached document, or a selected template (minimum-to-value gate), with a visible hint.
- **AC-7:** "See it on a sample project" loads the DevNorth brief into the composer (so the user sees the input) and runs the standard analyze flow.

## Fast Pass → arrival
- **AC-8 (D005/D012):** Initial Analysis presents a rails-first hold with a streaming trace, staged interstitials, and an "Analyzing…" pill; the label is "Initial Analysis" (not "Fast Pass").
- **AC-9 (D005):** On completion the user lands on a stub Overview that clearly states later slices continue there, and Extended Analysis auto-runs non-blocking and supersedes the initial read (direction-only confidence move).
- **AC-10 (D002/D003):** The confidence pill is neutral (understanding maturity + reliability) and is never traffic-light colored.

## Orientation & advisory framing
- **AC-11 (D027):** A one-time, dismissible strategic-chain orientation shows on first arrival (Understanding·OSLO → Judgement·you → Decision·you → Oversight·you) and does not reappear once dismissed (proficiency flag persists across reloads).
- **AC-12 (D027):** The orientation is re-openable from the account menu.
- **AC-13 (D001/D027):** A persistent advisory footer ("OSLO advises; you decide — you stay in control at every step") is present on the authenticated app, and no copy implies OSLO plans/decides/runs the project.

## Session
- **AC-14 (D028):** The account menu offers Log out and a "Stay signed in" toggle; logout returns to the invitation/activation entry; with stay-signed-in on and an account present, reloading lands on intake.

## GA-phase behavior (under GA preview only)
- **AC-15 (D024):** In GA preview, an anonymous run executes Initial Analysis only (~10s framing, no signup) and lands on orientation.
- **AC-16 (D025/D026):** In GA preview, after orientation a save-to-keep bar appears; signing up performs claim-through, carrying the draft project through unchanged.

## Theme & accessibility
- **AC-17 (D015):** Dark is the default theme, using the exact v4 token values; Inter loads via CDN with a system-font fallback.
- **AC-18 (D015):** `:focus-visible` rings are present, custom toggles/checkboxes are keyboard-operable, and `prefers-reduced-motion` disables the analyzing animation.

## Build boundary
- **AC-19 (D016):** The prototype is a single openable HTML file that runs with no build step, no network dependency beyond the Google Fonts CDN, and persists state only in localStorage.
- **AC-20:** The prototype has no JavaScript console/parse errors on load or through the primary Alpha flow.

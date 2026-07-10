# Slice 2 — Intake & Fast-Pass Orientation · E2E Test Scenarios

Manual walkthroughs against `prototype.html` (client-side, simulated). ≤20 scenarios (Rev 2 covers D043–D046). Restart (top bar) clears localStorage between runs where noted.

| # | Scenario | Steps | Expected |
|---|---|---|---|
| 1 | **[S1] Activation funnel** | Restart → Activate → Create account → Start first project | Lands on intake composer; no anonymous access in Alpha (D022). |
| 2 | **[S1] Sample start** | On intake, click "See it on a sample project" | DevNorth brief loads into composer; CTA enabled; no auto-run (D030). |
| 3 | **Fast Pass runs ≈30s** | Click "See where I stand →" | Analyzing overlay: 4 interstitials, streaming trace incl. "constructed plan artifacts · 7 sections"; ~30s (D031/D036). |
| 4 | **[S1] First-run orientation** | After Fast Pass (fresh session) | Strategic-chain orientation overlay appears once; dismiss → Overview (D027/D039). |
| 5 | **Overview sections = Confidence/Start here/Progress/More** | Dismiss orientation; scan Overview | EXACTLY those 4 sections (DL-096/D046). Confidence: focal 58/100, "Understanding is forming", **reliability inline** ("qualified by moderate reliability"), CAF bars (Feasibility = the limit), no ring, **no standalone Reliability card**. |
| 6 | **Completion notice → OSLO chat, measured, fresh only** | Observe the OSLO chat rail (right) | Chat message "Initial Analysis complete in Ns — under the 60-second target" + "Take a quick tour →"; N measured, not fixed; **no arrival banner on the Overview** (D043/D036/D039). |
| 7 | **Six Fast Pass outputs present** | Scan Overview + chat | Confidence, Attention (switch + badge), Top issues (Start here), Clarification pointer (→ tied Issue), Suggested fixes (per-issue), Progress/Analysis status all reachable (D037). |
| 8 | **Seven plan artifacts** | More → "Plan artifacts (7)" | All 7 listed; each labelled **From OSLO** + reliability (D035). |
| 9 | **Attention Map reachable, heatmap** | Click "Attention" in top-center switch | Heatmap: 7 section rows × Clarity/Alignment/Feasibility cols; only issue cells colored; calm cells neutral (D003/D007/D038). |
| 10 | **Heatmap cell → issue** | Click the red Resources × Feasibility cell | Light Issue panel opens on "Venue Wi-Fi capacity is unconfirmed" (D042 panel). |
| 11 | **Dimensions toggle** | Attention → "⌖ Dimensions" | Three CAF cards; Feasibility flagged "the limit"; neutral bars. |
| 12 | **Extended Analysis auto-runs & supersedes → chat** | Wait ~6s on Overview after orientation | **Chat** message "Extended Analysis complete — superseded the provisional orientation" (58→62, Feasibility Very Low→Low); chip Provisional→Current; trend sparkline appears; Progress state line flips (status). **No Overview banner** (D040/D043). |
| 13 | **Analysis-state chip** | Observe hero chip before/after #12 | Amber "Provisional" → green "Current" (D040). |
| 14 | **Extended Analysis failure → chat** | Restart → arm "Sim Extended-Analysis fail" in the phase bar before ingesting → complete Fast Pass → dismiss orientation | **Chat** notice "couldn't complete — showing your last-good understanding · Retry"; read unchanged; chip "Last-good" (D041/D043). |
| 15 | **Retry recovers** | On the chat notice, click "Retry" | Re-runs; chat "complete"; recovers to Current (58→62) (D041). |
| 16 | **Feature tour (opt-in, spotlights ≥3 surfaces)** | Click "Take a quick tour →" in chat (or the left-rail affordance) | Spotlight coachmarks over Confidence, Start here, Attention switch, OSLO chat (4 steps); Skip/Back/Next; completing marks it seen (won't reappear); never gates value (D044). |
| 17 | **Clarification in-issue + close loop + confirmation** | Start here → "Answer the first →" (or open the tied issue) → type an answer → Submit & re-analyze | Panel "Re-analyzing…" → **resolved confirmation shown in the Issue detail** (not on the Overview, D045); issue count drops; Overview shows summary counts only; heatmap cell clears; section becomes **Confirmed by you** (D042/D011/D006/D045). |
| 18 | **Only reanalysis moves issues** | Inspect the issue panel | No manual "resolve" toggle; lifecycle Open→Addressed→Resolved shown; resolution comes via the clarification/reanalysis (D006/D018). |
| 19 | **[S1] Returning user — no completion notice/orientation** | With orientation already seen and stay-signed-in, reload | Lands on intake; if re-analyzed, orientation does not re-fire and the fresh completion notice is suppressed (D039). |
| 20 | **Accessibility + reduced motion** | Tab through Overview/Attention; enable OS reduce-motion | Focus rings visible; view switch keyboard-operable; spinner/pulse suppressed (D015). |

### Notes
- Scenario 14: the "Sim Extended-Analysis fail" trigger is demo scaffolding (arms the next Deep Pass to fail); it is not product chrome.
- All values (58/62, section counts) are illustrative, direction-only (ND-2); no fabricated canonical numbers ship (D036).
- **Rev 2 (2026-07-09):** completion notices now render in the OSLO chat rail, not as Overview banners (D043); the feature tour is opt-in and never gates value (D044); confirmations live in the Issue detail while the Overview shows summary counts only (D045); Overview sections are exactly Confidence/Start here/Progress/More with reliability inline (D046).

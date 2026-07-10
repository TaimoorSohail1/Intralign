# Slice 1 — Access & Onboarding · Workflows

Actor workflows for each feature. Three actors: **User**, **System** (client-side app + simulated persistence), and **AI Agent** (OSLO, simulated). OSLO is advisory-only (D001) — it never decides or acts for the user.

## 1 · Invitation & activation (Alpha) — D022
- **User:** opens the simulated invite email → clicks **Activate account** → enters display name + password → sets **Stay signed in** → clicks **Create account & continue**.
- **System:** renders the fixed sample invite; on activate, stores a simulated `Account` (`active:true`) + `staySignedIn`; advances to Welcome, then intake. No real auth (owner-TBD).
- **AI Agent:** not involved.

## 2 · Intake — four start methods — D023
- **User:** chooses one of Describe / Attach / Templates / Sample project; supplies evidence; when the start gate is satisfied, clicks **See where I stand**.
  - Describe: types a brief.
  - Attach: adds one or more documents (removable chips).
  - Templates: selects one of the five chips (seeds the composer).
  - Sample project: clicks "See it on a sample project" (loads the DevNorth brief, auto-starts after a short countdown, or "Analyze now").
- **System:** enforces the minimum-to-value gate (disables the CTA until description/document/template present); on start, transitions to the Fast Pass. Guided Q&A is not offered (out for R1).
- **AI Agent:** none yet (analysis begins in the next step).

## 3 · Fast Pass — Initial Analysis — D005/D012
- **User:** waits (or, in the sample path, may click "Analyze now").
- **System:** shows the rails-first hold, streaming trace, staged interstitial, and **Analyzing…** pill; runs a simulated timer (~60s Alpha framing / ~10s GA anonymous). Respects `prefers-reduced-motion` (no spinner/pulse). On completion, reveals the app shell.
- **AI Agent (simulated):** "reads inputs", "maps plan artifacts", "assesses Clarity·Alignment·Feasibility", "surfaces issues" — advisory framing only; produces an illustrative initial read (band + reliability).

## 4 · Arrival hand-off + one-time orientation — D027
- **System:** reveals the stub Overview and the persistent advisory footer; if `orientSeen` is false, shows the one-time strategic-chain orientation overlay.
- **User:** reads the chain (Understanding·OSLO → Judgement·you → Decision·you → Oversight·you) → clicks **Get started**; may later replay it from the account menu.
- **System:** on dismiss, sets `orientSeen` (proficiency sunset); starts the Deep Pass; lands the user on the stub Overview.
- **AI Agent:** presents the advisory chain framing — reinforces "OSLO advises; you decide."

## 5 · Deep Pass — Extended Analysis (auto, non-blocking) — D005
- **System:** kicks off Extended Analysis in the background immediately after orientation; updates the confidence pill to an illustrative initial band, then, on completion, shows a "superseded the initial read" note with a direction-only confidence move.
- **User:** free to explore during the run; nothing blocks.
- **AI Agent (simulated):** re-reads evidence, refines the assessment, supersedes the provisional read. Only reanalysis changes the assessment (no manual reanalyze in this slice).

## 6 · Session management — D028
- **User:** opens the account menu → toggles **Stay signed in**, replays orientation, or **Logs out**.
- **System:** persists `staySignedIn`; on logout, clears the simulated `Account` and returns to the invitation/activation entry; on next open, if signed-in + stay-on, lands on intake.
- **AI Agent:** not involved.

## 7 · GA-phase anonymous first-run + save-to-keep + claim-through (labelled) — D024/D025/D026
- **Precondition:** the phase preview is set to **GA** (annotated). In **Alpha/Beta** this workflow does not run.
- **User (anonymous):** runs a sample/own brief through Initial Analysis only (no signup) → lands on orientation → sees the save-to-keep bar → clicks **Sign up to keep** → enters email → **Save & keep**.
- **System:** runs the faster ~10s Initial Analysis; after orientation shows the save-to-keep bar; on save, performs claim-through — replaces anonymous state with an `Account`, carrying the draft project through unchanged; names/keeps the project.
- **AI Agent (simulated):** produces the same advisory initial read; Extended Analysis and keeping are gated behind signup.

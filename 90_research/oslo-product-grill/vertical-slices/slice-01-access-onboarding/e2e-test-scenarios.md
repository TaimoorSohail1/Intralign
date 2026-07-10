# Slice 1 — Access & Onboarding · E2E Test Scenarios

End-user scenarios only (max 20). Each is a click-through a human could run against `prototype.html`. Default phase is **Alpha** unless a scenario sets GA.

1. **Alpha entry is the invite, not anonymous.** Open the prototype → the simulated invitation email is shown (no anonymous intake). Confirm the "invite-only Alpha" copy.
2. **Activate account.** Click **Activate account** → enter a display name and password → click **Create account & continue** → the Welcome screen greets you by that name.
3. **Welcome to intake.** From Welcome, click **Start your first project** → the intake screen with the hero "See your plan like a strategic leader." appears.
4. **Start gate blocks empty intake.** On intake, confirm **See where I stand** is disabled and the hint "Add a description, a document, or a template to start" shows.
5. **Describe method enables start.** Type a brief in the composer → the CTA enables and the hint disappears.
6. **Attach method enables start (mixed accepted types).** Confirm the **Attach documents** control shows an accepted-types hint (PDF, DOCX, PPTX, XLSX, CSV, TXT, MD · up to 10 files, 10 MB each). With the composer empty, click **Attach documents** a few times → file chips appear with **mixed extensions** cycling across the accepted set (e.g. pdf/docx/xlsx/pptx/csv) and the CTA enables; remove the chips → the CTA disables again.
7. **Template method seeds and selects.** Click the **Event** chip → it becomes selected and the composer is seeded → the CTA enables. Confirm all five chips read Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan.
8. **Guided Q&A is absent.** Confirm there is no "guided / step-by-step / answer questions" intake method anywhere on the intake screen.
9. **Sample project is user-initiated (Alpha, D030).** In Alpha, click **See it on a sample project** → the DevNorth brief fills the Describe composer and the **See where I stand →** button enables → confirm analysis does **not** start on its own (no countdown/auto-run). Then click **See where I stand →** to start Initial Analysis yourself.
10. **Initial Analysis paces to ≈30s (D031).** Start analysis → confirm the "Analyzing…" pill, the rails-first hold, the streaming trace, four interstitial phases with rotating sub-copy, and the "Initial Analysis · about 30 seconds" caption; the flow runs roughly 30 seconds before landing.
11. **Arrival lands on the stub Overview.** After analysis, the app shell appears with an Overview stub stating "Overview / Attention (MRI) continues in Slice 2 / 3."
12. **One-time orientation shows on first arrival.** On first landing, the strategic-chain overlay appears with Understanding·OSLO → Judgement·you → Decision·you → Oversight·you → click **Get started** to dismiss.
13. **Orientation sunsets.** Reload (with stay-signed-in on) and run to arrival again → the orientation overlay does not reappear.
14. **Replay orientation.** Open the account menu → **How OSLO works (replay)** → the orientation overlay reappears.
15. **Extended Analysis supersedes.** On the stub Overview, wait → the confidence pill fills to an illustrative Moderate band and the deep-pass note updates to "Extended Analysis complete — it superseded the initial read" with a direction-only move.
16. **Confidence is neutral.** Confirm the confidence pill uses neutral styling (no red/amber/green health color).
17. **Persistent advisory footer.** Confirm the footer "OSLO advises; you decide — you stay in control at every step." is visible on the authenticated app.
18. **Stay-signed-in + logout.** Open the account menu → toggle **Stay signed in** off/on → click **Log out** → you return to the invitation/activation entry.
19. **GA preview — anonymous variant of the same sample (D030 + D024/D025/D026).** Set the phase toggle to **GA (annotated)** → confirm the sample method above is still available and the annotated block now describes the **anonymous, no-signup** layer → load the sample and run Initial Analysis (lighter ~12s, "Initial Analysis only · ~12 seconds · no signup" caption) → after orientation a "GA phase" save-to-keep bar appears → **Sign up to keep** → **Save & keep** carries the project through and names it. (In Alpha this bar never appears.)
20. **Reduced motion.** With OS "reduce motion" enabled, run Initial Analysis → confirm the scanner spinner and pulse are disabled while the rails-first hold and trace still render.

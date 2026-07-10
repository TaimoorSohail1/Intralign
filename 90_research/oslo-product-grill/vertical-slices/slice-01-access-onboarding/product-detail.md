# Slice 1 — Access & Onboarding · Product Detail

Detailed product behavior and requirements for the R1 (Alpha) access & onboarding funnel. Phase-gating is made explicit throughout. All decision IDs refer to `../../decision-log.md`.

## PD-0 · Release phase gate (governs everything below) — D021
- R1 is the **Alpha** release.
- **Alpha and Beta:** invite-only; users authenticated from activation; **never anonymous**.
- **GA:** anonymous product access begins.
- Consequence: **anonymity** (the no-signup first-run, D024), the save-to-keep gate (D025), and claim-through (D026) are **GA-phase** and MUST NOT be the Alpha default path. In the prototype they are present but labelled and inert in Alpha, live only under the GA preview.
- **Not gated by phase (D030):** the **Sample project** start method is an all-phase method. Only its *anonymous* + *save-to-keep* wrapping is GA-only. See PD-2 and PD-7.

## PD-1 · Invitation & activation — D022
- **Invitation email is simulated** (a rendered panel, not a real inbox). It shows the invited email, a unique activation token, and an **Activate account** CTA. Copy asserts invite-only Alpha and authenticated-from-activation.
- **Activation is simulated** (no real auth): email is pre-filled read-only; user supplies display name + password; a **Stay signed in** checkbox defaults on.
- On activation, a simulated `Account` record is stored (`active:true`) and the user proceeds to **Welcome**, then intake.
- Real auth provider and token issuance are **owner-TBD** — the prototype must not imply a specific provider.

## PD-2 · Intake — four start methods; Guided Q&A OUT — D023
- Exactly four methods:
  1. **Describe** (composer textarea; DevNorth brief placeholder).
  2. **Attach documents** (adds fake file chips; removable). **Accepted types (D033):** PDF, DOCX, TXT, MD, PPTX, XLSX, CSV (plus paste/typed text via the composer). Illustrative caps: ~10 MB per file, up to ~10 files — these are illustrative only and tier size rules are **owner-TBD (GA)**. The control communicates the accepted types and caps as a hint. Upload is simulated in the prototype (no file leaves the browser).
  3. **Templates** (five chips, exact labels/order): **Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan**.
  4. **Sample project** — an **all-phase, user-initiated** start method (D030). "See it on a sample project" **loads the real DevNorth brief into the Describe composer** (the user sees the input) and enables the start gate; it **does not auto-run** (no countdown/auto-ingest). The user reviews the brief and starts analysis with the primary CTA. In Alpha this runs inside the authenticated session; its anonymous/save-to-keep wrapping is GA-only (PD-7).
- **Guided step-by-step Q&A is OUT for R1** and is not implemented.
- **Start gate (minimum-to-value):** the primary CTA ("See where I stand") is disabled until there is a non-empty description, at least one attached document, or a selected template. A hint communicates the requirement.

## PD-3 · Fast Pass — "Initial Analysis" (≈30s) — D005/D012/D031
- Presentation: rails-first hold; spinning scanner; a staged interstitial of **four phases** (title + rotating sub-messages) that walks through the read; an **Analyzing…** pill; a streaming trace of steps (read inputs → extract plan artifacts → assess Clarity/Alignment/Feasibility → surface issues).
- **Ingestion depth (D034):** text is extracted from all supported types and synthesized into the seven plan artifacts — **Intent · Context · Scope · Requirements · WBS · Schedule · Resources**. Additionally, **structured tables** are extracted from spreadsheets/CSV and from in-document tables; their rows inform **Resources** and **Schedule**. **No OCR** of scanned/image-only content in R1 (owner-TBD later). In the prototype the depth is represented in the trace copy; extraction itself is simulated.
- User-facing label is **"Initial Analysis"** (internal: Fast Pass) — D012.
- Timing is **simulated** and paced to **≈30 seconds total (D031)**: the four phases hold ~8s / ~8s / ~8s / ~6s, with a sub-message rotating every ~2.6s so the read reads like a realistic flow. The Alpha caption is **"Initial Analysis · about 30 seconds."** In GA anonymous first-run the same rails run lighter/faster (~12s: 3.5 / 3.5 / 3 / 2s) and the caption reads "Initial Analysis only · ~12 seconds · no signup."
- **Reduced-motion:** the spinner and pulse are disabled; the hold, the paced ≈30s text steps, and the trace remain (no analysis animation) — D015.

## PD-4 · Arrival hand-off + one-time orientation — D027
- On completion the app shell shows with a **stub Overview** ("Overview / Attention (MRI) continues in Slice 2 / 3"). Slice 1 owns the funnel, not the Overview internals.
- **One-time strategic-chain orientation** overlay (dismissible): Understanding·**OSLO** → Judgement·**you** → Decision·**you** → Oversight·**you**. Dismissal sets a persistent proficiency flag (`orientSeen`, localStorage) so it does not reappear. Re-openable from the account menu ("How OSLO works — replay").
- **Persistent advisory footer** is shown on the authenticated app: "OSLO advises; you decide — you stay in control at every step."
- **Deep Pass ("Extended Analysis")** auto-runs non-blocking after orientation; when complete it supersedes the initial read. Confidence movement is **direction-only** (▲ 58 → 62 shown as an illustrative demo value; the real magnitude NFR is owner-TBD).

## PD-5 · Confidence presentation on hand-off — D002/D003
- The top-bar confidence pill starts in a "Forming / Initial read" placeholder, then shows an illustrative band (Moderate) qualified by reliability.
- Confidence is **understanding maturity**, never health/probability/readiness, and is rendered on the **neutral maturity ramp** — never traffic-light colored. Only severity (later slices) uses red/amber/green.

## PD-6 · Session management — D028
- **Account menu** (top-right avatar) contains: **Stay signed in** toggle (localStorage-simulated persistence), **How OSLO works (replay)**, and **Log out**.
- **Log out** clears the simulated session and returns to the invitation/activation entry.
- Real session length / idle-timeout policy is **owner-TBD** — the prototype only illustrates persistence.

## PD-7 · GA-phase capabilities (labelled; not Alpha) — D024/D025/D026 (scoped by D030)
- **Scope note (D030):** the Sample project *method* is not GA-gated (PD-2). What is GA-only is the **anonymous** framing and the **save-to-keep** gate + claim-through *layered over* the sample (or any brief). The annotated intake block describes/enables only this layer, not the method.
- **Anonymous first-run (D024):** at GA, an anonymous visitor runs the sample (or own brief) through **Initial Analysis only** (~12s, no signup) and lands on orientation. Extended Analysis and keeping require signup.
- **Save-to-keep gate (D025):** at GA, after orientation a save-to-keep bar appears; before signup the session is explore-only. In Alpha/Beta there is no such gate (the user already has an account, and the same sample runs authenticated with no anonymous/save-to-keep language).
- **Signup + claim-through (D026):** at GA, email-based save-to-keep (simulated); anonymous work is **claimed and carried through unchanged**.
- All three are rendered in the prototype but **only fire under the GA preview**; in Alpha they are visibly labelled "GA phase" and inert.

## PD-8 · Copy discipline — D001/D012
- Advisory-only: no copy implies OSLO plans/decides/runs the project.
- Plain-language labels: **Plan artifacts** (not Artifacts), **Issues** (not Findings), **Initial / Extended Analysis** (not Fast/Deep Pass). Internal canonical terms are preserved in code comments/data, never surfaced.

## Open / owner-TBD flagged in this slice
- Real auth provider & invitation/token mechanics (D022).
- Session length / idle-timeout policy (D028).
- Confidence movement magnitude on completion (direction-only in prototype).
- Tier numbers and enforcement (illustrative only; out of Slice-1 build).

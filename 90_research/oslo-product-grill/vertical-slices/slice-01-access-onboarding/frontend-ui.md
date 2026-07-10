# Slice 1 — Access & Onboarding · Frontend / UI

Routes/screens, components, content, interactions, and the exact theme tokens used. The look-and-feel is inherited 1:1 from `oslo_r1_experience_mockup_v4.html` so later slices stack cleanly. Prototype is a single self-contained HTML file (D016).

## Screens (state-switched, single-page)
The prototype is a single page whose top-level containers are shown/hidden by state (no router). Screens:
1. **`#phasebar`** — demo scaffold: release label + Alpha/GA preview toggle + Restart. (Not product chrome; frames the slice.)
2. **`#activation`** — Alpha entry. Three sub-steps: `#actEmail` (simulated invite email) → `#actForm` (activation) → `#actWelcome` (welcome).
3. **`#onboarding`** — authenticated intake (four start methods) + labelled GA first-run block + advisory footer.
4. **`#analyzing`** — Fast Pass "Initial Analysis" overlay (scanner, pill, interstitial, streaming trace).
5. **`#orient`** — one-time strategic-chain orientation overlay.
6. **`#app`** — app shell: topbar (brand · breadcrumb · confidence pill · account avatar), account menu, stub Overview body, persistent advisory footer.
7. **`#savebar` / `#signupScrim`** — GA-phase save-to-keep bar + claim-through modal.

## Components
- **Simulated invite email** (`.invite-mail`) — header row with mail icon + "simulated email" tag; body with To/subject/paragraph, mono token chip, **Activate account** button, expiry note.
- **Activation form** (`.act-card`) — read-only email, display-name + password inputs, **Stay signed in** custom checkbox (`.act-stay`, keyboard-operable), primary CTA, back link.
- **Welcome card** (`.welcome-card`) — success tick, greeting, CTA.
- **Composer** (`.composer`) — textarea + **Attach documents** button + file chips + start-gate hint + primary CTA (`#ingestBtn`). The **Attach** control communicates the accepted types (**PDF, DOCX, TXT, MD, PPTX, XLSX, CSV** — D033) and the illustrative caps (up to 10 files, ~10 MB each) via a small caption + `title`/`aria-label` hint; simulated chips cycle across mixed types (pdf/docx/xlsx/pptx/csv), not always `.pdf`.
- **Template chips** (`.sample`) — five, exact labels/order; selected state (`.on`).
- **Sample method link** (`#obAlt`, `.ob-alt`) — "See it on a sample project"; an all-phase, user-initiated start (D030). Loads the DevNorth brief into the composer; no auto-run.
- **GA anonymous-layer block** (`.ga-wrap`) — dashed, tagged "GA phase"; describes/enables only the anonymous + save-to-keep *layer* over the sample (not the method); **hidden entirely in Alpha (D032: `display:none`, not a dimmed/labelled card)**, shown only when the GA preview toggle is active.
- **Analyzing overlay** — `.scanner` (spinner), `.an-pill` ("Analyzing…"), `.int-title/.int-desc`, `.int-dots`, `.an-trace` (streaming mono trace), caption.
- **Orientation overlay** (`.orient-card`) — four `.ostep` cards, advisory foot line, **Get started** CTA.
- **Confidence pill** (`.conf-pill`) — neutral, "Confidence · index · band · reliability"; starts pending/forming.
- **Account menu** (`.acctmenu`) — identity row, **Stay signed in** toggle (`.am-toggle`), replay-orientation, **Log out** (danger).
- **Save-to-keep bar** (`.savebar`) + **signup modal** (`.modal`) — both tagged "GA phase".
- **Advisory footer** (`.advisory-foot`) — persistent line with ⓘ.

## Content (key strings — exact)
- Hero headline (D029): **"See your plan like a strategic leader."**
- Wordmark descriptor (D029): **"Strategic project leadership."**
- Hero sub: "Drop in a plan, brief, or notes. OSLO shows how clear, aligned, and feasible it is — and where the issues are."
- Advisory footer / advisory line: **"OSLO advises; you decide — you stay in control at every step."**
- Template chips: **Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan.**
- Analyzing caption: "Initial Analysis · about 30 seconds" (Alpha) / "Initial Analysis only · ~12 seconds · no signup" (GA anonymous). (D031)
- Orientation chain: Understanding·**OSLO** → Judgement·**you** → Decision·**you** → Oversight·**you**.
- Start-gate hint: "Add a description, a document, or a template to start."

## Interactions
- Composer input, template select, and file attach all feed the **start gate** (`checkIntake`); the CTA enables only when satisfied.
- **Attach** adds/removes fake file chips; simulated chip extensions cycle across the accepted set (pdf/docx/xlsx/pptx/csv, D033) so the demo reflects mixed types. A hint (caption + `title`/`aria-label`) states the accepted types and caps.
- **See it on a sample project** (D030) loads the DevNorth brief into the composer and focuses it; it is **user-initiated** — no countdown/auto-start. The user reviews it and clicks the primary **See where I stand →** to begin.
- **Fast Pass** advances four staged interstitial phases on a simulated timer paced to **≈30s** (Alpha; ~12s for the GA anonymous run), rotating a sub-message every ~2.6s; respects reduced motion (no spin/pulse, paced text steps remain).
- **Orientation** dismiss sets the `orientSeen` proficiency flag; replay via account menu.
- **Account menu**: toggle stay-signed-in, replay orientation, log out; closes on outside click.
- **Phase toggle** flips Alpha↔GA, enabling/disabling the anonymous/save-to-keep affordances.
- **Restart** clears flags and reloads.

## Theme tokens used (from theme-system.md / v4 baseline)
- Surfaces/text: `--bg #111315`, `--bg-2`, `--surface #1B1F24`, `--surface-2`, `--surface-3`, `--text #F5F4F0`, `--muted`, `--subtle`.
- Borders: `--border #343B44`, `--border-2`.
- Brand: `--primary #D97A3A`, `--primary-hover`, `--primary-light`, `--primary-fg`.
- Neutral maturity ramp (confidence): `--conf-low/-medium/-high` — **never health-colored** (D003).
- Severity ramp (`--danger`/`--warning`/`--success`) reserved for severity only; used in Slice 1 only for the neutral success tick / GA "phase" amber tag, not for confidence.
- Focus: `--color-focus` on `:focus-visible` (D015).
- Type: **Inter** (400–700) via Google Fonts CDN, degrading to system fonts; JetBrains Mono for the trace/index.
- Light theme overrides the same token names under `[data-theme="light"]`.

## Accessibility (D015)
- `:focus-visible` rings everywhere; custom checkboxes/toggles operable via Space/Enter with `role`/`aria-checked`/`tabindex`.
- `prefers-reduced-motion` disables the scanner spin and dot pulse and near-zeroes transitions.
- `color-scheme` set per theme; `aria-haspopup`/`aria-expanded` on the account button; `aria-hidden` on the inert GA block in Alpha.

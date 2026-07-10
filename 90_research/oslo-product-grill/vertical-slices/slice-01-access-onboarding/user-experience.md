# Slice 1 — Access & Onboarding · User Experience

OSLO R1 is the **Alpha** release. This slice owns the entry funnel end-to-end, from the invitation through to the moment the user lands on their project after Initial Analysis. It stops at the hand-off; the Overview/Attention internals belong to later slices.

## Inherited behavior
None. Slice 1 is the first cumulative slice — there is no prior slice to inherit from. It establishes the theme, the app shell chrome, the advisory framing, and the orientation pattern that later slices stack on.

## Phase gating (the spine of this slice) — D021
- **Alpha & Beta are invite-only.** Users are **authenticated from activation onward and are never anonymous** in these phases.
- **Anonymous product access begins at GA.** Therefore the anonymous first-run, the save-to-keep gate, and anonymous→claimed carry-through are **GA-phase** capabilities.
- In the prototype the release phase is a preview toggle in the top scaffold bar (**Alpha (default)** / **GA (annotated)**). The GA affordances are visibly present but clearly labelled and, in Alpha, inert.

## Primary Alpha flow (the default path)
1. **Invitation email (simulated).** The user sees a simulated invite email panel addressed to them, with a unique activation token and an **Activate account** button. Copy states the Alpha is invite-only and the user is authenticated from activation.
2. **Account activation (simulated).** A form pre-fills the invited email (read-only), takes a display name and password, and offers a **Stay signed in on this device** checkbox. No real auth — activation is faked (D022). Real auth provider is owner-TBD.
3. **Welcome.** A confirmation screen greets the user by name and invites them to start their first project.
4. **Authenticated intake — four start methods (D023):**
   - **Describe** — a composer textarea with the DevNorth sample brief as placeholder.
   - **Attach documents** — an upload affordance that adds file chips (fake files).
   - **Templates** — five chips: Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan.
   - **Sample project** — an **all-phase, user-initiated start method (D030)**. "See it on a sample project" **loads the real DevNorth brief into the Describe composer** so the user sees the input; it does **not** auto-run. The user reviews it and then starts analysis themselves with the primary **See where I stand →** button. (Only anonymity + save-to-keep are GA-only — see below.)
   - **Guided step-by-step Q&A is OUT for R1** and is not built.
   - The **See where I stand** button is gated: disabled until there is a description, a document, or a template (minimum-to-value).
5. **Fast Pass — "Initial Analysis" (≈30s simulated, D031).** A rails-first hold with a spinning scanner, a streaming trace, staged interstitial copy (four phases with rotating sub-messages so the read paces realistically), and an **Analyzing…** pill. The caption reads "Initial Analysis · about 30 seconds." Reduced-motion disables the spin/pulse animation but the ≈30s paced text steps remain.
6. **Arrival hand-off.** The app shell appears with a stub Overview. On first run a one-time, dismissible **strategic-chain orientation** overlay presents Understanding·OSLO → Judgement·you → Decision·you → Oversight·you. Dismissing it marks the proficiency flag (localStorage) so it does not reappear; it is re-openable from the account menu.
7. **60-second orientation + Deep Pass.** After the overlay, the user is on the stub Overview (a "Slice 2/3 continues here" placeholder). **Extended Analysis** auto-runs non-blocking in the background and, when complete, supersedes the initial read (direction-only confidence move, no fabricated jump).

## Session management (D028)
- An **account menu** on the top-right avatar contains: a **Stay signed in** toggle (illustrative persistence via localStorage), a **How OSLO works (replay)** action, and **Log out**.
- Logout clears the simulated session and returns the user to the invitation/activation entry (the Alpha re-auth path).
- If "stay signed in" is on and an account exists, re-opening the prototype lands the user straight on intake.

## GA-phase representation (labelled, not the Alpha default) — D024/D025/D026/D030
- The **sample method itself is available in every phase** (D030). What is **GA-only** is the **anonymous, no-signup** framing and the **save-to-keep** gate + claim-through. The dashed, annotated intake block now describes/enables *only that anonymous layer* — not the sample method (which lives with Describe/Attach/Templates above). In Alpha it is dimmed and inert with a "GA phase · not active in Alpha" tag and an explanatory note.
- Switching the top-bar preview to **GA (annotated)** makes the anonymous layer live: an anonymous visitor can run the **same sample** (or their own brief) through Initial Analysis only (a lighter ~12s read, no signup), land on orientation, and then meet a **save-to-keep** bar. Signing up opens a claim-through modal — the anonymous work is claimed and carried through unchanged.
- In Alpha/Beta none of the anonymous/save-to-keep behavior fires: the user already has an account from activation, so the same sample runs inside the authenticated session with no anonymous or save-to-keep language.

## Advisory framing (persistent) — D001/D027
- A persistent advisory footer reads **"OSLO advises; you decide — you stay in control at every step."** It is present on the onboarding screen and on the authenticated app.
- All analysis copy is advisory ("OSLO reads/maps/surfaces…", "advisory, never automatic"). No copy implies OSLO plans, decides, or runs the project.

## Accessibility (D015)
- Dark default theme; light overrides the same tokens.
- `:focus-visible` rings on all interactive elements; keyboard-operable checkboxes/toggles (Space/Enter), `role`/`tabindex` on non-native clickables.
- `prefers-reduced-motion` removes the analyzing spinner and pulse; the rails-first hold is preserved with no motion.

## New behavior introduced by this slice
- The activation/welcome funnel; the four-method intake with start-gating; the Fast Pass streaming-trace analyzing state; the one-time strategic-chain orientation with proficiency sunset; the account menu with logout + stay-signed-in; and the phase-gated, labelled GA anonymous/save-to-keep representation.

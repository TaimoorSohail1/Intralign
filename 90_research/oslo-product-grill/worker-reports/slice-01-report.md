# Worker Report — Slice 1: Access & Onboarding

**Slice:** 1 — Access & Onboarding (OSLO R1, the Alpha release)
**Date:** 2026-07-09
**Baseline reused:** `product-design/oslo_r1_experience_mockup_v4.html`

## Summary
Built the first cumulative vertical-slice deliverable for OSLO R1: the access & onboarding entry funnel end-to-end, from a simulated Alpha invitation through activation, welcome, four-method authenticated intake, the Fast Pass "Initial Analysis" state, the one-time strategic-chain orientation, and the arrival hand-off to a stub Overview (with Extended Analysis auto-running non-blocking). The prototype is a single self-contained HTML file — dark-default theme lifted 1:1 from the v4 baseline (canonical Intralign tokens, Inter font, orange primary, neutral maturity ramp), plain JS, localStorage flags, fake data, simulated timers, no build step. The seven spec docs and this report accompany it. JS parses cleanly (Node `new Function` check passed), script tags balance, no mojibake, and every inline handler resolves to a defined function.

## Decisions applied
- **D021 phase gate:** Alpha is invite-only and authenticated-from-activation; the anonymous first-run, save-to-keep gate, and claim-through are rendered but clearly labelled "GA phase" and inert in Alpha. A top-bar Alpha/GA preview toggle lets a reviewer see the GA path live without it being the default.
- **D022:** simulated invitation → activation → welcome; no real auth; email pre-filled read-only; password never stored.
- **D023:** exactly four start methods (Describe · Attach · Templates · Sample project); Guided Q&A not built; five template chips with exact labels/order; minimum-to-value start gate.
- **D024/D025/D026:** anonymous first-run (Initial Analysis only, ~10s), save-to-keep bar, and email claim-through — all GA-gated and annotated.
- **D027:** one-time dismissible strategic-chain orientation (Understanding·OSLO → Judgement·you → Decision·you → Oversight·you) with proficiency sunset (`orientSeen` localStorage flag) and replay from the account menu; persistent advisory footer.
- **D028:** account menu with Log out + "Stay signed in" (localStorage-simulated).
- **D029:** hero A "See your plan like a strategic leader." + descriptor "Strategic project leadership."
- **D001** advisory-only copy; **D012** plain-language labels (Plan sections, Issues, Initial/Extended Analysis); **D002/D003** neutral confidence pill (never health-colored); **D015** dark default + WCAG 2.1 AA (`:focus-visible`, keyboard toggles, `prefers-reduced-motion` kills the analyzing animation); **D016** client-side only.

## Files created
Under `oslo-product-output/vertical-slices/slice-01-access-onboarding/`:
- `prototype.html` — cumulative Slice 1 prototype (self-contained, opens by double-click).
- `user-experience.md`
- `product-detail.md`
- `product-data.md`
- `workflow.md`
- `frontend-ui.md`
- `success-criteria.md`
- `e2e-test-scenarios.md` (20 scenarios)
- `worker-reports/slice-01-report.md` (this report).

## Assumptions / interpretations (flagged, not invented spec)
- **Fast Pass timing:** the decisions say Fast Pass is ~60s in the authenticated flow but D024 says the anonymous first-run is ~10s. I framed the Alpha run with a "under 60 seconds" caption but kept the actual simulated wait short (~6s total) for demo usability, and used a faster ~10s framing/cadence for the GA anonymous run. This is a prototype pacing choice; real timing NFRs remain owner-TBD. **Flag if a literal ~60s wait is wanted.**
- **Confidence demo numbers (58 → 62):** carried over as illustrative from the v4 baseline; direction-only per the canonical-truth "ND-2 recommend direction-only." Not ratified values.
- **GA-phase representation approach:** I implemented it as a live preview toggle (Alpha default / GA annotated) rather than a purely static disabled variant, so the GA behavior is demonstrable while never being the Alpha default. This satisfies "shown but clearly labelled GA phase." **Flag if the owner prefers a strictly static/disabled variant with no live GA preview.**
- **Logout target:** logout returns to the invitation/activation entry (the Alpha re-auth path), since Alpha has no anonymous state to fall back to. Reasonable given D021; not separately specified.
- **Stub Overview:** kept deliberately minimal (a "Slice 2/3 continues here" placeholder) — Slice 1 owns the funnel, not the Overview internals, per the brief.

## Genuine spec gaps surfaced (owner-TBD; not assumed)
- Real auth provider + invitation/token issuance and validation (D022).
- Session length / idle-timeout policy (D028) — only illustrative persistence shown.
- Confidence movement magnitude on analysis completion (direction-only in prototype).
- Tier numbers/enforcement — out of Slice-1 build scope; left illustrative.

## Verification
- Node parse of the `<script>` block: OK. Balanced `<script>`/`</script>`. No replacement/mojibake characters. All 24 referenced inline handlers map to defined functions. No build step or network dependency beyond the Google Fonts CDN.

## Revision 2 (2026-07-09)
Two owner decisions applied by editing the existing Slice-1 deliverables in place (v4 dark theme and all working behavior preserved).

- **D030 — Sample project is an all-phase, user-initiated start method; only anonymity is GA.**
  - Moved **"See it on a sample project"** out of the GA-only gate; it is now a normal start method in the **Alpha default** intake, alongside Describe / Attach / Templates, for the authenticated user.
  - Made it **user-initiated**: `loadSample()` now loads the DevNorth brief **into the Describe composer** (the user sees the input) and enables the start gate — it does **not** auto-run. Removed the old `exploreSample()`/`analyzeSampleNow()` ~3s auto-countdown that kicked off ingestion. The user starts Fast Pass themselves via the primary "See where I stand →" CTA.
  - Kept **GA-only**: the **anonymous, no-signup** framing and the **save-to-keep** gate + claim-through. The `.ga-wrap` block was re-scoped to describe/enable *only that anonymous layer*, not the sample method. `setPhase()` no longer hides the sample link in GA (it's an all-phase method); it toggles just the anonymous layer live. Under GA the same sample runs anonymously with the "no signup" copy and a post-orientation save-to-keep prompt; under Alpha it runs in the authenticated session with no anonymous/save-to-keep language.
- **D031 — Fast Pass "Initial Analysis" paced to ≈30 seconds.**
  - Re-timed `ingest()` from a per-step `setInterval` (~6s total) to a per-phase `setTimeout` chain with an explicit duration array. **Alpha pacing: `[8000, 8000, 8000, 6000]` = 30,000ms (≈30s)** across the four interstitial phases; a sub-message rotates every ~2.6s within each phase so the read paces like a realistic flow. **GA anonymous run: `[3500, 3500, 3000, 2000]` = 12,000ms (≈12s)**, lighter/faster, Initial-Analysis-only.
  - Captions updated: Alpha now reads **"Initial Analysis · about 30 seconds"** (was "under 60 seconds"); GA anonymous reads **"Initial Analysis only · ~12 seconds · no signup"** (was "~10 seconds"). No "~10 seconds" copy remains for the Alpha flow.
  - Honest + skippable-safe; `prefers-reduced-motion` still disables the spinner/pulse while the ≈30s paced text steps and trace remain.

**Docs updated to match:** `user-experience.md` (intake methods + flow states + GA representation), `product-detail.md` (PD-0/PD-2/PD-3/PD-7 phase-gating + sample-method/anonymous split + ≈30s timing), `frontend-ui.md` (components, interactions, captions), `e2e-test-scenarios.md` (scenarios 9/10/19 rewritten for user-initiated Alpha sample, ≈30s Initial Analysis, and the GA anonymous variant; still 20 total). **Verification (rev 2):** `node --check` on the extracted script — OK; one `<script>` block, balanced; no mojibake; all inline handlers resolve (`exploreSample`/`analyzeSampleNow` removed, `loadSample` added); no residual "60s"/"~10 seconds" strings.

## Revision 3 (2026-07-09)
D032 — the GA-phase card / "GA PHASE · NOT ACTIVE IN ALPHA" annotation (`.ga-wrap`) is now **hidden entirely** in the Alpha default view (`display:none`, not a dimmed/labelled inert card); it appears only when the GA preview toggle is active (`setPhase('ga')` shows it, `setPhase('alpha')` fully hides it). Sample start method stays visible in all phases; GA toggle/behavior unchanged. `node --check` on extracted script: OK.

## Revision 4 (2026-07-09)
D033 (accepted attachment types: PDF, DOCX, TXT, MD, PPTX, XLSX, CSV + paste/typed; illustrative ~10 MB/file, ≤10 files, tier size rules owner-TBD/GA) and D034 (ingestion depth: text extraction from all supported types + synthesis into the 7 plan sections, plus structured-table extraction for spreadsheets/CSV & in-document tables informing Resources/Schedule; no OCR of scanned/image-only content in R1) reflected in place: `product-data.md` (`documents[].type` + caps + table-bearing rows), `product-detail.md` (PD-2 accepted types/caps, PD-3 ingestion depth), `frontend-ui.md` (Attach accepted-types hint + mixed-type chips), `prototype.html` (Attach caption + `title`/`aria` hint; `addFile()` cycles pdf/docx/xlsx/pptx/csv — still simulated), `e2e-test-scenarios.md` (scenario 6 mixed types; still 20). Theme/orientation/≈30s pacing/GA toggle/advisory footer/logout untouched. `node --check` on extracted script: OK.

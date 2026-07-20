# DL-156 — The two-beat journey, built — the four-stop axis, the beat threshold, and beat-aware Start here (amends DL-153)

- **Date:** 2026-07-20 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The two-beat journey, built — the four-stop axis, the beat threshold, and beat-aware Start here (amends DL-153)

**Class:** B (a build within the ratified two-beat model — no new identity scope) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-20 · **Realizes** the Class-A identity DL *(the journey gains its two beats)*; **amends DL-153** (the arc render + nesting). **Consumes** **DL-149** (`_execReadiness`), the **DL-146–150** model, and the existing issue engine. **Upholds** **D003/D183b**, **D179e**, **D196a**, **D088**, **D173**, **DL-145 §4**, **D179a**, **D195a**.

---

## Decision

The two-beat journey is **built into the deliverable prototype** on the Overview. Five pieces ship, each guarded:

1. **The four-stop axis** (`renderHeroArc`) — **Understand → Validate → Improve → Execute**, with an **Optimize bracket** (`.ovj-brk`) spanning Validate · Improve. Node state is **computed** from the stage: `now` (active), `done` (passed — a **cool ✓**, `--maturity`, never green, so it stays outside the RAG arc inside `.card.hero`), or `dest` (Execute, dashed ↗, never active). **Each node carries one metric**: Understand `done`/`read is in`, Validate `7 of 23` (coverage), Improve the band (`Moderate`), Execute `to Asana · anytime`.

2. **The behavioural, computed trigger** (`_planStage`) — replaces the backwards band≥High rule. **Understand** while `_execReadiness().confirmed === 0`; **Validate** while `frac < 0.5` (grounding the load-bearing set); **Improve** once `frac ≥ 0.5` (load-bearing confirmed → the read is reliable). Execute is never returned (destination). Computed, never authored (D173).

3. **The persistent read** (§6A) — the Outcome Confidence panel stays the always-visible first panel (D179a) in the inset `.ch-nest`, now with a neutral **"The read"** tab (no longer a stage tab, since the read is the through-line, not one node's detail). The panel markup is **byte-for-byte the ratified hero**, so its guards keep verifying. The nesting guard (was `_assertUnderstandDetailIsNested`, re-scoped) now asserts the read is nested + labelled + arc-preceded + spined — **not** that it is "Understand's" detail.

4. **Beat-aware Start here** (§6F) — `renderFocus` re-ranks the **same live open-issue set** via `_beatOrder`: on **Validate** (and the first-run Understand step) it leads with issues whose load-bearing assumption **grounds the read** (`_issueDerisk`); on **Improve** it leads with issues on the **limiter dimension** (`_beatLimiterDim` / `_issueOnDim`); severity breaks ties. A one-line beat intent (`.focus-beat`) states what the list is *for* right now. It is **computed** (D173), **advisory and non-blocking** (re-orders focus, never gates Execute), and carries **no tally** (D179e/D183g).

5. **Demo conveniences** (owner-requested) — *Sim first-run (Understand)* (`simFirstRun`, cleared on the first confirm) makes the Understand→Validate reward demoable; *Replay onboarding* (`demoReplayOnboarding`) clears the first-run localStorage flags and reloads, reproducing the real strategic-chain-orientation → tour-offer path rather than special-casing it. Both live in the Simulate ▾ menu; neither touches product logic.

## Guardrails

- **The arc is honest, and four-node** — `_assertHeroArcIsHonest`: exactly four nodes, one computed active node equal to `_planStage()` (Understand/Validate/Improve), an Execute destination never marked active, and **no forecast/health vocabulary** (D003/D183b).
- **The read is persistent + nested** — the re-scoped nesting guard: the Outcome Confidence heading + ramp are descendants of `.ch-nest`, the tab is present, the arc precedes the read, the active node drops its spine. The read never disappears across beats (D179a).
- **Start here follows the beat** — `_assertStartHereFollowsTheBeat`: on Improve the lead is on the limiter dimension (if any open issue is); on Validate the lead has a grounding assumption (if any open issue does). Otherwise the beats are cosmetic — this fails the boot.
- **Coverage and maturity stay distinct** — each node sources one metric; they are never fused into a single score (level ≠ trust; full coverage ≠ a high read).
- **Cool accent only** — the done ✓, the active dot/spine, and the read tab use `--maturity` (hue ≈ 214°); the whole-card colour cascade confirms no RAG hue and no `--primary` on state elements. The Optimize bracket is neutral grey.
- **Non-blocking + D088** — Execute never gates; crossings/coverage are immediate, the band moves only at an analysis update.
- **Class-resolve clean (D195a)** — new classes `ovj-brk`, `ovj-brk-lab`, `ovj-stage.done`, `focus-beat` all carry CSS.

## Verification

Built + verified in the deliverable prototype: **md5 `a327d702` · boot self-check 157/157 · 0 pageerrors · FAILS none** (guard count 156 → 157 for `_assertStartHereFollowsTheBeat`; `_assertHeroArcIsHonest` re-pointed to four nodes + Validate/Improve; nesting guard re-scoped to the persistent read). The Overview renders the four-stop axis with the active node computed (the demo's 7-of-23 lands on **Validate**), the Optimize bracket over the two beats, the persistent read below, and Start here carrying the beat intent. *Sim first-run* shows Understand active at "0 of 23" and the first confirm crosses into Validate.

## Scope · known follow-ons (logged, not silently dropped)

- **The demo's Start here doesn't visibly reshuffle** across beats because the seeded lead issue (ISS-01, Venue Wi-Fi) is simultaneously top-severity, on the limiter dimension, and grounding — so it leads in every beat. The mechanism + guard are real; a demo dataset that surfaces the re-ranking is a later refinement.
- **Per-beat inline detail** (Validate opening into an inline confirm-list, Improve into the read, with the two-dot beat sub-indicator from the mock) is deferred; the arc's body copy + the persistent read + Start here serve the beats' detail today.
- **The coverage-bar treatment (§6C)** — ensuring Validate's count never reads as a burndown-to-ready — is carried as an open build refinement.

## Governance

Lands as **Class-B** canon via `dl-land`, realizing the two-beat identity DL and amending DL-153. Built + verified in the deliverable prototype (157/157, 0 pageerrors). AI drafted + built; **only the owner ratifies.**

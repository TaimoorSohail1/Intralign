# R2 completion checklist — freemium tier

*Living checklist · 2026-08-04 · R2 build scope = FREEMIUM ONLY. Canonical prototype:
`oslo-prototype-r2.html` (Mac: …/OSLO Knowledge Base/oslo-prototype-r2.html).*

## To complete R2 (freemium)
- [x] **1 · Terminology sweep — "project" → outcome / plan.** ✅ DONE (2026-08-04). **Outcome** is now the
  top-level user-facing unit (outcome-forward, DL-158): switcher "Outcomes / New outcome", Projects door
  "Outcomes / New outcome / before an outcome opens", `_DOOR_T` "◱ Outcomes", menu "Outcomes & new outcome",
  welcome "Start your first outcome", intake aria-label + copy "your outcome", workspace/collaboration
  descriptions, VM-1 modal unified to "Add a second outcome" (both entry points). **plan** kept for the
  document/read input; **workspace** kept for the container; role title "project PM" kept. Internal keys
  (`openDoor('projects')`, `id="projPick"`, `showStage`, `vmOutcomeCap('plan')` telemetry code) unchanged.
  Verified: no stray user-facing "project" in the DOM; VM moments fire; 20/20 `_S10` green; 0 JS errors.
- [x] **2 · Ratify the freemium alignment into canon.** ✅ DONE (2026-08-04) — **DL-172** (freemium value
  moments & the unit of value: the outcome; R2 freemium-only; Alpha intent-capture; neutral tier copy; archive;
  handoff ladder; collaboration axis). Extends DL-158; supersedes project-as-unit / analyses-as-limit / "Basic
  10 seats". Status Ratified (Idris), staged in `release-2/`; withheld from `main` until R1 graduation.
- [x] **3 · Validation pass.** ✅ DONE (2026-08-04) — `oslo-r2-freemium-validation.md`. Verdict: freemium R2
  **holds together** across personas (outcome unit coherent, VM-1 exemplary, archive honest, neutral copy reads
  as candor). One friction found + **fixed in-pass**: VM-2 fired on every attach → now the attach just attaches
  and the envelope mirror fires only from a "simulate a larger upload (demo)" over-limit trigger. No blockers to
  ratify. 20/20 `_S10` green, verify_regress green, 0 JS errors.
- [x] **4 · Define "routed = owner-activation."** ✅ DONE (2026-08-04) — **DL-173**: activation = the first
  grounding act (confirm · flag · **route**), segmented by role; a route is the delegating owner's activation.
  Matches the product (routeTo→unlock); no code change needed. Status Ratified (Idris), staged in `release-2/`.

## ✅ R2 FREEMIUM COMPLETE — all 5 checklist items done (pending graduation from `release-2/` to `main`).
- [x] **5 · Decision: the optional "multiple outcomes" static preview.** ✅ DROPPED (owner, 2026-08-04) — it
  would preview a paid capability, against the neutral / no-paid-tiers stance. Never built; nothing to remove.

## Added post-completion (freemium, all users)
- [x] **In-app feedback + readiness survey.** ✅ DONE (2026-08-04). New **"✎ Feedback & rating"** door (menu +
  `_DOOR_T` + `doorBody`). Two honest capture surfaces: **(1) Product feedback** — defect / enhancement / other,
  filed as a **triageable ticket**. A **defect** ticket carries structured **"What happened" + "What did you
  expect" + impact** (Blocking me / Slowing me down / Minor), auto-attaches *where the user is* (view · role ·
  grounded X/Y · first-run flag) for reproducibility — with an explicit note that **no plan content leaves, only
  location + state** — and gets an auto **ticket ID** (`DEF-####` / `ENH-####` / `NOTE-####`, per-type sequence)
  surfaced in the confirm toast, plus a **"Filed this session"** list (id · title · Filed). **(2) Readiness
  survey** — the **Sean Ellis PMF question** ("How would you feel if you could no longer use OSLO?" · Very /
  Somewhat / Not disappointed — the ~40%-"very" bar is the broader-access gate) + a **1–5 experience rating** +
  one open "what would most improve it." Both persist in-memory (`_FEEDBACK_LOG` / `_SURVEY_LOG`; backend
  persistence is a build-phase task). Honest submit copy: **feedback goes to the team; it never changes your
  read, band, or issues**; the survey is **a readiness signal for us, not a verdict on your work**. Folded into
  `_S10` (now **23** checks: `feedbackCapturePresent` + `defectTicketFormat` +
  `surveyTriggerFiresOncePostActivation`). Verified: 23/23 green, verify_regress green, 0 JS errors; defect files
  DEF-#### with structured fields + auto-context, IDs increment, enhancement/other stay single-field, empty
  submit guarded, filed-list renders.
  **Discoverability + trigger (2026-08-04):** feedback is **always available** — persistent **"✎ Feedback &
  rating"** entry pinned in the **left-rail foot** (`.sb-foot`, next to the tour/account; best-practice
  secondary-nav placement) plus the menu item. The **readiness survey is triggered**, not just pull: a
  **fire-once, dismissible** nudge fires **only post-activation + engaged** (`_isActivated` confirmCount≥1 +
  `_isEngaged` past unlock, confirmCount≥3 — i.e. value experienced; asking first-run users inflates
  "not disappointed" and misreads the ~40% bar). Cool-toned (never action-orange), sits below the work list, and
  goes quiet after answer or dismiss. Internal `_SURVEY_TRIGGER_AB` knob ('immediate' vs 'delayed') staged for a
  later live A/B on timing.

## Done (freemium R2, this session)
Unit = outcome (ratified) · archive/reactivate (Free = 1 active outcome) · VM-1a/1b/2 intent-capture moments ·
neutral paid-tier copy (no tier names/prices user-facing) · analyses reframed to fair-use · viral primitives
free · one-tap activation (J-H1/U1) · forecast-framing (N2) · owner "Your outcome" dashboard (N3) · growth
invite loop + reach fix (U-1) · retention hook · engaged-tail density (U-2) · owner needs-triage (P-1) · agile
framing persistence (P-2) · label→button + scrollbar + resolved-card fixes · in-app feedback + readiness
survey (PMF + rating; defects filed as DEF-#### tickets w/ auto-context; persistent left-rail entry +
post-activation fire-once survey nudge) · `_S10` self-check harness (23).

## POST-R2 — NOT in scope (paid-tier capabilities)
VM-3 continuous monitoring (Pro) · auto-import + two-way sync (Basic) · CM-1 seated collaborator + CM-2 enforced
governance (Team) · roll-up / portfolio (Enterprise) · sprint-schedule lens (deferred product decision).

## Implementation note (not prototype work)
Intent telemetry is in-memory in the prototype (`_INTENT_LOG`); real persistence/wiring is a build task for the
implementation / product-grill phase.

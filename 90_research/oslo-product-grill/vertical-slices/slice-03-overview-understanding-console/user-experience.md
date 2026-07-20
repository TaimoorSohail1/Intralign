# Slice 3 — Project Overview & Understanding Console · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** Slice 1 + Slice 2 + Slice 3.
**Baseline of record:** frozen prototype (md5 `a327d702`, boot 157/157).
**Boundary:** advisory-only (D001); Outcome Confidence = understanding maturity, neutral, never health/readiness/probability (D002/D003/D183b); severity colour only on issues (D003); dark default + WCAG 2.1 AA (D015). Client-side prototype only (D016).

> This document notes what is **INHERITED** from Slice 1/2 (unchanged) and what is **CURRENT in Slice 3**. Nothing from Slice 1/2 regresses. **This is a regeneration to match the frozen build** — the original slice-03 grill (0–100 index, "How this is calculated" pill, Orientation ▸ Expanded ▸ Validated stages) is retired; those surfaces no longer exist.

---

## What Slice 3 is

Slice 3 is OSLO's **Overview** — the confidence-and-understanding console a PM lands on after intake. It does not add screens. It is one hero card that frames **the plan's journey to the outcome** (a computed arc) above the **always-visible Outcome Confidence read**, followed by **Start here** (what to do next) and **Progress** (where you stand). The top bar carries the read as a compact chip + on-demand popover.

The organising idea (DL-152→156): the Overview answers "how ready is my plan?" by **position on a journey**, not by a score. The journey is **Understand → ⟮Optimize: Validate · Improve⟯ → Execute**, "on the way to the outcome." Every position is **computed from state** (D173); there is no forecast and no health anywhere (D003/D183b).

---

## INHERITED (unchanged)

- **Slice 1:** invite → activate → welcome funnel; four start methods; anonymous + save-to-keep; one-time strategic-chain orientation + advisory footer; account menu; sample = all-phase, user-initiated.
- **Slice 2:** intake constructs all 7 plan documents, reliability-qualified, thin evidence → clarifications; Fast Pass ≈30s framed under the 60-second target; land on the **read-led Overview** with the Attention map co-primary; Outcome Analysis auto-runs, non-blocking, supersedes provisional→current; failure → last-good + retry; the **clarification loop** (a light prompt in *Start here* + the question/answer inside the tied issue → analysis update → issue closes); completion notices via OSLO chat; optional feature tour; confirmations live in the issue detail (Overview shows guidance, not a tally).
- **App shell:** persistent left sidebar (Overview live · Issues · History · Inference map · Reports · Documents · Full plan), top bar, command palette, chat rail. Chrome stays neutral/brand; severity colour on issues only.

---

## CURRENT in Slice 3 — the Overview surface, top to bottom

### 1. The journey arc (`#ov-arc`) — DL-152/153/154/155/156

A slim top-line frame over the read. Label: **"Your plan, on the way to the outcome."** Four nodes on one axis:

- **Understand → Validate → Improve → Execute**, with an **"Optimize" bracket** spanning Validate · Improve (the mission word stays on the axis).
- **Understand** is a **first-time milestone** (behavioural trigger `_planStage`): you leave it the moment you take your first optimization action — your first confirmed detail (coverage > 0). It shows a ✓ *done* mark afterward. Returning users are already past it. This replaces the retired band≥High rule (the old rule was backwards — optimizing is what raises the band).
- **Validate** carries **execution-readiness coverage** (`_execReadiness`, e.g. "7 of 23") — the WBS · Schedule · Resources statement subset, confirmed vs inferred. It is the beat where you confirm OSLO's load-bearing inferences so the read becomes **trustworthy**.
- **Improve** carries the **maturity band** (the Outcome Confidence read below). It is the beat where you raise the now-trustworthy read.
- **The two metrics are NEVER merged** (level ≠ trust — you can be 23 of 23 and still Moderate). Each node owns exactly one metric (D179e).
- **Execute** is a **destination** — dashed ↗ node, meta "to Asana · anytime." It is always reachable (export is non-blocking, DL-145 §4), **never the active node, never a "ready" verdict.**
- The **active node is computed** from state (`_planStage`): first-run/no coverage → Understand; coverage below half of load-bearing → Validate; load-bearing confirmed (frac ≥ 0.5) → Improve. The active node drops a spine toward the read below it.
- A **body line** explains the current beat and always offers "Execute whenever / Review & execute →" with "nothing is gated."
- **Honesty guard** `_assertHeroArcIsHonest`: exactly 4 nodes, exactly one computed active node equal to `_planStage()`, Execute is a destination never active, and no forecast/health vocabulary ("on track", "likely", "ready to succeed", "at risk"…) anywhere. The arc uses only the cool `--maturity` accent — never brand-orange on state, never RAG.

### 2. The persistent read (`.ch-nest`, tab "The read") — Outcome Confidence (D179a)

Nested directly below the arc, **always visible** — the beats change what you act on, never whether the read is shown (guard `_assertUnderstandDetailIsNested`). Top to bottom:

- **Heading "Outcome Confidence"** + info tip (the method's essence lives here: the weakest of Clarity · Alignment · Feasibility sets the level; a confident read on thin evidence is flagged; it moves only when something real changes) + the **neutral analysis-state chip** (Provisional while Outcome Analysis runs → Current when it completes, D175 — the labels are unchanged from D040, but the colour is gone; a **dot + word** carry it by weight and shape, never hue).
- **The lead-line** (`#ov-leadline`, DL-132) — OSLO's read as one plain-language sentence: the band paraphrased in plain maturity words, the computed limiter named, and a pointer into Start here. **Never a number or percentage** (that would read as a forecast). It is a **first-time nudge that sunsets** after the user first engages with Start here (follows the pointer, opens an issue, or confirms) — it never cycles to the next issue.
- **The maturity ramp** (`#ov-ramp`, D174/D003) — the hero. Five ordinal bands **Very Low · Low · Moderate · High · Very High**; the current one is **lit and named**, computed from the read. Neutral: **no percentage fill, no health colour.** A band move is drawn on the ramp (previous ghosted, current lit, arrow between) — only when a move actually happened.
- **The limiter** (`#ov-limit`, D186c) — the lowest CAF dimension, computed, with a grounding-aware verb: thinly evidenced → "Confirm it to lift the read"; no statements yet → "Bring evidence to firm it"; well-grounded → "A plan gap to fix." It **stays a limiter** — never a "Blocker" (low Feasibility is a fact about the *read*, not a warning about the *plan*). The phrase "holding it back" is gone.
- **The payoff** (`#payoff`) — a dismissible "What changed" delta strip, ≤20 words, computed from the previous snapshot (D179b). It never displaces the state above it and carries no counts (those live in Progress). `dismissPayoff()` clears it and the ramp ghosts.
- **The CAF rows** (Clarity · Alignment · Feasibility, Option C DL-123/124) — each row is a mini ramp + level word + a **per-dimension evidence cue** (e.g. "Mostly inferred · 1 of 3") + a "the limit" marker on the lowest. **Level ≠ trust:** the evidence cue is provenance, never folded into the band (no discount). Clicking a row toggles a drill-down (drivers: grounded/inferred split, open issues by severity, the lift, the finding-type cut) — the band stays a band; only drivers are quantified.
- **The grounding rollup** (`#ov-grounding`, D179e) — the **one home** for global grounding: e.g. "20 of 48 statements **Confirmed by you** · 28 **From OSLO** · ✓ largely grounded." It names both ratified epistemic classes and the statement unit; the ✓ marker appears only while the read is live-largely-grounded (never a "you lost it" negative).
- **The footer** — the **trend chip** (direction + word only, D056; routes to History; shown **only when the read actually moved** — a held read shows nothing) and **"Why ▾"**, which opens the reliability basis (Coverage · Evidence · How assessable), the neutral **false-confidence flag** when it holds (D052 — a high band on low reliability, disclosed neutrally, never RAG), and **"✦ Ask OSLO a follow-up →"** (hands the read to the chat).

### 3. Start here (`#ovStartHere`, `renderFocus`) — beat-aware guidance

The top open issue(s), **re-ranked by the current beat** (`_beatOrder`), never a static severity queue:

- On **Validate** (and the first-run Understand step): lead with issues whose **load-bearing assumption grounds the read** — confirming them makes the read trustworthy.
- On **Improve**: lead with issues on the **limiter dimension** — resolving them lifts the level.
- **Severity breaks ties** in both, so the list is always still severity-sane.
- A one-line **beat intent** (`.focus-beat`): "Confirm these to make OSLO's read trustworthy" (Validate) / "Resolve these to lift the read — your limit is Feasibility" (Improve) / "Confirm your first detail to make OSLO's read yours" (Understand).
- The lead issue carries an inline **"✦ Confirm first"** de-risk (`startInlineConfirm` — attest its load-bearing assumption in place) plus **"Review the issue →."** Secondary items list below; standalone confirmations (limiter with no open issue) point to the Inference map.
- **Computed, advisory, non-blocking, and it carries NO tally** (D179e/D183g). Guard `_assertStartHereFollowsTheBeat`.

### 4. Progress (`#ovProgress`) — pure work-state + the maturity ladder

- **Pure work-state:** Open (issues · critical · open questions) and Closed (resolved · answered). **No burndown grammar** — no completion %, no "N remaining", no target to drive to zero, no RAG. A rising issue count is a **deeper read, never a regression.**
- **The maturity-ladder rung** ("Grounded · 3 of 5", DL-129) — Oriented → Corroborated → Grounded → Anchored → Validated, **computed from evidence** (grounded share, load-bearing statements, stakeholder corroboration), never from running an analysis. Monotonic-with-work; a milestone is a timestamped event, never a revocable badge.
- **Which of Start here vs Progress leads is computed** (`_orderOverview`): first-run (no value earned yet) → **Start here first** (there is no progress to read); after first value → **Progress first** (the user knows what to do and wants to know where they stand). Same principle as D179a — state outranks event.

### 5. Top-bar Outcome Confidence chip + popover (`#confpill` / `#confpop`) — D050/D051

- The always-visible **chip** carries the label "Outcome Confidence" + the **band** (`#cp-band`) + the **ladder rung** (`#cp-grd`, e.g. Grounded). **DL-130 cut the standalone grounding word** from the chip — the rung already says it, and two quality scales in the top bar read as a stutter.
- Clicking opens the **popover** — the on-demand full breakdown: band + grounding word, the three CAF bands (limiter marked), the limiter verb, one computed "way out", the **reliability basis** (Coverage · Evidence · How assessable, on demand), a **trust-check** (calm "✓ Sound basis" when no leg is thin / loud "Read this with care" naming the thin leg when it is — **never celebrated**), and the false-confidence flag when it holds.
- Reliability is judged **independently of CAF** (D051): it says how firm the read is, not how good the plan is. It is also reachable from the Overview "Why" in prose; **there is no separate reliability card** (D046).

---

## Journey (Slice 3 lens)

1. Activate → intake → Fast Pass ≈30s (inherited) → land on the read-led Overview. First run: the arc sits at **Understand**, the lead-line pulls you into Start here, and Start here leads over Progress.
2. **Confirm your first detail** (the lead issue's "✦ Confirm first", or a standalone confirmation) → coverage ticks, the arc crosses **Understand → Validate** immediately, the lead-line retires, and Progress now leads.
3. Keep confirming load-bearing inferences → coverage rises. When load-bearing is confirmed (frac ≥ 0.5) the arc crosses to **Improve**; Start here re-ranks to the limiter dimension.
4. **Outcome Analysis** supersedes (auto or after a confirm) → the state chip flips Provisional → Current, the band may move on the ramp, the payoff shows "What changed", the trend chip appears if the read moved. **The read moves only at an analysis update** (D088) — confirming crosses a node and ticks coverage instantly, but the band does not jump on the confirm.
5. **Execute** is reachable the whole time (dashed destination) — nothing is gated.

All calls stay with the user (D001). OSLO reads and explains; nothing changes the plan without the user.

---

## Chat integration (inherited, adapted to Slice 3 surfaces)

The OSLO rail is a real conversation grounded in the read on screen (advisory, D001). "✦ Ask OSLO a follow-up" on the Why box hands the read to the chat (the deep answer: limiter, all three CAF rows, the reliability basis, the ladder rung, the false-confidence condition when it holds, and what would move the read). The issue panel hands any issue to the chat. Answering a clarification in the chat does exactly what answering in the issue panel does — same analysis update, same closure. The chat mutates nothing; every action is a link to a function that already exists, and it never claims to have closed an issue itself.

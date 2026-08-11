# Storyboard spec — the personalized "Outcome Orchestration" onboarding arc

**Status:** DRAFT spec for owner review. Merges the 60-second narrated script with the current reveal, per the persona audit (`ONBOARDING_ARC_PERSONA_AUDIT_2026-08-08.md`). Segment: *analyzing* beat → pre-activation. Ends at the **first decision** (activation).

## 1. What changes vs. the current flow
The current pre-activation is `_GR_BEATS` — four graph beats that teach the integrity model (outcome-at-center, "most of it is a guess," "uncertainty propagates upward," "confirm your outcome"). It's mechanism-first: it explains *what OSLO does* before establishing *why the PM should care*. This spec keeps the existing visual engine and re-sequences it under a **why-first** narration, adds the two missing beats (the identity shift and naming the discipline), personalizes every scene with the ingested plan, and runs it as **two modes over the same ~60s of unavoidable fast-pass processing**.

**Reuse (already in the prototype):** `_grBuild` (outcome→deliverables→workstreams→tasks→inference/evidence tree), the beat flags `plan/col/chip/exem/trace/focus/conf`, inference-marker rendering (faint hollow nodes), the pillar chips (Viability/Grounding/Adaptability), the upward-trace path, the analyzing ring (`_anBuildRing`), and the `gr-conf` confirm panel (activation).
**Net-new:** Scene 3 (identity shift / role reframe), Scene 5 (name the discipline), the two-mode controller, the processing-progress binding, and per-scene personalization tokens.

## 2. The time budget — sync the arc to processing, don't stack them
The fast pass takes **up to ~60s regardless**. The arc **is** the cover for that wait, not overhead on top of it. So:
- **Total default runtime = the processing duration** (target ~50–60s, but **event-driven, not fixed**: the arc advances on a floor timer but the *final* hand-off waits for `analysis-complete`).
- If processing finishes early, the arc can compress the tail; if it runs long, Scene 4/6 hold on a live "still reading…" state rather than stalling on a dead frame.
- **Never gate activation on the animation** — gate it on `analysis-complete`. The narration is pacing, not a lock.

## 3. Personalization data contract (from the ingested brief)
Every scene binds to the user's real plan; nothing is generic. Required tokens (all already produced at ingestion/analysis):

| Token | Source | Used in |
|---|---|---|
| `primaryOutcome.text` | intake / `_primaryOutcome()` | Scenes 1, 3, 6 |
| plan tree (deliverables→workstreams→tasks) | `_grBuild` on their plan | Scenes 2, 3, 4 |
| inferred nodes (count + which) | analysis (`state:'inferred'`) | Scenes 2, 4 |
| one real load-bearing inference + its upward path | analysis (`trace`) | Scenes 2, 4 |
| the three pillar reads (Viability/Grounding/Adaptability) | `viaLevel/grdLevel/adaLevel` | Scene 4 |
| the first decision (outcome-level) | `gr-conf` target | Scene 6 |

If a token is missing (thin brief), the scene degrades to the model-level statement — but **never** fabricates specifics.

## 4. Scene-by-scene storyboard

> Format per scene: **Narration · Visualization · Personalization · Mechanic (reuse/new) · Notes.** Timings are floors; the tail is event-driven (§2).

### Scene 1 — The Outcome (0–8s)
- **Narration:** "Every project begins with an outcome — that's what you're responsible for delivering."
- **Visualization:** a single glowing outcome node in the distance; a faint path forming toward it; slow push-in. No UI chrome.
- **Personalization:** the node **is their outcome** (`primaryOutcome.text`), not a placeholder.
- **Mechanic:** reuse the outcome-root node from `_grBuild` (the center node), pre-graph. **New:** the "distance / push-in" camera treatment.
- **Notes:** owner's language from second 1 — the biggest single lever for the non-technical-owner segment.

### Scene 2 — The Living Hypothesis (8–20s)
- **Narration:** "Today, AI can generate a plan in seconds. But generating a plan isn't the same as achieving the outcome. A plan is a living hypothesis for how the outcome will be achieved."
- **Visualization:** the plan constructs rapidly around the outcome (nodes connect); then subtle uncertainty — a few assumptions surface, **inference markers** appear, a couple of paths branch; the graph "breathes."
- **Personalization:** it builds **their** plan tree; the markers are **their** actual inferred nodes.
- **Mechanic:** reuse `_grBuild` growth + the `col/exem` inference-marker rendering (faint hollow nodes). This is today's beat-1/beat-2 visual, re-narrated.
- **Notes (audit):** the construct must **not** read as a static Gantt/document, or the scrum-PM rejects the metaphor — keep it as a living graph that breathes.

### Scene 3 — The Identity Shift (20–34s) · NET-NEW
- **Narration:** "As AI makes planning and execution easier, your value shifts. Your role isn't just to produce plans or oversee tasks — it's to continuously understand, judge, and steer the path toward the outcome."
- **Visualization:** camera pulls back; the emphasis moves off the plan and onto **the user**, positioned behind the project like a pilot at the controls. Outcome stays fixed; the path shifts underneath it.
- **Personalization:** the plan behind the "pilot" is theirs; the fixed outcome is theirs.
- **Mechanic:** **new** — no current beat does the role reframe. This is the missing *why* and the emotional core.
- **Notes (audit):** wins the owner, fine for the scrum PM, **risks the skeptical veteran** (can read as a lecture). Keep it **short and aspirational, not preachy** — this is the scene to trim if it drags. The skip route (§5) is the veteran's relief valve here.

### Scene 4 — The Three Judgments (34–48s)
- **Narration:** "To do that, ask three questions. Is the path **viable** — clear, aligned, feasible? Is it **grounded** — are the evidence, assumptions, and inferences visible? Is it **adaptable** — can you detect change and adjust before the outcome is at risk?"
- **Visualization:** three pillars illuminate around the project. Viable: goal-clarity + alignment lines + feasibility strengthen. Grounded: hidden assumptions/inference chains/evidence links illuminate — the project becomes transparent. Adaptable: timeline shifts, checkpoint markers light, the path adjusts toward the same outcome.
- **Personalization:** the pillars reflect **their** reads; the assumptions that illuminate are **theirs**; use the real upward-trace path from analysis.
- **Mechanic:** reuse the pillar chips + `trace` (uncertainty-propagates) + checkpoint markers. This is today's three-question intro, shown not lectured.
- **Notes (audit — the relapse point):** keep this to **three plain questions, shown**, not a pillar-terminology lecture. This is the scene that most risks re-introducing the mechanism-heaviness you're removing. Benefit-before-name (the existing terminology-bridge copy already does this).

### Scene 5 — Name the Discipline (48–53s) · NET-NEW
- **Narration:** "This is Outcome Orchestration."
- **Visualization:** everything simplifies to: Outcome → Living Hypothesis → Continuous Judgment → Successful Delivery. "Outcome Orchestration" appears as the operating model connecting them. Brief pause.
- **Mechanic:** **new** — a clean typographic beat.
- **Notes (audit):** name it **once**, don't dwell — framework-fatigue risk for agile natives and "they're selling me" for the skeptic. Canon-check the term (§8).

### Scene 6 — OSLO · your project · the first decision (53–60s+)
- **Narration:** "OSLO gives you the intelligence to surface what matters, strengthen your judgment, and continuously steer toward the outcome. Now — let's apply it to your project."
- **Visualization:** the abstract animation **dissolves into their actual project** (same objects become interactive — literal, because it was their data all along). The outcome becomes the focal point; OSLO highlights the first opportunity: **Outcome Definition — Decision Required.** The interface waits.
- **Personalization:** their outcome, their read; the first decision is **outcome-level** (confirm/own the outcome), not a granular assumption.
- **Mechanic:** reuse the `gr-conf` confirm panel (the existing activation moment) as the landing.
- **Notes (audit — the make-or-break for the owner):** the first decision **must** be owner-appropriate (define/own the outcome). If it lands on "confirm the Wi-Fi assumption," the whole owner win collapses at the finish line. Gate this beat on `analysis-complete`, not the timer (§2).

## 5. Two-mode controller (the audit's key recommendation)
Because no one can skip the *wait*, "skip" routes to a second view of the **same 60s**, not a spinner and not a teleport.

- **Mode A — Guided (default):** the narrated arc above.
- **Mode B — "Watch it work on my plan":** a persistent **"Skip the intro →"** control (visible from Scene 1) swaps to a lean live-processing view — their plan being analyzed, inference markers and early findings surfacing in real time (the analyzing-ring / live-reveal on their actual data). No narration.
- **Both modes converge** on the Scene-6 first decision when `analysis-complete` fires. Switching modes mid-way is allowed and preserves progress.
- **Who each serves:** Guided → the non-technical owner + the why-seeker; Watch-it-work → the skeptical veteran + the impatient. Neither can finish before processing does.

## 6. Fire-once & returning users
- First-ever run: default **Guided**.
- Returning user / second project: default **Mode B** (watch-it-work) — they've had the philosophy; they still must wait for the pass, so give them the live view, not a re-lecture. A small "replay intro" affordance is enough.
- Persist a `seenOnboardingArc` flag.

## 7. Activation hand-off
- The arc's terminal state **is** the existing activation moment (`gr-conf`). No new activation logic — the arc is a runway to it.
- Activation still = the user's real first call (`confirmCount≥1`). The arc must not auto-confirm or imply the decision is made. **OSLO advises; you decide** — unchanged.

## 8. Honesty guardrails (hard constraints) + canon
- **No overpromise:** narration stays advisory ("surface what matters, strengthen your judgment, help you steer") — never "OSLO achieves your outcome." No dark patterns.
- **No generic reel:** every scene is their data (§3); if data's missing, degrade to the model statement, never fabricate specifics.
- **Canon check before copy-lock:** run **"Outcome Orchestration"** and **"living hypothesis"** against `00_owner/CANONICAL_GLOSSARY.md` (Disambiguation Register, DL-053) to prevent term drift. If "living hypothesis" isn't canon, either adopt it via Framework 001 or swap to the ratified term.

## 9. Build mapping (for the eventual prototype)
| Scene | Reuse | Net-new |
|---|---|---|
| 1 Outcome | `_grBuild` root node | camera push-in, pre-graph state |
| 2 Living Hypothesis | `_grBuild` growth + inference markers (`col/exem`) | "breathing" motion, plan-builds-fast timing |
| 3 Identity Shift | plan tree as backdrop | **role reframe beat (new)** |
| 4 Three Judgments | pillar chips + `trace` + checkpoint markers | pillar-illumination choreography |
| 5 Name it | — | **typographic beat (new)** |
| 6 Your project + decision | `gr-conf` confirm panel | dissolve transition; bind to `analysis-complete` |
| Controller | analyzing ring / live reveal | **two-mode swap + processing binding (new)** |

## 10. Decisions — RESOLVED (owner, 2026-08-08)
1. **First decision at Scene 6 = own the outcome.** Land on the `gr-conf` outcome-definition/confirm (owner-level), the root the read grounds to — not a granular assumption confirm. This makes the arc pay off for the non-technical owner.
2. **Terminology:** "Outcome Orchestration" is already canon — use as-is. **"living hypothesis" → RATIFY as canon** via Framework 001 (no existing term to swap to). DL drafted for owner landing: `release-2/DL-PENDING-living-hypothesis-canonical-term.md`.
3. **Returning users (2nd+ project) default to Mode B (watch-it-work)** — the live analysis view of their plan, not a re-lecture; a "replay intro" link remains. First-ever run stays Guided.
4. **Early finish = mode-dependent.** Guided holds a **~25–30s minimum** so the identity-shift lands; **Watch-it-work never pads** — it hands to the decision the instant `analysis-complete` fires. (Updates §2: the floor is mode-scoped, and we never artificially delay the evidence-first user.)
5. **Backend deps = register the new part now.** The personalization tokens (§3) are existing analysis-engine outputs the arc *consumes*; the genuinely-new backend need is **progressive/streaming analysis events during the pass + an `analysis-complete` signal** (so watch-it-work shows findings forming live). Registered as capability **#21** in `OSLO_BACKEND_CAPABILITIES.md`.

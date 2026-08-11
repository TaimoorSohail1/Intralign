# DL-196 — All three integrity pillars resolve through the exposure-gated issue layer

**Status:** ⛔ **RATIFIED 2026-07-27 by Idris** (sole ratifier, Framework 001) — canon **for the R2 track** (R2 stays isolated from R1/main; ratification is a governance status, not a merge). Built + green (179→183 guards across DL-196/197). Reworks DL-195 Phase C (the standalone checkpoint-proposal panel) into the issue model. Consumes DL-193 (exposure/leverage queue), DL-194 (three-pillar integrity), DL-195 (Adaptability), DL-190 (limiter-standalone confirmation).
> _Scribe-drafted 2026-07-26 (owner-directed), ratified 2026-07-27._
**Origin:** owner — "manage outcome checkpoints as part of the issue class"; then the realization: "that would mean all outcome integrity pillars are resolved via the issue management layer."

---

## 1. The principle
**The issue layer is the single surface for resolving outcome integrity, across all three pillars.** One mechanism, one lifecycle (open → resolved), one detail view, one provenance model, and one **exposure-ranked queue** (DL-193) that prioritizes *across* pillars — a CAF gap, a missing checkpoint, and a load-bearing unconfirmed assumption compete for "what do I do next" on the same outcome-exposure basis. This retires the DL-195 Phase-C standalone `#ov-checkpoints` panel.

## 2. The three pillars → three issue types
- **Viability** → **CAF issues** (Clarity / Alignment / Feasibility). *Existing.*
- **Adaptability** → **checkpoint issues** (a NEW type): "the outcome goes unread until ~N weeks out." *This packet.*
- **Grounding** → **false-confidence issues**: a load-bearing assumption the outcome rests on that is still OSLO's inference ("your outcome leans on this, unverified"). This **formalizes DL-190's limiter-standalone** as a first-class issue type rather than a special case. *(May be staged after the checkpoint rework.)*

## 3. The load-bearing discipline (NON-NEGOTIABLE) — only high-exposure threats become active issues; the benign tail does not
This is what keeps the unification from breaking the doctrine, and it matters most for Grounding. **An unconfirmed inference is, by default, honest uncertainty — not a defect** (doctrine: "inference is what OSLO is for; marking an assumption unconfirmed is honesty, not a warning"). Issue-ifying every unconfirmed assumption would frame OSLO's own honesty as a wall of problems and resurrect the confirmation treadmill DL-190 killed.

So the same exposure-gate we already built governs all three pillars: the **load-bearing / high-exposure** threat is an active issue; the **low-exposure tail** stays available on its map (Inference map · the plan), **never issue-ified, never nagged**. *The issue layer resolves integrity; the exposure queue decides what surfaces; the maps hold the complete tail.*

## 4. Checkpoint issues — structure
- **One issue per checkpoint gap** (owner-chosen over an umbrella issue): each gap keeps its own severity, exposure rank, confirm/resolve lifecycle, and History entry. DevNorth → 3: "outcome unread until ~8 / ~4 / ~2 weeks out."
- **Shape:** `{ dim:'Adaptability', dims:['Adaptability'], ftype:'Coverage Gap', sec:'Schedule', sev, status }`. Severity scales with *urgency by runway* — the earliest gap is more critical (least runway remaining if missed).
- **Recommendation(s):** each issue carries a From-OSLO (inference, confirmable) recommendation — "Add checkpoint: read «indicator»; if it drifts, lever «lever»" — with the timing. Applying it is an `apply`-able action.
- **Resolving = registering the checkpoint.** Applying the rec resolves the issue AND adds the checkpoint to the plan → **`_adaptabilityBand` computes from the RESOLVED checkpoint issues** (open ones are proposals, not yet counted). So confirming a checkpoint issue raises Adaptability and recomputes integrity live — same behaviour as Phase C, now through the issue lifecycle.
- **Provenance preserved:** the checkpoint is OSLO inference until confirmed (From OSLO → Confirmed by you), level ≠ trust intact.

## 5. The dimension-space extension + the care point
Issue `dim` extends from CAF-only to the pillars an issue can threaten: **Clarity · Alignment · Feasibility** (→ Viability) **+ Adaptability** (+ later, Grounding's false-confidence type). 
**⛔ CARE POINT (get this exactly right):** **Adaptability-dim issues feed Adaptability ONLY** — they must **not** leak into the Viability/CAF band (`_cafOf`), the CAF rows, or the Attention heat map (those stay Clarity/Alignment/Feasibility). Keeping that filter is what preserves the three-pillar separation. Guard it.

## 6. Queue & drill-down integration
- Checkpoint (and false-confidence) issues rank in **"Your next move"** by outcome-exposure (DL-193) — a plan flying blind on its outcome is high-exposure, so they surface prominently, competing honestly with CAF issues. `_issueExposure` gets an Adaptability path.
- The integrity headline's **pillar chips become drill-downs into their issues**: Viability → CAF issues (+ the OC fold), Adaptability → checkpoint issues, Grounding → false-confidence issues (+ the Inference map for the tail).

## 7. Build plan (rework)
1. **Retire the Phase-C panel** — remove `#ov-checkpoints` + `renderCheckpoints()`; keep `_proposedCheckpoints()` content as the source for the checkpoint *issues*.
2. **Emit checkpoint issues** — inject 3 Adaptability issues into `ISSUES` (open = proposed), each with a From-OSLO "add checkpoint" recommendation; wire the rec's apply → resolve issue + push to `_ADDED_CHECKPOINTS`.
3. **Adaptability from resolved issues** — `_adaptabilityChecks` reads resolved checkpoint issues (via `_ADDED_CHECKPOINTS`, unchanged) so confirming raises the band.
4. **The filter (care point)** — exclude `dim:'Adaptability'` issues from `_cafOf` / CAF rows / heat; include them in the exposure queue + Adaptability.
5. **Exposure** — `_issueExposure` handles Adaptability issues (high — unprotected outcome; earliest gap highest).
6. **Guards** — rework the Phase-C guards to the issue model: checkpoint issues carry From-OSLO provenance; resolving raises Adaptability + gates further proposals; **NEW: Adaptability issues never touch the CAF band/rows/heat** (the care-point lock).
7. **(Staged) Grounding false-confidence issue type** — formalize DL-190 as an issue type; may follow the checkpoint rework.

## 8. Open for ratification
- Confirm the principle (§1) + the load-bearing discipline (§3) as canon.
- Confirm **one-issue-per-checkpoint** (§4) and severity-by-runway.
- Confirm the **care-point filter** (§5) as a guarded invariant.
- Timing of the **Grounding false-confidence issue type** (§2/§7.7) — with the checkpoint rework, or a fast-follow.

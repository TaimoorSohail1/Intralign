# Open Questions

Baseline: `oslo_r1_experience_mockup_v4.html`. Answer only overrides; unanswered recommendations are accepted and locked.

---

# Slice 1: Access & Onboarding — RESOLVED / SIGNED OFF (2026-07-09)
All recs accepted + GA-phase clarification. Locked D021–D034. See `decision-log.md`.

---

# Slice 2: Intake & Fast-Pass Orientation — RESOLVED (2026-07-09, accept all)
All recommendations accepted. Locked D035–D042; C-001 resolved (D038). Prototype build delegated to worker.

Builds on the Slice 1 funnel. Covers the depth of intake synthesis, the Fast Pass ("Initial Analysis"), the 60-second orientation hand-off, and the auto-running Deep Pass ("Extended Analysis"). Cumulative prototype = Slice 1 + Slice 2.

## Resolved from v4 / prior locks (no question)
- Flow: Intake → Fast Pass ≈30s (D031) → 60-second orientation → Deep Pass auto-runs & supersedes (D005/DL-046).
- User-facing labels: "Initial Analysis" / "Extended Analysis" (D012); "Issues" not Findings (D017).
- Analysis-state honesty: provisional ↔ current, error/last-good/retry (ORIENTATION_STATE_MODEL).
- Fast Pass trace/interstitials: Extract·Infer·Construct·Evaluate + rotating strategic copy.

## Feature 1: Evidence → synthesized plan artifacts
**F2.1Q1** — From a thin brief, does OSLO construct **all seven** plan artifacts (inferring/deriving the missing ones, marked "From OSLO" + lower reliability) or only populate sections with direct evidence?
*Recommended:* Construct all seven (Extract·Infer·Construct), with inferred content epistemically marked Derived and reliability-qualified; thin evidence → Clarification Requests. (Matches v4.)

## Feature 2: Fast Pass ("Initial Analysis")
**F2.2Q1** — Completion-time label: v4 shows "complete in 41s — under the 60-second target," but prototype pacing is ≈30s (D031). What ships?
*Recommended:* Show the **measured** Time-to-First-MRI (owner-TBD NFR), framed "under the 60-second target"; prototype displays ≈30s illustratively. No fabricated fixed number.
**F2.2Q2** — Fast Pass outputs surfaced at orientation: Orientation Confidence · Initial Attention (MRI) · Top Issues · Clarification Requests · Suggested Fixes · Analysis Status.
*Recommended:* Surface all six (workflow diagram).

## Feature 3: 60-second orientation hand-off
**F2.3Q1** — Landing surface after Fast Pass: the confidence-led **Overview** (DL-096, with the Attention section reachable) vs the **Attention Map** directly (C-001 "MRI co-primary").
*Recommended:* Land on the **Overview** (confidence-led), Attention reachable as a co-primary view. This also sets the C-001 default (owner may still flip).
**F2.3Q2** — The one-time strategic-chain orientation (D027) fires here on first project only; the arrival "Initial Analysis complete" notice shows only on a fresh analysis (not for returning users).
*Recommended:* Yes (v4 §6.5).

## Feature 4: Deep Pass ("Extended Analysis")
**F2.4Q1** — Deep Pass auto-runs immediately after Fast Pass, **non-blocking**, and supersedes the provisional orientation (provisional→current); no user action to start it.
*Recommended:* Yes (D005/DL-046); confidence hero carries the provisional↔current chip; "Extended Analysis complete — superseded the provisional orientation."
**F2.4Q2** — If Deep Pass fails: show "couldn't complete — showing your last-good understanding · Retry"; only reanalysis changes the assessment.
*Recommended:* Yes (ORIENTATION_STATE_MODEL).

## Feature 5: Clarification Requests (at intake)
**F2.5Q1** — Clarification Requests raised during analysis: surface as a light prompt at orientation **and** inside the relevant Issue; answering updates project info → reanalysis → issue closes.
*Recommended:* Yes (v4 §6.4; advisory framing — OSLO asks, you answer, you decide).

---
## Recommendation summary (accepted unless overridden)
F2.1Q1 construct all 7 (marked Derived) · F2.2Q1 measured time (~30s illustrative) · F2.2Q2 all six outputs · F2.3Q1 land on Overview (Attention co-primary) · F2.3Q2 first-run orientation + fresh-analysis notice · F2.4Q1 auto Deep Pass supersedes · F2.4Q2 last-good/retry on failure · F2.5Q1 clarification prompt + in-issue.

---

# Slice 3: Project Overview & Understanding Console — RESOLVED (2026-07-09, accept all)
Locked D050–D056; ND-2 resolved (D056). Cumulative build delegated to worker.

Deepens the confidence-led Overview from Slice 2 with the understanding-console layer v4 puts in the confidence pill popover + explainability. Cumulative = Slices 1–3.

## Resolved from v4 / prior locks (no question)
- Overview structure = Confidence → Start here → Progress → More (DL-096, D046). 5-band scale (DL-086/098). Neutral maturity ramp; severity color on issues only (D003).
- "Why" disclosure + provisional↔current ("Current / Still updating") chip already in Slice 2.

## Feature 1: Confidence pill + popover (compact console)
**F3.1Q1** — Top-bar Confidence pill (number + band + reliability qualifier, always visible) with a click popover showing the three CAF dimensions (first level) + Reliability basis + "Open full breakdown → Overview."
*Recommended:* Yes (v4). Metrics live in one home (top bar), not duplicated.

## Feature 2: Reliability basis breakdown
**F3.2Q1** — Reliability basis = **Coverage · Evidence availability · Assessability** (levels High/Moderate/Low), independent of CAF, shown in the pill popover; reachable from the Overview "Why."
*Recommended:* Yes (Reliability Model V1). Plain label "How assessable" for Assessability (D012). Popover is the home; Overview keeps reliability as the inline qualifier + Why (D046) — no separate card.

## Feature 3: False-confidence flag (CONF-06)
**F3.3Q1** — When a high confidence band sits on low reliability, surface a false-confidence flag that names the cause (reliability shortfall vs CAF weakness).
*Recommended:* Yes; advisory, non-alarming, neutral (not health-colored); appears in the Confidence card + popover when the condition holds.

## Feature 4: Confidence stages (CONF-05)
**F3.4Q1** — Understanding maturity stage (Orientation ▸ Expanded ▸ Validated).
*Recommended:* Surface subtly — in the Confidence info tooltip + a quiet stage marker; not standing chrome.

## Feature 5: Explainability "how this is calculated"
**F3.5Q1** — A subtle "how this is calculated" affordance by the confidence number (CAF-derived, reliability-qualified, cause-bound; below-band jitter not dramatized).
*Recommended:* Yes (info affordance, hover/click).

## Feature 6: Project summary depth
**F3.6Q1** — Project summary (in More) = plain-language narrative: what the project is · understanding level · main limiter · reliability basis · the "not health/readiness/probability" caveat.
*Recommended:* Yes (v4).

## Feature 7: Confidence movement (resolves ND-2)
**F3.7Q1** — When a fix is applied and reanalysis runs, the confidence signal moves **direction-only** (▲/▼ with the named cause), never a fabricated magnitude; can fall (better understanding, not worse project).
*Recommended:* Direction-only (ND-2). Resolves the open ND-2.

---
## Recommendation summary (accepted unless overridden)
F3.1Q1 pill+popover · F3.2Q1 reliability basis in popover (Overview inline+Why) · F3.3Q1 false-confidence flag · F3.4Q1 stages subtle · F3.5Q1 how-calculated · F3.6Q1 project summary depth · F3.7Q1 direction-only (ND-2).

---

# Slice 4: Attention Map (MRI) — RESOLVED (2026-07-09, accept all)
Locked D057–D062. Cumulative build delegated to worker.

Deepens the basic heatmap from Slice 2 into the full Attention Map surface. Cumulative = Slices 1–4.

## Resolved from v4 / prior locks (no question)
- Heatmap-primary, plan-artifacts × Clarity·Alignment·Feasibility (D007); Attention is a co-primary top-center view (D038). Severity color on cells only; confidence/CAF neutral (D003). "Plan artifacts" term (D049); "Issues" (D017).

## Feature 1: Heatmap (primary MRI visual)
**F4.1Q1** — Heatmap = rows (7 plan artifacts) × columns (Clarity · Alignment · Feasibility); cells shaded by attention severity (none → warning → moderate → critical, brighter = more attention); legend "Brighter = more attention — not a health score."
*Recommended:* Yes (D007; v4). Optional per-cell issue-count mini-label.

## Feature 2: Cell → Issues routing
**F4.2Q1** — Clicking a cell routes via openFindingsFor(artifact, dimension): exactly one open issue → opens that issue; otherwise opens the Issues list scoped to that section + dimension (both filters lit).
*Recommended:* Yes (D007; v4 §6.11). Full Issues list is Slice 6 — Slice 4 wires the routing to the light issue panel + a scoped-list seam.

## Feature 3: Field view (secondary)
**F4.3Q1** — A secondary "field" view toggle alongside the heatmap (heat primary / field secondary).
*Recommended:* Include as a light secondary toggle (heat is primary). If you'd rather defer the field view to keep R1 lean, say so — it's the one genuinely optional piece.

## Feature 4: Severity coloring + legend + hover
**F4.4Q1** — Cell severity ramp uses red/amber only (D003); confidence/CAF stay neutral. Hover scales the cell; the legend states it's attention, not health.
*Recommended:* Yes.

## Feature 5: Empty / edge states
**F4.5Q1** — A section×dimension with no open issues renders as a neutral, inert cell (not clickable); when nothing needs attention (all clear), show an all-clear empty state.
*Recommended:* Yes (four honest empty-state distinctions, D003/§Tier1).

## Feature 6: Co-primary placement + context preservation
**F4.6Q1** — Attention Map reachable as a co-primary top-center view + from the Overview's Attention pointer; closing returns to prior context (NAV-7).
*Recommended:* Yes (D038).

---
## Recommendation summary (accepted unless overridden)
F4.1Q1 heatmap primary · F4.2Q1 cell→scoped issues routing · F4.3Q1 field view secondary (defer? your call) · F4.4Q1 severity-only + legend · F4.5Q1 empty/all-clear states · F4.6Q1 co-primary + context preserved.

---

# Slice 5: Plan Artifacts / Artifact Workspace — RESOLVED (2026-07-09, accept all + F5.2Q1 clarification)
Locked D066–D071. F5.2Q1: Understanding artifacts default to prose but may include bullets/tables where items warrant. Cumulative build delegated.

Where the user reads and improves the 7 plan artifacts. Cumulative = Slices 1–5. Also fills the feature-tour artifact-edit step seam (D044).

## Resolved from v4 / prior locks (no question)
- 7 artifacts: Intent·Context·Scope·Requirements (Understanding) + Work breakdown·Schedule·Resources (Execution) (D004). "Plan artifacts" term (D049). Event-driven reanalysis only (D006). Epistemic notation From OSLO/Confirmed by you (D011). Severity color on annotations only (D003).

## Feature 1: Artifact explorer + open
**F5.1Q1** — Left-rail explorer lists the 7 artifacts (grouped Understanding / Execution) with a per-artifact open-issue count badge; clicking opens it in the center editor.
*Recommended:* Yes (v4).

## Feature 2: Type-aware editor
**F5.2Q1** — Understanding artifacts render as flowing prose; Execution artifacts (Work breakdown, Schedule, Resources) render as structured tables. Live edit (inline/contenteditable) with autosave.
*Recommended:* Yes — per-layer rule (prose vs tables), documented in v4. Simulated autosave (localStorage) in the prototype.

## Feature 3: Inline weakness annotations
**F5.3Q1** — Weak text is inline-colored (severity ramp) on the contiguous weak span; hover shows a summary; clicking opens the Issue panel.
*Recommended:* Yes (D003 severity color; Panel Model — annotations route to the Issue panel, not resolved inline).

## Feature 4: Epistemic notation (From OSLO / Confirmed by you)
**F5.4Q1** — Text is From OSLO (Derived) by default; editing or confirming a sentence makes it Confirmed by you (Attested) = a plan fact, with a visual distinction (accent marker). Saving changes no assessment; only reanalysis does.
*Recommended:* Yes (D011).

## Feature 5: Event-driven reanalysis
**F5.5Q1** — Editing runs the state machine automatically: Saved → analysis stale → Reanalyzing… → Up to date. No manual "Reanalyze" button.
*Recommended:* Yes (D006).

## Feature 6: Weakness stepper + artifact navigation
**F5.6Q1** — A "Jump to weakness ⌃ k of N ⌄" stepper to move between weak spots in an artifact, plus artifact prev/next navigation.
*Recommended:* Yes (cognitive audit C7).

---
## Recommendation summary (accepted unless overridden)
F5.1Q1 explorer + badges · F5.2Q1 type-aware prose/tables + autosave · F5.3Q1 inline annotations → Issue panel · F5.4Q1 From OSLO/Confirmed by you · F5.5Q1 event-driven reanalysis · F5.6Q1 weakness stepper + prev/next.

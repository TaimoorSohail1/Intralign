# Slice 2 — Intake & Fast-Pass Orientation · Workflows

Three actors: **User**, **System** (app shell/state), **AI Agent** (OSLO — simulated). Advisory-only throughout (D001): the AI Agent reads, constructs, evaluates, asks, and drafts — it never commits changes to the plan; the User decides.

---

## W1 — Intake → Fast Pass (Initial Analysis)

| # | Actor | Step |
|---|---|---|
| 1 | User | Provides intake (Describe / Attach / Template / Sample) and clicks "See where I stand →" (D023/D030). |
| 2 | System | Records start time (`_measuredStart`), shows the rails-first analyzing overlay. |
| 3 | AI Agent | **Extract** readable text (+ structured tables for XLSX/CSV, D034) from inputs. |
| 4 | AI Agent | **Infer + Construct** all seven plan artifacts (D035); inferred content → From OSLO (Derived) + reliability-qualified. |
| 5 | AI Agent | **Evaluate** Clarity·Alignment·Feasibility per section; surface Issues; raise Clarification Requests where evidence is thin. |
| 6 | System | Measures elapsed (D036), closes overlay, lands on Overview. |

## W2 — Orientation → land on Overview

| # | Actor | Step |
|---|---|---|
| 1 | System | If first project (`orientSeen`=false), show the one-time strategic-chain orientation (D027/D039); else skip. |
| 2 | User | Reads the chain, clicks "Get started →" (dismiss). |
| 3 | System | Marks `orientSeen`; lands on the confidence-led Overview (provisional) (D038/D019). |
| 4 | System | On a **fresh** analysis only, shows "Initial Analysis complete in Ns — under the 60-second target" (D039/D036). |
| 5 | AI Agent | Surfaces all six Fast Pass outputs (D037): confidence, attention, top issues, clarifications, suggested fixes, analysis status. |

## W3 — Extended Analysis (Deep Pass) — auto, non-blocking (D040/D041)

| # | Actor | Step |
|---|---|---|
| 1 | System | Immediately after orientation, auto-starts Extended Analysis (no user action). Shows "running…" banner + chip = Provisional. |
| 2 | AI Agent | Deepens the read in the background (simulated). |
| 3a | System (success) | Supersedes provisional→current: chip flips to Current, banner "Extended Analysis complete — superseded the provisional orientation," refined 58→62 / Feasibility Very Low→Low. |
| 3b | System (failure) | Keeps last-good (provisional) read; chip → Last-good; error banner "couldn't complete — showing your last-good understanding · Retry." |
| 4 | User (on failure) | Clicks Retry. |
| 5 | System | Re-runs; recovers provisional→current. |

## W4 — Clarification loop (D042)

| # | Actor | Step |
|---|---|---|
| 1 | AI Agent | Where a plan artifact rests on thin evidence, raises a Clarification Request — shown as a light Overview prompt AND inside the tied Issue. |
| 2 | User | Answers the question (at orientation via "Answer →" opening the issue, or directly in the issue's clarification block). |
| 3 | System | Updates project information: marks the tied section **Confirmed by you** (Attested, D011) and bumps its reliability. |
| 4 | AI Agent | Re-runs analysis (simulated) on the updated information (D006 — only reanalysis changes the assessment). |
| 5 | System | Closes the issue (Open→Addressed→Resolved, D018), refreshes Overview counts, Attention heatmap, and clarification list. |
| 6 | AI Agent | Refines confidence/CAF accordingly (illustrative, direction-only). |

## W5 — Attention Map navigation (D038/D007)

| # | Actor | Step |
|---|---|---|
| 1 | User | Clicks "Attention" in the top-center view switch (or the "Attention map →" link / a CAF row). |
| 2 | System | Shows the heatmap-primary Attention view (7 sections × Clarity·Alignment·Feasibility); severity color only on issue cells (D003). |
| 3 | User | Clicks a cell (or a section row). |
| 4 | System | Routes to the tied issue (light panel); one match → open it. Scoped filtered lists for multi-match are the Slice-6 seam. |

---

### Invariants
- The AI Agent never resolves an issue or edits the plan directly — the User answers/decides, reanalysis moves state (D006, D001).
- Last-good understanding is always preserved on failure (D041).
- Confidence never shown bare; band + reliability + cause always present (D002/D019).

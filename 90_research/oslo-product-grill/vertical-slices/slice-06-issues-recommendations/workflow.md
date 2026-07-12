# Slice 6 — Issues & Recommendations · Workflow

Cumulative Slices 1–6. The Slice-6 flows below assume the user is already in an analyzed project (Slices 1–5 complete).

## Entry points into the all-issues surface (D086)
- Top-center **Issues** view button (co-primary), or
- An **Attention-map cell / row header** (D058): one active issue → the issue's panel; several → the Issues pane scoped to Artifact × Dimension, both filters lit, or
- The Overview "Start here" top-issue, an inline **annotation** in the artifact editor, or an OSLO **chat** link — each opens the same full Issue Panel.

## Flow A — Triage the issue list
1. Open **Issues**. Default view: **By dimension**, **Status = Open**, all issues shown; header count "6 open".
2. Toggle **By severity** → triage strip (Critical/Moderate/Warning) + severity groups.
3. Apply filters (**Artifact / Dimension / Severity**). If filters hide issues, the footer shows "N hidden by filters · clear".
4. Click **clear** → filters reset; full list returns.

## Flow B — Resolve an issue via "Apply this fix" (D089 → D088)
1. Open an issue → full panel: Header + lifecycle (Open lit) → Why → Evidence (collapsible) → What this weakens → **Recommendations**.
2. Click **Apply this fix** on OSLO Recommended.
3. OSLO **drafts** the change into the plan (where it can), marks the tied artifact **Confirmed by you**, and shows **"Re-analyzing…"**. Lifecycle → **Addressed** ("awaiting reanalysis").
4. Reanalysis completes → lifecycle → **Resolved**. Confidence moves **direction-only** (▲/▼ with named cause, no number). The issue drops off the Attention map / badges / open counts; it appears under **Status = Resolved**.
   *Acceptance ≠ success:* if reanalysis found it still held, it would stay Addressed. (Simulated as always-resolving here.)

## Flow C — Choose a resolution path (D089)
1. In the panel, select one of **Possible resolution paths**.
2. It becomes the **Selected Path = Confirmed by you**; lifecycle → **Addressed**.
3. Resolution still requires reanalysis (Apply this fix, or edit the plan in the artifact → the Slice-5 debounced reanalysis). Never resolved by hand.

## Flow D — Answer a clarification (D090)
1. Open an issue that carries a **Clarification request**.
2. Type an answer → **Submit & re-analyze**.
3. OSLO updates project info (tied artifact attested), re-runs analysis (Addressed → reanalysis), and the issue **closes** (Resolved). Confidence refines direction-only.

## Flow E — Empty states (D091)
- **None-found:** resolve all issues → "No issues — your plan looks clear".
- **None-under-lens:** over-filter → "Nothing under this lens · clear filters".
- **Not-yet-analyzed / Unavailable:** reachable via the prototype-preview control → honest "analysis hasn't finished" / "temporarily unavailable — not an all-clear".

## Invariants
- OSLO advises; the user decides and acts (D001). Issues close **only** via reanalysis (D006/D088) — no manual resolve. Recommendations live **only** inside the issue (D009). Severity color only (D003); confidence direction-only (D056).

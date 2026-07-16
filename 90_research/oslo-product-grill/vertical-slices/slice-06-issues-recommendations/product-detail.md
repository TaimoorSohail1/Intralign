# Slice 6 — Issues & Recommendations · Product Detail

Cumulative Slices 1–6. This document specifies the behavior added in Slice 6. Inherited behavior from Slices 1–5 is unchanged.

## Scope
Graduate the light issue panel (Slice 2/4) and the Attention-map scoped seam (Slice 4) into: (1) an **all-issues surface**, (2) a **full Issue Panel**, (3) the **Open → Addressed → Resolved** lifecycle, (4) **recommendations + Apply this fix** (Panel Model), (5) the **clarification loop** in the panel, and (6) **four honest empty states**. Client-side only (D016): single HTML, plain JS, `localStorage`, fake data, simulated AI.

## Capabilities

### C6.1 — All-issues surface (D086)
- Reachable as a **fourth co-primary view** ("Issues") in the top-center switch, with a live open-count badge (`vsIssuesBadge`).
- Center pane `#pane-issues`; the OSLO chat rail persists; issues open as a contextual panel over the list (Panel Model, D009).
- **Group toggle:** "By dimension" (default) / "By severity" (adds a triage strip: Critical / Moderate / Warning counts).
- **Filters:** Artifact · Dimension · Severity · Status.
  - The artifact-scoping filter is labeled **"Artifact"** (D049). Chips built live from artifacts holding status-matching issues, with counts; zero-count chips dimmed.
  - Dimension: All · Clarity · Alignment · Feasibility. Severity: All · Critical · Moderate · Warning. Status: Open (=`active`, default) · Resolved · All.
- **Honest hidden count:** "N issues hidden by filters · clear" appears only when filters actually hide issues; the header count reads "M open / resolved / total (filtered)".
- **Per-issue card:** title + severity chip (color only, D003) + location `Artifact · Dimension` + lifecycle status pill (Open / Addressed / Resolved) + a `❓ clarification` flag when pending. Keyboard-operable (role=button, tabindex, Enter/Space).

### C6.2 — Full Issue Panel (D087)
Rendered by `openIssue(id)` into `#issuepanel`. Sections in order:
1. **Header:** title · severity chip · `Dimension · Artifact` (Artifact = link → `openIssueArtifact` → workspace) · issue id · **lifecycle track** (Open → Addressed → Resolved, current lit).
2. **Why this matters** — `why`.
3. **Evidence** — collapsible (`.ip-evsec`, collapsed by default); each source shows its origin + quote.
4. **What this weakens** — `caf`, tagged with the issue's dimension.
5. **Recommendations** (C6.4) — only when not resolved.
6. **History** — pointer sentence + "Open full timeline →" (`openHistorySeam`, Slice-7 stub).
7. **Reanalysis note** — "Only reanalysis changes this assessment…".
Lifecycle banners: **Addressed** ("awaiting reanalysis") and **Resolved** ("Resolved by reanalysis") render when applicable.

### C6.3 — Lifecycle Open → Addressed → Resolved (D088)
- State held in `_istatus[id]` ∈ {`open`,`addressed`,`resolved`}; `_LIFE = ['open','addressed','resolved']`.
- **No Acknowledge stage; no manual Resolve control.**
- Acting (select path / apply fix / answer clarification) → **Addressed**. **Resolved only via reanalysis** (simulated `setTimeout`).
- Status reflected consistently on: issue cards, Attention cells, artifact explorer badges, Overview summary counts. "Active" (open **or** addressed, i.e. not resolved) governs what shows on the map/badges/list — heatmap counts and routing stay in agreement.

### C6.4 — Recommendations + Apply this fix (D089, Panel Model)
- **OSLO Recommended** (`rec`) tagged **From OSLO (Derived)**.
- **Apply this fix** (`applyFix`): sets Selected Path = `rec`, advances to Addressed, applies the drafted change (marks tied artifact attested + nudges its reliability), shows a "Re-analyzing…" state, then after reanalysis sets **Resolved**. Confidence moves **direction-only** (D056) — e.g. Feasibility Very Low → Low when the critical Resources gap clears; no fabricated magnitude.
- **Possible resolution paths** (`paths[]`): selectable (`selectPath`) → **Selected Path = Confirmed by you** (Attested), advances Open → Addressed. Resolution still requires reanalysis.
- **Write my own fix in {Artifact} →** opens the artifact editor.
- **Recommendations appear only inside the Issue** (D009) — no standalone/orphan surface.

### C6.5 — Clarification loop (D090)
- `clar` block (question + `hint`) with an answer input; `answerClarification` updates project info (tied artifact attested, reliability nudged), advances Addressed → reanalysis → **Resolved / closes**. Consistent with Slice-2 handling.

### C6.6 — Empty states (D091)
- `_issEmpty(kind)` renders: **none** (none-found), **none-lens** (filters hide all, with clear link), **wait** (not-yet-analyzed), **unavail** (unavailable — "not an all-clear"). Resolved-status-with-none shows a dedicated "No resolved issues yet".
- `_issuesState` ∈ {`ready`,`analyzing`,`unavailable`} drives wait/unavail; a subtle prototype-preview control makes them reachable.

### C6.7 — Attention-map routing graduated (D058)
- `openFindingsFor(art,dim)`: exactly one active issue → `openIssue`; else `scopeIssuesTo(art,dim)` → Issues center pane scoped (both filters lit). `openFindingsForArtifact(art)` scopes by artifact only. One consistent Issues destination (the separate scoped scrim is retired from the routing path).
- **Extended-state issue set (Enhancement #2 Phase 2):** the wired set is **9 issues at Extended** (6 at Fast Pass; ISS-07/08/09 add once Extended Analysis auto-runs), occupying 8 of 21 Attention cells. Multi-issue cells that route to the scoped list include **Resources × Feasibility** (ISS-01, ISS-03), **Schedule × Feasibility** (ISS-04, ISS-07) and **Scope × Alignment** (ISS-08, ISS-09). ISS-07 (Feasibility+Alignment) and ISS-08 (Clarity+Alignment, a Resources↔Scope coherence gap) each occupy two cells via `_dimsOf`, so a resolve in one cell still drops the shared issue everywhere. The **Alignment** dimension now spans element↔element and element↔outcome coherence — ISS-05 (accountability), ISS-07 (sequencing), ISS-08 (resource↔scope), ISS-09 (scope↔outcome) — not just stakeholder-agreement (canonical Alignment, CAF_ASSESSMENT_MODEL_V1 §3).

## Constraints
- Advisory-only (D001); severity color only (D003); dark default + WCAG 2.1 AA (list, filters, group toggle, and panel all keyboard-operable, focus-visible). No backend/API/DB/auth/real-AI (D016).
- Not built (seams): threaded comments/@mentions (Slice 9); full History timeline (Slice 7).

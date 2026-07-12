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

---

# Slice 6: Issues & Recommendations (Panel Model) — RESOLVED (2026-07-09, accept all + F6.1Q1 label edit)
Locked D086–D091. F6.1Q1: artifact-scoping filter labeled "Artifact" (not "Section"). Cumulative build delegated.

Consolidates the light issue panel (Slices 2–5) into the full Issues surface + full Issue Panel + recommendations. Cumulative = Slices 1–6.

## Resolved from v4 / prior locks (no question)
- Panel Model (D009): recommendations exist only inside the Issue context; no orphan/roll-up surface. "Issues" label (D017). Lifecycle Open→Addressed→Resolved (D018/DL-094). Never resolved by hand — only reanalysis (D006/D008). Severity color on issues only (D003).

## Feature 1: All-Issues surface
**F6.1Q1** — All-issues list (center pane) with filters (Section · Dimension · Severity) + a "By dimension / By severity" group toggle; honest "N hidden by filters · clear"; per-issue card = title + severity + location + status.
*Recommended:* Yes (v4 §6.11; Finding Presentation).

## Feature 2: Full Issue Panel
**F6.2Q1** — Contextual Issue Panel: Header (title · severity · dimension·section · lifecycle status) → **Why this matters** → **Evidence** (collapsible) → **What this weakens** (Clarity/Alignment/Feasibility impact) → **Recommendations** → **History** (pointer; full timeline = Slice 7) → reanalysis note.
*Recommended:* Yes (Finding Panel Option A, ratified).

## Feature 3: Lifecycle Open → Addressed → Resolved
**F6.3Q1** — Lifecycle Open → Addressed → Resolved (Acknowledge removed, DL-094). "Addressed by acting · awaiting reanalysis"; Resolved only via reanalysis (never by hand).
*Recommended:* Yes (D018).

## Feature 4: Recommendations + Apply this fix (Panel Model)
**F6.4Q1** — OSLO Recommended + Possible Resolution Paths, selectable → **Selected Path** (Confirmed by you); single-action **"Apply this fix"** where OSLO can draft → applies to the plan → reanalysis. Acceptance ≠ success; success is downstream (confidence moves direction-only, D056). No recommendations outside the Issue (D009).
*Recommended:* Yes.

## Feature 5: Clarification requests
**F6.5Q1** — Clarification block in the panel (question + answer input); answering → Update project info → reanalysis → the issue closes. Advisory (OSLO asks; you answer; you decide).
*Recommended:* Yes (D042).

## Feature 6: Empty states + honesty
**F6.6Q1** — Four honest empty states (none-found / none-under-lens / not-yet-analyzed / unavailable) + the honest "hidden by filters" count.
*Recommended:* Yes.

*(Threaded comments / @mentions on issues → deferred to Slice 9. Full History/timeline → Slice 7.)*

---
## Recommendation summary (accepted unless overridden)
F6.1Q1 all-issues list + filters + group toggle · F6.2Q1 full Issue Panel · F6.3Q1 Open→Addressed→Resolved · F6.4Q1 recommendations + Apply this fix (Panel Model) · F6.5Q1 clarification loop · F6.6Q1 empty states + honesty.

---

# Slice 7: History & Confidence Trend — RESOLVED (2026-07-09, accept all)
Locked D096–D100. Cumulative build delegated.

Fills the History seam (sidebar "History" nav) with the real append-only timeline + the understanding-over-runs trend. Cumulative = Slices 1–7.

## Resolved from v4 / prior locks (no question)
- History is a center pane (`#pane-history`), reachable from the sidebar. Append-only; prior states never overwritten (HISTORY_AND_TIMELINE §J). Confidence is direction-only (D056); a fall = better understanding, not a worse project. 5-band scale (DL-086/098).

## Feature 1: Append-only History/timeline
**F7.1Q1** — A chronological, append-only event list: analysis runs (Initial / Extended Analysis), artifact versions (vN), issue lifecycle changes (Open → Addressed → Resolved), selected resolution paths, clarifications answered. Current vs prior labeling; nothing overwritten; viewing is read-only (never changes the assessment).
*Recommended:* Yes (v4).

## Feature 2: Understanding-over-runs trend
**F7.2Q1** — An "Understanding over runs" trend sparkline: each point is cause-bound and band-qualified; the line can rise OR fall (a fall after deeper analysis usually means it found something real). Shown in History and mirrored by the Overview confidence trend row (already present).
*Recommended:* Yes (v4; direction-only, D056). Real magnitudes owner-TBD.

## Feature 3: Last-good + read-only honesty
**F7.3Q1** — Last-good understanding is preserved (e.g., on a failed analysis); History is read-only — you can view prior states but not edit them, and viewing changes nothing.
*Recommended:* Yes (ORIENTATION_STATE_MODEL).

## Feature 4: Version lineage
**F7.4Q1** — Artifact versions (vN) are append-only; History links to prior versions as view-only snapshots.
*Recommended:* Yes.

## Feature 5: Empty / first-run state
**F7.5Q1** — Before multiple runs, History shows a minimal state (the initial analysis) with an honest "more appears as your plan evolves."
*Recommended:* Yes.

*(Threaded comments as timeline events → deferred to Slice 9.)*

---
## Recommendation summary (accepted unless overridden)
F7.1Q1 append-only timeline · F7.2Q1 understanding-over-runs trend (direction-only) · F7.3Q1 last-good + read-only · F7.4Q1 version lineage · F7.5Q1 first-run state.

---

# Slice 8: Multi-Project Workspace & Awareness — RESOLVED (2026-07-09, accept all)
Locked D102–D106. Cumulative build delegated.

Fills the shell seams: project switcher, Settings, + adds Workspace Home/Dashboard, Notifications, Appearance. Cumulative = Slices 1–8. Canonical owner of the global nav/switcher/settings the shell already uses.

## Resolved from v4 / prior locks (no question)
- Three-context shell + command palette already built (D093/D094). Visibility-first tiering (D014, DL-048): honest limits, non-destructive archive; billing/enforcement deferred. Two-theme (D015). Alpha = invite-only (D021); tier numbers illustrative.

## Feature 1: Workspace Home / Dashboard
**F8.1Q1** — A global Workspace Home (via the OSLO/Intralign logo + Workspace context): **Pinned + Recent** project cards, each with name · ownership/shared · analysis status (incl. **stale**) · reliability-qualified understanding indicator · recency · open-issues count; an **Archived projects** area (non-destructive, restore anytime); a "no computed scores across projects" honesty note; and the at-cap **Create → upgrade-or-archive** prompt (DL-048).
*Recommended:* Yes. Alpha shows the structure with illustrative projects; "1 active project" tier note.

## Feature 2: Project switcher
**F8.2Q1** — Wire the top-bar "DevNorth 2026 ▾" chip to a real switcher: project list + Workspace Home + New project (at-cap → the honest prompt).
*Recommended:* Yes.

## Feature 3: Notifications / awareness panel
**F8.3Q1** — An awareness panel with R1 categories (mention · reply · shared-with-me · analysis complete/failed · stale); read/unread (**presentation-only**); **routes to source**; **never triggers analysis**; an unread badge in the top bar.
*Recommended:* Yes (Notification & Awareness spec).

## Feature 4: Settings
**F8.4Q1** — Wire the Settings seam to a real Settings surface with the areas: Account · Profile · Workspace · Project defaults · Collaboration · Notifications · Subscription · Billing · Integrations · Membership. **Visibility-first** for Subscription/Billing/Integrations/Membership (facts + upgrade paths; no enforcement).
*Recommended:* Yes.

## Feature 5: Appearance (theme + a11y)
**F8.5Q1** — Settings → Appearance: dark/light **theme toggle** (dark default), plus accessibility controls (reduced-motion honored, focus rings).
*Recommended:* Yes (D015 two-theme).

---
## Recommendation summary (accepted unless overridden)
F8.1Q1 Workspace Home/Dashboard · F8.2Q1 project switcher · F8.3Q1 notifications/awareness · F8.4Q1 Settings (visibility-first) · F8.5Q1 Appearance dark/light + a11y.

---

# Slice 9: Collaboration, Sharing & Export  (Slices 1–8 signed off; grill)

Fills the Share/Export top-bar seams + Settings → Collaboration, and un-gates the collaboration notification categories. Cumulative = Slices 1–9. Alpha-scope; presentation-first (no permission/billing enforcement).

## Resolved from v4 / prior locks (no question)
- Advisory-only (D001); Panel Model (comments live in the Issue context, D009); append-only History (D096); visibility-first (D014); notifications presentation-only + never trigger an analysis (D104).

## Feature 1: Sharing dialog
**F9.1Q1** — Invite by email + **participant types (Owner · Collaborator · Viewer)** with what each can do; plus a **view-only snapshot link** (labeled "previous analysis" if the read is stale). **Presentation-only** — no real permission enforcement in R1 (link-access enforcement is spec-deferred).
*Recommended:* Yes.

## Feature 2: Threaded comments + @mentions on issues
**F9.2Q1** — Threaded comments attached to an **Issue** (Panel Model — no orphan comment surface), **append-only**, with **@mention** autocomplete (registered teammates, or invite someone new). Persistent honesty: **"Comments never change the assessment."** Comments append to History (D096).
*Recommended:* Yes.

## Feature 3: Export / share-out
**F9.3Q1** — Export a **snapshot** of the current understanding with an **analysis-currency marker** and the **required disclaimer** (this is understanding maturity — not project health, readiness, or a probability of success); PDF / copy / link. **Free = PDF-only.** "Export generates no new assessment and never triggers an analysis."
*Recommended:* Yes.

## Feature 4: Un-gate collaboration notifications
**F9.4Q1** — Now that collaboration exists, un-gate the **mention · reply · shared-with-me** notification categories (gated in Slice 8 / D107); they route to source and remain presentation-only.
*Recommended:* Yes.

## Feature 5: CRR — CAF Review Requests  ⚠️ CORRECTION

**Prior position (WRONG):** "CRR is a genuine spec gap; keep it out of scope."
**Evidence says otherwise.** CRR is **fully specified canon** — five Alpha-scope, High-priority capability rows with an M4 exit criterion (C14), and the identity gap is **already ratified**:

| Ref | Canonical spec |
|---|---|
| **CRR-01** | "Share For Review" a CAF finding (issue) to a stakeholder. **Free-tier with bounded cap.** Recipient = **Reviewer Principal (DL-049)**. |
| **CRR-02** | **Review Package** = finding + context + recommendation + artifact reference. |
| **CRR-03** | **Stakeholder responses: Comment · Approve · Reject · Suggest Alternative.** Responses preserved. |
| **CRR-04** | **Response → evidence → triggers Extended Analysis**; confidence/MRI update. *"Review Requests create evidence."* |
| **CRR-05** | **Review-status visibility** across workspace + MRI → drives **MRI-07 Understanding Dependencies** ("2 issues awaiting sponsor review"). |
| OVL-03 / REC-05 | "Share For Review" is an issue-overlay action; **Validation Recommendations are prime CRR candidates**. |
| **DL-049** (Ratified) | Single `Principal`, `type: reviewer \| user`, **in-place promotion**. **Gap #337 (external-reviewer identity) RESOLVED.** |
| DL-055 (Ratified) | Share For Review reclassified as a **collaboration affordance** (not a recommendation state). |

**Non-negotiable guardrails (Visual Design Spec):** a stakeholder response is **evidence, not truth** · **no autonomous acceptance** · **OSLO never self-accepts**.

**Why this matters:** per the Virality/K-Factor audit, **OSLO's core value action *is* its viral action** — you invite a stakeholder *because you need their input*, and their answer becomes evidence that improves your understanding. CRR is the collaboration↔understanding bridge (the only collaboration capability requiring AI). Cutting it would gut Slice 9.

### The questions that are actually open

**F9.5Q1 — Build sender-side CRR (CRR-01…05) in Slice 9?**
*Recommended:* **Yes.** It is ratified canon and Alpha-scope. Share for review on an issue → review package → response → evidence → Extended Analysis → confidence/MRI move → "Awaiting review" status + Understanding Dependencies on Overview/Attention.

**F9.5Q2 — Response semantics (the doctrinal edge).**
*Recommended:* Reviewer response enters as **evidence** and triggers an analysis update — but it is labeled a **third-party attestation** (distinct from *Confirmed by you* and from *From OSLO*), it **never auto-resolves the issue**, and **OSLO never self-accepts it as truth**. Confidence may move; the assessment is never overwritten by a stakeholder's assertion. (An "Approve" is evidence *that a stakeholder approves* — not proof the plan is sound.)

**F9.5Q3 — The recipient (external reviewer) experience.** ⬅ *the genuinely open one*
Explicitly **owner-open** in the audit ("the commodity recipient UI / convert-moment + R1-vs-fast-follow scope remain owner-open"). The audit's **P0**: a **low-friction, no-account-required review view** with a **convert-moment at realized value** ("create your own project" *after* they've reviewed) — the binding constraint on k.
*Options:* **(a)** sender-side only; reviewer response simulated for demo. **(b)** build the low-friction reviewer view + convert-moment **as an explicit owner PROPOSAL** (not asserted canon). **(c)** defer to fast-follow.
*Recommended:* **(b)** — prototype it and label it a proposal. Highest-leverage open item; a prototype is the cheapest way to make the decision concrete. Anti-Assumption is honored because it is **proposed, not inferred as settled**.

**F9.5Q4 — Share-link hygiene (gap #339 — still unspecified).**
Expiry / revocation / scoping are undefined. *Recommended:* prototype a **revocable, scoped** link (scope = one issue package, or one MRI snapshot) and carry **expiry as an owner-TBD** — shown, not invented.

**F9.5Q5 — Free-tier CRR cap (CRR-01 "bounded cap").**
The **mechanism** is canon; the **number is not ratified.** *Recommended:* build the cap + counter with the value as an explicit **owner-TBD placeholder**. **Do not invent a number.** (Doctrine: virality must seed on Free — gate collaboration *depth*, never the *seed* of the loop.)

---
## Recommendation summary (accepted unless overridden)
F9.1Q1 sharing dialog (Owner/Collaborator/Viewer + view-only link) · F9.2Q1 threaded comments + @mentions on issues (append-only; never change the assessment) · F9.3Q1 export snapshot (currency marker + disclaimer; Free=PDF-only) · F9.4Q1 un-gate collab notifications · **F9.5Q1 build CRR-01…05** · F9.5Q2 response = evidence, never auto-resolves, OSLO never self-accepts · F9.5Q3 reviewer view + convert-moment **as a proposal** · F9.5Q4 revocable scoped link, expiry = owner-TBD · F9.5Q5 Free cap mechanism, number = owner-TBD.

---

# Slice 10: Tiering & Limits  (FINAL SLICE — grill)

**Canon does most of the deciding here.** DL-102 is now ratified canon. Most numbers are already settled — I use them and cite them; I do not re-propose them (that is how the Basic-10-projects error happened).

## Already RATIFIED — adopted, not re-opened
| Value | Source |
|---|---|
| **Free = 1 active project · Basic = 3** | UP-3 |
| **Daily fixes: Free 5 · Basic 20** | MON-02 / UP-1 |
| **Daily chat: Free 20** | MON-03 / UP-2 |
| **Deep runs/day: Free 2** | UP-5 |
| **Export: Free = PDF only** | MON-01 / SHARE-04 |
| **Free scope:** full Workspace · Confidence · CAF · MRI · Issues · Recommendations · Sharing · Comments · **CRR** | MON-01 + CHG-061 |
| **Seats: Free 3 · Basic 10; Viewers unlimited; reviewers free** | DL-102 E / B (seats = recommendation into the Tier-Definitions gap) |
| **Never meter the epistemic record** (artifacts uncapped, History never expires) · **never sell safety** · **no eviction on downgrade** · **two limits never conflated** | DL-102 D/E |

## Feature 1: Plans / upgrade surface
**F10.1Q1** — A real Free → Basic upgrade path (simulated). Pro is **named only as a forward capability** (continuous monitoring, UP-7) — not purchasable in R1. **Basic price renders as an explicit owner-TBD — no invented number.**
*Recommended:* Yes.

## Feature 2: Caps + honest counters
**F10.2Q1** — Visible counters for projects · daily fixes · daily chat · deep runs/day, with real values and real reset times. Unset values (Extended-Analysis budget) render **unset**, never as fake numbers.
*Recommended:* Yes.

## Feature 3: Upgrade prompts (MON-04 — the taxonomy is ratified)
**F10.3Q1** — Implement **UP-1…UP-8** with the two trigger classes (**value-moment** — fires at a positive peak, rare, strict cooldown · **friction-moment** — honest limit disclosure + the specific relief) and the **standing rules**: *no persistent upgrade wallpaper*; every prompt is **contextual, value-based, and names the specific limit hit + the specific tier that relieves it** (never a generic "upgrade").
**Global guards:** never interrupt an active Fast/Deep pass · never fire before first value (first MRI) · per-trigger cooldown + a global per-day cap.
*Recommended:* Yes, exactly as ratified.

## Feature 4: The limit-reached interaction rule (Seam Audit 001 — ratified in DL-102 E-1)
**F10.4Q1** — **EVERY** limit-bearing affordance **stays enabled**. The *attempt* is gated and surfaces the matching prompt **with resolutions** — e.g. 2nd project → *"upgrade **or** archive the current project"* (archiving is reversible and frees the slot, DL-058). **Never disabled, never hidden** (disabling suppresses the highest-intent moment); **never a raw error.** Applies to seats too.
*Recommended:* Yes. This also **corrects Slice 9**, where the seat cap blocked rather than prompted.

## Feature 5: Envelope exceeded → partial orientation (UP-4)
**F10.5Q1** — When a project exceeds the Free size envelope, OSLO delivers a **partial** analysis with an **honest disclosure** — fired **on one surface** with the upgrade prompt, never two competing notices. This is an epistemic honesty requirement first, a monetization surface second.
*Recommended:* Yes.

## Feature 6: The Tier-Definitions census  ⬅ the real deliverable
**F10.6Q1** — Slice 10 is the surface that **consumes every tier number**. Building it produces a **complete census of every consumption point** — which becomes the evidence-based table of contents for the missing `RELEASE_1_TIER_DEFINITIONS_V1` (cited as authoritative by **18 documents**; does not exist; escalated as a **blocking prerequisite for shipping Basic in Alpha** — DL-102 Concern 7).
*Recommended:* Yes. Output a `tier-definitions-census.md` listing every number the product needs, marking each **RATIFIED (with citation)** or **UNSET (owner decision required)**.

## Deliberately NOT invented (render unset)
**Basic price** · **Extended-Analysis budget numbers** (shape ratified: Free small / Basic generous) · **Free size envelope** (UP-4's "~100k words" is illustrative in canon, not ratified) · **monthly budget gate** (UP-6).

---
## Recommendation summary (accepted unless overridden)
F10.1Q1 Plans/upgrade (price unset) · F10.2Q1 honest counters · F10.3Q1 UP-1…UP-8 + standing rules + global guards · F10.4Q1 stays-enabled limit rule everywhere (corrects Slice 9 seats) · F10.5Q1 partial-orientation honest disclosure · F10.6Q1 Tier-Definitions census.

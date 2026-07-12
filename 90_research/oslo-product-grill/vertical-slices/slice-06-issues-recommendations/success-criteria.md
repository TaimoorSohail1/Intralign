# Slice 6 — Issues & Recommendations · Success Criteria

Cumulative Slices 1–6. A build passes Slice 6 when all below hold and Slices 1–5 do not regress.

## D086 — All-issues surface
- [ ] Issues is reachable as a co-primary view (top-center **Issues** button with a live open-count badge).
- [ ] Filters present: **Artifact · Dimension · Severity** (+ Status). The artifact-scoping filter is labeled **"Artifact"**, never "Section".
- [ ] **"By dimension / By severity"** group toggle works; By severity shows a triage strip.
- [ ] Honest **"N hidden by filters · clear"** appears only when filters hide issues; clear resets them.
- [ ] Per-issue card shows title + severity + location (Artifact · Dimension) + lifecycle status; wired to the 6 real issues.

## D087 — Full Issue Panel
- [ ] Panel shows, in order: Header (title · severity · dimension·artifact · lifecycle) → **Why this matters** → **Evidence** (collapsible) → **What this weakens** → **Recommendations** → **History** (pointer) → reanalysis note.

## D088 — Lifecycle
- [ ] The 3-step **Open → Addressed → Resolved** track shows in the panel; no Acknowledge stage.
- [ ] Acting shows **"Addressed · awaiting reanalysis"**; **Resolved only via reanalysis** — there is **no** manual resolve button.
- [ ] Status reflects consistently on the issue cards, the Attention cells, and the artifact badges.

## D089 — Recommendations + Apply this fix
- [ ] **OSLO Recommended** + **Possible resolution paths**; selecting a path → **Selected Path = Confirmed by you**.
- [ ] Single **"Apply this fix"** drafts (where possible) → applies → reanalysis → issue advances Addressed then Resolved.
- [ ] Confidence moves **direction-only** (no fabricated number).
- [ ] Recommendations appear **only inside the issue** (no standalone/orphan surface).

## D090 — Clarification loop
- [ ] The clarification block (question + answer) is present in the panel; answering updates project info → reanalysis → the issue closes.

## D091 — Empty states
- [ ] Four honest empty states reachable: none-found / none-under-lens / not-yet-analyzed / unavailable, plus the honest hidden-by-filters count.

## Cross-cutting
- [ ] Advisory-only (D001): copy never says OSLO resolves/plans it for you; issues close only via reanalysis.
- [ ] Severity color only (D003); confidence/CAF neutral.
- [ ] Terms: "Issues", "Clarity·Alignment·Feasibility", **"Artifact"** filter, "Confirmed by you"/"From OSLO", "Apply this fix", "Plan artifacts".
- [ ] Dark default + WCAG 2.1 AA: list, filters, group toggle, and panel are keyboard-operable with focus-visible rings.
- [ ] The Attention-map scoped routing (D058) opens into this full surface consistently.
- [ ] Slices 1–5 intact: activation funnel, intake, Fast Pass, confidence-led Overview + pill/popover, Attention heatmap, chat + notices, feature tour, analysis-state machine, and the full Artifact Workspace (annotations, stepper, editor).
- [ ] `node --check` on the extracted script passes; jsdom parse yields `document.body.children.length > 0` with all key elements present.
- [ ] Not built (seams honored): threaded comments/@mentions (Slice 9); full History timeline (Slice 7 — pointer only).

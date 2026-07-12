# Slice 2 — Intake & Fast-Pass Orientation · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** this slice = Slice 1 + Slice 2. Every Slice-1 flow is preserved; Slice 2 replaces the Slice-1 *stub Overview* with a real (illustrative) confidence-led Overview + a reachable Attention Map, and adds the analysis-state machine (Fast Pass → orientation → Extended Analysis) and the clarification loop.

Labels marked **[INHERITED]** are unchanged from Slice 1; **[NEW · S2]** are introduced here.

---

## 1. End-to-end flow

```
[INHERITED S1]  Invite email → Activate → Welcome → Intake (4 start methods)
                       │
      ingest() ┌───────┴────────────────────────────────────────────┐
[NEW · S2]     ▼                                                     │
        Fast Pass "Initial Analysis" (≈30s, paced) ── D031/D036      │
          Extract → Construct 7 sections → Evaluate CAF → Ready      │
                       │                                             │
[INHERITED S1] One-time strategic-chain orientation (first project) ─┘  D027/D039
                       │
[NEW · S2]     ▼
        Land on confidence-led OVERVIEW (provisional)  ── D038/D019/DL-096
          · completion notice → OSLO CHAT (not an Overview banner): "Initial Analysis complete in Ns — under the 60-second target" + "Take a quick tour →" (fresh only, D043/D044)
          · all six Fast Pass outputs surfaced (D037)
          · Overview sections EXACTLY: Confidence → Start here → Progress → More (D046/DL-096)
          · Attention Map reachable as co-primary top-center view (D038)
                       │
[NEW · S2]     ▼  (auto, non-blocking)
        Extended Analysis (Deep Pass) runs ── D040
          · success → supersedes provisional → CURRENT (chip flips; completion notice → OSLO CHAT, D043)
          · failure → last-good + Retry (notice → OSLO CHAT) ── D041/D043
                       │
[NEW · S2]     ▼
        Clarification loop ── D042
          answer (at orientation OR in-issue) → update project info → reanalysis → issue closes
```

---

## 2. Screens & states

### 2.1 Intake [INHERITED S1]
Four start methods (Describe · Attach · Templates · Sample) — D023. Sample loads the DevNorth 2026 brief into the composer; the user initiates analysis (D030). No behavior change in S2; it is the on-ramp to the new analysis flow.

### 2.2 Fast Pass — "Initial Analysis" [NEW · S2, extends S1 pacing]
- Rails-first hold: spinner, "Analyzing…" pill, streaming mono trace, four interstitials. **Paced ≈30s** (D031); GA anonymous ≈12s.
- Interstitials now name the **seven-section construction** explicitly (Extract → Infer → Construct → Evaluate).
- The elapsed time is **measured** (`Date.now()` deltas), not a fixed literal (D036). The arrival notice frames it "under the 60-second target."
- Reduced-motion honored (no spinner/pulse) (D015).

### 2.3 Orientation overlay [INHERITED S1]
One-time strategic chain (Understanding·OSLO → Judgement·you → Decision·you → Oversight·you). Fires **first project only** (D027/D039); re-openable from account menu.

### 2.4 Overview (confidence-led) [NEW · S2 — replaces the S1 stub · reconciled to DL-096, Rev 2]
Landing view after Fast Pass (D038). Sections are **EXACTLY** (D046/DL-096, matching `oslo_r1_overview_redesign_mockup.html`): **Confidence → Start here → Progress → More**. No completion banners render here (moved to OSLO chat, D043).
- **Confidence** — focal score `58/100` + "/100", meaning line "Understanding is forming", band + **reliability as an inline qualifier** ("Moderate · qualified by moderate reliability"; reliability detail via the **Why** disclosure, **not** a standalone Reliability card — D046). Carries the **provisional↔current chip** (D040). Quiet **trend sparkline** ("↗ N since your change · from X") shown once Extended Analysis supersedes. **What's driving it** — Clarity/Alignment/Feasibility maturity bars, neutral ramp, 5-band words (Very Low…Very High, DL-086/098), lowest flagged **"the limit"** (D003, no health color). **Summary counts only** — "N issues open · M resolved" (no confirmation/attestation views — D045). Why + Timeline links.
- **Start here** — the top open issue + "Then: …" + "See all N issues" (D037). A **light clarification pointer** (D042) sits here — the question + answer box live in the tied **Issue detail**, not on the Overview.
- **Progress** — resolved count + open/critical + Plan artifacts drafted (7/7) + Dependencies confirmed, plus the analysis-state line (status, not a notification) — D037.
- **More** (collapsible): Project summary + the **7 plan artifacts** with From OSLO / reliability labels — D035.

### 2.5 Attention Map (co-primary) [NEW · S2]
Reachable via the top-center view switch (Overview · Attention) — D038/NAV-C3. Heatmap-primary (D007): rows = 7 plan artifacts (grouped Understanding / Execution), columns = Clarity·Alignment·Feasibility. Cell brightness = severity of the worst open issue; **empty cells are calm/neutral, severity color only on issues** (D003). Secondary "Dimensions" toggle shows the three CAF bands. Clicking a cell routes to the issue (light panel).

### 2.6 Light Issue panel [NEW · S2, minimal]
Slide-in panel: header (severity + title) → lifecycle chip (Open→Addressed→Resolved, D018) → Why → Evidence → **Clarification request** (if any) → Suggested fixes. Enough to demonstrate the clarification loop; the full Issues UI (filters, By-dimension/By-severity, apply-fix drafting) is **Slice 6** — a clear seam.

### 2.7 Analysis-state machine [NEW · S2 · Rev 2]
Completion/failure notices are delivered as **OSLO chat messages** (D043); the **chip** and the **Progress state line** remain as status on the Overview.
| State | Trigger | Overview | Chip | Chat notice (D043) |
|---|---|---|---|---|
| provisional | Fast Pass complete | 58 / Moderate / Feas Very Low | Provisional (amber) | "Initial Analysis complete in Ns — under the 60-second target" + tour offer |
| current | Extended Analysis success | 62 / Moderate / Feas Low | Current (green) | "Extended Analysis complete — superseded the provisional orientation." |
| error (last-good) | Extended Analysis fail (demo trigger) | unchanged (last-good) | Last-good (amber) | "couldn't complete — showing your last-good understanding · Retry" |
| current (recovered) | Retry succeeds | 62 / current | Current | (retry → complete message) |

Only reanalysis changes the assessment; last-good preserved on failure (D041, D006).

### 2.8 OSLO chat rail + feature tour [NEW · S2 · Rev 2]
- **Global OSLO chat rail** (right, collapsible) — persistent advisor. **Completion notices land here** (D043): fast-pass and deep-pass completions, plus failure/retry and claim-through confirmations. Seeded with an intro message on landing.
- **Optional feature tour** (D044) — spotlight coachmarks (`.tourmask`/`.tourtip`, `startTour()`), **opt-in, never gating value**. Offered from (a) the chat completion message ("Take a quick tour →") and (b) a small left-rail "Take a quick tour" affordance. Steps spotlight surfaces that **exist by Slice 2**: the strategic read/Overview (Confidence), the "Start here" focus, the Attention map switch, and the OSLO chat. Dismissible/skippable; marked seen in `localStorage` (`oslo-s1-tourSeen`) so it sunsets with proficiency. **Slice 5 seam**: an artifact-edit step is stubbed in a code comment (no artifact editor faked). **Slice 8 seam**: a Settings→Help re-open control is left as a comment (no Settings built here).

---

## 3. Advisory framing (cross-cutting)
Persistent advisory footer [INHERITED]. All Slice-2 copy stays advisory: "OSLO asks; you answer; you decide"; clarification and fixes never mutate the plan without the user. No copy implies OSLO plans/decides/runs the project (D001).

---

## Revision 2 (2026-07-09)
Owner-directed fixes applied: **D043** completion notices moved from Overview banners to the OSLO chat rail (status pill + Progress state line kept as status); **D044** optional feature tour added (chat + rail launch, 4 Slice-2 surfaces, localStorage-seen, Slice 5/8 seams); **D045** confirmations live in the Issue detail, Overview shows summary counts only; **D046** Overview reconciled to DL-096 (Confidence → Start here → Progress → More; standalone Reliability card removed → inline qualifier + Why disclosure). Slice 1 funnel and the rest of Slice 2 unchanged.

---

## Chat integration (D108 cascade)

The OSLO chat rail becomes a **working advisor** in Slice 2, not just a place completion notices land. It is advisory-only (D001): OSLO reads and explains, and the user acts.

**What the user can now do**
- **Ask, and get a grounded answer.** Type a question (Send, or Enter — Shift+Enter for a newline) and OSLO answers from the *live* read: the confidence index/band and its reliability qualifier, the limiting CAF dimension, the open-issue count and the top issue, the analysis state (provisional / current / last-good). The replies are simulated, but nothing in them is invented — every number and every issue traces to what the Overview and the Attention map are showing.
- **Hand a surface to the chat.** "**✦ Ask OSLO why**" beside the confidence number, and "**✦ Ask OSLO about this issue**" in the Issue panel, open the conversation *about that thing*. A **context pill** at the top of the rail names what OSLO is scoped to; the **×** clears it and OSLO says so ("Context cleared — I'm answering across the whole project again").
- **Start from a suggestion.** State-derived prompt chips sit above the composer ("What should I do next?", "Why is Feasibility Very Low?", "Explain the top issue", "What do you need me to confirm?"). They change as the read changes.
- **Answer a clarification in the conversation.** Where the inputs are thin, OSLO raises the question *in the thread* with an answer box. Answering there does exactly what answering in the Issue panel does — the same project-information update ("From OSLO" → "Confirmed by you"), the same issue transition, the same analysis update, the same refreshed read. There is no side channel and no second answer path; the panel also offers "Answer in chat →" as a route into the same loop.
- **Be told the boundary, plainly.** Ask OSLO to fix, close, or resolve something and it says it can't: *"I read and explain, you decide."* An issue closes only when an **analysis update** confirms it no longer holds. Every action OSLO offers is a **link the user clicks**, which runs the same surface the UI already exposes (open the issue, open the Attention map, see the read).

**Journey impact:** unchanged funnel (activation → intake → Fast Pass → orientation → Overview). The chat now carries the *why* alongside the *what* — the orientation moment ends with an advisor the user can interrogate, not just a report they must decode.

**Scope boundary (kept deliberately):** no Discuss / resolution-path conversation (Slice 6), no artifact ask or editing (Slice 5), no History or timeline references (Slice 7), no Attention-cell ask (Slice 4). OSLO never claims to have changed the plan, and "analysis update" — never "reanalysis" — is how the read moves.

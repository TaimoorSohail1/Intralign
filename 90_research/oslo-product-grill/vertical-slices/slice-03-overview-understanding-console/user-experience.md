# Slice 3 — Project Overview & Understanding Console · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** Slice 1 + Slice 2 + Slice 3.
**Baseline of record:** `oslo_r1_experience_mockup_v4.html` (2026-07-09).
**Boundary:** advisory-only (D001); confidence = understanding maturity, neutral (D002); severity color only on issues (D003); dark default + WCAG 2.1 AA (D015). Client-side prototype only (D016).

> This document notes what is **INHERITED** from Slice 1/2 (unchanged) and what is **NEW in Slice 3**. Nothing from Slice 1/2 regresses.

---

## INHERITED from Slice 1 (unchanged)
- Invite → activate → welcome funnel (D021/D022); four start methods (D023, Guided Q&A out); GA-phase anonymous + save-to-keep, labelled not default (D024–D026, D032); one-time strategic-chain orientation + advisory footer (D027); account menu logout + stay-signed-in (D028); hero headline A + descriptor (D029); sample = all-phase, user-initiated (D030); attach types + ingestion depth (D033/D034).

## INHERITED from Slice 2 (unchanged)
- Intake constructs all 7 plan artifacts, reliability-qualified, thin evidence → clarifications (D035); Fast Pass ≈30s with a **measured** completion time framed "under the 60-second target" (D031/D036); the six Fast Pass outputs at orientation (D037); **land on the confidence-led Overview** with **Attention map co-primary** (D038); first-run orientation + fresh-arrival notice (D039); **Extended Analysis auto-runs, non-blocking, supersedes** provisional→current (D040); Extended-Analysis failure → last-good + retry (D041); the **clarification loop** — light prompt inside *Start here* + the question/answer inside the tied Issue → reanalysis → issue closes (D042); **completion notices delivered via OSLO chat** (D043); optional **feature tour** (D044); confirmations live in the Issue detail, Overview shows counts only (D045); **Overview = Confidence → Start here → Progress → More**, reliability inline not a card (D046); v4 Progress ledger (D047); **"Plan artifacts"** term (D048/D049).

---

## NEW in Slice 3 — the Understanding Console

Slice 3 does not add screens. It deepens the *one* confidence surface and gives it a compact console home in the top bar. Everything new is either in the **Confidence pill popover**, the **Confidence card** (subtle markers only), the **Why** disclosure, or the **Project summary** in More — never as a new standing Overview section, and never as a separate reliability card (DL-096/D046).

### 1. Confidence pill → compact console (D050)
The always-visible top-bar pill shows **index + band + reliability qualifier** (e.g. "Confidence 58 · Moderate · Moderate reliability"). In Slice 2 it merely jumped to the Overview; in Slice 3 **clicking it opens a popover** — the compact understanding console:
- **First level:** the three CAF dimensions (Clarity · Alignment · Feasibility) with band words.
- **Reliability basis section** (see §2).
- A conditional **false-confidence flag** (see §3).
- A **"Open full breakdown → Overview"** button.
The pill is the **single home** for the live metrics; the Overview is not duplicated inside the popover, and the metrics are not re-stated as new Overview cards.

### 2. Reliability basis (D051)
The popover's Reliability basis section shows three levels, **judged independently of CAF**:
- **Coverage** — how much of the project reality was observable in your inputs.
- **Evidence availability** — presence/accessibility of supporting evidence.
- **How assessable** — plain label for Assessability (D012): how readily the plan can be assessed while key dependencies are unconfirmed.
Levels use the reliability scale **High / Moderate / Low**. The basis is **also reachable from the Overview "Why"** disclosure (no separate Overview reliability card — reliability stays the inline qualifier + Why per D046).

### 3. False-confidence flag (D052, CONF-06)
When a **high band sits on low reliability**, a **neutral, advisory, non-alarming** flag appears in both the popover and the Confidence card. It **names the cause** — here a *reliability shortfall*, distinguished from a *CAF weakness* — and says what would firm it up. It is **never health/severity colored** (neutral surface + info glyph only, D003). When the condition doesn't hold, the flag is **absent**. Demoable via the phase-bar "Sim false-confidence" trigger.

### 4. Confidence stages (D053, CONF-05)
The understanding-maturity stage — **Orientation ▸ Expanded ▸ Validated** — is surfaced **subtly**: named in the Confidence info tooltip and shown as a quiet stage marker (stagepips) beside the number and in the popover header. It is **not standing chrome**. At Fast Pass the read is at **Orientation**; after Extended Analysis it advances to **Expanded**.

### 5. "How this is calculated" (D054)
A subtle affordance sits by the confidence number. On hover/click it explains the number is **CAF-derived** (lowest dimension sets the ceiling), **reliability-qualified**, and **cause-bound** (every move names a reason), and that **below-band jitter is not dramatized** — only a band change is meaningful.

### 6. Project summary depth (D055)
The Project summary in **More** is a plain-language narrative covering: **what the project is · understanding level (with stage) · main limiter · reliability basis · the "not health / readiness / probability" caveat.**

### 7. Confidence movement is direction-only (D056)
Any confidence move is shown **direction-only** (▲/▼ with a **named cause**), never a fabricated magnitude. The Extended-Analysis chat notice reads "Confidence moved ▲ up — deeper analysis firmed up the read" (not "58 → 62"), and the trend row reads "Up — deeper analysis firmed up the read." Confidence **can fall** and still mean *better understanding, not a worse project*.

---

## Journey (Slice 3 lens)
1. Activate → intake → Fast Pass ≈30s (INHERITED) → land on the confidence-led Overview.
2. The **pill** carries the live read; the user clicks it to open the **console** — CAF first, then reliability basis, then (if it holds) the false-confidence flag.
3. On the card, the user can read the **stage**, open **"how this is calculated,"** or expand **Why** to reach the reliability basis in prose.
4. Extended Analysis supersedes; the stage advances Orientation ▸ Expanded and the movement shows **direction-only**.
5. The **Project summary** in More gives the full narrative.

All calls stay with the user (D001). OSLO reads and explains; nothing changes the plan without the user.

---

## App shell (D093/D094/D095 — shell cascade, 2026-07-09)

Slice 3 now wears the **approved OSLO app shell** (ported from Slice 6) so navigation is identical across every slice. The old top-center Overview·Attention toggle is gone; primary navigation lives in a **persistent left sidebar**.

- **Persistent left sidebar — PROJECT nav.** Overview (**live** confidence-led console) · Issues · History · Attention map (**live**, basic map from Slice 2). The active view highlights with `aria-current="page"`, and the top-bar breadcrumb names where you are.
- **Slice-3 live vs. seams:**
  - **Overview** — live (the understanding console; nothing regresses).
  - **Attention map** — live (basic heatmap + dimensions; from Slice 2).
  - **Issues** — Slice 3 has only the **light issue panel** (open any issue from the Overview "Start here" list or an Attention cell). The Issues nav item and the palette's "Issues" jump route to a **clearly-labeled seam** — *"Full Issues view arrives in Slice 6."* Never a broken or wrong view.
  - **History** — a **clearly-labeled seam** — *"History & timeline — arrives in Slice 7."* The Overview's "Timeline →" link routes here.
- **PLAN ARTIFACTS section is omitted** from the sidebar in Slice 3 — the artifact editor first appears in Slice 5. (The Overview's "7 plan artifacts" narrative and the More list are unchanged; only the *editor* is absent.)
- **Top bar.** Intralign brand · project switcher (Slice-8 seam) · `sample` tag · breadcrumb; the **Confidence pill stays the one home for the metrics** (D050); right cluster adds search · Share (Slice-9 seam) · Export (Slice-9 seam) · report · **Free** plan chip. A `☰` button opens the sidebar as a drawer on narrow screens; the OSLO chat rail, feature tour (now a sidebar-foot button), confidence popover, and phase-bar offset are all preserved.
- **Command palette (⌘/Ctrl+K or the ⌕ button).** Keyboard-operable jump-to: **GO TO** the four project views, and **OPEN AN ISSUE** (each still-open issue opens the light panel). No PLAN ARTIFACTS group in Slice 3.
- **Chrome stays neutral/brand** (D003) — sidebar badges are neutral; severity color remains on issue badges only.

---

## Chat integration (D108 cascade)

The OSLO rail was a persistent advisor that **could not be talked to** — the composer and Send were inert. In Slice 3 the chat becomes a **real conversation**, grounded in the read that is on screen. It stays what it always was: **advisory** (D001). OSLO reads and explains; it points you at the action, you take it.

**You can now ask.** Type a question and hit **Enter** (Shift+Enter for a new line) or click **Send**. Suggested prompt chips sit above the composer and are **derived from your live read** — "What should I do next?", "Why is Feasibility Very Low?", "Explain the top issue" — so the chat is never a blank box. Before the first message, an empty state says plainly what OSLO can and cannot do.

**Every answer traces to your actual state.** OSLO answers from the confidence read, the CAF dimensions, the reliability basis, the analysis state, the open issues, and the seven plan artifacts as they stand *right now* — not from a script. Answer a clarification and the next reply reflects the new number.

**"✦ Ask OSLO why" — the confidence read, explained.** Beside the number on the Overview (right under *How this is calculated*), this hands the confidence read to the chat and pins it as **Context**. Slice 3 is where the understanding console lives, so this answer is the rich one:

- **What's holding it back** — the **limiting CAF dimension** (the weakest of Clarity · Alignment · Feasibility caps the number), with all three levels named.
- **How much OSLO had to go on** — the **reliability basis**: Coverage · Evidence availability · How assessable — and the point that reliability is judged *independently of the plan's integrity*. Reliability says how firm the read is, not how good the plan is. That's why the number is never shown without it.
- **Where the understanding is** — the **stage** (Orientation ▸ Expanded ▸ Validated) and whether the read is provisional, current, or last-good.
- **The false-confidence condition**, but only when it actually holds — a High band on Low reliability is flagged, not hidden.
- **What would move it** — named against the live open issues, with the honest boundary: the number moves only when an **analysis update** changes the read, never because something was dismissed.

**"✦ Ask OSLO about this issue."** In the light issue panel, hand any issue to the chat: why it matters, what it rests on, the suggested fixes, and whether its dimension is the one capping your confidence. The panel steps aside so the conversation is visible.

**Context, and clearing it.** When a surface hands something to the chat, a **Context** pill names it ("Your confidence read", "Venue Wi-Fi capacity is unconfirmed (ISS-01)"). Follow-ups stay inside that context — a bare "why?" means *why this*. The **×** clears it, and OSLO says so.

**Answer a clarification without leaving the conversation.** When OSLO has a question tied to an issue, the answer box appears **in the chat**. Answering there does **exactly** what answering in the issue panel does — same project-information update, same *Confirmed by you* basis change, same reliability lift, same analysis update, same issue closure, same refreshed Overview. The chat is not a shortcut and not a side door; it is the same door. OSLO reports the update as it runs, and tells you when it lands — it never claims to have closed the issue itself.

**What the chat will not do.** It will not change your plan, edit an artifact, resolve an issue, or move the assessment. Ask it to "just fix it" and it says so, then shows you where the real action is. Replies link straight to the surface — the issue, the Attention map, the confidence console — so a conversation always ends somewhere you can act.

**Not in Slice 3.** No recommendation paths / "Discuss" (Slice 6), no artifact-editor ask (Slice 5), no History links (Slice 7). The chat never offers an action this slice cannot run.

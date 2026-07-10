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

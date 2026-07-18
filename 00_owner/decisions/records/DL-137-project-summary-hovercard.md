# DL-137 — The Project summary retires from the Overview — it becomes a hovercard on the project name

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The Project summary retires from the Overview — it becomes a hovercard on the project name

**Class:** B (experience-doctrine refinement — the Overview's standing panels) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Refines** DL-096 / D046 (the "More" section) and D055 (the plain-language project narrative). **Upholds** the OSLO-voice check (`#proj-summary` stays a graded surface).

---

## Decision

The standing **"More → Project summary"** panel is **retired from the Overview** and relocated to a **hovercard on the project name** (`#tbProj`) in the top bar. Hover or keyboard-focus the project name to read the summary; a click still opens the project switcher (the hovercard dismisses).

The panel was self-described as optional — its own header read *"the read above is the summary."* With the lead-line (DL-132) leading the read and the ramp, limiter and "Why" box already on the card, its **Understanding-level**, **Main-limiter** and **Reliability-basis** sections duplicated the read on a second standing surface. The one genuinely unique part — **"What this is"** (the plain description of the project itself) — is not a read at all; it belongs with the **project**, which is exactly what the project name anchors. So the whole summary moves to a hovercard tied to the project name, where the duplication is on-demand reference rather than standing clutter, and the project description sits where a reader would look for it.

Nothing is lost: the full summary (What this is · Understanding level · Main limiter · Reliability basis · the caveat) moves intact, `syncReliabilityCopy()` keeps its live fields (`#ps-band` · `#ps-stagew` · `#ps-rel`) current, and the `#proj-summary` element — a graded OSLO-voice surface — stays present inside the hovercard.

## Why — the constraint that shaped it

Two forces pointed the same way. First, the Overview declutter thread: a standing panel that repeats the read is exactly the guidance density the first-time work set out to cut. Second, information architecture: a *project* summary is a property of the project, not of the Overview view — anchoring it to the project name makes it discoverable where its subject lives, and frees the Overview to be the read. The move is a relocation, not a deletion; the summary is one hover away, not gone.

## Guardrails

- **The summary survives, on demand** — the full narrative moves into `#projSummaryPop`; nothing is trimmed. `syncReliabilityCopy()` still paints its live fields.
- **`#proj-summary` stays a graded voice surface** — it remains in the DOM (inside the hovercard) and in `_OSLO_VOICE_SURFACES`, so the second-person voice check still grades it (it resolves to a real element, never a blind pass).
- **The hovercard is an opaque, registered dialog** — `#projSummaryPop` is in `_DIALOG_PANELS`. → `_assertEveryDialogHasAnOpaquePanel()`.
- **No conflict with the switcher** — hover/focus shows the card; click opens the project menu and the card hides (`toggleProjMenu` dismisses it).

## Governance

Lands as Class-B canon via `dl-land`, refining DL-096/D046 and D055. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; the standing panel removed, the hovercard verified on hover, `#proj-summary` still voice-graded). AI drafted + built; **only the owner ratifies.**

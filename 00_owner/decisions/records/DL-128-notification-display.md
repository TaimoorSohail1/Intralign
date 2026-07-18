# DL-128 — Event is a notification, read-movement is a delta; one moment one toast

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The event is a notification, the read-movement is a delta — and one moment shows one toast

**Class:** B (experience-doctrine — notification & recognition display) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18 · **Realizes** DL-122 / D179a / D179b · **Additive to** the recognition layer.
**Build:** `slice-10-tiering-limits/prototype.html`.

---

## Decision

Two clarifications to how OSLO surfaces what changed, both resolving the same confusion: an **event** (what happened) and a **read-movement** (how the read changed) are different things with different homes, and they must not compete for the same surface or fire as duplicate toasts.

### 1. The payoff card is a READ-DELTA; the event is a NOTIFICATION

The "What changed" card inside the Confidence read fused two things: an **event headline** ("You applied OSLO's fix to Requirements") and a **read-movement** ("Grounding: partly → largely grounded"). The event is a **notification** — awareness that something happened — and its home is the notification lane (global toast + the Notifications record), attributed to **no panel** (DL-122). The read-movement is the **payoff** — a statement about the read — and its home is inside the Confidence card (D179b).

So the payoff card now renders the **read-movement only**; the event headline leaves the card for the notification lane (D179a — an event may annotate the state, never share its panel; and it was already being published there, so the headline was a redundant second copy in the wrong container). The Extended pass — the one resolution path that had been firing a payoff without also routing a notification — now routes its event to the lane like every other path, so every event has one home and the card is consistently a delta. Guard: `_assertPayoffCardIsReadDeltaNotEvent` (the card carries the read-movement and never an event headline).

### 2. One moment shows one toast — and a recognition outranks the routine notification

Because a single action can produce both a recognition (earned) and a routine "analysis landed" notification (awareness) for the **same event**, the two were toasting at once — the same thing said twice, in two lanes. Every toast now passes through **one queue** and shows **one at a time**, with a precedence rule:

- **Recognition wins.** When a recognition is in the batch, the coincident routine notification **toasts are dropped** — they say a weaker version of what the recognition just said. Their **awareness record is untouched** (`routeNotification` unshifts it into the Notifications record before it ever enqueues a toast), so the bell still carries the event. Nothing is lost; the duplicate toast is.
- **No stacking.** Genuinely-distinct toasts (two separate milestones; a recognition plus an unrelated reply) present in sequence, highest-priority first (loud milestone > milestone > first > notification), never stacked into a wall; a hard cap bounds the queue.
- **Lone notifications still toast** — precedence only collapses the *redundant* pair; a notification with no coincident recognition shows normally.

Guard: `_assertRecognitionOutranksNotificationToast` (pure precedence rule + queue mechanism: recognition drops the coincident notification toast, the record is kept, one at a time).

---

## Why this is the honest frame

It is the same line drawn twice: **OSLO's work is a notification; the user's earned progress is a recognition; the read's movement is a delta on the read.** The Extended pass landing (OSLO computing harder) is a notification, not an achievement — which is also why stage-advance-to-Expanded is not recognized (see the recognition record). Keeping these on separate, non-competing surfaces is what lets each stay truthful.

## Governance

Lands as canon via `dl-land`, realizing DL-122 / D179a / D179b (no new invariant beyond them). Built + verified in the deliverable prototype (boot self-check **149/149**, 0 pageerrors; new guards `payoffIsReadDeltaNotEvent` + `recognitionOutranksNotifToast` green; `payoffIsADelta` still green). AI drafted + built; **only the owner ratifies.**

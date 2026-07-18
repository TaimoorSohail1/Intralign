# DL-133 — The feature tour is offered after the strategic chain, not left to be hunted for

- **Date:** 2026-07-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B

# The feature tour is offered after the strategic chain, not left to be hunted for

**Class:** B (experience-doctrine refinement — onboarding) · **Framework 001** — AI drafts + builds; **owner ratifies at land.**
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-18. **Refines** D044 (the optional feature tour) and D093 (the tour affordance's home). **Upholds** D044's principle — the tour never gates value.

---

## Decision

Right after the strategic-chain orientation closes, OSLO now **offers** the feature tour instead of leaving the user to discover it. The offer is a small card (`#tourOffer`, bottom-left): **"Want a quick tour?"** with **Start tour →** and **Not now**. It honours D044 literally — OSLO offers the tour, it does **not** auto-run it.

The flow has three outcomes, first-run only:
- **Accept** → the tour runs (`startTour`).
- **Decline** ("Not now" / dismiss) → the offer disappears and the left-rail **"Take a quick tour"** chip (`#railTour`) is revealed as a standing future reminder.
- **Already answered** → once the offer has been shown and answered (`tourOffered`), it never appears again; the rail chip carries re-entry until the tour is taken (`tourSeen`), then retires for good.

The rail chip is therefore the tour's **post-decline reminder**, not a permanent button: it is hidden by default, revealed on decline (or on load when the offer was answered but the tour not yet taken), and hidden once the tour is taken. Visibility is owned by one function (`_syncRailTour`). The command palette keeps a "Take a quick tour" entry (HELP group) as a durable, unobtrusive re-entry point.

## Why — the regression this corrects

A prior declutter had removed the standing rail chip, which silently took the tour prompt out of view at the Overview reveal (the chat completion offer fires only once, at fast-pass completion). The correct model — the one the owner described — is **offer-then-remind**: prompt the user at the moment they land, and if they decline, leave a quiet standing reminder rather than either nagging or vanishing. This restores that model and makes the tour's discoverability a deliberate onboarding step instead of an accident of where a chip happened to live.

## Guardrails

- **The tour never gates value (D044)** — the offer is dismissible, the tour is opt-in, and neither blocks the product; "opt-in" is honoured as *offer + opt-out*, never auto-run.
- **The offer shows once** — `tourOffered` prevents a second prompt; the rail chip (not a repeated modal) is the standing reminder.
- **One owner of chip visibility** — `_syncRailTour()` is the single source of truth (hidden before the offer · shown after decline while not-yet-taken · hidden once taken).
- **The offer card is an opaque, registered dialog** — `#tourOffer` is in `_DIALOG_PANELS`, so the dialog-opacity guard grades it. → `_assertEveryDialogHasAnOpaquePanel()`.
- **Restart replays it** — `resetDemo` clears `tourOffered` (with `orientSeen`/`tourSeen`) so the first-run journey replays intact.

## Governance

Lands as Class-B canon via `dl-land`, refining D044/D093. Built + verified in the deliverable prototype (boot self-check **152/152**, 0 pageerrors; offer→accept and offer→decline→chip both verified). AI drafted + built; **only the owner ratifies.**

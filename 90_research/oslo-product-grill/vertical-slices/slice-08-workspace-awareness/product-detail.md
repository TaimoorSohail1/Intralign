# Slice 8 — Multi-Project Workspace & Awareness · Product Detail

Cumulative Slices 1–8. This document specifies the behavior of each Slice-8 surface at product-requirement granularity. Advisory-only, visibility-first, client-side (D016).

## D102 — Workspace Home / Dashboard

**Entry.** Top-left Intralign/OSLO logo (`role="button"`, Enter/Space operable) → `showWorkspace()`. Also reachable from the switcher (⊞ Workspace Home) and from a shared-with-me notification.

**Context.** A distinct **"Workspace"** context, not a project view: its own top bar (*Intralign · Workspace*), a Free-plan chip, a notifications bell, and an account avatar → Settings. It overlays the project shell; leaving it (entering a project, or a notification routing into the app) returns to the shell.

**Content.**
- **★ Pinned** grid + **Recent** grid of project cards. Card fields (per the data model): name · ownership (*Owned* / *Shared with me*) · analysis status (*Analyzed* / neutral *⋯ Analysis stale* chip) · **reliability-qualified understanding indicator** (neutral maturity dot + "Understanding **{band}** · qualified by {reliability} reliability") · recency · open-issues count · artifact count · Pinned tag where applicable.
- A **New project** card (dashed) + a header **+ New project** button.
- **No computed scores across projects** honesty note (with an ⓘ): each project is assessed on its own inputs/reliability; no portfolio score, average, or ranking.
- **Archived projects (N)** section — each archived project shows name + "history & last assessment retained" + a **Restore** button. Non-destructive.
- Footer note: **1 active project** (Free plan, DevNorth 2026); recent cards illustrative; archiving non-destructive.

**Actions.**
- Open a card: real project (DevNorth) → enter shell at Overview; illustrative → honest toast.
- New project → **at the Free cap** → the **upgrade-or-archive** prompt (D048; below).
- Restore (archived) → non-destructive toast (illustrative).

**Honesty.** Understanding is per-project and reliability-qualified; nothing is rolled up or ranked; archiving never deletes.

## D103 — Project switcher

**Entry.** Top-bar "DevNorth 2026 ▾" chip → `toggleProjMenu()`; keyboard-operable; closes on Escape / outside click. Anchored below the chip.

**Content (rendered live).** Section label "Projects" → each non-archived project (neutral maturity dot + name + a *stale* chip or a *sample* chip) → divider → **+ New project** → **⊞ Workspace Home**.

**Behavior.** Switching is illustrative (one real project). New project → the Free-cap prompt. Workspace Home → `showWorkspace()`.

## D104 — Notifications / awareness

**Entry.** Top-bar bell (◔) with an **unread badge** (also in the Workspace Home top bar). Right-hand slide-in panel + a scrim.

**Categories (R1).** mention · reply · shared-with-me · analysis complete · analysis failed · stale. (No "reanalysis" wording — D092.)

**Item.** icon + label + source line + timestamp + category chip; unread items carry a filled dot and a faint tint.

**Rules.**
- **read/unread is presentation-only.** *Mark all read* and opening an item update the badge and nothing else. No assessment changes.
- **Routes to source.** mention → its artifact (`openArtifact`); reply → Issues (`showView('issues')`); analysis complete / stale → History; analysis failed → Overview; shared-with-me → Workspace Home. Routing first ensures the project shell is visible.
- **Persistent note:** "Awareness is presentation-only — it never triggers an analysis, and marking items read changes nothing."
- Badge is **neutral/brand**, never a severity color (D003).

## D105 — Settings (visibility-first)

**Entry.** Account menu → Settings, and sidebar *Your account · Settings* → `openSettings()`. Full-viewport surface; **left section nav** (keyboard-operable) + scrolling panels; Escape / *Back to app* closes; default section = Account.

**Sections (11).** Account · Profile · Appearance · Notifications · Workspace · Project defaults · Collaboration · Membership · Subscription · Billing · Integrations.

**Visibility-first areas** (tagged *visibility* / *view-only*): **Subscription** (Plan: Free · Active projects: 1 of 1 · Analysis: Initial only · Upgrade →), **Billing** (no payment method · no invoices), **Integrations** (none · configuration deferred), **Membership** (Idris = Owner · 1 member · invite & roles arrive with collaboration). **Facts + upgrade paths only — no enforcement, no real billing.**

**Seams onward.** Collaboration → *Manage* → the Slice-9 sharing seam. (Sharing/collaboration internals are not built here.)

## D106 — Appearance (theme + a11y)

**Theme.** Settings → Appearance → a **Dark / Light** segmented control. **Dark is the default.** `setTheme(t)` flips a single `data-theme` attribute on `document.documentElement` (light token overrides pre-exist), applies instantly, and persists to `localStorage`. **Match system** clears the override → follows `prefers-color-scheme`; a media-query listener keeps an un-overridden preference in sync with OS changes.

**Accessibility.** Reduced motion is honored (CSS `@media (prefers-reduced-motion: reduce)`); focus indicators are always visible (`:focus-visible` ring). Both are surfaced as read-only facts in the Appearance section. The app is fully usable in light mode with no neutral-ramp/severity-color regression (both have light token values).

## D048 — Upgrade-or-archive at the Free cap (reused)

Triggered by any **New project** action at the cap (Workspace Home, switcher, Free chips). A modal: "Free plan · 1 active project" → two options: **Upgrade your plan** (→ Settings → Subscription, visibility-only) and **Archive DevNorth 2026 to free the slot** (non-destructive; history/issues/last assessment retained & restorable). *Not now* dismisses. No charge, no enforcement.

# Slice 8 (Workspace & Awareness) — Critical Analysis & Refinements
Date: 2026-07-09 · Scope: Workspace Home, project switcher, Notifications, Settings, Appearance in `slice-08-workspace-awareness/prototype.html`. Severity: **S1** blocks · **S2** meaningful · **S3** polish.

## What works well
Notifications are genuinely wired (render, open, mark-all-read, route-to-source) with the honest "never triggers an analysis" note. Appearance has a real dark/light toggle that persists. Workspace Home has the honest "no computed scores across projects" note, a neutral *stale* chip (severity color correctly confined to issues), non-destructive Archive/Restore, and the at-cap upgrade-or-archive prompt. Good, on-doctrine base.

## S2 — Meaningful

### 1. Settings is full of **dead affordances** (the headline issue)
Most Settings rows are read-only text with links that **have no handler**: "Password & security → **Manage**", "Avatar → **Upload**", "Delete account → **Confirmation-gated**", and similar across Workspace / Project defaults / Membership. They render as `<a role="button" tabindex="0">` — focusable, cursor-clickable — but clicking does nothing. That's worse than a labeled stub: it teaches users the app is broken. **Every affordance must either work, be a clearly-labeled seam, or not look interactive.**

**Which should actually be FUNCTIONAL now (prototype-grade, localStorage):**
- **Profile** — editable display name (and optional role/title).
- **Workspace** — editable workspace name.
- **Notifications** — per-category preference toggles. These are legitimately live *because* awareness is presentation-only (D104): the toggles change what the panel shows, not any real delivery.
- **Account** — surface the sign-out and "stay signed in" controls that already exist elsewhere (D028).
- **Appearance** — already functional. ✔

**Which are correctly NOT functional (canon — but must be labeled, not dead):**
- **Subscription / Billing** — visibility-first by DL-048/D014: show plan + usage as *facts* and the upgrade path; billing/enforcement is deferred. Say so ("Billing is handled outside the app in Alpha") instead of a dead "Manage".
- **Integrations / Membership** — not in R1 scope; label as later.
- **Collaboration** — **Slice 9** seam; label it.
- **Delete account** — needs real confirmation semantics; "Confirmation-gated" is internal-spec language leaking into the UI, and the link does nothing.

### 2. Notifications over-promise what Alpha can do
The panel includes **mention · reply · shared-with-me** categories — but collaboration/sharing isn't built until **Slice 9**, and Alpha is invite-only single-user. These events can't actually occur yet, so seeding them with fake data implies capability the product doesn't have. Either gate those categories until Slice 9, or mark them clearly as previews.

### 3. Notification preferences aren't wired
Settings → Notifications is read-only, so users can see categories but not control them — even though presentation-only control is legitimately in scope (see #1).

### 4. The Dashboard doesn't yet earn its space in Alpha
Workspace Home is built for scanning *many* projects (Pinned + Recent), but Alpha/Free caps at **1 active project**. With a single card, the surface feels empty and the switcher near-pointless. Consider a leaner Alpha presentation (a single "current project" + archive + create), with the full Pinned/Recent grid appearing once multi-project is actually available.

### 5. Light mode needs a contrast/AA sweep
The theme toggle works, but light mode has never been audited: the brand orange on light needs the AA-safe variant, and the **neutral maturity ramp** (confidence/CAF) plus **severity colors** must still read correctly and stay distinguishable. This was flagged as an open item in the v4 notes and is still open.

### 6. Stale projects offer no action
A project card can show *stale*, but there's no obvious next step ("open to bring the read up to date"). The status is honest but inert.

## S3 — Polish
7. **No search within Settings** — 11 sections is a lot to scan.
8. **Notifications: no empty state** and "mark all read" discoverability is low.
9. **Switcher with one project** — ensure it degrades gracefully (shows Workspace Home + New project rather than a list of one).
10. **Workspace empty state** — a brand-new workspace with zero projects isn't handled.
11. **Internal spec language in UI** — e.g. "Confirmation-gated"; use plain user language.
12. **Accessibility** — the Settings section nav is keyboard-operable (good); ensure the dead links (once fixed) get proper roles, and the theme control announces state.

## Recommended priority
1. **Fix the dead Settings affordances** (#1) — make Profile/Workspace/Notification-prefs/Account functional; convert Subscription/Billing/Integrations/Membership/Collaboration to clearly-labeled visibility-first or seam rows; remove "Confirmation-gated" phrasing.
2. **Gate or label the collaboration notification categories** (#2) until Slice 9.
3. **Lean the Alpha dashboard** (#4) so it matches the 1-project reality.
4. **Light-mode AA sweep** (#5).
5. Polish: stale→action, settings search, empty states, plain language.

## Note
None of this changes ratified canon. Visibility-first (billing/subscription/integrations/membership) and Collaboration-in-Slice-9 are *correct* — the defect is presenting them as dead links rather than honest, labeled states.

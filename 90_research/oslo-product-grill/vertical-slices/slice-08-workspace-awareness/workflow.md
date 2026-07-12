# Slice 8 — Multi-Project Workspace & Awareness · Workflow

Cumulative Slices 1–8. The Slice-8 flows layer onto the existing shell without disturbing the Slices 1–7 funnel.

## Flow A — Workspace Home (D102)
1. In the project shell, click the **Intralign logo** (top-left) → `showWorkspace()` renders and shows the Workspace overlay.
2. See **★ Pinned** (DevNorth 2026) + **Recent** (Q3 Platform Migration *stale/shared*, Brand Refresh, and a **New project** card), the **no-computed-scores** note, and **Archived projects (1)** with a **Restore** button.
3. Open **DevNorth 2026** → `openProject('devnorth')` → overlay hides, shell shows at **Overview**.
4. Open an illustrative card → honest toast (demo focuses on DevNorth).
5. **+ New project** → Flow D (Free-cap prompt).
6. **Restore** an archived project → non-destructive toast.
7. Escape closes the overlay.

## Flow B — Project switcher (D103)
1. Click **"DevNorth 2026 ▾"** → `toggleProjMenu()` renders + positions the dropdown.
2. See the project list (maturity dots, *stale* / *sample* chips), **+ New project**, **⊞ Workspace Home**.
3. Pick a project (illustrative) / New project (Flow D) / Workspace Home (Flow A).
4. Escape or an outside click closes it.

## Flow C — Notifications / awareness (D104)
1. Click the **bell (◔)** (top bar or Workspace Home) → `openNotif()` slides in the panel + scrim; the unread badge count is shown.
2. Read the items (mention · reply · shared-with-me · analysis complete · analysis failed · stale) and the foot-note **"never triggers an analysis."**
3. **Mark all read** → `markAllNotifRead()` → badges update; **nothing else changes**.
4. Click an item → `notifGo(i)` marks it read, closes the panel, ensures the shell is visible, and **routes to its source** (artifact / Issues / History / Overview / Workspace Home).
5. Escape closes the panel.

## Flow D — New project at the Free cap (D048)
1. Any **New project** action at the cap → `openUpgrade()` shows the prompt.
2. **Upgrade your plan** → Settings → Subscription (visibility-only).
3. **Archive DevNorth 2026 to free the slot** → `archiveAndCreate()` → non-destructive confirming toast.
4. **Not now** / Escape dismisses.

## Flow E — Settings (D105)
1. Sidebar **Your account** → account menu → **Settings** (or Workspace-Home avatar) → `openSettings()` shows the surface at **Account**.
2. Use the **left section nav** (mouse or keyboard) → `setNav(sec)` highlights the section and scrolls to it.
3. Review the **visibility-first** areas (Subscription/Billing/Integrations/Membership) — facts + upgrade paths, no enforcement.
4. **Back to app** / Escape closes.

## Flow F — Appearance / theme (D106)
1. Settings → **Appearance**.
2. Toggle **Dark ↔ Light** → `setTheme('light'|'dark')` flips `data-theme` on `<html>`, applies instantly, persists to `localStorage`, and syncs the toggle state.
3. **Match system** → `matchSystemTheme()` clears the override → follows `prefers-color-scheme`.
4. Reload → `initTheme()` restores the persisted (or system) theme before paint.

## Preserved flows (Slices 1–7)
Invite → activation → intake → Initial Analysis → orientation; Overview ↔ Attention ↔ Issues ↔ History via the sidebar; artifact editing in the workspace; command palette (⌘/Ctrl+K); OSLO chat; feature tour. Unchanged.

# Slice 8 — Multi-Project Workspace & Awareness · E2E Test Scenarios

Cumulative Slices 1–8. Manual/automatable scenarios against the single `prototype.html`. (≤20.)

1. **Logo → Workspace Home.** Click the top-left Intralign logo → Workspace Home overlay appears in the "Workspace" context. Expect Pinned + Recent + Archived sections.
2. **Logo keyboard.** Tab to the logo, press Enter → Workspace Home opens. Escape → it closes.
3. **Workspace card fields.** Each Pinned/Recent card shows name, ownership tag, analysis status, "Understanding {band} · qualified by {reliability} reliability" (neutral dot), recency, open-issues count.
4. **Stale status.** Q3 Platform Migration shows a neutral **⋯ Analysis stale** chip (not a severity color).
5. **No-scores note.** Workspace Home shows the **"No computed scores across projects"** honesty note.
6. **Archived + Restore.** The Archived (1) section lists 2025 Leadership Offsite with a **Restore** button → clicking it shows a non-destructive toast.
7. **1-active-project note.** The footer note states 1 active project (Free plan) and that archiving is non-destructive.
8. **Enter real project.** Click the DevNorth 2026 card → overlay hides, project shell shows at Overview.
9. **Enter illustrative project.** Click Brand Refresh 2026 → an honest toast ("demo focuses on DevNorth"); no broken state.
10. **Switcher opens.** Click "DevNorth 2026 ▾" → dropdown lists the projects, **New project**, and **Workspace Home**. Escape / outside click closes it.
11. **Switcher → Workspace Home.** Pick ⊞ Workspace Home in the dropdown → Workspace Home opens.
12. **New project at cap.** Click **+ New project** (Workspace Home or switcher) → the upgrade-or-archive prompt appears with both options + Not now.
13. **Archive-to-create.** In the prompt, click **Archive DevNorth 2026 to free the slot** → non-destructive confirming toast; prompt closes.
14. **Notifications open.** Click the top-bar bell → the awareness panel slides in; the unread badge reads 3.
15. **Notification categories.** The panel shows mention, reply, shared-with-me, analysis complete, analysis failed, stale, and the note **"never triggers an analysis."**
16. **Mark all read (presentation-only).** Click **Mark all read** → badge → 0/hidden; no view or assessment changes.
17. **Route to source.** Click the mention item → panel closes, shell shows, its **artifact** opens. Click the shared-with-me item → **Workspace Home** opens. Badge decrements as items are opened.
18. **Settings opens with 11 sections.** Account menu → Settings (or Workspace-Home avatar) → the Settings surface shows Account · Profile · Appearance · Notifications · Workspace · Project defaults · Collaboration · Membership · Subscription · Billing · Integrations. Section nav (keyboard) jumps to a section. Subscription/Billing/Integrations/Membership show facts + upgrade paths only (no enforcement).
19. **Appearance theme flip + persist.** Settings → Appearance → toggle **Light** → `data-theme="light"` on `<html>`, app repaints in light mode with no color regression; reload → light persists. Toggle **Dark** → attribute removed. **Match system** follows the OS scheme.
20. **Non-regression.** Command palette (⌘/Ctrl+K), Overview/Attention/Issues/History views, the artifact editor, OSLO chat and the feature tour all still work; console shows 0 errors.

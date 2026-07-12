# Slice 8 — Multi-Project Workspace & Awareness · Success Criteria

Cumulative Slices 1–8. A criterion passes only if it holds in the single openable `prototype.html`.

## D102 — Workspace Home
- [ ] The Intralign/OSLO logo (top-left) opens a global **Workspace Home** in a distinct "Workspace" context (not a project view).
- [ ] Workspace Home shows **Pinned** and **Recent** project cards, each with name · ownership · analysis status (incl. **stale**) · a **reliability-qualified understanding indicator** (band + "qualified by … reliability", neutral) · recency · open-issues count.
- [ ] An **Archived projects** section exists with a non-destructive **Restore** affordance.
- [ ] A **"no computed scores across projects"** honesty note is present.
- [ ] **New project** at the Free cap opens the honest **upgrade-or-archive** prompt.
- [ ] A **"1 active project"** note is present; illustrative projects convey the structure.

## D103 — Project switcher
- [ ] The top-bar "DevNorth 2026 ▾" chip opens a real dropdown (replaces the seam).
- [ ] The dropdown lists the **projects**, **Workspace Home**, and **New project** (at cap → prompt).
- [ ] Keyboard-operable; closes on Escape / outside click.

## D104 — Notifications / awareness
- [ ] A top-bar **bell** with an **unread badge** opens an awareness panel.
- [ ] R1 categories present: **mention · reply · shared-with-me · analysis complete · analysis failed · stale**.
- [ ] read/unread is **presentation-only** (marking read changes nothing real).
- [ ] Each item **routes to its source** (artifact / Issues / History / Overview / Workspace Home).
- [ ] The persistent note **"never triggers an analysis"** is shown; no "reanalysis" mechanism is surfaced (D092).
- [ ] The unread badge is **neutral/brand**, not a severity color (D003).

## D105 — Settings (visibility-first)
- [ ] The Settings seam (account menu + sidebar) opens a real Settings surface.
- [ ] All **ten** areas present: Account · Profile · Workspace · Project defaults · Collaboration · Notifications · Subscription · Billing · Integrations · Membership (plus **Appearance**).
- [ ] Subscription/Billing/Integrations/Membership are **visibility-first** — facts + upgrade paths, **no enforcement, no real billing**.
- [ ] Section nav is **keyboard-accessible**.

## D106 — Appearance
- [ ] Settings → **Appearance** has a **Dark/Light** toggle; **dark is default**.
- [ ] The toggle flips a single **`data-theme`** attribute on `document.documentElement` and **persists to localStorage**.
- [ ] **Match system** follows `prefers-color-scheme`.
- [ ] Reduced-motion is honored; focus rings visible.
- [ ] The app is **usable in light mode** — no severity-color / neutral-ramp regression.

## Boundaries
- [ ] Advisory-only; "Issues" not Findings; visibility-first tiering (illustrative numbers, no enforcement); Alpha invite-only frame.
- [ ] Neutral chrome; severity color confined to issues.
- [ ] Sharing/collaboration/export remain clearly-labeled **Slice-9 seams** (not built here).

## Non-regression (Slices 1–7)
- [ ] Onboarding funnel, Overview, Attention map, full artifact editor, Issues, History + trend all intact.
- [ ] Persistent sidebar + top bar + command palette (⌘/Ctrl+K) + OSLO chat + feature tour all intact.

## Build integrity
- [ ] Extracted `<script>` passes `node --check`.
- [ ] jsdom structural parse: `body.children.length > 0`; Workspace Home, switcher, notifications, settings elements present.
- [ ] jsdom runtime: all Slice-8 behaviors succeed with **0 non-environment errors**; prior slices intact.

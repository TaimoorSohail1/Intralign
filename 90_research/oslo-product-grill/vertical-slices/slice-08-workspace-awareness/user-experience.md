# Slice 8 — Multi-Project Workspace & Awareness · User Experience

**Cumulative:** Slice 1 + Slice 2 + Slice 3 + Slice 4 + Slice 5 + Slice 6 + Slice 7 + **Slice 8**. This slice fills the four remaining top-bar / sidebar **seams** that Slices 3–7 deliberately left as clearly-labeled stubs — the project **switcher**, the **Workspace Home** logo, **Settings**, and **Notifications** — and adds the **Appearance (dark/light)** theme control. Everything from Slices 1–7 is preserved 1:1 (onboarding funnel, Overview, Attention map, full artifact editor, Issues, History + trend, persistent left sidebar + top bar + command palette, OSLO chat, feature tour).

Decisions encoded: **D102** (Workspace Home / dashboard), **D103** (project switcher), **D104** (notifications / awareness), **D105** (Settings, visibility-first), **D106** (Appearance — theme + a11y) — plus inherited **D001** advisory-only, **D002** confidence = neutral maturity, **D003** severity-only color, **D006** analysis-update-only assessment, **D015** dark default + WCAG 2.1 AA, **D017** "Issues" (not Findings), **D021** Alpha invite-only frame, **D048** upgrade-or-archive at the Free cap, **D049** "Plan artifacts", **D092** no user-facing "reanalysis" mechanism.

---

## What's NEW in Slice 8 (which seams are filled)

### 1. The Intralign/OSLO logo now opens Workspace Home (D102) — was: `title="Workspace Home"` only
Clicking the **top-left Intralign logo** (or pressing Enter/Space on it) opens a **global Workspace Home** — a full-viewport surface in the **"Workspace" context**, visibly distinct from the project shell (its own top bar reads *Intralign · Workspace*). It shows:

- **★ Pinned** and **Recent** project cards. Each card carries: **name**, an **ownership** tag (*Owned* / *Shared with me*), **analysis status** (*Analyzed* or a neutral **⋯ Analysis stale** chip), a **reliability-qualified understanding indicator** (a neutral maturity dot + *"Understanding **{band}** · qualified by {reliability} reliability"*), **recency**, and an **open-issues count** (+ artifact count).
- A **"New project"** card and a header **+ New project** button.
- A **No computed scores across projects** honesty note — OSLO assesses each project on its own inputs and reliability; there is no portfolio score, average, or ranking.
- An **Archived projects (N)** section — non-destructive, each with a **Restore** affordance (history, issues and the last assessment return intact).
- A footer note: **1 active project** on the Free plan (DevNorth 2026); recent cards illustrate the multi-project structure; archiving is non-destructive.

Opening a card: **DevNorth 2026** (the one real project) enters the project shell at Overview; the illustrative cards show an honest toast ("the demo focuses on DevNorth 2026; this card illustrates the multi-project structure"). **New project** → the Free-cap prompt (below).

### 2. The top-bar project switcher is real (D103) — was: `openProjectSwitcher()` → "arrives in Slice 8" toast
The **"DevNorth 2026 ▾"** chip now opens a real dropdown anchored below it: the **project list** (each with a neutral maturity dot + a *stale* chip where applicable), a divider, then **+ New project** and **⊞ Workspace Home**. Switching is illustrative (single real project); **New project** at the cap → the prompt. The dropdown is keyboard-operable and closes on Escape or an outside click.

### 3. A notifications / awareness panel (D104) — was: absent
A **bell (◔) with an unread badge** now sits in the top-bar right cluster (and in the Workspace Home top bar). Clicking it slides in a right-hand **awareness panel**. R1 categories: **mention · reply · shared-with-me · analysis complete · analysis failed · stale**. Each item shows a label, a source line, a timestamp and a category chip. Behavior is deliberately honest:

- **read/unread is presentation-only** — *Mark all read* and opening an item change the badge, and **nothing else**; no assessment moves.
- **Each item routes to its source** — a mention → its **artifact**; a reply → the **Issues** surface; analysis complete/stale → **History**; analysis failed → **Overview**; shared-with-me → **Workspace Home**.
- A persistent foot-note: **"Awareness is presentation-only — it never triggers an analysis, and marking items read changes nothing."** (No "reanalysis" mechanism is surfaced — D092.)
- The unread badge is a **neutral/brand** dot, not a severity color (D003).

### 4. A real Settings surface (D105) — was: `openSettings()` → "coming in a later slice" toast
The **account menu → Settings** and the sidebar **Your account · Settings** row now open a full-viewport **Settings** surface with a **keyboard-accessible left section nav** and eleven sections: **Account · Profile · Appearance · Notifications · Workspace · Project defaults · Collaboration · Membership · Subscription · Billing · Integrations**. The four tier/commercial areas are **visibility-first** (tagged *visibility* / *view-only*): they show **facts** (plan = Free, active projects = 1 of 1, analysis = Initial only, no payment method, no connected tools, Owner membership) and **upgrade paths** — with **no enforcement and no real billing**. Section nav highlights the active area and scrolls to it; Escape or *Back to app* closes.

### 5. Appearance — dark/light theme toggle (D106) — new control
**Settings → Appearance** has a **Dark / Light** segmented toggle (**dark is the default**). It flips a **single `data-theme` attribute** on `document.documentElement` (the light token overrides already exist in the theme), applies instantly, and **persists to localStorage**. A **Match system** action clears the override and follows the OS `prefers-color-scheme`. The section also states that **reduced motion is honored** (following the OS setting) and that **focus indicators are always visible** — both already implemented in the theme. The app remains fully usable in light mode; the neutral maturity ramp and severity colors both have light-mode token values, so there is no color regression.

---

## INHERITED (unchanged from Slices 1–7)

- **Onboarding funnel** — invite → activation → intake composer → Initial Analysis interstitial → orientation overlay (Slices 1–2).
- **Overview** — confidence-led understanding console: the confidence pill + popover (CAF dimensions, independent reliability basis, neutral false-confidence flag, stages), Start-here, Progress, More (Slice 3).
- **Attention map** — the co-primary heatmap of artifacts × dimensions, neutral intensity ramp (Slice 4).
- **Artifact workspace** — the full Notion-like rich-text editor, tables with row/column ops, provenance gutter, inline weakness annotations, find/replace, slash menu, link popover (Slice 5, folded-in batches A–C).
- **Issues** — the all-issues surface, full issue panel, lifecycle Open → Addressed → Resolved, recommendations + Apply-this-fix, clarification loop, empty states (Slice 6).
- **History & trend** — the append-only, run-grouped timeline + "Understanding over runs" trend, read-only + last-good honesty (Slice 7).
- **Shell** — the persistent left sidebar (Project views + Plan-artifacts subgroups), the top bar (breadcrumb, confidence pill), the **command palette** (⌘/Ctrl+K), the persistent **OSLO chat rail**, the **feature tour**, the phase preview scaffolding, and the account menu.

All of the above are byte-for-byte the Slice-7 behavior; Slice 8 only **adds** overlays/panels and **rewires** the four seam handlers plus the appearance toggle.

---

## Boundaries honored
- **Advisory-only**; "Issues" not Findings; **visibility-first** tiering (no enforcement, illustrative numbers); **Alpha invite-only** frame (D021).
- **No "reanalysis" mechanism** surfaced (D092) — awareness explicitly "never triggers an analysis".
- **Neutral chrome**; severity color stays confined to issues; the workspace understanding dots and the unread badge use the neutral/brand palette.
- **WCAG 2.1 AA** — the switcher, notifications, settings section nav and the appearance toggle are all keyboard-operable with visible focus rings; Escape closes each surface.
- **Deferred to Slice 9** — real sharing/collaboration internals, invites/roles enforcement, and export. The top-bar Share/Export icons still point to their clearly-labeled Slice-9 seams.

---

# Revision 2 — D107 gap-analysis refinements

Slice 8 shipped a Settings surface where a lot of rows *looked* clickable and did nothing, an awareness panel that showed collaboration events a single invite-only user cannot have, and a dashboard built to scan many projects for a plan that allows one. Revision 2 makes the surface tell the truth. All Slice 1–8 behavior is preserved.

## 1. Nothing in Settings pretends to work
Every row is now one of three things — a control that does something, a clearly-labelled thing that arrives later, or plain text. The clickable-looking dead ends (*Password & security → Manage*, *Avatar → Upload*, *Delete account → "Confirmation-gated"*, *Invite preferences → Manage*, *Billing → Manage*) are gone.

**What actually works now:**
- **Profile** — type your **display name** (and an optional **role/title**). It saves as you type and updates everywhere you appear: the sidebar account row, the account menu, your avatar initials, the Membership list.
- **Workspace** — rename your **workspace**. It updates in the top bar, on Workspace Home and in Settings.
- **Notifications** — a **switch per category**. These are genuinely live, and safely so: awareness is presentation-only, so a switch changes only *what the panel shows you*. It never starts, changes, or re-runs an analysis. The honest note stays: *"Awareness is presentation-only — it never triggers an analysis."*
- **Account** — **Sign out** and **Stay signed in** now live here (as well as in the account menu; one shared state). Email stays read-only fact.
- **Appearance** — the Dark/Light toggle and **Match system**, as before.
- **Delete account** — a **real confirmation dialog**. It explains what deletion would mean and then says plainly that nothing is deleted in this prototype. The internal phrase *"Confirmation-gated"* is gone; no spec language is shown to a user anywhere.

**What is honestly labelled instead of faked:**
- **Subscription** — plan, active projects, what's included, and **See plans**. No enforcement.
- **Billing** — *"Billing is handled outside the app in Alpha — the Intralign team sets your plan up with you directly. No card is stored here."*
- **Collaboration** — a plainly labelled **Slice 9** seam: *"Every project is private to you today. Sharing, invites and collaborator roles are the next thing we build — nothing on this page does anything with them yet."*
- **Membership / Integrations** — *"Arrives with Collaboration"* / *"Arrives after this release"*.

## 2. Collaboration notifications are gated, not faked
Alpha is **invite-only and single-user**, and sharing itself is Slice 9 — so nobody can mention you, reply to you, or share a project with you. **Mentions · Replies · Shared-with-me are therefore switched off and hidden from the panel**, and appear in Settings as disabled switches tagged *"Arrives with Collaboration"*, with a note explaining why. The panel keeps the three categories that can actually happen — **analysis complete · analysis failed · your plan has moved on past its last read** — and all of them now reference the one real project.

## 3. The dashboard matches the 1-project reality
The Free plan includes **one active project**, so Workspace Home no longer presents an empty Pinned/Recent grid built for scanning many. At one project it collapses into a single **"Your project"** section with the **full-detail card** (understanding, reliability, open issues, artifacts) alongside **New project**, plus **Archived** and the unchanged **"no computed scores across projects"** note. A line explains that **Pinned and Recent appear as soon as you have more than one project** — and they do: the grid returns automatically. Archiving is real and non-destructive; restoring brings the project back intact.

## 4. Light mode is now audited
Light mode worked but had never been checked for contrast. Small grey text, the orange used for links and active nav, the amber used for moderate issues, and the low end of the understanding ramp all fell below AA. They were darkened; the **understanding ramp stays purely neutral grey** (never a health color) and **severity keeps its hue**, so issues remain visually distinct from the maturity ramp. Every text and non-text combination in light now clears WCAG 2.1 AA.

## 5. Polish
- A **stale project** card now carries its next step: *"→ Open to bring the read up to date."*
- **Settings search** filters the eleven sections (and their nav entries) as you type.
- **Empty states**: *"You're all caught up"* in notifications; a *"No active projects"* state on Workspace Home with restore + start-something-new.
- Plain language throughout Settings and Workspace — no internal or spec phrasing.

**Still not built:** Slice 9 (collaboration, sharing, export) internals. Everything that touches them is a labelled seam, not a control.

---

# Revision 3 — D108 · OSLO can actually be asked

Until now the OSLO rail was a **noticeboard**: it announced when analysis finished and nothing else. The box you typed into did nothing, and **Send did nothing at all**. Nothing on any screen handed OSLO a subject to talk about. D108 turns the rail into the advisor the product has always claimed it is — and threads it through the work rather than parking it beside it.

## 1. You can ask, and OSLO answers from your plan
Type a question and press **Send** — or just **Enter** (Shift+Enter for a new line). OSLO replies from the read that is on your screen right now: your confidence number and band, the reliability behind it, **the dimension that is holding the number back**, how many issues are open, which one it would take first, and which artifact you have open. Nothing is invented. If the read changes, the next answer changes with it.

Ask *"What should I do next?"* and it points at the most consequential open issue and explains why. Ask *"Why is Feasibility Very Low?"* and it names the limit and what would move it. Ask *"Explain the top issue"* and you get the stakes, what it weakens, and the options.

**And it stays advisory.** Ask OSLO to just fix it and it says plainly what it is: *"I can't change your plan — I read and explain, you decide."* It never edits an artifact, never selects a path, never closes an issue. Issues reach **Resolved** only when an analysis update confirms they no longer hold. What OSLO *can* do is hand you the action — *Open this issue →*, *Apply this fix →*, *Open the Attention map →* — as a link **you** click, which runs the very same control you'd have used on the surface.

## 2. Every surface can hand OSLO the subject — and you can see what it's holding
From an **issue**, a **resolution path**, a **plan artifact**, a **weak sentence** in the editor, your **confidence score**, or an **Attention-map cell**, you can now ask OSLO about *that thing*. The rail opens, a **context pill** appears at the top of the conversation — *"Context · Venue Wi-Fi capacity is unconfirmed (ISS-01)"* — and OSLO opens with a grounded read of it. Everything you ask next is answered inside that context, until you clear it with the **×**. No guessing about what OSLO thinks you're talking about.

Where you'll find it: **✦ Ask OSLO about this issue** in the issue panel · **✦** in the artifact toolbar · **Ask about this** on the hover popover of any flagged sentence · **✦ Ask OSLO why** beside the confidence number · **Ask OSLO about this cell** at the head of a list scoped from the Attention map.

## 3. Discuss — the missing recommendation action
Recommendations offered *Apply this fix* and *Select* — decisions — with no way to **think out loud first**. **Discuss** is now on the OSLO Recommended block and on every resolution path. It opens the conversation about that path: what it buys you, how it weighs against the alternatives, and what it costs. **Discussing a path does not select it.** Selecting stays a deliberate act you take in the issue — the conversation just makes it an informed one.

## 4. You can answer OSLO's questions in the conversation
When OSLO needs something confirmed, it can now **ask you in the chat**, with the answer box right there in the thread (the issue panel also offers *"Answer in chat →"*). Answering there does exactly what answering in the panel does — your project information updates, the issue moves to **Addressed**, the analysis update moves it to **Resolved**, and **the same entry lands on your timeline**. The conversation is a front door to the same governed path, not a back door around it.

## 5. Smaller things that make it usable
**Suggested prompts** sit above the box and change with your plan — *"Why is Feasibility Very Low?"* only appears because Feasibility *is* your limit. A **first-run state** says what OSLO is for and what it will not do. Answers **link you to the thing they're describing** instead of leaving you to find it. The conversation is a live region for screen readers, everything is keyboard-operable, and the rail carries **no severity color** — severity stays a word, not decoration.

**Unchanged:** every completion notice, the tour, and every prior slice.

---

# Revision 4 — D109 · OSLO talks like OSLO

D108 made the chat answer. It answered **confidently** — and that was the problem. OSLO's whole promise is that it tells you *how much to trust what it just said*; the rail was the one surface in the product that didn't. Revision 4 makes the conversation inherit the epistemics that the Overview, the artifacts and the Attention map already carry — and turns it from a text box into something you can actually work in.

## 1. Every answer tells you how much to trust it
Ask OSLO anything about your plan and the reply now ends with its **reliability**, taken from the same read the Overview shows: *"Reliability is **Moderate** — this rests on the documents you gave me, so treat it as directional. Basis: Coverage Moderate · Evidence Moderate · How assessable Moderate."* When reliability is **Low**, the wording changes — *"the evidence behind it is thin; treat this as a hypothesis to test, not a finding"* — and the block is flagged. If a **High** band is sitting on **Low** reliability, OSLO says so out loud, in the chat, the way it does everywhere else.

## 2. It tells you where a fact came from — and admits when it guessed
Every plan fact is labelled: **From OSLO** (I derived this) or **Confirmed by you** (you told me this). Ask about Resources and you get *"Resources: From OSLO"*, because you haven't confirmed it. Confirm it — answer the clarification, apply the fix, edit the artifact — and the same question afterwards says **Confirmed by you**, and OSLO changes what it claims accordingly.

And where the ground is thin, it stops short instead of sounding certain: **"I inferred this — it isn't confirmed in your inputs."** That line appears *instead of* a confident answer, not as a footnote to one.

## 3. It shows its sources
Under each reply sits **What this rests on** — small, neutral chips carrying the actual source line: *"Resources · Vendors — 'Venue — rooms, power, Wi-Fi (must confirm 500-person Wi-Fi capacity)'"*. Click one and you land on the artifact, the issue, the read, or the History run it came from. The chat never becomes the place the work happens: it hands you back to the surface that owns the thing.

## 4. When it doesn't know, it says so
Ask OSLO something off-script and it will not improvise a plausible-sounding summary at you. It says: *"I don't have a grounded answer to that — so I'm not going to invent one,"* and then lists what it can genuinely do (explain your read · compare resolution paths · explain an issue or artifact · tell you what changed), each as a chip that works. Ask it to draft an email or call the venue and it draws the boundary: *"That's outside what I do."* Ask it to just fix it, and it repeats the one rule that never bends — **an issue is Resolved only when an analysis update confirms it no longer holds.**

## 5. It thinks before it answers
A brief **"OSLO is reading your plan…"** appears, then the reply streams in. It's a small thing, and it does one honest job: it shows you that the answer is being read *out of your plan*, not retrieved from a drawer. If you've asked for reduced motion, it simply appears.

## 6. You can keep what's useful
Every reply now carries **Copy**, **Retry** (re-answer from the read as it stands now), **👍/👎**, and **Save to History** — which puts the insight on your timeline as a note, append-only, alongside everything else that happened to this project. It records what was said. It changes no assessment, closes nothing, and moves no number.

## 7. Follow-ups, and more than one thing at a time
After an answer, OSLO offers two or three **next questions drawn from that answer** — after an issue: *"Compare the resolution paths" · "What evidence supports this?" · "What would move Feasibility?"*. And you can now hold **several things in view at once**: type **@** to pin an issue, a plan artifact, or Clarity/Alignment/Feasibility. Each pinned thing shows as a removable pill, and the answers visibly read all of them ("Also in view…"). **Esc** clears them.

## 8. Room to think, and actions that tell you what they'll do
A control **expands the rail** into a wider column for longer reasoning — and remembers that you like it that way. And every action link in a reply now states its consequence before you take it: *"Apply this fix → Drafts the change into Resources; the issue moves to Addressed and your read updates after the analysis run."* You still click it. OSLO still doesn't.

## 9. It remembers the conversation
Reload, navigate away, come back — **the thread is still there**, per project. Answers keep their citations, their reliability, their saved-to-History marks. Nothing is re-generated behind your back: what you read yesterday is what you read today.

## Smaller things
The empty state now **teaches** — three example questions, one click each. ⌘/Ctrl+Shift+K focuses the chat; ⌘/Ctrl+Enter sends; Esc clears the context. (⌘/Ctrl+K stays the command palette.) Replies **lead with the point** and then explain it. And the advisory boundary — *OSLO reads and explains; you stay in control* — now lives in **one** place, on the composer, with the full rule on hover, instead of being recited at you in every single reply.

**Unchanged:** every completion notice, the tour, the clarification path (still the same update, same lifecycle, same timeline entry as the Issue panel), and every prior slice.

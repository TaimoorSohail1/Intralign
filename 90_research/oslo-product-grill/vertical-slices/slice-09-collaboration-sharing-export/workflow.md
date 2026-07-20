# Slice 9 — Collaboration, Sharing & Export · Workflow

Cumulative (Slices 1–9). Actor workflows on the collaboration/sharing/export layer + the Reports workspace of the frozen build. Actors: **User** (PM/Owner) · **Collaborator/Viewer** · **System** (client-side prototype render/state) · **AI** (simulated OSLO — timers + fixed illustrative data; no real model, no network, no email).

> Regenerated to match the frozen build. Every flow here **packages, never produces**: sharing, commenting, exporting and generating/scheduling a report **run no analysis and write no assessment** — only an analysis update moves the read (D111/D112/D088).

## Preserved end-to-end journey (INHERITED)

Invite → Activate → Intake → Fast Pass ≈30s → read-led Overview → Outcome Analysis (auto, non-blocking, provisional→current) → clarification loop → **History** (append-only) records every event. Slice 9 adds the people, the conversation, the hand-off, and the Reports workspace around that spine.

## Flow A — Share the project (invite + view-only link)

1. **User** opens the top-bar Share (`⤴`) → `openShare()` renders the dialog: the two limits (phase · tier, separate), the invite row, the roles, the people list, and the share-link box.
2. **User** enters an email, picks **Collaborator** or **Viewer**, presses Invite (`sendInvite`). **System** records the membership (pending), or — if blocked — names **which** limit blocked it (`admissionBlockHTML`: phase → waitlist, no upgrade CTA; tier → real upgrade path + "add them as a Viewer"). A **Viewer is never blocked** (X-1).
3. **User** clicks **"Create a view-only link"** → `createSnapshotLink()` mints a snapshot link. **System** shows Copy / Preview what they see / Revoke, plus its 30-day revocable lifetime.
4. **User** copies the link. **Collaborator/Viewer** opening it sees the read **as it stood**; if the read has since moved, **System** labels it **"previous analysis."** The link **never re-runs an analysis.**
5. **User** may **Revoke** at any time → **System** appends a History `share` event; anyone opening it now sees a revoked notice. **Nothing about the assessment changed.**

## Flow B — Comment on a finding, @mention a teammate

1. **User** (or **Collaborator**) opens an issue → the **Comments** row.
2. **User** types a comment, presses `@` → **System** opens the mention menu over teammates + members; **User** picks one → an `@Name` pill is inserted. Picking **"Invite someone new…"** routes to the share dialog.
3. **User** posts (`⌘↵` or the Comment button) → `addComment()` appends the comment (a **Reply** threads under the last one). **System** writes an **append-only History `comment` event** naming any mentions.
4. **The assessment is untouched** — the honest label "Comments never change the assessment" sits at the compose box; the append-only contract is the row's ⓘ. **There is no edit or delete** (D111).

## Flow C — Export / share-out a snapshot

1. **User** opens Export (top bar, or a report's Export control) → `openExportSeam()` → `openExport()`.
2. **System** renders the **currency marker** (band + reliability + run + when + open issues — off live state), the **verbatim disclaimer** (understanding maturity, not health/readiness/probability), and the formats.
3. **User** picks **PDF** (Free) → `doExport('pdf')` appends a History `export` record ("generates no new assessment; never triggers an analysis") and toasts the simulated export.
4. **User** picks **Copy summary** or **Export link** on Free → the button is live, but `doExport()` gates the **attempt** → `fireUP('UP-EXPORT')` shows the value-framed Basic prompt (naming the exact format and tier). Never a disabled control, never silence (D138).
5. At any point **System** assembles the **Strategic Readout Composer** preview (five-section spine); switching the **audience** re-tailors **§4 (the ask) only** (DL-108). Assembling it **runs no analysis** (packages, never produces).

## Flow D — The Reports workspace (Executive Briefing + three generated reports)

1. **User** opens **Reports** → `enterReports()` draws the tab strip (`renderReportTabs`) — Authored **Executive Briefing** + Generated **Outcome Readiness · Assumptions & Evidence · Decision Record** — and shows the last-selected report.
2. **User** clicks a **Generated** tab → `switchReport(k)` hides the composer, shows `#rptGenPage`, calls the type's renderer. **System** **computes the report live** from state (`currentRead`/`_cafOf`/`_ciLoadBearingStatements`/`_decision`…) — no forecast, no composite, maturity not health.
3. **User** reads **Outcome Readiness** — band + ramp + drivers + reliability trust-check + grounding + the one next move. Single depth by design.
4. **User** switches to **Assumptions & Evidence** and flips it to **Full** (`setReportDepth('assumptions','full')`) → **System** re-renders with the complete inferred register + what breaks per assumption, and **persists** the depth (`repDepth`). Re-entering later restores Full.
5. **User** opens **Decision Record** → **System** lists each owner decision, what it firmed, and a **D088 status**: **"Live in the read"** (an analysis run is newer than the decision) or **"Awaiting the next analysis update."** No decision claims to have moved the read itself.

## Flow E — Export any generated report (one modal)

1. On any generated report, **User** clicks **Export** (`_genControlsHTML` → `openExportSeam()`).
2. **System** opens the **same** export modal (currency marker · disclaimer · tier gating · append-only record) — **no parallel machinery** (DL-144).
3. **"Send"** (a view-only share link — a share of the *live* project) stays a **distinct object** from a frozen export (D107).

## Flow F — Report vs memo (what travels is frozen)

1. **User** edits the **Executive Briefing** (a living **report**, tracks the read; editing is free on every tier — the gate is REUSE, D154).
2. **User** cuts/sends a **memo** → **System** deep-freezes it (`_deepFreeze`); it is **immutable** thereafter.
3. When the read later moves, **System** relabels the memo **"previous analysis"** (never rewrites it). Cutting it ran **no analysis** (D168/D171).

## Flow G — Hand off to Asana (crosses into Slice 11)

1. For an execution hand-off, **User** crosses into the **structured Asana export** — mapping preview → simulated hand-off; only the plan crosses.
2. This is **Slice 11's distinct object** (DL-151), not Slice 9's reader-export (D107). See `slice-11-execution-ready-planning-export`.

## Simulated-AI boundary

No analysis runs in any Slice 9 flow. Sharing, commenting, exporting, and generating/scheduling a report are **read-packaging** operations over existing state (`_assertReadoutRunsNoAnalysis` / `_assertReportPackagesNeverProduces`). The read moves **only at an analysis update** (D088); every package that outlives its run is relabelled **"previous analysis"** — never a stale read passed off as current.

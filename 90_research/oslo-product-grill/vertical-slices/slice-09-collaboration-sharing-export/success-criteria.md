# Slice 9 — Collaboration, Sharing & Export · Success Criteria

The developer's checklist for the collaboration/sharing/export layer + the Reports workspace of the frozen build (md5 `a327d702`, boot 157/157). **FREEZE-INTACT:** these assert the build as frozen — not new enhancements. Guard/doctrine refs in parentheses.

## Cumulative-integrity (no regression)
- [ ] SC-0 Every Slice 1–8 route, screen, interaction, theme token, and localStorage key still works (activation funnel, intake, Fast Pass, read-led Overview, Issues, Inference map, **History append-only timeline**, chat + completion notices, tour, clarification loop, analysis-state machine).
- [ ] SC-0b The build boots green (157/157 guards) with no console error.

## Sharing dialog (D110)
- [ ] SC-1 Share opens a dialog (`openShare`/`#shareScrim`) to **invite by email** as **Collaborator** or **Viewer** (Owner is never invitable) and to hand out a **view-only snapshot link**. Roles are **shown, not enforced** this release.
- [ ] SC-2 Roles + seats: Owner/Collaborator take a **tier seat**; **Viewer takes no seat and is unlimited on every tier** — the seat cap can never block a Viewer (`PARTICIPANT_TYPES` / `_roleTakesSeat` / `_assertViewersUnlimited`, X-1).
- [ ] SC-3 The **two limits are shown separately and never merged** into one "you've hit your limit — upgrade" sentence: a **phase** limit (invites/supply, no upgrade CTA, offers the waitlist) and a **tier** limit (seats/depth, real upgrade path + the free "add as Viewer" remedy) (D124 / `admissionBlockHTML`). "Asking for a read is free — no invite, no seat" survives (CR-2).
- [ ] SC-4 The share link is a **view-only snapshot of the LIVE project** — it **never re-runs an analysis**, is **relabelled "previous analysis"** when the read moves on, and offers **Copy / Preview what they see / Revoke** (`createSnapshotLink` / `_linkStale` / `revokeLink`).
- [ ] SC-5 Link lifetime is **30 days, revocable, the same on every plan** — safety is never sold (`SHARE_LINK_EXPIRY_DAYS`, CR-6; `CONFIGURABLE_EXPIRY_BASIC = false`, D128 P2).
- [ ] SC-6 The dialog states **"A share link is not an export link"** (revocable live-project access vs a frozen snapshot copy) and the footer states **"Sharing changes no assessment. Only an analysis update does."** (D107/D111).

## Threaded comments + @mentions on findings (D111/D114/D162a)
- [ ] SC-7 An issue (finding) carries a **comments thread** (`_commentsHTML`); comments are **append-only** — there is **no edit and no delete** (`addComment` only; no `editComment`/`deleteComment`, D111).
- [ ] SC-8 A **Reply** threads under its parent; **@mentions** open a menu over teammates + members, insert an `@Name` pill, and offer **"Invite someone new…"** that routes to the share dialog (`cmInput`/`cmPickMention`).
- [ ] SC-9 The honesty label **"Comments never change the assessment"** shows **once, short** at the compose box; the append-only contract is the row ⓘ, not a standing lecture (`COMMENT_HONESTY`, D162a). Posting appends an **append-only History `comment` event** (D096) and changes **no assessment**.

## Export / share-out — the one ratified modal (D112)
- [ ] SC-10 There is **one export surface** (`openExportSeam` → `openExport`/`#exportScrim`) carrying the **analysis-currency marker** (band + reliability + run + when + open issues, **read off live state**, D112/D153/D173) and the **verbatim required disclaimer** — "understanding maturity … **not** health, readiness, or probability of success" (`EXPORT_DISCLAIMER`, D003/DL-104).
- [ ] SC-11 **Free = PDF only**; Copy summary and Export link are **shown + labelled Basic, never hidden** (D048), and their buttons **stay enabled** — the **attempt** is gated (`doExport` → `fireUP('UP-EXPORT')`), never the control (D138/D123).
- [ ] SC-12 An export **produces no assessment and triggers no analysis**; `doExport` appends an **append-only export record** to History saying exactly that (D112). An **export link is not a share link** (D107) — an export is a **frozen** object; the tier note restates it.
- [ ] SC-13 The export preview assembles the **five-section Strategic Readout** (§1 read · §2 limiting · §3 unknowns · §4 ask · §5 what I'd need to be sure · §6 how to read this) live from state; the audience selector tailors **§4 (the ask) only** — §1–§3/§5/§6 are identical across audiences (`_assertReadIdenticalAcrossAudience`, DL-108) — and assembling it **runs no analysis** (`_assertReadoutRunsNoAnalysis`, DL-107).

## Reports workspace (DL-141→144)
- [ ] SC-14 Reports is a **slim tab strip hosting more than one report** (`renderReportTabs`/`REPORT_TYPES`): the **authored Executive Briefing** + three **generated, read-only** reports — **Outcome Readiness** (DL-141), **Assumptions & Evidence** (DL-142), **Decision Record** (DL-143). Each tab shows an "Authored"/"Generated" kind chip.
- [ ] SC-15 Every generated report is **computed live** from state (`renderOutcomeReadiness`/`renderAssumptionsEvidence`/`renderDecisionRecord`) — **nothing authored** (D173), **no forecast/composite** (D183b), **maturity not health / never a RAG rating** (D003, P1 class per DL-104).
- [ ] SC-16 **Outcome Readiness** shows the band + maturity ramp + drivers + a reliability trust-check ("✓ Sound basis" / "Read this with care") + grounding + issue counts + the one next move; it is **single-depth** ("A single depth — this snapshot is short by design").
- [ ] SC-17 **Assumptions & Evidence** shows the load-bearing unconfirmed assumptions, open questions, and per-dimension inference, with **"a dimension's level is not its trustworthiness"**; inference is named honestly, never as a warning (DL-142/DL-109).
- [ ] SC-18 **Decision Record** lists the owner's decisions from the `_decision` register, each with **what it firmed** (a document → Confirmed by you, ± a reliability move) and a **D088 status**: **"Live in the read"** iff an analysis run is newer than the decision, else **"Awaiting the next analysis update."** A decision **firms the document but never moves the Outcome Confidence read by itself**, and **never self-credits** moving the read (`_decisionRecordRows`, D088).
- [ ] SC-19 The **Summary ⇄ Full depth toggle** exists on Assumptions & Evidence and Decision Record only (Outcome Readiness single-depth), is **persisted** (`repDepth`/`_depthOf`/`setReportDepth`), and **changes how much is shown, never what is claimed** (DL-144). Full adds registers/provenance/withdrawn trails, not new claims.
- [ ] SC-20 Every generated report's **Export reuses the one export modal** (`_genControlsHTML` → `openExportSeam`) — **no parallel machinery**; "send" (a view-only share link of the live project) stays **distinct** from a frozen export (DL-144/D107).
- [ ] SC-21 The **six D143-dead types** (status/risk/stakeholder/executive/portfolio/programme "reports") are held as a **negative list** and never appear as a report type or type-chrome (`D143_DEAD_REPORT_TYPES`, D143).

## Packages-never-produces + report/memo (D146/D168/D171)
- [ ] SC-22 Sharing, commenting, exporting, and generating/scheduling a report **run no analysis and write no assessment** (`_assertReportPackagesNeverProduces` / `_assertReadoutRunsNoAnalysis`). A stale package **says so** ("previous analysis"); it never refreshes the read.
- [ ] SC-23 A **report** (Executive Briefing / the live generated reports) is editable and tracks the read; a **memo** is a dated **immutable, deep-frozen** snapshot that has left OSLO, relabelled "previous analysis" when the read moves past it (`_assertReportAndMemoAreNotConfused` / `_assertMemoIsImmutable`, D168/D171). Editing is **free on every tier — the gate is REUSE** (D154).

## Boundary + cross-cutting
- [ ] SC-24 The **structured Asana execution-export** (DL-151) is **NOT** in this slice — it is Slice 11's **distinct object** (D107) and is referenced, not re-documented (Boundary B).
- [ ] SC-25 Advisory-only throughout (D001); severity red/amber/green only on issues/assumption markers (D003); dark default + light parity; WCAG 2.1 AA (focus, keyboard, reduced-motion); client-side prototype only (D016).

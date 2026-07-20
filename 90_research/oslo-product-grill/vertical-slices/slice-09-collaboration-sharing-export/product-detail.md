# Slice 9 — Collaboration, Sharing & Export · Product Detail

**Scope:** the collaboration/sharing/export layer of the frozen R1 build (md5 `a327d702`) — the sharing dialog, threaded comments + @mentions on findings, the one ratified export/share-out modal, and the **Reports workspace** (Executive Briefing + three generated read-only reports + the depth toggle). Cumulative (Slices 1–9). Product behaviour only; no backend/API/DB.

> Regenerated to match the frozen build (post DL-133→156). **Export ≠ share** (D107); an export/report **produces no assessment** (D112); **no forecast/composite** in any report (D183b); **maturity-not-health** (D003); **computed never invented** (D173); **Decision Record honours D088**; **one export modal, depth changes volume not claim** (DL-144). The structured Asana execution-export (DL-151) is **Slice 11's** and is not documented here.

---

## Component: The sharing dialog (`#shareScrim`) — D110 · `openShare()` / `renderShare()`

- **Entry:** top-bar Share (`#tbShare`, `⤴`) or the "Invite someone new…" item in a comment mention menu.
- **Two limits, side by side, never merged (D124):** a **phase** limit (invites / supply, retires at GA) and a **tier** limit (collaborator seats / depth, enforced on Membership). `renderShare()` writes them into `#shareAlloc` as separate `.limbox` rows. Merging them into one "upgrade" sentence is a prohibited dark pattern. If the last invite attempt was blocked, `#shareBlock` names **which** limit blocked it (`admissionBlockHTML` — the phase message offers the waitlist and carries **no** upgrade CTA; the tier message offers a real upgrade path **and** the free remedy "add them as a Viewer").
- **Invite row:** email input + a **role picker** (`#shareRolePick`) built from `PARTICIPANT_TYPES` minus Owner (Collaborator / Viewer) + Invite (`sendInvite`). Validation: a well-formed email enables the button. No email leaves the prototype; the invite is recorded. **Roles are shown, not enforced** this release.
- **Roles + seats (`#shareTypes`, `PARTICIPANT_TYPES`):** Owner ("Changes the plan, shares it, exports it", `seat:true`), Collaborator ("Comments and answers review requests", `seat:true`), **Viewer** ("Reads the plan and OSLO's read of it", `seat:false`). `_roleTakesSeat()` drives the seat cap; **Viewers hold no seat and are unlimited on every tier** (X-1, `_assertViewersUnlimited`). **Asking for a read is free — no invite, no seat** (CR-2).
- **People (`#sharePeople`, `_members()`):** a **view over the Membership registry** (`MEMBERSHIPS`, keyed by principal email, N-2 — never a second registry). Each row: name (+ "you"), email, seat/no-seat chip, role, and pending-invite state (real 14-day expiry + "returns to your balance if unused" refund).
- **Share link (`#shareLinkBox`) — a view-only snapshot of the project:** "Create a view-only link" → `createSnapshotLink()` → `_mkLink('snapshot')`. It shows the read **as it stood when the link was made**, never re-runs an analysis; if the read has moved on, the link shows a **"previous analysis"** label with its date (`_linkStale`). Per link: **Copy link** (`copyLink`) · **Preview what they see** (`openSnapshotPreview`) · **Revoke** (`revokeLink`, appends a History event). Lifetime **30 days, revocable** (`SHARE_LINK_EXPIRY_DAYS`, CR-6) — **the same on every plan** (D128 P2; `CONFIGURABLE_EXPIRY_BASIC = false`, safety is never sold).
- **The object distinction, in the dialog:** *"A share link is not an export link."* A share link = revocable view-only access to the **live** project; an export link = a **frozen** copy of one snapshot (D107).
- **Footer:** *"Sharing changes no assessment. Only an analysis update does."*

## Component: Threaded comments + @mentions on findings — D111 / D114 / D162a · `_commentsHTML(id)`

- **Store:** `COMMENTS` keyed by issue id → `[{id, who, email, ts, body, parent, mentions}]`. **Append-only: there is no `editComment()` and no `deleteComment()` — by design (D111).**
- **Add / reply (`addComment(parentId)`):** posts the textarea body; a **Reply** passes the last comment's id as `parent` (a thread child, `.cm-reply`, "reply" chip). Empty body flags the field. Writes an **append-only History `comment` event** (D096) naming any mentions, with "Comments are append-only and change no assessment — only an analysis update does."
- **@mentions (`cmInput` / `cmKey` / `cmPickMention`):** typing `@` opens `#cmMention` over a pool of `TEAMMATES` + project members; ↑/↓ + Enter/Tab select; picking inserts `@Name `. The trailing **"Invite someone new…"** item closes the issue and opens the sharing dialog. `_cmRender()` highlights known `@Name` tokens as `.mention` pills.
- **Honesty (`COMMENT_HONESTY` = "Comments never change the assessment."):** shown **once, short** at the compose box (D162a). The full append-only contract is the row's ⓘ tooltip ("Append-only — comments can't be edited or deleted once posted"), not a standing lecture.
- **Keyboard:** `@` mention menu, `⌘↵ / Ctrl↵` posts.

## Component: The export / share-out modal (`#exportScrim`) — D112 · `openExportSeam()` → `openExport()` / `renderExport()`

- **`openExportSeam()`** is the single seam every export path calls (the top bar and every generated report's Export control) → `openExport()`. (The frozen build carries an earlier `openExportSeam` stub that is overwritten later in load order by the real `openExport()` binding.)
- **Currency block (`#exportCurrency`, D112/D153/D163):** facts, not prose — **Outcome Confidence** band + reliability (from `_readCurrency`), the analysis run + when + state, the open-issue count, and Clarity · Alignment · Feasibility. Read off live state, never invented (D173).
- **Disclaimer (`#exportDisclaimer`, `EXPORT_DISCLAIMER`, D003/DL-104):** verbatim — *"…understanding maturity … **not** a measure of project health, readiness, or probability of success."* This is the P1 anti-health-framing guard rendered as copy.
- **Formats (`#exportFormats`, `EXPORT_FORMATS`):** `pdf` (free) · `copy` (Basic) · `link` (Basic — "A hosted copy of THIS snapshot, frozen. Not the same as a share link."). **Free = PDF only** (D112/D123, tier gating live in Alpha). Locked formats are **shown with a Basic label, never hidden** (D048) and **the button stays enabled** (D138) — `doExport()` gates the **attempt** (`TIER==='free' && !fmt.free` → `fireUP('UP-EXPORT')`), never the control. Tier note (`#exportTierNote`) carries a real "Compare →" path.
- **The record (`doExport()`, D112):** appends a History `export` record — "Carried the analysis-currency marker … Export generates no new assessment and never triggers an analysis." **An export is a read.** Restates D107 in the tier note: an export link ≠ a share link.
- **Strategic Readout Composer (WI-R1, DL-107/108/104) — the export preview:** `sroRender()` assembles a **five-section spine** into `#sroDoc`, live from `ISSUES` + the current read: §1 **The read** (`sroRead`) · §2 **What's limiting it** (`sroLimit`) · §3 **What we don't know yet** (`sroUnknowns`) · §4 **What I need from you** (`sroAsk`) · §5 **What I'd need to be sure** (`sroSure`) · §6 **How to read this** (`sroHow`). **§4 is the ONLY audience-dependent section** (DL-108) — the audience selector renders the four `REPORT_RECIPIENTS` (Sponsor / Programme lead / Operations / Executive-board) and tailors **the ASK, never the READ**; §1–§3, §5, §6 are structurally byte-identical across audiences (`_assertReadIdenticalAcrossAudience`). **Assembling it runs NO analysis and writes nothing to History/Trend** (`_assertReadoutRunsNoAnalysis` — packages, never produces).

## Component: The Reports workspace — DL-141→144 · `enterReports()` / `renderReportTabs()` / `switchReport()`

- **Tab strip (`#rptTabs`, `renderReportTabs`):** one `.rw-tab` per registered `REPORT_TYPES`, each carrying a **`.rt-kind`** chip ("Authored" / "Generated") + the document name. A slim strip **hosting more than one report** (DL-141). `switchReport(k)` sets `_curReportK`, shows the authored composer page (`#rptAuthoredPage`) **or** the generated page (`#rptGenPage`) and calls the type's `render()`. The Briefing's `#rptDoc`/`#rptEd` stay in the DOM (hidden) so its guards still verify.
- **`REPORT_TYPES` registry:**
  - `readout` — **Executive Briefing** (display name; internal `nm:'Readout'` unchanged so the D143 dead-type guard reads it correctly), kind **authored**. `render → renderReports()` (the composer). Editing free on every tier; the gate is REUSE (D154).
  - `readiness` — **Outcome Readiness** (DL-141), kind **generated**, single-depth. `render → renderOutcomeReadiness()`.
  - `assumptions` — **Assumptions & Evidence** (DL-142), kind **generated**, `depth:true`. `render → renderAssumptionsEvidence()`.
  - `decision` — **Decision Record** (DL-143), kind **generated**, `depth:true`. `render → renderDecisionRecord()`.
- **The D143 negative list (`D143_DEAD_REPORT_TYPES`):** status / risk / stakeholder / executive / portfolio / programme "reports" — the six D143 killed (they were sections of one memo, not reports). The registry guard fails if any resurfaces as a type; every generated type's `nm` is chosen to carry none of those dead first words.

### Sub-component: Depth toggle (DL-144) — `_REP_DEPTH` / `_depthOf(k)` / `setReportDepth(k,d)`

- **Per-report Summary ⇄ Full**, rendered by `_genControlsHTML(k)` only where `t.depth` is true (Assumptions & Evidence, Decision Record). Outcome Readiness shows "A single depth — this snapshot is short by design."
- **Persisted** in `repDepth` (localStorage), so re-entering a report restores the last depth. `setReportDepth` re-renders the current report in place.
- **Depth changes VOLUME, never the CLAIM** (DL-144): Full adds registers, provenance and withdrawn trails; it never changes what the report asserts.
- **Export control (`_genControlsHTML`):** every generated report carries an **Export** button → `openExportSeam()` — **the one ratified modal** (DL-144). No parallel machinery; "send" (a view-only share link) is kept distinct from an export (D107).

### Sub-component: Outcome Readiness (`renderOutcomeReadiness`) — DL-141

Computed live from `currentRead()` / `_cafOf` / `_limitingOf` / reliability / grounding / `ISSUES` — nothing authored, no forecast/composite (D183b), maturity not health (D003). Sections: **Outcome Confidence** (band + 5-step maturity ramp + plain-language lead naming the weakest dimension); **What's driving it** (CAF rows — mini ramp + level + "the limit" marker + a per-dimension evidence cue, level ≠ trust); **Can you trust this read** (reliability basis Coverage · Evidence · How assessable + a `_reliabilitySound` trust-check pill "✓ Sound basis" / "Read this with care"); **Where the read stands** (grounding rollup + open/critical issue counts + the ladder rung); **The one next move** (the top load-bearing assumption behind the sharpest open issue, if any). Foot: "OSLO advises; you decide — this reflects OSLO's understanding of the plan, not a guarantee of the outcome."

### Sub-component: Assumptions & Evidence (`renderAssumptionsEvidence`) — DL-142

Computed from `_ciLoadBearingStatements` / `_ciInferred`, `_openClarIds`, `_ciDimInferenceStats`, `_progressRows`. Intro states the Confirmed-by-you vs still-inferred split of the total statements. **Summary:** the load-bearing assumptions still unconfirmed (severity-ranked, "confirm these first"), open questions, and where each dimension leans on inference — with the explicit note *"A dimension's level is not its trustworthiness."* **Full** (`_depthOf('assumptions')==='full'`) adds: for each load-bearing assumption, the open issues that break if it is wrong; and the **complete inferred register**, every still-inferred statement grouped by dimension with a "load-bearing" tag. Inference is named honestly, never as a warning. Foot: "…Marking an assumption unconfirmed is honesty about the evidence, not a warning about the plan."

### Sub-component: Decision Record (`renderDecisionRecord` / `_decisionRecordRows`) — DL-143 · **D088 is the law**

- **Rows** are the owner's decisions from the `_decision` register (newest first by History index). Each row: a **verb** by kind — `fix` → "Applied OSLO's fix" (firms), `answer` → "Answered OSLO's question" (firms), else "Chose a path" (does not firm); the issue it addressed; and a **firm clause** — "Firmed **<document>** — now Confirmed by you" (± "reliability X → Y" when the document's reliability moved), or "a path chosen, not yet confirmed."
- **D088 status (`takenUp`):** a decision is **"Live in the read"** iff an analysis run is **newer** than it (`runIdx < idx(r.evId)`); otherwise **"Awaiting the next analysis update."** A decision **never self-credits moving the read** — *"A decision firms the document it touches … It does not move the Outcome Confidence read by itself — that moves only when the next analysis update takes the change up."*
- **Full** adds each row's issue provenance (severity + what confirming it unblocks) and a **Withdrawn — the append-only trail** section (`HISTORY` `withdrawn` events — a withdrawal is a new event, never an erasure).
- Empty state invites the first decision. No composite/forecast (D183b); maturity not health (D003).

## Behaviour: everything here packages, never produces

- **Sharing, commenting, exporting, generating/scheduling a report all run NO analysis and write NO assessment** — proven by `_assertReadoutRunsNoAnalysis()`, `_assertReportPackagesNeverProduces()`, and the History honesty copy on every event. A stale package **says so** (relabelled "previous analysis"); it does not go and refresh the read.
- **Report vs memo (D168/D171):** you edit a **report** (living, tracks the read); what travels is a **memo** (dated, deep-frozen at cut, immutable, relabelled "previous analysis" when the read moves past it). `_assertReportAndMemoAreNotConfused()` / `_assertMemoIsImmutable()`.

## Non-goals / seams (do not build here)

- The **structured Asana execution-export** (DL-151 — mapping preview, simulated hand-off, provenance custom field, OSLO Task ID) is **Slice 11's** distinct object (D107) — referenced, not built here.
- **CRR (CAF Review Requests)** virality loop is escalated out of scope for this slice.
- Tier **numbers/prices** and enforcement are Slice 10's subject (illustrative here, owner-TBD).
- Real email delivery, real auth/accounts, and any server persistence are out of scope (D016 — client-side prototype; "persistence" is localStorage).

## OWNER-DECISION FLAGS

Genuine owner-open items the frozen build itself flags on this slice's surfaces (documented as-frozen; not resolved here):

- **Report scheduling (`SCHEDULING_R1 = null`).** Whether sending the Executive Briefing on a schedule is R1 or a fast-follow is **owner-open** — the build ships the surface and flags it. Documented as present; the R1/fast-follow call is not made.
- **Report branding tier (`REPORT_BRANDING_TIER = 'basic'`).** Own-branding on the Briefing cover is built at **Basic** but flagged as **unsettled** (could be a higher tier). Owner-TBD.
- **Collaborator seat caps are NOT RATIFIED.** The share dialog surfaces a tier seat cap (Free 3 / Basic 10), but Basic=10 is flagged commercially wrong and the numbers are an unratified product-grill recommendation, **owner decision pending** (`_assertSeatCapsFlagged`, D124/X-1). The seat *numbers* are Slice 10's subject; only their appearance in the share dialog is Slice 9's. Enforced provisionally; **never** the reason anyone is asked to buy.
- **Duplicate `openExportSeam` definition (code hygiene, prototype-wins).** The frozen file defines `openExportSeam()` twice — an early Slice-9 stub (`_stubToast`) and the real binding (`openExport()`) later; load order makes the real one win. Flagged per FREEZE-INTACT (prototype wins on conflict) — behaviour is correct as frozen; not fixed here.

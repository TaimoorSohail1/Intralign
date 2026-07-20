# Slice 9 — Collaboration, Sharing & Export · User Experience

**Release:** OSLO R1 (ALPHA). **Cumulative:** Slices 1–9.
**Baseline of record:** frozen prototype (md5 `a327d702`, boot 157/157).
**Boundary:** advisory-only (D001); sharing/commenting/exporting **never change the assessment — only an analysis update does** (D111/D112); an export/report is a **read**, it produces no assessment (D112); **export ≠ share** — a frozen export snapshot is a distinct object from a view-only share link (D107); no forecast/composite anywhere (D183b); maturity-not-health (D003, a P1 defect class per DL-104); computed never invented (D173); dark default + WCAG 2.1 AA (D015); client-side prototype only (D016).

> **This is a regeneration to match the frozen build.** The baseline slice-09 docs predate DL-133→156; this rewrite documents the surface as frozen — including the **Reports workspace** (DL-141→144), which is the slice's read-packaging output. What Slice 9 *owns* is **share + the reader-export + the Reports workspace**. The **structured Asana execution-export** (DL-151) is **Slice 11's** (`slice-11-execution-ready-planning-export`) — a distinct object (D107), cross-referenced here, not re-documented.

---

## What Slice 9 is

Slice 9 is OSLO's **collaboration-and-hand-off layer** — everything that lets a PM bring other people to the read and carry the read out of OSLO, without ever letting any of it change the read. It adds no new assessment surface; it wraps the existing one. Four things live here:

1. **The sharing dialog** (`openShare`) — invite people by email as Owner / Collaborator / Viewer, and hand out a **view-only snapshot link** to the live project.
2. **Threaded comments + @mentions** on findings (issues) — a conversation recorded next to the read, **append-only, and it changes no assessment**.
3. **Export / share-out** (`openExportSeam` → the one ratified export modal) — package the read as a PDF / copy / export link, carrying the analysis-currency marker and the required understanding-maturity disclaimer, tier-gated, with an append-only export record.
4. **The Reports workspace** (`Reports` view) — a slim tab strip hosting **more than one report**: the **authored Executive Briefing** plus **three generated, read-only reports computed from live state** (Outcome Readiness · Assumptions & Evidence · Decision Record). Every generated report reuses the one export modal.

The organising idea: **OSLO reads and packages; it never produces from a package.** Sharing, commenting, exporting, and generating a report all run **no analysis** and write **no assessment** — they move the existing read to another person or another surface, honestly labelled with when it was produced.

---

## INHERITED (unchanged)

- **Slices 1–2:** activation funnel; four-method intake; Fast Pass ≈30s; the read-led Overview; Outcome Analysis auto-runs, non-blocking, supersedes provisional→current; the clarification loop; OSLO chat + completion notices; optional tour.
- **Slices 3–7:** the Overview (journey arc + persistent Outcome Confidence read + Start here + Progress); Issues; the Inference map; **History & timeline** — the **append-only** record (D096) that comments, shares, exports and revocations all write to.
- **App shell:** left sidebar (Overview · Issues · History · Inference map · **Reports** · Documents · Full plan); top bar carrying **Share (`⤴`)** and **Export** affordances; command palette; chat rail. Chrome neutral; severity colour on issues only.

---

## CURRENT in Slice 9

### 1. The sharing dialog (`#shareScrim`, `openShare` / `renderShare`) — D110

Opened from the top-bar **Share (`⤴`)** control. It has four bands, top to bottom:

- **Two limits, stated separately and never merged (D124).** A **phase limit** (invites / supply — how many new humans you may bring into the Alpha, retires at GA) and a **tier limit** (collaborator seats / depth — how many seats this project holds). The two are shown side by side; **merging them into one "you've hit your limit — upgrade" sentence is the dark pattern and is prohibited.** (Tier numbers are illustrative and are Slice 10's subject; here they are only the seat/invite context around inviting.)
- **Invite by email + a role picker.** Enter an email, pick **Collaborator** or **Viewer** (Owner is never an invite option), press Invite. No email leaves the prototype; the invite is recorded so the participant list and roles are visible. **Roles are shown, not enforced** in this release.
- **What each role can do + whether it takes a seat.** Owner ("Changes the plan, shares it, exports it" · takes a seat), Collaborator ("Comments and answers review requests" · takes a seat), **Viewer** ("Reads the plan and OSLO's read of it" · **no seat**). **Viewers are unlimited on every tier** (X-1) and are never blocked by the seat cap. **Asking for a read is free — no invite, no seat** (CR-2, the load-bearing virality fact).
- **People on this project.** A live view over the Membership registry — each row shows the person, their role, whether they hold a seat, and any pending-invite state (with its real expiry and the "returns to your balance if unused" refund).
- **The share link — a view-only snapshot of the project.** "Create a view-only link" mints a snapshot link; it shows OSLO's read **as it stood when the link was made**, never re-runs an analysis, and if the project has moved on, anyone opening it is told they are looking at a **previous analysis** (never a stale read passed off as current). Per link: **Copy link · Preview what they see · Revoke.** Lifetime **30 days, revocable** (CR-6) — **the same on every plan** (D128 P2, safety is never sold).
- **The distinction, restated in the dialog:** *"A share link is not an export link."* A share link is view-only access to *this project, live in OSLO* — revocable, relabelled when the read moves on. An **export link** is a frozen copy of one snapshot (D107).
- **Footer:** *"Sharing changes no assessment. Only an analysis update does."*

### 2. Threaded comments + @mentions on findings — D111 / D114 / D162a

Inside the issue (finding) detail, a **Comments** row (`_commentsHTML`) holds a thread:

- **A conversation recorded next to the read, append-only.** Comments are added with `addComment()`; a **Reply** posts under the last comment as a thread child. **There is no edit and no delete — by design (D111):** the code has no `editComment()` / `deleteComment()`.
- **@mentions.** Typing `@` opens a mention menu over teammates + project members; picking one inserts an `@Name` pill (rendered as a highlighted mention). The last item, **"Invite someone new…"**, closes the issue and opens the sharing dialog — mentioning a stranger routes into inviting them.
- **The honesty label, once and short (D162a):** *"Comments never change the assessment."* The full append-only contract lives in the row's ⓘ on demand ("Append-only — comments can't be edited or deleted once posted"), not as a standing lecture.
- **Every comment writes an append-only History event** (D096) — the comment, and any names it mentioned — with the line "Comments are append-only and change no assessment — only an analysis update does."
- **Keyboard:** `@` to mention, `⌘↵ / Ctrl↵` to post.

### 3. Export / share-out — the one ratified export modal (`#exportScrim`, `openExportSeam` → `openExport` / `renderExport`) — D112

The single export surface, opened from the top bar or from any generated report's Export control. It carries, in order:

- **The analysis-currency marker (D112/D153) — a set of facts, not a paragraph.** The **Outcome Confidence** band + reliability, the analysis **run + when + state**, the open-issue count, and the three CAF dimension names — **read off live state, never invented** (D173).
- **The required disclaimer (D003/DL-104), verbatim canon:** *"This reflects OSLO's understanding maturity — how clear, aligned and feasible the plan reads to it, and how reliable that read is. It is **not** a measure of project health, readiness, or probability of success."*
- **The formats.** **PDF** (a written snapshot) · **Copy summary** (the read as text) · **Export link** (a hosted copy of *this* snapshot, frozen). **Free = PDF only** (D112/D123 — tier gating is live in Alpha). Locked formats are **shown, never hidden** (D048), and the buttons **stay enabled** (D138) — the *attempt* is gated (→ the value-framed UP-EXPORT prompt naming Basic), never the control.
- **The append-only export record (D112).** Exporting appends a History record — *"Export generates no new assessment and never triggers an analysis"* — and toasts "Exported … dated to the analysis behind it." **An export is a read** (D112). **An export link is not a share link** (D107): a hosted copy of one frozen snapshot vs revocable view-only access to the live project — restated here too.
- **The Strategic Readout Composer (WI-R1, DL-107/108).** The export preview assembles a **five-section spine** live from the issues + the current read: **§1 The read · §2 What's limiting it · §3 What we don't know yet · §4 What I need from you · §5 What I'd need to be sure · §6 How to read this.** The audience selector (Sponsor / Programme lead / Operations / Executive-board, the shared `REPORT_RECIPIENTS` taxonomy) **tailors §4 — the ASK — only** (DL-108); §1–§3, §5, §6 are structurally identical for every audience. **Assembling it runs no analysis** (packages, never produces).

### 4. The Reports workspace (`Reports` view) — DL-141→144

A slim **tab strip** (`renderReportTabs`) that hosts **more than one report**; each tab is labelled **Authored** or **Generated** plus the document name. `switchReport(k)` swaps between the authored composer and the generated-report surface; `enterReports()` is the view entry. The registered `REPORT_TYPES`:

- **Executive Briefing** (`readout`, kind **authored**) — the editable, PM-authored note that goes out (D143). One composable document; editing is **free on every tier — the gate is REUSE, not edit** (D154). Selecting it shows the composer (recipient · sections · options · export · schedule).
- **Outcome Readiness** (`readiness`, kind **generated**, DL-141) — a read-only snapshot of *where the plan stands*, single-depth. Shows the Outcome Confidence band + maturity ramp + plain-language lead, the CAF drivers, the reliability basis with a **trust-check** ("✓ Sound basis" / "Read this with care"), the grounding rollup + open-issue/critical counts + the ladder rung, and **"the one next move."** Every value **computed live** — no forecast, no composite, framed as maturity not health.
- **Assumptions & Evidence** (`assumptions`, kind **generated**, DL-142) — a read-only due-diligence snapshot of *what the plan rests on*: the load-bearing assumptions OSLO still infers (confirm these first), open questions, and where each dimension leans on inference. **Summary ⇄ Full** depth; Full adds the complete inferred register by dimension and names what breaks if each assumption is wrong. Inference is named **honestly, never as a warning**; the "level ≠ trust" note is explicit.
- **Decision Record** (`decision`, kind **generated**, DL-143) — a read-only record of **the owner's own decisions** from the `_decision` register, each paired with **what it firmed** (a document → Confirmed by you, possibly raising that document's reliability) and **whether the read has taken it up**: **Live in the read** vs **Awaiting the next analysis update**. **D088 is the law of this report** — a decision firms the document it touches but **does NOT move the Outcome Confidence read; the read moves only at the next analysis update.** **Summary ⇄ Full** depth; Full adds the issue provenance and the withdrawn append-only trail.

- **The depth toggle (DL-144).** A per-report **Summary ⇄ Full** control on the two reports that carry it (Assumptions & Evidence · Decision Record); Outcome Readiness is single-depth ("A single depth — this snapshot is short by design"). Depth is **persisted** (`repDepth`), so re-entering restores the last choice. **Depth changes how much is shown, never what is claimed** (DL-144).
- **One export modal for everything (DL-144).** Every generated report's Export control calls `openExportSeam()` — the same modal above, with the same currency marker, disclaimer, tier gating and append-only record. **No parallel export machinery.** "Send" (a view-only share link, a share of the *live* project) is kept distinct from a frozen export (D107).

---

## Report vs memo — the object distinction (D168 / D171)

A **report** is the living document inside OSLO — editable, current, it tracks the read (the Executive Briefing; the generated reports re-compute on every view). A **memo** is a dated snapshot that **has left OSLO** — exported, shared, or sent. **Once cut, a memo never changes again** (deep-frozen). What it *does* change is its label: when the read moves past it, it is shown as **"previous analysis"** — the date it carries is a fact about the run behind it. Cutting a memo runs **no analysis** (packages, never produces).

---

## Journey (Slice 9 lens)

1. From any read, the PM opens **Share** → invites a Collaborator, or creates a **view-only snapshot link** and copies it. A recipient opening the link sees the read as it stood, labelled current or "previous analysis."
2. Inside a finding, the PM (or a Collaborator) leaves a **comment**, `@`-mentions a teammate, and posts. The thread records next to the read; the assessment is untouched; History gains an append-only row.
3. The PM opens **Export**, reads the currency marker + disclaimer, and exports a **PDF** (Free) — or hits Copy/Export link and sees the honest, value-framed Basic prompt. The export is recorded; nothing is re-analysed.
4. The PM opens **Reports** → reads **Outcome Readiness**, switches to **Assumptions & Evidence** and flips it to **Full**, then **Decision Record** and confirms each decision's "Live in the read" vs "Awaiting the next analysis update" status. Any report can be **Exported** through the one modal.
5. For an **execution hand-off to Asana**, the PM crosses into Slice 11's structured export — a distinct object, not this slice's reader-export.

All calls stay with the user (D001). OSLO reads, packages, and hands off; nothing here changes the plan or the read.

---

## Boundary with Slice 11 (owner-accepted 2026-07-20)

Slice 9 owns **share + the reader-export + the Reports workspace**. The **structured Asana execution-export** (DL-151 — mapping preview → simulated hand-off; only the plan crosses; provenance custom field + OSLO Task ID) is **Slice 11's**. They are **distinct objects** (D107): the reader-export is a *frozen human snapshot*; the Asana export is the *structured executable hand-off*. See `slice-11-execution-ready-planning-export`.

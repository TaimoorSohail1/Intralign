# Slice 9 — Collaboration, Sharing & Export · Product Data

Client-side prototype only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no API, no real AI, no email.** "Persistence" means browser localStorage. These are the **product entities, visible fields, and prototype-local data concepts** the collaboration/sharing/export layer and the Reports workspace read and append to — not a schema.

> Regenerated to the frozen build. **Export ≠ share are distinct objects** (D107). Comments and export records are **append-only** (D111/D112). Reports are **computed, never authored** (D173), carry **no forecast/composite** (D183b), and the Decision Record honours **D088**.

---

## Membership & roles (the sharing registry) — D110 / D124 / N-2

`MEMBERSHIPS` — **one registry**, keyed by principal email (principal × project × role). The people list is a **derived view** (`_members()`), never a second registry.

| Field | Values | Notes |
|---|---|---|
| `email` | principal email | one identity per person (N-2) |
| `project` | project id | |
| `role` | **Owner · Collaborator · Viewer** (`PARTICIPANT_TYPES`) | Owner/Collaborator hold a **tier seat** (`seat:true`); **Viewer holds no seat** (`seat:false`) and is **unlimited on every tier** (X-1) |
| `pending` | bool | invited, not yet accepted (X-2) — 14-day expiry, refunded to balance if unused |

- **Role lines (label role, ≤8 words):** Owner "Changes the plan, shares it, exports it." · Collaborator "Comments and answers review requests." · Viewer "Reads the plan and OSLO's read of it."
- `_seatsUsed()` counts **seat-holding** memberships only (Viewers excluded, X-1). `DEFAULT_SHARE_ROLE` = `Collaborator` (localStorage `defaultShareRole`).
- **Roles are shown, not enforced** in this release.

## Share links (view-only, revocable) — D110 / D117 / CR-6 / D172c

`SHARELINKS` — **one link factory** (`_mkLink`). Three kinds share it; Slice 9 mints the `snapshot` kind from the share dialog.

| Field | Values | Notes |
|---|---|---|
| `kind` | `snapshot` (project) · `issue` (review grant) · `memo` (one shared memo) | Slice 9's share dialog creates `snapshot` |
| `scope` | project / issue / memo | a snapshot link scopes the whole project |
| `url` | `https://app.oslo.intralign.ai/s/v/…` (snapshot) | illustrative host |
| `runIndex` | the read's run at creation | drives the "previous analysis" relabel (`_linkStale`) |
| `days` | **30** for snapshot (`SHARE_LINK_EXPIRY_DAYS`, CR-6) | same on Free and Basic |
| `revoked` / `expired` | bool | `_linkDead()`; revocation appends a History event |
| `granted` | bool | the token-acceptance flips once on landing (the invite IS the auth, D119/D172c) |

- **A share link is view-only access to the LIVE project** — revocable, relabelled **"previous analysis"** when the read moves on. **Never re-runs an analysis.** Lifetime + revocation are identical on every tier (`CONFIGURABLE_EXPIRY_BASIC = false`, D128 P2 — safety is never sold).
- **A share link is NOT an export link** (D107) — different object, different name, everywhere.

## Comments on findings (append-only) — D111 / D114

`COMMENTS` — keyed by **issue (finding) id**.

| Field | Values | Notes |
|---|---|---|
| `id` | `CM-<n>` | `_cmSeq` |
| `who` / `email` | author profile name / email | |
| `ts` | "just now" (illustrative) | |
| `body` | the comment text | `@Name` tokens rendered as `.mention` pills (`_cmRender`) |
| `parent` | comment id or `null` | a reply threads under its parent (`.cm-reply`) |
| `mentions` | names mentioned | drives the History event text |

- **Append-only: no edit, no delete** — there is no `editComment()`/`deleteComment()` (D111). `COMMENT_HONESTY` = "Comments never change the assessment."
- Mention pool = `TEAMMATES` + project `_members()`; "Invite someone new…" routes to the share dialog.

## Export record + formats — D112 / D123 / D138

- **`EXPORT_FORMATS`:** `pdf` (`free:true`) · `copy` (`free:false`) · `link` (`free:false`, "a hosted copy of THIS snapshot, frozen"). **Free = PDF only** (tier gating live in Alpha); non-free formats are **shown + locked, never hidden** (D048) and the button stays enabled (D138).
- **`EXPORT_DISCLAIMER`** (verbatim canon, D003/DL-104): "…understanding maturity … **not** a measure of project health, readiness, or probability of success."
- **Currency marker** (`_readCurrency`, D112/D153): band + reliability + run + when + state + open-issue count — **read off live state, never invented** (D173).
- **The export record:** `doExport()` appends a History `export` event — "Export generates no new assessment and never triggers an analysis." **An export is a read** (D112) and a **frozen** object, distinct from a share link (D107). `copy` writes the read to clipboard; the record is appended regardless.

## Strategic Readout Composer state (export preview) — WI-R1 / DL-107 / DL-108

`SRO = { aud, opts:{alignment, assumptions, matured, artifact} }`. The **five-section spine** (§1 read · §2 limiting · §3 unknowns · §4 ask · §5 what I'd need to be sure · §6 how to read this) is assembled live from `ISSUES` + the current read. **Audience (`aud`) is one of `REPORT_RECIPIENTS`** (Sponsor / Programme lead / Operations / Executive-board) and **feeds §4 only** (DL-108) — every other section is structurally identical across audiences. Assembling it **runs no analysis** (packages, never produces).

## Reports registry (the Reports workspace) — DL-141→144

`REPORT_TYPES` — the ordered, registered set the tab strip renders. `REPORT_TYPE_DEFAULT = 'readout'`.

| `k` | Document (`doc`) | `kind` | `depth` | Renderer | Decision |
|---|---|---|---|---|---|
| `readout` | **Executive Briefing** (internal `nm:'Readout'`) | authored | — | `renderReports()` | D143 · editable, PM-authored |
| `readiness` | **Outcome Readiness** | generated | no (single-depth) | `renderOutcomeReadiness()` | DL-141 |
| `assumptions` | **Assumptions & Evidence** | generated | **yes** | `renderAssumptionsEvidence()` | DL-142 |
| `decision` | **Decision Record** | generated | **yes** | `renderDecisionRecord()` | DL-143 |

- **`D143_DEAD_REPORT_TYPES`** (negative list — the guard fails if any becomes a type): status · risk · stakeholder · executive · portfolio · programme "reports." They were sections of one memo, not reports.
- Each generated report is **computed live** — no authored data, no forecast/composite (D183b), maturity not health (D003).

## Depth state (persisted) — DL-144

`_REP_DEPTH` (localStorage key **`repDepth`**), `_depthOf(k)` ∈ {`summary` (default), `full`}, `setReportDepth(k,d)`. Applies to `assumptions` + `decision` only; `readiness` is single-depth. **Depth changes how much is shown, never what is claimed.**

## Decision Record source data — DL-143 / D088

`_decisionRecordRows()` reads the **`_decision`** register (keyed by issue id) + `HISTORY` + `PLAN_SECTIONS`:

| Concept | Meaning |
|---|---|
| `kind` | `fix` / `answer` / `path` → verb + whether it **firms** a document |
| `doc` | the document the decision touched → now "Confirmed by you" |
| `relBefore` / `relNow` | the document's reliability before/after (a firm can raise it) |
| `takenUp` | **true iff an analysis run is newer than the decision** (`runIdx < idx(evId)`) → "Live in the read"; else "Awaiting the next analysis update" |

**D088:** a decision firms the document it touches; the **Outcome Confidence read moves only at the next analysis update**, never from the decision alone. A decision **never self-credits** moving the read.

## Report vs memo — D168 / D171

- **Report** = the living document inside OSLO (Executive Briefing; the generated reports re-compute on view) — editable, tracks the read.
- **Memo** (`REPORT_SNAPSHOTS`) = a dated snapshot that **left OSLO** — **deep-frozen** at cut (`_deepFreeze`), immutable, relabelled **"previous analysis"** when the read moves past it. Cutting one runs **no analysis**.

## History integration (append-only) — D096 / D111 / D114

Comments, shares (link creation/revocation), and exports all append **append-only** events to `HISTORY` (`comment` · `share` · `export` · `withdrawn`), each carrying the honest line that the action **changed no assessment — only an analysis update does**. The record is **never metered or trimmed** on any tier (D128 P1).

## localStorage keys (browser-local persistence)

- `repDepth` — per-report Summary/Full depth (DL-144).
- `defaultShareRole` — the invite role default (`Collaborator`).
- `rptComposer` / `rptSchedule` / `rptEdits` — Executive Briefing composer state, schedule, and (Basic-only) persisted edits (D154 — Free rewrites, nothing persists).
- Inherited Slice 1–7 keys (account, phase/tier, History). `COMMENTS`, `SHARELINKS`, `MEMBERSHIPS`, `SRO`/`RPT` runtime state are in-memory unless noted.

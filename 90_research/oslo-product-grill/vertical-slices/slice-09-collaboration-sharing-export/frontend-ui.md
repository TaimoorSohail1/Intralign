# Slice 9 — Collaboration, Sharing & Export · Frontend / UI

Single openable HTML; dark default + light override on the same tokens (D015); WCAG 2.1 AA (focus-visible rings, keyboard operability, reduced-motion). No framework; plain JS + CSS variables. Colour discipline: sharing/export/report chrome is neutral; **severity red/amber/green appears only on issues** (D003); no percentage fills, no health bars, no RAG in any report.

> Regenerated to the frozen build (md5 `a327d702`). The Slice 9 surfaces are the **sharing dialog**, the **comments thread on findings**, the **one export modal**, and the **Reports workspace** (tab strip + generated reports + depth toggle). Export ≠ share, everywhere (D107).

## The sharing dialog — `#shareScrim` (D110)

`role="dialog" aria-modal="true"`; opened by `openShare()`, closed by `closeShare()` (Esc / backdrop / Done).

| Element | Selector / id | Notes |
|---|---|---|
| Two-limit banner | `#shareAlloc` | phase (`.limbox.lim-phase`) + tier (`.limbox.lim-tier`), **separate** (D124) — never merged |
| Block notice | `#shareBlock` | `admissionBlockHTML` — names which limit blocked the last invite |
| Invite row | `#shareEmail` + `#shareRolePick` + `#shareInviteBtn` | role picker built from `PARTICIPANT_TYPES` minus Owner; `sendInvite` |
| Roles + seats | `#shareTypes` (`.ptype`) | Owner / Collaborator (`.seat-y` "takes a seat") · Viewer (`.seat-n` "no seat") |
| People | `#sharePeople` (`.pt-row`) | view over `MEMBERSHIPS`; seat chip + role + pending state |
| Share-link box | `#shareLinkBox` (`.lnkbox` / `.lnk-*`) | Create → `createSnapshotLink()`; Copy / Preview what they see / Revoke; "previous analysis" relabel; 30-day revocable |
| Object distinction | `.rule-box` | "A share link is not an export link" → links to `openExport()` (D107) |
| Footer | `.wm-f` | "Sharing changes no assessment. Only an analysis update does." |

- **Colour:** neutral chrome; the phase/tier `.limbox` and seat chips are informational, never RAG. Revoked link state uses `--danger` on the URL/chip only.

## Comments on findings — inside the issue detail (`_commentsHTML`) (D111/D162a)

| Element | Selector / class | Notes |
|---|---|---|
| Thread | `.cm-thread` | comment rows; a reply is `.cm-reply` with a "reply" chip |
| Comment row | `.cm` / `.cm-av` / `.cm-b` / `.cm-hd` / `.cm-tx` | avatar initials + who + ts + body; `@Name` → `.mention` pill |
| Compose | `#cmInput` (textarea) | `oninput="cmInput()"` `onkeydown="cmKey(event)"`; `⌘↵` posts |
| Mention menu | `#cmMention` (`.cm-men`, `role="listbox"`) | `@` opens; ↑/↓ + Enter/Tab select; "Invite someone new…" → share dialog |
| Foot | `.cm-foot` (`.cm-note`) + Reply/Comment buttons | honest label "Comments never change the assessment" (D162a) |
| Row header ⓘ | `_ipRowHTML(...,'Append-only — comments can't be edited or deleted once posted.')` | the append-only contract, on demand |

- **No edit/delete affordance exists** (D111) — there is no such control in the DOM.

## The export modal — `#exportScrim` (D112)

`role="dialog" aria-modal="true"`; `openExportSeam()` → `openExport()`; `closeExport()`.

| Element | Selector / id | Decision | Notes |
|---|---|---|---|
| Currency marker | `#exportCurrency` | D112/D153 | band + reliability + run + when + open issues + CAF names — facts, not prose |
| Disclaimer | `#exportDisclaimer` (`EXPORT_DISCLAIMER`) | D003/DL-104 | verbatim "understanding maturity … **not** health/readiness/probability" |
| Formats | `#exportFormats` (`.ex-opt`, `.ex-lock`) | D048/D138 | PDF (free) · Copy · Export link; locked = **shown + labelled Basic**, button **stays enabled** |
| Tier note | `#exportTierNote` (`.limbox.lim-tier`) | D123/D107 | Free = PDF-only; "Compare →"; restates export link ≠ share link |
| SRO preview | `#sroDoc` (`.sro-sec` / `.sro-sh` / `.sro-sb`) | DL-107/108 | five-section spine; audience selector tailors §4 only |

- **`.ex-lock` is a LABEL, not a lock** (D138) — the button works; the attempt is gated in `doExport()` (→ UP-EXPORT).

## The Reports workspace — the `Reports` view (DL-141→144)

| Element | Selector / id | Notes |
|---|---|---|
| Tab strip | `#rptTabs` (`.rw-tab`, `.rt-kind`) | `renderReportTabs()`; one tab per `REPORT_TYPES`, "Authored"/"Generated" chip + doc name; `role="tab"` |
| Authored page | `#rptAuthoredPage` + `#rptBar` (composer) | Executive Briefing; hidden when a generated report is shown |
| Generated page | `#rptGenPage` (`.genrep`) | the three generated reports render here; hidden when the Briefing is shown |
| Memo host | `#rptMemoHost` | the sent memo + its package; `aria-hidden` over a generated report |
| Notes rail | `#reportsBody` (`.rw-notes`) | prototype-notes rail (D161) — empty unless the toggle is on |

### Generated-report chrome — `_genControlsHTML(k)`

| Element | Selector / class | Notes |
|---|---|---|
| Depth toggle | `.gr-depth` (`.gd`, `role="tablist"`) | Summary / Full; only where `t.depth` (Assumptions, Decision); `setReportDepth` |
| Single-depth note | `.gr-depthnote` | "A single depth — this snapshot is short by design" (Outcome Readiness) |
| Export | `.gr-exp` (`onclick="openExportSeam()"`) | **the one export modal** (DL-144) |
| Report body | `.genrep` (`.gr-kicker` / `.gr-title` / `.gr-meta` / `.gr-sec` / `.gr-h` / `.gr-card` / `.gr-foot`) | rebuilt with the report; never standing chrome |

### Outcome Readiness (`renderOutcomeReadiness`) — DL-141

`.gr-band` + `.gr-ramp`/`.gr-ramplabs` (5 ordinal maturity steps, neutral) + `.gr-lead`; `.gr-caf` driver rows (mini ramp + level + `.lim` "the limit" + `.ev` evidence cue); reliability card with `.gr-pill` trust-check (`cool` "✓ Sound basis" / `ok` "Read this with care") + `.gr-kv` Coverage/Evidence/How assessable; grounding rollup + issue counts + ladder rung; `.gr-next` the one next move. **No fill, no health colour.**

### Assumptions & Evidence (`renderAssumptionsEvidence`) — DL-142

`.gr-intro` split; `.gr-arow` load-bearing rows (`.mk mk-<sev>` marker + `.a1`/`.a2`, severity word by class only); Full adds `.gr-sub` "if it's wrong" + `.gr-reg-*` full inferred register by dimension with `.gr-lb` "load-bearing"; `.gr-q` open questions; `.gr-caf` per-dimension inference; `.gr-note` "level is not trustworthiness."

### Decision Record (`renderDecisionRecord`) — DL-143 / D088

`.gr-drow` (`.gr-dmark` + `.dt` verb+title + `.dm` firm clause) + **`.gr-dstat`** status pill — **`.gr-dstat-live` "Live in the read"** vs **`.gr-dstat-await` "Awaiting the next analysis update"** (class built outside the literal, D195a). Full adds `.gr-sub` issue provenance + `.gr-wrow` withdrawn append-only trail. Summary count card + the D088 `.gr-note`. Neutral throughout — never RAG.

## Top-bar affordances (inherited chrome, wired here)

| Element | Selector / id | Notes |
|---|---|---|
| Share | `#tbShare` (`⤴`) | `openShare()`; `aria-haspopup="dialog"` |
| Export | top-bar export control | `openExport()` |
| Reports nav | left sidebar `Reports` | `showView('reports')` → `enterReports()` |

## Color discipline (D003)

Sharing, comments, export, and every report use the **neutral** palette — **no percentage fill, no health bar, no RAG.** Report maturity ramps use the cool `--maturity` accent; severity red/amber/green stays on issue/assumption severity markers only. The Decision Record status pills ("Live in the read" / "Awaiting…") are neutral weight/shape, never hue-coded as good/bad.

## Accessibility

- Dialogs: `role="dialog"`, `aria-modal`, labelled; Esc + backdrop close; focus into the primary input on open.
- Role picker / format buttons / depth toggle: `role="group"`/`role="tablist"`, `aria-pressed`/`aria-selected`, keyboard-operable.
- Comment mention menu: `role="listbox"`, arrow-key navigation, Enter/Tab select, Esc close; `⌘↵` posts.
- Tab strip: `role="tab"`/`aria-selected`. Report ramps carry ordinal labels. Colour is never the sole signal (trust-check and status carry words, not just hue). Focus-visible rings + reduced-motion inherited.

## App shell (inherited)

Left sidebar (Overview · Issues · History · Inference map · **Reports** · Documents · Full plan), top bar (Share `⤴` · Export · report/Free chip), command palette (⌘/Ctrl+K), chat rail. Nav chrome neutral. History (`showView('history')`) is the append-only home for every share/comment/export/revocation event.

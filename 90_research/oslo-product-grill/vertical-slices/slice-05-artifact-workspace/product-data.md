# Slice 5 — Plan Artifacts / Artifact Workspace · Product Data

**Client-side only (D016).** All state is fake data + `localStorage` + simulated timers. No DB, server, API, auth, or real AI. Keys are namespaced `oslo-s1-*` (inherited).

Decisions: **D066–D071**, D004 (seven artifacts), D011 (Derived/Attested), D017 (Issues internal object = Finding).

---

## PlanArtifact (NEW — the Slice-5 model)

A **PlanArtifact** is one of the seven planning artifacts OSLO constructs from intake (D004/D035).

| Field | Type | Values / notes |
|---|---|---|
| `id` | string | `Intent` · `Context` · `Scope` · `Requirements` · `WBS` · `Schedule` · `Resources` (code key; `WBS` displays as "Work breakdown") |
| `group` | enum | `Understanding` (Intent·Context·Scope·Requirements) · `Execution` (WBS·Schedule·Resources) |
| `format` | enum | `prose` · `mixed` · `table` — how the body renders (D067) |
| `blocks[]` | array | ordered content blocks (see **Block** below) |
| `version` | int | append-only version counter; bumps on autosave (starts at 2; History = Slice 7) |
| `openIssueCount` | derived | count of open ISSUES with `sec === id` — drives the explorer badge (D066); not stored, computed live |
| `badgeSeverity` | derived | most-severe open issue's severity in this artifact (`critical`/`moderate`/`warning`) — badge color (D003) |

`format` mapping (`_ARTFORMAT`):

```
Intent: mixed        (prose + bulleted goals list)
Context: mixed       (prose + stakeholder table)
Scope: prose
Requirements: mixed  (prose + bulleted acceptance list)
WBS: table
Schedule: table
Resources: table
```

## Block (a content block inside an artifact)

| Field | Type | Values / notes |
|---|---|---|
| `kind` | enum | `p` (prose) · `h3` (subhead) · `ul/li` (bullets) · `table/tr/td` (table) |
| `epistemic` | enum | `derived` ("From OSLO") **default** · `attested` ("Confirmed by you") after edit/confirm (D069) |
| `annotationSpans[]` | array | zero or more inline weakness spans (see **AnnotationSpan**) |
| `attestedMarker` | bool | when `epistemic==='attested'`, block shows the left-border accent |

Epistemic transition (D069): `derived → attested` on edit or confirm. Reverse never happens automatically. **Saving does not change the assessment; only reanalysis does.**

## AnnotationSpan (inline weakness — D068)

| Field | Type | Values / notes |
|---|---|---|
| `fid` | string | the wired issue id (`ISS-01`..`ISS-06`) — internal object is a **Finding** (D017) |
| `severity` | enum | `critical` (`crit`) · `moderate` (`mod`) · `warning` (`warn`) — color only (D003) |
| `dimension` | enum | `Clarity` · `Alignment` · `Feasibility` |
| `text` | string | the contiguous weak text the span wraps |
| behavior | — | hover → summary (title); click → `openIssue(fid)` (light panel); **never resolved inline** |

**Annotation → issue wiring** (each references one live open issue):

| fid | artifact (`sec`) | dimension | severity |
|---|---|---|---|
| ISS-01 | Resources | Feasibility | critical |
| ISS-02 | Requirements | Clarity | moderate |
| ISS-03 | Resources | Feasibility | moderate |
| ISS-04 | Schedule | Feasibility | moderate |
| ISS-05 | WBS | Alignment | moderate |
| ISS-06 | Context | Clarity | warning |

(The single source of truth is the inherited `ISSUES` map + `_istatus`; annotations, explorer badges, the Attention heatmap, and the Overview counts all read from it.)

## Edit / analysis state (D070)

| Field | Type | Values |
|---|---|---|
| `saveState` | enum | `ok` (Up to date) · `saving` (Saving…) · `stale` (Saved · analysis stale) · `reana` (Reanalyzing…) |
| transitions | — | `saving → stale → reana → ok`, driven by simulated timers on edit; no manual trigger |

## Local storage (simulated persistence)

| Key | Value | Purpose |
|---|---|---|
| `oslo-s1-art-<name>` | HTML string | last-saved artifact body (autosave, D067) |
| `oslo-s1-art-<name>-ver` | int | artifact version counter |
| `oslo-s1-tourSeen` | bool | inherited — tour sunsets (now includes the editor step) |
| `oslo-s1-orientSeen`, `oslo-s1-account`, `oslo-s1-staySignedIn`, `oslo-s1-phase` | — | inherited (S1–S4), unchanged |

**No database.** Artifacts, issues, and versions are in-memory JS objects seeded at load; localStorage only persists autosaved bodies + flags for the demo. Reanalysis and confidence movement are simulated; real persistence/AI are owner-TBD.

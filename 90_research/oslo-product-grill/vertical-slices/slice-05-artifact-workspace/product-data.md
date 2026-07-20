# Slice 5 — Plan Artifacts / Artifact Workspace · Product Data

Client-side prototype only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no API, no real AI.** "Persistence" below means browser localStorage; real-store tech is owner-TBD and out of scope. These are the **product entities, visible fields, and prototype-local data concepts** the Artifact Workspace reads/writes — not a schema.

> Regenerated to the frozen build. Supersedes the July-9 slice-05 data doc. **Boundary A:** the execution task model (`WBS_TASKS`, critical path, export mapping) is **Slice 11's** data and is only referenced here.

---

## PlanArtifact ×7 (the workspace's focal object) — D035 / D067

The seven documents OSLO drafts at intake and the user edits here. User-facing term **Documents / Plan artifacts** (D048/D049).

| Concept | Values | Notes |
|---|---|---|
| `_ARTORDER` | `Intent · Context · Scope · Requirements · WBS · Schedule · Resources` | fixed order; `WBS` displays as **Work breakdown** (`dispName`) |
| layer (`_artLayer`) | **Understanding** (Intent·Context·Scope·Requirements) / **Execution** (WBS·Schedule·Resources) | drives the explorer subgroups + the head label |
| body (`ARTBODY[name]`) | HTML: prose / mixed / tables | type-aware (D067) — Understanding prose/mixed, Execution tables |
| version (`_artVersion`) | integer, default 2 | `art-{name}-ver`; **bumps on every committed edit**; versions kept forever (D096) |
| epistemic basis (`_epiOf`) | `derived` (From OSLO) / `attested` (Confirmed by you) | attested once any block/cell in the open artifact is edited |
| open issues | derived from ISSUES (`_artOpenIssues`) | drives the explorer badge count + colour |

- **Artifacts are UNCAPPED and NEVER metered** on any tier, in any phase (D128 P1): no artifact count check, no version-retention window. Do not add one.

## Epistemic provenance (per block / per cell) — D011 / D069 / D083 / D194b

Two **positive** classes, single-sourced from one registry (`EPI_CLASSES` / `epiClassName`).

| Level | Field | From OSLO (default) | Confirmed by you (on edit) |
|---|---|---|---|
| Prose block (`p`/`li`/`h3`) | `.epi-tag`, `.attested`, `data-epi` | "From OSLO" (`derived`) | "Confirmed by you" (`attested`) via `_attestSelectionBlocks` |
| Table cell (`td`) | `data-epi="derived"\|"attested"` + `.cell-epi` reveal chip | seeded `derived` on open (`_seedTableProvenance`) | flips `attested` on cell edit |
| Table row | gutter `.rowprov` dot (`_rowProvState`) | `derived` if all cells derived | `attested` if any cell attested |

- **D196a — the per-item verb is Confirm.** Editing/accepting a cell or task *is* confirming it (the ratified mechanism at cell + task altitude). **D173:** From OSLO marks an inference, never presented as fact.
- Re-draft merge (`redraftArtifact`): attested blocks/cells kept verbatim; only derived content refreshed.

## Autosave / reanalysis state (per open artifact) — D070 / D073 / D079

| Concept | Values | Notes |
|---|---|---|
| save/analysis chip (`#savestate`) | `ok` · `saving` · `editing` · `stale` · `reana` | dot colour + hover title only (no reflow); `ok`="Analysis up to date", `reana`="Reanalyzing…" |
| `_pendEdit` | boolean | a commit is pending; cleared by `commitArtEdit` |
| debounce timers | `_idleT` (~1500ms) · `_reanT2` (~1500ms) | typing-idle → commit → Reanalyzing… → Up to date |
| undo/redo (`_undoStacks`/`_redoStacks`) | per-artifact innerHTML snapshots, cap ~50 | fresh stack per open (D084/D085) |

- **No manual reanalyze control exists** (D070). Editing runs no assessment; the read moves only at an analysis update (D088).

## WeaknessAnnotation (the editor's issue markers) — D068 / D071 / D074

| Field | Meaning |
|---|---|
| `.anno[data-fid]` | inline weak span; `data-fid` → a real open issue (ISS-01…11) |
| severity | severity ramp **red/amber only** (D003); routes to the light issue panel, never resolved inline |
| live-only | `_artBodyLive` unwraps annotations whose issue is not `open` (mark drops on re-render) |
| stepper (`#wnav`) | `curAnnos()` = `#artdoc .anno`; `weaknessNav` cycles k of N; "✓ No issues in view" when empty |

## WBS task tree — DL-143→156 · 2A (**data modelled in Slice 11**)

The Work breakdown body (`ARTBODY.WBS`) is an authored graded task tree rendered as a `<table>`: rows = workstream (`.wbs-h`, `data-lvl="0"`) → task (`data-lvl="1"`) → subtask (`data-lvl="2"`), each with an outline number (`.wbs-n`, e.g. `1 · 1.1 · 1.3.1`) and a Task · Owner pair. Thin inferences carry a neutral `.conf-low` grade. **Every row is From OSLO** until confirmed via the generic cell-provenance engine.

> The underlying **task model** (`WBS_TASKS`: id · outline `n` · workstream · owner · inferred `dur` · `deps` · `lowConf` · `milestone`), the **critical path** computation, the execution-readiness rollup, and the Asana export mapping are **Slice 11 data** (`slice-11-execution-ready-planning-export`) — not re-specified here. The read-only "Sequencing & critical path" panel in the Work-breakdown view is rendered from that model, outside the editable `#artdoc`.

## Issue (the annotation / badge unit) — INHERITED

Internal object = **Finding**; user-facing = **Issues** (D017). `{ title, sev: critical|moderate|warning, dim: Clarity|Alignment|Feasibility, sec:<artifact>, status: open|addressed|resolved }`. The explorer badge and the weakness stepper read `sec` + `sev` + status live. **Only an analysis update resolves an issue** (D088); editing an artifact does not.

## localStorage keys (browser-local persistence)

- `art-{name}` — the artifact's edited `#artdoc` innerHTML (per session).
- `art-{name}-ver` — the artifact version integer (bumps on commit).
- Undo/redo snapshots are in-memory (per open), not persisted.
- Inherited Slice 1–4 keys (phase, orientation-seen, tour-seen, account, analysis state) unchanged.

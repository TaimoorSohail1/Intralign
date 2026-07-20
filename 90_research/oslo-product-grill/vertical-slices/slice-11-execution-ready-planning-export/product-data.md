# Slice 11 — Execution-Ready Planning & Export · Product Data

Client-side prototype only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no real API, no real AI; the Asana connector is simulated.** "Persistence" means browser localStorage; real-store tech is owner-TBD and out of scope. These are the **product entities, visible fields, and prototype-local data concepts** the execution-ready surfaces read — not a schema.

---

## `WBS_TASKS` — the converged task model (the one source of truth)

The whole decomposition as structured data (DL-150 promoted it from sequencing-only to the full plan). The consolidated view (Feature 4), the critical path (Feature 3), and the Asana mapping (Feature 5) **all render from this one array** — not from re-parsed document HTML (D173).

| Field | Values | Notes |
|---|---|---|
| `id` | stable string (`t-cfp`, `t-ros`…) | The stable anchor; becomes the **OSLO Task ID** custom field on export. |
| `ws` | workstream name | Groups tasks in the consolidated view. |
| `n` | outline number (`1.1`, `1.3.1`) | Depth = `n.split('.').length − 1` drives indentation. |
| `name` | task name | Mirrors the Work breakdown document task text. |
| `owner` | Ops lead · Program lead · Sales · Marketing | → Asana **assignee**. |
| `dur` | weeks (integer) — **inferred** | OSLO's inference, flagged low confidence — the least-inferable input (DL-145 §5). `0` for the milestone. |
| `deps` | array of task `id`s | Dependency edges; → Asana **dependency**. |
| `lowConf` | `true` on the thinnest inferences | Carries the neutral `low confidence` grade (D003). |
| `milestone` | e.g. `'Sep 1'` (one task) | The critical path anchors on this task's earliest finish. |

**The 14 tasks × 5 workstreams (frozen data):**

| # | Task | Owner | Dur (wk) | Depends on | Low-conf | Milestone |
|---|---|---|---|---|---|---|
| 1.1 | Sign the venue contract | Ops lead | 2 | — | | |
| 1.2 | Confirm 500-person Wi-Fi capacity | Ops lead | 1 | 1.1 | ● | |
| 1.3 | Finalize the floor plan | Ops lead | 2 | 1.1 | | |
| 1.3.1 | Map AV power drops | Ops lead | 1 | 1.3 | ● | |
| 1.3.2 | Lay out badging & check-in stations | Ops lead | 1 | 1.3 | ● | |
| 2.1 | Close the CFP | Program lead | 2 | — | | |
| 2.2 | Select 2 keynotes + 12 breakouts | Program lead | 3 | 2.1 | | |
| 2.3 | Lock the run-of-show | Program lead | 0 | 2.2, 1.3 | | **Sep 1** |
| 3.1 | Finalize the sponsor kit | Sales | 2 | — | | |
| 3.2 | Sell & assign booths | Sales | 4 | 3.1 | | |
| 4.1 | Launch the registration site | Marketing | 2 | — | | |
| 4.2 | Run the promotion campaign | Marketing | 6 | 4.1 | | |
| 5.1 | Staff check-in & badging | Ops lead | 1 | 1.3.2 | | |
| 5.2 | Run day-of logistics | Ops lead | 1 | 5.1 | | |

Three tasks carry the `low confidence` grade (1.2, 1.3.1, 1.3.2). The Work breakdown *document* mirrors these names (task 2.3 reads "Lock the run-of-show by Sep 1" in the doc; the model names it "Lock the run-of-show" + `milestone:'Sep 1'`).

## Critical path (computed, not stored) — `_criticalPath()`

`{ chain:[task…], weeks:Number }`. Standard earliest-finish over the DAG; the chain is reconstructed by following the critical predecessor back from the **milestone** task. Frozen result: **Close the CFP → Select 2 keynotes + 12 breakouts → Lock the run-of-show, `weeks: 5`**. The marketing chain (Launch registration → Run campaign, 8 wk) is longer overall but does **not** reach the Sep 1 milestone; the critical path is the longest chain **to the milestone** (D173, guard `_assertCriticalPathComputed`). Change an edge or a duration and the path moves.

## Execution readiness (computed, not stored) — `_execReadiness()`

Provenance coverage of the **execution-critical statement set** (`_ciStatements` filtered to `art ∈ {WBS, Schedule, Resources}`):

| Field | Meaning |
|---|---|
| `total` | execution-critical statements (M) |
| `inferred` | still From OSLO |
| `confirmed` | `total − inferred` (Confirmed by you) |
| `frac` | `confirmed / total` |
| `state` | **named validation-progress state** derived from `frac`: `Mostly OSLO's draft` (< .5) / `Load-bearing confirmed` (≥ .5) / `Fully validated` (= 1) — never a "will-succeed" verdict |

**One substrate:** the state is a read-off of grounding, not a second judgment. Scoped to **artifact-readiness, not outcome-likelihood**. The coverage bar is a **Confirmed-by-you read, never a health bar** (D003). Frozen-build render (computed): `Mostly OSLO's draft · 7 of 23` — DL-149's earlier `7 of 29` example predates the DL-150 model promotion; the value is computed, so cite the live figure, not a fixed one.

## Task-altitude findings (Issues) — ISS-10 / ISS-11

Ordinary `ISSUES` entries (internal object = Finding; user-facing = Issues, D017), surfaced on the **deeper (Extended) read**:

| Id | Title | Sev | Dim | Sec | rectype / ftype | Anchor |
|---|---|---|---|---|---|---|
| ISS-10 | The freeze rests on undated tasks | moderate | Feasibility | WBS | planning / Coverage Gap | task 2.1 |
| ISS-11 | Part of the breakdown is inferred | moderate | Clarity | WBS | definition / Assumption | task 1.3.1 |

Each carries `why`, `ev` (real citations), `caf`, `rec`, `paths[]`, `status: open|addressed|resolved`. Lifecycle Open → Addressed → Resolved; **only an analysis update resolves** (D088). Supporting context items **CI-71** (relationship, ISS-10), **CI-72** (assumption, ISS-10), **CI-73** (assumption, ISS-11) — all `hz:'deep'`, `art:'WBS'`, `run:'Extended'`.

## The Asana mapping (prototype-local export object) — `_asanaMapping()`

A per-task projection carrying **only the execution allowlist** — this array *is* the export payload:

| Field | Source | → Asana |
|---|---|---|
| `osloId` | `WBS_TASKS[].id` | custom field **OSLO Task ID** (the monitoring anchor) |
| `name` | task name | Asana task · subtask |
| `assignee` | `owner` | Assignee |
| `due` | `milestone` or `~{dur} wk` | Due date |
| `deps` | dependency task names, joined | Dependency |
| `prov` | `From OSLO` / `From OSLO · low confidence` | custom field **OSLO Provenance** |

**What does NOT cross:** the critical path, the issues, the CAF/band, reliability — OSLO's analysis stays in OSLO (`_assertExportSendsPlanNotAnalysis` enforces the allowlist + the two non-negotiables `prov` and `osloId`). Provenance today is uniformly *From OSLO* (nothing Confirmed by you yet); the three low-confidence tasks cross as *From OSLO · low confidence*. **Tag fallback** on free-tier Asana carries provenance as a tag instead of a custom field.

## Provenance / epistemic classes (INHERITED, D011/D069/D253)

Every statement OSLO extracted splits into **From OSLO** (inferred) and **Confirmed by you** (attested) — both positive epistemic states, the unit is the statement. At task altitude the same classes apply per row; the **`low confidence`** grade is a third, epistemic mark **layered on From OSLO** (thinnest inferences) — never a severity.

## localStorage keys (browser-local persistence)

- WBS document cell provenance + confirmations persist through the existing table-provenance/autosave engine (Slice 5).
- History records (including the Asana export hand-off) persist in the History store (Slice 8).
- `WBS_TASKS`, the critical path, execution readiness, the Asana mapping, and the two findings are **computed/seeded at boot** — a full-plan/mapping value that cannot be computed is absent (D173). The Asana export modal open state and the mapping preview are ephemeral UI, not persisted.
</content>

# R1 UI ↔ Backend Integration Map

> Binds every **dynamic** element of the R1 prototype (`product-design/oslo_r1_experience_mockup_v4.html`) to the canonical **State Model / Event Model / API Contract** so the developer wires the exact UX to real data — and so UI/backend fit is proven *before* code, not discovered at integration. AI-produced; owner ratifies contract changes (Framework 001). Date: 2026-07-01.

> **Gap status (updated 2026-07-02):** **G1 (clarification) — RESOLVED** by DL-089 (`clarification_answer_captured` + `POST /projects/{pid}/clarification-answers`; in-panel + chat). **G2 (notification view/dismiss) — COVERED** by existing `POST /notifications/{nid}:view|:dismiss` in the API catalog. **G3–G8 remain open** build/owner items (history feed read, ledger-derived metrics, confidence-change cause linkage, numeric trend series, auto-reanalysis debounce semantics, recommendation `deferred` surface).

**Contract sources:** `20_handoff/interfaces/RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` · `…_EVENT_MODEL_…` · `…_API_CONTRACT_…` + `API_CONTRACT_ENDPOINT_CATALOG.md`. Prototype internal event names differ from canon — this map translates them.

## Legend
Read = query endpoint that populates it · Write = command endpoint the action calls · Event = what the backend emits (UI updates on it). "Prototype fn" = the function in the mockup.

## Surface-by-surface binding

### Onboarding / intake
| UI element (prototype fn) | Read | Write | Event |
|---|---|---|---|
| "See where I stand" / sample (`ingest`, `exploreSample`) | — | `POST /projects` → `POST /projects/{pid}/artifacts` → `POST /projects/{pid}/analysis-runs:fast` | `project_created`, `artifact_created`, `fast_analysis_requested/started/completed` |
| Auto-provisioned account/workspace/project (DL-073) | — | (server auto-provision on first ingest) | `project_created` |

### Analyzing / building (rails-first)
| UI element | Read | Write | Event |
|---|---|---|---|
| Interstitials + Fast-trace (`seedFastTrace`) | `GET /analysis-runs/{rid}?include=caf_state,confidence_state,mri_snapshot` (poll) | — | `fast_analysis_started/completed` |
| Extended (Deep) trace (`startDeepPass`) | same, `run_type=deep_analysis_pass` | (auto after orientation, or `POST …:deep`) | `deep_analysis_started/completed`, `confidence_recalculated` |
| Arrival "complete in Ns" | run timing from run object | — | `fast_analysis_completed` |

### Overview — Confidence (the signature surface)
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| Ring number + band + reliability (`ring-idx/ring-band/cp-*`) | `GET /projects/{pid}/confidence` → `outcome_confidence_value`, `confidence_band`, `reliability_qualifier` | — | `confidence_created` / `confidence_recalculated` |
| Trend across runs (`renderTrend`, `TREND`) | `GET /projects/{pid}/confidence?history=true` (supersession chain) → value per run | — | `confidence_superseded` |
| Cause-bound change banner (`bumpConfidence`, `#conf-change`) | recalculation payload + the finding(s) that moved it | — | `confidence_recalculated` (**needs cause linkage — gap G5**) |
| "How this is calculated" ⓘ | static (from v0 formula doc) | — | — |
| CAF section (`osec-caf`, `feas-*`) | `GET /analysis-runs/{rid}/caf-state` → per-dimension level, per-dim reliability, **preliminary** flag (Fast) | — | `confidence_recalculated` |
| Reliability section (`osec-rel`) | reliability from confidence/caf state | — | — |
| Progress ledger (`renderLedger`) | derived: `GET …/findings?status=` counts (+ artifact/evidence counts) | — | finding_* events (**deps-confirmed / sections-read need derivation — gap G4**) |
| "Start here" top finding (`renderFocus`) | `GET …/findings?status=open` severity-ordered → first | — | finding_* |

### Findings (center pane = "Findings Workspace" #8)
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| List + Dimension/Severity/Section filters (`renderFinds`, `setFilt`) | `GET /projects/{pid}/findings?severity=&finding_type=` + client filter by CAF dim & artifact | — | `finding_created/updated/closed/reopened` |
| Group-by Dimension/Section (`setGroup`) | client-side grouping | — | — |
| Heatmap cell → scoped list (`openFindingsFor`) | findings filtered by artifact×dimension (or MRI snapshot) | — | — |

### Finding detail (contextual panel — stays a panel)
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| Panel header/summary/evidence/CAF-impact (`openFindingPanel`) | `GET /findings/{fid}` (+ evidence refs) | — | — |
| Recommendations in panel (`selectPath`) | `GET /findings/{fid}/recommendations` | — | — |
| Acknowledge (`ackFinding`) | — | `POST /findings/{fid}:acknowledge` | `finding_updated` |
| Choose a path / Selected Path (`selectPath`) | — | `POST /findings/{fid}:address` + `POST /recommendations/{rid}:accept` | `finding_updated`, `recommendation_accepted` |
| Confirm OSLO draft (`attestDraft`) / edit myself (`applyFix`) | — | `POST /artifacts/{aid}/versions` (Attested authorship) | `artifact_version_created` → stale → recompute |
| Answer clarification (`answerClarification`) | — | **no endpoint — gap G1** | **missing** |
| Close-on-reanalysis (not manual) (`setStatus 'closed'`) | recompute result | (server) `POST /findings/{fid}:close` on reanalysis | `finding_closed` |

### Artifact / plan section (editor)
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| Section content, versions (`openArtifact`, `artHTML`) | `GET /projects/{pid}/artifacts`, versions | `PATCH /artifacts/{aid}`, `POST /artifacts/{aid}/versions` | `artifact_updated`, `artifact_version_created` |
| Inline weakness spans / stepper (`_a`, `weaknessNav`) | findings linked to artifact | — | finding_* |
| Edit → autosave → "Reanalyzing…" (`onArtInput`) | staleness state | version create → recompute (fast/deep per policy) | `artifact_version_created`, analysis events |

### History (center pane)
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| Append-only timeline (`renderHistory`, `HISTORY`) | **aggregated history feed across the 11 R1 categories — gap G3** (today: per-object reads + event stream) | — | all lifecycle events (current/prior/superseded labels) |

### Global shell / actions
| UI element (fn) | Read | Write | Event |
|---|---|---|---|
| Project switcher (`toggleProjMenu`) | `GET /projects?lifecycle_state=` | — | — |
| Notifications (`openNotif`) | `GET /notifications?state=` | mark read/dismiss — **endpoint not in catalog — gap G2** | `notification` states |
| Share + Viewer/Collaborator roles (`openShare`) | `GET /shares` | `POST /shares` (`permission_level`: view=Viewer, comment=Collaborator), `POST /shares/{sid}:revoke` | `artifact_shared`, `share_revoked` |
| Export snapshot (`openExport`) | — | `POST /projects/{pid}/reports` → `POST /reports/{rid}:publish` | `report_generated`, `report_published` |
| @mention (`mentionInput`, `pickMention`) | workspace members | `POST /projects/{pid}/comments` (with mentions) | `comment_created`, `mention_created` |
| Command palette (⌘K) | none — client nav that calls the same reads/actions | — | — |

## Contract gaps to close (before/with the build)

| ID | Gap | Why it matters | Recommendation |
|---|---|---|---|
| **G1** | **Clarification request/answer** flow absent from Event/API model | Prototype's OSLO-asks-you-answer path (`answerClarification`) has no contract | Owner scope decision: add a clarification contract package for R1, or defer the flow to R2 (prototype documents it) |
| **G2** | Notification **mark-read/dismiss** endpoint not in catalog | Notif center needs to change `state` (Viewed/Dismissed) | Confirm/add `POST /notifications/{id}:view` / `:dismiss` |
| **G3** | Unified **History feed** read | History surface aggregates 11 categories; unclear if one feed or many per-object reads | Confirm a `GET /projects/{pid}/history` (or specify client aggregation of event stream) |
| **G4** | Ledger **derived metrics** ("dependencies confirmed", "plan sections read") aren't first-class objects | Progress ledger shows them | Define derivation (from artifact/evidence status) or drop those two counts; keep findings-resolved/critical (first-class) |
| **G5** | **Confidence-change cause linkage** in `confidence_recalculated` payload | Cause-bound banner ("rose because you resolved X") needs the finding link | Confirm payload carries the driving finding/CAF-dimension refs |
| **G6** | **Confidence trend series** — does `confidence?history=true` return `outcome_confidence_value` per run? | Trend chart plots numeric per run | Confirm the history read includes the numeric value + run label, not just band |
| **G7** | **Auto-reanalysis on edit** semantics (fast vs deep, debounce) | Prototype auto-recomputes after an edit | Bind to the recompute/stale backbone; specify which pass + trigger timing |
| **G8** | **Recommendation deferred** state (`:defer`) has no prototype surface | Contract supports Deferred; UI doesn't expose it | Decide: add a "defer" affordance in the finding panel, or note R1 omits it |

## Build sequencing implication
- Elements with **no backend dependency** (command palette, panes/nav, filters/group-by, plain-language, artifact format, Start-here) → developer can build immediately against the prototype.
- **Confidence surface** → buildable now against the **v0 formula** + confidence read/events; final thresholds/±7 slot in when calibration ratifies (queue #2).
- **Gaps G1–G8** → route as contract clarifications/additions alongside the UX-surface reconciliation PR; G1 (clarification) is the only one that may change R1 scope.

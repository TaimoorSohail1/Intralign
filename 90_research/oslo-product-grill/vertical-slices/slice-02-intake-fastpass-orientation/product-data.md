# Slice 2 — Intake & Fast-Pass Orientation · Product Data

Prototype-local only (D016): entities live in JS + localStorage. No DB technology, schema, or backend implied. Field names below are the illustrative shape the prototype uses; canonical internal names (Finding, PlanFact) are preserved per D012/D095.

## Entities

### PlanSection ×7 (D035, D004, D011)
The seven artifacts OSLO constructs from any intake.

| Field | Type | Notes |
|---|---|---|
| `id` | enum | Intent · Context · Scope · Requirements · WBS · Schedule · Resources |
| `name` | string | User-facing (WBS → "Work breakdown", D012) |
| `grp` | enum | Understanding \| Execution |
| `basis` | enum | `derived` (From OSLO) \| `attested` (Confirmed by you) — D011 |
| `rel` | enum | Reliability qualifier: High \| Moderate \| Low (D010) |
| `body` | string | Constructed content (Extract from inputs / Infer where thin) |

Rules: every section is constructed even from a thin brief; inferred content defaults to `basis:derived` + reliability-qualified; answering a clarification promotes the tied section to `attested` and bumps `rel` one step (Low→Moderate→High).

### AnalysisRun (D005, D040, D041)
| Field | Type | Notes |
|---|---|---|
| `kind` | enum | `fast` (Initial Analysis) \| `deep` (Extended Analysis) |
| `state` | enum | `provisional` \| `current` \| `error` (last-good) |
| `measuredMs` | number | Fast Pass elapsed, measured not fixed (D036) |
| `read` | ref | → OrientationOutputs snapshot (provisional vs current) |

State machine: `fast → provisional` → `deep` auto-runs → `current` (supersedes) OR `error` (keeps last-good) → retry → `current`.

### OrientationOutputs (D037) — the six Fast Pass outputs
| Field | Type | Notes |
|---|---|---|
| `confidence` | {idx, band, reliability, feasLimit} | Focal score + 5-band + reliability + the-limit dimension |
| `attention` | ref | Initial Attention (heatmap section×CAF) |
| `topIssues` | IssueSummary[] | Ordered by severity |
| `clarifications` | ClarificationRequest[] | Thin-evidence questions |
| `suggestedFixes` | per-issue | Resolution paths inside each issue |
| `analysisStatus` | {state, sectionsDrafted, issuesOpen, clarOpen} | Progress ledger objects |

Read values (illustrative, direction-only per ND-2): provisional idx 58 / Feas Very Low; current idx 62 / Feas Low.

### IssueSummary (D008/D017/D018) — user-facing "Issues"; internal object "Finding"
| Field | Type | Notes |
|---|---|---|
| `id` | string | ISS-01…ISS-06 (prototype); internal `FND-*` |
| `title` | string | |
| `sev` | enum | critical \| moderate \| warning (drives severity color, D003) |
| `dim` | enum | Clarity \| Alignment \| Feasibility |
| `sec` | enum | one of the 7 PlanSection ids |
| `status` | enum | open \| resolved (lifecycle Open→Addressed→Resolved, D018) |
| `why`,`ev[]`,`fixes[]` | | Panel content; evidence pairs |
| `clar` | ClarificationRequest? | Present when the issue rests on thin evidence (D042) |

Rule: issues are never resolved by hand — only reanalysis (here: answering a clarification) moves them (D006).

### ClarificationRequest (D035, D042)
| Field | Type | Notes |
|---|---|---|
| `q` | string | The question OSLO asks |
| `hint` | string | Why it's asked (what's missing) |
| tied-to | IssueSummary.id | Surfaces at orientation AND inside the issue |
| `answer` | string | User-supplied; triggers update → reanalysis → issue close |

## Prototype-local storage (localStorage, `oslo-s1-*` namespace — inherited)
| Key | Purpose |
|---|---|
| `oslo-s1-phase` | alpha \| ga preview |
| `oslo-s1-account` | simulated account {email,name,active} |
| `oslo-s1-staySignedIn` | boolean |
| `oslo-s1-orientSeen` | one-time strategic orientation flag (D027/D039) |

In-session (not persisted): `ANALYSIS_STATE`, `_istatus{}` per-issue status, `PLAN_SECTIONS[].basis/rel` mutations, `DEEP_FAIL` demo flag. These reset on reload — consistent with the prototype's single-session illustrative nature.

## Owner-TBD flags (not assumed)
- Real Time-to-First-MRI NFR (D036) — prototype shows ≈30s illustratively.
- Confidence movement magnitude (ND-2) — direction-only used.
- Real persistence/DB, auth, reanalysis engine — all out of prototype scope (D016).

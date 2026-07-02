# OSLO R1 — UX Prototype: Notes, Decisions & Spec-Gap Audit

**Artifact:** `oslo_r1_experience_mockup_v2.html` (single self-contained file; dark Intralign theme)
**Status:** Working target-experience prototype — **illustrative, not canon.** Structure traces to ratified specs; sample text/numbers are demo data on the DevNorth 2026 sample.
**Date:** 2026-06-30

> This is a design exploration. Per the Authority Constraint, none of this is ratified UX; when the direction is locked it should route through Framework 001 as a UX-revision proposal against `10_product/experience` for owner ratification.

---

## 1. How to resume from here (lock & continue)

- The prototype is **one HTML file** — open it by double-click; edit in any editor. No build step, no dependencies (Google Fonts via CDN, degrades to system fonts).
- To continue in a new session: open this notes file + the HTML; everything needed to pick up is here. Decisions and remaining gaps are in §3–§4.
- The file is the **source of truth** for the prototype. Versioning is whatever you keep in the folder (or commit it to the repo under a `product-design/` path if you want history).
- Nothing here has touched canon — the `10_product/experience` specs are unchanged.

## 2. Decisions captured in the prototype (canon mappings)

| Area | Decision in prototype | Canon source |
|---|---|---|
| Intake | Any readable document (paste/upload); templates optional quick-starts → synthesized into artifacts | Template Intake spec; DL-077 |
| Artifacts | 7: **Intent · Context · Scope · Requirements** (understanding core) + **WBS · Schedule · Resources** (classical-PM execution) | **DL-077** |
| Flow | Fast Pass <60s → **60-second orientation lands on MRI** → **Deep Pass auto-runs** (non-blocking) and supersedes | DL-046; SIXTY_SECOND_ORIENTATION; Canonical Scope §48; Capability Matrix AE-02 |
| MRI | **Heatmap primary** (artifacts × CAF), CAF field secondary | MRI Experience; MRI model (Heatmap) |
| Confidence/CAF | Visual-first, band + **0–100 maturity index** (explainability), neutral ramp — never health; always reliability-qualified | Visual/Brand spec §1.2; Confidence v2; CAFDimensionScore |
| Artifact editor | Flowing prose, type-appropriate (narrative/bullets/tables); **live edit, autosave, event-driven reanalysis** (no explicit edit/save) | Artifact Workspace; Authoring & Editing; AW-03/AE-03 |
| Annotations | **Inline color on the contiguous weak text** (severity ramp); hover summary; click → Finding Panel | Artifact Workspace §G CAF overlays; Finding Presentation |
| Epistemic notation | Per text: **Derived (OSLO)** default; edit/confirm → **Attested (you)** plan fact | DL-043; PlanFact (attested-user); Wave U DTM-0016 |
| Finding panel | Contextual panel (Header→Why→Evidence→CAF impact→Recommendations→History→Reanalysis); can't resolve by hand | **Finding Panel spec (Option A, ratified)** |
| All-findings | Overlay grouped **by CAF dimension, severity-ordered**, filters by dimension/severity; honest "hidden by filters" | Finding Presentation spec |
| Recommendations | OSLO Recommended + Possible Resolution Paths, **selectable → Selected Path** (Attested) | Recommendation Presentation; Finding Panel §J |
| Chat | Global persistent panel + **engage in context** from a finding | OSLO Chat spec; IMPLEMENTATION_PLAN M3 |
| Free tier | UP-3 limit modal — honest, two paths, non-destructive archive | DL-048; Seam Audit; Visual spec §1.3 |

## 3. Spec-vs-UI gap audit — by canonical screen (UI_SCREEN_INVENTORY) + behavior

Legend: ✅ captured · ◐ partial · ⬜ not yet

### Primary screens
| Screen | State | Notes / what's missing |
|---|---|---|
| Project Creation / intake | ✅ | composer + templates + analysis scan |
| 60-Second Orientation | ✅ | lands on MRI; Time-to-First-MRI shown |
| Project Workspace (hub) | ✅ | IDE shell: explorer + center + global panel |
| Artifact Editor | ✅ | prose, type-aware, live edit, inline annotations |
| Analysis Progress | ◐ | intake scan + Deep-Pass banner; no per-run progress/cancel UI |
| Deep Analysis Results | ◐ | auto Deep Pass supersedes; **no distinct results/run-history view** |
| Findings Workspace | ✅ | all-findings overlay + filters + Finding Panel |
| Recommendation Workspace | ◐ | rec tab + in-panel selection; **no standalone Recommendation Panel as a distinct surface** |
| **Dashboard** (multi-project) | ⬜ | v2 is single-project; **no multi-project dashboard / attention feed** |
| **Report Viewer** (view/version/publish/archive/export) | ⬜ | not built |
| **Shared Artifact Viewer** (scoped read) | ⬜ | not built |
| **Notification Center** | ⬜ | not built |
| **User / Workspace Settings** | ⬜ | not built |

### Embedded views
| View | State | Notes |
|---|---|---|
| Confidence Experience (history/trend/CAF drivers) | ◐ | persistent panel + Understanding tab; **no trend/history chart** |
| Explainability panel | ✅ | Finding Panel evidence + CAF impact |
| Activity / Comments thread | ⬜ | no comments/replies/mentions |
| Sharing dialog | ⬜ | not built |

### Behaviors / models not yet reflected
| Behavior | State | Notes |
|---|---|---|
| Reliability **card** with basis (Coverage / Evidence / Assessability) | ◐ | shown only as a qualifier label; no dedicated breakdown |
| Project Overview hierarchy (Header→Confidence→CAF→Reliability→Findings→Recs→Summary) | ◐ | Understanding tab has confidence+CAF; missing Reliability card, Recs summary, Project Summary |
| Overlay **navigation** (next/prev weakness) + "select overlay" focus | ⬜ | Workspace §G interactions |
| Finding **lifecycle** (detected→acknowledged→addressed→closed) + acknowledge action | ◐ | status shown as "detected" only; no transitions |
| **History / timeline** (append-only, closed findings, version lineage) | ⬜ | History nav is a stub |
| Empty-state distinctions (no findings / no overlays / not-yet-analyzed / unavailable) | ⬜ | only the free-tier + empty-second-project states |
| **Apply Suggested Fix** → confidence updates via Deep Pass (REC-04/05) | ⬜ | accept/defer present; no apply-fix flow |
| **Clarification Requests** (finding/flow) | ◐ | chat exists; no explicit clarification object/flow |
| **CAF Review Requests (CRR)** → evidence → Deep Pass (virality loop) | ⬜ | Alpha-scope; not built |
| Confidence **stages** (Orientation→Expanded→Validated, CONF-05) | ◐ | "Preliminary" badges only |
| **False-confidence flag** (CONF-06: high band on low reliability) | ⬜ | in model; not surfaced |
| Understanding **state** (Initial→…→Mature, AE-04) | ⬜ | not surfaced |
| Two-mode onboarding: anonymous first run + **signup = save-to-keep gate after orientation** (DL-073/080); sample-project flag banner | ◐ | intake + "sample" chip; no signup-to-save gate |
| Honest-limit **partial orientation** for over-size Free projects (DL-048) | ◐ | limit modal only |
| Evidence ingestion **in-app** (add more evidence / evidence tray) | ◐ | onboarding attach only |
| Artifact prev/next + hierarchy navigation | ◐ | explorer list; no prev/next |
| Accessibility (WCAG 2.1 AA: focus rings, keyboard nav, reduced-motion) | ⬜ | not addressed in prototype |
| Brand as **token swap** (CSS variables, no hardcoded hex) | ◐ | uses Intralign tokens but hardcoded hex (prototype) |

## 4. Suggested next refinements (priority order)

1. **Reliability card + full Project Overview hierarchy** (closes the headline understanding console gap).
2. **Finding lifecycle + History/timeline** (acknowledge; append-only closed findings) — core to the descriptive model.
3. **Apply Suggested Fix flow** (the improvement-loop "aha": apply → Deep Pass → confidence moves).
4. **Empty states** (the four honest distinctions) + **overlay next/prev navigation**.
5. **Multi-project Dashboard** + **Notification/Awareness**.
6. Collaboration (comments/mentions), Sharing/CRR, Export/Report viewer — Alpha-scope, larger.
7. Accessibility pass + tokenized brand (for build-handoff).

## 5. Anti-Assumption note

The prototype's **structure** is canon-traceable (table §2). The **content** (DevNorth sample text, finding wording, index values 58/64/38/34, severities, filter contents) is **illustrative demo data**, not ratified values. Numeric NFRs (e.g., confidence index, latency p50/p95) remain **owner-TBD** (OPEN_TBD A1/A2) and must not be read as canonical from this mock.

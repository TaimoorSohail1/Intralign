# Deep-task plan — Wave E: Disclose Surfaces (the final phase)

Vertical slices on `feat/phase6-wavee-disclose`. One fresh worker per task, EM review → fix →
verify → approve between tasks. **Coding gated on the Wave E owner authorization (DL-044) +
ideally Wave U (#69) merged** — these files are planning only. Wave E completion = **Release 1
feature-complete** (production deploy stays owner-only).

## Slices (REST-exposure → shell → one surface per slice)

| # | Module | Slice (vertical outcome) | Source | Depends on |
|---|---|---|---|---|
| 1 | **DTM-0018** | **REST exposure:** `api/v1` GET routers + `services/render` mappers presenting the governed objects (Project/Finding/Issue/Recommendation/Confidence/CAF/Outcome/CHR-history/UAR/PlanFact/Acceptance-Impact/Notification) as **Data Model v1.2 DTOs**, read-mostly; OpenAPI regenerates the Orval client; drift gate green | API Contract Spec, ADR-0003, Data Model v1.2 | Waves A–U (the cognition) |
| 2 | **DTM-0019** | **App shell + design system:** TanStack Router tree + MUI `ThemeProvider`/`CssBaseline` (Intralign palette, WCAG AA), `QueryClient` wired to the generated client, and the **reusable epistemic-safety label** (Attested/Derived + band + conflict) every surface uses; Playwright + Vitest set up | UX master, CHG-068, ADR-0010 | DTM-0018 |
| 3 | **DTM-0020** | **MRI** (umbrella) + sub-components MRI-04…07 (Heatmap, CAF Triangle, Understanding Timeline, Understanding Dependencies) | MRI spec, E1 | DTM-0019 |
| 4+ | **DTM-0021…** | one surface each: **Finding Panel** · **Recommendation Panel (RP-C1)** · **Issue Cards** · **Project Overview** (+ Dashboard/Project List) · **Understanding Companion** (route via Finding) · **Notification/Awareness** · **History/Timeline** · **Export/Share-out** · **OSLO Chat** + **Assisted Editing** (AW-04/05) + **honest-limit disclosure** (DL-048) | the per-surface UX specs + E1 | DTM-0019 (+ DTM-0018 endpoints) |

> DTM-0021+ worker contracts are authored **after DTM-0018 lands** — they bind to its concrete
> endpoints/DTOs and the DTM-0019 shell/label component. Each surface is its own vertical slice.

## Test strategy

- **Presentation negatives are the heart (QA-WE-DISCLOSE):** Derived-shown-as-settled; confidence
  overstated (band-edge guard breached); **RP-C1** violation (Recommendation Panel without a
  Finding); Resolution-Path-as-object; **acceptance-by-Disclose**; notification-state-as-canonical;
  export emitting an unsourced claim; **Chat writing canonical / mutating an artifact / changing
  assessment** (Critical). Each surface ships these as component/E2E negatives.
- **Positives:** each surface renders its governed objects with epistemic labels; current + history
  both present; plan facts user-attested; drift/Acceptance-Impact surfaced ≥10pts/band; export
  preserves labels + provenance.
- **Backend (DTM-0018):** pytest positive/negative — render maps cognition→DTO with epistemic
  labels intact; the API is read-mostly (no write/mutation surface on the present endpoints); no
  internal `epistemic.py` type leaks verbatim. ruff + gate-4 + gate-5 green; baseline must not
  regress.
- **Frontend:** Vitest component tests + **Playwright** E2E; `tsc` drift gate green;
  `npm run build` (Gate 1) + `npm audit` (Gate 6) green.

## Manual checks (EM / owner)

- Backend up + frontend `npm run dev` → each surface loads against live data; epistemic labels
  visible; Recommendation Panel only reachable from a Finding; accept affordance routes to the
  Wave U capture (records a UAR + plan fact) — Disclose itself writes no cognition.
- Studio/API: the present endpoints return DTOs only (no canonical mutation from the read surface).

## Done = Wave E complete (Release 1 feature-complete)

All surfaces present the cognition chain + acceptance with enforced epistemic-safety labeling and
current+history; Disclose proven to generate nothing and change no assessment; OSLO Chat
no-canonical-write proven; honest-limit disclosure present. → **Owner exit-gate = Release 1
production-readiness review** (production deploy remains owner-only).

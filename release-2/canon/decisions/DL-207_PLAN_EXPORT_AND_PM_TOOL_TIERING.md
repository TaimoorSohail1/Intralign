# DL-207 — Plan export & PM-tool integration: file export = Free, one-way push = Basic, two-way sync + monitoring = Pro (R2, staged)

- **Date:** 2026-08-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console) · **Class:** B (product scope / monetization *placement* — non-doctrinal)
- **Framework 001** — AI drafts; only the owner ratifies. AI does not author canon; this record is a proposal.
- **Basis:** owner working session 2026-08-09 (the export-capability build). The owner directed a real, multi-format file export and a **Basic, one-way** push to a PM tool, correcting an initial "auto-sync" framing.
- **Extends / realizes:** **DL-206** §2 ("auto-import + two-way sync → Pro; Basic retains manual/one-shot connection: plan export → execution tool") and §4 ("Free: export a file"); **DR-7** (pricing); **DL-083** (execution-tool connection capabilities). It adds no new tier boundary — it makes DL-206's placement concrete for the *export / PM-tool integration* surface and specifies the file-format set DL-206 left open.
- **Placement:** staged in `release-2/` (R2 copy-of-record); **withheld from `main` until R1 graduation**, consistent with the DL-172 / DR-7 / DL-206 staging posture. No R1/Alpha canon (≤ DL-156) touched.

---

## Decision

**Organizing axis (from DL-206):** Free = you move the file; Basic = one-way, on-demand push (the user still drives updates); Pro = automated + bi-directional (the system drives them).

1. **Export a file → Tier 1 / Free.** The user downloads the executable plan (task · owner · dates · **provenance** · note) in the format of their choice — **CSV, Excel (.xlsx), plain text, and a PDF package** — dated, carrying the advisory disclaimer. They import it into Asana or any tool themselves. Export runs **no new analysis** (a projection of the governed read). This realizes DL-206 §4 and fixes the format set. *(Not metered — moving your own plan out is never a paywall.)*

2. **One-way push / import into a PM tool → Tier 2 / Basic.** OSLO pushes the plan **into** Asana (and other PM tools) so the user can **view** it there — a one-shot / on-demand connection, replacing the manual download-and-import. It is **one-way**: updates stay authoritative in OSLO; the user re-pushes to reflect later changes. This realizes DL-206 §2's "manual/one-shot connection: plan export → execution tool (DL-083 cap 2)." **It is not "auto-sync" and must never be presented as bi-directional.**

3. **Two-way sync + execution monitoring → Tier 3 / Pro+** (Team/Enterprise inherit). Bi-directional synchronization between OSLO and the PM tool, plus continuous/automated execution-stage monitoring of actuals against the plan. Adopts DL-206 §1 (continuous monitoring = Pro) and §2 (two-way sync = Pro). Eases — does not close — Pro's PROVISIONAL price (DR-7); **final Pro price stays OPEN**.

## Doctrine preserved (unchanged)

Freemium gates **capacity / automation** (the push, the sync, the monitoring) — **never** judgment quality, the record, reviewers, or Viewers (DL-103 §1, DL-102). The **file export and the accuracy bar are free on every tier** — one accuracy bar for all. What crosses to the PM tool is the **executable plan only**; OSLO keeps the plan of record. No forecast / probability of success (D003/D183b). Flat per-account, never per-seat (DR-7). Export carries the D153 advisory disclaimer (maturity, not a success prediction).

## Terminology (routes to the DL-053 register)

Canonical, per surface: **export a file** (Free) · **push / one-way import** (Basic — view-only in the PM tool) · **two-way sync** + **continuous / execution-stage monitoring** (Pro). **"Auto-sync" is prohibited copy for Basic.** Exact terms are the owner's DL-053 call.

## Phase / build

The **file export is realized now** (R2 prototype: CSV/Excel/text are real client-side downloads; PDF is a simulated package). The **PM-tool push (Basic) and two-way sync + monitoring (Pro) are Beta / post-R2** — registered as backend obligation **#24** in `OSLO_BACKEND_CAPABILITIES.md` (server-side .xlsx/PDF generation + PM-tool APIs). No R2 freemium-build change beyond the export UI (DL-172 §5).

## Open (non-blocking)

Final Pro price; exact DL-053 terms; which PM tools beyond Asana at launch; whether the Basic one-way push needs a distinct product name; land-to-`main` timing (at R1 graduation, with the other R2-staged DLs).

## Affected artifacts

`OSLO_BACKEND_CAPABILITIES.md` #24 · `oslo-prototype-r2.html` (export modal) · at graduation: `RELEASE_1_TIER_DEFINITIONS_V1` (export/integration rows), `CANONICAL_GLOSSARY` DL-053 register, and the DR-7 pricing page. Relationship: **realizes DL-206**, **extends DR-7 / DL-083**.

---

_AI-drafted (Framework 001); **ratified by the owner 2026-08-09**. Realizes DL-206; staged in `release-2`, folds into `main` at R1 graduation with the other R2-staged DLs._

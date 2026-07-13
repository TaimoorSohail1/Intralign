# Work Item WI-R1 — Strategic Readout composer (Reports surface upgrade)

**Opened:** 2026-07-12 · **Type:** Prototype / Product Design (Reports surface) · **Status:** REOPENED — In review (pending owner re-signoff)
**Slice:** 10 — Tiering & Limits → **Reports surface** (the surface added in the DL-103 fold-in). Reporting has no standalone numbered slice; it rides in Slice 10.
**Realizes (ratified canon):** **DL-107** (Reporting spec commission + readout spine) · **DL-108** (tailor the ASK, never the READ — merged to `main` 2026-07-12, PR #149) · **DL-104** (P1 health-framing / overclaim defect classes).
**Non-ratifying.** AI-authored work item; owner ratifies scope and signs off. `RELEASE_1_REPORTING_SPECIFICATION_V1` remains authoritative on reporting.

---

## Why this reopens a signed-off surface

Slice 10 signed off 2026-07-12 with a Reports surface (nav + modal + `REPORTS` registry; reliability-qualified; currency-marked; standing disclaimer; **packages, never produces**; `reportsNoHealth` boot guard). That surface predates two things:
1. **DL-107's readout spine** — the "So what · How do we know · What now" five-section memo structure (§1 the read · §2 what's limiting it · §3 what we don't know · §4 what I need from you · §5 how to read this).
2. **DL-108** — *tailor the ASK, never the READ*: §1–§3 identical for every audience; only §4 addressed to the recipient. Ratified **after** Slice 10 sign-off, so the current Reports surface does not yet encode it.

This is an **enhancement of an existing surface**, not a contradiction: it is additive over "packages-never-produces / no-health," which it preserves.

## Design input (already built, verified)

`OSLO Knowledge Base/oslo_r1_experience_mockup_v5_readout_DRAFT.html` — a **non-canonical** copy of `product-design/oslo_r1_experience_mockup_v4.html` where **only the export surface** was upgraded into the Strategic Readout composer. Reference v4 untouched.
- Assembles the five-section spine **live** from `FINDINGS` (confidence band + reliability, limiting dimension + sharpest issue, inferred/unvalidated items + open clarifications, audience-tailored ask, reliability/currency/derived-attested footer).
- **Verified (headless Chromium):** switching Practitioner → Sponsor → Executive leaves §1–§3 and §5 **byte-identical**; only §4 changes. 0 JS errors. Optional sections (Alignment · Unvalidated assumptions · How understanding matured · Artifact detail) render.

## Acceptance / success criteria

1. Reports surface renders the DL-107 five-section spine, assembled from existing understanding (no new analysis on generate — **packages, never produces**).
2. **DL-108 binding enforced in code:** §1–§3 (+§5) are audience-independent; only §4 reads the audience. A visible statement of the rule + citation.
3. **P1 guards (DL-104):** the read carries the explicit "not health / RAG / readiness / probability of success" line; derived ("From OSLO") never dressed as attested ("Confirmed by you"); analysis-currency marker on every snapshot; stale = "previous analysis."
4. Free = the read snapshot (§1–§5, PDF); Basic = composable + optional sections + branding + scheduling (per DL-103 §7 tiering; **the seed is never gated**).
5. Report **names** stay owner/glossary (DL-053) — labelled descriptively, "naming pending"; avoid "status report" / any health-or-readiness implication (DL-104 P1).
6. New boot guards to add alongside existing `reportsNoHealth`: `readIdenticalAcrossAudience` · `readoutRunsNoAnalysis`.

## Explicitly OUT of scope (guardrails — deferred/foreclosed by canon)

- Cognitive-event / "Understanding Debt" feed → **R2-F / AE-06** (deferred).
- Assumption *validated/invalidated* lifecycle, re-validation prompts, "which assumptions failed" → **RB-017** (backlog, not ratified; PR #150). The optional "Unvalidated assumptions" section is **presentation-only** — no lifecycle.
- Cross-project / portfolio pattern call-outs → **Future Architecture / R2-E** (out of R1; DL-034 Provisional).
- Uncertainty / Trade-off as first-class objects → **foreclosed** (Epistemic State Model: "represented, not stored").
- Audience-reframed *reads* → **forbidden** by DL-108.

## Worker task (to delegate — not done in main session)

Fold the readout composer into `vertical-slices/slice-10-tiering-limits/prototype.html` (replace/extend the existing Reports modal), preserving all prior Slice-10 routes/guards/theme; add the two boot guards; update `product-detail.md`, `frontend-ui.md`, `user-experience.md`, `success-criteria.md`, `e2e-test-scenarios.md`, and `open-items.md` for the Reports surface. Cumulative-prototype rule applies. Re-run the Slice-10 verification battery + the new guards.

## Owner decision requested

- **Reopen Slice 10 Reports surface to fold in DL-107 + DL-108?** Recommended: **yes** — DL-108 is ratified and the current surface doesn't encode it; the design input is built and verified. On approval, delegate the worker task and require re-signoff of the Reports portion of Slice 10.

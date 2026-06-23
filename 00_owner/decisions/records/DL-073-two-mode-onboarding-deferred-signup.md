# DL-073 — Two-mode stage-conditioned onboarding (deferred-signup) + save-to-keep signup trigger

- **Date:** 2026-06-19 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction 2026-06-18 (two distinct core experiences: first-time vs resume); signup-trigger decided after a PLG best-practice review (delay the wall until after first realized value); the 2026-06-18 onboarding / Time-to-First-MRI review (the §V first-time-journey gap). Supporting analysis: `PROPOSAL_TWO_MODE_ONBOARDING_DEFERRED_SIGNUP_DRAFT.md`.
- **Layer:** Product experience (10_product). Amends ratified onboarding conformance **OB-C1**. No doctrine or constitution change.

## Decision
1. **Two-mode onboarding adopted.** First-time = **ingestion-first, deferred-signup**: account, authentication, workspace initialization, and project creation are **auto-provisioned with no user action**; the user goes arrive → add artifact → analysis → 60-second orientation. Resume = **auth-entry** (returning users sign in and land on their work). **Ingestion-first landing invariant:** when there is nothing to resume (first-time, or signed-in with zero projects), the landing surface is the **ingestion screen** — not an empty-workspace placeholder; when there is work to resume, the user lands on it (project list / last orientation state).
2. **Release-stage conditioning.** Alpha/Beta (controlled access) = a **front auth gate** (invite/allowlist) → the ingestion landing. GA (open access) = **no front gate**; new users **sign up or start immediately**. The auth-gate position is **release-stage config**, not hard-coded; the empty→ingestion / has-work→resume landing logic is **stage-invariant**.
3. **Signup trigger (GA) = save-to-keep.** The full first run — ingestion → analysis → 60-second orientation → explore — is **anonymous**; sign-up is required only to **save/persist** the project (claimed on sign-up), placing the gate **immediately after the aha** (the 60s orientation) per PLG best practice. **Paired with a light anonymous-usage cap** (a thin slice of the DL-048 free-tier envelope) to bound anonymous compute cost/abuse. **Deep Pass is the later upgrade gate** (Fast Pass free, Deep behind sign-up/paid), not the initial sign-up gate.
4. **Invariants preserved.** No change to the §T integrity rules / OB-1 / OB-5 (onboarding computes/generates/governs nothing; only reanalysis changes assessment), epistemic safety / no-fabricated-assessment, or the DL-046 Time-to-First-MRI definition (Fast-Pass latency, Analysis Initiation → Orientation).

## Phasing (ratified for build now vs GA)
- **Now (Alpha/Beta):** the auth-first → ingestion-landing model + the stage-invariant landing logic are ratified for build; **no anonymous-identity machinery required** (Alpha/Beta runs authenticated).
- **Before GA:** the deferred-signup + save-to-keep model, conditioned on engineering proposals for (a) provisional/anonymous identity → persistence → claim-on-signup; (b) DL-048 pre/post-signup gating + the anonymous-usage cap; (c) pre-signup data retention & privacy. Owner ratifies intent; engineering authors realization (ratify ≠ author).

## Realization (follow-on)
Amend `10_product/experience/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` §D, §E, §G, §H, §I, §S and conformance **OB-C1** to the two-mode, stage-conditioned model. Engineering proposes the provisional-identity / persistence / claim-on-signup data model (GA).

## Supersedes / Amends
Amends the onboarding spec's conformance **OB-C1** (which mandated "New User → Account Creation → Workspace Initialization → …" as the journey) and §D/§E/§G/§H/§I/§S. Reconciles with DL-046 (60s unchanged), DL-048 (tier/freemium — the anonymous cap + Deep-Pass upgrade gate), and DL-056 (templates — a template start is the ideal friction-free first artifact). No doctrine or constitution content superseded; epistemic-safety invariants preserved.

## Provenance
Owner decision via the Founder Console / working session, 2026-06-18. Drafted by AI under Framework 001 (proposal → owner ratification); the signup trigger was selected by the owner after a PLG best-practice review. AI drafted and recommended; the owner ratified. Numbered at landing under the DL-065 records discipline.

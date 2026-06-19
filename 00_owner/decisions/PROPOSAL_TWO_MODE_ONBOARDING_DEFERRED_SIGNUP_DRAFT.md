# PROPOSAL — Two-Mode Onboarding: Deferred-Signup First-Time Experience + Auth-Entry Resume

- **Status:** **Owner-ratified (intent), 2026-06-18.** Two-mode stage-conditioned onboarding adopted; signup trigger decided = **save-to-keep** (§4.1). Formalized as a Decision (DL) record landing alongside this proposal. Spec amendment + GA engineering items (§4.2–4.4) are realization follow-ons. AI-drafted; owner ratified.
- **Framework 001 stage:** Proposal.
- **Class:** Product-experience amendment (10_product). Amends a ratified UX spec; routes through Framework 001.
- **Amends:** `10_product/experience/ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` — §D (Experience Architecture), §E (Account Creation), §G (First-Time UX), §H (Workspace Initialization), §I (Project Creation), §S (Progressive Disclosure), and conformance **OB-C1**. §F (Authentication) and §P (Returning User) are largely preserved (auth becomes the resume entry).
- **Source:** Owner direction, 2026-06-18. Builds on the latent gap surfaced in the 2026-06-18 onboarding/Time-to-First-MRI review: the current spec budgets only the post-analysis 60s (Time-to-First-MRI) and leaves the first-time onboarding overhead (account → auth → workspace → project) unbudgeted (§V).

---

## 1. Proposed change — two distinct core experiences

The Release 1 onboarding splits into **two modes**, by user type:

**Mode 1 — First-Time User (deferred signup / understanding-first).**
The user is greeted with a screen that lets them **immediately ingest a project** (upload / paste / combine / template) — no account, sign-in, workspace setup, or manual project-creation step in front of value. **Account creation, authentication, workspace initialization, and project creation happen automatically, system-side, with no action required by the user.** The user goes straight: *arrive → add artifact → analysis → 60-Second Orientation*. **Signup is deferred** to a later point in the value path (see Decision 1). Pattern reference: Lovable and similar "vibe"/PLG tools — value first, identity later.

**Mode 2 — Resuming User (auth entry).**
A returning user **enters via authentication**, signs in, and lands on their workspace / project list (or the orientation state a project was in), per the existing §F/§P behavior.

This **inverts the current §D/OB-C1 ordering** (which puts Account Creation first and discloses "create account → create project → add artifact") for first-time users, while keeping the resume path auth-first.

## 1a. Release-stage conditioning (Alpha/Beta controlled access → GA)

The deferred-signup model is **release-stage-aware** (Alpha/Beta vs GA — the canonical product lifecycle, Master Spec §19/§20; Alpha graduation metrics gate the progression):

- **Alpha / Beta — controlled access:** sign-up and authentication **are required up front** (they are the **access-control gate** for invite/allowlist-limited access — not an onboarding-philosophy choice). **But upon sign-up/sign-in the user lands directly on the ingestion page** — the ingestion-first landing already applies; only the front auth gate differs.
- **GA — open access:** sign-up and authentication are **removed as first steps**. Every new user can **either sign up or immediately ingest a project** (the full deferred-signup Mode 1). The access-control gate is gone, so identity can be deferred.

**The invariant across both stages is the ingestion-first landing.** The **variable is the position of the auth gate** — a front gate during controlled-access Alpha/Beta, deferred/optional at GA. This should be **read from release-stage config, not hard-coded** (mirroring the tier-keyed config principle in the glossary: "do not hard-code … read it from config").

**Sequencing benefit (de-risks the build):** the **provisional/anonymous-identity machinery (Decision 2 below) is only required at GA.** Alpha/Beta runs fully **authenticated**, so it ships the simpler "auth gate → ingestion page" with **no anonymous-session or claim-on-signup work**. The signup-trigger (Decision 1) likewise only applies at GA (signup is upfront during Alpha/Beta). So Alpha/Beta is buildable now; the GA decisions can land before GA.

## 1b. Permutation matrix (release stage × identity state)

**Ingestion-first landing — clarified invariant.** When a user has **nothing to resume** (a first-time visitor, or a signed-in user with zero projects), the landing surface is the **ingestion screen itself** — never an empty-workspace placeholder that gates ingestion behind a "Create project" click. When a user **has work to resume** (≥1 project), they land on it (project list / last orientation state, §P). This **removes the §G/§R empty-workspace step** for the empty case; it does not force ingestion on returning users.

| Identity state | Alpha / Beta — controlled access | GA — open access |
|---|---|---|
| **First-time visitor** | **Auth gate** — invite/allowlist sign-in required, *then* the ingestion page | **No gate** — sign up *or* start now → straight to ingestion |
| **Working anonymously** (pre-signup) | **n/a** — no anonymous sessions; everyone is authenticated | **Ingestion** — ingest → analyze → 60s orientation; signup deferred; project claimed on signup |
| **Signed in, no projects** | **Ingestion** — lands on the ingestion page (not an empty workspace) | **Ingestion** — same |
| **Returning, has projects** | **Resume** — project list / last orientation state | **Resume** — same |

**Orthogonality + sequencing.** The *release-stage* column governs **access** (the front auth gate + whether anonymous sessions exist); the *identity-state* row governs **where the user lands**. The **bottom two rows are stage-invariant** — that landing logic is the part **ready to amend now** (it holds for Alpha/Beta and GA alike, needs no anonymous-identity work). Only the **top row's GA cell** and the **anonymous row** depend on the GA decisions (signup trigger §4.1, provisional identity §4.2).

## 2. What this preserves (invariants — unaffected)

The change is **friction removal, not analysis behavior**. It does **not** touch:
- §T Integrity Rules / OB-1 / OB-5 — onboarding still **computes nothing, generates nothing, governs nothing**; only reanalysis changes assessment.
- Epistemic safety and the no-fabricated-assessment rule (§Q failure states).
- The 60-Second Orientation / Time-to-First-MRI definition (DL-046) — still the Fast-Pass latency from Analysis Initiation → Orientation.
- "Minimum-to-value = project name + one artifact" (now satisfiable without the user ever seeing an account/workspace/project-creation step, since those are auto-provisioned).

## 3. Why (rationale)

- **Realizes the spec's own philosophy** (§C): "remove everything between a user and their first understanding." Auto-provisioning the identity/workspace/project scaffolding is the logical endpoint of "onboarding is lightweight, skippable, straight to project creation" (§G).
- **Closes the §V first-time-journey gap.** With account/workspace/project friction removed, the first-time wall-clock to value is bounded by *ingestion + the 60s Fast Pass* — not by setup. The earlier "no end-to-end first-time budget" concern is largely dissolved by design.
- **Conversion economics:** value-first / deferred-signup is the dominant PLG pattern for tools of this class; it raises first-session activation by letting users reach the orientation before committing identity.

## 4. Owner Decisions Required (open — escalated, not assumed)

These are underspecified by the direction and are the owner's to settle; the proposal does **not** invent answers. **Note (per §1a): Decisions 1–4 are GA-phase** — Alpha/Beta ships auth-first → ingestion-landing and needs none of them.

1. **[GA] Signup-trigger point — DECIDED (owner, 2026-06-18): save-to-keep.** The user reaches ingestion → analysis → **60-second orientation** → explore **fully anonymously**; sign-up is required only to **save/persist** the project beyond the session (claimed on sign-up). This places the gate **immediately after the aha moment** (the 60s orientation), per PLG best practice (delay the wall until after first realized value). **Dependency:** pair with a **light anonymous-usage cap** (e.g., one free project/analysis or a rate-limit — a thin slice of the DL-048 free-tier envelope) to bound anonymous compute cost/abuse. **Deep Pass** is reserved as the later **upgrade** gate (Fast Pass free, Deep behind sign-up/paid), **not** the initial sign-up gate. *(GA items 2–4 below remain open.)*
2. **Provisional identity & data model (product ↔ engineering seam).** Auto-provisioning an account+workspace+project "without user action" implies a **provisional/anonymous session** that is later **claimed** at signup. How it is represented, **persisted, secured, and migrated-on-claim** is engineering realization (data model, identity, retention) — currently under the §V deferred "permissions/identity architecture, database design." Owner ratifies the **intent**; engineering **proposes the realization** (ratify ≠ author).
3. **Tier/freemium gating pre- vs post-signup (DL-048).** What is available anonymously (Fast Pass? Deep Pass? how many projects?) vs gated behind signup?
4. **Pre-signup data retention & privacy.** How long is an unclaimed anonymous project retained; what is the security boundary before identity exists; what happens if it's never claimed.

## 5. Framework 001A Review

- **Findings:** the direction is a coherent two-mode model that inverts first-time identity ordering while preserving the resume path; it is consistent with §C philosophy and resolves the §V first-time-budget gap; it amends §D/§E/§G/§H/§I/§S/OB-C1.
- **Concerns:** the **signup-trigger** and the **provisional-identity/persistence/security** model are unspecified and load-bearing — the experience cannot be conformance-defined without them. Auto-provisioning touches the §V-deferred identity/permissions/data-model architecture (product↔engineering seam) and the DL-048 tier model; these must move in concert. No epistemic-safety/integrity invariant is threatened.
- **Dependencies:** DL-046 (60s, unchanged); DL-048 (tier/freemium envelope — gating + signup gate); DL-056 (templates — a template start is the ideal friction-free first artifact); the §V-deferred identity/permissions/data-model work (engineering); SIXTY_SECOND_ORIENTATION + ORIENTATION_STATE_MODEL (unchanged).
- **Recommendation:** **adopt the two-mode, stage-conditioned intent** and amend §D/§E/§G/§H/§I/§S + OB-C1 in **two phases**: (1) **now — Alpha/Beta**: auth gate (controlled access) → **ingestion-first landing**, resume = auth-entry; no anonymous-identity work. (2) **before GA**: drop the front auth gate → full deferred-signup Mode 1, conditioned on Decision 1 (signup trigger) and an engineering proposal for Decision 2 (provisional identity/persistence/claim). Make the auth-gate position **release-stage config**. I recommend only; owner ratifies.
- **Status:** Alpha/Beta portion ready for owner ratification + spec amendment now; GA portion pending Decision 1 + delegation of Decision 2.

## 6. Owner decision required (summary)

1. Ratify the **two-mode intent** (deferred-signup first-time + auth-entry resume)?
2. Set the **signup trigger** (Decision 1 options above).
3. Authorize an **engineering proposal** for provisional identity / persistence / claim-on-signup (Decision 2), and the DL-048 pre/post-signup gating (Decision 3) + retention/privacy (Decision 4).
4. On ratification, the canonical amendment to `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1` routes through Framework 001 (proposal → owner-ratified change → changelog), and likely an owner Decision (DL) given it supersedes ratified conformance OB-C1.

# Account & Workspace Settings Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Consistent with and subordinate to (authoritative — must not redefine):** `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1.md` · `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` · `MRI_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_WORKSPACE_SPECIFICATION_V1.md` · `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW_SPECIFICATION_V1.md` · `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · Release 1 Tier Definitions.

> **Non-negotiable constraints.** This specification defines **UX architecture, settings experiences, preferences experiences, and workspace management experiences only**. It must **NOT** define: governance workflows, execution workflows, automation, agents, APIs, events, implementation, styling, permissions architecture, billing implementation, or subscription implementation.
>
> **The experience presents settings. It computes nothing. It generates nothing. It governs nothing.**
>
> **Preserved invariants.** Settings never touch project understanding: artifacts remain the source of truth, findings descriptive, recommendations advisory, MRI the diagnostic discovery experience, and **only reanalysis changes assessment**. Settings change **preferences and account/workspace information**, never assessment.

---

## A. Purpose

Define the canonical Release 1 **Account & Workspace Settings Experience** — how a user manages their account information, profile, workspace preferences, project defaults, notification preferences, collaboration preferences, and the **visible** state of subscription, billing, integrations, and workspace membership. It answers:

> **"How does a user manage their OSLO account and workspace?"**

Settings is the **management periphery** of the product — deliberately separate from the understanding center of gravity. It lets users adjust how OSLO works **for them** without ever altering project understanding or assessment.

## B. Scope

**In scope:** the UX of account settings, profile settings, workspace settings, project default settings, collaboration preferences, notification preferences, and the **read/visibility** experiences for subscription, billing, integrations, and workspace membership; plus empty states, failure states, and progressive disclosure across settings.

**Out of scope (explicitly):** governance/execution workflows; automation; agents; APIs; events; implementation; styling; **permissions architecture** (logic/enforcement); **billing implementation** and **subscription implementation** (payment/plan-change processing); and any computation (scoring / CAF / Reliability / Confidence) or generation. The experience **presents and edits settings**; it processes no payments, enforces no permissions, and changes no assessment.

## C. Settings Philosophy

Settings exists to let users **manage their account and workspace** — not to manage projects, govern work, or coordinate execution. It is the **calm periphery**: low-stakes, reversible, clearly scoped preference and account management that keeps **project understanding untouched**. Settings **presents** plan/billing/integration/membership information for **visibility and transparency**, and **edits** the preferences a user legitimately owns (profile, workspace name, defaults, notifications, collaboration preferences). It **computes nothing, generates nothing, governs nothing**, and never becomes a surface for assessment, findings, recommendations, or governance.

## D. Experience Architecture

A single **Settings surface** organized into clearly separated areas, reached from a consistent entry point and kept apart from the understanding workspaces:

```text
Settings
 ├─ Account          (identity & security visibility)
 ├─ Profile          (how the user appears)
 ├─ Workspace        (workspace name & defaults)
 │    └─ Project Defaults
 ├─ Collaboration    (sharing & invite preferences)
 ├─ Notifications    (awareness preferences)
 ├─ Subscription     (plan — visibility)
 ├─ Billing          (billing — visibility)
 ├─ Integrations     (visibility; configurability per §M)
 └─ Workspace Membership (who's in the workspace — visibility)
```

**How a user accesses settings (Q1):** from a consistent, always-available entry point (e.g., the account/workspace menu), settings opens as its own surface — **never overlaying or altering** the Project Overview / MRI / Artifact workspaces. Each area has **purpose, visible information, allowed actions** (edit vs. view-only), and empty/failure states. Editable areas save **preferences/account info only**; visibility areas are **read-only presentations** in Release 1.

## E. Account Settings Experience (Q2)

- **Purpose:** manage core account identity and see security state.
- **Editable account information (resolved):** the user's **account email/identity contact** and basic account fields the product owns (per the account mechanism). Editing updates account information only.
- **Password / security visibility (resolved):** security state is **visible** (e.g., that a password/auth method is set, last-changed indication) with an entry point to **change password / manage security** — presented as a user-facing affordance; the **mechanism is out of scope** (no auth/permissions architecture, §T).
- **Account deletion visibility (resolved):** account deletion is **visible** as an available, clearly-labelled, **confirmation-gated** action (a path to delete/close the account). Its **processing/implementation is out of scope** (§T); the experience presents the option honestly rather than hiding it.
- **Allowed actions:** edit account fields; enter the security/password flow; initiate account deletion (confirmation-gated).

## F. Profile Settings Experience (Q3)

- **Purpose:** manage **how the user appears** to themselves and collaborators.
- **Editable profile fields (resolved):** **display name**, optional **avatar/photo**, and optional lightweight profile descriptors (e.g., role/title) — all descriptive, all optional except a display name for identification.
- **Allowed actions:** edit display name; add/change avatar; edit optional descriptors.
- **Constraint:** profile is **presentation of the person**; it drives no permissions, no computation, no governance.

## G. Workspace Settings Experience (Q4)

- **Purpose:** manage the workspace that holds the user's projects.
- **Workspace naming (resolved):** the **workspace name is editable** — the primary workspace setting.
- **Workspace branding (resolved):** lightweight branding (e.g., a workspace **logo/avatar**) is **optional**; full branding/theming is **deferred** (§T) and **no styling** is defined here.
- **Default project settings (resolved):** the workspace exposes **default project settings** (§H) that pre-fill new project creation — convenience defaults only.
- **Allowed actions:** edit workspace name; set optional workspace avatar; manage project defaults (§H).

## H. Project Default Settings Experience (Q5)

- **Purpose:** configure **defaults** applied when creating new projects (consistent with the Onboarding/Project Creation spec, where type/workflow are optional and name is required).
- **Configurable project defaults (resolved):** optional **default project type** and **default workflow type** (pre-fills only; still optional at creation), and optional default collaboration/sharing preference (§I). Defaults **never gate** project value (name + one artifact remains the minimum).
- **Allowed actions:** set/clear defaults.
- **Constraint:** defaults are **convenience pre-fills**; they configure no computation, generation, or governance, and never override the onboarding minimum-to-value.

## I. Collaboration Preferences Experience (Q6)

- **Purpose:** set the user's/workspace's **collaboration preferences**, consistent with `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`.
- **Default sharing behavior (resolved):** the default is **private / not shared** — a new project is not shared until the user shares it; the user may change this default preference.
- **Invite preferences (resolved):** preferences for how invites are presented/sent (e.g., default participant type suggested on invite) — **presentation preferences only**, not permission logic.
- **Notification defaults for collaboration (resolved):** sensible defaults (e.g., notify on mentions and direct replies) that the user can adjust (§J).
- **Constraint:** these are **preferences**; they enforce no permissions and perform no governance. Comments still never change assessment/findings/recommendations (that invariant lives in the collaboration spec).

## J. Notification Preferences Experience (Q7)

- **Purpose:** let users control **awareness** preferences (consistent with the collaboration spec's awareness model — mentions, replies, new comments, shared-project activity).
- **Notification preferences (resolved):** per-category toggles for **mentions, replies, new comments, and shared-project activity**, with sensible defaults.
- **Allowed actions:** enable/disable categories; set defaults.
- **Constraint:** preferences are **presentation only** — **no notification/delivery infrastructure, no event definitions** are defined here (§T). The experience presents the choices; delivery mechanics are out of scope.

## K. Subscription Experience (Q8, Q12)

- **Purpose:** make the user's **plan and limits visible** (per Release 1 Tier Definitions) — transparency, not transaction.
- **Plan visibility (resolved):** the **current plan/tier is visible**.
- **Usage visibility (resolved):** **usage relative to the plan is visible** (e.g., projects used vs. allowed) — presented as **plan information**, not as any assessment/score.
- **Project limits visibility (resolved):** **plan limits (e.g., project limits) are visible** (Q12), shown as plan facts.
- **Allowed actions (Release 1):** **view** plan, usage, and limits; an entry point to **manage/upgrade** may be presented, but **subscription processing/implementation is out of scope** (§T) — Release 1 is **visibility-first**.
- **Constraint:** no billing/subscription **implementation**, no computation; figures shown are plan information, not computed scores.

## L. Billing Experience (Q9)

- **Purpose:** make **billing information visible** — transparency only.
- **Billing visibility (resolved):** the user can **view** relevant billing information (e.g., current plan's billing status, billing contact, invoices/history **as presented**).
- **Allowed actions (Release 1):** **view** billing information; an entry point to **manage billing** may be presented, but **billing implementation/payment processing is out of scope** (§T).
- **Constraint:** **no billing implementation**, no payment processing, no computation defined here — Release 1 billing is **visibility-first**.

## M. Integrations Experience (Q10)

- **Purpose:** present integrations transparently.
- **Whether integrations appear in Release 1 (resolved):** integrations **may appear as a visible area** showing available/connected integrations — **visibility-first**.
- **Whether integrations are configurable in Release 1 (resolved):** integrations are **view-only / not configurable in Release 1** — connecting/configuring/automating integrations is **deferred** (§T). No APIs, events, automation, or agent behavior are defined here.
- **Allowed actions (Release 1):** **view** the integrations area and connection status; configuration is deferred.

## N. Workspace Membership Experience (Q11)

- **Purpose:** **display** who is in the workspace (consistent with the collaboration spec's participant types).
- **How team members are displayed (resolved):** members are **listed with their user-visible participant type** (Project Owner / Collaborator / Viewer) — **presentation only**.
- **Allowed actions (Release 1):** **view** membership; invite/share affordances live in the collaboration experience (referenced, not redefined). **No permission logic/architecture** is defined here.
- **Constraint:** membership display is **presentation only**; it enforces nothing and governs nothing.

## O. Empty States (Q13)

The experience must **distinguish**:

- **No optional profile/workspace info set** — neutral "add details" states (e.g., no avatar, no workspace logo).
- **No collaborators / solo workspace** — membership shows just the owner ("invite people to collaborate").
- **No integrations connected** — a neutral "no integrations connected" state (distinct from "integrations unavailable").
- **No billing/subscription information available** — distinct from "unavailable."
- **Unavailable** — a settings area is **temporarily unavailable**, distinct from "empty/none."

## P. Failure States (Q14)

Failures are **honest and recoverable**; settings never corrupt account/workspace state silently:

- **Save fails** (account/profile/workspace/defaults/preferences): the experience **reports the failure**, **retains the prior saved values**, preserves the user's unsaved input, and offers **retry** — no silent loss, no partial save presented as complete.
- **Visibility data unavailable** (subscription/billing/integrations/membership): the area shows an **"unavailable — try again"** state rather than blank or fabricated data; **no figures are invented**.
- **Security/deletion action fails:** clearly reported, with the account left in a known, safe state and a retry path; destructive actions remain **confirmation-gated** and never proceed ambiguously.
- **General principle:** account/workspace state is never silently changed; nothing is fabricated; the user always knows whether a change saved.

## Q. Progressive Disclosure

- **Immediately visible:** the settings areas (Account, Profile, Workspace, Collaboration, Notifications, Subscription, Billing, Integrations, Membership) as a clear, separated index.
- **In context:** each area's editable fields or read-only information.
- **Through expansion:** advanced/optional fields, security flow, deletion (confirmation-gated), invoices/usage detail.
- **Intentionally absent:** any project-understanding surface (findings/recommendations/CAF/MRI); scores/computed metrics; governance/approval/execution affordances; automation/agents; permission-enforcement, billing-processing, or integration-configuration logic (Release 1).

## R. Integrity Rules

- **SET-1.** Settings **computes nothing** (no CAF / Reliability / Confidence / scoring).
- **SET-2.** Settings **generates nothing** (no findings / recommendations / assessment).
- **SET-3.** Settings **governs nothing** — no governance/approval/decision workflow.
- **SET-4.** Settings introduces **no execution, automation, or agent** workflow.
- **SET-5.** Settings **never touches project understanding** — artifacts/findings/recommendations/MRI/assessment are untouched; **only reanalysis changes assessment** (and that lives elsewhere).
- **SET-6.** Editable areas change **preferences and account/workspace information only**; visibility areas (subscription, billing, integrations, membership) are **read-only in Release 1**.
- **SET-7.** Subscription, billing, usage, and limits are **plan information presented for visibility** — **not** computed scores; **no billing/subscription implementation** is defined.
- **SET-8.** Integrations are **view-only in Release 1**; configuration/connection/automation is deferred.
- **SET-9.** Membership and participant types are **presentation only** — **no permissions architecture** is defined.
- **SET-10.** Notification/awareness preferences are **presentation only** — **no notification/event infrastructure**.
- **SET-11.** Destructive actions (e.g., account deletion) are **visible and confirmation-gated**; never hidden, never ambiguous.
- **SET-12.** Failures are **honest and recoverable** — prior values retained, unsaved input preserved, nothing fabricated.
- **SET-13.** Defaults (project/collaboration) are **convenience pre-fills** that never gate project value or override onboarding minimums.
- **SET-14.** **No APIs, events, implementation, or styling** is defined here; no existing model is redefined.

## S. Conformance Requirements

A conforming Account & Workspace Settings experience MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **SET-C1.** Provide a **settings surface separate** from the understanding workspaces, reachable from a consistent entry point, organized into the defined areas (§D). **Fail** if settings alters or overlays project understanding.
- **SET-C2.** Make **Account/Profile/Workspace/Project-Default/Collaboration/Notification** areas **editable for preferences/account info only**, saving no assessment and touching no project understanding (§E–§J; SET-5/SET-6). **Fail** if any setting changes assessment, findings, or recommendations.
- **SET-C3.** Present **Subscription, Billing, Usage, and Limits as visibility-first plan information** (not computed scores), with processing/implementation out of scope (§K, §L; SET-7). **Fail** if billing/subscription processing or any computed score is defined.
- **SET-C4.** Present **Integrations as view-only in Release 1** (no configuration/connection/automation) (§M; SET-8). **Fail** if integration configuration/automation/APIs appear.
- **SET-C5.** Display **workspace membership and participant types as presentation only**, with no permission logic (§N; SET-9). **Fail** if permission enforcement/architecture is defined.
- **SET-C6.** Present **notification preferences as presentation only**, with no delivery/event infrastructure (§J; SET-10). **Fail** if notification/event infrastructure or APIs are defined.
- **SET-C7.** Make **destructive actions visible and confirmation-gated** (e.g., account deletion) without defining their processing (§E; SET-11).
- **SET-C8.** Handle **save and data-unavailable failures** honestly — retain prior values, preserve unsaved input, fabricate no data, offer retry (§P; SET-12). **Fail** if a setting is silently changed or data is fabricated.
- **SET-C9.** Keep **defaults as non-gating pre-fills** consistent with onboarding (§H; SET-13). **Fail** if a default gates project value.
- **SET-C10.** Implement empty states distinguishing the defined none/unavailable cases (§O), and expose **no** governance, execution, automation, agent, API, event, permissions-architecture, billing-implementation, or subscription-implementation definition (SET-3/SET-4/SET-14). **Fail if governance workflows appear. Fail if execution workflows appear.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The experience **fails** if it: computes any value or score; generates any finding/recommendation/assessment; changes any project understanding or assessment; defines billing/subscription/payment processing; defines permissions architecture or enforces permissions; defines integration configuration/connection/automation in Release 1; defines notification/event infrastructure or APIs; hides or ambiguously executes destructive actions; silently changes account/workspace state or fabricates plan/billing data on failure; or introduces governance, execution, automation, agents, implementation, or styling.

## T. Deferred Items

Explicitly **deferred / out of scope:** governance; execution; automation; agents; APIs; events; implementation; styling; **permissions architecture** (logic/enforcement); **billing implementation** and payment processing; **subscription implementation** and plan-change processing; **integration configuration/connection/automation**; **notification/delivery infrastructure**; full **workspace branding/theming**; security/auth mechanisms behind the password/security flow; account-deletion processing; and any numeric tier/limit values beyond what Release 1 Tier Definitions specify (presented, not computed).

---

*This specification defines the canonical Release 1 Account & Workspace Settings Experience — the management periphery where users edit account, profile, workspace, project-default, collaboration, and notification preferences, and view subscription, billing, integrations, and workspace membership. Release 1 resolutions: editable profile (display name, avatar, optional descriptors), account email and confirmation-gated deletion visible, security visible; workspace name editable with optional lightweight branding; project defaults are non-gating pre-fills; default sharing is private; notification preferences cover mentions/replies/new comments/shared-project activity; subscription, billing, usage, and limits are visibility-first; integrations are view-only; membership and participant types are presentation only. It is UX/interaction only — it presents settings, computes nothing, generates nothing, governs nothing, never touches project understanding, and introduces no governance, execution, automation, agents, APIs, events, implementation, styling, permissions architecture, or billing/subscription implementation.*

**Account & Workspace Settings Experience Specification v1 complete.**

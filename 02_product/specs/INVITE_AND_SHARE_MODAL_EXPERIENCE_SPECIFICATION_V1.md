# Invite & Share Modal Experience Specification v1

**Document Type:** Experience Specification (UX / Interaction Model Only)
**Status:** Draft · Active Release 1 · **Date:** 2026-05-31
**Construct type:** **Contextual modal** — a lightweight, in-context dialog mapped to the ratified taxonomy as a **contextual (Panel-family) surface** that presents sharing UX; subordinate to Collaboration & Settings; not a destination/Workspace (§D).
**Consistent with and subordinate to (authoritative — must not redefine):** `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md` · `ACCOUNT_AND_WORKSPACE_SETTINGS_EXPERIENCE_SPECIFICATION_V1.md` · `NOTIFICATION_AND_AWARENESS_SURFACE_SPECIFICATION_V1.md` · `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` · `PROJECT_DASHBOARD_AND_PROJECT_LIST_EXPERIENCE_SPECIFICATION_V1.md` · `UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md` · Release 1 Tier Definitions.

> **Non-negotiable constraints.** UX / interaction model only. The modal **presents sharing UX only. It computes nothing, generates nothing, governs nothing, executes nothing, and changes no assessment.** It must **NOT** define: permissions architecture, **permission/access enforcement**, APIs, events, implementation, styling, delivery infrastructure, governance, approvals, or collaboration workflows beyond what is already specified in `COLLABORATION_AND_SHARING_EXPERIENCE_SPECIFICATION_V1.md`. **Only reanalysis changes assessment.** Sharing changes **no** project understanding; Artifacts remain the source of truth, Findings descriptive, Recommendations advisory.

> **Position in the architecture.** This is the **detailed UX** for the sharing intent already specified in `COLLABORATION_AND_SHARING_…` (§E) — a lightweight modal to **invite people, share project access, view shared participants, and remove access** — inside OSLO. It is distinct from Export & Share-Out (which packages understanding for **outside** review).

---

## A. Purpose

Define the canonical Release 1 **Invite & Share Modal** — the lightweight UX for **inviting people, sharing project access, viewing shared participants, and removing share access**. It answers: **"How do users grant, view, and remove access to a project inside OSLO?"** — without defining permissions architecture, enforcement, APIs, events, governance, approvals, or new collaboration workflows.

## B. Scope

**In scope:** where invite/share is accessed; the invite modal contents and interaction; how view-only sharing is presented; private invite-link presentation (if included, §H); the shared-users list; the remove-share/access UX; the relationship to Notifications/Awareness and to Collaboration comments; tier visibility/limits; empty/failure states; progressive disclosure; integrity rules; conformance.

**Out of scope:** permissions **architecture** and **enforcement** (who can actually do what is enforced elsewhere/deferred); APIs; events; implementation; styling; delivery infrastructure (how invites are sent); governance; approvals; collaboration workflows beyond `COLLABORATION_AND_SHARING_…`; billing/payment/entitlement implementation; and any assessment/finding/recommendation behavior. The modal **presents sharing and routes**; it enforces nothing and changes no understanding.

## C. Sharing Philosophy

Sharing exists to let the **right people see and collaborate on project understanding** — quickly and clearly — not to administer permissions or run an approval process. The modal is a **calm, lightweight dialog**: invite by identity, pick a participant type, see who has access, remove access — then close. It keeps **understanding the center of gravity**: sharing changes **no** assessment, finding, recommendation, or artifact, and **only reanalysis changes assessment.** It **presents** participant types and access as defined by Collaboration; it **enforces nothing** (enforcement is out of scope) and adds **no** governance.

## D. Construct Classification

Per the ratified governing taxonomy (`UNDERSTANDING_ARCHITECTURE_CLASSIFICATION_DECISION_001.md`), the Invite & Share Modal is a **contextual modal** — mapped to the **Panel-family** (contextual surface) sense: opened **in context** over the current surface, **preserving** it, **not a destination/Workspace**, subordinate to Collaboration & Settings. It is **not** an Understanding-Object Panel (it inspects no finding/recommendation); it is a **contextual sharing dialog**.

| Attribute | Classification |
|---|---|
| **Type** | **Contextual modal** (contextual surface), subordinate to `COLLABORATION_AND_SHARING_…` / Settings. |
| **Purpose** | present **invite / share / view participants / remove access** UX. |
| **Navigation** | opened **in context** from relevant surfaces; **not a destination/Workspace**; preserves and returns to the underlying surface. |
| **Context** | scoped to the **project** being shared (read of existing sharing state). |
| **Independent?** | No — a contextual dialog. |
| **Destination?** | **No.** |
| **Hosts actions?** | sharing-presentation actions only (invite / set participant type / remove); **no** understanding-changing actions, **no** enforcement. |
| **Contains?** | may route to Settings (workspace membership) / Awareness; **contains** no Workspaces/Panels. |
| **Not** | not a Workspace, not an Understanding-Object Panel, not Chat, not a permissions/governance/approval system, not the Export outside-review link surface. |

This binds the spec: anything that makes the modal a permissions-enforcement engine, a governance/approval workflow, or an assessment-changer is **out of type** and forbidden (§R/§S).

## E. Owner-Level Decisions — Resolutions

### 1 — Where invite/share is accessed (§F)
From **Project Overview** (a Share affordance), the **Project Dashboard / Project List** (per-project share), **Collaboration surfaces**, and **Account & Workspace Settings** (workspace membership view routes into per-project sharing). One modal; multiple in-context entry points (global navigation exposes it only via these project surfaces, not as its own destination).

### 2 — What the modal contains (§G)
An **invite input** (by identity/email — entry only; delivery out of scope), a **participant-type selector** (Owner/Collaborator/Viewer — presentation), the **shared-users list** (§J), a **remove-access** affordance per participant (§K), an optional **private invite-link** presentation (§H), and **tier-limit visibility** (§N). Nothing else — no permissions matrices, no approval steps.

### 3 — Participant types shown (§I)
**Project Owner · Collaborator · Viewer** — exactly the user-visible categories from `COLLABORATION_AND_SHARING_…` (presentation only; **no permission logic**).

### 4 — View-only sharing (§I)
**Viewer** = view-only participant: can read understanding and discussion but is presented as **not contributing edits/comments where not permitted**. The modal **presents** this as the Viewer type; it **does not enforce** it (enforcement out of scope).

### 5 — Public/private links (§H)
**Release 1: a private invite link MAY be presented** as a convenience to invite a specific person to become a participant (view-only/participant per type) — **routes into OSLO**, honestly labeled. **Public links and link-access enforcement are deferred** (§T). *(Distinct from Export & Share-Out's outside-review view-only link, which shares understanding outside OSLO; this link grants inside-OSLO access.)*

### 6 — How shared users are displayed (§J)
A simple **list of participants** with identity and **participant type**; the owner is indicated; **presentation only** (no roles/permissions matrix).

### 7 — Remove share/access (§K)
A per-participant **remove-access** affordance, **confirmation-gated**, presented as a **reversible sharing change** (re-invite possible). Removal is a **sharing-presentation** action; the modal does not define the enforcement mechanism.

### 8 — Awareness/notifications relation (§L)
Inviting/sharing **surfaces awareness** ("invitation received" / "project shared with me") via `NOTIFICATION_AND_AWARENESS_…`; the modal **triggers awareness presentation**, it **defines no notification/delivery infrastructure** and sends nothing itself.

### 9 — Tier limits visible (§N)
**Collaborator/seat limits per Release 1 Tier Definitions** are **visible** (e.g., "X of Y seats used"; additional sharing on higher tiers if tiers define it) — **visibility-first**, **no billing/entitlement implementation**.

### 10 — Out of scope (§T)
Permissions architecture/enforcement; public links; approval workflows; governance; APIs/events/implementation/styling; delivery infrastructure; billing/entitlement; and collaboration workflows beyond the Collaboration spec.

## F. Access Points

- **Project Overview** — primary Share affordance for the open project.
- **Project Dashboard / Project List** — per-project share entry.
- **Collaboration surfaces** — in-context share/invite.
- **Account & Workspace Settings** — workspace membership view routes into per-project sharing (membership is presentation-only there).
All open the **same** modal, scoped to the project; the modal is **not** a standalone destination.

## G. Invite Modal Experience

- **Invite input:** add a person by identity/email (entry only — **delivery mechanics out of scope**).
- **Participant type:** choose **Owner / Collaborator / Viewer** (presentation; §I).
- **Confirm invite:** presents the pending/added participant; **surfaces awareness** (§L); **enforces nothing**.
- **Shared-users list** (§J) and **remove** (§K) are present in the same modal.
- **Tier-limit visibility** (§N) shows seat usage; if at limit, the modal presents this honestly (per tiers) without billing logic.
- The modal opens **in context**, **preserves** the underlying surface, and **changes no project understanding**.

## H. Share Link Experience

- **Release 1 (optional):** a **private invite link** that **routes into OSLO** to let a specific person become a participant (per participant type), honestly labeled (view-only/participant).
- The link **creates no governance**, no approval, and **no comments/notifications beyond the awareness cue** (§L); **link-access enforcement is out of scope** (§T).
- **Public links are deferred.** This inside-OSLO access link is **distinct** from Export & Share-Out's outside-review snapshot link.

## I. Participant Type Presentation

- **Project Owner** — the originating participant (indicated, not removable via this modal).
- **Collaborator** — can contribute (edit/comment) where permitted — **presented**, not enforced.
- **Viewer** — view-only — **presented**, not enforced.
These mirror `COLLABORATION_AND_SHARING_…` exactly; the modal **defines no permission logic** and may not invent new types.

## J. Shared Users List

- A simple list: each participant's **identity** + **participant type**; the **owner** indicated.
- **Presentation only** — no permissions matrix, no role administration beyond type display.
- Routes (where useful) to the workspace-membership view in Settings (presentation-only there).

## K. Remove Share Experience

- A per-participant **remove-access** affordance, **confirmation-gated**, presented as a **reversible** sharing change.
- Removal **changes no project understanding** and triggers no governance/approval; it may surface an awareness cue per the Notification spec.
- The modal presents removal; it **does not define** the enforcement mechanism (out of scope).

## L. Relationship to Notifications & Awareness

- Inviting/sharing/removing **surfaces awareness** ("invitation received" / "project shared with me" / sharing activity) via `NOTIFICATION_AND_AWARENESS_…`.
- The modal **triggers awareness presentation**; it **creates no notification infrastructure**, defines no delivery, and sends nothing itself. Awareness items route to the project/collaboration context (per that spec).

## M. Relationship to Collaboration Comments

- The modal manages **access**, not discussion. **Comments remain attached to objects** (Collaboration spec); the modal **creates, edits, or references no comments.**
- Granting access lets a participant *reach* collaboration; the modal itself never touches comment content.

## N. Tier Visibility & Limits

- **Collaborator/seat limits per Release 1 Tier Definitions** are **visible** (e.g., seats used/available; higher-tier sharing if defined).
- Tier limits are shown as **plan information** (visibility-first, consistent with Settings/Dashboard) — **no billing, payment, or entitlement implementation**.
- At-limit states are presented honestly (e.g., "seat limit reached on current plan") without fabricating access and without a billing flow.

## O. Empty States

- **No participants yet** — a solo project: "invite people to collaborate" (distinct from unavailable).
- **No invite link (if links disabled/not applicable)** — neutral; invite-by-identity remains.
- **At seat limit** — presented per tier (§N), distinct from "unavailable."
- **Unavailable** — sharing temporarily unavailable (§P), distinct from "no participants."

## P. Failure States

- **Sharing unavailable** — "sharing unavailable — retry"; the underlying surface remains usable; no fabricated participants.
- **Invite failed** — reported honestly; input preserved; no silent partial invite; no fabricated "invited" state.
- **Remove failed** — reported; prior sharing state retained; confirmation-gated retry.
- **Link unavailable** — the invite link can't be produced → "unavailable — retry"; no fabricated link.
- **No access (cannot share)** — if the user/plan can't share (tier-locked or not permitted), present plainly; no fabricated access; no billing flow defined here.
- **General principle:** honest, recoverable, non-fabricating; the modal never invents participants, access, or invite outcomes.

## Q. Progressive Disclosure

- **Always visible (in modal):** invite input + participant-type selector + shared-users list.
- **One interaction away:** remove-access (confirmation-gated); private invite link (if enabled); tier-limit detail.
- **Routes:** workspace membership (Settings); awareness (Notification surface).
- **Intentionally absent:** permissions matrices/role administration; approval/governance steps; assessment-changing or understanding affordances; billing/upgrade flows; delivery configuration; public-link/enforcement controls.

## R. Integrity Rules

- **IS-1.** The modal **computes nothing** and **changes no assessment**; **only reanalysis changes assessment**; sharing touches no project understanding.
- **IS-2.** The modal **generates nothing** (no findings/recommendations/assessment/comments).
- **IS-3.** The modal **governs nothing, executes nothing, automates nothing**, and adds **no approval workflow**.
- **IS-4.** **No permissions architecture or enforcement** is defined — participant types and access are **presentation only**, mirroring `COLLABORATION_AND_SHARING_…`.
- **IS-5.** Participant types are exactly **Owner / Collaborator / Viewer**; the modal **invents no new types** and no permission logic.
- **IS-6.** **Viewer = view-only (presented, not enforced)**; enforcement is out of scope.
- **IS-7.** **Private invite link routes into OSLO** (inside-access), honestly labeled; **public links and link enforcement deferred**; distinct from Export's outside-review link.
- **IS-8.** Sharing/removal **surfaces awareness** via the Notification surface; the modal **defines no notification/delivery infrastructure** and sends nothing itself.
- **IS-9.** **Comments remain on objects** (Collaboration); the modal creates/edits/references no comments.
- **IS-10.** **Tier limits are presented** (visibility-first); **no billing/payment/entitlement implementation**.
- **IS-11.** Remove-access is **confirmation-gated and reversible**; it changes no understanding and runs no governance.
- **IS-12.** The modal is a **contextual modal**, **not a destination/Workspace/Object-Panel/Chat/permissions-system**, opened in context and preserving the underlying surface.
- **IS-13.** **No** APIs, events, implementation, styling, delivery infrastructure, or enforcement defined here; redefines no surface; fabricates nothing.

## S. Conformance Requirements

A conforming Invite & Share Modal MUST (objective, structural, **non-numeric**); it **fails** if any forbidden behavior appears:

- **IS-C1.** Be a **contextual modal** opened from project surfaces, preserving the underlying surface, **not a destination** (§D, §F; IS-12). **Fail** if it becomes a destination or a permissions/governance system.
- **IS-C2.** Contain only **invite / participant-type / shared-users / remove / optional private link / tier visibility** (§G; §E.2). **Fail** if it exposes a permissions matrix, role administration, or approval workflow.
- **IS-C3.** Present participant types as exactly **Owner/Collaborator/Viewer**, **presentation only**, mirroring Collaboration; **define no permission logic/enforcement** (§I; IS-4/IS-5). **Fail** if it invents a type or enforces/defines permissions.
- **IS-C4.** Present **Viewer as view-only** (not enforced) (§I; IS-6).
- **IS-C5.** If a link is offered, make it a **private invite link routing into OSLO**, honestly labeled, with **public links/enforcement deferred** (§H; IS-7). **Fail** if a public link or link-enforcement is defined, or it is conflated with Export's outside link.
- **IS-C6.** Make **remove-access confirmation-gated and reversible**, changing no understanding (§K; IS-11).
- **IS-C7.** **Surface awareness** via the Notification surface without defining notification/delivery infrastructure (§L; IS-8). **Fail** if it defines delivery/notification infrastructure or sends directly.
- **IS-C8.** Touch **no comments** (§M; IS-9) and **change no assessment/understanding** (IS-1/IS-2). **Fail if sharing changes assessment or touches a comment/finding/recommendation.**
- **IS-C9.** **Present** tier limits (visibility-first) with **no billing/entitlement implementation** (§N; IS-10). **Fail** if a billing/upgrade/entitlement flow is defined.
- **IS-C10.** Implement empty states (no participants / no link / at-limit / unavailable) and honest failure states (sharing/invite/remove/link unavailable / no access) that fabricate nothing (§O, §P).
- **IS-C11.** Define **no** permissions architecture/enforcement, APIs, events, implementation, styling, delivery infrastructure, governance, approvals, or new collaboration workflows (IS-3/IS-4/IS-13; §T). **Fail if permission enforcement, governance, approvals, APIs, or new workflows appear.**

**Explicit fail conditions.** Conformance is **all-or-nothing**. The modal **fails** if it: defines or enforces permissions; invents a participant type; exposes a permissions matrix / role administration / approval / governance workflow; defines a public link or link-access enforcement, or conflates the invite link with Export's outside-review link; changes any assessment or project understanding, or touches a comment/finding/recommendation; defines notification/delivery infrastructure or billing/entitlement; becomes a destination/Workspace; fabricates participants/access/invite outcomes; or defines APIs, events, implementation, styling, delivery infrastructure, or collaboration workflows beyond the Collaboration spec.

## T. Deferred Items

Explicitly **deferred / out of scope:** permissions architecture and **enforcement**; **public links**; link-access enforcement; approval/governance workflows; role/permission administration; bulk invite/management; invite-delivery infrastructure (email/SMS/push); billing/payment/entitlement implementation and upgrade flows; external/guest-domain controls; collaboration workflows beyond `COLLABORATION_AND_SHARING_…`; APIs; events; implementation; styling; mobile-specific modal behavior; and any numeric/calibration values.

---

*This specification defines the canonical Release 1 Invite & Share Modal — a lightweight contextual modal (subordinate to Collaboration & Settings) that provides the detailed UX for inviting people, sharing project access, viewing shared participants, and removing access inside OSLO, opened in context from Project Overview, the Dashboard/Project List, Collaboration surfaces, and Settings. It presents an invite input (by identity; delivery out of scope), the participant types Owner/Collaborator/Viewer exactly as Collaboration defines them (presentation only; view-only Viewer presented, not enforced), a shared-users list, a confirmation-gated reversible remove-access affordance, an optional private invite link that routes into OSLO (public links and link enforcement deferred; distinct from Export's outside-review link), and visibility-first tier/seat limits. Sharing surfaces awareness via the Notification surface without defining delivery; comments remain on their objects; and sharing changes no assessment or project understanding. It defines no permissions architecture or enforcement, APIs, events, implementation, styling, delivery infrastructure, governance, approvals, billing/entitlement, or collaboration workflows beyond the Collaboration spec. Only reanalysis changes assessment.*

**Invite & Share Modal Experience Specification v1 complete.**

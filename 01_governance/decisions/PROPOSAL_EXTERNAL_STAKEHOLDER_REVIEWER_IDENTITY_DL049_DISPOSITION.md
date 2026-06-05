# DL-049 (DISPOSITION DRAFT) — External-Stakeholder / Reviewer Identity + Reviewer→User Promotion

**Status:** **RATIFIED — DL-049 (2026-06-05); applied to the Runtime Object Model (Principal); gap #337 resolved; CHG-060.** Owner elected **Option A — lightweight Reviewer**. Per `CLAUDE.md`, only the owner ratifies; the contracted CRR evidence seam is **preserved, not redefined.** **Separable scope call RESOLVED (2026-06-05, CHG-064): the recipient-experience build is fast-follow → Release 2; R1 (the owner's own validation vehicle) generates + measures invitations only.** The identity *model* is ratified now; the *recipient UI / auth / promotion / convert-moment* is R2.

> **Why a Decision (ontology):** this introduces a **new identity concept** into the object model (a Reviewer/Stakeholder principal distinct in *capability* from a full User) and the rule for how one becomes the other. That is an **ontology/architecture choice** — it cannot be settled by a commodity spec. The **recipient UI, convert-moment, and link security are commodity**; only the **identity model + promotion semantics** are decided here.

---

## Part A — The identity model: one Principal, two capability levels

Resolve gap #337 with a **single `Principal` identity object** carrying a capability attribute **`type: reviewer | user`** — **not** two distinct objects you migrate data between.

- **Reviewer** (`type = reviewer`): a **lightweight, email-verified** principal **scoped to the specific items shared with them** (a CAF finding / CRR package, or a shared MRI). May **view** the shared item and **respond** (CRR responses). Has **no Workspace, no projects.**
- **User** (`type = user`): an email-verified principal **plus** a Workspace/Account, project-creation rights, and a tier (default **Free / Tier 1**).

**Rationale:** modeling Reviewer and User as **one principal at two capability levels** makes promotion a **state transition**, not a data migration — no record copy, no reconciliation, **no attribution drift**. (The "two distinct objects" alternative re-introduces a copy-and-merge problem and risks provenance rewrite — rejected for exactly that reason.)

## Part B — Reviewer → User promotion (the migration path)

Promotion is an **in-place upgrade of the same principal**, triggered at the realized-value convert-moment ("create your own project"):

1. The Reviewer is **already authenticated** (verified email) → promotion is **one step**: provision a Workspace/Account, set **`type = user`**, assign **Free (Tier 1)** caps (DL-048), enable project creation.
2. **Identity ID is unchanged** → continuity of the principal.
3. **Audited** (SEC-06): the `reviewer→user` transition is logged (who, when).

**Carries (unchanged):** identity (verified email, display name), **contribution history** — every CRR response stays attributed to the same principal — and the audit trail.
**Gains:** own Workspace, Free tier, project creation.
**Does NOT widen:** the principal's **scoped access to the inviter's project.** Account-type and share-scope are **separate axes** — becoming a User grants *their own* workspace, **never** elevated access to the inviter's project. (Privilege-escalation guard.)

## Part C — Invariants preserved (not negotiable)

- **Append-only / no overwrite:** past CRR responses are canonical evidence (evidence-attested, provenance = the principal). Promotion **never re-keys or re-attributes** them; the stable identity ID is the through-line. History is **immutable**.
- **Response = evidence, not truth:** unchanged by promotion. A promoted User's past responses do **not** retroactively become truth; **OSLO never self-accepts.**
- **Contracted seam preserved:** the **response → evidence → Deep Pass** path (Wave A Perceive intake · Wave I CRR) is **unchanged** — its author is now simply a `Principal` of `type = reviewer`. No contract is redefined.
- **Cost-governed:** reviewer activity (CRR-04 → Deep Pass) is **bounded by DL-048** and draws on the **inviter's** budget/allowance; on promotion the new User receives their **own** Tier-1 budget.

## Part D — Edge cases (design notes; not blocking)

- **Different-email later signup:** a new `Principal` (not a migration); prior Reviewer contributions stay attributed to the original principal. **Optional account-linking** by re-verifying the reviewer email is a **later concern** (account-merge is sensitive); the **default convert path uses the already-verified reviewer email**, avoiding merge.
- **De-dup:** on signup, **match by verified email** so a Reviewer is not duplicated ("continue as your existing reviewer identity").
- **Never converts:** persists as a Reviewer principal (per retention); the inviter keeps the value regardless.
- **Tier on promotion:** plain **Free** — no bypass; standard Tier-1 caps apply.

## Part E — Classification (build accordingly)
- **Architecture / ontology (this DL):** the `Principal` object + `type` attribute + promotion semantics + external-auth (email-verified Reviewer).
- **Commodity (SEC + SHARE + MON):** the scoped review/view UI, the convert-moment, attribution/CTA, **link security** (expiry/revocation/scoping — closes gap #339).
- **Already contracted (preserve):** the CRR response→evidence→Deep-Pass seam (Wave A/I); the DL-048 cost governance that bounds it.

---

## Disposition / conditions
- **Disposition:** **Accepted** (owner ratified 2026-06-05; Option A). Object Model updated; gap #337 resolved.
- **Conditions (proposed):** single-`Principal`-with-`type` model (not two objects); promotion is a **state transition, not a data copy**; **scope is never widened** on promotion (account-type ≠ share-scope); **provenance/history immutable** (no re-attribution); default tier **Free**; promotion **audited**; the CRR evidence seam is **preserved, not redefined**.
- **Separable scope call — RESOLVED (2026-06-05): fast-follow → Release 2.** R1 is the owner's own test/validation vehicle, so the conversion side has nothing to convert yet; R1 ships share/CRR generating invitations + TEL-06 measuring them (instrumented and ready), and **Release 2** builds the recipient experience (auth, view/respond, promotion, convert-moment) against real funnel data. The identity model (this DL) is unchanged — zero rework, clean drop-in.

## Owner decision required
- [ ] Adopt **Part A** — single `Principal` with `type: reviewer | user` (Option A).
- [ ] Adopt **Part B** — in-place `reviewer→user` promotion (provision workspace, Free tier; identity ID stable; scope not widened).
- [ ] Affirm **Part C** invariants + **Part E** classification.
- [ ] Decide **R1 vs fast-follow** for the recipient experience (separable).
- [ ] On ratification: update the **Runtime Object Model** (introduce `Principal`/`type`, relate `StakeholderResponse` author to it) + auth/security model; spec the commodity review/view + convert-moment + link security; **preserve** the Wave A/I CRR seam; record DL-049 + changelog; resolve gap #337 (and #339 via link security).

---
*This draft resolves Capability-Matrix gap #337 per the owner's election of Option A by introducing a single `Principal` identity object with a `type: reviewer | user` capability attribute — a lightweight email-verified Reviewer scoped to shared items at one level, a full Workspace-owning Free-tier User at the other — so that Reviewer→User conversion is an in-place, one-step promotion (provision workspace, set type=user, assign Free tier) rather than a data migration between two objects, keeping the identity ID stable and therefore preserving the append-only attribution of all prior CRR responses, the response-as-evidence-not-truth invariant, and the contracted response→evidence→Deep-Pass seam, while never widening the principal's scoped access to the inviter's project. It classifies the identity/ontology/auth model as the architecture decision (this DL), the review/view UI + convert-moment + link security as commodity, and the CRR evidence seam + DL-048 cost governance as already-contracted to preserve; it folds in the edge cases (different-email signup as a new principal with optional later linking, email de-dup, non-converting reviewers, default Free tier) and keeps the R1-vs-fast-follow timing as a separable owner scope call. It edits no ratified contract and routes ratification to the owner.*

**DL-049 (DRAFT) — External-Stakeholder / Reviewer Identity + Promotion prepared. Pending Owner Ratification.**

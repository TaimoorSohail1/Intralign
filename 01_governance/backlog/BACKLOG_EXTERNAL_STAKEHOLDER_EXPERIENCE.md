# Backlog (DRAFT) — External-Stakeholder Experience (the P0 conversion-path scoping item)

**Status:** **Proposed — owner-directed (2026-06-05).** Pending Owner Ratification. Resolves **P0** of `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001` and **Capability-Matrix gap #337**. **Architecture-touching** (a new identity concept) — therefore this **scopes** the decision and **routes the ontology/identity choice to the owner**; it does **not** decide it. Per `CLAUDE.md`: no new ontology resolved unilaterally; the contracted CRR evidence seam is **preserved, not redefined.**

---

## 0. Intent

Define the **external-stakeholder experience** — what an invited, non-account recipient lands in, and how they become a user — so OSLO's viral loops actually **convert**. Today invitations are generated (CRR "Share For Review"; MRI share links) but the recipient side is undefined, capping k-factor's conversion term (**c**) near zero (Virality Audit F1/F2).

## 1. The gap (#337)

> "CRRs and external-stakeholder virality imply **non-account participants**, but there is **no Stakeholder/Reviewer object distinct from User, and no external-auth model.**"

So a CRR or shared MRI produces an *invitation* with **no specified recipient experience and no convert-moment.** This is simultaneously the **#1 growth lever** and a **real architecture gap** — not just a UX nicety.

## 2. What must be true (requirements — independent of the identity model)

- **Low-friction entry:** an invited recipient reaches the shared **finding / review package (CRR-02) or MRI** with **minimal or no signup** before seeing value.
- **Realized-value convert-moment:** at the point the recipient *feels* the value (after reviewing a finding or exploring an MRI), offer "**map your own project's understanding**" → account creation. The highest-intent instant must be owned.
- **Preserve the contracted epistemic seam:** a stakeholder response is already **evidence-attested** (provenance = the stakeholder) → Perceive intake → Deep Pass (**CRR-04**, Wave A/I). The recipient experience **must not disturb** that — a response is **evidence, not truth**; OSLO still never self-accepts.
- **Scoped, safe access:** the recipient sees **only** what was shared (one finding / one MRI), with **link expiry / revocation / scoping** (closes gap #339). No lateral access to the project.
- **Cost-governed:** recipient-driven recompute (CRR-04 → Deep Pass) is **bounded by DL-048** — a burst of stakeholder responses **coalesces**, never a cost spike. Recipient activity counts against the **inviter's** tier budget (or a defined allowance), not an ungoverned path.
- **Value-aligned:** invitation is **user-initiated** (no autonomous sends); recipient prompts are honest/value-based (no dark patterns), per the upgrade-prompt rules.

## 3. The architecture / identity decision (OWNER choice — options framed, not decided)

| Option | Model | Friction (c) | Security / attribution | Convert path |
|---|---|---|---|---|
| **A — Lightweight Reviewer (recommended)** | A **Stakeholder/Reviewer** identity **distinct from User** (email-verified, scoped to shared items; can view + respond; upgradeable to full User) | low | strong (verified, scoped) | **clean** — identity persists, upgrade-in-place |
| **B — Tokenized anonymous link** | No identity; signed link grants scoped access; respond as named-but-unauthenticated | **lowest** | weaker (link-bearer access; attribution soft) | full signup later (identity not carried) |
| **C — Full account required** | Recipient must sign up to view/respond | **highest** (kills c) | strong | n/a — this is the implicit status quo the audit flags |

**Recommendation: Option A** — best balance of low friction, scoped security, attribution, and a **clean in-place convert path** (a Reviewer simply becomes a User). It introduces a **new identity object** (Reviewer/Stakeholder ≠ User), so it is an **ontology/architecture decision for the owner** (may warrant a DL). Option B is a faster, weaker interim; Option C is not recommended.

## 4. Recipient flow (illustrative — Option A)

invite (user-initiated CRR / share) → recipient opens a **scoped review/view** (email-verified Reviewer) → sees **value** (finding + context + recommendation, or the MRI) → **acts** (responds → flows as evidence to the inviter via CRR-04; or explores) → **convert-moment** ("map your own project") → optional **upgrade Reviewer→User**. The inviter's understanding improves from the response **regardless** of whether the recipient converts (value = virality).

## 5. Classification (build accordingly)

- **Architecture / ontology (owner decision, possibly a DL):** the **Reviewer/Stakeholder identity** + external-auth model (Option A/B/C).
- **Commodity (SEC + SHARE + MON):** the scoped review/view UI, link security (expiry/revocation/scoping, #339), the convert-moment + attribution/CTA.
- **Already contracted (preserve, do not redefine):** the **response → evidence → Deep Pass** seam (Wave A Perceive intake + Wave I CRR), and the DL-048 cost governance that bounds it.

## 6. Scope question — R1 or fast-follow?

It is the **#1 k-factor lever** *and* a **real architecture gap**, so the tradeoff is genuine:
- **In R1:** the viral loop is *real at launch* (invitations convert) — but adds identity/auth scope to an already-full R1.
- **Fast-follow:** R1 ships with the loops **present but conversion-capped** (invitations generated, recipients hit friction); convert them in the first follow-on. Lower R1 risk, slower early k.

**Owner decides.** (If fast-follow: ship R1 with share/CRR generating invitations + TEL-06 measuring them, so the loop is instrumented and ready the moment the recipient experience lands.)

## 7. Dependencies
CRR (Wave A Perceive intake · Wave I) · SHARE-01…05 · SEC (auth, scoping, link security #339) · DL-048 (recipient-driven cost) · TEL-06/TEL-02 (measure conversion) · the Virality Audit (parent).

## 8. Owner decision required
- [ ] **Identity model:** Option **A (lightweight Reviewer, recommended)** / B (tokenized) / C (full account). If A, authorize the **Reviewer/Stakeholder ontology** decision (likely a DL).
- [ ] **Scope:** **R1** vs **fast-follow** (with R1 shipping the instrumented-but-uncapped loop).
- [ ] Confirm **scoped access + link security** (expiry/revocation/scoping) requirements (closes #339).
- [ ] Confirm **recipient cost** is bounded under DL-048 (whose budget it draws).
- [ ] Reaffirm the **value-alignment guardrails** (user-initiated, evidence-not-truth, no dark patterns).
- [ ] On approval: route the identity/ontology decision (Object Model + auth) ; spec the commodity review/view + convert-moment; preserve the CRR seam; record via changelog.

---
*This owner-directed draft scopes the external-stakeholder experience — the P0 lever from the virality audit and Capability-Matrix gap #337 — which is simultaneously OSLO's highest-leverage k-factor conversion fix and a genuine architecture gap (no Reviewer/Stakeholder identity distinct from User, no external-auth model). It states the requirements independent of the identity model (low-friction entry, a realized-value convert-moment, preservation of the contracted response→evidence→Deep-Pass seam, scoped/safe access with link hygiene, DL-048-bounded recipient cost, and user-initiated/no-dark-pattern guardrails), frames three identity options (a recommended lightweight email-verified Reviewer distinct from User, a tokenized anonymous link, or full-account-required) and routes that ontology decision to the owner, classifies which parts are architecture vs commodity vs already-contracted, and surfaces the R1-vs-fast-follow scope tradeoff with an instrumented-but-uncapped interim. It decides nothing unilaterally and preserves the CRR evidence seam.*

**External-Stakeholder Experience backlog (DRAFT) prepared. Pending Owner Ratification.**

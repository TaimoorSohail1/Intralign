# Backlog (DRAFT) — Internal Test-Bypass Entitlement (designated accounts bypass Free-tier constraints)

**Status:** **Proposed — owner-directed (2026-06-05).** Pending Owner Ratification. Per `CLAUDE.md`, only the owner ratifies. **Commodity (MON + SEC, Category C/E — DL-043 J); no cognition, no epistemic invariant touched; no architecture change.** Builds on DL-048 (tier-keyed cost governance) + CHG-056/057 (tier config).

---

## 0. Owner intent

> A **system flag** that allows **designated accounts to bypass Free-tier constraints, primarily for testing.** How to accommodate.

## 1. The principle — config, not a code bypass

**Do NOT implement a divergent branch** (`if (account.isInternal) skipChecks()`). That is an untested code path and a privilege-escalation surface. **Model the bypass as configuration on the one governed enforcement path:**

- Add a **non-consumer `Internal` entitlement** — a **tier-keyed config row** (Calibration §4c) whose caps (active projects, fix/chat per day, Fast/Deep envelope, Deep/day, daily + monthly token budget) are **unlimited / very-high**. The **same contracted DL-048 enforcement still runs** — it simply reads "unlimited." Consistent with the standing rule: **add config rows, not code.**
- `Internal` is **not part of the consumer ladder** (Free · Basic · Pro · Team · Enterprise). It is an internal/staff/test entitlement, never sold, never shown as an upgrade target.

**Why this is architecturally clean:** it touches no cognition and no epistemic invariant — an Internal account gets the identical analysis, the identical Attested/Derived handling, the identical recompute discipline; only its *quota* differs. Blast radius = quota enforcement only.

## 2. Grant mechanism (the security story — mandatory)

A "bypass Free-tier" entitlement is a **privilege-escalation + cost vector**, so:

- **Server-side only.** The entitlement lives on the account record; settable **only** via an admin/ops path. **Never** client- or user-API-settable. **Not self-grantable.**
- **Allowlist, default-off.** Only explicitly designated accounts; every account is non-Internal by default.
- **Audited (SEC-06).** Grant/revoke emits an audit record: who, when, why, scope. Immutable trail.
- **Time-boxed (recommended).** Optional auto-expiry on the grant so a bypass can't silently persist.
- **Environment scope (owner default: staging/test only).** Bypass entitlement is grantable **only in non-production**, so uncapped cost can never reach prod. *(Owner may elect "production allowed (controlled)" — if so, require tight monitoring + mandatory time-box, since uncapped cost on prod is a real risk.)*

## 3. Bypass the limit — NOT the telemetry or the analytics hygiene

- **`AI Spend Recorded` still fires** for Internal accounts. They are *uncapped*, so their cost especially must be visible. **Bypassing the cap must not bypass the meter.**
- **Exclude Internal accounts from analytics** (easy to miss, and it skews real data): **flag them out of TEL-07 conversion metrics and out of the Free-tier unit-economics medians.** Otherwise test traffic distorts both the upgrade-prompt optimality tuning (§4d) and the cost data used to re-tune the DL-048 defaults.
- **Suppress Upgrade Prompts (MON-04)** for Internal accounts — they are not conversion targets.

## 4. Classification & QA

- **Classification:** commodity — **MON** (entitlement/limits) + **SEC** (grant, RBAC, audit). No cognitive contract; no epistemic-invariant impact; no DL required (config + commodity capability).
- **QA acceptance:** (1) an Internal account is **not capped** (projects/fix/chat/envelope/deep/budget); (2) `AI Spend Recorded` **still emits**; (3) the account is **excluded** from conversion + cost analytics; (4) no Upgrade Prompts shown; (5) the entitlement **cannot be self-granted or client-set**; (6) grant/revoke is **audited**; (7) (if staging-only) the grant path is **unavailable in production**.

## 5. Owner decision required
- [ ] Approve the **Internal entitlement** model (non-consumer tier-keyed config row, unlimited caps) — *recommended* — vs. an account-override attribute, vs. both.
- [ ] Confirm **environment scope: staging/test only** *(recommended)* vs. production-allowed (controlled + time-boxed).
- [ ] Approve the **grant controls** (server-side admin-only, allowlist, audit, optional time-box).
- [ ] Approve **analytics exclusion + prompt suppression** for Internal accounts.
- [ ] On approval: add the `Internal` row to Calibration §4c; glossary note; enumerate the grant/audit + exclusion as MON/SEC obligations; QA per §4; record via changelog.

---
*This owner-directed draft accommodates a system flag for designated test accounts to bypass Free-tier constraints by modeling it as a non-consumer `Internal` entitlement — a tier-keyed config row with unlimited caps that the existing contracted DL-048 enforcement reads, rather than a divergent bypass code path — keeping the change in the commodity monetization/security layer with no impact on cognition or any epistemic invariant. It specifies the mandatory security story (server-side admin-only grant, allowlist, audit trail, optional time-box, staging-only by default), requires that the bypass lift the limit but never the `AI Spend Recorded` telemetry, and requires excluding Internal accounts from TEL-07 conversion metrics and the unit-economics medians plus suppressing upgrade prompts, with a seven-point QA acceptance set. It routes the model/scope/control choices to the owner.*

**Internal Test-Bypass Entitlement backlog (DRAFT) prepared. Pending Owner Ratification.**

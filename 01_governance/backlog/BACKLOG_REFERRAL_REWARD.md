# Backlog (DRAFT) — Referral Reward (Virality Audit P5)

**Status:** **Proposed — owner-directed (2026-06-05).** Pending Owner Ratification + an **in/out-of-R1** call. Commodity (MON + SHARE); **cost-and-abuse-sensitive** — bounded by DL-048 + Internal-style guards. No cognition, no epistemic invariant touched.

---

## 0. Intent

Add a **bounded reward for inviting** (Virality Audit P5) — a direct i+c multiplier: "**invite a reviewer/teammate who joins → a capped capacity bump.**" The only virality amplifier with a real **cost + abuse surface**, so it is drafted, not auto-applied.

## 1. Mechanic (proposed)

- **Trigger:** an invited recipient **joins** (activates a `Principal`, DL-049) — i.e. credit on *conversion*, not mere invite (anti-spam).
- **Reward (both sides, bounded):** a **capped, time-boxed capacity bump** on the **Free/Basic** tier — e.g. **+N suggested-fixes/day for 7 days** or **a one-time +X token allowance** — **tier-keyed config** (Calibration), never an unbounded or permanent grant.
- **Caps:** **max rewarded referrals per user per month**; reward **expires**; **diminishing** beyond the cap. The reward draws on a **bounded referral pool**, not the user's normal budget — so it can't cascade.

## 2. Cost + abuse guardrails (mandatory)

- **Bounded by DL-048:** every reward is a **finite, tier-keyed config value** with a **monthly per-user referral cap**; the aggregate is modeled into unit economics before launch. **No reward may create an uncapped cost path.**
- **Abuse-resistant** (reuse the Internal-bypass guard mindset): credit only on **genuine activation** (verified email, real usage signal), **de-dup on verified email** (no self-referral / same-person loops), **velocity limits**, and **fraud telemetry**. Internal/test accounts (CHG-059) **cannot earn or grant** rewards.
- **Value-aligned:** **user-initiated**, honest framing, no dark patterns (consistent with the share/upgrade-prompt rules). The reward **augments**, never coerces.

## 3. Measurement
Folds into the **k-factor instrumentation (P6)** — track referral-attributed joins/conversions and **reward cost per converted user** vs. blended CAC, so the reward's ROI is visible from day one (TEL-06 + cost telemetry).

## 4. Classification
Commodity **MON** (reward grant/caps) + **SHARE** (referral link) + **TEL** (attribution). The grant is **config**; no contract or epistemic impact. No DL required if adopted (config + commodity capability) — **but the in/out-of-R1 and the reward values are owner decisions.**

## 5. Owner decision required
- [ ] **In or out of R1?** (the loop works without it via P1–P4; this is an accelerant, not a prerequisite.)
- [ ] Reward **shape** (capacity bump vs token allowance) + **values** + **monthly referral cap** (Calibration config).
- [ ] Confirm the **DL-048 bound + abuse guards + Internal exclusion**.
- [ ] On approval: add reward config to Calibration; spec the referral link + attribution (TEL-06); record via changelog.

---
*This owner-directed draft proposes the Virality Audit's P5 referral reward — a bounded, conversion-credited capacity bump for inviting users who actually join — as the one amplifier with a real cost and abuse surface, and therefore designs it defensively: every reward is a finite, tier-keyed, time-boxed config value drawn from a bounded pool with a monthly per-user cap so it can never open an uncapped cost path, credited only on genuine activation with email de-dup, velocity limits, fraud telemetry, and Internal-account exclusion, and framed value-alignedly (user-initiated, honest, no dark patterns). Its ROI folds into the P6 k-factor instrumentation (reward cost per converted user vs blended CAC). It is classified commodity (MON/SHARE/TEL) requiring no DL, but the in/out-of-R1 decision and the reward values are routed to the owner.*

**Referral Reward backlog (DRAFT) prepared. Pending Owner Ratification + R1 scope call.**

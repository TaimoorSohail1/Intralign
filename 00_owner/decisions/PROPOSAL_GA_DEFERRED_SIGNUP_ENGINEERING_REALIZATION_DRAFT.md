# PROPOSAL — GA Deferred-Signup: Three Engineering Realization Proposals (Provisional Identity · Pre/Post-Signup Gating · Pre-Signup Retention & Privacy)

- **Status:** **Draft — Framework 001 Proposal stage. NOT ratified.** AI-drafted; owner ratifies intent; **engineering authors the realization** (ratify ≠ author). **GA-gated** — Alpha/Beta runs authenticated and requires none of this; this package must land **before GA open-access** (DL-073 §Phasing; DL-076 GA stage).
- **Framework 001 stage:** Proposal (packages the three engineering proposals DL-073 deferred).
- **Class:** Product↔engineering seam (20_handoff intent; 30_engineering realization). Touches identity/persistence, DL-048 gating, and retention/privacy. **No doctrine, constitution, or epistemic-invariant change.**
- **Authorized by:** Owner direction 2026-06-19 ("proceed — GA onboarding"), discharging the open authorization in `PROPOSAL_TWO_MODE_ONBOARDING_DEFERRED_SIGNUP_DRAFT.md` §6.3 and **DL-073 §Phasing ("Before GA")** items (a)/(b)/(c).
- **Source:** DL-073 (two-mode stage-conditioned onboarding / deferred-signup / save-to-keep). Grounded in DL-046 (60s Time-to-First-MRI), DL-048 (freemium envelope + enforcement), DL-049 (`Principal` / reviewer identity), DL-074 (normalized-compute governor + overage), DL-076 (Alpha/Beta/GA stages), and the Calibration Defaults §4/§4b/§4c.

---

## 0. Scope and boundaries (read first)

DL-073 ratified the **save-to-keep** deferred-signup model and deferred three realization items to "before GA." This proposal frames all three for owner ratification of **intent**, recommends starting positions, and **delimits what engineering authors** — it does **not** author the data model, schema, or final numeric values as canon (Anti-Assumption: open values are escalated as owner decisions with *recommended* starting points, never assumed).

What is **already ratified** (DL-073, not reopened here): the full first run — ingest → analysis → **60-second orientation** → explore — is **anonymous**; **signup is required only to save/persist**; **Deep Pass is the later upgrade gate**, not the initial signup gate; a **light anonymous-usage cap** bounds anonymous compute. This package realizes *how*.

**Invariants preserved by all three parts (binding):** OB-1 / OB-5 (onboarding and provisioning **compute nothing, generate nothing, govern nothing**; only reanalysis changes assessment); epistemic safety / no-fabricated-assessment; the DL-046 60s definition; **identity continuity** (a claimed account is the *same* principal, not a copy); the DL-048 enforcement mechanism is **contracted** (Wave B/S/I) and is **reused via config**, not re-coded.

---

## Foundation — the provisional-session lifecycle (shared substrate for all three parts)

The deferred-signup run implies a **provisional (anonymous) principal** that is later **claimed** at signup:

```
visit ──▶ provisional session (anonymous_id)
        ├─ ingest → Fast Pass → 60-second orientation → explore   [all anonymous]
        └─ "save to keep" ──▶ sign up ──▶ CLAIM ──▶ durable account (same principal)
                                   │
        (never claimed) ──────────┴──▶ retention TTL ──▶ purge
```

The telemetry envelope **already carries `anonymous_id` alongside `principal_id`** (`OBSERVABILITY_AND_ECONOMICS_PLATFORM_SPECIFICATION_V1` §2.1), and `Principal` is the ratified identity entity (DL-049) — so the substrate exists; this package promotes it from telemetry-only to a first-class pre-signup account state. The three parts below are **one decision surface**: identity (A) defines what gating (B) and retention (C) operate on.

---

## Part A — Provisional / anonymous identity → persistence → claim-on-signup

### A.1 Intent (owner ratifies)
A first-time user ingests, analyzes, and reaches orientation **with no account**, and on **save-to-keep signup** that work becomes a durable account **with full continuity** (same principal, same project, same Cognition-History / Attested records — nothing re-derived).

### A.2 Analysis & options (AI)
- **Option A1 — provisional `Principal` from first touch** *(recommended)*: create a `Principal` with `is_provisional = true` at session start; **claim = promote the row** (bind the auth identity, flip the flag) — not a data migration. Reuses DL-049 `Principal` and the existing `anonymous_id → principal_id` join; makes continuity structural; claim is a small idempotent transaction.
- **Option A2 — ephemeral session store, migrate-on-claim**: hold pre-signup work outside the principal model and copy it into a new principal at signup. *Simpler pre-signup, but claim becomes a data migration that risks breaking record/run identity (OB-5 / identity continuity) and duplicates storage logic.*
- **Option A3 — device/cookie token only**: no server principal until signup. *Lowest pre-signup cost; worst continuity and worst cross-device/abuse story.*

### A.3 Recommendation (AI — owner ratifies intent)
Adopt **Option A1 (provisional Principal, claim = promotion)**. Ratify the **intent** that the provisional principal is claimed-on-signup with full continuity; **engineering authors** the data model (provisional-principal representation, the claim transaction, idempotency, multi-device/already-authenticated collision handling, token security).

### A.4 Engineering-authored realization boundary
The provisional-principal schema, the claim transaction (atomicity/idempotency/rollback), provisional-token issuance & security, and collision rules are **engineering's to propose** (a 30_engineering data-model proposal). Owner ratifies that **claim preserves identity continuity and record integrity**; engineering proves it (claim-continuity test in the traceability matrix).

### A.5 Invariants
Provisioning computes/generates/governs nothing (OB-1). Records created anonymously **carry through claim unchanged** (OB-5 — claim is not reanalysis). The claimed account is the **same principal** (identity continuity), not a copy.

---

## Part B — DL-048 pre/post-signup gating + anonymous-usage cap

### B.1 Intent (owner ratifies)
Define what compute an **anonymous session** may consume before signup — enough to reach the aha (the 60s orientation), bounded as a **thin slice of the DL-048 Free envelope** to cap cost/abuse — and how entitlement transitions at claim.

### B.2 Analysis & options (AI)
Anonymous sessions are **sybil-cheap** (no verified identity), so the anonymous cap must be **tighter than Free** and rate-limited per device/IP, while still permitting the ratified anonymous first run.
- **Anonymous entitlement (recommended starting position):** **exactly one project**, **Fast Pass only**, within the **Free / Tier-1 per-run envelope** (§4b: ~20 artifacts / ~50k words / 1 active) and the §4c Free routing (nano/mini); **Deep Pass, project #2, and persistence all require signup**. Add a tight **per-session / per-device rate cap** (e.g., re-runs per hour) since anonymous traffic is abuse-prone.
- **Transition at claim (open — owner decides):** does pre-signup consumption **count against** the new account's Free monthly governor, or **reset** at claim? **Recommended:** **reset to the standard Free governor at claim** — don't penalize a converting user for the trial that converted them; the anonymous cap already bounded the pre-signup cost.
- **Mechanism:** this is a **new tier/identity-state row** in the §4c config (an "anonymous" column), **not new code** — the DL-048 enforcement, the §4c caps, and the DL-074 normalized-compute governor all apply unchanged; internal/test bypass stays excluded.

### B.3 Recommendation (AI — owner ratifies)
Ratify the **anonymous = one-project / Fast-Pass-only / Free-envelope / rate-capped** policy and the **reset-at-claim** transition as **starting config** (re-tunable from `AI Spend Recorded`, per §4c). Add the anonymous row to §4c on ratification. **Owner decides** the exact rate-cap numbers and the count-vs-reset question; **engineering authors** the enforcement wiring (reusing Wave B/S/I).

### B.4 Invariants
DL-048 enforcement is contracted and **reused via config** (no parallel enforcement path). Honest-limit disclosure (UP-4) applies at the anonymous cap — degrade/gate, **never silent overspend**. The DL-074 governor (tokens × model-tier weight) meters anonymous compute like any other.

---

## Part C — Pre-signup data retention & privacy

### C.1 Intent (owner ratifies)
Define **how long** an unclaimed provisional project/records are retained, the **security boundary** before a verified identity exists, and the **disposition** if a session is never claimed.

### C.2 Analysis & options (AI)
Pre-signup, the **provisional-session token is the only access credential** — it must be unguessable, scoped to the one session, and **expiring**; no cross-session access. Provisional artifacts are **user content without a verified owner**, so they should carry a **shorter, bounded retention** and be **purgeable**, not the canonical lifetime retention.
- **Retention options:** (C-i) **session-end deletion** — most privacy-preserving, but kills the "come back and claim" window; (C-ii) **bounded unclaimed TTL then hard-delete** *(recommended)*; (C-iii) retain-until-claimed indefinitely — worst privacy, sybil-storage risk.
- **Recommended starting position:** treat an **unclaimed provisional project as Operational-class** (not canonical) — **purge at an unclaimed TTL (recommended 30 days; owner sets)**. Canonical-record retention (project-lifetime + 1 yr, §4 Retention Durations) **attaches only at claim**, when a durable owner exists. This adds a **new "provisional / unclaimed" retention class** to Calibration Defaults §4 (to land at ratification).
- **Privacy:** minimal PII pre-signup (mirrors the feedback spec §4 posture); anonymized telemetry; a **never-claimed session must be purgeable and non-linkable to a person** (GDPR/CCPA erasure). A pre-signup privacy notice covers provisional artifacts.

### C.3 Recommendation (AI — owner ratifies)
Ratify: **provisional = Operational-class, bounded unclaimed TTL (recommend 30 days), hard-delete on expiry, canonical retention attaches at claim, never-claimed data purgeable and non-linkable.** Add the provisional retention class to §4 on ratification. **Owner sets** the exact TTL; **engineering authors** the purge job, token-security boundary, and erasure guarantees.

### C.4 Invariants
A never-claimed session **writes nothing canonical that outlives the TTL**. No provisional content is used for anything beyond the user's own session (no training, no benchmarking) before claim. OB-5 and epistemic safety unaffected (purge ≠ reanalysis).

---

## Framework 001A Review

- **Findings:** The three deferred GA items form **one decision surface** founded on a provisional-session lifecycle. The substrate already exists (`anonymous_id` in telemetry; `Principal` in DL-049). Each part has a clear recommended starting position consistent with ratified canon (DL-073/046/048/074) and reuses contracted mechanisms (DL-048 enforcement, §4c config, the DL-074 governor) rather than introducing parallel paths.
- **Concerns:** (1) **Claim continuity** is load-bearing — a botched claim would break identity continuity / record integrity (OB-5); it needs an explicit continuity test. (2) **Anonymous abuse** (sybil) is the real cost risk — the anonymous cap and per-device rate limit must be tight. (3) Two genuinely **open owner values** remain: the **count-vs-reset-at-claim** rule (B.2) and the **unclaimed TTL** (C.2) — surfaced, not assumed. (4) Each part adds a config row (§4c anonymous tier; §4 provisional retention class) to land at ratification. No epistemic-safety, doctrine, or constitution invariant is threatened.
- **Dependencies:** DL-073 (parent), DL-046 (60s), DL-048 (envelope + enforcement, Waves B/S/I), DL-049 (`Principal`), DL-074 (normalized governor + overage), DL-076 (GA stage gate), Calibration Defaults §4/§4b/§4c, the onboarding spec §V deferred identity/permissions/data-model work, and the feedback spec §4 (privacy precedent).
- **Recommendation:** **Ratify the intent of all three parts** (A1 provisional-Principal/claim-as-promotion; B anonymous = one-project/Fast-only/Free-envelope/rate-capped with reset-at-claim; C provisional Operational-class with a bounded unclaimed TTL), **delegate the realization to engineering** (data model, claim transaction, enforcement wiring, purge/erasure), and **decide the two open values** (count-vs-reset; TTL). On ratification this becomes one DL (or three, owner's call) with §4/§4c config follow-ons. **AI recommends; owner ratifies; engineering authors.**
- **Status:** Draft proposal ready for owner review. **GA-gated** (no build pressure until GA approaches); does not block Alpha/Beta. Pending owner ratification of intent + the two open values, then engineering realization proposals.

## Owner decision required (summary)

1. Ratify **Part A** intent — provisional `Principal`, **claim = promotion** with full identity/record continuity?
2. Ratify **Part B** intent — anonymous = **one project, Fast Pass only, Free per-run envelope, rate-capped**; and decide **count-vs-reset-at-claim** (recommended: **reset**)?
3. Ratify **Part C** intent — provisional = **Operational-class**, **bounded unclaimed TTL** (set the value; recommended **30 days**), canonical retention **attaches at claim**, never-claimed **purgeable/non-linkable**?
4. Confirm packaging: **one DL** for the GA deferred-signup realization, or **three** (A/B/C)? And authorize the engineering realization proposals (data model + enforcement + purge).

---

*This proposal packages the three engineering-realization items DL-073 deferred to before GA — provisional/anonymous identity with claim-on-signup, DL-048 pre/post-signup gating with an anonymous-usage cap, and pre-signup retention & privacy — on a shared provisional-session lifecycle that reuses the existing `anonymous_id` telemetry key and the DL-049 `Principal`. For each it states the owner-ratifiable intent, analyzes options, recommends a starting position consistent with ratified canon, and delimits the engineering-authored realization, while escalating (not assuming) the two genuinely open values (count-vs-reset-at-claim; the unclaimed retention TTL). It preserves every epistemic and onboarding invariant (OB-1/OB-5, identity continuity, the DL-046 60s, contracted DL-048 enforcement reused via config), introduces no doctrine, and is GA-gated so it imposes no Alpha/Beta build pressure. AI recommends; the owner ratifies intent; engineering authors the realization.*

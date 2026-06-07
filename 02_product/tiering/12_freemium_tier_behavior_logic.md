# Freemium / Tier Behavior Logic

## Freemium Should Include

- multi-input intake
- sample project buttons
- fast-pass confidence
- deep refinement
- basic Outcome Space
- limited fixes
- basic attention queue
- PDF/export snapshot
- lightweight sharing

### Viral primitives guaranteed on Free (P2 — Virality Audit 001)

The viral loop **seeds on Free**; monetize *depth/capacity*, not the *seed*. The following are **Free-tier capabilities** (subject only to bounded caps, never tier-gated off):

- **MRI share links** (SHARE-02) — the passive loop.
- **PDF export** (SHARE-04) — the portable, brandable artifact (Free = PDF only).
- **Comments** (COLLAB-01) — pull people into context.
- **CAF Review Requests — limited** (CRR) — the **active** loop. Available on Free with a **bounded daily/active CRR cap** (cost-governed under DL-048; tier-keyed config), since CRR is both the strongest virality mechanic *and* how Free users get stakeholder value. **Gate CRR *depth/volume*, not its existence.**

*(What stays constrained on Free remains below: collaboration **depth**, integrations, continuous monitoring, governance, export/sync — i.e. capacity and advanced surfaces, not the seed primitives.)*

---

# Freemium Constraints

Constrain:
- number of Outcome Spaces
- number of daily fixes
- number of simulations
- continuous monitoring
- integrations
- team collaboration depth
- governance policies
- export/sync capabilities

---

# Upgrade Prompt Rules (MON-04) — timing taxonomy

*Applied from `FREEMIUM_UPGRADE_PROMPT_TIMING_AUDIT_001.md` (owner-directed, 2026-06-05). Canonical term: **Upgrade Prompt** ("upsell notification" = same). Prompts are **commodity (MON-04, Category C)**; their friction triggers **consume the contracted DL-048 constraint-detection signals** (cap-hit, envelope-exceeded, budget gate). Timing **numbers are tunable config** — see Calibration Defaults §4d.*

**Standing rules:** no persistent upgrade wallpaper; every prompt is **contextual, value-based, and names the specific limit hit + the specific tier that relieves it** (no generic "upgrade"). Now concrete because **Tier-2 Basic** is defined (CHG-057).

**Two trigger classes (every prompt is exactly one):**
- **Value-moment** — fires at a positive peak; sells the *next* capability (rare, strict cooldown).
- **Friction-moment** — fires when a Tier-1 constraint is hit; an **honest limit disclosure + the specific relief.**

**Trigger taxonomy:**

| # | Trigger event (Tier-1) | Class | Target | Value-framed message (illustrative) | Timing |
|---|---|---|---|---|---|
| UP-1 | Daily **fix cap** reached (5/day) | friction | Basic | "You've used today's fixes — **Basic** gives you 20/day." | at cap-hit; once/day |
| UP-2 | Daily **chat cap** reached (20/day) | friction | Basic | "More questions? **Basic** raises your daily chat limit." | at cap-hit; once/day |
| UP-3 | **2nd active project** attempted (Free = 1) | friction (high-intent) | Basic | "Free includes 1 active project — **Basic** gives you 3." | immediate; no cooldown |
| UP-4 | **Envelope exceeded** → partial orientation | friction + **honest disclosure** | Basic | "This is a **partial** analysis — your project exceeds the Free size. **Basic** analyzes projects up to ~100k words." | **fire with the Wave E partial-orientation disclosure — one surface** |
| UP-5 | **Deep-runs/day** cap reached (2/day) | friction | Basic | "You've used today's deep analyses — **Basic** gives you more." | at cap-hit; once/day |
| UP-6 | **Monthly budget** gate reached | friction (soft) | Basic | "You've reached this month's analysis limit." | once/month; gentle |
| UP-7 | **Confidence improved / outcome achieved** | value | Pro | "**Continuous monitoring** can protect this confidence over time." *(→ Pro exec-monitoring, forward capability)* | at value peak; rare |
| UP-8 | **First MRI delivered** (activation) | value | — / Basic (soft) | celebrate value; no hard sell | once, first project |

**Global guards (all triggers):** never interrupt an active Fast/Deep pass; not before first value (first MRI) delivered; honor per-trigger cooldown + a global per-day cap (Calibration §4d); no persistent wallpaper.

**UP-3 precondition — attempt → trigger (required).** The **Create Project** affordance **stays enabled at the active-project limit.** A Free user at the cap may **attempt** a 2nd active project; the attempt is **gated server-side (API `POST /projects` → `422`)** and surfaces UP-3 with **two resolutions: upgrade, *or* archive the current project** (archiving is reversible and frees the slot). The control is **never disabled or hidden** at the limit — doing so would suppress the highest-intent upgrade trigger. (Project Dashboard §D and Onboarding §I carry the matching UX rule; limit *values* per Tier Definitions, presented not computed.)

**Limit-reached interaction rule — ALL monetization caps (Seam Audit 001 S1–S3).** UP-3 generalizes: **every** limit-bearing affordance follows one pattern — it **stays enabled**, the attempt is **gated server-side** (`429`/`422` + `Retry-After` where applicable), and the surface presents the **matching UP prompt + resolution(s)**. **Never disabled/hidden** (suppresses the trigger); **never a raw error** (always the value-framed prompt).

| Cap | Affordance (surface) | Gate | Prompt | Resolutions |
|---|---|---|---|---|
| Active project | Create Project (Dashboard/Onboarding) | `422` | UP-3 | upgrade · archive current |
| Daily fix | Apply Suggested Fix (Recommendation Panel / Issue Panel / Artifact view) | `429` | UP-1 | upgrade · wait for daily reset |
| Daily chat | Chat send (OSLO Chat) | `429` | UP-2 | upgrade · wait for reset |
| Deep-runs/day | Analyze / trigger reanalysis (Project Overview) | `429` / DL-048 gate | UP-5 | upgrade · wait · keep last analysis |
| Monthly budget | any AI action | DL-048 gate | UP-6 | upgrade · wait for month reset |

Each listed UX surface carries a pointer to this rule. Values per Tier Definitions (presented, not computed); no governance, no computation in the surface.

**Optimality objective (what TEL-07 tunes against):** maximize **prompt → conversion** while keeping the **dismissal/annoyance signal** (rapid-dismiss, repeat-ignore) below threshold. A trigger that under-converts **and** over-annoys is auto-suppressed and re-tuned. "Optimal timing" = this objective, not a fixed schedule.

---

# Virality — Surface Attribution + Share-Prompt Timing (P1/P3 — Virality Audit 001)

*Applied from `RELEASE_1_VIRALITY_K_FACTOR_AUDIT_001`. Commodity (SHARE/MON); **value-aligned** — user-initiated, honest, no dark patterns; reuses the Upgrade-Prompt two-class trigger model. Timing numbers → Calibration §4e.*

## Viral surface attribution (P1)

Every shared artifact is a viral surface. **PDF exports (SHARE-04)** and **shared MRI links (SHARE-02)** carry **tasteful attribution + CTA** — e.g. *"Made with OSLO — map your own project's understanding,"* linking to project creation. **Honest attribution, not a watermark gimmick; never misleading.** This is the cheapest i×c lever (pure presentation).

## Share / Invite prompt timing (P3)

Reuses the Upgrade-Prompt **two-class** model, but here the dominant class is **value-moment** (sharing is sold at a peak, not at a wall):

| # | Trigger event | Class | Message (illustrative) | Timing |
|---|---|---|---|---|
| SP-1 | Strong MRI delivered / first MRI | value | "Share this understanding with your stakeholders." | at value peak; once/project |
| SP-2 | Finding ready for stakeholder input (REC-05 validation rec) | value | "**Invite a stakeholder to strengthen this finding**" → CRR | in-context on the finding |
| SP-3 | Confidence raised / outcome milestone | value | "Share your progress." | at milestone; cooldown |
| SP-4 | Export completed (PDF) | value (soft) | "Your PDF carries a link — invite others to map their own." | once per export, non-modal |

**Guards (reuse §4d pattern):** user-initiated only (no autonomous sends); never interrupt an active pass; value before ask (not before first MRI); per-trigger cooldown + global cap (Calibration §4e); no persistent wallpaper. **Foreground SP-2** — because a CRR response becomes evidence (CRR-04), "invite a stakeholder" both grows the network *and* improves the user's own understanding (value = virality). **Objective (TEL-06):** maximize invites→joins→conversions while keeping the annoyance signal bounded.

## Virality measurement — k-factor (P6)

Make virality a **tracked objective**, not a vibe. From **TEL-06** (shared / invited / joined / returned / converted) + **TEL-02** (invited / accepted / activated):

- **k (virality coefficient) = i × c** — `i` = exposures (shares + invites) generated per active user per window; `c` = fraction of those exposures that convert to an **activated** new account. **k > 1 = self-sustaining** growth.
- **Per loop, separately:** **active (CRR)** · **passive (MRI share links)** · **portable (PDF)** — so you know *which* loop drives growth and where to invest.
- **Cycle time T:** median exposure→conversion time per loop (governs how fast k compounds).
- **Exclusions:** **Internal accounts excluded** (CHG-059) — test traffic must never inflate k.
- **Window + targets:** rolling window + k target are **Calibration §4f** config (owner-set; track-only until a baseline exists). Alert on sustained decline.
- **Surface:** a **virality dashboard** (k, i, c, T per loop, segmented) — a natural live artifact, refreshed from telemetry.

This is the objective function P1–P5 are tuned against; pure measurement, no cognition.

---

# Tier 3 — Pro

Unlock:
- continuous monitoring
- unlimited or expanded fixes
- more simulations
- execution integration *(3rd-party platforms — forward capability; see tier-progression backlog)*
- richer artifact optimization

---

# Tier 4 — Team

Unlock:
- collaboration
- shared spaces
- approvals
- execution synchronization
- advanced shared views

---

# Tier 5 — Enterprise

Unlock:
- governance policies
- organizational thresholds
- portfolio cognition
- agent governance
- cross-system orchestration

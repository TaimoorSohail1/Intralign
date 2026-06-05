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

**Optimality objective (what TEL-07 tunes against):** maximize **prompt → conversion** while keeping the **dismissal/annoyance signal** (rapid-dismiss, repeat-ignore) below threshold. A trigger that under-converts **and** over-annoys is auto-suppressed and re-tuned. "Optimal timing" = this objective, not a fixed schedule.

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

# In-Product Feedback Capture — Capability Specification v1

- **Status:** Active · Release 1 · **Date:** 2026-06-19 · owner-adopted decisions baked in (§6).
- **Type:** Product capability spec. **Commodity / non-cognitive** (DL-043 Categories C/E/F; per the Experience-Surface ↔ Responsibility Crosswalk, DL-064). Built with normal engineering judgment; **touches no cognitive contract**.
- **Source:** Owner direction 2026-06-19 (capture in-product feedback: defects, enhancements, satisfaction); the 2026-06-19 feedback best-practice review.

---

## 0. Governance classification (read first)

This is **commodity plumbing**, like Notifications / Settings / Telemetry — it maps to **no cognitive responsibility** and emits **no canonical content**.

**Critical boundary — feedback ≠ acceptance (owner-acknowledged 2026-06-19).** *Product feedback about the app* (a bug, a feature idea, a satisfaction rating) is commodity and handled here. *User input on the analysis* — accepting, rejecting, deferring, or clarifying a Finding/Recommendation — is **NOT feedback**; it is governed **cognition/acceptance** (Wave U / DL-055). The two flows must be **visibly separate**: this capability **never alters an assessment** (preserves **OB-5: only reanalysis changes assessment**) and writes **nothing canonical**. *(Per the crosswalk's own rule: if unsure whether something is commodity, treat it as cognitive and escalate.)*

## 1. Three jobs, one entry point

A single "Give feedback" entry point, **intent-routed** to the right surface:

1. **Defect / bug report** — a **structured form**: what happened, expected vs. actual, steps to reproduce; **context auto-attached** (current project id, orientation/analysis state, app version, route) — anonymized where possible. Routes to the engineering tracker (e.g. Linear), tagged.
2. **Feature request / enhancement** — **lightweight capture**, feeding (at GA) a **voted/public roadmap board** so users see status and upvote — doubles as a roadmap-signal engine.
3. **Satisfaction / sentiment** — **contextual micro-surveys** (≤3 questions), triggered at moments, not by email (in-app surveys within ~2 min of an interaction outperform email ~3–4×).

## 2. Survey cadence (owner-adopted)

- **CSAT** right after the first **60-second orientation** (the aha moment) and after a **Deep Pass**.
- **CES** after **onboarding completion**.
- **NPS** **quarterly** per active user.
- Internal/test accounts **excluded** from sampling (mirrors the DL-048 internal-entitlement exclusion).

## 3. Routing, tagging, and data

- **Intent routing:** the entry point asks "report a problem / suggest an improvement / rate your experience" and opens the matching surface.
- **Tag every item** by **type** (bug · feature · UX · praise) × **product area** (onboarding · MRI · Findings · Recommendations · ingestion · chat · billing) × **source** (in-app · survey · support), into **one backlog** for triage.
- **Events:** rides the observability/telemetry plane as **non-canonical events** (`Feedback Submitted`, `Survey Shown/Answered/Dismissed`). No canonical record; no assessment linkage.

## 4. Privacy & identity (ties to DL-073)

- Capture **minimal PII**; anonymize attached context where feasible.
- For **anonymous / pre-signup** users (DL-073), feedback is tied to the **session**, not an identity; respect the same pre-signup retention/privacy decisions (DL-073 §4.4).

## 5. Distinctness from adjacent surfaces

- **Not OSLO Chat (CHAT-01…04)** — Chat is a Disclose-class surface about *understanding*; app-feedback is commodity and separate.
- **Not the acceptance affordance** (Wave U) — see §0.
- **Not Notifications** — Notifications surface drift/awareness; feedback flows user → team.

## 6. Adopted decisions & phasing (owner, 2026-06-19)

- **Build/buy — built-in for Alpha/Beta, dedicated tool at GA.** Alpha/Beta ships a **lightweight in-house** form (bug + idea) + the §2 micro-surveys (CSAT post-orientation, CES post-onboarding) for the controlled cohort. **GA** adopts a dedicated tool (e.g. Sprig / Canny / Featurebase / Userflow) + a **public voted roadmap**, and broadens NPS/CSAT cadence.
- **Classification:** commodity (non-cognitive); routes as a product/commodity capability — **no DL or cognitive contract required**. The one governance-sensitive invariant is the **§0 feedback-vs-Wave-U boundary** (owner-acknowledged).
- **Build note:** no new cognitive contract, no epistemic invariant, no governance/execution workflow; emits non-canonical events only.

---

*This specification defines the Release 1 in-product feedback-capture capability as commodity, non-cognitive plumbing: one intent-routed entry point over three jobs (structured bug reports, feature requests, and contextual ≤3-question satisfaction micro-surveys), tagged by type/area/source into one triage backlog, riding telemetry as non-canonical events, with built-in Alpha/Beta delivery and a dedicated tool + public roadmap at GA. It preserves the strict boundary that product feedback about the app is never user input on the analysis (Wave U / DL-055) and never alters an assessment (OB-5), introducing no cognition, no canonical content, and no governance or execution workflow.*

# Source Summary — OSLO R1 Product Scan

**Scan date:** 2026-07-09 · **Reconciled to v4 baseline:** 2026-07-09
**Scope (client-selected):** R1 product artifacts only. Governance proposals, decision-log drafts, dev-readiness monitors, and reconciliation packets in the folder were excluded as engineering/release noise per the skill's Source Filtering Rule.
**Baseline of record:** `product-design/oslo_r1_experience_mockup_v4.html` (in the connected `oslo-knowledge-base` repo). Initial scan used v2 from the `OSLO Knowledge Base` project folder; reconciled to v4 after the owner flagged it. v4 folds in DL-094 (issue lifecycle), DL-095 ("Issues" label), DL-096 (Overview redesign), DL-086/098 (5-band scheme).

## Sources scanned

| Source | Type | Classification | Use |
|---|---|---|---|
| `product-design/oslo_r1_experience_mockup_v4.html` (217 KB, 2026-07-09) | **Baseline of record** — target-experience prototype | Design evidence | Primary UX/interaction source; illustrative, not canon |
| `product-design/oslo_r1_overview_redesign_mockup.html` (2026-07-09) | Overview redesign review mockup (DL-096) | Design evidence | Confidence-led Overview reference |
| `oslo_r1_experience_mockup_v2.html` / `_v3.html` | Prior baselines (superseded) | Design evidence | History; referenced by DL-088/090/093 (v2), DL-094/095 (v3) |
| `product-design/OSLO_R1_UX_PROTOTYPE_NOTES_AND_GAP_AUDIT.md` (39 KB) | Prototype decisions + canon mappings + spec-gap audit + v3/v4 changelog | Product + Design evidence | Primary decision source (canon-traceable) |
| `OSLO_R1_COGNITIVE_AUDIT.md` | Cognitive-load walkthrough (Nielsen/Hick/Miller) | Design evidence | UX quality constraints; issue register C1–C9 |
| `OSLO_ONBOARDING_POSITIONING_DRAFT.md` | Positioning spine + onboarding copy (draft for owner ratification) | Product evidence (positioning) | Voice, value framing, guardrails |
| `OSLO_Release_1_Workflow.svg` / `.png` | End-to-end product workflow diagram (from OSLO_RELEASE_1_MASTER_SPEC §5,§6,§8,§14) | Product evidence | Canonical flow spine |

## What was extracted

**Product goal / mission.** Help users understand project reality faster, more completely, and more accurately. OSLO is the *strategic layer above* the user's PM tools (Asana/Jira/spreadsheet) — not another task tracker. Category: Outcome Orchestration; descriptor "Strategic project leadership."

**Primary persona.** Project/program managers who want to move from task-herding to strategic influence ("AI-first PM"). Secondary: non-PMs who manage projects.

**Actors.** User (PM), System, AI Agent (OSLO analysis/chat), Collaborators/Viewers.

**Core flow spine (from workflow diagram).** Alpha access & activation → Intake (upload / describe / template / guided Q&A) → **Fast Pass ≈60s** (Extract·Infer·Construct·Evaluate → Orientation Confidence, Initial MRI, Top Issues, Clarification Requests, Suggested Fixes) → **60-second orientation lands on MRI** → **Deep Pass** auto-runs (highest-compute, supersedes) → **Core Improvement Loop** (event-driven: no change → no reanalysis).

**Product data concepts.** Project, Plan artifacts / Artifacts (7: Intent·Context·Scope·Requirements + WBS·Schedule·Resources), **Issues** (user-facing label per DL-095; "Finding" internal) with severity → CAF and lifecycle **Open→Addressed→Resolved** (DL-094), Recommendations / Resolution Paths / Selected Path + "Apply this fix", Confidence (0–100 understanding maturity + band), Reliability (Coverage·Evidence·Assessability), CAF = Clarity·Alignment·Feasibility on a shared **5-band scale** (Very Low…Very High, DL-086/098), PlanFact (Derived vs Attested), Clarification Requests, History/timeline (append-only), Comments, Notifications.

**AI behaviors.** Advisory-only (OSLO advises; user decides/acts). Event-driven reanalysis only. Only reanalysis changes the assessment. Confidence ≠ health/success/probability. Findings never resolved by hand. Simulated in prototype (no real model).

**User-visible constraints.** Free tier: honest limits, non-destructive archive, visibility-first billing (no enforcement in R1), save-to-keep gate after orientation, anonymous first-run Fast-Pass-only. Accessibility WCAG 2.1 AA target. Two-theme (dark default / light).

**Contradictions found.** See `contradictions.md` (MRI-in-Overview vs NAV-C3 "MRI co-primary"; stale "Recommendation Workspace" in UI inventory vs ratified Panel Model Decision 001).

**Escalated / genuine spec gaps.** CAF Review Requests (CRR) virality loop — not defined in any R1 surface spec; escalated to owner, not invented.

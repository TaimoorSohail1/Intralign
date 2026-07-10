# Decision Log — OSLO R1

All decisions locked from R1 product artifacts unless marked otherwise. Illustrative values are flagged, not ratified.

**Baseline: `oslo_r1_experience_mockup_v4.html` (2026-07-09, reference of record).** v4 supersedes v3/v2 and integrates DL-094 (issue lifecycle), DL-095 ("Issues" label), DL-096 (Overview redesign), DL-086/098 (5-band scheme). v2/v3 preserved as prior baselines. Decisions D002/D008/D009 were updated from the v2 scan; D017–D020 are new from v4.

## Decision 001: Advisory-only doctrine
Status: Locked from docs · Type: Product Constraint · Area: Global · Slice: All · Feature: — · Question ID: — · Source: Onboarding Positioning §Guardrails (DL-043/047); Workflow diagram · Source classification: Product evidence
Decision: OSLO advises; the user decides and acts. No copy or behavior implies OSLO plans/decides/runs the project.
Rationale: Core doctrine; credibility differentiator.
Impacts: product-requirements.md, all slice docs, copy.

## Decision 002: Confidence = understanding maturity (neutral)
Status: Locked from docs (updated for v4) · Type: Product Requirement · Area: Confidence · Slice: 3 · Source: Confidence Doctrine; Visual §1.2; UX Notes §2/§4c; **DL-096, DL-086/098** (v4)
Decision: Confidence is a 0–100 maturity index + band; never health/success/readiness/probability/risk; never traffic-light colored. Number never shown bare (band + reliability + cause always present). **v4 (DL-096): Overview is confidence-led — focal score + CAF maturity bars (band word + hover) + quiet change-delta trend + "Why" disclosure. The confidence RING, green box, and Current/From-OSLO pills are REMOVED.** Band vocabulary = the shared **5-band scheme (DL-086/098): Very Low · Low · Moderate · High · Very High**, used by both the Confidence index and the CAF dimensions (no separate thresholds).
Rationale: Category-error prevention; v4 leaner confidence-led Overview.
Impacts: product-design.md, slice-03, slice-07, theme-system.md.
Supersedes: v2 confidence ring + 4-band vocabulary.

## Decision 003: Severity-only color semantics
Status: Locked from docs · Type: Product Design · Area: Color · Slice: All · Source: UX Notes §4c; Visual §1.2
Decision: Red/amber/green only for finding severity (critical/moderate/warning). Confidence/CAF use neutral maturity ramp.
Impacts: theme-system.md, slice-03, slice-04, slice-06.

## Decision 004: Seven planning artifacts
Status: Locked from docs · Type: Product Data · Area: Artifacts · Slice: 5 · Source: DL-077; UX Notes §2
Decision: Intent · Context · Scope · Requirements (understanding core) + WBS · Schedule · Resources (execution). User-facing "Plan sections"; "WBS"→"Work breakdown".
Impacts: slice-05, product-data.md.

## Decision 005: Intake → Fast Pass → Orientation/MRI → Deep Pass
Status: Locked from docs · Type: Journey · Area: Analysis flow · Slice: 2 · Source: DL-046; Workflow diagram
Decision: Intake (upload/describe/template/guided) → Fast Pass ≈60s (Extract·Infer·Construct·Evaluate) → 60s orientation lands on MRI → Deep Pass auto-runs (non-blocking) and supersedes. User-facing "Initial/Extended Analysis".
Impacts: slice-01, slice-02, slice-03.

## Decision 006: Event-driven reanalysis only
Status: Locked from docs · Type: AI Behavior · Area: Analysis · Slice: 5 · Source: UX Notes §6.3/§6.4; Orientation State Model
Decision: No manual reanalyze. Editing an artifact or updating a finding auto-reanalyzes (Saved→stale→Reanalyzing→Up to date). Only reanalysis changes the assessment; last-good preserved on failure with retry.
Impacts: slice-05, slice-06, slice-07.

## Decision 007: MRI heatmap-primary
Status: Locked from docs · Type: Screen/Interaction · Area: MRI · Slice: 4 · Source: MRI Model; UX Notes §2/§6.8
Decision: Attention Map = heatmap (plan-section × CAF) primary, field view secondary. Cells route via openFindingsFor(section,dimension): one match → open finding; else scoped findings list.
Impacts: slice-04, slice-06.

## Decision 008: Issue Panel Model + lifecycle
Status: Locked from docs (updated for v4) · Type: Screen/Interaction · Area: Issues · Slice: 6 · Source: Finding Panel spec (Option A); Finding System §C; **DL-094**, **DL-095** (v4)
Decision: Contextual Issue Panel (Header→Why→Evidence→CAF impact→Recommendations→History→Reanalysis). **Lifecycle Open → Addressed → Resolved** (the Acknowledge stage is removed, DL-094). Issues never resolved by hand — only reanalysis moves them. **User-facing label "Issues"; "Finding" is the internal object (DL-095).** List toggle = "By dimension / By severity."
Rationale: v4 simplifies the lifecycle and retires "Findings/weaknesses" from the UI.
Impacts: slice-06, all copy.
Supersedes: v2 lifecycle (detected→acknowledged→addressed→closed).

## Decision 009: Panel Model for recommendations (Decision 001, 2026-05-31)
Status: Locked from docs (updated for v4) · Type: Screen/Interaction · Area: Recommendations · Slice: 6 · Source: Reconciliation Decision 001; RECOMMENDATION_PANEL_SPEC RP-12; **DL-094** (v4)
Decision: Recommendations exist only inside the Issue context; no standalone Recommendation Workspace or orphan roll-up. Selecting a Resolution Path = Selected Path (Attested). **v4 (DL-094): single-action "Apply this fix" where OSLO can draft** (internal `validated`/`recommended` states — no UI change). Overview keeps a pointer-only Recommendations summary.
Impacts: slice-03, slice-06.

## Decision 010: Reliability qualifier + false-confidence flag
Status: Locked from docs · Type: Product Requirement · Area: Overview · Slice: 3 · Source: Reliability Model V1; Confidence Model CONF-06
Decision: Reliability card with Coverage · Evidence availability · Assessability (High/Moderate/Low), independent of CAF. Flag when a high confidence band sits on low reliability.
Impacts: slice-03, slice-07.

## Decision 011: Epistemic notation (Derived / Attested)
Status: Locked from docs · Type: Product Data · Area: Editor · Slice: 5 · Source: DL-043; PlanFact
Decision: Text is Derived (OSLO) by default; edit/confirm → Attested (you) = plan fact. Plain labels "From OSLO" / "Confirmed by you."
Impacts: slice-05.

## Decision 012: Plain-language display map
Status: Locked from docs · Type: Product Design · Area: Copy · Slice: All · Source: UX Notes §6.8
Decision: Canonical internal terms preserved; user sees Plan sections, Work breakdown, Clarity·Alignment·Feasibility, From OSLO, Confirmed by you, Initial/Extended Analysis, Still updating.
Impacts: all copy, product-design.md.

## Decision 013: Three-context global shell
Status: Locked from docs · Type: Routing · Area: App shell · Slice: 8 · Source: GLOBAL_NAVIGATION NAV-6/C3; UX Notes §4b
Decision: Workspace › Project › Object. Left rail = Project/Object; top-left = Workspace Home + project switcher; top-center = Overview·MRI·Artifact (primary), Collaboration·History (secondary); top-right = Settings/Account. Command palette (⌘K).
Impacts: slice-08, all slice prototypes (shell).

## Decision 014: Free-tier visibility-first
Status: Locked from docs · Type: Scope · Area: Tiering · Slice: 10 · Source: DL-048/DL-080; UX Notes §6.6
Decision: Honest at-cap upgrade-or-archive modal (non-destructive archive frees slot), quiet "Free · Upgrade" chip, save-to-keep after orientation, anonymous first-run Fast-Pass-only. Billing/enforcement deferred; tier numbers illustrative.
Impacts: slice-01, slice-10.

## Decision 015: Two-theme + accessibility
Status: Locked from docs · Type: Theme · Area: Visual · Slice: All · Source: Visual Design §1/§3; UX Notes §6.2/Tier 4
Decision: One semantic token set; dark default, light overrides same names; neutral maturity ramp per theme; WCAG 2.1 AA target (focus-visible rings, keyboard nav, reduced-motion, no-animation-during-analysis).
Impacts: theme-system.md, all prototypes.

## Decision 016: Prototype is client-side only
Status: Locked from docs · Type: Prototype · Area: Build boundary · Slice: All · Source: Skill boundary + prototype nature
Decision: Single openable HTML per slice; Tailwind CDN + plain JS + localStorage + fake data + simulated AI. No server/backend/API/DB/auth/real-AI.
Impacts: all prototypes.

## Decision 017: User-facing label "Issues" (DL-095)
Status: Locked from docs · Type: Product Design · Area: Copy/Issues · Slice: 6 · Source: DL-095 (v4)
Decision: The user-facing term is "Issues." "Findings/weaknesses" retired from the UI; "Finding" remains the internal object. The list toggle is "By dimension / By severity."
Impacts: slice-06, all copy, decision-tree.md, slice-map.md.

## Decision 018: Simplified issue lifecycle Open→Addressed→Resolved (DL-094)
Status: Locked from docs · Type: Product Requirement · Area: Issues · Slice: 6 · Source: DL-094 (v4)
Decision: Lifecycle is Open → Addressed → Resolved; the Acknowledge stage is removed. Single-action "Apply this fix" where OSLO can draft; internal `validated`/`recommended` states are not surfaced.
Impacts: slice-06, slice-07 (timeline events).
Supersedes: v2 lifecycle.

## Decision 019: Overview redesign — confidence-led, ring removed (DL-096)
Status: Locked from docs · Type: Product Design · Area: Overview · Slice: 3 · Source: DL-096 (v4); overview_redesign_mockup
Decision: Overview leads with a focal Confidence score + "Understanding is forming" meaning line + reliability qualifier; CAF shown as maturity bars (band word + hover detail, lowest dimension flagged as "the limit"); quiet change-delta trend sparkline; "Why" disclosure; then Start here → top issue, Progress ledger, and a collapsed "More" (Project summary). Removed: confidence ring, green box, Current/From-OSLO pills.
Impacts: slice-03, theme-system.md.
Supersedes: v2 confidence ring Overview.

## Decision 020: Shared 5-band scheme (DL-086/098)
Status: Locked from docs · Type: Product Data · Area: Confidence/CAF · Slice: 3 · Source: DL-086, DL-098 (v4)
Decision: One 5-band scheme — Very Low · Low · Moderate · High · Very High — owns the edges for both the Confidence index and the CAF dimensions. Supersedes the earlier 4-band vocabulary; no separate thresholds.
Impacts: slice-03, slice-04, slice-07, theme-system.md.
Supersedes: v2 4-band vocabulary.

---

# Slice 1 — Access & Onboarding (locked 2026-07-09)

## Decision 021: Release-phase gate — anonymous access is GA-only
Status: Client override/clarification · Type: Scope · Area: Access/Onboarding · Slice: 1 · Question ID: F4Q1 (clarification) · Source: owner direction 2026-07-09
Decision: R1 is the **Alpha** release. **Alpha and Beta are invite-only; users are never anonymous in those phases** and are authenticated from activation onward. **Anonymous product access begins at GA.** Therefore the anonymous first-run, the save-to-keep-after-orientation gate, and anonymous→claimed carry-through are **GA-phase** capabilities, not Alpha/Beta.
Rationale: Owner phasing decision; keeps Alpha/Beta gated to invited users.
Impacts: slice-01 docs + prototype, canonical-truth.md, slice-map.md. Governs D024–D026 below.

## Decision 022: Invite-gated Alpha access (simulated)
Status: Accepted recommendation · Type: Routing · Area: Access · Slice: 1 · Question ID: F1Q1 · Source: Workflow diagram; owner
Decision: Access model = invite-gated Alpha — Invitation email → Account activation → Welcome. Prototype simulates activation (no real auth); real auth provider owner-TBD.
Impacts: slice-01.

## Decision 023: Four start methods; Guided Q&A out for R1
Status: Accepted recommendation · Type: Scope · Area: Intake · Slice: 1 · Question ID: F2Q1 · Source: v4; workflow diagram (escalated)
Decision: R1 start methods = Upload/Attach · Describe (composer) · Templates (Event, Marketing Campaign, Product/Software Launch, Strategic Initiative, Generic Project Plan) · Sample project. **Guided step-by-step Q&A intake is OUT for R1** (in the workflow diagram, not built in v4); revisit post-R1.
Impacts: slice-01, slice-02.

## Decision 024: Anonymous Fast-Pass-only first run — GA-phase
Status: Accepted recommendation (GA-gated per D021) · Type: Product Requirement · Area: Onboarding · Slice: 1 · Question ID: F3Q1 · Source: DL-080; owner
Decision: An anonymous user runs a sample or own brief through Fast Pass only (~10s, no signup) and lands on orientation; Extended Analysis and keeping require signup. **Active at GA only** — in Alpha/Beta the equivalent value-first flow runs inside the invited, authenticated session.
Impacts: slice-01.

## Decision 025: Save-to-keep gate after orientation — GA-phase
Status: Accepted recommendation (GA-gated per D021) · Type: Product Requirement · Area: Onboarding · Slice: 1 · Question ID: F4Q1 · Source: DL-073; owner
Decision: Signup fires after orientation (save-to-keep); before signup the session is explore-only. **GA-phase.** In Alpha/Beta the user already has an account from activation, so no save-to-keep gate applies.
Impacts: slice-01, slice-10.

## Decision 026: Signup method (email, simulated) + claim-through — GA-phase
Status: Accepted recommendation (GA-gated per D021) · Type: Product Requirement · Area: Auth · Slice: 1 · Question ID: F4Q2/F4Q3 · Source: owner; v4 copy
Decision: Signup is email-based save-to-keep (simulated in prototype; real auth owner-TBD). Anonymous work is claimed and carried through unchanged on signup. Both are **GA-phase** (see D024/D025).
Impacts: slice-01.

## Decision 027: One-time strategic-chain orientation + advisory framing
Status: Accepted recommendation · Type: Journey · Area: Onboarding · Slice: 1 · Question ID: F5Q1 · Source: Onboarding Positioning; v4
Decision: One-time, dismissible strategic-chain orientation on first run (Understanding·OSLO → Judgement·you → Decision·you → Oversight·you); persistent advisory footer. Sunsets with proficiency; re-openable from Settings → Help. Applies in all phases.
Impacts: slice-01.

## Decision 028: Session management + logout
Status: Accepted recommendation · Type: Screen/Interaction · Area: Session · Slice: 1 · Question ID: F6Q1 · Source: owner (v4 gap)
Decision: Add logout in the account menu + "stay signed in" (illustrative persistence, simulated via localStorage). Real session/timeout policy owner-TBD.
Impacts: slice-01, slice-08.

## Decision 029: Hero headline A + descriptor
Status: Locked from docs · Type: Product Design · Area: Copy · Slice: 1 · Question ID: ND-1 · Source: v4 (already shipped)
Decision: Hero headline **A — "See your plan like a strategic leader."**; wordmark descriptor **"Strategic project leadership."**
Impacts: slice-01, all onboarding copy. Resolves ND-1.

## Decision 030: "Sample project" is an all-phase start method (user-initiated); only anonymity is GA
Status: Client override · Type: Product Requirement · Area: Intake/Onboarding · Slice: 1 · Question ID: prototype feedback (F3Q1 refinement) · Source: owner 2026-07-09
Decision: "See it on a sample project" is available to **Alpha/Beta users too** (authenticated), not GA-gated. It loads the sample brief into the composer and the **user initiates ingestion/analysis** — no ~10s auto-run. What remains **GA-only** is the *anonymous, no-signup* framing (D024) and the save-to-keep gate (D025). So: the sample **method** = all phases + user-initiated; **anonymous** = GA.
Rationale: Alpha/Beta users should be able to try the sample; auto-run removes user agency over ingestion.
Impacts: slice-01 prototype + user-experience.md, product-detail.md, frontend-ui.md, e2e-test-scenarios.md. Refines D024 (splits "sample method" from "anonymous").

## Decision 031: Fast Pass pacing ≈30s across interstitials
Status: Client override · Type: Product Requirement · Area: Analysis UX · Slice: 1/2 · Question ID: prototype feedback (pacing flag) · Source: owner 2026-07-09
Decision: The Fast Pass ("Initial Analysis") simulated wait is paced to **≈30 seconds**, distributed across the interstitial screens and rotating copy so the flow reads realistically. (Real Time-to-First-MRI remains an owner-TBD NFR; ≈30s is the prototype pacing.)
Impacts: slice-01 prototype, slice-02 (analysis), frontend-ui.md, user-experience.md.

## Decision 032: Hide the GA-phase annotation from the Alpha onboarding screen
Status: Client override · Type: Product Design · Area: Onboarding · Slice: 1 · Question ID: prototype feedback · Source: owner 2026-07-09
Decision: The "GA PHASE · NOT ACTIVE IN ALPHA" card/caption must **not** be visible on the Alpha onboarding/intake screen. The GA anonymous + save-to-keep content appears **only when the GA preview toggle is active** — no inert labelled GA card in the default Alpha view.
Rationale: The preview toggle already exposes GA behavior; the standing annotation is clutter (single-home + hover principle, §6.7).
Impacts: slice-01 prototype, frontend-ui.md.

## Decision 033: Accepted attachment file types (R1 Alpha)
Status: Client override · Type: Product Constraint · Area: Intake · Slice: 1/2 · Source: owner 2026-07-09
Decision: Attach documents accepts **PDF, DOCX, TXT, MD, PPTX, XLSX, CSV** plus **paste/typed** text (options 1 + 3 combined). Illustrative caps: ~10 MB/file, up to ~10 files. Tier-based size rules (DL-048 over-size Free handling) remain owner-TBD for GA (moot in invite-only Alpha).
Rationale: Cover the common plan/brief document set including slides and spreadsheets.
Impacts: slice-01 product-data.md/product-detail.md/frontend-ui.md/prototype, canonical-truth.md.

## Decision 034: Ingestion depth (R1)
Status: Client override · Type: Product Requirement · Area: Analysis/Intake · Slice: 1/2 · Source: owner 2026-07-09
Decision: OSLO extracts readable text from all supported types and synthesizes it into the seven plan sections (Intent·Context·Scope·Requirements·WBS·Schedule·Resources), **plus structured-table extraction** for spreadsheets/CSV and in-document tables (rows inform Resources/Schedule where applicable) — the coherent depth given XLSX/CSV are accepted (D033). **No OCR of scanned/image-only content in R1** (owner-TBD for a later release).
Rationale: Matches the accepted file set; keeps OCR out of Alpha scope.
Impacts: slice-01/slice-02 docs; flag OCR as owner-TBD.

# Slice 2 — Intake & Fast-Pass Orientation (locked 2026-07-09, all recs accepted)

## Decision 035: Intake constructs all seven plan sections
Status: Accepted recommendation · Type: Product Requirement · Area: Intake/Analysis · Slice: 2 · Question ID: F2.1Q1 · Source: v4; DL-077
Decision: From any intake (even a thin brief), OSLO constructs all seven plan sections (Extract·Infer·Construct); inferred content is marked **From OSLO (Derived)** and reliability-qualified; thin/absent evidence raises Clarification Requests rather than fabricating certainty.
Impacts: slice-02, slice-05, product-data.md.

## Decision 036: Fast Pass completion time = measured, not fixed
Status: Accepted recommendation · Type: Product Requirement · Area: Analysis UX · Slice: 2 · Question ID: F2.2Q1 · Source: DL-046 (owner-TBD NFR); D031
Decision: The "Initial Analysis complete" surface shows the **measured** Time-to-First-MRI framed "under the 60-second target." Prototype displays ≈30s illustratively (D031). No fabricated fixed number ships.
Impacts: slice-02 prototype.

## Decision 037: Fast Pass surfaces all six outputs
Status: Accepted recommendation · Type: Screen/Interaction · Area: Orientation · Slice: 2 · Question ID: F2.2Q2 · Source: workflow diagram
Decision: At orientation the Fast Pass surfaces Orientation Confidence · Initial Attention (MRI) · Top Issues · Clarification Requests · Suggested Fixes · Analysis Status.
Impacts: slice-02, slice-03, slice-04.

## Decision 038: Orientation lands on the Overview; Attention is co-primary — resolves C-001
Status: Accepted recommendation · Type: Routing · Area: Orientation/Nav · Slice: 2/3/4 · Question ID: F2.3Q1 · Source: DL-096; GLOBAL_NAVIGATION NAV-C3
Decision: After Fast Pass the 60-second orientation lands on the confidence-led **Overview** (DL-096), with the **Attention Map reachable as a co-primary top-center view** (NAV-C3). This sets the C-001 default; owner may flip to Attention-first later.
Impacts: slice-02, slice-03, slice-04, contradictions.md C-001.

## Decision 039: First-run orientation + fresh-analysis arrival notice
Status: Accepted recommendation · Type: Journey · Area: Onboarding/Orientation · Slice: 2 · Question ID: F2.3Q2 · Source: v4 §6.5; D027
Decision: The one-time strategic-chain orientation (D027) fires on the first project only; the "Initial Analysis complete in Ns" arrival notice shows only on a fresh analysis (ingest/sample), not for returning users re-opening an analyzed project.
Impacts: slice-02.

## Decision 040: Deep Pass auto-runs, non-blocking, supersedes
Status: Accepted recommendation · Type: AI Behavior · Area: Analysis · Slice: 2 · Question ID: F2.4Q1 · Source: DL-046; ORIENTATION_STATE_MODEL
Decision: Extended Analysis (Deep Pass) auto-runs immediately after Fast Pass, non-blocking, and supersedes the provisional orientation (provisional→current). No user action starts it; the confidence hero carries the provisional↔current chip.
Impacts: slice-02, slice-03, slice-07.

## Decision 041: Deep Pass failure → last-good + retry
Status: Accepted recommendation · Type: Screen/Interaction · Area: Analysis state · Slice: 2 · Question ID: F2.4Q2 · Source: ORIENTATION_STATE_MODEL
Decision: On Extended Analysis failure, show "couldn't complete — showing your last-good understanding · Retry." Only reanalysis changes the assessment; last-good preserved.
Impacts: slice-02, slice-07.

## Decision 042: Clarification Requests at orientation + in-issue
Status: Accepted recommendation · Type: AI Behavior · Area: Clarification · Slice: 2 · Question ID: F2.5Q1 · Source: v4 §6.4
Decision: Clarification Requests surface as a light prompt at orientation and inside the relevant Issue; answering updates project information → reanalysis → the issue closes. Advisory framing (OSLO asks; you answer; you decide).
Impacts: slice-02, slice-06.

# Slice 2 — prototype feedback (2026-07-09)

## Decision 043: Analysis completion notices delivered via OSLO chat
Status: Client override · Type: Screen/Interaction · Area: Orientation/Chat · Slice: 2 · Source: owner 2026-07-09
Decision: "Initial Analysis complete" and "Extended Analysis complete — superseded the provisional orientation" are delivered as **OSLO chat messages**, not banners on the Overview panel. Analysis **status** (the pill state, the ledger "Initial/Extended Analysis complete" state line) stays where it is — only the arrival/completion **notifications** move to chat. Refines D037/D039.
Impacts: slice-02 prototype + user-experience.md/frontend-ui.md.

## Decision 044: Optional feature tour placement
Status: Client override · Type: Journey · Area: Onboarding/Education · Slice: 2 (offer) / 8 (re-open) · Source: owner 2026-07-09; v4 §6.5
Decision: The optional feature tour (spotlight coachmarks) is an onboarding/education surface distinct from the one-time strategic-chain orientation. It is **offered at first-analysis arrival** (from the chat completion message + a left-rail "Take a quick tour") and is **re-openable from Settings → Help** (Slice 8). Opt-in only; never gates value; sunsets with proficiency. It was omitted in the Slice 2 build — add it, spotlighting the surfaces that exist by Slice 2 (Overview/strategic read, Attention map, chat, confidence), with a seam for the artifact-edit step (Slice 5).
Impacts: slice-02, slice-05 (tour step), slice-08 (re-open control).

## Decision 045: Confirmations live in the Issue detail flow, not the Overview
Status: Client override · Type: Screen/Interaction · Area: Issues/Overview · Slice: 2/6 · Source: owner 2026-07-09; D009 Panel Model
Decision: Attestations/confirmations ("Confirmed by you", resolved-issue confirmations) are viewable **inside the Issue detail flow** (built out in Slice 6), not on the Overview. The Overview shows **summary counts only** (e.g. "N open · M resolved"), never the confirmations themselves. Keep the Slice 2 Overview count-only.
Impacts: slice-02 (count-only), slice-06 (confirmation view).

## Decision 046: Overview must match the DL-096 canonical redesign (no added sections)
Status: Client override · Type: Product Design · Area: Overview · Slice: 2/3 · Source: owner 2026-07-09; overview_redesign_mockup (DL-096)
Decision: The Overview sections are exactly **Confidence → Start here → Progress → More** as in the DL-096 redesign mockup. **Reliability is an inline qualifier** on the Confidence card ("Moderate · qualified by moderate reliability", with Why/hover), **not a separate Reliability card**. Remove the added Reliability section and any reformatting the worker introduced; match the redesign mockup's structure and formatting.
Impacts: slice-02, slice-03. Note: supersedes the older §D "Reliability card" treatment (D010) for the R1 Overview surface — reliability card content, if needed, folds into the Confidence qualifier + Why.
Impacts canonical-truth.md.

## Decision 047: Progress section matches the v4 ledger exactly
Status: Client override · Type: Product Design · Area: Overview/Progress · Slice: 2 · Source: owner 2026-07-09; v4 renderLedger
Decision: The Overview Progress section must match the v4 original ledger: left column = "{res} **issues resolved** · {open} open · view →" (resolved is the hero number, colored when >0) and "{crit} **critical issues open**" (append " · all clear" when crit=0); right column order = **Dependencies confirmed** then **Plan sections read** (verb "read" per v4; user-facing term kept "Plan sections" per D012 — flagged for owner; v4 literally says "Plan artifacts read"). Remove the extra "Initial/Extended Analysis complete" status line from Progress — analysis status stays on the confidence pill/provisional↔current chip and chat (preserves D043 intent: status visible, notifications in chat).
Impacts: slice-02 prototype (markup + deep-pass handlers repointed off the removed line), frontend-ui.md.
~~Open flag: "Plan sections read" vs literal "Plan artifacts read"~~ → **Resolved (D048).**

## Decision 048: Progress ledger label = "Plan artifacts read" (D012 exception)
Status: Client override · Type: Product Design · Area: Copy/Overview · Slice: 2 · Source: owner 2026-07-09
Decision: The Progress ledger meter reads **"Plan artifacts read"** (matching the v4 original), a deliberate **exception** to the D012 plain-language swap (artifacts→"Plan sections") for this specific label. Elsewhere the user-facing term stays "Plan sections."
Rationale: Owner preference for fidelity to the v4 ledger wording.
Impacts: slice-02 prototype (done), frontend-ui.md. Note against D012 (scoped exception, not a global reversal).

## Decision 049: User-facing term is "Plan artifacts" (supersedes D012's "Plan sections")
Status: Client override · Type: Product Design · Area: Copy/Global · Slice: All · Source: owner 2026-07-09
Decision: The user-facing term for the seven planning artifacts is **"Plan artifacts"** (singular "Plan artifact") everywhere in the UI and docs, **superseding** the D012/D048 plain-language mapping to "Plan sections." Internal code keys (`artifact`, `WBS`) unchanged. Aligns with the canonical DL-077 term "planning artifacts."
Rationale: Owner preference; closer to canonical DL-077 wording.
Impacts: Slice 1 (reopened for copy change → re-signoff), Slice 2, and all package docs. Supersedes D012 (Artifacts→"Plan sections") and folds in D048 (the ledger already reads "Plan artifacts read"). "WBS"→"Work breakdown" from D012 stays.
Divergence flag (baseline): reverses v4 §6.8 plain-language pass; owner may wish to update the CANONICAL_GLOSSARY / a DL entry to match (AI recommends; owner ratifies).

# Slice 3 — Project Overview & Understanding Console (locked 2026-07-09, all recs accepted)

## Decision 050: Confidence pill + popover (compact console)
Status: Accepted recommendation · Type: Screen/Interaction · Area: Overview/Nav · Slice: 3 · Question ID: F3.1Q1 · Source: v4; UX Notes §6.3
Decision: Top-bar Confidence pill (number + band + reliability qualifier, always visible) with a click popover showing the three CAF dimensions (first level) + Reliability basis + "Open full breakdown → Overview." Metrics live in one home (top bar), not duplicated.
Impacts: slice-03, all-slice shell.

## Decision 051: Reliability basis breakdown
Status: Accepted recommendation · Type: Product Requirement · Area: Reliability · Slice: 3 · Question ID: F3.2Q1 · Source: Reliability Model V1; v4 cpp
Decision: Reliability basis = Coverage · Evidence availability · Assessability (levels High/Moderate/Low), independent of CAF, shown in the pill popover; reachable from the Overview "Why." Plain label "How assessable" for Assessability (D012). Overview keeps reliability as inline qualifier + Why (D046) — no separate card.
Impacts: slice-03.

## Decision 052: False-confidence flag (CONF-06)
Status: Accepted recommendation · Type: Product Requirement · Area: Confidence · Slice: 3 · Question ID: F3.3Q1 · Source: Confidence Model CONF-06
Decision: When a high confidence band sits on low reliability, surface a false-confidence flag naming the cause (reliability shortfall vs CAF weakness). Advisory, non-alarming, neutral (not health-colored); appears in Confidence card + popover when the condition holds.
Impacts: slice-03, slice-07.

## Decision 053: Confidence stages (CONF-05)
Status: Accepted recommendation · Type: Screen/Interaction · Area: Confidence · Slice: 3 · Question ID: F3.4Q1 · Source: Confidence Model CONF-05; v4
Decision: Surface the understanding maturity stage (Orientation ▸ Expanded ▸ Validated) subtly. **Revised 2026-07-09 (owner): the stage marker lives in the Confidence pill popover only (with a ⓘ explanation) — removed from the Overview card as standing chrome** (it's static/low-signal in R1 and the provisional↔current chip already carries the actionable state). Details-on-demand, not Overview chrome.
Impacts: slice-03, slice-04, slice-07.

## Decision 054: Explainability "how this is calculated"
Status: Accepted recommendation · Type: Screen/Interaction · Area: Confidence · Slice: 3 · Question ID: F3.5Q1 · Source: v4 §6.12
Decision: A subtle "how this is calculated" affordance by the confidence number (CAF-derived, reliability-qualified, cause-bound; below-band jitter not dramatized). Hover/click.
Impacts: slice-03.

## Decision 055: Project summary depth
Status: Accepted recommendation · Type: Product Design · Area: Overview · Slice: 3 · Question ID: F3.6Q1 · Source: v4
Decision: Project summary (in More) = plain-language narrative: what the project is · understanding level · main limiter · reliability basis · the "not health/readiness/probability" caveat.
Impacts: slice-03.

## Decision 056: Confidence movement direction-only — resolves ND-2
Status: Accepted recommendation · Type: Product Requirement · Area: Confidence · Slice: 3 · Question ID: F3.7Q1 · Source: OPEN_TBD A1; v4 §6.1
Decision: On apply-fix → reanalysis, the confidence signal moves direction-only (▲/▼ with the named cause), never a fabricated magnitude; can fall (better understanding, not a worse project). Real deltas owner-TBD. Resolves ND-2.
Impacts: slice-03, slice-06, slice-07.

# Slice 4 — Attention Map (MRI) (locked 2026-07-09, all recs accepted)

## Decision 057: Heatmap primary MRI visual
Status: Accepted recommendation · Type: Screen/Interaction · Area: Attention/MRI · Slice: 4 · Question ID: F4.1Q1 · Source: D007; v4
Decision: Heatmap = rows (7 plan artifacts) × columns (Clarity·Alignment·Feasibility); cells shaded by attention severity (none→warning→moderate→critical; brighter = more attention); legend "Brighter = more attention — not a health score." Optional per-cell issue-count mini-label.
Impacts: slice-04.

## Decision 058: Cell → scoped Issues routing
Status: Accepted recommendation · Type: Screen/Interaction · Area: Attention · Slice: 4 · Question ID: F4.2Q1 · Source: D007; v4 §6.11
Decision: Clicking a cell routes via openFindingsFor(artifact, dimension): exactly one open issue → opens that issue; else opens the Issues list scoped to that section + dimension (both filters lit). Slice 4 wires routing to the light issue panel + a scoped-list seam (full Issues list = Slice 6).
Impacts: slice-04, slice-06.

## Decision 059: Field view (secondary)
Status: Accepted recommendation · Type: Screen/Interaction · Area: Attention · Slice: 4 · Question ID: F4.3Q1 · Source: v4 mview-field
Decision: A light secondary "field" view toggle alongside the heatmap; heatmap stays primary.
Impacts: slice-04.

## Decision 060: Severity-only coloring + legend + hover
Status: Accepted recommendation · Type: Product Design · Area: Attention · Slice: 4 · Question ID: F4.4Q1 · Source: D003; v4
Decision: Cell severity ramp uses red/amber only; confidence/CAF stay neutral. Hover scales the cell; legend states it's attention, not health.
Impacts: slice-04.

## Decision 061: Empty / all-clear states
Status: Accepted recommendation · Type: Screen/Interaction · Area: Attention · Slice: 4 · Question ID: F4.5Q1 · Source: D003; Tier 1 empty states
Decision: A section×dimension with no open issues renders as a neutral, inert cell (not clickable); when nothing needs attention, show an all-clear empty state.
Impacts: slice-04.

## Decision 062: Co-primary placement + context preservation
Status: Accepted recommendation · Type: Routing · Area: Attention/Nav · Slice: 4 · Question ID: F4.6Q1 · Source: D038; NAV-7
Decision: Attention Map reachable as a co-primary top-center view + from the Overview's Attention pointer; closing returns to prior context.
Impacts: slice-04.

# Slice 4 — prototype feedback (2026-07-09)

## Decision 063: Remove the Attention-map Dimensions/Field view (supersedes D059)
Status: Client override · Type: Screen/Interaction · Area: Attention · Slice: 4 · Source: owner 2026-07-09
Decision: The secondary "Dimensions"/field view on the Attention map is removed — not helpful. The map has one view (the heatmap); the heat/field toggle is removed. Supersedes D059.
Impacts: slice-04 prototype + docs.

## Decision 064: Understanding-description framing (positive)
Status: Client override · Type: Product Design · Area: Copy/Confidence · Slice: 3/4 · Source: owner 2026-07-09
Decision: The Project-summary closing line reads "This reflects OSLO's understanding of the plan — how clear, aligned, and feasible it is." (positive framing), replacing the "not project health, readiness, or a probability of success" negative. The doctrinal caveat (confidence ≠ health/probability) is preserved as its single home in the Confidence info tooltip/popover (§6.7 single-home + hover), not reprinted here.
Impacts: slice-03/04 copy.

## Decision 065: Attention-map stale-count bug fix + Timeline→History seam + UX polish
Status: Client override (fixes) · Type: Screen/Interaction · Area: Attention/Overview · Slice: 4 · Source: owner 2026-07-09
Decision: (a) Heatmap re-renders on Attention-view entry and after any issue-status change so displayed counts always match routing (fixes a stale "2" cell opening a single issue). (b) A "Timeline →" link routes to a History/timeline seam (Slice 7), never the heatmap. (c) "How this is calculated" loses its duplicate native tooltip and sits by the number. (d) The Stage marker gains a visible ⓘ explanation. (e) The CAF dimension tooltip triggers only on the dimension word.
Impacts: slice-04 prototype + docs.

# Slice 5 — Plan Artifacts / Artifact Workspace (locked 2026-07-09, all recs accepted)

## Decision 066: Artifact explorer + issue badges
Status: Accepted recommendation · Type: Screen/Interaction · Area: Workspace · Slice: 5 · Question ID: F5.1Q1 · Source: v4
Decision: Left-rail explorer lists the 7 plan artifacts (grouped Understanding / Execution) with a per-artifact open-issue count badge; clicking opens it in the center editor.
Impacts: slice-05.

## Decision 067: Type-aware editor (prose / tables), with mixed content in Understanding
Status: Accepted recommendation + client clarification · Type: Product Design · Area: Editor · Slice: 5 · Question ID: F5.2Q1 · Source: v4; owner 2026-07-09
Decision: Understanding artifacts (Intent·Context·Scope·Requirements) render as **flowing prose by default, but may include sections of bullets or tables where that better represents the items** (e.g. lists of goals, stakeholders, constraints). Execution artifacts (Work breakdown·Schedule·Resources) render as structured tables. Live edit (inline/contenteditable) with autosave (simulated via localStorage in the prototype).
Rationale: Owner clarification — prose is the default, not a straitjacket; use the format that reads best for the content.
Impacts: slice-05.

## Decision 068: Inline weakness annotations → Issue panel
Status: Accepted recommendation · Type: Screen/Interaction · Area: Editor · Slice: 5 · Question ID: F5.3Q1 · Source: D003; Panel Model
Decision: Weak text is inline-colored (severity ramp) on the contiguous weak span; hover shows a summary; clicking opens the Issue panel (never resolved inline).
Impacts: slice-05, slice-06.

## Decision 069: Epistemic notation (From OSLO / Confirmed by you)
Status: Accepted recommendation · Type: Product Data · Area: Editor · Slice: 5 · Question ID: F5.4Q1 · Source: D011
Decision: Text is From OSLO (Derived) by default; editing or confirming a sentence makes it Confirmed by you (Attested) = a plan fact, with a visual accent marker. Saving changes no assessment; only reanalysis does.
Impacts: slice-05.

## Decision 070: Event-driven reanalysis in the editor
Status: Accepted recommendation · Type: AI Behavior · Area: Editor · Slice: 5 · Question ID: F5.5Q1 · Source: D006
Decision: Editing runs the state machine automatically: Saved → analysis stale → Reanalyzing… → Up to date. No manual "Reanalyze" button.
Impacts: slice-05.

## Decision 071: Weakness stepper + artifact navigation
Status: Accepted recommendation · Type: Screen/Interaction · Area: Editor · Slice: 5 · Question ID: F5.6Q1 · Source: cognitive audit C7
Decision: A "Jump to weakness ⌃ k of N ⌄" stepper to move between weak spots in an artifact, plus artifact prev/next navigation. Fills the feature-tour artifact-edit step (D044).
Impacts: slice-05.

## Decision 071b / 075: Editor term + table row editing
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: (a) The weakness stepper and its labels use the canonical user-facing term "issue": "Jump to issue", "Previous/Next issue", "No issues in view" (internal fn names unchanged). "CAF weakness" (a weak dimension) is a distinct, correct phrase and stays. (b) Structured Execution tables (Work breakdown · Schedule · Resources) get explicit **add-row** and **delete-row** controls (an "+ Add row" affordance under each table; a per-row delete on hover/focus), so the user can manage rows — not only edit existing cells. Row changes flow through the debounced reanalysis (D073).
Impacts: slice-05 prototype + docs.

## Decision 079: Quiet, non-reflowing save/analysis indicator (refines D076)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: The reflowing per-edit hint blocks ("You're editing…", "Saved · analysis stale…") that shifted the artifact body vertically are removed. The status indicator becomes a single small **dot** in the toolbar (fixed size, no layout shift, no repeating prose): resting = green ("Analysis up to date" on hover title), briefly amber during reanalysis ("Reanalyzing…" on hover). No changing text, no body reflow, minimal attention pull.
Impacts: slice-05 prototype + docs.

## Decision 080: Expanded Notion-style rich-text toolbar (refines D078)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: The floating selection toolbar is expanded and restyled to resemble Notion's RTF popup — grouped controls with dividers, rounded dark pill, subtle shadow, clear hover/active states. Adds more inline options (e.g. bold, italic, underline, strikethrough, inline code, link) and block/turn-into options (headings, bullet/numbered list, quote) with indent/outdent. Prototype-grade formatting; owner-directed enhancement beyond v4.
Impacts: slice-05 prototype + docs.

## Decision 077: Demote the epistemic tag to hover (refines D069/D011)
Status: Client override · Type: Product Design · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: The permanent per-block "Confirmed by you" / "From OSLO" text tag is excessive/distracting as standing chrome. Keep the epistemic distinction as a **subtle visual accent** (e.g. the attested left-border) and **reveal the label only on hover/focus** of the block (single-home + hover, §6.7; sunsets, §6.9). The behavior (edit → attested) is unchanged; only its persistent display is demoted. "Saving changes no assessment; only reanalysis does" stays available on hover.
Impacts: slice-05 prototype + docs.

## Decision 078: Rich-text (Notion-like) editing in the artifact editor (owner-directed addition)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: The artifact editor supports basic rich-text editing like Notion — **bold/italic, bullet & numbered lists, indent/outdent** — via a floating selection toolbar and keyboard shortcuts (⌘/Ctrl+B etc.). An enhancement beyond the v4 "flowing prose" contenteditable baseline; flagged as owner-directed (not v4 canon). Must coexist with inline issue annotations (D074), epistemic accents (D077), and the debounced reanalysis (D073/D076). Prototype uses contenteditable/execCommand-style formatting; real build maps to a proper rich-text model.
Impacts: slice-05 prototype + docs. (Divergence flag: not in v4 — owner may want it reflected in canon/specs.)

## Decision 076: Calm editor save/analysis indicator (refines D070/D073)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: The two typing-time notifications — **"Editing…"** and **"Saving…"** — are removed (redundant/interruptive). Autosave is silent. While the user types the indicator does not churn; only after the pause/blur commit does it show the meaningful chain **Saved · analysis stale → Reanalyzing… → Up to date**. Staleness/honesty preserved by that chain + the confidence provisional↔current chip.
Impacts: slice-05 prototype + docs.

## Decision 081: Insert table rows anywhere (extends D075)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: Table row insertion is not limited to appending at the end. Each body row gets a per-row "insert row" control (e.g. a "+" in the row gutter alongside the delete "×") that inserts a new empty row immediately after it (with insert-above available on the first row, or via the header gutter), so a row can be added anywhere. The "+ Add row" append affordance stays. Inserts flow through the same quiet debounced reanalysis (D073/D076/D079); new rows are "Confirmed by you".
Impacts: slice-05 prototype + docs.

## Decision 082: Row reordering + discoverable top-insert (extends D081)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: (a) Table rows can be **reordered** — a drag handle (⠿) in the row gutter enables drag-and-drop reorder, with a keyboard alternative (focus handle + ↑/↓ or Alt+↑/↓ to move up/down) for WCAG. (b) The **insert-at-top** control (header-gutter "+") is made discoverable (clearer/always-hinted affordance), since it was only visible on header hover. Reorders/inserts flow through the quiet debounced reanalysis (D073/D076/D079); moved/new rows keep their attested state and gutter controls.
Impacts: slice-05 prototype + docs.

## Decision 083: Table-cell provenance — row gutter dot + per-cell hover (extends D069/D077)
Status: Client override · Type: Product Design · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: Table content shows epistemic provenance like prose does. (a) A subtle **provenance dot in each row's gutter**: muted = From OSLO (all cells derived), brand = Confirmed by you (row has any attested cell); it flips when the user edits a cell in that row or adds/inserts a row (new rows = Confirmed by you). (b) **Per-cell hover** reveals that exact cell's state ("From OSLO" / "Confirmed by you"), so a single edited cell in an OSLO row is still identifiable. Drafted cells seed as derived; editing a cell attests it (D069). Consistent with the subtle-accent + hover-reveal pattern (D077); low clutter.
Impacts: slice-05 prototype + docs.

## Decision 084: Fold editor gap-analysis items into Slice 5
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09; slice-05-editor-critical-analysis.md
Decision: The editor gaps from the critical analysis are folded into Slice 5 (prototype-grade), in priority batches. **Batch A (trust-critical + core table):** undo/redo (snapshot-based history incl. structural ops), reanalysis-merge preservation (a reanalysis/re-draft preserves "Confirmed by you" attested content; only "From OSLO" derived content refreshes), table cell Tab/arrow navigation, table column add/delete/reorder/resize, paste sanitization. **Batch B (authoring + a11y):** block insertion / "/" menu, image/file embedding, keyboard/touch reachability of hover-only info (annotation summary, epistemic, how-calculated), markdown input shortcuts, whole-block drag-reorder. **Batch C (polish):** in-artifact find/replace, link edit/remove, explicit save affordance, empty/placeholder states, mobile/touch pass. Deferred items stay out: version history/diff/revert → Slice 7; inline comments/@mentions → Slice 9.
Impacts: slice-05 prototype + docs (multiple revisions).

## Decision 073: Reanalysis is patient/debounced (refines D070)
Status: Client override · Type: AI Behavior · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: Editing does not churn the analysis state on every keystroke. While the user is actively typing, the editor stays quiet (a calm "Editing…"); the Saved → analysis stale → Reanalyzing… → Up to date chain only advances after the user has plausibly finished a block — i.e. after a typing-idle debounce (~1.5s) or when the block loses focus (blur). A single character never triggers a reanalysis notification.
Impacts: slice-05 prototype.

## Decision 074: Annotated weak text is directly (partially) editable (refines D068)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: Inline severity-annotated text is editable in place — the user can place a caret inside it and edit any portion (not forced to replace the whole span). The annotation keeps its color/underline as a flag. "Open issue" moves off the text click onto the hover summary (an "Open issue →" action) and/or a small non-editable marker, so clicking the text edits it while the issue stays reachable (and still never resolved inline — reanalysis reconciles). 
Impacts: slice-05 prototype.

## Decision 072: Fix — app top bar (view switch + confidence pill) was hidden behind the phase bar
Status: Client override (bug fix) · Type: Screen/Interaction · Area: App shell · Slice: 5 (carries forward) · Source: owner 2026-07-09
Decision: The demo phase bar (`position:fixed`, 38px) was overlapping `#app`, hiding the top-center view switch (Overview·Attention·Artifacts) and the confidence pill. Fixed by offsetting `#app` below the phase bar (`margin-top:38px; height:calc(100vh - 38px)`). Latent since Slice 1; fix carries forward in the cumulative prototype.
Impacts: slice-05 prototype (and forward).

- ~~ND-1: Hero headline~~ → **Resolved (D029): A + "Strategic project leadership".**
- ~~ND-2: Confidence movement magnitude~~ → **Resolved (D056): direction-only.**
- ND-3: Scope of multi-project / collaboration / export surfaces as fat slices (recommend include; CRR out).
- ~~ND-4: MRI co-primary vs nested~~ → **Resolved (D038): land on Overview; Attention co-primary. Owner may flip.**

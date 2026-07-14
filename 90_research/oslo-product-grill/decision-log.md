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

## Decision 085: Editor action buttons (discoverability for keyboard-only actions)
Status: Client override · Type: Screen/Interaction · Area: Editor · Slice: 5 · Source: owner 2026-07-09
Decision: Surface keyboard-only editor actions as visible toolbar buttons where it makes sense: **Undo / Redo** (with disabled state when the stack is empty), **Insert (＋)** opening the slash/block menu, and **Find (⌕)**. Placed in the artifact toolbar, wired to the existing functions, keyboard-accessible, themed/subtle. Shortcuts still work; buttons add discoverability.
Impacts: slice-05 prototype + docs.

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

# Slice 6 — Issues & Recommendations (Panel Model) (locked 2026-07-09, all recs accepted)

## Decision 093b: Issue Panel is a bounded, scrollable flyout
Status: Client override (fix) · Type: Screen/Interaction · Area: Issues · Slice: 6 · Source: owner 2026-07-09
Decision: The Issue Panel was clipped (phase bar covered its top; app chrome clipped its bottom). Fixed: raise the scrim above app chrome (z-index 260), full-viewport height with internal `overflow-y:auto`, a persistent ✕ close (top-right) + Esc-to-close, extra bottom padding so the header and History are always reachable.
Impacts: slice-06 prototype.

## Decision 095: Cascade the approved shell back to Slices 3–5
Status: Client override · Type: Screen/Interaction · Area: App shell · Slice: 3/4/5 (reopened) · Source: owner 2026-07-09
Decision: The approved shell (persistent left sidebar + top bar + command palette, D093/D094) is cascaded into the Slice 3, 4, 5 prototypes so it appears consistently from the orientation hand-off onward. Per cumulative discipline, each slice wires nav to views that EXIST in that slice and shows labeled seams for the rest (History → Slice 7 always; Issues surface → Slice 6 seam in Slices 3–5 unless a light list exists; the Plan-artifacts sidebar section appears only from Slice 5 where the editor exists). Reopens Slices 3–5 for the shell change (re-signoff). The shell's canonical owner remains Slice 8 (global nav/switcher/settings/palette); this is a presentation cascade.
Impacts: slice-03/04/05 prototypes + docs.

## Decision 094: Command palette (search / jump-to) — approved design
Status: Client override · Type: Screen/Interaction · Area: App shell · Slice: 6 (carries forward) · Source: owner 2026-07-09 (approved design)
Decision: The top-bar search (⌕) button and **⌘/Ctrl+K** open a command palette: input "Search or jump to…"; grouped, fuzzy-filtered results — **GO TO** (Overview · Issues · History · Attention map), **PLAN ARTIFACTS** (the 7 artifacts → openArtifact), **OPEN AN ISSUE** (open issues → openIssue). Keyboard: ↑↓ navigate · ↵ open · esc close; footer shows the hint. User-facing term "Issues"/"Open an issue" (approved image says "Findings/Open a finding" — pre-rename; we keep the ratified "Issues", DL-095).
Impacts: slice-06 prototype (carries forward).

## Decision 093: Persistent left navigation sidebar (app-shell IA change; supersedes top-center switch)
Status: Client override · Type: Routing · Area: App shell · Slice: 6 (carries forward) · Source: owner 2026-07-09
Decision: Replace the top-center view switch with a **persistent left navigation sidebar**, visible by default across all project views. Sections: (a) **Project views** — Overview · Attention map · Issues (active-state links); (b) **Plan artifacts** — the 7-artifact list with issue badges (opens the artifact editor); (c) **bottom utilities** — Product tour, Settings, Help/account. The top bar keeps brand + confidence pill + account (or account moves to the sidebar bottom). Responsive: collapses to a drawer on narrow (reuse the Slice-5 explorer-drawer pattern). Supersedes the top-center co-primary switch aspect of D013/D038/NAV-C3 — **divergence from NAV-C3 flagged; owner may want the navigation canon updated** (AI recommends; owner ratifies).
Impacts: slice-06 prototype (app shell, carries forward), REPOSITORY navigation canon (recommend update). 
Assumption flagged: sidebar becomes primary nav; top-center tabs removed to avoid duplication — owner may adjust.
**Refined to the owner's approved design (2026-07-09):** Sidebar — PROJECT: Overview · Issues · History · Attention map (History nav routes to a Slice-7 seam); PLAN ARTIFACTS grouped Understanding (Intent·Context·Scope·Requirements) / Execution (Work breakdown·Schedule·Resources) with badges; bottom: "✦ Take a quick tour" button, "Free plan · 1 active project · Upgrade" chip (visibility-first, DL-048), "Your account · Settings" row. Top bar — Intralign brand + project switcher ("DevNorth 2026 ▾", Slice-8 seam) + sample chip + breadcrumb (current view/artifact); right: confidence pill + search + Share + Export (Slice-9 seams) + report icon + Free chip. Note: approved design image labels it "Findings 14" — we keep the ratified user-facing term **"Issues"** (DL-095/D017); flagged for owner.

## Decision 092: Declutter the Issue Panel; drop user-facing "reanalysis" language (refines D008/D087/D090)
Status: Client override · Type: Product Design · Area: Issues/Copy · Slice: 6 · Source: owner 2026-07-09
Decision: The Issue Panel is over-verbose; several static explanatory descriptions reduce readability and go stale. Trim them, and **stop surfacing "reanalysis / re-analyze" as a user-facing mechanism** — users care about the outcome, not the mechanism. Specifically: remove standing lines like "OSLO asks; you answer; you decide. Answering updates your project info, re-runs analysis, and closes this issue." and "OSLO will update your project info and run re-analysis" and "Only reanalysis changes this assessment. You can't resolve an issue by hand…". The honesty invariant (issues close as OSLO's understanding updates, not by hand — the behavior enforces it) lives in **exactly one subtle hover** (ⓘ), phrased in plain outcome language (prefer "updates" over "reanalysis"). Buttons: "Submit & re-analyze" → "Submit answer"; "Addressed · awaiting reanalysis" → "Addressed · updating…" (or just the lifecycle). Applies across the panel, the clarification block, and the apply-fix flow. Keep advisory framing implicitly (OSLO advises; you decide) without repeating it as chrome.
Impacts: slice-06 prototype + docs; consistent with §6.7 (single-home + hover) and §6.9 (sunset teaching copy).


## Decision 086: All-Issues surface (filters + group toggle)
Status: Accepted recommendation + client edit · Type: Screen/Interaction · Area: Issues · Slice: 6 · Question ID: F6.1Q1 · Source: v4 §6.11
Decision: All-issues list (center pane) with filters **Artifact · Dimension · Severity** (the artifact-scoping filter is labeled **"Artifact"**, not "Section" — client edit, per D049) + a group toggle **By dimension / By severity / By artifact** (D092b — By artifact added at owner request); honest "N hidden by filters · clear"; per-issue card = title + severity + location + status. Subtitle kept minimal ("What needs your attention") — the group buttons already convey the grouping (D092b declutter).
Impacts: slice-06.

## Decision 087: Full Issue Panel
Status: Accepted recommendation · Type: Screen/Interaction · Area: Issues · Slice: 6 · Question ID: F6.2Q1 · Source: Finding Panel spec (Option A)
Decision: Issue Panel: Header (title · severity · dimension·artifact · lifecycle) → Why this matters → Evidence (collapsible) → What this weakens (Clarity/Alignment/Feasibility) → Recommendations → History (pointer; full timeline = Slice 7) → reanalysis note.
Impacts: slice-06.

## Decision 088: Lifecycle Open → Addressed → Resolved
Status: Accepted recommendation · Type: Product Requirement · Area: Issues · Slice: 6 · Question ID: F6.3Q1 · Source: D018/DL-094
Decision: Open → Addressed ("by acting · awaiting reanalysis") → Resolved. Never resolved by hand; Resolved only via reanalysis.
Impacts: slice-06.

## Decision 089: Recommendations + Apply this fix (Panel Model)
Status: Accepted recommendation · Type: Screen/Interaction · Area: Recommendations · Slice: 6 · Question ID: F6.4Q1 · Source: D009
Decision: OSLO Recommended + Possible Resolution Paths, selectable → Selected Path (Confirmed by you); single-action "Apply this fix" where OSLO can draft → applies → reanalysis. Acceptance ≠ success; confidence direction-only (D056). No recommendations outside the Issue.
Impacts: slice-06, slice-05.

## Decision 090: Clarification loop in the panel
Status: Accepted recommendation · Type: AI Behavior · Area: Issues · Slice: 6 · Question ID: F6.5Q1 · Source: D042
Decision: Clarification block (question + answer input); answering → Update project info → reanalysis → the issue closes.
Impacts: slice-06.

## Decision 091: Empty states + honesty
Status: Accepted recommendation · Type: Screen/Interaction · Area: Issues · Slice: 6 · Question ID: F6.6Q1 · Source: Tier 1 empty states
Decision: Four honest empty states (none-found / none-under-lens / not-yet-analyzed / unavailable) + honest "hidden by filters" count. Comments/@mentions → Slice 9; full History → Slice 7.
Impacts: slice-06.

# OSLO Chat integration (cross-cutting; introduced Slice 2, lands in latest cumulative)

## Decision 109: Chat UX refinements (epistemic replies, citations, honest fallback, AI-native patterns)
Status: Client override · Type: AI Behavior / Screen-Interaction · Area: Chat · Slice: 8 (reference; cascade optional) · Source: owner 2026-07-09; oslo-chat-ux-critical-analysis.md
Decision: (1) **Epistemic replies** — chat inherits OSLO's doctrine: every answer is **reliability-qualified** ("Reliability is Moderate — this rests on the documents you gave me; treat it as directional"), distinguishes **From OSLO (derived)** vs **Confirmed by you (attested)** when asserting a plan fact, and says when evidence is thin instead of answering confidently. (2) **Citations/provenance** — replies cite their basis as clickable chips (issue `ev[]` sources, artifact spans, history events) that route to the surface. (3) **Honest capability-scoped fallback** — off-script questions get an honest "I can't answer that yet; here's what I can do…", NEVER a fabricated/canned answer. (4) **Streaming/thinking affordance** + **message actions** (copy · retry · 👍/👎 · **save to History**). (5) **Follow-up suggestions** after each reply; **@-mention + multi-context** pinning; **expand mode** for the rail; action links **state their consequence**. (6) **Per-project conversation persistence**; polish (so-what-first formatting, ⌘K focus / ⌘Enter send / Esc clear, teaching empty state, advisory copy single-home per §6.7). Anti-pattern guard: **no chat-washing** — canonical surfaces stay primary; chat augments and hands the user back to the owning surface.
Impacts: slice-08 prototype + docs (reference build); optional cascade to Slices 2–7.


## Decision 108: Make OSLO chat functional + integrate it into the workflows
Status: Client override · Type: AI Behavior / Screen-Interaction · Area: Chat (cross-cutting) · Slice: 8 (carries forward; cascade to earlier) · Source: owner 2026-07-09; oslo-chat-integration-analysis.md
Decision: OSLO chat was non-functional (composer + Send had no handlers; no send/reply logic) — a read-only notice feed. Fix and integrate:
(1) **Make chat work** — composer + Send (Enter to send, Shift+Enter newline); OSLO replies are **simulated but state-grounded** (current confidence band + reliability, the limiting dimension, open issues, active artifact). Advisory-only (D001): chat reads, explains, recommends — it NEVER mutates the plan or resolves an issue.
(2) **Context handoff + context pill** — a single `askOslo(context)` entry point; chat shows "Context · <what>" with a clear-context control.
(3) **Wire the entry points** (each in the slice where its surface exists): Issue Panel → "Ask OSLO about this issue"; Recommendations → **"Discuss"** (a canonical v4 recommendation action that was entirely missing); Artifact annotation/toolbar → "Ask about this"; Overview confidence card → "Ask why"; Attention cell → ask about it.
(4) **Clarifications are conversational** — OSLO can raise a clarification in chat and the user can answer there; the answer routes to the SAME project-info update, issue transition, and **History** entry (no side-channel that bypasses governance, D096).
(5) Polish — suggested prompt chips, replies link to the surface they reference, chat empty/first-run state, live-region a11y.
Impacts: slice-08 prototype + docs (reference); cascade the core (working chat + context pill + slice-appropriate entry points) back to Slices 2–7 per cumulative discipline.


## Decision 107: Fold Slice 8 gap-analysis refinements
Status: Client override · Type: Screen/Interaction · Area: Workspace/Settings · Slice: 8 · Source: owner 2026-07-09; slice-08-critical-analysis.md
Decision: (1) **Remove dead Settings affordances** — every row must work, be a clearly-labeled seam/visibility-first state, or not look interactive. Make FUNCTIONAL now (prototype-grade, localStorage): Profile (editable display name/role), Workspace (editable name), **Notification preferences** (per-category toggles — legitimate because awareness is presentation-only, D104), Account (surface sign-out + stay-signed-in, D028). Keep visibility-first but LABEL honestly: Subscription/Billing ("handled outside the app in Alpha" — DL-048/D014), Integrations/Membership (later), Collaboration (Slice 9 seam). Remove internal spec language ("Confirmation-gated"); Delete account gets a real confirm dialog or an honest label. (2) **Gate/label the collaboration notification categories** (mention/reply/shared) until Slice 9 — they can't occur in Alpha; don't imply capability. (3) **Lean the Alpha dashboard** to the 1-active-project reality (honest presentation; full Pinned/Recent grid when multi-project is real). (4) **Light-mode AA contrast sweep** (brand orange, neutral maturity ramp vs severity separation). (5) Polish: stale → "open to bring the read up to date" action, Settings search, notification + workspace empty states, plain language.
Impacts: slice-08 prototype + docs.


## Decision 102: Workspace Home / Dashboard
Status: Accepted recommendation · Type: Screen/Interaction · Area: Workspace · Slice: 8 · Question ID: F8.1Q1 · Source: PROJECT_DASHBOARD spec; DL-048
Decision: Global Workspace Home (via the Intralign/OSLO logo + Workspace context): Pinned + Recent project cards (name · ownership/shared · analysis status incl. stale · reliability-qualified understanding indicator · recency · open-issues count); Archived projects area (non-destructive, restore anytime); "no computed scores across projects" honesty note; at-cap Create → upgrade-or-archive prompt (DL-048). Alpha shows the structure with illustrative projects + "1 active project" note.
Impacts: slice-08.

## Decision 103: Project switcher
Status: Accepted recommendation · Type: Routing · Area: Nav · Slice: 8 · Question ID: F8.2Q1 · Source: GLOBAL_NAVIGATION §N
Decision: The top-bar "DevNorth 2026 ▾" chip opens a real switcher: project list + Workspace Home + New project (at-cap → honest prompt). Replaces the Slice-6 switcher seam.
Impacts: slice-08.

## Decision 104: Notifications / awareness panel
Status: Accepted recommendation · Type: Screen/Interaction · Area: Awareness · Slice: 8 · Question ID: F8.3Q1 · Source: NOTIFICATION_AND_AWARENESS spec
Decision: Awareness panel, R1 categories (mention · reply · shared-with-me · analysis complete/failed · stale); read/unread presentation-only; routes to source; never triggers analysis; unread badge in top bar.
Impacts: slice-08.

## Decision 105: Settings (visibility-first)
Status: Accepted recommendation · Type: Screen/Interaction · Area: Settings · Slice: 8 · Question ID: F8.4Q1 · Source: ACCOUNT_AND_WORKSPACE_SETTINGS spec
Decision: Settings surface (wires the seam) with areas: Account · Profile · Workspace · Project defaults · Collaboration · Notifications · Subscription · Billing · Integrations · Membership. Visibility-first for Subscription/Billing/Integrations/Membership (facts + upgrade paths; no enforcement).
Impacts: slice-08.

## Decision 106: Appearance (theme + a11y)
Status: Accepted recommendation · Type: Product Design · Area: Settings/Theme · Slice: 8 · Question ID: F8.5Q1 · Source: D015; VISUAL_DESIGN §1
Decision: Settings → Appearance: dark/light theme toggle (dark default; one semantic token set flips via data-theme), plus accessibility controls (reduced-motion honored, focus rings).
Impacts: slice-08, theme-system.md.

# Slice 7 — History & Confidence Trend (locked 2026-07-09, all recs accepted)

## Decision 101: Fold History gap-analysis refinements into Slice 7
Status: Client override · Type: Screen/Interaction · Area: History · Slice: 7 · Source: owner 2026-07-09; slice-07-history-critical-analysis.md
Decision: Fold these History refinements (prototype-grade): (1) remove the internal event-type identifier leak (`analysis_run`, etc.) from the UI — replace with human category labels; (2) group the timeline by **analysis run** (collapsible clusters: each run + the events it caused) and/or by day; (3) per-run **"what changed" delta** (issues +/resolved · CAF band moves · stage · confidence direction); (4) **link the trend to the timeline** (click a trend point → its run; run events show the confidence band produced); (5) event-type **filter chips** (All · Analysis · Issues · Versions · Your decisions) with honest hidden-count; plus light polish: absolute timestamp on hover, cleaner current-state (not per-event "current") semantics, list a11y. Preserve append-only + read-only + last-good honesty. Deferred: full version diff/restore (build-phase/versioning model), history search, export/share (Slice 9), windowing.
Impacts: slice-07 prototype + docs.


## Decision 096: Append-only History/timeline
Status: Accepted recommendation · Type: Screen/Interaction · Area: History · Slice: 7 · Question ID: F7.1Q1 · Source: HISTORY_AND_TIMELINE §J; v4
Decision: History center pane (`#pane-history`, from the sidebar) = chronological, append-only event list — analysis runs (Initial/Extended), artifact versions (vN), issue lifecycle (Open→Addressed→Resolved), selected resolution paths, clarifications answered. Current vs prior labels; nothing overwritten; viewing is read-only and changes no assessment. Replaces the Slice-6 History seam.
Impacts: slice-07.

## Decision 097: Understanding-over-runs trend
Status: Accepted recommendation · Type: Product Design · Area: Confidence · Slice: 7 · Question ID: F7.2Q1 · Source: v4; D056
Decision: "Understanding over runs" trend sparkline — each point cause-bound + band-qualified; can rise OR fall (a fall after deeper analysis usually means it found something real). Shown in History; mirrored by the Overview confidence trend row. Direction-only; real magnitudes owner-TBD.
Impacts: slice-07, slice-03.

## Decision 098g: Last-good + read-only honesty
Status: Accepted recommendation · Type: Product Requirement · Area: History · Slice: 7 · Question ID: F7.3Q1 · Source: ORIENTATION_STATE_MODEL
Decision: Last-good understanding preserved (e.g., on failed analysis); History is read-only — prior states viewable, never editable, and viewing changes nothing. (Grill decision 98 — distinct from canonical DL-098.)
Impacts: slice-07.

## Decision 099: Version lineage
Status: Accepted recommendation · Type: Product Data · Area: History · Slice: 7 · Question ID: F7.4Q1 · Source: v4
Decision: Artifact versions (vN) are append-only; History links to prior versions as view-only snapshots.
Impacts: slice-07, slice-05.

## Decision 100: First-run state
Status: Accepted recommendation · Type: Screen/Interaction · Area: History · Slice: 7 · Question ID: F7.5Q1 · Source: empty-state model
Decision: Before multiple runs, History shows a minimal state (initial analysis) with an honest "more appears as your plan evolves." Threaded comments as timeline events deferred to Slice 9.
Impacts: slice-07.

- ~~ND-1: Hero headline~~ → **Resolved (D029): A + "Strategic project leadership".**
- ~~ND-2: Confidence movement magnitude~~ → **Resolved (D056): direction-only.**
- ~~ND-3: Scope of multi-project / collaboration / export surfaces~~ → **Resolved (D110–D118): included as Slices 8–9. CRR *reinstated* — it is ratified canon (CRR-01…05, DL-049), not a gap; the earlier 'CRR out' position was a documented over-escalation, corrected 2026-07-10.**
- ~~ND-4: MRI co-primary vs nested~~ → **Resolved (D038): land on Overview; Attention co-primary. Owner may flip.**


---

# Slice 9 — Collaboration, Sharing & Export (2026-07-10)

**D110 — Sharing dialog.** Invite by email + participant types **Owner · Collaborator · Viewer** (each with a plain statement of what they can do), plus a **view-only snapshot link**. Presentation-only in R1: no permission enforcement. A stale link is labeled **"previous analysis"** — never silently presented as current.

**D111 — Threaded comments + @mentions on issues.** Comments attach to an **Issue** (Panel Model — no orphan comment surface), are **append-only**, and support **@mention** autocomplete (registered teammates, or invite someone new). Persistent honesty line: **"Comments never change the assessment."** Comments append to History (D096).

**D112 — Export / share-out.** Export a **snapshot** of current understanding carrying an **analysis-currency marker** and the **required disclaimer** (understanding maturity — *not* project health, readiness, or probability of success). PDF / copy / link. **Free = PDF-only.** Export generates no new assessment and never triggers an analysis.

**D113 — Collaboration notifications un-gated.** The **mention · reply · shared-with-me** categories (gated in Slice 8 / D107) are now live; they route to source and remain presentation-only.

**D114 — CRR reinstated as ratified canon (corrects the prior "spec gap" escalation).**
CRR-01…05 are Alpha-scope, High-priority canon with the M4 exit criterion (C14); **DL-049 (ratified) resolved gap #337** (external-reviewer identity: single `Principal`, `type: reviewer|user`, in-place promotion); **DL-055 (ratified)** reclassified *Share For Review* as a collaboration affordance. Build:
- **CRR-01** *Share for review* on an issue (Issue Panel + issue-overlay action; **Validation Recommendations are prime candidates** per REC-05).
- **CRR-02** **Review Package** = finding + context + recommendation + artifact reference.
- **CRR-03** Reviewer responses: **Comment · Approve · Reject · Suggest Alternative** — structured and preserved.
- **CRR-04** Response → **evidence** → triggers **Extended Analysis**; confidence / Attention (MRI) update.
- **CRR-05** **Review-status visibility** across the workspace, driving **MRI-07 Understanding Dependencies** ("2 issues awaiting sponsor review") on Overview + Attention.

**D115 — Reviewer-response semantics (doctrinal).** A stakeholder response is **evidence, not truth**. It enters the record as a **third-party attestation** — a *third* epistemic class, distinct from **From OSLO** (derived) and **Confirmed by you** (owner-attested). It triggers an analysis update and confidence may move, but it **never auto-resolves the issue**, and **OSLO never self-accepts it** (no autonomous acceptance). An "Approve" is evidence *that a stakeholder approves* — never proof the plan is sound.

**D116 — Reviewer (recipient) experience — PROPOSAL, not asserted canon.** Build a **low-friction, no-account-required reviewer view** (lands directly in the review package; responds without a signup wall) with a **convert-moment at realized value** ("create your own project" *after* they respond, never before). Per the Virality/K-Factor audit this is **P0** — the binding constraint on k — and is explicitly **owner-open**. It is therefore built and **labeled in-product and in the docs as an owner proposal requiring ratification**, not as settled canon. Anti-Assumption is honored: proposed, not inferred.

**D117 — Share-link hygiene (gap #339, unspecified).** Links are **revocable** and **scoped** (one issue package, or one snapshot). **Expiry is an explicit owner-TBD** — surfaced in-product as an unset value, not invented.

**D118 — Free-tier CRR cap.** The **bounded-cap mechanism** is canon (CRR-01); **the number is not ratified.** Build the cap + counter with the value as an explicit **owner-TBD placeholder**. Doctrine: **virality seeds on Free** — gate collaboration *depth*, never the *seed* of the loop.

**Out of scope (Slice 9):** real auth/permission enforcement, real email delivery, real PDF generation, billing.

---

# Controlled Release & Demand (owner-directed, 2026-07-10) — amends D116/D117/D118

**D119 — Reviewer access is GATED in Alpha/Beta via token-granted Reviewer Principal.** Supersedes D116's "no-account-required" reviewer view. A review-request link carries a **token that grants Reviewer Principal access (DL-049)** scoped to exactly that review package. **The invite IS the authentication** — so a reviewer is *identified and invited*, never anonymous, satisfying D021 (Alpha/Beta invite-only, never anonymous) **without** a signup wall and **without** breaking the CRR evidence loop. Resolves the worker's escalation #1 and gap #337's residue.

**D120 — Bound seats, never bound evidence (the crux rule).** An invite is consumed **only when a NEW principal is admitted** (collaborator seat, or first-time reviewer). **Sending a review request to an existing principal is free, forever, and is never metered.** Rationale: a review request is not a marketing share — it is how the user gets their answer. Bounding new-principal grants controls *supply*; bounding evidence-seeking *sabotages the product* and degrades the user's understanding by design.

**D121 — Controlled-release / waitlist demand mechanics (Alpha/Beta).** Per `controlled-release-demand-framework.md`:
- **Bounded, replenishing invite allocation** — {N} invites per {period}, balance + replenish date always visible (real numbers only).
- **Waitlist with earned position** — improved by converted referrals, by **being review-requested** (strongest inbound demand signal), and by role/org fit.
- **Skip-the-line** — a user may spend an invite to admit someone immediately (the status good).
- **Convert-moment = the waitlist, not a signup** — offered to a reviewer **only after they respond** (post-value, never pre-value); the inviter may grant a seat from their allocation.
- **Phase ramp with an explicit sunset:** Alpha (tight) → Beta (loosening) → **GA: open, anonymous permitted (D021/D024), waitlist retired, limits become tier-based.** The scarcity mechanism is phase-scoped and self-terminating — not the business model.
- **Instrumented** — waitlist size/velocity, invite utilization, review-request→admit conversion, k per loop (TEL-06). Throttling supply without measuring demand is just throttling growth.
- **Guardrails (non-negotiable):** no fabricated scarcity, no dark patterns, the waitlist states plainly what it is, evidence-seeking is never bounded, reviewers are never spammed. OSLO's growth engine *is* its epistemic credibility; it cannot lie in its growth surfaces.

**D122 — Canon tension escalated (NOT resolved unilaterally).** This framework **deliberately gates the seed of the loop** in Alpha/Beta, conflicting with **CHG-061 / Virality-audit P2 (applied): "guarantee the viral primitives on Free… never gate the seed."** *Recommended reconciliation (owner to ratify via Framework 001):* the two are **orthogonal axes** — CHG-061 is a **tier** rule governing GA-phase freemium economics; controlled release is a **phase** rule that **sunsets at GA**, exactly when CHG-061 takes effect. Both then hold, and neither is substantively amended. **This is a recommendation, not canon** — it must route Backlog → Proposal → Review → Decision.

**Owner-TBD (DO NOT ASSUME):** CR-1 {N}/period · CR-2 does a first-time reviewer grant consume an invite (*rec: free/cheap*) · CR-3 waitlist admit rate + curation · CR-4 referral weighting · CR-5 does an inbound review request move the requested person up the queue (*rec: yes*) · CR-6 link expiry (gap #339) · CR-7 is the convert-moment R1 or fast-follow.

---

# Tiering in Alpha (owner-directed, 2026-07-10) — reverses my N-1 advice

**D123 — Basic tier is purchasable during Alpha; tier gating stays LIVE in Alpha.** Supersedes my N-1 recommendation ("make tier limits inert until GA"), which was predicated on the now-false premise that all Alpha users are on Free with no upgrade path. Consequences:

1. **Two orthogonal axes, both live in Alpha, never conflated in UI:**
   - **PHASE (supply)** — who gets a *seat*: bounded invite allocation + waitlist (D119–D121).
   - **TIER (depth)** — what a seat *can do*: Free vs Basic (D112 Free = PDF-only, etc.).
   A user can be blocked by one and not the other; the product must always say **which**, and never present a phase limit as a tier limit (that would be a dark pattern — manufacturing an upsell out of a supply constraint).

2. **CHG-061 is now OPERATIVE IN ALPHA, not just at GA.** This **kills the D122 "tier vs phase, sunsets at GA" reconciliation** — the tier rule no longer waits for GA. The tension now rests **entirely** on **CR-2 (reviewer grants free/unmetered)**: with reviewer grants free, the *seed* of the loop (CRR evidence-seeking) is **not gated on any tier or in any phase**; only **seats** are metered. CHG-061 then holds **literally**. **CR-2 = free is therefore load-bearing, not a preference.**

3. **DL-048 "paid-tier limits TBD" is now blocking, not deferred.** Basic cannot ship in Alpha without a ratified Free↔Basic boundary. Escalated (T-1).

4. **Slice 10 (Tiering & Limits) is now an Alpha-live surface**, not a GA preview: it must show a real Free→Basic upgrade path.

**Owner-TBD (DO NOT ASSUME):**
- **T-1 — the Free ↔ Basic boundary** (DL-048 paid-tier limits). *Recommendation:* **Free must be enough to fully experience the core read** on a real plan (intake → Fast Pass → Overview → Attention → Issues → CRR). **Basic sells depth and volume** (projects, Extended Analysis frequency, artifacts, collaborators/seats, export formats, history retention). Rationale: a crippled Free tier destroys the honest product signal Alpha exists to buy — churned alpha users tell you nothing.
- **T-2 — does tier change the seat allocation {N}?** *Recommendation:* **Yes — invites scale with tier** (Basic > Free). It is an honest monetization lever that meters *seats*, never the *seed*. Consistent with D120 and CR-2.
- **T-3 — is Alpha Basic actually charged, or comped / founding-member priced?** Not assumed. (Superhuman charged full price from a waitlist; scarcity + payment are compatible.) Real willingness-to-pay signal is only obtained if money actually changes hands.
- **T-4 — does billing/payment infrastructure exist in the Alpha build?** Currently out of prototype scope; needs an owner call.

---

# Controlled Release register — RATIFIED (owner: "accept", 2026-07-10)

**D124 — Two limits, never conflated. Always say which one you hit.**
- **Phase allocation** — how many NEW humans a user may bring into the OSLO alpha (waitlist bypass).
- **Tier seat cap** — how many collaborators a PROJECT may hold (Free vs Basic).
A user may have invites remaining and still hit a tier cap, or vice versa. The product must always name **which limit** blocked them. Presenting a *phase* (supply) constraint as a *tier* (upsell) constraint is a **dark pattern** and is prohibited (D123).

**D125 — The ratified register.**
- **CR-1 / T-2 — allocation scales with tier: Basic 5/month · Free 2/month**, replenishing, **non-cumulative**. Free is non-zero because virality must seed on Free (CHG-061). *Correction of record:* my earlier "set N from the 3–6 working-set size" argument **conflated seats with reviewers**. Because CR-2 makes reviewer grants free, the room for **evidence** is already unlimited; **seats** are only for people who must *work inside* OSLO. Seats can therefore be metered tightly **without starving the product** — but only *because* CR-2 is free.
- **CR-2 — reviewer grants FREE and unmetered. Structurally required (not a preference).** Anti-abuse ceiling only. Cost tie: each response triggers an Extended Analysis → DL-048 token budget (a **cost** control, never a monetization gate). This is the sole load-bearing resolution of D122/CHG-061 (per D123).
- **CR-3 — waitlist admits are HAND-CURATED in Alpha**, throttled by **owner onboarding capacity**, not a formula.
- **CR-4 — no points economy.** Three honest bands, date-ordered within each: (1) review-requested, (2) referred by an active user, (3) cold. **No referral-for-credit/discount in Alpha** (canon: referral rewards bounded by unit economics).
- **CR-5 — an inbound review request places you in the TOP band.** Strongest available demand signal.
- **CR-6 — scope link lifetime to purpose.** Share link: **30 days**, revocable, auto-labeled "previous analysis" when stale. **Review grant: expires when the issue resolves, or 14 days, whichever first** — the key was cut for one question. (Configurable expiry for Basic: NOT assumed — owner-open.)
- **CR-7 — convert-moment = WAITLIST ONLY in R1**, shown post-response (never pre-value). **PAY-TO-SKIP IS PROHIBITED IN ALPHA.** Per CR-3 the queue is throttled by onboarding capacity — **payment does not create capacity**, so selling passage past it is a toll booth on an invented constraint: prohibited under the §5 no-dark-patterns guardrail, and it would spend the credibility the product is built on. Pay-to-skip becomes legitimate **only if revenue genuinely expands supply** (e.g. onboarding staffed against revenue) — revisit then, and say so plainly.
- **N-1 — WITHDRAWN/REVERSED** (see D123): tier gating stays **live** in Alpha.
- **N-2 — one identity.** `Principal` is the single identity (DL-049). "Participant" is a **view**: `Membership` (principal × project × role) + `ReviewGrant` (principal × package, scoped). **Membership is where the tier seat cap is enforced.**
- **N-3 — admit as VIEWER by default**, one-click upgrade to Collaborator. Least privilege *and* least cost (a Collaborator consumes a tier seat; a Viewer need not).
- **T-1 — Free ↔ Basic boundary (unblocks Basic-in-Alpha):** **Free fully delivers the core read** (intake → Fast Pass → Overview → Attention → Issues → CRR). **Basic sells depth and volume** — projects, Extended Analysis frequency, artifacts, seats, export formats, history retention. A crippled Free tier destroys the honest product signal Alpha exists to buy.
- **T-3 — Alpha Basic is CHARGED** (founding-member pricing permitted). Comping teaches nothing about willingness to pay; scarcity + payment are compatible (Superhuman charged full price from a waitlist).
- **T-4 — billing/payment in the Alpha build:** required by T-3; **outside prototype scope** — carried to Slice 10 / engineering.

**D126 — Governing principle (canonical statement).**
> **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

**Still routing to Framework 001 (recommendation, not canon):** D122 (CHG-061 reconciliation via CR-2) · D123 (tier-live-in-Alpha consequences) · CR-6 numbers · T-1 boundary. **Owner-open:** configurable expiry for Basic; whether revenue ever expands onboarding capacity (re-opens CR-7).

**D127 — Dark is the product default (owner-directed, 2026-07-10).** Amends D106. Root cause of the prior behaviour: `initTheme()` fell back to the OS `prefers-color-scheme`, so a fresh user on a light-mode machine opened OSLO in light. Now: **a fresh user always opens in dark**, regardless of OS. System preference is honoured **only as an explicit opt-in** — "Match system" sets `theme='system'`, and only then does the OS setting (and live OS changes) drive the theme. Explicit Dark/Light choices persist as before. Applied to Slices 8–9 (the slices carrying Settings/Appearance).

---

# Open-items register — RATIFIED (owner: "accept", 2026-07-10)

**D128 — Two governing principles for metering.**
1. **Meter only what costs money or defines scope. NEVER meter the epistemic record.** Extended Analysis runs cost real tokens (DL-048) → honest lever. Projects and seats define scope → honest lever. **History retention and artifact counts are the epistemic record** — the append-only trace of how understanding evolved (D096) *is* the product's core promise. **Artifacts are never capped. History never expires.** Monetizing the epistemic record would sell the one thing OSLO declares inviolable.
2. **Never sell safety.** Link revocation and purpose-scoped expiry (CR-6) are **trust hygiene for everyone** — never a Basic-only feature. Charging for the secure default is disqualified on a product whose pitch is trustworthiness. **CR-6 configurable-expiry: NOT BUILT, closed.**

**D129 — The ratified open-items register.**
- **X-1 — seats: meter COLLABORATORS only.** **Viewers are unlimited** (read-only changes nothing — closer to a reviewer than a seat; unlimited read-only spread is pure upside). **Reviewers free/unmetered (CR-2).** **Free = 3 collaborator seats (incl. owner) · Basic = 10.** Free must permit *real* collaboration (a co-lead + a stakeholder) — experiencing it is what creates the want, and a one-seat Free tier would breach CHG-061 (comments guaranteed on Free).
- **X-2 — invite refunds:** **no refund once ACCEPTED** (an invite admits a *human to OSLO*, not a membership to a project; refunding on removal creates an add/remove recycling exploit). **NEW — refund on UNACCEPTED/EXPIRED invites:** no human was admitted, so no supply was consumed. Must be added (the build does not do this).
- **X-3 — allocation period: CALENDAR MONTH** (confirm as built). Legible ("resets Aug 1") and shares a cycle with billing now Basic is charged (T-3). Rolling windows are opaque.
- **T-1 numeric caps** — ⚠️ **CORRECTED (see D141): "Basic = 10 projects" was WRONG.** Canon (**UP-3**) ratifies **Basic = 3 projects**. Correct values: **Free = 1 project · Basic = 3 projects**; small/generous monthly Extended Analysis budget (numbers owner-open); **UNLIMITED artifacts · FULL History** on every tier. Per D128, the only metered dimensions are **analysis runs** (cost-linked) and **projects + collaborator seats** (scope-linked). *(Seat caps Free 3 / Basic 10 are a different number and are NOT affected.)*
- **"Sponsor" = `TEAMMATES[].role`** — confirmed as-is (cosmetic).

**D130 — Numbers are instrumented hypotheses, not settled canon.** Every value above (3 / 10 / 1 project) is a judgment, not a derivation. They were chosen to be **easy to loosen and painful to tighten** — the right direction of error before real alpha data exists. They must be instrumented and revisited against alpha behaviour.

**Still OWNER-OPEN (not assumed):**
- **T-3 — Basic price.** Business call; not invented. *Method recommended:* price against **the alternative** (the plan review a consultant would run), **not** against PM tools ($10–25/seat). Pick a **founding-member price you would be embarrassed to lower later**, declare it time-limited, and lock it for early users.
- **"Does a Reject move CAF?"** *Recommendation (requires Framework 001 — NOT built):* **yes, via Alignment.** A stakeholder rejecting a finding is literally evidence about **Alignment**, a first-class CAF dimension (DL-062) — so it may move Alignment and Reliability, while still **never auto-resolving the issue and never overwriting OSLO's read** (D115). Nothing ratifies this today, so it stays out of the build.
- **Whether revenue ever expands onboarding capacity** (would reopen CR-7 pay-to-skip).

**D131 — Framework 001 routing: ONE consolidated proposal, not four.** Package title: **"Controlled Release & Tiering-in-Alpha."** Contents: D122 (CHG-061 reconciliation via CR-2) · D123 (tier live in Alpha) · T-1 boundary + caps · CR-6 closure · Reject-moves-CAF. Rationale: these are **interdependent** — CR-2 is the *sole* resolution of D122, and T-1 exists only because of D123. Split into separate proposals, a reviewer could ratify one while silently breaking another.

**D132 — Final Slice 9 closures (owner: accepted, 2026-07-10).**
- **X-2a — pending invite expiry = 14 days.** Long enough for a busy stakeholder; short enough that supply isn't parked indefinitely. On expiry the invite **refunds** to the balance (D129) with a History event.
- **Seat cap vs downgrade — NO EVICTION.** Basic (10 seats used) → Free (cap 3): **nobody is removed.** The account simply cannot **add** another Collaborator until it is back under the cap. Evicting humans from a project to enforce a billing change is a severe act on a trust product; the non-destructive rule costs nothing and is now canon.

**D133 — A Reject MOVES CAF, via Alignment (owner: ratified, 2026-07-10).** Closes the last Slice 9 escalation.
A stakeholder **Reject** on a CRR review request is **evidence about Alignment** — a first-class CAF dimension (DL-062) — not merely a comment. It may therefore move **Alignment** (and **Reliability**, as any attested evidence does) through a normal Extended Analysis run.
**Bounded exactly as D115 binds every reviewer response:**
- It is **evidence, not truth** — recorded as a **third-party attestation** ("Attested by <name>"), never as OSLO's own read.
- It **never auto-resolves and never re-opens** an issue by itself; only an analysis update moves the read.
- **OSLO never self-accepts it.** A Reject is evidence *that a stakeholder disagrees* — never proof the plan is wrong.
- Symmetry note: an **Approve** is *also* Alignment evidence. Neither direction is privileged; both are attested inputs to the same run.
Rationale: refusing to let a Reject touch CAF would mean OSLO watched a sponsor reject a finding and learned **nothing about alignment** — which is precisely the dimension the event speaks to. Requires the Framework 001 package (D131) to become repository canon.

---

# Slice 10 — Tiering & Limits (FINAL SLICE) — owner: "accept all", 2026-07-10

**Governing rule for this slice: canon decides; I adopt and cite.** Where canon has ratified a number, it is used with its citation and **not re-proposed**. This is the direct correction of the Basic-10-projects failure (DL-102 Correction #3).

**D134 — Adopted from canon, unchanged (cited, not re-decided):**
| Value | Source |
|---|---|
| Free = **1** active project · Basic = **3** | UP-3 |
| Daily fixes: Free **5** · Basic **20** | MON-02 / UP-1 |
| Daily chat: Free **20** | MON-03 / UP-2 |
| Deep runs/day: Free **2** | UP-5 |
| Export: Free = **PDF only** | MON-01 / SHARE-04 |
| Free scope = full Workspace · Confidence · CAF · MRI · Issues · Recommendations · Sharing · Comments · **CRR** | MON-01 + CHG-061 |
| Seats: Free **3** · Basic **10**; **Viewers unlimited**; **reviewers free** | DL-102 B/E |

**D135 — Plans / upgrade surface.** Real (simulated) Free → Basic upgrade. **Pro is named only as a forward capability** (continuous monitoring, UP-7) — not purchasable in R1. **Basic price renders as an explicit owner-TBD. No invented number.**

**D136 — Honest counters.** Visible counters for projects · daily fixes · daily chat · deep runs/day, with real values and real reset times. Values canon has not settled (Extended-Analysis budget, size envelope, monthly budget gate) render **visibly unset** — never as fabricated numbers, never as fake scarcity.

**D137 — Upgrade prompts: UP-1…UP-8 exactly as ratified (MON-04).** Two trigger classes — **value-moment** (fires at a positive peak; sells the *next* capability; rare, strict cooldown) and **friction-moment** (an **honest limit disclosure + the specific relief**). **Standing rules:** *no persistent upgrade wallpaper*; every prompt is **contextual, value-based, and names the specific limit hit AND the specific tier that relieves it** — never a generic "upgrade." **Global guards:** never interrupt an active Fast/Deep pass · never fire before first value (first MRI delivered) · per-trigger cooldown + a global per-day cap.

**D138 — The limit-reached interaction rule (DL-102 E-1 / Seam Audit 001) applies to EVERY cap.** A limit-bearing affordance **stays enabled**; the *attempt* is gated and surfaces the matching prompt **with resolutions** — e.g. a 2nd project → *"upgrade **or** archive the current project"* (archiving is reversible and frees the slot, DL-058). **Never disabled, never hidden** — disabling suppresses the highest-intent moment — and **never a raw error.** **This corrects Slice 9**, where the collaborator seat cap *blocked* instead of *prompting*.

**D139 — Envelope exceeded → partial orientation (UP-4).** When a project exceeds the Free size envelope, OSLO delivers a **partial** analysis with an **honest disclosure**, fired on **one surface** together with the prompt — never two competing notices. **This is an epistemic-honesty requirement first and a monetization surface second:** if OSLO only saw part of the plan, it says so, plainly, whether or not anyone upgrades. The envelope size is **owner-TBD** (UP-4's "~100k words" is illustrative in canon, not ratified).

**D140 — The Tier-Definitions census (the real deliverable).** Slice 10 is the surface that **consumes every tier number**. The build produces `tier-definitions-census.md`: every number the product needs, each marked **RATIFIED (with citation)** or **UNSET (owner decision required)**. This is the evidence-based table of contents for the missing **`RELEASE_1_TIER_DEFINITIONS_V1`** — cited as authoritative by **18 documents**, never written, and escalated in **DL-102 Concern 7** as a **blocking prerequisite for shipping Basic in Alpha**.

**Deliberately NOT invented (render unset):** Basic price · Extended-Analysis budget numbers (shape ratified: Free small / Basic generous) · Free size envelope · monthly budget gate (UP-6).


---

**D141 — T10-1 correction: Basic = 3 projects (canon UP-3), not 10.** Closes the last contradiction from the Basic-projects error.
Two of my own records disagreed: **D129 T-1 said "Basic = 10 projects"**; canon **UP-3** (`12_freemium_tier_behavior_logic.md`) ratifies **Basic = 3**. The Slice 10 build followed canon (3); **D129 T-1 is now corrected above** so the contradiction does not outlive the session. **DL-102 already carries the correction** in repository canon (Correction of record #3).
**Scope of the error, for the record:** the invented number propagated from a recommendation → an owner ratification made on my advice → the D129 register → the Slice 9 prototype (`BASIC_PROJECT_CAP = 10`) → **and into a hard-coded copy string** (`'10 projects · 10 seats'`) that would have survived a constant-only fix. All corrected in Slice 10; **every displayed tier number is now painted from its constant**, so copy can no longer drift from canon.
*(The **seat** caps — Free 3 / Basic 10 — are a different quantity and were never in conflict.)*

**D142 — Remaining Slice 10 escalations (NOT resolved; carried to the owner).**
- **T10-2 — UP-5 presumes an affordance D006 forbids.** UP-5 caps a manual "reanalyze" control, but **D006 ratifies event-driven reanalysis only** — there is no manual button to cap. The build gates user-initiated triggers and **never** gates an evidence run (CR-2 holds). **Owner must state what the deep-run cap attaches to.**
- **T10-3 — seats and export formats have no slot in the ratified UP-1…UP-8 taxonomy**, though D138 governs their behaviour. Built as `UP-SEAT` / `UP-EXPORT`; **no canon numbers assigned** — owner to place them.
- **T10-4 — MON-04 requires a global per-day prompt cap and never sets it.** Guard enforced; number renders unset; the build **errs toward silence**.
- **The 11 UNSET tier values** (see `slice-10-tiering-limits/tier-definitions-census.md`): Basic price · billing rail · Basic daily chat · Basic deep-runs/day · Free + Basic monthly Extended-Analysis budget · UP-6 gate threshold · Free + Basic size envelope · Free CRR cap · global prompt cap/day.

---

# Reporting (M4) — design locked (owner: "accept all", 2026-07-12)

**D143 — ONE composable readout, not six report types.** Revises my own scope brief. Grilling it: **"leverage read" is not a report — it is the §2 section** (what's limiting the read); **"reliability disclosure" is not a report — it is §5, and it appears in EVERY report**; and alignment / assumptions / decisions are **not artifacts a PM sends separately — they are sections of one memo.** Fewer objects, less to name, less to spec, and it matches what a PM actually wants: **one artifact they can shape for the room.**

**D144 — The spine (fixed; §1–§5 always present).** What makes a report *strategic* rather than a data dump is **selection and framing, not volume**. A dump ("here are 12 issues") makes the PM look like a **clerk**. The spine is the shape of a good executive memo — **so what · how do we know · what now**:
1. **The read** — one line; understanding maturity, reliability-qualified. **Never health, readiness, RAG, or probability of success.**
2. **What's limiting it** — the limiting CAF dimension **and the specific reason**. Prioritization *with a reason*, not a list.
3. **What we don't know** — unvalidated assumptions, open clarifications. **The status-conferring part** — *"here's what we haven't validated"* is how senior people talk.
4. **What I need from you** — decisions owed, evidence outstanding (MRI-07 Understanding Dependencies). **Turns the PM from reporter into agenda-setter.**
5. **How to read this** — reliability basis (Coverage · Evidence · Assessability), analysis-currency marker, standing disclaimer. **A report without §5 is not shippable.**
**Optional sections (Basic):** Alignment · Assumptions · How our understanding matured (History narrative) · Artifact detail.

**D145 — BINDING: tailor the ASK, never the READ.**
> **Re-framing the assessment by audience is SPIN** — the *"make me look good by shading the truth"* failure — **and it would destroy the PM's credibility in front of the exact people they are trying to impress.**
- **§4 (what I need from you) IS addressed to the recipient.** ✅
- **§1–§3 (the read, the limiter, the unknowns) are IDENTICAL for every audience.** ❌ **never re-framed.**
**One honest read. Many asks.** This is what keeps the status lever from becoming a spin machine — the single way this feature could turn on the product.

**D146 — Live composer → dated snapshot.** The readout is a **live composer in-app** (pick sections; watch it assemble from current understanding) producing a **dated snapshot** on export. **The snapshot is what travels.** Carries the **analysis-currency marker**; a stale one is labeled **"previous analysis"**, never presented as current. **Packages, never produces — generating a report runs NO analysis** (Export doctrine, already asserted in the build).

**D147 — Tiering + scheduling + names.**
- **Free** — the **read snapshot**: spine §1–§5, PDF, OSLO-marked. **CHG-061: the seed is never gated** — it must be able to travel into an exec's inbox.
- **Basic** — the **composable readout**: optional sections, branding, scheduling, all export formats. **The seed is not gated; the depth is.**
- **Scheduling** at Basic (R1 if cheap — a weekly readout is the PM's recurring obligation, and automating it is the labour half of the lever). **A scheduled report MUST re-check currency**: if the analysis is stale it says so; it **never quietly ships a stale read as current.** *(R1-vs-fast-follow: owner-open.)*
- **Names: owner/glossary decision (DL-053).** Build labels descriptively, flags "naming pending." **Avoid "status report"** — that is the clerk artifact this feature exists to escape — and **anything implying health or readiness** (DL-104 §5 P1).

**The binding risk (carried in-product):** the PM puts OSLO's output in front of their leadership **under their own name**. A mis-framed claim in a status update is **embarrassing**; **in a board-level strategic read it can end a career.** Rigorous reliability-qualification is therefore **not doctrinal fussiness — it is protection of the user's reputation, which is what they are buying.**

---

# Reporting — REDESIGN (owner-directed, 2026-07-12). Revises D144/D146/D147.

**D148 — Reports is a WORKSPACE, not a modal.** Peer to Overview · Attention · Artifacts · Issues · History. Left: the live composer. Right: the readout rendering as an actual document.

**D149 — THE GOVERNING WRITING RULE (corrects my own spine).**
> **The doctrine governs what the report may CLAIM. It must NEVER govern how the report SOUNDS.**
My spine (D144) was **OSLO describing its own epistemic state** — a section literally titled *"How to read this"*, headings like *"What we don't know"* and *"What's limiting it."* That is a report **about OSLO's understanding**, not a report **about the project**. **Struck.**
**The report is written for its reader, in their language.** It is an **executive summary** — familiar style, layout and vocabulary. **ZERO OSLO vocabulary:** no *confidence · CAF · reliability · understanding maturity · assessability · artifacts · the read · Outcome Orchestration*.
**The epistemic honesty appears as ORDINARY GOOD WRITING.** Canonical example — derived-vs-attested, rendered without jargon:
> *"80% support coverage is sufficient. **This came from the plan, not from Support.**"*
The sponsor now knows exactly how much to trust that number. No doctrine was spoken.

**D150 — Structure (owner-set).**
1. **Summary** — executive-level, **standalone**. A sponsor who reads only this has the whole picture.
2. **What's changed since previous week** (versus \<date\>).
3. **Key risks** — **before** assumptions.
4. **Key assumptions** — what the plan rests on that is unconfirmed.
5. **Plan of action** — strategic next steps.
6. **Decisions needed from you** — with owner + what each unblocks.
7. **Appendix — per-workstream detail** (for the leads; the sponsor can ignore it).

**D151 — TWO ALTITUDES on every risk (the strategic differentiator, owner-set).**
Every risk is framed at **both** altitudes:
- **For the plan** — what breaks in the schedule/scope (**deliverable impact**).
- **For the goal** — what it means for what the project exists to achieve (**outcome impact**).
*A delay is a schedule problem. A delay that means you miss the thing the project exists for is an outcome problem. **Same fact, different altitude** — and knowing which one you are looking at is what separates a senior read from a status update.* This is also what lets the PM **subtly elevate** an item by outcome impact or feasibility.
> ⚠️ **KNIFE-EDGE — binding.** **Outcome impact = "does the plan, AS WRITTEN, still reach its stated intent?"** — a **structural claim about the plan** (Intent is a plan artifact; it is what Clarity and Alignment are measured against).
> **It is NOT "will this project succeed?"** — a **prediction**, which doctrine forbids. **Frame BY outcome; never FORECAST the outcome.**

**D152 — "Plan of action" is the PM's, in the PM's first person. OSLO seeds; the PM owns.**
> **If that section reads as OSLO's plan, the PM becomes a PASSENGER IN THEIR OWN REPORT — and the entire status lever collapses.** The sponsor does not think *"my PM is sharp"*; they think *"the tool wrote this."*
OSLO **seeds** next steps from its recommendations; **the PM edits and owns them.** This is also the only form compatible with **advisory-only** — OSLO never decides. **Everything above the plan of action is OSLO's honest read in plain English; the plan of action is the PM's judgment.** That division is what makes the artifact both **trustworthy and career-safe**.

**D153 — The disclaimer is a property of the PACKAGE, not a paragraph in the PROSE.** (Revises D146.)
`EXPORT_AND_SHARE_OUT_EXPERIENCE_SPECIFICATION_V1` (ratified) requires **"every package carries an explicit disclaimer"** — so it **stays**, but it moves to the **PDF cover / share-link metadata — the wrapper the artifact travels in** — and **out of the memo body**. Canon satisfied (*the package* carries it); the writing is saved.
*Rationale:* a line saying *"this isn't a forecast"* **invites the reader to wonder whether it was trying to be one.** The real protection is that the memo **never makes a forecast claim** — no score, no RAG, no probability. Belt-and-braces here **undermines the credibility it is meant to protect.**
The **currency marker stays in the body** as plain attribution: *"Riverside relocation · plan as of 12 July · \<PM name\>"*.

**D154 — Editing is FREE. The gate is REUSE, not EDIT.** (Revises D147.)
**Rejected:** gating in-app editing on Free. Two reasons —
1. **It would make the PM sign words they could not correct.** The report goes out **under their name**; selling back the ability to control it monetizes their credibility, in the one artifact where it is on the line.
2. **It is a commercial own-goal.** They would export and edit in Word — **stripping the currency marker, the provenance and OSLO's fingerprint**, and killing the viral surface. You would be gating your way out of the loop.

**The gate instead:**
- **Free** — **full edit, every time, from scratch.** Full read, all sections, PDF export. **Nothing persists.**
- **Basic** — **your edits PERSIST.** Standing text, tone, section choices and boilerplate carry week to week and auto-apply. Plus optional sections, branding, scheduling, all formats.
*The readout is a **recurring obligation**. Rewriting the same framing every Friday is the tedium; **not having to** is the product.* Pure labour lever, fires weekly, entirely sayable out loud — and **it never makes a PM sign words they could not change.**

**D155 — The PM's own prose: a gentle note, never a block (owner: accepted, 2026-07-12).** Closes the escalation the rebuild raised.
The vocabulary and forecast guards **exempt the PM's own sections — and they must** (policing the user's prose would be the tool writing the report again, which D152 forbids). But that leaves a real hole: **a PM can type *"we're 80% likely to hit 450"* into their own summary, and it ships under OSLO's mark, on OSLO's cover, carrying OSLO's disclaimer** — a forecast wearing OSLO's credibility.
**Resolution — OSLO offers a gentle, NON-BLOCKING note. It never blocks, never edits, never refuses to send.**
e.g. *"Heads up — this reads as a forecast. OSLO doesn't predict outcomes, and this goes out under OSLO's mark."*
*Rationale:* **blocking would be the tool overruling the human** (violates advisory-only, D001). **Silence would be OSLO lending its name to a claim it forbids itself.** The note is the only honest position — and it protects the PM from the exact reputational hit the feature exists to prevent. **The PM may dismiss it and send anyway. Always.**

**D156 — The `To:` line stays.** D145 (*tailor the ask, never the read*) forbids **re-framing the assessment** by audience — it does not forbid **addressing** the document. A memo without a recipient is not a memo. The guard remains **section-scoped**: §1–§4 are byte-identical across recipients; only the decisions section varies.

**D157 — Report length: selection is the value; the cut is spec'd, not invented.** Risks capped at 5 (highest impact first); the appendix walks every workstream and is explicitly skippable. **What gets cut and who decides** is carried as an open item for the M4 spec — *no truncation rule invented*.

**D158 — Defect fix: `_assertNoGenericUpgradeCopy()` (MON-04).** The guard failed when `TIER==='basic'` because **UP-6 only names "Basic" in its Free branch** — a Basic user got a red console at boot. **The guard was checking the wrong condition:** MON-04 requires a prompt to name **the specific tier that relieves the limit**, which is only meaningful when the user is **below** that tier. Fixed: require the tier name only when the user is beneath it.

---

# D159 — OBEY THE DOCTRINE. DON'T NARRATE IT. (owner-directed, 2026-07-12 — GLOBAL, applies to every surface)

**The failure, and its cause.** Across the prototypes the product **explains its own reasoning to the user**: canon citations (DL-/D-numbers, CR-2, CHG-061), rationale paragraphs, escalation notes, "the upgrade we deliberately did not build", "naming pending", governance meta. **This is my error.** I repeatedly instructed workers to *"carry the note in-product"* and *"say it out loud."* The **say-it-out-loud test was a constraint on BEHAVIOUR** — *don't do things you'd be embarrassed to explain* — **and I turned it into a CONTENT REQUIREMENT** — *explain everything*. They are not the same thing, and conflating them turned the app into a museum placard about itself.

**The rule (generalizes D149 from the report to the whole app):**
> **The doctrine governs what the product may CLAIM and DO. It must NEVER govern how much the product TALKS.**
> **Obey it everywhere. Speak it almost nowhere.**

**Binding:**
1. **Default to the content.** The user's work is the surface. Chrome, options and explanation are **not** resident on it.
2. **No meta in product copy.** No canon references, no rationale, no governance vocabulary, no design commentary.
3. **Progressive disclosure.** Explanations exist **on demand** (info affordance / hover / "why") — **never resident**.
4. **Bias to simplicity and readability**, everywhere — modals included. *(Owner: "across many modals in app, there is too much meta information disclosed, and no consideration of readability and simplicity.")*

**D160 — Reports workspace: the reading surface is sacred.**
**Default view = THE REPORT, AND ONLY THE REPORT.** Full-width, centred, comfortable measure. **Remove from the reading surface:** the recipient picker, section toggles, the package wrapper, option panels, advisory chrome, meta commentary.
**Controls move OFF the reading surface** — a slim toolbar / drawer (Recipient · Sections · Format · Export · Schedule). Opened on demand, closed by default.
Mandatory items keep their homes: the **currency marker** stays in the body as plain attribution (D153); the **disclaimer** stays on the **package wrapper** (shown at export, not while reading); the **forecast note** (D155) appears **only when triggered**, inline, subtle, dismissible — never resident.

**D161 — "Prototype notes" toggle (OFF by default).**
The prototype must carry owner-TBDs, guards, canon citations and escalations **for review** — but they must not pollute the product. **Move ALL of it behind a single "Prototype notes" toggle, OFF by default.**
- **Off** → it looks and reads like a product.
- **On** → every owner-TBD, canon citation, retired lever, guard and escalation is revealed for governance review.
This is what the owner meant by *"mandatory informational sections must be enabled via a different path than taking up valuable reporting real estate."*

---

# D162 — Issue Panel: progressive disclosure, and the D159 sweep missed the panels (owner, 2026-07-12)

**The D159 sweep hit modals and big surfaces and MISSED THE PANELS — where the doctrine copy accumulated worst**, because the Issue Panel is where *every* doctrinal rule has a touchpoint (evidence · provenance · comments-never-change · share-never-changes · append-only · CR-2). **It became a museum.** Observed:
- *"Sends the issue + its context + the recommendation + the artifact reference. It never changes the issue."* — the product explaining its own contract.
- *"This is a **validation recommendation** — the kind that a second pair of eyes settles fastest. Prime candidate for a review request."* — **design rationale, out loud.**
- *"0 review requests sent · **free and unlimited** — on every plan"* — **reassuring the user that CR-2 is honoured.** That is a note to the owner, not to the user.
- **Comments states "never change the assessment" TWICE**, plus *"a conversation about the read, recorded next to it"*, plus an append-only lecture.

**D162a — THE COPY RULE (extends D159).**
> **Say the honest thing ONCE, in the fewest words, at the moment it matters. Never twice. Never with its rationale.**
Honest **labels** stay (*"Comments never change the assessment"* — D111). Everything wrapped around them goes. Contracts and explanations move to an **info affordance**, never resident.

**D162b — Progressive disclosure, driven by user intent.**
The user opens an issue to learn **"what's wrong, and what do I do about it?"** Everything else is an action they may or may not want.
- **Always visible:** title · severity · dimension · where it lives · the plain-language read. Plus **ONE primary action**, contextual (*Apply this fix* if there is a recommendation; *Answer* if OSLO is asking).
- **Everything else collapses to a single scannable row** — count, chevron, **real hover state**: Evidence · Recommendations · Clarification · Comments · Share for review · Discuss.

**D162c — Affordance defects (owner-reported).**
- **Evidence looks flat.** It has a `▸` but **no hover state and no affordance** — the user cannot tell it expands. **Fix:** hover background, pointer cursor, rotating chevron, count.
- **Clarification defaults EXPANDED** with a large empty textarea. **A big empty textarea shouts "do work now"** and dominates a panel the user opened to *read*. **Fix: default MINIMIZED** — one line stating what OSLO needs, expanding to the input on click.
- **Share for review** carries three lines of explanation. **Fix: just the button.** The contract moves to an info tooltip; the "validation recommendation" hint and the CR-2 counter are **deleted**.

**D162d — Same treatment cascades** to the Recommendation panel and the artifact flyout (same disease).

---

# D163 — HARD WORD BUDGETS. The sweep is not done until every surface fits. (owner, 2026-07-12)

**Exhibit:** the Basic upgrade prompt shipped as a **~300-word, six-paragraph essay** — *"What we are NOT selling you is the right to your own words"* · *"spin, in front of the exact people you are trying to impress, is what would end you"* · *"OSLO does not produce those, at any price."* **That is the decision log pasted into a dialog.** Every sentence was written to persuade the **owner**, not to serve the **user**.

**"Be concise" is a wish. A budget is a constraint.** Binding, on every surface:

| Surface | Budget (user-visible words) |
|---|---|
| **Upgrade / limit prompt** | **≤ 30** — MON-04 requires exactly three things: **the limit hit · the tier that relieves it · the resolutions.** That is a sentence, not an essay. |
| **Tooltip / ⓘ** | ≤ 20 |
| **Modal body** | ≤ 60 |
| **Empty state** | ≤ 15 |
| **Panel row / label** | ≤ 8 |
| **Toast** | ≤ 12 |

**Ban outright, everywhere in product copy:**
- Any sentence explaining **why** we do something.
- Any sentence about what we **"will never do."**
- Any sentence that **names or paraphrases a doctrine**.
- Any **second sentence** that restates the first.
- Any **reassurance addressed to the owner** rather than the user.

**The test for every string:** *If a real product shipped this sentence, would a user read it — or is this the team talking to itself?*

**What survives:** the **honest label**, once, short. *"Editing is always free."* — yes. A paragraph about credibility and what we would never charge for — **no**.

**Scope: EVERY surface.** Modals · popovers · panels · prompts · tooltips · empty states · toasts · drawers · dialogs · banners. **The sweep is not complete until every one is inside its budget.**

---

# D164 — The Readout is a DOCUMENT. Give it the artifact editor. (owner, 2026-07-12)

**The Readout workspace must look, feel and behave like the Artifact workspace.**
- **WYSIWYG editing** — not a stack of textareas.
- **The user engages with readout content exactly as they engage with artifact content**: same editor, same interaction model, same affordances (inline rich text, selection, formatting, undo/redo, slash menu, find/replace, keyboard behaviour).

**Rationale:** a readout **is** a document, and artifacts **are** documents. One editor, one mental model — and all the editor work already done (D066–D085) applies for free.

**Constraints preserved:** the PM's sections stay PM-owned and byte-verbatim (D152/D155) · OSLO-authored sections remain reliability-qualified and free of OSLO vocabulary (D149) · *tailor the ask, never the read* (D145) · editing free on every tier; the gate is reuse (D154).

---

# D165 — OSLO Chat: make it a CONVERSATION, not a wall (owner, 2026-07-12)

**The disease.** One "ask about this issue" reply currently contains: title + severity + dimension + artifact + status · *Why it matters* · *What it weakens* · *My recommendation* · an epistemic chip · an "I inferred this" paragraph · a reliability-basis paragraph · 2 evidence cards · 2 context cards · **4 action cards each with an explanatory subtitle** · a clarification form with an open textarea · 3 "Ask next" chips — **and then the composer offers 3 DIFFERENT chips of its own.**
**That is a document pretending to be a message.** It pushes everything at once and asks for one decision. **Chat is the one surface where detail can be PULLED — and it was the one place we pushed hardest.**

**D165a — Progressive, user-driven depth.**
- **OSLO's opening turn is SHORT** — what it is, why it matters, and **one honest epistemic line**. That is all.
- **Every turn ends with a HANDOFF** — 2–3 contextual next moves. *This is what makes it a conversation, and it is what creates engagement.*
- **Detail is PULLED, never pushed.** Evidence · options · recommendation · reliability basis each arrive **only when asked for**, one at a time.
- **ONE IDEA PER TURN.** OSLO says one thing and stops.

**D165b — Actions appear when relevant, not all at once.** The four action cards (Open issue · Discuss · Apply fix · Open artifact), each with an explanatory subtitle, are **cut**. Surface the **one** action that fits the moment; the rest are reachable, not resident. **Subtitles → deleted** (they are the product explaining its own contracts — D159/D163).

**D165c — ONE set of suggestions at a time (fixes a real confusion).**
Two competing prompt sets ("ASK NEXT" in the message vs the composer's chips) leave the user unsure which to use.
- **In-message chips = the conversation's next moves** (contextual to what OSLO just said).
- **Composer chips = an EMPTY-STATE affordance only.** They **disappear once a conversation is underway.**
**Never both at once.**

**D165d — Visual separation of context blocks.** A new issue's thread must **read as a new thread**. Insert a clear context divider when the context changes; adjacent blocks currently appear merged.

**D165e — The clarification form collapses**, as everywhere else (D162c): a one-line prompt that expands to the input on click. **An open textarea shouts "do work now"** in a surface the user came to *read*.

**Preserved (compressed, never removed):** the epistemic honesty stays — but as **ONE line** (*"I inferred this — it isn't in your inputs."*), not a chip **plus** a paragraph **plus** a reliability block. Reliability basis is available **on request**. Advisory-only holds: chat never mutates, never selects a path, never resolves an issue.

---

# D166 — GUARDS MUST TEST MECHANISM, NOT COPY (2026-07-12)

**Four vacuous guards have now been caught in this prototype** — each one *passing while the thing it protected was broken*:
1. **Export drawer** — the button wasn't in the DOM when the drawer was shut, so the check passed for free.
2. **Recommendation row** — it checked the element's own `display`, but the *ancestor row* was hidden.
3. **Closed panel** — it graded a stale, closed panel's DOM.
4. **Chat reliability** — it looked for the bare word *"Moderate"*, which the qualifier sentence already contains. **Deleting the entire reliability basis still passed.**

**The pattern is unmistakable:**
> **A guard written against COPY rots the moment the copy changes. A guard written against MECHANISM survives.**
> **A guard that cannot fail is worse than no guard — it is a false assurance that a doctrine is being honoured.**

**Binding, for every doctrinal guard:**
1. **Test the mechanism, not the string.** Prefer a **state proof** (snapshot the model, exercise the path, assert nothing moved) or a **mechanism proof** (assert the code path cannot reach the prohibited state) over a **DOM/copy scan**.
2. **Every guard ships with a NEGATIVE CONTROL** — an injected regression proving the guard bites. **A guard without one is presumed vacuous.**
3. **When copy changes, re-verify the guards that referenced it.** Fix the **guard**, never the doctrine.

---

# D167 — Chat: the O-D closures (owner: approved, 2026-07-12)

**O-D165-1 — the clarification prompt stays VISIBLE in the opening turn (collapsed).** A chip is enough surfacing for **detail**. **But a question OSLO needs answered is not detail — it is a REQUEST**, and hiding a request one click deep means a blocked issue can sit unanswered because the ask was never seen. **Keep the one-line prompt in the opening (collapsed, expands on click, per D162c/D165e); the chip remains a shortcut.**

**O-D165-2 — the opening carries ONE action** (*Open this issue →*), consistent with D162b. Confirmed as built.

**O-D165-3 — D163 gains chat word budgets:**

| Surface | Budget |
|---|---|
| **Chat — opening turn** | **≤ 50** |
| **Chat — pull turn** (evidence · options · recommendation · reliability) | **≤ 40** |

**O-D165-4 — cosmetic:** with prototype-notes ON, the `pn()` block renders **below** the handoff chips in the tier answers. Move it above them.

---

# D168 — REPORT vs MEMO: two objects, one lifecycle (owner, 2026-07-12)

**The document has two states, and they are different objects:**

| | **REPORT** | **MEMO** |
|---|---|---|
| **What it is** | The **living document inside OSLO** | A **dated snapshot that has LEFT OSLO** — exported, shared, sent |
| **State** | Editable · current · tracks the read | **Fixed. It never changes again.** |
| **Presentation** | **A working document — looks and edits exactly like a plan artifact** (flush, top-left, `.doc`, continuous WYSIWYG) | **A memo — paper presentation**, its own quieter typographic voice, the cover, the **disclaimer**, the **currency marker** |
| **Doctrine** | **Live understanding** | **A package** — *"packages existing understanding"* (Export spec) |

**This reconciles both prior instincts: each was right, in the wrong place.** The paper-sheet styling was not wrong — **it was applied to the wrong object.** A memo *should* look like a memo; but only once it **is** one. While it is being written, it is a **report**, and a report is a document.

**It lands exactly on D146** (live composer → dated snapshot): **you edit a REPORT; what travels is a MEMO.**

**Binding:**
1. **The live editing surface is a REPORT.** Flush, top-left, `.doc` typography, continuous WYSIWYG — **artifact parity** (D164). **No card, no shadow, no paper.**
2. **The snapshot / export preview / the thing that travels is a MEMO.** **Restore the paper presentation there** — card, measure, and the memo's own typographic voice (this closes the escalation about the deleted 13px body type: **that voice belongs to the memo, not the report**).
3. **`REPORT_SNAPSHOTS[]` are MEMOS.** Every dated snapshot in History is a memo. **A memo is immutable.**
4. **Naming (partially closes R-O1):** the working document is a **report**; the sent artifact is a **memo**. *(Whether the workspace is called "Reports" remains an owner/glossary decision.)*
5. **Never call the live document a memo, and never call the sent artifact a report.** They are different objects with different rules.

**D169 — History opens the sent memo (owner: approved, 2026-07-12).** Closes O-D168-2.
Every dated snapshot **is** a memo (D168 §3), and a sent memo is **the most auditable artifact in the product** — the thing that went to the board, **under the PM's name, on a date**. *"What did I actually tell them in June?"* is a question a PM will ask, and OSLO already holds the answer **frozen and byte-exact**. Leaving it unreachable wastes the one immutable record the product has.
- A **"memo sent"** History event **opens the memo** — the exact bytes that travelled, with its cover, disclaimer and currency marker.
- **Read-only, always** (Slice 7's contract holds; D168 §3 immutability holds). Opening a memo **changes nothing** and **runs no analysis**.
- The memo is shown **as it was sent** — never re-rendered from current understanding. *(Re-rendering it would silently rewrite history.)*

---

# D170 — DEFECT: a gated attempt that surfaces NOTHING. And the guard that didn't catch it. (owner-reported, 2026-07-12)

**Reproduced.** On **Free** with the format set to **"Export link"** (a Basic-only format): the Export action **does nothing**. No export, **and no upgrade prompt**. `genReport()` correctly gates the attempt and calls `fireUP('UP-EXPORT')` — **but no prompt renders.** The button is live, the click lands, and the product **stops silently.**

**An enabled control that silently does nothing is WORSE than a disabled one.** A disabled control at least tells you something.

**D170a — The guard passed, and that is the finding.**
`_assertNoDisabledLimitAffordances()` proves the Export button **is not disabled**. It is not. **What it never proved is that the ATTEMPT DOES ANYTHING.**
**D138 has THREE clauses** — *the affordance stays enabled* · *the attempt is gated* · **_the prompt appears, with resolutions_** — **and the guards only ever verified the first.**

> **This is the ninth guard failure of the same shape. Extend D166:**
> **Do not merely prove the control is LIVE. Prove the ATTEMPT HAS A CONSEQUENCE.**
> For **every** limit-bearing affordance: **fire the gated attempt and assert a prompt renders, naming the limit and the tier that relieves it, with its resolutions.** A gated attempt that produces **no visible outcome** is a **P1 defect**.

**D170b — Fix the defect.** Every `fireUP(...)` path must render its prompt. Sweep **all** UP-* prompts, not only UP-EXPORT: any that fires into the void is the same bug.

**D170c — Readout toolbar: drawers → POPOVERS (owner).** The toolbar menus (Recipient · Sections · Format · Schedule · Export) become **popovers anchored to their buttons**, not a drawer that displaces the document. Cleaner, and it keeps the reading surface still while you act on it (D160).

# D171 — The Readout has no SEND. (owner, 2026-07-12)

**A readout is a thing you SEND — and there is no send action.** The toolbar has a **Recipient** picker (which only *addresses* the document) and **Export** (which produces a file). **You can compose a readout addressed to the Sponsor and then be unable to send it to the Sponsor.** D169's own History event is called **"memo sent"** — *sent by what?*

**Canon already separates the two:** `INVITE_AND_SHARE_MODAL_EXPERIENCE_SPECIFICATION_V1` — *"an optional private invite link that **routes into OSLO** … **distinct from Export's outside-review link**"*. The export spec is literally **"Export *and Share-Out*."**

| | **SHARE / SEND** | **EXPORT** |
|---|---|---|
| **What** | the memo **goes to named people** — in-app notification + a link that routes **into OSLO** | the memo becomes a **file or a hosted copy** the PM handles themselves — it leaves OSLO |
| **Recipient** | the people | the PM |
| **Both** | **produce a MEMO** — frozen, dated, cover, disclaimer (D168) · **run NO analysis** (D146) · **append a History event** (D169) |

**Binding:**
1. **Add SHARE/SEND to the readout toolbar**, alongside Export.
2. **Both freeze a MEMO.** One code path (`_mkMemo`) — a memo is a memo however it travelled; **`sent_via` records which.**
3. ⛔ **SHARE IS FREE ON EVERY TIER.** **CHG-061 — sharing is a viral primitive; the seed is never gated.** *(Export **formats** are tier-bound: Free = PDF. **Sharing is not.**)*
4. **A shared memo is read-only to its recipients**, carries its cover, disclaimer and currency marker, and is **relabelled "previous analysis"** when the read moves on — **never silently refreshed.**
5. **History records how it travelled** — sent, or exported.

---

# D172 — A scheduled readout is an automated SHARE. And the workspace is "Reports". (owner: approved, 2026-07-12)

**D172a — Scheduling is an automated SHARE, not an automated export.** Closes O-D171-2.
**Nobody schedules a PDF onto their own disk.** What a PM wants is *"send my sponsor the readout every Friday"* — it goes **to people**. That is a **share**, by definition.
- `sent_via = 'shared'` for scheduled sends · History records **sent** · **D169 opens the frozen memo** · the **D147 currency re-check still binds** — *a scheduled share must NEVER quietly ship a stale read as current.*

**D172b — THE TIER RULE: the share is free; the AUTOMATION is Basic.**
> **You can always send the readout — manually, to anyone, on any tier, as often as you like. What Basic sells is NOT HAVING TO REMEMBER.**
**Same shape as D154** (*editing is free; **persistence** is the gate*). It is the legitimate lever category: **meter the labour, never the understanding.**
**It does NOT breach CHG-061.** Sharing is guaranteed on Free as a **viral primitive** — **cron is not a viral primitive.** The **seed of the loop** — a human choosing to put a memo in front of an executive — stays **completely ungated**. Automating it is a convenience.
*Say-it-out-loud test: "Basic sends it for you every Friday." Passes.*

**D172c — A shared memo is a SCOPED, TOKEN-GRANTED, READ-ONLY view — the same mechanism as the CRR reviewer grant** (DL-102 constituent A). **The link IS the invite, and the invite IS the authentication.** No signup wall; no anonymity problem (DL-021 holds).
**Consequence:** the shared memo is **the best viral surface in the product, arriving on a schedule, in front of budget holders** — the passive loop, aimed **upward**, automated. *That is a better argument for Basic than anything on the Plans page.*

**D172d — Naming (closes half of R-O1).** The **workspace is "Reports"**; the document inside it is the **"Readout"**.
**Reports will host multiple report types over time; the Readout is the first.** Structure the code so **a second report type is an ADDITION, not a rebuild.**
⛔ **Do NOT build speculative UI for reports that do not exist.** *That is exactly how the six-card scaffold happened the first time.* **D143 stands:** the six "report types" it killed were **sections of one memo**, not reports — and they stay dead.

---

# D173 — THE PAYOFF: numbers that are TRUE. (owner-directed, 2026-07-12)

**The owner's point stands: humans need quantifiable values to comprehend efficiently.** The discipline was never *"no numbers"* — it is **"the number must be TRUE."** OSLO is not short of numbers. It is short of **honest** ones.

**D173a — THE INCOHERENCE (found, not invented).**
**D056 (ratified): "direction-only — never a fabricated magnitude."**
**The product renders `62/100` in a 52-pixel hero.** It was `58`. **The user does the subtraction.** The magnitude is already communicated — the product is merely **coy about arithmetic the user can do in a second.**
**And DL-062 says numeric calibration is Open-TBD (F1). The index is NOT CALIBRATED.**
> **OSLO is displaying a 52px uncalibrated number as though it were a measurement — on the one signal the entire product rests on.** That is **false precision**, and it invites exactly the score-gaming the doctrine exists to prevent. OSLO cannot defend **62** against **63**.

**D173b — THE PAYOFF: band transition + true counts + consequence.** Build all three.
1. **The BAND TRANSITION is the headline event.** *"Feasibility: **Very Low → Low**."* **Discrete. Earned. Visible.** An **ordinal scale is still a scale**, and crossing a band is a real event in a way 58→62 is not. (5-band scale, DL-086/098.)
2. **TRUE COUNTS alongside it** — numbers OSLO knows **exactly**: *Issues 12 → 11 (critical 4 → 3)* · *Unvalidated assumptions 5 → 4* · *Evidence coverage 3 of 7 artifacts → 4 of 7* · *Dependencies confirmed 5 of 8 → 6 of 8*. **Hard. Countable. True. And they move when the user acts.**
3. **THE CONSEQUENCE** — what changed **about the plan**, and **what is now the limit**: *"That was the one thing holding Feasibility back. **Resourcing is now the weak point.**"*

**Model payoff:**
> **You confirmed the Wi-Fi capacity.**
> **Feasibility: Very Low → Low.** That was the one thing holding it back.
> **Unvalidated assumptions: 5 → 4. Critical issues: 4 → 3.**
> **Resourcing is now the weak point.**
**Numeric. Vivid. Every number in it TRUE.**

**D173c — A FALL MUST BE AS LEGIBLE AS A RISE. (Binding — this is the one that protects the product.)**
**The read can legitimately FALL when the user improves the plan** — better understanding reveals weakness that was always there. **If score movement is made celebratory, a FALL becomes a PUNISHMENT** — and the product would be **training users to avoid the actions that teach them the most** (answering a hard clarification, surfacing an ugly dependency). **That is the one behaviour OSLO cannot afford to create.**
**A fall is stated plainly and without alarm:** *"Your read fell — because you learned something. That is the system working."*

**D173d — The 0–100 index: OWNER DECISION (packet).** Two honest options, and only two:
- **CALIBRATE it** (DL-062 **F1** is open — this is the work). If **62** means something defensible, show it **and its delta** proudly.
- **DEMOTE it** — lead with the **band** and the **counts**; keep the index as a **secondary aggregate**, not the hero.
**Recommendation: DEMOTE now, CALIBRATE later.** The honest version ships today, and **the number gets its hero slot back the day it earns it.**

# D174 — THE OVERVIEW HERO IS THE MATURITY RAMP. (owner, 2026-07-12)

**D173d demoted the 0–100 index and left a single word in 40px. That is not a hero — it is a label.** The hero's substance was removed and nothing replaced it. **Owner: *"the image is inadequate for an overview hero."*** Correct.

**The replacement was already in canon, undrawn.** **D003 mandates a NEUTRAL MATURITY RAMP** (*"neutral maturity ramp vs severity-only red/amber/green"*). **We never drew the ramp.**

**Confidence IS understanding maturity — five ordinal steps.** So **draw the position on the ramp:**
> **Very Low · Low · [ MODERATE ] · High · Very High**

**Why this is the right hero:**
- **It has visual mass** and is legible at a glance.
- **It shows how far along you are, and what the next rung is** — motivating **without being a score**.
- **It is ORDINAL, therefore defensible.** No fabricated precision. (Contrast: the 0–100 index is uncalibrated — DL-062 F1.)
- **It is what the doctrine already asked for** (D003) and was never built.

**The hero carries the things that give the position MEANING:**
1. **The ramp** — position among the five bands (DL-086/098). The band word is the lit step.
2. **The reliability qualifier** — *"on moderate reliability."*
3. **The limiter** — *"Feasibility is holding it back."*
4. **The direction** — with its **named cause** (D056: direction + cause, never a magnitude).
5. **The 0–100 index** — **secondary, small.** No delta. Calibration flag stays in the notes layer (D161), never in product copy.

**Binding:** **NEUTRAL — a rise is not green, a fall is not red** (D003). **The ramp is a maturity scale, not a health bar.** Every element computed from state (D173).

**D175 — Neutralise the Provisional/Current chip (owner: approved, 2026-07-12).** Closes O-D174-1. Amends D040.
`.ustate.prov` = `--warning` (amber) and `.ustate.cur` = `--success` (green), **sitting inside the confidence hero card**.
Each is *technically* honest — it describes the **analysis state**, not the project. **But amber-and-green one line above a five-step maturity ramp is exactly the adjacency a reader turns into RAG.** That is the **P1 health-framing class (DL-104 §5)** arriving through a side door: **not from what either element says, but from what they say TOGETHER.**
**Fix: neutralise it.** Provisional/Current is a **STATE**, not a **JUDGMENT** — a dot and a word carry it. **The only thing amber and green buy is the one misreading the whole doctrine exists to prevent.**
**Binding:** the D003 colour allowlist that governs the ramp now governs **the whole hero card** — **no severity/health tokens anywhere in it.** Guard by cascade read, and **extend the guard's scope to the card, not just the confidence focus.**

**D176 — Neutralise the CAF limiter row; and the CAF bars are false precision (owner: approved, 2026-07-12).** Closes O-D175-1 and O-D175-2.

**D176a — The limiter row loses brand orange.** `--primary` is not a severity token, so D175's rule did not reach it — **but D174's own reasoning does**: it banned `--primary` from the ramp *precisely because an amber-adjacent orange invites "amber = at risk."* The row sits **three lines under the ramp, inside the same card.**
> **The limiter is a FACT — *"Feasibility is holding it back"* — not a WARNING.** It needs **emphasis**, and **weight gives emphasis**. **Orange gives it a temperature it has not earned**, directly beneath a scale two decisions were spent making neutral.
**Binding:** the hero card's colour allowlist now excludes **`--primary`** as well. **Emphasis by weight, never by hue.**

**D176b — The popover's CAF bars are PERCENTAGE FILLS — the same false precision as the 0–100 index, in a different costume.**
A bar filled to 55% asserts a **cardinal magnitude** OSLO cannot defend, on the same uncalibrated scale (**DL-062 F1**). It is worse than the index, because **a filled bar reads as a measurement without even showing its number** — and a partial fill is the visual grammar of a **progress/health bar** (**DL-104 §5**).
**Fix: the CAF dimensions are BANDS, not percentages.** Show each dimension on **the same five-step ordinal ramp** as the hero (Very Low · Low · Moderate · High · Very High), with the limiter marked. **No percentage fill anywhere on a maturity surface.**
**Severity colour remains on ISSUES only (D003)** — the Attention heat map is **correct as-is**, because those cells *are* issues.

---

# D177 — The Extended Analysis payoff is HOLLOW, and the fix is the best demo in the product (owner, 2026-07-12)

**Owner: the "What changed" panel is incomplete.** Correct. It shows the band transition and the limiter — **and no counts.**

**The payoff machinery is CORRECT.** `_readSnapshot()` captures the counts; `renderPayoff()` emits band + counts + consequence; a count that did not move is **omitted** (right — *"Issues 6 → 6"* is noise, and D173 forbids fabricating a delta).

**The DEMO DATA is the defect.** The Extended pass says *"deeper analysis firmed the read"* — **and not one number moves.** **The narrative claims something happened; the counts say nothing did.** That is the hollowness. It is a **data** problem, not a code problem.

**A real Deep Pass MOVES COUNTS.** It re-reads the same evidence more thoroughly: it **finds issues the Fast Pass had no budget to find**, and it **firms the assessment**.

**D177a — Build it, and it becomes the best demonstration of the doctrine in the product:**
> **Extended Analysis landed.**
> **Feasibility: Very Low → Low.**
> **Issues: 6 → 8. Critical: 1 → 2.**
> *I looked deeper and found two more. The read is firmer because I know more.*
> **Feasibility is still the limit.**

> ## **MORE ISSUES *AND* HIGHER CONFIDENCE.**
> **That is not a contradiction — it is the point.** It is the clearest possible illustration that **confidence is understanding maturity, NOT project health**, and **no other moment in the product makes that case so plainly.**

**Binding:**
- The Extended pass must **surface issues it did not have the budget to find** (counts move **up**) **and** firm the read (band moves **up**). **Both, in the same payoff.**
- **The payoff must say so in plain language** — *"I looked deeper and found two more. The read is firmer because I know more."* **Never apologetic, never alarmed** (D003/D173c: a rise is not green, a fall is not red).
- It invents **no new evidence** — a Deep Pass re-reads the **same** inputs more thoroughly. **No fabricated facts.**
- **Every count still computed from state** (D173). **Word budget ≤45** (D163).

**D178 — A Deep Pass ASKS, it does not only FIND (owner: approved, 2026-07-12).** Closes O-D177-2.
A deeper read that spots a **funding-vs-commitment gap** should **ask about the sponsor floor** — not merely flag it. **Finding an issue and knowing what would close it are different acts, and OSLO can do both.**
- **The Extended pass raises at least one CLARIFICATION REQUEST** alongside its findings — bound to the issue it would close, and to real evidence.
- **It moves a third true count:** *Open questions 2 → 3* — computed from state (D173), never fabricated.
- **The clarification is the honest form of the ask:** OSLO does not know the answer, and says so. Answering it closes the gap through an **analysis update** — never by hand (advisory-only).
**The payoff then carries the full shape of a deeper read:** *it firmed the read · it found more · **and it knows what it still needs to ask**.*

---

# D179 — Overview layout: STATE outranks EVENT. Counts have ONE home. Colour without RAG. (owner, 2026-07-12)

**Four owner findings, all correct. Three are my drift.**

**D179a — THE STATE ALWAYS OUTRANKS THE EVENT.** The payoff panel was placed **above** the Confidence hero, pushing it down the page. **"What changed" is EPISODIC** — true for one moment after an analysis lands. **Confidence is PERMANENT.** **An event must never outrank state in the layout.**
**Fix: Confidence is the top panel. Always.**

**D179b — The payoff is NOT a panel. It is a DELTA ON THE CONFIDENCE CARD.** It presented as a standing surface, *"as if it is always relevant to the audience."* It is not.
**Fix:** it renders **on/under the hero**, **dismissible**, and **gone by the next visit**. It never displaces the state.

**D179c — Make it VISUAL, not textual.** It is a paragraph doing a picture's job.
**Fix — show the movement ON THE RAMP itself:** the **previous position ghosted**, the **current lit**, an arrow between them.
> Very Low · ~~Low~~ ⟶ **[ Moderate ]** · High · Very High
**Zero reading.** Then the **count deltas as chips** (they already work). Then **ONE** short line — not five.

**D179d — COLOURLESS WAS AN OVER-CORRECTION. Neutral ≠ monochrome.**
The intent was **remove SEVERITY colour, not ALL colour** (D003/D175/D176). Then `--primary` was banned from the hero card too — stripping everything, leaving it grey and dead.
> **The awkward truth: OSLO's brand colour is ORANGE. Orange reads as AMBER. Amber reads as "AT RISK."** That is a real **brand-vs-doctrine collision** on any maturity surface.
**Fix:** introduce a **COOL ACCENT (blue/violet)** for emphasis on maturity surfaces — **blue is not in the RAG vocabulary and cannot be misread as health.** **Reserve brand orange for ACTIONS and LINKS only — never for STATE.** Life without the misread.

**D179e — COUNTS HAVE ONE HOME. (The sharpest finding.)**
**"What changed" and "Progress" show the same numbers twice** — one as a delta, one as an absolute. **That is the overlap.**
**Fix: counts live in PROGRESS, with the delta annotated:**
> Issues **8** ↑2 · Critical **2** ↑1 · Open questions **3** ↑1 · Artifacts read **7/7**
**"What changed" then keeps ONLY what Progress cannot say: the BAND MOVEMENT and the ONE-LINE REASON.**
*(Progress was also tracking the wrong things — it carried a hard-coded "5 of 7 artifacts well-evidenced" that nothing computed. Already removed. **Every Progress count must be computed from state (D173); one that cannot be computed is not shown.**)*

**Resulting layout: HERO (state) → PAYOFF STRIP (the event — dismissible, movement shown on the ramp) → PROGRESS (the counts, one home, deltas annotated).**

---

# D180 — PROGRESS IS GROUNDING, NOT CLEARING. (owner: approved, 2026-07-12)

**Progress toward WHAT?** Not project completion — that is forbidden. **Progress in UNDERSTANDING.**

> ## ⛔ **PROGRESS IS NOT A BURNDOWN.**
> **If it looks like *issues → 0*, you have rebuilt a project-health tracker under a different name** — and the doctrine leaks out through the one panel nobody was watching.
> **Progress is GROUNDING, not CLEARING.**

**D180a — Three rows. All computed from state (D173). A count that cannot be computed is not shown.**

**1. GROUNDED — *"2 of 7 artifacts rest on your evidence."*  ← THE STAR.**
The **only** number that says **how much of this read is REAL versus INFERRED.** It is **the product's entire epistemic claim, made countable** — *derived vs attested*, in one line. It **rises as the user confirms artifacts, edits them, and answers clarifications.** **It IS the progress narrative.**

**2. OPEN — *8 issues · 2 critical · 3 questions.*** What is outstanding.

**3. CLOSED — *0 issues resolved · 1 question answered.*** What the user's work actually landed. *(Closes O-D179-3: **resolved is the one number that tells a PM their work worked** — but it sits under **Closed**, never as a target to drive to zero.)*

**D180b — KILL "Artifacts read 7/7" (closes O-D179-1).**
**OSLO always reads all seven. It is a CONSTANT, not progress.** It was hard-coded *because* it was meaningless — **a number that can never move is not information, it is decoration.** *"Read"* is not the interesting question. ***"Grounded in evidence"* is.**

**D180c — The property this preserves (and it is the point).**
As the user works: **they ground more artifacts → reliability rises → confidence rises. And issues may rise too, because grounding reveals things.**
> **Progress goes UP while the issue count goes UP. That is not a bug — it is the same lesson as the Extended-pass payoff (D177), showing up in a second place.**
> **You cannot game GROUNDING. You can only game a BURNDOWN.**

---

# D181 — "Load-bearing" = THE READ POINTS AT IT. And age the clock, not the past. (owner, 2026-07-13)

**D181a — LOAD-BEARING: reject both candidate definitions. (Closes O-DL109-3.)**
- **Loose** (`item.dim === limiting`) → **11.** **Over-counts** — it includes inferences that **nothing actually rests on**. A shrug, not a finding.
- **Strict** (*supports an open issue on the limiting dimension*) → **4.** **Under-counts, and has a fatal blind spot:** it would say **SCOPE's inferences are NOT load-bearing** — because Scope has **no critical issues open**. **But Scope is the artifact the Inference Map flagged as the most dangerous thing in the plan.** **The strict definition misses FALSE CONFIDENCE entirely — the exact case the feature exists to catch.**

> ## **An inference is LOAD-BEARING if the read would CHANGE were it false.**
> Operationally: **the read POINTS AT IT** —
> **(a)** a **critical issue** cites it · **(b)** the **limiting dimension's** assessment rests on it · **(c)** ⭐ **a STRONG-READING artifact's confidence rests on it.**

**Clause (c) is the one that matters and is non-negotiable.** **An inference is load-bearing in two ways: it supports a WARNING, or it supports a REASSURANCE.** **The reassurance case is MORE dangerous, because nobody is looking at it.** *Scope reads fine **because of** four things OSLO made up.*
**Items nothing points at are inferences — but they are not holding anything up.** The number is then **honest, actionable, and it INCLUDES Scope.**

**D181b — AGE THE CLOCK, NOT THE PAST. (Closes O-DL109-1.)**
**Ageing the demo project buys a static screenshot and costs a true thing.** The project **genuinely is new** — everything is minutes old — and **Slice 7's D100 first-run state assumes exactly that.** A three-week history on a first-run project is **a small lie told to make a surface look better**, which is precisely what the build refused to do (*"OSLO does not invent a longer past to make a surface look better."*).

**Use the mechanism that already exists: `simNextWeek()`.** **Advancing a week AGES the assumptions** — the viewer *watches* *"raised today"* become *"unvalidated for 3 weeks · 3 issues now depend on it."*
> **Demonstrate ageing; do not assert it.** **A number you watch climb argues better than a label that asserts.**
*(If a still frame is ever needed for a deck, ageing the project is acceptable — but knowingly, and with the D100 cost on the record.)*

---

# D182 — P1 DEFECT: the GUARDS are firing real prompts at the user. (owner-reported, 2026-07-13)

**Owner: an upgrade prompt appears "without any specified user-derived event/trigger having occurred."** **Reproduced. It is the test scaffolding leaking into the product.**

**Root cause.** The negative controls **monkeypatch `window.sendMemo` and `window._rptCommit`** to call `fireUP('UP-REPORT')` — in order to prove the guard bites. **`_rptCommit` is the readout's AUTOSAVE path.** `simNextWeek()` (D181b's ageing clock) **also** fires `UP-REPORT`. **So a probe reaches into the live product and SELLS TO THE USER with no user intent.**

> ## ⛔ **A PROBE MUST NEVER BE ABLE TO TOUCH THE USER.**
> **This is the THIRD leak of the same class:** a probe **retired a live chat answer box** the user was typing into · a probe **corrupted the append-only History** · and now a probe **fires an upgrade prompt at a user who did nothing.**
> **A guard that damages the product it protects is worse than no guard** — and this one *sells* to the user.

**Binding:**
1. **Sandbox every user-facing effect while a guard or probe runs** — prompts, chat, History, notifications, toasts. Use the established `_CHAT_PROBE` pattern; generalize it to **one probe fence** (`_PROBE`).
2. **A prompt may fire ONLY from a real user attempt** (D138/D170 — the affordance stays enabled; the *attempt* is gated; the prompt names the limit).
3. **Guard it:** a mechanism proof that **no prompt can be raised while a probe is active**, and that **every guard restores every byte it touched**.

---

# D183 — Copy and positioning (owner, 2026-07-13)

**D183a — OSLO says "I" ONLY in chat.** Everywhere else it is **"OSLO"**.
> *"I looked deeper: found two more…"* → **"OSLO looked deeper: found two more, and one more question. The read is firmer."**
Chat is a conversation; a panel is not. **First person is a voice, not a default.**

**D183b — ⭐ It is OUTCOME CONFIDENCE. (Positioning — and canon already says so.)**
The data model's entity is **`ConfidenceState` — "Per-run **Outcome Confidence** snapshot."** **Canon already calls it Outcome Confidence; the product just says "Confidence."** That is **both a positioning loss and canon drift** — and association with **Outcomes** is central to the category (Outcome Orchestration).
> ⛔ **BUT THE LABEL MAKES THE NUMBER DANGEROUS.** *"Outcome Confidence **62/100**"* reads as ***"62% likely to hit your outcome"*** — **the forecast the doctrine forbids, arriving through the label.**
> **The ramp does not have this problem:** *"Outcome Confidence: **Moderate**"* on a five-step ordinal scale **cannot** be read as a probability.
**Therefore: adopt "Outcome Confidence" — and DELETE the 0–100 index.** The label wins the category; the number would hand back the misread. *(This closes the D173d/DL-062-F1 "calibrate or demote" question: **delete**. It may return the day it is calibrated AND the forecast misread is closed.)*

**D183c — Confidence and Reliability must not share a vocabulary.**
*"Confidence 62 MODERATE | Moderate reliability"* — **two different things wearing the same word.** The pill reads like a stutter and the user cannot tell them apart.
**Reliability speaks in GROUNDING language, not band language** — because that is what it **is** (Coverage · Evidence · Assessability), and the provenance work now lets it say so plainly:
> **Outcome Confidence: Moderate** · *thinly grounded*
> **Outcome Confidence: High** · *well grounded*
**Confidence says how MATURE the read is. Grounding says how much of it is REAL.** Ties directly to the Inference Map.

**D183d — "things" → "inferences".** *"20 inferences are holding up your plan."* **Precise, short, and it teaches the word the whole feature rests on.** *"Things" is vague at exactly the moment precision is the point.*

**D183e — Plan artifacts are called DOCUMENTS in the application.** *(User-facing copy only.)* Supersedes **D049**'s user-facing term. **Canonical/internal entity remains `Artifact`** — the same split DL-095 made for *Finding* (canonical) vs *Issue* (user-facing). **Sweep every user-facing surface.**

**D183f — The trend line's cause text is deleted.** *"— deeper analysis firmed the read (Feasibility rose Very Low → Low)"* is **badly formatted and duplicates "What changed."** **The trend line shows the sparkline + the direction word. The CAUSE belongs in "What changed", and nowhere else.** *(Counts have one home — D179e — and so do causes.)*

**D183g — Overview order is USER-STATE dependent.** **"Start here" is GUIDANCE; Progress is STATE.**
- **First run** → **Start here first** (there is no progress to read).
- **After activation** → **Progress first** (the user knows what to do; they want to know where they stand).
Same principle as D179 (state outranks event), applied to the user's own maturity.

---

# D184 — P1: "Apply this fix" does not show the fix. (owner, 2026-07-13)

**Owner: *"Issues panel lists an 'Apply this fix' button, but it doesn't display the fix/recommendation it applies to. How would the user know what fix is to be applied?"***

**They wouldn't. And it is worse than it looks: there are THREE recommendations, collapsed, BELOW the button.** So the button does not even identify **which** one it applies.

> ## ⛔ **A FIX THE USER CANNOT READ IS A FIX THEY CANNOT CONSENT TO.**
> **OSLO is ADVISORY-ONLY (D001).** Advice the user cannot see is not advice — **it is an instruction.** The moment the product asks *"apply?"* about a change it has not shown, **it has stopped advising and started acting.** This is the doctrine's line, drawn in a button.

**Binding:**
1. **The primary recommendation is VISIBLE, in the button's own block, before the button.** *What OSLO would change, in the user's words.* **The button never floats above a closed drawer.**
2. **The button NAMES its subject** — not *"Apply this fix"* (which fix?) but a label bound to the change shown directly above it.
3. **If there is more than one recommendation, the button applies the one on screen and the others are one tap away.** *(Rank: the recommendation that moves the limiting dimension.)*
4. **A recommendation that cannot be rendered ⇒ NO BUTTON.** *(D173's rule, applied to actions: an action whose subject is absent is not degraded — it is removed.)*
5. **Guard:** *no apply-affordance may render without its recommendation text visible in the same block.* **Negative control:** hide the recommendation → the guard goes RED.

---

# D185 — The Confidence popover: obey the doctrine, don't narrate it. (owner, 2026-07-13)

**Owner: *"revisit this design… optimize for scanability and readability… should not be cognitively heavy."*** **Correct — and it is DL-107 all over again, in the most-opened panel in the product.**

**What is actually on that surface: THREE separate paragraphs, each justifying the row above it.**
- *"Understanding maturity — not health, readiness, or probability."*
- *"It is a fact about the read, not a warning about the project."*
- *"Determined independently of Clarity · Alignment · Feasibility — it reflects the evidence behind the read, not the plan's integrity, and can rise as evidence improves."*

> ## **The doctrine is a CONSTRAINT ON WHAT THE PRODUCT MAY CLAIM. It is not a SCRIPT the product must recite.**
> **The user opened this to read a state. They got a lecture.** The panel is ~90 words of prose defending itself and **~10 words of information.** *If the design is honest, it does not need to say so.*

**Binding — the popover is a READOUT, not an essay:**
1. **≤ 25 words of prose in the entire popover.** *(D163 budgets, applied here.)* The three self-justifying paragraphs are **deleted**, not shortened.
2. **Every explanation moves BEHIND the ⓘ affordance — on demand, never resident** (DL-107 / D159). **The info icon already exists.** *Use it.*
3. **The panel's job, in order:** (a) **the state** — Outcome Confidence + grounding · (b) **the three dimensions**, scannable · (c) **the limiter, named in ≤ 8 words** · (d) **one way out.** Nothing else.
4. **The limiter needs a VERB, not an apology.** *"Feasibility is holding it back — the lowest of the three. It is a fact about the read, not a warning about the project."* → **"Feasibility — the lowest. Ground it to lift the read."** *(A limiter the user cannot act on is trivia.)*
5. **Reliability basis:** three rows all reading *"Moderate"* is a **table with no information in it.** Show **what is thin**, not that everything is average. *(Rank; surface the weakest; the rest on demand.)*
6. **One vocabulary per concept** (D183c — already landed): Confidence uses the band; grounding uses grounding words. **Never both wearing "Moderate".**
7. **Scanability is a MECHANISM, not a taste:** the eye must land on **the state** first. **Guard: the popover's prose word-count, and the count of resident explanatory sentences (target: ZERO).**

**This is the same lesson as DL-107, and it has now cost us twice.** **Add it to the standing sweep: any surface that explains why it is trustworthy is not.**

---

# D186 — "Holding it up" dies. It means the OPPOSITE of what the owner read. (2026-07-13)

**Owner: *"Replace 'Holding It Up' label/copy with 'Blocker'."*** **The directive rests on a misreading — and the misreading IS the defect.**

**The phrase is used in two places with OPPOSITE meanings:**
- *"Feasibility is holding it **back**"* — the CAF limiter. **Obstructing.**
- *"20 inferences are holding it **up**"* — the load-bearing count (D181). ***SUPPORTING.*** **These are what the read RESTS ON.**

> ## ⛔ **Renaming the load-bearing row "Blocker" would tell the user to REMOVE THE THING CARRYING THEIR PLAN.**
> **The owner — who wrote the doctrine — read "holding it up" as "delaying it."** If *he* misreads it, **every user will.** **"Hold up" is ambiguous in English (support / delay) and it is sitting on the single most valuable number in the product.**

**D186a — the load-bearing label becomes "YOUR READ RESTS ON."** Unambiguous, plain, and it names the actual relationship. *(Not "Blocker" — inverted. Not "Load-bearing" — internal vocabulary.)*
**D186b — the copy: "20 inferences your read rests on."** *(Carries D183d: "inferences," never "things.")*
**D186c — the CAF limiter stays a LIMITER, not a "Blocker" — pending owner override.**
> **"Feasibility is a Blocker" reads as "the PROJECT is blocked."** But low Feasibility means **OSLO's READ of feasibility is immature** — **a fact about the read, not a warning about the plan (D003).** *"Blocker" imports the health/readiness framing the doctrine forbids, in the panel most likely to be screenshotted into a status deck.*
> **Recommended: "Feasibility — the lowest. Ground it to lift the read."** **ESCALATED: the owner may override; it will not be done silently.**

---

# D187 — Trend colour: GREEN where the user earned it. NEVER red. (owner, 2026-07-13)

**Owner: *"some of the trend arrows can legitimately be viewed as positive or negative. In those instances, can't we use Red or Green to reflect that truth?"*** **Half right — and the other half is the trap.**

> ## ⛔ **"Issues 8 ↑2" AFTER AN EXTENDED ANALYSIS DOES NOT MEAN THE PLAN GOT WORSE. IT MEANS OSLO LOOKED HARDER.**
> **Red would tell the user their plan degraded at the exact moment it was finally SEEN — punishing them for OSLO's own improvement.** Same for *inferences ↑* (**D177**: a rising inference count is NOT a regression) and *critical ↑* (a critical issue found is a critical issue **avoided**).
> **In this panel, a rising count is EVIDENCE OF BETTER SEEING as often as it is bad news — and the product cannot tell which from the number alone. A colour that cannot know is a colour that lies.**

**BINDING:**
1. **GREEN — and only green — on counts that CANNOT MOVE EXCEPT BY THE USER'S OWN WORK:** **you grounded · issues resolved · questions answered.** These have a **fixed valence**; nothing but the user's action moves them. **That green is honest, and it is earned.**
2. **NO RED. ANYWHERE. In this panel.** **Nothing here rising is unambiguously bad.**
3. **Everything else stays NEUTRAL** (D003 ramp) — **and the CAUSE lives in "What changed" and nowhere else** (D179e / D183f).
4. **Test, not taste:** *"Could this count rise for a reason that is GOOD?"* **If yes → no colour.** Severity colour remains **ISSUES-ONLY** (D003) — a count of issues is not an issue.
5. **Guard:** the valence table is **declared and computed**; a count with a "green" flag must be **provably user-driven**. **NC:** flag a count OSLO can move by itself → **RED**.

---

# D188 — The Structure panel: labels, not sentences. (owner, 2026-07-13)

**Owner: *"improve labeling, make more concise and scannable."*** **The panel has no labels — it has three captions.**
> *"**6** dependencies OSLO assumed, and nobody confirmed" · "**5** named parties with nobody accountable for them" · "**3** numbers in the plan that trace to nothing"*

**Each is a sentence doing a label's job.** The user must **read prose to find out what they are looking at.** *(And they are ~8 words each, three times, in a strip meant to be scanned in one pass.)*

**BINDING — a stat cell is `NUMBER · LABEL`, and the sentence goes behind the ⓘ:**
- **6** — **Unconfirmed dependencies**
- **5** — **Unowned parties**
- **3** — **Untraceable numbers**

**≤ 3 words per label. The vivid consequence is ONE TAP AWAY, not resident** (DL-107/D185). **The number carries the weight; the label names it; the ⓘ explains it.** *The consequence was the right instinct — it is in the wrong place.*

---

# D189 — Kill "A direction, not a target." (owner, 2026-07-13)

**Owner: *"'A direction, not a target' is not required here. You are attempting to communicate guidelines/philosophy."*** **Correct. DELETE.**

**This is DL-107 for the THIRD time.** The product keeps **narrating its own epistemics as a caption**. **Nobody reads a subheading and forms a belief about targets — they read the number.** *If it were a target, the panel would say "goal." It doesn't. That is the whole protection.*

**Also on this panel (already binding, not yet applied here):**
- *"I inferred"* → **"OSLO inferred"** — **D183a: first person ONLY in chat.** *(This is the Progress panel, not chat.)*
- *"20 things I inferred"* → **"20 inferences"** — **D183d.**

**Standing sweep, now mandatory:** **any caption whose job is to pre-empt a misreading is DELETED and moved behind the ⓘ.** *A surface that explains why it is trustworthy is not.*

---

# D190 — Issue panel: the recommendation block. (owner, 2026-07-13)

**D190a — the button says "Apply this fix." Nothing more.**
**This CORRECTS my own D184 clause 2.** I required the button to **name its subject** — written when the recommendation was *invisible*. **Once the recommendation is resident directly above it (D184 clause 1), the button repeating it is redundant** — and it produced *"Apply: Confirm the venue's 500-person Wi-Fi capacity…"*: **too long to scan, truncated before it can be read.** *The worst of both.*
> **The rule was always: THE USER MUST BE ABLE TO READ THE FIX BEFORE CONSENTING.** Clause 1 satisfies it completely. **Clause 2 was belt-and-braces that ate the belt.**
**Binding: the affordance is short and constant; the fix above it is the subject.** **D184's guard stands unchanged** (no apply-affordance without its recommendation visible in the same block) — **it never required the label to carry the text.**

**D190b — "Other paths" → "Other options."** *Owner's term. "Path" is jargon dressed as plain English.*

**D190c — the options belong UNDER the recommendation, not under Evidence.**
Currently **"Other options (2)" exists TWICE** — a button in the recommendation block **and** a disclosure row below Evidence. **The user is offered the same door in two places, in two different registers.**
**Binding: ONE home** (D179e, applied to actions). **The options expand IN PLACE, directly beneath the recommendation they are alternatives to.** **The disclosure row under Evidence is deleted.**
*The alternatives to a recommendation are part of the decision, not part of the record. Evidence is the record.* **Guard: no affordance opens the same set from two places.**

---

# D191 — P1: a fix, once applied, CANNOT BE UNDONE — and it attests the document in your name. (owner, 2026-07-13)

**Owner: *"can decisions such as fix selection be undone?"*** **No. And the code shows why that is worse than a missing button.**

```js
function applyFix(id){ …
  ps.basis = 'attested';                       // ← "CONFIRMED BY YOU"
  if(ps.rel==='Low') ps.rel='Moderate';        // ← Reliability RISES
  _istatus[id]='addressed';                    // ← one-way
```
`selectPath()` moves **Open → Addressed** with no way back. `applyFix()` **marks the document "Confirmed by you" and raises Reliability** — **and there is no path out of either.**

> ## ⛔ **"CONFIRMED BY YOU" IS THE USER'S WORD. AN ATTESTATION THAT CANNOT BE WITHDRAWN IS A CLAIM OSLO HOLDS THE USER TO AFTER THEY HAVE DISAVOWED IT.**
> **Reliability is computed FROM attestation.** So an un-withdrawable attestation means **the read rests on a confirmation the user no longer stands behind.** **This is not a UX gap. It is a TRUTH DEFECT.**
>
> ## ⛔ **AND IT CUTS AT D001.** **Advisory-only means the human can always change their mind.** **A product that gives advice but makes ACCEPTING it irreversible has converted advice into COMMITMENT.**

**BINDING — four things, and they are NOT the same thing:**

| Object | Undoable? | Why |
|---|---|---|
| **The SELECTION** (which option you are pursuing) | **YES — freely, including back to NO selection.** | It is an **intention**, not an act. Nothing in the plan changed. **Open ⇄ Addressed is not a ratchet.** |
| **The APPLIED EDIT + the ATTESTATION** | **YES — and ALWAYS TOGETHER.** | It is **your document and your word.** ⛔ **They may NEVER be undone separately** — an edit withdrawn while the attestation stands would leave OSLO asserting *"confirmed by you"* about **text that is no longer there.** |
| **The READ** | **NO.** | **Only an analysis update moves the read.** Doctrine. **Withdrawing a fix does not restore the old assessment — it triggers a NEW one.** *(Last-good honesty holds in the interval; D098g.)* |
| **HISTORY** | **NO. ⛔ APPEND-ONLY.** | **An undo is a NEW EVENT, never an erasure.** *(D128: the epistemic record is never metered — and never rewritten.)* |

> ## **YOU CAN UNDO THE DECISION. YOU CANNOT UNDO THE FACT THAT YOU MADE IT.**
> History records *applied → withdrawn*, **because that is what happened.** **A record you can edit is not a record.**

**Implementation:**
1. **Withdraw is available wherever the decision is visible** — the issue panel, and the History row. **Named for what it does** (*"Withdraw this fix"* / *"Clear selection"*), **never "Undo"** — *"undo" implies the world returns to how it was, and the read does not.*
2. **Withdrawing an applied fix restores the document to its pre-fix version** (the version snapshot already exists — `_artVersion` / `_pushUndo`), **drops the attestation, restores the prior Reliability**, and **triggers an analysis update** — it does not roll the read back.
3. **It says so, in one line, before it acts:** *"This removes the change from \<document\> and withdraws your confirmation. OSLO will re-read the plan."* **Consent, not a surprise** — the same rule as D184.
4. **The issue returns to OPEN** (not "resolved," not "addressed") — *because it is.*
5. ⛔ **A RESOLVED issue is NOT withdrawable by hand.** Resolution came from **an analysis update**, not from the user — **and the user may not hand-move the read** (standing doctrine). **Withdraw the FIX; the read follows.**
6. **The assisted-apply meter is REFUNDED on withdrawal** — *(you cannot bill a user for labour you then took back)* — **and the refund is recorded.**
7. **Guards:** (a) no state transition into `addressed`/`attested` exists without an inverse; (b) **edit and attestation move as ONE unit** — NC: withdraw one without the other → **RED**; (c) **History NEVER shrinks** — NC: make a withdrawal delete its origin event → **RED**; (d) **no hand-path moves the read** — NC: let withdraw write a CAF band directly → **RED**.

---

# D192 — ERRATUM to D191 §5. My own clause reinstated the P1 it was written to kill. (2026-07-13)

**D191 §5 said: *"A RESOLVED issue is NOT withdrawable by hand."*** **It is WRONG, and the worker measured exactly how wrong:**
> **The analysis update resolves the issue ~1.9 SECONDS after the fix is applied.** So the withdraw affordance **lives for about two seconds** — and then the attestation (*"Confirmed by you"*, on the user's own document, **with Reliability raised**) **becomes permanent again.** **In the ordinary happy path, D191 does not hold.**

**The error: I conflated two objects.**
> ## **WITHDRAWING A FIX IS NOT HAND-MOVING THE READ.**
> It is **the user editing their own document and retracting their own word.** **The READ then moves BY ANALYSIS** — which **re-opens the issue, because the gap is genuinely back.** **D191's own sentence already said it: *"Withdraw the FIX; the read follows."*** §5 then contradicted it.

**D192a — BINDING: withdraw is available on a RESOLVED issue.** Drop the resolved clause. **What the user may never do is move the READ by hand — and they still cannot: withdrawal restores the document, drops the attestation, and TRIGGERS AN ANALYSIS UPDATE. The read is re-derived, never rolled back.** The status guard binds the **read**, not the **document**.

**D192b — O-D191-5: the lifecycle chevron still draws a ratchet that no longer exists.** `Open → Addressed → Resolved` with one-way arrows. **The states are now reversible. The diagram must stop lying.**

**D192c — O-D191-1: answering a clarification attests on the same two lines → it gets the same inverse.** Consistent. Approved.

---

# D193 — Two questions D191 exposed. Both answered from doctrine.

**D193a — O-D191-2: the user edits the document AFTER applying the fix, then withdraws.**
> ## ⛔ **OSLO MAY NEVER DELETE THE USER'S OWN WRITING.**
> Restoring the pre-fix version would **destroy every word the user wrote afterwards** — to undo a change *OSLO* made. **That is the tool overruling the human, with their own prose as the casualty.** *(The same line D152/D155 draw: the product does not police, and does not touch, the user's words.)*

**BINDING — the restore is CONDITIONAL on the document being untouched since the fix:**
- **Untouched since the fix** ⇒ **restore the pre-fix version** (clean; nothing of the user's is lost).
- **Edited since the fix** ⇒ ⛔ **DO NOT RESTORE.** **Withdraw the ATTESTATION only**, and **say so plainly**: *"Your edits since are kept. OSLO's change is still in \<document\> — remove it yourself if you want it gone."*
- **The attestation drops in BOTH cases** — *because the user's word is the user's to retract, regardless of what happened to the text.*
- **An analysis update runs in both cases.**
- **Guard:** **a withdrawal may NEVER reduce the user's authored content.** **NC: withdraw after a user edit and assert the edit SURVIVES → RED if it doesn't.**

**D193b — O-D191-3: two decisions attest ONE document.**
**The attestation is held by the DOCUMENT, but EARNED by decisions.** Withdrawing one decision while another still stands must **not** drop the document's attested basis — that would retract a confirmation the user **has not** retracted.
**BINDING: the attestation stands while ANY standing decision attests it; it drops only when the LAST one is withdrawn.** *(Refcount by decision, computed — never a boolean flipped by whoever moved last.)* **Guard + NC: withdraw one of two → the document stays attested; withdraw both → it drops.**

---

# D194 — The Progress rows: say it once, and say it in the ratified vocabulary. (owner, 2026-07-13)

**Owner proposed: *"AI Interpretation | Your Understanding = 13 Inferences ↓7"*.** **The instinct is right; two of the three words are already taken.**

**D194a — the LOAD-BEARING row says it TWICE.** Label *"YOUR READ RESTS ON"* + copy *"13 inferences **your read rests on**"*. **Straight D179e violation — one home.**
> **LABEL:** `YOUR READ RESTS ON` · **VALUE:** **13 inferences** ↓7 · *See them →*
**~60% less text. Nothing said twice.**

**D194b — ⛔ "Interpretation" and "Understanding" are BOTH already canonical, at different sizes. Rejected — with the owner's idea preserved.**
1. **`interpretation` is ONE of the six `ContextItem.item_type`s** (`claim · assumption · relationship · entity · metric · interpretation`). **Using it as the heading for ALL inferences makes the word mean two different-sized things** — precisely what the **DL-053 Disambiguation Register** exists to prevent.
2. ⛔ **"Understanding" is the most load-bearing word in the product.** **Confidence *IS* understanding maturity.** If *"Your Understanding"* comes to mean *"the claims you grounded,"* then **understanding** names **OSLO's assessment** AND **the user's evidence** on the same screen. **Drift, on day one, in the highest-value term we own.**
3. **The product never calls itself "AI." It calls itself OSLO.**

**D194c — the owner's ledger ALREADY EXISTS, one row up — and the ratified epistemic classes ARE the distinction he is reaching for.**
The GROUNDED row becomes:
> **From OSLO** 12 · **Confirmed by you** 17

**That is *"AI Interpretation / Your Understanding"* said in words canon already owns (D011/D069)** — **and it teaches the two class names the user meets everywhere else** (issues, documents, reports, the Inference Map).

**D194d — the two rows are NOT one ledger. Do not merge them.**
**GROUNDED** answers *"how much of this is inferred?"* — **a comparison.**
**LOAD-BEARING** answers *"how much of the READ is LEANING on it?"* — **a subset.**
**Merging them collapses a subset into a comparison and invites the user to read 13-vs-7 as a RATIO. It is not one.** *(The same error as putting a count and its cause in one home — D179e.)*

---

# D196 — "Stabilize" REJECTED. The VERB becomes "Confirm"; the STATE stays "grounded." (owner, 2026-07-13)

**Owner: *"instead of Ground or Grounding, what about replacing all copy with Stabilize or Stabilizing?"*** **Rejected — the underlying objection is right, the replacement is not.**

## ⛔ Why "stabilize" is the wrong word

**Grounding = attaching a claim to EVIDENCE. Stabilizing = reducing MOVEMENT. They come apart immediately:**
1. **A WELL-GROUNDED read can still move** — new evidence arrives, the plan changes, and it **should** move. **That is the product working.**
2. **An UNGROUNDED read is not unstable — it is UNSUPPORTED.** It may sit perfectly still for months while **resting on nothing.** ⛔ ***"Scope reads strong — but 8 of 11 items are inference"* is a PERFECTLY STABLE READ. Its STABILITY is what makes it DANGEROUS.** **"Stabilize" would name the wrong failure — and would call the false-confidence case a success.**
3. ⛔ **It makes STILLNESS the goal.** OSLO's line is ***"honest, revisable confidence."*** **Telling the user to *stabilize* the read reframes it as a SCORE TO LOCK IN** — the same gravitational pull as the forecast/health misread the doctrine spends its whole budget resisting.
4. **It breaks the metaphor family that is now load-bearing.** *"Your read **RESTS ON** 13 inferences"* (D186) → rests on → foundation → **ground.** One coherent picture. **"Stabilize" belongs to balance/wobble/equilibrium — and it has NO OPPOSITE.** **Grounded ↔ Inferred is the clean pair the entire provenance model teaches (DL-109). "Stabilized ↔ Inferred" is not an opposition at all.**

## ✅ But the objection underneath is CORRECT — "ground" reads as jargon to a PM. **Split the verb from the state.**

**D196a — the ACTION the user takes → "CONFIRM."**
> *"Ground it to lift the read"* → **"Confirm it to lift the read."**
> *"Ground Feasibility →"* → **"Confirm Feasibility →"**
**It is ALREADY RATIFIED: *"Confirmed by you"* is one of the three epistemic classes (D011/D069) and now sits in the Progress ledger (D194c).** **Plainer English, and it teaches a word the user meets on every other surface.** *(One vocabulary, everywhere.)*

**D196b — the STATE of the read → "GROUNDED" stays.** *thinly grounded · partly grounded · largely grounded · well grounded* (D183c).
**Nothing else means *"resting on evidence"* without colliding with something canon already owns:**
- ⛔ **"evidenced" collides with EVIDENCE**, which is **one of the three Reliability components** (Coverage · **Evidence availability** · Assessability) — **the same "two sizes of one word" error as *interpretation* (D194b).**
- **"Confirmed" cannot carry the state**: a read is grounded by **evidence** as well as by **confirmation** — *Attested by \<name\>* grounds it too, and **that is not the user confirming.**

> ## **THE USER CONFIRMS. THE READ IS GROUNDED.** **Verb and state, cleanly separated, both in words canon already owns.**

**D196c — the split must be MECHANICAL, not remembered.** **Guard: "ground/grounding" never appears as an IMPERATIVE addressed to the user; "confirm/confirmed" never appears as the RELIABILITY STATE band.** **NC both directions.**

---

# D197 — "LOAD-BEARING." I was wrong to reject it. (owner, 2026-07-13)

**Owner: *"'your read rests on this' is long, not concise, not intuitive. Establish a different name."*** **Agreed — and the right name is one I ruled out myself.**

**In D186 I rejected "load-bearing" as *"internal vocabulary."* That was wrong.**
> ## **A LOAD-BEARING WALL is the most intuitive metaphor in the language for *"remove this and the thing falls down."*** **Two words. Zero ambiguity — unlike *"holding it up"*, which the owner himself read backwards (D186). And it pairs exactly with *"rests on"*: the read RESTS ON its LOAD-BEARING inferences.**

**D197a — the term is LOAD-BEARING.**
- Progress row label: `YOUR READ RESTS ON` → **`LOAD-BEARING`**
- Value: *"13 inferences your read rests on"* → **"13 load-bearing inferences"**
- Assumption row marker: `YOUR READ RESTS ON THIS` → **`LOAD-BEARING`**
- **Register it in the glossary.** One name, everywhere.

---

# D198 — A MARKER, not a LABEL. The badge is wrecking its own row. (owner, 2026-07-13)

**Owner: *"certain notifications force the text on the row to be justified left or right… I'd prefer a more minimal indication that this row deserves attention."***

**Two offenders, one disease:**
1. **`YOUR READ RESTS ON THIS`** — a chip, repeated on **six consecutive rows**, ⛔ **and REDUNDANT WITH ITS OWN HEADER**: the section already says *"The ones your read rests on come first."* **THE SORT ORDER IS THE SIGNAL.** The chip re-states it six times and **shoves every row's content sideways.**
2. **`VERIFY`** on the By-document row — a button in a **stat row**, forcing the counts to justify around it.

> ## **A ROW THAT NEEDS ATTENTION SHOULD BE *MARKED*, NOT *CAPTIONED*.**
> **A label competes with the content for the row. A marker sits beside it and lets the content keep its alignment.** *The user is scanning a list; every chip is a stop sign in the middle of a sentence.*

**BINDING:**
1. **Replace the chip with a minimal row marker** — a **quiet accent** (a rule, a bar, a small mark) that **does not enter the text flow and does not move a single character of the row's content.** **Alignment across all rows must be IDENTICAL, marked or not.**
2. **The MEANING moves to the ⓘ / hover / the section header** — *not resident, on demand* (DL-107/D185).
3. **`VERIFY` stops being a resident button in the stat row.** The row is a **readout**; the action belongs on **hover / row-click / the ⓘ**, or as a **single affordance for the panel**, never one wedged into one row's number column.
4. **⛔ Guard: a marked row and an unmarked row have IDENTICAL text geometry** (same start x, same end x for the content). **Mechanism, measured — not eyeballed.** **NC: put the chip back in the flow → RED.**
5. **The marker must survive being colour-blind** — it may not rely on colour alone (a11y), and **it is NOT severity colour** (D003 — this is not an issue).

---

# D199 — MISS: the trend surface still says "CONFIDENCE." (owner, 2026-07-13)

**Owner: *"Did you forget to update this to Outcome Confidence?"*** **Yes. And the reason is a GUARD GAP, which is worse than the typo.**

**D183b bound TWO things:** *(a)* **delete the 0–100 index**, and *(b)* **adopt the "Outcome Confidence" label.** **A guard was built for (a) and NOT for (b)** — so the index is provably gone everywhere, while **the LABEL was left to be remembered**, and on the trend surface it wasn't.

> ## **THIRTY-FOUR GUARD DEFECTS IN, THE LESSON REPEATS: WHAT IS NOT GUARDED IS NOT TRUE.**

**BINDING:** **every user-facing surface naming the concept says "Outcome Confidence"** — hero, pill, popover, **trend**, History, chat, reports, tour, prototype notes. **Guard: the bare word "Confidence" NEVER appears as a LABEL for the concept.** *(It may appear inside prose; grade the ROLE, not the substring.)* **NC: revert one label → RED.** **Sweep every surface, not just the one in the screenshot.**

## Decision 250: Overview Progress panel — foundation-bar (DL-111 fold-in)

Status: Locked from docs (ratified canon DL-111)
Type: Product Design | Screen/Interaction
Area: Overview / Progress panel
Slice: 10 (Tiering & Limits — Overview surface)
Feature: Progress panel
Question ID: WI-R5
Source: 00_owner/decisions/records/DL-111-progress-panel-foundation-bar.md
Source classification: Product evidence (ratified)

Decision:
The Overview Progress panel is a FOUNDATION BAR: a hero count of grounded facts (attested + derived, computed), a proportional Confirmed-by-you + From-OSLO solid bar with a set-apart provisional inferences tail, and OPEN/CLOSED work stats with severity red on Critical only. Reconciled with the Outcome Confidence panel (cool accent echoing the ramp, orange off-state, neutral deltas, de-exiled tail).

Rationale:
Owner directed the original locked design; harmony pass against the Confidence panel narrowed the reversal; ratified as DL-111. Supersedes the class-ledger presentation (D194c) FOR THIS PANEL only. Every number computed; guards re-based and live (135/135).

Impacts:
- vertical-slices/slice-10-tiering-limits/frontend-ui.md
- vertical-slices/slice-10-tiering-limits/user-experience.md
- vertical-slices/slice-10-tiering-limits/success-criteria.md
- vertical-slices/slice-10-tiering-limits/edge-cases.md
- vertical-slices/slice-10-tiering-limits/open-items.md
- vertical-slices/slice-10-tiering-limits/product-detail.md
- vertical-slices/slice-10-tiering-limits/e2e-test-scenarios.md
- vertical-slices/slice-10-tiering-limits/prototype.html

## Decision 251: Progress panel — grounded-facts arithmetic & two-state provenance (ERRATUM to Decision 250 / DL-111)

Status: Locked (owner-directed correction, 2026-07-14)
Type: Product Design | Screen/Interaction | Product Constraint
Area: Overview / Progress panel
Slice: 10 (Overview)
Feature: Progress panel
Question ID: WI-R5 (erratum)
Source: owner defect report, 2026-07-14; prototype slice10 R6 build
Supersedes: the arithmetic + vocabulary of Decision 250 (design unchanged)

Decision:
Three defects in the ratified foundation bar are corrected — the DESIGN is kept, the ARITHMETIC and VOCABULARY change:
1. **Grounded facts = ATTESTED ONLY.** The hero is the grounded count alone (evidence_id present), NEVER grounded+inferred. Inferred claims (evidence_id null) are not grounded facts. The grounded number lives in the hero; the "Confirmed by you" segment carries only its label.
2. **Two provenance states, not three.** The model has grounded (evidence) and inferred (none). "From OSLO" IS the inferred state, rendered hatched; the "Derived — supported" third class is deleted. Legend: "Grounded — your evidence" · "Inferred — OSLO's read".
3. **Load-bearing is a superset, not a disjoint addition.** Inferred claims ⊂ load-bearing inferred items of every type; the bar no longer `+`-joins them. Load-bearing is its own line: "Your read leans on N inferences — the inferred claims above plus inferred assumptions, relationships and metrics · See them →".

Guards now grade the POPULATION, not the string: grounded == attested-only (hero ≠ a+d); exactly two provenance classes in the legend; the bar never combines the inferred-claims count with the load-bearing count. The old guards passed the lie because they only proved "computed" and "registry-sourced" — neither was the thing that was wrong.

Rationale:
Owner defect report: the "blend / 29-hero" lock (DL-111) changed the design and smuggled in bad arithmetic; it superseded exactly D194c (ledger) and D176 (no-proportion), the decisions that had been holding this line. Correction keeps the hero and the bar. Prototype R6: 136/136 self-check, 0 pageerrors.

Impacts:
- vertical-slices/slice-10-tiering-limits/prototype.html
- vertical-slices/slice-10-tiering-limits/{frontend-ui,user-experience,success-criteria,e2e-test-scenarios,edge-cases,open-items}.md
- 00_owner/decisions/records/DL-111 (canon erratum owed — drafted, awaiting owner land)

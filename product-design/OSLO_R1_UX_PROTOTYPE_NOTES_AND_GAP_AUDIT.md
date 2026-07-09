# OSLO R1 — UX Prototype: Notes, Decisions & Spec-Gap Audit

**Artifact:** `oslo_r1_experience_mockup_v4.html` (single self-contained file; dark Intralign theme)
**Status:** Working target-experience prototype — **illustrative, not canon.** Structure traces to ratified specs; sample text/numbers are demo data on the DevNorth 2026 sample.
**Date:** 2026-06-30

> **v4 update (2026-07-09) — current baseline.** `oslo_r1_experience_mockup_v4.html` supersedes v3 and is the reference of record: it integrates the ratified **DL-096** Overview redesign (confidence-led — focal score, CAF maturity bars with band words + hover, quiet change-delta trend, Why disclosure; ring / green box / Current-From OSLO pills removed) into the full experience, on top of DL-094 (issue lifecycle) and DL-095 (Issues label). CAF-dimension bands use the ratified ramp **Limited · Forming · Solid · Strong** (DL-097, pending; band→score thresholds are a separate calibration item). v3 preserved as the prior baseline. **Follow-up:** regenerate the visual-regression baselines from v4.

> **v3 update (2026-07-08) — prior baseline (superseded by v4).** `oslo_r1_experience_mockup_v3.html` supersedes v2 and is the reference of record. v3 realizes two ratified decisions: **DL-095** — the user-facing label is **"Issues"** (Findings/weaknesses retired from the UI; Finding stays the internal object; the find/severity toggle is relabeled **By dimension / By severity**); and **DL-094** — the issue lifecycle is simplified to **Open -> Addressed -> Resolved** (the *Acknowledge* stage removed), with single-action **"Apply this fix"** where OSLO can draft (`validated`/`recommended` are internal-only — no UI change). v2 is preserved (marked superseded) because ratified records **DL-088/090/093** reference it. **Follow-up:** the visual-regression baseline screenshots (`30_engineering/visual_regression/`) must be regenerated from v3 for the issue/lifecycle surfaces.

> This is a design exploration. Per the Authority Constraint, none of this is ratified UX; when the direction is locked it should route through Framework 001 as a UX-revision proposal against `10_product/experience` for owner ratification.

---

## 1. How to resume from here (lock & continue)

- The prototype is **one HTML file** — open it by double-click; edit in any editor. No build step, no dependencies (Google Fonts via CDN, degrades to system fonts).
- To continue in a new session: open this notes file + the HTML; everything needed to pick up is here. Decisions and remaining gaps are in §3–§4.
- The file is the **source of truth** for the prototype. Versioning is whatever you keep in the folder (or commit it to the repo under a `product-design/` path if you want history).
- Nothing here has touched canon — the `10_product/experience` specs are unchanged.

## 2. Decisions captured in the prototype (canon mappings)

| Area | Decision in prototype | Canon source |
|---|---|---|
| Intake | Any readable document (paste/upload); templates optional quick-starts → synthesized into artifacts | Template Intake spec; DL-077 |
| Artifacts | 7: **Intent · Context · Scope · Requirements** (understanding core) + **WBS · Schedule · Resources** (classical-PM execution) | **DL-077** |
| Flow | Fast Pass <60s → **60-second orientation lands on MRI** → **Deep Pass auto-runs** (non-blocking) and supersedes | DL-046; SIXTY_SECOND_ORIENTATION; Canonical Scope §48; Capability Matrix AE-02 |
| MRI | **Heatmap primary** (artifacts × CAF), CAF field secondary | MRI Experience; MRI model (Heatmap) |
| Confidence/CAF | Visual-first, band + **0–100 maturity index** (explainability), neutral ramp — never health; always reliability-qualified | Visual/Brand spec §1.2; Confidence v2; CAFDimensionScore |
| Artifact editor | Flowing prose, type-appropriate (narrative/bullets/tables); **live edit, autosave, event-driven reanalysis** (no explicit edit/save) | Artifact Workspace; Authoring & Editing; AW-03/AE-03 |
| Annotations | **Inline color on the contiguous weak text** (severity ramp); hover summary; click → Finding Panel | Artifact Workspace §G CAF overlays; Finding Presentation |
| Epistemic notation | Per text: **Derived (OSLO)** default; edit/confirm → **Attested (you)** plan fact | DL-043; PlanFact (attested-user); Wave U DTM-0016 |
| Finding panel | Contextual panel (Header→Why→Evidence→CAF impact→Recommendations→History→Reanalysis); can't resolve by hand | **Finding Panel spec (Option A, ratified)** |
| All-findings | Overlay grouped **by CAF dimension, severity-ordered**, filters by dimension/severity; honest "hidden by filters" | Finding Presentation spec |
| Recommendations | OSLO Recommended + Possible Resolution Paths, **selectable → Selected Path** (Attested) | Recommendation Presentation; Finding Panel §J |
| Chat | Global persistent panel + **engage in context** from a finding | OSLO Chat spec; IMPLEMENTATION_PLAN M3 |
| Free tier | UP-3 limit modal — honest, two paths, non-destructive archive | DL-048; Seam Audit; Visual spec §1.3 |
| Analysis labels | User-facing **Initial Analysis / Extended Analysis** (internal terms unchanged) | DL-046 + Disambiguation entry: Initial=Fast Pass, Extended=Deep Pass (owner 2026-06-30) |

## 3. Spec-vs-UI gap audit — by canonical screen (UI_SCREEN_INVENTORY) + behavior

Legend: ✅ captured · ◐ partial · ⬜ not yet

> **⚠ Refreshed 2026-07-01 — read this first.** The tables below are the *original baseline*; most items have since been built (see §6.x logs). Current authoritative status:
>
> **Now ✅ (closed since baseline):** Reliability card · full Overview §D hierarchy (progressive-disclosure, single-open) · finding lifecycle + acknowledge · History/timeline · Apply-Suggested-Fix (direction-only) · confidence/reliability trend · false-confidence surfacing · confidence stages (in ⓘ) · overlay next/prev · Dashboard/Workspace Home (Pinned/Recent) · Notification center (routes-to-source) · Settings (visibility-first) · Export (currency + disclaimer) · Share (view-only link) · comments · dark/light + accessibility (focus/keyboard/reduced-motion) · **analysis-state honesty (provisional/current + error/retry)** · **Clarification Requests** · recommendation de-dup (Panel Model, Decision 001).
>
> **Still ◐ (partial, R1):** Empty states (none-found/none-lens live; not-yet-analyzed/unavailable coded, error/last-good now wired) · Analysis Progress (no per-run cancel) · full Orientation-state machine (8 states — provisional/current/error wired; not all transitions) · honest-limit **partial orientation** for over-size Free projects · **in-app evidence ingestion** (edit artifacts only; no evidence tray) · artifact prev/next · brand tokenization (residual `rgba()` alphas).
>
> **🚫 Escalated / out of scope:** CRR (genuine spec gap — not invented) · notification delivery, billing, link-access enforcement (spec-deferred) · owner-TBD numerics (confidence index, latency).
>
> **Divergence to reconcile (owner):** MRI nested in Overview vs. NAV-C3 "MRI as co-primary" (owner-directed) · UI_SCREEN_INVENTORY still lists "Recommendation Workspace" (stale vs. Decision 001).

### Primary screens
| Screen | State | Notes / what's missing |
|---|---|---|
| Project Creation / intake | ✅ | composer + templates + analysis scan |
| 60-Second Orientation | ✅ | lands on MRI; Time-to-First-MRI shown |
| Project Workspace (hub) | ✅ | IDE shell: explorer + center + global panel |
| Artifact Editor | ✅ | prose, type-aware, live edit, inline annotations |
| Analysis Progress | ◐ | intake scan + Deep-Pass banner; no per-run progress/cancel UI |
| Deep Analysis Results | ◐ | auto Deep Pass supersedes; **no distinct results/run-history view** |
| Findings Workspace | ✅ | all-findings overlay + filters + Finding Panel |
| Recommendation Workspace | ◐ | rec tab + in-panel selection; **no standalone Recommendation Panel as a distinct surface** |
| **Dashboard** (multi-project) | ⬜ | v2 is single-project; **no multi-project dashboard / attention feed** |
| **Report Viewer** (view/version/publish/archive/export) | ⬜ | not built |
| **Shared Artifact Viewer** (scoped read) | ⬜ | not built |
| **Notification Center** | ⬜ | not built |
| **User / Workspace Settings** | ⬜ | not built |

### Embedded views
| View | State | Notes |
|---|---|---|
| Confidence Experience (history/trend/CAF drivers) | ◐ | persistent panel + Understanding tab; **no trend/history chart** |
| Explainability panel | ✅ | Finding Panel evidence + CAF impact |
| Activity / Comments thread | ⬜ | no comments/replies/mentions |
| Sharing dialog | ⬜ | not built |

### Behaviors / models not yet reflected
| Behavior | State | Notes |
|---|---|---|
| Reliability **card** with basis (Coverage / Evidence / Assessability) | ◐ | shown only as a qualifier label; no dedicated breakdown |
| Project Overview hierarchy (Header→Confidence→CAF→Reliability→Findings→Recs→Summary) | ◐ | Understanding tab has confidence+CAF; missing Reliability card, Recs summary, Project Summary |
| Overlay **navigation** (next/prev weakness) + "select overlay" focus | ⬜ | Workspace §G interactions |
| Finding **lifecycle** (detected→acknowledged→addressed→closed) + acknowledge action | ◐ | status shown as "detected" only; no transitions |
| **History / timeline** (append-only, closed findings, version lineage) | ⬜ | History nav is a stub |
| Empty-state distinctions (no findings / no overlays / not-yet-analyzed / unavailable) | ⬜ | only the free-tier + empty-second-project states |
| **Apply Suggested Fix** → confidence updates via Deep Pass (REC-04/05) | ⬜ | accept/defer present; no apply-fix flow |
| **Clarification Requests** (finding/flow) | ◐ | chat exists; no explicit clarification object/flow |
| **CAF Review Requests (CRR)** → evidence → Deep Pass (virality loop) | ⬜ | Alpha-scope; not built |
| Confidence **stages** (Orientation→Expanded→Validated, CONF-05) | ◐ | "Preliminary" badges only |
| **False-confidence flag** (CONF-06: high band on low reliability) | ⬜ | in model; not surfaced |
| Understanding **state** (Initial→…→Mature, AE-04) | ⬜ | not surfaced |
| Two-mode onboarding: anonymous first run + **signup = save-to-keep gate after orientation** (DL-073/080); sample-project flag banner | ◐ | intake + "sample" chip; no signup-to-save gate |
| Honest-limit **partial orientation** for over-size Free projects (DL-048) | ◐ | limit modal only |
| Evidence ingestion **in-app** (add more evidence / evidence tray) | ◐ | onboarding attach only |
| Artifact prev/next + hierarchy navigation | ◐ | explorer list; no prev/next |
| Accessibility (WCAG 2.1 AA: focus rings, keyboard nav, reduced-motion) | ⬜ | not addressed in prototype |
| Brand as **token swap** (CSS variables, no hardcoded hex) | ◐ | uses Intralign tokens but hardcoded hex (prototype) |

## 4. Suggested next refinements (priority order)

1. **Reliability card + full Project Overview hierarchy** (closes the headline understanding console gap).
2. **Finding lifecycle + History/timeline** (acknowledge; append-only closed findings) — core to the descriptive model.
3. **Apply Suggested Fix flow** (the improvement-loop "aha": apply → Deep Pass → confidence moves).
4. **Empty states** (the four honest distinctions) + **overlay next/prev navigation**.
5. **Multi-project Dashboard** + **Notification/Awareness**.
6. Collaboration (comments/mentions), Sharing/CRR, Export/Report viewer — Alpha-scope, larger.
7. Accessibility pass + tokenized brand (for build-handoff).

## 4b. Global Navigation & App Shell reconciliation (added 2026-06-30)

Reconciled the IA against `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1.md` (the "navigation constitution"):

- **Validated by spec:** Findings/Recommendations as contextual Panels not nav destinations (NAV-8); Overview·MRI·Artifact primary, Collaboration·History secondary (NAV-C3); lifecycle reinforced-not-enforced (NAV-9); context preserved on close (NAV-7).
- **Applied:** renamed the understanding view **"Understanding" → "Overview"** (spec's canonical primary "Project Overview"); added a **minimal global (Workspace) frame** — OSLO logo = Workspace Home, a **project switcher** chip, and an **account/settings** avatar — so the three nested contexts (Workspace › Project › Object, NAV-6) are visible and distinct. Left rail = Project/Object (artifacts); top-left = Workspace; top-center = Project views; top-right periphery = Settings/Account.
- **Still open (NAV conformance gaps):** full **Workspace Home / Project List / Create Project / Settings / Account** screens are stubs (alerts) not surfaces (NAV-C1); **Collaboration** secondary surface absent (§K); nav **empty/failure states** (§O/§P) absent; returning-user lands on Workspace Home then project→Overview (§N) not modeled (new-project flow only).

## 4c. Color semantics — risk/traffic-light scope (owner Q, 2026-07-01)

**Decision applied:** red/amber/green (the alert ramp) is used **only for finding severity** (critical/moderate/warning) — on the attention heatmap cells, the "what's weakening understanding" list (severity-colored left accents), finding chips, and left-rail count badges. **Confidence and CAF stay on the neutral maturity ramp and are never health/traffic-light colored.**

**Why (canon, not style):** Confidence is *understanding maturity* — "not health, readiness, probability, or risk" (Confidence Doctrine; Confidence Model §5). The Visual Design spec §1.2 is explicit: *"Confidence/CAF are NOT health-colored — use a neutral maturity ramp… never red=bad / green=good; low confidence must not read as a failing project."* A red confidence ring would collapse "how well does OSLO understand this?" into "is this project failing?" — a category error, since low confidence often just means thin evidence / early draft on a healthy plan. Risk is therefore carried by the **findings** (which actually represent risk), plus the **reliability qualifier** and **false-confidence flag** for "how much to trust the read." Coloring confidence/CAF by risk would be a **doctrine-level change** requiring a Framework 001 proposal, not a UI tweak.

## 6.4 Analysis-state honesty + Clarification Requests (2026-07-01)

- ✅ **Analysis-state honesty (ORIENTATION_STATE_MODEL / AE-04)** — the Overview confidence hero carries a **provisional ↔ current** chip (provisional while Extended Analysis runs, current when complete). An **error / last-good** state is reachable: the "reanalysis failed" awareness item routes to the Overview and shows a "Reanalysis couldn't complete — showing your last-good understanding · Retry" banner; Retry recovers (provisional→current). Honors "only reanalysis changes assessment" and "last-good preserved." (Full 8-state machine not all wired, but the trust-critical signals are.)
- ✅ **Clarification Requests (IC-WC-ADVISE `clarification_requested`)** — the ambiguity finding (FND-2052) now carries a "OSLO needs a clarification" block in the Finding Panel with a question + answer input; answering = Update Project Information → reanalysis → the finding closes and Clarity strengthens. Flagged with a "❓ clarification" tag in the all-findings list. Advisory framing preserved (OSLO asks; you answer; you decide).

## 6.5 Education surfaces + arrival-notice coordination (2026-07-01)

- ✅ **Optional feature tour** — a 6-step **spotlight coachmark** walkthrough over the real UI (strategic read → where to focus → attention map → artifacts/edit → chat → confidence pill). Opt-in only (top-bar "?", first-run coach-tip link, Settings → Help); never gates value. Distinct from the strategic-chain **orientation** (the "why"), which remains in Settings → Help.
- ✅ **Arrival-notice coordination fix** — the "Initial analysis complete in Ns" banner is now emitted **only at completion of a fresh analysis** (ingest/sample), hidden by default, and not shown to returning users re-opening an analyzed project. The time is a slot (illustrative "41s") to be driven by the measured Time-to-First-MRI (owner-TBD NFR, DL-046).

## 6.6 Tier boundaries / gates / upsell (visibility-first, 2026-07-01)

R1 scope, framed **visibility-first** (present limits + upgrade paths honestly; billing/enforcement deferred). Canon: DL-048 (honest limits + non-destructive archive + partial orientation), Dashboard §E (Create stays enabled → upgrade-or-archive at cap), Settings→Subscription (plan facts), DL-080 (anonymous cap, Fast-Pass-only).
- ✅ **At-cap limit modal wired** — was dead code; "New project" at the Free cap now fires the honest **upgrade-or-archive** prompt. Archive path is non-destructive and frees the slot → create; upgrade path is visibility-first (billing on the user's side).
- ✅ **Persistent plan/upgrade chip** — a quiet "Free · Upgrade" chip in the app top bar and Workspace Home; opens the same prompt. Quiet, non-nagging tone (doctrine + honesty ethos).
- Already present: Settings→Subscription card (plan/usage as facts), export "PDF only" hint, save-to-keep (DL-080), workspace "1 active project" note.
- ⏸ **Deferred (owner-TBD tier rules):** the **Extended-Analysis-on-Free gate** (distorts the value demo + depends on unratified Tier Definitions) and **partial orientation for over-size Free projects** (DL-048; size threshold owner-TBD). Concepts are referenced in modal/Settings copy; not hard-built on unratified rules.
- **Anti-Assumption:** all tier values/limits/prices are **illustrative** — the Release 1 Tier Definitions are owner-TBD; the prototype shows the *structure* of gates/upsell, not ratified tier rules.

## 6.7 UX principle — integrity reminders (single-home + hover)

**Principle (for the build):** each epistemic/integrity invariant — e.g. "only reanalysis changes the assessment," "append-only / never overwritten," "presentation-only," "findings aren't resolved by hand," "confidence isn't health/score" — appears as **persistent text in exactly one home surface**, and everywhere else is **available on hover (ⓘ)** or omitted. The *behavior* enforces the invariant, so the UI must not reprint it as standing chrome on every panel. Reprinting reads as repetitive and slightly patronizing and adds cognitive load.

**Applied (2026-07-01):** removed/hover-moved redundant reminders on the Notification panel, History overlay, Finding Panel (History + footer + recommendation-grouping + reanalysis note), heatmap legend, and Settings — each invariant now has one home + ⓘ elsewhere. General decluttering rule already in force: teaching/explainer copy → hover ⓘ or one-time interstitial, never persistent chrome; metrics/status/actions persist where they belong.

## 6.8 Plain-language pass (2026-07-01)

Replaced user-facing jargon with plain labels; **canonical terms stay internal** (new Disambiguation entries, same pattern as CAF and Initial/Extended Analysis):

| Canonical (internal) | User-facing |
|---|---|
| Derived | **From OSLO** |
| Attested / attested-user / "Attested plan fact" | **Confirmed by you** / **part of your plan** |
| Selected Path | **the approach you chose / Choose this approach** |
| Assessability (Reliability component) | **How assessable** |
| Provisional (analysis state) | **Still updating** |
| MRI (residual nav-title/alert) | scrubbed (Attention is the plain surface) |

Also live: the finding panel's **state-aware plain-language guide** (§ prior) separating "your take" (acknowledge) from "resolve it," and CAF → Clarity·Alignment·Feasibility. Kept as-is (plain enough / audience-appropriate): Confidence, Reliability, Findings, Initial/Extended Analysis, WBS.

**Resolved (owner, 2026-07-01):** "Artifacts" → **"Plan sections"** and "WBS" → **"Work breakdown"** (user-facing display; internal keys `artifact`/`WBS` unchanged via a `dispName` display-map — a Disambiguation-style split). Chosen to read for both the PM ICP and the secondary non-PM-who-manages-projects audience. Canonical **DL-077** term "planning artifacts" stays internal.

## 6.9 Proficiency-based sunset of teaching copy (2026-07-01)

**Principle (for the build):** onboarding/teaching copy is **adaptive** — it fades as a function of interaction, so it doesn't nag an activated/expert user. Mechanism: a small persisted proficiency store counts meaningful actions; each teaching message declares a threshold and hides once the user has passed it (`learned(key)`). Status/feedback copy (not teaching) is exempt.
- **Applied (exemplar):** the finding panel's detected/acknowledged **teaching guide** sunsets after ~3 finding-flow interactions (acknowledge / resolve); its addressed/closed **status** lines always show. A **Settings → Help → Guidance tips → Reset** control (and the ? tour / orientation) let a user bring guidance back.
- **Extensible to:** the Overview coach tip, the arrival tour offer, in-flow interstitials, hover teaching — same `profBump`/`learned` pattern keyed per message. (Prototype persists via localStorage; real build would tie to the user/workspace profile.)
- This complements §6.7 (single-home + hover): first-time users get full plain-language guidance; repeat users get a progressively quieter UI.

## 6.10 Quantified + qualified progress — moving confidence number, honestly (2026-07-01)

**Owner concern:** pragmatic PMs discount progress they can't quantify; and a displayed confidence number that *doesn't move* when the user acts reads as broken ("don't show a dial you won't let move"). But the Confidence Interpretation Doctrine warns a bare number invites probability/health misreading, is **noise below band granularity** (±7 / same-band, OPEN_TBD D1), and — if only ever pushed *up* — pressures against **honest decreases**.

**Resolution (two tracks):**
- **Track 1 — Confidence signal moves, but governed.** `bumpConfidence()` now moves the ring index (58→66, illustrative), the arc, the band, and the Feasibility CAF level (Limited→Forming) on resolve, and the top-bar pill pulses. Every move is **cause-bound** (annotated with the resolved finding), **never bare** (band + reliability always shown), **labelled illustrative/calibration-pending**, and the trend chart shows the index can **fall** (Initial 61 → Extended 58, ▼) as well as rise — with a tooltip framing a fall as *better understanding, not a worse project*. This makes the doctrine's "change is cause-based" and the owner's "causes reflected in effects" the same requirement.
- **Track 2 — Quantified work-ledger (always safe).** A persistent `#ledger` "Progress" strip counts **concrete governed objects** — findings resolved/open by severity, dependencies confirmed, plan-section coverage — updated by `renderLedger()` on resolve. These are countable attested objects (outside the Confidence signal's scope), giving PMs hard, un-caveated numbers to judge improvement *or its absence*.
- **No gamification:** no points/streaks/badges; the number is a reading, not a reward; Confidence/CAF keep the neutral (non health-color) ramp — only findings carry severity color.

**Governance:** the moving user-facing index is a **presentation-doctrine** change → drafted as `PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT.md` (Framework 001, Conditions 1–7) for **owner ratification**. Prototype demonstrates it illustratively (non-canon).

## 6.11 Heatmap → findings routing + Section filter (2026-07-01)

**Bug (owner-found):** a heatmap cell is a **section × dimension** bucket, but the click hardcoded a single `openFindingPanel(<id>)`. Cells aggregating 2+ findings (Resources × Feasibility, Requirements × Clarity — both show "2") silently opened one finding and dropped the rest.

**Fix:** cells now route through `openFindingsFor(art,dim)` — if exactly one open finding matches, it opens that finding directly (no extra click); otherwise it opens the Findings list **scoped to that bucket** (both the Section and Dimension filters light up). Count-agnostic and future-proof: as findings close, a cell flips from list→direct automatically.

**Consistency gap (owner-found):** the heatmap could scope by section, but the Findings panel exposed only **Dimension** and **Severity** filters — no user-facing way to do the same. **Added a third `Section` filter row**, generated from the sections that actually have active findings (plain-language names via `dispName`, plan-order sorted), so it stays in sync as findings resolve. Heatmap scoping and manual filtering now share one visible mechanism; the interim scope chip was removed as redundant (the highlighted buttons + "N hidden by filters · clear" cover it).

**Responsive:** on narrow widths (≤560px) each filter group (label + its buttons) stacks as its own row so Dimension / Severity / Section don't interleave.

## 6.12 Confidence number: primary in hierarchy + production-clean presentation (2026-07-01)

**Hierarchy (owner direction):** in the confidence ring and the top-bar pill, the **number is now the focal element** and the **band (e.g. "Moderate") is the secondary qualifier** beneath it. Rationale: pragmatic-PM readability; the number is the figure they track. Guardrail preserved: the number is never bare — band + reliability sit with it.

**Production-clean caveat (owner decision 2026-07-01):** the on-screen word **"illustrative" is a mockup artifact and does NOT ship.** Two senses had been conflated: (a) *demo data* — the 58/66 values are fake, a prototype-only thing; (b) *calibration-pending* — a real but **temporary** doctrine state (OPEN_TBD D1), removed once the owner ratifies calibration. Decision: production shows the number **clean**. Honesty is preserved by **behaviour, not a disclaimer**:
- never shown bare (band + reliability + cause always present);
- a subtle **"how this is calculated"** info affordance next to the number (added on the card);
- sub-band jitter (within the ±7 / same-band tolerance) is **not** animated or celebrated — only real, cause-bound changes move it;
- it moves **both ways** (a fall after Extended Analysis usually means it found something real).

**Applied:** removed the visible "illustrative" text from the change banner, the trend header, and the movement tooltip; added the "how this is calculated" tooltip. The demo-data caveat now lives **only** in these notes (§5) and the code comment, not on screen. Proposal `PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT.md` Conditions 2 & 4 updated to match (clean number; magnitude calibrated, not caveated).

## 5. Anti-Assumption note

The prototype's **structure** is canon-traceable (table §2). The **content** (DevNorth sample text, finding wording, index values 58/64/38/34, severities, filter contents) is **illustrative demo data**, not ratified values. Numeric NFRs (e.g., confidence index, latency p50/p95) remain **owner-TBD** (OPEN_TBD A1/A2) and must not be read as canonical from this mock.

## 6. Tier build log — gap closure pass (2026-07-01)

All four gap tiers were designed into the prototype, each grounded in the governing spec (paths cited). Newly closed (✅), advanced (◐→), or deliberately **not built**:

**Tier 1 — Core R1 descriptive model** (`RELIABILITY_MODEL_V1`, `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` §D, `FINDING_SYSTEM_SPECIFICATION_V1` §C, `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1`, `RECOMMENDATION_SYSTEM_SPECIFICATION_V1` §11, `CONFIDENCE_MODEL_V1`, `ORIENTATION_STATE_MODEL_V1`, `ARTIFACT_WORKSPACE_SPECIFICATION_V1` §G):
- ✅ **Reliability card** with the three spec components — Coverage · Evidence availability · Assessability (levels High/Moderate/Low), stated as independent of CAF.
- ✅ **Project Overview canonical hierarchy** — Confidence → CAF → Reliability → Findings → Recommendations → Project Summary (§D order).
- ✅ **Finding lifecycle** — detected → acknowledged → addressed → closed track in the panel; Acknowledge action; status shown in panel + all-findings list. "Never resolved by hand" preserved.
- ✅ **Apply-Suggested-Fix loop** — select path → *addressed* → "Update information & reanalyze" → reanalysis **closes** the finding and moves Confidence (58→66 demo). Encodes RECOMMENDATION_SYSTEM §11: acceptance ≠ success; success is downstream.
- ✅ **History & timeline overlay** — append-only event list (analysis runs, versions, finding-lifecycle, selected-recommendation, comments), current/prior labels; live-appends on actions.
- ✅ **Confidence stage** indicator (Orientation ▸ Expanded ▸ Validated) + **false-confidence** surfacing (names the cause: CAF weakness vs reliability shortfall; note that a high band on low reliability is flagged).
- ✅ **Overlay next/prev weakness** navigation in the artifact (§G hover/click/select/navigate).
- ◐ **Empty states** — none-found demonstrated (Alignment); not-yet-analyzed / unavailable noted but not fully wired.

**Tier 2 — Multi-project shell** (`PROJECT_DASHBOARD_AND_PROJECT_LIST…`, `GLOBAL_NAVIGATION…` §N, `NOTIFICATION_AND_AWARENESS…`, `ACCOUNT_AND_WORKSPACE_SETTINGS…`):
- ✅ **Workspace Home / Dashboard** — Pinned + Recent, per-project fields (name, ownership/shared, analysis status incl. **stale**, reliability-qualified understanding indicator, recency, findings), archived pointer, "no computed scores" note.
- ✅ **Notification / awareness panel** — R1 categories (mention, reply, shared-with-me, reanalysis complete/failed, stale), read/unread (presentation-only), "routes to source", "never triggers reanalysis"; unread badge in app + workspace.
- ✅ **Settings** — 10 areas (Account, Profile, Workspace, Project defaults, Collaboration, Notifications, Subscription, Billing, Integrations, Membership), visibility-first for billing/subscription/integrations/membership.

**Tier 3 — Alpha-scope collaboration** (`COLLABORATION_AND_SHARING…`, `EXPORT_AND_SHARE_OUT…`):
- ✅ **Sharing dialog** — invite + participant types (Owner/Collaborator/Viewer) + **view-only link** (snapshot, "previous analysis" if stale); presentation-only, no permission enforcement.
- ✅ **Export / share-out** — packages existing understanding, **analysis-currency marker**, required **disclaimer** (not health/readiness/probability), PDF/copy/link, Free=PDF-only note.
- ✅ **Comments / discussion** — threaded on findings, @mentions, append-only, "comments never change the assessment".
- 🚫 **CAF Review Requests (CRR)** — **NOT built. Genuine spec gap** — the finding→evidence-request→Deep-Pass "virality loop" is not defined in any R1 surface spec. Per Anti-Assumption it is **escalated to the owner**, not invented. Needs a dedicated spec/amendment before it can be designed.

**Tier 4 — Build-handoff polish** (`RELEASE_1_VISUAL_DESIGN_AND_BRANDING…` §1/§3, Open-TBD E2):
- ✅ **Accessibility** — `:focus-visible` rings (`--color-focus`), `prefers-reduced-motion` honored globally, **no-animation-during-analysis** (`.analysis-active` gates MRI motion during Extended Analysis).
- ◐ **Accessibility (remaining)** — clickable `<div>`s (cards, cells, metrics) still need `role="button"`+`tabindex` + arrow-key nav; contrast audit not run. Core controls are real `<button>`s (already focusable).
- ◐ **Brand tokenization** — layout/color largely on CSS variables; residual hardcoded hex/rgba remain (prototype). Canonical Intralign token set (from VISUAL_DESIGN spec) not yet swapped in 1:1; token-adherence lint is a build-phase item.

### Open design decisions surfaced for owner (defaults applied, changeable)
1. **Confidence movement on apply-fix** — demo bumps 58→66. Real deltas are owner-TBD (OPEN_TBD A1). Direction only, not a ratified number.
2. **Collapsed-panel ambient confidence** — with no top-bar pill, collapsing the right rail hides all metrics. Accepted as an opt-in trade; revisit if an ambient readout is wanted.
3. **CAF compact rows** — level word moved to expand; only bar+index show at first level. Flagged earlier as a mild tension with "CAF is qualitative, not a score."
4. **CRR** — escalated; owner must decide R1 vs post-R1 and commission a spec.
5. **Notification delivery, link access-enforcement, billing** — all "visibility-first" per spec; real infrastructure deferred.

## 6.1 Follow-up pass (owner decisions applied, 2026-07-01)

Per owner direction after the tier build:
- ✅ **CRR** — confirmed **left out & escalated** (spec gap; needs a dedicated spec before design).
- ✅ **Apply-fix confidence = direction-only** — the 58→66 number was removed; confidence now shows "▲ rose" with a tooltip that the index is owner-TBD (OPEN_TBD A1). No fabricated figure on screen.
- ✅ **Reliability/confidence trend** — added an inline sparkline ("Understanding over runs") in the Overview confidence card; appends an "after fix ▲" point when a finding is closed. Direction-only.
- ✅ **Empty states** — canonical `_empty()` helper with four distinct states (none-found / none-under-lens / not-yet-analyzed / unavailable, each with correct copy). None-found + none-under-lens are live (resolve or filter findings); not-yet-analyzed/unavailable are coded and reachable only in their lifecycle contexts (new project / load failure), which the single happy-path demo doesn't force.
- ✅ **Accessibility** — an enhancer adds `role="button"` + `tabindex` to all clickable non-native elements and a delegated Enter/Space activator; a MutationObserver keeps dynamically-rendered content covered. Focus-visible rings + reduced-motion already in place. **Still build-phase:** a formal contrast audit and arrow-key roving within grids.
- ◐ **Brand tokenization** — standalone hardcoded hex (`#fff`, amber-fg) moved to tokens (`--on-accent`, `--amber-fg`); no bare component hex remains outside `:root`. **Still open (flagged for owner):** (a) `rgba(217,122,58,…)` alpha literals aren't tokenized (needs `color-mix`/token-alpha at build); (b) the prototype's base palette runs a shade darker than the ratified VISUAL_DESIGN token values (e.g., bg `#0E1013` vs canonical `#111315`) — a deliberate look-decision to confirm before the token values are aligned 1:1.

## 6.2 Dark + light theming (owner decisions applied)

Adopted the ratified two-theme model (VISUAL_DESIGN §1): one set of **semantic tokens** — dark in `:root` (default), light overriding the *same names* under `:root[data-theme="light"]`; component CSS references tokens only, so a single attribute flips the whole app.
- ✅ **Dark re-baselined to the canonical Intralign palette** (bg `#111315`, surface `#1B1F24`, border `#343B44`, etc.) — resolves the earlier shade decision.
- ✅ **Light theme** added (warm-white surfaces, dark text). **Orange contrast handled**: `--primary-light` darkens to `#B45309` for text/links in light (AA), while button text stays charcoal-on-orange in both (AA 4.8:1). Focus ring uses brand orange (non-text, AA).
- ✅ **Neutral maturity ramp per theme** — dark: grey→white; light: **single-hue intensity** (pale→dark). Non-health in both, per the epistemic rule.
- ✅ **Theme-sensitive surfaces tokenized** — hover tints → `--hover-tint` (white-alpha dark / black-alpha light); MRI node label → `color-mix` on `--bg`. No dark-only literals remain in component code.
- ✅ **Toggle** in Settings → Appearance; **defaults to dark** ("dark is primary"). `color-scheme` set per theme for native controls.
- ◐ **Remaining for build:** `rgba(primary,α)` accent tints still blend acceptably in both themes but should become `color-mix`/alpha tokens under the lint; a formal AA contrast sweep of light mode; optional `prefers-color-scheme` auto-default and persistence.

## 6.3 Cognitive-load refinements (owner decisions applied)

- ✅ **Overview progressive disclosure** — restructured to a pinned **Confidence hero + one 'needs attention most' line**; Clarity·Alignment·Feasibility, Reliability, Attention (heatmap), Recommendations, and Project summary are **single-open** collapsible sections (opening one closes the others), so only hero + one section is ever visible. Canonical §D order preserved.
- ✅ **'CAF' removed from the UI** — surfaced as **Clarity · Alignment · Feasibility** everywhere (Overview section, heatmap axes, 'Dimensions' toggle, finding panel 'What this weakens', all-findings grouping, export copy, analysis traces). CAF stays the internal canonical term (code + a discreet 'Internally: CAF' hover). **New user-facing-label Disambiguation entry required** (owner ratifies), same pattern as Initial/Extended Analysis.
- ✅ **Right panel = chat only** — the dense persistent metrics block was removed from the right panel. **Outcome Confidence relocated to a top-bar pill** (band + reliability qualifier, always visible) with a click **popover** showing the three dimensions (first-level) + 'Open full breakdown → Overview'. Metrics now live in exactly one place (top bar), not duplicated. Also: analysis 'traces' collapse to a one-line expandable summary; the 'Context' pill line and verbose footer text were trimmed. (This reverses the earlier 'remove the redundant top-bar pill' call — now justified because the right-panel copy is gone, so it is no longer a duplicate.)
- ✅ **Recommendation selection de-duplicated → Panel Model** — the standalone Recommendations center tab was **removed**. Selection of a Selected Path now happens **only in the finding context** (finding panel), per the owner-ratified **Finding & Recommendation Surface Reconciliation Decision 001 (2026-05-31, Option A / Panel Model)** and RECOMMENDATION_PANEL_SPECIFICATION_V1 (RP-12: "contextual decision-support surface subordinate to the Finding Panel — not a standalone destination"). Notably, RECOMMENDATION_PRESENTATION §B: "recommendations do not exist outside Findings in the UI — there is no 'orphan recommendation' surface" — so a project-wide recommendations roll-up was **not** built (it would be an orphan surface). The Overview keeps a canonical §D **Recommendations summary** (pointer only), now routing into the Findings panel. Chat/MRI-popover links repointed to the finding. **Spec note:** RELEASE_1_UI_SPECIFICATION_V1 / UI_SCREEN_INVENTORY still list a "Recommendation Workspace" — these predate Decision 001 and need normalization (owner task), not the prototype.
- ✅ **Manual 'Reanalyze' removed** — reanalysis is **event-driven only** (triggered by a change in project state): editing an artifact auto-runs it (Saved→stale→Reanalyzing→Up to date), and 'Update the plan' on a finding auto-reanalyzes. No user-initiated reanalyze buttons remain. Consistent with 'only reanalysis changes assessment' + the Orientation State model ('Reanalysis Running — after user-changed information'). **Reconcile with** `ARTIFACT_AUTHORING_AND_EDITING_WORKFLOW` / `ORIENTATION_STATE_MODEL` at build to confirm no spec-defined explicit user-trigger is expected.
